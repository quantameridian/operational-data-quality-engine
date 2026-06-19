"""Simple reporting-readiness scoring for operational tracker data."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from quality_engine.ingest import Record
from quality_engine.rules import ValidationIssue

ACTIVE_STATUSES: tuple[str, ...] = ("open", "in_review", "blocked")
UNRESOLVED_STATUSES: tuple[str, ...] = ("open", "in_review", "blocked")
HIGH_RISK_RATINGS: tuple[str, ...] = ("high", "critical")
SEVERITY_WEIGHTS: dict[str, int] = {
    "Critical": 5,
    "High": 2,
    "Medium": 1,
    "Low": 0,
}


@dataclass(frozen=True)
class QualitySummary:
    """Readiness score and the transparent inputs used to calculate it."""

    record_count: int
    exception_count: int
    severity_counts: dict[str, int]
    high_risk_unresolved_exception_count: int
    missing_evidence_count: int
    overdue_review_count: int
    exception_rate_penalty: int
    severity_penalty: int
    high_risk_penalty: int
    missing_evidence_penalty: int
    overdue_review_penalty: int
    score: int
    readiness_band: str


def _is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def _parse_date(value: str | None) -> date | None:
    if _is_blank(value):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _normalise(value: str | None) -> str:
    return (value or "").strip().lower()


def _has_missing_evidence(record: Record) -> bool:
    status = _normalise(record.get("status"))
    risk_rating = _normalise(record.get("risk_rating"))

    if status == "cancelled":
        return False

    review_evidence_missing = _is_blank(record.get("evidence_link"))
    closure_evidence_missing = status in {"closed", "complete"} and _is_blank(
        record.get("closure_evidence")
    )
    high_risk_evidence_missing = risk_rating in HIGH_RISK_RATINGS and review_evidence_missing

    return review_evidence_missing or closure_evidence_missing or high_risk_evidence_missing


def _is_overdue_for_review(record: Record, report_date: date) -> bool:
    status = _normalise(record.get("status"))
    if status not in UNRESOLVED_STATUSES and status not in {"pending", "awaiting_update"}:
        return False

    next_review_due = _parse_date(record.get("next_review_due"))
    return next_review_due is not None and next_review_due < report_date


def _high_risk_unresolved_exception_count(
    records: list[Record],
    issues: list[ValidationIssue],
) -> int:
    issue_record_ids = {issue.record_id for issue in issues}
    count = 0

    for record in records:
        record_id = record.get("record_id", "")
        risk_rating = _normalise(record.get("risk_rating"))
        status = _normalise(record.get("status"))
        has_issue = record_id in issue_record_ids
        missing_action_owner = _is_blank(record.get("action_owner"))

        if (
            risk_rating in HIGH_RISK_RATINGS
            and status in ACTIVE_STATUSES
            and (has_issue or missing_action_owner)
        ):
            count += 1

    return count


def _readiness_band(score: int) -> str:
    if score >= 85:
        return "Ready for routine reporting"
    if score >= 70:
        return "Usable with review"
    if score >= 50:
        return "Needs correction before reporting"
    return "Not ready for reporting"


def calculate_quality_summary(
    records: list[Record],
    issues: list[ValidationIssue],
    report_date: date,
) -> QualitySummary:
    """Calculate a simple, explainable quality score from records and issues."""

    record_count = len(records)
    exception_count = len(issues)
    severity_counts = dict(Counter(issue.severity for issue in issues))
    high_risk_count = _high_risk_unresolved_exception_count(records, issues)
    missing_evidence_count = sum(1 for record in records if _has_missing_evidence(record))
    overdue_review_count = sum(
        1 for record in records if _is_overdue_for_review(record, report_date)
    )

    if record_count == 0:
        exception_rate_penalty = 100
    else:
        exception_rate_penalty = min(30, round((exception_count / record_count) * 40))

    severity_penalty = min(
        25,
        sum(SEVERITY_WEIGHTS.get(issue.severity, 1) for issue in issues),
    )
    high_risk_penalty = min(15, high_risk_count * 5)
    missing_evidence_penalty = min(10, missing_evidence_count)
    overdue_review_penalty = min(10, overdue_review_count)

    score = max(
        0,
        100
        - exception_rate_penalty
        - severity_penalty
        - high_risk_penalty
        - missing_evidence_penalty
        - overdue_review_penalty,
    )

    return QualitySummary(
        record_count=record_count,
        exception_count=exception_count,
        severity_counts=severity_counts,
        high_risk_unresolved_exception_count=high_risk_count,
        missing_evidence_count=missing_evidence_count,
        overdue_review_count=overdue_review_count,
        exception_rate_penalty=exception_rate_penalty,
        severity_penalty=severity_penalty,
        high_risk_penalty=high_risk_penalty,
        missing_evidence_penalty=missing_evidence_penalty,
        overdue_review_penalty=overdue_review_penalty,
        score=score,
        readiness_band=_readiness_band(score),
    )


def render_quality_summary_markdown(summary: QualitySummary, report_date: date) -> str:
    """Render a management-readable markdown quality summary."""

    severity_lines = "\n".join(
        f"- {severity}: {count}" for severity, count in sorted(summary.severity_counts.items())
    )
    if not severity_lines:
        severity_lines = "- No validation exceptions"

    return f"""# Quality Summary

Report date: {report_date.isoformat()}

## Readiness Score

Score: {summary.score}/100

Band: {summary.readiness_band}

## Inputs

- Records checked: {summary.record_count}
- Validation exceptions: {summary.exception_count}
- High-risk unresolved records with current exceptions or missing action owner:
  {summary.high_risk_unresolved_exception_count}
- Records with missing evidence indicators: {summary.missing_evidence_count}
- Records with overdue review date: {summary.overdue_review_count}

## Severity Mix

{severity_lines}

## Penalties Applied

| Component | Penalty |
| --- | ---: |
| Exception rate | {summary.exception_rate_penalty} |
| Severity mix | {summary.severity_penalty} |
| High-risk unresolved exposure | {summary.high_risk_penalty} |
| Missing evidence indicators | {summary.missing_evidence_penalty} |
| Overdue review indicators | {summary.overdue_review_penalty} |

## Interpretation

The score is a practical reporting-readiness indicator. It helps identify whether the
sample tracker is clean enough to use in a management pack or dashboard refresh.

It does not prove that the underlying operational facts are correct, complete, or
suitable for formal assurance.
"""


def write_quality_summary(
    summary: QualitySummary,
    report_date: date,
    output_path: str | Path,
) -> Path:
    """Write the quality summary markdown file."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_quality_summary_markdown(summary, report_date), encoding="utf-8")
    return path
