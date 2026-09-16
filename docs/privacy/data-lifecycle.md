# Reliora Data Lifecycle and Retention Policy

## 1. Purpose

This document defines how Reliora handles data across its lifecycle:

```text
collection
→ validation
→ processing
→ persistence
→ telemetry
→ evaluation
→ evidence
→ retention
→ deletion
```

The policy applies to customer input, model inputs and outputs, tool
arguments, backend records, logs, traces, evaluation data, and generated
evidence used to operate and assess the system.

Reliora is designed to support customer workflows, not to build a general
purpose profile of customers. Data handling must therefore be limited to the
purpose, scope, and retention period required by the workflow.

## 2. Governing Principles

Reliora follows these principles:

1. Collect the minimum information needed for the requested workflow.
2. Treat customer-provided content as untrusted input.
3. Validate data before it reaches persistence or side-effecting tools.
4. Keep operational telemetry smaller and less sensitive than source input.
5. Separate customer records from evaluation and development data.
6. Use synthetic or redacted examples where real content is unnecessary.
7. Define retention before creating a persistent store or evidence artifact.
8. Make deletion and teardown an explicit operational action.
9. Verify enforcement with tests, configuration review, and runtime evidence.
10. Do not retain hidden model reasoning or ask the model to produce it.

## 3. Data Categories

### 3.1 Customer Input

Customer input is the message or structured information supplied for a support
interaction. It may contain personal, confidential, or unrelated information.

The application must treat it as untrusted content and must not assume that
every field is necessary for the requested operation.

Customer input may be passed to a model only when it is needed to produce the
next response or determine the next permitted workflow step.

### 3.2 Model Input and Output

Model input includes the system instructions, approved policy or knowledge
context, relevant customer content, and deterministic state needed for the
current step.

Model output is proposed data. It is not an authorization decision and must
not directly create a side effect or become trusted execution metadata.

Model output should be retained only when it is needed to explain an outcome,
support a defined evaluation, or investigate a failure. Hidden reasoning is
not a required product or operational record.

### 3.3 Tool Arguments and Results

Tool arguments can cross a trust boundary and may cause a backend mutation.
They must be schema-validated, size-limited, and authorized deterministically.

Tool results must be treated as the source of truth for backend outcomes.
Only validated results may establish that a side effect succeeded.

Raw tool payloads should not be copied into every log or trace. Store a safe
summary, outcome, operation identifier, and relevant error classification when
that is sufficient for operations.

### 3.4 Business Records

Business records include bug reports, operation results, status values, and
identifiers needed to support the defined customer workflow.

Records must contain the fields required for the workflow and no unrelated
conversation history by default. Free-text fields must have explicit size
limits and should be normalized where that improves safety or consistency.

### 3.5 Operational Telemetry

Operational telemetry includes logs, metrics, traces, correlation identifiers,
timings, route decisions, validation outcomes, and dependency outcomes.

Telemetry is for operating the system. It is not a second copy of the full
customer conversation. Sensitive values must be redacted, omitted, hashed, or
replaced with a safe identifier unless their presence is specifically required
for diagnosis.

### 3.6 Evaluation Data

Evaluation data includes test cases, expected behaviours, scorer inputs,
regression results, and dataset metadata. Evaluation data must be versioned
and its provenance must be recorded.

Real customer content must not enter a gold dataset by default. When a real
case is necessary, it must be minimized, redacted, approved, and labelled with
its source and permitted use.

### 3.7 Evidence and Reports

Evidence artifacts document what was measured, observed, tested, or inferred.
They must state the evidence type and avoid reproducing sensitive payloads.

Evidence should preserve identifiers and summaries needed to reproduce a
finding without retaining more source data than the finding requires.

## 4. Collection

Collection begins when input is received by the application boundary.

The application should collect:

- the customer request needed for the active workflow;
- required structured fields;
- a request or correlation identifier;
- the minimum context needed for authorization and routing;
- operational metadata needed to classify the outcome.

The application should not collect:

- unnecessary identity attributes;
- credentials, access tokens, or private keys;
- complete prompts or responses when a safe summary is sufficient;
- hidden chain-of-thought or private model reasoning;
- unrelated conversation history;
- sensitive values solely for convenience in debugging.

Input limits must be enforced before expensive model or tool work. Rejected
input should produce a safe validation result and should not be persisted as a
complete raw payload unless a defined security investigation requires it.

## 5. Validation and Classification

Input is validated before it is used for a side effect. Validation includes
syntax, type, size, required fields, allowed values, and semantic constraints.

The system should classify data according to its handling need:

| Class | Handling expectation |
|---|---|
| Public or synthetic | May be used in tests and documentation when labelled |
| Operational | Retain only for the defined operational purpose |
| Customer-sensitive | Minimize, restrict access, and redact from telemetry |
| Secret or credential | Never persist in application records or logs |
| Evaluation | Version, label, and protect dataset provenance |

Classification must not be treated as a substitute for access control. A
record can require both classification and a specific permitted purpose.

## 6. Processing

Processing must be purpose-bound. Each model call, routing decision, and tool
call should have a documented reason within the active workflow.

The system must keep customer content separate from system authority. User
instructions cannot change the data policy, authorization boundary, or logging
requirements.

Only the context needed for the current step should be supplied to a model.
Context should be assembled deterministically where practical and should not
include unrelated retained records.

Model output must pass through deterministic validation before it is returned
to the customer or used by application logic. A model must not choose what
data is retained, how long it is retained, or whether a tool is authorized.

## 7. Persistence

Persistence requires an identified purpose, owner, access boundary, and
retention decision. New persistent fields should be reviewed against this
policy before implementation.

