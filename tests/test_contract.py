import json
from dataclasses import asdict
from pathlib import Path

from quality_engine.config import load_engine_config
from quality_engine.schema import (
    REQUIRED_FIELDS,
    VALID_REVIEW_CYCLES,
    VALID_RISK_RATINGS,
    VALID_STATUSES,
)

CONTRACT_PATH = Path("contracts/operational-tracker-contract.json")


def _load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_required_fields_match_python_schema() -> None:
    contract = _load_contract()

    assert tuple(contract["required_fields"]) == REQUIRED_FIELDS


def test_contract_status_values_match_python_schema() -> None:
    contract = _load_contract()

    assert tuple(contract["approved_values"]["status"]) == VALID_STATUSES
    assert tuple(contract["approved_values"]["risk_rating"]) == VALID_RISK_RATINGS
    assert tuple(contract["approved_values"]["review_cycle"]) == VALID_REVIEW_CYCLES


def test_contract_declares_current_generated_outputs() -> None:
    contract = _load_contract()

    assert contract["generated_outputs"] == [
        "outputs/exception_register.csv",
        "outputs/quality_summary.md",
        "outputs/quality_report.html",
        "outputs/run_manifest.json",
        "outputs/quality_run.duckdb",
        "docs/exception-register-preview.md",
    ]


def test_contract_rule_ids_are_unique_and_reviewable() -> None:
    contract = _load_contract()
    rules = contract["implemented_rules"]
    rule_ids = [rule["rule_id"] for rule in rules]

    assert len(rule_ids) == len(set(rule_ids))
    assert rule_ids == [
        "DQ001",
        "DQ002",
        "DQ003",
        "DQ004",
        "DQ005",
        "DQ006",
        "DQ007",
        "DQ008",
        "DQ009",
        "DQ010",
        "DQ011",
        "DQ012",
        "DQ013",
    ]
    assert all(rule["severity"] in {"Critical", "High", "Medium", "Low"} for rule in rules)


def test_contract_rules_match_the_default_policy() -> None:
    contract = _load_contract()
    config = load_engine_config("config/default-rules.yml")

    contract_rules = {rule["rule_id"]: rule["severity"] for rule in contract["implemented_rules"]}
    configured_rules = {
        rule_id: setting.severity for rule_id, setting in config.rules.items() if setting.enabled
    }

    assert contract_rules == configured_rules
    assert contract["readiness_thresholds"] == asdict(config.readiness)
