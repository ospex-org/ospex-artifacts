# Ospex Phase 3 owner-state SSE live acceptance / short soak — MIL-COL contest 29

## Verdict

**AMBER** — core owner-state SSE live path was proven on Polygon mainnet and the postgame lifecycle is now complete, but the original soak remains abbreviated rather than the preferred 60–90 minute run. Partial-fill retained-remainder behavior, authoritative on-chain cancel, active on-chain cancel-sweep, and manufactured stream-fault coverage remain unproven in this artifact.

## Target

- Game: Milwaukee Brewers @ Colorado Rockies
- Slug: `mil-col-2026-06-07-0110`
- External gamePk: `824351`
- Contest ID: `29`
- Speculation ID: `19` (moneyline)
- Match time: `2026-06-07T01:10:00+00:00`

## Wallet roles

- Contest creator / seed maker / scoring signer / settle signer: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Moneyline seed taker: ospex-fresh-user `0x4ddfeEB90B53f7616135ce9D2B8f317af3c4066D`
- Live market-maker / winning controlled-fill maker: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled fill taker: ospex-flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

No private keys, passphrases, RPC URLs, raw signatures, or raw signed payloads are included in this artifact.

## What was live-proven

- SDK/CLI release alignment to `v0.5.4`; MM pin to `ospex-sdk-0.5.4.tgz` during the live soak.
- Contest creation from the approved same-evening MIL-COL game.
- Moneyline speculation seed via controlled lazy first match.
- `ownState.subscribe:true` live MM runtime using stage-maker-b.
- Stream-auth/own-state SSE connection: own-state subscriber count rose to 1 during the MM run and returned to 0 after shutdown.
- Live MM posted commitments for contest 29/speculation 19.
- Controlled taker filled one MM commitment on chain.
- MM telemetry recorded exactly one fill event for the filled commitment with `source=own-state-stream`.
- Restart/resume loaded the same state dir, entered a stream-health hold on cold restart, cleared it, and refused blank-slate reposting while exposure/no-headroom was present.
- Final cleanup after live run: no MM process remains, public visible open/partial commitments for stage-maker-b on contest 29 are 0.

## Postgame continuation

Completed at `2026-06-07T06:14:09Z` UTC (`2026-06-07T01:14:09-05:00` America/Chicago).

- Independent final-score sources: MLB Stats API `gamePk=824351` and ESPN game summary both show **Milwaukee Brewers 7, Colorado Rockies 1 — Final**.
- Protocol moneyline semantics: `upper = away`, so Milwaukee/away upper positions won.
- Contest 29 scored on-chain and indexed as `scored` with `awayScore=7`, `homeScore=1`.
- Speculation 19 settled/closed with `win_side=away`.
- Winning upper positions claimed:
  - stage-maker-a: `200000` wei6 = `0.200000` USDC.
  - stage-maker-b: `141000` wei6 = `0.141000` USDC.
- Final dry-run claim sweeps for stage-maker-a, stage-maker-b, ospex-flow-a, and ospex-fresh-user all returned zero entries.

## Caveats

- Soak duration was short (~3.5 minutes across live + restart) rather than 60–90 minutes / through first pitch.
- The controlled MM fill was full, not partial; retained-partial behavior was not live-proven.
- MM ran with `orders.cancelMode: offchain`; authoritative on-chain cancel was not exercised.
- A natural stream-health hold was observed during restart, but no production outage/fault injection was performed and no on-chain active cancel-sweep was exercised.
- Local SDK/CLI used for postgame continuation built from the available local checkout and reported `0.5.3`; the live soak/release evidence remains pinned to SDK/CLI `v0.5.4`.

## Key txs

See `raw/tx-receipt-summaries.sanitized.json` and `raw/postgame-tx-receipts.sanitized.json` for gas/block summaries.

- Contest creation: `0x51d1647723f2d31b63edb35e0d583265659fc548b60e71265d6f202dd55453ef`
- Moneyline seed match/spec creation: `0x92eaa54eaba733f426570f3ba91eb8c163a2bdab832d1378bd3fb2d37cc007fe`
- Controlled MM fill: `0xb3f7501681352c18c5dc41b11138028e20b666e40b3750f76f40687d9de443c7`
- Postgame score contest 29: `0x42288378b6daf4f7555530c423d80c53bac22b286e4e7ea9d88baffc8a469111`
- Postgame settle speculation 19: `0x65c76f323a304cc39da83e69ba69fe585e047716b510a523ef79fdf09260d1c7`
- Postgame claim stage-maker-a: `0xa61ae88c1f5df026b5606139d515d90af715c2b62dc053f3e6041b2901d2d6e4`
- Postgame claim stage-maker-b: `0x61d306a6c6b1daa7ae94c8d163f29053f674a971eed266af1a3d50a4a5ab4d76`

## Final exposure / lifecycle state

- MM processes: 0.
- Public `commitments list --contest-id 29` rows: 0.
- Public `commitments list --speculation 19` rows: 0.
- `contests show 29` orderbook rows: 0.
- Contest: scored, MIL 7 / COL 1.
- Speculation 19: closed/settled, win side away/upper.
- Winning upper positions: both claimed; loser lower positions remain unclaimed as expected.
- Final claim sweeps: empty for all four controlled wallets.

## Recommended next step

Keep this artifact **AMBER**. The postgame lifecycle row is now proven with caveats, but the next acceptance target remains a longer one-contest owner-state SSE soak with partial-fill and authoritative/on-chain cancel coverage before broader MVE ramp.
