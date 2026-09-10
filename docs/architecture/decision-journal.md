---
title: "Reliora Solutions Architect Decision Journal"
subtitle: "Project-specific architectural reasoning, evidence and interview system"
product: "Reliora"
version: "1.1"
status: "Living Project Journal"
date: "2026-09-04"
---

# Reliora Solutions Architect Decision Journal

## 0. Purpose

This is the project-specific instance of the **Universal Solutions Architect Decision Journal** for Reliora.

It preserves the reasoning behind important Reliora decisions so that:

- implementation remains requirement-driven;
- the architecture does not drift into technology collection;
- important trade-offs remain visible;
- source authority is respected;
- decisions can be verified through evidence;
- architecture lessons can be extracted into the Learning Ledger;
- interview narratives are created from real engineering work;
- future changes can be compared against the reasoning that produced the current system.

Reliora is a **production-oriented AI customer-support reliability and control platform for online commerce**.

Its core engineering principle is:

> **The LLM may propose; deterministic software validates and authorizes.**

The journal must distinguish:

- **decision accepted** from **implementation complete**;
- **designed** from **measured**;
- **target** from **observed**;
- **synthetic business assumption** from **real system measurement**.

---

# 1. Source Authority

Use this precedence when a Reliora decision is challenged:

1. official Udacity/AWS P1 requirements and rubric;
2. Reliora Product Constitution;
3. Reliora Product North Star;
4. Reliora requirements, policies, architecture, evaluation contracts, ADRs and preserved evidence;
5. Portfolio Product Engineering Standard;
6. Reliora End-to-End Solutions Architect Delivery Blueprint;
7. general/external knowledge.

The Decision Journal records reasoning. It does not override higher-authority product sources.

---

# 2. Current Source Snapshot

The governing source snapshot currently records:

- Stage-1 provenance preserved;
- local deterministic evaluation foundation complete;
- routing benchmark v1 completed;
- local runtime safety foundation substantially complete;
- distinct request/session/operation identity;
- deterministic authorization;
- idempotency admission/replay semantics;
- authoritative ticket confirmation;
- ticket-provider abstraction;
- source snapshot commit: `6a9ad71`;
- source snapshot test baseline: **190 passing tests**;
- ADR-017 added as a PROPOSED trusted-execution-identity decision;
- architecture-hypothesis correction captured before Strands or another runtime was introduced;
- source snapshot delivery branch: `feat/aws-infrastructure`.

These values are a dated source snapshot and must be re-verified against the live repository before they are used as current evidence.

---

# 3. Decision Index

Implementation status should be updated as the project progresses.

| ID | Decision | Importance | Decision Status | Implementation Status | Evidence Status |
|---|---|---|---|---|---|
| RJ-001 | Treat Reliora as a reliability/control product, not a chatbot demo | CRITICAL | ACCEPTED | IN PROGRESS | PARTIAL |
| RJ-002 | Preserve P1-S1 as provenance instead of rewriting history | HIGH | ACCEPTED | IMPLEMENTED | PARTIAL/VERIFY |
| RJ-003 | Separate probabilistic reasoning from deterministic authorization | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-004 | Use request, session and operation identity as separate concepts | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-005 | Authorize before idempotency admission and side-effect execution | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-006 | Matching retry replays the authoritative result; conflict does not execute | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-007 | Backend truth is required before customer-visible ticket success | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-008 | Use provider/adapter boundaries for replaceable ticket integrations | HIGH | ACCEPTED | IMPLEMENTED LOCALLY | LOCAL VERIFIED |
| RJ-009 | Keep approved knowledge small/versioned; do not add mandatory RAG without evidence | HIGH | ACCEPTED | P1 BASELINE + RELIORA TARGET | VERIFY |
| RJ-010 | Keep frontend/product experience decoupled from permanent AWS runtime | HIGH | ACCEPTED | PLANNED | PENDING |
| RJ-011 | AWS-first implementation, but product identity is not AWS-defined | HIGH | ACCEPTED | IN PROGRESS | PARTIAL |
| RJ-012 | Use Terraform for productized persistent cloud infrastructure | HIGH | ACCEPTED | PENDING / IN PROGRESS | PENDING |
| RJ-013 | Preserve AgentCore/Gateway/Lambda/DynamoDB functional baseline while strengthening controls | HIGH | ACCEPTED | PENDING CLOUD INTEGRATION | PENDING |
| RJ-014 | Separate deterministic evaluation from generative/LLM evaluation | CRITICAL | ACCEPTED | IMPLEMENTED LOCALLY / CLOUD PENDING | PARTIAL |
| RJ-015 | Select routing architecture from benchmark evidence, not model fashion | HIGH | ACCEPTED | BENCHMARK COMPLETE | VERIFY/FREEZE |
| RJ-016 | Treat human handoff as a structured workflow outcome | HIGH | ACCEPTED | PLANNED / PARTIAL | PENDING |
| RJ-017 | Observability should reconstruct decisions without hidden chain-of-thought | HIGH | ACCEPTED | PLANNED | PENDING |
| RJ-018 | Failure/retry behaviour is part of product acceptance | CRITICAL | ACCEPTED | LOCAL PARTIAL / CLOUD PENDING | PARTIAL |
| RJ-019 | Cost is an architecture dimension and must be measured within a stated workload | HIGH | ACCEPTED | PLANNED | PENDING |
| RJ-020 | Do not add multi-agent/RAG/Kubernetes/etc. merely for résumé breadth | HIGH | ACCEPTED | ACTIVE GUARDRAIL | DOCUMENTED |
| RJ-021 | Support local, AWS integration and ephemeral cloud demonstration modes | HIGH | ACCEPTED | PARTIAL / PLANNED | PENDING |
| RJ-022 | Public claims must be bounded by evidence | CRITICAL | ACCEPTED | ACTIVE | PARTIAL |
| RJ-023 | Use a formal Solutions Architect decision journal linked to Learning and Interview ledgers | HIGH | ACCEPTED | IMPLEMENTED BY THIS DOCUMENT | VERIFIED |
| RJ-024 | Use a dedicated least-privilege Lambda execution role derived from Reliora's actual runtime access pattern | CRITICAL | ACCEPTED | PENDING IMPLEMENTATION | LOCAL/SOURCE VERIFIED; AWS PENDING |
| RJ-039 | Require an evidence gate before adopting candidate architecture or technology | HIGH | ACCEPTED | ACTIVE PROCESS GUARDRAIL | DOCUMENTED |

