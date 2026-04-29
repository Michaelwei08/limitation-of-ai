"""Deterministic policy evaluation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from papf.capabilities.models import CapabilityBundle, capability_matches_request
from papf.common import ConsentLevel, DecisionLabel, ScopeSpec
from papf.policy.models import PolicyDecision, PolicyPack, PolicyRule

if TYPE_CHECKING:
    from papf.enforcement.models import ToolRequest


def evaluate_policy(
    *,
    run_id: str,
    task_id: str,
    request: ToolRequest,
    capabilities: CapabilityBundle,
    policy_pack: PolicyPack,
) -> PolicyDecision:
    rules = _matching_rules(policy_pack, request)
    explicit_deny = [rule for rule in rules if rule.effect == DecisionLabel.DENY]
    if explicit_deny:
        return _decision(
            run_id,
            task_id,
            request.call_id,
            explicit_deny,
            DecisionLabel.DENY,
            explicit_deny[0].rationale_code,
        )

    active_match = any(
        capability_matches_request(capability, request.action, request.requested_scope)
        for capability in capabilities.active_capabilities
    )
    if active_match:
        rule = _best_rule(rules)
        if rule is None:
            return _deny(run_id, task_id, request.call_id, "NO_MATCHING_POLICY_RULE")
        if rule.effect == DecisionLabel.ALLOW_WITH_REDACTION:
            return _decision(
                run_id,
                task_id,
                request.call_id,
                [rule],
                DecisionLabel.ALLOW_WITH_REDACTION,
                rule.rationale_code,
                redaction_applied=True,
                redaction_requirements=rule.redaction_requirements,
            )
        return _decision(run_id, task_id, request.call_id, [rule], DecisionLabel.ALLOW, rule.rationale_code)

    narrowed = _narrow_request_scope(request, rules)
    if narrowed is not None:
        narrowed_match = any(
            capability_matches_request(capability, request.action, narrowed)
            for capability in capabilities.active_capabilities
        )
        if narrowed_match:
            rule = _best_rule(rules)
            return _decision(
                run_id,
                task_id,
                request.call_id,
                [rule] if rule else (),
                DecisionLabel.ALLOW_WITH_NARROWED_SCOPE,
                "SCOPE_NARROWED_TO_ALLOWED_REF",
                narrowing_applied=True,
                narrowed_scope=narrowed,
            )

    dormant_match = any(
        capability_matches_request(capability, request.action, request.requested_scope)
        for capability in capabilities.dormant_capabilities
    )
    if dormant_match:
        rule = _best_rule(rules)
        if rule and rule.consent_level in {ConsentLevel.CONFIRM, ConsentLevel.HIGH_RISK_CONFIRM}:
            return _decision(
                run_id,
                task_id,
                request.call_id,
                [rule],
                DecisionLabel.REQUIRE_CONFIRMATION,
                rule.rationale_code,
                confirmation_required=True,
            )

    if not rules:
        return _deny(run_id, task_id, request.call_id, "NO_MATCHING_POLICY_RULE")
    return _deny(run_id, task_id, request.call_id, "MISSING_ACTIVE_CAPABILITY", rules)


def _matching_rules(policy_pack: PolicyPack, request: ToolRequest) -> list[PolicyRule]:
    return [
        rule
        for rule in policy_pack.rules
        if rule.action == request.action and rule.resource_type == request.requested_scope.resource_type
    ]


def _best_rule(rules: list[PolicyRule]) -> PolicyRule | None:
    for rule in rules:
        if rule.effect != DecisionLabel.DENY:
            return rule
    return rules[0] if rules else None


def _narrow_request_scope(request: ToolRequest, rules: list[PolicyRule]) -> ScopeSpec | None:
    if not request.requested_scope.is_broad:
        return None
    allowed_refs = {data_ref for rule in rules for data_ref in rule.allow_refs}
    if any(data_ref not in allowed_refs for data_ref in request.input_refs):
        return None
    candidates = [data_ref for data_ref in request.input_refs if data_ref in allowed_refs]
    if len(candidates) != 1:
        return None
    return ScopeSpec.data_ref(request.requested_scope.resource_type, candidates[0])


def _deny(
    run_id: str,
    task_id: str,
    call_id: str,
    reason: str,
    rules: list[PolicyRule] | None = None,
) -> PolicyDecision:
    return _decision(run_id, task_id, call_id, rules or [], DecisionLabel.DENY, reason)


def _decision(
    run_id: str,
    task_id: str,
    call_id: str,
    rules: list[PolicyRule] | tuple[PolicyRule, ...],
    label: DecisionLabel,
    reason: str,
    *,
    narrowing_applied: bool = False,
    narrowed_scope: ScopeSpec | None = None,
    redaction_applied: bool = False,
    redaction_requirements: tuple[str, ...] = (),
    confirmation_required: bool = False,
) -> PolicyDecision:
    return PolicyDecision(
        policy_decision_id=f"pd_{call_id}",
        run_id=run_id,
        task_id=task_id,
        call_id=call_id,
        matched_rule_ids=tuple(rule.rule_id for rule in rules),
        decision=label,
        decision_reason=reason,
        narrowing_applied=narrowing_applied,
        narrowed_scope=narrowed_scope,
        redaction_applied=redaction_applied,
        redaction_requirements=redaction_requirements,
        confirmation_required=confirmation_required,
    )
