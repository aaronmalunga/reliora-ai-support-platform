# Reliora Product Alternatives and Measurable Value Hypothesis

**Product:** Reliora - AI Customer-Support Reliability and Control Platform for Online Commerce
**Lifecycle stage:** M1.3 - Product-Level Alternatives and Value Hypothesis
**Date:** 2026-09-17
**Status:** Retrospective product-lifecycle repair
**Current product gate:** NARROW
**Customer/production claim:** None
**Financial claim:** None

---

# 1. Purpose

This document evaluates whether the narrowed Reliora product direction is an economically and operationally defensible intervention relative to simpler or incumbent alternatives.

It exists to answer a product question before additional feature expansion:

> What is the smallest solution that can credibly address the reliability-and-control problem Reliora is targeting, and what evidence would show that the solution creates value?

This is not a vendor-selection document and it is not a claim that Reliora is superior to commercial alternatives.

The current evidence base is sufficient to compare solution shapes and define measurable hypotheses.

It is not sufficient to claim:

- validated market demand;
- willingness to pay;
- production reliability;
- real customer ROI;
- labour savings;
- commercial superiority.

---

# 2. Governing Context

Reliora is currently operating under a `NARROW` product decision.

The authorized scope is a bounded production-oriented reference implementation focused on:

- AI-assisted customer support;
- deterministic authorization;
- stable logical-operation identity;
- retry-safe and idempotent side effects;
- reconciliation of ambiguous outcomes;
- structured human handoff;
- reconstructable operational evidence;
- deterministic and generative evaluation;
- behavioural release controls;
- bounded target-environment verification;
- reproducible delivery.

This document does not broaden that scope.

The governing product rule remains:

> The product chooses the technology; the technology does not choose the product.

The governing execution rule remains:

> The LLM may propose; deterministic software validates and authorizes.

---

# 3. Evidence Discipline

The analysis below separates five evidence states.

## 3.1 KNOWN FROM CURRENT RELIORA

Facts supported by current implementation, tests, experiments, preserved evidence, or accepted product decisions.

## 3.2 INDUSTRY-RESEARCH EVIDENCE

Evidence that the wider problem class exists in real organizations.

Industry evidence does not prove that a specific retailer experiences the problem or would buy Reliora.

## 3.3 SYNTHETIC ASSUMPTION

A deliberately invented business, workload, cost, staffing, or workflow assumption used for modelling or experiment design.

## 3.4 PRODUCT HYPOTHESIS

A plausible proposition that has not yet been validated with a real target customer or buyer.

## 3.5 OPEN QUESTION

A material unknown that requires discovery, measurement, target-environment evidence, or customer evidence.

---

# 4. Decision Question

The relevant comparison is not:

> Is Reliora technically sophisticated?

The relevant comparison is:

> For the narrowed reliability-and-control problem, does Reliora provide enough incremental value over simpler or incumbent approaches to justify its additional engineering and operating burden?

Every alternative must therefore be allowed to remain viable.

A simpler solution is preferred when it can satisfy the actual requirement with lower risk, lower cost, or lower operational burden.

---

# 5. Alternative A0 - No Change

**Evidence state:** REQUIRED BASELINE ALTERNATIVE

## 5.1 Description

The organization keeps its current support process and makes no Reliora-style architectural intervention.

This alternative matters because the correct product decision can be to do nothing.

## 5.2 Potential reasons to choose it

- the current support process is already adequate;
- automation volume is too low to justify investment;
- the identified failures are rare or low impact;
- existing helpdesk controls already solve the relevant problems;
- integration cost exceeds plausible value;
- the organization does not want AI-assisted business actions.

## 5.3 What must be learned

- current support cost;
- current failure frequency;
- current duplicate-action frequency;
- current handoff quality;
- current incident-diagnosis burden;
- current release-regression burden;
- current AI/tool operating cost.

## 5.4 Reliora implication

If real evidence shows that the current process already meets the important outcome requirements, Reliora should not be introduced merely to demonstrate technology.

---

# 6. Alternative A1 - Predominantly Human Support

**Evidence state:** PLAUSIBLE INCUMBENT HYPOTHESIS

## 6.1 Description

Human support agents perform most triage, reasoning, escalation, and business-action work.

Automation may be limited to basic forms, macros, or routing.

