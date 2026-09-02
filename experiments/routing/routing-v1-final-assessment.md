# Routing Benchmark v1 — Final Assessment

## Assessment metadata

| Field | Value |
|---|---|
| Assessment | Routing Benchmark v1 |
| Status | `CLOSED` |
| Selected candidate | `C2-N1-C2.0` |
| Feature representation | TF-IDF word unigrams |
| Classifier | Linear SVM (`LinearSVC`) |
| Regularization | `C = 2.0` |
| Evidence classification | `EXPERIMENTAL` |
| Held-out test runs used for v1 | One |
| Post-test tuning performed | No |

## Executive conclusion

Routing Benchmark v1 demonstrated that a lightweight learned classifier materially outperformed the deterministic lexical routing baseline.

The selected `C2-N1-C2.0` configuration achieved strong validation performance but did not reproduce that level of performance on the untouched held-out test set.

The held-out result exposed a real generalization limitation, particularly at the boundary between PLATFORM and OTHER intents.

The experiment therefore supports the use of classical machine learning over the original expanding lexical-rule router, but it does **not** support a claim that the current routing model is production-grade.

Routing v1 is closed without tuning against held-out test failures.

Any future routing improvement must occur in a separately versioned evaluation cycle with new independent evaluation evidence.

---

## Final evidence summary

| Metric | Validation | Held-out test |
|---|---:|---:|
| Accuracy | 0.9722 | 0.7500 |
| Macro F1 | 0.9722 | 0.7403 |
| Failures | 1 / 36 | 9 / 36 |
| BUG recall | 1.0000 | 1.0000 |
| PLATFORM recall | 0.9167 | 0.6667 |
| OTHER recall | 1.0000 | 0.5833 |

The validation-to-test macro-F1 difference was:

`0.9722 - 0.7403 = 0.2319`

The test result therefore did not confirm the performance level observed during validation.

---

## Held-out confusion matrix

Rows are actual intents and columns are predicted intents.

| Actual \ Predicted | BUG | PLATFORM | OTHER |
|---|---:|---:|---:|
| BUG | 12 | 0 | 0 |
| PLATFORM | 1 | 8 | 3 |
| OTHER | 3 | 2 | 7 |

The selected model retained perfect BUG recall on the held-out test.

Its primary weakness was distinguishing PLATFORM and OTHER requests and preventing unrelated requests from being drawn into support-oriented classes.

---

## Failure directions

| Expected | Predicted | Count | Operational interpretation |
|---|---|---:|---|
| PLATFORM | OTHER | 3 | Valid support requests may unnecessarily fall to fallback or handoff |
| PLATFORM | BUG | 1 | Policy/support request may enter the bug-reporting path |
| OTHER | BUG | 3 | Unrelated request may incorrectly activate bug handling |
| OTHER | PLATFORM | 2 | Unrelated request may enter platform-support handling |
| BUG | PLATFORM or OTHER | 0 | No true BUG cases were lost |

The absence of BUG false negatives is favorable, but the PLATFORM/OTHER boundary remains insufficiently robust for production claims.

---

## Held-out failure families

| Semantic family | Failures | Observed pattern |
|---|---:|---|
| `other-food-order-request` | 3 | Commerce-like words such as `order` and `buy` appear to overlap with retailer-support vocabulary |
| `platform-account-deletion` | 2 | Legitimate account-support intent fell to OTHER |
| `platform-exchange-policy` | 2 | Exchange-policy language was confused with OTHER and BUG |
| `other-stock-market-question` | 1 | `stock` appeared in an unrelated financial context but was classified as BUG |
| `other-chess-advice` | 1 | Unrelated advice request was classified as PLATFORM |

The concentration of failures by semantic family indicates that the errors were not uniformly distributed.

---

## Failure examples

