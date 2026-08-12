import hashlib
from datetime import date
from pathlib import Path

from quality_engine.context import RunContext, sha256_file


def test_run_context_records_reproducible_lineage(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    config = tmp_path / "rules.yml"
    source.write_text("record_id\nCASE-1\n", encoding="utf-8")
    config.write_text("version: '1'\n", encoding="utf-8")

    context = RunContext.build(source, config, date(2026, 6, 19), "1.0.0")

    expected_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    assert sha256_file(source) == expected_hash
    assert context.input_sha256 == expected_hash
    assert context.run_id == f"dq-2026-06-19-{expected_hash[:10]}"
    assert context.input_format == "csv"
    assert context.as_dict()["engine_version"] == "0.2.0"
