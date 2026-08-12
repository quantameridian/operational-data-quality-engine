"""Data loading helpers for operational tracker files."""

from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path

import duckdb

from quality_engine.schema import REQUIRED_FIELDS, validate_required_fields

Record = dict[str, str]


def _normalise_database_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def _load_csv(path: Path) -> list[Record]:
    """Load a CSV source after checking the expected header."""

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        validate_required_fields(reader.fieldnames)
        return [dict(row) for row in reader]


def _load_duckdb(path: Path, table: str) -> list[Record]:
    """Load a table from a read only DuckDB database."""

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        raise ValueError("DuckDB table names may contain only letters, numbers, and underscores.")

    with duckdb.connect(str(path), read_only=True) as connection:
        columns = [row[1] for row in connection.execute(f"PRAGMA table_info('{table}')").fetchall()]
        validate_required_fields(columns)
        selected = ", ".join(f'"{field}"' for field in REQUIRED_FIELDS)
        values = connection.execute(f'SELECT {selected} FROM "{table}"').fetchall()

    return [
        {
            field: _normalise_database_value(value)
            for field, value in zip(REQUIRED_FIELDS, row, strict=True)
        }
        for row in values
    ]


def load_operational_tracker(path: str | Path, table: str = "operational_tracker") -> list[Record]:
    """Load an operational tracker from CSV or DuckDB."""

    input_path = Path(path)
    if input_path.suffix.lower() in {".duckdb", ".db"}:
        return _load_duckdb(input_path, table)
    if input_path.suffix.lower() == ".csv":
        return _load_csv(input_path)
    raise ValueError("Input must be a .csv, .duckdb, or .db file.")
