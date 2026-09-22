# Start here: continue Reliora

Prepared 2026-09-22. This is an engineering continuation checkpoint, not a production release certificate.

## First ten minutes

1. Read [agent instructions](../../AGENTS.md) and [current state](CURRENT_STATE.md).
2. Inspect the real branch, commit, local changes, and upstream. The preparation branch is `chore/reliora-handover-readiness`; `main` was still the older baseline at preparation time.
3. Read [verification evidence](VERIFICATION_MANIFEST.json), then [next steps](NEXT_STEPS.md). Separate completed work from verification debt.
4. Read the [constitution](../product/reliora-product-constitution.md), [North Star](../../RELIORA-PRODUCT-NORTH-STAR.md), and [source map](SOURCE_MAP.md).
5. Read the [discovery gate](../discovery/customer-discovery-brief.md), [business case](../business/business-case.md), and [ADR-017](../architecture/adr/ADR-017-trusted-execution-identity.md).
6. Reproduce only the checks needed for your task using [VERIFY.md](VERIFY.md), and report actual outcomes before changing claims.

## What to continue

Reliora already has local deterministic safety and evaluation foundations. Preserve them. Discovery repair is recorded complete with a NARROW decision; do not repeat it because an older audit predates its completion. Trusted identity through real AgentCore/Gateway/Lambda remains unverified and requires the smallest applicable experiment after AWS authentication succeeds.

The immediate handover work is to complete the applicable evaluator, packaging, infrastructure, and security evidence; record the final continuation commit; and finish a reviewed integration path. GitHub Actions billing and AWS authentication are distinct blockers. Pending cloud evidence must stay pending while independent repository work proceeds.

## Readiness boundaries

| State | Meaning |
|---|---|
| Continuation checkpoint | Source and governance are consolidated on a known branch, with instructions and explicit limitations. |
| Fully verified handover | Applicable reproduction and security checks have evidence, review is complete, final commit is pinned, and the export is verified. Not yet claimed. |
| Cloud-verified product | Actual identity, side effects, failures, recovery, deployment, and cost/latency behavior are demonstrated within a stated workload. Not yet claimed. |
| Commercial pilot | Relevant buyer/workflow evidence, agreed outcomes, operational ownership, and suitable controls exist. Not yet claimed. |

## Receiver's first response

Report the actual branch/commit, dirty or unpushed work, implemented capabilities, evidence boundaries, blockers, and the next bounded task with acceptance criteria. Then perform that task under the applicable authorization. A summary alone does not complete the transfer.

## Transfer package

Prefer authenticated private repository access plus this entry point. A text-only LLM also needs a source archive and a human or coding environment to execute changes. Generate the final source archive from the final reviewed commit, identify that commit outside the archive, and record its SHA-256 checksum. A ZIP omits Git history and PR/issues/settings; include material decision summaries or retain authenticated access.

The current documents are not the final archive, and no final handover tag or archive checksum has been issued. The supporting external source attachments listed in [SOURCE_MAP.md](SOURCE_MAP.md) must accompany a complete context transfer until they are deliberately canonicalized in Git. Review export content for secrets; do not include environment files, credentials, Terraform state/plans, customer records, or unredacted logs.