---

# 4. RJ-001 — Reliora is a reliability and control product, not a chatbot demo

### Metadata

| Field | Value |
|---|---|
| Category | Product / Architecture |
| Importance | CRITICAL |
| Decision status | ACCEPTED |
| Implementation status | IN PROGRESS |
| Source basis | Product Constitution, Product North Star, Delivery Blueprint |

### Decision question

What is the product actually being built?

### Decision

Reliora is an **AI Customer-Support Reliability and Control Platform for Online Commerce**.

The chatbot/support conversation is an interface into the product, not the product definition itself.

### Rationale

The difficult production problem is not merely fluent generation. The value is controlling:

- routing;
- grounding;
- persistent actions;
- retry safety;
- backend truth;
- human escalation;
- evaluation;
- observability;
- release regression;
- operating cost.

### Trade-off accepted

Reliora deliberately rejects feature breadth that does not strengthen this thesis.

### Reconsideration trigger

Revisit only if customer discovery or product evidence shows that the primary buyer problem has materially changed.

### Interview narrative

> "I started from a working support chatbot, but reframed the project around the operational risks companies face once LLMs can route requests and invoke business actions. That changed the architecture from 'make the bot answer' to 'make the system safe, observable, retry-safe and releasable.'"

### Transfer principle

Start product architecture from the **business risk and outcome**, not from the AI capability.

---

# 5. RJ-002 — Preserve the P1-S1 baseline rather than rewriting history

### Category
Architecture / Evidence / Portfolio

### Decision status
ACCEPTED

### Decision

Preserve Stage-1 evidence as historical provenance and make Reliora enhancements separately traceable.

### Why

The accepted baseline is useful because it provides:

- externally reviewed functional behaviour;
- original AgentCore/Gateway/Lambda/DynamoDB path;
- a before/after comparison;
- evidence that Reliora evolved from a working system.

Editing historical artifacts to imply newer Reliora controls existed earlier would weaken evidence integrity.

### Trade-off

Maintaining two layers of history requires more documentation discipline.

### Verification

A reviewer should be able to distinguish:

```text
P1-S1 fact
vs
Reliora enhancement
```

### Interview question

Why preserve a working baseline instead of rebuilding from scratch?

---

# 6. RJ-003 — Probabilistic reasoning, deterministic control

### Category
AI / Reliability / Security

### Importance
CRITICAL

### Decision status
ACCEPTED

### Implementation status
IMPLEMENTED LOCALLY; CLOUD VERIFICATION PENDING

### Decision question

Should the LLM be trusted to authorize state-changing business operations?

### Options

1. prompt instructions only;
2. LLM decides and executes directly;
3. LLM proposes, deterministic application code validates and authorizes.

### Decision

Use option 3.

### Reliora control chain

```text
LLM / workflow proposal
    ↓
typed validation
    ↓
deterministic authorization
    ↓
idempotency admission
    ↓
approved provider
    ↓
authoritative backend confirmation
    ↓
customer-visible success
```

### Why

Prompt adherence is probabilistic.

Persistent business actions require deterministic enforcement.

### Trade-off

More application code and contracts are required than in a simple tool-calling chatbot.

### Failure prevented

A model instruction failure must not be sufficient to bypass business authorization.

### Verification

- unauthorized tool proposal rejected;
- incomplete bug state cannot execute ticket creation;
- malformed arguments rejected;
- customer success only after backend confirmation.

### Interview explanation

> "I use the LLM for interpretation and proposal, but deterministic software owns authorization and persistent state. The model can be wrong without automatically making the business system wrong."

### Transfer question

How would this principle apply to an insurance agent proposing a payment or an account-change agent?

---

# 7. RJ-004 — Distinguish request_id, session_id and operation_id

### Category
Reliability / Observability / Integration

### Importance
CRITICAL

### Decision

Reliora uses three identities with different semantics.

