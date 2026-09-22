# Source map and reading authority

This index maps existing sources; it does not replace them. Follow the source precedence in the [constitution](../product/reliora-product-constitution.md): official P1 submission requirements, constitution, North Star, Reliora-specific sources, portfolio standard, then general engineering knowledge. Later source evidence updates dated status; it does not silently overrule an accepted governing requirement.

## Repository sources

| Subject | Canonical source | Interpretation |
|---|---|---|
| Current continuation | [CURRENT_STATE.md](CURRENT_STATE.md), [manifest](VERIFICATION_MANIFEST.json), actual Git HEAD | Dated status and evidence boundaries; verify freshness. |
| Product rules | [Constitution](../product/reliora-product-constitution.md) | Newer than the attached version because it includes M1 gate work. |
| North Star | [RELIORA-PRODUCT-NORTH-STAR.md](../../RELIORA-PRODUCT-NORTH-STAR.md) | Copied from the supplied North Star with content preserved; provenance below. |
| Product decision | [Discovery](../discovery/customer-discovery-brief.md), [business case](../business/business-case.md) | M1 complete, NARROW; buyer/value hypotheses remain unproven. |
| Requirements | [Functional](../requirements/functional-requirements.md), [non-functional](../requirements/non-functional-requirements.md) | Existing requirement identifiers govern acceptance. |
| Architecture | [Logical architecture](../architecture/logical-architecture.md), [decision journal](../architecture/decision-journal.md), [ADR index](../architecture/adr/README.md) | Distinguish proposed, accepted, implemented, and verified. |
| Identity blocker | [ADR-017](../architecture/adr/ADR-017-trusted-execution-identity.md), [AWS entry gate](../../evidence/adr017-target-environment-entry-gate-2026-09-18.md) | PROPOSED; authentication blocked the experiment. |
| Policy/security | [Autonomy](../governance/autonomy-policy.md), [threat model](../security/threat-model.md), [privacy](../privacy/data-lifecycle.md) | Requirements and scoped controls; not full cloud verification. |
| Security evidence | [Security scan baseline](../security/security-scan-baseline.md) | September 8 baseline and September 22 user-reported fresh scans; 12 Checkov findings remain. |
| Evaluation | [Evaluation guide](../../evals/README.md), [contract](../../evals/behavioural-evaluation-contract.md) | Fixture scope, result interpretation, and limitations. |
| Evidence maturity | [Register](../../evidence/evidence-maturity-register.md), [September 17 baseline](../../evidence/post-audit-engineering-baseline-2026-09-17.md) | Historical records, not automatically current test results. |
| Completion sequence | [Mitigation plan](../audit/RELIORA_MITIGATION_PLAN.md), [NEXT_STEPS](NEXT_STEPS.md) | Existing gates with current completion/dependency overlay. |
| Historical audit | [September 16 audit](../audit/RELIORA_PRODUCT_LIFECYCLE_AND_ARCHITECTURE_AUDIT.md) | Preserve original observations; do not restart completed M1 work. |
| Stage-1 origin | [Baseline manifest](../baseline/stage1-baseline-manifest.md) | Original submitted project provenance and known defects. |
| Operations | [Diagnostic playbook](../operations/diagnostic-playbook.md), [failure analysis](../operations/failure-mode-analysis.md) | Operational reasoning; recovery/runtime evidence still requires completion. |

## Imported North Star

Source attachment: `RELIORA-PRODUCT-NORTH-STAR(1).md`, supplied in the handover conversation. The root `RELIORA-PRODUCT-NORTH-STAR.md` preserves its source content. The verification manifest records its source SHA-256. Its deadline-related sequencing is inherited historical context; consult CURRENT_STATE for actual current blockers. No new deadline, architecture, or scope is adopted by copying the source.

## Supporting external attachments

These supplied sources are not yet bundled by this documentation commit. Include them with a complete cross-LLM transfer, or deliberately version them under an appropriate reference directory after provenance/content review. Their filenames identify the attachments, not existing repository paths.

| Supplied source | Role |
|---|---|
| `Project-Customer Support Chatbot with Amazon Bedrock AgentCore.txt` | Official P1 specification supplied by the user; mandatory submission authority. |
| `AgentCore-Project-Runbook_1.pdf`, `Useful-github-links-for-this-project.txt` | Implementation/submission support. |
| `How-to-1.1.txt`, `How-to-1.2.txt` | Secondary observations; do not override the official specification. |
| `deep-research-report for P1-S2.md` | Research rationale; verify current external technical assumptions before new implementation. |
| `portfolio-product-engineering-standard-v1.1(1).md` | Shared engineering quality; does not import other products' architecture. |
| `universal-international-production-ds-ml-ai-solutions-architecture-charter-v1.1(1).md` | Cross-project production guidance, applied proportionally to Reliora. |
| `Universal Forward-Deployed AI-ML Solutions Architecture Charter.md` | Customer discovery, realistic constraints, outcomes, feedback, and adaptation discipline. |
| `Reliora-End-to-End-Solutions-Architect-Delivery-Blueprint-v1.0(1).md` | Delivery and portfolio/interview guidance. |
| Attached constitution, decision journal, evidence ledger, audit, and mitigation plan | Historical/source copies; compare versions before replacing newer repository counterparts. |

The separate [aws-agentic-ai-learning-ledger](https://github.com/aaronmalunga/aws-agentic-ai-learning-ledger) contains transferable lessons, not the product's implementation authority.

## Unresolved context and limitations

The receiving LLM should not infer customer evidence, current credentials, billing resolution, local tool versions, or completion of a capability from its branch name. The initial downloadable handover assessment predates the merged governance corrections and billing diagnosis; use this repository checkpoint for subsequent continuation status.
