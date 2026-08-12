"""Exception register generation for validation issues."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict
from datetime import date
from html import escape
from pathlib import Path

from quality_engine.context import RunContext
from quality_engine.rules import ValidationIssue
from quality_engine.scoring import QualitySummary

EXCEPTION_REGISTER_FIELDS: tuple[str, ...] = (
    "rule_id",
    "rule_name",
    "severity",
    "record_id",
    "field",
    "issue",
    "recommended_action",
)


def issue_to_exception_row(issue: ValidationIssue) -> dict[str, str]:
    """Convert an internal validation issue to an exception register row."""

    return {
        "rule_id": issue.rule_id,
        "rule_name": issue.rule_name,
        "severity": issue.severity,
        "record_id": issue.record_id,
        "field": issue.field,
        "issue": issue.message,
        "recommended_action": issue.recommended_action,
    }


def build_exception_register(issues: Iterable[ValidationIssue]) -> list[dict[str, str]]:
    """Create exception register rows from validation issues."""

    return [issue_to_exception_row(issue) for issue in issues]


def write_exception_register(
    issues: Iterable[ValidationIssue],
    output_path: str | Path,
) -> Path:
    """Write validation issues to an exception register CSV."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_exception_register(issues)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=EXCEPTION_REGISTER_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    return path


def _severity_rows(summary: QualitySummary) -> str:
    if not summary.severity_counts:
        return '<tr><td colspan="2">No validation exceptions</td></tr>'
    return "".join(
        f"<tr><td>{escape(severity)}</td><td>{count}</td></tr>"
        for severity, count in sorted(summary.severity_counts.items())
    )


def render_quality_report_html(
    summary: QualitySummary,
    issues: Iterable[ValidationIssue],
    report_date: date,
    run_id: str,
) -> str:
    """Render a standalone management summary with the highest priority issues."""

    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    priority_issues = sorted(
        issues,
        key=lambda issue: (severity_order.get(issue.severity, 9), issue.record_id, issue.rule_id),
    )[:12]
    issue_rows = "".join(
        "<tr>"
        f"<td>{escape(issue.severity)}</td>"
        f"<td>{escape(issue.record_id)}</td>"
        f"<td>{escape(issue.rule_id)}</td>"
        f"<td>{escape(issue.message)}</td>"
        f"<td>{escape(issue.recommended_action)}</td>"
        "</tr>"
        for issue in priority_issues
    )
    if not issue_rows:
        issue_rows = '<tr><td colspan="5">No validation exceptions</td></tr>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Operational data quality report</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; color: #17212b; }}
    body {{ margin: 0; background: #f4f6f7; }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 20px 48px; }}
    header {{ border-top: 6px solid #006c67; background: white; padding: 24px; }}
    h1, h2 {{ margin: 0 0 12px; }}
    .meta {{ color: #52606d; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 20px 0;
    }}
    .metric {{ background: white; border-left: 4px solid #006c67; padding: 16px; }}
    .metric strong {{ display: block; font-size: 1.6rem; }}
    section {{ margin-top: 24px; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ padding: 10px; border: 1px solid #d8dee3; text-align: left; vertical-align: top; }}
    th {{ background: #e8efee; }}
    @media (max-width: 700px) {{
      .metrics {{ grid-template-columns: 1fr; }}
      table {{ font-size: .85rem; }}
    }}
  </style>
</head>
<body>
<main>
  <header>
    <h1>Operational data quality report</h1>
    <p class="meta">Run {escape(run_id)} | Report date {report_date.isoformat()}</p>
    <p>{escape(summary.readiness_band)}</p>
  </header>
  <div class="metrics">
    <div class="metric"><strong>{summary.score}/100</strong>Readiness score</div>
    <div class="metric"><strong>{summary.record_count}</strong>Records checked</div>
    <div class="metric"><strong>{summary.exception_count}</strong>Exceptions found</div>
  </div>
  <section>
    <h2>Severity profile</h2>
    <table><thead><tr><th>Severity</th><th>Count</th></tr></thead><tbody>{_severity_rows(summary)}</tbody></table>
  </section>
  <section>
    <h2>Priority exceptions</h2>
    <table>
      <thead><tr><th>Severity</th><th>Record</th><th>Rule</th><th>Issue</th><th>Action</th></tr></thead>
      <tbody>{issue_rows}</tbody>
    </table>
  </section>
</main>
</body>
</html>
"""


def write_quality_report_html(
    summary: QualitySummary,
    issues: Iterable[ValidationIssue],
    report_date: date,
    run_id: str,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_quality_report_html(summary, issues, report_date, run_id), encoding="utf-8"
    )
    return path


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_run_manifest(
    context: RunContext,
    summary: QualitySummary,
    output_paths: Iterable[Path],
    output_path: str | Path,
) -> Path:
    """Write deterministic lineage and result metadata for a completed run."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        **context.as_dict(),
        "result": {
            "record_count": summary.record_count,
            "exception_count": summary.exception_count,
            "readiness_score": summary.score,
            "readiness_band": summary.readiness_band,
            "severity_counts": summary.severity_counts,
        },
        "outputs": [
            {"path": item.as_posix(), "sha256": _file_digest(item)} for item in output_paths
        ],
        "quality_summary": asdict(summary),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
