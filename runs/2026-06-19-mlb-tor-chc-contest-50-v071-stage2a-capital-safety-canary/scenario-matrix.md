# Scenario matrix — TOR @ CHC Stage-2a canary

| ID | Scenario | Status | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | pass | raw/target-preflight.sanitized.json | TOR away @ CHC home contest 50/spec 39 passed official pre-game status, identity, allowlist, and quote-ready gates. |
| `repo-runtime-gates` | Repo/runtime gates | pass | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; prior install/build/typecheck/test/smoke evidence reused because SHA and pins were unchanged. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | pass | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker and controlled taker were clean before start; balances/allowances were sufficient and bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | pass | raw/bounded-approvals.sanitized.json | No unlimited approvals; live auto-approval stayed off; existing PositionModule allowances were bounded. |
| `dry-run-quote-loop` | Dry-run quote loop | pass | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 50 returned pipeline=computed and canQuote=true. |
| `live-commitments-posted` | Live commitments posted | pass | raw/live-public-commitments-posted.sanitized.json | Live commitments posted under strict allowlist [50], all target 50/39 only. |
| `live-fill` | Controlled live fill | pass | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0xdcee7fb3… using mm-shakeout-flow-a. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | pass | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| `exposure-drain-zero` | Exposure drained to zero | pass | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | not_applicable | — | Not run for this Stage-2a live-window artifact; final zero-exposure and process checks were run instead. |
| `postgame-score` | Postgame score | pass | raw/postgame-lifecycle.sanitized.json | Official final score TOR 2, CHC 16 was verified and contest 50 scored. |
| `postgame-settle` | Postgame settle | pass | raw/postgame-lifecycle.sanitized.json | Speculation 39 settled to home/lower/Chicago Cubs. |
| `postgame-claim` | Postgame claim/no-op | pass | raw/postgame-lifecycle.sanitized.json | Winning lower/Chicago Cubs live-fill and setup seed positions were claimed; losing upper/TOR positions are no-op. |
| `cost-within-cap` | Cost within cap | pass | raw/tx-receipts.summary.json | Tracked live maker risk and combined open+active maker risk stayed within Stage-2a caps; postgame gas recorded. |
