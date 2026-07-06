# MVE scorecard

| ID | Capability | Proof | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `target-preflight` | Target preflight and allowlist | `proven_live` | `raw/target-preflight.sanitized.json` | PHI @ KC contest 17 and specs 39/40/41 passed target identity, allowlist, odds, and runway gates. |
| `repo-runtime-gates` | Repo/runtime gates | `proven_live` | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.10.0, MM head 6f3ccc1, installed MM SDK v0.9.0, and required ancillary repo heads were verified. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `proven_live` | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public balances were sufficient and allowances were bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `proven_live` | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were created. |
| `dry-run-quote-loop` | Dry-run quote loop | `proven_synthetic_only` | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned quote-ready rows for contest 17 and all three seeded markets; dry run stayed target-scoped with seedSpeculations=false. |
| `live-commitments-posted` | Live commitments posted | `proven_live` | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline and spread commitments posted under strict contest allowlist [17], seedSpeculations=false; total skipped live after a reference-line mismatch. |
| `live-fill` | Controlled live fill | `proven_live` | `raw/live-fill.sanitized.json` | A controlled taker filled one live MM spread quote for contest 17. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `proven_live` | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured eventCounts.fill=1 with canonicalFillObserved=true; startup stream-health hold cleared before fill, bad own-state counters stayed zero, and the single own-state-stream error was OwnerPositionStatusForUnknownPosition. |
| `exposure-drain-zero` | Exposure drained to zero | `proven_live` | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | `not_applicable` |  | Block C brief did not require a separate scratch cold-start probe; zero-open and no-orphan shutdown proofs were captured. |
| `postgame-score` | Postgame score | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Official final score was verified and contest 17 scored via R5/CRE using CLI v0.10.0 score --wait. |
| `postgame-settle` | Postgame settle | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Moneyline, spread, and total speculations 39/40/41 carried settledAt values after scoring; explicit settle commands returned alreadySettled. |
| `postgame-claim` | Postgame claim/no-op | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Winning controlled positions were claimed and final target positions are zero. |
| `cost-within-cap` | Cost within cap | `proven_live` | `raw/tx-receipts.summary.json` | Tiny manual/live risk plus protocol fees stayed within the Phase 1 Block C low-cap budget. |

## Verdict

`FULL_GREEN` / `MVE_PHASE1_BLOCK_C_GREEN_WITH_CAVEATS`
