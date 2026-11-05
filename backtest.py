"""
backtest.py — Lab 18/19: Holdout Test + Signal Decision
FIN 43900 — AI in Finance, Fall 2026 | Week 11
Author: Will Gao (gao713@purdue.edu)

Standard library only. No external dependencies.

Rule card (committed before build):
  Signal: month-end card-spend change, published by month-end.
  Rule:   signal > 0 → hold the equity fund next month; otherwise Treasury bills.
  Lag:    1 month (this month's signal decides next month's position).
  Cost:   0.10% per switch month; start in bills.
  Bills:  0.30% per month.
  Dev:    2025-01 to 2025-12.
  Holdout: 2026-01 to 2026-06, run once, never tuned.
  Benchmark: buy-and-hold equity fund.
  Failure rule: stop if holdout net return trails buy-and-hold.

Run:
  python3 backtest.py                         # training panel (Lab 18)
  python3 backtest.py my_signal.csv 12        # own CSV, last 12 months = holdout
"""

from __future__ import annotations
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# EDITABLE INPUTS — TRAINING PANEL
# ---------------------------------------------------------------------------

TRAINING_DATA = [
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

LAG_MONTHS = 1
COST_PER_SWITCH = 0.10  # percent
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
    flip_signal: bool = False,
) -> dict:
    """
    Apply the rule over a contiguous range of months.
    If flip_signal is True, the sign of the signal is reversed (placebo).
    Returns dict with gross/net compounded return (%), buy-and-hold return (%),
    number of switches, final position, and month-by-month detail.
    """
    month_idx = {row[0]: i for i, row in enumerate(data)}
    months = [row[0] for row in data if row[2] is not None]
    months = [m for m in months if start_month <= m <= end_month]

    position = initial_position
    gross_cum = 1.0
    net_cum   = 1.0
    bh_cum    = 1.0
    switches  = 0
    detail    = []

    for m in months:
        idx = month_idx[m]
        equity_ret = data[idx][2]

        signal_idx = idx - lag
        if signal_idx < 0:
            signal_val = None
            new_position = position
        else:
            signal_val = data[signal_idx][1]
            if flip_signal:
                signal_val_decision = -signal_val
            else:
                signal_val_decision = signal_val
            new_position = "equity" if signal_val_decision > 0 else "bills"

        switched = (new_position != position)
        if switched:
            switches += 1
        position = new_position

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
            "signal": data[signal_idx][1] if signal_idx >= 0 else None,
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
# CSV LOADER
# ---------------------------------------------------------------------------

def load_csv(path: str) -> list[tuple]:
    """
    Load a CSV with columns: month, signal, asset_return_pct.
    The first row may have a None asset return (seed signal for lag).
    """
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            month = r["month"].strip()
            signal = float(r["signal"].strip())
            ret_str = r["asset_return_pct"].strip()
            ret = None if ret_str in ("", "None", "NA") else float(ret_str)
            rows.append((month, signal, ret))
    return rows


# ---------------------------------------------------------------------------
# PRINT HELPERS
# ---------------------------------------------------------------------------

def print_period(label: str, rule: dict, placebo: dict) -> None:
    """Print rule, placebo, and buy-and-hold for one period."""
    print(f"\n{label}")
    print(f"  {'':20s} {'Rule':>10s} {'Placebo':>10s} {'Buy&Hold':>10s}")
    print(f"  {'Gross':20s} {rule['gross_pct']:>9.2f}% {placebo['gross_pct']:>9.2f}% {rule['bh_pct']:>9.2f}%")
    print(f"  {'Net':20s} {rule['net_pct']:>9.2f}% {placebo['net_pct']:>9.2f}% {rule['bh_pct']:>9.2f}%")
    print(f"  {'Switches':20s} {rule['switches']:>10d} {placebo['switches']:>10d}")


