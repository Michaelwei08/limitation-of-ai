# Implementation Plan

## 1. Minimal viable prototype

The first PAPF prototype should implement a narrow but complete control loop over synthetic tasks in the `email + files + browser` slice.

### MVP objective

Demonstrate that an external permission control plane can:

- compile scoped task authority from a user request,
- enforce that authority on every tool call,
- require confirmation for higher-risk actions,
- emit a usable audit trace, and
- score runs on utility and privacy/security metrics.

### MVP boundaries

- No production integrations
- No real personal data
- No credentials or account tokens
- No hidden LLM override path
- No broad cross-domain support yet

### MVP scenario types

- Clean utility tasks
- Temptation tasks with irrelevant private files available
- Adversarial tasks with injected instructions in emails or webpages
- Recovery tasks where a blocked action has a safer fallback

## 2. Main modules

The repo should keep runtime concerns aligned with the suggested package layout.

### `src/papf/intent/`

Responsibility:

- Define the normalized task-intent schema.
- Validate parser outputs.
- Provide a rule-based baseline parser for narrow benchmark tasks.
- Later support an LLM-backed proposer behind the same schema.

Primary outputs:

- `TaskIntent`
- `IntentIssue`

### `src/papf/capabilities/`

Responsibility:

- Define capability and scope schemas.
- Compile `TaskIntent` plus environment metadata into a `CapabilityBundle`.
- Separate active capabilities from capabilities requiring confirmation.

Primary outputs:

- `Capability`
- `CapabilityBundle`
- `ScopeSpec`

### `src/papf/policy/`

Responsibility:

- Store static policy rules for benchmark tasks.
- Match normalized action requests against rules and capabilities.
- Produce deterministic policy decisions with rationale codes.

Primary outputs:

- `PolicyRule`
- `PolicyPack`
- `PolicyDecision`

### `src/papf/enforcement/`

Responsibility:

- Serve as the runtime policy enforcement point.
- Normalize tool requests into a common action model.
- Ask the policy layer for a decision before execution.
- Apply narrowing, redaction, blocking, or confirmation flow.

Primary outputs:

- `ToolRequest`
- `EnforcementResult`

### `src/papf/audit/`

Responsibility:

- Emit append-only structured events.
- Link task intent, compiled capabilities, confirmations, policy decisions, and executed calls.
- Support later explanation and debugging views without changing runtime semantics.

Primary outputs:

- `AuditEvent`
- `RunAuditLog`

### `src/papf/benchmark/`

Responsibility:

- Load task definitions, policy packs, and synthetic environment fixtures.
- Define task suites for clean, temptation, attack, and recovery settings.
- Provide fixture validators.

Primary outputs:

- `BenchmarkTask`
- `EnvironmentBundle`

### `src/papf/evaluation/`

Responsibility:

- Score traces against benchmark expectations.
- Compute task success, over-access, exfiltration, false allow, false deny, consent burden, recovery quality, and auditability.
- Produce run summaries that are reproducible and baseline-comparable.

Primary outputs:

- `RunMetrics`
- `EvaluationReport`

## 3. Data structures needed

The first implementation should keep records explicit and small.

### Core runtime records

- `TaskIntent`
  - goal summary
  - requested actions
  - candidate resources
  - scope constraints
  - expected output
  - uncertainty flags

- `ScopeSpec`
  - resource type
  - selector type
  - selector value
  - optional destination or domain constraint

- `Capability`
  - capability id
  - action
  - scope spec
  - purpose binding
  - consent level
  - expiration or session boundary

- `CapabilityBundle`
  - task id
  - active capabilities
  - dormant capabilities requiring confirmation
  - compiler notes

- `ToolRequest`
  - tool name
  - normalized action
  - requested scope
  - referenced inputs
  - external destination if any

- `PolicyDecision`
  - matched rules
  - decision label
  - reason code
  - narrowing details
  - redaction details
  - confirmation requirement

- `AuditEvent`
  - event type
  - actor
  - related ids
  - summary
  - outcome

### Benchmark and scoring records

- `BenchmarkTask`
- `PolicyPack`
- `ToolCallRecord`
- `EnvironmentBundle`
- `RunMetrics`

These should align with the schema intent already documented in [benchmark_schema_plan.md](benchmark_schema_plan.md).

## 4. Interfaces between modules

The architecture should use narrow, explicit interfaces so later tasks can implement each layer independently.

### Intent -> Capabilities

Input:

- `TaskIntent`
- task-local environment metadata

Output:

- `CapabilityBundle`
- compiler warnings or abstentions

Contract:

- The compiler consumes only validated intent records.
- The intent layer cannot directly activate a tool permission.

### Capabilities + Policy -> Enforcement

Input:

- `CapabilityBundle`
- `PolicyPack`
- `ToolRequest`

Output:

- `PolicyDecision`
- optional narrowed request

Contract:

- Enforcement must ask policy for every request, including reads.
- Any request lacking a matching capability is denied by default.

