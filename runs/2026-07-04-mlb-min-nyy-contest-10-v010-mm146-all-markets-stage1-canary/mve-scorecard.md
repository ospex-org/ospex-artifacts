# MVE scorecard

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

- **Target preflight and allowlist** (`target-preflight`): proven_live — Primary MIN away @ NYY home contest 10/specs 18/19/20 passed pre-game status, identity, allowlist, odds, and lead-time gates.
- **Repo/runtime gates** (`repo-runtime-gates`): proven_live — SDK/CLI v0.10.0, MM head 6f3ccc1 with PR #146 approval self-heal and PR #145 own-state orphan safety coverage, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified.
- **Wallet auth, balances, allowances** (`wallet-auth-balances`): proven_live — Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded.
- **Bounded approvals / no unlimited approvals** (`bounded-approvals`): proven_live — Only bounded USDC approvals were used; live autoApprove used exact mode and raised PositionModule allowance from 0.400000 to 0.600001 USDC.
- **Dry-run quote loop** (`dry-run-quote-loop`): proven_synthetic_only — Candidates --allowlist-only returned contest 10 moneyline, spread, and total quote_ready; dry run would-submit remained target-scoped.
- **Live commitments posted** (`live-commitments-posted`): proven_live — Tiny live moneyline, spread, and total commitments posted under strict allowlist [10], seedSpeculations=false.
- **Controlled live fill** (`live-fill`): proven_live — Two controlled live fills succeeded: spread commitment 0xd44aa5a2fdba… and total commitment 0x5cd5eb435cba… using ospex-flow-a.
- **Own-state SSE canonical fill source** (`own-state-sse-canonical-fill`): proven_live — Telemetry captured both fills with source own-state-stream for the filled spread and total commitment hashes.
- **Exposure drained to zero** (`exposure-drain-zero`): proven_live — Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained.
- **Restart/cold-start safety** (`restart-cold-start-safety`): proven_synthetic_only — A scratch-state dry-run/cold-start probe loaded state cleanly, expired copied stale records, and did not create duplicate live exposure.
- **Postgame score** (`postgame-score`): proven_live — Official final score MIN 11, NYY 4 was verified and contest 10 scored via R5/CRE. Operator/watchdog caveat: The postgame cron/watchdog initially no-oped because core games API status still reported `upcoming` after MLB official final. Postgame was manually resumed after independent MLB Stats official-final verification; score/settle/claim completed successfully, and final zero-state was verified. This is an operator/watchdog methodology caveat, not a protocol/MM failure.
- **Postgame settle** (`postgame-settle`): proven_live — Moneyline speculation 18 settled to away/upper/Minnesota Twins; spread 19 to away/upper/Minnesota Twins +1.5; total 20 to over/upper/over 10. Completed after manual resume from the operator/watchdog caveat documented under postgame-score.
- **Postgame claim/no-op** (`postgame-claim`): proven_live — Winning upper positions for stage-maker-a and stage-maker-b were claimed; losing positions are no-op/not claimable, and final target positions are zero. Completed after manual resume from the operator/watchdog caveat documented under postgame-score.
- **Cost within cap** (`cost-within-cap`): proven_live — Tiny canary risk plus protocol fees stayed within the requested cap; recorded lifecycle transactions are summarized.
