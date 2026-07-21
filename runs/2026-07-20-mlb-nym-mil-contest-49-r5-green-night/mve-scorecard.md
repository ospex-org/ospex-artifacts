# MVE scorecard

**Verdict: FULL_GREEN**

| Capability | Proof | Evidence |
|---|---|---|
| Target preflight and allowlist | proven_live | `raw/target-preflight.sanitized.json` |
| Repo/runtime gates | proven_live | `raw/runtime-and-setup.sanitized.json` |
| Wallet auth, balances, allowances | proven_live | `raw/runtime-and-setup.sanitized.json` |
| Bounded approvals / no unlimited approvals | proven_live | `raw/runtime-and-setup.sanitized.json` |
| Dry-run quote loop | proven_synthetic_only | `raw/dry-live-summary.sanitized.json` |
| Live commitments posted | proven_live | `raw/dry-live-summary.sanitized.json` |
| Controlled live fill | proven_live | `raw/live-fill.sanitized.json` |
| Own-state SSE canonical fill source | proven_live | `raw/own-state-sse-summary.sanitized.json` |
| Exposure drained to zero | proven_live | `raw/zero-exposure.sanitized.json` |
| Restart/cold-start safety | proven_synthetic_only | `raw/dry-live-summary.sanitized.json` |
| Postgame score | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| Postgame settle | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| Postgame claim/no-op | proven_live | `raw/postgame-lifecycle.sanitized.json` |
| Cost within cap | proven_live | `raw/balance-reconciliation.sanitized.json` |

Final zero checked at `2026-07-21T03:31:17Z`.
