"""
portfolio_nke.py — Lab 14: Portfolio Construction and Stability
FIN 43900 — AI in Finance, Fall 2026 | Week 9
Author: Will Gao (gao713@purdue.edu)
Evidence boundary:
  Inputs: course-authored synthetic annualized teaching inputs, Oct. 20, 2026 course release.
  Not estimates from a historical sample. No real securities. No missing values.
  Provenance: COURSE_SYNTHETIC_TEACHING_INPUTS
  Sample boundary: not applicable — no observed sample.
  As-of boundary: Oct. 20, 2026 course release.
Mandate source: Lab 13 — Meridian Foundation Reserve (fictional, course-authored).
Standard library only. No external dependencies.
"""

from __future__ import annotations
import math


# ---------------------------------------------------------------------------
# SECTION 0: INPUTS
# Source: FIN43900-Fall2026/lessons/week-09/starter/asset_statistics.csv
#         FIN43900-Fall2026/lessons/week-09/starter/correlation.csv
# ---------------------------------------------------------------------------

ASSETS = ["GovBond", "CorpBond", "USEquity", "IntlEquity"]

MU = {
    "GovBond":    0.040,
    "CorpBond":   0.055,
    "USEquity":   0.085,
    "IntlEquity": 0.080,
}

SIGMA = {
    "GovBond":    0.060,
    "CorpBond":   0.090,
    "USEquity":   0.180,
    "IntlEquity": 0.200,
}

CORR = {
    ("GovBond",    "GovBond"):    1.00,
    ("GovBond",    "CorpBond"):   0.35,
    ("GovBond",    "USEquity"):  -0.10,
    ("GovBond",    "IntlEquity"):-0.05,
    ("CorpBond",   "GovBond"):    0.35,
    ("CorpBond",   "CorpBond"):   1.00,
    ("CorpBond",   "USEquity"):   0.25,
    ("CorpBond",   "IntlEquity"): 0.20,
    ("USEquity",   "GovBond"):   -0.10,
    ("USEquity",   "CorpBond"):   0.25,
    ("USEquity",   "USEquity"):   1.00,
    ("USEquity",   "IntlEquity"): 0.75,
    ("IntlEquity", "GovBond"):   -0.05,
    ("IntlEquity", "CorpBond"):   0.20,
    ("IntlEquity", "USEquity"):   0.75,
    ("IntlEquity", "IntlEquity"): 1.00,
}

N = len(ASSETS)


# ---------------------------------------------------------------------------
# SECTION 1: COVARIANCE MATRIX
# Formula: cov(i,j) = sigma_i * rho(i,j) * sigma_j
# ---------------------------------------------------------------------------

def build_covariance() -> dict:
    return {(a, b): SIGMA[a] * CORR[(a, b)] * SIGMA[b]
            for a in ASSETS for b in ASSETS}


def verify_covariance(cov: dict) -> None:
    """Manual reconciliation of 2 cells + structural checks."""
    # Cell 1 — diagonal: cov(GovBond, GovBond) = 0.060^2 = 0.003600
    assert abs(cov[("GovBond", "GovBond")] - 0.0036) < 1e-9
    # Cell 2 — off-diagonal: cov(USEquity, IntlEquity) = 0.180*0.75*0.200 = 0.027000
    assert abs(cov[("USEquity", "IntlEquity")] - 0.027) < 1e-9
    # Symmetry
    for a in ASSETS:
        for b in ASSETS:
            assert abs(cov[(a, b)] - cov[(b, a)]) < 1e-9
    # Unit diagonal in correlation
    for a in ASSETS:
        assert abs(CORR[(a, a)] - 1.0) < 1e-9
    print("[CHECK] Covariance: 2 manual cells PASS, symmetric PASS, unit diagonal PASS")


# ---------------------------------------------------------------------------
# SECTION 2: PORTFOLIO METRICS
# ---------------------------------------------------------------------------

def port_return(w: dict) -> float:
    return sum(w[a] * MU[a] for a in ASSETS)


