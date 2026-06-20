# v0.7.1 Stage-2a repeat capital-safety canary — WSH @ TB contest 51

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-06-19 v0.7.1 Ospex market-maker Stage-2a repeat capital-safety canary for Washington Nationals @ Tampa Bay Rays (`contestId 51`, `speculationId 40`).

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — WSH/TB was official pre-game, exact identity matched, and quote dry-run returned `computed` / `canQuote=true`. |
| Same-day wallet reuse | PASS — the TOR/CHC canary was postgame-clean first, then the same live maker/taker were freshly proven clean before WSH/TB. |
| Live MM | PASS — exactly one live MM process, strict allowlist `[51]`, Stage-2a risk caps. |
| Controlled fill | PASS — one fill, commitment `0x19a0faa4548a84a669744e76c8166cafb08e9f750d8db450335c4b7911912eb8`, tx `0x2b1734ebd1e77a064447a9df8b9b1d32c1aec895f11f7fa37c8729a9e22609e7`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — graceful KILL, process exit 0, no orphan live MM process. |
| Zero visible-open exposure | PASS — public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — Washington Nationals 2, Tampa Bay Rays 5; contest scored, speculation settled to home/lower/Tampa Bay Rays, winning positions claimed. |
| Artifact validation | PASS locally before PR/opening. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Washington Nationals @ Tampa Bay Rays |
| gamePk | `822966` |
| Contest / speculation | `51` / `40` |
| Market | moneyline |
| Upper / lower | upper = away = Washington Nationals; lower = home = Tampa Bay Rays |
| Reference odds at live gate | Washington Nationals +136, Tampa Bay Rays -155 |
| Favorite / underdog at live gate | Tampa Bay Rays favorite, Washington Nationals underdog |
| Final score | Washington Nationals 2, Tampa Bay Rays 5 |
| Winning side | home / lower / Tampa Bay Rays |

## Live fill

| Field | Value |
|---|---|
| Live maker | `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2` |
| Controlled taker | `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494` |
| Commitment | `0x19a0faa4548a84a669744e76c8166cafb08e9f750d8db450335c4b7911912eb8` |
| Fill tx | `0x2b1734ebd1e77a064447a9df8b9b1d32c1aec895f11f7fa37c8729a9e22609e7` |
| Maker side | upper / away / Washington Nationals |
| Taker side | lower / home / Tampa Bay Rays |
| Maker filled risk | 5.000000 USDC |
| Taker risk | 7.150000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Setup seed fill | `0x9c490581c1399c6cf059a2e5dc02348cf2277ca55504946069f034663f3f4e4e` |
| Controlled live fill | `0x2b1734ebd1e77a064447a9df8b9b1d32c1aec895f11f7fa37c8729a9e22609e7` |
| Score contest 51 request | `0xbe83ef82861e19a8ba5b11d3c2741ef50e775d7cd68155d06492e9869928f533` |
| Settle speculation 40 | `0x27cbadf00abf69fa2c60e11d361dd38ac2ae64a4d18e4d3cab17e98ce8895f34` |
| Claim controlled live taker winner | `0x5772910966d45e22ad85565bdda75ca304335ffc10bfea4857e521e4e6f1b89c` |
| Claim setup seed taker winner | `0xb282931729d2fca7256983cbb67307c2c2dd3c3b43851cfdc94d38188e2bc82a` |

## Final exposure and claim state

- Public open commitments for contest 51: **0**
- Maker-filtered visible/open commitments: **0**
- Contest/spec orderbook entries: **0**
- Final claim dry-runs for setup/live maker/taker wallets on spec 40: **0 entries**
- Orphan live MM process: **none**
- Losing upper/Washington Nationals positions are not claimable and are no-op.

## Caveats

- A separate restart/cold-start probe was not run; final zero-exposure and process checks were run instead.
- The artifact lists the score request transaction and verifies the resulting scored contest plus successful settlement; no separate score-callback transaction hash is claimed.
- The controlled fill landed on a quote that had been off-chain hidden as part of the normal replacement/risk loop; the signature was still matchable until expiry, own-state SSE recorded the fill, and final public/open exposure was zero.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
