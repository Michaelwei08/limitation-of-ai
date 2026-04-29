"""Task intent records."""

from __future__ import annotations

from dataclasses import dataclass, field

from papf.common import Action, ResourceType, ScopeSpec


@dataclass(frozen=True)
class IntentIssue:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class TaskIntent:
    task_id: str
    task_summary: str
    user_goal: str
    requested_actions: tuple[Action, ...]
    candidate_resource_types: tuple[ResourceType, ...]
    candidate_resource_refs: tuple[str, ...] = ()
    proposed_scope_constraints: tuple[ScopeSpec, ...] = ()
    expected_output_type: str = ""
    uncertainty_flags: tuple[str, ...] = ()
    safety_notes: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

    def require_valid(self) -> None:
        errors = [issue for issue in validate_intent(self) if issue.severity == "error"]
        if errors:
            joined = "; ".join(f"{issue.code}: {issue.message}" for issue in errors)
            raise ValueError(f"invalid TaskIntent: {joined}")


def validate_intent(intent: TaskIntent) -> list[IntentIssue]:
    issues: list[IntentIssue] = []
    if not intent.task_id.strip():
        issues.append(IntentIssue("error", "MISSING_TASK_ID", "task_id must be non-empty"))
    if not intent.user_goal.strip():
        issues.append(IntentIssue("error", "MISSING_USER_GOAL", "user_goal must be non-empty"))
    if not intent.requested_actions:
        issues.append(IntentIssue("error", "MISSING_ACTIONS", "requested_actions must not be empty"))
    if not intent.candidate_resource_types:
        issues.append(
            IntentIssue("error", "MISSING_RESOURCE_TYPES", "candidate_resource_types must not be empty")
        )
    for scope in intent.proposed_scope_constraints:
        if scope.resource_type not in intent.candidate_resource_types:
            issues.append(
                IntentIssue(
                    "error",
                    "SCOPE_RESOURCE_MISMATCH",
                    f"scope resource_type {scope.resource_type.value} is not in candidate_resource_types",
                )
            )
    if "ambiguous_scope" in intent.uncertainty_flags and intent.candidate_resource_refs:
        issues.append(
            IntentIssue(
                "warning",
                "AMBIGUOUS_WITH_REFS",
                "intent reports ambiguous scope despite candidate_resource_refs",
            )
        )
    return issues
