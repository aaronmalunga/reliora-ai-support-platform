# Verification guide

Run from the product repository root. The user's path is `C:\Users\Aaron\Projects\reliora-ai-support-platform`. For another machine, use its actual checkout path. Record HEAD and environment before running a release baseline. Stop after a failing dependent step and preserve its output.

## Identify the source

These commands inspect the commit and working tree; they do not change files:

```powershell
git rev-parse HEAD
git status --short --branch
uv --version
uv run --frozen python --version
```

Expect a full SHA, branch/change status, and tool versions. The uv invocation may synchronize the environment if needed; `--frozen` prevents lockfile updates. Identify dirty changes if present; a SHA alone does not describe a modified working tree.

## Local code checks

Sync installs the locked environment and may download packages. Ruff checks lint, mypy checks types under `src`, and pytest runs the configured suite with concise output (`-q`). Expect no lint/type errors and no failed tests; record the actual count and exit codes. No cloud deployment is performed.

```powershell
uv sync --frozen
uv run --frozen ruff check .
uv run --frozen mypy src
uv run --frozen python -m pytest -q
```

The user-reported 2026-09-22 results used bare `ruff check`, `mypy src`, and `python -m pytest -q` in the active environment. The commands above are the recommended reproduction procedure, not a claim that they all ran in that form previously.

## Deterministic evaluations

These runners use existing versioned fixtures and write their reports under `evidence/generated/`. They do not call AWS. They can modify tracked reports, so review the resulting diff rather than discarding or committing it automatically.

```powershell
uv run --frozen python evals/runners/run_deterministic_evaluator_regression.py
uv run --frozen python evals/runners/run_stage1_reproduction.py
git diff -- evidence/generated/
```

Expected: 15 regression cases with all expectations matched and zero mismatches; Stage-1 reproduction with zero mismatches and the expected historical defects detected. A reproduced known defect is an expected result, not a new regression. The current historical baseline records three detected known defects. Both runners return a nonzero exit code on mismatches. Do not edit fixtures to disguise an unexpected result. See [evaluation documentation](../../evals/README.md) for scope.

## Lambda packaging and infrastructure

Review [the packaging script](../../scripts/build_lambda.ps1) before invoking it. It builds the Linux x86_64 Python 3.12 Lambda ZIP, downloads dependencies as needed, and recreates its build output. It is a local packaging operation, not deployment.

```powershell
./scripts/build_lambda.ps1
```

Verify the generated ZIP using the artifact-verification step in [the existing workflow](../../.github/workflows/quality-gate.yml): handler, boto3, pydantic, and Linux pydantic-core binary must be present. Successful packaging is not proof of execution in Lambda.

Terraform commands below select the development directory using `-chdir`. Formatting is checked without rewriting files. Initialization downloads providers and writes local initialization files; `-backend=false` skips backend initialization and `-input=false` disables prompts. Validation checks configuration without creating infrastructure. Review any provider-lockfile changes rather than accepting them silently.

```powershell
terraform -chdir=infra/terraform/envs/dev fmt -check
terraform -chdir=infra/terraform/envs/dev init -backend=false -input=false
terraform -chdir=infra/terraform/envs/dev validate -no-color
```

Expect no formatting failures and valid configuration. These checks do not establish valid AWS credentials, a successful plan/apply, or runtime behavior. No apply/destroy commands are part of this local baseline.

## Security and hosted CI

Use [the security baseline](../security/security-scan-baseline.md) to identify scanner versions, scopes, prior findings, and dispositions. Fresh secret/history, runtime dependency, and Terraform scans require current execution evidence. Scanners may download vulnerability information; do not publish raw sensitive findings. Preserve findings and justified exceptions rather than promising all policies pass.

GitHub Actions is currently billing-blocked. Once restored, select a supported workflow trigger and capture the run for the candidate commit. The current workflow is triggered by pull requests and pushes to main; pushing an arbitrary feature branch is not itself evidence that all checks ran. The existing workflow also needs the outstanding behavioral/security gate work described in NEXT_STEPS.

## Evidence record

For each executed check retain actual command, UTC date/time when available, full code SHA, worktree state, OS, relevant versions, observer, exit code, result, artifact references, and limitations. Do not fill unknown values from an older run. Evidence committed after a code check should name the code commit actually tested, not claim that an untested new metadata commit was executed.
