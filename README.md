# Ospex Artifacts

Ospex Artifacts is a public repository of sanitized protocol evidence and derived activity records.

Artifacts are generated from public chain data, approved external facts, and sanitized indexer/API snapshots. JSON files are the machine-readable source for agents, dashboards, and other consumers. Markdown files are human-readable renderings of the same facts.

This repository intentionally avoids internal planning notes, brainstorming text, private operator material, and promotional language. It should read like an evidence/data product: boring, durable, precise.

## Artifact classes

- `runs/` — per-contest, per-market, or multi-contest lifecycle evidence bundles.
- `releases/` — release acceptance evidence for SDK/CLI or service versions, including fresh-install gates and bounded live gates where applicable.
- `daily/` — daily protocol activity digests. This class is reserved for future rollups generated from run/release evidence, chain data, and sanitized snapshots.
- `index.json` — a lightweight artifact index for agents, dashboards, and humans that need a stable entry point.

See `docs/artifact-types.md` for the current conventions.

## Source-of-truth rule

For each artifact, the canonical facts live in JSON:

- `evidence.json` for `runs/`
- `acceptance.json` for `releases/`
- `digest.json` for future `daily/` artifacts

Markdown summaries are presentation files. They should not introduce facts that are absent from the corresponding JSON or raw sanitized inputs.

## Public artifact rules

Include:

- network and chain context
- contest, speculation, commitment, and release identifiers
- public wallet addresses and role labels where useful
- tx hashes, receipt summaries, and explorer links
- final-score or external fact source references
- sanitized API/indexer snapshots
- test gates, lifecycle checks, observations, and caveats

Exclude:

- private keys
- password files
- RPC URLs or API secrets
- raw environment files
- raw signatures unless deliberately required for reproducibility
- unredacted logs, telemetry dumps, local paths, or operator scratch files
- internal planning, roadmap discussion, or promotional copy

See `docs/publication-rules.md` for the full publication checklist.

## Published artifacts

Runs:

- `runs/2026-05-19-mlb-atl-mia-contest-13/` — single-game Braves @ Marlins market-maker lifecycle artifact.
- `runs/2026-05-20-mlb-three-game-mm-shakeout-contests-14-16/` — three-game MLB market-maker shakeout across contests 14, 15, and 16.

Releases:

- `releases/v0.3.0/2026-05-22-mlb-hou-chc-release-acceptance/` — SDK/CLI `v0.3.0` public release acceptance against a fresh install and bounded live contest-create path.

Daily digests:

- none published yet.

## Directory conventions

Run artifacts:

```text
runs/YYYY-MM-DD-sport-away-home-contest-<id>/
  summary.md
  evidence.json
  raw/
    indexer-snapshot.sanitized.json
    tx-receipts.summary.json
    final-score-source.json
```

Release acceptance artifacts:

```text
releases/v<version>/YYYY-MM-DD-<scope>-release-acceptance/
  acceptance.md
  acceptance.json
  raw/
    release-assets.json
    setup-gates.json
    live-gates.json
    tx-receipts.summary.json
```

Future daily artifacts:

```text
daily/YYYY-MM-DD/
  digest.json
  summary.md
  raw/
```

Each artifact should be reproducible from public chain data plus the recorded sanitized inputs, or should explicitly state which gate or input was not available.
