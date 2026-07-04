# 2026-07-04-mlb-min-nyy-contest-10-v010-mm146-all-markets-stage1-canary

## Verdict

**FULL_GREEN** / `complete_verified_with_caveats` — The v0.10.0/R5 MM #146 strict-allowlist all-market Stage 1 canary for Minnesota Twins @ New York Yankees completed the full lifecycle: pregame setup passed, contest 10 was created and verified, moneyline speculation 18, spread speculation 19, and total speculation 20 were manually seeded/filled with zero residual seed exposure, the market maker posted tiny live moneyline, spread, and total quotes under contest allowlist [10] with seedSpeculations=false, two controlled live spread/total quotes were filled, visible quotes were soft-cancelled after a bounded funding-shortfall hold, final open exposure drained to zero, official final score Minnesota Twins 11 / New York Yankees 4 was verified, contest 10 was scored through R5/CRE, speculations 18/19/20 settled to away/upper/Minnesota Twins, away/upper/Minnesota Twins +1.5, and over/upper/over 10, winning controlled positions were claimed, and final target commitments plus active/pending/claimable positions are zero.

## Target

- Game: Minnesota Twins (away) @ New York Yankees (home)
- Contest: `10`
- Markets/speculations: moneyline `18`, spread `19`, total `20`
- Final: Minnesota Twins 11, New York Yankees 4
- Winning protocol sides: moneyline upper/away, spread upper/away +1.5, total upper/over 10

## Live canary

- Strict contest allowlist: `[10]`
- Markets posted: moneyline, spread, total
- Live commitments posted: 6
- Controlled fills: spread `0xd44aa5a2fdba…`, total `0x5cd5eb435cba…`
- Funding caveat: after controlled fills, the MM entered a bounded funding-shortfall hold and soft-cancelled visible quotes; final visible exposure was zero.

## Postgame

- Score tx: `0x34ad599c48765d1c93db336cf748972d9353a1dc87d15ffdf1990969d36b58dd`
- Settle txs: moneyline `0x9afc9fa30800ce57b8a6e9c4a3ab72cb29e5fe6a607d71d541bc370e933a6db2`, spread `0x500946516ae886157abd1bafba18e3b79c205b69c87b234541d32f4cf50b50e6`, total `0xbf9ec03d9c76d72c2e6e212a24e3a4eb6554e3318d80cbb827522cfab444c090`
- Claim txs: stage-maker-a `0x541b469913d374904261816dc48aa06c2c9428d0f0a93da4bc32c211dc3d72a6`, `0x8103f472b1b6c3b2c37498dace4e50558697ea8c523bb00020c3d0d51aa7c971`, `0x4a707455d75939be1cdcaed9084695ddbba6dbfe1b7e89a7579e9ae56c9d1606`; stage-maker-b `0x6755511b40f2d324a5151456ce4743388fb50e695fa8cfd4eebd5fa6e9057c32`, `0xe158c082888471525912b1dc7f076232bd5ac4d6a9fe5f163de183a49aacba2c`
- Final open commitments: `0`; final active/pending/claimable target positions: `0` for stage-maker-a, stage-maker-b, and flow-a.

## Caveats

- The postgame cron/watchdog initially no-oped because core games API status still reported `upcoming` after MLB official final. Postgame was manually resumed after independent MLB Stats official-final verification; score/settle/claim completed successfully, and final zero-state was verified. This is an operator/watchdog methodology caveat, not a protocol/MM failure.
- Live MM correctly entered a bounded funding-shortfall hold after the controlled fills and soft-cancelled visible quotes; final visible exposure was zero.
- The market-maker repository still installed @ospex/sdk 0.9.0 while the operator CLI for this run was 0.10.0; this was recorded and did not block the tested flow.

## Evidence

- `evidence.json`
- `scenario-matrix.json` / `scenario-matrix.md`
- `mve-scorecard.json` / `mve-scorecard.md`
- sanitized raw evidence under `raw/`
