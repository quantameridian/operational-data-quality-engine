"""Generate synthetic records and measure core rule throughput."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from quality_engine.config import load_engine_config  # noqa: E402
from quality_engine.ingest import Record  # noqa: E402
from quality_engine.rules import run_core_rules  # noqa: E402


def build_records(row_count: int, report_date: date) -> list[Record]:
    """Create deterministic records with a small, repeatable exception rate."""

    records: list[Record] = []
    for index in range(row_count):
        review_date = report_date - timedelta(days=10)
        record: Record = {
            "record_id": f"PERF-{index:07d}",
            "service_area": "Service Operations",
            "reporting_unit": "National Operations",
            "owner_name": "Example Owner",
            "owner_email": "owner@example.com",
            "review_cycle": "monthly",
            "status": "open",
            "risk_rating": "medium",
            "evidence_link": f"evidence/PERF-{index:07d}.pdf",
            "last_reviewed_date": review_date.isoformat(),
            "next_review_due": (review_date + timedelta(days=30)).isoformat(),
            "action_owner": "Example Action Owner",
            "action_due_date": (report_date + timedelta(days=10)).isoformat(),
            "issue_category": "service_control",
            "closure_evidence": "",
            "notes": "Performance fixture",
        }
        if index % 100 == 0:
            record["owner_email"] = ""
        records.append(record)
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure core rule throughput.")
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--report-date", type=date.fromisoformat, required=True)
    args = parser.parse_args(argv)
    if args.rows < 1:
        parser.error("--rows must be positive")

    records = build_records(args.rows, args.report_date)
    config = load_engine_config(PROJECT_ROOT / "config/default-rules.yml")
    started = perf_counter()
    issues = run_core_rules(records, args.report_date, config)
    elapsed_seconds = perf_counter() - started
    result = {
        "elapsed_seconds": round(elapsed_seconds, 4),
        "exception_count": len(issues),
        "rows": args.rows,
        "rows_per_second": round(args.rows / elapsed_seconds),
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