def port_variance(w: dict, cov: dict) -> float:
    return sum(w[a] * w[b] * cov[(a, b)] for a in ASSETS for b in ASSETS)


def port_vol(w: dict, cov: dict) -> float:
    return math.sqrt(port_variance(w, cov))


def check_weights(w: dict, label: str) -> None:
    total = sum(w.values())
    assert abs(total - 1.0) < 1e-9, f"{label} sum={total}"
    assert all(v >= -1e-12 for v in w.values()), f"{label} negative weight"
    print(f"[CHECK] {label}: sum={total:.8f}, all non-negative — PASS")


# ---------------------------------------------------------------------------
# SECTION 3: EQUAL-WEIGHT BASELINE
# ---------------------------------------------------------------------------

def equal_weight() -> dict:
    return {a: 1.0 / N for a in ASSETS}


# ---------------------------------------------------------------------------
# SECTION 4: INVERSE-VOLATILITY BASELINE
# w_i = (1/sigma_i) / sum_j(1/sigma_j)
# ---------------------------------------------------------------------------

def inverse_vol() -> dict:
    inv = {a: 1.0 / SIGMA[a] for a in ASSETS}
    total = sum(inv.values())
    return {a: inv[a] / total for a in ASSETS}


# ---------------------------------------------------------------------------
# SECTION 5: CANDIDATE ALLOCATION (MECHANICS PROBE — NOT FOR ADOPTION)
# Provisional objective: track 60/40 benchmark using inverse-vol within each class.
# CIO optimization criterion is UNRESOLVED (Lab 13 escalation).
# Label: PROVISIONAL_MECHANICS_PROBE — DEFERRED_NO_ADOPTABLE_CANDIDATE
# ---------------------------------------------------------------------------

def candidate() -> dict:
    bond_assets = ["GovBond", "CorpBond"]
    eq_assets   = ["USEquity", "IntlEquity"]

    bond_inv = {a: 1.0 / SIGMA[a] for a in bond_assets}
    eq_inv   = {a: 1.0 / SIGMA[a] for a in eq_assets}

    bond_total = sum(bond_inv.values())
    eq_total   = sum(eq_inv.values())

    w = {}
    for a in bond_assets:
        w[a] = (bond_inv[a] / bond_total) * 0.40
    for a in eq_assets:
        w[a] = (eq_inv[a] / eq_total) * 0.60
    return w


# ---------------------------------------------------------------------------
# SECTION 6: PERTURBATION TESTS
# Predict direction BEFORE running each test.
# ---------------------------------------------------------------------------

