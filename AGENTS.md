# Reliora agent instructions

## Begin each continuation

Read `docs/handover/START_HERE.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`, and `VERIFICATION_MANIFEST.json` under `docs/handover/`. Inspect the actual branch, HEAD, working tree, and applicable nested instructions before changing files. Check whether a newer commit has superseded the dated handover.

Never assume the default branch contains all work. The preparation branch is `chore/reliora-handover-readiness`; the consolidated parent checkpoint is `bb55f983c18b3abe618291be0e8468bd38b96223`. Discover the current HEAD rather than treating this parent as the final export commit. Preserve uncommitted work and avoid history rewriting or branch deletion during consolidation.

## Product and decision discipline

Reliora is a bounded AI support reliability/control reference implementation. Preserve the current NARROW product decision and BUG / PLATFORM / OTHER scope. M1 is recorded complete; M2 is blocked on AWS authentication. ADR-017 remains PROPOSED. A blocked experiment does not establish that the proposed architecture failed.

Follow the constitution's source precedence: official P1 submission requirements; Reliora constitution; Reliora North Star; Reliora-specific requirements/ADRs/policies/evidence; portfolio standard; general engineering knowledge. Distinguish mandatory historical submission requirements from later product engineering. Do not silently replace newer repository documents with older attachments. `SOURCE_MAP.md` identifies external supporting sources not yet bundled.

The LLM proposes; deterministic software validates and authorizes. Preserve:

- separate request, session, and logical operation identities;
- application-owned trusted identity, independent of model-supplied arguments;
- authorization before side effects and idempotency admission;
- matching replay, conflict detection, and explicit UNCONFIRMED outcomes;
- authoritative backend confirmation, conditional transactions, and reconciliation;
- best-effort telemetry that does not mask primary failures;
- approved knowledge boundaries and explicit human fallback;
- minimized telemetry without hidden model reasoning.

Do not introduce a new framework, RAG, vector store, multi-agent orchestration, personalized memory, Kubernetes, Kafka, Redis, refunds, or broad commerce capabilities without a Reliora-specific requirement and justified decision. Preserve held-out routing evidence; do not tune on it or weaken evaluation expectations to obtain passing results.

## Commands and verification

Use Python 3.12 and the existing uv lockfile. From the repository root:

```text
uv sync --frozen
uv run --frozen ruff check .
uv run --frozen mypy src
uv run --frozen python -m pytest -q
```

Each line is one complete command. `--frozen` retains the dependency lock; sync changes the local environment and may download packages. Checks report violations or failures. These do not deploy infrastructure. See `docs/handover/VERIFY.md` for evaluator and packaging commands, expected results, and generated-file effects.

For meaningful code changes run relevant tests and required gates. For documentation-only changes inspect links, formatting, evidence accuracy, and the diff; do not claim tests were rerun if they were not. Never substitute local success for hosted CI or AWS verification.

## Evidence and handover maintenance

Use the existing evidence classes and maturity framework. Record command, commit, environment, result, observer/source, date, and limitations. User-pasted output is user-reported evidence. Unknown exit codes, tool versions, timestamps, or hashes remain unknown. Historical security scans do not certify the new release. The September 8 Checkov result had 12 failures with classified dispositions.

As of the handover, GitHub Actions is blocked by account billing. AWS authentication is a separate blocker. Recheck both before claiming they are resolved. Do not change account billing, publish the repository, or provision cloud resources merely to bypass a verification blocker.

Update current state and next steps when evidence or a completed change warrants it. Keep dated audit and Stage-1 records historical. Keep detailed decisions in existing ADRs and requirements in their current files. Do not create duplicate governing specifications.

## Working with Aaron

The user works in Windows PowerShell at `C:\Users\Aaron\Projects\reliora-ai-support-platform`. For any command the user must run, name the repository, provide the exact directory change when relevant, and explain purpose, meaningful arguments, expected output, and effects before the command. Provide complete lines that can be pasted individually. Stop follow-on dependent operations when a command fails.

The learning ledger is a separate repository, `aws-agentic-ai-learning-ledger`. State repository switches explicitly. Do not place credentials, Terraform state/plans, private keys, raw customer records, or unredacted sensitive logs in Git or export bundles.
