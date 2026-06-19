# MVE scorecard — TOR @ CHC Stage-2a canary

Verdict: **FULL_GREEN**.

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| `target-preflight` | proven_live | raw/target-preflight.sanitized.json | TOR away @ CHC home contest 50/spec 39 passed official pre-game status, identity, allowlist, and quote-ready gates. |
| `repo-runtime-gates` | proven_live | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; prior install/build/typecheck/test/smoke evidence reused because SHA and pins were unchanged. |
| `wallet-auth-balances` | proven_live | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker and controlled taker were clean before start; balances/allowances were sufficient and bounded. |
| `bounded-approvals` | proven_live | raw/bounded-approvals.sanitized.json | No unlimited approvals; live auto-approval stayed off; existing PositionModule allowances were bounded. |
| `dry-run-quote-loop` | proven_synthetic_only | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 50 returned pipeline=computed and canQuote=true. |
| `live-commitments-posted` | proven_live | raw/live-public-commitments-posted.sanitized.json | Live commitments posted under strict allowlist [50], all target 50/39 only. |
| `live-fill` | proven_live | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0xdcee7fb3… using mm-shakeout-flow-a. |
| `own-state-sse-canonical-fill` | proven_live | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| `exposure-drain-zero` | proven_live | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| `restart-cold-start-safety` | not_applicable | — | Not run for this Stage-2a live-window artifact; final zero-exposure and process checks were run instead. |
| `postgame-score` | proven_live | raw/postgame-lifecycle.sanitized.json | Official final score TOR 2, CHC 16 was verified and contest 50 scored. |
| `postgame-settle` | proven_live | raw/postgame-lifecycle.sanitized.json | Speculation 39 settled to home/lower/Chicago Cubs. |
| `postgame-claim` | proven_live | raw/postgame-lifecycle.sanitized.json | Winning lower/Chicago Cubs live-fill and setup seed positions were claimed; losing upper/TOR positions are no-op. |
| `cost-within-cap` | proven_live | raw/tx-receipts.summary.json | Tracked live maker risk and combined open+active maker risk stayed within Stage-2a caps; postgame gas recorded. |

## Transactions

| Category | Tx | Purpose |
|---|---|---|
| seed-match | `0xb2f8947c31e5f34f671006a6a96c2886f6d0f32351264bdaca930773cf4a81c3` | Setup seed/open fill for contest 50 before live canary. |
| match-commitment | `0x89f09327ac9d51ea18ca7d4391ce3ee106d71bd27cf40dc2adf4a8d469c2ccbc` | Exactly one controlled live fill against the live MM quote. |
| score-request | `0x5ac8afe5e0808de878151a5bb8a0c96e356d48b11eab3a63afaba95d70c5d524` | Score contest 50 after MLB final. |
| settle | `0xd4f4edf930c97b0b72e3e425da00dfa5f7307b25a285daef1c9e39564bc57e44` | Settle speculation 39 to home/lower/Chicago Cubs. |
| claim | `0x4be831d50d2111ed14104c801a80c20d880c07506094f56568be4428a6554ae8` | Claim controlled live maker winning position. |
| claim | `0xc0e73ae2d934eff9d03c491b6555016cc81a605d9d97b2fa6e6a3b2c50be1dbc` | Claim setup seed taker winning position. |
