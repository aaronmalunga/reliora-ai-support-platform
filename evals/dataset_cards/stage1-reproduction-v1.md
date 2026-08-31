# Dataset Card — stage1-reproduction-v1

## Dataset

**ID:** `stage1-reproduction-v1`

**Version:** `1.0.0`

## Purpose

This dataset preserves known behavioural and factual evaluation gaps from the frozen Stage-1 customer-support chatbot and provides reproducible inputs for Reliora's deterministic evaluation system.

It is not a training dataset.

It is a regression and evaluation dataset.

---

## Source Baseline

**Repository:** `aws-agentcore-customer-support-chatbot`

**Frozen commit:**

`2da594b1126c566a593f31891f25a6f4ea4afa53`

The relevant source artifacts were independently verified using SHA-256 hashes computed from the exact Git objects stored at this commit.

Windows working-copy hashes are not used as canonical evidence because the local Git configuration performs CRLF checkout conversion.

---

## Cases

### REPRO-001 — Multiple Missing Bug Fields

The Stage-1 prompt requires the agent to ask for only one missing bug-report field at a time.

The frozen evaluation response instead requests description, reproduction steps, and environment in one response.

**Evidence type:** directly reproducible

**Primary invariant:** `INV-004`

**Expected deterministic result:** FAIL

---

### REPRO-002 — Internal Route Label Leakage

The frozen system prompt identifies `HUMAN HANDOFF` as an internal route and explicitly prohibits customer-facing route-name exposure.

The frozen evaluation response begins with the literal text:

`HUMAN HANDOFF`

**Evidence type:** directly reproducible

**Primary invariant:** `INV-012`

**Expected deterministic result:** FAIL

---

### REPRO-003 — Streamed Thinking Exposure

The frozen repository documents that `<thinking>...</thinking>` content was visible during manual AgentCore/Nova Pro development execution.

The repository preserves:

`[streamed <thinking> content visible]`

but does not preserve the complete raw reasoning text.

Reliora therefore does not reconstruct or fabricate the missing content.

**Evidence type:** repository-preserved OBSERVED runtime evidence

**Primary invariant:** `INV-012`

**Executable replay:** No

---

### REPRO-004 — Incomplete Return-Policy Detail

The authoritative FAQ states that most items may be returned within 30 days when unused and in original packaging, with an exception when the item arrived defective.

The Stage-1 evaluation reference also explicitly requires that exception.

The actual frozen response includes the 30-day window, unused condition, and original-packaging condition, but omits the defective-item exception.

**Evidence type:** directly reproducible

**Evaluation contract:** `FACT-001 — required FAQ fact completeness`

**Expected assertion result:** FAIL

---

## Evidence Classification

The cases are classified as **OBSERVED** because they are preserved in the frozen Stage-1 repository or its associated execution documentation.

Results produced by executing Reliora's evaluators against these cases will be classified as **EXPERIMENTAL**.

---

## Annotation Policy

Raw prompts and responses are preserved exactly where available.

Structured fields such as:

- requested bug fields;
- required factual assertions;
- executable status;

are reviewed annotations used to make deterministic evaluation possible.

Annotations must not be represented as raw Stage-1 output.

---

## Known Limitation

REPRO-003 cannot be replayed byte-for-byte because the repository does not preserve the complete raw reasoning text that was exposed.

The case remains valuable as historical evidence and as motivation for leakage regression tests, but must not be counted as an executable reproduction.

---

## Intended Use

This dataset may be used for:

- Stage-1 defect reproduction;
- deterministic evaluator regression testing;
- evaluation-system demonstrations;
- release-regression tests.

It must not be silently modified to improve Reliora evaluation scores.

Material changes require a new dataset version.