# Ospex Evidence Artifact: 2026-05-20 MLB Three-Game MM Shakeout

**Artifact ID:** `2026-05-20-mlb-three-game-mm-shakeout-contests-14-16`  
**Network:** Polygon mainnet  
**Contests:** `14`, `15`, `16`  
**Speculations:** `7`, `8`, `9`  
**Market:** MLB moneyline  
**Status:** complete / verified with caveats

## Result

All three selected MLB games finished, all protocol contests were scored, all three moneyline speculations settled closed, and all indexed winning `upper`/away positions were claimed. Final `claim-all --dry-run` sweeps for the market-maker, flow, and stage wallets returned zero remaining claimable entries.

- Cincinnati Reds defeated Philadelphia Phillies, **9–4** (`contest 14`, `speculation 7`).
- Texas Rangers defeated Colorado Rockies, **5–4** (`contest 15`, `speculation 8`).
- Toronto Blue Jays defeated New York Yankees, **2–1** (`contest 16`, `speculation 9`).

Protocol semantics for these moneyline markets:

- `upper` / `away` = away team
- `lower` / `home` = home team
- winning side for all three games = `away` / `upper`

External score source:

- MLB Stats API, date `2026-05-20`, all three games status `Final`.

## What this artifact proves

This run demonstrates a three-market low-value Ospex market-maker lifecycle:

1. three contests and moneyline speculations existed on Polygon mainnet
2. the market-maker posted live EIP-712 commitments in three scheduled windows
3. a controlled flow wallet matched one tiny market-maker quote in each market
4. live exposure was pulled/expired before first pitch, with zero visible live commitments at wrap-up
5. all three contests were scored from final MLB results
6. all three speculations settled closed
7. all winning positions were claimed
8. final post-wrap `claim-all --dry-run` sweeps showed no remaining claimable entries

## Markets and controlled fills

### CIN @ PHI — contest `14`, speculation `7`

- Final score: Cincinnati Reds 9, Philadelphia Phillies 4.
- Seed fill tx: `https://polygonscan.com/tx/0x28f45ca18d7ea0040c6951b61c1c4317ef2c56d328a6307a48f175165ad7807c`
- Controlled MM fill tx: `https://polygonscan.com/tx/0xbf16a7f619c7125d5cdd6880717c3de386a0df9202cfdce0f12dab09f52adbe8`
- Controlled commitment: `0x5ff2d8dd45231fd4e517a5f4edf62dc09e4ff467d1185a6e45e801a0c563a1a0`
- MM maker side: `upper` / away / Cincinnati Reds
- Controlled taker side: `lower` / home / Philadelphia Phillies
- Maker risk: `0.0359 USDC`
- Taker risk: `0.049901 USDC`
- Odds tick: `239`

### TEX @ COL — contest `15`, speculation `8`

- Final score: Texas Rangers 5, Colorado Rockies 4.
- Seed fill tx: `https://polygonscan.com/tx/0x7c5b551a1d9910a6338e920f175fb55bb0cc711896454b405008f9ca3915940a`
- Controlled MM fill tx: `https://polygonscan.com/tx/0x2f0da9d6a0b9706bbc27b94dab3d6aab6c42b2325b4f1cd7835c9ce73a35f540`
- Controlled commitment: `0xe6839b23f450421da870934b32045399702d3b01e7958f5a811d9ae2fdf3c15b`
- MM maker side: `upper` / away / Texas Rangers
- Controlled taker side: `lower` / home / Colorado Rockies
- Maker risk: `0.0561 USDC`
- Taker risk: `0.049929 USDC`
- Odds tick: `189`

### TOR @ NYY — contest `16`, speculation `9`

- Final score: Toronto Blue Jays 2, New York Yankees 1.
- Seed fill tx: `https://polygonscan.com/tx/0xe4a035a0e486ae7209282334340c6e1c9b8cc4c4d2c9d72aa7830c539bf2fcbd`
- Controlled MM fill tx: `https://polygonscan.com/tx/0x3c8e16a5406afe7dd9bdef5891bdf2640b877a0b69157c4324a8ba7670816664`
- Controlled commitment: `0xf305b6f8be5a57265add77abaf710424a6943bf852b1d434bbb070e28addd73e`
- MM maker side: `upper` / away / Toronto Blue Jays
- Controlled taker side: `lower` / home / New York Yankees
- Maker risk: `0.032 USDC`
- Taker risk: `0.04992 USDC`
- Odds tick: `256`

