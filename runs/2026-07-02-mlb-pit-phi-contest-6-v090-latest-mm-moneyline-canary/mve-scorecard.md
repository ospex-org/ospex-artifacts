# MVE readiness scorecard

Verdict: **FULL_GREEN**

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| Target preflight and allowlist | proven_live | raw/target-preflight.sanitized.json | Primary PIT away @ PHI home contest 6/spec 10 passed official pre-game status, identity, allowlist, odds, and lead-time gates. |
| Repo/runtime gates | proven_live | raw/release-runtime-matrix.sanitized.json | SDK/CLI v0.9.0, MM head 6121a73+, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified. |
| Wallet auth, balances, allowances | proven_live | raw/wallet-auth-balance-allowances.sanitized.json | Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded. |
| Bounded approvals / no unlimited approvals | proven_live | raw/bounded-approvals.sanitized.json | Only a bounded 1.000000 USDC TreasuryModule approval was sent for ospex-stage-maker-b; no unlimited approvals were used. |
| Dry-run quote loop | proven_synthetic_only | raw/mm-dryrun-summary.sanitized.json | Candidates --allowlist-only returned exactly contest 6 quote_ready; quote dry-run canQuote=true; dry run would-submit remained target-scoped. |
| Live commitments posted | proven_live | raw/live-public-commitments-posted.sanitized.json | Two tiny live commitments posted under strict allowlist [6], moneyline only, speculation 10 only. |
| Controlled live fill | proven_live | raw/live-fill.sanitized.json | Exactly one controlled fill succeeded against live commitment 0x6d2a5bd0… using ospex-flow-a. |
| Own-state SSE canonical fill source | proven_live | raw/own-state-sse-summary.sanitized.json | Telemetry captured the fill with source own-state-stream for the filled commitment hash. |
| Exposure drained to zero | proven_live | raw/zero-exposure.sanitized.json | Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained. |
| Restart/cold-start safety | proven_synthetic_only | raw/restart-cold-start-probe.sanitized.json | A fresh dry-run/cold-start probe stayed target-scoped; synthetic dry records were cleaned from live state before final reporting. |
| Postgame score | proven_live | raw/postgame-lifecycle.sanitized.json | Official final score PIT 6, PHI 1 was verified and contest 6 scored. |
| Postgame settle | proven_live | raw/postgame-lifecycle.sanitized.json | Speculation 10 settled to away/upper/Pittsburgh Pirates. |
| Postgame claim/no-op | proven_live | raw/postgame-lifecycle.sanitized.json | Winning upper/Pittsburgh Pirates seed-maker and live-taker positions were claimed; losing lower/PHI positions are no-op. |
| Cost within cap | proven_live | raw/tx-receipts.summary.json | Tiny canary risk stayed within the requested caps; recorded lifecycle gas is summarized. |
