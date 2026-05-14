import unittest

from papf.baselines import (
    BaselineMode,
    DEFAULT_PROMPT_ONLY_ADVISORY,
    evaluate_baseline_scenario,
    evaluate_broad_access_scenario,
    evaluate_prompt_only_scenario,
)
from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.traces import TraceScenario, email_files_browser_scenarios
from papf.common import Action, ResourceType, ScopeSpec
from papf.enforcement.models import ToolRequest
from papf.evaluation.runner import evaluate_scenario


class BaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()
        self.scenarios = {scenario.suite_id: scenario for scenario in email_files_browser_scenarios()}

    def test_broad_access_allows_private_file_that_papf_blocks(self) -> None:
        papf_result = evaluate_scenario(
            run_id="papf_temptation",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["temptation"],
        )
        broad_result = evaluate_broad_access_scenario(
            run_id="broad_temptation",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["temptation"],
        )

        self.assertEqual(papf_result.metrics.false_allow_count, 0)
        self.assertEqual(papf_result.metrics.over_access_rate, 0.0)
        self.assertEqual(broad_result.metrics.false_allow_count, 1)
        self.assertGreater(broad_result.metrics.over_access_rate, 0.0)
        self.assertTrue(all(result.may_execute for result in broad_result.results))

    def test_prompt_only_advisory_does_not_enforce_attack_trace(self) -> None:
        papf_result = evaluate_scenario(
            run_id="papf_attack",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["attack"],
        )
        prompt_result = evaluate_prompt_only_scenario(
            run_id="prompt_attack",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["attack"],
        )

        self.assertEqual(papf_result.metrics.false_allow_count, 0)
        self.assertEqual(prompt_result.metrics.false_allow_count, 2)
        self.assertGreater(prompt_result.metrics.over_access_rate, 0.0)
        self.assertIn("PROMPT_ONLY_ADVISORY_NOT_ENFORCED", prompt_result.results[0].decision.decision_reason)
        self.assertIn(DEFAULT_PROMPT_ONLY_ADVISORY, prompt_result.results[0].decision.decision_reason)

    def test_broad_access_records_observed_data_touches_for_broad_requests(self) -> None:
        result = evaluate_broad_access_scenario(
            run_id="broad_recovery",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["recovery"],
        )
        executed_events = [
            event
            for event in result.audit_log.events
            if event.event_type == "tool_executed" and event.related_call_id == "call_recovery_001"
        ]

        self.assertEqual(len(executed_events), 1)
        self.assertEqual(
            executed_events[0].related_data_refs,
            ("file_receipt_042", "file_tax_return_2025"),
        )
        self.assertEqual(result.metrics.false_allow_count, 2)
        self.assertGreater(result.metrics.over_access_rate, 0.0)

    def test_baselines_consume_same_trace_records_as_papf(self) -> None:
        scenario = self.scenarios["clean"]
        papf_result = evaluate_scenario(
            run_id="papf_clean",
            task=self.task,
            environment=self.environment,
            scenario=scenario,
        )
        broad_result = evaluate_broad_access_scenario(
            run_id="broad_clean",
            task=self.task,
            environment=self.environment,
            scenario=scenario,
        )
        prompt_result = evaluate_prompt_only_scenario(
            run_id="prompt_clean",
            task=self.task,
            environment=self.environment,
            scenario=scenario,
        )

        self.assertEqual([result.request.call_id for result in broad_result.results], [result.request.call_id for result in papf_result.results])
        self.assertEqual([result.request.call_id for result in prompt_result.results], [result.request.call_id for result in papf_result.results])
        self.assertTrue(broad_result.metrics.task_success_proxy)
        self.assertTrue(prompt_result.metrics.task_success_proxy)

    def test_broad_baseline_fails_clearly_without_observed_refs_for_broad_request(self) -> None:
        scenario = TraceScenario(
            scenario_id="missing_refs",
            suite_id="malformed",
            description="Broad synthetic request omits observed touched refs.",
            requests=(
                ToolRequest(
                    call_id="missing_refs_001",
                    tool_name="files",
                    action=Action.READ,
                    requested_scope=ScopeSpec(ResourceType.ATTACHMENT, "directory", "receipts/*"),
                ),
            ),
        )

        with self.assertRaisesRegex(ValueError, "must list observed input_refs"):
            evaluate_broad_access_scenario(
                run_id="broad_missing_refs",
                task=self.task,
                environment=self.environment,
                scenario=scenario,
            )

    def test_tool_scope_baseline_blocks_upload_but_allows_untrusted_page(self) -> None:
        result = evaluate_baseline_scenario(
            run_id="run_tool_scope",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["attack"],
            mode=BaselineMode.TOOL_SCOPE,
        )

        by_call = {item.request.call_id: item for item in result.results}
        self.assertTrue(by_call["call_attack_001"].may_execute)
        self.assertFalse(by_call["call_attack_002"].may_execute)
        self.assertGreater(result.metrics.false_allow_count, 0)
        self.assertIn("baseline:tool_scope", by_call["call_attack_001"].decision.matched_rule_ids)

    def test_static_policy_baseline_blocks_broad_recovery_request_without_narrowing(self) -> None:
        result = evaluate_baseline_scenario(
            run_id="run_static_policy",
            task=self.task,
            environment=self.environment,
            scenario=self.scenarios["temptation"],
            mode=BaselineMode.STATIC_POLICY,
        )

        first = result.results[0]
        self.assertFalse(first.may_execute)
        self.assertEqual(result.metrics.false_deny_count, 1)
        self.assertIn("baseline:static_policy", first.decision.matched_rule_ids)


if __name__ == "__main__":
    unittest.main()
