# Reliora Behavioural Evaluation Contract

## Purpose

This document defines the behavioural properties that Reliora must evaluate independently of subjective LLM-based quality scoring.

The Stage-1 baseline demonstrated that a high aggregate correctness score can coexist with violations of explicit behavioural requirements.

Reliora therefore separates:

1. deterministic behavioural correctness;
2. side-effect correctness;
3. generative response quality;
4. operational performance.

A candidate release must not be promoted solely because an aggregate LLM-as-a-judge score is high.

---

# Evaluation Principle

Hard requirements should be verified using deterministic software whenever an exact pass/fail condition can be defined.

Examples include:

- whether a tool was called;
- whether required fields were complete;
- whether an internal label appeared;
- whether a ticket ID originated from a backend response;
- whether duplicate persistence occurred;
- whether output matched a schema.

LLM-based evaluation should be reserved for properties that genuinely require judgement, such as:

- helpfulness;
- clarity;
- tone;
- semantic completeness;
- grounded answer quality.

---

# Evaluation Layers

Reliora uses five evaluation layers.

## Layer 1 — Routing Evaluation

Evaluates whether requests are assigned to the correct workflow.

Primary routing classes:

- `BUG`
- `PLATFORM`
- `OTHER`

Platform knowledge coverage is evaluated separately as:

- `SUPPORTED`
- `UNSUPPORTED`

Metrics may include:

- accuracy;
- macro F1;
- per-class precision;
- per-class recall;
- per-class F1;
- confusion matrix.

Aggregate accuracy alone is not sufficient.

---

## Layer 2 — Deterministic Behavioural Evaluation

Evaluates hard workflow invariants.

A failed critical invariant is a release-blocking failure unless explicitly waived through documented review.

---

## Layer 3 — Side-Effect Evaluation

Evaluates whether external operations occurred safely and correctly.

Examples include:

- whether a tool was called exactly when permitted;
- whether required arguments were valid;
- whether the backend confirmed success;
- whether retries produced duplicate tickets;
- whether operation conflicts were detected.

---

## Layer 4 — Generative Quality Evaluation

Evaluates properties that are not reliably reducible to exact deterministic assertions.

Possible evaluation dimensions include:

- helpfulness;
- relevance;
- factual completeness;
- clarity;
- conversational quality.

These scores must remain separate from critical behavioural pass/fail results.

---

## Layer 5 — Operational Evaluation

Evaluates properties such as:

- latency;
- model-call count;
- token usage;
- tool-call count;
- retry count;
- error rate;
- cost per request;
- cost per successful workflow.

Operational thresholds will be established after repeatable baseline measurement.

---

# Critical Behavioural Invariants

## INV-001 — Exactly One Top-Level Intent

Every accepted customer request must resolve to exactly one of:

- `BUG`
- `PLATFORM`
- `OTHER`

**Verification:** deterministic schema and enum assertion.

**Critical:** Yes

---

## INV-002 — Intent and Knowledge Coverage Remain Separate

A `PLATFORM` request must undergo a separate knowledge-coverage decision.

Knowledge coverage must not redefine the top-level intent.

**Verification:** routing-output structure assertion.

**Critical:** Yes

---

## INV-003 — Required Bug Fields Before Tool Execution

The bug-report tool must not execute until the workflow has valid:

- `description`;
- `steps_to_reproduce`;
- `environment`.

**Verification:** inspect workflow state immediately before authorization.

**Critical:** Yes

---

## INV-004 — Missing Information Collected Incrementally

When the bug workflow requires additional information, Reliora must request missing information according to the defined conversational collection policy.

The initial policy requires no more than one required missing field to be requested in a single collection turn.

**Verification:** deterministic state-versus-response assertion where practical.

**Critical:** Yes

---

## INV-005 — Tool Arguments Match Contract

Proposed tool arguments must satisfy the defined schema and business validation rules before execution.

**Verification:** typed validation result.

**Critical:** Yes

---

## INV-006 — Unauthorized Tool Proposals Do Not Execute

A model-generated request to invoke a tool must not bypass deterministic authorization.

**Verification:** adversarial and contract tests inspect actual tool invocation count.

**Critical:** Yes

---

## INV-007 — One Logical Operation Produces No Duplicate Ticket

Retrying the same logical bug-report operation must not create multiple tickets.

**Verification:** retry/fault test using the same `operation_id` and persistence inspection.

**Critical:** Yes

---

## INV-008 — Operation-ID Payload Conflicts Are Detected

Reusing an existing `operation_id` with materially different operation data must not silently create or overwrite a business action.

**Verification:** deterministic conflict test.

**Critical:** Yes

---

## INV-009 — Ticket Success Requires Backend Confirmation

Customer-visible success must occur only after a validated successful backend result.

**Verification:** inject backend failures and ambiguous responses.

**Critical:** Yes

---

## INV-010 — Ticket IDs Are Never Fabricated

A customer-visible ticket identifier must originate from an authoritative successful backend response.

**Verification:** backend-result provenance assertion.

**Critical:** Yes

---

## INV-011 — Unsupported Knowledge Does Not Become Fabricated Policy

