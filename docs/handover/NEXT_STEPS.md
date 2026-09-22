# Ordered continuation backlog

Snapshot: 2026-09-22. Preserve the NARROW gate. Each completed item must identify its actual commit, verification, and remaining limitations. Do not turn documentation updates into indefinite implementation delay.

## Handover completion

| ID | Task | Acceptance evidence |
|---|---|---|
| H1 | Synchronize the handover branch locally after these documentation changes | Correct HEAD/upstream; no unaccounted local work. |
| H2 | Run both evaluator runners | Actual command/result tied to HEAD; 15/15 regression expectations; zero reproduction mismatches; known historical defects retained. Review generated JSON differences. |
| H3 | Refresh Lambda packaging and Terraform static verification | Build/artifact check and fmt/init/validate evidence with tool versions and exact SHA. No deployment claim. |
| H4 | Refresh scoped security checks | Secret/history, runtime dependency, and IaC findings retained, classified, and either remediated or explicitly justified for the release scope. Do not suppress findings just to pass. |
| H5 | Complete hosted CI evidence when billing is restored | The appropriate workflow executes on the actual candidate commit; job results and limitations retained. A billing-blocked status remains blocked. |
| H6 | Review final integration to main | All intended branch work accounted for; existing PR #1/#2 dispositions explicit; no loss of decisions or unique changes; required checks satisfied or a permitted exception explicitly documented. Do not bypass a required gate. |
| H7 | Pin and transfer the final checkpoint | Final commit/tag, sanitized source archive, checksum, source map/supporting references, and receiver reproduction. No production-release claim implied by a handover tag. |

The observed pre-merge code baseline has passing local lint/type/unit-test evidence. Documentation changes alone do not require repeating that suite without a concrete reason. H2-H4 close specific outstanding evidence gaps rather than repeating known checks indiscriminately.

## Product completion

| Stage | Smallest useful increment | Dependency and acceptance |
|---|---|---|
| M2 | Trusted identity experiment using the existing managed path | Authorized target account/region and cost boundary first. Demonstrate model non-override, stable operation ID across retry, distinct request IDs where appropriate, new ID for new operation, and DynamoDB replay. Update ADR-017 from evidence. |
| M3 | Typed structured human handoff and one end-to-end path | Existing requirements and data minimization. Test unsupported, explicit-human, and failure cases with preserved context. Keep cloud-dependent results unverified until exercised. |
| M4 | Complete behavioral/security release controls | Extend the existing workflow; include deterministic evaluator execution and appropriate scans. Prove a safe change passes and a controlled unsafe change is rejected. Never merge the intentionally unsafe change. |
| M5 | Minimal telemetry wiring and reconstruction | Correlate one success and one failure without customer-payload leakage or masking backend errors; define provenance and recovery. |
| M6 | Target-cloud integration and controlled experiments | Verify Lambda/DynamoDB and AgentCore/Gateway boundaries, retry/conflict/ambiguity, recovery/redeploy, teardown, and bounded cost/latency. Preserve the experiment envelope. |
| M7 | Focused reference customer experience and operator view | Demonstrate canonical BUG/PLATFORM/OTHER journeys and evidence inspection. Label synthetic/local and live modes clearly. |
| M8 | Reproducible release and operating handoff | Adaptation, deployment, verification, troubleshooting, recovery, ownership, evidence-linked case study, demo, and separate learning-ledger update. |

Repository hygiene and work independent of trusted cloud identity can proceed while AWS access is blocked. Review dependency boundaries explicitly before beginning an increment; do not represent local work as closure of M2 or M6.

## Scope and commercial gate

Do not restart completed M1 work without materially new evidence. Broader continuation requires credible retailer workflow, buyer ownership, incumbent-gap, and value evidence. A reference implementation can be completed without inventing customers or measured ROI.

Refund/order-tracking demo ideas are not accepted autonomous business-action requirements. Reconcile them with current scope before implementation. No technology enters merely because another portfolio project uses it.
