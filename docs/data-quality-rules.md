# Data Quality Rules

## Purpose

This document defines the rule catalogue for the operational data quality engine. The rules are written in business language first so they can be reviewed alongside the generated exception register.

Each implemented rule should return enough information to populate an exception register:

- `record_id`
- `rule_id`
- rule name
- severity
- failed field or fields
- issue description
- recommended action

## Severity model

| Severity | Meaning |
| --- | --- |
| Critical | The record creates a material reporting or escalation risk if not reviewed |
| High | The record is not reliable enough for reporting without correction or explanation |
| Medium | The record may be usable but needs review before reporting |
| Low | The record has a minor quality issue or useful improvement |

## Rule catalogue

| Rule ID | Rule name | Status | Severity | Business meaning | Recommended action |
| --- | --- | --- | --- | --- | --- |
| DQ001 | Missing owner | Implemented | High | A record does not have enough owner detail to support follow-up. | Add owner name and owner email before reporting. |
| DQ002 | Invalid status | Implemented | High | The status value does not match the approved status list, which weakens reporting consistency. | Correct the status to an approved value. |
| DQ003 | Missing evidence | Planned | Medium | A record that should have supporting review evidence does not include an evidence reference. | Add an evidence reference or confirm why evidence is not required. |
| DQ004 | Duplicate record | Implemented | High | The same `record_id` appears more than once, creating risk of double counting or conflicting updates. | Review duplicate rows and retain a single authoritative record. |
| DQ005 | Overdue review | Implemented | Medium | The `next_review_due` date has passed and the record is unresolved. | Complete the review and update the next review due date. |
| DQ006 | Stale record | Implemented | Medium | An unresolved record has gone more than two expected review cycles without review. | Review the record and confirm whether it remains current. |
| DQ007 | Invalid review cycle | Implemented | Medium | The next review due date is earlier than or equal to the last reviewed date. | Correct review dates so the next review falls after the last review. |
| DQ008 | High-risk issue without action owner | Planned | Critical | A high or critical risk record is unresolved and has no clear action owner. | Assign an accountable owner and confirm the next action before reporting. |
| DQ009 | Closed item missing closure evidence | Implemented | High | A closed record does not have closure evidence. | Add closure evidence or reopen the record. |
| DQ010 | Overdue action | Implemented | High | A record has passed its action due date and is unresolved. | Confirm current status, agree recovery action, or escalate the overdue item. |
| DQ011 | Invalid risk rating | Planned | Medium | The risk rating does not match the approved list. | Correct the risk rating to an approved value. |
| DQ012 | Escalation flag inconsistent with risk | Planned | Medium | A high or critical risk item is not marked for escalation. | Review escalation status and update the flag where management attention is required. |

## Approved values to define

The implementation uses reference values for:

- status;
- review cycle.

Future rules may add reference values for risk rating, record type, owning team, and escalation flags.

## Testing expectations

Each rule should have:

- at least one passing example;
- at least one failing example;
- a test for missing or blank values where relevant;
- a test for the exception fields returned by the rule.
