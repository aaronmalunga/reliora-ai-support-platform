# Routing Candidate Selection Decision v1

## Decision metadata

| Field | Value |
|---|---|
| Decision ID | `ROUTING-SELECTION-V1` |
| Decision status | `SELECTED_FOR_HELD_OUT_TEST` |
| Evidence classification | `EXPERIMENTAL` |
| Selected candidate | `C2-N1-C2.0` |
| Feature representation | TF-IDF word unigrams |
| Classifier | Linear SVM (`LinearSVC`) |
| Regularization parameter | `C = 2.0` |
| Held-out test consulted during selection | No |

## Decision

Reliora selects `C2-N1-C2.0` as the routing configuration to advance to the final held-out test evaluation.

This decision was made using the frozen validation evidence, preserved failure cases, local operational measurements, determinism checks, and implementation-complexity considerations.

The held-out test split was not consulted when making this decision.

Selection does not yet constitute final generalization evidence. The selected configuration must still be evaluated once against the untouched held-out test split.

---

## Candidate comparison

| Candidate | Validation accuracy | Validation macro F1 | Validation failures | BUG recall | Deterministic | Local inference p50 / message | Local inference p95 / message |
|---|---:|---:|---:|---:|---|---:|---:|
| `B1` | 0.3889 | 0.2767 | 22 | 0.0833 | Yes | 0.0167 ms | 0.0307 ms |
| `C1-N1-C2.0` | 0.9444 | 0.9444 | 2 | 1.0000 | Yes | 0.1079 ms | 0.1563 ms |
| **`C2-N1-C2.0`** | **0.9722** | **0.9722** | **1** | **1.0000** | **Yes** | **0.1071 ms** | **0.1627 ms** |

Classical training-time measurements on the local benchmark environment were also small relative to the application lifecycle:

| Candidate | Training required | Local training p50 |
|---|---|---:|
| `B1` | No | N/A |
| `C1-N1-C2.0` | Yes | 21.0384 ms |
| `C2-N1-C2.0` | Yes | 6.7938 ms |

Training latency is secondary evidence because the benchmark dataset is small and training occurs outside the request-serving path.

---

## Validation behavior

### Selected candidate

`C2-N1-C2.0` correctly classified 35 of 36 validation records.

| Actual intent | Correct | Total | Recall |
|---|---:|---:|---:|
| BUG | 12 | 12 | 1.0000 |
| PLATFORM | 11 | 12 | 0.9167 |
| OTHER | 12 | 12 | 1.0000 |

Its only validation failure was:

| Case | Expected | Predicted | Message |
|---|---|---|---|
| `ROUTE-PLATFORM-012-C` | PLATFORM | OTHER | What is the normal refund processing time? |

This failure represents a valid platform-support request being sent toward the OTHER/fallback path.

It is undesirable because it can reduce successful self-service and increase escalation or support workload. However, the selected candidate produced no BUG routing failures and no OTHER-to-PLATFORM false positives on validation.

No numerical failure-severity score is assigned because the preregistered benchmark protocol did not define severity weights.

---

## Why B1 was rejected

The deterministic rule baseline achieved complete fit on the permitted training records during development but generalized poorly to unseen validation families.

| B1 evidence | Result |
|---|---:|
| Training records correctly classified after train-only rule development | 108 / 108 |
| Validation accuracy | 0.3889 |
| Validation macro F1 | 0.2767 |
| Validation failures | 22 / 36 |
| BUG recall | 0.0833 |
| PLATFORM recall | 0.0833 |
| OTHER recall | 1.0000 |

The validation failures included unseen concepts and paraphrases involving password-reset links, wishlist synchronization, notification links, gift cards, restocking, and refund timing.

This demonstrated that extending the lexical rule dictionary to fit known language did not provide sufficient semantic generalization.

The result supports replacing the expanding deterministic routing rules with a lightweight learned classifier.

---

## Why C1 was not selected

`C1-N1-C2.0` was a strong lightweight alternative.

It achieved:

- validation macro F1 of `0.9444`;
- perfect BUG recall;
- deterministic repeated predictions;
- sub-millisecond local inference in the benchmark environment.

However, it produced two validation failures rather than one.

In addition to the PLATFORM-to-OTHER refund-timing failure shared with C2, it incorrectly classified the unrelated query:

> How do I make creamy mushroom pasta?

as PLATFORM.

The operational latency difference between C1 and C2 was negligible for the application architecture:

