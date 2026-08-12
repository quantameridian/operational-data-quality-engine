from pathlib import Path

import pytest

from quality_engine.config import ConfigurationError, load_engine_config

CONFIG_PATH = Path("config/default-rules.yml")


def test_default_configuration_is_versioned_and_complete() -> None:
    config = load_engine_config(CONFIG_PATH)

    assert config.version == "1.0.0"
    assert len(config.rules) == 13
    assert config.rules["DQ001"].severity == "High"
    assert config.stale_review_cycles == 2
    assert config.readiness.ready_score == 85
    assert config.readiness.block_ready_on_high_severity is True


@pytest.mark.parametrize(
    "content, expected_message",
    [
        ("rules: {}\n", "version"),
        (
            "version: '1'\nrules:\n  DQ001: {enabled: yes, severity: Urgent}\n",
            "severity",
        ),
        (
            "version: '1'\nrules: {}\nparameters: {stale_review_cycles: 0}\n",
            "positive integer",
        ),
        (
            "version: '1'\nrules: {}\nreadiness: {ready_score: 50, review_score: 70}\n",
            "must descend",
        ),
        ("version: '1'\nrules: {}\n", "Rule set must match"),
        (
            "version: '1'\nrules: {}\nreadiness: {block_ready_on_high_severity: maybe}\n",
            "must be true or false",
        ),
        ("version: [\n", "Invalid YAML"),
    ],
)
def test_invalid_configuration_fails_with_a_clear_message(
    tmp_path: Path, content: str, expected_message: str
) -> None:
    path = tmp_path / "rules.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigurationError, match=expected_message):
        load_engine_config(path)
