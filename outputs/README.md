# Generated Outputs

`make run` rebuilds:

- `exception_register.csv` with one row per failed rule;
- `quality_summary.md` with the score and penalty calculation;
- `quality_report.html` with a management view;
- `run_manifest.json` with run lineage and output hashes;
- `quality_run.duckdb` with source, exception, summary, and manifest tables.

The text outputs are committed for immediate review. The DuckDB file is ignored by Git and uploaded by CI as a short lived artifact.
