import json
import unittest
from pathlib import Path

import yaml

from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.loader import BenchmarkLoaderError, load_benchmark_case, load_benchmark_cases
from papf.benchmark.validators import validate_task_bundle
from papf.common import Action, DecisionLabel, ResourceType
from papf.evaluation.runner import evaluate_scenario


SEED_CASE = Path("benchmarks/papf_seed_cases/email_files_browser.yaml")
TEMP_CASE = Path("tests/.tmp_benchmark_loader_case.json")


class BenchmarkLoaderTests(unittest.TestCase):
    def test_loads_seed_case_from_yaml_directory(self) -> None:
        cases = load_benchmark_cases(SEED_CASE.parent)

        self.assertEqual(len(cases), 1)
        case = cases[0]
        self.assertEqual(case.task.task_id, "email_files_001")
        self.assertEqual(case.environment.environment_id, "env_email_files_001")
        self.assertEqual({scenario.suite_id for scenario in case.scenarios}, {"clean", "temptation", "attack", "recovery"})
        self.assertEqual(case.task.safer_alternatives[0].alternative_id, "alt_read_receipt_by_id")
        self.assertEqual(validate_task_bundle(case.task, case.environment), [])

    def test_seed_case_preserves_hard_coded_smoke_fixture_shape(self) -> None:
        loaded = load_benchmark_case(SEED_CASE)
        fixture_task, fixture_environment = email_files_fixture()

        self.assertEqual(loaded.task.environment_refs, fixture_task.environment_refs)
        self.assertEqual(loaded.environment.data_ids(), fixture_environment.data_ids())
        self.assertEqual(len(loaded.task.policy_pack.rules), len(fixture_task.policy_pack.rules))
        self.assertEqual(loaded.scenarios[0].requests[0].action, Action.READ)
        self.assertEqual(loaded.scenarios[0].requests[0].requested_scope.resource_type, ResourceType.EMAIL_THREAD)

    def test_loaded_trace_runs_through_evaluation_harness(self) -> None:
        loaded = load_benchmark_case(SEED_CASE)

        result = evaluate_scenario(
            run_id="loaded_clean",
            task=loaded.task,
            environment=loaded.environment,
            scenario=loaded.scenarios[0],
        )

        self.assertTrue(result.metrics.task_success_proxy)
        self.assertEqual(result.metrics.false_allow_count, 0)

    def test_loads_case_from_json(self) -> None:
        case_data = _seed_case_data()
        loaded = _load_temp_json(case_data)

        self.assertEqual(loaded.task.task_id, "email_files_001")
        self.assertEqual(loaded.scenarios[-1].expected_decision_map()["call_recovery_003"], DecisionLabel.REQUIRE_CONFIRMATION)

    def test_rejects_missing_policy_data_ref_with_clear_error(self) -> None:
        case_data = _seed_case_data()
        case_data["policy"]["rules"][0]["allow_refs"] = ["missing_email_thread"]

        with self.assertRaisesRegex(
            BenchmarkLoaderError,
            "missing data objects: missing_email_thread",
        ):
            _load_temp_json(case_data)

    def test_rejects_missing_trace_data_ref_with_clear_error(self) -> None:
        case_data = _seed_case_data()
        case_data["traces"][0]["requests"][0]["scope"]["selector_value"] = "missing_email_thread"

        with self.assertRaisesRegex(
            BenchmarkLoaderError,
            "scope.selector_value references missing data object: missing_email_thread",
        ):
            _load_temp_json(case_data)

    def test_rejects_invalid_enum_label_with_clear_error(self) -> None:
        case_data = _seed_case_data()
        case_data["policy"]["rules"][0]["action"] = "read_email"

        with self.assertRaisesRegex(
            BenchmarkLoaderError,
            "policy.rules\\[0\\].action has invalid enum label 'read_email'",
        ):
            _load_temp_json(case_data)

    def test_rejects_non_synthetic_case(self) -> None:
        case_data = _seed_case_data()
        case_data["synthetic"] = False

        with self.assertRaisesRegex(BenchmarkLoaderError, "synthetic must be true"):
            _load_temp_json(case_data)

    def test_rejects_non_synthetic_data_object(self) -> None:
        case_data = _seed_case_data()
        case_data["environment"]["data_objects"][0]["synthetic"] = False

        with self.assertRaisesRegex(BenchmarkLoaderError, "environment.data_objects\\[0\\].synthetic must be true"):
            _load_temp_json(case_data)


def _seed_case_data() -> dict:
    return yaml.safe_load(SEED_CASE.read_text(encoding="utf-8"))


def _load_temp_json(case_data: dict):
    try:
        TEMP_CASE.write_text(json.dumps(case_data), encoding="utf-8")
        return load_benchmark_case(TEMP_CASE)
    finally:
        if TEMP_CASE.exists():
            TEMP_CASE.unlink()


if __name__ == "__main__":
    unittest.main()
