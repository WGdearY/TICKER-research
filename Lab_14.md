# Lab 14 — Portfolio Construction and Stability

**Author:** Will Gao | gao713@purdue.edu
**Date:** October 20, 2026
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 14
**Mandate source:** Lab 13 — Meridian Foundation Reserve (fictional, course-authored)
**Input provenance:** COURSE_SYNTHETIC_TEACHING_INPUTS — course-authored, annualized, Oct. 20, 2026 release.
Not estimates from a historical sample. No real securities. No missing values.
Sample boundary: not applicable — no observed sample.

---

## Prework Record (Written Before Running — No AI)

1. **Two assets I expect to be most highly correlated:** USEquity and IntlEquity — both are broad equity exposures driven by global growth; I expect correlation ≈ 0.70–0.80.
2. **Asset expected to receive the largest inverse-volatility weight:** GovBond — lowest volatility (6.0%) → highest 1/σ → largest weight.
3. **One mandate constraint that could bind:** The 40% benchmark allocation to bonds. If a risk-optimization model pushes equity weight above 65%, the benchmark-alignment constraint would bind and require overriding the optimizer.

---

## Part 1 — Mandate Restatement (from Lab 13)

| Mandate element | Operational value | Source |
|---|---|---|
| Decision user | Meridian Foundation investment committee | Lab 13 |
| Decision | Authorize analysis and pilot — not execute trades | Lab 13 |
| Objective | CPI + 4.0% net of costs, rolling 5-year periods | CIO statement |
| Benchmark | 60% broad global equities / 40% U.S. investment-grade bonds | Case |
| Horizon / rebalancing | 7-year policy; quarterly review; annual rebalancing | Case |
| Risk measure | Calendar-year return; loss stated as > -10% (no enforcement mechanism) | Case |
| Liquidity rule | $3M in daily-liquid government securities; 90% within 5 business days | Case |
| Constraints | Long-only; no leverage, shorting, or derivatives; 8% single-issuer max; turnover ≤ 25%/yr | Case |
| Optimization criterion | **UNRESOLVED** — committee has not defined return / tracking-error / drawdown / distribution-probability | Lab 13 escalation |

---

## Part 2 — Input Conventions

| Convention | Value |
|---|---|
| Frequency | Annualized (both expected returns and volatilities) |
| As-of boundary | October 20, 2026 (course release date) |
| Provenance | COURSE_SYNTHETIC_TEACHING_INPUTS — not historical estimates, not real securities |
| Missing values | None — no missingness policy required |
| Expected returns | Teaching inputs, not forecasts or forward estimates |
| Covariance | Computed as Σ = diag(σ) × C × diag(σ); annualized consistent with volatility inputs |

**Asset inputs:**

| Asset | Expected Return | Volatility |
|---|---:|---:|
| GovBond | 4.00% | 6.00% |
| CorpBond | 5.50% | 9.00% |
| USEquity | 8.50% | 18.00% |
| IntlEquity | 8.00% | 20.00% |

**Correlation matrix:**

| | GovBond | CorpBond | USEquity | IntlEquity |
|---|---:|---:|---:|---:|
| GovBond | 1.00 | 0.35 | -0.10 | -0.05 |
| CorpBond | 0.35 | 1.00 | 0.25 | 0.20 |
| USEquity | -0.10 | 0.25 | 1.00 | **0.75** |
| IntlEquity | -0.05 | 0.20 | **0.75** | 1.00 |

Most correlated pair: USEquity ↔ IntlEquity at 0.75 (confirmed prework prediction). GovBond has negative correlation with both equity assets — the primary diversification source.

---

## Part 3 — Covariance Matrix

Formula: `cov(i,j) = σ_i × ρ(i,j) × σ_j`

| | GovBond | CorpBond | USEquity | IntlEquity |
|---|---:|---:|---:|---:|
| GovBond | 0.003600 | 0.001890 | -0.001080 | -0.000600 |
| CorpBond | 0.001890 | 0.008100 | 0.004050 | 0.003600 |
| USEquity | -0.001080 | 0.004050 | 0.032400 | 0.027000 |
| IntlEquity | -0.000600 | 0.003600 | 0.027000 | 0.040000 |

**Manual reconciliation (2 required cells):**