## 6.2 Potential strengths

- flexible human judgment;
- natural handling of exceptions;
- low autonomous-action risk;
- existing organizational familiarity;
- no model-governance dependency for the core workflow.

## 6.3 Potential limitations requiring validation

- labour cost;
- queue delay;
- repetitive work;
- inconsistent case handling;
- difficult scaling during bursts;
- manual context transfer;
- manual diagnosis and rework.

## 6.4 When it may be the simpler answer

Human-first support may remain appropriate when:

- support volume is modest;
- cases are highly variable;
- business actions are high risk;
- automation accuracy is insufficient;
- human review is required regardless of automation.

## 6.5 Reliora implication

Reliora must not treat human involvement as failure.

Human handoff is part of the intended control system.

---

# 7. Alternative A2 - Deterministic Workflow / Rules Automation

**Evidence state:** PLAUSIBLE SIMPLER ALTERNATIVE

## 7.1 Description

A rules engine or conventional workflow system handles supported categories through deterministic logic without generative reasoning.

## 7.2 Potential strengths

- predictable execution;
- explicit business logic;
- comparatively easy testing;
- lower model dependency;
- lower inference cost;
- straightforward auditability for bounded workflows.

## 7.3 Potential limitations requiring validation

- brittle handling of open-ended language;
- growing rule maintenance burden;
- poor fit for ambiguous or unstructured requests;
- reduced conversational flexibility;
- difficulty extracting structured facts from varied user language.

## 7.4 Required Reliora comparison

Reliora should use deterministic logic wherever generative reasoning has not earned its place.

A generative component is justified only where it contributes useful flexibility that simpler deterministic software cannot provide economically.

## 7.5 Reliora implication

The deterministic alternative remains a permanent baseline, not an obsolete architecture.

---

# 8. Alternative A3 - Conventional Chatbot / Helpdesk Automation

**Evidence state:** PLAUSIBLE INCUMBENT HYPOTHESIS

## 8.1 Description

The retailer uses established chatbot, ticketing, workflow, knowledge, and escalation capabilities from a conventional support platform.

## 8.2 Potential strengths

- established support workflows;
- mature ticketing and CRM integration;
- agent workspace integration;
- organizational familiarity;
- existing escalation and reporting capabilities.

## 8.3 Open comparison questions

- how are persistent AI-proposed actions authorized?
- what idempotency semantics exist for side effects?
- how are ambiguous outcomes reconciled?
- can behavioural invariants be release-gated?
- how complete is request-to-backend reconstruction?
- how are model, prompt, policy, and workflow versions attributed?
- what portability or customization burden exists?
- what is the actual operating cost?

## 8.4 Reliora implication

Reliora has no basis to claim superiority over a conventional platform until a real deployment context and incumbent system are identified.

---

# 9. Alternative A4 - Commercial AI Customer-Support SaaS

**Evidence state:** OPEN MARKET QUESTION

## 9.1 Description

The retailer buys a commercial AI-support platform rather than building or adapting Reliora.

## 9.2 Potential strengths

A commercial platform may provide:

- faster time to adoption;
- packaged integrations;
- managed operations;
- vendor support;
- prebuilt agent tooling;
- analytics;
- established customer-service workflows.

## 9.3 Open comparison questions

Reliora cannot assume a commercial product lacks the controls it demonstrates.

A real comparison would need to evaluate:

- deterministic policy enforcement;
- business-action authorization;
- side-effect idempotency;
- retry semantics;
- ambiguous-outcome handling;
- human handoff;
- evaluation and release governance;
- observability;
- evidence export;
- data residency and privacy;
- integration effort;
- configuration portability;
- unit economics;
- contractual and supplier risk.

## 9.4 Reliora implication

A commercial SaaS option may be the correct choice for a real retailer.

Reliora's value must come from requirements and evidence, not from the fact that it is custom-built.

---

# 10. Alternative A5 - Reliability / Control Middleware Around an Existing AI System

**Evidence state:** PRODUCT HYPOTHESIS

## 10.1 Description

Instead of replacing the customer-facing support application, a retailer keeps its existing AI/chat/helpdesk layer and introduces only a reliability-and-control layer around risky operations.

The layer could provide selected capabilities such as:

- typed tool contracts;
- deterministic authorization;
- operation identity;
- idempotency;
- reconciliation;
- structured failure taxonomy;
- behavioural evaluation;
- evidence generation.

