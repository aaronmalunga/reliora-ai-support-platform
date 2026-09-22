# RELIORA PRODUCT LIFECYCLE AND ARCHITECTURE AUDIT

**Document type:** Product lifecycle, architecture, evidence, and implementation-readiness audit
**Product:** Reliora — AI Customer-Support Reliability and Control Platform for Online Commerce
**Audit date:** 2026-09-16
**Audit mode:** Audit first; change second
**Code-change status:** No source-code or architecture changes made by this audit
**Primary live implementation snapshot:** `feat/failure-telemetry-emission @ 88c13baa8ae5d47910acf39ba879cf066815a364`
**Parent architecture line:** `feat/aws-infrastructure @ da0d028a1b41aa1f2a7ccf084b49211c25d3fc1e`
**Historical local-safety baseline:** `main @ cc02e5838dda9d1ded121008d86a04526e6e273e`
**Separate outstanding governance branch:** `docs/security-privacy-hardening`
**Learning Ledger snapshot:** `aws-agentic-ai-learning-ledger/main @ ad88d39fb686efe677d18f6a917bc19379d9f409`

---

## Audit Rule

This audit treats Product 2 and later universal project processes as a **process mirror**, not as an architecture template.

A missing artifact does not automatically create an implementation requirement.

Every recommended remediation must be independently justified by at least one of:

- a Reliora product requirement;
- a Reliora customer/problem hypothesis that still requires validation;
- an observed implementation failure;
- a security, reliability, governance, privacy, operational, or cost risk;
- an experiment;
- an accepted architecture decision;
- or an applicable governing portfolio/product standard.

Historical evidence is preserved as historical evidence. The audit does not rewrite P1-S1 or earlier Reliora work to make later practices appear to have existed from the beginning.

---

# 1. Executive Summary

Reliora is **not an early-stage project**. It already has a substantial production-oriented engineering foundation, including:

- a frozen P1-S1 provenance baseline;
- explicit functional and non-functional requirements;
- deterministic domain contracts;
- request, session, and operation identity separation;
- deterministic authorization before side effects;
- idempotency and conflict semantics;
- authoritative backend-result requirements;
- local reference execution semantics;
- a DynamoDB-backed durable execution adapter;
- conditional transactional persistence;
- strongly consistent reconciliation reads;
- explicit `UNCONFIRMED` outcomes for ambiguous state;
- local failure-injection coverage;
- a structured failure taxonomy;
- early failure-telemetry emission;
- routing experiments and frozen held-out evidence;
- deterministic behavioural evaluation;
- evidence classification and E0-E9 maturity discipline;
- a metric dictionary;
- Terraform definitions for the current Lambda/DynamoDB core;
- a GitHub Actions quality workflow;
- a logical architecture;
- an autonomy policy;
- a threat model;
- a decision journal;
- an AWS learning and interview ledger.

The principal audit finding is therefore:

> **Reliora does not need a redesign. It needs lifecycle closure, evidence promotion, selective implementation completion, and source-state consolidation.**

The strongest parts of Reliora are currently the **local control architecture, side-effect semantics, evaluation discipline, and claim discipline**.

The weakest parts are not “missing fashionable technology.” They are:

1. **retrospective discovery and buyer/problem evidence**;
2. **a formal problem-buyer evidence gate and explicit kill/pivot/narrow conditions**;
3. **a product-level alternatives/business-case record**, beyond component-level alternatives;
4. **trusted logical-operation identity through the real AgentCore/Gateway/Lambda path**, which remains explicitly unproven;
5. **structured handoff implementation**, which is specified but not yet present as a current runtime capability;
6. **end-to-end observability wiring and target-environment reconstruction evidence**;
7. **recovery/rollback/DR operational closure**;
8. **release-gate completion**, including deterministic evaluation and security checks;
9. **cloud integration evidence**, still below target-environment maturity;
10. **repository/source drift**, including stale status snapshots and a divergent privacy/security branch;
11. **Learning Ledger lag** for the newest reconciliation and telemetry lessons.

No evidence was found that Reliora independently requires:

- mandatory RAG;
- multi-agent orchestration;
- Kubernetes/EKS;
- Kafka/MSK;
- Redis;
- persistent customer memory;
- browser automation;
- code execution;
- enterprise multi-tenancy;
- multi-region architecture.

Those remain **NO CHANGE / NOT JUSTIFIED**.

The project is best described today as a **research-grounded, production-oriented reference implementation with strong local evidence and incomplete target-cloud verification**, not as a production-proven commercial system.

---

# 2. Current Reliora Product and Architecture Baseline

## 2.1 Historical P1-S1 baseline

The preserved P1-S1 baseline remains an important source of provenance.

The frozen Stage-1 manifest records:

- the original AgentCore Harness;
- prompt-based three-way routing;
- embedded FAQ behaviour;
- human handoff behaviour;
- AgentCore Gateway;
- Lambda;
- DynamoDB ticket persistence;
- Bedrock evaluation;
- an aggregate 6/6 correctness result.

The same manifest also records later-discovered behavioural gaps that the aggregate score did not reveal, including:

- asking for multiple missing bug fields at once;
- exposing an internal route label;
- exposing development reasoning tags;
- omitting policy detail while still scoring as correct.

**Audit classification:** `ADEQUATE`

**Decision:** Preserve unchanged as historical provenance.

## 2.2 Current product identity

Reliora is defined as:

> **AI Customer-Support Reliability and Control Platform for Online Commerce**

The product thesis is not “a chatbot.” It is a reliability/control layer around probabilistic AI behaviour.

The primary target customer is a small-to-mid-size or growing online retailer.

Potential buyer roles are already hypothesized, including:

- Head of Customer Support;
- Customer Experience leader;
- CTO / VP Engineering;
- Head of AI / Automation;
- E-commerce Operations;
- Platform Engineering.

These are **buyer hypotheses**, not validated customers.

**Audit classification:** `ADEQUATE` for product definition; `PARTIAL` for customer validation.

## 2.3 Current implementation baseline

The correct current implementation audit baseline is not `main`.

The branch lineage is:

```text
main @ cc02e58
    |
    +-- feat/aws-infrastructure @ da0d028
            |
            +-- feat/failure-telemetry-emission @ 88c13ba
```

The current feature line includes:

- source runtime;
- tests;
- evaluation tooling;
- experiments;
- evidence;
- Terraform;
- GitHub Actions;
- governance and operations documents.

A separate `docs/security-privacy-hardening` branch contains additional privacy/security work but has diverged from the current infrastructure branch.

**Audit classification:** `PARTIAL`

Reason: implementation is substantial, but current project truth is distributed across multiple branches and dated documentation snapshots.

## 2.4 Current evidence baseline

The evidence maturity register establishes the following broad state:

- E1: unit/static quality evidence;
- E2: local integration evidence;
- E3: controlled local synthetic measurement for selected routing/performance experiments;
- E4+: not yet established for current target-cloud capabilities;
- E7-E9: no beta, production, or independent-assurance evidence.

