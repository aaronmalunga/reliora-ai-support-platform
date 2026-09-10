# Reliora Metric Dictionary

**Project:** Reliora AI Support Platform
**Document type:** Metric governance and semantic contract
**Established:** 2026-09-09
**Status:** ACTIVE

---

## 1. Purpose

This document defines the canonical meaning of important Reliora metrics.

Its purpose is to prevent metric drift, ambiguous reporting, misleading comparisons, and unsupported production claims.

A metric appearing in source code, an experiment, a dashboard, a benchmark, or an evidence artifact does not automatically make that metric a production KPI.

Every material metric should have:

- a stable name;
- a clear definition;
- a measurement boundary;
- a unit;
- a source of truth;
- an aggregation method;
- an evidence classification;
- an evidence maturity level where established;
- a claim boundary;
- and an owner.

---

## 2. Governing Rules

### 2.1 Measurement boundary is part of the metric

Two measurements with the same label are not equivalent if their execution scopes differ.

For example:

```text
local in-process p95 latency
!=
Lambda p95 latency
!=
Gateway-to-Lambda p95 latency
!=
end-to-end customer-request p95 latency
```

````

The measurement boundary must therefore accompany any important latency, throughput, reliability, or cost claim.

### 2.2 Local evidence is not cloud evidence

Measurements produced by local in-process experiments may establish local baselines.

They must not be represented as:

- AWS service capacity;
- production throughput;
- production latency;
- production availability;
- production scalability;
- production unit economics.

### 2.3 Targets follow baselines

Reliora does not select numerical latency, throughput, concurrency, availability, cost, SLO, or error-budget targets merely because a number appears desirable.

Targets must follow relevant baseline measurement and business requirements.

### 2.4 Evidence class and evidence maturity are separate

A metric result may have an evidence class such as:

- `MEASURED`;
- `OBSERVED`;
- `VERIFIED`;
- `EXPERIMENTAL`;
- `SYNTHETIC`;
- `TARGET`.

It may separately have an evidence maturity level such as E0 through E9.

These dimensions must not be conflated.

### 2.5 No silent metric redefinition

If the calculation, workload, aggregation method, dataset, measurement boundary, or source changes materially, the metric definition or version must change.

---

# 3. Routing Quality Metrics

## Routing Accuracy

**Definition**

Fraction of evaluated routing examples for which the predicted top-level route equals the expected route.

**Formula**

