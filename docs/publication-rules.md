# Publication Rules

Public artifacts should be factual, reproducible, and safe to consume directly. Treat this repository as a published data/evidence layer, not as an internal planning workspace.

## Editorial rules

- Use neutral, descriptive language.
- Do not include internal brainstorming, roadmap debate, private operator notes, or promotional copy.
- State what the artifact proves and what it does not prove.
- Record skipped optional checks explicitly.
- Keep caveats factual and scoped to the artifact.
- Prefer role labels such as `market-maker`, `flow-taker`, `contest-creator`, or `acceptance-wallet` unless a public identity is intentional.
- If wallet classification is present, mark it as best-effort unless it is derived from a deterministic rule.

## Source-of-truth rules

- JSON artifacts are canonical.
- Markdown summaries must be derived from JSON facts and sanitized raw inputs.
- Summaries may explain context, but they should not add new factual claims absent from the machine-readable artifact.
- Keep summaries evidence-grade and technical. Audience-friendly headlines and simplified narrative belong in a frontend/dashboard layer derived from the artifact, not in the artifact itself.
- Raw files under `raw/` should be sanitized snapshots or summaries, not unfiltered runtime captures.

## Include

Include public and reproducible evidence such as:

- chain/network identifiers
- block numbers, tx hashes, tx receipt summaries, and explorer links
- contest, speculation, position, commitment, release, and artifact identifiers
- public wallet addresses and role labels
- final-score or other approved external fact sources
- sanitized indexer/API snapshots
- package asset names and hashes for release acceptance
- setup/live/lifecycle gate results
- non-blocking observations and known caveats

## Exclude

Never publish:

- private keys
- seed phrases
- password files or password-file paths
- RPC URLs
- API keys, Supabase keys, Postgres URLs, auth headers, or bearer tokens
- raw environment files
- raw EIP-712 signatures unless deliberately required for a specific reproducibility reason
- raw calldata or revert blobs unless intentionally summarized and reviewed
- local machine paths, scratch workdirs, or Hermes cache paths
- unredacted logs, telemetry dumps, SQLite databases, or wallet keystore material
- internal brainstorming or marketing language

## Pre-publication checklist

Before committing an artifact:

1. Run `python3 scripts/generate-indexes.py` after adding, removing, or editing an artifact. It rewrites `index.json` and archive shards from artifacts on disk, preserving existing `publishedAt` values and assigning a current UTC `publishedAt` to newly discovered artifacts.
2. Run `python3 scripts/validate-artifacts.py`; it validates JSON/NDJSON parseability, schema-backed `$schema` pointers, artifact-level status vocabulary, generated index/archive consistency, referenced path existence, and conservative public-safety patterns.
3. Confirm Markdown summaries only contain facts from JSON or sanitized raw inputs.
4. Check that optional/skipped gates are explicit.
5. Check that public wallet labels are role labels or intentionally public identities.
6. Review any occurrence of words such as `password`, `secret`, `signature`, `token`, `RPC`, `Supabase`, `Postgres`, or `/home/` before publishing.
7. Verify artifact paths are referenced from `README.md` or `index.json` when they are intended to be discoverable.

Allowed findings include checklist text in this document and sanitized explanatory notes. Actual credentials, paths to secret files, and raw sensitive material are not allowed.

## Reproducibility notes

Each artifact should make its reproducibility boundary clear:

- A lifecycle run should identify the public chain data, external final-score source, and sanitized indexer/API rows needed to check the lifecycle.
- A release acceptance should identify the public release assets, hashes, setup gates, live gates, and resulting on-chain transactions.
- A daily digest should identify the UTC date, block range, sanitized snapshot hash, and linked run artifacts used to compute the rollup. Publish one digest for every UTC calendar day; zero-activity days should record zero counts and coverage/provenance rather than being skipped.