## 10.2 Why this alternative matters

This may be materially smaller than deploying Reliora as an end-to-end support product.

It tests whether Reliora's strongest differentiated value is the reliability/control layer itself rather than the full customer-support experience.

## 10.3 Open questions

- can these controls integrate cleanly with incumbent systems?
- who owns the middleware?
- does the incumbent platform already provide equivalent controls?
- is there enough unresolved risk to justify another operational component?
- would integration complexity exceed the value of the control layer?

## 10.4 Pivot signal

If future customer evidence consistently values the control layer while rejecting replacement of the customer-facing support workflow, the product gate should be reassessed for a possible `PIVOT`.

No such pivot is currently validated.

---

# 11. Alternative A6 - Current Reliora Hybrid

**Evidence state:** CURRENT PRODUCT HYPOTHESIS + LOCAL ENGINEERING EVIDENCE

## 11.1 Description

The current Reliora approach combines:

- generative flexibility where appropriate;
- deterministic routing or classical alternatives where evidence supports them;
- typed contracts;
- deterministic authorization;
- retry-safe side effects;
- authoritative persistence;
- reconciliation;
- structured human handoff;
- evaluation and release controls;
- operational evidence.

## 11.2 What current evidence supports

Current Reliora evidence supports the existence and local behaviour of several reliability controls.

It does not yet prove:

- live AgentCore/Gateway identity semantics;
- live end-to-end cloud reliability;
- production availability;
- production unit economics;
- real customer value;
- commercial superiority.

## 11.3 Why this alternative remains worth testing

The hybrid remains a credible experiment because it directly combines the problem classes Reliora is designed to study:

- useful AI flexibility;
- controlled authority;
- retry-safe business actions;
- human fallback;
- observable and testable behaviour.

It remains a hypothesis, not a market winner.

---

# 12. Product-Level Comparison

The following comparison is intentionally non-numeric.

No score is assigned because Reliora does not yet have sufficiently comparable customer, cost, or production evidence.

| Alternative | Primary design advantage | Important limitation / unknown | Evidence needed |
|---|---|---|---|
| A0 No change | Zero new implementation burden | May preserve existing pain | Real current-state baseline |
| A1 Human-first | Flexible judgment and exception handling | Human effort, delay, consistency unknown | Workload, cost, queue, quality baseline |
| A2 Deterministic workflow | Predictable, testable, low model dependence | Open-ended language and maintenance burden | Workflow coverage and exception rate |
| A3 Conventional helpdesk automation | Mature support workflow/integration potential | Control semantics depend on actual platform | Incumbent capability assessment |
| A4 Commercial AI SaaS | Fast adoption and managed capability potential | Vendor controls, cost, portability, governance unknown | Product/vendor evaluation in real context |
| A5 Reliability middleware | Smaller intervention around existing AI | Additional integration/ownership layer | Integration experiment + buyer evidence |
| A6 Reliora hybrid | End-to-end demonstration of AI plus deterministic control | Highest custom engineering burden among bounded options | Target-cloud + customer/value evidence |

The table does not establish a winner.

---

# 13. Simplest-Viable-Alternative Rule

Before adding a Reliora capability, ask in order:

1. Can the problem be solved by leaving the current process unchanged?
2. Can a human workflow solve it acceptably?
3. Can deterministic software solve it?
4. Can an incumbent support platform solve it?
5. Can a commercial AI-support platform solve it?
6. Can a smaller reliability/control layer solve it?
7. Only then, does the end-to-end Reliora hybrid earn the additional complexity?

The answer may differ by workflow.

Reliora does not require one architecture to handle every support problem.

---

# 14. AI Versus Deterministic Boundary

Reliora should use generative AI only where it creates useful flexibility.

Candidate generative work includes:

- interpreting varied natural-language requests;
- collecting structured details conversationally;
- producing bounded customer-facing language;
- summarizing approved context for handoff.

Deterministic software should retain authority over:

- schema validation;
- policy;
- authorization;
- side-effect permission;
- logical-operation identity;
- idempotency;
- conflict handling;
- authoritative-state lookup;
- reconciliation rules;
- release-blocking invariants.

The value hypothesis depends on this division of responsibility.

---

# 15. Measurable Value Thesis

