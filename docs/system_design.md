# System Design

## Design objective

PAPF should let an agent help interpret a user task without letting the model decide what authority it ultimately receives. The system therefore separates:

- `proposal logic`: task interpretation, candidate capabilities, plain-language explanations, and recovery suggestions.
- `enforcement logic`: deterministic policy checks, scoped capability issuance, consent gating, and runtime mediation.

The result should be a permission control plane for consumer agents, not a prompt-only behavior policy.

## Core design principles

- External enforcement: the LLM is never the final authority for access, transfer, or commitment actions.
- Least privilege by construction: authority should be bound to action, resource type, scope, purpose, and session.
- Deny on mismatch: if a tool request cannot be matched to an explicit capability or policy rule, it should not execute.
- Inspectable state: every granted capability, denial, narrowing step, confirmation, and executed call should be reconstructable from structured logs.
- Modular evaluation: intent parsing, policy decisions, traces, and metrics should remain separate so the benchmark can test each layer.
- Privacy-safe development: the first prototype should use synthetic environments only and avoid production integrations.

## Trust boundaries

### Trusted control-plane components

- Intent normalizer after schema validation
- Capability compiler
- Policy engine
- Consent manager
- Audit logger
- Evaluation harness

These components are trusted to enforce policy, but their outputs must still be explicit and reviewable.

### Untrusted or partially trusted components

- The LLM planner or parser
- Tool outputs such as emails, files, webpages, and messages
- Any content that may contain prompt injection or hidden instructions
- Tool adapters that expose broad stores unless mediated by PAPF

The system should assume these components may suggest over-broad access, off-task actions, or unauthorized disclosure.

## End-to-end execution flow

1. The user issues a natural-language task.
2. The intent layer produces a structured task proposal.
3. The capability compiler converts that proposal plus environment metadata into a narrow capability bundle and policy pack.
4. The consent layer determines which capabilities can activate immediately and which require user confirmation.
5. The agent proposes tool calls while working on the task.
6. Every tool call passes through the runtime enforcement point before the tool executes.
7. The enforcement point allows, narrows, redacts, escalates, or blocks the call.
8. Executed calls return sanitized outputs to the agent.
9. The audit layer records the proposal, compiled capabilities, decisions, confirmations, tool calls, observed data touches, and task outcome.
10. The evaluation harness scores the run against task policy and benchmark metrics.

At no point should a direct model decision bypass the enforcement point.

## Layer 1: Task intent analysis

### Purpose

Convert an ambiguous user request into a normalized task-intent record that later layers can reason over.

### Inputs

- User request
- Optional conversation context
- Environment summaries or resource metadata

### Outputs

A `TaskIntent` record should capture at least:

- `task_summary`
- `user_goal`
- `requested_actions`
- `candidate_resource_types`
- `candidate_resource_refs`
- `proposed_scope_constraints`
- `expected_output_type`
- `uncertainty_flags`
- `safety_notes`

### Design stance

- This layer may use an LLM for semantic interpretation.
- Its output is advisory until validated against a schema and compiled by later layers.
- If uncertainty is high, the layer should surface ambiguity instead of silently broadening scope.

## Layer 2: Capability compiler

### Purpose

Translate normalized task intent into machine-checkable authority that the runtime can enforce.

### Inputs

- `TaskIntent`
- Environment/resource metadata
- Benchmark task policy definitions
- System defaults for risk and consent

### Outputs

The compiler should produce two linked artifacts:

1. `CapabilityBundle`
2. `PolicyPack`

Each capability should bind:

- `capability_id`
- `resource_type`
- `action`
- `scope`
- `purpose_binding`
- `session_bound`
- `consent_level`
- `derived_from_intent_fields`
- `expiration`

### Compiler behavior

- Prefer narrow references over broad search authority when the environment already contains likely targets.
- Separate preparatory authority from commitment authority. For example, `draft` and `send` should usually be distinct capabilities.
- Encode safer alternatives when a risky action is not pre-approved.
- Fail closed when the requested authority cannot be justified from the task intent.

## Layer 3: Runtime policy enforcement point

### Purpose

Mediate every attempted tool action and make the final allow or deny decision outside the LLM.

### Responsibilities

