"""Deterministic benchmark evaluation harness."""

from __future__ import annotations

from papf.audit.models import AuditEvent, RunAuditLog
from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.models import BenchmarkTask, EnvironmentBundle
from papf.benchmark.traces import TraceScenario, email_files_browser_scenarios, run_trace_scenario
from papf.benchmark.validators import validate_task_bundle
from papf.enforcement.models import EnforcementResult
from papf.enforcement.redaction import RedactionArtifact
from papf.evaluation.metrics import score_trace
from papf.evaluation.results import EvaluationCaseResult, EvaluationSuiteResult


def evaluate_scenario(
    *,
    run_id: str,
    task: BenchmarkTask,
    environment: EnvironmentBundle,
    scenario: TraceScenario,
) -> EvaluationCaseResult:
    validation_errors = validate_task_bundle(task, environment)
    if validation_errors:
        raise ValueError(f"invalid benchmark task bundle: {'; '.join(validation_errors)}")

    results = run_trace_scenario(run_id=run_id, task=task, scenario=scenario)
    audit_log = build_audit_log(run_id=run_id, task=task, scenario=scenario, results=results)
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


def evaluate_default_suite() -> EvaluationSuiteResult:
    task, environment = email_files_fixture()
    results = tuple(
        evaluate_scenario(
            run_id=f"run_{scenario.suite_id}",
            task=task,
            environment=environment,
            scenario=scenario,
        )
        for scenario in email_files_browser_scenarios()
    )
    return EvaluationSuiteResult(results=results)


def build_audit_log(
    *,
    run_id: str,
    task: BenchmarkTask,
    scenario: TraceScenario,
    results: tuple[EnforcementResult, ...],
) -> RunAuditLog:
    events: list[AuditEvent] = [
        AuditEvent(
            audit_event_id=f"{run_id}_audit_000",
            run_id=run_id,
            task_id=task.task_id,
            event_index=0,
            event_type="task_start",
            actor="evaluator",
            summary=f"started scenario {scenario.scenario_id}",
            outcome="started",
            evidence_refs=(scenario.scenario_id,),
        )
    ]
    for result in results:
        events.append(_policy_event(run_id, task.task_id, len(events), result))
        events.append(_tool_event(run_id, task.task_id, len(events), result))
    events.append(
        AuditEvent(
            audit_event_id=f"{run_id}_audit_{len(events):03d}",
            run_id=run_id,
            task_id=task.task_id,
            event_index=len(events),
            event_type="task_completed",
            actor="evaluator",
            summary=f"completed scenario {scenario.scenario_id}",
            outcome="completed",
            evidence_refs=tuple(result.decision.policy_decision_id for result in results),
        )
    )
    return RunAuditLog(run_id=run_id, events=tuple(events), redaction_artifacts=_redaction_artifacts(results))


def _policy_event(run_id: str, task_id: str, event_index: int, result: EnforcementResult) -> AuditEvent:
    artifact_refs = _redaction_artifact_refs(result)
    return AuditEvent(
        audit_event_id=f"{run_id}_audit_{event_index:03d}",
        run_id=run_id,
        task_id=task_id,
        event_index=event_index,
        event_type="policy_checked",
        actor="policy_engine",
        related_call_id=result.request.call_id,
        related_rule_ids=result.decision.matched_rule_ids,
        summary=f"{result.request.action.value} request evaluated",
        outcome=result.decision.decision.value,
        explanation=result.decision.decision_reason,
        related_redaction_artifact_refs=artifact_refs,
        evidence_refs=(result.decision.policy_decision_id, *artifact_refs),
    )


def _tool_event(run_id: str, task_id: str, event_index: int, result: EnforcementResult) -> AuditEvent:
    event_type = "tool_executed" if result.may_execute else "tool_blocked"
    related_data_refs = ()
    if result.resolved_scope is not None:
        related_data_refs = (result.resolved_scope.selector_value,)
    artifact_refs = _redaction_artifact_refs(result)
    return AuditEvent(
        audit_event_id=f"{run_id}_audit_{event_index:03d}",
        run_id=run_id,
        task_id=task_id,
        event_index=event_index,
        event_type=event_type,
        actor="tool_runtime",
        related_call_id=result.request.call_id,
        related_rule_ids=result.decision.matched_rule_ids,
        related_data_refs=related_data_refs,
        related_redaction_artifact_refs=artifact_refs,
        summary=f"{result.request.tool_name}.{result.request.action.value} {result.execution_status.value}",
        outcome=result.execution_status.value,
        evidence_refs=(result.request.call_id, result.decision.policy_decision_id, *artifact_refs),
    )


def _redaction_artifact_refs(result: EnforcementResult) -> tuple[str, ...]:
    if result.redaction_artifact is None:
        return ()
    return (result.redaction_artifact.redaction_artifact_id,)


def _redaction_artifacts(results: tuple[EnforcementResult, ...]) -> tuple[RedactionArtifact, ...]:
    artifacts: list[RedactionArtifact] = []
    seen: set[str] = set()
    for result in results:
        artifact = result.redaction_artifact
        if artifact is None or artifact.redaction_artifact_id in seen:
            continue
        artifacts.append(artifact)
        seen.add(artifact.redaction_artifact_id)
    return tuple(artifacts)
