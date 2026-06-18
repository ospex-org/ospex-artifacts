# Scenario matrix

| ID | Scenario | Status | Notes |
|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `pass` | Target selected as contest 41/spec 30 only; MIA/PIT and CHC/SF skipped. |
| `repo-runtime-gates` | Repo/runtime gates | `pass` | Version matrix captured and yarn build exited 0. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `pass` | Strict signer/auth and balance/allowance checks passed for tiny canary. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `pass` | No unlimited approvals or new live/postgame approvals were needed. |
| `dry-run-quote-loop` | Dry-run quote loop | `pass` | Dry-run proved exactly target 41/30 and 0.10 USDC quote sizes. |
| `live-commitments-posted` | Live commitments posted | `pass` | Exactly two tiny live commitments posted on target 41/30. |
| `live-fill` | Controlled live fill | `pass` | Exactly one controlled fill succeeded on the intended commitment. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `pass` | Telemetry captured the fill from own-state-stream. |
| `exposure-drain-zero` | Exposure drained to zero | `pass` | Final public commitments/orderbook/process/target claim sweeps are zero. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_run` | Not run for this salvage; final zero-exposure and process checks were run instead. |
| `postgame-score` | Postgame score | `pass` | Official final score was verified and contest 41 scored. |
| `postgame-settle` | Postgame settle | `pass` | Speculation 30 settled to home/lower/Toronto. |
| `postgame-claim` | Postgame claim/no-op | `pass` | Winning lower/Toronto positions claimed; losing upper/Yankees position documented no-op. |
| `cost-within-cap` | Cost within cap | `pass` | Tracked live+postgame costs stayed within low-value canary envelope. |
