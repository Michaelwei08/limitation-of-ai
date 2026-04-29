"""Artifact loading and validation for reporting."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CURRENT_METRIC_SCHEMA = "papf.metrics.v3"


@dataclass(frozen=True)
class RunArtifacts:
    run_dir: Path
    metadata_path: Path
    metrics_path: Path
    decisions_path: Path
    audit_path: Path
    metadata: dict[str, Any]
    metrics: tuple[dict[str, Any], ...]
    decisions: tuple[dict[str, Any], ...]
    audit_rows: tuple[dict[str, Any], ...]


def load_run_artifacts(run_dir: str | Path) -> RunArtifacts:
    base = Path(run_dir)
    paths = {
        "metadata": base / "metadata.json",
        "metrics": base / "metrics.jsonl",
        "decisions": base / "decisions.jsonl",
        "audit": base / "audit_summaries.jsonl",
    }
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise ValueError(f"missing run artifacts: {', '.join(missing)}")

    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    if metadata.get("metric_schema_version") != CURRENT_METRIC_SCHEMA:
        raise ValueError(
            f"unsupported metric schema {metadata.get('metric_schema_version')!r}; "
            f"expected {CURRENT_METRIC_SCHEMA}"
        )
    metrics = _read_jsonl(paths["metrics"])
    decisions = _read_jsonl(paths["decisions"])
    audit_rows = _read_jsonl(paths["audit"])
    _validate_run_ids(metadata, metrics, decisions)
    return RunArtifacts(
        run_dir=base,
        metadata_path=paths["metadata"],
        metrics_path=paths["metrics"],
        decisions_path=paths["decisions"],
        audit_path=paths["audit"],
        metadata=metadata,
        metrics=metrics,
        decisions=decisions,
        audit_rows=audit_rows,
    )


def _validate_run_ids(
    metadata: dict[str, Any],
    metrics: tuple[dict[str, Any], ...],
    decisions: tuple[dict[str, Any], ...],
) -> None:
    metric_run_ids = {str(row.get("run_id")) for row in metrics}
    metadata_run_ids = {str(run_id) for run_id in metadata.get("run_ids", [])}
    if metric_run_ids != metadata_run_ids:
        raise ValueError("metrics run_ids do not match metadata run_ids")
    decision_run_ids = {str(row.get("run_id")) for row in decisions}
    if metric_run_ids - decision_run_ids:
        missing_ids = ", ".join(sorted(metric_run_ids - decision_run_ids))
        raise ValueError(f"decisions missing run_ids from metrics: {missing_ids}")


def _read_jsonl(path: Path) -> tuple[dict[str, Any], ...]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError(f"{path}:{line_number} must contain a JSON object")
        rows.append(data)
    return tuple(rows)
