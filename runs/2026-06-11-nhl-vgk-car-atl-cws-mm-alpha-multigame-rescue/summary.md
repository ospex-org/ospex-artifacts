# NHL VGK-CAR + MLB ATL-CWS ospex-market-maker v0.1.0-alpha.1 multigame rescue

Status: **complete_verified_with_caveats** / live-window green; NHL postgame complete; MLB void/refund complete.

This artifact records a low-value two-target rescue canary on Polygon using `ospex-market-maker` `v0.1.0-alpha.1` at `af1bb107af47dc80f27485dee7417ca95b782b50` with the repo-pinned `@ospex/sdk` `v0.6.2`.

## Targets

- NHL: Vegas Golden Knights @ Carolina Hurricanes, NHL game `2025030415`, Ospex game `12fcb924-bfbe-4fac-b447-af05b8c9c3e1`, contest `39`, speculation `28`.
- Team identity / reference odds: Carolina Hurricanes were the home/lower favorite (`-160`, tick `163`) and won; Vegas Golden Knights were the road/upper underdog (`+140`, tick `240`) and lost.
- MLB: Atlanta Braves @ Chicago White Sox, MLB gamePk `824589`, contest `38`, speculation `27`.
- Team identity / reference odds: Atlanta Braves were the road/upper favorite (`-113`, tick `188`) and Chicago White Sox were the home/lower underdog/even side (`-100`, tick `200`); protocol outcome is now `void_refunded` for both sides.
- Excluded: SEA/BAL contest `37` was created/verified on-chain (`0xd5f88f32d9ab68f528dc6351813586d48fa29d2f98c80a672398cc1b03b1d75f`) but was not in live scope after missing the safe window; no speculation was opened, nothing is locked, no postgame action is owed, and its costs are included in prep figures.

## What passed

- Release gate passed: frozen install, build, and smoke (`793` tests).
- NHL contest create/verify succeeded and NHL moneyline speculation opened via a tiny fully matched seed.
- Two-target dry-run selected exactly contests `38` and `39`, both `canQuote=true`, with `would-submit` only and errors total `0`.
- Live run posted four tiny commitments across the two allowed contests; evidence includes inline maker/taker odds ticks and team-at-site side details for each commitment.
- One controlled NHL fill landed: `0x4ae5d0a19614d5abe80cbc5784a429ee8121c277605062b4892bb25749eb80f0`.
- Fill was observed canonically from `own-state-stream`; no legacy canonical fill source was observed.
- Shutdown soft-cancelled the remaining live quotes; public/API open commitment exposure was zero for contests `38` and `39`; no orphan MM process remained.
- Fresh-state cold-start dry-run completed as a would-submit-only probe with errors total `0`.
- Postgame attempt 1 verified NHL official final: VGK `2`, CAR `4`; contest `39` was scored, speculation `28` settled with home/lower Carolina Hurricanes as winner, and maker/flow winner claims were confirmed.
- Postgame attempt 2 was read-only: NHL remained complete, MLB remained not final/scoreable, final claim-all dry-runs for the three controlled wallets were empty, and public/API exposure stayed zero.
- Postponed-game void/refund follow-up verified the 7-day cooldown elapsed, confirmed MLB gamePk `824589` still had the original `Postponed` / `Rain` row with feed/live pointing to the `2026-08-20T18:10:00Z` makeup, settled speculation `27` as `void`, and refunded both controlled seed positions risk-only (`0.050000` USDC each).

## Postgame attempt 1

- Checked: `2026-06-12T03:45:58Z` / `2026-06-11 22:45 CDT`.
- NHL score tx: `0x748a3e699fbc4c938f1a486ee765ce1adbfa25032edb4a1336bd28118185f10b`.
- NHL settle tx: `0x5d527556d6533c9de6809bb24e079703e720bb0ce622ae4ca39eeaacfcbbfa31`.
- NHL maker claim tx: `0xc7020e5dc49d02022767de3dc9e3e8bac500d0564c93e07657826e180ea929c2` for `0.084500` USDC (`84500` wei6), home/lower Carolina Hurricanes.
- NHL flow claim tx: `0xbe67332441816ed55d72cb0b5b4656b5f81c5bdf71116aee3229d78b803bc49f` for `0.100000` USDC (`100000` wei6), home/lower Carolina Hurricanes seed/open position.
- MLB gamePk `824589` was postponed for rain and rescheduled by MLB Stats API to `2026-08-20T18:10:00Z`; contest `38` / speculation `27` was not scored or settled in this attempt.

## Postgame attempt 2

