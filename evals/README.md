# Reliora Evaluation System

This directory contains the versioned datasets, dataset documentation, execution runners, and evaluation contracts used to test Reliora's AI behaviour.

Reliora treats evaluation as an engineering subsystem rather than as a single model score.

The core principle is:

> **The LLM may propose; deterministic software validates and authorizes.**

The evaluation system is designed to make important behavioural requirements explicit, executable where practical, versioned, reproducible, and traceable to evidence.

---

# Why This Evaluation System Exists

AI systems can produce responses that appear reasonable while still violating important behavioural contracts.

Examples include:

```text
requesting multiple required fields at once
exposing internal route labels
leaking hidden reasoning markers
omitting required policy information
creating duplicate side effects
fabricating backend identifiers
```

A general LLM-as-a-judge score may not reliably detect every hard behavioural requirement.

Reliora therefore separates:

```text
hard behavioural requirements
→ deterministic evaluation where practical

generative qualities
→ human or model-based evaluation where appropriate
```

---

# Evaluation Architecture

The evaluation workflow follows:

```text
Requirement
    ↓
Evaluation Contract
    ↓
Evaluator
    ↓
Dataset
    ↓
Dataset Card
    ↓
Runner
    ↓
Generated Evidence
    ↓
Engineering / Release Decision
```

Supporting unit tests independently verify that the evaluator logic itself behaves correctly.

A more complete view is:

```text
Behavioural Requirement
        │
        ▼
evals/behavioural-evaluation-contract.md
        │
        ▼
Evaluator Implementation
src/reliora/evaluation/
        │
        ├──────────────► Unit Tests
        │                tests/unit/evaluation/
        │
        ▼
Evaluation Dataset
evals/datasets/
        │
        ▼
Dataset Card
evals/dataset_cards/
        │
        ▼
Evaluation Runner
evals/runners/
        │
        ▼
Generated Evidence
evidence/generated/
        │
        ▼
Regression / CI / Release Decision
```

---

# Directory Structure

```text
evals/
│
├── README.md
├── behavioural-evaluation-contract.md
│
├── datasets/
│   ├── stage1-reproduction-v1.json
│   └── deterministic-evaluator-regression-v1.json
│
├── dataset_cards/
│   ├── stage1-reproduction-v1.md
│   └── deterministic-evaluator-regression-v1.md
│
└── runners/
    ├── run_stage1_reproduction.py
    └── run_deterministic_evaluator_regression.py
```

Related evaluator implementation exists under:

```text
src/reliora/evaluation/
```

Current evaluator modules include:

```text
models.py
bug_workflow.py
leakage.py
factual.py
reproduction.py
regression.py
```

Evaluator unit tests exist under:

```text
tests/unit/evaluation/
```

Current evaluation test modules include:

```text
test_bug_workflow.py
test_factual.py
test_leakage.py
test_reproduction.py
test_regression.py
```

Generated evaluation evidence is stored under:

```text
evidence/generated/
```

---

# 1. Behavioural Evaluation Contract

File:

```text
evals/behavioural-evaluation-contract.md
```

This document defines Reliora's behavioural invariants.

An invariant represents a system behaviour that should remain true.

Examples include:

```text
INV-001
Exactly One Top-Level Intent

INV-004
Missing Information Collected Incrementally

INV-007
One Logical Operation Produces No Duplicate Ticket

INV-012
Internal Information Does Not Leak
```

The contract is the specification layer.

It answers:

> What behaviour is required?

Not every documented invariant is immediately executable.

Some invariants depend on architecture that has not yet been implemented.

Reliora therefore distinguishes:

```text
documented invariant
```

from:

```text
implemented evaluator
```

and from:

```text
verified system behaviour
```

These are different maturity levels.

---

# 2. Evaluators

Location:

```text
src/reliora/evaluation/
```

Evaluators contain reusable deterministic evaluation logic.

They answer:

> Given a particular system output or workflow state, does it satisfy a defined evaluation rule?

Current examples include:

```text
bug_workflow.py
→ INV-004

leakage.py
→ INV-012

factual.py
→ FACT-001
```

---

## bug_workflow.py

Contains:

```python
evaluate_incremental_bug_collection(...)
```

This evaluator compares:

```text
missing_fields
requested_fields
```

to determine whether bug-report information is being collected according to the incremental collection policy.

For example:

```text
missing:
steps_to_reproduce
environment

requested:
steps_to_reproduce
```

should pass.

But:

```text
missing:
steps_to_reproduce
environment

requested:
steps_to_reproduce
environment
```

