# Reliora

**AI Customer-Support Reliability and Control Platform for Online Commerce**

Reliora develops the controls needed to make AI-assisted support safe to operate: deterministic authorization, retry-safe side effects, authoritative backend results, human fallback, behavioral evaluation, and useful operational evidence.

**The LLM may propose; deterministic software validates and authorizes.**

## Start here

Continue development through [the handover entry point](docs/handover/START_HERE.md), [current state](docs/handover/CURRENT_STATE.md), and [ordered next steps](docs/handover/NEXT_STEPS.md). Coding agents must read [AGENTS.md](AGENTS.md).

## Current maturity

As of 2026-09-22, Reliora is a bounded production-oriented reference implementation. M1 lifecycle repair is recorded complete; its product decision is **NARROW**. M2, the trusted identity experiment, is blocked on authenticated AWS access. [ADR-017](docs/architecture/adr/ADR-017-trusted-execution-identity.md) remains PROPOSED.

| Evidence | Current boundary |
|---|---|
| Local checks reported on 2026-09-22 | Ruff passed; mypy passed for 31 source files; 208 tests passed in 16.67 seconds at the pre-merge code baseline. |
| Security/privacy consolidation | Merged on the handover branch at `bb55f983c18b3abe618291be0e8468bd38b96223`; only three documentation files changed. |
| GitHub Actions | Execution blocked by account billing, confirmed in the user's GitHub screenshot; no passing hosted CI claim. |
| AWS integration | Latest recorded entry gate failed with `InvalidClientTokenId` on 2026-09-18; current credentials have not been rechecked. |
| Product experience and pilot | Full storefront/operator experience, current cloud verification, and commercial validation remain incomplete. |

The [verification manifest](docs/handover/VERIFICATION_MANIFEST.json) distinguishes user-reported results, historical records, and checks still pending. There is no current production-reliability, customer-adoption, or ROI claim.

## Product scope

- **BUG:** collect description, reproduction steps, and environment; validate and authorize ticket creation; return a confirmed backend identifier.
- **PLATFORM:** answer from approved, versioned knowledge; escalate unsupported questions.
- **OTHER / explicit human request:** provide an appropriate human fallback; structured handoff implementation is outstanding.

The functional baseline comes from the preserved Stage-1 project. These are intended product workflows; their complete current AWS execution is not yet demonstrated. Autonomous refunds, broad order management, mandatory RAG, multi-agent systems, and enterprise multi-tenancy are not admitted by the current scope decision.

## Local engineering checks

Prerequisites: Git, uv, and Python 3.12 (the repository's required minor version). From the repository root, run each complete command separately:

```powershell
uv sync --frozen
uv run --frozen ruff check .
uv run --frozen mypy src
uv run --frozen python -m pytest -q
```

`--frozen` prevents lockfile updates. Synchronization may download packages and update the local virtual environment. Ruff reports lint violations, mypy checks `src`, and pytest runs the configured tests with a concise summary. Expect no lint/type errors and no failed tests; report the actual count. Stop and investigate a failed command. These commands do not deploy AWS resources. See [the verification guide](docs/handover/VERIFY.md) for evaluator, packaging, and Terraform checks and their effects.

## Repository map

| Path | Responsibility |
|---|---|
| `src/reliora/` | Domain, policy, execution, provider, AWS adapter, telemetry, and evaluator code |
| `tests/` | Automated regression checks |
| `evals/` | Behavioral contracts, reviewed fixtures, dataset cards, and runners |
| `experiments/` | Bounded investigations and frozen routing evidence |
| `evidence/` | Results with scope and maturity limitations |
| `infra/terraform/envs/dev/` | Development infrastructure definitions |
| `scripts/` | Operational scripts, including Lambda packaging |
| `docs/` | Requirements, architecture, decisions, governance, operations, and handover |

## Governance and provenance

Read the [constitution](docs/product/reliora-product-constitution.md), [North Star](RELIORA-PRODUCT-NORTH-STAR.md), [discovery gate](docs/discovery/customer-discovery-brief.md), and [business case](docs/business/business-case.md). The [source map](docs/handover/SOURCE_MAP.md) identifies authoritative and historical sources.

The [Stage-1 manifest](docs/baseline/stage1-baseline-manifest.md) preserves the original AWS/Udacity implementation. The separate [learning ledger](https://github.com/aaronmalunga/aws-agentic-ai-learning-ledger) captures transferable reasoning and interview preparation; implementation truth stays here.
