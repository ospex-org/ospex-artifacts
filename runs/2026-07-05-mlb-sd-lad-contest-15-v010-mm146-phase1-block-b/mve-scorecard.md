# MVE scorecard

| ID | Capability | Proof | Evidence | Notes |
|---|---|---|---|---|
| `target-preflight` | Target preflight and allowlist | `proven_live` | `raw/target-preflight.sanitized.json` | San Diego Padres @ Los Angeles Dodgers contest 15 and specs 33/34/35 passed target identity, allowlist, odds, and runway gates. |
| `repo-runtime-gates` | Repo/runtime gates | `proven_live` | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.10.0, MM head 6f3ccc1 with strict allowlist / own-state / bounded-approval coverage, installed MM SDK v0.9.0, and ancillary repo heads were verified. |
| `wallet-auth-balances` | Wallet auth, balances, allowances | `proven_live` | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public balances were sufficient and allowances were bounded. |
| `bounded-approvals` | Bounded approvals / no unlimited approvals | `proven_live` | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were created. |
| `dry-run-quote-loop` | Dry-run quote loop | `proven_synthetic_only` | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned quote-ready rows for contest 15 and all seeded markets; dry run stayed target-scoped with seedSpeculations=false. |
| `live-commitments-posted` | Live commitments posted | `proven_live` | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline, spread, and total commitments posted under strict contest allowlist [15], seedSpeculations=false. |
| `live-fill` | Controlled live fill | `proven_live` | `raw/live-fill.sanitized.json` | A controlled taker filled one live MM total quote for contest 15. |
| `own-state-sse-canonical-fill` | Own-state SSE canonical fill source | `proven_live` | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the controlled fill without unknown-own-fill, owner-mapping, or divergence safety events; a startup stream-health hold cleared before controlled fill. |
| `exposure-drain-zero` | Exposure drained to zero | `proven_live` | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| `restart-cold-start-safety` | Restart/cold-start safety | `proven_synthetic_only` | `raw/restart-cold-start-probe.sanitized.json` | A scratch-state dry-run/cold-start probe loaded state cleanly and did not create duplicate live exposure; live CLI reads remained zero-open. |
| `postgame-score` | Postgame score | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Official final score was verified and contest 15 scored via R5/CRE using CLI v0.10.0 score --wait. |
| `postgame-settle` | Postgame settle | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Moneyline, spread, and total speculations 33/34/35 settled to expected winning sides. |
| `postgame-claim` | Postgame claim/no-op | `proven_live` | `raw/postgame-lifecycle.sanitized.json` | Winning controlled positions were claimed, losing positions were no-op/not claimable, and final target positions are zero. |
| `cost-within-cap` | Cost within cap | `proven_live` | `raw/tx-receipts.summary.json` | Tiny manual/live risk plus protocol fees stayed within the Phase 1 Block B low-cap budget; lifecycle transactions are summarized. |

## Verdict

`FULL_GREEN` / `MVE_PHASE1_BLOCK_B_GREEN_WITH_CAVEATS`