The evidence register previously recorded 200 passing tests. The latest telemetry branch adds additional tests, but no current GitHub status result was observed for the latest tip during this audit.

Therefore this audit **does not assert a new exact current test total**.

**Audit classification:** `ADEQUATE` evidence discipline; `PARTIAL` evidence freshness.

---

# 3. Source-Authority Map

## 3.1 Reliora product-specific authority

Use the following precedence when determining what Reliora is:

1. **Official Udacity/AWS P1 project specification and mandatory rubric**
2. **Reliora Product Constitution**
3. **Reliora Product North Star**
4. **Reliora-specific requirements, ADRs, policies, architecture, evaluation contracts, and preserved evidence**
5. **Portfolio Product Engineering Standard**
6. **Reliora delivery blueprint / execution guidance**
7. **Universal charters as quality/process comparison lenses**
8. **External/general engineering knowledge**

The more specific Reliora source wins over a broader universal source.

## 3.2 Universal source role

The universal documents may ask:

- Was discovery adequate?
- Was an alternative considered?
- Was evidence classified correctly?
- Is there an operational owner?
- Can the system be recovered?
- Are claims bounded by evidence?

They must not imply:

- Reliora needs RAG;
- Reliora needs multi-agent orchestration;
- Reliora needs Kubernetes;
- Reliora needs a vector database;
- Reliora needs another cloud;
- Reliora needs enterprise multi-tenancy.

## 3.3 Learning Ledger authority

The AWS Agentic AI Learning Ledger is not a product source of truth.

Its purpose is to preserve:

- reusable concepts;
- command knowledge;
- troubleshooting;
- architecture lessons;
- interview narratives.

The product repository should answer:

> What did Reliora build?

The Learning Ledger should answer:

> Why was it built this way, how does it work, what failed, and what was learned?

**Audit classification:** `ADEQUATE`

## 3.4 Source-control inconsistency

The Product Constitution references the North Star as governing source, but the current audited GitHub tree does not contain the North Star file even though the document exists in the project sources.

This creates a small but real source-authority ambiguity for anyone reviewing the repository alone.

**Audit classification:** `PARTIAL`

---

# 4. Lifecycle and Discovery Audit

The Forward-Deployed charter requires a sequence resembling:

```text
opportunity
→ discovery
→ solution framing
→ architecture
→ prototype
→ production engineering
→ controlled deployment
→ scale
→ productized learning
```

Reliora did not begin this way.

Its true history is:

```text
Udacity P1-S1 implementation
→ successful submission
→ production-hardening/productization
→ architecture and reliability controls
→ broader governance
→ later adoption of stronger discovery/FDE standards
```

That order must remain visible.

## 4.1 Real-world problem

Reliora has a credible, researched problem thesis:

- aggregate LLM quality can hide behavioural violations;
- AI side effects can be unsafe;
- retries can duplicate business actions;
- failures can be difficult to reconstruct;
- handoff can be poor;
- AI costs can be unclear;
- release regressions can be difficult to detect.

Industry research supports those problem classes.

However, there is no evidence that a specific retailer has validated Reliora's exact problem framing.

**Classification:** `PARTIAL`

## 4.2 Primary user/operator

End users and secondary operators are documented.

The Constitution distinguishes:

- retailer customer;
- support agent;
- support manager;
- reliability engineer;
- engineering team;
- AI platform operator.

**Classification:** `ADEQUATE` as hypothesis/design.

## 4.3 Buyer/economic owner

Potential buyers are documented.

No real buyer discovery or economic-owner interview evidence exists.

**Classification:** `PARTIAL`

## 4.4 Current alternatives and incumbent workflow

Reliora has strong technical alternatives analysis for specific architecture questions such as:

- LLM routing vs deterministic/classical routing;
- embedded/versioned knowledge vs RAG;
- prompt-only authorization vs deterministic application authorization;
- local in-memory vs durable DynamoDB execution semantics.

What is missing is the **product-level incumbent workflow**:

- how a representative retailer handles these cases today;
- what current support stack exists;
- what failure/retry processes exist today;
- what manual controls are already in place;
- what commercial SaaS alternatives already solve part of the problem.

**Classification:** `MISSING`

## 4.5 Problem frequency and severity

Industry research provides general evidence that reliability, cost, handoff, and governance are real customer-service AI concerns.

Reliora does not have customer-specific frequency/severity measurements.

**Classification:** `PARTIAL`

## 4.6 Baseline before solution

Reliora has a strong **technical baseline** in the frozen P1-S1 system.

It does not yet have a strong **business/current-workflow baseline** such as:

- support time;
- duplicate-ticket frequency;
- human rework;
- false automation cost;
- mean time to diagnose;
- cost per eligible resolution.

**Classification:** `PARTIAL`

## 4.7 Assumptions vs validated facts

Reliora's evidence discipline is strong.

The project explicitly separates:

- TARGET;
- OBSERVED;
- EXPERIMENTAL;
- MEASURED;
- SYNTHETIC;
- BLOCKED;
- evidence maturity levels.

That discipline materially reduces the risk of fake validation.

**Classification:** `ADEQUATE`

## 4.8 Problem-buyer evidence gate

No explicit formal gate exists that says:

> Do we have enough problem/buyer evidence to continue investing in this product direction?

**Classification:** `MISSING`

## 4.9 Kill, pivot, and narrow conditions

Feature admission tests and reconsideration triggers exist.

However, there is no explicit product-level statement of:

- when Reliora should be abandoned;
- when its scope should narrow;
- when the buyer hypothesis should change;
- when the product thesis should pivot.

**Classification:** `MISSING`

## 4.10 Grounding level

Using the later FDE charter only as a comparison lens, Reliora is best described as:

> **a research-grounded synthetic/reference product case**

It is not yet:

- domain-expert validated;
- design-partner validated;
- pilot validated;
- production validated.

**Classification:** `UNPROVEN` beyond research-grounded reference status.

---

# 5. North Star and Constitution Audit

## 5.1 Product direction consistency

The North Star and Constitution are aligned around:

- AI support reliability/control;
- online commerce;
- deterministic authority;
- safe side effects;
- evidence;
- human escalation;
- cost;
- observability;
- regression protection.

No material contradiction was found in product identity.

**Classification:** `ADEQUATE`

## 5.2 Non-goals

The product explicitly excludes, absent independent evidence:

- multi-agent;
- persistent personalized memory;
- mandatory RAG;
- browser;
- code interpreter;
- EKS;
- Kafka;
- Redis;
- MLflow;
- full commerce backend;
- multi-region;
- enterprise tenancy.

**Classification:** `ADEQUATE`

## 5.3 Architectural invariants

Strongly defined invariants include:

- the LLM may propose; deterministic software authorizes;
- no premature side effect;
- stable logical operation identity;
- matching retry replay;
- conflict rejection;
- authoritative backend confirmation;
- unsupported knowledge must not become invented policy;
- critical deterministic failures can block release;
- public claims must remain within evidence.

**Classification:** `ADEQUATE`

## 5.4 Claim/evidence boundaries

The Constitution, evidence maturity register, and metric dictionary strongly enforce evidence-bounded claims.

