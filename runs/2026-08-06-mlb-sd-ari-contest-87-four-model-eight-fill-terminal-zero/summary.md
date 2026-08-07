# August 6 SD@ARI contest 87 — four models, two markets, 8/8 fills, terminal zero

- **Status:** `complete_verified_with_caveats`
- **Network:** Polygon mainnet (`chainId=137`)
- **Contest:** `87`; moneyline `235`; total 9 `236`
- **Frozen plan:** `91654424daa58ba05e879db6aa6bb38cc1ba53770fa339daf6a03b572732c488`

Four role-isolated model wallets each supplied one moneyline and one total decision. Under the fixed moneyline/total execution policy all eight decisions were selected for execution; six carried `wouldAbstain=true`. The four model responses landed in a **10.418-second** window. All **8/8 frozen arms** have durable successful fill completions: four from the original pass and four from two separately timestamped, authorized late-retry passes. Every retry reused its model’s original frozen response timestamp, so no new benchmark response is represented in retry evidence. Aggregate model risk was **7.999343 USDC** against 8 USDC requested.

## Controlled fills

| Model | Market | Selection | Confidence | Would abstain | Model risk USDC | Timing | Transaction |
|---|---|---|---:|---|---:|---|---|
| Anthropic | moneyline | Arizona Diamondbacks | `0.35` | `true` | `0.999972` | original-pass-completion | [`0x27cbde649366071491f7812561dfc68f06e378d7186cc7f03750b293b04ff974`](https://polygonscan.com/tx/0x27cbde649366071491f7812561dfc68f06e378d7186cc7f03750b293b04ff974) |
| Gemini | moneyline | San Diego Padres | `0.5` | `false` | `0.999915` | authorized-late-retry | [`0xd6a1022179f21de07ae7d85aa010ecf055d4e858b945b62b6218c9f7110daee1`](https://polygonscan.com/tx/0xd6a1022179f21de07ae7d85aa010ecf055d4e858b945b62b6218c9f7110daee1) |
| OpenAI | moneyline | Arizona Diamondbacks | `0.5` | `true` | `0.999898` | original-pass-completion | [`0x9fda4f46523abc6a35bbd58ce2b08965ecc52738cbda178165633c3fe1befdb0`](https://polygonscan.com/tx/0x9fda4f46523abc6a35bbd58ce2b08965ecc52738cbda178165633c3fe1befdb0) |
| xAI | moneyline | Arizona Diamondbacks | `0.52` | `true` | `0.999898` | authorized-late-retry | [`0x94cdff539bf2f2e7376e503228ec88d49cfd8a728ba8decafa826f4d30be8e32`](https://polygonscan.com/tx/0x94cdff539bf2f2e7376e503228ec88d49cfd8a728ba8decafa826f4d30be8e32) |
| Anthropic | total | under | `0.3` | `true` | `0.999915` | authorized-late-retry | [`0x29ec0f98c4c9e34f9316006b847cf941f6c43e82aa8f8520281b2f23b84b4f5f`](https://polygonscan.com/tx/0x29ec0f98c4c9e34f9316006b847cf941f6c43e82aa8f8520281b2f23b84b4f5f) |
| Gemini | total | over | `0.5` | `false` | `0.999915` | authorized-late-retry | [`0x3cfd307b03cca69f5b0380c4ea4e3b37f4d126fefcc75bde06285c3fa83f57e8`](https://polygonscan.com/tx/0x3cfd307b03cca69f5b0380c4ea4e3b37f4d126fefcc75bde06285c3fa83f57e8) |
| OpenAI | total | under | `0.45` | `true` | `0.999915` | original-pass-completion | [`0x68fdeba966b20322e059930a51f9074d0af57b076b8fe82617343fe83886d059`](https://polygonscan.com/tx/0x68fdeba966b20322e059930a51f9074d0af57b076b8fe82617343fe83886d059) |
| xAI | total | under | `0.5` | `true` | `0.999915` | original-pass-completion | [`0xf602c24ae2008cfad66ab883ac3f974ee9637b407a7813262c104c1ac1bca608`](https://polygonscan.com/tx/0xf602c24ae2008cfad66ab883ac3f974ee9637b407a7813262c104c1ac1bca608) |

The per-arm confidence, probabilities, and abstention flags are bound collectively by benchmark source artifact SHA-256 `f115c25cab8714d4f445df8dd080ad5e11c6a6ee57699a440942c25b3f469025`; no per-arm decision hash is claimed.

## Postgame lifecycle

The [official MLB schedule feed](raw/final-score-source.sanitized.json), captured at `2026-08-07T19:13:22Z`, exactly matched San Diego at Arizona, the scheduled `2026-08-07T01:40:00Z` start, `Final` status, and San Diego’s **5–1** win. The CRE callback set that exact on-chain score; moneyline speculation `235` settled **away / San Diego**, and total-9 speculation `236` settled **under**.

- score request: [`0xb92215ea056326b75ea25c55e72540d633d13142442dc8c8d164205d718d775d`](https://polygonscan.com/tx/0xb92215ea056326b75ea25c55e72540d633d13142442dc8c8d164205d718d775d)
- CRE score callback: [`0xc0082b2f1f96bb62414719379d60d83ceee4325d4c02ad7a8637df6b4dc92425`](https://polygonscan.com/tx/0xc0082b2f1f96bb62414719379d60d83ceee4325d4c02ad7a8637df6b4dc92425)
- settle moneyline 235: [`0xcd6989e5a88857bbbbd41362a96ab427efc3d4d17c844f81e1922a9630665622`](https://polygonscan.com/tx/0xcd6989e5a88857bbbbd41362a96ab427efc3d4d17c844f81e1922a9630665622)
- settle total 236: [`0x93a7e0b7f52e4b08a8e68cba4790e9e5bbaae49cbcd790799c9201b18670082e`](https://polygonscan.com/tx/0x93a7e0b7f52e4b08a8e68cba4790e9e5bbaae49cbcd790799c9201b18670082e)
- winning claims: **8**, all confirmed

Fresh publication readback found all **22/22 selected lifecycle proof transactions** successful: eight fills, score request, CRE callback, two settlements, eight claims, and two dated-permission revocations. That selected set begins at model fills and excludes setup.

## Market-setup boundary

- contest creation-verification request: [`0x8ac20616fa05472d7ed0d52c64070c135e37ccff40f53b5b6def8f52828ac95b`](https://polygonscan.com/tx/0x8ac20616fa05472d7ed0d52c64070c135e37ccff40f53b5b6def8f52828ac95b) — Flow paid `1.000000 USDC`
- seed speculation `235`: [`0x36331223bac447f361da6f48c0486f78323732072ef1b2c5b96a41164029a68b`](https://polygonscan.com/tx/0x36331223bac447f361da6f48c0486f78323732072ef1b2c5b96a41164029a68b) — Flow self-matched `0.010000 USDC` per side and paid `0.500000 USDC`
- seed speculation `236`: [`0x8ef838c055a3289a27ab11d7f916106887c974c3c11d44790e34bb766d371e72`](https://polygonscan.com/tx/0x8ef838c055a3289a27ab11d7f916106887c974c3c11d44790e34bb766d371e72) — Flow self-matched `0.010000 USDC` per side and paid `0.500000 USDC`

The two self-matches supplied `0.040000 USDC` setup principal and later returned `0.040000 USDC` in two Flow claims, for `0.000000 USDC` setup-position P&L. This explains the difference between `15.573343 USDC` model/Maker matched principal and `15.613343 USDC` published claim payouts. Total setup protocol fees were `2.000000 USDC`, all from Flow.

## Outcome economics

- aggregate model delta: **−0.190483 USDC**
- Maker A delta: **+0.190483 USDC**
- Flow creation-fee-path delta: **−2.000000 USDC**
- model deltas: Anthropic `−0.047672`, OpenAI `−0.047598`, Gemini `−0.047615`, xAI `−0.047598 USDC`

Each model finished one win and one loss. The `0.000074 USDC` range among model deltas is economically non-discriminative in this one-contest smoke and is not a model ranking.

## Terminal zero

At `2026-08-07T12:05:36.170738Z`:

- active / pending-settlement / claimable positions across six wallets: **0 / 0 / 0**
- Maker A live contest commitments: **0**
- relevant controller processes: **0**
- Flow dated Position/Treasury allowance: **0 / 0**
- Maker A dated Position/Treasury allowance: **0 / 0**
- durable controlled-fill completions: **8**

For this artifact-specific terminal-zero boundary, four reusable model PositionModule allowances are outside run-dated permission cleanup; all model Treasury allowances are zero. This is not asserted as a repository-wide policy.

## Gate terminology

Here **B1** means a bounded one-contest role-isolated lifecycle proof through terminal cleanup. **B2** means a separate seven-day canonical-cohort acceptance gate. This run completes B1 with disclosed defects and makes no B2 acceptance claim.

## Disclosed caveats

The requested pre-start Maker report was missed. Four fills required two authorized retry passes, and original failures remain preserved rather than rewritten. A readiness-field mismatch delayed the single score request by over seven hours; claim-side routing and late-index readback also required manual repair. No duplicate score request or failed on-chain recovery transaction was sent. The benchmark smoke used uncommitted exact-game selection support, and run-recovery control-plane repairs were also uncommitted at evidence freeze; the published bare commits therefore identify committed baselines rather than fully reproducing the run. No closing-odds/CLV artifact exists, and this run makes no B2 acceptance claim.

Machine-readable source of truth: [`evidence.json`](evidence.json).
