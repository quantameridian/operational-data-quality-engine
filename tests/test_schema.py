from pathlib import Path

import pytest

from quality_engine.ingest import load_operational_tracker
from quality_engine.schema import (
    REQUIRED_FIELDS,
    SchemaValidationError,
    missing_required_fields,
    validate_required_fields,
)

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")


def test_required_fields_are_present_for_sample_file() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    assert len(records) == 30
    assert set(REQUIRED_FIELDS).issubset(records[0])


def test_missing_required_fields_are_reported_in_schema_order() -> None:
    fieldnames = ["record_id", "status", "risk_rating"]

    assert missing_required_fields(fieldnames) == (
        "service_area",
        "reporting_unit",
        "owner_name",
        "owner_email",
        "review_cycle",
        "evidence_link",
        "last_reviewed_date",
        "next_review_due",
        "action_owner",
        "action_due_date",
        "issue_category",
        "closure_evidence",
        "notes",
    )


def test_validate_required_fields_raises_for_missing_fields() -> None:
    with pytest.raises(SchemaValidationError) as exc_info:
        validate_required_fields(["record_id", "status"])

    assert exc_info.value.missing_fields[:3] == (
        "service_area",
        "reporting_unit",
        "owner_name",
    )
    assert "Missing required field" in str(exc_info.value)


def test_validate_required_fields_accepts_complete_header() -> None:
    validate_required_fields(REQUIRED_FIELDS)
