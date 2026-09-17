# RELIORA MITIGATION PLAN

**Document type:** Post-audit remediation plan
**Product:** Reliora — AI Customer-Support Reliability and Control Platform for Online Commerce
**Date:** 2026-09-16
**Depends on:** `RELIORA_PRODUCT_LIFECYCLE_AND_ARCHITECTURE_AUDIT.md`
**Implementation rule:** Smallest justified remediation first
**Architecture rule:** Preserve current Reliora architecture unless evidence justifies change
**Code-change status at plan creation:** No remediation code changes made yet

---

# 1. Purpose

This plan translates the completed Reliora Product Lifecycle & Architecture Audit into an ordered remediation programme.

It does **not** attempt to make every universal control “green.”

The objective is to:

1. close correctness and architecture blockers;
2. restore missing product-lifecycle gates;
3. promote evidence from local to target-environment maturity;
4. complete only the operability controls Reliora independently needs;
5. preserve existing strong architecture;
6. defer capabilities that have not earned their place.

The plan uses the required priority model:

```text
P0 — correctness / security / architectural blockers
P1 — implementation-gate deficiencies
P2 — evidence / reliability / operability gaps
P3 — documentation / maturity improvements
DEFERRED — not justified yet
NO CHANGE — existing Reliora approach is adequate
```

---

# 2. Current Starting Point

Use this as the remediation baseline:

```text
Historical local-safety baseline
main @ cc02e5838dda9d1ded121008d86a04526e6e273e

Parent AWS architecture line
feat/aws-infrastructure @ da0d028a1b41aa1f2a7ccf084b49211c25d3fc1e

Current implementation snapshot
feat/failure-telemetry-emission @ 88c13baa8ae5d47910acf39ba879cf066815a364

Outstanding governance branch
docs/security-privacy-hardening

Learning Ledger
aws-agentic-ai-learning-ledger/main
@ ad88d39fb686efe677d18f6a917bc19379d9f409
```

Do not use `main` alone as the representation of current Reliora.

---

# 3. Governing Dependencies

The remediation order is constrained by four dependencies.

## Dependency A — Product reasoning before more product expansion

Before adding additional product capabilities:

```text
discovery
→ problem/buyer gate
→ alternatives/value hypothesis
→ continue/narrow/pivot/stop decision
```

## Dependency B — Trusted identity before end-to-end side-effect claims

Before depending on the real AgentCore/Gateway path for retry-safe ticket creation:

```text
ADR-017 experiment
→ trusted operation identity demonstrated
→ live idempotency experiment
→ end-to-end claim
```

## Dependency C — Evidence before maturity claims

Before claiming cloud verification:

```text
local evidence
→ target environment
→ E4 integration
→ E5 controlled experiment
→ E6 end-to-end deployment
```

## Dependency D — Operability before pilot claims

Before a real pilot:

```text
reconstruction
→ security/privacy controls
→ recovery/rollback
→ operational ownership
→ pilot criteria
```

---

# 4. P0 — Correctness / Security / Architectural Blockers

## P0-001 — Resolve trusted logical-operation identity

**Source gap:** `GAP-ARCH-001`
**Related decision:** ADR-017
**Current status:** `UNPROVEN`

### Why this is P0

Reliora's strongest reliability claim depends on:

```text
one logical operation
→ stable operation_id
→ retries preserve operation_id
→ no duplicate ticket
```

The current Lambda adapter expects trusted identifiers from `Lambda ClientContext`, but the real AgentCore/Gateway path has not demonstrated that those values reach Lambda with the required semantics.

If this assumption is wrong, the local idempotency architecture may still be internally correct while the real transport fails to preserve the logical operation identity needed to use it.

### Smallest experiment

Do not redesign the runtime.

Create one target-environment experiment answering only:

1. Where does `request_id` originate?
2. Where does `session_id` originate?
3. Where does `operation_id` originate?
4. Can the model override any of them?
5. Does a matching retry retain the same `operation_id`?
6. Can the retry have a new `request_id`?
7. Does a second logical business action receive a new `operation_id`?

