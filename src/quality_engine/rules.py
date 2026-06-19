"""Initial data quality rules for operational tracker records."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime

from quality_engine.ingest import Record
from quality_engine.schema import COMPLETION_STATUSES, VALID_STATUSES

DEFAULT_REPORT_DATE = date(2026, 6, 19)
UNRESOLVED_STATUSES: tuple[str, ...] = (
    "open",
    "in_review",
    "blocked",
    "pending",
    "awaiting_update",
)
REVIEW_CYCLE_DAYS: dict[str, int] = {
    "weekly": 7,
    "fortnightly": 14,
    "monthly": 30,
    "quarterly": 90,
}


@dataclass(frozen=True)
class ValidationIssue:
    """A row-level data quality issue found by a rule."""

    rule_id: str
    rule_name: str
    severity: str
    record_id: str
    field: str
    message: str
    recommended_action: str


def _is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def _normalise(value: str | None) -> str:
    return (value or "").strip().lower()


def _parse_date(value: str | None) -> date | None:
    if _is_blank(value):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _is_unresolved(record: Record) -> bool:
    return _normalise(record.get("status")) in UNRESOLVED_STATUSES


def find_missing_owner(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag records where owner name or owner email is missing."""

    issues: list[ValidationIssue] = []
    for record in records:
        missing_fields = [
            field for field in ("owner_name", "owner_email") if _is_blank(record.get(field))
        ]
        if missing_fields:
            issues.append(
                ValidationIssue(
                    rule_id="DQ001",
                    rule_name="Missing owner details",
                    severity="High",
                    record_id=record.get("record_id", ""),
                    field=",".join(missing_fields),
                    message="Record is missing owner details needed for follow-up.",
                    recommended_action="Add owner name and owner email before reporting.",
                )
            )
    return issues


