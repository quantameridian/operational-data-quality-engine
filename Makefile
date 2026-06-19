.PHONY: install test lint run preview qa clean

PYTHON ?= python3

install:
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

run:
	$(PYTHON) -m quality_engine.cli \
		--input data/raw/operational_tracker_sample.csv \
		--output-dir outputs \
		--report-date 2026-06-19

preview:
	$(PYTHON) scripts/export_exception_preview.py \
		--input outputs/exception_register.csv \
		--output docs/exception-register-preview.md

qa: lint test run preview

clean:
	rm -f outputs/exception_register.csv outputs/quality_summary.md docs/exception-register-preview.md
