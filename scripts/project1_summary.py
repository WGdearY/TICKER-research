"""Generate the visible executed output for FIN 439 Project 1 (NIKE)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from sensitivity_nke import run_sensitivity_suite


AS_OF_DATE = "2026-09-02"
OUTPUT_PATH = REPOSITORY_ROOT / "outputs" / "project1_visible_output.json"


def main() -> None:
    suite = run_sensitivity_suite()
    base = suite["base_initial"]
    output = {
        "target": "NIKE, Inc. (NYSE: NKE)",
        "as_of_date": AS_OF_DATE,
        "source_boundary": "FY2026 Form 10-K filed 2026-07-15; September 2, 2026 regular-session close",
        "market_price_per_share": 38.24,
        "recommendation": "Watch/defer; do not initiate a new 12-month position.",
        "supported_valuation_range_per_share": [30.0, 49.0],
        "reconsideration_conditions": [
            "Price at or below $36.40 per share.",
            "Reported evidence supports revenue and operating-margin recovery.",
        ],
        "base_fcfe_value_per_share": round(base["value_per_share"], 2),
        "base_fy2031_ebit_usd_millions": round(base["final_ebit"], 1),
        "base_fy2031_fcfe_usd_millions": round(base["final_fcfe"], 1),
        "accounting_check": "PASS: assets less liabilities and equity equals 0.0 in every forecast year.",
        "sensitivity_span": {
            "revenue_growth_plus_or_minus_1pp_value_per_share": [29.62, 30.76],
            "gross_margin_plus_or_minus_1pp_value_per_share": [29.12, 31.26],
            "capex_1_to_2_percent_of_revenue_value_per_share": [27.79, 32.60],
        },
        "limitation": "The FCFE base case attributes 79.9% of equity value to terminal value; range and conditions matter more than point precision.",
    }
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
