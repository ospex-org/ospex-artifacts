# MVE scorecard — 2026-07-05-mlb-nym-atl-contest-13-v010-mm146-phase1-block-a

Verdict: **FULL_GREEN** — The v0.10.0/R5 MM #146 strict-allowlist Phase 1 Block A two-contest MVE for New York Mets @ Atlanta Braves completed the full lifecycle: contest 13 was created and verified; moneyline, spread, and total speculations 27/28/29 were manually seeded and filled with zero residual seed exposure; the market maker posted tiny live quotes under strict contest allowlist [13,14] with seedSpeculations=false; one controlled live total quote was filled; visible quotes were soft-cancelled or expired; final open commitments were zero; official final score New York Mets 10 / Atlanta Braves 9 was verified; contest 13 was scored through R5/CRE; target speculations were settled, winning controlled positions were claimed, and final target active/pending/claimable positions are zero.

| Capability | Proof | Evidence | Notes |
|---|---:|---|---|
| Target preflight and allowlist | proven_live | `raw/target-preflight.sanitized.json` | New York Mets @ Atlanta Braves contest 13 and specs 27/28/29 passed target identity, allowlist, odds, and runway gates. |
| Repo/runtime gates | proven_live | `raw/release-runtime-matrix.sanitized.json` | SDK/CLI v0.10.0, MM head 6f3ccc1 with strict allowlist / own-state / bounded-approval coverage, installed MM SDK v0.9.0, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | proven_live | `raw/wallet-auth-balance-allowances.sanitized.json` | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | proven_live | `raw/bounded-approvals.sanitized.json` | Only bounded USDC approvals were used; no unlimited approvals were created. |
| Dry-run quote loop | proven_synthetic_only | `raw/mm-dryrun-summary.sanitized.json` | Candidates --allowlist-only returned quote-ready rows for both allowlisted contests and all seeded markets; dry run stayed target-scoped. |
| Live commitments posted | proven_live | `raw/live-public-commitments-posted.sanitized.json` | Tiny live moneyline, spread, and total commitments posted under strict allowlist [13,14], including contest 13, seedSpeculations=false. |
| Controlled live fill | proven_live | `raw/live-fill.sanitized.json` | A controlled taker filled the MM total quote for contest 13; tx 0x51e2dea37d…. |
| Own-state SSE canonical fill source | proven_live | `raw/own-state-sse-summary.sanitized.json` | Telemetry captured the controlled fills without unknown-own-fill, owner-mapping, or divergence safety events. |
| Exposure drained to zero | proven_live | `raw/zero-exposure.sanitized.json` | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | proven_synthetic_only | `raw/restart-cold-start-probe.sanitized.json` | A scratch-state dry-run/cold-start probe loaded state cleanly and did not create duplicate live exposure; live CLI reads remained zero-open. |
| Postgame score | proven_live | `raw/postgame-lifecycle.sanitized.json` | Official final score New York Mets 10, Atlanta Braves 9 was verified and contest 13 scored via R5/CRE. |
| Postgame settle | proven_live | `raw/postgame-lifecycle.sanitized.json` | Moneyline, spread, and total speculations 27/28/29 settled to the expected winning sides or push semantics. |
| Postgame claim/no-op | proven_live | `raw/postgame-lifecycle.sanitized.json` | Winning controlled positions were claimed, losing positions were no-op/not claimable, and final target positions are zero. |
| Cost within cap | proven_live | `raw/tx-receipts.summary.json` | Tiny manual/live risk plus protocol fees stayed within the Phase 1 low-cap budget; lifecycle transactions are summarized. |
