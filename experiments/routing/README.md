# Reliora Routing Benchmark

## Purpose

This directory contains the controlled experiments used to evaluate candidate routing strategies for Reliora.

The routing benchmark exists to support an evidence-based architecture decision rather than selecting a router based on preference, implementation novelty, or assumed cost.

The central question is:

> Which routing approach provides the strongest evidence-supported balance of intent-classification quality, deterministic behaviour, latency, implementation complexity, and operational suitability for Reliora's top-level customer-request routing?

The benchmark evaluates **top-level intent classification only**.

The allowed intents are:

```text
BUG
PLATFORM
OTHER
```

Knowledge-coverage classification is deliberately outside this benchmark.

---

# 1. Requirements Traceability

The experiment is derived from Reliora's documented functional and non-functional requirements.

## FR-004 — Intent Classification

Every accepted customer message must be classified into exactly one top-level intent:

```text
BUG
PLATFORM
OTHER
```

Routing results must use a machine-verifiable contract rather than relying solely on free-form text.

Therefore the benchmark evaluates a **single-label, three-class classification problem**.

---

## FR-005 — Knowledge Coverage Classification

A request classified as:

```text
PLATFORM
```

must undergo a separate knowledge-coverage decision:

```text
SUPPORTED
UNSUPPORTED
```

Intent classification and knowledge coverage must remain logically distinct.

Therefore this benchmark must **not** introduce combined labels such as:

```text
PLATFORM_SUPPORTED
PLATFORM_UNSUPPORTED
```

Doing so would collapse two separate architectural decisions into one classifier.

---

## FR-006 — Unsupported Request Handling

Requests classified as:

```text
OTHER
```

eventually transition toward the human-handoff workflow.

Unsupported PLATFORM requests also transition toward human handoff, but only after the separate knowledge-coverage decision.

Therefore a routing error can affect downstream workflow selection and is not merely a cosmetic classification mistake.

---

# 2. Architecture Decision Traceability

## ADR-002

Reliora separates:

```text
intent classification
```

from:

```text
knowledge-coverage classification
```

The routing benchmark must preserve this separation.

---

## ADR-012

Reliora must benchmark routing alternatives before selecting the production routing strategy.

Therefore:

```text
candidate implementation
        ≠
selected architecture
```

A candidate becomes preferred only after evidence has been generated and reviewed.

---

# 3. Non-Functional Requirements

## NFR-PERF-001 — Baseline Before Target

Latency, throughput, and concurrency targets must be established only after a repeatable baseline measurement exists.

Therefore the first routing benchmark will:

```text
measure latency
record measurement methodology
record environment information
```

but will not claim that a production latency objective has already been achieved.

---

## NFR-GOV-001 — Evidence Classification

Routing benchmark results are classified as:

```text
EXPERIMENTAL
```

unless stronger evidence is explicitly established.

---

## NFR-GOV-003 — Versioned Release Evidence

Evidence should retain enough provenance to identify the relevant:

```text
application version
routing implementation
dataset version
configuration
model where applicable
```

This allows future results to be reproduced and compared.

---

# 4. Prediction Contract

The logical prediction contract for the Phase 5 router is:

```text
customer message
      ↓
exactly one intent
      ↓
BUG | PLATFORM | OTHER
```

A candidate implementation may internally calculate:

```text
scores
probabilities
decision margins
feature vectors
```

but its accepted routing result must resolve to exactly one top-level intent.

A future typed runtime contract may contain fields such as:

```json
{
  "intent": "BUG",
  "router_version": "..."
}
```

Additional metadata must not change the one-intent requirement.

---

# 5. Intent Definitions

The benchmark requires stable label semantics.

## BUG

Use `BUG` when the customer is reporting behaviour that appears to represent a technical defect or malfunction requiring the bug-report workflow.

Examples include:

```text
the checkout page crashes
the application freezes
a button does not work
an error appears during a supported workflow
```

