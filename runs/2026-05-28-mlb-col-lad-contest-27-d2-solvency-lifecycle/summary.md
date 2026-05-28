# Rockies @ Dodgers D2 solvency/script-hash lifecycle smoke

Artifact ID: `2026-05-28-mlb-col-lad-contest-27-d2-solvency-lifecycle`
Status: `complete_verified_with_caveats`
Network: Polygon mainnet (`137`)
Contest/speculation: `27` / `17`
Market: MLB moneyline, Colorado Rockies @ Los Angeles Dodgers
Captured: `2026-05-28T06:08:32Z`

## Verdict

GREEN with non-blocking caveats.

- Protocol safety: GREEN.
- Refreshed script-hash gate: GREEN.
- D2 solvency/fillability smoke: GREEN.
- Postgame score/settle/claim lifecycle: GREEN.

## Final score and outcome

Official final source: MLB Stats API.

- Colorado Rockies: 1
- Los Angeles Dodgers: 4
- Ospex outcome: home/lower wins.
- Contest `27`: `scored`, score `1-4`.
- Speculation `17`: `closed`, win side `home`.

## Smoke phase evidence

The live smoke proved:

- Refreshed verify script hash matched before live writes: `0xec6a7e9cdffa09fdcaa611220e2c99ba0ec58cc082812a01b5d321ccc1e5ebcf`.
- Contest `27` was created and verified.
- Tiny fundable quote was submitted: `0x4ba7598c03eae419a2340dbd28ba1dcc8c19f5bd8bb9d1721d3a272e4957326f`.
- Oversized submit was refused before signing/posting with `MAKER_USDC_BALANCE_INSUFFICIENT, MAKER_POSITION_ALLOWANCE_INSUFFICIENT`.
- Controlled taker matched the quote: `0x4114152ac6a6461e7fa062ee034044d9d7a2ff01e2b9105f40459154a67a5c6e`.
- Final target commitment state: `filled`, remaining risk `0`, maker list count `0`.

## Postgame transactions

- Initial score request tx: `0xa9c384af8e30f761fa1f7b19518ecb9d042becd3d749575474fd58fc4ecc74e5`
- Initial score callback tx: `0xdec4c728679c7cfb47734a597a3fb58426762ddfd5e58ea71a0071ddde257949` — callback failed with an oracle upstream API error; no scores set.
- Retry score request tx: `0x84635509dd5c9de596084556e8943ad55b99cbfa7435c3816c0a1a9f626ecbe4`
- Retry score callback tx: `0x69daa6cf031d98a7d611684e763ae7ca2930bff0caf421d6b2119b1334e1932d` — scores set to `1-4`.
- Settle speculation tx: `0x1dbce640272789833d16d48efb139185b4a26a0a4d336eac941fad0001e9ab7d`
- Claim `ospex-stage-maker-a`: `0x9c5382f5430d05e3d5dc6e298f1a0b2d1a8f6eac19781c73000cc339f1d80a60`
- Claimed payout: `191000 wei6` = `0.191000 USDC`.

Final claim dry-runs for `ospex-stage-maker-a` and `ospex-flow-a` returned zero entries. The final orderbook/visible maker list was empty.

## Caveats

- SDK/CLI observability: bundled CLI `contests create` emitted generic `CHAIN_ERROR` with no tx/effects twice; direct SDK create with the same signer/env succeeded after nonce/game-state checks.
- Oracle-upstream transient: first score callback failed; one retry scored correctly and the lifecycle completed.
- SDK/CLI JSON UX: match envelope retained the pre-approval taker fillability verdict even though the command remediated allowance and matched successfully.
- Operator-methodology caveat: small controlled live mainnet positions and pre-funded operator wallets were used.

## Raw evidence

- `raw/final-score-source.json`
- `raw/final-supabase-state.sanitized.json`
- `raw/tx-receipts.summary.json`
- `raw/cli-postgame.sanitized.json`
- `raw/final-contest-show.sanitized.json`
- `raw/oracle-score-callbacks.sanitized.json`
- `raw/smoke-phase.sanitized.json`
- `raw/process-check.sanitized.txt`
