# Reliora Retrospective Customer Discovery Brief

**Product:** Reliora — AI Customer-Support Reliability and Control Platform for Online Commerce
**Lifecycle stage:** M1 — Product-Lifecycle Repair
**Discovery mode:** Retrospective
**Date:** 2026-09-17
**Status:** Discovery evidence in progress
**Production/customer claim:** None

---

# 1. Purpose

This document reconstructs the customer, operational, buyer, and problem context that should inform Reliora before additional product expansion.

It is intentionally retrospective.

Reliora began from the Udacity/AWS P1 customer-support implementation and subsequently developed substantial architecture, reliability, evaluation, governance, infrastructure, and evidence controls before a formal customer-discovery gate was created.

This document does not rewrite that history.

Its purpose is to determine whether continued investment in Reliora is justified by a credible real-world problem and whether the current product direction should:

- continue;
- narrow;
- pivot;
- stop;
- or remain deferred pending evidence.

The governing question is:

> What customer or operational problem earns the next unit of engineering investment?

Technology is deliberately secondary.

---

# 2. Evidence Classification

Every discovery statement in this document should be interpreted using one of the following evidence classes.

## KNOWN FROM P1 / CURRENT IMPLEMENTATION

Facts directly established by:

- the official P1 system;
- the current Reliora codebase;
- deterministic tests;
- experiments;
- preserved evidence;
- accepted Reliora decisions.

This is technical/product evidence.

It is not automatically customer-market evidence.

## INDUSTRY-RESEARCH EVIDENCE

Evidence derived from the Reliora deep-research work and cited external industry or engineering sources.

This evidence can establish that a problem class plausibly exists in real organizations.

It does not prove:

- that a specific retailer experiences the problem;
- that a specific buyer will pay for Reliora;
- that Reliora produces business ROI.

## SYNTHETIC CUSTOMER ASSUMPTION

A deliberately simulated customer, workflow, workload, organization, cost, staffing model, or business condition used to design and test the reference implementation.

Synthetic assumptions must never be represented as observed customer facts.

## UNVALIDATED BUYER HYPOTHESIS

A plausible economic buyer or organizational owner whose willingness to sponsor, purchase, adopt, or operate Reliora has not been directly validated.

## OPEN QUESTION

A question that currently lacks sufficient evidence and must remain unresolved until research, experiment, expert review, pilot evidence, or customer discovery provides an answer.

---

# 3. Source Anchors

This discovery brief is derived from Reliora-specific sources including:

- `RELIORA-PRODUCT-NORTH-STAR.md`;
- Reliora Product Constitution;
- Reliora functional and non-functional requirements;
- Reliora Solutions Architect Decision Journal;
- Reliora End-to-End Solutions Architect Delivery Blueprint;
- `deep-research-report for P1-S2.md`;
- preserved P1-S1 requirements and evidence;
- `RELIORA_PRODUCT_LIFECYCLE_AND_ARCHITECTURE_AUDIT.md`;
- `RELIORA_MITIGATION_PLAN.md`;
- current implementation and test evidence.

Cross-project products are not sources of Reliora requirements.

---

# 4. Representative Customer Profile

**Evidence class:** SYNTHETIC CUSTOMER ASSUMPTION

The working reference customer is a small-to-mid-size or growing online retailer.

The organization:

- sells products through digital commerce channels;
- receives customer-support requests through one or more online channels;
- has enough support volume that automation is attractive;
- has engineering or platform capability sufficient to integrate APIs and cloud services;
- does not want an LLM to operate as an uncontrolled business-action engine;
- needs human support to remain available for unsupported, uncertain, failed, or sensitive cases;
- values predictable operations more than maximum agent autonomy.

Reference geographies may include:

- United States;
- United Kingdom;
- Canada;
- South Africa;
- comparable digital-commerce markets.

No real retailer is represented by this profile.

