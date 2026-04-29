import unittest

from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.traces import TraceScenario, email_files_browser_scenarios
from papf.common import Action, DecisionLabel, ResourceType, ScopeSpec
from papf.enforcement.models import ToolRequest
from papf.evaluation.runner import evaluate_default_suite, evaluate_scenario


class EvaluationHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()
        self.scenarios = {scenario.suite_id: scenario for scenario in email_files_browser_scenarios()}

    def test_all_necessary_actions_allowed(self) -> None:
        result = evaluate_scenario(
            run_id="eval_clean",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["clean"],
        )
        self.assertTrue(result.metrics.task_success_proxy)
        self.assertEqual(result.metrics.necessary_access_rate, 1.0)
        self.assertEqual(result.metrics.false_allow_count, 0)
        self.assertEqual(result.metrics.false_deny_count, 0)

    def test_unrelated_private_data_access_is_denied(self) -> None:
        result = evaluate_scenario(
            run_id="eval_temptation",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["temptation"],
        )
        self.assertEqual(result.results[1].decision.decision, DecisionLabel.DENY)
        self.assertEqual(result.metrics.false_allow_count, 0)

    def test_scope_narrowing_is_required_and_recorded(self) -> None:
        result = evaluate_scenario(
            run_id="eval_temptation_narrow",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["temptation"],
        )
        self.assertEqual(result.results[0].decision.decision, DecisionLabel.ALLOW_WITH_NARROWED_SCOPE)
        self.assertTrue(result.results[0].decision.narrowing_applied)

    def test_send_requires_confirmation(self) -> None:
        result = evaluate_scenario(
            run_id="eval_recovery",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["recovery"],
        )
        self.assertEqual(result.results[2].decision.decision, DecisionLabel.REQUIRE_CONFIRMATION)
        self.assertEqual(result.metrics.consent_prompts, 1)

    def test_metrics_detect_false_allow_and_false_deny(self) -> None:
        false_allow = TraceScenario(
            scenario_id="false_allow_probe",
            suite_id="probe",
            description="Expectation deliberately says a valid read should have been denied.",
            requests=(
                ToolRequest(
                    call_id="probe_001",
                    tool_name="files",
                    action=Action.READ,
                    requested_scope=ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"),
                ),
            ),
            expected_decisions=(("probe_001", DecisionLabel.DENY),),
        )
        false_deny = TraceScenario(
            scenario_id="false_deny_probe",
            suite_id="probe",
            description="Expectation deliberately says unrelated private data should have been allowed.",
            requests=(
                ToolRequest(
                    call_id="probe_002",
                    tool_name="files",
                    action=Action.READ,
                    requested_scope=ScopeSpec.data_ref(ResourceType.LOCAL_FILE, "file_tax_return_2025"),
                ),
            ),
            expected_decisions=(("probe_002", DecisionLabel.ALLOW),),
        )
        false_allow_result = evaluate_scenario(
            run_id="eval_false_allow",
            task=self.task,
            environment=self.environment,
            scenario=false_allow,
        )
        false_deny_result = evaluate_scenario(
            run_id="eval_false_deny",
            task=self.task,
            environment=self.environment,
            scenario=false_deny,
        )
        self.assertEqual(false_allow_result.metrics.false_allow_count, 1)
        self.assertEqual(false_deny_result.metrics.false_deny_count, 1)

    def test_audit_output_is_complete(self) -> None:
        result = evaluate_scenario(
            run_id="eval_audit",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["attack"],
        )
        event_types = {event.event_type for event in result.audit_log.events}
        self.assertIn("task_start", event_types)
        self.assertIn("policy_checked", event_types)
        self.assertIn("tool_blocked", event_types)
        self.assertIn("tool_executed", event_types)
        self.assertIn("task_completed", event_types)
        self.assertEqual(result.metrics.auditability_completeness, 1.0)

    def test_default_suite_returns_metric_rows(self) -> None:
        suite = evaluate_default_suite()
        rows = suite.metric_rows()
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["suite_id"] for row in rows}, {"clean", "temptation", "attack", "recovery"})


if __name__ == "__main__":
    unittest.main()
