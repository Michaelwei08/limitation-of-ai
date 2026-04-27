# Research Brief

## Problem statement

Consumer AI agents increasingly act over personal resources such as email, calendars, files, browsers, and payment flows. Current agent stacks often grant broad access once a task begins, even when the task only needs a narrow subset of data or actions. This project asks whether an agent can operate under task-scoped permissions that are both understandable to non-expert users and enforceable at runtime.

## Motivation

- Personal-agent tasks naturally cross sensitive data boundaries.
- Existing approval flows are often too coarse or too frequent.
- Prompt-only guardrails are weak against overreach, confused-deputy behavior, and prompt-injection attacks.
- A useful solution must preserve task success while reducing unnecessary access.

## Core thesis

Permission enforcement should not depend on the LLM's self-restraint. The LLM may help interpret task intent and explain requested access, but final decisions and enforcement should be externalized into machine-checkable capabilities, runtime policy checks, and auditable traces.

## Main research questions

1. Can task intent be compiled into narrow permissions that still allow successful completion of realistic consumer-agent tasks?
2. How should permissions be presented so non-expert users can understand what is being granted and why?
3. How well does task-scoped enforcement reduce over-access and exfiltration risk compared with broader agent permissions?
4. What failure modes appear when permissions are too strict, and how effectively can the system recover through escalation or denial handling?

## Intended contribution

- A system framing for task-scoped permission boundaries for consumer AI agents
- A benchmark of synthetic personal-agent tasks with explicit necessary and unnecessary access
- A measurement protocol covering utility, privacy, and security tradeoffs
- A concrete enforcement architecture that places policy checks outside the LLM

## Paper argument

The paper should argue that agent safety for consumer settings needs a permission model closer to capability systems than to prompt-level refusal. The contribution is not a generic ethics discussion; it is a measurable framework for constraining agent access while preserving usefulness.

## Possible venue positioning

- Security/privacy systems venue: emphasize enforcement, threat model, and attack resistance
- HCI/privacy venue: emphasize user-comprehensible permission boundaries and consent burden
- ML datasets and benchmarks venue: emphasize the benchmark and multi-metric evaluation setup

Exact venue choice is `TODO`. Positioning should be refined after the first benchmark slice and prototype evaluation are defined.
