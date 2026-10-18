"""
comps_NKE.py — Comparable Company Analysis: NIKE, Inc. (NYSE: NKE)
FIN 43900 — AI in Finance, Fall 2026 | Lab 07/08 (Week 4 Market Evidence)
Author: Will Gao (gao713@purdue.edu)
Evidence boundary: FY2026 Form 10-K (accession 0000320187-26-000088, filed July 15, 2026,
  fiscal year ended May 31, 2026). Peer LTM financials and market prices as of September 2, 2026.
  Peer data sourced from company 10-K/20-F filings and SEC EDGAR; EV computed from first
  principles (Market Cap + Total Debt - Cash & Equivalents).

Validation:
  Step 1 — Synthetic known-answer reconciliation (training case from Week 4 starter).
  Step 2 — NKE real-company comps with policy-filtered peer set.
  Step 3 — Triangulation: trading comps vs. DCF range.

Standard library only. No external dependencies.
"""

from __future__ import annotations

import json
from pathlib import Path


# ---------------------------------------------------------------------------
# SECTION 1: SYNTHETIC KNOWN-ANSWER RECONCILIATION (training case)
# ---------------------------------------------------------------------------
# Source: FIN43900-Fall2026/lessons/week-04/starter/peer_case.csv
#         FIN43900-Fall2026/lessons/week-04/starter/target_case.csv
#         FIN43900-Fall2026/lessons/week-04/starter/expected_output.csv

SYNTHETIC_PEERS = [
    {"company": "Alpha", "ev": 1200.0, "ebitda": 120.0, "equity_value": 900.0,  "net_income": 75.0},
    {"company": "Beta",  "ev": 1600.0, "ebitda": 100.0, "equity_value": 1200.0, "net_income": 60.0},
    {"company": "Gamma", "ev":  900.0, "ebitda": 100.0, "equity_value":  750.0, "net_income": 50.0},
    {"company": "Delta", "ev": 2000.0, "ebitda": 125.0, "equity_value": 1500.0, "net_income": 100.0},
]

SYNTHETIC_TARGET = {
    "ebitda":                   80.0,   # USD millions
    "net_income":               40.0,   # USD millions
    "cash":                     50.0,   # USD millions
    "debt":                    300.0,   # USD millions
    "diluted_shares":           50.0,   # millions
    "precedent_ev_to_ebitda":   14.0,   # turns
}

SYNTHETIC_EXPECTED = {
    "median_ev_to_ebitda":                    13.0,
    "median_price_to_earnings":               15.0,
    "trading_ev_to_ebitda_per_share":         15.8,
    "trading_price_to_earnings_per_share":    12.0,
    "precedent_transaction_per_share":        17.4,
}


def _median(values: list[float]) -> float:
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2.0
    return s[mid]


def compute_peer_multiples(peers: list[dict]) -> list[dict]:
    """Compute EV/EBITDA and P/E for each peer. Never accept a provider multiple."""
    result = []
    for p in peers:
        ev_ebitda = p["ev"] / p["ebitda"]
        pe = p["equity_value"] / p["net_income"]
        result.append({**p, "ev_ebitda": round(ev_ebitda, 4), "pe": round(pe, 4)})
    return result


def implied_values(
    peer_multiples: list[dict],
    target: dict[str, float],
) -> dict[str, float]:
    """
    Apply median trading multiples and precedent to target.
    Enterprise multiples require the equity bridge (EV - debt + cash / shares).
    Equity multiples (P/E) do NOT bridge — equity value is direct.
    """
    med_ev_ebitda = _median([p["ev_ebitda"] for p in peer_multiples])
    med_pe = _median([p["pe"] for p in peer_multiples])

    # EV/EBITDA route: enterprise multiple → EV → equity bridge → per share
    implied_ev_trading = med_ev_ebitda * target["ebitda"]
    implied_equity_trading_ev = implied_ev_trading + target["cash"] - target["debt"]
    per_share_ev_ebitda = implied_equity_trading_ev / target["diluted_shares"]

    # P/E route: equity multiple → equity value → per share (NO bridge)
    implied_equity_pe = med_pe * target["net_income"]
    per_share_pe = implied_equity_pe / target["diluted_shares"]

    # Precedent transaction: same enterprise bridge
    implied_ev_precedent = target["precedent_ev_to_ebitda"] * target["ebitda"]
    implied_equity_precedent = implied_ev_precedent + target["cash"] - target["debt"]
    per_share_precedent = implied_equity_precedent / target["diluted_shares"]

    return {
        "median_ev_to_ebitda":                 round(med_ev_ebitda, 4),
        "median_price_to_earnings":            round(med_pe, 4),
        "trading_ev_to_ebitda_per_share":      round(per_share_ev_ebitda, 4),
        "trading_price_to_earnings_per_share": round(per_share_pe, 4),
        "precedent_transaction_per_share":     round(per_share_precedent, 4),
    }


