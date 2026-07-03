# MVE scorecard — SD @ LAD v0.9 latest-MM spread canary

Verdict: **FULL_GREEN**

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| Target preflight and allowlist | proven_live | `raw/target-preflight.sanitized.json` | Primary SD away @ LAD home contest 7/spec 12 passed official pre-game status, identity, allowlist, odds, and lead-time gates. |
| Repo/runtime gates | proven_live | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.9.0, MM head 4fcd489 with PR #145 own-state orphan safety tests, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | proven_live | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | proven_live | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were sent. |
| Dry-run quote loop | proven_synthetic_only | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned contest 7 moneyline + spread quote_ready; dry run would-submit remained target-scoped. |
| Live commitments posted | proven_live | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline and spread commitments posted under strict allowlist [7], seedSpeculations=false. |
| Controlled live fill | proven_live | `raw/live-fill.sanitized.json` | Exactly one controlled live spread fill succeeded against commitment 0xe09448186d54… using ospex-flow-a. |
| Own-state SSE canonical fill source | proven_live | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the fill with source own-state-stream for the filled spread commitment hash. |
| Exposure drained to zero | proven_live | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | proven_synthetic_only | `raw/restart-cold-start-probe.sanitized.json` | A fresh dry-run/cold-start probe stayed target-scoped; synthetic dry records were cleaned from live state before final reporting. |
| Postgame score | proven_live | `raw/postgame-lifecycle.sanitized.json` | Official final score SD 7, LAD 12 was verified and contest 7 scored via R5/CRE. |
| Postgame settle | proven_live | `raw/postgame-lifecycle.sanitized.json` | Moneyline speculation 11 and spread speculation 12 settled to home/lower/Los Angeles Dodgers. |
| Postgame claim/no-op | proven_live | `raw/postgame-lifecycle.sanitized.json` | Winning lower/Dodgers seed-maker and controlled-taker positions were claimed; losing positions are no-op. |
| Cost within cap | proven_live | `raw/tx-receipts.summary.json` | Tiny canary risk stayed within the requested caps; recorded lifecycle gas is summarized. |
