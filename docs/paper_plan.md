# Paper Plan

## Purpose

This document is a planning artifact for the first PAPF paper. It is not a draft paper and it does not assume that any experimental claim is already supported.

## Recommended first-paper framing

- Primary framing: security/privacy systems paper
- Core artifact stack:
  - a task-to-capability compiler,
  - an external runtime policy enforcement point,
  - an audit trace model, and
  - a benchmark-backed evaluation slice
- Scope discipline:
  - keep the first paper centered on the synthetic `email + files + browser` slice,
  - treat the benchmark as evaluation infrastructure for the systems thesis,
  - treat non-expert comprehension as a design requirement rather than a validated result unless a user study is added

## Working title options

1. Personal Agent Permission Firewall: Task-Scoped External Enforcement for Consumer AI Agents
2. Task-Scoped Permission Boundaries for Consumer AI Agents
3. Compiling User Tasks into Enforceable Agent Permissions
4. PAPF: A Permission Control Plane for Consumer AI Agents
5. Narrow Authority for Consumer AI Agents: External Permission Enforcement from Task Intent

## One-sentence thesis

Consumer AI agents should operate under task-scoped, machine-checkable permissions enforced outside the LLM, and those permission boundaries should be evaluated jointly for utility, over-access, exfiltration resistance, and recovery behavior.

## Candidate contributions

These are candidate contributions for planning purposes. They are not final novelty claims.

1. A clearer problem formulation for consumer-agent safety as a task-scoped permission-boundary problem rather than a prompt-only refusal problem.
2. A PAPF architecture that separates model-assisted task interpretation from deterministic capability issuance, runtime enforcement, consent gating, and audit logging.
3. A capability and policy representation that binds authority to action, resource, scope, purpose, session, and consent level.
4. A narrow but realistic benchmark slice with synthetic personal-agent tasks, explicit necessary/unnecessary/dangerous data labels, and attack variants.
5. An evaluation protocol that measures both utility and privacy/security failures at the level of concrete tool calls and data touches.

## Paper structure

### 1. Introduction

- Goal:
  establish why consumer agents need explicit permission boundaries
- Required evidence:
  citations on prompt injection, excessive agency, delegated authorization, and permission-UX limits
- Notes:
  keep the novelty phrasing cautious and avoid "first" claims unless the literature review later proves them

### 2. Problem Setting and Threat Model

- Goal:
  define the consumer-agent setting, trusted boundaries, attacker model, and target failure modes
- Required evidence:
  precise definitions aligned with benchmark labels and runtime policy semantics
- Notes:
  explicitly state non-goals, especially no claim of formal least-privilege optimality and no validated user-comprehension result yet

### 3. PAPF Design

- Goal:
  explain the control plane and why the LLM is not the final authority
- Required evidence:
  executable or implementation-aligned module boundaries, runtime record schemas, and at least one concrete capability-compilation example
- Notes:
  this section should make the system contribution legible even before the reader sees results

### 4. Benchmark and Evaluation Substrate

- Goal:
  describe the benchmark slice, task taxonomy, policy schema, tool traces, audit traces, and metrics
- Required evidence:
  benchmark task format, schema examples, attack taxonomy, and deterministic scoring hooks
- Notes:
  do not let this section overshadow the systems claim; it exists to make the evaluation credible

### 5. Experimental Setup

- Goal:
  define prototype scope, baselines, environments, suites, and metrics
- Required evidence:
  runnable prototype, comparable baselines, and explicit scoring protocol
- Notes:
  baselines should run in the same synthetic tool environment

### 6. Results

- Goal:
  show measured tradeoffs rather than isolated success rates
- Required evidence:
  actual runs over clean, temptation, attack, and recovery suites
- Notes:
  aggregate tables should be paired with failure-mode examples

### 7. Discussion and Limitations

- Goal:
  explain what PAPF does and does not establish
- Required evidence:
  observed failure cases, open design questions, and bounded interpretation of the results
- Notes:
  this section should preempt reviewer concerns about generality, ambiguity, and consent claims

### 8. Related Work

- Goal:
  place PAPF at the intersection of agent safety, delegated authorization, least privilege, permission UX, and auditability
- Required evidence:
  verified citations and cautious gap language
- Notes:
  the paper should argue for a gap at the intersection, not claim that neighboring categories are empty

### 9. Conclusion

- Goal:
  restate the systems contribution and bounded empirical findings
- Required evidence:
  only claims actually supported by the implemented evaluation

## Required evidence by major paper claim

