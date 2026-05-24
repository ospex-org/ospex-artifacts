# Ospex Evidence Artifact: Twins @ Red Sox MM early2 soft-cancel recovery lifecycle wrap

- **Artifact ID:** `2026-05-24-mlb-min-bos-contest-23-mm-early2-softcancel-recovery`
- **Network:** Polygon mainnet
- **Contest:** `23`
- **Speculation:** `14`
- **Market:** MLB moneyline
- **Status:** complete / verified with caveats

## Direct answer

This test is wrapped. The contest was scored from the external final, the speculation settled, winning positions were claimed, and final claim dry-runs plus position-status checks are empty for the controlled wallets.

## Result

Minnesota Twins @ Boston Red Sox finished **Minnesota Twins 6, Boston Red Sox 5**.

Protocol semantics for this market:

- `upper` / `away` = Minnesota Twins
- `lower` / `home` = Boston Red Sox
- winning side = `away/upper` / Minnesota Twins

External score source:

- MLB Stats API: gamePk `824759`, status `Final`

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

- Commitment hash: `0xe9b243ee5b3a333e76d67fcea76fc3fe7c44a7e26bf6bfe01fa0e051dcf8c0a3`
- Fill tx: `0xa8b4422a502e870a70ea7c371a8e05d197bb31162dc06aba77c65d43fda97202`

## Polygonscan

- Contest create: https://polygonscan.com/tx/0x5a7d5807ce2203c8bdc2a4285df144e640ea2dc76fd3465f1f589bc11bde2c94
- Seed match/speculation create: https://polygonscan.com/tx/0x9c3a79cc772835f7bc9b691f288b7e4c5ac9b56d253ac58d18951df086b77212
- Controlled MM fill: https://polygonscan.com/tx/0xa8b4422a502e870a70ea7c371a8e05d197bb31162dc06aba77c65d43fda97202
- Score request: https://polygonscan.com/tx/0x376e31715650fdb94b52f5f09884555e5518d6023155c6020b41b37bed61edd3
- Score callback / scores set: https://polygonscan.com/tx/0x2c4d7df6dacb8a0db74659c3aee3686a5bc53df8786c5631a846f88c14633dfa
- Settle: https://polygonscan.com/tx/0x197043a852f096519d56b2cc9e3b01cfdc04acb5a6a61f4303ec8892bb6b21d4
- Claim (ospex-fresh-user): https://polygonscan.com/tx/0xbedca3232659f2eed0e3a968f5c307698da82f06f068d65efa080c1450a9c2f9
- Claim (ospex-flow-a): https://polygonscan.com/tx/0x8d400ef611dacac5f141ce7f6b1f057dea4fd0f5fc09af4d6ba4e22eacb7ffad

## Scoring, settlement, and claims

Score:

- Score request tx: `0x376e31715650fdb94b52f5f09884555e5518d6023155c6020b41b37bed61edd3`
- Scores-set callback tx: `0x2c4d7df6dacb8a0db74659c3aee3686a5bc53df8786c5631a846f88c14633dfa`
- Protocol score: Minnesota Twins `6`, Boston Red Sox `5`

Settlement:

- Tx: `0x197043a852f096519d56b2cc9e3b01cfdc04acb5a6a61f4303ec8892bb6b21d4`
- winSide: `away` / `upper`

Winning position claims:

- `ospex-flow-a`: upper/away/Minnesota Twins, risk `0.019968 USDC`, claimed `0.051168 USDC`
- `ospex-fresh-user`: upper/away/Minnesota Twins, risk `0.020000 USDC`, claimed `0.040000 USDC`

Losing positions:

- `ospex-flow-a`: lower/home/Boston Red Sox, risk `0.020000 USDC`, lost/no claim expected
- `ospex-stage-maker-a`: lower/home/Boston Red Sox, risk `0.031200 USDC`, lost/no claim expected

## MM exposure and telemetry

- Live MM run IDs: `2026-05-24T16-45-39-251Z-tlpty8`, `2026-05-24T16-47-30-805Z-j4g818`
- Ticks: `2`
- Submit events: `2`
- Soft-cancel events: `2`
- Expire events: `0`
- On-chain cancel events: `0`
- Fill events: `2`
- Telemetry errors: `2`
- Final Supabase visible-live commitments: `0`
- Live MM runner processes after wrap-up: `0`

## Caveats / product or ops debt observed

- This is complete lifecycle evidence for early2 and does exercise soft-cancelled hidden-hash fill recovery, but it is not clean green D1/D2 on-chain-cancel acceptance evidence.
- The first early2 score attempt failed before sending a tx because the fresh-user contest creator had zero LINK allowance for OracleModule; approving 0.005 LINK and retrying scored cleanly.
- The MM telemetry included two position-poll PositionWithoutCommitment errors for an older speculation on the shared maker wallet; the target soft-cancel recovery fill still recorded via source=softcancel-recovery, and final protocol state is complete.
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
