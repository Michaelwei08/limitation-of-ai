# Task 014: Redaction Evidence

## Goal

Represent `allow_with_redaction` as a verifiable runtime artifact.

## Create or update

- `src/papf/enforcement/redaction.py`
- `src/papf/audit/models.py`
- `tests/test_redaction_evidence.py`

## Requirements

- Add a `RedactionArtifact` record with source refs, removed field labels, output ref, and rationale.
- Ensure audit events link to redaction artifacts.
- Do not store raw sensitive payloads in logs.
- Make metric computation able to distinguish redacted access from unredacted disclosure.

## Verification

- Test that redaction-required rules cannot execute without a redaction artifact.
