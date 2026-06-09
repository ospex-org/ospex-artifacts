# Scenario matrix

| ID | Scenario | Status | Evidence | Notes |
|---|---|---:|---|---|
| `runtime-v060` | SDK/CLI/MM v0.6.0 alignment | `pass` | `evidence.json, raw/mm-config-summary.sanitized.json` | Released CLI/SDK v0.6.0 and MM v0.6.0 pin used. |
| `observers` | Operator watch and MM own-state observer live | `pass` | `raw/own-state-watch.ndjson, raw/mm-telemetry-summary.sanitized.json` | Operator watch snapshot→ready; MM telemetry with ownState.subscribe=true and slow audit polling configured. |
| `cold-start` | Cold-start snapshot→ready | `pass` | `raw/own-state-watch.ndjson` | Full-soak watch emitted snapshot and ready at 2026-06-09T17:45:29Z. |
| `visible-fill` | Normal visible fill | `pass` | `raw/mm-telemetry-summary.sanitized.json` | Commitment 0x6c66… filled once; MM source own-state-stream; watch tx/log 0xaa65…/1194. |
| `partial-fill` | Partial fill | `pass` | `raw/mm-telemetry-summary.sanitized.json` | Commitment 0x26e5… partial fill newFillWei6=46200; no duplicate telemetry. |
| `hidden-soft-cancel` | Soft-cancel/hidden recovery | `pass_with_caveat` | `raw/own-state-extract.sanitized.ndjson` | Watch observed hidden cancelled commitments with signedPayloadPresent=true and later terminal on-chain cancellation; simultaneous anonymous hidden-read probe was not captured. |
| `expiry-replacement` | Expiry/replacement lifecycle | `pass` | `raw/mm-telemetry-summary.sanitized.json` | MM emitted replacement and expiry telemetry across short-lived quotes. |
| `reconnect` | Reconnect/degraded catchup without duplicate fill | `pass` | `raw/mm-telemetry-summary.sanitized.json` | Stream-degraded event observed at 17:51:02Z; no duplicate fills across the run. |
| `restart-resume` | MM restart/resume from persisted cursor | `pass_with_caveat` | `raw/mm-telemetry-summary.sanitized.json` | Restart reused state/cursor, then emitted stream-cold-restart reason=resume-without-baseline; health hold cleared and no duplicate fill telemetry. |
| `lifecycle-terminal` | Score→settle→claim or terminal position lifecycle | `deferred` | `raw/final-speculation-23.sanitized.json` | Target game MIL/ATH starts 2026-06-10T02:05Z, outside this run window; positions remained active. |
| `divergence` | Zero persistent audit divergence | `fail` | `raw/final-safety-state.sanitized.json` | Actual public/orderbook/fresh watch state was zero, but full-soak operator watch summary reported liveCommitmentCount=8 after drain. |
| `duplicate-fills` | No duplicate fill telemetry | `pass` | `raw/mm-telemetry-summary.sanitized.json` | Watch tx/log keys and MM commitment fill keys unique. |
| `position-monotonic` | No backwards position transition | `pass` | `raw/mm-telemetry-summary.sanitized.json` | Only active positionStatus events observed; no backwards rank transition detected. |
| `post-summary` | No direct state mutation after summary | `pass` | `raw/final-safety-state.sanitized.json` | 0 lines after operator-watch summary. |
| `final-drain` | Drain to zero and no orphaned processes | `fail` | `raw/final-safety-state.sanitized.json` | No orphaned processes and public/fresh state zero, but full-soak watch summary liveCommitmentCount=8, failing the scenario final row. |
| `public-safety` | Public artifact safety scan | `pass` | `raw/validation-scan.json` | No signatures/secrets detected by artifact scan. |
