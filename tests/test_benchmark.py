from datetime import date

from scripts.benchmark_engine import build_records


def test_benchmark_fixture_is_deterministic_and_exercises_failures() -> None:
    records = build_records(201, date(2026, 6, 19))

    assert len(records) == 201
    assert records[0]["owner_email"] == ""
    assert records[1]["owner_email"] == "owner@example.com"
    assert records[200]["record_id"] == "PERF-0000200"
