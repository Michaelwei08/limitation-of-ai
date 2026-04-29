# Model-Assisted Boundaries

This project allows model assistance only as an advisory proposal layer. A model,
scripted adapter, or deterministic fake proposer may return `TaskIntent`-shaped
data, but it cannot grant permissions, create capabilities, override policy
decisions, skip confirmation, or suppress audit records.

## Boundary Contract

The security-critical path remains deterministic:

1. A proposer returns an `IntentProposal` with raw candidate intent fields.
2. PAPF validates the raw proposal schema and converts it to a `TaskIntent` only
   if the required fields, enum labels, scope records, and known data references
   are valid.
3. Capability compilation uses only the validated `TaskIntent` plus the
   deterministic `PolicyPack`.
4. Every tool request is still mediated by runtime policy enforcement.

The accepted proposal is therefore a candidate input to the existing compiler,
not an authority source. Invalid proposals fail closed before capability
compilation.

## Allowed Model Roles

- Propose candidate intent fields such as requested actions, resource types,
  candidate data refs, uncertainty flags, and safety notes.
- Mark uncertainty that should lead to clarification or deterministic refusal in
  later policy layers.
- Draft user-facing explanations from structured policy, scope, consent, and
  audit records.
- Suggest recovery alternatives after a denial, provided any resulting request
  re-enters the same validation and enforcement path.

## Forbidden Model Roles

- Mint active or dormant capabilities.
- Treat model confidence as consent or policy authority.
- Expand scope after deterministic validation or runtime enforcement.
- Override denials, redaction requirements, or confirmation gates.
- Certify that redaction occurred without concrete redaction artifacts.
- Use hidden chain-of-thought as an enforcement or audit explanation.

## Current Implementation

`src/papf/intent/proposer.py` defines:

- `IntentProposer`, a protocol for optional advisory proposers.
- `IntentProposal`, a raw candidate intent record.
- `ProposalValidationResult`, which either contains an accepted `TaskIntent` or
  validation issues.
- `DeterministicFakeIntentProposer`, a no-model test proposer.
- `compile_capabilities_from_proposal`, a helper that validates before calling
  the existing deterministic compiler.

No model call is required for this layer. The deterministic fake proposer exists
to exercise the contract in tests and later ablations.

## Failure Behavior

Malformed proposal fields, unsupported enum labels, missing required lists,
scope/resource mismatches, and unknown data references are rejected before
capability compilation. A rejected proposal has no accepted `TaskIntent`, so it
cannot mint capabilities through the model-assisted path.
