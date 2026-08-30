# Reliora Failure Mode Analysis

## Purpose

This document identifies credible failure modes in Reliora, their effects, how they should be detected, how the system should respond, and how the failures will eventually be tested.

The purpose is not to predict every possible outage.

It is to answer engineering questions such as:

> What can fail?

> What happens when it fails?

> How would we know?

> What should Reliora do automatically?

> What would an engineer investigate?

> How will we prove the recovery behaviour works?

Reliora uses a lightweight failure-mode analysis rather than assigning arbitrary numerical risk scores before operational evidence exists.

---

# Analysis Model

Each important failure mode should eventually have:

**Failure Mode**

→ Trigger or Cause

→ Customer / System Effect

→ Detection Signal

→ Automatic System Response

→ Operator Diagnostic Path

→ Recovery

→ Verification Test

→ Evidence

Failure status uses Reliora's evidence discipline.

---

# Failure Register

| ID | Failure Mode | Primary Effect | Expected Detection | Initial Response |
|---|---|---|---|---|
| FM-001 | Incorrect intent routing | Wrong workflow selected | Routing evaluation / trace | Safe handoff where ambiguity is detected |
| FM-002 | Incorrect knowledge coverage | Unsupported answer or unnecessary handoff | Coverage evaluation | Handoff rather than fabricate |
| FM-003 | Malformed model output | Downstream contract failure | Schema validation | Reject / retry within bounds / handoff |
| FM-004 | Premature tool proposal | Invalid ticket creation attempt | Tool authorization telemetry | Block execution |
| FM-005 | Duplicate side effect | Multiple tickets for one logical operation | Operation-ID persistence checks | Return original result |
| FM-006 | Ambiguous side-effect outcome | Unknown ticket state | Timeout + operation lookup | Reconcile using operation ID |
| FM-007 | Agent/model dependency failure | Response unavailable or delayed | Invocation error / latency | Bounded retry or handoff |
| FM-008 | AgentCore Gateway failure | Tool unavailable | Gateway/tool error | Bounded retry or handoff |
| FM-009 | Lambda execution failure | Ticket not processed | Lambda error telemetry | Safe failure / retry policy |
| FM-010 | DynamoDB persistence failure | Ticket not stored or result unavailable | Persistence error | Bounded retry / safe failure |
| FM-011 | Telemetry failure | Reduced diagnostic visibility | Missing expected telemetry | Preserve customer workflow where safe |
| FM-012 | IAM or authorization failure | Legitimate operation blocked | AccessDenied / authorization telemetry | Fail closed |
| FM-013 | Prompt-injection attempt | Policy bypass attempt | Security/adversarial signal | Block privileged behaviour |
| FM-014 | Unbounded execution or retry amplification | Latency/cost/resource exhaustion | Iteration, retry, token, concurrency metrics | Enforce limits |
| FM-015 | Stale or incorrect approved knowledge | Incorrect customer information | Knowledge-version evaluation | Roll back/update knowledge |
| FM-016 | Evaluation regression | Unsafe release appears acceptable | CI/evaluation gate | Block promotion |
| FM-017 | Bad deployment/configuration | Previously working behaviour degrades | Smoke tests / version metrics | Roll back |
| FM-018 | Sensitive data enters logs | Privacy exposure | Redaction/security tests | Stop unnecessary logging and remediate |

---

# Detailed Failure Modes

## FM-001 — Incorrect Intent Routing

### Scenario

A customer request is routed to the wrong top-level workflow.

Examples include:

- a bug report classified as PLATFORM;
- a platform question classified as BUG;
- an unsupported request incorrectly treated as automatable.

### Effect

Potential consequences include:

- irrelevant answers;
- unnecessary handoff;
- incorrect information collection;
- proposed tool invocation for the wrong workflow.

### Detection

Useful signals include:

- routing confusion matrix;
- per-class precision and recall;
- route recorded in request provenance;
- workflow mismatch during evaluation.

### Automatic Response

Low-confidence or invalid routing results should reduce autonomy and transition to a safe workflow rather than force a potentially unsafe action.

### Diagnosis

Inspect:

`request_id`

→ input validation

→ routing output

→ routing version

→ model or classifier version

→ downstream workflow chosen.

