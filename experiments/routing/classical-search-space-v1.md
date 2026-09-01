# Reliora Routing Benchmark — Classical Candidate Search Space v1

## Status

PRE-VALIDATION CONFIGURATION

This document defines the bounded configuration search space for the
classical routing candidates before validation-result inspection.

The search space must not be expanded in response to validation results
without explicitly versioning the experiment configuration and recording
the rationale.

---

## 1. Purpose

The routing benchmark compares two lightweight statistical text
classification approaches:

- C1 — TF-IDF + Logistic Regression
- C2 — TF-IDF + Linear SVM

The purpose is not exhaustive hyperparameter optimization.

The experiment asks:

> Does a small, operationally simple statistical text classifier
> materially improve on the deterministic routing baseline?

The search space is intentionally small because the benchmark contains
only 108 training records and 36 validation records.

---

## 2. Dataset Discipline

Candidate fitting uses:

```text
TRAIN
108 records
```

Configuration comparison uses:

```text
VALIDATION
36 records
```

The held-out split is:

```text
TEST
36 records
```

The held-out test split must not be used for:

- fitting;
- hyperparameter selection;
- preprocessing selection;
- candidate repair;
- configuration selection.

The preferred candidate and configuration must be fixed before the
held-out test split is evaluated.

Validation evidence may be used only to compare configurations contained
in this predeclared search space.

Configurations must not be added reactively because validation
performance is disappointing.

---

## 3. Predictive Input Boundary

The only predictive input is:

```text
customer message
```

The following dataset fields must not become predictive features:

- case ID;
- family ID;
- variant ID;
- split;
- provenance;
- expected intent.

The supervised target during fitting is:

```text
expected intent
```

with the frozen routing labels:

```text
BUG
PLATFORM
OTHER
```

---

## 4. Shared TF-IDF Preprocessing

C1 and C2 use the same TF-IDF preprocessing except for the predeclared
n-gram-range variation.

Shared configuration:

```text
analyzer = word
lowercase = true
strip_accents = none
min_df = 1
max_df = 1.0
norm = l2
use_idf = true
smooth_idf = true
sublinear_tf = false
stop_words = none
```

No stemming is applied.

No lemmatization is applied.

No character n-grams are included.

No vocabulary may be constructed from validation or held-out test data.

The TF-IDF vectorizer is fitted using training messages only.

---

## 5. TF-IDF Search Dimension

Two word n-gram configurations are evaluated.

### N1 — Unigrams

```text
ngram_range = (1, 1)
```

This represents individual word tokens.

### N2 — Unigrams + Bigrams

```text
ngram_range = (1, 2)
```

This includes individual words and adjacent two-word phrases.

Bigrams test whether phrases such as:

```text
log in
return policy
payment method
order history
```

provide useful additional routing information.

Higher-order word n-grams are excluded from benchmark v1 to avoid an
unnecessarily large and sparse feature space for the small training
dataset.

---

## 6. Regularization Search Dimension

Both statistical classifiers evaluate:

```text
C = 0.5
C = 1.0
C = 2.0
```

`C` is the inverse regularization-strength parameter.

Conceptually:

```text
smaller C
→ stronger regularization

larger C
→ weaker regularization
```

The values intentionally provide only a small comparison around the
reference value of 1.0.

A wider numerical sweep is out of scope for benchmark v1.

---

## 7. C1 — TF-IDF + Logistic Regression

C1 uses:

```text
TF-IDF
+
Logistic Regression
```

Classifier configuration:

```text
solver = lbfgs
max_iter = 1000
class_weight = none
fit_intercept = true
tol = 0.0001
```

The training split is balanced across BUG, PLATFORM, and OTHER.
Class weighting is therefore not introduced in benchmark v1.

C1 evaluates exactly six configurations:

```text
C1-N1-C0.5
C1-N1-C1.0
C1-N1-C2.0

C1-N2-C0.5
C1-N2-C1.0
C1-N2-C2.0
```

No additional C1 configuration may be introduced after validation-result
inspection without versioning the experiment configuration.

---

## 8. C2 — TF-IDF + Linear SVM

C2 uses:

```text
TF-IDF
+
Linear Support Vector Machine
```

Classifier configuration:

```text
class_weight = none
max_iter = 5000
tol = 0.0001
```

The training split is balanced across BUG, PLATFORM, and OTHER.
Class weighting is therefore not introduced in benchmark v1.

C2 evaluates exactly six configurations:

```text
C2-N1-C0.5
C2-N1-C1.0
C2-N1-C2.0

C2-N2-C0.5
C2-N2-C1.0
C2-N2-C2.0
```

No additional C2 configuration may be introduced after validation-result
inspection without versioning the experiment configuration.

---

## 9. Total Classical Search Space

The complete benchmark-v1 classical search space contains:

```text
6 Logistic Regression configurations
+
6 Linear SVM configurations
=
12 configurations
```

This number is frozen before validation-result inspection.

---

## 10. Configuration Selection

Validation macro F1 is the primary classification-quality metric.

Selection must also inspect:

- accuracy;
- macro precision;
- macro recall;
- per-class precision;
- per-class recall;
- per-class F1;
- confusion matrix;
- operationally important failure patterns.

Accuracy alone must not determine configuration selection.

A configuration with a slightly higher aggregate metric may be rejected
if its per-class behavior or failure modes are materially worse for the
Reliora routing contract.

When two configurations provide effectively equivalent classification
evidence, prefer the simpler representation:

```text
unigrams
before
unigrams + bigrams
```

The selection rationale must be documented explicitly.

---

## 11. Explicitly Excluded Tuning

Benchmark v1 does not search:

- character n-grams;
- trigrams or higher-order word n-grams;
- alternative stop-word configurations;
- stemming;
- lemmatization;
- alternative tokenizers;
- class weighting;
- alternative Logistic Regression solvers;
- nonlinear SVM kernels;
- large C sweeps;
- random search;
- Bayesian optimization;
- automated hyperparameter optimization;
- additional classifier families.

These techniques require a separately documented justification if later
evidence indicates that benchmark-v1 candidates are inadequate.

They must not be added merely to improve validation results.

---

## 12. Determinism

The fitted Logistic Regression and Linear SVM candidates are expected to
produce deterministic predictions under a fixed dataset, implementation,
library version, and candidate configuration.

This expectation must be verified experimentally rather than assumed.

---

## 13. Evidence Requirements

Generated experiment evidence must identify at least:

- candidate ID;
- candidate family;
- TF-IDF preprocessing;
- n-gram range;
- C value;
- classifier configuration;
- training split usage;
- validation split usage;
- metric results;
- confusion matrix;
- relevant failure cases;
- Python version;
- scikit-learn version;
- benchmark implementation Git revision;
- experiment timestamp;
- evidence classification.

The held-out test result is recorded only after the preferred candidate
and configuration have been fixed.

---

## 14. Change Control

This document is a pre-validation experimental control.

After validation-result inspection begins, changes to the predefined
classical search space must not be silently incorporated.

If a material configuration change becomes necessary, it requires:

```text
new configuration version
+
documented rationale
+
explicit acknowledgement that prior validation evidence was observed
```

The held-out test set must remain closed throughout any such
configuration-development work.

---

## 15. Guiding Principle

The benchmark should answer the smallest useful architecture question:

> Can a lightweight statistical classifier provide materially better
> routing behavior than deterministic rules without introducing
> unjustified operational complexity?

The objective is evidence-based architecture selection, not maximum
algorithm count or maximum hyperparameter tuning.