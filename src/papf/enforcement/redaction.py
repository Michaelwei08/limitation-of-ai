"""Redaction evidence records and validation."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import ScopeSpec
from papf.policy.models import PolicyDecision


@dataclass(frozen=True)
class RedactionArtifact:
    """Verifiable evidence that a scoped output was redacted before use.

    The artifact intentionally stores references and removed field labels only.
    It must not contain raw source or output payloads.
    """

    redaction_artifact_id: str
    run_id: str
    task_id: str
    call_id: str
    source_refs: tuple[str, ...]
    removed_field_labels: tuple[str, ...]
    output_ref: str
    rationale: str
    policy_decision_id: str | None = None


def validate_redaction_artifact(
    artifact: RedactionArtifact,
    *,
    run_id: str,
    task_id: str,
    call_id: str,
    decision: PolicyDecision,
    resolved_scope: ScopeSpec,
) -> list[str]:
    errors: list[str] = []
    _require_non_empty(errors, "redaction_artifact_id", artifact.redaction_artifact_id)
    _require_non_empty(errors, "run_id", artifact.run_id)
    _require_non_empty(errors, "task_id", artifact.task_id)
    _require_non_empty(errors, "call_id", artifact.call_id)
    _require_non_empty(errors, "output_ref", artifact.output_ref)
    _require_non_empty(errors, "rationale", artifact.rationale)

    if artifact.run_id != run_id:
        errors.append("redaction artifact run_id must match enforcement run_id")
    if artifact.task_id != task_id:
        errors.append("redaction artifact task_id must match enforcement task_id")
    if artifact.call_id != call_id:
        errors.append("redaction artifact call_id must match request call_id")
    if artifact.policy_decision_id and artifact.policy_decision_id != decision.policy_decision_id:
        errors.append("redaction artifact policy_decision_id must match policy decision")
    if not artifact.source_refs:
        errors.append("redaction artifact source_refs must be non-empty")
    if resolved_scope.selector_value not in artifact.source_refs:
        errors.append("redaction artifact source_refs must include the resolved source ref")
    if not artifact.removed_field_labels:
        errors.append("redaction artifact removed_field_labels must be non-empty")

    missing_labels = sorted(set(decision.redaction_requirements) - set(artifact.removed_field_labels))
    if missing_labels:
        errors.append(f"redaction artifact is missing required removed labels: {', '.join(missing_labels)}")
    if artifact.output_ref in artifact.source_refs:
        errors.append("redaction artifact output_ref must differ from source_refs")
    return errors


def require_valid_redaction_artifact(
    artifact: RedactionArtifact,
    *,
    run_id: str,
    task_id: str,
    call_id: str,
    decision: PolicyDecision,
    resolved_scope: ScopeSpec,
) -> None:
    errors = validate_redaction_artifact(
        artifact,
        run_id=run_id,
        task_id=task_id,
        call_id=call_id,
        decision=decision,
        resolved_scope=resolved_scope,
    )
    if errors:
        raise ValueError(f"invalid RedactionArtifact: {'; '.join(errors)}")


def _require_non_empty(errors: list[str], field_name: str, value: str) -> None:
    if not value.strip():
        errors.append(f"{field_name} must be non-empty")