```text
request_id  = one processing attempt
session_id  = one support conversation
operation_id = one logical side-effecting action
```

Example:

```text
Request 1:
request_id = R1
session_id = S1
operation_id = O1

Retry:
request_id = R2
session_id = S1
operation_id = O1
```

### Why

A network retry is a new processing request but may represent the **same intended business action**.

Without logical operation identity, safe replay becomes difficult.

### Trade-off

Additional identity management and telemetry fields.

### Verification

Retry tests must show a changed `request_id` with the same `operation_id`.

### Interview follow-up

Why is a request ID not enough for idempotency?

---

# 8. RJ-005 — Authorization precedes idempotency admission

### Category
Reliability / Security

### Importance
CRITICAL

### Decision

Reliora checks whether an action is allowed before accepting it into the idempotent side-effect path.

### Why

Idempotency prevents duplicate execution; it does not make an unauthorized action safe.

### Key distinction

```text
authorization asks:
"May this action happen?"

idempotency asks:
"Has this same logical action already happened?"
```

### Trade-off

The execution pipeline is more explicit and has additional states.

### Interview explanation

> "Idempotency is a reliability property, not an authorization policy. Replaying an unauthorized request safely is still unauthorized."

---

# 9. RJ-006 — Matching retry replays; conflicting reuse does not execute

### Category
Reliability / Integration

### Importance
CRITICAL

### Decision

Required semantics:

```text
O1 + payload P1
→ NEW_OPERATION
→ execute

O1 + payload P1 again
→ MATCHING_OPERATION
→ return existing authoritative outcome
→ do not execute provider again

O1 + different payload P2
→ CONFLICT
→ do not execute
```

### Why

This protects against:

- client retries;
- network ambiguity;
- duplicate tool invocation;
- accidental operation-ID reuse.

### Verification

Evidence must include:

- provider invocation count;
- ticket count;
- replay result;
- conflict result.

### Claim-safe wording

> "Reliora's tested execution path prevents duplicate logical ticket creation for matching retries within the demonstrated test environment."

---

# 10. RJ-007 — Backend truth before customer-visible success

### Category
Reliability / Product

### Importance
CRITICAL

### Decision

The model cannot invent:

- execution success;
- ticket ID;
- backend confirmation.

### Required state

If the system cannot determine whether the operation succeeded:

```text
UNCONFIRMED
```

is safer than guessed success.

### Why

A fluent model response is not proof of a persistent business outcome.

### Verification

- customer-visible ticket ID must match authoritative backend record;
- malformed backend response cannot become success;
- timeout/ambiguous response does not create fabricated confirmation.

### Interview transfer

A payment agent, booking agent, refund agent and ticket agent all need authoritative system-of-record confirmation.

---

# 11. RJ-008 — TicketProvider / adapter boundary

### Category
Architecture / Integration / Product

### Importance
HIGH

### Decision

Reliora business logic should depend on a provider contract rather than a specific ticket vendor implementation.

### Why

A retailer may use:

- custom support API;
- Zendesk;
- Jira Service Management;
- ServiceNow;
- Salesforce Service Cloud.

Reliora does not need to implement all of them.

The architecture should expose one clean replacement point.

### Trade-off

Some abstraction code is required.

### Guardrail

Do not create wrappers around every AWS service merely to claim portability.

### Interview explanation

> "I abstracted the boundary that a real customer is likely to replace—the ticket provider—not every internal implementation detail."

---

# 12. RJ-009 — Small approved knowledge source instead of mandatory RAG

### Category
AI / Knowledge / Cost

### Importance
HIGH

### Decision

Use a small, versioned approved knowledge source while the support knowledge scope remains small.

Do not add mandatory RAG until evidence shows:

- context size;
- content volume;
- update frequency;
- retrieval needs;
- cost

justify it.

### Alternatives

- embedded/versioned knowledge;
- Bedrock Knowledge Base / vector retrieval;
- external search/retrieval;
- fine-tuning.

### Why

RAG introduces additional:

- indexing;
- retrieval evaluation;
- latency;
- cost;
- operational dependencies;
- failure modes.

### Trade-off

Embedded knowledge does not scale indefinitely.

### Reconsideration trigger

Revisit when the approved corpus materially outgrows the current approach or retrieval quality becomes a documented requirement.

### Interview question

Why can "no RAG" be the more mature architecture decision?

---

# 13. RJ-010 — Decouple product UX from permanent AWS runtime

### Category
Architecture / Product / FinOps

### Importance
HIGH

### Decision

Reliora should support:

1. **Local Product Demo Mode**
2. **AWS Integration Mode**
3. **Ephemeral Portfolio Cloud Mode**

### Why

The product must remain:

- developable;
- demoable;
- testable;
- presentable

without maintaining paid cloud infrastructure continuously.

### Trade-off

Local/reference adapters must preserve compatible product contracts.

### Verification

The same canonical product journey should be demonstrable locally, while cloud evidence remains clearly distinguished from mocked/reference behaviour.

---

# 14. RJ-011 — AWS-first, not AWS-defined

### Category
Architecture / Product

### Decision

AWS is the primary implementation environment for Reliora, but service names do not define the product.