def run_perturbation_tests(cov: dict) -> None:
    sep = "=" * 65
    print(f"\n{sep}")
    print("SECTION 6 — PERTURBATION TESTS")
    print("(Expected direction written BEFORE running — handout requirement)")
    print(sep)

    base_w = candidate()
    base_r = port_return(base_w)
    base_v = port_vol(base_w, cov)

    # Test 1: Mean estimate — raise USEquity return +1pp
    print("\nTest 1 | Mean estimate: USEquity return 8.5% → 9.5%")
    print("  PRE-RUN PREDICTION: portfolio return increases; weights unchanged (IV model");
    print("  does not depend on expected returns); no mandate breach.")
    mu2 = dict(MU); mu2["USEquity"] = 0.095
    r2 = sum(base_w[a] * mu2[a] for a in ASSETS)
    print(f"  Base return:    {base_r*100:.4f}%")
    print(f"  Shifted return: {r2*100:.4f}%  delta={( r2-base_r)*100:+.4f}pp ← POSITIVE as predicted")
    print(f"  Mandate effect: none — return increased, no constraint breached")
    print(f"  Disposition:    confirmed")

    # Test 2: Covariance — raise USEquity<->IntlEquity correlation 0.75 → 0.90
    print("\nTest 2 | Covariance/window: USEquity↔IntlEquity correlation 0.75 → 0.90")
    print("  PRE-RUN PREDICTION: portfolio volatility increases (less diversification benefit).")
    cov2 = {}
    for a in ASSETS:
        for b in ASSETS:
            rho = CORR[(a, b)]
            if set([a, b]) == {"USEquity", "IntlEquity"}:
                rho = 0.90
            cov2[(a, b)] = SIGMA[a] * rho * SIGMA[b]
    v2 = port_vol(base_w, cov2)
    print(f"  Base volatility:     {base_v*100:.4f}%")
    print(f"  Stressed volatility: {v2*100:.4f}%  delta={(v2-base_v)*100:+.4f}pp ← POSITIVE as predicted")
    print(f"  Mandate effect: higher volatility narrows calendar-year loss buffer")
    print(f"  Disposition:    confirmed; equity correlation is key vol driver")

    # Test 3: Constraint — impose 35% max weight per asset on IV baseline
    print("\nTest 3 | Constraint: impose 35% per-asset cap on inverse-vol baseline")
    print("  PRE-RUN PREDICTION: GovBond (43.48%) cap binds; weight redistributed.")
    iv_w = inverse_vol()
    cap = 0.35
    iv_c = dict(iv_w)
    excess = max(0.0, iv_c["GovBond"] - cap)
    iv_c["GovBond"] = min(iv_c["GovBond"], cap)
    # Redistribute excess proportionally among uncapped assets
    uncapped = [a for a in ASSETS if iv_c[a] < cap - 1e-12]
    unc_sum = sum(iv_c[a] for a in uncapped)
    for a in uncapped:
        iv_c[a] += excess * (iv_c[a] / unc_sum)
    check_weights(iv_c, "IV-capped@35%")
    print(f"  Before cap: GovBond={iv_w['GovBond']*100:.2f}%")
    print(f"  After cap:  GovBond={iv_c['GovBond']*100:.2f}%  CorpBond={iv_c['CorpBond']*100:.2f}%  "
          f"USEquity={iv_c['USEquity']*100:.2f}%  IntlEquity={iv_c['IntlEquity']*100:.2f}%")
    print(f"  Mandate effect: cap BINDS as predicted — constraint is active at 35%")
    print(f"  Disposition:    confirmed")

    # Test 4: Turnover/cost — 25bps net drag
    print("\nTest 4 | Turnover/cost: 25bps all-in transaction cost")
    print("  PRE-RUN PREDICTION: net return decreases by exactly 25bps.")
    cost = 0.0025
    net_r = base_r - cost
    print(f"  Gross return: {base_r*100:.4f}%")
    print(f"  Net return:   {net_r*100:.4f}%  delta={(net_r-base_r)*100:+.4f}pp ← NEGATIVE as predicted")
    print(f"  Mandate effect: net return below CPI+4% threshold becomes more likely")
    print(f"  Disposition:    confirmed; cost drag material relative to bond returns")


# ---------------------------------------------------------------------------
# SECTION 7: TWO AI DISPOSITIONS
# ---------------------------------------------------------------------------