def find_missing_action_owner(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag unresolved records without an accountable action owner."""

    issues: list[ValidationIssue] = []
    for record in records:
        if _is_unresolved(record) and _is_blank(record.get("action_owner")):
            issues.append(
                ValidationIssue(
                    rule_id="DQ003",
                    rule_name="Missing action owner",
                    severity="High",
                    record_id=record.get("record_id", ""),
                    field="action_owner",
                    message="Unresolved record does not have an action owner.",
                    recommended_action=(
                        "Assign an action owner before the record is used in reporting."
                    ),
                )
            )
    return issues


def find_invalid_status(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag status values outside the approved status list."""

    valid_statuses = set(VALID_STATUSES)
    issues: list[ValidationIssue] = []
    for record in records:
        status = record.get("status", "")
        if status not in valid_statuses:
            issues.append(
                ValidationIssue(
                    rule_id="DQ002",
                    rule_name="Invalid status",
                    severity="High",
                    record_id=record.get("record_id", ""),
                    field="status",
                    message=f"Status '{status}' is not an approved value.",
                    recommended_action="Update the status to an approved value.",
                )
            )
    return issues


def find_duplicate_record_ids(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag records sharing the same non-blank record identifier."""

    materialised = list(records)
    counts = Counter(
        record.get("record_id", "").strip()
        for record in materialised
        if not _is_blank(record.get("record_id"))
    )
    duplicate_ids = {record_id for record_id, count in counts.items() if count > 1}

    return [
        ValidationIssue(
            rule_id="DQ004",
            rule_name="Duplicate record ID",
            severity="High",
            record_id=record.get("record_id", ""),
            field="record_id",
            message="Record identifier appears more than once.",
            recommended_action="Review duplicate rows and retain one authoritative record.",
        )
        for record in materialised
        if record.get("record_id", "").strip() in duplicate_ids
    ]


def find_missing_completion_evidence(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag closed or complete records without closure evidence."""

    completion_statuses = set(COMPLETION_STATUSES)
    issues: list[ValidationIssue] = []
    for record in records:
        status = record.get("status", "")
        if status in completion_statuses and _is_blank(record.get("closure_evidence")):
            issues.append(
                ValidationIssue(
                    rule_id="DQ009",
                    rule_name="Closed item missing closure evidence",
                    severity="High",
                    record_id=record.get("record_id", ""),
                    field="closure_evidence",
                    message="Completed record does not include closure evidence.",
                    recommended_action="Add closure evidence or reopen the record.",
                )
            )
    return issues


def find_overdue_reviews(
    records: Iterable[Record],
    report_date: date = DEFAULT_REPORT_DATE,
) -> list[ValidationIssue]:
    """Flag unresolved records where the next review due date has passed."""

    issues: list[ValidationIssue] = []
    for record in records:
        next_review_due = _parse_date(record.get("next_review_due"))
        if _is_unresolved(record) and next_review_due is not None and next_review_due < report_date:
            issues.append(
                ValidationIssue(
                    rule_id="DQ005",
                    rule_name="Overdue review",
                    severity="Medium",
                    record_id=record.get("record_id", ""),
                    field="next_review_due",
                    message="Record review date has passed while the record is unresolved.",
                    recommended_action="Complete the review and update the next review due date.",
                )
            )
    return issues


def find_stale_records(
    records: Iterable[Record],
    report_date: date = DEFAULT_REPORT_DATE,
) -> list[ValidationIssue]:
    """Flag unresolved records that have gone more than two review cycles without review."""

    issues: list[ValidationIssue] = []
    for record in records:
        review_cycle = _normalise(record.get("review_cycle"))
        cycle_days = REVIEW_CYCLE_DAYS.get(review_cycle)
        last_reviewed = _parse_date(record.get("last_reviewed_date"))

        if not _is_unresolved(record) or cycle_days is None or last_reviewed is None:
            continue

        days_since_review = (report_date - last_reviewed).days
        if days_since_review > cycle_days * 2:
            issues.append(
                ValidationIssue(
                    rule_id="DQ006",
                    rule_name="Stale record",
                    severity="Medium",
                    record_id=record.get("record_id", ""),
                    field="last_reviewed_date",
                    message="Unresolved record has not been reviewed within two expected cycles.",
                    recommended_action="Review the record and confirm whether it remains current.",
                )
            )
    return issues


def find_invalid_review_cycles(records: Iterable[Record]) -> list[ValidationIssue]:
    """Flag records where the next review due date is not after the last review date."""

    issues: list[ValidationIssue] = []
    for record in records:
        last_reviewed = _parse_date(record.get("last_reviewed_date"))
        next_review_due = _parse_date(record.get("next_review_due"))

        if (
            last_reviewed is not None
            and next_review_due is not None
            and next_review_due <= last_reviewed
        ):
            issues.append(
                ValidationIssue(
                    rule_id="DQ007",
                    rule_name="Invalid review cycle",
                    severity="Medium",
                    record_id=record.get("record_id", ""),
                    field="last_reviewed_date,next_review_due",
                    message="Next review due date is not after the last reviewed date.",
                    recommended_action=(
                        "Correct review dates so the next review falls after the last review."
                    ),
                )
            )
    return issues


def find_overdue_actions(
    records: Iterable[Record],
    report_date: date = DEFAULT_REPORT_DATE,
) -> list[ValidationIssue]:
    """Flag unresolved records where the action due date has passed."""

    issues: list[ValidationIssue] = []
    for record in records:
        action_due_date = _parse_date(record.get("action_due_date"))
        if _is_unresolved(record) and action_due_date is not None and action_due_date < report_date:
            issues.append(
                ValidationIssue(
                    rule_id="DQ010",
                    rule_name="Overdue action",
                    severity="High",
                    record_id=record.get("record_id", ""),
                    field="action_due_date",
                    message="Action due date has passed while the record is unresolved.",
                    recommended_action=(
                        "Confirm status, agree recovery action, or escalate the overdue item."
                    ),
                )
            )
    return issues


def run_core_rules(
    records: Iterable[Record],
    report_date: date = DEFAULT_REPORT_DATE,
) -> list[ValidationIssue]:
    """Run the first implemented data quality rules."""

    materialised = list(records)
    return [
        *find_missing_owner(materialised),
        *find_missing_action_owner(materialised),
        *find_invalid_status(materialised),
        *find_duplicate_record_ids(materialised),
        *find_overdue_reviews(materialised, report_date),
        *find_stale_records(materialised, report_date),
        *find_invalid_review_cycles(materialised),
        *find_missing_completion_evidence(materialised),
        *find_overdue_actions(materialised, report_date),
    ]
