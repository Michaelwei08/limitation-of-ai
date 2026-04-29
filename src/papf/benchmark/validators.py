"""Validation for synthetic benchmark bundles."""

from __future__ import annotations

from papf.benchmark.models import BenchmarkTask, EnvironmentBundle


def validate_task_bundle(task: BenchmarkTask, environment: EnvironmentBundle) -> list[str]:
    errors: list[str] = []
    data_ids = environment.data_ids()
    missing_refs = sorted(set(task.environment_refs) - data_ids)
    if missing_refs:
        errors.append(f"task references missing data objects: {', '.join(missing_refs)}")

    rule_refs = {
        data_ref
        for rule in task.policy_pack.rules
        for data_ref in rule.allow_refs
    }
    missing_rule_refs = sorted(rule_refs - data_ids)
    if missing_rule_refs:
        errors.append(f"policy rules reference missing data objects: {', '.join(missing_rule_refs)}")

    for obj in environment.data_objects:
        if obj.relevance not in {"necessary", "supporting", "available_unnecessary", "unrelated_private"}:
            errors.append(f"{obj.data_id} has invalid relevance label: {obj.relevance}")
        if obj.sensitivity not in {"ordinary", "sensitive", "dangerous"}:
            errors.append(f"{obj.data_id} has invalid sensitivity label: {obj.sensitivity}")
        if obj.trust not in {"trusted_content", "untrusted_content"}:
            errors.append(f"{obj.data_id} has invalid trust label: {obj.trust}")
    return errors
