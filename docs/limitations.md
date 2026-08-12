# Limitations

## Accuracy

The engine checks declared structure and rules. It cannot establish whether a source statement is true, whether an evidence file is sufficient, or whether an assigned owner accepted responsibility.

## Operation

This is a local batch application. It has no scheduler, user interface, alert transport, identity provider, secrets store, retention service, or recovery controller. CSV and DuckDB are local boundaries, not live enterprise integrations.

## Scale

Rules materialise records in memory. The benchmark covers 100,000 synthetic rows and core rule time only. It does not prove remote source throughput, peak memory, concurrent use, or service availability.

## Policy

Severities, score penalties, and thresholds are examples for the worked case. An organisation would need named policy owners, approval records, change control, metric impact assessment, and local risk tolerances.

## Data

Synthetic scenarios are useful for repeatability but are cleaner and narrower than most operational sources. They do not cover encoding failure, very large fields, partial extracts, changing identifiers, late arriving records, or malicious content beyond the tested table name boundary.
