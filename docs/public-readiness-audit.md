# Public Readiness Audit

Audit date: 2026-06-19

## Scope

This audit covers the current state of the `operational-data-quality-engine` repository. It checks whether the project is ready to be reviewed publicly as a technical portfolio repository, not whether it is complete as a production data quality product.

## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| README is accurate | Pass | README describes the current CLI, Makefile commands, generated outputs, scoring model, and limitations. |
| Install command works | Pass | `make PYTHON=/tmp/odqe-rules-audit-venv/bin/python install` completed successfully in a fresh virtual environment. |
| Test command works | Pass | `make PYTHON=/tmp/odqe-rules-audit-venv/bin/python test` completed with 19 passing tests. |
| Lint and format checks pass | Pass | `make PYTHON=/tmp/odqe-rules-audit-venv/bin/python lint` passed Ruff lint and format checks. |
| Run command regenerates outputs | Pass | `make PYTHON=/tmp/odqe-rules-audit-venv/bin/python run` regenerated the exception register and quality summary. |
| GitHub Actions CI checks install, lint, and tests | Pass | `.github/workflows/ci.yml` now runs `make install`, `make lint`, and `make test`. |
| Sample data is safe | Pass | Sample data is synthetic, generic, and uses `example.com` email addresses. |
| No fake client claims | Pass | No delivery claim for a named organisation is made. |
| No internal workplace references | Pass | Audit scan found no internal workplace, protected, or official source references in the sample data or docs. |
| No broken placeholders | Pass | Remaining future-scope wording is explicit and tied to planned improvements. |
| Generated outputs match documentation | Pass | `outputs/exception_register.csv` has 29 rows and documented columns; `outputs/quality_summary.md` reports 30 records, 29 exceptions, and score 12/100. |
| Limitations are honest | Pass | Limitations state that the data is synthetic, scoring is simple, evidence is not verified, and the tool does not certify data quality. |
| Wording is specific and practical | Pass | The repo avoids broad marketing claims and explains concrete reporting-readiness checks. |

## Commands Verified

```bash
rm -rf /tmp/odqe-rules-audit-venv
python3 -m venv /tmp/odqe-rules-audit-venv
make PYTHON=/tmp/odqe-rules-audit-venv/bin/python install
make PYTHON=/tmp/odqe-rules-audit-venv/bin/python test
make PYTHON=/tmp/odqe-rules-audit-venv/bin/python lint
make PYTHON=/tmp/odqe-rules-audit-venv/bin/python run
```

Verified results:

- install completed successfully;
- tests passed: 19 passed;
- Ruff lint passed;
- Ruff format check passed;
- generated outputs were written to `outputs/exception_register.csv` and `outputs/quality_summary.md`.

## Output Check

Current generated outputs:

| Output | Status | Notes |
| --- | --- | --- |
| `outputs/exception_register.csv` | Pass | 29 exception rows generated from the sample tracker and implemented rules. |
| `outputs/quality_summary.md` | Pass | Score is 12/100 with band `Not ready for reporting`. |

Current exception register columns:

- `rule_id`
- `rule_name`
- `severity`
- `record_id`
- `field`
- `issue`
- `recommended_action`

## Remaining Risks

- Missing review evidence and high-risk unresolved records without action owner are still scored or implied in the summary, but not yet fully represented as separate row-level rules.
- CI has been configured but not run on GitHub yet because the repo has not been pushed.
- The project uses synthetic evidence paths only. The tool does not check whether the referenced evidence files exist or are sufficient.
- The README mentions an optional future HTML summary output. This is clearly labelled as future scope, but it should be removed if the repo is published before that output is planned.

## Recommended Fixes Before Publishing

1. Consider adding explicit row-level rules for missing review evidence and high-risk unresolved records without action owner.
2. Run the GitHub Actions workflow after the repository is pushed.
3. Consider adding a short rendered markdown preview only after outputs are final for the first public version.
4. Make an initial commit before pushing so the public history starts from a coherent project state.