### Pass condition

ADR-017 can move from `PROPOSED` to `ACCEPTED` only if the required semantics are demonstrated.

### Failure condition

If the current transport cannot preserve trusted logical-operation identity:

```text
do not hide the result
→ classify the mechanism as disproven
→ compare the smallest alternatives
→ make a new ADR
```

### Explicit non-response

Do not automatically introduce:

- Strands;
- MCP redesign;
- a new agent framework;
- a new database;
- a new orchestration platform.

A failed experiment authorizes investigation, not architecture expansion.

### Evidence to retain

- exact deployed commit;
- exact runtime configuration;
- captured IDs at each boundary;
- retry trace;
- new-operation trace;
- DynamoDB result;
- experiment conclusion.

---

# 5. P1 — Implementation-Gate Deficiencies

## P1-001 — Freeze a fresh post-audit engineering baseline

**Source gap:** `GAP-EVID-001`

Before implementation resumes, establish the new known-good local baseline.

### Verify

```text
branch
commit
working tree
pytest
Ruff
mypy
deterministic evaluation
Terraform fmt
Terraform validate
```

Where available, also record:

```text
Lambda package verification
security scans
```

### Output

Create or update a baseline artifact containing:

- commit SHA;
- branch;
- date;
- test result;
- lint result;
- type-check result;
- evaluator result;
- Terraform validation result;
- known blockers.

### Reason

The evidence register currently reflects an earlier snapshot and the latest telemetry work has moved ahead.

---

## P1-002 — Retrospective Reliora discovery brief

**Source gap:** `GAP-LC-001`

This is a **retrospective lifecycle repair**, not rewritten history.

### Create

```text
docs/discovery/customer-discovery-brief.md
```

### It must explicitly distinguish

```text
KNOWN FROM P1 / CURRENT IMPLEMENTATION
INDUSTRY-RESEARCH EVIDENCE
SYNTHETIC CUSTOMER ASSUMPTION
UNVALIDATED BUYER HYPOTHESIS
OPEN QUESTION
```

### Required content

- representative retailer profile;
- actors;
- buyer/economic-owner hypotheses;
- current support workflow;
- current incumbent alternatives;
- current failure/retry process;
- current observability process;
- current human escalation;
- data constraints;
- security/privacy constraints;
- staffing/operational constraints;
- business pain;
- frequency/severity assumptions;
- baseline measures that are unknown;
- desired outcomes;
- open validation questions.

### Guardrail

Do not create fictional customer interviews or invented dollar savings.

---

## P1-003 — Problem–buyer evidence gate and kill/pivot/narrow rules

**Source gap:** `GAP-LC-002`

Add a small governance section rather than a new framework.

### Decision outcomes

Every future major product investment should end in one of:

```text
CONTINUE
NARROW
PIVOT
STOP
DEFER
```

### Example conditions

**Continue** when:
- problem remains credible;
- target buyer plausibly owns the pain;
- Reliora provides a differentiated control/evidence story;
- the required architecture remains economically proportional.

**Narrow** when:
- only a subset of workflows has strong value/evidence;
- additional automation increases risk faster than value;
- support scope is broader than evidence justifies.

**Pivot** when:
- the strongest need is reliability tooling rather than customer-facing automation;
- the buyer differs materially from the current hypothesis;
- a different workflow has stronger evidence.

**Stop** when:
- the problem is not material;
- existing alternatives solve it sufficiently;
- customer/buyer evidence contradicts the thesis;
- required operational cost/risk is disproportionate;
- AI adds no meaningful value over simpler software.

### Where to place it

Prefer an amendment to an existing governing product document rather than creating document symmetry for its own sake.

---

## P1-004 — Product-level alternatives and measurable value hypothesis

**Source gap:** `GAP-LC-003`

### Compare at least

1. status quo/manual support;
2. conventional chatbot/helpdesk automation;
3. deterministic workflow/rules;
4. current Reliora hybrid;
5. commercial SaaS alternative where relevant.

### Compare on

