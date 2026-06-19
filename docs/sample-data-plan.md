# Sample Data Plan

## Dataset

The first sample dataset has been created at `data/raw/operational_tracker_sample.csv`.

## Fields under consideration

- `record_id`
- `service_area`
- `reporting_unit`
- `owner_name`
- `owner_email`
- `review_cycle`
- `status`
- `risk_rating`
- `evidence_link`
- `last_reviewed_date`
- `next_review_due`
- `action_owner`
- `action_due_date`
- `issue_category`
- `closure_evidence`
- `notes`

## Built-in quality scenarios

The dataset should include deliberate but realistic issues:

- missing owner details
- stale review date
- duplicate record identifier
- closed record without closure evidence
- high-risk record without evidence
- high-risk record without an action owner
- invalid status value
- invalid risk rating
- overdue review
- overdue action
