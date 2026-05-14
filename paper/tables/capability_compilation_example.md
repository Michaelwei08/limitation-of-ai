# Capability Compilation Example

This table is a paper-facing synthetic example based on the reimbursement seed case and the PAPF redaction, confirmation, and audit semantics. It is illustrative of the implemented schema and policy model; it does not introduce new experimental numbers.

| User-facing step or risk | Compiled authority or policy rule | Plain-language implication |
| --- | --- | --- |
| Summarize Alex's reimbursement email | `read` on `email_thread_alex_reimbursement` | Allow only the named reimbursement thread, not the whole mailbox. |
| Pull the receipt total | `read` on `file_receipt_042` | Allow only the relevant receipt attachment, not the full files folder. |
| Check merchant policy page | `browse` on `webpage_merchant_reimbursement_policy` | Allow only the approved policy page. |
| Hide private fields before reuse | `allow_with_redaction` plus a `RedactionArtifact` for removed fields such as address or payment identifier | Show evidence that sensitive fields were removed before the summary or draft is reused. |
| Draft a reply | `draft` on `draft_reply_alex_reimbursement` | Allow a local draft artifact without external send. |
| Send the reply | `send` on `draft_reply_alex_reimbursement` with `confirm` consent | Require user confirmation before anything leaves the account. |
| Follow malicious webpage instruction | No allow rule for `webpage_prompt_injection_trap` or off-task `upload` actions | Deny instructions from an untrusted page when they exceed the user's task. |
| Read unrelated tax return | No allow rule for `file_tax_return_2025` | Deny unrelated dangerous private data. |
| Review what happened later | Audit events link task intent, decisions, data touches, redaction artifacts, denials, and confirmations | Preserve a readable trace without relying on the model to remember or explain itself after the fact. |
