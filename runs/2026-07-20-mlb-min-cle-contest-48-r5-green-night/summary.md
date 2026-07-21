# Minnesota Twins @ Cleveland Guardians — R5 contest 48

## Verdict

**FULL_GREEN** — Minnesota Twins @ Cleveland Guardians contest 48 completed the bounded R5 lifecycle: three markets seeded and filled, live maker quotes posted, official final verified, all three speculations settled, winning positions claimed, both controlled-wallet allowances revoked, and final commitments/positions/processes were zero.

## Target

- Network: Polygon mainnet (chain 137)
- Deployment round: **R5**
- Contest: `48`
- Target speculation: `126` moneyline
- Official final: Minnesota Twins 4, Cleveland Guardians 13
- Seed-match transaction: `0x0c8c59534aac759015d2b127500c0c44504ed8df100eed0ede2469da3f7c295a`

## Lifecycle

- All three approved markets were seeded and fully matched.
- Bounded live maker quotes were posted only for contests 48 and 49.
- Official final and on-chain/API score agreed.
- All three speculations settled and all winning controlled positions were claimed.
- Final commitments, positions, allowances, and orphan processes were zero.

## Caveats

- A same-run settle followed by an immediate claim estimate produced one attributable pre-send error with no transaction. Independent settled-state readback preceded a single direct claim, which succeeded.
- Two unrelated micro-USDC inflows were attributed separately and excluded from protocol P&L.
- One transient dry discovery fetch recovered; one replaced quote was rejected before transaction.

Canonical facts are in `evidence.json`; sanitized supporting facts are under `raw/`.