should fail.

---

## leakage.py

Contains:

```python
evaluate_internal_information_leakage(...)
```

This evaluator inspects customer-visible text for currently implemented prohibited marker patterns.

Current deterministic coverage includes:

```text
HUMAN HANDOFF
<thinking>...</thinking>
case-insensitive thinking tags
thinking tags containing attributes
```

The broader INV-012 contract is larger than the currently implemented detector.

Therefore a passing INV-012 result does not prove that every possible form of information leakage is absent.

---

## factual.py

Contains:

```python
evaluate_required_fact_completeness(...)
```

This checks whether every reviewed required fact has at least one accepted textual representation in a response.

Example:

```text
fact:
defective_item_exception

accepted patterns:
defective
damaged
faulty
```

If any accepted pattern is present, that fact is considered represented.

This is a lexical completeness check.

It does not independently prove semantic truth or absence of contradiction.

---

## models.py

Defines shared typed evaluator result contracts.

Current primary model:

```text
EvaluationFinding
```

It contains:

```text
evaluation_id
passed
message
evidence
```

Using one result contract allows different evaluators to produce consistent outputs.

---

# 3. Unit Tests

Location:

```text
tests/unit/evaluation/
```

Unit tests verify the evaluator implementation itself.

This distinction is important.

For example:

```text
Evaluator requirement:
Two requested missing bug fields should fail INV-004.
```

A unit test checks that:

```python
evaluate_incremental_bug_collection(...)
```

actually returns:

```text
passed = false
```

Unit tests therefore answer:

> Does the evaluator code behave correctly?

They do not replace the versioned evaluation dataset.

---

# 4. Evaluation Datasets

Location:

```text
evals/datasets/
```

Datasets contain versioned evaluation cases in machine-readable JSON.

They answer:

> Which cases should be executed?

Typical case information includes:

```text
case_id
evaluation_id
inputs
expected result
case type
reviewed rationale
```

Because the dataset is machine-readable, a runner can load and execute it automatically.

---

# 5. Dataset Cards

Location:

```text
evals/dataset_cards/
```

Each important dataset should have a corresponding human-readable dataset card.

For example:

```text
datasets/
deterministic-evaluator-regression-v1.json

dataset_cards/
deterministic-evaluator-regression-v1.md
```

These two files have different responsibilities.

---

## Dataset JSON

The JSON answers:

> What exactly should the computer execute?

It contains:

```text
cases
inputs
evaluation IDs
expected outcomes
machine-readable metadata
```

---

## Dataset Card Markdown

The Markdown answers:

> What does this dataset mean?

It documents:

```text
purpose
scope
provenance
fixture policy
case interpretation
known limitations
evidence classification
claim boundaries
versioning rules
intended use
```

There is intentional overlap between the JSON and Markdown.

However, the Markdown is not simply a duplicate of the JSON.

The JSON is executable data.

The dataset card is governance and interpretation documentation.

---

# 6. Stage-1 Reproduction Dataset

Dataset:

```text
evals/datasets/stage1-reproduction-v1.json
```

Dataset card:

```text
evals/dataset_cards/stage1-reproduction-v1.md
```

Purpose:

> Reproduce known behavioural and factual evaluation gaps from the frozen Stage-1 project.

These cases are grounded in preserved Stage-1 evidence.

Examples include:

```text
REPRO-001
multiple required bug fields requested

REPRO-002
HUMAN HANDOFF route label exposed

REPRO-003
thinking content documented as exposed

REPRO-004
required return-policy fact omitted
```

This dataset answers:

> Can Reliora's deterministic evaluation layer detect known Stage-1 defects?

---

# 7. Deterministic Evaluator Regression Dataset

Dataset:

```text
evals/datasets/deterministic-evaluator-regression-v1.json
```

Dataset card:

```text
evals/dataset_cards/deterministic-evaluator-regression-v1.md
```

Purpose:

> Test currently implemented deterministic evaluators across deliberately designed positive, negative, boundary, and control fixtures.

Version `1.0.0` contains:

```text
15 cases
```

with:

```text
INV-004     5
INV-012     5
FACT-001    5
```

These fixtures are not historical observations.

They are deliberately designed regression cases.

The dataset answers:

> Does the evaluator behave as expected across reviewed regression inputs?

---

# Historical Reproduction vs Designed Regression

These dataset families must remain separate.

```text
Stage-1 reproduction
→ historical evidence
→ known defects
→ provenance tied to frozen source artifacts

Deterministic regression
→ designed fixtures
→ evaluator behaviour
→ not historical evidence
```

