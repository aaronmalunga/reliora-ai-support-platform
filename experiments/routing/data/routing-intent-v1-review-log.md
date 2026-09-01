# Routing Intent Dataset v1 — Pre-Freeze Review Log

## 1. Purpose

This document records the pre-freeze human review of the Reliora
`routing-intent-v1` synthetic routing benchmark.

It provides an auditable record of:

- automated findings reviewed;
- engineering interpretation of those findings;
- individual records intentionally revised;
- findings intentionally retained;
- validation and audit results after curation;
- the relationship between this review and later model benchmarking.

The review occurred before any routing classifier was trained against
`routing-intent-v1`.

This is important because dataset changes made after inspecting model
performance could contaminate the held-out evaluation process.

---

## 2. Review State

Dataset:

`routing-intent-v1`

Dataset version:

`1.0.0`

Dataset lifecycle state during this review:

`DESIGN_COMPLETE_PENDING_REVIEW`

Dataset provenance:

`SYNTHETIC_ASSUMPTION`

Review stage:

`PRE_MODEL_BENCHMARK`

The dataset was not frozen when the changes documented here were made.

---

## 3. Inputs to Review

Human review considered the following version-controlled artifacts:

- `routing-intent-v1.json`
- `routing-intent-v1-families.json`
- `routing-intent-v1-card.md`
- `routing-intent-v1-methodology.md`
- `validate_routing_data.py`
- `audit_routing_dataset.py`
- `routing-intent-v1-audit.json`

Review considered both deterministic integrity checks and diagnostic
quality findings.

---

## 4. Structural Validation Before Curation

Before lexical curation, the routing dataset passed deterministic
structural validation.

Observed state:

| Check | Result |
|---|---:|
| Records | 180 |
| Semantic families | 45 |
| BUG records | 60 |
| PLATFORM records | 60 |
| OTHER records | 60 |
| Train records | 108 |
| Validation records | 36 |
| Test records | 36 |
| Duplicate case IDs | 0 |
| Exact duplicate messages | 0 |
| Structural validator | PASS |
| mypy | PASS |
| Ruff | PASS |

The dataset also matched the family manifest for:

- intent;
- split;
- family identity;
- A/B/C/D variant structure;
- provenance.

---

## 5. Initial Diagnostic Audit

The initial quality audit produced:

| Finding | Result |
|---|---:|
| Cross-split near-duplicate findings | 0 |
| Strongly class-associated token findings | 32 |
| Cross-family class-associated token findings | 24 |

The near-duplicate result means no pair crossing train, validation, or
test exceeded the configured Jaccard or sequence-similarity review
thresholds.

This does not prove complete semantic independence between splits.

---

## 6. Lexical-Finding Interpretation

Automated lexical findings were treated as diagnostic signals rather
than automatic dataset defects.

The review distinguished between:

### Legitimate predictive language

Words associated with actual malfunction behavior may naturally help
distinguish `BUG`.

Examples include:

- `broken`
- `error`
- `wont`
- `nothing`
- `keeps`

The objective of dataset curation was not to remove legitimate
predictive language.

### Cross-class boundary vocabulary

Some domain terms intentionally occur in multiple routing classes.

Examples include:

- `order`
- `tracking`
- `payment`
- `shipping`
- `checkout`
- `return`
- `account`
- `address`

This overlap helps prevent classification from reducing to a simple
domain-keyword lookup.

### Suspected synthetic style shortcuts

The initial audit identified several words whose distribution appeared
more likely to reflect synthetic writing style than actual intent.

The clearest examples were:

- `help`
- `just`
- `page`

These terms can naturally occur in multiple intent classes and should
not independently identify a routing label.

---

## 7. Initial Findings Selected for Curation

### `help`

Initial state:

- 8 messages;
- 7 semantic families;
- dominant intent `OTHER`;
- document-level purity `100%`;
- family-level purity `100%`.

Engineering interpretation:

`help` is a generic conversational support term.

Customers may naturally use it when:

- reporting a bug;
- asking a platform question;
- making an out-of-domain request.

Its initial `OTHER`-only distribution was therefore considered a
synthetic-language artifact rather than a desirable routing feature.

Decision:

`REVISE DISTRIBUTION`

---

### `just`

Initial state:

- 6 messages;
- 6 semantic families;
- dominant intent `BUG`;
- document-level purity `100%`;
- family-level purity `100%`.

Engineering interpretation:

`just` is primarily a discourse or conversational-style word.

It does not provide meaningful evidence that a customer is reporting a
software defect.

Decision:

`REVISE DISTRIBUTION`

---

### `page`

Initial state:

- 13 messages;
- 7 semantic families;
- dominant intent `BUG`;
- document-level purity `100%`;
- family-level purity `100%`.

Engineering interpretation:

A page may be:

- broken;
- informational;
- the location where a customer looks for platform information.

