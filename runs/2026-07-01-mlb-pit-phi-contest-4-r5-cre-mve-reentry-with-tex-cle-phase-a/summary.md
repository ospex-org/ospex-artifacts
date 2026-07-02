# R5/CRE MVE re-entry lifecycle — TEX/CLE all-markets + PIT/PHI MM canary

Verdict: **POSTGAME zero-state GREEN with caveats** (`complete_verified_with_caveats`)

This artifact records the 2026-07-01 Ospex R5/CRE MVE re-entry run. It combined an early manual all-market R5 lifecycle setup on contest `3` with an evening strict-allowlist market-maker canary on contest `4`, then completed postgame score → settle → claim convergence for both contests.

## Scope

- Phase A: manual SDK/CLI all-market R5 setup for moneyline, spread, and total.
- Phase B: strict-allowlist MM canary against one evening moneyline speculation.
- Tiny controlled positions only.
- Bounded approvals only; no unlimited approvals.
- No broad market-maker slate run.
- R5/CRE path only; no old Functions/LINK flow.

## Version gates

| Gate | Result |
|---|---|
| Setup/live SDK/CLI | PASS — v0.8.0 at `4c7af9106166` |
| Setup/live market-maker | PASS — `aa43da8836f2` with installed `@ospex/sdk` 0.8.0 |
| MM typecheck/test/build | PASS |
| core-api / indexer / CRE / contracts-v2 | PASS — `ca9e68521c59` / `75be9e76965b` / `fed6e26e27e5` / `5483452e95c8` |
| Postgame executor | Observed CLI/SDK 0.9.0 in postgame command JSON after the local checkout was updated; postgame converged successfully. |

## Phase A — early all-market manual setup

| Field | Value |
|---|---|
| Game | Texas Rangers @ Cleveland Guardians |
| gamePk | `824419` |
| Contest | `3` |
| Final score | Texas Rangers 4, Cleveland Guardians 9 |
| Final contest status | `scored` |

### Phase A fills

| Market | Spec | Maker side | Taker side | Maker risk | Taker risk | Match tx | Winner |
|---|---:|---|---|---:|---:|---|---|
| moneyline | `3` | Texas Rangers away/upper `-104` | Cleveland Guardians home/lower `+104` | 0.100000 | 0.096000 | `0x8e3b1130a35bd617f910c3a9d6631517f741df73ff5de01a658ce4712b612629` | Cleveland home/lower |
| spread | `4` | Cleveland Guardians home/lower `-1.5` at `+184` | Texas Rangers away/upper `+1.5` | 0.100000 | 0.184000 | `0x5c174f334b58981f32fedecc23266cdf110caf5449b7b9157c373f29cea622e7` | Cleveland home/lower |
| total | `5` | Over `8.0` upper at `-105` | Under `8.0` lower | 0.100000 | 0.095000 | `0x415facb8078c7418eb9b6d9db737c90ee81ed2bba8d7b72eb6436fd9fc9d3613` | Over/upper |

Pregame state was clean: contest verified, exactly three intended speculations present, and open commitments `0`.

## Phase B — evening strict-allowlist MM canary

| Field | Value |
|---|---|
| Game | Pittsburgh Pirates @ Philadelphia Phillies |
| gamePk | `823446` |
| Contest | `4` |
| Speculation | `6` moneyline |
| Final score | Pittsburgh Pirates 6, Philadelphia Phillies 10 |
| Winner | Philadelphia Phillies / home / lower |
| Final contest status | `scored` |

### Canary setup and live fill

- MM config: markets `[moneyline]`, `contestAllowList: ["4"]`, `seedSpeculations: false`, direct pricing, max risk per commitment 0.10 USDC, max open commitments 2, 120-second expiry, off-chain cancel, auto-approval disabled.
- Dry-run gates: doctor ready, target contest quote-ready, quote `canQuote=true`, dry-run telemetry would-submit only for contest `4`.
- Manual seed: speculation `6`, maker `ospex-stage-maker-a` backed Philadelphia home/lower at CLI-rounded `-135`; taker `ospex-flow-a` backed Pittsburgh away/upper at `+135`; match tx `0x9ca5849a3521435880ebb117bb1f38a0474335347fe3f30ffca8f9d8a74a1330`.
- Live MM canary: run `2026-07-01T14-35-21-607Z-51tskn` posted tiny moneyline quotes. Controlled taker matched commitment `0xa3ee7a32…` via tx `0x5b484dfa52d57073e437a9b36792eb650a331b70bed60f4a09a104adf9e96a35`.
- Matched live quote: maker `ospex-stage-maker-b` Philadelphia home/lower `-122`, risk 0.100000 USDC; taker `ospex-flow-a` Pittsburgh away/upper `+122`, risk 0.082000 USDC.
- Remaining visible quote was cancelled off-chain; final contest-4 commitments list was empty.

