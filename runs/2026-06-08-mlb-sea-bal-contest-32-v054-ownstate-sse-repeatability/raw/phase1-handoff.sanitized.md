# Sanitized Phase 1 handoff

Verdict: **GREEN-candidate with caveats for Phase 2 wrap-up**.

No public/matchable quote exposure remained after Phase 1: visible maker commitments were `0`, the contest/speculation orderbook was `[]`, and process rechecks found `0` live market-maker processes. Filled economic positions remain active for postgame lifecycle handling; these are expected and are not public/orderbook quotes.

## Target

- Slug: `sea-bal-2026-06-08`
- Game: Seattle Mariners @ Baltimore Orioles
- Start: `2026-06-08T22:35:00Z` / `2026-06-08 17:35 CDT`
- Contest id: `32`
- Speculation id: `22`
- Market: moneyline (`upper=away`, `lower=home`)

## Wallet roles

- Creator / maker: stage-maker-a — `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Controlled taker / flow: ospex-flow-a — `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

## Main writes / hashes

- Treasury allowance `0 -> 0.35 USDC`: `0xe90f7342e1908941842e5c3ccd1e7098c915ce53cd77abc8e661dbdd641b3c00`
- Treasury allowance `0.35 -> 1.0 USDC`: `0x2cc6805df0f43fef0dd4101f0f3739af440ad9c66a28adcf2e1c4eee98aa8b54`
- Lazy moneyline/speculation maker-fee allowance `0.25 USDC`: `0xd00edddcdceccab974457b76e1dc1e91fc5011760e0d60abde93d948d53d1dfa`
- Contest create tx: `0x28fab025e65d00ce3f23055efcc2cae266fa9f0790702abcf993f141db3d2640`
- Seed commitment hash: `0x60515a8bf862119d9cdb2f01b17ac0d5d250d6d551b3a2c50f712fc2dfcebcb0`
- Seed/open-speculation tx: `0x0f1b38bf8a176f75830c7a929a24019767679eea27ccf1896e89b2803e30badf`
- Main filled MM quote hash: `0x2e62e694ba0856203cbc0716c9343e084003065ac1db9c69e9891cc34fef4f9d`
- Controlled fill tx: `0x1590ec5398b6ef103fba850ae492bd5c5b8e21a4e4b21d88f670eb553ce8bded`
- Retained partial on-chain cancel tx: `0xb051cfcd450f9b4e0007d265627f80c8a1771faa4981af3737e5dde1fcf27ddd`
- Opposite-side quote on-chain cancel tx: `0x9d0c376e24d594ba6d713d514e61c9d0c8ca8dcdd9ece4df383ebf014db38a4e`

## Own-state SSE / restart-resume

- Initial bounded config with `maxOpenCommitments: 2` self-limited before the controlled taker saw a candidate. The successful run used bounded `maxOpenCommitments: 4`.
- Restart/resume reused the same state directory privately; local path not published.
- `stream-cold-restart` observed.
- `stream-health-hold` entered with setup exposure and later cleared.
- Controlled fill ingestion for the main quote occurred exactly once; final `eventCounts.fill = 1`.

## Budget

- Confirmed write receipts parsed: `8 / 8`
- Total gas: `0.77985881746265763 POL`
- Estimated USDC movement/lock: `1.778760 USDC`, under the `5.00 USDC` cap
- LINK: not measured in Phase 1

## Caveats

- Initial `maxOpenCommitments: 2` self-limited; successful run used bounded `4`.
- One near-expiry match attempt returned rc `1` with timeout/no receipt and did not land.
- One transient `OwnerPositionStatusForUnknownPosition` occurred before fill materialization; fill accounting then occurred exactly once.
- Filled positions remain active until postgame.
