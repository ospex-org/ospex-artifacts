# Ospex Evidence Artifact: Dodgers @ Brewers Controlled Tiny Lifecycle

**Artifact ID:** `2026-05-22-mlb-lad-mil-contest-18-controlled-lifecycle`  
**Network:** Polygon mainnet  
**Contest:** `18`  
**Speculation:** `10`  
**Market:** MLB moneyline  
**Status:** complete / verified with caveats

## Result

Milwaukee Brewers defeated Los Angeles Dodgers, **5–1**.

Protocol semantics for this market:

- `upper` / `away` = Los Angeles Dodgers
- `lower` / `home` = Milwaukee Brewers
- winning side = `home` / `lower`

External score source:

- MLB Stats API: gamePk `823788`, status `Final`

## What this artifact proves

This run demonstrates a complete low-value Ospex v0.3.0 public-release lifecycle:

1. public v0.3.0 release tarballs installed in a clean Node 22 Docker harness
2. `ospex --version` returned `0.3.0`
3. release tarball hashes matched expected v0.3.0 hashes
4. npm audit signatures passed: 37 registry signatures and 16 attestations
5. no high/critical npm audit findings; moderate `ws` via `ethers` remains non-blocking
6. contest created and verified for Los Angeles Dodgers @ Milwaukee Brewers
7. one moneyline EIP-712 commitment submitted
8. one controlled low-value match/fill executed
9. positions were created for both wallets
10. contest was scored with the real final score
11. speculation was settled with `winSide=home`
12. winning position was claimed
13. final claim dry-runs were empty for both controlled wallets

## Controlled fill

- Commitment hash: `0xd97bc10a8dd2e4f04e226f4b2ad51881203e8b949ff8ca755a6d8da6a9d7df51`
- Fill tx: `0x86ed1b315de3ae764e75f4df987968336b149c4fcbec3b956031ac2c414edbdb`
- Maker: `ospex-stage-maker-b` / `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482`
- Taker: `ospex-stage-maker-a` / `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`
- Maker side: `upper` / away / Dodgers
- Taker side: `lower` / home / Brewers
- Maker risk: `0.25 USDC`
- Taker risk: `0.25 USDC`
- Odds tick: `200` (`+100` / decimal `2.00`)

Polygonscan:

- Contest create: https://polygonscan.com/tx/0x0e6fbc08883579f136cafed64ca22e03637c4bf8a12714bb5306d0f9c97ead92
- Fill: https://polygonscan.com/tx/0x86ed1b315de3ae764e75f4df987968336b149c4fcbec3b956031ac2c414edbdb
- Score request: https://polygonscan.com/tx/0x4190320ea7b3b0887a3b4a3f5e5bf0fa0805beefd5e4b83f1eb41266a8a2fd8c
- Settle: https://polygonscan.com/tx/0xbbb07d86b500ba5acc1dea492688cec99b3d091f4c240ebc5779bc03a0a40561
- Claim: https://polygonscan.com/tx/0x2977ba27898ec01070693452b3ef1a81ece2792e54c93172fe872e4d83442b5f

## Scoring, settlement, and claim

Score request:

- Tx: `0x4190320ea7b3b0887a3b4a3f5e5bf0fa0805beefd5e4b83f1eb41266a8a2fd8c`
- Block: `87294277`

Settlement:

- Tx: `0xbbb07d86b500ba5acc1dea492688cec99b3d091f4c240ebc5779bc03a0a40561`
- Block: `87294294`
- winSide: `home`

Winner claim:

- Wallet: `ospex-stage-maker-a` / `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`
- Side: `lower` / home / Brewers
- Tx: `0x2977ba27898ec01070693452b3ef1a81ece2792e54c93172fe872e4d83442b5f`
- Payout: `0.5 USDC`

## Position outcomes

- `ospex-stage-maker-b`: Dodgers/upper, risk `0.25 USDC`, lost, no claim expected
- `ospex-stage-maker-a`: Brewers/lower, risk `0.25 USDC`, claimed `0.5 USDC`, realized profit `0.25 USDC`

## Caveats / product debt observed

- Initial contest-create attempt with `ospex-stage-maker-a` returned `CHAIN_ERROR` before any tx hash. No contest was created. This matched low POL headroom and was resolved by swapping creation/maker duties to `ospex-stage-maker-b`; Vince later topped up `ospex-stage-maker-a` and doctor rechecked green.
- Immediately after claim, `positions status` briefly still showed the winning claimable entry while `claim-all --dry-run` was already empty. A refresh showed `claimableCount=0` and `positions list` showed speculation `10` `claimed=true`. This appears to be short API/indexer projection lag, not a claim failure.
- Private operator files, RPC URLs, wallet password files, raw signatures, and raw runtime transcripts are intentionally excluded.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/indexer-snapshot.sanitized.json` — selected CLI/API projection rows with signature omitted
- `raw/tx-receipts.summary.json` — compact Polygon receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation
