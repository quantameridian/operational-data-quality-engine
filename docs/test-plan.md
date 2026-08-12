# Test Strategy

## Automated checks

| Area | Evidence |
| --- | --- |
| Schema | Missing headers fail in contract order; valid input passes |
| Rules | Each implemented rule has a deliberate failure and structured output assertion |
| Policy | YAML syntax, types, severity values, thresholds, switches, and overrides are tested |
| Scoring | Counts, penalties, bands, empty input behavior, and rendered explanation are checked |
| Scenarios | Clean, review, and blocked datasets produce 100, 82, and 12 |
| Reporting | CSV shape, line endings, HTML content, and manifest lineage are checked |
| Integration | CSV and DuckDB inputs share the contract; DuckDB output tables are queried |
| Security | Unsafe DuckDB table names and unsupported input types fail before processing |
| Command line | Success, structured events, source failure, and score gate exit code are checked |
| Contract | Python fields, approved values, rule identifiers, and output names match JSON |

`make test` enforces at least 90 per cent statement coverage. Current coverage is 96 per cent. Coverage is a guard against untested paths, not a measure of requirement quality.

## Scale check

The 100,000 row benchmark measures the in memory rule path. CI runs a 10,000 row smoke case. Neither uses a fixed timing assertion because shared CI timing is noisy. See [performance.md](performance.md) for the measurement boundary.

## Release check

```bash
make lint
make test
make run
make preview
make audit
git diff --exit-code outputs docs/exception-register-preview.md
```

Review the manifest and HTML output after any rule, policy, score, or sample data change.
