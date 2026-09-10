# Reliora Recording Evidence Ledger

**Purpose:** Track portfolio-worthy recording opportunities during Reliora implementation so high-value evidence is captured while cloud resources and runtime states exist.

**Status:** Living document
**Established:** 2026-09-03

## Recording Priority

- **HIGH** — Capture whenever practical. Strong recruiter/interview evidence of architecture, reliability, AI/ML evaluation, deployment, observability, failure handling, or measurable engineering outcomes.
- **MEDIUM** — Capture when inexpensive. Useful supporting evidence or educational content, but not essential to the main recruiter story.
- **LOW** — Do not interrupt engineering work to record unless specifically useful for a tutorial.

## Capture Rules

For every HIGH or MEDIUM recording opportunity, record:
- phase and capability;
- business/engineering question being proved;
- exact screen/terminal state;
- expected duration;
- secrets/account information to hide;
- evidence or metric to preserve;
- suggested raw filename;
- whether the clip is submission evidence, technical evidence, recruiter evidence, or educational evidence.

Keep raw masters. Add narration, zooms, blur, captions, and face-camera presentation later.

Never intentionally expose passwords, MFA codes, access keys, session tokens, authentication QR codes or TOTP secrets, private customer data, or unnecessary AWS account identifiers.

AWS account IDs/ARNs are not passwords, but mask or crop them in public portfolio footage when they are not needed.

## Captured / In Progress

| ID | Phase | Evidence | ROI | Audience | Status | Notes |
|---|---|---|---|---|---|---|
| REC-001 | Cloud 0 / FinOps | AWS Budgets creation and configuration | MEDIUM | Recruiter + educational | CAPTURED | $20 monthly recurring cost budget; 50% actual, 80% forecasted, 100% actual alerts. Blur/crop account identifiers. |
| REC-002 | Cloud 0 / Account security | Root and IAM MFA setup | LOW recruiter / MEDIUM educational | Educational | OPTIONAL / largely completed | Useful learning evidence, but not central to Reliora's product story. Never expose QR/TOTP secrets. |
| REC-003 | Cloud 0 / Local AWS authentication | Temporary CLI authentication + caller identity verification | MEDIUM | Technical + educational | NEXT | Show secure local-development workflow. Mask account ID/ARN if published. |

## Planned High-ROI Evidence

| ID | Phase | Evidence | ROI | Why it matters |
|---|---|---|---|---|
| REC-010 | IaC | Terraform validate/plan/apply of Reliora cloud core | HIGH | Proves reproducible infrastructure rather than click-only deployment. |
| REC-011 | Backend | Lambda → DynamoDB authoritative ticket creation | HIGH | Proves real side effect and backend truth. |
| REC-012 | Reliability | Matching retry returns same ticket without duplicate execution | HIGH | Core Reliora differentiator: idempotent business action. |
| REC-013 | Reliability | Same operation ID + changed payload produces conflict | HIGH | Demonstrates deterministic safety under retry misuse. |
| REC-014 | Agent integration | AgentCore/Gateway invokes controlled ticket tool | HIGH | Proves managed agent-to-business-system integration. |
| REC-015 | Product behaviour | Multi-turn bug collection before tool authorization | HIGH | Shows AI proposal separated from deterministic authorization. |
| REC-016 | Grounding | Supported FAQ answer vs unsupported structured handoff | HIGH | Proves controlled knowledge behaviour and human escalation. |
| REC-017 | Observability | One request reconstructed through correlated CloudWatch/AgentCore evidence | HIGH | Strong Solutions Architect / production-operations signal. |
| REC-018 | Failure engineering | Controlled dependency failure without fabricated success | HIGH | Proves failure is intentionally designed, not ignored. |
| REC-019 | Evaluation | Bedrock evaluation + deterministic regression evidence | HIGH | Demonstrates LLMOps/evaluation maturity beyond a chatbot demo. |
| REC-020 | CI/CD | Deliberately unsafe change blocked by quality/regression gate | HIGH | Strong software/ML release-engineering evidence. |
| REC-021 | FinOps | Measured latency/token/tool/cost evidence | HIGH | Shows cost as an architecture dimension. |
| REC-022 | Deployment | Deploy → verify → evidence → destroy sequence | HIGH | Proves reproducibility and cost governance. |
| REC-023 | Product UX | Reference storefront → support → confirmed backend outcome | HIGH | Converts infrastructure into a believable commercial product demonstration. |
| REC-024 | Operator UX | Request Explorer / evaluation / operational evidence | HIGH | Shows why a business/operator would pay for the reliability layer. |

## Planned Medium-ROI Evidence

| ID | Phase | Evidence | ROI | Why it matters |
|---|---|---|---|---|
| REC-030 | AWS setup | CLI profile/region verification | MEDIUM | Shows disciplined local cloud setup. |
| REC-031 | IaC | Terraform init and formatting/validation | MEDIUM | Educational IaC workflow; recruiter value is lower than plan/apply/evidence. |
| REC-032 | Security | Gitleaks and Checkov clean run | MEDIUM | Useful supporting security evidence. |
| REC-033 | Operations | Budget/alert confirmation | MEDIUM | Supports FinOps story. |
| REC-034 | Teardown | Resource inventory after destroy | MEDIUM-HIGH | Confirms resources were actually removed and cost lifecycle is controlled. |

## Recording Decision Rule

Before recording, ask whether the moment proves a difficult-to-recreate cloud/runtime fact, demonstrates a Reliora differentiator, shows a measurable engineering outcome, matters to a recruiter/interviewer/reviewer/technical buyer, or would be expensive to reconstruct after teardown.

If strongly yes, mark **RECORD THIS — HIGH PORTFOLIO ROI** and capture it before proceeding.
