# Business Assumptions

## Scenario assumptions

- A team maintains a manual operational tracker that supports reporting or assurance review.
- The tracker contains generic records such as actions, findings, service issues, or risk items.
- Records may be open, in review, blocked, closed, or cancelled.
- Records may require evidence when they are closed or when the risk rating is high.
- Open and high-risk records should have a clear action owner.
- Review dates are used to judge whether records are current enough for reporting.
- The engine reports exceptions rather than automatically changing source records.

## Data assumptions

- Sample data is synthetic and non-client.
- The first sample dataset is `data/raw/operational_tracker_sample.csv`.
- Dates will use ISO format: `YYYY-MM-DD`.
- Blank strings and missing values should be treated consistently.
- Reference values should be held separately from the raw tracker where practical.
- Record identifiers are expected to be unique.
- Email addresses in sample data use the reserved `example.com` domain.
- Evidence fields are references only. The referenced evidence files do not exist in this layer.

## Sample data assumptions

- The sample tracker is designed around a reporting review date of `2026-06-19`.
- Active statuses are `open`, `in_review`, and `blocked`.
- `closed` records should normally have closure evidence.
- `cancelled` records may not require evidence if no work was completed.
- High and critical records should normally have evidence and an action owner.
- Low-risk open records may have optional evidence depending on the issue category.
- Some rows deliberately break the expected rules so validation tests can be meaningful.

## Planned status assumptions

Approved status values are expected to include:

- `open`
- `in_review`
- `blocked`
- `closed`
- `cancelled`

The implementation should define the exact list in code and reference data.

## Planned risk assumptions

Approved risk ratings are expected to include:

- `low`
- `medium`
- `high`
- `critical`

High and critical records should receive stronger checks around ownership, escalation, and evidence.

## Reporting-readiness assumptions

The quality engine should help answer:

- Are records complete enough to report?
- Are open records owned and current?
- Are high-risk records being actively managed?
- Are closed records supported by evidence?
- Would the tracker create obvious reporting errors such as duplicates or invalid status values?

## Sample dataset caveat

The sample data intentionally includes flawed rows. The presence of a row in the sample file should not be read as an endorsed operating practice.

## Out of scope

- Real organisational or employer-owned data.
- Claims that this represents delivery for a named organisation.
- Live system integration.
- Workflow automation or automatic correction of source data.
- Formal data governance certification.
