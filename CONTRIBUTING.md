# Contributing

Changes are welcome when they improve correctness, evidence, or operation.

## Before a pull request

1. Keep all sample data synthetic.
2. Explain the reporting risk or owner need behind a rule change.
3. Update the YAML policy, JSON contract, tests, and generated outputs together.
4. Run `make qa`, `make audit`, and any relevant benchmark.
5. Check that a second `make qa` leaves tracked outputs unchanged.
6. State compatibility, security, and performance effects in the pull request.

Do not commit local databases, virtual environments, caches, logs, editor files, credentials, internal URLs, or real operational records.