## Quote-window telemetry

All three live windows were low-value and ended before first pitch. The market-maker had zero visible live commitments at window end / wrap-up.

- CIN @ PHI: 116 live ticks, 10 submits, 64 replaces, 2 soft-cancels, 1 controlled fill, 82 competitiveness samples, 100% at/inside reference book, mean `+5.83` ticks vs reference.
- TEX @ COL: 116 live ticks, 8 submits, 66 replaces, 2 soft-cancels, 1 controlled fill, 80 competitiveness samples, 100% at/inside reference book, mean `+5.76` ticks vs reference.
- TOR @ NYY: 114 live ticks, 8 submits, 64 replaces, 2 soft-cancels, 1 controlled fill, 80 competitiveness samples, 100% at/inside reference book, mean `+5.31` ticks vs reference.

## Scoring, settlement, and claims

Scoring:

- Contest 14 score tx: `https://polygonscan.com/tx/0x65bc39c82174f36de8e7fecfd5c2715a2a5e60e6f365ea0ca9b2a25dcf7425c1`
- Contest 15 score tx: `https://polygonscan.com/tx/0xb0b18bad55e1cf20d8b51e638f96c5093a702046ed5ee5351b6ac525d81e927e`
- Contest 16 score tx: `https://polygonscan.com/tx/0x6e60e998c1ddd43a4b76e43eba0335a7b9c35c75b7e1ba1ab5aab630ad47b829`

Settlement and claim transactions are included in `evidence.json` and `raw/tx-receipts.summary.json`. Final indexed winning claims:

- Flow seed claims: `0.0573 USDC` total return across three tiny seed positions.
- Market-maker controlled-fill claims: `0.27375 USDC` total return, with `0.14975 USDC` realized profit across the three controlled fills.
- Stage seed maker had lower/home positions in all three seed fills; all three lost and had no claim expected.

## Caveats / product debt observed

- Postgame first-pass and retry cron scripts timed out at 120s. They did score the contests, but did not fully finish settlement/claim documentation before timeout.
- Manual wrap-up completed the remaining settlement/claim sweep. The first `claim-all` execute pass partially failed after settlement state changed; repeating the sweep completed the remaining claims, and final dry-runs were empty.
- MM telemetry reported `PositionWithoutCommitment` while polling wallet positions from earlier markets not present in the current local MM commitment state. It did not hold quoting or leave live exposure.
- MM telemetry reported `UnexpectedFillStatus` for disappeared commitments whose DB rows could still read `status=open` after expiry/cancel/fill classification. Wrap-up checks still found zero visible live unfilled commitments.
- The run used frozen SDK/CLI `0.2.1`. The Phase 1.5 core API fixes were merged after/during wrap-up, but this evidence does **not** prove the next packaged/deployed stack yet. Next pass should deploy/rebuild/re-pull first.

## Release/deploy context before next tests

Verified GitHub state at wrap-up:

- ospex-core-api PR #20 merged at `2026-05-21T03:36:21Z`, merge commit `31cdc6d45131ad7533cf4d33d7be4b26177dfbfd`.
- ospex-core-api PR #21 merged at `2026-05-21T07:52:46Z`, merge commit `7fa54f68f193bb49f057a4fb173a98c2f17a3b3b`.

Still pending before more tests:

- bump SDK/package version for the next evidence pass, likely `0.3.0`
- rebuild tarballs / refresh frozen runtime install
- deploy updated services to Heroku
- re-pull/reinstall market-maker runtime against the deployed/package version
- then choose the next roadmap-backed test scope

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/indexer-snapshot.sanitized.json` — selected Supabase/indexer rows with commitment signatures and raw event payload blobs omitted
- `raw/tx-receipts.summary.json` — compact Polygon receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observations
- `raw/mm-run-summaries.sanitized.json` — summarized MM telemetry/control reports
- `raw/claim-sweeps.sanitized.json` — sanitized claim-all dry-run/execute outputs

Private operator files, RPC URLs, wallet password files, raw signatures, and noisy raw telemetry logs are intentionally excluded.
