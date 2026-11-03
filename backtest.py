"""
backtest.py — Lab 18: Holdout Test
FIN 43900 — AI in Finance, Fall 2026 | Week 11 (Tuesday)
Author: Will Gao (gao713@purdue.edu)

Standard library only. No external dependencies.

Rule card (committed before build):
  Signal: month-end card-spend change, published by month-end.
  Rule:   signal > 0 → hold equity fund next month; otherwise Treasury bills.
  Lag:    1 month (this month's signal decides next month's position).
  Cost:   0.10% per switch month; start in bills.
  Bills:  0.30% per month.
  Dev:    2025-01 to 2025-12.
  Holdout: 2026-01 to 2026-06, run once, never tuned.
  Benchmark: buy-and-hold equity fund.
  Failure rule: stop if holdout net return trails buy-and-hold.

Run:  python3 backtest.py
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# EDITABLE INPUTS
# ---------------------------------------------------------------------------

# Monthly data: (month, signal_pct, equity_fund_pct)
# Signal for 2024-12 is the seed for the first lag decision; no equity return.
DATA = [
    ("2024-12",  0.8, None),
    ("2025-01",  1.2,  2.0),
    ("2025-02",  0.9,  1.5),
    ("2025-03",  1.5,  3.0),
    ("2025-04", -1.0, -2.5),
    ("2025-05", -0.7, -1.5),
    ("2025-06", -1.4, -3.0),
    ("2025-07",  1.1,  2.5),
    ("2025-08",  0.6,  1.0),
    ("2025-09",  0.9,  2.0),
    ("2025-10", -0.9, -2.0),
    ("2025-11", -0.5, -1.0),
    ("2025-12",  1.6,  3.5),
    ("2026-01", -1.1, -2.0),
    ("2026-02",  0.7,  1.5),
    ("2026-03", -1.3, -3.0),
    ("2026-04",  0.8,  2.0),
    ("2026-05", -0.6, -1.5),
    ("2026-06",  0.5,  1.0),
]

LAG_MONTHS = 1          # how many months back the signal is read
COST_PER_SWITCH = 0.10  # percent; charged in the month of a switch
BILLS_RETURN = 0.30     # percent per month
DEV_START  = "2025-01"
DEV_END    = "2025-12"
HOLD_START = "2026-01"
HOLD_END   = "2026-06"


# ---------------------------------------------------------------------------
# BACKTEST ENGINE
# ---------------------------------------------------------------------------

def run_backtest(
    data: list[tuple],
    start_month: str,
    end_month: str,
    lag: int,
    cost_pct: float,
    bills_pct: float,
    initial_position: str,
) -> dict:
    """
    Apply the rule over a contiguous range of months.
    Returns dict with gross/net compounded return (%), buy-and-hold return (%),
    number of switches, final position, and month-by-month detail.
    """
    # Build lookup: month -> index in DATA
    month_idx = {row[0]: i for i, row in enumerate(data)}

    # Identify the months to iterate
    months = [row[0] for row in data if row[2] is not None]
    months = [m for m in months if start_month <= m <= end_month]

    position = initial_position   # "bills" or "equity"
    gross_cum = 1.0
    net_cum   = 1.0
    bh_cum    = 1.0
    switches  = 0
    detail    = []

    for m in months:
        idx = month_idx[m]
        equity_ret = data[idx][2]  # percent

        # Determine position from lagged signal
        signal_idx = idx - lag
        if signal_idx < 0:
            signal_val = None
            new_position = position  # no signal yet, stay put
        else:
            signal_val = data[signal_idx][1]
            new_position = "equity" if signal_val > 0 else "bills"

        # Detect switch
        switched = (new_position != position)
        if switched:
            switches += 1
        position = new_position

        # Returns this month
        if position == "equity":
            gross_ret = equity_ret
        else:
            gross_ret = bills_pct

        cost = cost_pct if switched else 0.0
        net_ret = gross_ret - cost

        gross_cum *= (1 + gross_ret / 100)
        net_cum   *= (1 + net_ret / 100)
        bh_cum    *= (1 + equity_ret / 100)

        detail.append({
            "month": m,
            "signal_month": data[signal_idx][0] if signal_idx >= 0 else "—",
            "signal": signal_val,
            "position": position,
            "equity_ret": equity_ret,
            "gross_ret": gross_ret,
            "cost": cost,
            "net_ret": net_ret,
        })

    return {
        "gross_pct": (gross_cum - 1) * 100,
        "net_pct":   (net_cum - 1) * 100,
        "bh_pct":    (bh_cum - 1) * 100,
        "switches":  switches,
        "final_position": position,
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 68

    print(sep)
    print("LAB 18 — HOLDOUT TEST")
    print("Author: Will Gao | gao713@purdue.edu")
    print(f"Lag: {LAG_MONTHS} month(s) | Cost per switch: {COST_PER_SWITCH}%")
    print(f"Bills return: {BILLS_RETURN}% / month | Start position: bills")
    print(sep)

    # ---- Development ----
    dev = run_backtest(DATA, DEV_START, DEV_END, LAG_MONTHS,
                       COST_PER_SWITCH, BILLS_RETURN, "bills")

    print(f"\nDEVELOPMENT ({DEV_START} to {DEV_END})")
    print(f"  Rule gross:    {dev['gross_pct']:>7.2f}%")
    print(f"  Rule net:      {dev['net_pct']:>7.2f}%")
    print(f"  Buy-and-hold:  {dev['bh_pct']:>7.2f}%")
    print(f"  Switches:      {dev['switches']}")

    # ---- Month-by-month development detail ----
    print(f"\n  {'Month':<9} {'Sig mo':<9} {'Signal':>7} {'Pos':<7} "
          f"{'EqRet%':>7} {'Gross%':>7} {'Cost%':>6} {'Net%':>7}")
    print("  " + "-" * 66)
    for d in dev["detail"]:
        sig_str = f"{d['signal']:>7.1f}" if d['signal'] is not None else "      —"
        print(f"  {d['month']:<9} {d['signal_month']:<9} {sig_str} {d['position']:<7} "
              f"{d['equity_ret']:>7.1f} {d['gross_ret']:>7.1f} {d['cost']:>6.2f} {d['net_ret']:>7.2f}")

    # ---- Holdout ----
    hold = run_backtest(DATA, HOLD_START, HOLD_END, LAG_MONTHS,
                        COST_PER_SWITCH, BILLS_RETURN, dev["final_position"])

    print(f"\nHOLDOUT ({HOLD_START} to {HOLD_END})")
    print(f"  Rule gross:    {hold['gross_pct']:>7.2f}%")
    print(f"  Rule net:      {hold['net_pct']:>7.2f}%")
    print(f"  Buy-and-hold:  {hold['bh_pct']:>7.2f}%")
    print(f"  Switches:      {hold['switches']}")

    # ---- Month-by-month holdout detail ----
    print(f"\n  {'Month':<9} {'Sig mo':<9} {'Signal':>7} {'Pos':<7} "
          f"{'EqRet%':>7} {'Gross%':>7} {'Cost%':>6} {'Net%':>7}")
    print("  " + "-" * 66)
    for d in hold["detail"]:
        sig_str = f"{d['signal']:>7.1f}" if d['signal'] is not None else "      —"
        print(f"  {d['month']:<9} {d['signal_month']:<9} {sig_str} {d['position']:<7} "
              f"{d['equity_ret']:>7.1f} {d['gross_ret']:>7.1f} {d['cost']:>6.2f} {d['net_ret']:>7.2f}")

    # ---- Failure rule ----
    triggered = hold["net_pct"] < hold["bh_pct"]
    print(f"\n{sep}")
    print(f"FAILURE RULE: holdout net ({hold['net_pct']:.2f}%) "
          f"{'<' if triggered else '>='} buy-and-hold ({hold['bh_pct']:.2f}%)")
    print(f"  → {'TRIGGERED — stop.' if triggered else 'NOT triggered — may continue.'}")
    print(sep)


if __name__ == "__main__":
    main()