No company size, ticket volume, revenue, staffing level, support cost, or AI budget should be treated as factual until separately evidenced.

---

# 5. Stakeholder Map

## 5.1 Primary end user

**Evidence class:** PRODUCT HYPOTHESIS / CURRENT PRODUCT DEFINITION

The primary end user is the retailer's customer seeking support.

Desired experience:

- receive a useful answer when the request is supported;
- avoid unnecessary repetition;
- avoid unsafe or incorrect automated action;
- reach a human when automation is inappropriate or unsuccessful;
- receive confirmation only when a business action is actually authoritative.

## 5.2 Support agent

**Evidence class:** PRODUCT HYPOTHESIS

The support agent may receive escalated cases.

Potential needs include:

- sufficient customer context;
- reason for handoff;
- information already collected;
- attempted automated actions;
- relevant failure state;
- minimal unnecessary sensitive information.

Whether this matches a real retailer's support-agent workflow is currently unvalidated.

## 5.3 Support / CX leadership

**Evidence class:** UNVALIDATED BUYER HYPOTHESIS

Potential interests:

- support workload;
- quality;
- unnecessary handoff;
- false automation;
- customer effort;
- resolution outcomes;
- escalation quality;
- operating cost.

## 5.4 CTO / VP Engineering

**Evidence class:** UNVALIDATED BUYER HYPOTHESIS

Potential interests:

- architecture risk;
- integration burden;
- security;
- reliability;
- engineering ownership;
- cloud cost;
- observability;
- deployment reproducibility;
- failure and rollback behaviour.

## 5.5 Head of AI / Automation

**Evidence class:** UNVALIDATED BUYER HYPOTHESIS

Potential interests:

- AI adoption;
- safe autonomy;
- model and prompt governance;
- evaluation;
- regression controls;
- operational evidence;
- cost versus value.

## 5.6 E-commerce Operations

**Evidence class:** UNVALIDATED BUYER HYPOTHESIS

Potential interests:

- support throughput;
- customer experience;
- operational disruption;
- duplicate actions;
- escalation;
- incident impact.

## 5.7 Engineering / platform / reliability teams

**Evidence class:** PRODUCT HYPOTHESIS

Potential operational responsibilities include:

- integrations;
- infrastructure;
- monitoring;
- incident diagnosis;
- deployment;
- rollback;
- access control;
- reliability.

Exact ownership remains an open validation question.

---

# 6. Core Problem Thesis

Reliora is not primarily attempting to answer:

> Can an LLM answer a customer question?

The current product thesis is:

> Can an organization operate AI-assisted customer support reliably, safely, observably, economically, and with controlled business actions?

This thesis is currently supported by:

- P1/current implementation evidence showing the technical workflow exists;
- Reliora's reliability and control engineering work;
- industry research indicating that operational control, observability, human escalation, cost, integration, and safe autonomy are meaningful production concerns.

It is not yet supported by direct Reliora customer interviews or paid-pilot evidence.

---

# 7. Problem Inventory

## 7.1 Unreliable AI behaviour

**Evidence class:** INDUSTRY-RESEARCH EVIDENCE + PRODUCT REQUIREMENT

Potential symptom:

A support system appears generally accurate while violating an important behavioural rule.

Reliora response:

Separate:

- deterministic behavioural invariants;
- generative quality;
- operational reliability;
- business outcome.

Customer-specific frequency and cost are unknown.

## 7.2 Incorrect or unnecessarily expensive routing

**Evidence class:** INDUSTRY-RESEARCH EVIDENCE + EXPERIMENTAL RELIORA EVIDENCE

Potential symptom:

Every request is routed through an unnecessarily expensive or unpredictable decision path.

Reliora has already investigated deterministic and classical routing alternatives.

Whether routing cost is a material buying trigger for a real retailer remains unvalidated.

## 7.3 Unsafe persistent side effects

