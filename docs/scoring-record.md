# Public scoring record: scope, sources and rebuild

Start at the [readable record](../scoring/README.md), [complete CSV](../scoring/record.csv), or [deployment-qualified run index](../scoring/run-contests.csv). These are generated views of [`scoring/snapshot.json`](../scoring/snapshot.json), not a live status endpoint.

## Coverage and identity

The snapshot is Polygon chain 137, block **95902150**, `2026-10-21T04:56:33Z`, hash `0x6543344d163b2fdff53f1de1218bf3b3b024df3d32b366ee055fdf2b52acfb70`. Public inputs were captured on 2026-10-21; the bundle baseline is artifact-repository commit `351c19f78d070f0b2db863f25924cbc4b0f44352`.

- **R5:** core `0x40047BAFcdEd16C938058b7b67186299a2893561`, contest module `0x0f838AF735E95625905c6acFB887a2E9f4DB9216`, deployment block 89322650. The complete counter is contests **1–483**, including contests with no run bundle: **475 scored, 1 void, 4 verified/unscored, 3 unverified**. All 475 scored rows agree with the separately captured final. This is a count of registry entries, not unique real-world games and not a measure of scoring latency or availability.
- **R4:** core `0xECD12Af197FBF4C9F706B5Eb11a19c40Cfd643db`, contest module `0x1Eb0048650380369C6F4239dE070114463626102`, deployment block 86135682. The 51-contest chain capture supports legacy bundle reconciliation; it is **not** a second complete actual-results table. The run index retains its score receipts and its #38 void. R4 rows must never be attributed to the same-number R5 contest.
- R4 and R5 are both **protocol v2** deployment labels. No v3 deployment or v3 observation is included.

The key is `(chain_id, deployment_address, contest_number)`, serialized as `contest_key`. The module address is the log emitter, not a substitute for the core deployment identity. Every score is **away–home**. Empty CSV cells mean absent, never zero; a void is not a 0–0 score.

## Actual result and scoring time

The chain capture reads the counter, `getContest(uint256)` and `s_contestStartTimes(uint256)` at the frozen block; it enumerates `ContestScoresSet(uint256,uint32,uint32)` and `ContestVoided(uint256)` from the corresponding module's deployment block through that block. Terminal entries carry the transaction hash, successful receipt status, typed event/topic, emitter, block number/hash and UTC block timestamp. **`scored_at_utc` is the successful scoring transaction's block time**, not request submission, game completion, API ingestion, or local observation time. Void timestamps use the separate terminal columns. This record does not assert who requested a score or how quickly a game was scored after its final.

R5 names and original game times come from the public core API contest resource (`/v1/contests/{contest_number}`). The snapshot retains the three external identity IDs, which must agree with the pinned chain contest; verified league and start time are checked separately. API score/status fields are **not** used as protocol truth. `game_date_utc`, `chain_start_utc`, and `source_event_time_utc` remain distinct rather than silently rewriting one to match another.

Actual results have their own source URL and source event ID:

- **478 MLB entries:** MLB's official Stats API schedule. The row's `actual_event_id` is `gamePk`; `actual_source_url` identifies the daily schedule response. The source status, final flag, scores, official date, game number, doubleheader and rescheduling metadata are retained in the snapshot. Postponed entries retain their original event/status rather than borrowing the rescheduled game's final.
- **5 NFL entries:** ESPN's NFL scoreboard, explicitly identified as an **independent secondary source**, not an NFL-operated official feed. Each captured event is a completed game with exact away/home names on its local game date and its own ESPN event ID.

MLB matching uses exact away/home names and scheduled instant where available (453 entries). Another 25 entries use the uniquely nearest scheduled slot for the same teams, with the source delta, game number and doubleheader metadata disclosed; the permitted absolute delta is less than 12 hours. These are scheduled-time changes, **not** exact-time matches. NFL matching uses the unique exact-team event on the `America/New_York` game date (5 entries; these also have zero timestamp delta). The rebuild checks the frozen team/time/score associations; it does not download today's schedules or independently re-run candidate discovery. Source URLs can change after capture. A fresh capture and review is required to change the associations.

The archived source facts and chain summaries are auditable evidence inputs, not cryptographic proofs of RPC or HTTP responses. A reader can independently retrieve the linked events/receipts. The offline gate proves completeness and consistency of the committed capture and unchanged bundles; it cannot authenticate an intentionally rewritten capture against the network.

