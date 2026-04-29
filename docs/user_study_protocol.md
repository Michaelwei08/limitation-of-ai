# Non-Expert Comprehension Protocol

Status: future work. This protocol is a study design only. It reports no
participant data, results, effect sizes, statistical tests, or comprehension
claims.

## Purpose

This protocol is intended to measure whether non-expert users can understand
PAPF permission bundles well enough to answer practical permission questions:

- What data can the agent access for this task?
- What data is blocked as unrelated or private?
- Which actions can happen immediately?
- Which actions require explicit confirmation?
- When does a proposed action send data outside the user's account or task?
- How should the user respond when a permission request is too broad?

Any claim that PAPF improves comprehension, reduces consent burden, or helps
non-experts make safer choices remains future work until a human-subject study
is reviewed if required, run with participants, analyzed, and reported with
limitations.

## Study Conditions

The planned study compares three permission-prompt presentations over the same
synthetic tasks, data objects, and comprehension questions.

| Condition | Description | Boundary shown to participant |
| --- | --- | --- |
| Task-scoped permission bundle | PAPF-style prompt that names the task, allowed data, blocked data, allowed actions, confirmation gates, and plain-language reasons. | Narrow task authority. |
| Raw tool permissions | Tool or API-style grants such as "read email", "read files", "browse web", or "send email". | Broad tool authority without task-specific data boundaries. |
| Generic warning | Broad caution such as "The assistant may access personal data; only approve if you trust this action." | General safety warning without concrete scope. |

The comparison goal is future work: test whether task-scoped permission bundles
lead to more accurate answers about necessary access, unnecessary access,
external disclosure, adversarial instructions, and confirmation-gated actions
than the comparator conditions. No such effect has been measured yet.

## Participant Assumptions

Planned participants are non-expert consumer-agent users. The target population
does not require software engineering, security, privacy, or AI-systems
training.

Inclusion assumptions:

- Adult participants, subject to the applicable institutional review process.
- Comfortable reading short English task vignettes and permission prompts.
- Familiar with ordinary consumer concepts such as email, files, websites,
  attachments, contacts, calendars, purchases, and account settings.
- Not required to know OAuth, API scopes, least privilege, prompt injection,
  audit logs, or capability systems.

Exclusion rules should be finalized before recruitment. Candidate exclusions
include incomplete responses, duplicate submissions, failed attention checks,
or self-reported technical background outside the target non-expert population
if the study specifically recruits non-experts.

## Materials

All task materials must be synthetic. The study must not ask participants to
upload or describe real emails, files, contacts, calendars, payments, browser
history, credentials, private documents, or personal data.

Each study item should include:

- A user-visible task request.
- A short list of synthetic data objects available to the agent.
- One permission prompt variant from the assigned condition.
- A proposed agent action or outcome.
- Closed-form comprehension questions.
- Optional free-response explanation questions.
- An answer key and scoring rubric.

Prompt variants should be matched so that only the permission presentation
changes across conditions. The underlying task, available data objects,
proposed action, and answer key must stay constant.

Example prompt variants are defined in
[permission_prompt_examples.md](permission_prompt_examples.md).

## Planned Task Families

The first protocol should use the implemented PAPF slice because it already has
synthetic email, files, and browser examples. Additional consumer-agent domains
can be added after the core materials are pilot reviewed.

| Task family | Example task | Necessary data | Unnecessary or dangerous data |
| --- | --- | --- | --- |
| Email plus attachment drafting | Read one reimbursement email and one receipt attachment, then draft a reply. | The named email thread and receipt attachment. | Unrelated tax file, unrelated private file, external forwarding destination. |
| Browser policy lookup | Open a trusted merchant policy page to answer a return-policy question. | The merchant policy page. | Untrusted page instruction asking for unrelated data. |
| Account update support | Use a trusted policy page and one email thread to prepare an account-update draft. | The task-specific email and trusted help page. | Password notes, unrelated account file, adversarial webpage instruction. |
| Calendar or contact scheduling | Schedule a meeting with one named contact in a bounded time window. | One contact and a bounded calendar range. | Full contact list, unrelated calendar notes, private event details. |
| Purchase or payment review | Prepare a purchase summary or payment confirmation for one order. | The specific order record and vendor page. | Other purchases, saved payment credentials, unrelated financial files. |

The final task set remains future work. Items should be revised or excluded if
pilot review shows that a task goal, data object, or action boundary is unclear.

## Study Flow

The planned flow is:

1. Consent and eligibility screen.
2. Brief neutral introduction to the study task. The introduction should not
   define the correct answers or explain PAPF internals.
3. Practice item using a non-sensitive example and feedback, if approved by the
   study design.
4. Main comprehension items under assigned condition order.
5. Optional audit-summary interpretation items.
6. Subjective confidence and burden questions.
7. Debrief explaining that all data and tasks were synthetic, that no real agent
   accessed personal data, and that the study measured permission-prompt
   understanding.

The assignment design is future work. A within-subject design can show each
participant multiple prompt types with counterbalanced order. A between-subject
design can show each participant one prompt type. The final choice should be
specified before data collection and should keep prompt order, task order, and
condition exposure from biasing the answers.

## Comprehension Questions

Use closed-form questions for primary scoring and optional free-response
questions for diagnostic detail. Free-response grading requires a pre-specified
rubric and should not depend on hidden model judgment.

