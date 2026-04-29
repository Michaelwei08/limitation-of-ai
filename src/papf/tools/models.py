"""Synthetic tool execution records."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import Action, DecisionLabel, ExecutionStatus


@dataclass(frozen=True)
class ToolExecutionResult:
    call_id: str
    tool_name: str
    action: Action
    execution_status: ExecutionStatus
    decision: DecisionLabel
    policy_decision_id: str
    observed_data_refs: tuple[str, ...] = ()
    produced_artifact_refs: tuple[str, ...] = ()
    summary: str = ""

    @property
    def did_execute(self) -> bool:
        return self.execution_status == ExecutionStatus.EXECUTED
