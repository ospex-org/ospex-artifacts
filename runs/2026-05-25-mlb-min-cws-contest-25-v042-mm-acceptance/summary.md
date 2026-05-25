# Twins @ White Sox v0.4.2 MM acceptance lifecycle

Artifact ID: `2026-05-25-mlb-min-cws-contest-25-v042-mm-acceptance`
Status: `complete_verified_with_caveats`
Network: Polygon mainnet (`137`)
Contest/speculation: `25` / `16`
Market: MLB moneyline, Minnesota Twins @ Chicago White Sox
Captured: `2026-05-25T21:29:54Z`

## Verdict

GREEN with non-blocking caveats.

- Protocol safety: GREEN.
- Live MM phase: GREEN.
- Postgame score/settle/claim lifecycle: GREEN.
- Canonical run: `live2`; an earlier `live1` runner was setup/aborted and is not canonical.

## Final score and outcome

Official final source: MLB Stats API.

- Minnesota Twins: 1
- Chicago White Sox: 3
- Ospex outcome: home/lower wins.
- Contest `25`: `scored`, score `1-3`.
- Speculation `16`: `closed`, win side `home`.

## Live phase evidence

Live phase is GREEN for:

- v0.4.2 install/runtime path pinned to this run.
- Controlled target commitment submitted, partially filled, retained as a partial-remainder candidate, and then authoritatively cancelled on-chain.
- Same-side submit/replace count between target fill and target on-chain cancel: `0`.
- Final zero public exposure / zero orderbook.
- No background MM process.
- No MM telemetry errors.

Canonical Stage B:

- Maker: `ospex-stage-maker-b` / `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482`
- Taker: `ospex-flow-a` / `0x16Dc5D67D080a5521ef2c79680dBfC2aBf724D30`
- Filled hash: `0x150862b2b1f96e9b095b6d15712277c2c89628327175bf4d89a87b8800e966ad`
- Match tx: `0xe2d56b6e0a6b2281aced7fb317e10c63e0f17796186e25eb7add34874a15b2c3`
- On-chain cancel tx: `0x24028f2d43316556a5ed3a9c044ea4801f3baae94c53c5ec39069ea424cb62c2`

## Postgame transactions

- Score request tx: `0xda87981b680dc39e5c302ce05fa97cdccd094fcdc666ec1f5ccc5edbb1d554eb`
- Score callback tx: `0xdafa9d1be41c4163829619965b55e9c87a3feb1ad2691127cd3df0ffd01adc00`
- Settle speculation tx: `0x2ea8ff0acb44e6844a56204abcf5e687c595da16d2a492beff99f69261a31833`
- Claim `ospex-flow-a`: `0xfd50a9166287cac6d9ad6c1de4adb252440050f944b79d65b74bc3f66d19e8c6`

Final claim dry-runs for `ospex-stage-maker-a`, `ospex-stage-maker-b`, and `ospex-flow-a` returned zero entries. The final orderbook was empty.

## Caveats

- Non-blocking setup caveat: `live1` was setup/aborted; `live2` is canonical.
- Operator-methodology caveat: small controlled live mainnet positions and pre-funded operator wallets were used.
- Scheduling caveat: manual postgame verification completed after final score, ahead of the previously scheduled cron follow-up.

## Raw evidence

- `raw/final-score-source.json`
- `raw/final-supabase-state.sanitized.json`
- `raw/tx-receipts.summary.json`
- `raw/cli-postgame.sanitized.json`
- `raw/final-contest-show.sanitized.json`
- `raw/mm-final-status.sanitized.json`
- `raw/mm-telemetry-summary.sanitized.json`
- `raw/live-phase.sanitized.json`
- `raw/process-check.sanitized.txt`
