# Scenario matrix

| id | scenario | status | evidence | notes |
|---|---|---|---|---|
| target-preflight | Target preflight and allowlist | pass | raw/target-preflight.sanitized.json | Primary NYM away @ CIN home contest 44/spec 33 passed pre-live gates; fallback not used. |
| repo-runtime-gates | Repo/runtime gates | pass | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; heavy setup gates reused because worktree unchanged. |
| wallet-auth-balances | Wallet auth, balances, allowances | pass | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker was clean before start; maker and controlled taker balances/allowances sufficient. |
| bounded-approvals | Bounded approvals / no unlimited approvals | pass | raw/bounded-approvals.sanitized.json | autoApprove false; no new approvals and no unlimited approval creation. |
| dry-run-quote-loop | Dry-run quote loop | pass | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 44 returned pipeline=computed and canQuote=true. |
| live-commitments-posted | Live commitments posted | pass | raw/live-public-commitments-posted.sanitized.json | 10 tiny live commitments posted over the bounded live loop, all target 44/33 only. |
| live-fill | Controlled live fill | pass | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0x7818744c… using mm-shakeout-flow-a. |
| own-state-sse-canonical-fill | Own-state SSE canonical fill source | pass | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| exposure-drain-zero | Exposure drained to zero | pass | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| restart-cold-start-safety | Restart/cold-start safety | not_run |  | Not run for this live-window artifact; final zero-exposure and process checks were run instead. |
| postgame-score | Postgame score | deferred |  | Game had not reached final state at artifact cut; scoring is POSTGAME-DEFERRED. |
| postgame-settle | Postgame settle | deferred |  | Speculation 33 settlement is POSTGAME-DEFERRED. |
| postgame-claim | Postgame claim/no-op | deferred |  | Winning-position claim is POSTGAME-DEFERRED. |
| cost-within-cap | Cost within cap | pass | raw/tx-receipts.summary.json | Controlled live fill stayed within the <= $5 cap. |