The word itself should therefore not perfectly identify `BUG`.

Decision:

`REVISE DISTRIBUTION`

---

## 8. Records Revised During Pre-Freeze Curation

Only message text was changed.

Intent labels, family assignments, variant IDs, and dataset splits were
not changed.

### ROUTE-BUG-006-C

Family:

`bug-payment-button-unresponsive`

Split:

`train`

Intent:

`BUG`

Revised message:

> Can you help me understand why the payment button does nothing when I click it?

Reason:

Introduces a natural BUG use of `help` while preserving the underlying
unresponsive-payment-button failure.

---

### ROUTE-PLATFORM-006-A

Family:

`platform-loyalty-program`

Split:

`train`

Intent:

`PLATFORM`

Revised message:

> Can you help me understand how your loyalty program works?

Reason:

Introduces a natural PLATFORM use of `help`.

---

### ROUTE-PLATFORM-003-C

Family:

`platform-payment-methods`

Split:

`train`

Intent:

`PLATFORM`

Revised message:

> What payment options are available on the checkout page?

Reason:

Introduces a normal informational use of `page`.

---

### ROUTE-PLATFORM-013-B

Family:

`platform-order-tracking-process`

Split:

`test`

Intent:

`PLATFORM`

Revised message:

> Where on the order page should I look for my parcel tracking information?

Reason:

Creates an important semantic boundary between:

```text
BUG
→ tracking page does not function correctly

PLATFORM
→ customer asks where tracking information is located
```

This edit occurred before model training and before dataset freeze.

---

### ROUTE-PLATFORM-004-D

Family:

`platform-change-shipping-address`

Split:

`train`

Intent:

`PLATFORM`

Revised message:

> i just need to change where my order is going, is that allowed

Reason:

Introduces a natural PLATFORM use of the conversational term `just`.

---

### ROUTE-OTHER-007-D

Family:

`other-travel-planning`

Split:

`train`

Intent:

`OTHER`

Revised message:

> i just need help planning a short holiday in zanzibar

Reason:

Introduces a natural OTHER use of `just` while retaining the
out-of-domain travel-planning intent.

---

## 9. Findings Deliberately Retained

Not every strongly class-associated token was treated as a defect.

### `keeps`

Post-curation:

- 11 messages;
- 10 families;
- dominant intent `BUG`;
- document purity approximately `82%`;
- family purity approximately `80%`.

Decision:

`RETAIN`

Reason:

Repeated malfunction descriptions such as:

- keeps crashing;
- keeps reverting;
- keeps redirecting;

provide legitimate evidence of malfunction.

The term also occurs in `OTHER` scenarios, reducing its value as a
perfect routing shortcut.

---

### `nothing`

Post-curation:

- 7 messages;
- 6 families;
- `100% BUG` within the current dataset.

Decision:

`RETAIN AND DOCUMENT`

Reason:

Constructions such as:

- does nothing;
- nothing happens;
- nothing renders;

are genuine descriptions of non-functional behavior.

The association is semantically meaningful rather than merely
stylistic.

---

### `try`

Post-curation:

- 4 messages;
- 4 families;
- `100% BUG` within the current dataset.

Decision:

`RETAIN AND DOCUMENT`

Reason:

The token occurs inside failure constructions such as:

```text
when I try X, Y fails
```

`try` itself is not considered sufficient evidence of `BUG`, but the
surrounding construction is meaningful.

---

### `every`

Post-curation:

- 4 messages;
- 4 families;
- `100% BUG` within the current dataset.

Decision:

`RETAIN AND DOCUMENT`

Reason:

The term primarily expresses repeatability or recurrence of a failure.

It is not independently considered a routing rule.

---

### `wont`

Post-curation:

- 4 messages;
- 4 families;
- `100% BUG` within the current dataset.

Decision:

`RETAIN`

Reason:

Negative-functionality descriptions such as:

```text
button wont respond
cart wont change
```

are legitimate failure indicators.

---

## 10. Post-Curation Structural Validation

After the six message revisions, deterministic structural validation
was executed again.

Result:

`PASS`

Observed state remained:

| Check | Result |
|---|---:|
| Records | 180 |
| Semantic families | 45 |
| BUG records | 60 |
| PLATFORM records | 60 |
| OTHER records | 60 |
| Train records | 108 |
| Validation records | 36 |
| Test records | 36 |
| Duplicate case IDs | 0 |
| Exact duplicate messages | 0 |

No label, family, split, or variant integrity was lost through curation.

---

## 11. Post-Curation Diagnostic Audit

The quality audit was regenerated against the revised dataset.

Results:

| Finding | Before | After |
|---|---:|---:|
| Cross-split near-duplicate findings | 0 | 0 |
| Strongly class-associated token findings | 32 | 31 |
| Cross-family class-associated token findings | 24 | 23 |

Targeted lexical results changed as follows.

### `help`

Before:

- dominant intent: `OTHER`;
- document purity: `100%`;
- family purity: `100%`.

After:

- 10 documents;
- 9 semantic families;
- dominant intent: `OTHER`;
- document purity: `80%`;
- family purity: approximately `78%`.

Interpretation:

The term is no longer a perfect shortcut for `OTHER`.

---

### `just`

Before:

- dominant intent: `BUG`;
- document purity: `100%`;
- family purity: `100%`.

After:

`No longer meets the configured audit threshold.`

Interpretation:

The strongest identified stylistic shortcut was removed.

---

### `page`

Before:

- 13 documents;
- 7 families;
- dominant intent: `BUG`;
- document purity: `100%`;
- family purity: `100%`.

After:

- 15 documents;
- 9 families;
- dominant intent: `BUG`;
- document purity: approximately `87%`;
- family purity: approximately `78%`.

Interpretation:

`page` remains useful contextual vocabulary but no longer perfectly
identifies `BUG`.

---

## 12. Message-Length Observation

Before freeze, message length was also inspected because synthetic
datasets can accidentally encode labels through message length.

Observed token lengths:

| Intent | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| BUG | 6 | 19 | 12.00 |
| OTHER | 4 | 14 | 8.83 |
| PLATFORM | 5 | 15 | 8.88 |

BUG messages are longer on average.

This is retained as a documented benchmark limitation rather than
mechanically forcing equal message lengths.

Technical bug reports naturally contain more symptom description in
many cases.

Model performance must therefore not be interpreted as proof that a
candidate learned only semantic intent.

---

## 13. Human Review Principle

Dataset quality review follows:

```text
automated finding
        ↓
human interpretation
        ↓
semantic justification
        ↓
targeted edit only when warranted
        ↓
re-validation
        ↓
re-audit
```

It does not follow:

```text
automated finding
        ↓
force equal statistics
```

The objective is to reduce artificial shortcuts without removing
legitimate language signals.

---

## 14. Test-Set Governance

One revised message belongs to the test split:

`ROUTE-PLATFORM-013-B`

This edit is permitted at this stage because:

- dataset status is still `DESIGN_COMPLETE_PENDING_REVIEW`;
- the test set has not yet been frozen;
- no model has been trained;
- no model prediction or benchmark score influenced the edit;
- the reason was identified through model-independent dataset audit.

After dataset freeze, test records must not be modified in response to
model behavior.

Any material post-freeze correction must be documented and should
normally produce a new dataset version.

---

## 15. Review Conclusion

The reviewed dataset:

- passes deterministic structural validation;
- preserves family-aware train/validation/test separation;
- contains no cross-split near-duplicate findings at the configured
  audit thresholds;
- retains meaningful cross-class domain vocabulary;
- has reduced the clearest identified synthetic lexical shortcuts;
- documents remaining legitimate token associations;
- remains synthetic and balanced by design;
- completed human semantic review before model training;
- has not yet been used to train a routing classifier.

The subsequent held-out test-set review accepted all:

```text
9 / 9 test semantic families
36 / 36 test records
```

No additional held-out test record required revision during the final
semantic review.

Following completion of the review process:

```text
family manifest: FROZEN
routing dataset: FROZEN
test set: CLOSED TO MODEL-DRIVEN EDITING
routing-model benchmarking: NOT STARTED
```

The dataset content is frozen.

Canonical SHA-256 recording is complete.

The frozen routing-dataset milestone is recorded in Git commit:

`4c86dae270046e3d4372f41941b56de3101fcdc9`

Commit message:

`test: freeze routing intent benchmark dataset`

---

## 16. Held-Out Test-Set Semantic Review

All 36 held-out test records were manually reviewed before routing-model
training and before dataset freeze.

The review covered:

- semantic-label correctness;
- consistency between each message and its semantic-family definition;
- ambiguity between `BUG`, `PLATFORM`, and `OTHER`;
- synthetic or unnatural wording;
- cross-class lexical boundaries;
- unsupported platform assumptions;
- suitability of each family as held-out evaluation data.

Review outcome:

| Intent | Test families | Test records | Accepted | Revised |
|---|---:|---:|---:|---:|
| BUG | 3 | 12 | 12 | 0 |
| PLATFORM | 3 | 12 | 12 | 0 |
| OTHER | 3 | 12 | 12 | 0 |
| **Total** | **9** | **36** | **36** | **0** |

No held-out record required an additional pre-freeze edit.

### BUG families

#### `bug-product-filter-stuck`

Decision:

`ACCEPT`

All four variants describe malfunctioning product-filter controls.

The family consistently represents technical failure rather than a
question about product-search policy or capability.

#### `bug-profile-update-not-persisting`

Decision:

`ACCEPT`

All four variants describe incorrect persistence of profile state.