**Evidence class:** PRODUCT REQUIREMENT + INDUSTRY-RESEARCH EVIDENCE

Potential symptom:

An AI system proposes or executes a persistent business action without sufficient deterministic control.

Reliora's current principle is:

> The LLM may propose; deterministic software validates and authorizes.

Current controls include concepts such as:

- typed input;
- deterministic authorization;
- stable logical operation identity;
- idempotency;
- backend confirmation.

The real-world frequency of unsafe support-agent side effects at target retailers is unknown.

## 7.4 Retry and duplicate-action risk

**Evidence class:** IMPLEMENTATION / RELIABILITY EVIDENCE + INDUSTRY-RESEARCH EVIDENCE

Potential symptom:

A timeout or retry creates two business records for one logical customer action.

Reliora has substantial local implementation evidence for:

- duplicate suppression;
- replay;
- conflict;
- timeout ambiguity;
- reconciliation;
- unconfirmed outcomes.

The target-cloud transport contract remains partially unproven.

## 7.5 Poor failure diagnosis

**Evidence class:** INDUSTRY-RESEARCH EVIDENCE + PRODUCT REQUIREMENT

Potential symptom:

An operator knows an AI interaction failed but cannot reconstruct:

- the request;
- route;
- policy decision;
- proposed action;
- authorization;
- backend state;
- retry;
- failure;
- version context.

Reliora treats reconstructability as an important product capability.

Customer-specific current incident-diagnosis time is unknown.

## 7.6 Poor human escalation

**Evidence class:** INDUSTRY-RESEARCH EVIDENCE + PRODUCT REQUIREMENT

Potential symptom:

The customer becomes trapped in automation or repeats information after escalation.

Reliora intends to treat handoff as a structured workflow outcome.

A minimum structured handoff implementation remains outstanding.

## 7.7 Release regression

**Evidence class:** ENGINEERING RISK + INDUSTRY-RESEARCH EVIDENCE

Potential symptom:

A change to code, prompt, model, router, policy, or knowledge silently changes important behaviour.

Reliora already has deterministic evaluation foundations but does not yet have the complete behavioural release gate required by the mitigation plan.

## 7.8 AI operating cost without demonstrated value

**Evidence class:** INDUSTRY-RESEARCH EVIDENCE

Potential symptom:

AI expenditure increases while the organization cannot demonstrate improved successful support outcomes.

Candidate useful measures include:

- model calls per request;
- tool calls per request;
- latency;
- cost per request;
- cost per successful eligible resolution.

No real Reliora customer economics have been measured.

---

# 8. Known Technical Baseline Workflow

**Evidence class:** KNOWN FROM P1 / CURRENT IMPLEMENTATION

The inherited support workflow contains three high-level request categories:

```text
customer request
      |
      v
BUG / PLATFORM / OTHER
```

## BUG

The system collects required structured bug-report information and may invoke a persistent bug-ticket action.

Reliora subsequently introduced stronger controls around:

- authorization;
- operation identity;
- idempotency;
- conflict detection;
- authoritative persistence;
- reconciliation;
- failure classification.

## PLATFORM

Supported questions can be answered from the approved product knowledge boundary.

Unsupported questions should move toward human support rather than fabricated answers.

## OTHER

Requests outside supported automated scope move toward human assistance.

This is a known Reliora workflow.

It must not be confused with the exact current-state workflow of a real retailer.

---

# 9. Real Retailer Current-State Workflow

**Evidence class:** OPEN QUESTION

We do not currently know how a specific target retailer handles the equivalent workflow.

Questions requiring validation include:

1. Through which channels do customers request support?
2. Is triage performed by humans, rules, AI, or a mixture?
3. What helpdesk or CRM system owns the support record?
4. What support actions can agents currently execute?
5. Which actions require authentication or approval?
6. What happens after a support-system timeout?
7. What prevents duplicate actions today?
8. How are incidents investigated?
9. How is context transferred during escalation?
10. What information is customers commonly forced to repeat?
11. Which support categories drive the most volume?
12. Which support categories drive the greatest cost or risk?

