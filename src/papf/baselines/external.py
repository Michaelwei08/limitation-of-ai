"""External-enforcement baselines stronger than broad access."""

from __future__ import annotations

from papf.audit.models import AuditEvent, RunAuditLog
from papf.benchmark.models import BenchmarkTask, EnvironmentBundle
from papf.benchmark.traces import TraceScenario
from papf.benchmark.validators import validate_task_bundle
from papf.common import DecisionLabel, ExecutionStatus, ScopeSpec
from papf.enforcement.models import EnforcementResult, ToolRequest
from papf.evaluation.metrics import observed_data_refs, score_trace
from papf.evaluation.results import EvaluationCaseResult
from papf.policy.models import PolicyDecision, PolicyRule

TOOL_SCOPE_BASELINE = "tool_scope"
STATIC_POLICY_BASELINE = "static_policy"


def evaluate_external_policy_scenario(
    *,
    run_id: str,
    task: BenchmarkTask,
    environment: EnvironmentBundle,
    scenario: TraceScenario,
    mode_label: str,
) -> EvaluationCaseResult:
    validation_errors = validate_task_bundle(task, environment)
    if validation_errors:
        raise ValueError(f"invalid benchmark task bundle: {'; '.join(validation_errors)}")
    if mode_label not in {TOOL_SCOPE_BASELINE, STATIC_POLICY_BASELINE}:
        raise ValueError(f"unsupported external baseline mode: {mode_label}")

    results = tuple(
        _evaluate_request(run_id=run_id, task=task, request=request, mode_label=mode_label)
        for request in scenario.requests
    )
    audit_log = _build_external_audit_log(run_id=run_id, task=task, scenario=scenario, results=results, mode_label=mode_label)
    metrics = score_trace(
        results,
        environment,
        expected_decisions=scenario.expected_decision_map(),
        audit_log=audit_log,
        task=task,
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


def _evaluate_request(
    *,
    run_id: str,
    task: BenchmarkTask,
    request: ToolRequest,
    mode_label: str,
) -> EnforcementResult:
    if mode_label == TOOL_SCOPE_BASELINE:
        decision = _tool_scope_decision(run_id=run_id, task=task, request=request)
    else:
        decision = _static_policy_decision(run_id=run_id, task=task, request=request)
    status = _execution_status(decision)
    return EnforcementResult(
        request=request,
        decision=decision,
        execution_status=status,
        resolved_scope=request.requested_scope if status == ExecutionStatus.SIMULATED else None,
    )


def _tool_scope_decision(*, run_id: str, task: BenchmarkTask, request: ToolRequest) -> PolicyDecision:
    matching = [
        rule
        for rule in task.policy_pack.rules
        if rule.action == request.action and rule.resource_type == request.requested_scope.resource_type
    ]
    if not matching:
        return _decision(run_id, task.task_id, request, TOOL_SCOPE_BASELINE, DecisionLabel.DENY, "TOOL_SCOPE_NOT_GRANTED")
    if any(rule.effect == DecisionLabel.REQUIRE_CONFIRMATION for rule in matching):
        return _decision(
            run_id,
            task.task_id,
            request,
            TOOL_SCOPE_BASELINE,
            DecisionLabel.REQUIRE_CONFIRMATION,
            "TOOL_SCOPE_CONFIRMATION_REQUIRED",
            confirmation_required=True,
        )
    return _decision(run_id, task.task_id, request, TOOL_SCOPE_BASELINE, DecisionLabel.ALLOW, "TOOL_SCOPE_GRANTED")


def _static_policy_decision(*, run_id: str, task: BenchmarkTask, request: ToolRequest) -> PolicyDecision:
    if request.requested_scope.is_broad:
        return _decision(run_id, task.task_id, request, STATIC_POLICY_BASELINE, DecisionLabel.DENY, "STATIC_POLICY_NO_NARROWING")
    for rule in _matching_exact_rules(task.policy_pack.rules, request):
        if rule.effect == DecisionLabel.REQUIRE_CONFIRMATION:
            return _decision(
                run_id,
                task.task_id,
                request,
                STATIC_POLICY_BASELINE,
                DecisionLabel.REQUIRE_CONFIRMATION,
                "STATIC_POLICY_CONFIRMATION_REQUIRED",
                matched_rule_id=rule.rule_id,
                confirmation_required=True,
            )
        return _decision(
            run_id,
            task.task_id,
            request,
            STATIC_POLICY_BASELINE,
            rule.effect,
            "STATIC_POLICY_RULE_MATCH",
            matched_rule_id=rule.rule_id,
            redaction_applied=rule.effect == DecisionLabel.ALLOW_WITH_REDACTION,
            redaction_requirements=rule.redaction_requirements,
        )
    return _decision(run_id, task.task_id, request, STATIC_POLICY_BASELINE, DecisionLabel.DENY, "STATIC_POLICY_NO_RULE_MATCH")


def _matching_exact_rules(rules: tuple[PolicyRule, ...], request: ToolRequest) -> tuple[PolicyRule, ...]:
    return tuple(
        rule
        for rule in rules
        if rule.action == request.action
        and rule.resource_type == request.requested_scope.resource_type
        and request.requested_scope.selector_value in rule.allow_refs
    )


def _decision(
    run_id: str,
    task_id: str,
    request: ToolRequest,
    mode_label: str,
    label: DecisionLabel,
    reason: str,
    *,
    matched_rule_id: str | None = None,
    confirmation_required: bool = False,
    redaction_applied: bool = False,
    redaction_requirements: tuple[str, ...] = (),
) -> PolicyDecision:
    rule_ids = (f"baseline:{mode_label}",)
    if matched_rule_id is not None:
        rule_ids = (matched_rule_id, *rule_ids)
    return PolicyDecision(
        policy_decision_id=f"{mode_label}_pd_{request.call_id}",
        run_id=run_id,
        task_id=task_id,
        call_id=request.call_id,
        matched_rule_ids=rule_ids,
        decision=label,
        decision_reason=reason,
        confirmation_required=confirmation_required,
        redaction_applied=redaction_applied,
        redaction_requirements=redaction_requirements,
    )


def _execution_status(decision: PolicyDecision) -> ExecutionStatus:
    if decision.decision in {DecisionLabel.DENY, DecisionLabel.REQUIRE_CONFIRMATION, DecisionLabel.ALLOW_WITH_REDACTION}:
        return ExecutionStatus.BLOCKED
    return ExecutionStatus.SIMULATED


def _build_external_audit_log(
    *,
    run_id: str,
    task: BenchmarkTask,
    scenario: TraceScenario,
    results: tuple[EnforcementResult, ...],
    mode_label: str,
) -> RunAuditLog:
    events = [
        AuditEvent(
            audit_event_id=f"{run_id}_audit_000",
            run_id=run_id,
            task_id=task.task_id,
            event_index=0,
            event_type="task_start",
            actor="evaluator",
            summary=f"started {mode_label} scenario {scenario.scenario_id}",
            outcome="started",
            evidence_refs=(scenario.scenario_id, mode_label),
        )
    ]
    for result in results:
        events.append(_decision_event(run_id, task.task_id, len(events), result, mode_label))
        events.append(_tool_event(run_id, task.task_id, len(events), result, mode_label))
    return RunAuditLog(run_id=run_id, events=tuple(events))


def _decision_event(run_id: str, task_id: str, event_index: int, result: EnforcementResult, mode_label: str) -> AuditEvent:
    return AuditEvent(
        audit_event_id=f"{run_id}_audit_{event_index:03d}",
        run_id=run_id,
        task_id=task_id,
        event_index=event_index,
        event_type="baseline_decision",
        actor=f"{mode_label}_runner",
        related_call_id=result.request.call_id,
        related_rule_ids=result.decision.matched_rule_ids,
        summary=f"{mode_label} evaluated {result.request.action.value}",
        outcome=result.decision.decision.value,
        explanation=result.decision.decision_reason,
        evidence_refs=(result.decision.policy_decision_id, mode_label),
    )


def _tool_event(run_id: str, task_id: str, event_index: int, result: EnforcementResult, mode_label: str) -> AuditEvent:
    refs = observed_data_refs(result)
    event_type = "tool_executed" if result.may_execute else "tool_blocked"
    return AuditEvent(
        audit_event_id=f"{run_id}_audit_{event_index:03d}",
        run_id=run_id,
        task_id=task_id,
        event_index=event_index,
        event_type=event_type,
        actor="tool_runtime",
        related_call_id=result.request.call_id,
        related_rule_ids=result.decision.matched_rule_ids,
        related_data_refs=refs,
        summary=f"{mode_label} {event_type} {result.request.tool_name}.{result.request.action.value}",
        outcome=result.execution_status.value,
        evidence_refs=(result.request.call_id, *refs),
    )
