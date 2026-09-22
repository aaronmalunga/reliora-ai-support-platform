# Reliora Product North Star and Delivery Guardrails

**Status:** Living source of truth  
**Project:** P1-S2 — Reliora  
**Purpose:** Keep Reliora commercially credible, technically disciplined, portfolio-ready, and protected from unnecessary scope expansion or cross-project contamination.

---

## 1. Portfolio Product Standard — Applies to All Three Projects

Every project in the portfolio should be treated as a **product reference implementation**, not merely as coursework or an AWS service demonstration.

Each project must answer four questions:

1. **What real business problem does this solve?**
2. **What does a customer or employee experience when the problem occurs?**
3. **What does the business gain from the solution?**
4. **What engineering evidence proves that the solution is safe, reliable, observable, deployable, and economically defensible?**

The goal is not to build three giant products. The goal is to build three **focused products with convincing end-to-end reference experiences**.

A project should be able to demonstrate:

- a realistic user journey;
- a realistic business/operator journey;
- measurable technical behaviour;
- controlled failure behaviour;
- a reproducible deployment path;
- clear configuration/adaptation boundaries;
- evidence that supports both business value and engineering quality.

Cloud services are implementation details. The portfolio story must begin with the pain point and outcome.

---

# 2. Reliora Product Thesis

**Reliora is a configurable AI customer-support reliability and control platform for online commerce.**

It helps retailers automate appropriate support interactions while making AI behaviour:

- measurable;
- safe;
- observable;
- recoverable;
- regression-tested;
- cost-aware;
- human-supervised where appropriate.

Reliora evolves the successful P1-S1 customer-support chatbot into a production-oriented product reference implementation.

The core engineering principle remains:

> **The LLM may propose; deterministic software validates and authorizes.**

---

# 3. Target Customer

Reliora should be designed primarily for small-to-mid-size and growing online retailers operating in markets such as:

- United States;
- United Kingdom;
- Canada;
- other comparable e-commerce markets.

Potential buyers and evaluators include:

- Head of Customer Support;
- Customer Experience leader;
- CTO / VP Engineering;
- Head of AI / Automation;
- E-commerce Operations leader;
- Solutions / Platform Engineering teams.

The reference implementation must not imply that Reliora already has real commercial customers.

All simulated organizations, customers, traffic, costs, and business assumptions must be clearly labelled as synthetic unless measured from the deployed Reliora system itself.

---

# 4. The Business Problems Reliora Must Solve

Reliora should stay focused on the problems that make AI customer support difficult to operate in a real business.

## 4.1 Unreliable AI behaviour

A generic LLM quality score can look strong while important behavioural requirements still fail.

Reliora must therefore distinguish:

- deterministic behavioural invariants;
- semantic/generative quality;
- operational reliability;
- business impact.

## 4.2 Incorrect or expensive routing

Not every message necessarily requires an expensive LLM routing decision.

Reliora should experimentally compare appropriate deterministic/classical/LLM alternatives and select the architecture from evidence.

## 4.3 Unsafe side effects

The model must not be treated as the authority that approves persistent business actions.

Tool execution should be controlled through:

- typed schemas;
- deterministic validation;
- authorization rules;
- stable operation identity;
- idempotency;
- authoritative backend confirmation.

## 4.4 Retry and duplicate-action risk

A timeout must not cause one logical customer action to create multiple business records.

Reliora should demonstrate safe replay and idempotent side-effect behaviour.

## 4.5 Poor failure diagnosis

Engineers must be able to reconstruct what happened without relying on hidden model reasoning.

Important provenance should include:

- request ID;
- session ID where applicable;
- operation ID where applicable;
- route;
- application version;
- router version;
- prompt/model configuration where applicable;
- tool proposal;
- authorization outcome;
- backend result;
- latency;
- failure category.

## 4.6 Bad human escalation

Customers should not be trapped in loops or forced to repeat the same information.

Reliora should treat handoff as a structured workflow outcome rather than merely a support-phone-number message.

## 4.7 Release regression

A prompt, model, router, workflow, or code change must not silently break known behaviour.

Reliora should ultimately support versioned evaluation and behavioural release gates.

