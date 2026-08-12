"""Command line entry point for data quality runs."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import duckdb

from quality_engine.config import ConfigurationError, load_engine_config
from quality_engine.context import RunContext
from quality_engine.ingest import load_operational_tracker
from quality_engine.reporting import (
    write_exception_register,
    write_quality_report_html,
    write_run_manifest,
)
from quality_engine.rules import run_core_rules
from quality_engine.schema import SchemaValidationError
from quality_engine.scoring import calculate_quality_summary, write_quality_summary
from quality_engine.storage import write_run_database

DEFAULT_OUTPUT_DIR = Path("outputs")


def _parse_report_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        message = f"Invalid report date '{value}'. Use YYYY-MM-DD."
        raise argparse.ArgumentTypeError(message) from exc


def _score_threshold(value: str) -> int:
    try:
        score = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Score threshold must be an integer.") from exc
    if not 0 <= score <= 100:
        raise argparse.ArgumentTypeError("Score threshold must be from 0 to 100.")
    return score


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Evaluate operational records and create review evidence."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--input-table", default="operational_tracker")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--rules-config", type=Path, required=True)
    parser.add_argument(
        "--report-date",
        type=_parse_report_date,
        required=True,
        help="Decision date for overdue and staleness rules, in YYYY-MM-DD format.",
    )
    parser.add_argument("--run-id", help="Optional stable identifier for this run.")
    parser.add_argument(
        "--log-format", choices=("text", "json"), default="text", help="Console output format."
    )
    parser.add_argument(
        "--fail-below-score",
        type=_score_threshold,
        default=0,
        help="Return exit code 2 when the readiness score is below this value.",
    )
    parser.add_argument(
        "--write-duckdb",
        action="store_true",
        help="Also write a local DuckDB file with source, exception, and run tables.",
    )
    return parser


def _emit(log_format: str, event: str, **values: object) -> None:
    if log_format == "json":
        print(json.dumps({"event": event, **values}, sort_keys=True))
        return
    if event == "run_completed":
        print(f"Records checked: {values['record_count']}")
        print(f"Exceptions found: {values['exception_count']}")
        print(f"Readiness score: {values['score']}/100 ({values['readiness_band']})")
        print(f"Run manifest: {values['manifest_path']}")
    elif event == "run_failed":
        print(f"Run failed: {values['error']}")


def run(
    input_path: Path,
    output_dir: Path,
    report_date: date,
    rules_config_path: Path,
    input_table: str = "operational_tracker",
    run_id: str | None = None,
    log_format: str = "text",
    fail_below_score: int = 0,
    write_duckdb: bool = False,
) -> int:
    """Execute one data quality run and return a process exit code."""

    try:
        config = load_engine_config(rules_config_path)
        context = RunContext.build(
            input_path=input_path,
            config_path=rules_config_path,
            report_date=report_date,
            config_version=config.version,
            run_id=run_id,
        )
        _emit(log_format, "run_started", **context.as_dict())

        records = load_operational_tracker(input_path, input_table)
        issues = run_core_rules(records, report_date, config)
        summary = calculate_quality_summary(records, issues, report_date, config.readiness)

        exception_path = write_exception_register(issues, output_dir / "exception_register.csv")
        summary_path = write_quality_summary(
            summary, report_date, output_dir / "quality_summary.md"
        )
        html_path = write_quality_report_html(
            summary,
            issues,
            report_date,
            context.run_id,
            output_dir / "quality_report.html",
        )
        if write_duckdb:
            write_run_database(records, issues, summary, context, output_dir / "quality_run.duckdb")
        manifest_path = write_run_manifest(
            context,
            summary,
            [exception_path, summary_path, html_path],
            output_dir / "run_manifest.json",
        )
    except (
        ConfigurationError,
        duckdb.Error,
        FileNotFoundError,
        SchemaValidationError,
        ValueError,
    ) as exc:
        _emit(log_format, "run_failed", error=str(exc), error_type=type(exc).__name__)
        return 1

    _emit(
        log_format,
        "run_completed",
        run_id=context.run_id,
        record_count=summary.record_count,
        exception_count=summary.exception_count,
        score=summary.score,
        readiness_band=summary.readiness_band,
        manifest_path=manifest_path.as_posix(),
    )
    return 2 if summary.score < fail_below_score else 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    args = build_parser().parse_args(argv)
    return run(
        input_path=args.input,
        output_dir=args.output_dir,
        report_date=args.report_date,
        rules_config_path=args.rules_config,
        input_table=args.input_table,
        run_id=args.run_id,
        log_format=args.log_format,
        fail_below_score=args.fail_below_score,
        write_duckdb=args.write_duckdb,
    )


if __name__ == "__main__":
    raise SystemExit(main())