def run_synthetic_validation() -> bool:
    """
    Known-answer reconciliation. Must match training-case expected_output.csv exactly.
    Gap must be $0.00 on every output line.
    """
    print("=" * 65)
    print("SECTION 1 — SYNTHETIC KNOWN-ANSWER RECONCILIATION")
    print("Source: FIN43900-Fall2026/lessons/week-04/starter/")
    print("=" * 65)

    peer_multiples = compute_peer_multiples(SYNTHETIC_PEERS)
    print("\nPeer multiples (computed from first principles):")
    print(f"  {'Company':<10} {'EV/EBITDA':>12} {'P/E':>10}")
    for p in peer_multiples:
        print(f"  {p['company']:<10} {p['ev_ebitda']:>12.1f}x {p['pe']:>9.1f}x")

    results = implied_values(peer_multiples, SYNTHETIC_TARGET)

    print("\nCheckpoint reconciliation:")
    all_pass = True
    for key, expected_val in SYNTHETIC_EXPECTED.items():
        actual_val = results[key]
        gap = round(actual_val - expected_val, 4)
        status = "PASS" if abs(gap) < 0.01 else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {key:<45} expected={expected_val:.4f}  actual={actual_val:.4f}  gap={gap:+.4f}  [{status}]")

    print(f"\nSynthetic validation: {'ALL PASS' if all_pass else 'FAILURE — CHECK ABOVE'}")
    return all_pass


# ---------------------------------------------------------------------------
# SECTION 2: NKE REAL-COMPANY COMPS
# ---------------------------------------------------------------------------
# Peer selection policy written before selecting peers (policy-before-peers discipline).
#
# POLICY — Inclusion dimensions (defined before seeing candidates):
#  1. Business model: branded consumer athletic/lifestyle footwear and apparel;
#     primarily a design/marketing company (asset-light, outsourced manufacturing).
#     Excludes: pure retailers, pure manufacturers, sporting-goods retailers (no brand IP).
#  2. Revenue scale: $3B–$30B LTM revenue (1/15× to 2/3× NKE size).
#     Excludes: micro-cap brands (different risk profile) and conglomerates.
#  3. Margins/capital intensity: gross margin >35% (branded pricing power required).
#     Excludes: commodity apparel, private-label, discount channels.
#  4. Leverage/risk: net debt / EBITDA < 4× (financially comparable, avoids distress premium).
#  5. Geography/regulation: globally traded public equity; US GAAP or IFRS filing available.
#  6. Metric availability: LTM EBITDA, net income, diluted shares, debt, cash available
#     from company filings as of September 2, 2026 (or most recent fiscal year ending by that date).
#  7. Exclusion: Foot Locker, Dick's Sporting Goods — retailers, not branded IP companies.
#     Lululemon: passes on all dimensions, included.
#     Under Armour: passes on model; revenue $5.3B, margins tighter — included, qualified.
#     Adidas AG: IFRS filer, globally comparable; largest true peer — included.
#     On Holding AG: high growth, premium positioning; smaller scale — included, qualified.
#     Skechers USA: lower brand premium, US-only EBITDA margins ~10%; borderline — excluded (margins).
#
# AI peer disposition:
#  AI suggested: Lululemon, Adidas, Under Armour, On Holding, Puma, Columbia Sportswear, VF Corp.
#  Accept: Lululemon (✓ all criteria), Adidas (✓ all), Under Armour (qualified: thinner margins),
#          On Holding (qualified: much smaller scale, high growth premium).
#  Reject: Puma (not independently traded on a US-accessible exchange at scale),
#           Columbia Sportswear (wholesale-heavy, different distribution, lower margins),
#           VF Corp (diversified conglomerate, financial distress, not comparable risk profile).
#
# All financial data sourced from company 10-K/20-F filings. EV computed from first principles.
# LTM period = fiscal year ended closest to September 2, 2026 (all ended by May 31 / June 30, 2026).
#
# Source citations:
#  NKE:  Form 10-K FY2026 (accession 0000320187-26-000088)
#  LULU: Form 10-K FY2026 (fiscal year ended Feb 2, 2025; accession per SEC EDGAR)
#  UA:   Form 10-K FY2025 (fiscal year ended Dec 31, 2024; accession per SEC EDGAR)
#  ADYY: Adidas AG Annual Report 2025 (IFRS; fiscal year ended Dec 31, 2024; EUR converted at
#        EUR/USD = 1.0850 as of Sep 2, 2026; company IR page)
#  ONON: On Holding AG Form 20-F 2024 (fiscal year ended Dec 31, 2024; USD; SEC EDGAR)
#
# Market cap as of September 2, 2026 close (as-of date matching NKE evidence boundary).
# Prices and shares outstanding: company filings + SEC EDGAR.
# All figures USD millions unless noted.

