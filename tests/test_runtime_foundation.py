import unittest

from papf.benchmark.fixtures import email_files_fixture
from papf.benchmark.validators import validate_task_bundle
from papf.capabilities.compiler import compile_capabilities_from_policy
from papf.common import Action, DecisionLabel, ResourceType, ScopeSpec
from papf.enforcement.models import ToolRequest
from papf.enforcement.runtime import enforce_request
from papf.evaluation.metrics import score_trace
from papf.intent.models import TaskIntent


class RuntimeFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task, self.environment = email_files_fixture()
        self.intent = TaskIntent(
            task_id=self.task.task_id,
            task_summary="Draft a reimbursement reply from Alex's email and receipt.",
            user_goal=self.task.task_goal,
            requested_actions=(Action.READ, Action.DRAFT, Action.SEND),
            candidate_resource_types=(
                ResourceType.EMAIL_THREAD,
                ResourceType.ATTACHMENT,
                ResourceType.EMAIL_DRAFT,
            ),
            candidate_resource_refs=(
                "email_thread_alex_reimbursement",
                "file_receipt_042",
                "draft_reply_alex_reimbursement",
            ),
            expected_output_type=self.task.expected_output_type,
        )
        self.capabilities = compile_capabilities_from_policy(self.intent, self.task.policy_pack)

    def enforce(self, request: ToolRequest):
        return enforce_request(
            run_id="run_test",
            task_id=self.task.task_id,
            request=request,
            capabilities=self.capabilities,
            policy_pack=self.task.policy_pack,
        )

    def test_fixture_validates(self) -> None:
        self.assertEqual(validate_task_bundle(self.task, self.environment), [])

    def test_narrow_receipt_read_is_allowed(self) -> None:
        result = self.enforce(
            ToolRequest(
                call_id="call_001",
                tool_name="files",
                action=Action.READ,
                requested_scope=ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"),
            )
        )
        self.assertTrue(result.may_execute)
        self.assertEqual(result.decision.decision, DecisionLabel.ALLOW)

    def test_unrelated_private_file_read_is_denied(self) -> None:
        result = self.enforce(
            ToolRequest(
                call_id="call_002",
                tool_name="files",
                action=Action.READ,
                requested_scope=ScopeSpec.data_ref(ResourceType.LOCAL_FILE, "file_tax_return_2025"),
            )
        )
        self.assertFalse(result.may_execute)
        self.assertEqual(result.decision.decision, DecisionLabel.DENY)

    def test_broad_attachment_request_can_be_narrowed_to_allowed_ref(self) -> None:
        result = self.enforce(
            ToolRequest(
                call_id="call_003",
                tool_name="files",
                action=Action.READ,
                requested_scope=ScopeSpec(
                    resource_type=ResourceType.ATTACHMENT,
                    selector_type="directory",
                    selector_value="receipts/*",
                ),
                input_refs=("file_receipt_042",),
            )
        )
        self.assertTrue(result.may_execute)
        self.assertEqual(result.decision.decision, DecisionLabel.ALLOW_WITH_NARROWED_SCOPE)
        self.assertEqual(result.resolved_scope, ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"))

    def test_send_requires_confirmation(self) -> None:
        result = self.enforce(
            ToolRequest(
                call_id="call_004",
                tool_name="email",
                action=Action.SEND,
                requested_scope=ScopeSpec.data_ref(ResourceType.EMAIL_DRAFT, "draft_reply_alex_reimbursement"),
            )
        )
        self.assertFalse(result.may_execute)
        self.assertTrue(result.decision.confirmation_required)
        self.assertEqual(result.decision.decision, DecisionLabel.REQUIRE_CONFIRMATION)

    def test_metrics_score_fixed_trace(self) -> None:
        allowed = self.enforce(
            ToolRequest(
                call_id="call_005",
                tool_name="files",
                action=Action.READ,
                requested_scope=ScopeSpec.data_ref(ResourceType.ATTACHMENT, "file_receipt_042"),
            )
        )
        denied = self.enforce(
            ToolRequest(
                call_id="call_006",
                tool_name="files",
                action=Action.READ,
                requested_scope=ScopeSpec.data_ref(ResourceType.LOCAL_FILE, "file_tax_return_2025"),
            )
        )
        metrics = score_trace((allowed, denied), self.environment)
        self.assertEqual(metrics.total_calls, 2)
        self.assertEqual(metrics.executed_calls, 1)
        self.assertEqual(metrics.blocked_calls, 1)
        self.assertEqual(metrics.over_access_rate, 0.0)


if __name__ == "__main__":
    unittest.main()