| Case | Expected | Predicted | Message |
|---|---|---|---|
| `ROUTE-PLATFORM-014-A` | PLATFORM | OTHER | How can I delete my account? |
| `ROUTE-PLATFORM-014-D` | PLATFORM | OTHER | can i completely get rid of my account |
| `ROUTE-PLATFORM-015-A` | PLATFORM | OTHER | Can I exchange an item instead of returning it for a refund? |
| `ROUTE-PLATFORM-015-C` | PLATFORM | BUG | If I ordered the wrong size, am I allowed to swap it for another one? |
| `ROUTE-OTHER-013-D` | OTHER | BUG | is apple stock doing well right now |
| `ROUTE-OTHER-014-A` | OTHER | BUG | Order me a pepperoni pizza from a restaurant near my house. |
| `ROUTE-OTHER-014-C` | OTHER | BUG | Please buy me lunch from the cafe down the road. |
| `ROUTE-OTHER-014-D` | OTHER | PLATFORM | i want to order sushi from a local place, can you do it |
| `ROUTE-OTHER-015-C` | OTHER | PLATFORM | Can you help me understand how to respond to the Sicilian Defence? |

---

## Interpretation

The error pattern is consistent with a limitation of the current unigram TF-IDF representation.

Words such as:

- `order`;
- `buy`;
- `stock`;
- `account`;
- `size`;

can be strongly associated with the support domain while also appearing in unrelated or semantically different contexts.

A unigram representation captures weighted lexical evidence but has limited representation of broader semantic context.

This is a supported hypothesis based on the observed failure pattern, not a proven causal conclusion.

The held-out test therefore suggests that stronger semantic separation may be required if future routing requirements demand materially higher generalization.

---

## Why the original candidate selection remains valid

The held-out result does not retroactively make the pre-test selection decision incorrect.

At selection time, the available evidence was:

| Candidate | Validation macro F1 | Validation failures |
|---|---:|---:|
| B1 deterministic rules | 0.2767 | 22 |
| C1-N1-C2.0 | 0.9444 | 2 |
| C2-N1-C2.0 | **0.9722** | **1** |

`C2-N1-C2.0` also demonstrated deterministic repeated predictions and negligible local inference overhead relative to the expected cloud request path.

Therefore selecting C2 before test exposure was justified by the evidence available at the decision boundary.

The held-out test answers a different question:

> How well did the frozen selected configuration generalize to an additional untouched set of semantic families?

The answer was:

> Better than the deterministic baseline evidence suggested, but substantially below the selected model's validation performance.

---

## Deterministic baseline conclusion

The deterministic B1 router achieved:

| Stage | Result |
|---|---:|
| Training after train-only development | 108 / 108 correct |
| Validation accuracy | 0.3889 |
| Validation macro F1 | 0.2767 |
| Validation failures | 22 / 36 |

This demonstrated that perfect development-set fit did not translate into semantic-family generalization.

The evidence therefore supports replacing the expanding lexical rule router with a learned classifier.

---

## Operational evidence

The shortlisted candidates were also measured for local inference latency and prediction determinism.

| Candidate | Deterministic | Local p50 / message | Local p95 / message |
|---|---|---:|---:|
| B1 | Yes | 0.0167 ms | 0.0307 ms |
| C1-N1-C2.0 | Yes | 0.1079 ms | 0.1563 ms |
| C2-N1-C2.0 | Yes | 0.1071 ms | 0.1627 ms |

The additional local inference cost of C2 relative to B1 was small in absolute terms and did not justify accepting B1's severe validation generalization failure.

These measurements represent local batch-normalized inference only.

They are not production API latency measurements.

---

## Production-readiness conclusion

Routing Benchmark v1 does **not** establish production-grade routing performance.

The evidence supports the following narrower claims:

| Claim | Supported? |
|---|---|
| Deterministic lexical rules were insufficient | Yes |
| Classical ML materially improved validation performance | Yes |
| C2 was the strongest preregistered validation candidate | Yes |
| C2 preserved all BUG cases on held-out test | Yes |
| Validation performance generalized unchanged to TEST | No |
| PLATFORM/OTHER separation is production-ready | No |
| Current router should be advertised as 97.22% accurate | No |
| Current evidence justifies an LLM router | No |

