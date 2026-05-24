# MM post-D1/D2 partial-fill smoke report

Run dir: `[REDACTED_LOCAL_PATH]
Worktree: `work/ospex-market-maker`
Config: `ospex-mm.yaml`

## Target

- Contest: `21`
- Game: Texas Rangers @ Los Angeles Angels, 2026-05-24 — MLB
- Speculation: `12` moneyline
- Maker: `ospex-stage-maker-a` / `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Taker for controlled fill: `ospex-flow-a` / `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

## Live evidence

- Seed commitment hash: `0x1a79ac4d2b28b49b9efba9df91c0c8eff0ac32faf0923aa2af4c0f72eca23b52`
- Seed match tx: `0x793dd7f35538427fd0547ad0eeef5b2678914651be4fac4decc56a2f01cb9640`
- Live MM run id: `2026-05-23T23-19-28-312Z-5lebzc`
- Live telemetry: `telemetry/run-2026-05-23T23-19-28-312Z-5lebzc.ndjson`
- Controlled partial-fill target hash: `0x05879daacb266b498028c511ba51b71644337081f9c32e84049f16328df2373d`
- Controlled partial-fill tx: `0x4a48490762ce8599beb23cfadbc69b6ca066202577c3ca3ef62a585648d26614`
- Controlled fill size:
  - Taker risk: `0.030000` USDC / `30000` wei6
  - Maker filled risk: `0.037500` USDC / `37500` wei6

## Final safety checks

- Hermes tracked background processes: none.
- Visible maker commitments for contest `21`: `0`.
- Contest `21` speculation `12` orderbook rows: `0`.
- MM status visibleOpen: `0`.
- MM status active positions: `1`, own risk `37500` wei6.
- Telemetry summary: `fill=1`, `submit=2`, `replace=2`, `soft-cancel=2`, `onchain-cancel=0`, `error=0`, `kill=2`.
- No write-like events after the observed fill (`submit`, `replace`, `soft-cancel`, `onchain-cancel`, etc. count after fill: `0`).

## Unexpected / not clean-green

1. The first controlled fill attempt raced a stale replacement: the original target hash was already cancelled by the MM before the taker match command executed.
2. The second controlled fill succeeded on-chain, but the MM had already off-chain soft-cancelled that hash before the position poll observed the fill. Telemetry sequence for the filled hash:
   - `23:20:33.649Z` `replace` created `0x05879d...373d`
   - `23:21:35.524Z` `soft-cancel` on `0x05879d...373d` with reason `side-not-quoted`
   - `23:22:06.132Z` `fill` from `position-poll`, maker side `away`, `newFillWei6=37500`
3. Because the fill was discovered through `position-poll` after the off-chain soft-cancel, the retained-partial/on-chain-cancel path was not exercised:
   - `partial-remainder-retained`: `0`
   - `onchain-cancel`: `0`
4. `commitments show 0x05879d...373d` reports `status=cancelled`, `filledRiskAmount=0`, `remainingRiskAmount=250000`, `isLive=false` even though the match tx confirmed and MM state has the maker position. This is an API/local-bookkeeping mismatch to investigate.
5. `mm status` still reports the four stopped-before-expiry records as stored `softCancelled`; public/API exposure is clean, but the local lifecycle is not a clean terminal state.

## Artifact eligibility

Not clean-green for acceptance promotion. The live window is operationally safe/closed, and it produced useful public-safe evidence, but this should be recorded as an amber/red investigation artifact rather than a green D1/D2 acceptance artifact. The specific follow-up is the soft-cancel-before-position-poll race and the lack of retained-partial/on-chain-cancel exercise in this run.
