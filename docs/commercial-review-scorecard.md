# Review Scorecard

## Verdict

Current grade: 8.0 / 10 for a public portfolio data quality engineering repo.

This repo is strong enough to show in a Python data quality portfolio. It has business rules, tests, a contract, generated outputs, and visible public repo practice. It should be described as a local engine and control pattern, not as a live data quality platform.

For a hiring reviewer, the main signal is that the project connects code to a real reporting problem. The rules are not abstract checks. They point to ownership, evidence, review timing, stale records, and actions that would matter before a management report is trusted.

## Research Alignment

This repo lines up with data engineering expectations around:

- designing data processing checks;
- preparing data for analysis;
- maintaining and automating data workloads;
- using CI, dependency audit, CodeQL, and Scorecard for public repo hygiene;
- making data quality visible before reporting.

Reference expectations:

- Google Cloud Professional Data Engineer: design, ingest/process, prepare/use,
  maintain, and automate data workloads.
- GitHub Actions security guidance: least privilege workflows and careful use of outside actions.
- OpenSSF Scorecard: public supply chain health checks.

## Strengths

| Area | Assessment |
| --- | --- |
| Python structure | Clear package split between ingest, schema, rules, scoring, reporting, and CLI |
| Testability | Good for the repo size; schema, rules, contract, CLI, scoring, and reporting are covered |
| Business realism | Rules map to reporting issues rather than only technical null checks |
| Reviewer evidence | Generated exception register, quality summary, contract, preview, and runbook are inspectable |
| Security posture | Public data boundary, dependency audit, CodeQL, Scorecard, and ignored generated folders are present |

## Portfolio Signal

The repo gives a credible story for data engineering, analytics engineering, reporting control, and assurance roles. It shows Python package structure, a CLI, rule based data quality logic, generated output, a JSON contract, tests, and clear public data boundaries.

## Weaknesses

| Gap | Why it matters |
| --- | --- |
| No scheduler or orchestration | Does not yet show how the check runs as part of a recurring reporting cycle |
| No database or warehouse integration | CSV batch mode is useful but limited |
| No configurable rule file | Rules are testable, but not yet editable by configuration or business owner review |
| No HTML or dashboard output | The output is easy to inspect, but not yet a report for managers |
| No profiling baseline | The repo checks defined rules, but does not profile unexpected distributions or drift |

## Best Next Upgrades

1. Add rule selection and severity overrides from a config file.
2. Add a small orchestration example that runs validation, summary, and preview as a pipeline.
3. Add an HTML quality report generated from the exception register.
4. Add input profiling for distribution drift, unexpected categories, and unusual missingness.
5. Add database input/output adapters while keeping the CSV path for public review.

## Hard Bar

Do not describe this as production ready until it has orchestration, monitoring,
configurable rule management, and a clear deployment boundary. Right now it is
a solid local engine for a portfolio.
