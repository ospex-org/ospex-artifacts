# v0.7.1 MM live canary — NYM @ CIN contest 44

**Verdict:** GREEN_LIVE_WINDOW_POSTGAME_DEFERRED

The v0.7.1 live-window canary used primary target **New York Mets (away/upper/favorite) @ Cincinnati Reds (home/lower/underdog)**, contest `44`, speculation `33`. Fallback was not needed.

## Live-window result

- Stack: CLI/SDK `0.7.1`; ospex-market-maker `8389e11d53839941e998ad3686ca5eb05f50f905`; package and lockfile pinned to the v0.7.1 SDK tarball.
- Live maker: `mm-shakeout-maker-a` `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2`; clean before start.
- Controlled taker: `mm-shakeout-flow-a` `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494`.
- MLB status at start gate: `Pre-Game / Preview` before scheduled first pitch.
- Final MLB status at artifact cut: `Warmup / Live`; postgame remains deferred.
- Live runId: `2026-06-17T15-52-18-226Z-o7vnzx`.
- Live commitments posted: `10` tiny 0.10 USDC-risk quotes over the bounded live loop, all contest 44/speculation 33.
- Controlled fill: commitment `0x7818744c708eb986aefcfe7ec70913821652bd061268f61287f0a78b22a6662b`, tx `0x7d8ad8dc09db574e7b4ab1e713d8b1ff16b2df9dc0e0bc73335bb090849273cc`, receipt status `0x1`.
- MM fill detection: telemetry `kind=fill`, `source=own-state-stream`, `newFillWei6=81300`.
- Shutdown: KILL file requested at 2026-06-17T16:07:01Z; process exited within 4s.
- Final public/API/MM visible-open exposure: zero.

## Costs

- Taker USDC delta: `-0.099999`.
- Maker USDC delta: `-0.0813`.
- Match gas: `0.11844371715787931` POL.
- Controlled run stayed within the ≤ $5 cap.

## Postgame deferred

After official MLB final: score contest 44, settle speculation 33, claim winning maker/taker positions, then update or supersede this artifact to `FULL_GREEN` if earned.