The defining characteristic is that the customer is reporting an apparent technical problem.

---

## PLATFORM

Use `PLATFORM` when the customer is asking for information about the supported platform, product behaviour, policies, or services.

Examples include:

```text
What is the return policy?
How long does delivery take?
Can I change my shipping address?
Do you offer a particular supported service?
```

`PLATFORM` does not imply that Reliora necessarily knows the answer.

After this classification, a separate knowledge-coverage decision determines:

```text
SUPPORTED
or
UNSUPPORTED
```

---

## OTHER

Use `OTHER` when the request is neither:

```text
a technical bug report
nor
a platform-information request
```

Examples may include:

```text
unrelated requests
requests outside the platform domain
requests requiring unsupported human assistance
```

`OTHER` should not be used as a substitute for uncertain PLATFORM knowledge coverage.

That distinction is important:

```text
platform question that Reliora cannot answer
→ PLATFORM

then
→ UNSUPPORTED knowledge coverage

not
→ OTHER
```

---

# 6. Experiment Scope

## In Scope

Phase 5 evaluates:

```text
top-level intent classification
BUG / PLATFORM / OTHER

candidate routing algorithms

classification quality

per-class behaviour

confusion patterns

local inference latency

prediction determinism where applicable

implementation complexity

model/configuration provenance
```

---

## Out of Scope

Phase 5 does not evaluate:

```text
SUPPORTED / UNSUPPORTED knowledge coverage

RAG retrieval quality

bug-field collection

tool authorization

ticket creation

idempotency

human-handoff execution

Bedrock response quality

full customer-support conversations

production traffic

production concurrency

production availability
```

These concerns belong to other Reliora components and evaluation layers.

---

# 7. Why Benchmark Multiple Routing Approaches?

A large language model is not automatically the best component for every AI-system decision.

Top-level routing has several properties that may make smaller approaches attractive:

```text
small fixed label set
structured output
high repeatability requirement
frequent execution
clear evaluation metric
```

A lightweight router may potentially provide advantages in:

```text
latency
cost
determinism
testability
operational simplicity
```

However, those advantages must be measured rather than assumed.

Likewise, a simpler router may have insufficient semantic capability.

The experiment therefore compares alternatives before the runtime architecture is selected.

---

# 8. Candidate Families

The benchmark should begin with deliberately simple baselines before more complex alternatives.

Candidate families may include:

```text
1. deterministic / heuristic baseline

2. classical text-classification baseline

3. additional classical ML alternatives

4. optional LLM-based routing comparison
```

The exact candidate set will be versioned with the experiment.

A more complex candidate should not be preferred merely because it is more sophisticated.

---

# 9. Baseline Philosophy

Every benchmark needs a baseline.

Without one, statements such as:

```text
the model performed well
```

have little comparative meaning.

A simple baseline provides a minimum reference point.

Possible baseline forms may include:

```text
majority-class prediction
simple keyword/rule routing
```

The chosen baseline must be documented explicitly.

---

# 10. Classical ML Benchmark

A classical text-classification experiment may evaluate combinations such as:

```text
TF-IDF
    +
Logistic Regression
```

and other justified alternatives.

The purpose is not to maximize the number of algorithms tested.

The purpose is to answer:

> Can an inexpensive and operationally simple classifier meet Reliora's routing-quality requirements?

Candidate models should therefore be selected because they represent meaningful architectural alternatives.

---

# 11. Dataset Requirements

The routing dataset must be versioned.

Each example should contain enough information to identify at least:

```text
case ID
customer message
expected intent
dataset split or split assignment mechanism
fixture provenance/type
```

Additional metadata may be added when justified.

---

# 12. Dataset Provenance

Dataset examples must not be represented as real production traffic unless they actually originate from verified production data.

Designed examples should be labelled appropriately.

For example:

```text
SYNTHETIC ASSUMPTION
```

may describe deliberately constructed customer-request fixtures.

Benchmark execution results produced from those fixtures may then constitute:

```text
EXPERIMENTAL
```

evidence.

The evidence class of the execution does not change the provenance of the underlying input examples.

---

# 13. Dataset Design Principles

The benchmark should contain more than trivial keyword examples.

Cases should eventually include variation such as:

```text
direct statements
short messages
long messages
informal wording
typos
paraphrases
ambiguous phrasing
multiple symptoms
questions containing technical vocabulary
bug reports phrased as questions
platform questions mentioning errors
unrelated requests using platform terminology
```

This reduces the risk of evaluating only easy cases.

---

# 14. Class Balance

Dataset composition must be reported explicitly.

At minimum, evidence should record:

```text
total examples
BUG examples
PLATFORM examples
OTHER examples
```

Overall accuracy must not be interpreted without considering class distribution.

A model that predicts the largest class frequently may achieve misleading aggregate accuracy on an imbalanced dataset.

---

# 15. Data Leakage Controls

Train/test leakage would make benchmark results unreliable.

The experiment must guard against examples where near-identical wording appears across training and test sets.

Examples of risky leakage include:

```text
Training:
"The checkout page crashes when I press Pay."

Test:
"Checkout crashes when I click Pay."
```

These examples may represent the same underlying template.

A random row-level split alone may therefore be insufficient if the dataset contains generated paraphrase families.

---

# 16. Semantic Families

Where multiple examples originate from the same scenario or template, they should be associated with a common semantic family where practical.

Conceptually:

```text
family:
checkout-crash

examples:
- checkout crashes when Pay is clicked
- payment screen closes when I press Pay
- app freezes at checkout
```

Family-aware splitting helps prevent closely related paraphrases from appearing on opposite sides of the evaluation boundary.

---

# 17. Split Strategy

The version 1 routing dataset uses **semantic-family-aware splitting**.

Individual message variants are not independently randomized across
splits. Instead, the semantic family is the split unit.

This prevents paraphrases describing the same underlying scenario from
appearing on opposite sides of an evaluation boundary.

The frozen version 1 split contains:

```text
semantic families: 45

train families: 27
validation families: 9
test families: 9

train records: 108
validation records: 36
test records: 36
```

Each intent contributes:

```text
9 train families
3 validation families
3 test families
```

Because each semantic family contains four message variants, each intent
therefore contributes:

```text
36 train records
12 validation records
12 test records
```

The held-out test families were assigned before routing-model
benchmarking and were manually reviewed before dataset freeze.

The test set is now:

```text
CLOSED TO MODEL-DRIVEN EDITING
```

It must not be repeatedly inspected or rewritten in response to model
errors.

A genuine ground-truth defect may still be corrected through explicit
dataset change control and versioning.

This split discipline is intended to reduce paraphrase leakage and
preserve the test set as independent evidence.

---

# 18. Metrics

No single metric is sufficient.

The core classification metrics should include:

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

---

# 19. Why Macro F1 Matters

Macro F1 calculates performance for each class and then gives each class equal importance.

This is useful because Reliora has three operationally distinct intents:

```text
BUG
PLATFORM
OTHER
```

Strong performance on one common class should not hide poor performance on another.

---

# 20. Why Per-Class Recall Matters

Per-class recall answers:

> Of all examples that truly belonged to this class, how many did the router correctly identify?

This is especially useful for identifying failure modes such as:

```text
BUG messages incorrectly routed as PLATFORM
```

or:

```text
OTHER messages incorrectly kept inside an autonomous workflow
```

Aggregate metrics could hide those failures.

---

# 21. Confusion Matrix

The benchmark must preserve a confusion matrix.

The matrix answers questions such as:

```text
Which class is most commonly confused with BUG?

Are PLATFORM messages being sent to OTHER?

Does the classifier over-predict one class?
```

These patterns may matter more architecturally than a small difference in overall accuracy.

---

# 22. Error Analysis

Benchmarking does not stop at a score.