## Pending rows and voids

**The five sweep residuals are R5 #46, #47 and #52 (verified historical games whose configured scoring feeds no longer supplied a final) plus #119 and #123 (unverified entries for the same real game); all five belong in the table.** Archived MLB finals are shown independently even where the protocol has no score. This distinction preserves both the real result and the unsuccessful protocol outcome.

The complete counter additionally retains #85 (postponed; still verified/unscored) and #479 (unverified), so the five sweep residuals are not presented as the entire pending population. They are not silently excluded from the denominator or labeled void.

R5 #451 is void. Its independent source reports postponement (rain); the v2 `ContestVoided` event does **not** encode that reason. The record states the protocol void and independent game status separately rather than inventing an on-chain reason. R4 #38 is also retained as a legacy void in the run index.

## Repeated numbers and immutable bundles

No directory, filename or byte under `runs/` is changed. `bundleFileSha256` pins all **1,118 files in 63 bundles**. Rebuild checks **219 identity claims and 497 score claims** against the deployment-qualified chain capture and the original JSON pointers/fields. A disagreement fails the build rather than choosing one source. Bindings use matching chain identities and/or successful transaction receipts emitted by the identified core/module, not a date guess or the contest number alone.

`run-contests.csv` contains **141 run/contest references**. `reference_kind` distinguishes a canonical `evidence.json` reference from a contest found only in supporting files. `number_shared_across_deployments` labels repeated numbers; neither occurrence is removed. The one decisions-only bundle with no on-chain contest remains in the snapshot's binding and immutable-file inventories but contributes no contest row.

The earlier inspection reported **18 doubled numbers**. The exhaustive capture finds a larger set: **22 shared numbers in canonical evidence**, and **29 when supporting files are included**. All are labeled by deployment; no old bundle is "cleaned" to force the earlier count. The exact sets are generated in [`summary.json`](../scoring/summary.json):

- Canonical: 13, 14, 15, 16, 18, 19, 21, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 44, 48, 49, 50, 51.
- Including supporting files: 12, 13, 14, 15, 16, 18, 19, 21, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 48, 49, 50, 51.

## v3-compatible end shape, not v3 evidence

The [row schema](../schemas/scoring-row.schema.json) and row-contract tests reserve distinct `end_kind` / `end_result` combinations:

- `score` → `score`;
- `hour_24_void` → `void`;
- `day_7_result` → `score` **or** `void` (one quorum-result path, not an automatic timeout void);
- `day_30_release` → `release`;
- `all_scorers_retired_release` → `release`.

`legacy_void` is v2-only. Nonterminal rows have empty end fields. Release is distinct from scored and void; a later v3 release row uses `status=released` and empty protocol score fields. Terminal receipts/times are separate from score-only receipts/times, so later producers can preserve those distinctions without changing the CSV columns. The present snapshot validator intentionally accepts only R4/R5 v2 captures; adding a real v3 deployment requires a reviewed capture/adapter update. Tests use labeled in-memory v3 examples only, and no generated file contains v3 rows.

## Rebuild and validation

Python 3 standard library only, from repository root:

```sh
python3 scripts/generate-scoring-record.py
python3 scripts/generate-scoring-record.py --check
python3 -m unittest discover -s tests -v
python3 scripts/validate-artifacts.py
```

The generator performs **no network calls, signing or chain writes**. It rewrites only `scoring/record.csv`, `scoring/run-contests.csv`, `scoring/summary.json` and `scoring/README.md`; `--check` writes nothing. Both modes reject missing/duplicate contests, missing/wrong terminal events, unsuccessful receipts, cross-source identity/score disagreements, changed bundle inventories and changed bundle bytes. Outputs use fixed ordering and the frozen block timestamp, never the current clock. The repository validator invokes the scoring check and public-safety scans both JSON and CSV. The existing CI runs the full test suite and validator.

This snapshot does not automatically ingest future bundles: their addition changes the pinned inventory and requires an explicit, reviewed snapshot refresh alongside the new evidence. Never edit existing run bundles to make a refresh pass. New inputs are captured read-only, cross-checked, and then committed separately from this deterministic rebuild; no operator secrets, RPC endpoint or local configuration belongs in the public snapshot. This addition does not change the existing run/release index format or turn the scoring snapshot into a lifecycle run.
