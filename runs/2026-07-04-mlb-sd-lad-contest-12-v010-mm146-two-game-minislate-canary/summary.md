# San Diego Padres @ Los Angeles Dodgers — v0.10/MM146 two-game mini-slate canary

**Verdict:** FULL_GREEN with operator harness caveat  
**Artifact:** `2026-07-04-mlb-sd-lad-contest-12-v010-mm146-two-game-minislate-canary`  
**Network:** Polygon mainnet  
**Contest:** `12`  
**Speculations:** moneyline `24`, spread `25`, total `26`

## What was proven

- Pregame target/identity/allowlist gates passed.
- Contest `12` was created, verified, had markets updated, and covered moneyline/spread/total.
- Manual seed/fill created all three speculations with zero residual seed commitments.
- The market maker ran under strict allowlist `[11, 12]`, `seedSpeculations=false`, exact/bounded approvals, and posted tiny live commitments.
- Controlled live fill for the target `moneyline` market succeeded: `A controlled taker filled the MM moneyline quote on Los Angeles Dodgers. The final score made Los Angeles Dodgers/home/lower the winning side, so this controlled live-fill position was claimed.`
- Final score was verified from MLB Stats API: San Diego Padres 0, Los Angeles Dodgers 3.
- R5/CRE score, settle, and claims completed.
- Final open commitments and controlled active/pending/claimable positions are zero.

## Caveat / issue classification

The Slack `POSTGAME_ERROR` messages were caused by the Hermes/operator watchdog harness, not the Ospex codebase. The script used `${profile-before-claim}` in a filename; Bash treated that as parameter expansion on `profile` and dropped the literal `-before-claim` suffix. The CLI had written `positions-status-<profile>-before-claim-<timestamp>.json`, but the Python claim-planning step attempted to read `positions-status-<profile>-<timestamp>.json`. The harness was patched and the final postgame verification is green.

See `raw/watchdog-harness-caveat.sanitized.json` for the exact classification.
