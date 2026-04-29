"""Rule-based capability compilation for benchmark policies."""

from __future__ import annotations

from papf.capabilities.models import Capability, CapabilityBundle
from papf.common import ConsentLevel, DecisionLabel, ScopeSpec
from papf.intent.models import TaskIntent
from papf.policy.models import PolicyPack


def compile_capabilities_from_policy(intent: TaskIntent, policy_pack: PolicyPack) -> CapabilityBundle:
    """Compile narrow capabilities from validated intent and benchmark policy rules.

    The first compiler is deliberately conservative: only explicit policy allow
    references become capabilities. Broad search authority is not minted here.
    """

    intent.require_valid()
    active: list[Capability] = []
    dormant: list[Capability] = []
    notes: list[str] = []

    for rule in policy_pack.rules:
        if rule.action not in intent.requested_actions:
            notes.append(f"skipped {rule.rule_id}: action not requested by intent")
            continue
        if rule.resource_type not in intent.candidate_resource_types:
            notes.append(f"skipped {rule.rule_id}: resource type not proposed by intent")
            continue
        if rule.consent_level == ConsentLevel.DISALLOW or rule.effect == DecisionLabel.DENY:
            continue
        if not rule.allow_refs:
            notes.append(f"skipped {rule.rule_id}: no explicit allow_refs")
            continue
        for data_ref in rule.allow_refs:
            capability = Capability(
                capability_id=f"cap_{rule.rule_id}_{data_ref}",
                action=rule.action,
                scope=ScopeSpec.data_ref(rule.resource_type, data_ref),
                purpose_binding=rule.purpose_binding,
                consent_level=rule.consent_level,
            )
            if rule.consent_level == ConsentLevel.NONE and rule.effect != DecisionLabel.REQUIRE_CONFIRMATION:
                active.append(capability)
            else:
                dormant.append(capability)

    return CapabilityBundle(
        task_id=intent.task_id,
        active_capabilities=tuple(active),
        dormant_capabilities=tuple(dormant),
        compiler_notes=tuple(notes),
    )