## 4.8 AI operating cost without clear value

Reliora should measure cost and workload behaviour at useful units such as:

- model calls per request;
- tokens per request where applicable;
- tool calls per request;
- latency;
- cost per request;
- cost per successful eligible resolution.

Business ROI projections must remain synthetic unless a real organization supplies the necessary assumptions.

---

# 5. P1-S1 Functional Baseline That Reliora Preserves

Reliora inherits the functional concept of the completed P1-S1 customer-support chatbot.

## BUG

The system should:

1. identify the request as a bug report;
2. collect the bug description;
3. collect steps to reproduce;
4. collect the customer environment;
5. avoid premature tool execution;
6. create a ticket through the controlled backend path;
7. return the confirmed ticket identifier.

## PLATFORM

The system should:

1. identify the request as a platform question;
2. determine whether approved knowledge supports the answer;
3. provide a grounded answer when supported;
4. hand off when the approved knowledge does not support the answer.

## OTHER

The system should route unsupported automated workflows to human support.

Reliora may strengthen these behaviours but should not casually replace them with unrelated capabilities.

---

# 6. Product Experience Requirement

Reliora must eventually include a **product-grade reference commerce experience**.

The purpose is not to build a complete Shopify competitor.

The reference application exists so customers, recruiters, engineers, and hiring managers can experience the problems Reliora solves.

## Customer-facing reference experience

The reference storefront should eventually support enough realistic interaction to demonstrate scenarios such as:

- browsing products;
- opening product details;
- a lightweight cart/checkout simulation;
- order or support context where useful;
- embedded Reliora customer support.

Example support scenarios:

### Bug

> “Every time I press Pay, the checkout crashes.”

### Platform question

> “How long can I return this item?”

### Unsupported question

> “Do you offer a policy that is not in the approved knowledge?”

### Explicit human request

> “I want to speak to a person.”

The storefront is **not Reliora itself**. It is the reference environment through which Reliora is experienced.

---

# 7. Internal Reliora Console Requirement

Reliora should eventually expose an internal support/reliability console sufficient to demonstrate why a business would pay for the platform.

Potential product surfaces include:

## Overview

- request volume in the reference workload;
- route distribution;
- automated outcomes;
- handoffs;
- ticket operations;
- failure rate;
- latency;
- cost indicators.

## Request Explorer

- request ID;
- route;
- decision provenance;
- workflow state;
- tool proposal;
- authorization outcome;
- backend result;
- latency;
- system/configuration version.

## Evaluation

- regression status;
- benchmark comparison;
- confusion matrix;
- known failure cases;
- release-gate status.

## Operations

- recent failures;
- dependency errors;
- alerts;
- diagnostic links;
- failure categories.

Only the subset justified by the final product demonstration needs to be implemented.

---

# 8. Configurable / Off-the-Shelf Product Boundary

Reliora should be adaptable without requiring a customer to rewrite the platform.

Configuration/adaptation boundaries should eventually include appropriate subsets of:

- brand configuration;
- approved FAQ/knowledge;
- support contact or escalation destination;
- permitted workflows;
- policy configuration;
- backend/tool adapters;
- deployment configuration;
- region/environment configuration;
- retention/redaction configuration;
- UI branding.

The preferred adoption experience is conceptually:

```text
configure
    ↓
deploy
    ↓
verify
    ↓
pilot
```

rather than:

```text
fork the project
    ↓
rewrite the entire application
```

Reliora does **not** need to become a multi-tenant commercial SaaS platform during P1-S2.

---

# 9. Architecture Boundaries

Reliora should preserve clear separation between:

## Product runtime

`src/reliora/`

Selected, reusable runtime implementation.

## Durable evaluation

`evals/`

Versioned evaluation datasets, contracts, and runners used to protect selected behaviour over time.

## Experimental engineering

`experiments/`

Controlled investigations used to make architecture/model decisions.

Experimental candidates do not automatically belong in runtime code.

## Evidence

`evidence/`

Retained evidence produced by durable evaluations and other approved engineering processes.

## Infrastructure

`infra/`

Infrastructure-as-code and deployment definitions.

## Repository operations

`scripts/`

