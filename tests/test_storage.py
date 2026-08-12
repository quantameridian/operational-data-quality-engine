from datetime import date
from pathlib import Path

import duckdb

from quality_engine.config import load_engine_config
from quality_engine.context import RunContext
from quality_engine.ingest import load_operational_tracker
from quality_engine.rules import run_core_rules
from quality_engine.scoring import calculate_quality_summary
from quality_engine.storage import write_run_database

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")
CONFIG_FILE = Path("config/default-rules.yml")
REPORT_DATE = date(2026, 6, 19)


def test_run_database_contains_source_exceptions_summary_and_lineage(tmp_path: Path) -> None:
    config = load_engine_config(CONFIG_FILE)
    context = RunContext.build(SAMPLE_FILE, CONFIG_FILE, REPORT_DATE, config.version, "test-run")
    records = load_operational_tracker(SAMPLE_FILE)
    issues = run_core_rules(records, REPORT_DATE, config)
    summary = calculate_quality_summary(records, issues, REPORT_DATE, config.readiness)
    output_path = tmp_path / "quality_run.duckdb"

    written = write_run_database(records, issues, summary, context, output_path)

    assert written == output_path
    with duckdb.connect(str(output_path), read_only=True) as connection:
        assert connection.execute("SELECT count(*) FROM operational_tracker").fetchone()[0] == 30
        assert connection.execute("SELECT count(*) FROM quality_exceptions").fetchone()[0] == 39
        run_id, score = connection.execute("SELECT run_id, score FROM run_summary").fetchone()
        assert (run_id, score) == ("test-run", 12)

    reloaded_records = load_operational_tracker(output_path)
    assert len(reloaded_records) == 30
    assert reloaded_records[0]["record_id"] == "OP-1001"
