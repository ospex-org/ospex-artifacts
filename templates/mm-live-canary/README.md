# MM live canary templates

Templates for the per-run scenario matrix and MVE readiness scorecard that every market-maker live canary publishes. The vocabulary, validator rules, and worked semantics live in `docs/mm-live-canary-evidence.md`; this directory only carries the copyable starting points.

## How to instantiate

1. Copy the four `*.template.*` files into the new `runs/<artifact-id>/` directory and drop the `.template` part of each name (`scenario-matrix.json`, `scenario-matrix.md`, `mve-scorecard.json`, `mve-scorecard.md`).
2. Replace every placeholder: `artifactId` (must equal the run directory name), `generatedAt`/`checkedAtUtc` timestamps, statuses, proof levels, evidence paths, notes, and the verdict label + reason. Placeholders are intentionally invalid so the validator fails until they are filled.
3. In `mve-scorecard.json`, add one `transactions` entry per on-chain transaction the run relies on and delete unused skeleton entries. Every entry needs a controlled `category`; free-form context goes in `purpose`.
4. Keep all fourteen capability rows. A capability that did not apply or was intentionally left for a future run still gets a row (`not_applicable` or `deferred`) — the scorecard exists to show exactly what is proven, synthetic-only, deferred, or failed.
5. Reference both files from `evidence.json` `artifactFiles` (the validator requires `scenario-matrix.json` and `mve-scorecard.json` to appear among the values).
6. Update the markdown renders so they mirror the JSON facts; JSON is canonical.
7. Run `python3 scripts/generate-indexes.py`, then `python3 scripts/validate-artifacts.py`.

## What adoption turns on

Validation of these shapes is opt-in: it triggers when a run directory contains `mve-scorecard.json` or a `scenario-matrix.json` that declares adoption (a `$schema` pointer, or a plain-integer `schemaVersion` of 2 or higher — near-miss declarations like `"2"` or `2.0` are rejected loudly). Earlier free-form scenario matrices are grandfathered. `runClass` is a closed registry (currently `mm-live-canary` only) and the matrix and scorecard must declare the same value; an mm-live-canary v2 matrix requires a scorecard and every scorecard requires a v2 matrix. An adopting run covers exactly one target contest/speculation — a multi-contest canary publishes one run directory per contest. Once a run adopts, the validator enforces the matrix/scorecard schemas, the verdict vocabulary and its consistency with the artifact status and successful transaction categories, the moneyline team-identity block, and the end-of-run zero-exposure invariant.
