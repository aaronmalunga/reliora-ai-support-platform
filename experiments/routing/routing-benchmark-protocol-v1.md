# Routing Benchmark Protocol v1

## Status

```text
protocol ID: routing-benchmark-protocol-v1
status: PRE-REGISTERED
benchmark dataset: routing-intent-v1
dataset lifecycle state: FROZEN
model benchmarking: NOT STARTED
evidence class for benchmark results: EXPERIMENTAL
```

This protocol defines the first controlled comparison of routing
alternatives for Reliora.

It is recorded before candidate training or model-result inspection so
that model-selection criteria are not chosen retrospectively.

---

# 1. Decision Being Evaluated

Reliora requires a top-level routing decision with exactly one of:

```text
BUG
PLATFORM
OTHER
```

This benchmark evaluates candidate implementations for that routing
decision.

It does not evaluate the separate PLATFORM knowledge-coverage decision.

The routing and knowledge-coverage decisions must remain separate.

---

# 2. Architectural Question

The experiment asks:

> What is the simplest routing implementation that provides strong,
> balanced classification quality while remaining operationally
> appropriate for Reliora?

The benchmark is therefore an architecture-selection experiment, not
an algorithm leaderboard.

---

# 3. Candidate Set

The first benchmark evaluates exactly four candidate strategies.

## B0 — Majority-Class Baseline

Purpose:

> Establish a trivial classification floor.

The candidate predicts the majority class observed in the training
split.

The frozen training dataset is balanced, so any deterministic tie
resolution used by this baseline must be documented in benchmark
evidence.

---

## B1 — Deterministic Keyword/Rule Baseline

Purpose:

> Determine how far a transparent, deterministic routing strategy can
> go before statistical classification is justified.

The rule set must:

- use only the customer-message field;
- be versioned with the benchmark implementation;
- return exactly one allowed routing label;
- use deterministic precedence when more than one rule matches;
- provide a deterministic fallback;
- remain unchanged after final validation-based candidate selection
  begins unless the benchmark protocol is versioned.

Rule design may use the training split and documented routing contract.

The held-out test split must not be used to develop or repair rules.

---

## C1 — TF-IDF + Logistic Regression

Purpose:

> Evaluate a lightweight and interpretable statistical text classifier.

The candidate uses:

```text
TF-IDF text representation
+
Logistic Regression classifier
```

Hyperparameters and preprocessing must be recorded in experiment
evidence.

Training data may be used for fitting.

Validation data may be used for model/configuration selection.

The held-out test split must not be used for fitting or configuration
selection.

---

## C2 — TF-IDF + Linear SVM

Purpose:

> Evaluate a strong classical sparse-text classifier as an alternative
> to Logistic Regression.

The candidate uses:

```text
TF-IDF text representation
+
Linear Support Vector Machine classifier
```

Hyperparameters and preprocessing must be recorded in experiment
evidence.

Training data may be used for fitting.

Validation data may be used for model/configuration selection.

The held-out test split must not be used for fitting or configuration
selection.

---

# 4. Candidates Explicitly Out of Scope for v1

The following are not part of this benchmark version:

- Naive Bayes;
- embedding-based classifiers;
- neural classifiers;
- hosted LLM routing;
- Bedrock prompt-based routing;
- fine-tuned foundation models;
- additional ensemble models.

These may become separate experiments only if justified by evidence or
new requirements.

They must not be added merely to increase the number of algorithms
tested.

---

# 5. Frozen Dataset Identity

The benchmark uses:

```text
dataset:
routing-intent-v1.json

dataset canonical SHA-256:
369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450
```

Family manifest:

```text
routing-intent-v1-families.json

family-manifest canonical SHA-256:
93d07598b846c2df3490f39b68971b2ae2a5dba872fb149e513f592c0d5724a1
```

Hash basis:

```text
SHA-256 over file bytes with line endings normalized to LF
```

Frozen dataset Git commit:

```text
4c86dae270046e3d4372f41941b56de3101fcdc9
```

The frozen dataset and family-manifest hashes were independently
verified from that Git commit before model benchmarking began.

---

# 6. Dataset Structure

The frozen benchmark contains:

