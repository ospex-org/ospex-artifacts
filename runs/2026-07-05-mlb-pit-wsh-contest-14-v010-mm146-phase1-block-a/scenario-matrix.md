# Scenario matrix — 2026-07-05-mlb-pit-wsh-contest-14-v010-mm146-phase1-block-a

| Scenario | Status | Evidence | Notes |
|---|---:|---|---|
| Target preflight and allowlist | pass | `raw/target-preflight.sanitized.json` | Pittsburgh Pirates @ Washington Nationals contest 14 and specs 30/31/32 passed target identity, allowlist, odds, and runway gates. |
| Repo/runtime gates | pass | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.10.0, MM head 6f3ccc1 with strict allowlist / own-state / bounded-approval coverage, installed MM SDK v0.9.0, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | pass | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | pass | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were created. |
| Dry-run quote loop | pass | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned quote-ready rows for both allowlisted contests and all seeded markets; dry run stayed target-scoped. |
| Live commitments posted | pass | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline, spread, and total commitments posted under strict allowlist [13,14], including contest 14, seedSpeculations=false. |
| Controlled live fill | pass | `raw/live-fill.sanitized.json` | A controlled taker filled the MM spread quote for contest 14; tx 0x93368b1340…. |
| Own-state SSE canonical fill source | pass | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the controlled fills without unknown-own-fill, owner-mapping, or divergence safety events. |
| Exposure drained to zero | pass | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | pass | `raw/restart-cold-start-probe.sanitized.json` | A scratch-state dry-run/cold-start probe loaded state cleanly and did not create duplicate live exposure; live CLI reads remained zero-open. |
| Postgame score | pass | `raw/postgame-lifecycle.sanitized.json` | Official final score Pittsburgh Pirates 11, Washington Nationals 5 was verified and contest 14 scored via R5/CRE. |
| Postgame settle | pass | `raw/postgame-lifecycle.sanitized.json` | Moneyline, spread, and total speculations 30/31/32 settled to the expected winning sides or push semantics. |
| Postgame claim/no-op | pass | `raw/postgame-lifecycle.sanitized.json` | Winning controlled positions were claimed, losing positions were no-op/not claimable, and final target positions are zero. |
| Cost within cap | pass | `raw/tx-receipts.summary.json` | Tiny manual/live risk plus protocol fees stayed within the Phase 1 low-cap budget; lifecycle transactions are summarized. |
