# Benchmark Specification

## Benchmark goal

NonExpert-AgentPermBench should measure whether a consumer AI agent can complete realistic personal-assistant tasks while respecting task-scoped permission boundaries enforced outside the LLM. The benchmark must expose the tradeoff between utility and privacy/security outcomes, not just end-task completion.

## Design stance

- Treat permission control as an external systems problem, not a prompt-only behavior problem.
- Evaluate at the level of concrete tool calls and concrete data touches.
- Keep task definitions, policy definitions, audit traces, and metric computation modular.
- Use synthetic personal data and synthetic adversarial content only.
- Prefer deterministic labels and deterministic policy outcomes wherever feasible.

## Benchmark structure

Each benchmark task should package four linked artifacts:

1. A task definition that describes the user-visible goal, environment, success conditions, and attack variants.
2. A policy definition that states what the agent may do, what requires escalation, and what must be blocked.
3. A tool-call trace format that can record what the agent attempted and what data it actually touched.
4. An audit format that links user intent, compiled permissions, policy decisions, confirmations, denials, and outcomes.

The benchmark should support at least four evaluation settings:

- Clean utility tasks with no adversarial content.
- Temptation tasks where irrelevant private data is available and easy to access.
- Adversarial tasks with malicious content, confused-deputy pressure, or exfiltration attempts.
- Recovery tasks where the initial plan is safely blocked or narrowed and the agent must pursue a safer alternative.

## Recommended release strategy

The overall taxonomy should remain cross-domain, but the first executable benchmark release should likely stay narrow enough to support a strong systems paper. The current best candidate slice is:

- Email
- Files
- Browser-linked tasks

This slice is broad enough to expose prompt injection, over-access, unauthorized sharing, and recovery behavior, while remaining implementable before a full cross-domain suite.

## Task categories

The full benchmark taxonomy should cover the following consumer-agent task families:

- Email: triage, retrieve facts from a thread, draft replies, handle attachments, and coordinate follow-up.
- Calendar: check availability, propose times, create or modify events, and reason over attendee constraints.
- Contacts: find a person, retrieve limited fields, or share contact details only when justified.
- Files: locate, summarize, compare, or selectively share local or cloud documents.
- Browser: gather information from approved sites, navigate forms, or retrieve facts from web pages.
- Travel booking: compare options, prepare itineraries, and stage bookings that may later require approval.
- Messaging: draft or send follow-ups in chat or SMS-like channels.
- Payments and purchases: review invoices, authorize payments, or prepare purchases with high-risk action boundaries.
- Cloud and device management: review device status, storage, or account settings without broad administrative overreach.

Each category should include both routine utility tasks and failure-mode tasks that pressure the permission boundary.

## Data taxonomy

The benchmark should not use a single overloaded data label. Each data object should instead be labeled along multiple axes so later evaluation stays modular.

### Relevance labels

- `necessary`: required for successful completion.
- `supporting`: helpful but not strictly required.
- `unnecessary_available`: accessible in the environment but not needed.
- `unrelated_private`: personal data that is irrelevant to the task and should stay untouched.

### Sensitivity labels

- `ordinary`: low-risk content.
- `sensitive`: personal content that may be needed only in narrow cases.
- `dangerous`: high-impact content such as payment credentials, account recovery artifacts, identity documents, or unrelated secrets.

### Trust labels

- `trusted_content`: benign benchmark content.
- `untrusted_tool_output`: ordinary external content whose safety is unknown.
- `adversarial_content`: content intentionally crafted to inject instructions, lure exfiltration, or trigger over-broad actions.

### Derived data

Benchmark outputs produced from allowed inputs should be labeled separately as derived artifacts. A derived artifact is acceptable only if its inputs were allowed and any required redaction policy was satisfied.

## Tool action taxonomy

Benchmark tools should normalize actions into a compact vocabulary so policy labels and metrics can stay stable across domains.

- `read`: open or retrieve a specific resource.
- `search`: query or enumerate resources within a store.
- `summarize`: produce a condensed output from already allowed inputs.
- `draft`: create but do not externally commit a message, form, or record.
- `send`: transmit a message through an approved channel.
- `forward`: transmit an existing artifact or content bundle.
- `upload`: move local data to an external service.
- `download`: import external data into the session or storage.
- `modify`: edit an existing record.
- `delete`: remove or archive an item.
- `purchase`: initiate a transaction or booking.
- `authorize_payment`: commit payment or release funds.
- `post_external`: publish or send data to an external endpoint.
- `authorize_access`: grant or extend authority for another principal or service.

The benchmark should explicitly test cases where a narrow action should be allowed but a broader action over the same resource should be denied or require confirmation.

## Policy labels

Per-action policy outcomes should use a small, explicit label set:

- `allow`
- `deny`
- `require_confirmation`
- `allow_with_redaction`
- `allow_with_narrowed_scope`
- `require_safer_alternative`

These labels should be applied to concrete action-plus-scope requests, not only to whole tasks. A benchmark instance may include multiple policy outcomes within the same task.

## Attack taxonomy

The benchmark should include both standalone attack cases and attack variants attached to routine tasks.

- Indirect prompt injection from email, documents, webpages, or messages.
- Explicit data-exfiltration requests hidden inside otherwise relevant content.
- Over-broad access requests where the agent asks for an entire mailbox, directory, or contact list when only a narrow slice is needed.
- Confused-deputy scenarios where a tool with broader authority is misused for a narrower task.
- Malicious document cases that entice the agent to reveal unrelated secrets or upload private files.
- Malicious webpage cases that attempt off-task navigation, credential capture, or unauthorized sharing.
- Malicious email cases that mix legitimate user goals with embedded attacker instructions.
- Consent-laundering cases where a system tries to justify risky access with vague user-facing language.

## Benchmark instance composition

Every benchmark task should define:

- A stable task identifier and category.
- A synthetic environment bundle with resource references and data labels.
- The user-visible request as the agent sees it.
- The minimum intended task output.
- Available tools and normalized actions.
- Expected allowed actions.
- Expected denied or escalated actions.
- Attack variants, if any.
- Success criteria and failure criteria.

The benchmark should not require a single gold action sequence. It should instead define a permitted action envelope and a minimal outcome target, so different agents can solve the task in different safe ways.

## Evaluation metrics

Core metrics remain:

- Task success
- Necessary access rate
- Over-access rate
- Exfiltration rate
- False allow
- False deny
- Consent burden
- Recovery quality
- Auditability

`non-expert comprehension score` remains an important project metric, but it should stay out of the first purely automated benchmark release unless the project adds a separate user-study protocol or a defensible proxy.

Formal definitions and record-level measurement hooks are specified in [benchmark_schema_plan.md](benchmark_schema_plan.md).

## Constraints

- Do not include real personal data, credentials, or account artifacts.
- Do not claim validation or empirical results at the schema stage.
- Keep schemas easy to implement later in Python.
- Keep task definitions independent from any one agent implementation.
- Keep policy and audit records expressive enough to score both utility and privacy/security failures.

## Open design questions

- Should the first release be narrow and attack-rich, or small but cross-domain from day one?
- How should partial task success be scored when a safe denial prevents the original plan but a safer alternative succeeds?
- How should confirmation burden be measured when one task contains multiple medium-risk decisions?
- How much environment detail should be part of the task record versus shared fixture libraries?
- When should `allow_with_redaction` be scored as success versus partial success?
