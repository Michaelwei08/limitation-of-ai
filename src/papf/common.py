"""Shared enums and scope primitives for PAPF."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Action(StrEnum):
    READ = "read"
    SEARCH = "search"
    DRAFT = "draft"
    SEND = "send"
    FORWARD = "forward"
    UPLOAD = "upload"
    BROWSE = "browse"


class ResourceType(StrEnum):
    EMAIL_THREAD = "email_thread"
    ATTACHMENT = "attachment"
    LOCAL_FILE = "local_file"
    EMAIL_DRAFT = "email_draft"
    WEBPAGE = "webpage"


class ConsentLevel(StrEnum):
    NONE = "none"
    CONFIRM = "confirm"
    HIGH_RISK_CONFIRM = "high_risk_confirm"
    DISALLOW = "disallow"


class DecisionLabel(StrEnum):
    ALLOW = "allow"
    ALLOW_WITH_NARROWED_SCOPE = "allow_with_narrowed_scope"
    ALLOW_WITH_REDACTION = "allow_with_redaction"
    REQUIRE_CONFIRMATION = "require_confirmation"
    DENY = "deny"


class ExecutionStatus(StrEnum):
    EXECUTED = "executed"
    BLOCKED = "blocked"
    ABORTED = "aborted"
    SIMULATED = "simulated"
    FAILED = "failed"


@dataclass(frozen=True)
class ScopeSpec:
    """Machine-checkable action scope.

    Broad selectors are intentionally not treated as matching narrow references;
    they must be narrowed by policy before execution.
    """

    resource_type: ResourceType
    selector_type: str
    selector_value: str
    destination: str | None = None

    @classmethod
    def data_ref(cls, resource_type: ResourceType, data_id: str) -> "ScopeSpec":
        return cls(resource_type=resource_type, selector_type="data_id", selector_value=data_id)

    @property
    def is_broad(self) -> bool:
        return self.selector_type in {"all", "directory", "query", "search"}

    def matches_data_ref(self, data_id: str) -> bool:
        return self.selector_type == "data_id" and self.selector_value == data_id

    def to_dict(self) -> dict[str, str | None]:
        return {
            "resource_type": self.resource_type.value,
            "selector_type": self.selector_type,
            "selector_value": self.selector_value,
            "destination": self.destination,
        }


def require_non_empty(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must be non-empty")