**Classification:** `ADEQUATE`

## 5.5 Technology-admission rules

The feature-admission and tool-selection rules are explicit.

**Classification:** `ADEQUATE`

## 5.6 Autonomy boundaries

The autonomy policy is explicit and risk-tiered.

**Classification:** `ADEQUATE` in design; implementation coverage remains partial.

## 5.7 Implementation-entry rules

The Decision Journal's evidence gate and the later RJ-039 process guardrail are strong.

**Classification:** `ADEQUATE` in governance.

## 5.8 Kill conditions

No explicit product-level kill/pivot/narrow conditions are present.

**Classification:** `MISSING`

## 5.9 Documentation freshness

The Constitution and README contain stale project-status snapshots.

Examples include:

- 164-test baseline;
- Phase 0 / AWS Cloud 0 language;
- older branch/commit status.

These do not invalidate governing principles, but they can mislead a reviewer about the current state.

**Classification:** `PARTIAL`

## 5.10 Amendment recommendation

Do not silently rewrite historical sections.

After the audit, make a controlled amendment that:

- marks old status sections as dated snapshots;
- adds a new current-status note;
- adds discovery/kill-condition governance;
- restores the North Star into the canonical repository if desired.

---

# 6. Architecture Audit

## 6.1 Core bounded responsibilities

The logical architecture clearly separates:

- Serving Plane;
- Tool / Side-Effect Plane;
- Evaluation and Control Plane;
- Operations and Governance Plane.

**Classification:** `ADEQUATE`

## 6.2 Authoritative state

For ticket creation, authoritative state is well defined:

- operation state in durable persistence;
- ticket state in durable persistence;
- backend confirmation required for customer-visible success.

**Classification:** `ADEQUATE` locally; `UNPROVEN` in target cloud.

## 6.3 Domain model

The current domain model explicitly represents:

- support request;
- intent;
- routing decision;
- bug draft;
- bug fields;
- logical bug-report operation;
- execution status;
- ticket confirmation.

**Classification:** `ADEQUATE` for current implemented ticket scope.

## 6.4 AI entry and exit points

The architecture clearly treats model output as proposed input to deterministic controls.

**Classification:** `ADEQUATE` in architecture.

## 6.5 Policy and authorization

Deterministic authorization precedes ticket execution.

**Classification:** `ADEQUATE` locally.

## 6.6 Approval / HITL

Risk 0 and Risk 1 policies are documented.

Higher-risk actions are out of current scope.

Structured human handoff is required but not fully implemented in the current runtime tree.

**Classification:** `PARTIAL`

## 6.7 Idempotency

Strong local design:

- operation ID;
- deterministic fingerprint;
- matching replay;
- conflict;
- conditional durable creation;
- strongly consistent reconciliation.

**Classification:** `ADEQUATE` at local/integration maturity; `UNPROVEN` in live AWS.

## 6.8 Ambiguous mutation handling

The DynamoDB adapter explicitly reconciles:

- transaction cancellation;
- read timeout after uncertain mutation;
- absent durable state;
- incomplete durable state.

It returns `UNCONFIRMED` rather than fabricating success.

**Classification:** `ADEQUATE` locally.

## 6.9 Postcondition verification

Backend confirmation is required.

However, end-to-end verification through AgentCore/Gateway/Lambda/DynamoDB is not yet demonstrated.

**Classification:** `PARTIAL / UNPROVEN`

## 6.10 Evidence model

Strongly defined.

**Classification:** `ADEQUATE`

## 6.11 Tenant/security boundaries

Reliora is not currently an enterprise multi-tenant SaaS product.

Enterprise multi-tenancy is explicitly outside scope.

**Classification:** `NOT_APPLICABLE` for enterprise tenancy.

Isolation for a single customer/environment still requires normal IAM/data-boundary verification.

## 6.12 Persistence

Current durable design is appropriately narrow.

**Classification:** `ADEQUATE` in design/local implementation.

## 6.13 Failure/degraded modes

Failure-mode analysis is extensive.

Many documented failure modes remain TARGET rather than verified.

**Classification:** `PARTIAL`

## 6.14 Observability

Design is strong, implementation incomplete.

**Classification:** `PARTIAL / UNPROVEN`

## 6.15 Deployment topology

The Lambda/DynamoDB core is expressed in Terraform.

The full AgentCore/Gateway path is not yet captured and proven as the complete physical deployment.

**Classification:** `PARTIAL / UNPROVEN`

## 6.16 Portability

Portability is selective and focused on replaceable product boundaries rather than fake multi-cloud neutrality.

**Classification:** `ADEQUATE`

## 6.17 Smallest justified architecture

No evidence was found that the current system is unnecessarily distributed.

The current design remains relatively small.

**Classification:** `ADEQUATE`

---

# 7. Domain Model and Lifecycle Audit

## 7.1 Bug collection lifecycle

`BugReportDraft` expresses:

- description;
- steps to reproduce;
- environment;
- missing fields;
- completeness;
- next missing field.

This is enough to make incremental collection deterministic without introducing a large state-machine framework.

**Classification:** `ADEQUATE`

## 7.2 Side-effect lifecycle

The execution model distinguishes:

- CREATED;
- REPLAYED;
- CONFLICT;
- UNCONFIRMED.

This is a major strength.

Partial or ambiguous outcomes remain partial rather than silently becoming success.

**Classification:** `ADEQUATE`

## 7.3 Legal/illegal transitions

Critical illegal actions are already represented through authorization, idempotency, and result semantics.

A formal general-purpose state-machine abstraction is not currently justified.

**Classification:** `ADEQUATE / NO CHANGE`

## 7.4 Requested vs current vs derived state

The current design distinguishes:

- customer-collected draft state;
- proposed logical operation;
- authorization result;
- durable operation state;
- authoritative confirmation;
- replay/conflict/unconfirmed execution result.

**Classification:** `ADEQUATE`

## 7.5 Whole support lifecycle

The entire support lifecycle is not yet represented as one implemented typed workflow.

In particular:

- structured handoff is still mostly policy/requirements;
- platform knowledge coverage is more strongly specified than implemented in the current runtime tree;
- end-to-end AgentCore conversation state remains unproven.

**Classification:** `PARTIAL`

**Decision:** Do not add abstraction merely for symmetry. Implement only the missing product-required transitions.

---

# 8. Authority, Policy, and Autonomy Audit

## 8.1 Truth sources

Reliora correctly distinguishes:

- approved knowledge as platform-answer authority;
- deterministic application logic as side-effect authorization authority;
- DynamoDB/backend result as ticket-outcome authority;
- telemetry as operational evidence, not business authority.

**Classification:** `ADEQUATE`

## 8.2 AI authority

AI may:

- classify;
- extract;
- summarize;
- propose;
- generate customer-facing text within bounded rules.

AI may not independently authorize persistent side effects.

**Classification:** `ADEQUATE`

## 8.3 Risk levels

The autonomy policy defines four levels from informational to financial/security/legal/irreversible.

The current product only allows autonomous informational support and validated low-risk bug-ticket creation.

