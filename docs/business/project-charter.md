# Reliora Project Charter

## Project

**Reliora — Production AI Support Reliability & Control Platform**

## Problem Statement

A functionally successful tool-using AI customer-support system can still violate behavioural requirements while appearing correct under aggregate LLM-based evaluation.

Reliora investigates how to operate such systems with stronger engineering controls around behaviour, side effects, observability, human escalation, release safety, security, and cost.

## Core Engineering Question

How can an AI-assisted customer-support system preserve the flexibility of generative models while ensuring that critical operational behaviours are enforced, measured, and auditable?

## Primary Objectives

Reliora will:

1. separate intent routing from knowledge coverage;
2. represent critical inputs and outputs through typed contracts;
3. enforce hard behavioural requirements deterministically;
4. make side-effecting tool calls retry-safe and idempotent;
5. implement structured human escalation;
6. provide request and operation traceability;
7. evaluate generative quality separately from behavioural correctness;
8. establish repeatable release and regression gates;
9. measure latency, reliability, and cost before making scalability claims;
10. document architecture decisions and operational trade-offs.

## Architectural Principle

**The LLM may propose; deterministic software validates and authorizes.**

## Scope Boundary

Reliora is not intended to demonstrate every available AI technology.

Capabilities such as multi-agent orchestration, persistent customer memory, browser automation, code interpretation, Kubernetes, Kafka, and mandatory RAG are outside the initial scope unless a measured requirement later justifies them.

Modern AWS capabilities such as Bedrock Structured Outputs, AgentCore Evaluations, AgentCore Optimization, Guardrails, Policy, or other newly released services will be adopted only where they directly strengthen a documented requirement.

Preview services will not become critical runtime dependencies.

## Portfolio Intent

Reliora is an engineering case study demonstrating production-oriented AI/ML Solutions Architecture practices on AWS.

It does not claim real enterprise traffic, customers, incidents, revenue, ROI, or production scale unless such evidence genuinely exists.

## Evidence Discipline

Project claims will use the following classifications:

- **MEASURED** — obtained through a defined measurement procedure.
- **OBSERVED** — directly seen during implementation or testing.
- **EXPERIMENTAL** — produced through a controlled experiment.
- **TARGET** — a desired threshold that has not yet been demonstrated.
- **SYNTHETIC ASSUMPTION** — deliberately invented for scenario or workload modelling and never presented as real production data.

## Current Phase

**Phase 0 — Foundation and baseline definition**
