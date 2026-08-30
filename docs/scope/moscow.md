# Reliora MoSCoW Scope

## Purpose

This document defines the implementation boundaries for the initial Reliora production-hardening project.

MoSCoW prioritisation separates capabilities into:

- **Must Have** — required for the project to fulfil its central engineering purpose;
- **Should Have** — high-value capabilities that should be implemented when practical but are not required for minimum project success;
- **Could Have** — useful enhancements that require evidence, time, or a stronger business justification;
- **Won't Have This Time** — deliberately excluded from the current project scope.

The purpose is to prevent feature accumulation from obscuring Reliora's primary engineering question:

> How can an AI-assisted customer-support system preserve the flexibility of generative models while ensuring that critical operational behaviours are enforced, measured, and auditable?

---

# Must Have

The following capabilities define the minimum commercially meaningful version of Reliora.

## M-001 — Preserved Stage-1 Baseline

The original Stage-1 implementation must remain independently preserved and attributable through verified provenance.

Reliora must document what was inherited, what failed during audit, and what changed.

## M-002 — Explicit Behavioural Contracts

Critical system boundaries must use explicit schemas or typed contracts.

This includes, where applicable:

- routing decisions;
- knowledge-coverage decisions;
- bug-report inputs;
- tool arguments;
- tool results;
- structured handoffs;
- evaluation records.

## M-003 — Intent and Knowledge-Coverage Separation

Reliora must distinguish:

1. what type of request the customer made; and
2. whether approved knowledge can answer it.

The primary intent classes are:

- BUG
- PLATFORM
- OTHER

Platform requests then undergo a separate:

- SUPPORTED
- UNSUPPORTED

knowledge decision.

## M-004 — Deterministic Behavioural Evaluation

Critical behavioural invariants must be evaluated deterministically where exact verification is possible.

Examples include:

- premature tool invocation;
- multiple missing bug fields requested when only one is permitted;
- internal route-label leakage;
- hidden reasoning leakage;
- fabricated ticket IDs;
- malformed tool arguments;
- duplicate side effects.

## M-005 — Separate Generative-Quality Evaluation

LLM-based judges may evaluate qualities that genuinely require judgement, such as response helpfulness or answer quality.

An aggregate LLM-judge score must not override a failed critical deterministic invariant.

## M-006 — Versioned Evaluation Data

Reliora must maintain clearly separated and versioned evaluation datasets for purposes such as:

- routing gold evaluation;
- adversarial/challenge evaluation;
- workflow regression;
- controlled experiments.

Evaluation ground truth must be manually reviewed before being treated as authoritative.

## M-007 — Retry-Safe Bug Ticket Creation

Bug-report creation must be idempotent.

Retrying the same logical operation must not create duplicate tickets.

## M-008 — Deterministic Tool Validation

An LLM may propose a side-effecting tool call, but deterministic software must validate and authorize the operation before execution.

## M-009 — Structured Human Handoff

Unsupported, ambiguous, unsafe, or failed automation must support a structured human handoff containing useful context without exposing unnecessary sensitive or internal information.

## M-010 — End-to-End Traceability

Requests must carry appropriate identifiers through major system boundaries.

The design must distinguish:

- request identity;
- session identity;
- logical operation identity.

## M-011 — Decision Provenance

Operational evidence must make it possible to determine relevant serving context such as:

- application version;
- prompt version;
- routing configuration;
- model version or identifier;
- approved knowledge version;
- tool outcome.

Hidden chain-of-thought must not be required for auditability.

## M-012 — Security and Privacy Baseline

The project must include:

- least-privilege IAM;
- input and tool validation;
- prompt-injection testing;
- secret scanning;
- infrastructure security scanning;
- data minimisation;
- sensitive-log reduction;
- explicit retention decisions.

## M-013 — Bounded Agent Execution

Model and agent execution must have intentionally selected limits where supported, including relevant limits for:

- input size;
- generated tokens;
- iterations;
- tool calls;
- invocation duration;
- retries.

## M-014 — Failure and Fault Testing

Reliora must test failure behaviour, not only successful workflows.

