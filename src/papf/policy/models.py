"""Policy records."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import Action, ConsentLevel, DecisionLabel, ResourceType, ScopeSpec


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    policy_pack_id: str
    resource_type: ResourceType
    action: Action
    effect: DecisionLabel
    consent_level: ConsentLevel
    allow_refs: tuple[str, ...]
    purpose_binding: str
    rationale_code: str
    redaction_requirements: tuple[str, ...] = ()
    safer_alternative: str | None = None


@dataclass(frozen=True)
class PolicyPack:
    policy_pack_id: str
    rules: tuple[PolicyRule, ...]


@dataclass(frozen=True)
class PolicyDecision:
    policy_decision_id: str
    run_id: str
    task_id: str
    call_id: str
    matched_rule_ids: tuple[str, ...]
    decision: DecisionLabel
    decision_reason: str
    narrowing_applied: bool = False
    narrowed_scope: ScopeSpec | None = None
    redaction_applied: bool = False
    redaction_requirements: tuple[str, ...] = ()
    confirmation_required: bool = False
    confirmation_outcome: str | None = None
