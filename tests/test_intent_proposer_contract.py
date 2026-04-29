import unittest

from papf.benchmark.fixtures import email_files_fixture
from papf.intent.proposer import (
    DeterministicFakeIntentProposer,
    IntentProposal,
    compile_capabilities_from_proposal,
    validate_intent_proposal,
)


class IntentProposerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()
        self.raw_intent = {
            "task_id": self.task.task_id,
            "task_summary": "Draft a reimbursement reply from Alex's email and receipt.",
            "user_goal": self.task.task_goal,
            "requested_actions": ["read", "draft", "send"],
            "candidate_resource_types": ["email_thread", "attachment", "email_draft"],
            "candidate_resource_refs": [
                "email_thread_alex_reimbursement",
                "file_receipt_042",
                "draft_reply_alex_reimbursement",
            ],
            "expected_output_type": self.task.expected_output_type,
            "metadata": {"source": "unit_test"},
        }

    def test_deterministic_fake_proposer_returns_candidate_intent(self) -> None:
        proposer = DeterministicFakeIntentProposer("proposal_valid", self.raw_intent)

        proposal = proposer.propose(self.task.user_request)
        validation = validate_intent_proposal(proposal, known_data_refs=self.environment.data_ids())

        self.assertTrue(validation.is_valid)
        self.assertIsNotNone(validation.accepted_intent)
        self.assertEqual(validation.proposer_mode, "deterministic_fake")
        self.assertEqual(validation.require_intent().task_id, self.task.task_id)

    def test_validated_proposal_can_enter_existing_compiler(self) -> None:
        proposal = IntentProposal("proposal_valid", "deterministic_fake", self.raw_intent)

        bundle = compile_capabilities_from_proposal(
            proposal,
            self.task.policy_pack,
            known_data_refs=self.environment.data_ids(),
        )

        active_ids = {capability.capability_id for capability in bundle.active_capabilities}
        self.assertIn("cap_rule_read_receipt_file_receipt_042", active_ids)

    def test_invalid_action_label_cannot_mint_capabilities(self) -> None:
        raw = dict(self.raw_intent, requested_actions=["read", "approve_everything"])
        proposal = IntentProposal("proposal_bad_action", "deterministic_fake", raw)

        validation = validate_intent_proposal(proposal, known_data_refs=self.environment.data_ids())

        self.assertFalse(validation.is_valid)
        self.assertIsNone(validation.accepted_intent)
        self.assertTrue(any(issue.code == "SCHEMA_REQUESTED_ACTIONS" for issue in validation.issues))
        with self.assertRaisesRegex(ValueError, "invalid IntentProposal proposal_bad_action"):
            compile_capabilities_from_proposal(
                proposal,
                self.task.policy_pack,
                known_data_refs=self.environment.data_ids(),
            )

    def test_unknown_candidate_ref_cannot_mint_capabilities(self) -> None:
        raw = dict(self.raw_intent, candidate_resource_refs=("file_receipt_042", "file_does_not_exist"))
        proposal = IntentProposal("proposal_unknown_ref", "deterministic_fake", raw)

        validation = validate_intent_proposal(proposal, known_data_refs=self.environment.data_ids())

        self.assertFalse(validation.is_valid)
        self.assertTrue(any(issue.code == "UNKNOWN_CANDIDATE_REF" for issue in validation.issues))
        with self.assertRaisesRegex(ValueError, "UNKNOWN_CANDIDATE_REF"):
            compile_capabilities_from_proposal(
                proposal,
                self.task.policy_pack,
                known_data_refs=self.environment.data_ids(),
            )

    def test_mismatched_scope_constraint_cannot_mint_capabilities(self) -> None:
        raw = dict(
            self.raw_intent,
            proposed_scope_constraints=[
                {
                    "resource_type": "local_file",
                    "selector_type": "data_id",
                    "selector_value": "file_tax_return_2025",
                }
            ],
        )
        proposal = IntentProposal("proposal_scope_mismatch", "deterministic_fake", raw)

        validation = validate_intent_proposal(proposal, known_data_refs=self.environment.data_ids())

        self.assertFalse(validation.is_valid)
        self.assertTrue(any(issue.code == "SCOPE_RESOURCE_MISMATCH" for issue in validation.issues))
        with self.assertRaisesRegex(ValueError, "SCOPE_RESOURCE_MISMATCH"):
            compile_capabilities_from_proposal(
                proposal,
                self.task.policy_pack,
                known_data_refs=self.environment.data_ids(),
            )


if __name__ == "__main__":
    unittest.main()
