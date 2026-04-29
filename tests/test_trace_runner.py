import unittest

from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.traces import email_files_browser_scenarios, run_trace_scenario
from papf.common import DecisionLabel
from papf.evaluation.metrics import score_trace


class TraceRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()
        self.scenarios = {scenario.suite_id: scenario for scenario in email_files_browser_scenarios()}

    def test_all_expected_scenarios_exist(self) -> None:
        self.assertEqual(set(self.scenarios), {"clean", "temptation", "attack", "recovery"})

    def test_clean_trace_executes_without_blocks_or_prompts(self) -> None:
        results = run_trace_scenario(run_id="run_clean", task=self.task, scenario=self.scenarios["clean"])
        metrics = score_trace(results, self.environment)
        self.assertEqual(metrics.executed_calls, 4)
        self.assertEqual(metrics.blocked_calls, 0)
        self.assertEqual(metrics.consent_prompts, 0)
        self.assertEqual(metrics.over_access_rate, 0.0)

    def test_temptation_trace_denies_unrelated_private_file(self) -> None:
        results = run_trace_scenario(run_id="run_temptation", task=self.task, scenario=self.scenarios["temptation"])
        decisions = {result.request.call_id: result.decision.decision for result in results}
        self.assertEqual(decisions["call_tempt_001"], DecisionLabel.ALLOW_WITH_NARROWED_SCOPE)
        self.assertEqual(decisions["call_tempt_002"], DecisionLabel.DENY)
        self.assertEqual(decisions["call_tempt_003"], DecisionLabel.ALLOW)

    def test_attack_trace_blocks_untrusted_browse_and_upload(self) -> None:
        results = run_trace_scenario(run_id="run_attack", task=self.task, scenario=self.scenarios["attack"])
        decisions = {result.request.call_id: result.decision.decision for result in results}
        self.assertEqual(decisions["call_attack_001"], DecisionLabel.DENY)
        self.assertEqual(decisions["call_attack_002"], DecisionLabel.DENY)
        self.assertEqual(decisions["call_attack_003"], DecisionLabel.ALLOW)

    def test_recovery_trace_blocks_ambiguous_broad_request_then_allows_narrow_request(self) -> None:
        results = run_trace_scenario(run_id="run_recovery", task=self.task, scenario=self.scenarios["recovery"])
        decisions = {result.request.call_id: result.decision.decision for result in results}
        self.assertEqual(decisions["call_recovery_001"], DecisionLabel.DENY)
        self.assertEqual(decisions["call_recovery_002"], DecisionLabel.ALLOW)
        self.assertEqual(decisions["call_recovery_003"], DecisionLabel.REQUIRE_CONFIRMATION)


if __name__ == "__main__":
    unittest.main()
