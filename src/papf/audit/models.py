"""Append-only audit records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from papf.enforcement.redaction import RedactionArtifact


@dataclass(frozen=True)
class AuditEvent:
    audit_event_id: str
    run_id: str
    task_id: str
    event_index: int
    event_type: str
    actor: str
    summary: str
    outcome: str
    related_call_id: str | None = None
    related_rule_ids: tuple[str, ...] = ()
    related_data_refs: tuple[str, ...] = ()
    related_redaction_artifact_refs: tuple[str, ...] = ()
    explanation: str = ""
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunAuditLog:
    run_id: str
    events: tuple[AuditEvent, ...]
    redaction_artifacts: tuple["RedactionArtifact", ...] = ()

    def append(self, event: AuditEvent) -> "RunAuditLog":
        if event.run_id != self.run_id:
            raise ValueError("audit event run_id must match log run_id")
        return RunAuditLog(
            run_id=self.run_id,
            events=(*self.events, event),
            redaction_artifacts=self.redaction_artifacts,
        )

    def redaction_artifact_ids(self) -> set[str]:
        return {artifact.redaction_artifact_id for artifact in self.redaction_artifacts}
