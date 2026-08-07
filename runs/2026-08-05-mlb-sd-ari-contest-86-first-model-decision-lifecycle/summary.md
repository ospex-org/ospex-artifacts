# August 5 SD@ARI contest 86 — first model-decision lifecycle

- **Status:** `complete_verified_with_caveats`
- **Network:** Polygon mainnet (`chainId=137`)
- **Lifecycle:** model decision → on-chain position → exact final score → settlement → winning claim → terminal zero

A source-pinned `openai-gpt-5.6-sol` moneyline decision selected **San Diego Padres** at `2026-08-05T05:34:15.743Z`. The controlled taker matched `0.999925 USDC` against `0.869500 USDC` of Arizona market-maker risk in speculation `234`.

The official final was **San Diego 4, Arizona 10**. The on-chain score matched exactly, speculation `234` settled to **home / Arizona**, and the market-maker's winning position claimed **1.869425 USDC**. The model position settled as a loser with zero payout.

## Proof transactions

| Action | Transaction | Block |
|---|---|---:|
| Match model decision | [`0xbe9236c17953d7c83822d188d9fde69fea9bcbe8889fd42214e5b8878c7c0cea`](https://polygonscan.com/tx/0xbe9236c17953d7c83822d188d9fde69fea9bcbe8889fd42214e5b8878c7c0cea) | `91473035` |
| Request score | [`0x54e98d703c6a1cea7145ded4ec079a2824fb68018594b1372cdcc98b90596d1d`](https://polygonscan.com/tx/0x54e98d703c6a1cea7145ded4ec079a2824fb68018594b1372cdcc98b90596d1d) | `91524975` |
| CRE score callback | [`0x057d4bca7bbec41d6c985f13f0273e34113d5d76b8cb00dd49590803ee400bbd`](https://polygonscan.com/tx/0x057d4bca7bbec41d6c985f13f0273e34113d5d76b8cb00dd49590803ee400bbd) | `91524990` |
| Settle speculation 234 | [`0x91165c580288161a8a8bc904e0a8b6dcbfc12f81a0f1f466a214da30fc24df6f`](https://polygonscan.com/tx/0x91165c580288161a8a8bc904e0a8b6dcbfc12f81a0f1f466a214da30fc24df6f) | `91525043` |
| Claim winning position | [`0xd3645d12745b87be67e8057c566c4de4dd44eabe7017eb232c984d51173105c9`](https://polygonscan.com/tx/0xd3645d12745b87be67e8057c566c4de4dd44eabe7017eb232c984d51173105c9) | `91525087` |

Fresh receipt readback found all **11/11** published lifecycle proof transactions successful at their source-recorded blocks.

## Terminal state

At `2026-08-06T05:06:51.000Z`:

- open commitments: **0**
- active positions: **0**
- pending-settlement positions: **0**
- claimable positions: **0**
- nonzero scoped allowances across three wallets: **0 / 6**
- writer processes: **0**

## Caveats

This was a bounded smoke/shakedown, not a canonical benchmark cohort. The model record had `wouldAbstain=true` but was explicitly selected for lifecycle execution. San Diego lost, so the claimed winner was the Arizona counterparty position. A separately selected total decision did not fill after a funding-guard bulk-nonce invalidation and is not represented as a successful position. No closing-odds or CLV artifact was captured.

Machine-readable source of truth: [`evidence.json`](evidence.json).
