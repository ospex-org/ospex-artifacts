# Ospex Evidence Artifact: Pirates @ Blue Jays MM early1 lifecycle wrap

- **Artifact ID:** `2026-05-24-mlb-pit-tor-contest-22-mm-early1`
- **Network:** Polygon mainnet
- **Contest:** `22`
- **Speculation:** `13`
- **Market:** MLB moneyline
- **Status:** complete / verified with caveats

## Direct answer

This test is wrapped. The contest was scored from the external final, the speculation settled, winning positions were claimed, and final claim dry-runs plus position-status checks are empty for the controlled wallets.

## Result

Pittsburgh Pirates @ Toronto Blue Jays finished **Pittsburgh Pirates 4, Toronto Blue Jays 1**.

Protocol semantics for this market:

- `upper` / `away` = Pittsburgh Pirates
- `lower` / `home` = Toronto Blue Jays
- winning side = `away/upper` / Pittsburgh Pirates

External score source:

- MLB Stats API: gamePk `822813`, status `Final`

## What this artifact proves

- contestCreated: `True`
- contestVerified: `True`
- mmQuotedLive: `True`
- controlledFillExecuted: `True`
- postgameScore: `True`
- speculationSettled: `True`
- winningPositionsClaimed: `True`
- finalClaimDryRunsEmpty: `True`
- finalPositionActivePendingClaimableCountsZero: `True`
- visibleLiveCommitmentsFinal: `0`
- mmRunnerProcessesAfterWrapup: `0`

## Controlled fills

Seed and MM fills are recorded in `evidence.json` and the sanitized final projection snapshot. Main MM controlled fill:

- Commitment hash: `0x59a0d50b0269b296c00c0603248a47f09930ecabb9820d6873e121e572f7f5a9`
- Fill tx: `0x02e30de29d26630328c0fd150b2f25a1e17c6f3ac63f0adbad8521cce56193a0`

## Polygonscan

- Contest create: https://polygonscan.com/tx/0x8f9fa4c09661e73d3a194fe2efa3a6440068caa55a6f5df996cbcb9be0e78a56
- Seed match/speculation create: https://polygonscan.com/tx/0x2638c739f6dfb95171dfc7c8f60fd9c65e0a68ea4755c46c496c96d097225c6c
- Controlled MM fill: https://polygonscan.com/tx/0x02e30de29d26630328c0fd150b2f25a1e17c6f3ac63f0adbad8521cce56193a0
- Score request: https://polygonscan.com/tx/0xe951a85c1376b96d439cb73977a7f36dc86cd9a0c545660bdf1b16a2ef0bd6c6
- Score callback / scores set: https://polygonscan.com/tx/0x63c5e996018464177e8dbbd4181835bc3da0347750f0f1365805517243ba0350
- Settle: https://polygonscan.com/tx/0xf28473e07826e8137114fcba6c4a0c664d074e351e431d22d01ed0b47837991a
- Claim (ospex-stage-maker-a): https://polygonscan.com/tx/0x752c85420d49b1840868b77393be3cdae72da5b9fdae65e2d886bbf39f24b191
- Claim (ospex-stage-maker-b): https://polygonscan.com/tx/0xa4b2168898c7e09beec9dd5fa4ed1d0dc1a64c7d0a8390f77312bbc3a5f90464

## Scoring, settlement, and claims

Score:

- Score request tx: `0xe951a85c1376b96d439cb73977a7f36dc86cd9a0c545660bdf1b16a2ef0bd6c6`
- Scores-set callback tx: `0x63c5e996018464177e8dbbd4181835bc3da0347750f0f1365805517243ba0350`
- Protocol score: Pittsburgh Pirates `4`, Toronto Blue Jays `1`

Settlement:

- Tx: `0xf28473e07826e8137114fcba6c4a0c664d074e351e431d22d01ed0b47837991a`
- winSide: `away` / `upper`

Winning position claims:

- `ospex-stage-maker-b`: upper/away/Pittsburgh Pirates, risk `0.020000 USDC`, claimed `0.040000 USDC`
- `ospex-stage-maker-a`: upper/away/Pittsburgh Pirates, risk `0.018600 USDC`, claimed `0.048546 USDC`

Losing positions:

- `ospex-flow-a`: lower/home/Toronto Blue Jays, risk `0.049946 USDC`, lost/no claim expected

## MM exposure and telemetry

- Live MM run IDs: `2026-05-24T15-50-47-649Z-gkkwe4`
- Ticks: `6`
- Submit events: `4`
- Soft-cancel events: `3`
- Expire events: `2`
- On-chain cancel events: `0`
- Fill events: `1`
- Telemetry errors: `0`
- Final Supabase visible-live commitments: `0`
- Live MM runner processes after wrap-up: `0`
- Retained-partial metric note: `partialRemainderRetainedTelemetryCount: 0` is the retained-partial/on-chain-cancel acceptance-event count. `raw/mm-final-status.sanitized.json` also has `candidates.skipReasons.partial-remainder-retained: 1`, which is a separate quote-candidate skip reason.

## Caveats / product or ops debt observed

- This is complete lifecycle evidence for early1, but it is not clean green D1/D2 on-chain-cancel acceptance evidence: on-chain cancel and retained-partial acceptance telemetry counts were zero. The separate `partial-remainder-retained: 1` in final-status candidate skip reasons is a routine quoting metric, not a retained-partial acceptance/on-chain-cancel telemetry event.
- The MM recorded the controlled fill, then the filled commitment expired; final public/API exposure was zero, while local status retained expired/soft-cancelled nonterminal bookkeeping rows.
- Projection lag after the first settlement caused one duplicate-settle estimateGas failure for the second winner; retry after convergence succeeded and final dry-runs were empty.
- The games projection still reported status upcoming at capture even though contest/speculation protocol state and MLB Stats API were final/scored/settled.
- The public artifact intentionally excludes raw signatures, private operator material, credential material, keystore paths, local run paths, raw provider IDs, and raw telemetry transcripts.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/final-supabase-state.sanitized.json` — final selected projection rows with signatures/source-provider IDs omitted
- `raw/tx-receipts.summary.json` — public receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation
- `raw/mm-telemetry-summary.sanitized.json` — MM telemetry rollup without local paths/raw telemetry
- `raw/mm-final-status.sanitized.json` — MM final status rollup without local paths
- `raw/cli-postgame.sanitized.json` — postgame command rollup
