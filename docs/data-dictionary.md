# Data Dictionary

## Dataset

`data/raw/operational_tracker_sample.csv`

This file is a synthetic operational tracker for testing data quality rules. It is not client data, workplace data, or an extract from any real system.

## Field definitions

| Field | Type | Required | Description | Example |
| --- | --- | --- | --- | --- |
| `record_id` | string | Yes | Operational tracker identifier. Expected to be unique. | `OP-1001` |
| `service_area` | string | Yes | Broad service area responsible for or affected by the record. | `Customer Support` |
| `reporting_unit` | string | Yes | Reporting unit used for management grouping. | `North Operations` |
| `owner_name` | string | Yes for active records | Person or role recorded as the owner of the tracker row. | `Avery Patel` |
| `owner_email` | string | Yes where owner exists | Generic email address for the owner. Uses `example.com` addresses. | `avery.patel@example.com` |
| `review_cycle` | string | Yes | Expected review frequency. | `monthly` |
| `status` | string | Yes | Current lifecycle state of the record. | `open` |
| `risk_rating` | string | Yes | Reporting risk or operational priority. | `high` |
| `evidence_link` | string | Conditional | Reference to review or supporting evidence. | `evidence/OP-1001-review-note.pdf` |
| `last_reviewed_date` | date | Yes for active records | Date the record was last reviewed. | `2026-06-03` |
| `next_review_due` | date | Yes for active records | Date the next review is due. | `2026-07-03` |
| `action_owner` | string | Yes for active high-risk records | Person or role responsible for the next action. | `Jordan Lee` |
| `action_due_date` | date | Conditional | Due date for the next action. | `2026-06-28` |
| `issue_category` | string | Yes | Generic issue grouping for analysis and exception reporting. | `service_backlog` |
| `closure_evidence` | string | Required for closed records | Reference supporting closure. | `evidence/OP-1004-closure.pdf` |
| `notes` | string | Optional | Short human-readable note explaining the sample scenario. | `Clean open record with current review` |

## Approved values planned for validation

### `review_cycle`

- `weekly`
- `fortnightly`
- `monthly`
- `quarterly`

### `status`

- `open`
- `in_review`
- `blocked`
- `closed`
- `cancelled`

### `risk_rating`

- `low`
- `medium`
- `high`
- `critical`

## Date handling

Dates use ISO format: `YYYY-MM-DD`.

The sample data is designed around a reporting review date of `2026-06-19`. Future validation logic should avoid hard-coding that date in business rules unless a report date parameter is supplied.

## Deliberate quality scenarios

The sample file includes records designed to support rule tests for:

- missing owner details;
- duplicate `record_id` values;
- invalid status values;
- invalid risk rating values;
- overdue reviews;
- stale open records;
- missing evidence;
- high-risk or critical records without action owners;
- closed records without closure evidence;
- action due dates that have passed;
- review cycles where `next_review_due` is earlier than `last_reviewed_date`.

