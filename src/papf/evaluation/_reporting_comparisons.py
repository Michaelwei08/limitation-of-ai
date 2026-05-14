"""Comparison-table builders for reporting artifacts."""

from __future__ import annotations

from typing import Any

ABLATION_MODES = (
    "ablation_no_scope_narrowing",
    "ablation_no_redaction_evidence",
    "ablation_no_confirmation_gating",
    "ablation_no_safer_alternative_recovery",
    "ablation_no_audit_completeness_validation",
)
BASELINE_MODES = ("broad_access", "prompt_only", "tool_scope", "static_policy")
STRONGER_BASELINE_MODES = ("tool_scope", "static_policy")


def baseline_comparison_rows(metrics: tuple[dict[str, Any], ...], mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    papf_by_case = {
        _case_key(row): row
        for row in metrics
        if mode_by_run[row["run_id"]] == "papf"
    }
    rows: list[dict[str, Any]] = []
    for mode in BASELINE_MODES:
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


def ablation_result_rows(metrics: tuple[dict[str, Any], ...], mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    return _comparison_rows(metrics, mode_by_run, compared_modes=ABLATION_MODES, label_key="ablation")


def stronger_baseline_result_rows(metrics: tuple[dict[str, Any], ...], mode_by_run: dict[str, str]) -> list[dict[str, Any]]:
    return _comparison_rows(metrics, mode_by_run, compared_modes=STRONGER_BASELINE_MODES, label_key="baseline")


def _comparison_rows(
    metrics: tuple[dict[str, Any], ...],
    mode_by_run: dict[str, str],
    *,
    compared_modes: tuple[str, ...],
    label_key: str,
) -> list[dict[str, Any]]:
    papf_by_case = {
        _case_key(row): row
        for row in metrics
        if mode_by_run[row["run_id"]] == "papf"
    }
    rows: list[dict[str, Any]] = []
    for mode in compared_modes:
        selected = [
            row
            for row in metrics
            if mode_by_run[row["run_id"]] == mode and _case_key(row) in papf_by_case
        ]
        if not selected:
            continue
        papf_rows = [papf_by_case[_case_key(row)] for row in selected]
        rows.append(_comparison_row(label_key, mode, selected, papf_rows))
    return rows


def _comparison_row(
    label_key: str,
    mode: str,
    selected: list[dict[str, Any]],
    papf_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        label_key: mode,
        "matched_scenarios": len(selected),
        "task_success_rate": _mean_bool(selected, "task_success_proxy"),
        "task_success_delta_vs_papf": _mean_bool(selected, "task_success_proxy")
        - _mean_bool(papf_rows, "task_success_proxy"),
        "safe_partial_success_rate": _mean_bool(selected, "safe_partial_success"),
        "safe_partial_success_delta_vs_papf": _mean_bool(selected, "safe_partial_success")
        - _mean_bool(papf_rows, "safe_partial_success"),
        "over_access_rate": _mean(selected, "over_access_rate"),
        "over_access_delta_vs_papf": _mean(selected, "over_access_rate")
        - _mean(papf_rows, "over_access_rate"),
        "false_allow_count": _sum(selected, "false_allow_count"),
        "false_allow_delta_vs_papf": _sum(selected, "false_allow_count")
        - _sum(papf_rows, "false_allow_count"),
        "unredacted_disclosure_count": _sum(selected, "unredacted_disclosure_count"),
        "unredacted_disclosure_delta_vs_papf": _sum(selected, "unredacted_disclosure_count")
        - _sum(papf_rows, "unredacted_disclosure_count"),
        "consent_prompts": _sum(selected, "consent_prompts"),
        "consent_prompt_delta_vs_papf": _sum(selected, "consent_prompts")
        - _sum(papf_rows, "consent_prompts"),
        "recovery_quality": _mean(selected, "recovery_quality"),
        "recovery_quality_delta_vs_papf": _mean(selected, "recovery_quality")
        - _mean(papf_rows, "recovery_quality"),
        "auditability_completeness": _mean(selected, "auditability_completeness"),
        "auditability_completeness_delta_vs_papf": _mean(selected, "auditability_completeness")
        - _mean(papf_rows, "auditability_completeness"),
    }


def _case_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["task_id"]), str(row["suite_id"]), str(row["scenario_id"]))


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    return sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0


def _mean_bool(rows: list[dict[str, Any]], key: str) -> float:
    return sum(1.0 for row in rows if bool(row[key])) / len(rows) if rows else 0.0


def _sum(rows: list[dict[str, Any]], key: str) -> int:
    return sum(int(row[key]) for row in rows)