- **Diagonal — cov(GovBond, GovBond):** `0.060 × 1.00 × 0.060 = 0.003600` ✓
- **Off-diagonal — cov(USEquity, IntlEquity):** `0.180 × 0.75 × 0.200 = 0.027000` ✓

**Structural checks:** Symmetric (all 16 cells verified), unit diagonal in correlation matrix — PASS.

---

## Part 4 — Baseline and Candidate Portfolios

### Portfolio Comparison Table

| Portfolio | GovBond | CorpBond | USEquity | IntlEquity | Exp. Return | Volatility | Constraint breach? | What it establishes |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **Equal weight** | 25.00% | 25.00% | 25.00% | 25.00% | 6.50% | 9.80% | None | Transparent minimum-complexity baseline |
| **Inverse volatility** | 43.48% | 28.99% | 14.49% | 13.04% | 5.61% | 6.80% | None | Risk-scaling baseline; lower return, much lower vol |
| **Candidate (PROVISIONAL)** | 24.00% | 16.00% | 31.58% | 28.42% | 6.80% | 11.12% | None | Mechanics probe — 60/40 benchmark-aligned; NOT for adoption |

**Net-of-cost (25bps):** Candidate net return = **6.55%**

### Candidate Allocation — Provisional Objective and Constraints

> **PROVISIONAL_MECHANICS_PROBE — DEFERRED_NO_ADOPTABLE_CANDIDATE**
> The CIO optimization criterion remains unresolved (Lab 13 escalation). This allocation
> practices model mechanics but cannot support adoption.

**Provisional objective (explicitly labeled):** Track the 60/40 benchmark by applying inverse-volatility weighting *within* each asset class. No optimizer objective invented; no CIO preference assumed.

**Constraints applied:**
1. Long-only — all weights ≥ 0 ✓
2. No leverage — weights sum to 1.000000 ✓
3. Benchmark alignment — 40% bonds / 60% equities (matches stated policy benchmark) ✓
4. Single-issuer cap (8%) — applies to individual securities, not broad asset classes; not binding ✓
5. Liquidity — GovBond + CorpBond = 40.0% (daily-liquid) ✓

**CIO escalation required before adoption:**
> *"Is the primary success criterion (a) maximizing probability of funding distributions, (b) minimizing tracking error to the 60/40 benchmark, or (c) achieving CPI + 4% over rolling 5-year periods?"*
> Escalation owner: Meridian Foundation investment committee.

---

## Part 5 — Perturbation / Stability Tests

> Expected direction written **before** running each test (required by handout).

| Test | Input/constraint changed | Expected direction (pre-run) | Actual result | Mandate effect | Disposition |
|---|---|---|---|---|---|
| **Mean estimate** | USEquity return: 8.5% → 9.5% | Return increases; weights unchanged (IV model independent of returns) | Return +0.32pp (6.80% → 7.11%); vol unchanged | None — no constraint breached | Confirmed ✓ |
| **Covariance/window** | USEquity↔IntlEquity correlation: 0.75 → 0.90 | Vol increases (less diversification between equity assets) | Vol +0.43pp (11.12% → 11.55%) | Higher vol narrows calendar-year loss headroom | Confirmed ✓ |
| **Constraint/bound** | Impose 35% per-asset cap on IV baseline | GovBond (43.48%) cap binds; weight redistributed to other assets | Cap binds: GovBond capped at 35%; CorpBond rises to 33.33% | Constraint is active; redistribution shifts risk to CorpBond | Confirmed ✓ |
| **Turnover/cost** | 25bps all-in transaction cost applied | Net return decreases by exactly 25bps | Net return 6.55% vs. gross 6.80% (−0.25pp) | CPI+4% objective harder to meet net-of-cost | Confirmed ✓ |

All 4 perturbation directions matched pre-run predictions.

---

## Part 6 — Two AI Dispositions

### System A — Risk Parity

**Recommendation:** Equal risk contribution from all 4 assets.

| Claim | Tag | Independent verification |
|---|---|---|
| Risk parity is more diversified than inverse-vol | `output-supported` | **Verified:** IV weights do not equalize risk contributions when assets are correlated; USEquity at 31.6% contributes disproportionate variance via 0.75 correlation with IntlEquity. Mathematically correct. |
| Bonds and equities should contribute equally to portfolio risk | `assumption-dependent` | Contradicts the 60/40 benchmark stated in the mandate; requires CIO override not supplied in the case |
| Historical risk parity outperforms 60/40 | `unsupported` | Inputs are synthetic teaching data with no historical sample; no performance evidence exists or is applicable here |

