import json
from pathlib import Path

from quality_engine.schema import REQUIRED_FIELDS, VALID_STATUSES

CONTRACT_PATH = Path("contracts/operational-tracker-contract.json")


def _load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_required_fields_match_python_schema() -> None:
    contract = _load_contract()

    assert tuple(contract["required_fields"]) == REQUIRED_FIELDS


def test_contract_status_values_match_python_schema() -> None:
    contract = _load_contract()

    assert tuple(contract["approved_values"]["status"]) == VALID_STATUSES


def test_contract_declares_current_generated_outputs() -> None:
    contract = _load_contract()

    assert contract["generated_outputs"] == [
        "outputs/exception_register.csv",
        "outputs/quality_summary.md",
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
        "DQ009",
        "DQ010",
    ]
    assert all(rule["severity"] in {"Critical", "High", "Medium", "Low"} for rule in rules)
