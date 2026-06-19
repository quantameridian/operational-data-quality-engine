# Limitations

## Current stage

This repository now has a small Python foundation, synthetic sample data, initial validation rules, an exception register, and a markdown quality summary.

## Data limitations

- The project will use synthetic data only.
- The sample tracker will represent common reporting quality issues but will not cover every operational edge case.
- The data will not prove performance, risk, or assurance outcomes for any real organisation.

## Technical limitations

- The current implementation uses local batch processing from CSV files.
- It will not connect to live systems.
- It will not provide a user interface.
- It will not automatically repair source data.

## Rule limitations

- Rule severity will be illustrative until adapted to a specific operating context.
- Some issues need human judgement, especially around evidence quality and whether escalation is appropriate.
- A record can pass these checks and still be unsuitable for reporting if the source information is factually wrong.

## Scoring limitations

- The readiness score is a simple capped-penalty model.
- It is designed to support review conversations, not to certify data quality.
- It does not measure operational performance.
- It does not prove that evidence references are valid or sufficient.
- It currently uses the implemented validation issues plus supplementary indicators for missing evidence and overdue reviews.
- Thresholds and penalties should be reviewed before applying the pattern to any real reporting process.

## Portfolio limitations

- This repo should demonstrate the data quality engine only.
- It should not become a full reporting mart, Power BI report, or architecture playbook.
- Included outputs should be regenerated from the sample data when validation rules change.
