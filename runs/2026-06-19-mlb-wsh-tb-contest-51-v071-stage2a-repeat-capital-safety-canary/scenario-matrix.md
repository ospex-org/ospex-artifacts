# Scenario matrix — WSH @ TB contest 51 Stage-2a repeat canary

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| Target preflight and allowlist | pass | raw/target-preflight.sanitized.json | WSH away @ TB home contest 51/spec 40 passed official pre-game status, identity, allowlist, and quote-ready gates. |
| Repo/runtime gates | pass | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; prior install/build/typecheck/test/smoke evidence reused because SHA and pins were unchanged. |
| Wallet auth, balances, allowances | pass | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker and controlled taker were clean before start after TOR/CHC cleanup; balances/allowances were sufficient and bounded. |
| Bounded approvals / no unlimited approvals | pass | raw/bounded-approvals.sanitized.json | No unlimited approvals; live auto-approval stayed off; existing PositionModule allowances were bounded. |
| Dry-run quote loop | pass | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 51 returned pipeline=computed and canQuote=true. |
| Live commitments posted | pass | raw/live-public-commitments-posted.sanitized.json | Live commitments posted under strict allowlist [51], all target 51/40 only. |
| Controlled live fill | pass | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0x19a0faa4… using mm-shakeout-flow-a. |
| Own-state SSE canonical fill source | pass | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| Exposure drained to zero | pass | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| Restart/cold-start safety | not_applicable | — | Not run for this Stage-2a repeat live-window artifact; final zero-exposure and process checks were run instead. |
| Postgame score | pass | raw/postgame-lifecycle.sanitized.json | Official final score WSH 2, TB 5 was verified and contest 51 scored. |
| Postgame settle | pass | raw/postgame-lifecycle.sanitized.json | Speculation 40 settled to home/lower/Tampa Bay Rays. |
| Postgame claim/no-op | pass | raw/postgame-lifecycle.sanitized.json | Winning lower/Tampa Bay Rays live-fill and setup seed positions were claimed; losing upper/WSH positions are no-op. |
| Cost within cap | pass | raw/tx-receipts.summary.json | Tracked live maker risk and combined open+active maker risk stayed within Stage-2a caps; postgame gas recorded. |
