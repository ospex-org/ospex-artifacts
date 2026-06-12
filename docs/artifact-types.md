# Artifact Types

This repository publishes public-safe Ospex artifacts in a small number of stable classes. The classes can evolve, but each artifact should be explicit about what it proves and what it does not prove.

## Common rules

Every artifact class should follow these rules:

1. JSON is the source of truth.
2. Markdown is an evidence-grade rendering of JSON facts. It should stay complete, technical, and faithful rather than becoming dashboard or marketing copy.
3. Raw inputs are sanitized before publication.
4. Artifact-level `status` values use the controlled vocabulary below. Gate-level statuses such as `pass`, `fail`, `not_run`, and `not_available` remain local to the gate object.
5. Observations and caveats are factual and test-scoped. They should not contain internal planning language.
6. Wallet labels are role labels unless a public identity is intentionally part of the artifact.
7. Schema-backed JSON files include a top-level `$schema` pointer to the matching file under `schemas/` and are validated by `python3 scripts/validate-artifacts.py`.
8. Live-write artifacts distinguish transaction receipt success from API/indexer projection convergence. The harness should wait for the projection target before final assertions; one stale immediate read is a projection-lag observation, not a final failure, if convergence passes inside the documented window.
9. Frontend/dashboard prose can translate artifact facts into friendlier headlines, but that translation belongs outside the artifact and should link back to the source JSON/Markdown.

## Status vocabulary

Dashboards and agents may switch on artifact-level `status`, so it is intentionally constrained.

- `run` (`runs/`): `complete_verified`, `complete_verified_with_caveats`, `partial`, `superseded`
- `release-acceptance` (`releases/`): `stage0_green`, `stage0_green_with_caveats`, `stage0_partial`, `stage0_failed`, `superseded`
- `daily-digest` (`daily/`): `complete`, `complete_with_caveats`, `partial`, `superseded`

These are artifact-level statuses only. Individual check/gate fields can use their own local values, for example `pass`, `fail`, `not_run`, or a version string when the gate records an observed value.

## `runs/` — lifecycle evidence

`runs/` artifacts record a completed protocol or market-maker lifecycle for one or more contests. (Runs adopting the MVE scorecard cover exactly one contest/speculation each — see `docs/mm-live-canary-evidence.md`.)

Typical files:

```text
runs/<artifact-id>/
  summary.md
  evidence.json
  raw/
    indexer-snapshot.sanitized.json
    tx-receipts.summary.json
    final-score-source.json
```

Typical facts:

- network and contest identifiers
- speculation and side semantics
- commitment hashes and fill transactions
- score, settle, and claim transactions
- position outcomes and realized PnL where applicable
- quote-window or market-maker telemetry summaries
- final claim/dry-run checks
- post-write projection convergence gates for fill, score, settle, and claim writes when those steps are in scope
- known caveats observed during the run

A run artifact may be `complete_verified`, `complete_verified_with_caveats`, `partial`, or `superseded`. Caveats are part of the record; they do not make an artifact invalid by default.

Market-maker live canary runs additionally publish a schema-backed scenario matrix and MVE readiness scorecard with a controlled verdict vocabulary; see `docs/mm-live-canary-evidence.md` and the templates under `templates/mm-live-canary/`.

## `releases/` — release acceptance evidence

`releases/` artifacts record acceptance checks for a public SDK/CLI or service version. These artifacts are separate from lifecycle runs because a release acceptance may only prove installability, read-only behavior, approvals, contest creation, or another bounded path.

Typical files:

```text
releases/v<version>/<artifact-id>/
  acceptance.md
  acceptance.json
  raw/
    release-assets.json
    setup-gates.json
    live-gates.json
    tx-receipts.summary.json
```

Recommended release acceptance facts:

- release repository, tag, URL, publish timestamp, and asset hashes
- fresh-install environment and package source
- version/help/read-only smoke gates
- audit and package-integrity gates when applicable
- signer/auth/doctor readiness gates
- bounded approvals and live transaction gates when applicable
- tx receipt summaries for live gates
- post-action state checks, including post-write API/indexer projection convergence when live write gates are in scope
- explicit `not_run` status for optional tests that were not part of the acceptance scope

For example, the `v0.3.0` acceptance path records a fresh install from GitHub release tarballs, read-only CLI smoke checks, signer readiness, bounded LINK/USDC approvals, contest creation, Chainlink verification, and post-create readiness observations. It does not claim to prove a full market lifecycle unless a fill, score, settlement, and claim path are also present.

## `daily/` — daily protocol activity digests

`daily/` is reserved for daily rollups. These artifacts should be generated from chain/indexer data, sanitized snapshots, and already-published run/release artifacts.

Planned files:

```text
daily/YYYY-MM-DD/
  digest.json
  summary.md
  raw/
```

Recommended daily digest properties:

- summarize every UTC calendar day, including zero-activity days
- represent zero-activity days explicitly with zero counts, empty artifact references, and verified coverage/provenance rather than omitting the day
- record block range and snapshot provenance
- report protocol metrics with prior-calendar-day deltas
- link to the per-contest run artifacts instead of duplicating their evidence
- include sample sizes with wallet performance metrics
- mark wallet classification as best-effort when present
- keep forward-looking fields optional and non-load-bearing

The first daily schema should be based on repeated MVE data rather than speculative fields. Consumers should ignore unknown fields.

## `index.json` — repository index

`index.json` is a lightweight entry point for agents, dashboards, and humans. It contains a bounded recent feed window, latest pointers, and archive pointers, not the full unbounded artifact history.

Index conventions:

- `latestByArtifactType` keys exactly mirror `artifactType` values: `run`, `release-acceptance`, and `daily-digest`. Consumers do not need a pluralization or directory-name lookup table.
- `recentArtifacts` is the recent-N feed window and is sorted by `publishedAt` descending.
- Every index/archive entry has `publishedAt` for feed ordering. The `date` field remains the subject calendar date and must not be used as the primary sort key.
- `archiveIndexes` points to full-history archives such as `archive/2026/index.json`. Consumers fetch those only when they need older entries.
- Run `python3 scripts/generate-indexes.py` after artifact changes. The generator discovers canonical artifact JSON files, preserves existing entry `publishedAt` values, assigns current UTC publication time to newly discovered artifacts, and keeps `recentArtifacts`, archive shards, and `archiveIndexes` summaries synchronized.

The index is not a replacement for artifact contents. It should contain enough metadata to discover artifacts and decide whether to fetch them.