Examples include:

- model failure;
- Gateway failure;
- Lambda failure;
- DynamoDB failure;
- response lost after a successful write;
- malformed model output;
- unsupported knowledge;
- duplicate operation retry.

## M-015 — Operational Observability

The system must expose sufficient telemetry to investigate behaviour across:

- service/system health;
- AI behaviour;
- business workflow outcomes.

Observability should use managed AgentCore and CloudWatch capabilities before custom infrastructure is introduced.

## M-016 — Release Regression Gate

Candidate releases must pass defined behavioural regression checks before promotion.

Critical failures must block release.

## M-017 — Rollback and Versioning

A previously validated application or Harness configuration must be recoverable without manually reconstructing its behaviour.

## M-018 — Infrastructure as Code

Persistent AWS infrastructure used by Reliora must be reproducibly described with Terraform unless a documented exception is justified.

## M-019 — Secure CI/CD Authentication

Cloud deployment automation must avoid long-lived AWS credentials stored in GitHub.

GitHub Actions should use short-lived AWS authentication through OIDC where supported.

## M-020 — Cost Governance

Reliora must include:

- AWS resource tagging;
- budget/cost monitoring;
- known teardown procedures;
- model/tool usage metrics;
- workload-level cost evidence where practical.

## M-021 — Quality-Adjusted Routing Experiment

Reliora must compare plausible routing strategies using the same controlled evaluation methodology.

Initial candidates are:

- deterministic rules;
- TF-IDF + Logistic Regression;
- TF-IDF + Linear SVM;
- LLM routing.

A hybrid router must only be adopted if experimental results justify it.

Comparison must consider more than aggregate accuracy, including:

- macro and per-class performance;
- dangerous error types;
- latency;
- operational cost.

---

# Should Have

These capabilities provide substantial portfolio and engineering value but do not define minimum Reliora success.

## S-001 — Native Bedrock Structured Outputs Evaluation

Evaluate Amazon Bedrock Structured Outputs where it can strengthen model-to-software contracts.

Application-side validation must remain in place even when provider-native schema enforcement is used.

## S-002 — AgentCore Evaluation Integration

Use current AgentCore/Bedrock evaluation capabilities where they strengthen:

- expected response evaluation;
- assertions;
- tool trajectory evaluation;
- custom evaluator integration.

## S-003 — SLI and SLO Definition

After baseline measurements exist, define defensible service-level indicators and objectives for selected workflows.

Numerical SLOs must not be invented before measurement.

## S-004 — Error-Budget Model

Where meaningful SLOs exist, demonstrate how an error budget could influence release or operational decisions.

## S-005 — Controlled Replay or Shadow Routing

Evaluate candidate routing logic against the same requests without allowing the candidate to alter the real approved workflow.

This is preferred over fabricating live production traffic.

## S-006 — Knowledge Lifecycle

The embedded FAQ or equivalent approved knowledge source should have:

- explicit version;
- ownership;
- update procedure;
- regression tests for policy changes.

## S-007 — Feedback Review Loop

Human corrections should be capturable and reviewable for possible promotion into future evaluation datasets.

## S-008 — Lightweight Concurrency and Load Testing

Run controlled workload experiments sufficient to understand:

- latency behaviour;
- throttling;
- concurrency limits;
- failure behaviour;
- cost effects.

Testing must not be presented as real production traffic.

## S-009 — Production-Readiness Scorecard

Maintain an evidence-backed readiness assessment covering areas such as:

- reliability;
- security;
- observability;
- evaluation;
- deployment;
- cost;
- operations.

---

# Could Have

These capabilities may be explored only when the Must and relevant Should requirements are satisfied and a clear engineering reason exists.

## C-001 — AgentCore Optimization

Experiment with AgentCore optimisation capabilities if the available evaluation evidence and workload are sufficient to make the experiment meaningful.

## C-002 — A/B Testing

Use managed A/B capabilities only if a legitimate controlled traffic model exists.

Synthetic traffic must never be presented as real customer traffic.

## C-003 — AgentCore Policy

