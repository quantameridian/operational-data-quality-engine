# Decision Scenarios

These synthetic files show three outcomes against the same reporting date, `2026-06-19`.

| File | Expected result | Reason |
| --- | --- | --- |
| `tracker_clean.csv` | Ready for routine reporting, 100 | No implemented rule fails |
| `tracker_review.csv` | Usable with review, 82 | Three records have overdue reviews |
| `../raw/operational_tracker_sample.csv` | Not ready for reporting, 12 | The sample contains ownership, status, evidence, duplicate, timing, and reference value failures |

The scenario test calculates these results from the engine. The values are not maintained by hand.
