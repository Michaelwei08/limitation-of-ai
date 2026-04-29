"""Validation helpers for policy-adjacent PAPF records."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from enum import StrEnum
from typing import Any

from papf.common import Action, ConsentLevel, DecisionLabel, ResourceType
from papf.policy.models import PolicyPack


DATA_RELEVANCE_LABELS = {"necessary", "supporting", "available_unnecessary", "unrelated_private"}
DATA_SENSITIVITY_LABELS = {"ordinary", "sensitive", "dangerous"}
DATA_TRUST_LABELS = {"trusted_content", "untrusted_content"}
CONFIRMATION_CONSENT = {ConsentLevel.CONFIRM, ConsentLevel.HIGH_RISK_CONFIRM}
PERMISSIVE_DECISIONS = {
    DecisionLabel.ALLOW,
    DecisionLabel.ALLOW_WITH_NARROWED_SCOPE,
    DecisionLabel.ALLOW_WITH_REDACTION,
}


def validate_policy_pack(policy_pack: PolicyPack, environment: Any | None = None) -> list[str]:
    """Validate a policy pack and, when available, its environment references."""

    errors: list[str] = []
    if not policy_pack.policy_pack_id.strip():
        errors.append("policy_pack_id must be non-empty")

    _extend_duplicate_errors(errors, "policy rule_id", (rule.rule_id for rule in policy_pack.rules))
    data_by_id = _data_by_id(environment, errors) if environment is not None else {}

    for rule in policy_pack.rules:
        rule_label = rule.rule_id or "<missing>"
        if not rule.rule_id.strip():
            errors.append("policy rule_id must be non-empty")
        if rule.policy_pack_id != policy_pack.policy_pack_id:
            errors.append(
                f"policy rule {rule_label} policy_pack_id must match "
                f"policy_pack_id {policy_pack.policy_pack_id!r}"
            )
        _validate_enum(errors, "policy rule", rule_label, "resource_type", rule.resource_type, ResourceType)
        _validate_enum(errors, "policy rule", rule_label, "action", rule.action, Action)
        valid_effect = _validate_enum(errors, "policy rule", rule_label, "effect", rule.effect, DecisionLabel)
        valid_consent = _validate_enum(
            errors,
            "policy rule",
            rule_label,
            "consent_level",
            rule.consent_level,
            ConsentLevel,
        )
        if not rule.purpose_binding.strip():
            errors.append(f"policy rule {rule_label} purpose_binding must be non-empty")
        if not rule.rationale_code.strip():
            errors.append(f"policy rule {rule_label} rationale_code must be non-empty")
        _extend_duplicate_errors(errors, f"allow_ref in policy rule {rule_label}", rule.allow_refs)
        if data_by_id:
            _validate_rule_environment_refs(errors, rule, data_by_id, valid_effect, valid_consent)
    return errors


def require_valid_policy_pack(policy_pack: PolicyPack, environment: Any | None = None) -> None:
    errors = validate_policy_pack(policy_pack, environment)
    if errors:
        raise ValueError(f"invalid PolicyPack: {'; '.join(errors)}")


def validate_capability_bundle(bundle: Any) -> list[str]:
    errors: list[str] = []
    if not bundle.task_id.strip():
        errors.append("capability bundle task_id must be non-empty")

    capabilities = (*bundle.active_capabilities, *bundle.dormant_capabilities)
    _extend_duplicate_errors(errors, "capability_id", (capability.capability_id for capability in capabilities))
    for capability in capabilities:
        cap_label = capability.capability_id or "<missing>"
        if not capability.capability_id.strip():
            errors.append("capability_id must be non-empty")
        _validate_enum(errors, "capability", cap_label, "action", capability.action, Action)
        _validate_enum(errors, "capability", cap_label, "consent_level", capability.consent_level, ConsentLevel)
        _validate_scope(errors, f"capability {cap_label}", capability.scope)
        if capability.scope.is_broad:
            errors.append(f"capability {cap_label} uses broad scope; capabilities must be narrow")
        if not capability.purpose_binding.strip():
            errors.append(f"capability {cap_label} purpose_binding must be non-empty")
    return errors


def require_valid_capability_bundle(bundle: Any) -> None:
    errors = validate_capability_bundle(bundle)
    if errors:
        raise ValueError(f"invalid CapabilityBundle: {'; '.join(errors)}")


def validate_environment(environment: Any) -> list[str]:
    errors: list[str] = []
    if not environment.environment_id.strip():
        errors.append("environment_id must be non-empty")
    _data_by_id(environment, errors)
    return errors


def validate_trace_scenario(scenario: Any) -> list[str]:
    errors: list[str] = []
    if not scenario.scenario_id.strip():
        errors.append("scenario_id must be non-empty")
    call_ids = {request.call_id for request in scenario.requests}
    _extend_duplicate_errors(
        errors,
        f"call_id in scenario {scenario.scenario_id}",
        (request.call_id for request in scenario.requests),
    )
    for request in scenario.requests:
        request_label = request.call_id or "<missing>"
        if not request.call_id.strip():
            errors.append(f"scenario {scenario.scenario_id} call_id must be non-empty")
        if not request.tool_name.strip():
            errors.append(f"request {request_label} tool_name must be non-empty")
        _validate_enum(errors, "request", request_label, "action", request.action, Action)
        _validate_scope(errors, f"request {request_label}", request.requested_scope)
    _validate_expected_decisions(errors, scenario, call_ids)
    return errors


def require_valid_trace_scenario(scenario: Any) -> None:
    errors = validate_trace_scenario(scenario)
    if errors:
        raise ValueError(f"invalid TraceScenario: {'; '.join(errors)}")


def _validate_rule_environment_refs(
    errors: list[str],
    rule: Any,
    data_by_id: dict[str, Any],
    valid_effect: bool,
    valid_consent: bool,
) -> None:
    missing_refs = sorted(set(rule.allow_refs) - set(data_by_id))
    if missing_refs:
        errors.append(f"policy rule {rule.rule_id} references missing data objects: {', '.join(missing_refs)}")
    for data_ref in rule.allow_refs:
        data_object = data_by_id.get(data_ref)
        if data_object is None:
            continue
        if data_object.resource_type != rule.resource_type:
            errors.append(
                f"policy rule {rule.rule_id} references {data_ref} with resource_type "
                f"{_label_value(data_object.resource_type)}, not {_label_value(rule.resource_type)}"
            )
        if valid_effect and valid_consent and _allows_dangerous_unrelated_without_confirmation(rule, data_object):
            errors.append(
                f"policy rule {rule.rule_id} allows dangerous unrelated data {data_ref} without confirmation"
            )


def _validate_expected_decisions(errors: list[str], scenario: Any, call_ids: set[str]) -> None:
    expected_call_ids: list[str] = []
    for index, expected in enumerate(scenario.expected_decisions):
        label = f"scenario {scenario.scenario_id} expected_decisions[{index}]"
        if not isinstance(expected, tuple) or len(expected) != 2:
            errors.append(f"{label} must be a call_id and decision tuple")
            continue
        call_id, decision = expected
        if not isinstance(call_id, str) or not call_id.strip():
            errors.append(f"{label} call_id must be a non-empty string")
        else:
            expected_call_ids.append(call_id)
            if call_id not in call_ids:
                errors.append(f"{label} references missing trace request: {call_id}")
        _validate_enum(errors, "expected decision", call_id, "decision", decision, DecisionLabel)
    _extend_duplicate_errors(
        errors,
        f"expected decision call_id in scenario {scenario.scenario_id}",
        expected_call_ids,
    )


def _allows_dangerous_unrelated_without_confirmation(rule: Any, data_object: Any) -> bool:
    return (
        rule.effect in PERMISSIVE_DECISIONS
        and rule.consent_level not in CONFIRMATION_CONSENT
        and data_object.relevance == "unrelated_private"
        and data_object.sensitivity == "dangerous"
    )


def _data_by_id(environment: Any, errors: list[str]) -> dict[str, Any]:
    data_by_id: dict[str, Any] = {}
    _extend_duplicate_errors(errors, "data_id", (obj.data_id for obj in environment.data_objects))
    for obj in environment.data_objects:
        if not obj.data_id.strip():
            errors.append("data_id must be non-empty")
        if obj.data_id in data_by_id:
            continue
        data_by_id[obj.data_id] = obj
        _validate_enum(errors, "data object", obj.data_id or "<missing>", "resource_type", obj.resource_type, ResourceType)
        _validate_label(errors, obj.data_id, "relevance", obj.relevance, DATA_RELEVANCE_LABELS)
        _validate_label(errors, obj.data_id, "sensitivity", obj.sensitivity, DATA_SENSITIVITY_LABELS)
        _validate_label(errors, obj.data_id, "trust", obj.trust, DATA_TRUST_LABELS)
    return data_by_id


def _validate_scope(errors: list[str], label: str, scope: Any) -> None:
    _validate_enum(errors, label, "", "resource_type", scope.resource_type, ResourceType)
    if not scope.selector_type.strip():
        errors.append(f"{label} selector_type must be non-empty")
    if not scope.selector_value.strip():
        errors.append(f"{label} selector_value must be non-empty")


def _validate_enum(
    errors: list[str],
    record_type: str,
    record_id: str,
    field_name: str,
    value: Any,
    enum_cls: type[StrEnum],
) -> bool:
    if isinstance(value, enum_cls):
        return True
    if isinstance(value, str) and value in {item.value for item in enum_cls}:
        return True
    allowed = ", ".join(item.value for item in enum_cls)
    label = f"{record_type} {record_id}".strip()
    errors.append(f"{label} {field_name} has invalid label {value!r}; allowed: {allowed}")
    return False


def _validate_label(errors: list[str], data_id: str, field_name: str, value: str, allowed: set[str]) -> None:
    if value in allowed:
        return
    errors.append(f"{data_id} has invalid {field_name} label: {value}")


def _label_value(value: Any) -> Any:
    return value.value if isinstance(value, StrEnum) else value


def _extend_duplicate_errors(errors: list[str], label: str, values: Iterable[str]) -> None:
    for value, count in Counter(values).items():
        if value and count > 1:
            errors.append(f"duplicate {label}: {value}")
