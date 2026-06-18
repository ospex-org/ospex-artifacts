# v0.7.1 MM repeatability canary — TOR @ BOS contest 46

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the second v0.7.1 Ospex market-maker repeatability canary from 2026-06-17. The selected live target was Toronto Blue Jays @ Boston Red Sox (`contestId 46`, `speculationId 35`). The prepared fallback, Cleveland Guardians @ Milwaukee Brewers (`contestId 47`, `speculationId 36`), was not used live; its setup seed lifecycle was also scored/settled/claimed after final so no setup exposure remains.

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — TOR/BOS was official pre-game, exact identity matched, and quote dry-run returned `computed` / `canQuote=true`. |
| Live MM | PASS — exactly one live MM process, strict allowlist `[46]`, tiny risk caps. |
| Controlled fill | PASS — one fill, commitment `0xe84032f1a0f3d8a4b92bf6774e0e117fe5fe610bb678c2afa69aecf34709e2e8`, tx `0xe2d797bdd7936c7b81f5d5236c38749d35b57ea2b4ef1232b85079f4c80b3be8`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Shutdown | PASS — graceful KILL, process exit 0, no orphan live MM process. |
| Zero visible-open exposure | PASS — public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — TOR 3, BOS 0; contest scored, speculation settled to away/upper/Toronto, winning positions claimed. |
| Artifact validation | PASS locally before PR. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Toronto Blue Jays @ Boston Red Sox |
| gamePk | `824746` |
| Contest / speculation | `46` / `35` |
| Market | moneyline |
| Upper / lower | upper = away = Toronto; lower = home = Boston |
| Reference odds at setup | Toronto +105, Boston -119 |
| Favorite / underdog at setup | Boston favorite, Toronto underdog |
| Final score | Toronto 3, Boston 0 |
| Winning side | away / upper / Toronto Blue Jays |

## Live fill

| Field | Value |
|---|---|
| Live maker | `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2` |
| Controlled taker | `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494` |
| Commitment | `0xe84032f1a0f3d8a4b92bf6774e0e117fe5fe610bb678c2afa69aecf34709e2e8` |
| Fill tx | `0xe2d797bdd7936c7b81f5d5236c38749d35b57ea2b4ef1232b85079f4c80b3be8` |
| Maker side | upper / away / Toronto Blue Jays |
| Taker side | lower / home / Boston Red Sox |
| Maker filled risk | 0.100000 USDC |
| Taker risk | 0.114000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Score contest 46 | `0x5deff565bf47d9b56fdf60fc5cb14085653b815d84c55e175cabcc8acea3e70e` |
| Settle speculation 35 | `0x735adad17d9918b4fb3bf493a0442cde6d64b24e05960fa33ad346e74f9c4ed2` |
| Claim setup seed winner | `0x315892ddf9230d6234f4a4a5a01974eaf7189f8b50f338d9b27e38c4b05afb82` |
| Claim live maker winner | `0x81362c0844457b2e05652caf446e159b06ebcbafba0cfd1d8998e162bd2df100` |

## Final exposure and claim state

- Public open commitments for contest 46: **0**
- Maker-filtered visible/open commitments: **0**
- Contest orderbook entries: **0**
- Final claim dry-runs for setup/live maker/taker wallets: **0 entries**
- Orphan live MM process: **none**
- Losing lower/Boston positions are not claimable and are no-op.

## Fallback setup cleanup

Fallback CLE @ MIL was prepared but not used live. After final, Milwaukee beat Cleveland 9-4. Contest 47 was scored, speculation 36 settled to home/lower/Milwaukee, and the setup seed taker/winner was claimed. Final fallback claim dry-runs and public/open commitments are zero.

## Caveats

- Restart/cold-start safety was not run as a separate probe; final zero-exposure/process checks were run instead.
- During the live window, an operator-side polling filter initially over-constrained commitment listing. That delayed the fill but did not create extra fills or exposure.
- The live loop posted and expired/soft-cancelled multiple tiny quotes while waiting for the controlled fill; telemetry shows exactly one fill and final visible-open exposure zero.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