### Why

Reliora's value proposition should remain understandable even if the implementation provider changes.

### Current AWS baseline

- Amazon Bedrock;
- AgentCore managed runtime/harness;
- AgentCore Gateway;
- Lambda;
- DynamoDB;
- CloudWatch;
- S3/evaluation resources where required;
- IAM.

### Guardrail

Do not add "multi-cloud" abstractions without an actual product need.

### Interview explanation

> "AWS is the implementation choice; reliability-controlled AI support is the product capability."

---

# 15. RJ-012 — Terraform for persistent productized infrastructure

### Category
Cloud / Delivery / Operations

### Importance
HIGH

### Decision

Use Terraform for persistent/reproducible cloud infrastructure where provider support and reliability make it appropriate.

### Why

Desired properties:

- reviewable architecture;
- repeatable provisioning;
- explicit configuration;
- environment reproducibility;
- destroyability;
- infrastructure provenance.

### Important nuance

Do not force every temporary or poorly supported managed-service configuration into Terraform if a documented script/API workflow is more reliable.

### Verification

Target lifecycle:

```text
plan
→ review
→ apply
→ verify
→ evidence
→ destroy
```

### Interview follow-ups

- Why Terraform rather than console-only setup?
- How would remote state differ in a team environment?
- What should not be put in Terraform?

---

# 16. RJ-013 — Preserve AgentCore/Gateway/Lambda/DynamoDB baseline while strengthening controls

### Category
Architecture / Cloud / AI

### Importance
HIGH

### Decision

Reliora should preserve the useful P1 functional path rather than rearchitect simply because newer technologies are available.

Conceptual path:

```text
customer/support request
→ Reliora application/runtime
→ AgentCore
→ Gateway/tool boundary
→ Lambda
→ DynamoDB
```

Reliora adds safety/evaluation/operations controls around the working functional baseline.

### Why

Rewriting working architecture has cost and risk without automatic business value.

### Reconsideration triggers

- measured runtime limitation;
- cost problem;
- unsupported reliability requirement;
- provider capability gap;
- customer integration requirement.

---

# 17. RJ-014 — Deterministic vs generative evaluation

### Category
AI / LLMOps / Reliability

### Importance
CRITICAL

### Decision

Use deterministic evaluation for exact invariants and LLM/generative evaluation for judgement-like qualities.

### Deterministic examples

- required bug fields;
- no premature tool call;
- authorization;
- schema;
- duplicate prevention;
- conflicting operation ID;
- backend ID match;
- forbidden actions;
- structured handoff fields.

### Generative examples

- response clarity;
- semantic completeness;
- grounded FAQ quality;
- handoff quality.

### Governing rule

A strong LLM-judge score cannot override a failed safety invariant.

### Why

An evaluator can only enforce requirements it actually tests.

### Interview explanation

> "I don't ask an LLM judge to decide something Python can prove exactly."

---

# 18. RJ-015 — Evidence-driven routing architecture

### Category
AI / ML / Cost

### Importance
HIGH

### Decision

The routing architecture is selected from measured comparison rather than assuming every classification decision requires an LLM.

Frozen v1 candidates include:

- majority-class baseline;
- deterministic rules;
- TF-IDF + Logistic Regression;
- TF-IDF + Linear SVM.

The architecture decision should consider:

- macro/per-class F1;
- confusion patterns;
- failure severity;
- latency;
- determinism;
- dependency complexity;
- cost.

### Guardrail

Held-out test evidence must not be tuned against after it has influenced design.

### Reconsideration trigger

New representative data or changed business-error costs may justify a new benchmark version.

---

# 19. RJ-016 — Structured human handoff

### Category
Product / Reliability / Operations

### Importance
HIGH

### Decision

Handoff is a first-class workflow outcome, not merely:

> "Call this phone number."

A handoff should eventually include an appropriate, minimized subset of:

- reason;
- intent;
- safe summary;
- collected facts;
- attempted action;
- dependency failure;
- destination;
- correlation IDs;
- version/provenance.

### Why

Customers should not be trapped in automation or forced to repeat safely collected information.

### Verification

Evaluate:

- correct escalation;
- handoff package completeness;
- no unsupported automation;
- explicit human request respected.

---

# 20. RJ-017 — Observability without hidden chain-of-thought

### Category
Operations / Governance

### Importance
HIGH

### Decision

Operational reconstruction should use explicit provenance, not hidden model reasoning.

Required/target evidence includes:

- request ID;
- session ID;
- operation ID;
- route;
- versions;
- authorization result;
- idempotency state;
- provider/backend outcome;
- latency;
- failure category.

### Why

Operators need reconstructable actions, not private reasoning text.

### Verification

A controlled request/failure can be reconstructed from one identifier across the critical path.

---

# 21. RJ-018 — Failure is part of product acceptance

### Category
Reliability / Product

### Importance
CRITICAL

### Decision

Reliora is not accepted solely on happy-path success.

Required failure families include:

- model timeout;
- invalid output/schema;
- Gateway failure;
- Lambda timeout after write;
- malformed provider result;
- DynamoDB failure;
- duplicate tool invocation;
- unsupported knowledge;
- prompt injection;
- deployment regression.

