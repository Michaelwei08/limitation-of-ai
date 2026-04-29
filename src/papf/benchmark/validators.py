"""Validation for synthetic benchmark bundles."""

from __future__ import annotations

from papf.benchmark.models import BenchmarkTask, EnvironmentBundle
from papf.policy.validators import validate_environment, validate_policy_pack


def validate_task_bundle(task: BenchmarkTask, environment: EnvironmentBundle) -> list[str]:
    errors: list[str] = []
    data_ids = environment.data_ids()
    missing_refs = sorted(set(task.environment_refs) - data_ids)
    if missing_refs:
        errors.append(f"task references missing data objects: {', '.join(missing_refs)}")

    errors.extend(validate_environment(environment))
    errors.extend(validate_policy_pack(task.policy_pack, environment))
    return errors