The customer reports successful-looking updates that subsequently
disappear or revert.

#### `bug-tracking-page-blank`

Decision:

`ACCEPT`

All four variants describe a tracking interface that can be reached but
does not render the expected information.

This family provides an important boundary against
`platform-order-tracking-process`.

---

### PLATFORM families

#### `platform-account-deletion`

Decision:

`ACCEPT`

All four variants ask whether or how an account can be removed.

The messages concern a platform capability or process rather than a
technical failure.

Any later authorization or execution policy for performing deletion is
outside the top-level routing-label decision.

#### `platform-exchange-policy`

Decision:

`ACCEPT`

All four variants ask about exchange rules or eligibility.

The family contains useful commerce vocabulary such as:

- item;
- return;
- refund;
- size;

without reporting malfunction.

#### `platform-order-tracking-process`

Decision:

`ACCEPT`

All four variants request information about how or where order tracking
is exposed.

This family is intentionally contrasted with
`bug-tracking-page-blank`.

For example:

```text
BUG
"The tracking page opens but it is completely blank."

PLATFORM
"Where on the order page should I look for my parcel tracking information?"
```

Both may contain words such as:

- tracking;
- order;
- page;

but the semantic distinction is:

```text
observed technical malfunction
vs.
request for platform workflow information
```

This boundary is retained intentionally.

---

### OTHER families

#### `other-chess-advice`

Decision:

`ACCEPT WITH DOCUMENTED LIMITATION`

All four variants are clearly unrelated to the supported commerce
platform.

Some questions do not provide enough board state for a complete chess
answer.

That limitation affects answerability, not the correctness of the
`OTHER` routing label.

#### `other-food-order-request`

Decision:

`ACCEPT`

The family intentionally contains commerce-like vocabulary such as:

- order;
- buy;
- purchase;
- local place.

The requested action remains outside the supported platform.

This is useful because the classifier should not learn:

```text
"order" → PLATFORM
```

without considering the surrounding intent.

#### `other-stock-market-question`

Decision:

`ACCEPT WITH DOCUMENTED LIMITATION`

All four messages request external financial or market information and
are correctly labelled `OTHER`.

Some variants are explicitly time-sensitive.

That creates a downstream freshness requirement if such a question were
ever answered, but freshness does not alter the top-level routing ground
truth.

---

## 17. Held-Out Test-Set Conclusion

The held-out test set is approved for freeze.

Observed result:

- 9 of 9 test semantic families accepted;
- 36 of 36 test records accepted;
- 0 additional test records revised during final semantic review;
- no model prediction or benchmark score informed the review;
- test-family assignments remain unchanged;
- test labels remain unchanged.

The test set is now closed to model-driven editing because the dataset
lifecycle state has been changed to `FROZEN`.

After freeze, a model error is evidence about the model or routing
strategy.

It must not automatically result in rewriting the held-out example.

A genuine post-freeze ground-truth defect must instead be:

1. documented independently of model preference;
2. reviewed explicitly;
3. corrected under dataset change control;
4. versioned when material.

---

## 18. Freeze Finalization Status Before Benchmarking

The semantic review and routing-dataset content freeze are complete.

The following validation and freeze gates have completed successfully:

```text
structural validator: PASS
diagnostic dataset audit: REGENERATED
mypy: PASS
Ruff: PASS
pytest: PASS — 23 / 23
git diff --check: PASS
canonical dataset SHA-256: RECORDED
canonical family-manifest SHA-256: RECORDED
hash basis: RECORDED
committed artifact hash verification: PASS
```

Frozen identities:

```text
routing-intent-v1.json
369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450

routing-intent-v1-families.json
93d07598b846c2df3490f39b68971b2ae2a5dba872fb149e513f592c0d5724a1
```

The routing-dataset freeze milestone is recorded in Git commit:

```text
freeze commit:
4c86dae270046e3d4372f41941b56de3101fcdc9

commit message:
test: freeze routing intent benchmark dataset
```

The frozen artifacts were subsequently extracted directly from that Git
commit and hashed independently.

The verification result was:

```text
DATASET MATCH: True
MANIFEST MATCH: True
ALL COMMITTED HASHES MATCH: True
```

This verifies that the dataset and family manifest stored in the frozen
Git commit correspond exactly to the canonical SHA-256 identities
recorded in the benchmark documentation.

The remaining work before routing-model benchmarking is limited to
provenance-documentation finalization:

1. synchronize the remaining routing-experiment documentation with the
   recorded freeze commit and verification result;
2. perform a final Git diff/status review of the provenance-only
   documentation changes;
3. commit the provenance-only documentation update.

No routing candidate should be trained, selected, or evaluated on the
held-out test set until these documentation-finalization steps are
complete.

Any subsequent change to frozen benchmark content must follow the
versioning and change-control policy rather than being made in response
to model performance.