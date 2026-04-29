import unittest
from pathlib import Path

import yaml

from papf.benchmark.loader import load_benchmark_cases
from papf.common import DecisionLabel
from papf.evaluation.runner import evaluate_scenario


SEED_CASE_DIR = Path("benchmarks/papf_seed_cases")
REQUIRED_SUITES = {"clean", "temptation", "attack", "recovery"}
REQUIRED_ATTACK_LABELS = {
    "overbroad_access",
    "prompt_injection",
    "cross_tool_exfiltration",
    "redaction_required",
    "confirmation_gated_outbound",
    "recovery_after_denial",
}
REQUIRED_POLICY_OUTCOMES = {
    DecisionLabel.ALLOW,
    DecisionLabel.ALLOW_WITH_NARROWED_SCOPE,
    DecisionLabel.ALLOW_WITH_REDACTION,
    DecisionLabel.REQUIRE_CONFIRMATION,
    DecisionLabel.DENY,
}


class SeedCaseCoverageTests(unittest.TestCase):
    def test_seed_suite_covers_required_tools_labels_and_outcomes(self) -> None:
        cases = load_benchmark_cases(SEED_CASE_DIR)
        scenarios = [scenario for case in cases for scenario in case.scenarios]
        raw_traces = _raw_traces()

        self.assertGreaterEqual(len(scenarios), 12)
        self.assertEqual({scenario.suite_id for scenario in scenarios}, REQUIRED_SUITES)
        self.assertTrue(_all_data_objects_are_synthetic())

        tools = {
            request.tool_name
            for scenario in scenarios
            for request in scenario.requests
        }
        self.assertGreaterEqual(tools, {"email", "files", "browser"})

        attack_labels = {
            label
            for trace in raw_traces
            for label in trace.get("attack_labels", [])
        }
        self.assertGreaterEqual(attack_labels, REQUIRED_ATTACK_LABELS)

        expected_outcomes = {
            decision
            for scenario in scenarios
            for decision in scenario.expected_decision_map().values()
        }
        self.assertGreaterEqual(expected_outcomes, REQUIRED_POLICY_OUTCOMES)

    def test_cross_tool_exfiltration_redaction_and_confirmation_cases_are_explicit(self) -> None:
        cases = load_benchmark_cases(SEED_CASE_DIR)
        raw_traces = _raw_traces()

        cross_tool_traces = [
            trace
            for trace in raw_traces
            if "cross_tool_exfiltration" in trace.get("attack_labels", [])
        ]
        self.assertTrue(cross_tool_traces)
        for trace in cross_tool_traces:
            tools = {request["tool_name"] for request in trace["requests"]}
            self.assertGreaterEqual(len(tools), 2)

        redaction_decisions = [
            decision
            for case in cases
            for scenario in case.scenarios
            for decision in scenario.expected_decision_map().values()
            if decision == DecisionLabel.ALLOW_WITH_REDACTION
        ]
        self.assertTrue(redaction_decisions)

        confirmation_sends = [
            request
            for case in cases
            for scenario in case.scenarios
            for request in scenario.requests
            if request.action.value == "send"
            and scenario.expected_decision_map().get(request.call_id) == DecisionLabel.REQUIRE_CONFIRMATION
        ]
        self.assertTrue(confirmation_sends)

    def test_policy_outcomes_match_evaluator_for_all_loaded_seed_traces(self) -> None:
        for case in load_benchmark_cases(SEED_CASE_DIR):
            for scenario in case.scenarios:
                result = evaluate_scenario(
                    run_id=f"coverage_{scenario.scenario_id}",
                    task=case.task,
                    environment=case.environment,
                    scenario=scenario,
                )
                observed = {
                    enforcement.request.call_id: enforcement.decision.decision
                    for enforcement in result.results
                }
                self.assertEqual(observed, scenario.expected_decision_map())


def _raw_traces() -> list[dict]:
    traces = []
    for path in sorted(SEED_CASE_DIR.glob("*.yaml")):
        raw_case = yaml.safe_load(path.read_text(encoding="utf-8"))
        traces.extend(raw_case["traces"])
    return traces


def _all_data_objects_are_synthetic() -> bool:
    for path in sorted(SEED_CASE_DIR.glob("*.yaml")):
        raw_case = yaml.safe_load(path.read_text(encoding="utf-8"))
        if raw_case.get("synthetic") is not True:
            return False
        for data_object in raw_case["environment"]["data_objects"]:
            if data_object.get("synthetic") is not True:
                return False
    return True


if __name__ == "__main__":
    unittest.main()
