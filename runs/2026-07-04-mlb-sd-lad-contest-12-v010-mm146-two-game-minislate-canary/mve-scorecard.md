# MVE readiness scorecard

| ID | Capability | Proof | Evidence |
|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | proven_live | `raw/target-preflight.sanitized.json` |
| `repo-runtime-gates` | Repo/runtime gates | proven_live | `raw/release-runtime-matrix.sanitized.json` |
| `wallet-auth-balances` | Wallet auth, balances, allowances | proven_live | `raw/wallet-auth-balance-allowances.sanitized.json` |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | proven_live | `raw/bounded-approvals.sanitized.json` |
| `dry-run-quote-loop` | Dry-run quote loop | proven_synthetic_only | `raw/mm-dryrun-summary.sanitized.json` |
| `live-commitments-posted` | Live commitments posted | proven_live | `raw/live-public-commitments-posted.sanitized.json` |
| `live-fill` | Controlled live fill | proven_live | `raw/live-fill.sanitized.json` |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | proven_live | `raw/own-state-sse-summary.sanitized.json` |
| `exposure-drain-zero` | Exposure drained to zero | proven_live | `raw/zero-exposure.sanitized.json` |
| `restart-cold-start-safety` | Restart/cold-start safety | proven_synthetic_only | `raw/restart-cold-start-probe.sanitized.json` |
| `postgame-score` | Postgame score | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| `postgame-settle` | Postgame settle | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| `postgame-claim` | Postgame claim/no-op | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| `cost-within-cap` | Cost within cap | proven_live | `raw/tx-receipts.summary.json` |
