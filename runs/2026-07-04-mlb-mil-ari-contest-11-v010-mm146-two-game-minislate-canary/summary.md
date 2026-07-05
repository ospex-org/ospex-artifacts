# Milwaukee Brewers @ Arizona Diamondbacks — v0.10/MM146 two-game mini-slate canary

**Verdict:** FULL_GREEN with operator harness caveat  
**Artifact:** `2026-07-04-mlb-mil-ari-contest-11-v010-mm146-two-game-minislate-canary`  
**Network:** Polygon mainnet  
**Contest:** `11`  
**Speculations:** moneyline `21`, spread `22`, total `23`

## What was proven

- Pregame target/identity/allowlist gates passed.
- Contest `11` was created, verified, had markets updated, and covered moneyline/spread/total.
- Manual seed/fill created all three speculations with zero residual seed commitments.
- The market maker ran under strict allowlist `[11, 12]`, `seedSpeculations=false`, exact/bounded approvals, and posted tiny live commitments.
- Controlled live fill for the target `spread` market succeeded: `A controlled taker filled the MM spread quote: Milwaukee Brewers -1.5. The final score made Arizona Diamondbacks +1.5 the winning lower side, so this controlled live-fill position lost and the MM maker lower-side position was claimable.`
- Final score was verified from MLB Stats API: Milwaukee Brewers 3, Arizona Diamondbacks 4.
- R5/CRE score, settle, and claims completed.
- Final open commitments and controlled active/pending/claimable positions are zero.

## Caveat / issue classification

The Slack `POSTGAME_ERROR` messages were caused by the Hermes/operator watchdog harness, not the Ospex codebase. The script used `${profile-before-claim}` in a filename; Bash treated that as parameter expansion on `profile` and dropped the literal `-before-claim` suffix. The CLI had written `positions-status-<profile>-before-claim-<timestamp>.json`, but the Python claim-planning step attempted to read `positions-status-<profile>-<timestamp>.json`. The harness was patched and the final postgame verification is green.

See `raw/watchdog-harness-caveat.sanitized.json` for the exact classification.