**Classification:** `ADEQUATE`

## 8.4 Evidence required to increase autonomy

The policy says higher-risk operations require stronger deterministic authorization or human approval.

What remains less explicit is a promotion protocol such as:

```text
risk level
→ evidence threshold
→ approval authority
→ rollout condition
```

for any future autonomy increase.

This is not currently a blocker because higher-risk actions are out of scope.

**Classification:** `PARTIAL`, low urgency.

## 8.5 Bypass risk

At the local application layer, authorization precedes execution.

At the full AgentCore/Gateway transport layer, trusted operation identity remains unproven.

Until ADR-017 is resolved experimentally, the complete bypass-proof execution chain is not established in the target environment.

**Classification:** `UNPROVEN`

---

# 9. Execution, Idempotency, Reconciliation, and Verification Audit

This is one of Reliora's strongest areas.

## 9.1 Stable logical operation identity

Defined in domain model and requirements.

**Classification:** `ADEQUATE` locally.

## 9.2 Duplicate suppression

Implemented through operation-state lookup, conditional transactional write, replay semantics, and conflict detection.

**Classification:** `ADEQUATE` locally.

## 9.3 Retry semantics

Matching retry and conflict semantics are explicit.

**Classification:** `ADEQUATE`

## 9.4 Timeout-after-success

The durable adapter treats read timeout as ambiguous and reconciles against authoritative operation state.

**Classification:** `ADEQUATE` locally.

## 9.5 Timeout without authoritative state

Returns `UNCONFIRMED`.

**Classification:** `ADEQUATE`

## 9.6 Partial/incomplete persisted state

Incomplete operation state returns `UNCONFIRMED`.

**Classification:** `ADEQUATE`

## 9.7 Access denied

Access-denied backend errors propagate rather than being misclassified as an ambiguous successful write.

The latest branch also emits an authorization failure event without allowing telemetry failure to replace the primary error.

**Classification:** `ADEQUATE` locally.

## 9.8 Safe reconciliation

Strongly consistent operation reads are used.

**Classification:** `ADEQUATE`

## 9.9 Operation success vs business outcome

The model is explicit: execution status and confirmation are separate.

**Classification:** `ADEQUATE`

## 9.10 Remaining evidence boundary

All of the above is currently strongest at local/integration maturity.

Live target-cloud behaviour remains unproven.

**Classification:** `UNPROVEN` for cloud claims.

---

# 10. Evidence, Observability, and Auditability Audit

## 10.1 Evidence classification

Excellent.

**Classification:** `ADEQUATE`

## 10.2 Evidence maturity

E0-E9 is explicitly tracked.

**Classification:** `ADEQUATE`

## 10.3 Metric governance

The metric dictionary defines:

- meaning;
- measurement boundary;
- unit;
- source of truth;
- aggregation;
- evidence;
- maturity;
- claim boundary;
- owner.

**Classification:** `ADEQUATE`

## 10.4 Authoritative state vs telemetry

The architecture does not treat observability as business authority.

**Classification:** `ADEQUATE`

## 10.5 Failure taxonomy

A typed failure taxonomy now exists.

**Classification:** `ADEQUATE` as contract.

## 10.6 Failure telemetry emission

The latest DynamoDB adapter can emit structured failure events.

However, the actual Lambda composition currently constructs the execution coordinator without a `failure_telemetry` sink.

Therefore:

```text
telemetry contract exists
+ adapter emission exists
!= runtime telemetry is wired and operational
```

**Classification:** `PARTIAL`

## 10.7 End-to-end reconstruction

CloudWatch request reconstruction is still E0/TARGET/BLOCKED in the evidence register.

A case cannot yet be proven reconstructable through:

- actor;
- input boundary;
- decision;
- policy;
- operation;
- backend result;
- reconciliation;
- failure;
- deployment/version context.

**Classification:** `UNPROVEN`

## 10.8 Public claims

Current claim discipline is strong.

**Classification:** `ADEQUATE`

---

# 11. Tenancy, Security, Privacy, and Deployment Boundaries Audit

## 11.1 Tenancy

Enterprise multi-tenancy is explicitly out of scope.

**Classification:** `NOT_APPLICABLE`

## 11.2 Workload identity and least privilege

Terraform defines a dedicated Lambda role with narrow DynamoDB and log permissions.

**Classification:** `ADEQUATE` in source; `UNPROVEN` in target environment.

## 11.3 Secrets

No long-lived repository credentials are intended.

The separate security/privacy branch records successful local secret-history scans.

Current CI does not yet include a secret-scanning step.

**Classification:** `PARTIAL`

## 11.4 Prompt injection

Threat and NFR coverage exist.

No current complete adversarial release gate was identified.

**Classification:** `PARTIAL`

## 11.5 Data egress and logging

Minimization is strongly documented.

The newer failure-event contract deliberately avoids customer payload content.

**Classification:** `ADEQUATE` in design; operational enforcement `UNPROVEN`.

## 11.6 Privacy and deletion

A strong data-lifecycle policy exists on `docs/security-privacy-hardening`.

It is not part of the current audited implementation branch.

Operational deletion/retention enforcement in AWS remains unproven.

**Classification:** `PARTIAL`

## 11.7 Supplier/model/provider risk

The universal delta assessment recognizes supplier/provider risk as applicable.

A dedicated current provider-risk package was not found in the audited branch.

**Classification:** `PARTIAL`

## 11.8 Vulnerability/security assurance

Threat modelling exists.

The current GitHub Actions workflow does not yet run Gitleaks/Checkov or a dedicated adversarial security gate.

**Classification:** `PARTIAL`

## 11.9 Incident response

Failure analysis and diagnostics exist.

A complete hosted-service incident lifecycle is not yet needed for an unhosted reference implementation, but should precede real pilot operation.

**Classification:** `PARTIAL / DEFERRED WITH RATIONALE`

---

# 12. Persistence and Recovery Audit

## 12.1 Durable state ownership

Two durable responsibilities are explicit:

- operations table keyed by `operation_id`;
- tickets table keyed by `ticket_id`.

**Classification:** `ADEQUATE`

## 12.2 Current state vs history

Current operation/ticket state is represented.

A broader event-history model is not currently required.

**Classification:** `ADEQUATE / NO CHANGE`

## 12.3 Transaction boundary

Operation and ticket creation use a DynamoDB transaction.

**Classification:** `ADEQUATE`

## 12.4 Concurrent updates

Conditional write + reconciliation handles concurrent logical-operation claims.

**Classification:** `ADEQUATE` locally.

## 12.5 Crash/ambiguous recovery

The design explicitly reconciles uncertain writes.

**Classification:** `ADEQUATE` locally.

## 12.6 Process restart semantics

Durable operation state means replay semantics need not rely on in-process memory in the AWS adapter.

**Classification:** `ADEQUATE` in design/local integration.

## 12.7 Configuration versioning

Requirements expect deployment provenance for model/prompt/router/knowledge/application versions.

That deployed provenance has not yet been demonstrated.

**Classification:** `PARTIAL / UNPROVEN`