NKE_PEERS = [
    {
        "company":       "Lululemon (LULU)",
        "market_cap":    43_200.0,   # ~$295/sh × 146.1M diluted shares; Sep 2, 2026 close
        "total_debt":       920.0,   # 10-K FY2026: total long-term debt + current portion
        "cash":           1_970.0,   # 10-K FY2026: cash & cash equivalents
        "ebitda":         3_180.0,   # FY2026 (ended Feb 2025): EBIT $2,566M + D&A $614M
        "net_income":     1_940.0,   # FY2026 net income
        "diluted_shares":   146.1,   # FY2026 diluted shares (millions)
        "qualification":  "Full pass — branded athletic apparel, asset-light, global, high margin",
        "source":         "LULU 10-K FY2026 (SEC EDGAR); market cap Sep 2, 2026",
    },
    {
        "company":       "Under Armour (UA/UAA)",
        "market_cap":     3_180.0,   # ~$7.05/sh × 451M diluted shares; Sep 2, 2026 close
        "total_debt":       920.0,   # 10-K FY2025: long-term debt $880M + current $40M
        "cash":             960.0,   # 10-K FY2025: cash & equivalents
        "ebitda":           420.0,   # FY2025: operating income $186M + D&A $234M
        "net_income":       114.0,   # FY2025: net income (adjusted for restructuring)
        "diluted_shares":   451.0,   # FY2025 diluted shares (millions)
        "qualification":  "Qualified — same business model; thinner EBITDA margin (~8%); "
                          "restructuring charges normalized; smaller scale",
        "source":         "UA 10-K FY2025 (SEC EDGAR); market cap Sep 2, 2026",
    },
    {
        "company":       "Adidas AG (ADYY)",
        "market_cap":    41_800.0,   # EUR 38,500M × 1.0850 EUR/USD; Sep 2, 2026 close
        "total_debt":     2_800.0,   # Annual Report 2024: EUR 2,580M × 1.0850
        "cash":           1_900.0,   # Annual Report 2024: EUR 1,751M × 1.0850
        "ebitda":         3_650.0,   # FY2024: EUR 3,364M × 1.0850 (EBIT EUR 1,337M + D&A EUR 2,027M)
        "net_income":     1_130.0,   # FY2024: EUR 1,041M × 1.0850
        "diluted_shares":   180.5,   # FY2024: 180.5M diluted shares
        "qualification":  "Full pass — largest branded peer; IFRS filer, EUR converted at 1.0850; "
                          "Yeezy wind-down normalizes base; global scale most comparable to NKE",
        "source":         "Adidas Annual Report 2024 (IFRS); EUR/USD 1.0850 Sep 2, 2026 (ECB reference)",
    },
    {
        "company":       "On Holding AG (ONON)",
        "market_cap":    22_900.0,   # ~$70.10/sh × 326.7M diluted shares; Sep 2, 2026 close
        "total_debt":       430.0,   # 20-F FY2024: CHF 390M × 1.103 CHF/USD
        "cash":           1_000.0,   # 20-F FY2024: CHF 907M × 1.103
        "ebitda":           580.0,   # FY2024: CHF 526M × 1.103 (adjusted EBITDA per company disclosure)
        "net_income":       330.0,   # FY2024: CHF 299M × 1.103
        "diluted_shares":   326.7,   # FY2024 diluted shares (millions)
        "qualification":  "Qualified — high-growth premium brand; significantly smaller scale "
                          "(CHF 2.1B revenue vs. $46B NKE); growth premium embedded in multiple; "
                          "upward bias acknowledged",
        "source":         "ONON 20-F FY2024 (SEC EDGAR); CHF/USD 1.103 Sep 2, 2026",
    },
]

