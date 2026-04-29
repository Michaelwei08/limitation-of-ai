"""Non-authoritative intent proposal interface.

Model-assisted proposers can suggest TaskIntent-shaped data, but this module
keeps that output outside the security-critical path until schema validation
accepts it.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol

from papf.capabilities.compiler import compile_capabilities_from_policy
from papf.capabilities.models import CapabilityBundle
from papf.common import Action, ResourceType, ScopeSpec
from papf.intent.models import IntentIssue, TaskIntent, validate_intent
from papf.policy.models import PolicyPack


@dataclass(frozen=True)
class IntentProposal:
    """Raw candidate intent emitted by an advisory proposer."""

    proposal_id: str
    proposer_mode: str
    raw_intent: Mapping[str, Any]
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProposalValidationResult:
    proposal_id: str
    proposer_mode: str
    accepted_intent: TaskIntent | None
    issues: tuple[IntentIssue, ...]

    @property
    def is_valid(self) -> bool:
        return self.accepted_intent is not None and not any(issue.severity == "error" for issue in self.issues)

    def require_intent(self) -> TaskIntent:
        if self.accepted_intent is None:
            joined = "; ".join(f"{issue.code}: {issue.message}" for issue in self.issues)
            raise ValueError(f"invalid IntentProposal {self.proposal_id}: {joined}")
        return self.accepted_intent


class IntentProposer(Protocol):
    """Interface for optional advisory intent proposers."""

    def propose(self, user_request: str, context: Mapping[str, Any] | None = None) -> IntentProposal:
        """Return a candidate intent proposal without granting authority."""


@dataclass(frozen=True)
class DeterministicFakeIntentProposer:
    """Test/deterministic proposer that returns a configured raw proposal."""

    proposal_id: str
    raw_intent: Mapping[str, Any]
    proposer_mode: str = "deterministic_fake"
    notes: tuple[str, ...] = field(default_factory=tuple)

    def propose(self, user_request: str, context: Mapping[str, Any] | None = None) -> IntentProposal:
        if not user_request.strip():
            raise ValueError("user_request must be non-empty")
        return IntentProposal(
            proposal_id=self.proposal_id,
            proposer_mode=self.proposer_mode,
            raw_intent=self.raw_intent,
            notes=self.notes,
        )


def validate_intent_proposal(
    proposal: IntentProposal,
    known_data_refs: Iterable[str] | None = None,
) -> ProposalValidationResult:
    """Validate raw proposal schema and return an accepted TaskIntent candidate."""

    issues: list[IntentIssue] = []
    if not isinstance(proposal.proposal_id, str) or not proposal.proposal_id.strip():
        issues.append(_error("SCHEMA_PROPOSAL_ID", "proposal_id must be a non-empty string"))
    if not isinstance(proposal.proposer_mode, str) or not proposal.proposer_mode.strip():
        issues.append(_error("SCHEMA_PROPOSER_MODE", "proposer_mode must be a non-empty string"))
    raw = proposal.raw_intent
    if not isinstance(raw, Mapping):
        issues.append(_error("SCHEMA_RAW_INTENT", "raw_intent must be an object"))
        return _result(proposal, None, issues)

    known_refs = set(known_data_refs) if known_data_refs is not None else None
    task_id = _required_str(raw, "task_id", issues)
    task_summary = _required_str(raw, "task_summary", issues)
    user_goal = _required_str(raw, "user_goal", issues)
    requested_actions = _enum_tuple(Action, raw.get("requested_actions"), "requested_actions", issues)
    resource_types = _enum_tuple(
        ResourceType,
        raw.get("candidate_resource_types"),
        "candidate_resource_types",
        issues,
    )
    candidate_refs = _str_tuple(raw.get("candidate_resource_refs", ()), "candidate_resource_refs", issues)
    scopes = _scope_tuple(raw.get("proposed_scope_constraints", ()), "proposed_scope_constraints", issues)
    uncertainty_flags = _str_tuple(raw.get("uncertainty_flags", ()), "uncertainty_flags", issues)
    safety_notes = _str_tuple(raw.get("safety_notes", ()), "safety_notes", issues)
    expected_output_type = _optional_str(raw.get("expected_output_type", ""), "expected_output_type", issues)
    metadata = _metadata(raw.get("metadata", {}), issues)

    if known_refs is not None:
        _validate_known_refs(candidate_refs, scopes, known_refs, issues)

    if any(issue.severity == "error" for issue in issues):
        return _result(proposal, None, issues)

    intent = TaskIntent(
        task_id=task_id,
        task_summary=task_summary,
        user_goal=user_goal,
        requested_actions=requested_actions,
        candidate_resource_types=resource_types,
        candidate_resource_refs=candidate_refs,
        proposed_scope_constraints=scopes,
        expected_output_type=expected_output_type,
        uncertainty_flags=uncertainty_flags,
        safety_notes=safety_notes,
        metadata=metadata,
    )
    issues.extend(validate_intent(intent))
    if any(issue.severity == "error" for issue in issues):
        return _result(proposal, None, issues)
    return _result(proposal, intent, issues)


def compile_capabilities_from_proposal(
    proposal: IntentProposal,
    policy_pack: PolicyPack,
    known_data_refs: Iterable[str] | None = None,
) -> CapabilityBundle:
    """Compile only after the advisory proposal passes deterministic validation."""

    validation = validate_intent_proposal(proposal, known_data_refs=known_data_refs)
    intent = validation.require_intent()
    return compile_capabilities_from_policy(intent, policy_pack)


def _result(
    proposal: IntentProposal,
    accepted_intent: TaskIntent | None,
    issues: list[IntentIssue],
) -> ProposalValidationResult:
    return ProposalValidationResult(
        proposal_id=proposal.proposal_id,
        proposer_mode=proposal.proposer_mode,
        accepted_intent=accepted_intent,
        issues=tuple(issues),
    )


def _required_str(raw: Mapping[str, Any], field_name: str, issues: list[IntentIssue]) -> str:
    value = raw.get(field_name)
    if isinstance(value, str) and value.strip():
        return value
    issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{field_name} must be a non-empty string"))
    return ""


def _optional_str(value: Any, field_name: str, issues: list[IntentIssue]) -> str:
    if value == "":
        return ""
    if isinstance(value, str) and value.strip():
        return value
    issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{field_name} must be a string when provided"))
    return ""


def _str_tuple(value: Any, field_name: str, issues: list[IntentIssue]) -> tuple[str, ...]:
    values = _sequence(value, field_name, issues)
    result: list[str] = []
    for index, item in enumerate(values):
        if isinstance(item, str) and item.strip():
            result.append(item)
        else:
            issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{field_name}[{index}] must be a non-empty string"))
    return tuple(result)


def _enum_tuple(
    enum_cls: type[StrEnum],
    value: Any,
    field_name: str,
    issues: list[IntentIssue],
) -> tuple[Any, ...]:
    values = _sequence(value, field_name, issues)
    result: list[Any] = []
    allowed = ", ".join(item.value for item in enum_cls)
    for index, item in enumerate(values):
        if not isinstance(item, str):
            issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{field_name}[{index}] must be a string enum label"))
            continue
        try:
            result.append(enum_cls(item))
        except ValueError:
            issues.append(
                _error(
                    f"SCHEMA_{field_name.upper()}",
                    f"{field_name}[{index}] has invalid label {item!r}; allowed: {allowed}",
                )
            )
    return tuple(result)


def _scope_tuple(value: Any, field_name: str, issues: list[IntentIssue]) -> tuple[ScopeSpec, ...]:
    values = _sequence(value, field_name, issues)
    scopes: list[ScopeSpec] = []
    for index, item in enumerate(values):
        path = f"{field_name}[{index}]"
        if not isinstance(item, Mapping):
            issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{path} must be an object"))
            continue
        resource_type = _enum_value(ResourceType, item.get("resource_type"), f"{path}.resource_type", issues)
        selector_type = _required_scope_str(item, "selector_type", f"{path}.selector_type", issues)
        selector_value = _required_scope_str(item, "selector_value", f"{path}.selector_value", issues)
        destination = item.get("destination")
        if destination is not None and not (isinstance(destination, str) and destination.strip()):
            issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{path}.destination must be a non-empty string"))
            destination = None
        if resource_type is not None and selector_type and selector_value:
            scopes.append(ScopeSpec(resource_type, selector_type, selector_value, destination))
    return tuple(scopes)


def _enum_value(
    enum_cls: type[StrEnum],
    value: Any,
    path: str,
    issues: list[IntentIssue],
) -> Any | None:
    if not isinstance(value, str):
        issues.append(_error("SCHEMA_SCOPE", f"{path} must be a string enum label"))
        return None
    try:
        return enum_cls(value)
    except ValueError:
        allowed = ", ".join(item.value for item in enum_cls)
        issues.append(_error("SCHEMA_SCOPE", f"{path} has invalid label {value!r}; allowed: {allowed}"))
        return None


def _required_scope_str(raw: Mapping[str, Any], key: str, path: str, issues: list[IntentIssue]) -> str:
    value = raw.get(key)
    if isinstance(value, str) and value.strip():
        return value
    issues.append(_error("SCHEMA_SCOPE", f"{path} must be a non-empty string"))
    return ""


def _metadata(value: Any, issues: list[IntentIssue]) -> dict[str, str]:
    if not isinstance(value, Mapping):
        issues.append(_error("SCHEMA_METADATA", "metadata must be an object when provided"))
        return {}
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            issues.append(_error("SCHEMA_METADATA", "metadata keys and values must be strings"))
            continue
        result[key] = item
    return result


def _sequence(value: Any, field_name: str, issues: list[IntentIssue]) -> Sequence[Any]:
    if isinstance(value, (list, tuple)):
        return value
    issues.append(_error(f"SCHEMA_{field_name.upper()}", f"{field_name} must be a list"))
    return ()


def _validate_known_refs(
    candidate_refs: tuple[str, ...],
    scopes: tuple[ScopeSpec, ...],
    known_refs: set[str],
    issues: list[IntentIssue],
) -> None:
    missing = sorted(set(candidate_refs) - known_refs)
    if missing:
        issues.append(_error("UNKNOWN_CANDIDATE_REF", f"candidate_resource_refs unknown: {', '.join(missing)}"))
    missing_scope_refs = sorted(
        {scope.selector_value for scope in scopes if scope.selector_type == "data_id"} - known_refs
    )
    if missing_scope_refs:
        issues.append(_error("UNKNOWN_SCOPE_REF", f"scope data_id refs unknown: {', '.join(missing_scope_refs)}"))


def _error(code: str, message: str) -> IntentIssue:
    return IntentIssue("error", code, message)