Evaluate AgentCore Policy if the tool surface becomes sufficiently sensitive to justify an external deterministic policy layer.

The initial low-risk bug-ticket tool alone does not automatically require it.

## C-004 — Bedrock Guardrails

Add Bedrock Guardrails as defence-in-depth if testing demonstrates useful coverage.

Guardrails must not replace application-side validation, authorization, or PII controls.

## C-005 — Custom OpenTelemetry Instrumentation

Add custom spans only if managed AgentCore/CloudWatch telemetry leaves a demonstrated observability gap.

## C-006 — Queue-Based Backpressure

Introduce a queue such as Amazon SQS only if measured workload or failure testing demonstrates a need for asynchronous buffering or backpressure.

## C-007 — Custom AgentCore Runtime / Strands Export

Export the managed Harness or migrate to a custom Strands/Runtime implementation only if a required capability cannot be implemented cleanly with the managed Harness.

## C-008 — Public API Boundary

Expose Reliora through a dedicated API layer only if a real integration or demonstration requirement justifies it.

If exposed publicly, authentication, throttling, abuse protection, and potentially AWS WAF must be reconsidered.

## C-009 — Advanced AWS FinOps Capabilities

FinOps Agent or similar advanced operations tooling may be explored for account-level cost analysis, but it is not central to Reliora's runtime architecture.

Application-level unit economics remain the primary P1-S2 FinOps requirement.

---

# Won't Have This Time

The following are intentionally excluded from the initial Reliora project.

## W-001 — Multi-Agent Architecture

Reliora will not become a multi-agent system.

Multi-agent orchestration belongs to the later portfolio project focused specifically on enterprise multi-agent architecture.

## W-002 — Persistent Personal Memory

Long-term customer-profile memory is outside Reliora's initial scope.

Session continuity and persistent personal memory are treated as separate architectural concerns.

## W-003 — Mandatory RAG Platform

Reliora will not introduce a vector database or managed RAG architecture merely to answer the small, stable Stage-1 FAQ.

Knowledge architecture may evolve only if document scale or freshness requirements justify it.

## W-004 — Browser Automation

AgentCore Browser is outside the P1-S2 problem definition.

## W-005 — Code Interpreter

AgentCore Code Interpreter is outside the P1-S2 problem definition.

## W-006 — Multi-Region Architecture

Reliora will not claim or implement multi-region resilience in the initial project.

## W-007 — Kubernetes / Amazon EKS

Container orchestration is not justified by the current workload or architecture.

## W-008 — Kafka or Managed Streaming Platform

No streaming requirement currently justifies Kafka, MSK, or an equivalent event-streaming architecture.

## W-009 — Redis / Dedicated Distributed Cache

No demonstrated caching or distributed-lock requirement currently justifies Redis.

## W-010 — MLflow

The classical routing experiment does not currently require a dedicated ML experiment-tracking platform.

Experiment results can remain versioned in the repository until scale justifies additional tooling.

## W-011 — LangGraph Reimplementation

Reliora will not rebuild working AgentCore orchestration in another agent framework solely for technology breadth.

## W-012 — Elaborate Customer Frontend

A polished production frontend is outside the initial engineering question.

The project prioritises backend reliability, evaluation, operations, and architecture evidence.

## W-013 — Fabricated Production Scale

The project will not fabricate:

- customer traffic;
- company revenue;
- incidents;
- availability;
- latency achievements;
- ROI;
- cost savings;
- enterprise adoption.

Synthetic scenarios must remain clearly identified as synthetic.

---

# Scope Change Rule

A capability may move between Must, Should, Could, and Won't only when one of the following provides a defensible reason:

1. a documented functional or non-functional requirement;
2. measured experimental evidence;
3. a newly discovered security or reliability risk;
4. a genuine platform constraint;
5. a material change in the project objective.

A technology announcement alone is not sufficient justification for a scope change.

Any material scope change should be reflected in the relevant ADR or project documentation.

---

# Current Status

This MoSCoW scope is the initial **TARGET scope baseline** for Reliora P1-S2.

It should be reviewed at major architecture milestones rather than expanded opportunistically during implementation.