- reliability;
- side-effect risk;
- human effort;
- integration burden;
- evaluation burden;
- observability;
- cost;
- adaptability;
- operational complexity.

### Value hypothesis

Define measurable but currently unproven product metrics such as:

- successful eligible resolution;
- false automation;
- unnecessary handoff;
- duplicate logical ticket rate;
- ticket completeness;
- customer repetition at handoff;
- time to diagnose;
- cost per successful eligible resolution.

### Evidence rule

Synthetic financial assumptions must remain labelled synthetic.

---

## P1-005 — Minimum structured handoff implementation

**Source gap:** `GAP-DOM-001`

Reliora already requires structured handoff.

Do not build a full contact-center platform.

### Minimum typed contract

Use only fields that current Reliora scenarios need, for example:

```text
handoff_reason
intent
safe_summary
information_already_collected
attempted_action
failure_category
recommended_destination
request_id
session_id
operation_id where relevant
application/deployment version where available
```

### First required scenarios

1. unsupported PLATFORM question;
2. explicit human request;
3. unconfirmed side-effect outcome;
4. backend failure after bounded retry policy.

### Tests

- schema validation;
- data minimization;
- no hidden reasoning/system prompt;
- preserves relevant collected context;
- routes correct reason.

---

## P1-006 — Complete the behavioural release gate

**Source gap:** `GAP-CI-001`

Extend the existing GitHub Actions workflow.

Do not create a second CI system.

### Current gate already covers

- locked dependency install;
- Ruff;
- mypy;
- pytest;
- Lambda artifact build/verification;
- Terraform fmt/init/validate.

### Add only justified controls

- deterministic evaluator regression;
- Stage-1 reproduction/regression where appropriate;
- Gitleaks;
- Checkov or equivalent IaC scan;
- generated release/evidence metadata if practical.

### Required demonstration

Create one deliberate unsafe test change in a controlled branch and show:

```text
unsafe behavioural change
→ deterministic gate fails
→ release blocked
```

Then revert/fix it.

The demonstration should not be merged as broken product code.

---

## P1-007 — Reconcile Git branch/source fragmentation

**Source gap:** `GAP-REPO-001`

Do this after the audit artifacts are stable.

### Required sequence

1. determine dependency order;
2. inspect PR #2 privacy/security changes against current branch;
3. rebase/cherry-pick/port only still-valid changes;
4. avoid silently overwriting newer threat-model work;
5. integrate telemetry branch through normal review;
6. run the full gate;
7. update evidence snapshot;
8. merge toward the intended parent branch.

### Rule

Do not mix branch cleanup with unrelated architecture redesign.

---

## P1-008 — Promote target-environment evidence

**Source gap:** `GAP-AWS-001`

When a valid AWS account is available:

### Promote in order

```text
Terraform plan
→ apply
→ Lambda/DynamoDB verification
→ identity experiment
→ Gateway verification
→ AgentCore verification
→ end-to-end workflow
```

### Evidence maturity

Promote claim by claim.

Do not upgrade the whole project from E2/E3 to E6 because one integration succeeds.

---

# 6. P2 — Evidence / Reliability / Operability Gaps

## P2-001 — Wire the existing failure telemetry path

**Source gap:** `GAP-OBS-001`

The telemetry abstraction and adapter emission already exist.

The Lambda composition currently does not provide a telemetry sink.

### Required action

Use the smallest approved sink compatible with the current AWS observability design.

Do not introduce a separate observability stack unless CloudWatch/AgentCore evidence proves insufficient.

### Verify

- AccessDenied emits authorization failure;
- backend failure remains the primary error;
- telemetry failure does not mask the primary error;
- no unnecessary customer payload enters telemetry.

---

## P2-002 — Prove one end-to-end request reconstruction

### Required scenario

Choose one high-value request, preferably:

```text
bug report
→ authorization
→ operation identity
→ ticket execution
→ persistence
→ final outcome
```

and one controlled failure.

### Operator should reconstruct

- request;
- session;
- logical operation;
- route/workflow;
- authorization;
- persistence result;
- reconciliation state;
- failure category;
- version/deployment context;
- timing where available.