## 12.8 Retention/deletion effects

Policy exists, operational enforcement not yet demonstrated.

**Classification:** `PARTIAL`

## 12.9 Recovery/DR/rollback

There is no complete current recovery/DR runbook proving:

- restore;
- rollback;
- redeploy;
- data recovery;
- configuration restoration;
- evidence preservation.

**Classification:** `MISSING`

---

# 13. AI and Tooling Admission Audit

## 13.1 Current capability classification

| Capability | Classification | Reason |
|---|---|---|
| Bedrock / managed model | CORE | Official P1 baseline and AI support requirement |
| AgentCore Harness/runtime | CORE, CLOUD UNPROVEN | Official baseline; target integration still requires evidence |
| AgentCore Gateway | CORE, CLOUD UNPROVEN | Controlled tool path in official baseline |
| Lambda | CORE | Current side-effect runtime |
| DynamoDB | CORE | Current durable operation/ticket state |
| Small approved knowledge source | CORE | Current knowledge scope is small and stable |
| Deterministic routing / classical routing candidates | EXPERIMENTAL / EVIDENCE-DRIVEN | Explicitly benchmarked as alternatives |
| Deterministic evaluator | CORE | Protects hard behavioural invariants |
| LLM-as-judge / generative evaluation | OPTIONAL/COMPLEMENTARY | Appropriate for judgement-like qualities |
| Structured handoff | CORE PRODUCT CAPABILITY, PARTIAL | Required by Reliora requirements |
| Failure telemetry | CORE OPERABILITY CAPABILITY, PARTIAL | Required for diagnosis, but not fully wired |
| CloudWatch | CORE TARGET OPERABILITY | Needed for AWS operational evidence |
| Terraform | CORE DELIVERY CAPABILITY | Reproducible persistent infrastructure |
| GitHub Actions | CORE DELIVERY CAPABILITY | Quality/release controls |
| RAG / vector database | DEFERRED / NOT JUSTIFIED | No demonstrated corpus/retrieval need |
| Multi-agent system | REJECTED / NOT JUSTIFIED | No Reliora requirement |
| AgentCore Browser | REJECTED / NOT JUSTIFIED | No Reliora requirement |
| Code Interpreter | REJECTED / NOT JUSTIFIED | No Reliora requirement |
| Kubernetes / EKS | REJECTED / NOT JUSTIFIED | Current architecture does not require orchestration |
| Kafka / MSK | REJECTED / NOT JUSTIFIED | No streaming requirement |
| Redis | REJECTED / NOT JUSTIFIED | No demonstrated caching/state requirement |
| Enterprise multi-tenancy | DEFERRED / OUT OF SCOPE | Explicit current product boundary |
| Multi-region | DEFERRED / NOT JUSTIFIED | No current requirement/evidence |
| Docker | OPTIONAL / DEFERRED | Useful for local product mode if it solves a concrete delivery need |

## 13.2 Admission conclusion

Reliora's tool-admission discipline is already strong.

**Classification:** `ADEQUATE`

---

# 14. Component and Deployment Architecture Audit

## 14.1 Smallest architecture

The current component model is narrow and defensible.

**Classification:** `ADEQUATE`

## 14.2 Distribution

Reliora does not currently show unjustified microservice decomposition.

**Classification:** `ADEQUATE`

## 14.3 AWS coupling

Reliora is intentionally AWS-first, with selective provider boundaries.

**Classification:** `INTENTIONAL_DEVIATION` from cloud-neutral architecture.

This is justified by:

- program context;
- official P1 baseline;
- portfolio AWS focus;
- defined replaceable application boundaries.

## 14.4 Physical deployment completeness

Terraform currently covers the Lambda/DynamoDB/IAM/logging core.

The full AgentCore/Gateway integration remains unproven.

**Classification:** `PARTIAL / UNPROVEN`

## 14.5 Local/cloud mode strategy

The Constitution defines Local Demo, AWS Integration, and Ephemeral Portfolio Cloud modes.

The local/cloud product experience is not yet implemented end to end.

**Classification:** `PARTIAL`

## 14.6 Frontend/operator surfaces

They are product targets, not current evidence.

**Classification:** `UNPROVEN`

---

# 15. Architecture Validation / Implementation Gate Audit

Reliora already has several pieces of the intended gate:

```text
architecture
→ experiments
→ decisions
→ implementation
→ evidence
```

Strong existing examples include:

- routing benchmark before final routing selection;
- held-out test discipline;
- ADR-017 refusing to accept an unverified identity mechanism;
- local reference semantics before AWS persistence;
- performance evidence kept within local claim boundaries;
- RJ-039 candidate-architecture evidence gate.

## 15.1 Decision classes

### GOVERNING

The following should be treated as governing unless evidence explicitly overturns them:

- Reliora is a reliability/control product, not a chatbot demo.
- Product requirements select technology.
- The LLM may propose; deterministic software authorizes.
- Authorization precedes side-effect execution.
- Logical operation identity is distinct from request identity.
- Matching retry must not duplicate a business side effect.
- Backend truth is required before customer-visible success.
- Public claims remain within evidence.
- Cross-project contamination is prohibited.

### BASELINE

The following are accepted current baseline choices:

- P1 functional path: AgentCore/Gateway/Lambda/DynamoDB.
- Small approved knowledge source for current scope.
- Provider boundary for ticket backends.
- Terraform for persistent AWS infrastructure.
- GitHub Actions for quality automation.
- Evidence maturity + metric-governance model.
- Routing benchmark methodology.

### PROVISIONAL

The following are reasonable but incomplete implementation choices:

- current physical AWS topology beyond Lambda/DynamoDB;
- telemetry sink implementation and runtime wiring;
- structured handoff implementation shape;
- full release workflow;
- storefront/operator product surfaces;
- local/cloud runtime-switching implementation.

### UNPROVEN

The following require real experiment/integration evidence:

- ADR-017 trusted operation identity through AgentCore/Gateway/Lambda;
- live DynamoDB replay/conflict behaviour;
- end-to-end AgentCore/Gateway controlled ticket path;
- CloudWatch request reconstruction;
- cloud latency/throughput/cost;
- rollback/recovery;
- deployed prompt/model/router/knowledge provenance;
- real adversarial security behaviour;
- product adoption/value realization.

## 15.2 CI gate

A quality workflow exists and runs:

- dependency sync;
- Ruff;
- mypy;
- pytest;
- Lambda package build/verification;
- Terraform fmt/init/validate.

The current workflow does not yet visibly include:

- deterministic evaluation runner;
- Gitleaks;
- Checkov;
- target-cloud plan/deploy;
- release evidence generation.

No current combined status checks were observed for the latest telemetry tip during this audit.

**Classification:** `PARTIAL / UNPROVEN`

---

# 16. Gap Register

## GAP-LC-001

**Area**
Discovery / customer evidence

**Current evidence**
Research-backed product thesis, target users/buyers, P1 technical baseline, production research.

**Observation**
No formal Reliora customer-discovery record exists in the live repository. Current-state workflow, stakeholder conflicts, buyer evidence, incumbent tools, and customer-specific pain are not formally captured.

