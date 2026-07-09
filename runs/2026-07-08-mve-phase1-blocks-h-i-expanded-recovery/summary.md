# Ospex MVE Phase 1 Blocks H/I — 2026-07-08 partial artifact

Generated: 2026-07-09T00:11:16Z

This is a facts-only **partial** artifact published before the combined H/I postgame zero-state marker exists. It documents the live-window result and the harness failure/fix so the day is not lost; the same PR is expected to be updated after score/settle/claim/zero-state completes.

## Current wrap-up status

- Postgame complete marker: not present yet.
- Pending final/postgame labels at publication: A, B, C, D, E, F.
- Postgame watcher remains active: cron `8629ab6e6847`.
- Artifact update watcher remains active: cron `525111bc1891`.

## Block H

- Contest: `35` Toronto Blue Jays @ San Francisco Giants.
- Setup/manual fills: 3.
- Live MM submit events: 6.
- Controlled live fills: 2.
- Live zero-open after shutdown: `True`.

## Block I

- Contests: A=29, B=30, C=31, D=32, E=33, F=34.
- Setup/manual fills: 18 tiny fills across six contests / 18 markets.
- Live MM quotes posted: 0.
- Live controlled fills: 0.
- Live tx sent: no.
- Live classification: `AMBER_PRELIVE_GATE_HALT`.
- p1 dry replay under fixed harness: `GO_WITH_CAVEATS` with expected 18, actual 14, two `reference-line-mismatch` total skips, fatal events 0.

## Why publish this partial artifact

The useful artifact value is documenting the operator harness failure and the fixed replay result without claiming postgame completion. It should make review/merge possible for the live-window facts while preserving the later zero-state update path.
