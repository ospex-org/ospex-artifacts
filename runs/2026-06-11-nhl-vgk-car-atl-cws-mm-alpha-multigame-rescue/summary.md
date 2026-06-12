# NHL VGK-CAR + MLB ATL-CWS ospex-market-maker v0.1.0-alpha.1 multigame rescue

Status: **complete_verified_with_caveats** / live-window green; NHL postgame complete; MLB postponed/deferred after attempt 2.

This artifact records a low-value two-target rescue canary on Polygon using `ospex-market-maker` `v0.1.0-alpha.1` at `af1bb107af47dc80f27485dee7417ca95b782b50` with the repo-pinned `@ospex/sdk` `v0.6.2`.

## Targets

- NHL: Vegas Golden Knights @ Carolina Hurricanes, NHL game `2025030415`, Ospex game `12fcb924-bfbe-4fac-b447-af05b8c9c3e1`, contest `39`, speculation `28`.
- MLB: Atlanta Braves @ Chicago White Sox, MLB gamePk `824589`, contest `38`, speculation `27`.
- Excluded: SEA/BAL contest `37` was not in live scope after missing the safe window.

## What passed

- Release gate passed: frozen install, build, and smoke (`793` tests).
- NHL contest create/verify succeeded and NHL moneyline speculation opened via a tiny fully matched seed.
- Two-target dry-run selected exactly contests `38` and `39`, both `canQuote=true`, with `would-submit` only and errors total `0`.
- Live run posted four tiny commitments across the two allowed contests.
- One controlled NHL fill landed: `0x4ae5d0a19614d5abe80cbc5784a429ee8121c277605062b4892bb25749eb80f0`.
- Fill was observed canonically from `own-state-stream`; no legacy canonical fill source was observed.
- Shutdown soft-cancelled the remaining live quotes; public/API open commitment exposure was zero for contests `38` and `39`; no orphan MM process remained.
- Fresh-state cold-start dry-run completed as a would-submit-only probe with errors total `0`.
- Postgame attempt 1 verified NHL official final: VGK `2`, CAR `4`; contest `39` was scored, speculation `28` settled with `home/lower` as winner, and maker/flow winner claims were confirmed.
- Postgame attempt 2 was read-only: NHL remained complete, MLB remained not final/scoreable, final claim-all dry-runs for the three controlled wallets were empty, and public/API exposure stayed zero.

## Postgame attempt 1

- Checked: `2026-06-12T03:45:58Z` / `2026-06-11 22:45 CDT`.
- NHL score tx: `0x748a3e699fbc4c938f1a486ee765ce1adbfa25032edb4a1336bd28118185f10b`.
- NHL settle tx: `0x5d527556d6533c9de6809bb24e079703e720bb0ce622ae4ca39eeaacfcbbfa31`.
- NHL maker claim tx: `0xc7020e5dc49d02022767de3dc9e3e8bac500d0564c93e07657826e180ea929c2` for `0.084500` USDC (`84500` wei6).
- NHL flow claim tx: `0xbe67332441816ed55d72cb0b5b4656b5f81c5bdf71116aee3229d78b803bc49f` for `0.100000` USDC (`100000` wei6).
- MLB gamePk `824589` was postponed for rain and rescheduled by MLB Stats API to `2026-08-20T18:10:00Z`; contest `38` / speculation `27` was not scored or settled in this attempt.

## Postgame attempt 2

- Checked: `2026-06-12T04:53:05Z` / `2026-06-11 23:53 CDT`.
- NHL official API still reports final/off: VGK `2`, CAR `4`; no new NHL transaction was needed.
- MLB Stats API feed/live now points to the scheduled makeup at `2026-08-20T18:10:00Z`; the schedule row for the original 2026-06-11 game remains `Postponed` / `Rain`, so contest `38` / speculation `27` was not scored, settled, or claimed.
- Final claim-all dry-runs for `ospex-stage-maker-a`, `ospex-stage-maker-b`, and `ospex-flow-a` were empty.
- Public/API commitment exposure remained zero for contests `38` and `39`; orphan MM process count remained `0`.
- Later duplicate crons were left in place because MLB is still deferred.

## Costs / budget

Combined same-evening controlled fees/seed/live risk: `4.284500` USDC. Operator gas through the live window: `1.707729091358687121` POL (`0.426932` USDC at the 0.25 reporting price). NHL postgame gas added `0.304275479007771818` POL (`0.076069` USDC at the same reporting price). Combined estimate after NHL postgame gas: `4.787501` USDC, under the `5.00` USDC cap. LINK consumed: `0.015000` LINK, reported separately. Attempt 2 sent no transactions and added no gas.

## Caveats

- NHL official API initially returned 403 without browser-like headers; final official probes were `OFF` / `OK` with CAR `4`, VGK `2`.
- NHL postgame cleanup is complete for contest `39` / speculation `28`.
- MLB gamePk `824589` was postponed for rain and rescheduled to `2026-08-20T18:10:00Z`; ATL/CWS contest `38` / speculation `27` remains verified/open and requires a future makeup-final or eligible void/refund continuation.
