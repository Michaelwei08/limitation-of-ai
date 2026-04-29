"""Serialization for deterministic PAPF evaluation runs."""

from __future__ import annotations

import csv
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from papf.evaluation.results import EvaluationCaseResult, EvaluationSuiteResult
from papf.evaluation.runner import evaluate_default_suite

METRIC_SCHEMA_VERSION = "papf.metrics.v1"


@dataclass(frozen=True)
class SerializedRun:
    output_dir: Path
    metadata_path: Path
    metrics_jsonl_path: Path
    metrics_csv_path: Path
    audit_jsonl_path: Path


def write_default_evaluation_run(
    output_dir: str | Path,
    *,
    timestamp: str | None = None,
    repo_root: str | Path | None = None,
) -> SerializedRun:
    suite = evaluate_default_suite()
    return write_evaluation_suite(
        suite,
        output_dir,
        timestamp=timestamp,
        repo_root=repo_root,
        run_label="default_email_files_browser",
    )


def write_evaluation_suite(
    suite: EvaluationSuiteResult,
    output_dir: str | Path,
    *,
    timestamp: str | None = None,
    repo_root: str | Path | None = None,
    run_label: str = "papf_evaluation",
) -> SerializedRun:
    target_dir = _prepare_output_dir(output_dir)
    resolved_timestamp = timestamp or datetime.now(UTC).isoformat()
    metadata = _metadata(
        suite=suite,
        timestamp=resolved_timestamp,
        repo_root=Path(repo_root) if repo_root is not None else None,
        run_label=run_label,
    )

    metadata_path = target_dir / "metadata.json"
    metrics_jsonl_path = target_dir / "metrics.jsonl"
    metrics_csv_path = target_dir / "metrics.csv"
    audit_jsonl_path = target_dir / "audit_summaries.jsonl"

    _write_json(metadata_path, metadata)
    _write_jsonl(metrics_jsonl_path, suite.metric_rows())
    _write_csv(metrics_csv_path, suite.metric_rows())
    _write_jsonl(audit_jsonl_path, _audit_rows(suite.results))

    return SerializedRun(
        output_dir=target_dir,
        metadata_path=metadata_path,
        metrics_jsonl_path=metrics_jsonl_path,
        metrics_csv_path=metrics_csv_path,
        audit_jsonl_path=audit_jsonl_path,
    )


def _prepare_output_dir(output_dir: str | Path) -> Path:
    if isinstance(output_dir, str) and output_dir.strip() == "":
        raise ValueError("output_dir must be non-empty")
    target = Path(output_dir)
    if target.exists() and not target.is_dir():
        raise ValueError(f"output_dir must be a directory, got file: {target}")
    if target.parent.exists() and not target.parent.is_dir():
        raise ValueError(f"output_dir parent must be a directory: {target.parent}")
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        detail = exc.strerror or str(exc)
        raise ValueError(f"failed to create output_dir {target}: {detail}") from exc
    return target


def _metadata(
    *,
    suite: EvaluationSuiteResult,
    timestamp: str,
    repo_root: Path | None,
    run_label: str,
) -> dict[str, Any]:
    return {
        "run_label": run_label,
        "timestamp": timestamp,
        "metric_schema_version": METRIC_SCHEMA_VERSION,
        "scenario_ids": [result.scenario_id for result in suite.results],
        "suite_ids": [result.suite_id for result in suite.results],
        "run_ids": [result.run_id for result in suite.results],
        "git_status_summary": _git_status_summary(repo_root) if repo_root is not None else "not_collected",
    }


def _git_status_summary(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {type(exc).__name__}"
    changed = [line for line in completed.stdout.splitlines() if line.strip()]
    return "clean" if not changed else f"{len(changed)} changed paths"


def _audit_rows(results: tuple[EvaluationCaseResult, ...]) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for result in results:
        for event in result.audit_log.events:
            rows.append(
                {
                    "run_id": event.run_id,
                    "task_id": event.task_id,
                    "scenario_id": result.scenario_id,
                    "suite_id": result.suite_id,
                    "audit_event_id": event.audit_event_id,
                    "event_index": event.event_index,
                    "event_type": event.event_type,
                    "actor": event.actor,
                    "related_call_id": event.related_call_id,
                    "related_rule_ids": list(event.related_rule_ids),
                    "related_data_refs": list(event.related_data_refs),
                    "outcome": event.outcome,
                    "evidence_refs": list(event.evidence_refs),
                }
            )
    return tuple(rows)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: tuple[dict[str, Any], ...]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_csv(path: Path, rows: tuple[dict[str, Any], ...]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
