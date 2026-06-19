"""Data loading helpers for operational tracker files."""

from __future__ import annotations

import csv
from pathlib import Path

from quality_engine.schema import validate_required_fields

Record = dict[str, str]


def load_operational_tracker(path: str | Path) -> list[Record]:
    """Load an operational tracker CSV after checking the expected header."""

    input_path = Path(path)
    with input_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        validate_required_fields(reader.fieldnames)
        return [dict(row) for row in reader]