Repository-wide operational commands such as deploy, verify, export evidence, and destroy.

## CI/CD

`.github/workflows/`

Automated engineering and release controls when implemented.

---

# 10. Routing Experiment Boundary

The routing benchmark answers:

> **Does every routing decision actually require an LLM?**

The frozen v1 benchmark candidates are:

- B0 — majority-class baseline;
- B1 — deterministic rule baseline;
- C1 — TF-IDF + Logistic Regression;
- C2 — TF-IDF + Linear SVM.

The benchmark should compare candidates using evidence such as:

- macro F1;
- per-class behaviour;
- confusion patterns;
- failure severity;
- determinism;
- latency;
- dependency complexity;
- cost implications.

The selected architecture should not be chosen solely because it has the highest accuracy.

The held-out test set must remain closed to model-driven editing and should only be used after candidate/configuration selection is fixed.

Only the selected routing design should later be promoted to the production runtime package.

---

# 11. Minimum Productization Gaps to Close

These are necessary product gaps, not invitations to expand scope.

## G-001 — Product acceptance scenarios

Reliora needs a small set of canonical end-to-end demonstrations that define what a successful reference product looks like.

At minimum:

1. supported platform question;
2. unsupported platform question → structured handoff;
3. multi-turn bug collection;
4. confirmed ticket creation;
5. retry/idempotency scenario;
6. controlled backend/dependency failure;
7. trace/reconstruction of one request;
8. evaluation regression preventing an unsafe change.

## G-002 — Configuration boundary

Hard-coded sample-company values should gradually move behind clearly owned configuration where doing so directly improves adoptability.

Do not build a generalized configuration platform prematurely.

## G-003 — Adapter boundary

The sample bug-ticket backend should demonstrate how a real company could replace the reference adapter with its own ticketing or support system.

One clean adapter contract is more valuable than integrating many vendors.

## G-004 — Reproducible deployment

A technically competent evaluator should be able to understand how Reliora is deployed, verified, and destroyed without reverse engineering the repository.

Target operational lifecycle:

```text
bootstrap
deploy
verify
capture evidence
destroy
```

## G-005 — Reference data and simulation discipline

Synthetic storefront data, support cases, failures, load assumptions, and business assumptions must be versioned or documented sufficiently to distinguish simulation from measured production evidence.

## G-006 — Product/operator documentation

Before portfolio release, Reliora should contain enough documentation for:

- what the product solves;
- how the reference architecture works;
- how to deploy it;
- how to configure it;
- how to verify it;
- how to troubleshoot it;
- what is deliberately out of scope.

## G-007 — Evidence-to-claim traceability

Important portfolio claims should point to measurable evidence.

Examples:

> “Retry-safe ticket creation”

should point to an idempotency/replay test.

> “Observable request path”

should point to a trace/correlation demonstration.

> “Cheaper routing alternative selected”

should point to benchmark evidence.

---

# 12. Scope Guardrails — Explicitly Not Required for Reliora P1-S2

The following do not enter Reliora merely for technology breadth:

- multi-agent architecture;
- persistent personalized customer memory;
- AgentCore Browser;
- Code Interpreter;
- mandatory Bedrock Knowledge Base RAG;
- Kubernetes / Amazon EKS;
- Kafka / Amazon MSK;
- Redis;
- MLflow;
- LangGraph reimplementation;
- multi-region architecture;
- full e-commerce platform;
- real payment processing;
- real warehouse/inventory platform;
- full order-management system;
- enterprise multi-tenancy;
- billing/subscription system.

A capability may enter only if a documented product requirement, risk, bottleneck, experiment, or accepted architecture decision justifies it.

---

# 13. S-Tier Quality Standard

Reliora should be considered S-tier only when the strongest claims are demonstrated end to end rather than described only in documentation.

The target S-tier story is:

> A realistic customer experiences a support problem inside a reference commerce application. Reliora classifies and controls the request, safely executes or escalates the appropriate workflow, persists authoritative state, exposes reconstructable operational evidence, survives a controlled failure/retry scenario, protects behaviour through evaluation/regression controls, and can be reproducibly deployed and adapted by another engineering team.

S-tier does **not** require maximum feature count.