Records must use stable operation identifiers where retries can create a side
effect. Idempotency metadata should not contain raw customer content when an
opaque identifier is sufficient.

Database records should be scoped to the smallest required tenant, workflow,
or operation boundary. Access should be limited to the component responsible
for the corresponding action.

Persistence failures must not cause the application to claim that a business
operation succeeded. Ambiguous outcomes require explicit classification and
safe handling.

## 8. Logging and Tracing

Logs should answer operational questions such as:

- which workflow and version ran;
- whether validation succeeded;
- which approved route was selected;
- whether a tool was authorized;
- whether the backend succeeded or failed;
- how long each dependency took;
- which safe correlation identifier links the events.

Logs should not answer those questions by copying the entire request, prompt,
model response, or backend payload.

Before a field is added to telemetry, the owner must identify its operational
purpose and confirm that a less sensitive representation is insufficient.

Secrets, credentials, authorization headers, private keys, and access tokens
must never be logged. Customer-sensitive values must be redacted or omitted.

Traces must follow the same minimization rule as logs. A trace span may carry
a safe status and timing value without carrying the source payload.

## 9. Evaluation and Development Use

Development and evaluation environments should use synthetic, generated, or
redacted content whenever that is sufficient to test behaviour.

Evaluation datasets must include:

- dataset name and version;
- source and provenance;
- permitted purpose;
- expected sensitivity class;
- reviewer or approval record where required;
- deletion or review date.

Experimental outputs must not silently become production data or gold
evaluation truth. Dataset changes must identify what changed and why.

Failure examples may be retained to improve the system, but they must be
minimized to the fields needed to reproduce the failure and must not include
secrets or unnecessary customer content.

## 10. Access and Use

Access follows least privilege and purpose limitation. A role that can operate
the service does not automatically need access to evaluation datasets or raw
customer records.

Access to sensitive data should be:

- granted to a named role or service identity;
- limited to the required resource and action;
- auditable through provider and application records;
- removed when the operational need ends;
- reviewed when the workflow or data classification changes.

Local development copies must not be treated as permanent archives. They must
be excluded from source control, protected on the developer workstation, and
removed when no longer required.

## 11. Retention Schedule

The following schedule is the default policy for the current development and
evaluation scope. A longer period requires a documented reason and owner.

| Data type | Default retention decision |
|---|---|
| Rejected raw input | Do not persist; retain only a safe error summary |
| Customer workflow record | Retain only for the approved workflow period |
| Tool outcome summary | Retain with the related operation record |
| Raw logs and traces | Short operational period; redact before storage |
| Metrics and aggregates | Retain while useful for service operations |
| Evaluation datasets | Versioned; review at each release or dataset change |
| Evaluation results | Retain as release evidence while the release is supported |
| Failure evidence | Retain only while needed to reproduce or remediate |
| Temporary build artifacts | Delete after the build or investigation |
| Local development exports | Delete after the task and never commit them |

The schedule is a decision framework, not permission to retain everything in a
category. The smallest useful representation and the shortest useful period
remain the default.

## 12. Deletion and Teardown

Deletion must remove the data from the active store and from derived copies
that are within the project’s control, including local exports, generated
reports, temporary artifacts, and test fixtures where applicable.

When a managed service owns backups or delayed deletion, the project must
record that limitation and follow the provider’s documented deletion controls.

Teardown must include:

- application records created for the experiment;
- telemetry and temporary evidence;
- local build and packaging directories;
- evaluation exports no longer required;
- cloud resources and associated retained data;
- access grants created only for the experiment.

Deletion evidence should record the scope, date, actor or automation identity,
and any provider limitation without reproducing the deleted content.

## 13. Incident and Exception Handling

If sensitive data is logged, committed, copied to an unintended store, or
retained beyond its approved period, the issue must be classified as an
incident or policy exception.

The response should:

1. stop further propagation where practical;
2. restrict access to the affected data;
3. identify stores and derived copies;
4. remove or rotate the affected material;
5. record the scope and evidence of the response;
6. update controls or tests that failed to prevent the issue.

Exceptions must name an owner, purpose, scope, expiration, and compensating
control. An undocumented exception is not a retention policy.

## 14. Verification

Privacy controls are verified through a combination of:

- schema and boundary tests;
- logging and redaction tests;
- secret scanning;
- configuration and IAM review;
- retention and teardown checks;
- evaluation dataset review;
- inspection of generated artifacts;
- cloud integration evidence when local mocks are insufficient.

Local verification does not prove cloud enforcement. Provider retention,
transport, access, and deletion behaviour must be labelled as pending until
demonstrated in the relevant environment.

### Current State

| Control | Status |
|---|---|
| repository history scan | LOCAL VERIFIED — GITLEAKS, 0 FINDINGS |
| CI secret scan | PENDING |
| Secret History Scan | LOCAL VERIFIED — 0 FINDINGS |

Evidence should identify the control, test or inspection performed, result,
environment, and remaining limitation. Claims must not be stronger than the
evidence supporting them.

## 15. Ownership

The application owner is responsible for applying this policy to new data
flows and for keeping the retention schedule current.

Operations owns telemetry configuration, access review, and deletion or
teardown procedures.

Evaluation owners are responsible for dataset provenance, sensitivity labels,
review, and removal of obsolete artifacts.

Security review is required when a new trust boundary, sensitive data class,
external provider, or side-effecting workflow is introduced.

## 16. Final Principle

Every data flow should be explainable in terms of purpose, minimum necessary
content, access, retention, and deletion.

```text
collect less
→ persist deliberately
→ log minimally
→ retain explicitly
→ verify enforcement
→ delete intentionally
```