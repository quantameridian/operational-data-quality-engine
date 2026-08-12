# Operational Runbook

## Monthly reporting gate

| Step | Owner | Action | Evidence |
| --- | --- | --- | --- |
| Receive source | Reporting owner | Place the approved extract in the controlled input location | Source name and receipt record |
| Confirm run context | Reporting owner | Set report date, rule policy, and run identifier | Command or scheduler parameters |
| Execute gate | Data engineer | Run the CLI with a minimum score agreed for the report | JSON events and process exit code |
| Review exceptions | Data owner and assurance owner | Assign high severity failures and assess metric impact | Exception register |
| Decide use | Reporting owner | Publish, publish with a visible caveat, or stop | Quality report and decision record |
| Retain lineage | Data engineer | Retain the manifest and approved outputs with the report | Hashes and run identifier |

Example gate:

```bash
quality-engine \
  --input approved/monthly_tracker.duckdb \
  --input-table operational_tracker \
  --output-dir run/2026-06 \
  --report-date 2026-06-19 \
  --rules-config config/default-rules.yml \
  --run-id service-review-2026-06 \
  --log-format json \
  --fail-below-score 70 \
  --write-duckdb
```

## Response

| Condition | Response |
| --- | --- |
| Exit code 1 | Stop. Check file availability, schema, table name, date, and policy syntax. Do not use stale output from an earlier run. |
| Exit code 2 | The run completed but failed the agreed score gate. Review high severity exceptions and affected measures before use. |
| High severity duplicate | Hold any count that uses the duplicate key until an authoritative record is agreed. |
| Missing owner on a high risk item | Escalate ownership before presenting the item as controlled. |
| Closed item without evidence | Reopen it or obtain closure evidence before counting it as complete. |
| Large overdue review increase | Check source freshness and review process failure before discussing operational movement. |

## Recovery

The engine does not alter the source, so recovery starts with a corrected extract or an approved policy change. Keep the failed manifest and exceptions when they form part of an audit trail. Run again with a new run identifier when the source changes.

For a production schedule, add alerts that contain the run identifier and failure class but no sensitive record content. Route operational failure separately from a valid run that fails the quality gate.