| Candidate claim | Required evidence | Current status |
| --- | --- | --- |
| Prompt-only safety is insufficient for consumer-agent permission control | Verified prior work and threat framing | Partially supported by current literature map |
| External enforcement can reduce over-access and exfiltration while preserving useful task completion | Executable prototype plus comparative experiments against shared baselines | Unsupported until implementation and experiments exist |
| Task-to-capability compilation can produce usefully narrow authority on realistic tasks | Capability compiler, task fixtures, and qualitative plus quantitative examples | Unsupported until compiler and fixtures exist |
| PAPF supports meaningful recovery after denial or narrowing | Recovery tasks and measured recovery-quality outcomes | Unsupported until benchmark and runtime exist |
| Auditability is measurable rather than anecdotal | Concrete audit schema plus completeness scoring over actual runs | Unsupported until trace generation and scoring exist |
| Task-scoped grants are understandable to non-experts | User study or other direct human-subject evidence | Unsupported; should not be claimed in the first automated-only paper |

## Figures and tables needed

See [figures_and_tables_plan.md](figures_and_tables_plan.md). The minimum likely paper set is:

- a system architecture figure,
- a task-to-capability compilation example,
- a benchmark/task taxonomy figure or table,
- a policy-decision example,
- a main metrics table,
- a baseline comparison table,
- a failure-case table or qualitative figure.

## Experiments needed

### E1. Core PAPF versus baselines

- Compare:
  - broad ambient access baseline
  - prompt-only guardrail baseline
  - PAPF external enforcement
- Suites:
  - clean
  - temptation
  - attack
  - recovery
- Metrics:
  - task success
  - necessary access rate
  - over-access rate
  - exfiltration rate
  - false allow
  - false deny
  - consent burden
  - recovery quality
  - auditability

### E2. Narrowing and escalation analysis

- Measure how often PAPF narrows broad requests into safe scopes.
- Measure how often confirmation is triggered and whether the prompts correspond to genuinely higher-risk steps.
- Show examples where denial plus safer alternative still succeeds.

### E3. Attack-focused evaluation

- Use prompt-injection and exfiltration variants across email, files, and browser-linked tasks.
- Evaluate whether PAPF blocks or narrows cross-tool misuse that broad-access or prompt-only baselines allow.

### E4. Ablation or component analysis

- Candidate ablations:
  - without capability narrowing
  - without confirmation gating
  - without audit scoring
- Goal:
  identify which control-plane components matter most for the utility/privacy tradeoff

### E5. Cross-task generalization within the narrow slice

- Show that the same policy machinery handles multiple task templates within `email + files + browser`.
- Avoid claiming full cross-domain generality from this evidence alone.

## Related work sections

The paper should likely structure related work into these clusters:

1. Prompt injection and tool-using agent safety
2. Excessive agency and over-broad tool authority
3. Confused deputy, capability security, and least privilege
4. Delegated authorization, structured scopes, and machine-checkable access control
5. Permission UX and consent fatigue
6. Auditability and provenance

## Claims that are currently unsupported

- PAPF materially improves task success and privacy/security tradeoffs relative to realistic baselines.
- PAPF reduces over-access and exfiltration in attack-rich tasks.
- PAPF grants are near-minimal rather than simply narrower than broad defaults.
- PAPF generalizes beyond the first `email + files + browser` slice.
- PAPF's confirmation model is understandable to non-experts.
- PAPF audit traces are practically useful for debugging, review, or user explanation.
- PAPF occupies a novel research gap rather than a crowded adjacent design space.

## Risks of overclaiming

1. Claiming novelty too early
   The safest phrasing is that PAPF targets an apparent gap at the intersection of several literatures.
2. Claiming least privilege in a formal sense
   The first prototype may only show narrower and externally enforced authority, not optimal minimal authority.
3. Claiming user comprehension
   Without a user study, the paper should discuss legibility as a design goal only.
4. Claiming robustness to prompt injection in general
   The paper may only support claims within the benchmarked attacks, tools, and synthetic environments.
5. Claiming broad consumer-domain generality
   The first paper should stay disciplined around the narrow slice.
6. Claiming auditability as a solved property
   The paper should state what the audit schema records and what it does not yet enable.

## Recommended first submission framing

- Best current framing:
  security/privacy systems paper with benchmark-backed evaluation
- Abstract-level emphasis:
  compile user tasks into externally enforced capabilities, mediate every tool call, and evaluate the utility/privacy tradeoff under realistic synthetic attacks
- What to de-emphasize in the first submission:
  broad HCI claims, generalized consumer-agent deployment claims, and benchmark-only positioning

## Actionable writing order

1. Lock the system claim and threat model first.
2. Finalize the runtime and benchmark schemas so the evaluation section has stable semantics.
3. Implement the narrow prototype and baseline environment.
4. Run experiments before drafting strong Introduction and Results claims.
5. Draft Related Work only after the system and evaluation story are fixed enough to know what exactly must be contrasted.

## Concrete gaps before paper drafting

- Citation-ready bibliography entries are still missing.
- The benchmark slice is specified but not implemented.
- The capability compiler and runtime enforcement point do not yet exist in code.
- Baselines are not yet operationalized in a shared environment.
- Metric computation and audit completeness scoring are not yet implemented.
- No evidence yet supports a non-expert comprehension claim.
