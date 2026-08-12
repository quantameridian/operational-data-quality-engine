"""Run identity and lineage metadata."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from quality_engine import __version__


def sha256_file(path: str | Path) -> str:
    """Return the SHA256 digest for a file without loading it all into memory."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class RunContext:
    run_id: str
    report_date: str
    engine_version: str
    config_version: str
    input_path: str
    input_format: str
    input_sha256: str
    config_path: str
    config_sha256: str

    @classmethod
    def build(
        cls,
        input_path: Path,
        config_path: Path,
        report_date: date,
        config_version: str,
        run_id: str | None = None,
    ) -> RunContext:
        input_digest = sha256_file(input_path)
        effective_run_id = run_id or f"dq-{report_date.isoformat()}-{input_digest[:10]}"
        return cls(
            run_id=effective_run_id,
            report_date=report_date.isoformat(),
            engine_version=__version__,
            config_version=config_version,
            input_path=input_path.as_posix(),
            input_format=input_path.suffix.lower().lstrip("."),
            input_sha256=input_digest,
            config_path=config_path.as_posix(),
            config_sha256=sha256_file(config_path),
        )

    def as_dict(self) -> dict[str, str]:
        return asdict(self)
