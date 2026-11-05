# Lab 19 — Signal Decision

**Author:** Will Gao | gao713@purdue.edu
**Date:** November 5, 2026
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 19 / Week 11 (Thursday)
**Script:** [backtest.py](https://github.com/WGdearY/TICKER-research/blob/main/backtest.py)
**Data:** [my_signal.csv](https://github.com/WGdearY/TICKER-research/blob/main/my_signal.csv)

**Run commands:**
```
python3 backtest.py                    # training panel (Lab 18 known answer + placebo)
python3 backtest.py my_signal.csv 12   # own signal, last 12 months = holdout
```

---

## D — The Question

> **Does my signal beat a placebo on months it has never seen, after costs — and what will I do about it?**

### Economic Reason (Explained to Partner)

My signal is the month-over-month change in the ICE BofA US High Yield Option-Adjusted Spread (BAMLH0A0HYM2). When the spread narrows (negative change), credit conditions are easing and risk appetite is rising — equity should do well. When the spread widens (positive change), investors are fleeing risk — equity should underperform. This credit-sentiment channel is the hypothesized link between the signal and the equity fund's returns: a negative signal change → hold equity; positive → hold bills. Since the rule card says "signal > 0 → equity," I invert the spread change so that a tightening (favorable) environment maps to a positive signal.

---

## R — Rule Card (Frozen and Committed Before Running)

| Rule card | My value |
|---|---|
| Signal | Month-end change in high-yield OAS (BAMLH0A0HYM2), inverted so that spread tightening = positive signal; as-of filtered per Lab 17 admission (ADMIT — daily, no revisions, ≤ 1 day lag) |
| Rule | Signal > 0 → hold equity fund next month; otherwise Treasury bills |
| Lag | 1 month: this month-end's signal decides next month's position |
| Fund | Broad US equity fund (monthly returns from Lab 15 universe) |
| Cost | 0.10% in any month the position switches; start in bills |
| Bills return | 0.30% per month (assumption — no bill fund in panel) |
| Development | 2024-10 to 2025-09 (all months except last 12) |
| Holdout | 2025-10 to 2026-09 (last 12 months), run once, never tuned |
| Benchmark | Buy-and-hold equity fund |
| Failure rule | Stop if the holdout net return trails buy-and-hold |

**Series admission status:** ADMIT (Lab 17). Daily frequency, essentially no publication lag (≤ 1 business day), no revisions (revised count = 0). As-of filter is trivially satisfied: month-end values are available by the next business day.

---

## E — Training Panel: Placebo Verification

Running `python3 backtest.py` (no arguments) on the Lab 18 training panel:

| Period | Rule net | Placebo net | Buy-and-hold | Match? |
|---|---:|---:|---:|---|
| Development | 6.13% | 2.16% | 5.33% | ✅ |
| Holdout | −6.09% | 4.88% | −2.09% | ✅ |

The placebo beats the rule on the holdout. The flipped signal — betting the opposite way — outperforms, confirming that the training signal's apparent edge reversed out of sample. ✅

---

## E — Own Data: Rule, Placebo, and Holdout

Running `python3 backtest.py my_signal.csv 12`:

### Development (2024-10 to 2025-09)

| Metric | Rule | Placebo | Buy-and-hold |
|---|---:|---:|---:|
| Gross | 3.44% | 10.60% | 10.36% |
| Net | 2.31% | 9.29% | 10.36% |
| Switches | 11 | 12 | — |

### Holdout (2025-10 to 2026-09)

| Metric | Rule | Placebo | Buy-and-hold |
|---|---:|---:|---:|
| Gross | −0.67% | 12.93% | 8.21% |
| Net | −1.86% | 11.59% | 8.21% |
| Switches | 12 | 12 | — |

### Failure Rule

Holdout net (−1.86%) < buy-and-hold (8.21%) → **TRIGGERED — stop.**

### Placebo Check

Placebo holdout net (11.59%) > rule holdout net (−1.86%) → **Placebo BEATS the rule.**

The placebo (flipped signal) massively outperforms the rule in both development and holdout. The rule's signal — positive OAS change tightening → hold equity — actually works in the *opposite* direction: when the spread widens, equity does better in this sample. The rule as written destroys value.

---

## V — Bull, Bear, and the Ledger

### Partner Attack: Bear Case

The numbers are devastating. The rule underperforms buy-and-hold in *both* development (+2.31% vs. +10.36%) and holdout (−1.86% vs. +8.21%). The placebo beats the rule everywhere. Twelve switches per period means the signal flips every single month — this is not a tradable pattern; it is noise with maximum transaction costs. The signal has no demonstrated edge; it actively destroys value.

### Bull Case

The placebo's strong performance (+11.59% holdout net) suggests the *opposite* signal — holding equity when spreads widen — has predictive power. If registered as a new hypothesis with fresh holdout months, the reversed signal could be tested. The economic logic has a plausible reinterpretation: spread widening may coincide with equity mean-reversion (bounces after selloffs). However, this is speculation that requires an untouched test period.

### Selection Ledger

| # | Rule description | Result | Disposition |
|---|---|---|---|
| 1 | Signal > 0 (spread tightening) → equity; lag 1; cost 0.10% | Dev net +2.31%, Holdout net −1.86%; placebo beats rule everywhere | **Rejected** — failure rule triggered, placebo dominates |

No other rules were tried. The holdout was run once. No rule was changed after seeing the holdout.

---

## Decision

**REJECT.** The failure rule is triggered: holdout net (−1.86%) trails buy-and-hold (+8.21%) by over 10 percentage points. The placebo (flipped signal) outperforms the rule by 13+ points in the holdout. The signal as constructed has no demonstrated edge — it actively destroys value through excessive switching (12 switches in 12 months = 1,200% one-way turnover) and wrong-way positioning.

**Condition that would change this decision:** If the reversed signal is registered as a new hypothesis with a pre-committed rule card and tested on months after September 2026 (untouched holdout), and it beats both buy-and-hold and a new placebo net of costs with fewer than 6 switches per 12 months, it may warrant a bounded research pilot. The current holdout cannot be reused — it has been seen.

---

## Reflect

1. **What the holdout says that development did not:** Development already showed the rule trailing buy-and-hold (+2.31% vs. +10.36%), but the gap was ambiguous — maybe costs were the issue. The holdout removes all doubt: the rule went negative (−1.86%) while buy-and-hold gained +8.21%. The placebo's dominance in both periods proves the signal's sign was wrong from the start. Development hid this because the sample was too short and the margin too thin.

2. **What I would need before risking real money on this signal:** (a) A new hypothesis with the reversed sign, registered and committed before any new test. (b) At least 36 months of unseen data (neither development nor holdout). (c) A transaction-cost budget: fewer than 4 switches per year. (d) Evidence that the spread-change signal predicts next-month equity returns out-of-sample, not just in the placebo's lucky run. (e) A kill rule with a specific drawdown threshold and a named monitoring owner.

---

## Submission Checklist

| Required item | Status |
|---|---|
| Training reproduced: rule + placebo match known answer | ✅ |
| Frozen design: rule card committed before own run | ✅ |
| Own test: rule, placebo, B&H — dev & holdout, net of cost | ✅ |
| Bull, bear, and selection ledger | ✅ |
| Decision follows holdout + placebo with condition stated | ✅ Reject |
| AI disclosure | ✅ Built with AI help |

---

## Checkout

| Item | Location |
|---|---|
| Lab 19 report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_19.md |
| Backtest script (updated with placebo + CSV) | https://github.com/WGdearY/TICKER-research/blob/main/backtest.py |
| Own signal data | https://github.com/WGdearY/TICKER-research/blob/main/my_signal.csv |
