# Operational Runbook

## Purpose

This runbook defines how the data quality engine would be used in a reporting
cycle. It is written for portfolio review and uses synthetic data only.

The engine should not only find bad records. It should help a reporting owner
decide what happens next: publish, publish with caveats, escalate, or stop.

## Reporting Cycle

| Step | Owner role | Command or artifact | Expected evidence |
| --- | --- | --- | --- |
| Confirm source receipt | Reporting owner | `data/raw/operational_tracker_sample.csv` | Source file has expected columns |
| Validate and run checks | Analytics or assurance owner | `make run` | Exception register and quality summary generated |
| Review high severity issues | Reporting assurance owner | `outputs/exception_register.csv` | Important issues assigned or caveated |
| Decide readiness state | Reporting owner and decision owner | `outputs/quality_summary.md` | Ready, ready with caveats, review required, or not ready |
| Assign corrections | Source data owner | Exception register actions | Owner, due date, and closure evidence agreed |
| Refresh preview | Analytics or assurance owner | `make preview` | Markdown preview refreshed |
| Capture learning | Reporting assurance owner | Rule catalogue update | Repeated failure patterns reviewed |

## Readiness Decision Rules

| State | Trigger | Reporting action |
| --- | --- | --- |
| Ready | No important exceptions affect headline outputs and score is at least 90 | Publish normally |
| Ready with caveats | Issues exist but are owned and do not invalidate headline interpretation | Publish with visible caveats |
| Review required | Important issues affect headline interpretation or repeated failures recur | Escalate before formal use |
| Not ready | Schema validation fails or score is below 60 | Do not use for formal decision support |

## Failure Handling

| Failure mode | Likely cause | Response |
| --- | --- | --- |
| Schema validation fails | Source extract changed without notice | Stop run, compare source fields to `contracts/operational-tracker-contract.json`, then agree a source fix or contract change |
| Duplicate record spike | Source tracker has duplicate IDs or merged extracts | Hold metrics affected by duplicates and assign source owner review |
| Missing owner spike | Ownership process is incomplete | Caveat accountability metrics and assign owner correction |
| Closed missing evidence spike | Closure process is not enforcing evidence | Escalate to assurance owner before closed performance reporting |
| Stale record spike | Review cadence is not being followed | Publish with caveat only if decision owner accepts the risk |

## What To Inspect

A reviewer should be able to inspect:

- the schema and rule contract in `contracts/operational-tracker-contract.json`;
- the implemented rules in `src/quality_engine/rules.py`;
- generated outputs in `outputs/`;
- the markdown exception preview in `docs/exception-register-preview.md`;
- tests that prove the contract still matches the Python schema.

## Limitations

This is a local batch runbook, not a production operating procedure. It does not
include authentication, a scheduler, database access, monitoring alerts, or an
enterprise incident management integration.
