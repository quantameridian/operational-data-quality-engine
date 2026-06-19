# Reviewer Guide

## What To Review First

1. [README.md](../README.md) for the business problem, architecture, and rule table.
2. [outputs/quality_summary.md](../outputs/quality_summary.md) for the generated reporting-readiness summary.
3. [docs/exception-register-preview.md](exception-register-preview.md) for a fast markdown preview of exceptions.
4. [outputs/exception_register.csv](../outputs/exception_register.csv) for the full generated exception register.
5. [tests](../tests) for rule, scoring, reporting, schema, and CLI test coverage.

## What This Repository Proves

| Skill | Evidence |
| --- | --- |
| Python package design | `src/quality_engine` separates ingest, schema, rules, scoring, reporting, and CLI concerns |
| Data-quality rule design | Business-readable rules produce record-level validation issues with severity and actions |
| Testable analytics logic | Pytest coverage checks rule behavior, scoring math, output writing, and CLI execution |
| Reporting readiness | The engine produces a quality summary and exception register from synthetic tracker data |
| Public repo hygiene | CI, Ruff, pytest, `pip-audit`, CodeQL, OpenSSF Scorecard, and security posture docs are present |

## Fast Local Review

Use Python 3.11 or newer.

```bash
make install
make audit
make qa
```

Expected result:

- dependency audit reports no known vulnerabilities;
- Ruff passes;
- pytest passes;
- `outputs/exception_register.csv`, `outputs/quality_summary.md`, and `docs/exception-register-preview.md` are regenerated.

## Good Reviewer Questions

- Are the rule names understandable to a business user?
- Does each rule produce a clear owner action?
- Are severity and scoring assumptions explicit enough to challenge?
- Are synthetic-data limitations visible?
- Would this be safe to run before a management reporting cycle?

## Current Limitations

- Batch CSV processing only.
- Synthetic data only.
- No production scheduler, database integration, or access-control layer.
- The score is an explainable readiness signal, not a statistical model.