```text
180 records
45 semantic families
4 variants per family

BUG       60
PLATFORM  60
OTHER     60
```

Split distribution:

```text
train       108 records / 27 families
validation   36 records /  9 families
test         36 records /  9 families
```

Semantic families, not individual paraphrases, are the split unit.

This is intended to reduce paraphrase leakage across train,
validation, and test data.

---

# 7. Allowed Model Input

Candidate implementations may consume only:

```text
customer message
```

as model/routing input.

They must not use:

- expected labels;
- family IDs;
- case IDs;
- split labels;
- variant IDs;
- provenance metadata;
- review metadata;
- any other information unavailable from the customer request at
  inference time.

Metadata may be used for evaluation and evidence generation only.

---

# 8. Split Discipline

The benchmark uses the following interpretation:

```text
TRAIN
→ fit or construct candidates

VALIDATION
→ compare and select configurations

TEST
→ final independent evaluation
```

The held-out test set is:

```text
CLOSED TO MODEL-DRIVEN EDITING
```

Test examples must not be repeatedly inspected, rewritten, or used to
tune candidate behaviour in response to model errors.

A genuine post-freeze ground-truth defect requires explicit dataset
change control and versioning.

---

# 9. Candidate Development Discipline

Candidate configuration work must use only:

```text
training data
+
validation evidence
```

The final candidate/configuration must be fixed before held-out test
evaluation.

Once test evaluation begins, poor test performance is evidence about
the selected implementation.

It is not permission to rewrite the frozen test set or tune the selected
candidate against test failures.

---

# 10. Quality Metrics

Every candidate must report, where applicable:

```text
accuracy
macro precision
macro recall
macro F1
per-class precision
per-class recall
per-class F1
confusion matrix
```

Macro F1 is the primary aggregate classification-quality metric because
BUG, PLATFORM, and OTHER are operationally distinct and should receive
equal weight in the aggregate score.

Accuracy alone must not determine the preferred candidate.

---

# 11. Failure Analysis

Candidate comparison must inspect confusion patterns, not only aggregate
scores.

Particular attention should be paid to errors such as:

```text
BUG → PLATFORM
BUG → OTHER
OTHER → BUG
OTHER → PLATFORM
```

and other confusion patterns that could create inappropriate downstream
behaviour.

The benchmark evidence must preserve actual failures rather than
removing difficult cases from the report.

---

# 12. No Pre-Declared Numerical Quality Pass Threshold

No numerical macro-F1, per-class, accuracy, or recall threshold is
declared for this first benchmark.

The first experiment establishes:

```text
baseline evidence
+
candidate comparison evidence
```

It must not retroactively define a numerical quality target because a
measured result appears attractive.

Any future release threshold must be introduced explicitly and
prospectively using benchmark evidence and operational requirements.

---

# 13. Candidate Selection Rule

Candidate selection must consider:

```text
macro F1
per-class precision / recall / F1
confusion patterns
failure severity
latency
determinism
operational complexity
runtime dependencies
training characteristics
model size where applicable
cost where measurable
```

The preferred candidate must not be selected solely because it has the
highest accuracy.

The primary classification comparison is validation macro F1.

However, a candidate with a slightly stronger aggregate metric may be
rejected if its per-class behaviour or failure modes are materially
worse for Reliora's routing contract.

When candidates provide effectively equivalent classification evidence,
the simpler and more deterministic operational architecture should be
preferred.

The rationale must be documented rather than inferred from the final
score.

---

# 14. Test Evaluation Rule

The held-out test set is evaluated only after the preferred
configuration has been fixed using training and validation evidence.

The test result provides independent evidence about that selected
configuration.

Test results do not retroactively alter candidate-selection criteria.

---

# 15. Latency Measurement

Local prediction latency must be measured for each candidate where
meaningful.

The evidence must record:

```text
hardware / environment
operating system
Python version
relevant library versions
number of measured predictions or runs
warm-up behaviour where applicable
timing method
mean latency
median latency
p95 latency
```

Timing should use a high-resolution monotonic performance timer such as:

```text
time.perf_counter_ns()
```

where practical.

The benchmark should separate model fitting/training time from
prediction latency.