```text
correct routing predictions / total evaluated routing examples
````

**Unit**

Ratio or percentage.

**Current source of truth**

Routing benchmark and evaluation artifacts under:

```text
experiments/routing/
```

**Aggregation**

Across the explicitly identified evaluation dataset.

**Evidence class**

`EXPERIMENTAL` for controlled experiment results.

**Evidence maturity**

To be classified in the evidence maturity register.

**Claim boundary**

Measures routing classification correctness on the identified dataset only.

It does not by itself demonstrate production customer-support accuracy.

**Owner**

Reliora AI/ML evaluation.

---

## Routing Macro F1

**Definition**

Unweighted mean of the per-class F1 scores across the routing classes included in the evaluated dataset.

**Unit**

Ratio from 0 to 1.

**Current source of truth**

Routing benchmark artifacts under:

```text
experiments/routing/
```

**Aggregation**

Macro-average across evaluated routing classes.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

To be classified in the evidence maturity register.

**Claim boundary**

Represents balanced classification performance across the evaluated route classes.

It must not be interpreted as end-to-end support-resolution quality.

**Owner**

Reliora AI/ML evaluation.

---

## BUG Route Recall

**Definition**

Fraction of examples whose expected class is `BUG` that are correctly classified as `BUG`.

**Formula**

```text
true BUG predictions / all expected BUG examples
```

**Unit**

Ratio or percentage.

**Current source of truth**

Routing benchmark and selection artifacts under:

```text
experiments/routing/
```

**Aggregation**

Across BUG-labelled cases in the identified evaluation dataset.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

To be classified in the evidence maturity register.

**Claim boundary**

Measures the router's ability to recognize BUG cases in the evaluated dataset.

It does not prove successful ticket completion.

**Owner**

Reliora AI/ML evaluation.

---

# 4. Local Routing Performance Metrics

## Local Routing Inference p50

**Definition**

Median local routing inference time under the documented routing benchmark protocol.

**Unit**

Milliseconds per message.

**Current source of truth**

```text
experiments/routing/results/routing-operational-evidence-v1.json
```

**Aggregation**

50th percentile over the documented local inference workload.

**Evidence class**

`EXPERIMENTAL`.

**Claim boundary**

Local routing inference only.

Excluded unless explicitly measured:

* network latency;
* AWS service latency;
* API transport;
* cold starts;
* queueing;
* downstream tool latency;
* end-to-end request handling.

**Owner**

Reliora performance engineering.

---

## Local Routing Inference p95

**Definition**

95th-percentile local routing inference time under the documented routing benchmark protocol.

**Unit**

Milliseconds per message.

**Current source of truth**

```text
experiments/routing/results/routing-operational-evidence-v1.json
```

**Aggregation**

95th percentile over the documented local inference workload.

**Evidence class**

`EXPERIMENTAL`.

**Claim boundary**

Local routing inference only.

This is not production API p95 latency.

**Owner**

Reliora performance engineering.

---

# 5. Local Ticket Runtime Performance Metrics

The following metrics currently come from:

```text
experiments/performance/results/local-ticket-runtime-v1.json
```

The experiment executes:

```text
LambdaBugReportRuntime.handle
```

locally and in-process.

Its current evidence classification is:

```text
EXPERIMENTAL
```

Its current evidence maturity is:

```text
E3 — LOCAL SYNTHETIC MEASURED
```

The experiment explicitly excludes AWS Lambda infrastructure, Lambda cold starts, Lambda service scheduling/scaling, AgentCore, Gateway network/service overhead, DynamoDB service/network latency, AWS throttling, AWS billing, and external network latency.

---

## Local Ticket Runtime Throughput

**Definition**

Number of completed local runtime invocations divided by total wall-clock workload execution time.

**Formula**

```text
completed requests / workload wall-clock seconds
```

**Unit**

Requests per second.

**Aggregation**

Calculated separately for each requested experimental concurrency level.

**Current evidence**

The v1 benchmark measured 25,000 requests at each of four requested concurrency levels:

```text
1
2
4
8
```

for 100,000 measured requests in total.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

This is local in-process throughput.

It is not AWS Lambda throughput, system capacity, customer throughput, or production scalability evidence.

**Owner**

Reliora performance engineering.

---

## Local Ticket Runtime Mean Latency

**Definition**

Arithmetic mean of the measured `LambdaBugReportRuntime.handle` execution durations for a defined benchmark workload.

**Unit**

Milliseconds.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

Worker execution time only.

Executor queue wait and cloud/service/network latency are excluded.

**Owner**

Reliora performance engineering.

---

## Local Ticket Runtime p50 Latency

**Definition**

50th-percentile measured local runtime execution duration.

**Unit**

Milliseconds.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

Local in-process runtime execution only.

**Owner**

Reliora performance engineering.

---

## Local Ticket Runtime p95 Latency

**Definition**

95th-percentile measured local runtime execution duration.

**Unit**

Milliseconds.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

Local in-process runtime execution only.

It must not be reported as end-to-end or production p95.

**Owner**

Reliora performance engineering.

---

## Local Ticket Runtime p99 Latency

**Definition**

99th-percentile measured local runtime execution duration.

**Unit**

Milliseconds.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

Local in-process runtime execution only.

**Owner**

Reliora performance engineering.

---

## Local Benchmark Failure Rate

**Definition**

Fraction of measured benchmark requests that terminate as failed requests.

**Formula**

```text
failed requests / total measured requests
```

**Unit**

Ratio or percentage.

**Current evidence**

The `local-ticket-runtime-v1` benchmark observed:

```text
0 failures / 100,000 measured requests
```

within the defined local synthetic experiment.

**Evidence class**

`EXPERIMENTAL`.

**Evidence maturity**

`E3 — LOCAL SYNTHETIC MEASURED`.

**Claim boundary**

This demonstrates zero observed failures only within the documented local benchmark workload.

It does not establish production availability or production failure rate.

**Owner**

Reliora reliability/performance engineering.

---

# 6. Deterministic Behaviour Metrics

## Duplicate Side-Effect Rate

**Definition**

Fraction of matching retry scenarios in which more than one backend side effect is created for one authorized logical operation.

**Formula**

```text
matching-retry scenarios producing duplicate side effects
/
total matching-retry scenarios
```

**Desired semantic invariant**

```text
0 duplicate executions
```

This is a correctness invariant, not yet a production SLO.

**Current evidence source**

Unit and integration tests around ticket execution, idempotency, operation identity, and backend result replay.

**Cloud status**

`BLOCKED` for live Lambda/DynamoDB verification.

**Owner**

Reliora reliability engineering.

---

## Matching Retry Replay Correctness

**Definition**

Fraction of matching retry scenarios that return the previously authoritative result without executing the side effect again.

**Formula**

```text
correct matching replays / total matching-retry scenarios
```

**Current evidence source**

Deterministic ticket execution tests.

**Cloud status**

Live AWS verification remains `BLOCKED`.

**Owner**

Reliora reliability engineering.

---

## Conflicting Retry Rejection Correctness

**Definition**

Fraction of same-operation-ID scenarios with materially changed payloads that are rejected without executing a new side effect.

**Formula**

```text
correctly rejected conflicting retries
/
total conflicting-retry scenarios
```

**Current evidence source**

Deterministic ticket execution tests.

**Cloud status**

Live AWS verification remains `BLOCKED`.

**Owner**

Reliora reliability engineering.

---

# 7. Evaluation Metrics

## Deterministic Regression Pass Rate

**Definition**

Fraction of deterministic regression cases whose observed result satisfies the expected contract.

**Formula**

```text
passing deterministic cases / total deterministic cases
```

**Current source of truth**

```text
evidence/generated/deterministic-evaluator-regression-v1-report.json
```

and its associated runner/dataset card.

**Evidence class**

Controlled generated results use the evidence classification recorded in the artifact.

**Claim boundary**

Measures the covered deterministic regression contract only.

It does not establish production availability or end-user success.

**Owner**

Reliora evaluation engineering.

---

## Stage-1 Reproduction Pass Rate

**Definition**

Fraction of versioned Stage-1 reproduction cases that satisfy their expected behaviour.

**Formula**

```text
passing reproduction cases / total reproduction cases
```

**Current source of truth**

```text
evidence/generated/stage1-reproduction-v1-report.json
```

and its associated runner/dataset card.

**Claim boundary**

Measures the defined Stage-1 reproduction dataset and evaluator only.

**Owner**

Reliora evaluation engineering.

---

# 8. Cloud / Target-Environment Metrics

The following metrics are required or anticipated by Reliora's NFRs but are not currently supported by live target-environment evidence.

They must remain `TARGET`, `TBD`, or `BLOCKED` as appropriate.

---

## End-to-End Request Latency

**Definition**

Elapsed time from the defined external request-entry boundary until the defined final response boundary.

**Required reporting**

Where useful:

```text
p50
p95
p99
```

**Current status**

`BLOCKED — no active AWS target environment`.

No numerical production target is currently established.

---

## Model / Agent Latency

**Definition**

Elapsed time attributable to model or managed-agent execution within an end-to-end request.

**Current status**

`BLOCKED`.

---

## Tool Execution Latency

**Definition**

Elapsed time attributable to controlled tool execution.

**Current status**

`BLOCKED`.

---

## DynamoDB Operation Latency

**Definition**

Observed latency of the relevant live DynamoDB operations used by Reliora.

**Current status**

`BLOCKED`.

---

## End-to-End Failure Rate

**Definition**

Fraction of eligible requests that fail to reach their defined acceptable outcome.

**Formula**

```text
failed eligible requests / total eligible requests
```

The definition of "eligible request" and "acceptable outcome" must be frozen before production reporting.

**Current status**

`BLOCKED`.

---

## Availability

**Definition**

To be established only after the service boundary and availability semantics are defined.

**Current status**

`TBD TARGET`.

No production availability claim currently exists.

---

# 9. FinOps Metrics

## Cost per Request

**Definition**

Total attributable service cost divided by the number of requests within the same defined measurement window and environment.

**Formula**

```text
attributable cost / request count
```

**Current status**

Cloud measurement `BLOCKED`.

No production unit-cost claim currently exists.

---

## Cost per Successful Eligible Resolution

**Definition**

Total attributable cost divided by successfully completed eligible support resolutions within the same defined window.

**Formula**

```text
attributable cost / successful eligible resolutions
```

The definition of "successful eligible resolution" must be frozen before reporting.

**Current status**

Cloud measurement `BLOCKED`.

---

## Model Calls per Request

**Definition**

Number of model or managed-agent invocations attributable to a request.

**Unit**

Calls per request.

**Current status**

Target-environment measurement `BLOCKED`.

---

## Tokens per Request

**Definition**

Model input/output token usage attributable to a request, using the token accounting exposed by the selected model/runtime where available.

**Unit**

Tokens per request.

**Current status**

Target-environment measurement `BLOCKED`.

---

## Tool Calls per Request

**Definition**

Number of controlled external/business-tool invocations attributable to a request.

**Unit**

Tool calls per request.

**Current status**

Target-environment measurement `BLOCKED`.

---

# 10. SLI / SLO / Error-Budget Position

Reliora does not yet have sufficient target-environment evidence to establish defensible production SLOs.

Therefore:

```text
SLIs            DEFINITIONS MAY BE PREPARED
SLO thresholds  TBD TARGET
Error budgets   DEFERRED
SLA claims      NOT ESTABLISHED
```

Local synthetic measurements must not be converted directly into production SLOs.

---

# 11. Metric Promotion Rule

A metric may move from local experimental evidence toward a production-facing operational metric only when its evidence boundary advances appropriately.

Example:

```text
local experiment
    ↓
local integration evidence
    ↓
target-environment integration
    ↓
controlled cloud measurement
    ↓
end-to-end deployed measurement
    ↓
real beta observation
    ↓
production observation
```

Advancing a metric's maturity requires new evidence.

Changing only its documentation does not advance maturity.

---

# 12. Metric Change Control

A material metric definition change must record:

* metric ID;
* old definition;
* new definition;
* reason for change;
* affected evidence;
* whether historical comparisons remain valid;
* effective version/date.

Historical experiment artifacts must not be silently rewritten to conform to a new definition.

---

# 13. Current Governance Position

Reliora currently has useful local routing, evaluation, and ticket-runtime measurements.

These measurements provide evidence within their documented boundaries.

They do not currently establish:

* production latency;
* production throughput;
* production availability;
* production scalability;
* production SLO compliance;
* production error-budget performance;
* production unit economics.

Those claims require later target-environment evidence.

> **A metric is not just a number. Its definition, boundary, provenance, aggregation rule, and evidence maturity are part of the result.**