Until these questions are answered for a real organization, the retailer workflow remains a hypothesis.

---

# 10. Incumbent Alternatives

The following are candidate incumbent approaches to investigate.

They are not yet ranked.

## Manual / predominantly human support

**Evidence class:** PLAUSIBLE INCUMBENT HYPOTHESIS

Potential advantages:

- human judgment;
- flexible exception handling.

Potential limitations to validate:

- cost;
- queue time;
- repetitive work;
- inconsistent handling.

## Conventional chatbot / helpdesk automation

**Evidence class:** PLAUSIBLE INCUMBENT HYPOTHESIS

Potential advantages:

- established integrations;
- mature support workflows.

Questions:

- how well do incumbent products handle safe side effects?
- what evaluation/release controls already exist?
- is Reliora meaningfully differentiated?

## Deterministic workflow / rules engine

**Evidence class:** PLAUSIBLE ALTERNATIVE

Potential advantages:

- predictability;
- low inference cost;
- explainability.

Questions:

- which support categories actually require generative reasoning?
- could a simpler deterministic system solve enough of the problem?

## Existing AI customer-support SaaS

**Evidence class:** OPEN MARKET QUESTION

Reliora must eventually compare its value proposition against established commercial support automation.

No competitive superiority claim is currently supported.

## No change

**Evidence class:** REQUIRED BASELINE ALTERNATIVE

A credible product decision must allow the conclusion that the organization should keep its existing process if Reliora does not create sufficient incremental value.

---

# 11. Failure and Retry Discovery

## What Reliora already knows technically

**Evidence class:** KNOWN FROM CURRENT IMPLEMENTATION

Reliora has explicitly modelled cases including:

- matching retries;
- conflicting retries;
- concurrent operations;
- ambiguous writes;
- timeout after possible success;
- timeout without authoritative state;
- access denial;
- incomplete state.

## What remains unknown from a customer perspective

**Evidence class:** OPEN QUESTION

We do not yet know:

- how often target retailers experience equivalent failures;
- how duplicates are currently detected;
- the operational cost of duplicate support actions;
- the acceptable time to resolve ambiguous outcomes;
- who owns reconciliation;
- whether support platforms already provide sufficient protections.

---

# 12. Observability Discovery

## Reliora target

Operators should be able to reconstruct important behaviour through structured provenance rather than hidden model reasoning.

Potential context includes:

- request identity;
- session identity;
- logical operation identity;
- route;
- authorization outcome;
- backend outcome;
- failure category;
- version context;
- timing.

## Customer evidence gap

**Evidence class:** OPEN QUESTION

We do not know:

- what observability target retailers currently possess;
- what telemetry their helpdesk or AI platform already provides;
- how long diagnosis takes today;
- which incidents are difficult to reconstruct;
- whether observability is a primary buyer pain or only an engineering concern.

---

# 13. Human Escalation Discovery

Reliora assumes human access remains part of the support system.

The target handoff should preserve useful context while minimizing unnecessary data.

## Open questions

1. Which events should force handoff?
2. Which events merely permit handoff?
3. Which team receives the escalation?
4. What context does that team actually need?
5. Which information must never be transferred?
6. How is ownership acknowledged?
7. What happens if no human is available?
8. How is resolution fed back into evaluation or product learning?

---

# 14. Data, Security, and Privacy Discovery

Potential customer-support data may include:

- free-form user text;
- contact information;
- account identifiers;
- device/environment details;
- troubleshooting information;
- support history.

Reliora should minimize collection to the purpose of the supported workflow.

## Open validation questions

- What data is permitted in model inputs?
- What data is permitted in logs?
- What data is permitted in evaluation datasets?
- What must be redacted?
- What retention period is required?
- Who can access support records?
- Which regions may process or store data?
- Which actions require customer authentication?
- Which actions require employee approval?
- What deletion obligations apply?
- What incident-notification requirements apply?

