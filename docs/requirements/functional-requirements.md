# Reliora Functional Requirements

## Purpose

This document defines the functional behaviour Reliora must provide.

Each requirement has a stable identifier so that implementation code, tests, evaluation cases, architecture decisions, and evidence can reference the same behavioural contract.

---

## Request and Session Handling

### FR-001 — Request Identification

Every accepted customer request must receive a unique
equest_id.

The identifier must be propagated through routing, agent execution, tool invocation, telemetry, and relevant persistence boundaries.

### FR-002 — Session Identification

Conversation turns belonging to the same interaction must be associated with a session_id.

Session identity must remain distinct from request identity.

### FR-003 — Operation Identification

Every side-effecting business operation must use a stable operation_id that identifies the logical action independently of individual retries or transport requests.

---

## Routing

### FR-004 — Intent Classification

Every accepted customer message must be classified into exactly one top-level intent:

- BUG
- PLATFORM
- OTHER

Routing results must be represented through a machine-verifiable contract rather than relying solely on free-form text.

### FR-005 — Knowledge Coverage Classification

A request classified as PLATFORM must undergo a separate knowledge-coverage decision:

- SUPPORTED
- UNSUPPORTED

Intent classification and knowledge coverage must remain logically distinct.

### FR-006 — Unsupported Request Handling

Requests classified as OTHER, unsupported platform questions, or requests that cannot be handled safely must transition to the human-handoff workflow.

---

## Bug Report Workflow

### FR-007 — Required Bug Information

Before creating a bug ticket, the system must have all three required fields:

- description
- steps_to_reproduce
- environment

### FR-008 — Incremental Collection

When required bug information is missing, the system must collect the missing information conversationally.

The workflow must not create the ticket before all required fields satisfy the defined validation contract.

### FR-009 — Tool Authorization Gate

A proposed bug-report tool call must pass deterministic validation before the side effect is authorized.

The validation layer must not depend solely on the LLM deciding that its own arguments are valid.

### FR-010 — Exactly-One Logical Ticket

A single logical bug-report operation must create no more than one ticket, even when the caller retries after a timeout or ambiguous response.

### FR-011 — Idempotent Retry Result

When an identical logical operation is retried with the same operation_id, the system must return the existing operation result rather than creating a second ticket.

### FR-012 — Idempotency Conflict Detection

If the same operation_id is reused with materially different operation data, the system must reject or explicitly flag the conflict rather than silently treating it as the original operation.

### FR-013 — Ticket Confirmation

The customer may only be told that a ticket was successfully created when the backend operation has returned a confirmed successful result.

A ticket identifier must never be fabricated by the model.

---

## Platform Knowledge Workflow

### FR-014 — Grounded Platform Answers

Supported platform questions must be answered only from the approved knowledge source available to the current deployment.

### FR-015 — Unsupported Knowledge Handoff

If approved knowledge does not support an answer, the system must not invent a policy or platform fact.

It must transition to the human-handoff workflow.

### FR-016 — Knowledge Version Provenance

Responses that depend on approved platform knowledge must be attributable to the relevant knowledge or FAQ version.

---

## Human Handoff

### FR-017 — Structured Handoff

Human escalation must produce a structured handoff object rather than only displaying a phone number or generic redirect.

The handoff must support, at minimum:

- handoff reason;
- detected intent;
- conversation summary;
- information already collected;
- attempted actions;
- failed actions where applicable;
- recommended support queue;
- correlation/request identifier;
- relevant deployment provenance.

### FR-018 — Handoff Data Minimisation

The handoff package must exclude hidden reasoning, unnecessary sensitive information, internal system instructions, and other information not required by the receiving support workflow.

---

## Contracts and Validation

### FR-019 — Typed Boundary Contracts

Machine-to-machine boundaries must use explicit typed or schema-based contracts.

Examples include routing results, tool arguments, tool results, handoff objects, and evaluation records.

### FR-020 — Invalid Input Handling

Malformed, oversized, unsupported, or contract-invalid input must be rejected or safely handled before it can cause an unauthorized business side effect.

### FR-021 — Structured Model Output

Where model-generated data is consumed programmatically, the output must conform to a defined schema before downstream business logic uses it.

Native model-provider structured-output capabilities may be used when they strengthen this requirement, but they do not replace application-side validation.

---

## Safety and Output Control

### FR-022 — Internal Information Protection

Customer-facing responses must not expose:

- hidden system instructions;
- internal route labels unless deliberately designed for users;
- hidden reasoning or chain-of-thought;
- secrets or credentials;
- internal authorization logic.

### FR-023 — Untrusted Text Boundary

Customer-provided text, retrieved text, and tool-returned text must be treated as untrusted data.

Untrusted natural-language content must not independently authorize privileged actions or override system policy.

---

## Evaluation

### FR-024 — Deterministic Behavioural Evaluation

Hard behavioural requirements must be testable through deterministic evaluators whenever exact software verification is possible.

### FR-025 — Generative Quality Evaluation

Qualities requiring subjective judgement may use LLM-based evaluation separately from deterministic behavioural evaluation.

### FR-026 — Versioned Evaluation Data

Evaluation datasets must have explicit versions and documented purpose.

Gold, challenge/adversarial, workflow-regression, and experimental datasets must not be silently mixed.

### FR-027 — Regression Gate

A candidate release must satisfy the defined behavioural regression gate before promotion.

A high aggregate LLM-judge score must not override a failed critical deterministic invariant.

---

## Release and Provenance

### FR-028 — Deployment Provenance

Operational records must make it possible to determine which relevant model, prompt, routing configuration, knowledge version, and application version served a request.

### FR-029 — Rollback

A previously validated deployment version must be recoverable without reconstructing its behaviour manually.

---

## Feedback

### FR-030 — Human Correction Capture

Human corrections from reviewed handoffs or test reviews must be representable as feedback events.

### FR-031 — Reviewed Dataset Promotion

Human feedback must not automatically become evaluation ground truth.

It must undergo review before promotion into a versioned evaluation dataset.

---

## Current Status

These requirements describe the intended P1-S2 behavioural contract.

They are currently **TARGET requirements** unless implementation or evidence explicitly establishes a stronger evidence classification.
