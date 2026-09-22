# Reliora Architecture Decision Record Register

## Purpose

Architecture Decision Records (ADRs) document significant technical decisions made during the development of Reliora.

An ADR captures:

- the engineering problem or decision context;
- the requirements and constraints involved;
- reasonable alternatives considered;
- the selected decision;
- the consequences and trade-offs;
- conditions that may require the decision to be revisited.

ADRs are intended to preserve architectural reasoning, not merely record which technologies were used.

---

# Status Model

Reliora ADRs use the following statuses:

- **PROPOSED** — under consideration and not yet formally adopted;
- **ACCEPTED** — selected for the current architecture;
- **SUPERSEDED** — replaced by a later ADR;
- **DEPRECATED** — no longer recommended but retained for historical context;
- **REJECTED** — considered but deliberately not selected.

A decision may be revisited when new evidence, requirements, platform constraints, security findings, or measured system behaviour justify reconsideration.

A new AWS feature alone is not sufficient reason to change an accepted decision.

---

# ADR Register

| ADR | Decision | Status | Primary Driver |
|---|---|---|---|
| ADR-001 | Retain AgentCore Harness as the primary managed agent execution layer | PROPOSED | Simplicity, managed orchestration, existing Stage-1 baseline |
| ADR-002 | Separate intent classification from knowledge-coverage classification | PROPOSED | Routing correctness and separation of concerns |
| ADR-003 | Require deterministic validation before side-effecting tool execution | PROPOSED | Safety and authorization |
| ADR-004 | Use operation-level idempotency for bug-ticket creation | PROPOSED | Retry safety and duplicate prevention |
| ADR-005 | Keep persistent customer memory disabled in P1-S2 | PROPOSED | Privacy, scope control, lack of requirement |
| ADR-006 | Retain a small versioned approved knowledge source instead of introducing mandatory RAG | PROPOSED | Proportional architecture and scope |
| ADR-007 | Separate deterministic behavioural evaluation from LLM-based quality evaluation | PROPOSED | Reliable release decisions |
| ADR-008 | Use structured human handoff rather than generic fallback messaging | PROPOSED | Operational continuity and auditability |
| ADR-009 | Use managed AgentCore and CloudWatch observability before adding custom telemetry infrastructure | PROPOSED | Simplicity and operational visibility |
| ADR-010 | Manage persistent AWS infrastructure with Terraform | PROPOSED | Reproducibility, auditability, teardown |
| ADR-011 | Use GitHub Actions with AWS OIDC for cloud deployment authentication | PROPOSED | Short-lived credentials and CI/CD security |
| ADR-012 | Benchmark routing alternatives before selecting the production routing strategy | PROPOSED | Evidence-driven model selection |
| ADR-013 | Use versioned deployment provenance and rollback capability | PROPOSED | Release safety |
| ADR-014 | Measure application-level unit economics before making cost-efficiency claims | PROPOSED | Evidence-based FinOps |
| ADR-015 | Prevent preview AWS services from becoming critical runtime dependencies by default | PROPOSED | Platform risk management |
| ADR-016 | Separate durable operation-control state from authoritative ticket state | PROPOSED | Distributed idempotency, concurrency safety, and backend truth |
| ADR-017 | Source side-effect execution identity from deterministic trusted boundaries | PROPOSED | Retry safety, trust boundaries, and identity provenance |
---

# Decision Principles

Reliora architecture decisions should follow these principles.

## Requirements Before Technology

Technology is selected to satisfy documented functional or non-functional requirements.

The existence of a service or framework is not itself an architectural requirement.

## Evidence Before Complexity

Additional infrastructure should be introduced only when:

- a requirement demands it;
- measured evidence demonstrates a limitation;
- security or reliability analysis requires it;
- an operational constraint justifies it.

## Managed Before Custom

Where a managed AWS capability satisfies the requirement adequately, it should generally be evaluated before building equivalent custom infrastructure.

This principle does not prevent custom implementation when control, portability, cost, observability, or reliability requirements justify it.

## Deterministic Controls Around Probabilistic Components

Probabilistic model behaviour should not independently control critical system invariants.

Schema validation, authorization, idempotency, release gates, and other exact requirements should be enforced deterministically where practical.

## Reversible Decisions Where Possible

Architecture should favor decisions that can be changed without unnecessary reconstruction of the system.

More difficult-to-reverse decisions require stronger justification and evidence.

---

# ADR Lifecycle

An ADR normally progresses through:

`PROPOSED`

→ alternatives investigated

→ relevant evidence collected

→ decision reviewed

→ `ACCEPTED` or `REJECTED`

If a later decision replaces it:

`ACCEPTED`

→ new ADR created

→ previous ADR becomes `SUPERSEDED`

Historical ADRs should not normally be deleted because they explain how the architecture evolved.

---

# Relationship to Evidence

An ADR may reference:

- functional requirements;
- non-functional requirements;
- threat-model entries;
- experiments;
- benchmarks;
- evaluation results;
- AWS platform constraints;
- cost measurements;
- operational observations.

Claims inside ADRs must follow Reliora's evidence taxonomy:

- MEASURED
- OBSERVED
- EXPERIMENTAL
- TARGET
- SYNTHETIC ASSUMPTION

---

# Current Status

This register defines the initial set of architectural decisions expected during Reliora P1-S2.

Individual ADRs will be written and accepted progressively as the relevant decision is reached and supported by sufficient reasoning or evidence.