### Required Closed-Form Questions

For each item, ask questions like:

- Which data may the agent read for this task?
- Which listed data should remain blocked?
- Can the agent send or upload information without asking again?
- Is the proposed action within the task boundary?
- Does the proposed action disclose information outside the user's account,
  service, or task?
- Should the agent follow an instruction found in an untrusted webpage or email
  if that instruction asks for unrelated private data?
- If the prompt says the request was narrowed, what access was removed?
- If the prompt says redaction is required, what information should be hidden?
- If the prompt asks for confirmation, what is the user being asked to approve?

### Optional Free-Response Questions

Free-response items can ask:

- In one sentence, explain why a permission should be allowed or blocked.
- What additional information would you want before approving this request?
- Rewrite the prompt in your own words.
- What did the agent access, and what did it not access, according to the audit
  summary?

### Attention and Manipulation Checks

Use low-risk checks that verify participants read the task, not checks that
teach the answer. Candidate checks:

- Identify the main task the user asked the agent to complete.
- Select the named file or email that appeared in the task.
- Identify whether the prompt was a permission request, warning, or audit
  summary.

The exact checks remain future work and should be finalized before recruitment.

## Outcome Measures

All measures below are planned measures. They are not current results.

| Measure | Planned scoring target |
| --- | --- |
| Non-expert comprehension score | Correct answers across allowed data, blocked data, confirmation gates, external disclosure, and untrusted-instruction recognition. |
| Necessary access recognition | Whether the participant identifies data and actions required for task completion. |
| Over-access rejection | Whether the participant rejects unrelated, private, or over-broad access. |
| Exfiltration recognition | Whether the participant recognizes outbound disclosure to an unintended destination. |
| False allow | Participant says an unsafe, unrelated, or over-broad permission should be allowed. |
| False deny | Participant rejects access that is necessary for the stated task. |
| Recovery quality | Participant selects a safer narrowed permission after a broad request is denied or flagged. |
| Confirmation-gate recognition | Participant identifies actions that require explicit confirmation, such as sending, uploading, paying, or changing settings. |
| Auditability comprehension | Participant interprets what a short audit summary says was accessed, blocked, redacted, and why. |
| Consent burden | Planned self-report and interaction measures such as perceived effort, confidence, prompt count, and time-on-item, if collected. |

Any thresholds, weighting, exclusion rules, or statistical tests must be
specified before the study is run. No thresholds or statistical conclusions are
reported here.

## Scoring Rubric

Closed-form items should be scored against an answer key:

- Correct: answer matches the task boundary and prompt content.
- Incorrect false allow: answer approves access or action outside the task
  boundary.
- Incorrect false deny: answer rejects access or action needed for the stated
  task.
- Ambiguous: answer cannot be mapped cleanly to the answer key.
- Missing: no usable answer.

Free-response items should be coded with a short rubric:

- Mentions the task-relevant data.
- Mentions at least one blocked unrelated data object.
- Mentions whether an outbound action requires confirmation.
- Mentions whether an instruction came from untrusted content.
- Does not invent access that was not shown in the prompt.

If coder agreement is used, the agreement procedure and dispute-resolution
process must be specified before analysis. No agreement result exists yet.

## Consent, Privacy, and Ethics Notes

Before running the study:

- Obtain the applicable institutional review, exemption determination, or other
  required approval before recruitment.
- Provide plain-language informed consent describing the study purpose,
  estimated time, voluntary participation, compensation if any, risks,
  benefits, data handling, and withdrawal process.
- State that all tasks and data objects are synthetic and that no real personal
  account, agent, mailbox, filesystem, browser profile, payment method, or
  credential will be accessed.
- Do not collect real personal data beyond the minimum needed for study
  administration and compensation.
- Store responses with participant identifiers separated or removed according
  to the approved protocol.
- Avoid asking participants to reveal private events, documents, contacts,
  purchase history, credentials, or security incidents.
- Debrief participants about synthetic adversarial prompts and explain that the
  study examines permission-prompt interpretation.
- Treat any accessibility needs, withdrawal requests, or distress reports
  according to the approved protocol.

The study software, if built, should not connect to real email, file, browser,
calendar, payment, messaging, or device-management APIs.

## Analysis Plan

The future analysis should compare the three prompt conditions using the same
task items and answer keys. Candidate comparisons include:

- Task-scoped permission bundles versus raw tool permissions.
- Task-scoped permission bundles versus generic warnings.
- Raw tool permissions versus generic warnings.
- Differences by question type, such as allowed-data recognition, blocked-data
  recognition, external-disclosure recognition, and confirmation-gate
  recognition.
- Differences between closed-form correctness and subjective confidence.

The analysis plan must be finalized before data collection. This document does
not report or imply any expected direction, effect size, statistical
significance, or participant outcome.

## Claim Boundaries

Allowed current claim:

- PAPF has a planned protocol for measuring non-expert understanding of
  task-scoped permission bundles.

Disallowed until data exists:

- PAPF is understandable to non-experts.
- PAPF improves comprehension compared with raw tool permissions.
- PAPF improves comprehension compared with generic warnings.
- PAPF reduces consent fatigue or consent burden.
- PAPF helps users make safer permission choices.
- PAPF audit summaries are interpretable by non-experts.

These disallowed statements can only become evidence-backed claims after a
properly reviewed study is run, analyzed, and reported with limitations.