### Why

Reliability only becomes meaningful when the failure path is designed and tested.

### Verification

Each major fault should have:

```text
fault
→ expected safe behaviour
→ actual behaviour
→ detection signal
→ recovery path
→ evidence
```

---

# 22. RJ-019 — Cost is architecture

### Category
FinOps / Architecture

### Importance
HIGH

### Decision

Reliora should measure cost at useful workload units rather than treating cloud cost as an afterthought.

Target measures:

- model calls/request;
- tokens/request;
- tool calls/request;
- latency;
- cost/request;
- cost/successful eligible resolution;
- evaluation cost;
- infrastructure cost.

### Claim discipline

Synthetic retailer ROI must remain explicitly separate from measured AWS/project cost.

### Reconsideration trigger

A materially different traffic or route mix invalidates previous unit economics.

---

# 23. RJ-020 — Explicit scope exclusions

### Category
Product / Architecture

### Importance
HIGH

### Decision

Do not add the following merely for technology breadth:

- multi-agent architecture;
- persistent personalized memory;
- mandatory RAG;
- AgentCore Browser;
- Code Interpreter;
- Kubernetes/EKS;
- Kafka/MSK;
- Redis;
- MLflow;
- LangGraph reimplementation;
- multi-region architecture;
- full commerce backend;
- real payment processing;
- enterprise multi-tenancy.

### Why

Each technology must earn its place through a Reliora-specific requirement, risk, bottleneck or experiment.

### Interview value

Being able to explain **why a technology was excluded** is often stronger architecture evidence than merely having used it.

---

# 24. RJ-021 — Local, AWS integration and ephemeral cloud modes

### Category
Architecture / Delivery / Product

### Decision

Support multiple modes with clear environment labeling.

### Local

For:

- development;
- zero-cost demos;
- UI work;
- deterministic tests.

### AWS

For:

- real integration;
- cloud verification;
- measurements;
- evidence.

### Ephemeral cloud

```text
deploy
→ verify
→ demonstrate
→ capture evidence
→ destroy
```

### Guardrail

Never present local mocked evidence as if it were AWS evidence.

---

# 25. RJ-022 — Evidence-bounded public claims

### Category
Portfolio / Governance

### Importance
CRITICAL

### Decision

Every material public statement should be classifiable as:

- measured;
- observed;
- implemented;
- verified;
- target;
- synthetic assumption;
- experimental.

### Example

Good:

> "The local regression baseline contained 164 passing tests at the recorded source snapshot."

Bad:

> "Reliora is production-proven at enterprise scale."

### Required artifact

Maintain a claim-evidence ledger before final portfolio release.

---

# 26. RJ-023 — Decision Journal + Learning Ledger + Interview Ledger



### Category
Career / Engineering Process

### Importance
HIGH

### Decision

Every high-value Reliora architecture decision should produce three related records.

## A. Decision Journal

Project-specific reasoning:

```text
requirement
→ alternatives
→ evidence
→ decision
→ trade-off
→ verification
```

## B. Learning Ledger

Reusable knowledge:

```text
concept
→ simple explanation
→ how it works
→ failure modes
→ when to use / not use
→ transfer example
```

## C. Interview Ledger

Ability to defend and transfer the decision:

```text
15-second answer
30/60-second answer
deep dive
follow-up questions
failure scenario
other-domain transfer
```

### Why

The project should function simultaneously as:

- a working product;
- a portfolio artifact;
- an architecture case study;
- a private learning system;
- an interview preparation system.

### Verification

For every `CRITICAL` Reliora decision, confirm all three records exist before final portfolio release.

---

# 27. Open Decision Queue

These decisions should receive full journal entries when their implementation phase begins.

| ID | Future decision question | Target phase | Status |
    |---|---|---|---|
| RJ-025 | DynamoDB physical schema for ticket + idempotency records | AWS core | OPEN |
| RJ-026 | Exact retry responsibility and retry budget by layer | Reliability | OPEN |
| RJ-027 | AgentCore memory/session configuration for Reliora runtime | Agent integration | OPEN |
| RJ-028 | Exact structured handoff schema and destination abstraction | Product/runtime | OPEN |
| RJ-029 | Cloud observability schema, logs, metrics and trace correlation | Operations | OPEN |
| RJ-030 | SLOs/SLIs after baseline measurement | Operations | DEFERRED UNTIL MEASURED |
| RJ-031 | Exact CI release gates and threshold metrics | CI/CD | OPEN |
| RJ-032 | Threat-model-driven security control selection | Security | OPEN |
| RJ-033 | Data retention/redaction values | Governance | OPEN |
| RJ-034 | Workload model and safe load-test envelope | Performance | OPEN |
| RJ-035 | Storefront/API boundary and local/cloud adapter strategy | Product UX | OPEN |
| RJ-036 | Minimum operator-console scope | Product UX | OPEN |
| RJ-037 | Recovery/rollback and data-restore strategy | Operations | OPEN |
| RJ-038 | Final cloud hosting/demonstration strategy after portfolio release | Portfolio/FinOps | DEFERRED |

---

# 28. Full Reliora Decision Entry Template

Use this for `RJ-024` onward.

