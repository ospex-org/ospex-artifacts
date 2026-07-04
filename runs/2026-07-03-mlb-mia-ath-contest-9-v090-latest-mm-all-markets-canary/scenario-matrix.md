# Scenario matrix — MIA @ ATH contest 9 all-market MM canary

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| Target preflight and allowlist | pass | `raw/target-preflight.sanitized.json` | Primary MIA away @ ATH home contest 9/specs 15/16/17 passed official pre-game status, identity, allowlist, odds, and lead-time gates. |
| Repo/runtime gates | pass | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.9.0, MM head 4fcd489 with PR #145 own-state orphan safety tests, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | pass | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | pass | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were sent. |
| Dry-run quote loop | pass | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned contest 9 moneyline, spread, and total quote_ready; dry run would-submit remained target-scoped. |
| Live commitments posted | pass | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline, spread, and total commitments posted under strict allowlist [9], seedSpeculations=false. |
| Controlled live fill | pass | `raw/live-fill.sanitized.json` | Exactly one controlled live total fill succeeded against commitment 0xdf1762d2ce6a… using ospex-flow-a. |
| Own-state SSE canonical fill source | pass | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the fill with source own-state-stream for the filled total commitment hash. |
| Exposure drained to zero | pass | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | pass | `raw/restart-cold-start-probe.sanitized.json` | A scratch-state dry-run/cold-start probe loaded state cleanly, rehydrated before quote decisions, and did not create duplicate live exposure. |
| Postgame score | pass | `raw/postgame-lifecycle.sanitized.json` | Official final score MIA 12, ATH 5 was verified and contest 9 scored via R5/CRE on the first request. |
| Postgame settle | pass | `raw/postgame-lifecycle.sanitized.json` | Moneyline speculation 15 settled to away/upper/Miami Marlins; spread 16 to away/upper/Miami Marlins +1.5; total 17 to over/upper/over 10.5. |
| Postgame claim/no-op | pass | `raw/postgame-lifecycle.sanitized.json` | Winning upper positions for stage-maker-a and stage-maker-b were claimed; losing positions are no-op/not claimable, and final target positions are zero. |
| Cost within cap | pass | `raw/tx-receipts.summary.json` | Tiny canary risk plus protocol fees stayed within the requested cap; recorded lifecycle transactions are summarized. |
