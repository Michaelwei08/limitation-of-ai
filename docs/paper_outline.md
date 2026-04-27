# Paper Outline

## Recommended paper story

The first paper should be framed as a security/privacy systems paper on externally enforced, task-scoped permissions for consumer AI agents, with a benchmark-backed evaluation. The benchmark is an evaluation artifact in service of the systems claim, not the sole contribution.

## Working title options

1. Personal Agent Permission Firewall: Task-Scoped External Enforcement for Consumer AI Agents
2. Task-Scoped Permission Boundaries for Consumer AI Agents
3. Compiling User Tasks into Enforceable Agent Permissions
4. PAPF: A Permission Control Plane for Consumer AI Agents

## One-sentence thesis

Consumer AI agents should not receive broad ambient authority; instead, natural-language tasks should be compiled into narrow, machine-checkable permissions that are enforced outside the LLM and evaluated against both task utility and privacy/security failures.

## Core claims the paper may try to support

- A task-scoped permission architecture is a better framing for consumer-agent safety than prompt-only refusal.
- An external control plane can narrow effective authority while preserving useful task completion on a realistic synthetic task slice.
- Evaluation should measure both utility and privacy/security outcomes at the level of concrete tool calls and data touches.

These are candidate claims, not yet supported final findings.

## Proposed structure

### 1. Introduction

- Motivate why consumer agents cross sensitive personal-data boundaries.
- Argue that broad tool access creates excessive agency and confused-deputy risk.
- State the paper thesis: enforcement must be external to the LLM.
- Preview the artifact stack: PAPF architecture, narrow prototype, benchmark slice, and joint utility/security evaluation.

### 2. Problem Setting and Threat Model

- Define the consumer-agent setting and protected resources.
- Define over-access, exfiltration, false allow, false deny, consent burden, and recovery.
- Specify the attacker model: indirect prompt injection, malicious content, and over-broad tool requests.
- State the non-goals clearly: no production deployment claim, no formal least-privilege proof, no user-study-backed comprehension claim in the first paper.

### 3. PAPF Design

- Present the control-plane architecture.
- Explain the boundary between model-assisted proposal logic and deterministic enforcement logic.
- Describe task intent normalization, capability compilation, runtime mediation, consent gating, and audit logging.
- Emphasize deny-by-default mediation and inspectable decision traces.

### 4. Benchmark and Evaluation Substrate

- Describe the benchmark slice and why it focuses first on `email + files + browser`.
- Define the task schema, policy schema, tool-call trace schema, and audit schema.
- Explain the data-label taxonomy and attack taxonomy.
- Clarify that the benchmark defines safe action envelopes rather than one gold sequence.

### 5. Experimental Setup

- Describe the first PAPF prototype and the exact evaluation environment.
- Define baselines: broad ambient access and prompt-only guardrails.
- Specify task suites: clean, temptation, attack, and recovery.
- Define the reported metrics and what each metric captures.

### 6. Results

- Report only measured outcomes once implemented.
- Focus on tradeoffs among task success, over-access, exfiltration, false allow, false deny, consent burden, recovery quality, and auditability.
- Include failure analysis rather than only aggregate metrics.

### 7. Discussion and Limitations

- Analyze where PAPF helps and where it remains brittle.
- Discuss ambiguity, scope selection, redaction evidence, and benchmark generality limits.
- Separate supported conclusions from hypotheses for future work.

### 8. Related Work

- Prompt injection and tool-using agent safety
- Capability security, least privilege, and confused deputy
- Delegated authorization and explicit machine-checkable access control
- Permission UX, consent fatigue, and auditability

### 9. Conclusion

- Restate the systems argument.
- Summarize what the prototype and benchmark do establish.
- Bound the claims tightly and point to follow-up work on broader domains and user studies.

## Evidence expectations by section

### Introduction

- Needs verified threat and motivation citations.
- Must avoid novelty claims that are not literature-backed.

### Problem Setting and Threat Model

- Needs precise definitions that match the benchmark and system docs.
- Needs an explicit statement of what PAPF does not attempt to solve.

### PAPF Design

- Needs executable or at least implementation-aligned module boundaries.
- Needs concrete capability and policy examples.

### Benchmark and Evaluation Substrate

- Needs task fixtures, schema definitions, and deterministic metric computation.
- Needs attack variants and policy labels that can be validated in code.

### Experimental Setup

- Needs runnable baselines in the same synthetic environment.
- Needs a clear protocol for confirmations, narrowed scope, and blocked actions.

### Results

- Needs actual experiments.
- Must not include illustrative or speculative numbers.

### Discussion and Limitations

- Needs honest accounting of unsupported claims, especially on user comprehension and generality.

## Current framing decision

- Recommended first submission framing: security/privacy systems paper.
- Not recommended as the first framing: HCI-first permission-comprehension paper, unless a dedicated user study is added.
- Also not recommended as the primary framing: benchmark-only paper, unless implementation of the enforcement stack stalls and the benchmark becomes the strongest finished artifact.
