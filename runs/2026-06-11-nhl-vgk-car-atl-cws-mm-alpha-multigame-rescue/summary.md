# NHL VGK-CAR + MLB ATL-CWS ospex-market-maker v0.1.0-alpha.1 multigame rescue

Status: **complete_verified_with_caveats** / live-window green, postgame deferred.

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

## Costs / budget

Combined same-evening controlled fees/seed/live risk: `4.284500` USDC. Operator gas: `1.707729091358687121` POL, reported as `0.426932` USDC at the 0.25 reporting price. Combined estimate: `4.711432` USDC, under the `5.00` USDC cap. LINK consumed: `0.015000` LINK, reported separately.

## Caveats

- NHL official API initially returned 403 without browser-like headers; a later official probe showed `PRE` / `OK` before the official start cutoff.
- NHL is configured but less recently tested than MLB.
- Postgame cleanup is still required for NHL contest `39` / speculation `28` and ATL/CWS contest `38` / speculation `27`.
