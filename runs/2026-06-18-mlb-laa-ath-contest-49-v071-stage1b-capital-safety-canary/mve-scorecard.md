# MVE scorecard

| ID | Capability | Proof | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `proven_live` | raw/target-preflight.sanitized.json | LAA away @ ATH home contest 49/spec 38 passed official pre-game status, identity, allowlist, and quote-ready gates. |
| `repo-runtime-gates` | Repo/runtime gates | `proven_live` | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; prior install/build/typecheck/test/smoke evidence reused because SHA and pins were unchanged. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `proven_live` | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker was clean before start; balances/allowances were sufficient and bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `proven_live` | raw/bounded-approvals.sanitized.json | No unlimited approvals; live auto-approval stayed off; existing PositionModule allowances were bounded. |
| `dry-run-quote-loop` | Dry-run quote loop | `proven_synthetic_only` | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 49 returned pipeline=computed and canQuote=true. |
| `live-commitments-posted` | Live commitments posted | `proven_live` | raw/live-public-commitments-posted.sanitized.json | Tiny live commitments posted under strict allowlist [49], all target 49/38 only. |
| `live-fill` | Controlled live fill | `proven_live` | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0x0f6b5182… using mm-shakeout-flow-a. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `proven_live` | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| `exposure-drain-zero` | Exposure drained to zero | `proven_live` | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_applicable` | — | Not run for this Stage-1b live-window artifact; final zero-exposure and process checks were run instead. |
| `postgame-score` | Postgame score | `proven_live` | raw/postgame-lifecycle.sanitized.json | Official final score LAA 0, ATH 5 was verified and contest 49 scored. |
| `postgame-settle` | Postgame settle | `proven_live` | raw/postgame-lifecycle.sanitized.json | Speculation 38 settled to home/lower/Athletics. |
| `postgame-claim` | Postgame claim/no-op | `proven_live` | raw/postgame-lifecycle.sanitized.json | Winning lower/Athletics live-fill and setup seed positions were claimed; losing upper/LAA positions are no-op. |
| `cost-within-cap` | Cost within cap | `proven_live` | raw/tx-receipts.summary.json | Tracked live maker risk and combined open+active maker risk stayed within Stage-1b caps; postgame gas recorded. |
