# Reliora Non-Functional Requirements

## Purpose

This document defines the quality attributes and operational constraints under which Reliora should operate.

Unlike functional requirements, which describe what the system must do, non-functional requirements describe how reliably, securely, efficiently, observably, and maintainably the system must perform those functions.

Unless supported by measured evidence, numerical performance and reliability thresholds remain TARGET or TBD rather than being presented as achieved results.

---

## Reliability

### NFR-REL-001 — Safe Retry Behaviour

Side-effecting operations must remain safe when requests are retried because of timeouts, transient failures, or ambiguous responses.

### NFR-REL-002 — Bounded Retry Behaviour

Retries must be explicitly bounded.

The system must not permit uncontrolled retry loops across application, agent, tool, and backend layers.

### NFR-REL-003 — Graceful Degradation

When a required model, tool, knowledge source, or backend dependency is unavailable, the system must fail safely.

Where appropriate, the customer should receive a structured human handoff instead of an invented successful result.

### NFR-REL-004 — Failure Classification

Operational failures should distinguish, where practical, between:

- validation failure;
- authorization failure;
- transient dependency failure;
- permanent dependency failure;
- timeout;
- idempotency conflict;
- model or schema failure.

### NFR-REL-005 — Fault Testing

Critical workflows must be tested against defined failure scenarios rather than only successful execution paths.

---

## Security

### NFR-SEC-001 — Least Privilege

AWS identities and application components must receive only the permissions required for their documented responsibilities.

### NFR-SEC-002 — No Long-Lived Repository Credentials

AWS credentials, API secrets, private keys, and similar sensitive values must not be stored in the Git repository.

CI/CD should use short-lived workload identity where supported.

### NFR-SEC-003 — Deterministic Authorization

An LLM response alone must never be treated as sufficient authorization for a privileged or side-effecting operation.

### NFR-SEC-004 — Prompt Injection Resistance

The system must be tested against attempts to override system instructions, expose internal information, manipulate routing, or trigger unauthorized tools.

### NFR-SEC-005 — Dependency and Infrastructure Scanning

Source control and CI should support automated checks for secrets and infrastructure security issues.

---

## Privacy and Data Governance

### NFR-PRIV-001 — Data Minimisation

Reliora must collect and retain only information required for the defined support workflows.

### NFR-PRIV-002 — Sensitive Log Reduction

Operational telemetry must avoid unnecessary customer-sensitive content.

Where sensitive values are not required for debugging, redacted values, identifiers, or safe summaries should be preferred.

### NFR-PRIV-003 — Defined Retention

Persistent customer-support, evaluation, and telemetry data must have an explicitly documented retention decision.

### NFR-PRIV-004 — Synthetic Data Identification

Synthetic or fabricated data used for testing, workload modelling, or business scenarios must be clearly identified as synthetic.

---

## Performance and Scalability

### NFR-PERF-001 — Baseline Before Target

Latency, throughput, and concurrency targets must be established only after a repeatable baseline measurement exists.

### NFR-PERF-002 — Bounded Agent Execution

Agent execution must use deliberately selected limits for relevant resources such as:

- maximum model iterations;
- maximum generated tokens;
- tool calls;
- invocation duration;
- input size.

### NFR-PERF-003 — Controlled Concurrency

Concurrency must be bounded so that sudden workload increases cannot create uncontrolled downstream load or cost.

### NFR-PERF-004 — Measured Scaling Claims

The project must not claim production scalability solely because underlying AWS services are managed or serverless.

Scalability claims must distinguish architectural capability from experimentally measured workload behaviour.

---

## Observability

### NFR-OBS-001 — End-to-End Correlation

Operationally significant actions must be traceable using correlation identifiers across the major request path.

### NFR-OBS-002 — Structured Telemetry

Logs and metrics should be structured sufficiently to support filtering, aggregation, and investigation.

### NFR-OBS-003 — Decision Provenance

The system must record operationally useful decision provenance such as route, relevant version identifiers, tool outcome, and timing without storing hidden chain-of-thought.

### NFR-OBS-004 — Multi-Layer Metrics

Observability should distinguish:

- service/system metrics;
- AI behaviour metrics;
- business/workflow metrics.

### NFR-OBS-005 — Actionable Monitoring

Monitoring should be designed around conditions that would require investigation or action rather than collecting telemetry without an operational purpose.

---

## Maintainability and Reproducibility

### NFR-MAINT-001 — Infrastructure as Code

AWS infrastructure used for the production-engineering implementation should be reproducibly defined through Terraform unless a documented exception is required.

### NFR-MAINT-002 — Version-Controlled Configuration

Application configuration, prompts, schemas, evaluation definitions, and infrastructure configuration must be version controlled where safe to do so.

### NFR-MAINT-003 — Automated Quality Checks

The project should support automated formatting, linting, type checking, and testing.

### NFR-MAINT-004 — Architecture Decision Records

Significant architectural choices must be recorded through ADRs when alternatives and trade-offs materially affect the system.

### NFR-MAINT-005 — Simple Technology Preference

Additional infrastructure or frameworks should not be introduced unless they solve a documented requirement or experimentally demonstrated limitation.

---

## Cost and FinOps

### NFR-COST-001 — Resource Cost Awareness

Each deployed AWS resource must have a documented purpose and a known teardown path.

### NFR-COST-002 — Budget Protection

The personal AWS development environment must use budget monitoring and appropriate cost alerts before meaningful cloud experimentation begins.

### NFR-COST-003 — Unit Economics

Where technically practical, the project should measure cost at workload-relevant levels such as:

- cost per request;
- cost per successful resolution;
- model calls per request;
- tokens per request;
- tool calls per request.

### NFR-COST-004 — Cost-Aware Architecture Decisions

Cost comparisons must be considered alongside reliability, safety, latency, and quality rather than optimized in isolation.

### NFR-COST-005 — No Fabricated Savings

Projected financial savings must be labelled as synthetic assumptions unless based on genuine measured business data.

---

## Governance and Release Safety

### NFR-GOV-001 — Evidence Classification

Claims must use the project's defined evidence taxonomy:

MEASURED, OBSERVED, EXPERIMENTAL, TARGET, or SYNTHETIC ASSUMPTION.

### NFR-GOV-002 — Critical Invariant Protection

A release must not be promoted when a critical deterministic behavioural invariant fails, even if aggregate generative-quality metrics are high.

### NFR-GOV-003 — Versioned Release Evidence

Release evidence must identify the relevant application, prompt, model, evaluation-data, and infrastructure versions where applicable.

### NFR-GOV-004 — Preview Service Boundary

Preview AWS capabilities may be evaluated when useful but must not become critical customer-request dependencies without an explicit architecture decision and risk assessment.

---

## Numerical Targets

Specific latency, availability, throughput, error-budget, and cost thresholds are currently **TBD TARGETS**.

They will be established after baseline measurement rather than selected for appearance.

## Current Status

These NFRs define the intended production-engineering quality model for Reliora.

They remain **TARGET requirements** until implementation and evidence demonstrate compliance.
