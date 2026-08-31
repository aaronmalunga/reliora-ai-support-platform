# Dataset Card — deterministic-evaluator-regression-v1

## Dataset

**ID:** `deterministic-evaluator-regression-v1`

**Version:** `1.0.0`

**Cases:** 15

---

## Purpose

This dataset exercises the deterministic Reliora evaluators that are currently implemented.

It provides reviewed positive, negative, boundary, and control fixtures for:

- `INV-004` — incremental bug-field collection;
- `INV-012` — currently implemented internal-information leakage checks;
- `FACT-001` — deterministic required-fact completeness.

The dataset is intended to answer:

> Given a reviewed evaluator input and expected outcome, does the current deterministic evaluator return the expected result?

It is not intended to answer:

> Is the complete Reliora system correct?

---

## Dataset Type

This is a:

```text
designed regression dataset
```

It is not:

```text
a training dataset
a production traffic sample
a Stage-1 historical evidence dataset
a benchmark of real customer frequency
```

The cases were deliberately authored to exercise known evaluator behaviour.

Their distribution must therefore not be interpreted as representative of production prevalence.

For example, the number of negative cases in this dataset does not imply that the same proportion of production requests would contain defects.

---

# Relationship to Stage-1 Reproduction

Reliora maintains a separate dataset:

```text
stage1-reproduction-v1
```

That dataset preserves known defects and observations from the frozen Stage-1 repository.

Its purpose is:

> Can Reliora detect specific historically observed Stage-1 evaluation gaps?

This dataset has a different purpose:

```text
deterministic-evaluator-regression-v1
```

asks:

> Does each currently implemented deterministic evaluator behave as expected across deliberately constructed regression cases?

The two dataset families must remain separate.

Historical evidence must not be silently mixed with designed regression fixtures.

---

# Fixture Policy

The dataset declares:

```text
origin
→ designed_regression_fixture

historical_observation
→ false

expected_results_are_reviewed
→ true

production_frequency_is_not_implied
→ true
```

Each expected evaluator result is a reviewed engineering expectation.

It is not a claim that the fixture occurred in production or Stage 1.

---

# Current Coverage

The dataset contains 15 cases.

Coverage by evaluator:

```text
INV-004     5 cases
INV-012     5 cases
FACT-001    5 cases
```

Coverage by case type:

```text
positive    3
negative    8
boundary    2
control     2
```

The distribution is based on useful evaluator coverage rather than an attempt to balance categories artificially.

---

# Case-Type Semantics

## Positive

A fixture representing behaviour that should satisfy the evaluator contract.

Example:

```text
one required missing bug field requested
→ expected evaluator result: PASS
```

---

## Negative

A fixture intentionally containing behaviour that should violate the evaluator contract.

Example:

```text
multiple missing bug fields requested in one turn
→ expected evaluator result: FAIL
```

---

## Boundary

A fixture targeting an implementation edge or unusual but valid input condition.

Example:

```text
mixed-case thinking tag containing attributes
```

Boundary cases help test whether the evaluator behaves correctly near the edges of its intended matching logic.

---

## Control

A clean fixture used to demonstrate that the evaluator should not reject ordinary valid behaviour.

Example:

```text
normal customer-facing support language
→ expected leakage evaluation: PASS
```

Controls are particularly important for detecting false positives.

---

# INV-004 Coverage

## Contract

`INV-004` requires bug-report information to be collected incrementally.

The initial policy permits no more than one required missing field to be requested in a single collection turn.

The currently implemented evaluator receives:

```text
missing_fields
requested_fields
```

and deterministically compares the two.

---

## Cases

### REG-INV004-001

**Type:** positive

Several bug fields remain missing and exactly one currently missing field is requested.

**Expected result:** PASS

---

### REG-INV004-002

**Type:** negative

Required bug fields remain missing but no field is requested.

**Expected result:** FAIL

---

### REG-INV004-003

**Type:** negative

Multiple required missing fields are requested in one turn.

**Expected result:** FAIL

---

### REG-INV004-004

**Type:** negative

The workflow requests a field that is not currently missing.

**Expected result:** FAIL

