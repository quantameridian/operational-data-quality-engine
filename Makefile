.PHONY: check-python install test lint audit run preview benchmark qa clean

PYTHON ?= python3

check-python:
	@$(PYTHON) -c 'import sys; sys.exit("Python 3.11 or newer is required") if sys.version_info < (3, 11) else None'

install: check-python
	$(PYTHON) -m pip install --upgrade 'pip>=26.1.2' setuptools wheel
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

audit:
	$(PYTHON) -m pip_audit --skip-editable

run:
	$(PYTHON) -m quality_engine.cli \
		--input data/raw/operational_tracker_sample.csv \
		--output-dir outputs \
		--report-date 2026-06-19 \
		--rules-config config/default-rules.yml \
		--run-id sample-2026-06-19 \
		--write-duckdb

preview:
	$(PYTHON) scripts/export_exception_preview.py \
		--input outputs/exception_register.csv \
		--output docs/exception-register-preview.md

benchmark:
	$(PYTHON) scripts/benchmark_engine.py --rows 100000 --report-date 2026-06-19

qa: lint test run preview

clean:
	rm -f outputs/exception_register.csv outputs/quality_summary.md outputs/quality_report.html \
		outputs/run_manifest.json outputs/quality_run.duckdb docs/exception-register-preview.md
