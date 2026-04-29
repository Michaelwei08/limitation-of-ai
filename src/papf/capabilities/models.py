"""Capability records."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import Action, ConsentLevel, ScopeSpec


@dataclass(frozen=True)
class Capability:
    capability_id: str
    action: Action
    scope: ScopeSpec
    purpose_binding: str
    consent_level: ConsentLevel
    session_bound: bool = True
    expiration: str | None = None


@dataclass(frozen=True)
class CapabilityBundle:
    task_id: str
    active_capabilities: tuple[Capability, ...]
    dormant_capabilities: tuple[Capability, ...] = ()
    compiler_notes: tuple[str, ...] = ()


def capability_matches_request(capability: Capability, action: Action, scope: ScopeSpec) -> bool:
    if capability.action != action:
        return False
    if capability.scope.resource_type != scope.resource_type:
        return False
    if scope.destination and capability.scope.destination and scope.destination != capability.scope.destination:
        return False
    if scope.is_broad:
        return False
    return capability.scope.matches_data_ref(scope.selector_value)
