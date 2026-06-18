# Scenario matrix

| ID | Scenario | Status | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Exact target preflight | `pass` | `raw/target-preflight.sanitized.json` | Official identity, status, contest/speculation, and allowlist matched BAL away @ SEA home. |
| `repo-runtime-gates` | Release/runtime gate | `pass` | `raw/release-runtime-matrix.sanitized.json` | v0.7.1 CLI/SDK and MM runtime gates passed. |
| `wallet-auth-balances` | Wallet role hygiene | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Live maker stayed separate from setup roles and was clean before live. |
| `bounded-approvals` | Bounded approvals | `pass` | `raw/bounded-approvals.sanitized.json` | Approvals were bounded; no unlimited approval used. |
| `dry-run-quote-loop` | Quote dry-run | `pass` | `raw/mm-dryrun-summary.sanitized.json` | Quote dry-run returned computed/canQuote true. |
| `live-commitments-posted` | Live commitments posted | `pass` | `raw/live-public-commitments-posted.sanitized.json` | Live MM posted target-scoped tiny commitments. |
| `live-fill` | Controlled live fill | `pass` | `raw/live-fill.sanitized.json` | Exactly one controlled fill executed. |
| `own-state-sse-canonical-fill` | Canonical own-state fill | `pass` | `raw/own-state-sse-summary.sanitized.json` | Canonical fill telemetry source was own-state-stream. |
| `exposure-drain-zero` | Final zero exposure | `pass` | `raw/zero-exposure.sanitized.json` | Visible/open exposure and claim sweeps are zero after postgame cleanup. |
| `restart-cold-start-safety` | Restart/cold-start probe | `not_applicable` | — | A separate restart probe was not part of this Stage-1 cleanup; final zero/process checks were used. |
| `postgame-score` | Postgame score | `pass` | `raw/postgame-lifecycle.sanitized.json` | Contest 48 scored to BAL 0, SEA 3. |
| `postgame-settle` | Postgame settle | `pass` | `raw/postgame-lifecycle.sanitized.json` | Speculation 37 settled to home/lower/Seattle. |
| `postgame-claim` | Postgame claim/no-op | `pass` | `raw/postgame-lifecycle.sanitized.json` | Winning positions claimed; losing positions not claimable. |
| `cost-within-cap` | Cost/risk cap | `pass` | `raw/tx-receipts.summary.json` | Maker risk and observed exposure stayed within Stage-1 caps; gas recorded. |
