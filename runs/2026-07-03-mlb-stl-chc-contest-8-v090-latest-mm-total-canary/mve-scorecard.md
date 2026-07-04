# MVE readiness scorecard

Verdict: **FULL_GREEN**

| ID | Capability | Proof | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | proven_live | `raw/target-preflight.sanitized.json` | Primary STL away @ CHC home contest 8/spec 14 passed official pre-game status, identity, allowlist, odds, and lead-time gates. |
| `repo-runtime-gates` | Repo/runtime gates | proven_live | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.9.0, MM head 4fcd489 with PR #145 own-state orphan safety tests, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | proven_live | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | proven_live | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were sent. |
| `dry-run-quote-loop` | Dry-run quote loop | proven_synthetic_only | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned contest 8 moneyline + total quote_ready; dry run would-submit remained target-scoped. |
| `live-commitments-posted` | Live commitments posted | proven_live | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline and total commitments posted under strict allowlist [8], seedSpeculations=false. |
| `live-fill` | Controlled live fill | proven_live | `raw/live-fill.sanitized.json` | Exactly one controlled live total fill succeeded against commitment 0x345624d363db… using ospex-flow-a. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | proven_live | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the fill with source own-state-stream for the filled total commitment hash. |
| `exposure-drain-zero` | Exposure drained to zero | proven_live | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | proven_synthetic_only | `raw/restart-cold-start-probe.sanitized.json` | A scratch-state dry-run/cold-start probe loaded state cleanly, rehydrated before quote decisions, and did not create duplicate live exposure. |
| `postgame-score` | Postgame score | proven_live | `raw/postgame-lifecycle.sanitized.json` | Official final score STL 17, CHC 1 was verified and contest 8 scored via R5/CRE on the first request. |
| `postgame-settle` | Postgame settle | proven_live | `raw/postgame-lifecycle.sanitized.json` | Moneyline speculation 13 settled to away/upper/St. Louis Cardinals; total speculation 14 settled to over/upper/over 10.5. |
| `postgame-claim` | Postgame claim/no-op | proven_live | `raw/postgame-lifecycle.sanitized.json` | Winning upper positions for stage-maker-a, flow-a, and stage-maker-b were claimed; losing positions are no-op/not claimable. |
| `cost-within-cap` | Cost within cap | proven_live | `raw/tx-receipts.summary.json` | Tiny canary risk stayed within the requested caps; recorded lifecycle gas is summarized. |