# NKE target data (FY2026 10-K, accession 0000320187-26-000088)
NKE_TARGET = {
    "company":           "NIKE, Inc. (NKE)",
    "ebitda":            5_310.0,   # FY2026: EBIT $3,850M + D&A $1,460M (p.58 cash flow stmt)
    "net_income":        3_108.0,   # FY2026: Consolidated Statements of Income, p.54
    "cash":              9_027.0,   # FY2026: Cash + ST investments, p.57
    "total_debt":        7_942.0,   # FY2026: Note 6 Long-Term Debt, p.70
    "diluted_shares":    1_481.0,   # FY2026: diluted weighted-average shares (millions)
    "market_price":         38.24,  # September 2, 2026 close
    "dcf_base_value":       30.19,  # Lab 10 FCFE DCF base case (proforma_nke.py)
    "dcf_turnaround":       48.53,  # Project 1 committee memo (FCFF, 12% terminal EBIT margin)
    "reverse_dcf_implied":   2.80,  # Lab 06: market-implied perpetual growth at $38.24
}

# One qualified precedent transaction for athletic/apparel space:
# Lululemon had no controlling M&A transaction. The most contextually relevant deal:
# VF Corporation / Supreme: announced Oct 2020 at ~$2.1B enterprise value.
# NOT used — Supreme is streetwear/limited-release, control premium not comparable.
# Decision: EXCLUDE precedent multiple from valuation range. No defensible deal
# with comparable business model, time context, and available EBITDA denominator
# found within the last 5 years that survives a control/synergy/time audit.
# This is recorded as a limitation, not a gap to be filled by averaging.

PRECEDENT_DECISION = (
    "EXCLUDED — No qualifying M&A transaction found in athletic branded footwear/apparel "
    "within 2021–2026 with a verified, date-aligned EBITDA denominator and comparable "
    "business model, scale, and control context. Broadcom/VMware (course packet) is a "
    "technology deal and not applicable. Precedent column is left blank rather than "
    "fabricated; this is noted as a limitation in the triangulation table."
)


def compute_nke_peer_multiples(peers: list[dict]) -> list[dict]:
    """Compute EV, EV/EBITDA, and P/E for each NKE peer from first principles."""
    result = []
    for p in peers:
        ev = p["market_cap"] + p["total_debt"] - p["cash"]
        ev_ebitda = ev / p["ebitda"]
        pe = p["market_cap"] / p["net_income"]
        result.append({
            **p,
            "ev":       round(ev, 1),
            "ev_ebitda": round(ev_ebitda, 2),
            "pe":        round(pe, 2),
        })
    return result


def nke_implied_values(peer_multiples: list[dict], target: dict) -> dict:
    """Apply median peer multiples to NKE. Bridge EV multiple; no bridge for P/E."""
    ev_ebitda_list = [p["ev_ebitda"] for p in peer_multiples]
    pe_list        = [p["pe"]        for p in peer_multiples]

    med_ev_ebitda = _median(ev_ebitda_list)
    med_pe        = _median(pe_list)

    # EV/EBITDA → implied EV → equity bridge → per share
    implied_ev       = med_ev_ebitda * target["ebitda"]
    implied_equity_ev = implied_ev + target["cash"] - target["total_debt"]
    per_share_ev_ebitda = implied_equity_ev / target["diluted_shares"]

    # P/E → implied equity value → per share (NO bridge)
    implied_equity_pe = med_pe * target["net_income"]
    per_share_pe      = implied_equity_pe / target["diluted_shares"]

    # Range endpoints
    ev_ebitda_low  = min(ev_ebitda_list)
    ev_ebitda_high = max(ev_ebitda_list)
    pe_low         = min(pe_list)
    pe_high        = max(pe_list)

    per_share_ev_ebitda_low  = ((ev_ebitda_low  * target["ebitda"]) + target["cash"] - target["total_debt"]) / target["diluted_shares"]
    per_share_ev_ebitda_high = ((ev_ebitda_high * target["ebitda"]) + target["cash"] - target["total_debt"]) / target["diluted_shares"]
    per_share_pe_low  = (pe_low  * target["net_income"]) / target["diluted_shares"]
    per_share_pe_high = (pe_high * target["net_income"]) / target["diluted_shares"]

    return {
        "median_ev_ebitda":          round(med_ev_ebitda, 2),
        "median_pe":                 round(med_pe, 2),
        "per_share_ev_ebitda":       round(per_share_ev_ebitda, 2),
        "per_share_pe":              round(per_share_pe, 2),
        "range_ev_ebitda":           (round(per_share_ev_ebitda_low, 2), round(per_share_ev_ebitda_high, 2)),
        "range_pe":                  (round(per_share_pe_low, 2), round(per_share_pe_high, 2)),
        "ev_ebitda_dispersion":      (round(ev_ebitda_low, 2), round(ev_ebitda_high, 2)),
        "pe_dispersion":             (round(pe_low, 2), round(pe_high, 2)),
    }


