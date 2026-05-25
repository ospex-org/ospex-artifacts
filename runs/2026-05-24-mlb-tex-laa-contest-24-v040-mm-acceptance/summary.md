# Rangers @ Angels v0.4.0 MM acceptance lifecycle

Artifact ID: `2026-05-24-mlb-tex-laa-contest-24-v040-mm-acceptance`  
Status: `complete_verified_with_caveats`  
Network: Polygon mainnet (`137`)  
Contest/speculation: `24` / `15`  
Market: MLB moneyline, Texas Rangers @ Los Angeles Angels  
Captured: `2026-05-25T04:26:48Z`

## Verdict

GREEN with non-blocking caveats.

- Protocol safety: GREEN.
- Live MM phase: GREEN.
- Postgame score/settle/claim lifecycle: GREEN.
- Coverage caveat: AMBER, coverage-only. This run proves soft-cancelled signed-payload recovery plus authoritative on-chain cancellation after a recovered partial fill. It does not directly prove the alternate `visibleOpen -> observed partial -> retained partial -> routine onchain-cancel` path.

## Final score and outcome

Official final source: MLB Stats API.

- Texas Rangers: 1
- Los Angeles Angels: 2
- Ospex outcome: home/lower wins.
- Contest `24`: `scored`, score `1-2`.
- Speculation `15`: `closed`, win side `home`.

## Live phase evidence

Live phase is GREEN for:

- v0.4.0 install/runtime path.
- Expiry release grace.
- Soft-cancelled signed-payload recovery.
- Authoritative on-chain cancel after recovered partial.
- Final zero public exposure / zero orderbook.
- No background MM process.
- No MM errors.

Clean Stage B source:

- Maker: `ospex-fresh-user` / `0x4ddfeEB90B53f7616135ce9D2B8f317af3c4066D`
- Taker: `ospex-flow-a` / `0x16Dc5D67D080a5521ef2c79680dBfC2aBf724D30`
- Filled hash: `0x73144e58ba4e650eb0ed07f127a2095d83780800169a2098001c41570b000805`
- Match tx: `0x50fb9c70cc4c0964c35ed32e45cb2b8255a43ed7ae7b58649d117a3a62ebea34`
- On-chain cancel tx: `0x9ee5b426c90f692fd598ed2f6f31d255b96ecd218fbd59a9e942f8da9586e729`

## Postgame transactions

- Score request tx: `0x7e49dc73cf23ff25145608e823c277363fdf48e697620a5d8df0e152201e226b`
- Score callback tx: `0xd3697df1fd0ecdc823bfa7cc1ef44f4c9e7181c3e99faf375014ec6386ce0ee1`
- Settle speculation tx: `0x8e70cd5a28861707320ab9a997fd1f2a317aa9ee02402a652a0c77069acfec73`
- Claim `ospex-stage-maker-a`: `0x731fac3c73b5d34f02b15f730f9ed0d7f62ac79ae6a9f31c702561d4c98123d7`
- Claim `ospex-flow-a`: `0x32463e0b4af4843f0717d12b39da57f5ed3af60c0aadc975d3a890cbc45572bc`
- Claim `ospex-fresh-user`: `0x2a62cb9393e95b3a872ee1fc98272bbfb04afe4fa9cabe3ce47281b4b0114d83`

Final claim dry-runs for `ospex-stage-maker-a`, `ospex-stage-maker-b`, `ospex-flow-a`, and `ospex-fresh-user` returned zero entries. The final orderbook was empty.

## Caveats

- Coverage amber only: alternate direct partial-retention/routine-cancel path was not directly proven.
- Operator-methodology noise: stage-maker-a/b had shared-wallet prior active positions on speculation `15`; clean Stage B evidence is `ospex-fresh-user`.
- Projection lag: immediately after settlement, two live claim attempts still planned settlement and failed pre-send; after projection convergence, both claims succeeded.
- Game row projection lag: `games.status` remained `upcoming`; contest/speculation state and official final score were correct.

## Raw evidence

- `raw/final-score-source.json`
- `raw/final-supabase-state.sanitized.json`
- `raw/tx-receipts.summary.json`
- `raw/cli-postgame.sanitized.json`
- `raw/final-contest-show.sanitized.json`
- `raw/mm-final-status.sanitized.json`
- `raw/mm-telemetry-summary.sanitized.json`
- `raw/live-phase.sanitized.json`
