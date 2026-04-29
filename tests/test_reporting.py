import csv
import json
import unittest
from pathlib import Path

from papf.evaluation.reporting import generate_reporting_artifacts, load_run_artifacts


class ReportingTests(unittest.TestCase):
    def test_reports_are_derived_from_run_artifacts(self) -> None:
        root = Path("experiments/runs/test_reporting_artifacts")
        try:
            run_dir = root / "run"
            _prepare_dir(run_dir)
            _write_minimal_run(run_dir, broad_false_allows=7, prompt_over_access=0.42)

            generated = generate_reporting_artifacts(
                run_dir,
                tables_dir=root / "paper" / "tables",
                figures_dir=root / "paper" / "figures",
            )

            main_rows = _read_csv(generated.main_metrics_csv)
            broad_row = _row_by(main_rows, "mode", "broad_access")
            prompt_row = _row_by(main_rows, "mode", "prompt_only")
            self.assertEqual(broad_row["false_allow_count"], "7")
            self.assertEqual(prompt_row["over_access_rate"], "0.42")

            baseline_rows = _read_csv(generated.baseline_comparison_csv)
            broad_baseline = _row_by(baseline_rows, "baseline", "broad_access")
            self.assertEqual(broad_baseline["false_allow_delta_vs_papf"], "7")

            failure_rows = _read_csv(generated.failure_cases_csv)
            broad_failure = _row_by(failure_rows, "mode", "broad_access")
            self.assertIn("false_allow", broad_failure["failure_labels"])
            self.assertIn("call_broad:file_private", broad_failure["evidence"])

            provenance_rows = _read_csv(generated.provenance_csv)
            provenance = _row_by(provenance_rows, "run_id", "run_prompt")
            self.assertEqual(provenance["mode"], "prompt_only")
            self.assertEqual(provenance["metrics_artifact"], str(run_dir / "metrics.jsonl"))
            self.assertTrue(generated.task_success_figure.exists())
            self.assertIn("0.42", generated.main_metrics_csv.read_text(encoding="utf-8"))
        finally:
            _cleanup_known_files(root)

    def test_reporting_rejects_stale_metric_schema(self) -> None:
        root = Path("experiments/runs/test_reporting_stale_schema")
        try:
            run_dir = root / "run"
            _prepare_dir(run_dir)
            _write_minimal_run(run_dir, broad_false_allows=1, prompt_over_access=0.25)
            metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
            metadata["metric_schema_version"] = "papf.metrics.v2"
            (run_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "unsupported metric schema"):
                load_run_artifacts(run_dir)
        finally:
            _cleanup_known_files(root)


def _write_minimal_run(run_dir: Path, *, broad_false_allows: int, prompt_over_access: float) -> None:
    run_ids = ["run_papf", "run_broad", "run_prompt"]
    metadata = {
        "run_label": "test_run",
        "timestamp": "2026-04-29T00:00:00+00:00",
        "metric_schema_version": "papf.metrics.v3",
        "run_ids": run_ids,
        "scenario_ids": ["trace_case", "trace_case", "trace_case"],
        "suite_ids": ["attack", "attack", "attack"],
    }
    metrics = [
        _metric_row("run_papf", false_allow_count=0, over_access_rate=0.0),
        _metric_row("run_broad", false_allow_count=broad_false_allows, over_access_rate=0.5),
        _metric_row("run_prompt", false_allow_count=2, over_access_rate=prompt_over_access),
    ]
    decisions = [
        _decision_row("run_papf", "rule_allow_task_scope"),
        _decision_row("run_broad", "baseline:broad_access"),
        _decision_row("run_prompt", "baseline:prompt_only"),
    ]
    audit_rows = [
        _audit_row("run_broad", "call_broad", ("file_private",)),
        _audit_row("run_prompt", "call_prompt", ("webpage_trap",)),
    ]
    (run_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    _write_jsonl(run_dir / "metrics.jsonl", metrics)
    _write_jsonl(run_dir / "decisions.jsonl", decisions)
    _write_jsonl(run_dir / "audit_summaries.jsonl", audit_rows)


def _prepare_dir(path: Path) -> None:
    _cleanup_known_files(path.parent)
    path.mkdir(parents=True, exist_ok=True)


def _cleanup_known_files(root: Path) -> None:
    known_names = {
        "metadata.json",
        "metrics.jsonl",
        "decisions.jsonl",
        "audit_summaries.jsonl",
        "main_metrics.csv",
        "main_metrics.md",
        "baseline_comparison.csv",
        "baseline_comparison.md",
        "failure_cases.csv",
        "failure_cases.md",
        "run_provenance.csv",
        "run_provenance.md",
        "task_success_rate_by_mode.svg",
        "false_allows_by_mode.svg",
    }
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_file() and path.name in known_names:
            path.unlink()
    for path in sorted([p for p in root.rglob("*") if p.is_dir()], reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass
    try:
        root.rmdir()
    except OSError:
        pass


def _metric_row(run_id: str, *, false_allow_count: int, over_access_rate: float) -> dict[str, object]:
    return {
        "run_id": run_id,
        "task_id": "task_001",
        "scenario_id": "trace_case",
        "suite_id": "attack",
        "total_calls": 3,
        "executed_calls": 3,
        "blocked_calls": 0,
        "task_success_proxy": false_allow_count == 0 and over_access_rate == 0,
        "necessary_access_rate": 1.0,
        "over_access_rate": over_access_rate,
        "false_allow_count": false_allow_count,
        "false_deny_count": 0,
        "consent_prompts": 0,
        "redacted_access_count": 0,
        "unredacted_disclosure_count": 0,
        "recovery_quality": 0.0,
        "safe_partial_success": False,
        "task_failure": false_allow_count > 0 or over_access_rate > 0,
        "unsafe_workaround_count": 0,
        "auditability_completeness": 1.0,
    }


def _decision_row(run_id: str, rule_id: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "task_id": "task_001",
        "scenario_id": "trace_case",
        "suite_id": "attack",
        "call_id": f"{run_id}_call",
        "policy_decision_id": f"{run_id}_pd",
        "decision": "allow",
        "matched_rule_ids": [rule_id],
        "execution_status": "simulated",
        "may_execute": True,
        "reason": "test",
    }


def _audit_row(run_id: str, call_id: str, refs: tuple[str, ...]) -> dict[str, object]:
    return {
        "run_id": run_id,
        "task_id": "task_001",
        "scenario_id": "trace_case",
        "suite_id": "attack",
        "audit_event_id": f"{run_id}_audit",
        "event_index": 1,
        "event_type": "tool_executed",
        "actor": "tool_runtime",
        "related_call_id": call_id,
        "related_rule_ids": [],
        "related_data_refs": list(refs),
        "related_redaction_artifact_refs": [],
        "outcome": "simulated",
        "evidence_refs": [],
        "removed_field_labels": [],
        "rationale": "",
    }


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _row_by(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row[key] == value:
            return row
    raise AssertionError(f"missing row where {key}={value}")


if __name__ == "__main__":
    unittest.main()
