# MVE scorecard

Verdict: `AMBER_PRELIVE_GATE_HALT` / `MVE_PHASE1_BLOCK_D_AMBER`

| id | capability | proof | evidence | notes |
| --- | --- | --- | --- | --- |
| target-preflight | Target preflight and allowlist | proven_live | raw/target-preflight.sanitized.json | ARI @ SD contest 18 and specs 42, 43, 44 passed identity, verification, odds, and allowlist gates. |
| repo-runtime-gates | Repo/runtime gates | proven_live | raw/release-runtime-matrix.sanitized.json | SDK/CLI v0.10.0 and required MM/API/indexer/CRE heads were verified before writes. |
| wallet-auth-balances | Wallet auth, balances, allowances | proven_live | raw/wallet-auth-balance-allowances.sanitized.json | Controlled wallets passed expected-address/balance/allowance checks; only public balances/allowances are published. |
| bounded-approvals | Bounded approvals / no unlimited approvals | proven_live | raw/bounded-approvals.sanitized.json | Bounded approvals were used; no unlimited approval was created. |
| dry-run-quote-loop | Dry-run quote loop | proven_synthetic_only | raw/mm-dryrun-summary.sanitized.json | Initial candidates and strict allowlist dry-run passed; scheduled pre-live dry-run failed safely with 16 would-submit rows before live writes. |
| live-commitments-posted | Live commitments posted | failed | raw/live-public-commitments-posted.sanitized.json | No live public commitments were posted because the pre-live dry-run gate failed before starting live MM. |
| live-fill | Controlled live fill | deferred | raw/live-fill.sanitized.json | No controlled live fill was attempted because live MM was not started. |
| own-state-sse-canonical-fill | Own-state SSE canonical fill source | not_applicable | raw/own-state-sse-summary.sanitized.json | Not applicable: no live fill occurred. |
| exposure-drain-zero | Exposure drained to zero | proven_live | raw/zero-exposure.sanitized.json | Open commitments are zero, final target positions are zero after manual remediation claims, and no orphan MM process was present. |
| restart-cold-start-safety | Restart/cold-start safety | not_applicable | raw/restart-cold-start-probe.sanitized.json | Not applicable because no live MM state was created. |
| postgame-score | Postgame score | proven_live | raw/postgame-lifecycle.sanitized.json | MLB Stats API official final was captured and R5/CRE score --wait completed. |
| postgame-settle | Postgame settle | proven_live | raw/postgame-lifecycle.sanitized.json | All target speculations for the contest were explicitly settled. |
| postgame-claim | Postgame claim/no-op | proven_live | raw/postgame-lifecycle.sanitized.json | Winning controlled positions were claimed; manual remediation completed final target zero-state. |
| cost-within-cap | Cost within cap | proven_live | raw/tx-receipts.summary.json | Manual seed/fill risk and postgame transactions remained inside the Phase 1 Block D cap; no live MM risk was posted. |