The correct final performance evidence for this frozen v1 configuration includes the held-out result:

- accuracy: `0.7500`;
- macro F1: `0.7403`;
- failures: `9 / 36`.

---

## No post-test tuning

The held-out failures will not be used to modify and rerun Routing Benchmark v1.

The following actions are explicitly excluded from this evaluation cycle:

- adding rules for observed test failures;
- changing `C`;
- changing n-gram configuration;
- changing tokenization;
- adding character n-grams;
- modifying labels based on model behavior;
- adding the held-out cases to training;
- replacing the selected candidate after test exposure;
- rerunning the same held-out test after adapting the model.

The held-out result is evidence, not another development dataset.

---

## Future Routing v2 hypotheses

A future versioned routing experiment may investigate:

| Hypothesis | Motivation |
|---|---|
| Stronger domain-negative examples | Distinguish retailer ordering from unrelated food ordering |
| Additional semantic families | Improve coverage and estimate generalization more reliably |
| Hierarchical routing | First decide whether the message belongs to the retailer-support domain |
| Confidence/abstention mechanism | Route uncertain predictions to safe fallback/handoff |
| Alternative word or character features | Test robustness beyond current unigram representation |
| Embedding-based classifier | Test whether semantic representations improve PLATFORM/OTHER separation |
| Larger independent held-out set | Produce a stronger final generalization estimate |

These are future hypotheses only.

Routing v1 provides no authorization to tune against the existing held-out test.

A Routing v2 experiment must establish new development and independent evaluation boundaries.

---

## Evidence provenance

### Dataset

| Field | Value |
|---|---|
| Dataset | `routing-intent-v1` |
| Version | `1.0.0` |
| Status | `FROZEN` |
| Canonical LF SHA-256 | `369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450` |
| Train | 108 |
| Validation | 36 |
| Held-out test | 36 |

### Validation evidence

| Field | Value |
|---|---|
| Artifact | `experiments/routing/results/routing-benchmark-validation-v1.json` |
| SHA-256 | `615CC62703F466FFE9C75F016E3F8B8C6E743BDE661B0B70470DF0A0219D4B9F` |
| Validation runner freeze commit | `5d055b4` |
| Evidence preservation commit | `5e19899` |

### Operational evidence

| Field | Value |
|---|---|
| Artifact | `experiments/routing/results/routing-operational-evidence-v1.json` |
| SHA-256 | `5D3AA410BE54BB15BDBF4D2D23FD8C170488E633891CC6E52F76CCFDE070F96F` |
| Measurement freeze commit | `5a33421` |
| Evidence preservation commit | `c03c39f` |

### Candidate selection

| Field | Value |
|---|---|
| Decision | `ROUTING-SELECTION-V1` |
| Selected candidate | `C2-N1-C2.0` |
| Selection freeze commit | `fd47277` |
| Held-out test consulted during selection | No |

### Held-out evaluation

| Field | Value |
|---|---|
| Artifact | `experiments/routing/results/routing-held-out-test-v1.json` |
| SHA-256 | `FD93BFCDFB03ADC3C1D73F5B997DDEF58571B0EC590ED472F798C760CC867324` |
| Held-out runner freeze commit | `3edaa1c` |
| Raw evidence preservation commit | `8eca34b` |
| Configuration search during held-out evaluation | No |
| Validation used by held-out runner | No |
| Held-out test used | Yes |
| Held-out test record count | 36 |

---

## Final decision

**Routing Benchmark v1 is CLOSED.**

`C2-N1-C2.0` remains the selected v1 routing candidate because it was selected using legitimate pre-test evidence and materially outperformed the deterministic baseline.

However, its held-out macro F1 of `0.7403` establishes that the current routing implementation has meaningful generalization limitations.

The model will not be tuned against the existing test set.

Future routing improvements belong to a separately versioned Routing v2 evaluation cycle with new independent evaluation evidence.

Reliora development now proceeds to the runtime, policy-control, tool-execution, cloud-integration, observability, and product-experience layers.