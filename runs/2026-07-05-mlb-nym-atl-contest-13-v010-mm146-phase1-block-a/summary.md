# 2026-07-05-mlb-nym-atl-contest-13-v010-mm146-phase1-block-a

## Verdict

**FULL_GREEN** / `complete_verified` — The v0.10.0/R5 MM #146 strict-allowlist Phase 1 Block A two-contest MVE for New York Mets @ Atlanta Braves completed the full lifecycle: contest 13 was created and verified; moneyline, spread, and total speculations 27/28/29 were manually seeded and filled with zero residual seed exposure; the market maker posted tiny live quotes under strict contest allowlist [13,14] with seedSpeculations=false; one controlled live total quote was filled; visible quotes were soft-cancelled or expired; final open commitments were zero; official final score New York Mets 10 / Atlanta Braves 9 was verified; contest 13 was scored through R5/CRE; target speculations were settled, winning controlled positions were claimed, and final target active/pending/claimable positions are zero.

## Target

- Game: New York Mets (away) @ Atlanta Braves (home)
- Contest: `13`
- Markets/speculations: moneyline `27`, spread `28`, total `29`
- Final: New York Mets 10, Atlanta Braves 9
- Winning protocol sides: moneyline upper/away, spread upper/away, total upper/over

## Live Phase 1 block

- Strict contest allowlist: `[13, 14]`
- Markets posted: moneyline, spread, total
- Target controlled live fill: total `0x1879f298908f808878895576060d9f0cbc07fd8c33ae2917b7a3dd1441fe6afb`
- Live fill tx: `0x51e2dea37d595ab589be2db96a9707a6875605505b5f3fb26f35db83c46dd112`
- Final open commitments: `0`

## Postgame

- Score/settle/claim completed through SDK/CLI v0.10.0.
- Final active/pending/claimable target positions: `0` for ospex-stage-maker-a, ospex-stage-maker-b, and ospex-flow-a.

## Evidence

- `evidence.json`
- `scenario-matrix.json` / `scenario-matrix.md`
- `mve-scorecard.json` / `mve-scorecard.md`
- sanitized raw evidence under `raw/`
