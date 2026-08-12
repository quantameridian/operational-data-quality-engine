"""Versioned rule and readiness configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

VALID_SEVERITIES = frozenset({"Critical", "High", "Medium", "Low"})
IMPLEMENTED_RULE_IDS = frozenset(
    {
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
    }
)


class ConfigurationError(ValueError):
    """Raised when a rule configuration is incomplete or invalid."""


@dataclass(frozen=True)
class RuleSetting:
    enabled: bool
    severity: str


@dataclass(frozen=True)
class ReadinessThresholds:
    ready_score: int = 85
    review_score: int = 70
    correction_score: int = 50
    block_ready_on_high_severity: bool = True


@dataclass(frozen=True)
class EngineConfig:
    version: str
    rules: dict[str, RuleSetting]
    stale_review_cycles: int
    readiness: ReadinessThresholds

    def enabled(self, rule_id: str) -> bool:
        return self.rules[rule_id].enabled

    def severity_for(self, rule_id: str) -> str:
        return self.rules[rule_id].severity


def _required_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"'{name}' must be a mapping.")
    return value


def _score(value: Any, name: str) -> int:
    if not isinstance(value, int) or not 0 <= value <= 100:
        raise ConfigurationError(f"'{name}' must be an integer from 0 to 100.")
    return value


def load_engine_config(path: str | Path) -> EngineConfig:
    """Load and validate a YAML engine configuration."""

    config_path = Path(path)
    try:
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Invalid YAML in {config_path}.") from exc
    root = _required_mapping(payload, "configuration")

    version = root.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ConfigurationError("'version' must be a nonempty string.")

    rule_payload = _required_mapping(root.get("rules"), "rules")
    rules: dict[str, RuleSetting] = {}
    for rule_id, raw_setting in rule_payload.items():
        setting = _required_mapping(raw_setting, f"rules.{rule_id}")
        enabled = setting.get("enabled")
        severity = setting.get("severity")
        if not isinstance(enabled, bool):
            raise ConfigurationError(f"'rules.{rule_id}.enabled' must be true or false.")
        if severity not in VALID_SEVERITIES:
            raise ConfigurationError(
                f"'rules.{rule_id}.severity' must be one of {sorted(VALID_SEVERITIES)}."
            )
        rules[str(rule_id)] = RuleSetting(enabled=enabled, severity=str(severity))

    parameters = _required_mapping(root.get("parameters", {}), "parameters")
    stale_review_cycles = parameters.get("stale_review_cycles", 2)
    if not isinstance(stale_review_cycles, int) or stale_review_cycles < 1:
        raise ConfigurationError("'parameters.stale_review_cycles' must be a positive integer.")

    readiness_payload = _required_mapping(root.get("readiness", {}), "readiness")
    readiness = ReadinessThresholds(
        ready_score=_score(readiness_payload.get("ready_score", 85), "readiness.ready_score"),
        review_score=_score(readiness_payload.get("review_score", 70), "readiness.review_score"),
        correction_score=_score(
            readiness_payload.get("correction_score", 50), "readiness.correction_score"
        ),
        block_ready_on_high_severity=readiness_payload.get("block_ready_on_high_severity", True),
    )
    if not isinstance(readiness.block_ready_on_high_severity, bool):
        raise ConfigurationError("'readiness.block_ready_on_high_severity' must be true or false.")
    if not (readiness.ready_score > readiness.review_score > readiness.correction_score):
        raise ConfigurationError("Readiness scores must descend from ready to correction.")

    configured_rule_ids = set(rules)
    if configured_rule_ids != IMPLEMENTED_RULE_IDS:
        missing = sorted(IMPLEMENTED_RULE_IDS - configured_rule_ids)
        unknown = sorted(configured_rule_ids - IMPLEMENTED_RULE_IDS)
        raise ConfigurationError(
            f"Rule set must match the implementation. Missing: {missing}; unknown: {unknown}."
        )

    return EngineConfig(
        version=version,
        rules=rules,
        stale_review_cycles=stale_review_cycles,
        readiness=readiness,
    )