### Guardrail

Do not log hidden chain-of-thought.

---

## P2-003 — Reconcile privacy/data-lifecycle governance

**Source gap:** `GAP-PRIV-001`

The stronger data-lifecycle policy already exists on the diverged security/privacy branch.

### Required action

Reconcile it with:

- current telemetry contract;
- current persistence schema;
- current evidence stores;
- current Terraform;
- current threat model.

### Do not

- create additional stores;
- add retention technology merely because the policy mentions retention;
- claim provider deletion semantics until verified.

---

## P2-004 — Recovery / rollback / DR runbook

**Source gap:** `GAP-REC-001`

Create:

```text
docs/operations/recovery-and-dr.md
```

### Keep scope proportional

Cover:

- redeploy infrastructure from Terraform;
- restore/recreate application configuration;
- rollback to known validated application version;
- restore prompt/model/router/knowledge configuration;
- DynamoDB recovery approach appropriate to the demo scope;
- preserve evidence independent of live resources;
- dependency-safe teardown/redeploy;
- declared RTO/RPO as TARGET/ASSUMPTION only if business evidence exists.

### Required later experiment

One controlled rollback or redeploy.

---

## P2-005 — Security-assurance automation

**Source gap:** `GAP-SEC-001`

Add lightweight checks that correspond to actual risk.

### Minimum

- secret scan;
- IaC scan;
- dependency review if practical;
- prompt-injection/forbidden-tool deterministic cases.

### Not required merely for appearance

- full penetration test before a real exposed pilot;
- enterprise SOC tooling;
- third-party SIEM;
- WAF before a public endpoint exists.

---

## P2-006 — Deployment provenance

Create enough version provenance to answer:

> Which product configuration produced this observed outcome?

Where applicable track:

- Git commit;
- application artifact;
- Terraform/infrastructure revision;
- model ID/configuration;
- prompt version;
- router version;
- knowledge version;
- evaluation dataset version.

Do not invent versions for components not yet implemented.

---

## P2-007 — Controlled cloud reliability experiments

After the E4 integration boundary is stable, run:

1. matching retry;
2. conflicting operation;
3. timeout/ambiguous outcome;
4. access denied;
5. incomplete durable state where safely reproducible;
6. telemetry failure if practical;
7. dependency failure/handoff.

Each experiment must have:

```text
control
→ injection
→ observation
→ classification
→ decision
→ retained evidence
```

---

# 7. P3 — Documentation / Maturity Improvements

## P3-001 — Refresh dated status snapshots

Do not rewrite historical sections.

Instead add current-state notes to:

- README;
- Product Constitution;
- Decision Journal;
- Evidence register.

Historical statements such as:

```text
164 tests
Phase 0
AWS Cloud 0 next
```

should remain identifiable as dated snapshots.

---

## P3-002 — Canonicalize the Product North Star

The North Star is a governing project source but is not in the current audited GitHub tree.

Options:

1. place the current canonical North Star in the repository; or
2. explicitly document the external governing-source location.

Preferred: keep the governing product source available beside the Constitution if that does not create version ambiguity.

---

## P3-003 — Operational ownership and handoff

Before a real pilot, define:

- product owner;
- service owner;
- security/privacy owner;
- evaluation owner;
- incident owner;
- cost owner;
- handoff/escalation responsibilities;
- documentation/runbook owner.

Do not over-formalize this for a single-developer local project before it is operationally useful.

---

## P3-004 — Learning Ledger synchronization

Add reusable lessons only after the current architecture settles.

High-value new lessons:

- ambiguous mutation outcomes;
- timeout-after-write reconciliation;
- incomplete durable state → `UNCONFIRMED`;
- telemetry failure must not mask primary failure;
- failure taxonomy design;
- why operational telemetry is not business authority.

Do not duplicate implementation files.

---

## P3-005 — Claim-evidence ledger

If a separate claim ledger is still useful after reviewing the evidence register, keep it small.

Map public claims such as:

