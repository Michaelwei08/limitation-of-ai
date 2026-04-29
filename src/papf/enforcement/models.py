"""Tool request and enforcement result records."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import Action, DecisionLabel, ExecutionStatus, ScopeSpec
from papf.policy.models import PolicyDecision


@dataclass(frozen=True)
class ToolRequest:
    call_id: str
    tool_name: str
    action: Action
    requested_scope: ScopeSpec
    input_refs: tuple[str, ...] = ()
    destination: str | None = None


@dataclass(frozen=True)
class EnforcementResult:
    request: ToolRequest
    decision: PolicyDecision
    execution_status: ExecutionStatus
    resolved_scope: ScopeSpec | None = None

    @property
    def may_execute(self) -> bool:
        return self.decision.decision in {
            DecisionLabel.ALLOW,
            DecisionLabel.ALLOW_WITH_NARROWED_SCOPE,
            DecisionLabel.ALLOW_WITH_REDACTION,
        }
