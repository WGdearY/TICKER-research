"""FIN 43900 Week 6 Lab 11 — Pro-Forma Sensitivity: Find and Explain the Drivers (NIKE, Inc. / NKE).

Author: Will Gao (gao713@purdue.edu)
Company: NIKE, Inc. (NYSE: NKE)
Evidence Boundary: FY2026 Form 10-K (filed July 15, 2026) for fiscal year ended May 31, 2026.
Standard library only. Performs one-at-a-time sensitivity analysis on two core operating drivers:
  1. Revenue / Sales Growth Rate Trajectory (Top-Line Volume & Channel Recovery Driver)
  2. Gross Margin Trajectory (Operating Margin & Full-Price Realization Driver)
  (Also includes Operating Reinvestment / CapEx % of Revenue as cross-driver comparison)
Preserves fresh copies of base inputs, reruns linked 3-statement pro-forma model,
verifies accounting checks (Assets - Liabilities - Equity = 0.0), and restores base.
"""

from __future__ import annotations
import copy


def get_base_inputs() -> dict:
    """Returns a fresh, independent dictionary of all base inputs for NIKE, Inc."""
    return {
        # Opening Balance Sheet FY2026 (May 31, 2026, USD millions)
        "rev_0": 46398.0,
        "inv_0": 7501.0,
        "ppe_0": 4796.0,
        "other_assets_0": 17086.0,
        "cash_0": 9027.0,
        "debt_0": 7942.0,
        "revolver_0": 0.0,
        "other_liab_0": 15603.0,
        "equity_0": 14865.0,
        # 19 Labeled Assumptions (Base Case)
        "growths": [0.030, 0.040, 0.050, 0.040, 0.030],
        "gross_margins": [0.4320, 0.4360, 0.4400, 0.4430, 0.4450],
        "sga_ratios": [0.8050, 0.7900, 0.7800, 0.7750, 0.7700],
        "depr_ratio": 747.0 / 4828.0,
        "impairment": 0.0,
        "capex_pct": 0.015,
        "tax_rate": 0.203,
        "inv_days": 7501.0 / 26487.0 * 365.0,
        "fp_ratio": 0.0,
        "fp_rate": 0.0,
        "owc_ratio": 0.010,
        "min_cash": 3000.0,
        "revolver_limit": 3000.0,
        "revolver_rate": 0.055,
        "repayment": 500.0,
        "capital_return": 2500.0,
        "debt_rate": 0.0315,
        "cost_of_equity": 0.090,
        "terminal_growth": 0.025,
        "shares": 1481.0,
    }


