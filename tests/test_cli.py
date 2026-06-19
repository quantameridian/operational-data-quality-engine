from pathlib import Path

from quality_engine.cli import main

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")


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
        ]
    )

    assert exit_code == 0
    assert (output_dir / "exception_register.csv").exists()
    assert (output_dir / "quality_summary.md").exists()
    assert "Score: 12/100" in (output_dir / "quality_summary.md").read_text(encoding="utf-8")
