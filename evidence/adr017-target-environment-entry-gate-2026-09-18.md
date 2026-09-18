# ADR-017 Target-Environment Entry Gate - 2026-09-18

**Project:** Reliora AI Support Platform
**Stage:** M2 - ADR-017 Trusted Execution Identity Experiment
**Branch:** `feat/adr017-trusted-identity-experiment`
**Baseline commit:** `1892501`
**Evidence class:** `OBSERVED`
**Target-environment status:** `BLOCKED`
**Evidence maturity promotion:** None

---

## 1. Purpose

This artifact records the target-environment entry gate for the ADR-017 trusted execution identity experiment.

The experiment requires authenticated AWS access before Reliora can test the real AgentCore / Gateway / Lambda / DynamoDB identity path.

No architecture change is authorized by this artifact.

---

## 2. Local Tooling Context

Observed locally:

```text
AWS CLI: 2.33.29
AWS CLI runtime Python: 3.13.11
Operating system: Windows 11 AMD64
Configured region: us-east-1
Explicit AWS profile: none
Credential source: shared credentials file
```

Credential values are intentionally not recorded.

---

## 3. Authentication Gate

Command:

```text
aws sts get-caller-identity
```

Observed result:

```text
InvalidClientTokenId
The security token included in the request is invalid.
```

The STS identity gate did not succeed.

Therefore the experiment did not reach an authenticated AWS target environment.

---

## 4. Classification

This result means:

```text
AWS configuration exists             OBSERVED
Valid AWS authentication             NOT ESTABLISHED
Target environment reached           NO
ADR-017 cloud experiment executed    NO
AgentCore identity propagation       NOT VERIFIED
Gateway identity propagation         NOT VERIFIED
Lambda trusted identity path         NOT VERIFIED IN AWS
DynamoDB retry replay in AWS         NOT VERIFIED
ADR-017 acceptance criteria met      NO
```

This is a blocked evidence state, not a failed identity control.

---

## 5. Architecture Decision Consequence

ADR-017 remains:

```text
PROPOSED
```

The current architecture must not be rejected merely because the required target environment is unavailable.

The following are not justified by this blocker:

- replacing the managed AgentCore / Gateway / Lambda / DynamoDB baseline;
- introducing Strands solely to avoid the blocked experiment;
- using model-generated operation identity;
- treating request identity as logical operation identity;
- claiming end-to-end identity propagation;
- claiming live AWS retry/idempotency behaviour.

The existing local evidence remains valid only within its established boundary.

---

## 6. Unblock Condition

M2 can resume when authorized AWS credentials are available and:

```text
aws sts get-caller-identity
```

succeeds for the intended target account and region.

After that gate succeeds, the next action is the smallest end-to-end ADR-017 identity-propagation experiment.

---

## 7. Claim Boundary

This artifact supports the claim:

> On 2026-09-18, Reliora attempted the ADR-017 target-environment entry gate. AWS CLI configuration was present, but STS authentication failed with `InvalidClientTokenId`, so the cloud identity experiment remained blocked before deployment or invocation.

It does not support any claim about AgentCore, Gateway, Lambda, DynamoDB, cloud reliability, or production behaviour.