- Normalize incoming tool requests into a stable action-and-scope representation.
- Match requests against active capabilities and static policy rules.
- Apply scope narrowing or redaction when allowed by policy.
- Trigger confirmation when required.
- Deny unmatched, off-purpose, expired, or over-broad requests.
- Return explicit machine-readable reasons for each decision.

### Key invariant

No tool adapter should execute a real call until the enforcement point has emitted an `allow`, `allow_with_redaction`, or `allow_with_narrowed_scope` decision.

## Layer 4: Risk-adaptive consent

### Purpose

Control when the system can proceed automatically versus when it must ask the user to authorize a higher-risk step.

### Design model

Consent should be attached to concrete capability types, not left as an open-ended chat question. A simple first taxonomy is:

- `none`: low-risk, pre-approved read or draft activity inside the scoped task boundary.
- `confirm`: medium-risk actions such as sending a drafted message or accessing a narrower class of sensitive data.
- `high_risk_confirm`: high-impact actions such as payment authorization, external upload of sensitive data, or privilege extension.
- `disallow`: actions that should never be reachable in the current task.

### Design requirement

The user-facing prompt should describe:

- what the agent wants to do,
- which concrete data or destination is involved,
- why it is needed for the task, and
- what safer alternative exists if the user declines.

## Layer 5: Audit and traceability

### Purpose

Produce an append-only trace that is sufficient for debugging, evaluation, post-hoc review, and later user-facing explanations.

### Required event families

- Task start and normalized intent
- Capability compilation
- Policy checks
- Confirmation requests and resolutions
- Tool execution or tool blocking
- Data-touch summaries
- Final task outcome

### Logging stance

- Record structured identifiers and short rationales rather than raw personal payloads.
- Preserve links between intent, capability issuance, policy decisions, and actual tool calls.
- Keep the schema aligned with the benchmark plan so auditability becomes measurable rather than anecdotal.

## Layer 6: Evaluation harness

### Purpose

Measure whether PAPF improves the utility-versus-privacy tradeoff under realistic benchmark tasks.

### Responsibilities

- Load benchmark tasks, policies, and synthetic environments.
- Execute baseline and PAPF-controlled runs under comparable conditions.
- Score task success, over-access, exfiltration, false allow, false deny, consent burden, recovery quality, and auditability.
- Separate policy-definition errors from runtime-enforcement errors when analyzing failures.

The evaluation layer is not part of runtime enforcement, but it should consume the same schemas.

## First executable scope

The current best first slice remains a narrow, attack-relevant environment spanning:

- email
- files
- browser-linked retrieval

This slice is sufficient to test:

- narrow read versus broad search
- attachment handling
- prompt injection from messages or webpages
- unauthorized forwarding, upload, or cross-tool disclosure
- recovery after denial or scope narrowing

The first prototype should avoid real external services and instead run on synthetic fixtures with deterministic tool adapters.

## Rule-based versus model-assisted responsibilities

### Rule-based first

- Capability schema validation
- Mapping normalized actions to policy actions
- Scope matching
- Risk tier assignment
- Confirmation policy
- Deny-by-default runtime decisions
- Audit event emission
- Metric computation

### Model-assisted later

- Natural-language intent interpretation
- Candidate capability proposals
- User-facing explanation wording
- Safer recovery suggestions after a denial

Even when model-assisted features are added, the model should not be allowed to mint new authority on its own.

## Threat assumptions

- Untrusted content may contain indirect prompt injection.
- The agent may ask for more access than the task justifies.
- Tool APIs may expose ambient authority that must be narrowed by PAPF.
- Users may approve risky actions if prompts are vague or overly frequent.
- The first prototype will not eliminate all semantic ambiguity; it should instead make uncertainty explicit and fail safely.

## Non-goals for the first phase

- Production account integration
- Real user data
- Autonomous purchasing or payment execution
- Claims of formal least-privilege optimality
- Strong non-expert usability claims without a separate study

## Open design questions

- How much environment metadata should the compiler receive before it starts looking like a search engine itself?
- When intent is ambiguous, should the first prototype prefer clarification or deterministic refusal?
- How should `allow_with_redaction` be represented so both runtime and evaluator can verify what was removed?
- Which baseline best exposes PAPF's contribution: broad ambient access, prompt-only guardrails, or both?
