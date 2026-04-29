"""File-backed benchmark case loader."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from papf.benchmark._loader_builders import build_benchmark_case_from_mapping
from papf.benchmark.models import BenchmarkCase


class BenchmarkLoaderError(ValueError):
    """Raised when a benchmark file is malformed or internally inconsistent."""


def load_benchmark_case(path: str | Path) -> BenchmarkCase:
    file_path = Path(path)
    raw_case = _load_mapping(file_path)
    try:
        return build_benchmark_case_from_mapping(raw_case)
    except BenchmarkLoaderError:
        raise
    except ValueError as exc:
        raise BenchmarkLoaderError(f"invalid benchmark case {file_path}: {exc}") from exc


def load_benchmark_cases(path: str | Path) -> tuple[BenchmarkCase, ...]:
    root = Path(path)
    if root.is_file():
        return (load_benchmark_case(root),)
    if not root.is_dir():
        raise BenchmarkLoaderError(f"benchmark path does not exist: {root}")

    case_files = tuple(
        sorted(
            child
            for child in root.iterdir()
            if child.is_file() and child.suffix.lower() in {".json", ".yaml", ".yml"}
        )
    )
    if not case_files:
        raise BenchmarkLoaderError(f"benchmark directory contains no JSON or YAML cases: {root}")
    return tuple(load_benchmark_case(case_file) for case_file in case_files)


def _load_mapping(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise BenchmarkLoaderError(f"benchmark case file does not exist: {path}")
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
        elif suffix in {".yaml", ".yml"}:
            data = _load_yaml(path)
        else:
            raise BenchmarkLoaderError(f"unsupported benchmark file extension: {path.suffix}")
    except json.JSONDecodeError as exc:
        raise BenchmarkLoaderError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, Mapping):
        raise BenchmarkLoaderError(f"benchmark case root must be an object: {path}")
    return data


def _load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise BenchmarkLoaderError("PyYAML is required to load YAML benchmark cases") from exc
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BenchmarkLoaderError(f"invalid YAML in {path}: {exc}") from exc