**Classification**
`PARTIAL`

**Risk if unchanged**
Reliora can become technically impressive while its product value remains based on plausible assumptions rather than disciplined product discovery.

**Independent Reliora justification**
Reliora claims to be a commercially credible product reference implementation for retailers.

**Recommended action**
Create a retrospective discovery brief clearly labelled as synthetic/research-grounded. Separate known facts, industry evidence, assumptions, and open validation questions.

**Evidence required to close**
Reviewed discovery artifact + traceability to source evidence + explicit unresolved assumptions.

**Priority**
`P1`

---

## GAP-LC-002

**Area**
Problem-buyer gate / kill-pivot-narrow governance

**Current evidence**
Feature admission test, reconsideration triggers, non-goals.

**Observation**
No explicit product-level problem-buyer evidence gate or kill/pivot/narrow criteria were found.

**Classification**
`MISSING`

**Risk if unchanged**
The project can continue accumulating engineering work even if future evidence weakens the buyer/problem thesis.

**Independent Reliora justification**
The product should remain outcome-driven and evidence-led.

**Recommended action**
Add a concise product continuation gate defining:
- continue;
- narrow;
- pivot;
- stop;
based on problem evidence, buyer evidence, adoption potential, risk, cost, and technical feasibility.

**Evidence required to close**
Accepted product-governance amendment.

**Priority**
`P1`

---

## GAP-LC-003

**Area**
Solution framing / business case

**Current evidence**
Strong component-level alternatives, routing experiment, RAG rejection rationale, architecture decisions.

**Observation**
No complete product-level alternatives analysis and value hypothesis compares Reliora against:
- existing human workflow;
- deterministic workflow automation;
- conventional chatbot/helpdesk SaaS;
- narrower reliability middleware;
- current approach with no change.

**Classification**
`PARTIAL`

**Risk if unchanged**
Architecture may be justified locally without proving the full product approach is the simplest economically defensible intervention.

**Independent Reliora justification**
The product standard requires measurable business value and technology admission.

**Recommended action**
Create a concise product-level alternatives/value hypothesis, using synthetic assumptions where real numbers do not exist.

**Evidence required to close**
Reviewed alternatives matrix + business-value hypothesis + clearly synthetic assumptions.

**Priority**
`P1`

---

## GAP-GOV-001

**Area**
Source authority and documentation freshness

**Current evidence**
Constitution, North Star in project sources, Decision Journal, live repo history.

**Observation**
North Star is not present in the audited GitHub tree; README/Constitution/Decision Journal contain dated implementation snapshots.

**Classification**
`PARTIAL`

**Risk if unchanged**
Reviewers or future agents can audit the wrong source state or treat old snapshots as current facts.

**Independent Reliora justification**
Reliora explicitly depends on source precedence and evidence provenance.

**Recommended action**
After audit, reconcile governing source placement and add dated current-status amendments without rewriting historical snapshots.

**Evidence required to close**
Canonical source map + repository presence or explicit external-source reference + refreshed status note.

**Priority**
`P3`

---

## GAP-ARCH-001

**Area**
Trusted execution identity

**Current evidence**
ADR-017, local identity resolver, local tests, operation identity semantics.

**Observation**
Real AgentCore/Gateway/Lambda propagation of trusted `request_id`, `session_id`, and especially stable `operation_id` is not yet proven. ADR-017 explicitly remains PROPOSED.

**Classification**
`UNPROVEN`

**Risk if unchanged**
The end-to-end idempotency guarantee may rely on identity semantics that the actual transport does not preserve.

**Independent Reliora justification**
FR-001/002/003/010/011/012 and the core retry-safety architecture depend on trusted logical-operation identity.

**Recommended action**
Run the smallest possible target-environment identity experiment before broad AgentCore integration.

**Evidence required to close**
Real integration evidence proving:
- model cannot override identity;
- retry reuses operation ID;
- retry may use a new request ID;
- new logical action gets new operation ID;
- DynamoDB replay works.

**Priority**
`P0`

---

## GAP-DOM-001

**Area**
Structured human handoff

**Current evidence**
FR-017/018, autonomy policy, logical architecture.

**Observation**
Structured handoff is a strong design requirement but no complete implemented handoff runtime/schema path was identified in the current source tree.

**Classification**
`PARTIAL`

**Risk if unchanged**
One of Reliora's core product differentiators remains documentation-only.

**Independent Reliora justification**
Unsupported, ambiguous, failed, and higher-risk cases must transition safely without forcing customer repetition.

**Recommended action**
Implement the smallest typed handoff contract and one end-to-end handoff path after discovery/gate work.

**Evidence required to close**
Unit + integration tests; product scenario showing context-preserving handoff with minimized data.

**Priority**
`P1`

---

## GAP-OBS-001

**Area**
Failure telemetry and reconstructability

**Current evidence**
Failure taxonomy, FailureEvent contract, adapter emission, failure tests, logical observability model.

**Observation**
The Lambda entrypoint does not currently inject a telemetry sink into the durable execution coordinator. Cloud request reconstruction remains unproven.

**Classification**
`PARTIAL / UNPROVEN`

**Risk if unchanged**
Failure telemetry exists as an architectural capability but may not be emitted in the real runtime.

**Independent Reliora justification**
Poor failure diagnosis is a primary Reliora business/engineering problem.

**Recommended action**
Wire a minimal approved telemetry sink and prove one request/failure reconstruction; do not build a new observability platform.

**Evidence required to close**
Correlated runtime evidence for one controlled success and one controlled failure, with no customer-payload leakage.

**Priority**
`P2`

---

## GAP-SEC-001

**Area**
Security assurance automation

**Current evidence**
Threat model, IAM source, local secret-scan evidence on another branch, security NFRs.

**Observation**
Current CI does not visibly enforce secret scanning, IaC scanning, or a dedicated adversarial/prompt-injection gate.

**Classification**
`PARTIAL`

**Risk if unchanged**
Security remains partly a design/documentation property rather than an automated release property.

**Independent Reliora justification**
Reliora executes business side effects and handles potentially sensitive support content.

**Recommended action**
Integrate only justified lightweight checks:
- Gitleaks;
- Checkov or equivalent;
- targeted adversarial deterministic tests.

**Evidence required to close**
CI run evidence + documented scope/limitations.

**Priority**
`P2`

---

## GAP-PRIV-001

**Area**
Privacy/data lifecycle canonicalization

**Current evidence**
Strong data-lifecycle policy on `docs/security-privacy-hardening`; current NFRs and telemetry minimization.

**Observation**
The strongest data-lifecycle artifact is on a divergent branch and operational retention/deletion remains unverified.

**Classification**
`PARTIAL`

**Risk if unchanged**
Governance truth can diverge from current implementation and teardown behaviour.

**Independent Reliora justification**
Reliora explicitly commits to data minimization, retention, deletion, and claim discipline.

**Recommended action**
Reconcile the branch after audit; keep policy implementation proportional to the actual data stores.

