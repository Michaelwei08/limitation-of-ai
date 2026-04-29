"""Structured evaluation outputs."""

from __future__ import annotations

from dataclasses import dataclass

from papf.audit.models import RunAuditLog
from papf.enforcement.models import EnforcementResult
from papf.evaluation.metrics import RunMetrics


@dataclass(frozen=True)
class EvaluationCaseResult:
    run_id: str
    task_id: str
    scenario_id: str
    suite_id: str
    results: tuple[EnforcementResult, ...]
    audit_log: RunAuditLog
    metrics: RunMetrics


@dataclass(frozen=True)
class EvaluationSuiteResult:
    results: tuple[EvaluationCaseResult, ...]

    def metric_rows(self) -> tuple[dict[str, str | int | float | bool], ...]:
        return tuple(
            {
                "run_id": result.run_id,
                "task_id": result.task_id,
                "scenario_id": result.scenario_id,
                "suite_id": result.suite_id,
                "total_calls": result.metrics.total_calls,
                "executed_calls": result.metrics.executed_calls,
                "blocked_calls": result.metrics.blocked_calls,
                "task_success_proxy": result.metrics.task_success_proxy,
                "necessary_access_rate": result.metrics.necessary_access_rate,
                "over_access_rate": result.metrics.over_access_rate,
                "false_allow_count": result.metrics.false_allow_count,
                "false_deny_count": result.metrics.false_deny_count,
                "consent_prompts": result.metrics.consent_prompts,
                "redacted_access_count": result.metrics.redacted_access_count,
                "unredacted_disclosure_count": result.metrics.unredacted_disclosure_count,
                "recovery_quality": result.metrics.recovery_quality,
                "safe_partial_success": result.metrics.safe_partial_success,
                "task_failure": result.metrics.task_failure,
                "unsafe_workaround_count": result.metrics.unsafe_workaround_count,
                "auditability_completeness": result.metrics.auditability_completeness,
            }
            for result in self.results
        )
