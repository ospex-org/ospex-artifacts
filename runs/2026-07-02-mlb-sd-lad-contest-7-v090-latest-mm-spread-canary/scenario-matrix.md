# Scenario matrix — SD @ LAD v0.9 latest-MM spread canary

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| Target preflight and allowlist | pass | `raw/target-preflight.sanitized.json` | Primary SD away @ LAD home contest 7/spec 12 passed official pre-game status, identity, allowlist, odds, and lead-time gates. |
| Repo/runtime gates | pass | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.9.0, MM head 4fcd489 with PR #145 own-state orphan safety tests, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | pass | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | pass | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were sent. |
| Dry-run quote loop | pass | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned contest 7 moneyline + spread quote_ready; dry run would-submit remained target-scoped. |
| Live commitments posted | pass | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline and spread commitments posted under strict allowlist [7], seedSpeculations=false. |
| Controlled live fill | pass | `raw/live-fill.sanitized.json` | Exactly one controlled live spread fill succeeded against commitment 0xe09448186d54… using ospex-flow-a. |
| Own-state SSE canonical fill source | pass | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the fill with source own-state-stream for the filled spread commitment hash. |
| Exposure drained to zero | pass | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | pass_with_caveats | `raw/restart-cold-start-probe.sanitized.json` | A fresh dry-run/cold-start probe stayed target-scoped; synthetic dry records were cleaned from live state before final reporting. |
| Postgame score | pass | `raw/postgame-lifecycle.sanitized.json` | Official final score SD 7, LAD 12 was verified and contest 7 scored via R5/CRE. |
| Postgame settle | pass | `raw/postgame-lifecycle.sanitized.json` | Moneyline speculation 11 and spread speculation 12 settled to home/lower/Los Angeles Dodgers. |
| Postgame claim/no-op | pass | `raw/postgame-lifecycle.sanitized.json` | Winning lower/Dodgers seed-maker and controlled-taker positions were claimed; losing positions are no-op. |
| Cost within cap | pass | `raw/tx-receipts.summary.json` | Tiny canary risk stayed within the requested caps; recorded lifecycle gas is summarized. |
