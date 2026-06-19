import csv
from pathlib import Path

from quality_engine.ingest import load_operational_tracker
from quality_engine.reporting import (
    EXCEPTION_REGISTER_FIELDS,
    build_exception_register,
    write_exception_register,
)
from quality_engine.rules import run_core_rules

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")


def test_build_exception_register_maps_validation_issues_to_public_columns() -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records)

    register = build_exception_register(issues)

    assert len(register) == 29
    assert tuple(register[0]) == EXCEPTION_REGISTER_FIELDS
    assert register[0] == {
        "rule_id": "DQ001",
        "rule_name": "Missing owner",
        "severity": "High",
        "record_id": "OP-1003",
        "field": "owner_name,owner_email",
        "issue": "Record is missing owner details needed for follow-up.",
        "recommended_action": "Add owner name and owner email before reporting.",
    }


def test_write_exception_register_creates_csv_from_actual_rules(tmp_path: Path) -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records)
    output_path = tmp_path / "exception_register.csv"

    written_path = write_exception_register(issues, output_path)

    assert written_path == output_path
    with output_path.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 29
    assert rows[0]["rule_id"] == "DQ001"
    assert rows[-1]["record_id"] == "OP-1024"
    assert rows[-1]["rule_id"] == "DQ010"
    assert set(rows[0]) == set(EXCEPTION_REGISTER_FIELDS)