### Verification

Use:

- routing-gold evaluation;
- routing-challenge evaluation;
- ambiguous-input tests.

**Current status: TARGET**

---

## FM-002 — Incorrect Knowledge Coverage Decision

### Scenario

A PLATFORM request is incorrectly classified as supported or unsupported.

### Effect

False `SUPPORTED` may lead to fabricated or ungrounded policy information.

False `UNSUPPORTED` may create unnecessary human escalations.

### Detection

Measure:

- knowledge-coverage precision;
- knowledge-coverage recall;
- unsupported-answer rate;
- unnecessary-handoff rate.

### Automatic Response

When support cannot be established safely, prefer structured handoff over unsupported generation.

### Verification

Test:

- clearly supported questions;
- clearly unsupported questions;
- misleading wording;
- changed-policy questions.

**Current status: TARGET**

---

## FM-003 — Malformed Model Output

### Scenario

A model produces output that does not satisfy the expected machine-readable contract.

Examples include:

- invalid JSON;
- missing required field;
- unexpected enum;
- incorrect data type;
- excessive field length.

### Effect

Downstream application logic may fail or receive unsafe input.

### Detection

Typed validation must fail before downstream execution.

### Automatic Response

Depending on workflow state:

1. reject the output;
2. perform a bounded regeneration attempt where justified;
3. transition to safe handoff if a valid result cannot be obtained.

### Verification

Schema and boundary-value tests.

**Current status: TARGET**

---

## FM-004 — Premature Tool Proposal

### Scenario

The model proposes bug-ticket creation before all required information is complete.

### Effect

An incomplete or invalid business record could be created.

### Detection

The deterministic authorization layer compares workflow state against the required tool contract.

### Automatic Response

The tool call is blocked.

The workflow continues collecting the missing required information.

### Verification

Contract tests deliberately propose tool calls with incomplete workflow state.

**Current status: TARGET**

---

## FM-005 — Duplicate Side Effect

### Scenario

A successful ticket creation is retried because the original response was lost or the caller timed out.

### Effect

One logical customer action could create multiple tickets.

### Detection

The backend detects reuse of the same `operation_id`.

### Automatic Response

The existing successful operation result is returned.

A new ticket must not be created.

### Verification

Fault test:

1. perform ticket creation;
2. simulate loss of the successful response;
3. retry using the same `operation_id`;
4. inspect persistence;
5. confirm exactly one logical ticket exists.

**Current status: TARGET**

---

## FM-006 — Ambiguous Side-Effect Outcome

### Scenario

Reliora cannot determine whether ticket creation succeeded.

This may occur when the backend completes an operation but the response path fails.

### Effect

The model may be tempted to either:

- falsely claim success; or
- retry blindly and create duplicate state.

### Detection

A side-effect invocation times out or returns an indeterminate result.

### Automatic Response

Reliora must reconcile the logical operation through `operation_id`.

The model must not invent the outcome.

### Recovery

If authoritative state cannot be determined safely, transition to human support with the ambiguity recorded.

### Verification

Fault-injection test around the persistence-response boundary.

**Current status: TARGET**

---

## FM-007 — Agent or Model Dependency Failure

### Scenario

The selected model or managed agent execution layer:

- times out;
- returns an error;
- becomes temporarily unavailable;
- exceeds a defined execution bound.

### Effect

Customer response is delayed or unavailable.

### Detection

Capture:

- invocation result;
- latency;
- error category;
- model identifier;
- retry count.

### Automatic Response

Use bounded retry only for defined transient failures.

Otherwise transition to a safe failure or human-support path.

### Verification

Controlled dependency failure simulation where practical.

**Current status: TARGET**

---

## FM-008 — AgentCore Gateway Failure

### Scenario

AgentCore Gateway cannot successfully execute the approved tool invocation.

Possible causes include:

- service error;
- configuration error;
- authorization error;
- unavailable downstream target.

### Effect

Bug-ticket creation cannot complete.

### Detection

Tool invocation telemetry and correlated Gateway errors.

### Diagnosis

Trace:

`request_id`

→ `operation_id`

→ authorization result

→ Gateway invocation

→ target invocation result.

### Automatic Response

Apply bounded retry only to retryable failures.

