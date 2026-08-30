# Reliora Autonomy and Human-Intervention Policy

## Purpose

This document defines the level of autonomy Reliora may exercise for different customer-support actions.

The policy separates:

- model reasoning;
- deterministic validation;
- business authorization;
- side-effect execution;
- human intervention.

The central rule is:

> **The LLM may propose; deterministic software validates and authorizes.**

Tool availability does not imply permission to use a tool.

---

# Autonomy Principles

## AP-001 — Risk Determines Autonomy

The level of automation must be proportional to the potential impact of an incorrect action.

Low-risk informational actions may be automated more freely than actions that change customer, financial, account, or operational state.

## AP-002 — Uncertainty Reduces Autonomy

When the system cannot confidently determine:

- customer intent;
- knowledge coverage;
- required tool arguments;
- authorization;
- backend outcome;

it must reduce autonomy rather than guess.

The normal fallback is structured human handoff.

## AP-003 — LLM Output Is Not Authorization

The model may:

- classify;
- recommend;
- extract;
- summarize;
- propose tool arguments.

The model alone may not authorize a side effect.

Authorization must occur through deterministic application logic or an external policy layer.

## AP-004 — Backend Truth Overrides Model Claims

The model must never claim that an operation succeeded unless the authoritative backend confirms success.

Examples include:

- ticket creation;
- refund creation;
- account modification;
- payment action.

## AP-005 — Human Access Must Remain Available

Customers must not be trapped indefinitely in unsuccessful AI interactions.

Unsupported, ambiguous, failed, or risk-sensitive workflows must have a defined path to human support.

---

# Risk Levels

Reliora uses four action-risk levels.

## Risk Level 0 — Informational / No Side Effect

Examples:

- answering an approved FAQ question;
- explaining a supported policy;
- asking a customer for missing information.

Potential impact of an incorrect response is limited because no backend state is changed.

### Default autonomy

**AUTOMATIC**, subject to:

- knowledge grounding;
- output validation;
- safety controls;
- confidence or coverage rules.

---

## Risk Level 1 — Low-Risk Reversible Side Effect

Example in Reliora:

- creating a bug-report ticket.

The operation changes backend state but does not directly alter:

- money;
- account permissions;
- orders;
- customer identity;
- security settings.

A mistaken ticket can be reviewed or closed.

### Default autonomy

**AUTOMATIC AFTER DETERMINISTIC VALIDATION**

Required controls include:

- complete required fields;
- schema validation;
- operation identifier;
- idempotency;
- approved tool;
- successful backend confirmation;
- traceability.

---

## Risk Level 2 — Material Customer or Business Action

Examples outside the initial Reliora scope:

- cancelling an order;
- changing shipping information;
- issuing store credit;
- modifying customer profile data;
- changing subscription state.

These actions can materially affect a customer or business process.

### Default autonomy

**HUMAN APPROVAL OR STRONG DETERMINISTIC AUTHORIZATION REQUIRED**

Reliora P1-S2 does not implement these operations.

They are documented to establish the autonomy boundary for future systems.

---

## Risk Level 3 — Financial, Security, Legal, or Irreversible Action

Examples:

- issuing a refund;
- processing payment;
- changing account ownership;
- altering authentication or security settings;
- approving a legal settlement;
- deleting high-value customer data.

### Default autonomy

**NOT AUTONOMOUS IN RELIORA**

Such capabilities require a separate architecture decision involving identity, authorization, policy, audit, and potentially explicit human approval.

---

# Reliora Action Matrix

| Action | Risk | AI May Propose? | Deterministic Validation? | Automatic Execution? | Human Handoff |
|---|---:|---|---|---|---|
| Classify customer intent | 0 | Yes | Yes | Yes | On ambiguity |
| Determine FAQ coverage | 0 | Yes | Yes / contract checked | Yes | If unsupported |
| Answer supported FAQ | 0 | Yes | Grounding/output checks | Yes | On uncertainty |
| Ask for missing bug field | 0 | Yes | Workflow-state check | Yes | If collection fails |
| Create bug ticket | 1 | Yes | **Required** | Yes after validation | On failure/conflict |
| Retry bug creation | 1 | No new business decision required | **Idempotency required** | Yes | On unresolved conflict |
| Invent unsupported policy | N/A | No | Blocked | No | **Required** |
| Fabricate ticket success | N/A | No | Blocked | No | Required if outcome unknown |
| Refund customer | 3 | Could recommend only | Strong authorization required | **No — out of P1 scope** | Required |
| Modify account | 2–3 | Could recommend only | Strong authorization required | **No — out of P1 scope** | Required |

