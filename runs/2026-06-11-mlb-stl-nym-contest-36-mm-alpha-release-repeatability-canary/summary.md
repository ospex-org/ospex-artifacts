# STL-NYM contest 36 MM alpha release repeatability canary — FULL GREEN / complete_verified_with_caveats

**Status:** `complete_verified_with_caveats` / **FULL GREEN with caveats**.
Captured: `2026-06-11T20:55:48Z`.

## Verdict

The tagged `ospex-market-maker` `v0.1.0-alpha.1` release repeated the canary lifecycle through live window and postgame on a freshly prepared MLB target. Contest `36` / speculation `26` was created and opened for St. Louis Cardinals @ New York Mets. The release-tag MM dry-run quote path worked, live mode posted only two tiny short-expiry commitments on the intended moneyline target, one controlled partial fill succeeded, telemetry recorded the canonical fill source as `own-state-stream`, no canonical legacy fill source was observed, and public/API commitment exposure drained to zero after shutdown, expiry grace, and restart/cold-start probe.

Postgame continuation completed after MLB Stats API reported Final: New York Mets `5`, St. Louis Cardinals `4`. Contest `36` was scored, speculation `26` settled to home/lower, the controlled taker claimed the winning position, and final `claim-all --dry-run` checks for setup, maker, and flow wallets were empty.

## Target and wallets

- Game: St. Louis Cardinals @ New York Mets
- MLB gamePk: `823619`
- Final score: St. Louis Cardinals `4`, New York Mets `5` (MLB Stats API Final)
- Contest/speculation: `36` / `26`; market: moneyline
- Start: `2026-06-11T17:10:00Z` UTC / `2026-06-11 12:10 CDT`
- Target setup/scoring wallet: ospex-stage-maker-a `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`
- Live MM maker wallet: ospex-stage-maker-b `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482`
- Controlled taker wallet: ospex-flow-a `0x16Dc5D67D080a5521ef2c79680dBfC2aBf724D30`

## Runtime alignment

- MM repo/tag/head: `ospex-org/ospex-market-maker` `v0.1.0-alpha.1` / `af1bb107af47dc80f27485dee7417ca95b782b50`
- SDK dependency observed: `@ospex/sdk v0.6.2`
- Node/Yarn: `v22.22.0` / `1.22.22`
- Release gates: install, build, smoke, typecheck, lint, and test all exited `0`.

## Live-window evidence

- Live commitments posted: `2` tiny commitments, each `0.100000 USDC` risk, both expiring `2026-06-11T15:54:13Z`.
- Filled commitment: `0xf2b961cc392b26dbf725247ad85e53de51438eb137b1b4dbbb2c1d942111bcdc`.
- Fill tx: `0x1b60890d18e1afba6433c47ebceeb93dac108bfddaac5cb6871b638565065eae`, confirmed.
- Controlled fill size: taker risk `0.049950 USDC`; maker filled risk `0.037000 USDC`; partial fill.
- Own-state SSE evidence: one `fill` event, source `own-state-stream`; legacy canonical fill source list empty; stream-health hold entered and cleared automatically in live mode.
- Partial-fill safety: telemetry recorded `partial-remainder-retained` and no same-side replacement while the partial remainder was retained; public/API exposure reached zero after expiry.
- Public/API exposure after shutdown+expiry+restart and postgame: contest/spec visible commitments `0`, maker visible commitments `0`, contest orderbook `0`, MM status visible-open commitments `0`.
- Orphan process scan: `0`.

## Setup / seed / live txs

- Setup Treasury approval 1 USDC: `0xf799f0cb58765d7bad0d7cd359351fac71b0b82ed631899b7663d3ebd2e655c7`
- Contest create: `0xc43ecd8ab00283d998ce3821631e6829771f47c5141949bf2c32745b3988df0e`
- Setup seed/open approval 0.25 USDC: `0x4a3e15e739542822fb4dc60ee13bf79e64e88c4819e287111a7900b09a334a89`
- Flow seed/open approval 0.25 USDC: `0x8f3ecc073b00d0773949c3968716b8b80b07bae49ce977514b526f9cbd29edf9`
- Seed commitment: `0x0c320d55b5e67b0658ed68806b7697c404a77a26e03b258fac8fc645668dc354`
- Seed match/open speculation: `0x5190f1261623f6a9315e3de1796fe27e0bfe401f05993f7f8864b34769e55203`
- Controlled live fill: `0x1b60890d18e1afba6433c47ebceeb93dac108bfddaac5cb6871b638565065eae`

## Postgame txs

- Score contest `36`: `0xb2dde952cc0223e5b2826ef0016ce1658b3ab0f87d40933820d6f3110c6f8173`
- Settle speculation `26`: `0x0894efa5130d64d9138f6f5ae16cf8327ed218ef19a133bd2a0aa99832c94048`
- Claim winning flow position: `0xb8f86df71715b3dc3639ce6c4aedc42bd93e31fdcf5f3f1f2b9f1c6aa574513c`
- Claimed payout: `200450` wei6 / `0.200450 USDC`
- Final `claim-all --dry-run` entries: setup `0`, maker `0`, flow `0`.

## Budget / cost

- Live-window operator gas: `0.731891998164896975 POL`.
- Postgame operator gas: `0.263374338176443792 POL`.
- Total operator gas observed: `0.995266336341340767 POL` (≈ `0.24881658408533519175 USDC` at the run's reporting price `0.25 USDC/POL`).
- New controlled live risk: `0.049950 USDC` taker / `0.037000 USDC` maker filled.
- Postgame controlled taker claim returned `0.200450 USDC`.
- Within the `≤5.00 USDC` controlled tiny-risk/spend cap.

## Caveats

- Initial contest create attempt intentionally stopped on insufficient bounded allowance before any write; bounded approval/retry succeeded.
- Restart probe is read-only/dry-run with fresh state and expected timeout, not a process-level persisted cursor resume proof.
- Postgame was completed by the continuation job rather than restarting the frozen live MM runtime; local maker-state remains private and is not published.
- Coverage is one target/one maker/one controlled taker; not broad MVE/fishbowl coverage.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
