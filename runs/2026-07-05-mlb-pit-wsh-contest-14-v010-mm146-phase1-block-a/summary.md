# 2026-07-05-mlb-pit-wsh-contest-14-v010-mm146-phase1-block-a

## Verdict

**FULL_GREEN** / `complete_verified` — The v0.10.0/R5 MM #146 strict-allowlist Phase 1 Block A two-contest MVE for Pittsburgh Pirates @ Washington Nationals completed the full lifecycle: contest 14 was created and verified; moneyline, spread, and total speculations 30/31/32 were manually seeded and filled with zero residual seed exposure; the market maker posted tiny live quotes under strict contest allowlist [13,14] with seedSpeculations=false; one controlled live spread quote was filled; visible quotes were soft-cancelled or expired; final open commitments were zero; official final score Pittsburgh Pirates 11 / Washington Nationals 5 was verified; contest 14 was scored through R5/CRE; target speculations were settled, winning controlled positions were claimed, and final target active/pending/claimable positions are zero.

## Target

- Game: Pittsburgh Pirates (away) @ Washington Nationals (home)
- Contest: `14`
- Markets/speculations: moneyline `30`, spread `31`, total `32`
- Final: Pittsburgh Pirates 11, Washington Nationals 5
- Winning protocol sides: moneyline upper/away, spread upper/away, total upper/over

## Live Phase 1 block

- Strict contest allowlist: `[13, 14]`
- Markets posted: moneyline, spread, total
- Target controlled live fill: spread `0xacec44a376c7a30885a6913a5efba3bd881ff53d598fd6cb3549a30ee44383e8`
- Live fill tx: `0x93368b1340e88a05179477ab07cb62d4018f4a00575968ce9eed72577a1ec196`
- Final open commitments: `0`

## Postgame

- Score/settle/claim completed through SDK/CLI v0.10.0.
- Final active/pending/claimable target positions: `0` for ospex-stage-maker-a, ospex-stage-maker-b, and ospex-flow-a.

## Evidence

- `evidence.json`
- `scenario-matrix.json` / `scenario-matrix.md`
- `mve-scorecard.json` / `mve-scorecard.md`
- sanitized raw evidence under `raw/`
