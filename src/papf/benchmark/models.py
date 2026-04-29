"""Benchmark task and environment records."""

from __future__ import annotations

from dataclasses import dataclass

from papf.common import Action, DecisionLabel, ResourceType, ScopeSpec
from papf.policy.models import PolicyPack


@dataclass(frozen=True)
class DataObject:
    data_id: str
    resource_type: ResourceType
    relevance: str
    sensitivity: str
    trust: str
    contains_adversarial_content: bool = False


@dataclass(frozen=True)
class EnvironmentBundle:
    environment_id: str
    data_objects: tuple[DataObject, ...]

    def data_ids(self) -> set[str]:
        return {obj.data_id for obj in self.data_objects}


@dataclass(frozen=True)
class SaferAlternative:
    alternative_id: str
    description: str
    action: Action
    approved_scope: ScopeSpec
    trigger_decisions: tuple[DecisionLabel, ...] = (
        DecisionLabel.DENY,
        DecisionLabel.ALLOW_WITH_NARROWED_SCOPE,
    )


@dataclass(frozen=True)
class BenchmarkTask:
    task_id: str
    suite_id: str
    category: str
    difficulty: str
    user_request: str
    task_goal: str
    environment_refs: tuple[str, ...]
    expected_output_type: str
    success_criteria: tuple[str, ...]
    failure_criteria: tuple[str, ...]
    policy_pack: PolicyPack
    safer_alternatives: tuple[SaferAlternative, ...] = ()


@dataclass(frozen=True)
class BenchmarkCase:
    task: BenchmarkTask
    environment: EnvironmentBundle
    scenarios: tuple["TraceScenario", ...]
    case_id: str = ""