---

### REG-INV004-005

**Type:** control

No required fields remain missing and no additional field is requested.

**Expected result:** PASS

---

## INV-004 Scope

This dataset evaluates the deterministic state-versus-request contract.

It does not yet prove:

```text
that an LLM correctly extracted every bug field
that tool execution was prevented
that workflow state was persisted correctly
that the complete bug-report workflow is correct
```

Those concerns correspond to other invariants and later integration layers.

---

# INV-012 Coverage

## Contract

`INV-012` states that customer-facing output must not expose prohibited internal information.

The broader behavioural contract includes categories such as:

```text
hidden reasoning
chain-of-thought markers
system-prompt contents
protected route labels
credentials
secrets
```

However, the current deterministic evaluator implements only specific prohibited-marker families.

At dataset version `1.0.0`, the implemented deterministic checks cover:

```text
literal HUMAN HANDOFF route-label exposure
thinking tags such as <thinking>...</thinking>
case-insensitive thinking-tag variants
thinking tags containing attributes
```

---

## Cases

### REG-INV012-001

**Type:** control

Ordinary customer-facing support text contains no currently prohibited marker.

**Expected result:** PASS

---

### REG-INV012-002

**Type:** negative

The literal internal route label:

```text
HUMAN HANDOFF
```

appears in customer-visible output.

**Expected result:** FAIL

---

### REG-INV012-003

**Type:** negative

A customer-visible response contains:

```text
<thinking>...</thinking>
```

**Expected result:** FAIL

---

### REG-INV012-004

**Type:** boundary

A mixed-case thinking tag containing an attribute appears in customer-visible text.

**Expected result:** FAIL

---

### REG-INV012-005

**Type:** negative

A response contains multiple currently detectable prohibited markers.

**Expected result:** FAIL

---

## INV-012 Scope Limitation

Passing the current INV-012 evaluator does not prove that every possible form of internal-information leakage is absent.

Specifically, version `1.0.0` does not yet provide comprehensive deterministic detection for:

```text
arbitrary system-prompt disclosure
arbitrary credentials
arbitrary secrets
semantic disclosure of internal reasoning without marker tags
every possible internal route representation
```

Therefore the defensible claim is:

> Version 1.0.0 provides deterministic regression coverage for the currently implemented INV-012 leakage-marker families.

It must not be described as complete verification of the entire INV-012 contract.

---

# FACT-001 Coverage

## Contract

`FACT-001` evaluates whether every reviewed required fact has at least one accepted textual representation in a response.

Each fact may define one or more accepted patterns.

The evaluator performs case-insensitive lexical matching.

For example:

```text
defective
damaged
faulty
```

may be reviewed alternative patterns for the same required fact.

---

## Cases

### REG-FACT001-001

**Type:** positive

All reviewed return-policy facts are represented.

**Expected result:** PASS

---

### REG-FACT001-002

**Type:** positive

An accepted alternative representation such as:

```text
damaged
```

satisfies the defective-item exception fact.

**Expected result:** PASS

---

### REG-FACT001-003

**Type:** negative

The defective-item exception is omitted while the other required facts are represented.

**Expected result:** FAIL

---

### REG-FACT001-004

**Type:** negative

Multiple reviewed required facts are omitted.

**Expected result:** FAIL

---

### REG-FACT001-005

**Type:** boundary

The response is empty and therefore represents none of the required facts.

**Expected result:** FAIL

---

# FACT-001 Scope Limitation

`FACT-001` is a lexical completeness evaluator.

It determines whether reviewed textual patterns are represented.

It does not independently prove:

```text
semantic truth
logical consistency
absence of negation
absence of contradiction
policy correctness beyond the reviewed assertions
```

For example, the presence of the phrase:

```text
30 days
```

demonstrates lexical representation of that reviewed pattern.

By itself, it does not prove that the surrounding sentence expresses the correct semantic relationship.

Semantic factual correctness therefore requires a different or additional evaluation layer.

---

# Coverage Boundary

The behavioural evaluation contract currently defines additional invariants beyond those represented here.

This dataset intentionally does not create artificial fixtures for unimplemented evaluator surfaces merely to increase coverage numbers.

