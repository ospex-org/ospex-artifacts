# Odds stream monitor — contest 17

Verdict: **pass**

- Started: `2026-05-22T17:53:07.658599Z`
- Finished: `2026-05-22T18:43:07.688607Z`
- Duration requested: `3000s`
- Events: `{'snapshot': 3, 'status': 3, 'refresh': 74, 'change': 7}`
- Process return code: `0` (expected timeout/termination)

## Market metrics

### moneyline
- events: `{'snapshot': 1, 'status': 1, 'refresh': 22, 'change': 5}`
- statuses: `{'connected': 1}`
- first snapshot: `2026-05-22T17:53:09.546818Z`
- first connected: `2026-05-22T17:53:09.547351Z`
- first refresh: `2026-05-22T17:53:46.645815Z`
- first change: `2026-05-22T17:54:46.465344Z`
- max event gap seconds: `61.164`
- first pollCapturedAt: `2026-05-22T17:52:46.344000Z`
- last pollCapturedAt: `2026-05-22T18:19:46.976000Z`
- max poll age at receive seconds: `23.203`
- changedAt distinct count: `6`
- price signature distinct count: `7`

### spread
- events: `{'snapshot': 1, 'status': 1, 'refresh': 26, 'change': 1}`
- statuses: `{'connected': 1}`
- first snapshot: `2026-05-22T17:53:09.548116Z`
- first connected: `2026-05-22T17:53:09.548427Z`
- first refresh: `2026-05-22T17:53:46.650994Z`
- first change: `2026-05-22T18:19:47.205364Z`
- max event gap seconds: `61.164`
- first pollCapturedAt: `2026-05-22T17:52:46.407000Z`
- last pollCapturedAt: `2026-05-22T18:19:47.073000Z`
- max poll age at receive seconds: `23.141`
- changedAt distinct count: `2`
- price signature distinct count: `7`

### total
- events: `{'snapshot': 1, 'status': 1, 'refresh': 26, 'change': 1}`
- statuses: `{'connected': 1}`
- first snapshot: `2026-05-22T17:53:09.555410Z`
- first connected: `2026-05-22T17:53:09.556225Z`
- first refresh: `2026-05-22T17:53:46.657154Z`
- first change: `2026-05-22T18:09:48.049209Z`
- max event gap seconds: `61.139`
- first pollCapturedAt: `2026-05-22T17:52:46.464000Z`
- last pollCapturedAt: `2026-05-22T18:19:47.134000Z`
- max poll age at receive seconds: `23.091`
- changedAt distinct count: `2`
- price signature distinct count: `7`

## Post-first-pitch observation
- Scheduled first pitch: `2026-05-22T18:20:00Z`.
- Last market event: about `2026-05-22T18:19:47Z`.
- Events after scheduled first pitch: `0`.
- Interpretation: expected/neutral for this pre-game odds acceptance run; the stream delivered snapshots, connected statuses, refreshes, and price changes up to first pitch.

## Files
- `odds-stream-contest-17-through-first-pitch.received.ndjson` — received odds watch NDJSON with local receive timestamps
- `odds-stream-contest-17-through-first-pitch.summary.json` — machine-readable summary
- `odds-stream-contest-17-through-first-pitch.stderr.txt` — stderr capture

No wallet or signing material is used by this monitor.
