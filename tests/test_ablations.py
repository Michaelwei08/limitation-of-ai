import unittest

from papf.ablation import AblationMode, evaluate_ablation_scenario
from papf.benchmark.loader import load_benchmark_cases


class AblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = next(
            case for case in load_benchmark_cases("benchmarks/papf_seed_cases") if case.case_id == "email_files_browser_001"
        )

    def scenario(self, scenario_id: str):
        return next(scenario for scenario in self.case.scenarios if scenario.scenario_id == scenario_id)

    def test_no_scope_narrowing_converts_narrowed_allow_to_false_deny(self) -> None:
        result = evaluate_ablation_scenario(
            run_id="run_no_scope",
            task=self.case.task,
            environment=self.case.environment,
            scenario=self.scenario("trace_temptation"),
            mode=AblationMode.NO_SCOPE_NARROWING,
        )

        self.assertEqual(result.metrics.false_deny_count, 1)
        self.assertIn("ablation:ablation_no_scope_narrowing", result.results[0].decision.matched_rule_ids)

    def test_no_confirmation_gating_creates_false_allow_for_send(self) -> None:
        result = evaluate_ablation_scenario(
            run_id="run_no_confirm",
            task=self.case.task,
            environment=self.case.environment,
            scenario=self.scenario("trace_recovery"),
            mode=AblationMode.NO_CONFIRMATION_GATING,
        )

        self.assertEqual(result.metrics.false_allow_count, 1)
        self.assertEqual(result.metrics.consent_prompts, 0)

    def test_no_recovery_scoring_removes_safe_partial_credit(self) -> None:
        result = evaluate_ablation_scenario(
            run_id="run_no_recovery",
            task=self.case.task,
            environment=self.case.environment,
            scenario=self.scenario("trace_recovery"),
            mode=AblationMode.NO_SAFER_ALTERNATIVE_RECOVERY,
        )

        self.assertEqual(result.metrics.recovery_quality, 0.0)
        self.assertFalse(result.metrics.safe_partial_success)

    def test_no_audit_completeness_validation_scores_zero_auditability(self) -> None:
        result = evaluate_ablation_scenario(
            run_id="run_no_audit",
            task=self.case.task,
            environment=self.case.environment,
            scenario=self.scenario("trace_clean"),
            mode=AblationMode.NO_AUDIT_COMPLETENESS_VALIDATION,
        )

        self.assertEqual(result.metrics.auditability_completeness, 0.0)
        self.assertEqual(result.audit_log.events, ())

    def test_no_redaction_evidence_records_unredacted_disclosure(self) -> None:
        redaction_case = next(
            case for case in load_benchmark_cases("benchmarks/papf_seed_cases") if case.case_id == "email_files_browser_002"
        )
        scenario = next(item for item in redaction_case.scenarios if item.scenario_id == "trace_redaction_clean")

        result = evaluate_ablation_scenario(
            run_id="run_no_redaction",
            task=redaction_case.task,
            environment=redaction_case.environment,
            scenario=scenario,
            mode=AblationMode.NO_REDACTION_EVIDENCE,
        )

        self.assertGreaterEqual(result.metrics.unredacted_disclosure_count, 1)
        self.assertIn("ablation:ablation_no_redaction_evidence", result.results[0].decision.matched_rule_ids)


if __name__ == "__main__":
    unittest.main()
