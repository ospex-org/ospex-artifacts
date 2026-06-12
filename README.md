# Ospex Artifacts

Ospex Artifacts is a public repository of sanitized protocol evidence and derived activity records.

Artifacts are generated from public chain data, approved external facts, and sanitized indexer/API snapshots. JSON files are the machine-readable source for agents, dashboards, and other consumers. Markdown files are evidence-grade renderings of the same facts.

This repository intentionally avoids internal planning notes, brainstorming text, private operator material, and promotional language. It should read like an evidence/data product: boring, durable, precise.

## Artifact classes

- `runs/` — per-contest, per-market, or multi-contest lifecycle evidence bundles.
- `releases/` — release acceptance evidence for SDK/CLI or service versions, including fresh-install gates and bounded live gates where applicable.
- `daily/` — daily protocol activity digests. This class is reserved for future rollups generated from run/release evidence, chain data, and sanitized snapshots. Track every UTC calendar day, including zero-activity days.
- `index.json` — a lightweight artifact index for agents, dashboards, and humans that need a stable entry point.
- `archive/` — full-history index shards such as `archive/2026/index.json`; consumers fetch these only when they need older entries.

See `docs/artifact-types.md` for the current conventions and `docs/test-harness-expectations.md` for live-write harness expectations. Market-maker live canary runs publish a standardized scenario matrix and MVE readiness scorecard; see `docs/mm-live-canary-evidence.md` and the templates under `templates/mm-live-canary/`.

## Source-of-truth rule

For each artifact, the canonical facts live in JSON:

- `evidence.json` for `runs/`
- `acceptance.json` for `releases/`
- `digest.json` for future `daily/` artifacts

Schema-backed JSON files include a top-level `$schema` pointer into `schemas/`. After adding, removing, or editing an artifact, run `python3 scripts/generate-indexes.py` to refresh `index.json` and `archive/YYYY/index.json` shards, then run `python3 scripts/validate-artifacts.py` locally before publishing. GitHub Actions runs the same JSON-parse, schema/status, path-existence, generated-index, archive, and public-safety checks on every PR and `main` push.

Markdown summaries are presentation files only in the sense that they render canonical JSON facts. They should stay evidence-grade: complete, technical, and faithful to JSON/raw sanitized inputs. Friendly headlines, audience-specific framing, and scrollable gloss belong in the frontend/dashboard translation layer, not in the artifact itself.

## Public artifact rules

Include:

- network and chain context
- contest, speculation, commitment, and release identifiers
- public wallet addresses and role labels where useful
- tx hashes, receipt summaries, and explorer links
- final-score or external fact source references
- sanitized API/indexer snapshots
- test gates, lifecycle checks, post-write projection convergence checks, observations, and caveats

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

Top-level index and archive shards:

```text
index.json
archive/YYYY/index.json
```

`index.json` contains `latestByArtifactType`, a bounded `recentArtifacts` feed window sorted by `publishedAt`, and pointers to archive shards. Full history lives in `archive/`, so consumers do not need to fetch an unbounded top-level array to find the newest artifact. Generate the index files with:

```bash
python3 scripts/generate-indexes.py
```

The generator discovers canonical artifact JSON files under `runs/`, `releases/`, and `daily/`, preserves existing entry `publishedAt` values, assigns the current UTC time to newly discovered artifacts, and keeps archive shard counts plus oldest/newest summaries in sync.

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
