"""FIN 43900 Week 5 Lab 09 — Pro-Forma Financial Modeling I: Base Case Build (ABG).

Author: Will Gao (gao713@purdue.edu)
Standard library only. Builds 5-year three-statement pro-forma model for
Asbury Automotive Group (ABG) from opening balance sheet and 15 labeled assumptions.
Proves model on known answer ($291.75 per share) and asserts balancing.
"""

from __future__ import annotations


def run_proforma(break_test: bool = False) -> dict:
    # ---------------------------------------------------------
    # 1. Opening Balance Sheet FY2025 (USD millions)
    # ---------------------------------------------------------
    rev_0 = 17999.0
    inv_0 = 2135.8
    ppe_0 = 3070.4
    other_assets_0 = 6371.6
    cash_0 = 40.4
    fp_0 = 2027.0
    debt_0 = 3572.0
    other_liab_0 = 2127.5
    equity_0 = 3891.7
    revolver_0 = 0.0

    # ---------------------------------------------------------
    # 2. Assumption Set (15 Labeled Assumptions)
    # ---------------------------------------------------------
    growth = 0.018                                    # Organic revenue growth: 1.8%/yr (judgment)
    gross_margin = 0.1705                             # Gross margin: 17.05% (judgment)
    sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645] # SG&A ÷ gross profit 2026->2030 (judgment)
    depr_ratio = 82.4 / 3070.4                        # Depreciation ÷ opening PP&E (history)
    impairment = 120.0                                # Non-cash impairment: 120/yr (judgment)
    capex = 250.0                                     # Capital spending: 250/yr (guidance)
    tax_rate = 0.255                                  # Tax rate: 25.5% (judgment)
    inv_days = 2135.8 / (17999.0 - 3071.7) * 365.0    # Inventory days (history)
    fp_ratio = 2027.0 / 2135.8                        # Floor plan ÷ inventory (history)
    owc_ratio = 0.008                                 # Other working capital: 0.8% of delta rev (judgment)
    min_cash = 25.0                                   # Minimum cash (history)
    revolver_limit = 850.0                            # Revolver limit (judgment)
    revolver_rate = 0.06                              # Revolver interest rate: 6% (judgment)
    repayment = 150.0                                 # Term debt repayment: 150/yr (judgment)
    buyback = 150.0                                   # Share buyback: 150/yr (judgment)
    fp_rate = 0.0467                                  # Floor plan interest rate: 4.67% (history)
    debt_rate = 0.0544                                # Term debt interest rate: 5.44% (history)
    cost_of_equity = 0.10                             # Cost of equity: 10% (judgment)
    terminal_growth = 0.025                           # Terminal growth rate: 2.5% (judgment)
    shares = 17.951349                                # Shares outstanding: 17.951349M (fact: 10-Q)

    years = [2026, 2027, 2028, 2029, 2030]

    # Containers for statement outputs
    income_statement = []
    balance_sheet = []
    cash_flow = []
    checks = []

    # State variables tracking opening figures
    prev_rev = rev_0
    prev_inv = inv_0
    prev_ppe = ppe_0
    prev_other_assets = other_assets_0
    prev_cash = cash_0
    prev_fp = fp_0
    prev_debt = debt_0
    prev_other_liab = other_liab_0
    prev_equity = equity_0
    prev_revolver = revolver_0

    for idx, year in enumerate(years):
        # -----------------------------------------------------
        # Step A: Income Statement
        # -----------------------------------------------------
        rev = prev_rev * (1.0 + growth)
        gp = rev * gross_margin
        sga = gp * sga_ratios[idx]
        depr = prev_ppe * depr_ratio
        ebit = gp - sga - depr - impairment
        interest = prev_fp * fp_rate + prev_debt * debt_rate + prev_revolver * revolver_rate
        pretax = ebit - interest
        tax = max(0.0, pretax) * tax_rate
        ni = pretax - tax

        income_statement.append({
            "year": year,
            "revenue": rev,
            "gross_profit": gp,
            "sga": sga,
            "depreciation": depr,
            "impairment": impairment,
            "ebit": ebit,
            "interest": interest,
            "pretax": pretax,
            "tax": tax,
            "net_income": ni,
        })

        # -----------------------------------------------------
        # Step B: Balance Sheet (Except Cash)
        # -----------------------------------------------------
        cogs = rev - gp
        inv = cogs * inv_days / 365.0
        fp = inv * fp_ratio
        ppe = prev_ppe + capex - depr
        delta_rev = rev - prev_rev
        other_assets = prev_other_assets + owc_ratio * delta_rev - impairment
        debt = prev_debt - repayment
        other_liab = prev_other_liab
        equity = prev_equity + ni - buyback

        # -----------------------------------------------------
        # Step C: Free Cash Flow to Equity (FCFE)
        # -----------------------------------------------------
        delta_inv = inv - prev_inv
        delta_owc = owc_ratio * delta_rev
        delta_fp = fp - prev_fp

        fcfe = (
            ni
            + depr
            + impairment
            - capex
            - delta_inv
            - delta_owc
            + delta_fp
            - repayment
        )

        # -----------------------------------------------------
        # Step D: Cash, Revolver, and Liquidity
        # -----------------------------------------------------
        prelim_cash = prev_cash + fcfe - buyback
        revolver = prev_revolver
        revolver_borrow = 0.0
        revolver_repay = 0.0

        if prelim_cash < min_cash:
            shortfall = min_cash - prelim_cash
            borrow = min(shortfall, revolver_limit - revolver)
            revolver += borrow
            revolver_borrow = borrow
            cash = prelim_cash + borrow
        else:
            excess = prelim_cash - min_cash
            repay = min(excess, revolver)
            revolver -= repay
            revolver_repay = repay
            cash = prelim_cash - repay

        # In swap-and-break test: break 2026 cash to opening cash (40.4)
        if break_test and year == 2026:
            cash = cash_0

        cash_flow.append({
            "year": year,
            "net_income": ni,
            "depreciation": depr,
            "impairment": impairment,
            "capex": capex,
            "delta_inv": delta_inv,
            "delta_owc": delta_owc,
            "delta_fp": delta_fp,
            "debt_repayment": repayment,
            "fcfe": fcfe,
            "buyback": buyback,
            "revolver_net": revolver_borrow - revolver_repay,
            "net_change_cash": cash - prev_cash,
            "cash": cash,
        })

        balance_sheet.append({
            "year": year,
            "cash": cash,
            "inventory": inv,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": cash + inv + ppe + other_assets,
            "floor_plan": fp,
            "debt": debt,
            "revolver": revolver,
            "other_liab": other_liab,
            "total_liab": fp + debt + revolver + other_liab,
            "equity": equity,
            "total_liab_equity": fp + debt + revolver + other_liab + equity,
        })

        # -----------------------------------------------------
        # Step E: Checks
        # -----------------------------------------------------
        assets = cash + inv + ppe + other_assets
        liab_eq = fp + debt + revolver + other_liab + equity
        gap = assets - liab_eq
        checks.append({
            "year": year,
            "assets_minus_liab_equity": gap,
            "cash_at_or_above_min": cash >= (min_cash - 1e-4),
            "cash": cash,
        })

        # Advance state to next year
        prev_rev = rev
        prev_inv = inv
        prev_ppe = ppe
        prev_other_assets = other_assets
        prev_cash = cash
        prev_fp = fp
        prev_debt = debt
        prev_other_liab = other_liab
        prev_equity = equity
        prev_revolver = revolver

    # ---------------------------------------------------------
    # 3. Assert Balanced Check Function
    # ---------------------------------------------------------
    assert_balanced(checks)

    # ---------------------------------------------------------
    # 4. Valuation
    # ---------------------------------------------------------
    pv_fcfe_list = [
        cf["fcfe"] / ((1.0 + cost_of_equity) ** (i + 1))
        for i, cf in enumerate(cash_flow)
    ]
    pv_explicit_fcfe = sum(pv_fcfe_list)

    # Terminal value at 2030: (2030 FCFE + 2030 repayment) * (1 + g) / (Ke - g)
    terminal_cash_flow = (cash_flow[-1]["fcfe"] + repayment) * (1.0 + terminal_growth)
    terminal_value_2030 = terminal_cash_flow / (cost_of_equity - terminal_growth)
    pv_terminal_value = terminal_value_2030 / ((1.0 + cost_of_equity) ** len(years))

    total_equity_value = pv_explicit_fcfe + pv_terminal_value
    share_of_value_after_2030 = pv_terminal_value / total_equity_value
    value_per_share = total_equity_value / shares

    valuation = {
        "pv_explicit_fcfe": pv_explicit_fcfe,
        "terminal_cash_flow_2031": terminal_cash_flow,
        "terminal_value_2030": terminal_value_2030,
        "pv_terminal_value": pv_terminal_value,
        "total_equity_value": total_equity_value,
        "share_of_value_after_2030": share_of_value_after_2030,
        "shares_outstanding": shares,
        "value_per_share": value_per_share,
    }

    return {
        "income_statement": income_statement,
        "balance_sheet": balance_sheet,
        "cash_flow": cash_flow,
        "checks": checks,
        "valuation": valuation,
    }


