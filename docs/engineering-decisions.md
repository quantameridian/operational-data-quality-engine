# Engineering Decisions

## Explicit report date

Overdue and stale checks need a business date. The CLI requires it. Using the system clock would make the same input produce a different answer later without any visible change to source or policy.

## Versioned policy outside Python

Rule switches, severities, staleness, and readiness bands are stored in YAML. That lets a reviewer compare a policy change directly. Rule algorithms remain in Python because date comparison, duplicate detection, and exception construction need tested logic.

The limitation is that this file is not an approval workflow. A production team would add named ownership, controlled promotion, and evidence of approval.

## One exception per failed rule

A record can appear several times in the exception register. This is deliberate. Collapsing failures into one row would hide the rule, field, severity, and action that each owner needs to assess.

## Explainable score

The score uses capped penalties for exception rate, severity, high risk exposure, missing evidence, and overdue reviews. It is easy to calculate and challenge. It is not a statistical estimate and does not certify factual accuracy.

## CSV and DuckDB boundaries

CSV reflects the manual tracker case. DuckDB shows how the same contract can sit behind SQL based ingestion and review without introducing a remote service. Both paths return the same string record shape to the rule layer.

DuckDB is not presented as an enterprise warehouse. It is a portable integration and inspection boundary.

## Deterministic committed evidence

CSV, Markdown, HTML, and JSON outputs are committed so a reviewer can inspect a result before running the code. Runtime timestamps and elapsed time are excluded from those files because they would make every correct run dirty. Performance is measured separately.

The local DuckDB output is ignored because binary database changes are difficult to review in Git. CI uploads it as a short lived artifact.

## Synthetic public data

No real tracker or copied business document is needed to show how the control works. Synthetic records use `example.com` email addresses and plain evidence references. This reduces disclosure risk but also means the repository cannot prove behaviour against the volume, mess, or controls of a real source system.
