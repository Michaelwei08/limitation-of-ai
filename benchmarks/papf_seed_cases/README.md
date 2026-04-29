# PAPF Seed Cases

This directory contains synthetic, file-backed PAPF benchmark cases.

`email_files_browser.yaml` mirrors the current smoke-test fixture so loader
coverage can grow without removing the hard-coded fixture yet. The additional
YAML files expand the first `email + files + browser` slice with redaction,
confirmation-gated outbound actions, over-access temptation, prompt injection,
cross-tool exfiltration attempts, and recovery traces.

All records in this directory must use synthetic data only.
