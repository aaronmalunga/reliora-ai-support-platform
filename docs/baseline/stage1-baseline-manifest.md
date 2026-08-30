# Stage-1 Baseline Manifest

## Purpose

This document records the immutable engineering baseline from which Reliora is derived.

Reliora does not replace or rewrite the original Stage-1 implementation. The original project remains independently preserved so that improvements made during production hardening can be evaluated against a known working baseline.

## Original Project

**Repository:** aws-agentcore-customer-support-chatbot

**Project context:** AWS/Udacity customer-support chatbot built using Amazon Bedrock AgentCore.

## Baseline Architecture

The Stage-1 system implemented the following high-level path:

Customer request
→ AgentCore Harness
→ prompt-based routing
→ supported FAQ response, human handoff, or bug-report workflow

For bug-report workflows:

AgentCore Harness
→ AgentCore Gateway
→ AWS Lambda
→ Amazon DynamoDB

## Demonstrated Stage-1 Capabilities

The baseline demonstrated:

- prompt-based classification across support scenarios;
- multi-turn collection of required bug-report information;
- AgentCore Gateway tool invocation;
- Lambda execution;
- DynamoDB ticket persistence;
- embedded FAQ-based platform answers;
- human handoff behaviour;
- automated Bedrock evaluation.

## Original Evaluation Result

The submitted evaluation contained 6 prompts.

Reported Bedrock correctness result:

**6 / 6 prompts scored 1**

**Aggregate correctness: 1.00**

This result is preserved as an observed Stage-1 outcome. It is not treated as proof that all behavioural requirements were satisfied.

## Known Evaluation Gaps Identified During Audit

Subsequent review identified behavioural violations that the aggregate correctness score did not expose.

Examples included:

1. A bug-report response requested multiple missing fields at once despite the prompt contract requiring one missing field at a time.
2. A handoff response exposed the internal route label even though route names were intended to remain internal.
3. A development transcript exposed reasoning tags before a tool invocation.
4. A policy response omitted part of the expected policy detail while still receiving a correctness score of 1.

These findings motivate Reliora's separation of:

- deterministic behavioural invariants;
- side-effect validation;
- generative-quality evaluation;
- operational metrics.

## Baseline Provenance

The Stage-1 baseline is identified through two independently recorded provenance references.

### Public Repository

**Repository:** `aws-agentcore-customer-support-chatbot`

**Verified Git commit:**

`2da594b1126c566a593f31891f25a6f4ea4afa53`

**Short SHA:**

`2da594b`

**Commit message:**

`Rename E52_eval-per-prompt-results.png to E52_per-prompt-results.png`

### Submitted Archive

**Submission archive SHA-256:**

`fdc1c233977422cf15482663759d3bb424547591c3b6a7388aea5fdf5d9eda7d`

The submitted archive did not contain its `.git` directory.

Therefore, Reliora records the verified public Git commit and the submitted archive hash separately rather than claiming cryptographic proof that the archive bytes correspond exactly to that Git commit.

### Key Baseline Artifact Hashes

| Artifact | SHA-256 |
|---|---|
| `system_prompt.txt` | `08d51fa123bcf73e088aceaf5ba71a427c4185af92f3b005fef14e8746dfc8d2` |
| `harness-tests.json` | `69b61558ee815be95c411f274f090aa7cc8b3475137d99dd21759e6445a1418c` |
| `output_eval_dataset.jsonl` | `adbca1abe644698a1de34262353b40b0358df816a9d9bdcd3c9dfdeb7dbabb68` |
| `ARCHITECTURE.md` | `278e44c1a28ee41eba61ae452cae574f650db6d2190e95e5440116ed24d29bc6` |
| `create_bug_report.py` | `348717b8d8d0fe32460e773e8e7d969916bc1035602b09373e67b4b84cb1b54b` |
| `create_harness.py` | `117d61c233b7cd0865abf4b77536a0854266aba80d1c176f9ae85990b181b8dc` |
| `setup_gateway.py` | `eaa8e0f26acd0be7d0c0688bc042d4bbd6745f0210b454d98925cc8f5cfe4138` |
| `cloudformation-tool.yaml` | `cea9344592cefe2a788c431cd41bd5439acdeb04fb5e6afd0d28e69cedbc06f8` |

These hashes allow future comparisons to distinguish changes in Reliora from changes in the original Stage-1 artifacts.

## Evidence Classification

The following terms are used throughout Reliora:

- **MEASURED** — obtained from a defined measurement procedure.
- **OBSERVED** — directly seen during implementation or testing.
- **EXPERIMENTAL** — produced in a controlled experiment.
- **TARGET** — desired future threshold, not yet achieved.
- **SYNTHETIC ASSUMPTION** — invented deliberately for workload or scenario modelling and not presented as real production data.

## Baseline Status

**Status: FROZEN**

The Stage-1 baseline provenance was independently recorded before Reliora behavioural implementation began.

Reliora may reproduce or evaluate the baseline, but the original Stage-1 artifacts are not modified as part of P1-S2.