**Evidence required to close**
Canonical merged policy + retention/deletion configuration or verification evidence where applicable.

**Priority**
`P2`

---

## GAP-REC-001

**Area**
Recovery / rollback / DR

**Current evidence**
Terraform intent, rollback requirement, failure analysis, deploy/destroy philosophy.

**Observation**
No complete current recovery/DR/rollback runbook and no restoration exercise were found.

**Classification**
`MISSING`

**Risk if unchanged**
Reliora can describe how to deploy but not yet prove how to return to a known-good state after bad deployment or data/runtime failure.

**Independent Reliora justification**
Failure handling and recoverability are core product claims.

**Recommended action**
Define the smallest scope-appropriate recovery runbook before pilot claims.

**Evidence required to close**
Runbook + at least one controlled rollback/redeploy verification when cloud access exists.

**Priority**
`P2`

---

## GAP-CI-001

**Area**
Implementation/release gate

**Current evidence**
GitHub Actions quality gate.

**Observation**
The workflow covers static/test/IaC validation but not the complete intended release gate. The latest feature-tip CI result was not observed.

**Classification**
`PARTIAL / UNPROVEN`

**Risk if unchanged**
A change can pass code quality while bypassing deterministic behavioural evaluation or security checks.

**Independent Reliora justification**
Reliora explicitly exists to prevent behavioural regression.

**Recommended action**
Extend the existing workflow rather than create a second CI system.

**Evidence required to close**
One successful gate and one deliberately failing unsafe-change gate.

**Priority**
`P1`

---

## GAP-EVID-001

**Area**
Current evidence freshness

**Current evidence**
Evidence maturity register records a prior 200-test baseline; newer telemetry work exists.

**Observation**
The current branch has advanced beyond some documented evidence snapshots.

**Classification**
`PARTIAL`

**Risk if unchanged**
Claims can accidentally refer to an older code state.

**Independent Reliora justification**
Evidence provenance is a governing Reliora principle.

**Recommended action**
Before implementation resumes, freeze a fresh audit baseline:
- commit;
- test result;
- Ruff;
- mypy;
- Terraform validation;
- deterministic evals.

**Evidence required to close**
Versioned baseline manifest for the current post-audit branch.

**Priority**
`P1`

---

## GAP-AWS-001

**Area**
Target-environment verification

**Current evidence**
Terraform validation, local AWS adapter tests, E0-E3 evidence.

**Observation**
Live AWS integration evidence is not established for the current Reliora architecture.

**Classification**
`UNPROVEN`

**Risk if unchanged**
Local distributed-system assumptions remain unverified at real service boundaries.

**Independent Reliora justification**
Reliora's product thesis includes AgentCore/Gateway/Lambda/DynamoDB operation and AWS deployment.

**Recommended action**
Promote evidence incrementally E4→E6 once a target account is available.

**Evidence required to close**
Target-environment integration, controlled fault experiments, end-to-end verification.

**Priority**
`P1` dependency, not a reason to add architecture.

---

## GAP-OPS-001

**Area**
Operational ownership / incident lifecycle / handoff

**Current evidence**
Diagnostic playbook, failure-mode analysis, universal-charter delta assessment.

**Observation**
Strong diagnostic content exists, but complete pilot-ready RACI, incident lifecycle, support ownership, and commercial operational handoff are not yet canonical in the current branch.

**Classification**
`PARTIAL`

**Risk if unchanged**
A future pilot could depend on the original builder instead of a transferable operating model.

**Independent Reliora justification**
Reliora is intended to be maintainable/adaptable by another team.

**Recommended action**
Complete these only before real hosted/pilot operation; do not overbuild now.

**Evidence required to close**
Named ownership, escalation, runbooks, operational handoff checklist.

**Priority**
`P3` now; `P1` before pilot.

---

## GAP-ADOPT-001

**Area**
Adoption/value realization

**Current evidence**
Product-value metrics and buyer hypotheses.

**Observation**
No real beta/pilot usage or adoption evidence exists.

**Classification**
`UNPROVEN / DEFERRED WITH RATIONALE`

**Risk if unchanged**
None for the current local/reference engineering stage, provided claims remain bounded.

**Independent Reliora justification**
Real customer adoption cannot be invented.

**Recommended action**
Do not fabricate. Define pilot success criteria now; gather real evidence only if/when a real pilot exists.

**Evidence required to close**
Real pilot/beta usage and stakeholder feedback.

**Priority**
`DEFERRED`

---

## GAP-LEDGER-001

**Area**
Learning Ledger synchronization

**Current evidence**
Extensive learning and interview material through 2026-09-09.

**Observation**
The latest ambiguous-write reconciliation and failure-telemetry lessons are not yet captured as dedicated reusable learning entries.

**Classification**
`PARTIAL`

**Risk if unchanged**
Recent high-value engineering lessons may be harder to reuse or explain later.

**Independent Reliora justification**
The portfolio standard explicitly requires extracting reusable lessons without duplicating the product repository.

**Recommended action**
Add concise lessons after the current architecture settles.

**Evidence required to close**
Ledger entry tied to implemented commit/tests.

**Priority**
`P3`

---

## GAP-REPO-001

**Area**
Repository state / branch consolidation

**Current evidence**
Open infrastructure and security/privacy branches; telemetry child branch.

**Observation**
Current truth is distributed across feature branches, including a diverged governance branch.

**Classification**
`PARTIAL`

**Risk if unchanged**
Auditability, source precedence, and future merge correctness degrade.

**Independent Reliora justification**
Git history and source provenance are explicit quality goals.

**Recommended action**
After audit classification, reconcile branches in the smallest dependency-safe order. Do not combine architecture remediation with unrelated merges.

**Evidence required to close**
Clean branch lineage, merged/current governing docs, passing gates.

**Priority**
`P1`

---

# 17. Risk Classification

## Critical architecture risks

### RISK-A — Unproven trusted operation identity

If the actual AgentCore/Gateway path cannot preserve application-owned logical operation identity, the strongest idempotency claims may not hold end to end.

**Severity:** High
**Likelihood:** Unknown until experiment
**Priority:** P0

## High lifecycle risks

### RISK-B — Product engineering outruns product discovery

Reliora may continue accumulating technically strong controls without a formal problem-buyer gate.

**Severity:** Medium-High
**Likelihood:** High given project history
**Priority:** P1

### RISK-C — Release gate incomplete

Code/static checks alone do not prove behavioural release safety.

**Severity:** High
**Likelihood:** Medium
**Priority:** P1

### RISK-D — Current source/evidence fragmentation

Multiple branches and stale status snapshots can cause incorrect audits or claims.

**Severity:** Medium
**Likelihood:** High
**Priority:** P1/P3

## Medium operational risks

### RISK-E — Observability not operationally wired

Failure contracts exist but end-to-end reconstructability is unproven.

**Severity:** Medium-High
**Priority:** P2

### RISK-F — Recovery/rollback not proven

**Severity:** Medium
**Priority:** P2

### RISK-G — Security/privacy controls partly documentation-only

**Severity:** Medium
**Priority:** P2