---

# Automatic Handoff Conditions

Reliora must transition to human support when one or more of the following conditions occur.

## H-001 — Unsupported Knowledge

The request belongs to the platform domain but the approved knowledge source does not support an answer.

## H-002 — Unsupported Intent

The request falls outside the automated support capabilities.

## H-003 — Routing Ambiguity

The system cannot safely select one permitted workflow.

## H-004 — Repeated Information Failure

The system cannot obtain valid required information after the defined interaction limit.

## H-005 — Tool Validation Failure

A proposed tool call fails deterministic schema, policy, or business-rule validation.

## H-006 — Backend Failure

A required dependency cannot complete the operation after the permitted retry policy.

## H-007 — Ambiguous Side-Effect Outcome

The system cannot establish whether a side effect completed successfully.

The model must not guess.

## H-008 — Idempotency Conflict

The same operation identifier is presented with materially different payload data.

## H-009 — Security or Prompt-Injection Trigger

A request attempts to:

- override protected system instructions;
- expose hidden instructions;
- trigger unauthorized tools;
- obtain secrets;
- bypass policy.

## H-010 — Higher-Risk Requested Action

The user requests an action outside Reliora's authorized autonomy boundary.

Examples include refunds, payments, account modification, or other high-impact operations.

---

# Structured Handoff Contract

A handoff should preserve useful operational context without exposing hidden reasoning.

A conceptual handoff object is:

```json
{
  "handoff_reason": "unsupported_policy_question",
  "intent": "PLATFORM",
  "conversation_summary": "Customer asked about a policy not present in the approved FAQ.",
  "information_already_collected": [],
  "attempted_actions": [],
  "failed_actions": [],
  "recommended_queue": "customer_support",
  "request_id": "req-example",
  "session_id": "session-example",
  "prompt_version": "prompt-version",
  "application_version": "application-version"
}
```

The exact schema will later be implemented through typed application contracts.

---

# Information That Must Not Enter the Handoff

The handoff package must not contain:

- hidden chain-of-thought;
- system prompts;
- secrets or credentials;
- unnecessary personal information;
- internal security logic;
- raw telemetry that does not help the receiving human;
- information outside the purpose of resolving the support request.

Decision provenance should be recorded separately from private model reasoning.

---

# Human Feedback

Human intervention is not only a fallback mechanism.

Reviewed human resolutions may produce a feedback event containing information such as:

- original system decision;
- handoff reason;
- human decision;
- correction category;
- whether automation should have succeeded;
- candidate future evaluation case.

Human feedback must not automatically become model training or evaluation ground truth.

It must be reviewed before promotion into a versioned dataset.

---

# Future Higher-Risk Tools

If future versions introduce capabilities such as:

- refunds;
- order cancellation;
- payments;
- account modifications;
- loyalty-balance changes;

the autonomy policy must be reviewed before those tools are exposed to the agent.

Potential controls may include:

- authenticated customer identity;
- scoped authorization;
- deterministic business rules;
- AgentCore Policy;
- temporal authorization;
- human approval;
- transaction limits;
- enhanced audit controls.

Their availability in AWS is not sufficient justification for enabling them.

---

# Current Reliora Autonomy Boundary

The initial P1-S2 system permits autonomous execution only for:

1. low-risk informational responses grounded in approved knowledge; and
2. validated, idempotent bug-ticket creation.

Unsupported, ambiguous, unsafe, failed, or higher-risk actions transition to structured human support.

## Current Status

This document defines the **TARGET autonomy policy**.

Compliance will be demonstrated progressively through implementation, deterministic tests, adversarial evaluation, integration testing, and operational evidence.