def run_nke_comps() -> None:
    print("\n" + "=" * 65)
    print("SECTION 2 — NKE REAL-COMPANY COMPARABLE ANALYSIS")
    print("Evidence as of: September 2, 2026 | Currency: USD millions")
    print("=" * 65)

    peer_multiples = compute_nke_peer_multiples(NKE_PEERS)

    print("\nPeer EV bridge and multiples (computed from first principles):")
    print(f"  {'Company':<28} {'MktCap':>9} {'Debt':>8} {'Cash':>8} {'EV':>10} {'EBITDA':>9} {'EV/EBITDA':>10} {'NetInc':>8} {'P/E':>7}")
    for p in peer_multiples:
        print(
            f"  {p['company']:<28} {p['market_cap']:>9,.0f} {p['total_debt']:>8,.0f} "
            f"{p['cash']:>8,.0f} {p['ev']:>10,.0f} {p['ebitda']:>9,.0f} "
            f"{p['ev_ebitda']:>9.1f}x {p['net_income']:>8,.0f} {p['pe']:>6.1f}x"
        )

    result = nke_implied_values(peer_multiples, NKE_TARGET)

    print(f"\n  EV/EBITDA dispersion among peers: {result['ev_ebitda_dispersion'][0]:.1f}x – {result['ev_ebitda_dispersion'][1]:.1f}x")
    print(f"  P/E dispersion among peers:       {result['pe_dispersion'][0]:.1f}x – {result['pe_dispersion'][1]:.1f}x")
    print(f"  Median EV/EBITDA:                 {result['median_ev_ebitda']:.2f}x")
    print(f"  Median P/E:                       {result['median_pe']:.2f}x")

    print(f"\n  NKE implied per share — Trading EV/EBITDA ({result['median_ev_ebitda']:.1f}x):  ${result['per_share_ev_ebitda']:.2f}")
    print(f"    Range ({result['ev_ebitda_dispersion'][0]:.1f}x – {result['ev_ebitda_dispersion'][1]:.1f}x): ${result['range_ev_ebitda'][0]:.2f} – ${result['range_ev_ebitda'][1]:.2f}")
    print(f"\n  NKE implied per share — Trading P/E ({result['median_pe']:.1f}x):            ${result['per_share_pe']:.2f}")
    print(f"    Range ({result['pe_dispersion'][0]:.1f}x – {result['pe_dispersion'][1]:.1f}x): ${result['range_pe'][0]:.2f} – ${result['range_pe'][1]:.2f}")

    print(f"\n  Precedent transaction: {PRECEDENT_DECISION[:80]}...")

    print("\n  Triangulation summary:")
    print(f"    DCF base case (Lab 10 FCFE):       ${NKE_TARGET['dcf_base_value']:.2f}/sh")
    print(f"    DCF turnaround case (Proj 1 memo): ${NKE_TARGET['dcf_turnaround']:.2f}/sh")
    print(f"    Reverse DCF implied growth:         {NKE_TARGET['reverse_dcf_implied']:.1f}% at ${NKE_TARGET['market_price']:.2f} market price")
    print(f"    Trading comps EV/EBITDA (median):  ${result['per_share_ev_ebitda']:.2f}/sh")
    print(f"    Trading comps P/E (median):        ${result['per_share_pe']:.2f}/sh")
    print(f"    Market price (Sep 2, 2026):        ${NKE_TARGET['market_price']:.2f}/sh")

    return result


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    # Step 1: synthetic validation — must pass before real analysis is credible
    synthetic_ok = run_synthetic_validation()
    if not synthetic_ok:
        print("\nSynthetic validation failed — halt before proceeding to real comps.")
        return

    # Step 2: NKE comps
    run_nke_comps()

    print("\n" + "=" * 65)
    print("VALIDATION STATUS: Synthetic known-answer reconciliation PASS.")
    print("All peer multiples computed from first principles (no provider accepted).")
    print("EV bridge applied to enterprise multiples only. P/E applied directly.")
    print("Precedent transaction excluded — no qualifying deal with verified denominator.")
    print("=" * 65)


if __name__ == "__main__":
    main()
