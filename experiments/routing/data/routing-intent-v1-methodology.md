# Routing Intent Dataset v1 — Generation, Selection, and Review Methodology

## 1. Purpose

This document describes how the `routing-intent-v1` dataset was designed, generated, selected, validated, audited, reviewed, and eventually frozen for the Reliora routing benchmark.

The purpose is to make the benchmark reproducible and its limitations visible.

The dataset is not presented as production customer traffic.

It is a controlled synthetic evaluation asset intended to support an engineering decision about Reliora's top-level routing strategy.

The prediction target is:

- `BUG`
- `PLATFORM`
- `OTHER`

Knowledge coverage for `PLATFORM` requests is intentionally excluded from this classifier and is evaluated separately as:

- `SUPPORTED`
- `UNSUPPORTED`

This separation follows Reliora's functional requirements and routing architecture.

---

## 2. Evidence and Provenance Classification

### 2.1 Dataset provenance

Dataset records are classified as:

`SYNTHETIC_ASSUMPTION`

The messages were created specifically for the Reliora routing benchmark.

They were not:

- collected from real customers;
- extracted from production logs;
- purchased from a third-party dataset;
- presented as representative production traffic;
- derived from measured Reliora usage volume.

### 2.2 Audit evidence

Executed dataset-quality analyses are classified as:

`EXPERIMENTAL`

This classification means that the results were produced by a repeatable experiment against the versioned synthetic dataset.

### 2.3 Claim boundary

The dataset may support claims about:

- behavior on the documented synthetic benchmark;
- comparative performance of routing candidates on that benchmark;
- observed error patterns within the benchmark;
- reproducibility of the routing experiment.

The dataset does not, by itself, support claims about:

- production routing accuracy;
- real-world customer-language prevalence;
- production traffic distribution;
- production reliability;
- production latency;
- commercial impact;
- customer satisfaction;
- population-level language behavior.

---

## 3. Dataset Design Strategy

The dataset was designed before production-router selection.

The design process began from the routing contract rather than from a particular model.

The benchmark therefore follows:

```text
requirement
    ↓
label contract
    ↓
semantic families
    ↓
message variants
    ↓
train / validation / test partition
    ↓
candidate models
```

It does not follow:

```text
choose model
    ↓
generate examples that model handles well
    ↓
report score
```

This ordering reduces the risk of creating a benchmark around a preferred implementation.

---

## 4. Label Taxonomy

### 4.1 BUG

A customer message is labelled `BUG` when the primary intent is to report behavior that appears technically incorrect, broken, inconsistent, or non-functional within the supported commerce platform.

Examples of conceptual scenarios include:

- checkout crashes;
- login loops;
- cart updates fail;
- search malfunctions;
- a payment button does not respond;
- a tracking page is blank.

### 4.2 PLATFORM

A customer message is labelled `PLATFORM` when the primary intent is to ask for information about the supported commerce platform, its policies, capabilities, processes, or services.

Examples include:

- return policy;
- shipping times;
- payment methods;
- warranty information;
- loyalty programs;
- cancellation policy;
- account deletion;
- exchange policy.

A `PLATFORM` label does not imply that Reliora necessarily has sufficient knowledge to answer the question.

Knowledge coverage is a separate downstream decision.

### 4.3 OTHER

A customer message is labelled `OTHER` when the primary intent falls outside the supported platform domain.

Examples include:

- general knowledge;
- creative writing;
- unrelated mathematics;
- programming help;
- travel planning;
- recipe requests;
- external-company support;
- stock-market questions.

Downstream workflow policy may route these messages to human handoff or another controlled path.

---

## 5. Semantic-Family Selection

### 5.1 Why semantic families are used

Randomly splitting individual paraphrases can create information leakage.

For example, these messages may look different at the string level:

```text
Where can I track my order?
How do I see my parcel tracking?
Where is order tracking located?
```

but they represent essentially the same semantic problem.

If two variants are placed in training and another nearly identical variant is placed in test, model performance may be overstated.

For this reason, `routing-intent-v1` uses the **semantic family** as the partitioning unit.

### 5.2 Family inventory

The benchmark contains:

| Intent | Semantic families | Messages |
|---|---:|---:|
| BUG | 15 | 60 |
| PLATFORM | 15 | 60 |
| OTHER | 15 | 60 |
| **Total** | **45** | **180** |

Each semantic family contains exactly four message variants:

- `A`
- `B`
- `C`
- `D`

The family inventory is versioned separately in:

`routing-intent-v1-families.json`

