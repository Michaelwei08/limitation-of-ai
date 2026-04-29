# Benchmark Case Design Notes

## Design Principles

- Keep cases synthetic and privacy-safe.
- Label reusable and invalidated checkpoint state explicitly.
- Make local replanning preferable to both blind continuation and full restart when possible.
- Include cases where continuation should stop or clarify, not only cases where adaptation is straightforward.
- Avoid raw chain-of-thought; store compact checkpoint summaries instead.

## Input-Type Coverage

The seed set covers addition, revision, correction, constraint change, scope reduction, scope expansion, format override, abort, topic switch, ambiguous input, and safety override.

## Domain Coverage

The cases span literature review, long-form writing, coding/debugging, data analysis, math/reasoning, research planning, document analysis, tool-using workflow, email/calendar-style planning, travel planning, and safety-policy writing.

## Labeling Assumptions

The labels assume that a checkpointed system has access to summarized state rather than private hidden reasoning. `expected_reuse` identifies state that should remain useful. `expected_invalidate` identifies assumptions, conclusions, or planned steps that should no longer control the answer. `expected_local_replan` describes the minimal adaptation expected after the mid-task input.

## Open Questions

- How much reuse should be credited when the final answer changes substantially?
- When should topic switch or abort cases receive zero reuse credit versus credit for preserving safety constraints?
- How should ambiguity be scored when a model asks a useful clarification rather than producing a final answer?
- Should wasted reasoning be measured by token count, elapsed steps, or semantic duplication?

## Risks Of Ambiguity

Some user updates are intentionally underspecified. The benchmark should penalize confident guessing when a clarification is safer. It should not penalize a system for pausing when the local state does not contain enough information to revise correctly.

## Human Validation Needed Later

The current labels are seed annotations, not validated ground truth. Human review is needed to calibrate difficulty, decide acceptable alternate replans, and align scoring rubrics across domains.
