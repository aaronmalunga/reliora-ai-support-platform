# Reliora Evidence Maturity Register

**Project:** Reliora AI Support Platform
**Document type:** Evidence maturity register
**Established:** 2026-09-10
**Status:** ACTIVE

---

## 1. Purpose

This register records how mature Reliora's important evidence is relative to the environment and conditions in which it was produced.

Evidence maturity is separate from evidence classification.

For example:

```text
EXPERIMENTAL
```

describes the evidence class, while:

```text
E3 — Local Synthetic Measured
```

describes how far that evidence has progressed toward real target-environment or production conditions.

A higher maturity level requires stronger evidence.

Documentation changes alone do not increase evidence maturity.

---

## 2. Evidence Maturity Ladder

| Level | Meaning                                              |
| ----- | ---------------------------------------------------- |
| E0    | Design, requirement, target, or planned control only |
| E1    | Unit-level behaviour verified                        |
| E2    | Local integration behaviour verified                 |
| E3    | Local synthetic workload measured                    |
| E4    | Target/cloud environment integration verified        |
| E5    | Controlled target/cloud environment experiment       |
| E6    | End-to-end deployed system verified                  |
| E7    | Real beta or pilot behaviour observed                |
| E8    | Real production behaviour observed                   |
| E9    | Independent assurance or external verification       |

The level describes the strongest environment in which the specific claim has actually been demonstrated.

It does not describe how impressive, complex, or important the implementation is.

---

## 3. Current Evidence Register

| Evidence / capability                          | Current evidence                                                             | Evidence class / status         | Maturity                          | Claim boundary                                                                 |
| ---------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------- | --------------------------------- | ------------------------------------------------------------------------------ |
| Python automated test suite                    | 200 tests passing                                                            | Local verification              | E1                                | Demonstrates covered automated behaviours only                                 |
| Ruff quality gate                              | Ruff checks passing                                                          | Local verification              | E1                                | Static code-quality checks only                                                |
| mypy quality gate                              | No issues found in 30 source files                                           | Local verification              | E1                                | Static type checking of covered source only                                    |
| Deterministic evaluator regression             | Generated regression report under `evidence/generated/`                      | `EXPERIMENTAL`                  | E2                                | Demonstrates the covered deterministic evaluator contract locally              |
| Stage-1 reproduction evaluation                | Generated reproduction report under `evidence/generated/`                    | `EXPERIMENTAL`                  | E2                                | Demonstrates behaviour against the versioned reproduction dataset only         |
| Routing benchmark                              | Controlled routing benchmark and validation artifacts                        | `EXPERIMENTAL`                  | E3                                | Local controlled routing experiment only                                       |
| Routing held-out evaluation                    | Held-out routing evaluation artifact                                         | `EXPERIMENTAL`                  | E3                                | Generalization evidence within the held-out dataset only                       |
| Local routing performance                      | Local routing operational evidence                                           | `EXPERIMENTAL`                  | E3                                | Local routing inference only; excludes cloud/network/tool latency              |
| Local ticket-runtime performance               | `local-ticket-runtime-v1.json`; 100,000 measured requests                    | `EXPERIMENTAL`                  | E3                                | Local in-process `LambdaBugReportRuntime.handle` only                          |
| Local ticket-runtime failures                  | Zero observed failures in the 100,000-request synthetic benchmark            | `EXPERIMENTAL`                  | E3                                | Zero observed failures within that benchmark only; not production availability |
| Terraform formatting                           | Terraform source formatted successfully                                      | Local verification              | E1                                | Formatting only                                                                |
| Terraform initialization                       | Terraform provider initialization completed successfully                     | Local verification              | E2                                | Demonstrates local Terraform/provider initialization only                      |
| Terraform validation                           | Terraform configuration validated successfully                               | Local verification              | E2                                | Validates Terraform configuration locally; does not prove AWS deployability    |
| Terraform target-environment plan              | Cannot currently execute against a valid AWS target environment              | `BLOCKED`                       | Not reached                       | No cloud-plan claim may be made                                                |
| Terraform apply / cloud infrastructure         | No current active AWS target environment                                     | `BLOCKED`                       | Not reached                       | No deployed-infrastructure claim may be made                                   |
| Lambda-to-DynamoDB ticket execution            | Local adapter/runtime behaviour exists; live AWS path not yet verified       | PARTIAL / AWS `BLOCKED`         | E2 locally                        | Does not establish live Lambda/DynamoDB execution                              |
| Matching retry replay in AWS                   | Deterministic/local semantics exist; live AWS behaviour not yet demonstrated | PARTIAL / AWS `BLOCKED`         | E2 locally                        | No live cloud idempotency claim yet                                            |
| Conflicting retry rejection in AWS             | Deterministic/local semantics exist; live AWS behaviour not yet demonstrated | PARTIAL / AWS `BLOCKED`         | E2 locally                        | No live cloud conflict-handling claim yet                                      |
| AgentCore / Gateway controlled ticket workflow | Architecture and adapter contracts exist; target integration unavailable     | `BLOCKED` for live verification | Not reached in target environment | No end-to-end AgentCore/Gateway claim yet                                      |
| CloudWatch request reconstruction              | Planned evidence in recording/evidence ledger                                | `TARGET` / `BLOCKED`            | E0                                | No operational observability claim yet                                         |
| Cloud latency / throughput                     | Target-environment measurement unavailable                                   | `BLOCKED`                       | Not reached                       | Local measurements must not substitute for cloud measurements                  |
| Cloud unit cost                                | Target-environment billing evidence unavailable                              | `BLOCKED`                       | Not reached                       | No production cost-per-request claim                                           |
| Production availability                        | No production deployment or production traffic                               | `TARGET`                        | E0                                | No availability percentage may be claimed                                      |
| Production scalability                         | No production workload evidence                                              | `TARGET`                        | E0                                | Managed/serverless architecture does not itself prove scalability              |
| Real-user adoption / value realization         | No beta/pilot evidence yet                                                   | `TARGET`                        | E0                                | Deployment must not be represented as adoption                                 |
| Production operational readiness               | Production operating environment not established                             | `TARGET`                        | E0                                | Documentation and architecture alone do not prove readiness                    |

