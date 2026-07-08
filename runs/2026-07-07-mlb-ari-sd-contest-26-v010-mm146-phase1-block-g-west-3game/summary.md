# Arizona Diamondbacks @ San Diego Padres — MVE Phase 1 Block G west three-game

- Artifact ID: `2026-07-07-mlb-ari-sd-contest-26-v010-mm146-phase1-block-g-west-3game`
- Scope: Block G only; Block F was not mutated or republished.
- Primary schema-bound target: `A_ARI_SD` — contest `26`, moneyline spec `66`.
- Additional Block G targets: `B_TOR_SF` contest `27` specs `69/70/71`; `C_COL_LAD` contest `28` specs `72/73/74`.
- Live MM runIds: `2026-07-07T23-45-26-158Z-o7ow3r` (first attempt, no quotes) and `2026-07-07T23-50-14-611Z-nibqef` (retry).
- Dry-run gate: `PASS` (`wouldSubmitCount=18`, strict allowlist `[26,27,28]`, `seedSpeculations=false`).
- First live attempt caveat: bankroll exposure ceiling `0.24 / 0.15` USDC worst-case; no quotes posted; risk caps then reduced to `0.001` quote / `0.285` sport-team before retry.
- Live quotes posted on retry: `18` across moneyline, spread, and total.
- Controlled fills: A moneyline tx `0xd6548da7751e7c493cb2bc258f7a9e16b3479bc383144143b5fc129e4c9d5e6a`; B spread tx `0xf7421f6d3ffe2c9d4df39a65982b38232b65959fa3e5acfc3e5f4b63444ea6c1`; C total tx `0x2d8a3304129b7a93abc2f92481dfc0b8a7e6b08b888f44721474247764415905`.
- Stream-health hold events: entered/cleared in first attempt and retry; retry cleared before posting/fill. Bad own-state and OwnerPositionStatusForUnknownPosition counts: `0`.
- Final scores: ARI 1 / SD 4; TOR 9 / SF 3; COL 4 / LAD 3.
- Settled specs: `66-74`; final open commitments for contests `26-28`: `0`.
- Final target wallet positions: active `0`, pendingSettle `0`, claimable `0` for `stage_maker_a`, `stage_maker_b`, `flow_a`, and `fresh_user`.
- Verdict: `MVE_PHASE1_BLOCK_G_GREEN_WITH_CAVEATS` (`FULL_GREEN` scorecard label).

Caveats: First live attempt was a no-quote risk refusal at the bankroll exposure ceiling (0.24 / 0.15 USDC worst-case); retry used reduced caps of 0.001 USDC per quote and 0.285 USDC sport/team. Startup stream-health hold entered with exposureWei6=242000 and cleared before live submit/fill in both first attempt and retry. Controlled fill previews initially retried smaller risk because 0.002 USDC requested taker risk exceeded the visible remaining maker risk for the selected quote; successful fills used 0.001 USDC target risk. C_COL_LAD scoring required two score-request txs before the score callback appeared; final score callback and postgame zero-state completed.
