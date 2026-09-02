# Reliora Identifier Reference and Traceability Key

## Purpose

Reliora uses stable identifiers to connect requirements, governance policy, architecture, implementation, tests, evaluation evidence, and engineering decisions.

This document is the repository-level decoding key for those identifiers. It is an index and traceability aid; it does not replace the authoritative requirement, policy, architecture, ADR, or evaluation documents.

## 1. Identifier Taxonomy

| Prefix | Meaning | What it describes | Primary authoritative source |
|---|---|---|---|
| `FR` | Functional Requirement | What Reliora must do | `docs/requirements/functional-requirements.md` |
| `NFR` | Non-Functional Requirement | Reliability, security, privacy, performance, observability, maintainability, cost, and governance qualities | `docs/requirements/non-functional-requirements.md` |
| `AP` | Autonomy Principle | Rules governing AI autonomy | `docs/governance/autonomy-policy.md` |
| `H` | Handoff Condition | Conditions requiring human escalation | `docs/governance/autonomy-policy.md` |
| `CB` | Control Boundary | Critical validation, trust, authorization, execution, and handoff boundaries | `docs/architecture/logical-architecture.md` |
| `ADR` | Architecture Decision Record | Significant architecture decisions and rationale | `docs/architecture/adr/README.md` |
| `INV` | Behavioural Invariant | Deterministic behaviour that must remain true | `evals/behavioural-evaluation-contract.md` |
| `FACT` | Factual Evaluation Contract | Deterministic factual-completeness verification | evaluation contracts and evaluator implementation |
| `REPRO` | Reproduction Case | Frozen historical Stage-1 behaviour | Stage-1 reproduction dataset and evidence |

Conceptually:

```text
FR / NFR
   ↓
AP / H
   ↓
CB / ADR
   ↓
Implementation
   ↓
INV / FACT / REPRO
   ↓
Evidence
```

Identifiers describe different layers of the same system; they are complementary rather than interchangeable.

## 2. Functional Requirements — FR

`FR` means Functional Requirement.

| ID | Formal name | Plain-English meaning |
|---|---|---|
| `FR-001` | Request Identification | Every accepted customer request has a unique `request_id`. |
| `FR-002` | Session Identification | Related conversation turns share a `session_id`, distinct from individual requests. |
| `FR-003` | Operation Identification | One logical side effect uses a stable `operation_id` across retries. |
| `FR-004` | Intent Classification | Every accepted customer message resolves to exactly one of `BUG`, `PLATFORM`, or `OTHER`. |
| `FR-005` | Knowledge Coverage Classification | PLATFORM intent and knowledge coverage are separate decisions; coverage is `SUPPORTED` or `UNSUPPORTED`. |
| `FR-006` | Unsupported Request Handling | Unsupported, OTHER, or unsafe requests transition to human support. |
| `FR-007` | Required Bug Information | Bug creation requires description, reproduction steps, and environment. |
| `FR-008` | Incremental Collection | Missing bug information is collected conversationally before ticket creation. |
| `FR-009` | Tool Authorization Gate | A proposed side effect must pass deterministic validation before execution. |
| `FR-010` | Exactly-One Logical Ticket | One logical bug-report operation must create no more than one ticket. |
| `FR-011` | Idempotent Retry Result | Retrying the same logical operation returns the existing result rather than creating another ticket. |
| `FR-012` | Idempotency Conflict Detection | Reusing an `operation_id` with materially different data produces a conflict. |
| `FR-013` | Ticket Confirmation | Customer-visible success is allowed only after authoritative backend confirmation. |
| `FR-014` | Grounded Platform Answers | Supported platform questions use only approved knowledge. |
| `FR-015` | Unsupported Knowledge Handoff | Unsupported knowledge requests hand off rather than fabricate answers. |
| `FR-016` | Knowledge Version Provenance | Knowledge-dependent responses identify the relevant knowledge version. |
| `FR-017` | Structured Handoff | Human escalation produces a structured operational handoff. |
| `FR-018` | Handoff Data Minimisation | Handoff data excludes unnecessary sensitive or internal information. |
| `FR-019` | Typed Boundary Contracts | Machine-to-machine boundaries use explicit typed or schema-based contracts. |
| `FR-020` | Invalid Input Handling | Invalid, malformed, oversized, or unsupported input is safely handled before side effects. |
| `FR-021` | Structured Model Output | Model-generated data consumed by software must satisfy a defined schema. |
| `FR-022` | Internal Information Protection | Customer-visible output must not expose hidden instructions, reasoning, secrets, or protected internal information. |
| `FR-023` | Untrusted Text Boundary | Customer, retrieved, and tool-returned text is treated as untrusted input. |
| `FR-024` | Deterministic Behavioural Evaluation | Exact software requirements use deterministic evaluators where possible. |
| `FR-025` | Generative Quality Evaluation | Subjective qualities may use LLM-based evaluation separately from deterministic verification. |
| `FR-026` | Versioned Evaluation Data | Evaluation datasets have explicit versions and purposes. |
| `FR-027` | Regression Gate | A critical deterministic invariant failure blocks release regardless of aggregate LLM-judge scores. |
| `FR-028` | Deployment Provenance | Operational records identify relevant application, model, prompt, routing, knowledge, and infrastructure versions. |
| `FR-029` | Rollback | A previously validated deployment can be restored without reconstructing its behaviour manually. |
| `FR-030` | Human Correction Capture | Reviewed human corrections can be represented as feedback events. |
| `FR-031` | Reviewed Dataset Promotion | Human feedback is reviewed before becoming versioned evaluation ground truth. |

