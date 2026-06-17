# MVE scorecard

**Verdict:** GREEN_LIVE_WINDOW_POSTGAME_DEFERRED

v0.7.1 live-window canary on NYM away @ CIN home contest 44/speculation 33 posted bounded live MM commitments, executed exactly one controlled fill from mm-shakeout-flow-a, observed the fill canonically via own-state SSE, stopped the MM cleanly, and ended with zero public/API/MM visible-open exposure. Postgame score, settle, and claim remain deferred because the game was not final at artifact cut.

| id | capability | proof | evidence | notes |
|---|---|---|---|---|
| target-preflight | Target preflight and allowlist | proven_live | raw/target-preflight.sanitized.json | Primary target verified and quote_ready before live writes. |
| repo-runtime-gates | Repo/runtime gates | proven_live | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK/MM runtime alignment verified. |
| wallet-auth-balances | Wallet auth, balances, allowances | proven_live | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker was clean before start and wallet balances/allowances were sufficient. |
| bounded-approvals | Bounded approvals / no unlimited approvals | proven_live | raw/bounded-approvals.sanitized.json | No unlimited approvals; no new live approvals were required. |
| dry-run-quote-loop | Dry-run quote loop | proven_synthetic_only | raw/mm-dryrun-summary.sanitized.json | Quote dry-run was synthetic/read-only by nature and selected target 44 only. |
| live-commitments-posted | Live commitments posted | proven_live | raw/live-public-commitments-posted.sanitized.json | Live public commitments posted on target 44/33 only. |
| live-fill | Controlled live fill | proven_live | raw/live-fill.sanitized.json | Exactly one controlled live fill succeeded. |
| own-state-sse-canonical-fill | Own-state SSE canonical fill source | proven_live | raw/own-state-sse-summary.sanitized.json | Telemetry fill event source is own-state-stream. |
| exposure-drain-zero | Exposure drained to zero | proven_live | raw/zero-exposure.sanitized.json | End-of-run public/API/MM visible-open exposure is zero. |
| restart-cold-start-safety | Restart/cold-start safety | not_applicable |  | Not part of this live-window canary artifact; final zero-exposure/process checks cover shutdown safety. |
| postgame-score | Postgame score | deferred |  | POSTGAME-DEFERRED because NYM @ CIN was not final at artifact cut. |
| postgame-settle | Postgame settle | deferred |  | POSTGAME-DEFERRED for speculation 33. |
| postgame-claim | Postgame claim/no-op | deferred |  | POSTGAME-DEFERRED for maker/taker winning positions. |
| cost-within-cap | Cost within cap | proven_live | raw/tx-receipts.summary.json | Live fill taker risk/gas stayed under the <= $5 cap. |

## Transactions

- create-contest: `0x1fa840f942a6b6c34981a91b98dc940e1a815160539e3bea9564a52839c32e73`
- seed-match: `0x173f061fa56934fe51c906d9635d3a53b7c1d75a703e811d7b931d1b4143026e`
- match-commitment: `0x7d8ad8dc09db574e7b4ab1e713d8b1ff16b2df9dc0e0bc73335bb090849273cc`
