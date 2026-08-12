# Performance

## What is measured

`scripts/benchmark_engine.py` builds deterministic records in memory and runs the configured rule set. Every hundredth record has a missing owner email, which prevents a fast path that only sees valid data.

The benchmark excludes CSV parsing, database writes, report rendering, network transfer, process startup, and concurrency. It measures core rule throughput only.

## Local baseline

Command:

```bash
python scripts/benchmark_engine.py --rows 100000 --report-date 2026-06-19
```

Observed on 12 August 2026 with Python 3.12.13 on arm64 macOS:

| Rows | Exceptions | Elapsed | Throughput |
| ---: | ---: | ---: | ---: |
| 100,000 | 1,000 | 1.1579 seconds | 86,363 rows per second |

This is a reference result from one local run, not a service level objective. CI runs 10,000 rows as a smoke check and reports the measured value without using a brittle timing assertion.

## Scale decision

The current list based design is appropriate for a small batch control. It materialises records and duplicate counts in memory. Before using it for much larger files, measure peak memory, test chunked ingestion, decide whether duplicate detection belongs in SQL, and include database and report output in the workload test.
