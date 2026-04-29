"""Paper table and figure generation from serialized experiment artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from papf.evaluation._reporting_loader import RunArtifacts, load_run_artifacts
from papf.evaluation._reporting_writers import write_bar_svg, write_csv, write_markdown

MODE_ORDER = ("papf", "broad_access", "prompt_only")


@dataclass(frozen=True)
class ReportingArtifacts:
    tables_dir: Path
    figures_dir: Path
    main_metrics_csv: Path
    baseline_comparison_csv: Path
    failure_cases_csv: Path
    provenance_csv: Path
    task_success_figure: Path
    false_allow_figure: Path


def generate_reporting_artifacts(
    run_dir: str | Path,
    *,
    tables_dir: str | Path = "paper/tables",
    figures_dir: str | Path = "paper/figures",
) -> ReportingArtifacts:
    """Write paper-ready tables and SVG figures derived only from run artifacts."""
    artifacts = load_run_artifacts(run_dir)
    tables_path = Path(tables_dir)
    figures_path = Path(figures_dir)
    tables_path.mkdir(parents=True, exist_ok=True)
    figures_path.mkdir(parents=True, exist_ok=True)

    mode_by_run = infer_modes(artifacts.decisions)
    main_rows = main_metrics_rows(artifacts.metrics, mode_by_run)
    baseline_rows = baseline_comparison_rows(artifacts.metrics, mode_by_run)
    failure_rows = failure_case_rows(artifacts.metrics, artifacts.audit_rows, mode_by_run)
    provenance_rows = provenance_rows_from_artifacts(artifacts, mode_by_run)

    main_csv = tables_path / "main_metrics.csv"
    baseline_csv = tables_path / "baseline_comparison.csv"
    failure_csv = tables_path / "failure_cases.csv"
    provenance_csv = tables_path / "run_provenance.csv"

    write_csv(main_csv, main_rows)
    write_markdown(main_csv.with_suffix(".md"), main_rows, "Main Metrics")
    write_csv(baseline_csv, baseline_rows)
    write_markdown(baseline_csv.with_suffix(".md"), baseline_rows, "Baseline Comparison")
    write_csv(failure_csv, failure_rows)
    write_markdown(failure_csv.with_suffix(".md"), failure_rows, "Failure Cases")
    write_csv(provenance_csv, provenance_rows)
    write_markdown(provenance_csv.with_suffix(".md"), provenance_rows, "Run Provenance")

    success_svg = figures_path / "task_success_rate_by_mode.svg"
    false_allow_svg = figures_path / "false_allows_by_mode.svg"
    write_bar_svg(
        success_svg,
        title="Task Success Rate by Mode",
        y_label="Task success rate",
        values={row["mode"]: float(row["task_success_rate"]) for row in main_rows},
        value_format="{:.2f}",
    )
    write_bar_svg(
        false_allow_svg,
        title="False Allows by Mode",
        y_label="False allow count",
        values={row["mode"]: float(row["false_allow_count"]) for row in main_rows},
        value_format="{:.0f}",
    )

    return ReportingArtifacts(
        tables_dir=tables_path,
        figures_dir=figures_path,
        main_metrics_csv=main_csv,
        baseline_comparison_csv=baseline_csv,
        failure_cases_csv=failure_csv,
        provenance_csv=provenance_csv,
        task_success_figure=success_svg,
        false_allow_figure=false_allow_svg,
    )


def infer_modes(decisions: tuple[dict[str, Any], ...]) -> dict[str, str]:
    modes: dict[str, str] = {}
    for row in decisions:
        run_id = str(row["run_id"])
        rule_ids = tuple(str(rule_id) for rule_id in row.get("matched_rule_ids", ()))
        mode = "papf"
        if "baseline:broad_access" in rule_ids:
            mode = "broad_access"
        elif "baseline:prompt_only" in rule_ids:
            mode = "prompt_only"
        previous = modes.get(run_id)
        if previous is not None and previous != mode:
            raise ValueError(f"conflicting inferred modes for run_id {run_id}")
        modes[run_id] = mode
    return modes


def main_metrics_rows(metrics: tuple[dict[str, Any], ...], mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mode in _present_modes(mode_by_run):
        selected = [row for row in metrics if mode_by_run[row["run_id"]] == mode]
        rows.append(
            {
                "mode": mode,
                "scenario_count": len(selected),
                "task_success_rate": _mean_bool(selected, "task_success_proxy"),
                "safe_partial_success_rate": _mean_bool(selected, "safe_partial_success"),
                "task_failure_rate": _mean_bool(selected, "task_failure"),
                "necessary_access_rate": _mean(selected, "necessary_access_rate"),
                "over_access_rate": _mean(selected, "over_access_rate"),
                "false_allow_count": _sum(selected, "false_allow_count"),
                "false_deny_count": _sum(selected, "false_deny_count"),
                "unredacted_disclosure_count": _sum(selected, "unredacted_disclosure_count"),
                "consent_prompts": _sum(selected, "consent_prompts"),
                "recovery_quality": _mean(selected, "recovery_quality"),
                "auditability_completeness": _mean(selected, "auditability_completeness"),
            }
        )
    return rows


def baseline_comparison_rows(metrics: tuple[dict[str, Any], ...], mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    papf_by_case = {
        _case_key(row): row
        for row in metrics
        if mode_by_run[row["run_id"]] == "papf"
    }
    rows: list[dict[str, Any]] = []
    for mode in ("broad_access", "prompt_only"):
        selected = [
            row
            for row in metrics
            if mode_by_run[row["run_id"]] == mode and _case_key(row) in papf_by_case
        ]
        if not selected:
            continue
        papf_rows = [papf_by_case[_case_key(row)] for row in selected]
        rows.append(
            {
                "baseline": mode,
                "matched_scenarios": len(selected),
                "task_success_rate": _mean_bool(selected, "task_success_proxy"),
                "task_success_delta_vs_papf": _mean_bool(selected, "task_success_proxy")
                - _mean_bool(papf_rows, "task_success_proxy"),
                "over_access_rate": _mean(selected, "over_access_rate"),
                "over_access_delta_vs_papf": _mean(selected, "over_access_rate")
                - _mean(papf_rows, "over_access_rate"),
                "false_allow_count": _sum(selected, "false_allow_count"),
                "false_allow_delta_vs_papf": _sum(selected, "false_allow_count")
                - _sum(papf_rows, "false_allow_count"),
                "consent_prompt_delta_vs_papf": _sum(selected, "consent_prompts")
                - _sum(papf_rows, "consent_prompts"),
            }
        )
    return rows


def failure_case_rows(
    metrics: tuple[dict[str, Any], ...],
    audit_rows: tuple[dict[str, Any], ...],
    mode_by_run: dict[str, str],
) -> list[dict[str, Any]]:
    evidence_by_run = _audit_evidence(audit_rows)
    rows: list[dict[str, Any]] = []
    for row in metrics:
        issues = _failure_labels(row)
        if not issues:
            continue
        run_id = str(row["run_id"])
        rows.append(
            {
                "mode": mode_by_run[run_id],
                "task_id": row["task_id"],
                "suite_id": row["suite_id"],
                "scenario_id": row["scenario_id"],
                "run_id": run_id,
                "failure_labels": "; ".join(issues),
                "false_allow_count": row["false_allow_count"],
                "false_deny_count": row["false_deny_count"],
                "over_access_rate": row["over_access_rate"],
                "task_failure": row["task_failure"],
                "evidence": evidence_by_run.get(run_id, ""),
            }
        )
    return sorted(rows, key=lambda item: (item["mode"], item["suite_id"], item["scenario_id"]))


def provenance_rows_from_artifacts(artifacts: RunArtifacts, mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for row in artifacts.metrics:
        run_id = str(row["run_id"])
        rows.append(
            {
                "run_id": run_id,
                "mode": mode_by_run[run_id],
                "task_id": row["task_id"],
                "suite_id": row["suite_id"],
                "scenario_id": row["scenario_id"],
                "run_label": artifacts.metadata["run_label"],
                "timestamp": artifacts.metadata["timestamp"],
                "metric_schema_version": artifacts.metadata["metric_schema_version"],
                "metadata_artifact": str(artifacts.metadata_path),
                "metrics_artifact": str(artifacts.metrics_path),
                "decisions_artifact": str(artifacts.decisions_path),
                "audit_artifact": str(artifacts.audit_path),
            }
        )
    return sorted(rows, key=lambda item: item["run_id"])


def _present_modes(mode_by_run: dict[str, str]) -> tuple[str, ...]:
    present = set(mode_by_run.values())
    return tuple(mode for mode in MODE_ORDER if mode in present)


def _case_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["task_id"]), str(row["suite_id"]), str(row["scenario_id"]))


def _failure_labels(row: dict[str, Any]) -> tuple[str, ...]:
    labels = []
    if int(row["false_allow_count"]) > 0:
        labels.append("false_allow")
    if int(row["false_deny_count"]) > 0:
        labels.append("false_deny")
    if float(row["over_access_rate"]) > 0:
        labels.append("over_access")
    if int(row["unredacted_disclosure_count"]) > 0:
        labels.append("unredacted_disclosure")
    if bool(row["task_failure"]):
        labels.append("task_failure")
    if int(row["unsafe_workaround_count"]) > 0:
        labels.append("unsafe_workaround")
    return tuple(labels)


def _audit_evidence(audit_rows: tuple[dict[str, Any], ...]) -> dict[str, str]:
    evidence: dict[str, list[str]] = {}
    for row in audit_rows:
        if row.get("event_type") != "tool_executed":
            continue
        refs = row.get("related_data_refs") or []
        if not refs:
            continue
        run_id = str(row["run_id"])
        call_id = str(row.get("related_call_id") or "unknown_call")
        evidence.setdefault(run_id, []).append(f"{call_id}:{','.join(str(ref) for ref in refs)}")
    return {run_id: "; ".join(items[:3]) for run_id, items in evidence.items()}


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    return sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0


def _mean_bool(rows: list[dict[str, Any]], key: str) -> float:
    return sum(1.0 for row in rows if bool(row[key])) / len(rows) if rows else 0.0


def _sum(rows: list[dict[str, Any]], key: str) -> int:
    return sum(int(row[key]) for row in rows)