No compliance claim should be made until the relevant deployment context is known.

---

# 15. Staffing and Operational Constraints

**Evidence class:** SYNTHETIC CUSTOMER ASSUMPTION / OPEN QUESTION

A target retailer is assumed not to have unlimited AI-platform engineering capacity.

That assumption supports Reliora's preference for:

- managed services where justified;
- bounded architecture;
- limited operational burden;
- reproducible deployment;
- explicit failure handling;
- minimal unnecessary infrastructure.

This assumption requires validation.

Questions include:

- Who operates the system?
- Is there an SRE or platform team?
- Is support available outside business hours?
- Who owns prompts/models?
- Who owns support policy?
- Who owns security incidents?
- Who can approve a rollback?
- How much operational complexity can the organization sustain?

---

# 16. Business Pain and Baseline Measures

Reliora currently lacks real customer baseline measurements for:

- request volume;
- request-category distribution;
- current successful resolution rate;
- current handoff rate;
- false automation;
- unnecessary handoff;
- duplicate logical action rate;
- average diagnosis time;
- customer repetition during handoff;
- human handling time;
- human handling cost;
- AI cost;
- incident rate;
- release regression rate.

These must remain UNKNOWN unless measured.

Synthetic values may later be used for experiments or financial modelling, but must remain explicitly labelled synthetic.

---

# 17. Desired Outcomes

The current product hypothesis is that a credible deployment should improve some combination of:

- correct eligible automated resolution;
- safe execution;
- duplicate prevention;
- handoff quality;
- customer effort;
- failure diagnosis;
- regression prevention;
- operational predictability;
- cost efficiency.

These are candidate outcomes.

They are not yet validated customer success criteria.

---

# 18. Buyer Hypotheses

The following buyer hypotheses remain unvalidated.

## Hypothesis B1 — Customer Support / CX leadership

They may sponsor Reliora if it can improve support outcomes without increasing customer frustration or operational risk.

## Hypothesis B2 — CTO / VP Engineering

They may sponsor Reliora if AI customer-support adoption is desirable but existing solutions create unacceptable reliability, integration, security, or operational risk.

## Hypothesis B3 — Head of AI / Automation

They may sponsor Reliora if they need stronger evaluation, side-effect control, evidence, and release governance around AI-assisted support.

## Hypothesis B4 — E-commerce Operations

They may influence adoption if support automation materially affects operational workload or customer experience.

## Hypothesis B5 — Platform Engineering

They may be an evaluator or implementation owner rather than the economic buyer.

No hypothesis currently establishes willingness to purchase.

---

# 19. Discovery Questions for Future Validation

## Customer Support / CX

1. Which support categories generate the greatest volume?
2. Which generate the highest cost?
3. Which failures create the greatest customer frustration?
4. Where do customers abandon automation?
5. What information do customers repeat during escalation?
6. What automation errors are considered unacceptable?
7. What must always reach a person?

## Engineering / Platform

8. What systems own support state?
9. Which persistent actions are available through APIs?
10. How are retries handled?
11. How are duplicate actions prevented?
12. How are incidents reconstructed?
13. What deployment and rollback mechanisms exist?
14. What observability already exists?
15. What integration burden would be acceptable?

## Security / Privacy

16. What customer data can enter AI systems?
17. Which actions require identity or approval?
18. What retention/deletion rules apply?
19. What audit evidence is required?
20. What provider or regional constraints exist?

## Finance / Operations

21. What does a support interaction cost today?
22. Which cost is actually worth reducing?
23. What failure creates the largest rework burden?
24. What would justify a pilot?
25. What would cause the organization to stop the pilot?

## Buyer

