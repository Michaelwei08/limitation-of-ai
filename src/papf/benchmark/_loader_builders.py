"""Build benchmark dataclasses from parsed benchmark mappings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import Any

from papf.benchmark.models import BenchmarkCase, BenchmarkTask, DataObject, EnvironmentBundle
from papf.benchmark.traces import TraceScenario
from papf.benchmark.validators import validate_task_bundle
from papf.common import Action, ConsentLevel, DecisionLabel, ResourceType, ScopeSpec
from papf.enforcement.models import ToolRequest
from papf.policy.models import PolicyPack, PolicyRule
from papf.policy.validators import validate_trace_scenario


def build_benchmark_case_from_mapping(raw_case: Mapping[str, Any]) -> BenchmarkCase:
    errors = _validate_synthetic_marker(raw_case)
    task_record = _required_mapping(raw_case, "task", "task", errors)
    environment_record = _required_mapping(raw_case, "environment", "environment", errors)
    policy_record = _required_mapping(raw_case, "policy", "policy", errors)
    trace_records = _required_sequence(raw_case, "traces", "traces", errors)
    if errors:
        raise ValueError("; ".join(errors))

    task_policy_pack_id = _required_str(task_record, "policy_pack_id", "task.policy_pack_id", errors)
    task_environment_id = _required_str(task_record, "environment_id", "task.environment_id", errors)
    environment_id = _required_str(environment_record, "environment_id", "environment.environment_id", errors)
    if task_environment_id and environment_id and task_environment_id != environment_id:
        errors.append(
            f"task.environment_id references {task_environment_id!r}, "
            f"but environment.environment_id is {environment_id!r}"
        )

    policy_pack = _build_policy_pack(policy_record, errors)
    if task_policy_pack_id and policy_pack.policy_pack_id and task_policy_pack_id != policy_pack.policy_pack_id:
        errors.append(
            f"task.policy_pack_id references {task_policy_pack_id!r}, "
            f"but policy.policy_pack_id is {policy_pack.policy_pack_id!r}"
        )

    environment = _build_environment(environment_record, errors)
    task = _build_task(task_record, policy_pack, errors)
    scenarios = tuple(
        _build_trace_scenario(record, index, task.task_id, environment.data_ids(), errors)
        for index, record in enumerate(trace_records)
        if isinstance(record, Mapping)
    )
    for index, record in enumerate(trace_records):
        if not isinstance(record, Mapping):
            errors.append(f"traces[{index}] must be an object")

    errors.extend(validate_task_bundle(task, environment))
    for scenario in scenarios:
        errors.extend(validate_trace_scenario(scenario))
    if errors:
        raise ValueError("; ".join(errors))
    return BenchmarkCase(task=task, environment=environment, scenarios=scenarios)


def _build_task(record: Mapping[str, Any], policy_pack: PolicyPack, errors: list[str]) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=_required_str(record, "task_id", "task.task_id", errors),
        suite_id=_required_str(record, "suite_id", "task.suite_id", errors),
        category=_required_str(record, "category", "task.category", errors),
        difficulty=_required_str(record, "difficulty", "task.difficulty", errors),
        user_request=_required_str(record, "user_request", "task.user_request", errors),
        task_goal=_required_str(record, "task_goal", "task.task_goal", errors),
        environment_refs=_str_tuple(record.get("environment_refs"), "task.environment_refs", errors),
        expected_output_type=_required_str(record, "expected_output_type", "task.expected_output_type", errors),
        success_criteria=_str_tuple(record.get("success_criteria"), "task.success_criteria", errors),
        failure_criteria=_str_tuple(record.get("failure_criteria"), "task.failure_criteria", errors),
        policy_pack=policy_pack,
    )


def _build_environment(record: Mapping[str, Any], errors: list[str]) -> EnvironmentBundle:
    objects = _required_sequence(record, "data_objects", "environment.data_objects", errors)
    return EnvironmentBundle(
        environment_id=_required_str(record, "environment_id", "environment.environment_id", errors),
        data_objects=tuple(
            _build_data_object(obj, index, errors)
            for index, obj in enumerate(objects)
            if isinstance(obj, Mapping)
        ),
    )


def _build_data_object(record: Mapping[str, Any], index: int, errors: list[str]) -> DataObject:
    path = f"environment.data_objects[{index}]"
    if record.get("synthetic") is not True:
        errors.append(f"{path}.synthetic must be true")
    return DataObject(
        data_id=_required_str(record, "data_id", f"{path}.data_id", errors),
        resource_type=_enum(ResourceType, record.get("resource_type"), f"{path}.resource_type", errors),
        relevance=_required_str(record, "relevance", f"{path}.relevance", errors),
        sensitivity=_required_str(record, "sensitivity", f"{path}.sensitivity", errors),
        trust=_required_str(record, "trust", f"{path}.trust", errors),
        contains_adversarial_content=bool(record.get("contains_adversarial_content", False)),
    )


def _build_policy_pack(record: Mapping[str, Any], errors: list[str]) -> PolicyPack:
    policy_pack_id = _required_str(record, "policy_pack_id", "policy.policy_pack_id", errors)
    rules = _required_sequence(record, "rules", "policy.rules", errors)
    return PolicyPack(
        policy_pack_id=policy_pack_id,
        rules=tuple(
            _build_policy_rule(rule, index, policy_pack_id, errors)
            for index, rule in enumerate(rules)
            if isinstance(rule, Mapping)
        ),
    )


def _build_policy_rule(record: Mapping[str, Any], index: int, policy_pack_id: str, errors: list[str]) -> PolicyRule:
    path = f"policy.rules[{index}]"
    record_policy_pack_id = str(record.get("policy_pack_id", policy_pack_id))
    if record_policy_pack_id != policy_pack_id:
        errors.append(f"{path}.policy_pack_id must match policy.policy_pack_id {policy_pack_id!r}")
    return PolicyRule(
        rule_id=_required_str(record, "rule_id", f"{path}.rule_id", errors),
        policy_pack_id=record_policy_pack_id,
        resource_type=_enum(ResourceType, record.get("resource_type"), f"{path}.resource_type", errors),
        action=_enum(Action, record.get("action"), f"{path}.action", errors),
        effect=_enum(DecisionLabel, record.get("effect"), f"{path}.effect", errors),
        consent_level=_enum(ConsentLevel, record.get("consent_level"), f"{path}.consent_level", errors),
        allow_refs=_str_tuple(record.get("allow_refs"), f"{path}.allow_refs", errors),
        purpose_binding=_required_str(record, "purpose_binding", f"{path}.purpose_binding", errors),
        rationale_code=_required_str(record, "rationale_code", f"{path}.rationale_code", errors),
        redaction_requirements=_str_tuple(
            record.get("redaction_requirements", ()),
            f"{path}.redaction_requirements",
            errors,
        ),
        safer_alternative=_optional_str(record.get("safer_alternative"), f"{path}.safer_alternative", errors),
    )


def _build_trace_scenario(
    record: Mapping[str, Any],
    index: int,
    task_id: str,
    data_ids: set[str],
    errors: list[str],
) -> TraceScenario:
    path = f"traces[{index}]"
    trace_task_id = _optional_str(record.get("task_id"), f"{path}.task_id", errors)
    if trace_task_id is not None and trace_task_id != task_id:
        errors.append(f"{path}.task_id references {trace_task_id!r}, but task.task_id is {task_id!r}")
    request_records = _required_sequence(record, "requests", f"{path}.requests", errors)
    requests = tuple(
        _build_tool_request(request, index, request_index, data_ids, errors)
        for request_index, request in enumerate(request_records)
        if isinstance(request, Mapping)
    )
    call_ids = {request.call_id for request in requests}
    expected_decisions = _build_expected_decisions(record.get("expected_decisions", ()), path, call_ids, errors)
    return TraceScenario(
        scenario_id=_required_str(record, "scenario_id", f"{path}.scenario_id", errors),
        suite_id=_required_str(record, "suite_id", f"{path}.suite_id", errors),
        description=_required_str(record, "description", f"{path}.description", errors),
        requests=requests,
        expected_decisions=expected_decisions,
    )


def _build_tool_request(
    record: Mapping[str, Any],
    trace_index: int,
    request_index: int,
    data_ids: set[str],
    errors: list[str],
) -> ToolRequest:
    path = f"traces[{trace_index}].requests[{request_index}]"
    scope_record = _required_mapping(record, "scope", f"{path}.scope", errors)
    scope = ScopeSpec(
        resource_type=_enum(ResourceType, scope_record.get("resource_type"), f"{path}.scope.resource_type", errors),
        selector_type=_required_str(scope_record, "selector_type", f"{path}.scope.selector_type", errors),
        selector_value=_required_str(scope_record, "selector_value", f"{path}.scope.selector_value", errors),
        destination=_optional_str(scope_record.get("destination"), f"{path}.scope.destination", errors),
    )
    if scope.selector_type == "data_id" and scope.selector_value not in data_ids:
        errors.append(f"{path}.scope.selector_value references missing data object: {scope.selector_value}")
    input_refs = _str_tuple(record.get("input_refs", ()), f"{path}.input_refs", errors)
    missing_input_refs = sorted(set(input_refs) - data_ids)
    if missing_input_refs:
        errors.append(f"{path}.input_refs reference missing data objects: {', '.join(missing_input_refs)}")
    return ToolRequest(
        call_id=_required_str(record, "call_id", f"{path}.call_id", errors),
        tool_name=_required_str(record, "tool_name", f"{path}.tool_name", errors),
        action=_enum(Action, record.get("action"), f"{path}.action", errors),
        requested_scope=scope,
        input_refs=input_refs,
        destination=_optional_str(record.get("destination"), f"{path}.destination", errors),
    )


def _build_expected_decisions(
    raw: Any,
    path: str,
    call_ids: set[str],
    errors: list[str],
) -> tuple[tuple[str, DecisionLabel], ...]:
    records = _sequence(raw, f"{path}.expected_decisions", errors)
    decisions = []
    for index, record in enumerate(records):
        item_path = f"{path}.expected_decisions[{index}]"
        if not isinstance(record, Mapping):
            errors.append(f"{item_path} must be an object")
            continue
        call_id = _required_str(record, "call_id", f"{item_path}.call_id", errors)
        if call_id not in call_ids:
            errors.append(f"{item_path}.call_id references missing trace request: {call_id}")
        decisions.append((call_id, _enum(DecisionLabel, record.get("decision"), f"{item_path}.decision", errors)))
    return tuple(decisions)


def _validate_synthetic_marker(raw_case: Mapping[str, Any]) -> list[str]:
    if raw_case.get("synthetic") is not True:
        return ["benchmark case synthetic must be true"]
    return []


def _required_mapping(record: Mapping[str, Any], key: str, path: str, errors: list[str]) -> Mapping[str, Any]:
    value = record.get(key)
    if isinstance(value, Mapping):
        return value
    errors.append(f"{path} must be an object")
    return {}


def _required_sequence(record: Mapping[str, Any], key: str, path: str, errors: list[str]) -> Sequence[Any]:
    return _sequence(record.get(key), path, errors)


def _sequence(value: Any, path: str, errors: list[str]) -> Sequence[Any]:
    if isinstance(value, (list, tuple)):
        return value
    errors.append(f"{path} must be a list")
    return ()


def _required_str(record: Mapping[str, Any], key: str, path: str, errors: list[str]) -> str:
    value = record.get(key)
    if isinstance(value, str) and value.strip():
        return value
    errors.append(f"{path} must be a non-empty string")
    return ""


def _optional_str(value: Any, path: str, errors: list[str]) -> str | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip():
        return value
    errors.append(f"{path} must be a non-empty string when provided")
    return None


def _str_tuple(value: Any, path: str, errors: list[str]) -> tuple[str, ...]:
    values = _sequence(value, path, errors)
    result: list[str] = []
    for index, item in enumerate(values):
        if isinstance(item, str) and item.strip():
            result.append(item)
        else:
            errors.append(f"{path}[{index}] must be a non-empty string")
    return tuple(result)


def _enum(enum_cls: type[StrEnum], value: Any, path: str, errors: list[str]) -> Any:
    if not isinstance(value, str):
        errors.append(f"{path} must be a string enum label")
        return next(iter(enum_cls))
    try:
        return enum_cls(value)
    except ValueError:
        allowed = ", ".join(item.value for item in enum_cls)
        errors.append(f"{path} has invalid enum label {value!r}; allowed: {allowed}")
        return next(iter(enum_cls))