def print_detail(label: str, detail: list[dict]) -> None:
    """Print month-by-month detail."""
    print(f"\n  {label} detail:")
    print(f"  {'Month':<9} {'Sig mo':<9} {'Signal':>7} {'Pos':<7} "
          f"{'EqRet%':>7} {'Gross%':>7} {'Cost%':>6} {'Net%':>7}")
    print("  " + "-" * 66)
    for d in detail:
        sig_str = f"{d['signal']:>7.1f}" if d['signal'] is not None else "      —"
        print(f"  {d['month']:<9} {d['signal_month']:<9} {sig_str} {d['position']:<7} "
              f"{d['equity_ret']:>7.1f} {d['gross_ret']:>7.1f} {d['cost']:>6.2f} {d['net_ret']:>7.2f}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 68

    # Determine mode: training panel or CSV
    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]
        holdout_months = int(sys.argv[2]) if len(sys.argv) >= 3 else 12
        data = load_csv(csv_path)
        tradeable = [r for r in data if r[2] is not None]
        dev_start = tradeable[0][0]
        dev_end   = tradeable[-(holdout_months + 1)][0]
        hold_start = tradeable[-holdout_months][0]
        hold_end  = tradeable[-1][0]
        source_label = f"CSV: {csv_path}"
    else:
        data = TRAINING_DATA
        dev_start = DEV_START
        dev_end   = DEV_END
        hold_start = HOLD_START
        hold_end  = HOLD_END
        source_label = "Training panel (Lab 18)"

    print(sep)
    print("LAB 18/19 — HOLDOUT TEST + SIGNAL DECISION")
    print("Author: Will Gao | gao713@purdue.edu")
    print(f"Source: {source_label}")
    print(f"Lag: {LAG_MONTHS} month(s) | Cost per switch: {COST_PER_SWITCH}%")
    print(f"Bills return: {BILLS_RETURN}% / month | Start position: bills")
    print(f"Development: {dev_start} to {dev_end}")
    print(f"Holdout:     {hold_start} to {hold_end}")
    print(sep)

    # ---- Development ----
    dev_rule = run_backtest(data, dev_start, dev_end, LAG_MONTHS,
                            COST_PER_SWITCH, BILLS_RETURN, "bills", flip_signal=False)
    dev_plac = run_backtest(data, dev_start, dev_end, LAG_MONTHS,
                            COST_PER_SWITCH, BILLS_RETURN, "bills", flip_signal=True)

    print_period(f"DEVELOPMENT ({dev_start} to {dev_end})", dev_rule, dev_plac)
    print_detail("Rule", dev_rule["detail"])

    # ---- Holdout ----
    hold_rule = run_backtest(data, hold_start, hold_end, LAG_MONTHS,
                             COST_PER_SWITCH, BILLS_RETURN,
                             dev_rule["final_position"], flip_signal=False)
    hold_plac = run_backtest(data, hold_start, hold_end, LAG_MONTHS,
                             COST_PER_SWITCH, BILLS_RETURN,
                             dev_plac["final_position"], flip_signal=True)

    print_period(f"HOLDOUT ({hold_start} to {hold_end})", hold_rule, hold_plac)
    print_detail("Rule", hold_rule["detail"])

    # ---- Failure rule ----
    triggered = hold_rule["net_pct"] < hold_rule["bh_pct"]
    print(f"\n{sep}")
    print(f"FAILURE RULE: holdout net ({hold_rule['net_pct']:.2f}%) "
          f"{'<' if triggered else '>='} buy-and-hold ({hold_rule['bh_pct']:.2f}%)")
    print(f"  → {'TRIGGERED — stop.' if triggered else 'NOT triggered — may continue.'}")

    # ---- Placebo comparison ----
    plac_beats = hold_plac["net_pct"] > hold_rule["net_pct"]
    print(f"\nPLACEBO CHECK: placebo holdout net ({hold_plac['net_pct']:.2f}%) "
          f"{'>' if plac_beats else '<='} rule holdout net ({hold_rule['net_pct']:.2f}%)")
    print(f"  → {'Placebo BEATS the rule — signal may be noise.' if plac_beats else 'Rule beats the placebo.'}")
    print(sep)


if __name__ == "__main__":
    main()
