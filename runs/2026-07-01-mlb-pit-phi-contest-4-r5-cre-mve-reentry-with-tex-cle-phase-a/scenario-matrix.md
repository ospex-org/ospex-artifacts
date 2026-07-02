# Scenario matrix

| ID | Scenario | Status | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `pass` | `raw/target-preflight.sanitized.json` | PIT @ PHI contest 4/spec 6 was strict-allowlisted for the evening moneyline canary; Phase A TEX @ CLE contest 3 is recorded as related setup evidence. |
| `repo-runtime-gates` | Repo/runtime gates | `pass` | `raw/release-runtime-matrix.sanitized.json` | Setup/live gates used SDK/CLI 0.8.0, MM aa43da8 with installed @ospex/sdk 0.8.0, and required ancillary repo heads. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for operator/MM maker, manual maker, and controlled taker; balances/allowances were sufficient for tiny controlled exposure. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `pass` | `raw/bounded-approvals.sanitized.json` | Bounded approvals only; live MM auto-approval stayed off. |
| `dry-run-quote-loop` | Dry-run quote loop | `pass` | `raw/mm-dryrun-summary.sanitized.json` | Candidates/quote/run dry-run gates passed for the allowlisted contest 4 moneyline canary. |
| `live-commitments-posted` | Live commitments posted | `pass` | `raw/live-public-commitments-posted.sanitized.json` | The MM posted tiny moneyline commitments under allowlist [4]. |
| `live-fill` | Controlled live fill | `pass` | `raw/live-fill.sanitized.json` | Controlled taker matched exactly one live MM quote on contest 4/spec 6. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `pass` | `raw/own-state-sse-summary.sanitized.json` | Own-state stream telemetry observed the fill for commitment 0xa3ee7a32… |
| `exposure-drain-zero` | Exposure drained to zero | `pass` | `raw/zero-exposure.sanitized.json` | Final public commitments/orderbook, positions, and orphan-process checks are zero. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_applicable` | `n/a` | Not run for this bounded re-entry canary; process shutdown, lock cleanup, and zero-exposure checks were performed instead. |
| `postgame-score` | Postgame score | `pass` | `raw/postgame-lifecycle.sanitized.json` | Official finals were verified and contests 3 and 4 were scored through R5/CRE. |
| `postgame-settle` | Postgame settle | `pass` | `raw/postgame-lifecycle.sanitized.json` | Speculations 3, 4, 5, and 6 settled to the official winners. |
| `postgame-claim` | Postgame claim/no-op | `pass` | `raw/postgame-lifecycle.sanitized.json` | Controlled winning positions were claimed; final positions.status was active=0 pendingSettle=0 claimable=0 for all three roles. |
| `cost-within-cap` | Cost within cap | `pass` | `raw/tx-receipts.summary.json` | Tiny controlled risk stayed below the $5 cap; live MM canary was stopped after first fill. |
