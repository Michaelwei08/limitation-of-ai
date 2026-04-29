"""Runtime mediation for tool calls."""

from __future__ import annotations

from papf.capabilities.models import CapabilityBundle
from papf.common import DecisionLabel, ExecutionStatus
from papf.enforcement.models import EnforcementResult, ToolRequest
from papf.enforcement.redaction import RedactionArtifact, require_valid_redaction_artifact
from papf.policy.engine import evaluate_policy
from papf.policy.models import PolicyPack


def enforce_request(
    *,
    run_id: str,
    task_id: str,
    request: ToolRequest,
    capabilities: CapabilityBundle,
    policy_pack: PolicyPack,
    redaction_artifact: RedactionArtifact | None = None,
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
    resolved_scope = decision.narrowed_scope or request.requested_scope
    if decision.decision == DecisionLabel.ALLOW_WITH_REDACTION:
        if redaction_artifact is None:
            return EnforcementResult(
                request=request,
                decision=decision,
                execution_status=ExecutionStatus.BLOCKED,
                resolved_scope=resolved_scope,
            )
        require_valid_redaction_artifact(
            redaction_artifact,
            run_id=run_id,
            task_id=task_id,
            call_id=request.call_id,
            decision=decision,
            resolved_scope=resolved_scope,
        )
    elif redaction_artifact is not None:
        raise ValueError("redaction_artifact is only valid for allow_with_redaction decisions")
    return EnforcementResult(
        request=request,
        decision=decision,
        execution_status=ExecutionStatus.SIMULATED,
        resolved_scope=resolved_scope,
        redaction_artifact=redaction_artifact,
    )
