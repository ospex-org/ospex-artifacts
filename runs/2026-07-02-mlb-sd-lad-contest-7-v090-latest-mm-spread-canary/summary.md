# v0.9.0 latest-main moneyline+spread MM canary — SD @ LAD contest 7

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-07-02 Ospex R5/v0.9.0 latest-main market-maker canary for San Diego Padres @ Los Angeles Dodgers (`contestId 7`, moneyline `speculationId 11`, spread `speculationId 12`). The primary artifact target is the live **spread** fill; moneyline was included in setup and MM scope.

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — primary SD/LAD was official pre-game, exact identity matched, odds were available, and there was sufficient runway. |
| Repo/runtime gates | PASS — SDK/CLI v0.9.0 and MM head `4fcd489` with installed SDK v0.9.0; typecheck/test/build green. |
| Manual setup seed | PASS — one tiny moneyline seed and one tiny spread seed were fully matched, leaving zero open seed commitments. |
| MM dry-run | PASS — `candidates --allowlist-only` returned contest 7 quote_ready for moneyline and spread; dry run stayed allowlisted. |
| Live MM | PASS — strict allowlist `[7]`, markets moneyline+spread, `seedSpeculations=false`, no broad slate, tiny risk. |
| Controlled fill | PASS — one live spread quote filled, commitment `0xe09448186d54586f1aaaacb8b9673771f7d383e0270efc8bd9a0af74fe64eff7`, tx `0x35765b4df1c1ddbaf9af79bcf4be349a01540a582f5637f5c7aca9a07fcb88ad`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — runner exited cleanly and no orphan process remained. |
| Zero visible-open exposure | PASS — final public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — Los Angeles Dodgers 12, San Diego Padres 7; contest scored, moneyline and spread settled to home/lower/Dodgers, winning positions claimed. |
| Artifact validation | PASS locally before PR/opening. |

## Target and team identity

| Field | Value |
|---|---|
| Game | San Diego Padres @ Los Angeles Dodgers |
| gamePk | `823935` |
| Contest / target speculation | `7` / `12` |
| Companion speculation | moneyline `11` |
| Target market | spread |
| Upper / lower | upper = away = San Diego Padres +1.5; lower = home = Los Angeles Dodgers -1.5 |
| Reference spread at live gate | San Diego Padres +1.5 (-125), Los Angeles Dodgers -1.5 (+105) |
| Final score | San Diego Padres 7, Los Angeles Dodgers 12 |
| Winning side | home / lower / Los Angeles Dodgers -1.5 |

## Live fill

| Field | Value |
|---|---|
| Live maker | `ospex-stage-maker-b` / `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482` |
| Controlled taker | `ospex-flow-a` / `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30` |
| Commitment | `0xe09448186d54586f1aaaacb8b9673771f7d383e0270efc8bd9a0af74fe64eff7` |
| Fill tx | `0x35765b4df1c1ddbaf9af79bcf4be349a01540a582f5637f5c7aca9a07fcb88ad` |
| Maker side | away / upper / San Diego Padres +1.5 |
| Taker side | home / lower / Los Angeles Dodgers -1.5 |
| Maker filled risk | 0.050000 USDC |
| Taker risk | 0.045000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Contest create | `0xb4769985b401180b43028e4a112ffa26acf7966be28aef61eb0e5e03e96829a1` |
| Market update | `0xe7dcde97bd0ff8a2b6bc0199b972b6d410d5dace4e828e535333bd2007958da0` |
| Manual moneyline seed fill | `0x1211ae528d566d1a3f98456bcea4a09ccecfed07e9f6eef028c1a3345c691490` |
| Manual spread seed fill | `0x88a8dfbc83cf0eca953adcc3e818666da595ad049ad4128f04d8b04def545c02` |
| Controlled live spread fill | `0x35765b4df1c1ddbaf9af79bcf4be349a01540a582f5637f5c7aca9a07fcb88ad` |
| Score contest 7 request | `0x8fc5217bd6d8d5ee3d2add6eddcaa2de61c69dc7608d2d4fc380222967567dfc` |
| CRE score callback | `0x777950c2fd4502472da0eb8b4f39e86d87b60dd86b75ca018bb32bd586a27bc8` |
| Settle moneyline speculation 11 | `0x6cdd7310ddc7c42f9605e826e78d62a82aa8b770cd87ca98a93fe2caa930438a` |
| Settle spread speculation 12 | `0x0316aabf6e6ec89fcb81859a586e65ec3ae21f6ca3a9eafedb1ed28840ffc671` |
| Claim seed maker moneyline winner | `0x8ba7fa93ab37d0898769fc1193b7a2630ffdb2aa627fe17d131be2a1bd30c7b9` |
| Claim controlled spread taker winner | `0x5a29f4ad7eb6a1c54646f6651375e2e1999bb8e98b4335d358d9c0d6773dbb28` |

## Final exposure and claim state

- Public open commitments for contest 7: **0**
- Public open commitments for speculation 11: **0**
- Public open commitments for speculation 12: **0**
- Target active / pending-settle / claimable positions across the three controlled wallets: **0 / 0 / 0**
- Orphan live MM process: **none**
- Losing San Diego positions are not claimable and are no-op.

## Caveats

- The first live quote batch expired before controlled fill; MM reposted, and the controlled fill used the second spread batch.
- The live cancel sweep found no remaining visible quotes because unfilled quotes had already expired/been hidden; public/API open commitments are zero.
- A fresh dry-run/cold-start probe wrote synthetic dry records into the live state file; the synthetic records were backed up and removed before final state reporting.
- A duplicate score request attempted after postgame completion reverted because contest 7 was already scored; it had no state effect and is not part of the artifact transaction set.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
