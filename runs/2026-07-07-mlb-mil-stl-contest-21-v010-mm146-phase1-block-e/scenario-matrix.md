# Scenario Matrix

| ID | Scenario | Status | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `pass` | raw/target-preflight.sanitized.json | MIL @ STL contest 21 and specs 52/53/51 passed target identity, allowlist, odds, and runway gates. |
| `repo-runtime-gates` | Repo/runtime gates | `pass` | raw/release-runtime-matrix.sanitized.json | SDK/CLI v0.10.0, MM head 6f3ccc1, installed MM SDK v0.9.0, and required ancillary repo heads were verified. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `pass` | raw/wallet-auth-balance-allowances.sanitized.json | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public balances were sufficient and allowances were bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `pass` | raw/bounded-approvals.sanitized.json | Only bounded USDC approvals were used; no unlimited approvals were created. |
| `dry-run-quote-loop` | Dry-run quote loop | `pass` | raw/mm-dryrun-summary.sanitized.json | Candidates --allowlist-only returned quote-ready rows for contest 21 and all three seeded markets; dry run stayed target-scoped with seedSpeculations=false and wouldSubmitCount=6. |
| `live-commitments-posted` | Live commitments posted | `pass_with_caveats` | raw/live-public-commitments-posted.sanitized.json | Tiny live moneyline, spread, and total commitments posted under strict contest allowlist [21], seedSpeculations=false. |
| `live-fill` | Controlled live fill | `pass_with_caveats` | raw/live-fill.sanitized.json | A controlled taker filled exactly one live MM spread quote for contest 21; preview carried an expires-soon warning. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `pass_with_caveats` | raw/own-state-sse-summary.sanitized.json | Telemetry captured eventCounts.fill=1 with canonicalFillObserved=true; startup stream-health hold entered with zero exposure and cleared before posting/fill; bad own-state counters stayed zero. |
| `exposure-drain-zero` | Exposure drained to zero | `pass` | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame remediation, and no orphan MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_applicable` |  | Block E brief did not require a separate scratch cold-start probe; zero-open and no-orphan shutdown proofs were captured. |
| `postgame-score` | Postgame score | `pass` | raw/postgame-lifecycle.sanitized.json | Official final score was verified and contest 21 scored via R5/CRE using CLI v0.10.0 score --wait. |
| `postgame-settle` | Postgame settle | `pass` | raw/postgame-lifecycle.sanitized.json | Moneyline, spread, and total speculations 52/53/51 were explicitly settled after scoring. |
| `postgame-claim` | Postgame claim/no-op | `pass_with_caveats` | raw/postgame-lifecycle.sanitized.json | Winning controlled positions were claimed; manual remediation claims completed final target zero-state. |
| `cost-within-cap` | Cost within cap | `pass` | raw/tx-receipts.summary.json | Tiny manual/live risk plus protocol fees stayed within the Phase 1 Block E 10 USDC target budget and below the 15 USDC ask threshold. |
