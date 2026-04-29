"""Runtime mediation for tool calls."""

from __future__ import annotations

from papf.capabilities.models import CapabilityBundle
from papf.common import DecisionLabel, ExecutionStatus
from papf.enforcement.models import EnforcementResult, ToolRequest
from papf.policy.engine import evaluate_policy
from papf.policy.models import PolicyPack


def enforce_request(
    *,
    run_id: str,
    task_id: str,
    request: ToolRequest,
    capabilities: CapabilityBundle,
    policy_pack: PolicyPack,
) -> EnforcementResult:
    decision = evaluate_policy(
        run_id=run_id,
        task_id=task_id,
        request=request,
        capabilities=capabilities,
        policy_pack=policy_pack,
    )
    if decision.decision == DecisionLabel.REQUIRE_CONFIRMATION:
        return EnforcementResult(request, decision, ExecutionStatus.BLOCKED)
    if decision.decision == DecisionLabel.DENY:
        return EnforcementResult(request, decision, ExecutionStatus.BLOCKED)
    return EnforcementResult(
        request=request,
        decision=decision,
        execution_status=ExecutionStatus.SIMULATED,
        resolved_scope=decision.narrowed_scope or request.requested_scope,
    )
