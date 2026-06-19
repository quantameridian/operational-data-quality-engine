# Test Plan

## Unit tests

- Schema rejects missing required columns.
- Duplicate detection returns only duplicated keys.
- Owner validation checks approved teams.
- Review staleness handles missing and old dates.
- Evidence rule applies only where required.
- Status consistency checks closed records.

## Integration tests

- Sample input produces an exception register.
- Summary counts match the exception register.
- CLI exits with a clear error on invalid input.

## Manual review

- README run command matches the implemented CLI.
- Outputs are generated from sample data.
- Documentation does not claim real client delivery.

