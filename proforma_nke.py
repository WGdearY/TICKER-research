"""FIN 43900 Week 5 Lab 10 — Pro-Forma Financial Modeling I: Target Company Engine (NIKE, Inc. / NKE).

Author: Will Gao (gao713@purdue.edu)
Company: NIKE, Inc. (NYSE: NKE)
Evidence Boundary: FY2026 Form 10-K (filed July 15, 2026) for fiscal year ended May 31, 2026.
Standard library only. Builds 5-year three-statement pro-forma model for NIKE, Inc.
from opening balance sheet (May 31, 2026) and 19 labeled assumptions.
Asserts balance sheet equality (Assets - Liabilities - Equity = 0.0) in every year
and refuses to compute valuation if broken.
"""

from __future__ import annotations
import sys


def run_proforma_nke(break_test: bool = False) -> dict:
    # ---------------------------------------------------------
    # 1. Opening Balance Sheet FY2026 (May 31, 2026, USD millions)
    # Sourced directly from FY2026 Form 10-K Consolidated Balance Sheets, p. 57
    # ---------------------------------------------------------
    rev_0 = 46398.0          # FY2026 Revenue (10-K Income Statement, p. 54)
    inv_0 = 7501.0           # FY2026 Ending Inventories (10-K Balance Sheet, p. 57)
    ppe_0 = 4796.0           # FY2026 Net Property, Plant and Equipment (10-K Balance Sheet, p. 57)
    other_assets_0 = 17086.0 # FY2026 Other Assets (Receivables, ROU assets, Intangibles, etc.)
    cash_0 = 9027.0          # Cash & equivalents ($7,563M) + Short-term investments ($1,464M)

    fp_0 = 0.0               # Floor plan financing: None ($0.0) - Automotive line not applicable to Nike
    debt_0 = 7942.0          # Book Debt: Current portion ($2,000M) + Long-term debt ($5,942M) (Note 6, p. 70)
    revolver_0 = 0.0         # Drawn credit revolver: $0.0 (Note 6, p. 70)
    other_liab_0 = 15603.0   # Accounts payable, accrued liabilities, lease liabilities, etc.
    equity_0 = 14865.0       # Total Shareholders' Equity (10-K Balance Sheet, p. 57)

    # ---------------------------------------------------------
    # 2. Assumption Set (19 Labeled Assumptions)
    # ---------------------------------------------------------
    # Revenue growth: Currency-neutral recovery profile (judgment)
    growths = [0.030, 0.040, 0.050, 0.040, 0.030]
    
    # Gross margin: Recovery toward FY24 pre-discount levels (judgment)
    gross_margins = [0.4320, 0.4360, 0.4400, 0.4430, 0.4450]
    
    # SG&A as % of Gross Profit: Overhead restructuring under $2B cost program (judgment)
    sga_ratios = [0.8050, 0.7900, 0.7800, 0.7750, 0.7700]
    
    # Depreciation ratio: FY26 D&A ($747M) / FY25 ending PP&E ($4,828M) = 15.47% (history)
    depr_ratio = 747.0 / 4828.0
    
    # Non-cash impairment: Negligible for Nike (history)
    impairment = 0.0
    
    # Capital expenditures: ~1.5% of revenue (guidance / history: FY26 was $684M or 1.47%)
    capex_pct = 0.015
    
    # Effective tax rate: FY26 reported effective tax rate (history / guidance)
    tax_rate = 0.203
    
    # Inventory days: FY26 Inventories ($7,501M) / FY26 COGS ($26,487M) * 365 = 103.36 days (history)
    inv_days = 7501.0 / 26487.0 * 365.0
    
    # Floor plan financing ratio: Stated "none" ($0.0) (history / personalization)
    fp_ratio = 0.0
    fp_rate = 0.0
    
    # Other working capital: 1.0% of incremental revenue (judgment)
    owc_ratio = 0.010
    
    # Minimum operating cash floor: Global liquidity reserve (judgment)
    min_cash = 3000.0
    
    # Revolver limit: Committed credit facilities (guidance: Note 6, p. 70)
    revolver_limit = 3000.0
    
    # Revolver borrowing rate: SOFR + spread (judgment)
    revolver_rate = 0.055
    
    # Annual debt net repayment: Maturing debt repayment / refinancing (guidance / judgment)
    repayment = 500.0
    
    # Capital return (dividends + share repurchases): Disciplined capital return (judgment)
    capital_return = 2500.0
    
    # Book debt effective interest rate: FY26 interest / debt = 3.15% (history)
    debt_rate = 0.0315
    
    # Cost of equity: CAPM Rf=4.25%, Beta=0.95, ERP=5.0% = 9.0% (judgment)
    cost_of_equity = 0.090
    
    # Terminal value growth rate: Long-term mature economy GDP cap (judgment)
    terminal_growth = 0.025
    
    # Diluted weighted-average shares: FY26 Form 10-K Note 10, p. 77 (fact / history)
    shares = 1481.0

    years = [2027, 2028, 2029, 2030, 2031]

    # Containers for output records
    income_statement = []
    balance_sheet = []
    cash_flow = []
    checks = []

    # State variables tracking opening balances
    prev_rev = rev_0
    prev_inv = inv_0
    prev_ppe = ppe_0
    prev_other_assets = other_assets_0
    prev_cash = cash_0
    prev_fp = fp_0
    prev_debt = debt_0
    prev_revolver = revolver_0
    prev_other_liab = other_liab_0
    prev_equity = equity_0

    for idx, year in enumerate(years):
        # -----------------------------------------------------
        # Step A: Income Statement
        # -----------------------------------------------------
        g = growths[idx]
        gm = gross_margins[idx]
        sga_r = sga_ratios[idx]

        rev = prev_rev * (1.0 + g)
        gp = rev * gm
        sga = gp * sga_r
        depr = prev_ppe * depr_ratio
        ebit = gp - sga - depr - impairment
        interest = prev_debt * debt_rate + prev_revolver * revolver_rate + prev_fp * fp_rate
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
        fp = 0.0  # Floor plan is zero
        capex = rev * capex_pct
        ppe = prev_ppe + capex - depr
        delta_rev = rev - prev_rev
        other_assets = prev_other_assets + owc_ratio * delta_rev - impairment
        debt = prev_debt - repayment
        other_liab = prev_other_liab
        equity = prev_equity + ni - capital_return

        # -----------------------------------------------------
        # Step C: Free Cash Flow to Equity (FCFE)
        # -----------------------------------------------------
        delta_inv = inv - prev_inv
        delta_owc = owc_ratio * delta_rev
        delta_fp = 0.0

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
        # Cash is calculated LAST as the dynamic balance plug
        # -----------------------------------------------------
        prelim_cash = prev_cash + fcfe - capital_return
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

        # In swap-and-break test: break 2027 cash to opening cash ($9,027.0M)
        if break_test and year == 2027:
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
            "capital_return": capital_return,
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
        # Step E: Balance Checks
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
        prev_revolver = revolver
        prev_other_liab = other_liab
        prev_equity = equity

    # ---------------------------------------------------------
    # 3. Assert Balanced Check Function
    # ---------------------------------------------------------
    assert_balanced(checks)

    # ---------------------------------------------------------
    # 4. Valuation Engine (FCFE Discounting & Gordon Growth)
    # ---------------------------------------------------------
    pv_fcfe_list = [
        cf["fcfe"] / ((1.0 + cost_of_equity) ** (i + 1))
        for i, cf in enumerate(cash_flow)
    ]
    pv_explicit_fcfe = sum(pv_fcfe_list)

    # Terminal value at 2031: (2031 FCFE + 2031 debt repayment) * (1 + g) / (Ke - g)
    terminal_cash_flow = (cash_flow[-1]["fcfe"] + repayment) * (1.0 + terminal_growth)
    terminal_value_2031 = terminal_cash_flow / (cost_of_equity - terminal_growth)
    pv_terminal_value = terminal_value_2031 / ((1.0 + cost_of_equity) ** len(years))

    total_equity_value = pv_explicit_fcfe + pv_terminal_value
    share_of_value_after_2031 = pv_terminal_value / total_equity_value
    value_per_share = total_equity_value / shares

    valuation = {
        "pv_explicit_fcfe": pv_explicit_fcfe,
        "terminal_cash_flow_2032": terminal_cash_flow,
        "terminal_value_2031": terminal_value_2031,
        "pv_terminal_value": pv_terminal_value,
        "total_equity_value": total_equity_value,
        "share_of_value_after_2031": share_of_value_after_2031,
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
            raise ValueError(f"Liquidity check failed in FY{year}E: Cash ({c['cash']:.1f}) is below minimum floor")


def print_financial_statements(res: dict) -> None:
    years = [str(r["year"]) + "E" for r in res["income_statement"]]
    col_w = 12
    header_years = "".join(f"{y:>{col_w}}" for y in years)

    print("\n" + "=" * 95)
    print(f"{'INCOME STATEMENT (USD M)':<35}{header_years}")
    print("=" * 95)
    is_rows = [
        ("Revenue", [r["revenue"] for r in res["income_statement"]]),
        ("Gross Profit", [r["gross_profit"] for r in res["income_statement"]]),
        ("SG&A Expense", [r["sga"] for r in res["income_statement"]]),
        ("Depreciation", [r["depreciation"] for r in res["income_statement"]]),
        ("Operating Income (EBIT)", [r["ebit"] for r in res["income_statement"]]),
        ("Interest Expense", [r["interest"] for r in res["income_statement"]]),
        ("Pretax Income", [r["pretax"] for r in res["income_statement"]]),
        ("Income Tax", [r["tax"] for r in res["income_statement"]]),
        ("Net Income", [r["net_income"] for r in res["income_statement"]]),
    ]
    for name, vals in is_rows:
        val_str = "".join(f"{v:>{col_w}.1f}" for v in vals)
        print(f"{name:<35}{val_str}")

    print("\n" + "=" * 95)
    print(f"{'BALANCE SHEET (USD M)':<35}{header_years}")
    print("=" * 95)
    bs_rows = [
        ("Cash & Equivalents", [r["cash"] for r in res["balance_sheet"]]),
        ("Inventories", [r["inventory"] for r in res["balance_sheet"]]),
        ("PP&E (net)", [r["ppe"] for r in res["balance_sheet"]]),
        ("Other Assets", [r["other_assets"] for r in res["balance_sheet"]]),
        ("TOTAL ASSETS", [r["total_assets"] for r in res["balance_sheet"]]),
        ("Floor Plan Notes", [r["floor_plan"] for r in res["balance_sheet"]]),
        ("Term Debt", [r["debt"] for r in res["balance_sheet"]]),
        ("Credit Revolver", [r["revolver"] for r in res["balance_sheet"]]),
        ("Other Liabilities", [r["other_liab"] for r in res["balance_sheet"]]),
        ("TOTAL LIABILITIES", [r["total_liab"] for r in res["balance_sheet"]]),
        ("Shareholders' Equity", [r["equity"] for r in res["balance_sheet"]]),
        ("TOTAL LIABILITIES & EQUITY", [r["total_liab_equity"] for r in res["balance_sheet"]]),
    ]
    for name, vals in bs_rows:
        if name in ("TOTAL ASSETS", "TOTAL LIABILITIES & EQUITY"):
            print("-" * 95)
        val_str = "".join(f"{v:>{col_w}.1f}" for v in vals)
        print(f"{name:<35}{val_str}")

    print("\n" + "=" * 95)
    print(f"{'CASH FLOW & FCFE (USD M)':<35}{header_years}")
    print("=" * 95)
    cf_rows = [
        ("Net Income", [r["net_income"] for r in res["cash_flow"]]),
        ("(+) Depreciation", [r["depreciation"] for r in res["cash_flow"]]),
        ("(-) Capital Expenditures", [-r["capex"] for r in res["cash_flow"]]),
        ("(-) Change in Inventory", [-r["delta_inv"] for r in res["cash_flow"]]),
        ("(-) Change in Other Working Capital", [-r["delta_owc"] for r in res["cash_flow"]]),
        ("(-) Term Debt Repayment", [-r["debt_repayment"] for r in res["cash_flow"]]),
        ("Free Cash Flow to Equity (FCFE)", [r["fcfe"] for r in res["cash_flow"]]),
        ("(-) Capital Return (Div/Buybacks)", [-r["capital_return"] for r in res["cash_flow"]]),
        ("(+/-) Revolver Net Borrowing", [r["revolver_net"] for r in res["cash_flow"]]),
        ("Net Change in Cash", [r["net_change_cash"] for r in res["cash_flow"]]),
        ("Ending Cash", [r["cash"] for r in res["cash_flow"]]),
    ]
    for name, vals in cf_rows:
        if name in ("Free Cash Flow to Equity (FCFE)", "Ending Cash"):
            print("-" * 95)
        val_str = "".join(f"{v:>{col_w}.1f}" for v in vals)
        print(f"{name:<35}{val_str}")

    print("\n" + "=" * 95)
    print(f"{'CHECK BLOCK (REFUSAL CRITERIA)':<35}{header_years}")
    print("=" * 95)
    chk_gap = "".join(f"{r['assets_minus_liab_equity']:>{col_w}.1f}" for r in res["checks"])
    chk_cash = "".join(f"{r['cash']:>{col_w}.1f}" for r in res["checks"])
    print(f"{'Assets − Liabilities − Equity':<35}{chk_gap}")
    print(f"{'Cash Year-End':<35}{chk_cash}")

    v = res["valuation"]
    print("\n" + "=" * 55)
    print("VALUATION SUMMARY (NIKE, INC. BASE CASE)")
    print("=" * 55)
    print(f"PV of 5-Year Explicit FCFE      : $ {v['pv_explicit_fcfe']:>10.1f} M")
    print(f"Terminal Year Cash Flow (2032E) : $ {v['terminal_cash_flow_2032']:>10.1f} M")
    print(f"Terminal Value at 2031E         : $ {v['terminal_value_2031']:>10.1f} M")
    print(f"PV of Terminal Value            : $ {v['pv_terminal_value']:>10.1f} M")
    print(f"Total Equity Value              : $ {v['total_equity_value']:>10.1f} M")
    print(f"Diluted Shares Outstanding      :   {v['shares_outstanding']:>10.1f} M")
    print("-" * 55)
    print(f"Share of Value after 2031 (TV%) :   {v['share_of_value_after_2031'] * 100:>10.1f}%")
    print(f"Value per Diluted Share         : $ {v['value_per_share']:>10.2f}")
    print("=" * 55)


def demonstrate_refusal() -> None:
    print("\n=== Swap-and-Break Demonstration (Refusal Mechanism Check) ===")
    print("Deliberately forcing FY2027E cash to opening cash ($9,027.0M) instead of dynamic plug...")
    try:
        run_proforma_nke(break_test=True)
        print("[FAIL] Engine did not catch the deliberate balance sheet gap!")
    except ValueError as e:
        print(f"[PASS] Engine successfully refused to value:\n       --> {e}")


if __name__ == "__main__":
    print("Running Lab 10 Three-Statement Pro-Forma Engine (NIKE, Inc. Case)...")
    results = run_proforma_nke(break_test=False)
    print_financial_statements(results)
    demonstrate_refusal()