Combining them would make provenance and interpretation ambiguous.

---

# 8. Dispatcher

## Current Regression Dispatcher

File:

```text
src/reliora/evaluation/regression.py
```

Primary function:

```python
evaluate_regression_case(...)
```

The function receives one designed regression case and reads its:

```text
evaluation_id
inputs
```

It then converts evaluator-specific input data into the form required by the corresponding evaluator.

Current dispatch routes are:

```text
INV-004
→ evaluate_incremental_bug_collection()

INV-012
→ evaluate_internal_information_leakage()

FACT-001
→ evaluate_required_fact_completeness()
```

Unsupported evaluation IDs are rejected explicitly rather than silently ignored.

The dispatcher does not:

```text
load datasets
calculate dataset hashes
write reports
calculate experiment summaries
set process exit codes
```

Those responsibilities belong to the runner.

Its purpose is therefore narrowly defined:

> Convert one versioned regression fixture into one deterministic `EvaluationFinding`.

Conceptually:

```text
evaluation_id
        ↓
dispatcher
        ↓
correct evaluator
```

For example:

```text
INV-004
→ evaluate_incremental_bug_collection()

INV-012
→ evaluate_internal_information_leakage()

FACT-001
→ evaluate_required_fact_completeness()
```

The dispatcher prevents the runner from needing to contain all evaluator-specific logic directly.

This separation supports:

```text
maintainability
unit testing
future evaluator expansion
clear responsibility boundaries
```

---

# 9. Runner

Location:

```text
evals/runners/
```

A runner orchestrates an evaluation experiment.

It is different from an evaluator.

An evaluator answers:

> Does this one input satisfy this one rule?

A runner answers:

> What happened when the entire versioned dataset was executed?

A typical runner performs:

```text
load dataset
        ↓
canonicalize/hash dataset
        ↓
execute every case
        ↓
compare actual result with reviewed expectation
        ↓
calculate summary
        ↓
write evidence report
        ↓
return process exit code
```

---

# Current Stage-1 Runner

File:

```text
evals/runners/run_stage1_reproduction.py
```

This runner:

```text
loads stage1-reproduction-v1.json
calculates its canonical SHA-256
executes reproducible cases
preserves documented non-executable cases
calculates summary results
writes generated evidence
returns non-zero when mismatches occur

```

# Current Deterministic Regression Runner

File:

```text
evals/runners/run_deterministic_evaluator_regression.py
```

This runner executes:

```text
deterministic-evaluator-regression-v1.json
```

Its execution sequence is:

```text
load dataset
        ↓
normalize UTF-8 text to LF
        ↓
calculate canonical SHA-256
        ↓
execute each case through regression.py
        ↓
dispatch to the appropriate evaluator
        ↓
compare actual result with reviewed expectation
        ↓
summarize results overall and by evaluation ID
        ↓
write generated evidence
        ↓
return process exit code
```

The runner currently evaluates 15 reviewed fixtures:

```text
FACT-001    5
INV-004     5
INV-012     5
```

Regression-result statuses use:

```text
PASS
→ actual evaluator outcome matched the reviewed expectation

MISMATCH
→ actual evaluator outcome differed from the reviewed expectation
```

This differs from Stage-1 reproduction statuses such as:

```text
DETECTED
DOCUMENTED
CONFIRMED
```

because the deterministic regression dataset contains designed fixtures rather than historical observations.

The runner returns:

```text
exit code 0
→ no mismatches

exit code 1
→ one or more mismatches
```

This provides the basis for a future CI regression gate.

---

# Why Runner Exit Codes Matter

A runner can eventually participate in CI.

For example:

```text
exit code 0
→ all reviewed expectations matched

exit code 1
→ one or more regression expectations failed
```

A GitHub Actions workflow can use that process result as a release gate.

This turns evaluation from:

```text
manual inspection
```

into:

```text
repeatable engineering control
```

---

# 10. Generated Evidence

Location:

```text
evidence/generated/
```

Generated evidence records what actually happened during an evaluation execution.

This is different from the dataset.

```text
Dataset
→ expected experiment inputs and reviewed expectations

Generated report
→ actual execution results
```

A report may contain:

```text
dataset ID
dataset version
dataset SHA-256
hash basis
execution summary
case results
expected results
actual results
mismatches
```

Generated evaluation results are currently classified as:

```text
EXPERIMENTAL
```

unless another evidence classification is justified.



## Current Deterministic Regression Evidence

Generated report:

```text
evidence/generated/deterministic-evaluator-regression-v1-report.json
```

