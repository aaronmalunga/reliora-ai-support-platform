# Reliora Routing Benchmark — Classical Candidate Search Space v1

## Status

PRE-VALIDATION CONFIGURATION

This document defines the bounded configuration search space for the
classical routing candidates before validation-result inspection.

The search space must not be expanded in response to validation results
without explicitly versioning the experiment configuration and recording
the rationale.

---

## Purpose

The routing benchmark compares two lightweight statistical text
classification approaches:

- C1 — TF-IDF + Logistic Regression
- C2 — TF-IDF + Linear SVM

The goal is not exhaustive hyperparameter optimization.

The goal is to determine whether a small, operationally simple
statistical classifier materially improves on the deterministic routing
baseline.

---

## Dataset Discipline

Candidate fitting uses:

```text
TRAIN
108 records