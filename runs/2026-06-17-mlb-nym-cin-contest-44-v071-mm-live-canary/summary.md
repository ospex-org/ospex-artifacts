# v0.7.1 MM live canary — NYM @ CIN contest 44

**Verdict:** FULL_GREEN

The v0.7.1 canary used **New York Mets (away/upper/favorite) @ Cincinnati Reds (home/lower/underdog)**, contest `44`, speculation `33`. The live window posted bounded quotes, executed exactly one controlled live fill, then postgame completed after the official final score **New York Mets 9, Cincinnati Reds 1**.

## Live-window result

- Stack: CLI/SDK `0.7.1`; ospex-market-maker `8389e11d53839941e998ad3686ca5eb05f50f905`; package and lockfile pinned to the v0.7.1 SDK tarball.
- Live maker: `mm-shakeout-maker-a` `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2`; clean before start.
- Controlled taker: `mm-shakeout-flow-a` `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494`.
- Live runId: `2026-06-17T15-52-18-226Z-o7vnzx`.
- Controlled fill: commitment `0x7818744c708eb986aefcfe7ec70913821652bd061268f61287f0a78b22a6662b`, tx `0x7d8ad8dc09db574e7b4ab1e713d8b1ff16b2df9dc0e0bc73335bb090849273cc`.
- Own-state evidence: telemetry recorded `kind=fill`, `source=own-state-stream`, `newFillWei6=81300`.
- Live shutdown: KILL requested at 2026-06-17T16:07:01Z; process exited within 4s; final visible-open exposure was zero.

## Postgame lifecycle

- Official score source: MLB Stats API, final score New York Mets 9, Cincinnati Reds 1.
- Score tx: `0xec13a28e3fb6b1ca8ee2d8a66bb413a329be39cebc09857e348cfd486cde82de`.
- Settle tx: `0xc5a9d1b68781b519484f903debdd179c6ffcf308fc1001cbc695519a143b957e`; speculation 33 settled to away/upper/New York Mets.
- Claim tx, live-fill winner `mm-shakeout-flow-a`: `0x2e5d50bec4b618768c6193fcbe9cdddffd9e3813f2090cb9b50f6f3c9c5141c1`, payout `0.181299` USDC.
- Claim tx, setup seed/open winner `ospex-stage-maker-b`: `0x390cf95777650673d2971377ca1914dc27274039610921bf9d860ffc942818e9`, payout `0.100000` USDC.
- Losing lower/Cincinnati positions for `mm-shakeout-maker-a` and `ospex-fresh-user` are no-op/not claimable.

## Final checks

- Final claim-all dry-runs for maker, taker, seed maker, seed taker, and score operator returned zero entries.
- Public/API visible commitments: contest 44 `0`, contest 44/spec 33 `0`, live maker `0`.
- Speculation orderbook count: `0`.
- No orphan live MM process.
- Target active/claimable/pending-settle positions: `0` after score/settle/claim.

## Costs

- Live match gas: `0.11844371715787931` POL.
- Postgame gas: `0.301607157976180114` POL.
- Total tracked gas: `0.420050875134059424` POL.
- Live taker risk: `0.099999` USDC; live winning payout: `0.181299` USDC.
- Setup seed/open winning payout: `0.100000` USDC.

## Caveats

- Restart/cold-start probe was not run for this canary; final zero-exposure and process checks were run instead.
- CLI `speculations show` omitted `winSide`/`settledAt` at final read, but indexer/projection target state shows `win_side=away` and `settled_at` populated.
