# MIL/ATH contest 33 v0.6.0 own-state SSE retirement-gate soak — FAIL evidence

**Status:** `fail_blocked` / RED retirement-gate evidence. Do **not** open the OS-Phase 4 polling-retirement PR from this run.

## Verdict

The v0.6.0 live soak exercised the required live SSE surfaces with both observers running, but the gate did not finish GREEN. The blocking discrepancy is the final full-soak operator watch summary:

- full-soak `own-state watch` summary: `readyObserved=true`, `lastStatus=connected`, `liveCommitmentCount=8`, `error=0`, `lines_after_summary=0`.
- final public reads immediately after shutdown/drain: maker visible commitments `0`; speculation orderbook `[]`.
- fresh post-drain `own-state watch --until-ready`: `liveCommitmentCount=0`.

Interpretation: actual public/current state drained to zero, but the long-running operator watcher retained eight expired/hidden items in its summary live-set accounting. The scenario requires the full-soak watch `summary.liveCommitmentCount == 0`, so this run is RED.

## Target

- Game: Milwaukee Brewers @ Athletics
- Contest id: `33`
- Speculation id: `23`
- Market: moneyline
- Start: `2026-06-10T02:05:00Z`
- Team identity: away / Milwaukee Brewers; home / Athletics. Reference odds during the run treated Athletics as slight favorite and Milwaukee Brewers as underdog by implied probability.
- Maker: `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`

## Runtime

- CLI / SDK: `0.6.0`
- MM SDK pin: v0.6.0 release tarball
- MM commit used locally: `1d9bc94`
- Own-state subscription: enabled
- Slow audit polling: configured at `60000 ms`

## Covered events

- Cold-start operator watch: `snapshot → ready` at `2026-06-09T17:45:29Z`.
- Normal visible fill: commitment `0x6c6632f70c87714e3fe7e75bb9158ec5eec68f8176fe653c1f5dbbd1d513a068`, watch tx/log `0xaa65c8861541ac70624ff0691fa8ca4b1f85e01763a246d39e741e505d12f46f/1194`, MM source `own-state-stream`, `newFillWei6=200000`.
- Partial fill: commitment `0x26e57de0349351975f926ccdf31babec3d4d4950745b1adf031c49c1c13643bb`, watch tx/log `0x9d362fcae43533ed2558a2a3553b86bdae0f71c85e80a606a63f859ff2245c5a/1061`, MM source `own-state-stream`, `newFillWei6=46200`.
- Hidden/soft-cancel recovery: operator watch observed hidden commitments with `signedPayloadPresent=true`; final authoritative on-chain cancel cleared the last four stale records.
- Expiry/replacement: MM telemetry recorded `replace=9` and `expire=8`.
- Reconnect/degraded: MM telemetry recorded `degraded` / `stream-degraded` at `2026-06-09T17:51:02Z`; duplicate-fill checks remained clean.
- Restart/resume: MM restarted with the persisted state directory; telemetry recorded `stream-cold-restart` reason `resume-without-baseline`, health hold entered then cleared, and no duplicate fills were emitted.
- Score/settle/claim: deferred because the target game had not started during this run window.

## Blocking evidence

- `raw/own-state-watch.ndjson`: full-soak observer; final summary has `liveCommitmentCount=8`.
- `raw/final-safety-state.sanitized.json`: public/current zero-state proof plus the watch-summary mismatch.
- `raw/final-fresh-watch-until-ready.ndjson`: fresh post-drain snapshot with `liveCommitmentCount=0`.

## Final safety state

- `ospex commitments list --maker <maker> --speculation 23 --json`: payload `[]`.
- `ospex commitments list --speculation 23 --json`: payload `[]`.
- `ospex speculations show 23 --json`: `orderbook: []`.
- Final MM/watch process scan: `0` matching processes.
- Full-soak watch emitted no line after summary.

## Budget / cost

- New matched maker risk observed in MM fills: `0.246200 USDC` (`0.200000 + 0.046200`).
- Cumulative maker positions observed by MM after setup/fills: `0.346200 USDC`.
- Authoritative cancel gas observed by MM telemetry plus final cancel-stale rollup: `0.213479922538710620 POL` (`213479922538710633` wei).
- Budget cap: `≤ 5 USDC`; run stayed within the controlled tiny sizing envelope.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
