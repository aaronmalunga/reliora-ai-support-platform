# Reliora Diagnostic Playbook

## Purpose

This playbook defines a repeatable approach for diagnosing Reliora failures.

It is intended to reduce diagnosis based on intuition alone by establishing a consistent path from customer symptom to technical cause.

The playbook will evolve as actual telemetry, dashboards, alarms, and operational evidence are implemented.

---

# Core Diagnostic Principle

Start with the customer-visible symptom and follow the request through the system using correlation identifiers.

The preferred diagnostic path is:

**Symptom**

→ `request_id`

→ `session_id` where relevant

→ `operation_id` for side effects

→ routing decision

→ model / agent execution

→ deterministic validation

→ tool invocation

→ backend execution

→ persistence

→ customer response

Do not begin by randomly searching unrelated logs.

---

# Identifiers

## request_id

Identifies one individual request.

Use it to correlate the major processing steps for one request.

## session_id

Identifies the broader customer conversation.

Use it when diagnosis requires multiple turns.

## operation_id

Identifies one logical side-effecting business operation.

Use it to diagnose:

- retries;
- duplicate-action concerns;
- ambiguous outcomes;
- idempotency conflicts.

---

# Standard Triage Procedure

When investigating an incident or failed request:

1. capture the customer-visible symptom;
2. identify the approximate time;
3. obtain the `request_id` if available;
4. determine the route selected;
5. determine whether model execution succeeded;
6. inspect deterministic validation;
7. determine whether a tool was proposed;
8. determine whether that tool was authorized;
9. inspect Gateway execution if applicable;
10. inspect Lambda execution if applicable;
11. inspect DynamoDB state if applicable;
12. inspect retry and `operation_id` history;
13. identify the failure category;
14. determine whether the system recovered, handed off, or failed;
15. preserve relevant evidence before making destructive changes.

---

# Failure Categories

Operational errors should be categorized where practical as:

| Category | Meaning |
|---|---|
| VALIDATION | Input or model output failed contract validation |
| ROUTING | Incorrect or invalid routing decision |
| KNOWLEDGE | Approved knowledge could not support the workflow |
| AUTHORIZATION | An action was denied by deterministic or AWS authorization |
| MODEL | Model or agent execution failed |
| TOOL | Tool invocation failed |
| BACKEND | Lambda or business backend failed |
| PERSISTENCE | DynamoDB operation failed |
| IDEMPOTENCY | Duplicate/conflicting logical operation detected |
| TIMEOUT | Operation exceeded an allowed duration |
| THROTTLING | Capacity or quota limit rejected work |
| SECURITY | Injection, secret, or policy violation detected |
| TELEMETRY | Required operational visibility is unavailable |
| DEPLOYMENT | Version/configuration change caused failure |
| UNKNOWN | Failure has not yet been classified |

`UNKNOWN` should be a temporary state, not the desired end of an investigation.

---

# Playbook DP-001 — Bug Ticket Was Not Created

## Customer Symptom

The customer completed the bug-report workflow but no confirmed ticket was received.

## Diagnostic Path

Check:

`request_id`

→ route should be `BUG`

→ required bug fields present?

→ validation passed?

→ tool proposed?

→ tool authorized?

→ AgentCore Gateway invocation?

→ Lambda invocation?

→ DynamoDB operation?

→ successful backend result returned?

## Possible Causes

Likely categories include:

- missing required information;
- schema validation failure;
- authorization failure;
- Gateway error;
- Lambda error;
- DynamoDB failure;
- timeout;
- ambiguous successful write.

## Safety Rule

Do not manually retry blindly.

Check `operation_id` before performing another side-effecting attempt.

---

# Playbook DP-002 — Duplicate Bug Ticket Reported

## Customer / Operator Symptom

Two or more tickets appear to represent the same logical bug-report operation.

## Diagnostic Path

Locate:

- ticket identifiers;
- `operation_id`;
- request IDs;
- timestamps;
- retry records.

Determine whether the tickets share the same logical operation.