Otherwise hand off without claiming ticket creation succeeded.

**Current status: TARGET**

---

## FM-009 — Lambda Failure

### Scenario

The bug-report Lambda:

- raises an exception;
- rejects valid input incorrectly;
- exceeds its timeout;
- loses permission to access required resources.

### Effect

Ticket creation fails or becomes ambiguous.

### Detection

Lambda execution status and correlated application telemetry.

### Diagnosis

Inspect:

- request ID;
- operation ID;
- validation result;
- Lambda error category;
- downstream persistence result.

### Recovery

Depends on failure classification.

Retry must remain idempotent.

**Current status: TARGET**

---

## FM-010 — DynamoDB Persistence Failure

### Scenario

DynamoDB cannot complete the required operation.

Possible causes include:

- authorization failure;
- throttling;
- malformed key;
- conditional-write conflict;
- service failure.

### Effect

Ticket state may not be persisted or may require reconciliation.

### Detection

Persistence result and explicit error categorization.

### Automatic Response

Retry only where the failure is classified as safely retryable.

Idempotency must remain valid across retries.

### Verification

Integration and fault tests.

**Current status: TARGET**

---

## FM-011 — Telemetry Failure

### Scenario

Logs, metrics, or traces are incomplete or unavailable while the customer workflow continues operating.

### Effect

The system may still function but engineers lose diagnostic visibility.

### Detection

Expected telemetry events or traces are missing.

### Principle

Observability failure must not automatically become customer-facing application failure unless the missing telemetry is itself required for safe operation.

### Recovery

Restore telemetry and determine whether any operational evidence was lost.

**Current status: TARGET**

---

## FM-012 — IAM or Authorization Failure

### Scenario

A workload loses permission to perform a required authorized action.

### Effect

A valid business workflow fails.

### Detection

Explicit authorization or `AccessDenied` errors.

### Automatic Response

Fail closed.

Reliora must not bypass the authorization boundary.

### Diagnosis

Determine:

- which identity executed the request;
- which action was attempted;
- which resource was targeted;
- which policy allowed or denied it.

### Verification

IAM review and selected negative authorization tests.

**Current status: TARGET**

---

## FM-013 — Prompt Injection

### Scenario

A customer tries to manipulate Reliora into:

- ignoring protected instructions;
- exposing internal information;
- invoking unauthorized tools;
- overriding workflow policy.

### Effect

Potential policy bypass or information exposure.

### Detection

Adversarial evaluation and prohibited-behaviour telemetry.

### Automatic Response

Protected policies and deterministic authorization remain authoritative.

### Verification

Prompt-injection regression suite.

**Current status: TARGET**

---

## FM-014 — Unbounded Execution or Retry Amplification

### Scenario

One difficult request or one failing dependency causes excessive:

- model iterations;
- tokens;
- tool calls;
- retries;
- execution time.

At higher concurrency, this behaviour may amplify across many requests.

### Effect

Potential:

- latency degradation;
- quota exhaustion;
- downstream overload;
- excessive cost;
- denial of service;
- denial of wallet.

### Detection

Monitor:

- model calls per request;
- tokens per request;
- tool calls per request;
- retries per request;
- request duration;
- concurrent executions;
- throttling;
- cost indicators.

### Automatic Response

Enforce explicit execution limits and bounded retry policies.

### Verification

Adversarial and controlled workload testing.

**Current status: TARGET**

---

## FM-015 — Stale Approved Knowledge

### Scenario

The approved FAQ or policy source contains information that is no longer current.

### Effect

Reliora may generate a grounded answer that is technically grounded but factually outdated.

### Detection

Knowledge-version provenance and policy-change regression testing.

### Recovery

Deploy a reviewed knowledge update and rerun relevant evaluation cases.

### Verification

Versioned policy-change tests.

**Current status: TARGET**

---

## FM-016 — Evaluation Regression

### Scenario

A candidate version improves an aggregate quality score while introducing a critical behavioural defect.

### Effect

Unsafe behaviour may be promoted as an improvement.

### Detection

Separate deterministic behavioural gates from generative-quality scoring.

### Automatic Response

Critical invariant failure blocks release.

### Verification

Known Stage-1 regression cases and future defect reproductions.

**Current status: TARGET**