## 3. Non-Functional Requirements — NFR

`NFR` means Non-Functional Requirement. The middle code identifies the category.

| Category | Meaning |
|---|---|
| `REL` | Reliability |
| `SEC` | Security |
| `PRIV` | Privacy and Data Governance |
| `PERF` | Performance and Scalability |
| `OBS` | Observability |
| `MAINT` | Maintainability and Reproducibility |
| `COST` | Cost and FinOps |
| `GOV` | Governance and Release Safety |

### Reliability

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-REL-001` | Safe Retry Behaviour | Retries must not accidentally duplicate or corrupt side effects. |
| `NFR-REL-002` | Bounded Retry Behaviour | Retry loops have explicit limits. |
| `NFR-REL-003` | Graceful Degradation | Dependency failure produces safe degradation rather than invented success. |
| `NFR-REL-004` | Failure Classification | Important failure types are distinguishable for diagnosis. |
| `NFR-REL-005` | Fault Testing | Critical workflows are tested under failure as well as success. |

### Security

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-SEC-001` | Least Privilege | AWS identities receive only required permissions. |
| `NFR-SEC-002` | No Long-Lived Repository Credentials | Credentials and secrets are not stored in Git. |
| `NFR-SEC-003` | Deterministic Authorization | LLM output alone cannot authorize a side effect. |
| `NFR-SEC-004` | Prompt Injection Resistance | Protected behaviour is tested against manipulation attempts. |
| `NFR-SEC-005` | Dependency and Infrastructure Scanning | CI/source control supports automated security checks. |

### Privacy and Data Governance

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-PRIV-001` | Data Minimisation | Collect and retain only information required for supported workflows. |
| `NFR-PRIV-002` | Sensitive Log Reduction | Avoid unnecessary customer-sensitive information in telemetry. |
| `NFR-PRIV-003` | Defined Retention | Persistent support, evaluation, and telemetry data require explicit retention decisions. |
| `NFR-PRIV-004` | Synthetic Data Identification | Synthetic data is clearly labelled as synthetic. |

### Performance and Scalability

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-PERF-001` | Baseline Before Target | Measure a repeatable baseline before declaring latency, throughput, or concurrency targets. |
| `NFR-PERF-002` | Bounded Agent Execution | Agent iterations, tokens, tools, duration, and other resource use have deliberate limits. |
| `NFR-PERF-003` | Controlled Concurrency | Concurrency is bounded to avoid uncontrolled load and cost. |
| `NFR-PERF-004` | Measured Scaling Claims | Managed/serverless infrastructure alone does not prove application scalability. |

