# NYY-TOR contest 41 MM live canary — FULL GREEN / complete_verified_with_caveats

**Status:** `complete_verified_with_caveats` / **FULL GREEN with caveats**.  
Captured: `2026-06-13T04:45:19Z`.

## Verdict

NYY @ TOR contest `41` / speculation `30` completed the Phase 2 live MM canary lifecycle. The market-maker live run was allowlisted to the single moneyline target, posted exactly two tiny short-expiry commitments, executed exactly one controlled partial fill, captured the fill through `own-state-stream`, shut down cleanly, and drained public/API-visible quote exposure to zero.

Postgame completion then verified the MLB Stats API Final score — New York Yankees `5`, Toronto Blue Jays `8` — scored contest `41`, settled speculation `30` to Toronto/home/lower, claimed the two winning lower/Toronto positions, and verified final target claim sweeps and public commitment exposure at zero.

## Target and wallets

- Game: New York Yankees @ Toronto Blue Jays
- MLB gamePk: `822803`
- Final score: Yankees `5`, Blue Jays `8` (MLB Stats API Final)
- Contest/speculation: `41` / `30`; market: moneyline
- Team identity: Toronto was home/lower/favorite (`-112`, tick `189`) and won; Yankees were away/upper/underdog (`+112`, tick `212`) and lost.
- Official start: `2026-06-12T23:37:00Z` UTC / `2026-06-12 18:37 CDT`
- Score/settle operator: ospex-fresh-user `0x4ddfeEB90B53f7616135ce9D2B8f317af3c4066D`
- Live MM maker: ospex-stage-maker-b `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482`
- Controlled taker/setup wallet: ospex-flow-a `0x16Dc5D67D080a5521ef2c79680dBfC2aBf724D30`

## Runtime alignment

- MM repo/head/describe: `ospex-org/ospex-market-maker` / `9fd1465306d061391520552be68b17e0616ca76f` / `v0.1.0-alpha.1-3-g9fd1465`
- MM package: `0.1.0-alpha.1`
- SDK dependency and CLI: `@ospex/sdk v0.6.2` / CLI `0.6.2`
- Node/Yarn: `v22.22.0` / `1.22.22`
- `yarn build` exited `0` during manual postgame wrap.

## Live-window evidence

- Commitments posted: `2`, each `0.100000 USDC` risk, both expiring around `2026-06-12T23:03:08Z`.
- Filled commitment: `0xd9ad9e548213ba45cf240a6266052afa0e746fd35751b71a814c48fe195c55d1`.
- Unfilled opposite-side commitment: `0x2190854b5d29e185cf6e01335f7246046e71322f43fb86dcf9091e11c47ca9c0`, soft-cancelled/not visible.
- Controlled fill tx: `0x985408301fd5a40ec1978d4779e13fe869cbdf0852702df063bcd7db93e2cc32`, status `0x1`.
- Fill size: taker risk `0.049929 USDC`; maker filled risk `0.056100 USDC`.
- Own-state evidence: one fill event with source `own-state-stream`; post-fill same-side submit/replace count `0`; write-like count `0`.

## Setup / seed / live txs

- Setup seed commitment: `0xfd30e3dd661623440619ce872aee602f6993b9935846e5a270e9c37a47a66a0c`
- Setup seed/open tx: `0xbd91c6180b1a7c8e00d72143f69de481174f77dde471563d8e638aa758352830`
- Controlled live fill: `0x985408301fd5a40ec1978d4779e13fe869cbdf0852702df063bcd7db93e2cc32`

## Postgame txs

- Score contest `41`: `0x26859a2f82309817c5fd89181ece0a63b83aae29b1611d472dfeaa58c159c6c3`
- Settle speculation `30`: `0x6e883a25524e64e17d5abe117cf4ce21ad41d3c2919874ed4bced8ddf5d26db2`
- Claim maker live lower/Toronto position: `0xb5e41d48d00919690da8f5d6a7667d2d847b599601ce7deea47ed56675fe8b7b`; payout `0.106029 USDC`
- Claim flow setup lower/Toronto position: `0xc4d0371ceef99da65e3f6a0dc9e477c343b9e2a4ac4b9e5e2947e340e1249501`; payout `0.095500 USDC`
- Flow setup upper/Yankees position lost and was not claimable.

## Final zero exposure

- Public contest/spec visible commitments: `0`
- Maker visible commitments: `0`
- Indexer visible live commitment count: `0`
- Target active positions: maker `0`, flow `0`
- Target claimable positions after claims: maker `0`, flow `0`
- Target pending-settle positions: maker `0`, flow `0`
- Orphan MM process scan: `0`
- Final claim-all dry-run entries: maker `0`, flow `0`

## Budget / cost

- Live match gas: `0.10037259073362879 POL`
- Postgame gas: `0.301188498318548031 POL`
- Total tracked match+score+settle+claim gas: `0.401561089052176821 POL`
- LINK movement: score/settle operator `-0.005`; maker/flow `0`
- Controlled live risk: taker `0.049929 USDC`; maker `0.056100 USDC`
- Claimed payouts: maker `0.106029 USDC`; flow `0.095500 USDC`

## Caveats

- This is the NYY/TOR salvage lifecycle only. The missed MIA/PIT primary remains skipped/preserved evidence, not a public failure artifact.
- Final CLI `speculations show` omitted win-side/settledAt fields after settlement; indexer/protocol position rows showed spec `30` closed with `win_side=home` and `settled_at=2026-06-13T04:30:45Z`, and claim/no-op checks converged.
- Flow wallet has unrelated active positions outside contest/spec `41/30`; target-scoped active/claimable/pending-settle counts are zero.
- No restart/cold-start probe was performed for the salvage; final zero-exposure and process checks were performed instead.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- MVE scorecard: `mve-scorecard.md`, `mve-scorecard.json`
- Sanitized raw evidence: `raw/`