A narrower product with excellent evidence, UX, deployment, reliability, and technical explanation is preferred over a broad but incomplete platform.

---

# 14. Recording and Portfolio Evidence Standard

Recordings should answer business or engineering questions.

Avoid recordings whose primary message is:

> “Here is an AWS service.”

Prefer:

> “Can the customer complete this support journey safely?”

> “Can the business prove the ticket really exists?”

> “What happens when the backend times out after writing?”

> “Can an engineer reconstruct this failure from one request ID?”

> “Does this routing decision require LLM inference?”

> “Can a bad release be prevented automatically?”

Each strong recording should connect:

```text
pain point
    ↓
customer/business scenario
    ↓
Reliora behaviour
    ↓
technical evidence
    ↓
business or engineering implication
```

High-value evidence to capture while cloud resources exist includes:

- customer support journey;
- Gateway/Lambda/backend side effect;
- matching authoritative ticket;
- correlation/trace path;
- controlled dependency failure;
- idempotent retry;
- CloudWatch/AgentCore operational evidence;
- evaluation/regression result;
- CI gate failure/success where available;
- deployment verification;
- teardown/reproducibility evidence;
- measured latency/cost where valid.

Raw screen recordings can be captured before cloud teardown. Voice-over, editing, and face-camera presentation can be completed later.

---

# 15. Source Authority and Contamination Guardrail

Reliora must not inherit requirements from the other Udacity portfolio projects merely because their documents exist elsewhere.

Current Reliora source authority:

## Primary P1-S1 authority

- `Project-Customer Support Chatbot with Amazon Bedrock AgentCore.txt`

## P1 implementation/submission support

- `AgentCore-Project-Runbook_1.pdf`
- `Useful-github-links-for-this-project.txt`

## Secondary peer/reviewer observations

- `How-to-1.1.txt`
- `How-to-1.2.txt`

These may explain reviewer behaviour but do not override the official project specification.

## P1-S2 production research

- `deep-research-report for P1-S2.md`

## This living product charter

- `RELIORA-PRODUCT-NORTH-STAR.md`

Project 2 and Project 3 specifications must not be used to define Reliora requirements unless an independent Reliora requirement justifies the same capability.

---

# 16. Delivery Priority Through the AWS Deadline

The AWS deadline changes sequencing, not the product quality standard.

Cloud-dependent evidence must be captured before cloud credits/free-tier constraints become a blocker.

Priority order:

## Priority 1 — Reliora S-tier core

Finish the highest-value Reliora product path and capture irreplaceable cloud evidence.

## Priority 2 — Other projects' mandatory cloud work

Complete the cloud-dependent work required to preserve the ability to finish Projects 2 and 3 after the AWS deadline.

## Priority 3 — Post-cloud polish

Can happen after cloud teardown:

- README polish;
- long-form documentation;
- final diagrams;
- video editing;
- voice-over;
- LinkedIn posts;
- portfolio website integration;
- Learning Ledger refinement.

Do not sacrifice a coherent S-tier Reliora for three half-complete portfolios.

---

# 17. Change-Control Rule for This Document

This file is a **living source of truth**, but changes should be deliberate.

Update it when:

- a product requirement materially changes;
- an accepted ADR changes architecture;
- an experiment changes a product decision;
- a new scope boundary is accepted;
- a major product demonstration is added or removed;
- the delivery priority changes materially.

Do not update it for ordinary implementation details.

When updating, preserve the intent of earlier decisions and add a concise change note.

---

# 18. Current North-Star Check

Before accepting a new feature, ask:

1. Does it solve a documented customer/business problem?
2. Does it materially improve adoptability, reliability, safety, observability, or economics?
3. Is it required to demonstrate the product credibly?
4. Does it produce evidence valued by a serious engineering buyer or hiring manager?
5. Is there a simpler way to achieve the same outcome?
6. Does it steal time from a higher-value cloud-dependent deliverable?

If the feature cannot justify itself through those questions, it should normally remain out of scope.

---

## Current guiding statement

> **Build less, prove more. Make Reliora feel like a focused product a retailer could pilot, while proving the engineering controls required to operate AI support safely and economically.**
