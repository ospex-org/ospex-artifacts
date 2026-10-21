# Public scoring record: scope, sources and rebuild

Start at the [readable record](../scoring/README.md), [complete CSV](../scoring/record.csv), or [deployment-qualified run index](../scoring/run-contests.csv). These are generated views of [`scoring/snapshot.json`](../scoring/snapshot.json), not a live status endpoint.

## Coverage and identity

The snapshot is Polygon chain 137, block **95902150**, `2026-10-21T04:56:33Z`, hash `0x6543344d163b2fdff53f1de1218bf3b3b024df3d32b366ee055fdf2b52acfb70`. Public inputs were captured on 2026-10-21; the bundle baseline is artifact-repository commit `351c19f78d070f0b2db863f25924cbc4b0f44352`. **R5 is the fifth deployment of the contracts**, live on Polygon since 2026-06-28; R4 is the one before it.

- **R5:** core `0x40047BAFcdEd16C938058b7b67186299a2893561`, contest module `0x0f838AF735E95625905c6acFB887a2E9f4DB9216`, deployment block 89322650. The complete counter is contests **1–483**, including contests with no run bundle: **475 scored, 1 void, 4 verified/unscored, 3 unverified**. All 475 scored rows agree with the separately captured final. This is a count of registry entries, not unique real-world games and not a measure of scoring latency or availability.
- **R4:** core `0xECD12Af197FBF4C9F706B5Eb11a19c40Cfd643db`, contest module `0x1Eb0048650380369C6F4239dE070114463626102`, deployment block 86135682. The 51-contest chain capture supports legacy bundle reconciliation; it is **not** a second complete actual-results table. The run index retains its score receipts and its #38 void. R4 rows must never be attributed to the same-number R5 contest.
- R4 and R5 are both **protocol v2** deployment labels. No v3 deployment or v3 observation is included.

The key is `(chain_id, deployment_address, contest_number)`, serialized as `contest_key`. The module address is the log emitter, not a substitute for the core deployment identity. Every score is **away–home**. Empty CSV cells mean absent, never zero; a void is not a 0–0 score.

## Actual result and scoring time

The chain capture reads the counter, `getContest(uint256)` and `s_contestStartTimes(uint256)` at the frozen block; it enumerates `ContestScoresSet(uint256,uint32,uint32)` and `ContestVoided(uint256)` from the corresponding module's deployment block through that block. Terminal entries carry the transaction hash, successful receipt status, typed event/topic, emitter, block number/hash and UTC block timestamp. **`scored_at_utc` is the successful scoring transaction's block time**, not request submission, game completion, API ingestion, or local observation time. Void timestamps use the separate terminal columns. This record does not assert who requested a score or how quickly a game was scored after its final.

R5 names and API schedule times come from the public core API contest resource (`/v1/contests/{contest_number}`). The snapshot retains the three external identity IDs, which must agree with the pinned chain contest; verified league and start time are checked separately. API score/status fields are **not** used as protocol truth.

### Game-time fields

`gameMatchTime` is the API's raw upstream/reference schedule (`games.match_time`), not the verified on-chain start and not a recorded first observation. The [API mapping and time-field contract](https://github.com/ospex-org/ospex-core-api/blob/adc000fa352d47c13b81f07d950ec64c68b6b5fb/src/v1/contests.ts#L21-L40) distinguish it from `chainStartTime`. All comparisons are between timezone-aware UTC instants, and the capture does not contain each schedule's revision history.

The readable table shows **Chain start (UTC)**, the time written when the game was confirmed. It is a recorded scheduled start, not proof of actual first pitch or kickoff; unverified games have a dash. The CSV preserves all three inputs unchanged:

- `game_date_utc`: the captured API `gameMatchTime` schedule.
- `chain_start_utc`: the confirmed start from the chain, cross-checked against the API's `chainStartTime`.
- `source_event_time_utc`: the independent result source's scheduled event time. `source_time_delta_seconds` is this time minus the API schedule, not a scoring delay.

There are **25 MLB entries with nonzero schedule differences**, up to **3 h 50 min**; in **21** of them the chain start equals MLB's time. For #436 (Detroit Tigers @ Chicago White Sox, September 20), the API schedule is **22:00 UTC** while both the chain and MLB say **18:10 UTC**; the table shows **18:10 UTC**, and the CSV retains the **−13,800-second** source/API difference. The other four are #85 (chain 23:00, MLB 23:10; postponed), #296 (22:40 versus 22:45), #307 (23:10 versus 23:15), and #479 (no chain start). These are different schedule fields, not a proven history of rescheduling; no input is rewritten to make them agree.

