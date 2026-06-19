"""Exception register generation for validation issues."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

from quality_engine.rules import ValidationIssue

EXCEPTION_REGISTER_FIELDS: tuple[str, ...] = (
    "rule_id",
    "rule_name",
    "severity",
    "record_id",
    "field",
    "issue",
    "recommended_action",
)


def issue_to_exception_row(issue: ValidationIssue) -> dict[str, str]:
    """Convert an internal validation issue to an exception register row."""

    return {
        "rule_id": issue.rule_id,
        "rule_name": issue.rule_name,
        "severity": issue.severity,
        "record_id": issue.record_id,
        "field": issue.field,
        "issue": issue.message,
        "recommended_action": issue.recommended_action,
    }


def build_exception_register(issues: Iterable[ValidationIssue]) -> list[dict[str, str]]:
    """Create exception register rows from validation issues."""

    return [issue_to_exception_row(issue) for issue in issues]


def write_exception_register(
    issues: Iterable[ValidationIssue],
    output_path: str | Path,
) -> Path:
    """Write validation issues to an exception register CSV."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_exception_register(issues)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=EXCEPTION_REGISTER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return path
