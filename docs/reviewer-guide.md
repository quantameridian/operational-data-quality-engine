# Reviewer Guide

This guide is written for someone reviewing the repository from the outside: a hiring reviewer, technical interviewer, engineering lead, or portfolio reviewer. The aim is to make the evidence easy to inspect without implying this is a live production system.

## What To Review First

1. [README.md](../README.md) for the business problem, architecture, and rule table.
2. [outputs/quality_summary.md](../outputs/quality_summary.md) for the generated readiness summary.
3. [docs/exception-register-preview.md](exception-register-preview.md) for a fast markdown preview of exceptions.
4. [contracts/operational-tracker-contract.json](../contracts/operational-tracker-contract.json) for the schema, output, rule, and readiness contract.
5. [docs/operational-runbook.md](operational-runbook.md) for how a reporting team would respond to the results.
6. [docs/commercial-review-scorecard.md](commercial-review-scorecard.md) for the plain assessment of the repo.
7. [outputs/exception_register.csv](../outputs/exception_register.csv) for the full generated exception register.
8. [tests](../tests) for rule, scoring, reporting, schema, contract, and CLI test coverage.

## What This Repository Proves

| Skill | Evidence |
| --- | --- |
| Python package design | `src/quality_engine` separates ingest, schema, rules, scoring, reporting, and CLI concerns |
| Data quality rule design | Rules written in business language produce record level issues with severity and actions |
| Data contract discipline | The JSON contract is tested against the Python schema and generated output expectations |
| Testable analytics logic | Pytest coverage checks rule behavior, scoring math, output writing, and CLI execution |
| Reporting cycle operation | The runbook explains readiness states, escalation triggers, and correction ownership |
| Reporting readiness | The engine produces a quality summary and exception register from synthetic tracker data |
| Public repo hygiene | CI, Ruff, pytest, `pip-audit`, CodeQL, OpenSSF Scorecard, and security posture docs are present |

## Portfolio Reading

The strongest evidence is the route from rule design to runnable output. Start with `docs/data-quality-rules.md`, then compare it with `src/quality_engine/rules.py`, the tests, and the generated files in `outputs/`. That path is what a reviewer should judge. The repo is not trying to look larger than it is.

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
- Are synthetic data limitations visible?
- Would this be safe to run before a management reporting cycle?

## Current Limitations

- Batch CSV processing only.
- Synthetic data only.
- No production scheduler, database integration, or access control layer.
- The score is an explainable readiness signal, not a statistical model.

## Strongest Interview Angle

Use this repo to discuss how to design data quality checks that people can actually act on: rule wording, severity, exception ownership, output format, tests, and the boundary between a local engine and a production service.