Reliora's product value should not be expressed as:

> We use an advanced agent architecture.

A more defensible thesis is:

> Reliora creates value only if it increases safe, useful support outcomes or reduces avoidable operational burden at an acceptable total cost.

A conceptual value model is:

```text
Quality-adjusted support value
=
safe useful outcomes
/
(AI cost + human effort + rework + failure cost + operating burden)
```

This is a reasoning model, not a measured financial equation.

No monetary coefficient is currently validated.

---

# 16. Value Hypothesis H1 - Safe Eligible Resolution

**Hypothesis**

A controlled hybrid workflow can successfully resolve eligible requests while preventing unauthorized or unverified side effects.

**Candidate measure**

```text
successful eligible resolutions
/
total eligible requests
```

**Required boundary**

"Eligible request" and "successful resolution" must be frozen before reporting.

**Current status**

Target-environment end-to-end evidence is not yet established.

**Evidence needed**

- versioned scenario definition;
- end-to-end execution;
- authoritative business outcome;
- explicit failure/handoff classification.

---

# 17. Value Hypothesis H2 - False Automation

**Hypothesis**

Deterministic authorization and bounded automation can reduce unsafe or incorrect autonomous outcomes compared with a less-controlled AI path.

**Candidate measure**

```text
incorrect autonomous outcomes
/
automated outcomes
```

**Current status**

No real customer baseline exists.

**Evidence needed**

- frozen definition of an incorrect autonomous outcome;
- controlled evaluation set;
- comparison against an appropriate baseline;
- later real deployment evidence where available.

**Claim guardrail**

A low test-set false-automation rate is not automatically a production false-automation rate.

---

# 18. Value Hypothesis H3 - Duplicate Logical Side Effects

**Hypothesis**

Stable operation identity, idempotency, and reconciliation can prevent one logical request from creating duplicate persistent business records under retry conditions.

**Canonical metric**

Duplicate Side-Effect Rate.

**Desired semantic invariant**

```text
0 duplicate executions
```

This is a correctness invariant, not a production SLO.

**Current evidence**

Local deterministic reliability evidence exists.

**Remaining evidence**

Live transport and target-environment verification remain required.

---

# 19. Value Hypothesis H4 - Matching Retry Replay Correctness

**Hypothesis**

A matching retry can return the authoritative previous result without executing the side effect again.

**Canonical metric**

Matching Retry Replay Correctness.

**Current evidence**

Local deterministic tests.

**Remaining evidence**

Live AgentCore/Gateway/Lambda/DynamoDB path.

---

# 20. Value Hypothesis H5 - Human Handoff Quality

**Hypothesis**

A structured handoff package can reduce unnecessary customer repetition and improve operator context compared with a minimal escalation message.

**Candidate measures**

- handoff-package completeness;
- repeated-information rate;
- handoff resolution outcome;
- time from escalation to actionable human context.

**Current status**

The minimum structured handoff implementation remains outstanding.

**Evidence needed**

A controlled comparison using a defined synthetic or pilot workflow.

No real customer-effort improvement is currently claimed.

---

# 21. Value Hypothesis H6 - Failure Diagnosis

**Hypothesis**

Structured request, operation, policy, backend, failure, and version provenance can reduce the effort required to reconstruct an incident.

**Candidate measures**

- trace completeness;
- percentage of required evidence fields present;
- time to reconstruct a defined failure;
- number of systems or logs manually correlated.

**Current status**

Full end-to-end reconstruction is not yet proven.

**Evidence needed**

At least one successful request and one controlled failure reconstructed from target-environment evidence.

---

# 22. Value Hypothesis H7 - Release Regression Control

**Hypothesis**

Deterministic behavioural gates can prevent known unsafe behavioural changes from being promoted.

**Canonical measures**

- deterministic regression pass rate;
- Stage-1 reproduction pass rate;
- deliberate unsafe-change gate failure.

**Current evidence**

Local deterministic evaluation exists.

**Remaining evidence**

CI must demonstrate that an intentionally unsafe change is blocked before promotion.

---

# 23. Value Hypothesis H8 - Routing Efficiency

**Hypothesis**

A deterministic or classical router may reduce expensive model usage for suitable request classes without unacceptable loss of routing quality.

**Candidate measures**