---

## 4. Important Current Maturity Boundaries

### Local deterministic behaviour

Reliora has substantial deterministic behaviour verified through automated tests and local integration.

This supports E1 and E2 claims depending on the specific evidence.

It does not establish equivalent behaviour in AWS.

### Local experimental measurement

Routing and ticket-runtime performance experiments have crossed into E3 because they use defined local synthetic workloads and produce quantitative measurements.

E3 evidence may support local engineering decisions.

It must not be promoted to cloud or production claims.

### AWS integration

The next meaningful maturity transition for AWS-backed capabilities is target-environment verification.

Examples include:

* Lambda execution under the intended IAM role;
* DynamoDB transaction behaviour;
* matching retry replay against live persistence;
* conflicting retry rejection;
* Gateway invocation;
* AgentCore integration;
* CloudWatch request reconstruction.

These remain blocked until a valid AWS target environment exists.

### Production maturity

Reliora currently has no E7, E8, or E9 evidence.

That is expected at the current project stage.

Portfolio language must therefore distinguish:

```text
production-oriented
```

from:

```text
production-proven
```

Reliora may currently claim the former where supported by architecture and engineering evidence.

It must not claim the latter.

---

## 5. Promotion Rules

Evidence maturity increases only when stronger evidence exists.

Examples:

```text
unit test passes
E1
    ↓
local components interact successfully
E2
    ↓
controlled local workload is measured
E3
    ↓
same capability is verified in the target cloud environment
E4
    ↓
controlled cloud experiment produces measurements
E5
```

Likewise:

```text
deployed successfully
!=
used successfully by real users
```

An E6 deployed system does not become E7 until genuine beta or pilot behaviour is observed.

---

## 6. Blocked Evidence

A blocked evidence item is not a failed control.

`BLOCKED` means the required verification environment or dependency is unavailable.

Current primary blocker:

**No active AWS account / target environment is available.**

This currently blocks:

* Terraform target plan;
* Terraform apply;
* live IAM verification;
* Lambda deployment;
* DynamoDB live behaviour;
* AgentCore/Gateway integration;
* CloudWatch operational evidence;
* cloud performance measurement;
* cloud failure experiments;
* cloud unit-cost evidence;
* deployment and teardown verification.

Local evidence already obtained remains valid within its original boundary.

### ADR-017 target-environment entry gate - 2026-09-18

A fresh M2 entry-gate check confirmed that AWS CLI configuration is present but valid AWS authentication is not currently available.

Observed command:

```text
aws sts get-caller-identity
```

Observed result:

```text
InvalidClientTokenId
```

Classification:

```text
Target-environment access     BLOCKED
Evidence maturity promotion   NONE
ADR-017 cloud experiment      NOT EXECUTED
```

The blocker is recorded in:

```text
evidence/adr017-target-environment-entry-gate-2026-09-18.md
```

This does not invalidate existing local evidence and does not authorize an alternative architecture.

---

## 7. Evidence Promotion and Claim Control

When an evidence item advances in maturity:

1. preserve the previous artifact;
2. record the new environment and measurement method;
3. identify the new evidence class where applicable;
4. update this register;
5. update dependent claims only if the new evidence supports them;
6. do not rewrite historical evidence to make it appear more mature.

The strongest available evidence should determine the strongest permitted claim.

---

## 8. Current Reliora Position

Reliora currently has meaningful evidence through E3.

The strongest quantitative evidence is currently based on controlled local synthetic experiments.

AWS-backed verification above the local boundary remains blocked.

No E7-E9 evidence currently exists.

This is the current evidence state of the project and should be represented as such in portfolio, interview, and architecture claims.

> **Evidence maturity describes what has actually been demonstrated, not what the architecture is expected to do.**