26. Who owns the budget?
27. Who experiences the pain most directly?
28. Who can veto deployment?
29. Who must operate the solution after implementation?
30. What evidence would each stakeholder require before adoption?

---

# 20. Current Evidence Gaps

The following remain materially unresolved:

- no direct Reliora customer interview evidence;
- no verified retailer workflow;
- no validated economic buyer;
- no willingness-to-pay evidence;
- no real baseline support cost;
- no real support-volume baseline;
- no measured customer-effort baseline;
- no measured handoff baseline;
- no real deployment adoption evidence;
- no live-pilot evidence;
- no real ROI evidence.

These are discovery gaps, not reasons to fabricate evidence.

---

# 21. What Existing Engineering Evidence Does Prove

Current Reliora engineering evidence supports statements about the system itself.

It can support claims such as:

- deterministic controls exist locally;
- authorization occurs before ticket execution;
- request/session/operation identity are distinct concepts;
- local replay/conflict/reconciliation behaviour has been tested;
- deterministic evaluation exists;
- the codebase has a reproducible local quality baseline.

It does not prove:

- customer demand;
- willingness to pay;
- production reliability;
- customer ROI;
- production cost savings;
- adoption.

---

# 22. Retrospective Discovery Decision Status

This document alone does not authorize a `CONTINUE` decision.

Current status:

```text
TECHNICAL PROBLEM CREDIBILITY      SUPPORTED
INDUSTRY PROBLEM CREDIBILITY       SUPPORTED
TARGET CUSTOMER DEFINITION         HYPOTHESIZED
END-USER DEFINITION                HYPOTHESIZED / PRODUCT-DEFINED
ECONOMIC BUYER                     UNVALIDATED
CURRENT RETAILER WORKFLOW          UNKNOWN
CUSTOMER-SPECIFIC SEVERITY         UNKNOWN
WILLINGNESS TO PAY                 UNKNOWN
REAL ROI                           UNKNOWN
```

The next lifecycle control is the formal:

> Problem–Buyer Evidence Gate

That gate must determine whether current evidence justifies:

```text
CONTINUE
NARROW
PIVOT
STOP
DEFER
```

---

# 23. Discovery Guardrails

1. Do not invent customer interviews.
2. Do not invent buyer quotes.
3. Do not invent ticket volumes.
4. Do not invent ROI.
5. Do not convert industry statistics into Reliora customer facts.
6. Do not convert local engineering tests into production evidence.
7. Do not add technology to compensate for missing customer evidence.
8. Do not redefine the product merely to preserve previous engineering investment.
9. Preserve useful existing Reliora engineering if the product thesis survives.
10. Be willing to narrow, pivot, defer, or stop if future evidence requires it.

---

# 24. M1.1 Exit Condition

M1.1 is complete when:

- the representative customer is explicitly synthetic;
- actors and buyer hypotheses are visible;
- the known Reliora workflow is separated from an unknown real retailer workflow;
- industry evidence is separated from customer evidence;
- baseline metrics that do not exist remain unknown;
- incumbent approaches are identified without unsupported ranking;
- customer, operational, security, and buyer questions are documented;
- the artifact does not imply that Reliora has real customers;
- the next decision gate is explicit.

At that point Reliora may proceed to M1.2:

> **Problem–Buyer Evidence Gate**

---

# 25. M1.2 Problem-Buyer Evidence Gate Assessment

**Assessment date:** 2026-09-17

**Assessment mode:** Retrospective

**Current gate outcome:** `NARROW`

## 25.1 Why the current outcome is NARROW

The available evidence supports continued work on a bounded production-oriented reference implementation, but it does not currently support broad product expansion or market-validation claims.

Current evidence supports:

- a credible technical problem class;
- a credible industry problem class;
- a defined target-customer hypothesis;
- a coherent product boundary around safe AI-assisted support;
- substantial local engineering evidence for deterministic control, authorization, idempotency, replay, conflict handling, reconciliation, evaluation, and failure handling.

