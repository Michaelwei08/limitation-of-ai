import unittest
from dataclasses import replace

from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.models import DataObject, EnvironmentBundle
from papf.benchmark.traces import TraceScenario
from papf.capabilities.models import Capability, CapabilityBundle
from papf.common import Action, ConsentLevel, DecisionLabel, ResourceType, ScopeSpec
from papf.enforcement.models import ToolRequest
from papf.policy.models import PolicyPack, PolicyRule
from papf.policy.validators import (
    require_valid_capability_bundle,
    require_valid_policy_pack,
    validate_capability_bundle,
    validate_environment,
    validate_policy_pack,
    validate_trace_scenario,
)


class PolicyValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()

    def test_valid_fixture_policy_has_no_errors(self) -> None:
        self.assertEqual(validate_policy_pack(self.task.policy_pack, self.environment), [])
        self.assertEqual(validate_environment(self.environment), [])

    def test_rejects_duplicate_rule_ids(self) -> None:
        rule = self.task.policy_pack.rules[0]
        policy = replace(self.task.policy_pack, rules=(rule, rule))

        errors = validate_policy_pack(policy, self.environment)

        self.assertIn("duplicate policy rule_id: rule_read_reimbursement_thread", errors)

    def test_rejects_duplicate_data_ids(self) -> None:
        obj = self.environment.data_objects[0]
        environment = replace(self.environment, data_objects=(obj, obj))

        errors = validate_environment(environment)

        self.assertIn("duplicate data_id: email_thread_alex_reimbursement", errors)

    def test_rejects_duplicate_call_ids(self) -> None:
        request = ToolRequest(
            call_id="call_duplicate",
            tool_name="files",
            action=Action.READ,
            requested_scope=ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"),
        )
        scenario = TraceScenario(
            scenario_id="trace_duplicate_calls",
            suite_id="validation",
            description="Duplicate calls should be rejected.",
            requests=(request, request),
        )

        errors = validate_trace_scenario(scenario)

        self.assertIn("duplicate call_id in scenario trace_duplicate_calls: call_duplicate", errors)

    def test_rejects_invalid_expected_decision_labels(self) -> None:
        request = ToolRequest(
            call_id="call_001",
            tool_name="files",
            action=Action.READ,
            requested_scope=ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"),
        )
        scenario = TraceScenario(
            scenario_id="trace_bad_expected_decision",
            suite_id="validation",
            description="Expected decisions must use known labels and known call ids.",
            requests=(request,),
            expected_decisions=(("call_001", "approve"), ("call_missing", DecisionLabel.DENY)),
        )

        errors = validate_trace_scenario(scenario)

        self.assertTrue(any("decision has invalid label 'approve'" in error for error in errors))
        self.assertIn(
            "scenario trace_bad_expected_decision expected_decisions[1] references missing trace request: call_missing",
            errors,
        )

    def test_rejects_duplicate_capability_ids_and_broad_scopes(self) -> None:
        capability = Capability(
            capability_id="cap_duplicate",
            action=Action.READ,
            scope=ScopeSpec(ResourceType.ATTACHMENT, "directory", "receipts/*"),
            purpose_binding="read_receipt",
            consent_level=ConsentLevel.NONE,
        )
        bundle = CapabilityBundle("task_001", active_capabilities=(capability, capability))

        errors = validate_capability_bundle(bundle)

        self.assertIn("duplicate capability_id: cap_duplicate", errors)
        self.assertIn("capability cap_duplicate uses broad scope; capabilities must be narrow", errors)

    def test_rejects_invalid_consent_and_decision_labels(self) -> None:
        bad_rule = PolicyRule(
            rule_id="rule_bad_labels",
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            resource_type=ResourceType.ATTACHMENT,
            action=Action.READ,
            effect="approve",
            consent_level="silent",
            allow_refs=("file_receipt_042",),
            purpose_binding="read_receipt",
            rationale_code="BAD_LABELS",
        )
        policy = replace(self.task.policy_pack, rules=(bad_rule,))

        errors = validate_policy_pack(policy, self.environment)

        self.assertTrue(any("effect has invalid label 'approve'" in error for error in errors))
        self.assertTrue(any("consent_level has invalid label 'silent'" in error for error in errors))

    def test_detects_allowing_dangerous_unrelated_data_without_confirmation(self) -> None:
        unsafe_rule = PolicyRule(
            rule_id="rule_read_tax_return",
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            resource_type=ResourceType.LOCAL_FILE,
            action=Action.READ,
            effect=DecisionLabel.ALLOW,
            consent_level=ConsentLevel.NONE,
            allow_refs=("file_tax_return_2025",),
            purpose_binding="inspect_unrelated_tax_return",
            rationale_code="UNSAFE",
        )
        policy = replace(self.task.policy_pack, rules=(unsafe_rule,))

        errors = validate_policy_pack(policy, self.environment)

        self.assertIn(
            "policy rule rule_read_tax_return allows dangerous unrelated data "
            "file_tax_return_2025 without confirmation",
            errors,
        )

    def test_allows_dangerous_unrelated_data_only_with_confirmation(self) -> None:
        confirmed_rule = PolicyRule(
            rule_id="rule_confirm_tax_return",
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            resource_type=ResourceType.LOCAL_FILE,
            action=Action.READ,
            effect=DecisionLabel.REQUIRE_CONFIRMATION,
            consent_level=ConsentLevel.HIGH_RISK_CONFIRM,
            allow_refs=("file_tax_return_2025",),
            purpose_binding="confirmed_unrelated_tax_return_access",
            rationale_code="HIGH_RISK_CONFIRMATION_REQUIRED",
        )
        policy = replace(self.task.policy_pack, rules=(confirmed_rule,))

        self.assertEqual(validate_policy_pack(policy, self.environment), [])

    def test_rejects_rules_that_reference_missing_environment_objects(self) -> None:
        missing_ref_rule = PolicyRule(
            rule_id="rule_missing_ref",
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            resource_type=ResourceType.EMAIL_THREAD,
            action=Action.READ,
            effect=DecisionLabel.ALLOW,
            consent_level=ConsentLevel.NONE,
            allow_refs=("email_thread_missing",),
            purpose_binding="read_missing_thread",
            rationale_code="MISSING_REF",
        )
        policy = replace(self.task.policy_pack, rules=(missing_ref_rule,))

        errors = validate_policy_pack(policy, self.environment)

        self.assertIn("policy rule rule_missing_ref references missing data objects: email_thread_missing", errors)

    def test_rejects_rules_with_resource_type_mismatches(self) -> None:
        mismatched_rule = PolicyRule(
            rule_id="rule_mismatched_ref",
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            resource_type=ResourceType.EMAIL_THREAD,
            action=Action.READ,
            effect=DecisionLabel.ALLOW,
            consent_level=ConsentLevel.NONE,
            allow_refs=("file_receipt_042",),
            purpose_binding="read_receipt_as_thread",
            rationale_code="RESOURCE_MISMATCH",
        )
        policy = replace(self.task.policy_pack, rules=(mismatched_rule,))

        errors = validate_policy_pack(policy, self.environment)

        self.assertIn(
            "policy rule rule_mismatched_ref references file_receipt_042 with resource_type attachment, not email_thread",
            errors,
        )

    def test_require_helpers_fail_closed_on_invalid_policy_and_capabilities(self) -> None:
        unsafe_policy = PolicyPack(
            policy_pack_id=self.task.policy_pack.policy_pack_id,
            rules=(replace(self.task.policy_pack.rules[0], rule_id=""),),
        )
        broad_capability = Capability(
            capability_id="cap_broad",
            action=Action.READ,
            scope=ScopeSpec(ResourceType.ATTACHMENT, "directory", "receipts/*"),
            purpose_binding="read_receipts",
            consent_level=ConsentLevel.NONE,
        )

        with self.assertRaisesRegex(ValueError, "invalid PolicyPack"):
            require_valid_policy_pack(unsafe_policy)
        with self.assertRaisesRegex(ValueError, "invalid CapabilityBundle"):
            require_valid_capability_bundle(
                CapabilityBundle("task_001", active_capabilities=(broad_capability,))
            )

    def test_rejects_invalid_data_labels(self) -> None:
        bad_object = DataObject(
            data_id="file_bad",
            resource_type=ResourceType.LOCAL_FILE,
            relevance="maybe_relevant",
            sensitivity="secret",
            trust="unknown",
        )
        environment = EnvironmentBundle("env_bad", (bad_object,))

        errors = validate_environment(environment)

        self.assertIn("file_bad has invalid relevance label: maybe_relevant", errors)
        self.assertIn("file_bad has invalid sensitivity label: secret", errors)
        self.assertIn("file_bad has invalid trust label: unknown", errors)


if __name__ == "__main__":
    unittest.main()
