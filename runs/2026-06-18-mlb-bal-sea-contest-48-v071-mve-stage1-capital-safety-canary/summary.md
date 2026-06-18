# v0.7.1 Stage-1 capital-safety canary — BAL @ SEA contest 48

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-06-18 v0.7.1 Ospex market-maker Stage-1 MVE capital-safety canary for Baltimore Orioles @ Seattle Mariners (`contestId 48`, `speculationId 37`). BAL/SEA was the only live target. LAA/ATH was prepared as a backup and was not live-run; its lifecycle is outside this BAL/SEA artifact.

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — BAL/SEA was official pre-game, exact identity matched, and quote dry-run returned `computed` / `canQuote=true`. |
| Live MM | PASS — exactly one live MM process, strict allowlist `[48]`, Stage-1 risk caps. |
| Controlled fill | PASS — one fill, commitment `0x5ec9a0733f95d1edd6dcb269db4c70763864fb424e11bb4603a2d9c1996a5da2`, tx `0x8fbb99158ded6fd3938f5c2a9a01dce3d39bea4e9cf85f061cf51b5933643015`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — graceful KILL, process exit 0, no orphan live MM process. |
| Zero visible-open exposure | PASS — public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — BAL 0, SEA 3; contest scored, speculation settled to home/lower/Seattle, winning positions claimed. |
| Artifact validation | PASS locally before PR. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Baltimore Orioles @ Seattle Mariners |
| gamePk | `823125` |
| Contest / speculation | `48` / `37` |
| Market | moneyline |
| Upper / lower | upper = away = Baltimore; lower = home = Seattle |
| Reference odds at setup | Baltimore +124, Seattle -140 |
| Favorite / underdog at setup | Seattle favorite, Baltimore underdog |
| Final score | Baltimore 0, Seattle 3 |
| Winning side | home / lower / Seattle Mariners |

## Live fill

| Field | Value |
|---|---|
| Live maker | `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2` |
| Controlled taker | `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494` |
| Commitment | `0x5ec9a0733f95d1edd6dcb269db4c70763864fb424e11bb4603a2d9c1996a5da2` |
| Fill tx | `0x8fbb99158ded6fd3938f5c2a9a01dce3d39bea4e9cf85f061cf51b5933643015` |
| Maker side | upper / away / Baltimore Orioles |
| Taker side | lower / home / Seattle Mariners |
| Maker filled risk | 2.000000 USDC |
| Taker risk | 2.640000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Score contest 48 request | `0x8888e83a2170f3c0be45e0939b2a7a3aac800202700a864b549b8f3062b440c5` |
| Score contest 48 callback | `0xbebf7b7521a9016eee20b8b727c70a13ef0eb071d8115c310c3198601a3faca8` |
| Settle speculation 37 | `0x6fa6b3bc2f69443ef861b49a48de93f8c9126477e973e805ab714679a18402ba` |
| Claim controlled live taker winner | `0xb50646b16a2c1405df722e327028d6dd84277ec24a0eb5ce694fd3e78a1bebe6` |
| Claim setup seed taker winner | `0xbe937782bf650354ad93e07b180aae20ad0bc04ee70b1298425ac04f2e07f7e4` |

## Final exposure and claim state

- Public open commitments for contest 48: **0**
- Maker-filtered visible/open commitments: **0**
- Contest orderbook entries: **0**
- Final claim dry-runs for setup/live maker/taker wallets: **0 entries**
- Orphan live MM process: **none**
- Losing upper/Baltimore positions are not claimable and are no-op.

## Caveats

- LAA/ATH was prepared as a backup but not live-run; it is not part of this BAL/SEA lifecycle artifact.
- A separate restart/cold-start probe was not run; final zero-exposure and process checks were run instead.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
