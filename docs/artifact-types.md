# Artifact Types

This repository publishes public-safe Ospex artifacts in a small number of stable classes. The classes can evolve, but each artifact should be explicit about what it proves and what it does not prove.

## Common rules

Every artifact class should follow these rules:

1. JSON is the source of truth.
2. Markdown is a human-readable rendering of JSON facts.
3. Raw inputs are sanitized before publication.
4. Artifact-level `status` values use the controlled vocabulary below. Gate-level statuses such as `pass`, `fail`, `not_run`, and `not_available` remain local to the gate object.
5. Observations and caveats are factual and test-scoped. They should not contain internal planning language.
6. Wallet labels are role labels unless a public identity is intentionally part of the artifact.
7. Schema-backed JSON files include a top-level `$schema` pointer to the matching file under `schemas/` and are validated by `python3 scripts/validate-artifacts.py`.

## Status vocabulary

Dashboards and agents may switch on artifact-level `status`, so it is intentionally constrained.

- `runs/`: `complete_verified`, `complete_verified_with_caveats`, `partial`, `superseded`
- `releases/`: `stage0_green`, `stage0_green_with_caveats`, `stage0_partial`, `stage0_failed`, `superseded`
- `daily/`: `complete`, `complete_with_caveats`, `partial`, `superseded`

These are artifact-level statuses only. Individual check/gate fields can use their own local values, for example `pass`, `fail`, `not_run`, or a version string when the gate records an observed value.

## `runs/` — lifecycle evidence

`runs/` artifacts record a completed protocol or market-maker lifecycle for one or more contests.

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
- known caveats observed during the run

A run artifact may be `complete_verified`, `complete_verified_with_caveats`, `partial`, or `superseded`. Caveats are part of the record; they do not make an artifact invalid by default.

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
- post-action state checks
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

- summarize a UTC calendar day
- record block range and snapshot provenance
- report protocol metrics with prior-calendar-day deltas
- link to the per-contest run artifacts instead of duplicating their evidence
- include sample sizes with wallet performance metrics
- mark wallet classification as best-effort when present
- keep forward-looking fields optional and non-load-bearing

The first daily schema should be based on repeated MVE data rather than speculative fields. Consumers should ignore unknown fields.

## `index.json` — repository index

`index.json` is a lightweight entry point for agents, dashboards, and humans. It lists published artifacts and their canonical JSON/Markdown paths.

The index is not a replacement for artifact contents. It should contain enough metadata to discover artifacts and decide whether to fetch them.