## RJ-XXX — [Title]

### Metadata

| Field | Value |
|---|---|
| Date opened | |
| Last updated | |
| Owner | |
| Phase | |
| Category | |
| Importance | |
| Decision status | |
| Implementation status | |
| Requirement(s) | |
| Risk(s) | |
| ADR | |
| Experiment | |
| Evidence | |
| Git commit/version | |

### 1. Decision question

### 2. Why this decision exists

### 3. Customer/business consequence

### 4. Reliora-specific constraints

### 5. Source-supported facts

### 6. Assumptions

| Assumption | Validation | Status |
|---|---|---|

### 7. Options considered

#### Option A

#### Option B

#### Option C

### 8. Decision criteria

### 9. Experiment / evidence plan

### 10. Results

### 11. Decision

### 12. Rationale

### 13. Trade-offs accepted

### 14. Rejected alternatives and why

### 15. Risks introduced

### 16. Implementation plan

### 17. Verification plan

### 18. Reconsideration triggers

### 19. Evidence links

### 20. Claim-safe wording

### 21. Interview narrative

#### 15 seconds

#### 60 seconds

#### Deep dive

### 22. Interview follow-ups

### 23. Transfer question

### 24. Learning Ledger extraction

### 25. Final state

```text
Decision Status:
Implementation Status:
Verification Status:
Evidence Complete:
Learning Ledger Complete:
Interview Ledger Complete:
ADR Required/Created:
Next Review:
```

---

# 29. Reliora Interview Decision Matrix

Before final release, be able to defend at least these decisions.

| Decision | Core interviewer question |
|---|---|
| Product framing | Why is Reliora more than a chatbot? |
| Deterministic control | Why should the LLM not authorize persistent actions? |
| Identity | Why request ID vs operation ID? |
| Idempotency | What happens if a write succeeds but the response times out? |
| Backend truth | Why can't the model simply return a ticket ID? |
| Adapter | Why abstract TicketProvider but not every AWS call? |
| Knowledge | Why no mandatory RAG? |
| Routing | Why benchmark rules/classical ML instead of always using an LLM? |
| Evaluation | Why deterministic evaluators plus LLM judges? |
| Human handoff | When should autonomy stop? |
| Observability | How do you diagnose a failed request without chain-of-thought? |
| Terraform | Why IaC, and what would you leave out of IaC? |
| AWS | Why AgentCore/Gateway rather than direct model-to-Lambda architecture? |
| Reliability | What is the retry policy and where should retries live? |
| Cost | What is cost per successful eligible resolution? |
| Scope | Why did you deliberately exclude Kubernetes, multi-agent design, etc.? |

---

# 30. Reliora Learning Extraction Checklist

When each major decision is verified, extract:

- simple definition;
- architecture concept;
- exact Reliora implementation;
- commands/scripts involved;
- AWS service role;
- failure modes;
- alternatives;
- trade-offs;
- troubleshooting encountered;
- evidence;
- interview questions;
- transfer problem;
- certification mapping where relevant.

This allows Reliora to remain both a product and a private systems-engineering curriculum.

---

# 31. Decision Review Gates

## Before AWS implementation

Review:

- RJ-003 through RJ-009;
- RJ-012;
- RJ-013;
- open IAM/storage/retry decisions.

## Before agent integration

Review:

- model authority;
- Gateway boundary;
- memory/session behaviour;
- tool schema;
- authorization;
- backend truth;
- handoff.

## Before operational hardening

Review:

- observability;
- failure taxonomy;
- retry responsibility;
- security;
- data lifecycle;
- cost.

## Before portfolio release

Every `CRITICAL` decision should be:

```text
ACCEPTED
+ IMPLEMENTED
+ VERIFIED
+ evidence-linked
+ Learning-Ledger-linked
+ Interview-ready
```

unless explicitly marked as a future/non-goal decision.

---
# 32. RJ-024 — Least-privilege Lambda execution identity and permissions

### Metadata

| Field | Value |
|---|---|
| Date opened | 2026-09-04 |
| Last updated | 2026-09-04 |
| Phase | AWS product core |
| Category | Security / IAM / Cloud Architecture |
| Importance | CRITICAL |
| Decision status | ACCEPTED |
| Implementation status | PENDING IMPLEMENTATION |
| Evidence status | LOCAL/SOURCE VERIFIED; AWS PENDING |
| Requirement basis | Least privilege, deterministic side-effect execution, backend truth |
| Related decision | RJ-039 |
| Related ADR | None currently required |
| Delivery branch | `feat/aws-infrastructure` |

### 1. Decision question

What AWS IAM trust and permission boundary should Reliora's bug-ticket Lambda
use?

### 2. Why this decision exists

Reliora's ticket execution path performs a persistent business side effect.

The Lambda execution role must therefore provide enough authority for the
approved execution path while avoiding unrelated DynamoDB and CloudWatch
permissions.

The permissions must be derived from the actual runtime access pattern rather
than from a broad managed policy or guessed future requirements.

### 3. Source-supported runtime behaviour

The current DynamoDB execution adapter uses:

```text
operations table
→ GetItem with ConsistentRead=True

operations table + tickets table
→ TransactWriteItems containing conditional Put actions
```

