# v0.9 latest all-market MM canary — MIA @ ATH contest 9

Verdict: **V090_LATEST_MM_ALL_MARKETS_SINGLE_GAME_GREEN** (`complete_verified_with_caveats`)

This artifact records the first latest-main v0.9 strict-allowlist single-game market-maker canary that covered all three Ospex MLB markets: moneyline, spread, and total. The market maker posted tiny live quotes across all three markets for contest `9`, and one controlled live total quote was filled.

## Scope

- One MLB contest, strict contest allowlist `[9]`.
- Markets: moneyline `15`, spread `16`, total `17`.
- Tiny controlled capital only; budget/risk gate stayed under the requested cap.
- Bounded approvals only; no unlimited approvals.
- R5/CRE path only; no old Functions/LINK flow.
- `seedSpeculations=false` during MM runtime; speculations were manually seeded/filled before the live MM run.

## Target and identity

| Field | Value |
|---|---|
| Game | Miami Marlins @ Athletics |
| gamePk | `824982` |
| Game ID | `7ecd358d-14b6-420a-8155-df9a92b67ef3` |
| Contest | `9` |
| Start time | `2026-07-04T01:40:00Z` |
| Final score | Miami Marlins 12, Athletics 5 |
| Moneyline upper/lower | upper = away = Miami Marlins; lower = home = Athletics |
| Moneyline reference odds | Miami Marlins +125; Athletics -138 |
| Spread line | Miami Marlins +1.5 / Athletics -1.5 |
| Total line | 10.5 |
| Final winners | Miami Marlins / away / upper; Miami Marlins +1.5 / upper; over 10.5 / upper |

## Version gates

| Gate | Result |
|---|---|
| SDK/CLI version | PASS — v0.9.0 at `fd55bd1e7de0` |
| Market-maker repo | PASS — `4fcd489ef1ee` with installed `@ospex/sdk` 0.9.0 |
| MM typecheck/test/build | PASS — 1061 tests passed |
| core-api / indexer / CRE | PASS — `076f44d428fc` / `75be9e76965b` / `fed6e26e27e5` |

## Lifecycle result

| Gate | Result |
|---|---|
| Target selection | PASS — primary target upcoming, identity exact, odds available, and setup runway sufficient. |
| Contest create | PASS — contest `9` created on Polygon mainnet. |
| CRE verification | PASS — contest `9` verified through R5 CRE. |
| Market update | PASS — moneyline, spread, and total odds visible. |
| Manual seed/fill | PASS — speculations `15`, `16`, and `17` manually created/filled; open commitments returned to `0`. |
| Candidates allowlist | PASS — `quote_ready=3` scoped only to contest `9`. |
| Dry-run loop | PASS — would-submit across moneyline/spread/total, no broad-slate or seed behavior. |
| Live MM | PASS — 6 tiny quotes posted across all three markets under allowlist `[9]`. |
| Controlled live fill | PASS — one non-moneyline total quote filled. |
| Shutdown | PASS — 5 remaining visible quotes soft-cancelled/expired; open commitments `0`; no orphan process. |
| Restart/cold-start | PASS — dry-run cold-start probe rehydrated cleanly with no duplicate exposure. |
| CRE score | PASS — official final score was scored through R5/CRE on the first request. |
| Settlement | PASS — moneyline, spread, and total speculations settled. |
| Claims | PASS — winning controlled positions claimed. |
| Final zero-state | PASS — target maker/taker active/pending/claimable positions all `0`; open commitments `0`. |

## Live MM evidence

| Market | Spec | Live quote hashes |
|---|---:|---|
| moneyline | `15` | `0x61ad59245c7d8bfafd433e4a0b4edb573f5649cbb67f5c37a674568e77c8bafc`, `0x2d8bdfee288eeeacdeeea3b2196ea257ab767783fae1ab7d2581a8870d9e6010` |
| spread | `16` | `0x9009206b921b6b7c58416b513127e5b2c9e5e25d8ec4afe82977c0ea54dd42de`, `0xd61a25f88c197f99d6992a10f8e1aff005298dc1bfdb38d933bb4047c2498945` |
| total | `17` | `0x8a2edae969fde29ae73bc7f3d063c320bc7ee631e63cd638aacfc9d01404b18c`, `0xdf1762d2ce6a5f0e3b46cc677500a90bef79d131b361c10cc302b9c3535cfcce` |

Controlled fill: total quote `0xdf1762d2ce6a5f0e3b46cc677500a90bef79d131b361c10cc302b9c3535cfcce`, taker side Under 10.5, tx `0xe6b352524b30556331054006bcba741574520ea8f4b50d5124ad76e9f1f882c8`.

## Transactions

| Step | Tx |
|---|---|
| Contest create | `0xc8aec13c184cda258124ff05cfd7e0c95034daa635ab8a1438ab7d0ae057871e` |
| Market update | `0xd0137e5409943beaa074d6630404acc0bc937f005b7c35db54d41babbffb5695` |
| Moneyline seed match | `0xb1b1eeea9a05ec33822b1c48a27e30566adb8c559d7b661086b86487e39daffb` |
| Spread seed match | `0x0827410b27c5409bf914a9620548270a85eb310fb565b9ab32ad2a349f3acbac` |
| Total seed match | `0xfeb2d5789e831820bd8fda64948b0677d8f1663aaf9b08f42b4b4ff59d043c64` |
| Live total fill | `0xe6b352524b30556331054006bcba741574520ea8f4b50d5124ad76e9f1f882c8` |
| Score request | `0xdab2872fc1534d4ff67bbec6f7597ea41620522e0ebc4aaf127d005b590b6fc5` |
| Settle moneyline `15` | `0x381464bf7c5b9ee712a4d9c65e16835232731741e537b601064e1699d6d1601d` |
| Settle spread `16` | `0x8e659384c56701b5236c497f4d0269743c3c9ee379df2c95d907a0318f5e47de` |
| Settle total `17` | `0x7d052bf4455f7245f5cc606082ad7e2227016d00318c822b1567ee2880e2f6d0` |

## Final state

- Contest `9`: `scored`, Miami Marlins 12, Athletics 5.
- Speculation `15`: closed, winSide `away`.
- Speculation `16`: closed, winSide `away`.
- Speculation `17`: closed, winSide `over`.
- Open commitments: contest `0`; by spec orderbook counts `{"15": 0, "16": 0, "17": 0}`.
- Target positions:
  - `ospex-stage-maker-a`: active `0`, pendingSettle `0`, claimable `0`.
  - `ospex-flow-a`: active `0`, pendingSettle `0`, claimable `0`.
  - `ospex-stage-maker-b`: active `0`, pendingSettle `0`, claimable `0`.

## Caveats

1. Exactly one controlled live fill was executed. It was a non-moneyline total quote, which satisfies the acceptable gate because all three markets posted and all-market dry-run evidence was clean.
2. An initial controlled live fill attempt used the wrong inherited signer environment and failed before any transaction; the retried `ospex-flow-a` fill succeeded.
3. The live runner briefly entered a zero-exposure own-state health hold at boot and cleared it before posting quotes.

## Evidence files

Canonical facts are in `evidence.json`. Sanitized raw evidence is under `raw/`, including `raw/mm-dryrun-summary.sanitized.json`, `raw/live-public-commitments-posted.sanitized.json`, `raw/live-fill.sanitized.json`, `raw/postgame-lifecycle.sanitized.json`, and `raw/zero-exposure.sanitized.json`.
