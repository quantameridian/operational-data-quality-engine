# Business Assumptions

The worked case is a monthly service review. A reporting team receives a tracker of issues, actions, risks, reviews, and closures. The decision is whether the tracker is reliable enough to support the management pack dated 19 June 2026.

## Record assumptions

- Each nonblank `record_id` identifies one authoritative record.
- Active items use `open`, `in_review`, or `blocked`.
- A closed item needs closure evidence.
- An unresolved item needs an action owner.
- Review and action dates use `YYYY-MM-DD`.
- Risk values are `low`, `medium`, `high`, or `critical`.
- Evidence fields are references. This engine does not open or validate the evidence itself.
- Cancelled records do not need review evidence under the current policy.

## Decision assumptions

The score supports a review; it does not replace one. High severity failures can matter even when the aggregate score passes a threshold. A reporting owner still needs to understand which metrics and statements depend on the failed records.

The default readiness bands are configurable:

| Score | Band |
| ---: | --- |
| 85 to 100 | Ready for routine reporting |
| 70 to 84 | Usable with review |
| 50 to 69 | Needs correction before reporting |
| 0 to 49 | Not ready for reporting |

A high or critical exception prevents the routine ready band even when the numeric score is 85 or higher. The result falls to usable with review until that exception is corrected or the policy is changed through its normal approval route.

## Data boundary

All supplied data is synthetic. Names are invented, emails use `example.com`, evidence paths are illustrative, and no record describes a real person, client, employer, or service event.