- Checked: `2026-06-12T04:53:05Z` / `2026-06-11 23:53 CDT`.
- NHL official API still reports final/off: VGK `2`, CAR `4`; no new NHL transaction was needed.
- MLB Stats API feed/live now points to the scheduled makeup at `2026-08-20T18:10:00Z`; the schedule row for the original 2026-06-11 game remains `Postponed` / `Rain`, so contest `38` / speculation `27` was not scored, settled, or claimed.
- Speculation `27` locked funds are the tiny prep seed only: `0.050000` USDC on upper/away Atlanta held by `ospex-stage-maker-a` and `0.050000` USDC on lower/home Chicago White Sox held by `ospex-flow-a` (`0.100000` USDC total escrow), seed hash `0x633b523bbd4da612bc93dba9f66526adff9fd8486f5c62f1dbde49758a441a8d`.
- Final claim-all dry-runs for `ospex-stage-maker-a`, `ospex-stage-maker-b`, and `ospex-flow-a` were empty for completed/claimable work.
- Public/API commitment exposure remained zero for contests `38` and `39`; orphan MM process count remained `0`.
- Near-term duplicate postgame crons were removed after NHL completion and MLB postponement classification. A single void/refund follow-up cron is scheduled for `2026-06-18T23:45:00Z` / `2026-06-18 18:45 CDT`, five minutes after mainnet void eligibility (`2026-06-18T23:40:00Z`). Cron id: `1f8435fe7fbb`.


## Postponed-game void/refund follow-up

- Checked: `2026-06-18T23:51:37Z` / `2026-06-18 18:51:37 CDT`; mainnet void cooldown had elapsed from `2026-06-18T23:40:00Z`.
- MLB Stats API still showed the original gamePk `824589` row as `Postponed` / `Rain`; feed/live pointed to the scheduled makeup at `2026-08-20T18:10:00Z`. Contest `38` was **not** scored from the makeup.
- Void settle tx for speculation `27`: `0x8632a86660b681e932c5d6673875804594e5cdb81c2f2df371a80760ded0439b`; projected contest status `voided`, speculation status `closed`, `winSide=void`.
- `ospex-stage-maker-a` upper/away Atlanta seed claim: `0xe3599e6ab1a9de4306fd578084a48d29f275df65c3c68d03e6c2b4373095291c` for `0.050000` USDC (`50000` wei6).
- `ospex-flow-a` lower/home Chicago seed claim: `0xe866274484afd24367ef16b92ae53119f776868f8dae29fdad66c0037aaa9e99` for `0.050000` USDC (`50000` wei6).
- Final post-refund checks: public/API open commitment exposure for contest `38` was `0`; post-claim dry-runs for the two controlled seed wallets returned `0` entries; final controlled locked escrow for contest `38` is `0.000000` USDC.
- This completed the single deferred follow-up; no additional cron jobs were scheduled.

## Evidence scope notes

- `raw/live-telemetry.sanitized.ndjson` is a selected public-safe subset: `17` published NDJSON lines versus `24` canonical live telemetry events summarized in `raw/live-window.sanitized.json`.
- `raw/zero-exposure.sanitized.json` is scoped to target contests `38` and `39`; an unrelated controlled-wallet position on contest `34` is excluded from the public target-scope dump.

## Costs / budget

Combined same-evening controlled fees/seed/live risk: `4.284500` USDC. Operator gas through the live window: `1.707729091358687121` POL (`0.426932` USDC at the 0.25 reporting price). NHL postgame gas added `0.304275479007771818` POL (`0.076069` USDC at the same reporting price). MLB void/refund follow-up gas added `0.117444860779359179` POL (`0.029361` USDC). Combined estimate after full postgame/void follow-up gas: `4.816862` USDC, under the `5.00` USDC cap. LINK consumed: `0.020000` LINK total (`0.015000` for contest creates + `0.005000` for the NHL postgame score), reported separately. Void refunds returned `0.100000` USDC risk-only escrow (`0.050000` each); final controlled locked escrow for contest `38` is `0.000000` USDC.

## Caveats

- NHL official API initially returned 403 without browser-like headers; final official probes were `OFF` / `OK` with CAR `4`, VGK `2`.
- NHL postgame cleanup is complete for contest `39` / speculation `28`.
- MLB gamePk `824589` was postponed for rain and rescheduled to `2026-08-20T18:10:00Z`; ATL/CWS contest `38` / speculation `27` was not scored with the makeup and is now voided/refunded (`0.100000` USDC risk-only controlled refunds complete).