### 5.3 Family-selection criteria

Families were selected to provide:

1. representative examples of each routing contract;
2. multiple customer-language styles;
3. lexical overlap across classes where useful;
4. cases that distinguish technical failure from informational inquiry;
5. out-of-domain requests that may still contain commerce or technical vocabulary;
6. scenarios suitable for a small controlled benchmark;
7. enough semantic diversity to permit family-level holdout.

Family selection was not based on measured production-frequency estimates.

All prevalence implied by the class balance is therefore synthetic.

---

## 6. Message Generation Method

### 6.1 Generation process

Messages were generated with model assistance under explicit constraints defined by the semantic-family manifest and dataset design.

The generator was not asked to produce an unconstrained list of:

```text
60 BUG messages
60 PLATFORM messages
60 OTHER messages
```

Instead, generation was constrained by the pre-defined semantic-family structure.

For every family, four variants were authored to represent different expressions of the same underlying customer intent.

### 6.2 Variant design

Variants were intended to introduce controlled linguistic diversity, including combinations of:

- direct statements;
- questions;
- conversational phrasing;
- short informal messages;
- mildly noisy wording;
- different verbs for similar actions;
- explicit failure descriptions;
- implicit failure descriptions;
- overlapping commerce terminology.

The objective was not to simulate every possible customer expression.

The objective was to create a sufficiently varied benchmark for comparing routing approaches while maintaining traceable labels.

### 6.3 Generation constraints

Every generated record must contain:

- `case_id`;
- `family_id`;
- `variant_id`;
- `message`;
- `expected_intent`;
- `split`;
- `provenance`.

Every message must:

- contain a non-empty customer utterance;
- belong to exactly one registered semantic family;
- use one of the permitted top-level labels;
- inherit its split from its semantic family;
- use `SYNTHETIC_ASSUMPTION` provenance.

---

## 7. Dataset Partitioning

### 7.1 Split unit

The split unit is:

`semantic_family`

Individual messages are not independently randomized across splits.

All four variants belonging to one semantic family remain in the same split.

### 7.2 Split allocation

Per class:

| Split | Families | Messages |
|---|---:|---:|
| Train | 9 | 36 |
| Validation | 3 | 12 |
| Test | 3 | 12 |

Overall:

| Split | Families | Messages |
|---|---:|---:|
| Train | 27 | 108 |
| Validation | 9 | 36 |
| Test | 9 | 36 |
| **Total** | **45** | **180** |

### 7.3 Why family-aware splitting matters

Family-aware splitting is intended to test whether a router generalizes to **unseen semantic scenarios**, rather than simply recognizing another paraphrase of a scenario already present in training.

This makes the test set more demanding than a random message-level split.

### 7.4 Test-set governance

The test-family assignments were established before model benchmarking.

Once the dataset is formally frozen:

- the test set must not be modified in response to model errors;
- candidate tuning must use training and validation data;
- final test evaluation should occur only after the candidate configuration is selected;
- any necessary post-freeze test correction requires explicit documentation and, where material, a new dataset version.

---

## 8. Structural Validation

Hard dataset contracts are enforced by:

`experiments/routing/scripts/validate_routing_data.py`

The validator checks both the semantic-family manifest and the 180-record dataset.

Current checks include:

### Manifest checks

- expected dataset identity;
- permitted labels;
- permitted splits;
- required metadata;
- exactly 45 semantic families;
- exactly 15 families per intent;
- expected family split counts;
- expected per-intent split counts;
- unique family identifiers.

### Dataset checks

- expected dataset identity and version;
- declared record count;
- exactly 180 records;
- required record fields;
- non-empty identifiers and messages;
- permitted labels;
- permitted splits;
- permitted variants;
- provenance classification;
- unique case identifiers;
- duplicate-message detection;
- family existence in the manifest;
- dataset label matching manifest label;
- dataset split matching manifest split;
- all 45 manifest families represented;
- exactly four records per family;
- variants `A`, `B`, `C`, and `D` exactly once per family;
- 60 records per intent;
- expected train, validation, and test counts;
- expected per-intent split counts.

At the final pre-freeze validation checkpoint, structural validation
passed.

Structural validation was executed again after targeted dataset
curation and before the dataset content was frozen.

---

## 9. Dataset Quality Audit

Structural validity does not establish benchmark quality.

A separate diagnostic audit is therefore implemented in:

`experiments/routing/scripts/audit_routing_dataset.py`

The audit is intentionally separate from the hard validator.