## Deferred risks

### RISK-H — No adoption evidence

This is expected at current maturity.

**Severity now:** Low
**Priority:** Deferred

---

# 18. Remediation Priority

## P0 — correctness / security / architectural blockers

1. Resolve ADR-017 through the smallest real identity-propagation experiment before depending on AgentCore/Gateway for logical-operation idempotency.
2. Do not promote any end-to-end retry-safety claim beyond local evidence until that experiment succeeds.

## P1 — implementation-gate deficiencies

1. Freeze a fresh current baseline.
2. Complete retrospective discovery/problem-buyer gate.
3. Add kill/pivot/narrow conditions.
4. Complete product-level alternatives/value hypothesis.
5. Implement the minimum structured handoff contract.
6. Extend the existing release gate with deterministic evals and required security checks.
7. Reconcile current branch/source fragmentation.
8. Promote AWS evidence when a target environment is available.

## P2 — evidence / reliability / operability gaps

1. Wire minimal failure telemetry.
2. Prove one end-to-end request/failure reconstruction.
3. Reconcile privacy/data-lifecycle policy.
4. Add recovery/rollback runbook and later exercise.
5. Add appropriate security assurance automation.
6. Establish deployed provenance.

## P3 — documentation / maturity improvements

1. Refresh dated status snapshots without rewriting history.
2. Restore/canonicalize North Star access in the repo.
3. Complete operational ownership/handoff docs before pilot.
4. Synchronize Learning Ledger with latest reconciliation/telemetry lessons.

## DEFERRED — not justified yet

- real pilot/adoption evidence;
- SLO/error-budget numbers until target-environment baseline;
- enterprise multi-tenancy;
- multi-region;
- advanced DR beyond current risk envelope;
- broader vendor adapters.

## NO CHANGE

- no RAG without need;
- no multi-agent;
- no Kubernetes/Kafka/Redis;
- no new persistence technology merely for checklist completion;
- no rewrite of Stage-1 history;
- no replacement of current deterministic control semantics.

---

# 19. Items Explicitly Requiring No Change

The following should be preserved.

1. **Frozen P1-S1 provenance**
2. **Reliora's product identity as a reliability/control platform**
3. **Product-first technology selection**
4. **LLM proposes; deterministic software validates/authorizes**
5. **request_id / session_id / operation_id distinction**
6. **Authorization before idempotency/execution**
7. **Matching replay vs conflict semantics**
8. **Authoritative backend truth**
9. **Explicit `UNCONFIRMED` state**
10. **Conditional transactional DynamoDB design**
11. **Strongly consistent reconciliation at the correctness boundary**
12. **Small approved/versioned knowledge source for current scope**
13. **No mandatory RAG**
14. **Provider boundary around replaceable ticket backends**
15. **AWS-first but not AWS-defined positioning**
16. **Evidence classes + E0-E9 maturity**
17. **Metric measurement-boundary discipline**
18. **Deterministic vs generative evaluation separation**
19. **Held-out test discipline**
20. **Learning Ledger kept separate from product implementation**
21. **No enterprise multi-tenancy for current bounded product**
22. **No arbitrary SLOs before target-environment measurement**
23. **No multi-agent/Kubernetes/Kafka/Browser/Code Interpreter for résumé breadth**
24. **Best-effort telemetry must not mask the primary business/backend failure**

---

# 20. Architecture Decisions Requiring Experiments

## EXP-001 — Trusted execution identity

**Decision:** ADR-017
**Question:** Can the real AgentCore/Gateway/Lambda path carry trusted logical-operation identity without allowing model control?
**Why experiment:** This determines whether the current idempotency architecture survives the real transport boundary.
**Minimum evidence:** operation/request/session ID traces across a first call, matching retry, and new logical action.

## EXP-002 — Live DynamoDB idempotency and reconciliation

**Question:** Do real DynamoDB transactions and reads exhibit the same replay/conflict/unconfirmed semantics proven locally?
**Minimum evidence:** one create, one matching retry, one conflict, one controlled ambiguous outcome.

## EXP-003 — End-to-end request reconstruction

**Question:** Can an engineer reconstruct a request without hidden chain-of-thought?
**Minimum evidence:** request ID -> authorization -> operation -> backend -> failure/result -> version context.

## EXP-004 — Cloud release provenance

**Question:** Can a deployed behaviour be attributed to code/infrastructure/model/prompt/router/knowledge versions?
**Minimum evidence:** one deployment manifest tied to observed request evidence.

## EXP-005 — Cloud cost/latency baseline

**Question:** What does the real AWS path cost and how long does it take within a bounded workload?
**Minimum evidence:** controlled E5 experiment; no extrapolation beyond envelope.

## EXP-006 — Structured handoff workflow

**Question:** Does the minimum handoff package reduce repeated context without leaking unnecessary information?
**Minimum evidence:** one supported handoff scenario and one failure-induced handoff scenario.

## EXP-007 — Rollback/redeploy

**Question:** Can Reliora return to a known validated version without reconstructing configuration manually?
**Minimum evidence:** controlled rollback/redeploy evidence.

---

# 21. Proposed Mitigation Sequence

The smallest sensible sequence is:

```text
0. Freeze audit snapshot
   ↓
1. Retrospective discovery + problem/buyer gate
   ↓
2. Product-level alternatives + value hypothesis
   ↓
3. Confirm governing artifacts / kill conditions
   ↓
4. Resolve ADR-017 trusted identity experiment
   ↓
5. Freeze current implementation/evidence baseline
   ↓
6. Complete minimum structured handoff
   ↓
7. Complete release gate
   ↓
8. Wire minimal telemetry + reconstructability
   ↓
9. Reconcile privacy/security branch
   ↓
10. Target-environment Lambda/DynamoDB verification
   ↓
11. AgentCore/Gateway end-to-end verification
   ↓
12. Controlled failure/idempotency experiments
   ↓
13. Deployment provenance + rollback/recovery
   ↓
14. Cost/latency measurement
   ↓
15. Product UX/operator evidence
   ↓
16. Operational handoff and portfolio release
   ↓
17. Extract latest reusable lessons into Learning Ledger
```

## Why this order

The order intentionally prevents three mistakes:

1. **Building more before validating the product reasoning**
2. **Building broad cloud integration before resolving trusted logical-operation identity**
3. **Polishing documentation/UX before the difficult cloud evidence is captured**

---

# Final Audit Decision

Reliora should **continue**.

The audit does not identify a reason to abandon the current product direction or rearchitect it wholesale.

It does identify a need to **narrow the next work to evidence-critical closure**.

The correct posture is:

> Preserve the current deterministic control architecture.
> Repair the missing discovery/product gates retrospectively and honestly.
> Resolve trusted execution identity experimentally.
> Promote local evidence into real AWS evidence without overclaiming.
> Complete handoff, observability, release, recovery, and operational closure only where Reliora independently requires them.
> Add no technology that cannot trace back to a Reliora requirement or risk.

**Audit outcome:** `CONTINUE WITH TARGETED MITIGATION — NO BROAD REARCHITECTURE`
