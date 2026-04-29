import json
import unittest
from pathlib import Path

from papf.cli import ExperimentConfigError, run_experiment_config


class ExperimentRunnerTests(unittest.TestCase):
    def test_small_run_writes_expected_artifacts(self) -> None:
        written = run_experiment_config(
            Path("experiments/configs/smoke_email_files_browser.json"),
            timestamp="2026-04-29T00:00:00+00:00",
            repo_root=Path.cwd(),
        )

        run_dir = written.serialized_run.output_dir
        self.assertEqual(written.result_count, 3)
        self.assertTrue((run_dir / "metadata.json").exists())
        self.assertTrue((run_dir / "metrics.jsonl").exists())
        self.assertTrue((run_dir / "metrics.csv").exists())
        self.assertTrue((run_dir / "decisions.jsonl").exists())
        self.assertTrue((run_dir / "audit_summaries.jsonl").exists())
        self.assertTrue((run_dir / "config_snapshot.json").exists())

        metric_rows = [
            json.loads(line)
            for line in (run_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(len(metric_rows), 3)
        self.assertEqual({row["suite_id"] for row in metric_rows}, {"clean"})
        self.assertEqual(
            {row["run_id"].split("_email_files_browser_001_")[0] for row in metric_rows},
            {
                "smoke_email_files_browser_papf",
                "smoke_email_files_browser_broad_access",
                "smoke_email_files_browser_prompt_only",
            },
        )

        decision_rows = [
            json.loads(line)
            for line in (run_dir / "decisions.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertGreater(len(decision_rows), 0)
        self.assertTrue({"decision", "call_id", "policy_decision_id"}.issubset(decision_rows[0]))

        snapshot = json.loads((run_dir / "config_snapshot.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["config"]["config_id"], "smoke_email_files_browser")
        self.assertEqual(snapshot["result_count"], 3)

    def test_missing_case_reference_fails_clearly(self) -> None:
        config_path = Path("experiments/configs/test_experiment_runner_missing_case.json")
        try:
            config_path.write_text(
                json.dumps(
                    {
                        "config_id": "test_experiment_runner_missing_case",
                        "benchmark_path": "benchmarks/papf_seed_cases",
                        "case_ids": ["missing_case"],
                        "modes": ["papf"],
                        "output_dir": "experiments/runs/test_experiment_runner_missing_case",
                        "suite_ids": ["clean"],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ExperimentConfigError, "missing case ids: missing_case"):
                run_experiment_config(config_path, timestamp="2026-04-29T00:00:00+00:00", repo_root=Path.cwd())
        finally:
            config_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
