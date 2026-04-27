# System Design

## Overview

PAPF is a layered permission framework for consumer AI agents. The design goal is to keep intent interpretation flexible while making permission issuance and enforcement explicit, narrow, and auditable.

## Layer 1: Task intent analysis

Translate a user request into a structured task description.

Outputs should include:

- User goal
- Relevant entities and resources
- Required actions
- Candidate data categories
- Uncertainty flags

This layer may use an LLM, but its output is only a proposal. It does not grant access by itself.

## Layer 2: Capability compiler

Compile the structured task description into narrow, machine-checkable capabilities.

Possible capability fields:

- Resource type
- Resource scope
- Action type
- Purpose or task binding
- Expiration or session scope
- Consent level

The compiler should prefer the least privilege that still supports the task.

## Layer 3: Runtime policy enforcement

Check each tool call against the compiled capability set.

Responsibilities:

- Match requested action to allowed capability
- Reject out-of-scope data access
- Reject unapproved external transfers
- Produce clear denial reasons
- Support deterministic policy evaluation where possible

This layer is the main enforcement boundary and must operate outside the LLM.

## Layer 4: Risk-adaptive consent

Not every action should require the same user interaction. Consent should depend on risk and user comprehension.

Illustrative levels:

- Low risk: proceed under pre-approved scoped capability
- Medium risk: require explicit confirmation with plain-language rationale
- High risk: require stronger confirmation or deny by default

The exact policy is `TODO`, but the core idea is to reduce both blind over-approval and excessive prompt fatigue.

## Layer 5: Audit and traceability

Record what the agent asked for, what was granted, what was denied, and what data was accessed.

Audit records should support:

- Post-hoc review
- Failure analysis
- Metric computation
- User-facing explanations
- Security investigation

## Threat model assumptions

- The agent may face prompt injection from tools or content it reads.
- The LLM may suggest over-broad actions.
- Tool interfaces may offer access broader than the task requires.
- Users may not accurately evaluate raw technical permission requests.

Threat model details remain `TODO` and should be refined alongside the benchmark.

## Non-goals for the first phase

- Full implementation of all PAPF layers
- Claims about empirical performance
- Production-ready integration with real personal accounts
