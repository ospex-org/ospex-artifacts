# MVE scorecard

Verdict: `FULL_GREEN`

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| `target-preflight` | `proven_live` | raw/target-preflight.sanitized.json | Target selected as contest 41/spec 30 only; MIA/PIT and CHC/SF skipped. |
| `repo-runtime-gates` | `proven_live` | raw/release-runtime-matrix.sanitized.json | Version matrix captured and yarn build exited 0. |
| `wallet-auth-balances` | `proven_live` | raw/wallet-auth-balance-allowances.sanitized.json | Strict signer/auth and balance/allowance checks passed for tiny canary. |
| `bounded-approvals` | `proven_live` | raw/bounded-approvals.sanitized.json | No unlimited approvals or new live/postgame approvals were needed. |
| `dry-run-quote-loop` | `proven_live` | raw/mm-dryrun-summary.sanitized.json | Dry-run proved exactly target 41/30 and 0.10 USDC quote sizes. |
| `live-commitments-posted` | `proven_live` | raw/live-public-commitments-posted.sanitized.json | Exactly two tiny live commitments posted on target 41/30. |
| `live-fill` | `proven_live` | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded on the intended commitment. |
| `own-state-sse-canonical-fill` | `proven_live` | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill from own-state-stream. |
| `exposure-drain-zero` | `proven_live` | raw/zero-exposure.sanitized.json | Final public commitments/orderbook/process/target claim sweeps are zero. |
| `restart-cold-start-safety` | `not_applicable` | — | Not run for this salvage; final zero exposure/process checks were run instead. |
| `postgame-score` | `proven_live` | raw/postgame-lifecycle.sanitized.json | Official final score was verified and contest 41 scored. |
| `postgame-settle` | `proven_live` | raw/postgame-lifecycle.sanitized.json | Speculation 30 settled to home/lower/Toronto. |
| `postgame-claim` | `proven_live` | raw/postgame-lifecycle.sanitized.json | Winning lower/Toronto positions claimed; losing upper/Yankees position documented no-op. |
| `cost-within-cap` | `proven_live` | raw/tx-receipts.summary.json | Tracked live+postgame costs stayed within low-value canary envelope. |
