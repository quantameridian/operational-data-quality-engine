"""Command line entry point for generating data quality outputs."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from quality_engine.ingest import load_operational_tracker
from quality_engine.reporting import write_exception_register
from quality_engine.rules import run_core_rules
from quality_engine.scoring import calculate_quality_summary, write_quality_summary

DEFAULT_INPUT = Path("data/raw/operational_tracker_sample.csv")
DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_REPORT_DATE = date(2026, 6, 19)


def _parse_report_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        message = f"Invalid report date '{value}'. Use YYYY-MM-DD."
        raise argparse.ArgumentTypeError(message) from exc


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Generate operational data quality exception and summary outputs."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Input tracker CSV path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--report-date",
        type=_parse_report_date,
        default=DEFAULT_REPORT_DATE,
        help=f"Report date used for readiness indicators. Default: {DEFAULT_REPORT_DATE}",
    )
    return parser


def run(input_path: Path, output_dir: Path, report_date: date) -> int:
    """Generate the exception register and quality summary."""

    records = load_operational_tracker(input_path)
    issues = run_core_rules(records, report_date)
    summary = calculate_quality_summary(records, issues, report_date)

    exception_path = write_exception_register(issues, output_dir / "exception_register.csv")
    summary_path = write_quality_summary(summary, report_date, output_dir / "quality_summary.md")

    print(f"Records checked: {summary.record_count}")
    print(f"Exceptions found: {summary.exception_count}")
    print(f"Readiness score: {summary.score}/100 ({summary.readiness_band})")
    print(f"Wrote exception register: {exception_path}")
    print(f"Wrote quality summary: {summary_path}")

    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args.input, args.output_dir, args.report_date)


if __name__ == "__main__":
    raise SystemExit(main())
