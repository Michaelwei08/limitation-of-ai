"""Deterministic synthetic adapters for email, files, and browser tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Protocol

from papf.benchmark.models import DataObject, EnvironmentBundle
from papf.common import Action, ExecutionStatus, ResourceType
from papf.enforcement.models import EnforcementResult
from papf.tools.models import ToolExecutionResult


class SyntheticToolAdapter(Protocol):
    tool_name: str

    def execute(
        self,
        enforcement_result: EnforcementResult,
        environment: EnvironmentBundle,
    ) -> ToolExecutionResult:
        """Execute a deterministic synthetic call after enforcement allows it."""


@dataclass(frozen=True)
class SyntheticEmailAdapter:
    tool_name: ClassVar[str] = "email"

    def execute(
        self,
        enforcement_result: EnforcementResult,
        environment: EnvironmentBundle,
    ) -> ToolExecutionResult:
        scope = _require_executable(enforcement_result, self.tool_name)
        observed_refs = _observed_refs(enforcement_result)
        _require_known_refs(environment, scope.resource_type, observed_refs, enforcement_result.request.call_id)
        produced_refs = _redaction_artifact_refs(enforcement_result)

        if enforcement_result.request.action == Action.READ:
            _require_resource(scope.resource_type, ResourceType.EMAIL_THREAD, enforcement_result.request.call_id)
        elif enforcement_result.request.action == Action.DRAFT:
            _require_resource(scope.resource_type, ResourceType.EMAIL_DRAFT, enforcement_result.request.call_id)
            produced_refs = _merge_refs(produced_refs, (scope.selector_value,))
        elif enforcement_result.request.action == Action.SEND:
            _require_resource(scope.resource_type, ResourceType.EMAIL_DRAFT, enforcement_result.request.call_id)
            produced_refs = _merge_refs(produced_refs, (_artifact_ref("sent_email", enforcement_result),))
        elif enforcement_result.request.action == Action.FORWARD:
            produced_refs = _merge_refs(produced_refs, (_artifact_ref("forwarded_email", enforcement_result),))
        else:
            raise ValueError(f"email adapter does not support action {enforcement_result.request.action.value}")

        return _executed_result(enforcement_result, observed_refs, produced_refs)


@dataclass(frozen=True)
class SyntheticFilesAdapter:
    tool_name: ClassVar[str] = "files"

    def execute(
        self,
        enforcement_result: EnforcementResult,
        environment: EnvironmentBundle,
    ) -> ToolExecutionResult:
        scope = _require_executable(enforcement_result, self.tool_name)
        observed_refs = _observed_refs(enforcement_result)
        _require_known_refs(environment, scope.resource_type, observed_refs, enforcement_result.request.call_id)
        produced_refs = _redaction_artifact_refs(enforcement_result)

        if enforcement_result.request.action == Action.READ:
            _require_file_like(scope.resource_type, enforcement_result.request.call_id)
        elif enforcement_result.request.action == Action.UPLOAD:
            _require_file_like(scope.resource_type, enforcement_result.request.call_id)
            produced_refs = _merge_refs(produced_refs, (_artifact_ref("uploaded_file", enforcement_result),))
        else:
            raise ValueError(f"files adapter does not support action {enforcement_result.request.action.value}")

        return _executed_result(enforcement_result, observed_refs, produced_refs)


@dataclass(frozen=True)
class SyntheticBrowserAdapter:
    tool_name: ClassVar[str] = "browser"

    def execute(
        self,
        enforcement_result: EnforcementResult,
        environment: EnvironmentBundle,
    ) -> ToolExecutionResult:
        scope = _require_executable(enforcement_result, self.tool_name)
        observed_refs = _observed_refs(enforcement_result)
        _require_known_refs(environment, ResourceType.WEBPAGE, observed_refs, enforcement_result.request.call_id)

        if enforcement_result.request.action not in {Action.BROWSE, Action.SEARCH, Action.READ}:
            raise ValueError(f"browser adapter does not support action {enforcement_result.request.action.value}")

        return _executed_result(
            enforcement_result,
            observed_refs,
            _redaction_artifact_refs(enforcement_result),
        )


def _require_executable(enforcement_result: EnforcementResult, tool_name: str):
    request = enforcement_result.request
    if request.tool_name != tool_name:
        raise ValueError(f"{tool_name} adapter received request for tool {request.tool_name}")
    if not enforcement_result.may_execute:
        raise ValueError(f"{tool_name} adapter requires an executable enforcement result")
    if enforcement_result.resolved_scope is None:
        raise ValueError(f"request {request.call_id} is executable but has no resolved scope")
    if enforcement_result.resolved_scope.is_broad:
        raise ValueError(f"request {request.call_id} resolved scope must be narrow before tool execution")
    return enforcement_result.resolved_scope


def _observed_refs(enforcement_result: EnforcementResult) -> tuple[str, ...]:
    if enforcement_result.redaction_artifact is not None:
        return enforcement_result.redaction_artifact.source_refs
    if enforcement_result.resolved_scope is None:
        return ()
    return (enforcement_result.resolved_scope.selector_value,)


def _redaction_artifact_refs(enforcement_result: EnforcementResult) -> tuple[str, ...]:
    if enforcement_result.redaction_artifact is None:
        return ()
    return (enforcement_result.redaction_artifact.output_ref,)


def _executed_result(
    enforcement_result: EnforcementResult,
    observed_refs: tuple[str, ...],
    produced_refs: tuple[str, ...],
) -> ToolExecutionResult:
    request = enforcement_result.request
    return ToolExecutionResult(
        call_id=request.call_id,
        tool_name=request.tool_name,
        action=request.action,
        execution_status=ExecutionStatus.EXECUTED,
        decision=enforcement_result.decision.decision,
        policy_decision_id=enforcement_result.decision.policy_decision_id,
        observed_data_refs=observed_refs,
        produced_artifact_refs=produced_refs,
        summary=f"{request.tool_name}.{request.action.value} executed in synthetic runtime",
    )


def _require_known_refs(
    environment: EnvironmentBundle,
    resource_type: ResourceType,
    refs: tuple[str, ...],
    call_id: str,
) -> None:
    objects_by_id = {obj.data_id: obj for obj in environment.data_objects}
    missing = [ref for ref in refs if ref not in objects_by_id]
    if missing:
        raise ValueError(f"request {call_id} references unknown synthetic data ids: {', '.join(missing)}")
    mismatched = [obj for ref in refs if (obj := objects_by_id[ref]).resource_type != resource_type]
    if mismatched:
        detail = ", ".join(_resource_detail(obj) for obj in mismatched)
        raise ValueError(f"request {call_id} resource type does not match synthetic data: {detail}")


def _resource_detail(obj: DataObject) -> str:
    return f"{obj.data_id} is {obj.resource_type.value}"


def _require_resource(actual: ResourceType, expected: ResourceType, call_id: str) -> None:
    if actual != expected:
        raise ValueError(f"request {call_id} expected {expected.value}, got {actual.value}")


def _require_file_like(resource_type: ResourceType, call_id: str) -> None:
    if resource_type not in {ResourceType.ATTACHMENT, ResourceType.LOCAL_FILE}:
        raise ValueError(f"request {call_id} expected file-like resource, got {resource_type.value}")


def _artifact_ref(prefix: str, enforcement_result: EnforcementResult) -> str:
    request = enforcement_result.request
    return f"{prefix}:{request.call_id}:{enforcement_result.resolved_scope.selector_value}"


def _merge_refs(first: tuple[str, ...], second: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys((*first, *second)))