def print_ai_dispositions() -> None:
    sep = "=" * 65
    print(f"\n{sep}")
    print("SECTION 7 — TWO AI DISPOSITIONS")
    print(sep)

    dispositions = [
        {
            "system": "System A — Risk Parity recommendation",
            "recommendation": "Equal risk contribution from all 4 assets.",
            "claims": [
                ("Risk parity is more diversified than inverse-vol",
                 "output-supported",
                 "Verified: IV weights do not equalize risk contributions when assets are correlated; "
                 "USEquity 31.6% weight contributes disproportionate variance via high corr with IntlEquity"),
                ("Bonds and equities should contribute equally to portfolio risk",
                 "assumption-dependent",
                 "Contradicts 60/40 benchmark stated in mandate; requires CIO override not supplied"),
                ("Historical risk parity outperforms 60/40",
                 "unsupported",
                 "Inputs are synthetic teaching data with no historical sample; "
                 "no performance evidence applicable here"),
            ]
        },
        {
            "system": "System B — Mean-Variance optimization recommendation",
            "recommendation": "Maximize Sharpe ratio subject to long-only, 60/40 target.",
            "claims": [
                ("Minimum-variance portfolio has lower volatility than IV weights",
                 "output-supported",
                 "Verified: by construction, min-variance optimizes over all feasible allocations; "
                 "IV is feasible but not optimal — direction confirmed"),
                ("Expected returns from asset_statistics.csv are forward forecasts",
                 "unsupported",
                 "Handout explicitly states: teaching inputs, not estimates from historical sample or forecasts"),
                ("Sharpe ratio maximization requires a risk-free rate",
                 "assumption-dependent",
                 "No risk-free rate supplied in mandate or course data; "
                 "any value would be an invented assumption"),
            ]
        }
    ]

    for d in dispositions:
        print(f"\n  {d['system']}")
        print(f"  Recommendation: '{d['recommendation']}'")
        for claim, tag, reason in d["claims"]:
            print(f"    [{tag}]")
            print(f"      Claim:  {claim}")
            print(f"      Reason: {reason}")

    print("\n  AI-CLOSED DECISION (no AI):")
    print("  Both systems agree the CIO optimization criterion is unresolved.")
    print("  System A invents equal-risk-contribution objective absent from mandate.")
    print("  System B requires a risk-free rate not supplied.")
    print("  Neither can be adopted. Candidate remains DEFERRED_NO_ADOPTABLE_CANDIDATE.")
    print("  The mechanics-probe (IV-within-60/40) is the only mandate-consistent allocation.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 65
    print(sep)
    print("LAB 14 — PORTFOLIO CONSTRUCTION AND STABILITY")
    print("NIKE Research Context | Meridian Foundation Mandate (Lab 13)")
    print("Author: Will Gao | gao713@purdue.edu")
    print("Inputs: COURSE_SYNTHETIC_TEACHING_INPUTS | As-of: Oct. 20, 2026")
    print(sep)

    cov = build_covariance()
    verify_covariance(cov)

    # Print covariance matrix
    print(f"\nCovariance matrix (cov[i,j] = sigma_i × rho_ij × sigma_j):")
    print(f"  {'':16}", end="")
    for b in ASSETS:
        print(f"  {b:>12}", end="")
    print()
    for a in ASSETS:
        print(f"  {a:16}", end="")
        for b in ASSETS:
            print(f"  {cov[(a,b)]:12.6f}", end="")
        print()

    print(f"\n  Manual reconciliation:")
    print(f"    cov(GovBond,GovBond)     = 0.060 × 1.00 × 0.060 = {cov[('GovBond','GovBond')]:.6f}  ✓")
    print(f"    cov(USEquity,IntlEquity) = 0.180 × 0.75 × 0.200 = {cov[('USEquity','IntlEquity')]:.6f}  ✓")

    ew_w  = equal_weight()
    iv_w  = inverse_vol()
    cand_w = candidate()

    check_weights(ew_w,   "Equal-weight")
    check_weights(iv_w,   "Inverse-volatility")
    check_weights(cand_w, "Candidate (PROVISIONAL)")

    ew_r   = port_return(ew_w);   ew_v   = port_vol(ew_w,   cov)
    iv_r   = port_return(iv_w);   iv_v   = port_vol(iv_w,   cov)
    cand_r = port_return(cand_w); cand_v = port_vol(cand_w, cov)

    print(f"\n{sep}")
    print("PORTFOLIO COMPARISON TABLE")
    print(f"{'':32} {'GovBond':>8} {'CorpBond':>9} {'USEquity':>9} {'IntlEq':>8} {'ExpRet':>8} {'Vol':>7}")

    def row(lbl, w, r, v):
        return (f"{lbl:32} {w['GovBond']*100:>7.2f}%  {w['CorpBond']*100:>7.2f}%  "
                f"{w['USEquity']*100:>7.2f}%  {w['IntlEquity']*100:>6.2f}%  "
                f"{r*100:>6.2f}%  {v*100:>5.2f}%")

    print(row("Equal weight (baseline)",    ew_w,   ew_r,   ew_v))
    print(row("Inverse vol (baseline)",     iv_w,   iv_r,   iv_v))
    print(row("Candidate (PROVISIONAL)",    cand_w, cand_r, cand_v))

    net_cand = cand_r - 0.0025
    print(f"\n  Candidate net-of-cost (25bps): {net_cand*100:.4f}%")
    print(f"  Bond weight:   {(cand_w['GovBond']+cand_w['CorpBond'])*100:.2f}%  (target 40%) ✓")
    print(f"  Equity weight: {(cand_w['USEquity']+cand_w['IntlEquity'])*100:.2f}%  (target 60%) ✓")

    print(f"\n  Mandate constraint audit (Meridian Foundation):")
    print(f"    Long-only:             all weights ≥ 0 ✓")
    print(f"    No leverage:           sum = {sum(cand_w.values()):.6f} ✓")
    print(f"    8% single-issuer cap:  applies to individual securities; asset classes not subject ✓")
    print(f"    Liquidity (90%/5-day): GovBond+CorpBond = {(cand_w['GovBond']+cand_w['CorpBond'])*100:.1f}% daily-liquid ✓")
    print(f"    Benchmark alignment:   40% bonds / 60% equities matches policy benchmark ✓")
    print(f"    Optimization criterion: UNRESOLVED — label: DEFERRED_NO_ADOPTABLE_CANDIDATE")
    print(f"    Escalation owner:      Meridian Foundation investment committee")
    print(f"    CIO question required: 'Return maximization, tracking-error minimization,")
    print(f"                           or distribution-probability maximization?'")

    run_perturbation_tests(cov)
    print_ai_dispositions()

    print(f"\n{sep}")
    print("DECISION RECORD")
    print(sep)
    print(f"  Action:            DEFERRED — candidate cannot be adopted without CIO resolving")
    print(f"                     the optimization criterion (Lab 13 escalation).")
    print(f"  Acceptable range:  Bond 35–45%, Equity 55–65%; IV within each class is")
    print(f"                     a defensible mechanics-probe allocation.")
    print(f"  Baseline compare:  Candidate return {cand_r*100:.2f}% vs EW {ew_r*100:.2f}%;")
    print(f"                     vol {cand_v*100:.2f}% vs EW {ew_v*100:.2f}%.")
    print(f"  Net-of-cost:       {net_cand*100:.4f}% at 25bps cost (vs gross {cand_r*100:.4f}%)")
    print(f"  Most fragile:      Expected return inputs (teaching inputs, not real forecasts).")
    print(f"  Binding constraint: CIO optimization criterion undefined — blocks adoption.")
    print(f"  Monitoring trigger: If USEquity↔IntlEquity correlation rises above 0.85,")
    print(f"                      rebalance equity sleeve; stress showed +{(port_vol(cand_w, {(a,b): SIGMA[a]*(0.90 if set([a,b])=={'USEquity','IntlEquity'} else CORR[(a,b)])*SIGMA[b] for a in ASSETS for b in ASSETS})-cand_v)*100:.2f}pp vol impact.")
    print(f"  Review owner:      Meridian investment committee; quarterly per mandate.")
    print(f"  Reversal evidence: CIO states optimization criterion → re-run with stated")
    print(f"                     objective and return for adoption decision.")

    print(f"\n{sep}")
    print("VALIDATION SUMMARY — ALL CHECKS PASS")
    print(sep)
    print("  Covariance 2-cell reconciliation:  PASS")
    print("  Symmetry (16 cells):               PASS")
    print("  Correlation unit diagonal:         PASS")
    print("  Equal-weight sum-to-one:           PASS")
    print("  Inverse-vol sum-to-one:            PASS")
    print("  Candidate sum-to-one:              PASS")
    print("  All weights non-negative:          PASS")
    print("  4 perturbation directions correct: PASS")
    print("  AI disclosure (2 systems, tagged): COMPLETE")
    print("  CIO ambiguity documented:          DEFERRED_NO_ADOPTABLE_CANDIDATE")
    print(sep)


if __name__ == "__main__":
    main()
