"""Dispatcher for deterministic synthetic tool adapters."""

from __future__ import annotations

from papf.benchmark.models import EnvironmentBundle
from papf.enforcement.models import EnforcementResult
from papf.tools.adapters import (
    SyntheticBrowserAdapter,
    SyntheticEmailAdapter,
    SyntheticFilesAdapter,
    SyntheticToolAdapter,
)
from papf.tools.models import ToolExecutionResult


class SyntheticToolRuntime:
    def __init__(
        self,
        environment: EnvironmentBundle,
        adapters: tuple[SyntheticToolAdapter, ...] | None = None,
    ) -> None:
        self._environment = environment
        configured_adapters = adapters or (
            SyntheticEmailAdapter(),
            SyntheticFilesAdapter(),
            SyntheticBrowserAdapter(),
        )
        self._adapters = _adapter_map(configured_adapters)

    def execute(self, enforcement_result: EnforcementResult) -> ToolExecutionResult:
        if not enforcement_result.may_execute:
            return _blocked_result(enforcement_result)
        adapter = self._adapters.get(enforcement_result.request.tool_name)
        if adapter is None:
            raise ValueError(f"no synthetic adapter registered for tool {enforcement_result.request.tool_name}")
        return adapter.execute(enforcement_result, self._environment)


def _adapter_map(adapters: tuple[SyntheticToolAdapter, ...]) -> dict[str, SyntheticToolAdapter]:
    by_name: dict[str, SyntheticToolAdapter] = {}
    for adapter in adapters:
        if not adapter.tool_name.strip():
            raise ValueError("synthetic adapter tool_name must be non-empty")
        if adapter.tool_name in by_name:
            raise ValueError(f"duplicate synthetic adapter for tool {adapter.tool_name}")
        by_name[adapter.tool_name] = adapter
    return by_name


def _blocked_result(enforcement_result: EnforcementResult) -> ToolExecutionResult:
    request = enforcement_result.request
    return ToolExecutionResult(
        call_id=request.call_id,
        tool_name=request.tool_name,
        action=request.action,
        execution_status=enforcement_result.execution_status,
        decision=enforcement_result.decision.decision,
        policy_decision_id=enforcement_result.decision.policy_decision_id,
        summary=f"{request.tool_name}.{request.action.value} blocked before synthetic tool execution",
    )
