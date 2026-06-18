# MVE scorecard

Verdict: **FULL_GREEN**

The v0.7.1 TOR @ BOS repeatability canary completed the full lifecycle: official final score Toronto Blue Jays 3, Boston Red Sox 0 was verified; contest 46 was scored; speculation 35 settled to away/upper/Toronto; the winning controlled live-fill and setup seed positions were claimed; final claim sweeps, public commitments/orderbook, and live-MM process checks are zero. The prepared fallback CLE @ MIL setup seed was also scored/settled/claimed after final. Caveats are limited to a not-run restart/cold-start probe and an operator-side polling-filter delay during the live fill window; no extra fills occurred.

| id | capability | proof | evidence | notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `proven_live` | raw/target-preflight.sanitized.json | Primary TOR away @ BOS home contest 46/spec 35 passed pre-live gates; fallback prepared but not used live. |
| `repo-runtime-gates` | Repo/runtime gates | `proven_live` | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK and MM SHA/pins verified; heavy setup gates reused because worktree unchanged. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `proven_live` | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker was clean before start; maker and controlled taker balances/allowances sufficient. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `proven_live` | raw/bounded-approvals.sanitized.json | autoApprove false; no new approvals and no unlimited approval creation. |
| `dry-run-quote-loop` | Dry-run quote loop | `proven_synthetic_only` | raw/mm-dryrun-summary.sanitized.json | Pre-live quote dry-run for contest 46 returned pipeline=computed and canQuote=true. |
| `live-commitments-posted` | Live commitments posted | `proven_live` | raw/live-public-commitments-posted.sanitized.json | 9 tiny live commitments posted over the bounded live loop, all target 46/35 only. |
| `live-fill` | Controlled live fill | `proven_live` | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live-posted commitment 0xe84032f1… using mm-shakeout-flow-a. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `proven_live` | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream. |
| `exposure-drain-zero` | Exposure drained to zero | `proven_live` | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero and no orphan live MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_applicable` |  | Not run for this live-window artifact; final zero-exposure and process checks were run instead. |
| `postgame-score` | Postgame score | `proven_live` | raw/postgame-lifecycle.sanitized.json | Official MLB final score TOR 3, BOS 0 was verified and contest 46 scored. |
| `postgame-settle` | Postgame settle | `proven_live` | raw/postgame-lifecycle.sanitized.json | Speculation 35 settled to away/upper/Toronto Blue Jays. |
| `postgame-claim` | Postgame claim/no-op | `proven_live` | raw/postgame-lifecycle.sanitized.json | Winning upper/Toronto live-fill and setup seed positions were claimed; losing lower/Boston positions are no-op. |
| `cost-within-cap` | Cost within cap | `proven_live` | raw/tx-receipts.summary.json | Tracked live + postgame gas and USDC movement stayed within the low-value canary envelope. |

## Transactions

| category | tx | purpose |
|---|---|---|
| `create-contest` | `0x70e5cdfd8479dea6b96b7c46cb778d2aac321c0529c7a10069f1fdc445b3940c` | Setup handoff created verified contest 46 for TOR @ BOS before the live MM window. |
| `seed-match` | `0xc1672bd732252147e567c68aa17ac596fe47f2e29c94c845bdc0c85c5827a189` | Setup handoff seed/open moneyline fill for speculation 35. |
| `match-commitment` | `0xe2d797bdd7936c7b81f5d5236c38749d35b57ea2b4ef1232b85079f4c80b3be8` | Exactly one controlled live MM fill by mm-shakeout-flow-a against commitment 0xe84032f1a0f3d8a4b92bf6774e0e117fe5fe610bb678c2afa69aecf34709e2e8. |
| `score-request` | `0x5deff565bf47d9b56fdf60fc5cb14085653b815d84c55e175cabcc8acea3e70e` | Score contest 46 after official MLB final source showed Toronto Blue Jays 3, Boston Red Sox 0. |
| `settle` | `0x735adad17d9918b4fb3bf493a0442cde6d64b24e05960fa33ad346e74f9c4ed2` | Settle speculation 35 to away/upper/Toronto Blue Jays. |
| `claim` | `0x315892ddf9230d6234f4a4a5a01974eaf7189f8b50f338d9b27e38c4b05afb82` | Claim ospex-stage-maker-a winning setup seed/open upper/Toronto position. |
| `claim` | `0x81362c0844457b2e05652caf446e159b06ebcbafba0cfd1d8998e162bd2df100` | Claim mm-shakeout-maker-a winning controlled live-fill upper/Toronto position. |
| `score-request` | `0xa507e0974521bd84d0197bd301617a93b75b5863a9ab93e02a1e8aaf9458c15b` | Score prepared fallback contest 47 after official final source showed Milwaukee Brewers 9, Cleveland Guardians 4. |
| `settle` | `0xdb179c81ccb43066e8c0fa045067b3d4bdf062251b76bf2f3018aa8ff4c4cf0b` | Settle prepared fallback speculation 36 to home/lower/Milwaukee Brewers. |
| `claim` | `0x32e3d39f793b0d166f29f7f3cc6d218c4c708bbd74cd3fc2719f4c02a00924bc` | Claim ospex-fresh-user winning fallback setup seed lower/Milwaukee position. |