## Questions

Was the same `operation_id` used?

Did the first operation succeed before its response was lost?

Did retry logic generate a new operation identifier incorrectly?

Did persistence bypass the conditional/idempotency mechanism?

## Immediate Principle

Do not treat duplicate deletion as the complete fix.

The engineering cause of the duplicate must be identified.

## Relevant Failure Mode

`FM-005 — Duplicate Side Effect`

---

# Playbook DP-003 — Reliora Claims Success but No Ticket Exists

## Symptom

The customer received a successful ticket-creation response but authoritative backend state does not contain the ticket.

## Severity

High.

This violates a critical behavioural invariant.

## Diagnostic Path

Determine:

1. where the ticket identifier originated;
2. whether the backend returned it;
3. whether model generation fabricated or transformed it;
4. whether persistence succeeded;
5. whether the wrong environment/table was inspected.

## Release Implication

Confirmed fabrication or false backend success should block release until understood and corrected.

## Relevant Failure Modes

`FM-006`

`FM-009`

`FM-010`

---

# Playbook DP-004 — Wrong Workflow Selected

## Symptom

A request enters an inappropriate workflow.

Example:

A policy question begins collecting bug-report fields.

## Diagnostic Path

Inspect:

- original customer input;
- routing result;
- routing confidence where applicable;
- routing implementation version;
- prompt/model/classifier version;
- relevant gold/challenge dataset coverage.

## Determine

Is this:

- an isolated model error;
- systematic class confusion;
- a dataset gap;
- a label-definition problem;
- a routing-contract bug?

Do not automatically solve every routing error by adding prompt instructions.

---

# Playbook DP-005 — Unsupported Policy Answer Generated

## Symptom

Reliora gives a platform or policy answer that is not supported by the approved knowledge source.

## Diagnostic Path

Inspect:

- top-level intent;
- knowledge-coverage decision;
- knowledge version;
- retrieved/approved content if applicable;
- generated response;
- evaluation case coverage.

## Determine

Did:

- coverage classification fail;
- the model use unsupported prior knowledge;
- approved knowledge contain stale information;
- the output fail grounding checks?

## Safe Behaviour

Unsupported knowledge should transition to human support rather than be invented.

---

# Playbook DP-006 — Request Is Unusually Slow

## Symptom

A request has materially higher latency than the current baseline.

## Diagnostic Path

Break total latency into available stages:

`request`

→ model / agent latency

→ validation

→ tool invocation

→ Lambda

→ persistence

→ response.

Inspect:

- model calls;
- iterations;
- tool calls;
- retries;
- throttling;
- downstream latency.

## Principle

Do not assume the LLM is the bottleneck.

Measure each major boundary first.

---

# Playbook DP-007 — Error Rate Increases Under Load

## Symptom

Controlled concurrency testing shows an increasing failure rate.

## Diagnostic Path

Compare workload levels and inspect:

- success rate;
- latency distribution;
- model throttles;
- AgentCore/service quotas;
- Gateway errors;
- Lambda concurrency;
- DynamoDB errors;
- retries;
- execution duration;
- cost/request.

## Objective

Identify the **first demonstrated constraint**, not the most visually obvious service in the architecture.

## Evidence

Record the finding as EXPERIMENTAL or MEASURED.

Do not describe controlled synthetic load as production traffic.

---

# Playbook DP-008 — AWS AccessDenied Error

## Symptom

A legitimate workflow fails with an AWS authorization error.

## Diagnostic Path

Identify:

- acting IAM principal or role;
- attempted API action;
- target resource;
- relevant IAM policy;
- resource policy where applicable;
- recent infrastructure changes.

## Principle

Do not fix the problem by immediately granting wildcard permissions.

Determine the smallest permission required.

---

# Playbook DP-009 — Prompt Injection or Internal Leakage

## Symptom

A customer receives internal route information, protected instructions, reasoning markers, or triggers unexpected agent behaviour.

## Immediate Actions

Preserve:

