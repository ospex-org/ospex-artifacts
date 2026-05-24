# Ospex Evidence Artifact: Rangers @ Angels MM Partial-Fill Investigation Smoke

- **Artifact ID:** `2026-05-24-mlb-tex-laa-contest-21-mm-partial-smoke`
- **Network:** Polygon mainnet
- **Contest:** `21`
- **Speculation:** `12`
- **Market:** MLB moneyline
- **Status:** partial / investigation artifact, not green acceptance evidence

## Direct answer

Yes — the live smoke was run. It was not paused before live action.

The run created/verified the target contest, created moneyline speculation #12, started the MM, and executed a tiny controlled partial fill against the MM. It was then stopped cleanly.

## Result

Texas Rangers @ Los Angeles Angels finished **Angels 5, Rangers 2** according to MLB Stats API (`Final`, gamePk `824030`).

Protocol semantics for this market:

- `upper` / `away` = Texas Rangers
- `lower` / `home` = Los Angeles Angels
- external winning side = `home` / `lower`

At artifact capture, the Ospex contest was still `verified` / unscored and speculation #12 was still open. This artifact intentionally records that state; no additional manual score, settle, or claim transactions were sent during this wrap-up.

## What this artifact proves

This run demonstrates operationally safe live execution, but **not** clean D1/D2 acceptance:

1. contest #21 was created and verified for Texas Rangers @ Los Angeles Angels
2. moneyline speculation #12 was created through a tiny seed match
3. the live MM quoted the target contest
4. a controlled low-value taker match filled `0.037500 USDC` of maker risk
5. the live MM was stopped cleanly
6. final visible maker commitments were `0`
7. final target orderbook rows were `0`
8. telemetry errors were `0`
9. no write-like events were observed after the detected fill
10. final score was independently captured from MLB Stats API

## Controlled fills

Seed/setup fill:

- Commitment hash: `0x1a79ac4d2b28b49b9efba9df91c0c8eff0ac32faf0923aa2af4c0f72eca23b52`
- Fill tx: `0x793dd7f35538427fd0547ad0eeef5b2678914651be4fac4decc56a2f01cb9640`
- Maker: `ospex-stage-maker-b` / `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482`
- Taker: `ospex-flow-a` / `0x16dC5d67d080A5521ef2C79680DBFc2aBf724d30`
- Maker side: `upper` / away / Rangers
- Taker side: `lower` / home / Angels
- Maker risk: `0.020000 USDC`
- Taker risk: `0.020000 USDC`
- Odds tick: `200`

Controlled MM partial fill:

- Commitment hash: `0x05879daacb266b498028c511ba51b71644337081f9c32e84049f16328df2373d`
- Fill tx: `0x4a48490762ce8599beb23cfadbc69b6ca066202577c3ca3ef62a585648d26614`
- Maker: `ospex-stage-maker-a` / `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`
- Taker: `ospex-flow-a` / `0x16dC5d67d080A5521ef2C79680DBFc2aBf724d30`
- Maker side: `upper` / away / Rangers
- Taker side: `lower` / home / Angels
- Maker risk filled: `0.037500 USDC`
- Taker risk: `0.030000 USDC`
- Odds tick: `180`

Polygonscan:

- Contest create tx used for contest #21: https://polygonscan.com/tx/0x5b84bfa070bc801b2223d76fa9daa2aefd0f18c99f7f8622bd56132945529668
- Seed match/speculation create: https://polygonscan.com/tx/0x793dd7f35538427fd0547ad0eeef5b2678914651be4fac4decc56a2f01cb9640
- Controlled MM partial fill: https://polygonscan.com/tx/0x4a48490762ce8599beb23cfadbc69b6ca066202577c3ca3ef62a585648d26614

## MM exposure and telemetry

- Live MM run IDs: `2026-05-23T23-17-09-893Z-s0rjux, 2026-05-23T23-19-28-312Z-5lebzc`
- Live window: `2026-05-23T23:17:09.895Z` → `2026-05-23T23:22:36.311Z`
- Ticks: `9`
- Submit events: `2`
- Replace events: `2`
- Soft-cancel events: `2`
- On-chain cancel events: `0`
- Fill events: `1`
- Telemetry errors: `0`
- Final commitments list for the MM maker: `0` rows
- Final contest orderbook rows: `0`
- Live MM runner processes after wrap-up: `0`

## Why this is not green acceptance evidence

The intended retained-partial / `cancelMode:onchain` path was not actually exercised:

- `23:20:33.649Z` — `replace` created `0x05879daacb266b498028c511ba51b71644337081f9c32e84049f16328df2373d`
- `23:21:35.524Z` — `soft-cancel` on the same hash, reason `side-not-quoted`
- `23:22:06.132Z` — `fill` detected by `position-poll`, `newFillWei6=37500`
- `partial-remainder-retained`: `0`
- `onchain-cancel`: `0`

So the run is useful evidence for the race/API-local-bookkeeping mismatch, but it should not be promoted as clean D1/D2 acceptance evidence.

## Caveats / follow-up

- `commitments.show 0x05879daacb266b498028c511ba51b71644337081f9c32e84049f16328df2373d` reported `cancelled`, `filledRiskAmount=0`, `remainingRiskAmount=250000`, `isLive=false` even though the match tx confirmed and indexed positions/fills exist.
- The first controlled fill attempt raced a stale replacement and failed before a live fill.
- MM local status retained four `softCancelled` records after shutdown/expiry while public/API exposure was clean.
- Post-game score was observed externally, but protocol scoring/settlement/claiming was not performed in this artifact wrap-up.
- Private operator files, local run paths, RPC URLs, credential material, password files, keystore paths, raw signatures, and raw telemetry transcripts are intentionally excluded.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/indexer-snapshot.sanitized.json` — selected Supabase/API projection rows with signatures omitted
- `raw/tx-receipts.summary.json` — compact Polygon receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation
- `raw/mm-telemetry-summary.sanitized.json` — MM telemetry rollup without local paths/raw telemetry
- `raw/mm-final-status.sanitized.json` — MM final status rollup without local paths
- `raw/mm-controlled-partial-fill.sanitized.json` — selected CLI fill evidence with raw signature omitted
- `raw/mm-filled-commitment-final.sanitized.json` — final commitment read with raw signature omitted
- `raw/mm-maker-commitments-final.sanitized.json` — final MM commitments-list read
- `raw/investigation-report.sanitized.md` — compact investigation report with local paths redacted
