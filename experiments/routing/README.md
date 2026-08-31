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

The benchmark should use clearly separated data for:

```text
development / training
validation where applicable
final held-out testing
```

The exact split strategy will be specified once the dataset design is finalized.

The final test set should not be repeatedly inspected and modified in response to model errors.

Otherwise it gradually becomes part of the development process and stops functioning as genuinely held-out evidence.

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

# 31. Expected Directory Structure

```text
experiments/
└── routing/
    ├── README.md
    │
    ├── data/
    │   └── versioned routing datasets
    │
    ├── scripts/
    │   └── benchmark and analysis code
    │
    └── results/
        └── generated experimental evidence
```

---

# 32. Directory Responsibilities

## `data/`

Contains versioned inputs used by routing experiments.

This directory should hold data artifacts, not implementation code.

---

## `scripts/`

Contains executable experiment orchestration such as:

```text
dataset validation
training
benchmark execution
metric calculation
result generation
```

Reusable application runtime code should eventually live under:

```text
src/reliora/
```

rather than being hidden permanently inside an experiment script.

---

## `results/`

Contains generated experimental outputs.

Examples may include:

```text
metrics JSON
confusion matrices
timing summaries
model-comparison summaries
```

Generated evidence must be distinguishable from hand-authored documentation.

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

# 35. Planned Experiment Lifecycle

```text
1. define routing contract
2. design dataset
3. validate labels and provenance
4. establish simple baseline
5. train candidate classifiers
6. evaluate held-out data
7. analyze confusion patterns
8. measure repeatable local latency
9. generate versioned results
10. review evidence
11. update ADR-012
12. select or reject routing strategy
13. promote chosen implementation into runtime architecture
```

---

# 36. Current Status

Current status:

```text
experiment specification: IN PROGRESS
dataset: not yet created
baseline: not yet measured
candidate models: not yet benchmarked
preferred router: not selected
production router: not established
```

No routing-performance claim should be made until experimental evidence exists.

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