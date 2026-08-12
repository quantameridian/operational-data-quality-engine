# Data Quality Rules

## Policy model

The rule catalogue is implemented in `src/quality_engine/rules.py`. Operational settings live in `config/default-rules.yml` so a reviewer can see which rules are active, which severity each carries, how many review cycles make a record stale, and whether high severity failures block routine reporting.

Each failure contains:

- rule identifier and name;
- severity;
- source record identifier;
- failed field or fields;
- a plain description;
- a recommended owner action.

## Severity

| Severity | Use |
| --- | --- |
| Critical | Material reporting or escalation risk that needs immediate review |
| High | The record is not reliable enough for uncaveated reporting |
| Medium | The record may be usable after review and a visible decision |
| Low | A minor issue that does not change the reporting decision alone |

## Catalogue

| Rule | Trigger | Default severity | Owner response |
| --- | --- | --- | --- |
| DQ001 | Owner name or email is blank | High | Add accountable owner details |
| DQ002 | Status is not approved | High | Correct the lifecycle state |
| DQ003 | An unresolved item has no action owner | High | Assign the next action |
| DQ004 | A nonblank record identifier occurs more than once | High | Resolve duplicates and retain one authority |
| DQ005 | An unresolved review due date is before the report date | Medium | Complete the review and set the next date |
| DQ006 | An unresolved record has missed the configured review cycles | Medium | Confirm currency and update the review |
| DQ007 | Next review is not after last review | Medium | Correct the date sequence |
| DQ008 | A noncancelled item has no review evidence reference | Medium | Add evidence or record an approved exception |
| DQ009 | A completed item has no closure evidence | High | Add closure evidence or reopen the item |
| DQ010 | An unresolved action due date is before the report date | High | Recover, replan, or escalate the action |
| DQ011 | Risk rating is not approved | Medium | Correct the reference value |
| DQ012 | Review cycle is not approved | Medium | Correct the reference value |
| DQ013 | A nonblank date is not a valid `YYYY-MM-DD` calendar date | Medium | Correct the date before reporting |

## Rule change control

A rule change needs matching updates to code, configuration, contract, tests, sample output, and documentation. `make qa` regenerates the review evidence. The manifest hash changes when the policy changes, which makes that change visible to downstream review.

Rules indicate likely reporting risk. They do not prove an evidence reference exists, that an owner is the right person, or that a source statement is factually true.