Misclassified cases should be reviewed and grouped by failure pattern.

Potential categories include:

```text
ambiguous wording
multi-intent wording
insufficient context
lexical overlap
unseen vocabulary
short-message ambiguity
label-definition ambiguity
```

This analysis can reveal whether the problem is caused primarily by:

```text
the model
the dataset
the taxonomy
the labeling policy
```

---

# 23. Latency Measurement

The experiment should measure local prediction latency for each candidate where meaningful.

The methodology must state:

```text
hardware/environment
Python version
library versions
number of measured predictions or runs
warm-up behaviour where applicable
timing method
reported statistic
```

Potential statistics include:

```text
mean
median
p95
```

The first benchmark establishes a repeatable baseline.

It does not prove production latency.

---

# 24. Training Cost vs Inference Cost

Where applicable, benchmark evidence should distinguish:

```text
training time
model size
inference latency
external API cost
```

A model that takes longer to train may still be cheap to operate.

Conversely, an externally hosted generative router may require little local training but incur per-request inference cost.

These are different cost dimensions.

---

# 25. Determinism

Where meaningful, the benchmark should record whether repeated evaluation of the same input and versioned configuration returns the same routing result.

Classical deterministic inference may naturally provide strong repeatability.

Generative routing may require additional controls.

Determinism alone does not establish classification quality, but it is an operational property worth recording.

---

# 26. Reproducibility

A benchmark result should identify enough configuration to reproduce the experiment.

Where applicable, record:

```text
dataset ID
dataset version
dataset hash
split configuration
random seed
feature configuration
model type
model hyperparameters
software/library versions
Git commit
```

---

# 27. Evidence Classification

Dataset fixtures and benchmark results must use Reliora's evidence taxonomy accurately.

Examples:

```text
designed synthetic customer message
→ SYNTHETIC ASSUMPTION

result from executing the benchmark
→ EXPERIMENTAL

measured local inference latency
→ EXPERIMENTAL benchmark measurement
```

A local experiment must not be presented as evidence of real production traffic behaviour.

---

# 28. Numerical Targets

Reliora currently requires baseline measurement before establishing latency, throughput, concurrency, and related operational targets.

Therefore Phase 5 must not retroactively choose latency targets merely because a measured result appears attractive.

Classification-quality acceptance criteria must also be documented before using them as release claims.

Initial benchmark results should therefore be interpreted as:

```text
baseline evidence
+
candidate comparison
```

not automatically as proof of production readiness.

---

# 29. Candidate Selection Rule

The preferred router should not be selected solely by highest accuracy.

The decision should consider:

```text
macro F1
per-class behaviour
confusion patterns
failure severity
latency
determinism
operational complexity
runtime dependencies
cost where measurable
```

A statistically small quality improvement may not justify a substantially more complex or expensive runtime architecture.

Conversely, a simpler model should not be selected if its errors violate important routing requirements.

---

# 30. No Premature Production Decision

The benchmark may conclude:

```text
candidate A is currently preferred
```

without concluding:

```text
candidate A is production-ready
```

Production suitability additionally depends on:

```text
integration testing
failure handling
observability
security
deployment behaviour
realistic workload evidence
```

which extend beyond this benchmark.

---

# 31. Current Directory Structure

The routing experiment currently contains:

```text
experiments/
└── routing/
    ├── README.md
    │
    ├── data/
    │   ├── routing-intent-v1-card.md
    │   ├── routing-intent-v1-families.json
    │   ├── routing-intent-v1-methodology.md
    │   ├── routing-intent-v1-review-log.md
    │   └── routing-intent-v1.json
    │
    ├── scripts/
    │   ├── audit_routing_dataset.py
    │   └── validate_routing_data.py
    │
    └── results/
        └── routing-intent-v1-audit.json
```

This structure separates:

```text
experiment documentation
dataset artifacts
executable validation and audit tooling
generated experimental evidence
```

Routing-model training and benchmark-execution artifacts have not yet
been added because model benchmarking has not started.

---

# 32. Directory and Artifact Responsibilities

## `README.md`

Defines the routing experiment itself, including:

- requirements and ADR traceability;
- routing-label semantics;
- experiment scope;
- candidate-selection philosophy;
- evaluation metrics;
- evidence and reproducibility rules;
- dataset governance;
- experiment lifecycle and current status.

It explains **why the routing benchmark exists and how it is governed**.

---

## `data/`

Contains versioned benchmark inputs and the documentation required to
interpret them.

### `routing-intent-v1.json`

The executable routing benchmark dataset.

It contains:

```text
180 message records
45 semantic families
3 routing intents
train / validation / test assignments
4 variants per semantic family
```

The dataset content is currently `FROZEN`.

### `routing-intent-v1-families.json`

The semantic-family manifest.

It defines the 45 semantic families, their expected routing labels, and
their fixed split assignments.

The manifest is currently `FROZEN`.

### `routing-intent-v1-card.md`

Documents the dataset's purpose, scope, taxonomy, composition,
provenance, split design, claim boundaries, lifecycle, and current
identity state.

### `routing-intent-v1-methodology.md`

Documents how the dataset was designed, generated, partitioned,
validated, audited, reviewed, curated, frozen, and governed.

It also records the limitations of the synthetic benchmark and the
rules for post-freeze change control.

### `routing-intent-v1-review-log.md`

Preserves the human-review history and curation decisions made before
model benchmarking.

It records:

```text
pre-freeze review findings
targeted message revisions
post-curation audit findings
held-out test-set semantic review
freeze decision
remaining evidence-finalization work
```

The review log preserves historical states rather than rewriting them
to make the entire development process appear frozen from the start.

---

## `scripts/`

Contains executable experiment-support tooling.

### `validate_routing_data.py`

Enforces hard structural and lifecycle contracts for the routing
dataset and semantic-family manifest.

Examples include:

```text
required metadata
allowed labels
allowed splits
allowed variants
record counts
family counts
unique case IDs
family membership
label consistency
split consistency
four variants per family
expected class and split distributions
```

A validator failure indicates that a documented dataset contract has
been violated.

### `audit_routing_dataset.py`

Performs diagnostic dataset-quality analysis that requires engineering
interpretation rather than automatic rejection.

The audit currently examines:

```text
cross-split lexical similarity
Jaccard token-set similarity
character-sequence similarity
class-associated tokens
semantic-family token frequency
boundary-term distribution
message-length distribution
```

An audit finding is not automatically a defect.

The validator and audit are deliberately separate because:

```text
validator
→ enforces hard contracts

audit
→ surfaces quality risks for review
```

Future model-training and benchmark-execution scripts will be added
only when the frozen dataset evidence package is complete.

Reusable application runtime code belongs under:

```text
src/reliora/
```

rather than being permanently embedded in experiment scripts.

---

## `results/`

Contains generated experimental evidence rather than hand-authored
dataset documentation.

### `routing-intent-v1-audit.json`

Contains the machine-readable output produced by
`audit_routing_dataset.py`.

Its current evidence class is:

```text
EXPERIMENTAL
```

The audit result describes properties observed in the controlled
synthetic benchmark.

It does not constitute production-traffic or production-performance
evidence.

Additional benchmark outputs may later include:

```text
candidate metrics
per-class metrics
confusion matrices
latency measurements
model-comparison summaries
error-analysis artifacts
```

Those artifacts do not exist yet and must not be implied as completed
work.

---

# 33. Relationship to Runtime Code

The experiment may identify a preferred routing strategy.

That does not mean the experiment script itself becomes production runtime code.

The progression should be:

```text
experiment candidate
        ↓
evidence
        ↓
architecture decision
        ↓
production implementation boundary
        ↓
runtime tests
```

This prevents experimental orchestration and runtime application logic from becoming unnecessarily coupled.

---

# 34. Relationship to Reliora Evaluation

