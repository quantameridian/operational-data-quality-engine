# Reviewer Guide

## Ten minute review

1. Open the [HTML report](../outputs/quality_report.html) and decide whether the result is clear without reading code.
2. Inspect the [run manifest](../outputs/run_manifest.json) for input, policy, engine, and output lineage.
3. Compare [the rule policy](../config/default-rules.yml) with [`run_core_rules`](../src/quality_engine/rules.py).
4. Read the [contract tests](../tests/test_contract.py) and [scenario tests](../tests/test_scenarios.py).
5. Inspect the CSV and DuckDB paths in [ingest.py](../src/quality_engine/ingest.py) and [storage.py](../src/quality_engine/storage.py).
6. Read [engineering decisions](engineering-decisions.md) for the choices and limitations behind the design.

## Questions this repository answers

**Can a business rule be challenged?**

Yes. The rule name, severity, switch, threshold, failed field, message, and action are visible. A severity change does not require a code change.

**Can a run be reproduced?**

Yes, when the same source file, report date, configuration, and engine version are available. The manifest records hashes for each input and generated text output.

**Can it join a data workflow?**

Yes at a local batch boundary. The CLI emits JSON events, returns distinct failure and quality gate codes, reads CSV or DuckDB, writes DuckDB review tables, and runs in CI.

**Does the sample prove production scale?**

No. The benchmark measures the in memory rule path at 100,000 rows. It does not include remote I/O, concurrency, recovery, or service operation.

## Local verification

```bash
make install
make qa
make audit
make benchmark
```

Expected checks:

- more than 40 tests pass;
- coverage remains at or above 90 per cent;
- Ruff reports no lint or format errors;
- the dependency audit reports no known vulnerabilities;
- the blocked sample returns score 12 with 39 exceptions;
- the 100,000 row benchmark completes and reports throughput.

## Interview discussion

The useful discussion is not whether 12 is the perfect score. It is how to agree a rule with owners, prevent a policy change from becoming an invisible code edit, preserve lineage, set a pipeline gate, respond to failed records, and decide which controls belong in a production platform rather than this engine.
