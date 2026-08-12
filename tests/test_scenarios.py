from datetime import date
from pathlib import Path

import pytest

from quality_engine.config import load_engine_config
from quality_engine.ingest import load_operational_tracker
from quality_engine.rules import run_core_rules
from quality_engine.scoring import calculate_quality_summary

REPORT_DATE = date(2026, 6, 19)
CONFIG = load_engine_config(Path("config/default-rules.yml"))


@pytest.mark.parametrize(
    "source, expected_score, expected_band",
    [
        ("data/scenarios/tracker_clean.csv", 100, "Ready for routine reporting"),
        ("data/scenarios/tracker_review.csv", 82, "Usable with review"),
        ("data/raw/operational_tracker_sample.csv", 12, "Not ready for reporting"),
    ],
)
def test_decision_scenarios_cover_ready_review_and_blocked_outcomes(
    source: str, expected_score: int, expected_band: str
) -> None:
    records = load_operational_tracker(source)
    issues = run_core_rules(records, REPORT_DATE, CONFIG)
    summary = calculate_quality_summary(records, issues, REPORT_DATE, CONFIG.readiness)

    assert summary.score == expected_score
    assert summary.readiness_band == expected_band
