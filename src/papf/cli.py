"""Command-line experiment runner for PAPF benchmark suites."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from papf.baselines import BaselineMode, evaluate_baseline_scenario
from papf.benchmark.loader import load_benchmark_cases
from papf.benchmark.models import BenchmarkCase
from papf.benchmark.traces import TraceScenario
from papf.evaluation.results import EvaluationCaseResult, EvaluationSuiteResult
from papf.evaluation.runner import evaluate_scenario
from papf.evaluation.serialization import SerializedRun, write_evaluation_suite


class ExperimentConfigError(ValueError):
    """Raised when an experiment config is invalid or references missing records."""


class ExperimentMode(StrEnum):
    PAPF = "papf"
    BROAD_ACCESS = "broad_access"
    PROMPT_ONLY = "prompt_only"


@dataclass(frozen=True)
class ExperimentRun:
    serialized_run: SerializedRun
    config_snapshot_path: Path
    result_count: int


def run_experiment_config(
    config_path: str | Path,
    *,
    timestamp: str | None = None,
    repo_root: str | Path | None = None,
) -> ExperimentRun:
    config_file = Path(config_path)
    root = Path(repo_root) if repo_root is not None else Path.cwd()
    raw_config = _load_config(config_file)
    suite = build_experiment_suite(raw_config, repo_root=root)
    output_dir = _resolve_path(_required_str(raw_config, "output_dir"), root)
    run_label = _required_str(raw_config, "config_id")
    written = write_evaluation_suite(
        suite,
        output_dir,
        timestamp=timestamp,
        repo_root=root,
        run_label=run_label,
    )
    snapshot_path = written.output_dir / "config_snapshot.json"
    _write_config_snapshot(
        snapshot_path,
        raw_config=raw_config,
        config_path=config_file,
        repo_root=root,
        written=written,
        result_count=len(suite.results),
    )
    return ExperimentRun(
        serialized_run=written,
        config_snapshot_path=snapshot_path,
        result_count=len(suite.results),
    )


def build_experiment_suite(raw_config: Mapping[str, Any], *, repo_root: Path) -> EvaluationSuiteResult:
    config_id = _required_str(raw_config, "config_id")
    benchmark_path = _resolve_path(_required_str(raw_config, "benchmark_path"), repo_root)
    modes = _modes(raw_config)
    cases = _select_cases(load_benchmark_cases(benchmark_path), _optional_strs(raw_config, "case_ids"))
    suite_ids = _optional_strs(raw_config, "suite_ids")
    scenario_ids = _optional_strs(raw_config, "scenario_ids")
    selected = _select_scenarios(cases, suite_ids=suite_ids, scenario_ids=scenario_ids)

    results: list[EvaluationCaseResult] = []
    for mode in modes:
        for case, scenario in selected:
            run_id = _run_id(config_id, mode, case, scenario)
            results.append(_evaluate(mode=mode, run_id=run_id, case=case, scenario=scenario, raw_config=raw_config))
    if not results:
        raise ExperimentConfigError("experiment config selected zero scenarios")
    return EvaluationSuiteResult(results=tuple(results))


def _evaluate(
    *,
    mode: ExperimentMode,
    run_id: str,
    case: BenchmarkCase,
    scenario: TraceScenario,
    raw_config: Mapping[str, Any],
) -> EvaluationCaseResult:
    if mode == ExperimentMode.PAPF:
        return evaluate_scenario(run_id=run_id, task=case.task, environment=case.environment, scenario=scenario)
    baseline_mode = BaselineMode(mode.value)
    advisory = str(raw_config.get("prompt_only_advisory", ""))
    if mode == ExperimentMode.PROMPT_ONLY and advisory.strip():
        return evaluate_baseline_scenario(
            run_id=run_id,
            task=case.task,
            environment=case.environment,
            scenario=scenario,
            mode=baseline_mode,
            advisory_text=advisory,
        )
    return evaluate_baseline_scenario(
        run_id=run_id,
        task=case.task,
        environment=case.environment,
        scenario=scenario,
        mode=baseline_mode,
    )


def _select_cases(cases: tuple[BenchmarkCase, ...], case_ids: tuple[str, ...]) -> tuple[BenchmarkCase, ...]:
    if not cases:
        raise ExperimentConfigError("benchmark path loaded zero cases")
    by_id: dict[str, BenchmarkCase] = {}
    for case in cases:
        if not case.case_id:
            raise ExperimentConfigError(f"benchmark task {case.task.task_id} is missing case_id")
        if case.case_id in by_id:
            raise ExperimentConfigError(f"duplicate benchmark case_id: {case.case_id}")
        by_id[case.case_id] = case
    if not case_ids:
        return cases
    missing = tuple(case_id for case_id in case_ids if case_id not in by_id)
    if missing:
        raise ExperimentConfigError(f"config references missing case ids: {', '.join(missing)}")
    return tuple(by_id[case_id] for case_id in case_ids)


def _select_scenarios(
    cases: tuple[BenchmarkCase, ...],
    *,
    suite_ids: tuple[str, ...],
    scenario_ids: tuple[str, ...],
) -> tuple[tuple[BenchmarkCase, TraceScenario], ...]:
    available_suite_ids = {scenario.suite_id for case in cases for scenario in case.scenarios}
    available_scenario_ids = {scenario.scenario_id for case in cases for scenario in case.scenarios}
    _raise_missing("suite ids", suite_ids, available_suite_ids)
    _raise_missing("scenario ids", scenario_ids, available_scenario_ids)

    selected: list[tuple[BenchmarkCase, TraceScenario]] = []
    for case in cases:
        for scenario in case.scenarios:
            if suite_ids and scenario.suite_id not in suite_ids:
                continue
            if scenario_ids and scenario.scenario_id not in scenario_ids:
                continue
            selected.append((case, scenario))
    return tuple(selected)


def _raise_missing(label: str, requested: tuple[str, ...], available: set[str]) -> None:
    missing = tuple(value for value in requested if value not in available)
    if missing:
        raise ExperimentConfigError(f"config references missing {label}: {', '.join(missing)}")


def _modes(raw_config: Mapping[str, Any]) -> tuple[ExperimentMode, ...]:
    raw_modes: Any
    if "modes" in raw_config:
        raw_modes = raw_config["modes"]
    elif "mode" in raw_config:
        raw_modes = (raw_config["mode"],)
    else:
        raise ExperimentConfigError("config must include modes or mode")
    labels = _strs(raw_modes, "modes")
    modes: list[ExperimentMode] = []
    for label in labels:
        try:
            modes.append(ExperimentMode(label))
        except ValueError as exc:
            allowed = ", ".join(mode.value for mode in ExperimentMode)
            raise ExperimentConfigError(f"invalid experiment mode {label!r}; allowed: {allowed}") from exc
    return tuple(modes)


def _run_id(config_id: str, mode: ExperimentMode, case: BenchmarkCase, scenario: TraceScenario) -> str:
    return f"{config_id}_{mode.value}_{case.case_id}_{scenario.scenario_id}"


def _load_config(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise ExperimentConfigError(f"experiment config does not exist: {path}")
    if path.suffix.lower() != ".json":
        raise ExperimentConfigError(f"experiment config must be JSON: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExperimentConfigError(f"invalid JSON experiment config {path}: {exc}") from exc
    if not isinstance(data, Mapping):
        raise ExperimentConfigError(f"experiment config root must be an object: {path}")
    return data


def _write_config_snapshot(
    path: Path,
    *,
    raw_config: Mapping[str, Any],
    config_path: Path,
    repo_root: Path,
    written: SerializedRun,
    result_count: int,
) -> None:
    snapshot = {
        "config": dict(raw_config),
        "config_path": str(config_path),
        "repo_root": str(repo_root),
        "result_count": result_count,
        "artifacts": {
            "metadata": str(written.metadata_path),
            "metrics_jsonl": str(written.metrics_jsonl_path),
            "metrics_csv": str(written.metrics_csv_path),
            "decisions_jsonl": str(written.decisions_jsonl_path),
            "audit_summaries_jsonl": str(written.audit_jsonl_path),
        },
    }
    path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _required_str(raw_config: Mapping[str, Any], key: str) -> str:
    value = raw_config.get(key)
    if isinstance(value, str) and value.strip():
        return value
    raise ExperimentConfigError(f"config.{key} must be a non-empty string")


def _optional_strs(raw_config: Mapping[str, Any], key: str) -> tuple[str, ...]:
    if key not in raw_config:
        return ()
    return _strs(raw_config[key], key)


def _strs(value: Any, path: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ExperimentConfigError(f"config.{path} must be a list of non-empty strings")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ExperimentConfigError(f"config.{path}[{index}] must be a non-empty string")
        result.append(item)
    return tuple(result)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic PAPF experiments.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run-experiment", help="Run a JSON experiment config.")
    run_parser.add_argument("--config", required=True, help="Path to an experiment config JSON file.")
    run_parser.add_argument("--timestamp", help="Optional fixed timestamp for deterministic metadata.")
    run_parser.add_argument("--repo-root", help="Repository root for relative config paths.")
    args = parser.parse_args(argv)

    if args.command == "run-experiment":
        try:
            run = run_experiment_config(args.config, timestamp=args.timestamp, repo_root=args.repo_root)
        except (ExperimentConfigError, ValueError) as exc:
            print(f"papf experiment failed: {exc}", file=sys.stderr)
            return 2
        print(str(run.serialized_run.output_dir))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
