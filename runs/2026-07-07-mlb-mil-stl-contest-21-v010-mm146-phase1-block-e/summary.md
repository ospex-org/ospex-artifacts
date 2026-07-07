# Milwaukee Brewers @ St. Louis Cardinals — MVE Phase 1 Block E

- Artifact ID: `2026-07-07-mlb-mil-stl-contest-21-v010-mm146-phase1-block-e`
- Contest: `21`
- Speculations: moneyline `52`, spread `53`, total `51`
- Live MM runId: `2026-07-07T15-38-40-995Z-e0remr`
- Live quotes posted: `6` across moneyline, spread, and total
- Controlled fill: spread quote `0x61a41a1bd62c7d64007442201743d844cb583c3d7b17c80a75584bcfb8688c4e`, St. Louis Cardinals +1.5, tx `0x8b767a11cc988b2af28eb1c82309549764015fb69f6d20064f3aa527a8e0e85c`
- Pre-live dry-run gate: `PASS` (`wouldSubmitCount=6`, strict allowlist `[21]`, `seedSpeculations=false`)
- Manual seed/fill: moneyline, spread, and total filled with tiny controlled risk; contest open commitments returned to `0`
- Final score: Milwaukee Brewers 4, St. Louis Cardinals 3
- Score tx: `0x8aaac163b8970dcc38548a8c610f5d53a199a823a1319c381c7b55f2aac1ffe8`
- Settle txs: total `0x66f293138384013400855506a909b3c5df5bc7266db353e68fdea5a72e42de9b`, moneyline `0x105ccdde7064ede7422871a90317888c04b3ce529f563d0311e4f36c366e7c98`, spread `0xfd5d2651fc3b07848e5ed7272271df2802dfc93b05aa7b996facc43a26ffac28`
- Claim txs: `0x205b2dbc608eeb97a25b54a2243b8f72f2b8e3b7152f7c1b3edb94b8bf70ab51`, `0x6cae0c08c230fc163e249c9a340b229f76be6682b1e15305f342bf0c743d0a9d`, `0x8219398a1899bc2b48c4c6c1913768d5d171c709ff59f891066a2fe88a351246`, `0x0b0f411a414a2afc9b56a21ab63e63bbef17f2890db73838d923b8056966cbe2`
- Final open commitments: `0`
- Final target positions: active `0`, pendingSettle `0`, claimable `0` for controlled wallets after manual remediation
- Verdict: `MVE_PHASE1_BLOCK_E_GREEN_WITH_CAVEATS` (`FULL_GREEN` scorecard label)

Caveats: startup stream-health hold entered and cleared before posting/fill; controlled fill preview warned expires-soon; initial manual moneyline/spread operator commands required no-write shell-quoting retries; the no-agent postgame watcher surfaced residual claimables before manual remediation claims completed zero-state.