| Metric | C1 | C2 | Difference |
|---|---:|---:|---:|
| Local p50 / message | 0.1079 ms | 0.1071 ms | 0.0008 ms |
| Local p95 / message | 0.1563 ms | 0.1627 ms | 0.0064 ms |

The approximately `0.0064 ms` p95 difference does not justify accepting weaker validation performance.

---

## Why C2 was selected

`C2-N1-C2.0` provides the strongest balance of observed generalization, failure behavior, determinism, and operational simplicity.

| Decision dimension | Evidence | Conclusion |
|---|---|---|
| Primary metric | Highest validation macro F1: `0.9722` | Favors C2 |
| Validation failures | 1 / 36 | Favors C2 |
| BUG handling | 12 / 12 correct | Favors C2 |
| OTHER handling | 12 / 12 correct | Favors C2 |
| Determinism | Stable across 100 repetitions | Acceptable |
| Local inference latency | p95 `0.1627 ms/message` | Operationally negligible locally |
| Training requirement | Yes | Acceptable |
| External ML dependency | scikit-learn | Acceptable |
| Rule maintenance burden | Lower than expanding B1 lexical rules | Favors C2 |
| Architecture complexity | TF-IDF + linear classifier | Proportionate to demonstrated need |

The experiment therefore provides evidence for introducing a lightweight machine-learning routing component without escalating to embeddings, transformer fine-tuning, or an LLM router.

Those more complex approaches remain unjustified unless future evidence demonstrates a requirement that the selected classical model cannot satisfy.

---

## Latency interpretation

The operational benchmark measured local, in-process routing performance.

The measurement:

- used 12 synthetic operational probe messages;
- performed 25 warm-up runs;
- performed 500 measured runs;
- used `time.perf_counter_ns`;
- divided batch execution latency by the number of probe messages when reporting per-message values.

Therefore, the reported values are local batch-normalized inference measurements.

They are not end-to-end production API latency measurements.

The measurements exclude:

- network latency;
- AWS service latency;
- API serialization and deserialization;
- Lambda or container cold starts;
- queueing;
- telemetry transport;
- Bedrock invocation;
- AgentCore invocation;
- tool calls;
- downstream service latency.

End-to-end latency must be measured separately after cloud deployment.

---

## Complexity decision

The faster runtime of B1 does not compensate for its validation generalization failure.

The additional local processing time associated with C2 is small in absolute terms and is expected to be minor relative to the complete cloud request path.

The selected architecture therefore applies the principle:

> Introduce additional technology only when evidence shows that it solves a documented problem or limitation.

The learned router is justified here because the deterministic baseline demonstrated insufficient generalization.

The evidence does not currently justify a more complex neural or LLM-based router.

---

## Evidence provenance

### Validation evidence

| Field | Value |
|---|---|
| Artifact | `experiments/routing/results/routing-benchmark-validation-v1.json` |
| Artifact SHA-256 | `615CC62703F466FFE9C75F016E3F8B8C6E743BDE661B0B70470DF0A0219D4B9F` |
| Benchmark machinery freeze commit | `5d055b40a3d8f75def5dab0870c73f1331c355fe` |
| Evidence preservation commit | `5e19899` |
| Dataset | `routing-intent-v1` |
| Dataset version | `1.0.0` |
| Dataset status | `FROZEN` |
| Dataset canonical LF SHA-256 | `369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450` |
| Training records | 108 |
| Validation records | 36 |
| Held-out test used | No |

### Operational evidence

| Field | Value |
|---|---|
| Artifact | `experiments/routing/results/routing-operational-evidence-v1.json` |
| Artifact SHA-256 | `5D3AA410BE54BB15BDBF4D2D23FD8C170488E633891CC6E52F76CCFDE070F96F` |
| Measurement machinery freeze commit | `5a33421` |
| Evidence preservation commit | `c03c39f` |
| Validation split used | No |
| Held-out test used | No |
| Synthetic operational probes | 12 |
| Warm-up runs | 25 |
| Measurement runs | 500 |
| Determinism repetitions | 100 |

---

## Held-out test firewall

At the time this selection decision was made:

- the held-out test labels had not been used for model development;
- the held-out test had not been used for hyperparameter selection;
- the held-out test had not been used for failure analysis;
- the held-out test had not been used for latency measurement;
- the selected candidate was fixed using training, validation, and synthetic operational evidence only.

The next evaluation step is therefore a single held-out test evaluation of the selected `C2-N1-C2.0` configuration.

The held-out test result is evidence.

A disappointing result will not authorize retrospective tuning against the test set.

Any future model revision must create a new explicitly versioned development and evaluation cycle.