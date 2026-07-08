# Scenario matrix — MVE Phase 1 Block G west three-game

- `target-preflight`: `pass` — A/B/C target games, contests 26-28, and specs 66-74 passed allowlist, odds, status, and quote-ready gates.
- `repo-runtime-gates`: `pass` — SDK/CLI v0.10.0, MM head 6f3ccc1, MM internal SDK v0.9.0, and ancillary repo heads were recorded.
- `wallet-auth-balances`: `pass` — Expected-address/auth checks and public balances/allowances were captured; secret paths/signatures were omitted.
- `bounded-approvals`: `pass` — Only bounded USDC approvals were used; no unlimited approval was recorded.
- `dry-run-quote-loop`: `pass` — Dry run wouldSubmitCount=18 across nine contest/market pairs with strict allowlist [26,27,28], seedSpeculations=false, no bad events.
- `live-commitments-posted`: `pass_with_caveats` — Retry live run posted 18 tiny live quotes across moneyline, spread, and total for contests 26-28.
- `live-fill`: `pass_with_caveats` — Controlled fills landed on A moneyline, B spread, and C total; primary binding is A moneyline contest 26/spec 66.
- `own-state-sse-canonical-fill`: `pass_with_caveats` — Telemetry recorded three own-state-stream fill events; bad own-state and OwnerPositionStatusForUnknownPosition counts were zero.
- `exposure-drain-zero`: `pass` — Final open commitments are zero and final target wallet active/pending/claimable counts are zero.
- `restart-cold-start-safety`: `not_applicable` — Block G did not include a separate scratch cold-start probe; zero-open and no-orphan process checks were captured.
- `postgame-score`: `pass_with_caveats` — Official finals were verified and score request/callback evidence exists for contests 26-28.
- `postgame-settle`: `pass` — SPECULATION_SETTLED events exist for specs 66-74.
- `postgame-claim`: `pass_with_caveats` — Winning positions were claimed; final target wallet counts are zero.
- `cost-within-cap`: `pass` — Budget forecast total fees plus controlled risk envelope was 7.73 USDC, within 25 USDC target and 35 USDC hard stop.
