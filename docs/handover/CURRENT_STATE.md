# Reliora current state

Snapshot: 2026-09-22. Update when actual work or evidence changes; retain dated historical evidence.

## Canonical continuation line

- Repository: `aaronmalunga/reliora-ai-support-platform` (private).
- Preparation branch: `chore/reliora-handover-readiness`.
- Consolidated source parent: `bb55f983c18b3abe618291be0e8468bd38b96223`.
- Its parents are `0b9ab45781612e81759816dd9fe288b1088e0e0d` (implementation/discovery line) and `34ff019af529abc99f2e255913befd73554b1c4c` (security/privacy line).
- The consolidation changes only three documentation files. This handover documentation is added after that checkpoint; obtain its enclosing commit from Git. Do not mistake the parent checkpoint for the eventual final export SHA.
- `main` was `cc02e5838dda9d1ded121008d86a04526e6e273e` when inspected. It is not yet the consolidated continuation baseline.
- Existing PR #1 (infrastructure) and PR #2 (security/privacy) remain part of the historical review context. The consolidated branch contains both lines; final integration must explicitly account for or supersede those PRs, preserving their discussions.

Aaron's reported pre-merge worktree was clean. After fetching, no commits reachable from local branches were absent from all remote-tracking branches. His post-merge push reported a clean branch tracking the matching remote at `bb55f98`. This does not inspect ignored workstation files or prove future local state.

## Product and lifecycle

The product serves the reliability/control needs of AI-assisted online-commerce support. Its bounded scope is BUG / PLATFORM / OTHER with human fallback. Target buyers and business value remain hypotheses; no commercial adoption or ROI is established.

| Stage | Current state |
|---|---|
| M0 baseline | Historical baseline accepted; fresh local lint/type/test output also supplied in this session. |
| M1 discovery/lifecycle repair | Recorded complete; decision NARROW. |
| M2 trusted execution identity | BLOCKED at AWS entry gate; ADR-017 remains PROPOSED. |
| M3 structured handoff | Still outstanding; a local branch named `feat/structured-handoff-contract` pointed to the same code checkpoint and contained no additional commits at inspection. |
| M4 release controls | Existing static/unit/build workflow; standalone evaluator and security-gate completion outstanding; hosted execution blocked. |
| M5 operability | Security/privacy documents consolidated. Full telemetry wiring, request reconstruction, deployment provenance, and recovery proof outstanding. |
| M6 cloud evidence | Not established for the current architecture. |
| M7 product experience | Complete reference customer/operator experience outstanding. |
| M8 release/handoff | This engineering handover is in progress; final release evidence and archive pending. |

See the existing [mitigation plan](../audit/RELIORA_MITIGATION_PLAN.md) for stage definitions. Its 2026-09-16 starting snapshot is historical; later completion evidence supersedes its old status descriptions, not its justified requirements.

## Implementation and evidence boundaries

Existing code includes domain contracts, deterministic authorization, operation identity, replay/conflict handling, backend-confirmed results, local execution, DynamoDB transactional execution/reconciliation, Lambda boundaries, failure telemetry contracts/emission, and deterministic evaluators. Routing experiments and infrastructure definitions exist. Availability in source does not establish live AWS behavior or a full working product UI.

User-reported checks on the pre-merge `0b9ab45` baseline:

| Actual command | Reported result |
|---|---|
| `uv sync --frozen` | Checked 38 packages |
| `ruff check` | All checks passed |
| `mypy src` | No issues in 31 source files |
| `python -m pytest -q` | 208 passed in 16.67 seconds |

Aaron invoked the latter commands directly in the active PowerShell environment after entering incomplete `uv run --frozen` prefixes. Those prefixes printed usage help and did not run checks. The successful commands above are the actual observed transcript, not rewritten as uv-wrapped executions. Interpreter/tool versions and exit codes were not captured for that earlier run. These results were not executed by the receiving agent or hosted CI.

Aaron subsequently fast-forwarded to `f5323827a629e8589e3b50fb638c2e8af6133cd9` and reported both evaluator runners passing: 15/15 regression expectations and zero Stage-1 mismatches, with three expected historical defects detected. Lambda packaging and the workflow-equivalent ZIP inspection passed, including the Linux x86_64 pydantic-core binary. Terraform fmt/init/validate passed using Terraform 1.15.8 and AWS provider 6.62.0; Python 3.12.10 and uv 0.12.7 were reported. Numeric exit codes and execution timestamps remain unknown. The workflow pins Terraform 1.15.9, so local and CI tool versions differ. See [the manifest](VERIFICATION_MANIFEST.json) for actual commands and limitations.

The two generated JSON reports showed only CRLF-to-LF warnings and no content diff. Explicit staging subsequently produced no staged diff and a clean worktree. Aaron then fast-forwarded to `8d95afa829a2686ae50a10d57a3518ba181eb407`. No application source changes were reported.

The older [2026-09-17 baseline](../../evidence/post-audit-engineering-baseline-2026-09-17.md) remains historical. The [September 8 security record](../security/security-scan-baseline.md) records zero Gitleaks findings, no known runtime dependency vulnerabilities at scan time, and 36 passing / 12 failing Checkov checks with dispositions. It does not certify a new release.

Fresh security scans were reported at `8d95afa`: Gitleaks 8.30.1 scanned 73 commits with zero leaks (exit 0); pip-audit 2.10.1 reported no known runtime vulnerabilities (exit 0); Checkov 3.3.16 reported 36 passed / 12 failed / 0 skipped. All 12 check/resource failures match the existing finding register. Their existing development dispositions remain, including open code-signing, concurrency, and tracing gaps and pending DLQ semantics verification. No production risk acceptance or clean IaC scan is claimed. The successful Checkov run's numeric exit-code output was not included. Its earlier pyenv launcher failure was resolved by explicitly selecting Python and running the module; see [VERIFY.md](VERIFY.md).

## Active blockers

1. **GitHub Actions:** the user supplied a banner stating account billing is locked and workflows cannot execute. Startup-failure runs produced no passing check evidence. Account resolution is outside a code change; recheck before claiming restoration.
2. **AWS:** the [2026-09-18 entry gate](../../evidence/adr017-target-environment-entry-gate-2026-09-18.md) records STS `InvalidClientTokenId`. No current credential check was performed. This is independent of GitHub billing.
3. **Final verification:** local scan execution and report cleanup are recorded. Open security findings, hosted CI, reviewed integration, and pinned transfer remain outstanding. Checkov's numeric scan exit code remains unreported.

These blockers do not authorize weakening tests, making the repository public, changing identity semantics, or expanding the architecture. No live cloud retry-safety, production-readiness, or customer-value claim follows from local tests.
