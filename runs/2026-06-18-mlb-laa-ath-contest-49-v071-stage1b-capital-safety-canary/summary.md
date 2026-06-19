# v0.7.1 Stage-1b capital-safety canary — LAA @ ATH contest 49

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-06-18/19 v0.7.1 Ospex market-maker Stage-1b capital-safety canary for Los Angeles Angels @ Athletics (`contestId 49`, `speculationId 38`).

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — LAA/ATH was official pre-game, exact identity matched, and quote dry-run returned `computed` / `canQuote=true`. |
| Live MM | PASS — exactly one live MM process, strict allowlist `[49]`, Stage-1b risk caps. |
| Controlled fill | PASS — one fill, commitment `0x0f6b5182f859c887494f22f559038b31b828c1d904a2c3dd8df895f997ce06ae`, tx `0xabdd54e077b29c2d856d96a3071d53c88a163074e574dd141013de755ba3c114`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — graceful KILL, process exit 0, no orphan live MM process. |
| Zero visible-open exposure | PASS — public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — LAA 0, ATH 5; contest scored, speculation settled to home/lower/Athletics, winning positions claimed. |
| Artifact validation | PASS locally before PR. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Los Angeles Angels @ Athletics |
| gamePk | `824989` |
| Contest / speculation | `49` / `38` |
| Market | moneyline |
| Upper / lower | upper = away = Los Angeles Angels; lower = home = Athletics |
| Reference odds at fill | Los Angeles Angels +156, Athletics -156 |
| Favorite / underdog at fill | Athletics favorite, Los Angeles Angels underdog |
| Final score | Los Angeles Angels 0, Athletics 5 |
| Winning side | home / lower / Athletics |

## Live fill

| Field | Value |
|---|---|
| Live maker | `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2` |
| Controlled taker | `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494` |
| Commitment | `0x0f6b5182f859c887494f22f559038b31b828c1d904a2c3dd8df895f997ce06ae` |
| Fill tx | `0xabdd54e077b29c2d856d96a3071d53c88a163074e574dd141013de755ba3c114` |
| Maker side | upper / away / Los Angeles Angels |
| Taker side | lower / home / Athletics |
| Maker filled risk | 2.000000 USDC |
| Taker risk | 3.120000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Setup seed fill | `0xd376002295b0071e5927b34ee42592a60171fb16a97cb58b8691523526a42365` |
| Controlled live fill | `0xabdd54e077b29c2d856d96a3071d53c88a163074e574dd141013de755ba3c114` |
| Score contest 49 request | `0x3f08214754ccaab5f68797639b4380ceabced474a3883fa861e3f1ed905148c6` |
| Settle speculation 38 | `0x104282aab58b8f2d4ecbc0849f0dc1987f2051fbb0b81724ea707366bb78644a` |
| Claim controlled live taker winner | `0xced29afbc6361965f151e524526e2ed182e42bb155f040a0e2d3368a41bf14e6` |
| Claim setup seed taker winner | `0x3b390155a59f1adc4e6b8f1172a591b4c36dbda2f9bbd51faec92c426f941e61` |

## Final exposure and claim state

- Public open commitments for contest 49: **0**
- Maker-filtered visible/open commitments: **0**
- Contest/spec orderbook entries: **0**
- Final claim dry-runs for setup/live maker/taker wallets: **0 entries**
- Orphan live MM process: **none**
- Losing upper/Los Angeles Angels positions are not claimable and are no-op.

## Caveats

- A separate restart/cold-start probe was not run; final zero-exposure and process checks were run instead.
- The artifact lists the score request transaction and verifies the resulting scored contest plus settlement; no separate score-callback transaction hash is claimed.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