Examples include:

```text
INV-001
top-level intent

INV-002
intent versus knowledge coverage

INV-003
required bug fields before tool execution

INV-005
tool-argument contract validity

INV-006
authorization before tool execution

INV-007
idempotent ticket creation

INV-008
operation-ID conflict detection

INV-009
backend-confirmed success

INV-010
ticket-ID provenance

INV-011
unsupported-knowledge handling

INV-013
structured human handoff

INV-014
handoff data minimisation
```

Those invariants become executable regression targets when the relevant architecture exists.

This prevents documentation from claiming implementation maturity that the system has not yet reached.

---

# Evidence Classification

The dataset cases themselves are:

```text
DESIGNED REGRESSION FIXTURES
```

They are not `OBSERVED` production or Stage-1 evidence.

Results generated by executing Reliora evaluators against this dataset are classified as:

```text
EXPERIMENTAL
```

until a different evidence classification is justified by the execution context.

---

# Expected-Result Policy

Every case contains:

```text
expected_evaluator_passed
```

The regression runner should compare:

```text
actual evaluator result
```

against:

```text
reviewed expected result
```

A matched expectation should be reported as:

```text
PASS
```

An unexpected result should be reported as:

```text
MISMATCH
```

This differs from the Stage-1 reproduction dataset, where statuses such as:

```text
DETECTED
CONFIRMED
DOCUMENTED
MISMATCH
```

carry historical-reproduction semantics.

Generic regression fixtures do not need those historical categories.

---

# Release-Gate Intent

The regression runner should eventually return:

```text
exit code 0
```

when every reviewed expectation matches.

It should return:

```text
exit code 1
```

when one or more cases produce a mismatch.

This makes the suite suitable for later use in CI release gates.

The presence of a release gate does not by itself establish production readiness.

---

# Dataset Integrity

Material changes to:

```text
case inputs
expected results
reviewed rationale
coverage
```

require deliberate dataset versioning.

The dataset must not be silently modified merely to make an evaluator appear successful.

Generated evidence should include a SHA-256 hash of the exact canonical dataset representation used during execution.

Reliora currently standardizes text hashing on:

```text
UTF-8 text
normalized to LF line endings
before SHA-256
```

to avoid platform-specific CRLF/LF differences changing evidence identity.

---

# Known Limitations

Version `1.0.0` has several explicit limitations:

1. It evaluates only three currently implemented evaluator families.
2. INV-012 coverage is narrower than the complete documented invariant.
3. FACT-001 measures lexical completeness rather than semantic truth.
4. The dataset does not represent real customer traffic distribution.
5. The dataset does not establish production reliability.
6. The fixtures do not measure latency, cost, scalability, or operational resilience.
7. Passing every case means only that the evaluated implementation matched all 15 reviewed expectations in this dataset version.

---

# Claim Discipline

A valid statement after a successful execution would be:

> All 15 reviewed fixtures in `deterministic-evaluator-regression-v1` matched their expected deterministic evaluator outcomes.

A stronger statement such as:

```text
Reliora is 100% reliable.
```

would not be supported by this dataset.

Likewise:

```text
INV-012 is fully solved.
```

would exceed the current evidence because the implemented leakage detector covers only part of the broader contract.

---

# Intended Use

This dataset may be used for:

- deterministic evaluator regression testing;
- evaluator-development feedback;
- release-regression gates;
- CI quality controls;
- demonstration of evaluator behaviour;
- evidence generation;
- controlled reproduction of evaluator edge cases.

It should not be used as:

- production prevalence evidence;
- a customer-behaviour dataset;
- an LLM training dataset;
- proof of complete agent reliability;
- evidence that unimplemented invariants have been satisfied.

---

# Versioning Rule

Version `1.0.0` should remain stable once incorporated into generated evidence.

Future changes should use a new version when they materially alter:

```text
fixtures
expected outcomes
evaluator coverage
interpretation
```

This preserves the relationship:

```text
dataset version
        ↓
canonical dataset hash
        ↓
evaluation execution
        ↓
generated report
        ↓
engineering claim
```