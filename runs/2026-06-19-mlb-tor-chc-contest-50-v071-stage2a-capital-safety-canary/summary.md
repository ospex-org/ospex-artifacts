# v0.7.1 Stage-2a capital-safety canary — TOR @ CHC contest 50

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-06-19 v0.7.1 Ospex market-maker Stage-2a capital-safety canary for Toronto Blue Jays @ Chicago Cubs (`contestId 50`, `speculationId 39`).

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — TOR/CHC was official pre-game, exact identity matched, and quote dry-run returned `computed` / `canQuote=true`. |
| Live MM | PASS — exactly one live MM process, strict allowlist `[50]`, Stage-2a risk caps. |
| Controlled fill | PASS — one fill, commitment `0xdcee7fb35f7b0b62afbc41f18f3529fb51d85984ec4f3114ed8edd72b5fe8dd6`, tx `0x89f09327ac9d51ea18ca7d4391ce3ee106d71bd27cf40dc2adf4a8d469c2ccbc`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — graceful KILL, process exit 0, no orphan live MM process. |
| Zero visible-open exposure | PASS — public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — Toronto Blue Jays 2, Chicago Cubs 16; contest scored, speculation settled to home/lower/Chicago Cubs, winning positions claimed. |
| Artifact validation | PASS locally before PR/opening. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Toronto Blue Jays @ Chicago Cubs |
| gamePk | `824663` |
| Contest / speculation | `50` / `39` |
| Market | moneyline |
| Upper / lower | upper = away = Toronto Blue Jays; lower = home = Chicago Cubs |
| Reference odds at live gate | Toronto Blue Jays +107, Chicago Cubs -119 |
| Favorite / underdog at live gate | Chicago Cubs favorite, Toronto Blue Jays underdog |
| Final score | Toronto Blue Jays 2, Chicago Cubs 16 |
| Winning side | home / lower / Chicago Cubs |

## Live fill

| Field | Value |
|---|---|
| Live maker | `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2` |
| Controlled taker | `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494` |
| Commitment | `0xdcee7fb35f7b0b62afbc41f18f3529fb51d85984ec4f3114ed8edd72b5fe8dd6` |
| Fill tx | `0x89f09327ac9d51ea18ca7d4391ce3ee106d71bd27cf40dc2adf4a8d469c2ccbc` |
| Maker side | lower / home / Chicago Cubs |
| Taker side | upper / away / Toronto Blue Jays |
| Maker filled risk | 5.000000 USDC |
| Taker risk | 4.450000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Setup seed fill | `0xb2f8947c31e5f34f671006a6a96c2886f6d0f32351264bdaca930773cf4a81c3` |
| Controlled live fill | `0x89f09327ac9d51ea18ca7d4391ce3ee106d71bd27cf40dc2adf4a8d469c2ccbc` |
| Score contest 50 request | `0x5ac8afe5e0808de878151a5bb8a0c96e356d48b11eab3a63afaba95d70c5d524` |
| Settle speculation 39 | `0xd4f4edf930c97b0b72e3e425da00dfa5f7307b25a285daef1c9e39564bc57e44` |
| Claim controlled live maker winner | `0x4be831d50d2111ed14104c801a80c20d880c07506094f56568be4428a6554ae8` |
| Claim setup seed taker winner | `0xc0e73ae2d934eff9d03c491b6555016cc81a605d9d97b2fa6e6a3b2c50be1dbc` |

## Final exposure and claim state

- Public open commitments for contest 50: **0**
- Maker-filtered visible/open commitments: **0**
- Contest/spec orderbook entries: **0**
- Final claim dry-runs for setup/live maker/taker wallets on spec 39: **0 entries**
- Orphan live MM process: **none**
- Losing upper/Toronto Blue Jays positions are not claimable and are no-op.

## Caveats

- A separate restart/cold-start probe was not run; final zero-exposure and process checks were run instead.
- The artifact lists the score request transaction and verifies the resulting scored contest plus successful settlement; no separate score-callback transaction hash is claimed.
- The controlled fill landed on a quote that had been off-chain replaced/hidden just before confirmation; the signature was still matchable until expiry, own-state SSE recorded the fill, and final public/open exposure was zero.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
