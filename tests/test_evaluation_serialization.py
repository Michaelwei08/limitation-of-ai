import csv
import json
import unittest
from pathlib import Path

from papf.evaluation.serialization import METRIC_SCHEMA_VERSION, write_default_evaluation_run


class EvaluationSerializationTests(unittest.TestCase):
    def test_default_run_writes_expected_files(self) -> None:
        written = write_default_evaluation_run(
            Path("experiments/runs/test_serialization_default"),
            timestamp="2026-04-27T00:00:00+00:00",
            repo_root=Path.cwd(),
        )

        self.assertTrue(written.metadata_path.exists())
        self.assertTrue(written.metrics_jsonl_path.exists())
        self.assertTrue(written.metrics_csv_path.exists())
        self.assertTrue(written.audit_jsonl_path.exists())

        metadata = json.loads(written.metadata_path.read_text(encoding="utf-8"))
        self.assertEqual(metadata["timestamp"], "2026-04-27T00:00:00+00:00")
        self.assertEqual(metadata["metric_schema_version"], METRIC_SCHEMA_VERSION)
        self.assertEqual(set(metadata["suite_ids"]), {"clean", "temptation", "attack", "recovery"})
        self.assertIn("git_status_summary", metadata)

    def test_metric_jsonl_and_csv_have_same_rows(self) -> None:
        written = write_default_evaluation_run(
            Path("experiments/runs/test_serialization_rows"),
            timestamp="2026-04-27T00:00:00+00:00",
        )
        jsonl_rows = [
            json.loads(line)
            for line in written.metrics_jsonl_path.read_text(encoding="utf-8").splitlines()
        ]
        with written.metrics_csv_path.open(encoding="utf-8", newline="") as handle:
            csv_rows = list(csv.DictReader(handle))

        self.assertEqual(len(jsonl_rows), 4)
        self.assertEqual(len(csv_rows), 4)
        self.assertEqual({row["suite_id"] for row in jsonl_rows}, {"clean", "temptation", "attack", "recovery"})

    def test_audit_summary_excludes_raw_payload_fields(self) -> None:
        written = write_default_evaluation_run(
            Path("experiments/runs/test_serialization_audit"),
            timestamp="2026-04-27T00:00:00+00:00",
        )
        audit_rows = [
            json.loads(line)
            for line in written.audit_jsonl_path.read_text(encoding="utf-8").splitlines()
        ]

        self.assertGreater(len(audit_rows), 0)
        forbidden = {"raw_payload", "content", "body", "secret", "token"}
        self.assertTrue(all(forbidden.isdisjoint(row.keys()) for row in audit_rows))

    def test_output_dir_rejects_file_path(self) -> None:
        bad_path = Path("experiments/runs/test_serialization_not_a_dir.txt")
        bad_path.parent.mkdir(parents=True, exist_ok=True)
        bad_path.write_text("x", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "output_dir must be a directory"):
            write_default_evaluation_run(bad_path)


if __name__ == "__main__":
    unittest.main()