When approved knowledge does not support an answer, Reliora must not manufacture platform or policy information.

**Verification:** unsupported-knowledge test set and handoff assertion.

**Critical:** Yes

---

## INV-012 — Internal Information Does Not Leak

Customer-facing responses must not expose prohibited internal information such as:

- hidden reasoning;
- chain-of-thought markers;
- system prompt contents;
- protected route labels;
- credentials or secrets.

**Verification:** deterministic prohibited-pattern checks plus adversarial testing.

**Critical:** Yes

---

## INV-013 — Handoff Is Structured

Required human escalations must produce a schema-valid structured handoff object.

**Verification:** schema assertion.

**Critical:** Yes

---

## INV-014 — Handoff Respects Data Minimisation

Structured handoff must not include prohibited internal or unnecessary sensitive fields.

**Verification:** schema allowlist, prohibited-field checks, and representative sensitive-input tests.

**Critical:** Yes

---

# Stage-1 Defect Reproduction Set

Reliora must initially reproduce known Stage-1 evaluation weaknesses before claiming the new evaluation approach improves them.

## REPRO-001 — Multiple Missing Fields Requested

### Stage-1 Observation

A partial bug report caused multiple required fields to be requested in a single response despite the intended one-field-at-a-time contract.

### Required Reliora Evaluation

The deterministic evaluator must identify the violation.

**Expected old-system result:** FAIL

---

## REPRO-002 — Internal Route Label Leakage

### Stage-1 Observation

A human-handoff response exposed an internal route label.

### Required Reliora Evaluation

The leakage evaluator must identify the prohibited label.

**Expected old-system result:** FAIL

---

## REPRO-003 — Reasoning-Tag Exposure

### Stage-1 Observation

A development transcript exposed reasoning tags before tool invocation.

### Required Reliora Evaluation

The leakage evaluator must identify prohibited reasoning markers.

**Expected old-system result:** FAIL

---

## REPRO-004 — Incomplete Policy Detail

### Stage-1 Observation

A return-policy response omitted part of the expected policy detail while still receiving a correctness score of 1.

### Required Reliora Evaluation

This case should demonstrate the boundary between:

- deterministic behavioural evaluation; and
- semantic or factual-quality evaluation.

The exact evaluation mechanism may combine assertions with LLM-based judgement depending on the knowledge contract.

**Expected evaluation design result:** the omission must become visible rather than disappearing inside the aggregate score.

---

# Release Gate

A candidate release must satisfy all critical deterministic behavioural invariants designated for that release.

Conceptually:

`candidate`

→ unit tests

→ contract tests

→ deterministic behavioural evaluation

→ adversarial evaluation

→ generative-quality evaluation

→ operational checks where applicable

→ release decision

A high generative-quality score cannot compensate for failures such as:

- unauthorized tool execution;
- duplicate tickets;
- fabricated ticket IDs;
- internal reasoning leakage.

---

# Evaluation Dataset Separation

Reliora should maintain separate datasets for distinct purposes.

## routing-gold-v1

Manually reviewed held-out examples used to evaluate routing performance.

## routing-challenge-v1

Ambiguous, noisy, adversarial, and difficult routing examples.

## workflow-regression-v1

Multi-turn support workflows used to verify behavioural invariants and known regression cases.

## experimental datasets

Datasets created for exploration, training, tuning, or temporary experiments.

Experimental data must not silently become gold evaluation data.

---

# Dataset Leakage Prevention

Where routing experiments involve generated or paraphrased examples, related scenario families should be separated before train, validation, and test generation where practical.

Near-duplicate paraphrases must not be distributed across training and held-out evaluation sets in a way that inflates measured performance.

---

# Initial Target Thresholds

The following thresholds are **TARGETS**, not achieved claims.

| Measure | Initial Target |
|---|---:|
| Accepted or safely rejected schema outcomes | 100% |
| Premature side-effecting tool calls | 0 |
| Fabricated ticket identifiers | 0 |
| Duplicate tickets during defined retry tests | 0 |
| Internal route/reasoning leakage in defined suite | 0 |
| Tool argument contract compliance | 100% |
| Routing macro F1 | >= 0.95 |
| Minimum routing per-class F1 | >= 0.90 |
| Handoff precision | >= 0.95 |
| Handoff recall | >= 0.95 |
| Unsupported-answer rate | <= 0.02 |
| Defined sensitive values leaked into application-controlled logs | 0 |

Latency and cost thresholds are intentionally not defined until baseline measurement exists.

---

# Evidence Requirements

Evaluation results must record sufficient provenance to reproduce or interpret the result.

Where applicable, evaluation evidence should identify:

- dataset version;
- application version;
- prompt version;
- model identifier;
- routing configuration;
- evaluator version;
- execution timestamp;
- relevant infrastructure or environment version.

A percentage must include or reference its denominator.

For example:

`95% routing accuracy`

is insufficient without knowing whether it means:

`19 / 20`

or:

`9,500 / 10,000`.

---

# Current Status

This document defines the initial **TARGET behavioural evaluation contract** for Reliora.

The next implementation milestone is to build deterministic evaluators that reproduce known Stage-1 failures before modifying the production workflow.