### Enforcement -> Consent

Input:

- `PolicyDecision` requiring escalation

Output:

- confirmation outcome
- capability activation or refusal

Contract:

- Confirmation should activate only the specific dormant capability or one-time action, not a broad class of future actions.

### Enforcement -> Tool runtime

Input:

- allowed or transformed `ToolRequest`

Output:

- execution result
- observed data references

Contract:

- Tool adapters should expose what data objects were actually touched so scoring can distinguish requested scope from realized access.

### Runtime -> Audit -> Evaluation

Input:

- intent record
- compiled bundle
- policy decisions
- tool-call results
- task outcome

Output:

- append-only audit log
- scored metrics

Contract:

- Evaluation should operate from recorded structured events rather than hidden in-memory assumptions.

## 5. What should be rule-based first

The first prototype should keep the security-critical path deterministic.

- Intent schema validation
- Resource-type normalization
- Action normalization
- Capability compilation rules for benchmark templates
- Scope matching and narrowing
- Consent tier mapping
- Policy decision logic
- Audit event generation
- Metric computation

This is the minimum needed to make claims about external enforcement rather than prompt behavior.

## 6. What may later use an LLM

The first prototype can stub these or support them behind strict schema boundaries.

- Interpreting a natural-language task into a candidate `TaskIntent`
- Suggesting candidate resource references from coarse environment summaries
- Generating user-facing explanations for confirmation prompts
- Producing recovery suggestions after denial
- Summarizing an audit trace for human review

If an LLM is used, its outputs should be treated as proposals that must pass schema validation and policy checks.

## 7. Testing strategy

Testing should follow the module boundaries rather than only end-to-end demos.

### Unit-level priorities

- Intent validation rejects malformed or over-broad intent records.
- Capability compilation produces narrow scopes for known task templates.
- Policy matching allows expected actions and denies mismatched scope.
- Consent logic separates draft from send, read from upload, and prepare from commit actions.
- Audit logging preserves event linkage and required fields.
- Metrics are deterministic on fixed traces.

### Fixture and schema validation

- Every benchmark task should load successfully.
- Every referenced resource id should resolve in its environment bundle.
- Expected allowed and forbidden actions should be internally consistent.
- Synthetic data labels should cover relevance, sensitivity, and trust.

### End-to-end benchmark checks

- Clean tasks complete without unnecessary confirmations.
- Temptation tasks avoid unrelated private data.
- Attack tasks block cross-tool exfiltration or off-task browsing.
- Recovery tasks receive credit for safer alternatives after denial.

### Comparison runs

Once runtime code exists, compare at least:

- broad ambient access baseline
- prompt-only guardrail baseline
- PAPF enforcement runtime

## 8. Risks and failure modes

- Intent ambiguity: a user request may not identify the minimum necessary scope, forcing either clarification or safe refusal.
- Hidden ambient authority: a tool adapter may still expose broad access unless PAPF sits in front of every call.
- Over-broad compilation: the compiler may grant search or read scope wider than the task justifies.
- Consent laundering: vague prompt wording could make risky actions appear routine.
- Audit incompleteness: if observed data touches are not recorded, over-access cannot be measured credibly.
- Baseline mismatch: if baselines do not share the same tool environment, evaluation claims will be weak.
- Scope explosion: cross-domain support too early would blur interfaces before the first slice is validated.
- False deny burden: an overly conservative first version may protect privacy while making tasks fail too often.

## 9. Milestones

### Milestone 1: Runtime schema foundation

- Finalize `TaskIntent`, `Capability`, `PolicyRule`, `ToolRequest`, `PolicyDecision`, and `AuditEvent` shapes.
- Align them with the benchmark schema plan.
- Add fixture examples for the first narrow task family.

Exit criteria:

- The repository has stable documentation for the runtime records and their contracts.

### Milestone 2: Narrow benchmark slice

- Implement benchmark fixtures for `email + files + browser`.
- Encode clean, temptation, attack, and recovery variants.
- Validate task-policy consistency.

Exit criteria:

- The benchmark slice can load deterministically and express the intended policy boundary.

### Milestone 3: Rule-based PAPF runtime

- Implement a rule-based intent baseline for the narrow slice.
- Compile capabilities.
- Enforce per-call policy decisions.
- Emit audit events.

Exit criteria:

- Synthetic tasks can run end to end with enforcement outside the model.

### Milestone 4: Scoring and baselines

- Add metric computation.
- Run broad-access and prompt-only baselines.
- Compare against PAPF on the first benchmark slice.

Exit criteria:

- The project can generate defensible utility and privacy/security comparisons on synthetic tasks.

### Milestone 5: Model-assisted extensions

- Add optional LLM intent proposals or explanation generation behind the same schemas.
- Measure whether they improve utility without weakening enforcement.

Exit criteria:

- Any LLM-assisted layer remains non-authoritative and benchmark-comparable to the rule-based baseline.
