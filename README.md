# Reliora

**Production AI Support Reliability & Control Platform**

Reliora is a production-engineering case study focused on making AI-assisted customer support systems more reliable, observable, testable, and operationally safe on AWS.

The project evolves from a successful Amazon Bedrock AgentCore customer-support implementation into a more rigorous system centered on deterministic behavioural evaluation, safe tool execution, idempotency, structured human escalation, observability, release safety, and cost-aware operation.

## Current Status

**Phase 0 — Foundation and baseline definition**

The repository is being built evidence-first. Claims about reliability, latency, cost, scalability, or production readiness will be classified as measured, observed, experimental, target, or synthetic assumption.

## Engineering Principles

- Preserve proven functionality before redesigning it.
- Use deterministic software to enforce hard behavioural requirements.
- Use LLM-based evaluation for qualities that genuinely require judgement.
- Treat retries and partial failures as normal distributed-systems behaviour.
- Prefer simple managed infrastructure until measurements justify additional complexity.
- Keep human escalation explicit for unsupported, ambiguous, or failed automation.
- Do not record or depend on hidden chain-of-thought for operational auditability.

## Technology Direction

The planned implementation uses Python 3.12, Amazon Bedrock and Bedrock AgentCore, AWS Lambda, Amazon DynamoDB, CloudWatch, Terraform, GitHub Actions, pytest, and selected ML evaluation tooling.

Technology is added only when it addresses a documented requirement.

## Origin

Reliora is a separate production-hardening project derived from lessons learned while building an AWS/Udacity customer-support agent. The original implementation remains preserved independently as the Stage-1 baseline.

Detailed baseline provenance, architecture decisions, evaluation methodology, and measured results will be documented as the project develops.

## Project Status

This repository is under active development.
