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

The exact Stage-1 repository commit, submission archive hash, and evidence references will be recorded and independently verified before the baseline is declared frozen.

## Evidence Classification

The following terms are used throughout Reliora:

- **MEASURED** — obtained from a defined measurement procedure.
- **OBSERVED** — directly seen during implementation or testing.
- **EXPERIMENTAL** — produced in a controlled experiment.
- **TARGET** — desired future threshold, not yet achieved.
- **SYNTHETIC ASSUMPTION** — invented deliberately for workload or scenario modelling and not presented as real production data.

## Baseline Status

**Status: PROVISIONAL**

The baseline becomes FROZEN only after its Git commit, archive hash, and supporting evidence have been independently verified.
