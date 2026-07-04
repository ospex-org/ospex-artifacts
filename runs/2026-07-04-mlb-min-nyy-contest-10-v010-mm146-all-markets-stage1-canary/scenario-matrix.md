# Scenario matrix

- **Target preflight and allowlist** (`target-preflight`): pass — Primary MIN away @ NYY home contest 10/specs 18/19/20 passed pre-game status, identity, allowlist, odds, and lead-time gates.
- **Repo/runtime gates** (`repo-runtime-gates`): pass — SDK/CLI v0.10.0, MM head 6f3ccc1 with PR #146 approval self-heal and PR #145 own-state orphan safety coverage, installed SDK v0.9.0, typecheck/test/build, and ancillary repo heads were verified.
- **Wallet auth, balances, allowances** (`wallet-auth-balances`): pass — Expected-address checks passed for ospex-stage-maker-b, ospex-stage-maker-a, and ospex-flow-a; public allowances were bounded.
- **Bounded approvals / no unlimited approvals** (`bounded-approvals`): pass — Only bounded USDC approvals were used; live autoApprove used exact mode and raised PositionModule allowance from 0.400000 to 0.600001 USDC.
- **Dry-run quote loop** (`dry-run-quote-loop`): pass — Candidates --allowlist-only returned contest 10 moneyline, spread, and total quote_ready; dry run would-submit remained target-scoped.
- **Live commitments posted** (`live-commitments-posted`): pass_with_caveats — Tiny live moneyline, spread, and total commitments posted under strict allowlist [10], seedSpeculations=false.
- **Controlled live fill** (`live-fill`): pass_with_caveats — Two controlled live fills succeeded: spread commitment 0xd44aa5a2fdba… and total commitment 0x5cd5eb435cba… using ospex-flow-a.
- **Own-state SSE canonical fill source** (`own-state-sse-canonical-fill`): pass — Telemetry captured both fills with source own-state-stream for the filled spread and total commitment hashes.
- **Exposure drained to zero** (`exposure-drain-zero`): pass — Final public/API/MM visible-open exposure is zero, target active/pending/claimable positions are zero after postgame, and no orphan MM process remained.
- **Restart/cold-start safety** (`restart-cold-start-safety`): pass — A scratch-state dry-run/cold-start probe loaded state cleanly, expired copied stale records, and did not create duplicate live exposure.
- **Postgame score** (`postgame-score`): pass — Official final score MIN 11, NYY 4 was verified and contest 10 scored via R5/CRE.
- **Postgame settle** (`postgame-settle`): pass — Moneyline speculation 18 settled to away/upper/Minnesota Twins; spread 19 to away/upper/Minnesota Twins +1.5; total 20 to over/upper/over 10.
- **Postgame claim/no-op** (`postgame-claim`): pass — Winning upper positions for stage-maker-a and stage-maker-b were claimed; losing positions are no-op/not claimable, and final target positions are zero.
- **Cost within cap** (`cost-within-cap`): pass — Tiny canary risk plus protocol fees stayed within the requested cap; recorded lifecycle transactions are summarized.