### System B — Mean-Variance Optimization

**Recommendation:** Maximize Sharpe ratio subject to long-only, 60/40 target.

| Claim | Tag | Independent verification |
|---|---|---|
| Minimum-variance portfolio has lower volatility than IV weights | `output-supported` | **Verified:** By construction, minimum-variance optimizes over all feasible allocations; IV-within-60/40 is feasible but not optimal — direction confirmed directionally |
| Expected returns from asset_statistics.csv are forward forecasts | `unsupported` | Handout explicitly states: "teaching inputs, not estimates from a historical sample" — categorically not forecasts |
| Sharpe ratio maximization requires a risk-free rate | `assumption-dependent` | No risk-free rate supplied in mandate or course data; any rate chosen would be an invented assumption |

### AI-Closed Decision

Both systems agree the CIO optimization criterion is unresolved. System A invents an equal-risk-contribution objective absent from the mandate. System B requires a risk-free rate not supplied. Neither output can be adopted. The mechanics-probe (IV-within-60/40) remains the only mandate-consistent allocation — and it cannot be adopted either until the CIO question is resolved.

**Decision without AI:** DEFERRED_NO_ADOPTABLE_CANDIDATE.

---

## Part 7 — Decision Record

| Element | Content |
|---|---|
| **Action** | **DEFERRED** — no adoptable candidate; CIO must resolve optimization criterion before adoption |
| **Acceptable range** | Bond 35–45%, Equity 55–65%; IV-within-class weighting is defensible as a mechanics probe |
| **Baseline & net-of-cost** | Candidate 6.80% gross / 6.55% net vs. equal-weight 6.50%; candidate vol 11.12% vs. EW 9.80% |
| **Most fragile input** | Expected return assumptions — teaching inputs, not real forecasts; any live application requires independently sourced, dated return estimates |
| **Binding constraint** | CIO optimization criterion undefined — this is the single blocking issue |
| **Unresolved ambiguity** | Return maximization vs. tracking-error vs. distribution-probability — three materially different optimizer objectives |
| **Monitoring trigger** | If USEquity↔IntlEquity correlation rises above 0.85 in quarterly review, rebalance equity sleeve (stress test: +0.43pp vol impact at 0.90) |
| **Owner / frequency** | Meridian Foundation investment committee; quarterly review per mandate |
| **Reversal evidence** | CIO states optimization criterion → re-run with stated objective → return for adoption decision |

---

## Submission Checklist

| Required item | Status |
|---|---|
| Mandate restated (from Lab 13) | ✅ Part 1 |
| Input conventions (frequency, provenance, as-of) | ✅ Part 2 |
| Covariance matrix constructed | ✅ Part 3 |
| 2 manual covariance cells reconciled | ✅ Part 3 |
| Equal-weight baseline (weights + return + vol) | ✅ Part 4 |
| Inverse-volatility baseline (weights + return + vol) | ✅ Part 4 |
| Candidate allocation with explicit provisional objective | ✅ Part 4 |
| Constraint audit | ✅ Part 4 |
| Sum-to-one verified (all 3 portfolios) | ✅ Part 4 |
| CIO ambiguity labeled DEFERRED_NO_ADOPTABLE_CANDIDATE | ✅ Parts 4 & 7 |
| 4 perturbation tests with pre-run predictions | ✅ Part 5 |
| Two AI dispositions with claim tags | ✅ Part 6 |
| First claim from each system independently verified | ✅ Part 6 |
| AI-closed decision | ✅ Part 6 |
| Decision record (all 7 elements) | ✅ Part 7 |

---

## Checkout

| Item | Location |
|---|---|
| Lab 14 script | https://github.com/WGdearY/TICKER-research/blob/main/portfolio_nke.py |
| Lab 14 report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_14.md |
| Lab 13 mandate | https://github.com/WGdearY/TICKER-research/blob/main/mandate_1015_NKE.md |
| Full repository | https://github.com/WGdearY/TICKER-research |
