# Scenario matrix

| Scenario | Status | Evidence |
|---|---|---|
| Target preflight and allowlist | `pass` | `raw/target-preflight.sanitized.json` |
| Repository and runtime pins | `pass` | `raw/runtime-and-setup.sanitized.json` |
| Wallet identity and balances | `pass` | `raw/runtime-and-setup.sanitized.json` |
| Bounded approvals and revocation | `pass` | `raw/zero-exposure.sanitized.json` |
| Dry-run quote loop | `pass` | `raw/dry-live-summary.sanitized.json` |
| Live commitments posted | `pass_with_caveats` | `raw/dry-live-summary.sanitized.json` |
| Controlled live fill | `pass` | `raw/live-fill.sanitized.json` |
| Own-state SSE canonical fill source | `pass` | `raw/own-state-sse-summary.sanitized.json` |
| Exposure drained to zero | `pass_with_caveats` | `raw/zero-exposure.sanitized.json` |
| Restart and cold-start safety | `pass_with_caveats` | `raw/dry-live-summary.sanitized.json` |
| Postgame score | `pass` | `raw/postgame-lifecycle.sanitized.json` |
| Postgame settlement | `pass` | `raw/postgame-lifecycle.sanitized.json` |
| Winning-position claims and no-op | `pass` | `raw/postgame-lifecycle.sanitized.json` |
| Cost and accounting within cap | `pass` | `raw/balance-reconciliation.sanitized.json` |