Actual results have their own source URL and source event ID:

- **478 MLB entries:** MLB's official Stats API schedule, captured once and committed in the snapshot; a rebuild never re-pulls it. The row's `actual_event_id` is `gamePk`; `actual_source_url` identifies the daily schedule response. The source status, final flag, scores, official date, game number, doubleheader and rescheduling metadata are retained in the snapshot. Postponed entries retain their original event/status rather than borrowing the rescheduled game's final. When v3 rows begin and the record grows, a second source is required so no single feed is sole; MLB remains the official reference.
- **5 NFL entries:** [nflverse/nfldata](https://github.com/nflverse/nfldata), an attributed independent secondary source, not an NFL-operated official feed. The [pinned `games.csv`](https://raw.githubusercontent.com/nflverse/nfldata/1853019c22fa3e4845bdeb5232cd3920bcfd9cb3/data/games.csv) is commit `1853019c22fa3e4845bdeb5232cd3920bcfd9cb3`, captured `2026-10-21T06:50:45.552530Z`, file SHA-256 `43b1f34bf2b40eb1f44f7b1f10777e5da5598a8321226cb4d8e59a1cd0684937`. Each row retains its nflverse `game_id`, scores and capture provenance. The five away–home scores are 30–13, 24–16, 30–23, 14–17 and 13–23. nflverse distributes its data under CC-BY-4.0 while noting underlying data ownership; attribution here is not a claim of unrestricted betting-use rights.

MLB matching uses exact away/home names and scheduled instant where available (453 entries). Another 25 entries use the uniquely nearest scheduled slot for the same teams, with the source delta, game number and doubleheader metadata disclosed; the permitted absolute delta is less than 12 hours. These have different captured schedule times, **not** exact-time matches; see the field explanation above. NFL matching uses the unique exact-team event on the `America/New_York` game date (5 entries; these also have zero timestamp delta). The rebuild checks the frozen associations; it does not download today's schedules or independently re-run candidate discovery. MLB source URLs can change after capture; the nflverse URL is commit-pinned. A fresh capture and review is required to change the associations.

If Ospex's score differs from the captured final for the same game, the row has **`status=mismatch` and `comparison=mismatch`** and shows both scores. The reason, summary counts and readable headline come from those comparisons; the build continues and the row stays in the record. Wrong teams, times or IDs, a missing final, and disagreement between a chain capture and its event or run bundle remain capture errors that stop the build. The regression `test_planted_score_mismatch_is_published_and_build_continues` changes only an independent result in memory and checks the full row count, both scores, status, reason, summary and headline.

The archived source facts and chain summaries are auditable evidence inputs, not cryptographic proofs of RPC or HTTP responses. A reader can independently retrieve the linked events/receipts. The offline gate proves completeness and consistency of the committed capture and unchanged bundles; it cannot authenticate an intentionally rewritten capture against the network.

## Pending rows and voids

**The five contests left unscored by the after-game job are R5 #46, #47 and #52 (confirmed historical games whose scoring feeds no longer supplied a final) plus #119 and #123 (unverified entries for the same real game).** Archived MLB finals are shown independently even where the protocol has no score. This distinction preserves both the real result and the unsuccessful protocol outcome.

The complete counter additionally retains #85 (postponed; still verified/unscored) and #479 (unverified): seven never-scored contests in total. **No bets were ever placed on these seven contests as of Polygon block 95902150, so no money is held on them.** None had a market (a speculation in the contracts). On R5 an unscored confirmed game is voided only when someone settles a market after **seven days**, not merely because time passes. With no markets to settle, nothing triggers the void for the four July games #46, #47, #52 and #85, so they remain unscored on chain.

**Unverified** means the oracle never confirmed the game, so betting never opened. **Verified/unscored** means it was confirmed, but no score was written. A **cooldown void** is a void triggered by settlement after the seven-day waiting period. `legacy_void` is the machine-readable name for a v2 void; it is neither a score nor a v3 release.

R5 #451 had two markets (#939 and #940) and was voided through that settlement path. Its independent source reports postponement (rain); the v2 `ContestVoided` event does **not** encode that reason. The record states the protocol void and independent game status separately. R4 #38 is also retained as a v2 void in the run index, separate from R5 #38.

## Repeated numbers and immutable bundles

No directory, filename or byte under `runs/` is changed. `bundleFileSha256` pins all **1,118 files in 63 bundles**. Rebuild checks **219 identity claims and 497 score claims** against the deployment-qualified chain capture and the original JSON pointers/fields. A disagreement fails the build rather than choosing one source. Bindings use matching chain identities and/or successful transaction receipts emitted by the identified core/module, not a date guess or the contest number alone.

`run-contests.csv` contains **141 run/contest references**. `reference_kind` distinguishes a canonical `evidence.json` reference from a contest found only in supporting files. `number_shared_across_deployments` labels repeated numbers; neither occurrence is removed. The one decisions-only bundle with no on-chain contest remains in the snapshot's binding and immutable-file inventories but contributes no contest row.

**22 contest numbers were used by both R4 and R5** in the main `evidence.json` files; counting every mention in supporting files gives **29**. The run index labels each use by deployment. Supporting mentions add #12, #32, #33, #40, #41, #42 and #45. The exact sets are generated in [`summary.json`](../scoring/summary.json):

- Canonical: 13, 14, 15, 16, 18, 19, 21, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 44, 48, 49, 50, 51.
- Including supporting files: 12, 13, 14, 15, 16, 18, 19, 21, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 48, 49, 50, 51.

## v3-compatible end shape, not v3 evidence

The [row schema](../schemas/scoring-row.schema.json) and row-contract tests reserve distinct `end_kind` / `end_result` combinations:

- `score` → `score`;
- `hour_24_void` → `void`;
- `day_7_result` → `score` **or** `void` (one quorum-result path, not an automatic timeout void);
- `day_30_release` → `release`;
- `all_reporters_retired_release` → `release` (all of the game's reporters have retired).

`legacy_void` is v2-only. Nonterminal rows have empty end fields. Release is distinct from scored and void; a later v3 release row uses `status=released` and empty protocol score fields. Terminal receipts/times are separate from score-only receipts/times, so later producers can preserve those distinctions without changing the CSV columns. The present snapshot validator intentionally accepts only R4/R5 v2 captures; adding a real v3 deployment requires a reviewed capture/adapter update. Tests use labeled in-memory v3 examples only, and no generated file contains v3 rows.

## Rebuild and validation

**Rebuild on Linux with Python 3.11 or newer**, standard library only, from repository root. Python 3.11 is the minimum for the full repository validator (`datetime.UTC` is used by its imported validator). The generator reads and writes explicit UTF-8 and writes LF newlines; check mode compares bytes. Byte-identical rebuilds are verified on Linux. Windows is not a supported byte-reproduction target: Git line-ending conversion can change the immutable bundle bytes even when their text looks the same. No existing bundle is rewritten to compensate.

```sh
python3 scripts/generate-scoring-record.py
python3 scripts/generate-scoring-record.py --check
python3 -m unittest discover -s tests -v
python3 scripts/validate-artifacts.py
```

The generator performs **no network calls, signing or chain writes**; a rebuild never re-pulls the committed MLB or NFL results. It rewrites only `scoring/record.csv`, `scoring/run-contests.csv`, `scoring/summary.json` and `scoring/README.md`; `--check` writes nothing. Both modes reject missing/duplicate contests, missing/wrong terminal events, unsuccessful receipts, identity/time errors, missing finals, disagreements within chain/event/bundle evidence, changed bundle inventories and changed bundle bytes. A valid real-result/Ospex-score disagreement instead publishes a `mismatch` row, as described above. Outputs use fixed ordering and the frozen block timestamp, never the current clock. The repository validator invokes the scoring check and public-safety scans both JSON and CSV. The existing CI runs the full test suite and validator.

This snapshot does not automatically ingest future bundles: their addition changes the pinned inventory and requires an explicit, reviewed snapshot refresh alongside the new evidence. Never edit existing run bundles to make a refresh pass. New inputs are captured read-only, cross-checked, and then committed separately from this deterministic rebuild; no operator secrets, RPC endpoint or local configuration belongs in the public snapshot. The scoring snapshot is separate from the run/release index and is not a lifecycle run.
