# Research Brief

## Problem statement

Consumer AI agents increasingly act over personal resources such as email, calendars, files, browsers, and payment flows. Current agent stacks often grant broad access once a task begins, even when the task only needs a narrow subset of data or actions. This creates privacy harms before it becomes a conventional security incident: over-collection, secondary use, cross-context leakage, unauthorized disclosure, prompt-injection-mediated data exfiltration, and loss of user agency. This project asks whether an agent can operate under task-scoped permissions that are both understandable to non-expert users and enforceable at runtime.

## Motivation

- Personal-agent tasks naturally cross sensitive data boundaries.
- Existing approval flows are often too coarse or too frequent.
- Prompt-only guardrails are weak against overreach, confused-deputy behavior, and prompt-injection attacks that can become privacy violations.
- A useful solution must preserve task success while reducing unnecessary access, off-task disclosure, and hidden context transfer.

## Core thesis

Permission enforcement should not depend on the LLM's self-restraint. The LLM may help interpret task intent and explain requested access, but final decisions and enforcement should be externalized into machine-checkable capabilities, runtime policy checks, and auditable traces.

## Privacy principles as system requirements

| privacy principle | PAPF mechanism | evaluation measure |
|---|---|---|
| Data minimization | Compile only task-justified resource, action, scope, and session capabilities. | Necessary-access rate, over-access rate, false denies. |
| Purpose limitation | Bind each grant to the current task purpose and deny off-purpose tool calls. | False allows, unsafe-workaround rate, recovery quality. |
| Contextual integrity | Label resource relevance, sensitivity, and trust so data does not silently cross task contexts. | Cross-context leakage cases, forbidden data touches, exfiltration outcomes. |
| User consent | Escalate disclosure or commitment actions through risk-adaptive confirmation prompts. | Consent burden, allow/deny decision quality, perceived control. |
| Transparency and accountability | Record intent, capabilities, policy decisions, redactions, confirmations, tool calls, and outcomes. | Auditability completeness and trace-review usefulness. |

## Main research questions

1. Can task intent be compiled into narrow permissions that still allow successful completion of realistic consumer-agent tasks?
2. How should permissions be presented so non-expert users can understand what is being granted and why?
3. How well does task-scoped enforcement reduce over-collection, cross-context leakage, unauthorized disclosure, and exfiltration risk compared with broader agent permissions?
4. What failure modes appear when permissions are too strict, and how effectively can the system recover through escalation or denial handling?

## Intended contribution

- A human-centered privacy framing for task-scoped permission boundaries in consumer AI agents
- A consent interaction design space for making agent access, disclosure, redaction, and confirmation states legible to non-expert users
- An empirical evaluation plan for non-expert user comprehension, privacy-preserving consent decisions, perceived control, trust, workload, and consent fatigue
- A synthetic personal-agent evaluation slice with explicit necessary, unnecessary, dangerous, and cross-context access labels
- A concrete enforcement architecture that places policy checks outside the LLM and supplies technical feasibility evidence for the consent design
- A working hypothesis that the main gap lies in the combination of task-scoped capability compilation, external enforcement, non-expert permission framing, and multi-metric privacy-usability evaluation

## Paper argument

The paper should argue that personal-agent privacy requires a permission model closer to capability systems than to prompt-level refusal. The contribution is not a generic AI ethics discussion; it is a measurable human-centered privacy framework for constraining agent access, preserving user agency, and making enforcement outcomes inspectable while preserving usefulness.

## Venue positioning

- Primary target: HCI/privacy or usable-security privacy venue, centered on human-centered privacy, consent interaction design, user comprehension, and empirical evaluation with non-expert users.
- Evidence requirement for a full paper: the non-expert user study should be completed, analyzed, and reported with clear separation between user-study results and prototype trace results.
- Systems/security role: technical feasibility support. The enforcement prototype, capability compiler, policy checks, redaction evidence, confirmation gates, and audit logs show that the proposed consent states can be enforced outside the LLM.
- Benchmark role: secondary support. The synthetic suite helps measure over-access, false allows, exfiltration pressure, and auditability, but the paper should not be framed primarily as a systems/security benchmark paper.
- Workshop fallback: if the user study remains planned rather than completed, position PAPF as a bounded HCI/privacy workshop, design, or prototype paper about task-scoped consent and the evaluation protocol. In that fallback, do not claim empirical user comprehension, improved consent decisions, reduced fatigue, or deployable privacy protection.

Exact venue choice remains `TODO`, but the active direction is HCI/privacy-first: PAPF should be framed as human-centered task-scoped consent with external enforcement, with systems/security evidence used to establish that the interaction design has an enforceable backend.
