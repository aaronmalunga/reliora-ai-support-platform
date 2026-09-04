# ADR-017 - Trusted Execution Identity for Side-Effecting Agent Tools

## Status

PROPOSED

## Date

2026-09-04

## Context

Reliora distinguishes three identities:

- `request_id`: one processing or execution attempt.
- `session_id`: one logical customer conversation.
- `operation_id`: one logical side effect that remains stable across retries.

The current Lambda adapter expects custom Reliora identifiers in Lambda
ClientContext. Local tests verify that contract, but the real AgentCore
Gateway integration has not yet demonstrated that those custom values are
supplied end to end.

This decision affects:

- FR-001 - Request Identification
- FR-002 - Session Identification
- FR-003 - Operation Identification
- FR-010 - Exactly-One Logical Ticket
- FR-011 - Idempotent Retry Result
- FR-012 - Idempotency Conflict Detection
- NFR-REL-001 - Safe Retry Behaviour
- NFR-SEC-003 - Deterministic Authorization
- CB-004 - Side-Effect Boundary

## Decision Question

Where should trusted request, session, and logical-operation identity originate
for a side-effecting agent tool?

## Options

### A. Let the model supply the identifiers

Rejected.

The model may propose business arguments, but operation identity participates
in the deterministic idempotency boundary.

### B. Use an AgentCore request identifier as operation_id

Rejected.

A request represents one execution attempt. An operation represents one
logical business action and may span multiple attempts.

### C. Use a deterministic application/runtime identity boundary

Proposed.

Reliora should obtain execution identity from trusted application and transport
boundaries rather than from model-generated business arguments.

Intended semantics:

- `request_id` comes from trusted execution/request metadata.
- `session_id` is owned by the Reliora application/runtime conversation boundary.
- `operation_id` is created deterministically for one logical side effect and
  preserved across retries of that operation.

The exact Strands/MCP/Gateway propagation mechanism remains unverified.

## Decision

Option C is the proposed architecture.

It MUST NOT move to ACCEPTED until an integration experiment demonstrates the
identity path through the real AgentCore runtime.

## Acceptance Criteria

ADR-017 may become ACCEPTED when:

1. trusted identity is demonstrated end to end;
2. model arguments cannot override operation identity;
3. a retry preserves `operation_id`;
4. a retry can have a distinct request identity;
5. DynamoDB replays the original result rather than creating a duplicate;
6. a new logical tool call receives a different operation identity;
7. deterministic tests cover the identity transformation.

## Consequences

Benefits:

- idempotency remains under deterministic software control;
- request, session, and operation semantics remain distinct;
- the domain model remains portable beyond a specific AWS transport.

Costs:

- identity propagation becomes an explicit runtime responsibility;
- integration code and tests are required;
- provider behaviour must be verified rather than assumed.

## Evidence Status

- Identity domain behaviour: VERIFIED LOCALLY
- DynamoDB idempotency behaviour: VERIFIED LOCALLY
- AgentCore identity propagation: NOT YET VERIFIED
- AWS retry/idempotency behaviour: NOT YET VERIFIED

## Reconsideration Triggers

Revisit this decision if:

- AgentCore provides a documented logical-operation identity with the required
  retry semantics;
- Strands runtime behaviour does not preserve the required identity;
- a simpler trusted mechanism proves the same invariants.

## Current Claim

Reliora separates request, session, and logical-operation identities and
verifies their local idempotency semantics deterministically. End-to-end
AgentCore identity propagation remains under integration verification.


## Implementation Hypothesis History

During investigation of the trusted-identity requirement, Strands `toolUseId`
and tool-retry behaviour were considered as a possible mechanism for deriving
stable logical operation identity.

This was a candidate implementation mechanism, not an accepted architecture
decision.

The candidate was initially treated too strongly as the likely next
implementation. A subsequent source-precedence review confirmed that Reliora's
accepted baseline still uses the managed AgentCore Harness / Gateway / Lambda /
DynamoDB architecture and that this baseline had not yet been demonstrated
incapable of satisfying the identity requirement.

No Strands dependency, runtime replacement, or cloud resource was introduced.

The implementation sequence was corrected before execution.

The governing lesson is:

> UNKNOWN is an experiment state, not permission to introduce a plausible
> technology.

Therefore:

```text
candidate mechanism
!= architecture decision
!= implemented architecture
!= verified architecture```

Strands remains only a possible future implementation mechanism if later evidence independently justifies its introduction.
