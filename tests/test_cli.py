import hashlib
import json
from pathlib import Path

from quality_engine.cli import main

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")
CONFIG_FILE = Path("config/default-rules.yml")


def test_cli_generates_exception_register_and_summary(tmp_path: Path) -> None:
    output_dir = tmp_path / "outputs"

    exit_code = main(
        [
            "--input",
            str(SAMPLE_FILE),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-06-19",
            "--rules-config",
            str(CONFIG_FILE),
        ]
    )

    assert exit_code == 0
    assert (output_dir / "exception_register.csv").exists()
    assert (output_dir / "quality_summary.md").exists()
    assert (output_dir / "quality_report.html").exists()
    assert (output_dir / "run_manifest.json").exists()
    assert "Score: 12/100" in (output_dir / "quality_summary.md").read_text(encoding="utf-8")
    manifest = json.loads((output_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["report_date"] == "2026-06-19"
    assert manifest["result"]["exception_count"] == 39
    assert len(manifest["input_sha256"]) == 64
    for output in manifest["outputs"]:
        output_path = Path(output["path"])
        assert hashlib.sha256(output_path.read_bytes()).hexdigest() == output["sha256"]


def test_cli_returns_quality_gate_exit_code_and_json_events(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "--input",
            str(SAMPLE_FILE),
            "--output-dir",
            str(tmp_path),
            "--report-date",
            "2026-06-19",
            "--rules-config",
            str(CONFIG_FILE),
            "--log-format",
            "json",
            "--fail-below-score",
            "70",
        ]
    )

    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert exit_code == 2
    assert [event["event"] for event in events] == ["run_started", "run_completed"]
    assert events[-1]["score"] == 12


def test_cli_reports_input_failure_as_a_structured_event(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "--input",
            str(tmp_path / "missing.csv"),
            "--report-date",
            "2026-06-19",
            "--rules-config",
            str(CONFIG_FILE),
            "--log-format",
            "json",
        ]
    )

    event = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert event["event"] == "run_failed"
    assert event["error_type"] == "FileNotFoundError"