```text
retry-safe
idempotent
observable
deployable
cost-aware
security-controlled
```

to exact evidence and limitations.

If the evidence maturity register already provides sufficient traceability, extend it instead of creating another document.

---

# 8. DEFERRED — Not Justified Yet

The following are deliberately deferred.

## D-001 — Real beta/pilot adoption evidence

Reason:

No real customer/pilot currently exists.

Action:

Define pilot success criteria now; gather evidence only from a genuine future pilot.

---

## D-002 — Numerical SLOs and error budgets

Reason:

Reliora correctly requires relevant target-environment baseline measurement first.

Action:

No change until E4/E5 evidence exists and a business requirement can justify targets.

---

## D-003 — Enterprise multi-tenancy

Reason:

Explicitly outside current bounded product.

---

## D-004 — Multi-region deployment

Reason:

No current availability/residency requirement justifies it.

---

## D-005 — Mandatory RAG / vector database

Reason:

Current approved knowledge scope does not demonstrate the need.

---

## D-006 — Multi-agent architecture

Reason:

No independent Reliora requirement.

---

## D-007 — Kubernetes / EKS

Reason:

Current managed/serverless architecture does not demonstrate an orchestration problem.

---

## D-008 — Kafka / MSK / Redis

Reason:

No streaming/cache requirement exists.

---

## D-009 — Additional ticket-system integrations

Reason:

One clean adapter boundary proves adaptability better than shallow integrations with many vendors.

---

## D-010 — Advanced compliance claims

Reason:

No legal assessment or external assurance supports claims of compliance/certification.

---

# 9. NO CHANGE — Existing Reliora Approach Is Adequate

Preserve:

1. frozen Stage-1 provenance;
2. current product identity;
3. product-first technology rule;
4. deterministic authorization;
5. request/session/operation identity separation;
6. authorization before execution;
7. idempotency fingerprint/admission semantics;
8. matching replay and conflict;
9. backend-confirmed success;
10. explicit `UNCONFIRMED`;
11. DynamoDB conditional transactional persistence;
12. strongly consistent reconciliation;
13. small approved knowledge source;
14. no mandatory RAG;
15. provider boundary;
16. AWS-first but not AWS-defined architecture;
17. deterministic vs generative evaluation split;
18. held-out-test discipline;
19. evidence classes;
20. E0-E9 maturity;
21. metric-boundary discipline;
22. claim-bounded language;
23. no arbitrary SLOs;
24. Learning Ledger separation;
25. best-effort telemetry not masking primary errors.

---

# 10. Smallest Sensible Remediation Order

## Stage M0 — Baseline and audit preservation

1. commit/store the audit and mitigation artifacts in the appropriate documentation location;
2. capture current Git SHA/branch state;
3. run local quality/evaluation baseline;
4. update the evidence snapshot.

**Exit condition:** current implementation state is reproducibly known.

---

## Stage M1 — Product-lifecycle repair

1. retrospective discovery brief;
2. problem-buyer gate;
3. kill/pivot/narrow conditions;
4. product alternatives;
5. measurable value hypothesis.

**Exit condition:** future engineering investment can be justified without starting from AWS services.

---

## Stage M2 — Architecture blocker experiment

1. deploy smallest environment required;
2. run ADR-017 identity experiment;
3. accept/reject current mechanism;
4. update ADR;
5. only if needed, compare replacement mechanisms.

**Exit condition:** logical operation identity is proven or a replacement decision exists.

---

## Stage M3 — Complete core workflow contracts

1. structured handoff contract;
2. handoff tests;
3. relevant product path wiring.

**Exit condition:** unsupported/failure paths are first-class product outcomes.

---

## Stage M4 — Release gate

1. deterministic eval in CI;
2. security scans;
3. evidence metadata;
4. deliberate unsafe-change block demonstration.

**Exit condition:** code cannot be promoted solely because unit tests and linting pass.

---

## Stage M5 — Operability

1. wire telemetry sink;
2. request reconstruction;
3. privacy-policy reconciliation;
4. recovery/rollback runbook;
5. deployment provenance.