---

# 16. Latency Interpretation

This first experiment establishes a repeatable local baseline.

It does not establish production latency.

No production latency SLO or SLA may be inferred solely from this local
benchmark.

Numerical production targets require later operational evidence.

---

# 17. Training and Runtime Cost Dimensions

Where applicable, evidence should distinguish:

```text
training time
model size
local prediction cost
external API cost
runtime dependency cost
```

For the initial local classical benchmark:

```text
external inference API cost:
not applicable
```

unless a future protocol version introduces a hosted candidate.

---

# 18. Determinism

The benchmark should record whether repeated inference using the same
candidate version and identical input produces the same routing result.

The majority baseline, deterministic rule baseline, Logistic Regression,
and Linear SVM candidates are expected to provide deterministic
prediction under a fixed trained artifact/configuration.

This expectation must still be verified rather than merely assumed.

---

# 19. Reproducibility Evidence

Experiment evidence must identify at least:

```text
protocol ID
dataset ID
dataset version
dataset canonical SHA-256
family-manifest canonical SHA-256
dataset freeze Git revision
benchmark implementation Git revision
Python version
library versions
candidate configuration
split usage
metric results
confusion matrix
latency methodology
latency results
experiment timestamp
evidence classification
```

---

# 20. Evidence Classification

The resulting benchmark evidence is:

```text
EXPERIMENTAL
```

It represents controlled local evaluation against a synthetic frozen
benchmark.

It does not constitute:

- production traffic evidence;
- production latency evidence;
- customer outcome evidence;
- production reliability evidence;
- production prevalence evidence.

---

# 21. Benchmark Evidence Must Preserve Failures

Generated evidence must not be manually cleaned to remove
misclassifications.

Failure cases are part of the experiment result.

The benchmark implementation should make it possible to identify:

```text
case ID
expected intent
predicted intent
candidate
split
```

for misclassified records.

This supports later error analysis without modifying the underlying
benchmark.

---

# 22. Result Interpretation

The first benchmark may support a statement such as:

> Candidate X is currently preferred for Reliora's top-level routing
> decision under routing-benchmark-protocol-v1 because it provided the
> strongest overall balance of validation classification quality,
> failure behaviour, latency, determinism, dependencies, and operational
> complexity.

It must not automatically support:

> Candidate X is production-ready.

---

# 23. ADR-012 Relationship

ADR-012 remains:

```text
PROPOSED
```

until benchmark evidence has been generated and reviewed.

The benchmark result will inform whether ADR-012 can record a preferred
routing architecture.

The architecture decision must follow the evidence.

The evidence must not be rewritten to fit a preferred architecture.

---

# 24. Protocol Change Control

After candidate-result inspection begins, changes to:

- candidate set;
- primary metrics;
- split discipline;
- selection rules;
- test-use rules;
- latency methodology;
- frozen dataset identity;

must not be silently incorporated into this protocol.

A material change requires:

```text
new protocol version
+
documented rationale
```

This prevents experiment criteria from changing in response to observed
results.

---

# 25. Execution Order

The first routing benchmark must proceed in this order:

```text
1. freeze benchmark dataset                         COMPLETE
2. record canonical identities                     COMPLETE
3. record frozen Git provenance                    COMPLETE
4. independently verify frozen committed artifacts COMPLETE
5. pre-register benchmark protocol
6. implement majority baseline
7. implement deterministic rule baseline
8. add justified experiment-only ML dependency
9. implement TF-IDF + Logistic Regression
10. implement TF-IDF + Linear SVM
11. validate benchmark implementation
12. evaluate candidates using train/validation discipline
13. fix preferred candidate configuration
14. evaluate selected configuration on held-out test
15. record reproducible evidence
16. review failure patterns
17. measure and record local latency baseline
18. update ADR-012 from generated evidence
```

At the time this protocol is created:

```text
candidate-model result inspection: NOT STARTED
held-out test model evaluation: NOT STARTED
```

---

# Core Principle

> Pre-register how the evidence will be judged before seeing the
> evidence.

Reliora should select its routing architecture because the controlled
experiment supports the decision, not because a preferred architecture
was chosen in advance.