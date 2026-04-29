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

    errors.extend(_validate_safer_alternatives(task, environment))
    errors.extend(validate_environment(environment))
    errors.extend(validate_policy_pack(task.policy_pack, environment))
    return errors


def _validate_safer_alternatives(task: BenchmarkTask, environment: EnvironmentBundle) -> list[str]:
    errors: list[str] = []
    data_by_id = {obj.data_id: obj for obj in environment.data_objects}
    seen_ids: set[str] = set()
    for alternative in task.safer_alternatives:
        label = alternative.alternative_id or "<missing>"
        if not alternative.alternative_id.strip():
            errors.append("safer alternative_id must be non-empty")
        elif alternative.alternative_id in seen_ids:
            errors.append(f"duplicate safer alternative_id: {alternative.alternative_id}")
        seen_ids.add(alternative.alternative_id)
        if not alternative.description.strip():
            errors.append(f"safer alternative {label} description must be non-empty")
        if alternative.approved_scope.is_broad:
            errors.append(f"safer alternative {label} approved scope must be narrow")
        if alternative.approved_scope.selector_type != "data_id":
            errors.append(f"safer alternative {label} approved scope must select a data_id")
            continue
        data_object = data_by_id.get(alternative.approved_scope.selector_value)
        if data_object is None:
            errors.append(
                f"safer alternative {label} references missing data object: "
                f"{alternative.approved_scope.selector_value}"
            )
            continue
        if data_object.resource_type != alternative.approved_scope.resource_type:
            errors.append(
                f"safer alternative {label} references {data_object.data_id} with resource_type "
                f"{data_object.resource_type.value}, not {alternative.approved_scope.resource_type.value}"
            )
        if data_object.relevance not in {"necessary", "supporting"}:
            errors.append(f"safer alternative {label} must reference necessary or supporting data")
    return errors