**Exit condition:** one important request/failure can be reconstructed and restored safely.

---

## Stage M6 — Cloud evidence promotion

1. Lambda/DynamoDB E4;
2. retry/conflict E5;
3. AgentCore/Gateway E4;
4. full workflow E6;
5. failure experiments E5;
6. cost/latency E5;
7. deploy/destroy evidence.

**Exit condition:** cloud-backed claims are supported at their stated maturity.

---

## Stage M7 — Product experience

1. reference storefront;
2. embedded support;
3. minimum justified operator view;
4. local/cloud evidence-mode clarity;
5. Playwright canonical journeys where appropriate.

**Exit condition:** a reviewer can understand the product before opening AWS Console.

---

## Stage M8 — Operational handoff and portfolio release

1. adaptation/configuration guide;
2. operational ownership;
3. troubleshoot/recover/destroy;
4. claim-evidence review;
5. final architecture diagrams;
6. demo;
7. case study;
8. Learning Ledger update.

**Exit condition:** another competent engineer can understand, deploy, verify, operate, and explain the reference implementation within its stated evidence limits.

---

# 11. Dependency Graph

```text
Fresh baseline
    |
    +--> Discovery / buyer gate
    |       |
    |       +--> Alternatives / value hypothesis
    |               |
    |               +--> Continue / narrow / pivot / stop
    |
    +--> ADR-017 identity experiment
            |
            +--> live idempotency verification
                    |
                    +--> AgentCore/Gateway E2E
                            |
                            +--> observability
                            +--> cloud failure experiments
                            +--> cost/latency
                            +--> rollback/recovery

Structured handoff
    |
    +--> failure/human-path E2E

Release gate
    |
    +--> safer cloud promotion

Privacy/security reconciliation
    |
    +--> pilot readiness

All of the above
    |
    +--> product UX
    +--> operational handoff
    +--> portfolio release
```

---

# 12. Work That Must Not Start Yet

Until P0/P1 gates are addressed, do not prioritize:

- a large frontend build;
- operator-dashboard breadth;
- multiple vendor integrations;
- RAG;
- additional agents;
- Kubernetes;
- streaming infrastructure;
- new databases;
- multi-cloud wrappers;
- performance optimization beyond measured bottlenecks.

The next stage is not “add more.”

It is:

> **validate the product reasoning, resolve the trusted-identity blocker, then promote the strongest local engineering into target-environment evidence.**

---

# 13. Completion Criteria for the Mitigation Programme

The mitigation is complete when:

## Product lifecycle

- discovery evidence is explicit;
- buyer/problem assumptions are explicit;
- continuation/kill rules exist;
- solution alternatives and value hypothesis are documented.

## Architecture

- ADR-017 is accepted or replaced by an evidence-backed alternative;
- current side-effect architecture remains coherent;
- no unjustified technologies were introduced.

## Product behaviour

- structured handoff exists;
- safe side-effect semantics remain intact.

## Release

- deterministic evaluation is part of the release gate;
- security checks are appropriately automated.

## Operations

- failure telemetry is wired;
- one request can be reconstructed;
- privacy/data lifecycle is canonical;
- recovery/rollback is documented and tested at the appropriate maturity.

## Evidence

- cloud claims are promoted only when E4-E6 evidence exists;
- no local evidence is presented as production evidence.

## Repository

- branch/source fragmentation is reconciled;
- governing artifacts are current and traceable.

## Learning

- latest reusable lessons are captured in the Learning Ledger after the architecture stabilizes.

---

# Final Mitigation Decision

The mitigation programme is intentionally **surgical**.

Reliora already contains significant correct architecture.

The objective is not to replace it.

The objective is to close the lifecycle and evidence gaps around it so that the final product can truthfully demonstrate:

```text
real problem framing
→ justified architecture
→ deterministic control
→ safe side effects
→ target-environment evidence
→ operational reconstructability
→ controlled release
→ recoverability
→ credible product experience
→ evidence-bounded claims
```

**Plan status:** READY FOR EXECUTION AFTER AUDIT REVIEW
