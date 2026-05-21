# Ospex Artifacts

This directory is a staging home for public-safe Ospex lifecycle artifacts: evidence runs, scorecards, agent reports, dashboard-ready JSON, and future public proofs.

## Recommended long-term home

Use a dedicated repo: **`ospex-org/ospex-artifacts`**.

Do **not** keep these primarily in `ospex-sdk`.

`ospex-sdk` should stay focused on package source, SDK/CLI docs, tests, release notes, and public API contracts. Artifacts are protocol/operations/scorecard records; they cut across contracts, API, indexer, SDK, market-maker, and website. Putting them in the SDK repo would blur ownership and can accidentally ship operational history in package/release surfaces.

Recommended long-term structure:

- Dedicated repo: `ospex-org/ospex-artifacts`
- Website/dashboard consumes generated JSON from that repo
- SDK/MM docs link to selected artifacts, but do not own them

## Public artifact rules

Include:

- tx hashes and explorer links
- public wallet addresses, preferably labeled
- contest/speculation/commitment IDs
- final score sources
- sanitized API/indexer snapshots
- summarized MM telemetry and operator conclusions
- known caveats/product debt

Exclude:

- private keys
- password files
- RPC URLs or API secrets
- raw signatures unless deliberately needed for reproducibility
- raw environment files
- noisy unredacted logs

## Published runs

- `runs/2026-05-19-mlb-atl-mia-contest-13/` — single-game Braves @ Marlins MM lifecycle artifact.
- `runs/2026-05-20-mlb-three-game-mm-shakeout-contests-14-16/` — three-game MLB MM shakeout across contests 14, 15, and 16.

## Directory convention

```text
runs/YYYY-MM-DD-sport-away-home-contest-<id>/
  summary.md
  evidence.json
  raw/
    indexer-snapshot.sanitized.json
    tx-receipts.summary.json
    final-score-source.json
```

Multi-contest artifacts may use a descriptive slug such as `YYYY-MM-DD-sport-three-game-mm-shakeout-contests-<start>-<end>` and include extra sanitized raw summaries.

Each artifact should be reproducible from public chain data plus sanitized indexer/API snapshots.