def assert_balanced(checks: list[dict]) -> None:
    """Raises an error naming the year and the gap if any balance check fails."""
    for c in checks:
        gap = c["assets_minus_liab_equity"]
        year = c["year"]
        if abs(gap) > 0.01:
            raise ValueError(f"Balance sheet check failed in FY{year}E: Gap is {gap:.1f} (Assets != Liabilities + Equity)")
        if not c["cash_at_or_above_min"]:
            raise ValueError(f"Liquidity check failed in FY{year}E: Cash ({c['cash']:.1f}) is below minimum")


def print_table(title: str, rows: list[tuple[str, list[float]]], years: list[int]) -> None:
    header = f"{title:<34s}" + "".join(f"{y:>12d}E" for y in years)
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))
    for label, vals in rows:
        line = f"{label:<34s}" + "".join(f"{v:>13.1f}" for v in vals)
        print(line)


def main() -> None:
    print("Running Lab 09 Three-Statement Pro-Forma Engine (ABG Case)...")
    res = run_proforma(break_test=False)
    years = [c["year"] for c in res["income_statement"]]

    # 1. Print Income Statement
    is_rows = [
        ("Revenue", [r["revenue"] for r in res["income_statement"]]),
        ("Gross Profit", [r["gross_profit"] for r in res["income_statement"]]),
        ("SG&A Expense", [r["sga"] for r in res["income_statement"]]),
        ("Depreciation", [r["depreciation"] for r in res["income_statement"]]),
        ("Impairment (non-cash)", [r["impairment"] for r in res["income_statement"]]),
        ("Operating Income (EBIT)", [r["ebit"] for r in res["income_statement"]]),
        ("Interest Expense", [r["interest"] for r in res["income_statement"]]),
        ("Pretax Income", [r["pretax"] for r in res["income_statement"]]),
        ("Income Tax", [r["tax"] for r in res["income_statement"]]),
        ("Net Income", [r["net_income"] for r in res["income_statement"]]),
    ]
    print_table("INCOME STATEMENT (USD M)", is_rows, years)

    # 2. Print Balance Sheet
    bs_rows = [
        ("Cash & Equivalents", [r["cash"] for r in res["balance_sheet"]]),
        ("Inventory", [r["inventory"] for r in res["balance_sheet"]]),
        ("PP&E (net)", [r["ppe"] for r in res["balance_sheet"]]),
        ("Other Assets", [r["other_assets"] for r in res["balance_sheet"]]),
        ("TOTAL ASSETS", [r["total_assets"] for r in res["balance_sheet"]]),
        ("Floor Plan Notes Payable", [r["floor_plan"] for r in res["balance_sheet"]]),
        ("Term Debt", [r["debt"] for r in res["balance_sheet"]]),
        ("Revolving Credit", [r["revolver"] for r in res["balance_sheet"]]),
        ("Other Liabilities", [r["other_liab"] for r in res["balance_sheet"]]),
        ("Total Liabilities", [r["total_liab"] for r in res["balance_sheet"]]),
        ("Common Stockholders' Equity", [r["equity"] for r in res["balance_sheet"]]),
        ("TOTAL LIABILITIES & EQUITY", [r["total_liab_equity"] for r in res["balance_sheet"]]),
    ]
    print_table("BALANCE SHEET (USD M)", bs_rows, years)

    # 3. Print Cash Flow Statement
    cf_rows = [
        ("Net Income", [r["net_income"] for r in res["cash_flow"]]),
        ("(+) Depreciation", [r["depreciation"] for r in res["cash_flow"]]),
        ("(+) Non-cash Impairment", [r["impairment"] for r in res["cash_flow"]]),
        ("(-) Capital Expenditures", [-r["capex"] for r in res["cash_flow"]]),
        ("(-) Change in Inventory", [-r["delta_inv"] for r in res["cash_flow"]]),
        ("(-) Change in Other Working Cap", [-r["delta_owc"] for r in res["cash_flow"]]),
        ("(+) Change in Floor Plan", [r["delta_fp"] for r in res["cash_flow"]]),
        ("(-) Term Debt Repayment", [-r["debt_repayment"] for r in res["cash_flow"]]),
        ("Free Cash Flow to Equity (FCFE)", [r["fcfe"] for r in res["cash_flow"]]),
        ("(-) Share Buybacks", [-r["buyback"] for r in res["cash_flow"]]),
        ("(+/-) Revolver Draw/(Repay)", [r["revolver_net"] for r in res["cash_flow"]]),
        ("Net Change in Cash", [r["net_change_cash"] for r in res["cash_flow"]]),
        ("Ending Cash Balance", [r["cash"] for r in res["cash_flow"]]),
    ]
    print_table("CASH FLOW STATEMENT (USD M)", cf_rows, years)

    # 4. Print Checks
    chk_rows = [
        ("Assets − Liabilities − Equity", [r["assets_minus_liab_equity"] for r in res["checks"]]),
        ("Cash Year-End", [r["cash"] for r in res["checks"]]),
    ]
    print_table("BALANCE & LIQUIDITY CHECKS", chk_rows, years)

    # 5. Print Valuation Summary
    val = res["valuation"]
    print("\n" + "=" * 50)
    print("VALUATION SUMMARY (ABG Known-Answer Test)")
    print("=" * 50)
    print(f"PV of 5-Year Explicit FCFE      : ${val['pv_explicit_fcfe']:>10.1f} M")
    print(f"Terminal Year Cash Flow (2031E) : ${val['terminal_cash_flow_2031']:>10.1f} M")
    print(f"Terminal Value at 2030E         : ${val['terminal_value_2030']:>10.1f} M")
    print(f"PV of Terminal Value            : ${val['pv_terminal_value']:>10.1f} M")
    print(f"Total Equity Value              : ${val['total_equity_value']:>10.1f} M")
    print(f"Diluted Shares Outstanding      : {val['shares_outstanding']:>10.6f} M")
    print("-" * 50)
    print(f"Share of Value after 2030 (TV%) : {val['share_of_value_after_2030']:>10.1%}")
    print(f"Value per Diluted Share         : ${val['value_per_share']:>10.2f}")
    print("=" * 50)

    # Reconcile key known answer table
    print("\n=== Known Answer Reconciliation ===")
    chk_26 = res["income_statement"][0]
    chk_30 = res["income_statement"][-1]
    cf_26 = res["cash_flow"][0]
    cf_30 = res["cash_flow"][-1]
    b_26 = res["checks"][0]
    b_30 = res["checks"][-1]

    benchmarks = [
        ("Revenue", chk_26["revenue"], 18323.0, chk_30["revenue"], 19678.3),
        ("Operating Income", chk_26["ebit"], 844.2, chk_30["ebit"], 971.4),
        ("Net Income", chk_26["net_income"], 413.6, chk_30["net_income"], 527.5),
        ("Free Cash Flow to Equity", cf_26["fcfe"], 211.4, cf_30["fcfe"], 342.3),
        ("Cash, year end", cf_26["cash"], 101.8, cf_30["cash"], 719.8),
        ("Assets − Liab − Equity", b_26["assets_minus_liab_equity"], 0.0, b_30["assets_minus_liab_equity"], 0.0),
    ]

    all_match = True
    print(f"{'Line':<26s}{'FY26 Actual':>12s}{'FY26 Target':>12s}{'FY30 Actual':>12s}{'FY30 Target':>12s}{'Match':>8s}")
    print("-" * 70)
    for name, a26, t26, a30, t30 in benchmarks:
        match = (abs(a26 - t26) < 0.1) and (abs(a30 - t30) < 0.1)
        if not match:
            all_match = False
        print(f"{name:<26s}{a26:>12.1f}{t26:>12.1f}{a30:>12.1f}{t30:>12.1f}{'PASS' if match else 'FAIL':>8s}")

    share_match = abs(val["value_per_share"] - 291.75) < 0.01
    print(f"{'Value per share':<26s}{val['value_per_share']:>12.2f}{'$291.75':>12s}{'':>12s}{'':>12s}{'PASS' if share_match else 'FAIL':>8s}")

    if all_match and share_match:
        print("\n[SUCCESS] Model perfectly matches all ABG benchmark targets to the exact decimal!")
    else:
        print("\n[WARNING] Discrepancies detected against benchmark targets.")

    # Swap and break demonstration
    print("\n=== Swap-and-Break Demonstration ===")
    print("Testing intentional balance sheet failure (forcing FY2026 cash = $40.4M opening balance)...")
    try:
        run_proforma(break_test=True)
    except ValueError as e:
        print(f"Captured expected refusal: {e}")
        print("Test passed: The model refuses to value an unbalanced balance sheet!")


if __name__ == "__main__":
    main()