```text
validate_routing_data.py
→ determines whether hard dataset contracts pass

audit_routing_dataset.py
→ surfaces quality risks requiring engineering judgment
```

A diagnostic finding is not automatically a dataset defect.

---

## 10. Near-Duplicate Audit

### 10.1 Objective

The near-duplicate audit searches for suspiciously similar messages crossing:

- train → validation;
- train → test;
- validation → test.

### 10.2 Jaccard similarity

Jaccard similarity measures overlap between token sets.

For token sets \(A\) and \(B\):

\[
J(A,B)=\frac{|A \cap B|}{|A \cup B|}
\]

The current diagnostic threshold is:

`Jaccard similarity >= 0.55`

### 10.3 Sequence similarity

Character-sequence similarity is also used because token overlap alone does not capture highly similar sentence structure.

The current sequence threshold is:

`sequence similarity >= 0.78`

A pair is flagged when either threshold is met.

These thresholds are review heuristics, not universal definitions of data leakage.

### 10.4 Final Pre-Freeze Result

At the final pre-freeze audit checkpoint:

`Cross-split near-duplicate findings: 0`

No cross-split message pair exceeded either configured review threshold.

This result applies only to the documented Jaccard and sequence-similarity
heuristics.

It does not prove that the splits contain no semantic similarity.

---

## 11. Lexical-Shortcut Audit

### 11.1 Objective

A synthetic classifier benchmark can become artificially easy when particular words strongly reveal the class label.

For example:

```text
"crash" → always BUG
"policy" → always PLATFORM
"recipe" → always OTHER
```

Some association is expected and semantically legitimate.

The purpose of the audit is to identify associations for review rather than automatically remove them.

### 11.2 Message-level association

Tokens are currently considered for diagnostic reporting when:

- document frequency is at least `4`; and
- label purity is at least `0.80`.

### 11.3 Semantic-family frequency

Message frequency alone can exaggerate a lexical association because every semantic family contains four variants.

For example:

```text
wishlist
→ 4 messages
→ all BUG
```

may simply mean one four-variant wishlist family uses the word consistently.

The audit therefore also measures:

- number of distinct semantic families containing a token;
- dominant family-level intent;
- family-level label purity;
- families contributing to the association.

This distinguishes a family-specific term from a broader class-wide lexical shortcut.

### 11.4 Final Pre-Freeze Result

The initial audit identified:

- strongly class-associated token findings: `32`;
- cross-family class-associated token findings: `24`.

Human review identified several likely synthetic-style shortcuts,
including the initial distributions of `help`, `just`, and `page`.

Six message records were revised before model training.

After targeted curation and audit regeneration:

- strongly class-associated token findings: `31`;
- cross-family class-associated token findings: `23`;
- cross-split near-duplicate findings remained `0`.

The objective was not to drive these counts to zero.

Legitimate predictive language was retained when its relationship to
intent was semantically defensible.

Detailed curation decisions are recorded in:

`routing-intent-v1-review-log.md`

---

## 12. Boundary-Term Audit

The dataset deliberately contains some vocabulary across multiple intents.

This helps prevent the benchmark from reducing routing to a single keyword lookup.

Examples observed in the current dataset include:

| Term | BUG | PLATFORM | OTHER |
|---|---:|---:|---:|
| account | 2 | 3 | 0 |
| address | 4 | 3 | 0 |
| checkout | 4 | 1 | 0 |
| discount | 1 | 3 | 0 |
| error | 8 | 0 | 1 |
| order | 6 | 13 | 4 |
| payment | 4 | 3 | 0 |
| product | 3 | 1 | 0 |
| return | 1 | 3 | 1 |
| shipping | 1 | 4 | 0 |
| tracking | 3 | 3 | 0 |

This overlap is intentional.

For example, the word `tracking` may occur in:

```text
BUG
→ the tracking page is broken

PLATFORM
→ how do I track my order?
```

The routing decision should therefore depend on the customer intent rather than the word `tracking` alone.

---

## 13. Message-Length Audit

Message length can itself become an accidental synthetic-data shortcut.

Current token-length statistics are:

| Group | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| Overall | 4 | 19 | 9.91 |
| BUG | 6 | 19 | 12.00 |
| OTHER | 4 | 14 | 8.83 |
| PLATFORM | 5 | 15 | 8.88 |

`BUG` messages are currently longer on average than the other classes.

This may be partially explained by the additional language customers naturally use when describing a technical symptom.

However, it remains a benchmark risk that must be considered during model evaluation.

A candidate classifier should not be assumed to have learned intent semantics merely because it performs well on this dataset.

