# Reliora Security Scan Baseline

## Purpose

This artifact records locally observed security-scanning evidence for Reliora.

It is an evidence record, not a replacement for:

- `threat-model.md`;
- the Product Constitution;
- non-functional requirements;
- architecture decisions.

The evidence principle is:

**Control → Scan/Test → Observation → Classification → Decision**

---

## Evidence Date

2026-09-08

---

## Repository Secret Scan

Tool:

`Gitleaks`

Scope:

Repository and Git history.

Observed result:

```text
Findings: 0
```

Evidence classification:

**LOCAL VERIFIED**

Interpretation:

No secret matching the Gitleaks rules used during the scan was identified in the
tested repository history.

This result describes the tested repository state only. It does not guarantee
that future commits cannot introduce secrets.

Remaining control:

```text
Automated CI secret scanning
→ PENDING
```

---

## Runtime Dependency Vulnerability Scan

Tool:

`pip-audit 2.10.1`

Input:

Runtime-only dependency requirements exported from the authoritative `uv.lock`.

Export characteristics:

```text
uv export
→ --frozen
→ --no-dev
→ --no-emit-project
→ requirements.txt
```

Observed result:

```text
No known vulnerabilities found
```

Evidence classification:

**LOCAL VERIFIED**

Interpretation:

No known vulnerability was reported for the resolved Reliora production
dependency set using the vulnerability data available to `pip-audit` at scan
time.

This is time-sensitive evidence and must be repeated before release.

---

## Terraform Infrastructure Scan

Tool:

`Checkov 3.3.16`

Scope:

```text
infra/terraform
```

Framework:

```text
terraform
```

Observed result:

```text
Passed checks: 36
Failed checks: 12
Skipped checks: 0
```

Evidence classification:

**EXECUTED — FINDINGS CLASSIFIED, REMEDIATION PENDING**

A failed Checkov policy is not automatically equivalent to an exploitable
security vulnerability.

Each finding must be evaluated against:

- Reliora requirements;
- the current development architecture;
- the threat model;
- privacy and retention decisions;
- operational requirements;
- production-readiness requirements.

---

## Checkov Finding Register

| Check | Resource / Area | Classification | Current Disposition |
|---|---|---|---|
| `CKV_AWS_28` | DynamoDB operations PITR | ACCEPTED DEV DEVIATION | Reconsider for production recovery requirements |
| `CKV_AWS_119` | DynamoDB operations customer-managed KMS | ACCEPTED DEV DEVIATION | Current dev design retains default managed encryption |
| `CKV_AWS_28` | DynamoDB tickets PITR | ACCEPTED DEV DEVIATION | Reconsider for production recovery requirements |
| `CKV_AWS_119` | DynamoDB tickets customer-managed KMS | ACCEPTED DEV DEVIATION | Current dev design retains default managed encryption |
| `CKV_AWS_272` | Lambda code signing | OPEN HARDENING GAP | Evaluate with deployment provenance and signing design |
| `CKV_AWS_116` | Lambda DLQ | CONDITIONAL / CLOUD VERIFICATION PENDING | Confirm actual Gateway-to-Lambda invocation semantics first |
| `CKV_AWS_173` | Lambda environment-variable customer-managed KMS | ACCEPTED DEV DEVIATION | Current variables are configuration identifiers, not application secrets |
| `CKV_AWS_115` | Lambda reserved concurrency | OPEN HARDENING GAP | Define an evidence-backed concurrency limit before implementation |
| `CKV_AWS_117` | Lambda VPC placement | NOT REQUIRED BY CURRENT ARCHITECTURE | Do not introduce VPC complexity solely for scanner compliance |
| `CKV_AWS_50` | Lambda X-Ray tracing | OPEN OBSERVABILITY GAP | Evaluate as part of observability implementation |
| `CKV_AWS_158` | CloudWatch log-group customer-managed KMS | ACCEPTED DEV DEVIATION | Current dev design retains managed encryption |
| `CKV_AWS_338` | CloudWatch minimum one-year retention | INTENTIONALLY REJECTED FOR DEV | Preserve explicit seven-day development retention |

---

## High-Value Follow-Up

The scan identified four areas requiring further architectural work or
verification.

### Lambda reserved concurrency

Relevant threat:

```text
T-009 — Unbounded Resource Consumption
```

Purpose:

- bound Lambda scaling;
- reduce denial-of-wallet exposure;
- protect downstream capacity.

Current state:

```text
OPEN HARDENING GAP
```

The value must be derived from workload, downstream capacity, and cost evidence.
It must not be chosen arbitrarily to satisfy a scanner.

---

### Lambda code signing

Relevant threat:

```text
T-014 — Software Supply-Chain or Deployment Artifact Compromise
```

Purpose:

- strengthen deployment provenance;
- restrict deployment to approved signed artifacts.

Current state:

```text
OPEN HARDENING GAP
```

Evaluation should occur with the deployment and release-provenance design.

---

### Lambda X-Ray tracing

Relevant area:

```text
observability
failure diagnosis
runtime evidence
```

Current state:

```text
OPEN OBSERVABILITY GAP
```

This should be considered during the observability architecture phase rather
than added only to satisfy Checkov.

---

### Lambda DLQ

Check:

```text
CKV_AWS_116
```

Current state:

```text
CONDITIONAL / CLOUD VERIFICATION PENDING
```

Disposition depends on the actual invocation model demonstrated by the deployed
Gateway-to-Lambda integration.

No suppression should be added until the invocation semantics are verified.

---

## NFR-SEC-005 Evidence State

Current security-scanning evidence:

```text
Repository and Git-history secret scanning
→ Gitleaks
→ LOCAL VERIFIED
→ 0 findings

Runtime dependency vulnerability scanning
→ pip-audit 2.10.1
→ LOCAL VERIFIED
→ no known vulnerabilities found

Terraform infrastructure scanning
→ Checkov 3.3.16
→ EXECUTED
→ 36 passed
→ 12 failed
→ 0 skipped
→ findings classified

Automated hosted CI enforcement
→ PENDING
→ currently blocked by external GitHub Actions workflow-registration failure
```

---

## Evidence Limitations

The current scan results are local observations.

They do not demonstrate:

- successful AWS deployment;
- runtime AWS authorization;
- actual Lambda concurrency behaviour;
- real Gateway-to-Lambda invocation semantics;
- deployed encryption configuration;
- cloud retention enforcement;
- successful hosted CI security enforcement.

Those claims require separate evidence.

---

## Scanner Governance Principle

Reliora does not optimize for a zero-warning scanner dashboard by blindly
implementing every generic policy.

The decision process is:

```text
scan
→ inspect
→ compare with requirements and architecture
→ classify
→ remediate genuine risk
→ justify intentional deviations
→ verify
→ preserve evidence
```

A suppression is acceptable only when its rationale is explicit and evidence
supports the decision.

---

## Current State

```text
Gitleaks repository/history scan         LOCAL VERIFIED — 0 FINDINGS
pip-audit runtime dependency scan        LOCAL VERIFIED — NO KNOWN VULNERABILITIES
Checkov Terraform scan                   EXECUTED — 36 PASS / 12 FAIL
Checkov findings                         CLASSIFIED
Security remediation                     PARTIAL / PENDING
CI security enforcement                  PENDING / EXTERNALLY BLOCKED
AWS security verification                PENDING
```

---

## Final Principle

Security scanning provides evidence for architectural decisions.

It does not replace architectural judgment.

**Scanner result → architectural analysis → explicit decision → verification**