### 4. Trust decision

The Lambda execution role trusts:

```text
lambda.amazonaws.com
```

for:

```text
sts:AssumeRole
```

No customer, model-generated input, application user, or Gateway payload may
assume this execution role directly.

### 5. DynamoDB permission decision

The demonstrated runtime requires:

```text
operations table
→ dynamodb:GetItem

operations table
→ dynamodb:PutItem
  only as part of TransactWriteItems

tickets table
→ dynamodb:PutItem
  only as part of TransactWriteItems
```

Use `dynamodb:EnclosingOperation` to constrain the transactional PutItem
permissions to the approved `TransactWriteItems` path.

Do not grant permissions for DynamoDB operations that the selected runtime does
not use.

Current exclusions include:

```text
Scan
Query
UpdateItem
DeleteItem
BatchWriteItem
dynamodb:*
```

### 6. CloudWatch Logs decision

Terraform will create the Lambda log group explicitly.

The Lambda execution role therefore requires only:

```text
logs:CreateLogStream
logs:PutLogEvents
```

scoped to the Reliora Lambda log-group streams.

The execution role will not require `logs:CreateLogGroup`.

Terraform owns log-group creation, retention, tags, lifecycle and teardown.

### 7. Managed-policy decision

Do not attach broad DynamoDB managed policies.

Do not attach `AWSLambdaBasicExecutionRole` when Reliora can define the
required logging permissions more narrowly.

Use a Reliora-owned least-privilege execution policy.

### 8. Decision

Use a dedicated Terraform-managed Lambda execution role derived from the
runtime's demonstrated AWS access pattern.

```text
Trust
→ lambda.amazonaws.com
→ sts:AssumeRole

Operations table
→ GetItem

Operations + tickets tables
→ transactional PutItem

Reliora Lambda log streams
→ CreateLogStream
→ PutLogEvents
```

### 9. Rationale

The permission model follows:

```text
actual runtime requirement
→ required AWS operation
→ required resource
→ IAM permission
```

rather than:

```text
AWS service
→ broad managed policy
→ application
```

This keeps IAM authority aligned with implemented behaviour.

### 10. Trade-offs accepted

A custom least-privilege policy requires more maintenance than attaching broad
AWS-managed policies.

If the application later introduces a legitimate new AWS API operation, the
policy must be deliberately updated.

That maintenance cost is accepted because IAM should evolve with verified
application requirements rather than anticipate hypothetical future features.

### 11. Risks

The proposed policy could fail because of:

- incorrect DynamoDB resource scoping;
- incorrect `dynamodb:EnclosingOperation` use;
- incorrect CloudWatch log-stream ARN scoping;
- an undocumented runtime dependency;
- future code changes introducing additional AWS operations.

These risks must be resolved through Terraform validation and real AWS
integration testing.

### 12. Verification plan

RJ-024 becomes AWS-verified only when the deployed runtime proves:

```text
1. Lambda assumes the execution role.
2. Lambda writes its expected CloudWatch logs.
3. GetItem succeeds against the operations table.
4. transactional creation writes one operation and one ticket.
5. matching retry reads and replays the existing result.
6. conflicting operation reuse performs no new write.
7. the demonstrated workflow requires no broader DynamoDB permissions.
```

The existence of the IAM role in AWS is not sufficient evidence.

The application workflow must execute successfully while using that role.

### 13. Evidence state

```text
Lambda trust semantics
→ VERIFIED FROM AWS DOCUMENTATION

Reliora DynamoDB access pattern
→ VERIFIED FROM SOURCE

DynamoDB transaction permission mechanism
→ VERIFIED FROM AWS DOCUMENTATION

CloudWatch log-stream permission model
→ VERIFIED FROM AWS DOCUMENTATION

Terraform implementation
→ PENDING

AWS role assumption
→ PENDING

AWS create/replay/conflict behaviour
→ PENDING

CloudWatch log delivery
→ PENDING
```

### 14. Reconsideration triggers

Revisit RJ-024 if:

- Reliora introduces another AWS API operation;
- the persistence architecture changes;
- the Lambda execution boundary changes;
- KMS introduces additional authorization requirements;
- tracing introduces additional runtime permissions;
- AWS integration proves the proposed policy insufficient;
- a simpler policy achieves the same least-privilege properties.

### 15. Claim-safe wording

Before cloud verification:

> Reliora's Lambda IAM boundary is designed from the runtime's demonstrated
> DynamoDB access pattern and documented AWS authorization semantics. Cloud
> execution remains pending verification.

After successful verification:

> Reliora's demonstrated Lambda ticket workflow executes under a
> resource-scoped role limited to the DynamoDB and CloudWatch operations
> required by the tested path.

### 16. Interview narrative

#### 15 seconds

> I derived the Lambda execution role from the SDK operations the application
> actually performs instead of attaching a broad DynamoDB policy.

#### 60 seconds

> I inspected the runtime first. Reliora needs a strongly consistent GetItem
> against its operation record and transactional writes to its operations and
> tickets tables. The transaction writes are constrained to the transactional
> path, and Terraform owns the Lambda log group so the runtime only needs
> stream-level logging permissions. I still treat the design as cloud-pending
> until create, replay and conflict behavior succeeds under that exact role.

