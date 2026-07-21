# Scenario matrix

| Capability | Status | Evidence |
|---|---|---|
| Target preflight and allowlist | pass | `raw/target-preflight.sanitized.json` |
| Repo/runtime gates | pass | `raw/runtime-and-setup.sanitized.json` |
| Wallet auth, balances, allowances | pass | `raw/runtime-and-setup.sanitized.json` |
| Bounded approvals / no unlimited approvals | pass | `raw/runtime-and-setup.sanitized.json` |
| Dry-run quote loop | pass | `raw/dry-live-summary.sanitized.json` |
| Live commitments posted | pass | `raw/dry-live-summary.sanitized.json` |
| Controlled live fill | pass | `raw/live-fill.sanitized.json` |
| Own-state SSE canonical fill source | pass | `raw/own-state-sse-summary.sanitized.json` |
| Exposure drained to zero | pass | `raw/zero-exposure.sanitized.json` |
| Restart/cold-start safety | pass | `raw/dry-live-summary.sanitized.json` |
| Postgame score | pass | `raw/postgame-lifecycle.sanitized.json` |
| Postgame settle | pass | `raw/postgame-lifecycle.sanitized.json` |
| Postgame claim/no-op | pass | `raw/postgame-lifecycle.sanitized.json` |
| Cost within cap | pass | `raw/balance-reconciliation.sanitized.json` |