### Observability

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-OBS-001` | End-to-End Correlation | Significant actions are traceable across the request path. |
| `NFR-OBS-002` | Structured Telemetry | Logs and metrics support filtering, aggregation, and investigation. |
| `NFR-OBS-003` | Decision Provenance | Record useful route/version/tool/timing evidence without hidden chain-of-thought. |
| `NFR-OBS-004` | Multi-Layer Metrics | Distinguish system, AI-behaviour, and business/workflow metrics. |
| `NFR-OBS-005` | Actionable Monitoring | Monitoring is tied to conditions requiring investigation or action. |

### Maintainability and Reproducibility

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-MAINT-001` | Infrastructure as Code | Persistent AWS infrastructure is reproducibly defined with Terraform unless justified otherwise. |
| `NFR-MAINT-002` | Version-Controlled Configuration | Prompts, schemas, application config, evaluations, and infrastructure configuration are version controlled. |
| `NFR-MAINT-003` | Automated Quality Checks | Formatting, linting, typing, and tests are automated. |
| `NFR-MAINT-004` | Architecture Decision Records | Significant architecture choices have documented rationale and trade-offs. |
| `NFR-MAINT-005` | Simple Technology Preference | New technology is introduced only to solve a documented requirement or demonstrated limitation. |

### Cost and FinOps

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-COST-001` | Resource Cost Awareness | Every AWS resource has a documented purpose and teardown path. |
| `NFR-COST-002` | Budget Protection | Cloud experimentation has budget monitoring and cost alerts. |
| `NFR-COST-003` | Unit Economics | Where practical, workload-level cost is measured. |
| `NFR-COST-004` | Cost-Aware Architecture Decisions | Cost is evaluated alongside reliability, security, latency, and quality. |
| `NFR-COST-005` | No Fabricated Savings | Financial savings remain synthetic assumptions unless supported by real evidence. |

### Governance and Release Safety

| ID | Name | Plain-English meaning |
|---|---|---|
| `NFR-GOV-001` | Evidence Classification | Claims use the Reliora evidence taxonomy. |
| `NFR-GOV-002` | Critical Invariant Protection | Critical deterministic failures block promotion. |
| `NFR-GOV-003` | Versioned Release Evidence | Release evidence identifies relevant application/model/prompt/data/infrastructure versions. |
| `NFR-GOV-004` | Preview Service Boundary | Preview AWS services do not become critical dependencies without explicit risk assessment and an architecture decision. |

## 4. Autonomy Principles — AP

| ID | Formal name | Plain-English meaning |
|---|---|---|
| `AP-001` | Risk Determines Autonomy | Higher-risk actions receive less autonomous authority. |
| `AP-002` | Uncertainty Reduces Autonomy | Increasing uncertainty reduces autonomous execution and increases escalation. |
| `AP-003` | LLM Output Is Not Authorization | The model may propose an action, but deterministic software or policy authorizes it. |
| `AP-004` | Backend Truth Overrides Model Claims | The model cannot claim success unless the authoritative backend confirms it. |
| `AP-005` | Human Access Must Remain Available | Customers retain a defined path to human support. |

## 5. Human-Handoff Conditions — H

| ID | Formal name | Plain-English meaning |
|---|---|---|
| `H-001` | Unsupported Knowledge | Approved knowledge cannot support the requested answer. |
| `H-002` | Unsupported Intent | The request is outside supported automated workflows. |
| `H-003` | Routing Ambiguity | Routing cannot be made safely enough for automation. |
| `H-004` | Repeated Information Failure | Required information cannot be collected successfully after permitted attempts. |
| `H-005` | Tool Validation Failure | Proposed tool input fails deterministic schema, policy, or business-rule validation. |
| `H-006` | Backend Failure | A required dependency cannot complete the operation after permitted retries. |
| `H-007` | Ambiguous Side-Effect Outcome | Reliora cannot establish whether the side effect succeeded and must not guess. |
| `H-008` | Idempotency Conflict | The same `operation_id` is associated with materially different operation data. |
| `H-009` | Security or Prompt-Injection Trigger | Input attempts to bypass policy, expose protected information, or trigger unauthorized behaviour. |
| `H-010` | Higher-Risk Requested Action | The requested action exceeds the autonomy level supported by the current scope. |

## 6. Control Boundaries — CB

| ID | Formal name | Plain-English meaning |
|---|---|---|
| `CB-001` | Input Boundary | External input is validated before entering trusted application state. |
| `CB-002` | Model Output Boundary | Probabilistic model output crosses typed/schema validation before software consumes it. |
| `CB-003` | Tool Authorization Boundary | A model proposal does not authorize execution; deterministic policy decides. |
| `CB-004` | Side-Effect Boundary | Persistent state changes require validated arguments, stable operation identity, idempotency, backend confirmation, and traceability. |
| `CB-005` | Human Handoff Boundary | Unsupported, failed, unsafe, or higher-risk workflows transition through structured human support. |

## 7. Architecture Decision Records — ADR

`ADR` means Architecture Decision Record.

| ID | Decision | Current index status |
|---|---|---|
| `ADR-001` | Retain AgentCore Harness as the primary managed agent execution layer | `PROPOSED` |
| `ADR-002` | Separate intent classification from knowledge-coverage classification | `PROPOSED` |
| `ADR-003` | Require deterministic validation before side-effecting tool execution | `PROPOSED` |
| `ADR-004` | Use operation-level idempotency for bug-ticket creation | `PROPOSED` |
| `ADR-005` | Keep persistent customer memory disabled in P1-S2 | `PROPOSED` |
| `ADR-006` | Retain a small versioned approved knowledge source instead of introducing mandatory RAG | `PROPOSED` |
| `ADR-007` | Separate deterministic behavioural evaluation from LLM-based quality evaluation | `PROPOSED` |
| `ADR-008` | Use structured human handoff rather than generic fallback messaging | `PROPOSED` |
| `ADR-009` | Use managed AgentCore and CloudWatch observability before adding custom telemetry infrastructure | `PROPOSED` |
| `ADR-010` | Manage persistent AWS infrastructure with Terraform | `PROPOSED` |
| `ADR-011` | Use GitHub Actions with AWS OIDC for cloud deployment authentication | `PROPOSED` |
| `ADR-012` | Benchmark routing alternatives before selecting the production routing strategy | `PROPOSED` |
| `ADR-013` | Use versioned deployment provenance and rollback capability | `PROPOSED` |
| `ADR-014` | Measure application-level unit economics before making cost-efficiency claims | `PROPOSED` |
| `ADR-015` | Prevent preview AWS services from becoming critical runtime dependencies by default | `PROPOSED` |

The ADR index currently marks all fifteen entries `PROPOSED`. Some engineering work has progressed beyond that state, especially `ADR-012`; ADR lifecycle reconciliation should be handled explicitly in a separate change.

## 8. Behavioural Invariants — INV

`INV` means Behavioural Invariant.

| ID | Formal name | Plain-English meaning |
|---|---|---|
| `INV-001` | Exactly One Top-Level Intent | A request must not resolve to multiple top-level routes simultaneously. |
| `INV-002` | Intent and Knowledge Coverage Remain Separate | PLATFORM classification and knowledge coverage remain independent decisions. |
| `INV-003` | Required Bug Fields Before Tool Execution | A ticket tool must not execute before all required bug fields exist. |
| `INV-004` | Missing Information Collected Incrementally | Missing bug information is requested incrementally rather than all at once. |
| `INV-005` | Tool Arguments Match Contract | Tool input satisfies the documented machine contract. |
| `INV-006` | Unauthorized Tool Proposals Do Not Execute | Proposed but unauthorized operations never cross into side-effect execution. |
| `INV-007` | One Logical Operation Produces No Duplicate Ticket | Retrying one logical operation must not create multiple tickets. |
| `INV-008` | Operation-ID Payload Conflicts Are Detected | Reusing an operation ID with materially different data produces a conflict. |
| `INV-009` | Ticket Success Requires Backend Confirmation | Customer-facing success requires authoritative backend confirmation. |
| `INV-010` | Ticket IDs Are Never Fabricated | Ticket identifiers originate from authoritative backend state, not model generation. |
| `INV-011` | Unsupported Knowledge Does Not Become Fabricated Policy | Unsupported platform questions do not cause invented policy answers. |
| `INV-012` | Internal Information Does Not Leak | Customer-visible output does not reveal protected internal information. |
| `INV-013` | Handoff Is Structured | Human escalation satisfies the structured handoff contract. |
| `INV-014` | Handoff Respects Data Minimisation | Handoff data excludes unnecessary or protected information. |

### Current executable evaluator coverage

| ID | Current implementation | Scope |
|---|---|---|
| `INV-004` | `src/reliora/evaluation/bug_workflow.py` | Incremental bug-field collection |
| `INV-012` | `src/reliora/evaluation/leakage.py` | Current deterministic leakage-marker families |
| `FACT-001` | `src/reliora/evaluation/factual.py` | Required-fact lexical completeness |

A documented invariant is not automatically verified merely because the identifier exists.

### INV-999

`INV-999` is not a defined Reliora invariant. It is intentionally used in evaluator unit testing as an unsupported identifier to verify that unknown evaluation IDs are rejected.

## 9. Factual Evaluation — FACT

### FACT-001 — Required Fact Completeness

`FACT-001` verifies whether every reviewed required fact has at least one accepted textual representation in a response.

The current evaluator is lexical. Passing it must not be described as proof of complete semantic truth.

Current implementation: `src/reliora/evaluation/factual.py`.

## 10. Reproduction Cases — REPRO

| ID | Historical case | Primary evaluation relationship |
|---|---|---|
| `REPRO-001` | Bug workflow requested multiple missing required fields instead of collecting them incrementally | `INV-004` |
| `REPRO-002` | Customer-visible behaviour exposed an internal-style routing/handoff marker | `INV-012` |
| `REPRO-003` | Streamed model output exposed hidden/internal reasoning markers | `INV-012` |
| `REPRO-004` | Platform-policy answer omitted a required defective-item return exception | `FACT-001` |

A `REPRO-*` ID represents one historical case; an `INV-*` or `FACT-*` ID represents a reusable evaluation rule or contract.

## 11. Evidence Classification

| Evidence label | Meaning |
|---|---|
| `TARGET` | Intended requirement or desired state not yet demonstrated |
| `OBSERVED` | Directly observed behaviour or system state |
| `MEASURED` | Quantitatively measured evidence |
| `EXPERIMENTAL` | Result produced under a documented experimental protocol |
| `SYNTHETIC ASSUMPTION` | Fabricated scenario/data deliberately used for modelling or demonstration |

Identifier type and evidence strength are separate concepts.

## 12. Implementation-State Vocabulary

| State | Meaning |
|---|---|
| `NOT STARTED` | No implementation yet |
| `PARTIAL` | Some required behaviour exists, but the complete contract is not satisfied |
| `IMPLEMENTED` | Required implementation exists |
| `VERIFIED` | Implementation has appropriate deterministic or evidence-backed verification |

These are implementation-management terms, separate from the formal evidence taxonomy.

## 13. Current Runtime Traceability Snapshot

| Requirement | Short name | Current state | Current implementation/evidence |
|---|---|---|---|
| `FR-001` | Request Identification | `IMPLEMENTED` | `SupportRequest.request_id` |
| `FR-002` | Session Identification | `IMPLEMENTED` | `SupportRequest.session_id` |
| `FR-003` | Operation Identification | `IMPLEMENTED` | `BugReportOperation.operation_id` |
| `FR-004` | Intent Classification | `PARTIAL` | Typed `RoutingDecision` exists; runtime router integration remains |
| `FR-007` | Required Bug Information | `VERIFIED` | `BugReportDraft` plus unit tests |
| `FR-008` | Incremental Collection | `PARTIAL / VERIFIED CORE` | Missing-field ordering and one-next-field state implemented; full conversation orchestration remains |
| `FR-009` | Tool Authorization Gate | `PARTIAL` | Deterministic preconditions implemented; complete authorization chain still requires remaining controls |
| `FR-010` | Exactly-One Logical Ticket | `PARTIAL` | Idempotency admission exists; ticket provider/result persistence remains |
| `FR-011` | Idempotent Retry Result | `PARTIAL` | Matching retry recognition exists; authoritative previous-result replay remains |
| `FR-012` | Idempotency Conflict Detection | `PARTIAL / LOCAL REFERENCE` | In-memory operation-payload conflict detection implemented and tested |
| `FR-013` | Ticket Confirmation | `NOT STARTED` | Authoritative ticket-result/provider boundary still required |

## 14. Current Runtime Control Chain

```text
SupportRequest
    ↓
