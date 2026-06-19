"""Schema definitions for the operational tracker sample data."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

REQUIRED_FIELDS: tuple[str, ...] = (
    "record_id",
    "service_area",
    "reporting_unit",
    "owner_name",
    "owner_email",
    "review_cycle",
    "status",
    "risk_rating",
    "evidence_link",
    "last_reviewed_date",
    "next_review_due",
    "action_owner",
    "action_due_date",
    "issue_category",
    "closure_evidence",
    "notes",
)

VALID_STATUSES: tuple[str, ...] = (
    "open",
    "in_review",
    "blocked",
    "closed",
    "cancelled",
)

COMPLETION_STATUSES: tuple[str, ...] = ("closed", "complete")


@dataclass(frozen=True)
class SchemaValidationError(ValueError):
    """Raised when input data does not match the required tracker schema."""

    missing_fields: tuple[str, ...]

    def __str__(self) -> str:
        missing = ", ".join(self.missing_fields)
        return f"Missing required field(s): {missing}"


def missing_required_fields(fieldnames: Iterable[str] | None) -> tuple[str, ...]:
    """Return required fields that are absent from a CSV header."""

    available = set(fieldnames or ())
    return tuple(field for field in REQUIRED_FIELDS if field not in available)


def validate_required_fields(fieldnames: Iterable[str] | None) -> None:
    """Raise a schema error when any required field is missing."""

    missing = missing_required_fields(fieldnames)
    if missing:
        raise SchemaValidationError(missing)
