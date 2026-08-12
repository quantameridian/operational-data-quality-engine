from pathlib import Path

import duckdb
import pytest

from quality_engine.ingest import load_operational_tracker
from quality_engine.schema import REQUIRED_FIELDS, SchemaValidationError

SAMPLE_FILE = Path("data/raw/operational_tracker_sample.csv")


def _create_database(path: Path, table: str = "operational_tracker") -> None:
    records = load_operational_tracker(SAMPLE_FILE)
    columns = ", ".join(f'"{field}" VARCHAR' for field in REQUIRED_FIELDS)
    placeholders = ", ".join("?" for _ in REQUIRED_FIELDS)
    with duckdb.connect(str(path)) as connection:
        connection.execute(f'CREATE TABLE "{table}" ({columns})')
        connection.executemany(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            [[record[field] for field in REQUIRED_FIELDS] for record in records[:2]],
        )


def test_duckdb_input_uses_the_same_record_contract(tmp_path: Path) -> None:
    database = tmp_path / "tracker.duckdb"
    _create_database(database)

    records = load_operational_tracker(database)

    assert len(records) == 2
    assert records[0]["record_id"] == "OP-1001"
    assert tuple(records[0]) == REQUIRED_FIELDS


def test_duckdb_input_rejects_unsafe_table_names(tmp_path: Path) -> None:
    database = tmp_path / "tracker.duckdb"
    _create_database(database)

    with pytest.raises(ValueError, match="table names"):
        load_operational_tracker(database, 'tracker"; DROP TABLE tracker; --')


def test_duckdb_input_rejects_missing_contract_fields(tmp_path: Path) -> None:
    database = tmp_path / "tracker.duckdb"
    with duckdb.connect(str(database)) as connection:
        connection.execute("CREATE TABLE operational_tracker (record_id VARCHAR)")

    with pytest.raises(SchemaValidationError):
        load_operational_tracker(database)


def test_input_rejects_unknown_file_types(tmp_path: Path) -> None:
    path = tmp_path / "tracker.parquet"
    path.touch()

    with pytest.raises(ValueError, match="Input must be"):
        load_operational_tracker(path)