RoutingDecision
    ↓
BugReportDraft
    ↓
BugReportOperation
    ↓
Authorization Preconditions
    ├── DENIED
    └── READY_FOR_IDEMPOTENCY_CHECK
            ↓
      Idempotency Admission
        ├── NEW_OPERATION
        ├── MATCHING_OPERATION
        └── CONFLICT
```

Important distinctions:

```text
READY_FOR_IDEMPOTENCY_CHECK ≠ AUTHORIZED
AUTHORIZED ≠ EXECUTED
EXECUTED ≠ SUCCEEDED
```

Customer-visible success must ultimately depend on authoritative backend confirmation.

## 15. Key Traceability Examples

### Tool authorization

```text
FR-009 — Tool Authorization Gate
    ↓
AP-003 — LLM Output Is Not Authorization
    ↓
NFR-SEC-003 — Deterministic Authorization
    ↓
CB-003 — Tool Authorization Boundary
```

### Idempotency

```text
FR-003 — Operation Identification
    ↓
FR-010 — Exactly-One Logical Ticket
    ├── FR-011 — Idempotent Retry Result
    └── FR-012 — Idempotency Conflict Detection
    ↓
NFR-REL-001 — Safe Retry Behaviour
    ↓
ADR-004 — Operation-Level Idempotency
    ├── INV-007 — No Duplicate Ticket
    └── INV-008 — Payload Conflict Detection
