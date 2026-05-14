# PAPF Prompt Design Variants

Status: design artifact for a future non-expert study. This table reports no
participant results.

All variants show the same underlying task-scoped enforcement decision. They
differ only in how much information is visible, how privacy risk is framed,
whether details are progressively disclosed, and whether the prompt previews
the audit record.

| Variant | Task goal | Requested tool access | Data touched | Data sent externally | Redactions applied | Confirmation reason | Design dimension |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Minimal prompt | Yes, one line. | Yes, summarized. | Yes, main records only. | Yes, if outbound sharing is requested. | Only if redaction is part of the decision. | Yes, one sentence. | Low text and low interruption. |
| Detailed prompt | Yes. | Yes, listed by action. | Yes, listed by named data object. | Yes, with recipient or destination. | Yes, with hidden field names. | Yes, with the risky action named. | Complete visible scope. |
| Risk-highlighted prompt | Yes. | Yes, listed by action. | Yes, including blocked sensitive data when relevant. | Yes, emphasized as data leaving the account. | Yes, emphasized before approval. | Yes, tied to privacy risk. | Salience of privacy consequences. |
| Prompt with expandable explanation | Yes, visible by default. | Yes, visible by default. | Collapsed until opened. | Yes, visible when outbound sharing is requested. | Collapsed until opened, unless redaction is the main issue. | Collapsed until opened. | Progressive disclosure. |
| Prompt with audit-log preview | Yes. | Yes, as planned audit entries. | Yes, as planned data-touch entries. | Yes, as planned outbound entries. | Yes, as planned redaction entries. | Yes, as planned confirmation entries. | Accountability before approval. |

Concrete matched examples are in
`docs/permission_prompt_examples.md`, using the US-03 redacted contractor reply
scenario. The planned protocol in `docs/user_study_protocol.md` treats these
variants as either pilot materials or a pre-specified prompt-format factor
nested inside the task-scoped condition.