- routing macro F1;
- per-class recall;
- model calls avoided;
- local or cloud routing latency;
- cost per request;
- error severity by route.

**Current evidence**

Controlled routing experiments exist.

**Claim boundary**

Local routing evidence does not establish end-to-end customer value.

---

# 24. Value Hypothesis H9 - Unit Economics

**Hypothesis**

The selected architecture can produce acceptable quality-adjusted support outcomes at a defensible unit cost.

**Canonical metrics**

- Cost per Request;
- Cost per Successful Eligible Resolution;
- Model Calls per Request;
- Tokens per Request;
- Tool Calls per Request.

**Current status**

Cloud unit-cost measurement remains blocked until a valid target environment is available.

No production unit-cost claim exists.

---

# 25. Value Hypothesis H10 - Operational Burden

**Hypothesis**

Reliora's reliability controls create enough operational value to justify their implementation and maintenance burden.

**Candidate measures**

- deployment effort;
- number of operational components;
- incident-diagnosis effort;
- rollback effort;
- runbook steps;
- change-failure evidence;
- engineering time required for routine operation.

**Current status**

No real customer operating model exists.

This remains a product hypothesis.

---

# 26. Metric Governance

Reliora already maintains a canonical Metric Dictionary.

This business case does not redefine those metrics.

The following rules apply:

- the measurement boundary is part of the metric;
- local evidence is not cloud evidence;
- targets follow baselines;
- evidence class and maturity remain separate;
- metric definitions must not silently change;
- no local benchmark is converted into a production SLO;
- no financial claim is made from a synthetic workload alone.

Where this business case proposes a metric that is not yet canonical, the metric must either:

1. remain an explicitly provisional product metric; or
2. be admitted into the Metric Dictionary through normal metric change control before becoming a formal KPI.

---

# 27. Synthetic Economic Model

A synthetic economic model may be used to test sensitivity and architecture trade-offs.

It must not be presented as customer ROI.

Potential variables include:

```text
R  = support requests in the modelled period
E  = fraction of requests eligible for automation
S  = safe successful automation rate
H  = human handling time per escalated case
C_h = synthetic human handling cost per unit time
C_ai = measured or modelled attributable AI/runtime cost
C_r = synthetic rework cost from incorrect automation
C_d = synthetic duplicate-action remediation cost
C_o = synthetic operational/platform burden
```

A quality-adjusted synthetic cost model could be expressed as:

```text
Total modelled cost
=
human handling
+ AI/runtime
+ rework
+ duplicate remediation
+ operating burden
```

and:

```text
Modelled cost per safe successful eligible resolution
=
Total modelled attributable cost
/
safe successful eligible resolutions
```

Every synthetic coefficient must be labelled `SYNTHETIC ASSUMPTION`.

When actual AWS cost becomes measurable, measured infrastructure cost may replace the corresponding synthetic runtime-cost variable.

That does not convert the remaining synthetic business variables into real customer economics.

---

# 28. What Would Constitute Meaningful Value Evidence?

A stronger product case should eventually contain evidence from multiple layers.

## 28.1 Technical outcome evidence

Examples:

- duplicate suppression;
- safe replay;
- conflict rejection;
- authorization;
- handoff schema correctness;
- release-gate failure on unsafe change;
- target-cloud request reconstruction.

## 28.2 Operational evidence

Examples:

- measured target-environment latency;
- target-environment failure rate;
- tool-call counts;
- model-call counts;
- cloud cost per defined unit;
- recovery and rollback evidence.

## 28.3 Customer/workflow evidence

Examples:

- actual current-state workflow;
- stakeholder pain;
- baseline diagnosis effort;
- handoff burden;
- duplicate-action burden;
- support-volume distribution.

## 28.4 Buyer evidence

Examples:

- identified economic owner;
- budget ownership;
- adoption constraints;
- evidence required for a pilot;
- reasons to reject the solution.

## 28.5 Adoption/value evidence

Examples:

- pilot usage;
- repeat use;
- accepted operational workflow;
- measured outcome change;
- willingness to continue or pay.

Reliora currently has meaningful evidence mainly in the technical layer.

---

# 29. Smallest Useful Product Experiments

The next experiments should remove uncertainty, not add features.

## Experiment E1 - Trusted logical-operation identity

Question:

Can the real AgentCore/Gateway/Lambda path preserve trusted logical-operation identity with the semantics required by Reliora's idempotency design?

This is the ADR-017 experiment.

## Experiment E2 - Structured handoff

Question:

Can a minimum handoff package preserve useful context without leaking unnecessary information?

## Experiment E3 - End-to-end reconstruction

Question:

Can an operator reconstruct one successful request and one controlled failure without hidden model reasoning?

## Experiment E4 - Behavioural release block

Question:

Does a deliberate unsafe behavioural change fail the deterministic release gate and prevent promotion?

## Experiment E5 - Target-environment unit cost

Question:

What is the measured cost per request and cost per successful eligible resolution under a frozen synthetic workload?

## Experiment E6 - Customer/problem validation

Question:

Do relevant support, CX, engineering, AI/automation, or operations stakeholders recognize the narrowed problem as material, and what incumbent process do they use today?

No arbitrary interview count alone closes this experiment.

---

# 30. Technology Admission Consequence

This analysis does not authorize new technology.

Current evidence does not establish a need for:

- multi-agent orchestration;
- mandatory RAG;
- vector infrastructure;
- persistent personalized memory;
- browser automation;
- code interpretation;
- Kubernetes;
- Kafka;
- Redis;
- enterprise multi-tenancy;
- multi-region deployment.

A future capability must trace to:

- a validated requirement;
- an observed limitation;
- a material risk;
- a measured bottleneck;
- a controlled experiment;
- or an accepted Reliora decision.

---

# 31. Current Product-Level Conclusion

Current evidence supports the following bounded position:

> Reliora remains a credible production-oriented reference implementation for studying and demonstrating safe AI-assisted support with deterministic control, retry-safe side effects, human fallback, evaluation, and operational evidence.

Current evidence does not establish that:

- a real retailer should buy Reliora;
- Reliora should replace an incumbent support platform;
- Reliora is cheaper than a commercial SaaS product;
- Reliora improves real customer outcomes;
- Reliora creates positive real-world ROI.

The product therefore remains under the existing `NARROW` decision.

The correct next step is evidence promotion, not scope expansion.

---

# 32. M1.3 Decision Record

**Decision:** Retain all seven alternatives as valid comparison paths.

**Current working hypothesis:** The Reliora hybrid is worth continuing as a bounded reference implementation because it directly tests the reliability-and-control thesis.

**Not established:** That the hybrid is the best commercial solution for a real retailer.

**Simplest-alternative rule:** Prefer a simpler alternative whenever it satisfies the validated requirement with lower proportional burden.

**Reassessment:** Re-run the Problem-Buyer Evidence Gate when customer, buyer, incumbent, technical, operational, or economic evidence materially changes.

---

# 33. M1 Exit Assessment

The M1 product-lifecycle repair required Reliora to establish:

1. a retrospective discovery brief;
2. explicit separation of known facts, industry evidence, assumptions, buyer hypotheses, and open questions;
3. a formal Problem-Buyer Evidence Gate;
4. explicit `CONTINUE / NARROW / PIVOT / STOP / DEFER` rules;
5. a current gate decision;
6. a product-level alternatives analysis;
7. a measurable value hypothesis.

With this document accepted, those lifecycle controls are now explicitly represented.

The remaining evidence gaps are not documentation gaps.

They are evidence-generation tasks.

---

# 34. M1 Exit Condition

M1 is complete when:

- the discovery brief is accepted;
- the Problem-Buyer Evidence Gate is present in the Product Constitution;
- the current gate outcome is explicit;
- alternatives include simpler, incumbent, and no-change paths;
- the current solution is not declared superior without evidence;
- value is expressed through measurable hypotheses rather than invented ROI;
- metric boundaries preserve the existing Metric Dictionary;
- synthetic economics remain synthetic;
- the next experiments are evidence-seeking rather than feature-seeking.

Current lifecycle position:

```text
M1 PRODUCT-LIFECYCLE REPAIR     READY FOR FINAL REVIEW
CURRENT PRODUCT GATE            NARROW
BROAD FEATURE EXPANSION         NOT AUTHORIZED
NEXT MAJOR STAGE                M2 - ADR-017 TRUSTED IDENTITY EXPERIMENT
```

If M2 cannot run because no valid AWS target environment is available, the blocker must remain explicit rather than being bypassed through architecture expansion.