## Postgame result

| Gate | Result |
|---|---|
| Official final score | PASS — contests `3` and `4` both final. |
| R5/CRE score request | PASS — score requests submitted for contests `3` and `4`. |
| Settlement | PASS — specs `3`, `4`, `5`, and `6` settled. |
| Claims | PASS — controlled winning positions claimed. |
| Final commitments/orderbook | PASS — contest `3` open commitments `0`, contest `4` open commitments `0`. |
| Final positions.status | PASS — maker, taker, and operator all active `0`, pendingSettle `0`, claimable `0`. |

## Key transactions

| Step | Tx |
|---|---|
| Phase A contest create | `0x2718cb65e739310ca6801f049a2dc16cd97a4c4610493182bcd41b0cac836e3e` |
| Phase A market update | `0x7fd9cc5ebca4bca1c7e55bd4262d35340d4acbb9c6e88f510975870e0b4c1391` |
| Phase A moneyline match | `0x8e3b1130a35bd617f910c3a9d6631517f741df73ff5de01a658ce4712b612629` |
| Phase A spread match | `0x5c174f334b58981f32fedecc23266cdf110caf5449b7b9157c373f29cea622e7` |
| Phase A total match | `0x415facb8078c7418eb9b6d9db737c90ee81ed2bba8d7b72eb6436fd9fc9d3613` |
| Phase B contest create | `0x828d6199810be2e2ffa58ac3f74f147a13a517d5cac0d715507f2509570435e3` |
| Phase B market update | `0xeb5f9116bbc9145e2fb9dd115e7b7b3310fc6a422d44cc7e7fec77316a150ab9` |
| Phase B seed match | `0x9ca5849a3521435880ebb117bb1f38a0474335347fe3f30ffca8f9d8a74a1330` |
| Phase B controlled MM quote match | `0x5b484dfa52d57073e437a9b36792eb650a331b70bed60f4a09a104adf9e96a35` |
| Contest 3 score request | `0x06a07b8ef4bfda8bb9978abeb48e7d4e4e655cf716aca66a9f1dbe3f514daced` |
| Contest 4 score request | `0xa1d32047f8890a86c5578b26cd2a786f84a23fd63d56c8451c92043b9e35bae6` |
| Settle specs `3/4/5/6` | `0x963006827c0a86dd84c98bd10f34e622c2f4b5e6c6d54e1cdf1cdd5bbb81754e`, `0x4abfa09d79308956a828132ae92db4bca81da2446c90cc2d8d4dfeb832da162c`, `0xfef3934c514bb03c184241ede43f6e12add3227390c7a33a9425b21584ec64b5`, `0xc3d2411d969b2b47a5c6c27798f05f540ecdb2715e5071052d7660bf7a46e777` |
| Claim winners | `0x1749cf2227a622febadc820aa00781733442f83e8a3d6e2e4360ec5bac4a7631`, `0x97641368afafd852e191db4cb0e4b74ea28d935a07d6aa19bd8f2f1652f49eb4`, `0xb7973c8fe665bfdef2993f2ba4ec85d6e9f35e81968c54622751418b6472e4d0`, `0x3f848021ab0b343612a03a598f2229921391c42a9cd9abbc5f6438f396ab62f4`, `0x8a6421e4c457281242398c5b21dc2f5332f020eb4e4763db50204632070188d9` |

## Final zero-state

- Contest `3`: open commitments `0`.
- Contest `4`: open commitments `0`.
- `ospex-stage-maker-a`: active `0`, pendingSettle `0`, claimable `0`.
- `ospex-flow-a`: active `0`, pendingSettle `0`, claimable `0`.
- `ospex-stage-maker-b`: active `0`, pendingSettle `0`, claimable `0`.

## Caveats

1. The live MM process was intentionally stopped after the first controlled fill to keep exposure bounded. The remaining visible quote was cancelled off-chain and final open commitments were zero.
2. The candidates command emitted non-allowlisted setup rows despite `contestAllowList`; dry-run/live runner telemetry selected only contest `4`, so this is recorded as a CLI/reporting caveat, not broad live quoting.
3. Setup/live gates were run with SDK/CLI 0.8.0 as requested for the first MVE re-entry run. Postgame score, settle, claim, and final status commands were later executed with local CLI/SDK 0.9.0 and converged successfully.

## Evidence files

Canonical facts are in `evidence.json`. Sanitized raw evidence is under `raw/`, with scenario coverage in `scenario-matrix.json` and MVE readiness coverage in `mve-scorecard.json`.