def run_proforma(inp: dict, break_test: bool = False) -> dict:
    """Executes 5-year linked pro-forma statements for a given input dictionary."""
    years = [2027, 2028, 2029, 2030, 2031]
    prev_rev = inp["rev_0"]
    prev_inv = inp["inv_0"]
    prev_ppe = inp["ppe_0"]
    prev_other_assets = inp["other_assets_0"]
    prev_cash = inp["cash_0"]
    prev_debt = inp["debt_0"]
    prev_revolver = inp["revolver_0"]
    prev_other_liab = inp["other_liab_0"]
    prev_equity = inp["equity_0"]

    income_statement = []
    balance_sheet = []
    cash_flow = []
    checks = []

    for idx, year in enumerate(years):
        # Income Statement
        g = inp["growths"][idx]
        gm = inp["gross_margins"][idx]
        sga_r = inp["sga_ratios"][idx]

        rev = prev_rev * (1.0 + g)
        gp = rev * gm
        sga = gp * sga_r
        depr = prev_ppe * inp["depr_ratio"]
        ebit = gp - sga - depr - inp["impairment"]
        interest = prev_debt * inp["debt_rate"] + prev_revolver * inp["revolver_rate"]
        pretax = ebit - interest
        tax = max(0.0, pretax) * inp["tax_rate"]
        ni = pretax - tax

        income_statement.append({
            "year": year, "rev": rev, "gp": gp, "sga": sga, "depr": depr,
            "ebit": ebit, "interest": interest, "pretax": pretax, "tax": tax, "ni": ni
        })

        # Balance Sheet (except cash)
        cogs = rev - gp
        inv = cogs * inp["inv_days"] / 365.0
        capex = rev * inp["capex_pct"]
        ppe = prev_ppe + capex - depr
        delta_rev = rev - prev_rev
        other_assets = prev_other_assets + inp["owc_ratio"] * delta_rev - inp["impairment"]
        debt = prev_debt - inp["repayment"]
        other_liab = prev_other_liab
        equity = prev_equity + ni - inp["capital_return"]

        # FCFE calculation
        delta_inv = inv - prev_inv
        delta_owc = inp["owc_ratio"] * delta_rev
        delta_fp = 0.0

        fcfe = ni + depr + inp["impairment"] - capex - delta_inv - delta_owc + delta_fp - inp["repayment"]

        # Dynamic Cash Plug and Revolver
        prelim_cash = prev_cash + fcfe - inp["capital_return"]
        revolver = prev_revolver
        revolver_borrow = 0.0
        revolver_repay = 0.0

        if prelim_cash < inp["min_cash"]:
            shortfall = inp["min_cash"] - prelim_cash
            borrow = min(shortfall, inp["revolver_limit"] - revolver)
            revolver += borrow
            revolver_borrow = borrow
            cash = prelim_cash + borrow
        else:
            excess = prelim_cash - inp["min_cash"]
            repay = min(excess, revolver)
            revolver -= repay
            revolver_repay = repay
            cash = prelim_cash - repay

        if break_test and year == 2027:
            cash = inp["cash_0"]

        cash_flow.append({
            "year": year, "ni": ni, "depr": depr, "capex": capex,
            "delta_inv": delta_inv, "delta_owc": delta_owc, "repayment": inp["repayment"],
            "fcfe": fcfe, "capital_return": inp["capital_return"],
            "revolver_net": revolver_borrow - revolver_repay, "cash": cash
        })

        assets = cash + inv + ppe + other_assets
        liab_eq = debt + revolver + other_liab + equity
        gap = assets - liab_eq
        checks.append({
            "year": year, "gap": gap, "cash_ok": cash >= (inp["min_cash"] - 1e-4), "cash": cash
        })

        prev_rev = rev
        prev_inv = inv
        prev_ppe = ppe
        prev_other_assets = other_assets
        prev_cash = cash
        prev_debt = debt
        prev_revolver = revolver
        prev_other_liab = other_liab
        prev_equity = equity

    for c in checks:
        if abs(c["gap"]) > 0.01:
            raise ValueError(f"Balance check failed in FY{c['year']}E: Gap is {c['gap']:.1f}")

    # Valuation Engine
    pv_fcfe_list = [cf["fcfe"] / ((1.0 + inp["cost_of_equity"]) ** (i + 1)) for i, cf in enumerate(cash_flow)]
    pv_explicit_fcfe = sum(pv_fcfe_list)
    terminal_cash_flow = (cash_flow[-1]["fcfe"] + inp["repayment"]) * (1.0 + inp["terminal_growth"])
    terminal_value_2031 = terminal_cash_flow / (inp["cost_of_equity"] - inp["terminal_growth"])
    pv_terminal_value = terminal_value_2031 / ((1.0 + inp["cost_of_equity"]) ** len(years))
    total_equity_value = pv_explicit_fcfe + pv_terminal_value
    value_per_share = total_equity_value / inp["shares"]

    return {
        "final_rev": income_statement[-1]["rev"],
        "final_ebit": income_statement[-1]["ebit"],
        "final_fcfe": cash_flow[-1]["fcfe"],
        "value_per_share": value_per_share,
        "checks": checks,
        "cash_flow": cash_flow,
        "income_statement": income_statement,
        "balance_sheet": balance_sheet
    }