### 17. Learning Ledger extraction

After AWS verification, extract reusable lessons covering:

- Lambda execution-role trust;
- invocation permission versus execution permission;
- deriving IAM from SDK access patterns;
- DynamoDB resource scoping;
- transaction-scoped permissions;
- Terraform-managed CloudWatch logging;
- least-privilege verification.

### 18. Final state

```text
Decision Status: ACCEPTED
Implementation Status: PENDING
Verification Status: SOURCE/DOCUMENTATION VERIFIED; AWS PENDING
Evidence Complete: NO
Learning Ledger Complete: DEFER UNTIL AWS VERIFICATION
Interview Ledger Complete: PARTIAL
ADR Required/Created: NO
Next Review: after Lambda/DynamoDB cloud integration
```


# 33. RJ-039 — Candidate architecture requires an evidence gate before implementation

### Category
Engineering Process / Architecture Governance

### Importance
HIGH

### Decision status
ACCEPTED

### Implementation status
ACTIVE PROCESS GUARDRAIL

### Decision

Before introducing a new framework, service, runtime, database, orchestration layer,
model architecture, major dependency or material architecture change, Reliora must pass
a pre-implementation architecture gate.

The gate is:

```text
requirement / observed problem
        ↓
authoritative current architecture
        ↓
can the existing architecture satisfy it?

YES
→ use the existing architecture

UNKNOWN
→ run the smallest experiment that removes the uncertainty

NO, supported by evidence
→ compare alternatives
→ document trade-offs
→ select the change
→ implement only after the decision is justified
```

Every material recommendation should be labelled as one of:

- `REQUIRED BY SOURCE`;
- `ACCEPTED BASELINE`;
- `PROPOSED`;
- `EXPERIMENTAL CANDIDATE`;
- `VERIFIED`.

### Why this decision exists

During the trusted-execution-identity investigation, Reliora correctly discovered that
the locally mocked Lambda `ClientContext` contract did not prove the real AgentCore
Gateway transport contract.

A plausible implementation mechanism was then identified using Strands tool-use
identity and retry semantics.

The mistake was not identifying Strands as a candidate. The mistake was allowing a
candidate mechanism to become the likely next implementation before proving that the
accepted AgentCore managed baseline was inadequate.

A source-precedence review showed that the current Reliora architecture still preserves
the official managed AgentCore Harness / Gateway / Lambda / DynamoDB baseline. That
baseline had not yet been demonstrated incapable of satisfying the identity requirement.

No Strands dependency, runtime replacement or cloud resource was introduced. The plan
was corrected before implementation.

### General rule

> **UNKNOWN is an experiment state, not permission to introduce a plausible technology.**

Also:

```text
candidate mechanism
!= architecture decision
!= implemented architecture
!= verified architecture
```

### Failure prevented

Without this gate, a technically attractive mechanism can cause:

- architecture drift;
- unnecessary dependencies;
- source-precedence violations;
- multiple simultaneous integration unknowns;
- harder troubleshooting;
- accidental résumé-driven technology collection.

### Trade-off

The gate adds a small amount of decision overhead before material architecture changes.

That cost is accepted because it reduces unnecessary implementation and makes future
architecture decisions easier to defend.

### Verification

For future material architecture changes, confirm before implementation:

1. the requirement or observed limitation is named;
2. the governing source and accepted baseline are identified;
3. the existing architecture is evaluated first;
4. an `UNKNOWN` capability is resolved through the smallest useful experiment;
5. candidate technologies remain labelled as candidates until selected;
6. dependency, infrastructure and runtime changes occur only after the gate passes;
7. the decision is recorded in an ADR or Decision Journal when material.

### Current example

For ADR-017:

- trusted execution identity remains a real requirement;
- Strands remains only a possible future mechanism if independently justified;
- the managed AgentCore baseline is tested first;
- Lambda/DynamoDB cloud correctness is verified before adding Gateway/runtime
  uncertainty;
- ADR-017 remains `PROPOSED` until end-to-end identity evidence exists.

### Interview narrative

> "I discovered a real integration-contract gap, but initially moved too quickly from
> the problem to a plausible framework-specific solution. Before implementation, I
> rechecked the governing architecture and saw that the managed AgentCore baseline had
> not yet been proven inadequate. I corrected the sequence, preserved the unresolved
> requirement in the ADR, and added an architecture-admission gate so unknowns trigger
> experiments rather than automatic technology adoption."

### Learning Ledger extraction

The reusable portfolio rule is maintained in the Portfolio Product Engineering
Standard under the Tool Admission Rule and Pre-Implementation Architecture Gate.

---

# 34. Final Reliora Rule

> **Reliora should not merely show that the architecture works. It should preserve why the architecture exists, what alternatives were rejected, what trade-offs were accepted, what evidence supports the decision, what would cause the design to change, and how the principle transfers beyond Reliora.**

> **By project completion, the codebase is the implementation, the evidence ledger is the proof, the Learning Ledger is the reusable knowledge, the Interview Ledger is the communication layer, and this Decision Journal is the reasoning that connects them.**
