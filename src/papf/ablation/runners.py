"""Ablation modes derived from the PAPF enforcement path."""

from __future__ import annotations

from dataclasses import replace
from enum import StrEnum

from papf.audit.models import RunAuditLog
from papf.benchmark.models import BenchmarkTask, EnvironmentBundle
from papf.benchmark.traces import TraceScenario, run_trace_scenario
from papf.benchmark.validators import validate_task_bundle
from papf.common import DecisionLabel, ExecutionStatus
from papf.enforcement.models import EnforcementResult
from papf.evaluation.metrics import score_trace
from papf.evaluation.results import EvaluationCaseResult
from papf.evaluation.runner import build_audit_log
from papf.policy.models import PolicyDecision


class AblationMode(StrEnum):
    NO_SCOPE_NARROWING = "ablation_no_scope_narrowing"
    NO_REDACTION_EVIDENCE = "ablation_no_redaction_evidence"
    NO_CONFIRMATION_GATING = "ablation_no_confirmation_gating"
    NO_SAFER_ALTERNATIVE_RECOVERY = "ablation_no_safer_alternative_recovery"
    NO_AUDIT_COMPLETENESS_VALIDATION = "ablation_no_audit_completeness_validation"


def evaluate_ablation_scenario(
    *,
    run_id: str,
    task: BenchmarkTask,
    environment: EnvironmentBundle,
    scenario: TraceScenario,
    mode: AblationMode,
) -> EvaluationCaseResult:
    validation_errors = validate_task_bundle(task, environment)
    if validation_errors:
        raise ValueError(f"invalid benchmark task bundle: {'; '.join(validation_errors)}")

    base_results = run_trace_scenario(run_id=run_id, task=task, scenario=scenario)
    results = tuple(_apply_ablation(result, mode) for result in base_results)
    audit_log = _audit_log(run_id=run_id, task=task, scenario=scenario, results=results, mode=mode)
    scoring_task = None if mode == AblationMode.NO_SAFER_ALTERNATIVE_RECOVERY else task
    metrics = score_trace(
        results,
        environment,
        expected_decisions=scenario.expected_decision_map(),
        audit_log=audit_log,
        task=scoring_task,
    )
    return EvaluationCaseResult(
        run_id=run_id,
        task_id=task.task_id,
        scenario_id=scenario.scenario_id,
        suite_id=scenario.suite_id,
        results=results,
        audit_log=audit_log,
        metrics=metrics,
    )


def _apply_ablation(result: EnforcementResult, mode: AblationMode) -> EnforcementResult:
    tagged = _tag_result(result, mode)
    if mode == AblationMode.NO_SCOPE_NARROWING:
        return _deny_narrowed_request(tagged, mode)
    if mode == AblationMode.NO_REDACTION_EVIDENCE:
        return _remove_redaction_artifact(tagged, mode)
    if mode == AblationMode.NO_CONFIRMATION_GATING:
        return _bypass_confirmation(tagged, mode)
    return tagged


def _tag_result(result: EnforcementResult, mode: AblationMode) -> EnforcementResult:
    decision = _tag_decision(result.decision, mode, reason_suffix="ABLATION_MODE_ACTIVE")
    return replace(result, decision=decision)


def _tag_decision(decision: PolicyDecision, mode: AblationMode, *, reason_suffix: str) -> PolicyDecision:
    return replace(
        decision,
        matched_rule_ids=(*decision.matched_rule_ids, f"ablation:{mode.value}"),
        decision_reason=f"{decision.decision_reason}; {reason_suffix}",
    )


def _deny_narrowed_request(result: EnforcementResult, mode: AblationMode) -> EnforcementResult:
    if result.decision.decision != DecisionLabel.ALLOW_WITH_NARROWED_SCOPE:
        return result
    decision = _tag_decision(
        replace(
            result.decision,
            decision=DecisionLabel.DENY,
            narrowing_applied=False,
            narrowed_scope=None,
        ),
        mode,
        reason_suffix="SCOPE_NARROWING_DISABLED",
    )
    return replace(result, decision=decision, execution_status=ExecutionStatus.BLOCKED, resolved_scope=None)


def _remove_redaction_artifact(result: EnforcementResult, mode: AblationMode) -> EnforcementResult:
    if result.decision.decision != DecisionLabel.ALLOW_WITH_REDACTION:
        return result
    decision = _tag_decision(
        replace(result.decision, redaction_applied=False),
        mode,
        reason_suffix="REDACTION_ARTIFACT_DISABLED",
    )
    return replace(
        result,
        decision=decision,
        execution_status=ExecutionStatus.SIMULATED,
        resolved_scope=result.resolved_scope or result.request.requested_scope,
        redaction_artifact=None,
    )


def _bypass_confirmation(result: EnforcementResult, mode: AblationMode) -> EnforcementResult:
    if result.decision.decision != DecisionLabel.REQUIRE_CONFIRMATION:
        return result
    decision = _tag_decision(
        replace(
            result.decision,
            decision=DecisionLabel.ALLOW,
            confirmation_required=False,
            confirmation_outcome="ablation_bypassed",
        ),
        mode,
        reason_suffix="CONFIRMATION_GATING_DISABLED",
    )
    return replace(
        result,
        decision=decision,
        execution_status=ExecutionStatus.SIMULATED,
        resolved_scope=result.request.requested_scope,
    )


def _audit_log(
    *,
    run_id: str,
    task: BenchmarkTask,
    scenario: TraceScenario,
    results: tuple[EnforcementResult, ...],
    mode: AblationMode,
) -> RunAuditLog:
    if mode == AblationMode.NO_AUDIT_COMPLETENESS_VALIDATION:
        return RunAuditLog(run_id=run_id, events=())
    return build_audit_log(run_id=run_id, task=task, scenario=scenario, results=results)
