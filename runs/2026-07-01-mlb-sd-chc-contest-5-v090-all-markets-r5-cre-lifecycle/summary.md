# R5 CRE v0.9.0 all-market lifecycle — SD @ CHC contest 5

Verdict: **V090 all-markets lifecycle GREEN with caveats** (`complete_verified_with_caveats`)

This artifact records the first Ospex R5/CRE v0.9.0 all-market manual SDK/CLI lifecycle proof for contest `5`, San Diego Padres @ Chicago Cubs. It covers moneyline, spread, and total markets with tiny controlled positions, then postgame score → settle → claim convergence.

## Scope

- Manual SDK/CLI controlled lifecycle, not a market-maker autonomous loop.
- One MLB contest, three speculations: moneyline `7`, spread `8`, total `9`.
- Tiny controlled capital only.
- Bounded approvals only; no unlimited approvals.
- R5/CRE path only; no old Functions/LINK flow.

## Target and identity

| Field | Value |
|---|---|
| Game | San Diego Padres @ Chicago Cubs |
| gamePk | `824660` |
| Contest | `5` |
| Start time | `2026-07-01T18:20:00Z` |
| Final score | San Diego Padres 3, Chicago Cubs 23 |
| Moneyline upper/lower | upper = away = San Diego Padres; lower = home = Chicago Cubs |
| Moneyline reference odds | San Diego Padres +106; Chicago Cubs -120 |
| Moneyline favorite / underdog | Chicago Cubs favorite; San Diego Padres underdog |
| Final winner | Chicago Cubs / home / lower |

## Version gates

| Gate | Result |
|---|---|
| SDK/CLI version | PASS — v0.9.0 at `fd55bd1e7de0` |
| Market-maker repo | PASS — `e89eecbd4b53` with installed `@ospex/sdk` 0.9.0 |
| MM typecheck/test/build | PASS |
| core-api / indexer / CRE | PASS — `076f44d428fc` / `75be9e76965b` / `fed6e26e27e5` |

## Lifecycle result

| Gate | Result |
|---|---|
| Target selection | PASS — selected later preferred target with upcoming status, odds, `canCreateContest=true`, and sufficient lead time. |
| Contest create | PASS — contest `5` created on Polygon mainnet. |
| CRE verification | PASS — contest `5` verified through R5 CRE. |
| Market update | PASS — moneyline, spread, and total odds visible. |
| Moneyline fill | PASS — speculation `7` created/fill matched. |
| Spread fill | PASS — speculation `8` created/fill matched with explicit side/line identity. |
| Total fill | PASS — speculation `9` created/fill matched with explicit over/under/push semantics. |
| Pregame exposure drain | PASS — open commitments for contest/specs were `0`. |
| CRE score | PASS with caveat — first confirmed score request did not callback before bounded retry; second request scored the contest. |
| Settlement | PASS — speculations `7`, `8`, and `9` settled. |
| Claims | PASS — controlled winning positions claimed. |
| Final zero-state | PASS — contest-5 active/pending/claimable positions all `0` for maker, taker, and operator; open commitments `0`. |

## Live all-market fills

| Market | Spec | Maker side | Taker side | Maker risk | Taker risk | Match tx |
|---|---:|---|---|---:|---:|---|
| moneyline | `7` | San Diego Padres away/upper `+106` | Chicago Cubs home/lower | 0.100000 | 0.106000 | `0x22f4170ff96dce03d50bdd73767c7dc2abcc033f7179b0d1a6052fbba80549d6` |
| spread | `8` | Chicago Cubs home/lower `-1.5` at `+151` | San Diego Padres away/upper `+1.5` | 0.100000 | 0.151000 | `0x934a46c7f8665a36f8a751f830e18a48d07dea09a40c13e5162bc5d0ed34992e` |
| total | `9` | Over `12.0` upper at `-110` | Under `12.0` lower | 0.100000 | 0.091000 | `0xe412f37fdf0e59ac10586cfad94e061525c9179ac64080a51f666a86f049dedb` |

Spread semantics: Chicago Cubs `-1.5` wins if Chicago wins by 2 or more; San Diego `+1.5` wins if San Diego wins or loses by 1. Chicago won by 20, so the Chicago/lower side won.

