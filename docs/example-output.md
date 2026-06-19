# Example Output

This document describes the current generated exception register.

## Exception register

Path:

`outputs/exception_register.csv`

The exception register is generated from:

- `data/raw/operational_tracker_sample.csv`
- the implemented core rules in `src/quality_engine/rules.py`

Current columns:

| Column | Meaning |
| --- | --- |
| `rule_id` | Data quality rule identifier |
| `rule_name` | Business-readable rule name |
| `severity` | Severity assigned by the rule |
| `record_id` | Source tracker record that failed the rule |
| `field` | Field or fields that caused the exception |
| `issue` | Short explanation of the failure |
| `recommended_action` | Suggested correction or review action |

## Current rule coverage

The current generated output covers:

- missing owner details;
- invalid status values;
- duplicate record IDs;
- overdue reviews;
- stale unresolved records;
- invalid review cycles;
- missing closure evidence for closed or complete records;
- overdue actions.

## Regeneration command

```bash
python - <<'PY'
from datetime import date
from pathlib import Path

from quality_engine.ingest import load_operational_tracker
from quality_engine.reporting import write_exception_register
from quality_engine.rules import run_core_rules
from quality_engine.scoring import calculate_quality_summary, write_quality_summary

records = load_operational_tracker(Path("data/raw/operational_tracker_sample.csv"))
issues = run_core_rules(records, date(2026, 6, 19))
write_exception_register(issues, Path("outputs/exception_register.csv"))
summary = calculate_quality_summary(records, issues, date(2026, 6, 19))
write_quality_summary(summary, date(2026, 6, 19), Path("outputs/quality_summary.md"))
PY
```

## Expected current result

The current sample data and core rules generate 29 exception rows:

- 2 missing owner exceptions;
- 3 invalid status exceptions;
- 2 duplicate record ID exceptions;
- 10 overdue review exceptions;
- 4 stale record exceptions;
- 1 invalid review cycle exception;
- 2 missing closure evidence exceptions;
- 5 overdue action exceptions.

## Quality summary

Path:

`outputs/quality_summary.md`

The quality summary is generated from the same sample data and validation issues. It adds an explainable readiness score.

Current score:

`12/100`

Current band:

`Not ready for reporting`

The score uses capped penalties for:

- exception rate;
- severity mix;
- high-risk unresolved records with current exceptions or missing action owner;
- missing evidence indicators;
- overdue review indicators.

The score should be read as a practical review signal. It does not prove that the tracker is accurate, complete, or suitable for formal assurance.