---

## 14. Human Semantic Review

Automated validation cannot determine whether every label is
conceptually correct.

Human semantic review was therefore completed before model training and
before the dataset content freeze.

Review evaluated:

1. whether the expected intent matched the actual meaning of the
   message;
2. whether a message could reasonably belong to more than one class;
3. whether wording unintentionally revealed the label;
4. whether test families were sufficiently distinct from training
   families;
5. whether synthetic language was unnaturally repetitive;
6. whether class-specific message length created an excessive shortcut;
7. whether cross-class lexical overlap was sufficient;
8. whether any message depended on unsupported assumptions about
   platform behavior;
9. whether examples remained aligned with the documented routing
   contract.

All 36 held-out test records across all 9 test semantic families were
manually reviewed.

Result:

```text
test semantic families reviewed: 9 / 9
test records reviewed: 36 / 36
test records accepted: 36 / 36
additional test records revised during final semantic review: 0
```

The complete decisions are recorded in:

`routing-intent-v1-review-log.md`

The test set is now closed to model-driven editing.

After model evaluation begins, a model error must not automatically
result in rewriting a held-out example.

A genuine ground-truth defect may still be corrected under explicit
dataset change control and versioning.

---

## 15. Selection and Rejection Policy

Synthetic examples are not retained simply because they were generated.

A message may be revised or rejected before dataset freeze when it:

- has an ambiguous primary intent;
- duplicates or nearly duplicates another split;
- violates the semantic-family definition;
- contains the wrong split or label;
- contains artificial wording that makes the class trivial to infer;
- introduces a misleading platform assumption;
- fails the structural validator;
- materially weakens benchmark independence.

Changes made before model benchmarking are dataset-design corrections.

Changes made after observing test-model performance require stricter change control because they may introduce test-set contamination.

---

## 16. Freeze Criteria and Finalization

Reliora distinguishes between:

```text
DATA CONTENT FREEZE
and
FINAL FREEZE EVIDENCE PACKAGE
```

### 16.1 Data Content Freeze

The data content may be marked `FROZEN` once:

- family-manifest validation passes;
- dataset structural validation passes;
- no unresolved duplicate identifiers exist;
- cross-split near-duplicate findings are reviewed;
- class-associated token findings are reviewed;
- boundary-term distributions are reviewed;
- message-length distributions are reviewed;
- semantic labels are manually reviewed;
- ambiguous records are resolved or documented;
- held-out test records are manually reviewed;
- the test set is declared closed to model-driven editing.

These conditions were satisfied before the version 1 data content was
frozen.

The following artifacts therefore now carry lifecycle state:

```text
routing-intent-v1-families.json → FROZEN
routing-intent-v1.json          → FROZEN
```

`FROZEN` means the benchmark content is closed to model-driven editing.

It does not mean every evidence-packaging task has already been
completed.

### 16.2 Final Freeze Evidence Package

Before model benchmarking begins, the frozen dataset must also receive a
final evidence package containing:

- synchronized dataset-card status;
- synchronized methodology status;
- synchronized review-log status;
- synchronized routing-experiment documentation;
- final structural-validation execution;
- final diagnostic-audit execution;
- applicable Python quality gates;
- canonical SHA-256 hashes;
- explicit hash basis;
- associated Git revision.

This evidence-finalization stage is still in progress.

### 16.3 Benchmark Execution Preconditions

Routing-model benchmarking must not begin until:

- the final freeze evidence package is complete;
- canonical frozen hashes are recorded;
- the associated Git revision is recorded;
- benchmark code consumes only the documented customer-message field as
  model input;
- train, validation, and test usage follows the documented split
  discipline.

This separation prevents evidence-packaging tasks from being confused
with permission to continue editing frozen benchmark content.

---

## 17. Versioning and Change Control

Dataset version:

`1.0.0`

Current lifecycle state:

`FROZEN`

Family-manifest lifecycle state:

`FROZEN`

The frozen content has completed pre-model semantic review and is closed
to model-driven editing.

An earlier pre-curation SHA-256 was used as an integrity checkpoint
during dataset construction.

That digest is historical development evidence and is not the final
frozen dataset identity because legitimate pre-freeze curation changed
the dataset afterward.

The final canonical frozen identities are now recorded as:

```text
dataset:
routing-intent-v1.json

dataset SHA-256:
369600abb8711dcadc0acb96bd19edc33a9c06a83cf7c09208bccb6dbde85450

family manifest:
routing-intent-v1-families.json

family-manifest SHA-256:
93d07598b846c2df3490f39b68971b2ae2a5dba872fb149e513f592c0d5724a1

hash algorithm:
SHA-256

hash basis:
file bytes with line endings normalized to LF
```

The LF-normalized hash basis matches the repository's enforced
`eol=lf` Git attribute for both frozen JSON artifacts.

The associated frozen Git revision remains pending until the complete
dataset-freeze milestone is committed.

After freeze:

- documentation-only changes do not require a dataset version
  increment;
- corrections to message content, labels, family membership, or split
  membership require explicit change documentation;
- material benchmark-data changes should result in a new dataset
  version;
- model failures do not justify silently rewriting test records;
- benchmark results must always identify the exact dataset version,
  canonical hash, and associated Git revision used.

---

## 18. Current Frozen Checkpoint

At the current frozen-content checkpoint:

| Check | Result |
|---|---|
| Dataset version | 1.0.0 |
| Dataset records | 180 |
| Semantic families | 45 |
| BUG records | 60 |
| PLATFORM records | 60 |
| OTHER records | 60 |
| Train records | 108 |
| Validation records | 36 |
| Test records | 36 |
| Duplicate case IDs | 0 |
| Exact duplicate messages | 0 |
| Cross-split near-duplicate findings | 0 |
| Strongly class-associated token findings | 31 |
| Cross-family class-associated token findings | 23 |
| Structural validator | PASS |
| Python static type checks executed | PASS |
| Ruff lint checks executed | PASS |
| Human semantic review | COMPLETE |
| Test families reviewed | 9 / 9 |
| Test records accepted | 36 / 36 |
| Family manifest frozen | YES |
| Dataset content frozen | YES |
| Test set closed to model-driven editing | YES |
| Final canonical frozen hashes | RECORDED |
| Associated frozen Git revision | PENDING |
| Routing-model benchmarking | NOT STARTED |

These results describe the controlled synthetic benchmark only.

They do not constitute production-performance evidence.

The dataset is content-frozen, while final evidence packaging and
canonical identity recording remain in progress.

---

## 19. Known Limitations

The current dataset has important limitations.

### 19.1 Synthetic language

All customer messages are synthetic.

Real customer conversations may contain:

- spelling mistakes;
- multiple simultaneous intents;
- incomplete context;
- emotional language;
- regional language differences;
- slang;
- very long messages;
- extremely short messages;
- adversarial instructions;
- prior-turn dependencies;
- attachments;
- unexpected domain combinations.

### 19.2 Small benchmark

A 180-message benchmark is suitable for controlled architectural comparison but is not sufficient to establish broad production generalization.

### 19.3 Balanced classes

The dataset contains exactly 60 records for each intent.

This balance is an experimental design choice and should not be interpreted as an estimate of real production class prevalence.

### 19.4 Single-turn routing

The current benchmark focuses on individual customer messages.

Multi-turn context may require separate evaluation.

### 19.5 Lexical artifacts

Because the dataset is synthetic and family-structured, vocabulary and message-length artifacts may remain even after review.

These limitations must be considered when interpreting model performance.

---

## 20. Relationship to Other Routing Artifacts

| Artifact | Responsibility |
|---|---|
| `routing-intent-v1-families.json` | Defines semantic families, labels, and split assignments |
| `routing-intent-v1.json` | Contains the 180 executable benchmark records |
| `routing-intent-v1-card.md` | Provides the concise dataset specification and usage contract |
| `routing-intent-v1-methodology.md` | Documents generation, selection, audit, review, and governance |
| `validate_routing_data.py` | Enforces hard structural and cross-artifact contracts |
| `audit_routing_dataset.py` | Produces diagnostic benchmark-quality findings |
| `routing-intent-v1-audit.json` | Stores generated audit evidence |
| `experiments/routing/README.md` | Defines the broader routing experiment protocol |

---

## 21. Reproducibility Principle

A future engineer should be able to answer all of the following without relying on undocumented project history:

- Why do these three labels exist?
- Why were these 45 families selected?
- Why are there four variants per family?
- Why are there 180 records?
- How were train, validation, and test records separated?
- How was leakage risk assessed?
- How were lexical shortcuts assessed?
- Which checks are deterministic?
- Which checks require engineering judgment?
- Which results are synthetic assumptions?
- Which results are experimental measurements?
- When was the test set frozen?
- Which exact dataset version produced a benchmark result?

If those questions cannot be answered from version-controlled artifacts, the benchmark is not sufficiently reproducible.