Total semantics: 13+ total runs wins over/upper; exactly 12 pushes; 11 or fewer wins under/lower. The final total was 26, so over/upper won.

## Transactions

| Step | Tx |
|---|---|
| Contest create | `0xa27b5b55c6790ac621819adb15b29378b1efc062b6c4875a353e3d4ebc9e780c` |
| Market update | `0x8239cc86e5f37c74c55c58b7663045f54e241db28b1ab4a8468fa6b761ced19a` |
| Moneyline match | `0x22f4170ff96dce03d50bdd73767c7dc2abcc033f7179b0d1a6052fbba80549d6` |
| Spread match | `0x934a46c7f8665a36f8a751f830e18a48d07dea09a40c13e5162bc5d0ed34992e` |
| Total match | `0xe412f37fdf0e59ac10586cfad94e061525c9179ac64080a51f666a86f049dedb` |
| Score attempt 1 | `0xfcf9d669a02073ff03a0f399f93b5cbe846e9c5e3e5a8acd9ab20325f9e00d43` |
| Score retry 2 | `0xc7a4167c72ce8bffe9a035b51b04afa97d4f756855637dbb9327435dbc101d7a` |
| Settle moneyline `7` | `0x60d476c048b80dbd8124f5dd82fafbf25c6d8806eadbbeaa2707778a246eaa6c` |
| Settle spread `8` | `0x4c3cbbe58e75d5660d813c6af93a4946b00b9b27f3706725bddf84854273acde` |
| Settle total `9` | `0x2ba826a74f71cf57c1237bf624212d1fcd18b3b60b9d534dd74a901e147c269c` |
| Claim moneyline lower/home winner | `0xd19a2d99ddf5b38f81680a13f2e04b143ba66d14df8f1775aebe226cfa657e32` |
| Claim spread lower/home winner | `0xc91b1787da42101959e285359924c2f3fb2f5ec9d5699cad0e676dc72b31b8c2` |
| Claim total upper/over winner | `0x964abd8c1fa06f103cab250260feb122a8c5f3767973e8bc7bd1a20e81fba1d6` |

## Final state

- Contest `5`: `scored`, San Diego Padres 3, Chicago Cubs 23.
- Speculation `7`: closed, winSide `home`.
- Speculation `8`: closed, winSide `home`.
- Speculation `9`: closed, winSide `over`.
- Open commitments: contest `0`; by spec `{"7": 0, "8": 0, "9": 0}`.
- Contest-5 positions:
  - `ospex-stage-maker-a`: active `0`, pendingSettle `0`, claimable `0`.
  - `ospex-flow-a`: active `0`, pendingSettle `0`, claimable `0`.
  - `ospex-stage-maker-b`: active `0`, pendingSettle `0`, claimable `0`.

## Caveats

1. The first confirmed score-request transaction did not produce a callback before a bounded retry. The second request produced the scored projection and all postgame state converged.
2. An initial maker approval transaction timed out while waiting for receipt and was not found by receipt/allowance checks. A bounded retry succeeded before live fills.
3. Global wallet position reads included earlier same-day contests; all final assertions here are filtered to contest `5`.

## Evidence files

Canonical facts are in `evidence.json`. Sanitized raw evidence is under `raw/`, including:

- `raw/version_gate.json`
- `raw/target_preflight.json`
- `raw/wallet_preflight_and_approvals_summary.json`
- `raw/contest_create_5.json`
- `raw/market_update_5.json`
- `raw/odds_snapshot_5.json`
- `raw/live_all_markets_summary.json`
- `raw/final_pregame_state.json`
- `raw/postgame_lifecycle_summary.json`
- `raw/final_score_source.json`
- `raw/final_contest_5_show.json`
- `raw/final_speculation_7_show.json`
- `raw/final_speculation_8_show.json`
- `raw/final_speculation_9_show.json`
- `raw/current_positions_status_ospex-stage-maker-a.json`
- `raw/current_positions_status_ospex-flow-a.json`
- `raw/current_positions_status_ospex-stage-maker-b.json`
- `raw/tx_receipts_summary.json`
