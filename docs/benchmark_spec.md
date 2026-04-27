# Benchmark Specification

## Benchmark goal

The benchmark should measure whether a consumer AI agent can complete realistic personal-assistant tasks while respecting task-scoped permissions. It should expose the tradeoff between task success and privacy/security outcomes, not just end-task completion.

## Task categories

- Email triage and drafting
- Calendar scheduling and rescheduling
- Contacts lookup and selective sharing
- File retrieval and summarization
- Browser-based information gathering
- Travel planning or booking preparation
- Messaging or follow-up coordination
- Payments or purchase-preparation flows
- Cloud or device administration tasks

## Data categories

Each benchmark task should label data as:

- Necessary data: required for successful completion
- Unnecessary data: available in the environment but not needed
- Dangerous data: highly sensitive content that should not be accessed or exposed
- Derived data: task-relevant artifacts produced from allowed inputs

Illustrative data classes:

- Email bodies, attachments, and metadata
- Calendar events and attendee lists
- Contact records
- Local or cloud files
- Browser page contents
- Payment details
- Authentication or account-management surfaces

## Task schema

Each benchmark instance should define:

- User-visible task
- Initial environment and synthetic data setup
- Required capabilities
- Allowed tool calls
- Forbidden tool calls
- Necessary data items
- Unnecessary but tempting data items
- Dangerous data items
- Expected policy outcome
- Success criteria

## Allowed and forbidden tool calls

Tool permissions should be explicit and machine-checkable. Examples:

- Allowed: read a specific email thread, query a named calendar range, open a listed file, draft but not send a reply
- Forbidden: broad mailbox search, reading unrelated files, exporting contacts, sending data to unapproved external endpoints

The benchmark should test both obvious denials and subtle overreach, including attempts to use a broad tool when a narrow tool would suffice.

## Attack cases

- Prompt injection from email or web content
- Data exfiltration attempts through agent outputs or external actions
- Confused-deputy behavior where one tool is used to access data for another purpose
- Over-broad search or enumeration of personal data stores
- Consent laundering through vague or misleading permission requests

## Evaluation metrics

Primary metrics:

- Task success
- Necessary access rate
- Over-access rate
- Exfiltration rate
- False allow
- False deny
- Consent burden
- Recovery quality
- Auditability

Secondary metrics are `TODO`. Metric definitions should be formalized before experiments are run.

## Benchmark constraints

- Use synthetic personal data by default
- Avoid real credentials and personal records
- Keep policy outcomes deterministic where possible
- Separate benchmark definitions from agent implementation logic

## Open design questions

- Whether the first benchmark release should focus on a narrow domain slice or a broader cross-domain suite
- How to score partial task completion under strict denials
- How to simulate realistic but safe injection and exfiltration attempts
