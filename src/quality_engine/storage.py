"""DuckDB persistence for local integration and review."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import duckdb

from quality_engine.context import RunContext
from quality_engine.ingest import Record
from quality_engine.reporting import EXCEPTION_REGISTER_FIELDS, build_exception_register
from quality_engine.rules import ValidationIssue
from quality_engine.schema import REQUIRED_FIELDS
from quality_engine.scoring import QualitySummary


def _create_varchar_table(
    connection: duckdb.DuckDBPyConnection,
    table: str,
    fields: tuple[str, ...],
) -> None:
    columns = ", ".join(f'"{field}" VARCHAR' for field in fields)
    connection.execute(f'CREATE OR REPLACE TABLE "{table}" ({columns})')


def write_run_database(
    records: list[Record],
    issues: list[ValidationIssue],
    summary: QualitySummary,
    context: RunContext,
    output_path: str | Path,
) -> Path:
    """Write source, exception, summary, and lineage tables to DuckDB."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(path)) as connection:
        _create_varchar_table(connection, "operational_tracker", REQUIRED_FIELDS)
        placeholders = ", ".join("?" for _ in REQUIRED_FIELDS)
        if records:
            connection.executemany(
                f"INSERT INTO operational_tracker VALUES ({placeholders})",
                [[record.get(field, "") for field in REQUIRED_FIELDS] for record in records],
            )

        _create_varchar_table(connection, "quality_exceptions", EXCEPTION_REGISTER_FIELDS)
        exception_rows = build_exception_register(issues)
        exception_placeholders = ", ".join("?" for _ in EXCEPTION_REGISTER_FIELDS)
        if exception_rows:
            connection.executemany(
                f"INSERT INTO quality_exceptions VALUES ({exception_placeholders})",
                [[row[field] for field in EXCEPTION_REGISTER_FIELDS] for row in exception_rows],
            )

        connection.execute(
            "CREATE OR REPLACE TABLE run_summary AS SELECT ? AS run_id, ? AS score, "
            "? AS readiness_band, ? AS record_count, ? AS exception_count",
            [
                context.run_id,
                summary.score,
                summary.readiness_band,
                summary.record_count,
                summary.exception_count,
            ],
        )
        connection.execute(
            "CREATE OR REPLACE TABLE run_manifest AS SELECT ? AS run_id, ? AS context_json, "
            "? AS quality_summary_json",
            [context.run_id, json.dumps(context.as_dict()), json.dumps(asdict(summary))],
        )
    return path