---

## FM-017 — Bad Deployment or Configuration

### Scenario

A deployment introduces an incorrect:

- application version;
- prompt;
- routing configuration;
- model configuration;
- knowledge version;
- infrastructure change.

### Effect

Previously validated behaviour degrades.

### Detection

Deployment provenance, smoke tests, regression tests, and operational telemetry.

### Recovery

Return to a previously validated version.

### Verification

Controlled rollback exercise later in the project.

**Current status: TARGET**

---

## FM-018 — Sensitive Data Leakage Through Telemetry

### Scenario

Customer-sensitive or protected values are copied into logs or traces unnecessarily.

### Effect

Privacy and security exposure.

### Detection

Representative sensitive-value tests and log inspection.

### Automatic / Preventive Controls

Use:

- field allowlists;
- redaction;
- structured telemetry;
- data minimisation;
- bounded retention.

### Verification

Send known marker values and verify they do not appear in application-controlled telemetry where prohibited.

**Current status: TARGET**

---

# Cascading Failure

Failures must not be analysed only in isolation.

One failure may trigger another.

Example:

Gateway timeout

→ application retry

→ repeated model/tool execution

→ increased concurrency

→ additional throttling

→ more retries

→ increased latency and cost.

This is a retry-amplification feedback loop.

Reliora must therefore consider:

- retry ownership;
- retry limits;
- backoff;
- concurrency;
- timeout hierarchy;
- idempotency;

as a connected resilience problem.

---

# Scaling Failure Hypotheses

Reliora does not currently have measured production-scale workload evidence.

The following are therefore hypotheses to investigate rather than claims.

## SH-001 — Model or Agent Quota

Managed model or agent request limits may become a throughput constraint before serverless compute or persistence.

**Evidence status: HYPOTHESIS / not yet measured**

## SH-002 — Model Latency

Model inference may dominate end-to-end request latency.

**Evidence status: HYPOTHESIS / not yet measured**

## SH-003 — Tool Concurrency

Increasing request concurrency may cause Gateway, Lambda, or downstream throttling.

**Evidence status: HYPOTHESIS / not yet measured**

## SH-004 — Retry Amplification

Transient failures may produce disproportionately higher load when retries occur at multiple layers.

**Evidence status: HYPOTHESIS / not yet measured**

## SH-005 — Cost Before Compute Capacity

The economically acceptable throughput limit may be reached before a technical service-capacity limit.

**Evidence status: HYPOTHESIS / not yet measured**

## SH-006 — Observability Volume

Trace and logging volume may become operationally or economically significant at higher request rates.

**Evidence status: HYPOTHESIS / not yet measured**

---

# Scaling Experiment Design

Controlled workload experiments should progressively increase concurrency rather than attempt to simulate fictitious enterprise traffic.

For each workload level, measure where practical:

| Measurement | Purpose |
|---|---|
| Successful requests | Reliability |
| Failed requests | Reliability |
| p50 latency | Typical latency |
| p95 latency | Tail behaviour |
| Model latency | AI-serving bottleneck |
| Tool latency | Tool-path bottleneck |
| Lambda duration | Compute behaviour |
| DynamoDB latency/errors | Persistence behaviour |
| Throttling events | Capacity boundary |
| Model calls/request | Agent efficiency |
| Tool calls/request | Workflow efficiency |
| Retries/request | Failure amplification |
| Tokens/request | Model usage |
| Estimated cost/request | Unit economics |

The first demonstrated constraint should be recorded as **EXPERIMENTAL** or **MEASURED**, depending on the measurement method.

Reliora must not claim that a particular component is the first scaling bottleneck before the experiment is performed.

---

# Failure Evidence Principle

A failure-control claim should eventually follow:

**Failure**

→ **Detection**

→ **Mitigation**

→ **Test**

→ **Evidence**

For example:

`FM-005 Duplicate Side Effect`

→ same `operation_id` detected

→ conditional persistence / idempotent result replay

→ response-loss retry test

→ one stored logical ticket

Only then should the control be described as demonstrated.

---

# Current Status

This document represents the initial **TARGET failure model**.

Failure modes, scaling hypotheses, and recovery behaviour will be refined as Reliora produces experimental and measured evidence.