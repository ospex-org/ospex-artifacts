# v0.9.0 latest-main moneyline+total MM canary — STL @ CHC contest 8

Verdict: **FULL_GREEN** (`complete_verified`)

This artifact records the 2026-07-03 Ospex R5/v0.9.0 latest-main market-maker canary for St. Louis Cardinals @ Chicago Cubs (`contestId 8`, moneyline `speculationId 13`, total `speculationId 14`). The primary artifact target is the live **total** fill; moneyline was included in setup and MM scope.

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — primary STL/CHC was official pre-game, exact identity matched, odds were available, and there was sufficient runway. |
| Repo/runtime gates | PASS — SDK/CLI v0.9.0 and MM head `4fcd489` with installed SDK v0.9.0; typecheck/test/build green. |
| Manual setup seed | PASS — one tiny moneyline seed and one tiny total seed were fully matched, leaving zero open seed commitments. |
| MM dry-run | PASS — `candidates --allowlist-only` returned contest 8 quote_ready for moneyline and total; dry run stayed allowlisted. |
| Live MM | PASS — strict allowlist `[8]`, markets moneyline+total, `seedSpeculations=false`, no broad slate, tiny risk. |
| Controlled fill | PASS — one live total quote filled, commitment `0x345624d363db80879bc97d9fa5224d061959d1a54f0fe31dd64e118ab8cd4e32`, tx `0x718427d62e75dc2ca08ce928da9f2a9c8f6f52214f7d33fadc631cb56456cb61`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — runner exited cleanly and no orphan process remained. |
| Zero visible-open exposure | PASS — final public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — St. Louis Cardinals 17, Chicago Cubs 1; contest scored, moneyline settled to away/upper/Cardinals, total settled to over/upper, winning positions claimed. |
| Artifact validation | PASS locally before PR/opening. |

## Target and total identity

| Field | Value |
|---|---|
| Game | St. Louis Cardinals @ Chicago Cubs |
| gamePk | `824659` |
| Contest / target speculation | `8` / `14` |
| Companion speculation | moneyline `13` |
| Target market | total |
| Total line | 10.5 |
| Upper / lower | upper = over 10.5; lower = under 10.5 |
| Reference total at market gate | over -120, under -100 |
| Final score | St. Louis Cardinals 17, Chicago Cubs 1 |
| Winning side | over / upper |

## Live fill

| Field | Value |
|---|---|
| Live maker | `ospex-stage-maker-b` / `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482` |
| Controlled taker | `ospex-flow-a` / `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30` |
| Commitment | `0x345624d363db80879bc97d9fa5224d061959d1a54f0fe31dd64e118ab8cd4e32` |
| Fill tx | `0x718427d62e75dc2ca08ce928da9f2a9c8f6f52214f7d33fadc631cb56456cb61` |
| Maker side | over / upper / over 10.5 |
| Taker side | under / lower / under 10.5 |
| Maker filled risk | 0.050000 USDC |
| Taker risk | 0.048500 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Contest create | `0xf1b722b316b95c6643279bb1db4a2c0d6778ad0187731d741ece7eca70d457c2` |
| Market update | `0x10d2bebab2f92ec7981c7a1f1dfe8129c4ba7babbb6af0ca384c29280fb00ff6` |
| Manual moneyline seed fill | `0x7ca3ad546038488d3f449f4f899a75baf28deabef878b566b8367f03a1191763` |
| Manual total seed fill | `0xb7ba5c920313587618129cc446ad079046709ece42dd054ba32008076728f5fa` |
| Controlled live total fill | `0x718427d62e75dc2ca08ce928da9f2a9c8f6f52214f7d33fadc631cb56456cb61` |
| Score contest 8 request | `0x1105af3deeb023ef55d91f51c0cf743343a70ad3eefa449e1f4a1eff396d6736` |
| CRE score callback | `0x6f3fe51e994b0ba2f09b868a57ab29668c5c7339ad42bc901c22be5d5c211200` |
| Settle moneyline speculation 13 | `0x1a86018d4c687446d7c3a836d330047b328da7cb9affd6a50c020f7e6094099f` |
| Settle total speculation 14 | `0xcb3685dc91be6f544cf5092b76fc2c6fc01d476b1cc1ae557cdd84bedfde8a11` |
| Claim seed maker moneyline winner | `0x00e20d725680e007f1f62a642e69be21aaa8cc188a47790e645e646cc3389749` |
| Claim controlled total seed-taker winner | `0x225880d81b73580f274a8a3c42881c85c2f75e408106c29b624959c32b846854` |
| Claim live MM total maker winner | `0x07313f36969138c15101d24cda6f48f6832c140b92398955e58a3701c6d22100` |

## Final exposure and claim state

- Public open commitments for contest 8: **0**
- Public open commitments for speculation 13: **0**
- Public open commitments for speculation 14: **0**
- Target active / pending-settle / claimable positions across the three controlled wallets: **0 / 0 / 0**
- Orphan live MM process: **none**
- Losing Cubs moneyline / under-total positions are not claimable and are no-op.

## Caveats

- The run was resumed after a machine/power outage; all postgame actions were gated on fresh official score, current contest/spec status, and target-scoped position/commitment reads.
- A transient live own-state advisory appeared before the canonical fill event; state converged and PR #145 orphan-safety regression evidence is included.
- The scheduled postgame cron was removed after manual completion to prevent duplicate score/settle/claim attempts.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
