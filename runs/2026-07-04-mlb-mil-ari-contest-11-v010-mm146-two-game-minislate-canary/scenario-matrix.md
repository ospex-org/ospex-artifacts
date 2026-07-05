# Scenario matrix

| ID | Scenario | Status | Evidence |
|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | pass | `raw/target-preflight.sanitized.json` |
| `repo-runtime-gates` | Repo/runtime gates | pass | `raw/release-runtime-matrix.sanitized.json` |
| `wallet-auth-balances` | Wallet auth, balances, allowances | pass | `raw/wallet-auth-balance-allowances.sanitized.json` |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | pass | `raw/bounded-approvals.sanitized.json` |
| `dry-run-quote-loop` | Dry-run quote loop | pass | `raw/mm-dryrun-summary.sanitized.json` |
| `live-commitments-posted` | Live commitments posted | pass_with_caveats | `raw/live-public-commitments-posted.sanitized.json` |
| `live-fill` | Controlled live fill | pass_with_caveats | `raw/live-fill.sanitized.json` |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | pass | `raw/own-state-sse-summary.sanitized.json` |
| `exposure-drain-zero` | Exposure drained to zero | pass | `raw/zero-exposure.sanitized.json` |
| `restart-cold-start-safety` | Restart/cold-start safety | pass | `raw/restart-cold-start-probe.sanitized.json` |
| `postgame-score` | Postgame score | pass_with_caveats | `raw/postgame-lifecycle.sanitized.json` |
| `postgame-settle` | Postgame settle | pass | `raw/postgame-lifecycle.sanitized.json` |
| `postgame-claim` | Postgame claim/no-op | pass | `raw/postgame-lifecycle.sanitized.json` |
| `cost-within-cap` | Cost within cap | pass | `raw/tx-receipts.summary.json` |
