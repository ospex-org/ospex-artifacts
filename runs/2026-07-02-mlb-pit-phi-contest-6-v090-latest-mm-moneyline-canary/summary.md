# v0.9.0 latest-main moneyline MM canary — PIT @ PHI contest 6

Verdict: **FULL_GREEN** (`complete_verified_with_caveats`)

This artifact records the 2026-07-02 Ospex R5/v0.9.0 latest-main market-maker moneyline canary for Pittsburgh Pirates @ Philadelphia Phillies (`contestId 6`, `speculationId 10`).

## Result

| Gate | Result |
|---|---|
| Target preflight | PASS — primary PIT/PHI was official pre-game, exact identity matched, odds were available, and there was sufficient runway. |
| Repo/runtime gates | PASS — SDK/CLI v0.9.0 and MM head `6121a73`+ with installed SDK v0.9.0; typecheck/test/build green. |
| Manual setup seed | PASS — one tiny seed was fully matched to create moneyline speculation 10, leaving zero open seed commitments. |
| MM dry-run | PASS — `candidates --allowlist-only` returned exactly contest 6 quote_ready; quote dry-run canQuote=true; dry run stayed allowlisted. |
| Live MM | PASS — strict allowlist `[6]`, moneyline only, no broad slate, tiny risk. |
| Controlled fill | PASS — one live MM quote filled, commitment `0x6d2a5bd0a364ca1f9c5584af8caa167f8d35e6bf7804f3e2e4fd4588d1b5698d`, tx `0x0b5a1039703e491a548891ba68b8b569228858e57fa8370769328a26b8b29e8f`. |
| Canonical fill source | PASS — telemetry `kind=fill`, `source=own-state-stream`. |
| Stop/exit | PASS — runner saw KILL, soft-cancelled the remaining quote, exited 0, and no orphan process remained. |
| Zero visible-open exposure | PASS — final public/open commitment checks and orderbook count are zero. |
| Postgame | PASS — Pittsburgh Pirates 6, Philadelphia Phillies 1; contest scored, speculation settled to away/upper/Pittsburgh Pirates, winning positions claimed. |
| Artifact validation | PASS locally before PR/opening. |

## Target and team identity

| Field | Value |
|---|---|
| Game | Pittsburgh Pirates @ Philadelphia Phillies |
| gamePk | `823442` |
| Contest / speculation | `6` / `10` |
| Market | moneyline |
| Upper / lower | upper = away = Pittsburgh Pirates; lower = home = Philadelphia Phillies |
| Reference odds at live gate | Pittsburgh Pirates +114, Philadelphia Phillies -126 |
| Favorite / underdog at live gate | Philadelphia Phillies favorite, Pittsburgh Pirates underdog |
| Final score | Pittsburgh Pirates 6, Philadelphia Phillies 1 |
| Winning side | away / upper / Pittsburgh Pirates |

## Live fill

| Field | Value |
|---|---|
| Live maker | `ospex-stage-maker-b` / `0x4fA0a5Aa3187517EFC320AAC7d33CD6115cC7482` |
| Controlled taker | `ospex-flow-a` / `0x16Dc5D67D080a5521ef2c79680dBfC2aBf724D30` |
| Commitment | `0x6d2a5bd0a364ca1f9c5584af8caa167f8d35e6bf7804f3e2e4fd4588d1b5698d` |
| Fill tx | `0x0b5a1039703e491a548891ba68b8b569228858e57fa8370769328a26b8b29e8f` |
| Maker side | lower / home / Philadelphia Phillies |
| Taker side | upper / away / Pittsburgh Pirates |
| Maker filled risk | 0.100000 USDC |
| Taker risk | 0.087000 USDC |
| Canonical telemetry | `source=own-state-stream` |

## Postgame transactions

| Step | Tx |
|---|---|
| Bounded Treasury approval | `0x79ba21eb4c250efcb5b65d616848d21a4b80b4dfb4365549e8df340f7b5eaedc` |
| Contest create | `0x0fd8b518dd485ea11dbf4301ba2ff47a2f4aafd2423e10ee633008dbd30e4873` |
| Market update | `0x9ffb9adc1fc72385c67f3fa4f4a9eb9d190c6b91ed7502fb64255384e5c00188` |
| Manual seed fill | `0xd7db6cbcba50ebf295461a790f53de8d5b50ac0c58f1474df766c44533afb1b6` |
| Controlled live fill | `0x0b5a1039703e491a548891ba68b8b569228858e57fa8370769328a26b8b29e8f` |
| Score contest 6 request | `0x2d0f65f8329a21cbaf34b143c6d8128536fa842f7d758f4cd687e1b863f25f51` |
| Settle speculation 10 | `0xd64e9dbc2fa8f8c05b0e8ef1cb09e2534bab48529d6e418d130c6648155430ac` |
| Claim seed maker winner | `0x4d1b4e0c3ac8aa2132fbaa19567e4cbaff514ab255e5493432018a8bd8fe3998` |
| Claim live taker winner | `0x40219eac365362a2e1e9d784c753c86e03c94b77cd99a83508a089ab7d68f832` |

## Final exposure and claim state

- Public open commitments for contest 6: **0**
- Public open commitments for speculation 10: **0**
- Speculation 10 orderbook entries: **0**
- Target active / pending-settle / claimable positions across the three controlled wallets: **0 / 0 / 0**
- Orphan live MM process: **none**
- Losing lower/Philadelphia positions are not claimable and are no-op.

## Caveats

- The live shutdown attempted to cancel the already-filled quote and got the expected filled-quote refusal; this is not residual exposure because the filled quote was matched and public/open exposure is zero.
- A fresh dry-run/cold-start probe wrote synthetic dry records into the live state file; the synthetic records were backed up and removed before final state reporting.
- The artifact lists the score request transaction and verifies the resulting scored contest plus successful settlement; no separate score-callback transaction hash is claimed.

## Evidence files

See `evidence.json`, `scenario-matrix.json`, `mve-scorecard.json`, and the sanitized files under `raw/`.