Current evidence does not yet establish:

- a validated real retailer workflow;
- a validated economic buyer;
- willingness to pay;
- customer-specific problem frequency or severity;
- real support economics;
- real adoption;
- production ROI.

`STOP` is not justified because the problem class remains credible and the current technical work addresses independently documented reliability and control risks.

`PIVOT` is not justified because current evidence has not demonstrated that another problem, buyer, or workflow is materially stronger.

A broad `CONTINUE` decision is not justified because customer-specific and buyer evidence remain insufficient.

A complete `DEFER` is unnecessary because Reliora can continue generating high-value technical and target-environment evidence inside a deliberately bounded reference-implementation scope.

Therefore, the current evidence supports `NARROW`.

## 25.2 Scope authorized by NARROW

Reliora may continue work that strengthens the existing reliability-and-control thesis, including:

- the existing `BUG / PLATFORM / OTHER` support boundary;
- deterministic authorization;
- stable logical-operation identity;
- idempotent execution and reconciliation;
- structured human handoff;
- reconstructable operational evidence;
- deterministic and generative evaluation;
- behavioural release controls;
- bounded target-cloud verification;
- measured workload and unit-cost evidence where available;
- reproducible deployment and recovery evidence.

Each item still requires its own architecture and evidence gate where applicable.

## 25.3 Scope not authorized by the current evidence

The current gate does not authorize expansion merely for capability breadth, including:

- additional autonomous business-action workflows without an independently evidenced need;
- multi-agent architecture;
- mandatory RAG or vector infrastructure;
- persistent personalized memory;
- browser or code-interpreter capability;
- Kubernetes/EKS;
- Kafka/MSK;
- Redis;
- enterprise multi-tenancy and billing;
- multi-region architecture;
- broad commerce, payment, warehouse, inventory, or order-management functionality.

It also does not authorize claims of:

- validated customer demand;
- willingness to pay;
- production reliability;
- real customer ROI;
- measured labour savings;
- commercial adoption.

## 25.4 Evidence that could support a later CONTINUE decision

A broader continuation decision would require stronger evidence such as:

- direct evidence from relevant customer-support, CX, engineering, AI/automation, or operations stakeholders;
- evidence of the actual current-state support workflow and its failure points;
- evidence that a plausible buyer or economic owner materially owns the problem;
- evidence that incumbent approaches leave a meaningful unresolved gap;
- at least one measurable customer or operational baseline relevant to the intended value;
- evidence that the operating burden and risk are proportionate to the expected benefit.

No arbitrary interview count is treated as sufficient by itself. Evidence quality and relevance matter more than document volume.

## 25.5 Evidence that could trigger PIVOT or STOP

Reassess toward `PIVOT` or `STOP` if credible evidence shows that:

- the target problem is low priority;
- incumbent products solve the problem sufficiently;
- the assumed buyer does not own or fund the problem;
- a materially different workflow has stronger value;
- the required operating model is disproportionate;
- the AI component provides no meaningful advantage over simpler deterministic software;
- the strongest value lies in a materially different product boundary.

## 25.6 Immediate consequence

The next Reliora product-lifecycle work should not be feature expansion.

The next evidence work should compare product-level alternatives and define a measurable value hypothesis for the narrowed scope.

This assessment does not modify the technical evidence maturity of the project.

---

# 26. M1.2 Exit Condition

M1.2 is complete when:

- the permanent problem-buyer governance gate exists in the Product Constitution;
- the current retrospective gate has been applied;
- the decision outcome is explicit;
- the authorized and non-authorized scope are explicit;
- no customer, buyer, production, or ROI evidence has been invented;
- the next evidence required for a broader continuation decision is explicit.

Current outcome:

> **NARROW - continue Reliora as a bounded reliability-and-control reference implementation while deferring broad expansion and commercial validation claims until stronger customer/buyer evidence exists.**