The routing benchmark evaluates model-selection and classification behaviour.

Reliora's deterministic evaluation framework evaluates behavioural contracts.

These systems are related but not identical.

For example:

```text
routing benchmark
→ How accurately does classifier A distinguish BUG / PLATFORM / OTHER?

deterministic invariant
→ Did the runtime emit exactly one allowed intent?
```

Both forms of evidence are needed.

---

# 35. Experiment Lifecycle

The routing experiment follows a staged lifecycle so that dataset
design, model development, held-out evaluation, and architecture
selection remain distinguishable.

Current lifecycle:

```text
1. define routing contract                         COMPLETE
2. design semantic-family benchmark                COMPLETE
3. validate labels and provenance                  COMPLETE
4. perform diagnostic dataset audit                COMPLETE
5. complete human semantic review                  COMPLETE
6. freeze dataset and family manifest              COMPLETE
7. close held-out test set to model-driven editing COMPLETE
8. record frozen Git provenance                    IN PROGRESS
9. establish simple routing baseline               NOT STARTED
10. train candidate classifiers                    NOT STARTED
11. select candidate using train/validation data   NOT STARTED
12. evaluate selected configuration on held-out test data
                                                   NOT STARTED
13. analyze confusion and failure patterns         NOT STARTED
14. measure repeatable local latency               NOT STARTED
15. generate versioned benchmark evidence          NOT STARTED
16. review experimental evidence                   NOT STARTED
17. update ADR-012                                  NOT STARTED
18. select or reject routing strategy              NOT STARTED
19. promote chosen strategy into runtime design    NOT STARTED
```

The lifecycle deliberately freezes benchmark content before model
training begins.

This prevents routing-model results from influencing the held-out test
data used to evaluate those models.

The next lifecycle gate is completion of the frozen dataset evidence
package by committing the freeze milestone and recording its Git
provenance.

The canonical SHA-256 hashes have already been calculated and recorded.

---

# 36. Current Status

Current routing-experiment state:

```text
experiment specification: COMPLETE

dataset ID: routing-intent-v1
dataset version: 1.0.0

semantic families: 45
dataset records: 180

family manifest: FROZEN
dataset content: FROZEN
human semantic review: COMPLETE
held-out test families reviewed: 9 / 9
held-out test records accepted: 36 / 36
test set: CLOSED TO MODEL-DRIVEN EDITING

structural validation: PASS
cross-split near-duplicate findings: 0
strongly class-associated token findings: 31
cross-family class-associated token findings: 23

dataset SHA-256:
369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450

family-manifest SHA-256:
93d07598b846c2df3490f39b68971b2ae2a5dba872fb149e513f592c0d5724a1

canonical hashes: RECORDED
hash basis: file bytes with line endings normalized to LF
associated frozen Git revision: PENDING

routing baseline: NOT STARTED
candidate-model benchmarking: NOT STARTED
held-out model evaluation: NOT STARTED
preferred router: NOT SELECTED
runtime routing strategy: NOT ESTABLISHED
```

The benchmark dataset is therefore **content-frozen but not yet
benchmark-executed**.

The next step is to perform the final Git diff and status review, commit
the complete routing-dataset freeze milestone, record the resulting Git
revision, and verify that the committed frozen artifacts correspond to
the recorded canonical hashes.

No routing-performance claim should be made until routing candidates
have been executed against the documented benchmark protocol and the
resulting evidence has been reviewed.

---

# 37. Claim Discipline

Acceptable future wording may look like:

> In routing benchmark version X, candidate Y achieved the strongest reviewed performance on the versioned held-out dataset under the documented experiment configuration.

That statement must include or reference the actual evidence.

Avoid claims such as:

```text
production-grade accuracy
enterprise-scale performance
zero routing failures
real-world reliability
```

unless corresponding evidence actually exists.

---

# Core Principle

> Reliora selects its routing strategy from reproducible evidence, not architectural preference.