def run_sensitivity_suite() -> dict:
    """Executes one-at-a-time sensitivity suite across Revenue Growth, Gross Margin, and CapEx."""
    base_inp_initial = get_base_inputs()
    base_res_initial = run_proforma(base_inp_initial)

    base_ebit = base_res_initial["final_ebit"]
    base_fcfe = base_res_initial["final_fcfe"]
    base_val = base_res_initial["value_per_share"]

    runs = []

    # -------------------------------------------------------------
    # Driver 1: Revenue / Sales Growth Rate Trajectory (+/- 1.0 pp)
    # -------------------------------------------------------------
    # Lower (-1.0 pp)
    inp_rev_low = copy.deepcopy(base_inp_initial)
    inp_rev_low["growths"] = [g - 0.010 for g in inp_rev_low["growths"]]
    res_rev_low = run_proforma(inp_rev_low)
    runs.append({
        "driver": "Revenue / Sales Growth Rate",
        "case": "Lower (-1.0 pp: 2.0% -> 2.0%)",
        "input_val": "[2.0%, 3.0%, 4.0%, 3.0%, 2.0%]",
        "rev": res_rev_low["final_rev"],
        "ebit": res_rev_low["final_ebit"],
        "delta_ebit": res_rev_low["final_ebit"] - base_ebit,
        "fcfe": res_rev_low["final_fcfe"],
        "delta_fcfe": res_rev_low["final_fcfe"] - base_fcfe,
        "val": res_rev_low["value_per_share"],
        "delta_val": res_rev_low["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_rev_low["checks"])
    })

    # Base
    runs.append({
        "driver": "Revenue / Sales Growth Rate",
        "case": "Base Case (3.0% -> 3.0%)",
        "input_val": "[3.0%, 4.0%, 5.0%, 4.0%, 3.0%]",
        "rev": base_res_initial["final_rev"],
        "ebit": base_ebit,
        "delta_ebit": 0.0,
        "fcfe": base_fcfe,
        "delta_fcfe": 0.0,
        "val": base_val,
        "delta_val": 0.0,
        "bs_pass": True
    })

    # Higher (+1.0 pp)
    inp_rev_high = copy.deepcopy(base_inp_initial)
    inp_rev_high["growths"] = [g + 0.010 for g in inp_rev_high["growths"]]
    res_rev_high = run_proforma(inp_rev_high)
    runs.append({
        "driver": "Revenue / Sales Growth Rate",
        "case": "Higher (+1.0 pp: 4.0% -> 4.0%)",
        "input_val": "[4.0%, 5.0%, 6.0%, 5.0%, 4.0%]",
        "rev": res_rev_high["final_rev"],
        "ebit": res_rev_high["final_ebit"],
        "delta_ebit": res_rev_high["final_ebit"] - base_ebit,
        "fcfe": res_rev_high["final_fcfe"],
        "delta_fcfe": res_rev_high["final_fcfe"] - base_fcfe,
        "val": res_rev_high["value_per_share"],
        "delta_val": res_rev_high["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_rev_high["checks"])
    })

    # -------------------------------------------------------------
    # Driver 2: Gross Margin Trajectory (+/- 1.0 pp)
    # -------------------------------------------------------------
    # Lower (-1.0 pp)
    inp_gm_low = copy.deepcopy(base_inp_initial)
    inp_gm_low["gross_margins"] = [m - 0.010 for m in inp_gm_low["gross_margins"]]
    res_gm_low = run_proforma(inp_gm_low)
    runs.append({
        "driver": "Gross Margin Trajectory",
        "case": "Lower (-1.0 pp: 42.20% -> 43.50%)",
        "input_val": "Base - 0.010",
        "rev": res_gm_low["final_rev"],
        "ebit": res_gm_low["final_ebit"],
        "delta_ebit": res_gm_low["final_ebit"] - base_ebit,
        "fcfe": res_gm_low["final_fcfe"],
        "delta_fcfe": res_gm_low["final_fcfe"] - base_fcfe,
        "val": res_gm_low["value_per_share"],
        "delta_val": res_gm_low["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_gm_low["checks"])
    })

    # Base
    runs.append({
        "driver": "Gross Margin Trajectory",
        "case": "Base (43.20% -> 44.50%)",
        "input_val": "Base (43.20% -> 44.50%)",
        "rev": base_res_initial["final_rev"],
        "ebit": base_ebit,
        "delta_ebit": 0.0,
        "fcfe": base_fcfe,
        "delta_fcfe": 0.0,
        "val": base_val,
        "delta_val": 0.0,
        "bs_pass": True
    })

    # Higher (+1.0 pp)
    inp_gm_high = copy.deepcopy(base_inp_initial)
    inp_gm_high["gross_margins"] = [m + 0.010 for m in inp_gm_high["gross_margins"]]
    res_gm_high = run_proforma(inp_gm_high)
    runs.append({
        "driver": "Gross Margin Trajectory",
        "case": "Higher (+1.0 pp: 44.20% -> 45.50%)",
        "input_val": "Base + 0.010",
        "rev": res_gm_high["final_rev"],
        "ebit": res_gm_high["final_ebit"],
        "delta_ebit": res_gm_high["final_ebit"] - base_ebit,
        "fcfe": res_gm_high["final_fcfe"],
        "delta_fcfe": res_gm_high["final_fcfe"] - base_fcfe,
        "val": res_gm_high["value_per_share"],
        "delta_val": res_gm_high["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_gm_high["checks"])
    })

    # -------------------------------------------------------------
    # Comparison Reinvestment Driver: CapEx % of Revenue (1.0% to 2.0%)
    # -------------------------------------------------------------
    inp_capex_low = copy.deepcopy(base_inp_initial)
    inp_capex_low["capex_pct"] = 0.010
    res_capex_low = run_proforma(inp_capex_low)
    runs.append({
        "driver": "CapEx % of Revenue",
        "case": "Lower (1.00% of Rev, -0.5 pp)",
        "input_val": "1.00% of Revenue",
        "rev": res_capex_low["final_rev"],
        "ebit": res_capex_low["final_ebit"],
        "delta_ebit": res_capex_low["final_ebit"] - base_ebit,
        "fcfe": res_capex_low["final_fcfe"],
        "delta_fcfe": res_capex_low["final_fcfe"] - base_fcfe,
        "val": res_capex_low["value_per_share"],
        "delta_val": res_capex_low["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_capex_low["checks"])
    })

    runs.append({
        "driver": "CapEx % of Revenue",
        "case": "Base (1.50% of Rev)",
        "input_val": "1.50% of Revenue",
        "rev": base_res_initial["final_rev"],
        "ebit": base_ebit,
        "delta_ebit": 0.0,
        "fcfe": base_fcfe,
        "delta_fcfe": 0.0,
        "val": base_val,
        "delta_val": 0.0,
        "bs_pass": True
    })

    inp_capex_high = copy.deepcopy(base_inp_initial)
    inp_capex_high["capex_pct"] = 0.020
    res_capex_high = run_proforma(inp_capex_high)
    runs.append({
        "driver": "CapEx % of Revenue",
        "case": "Higher (2.00% of Rev, +0.5 pp)",
        "input_val": "2.00% of Revenue",
        "rev": res_capex_high["final_rev"],
        "ebit": res_capex_high["final_ebit"],
        "delta_ebit": res_capex_high["final_ebit"] - base_ebit,
        "fcfe": res_capex_high["final_fcfe"],
        "delta_fcfe": res_capex_high["final_fcfe"] - base_fcfe,
        "val": res_capex_high["value_per_share"],
        "delta_val": res_capex_high["value_per_share"] - base_val,
        "bs_pass": all(abs(c["gap"]) <= 0.01 for c in res_capex_high["checks"])
    })

    # Restore Base and verify equality
    base_inp_restored = get_base_inputs()
    base_res_restored = run_proforma(base_inp_restored)

    base_match = (
        abs(base_res_initial["final_ebit"] - base_res_restored["final_ebit"]) < 1e-4 and
        abs(base_res_initial["final_fcfe"] - base_res_restored["final_fcfe"]) < 1e-4 and
        abs(base_res_initial["value_per_share"] - base_res_restored["value_per_share"]) < 1e-4
    )

    # Spans calculation
    rev_ebit_span = res_rev_high["final_ebit"] - res_rev_low["final_ebit"]
    rev_fcfe_span = res_rev_high["final_fcfe"] - res_rev_low["final_fcfe"]
    rev_val_span = res_rev_high["value_per_share"] - res_rev_low["value_per_share"]

    gm_ebit_span = res_gm_high["final_ebit"] - res_gm_low["final_ebit"]
    gm_fcfe_span = res_gm_high["final_fcfe"] - res_gm_low["final_fcfe"]
    gm_val_span = res_gm_high["value_per_share"] - res_gm_low["value_per_share"]

    capex_ebit_span = res_capex_low["final_ebit"] - res_capex_high["final_ebit"]
    capex_fcfe_span = res_capex_low["final_fcfe"] - res_capex_high["final_fcfe"]
    capex_val_span = res_capex_low["value_per_share"] - res_capex_high["value_per_share"]

    return {
        "base_initial": base_res_initial,
        "base_restored": base_res_restored,
        "base_match": base_match,
        "runs": runs,
        "spans": {
            "rev": {"ebit": rev_ebit_span, "fcfe": rev_fcfe_span, "val": rev_val_span},
            "gm": {"ebit": gm_ebit_span, "fcfe": gm_fcfe_span, "val": gm_val_span},
            "capex": {"ebit": capex_ebit_span, "fcfe": capex_fcfe_span, "val": capex_val_span},
        }
    }


def print_sensitivity_report(data: dict) -> None:
    print("=" * 112)
    print("FIN 43900 LAB 11 — ONE-AT-A-TIME SENSITIVITY TABLE (NIKE, INC. / NKE)")
    print("=" * 112)
    header = f"{'Independent Input / Case':<32} {'FY31E EBIT ($M)':<18} {'FY31E FCFE ($M)':<18} {'Value ($/sh)':<16} {'Checks':<10}"
    print(header)
    print("-" * 112)

    for r in data["runs"]:
        ebit_str = f"{r['ebit']:>8.1f} ({r['delta_ebit']:>+6.1f})"
        fcfe_str = f"{r['fcfe']:>8.1f} ({r['delta_fcfe']:>+6.1f})"
        val_str = f"{r['val']:>7.2f} ({r['delta_val']:>+5.2f})"
        chk_str = "PASS (0.0)" if r["bs_pass"] else "FAIL"
        print(f"{r['case']:<32} {ebit_str:<18} {fcfe_str:<18} {val_str:<16} {chk_str:<10}")

    print("=" * 112)
    print("\n" + "=" * 90)
    print("OUTPUT SPANS OVER TESTED RANGES (MAX − MIN ACROSS VALID RUNS)")
    print("=" * 90)
    print(f"{'Output Metric':<30} {'Revenue Growth (±1.0 pp)':<26} {'Gross Margin (±1.0 pp)':<26} {'CapEx % (1.0%–2.0%)':<22}")
    print("-" * 90)
    print(f"{'FY2031E Operating Profit (EBIT)':<30} ${data['spans']['rev']['ebit']:>8.1f} M{'':<15} ${data['spans']['gm']['ebit']:>8.1f} M{'':<15} ${data['spans']['capex']['ebit']:>8.1f} M")
    print(f"{'FY2031E Free Cash Flow (FCFE)':<30} ${data['spans']['rev']['fcfe']:>8.1f} M{'':<15} ${data['spans']['gm']['fcfe']:>8.1f} M{'':<15} ${data['spans']['capex']['fcfe']:>8.1f} M")
    print(f"{'Value per Diluted Share':<30} ${data['spans']['rev']['val']:>8.2f} /sh{'':<13} ${data['spans']['gm']['val']:>8.2f} /sh{'':<13} ${data['spans']['capex']['val']:>8.2f} /sh")
    print("=" * 90)

    print("\n=== Restored Base Verification ===")
    print(f"Base Initial  : EBIT = ${data['base_initial']['final_ebit']:.1f} M | FCFE = ${data['base_initial']['final_fcfe']:.1f} M | Value = ${data['base_initial']['value_per_share']:.2f}")
    print(f"Base Restored : EBIT = ${data['base_restored']['final_ebit']:.1f} M | FCFE = ${data['base_restored']['final_fcfe']:.1f} M | Value = ${data['base_restored']['value_per_share']:.2f}")
    if data["base_match"]:
        print("[SUCCESS] Restored-base check passed! No input or state contamination occurred.")
    else:
        print("[FAIL] Restored-base check failed!")


if __name__ == "__main__":
    suite_data = run_sensitivity_suite()
    print_sensitivity_report(suite_data)
