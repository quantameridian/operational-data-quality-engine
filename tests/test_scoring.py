from datetime import date
from pathlib import Path

from quality_engine.ingest import load_operational_tracker
from quality_engine.rules import run_core_rules
from quality_engine.scoring import (
    calculate_quality_summary,
    render_quality_summary_markdown,
    write_quality_summary,
)

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")
REPORT_DATE = date(2026, 6, 19)


def test_calculate_quality_summary_uses_records_exceptions_and_readiness_indicators() -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records, REPORT_DATE)

    summary = calculate_quality_summary(records, issues, REPORT_DATE)

    assert summary.record_count == 30
    assert summary.exception_count == 39
    assert summary.severity_counts == {"High": 16, "Medium": 23}
    assert summary.high_risk_unresolved_exception_count == 7
    assert summary.missing_evidence_count == 8
    assert summary.overdue_review_count == 10
    assert summary.score == 12
    assert summary.readiness_band == "Not ready for reporting"


def test_quality_summary_markdown_explains_score_inputs() -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records, REPORT_DATE)
    summary = calculate_quality_summary(records, issues, REPORT_DATE)

    markdown = render_quality_summary_markdown(summary, REPORT_DATE)

    assert "Score: 12/100" in markdown
    assert "Records checked: 30" in markdown
    assert "Validation exceptions: 39" in markdown
    assert "It does not prove" in markdown


def test_write_quality_summary_creates_markdown_file(tmp_path: Path) -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records, REPORT_DATE)
    summary = calculate_quality_summary(records, issues, REPORT_DATE)
    output_path = tmp_path / "quality_summary.md"

    written_path = write_quality_summary(summary, REPORT_DATE, output_path)

    assert written_path == output_path
    assert output_path.read_text(encoding="utf-8").startswith("# Quality Summary")


def test_empty_input_is_not_ready_for_reporting() -> None:
    summary = calculate_quality_summary([], [], REPORT_DATE)

    assert summary.record_count == 0
    assert summary.exception_rate_penalty == 100
    assert summary.score == 0
    assert summary.readiness_band == "Not ready for reporting"


def test_high_severity_exception_blocks_routine_ready_band() -> None:
    records = load_operational_tracker("data/scenarios/tracker_clean.csv")
    issue = run_core_rules(records, REPORT_DATE)
    assert issue == []

    high_issue = run_core_rules([{**records[0], "owner_email": ""}, *records[1:]], REPORT_DATE)
    summary = calculate_quality_summary(records, high_issue, REPORT_DATE)

    assert summary.score >= 85
    assert summary.severity_counts == {"High": 1}
    assert summary.readiness_band == "Usable with review"