```

### Backend-confirmed success

```text
FR-013 — Ticket Confirmation
    ↓
AP-004 — Backend Truth Overrides Model Claims
    ↓
CB-004 — Side-Effect Boundary
    ├── INV-009 — Success Requires Confirmation
    └── INV-010 — Ticket IDs Are Never Fabricated
```

## 16. Rules for Using Identifiers

On first use in a document or explanation, prefer `FR-011 — Idempotent Retry Result` rather than only `FR-011`.

Tests should reference identifiers when the test specifically verifies that contract.

New identifiers require an authoritative definition in the appropriate source document.

## 17. Authoritative Source Hierarchy

| Identifier | Authority |
|---|---|
| `FR-*` | `docs/requirements/functional-requirements.md` |
| `NFR-*` | `docs/requirements/non-functional-requirements.md` |
| `AP-*`, `H-*` | `docs/governance/autonomy-policy.md` |
| `CB-*` | `docs/architecture/logical-architecture.md` |
| `ADR-*` | `docs/architecture/adr/README.md` and future individual ADRs |
| `INV-*` | `evals/behavioural-evaluation-contract.md` |
| `FACT-*` | evaluation contract/dataset/evaluator documentation |
| `REPRO-*` | Stage-1 reproduction dataset and dataset card |

## 18. Maintenance Rule

Update this document when a new identifier is introduced, an identifier is retired or superseded, an ADR changes lifecycle state, implementation status materially changes, a documented invariant gains or loses executable evaluator coverage, or a new evaluation namespace is introduced.

The objective is that a developer, reviewer, interviewer, or future maintainer should never need to guess what an identifier such as `FR-011`, `H-008`, or `INV-007` means.
