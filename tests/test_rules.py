from datetime import date
from pathlib import Path

from quality_engine.config import (
    IMPLEMENTED_RULE_IDS,
    EngineConfig,
    ReadinessThresholds,
    RuleSetting,
)
from quality_engine.ingest import load_operational_tracker
from quality_engine.rules import (
    find_duplicate_record_ids,
    find_invalid_dates,
    find_invalid_review_cycle_values,
    find_invalid_review_cycles,
    find_invalid_risk_ratings,
    find_invalid_status,
    find_missing_action_owner,
    find_missing_completion_evidence,
    find_missing_evidence,
    find_missing_owner,
    find_overdue_actions,
    find_overdue_reviews,
    find_stale_records,
    run_core_rules,
)

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")
REPORT_DATE = date(2026, 6, 19)


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

    issues = find_overdue_reviews(records, REPORT_DATE)

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

    issues = find_stale_records(records, REPORT_DATE)

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

    issues = find_overdue_actions(records, REPORT_DATE)

    assert [issue.record_id for issue in issues] == [
        "OP-1007",
        "OP-1007",
        "OP-1016",
        "OP-1022",
        "OP-1024",
    ]
    assert all(issue.rule_id == "DQ010" for issue in issues)
    assert all(issue.severity == "High" for issue in issues)


def test_missing_evidence_rule_flags_non_cancelled_rows_without_evidence() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_missing_evidence(records)

    assert len(issues) == 6
    assert "OP-1006" in {issue.record_id for issue in issues}
    assert all(issue.rule_id == "DQ008" for issue in issues)


def test_invalid_risk_rating_rule_uses_approved_reference_values() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_invalid_risk_ratings(records)

    assert [issue.record_id for issue in issues] == ["OP-1015"]
    assert issues[0].rule_id == "DQ011"


def test_invalid_review_cycle_value_rule_flags_blank_and_unknown_values() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = find_invalid_review_cycle_values(records)

    assert [issue.record_id for issue in issues] == ["OP-1003"]
    assert issues[0].rule_id == "DQ012"


def test_invalid_date_rule_does_not_silently_skip_malformed_calendar_dates() -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    malformed = dict(records[0])
    malformed["last_reviewed_date"] = "2026-02-30"
    malformed["action_due_date"] = "19/06/2026"

    issues = find_invalid_dates([malformed])

    assert len(issues) == 1
    assert issues[0].rule_id == "DQ013"
    assert issues[0].field == "last_reviewed_date,action_due_date"


def test_core_rules_return_structured_issues() -> None:
    records = load_operational_tracker(SAMPLE_FILE)

    issues = run_core_rules(records, REPORT_DATE)

    assert len(issues) == 39
    assert {issue.rule_id for issue in issues} == {
        "DQ001",
        "DQ002",
        "DQ003",
        "DQ004",
        "DQ005",
        "DQ006",
        "DQ007",
        "DQ008",
        "DQ009",
        "DQ010",
        "DQ011",
        "DQ012",
    }
    assert all(issue.message for issue in issues)
    assert all(issue.recommended_action for issue in issues)


def test_rule_configuration_can_disable_a_rule_and_override_severity() -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    settings = {
        rule_id: RuleSetting(enabled=True, severity="Medium") for rule_id in IMPLEMENTED_RULE_IDS
    }
    settings["DQ001"] = RuleSetting(enabled=False, severity="High")
    settings["DQ002"] = RuleSetting(enabled=True, severity="Critical")
    config = EngineConfig(
        version="test",
        rules=settings,
        stale_review_cycles=2,
        readiness=ReadinessThresholds(),
    )

    issues = run_core_rules(records, REPORT_DATE, config)

    assert not any(issue.rule_id == "DQ001" for issue in issues)
    assert all(issue.severity == "Critical" for issue in issues if issue.rule_id == "DQ002")