Current experimental execution result:

```text
total cases:             15
matched expectations:    15
mismatches:               0
all expectations met:  True
```

Per-evaluator result:

```text
FACT-001    5/5 expectations matched
INV-004     5/5 expectations matched
INV-012     5/5 expectations matched
```

Dataset SHA-256:

```text
c0a3acce63e7af5176de0cceda20a8de54fdc90cdafc59e1c4a1679ab9fd6dbc
```

Hash basis:

```text
UTF-8 text normalized to LF line endings before SHA-256
```

The dataset hash was independently recalculated outside the runner and matched the value stored in the generated report.

This supports the scoped statement:

> All 15 reviewed fixtures in `deterministic-evaluator-regression-v1` matched their expected deterministic evaluator outcomes in this experimental execution.

It does not establish complete Reliora reliability or complete coverage of every behavioural invariant.

---

# 11. Evidence Integrity

Reliora uses SHA-256 to identify the dataset used for an evaluation execution.

Text datasets are canonicalized as:

```text
UTF-8
LF line endings
SHA-256
```

This prevents Windows CRLF checkout conversion from producing ambiguous evidence identity.

The intended chain is:

```text
dataset version
        ↓
canonical dataset bytes
        ↓
SHA-256
        ↓
evaluation execution
        ↓
generated report
        ↓
engineering claim
```

---

# 12. Evaluation IDs

Evaluation IDs identify reusable rules.

Examples:

```text
INV-004
INV-012
FACT-001
```

These are different from individual dataset case IDs.

For example:

```text
REG-INV004-001
REG-INV004-002
REG-INV004-003
```

may all test:

```text
INV-004
```

The evaluation ID identifies the general rule.

The case ID identifies one concrete test fixture.

---

# 13. Reproduction IDs

Historical reproduction cases use IDs such as:

```text
REPRO-001
REPRO-002
REPRO-003
REPRO-004
```

These identify concrete historical cases.

For example:

```text
REPRO-001
→ historical Stage-1 response

INV-004
→ reusable behavioural rule used to evaluate it
```

This distinction allows one invariant to be tested against many historical or designed cases.

---

# 14. Evidence vs Expectation

A dataset contains reviewed expectations.

For example:

```text
expected_evaluator_passed = false
```

means:

> The reviewed expectation is that this fixture should violate the evaluator contract.

This is not yet evidence that the evaluator actually behaved that way.

Only after execution can the generated report say:

```text
actual evaluator result = false
expectation matched = true
```

This distinction prevents expected results from being presented as measured results.

---

# 15. Evaluation Sequence in Development

The preferred Reliora evaluation workflow is:

```text
1. Define behavioural requirement

2. Assign evaluation identifier

3. Determine whether the requirement is currently executable

4. Implement deterministic evaluator where appropriate

5. Unit-test the evaluator

6. Create versioned evaluation cases

7. Document dataset scope and limitations

8. Execute through a runner

9. Preserve generated evidence

10. Use evidence to support engineering decisions
```

Requirements that depend on architecture not yet implemented remain documented until the necessary system boundary exists.

Reliora does not create artificial evaluator coverage merely to increase coverage counts.

---

# 16. Current Evaluation Maturity

Currently executable evaluator families include:

```text
INV-004
incremental bug-field collection

INV-012
initial internal-information leakage detection

FACT-001
required-fact lexical completeness
```

Other documented invariants will become executable as their corresponding architecture is implemented.

Examples include:

```text
routing
knowledge coverage
tool authorization
idempotency
backend confirmation
handoff
data minimisation
```

---

# 17. Claim Discipline

Passing an evaluation dataset supports only claims within that dataset's scope.

For example:

```text
All 15 reviewed fixtures in
deterministic-evaluator-regression-v1
matched their expected deterministic outcomes.
```

is defensible after a successful run.

The following would not be supported:

```text
Reliora is 100% reliable.

Every behavioural invariant is solved.

The system is production-ready.
```

Evaluation evidence must not be stronger than the experiment that produced it.

---

# 18. Long-Term Role of This Subsystem

As Reliora grows, the evaluation system can expand to cover:

```text
routing accuracy
knowledge-coverage decisions
tool argument validation
authorization boundaries
idempotency
backend-result provenance
structured handoff
data minimisation
security/adversarial cases
model comparisons
latency
cost
operational reliability
```

The architecture should remain:

```text
requirement
→ evaluator
→ versioned dataset
→ runner
→ evidence
→ engineering decision
```

rather than allowing evaluation logic to become scattered throughout the application.