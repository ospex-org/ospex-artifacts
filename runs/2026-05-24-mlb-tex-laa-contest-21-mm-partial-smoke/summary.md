# Ospex Evidence Artifact: Rangers @ Angels MM Partial-Fill Investigation + Lifecycle Wrap

- **Artifact ID:** `2026-05-24-mlb-tex-laa-contest-21-mm-partial-smoke`
- **Network:** Polygon mainnet
- **Contest:** `21`
- **Speculation:** `12`
- **Market:** MLB moneyline
- **Status:** complete / verified with caveats; not green D1/D2 acceptance evidence

## Direct answer

Yes — the live MM smoke ran, and the post-game wrap has now also been completed.

This artifact now records both the original partial-fill investigation and the completed post-game lifecycle: score request, scores-set callback, speculation settlement, winner claim, and final zero-entry dry-runs.

## Result

Texas Rangers @ Los Angeles Angels finished **Angels 5, Rangers 2**.

Protocol semantics for this market:

- `upper` / `away` = Texas Rangers
- `lower` / `home` = Los Angeles Angels
- winning side = `home` / `lower`

External score source:

- MLB Stats API: gamePk `824030`, status `Final`

## What this artifact proves

This run demonstrates a complete low-value Ospex lifecycle with a known MM investigation caveat:

1. contest #21 was created and verified for Texas Rangers @ Los Angeles Angels
2. moneyline speculation #12 was created through a tiny seed match
3. live MM quoted the target contest
4. a controlled low-value taker match filled `0.037500 USDC` of maker risk
5. final MM/API/orderbook exposure was clean after shutdown/expiry
6. contest was scored with the real final score, Rangers `2`, Angels `5`
7. speculation #12 was settled with `winSide=home`
8. the winning Angels/lower position was claimed by `ospex-flow-a`
9. final claim dry-runs were empty for the winner and both losing test wallets
10. final positions status showed zero active/pending/claimable rows for all three relevant wallets
11. the D1/D2 retained-partial / `cancelMode:onchain` proof remains inconclusive and should not be treated as green acceptance

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
- Score request: https://polygonscan.com/tx/0xb97616642ba440c51e8faa8e7d5d399aa7a03ff10e046a25c3f3c73ab3332943
- Score callback / scores set: https://polygonscan.com/tx/0xd89768c82a530adb0a60355f27398d01b75de01d25d814ef561bce0f7525ec28
- Settle: https://polygonscan.com/tx/0x943438400ee24fbb3c06d35ed7326ceb9d9ca4964e560ff5c4f6175831205c68
- Winner claim: https://polygonscan.com/tx/0x9499f7233bb568635b86e0afdffe21393aa1abbc4b6af763238d89a2ce4374f6

## Scoring, settlement, and claims

Score:

- Score request tx: `0xb97616642ba440c51e8faa8e7d5d399aa7a03ff10e046a25c3f3c73ab3332943`
- Scores-set callback tx: `0xd89768c82a530adb0a60355f27398d01b75de01d25d814ef561bce0f7525ec28`
- Protocol score: Rangers `2`, Angels `5`

Settlement:

- Tx: `0x943438400ee24fbb3c06d35ed7326ceb9d9ca4964e560ff5c4f6175831205c68`
- winSide: `home`

Winner claim:

- `ospex-flow-a`: Angels/lower, claimed `0.107500 USDC`, tx `0x9499f7233bb568635b86e0afdffe21393aa1abbc4b6af763238d89a2ce4374f6`

Position outcomes:

- `ospex-flow-a`: Angels/lower, risk `0.050000 USDC`, claimed `0.107500 USDC`, gross realized profit `0.057500 USDC`
- `ospex-stage-maker-b`: Rangers/upper, risk `0.020000 USDC`, lost, no claim expected
- `ospex-stage-maker-a`: Rangers/upper, risk `0.037500 USDC`, lost, no claim expected

## MM exposure and telemetry

- Live MM run IDs: `2026-05-23T23-17-09-893Z-s0rjux`, `2026-05-23T23-19-28-312Z-5lebzc`
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
- Final Supabase visible-live commitments for contest #21: `0`
- Live MM runner processes after wrap-up: `0`

## Caveats / product or ops debt observed

- Not green D1/D2 acceptance: the intended retained-partial / `cancelMode:onchain` path was not exercised.
- The filled hash had already been soft-cancelled before position polling observed the fill.
- `commitments.show 0x05879d...373d` reported `cancelled`, `filledRiskAmount=0`, `remainingRiskAmount=250000`, `isLive=false` despite the confirmed match tx and indexed positions/fills.
- The first controlled fill attempt raced a stale replacement and failed before a live fill.
- MM local status retained four `softCancelled` records after shutdown/expiry while public/API exposure was clean.
- Score projection had one observed stale read before the scores-set callback converged.
- Private operator files, local run paths, RPC URLs, credential material, password files, keystore paths, raw signatures, and raw telemetry transcripts are intentionally excluded.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/final-supabase-state.sanitized.json` — final selected Supabase/API projection rows with signatures omitted
- `raw/postgame-tx-receipts.summary.json` — score/settle/claim receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation
- `raw/mm-telemetry-summary.sanitized.json` — MM telemetry rollup without local paths/raw telemetry
- `raw/mm-final-status.sanitized.json` — MM final status rollup without local paths
- `raw/score-contest.sanitized.json` — score request CLI evidence
- `raw/settle-speculation.sanitized.json` — settle CLI evidence
- `raw/claimall-flow-a.sanitized.json` — winner claim CLI evidence
- `raw/final-claimall-flow-a-dry-run.sanitized.json` — final winner dry-run evidence
- `raw/final-claimall-stage-maker-a-dry-run.sanitized.json` — final losing MM maker dry-run evidence
- `raw/final-claimall-stage-maker-b-dry-run.sanitized.json` — final losing seed maker dry-run evidence
