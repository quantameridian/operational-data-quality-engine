from pathlib import Path

from quality_engine.ingest import load_operational_tracker
from quality_engine.rules import (
    find_duplicate_record_ids,
    find_invalid_review_cycles,
    find_invalid_status,
    find_missing_action_owner,
    find_missing_completion_evidence,
    find_missing_owner,
    find_overdue_actions,
    find_overdue_reviews,
    find_stale_records,
    run_core_rules,
)

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")


def test_missing_owner_rule_flags_rows_with_missing_owner_details() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_missing_owner(records)

    assert {issue.record_id for issue in issues} == {"OP-1003", "OP-1014"}
    assert all(issue.rule_id == "DQ001" for issue in issues)


def test_missing_action_owner_rule_flags_unresolved_records_without_action_owner() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_missing_action_owner(records)

    assert [issue.record_id for issue in issues] == ["OP-1006", "OP-1011"]
    assert all(issue.rule_id == "DQ003" for issue in issues)
    assert all(issue.field == "action_owner" for issue in issues)


def test_invalid_status_rule_flags_unapproved_status_values() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_invalid_status(records)

    assert {issue.record_id for issue in issues} == {"OP-1005", "OP-1012", "OP-1024"}
    assert all(issue.field == "status" for issue in issues)


def test_duplicate_record_id_rule_flags_each_duplicate_row() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_duplicate_record_ids(records)

    assert [issue.record_id for issue in issues] == ["OP-1007", "OP-1007"]
    assert all(issue.rule_id == "DQ004" for issue in issues)


def test_missing_completion_evidence_rule_flags_closed_or_complete_rows() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_missing_completion_evidence(records)

    assert {issue.record_id for issue in issues} == {"OP-1009", "OP-1028"}
    assert all(issue.rule_id == "DQ009" for issue in issues)


def test_overdue_review_rule_flags_unresolved_records_past_review_due_date() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_overdue_reviews(records)

    assert [issue.record_id for issue in issues] == [
        "OP-1003",
        "OP-1005",
        "OP-1007",
        "OP-1007",
        "OP-1008",
        "OP-1013",
        "OP-1019",
        "OP-1021",
        "OP-1024",
        "OP-1025",
    ]
    assert all(issue.rule_id == "DQ005" for issue in issues)
    assert all(issue.field == "next_review_due" for issue in issues)


def test_stale_record_rule_flags_records_unreviewed_for_more_than_two_cycles() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_stale_records(records)

    assert {issue.record_id for issue in issues} == {"OP-1008", "OP-1019", "OP-1024", "OP-1025"}
    assert all(issue.rule_id == "DQ006" for issue in issues)


def test_invalid_review_cycle_rule_flags_next_review_before_last_review() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_invalid_review_cycles(records)

    assert [issue.record_id for issue in issues] == ["OP-1021"]
    assert issues[0].field == "last_reviewed_date,next_review_due"
    assert issues[0].rule_id == "DQ007"


def test_overdue_action_rule_flags_unresolved_records_past_action_due_date() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_overdue_actions(records)

    assert [issue.record_id for issue in issues] == [
        "OP-1007",
        "OP-1007",
        "OP-1016",
        "OP-1022",
        "OP-1024",
    ]
    assert all(issue.rule_id == "DQ010" for issue in issues)
    assert all(issue.severity == "High" for issue in issues)


def test_core_rules_return_structured_issues() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = run_core_rules(records)

    assert len(issues) == 31
    assert {issue.rule_id for issue in issues} == {
        "DQ001",
        "DQ002",
        "DQ003",
        "DQ004",
        "DQ005",
        "DQ006",
        "DQ007",
        "DQ009",
        "DQ010",
    }
    assert all(issue.message for issue in issues)
    assert all(issue.recommended_action for issue in issues)