- request;
- response;
- relevant version identifiers;
- route;
- tool trajectory;
- authorization decision.

Do not preserve hidden chain-of-thought as an operational requirement.

## Diagnosis

Determine whether failure occurred in:

- prompt instruction hierarchy;
- output validation;
- tool authorization;
- response filtering;
- test coverage.

## Release Implication

Critical internal-information leakage or unauthorized side effects should block promotion.

---

# Playbook DP-010 — Unexpected AWS Cost Increase

## Symptom

AWS spend or estimated unit cost materially exceeds expected development behaviour.

## Diagnostic Path

Inspect:

- request volume;
- model calls/request;
- tokens/request;
- iterations/request;
- retries/request;
- tool calls/request;
- long-running invocations;
- unexpected resources;
- forgotten deployed environments;
- CloudWatch/log volume.

## Determine

Is the increase caused by:

- legitimate workload;
- inefficient agent behaviour;
- retry amplification;
- configuration error;
- abandoned infrastructure;
- abuse;
- telemetry volume?

## Principle

Cost is an operational signal, not only a billing concern.

---

# Playbook DP-011 — Observability Gap

## Symptom

A failure occurred but there is insufficient telemetry to determine where.

## Diagnosis

Identify which correlation or telemetry event should have existed.

Examples:

- missing `request_id`;
- missing `operation_id`;
- absent tool result;
- missing version provenance;
- incomplete error classification.

## Response

Treat the missing diagnostic signal as an engineering defect.

Add only the telemetry required to resolve the demonstrated diagnostic gap.

Avoid logging entire customer payloads merely to make debugging easier.

---

# Playbook DP-012 — Regression After Deployment

## Symptom

A previously passing workflow begins failing after a candidate deployment.

## Diagnostic Path

Compare:

- application version;
- prompt version;
- model/configuration version;
- routing version;
- knowledge version;
- infrastructure version;
- evaluation result.

Run targeted regression tests.

## Recovery

Where the new release is responsible, restore the previously validated version.

## Follow-Up

Create or update a regression case reproducing the defect before the incident is considered fully addressed.

---

# Diagnostic Evidence Package

A meaningful failure investigation should preserve enough evidence to answer:

| Question | Evidence |
|---|---|
| What happened? | Symptom / error classification |
| When? | Timestamp |
| Which request? | `request_id` |
| Which conversation? | `session_id`, when relevant |
| Which side effect? | `operation_id`, when relevant |
| Which code? | Application version |
| Which prompt? | Prompt version |
| Which model? | Model/configuration identifier |
| Which knowledge? | Knowledge version |
| Which route? | Routing result/version |
| Which tool? | Proposed/authorized/executed tool |
| What backend result? | Validated operation result |
| What failed? | Failure category |
| How was it recovered? | Retry / handoff / rollback / remediation |

Sensitive values must still follow the privacy and logging policy.

---

# Root Cause Analysis Principle

The first visible error is not necessarily the root cause.

Example:

Customer sees timeout

→ Gateway timed out

→ Lambda was slow

→ Lambda retried DynamoDB

→ DynamoDB requests increased

→ original cause was retry amplification from an upstream configuration change.

Investigations should therefore distinguish:

- symptom;
- immediate technical failure;
- contributing conditions;
- root cause;
- recovery;
- preventive action.

---

# Recovery Verification

Recovery is not complete merely because an engineer changed something.

Where practical:

failure

→ remediation

→ targeted test

→ regression test

→ operational verification

→ evidence.

If a new failure teaches the project something important, the knowledge should be reflected in:

- failure-mode analysis;
- regression dataset;
- threat model where applicable;
- ADR where architecture changes;
- diagnostic playbook.

---

# Current Status

This is the initial **TARGET diagnostic playbook**.

Specific CloudWatch queries, AgentCore trace locations, dashboards, alarm names, AWS console paths, and operational commands will be added after the corresponding infrastructure and telemetry exist.

The playbook deliberately avoids inventing diagnostic procedures for resources that have not yet been deployed.