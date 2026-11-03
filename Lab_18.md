# Lab 18 — Holdout Test

**Author:** Will Gao | gao713@purdue.edu
**Date:** November 3, 2026
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 18 / Week 11 (Tuesday)
**Script:** [backtest.py](https://github.com/WGdearY/TICKER-research/blob/main/backtest.py)
**Run command:** `python3 backtest.py`

---

## D — The Question

> **Does a rule that worked in development still work on months it has never seen — after costs?**

### F-Squared Summary (Explained to Partner)

The SEC's 2014 F-Squared order found that a hypothetical ETF rotation record was advertised as live performance. The historical signals were shifted one week earlier than a trade could have occurred. This one-week timing leak let the backtest appear to sell before drops and buy before rises. Correcting the timing removed virtually all claimed pre-October-2008 outperformance. One week of look-ahead bias manufactured most of the apparent alpha.

---

## R — Rule Card (Committed Before Build)

| Rule card | Training value |
|---|---|
| Signal | month-end card-spend change, published by month-end |
| Rule | signal above 0 → hold the equity fund next month; otherwise Treasury bills |
| Lag | one month: this month's signal decides next month's position |
| Cost | 0.10% in any month the position switches; start in bills |
| Bills return | 0.3% a month |
| Development | 2025-01 to 2025-12 |
| Holdout | 2026-01 to 2026-06, run once, never tuned |
| Benchmark | buy-and-hold equity fund |
| Failure rule | stop if the holdout net return trails buy-and-hold |

---

## I — The Backtest

The script `backtest.py` implements the rule card exactly:

1. **Inputs at the top:** the monthly table (signal %, equity fund %), lag, cost per switch, bills return, development and holdout month ranges.
2. **Engine:** for each month, reads the signal from `lag` months prior. If signal > 0, hold equity; otherwise bills. Tracks switches and applies cost. Compounds gross and net returns separately.
3. **Holdout continuity:** the holdout starts from the position held at end of development (bills, after the Dec signal of −0.5).
4. **Output:** development and holdout separately — rule gross, rule net, buy-and-hold, and switches. Then the failure rule verdict.

---

## V — Known Answer

### Development (2025-01 to 2025-12)

| Month | Signal month | Signal | Position | Equity % | Gross % | Cost % | Net % |
|---|---|---:|---|---:|---:|---:|---:|
| 2025-01 | 2024-12 | +0.8 | equity | 2.0 | 2.0 | 0.10 | 1.90 |
| 2025-02 | 2025-01 | +1.2 | equity | 1.5 | 1.5 | 0.00 | 1.50 |
| 2025-03 | 2025-02 | +0.9 | equity | 3.0 | 3.0 | 0.00 | 3.00 |
| 2025-04 | 2025-03 | +1.5 | equity | −2.5 | −2.5 | 0.00 | −2.50 |
| 2025-05 | 2025-04 | −1.0 | bills | −1.5 | 0.3 | 0.10 | 0.20 |
| 2025-06 | 2025-05 | −0.7 | bills | −3.0 | 0.3 | 0.00 | 0.30 |
| 2025-07 | 2025-06 | −1.4 | bills | 2.5 | 0.3 | 0.00 | 0.30 |
| 2025-08 | 2025-07 | +1.1 | equity | 1.0 | 1.0 | 0.10 | 0.90 |
| 2025-09 | 2025-08 | +0.6 | equity | 2.0 | 2.0 | 0.00 | 2.00 |
| 2025-10 | 2025-09 | +0.9 | equity | −2.0 | −2.0 | 0.00 | −2.00 |
| 2025-11 | 2025-10 | −0.9 | bills | −1.0 | 0.3 | 0.10 | 0.20 |
| 2025-12 | 2025-11 | −0.5 | bills | 3.5 | 0.3 | 0.00 | 0.30 |

### Holdout (2026-01 to 2026-06)

| Month | Signal month | Signal | Position | Equity % | Gross % | Cost % | Net % |
|---|---|---:|---|---:|---:|---:|---:|
| 2026-01 | 2025-12 | +1.6 | equity | −2.0 | −2.0 | 0.10 | −2.10 |
| 2026-02 | 2026-01 | −1.1 | bills | 1.5 | 0.3 | 0.10 | 0.20 |
| 2026-03 | 2026-02 | +0.7 | equity | −3.0 | −3.0 | 0.10 | −3.10 |
| 2026-04 | 2026-03 | −1.3 | bills | 2.0 | 0.3 | 0.10 | 0.20 |
| 2026-05 | 2026-04 | +0.8 | equity | −1.5 | −1.5 | 0.10 | −1.60 |
| 2026-06 | 2026-05 | −0.6 | bills | 1.0 | 0.3 | 0.10 | 0.20 |

### Summary vs. Known Answer

| Period | Rule gross | Rule net | Buy-and-hold | Switches | Match? |
|---|---:|---:|---:|---:|---|
| Development | 6.55% | 6.13% | 5.33% | 4 | ✅ |
| Holdout | −5.52% | −6.09% | −2.09% | 6 | ✅ |

**Failure rule: TRIGGERED** — holdout net (−6.09%) trails buy-and-hold (−2.09%) by ~4 percentage points. ✅

**Turnover:** each switch moves all the money. 4 switches = 400% one-way turnover in development; 6 switches = 600% in holdout. The holdout's high turnover (every single month switches) amplifies costs and destroys any remaining edge.

---

## Lag-0 Break

Setting `LAG_MONTHS = 0` in the script:

| Metric | Lag = 1 (correct) | Lag = 0 (leak) |
|---|---:|---:|
| Development net | 6.13% | **17.72%** |

The jump from 6.13% to 17.72% is the leak: with lag 0, the rule uses the *same month's* signal to decide that month's position. It avoids losses it could not have known about. This is exactly the F-Squared error — trading on information nobody had at the time.

---

## Decision

**STOP.** The failure rule is triggered: the holdout net return (−6.09%) trails buy-and-hold (−2.09%). The rule that worked in development (+6.13% net vs. +5.33% B&H) does not survive on unseen months after costs. The signal's edge was either overfitted to the development period or the holdout regime reversed the signal-to-return relationship.

A new rule would require a new hypothesis registered before looking at new data, with fresh holdout months it has never seen. Re-tuning on the same holdout would make it worthless as a test.

---

## Reflect

1. **Why development looked good:** In 2025-05 through 2025-07, the signal correctly went negative and the rule hid in bills while equity dropped (−1.5%, −3.0%, then recovered). In 2025-08 through 2025-09, the signal correctly went positive and the rule captured equity gains (+1.0%, +2.0%). The rule avoided the worst drawdowns and caught some upside — but with only 12 months and a binary signal, this could be coincidence.

2. **What the commit time proves:** The commit timestamp on the rule card proves the rule was frozen before the backtest was built or run. Without it, there is no way to distinguish a preregistered hypothesis from one that was fitted to the data and then presented as a prediction. The commit is the audit trail that separates science from storytelling.

---

## Submission Checklist

| Required item | Status |
|---|---|
| Rule card committed before build | ✅ |
| Backtest matches known answer (dev & holdout) | ✅ |
| Lag-0 break seen (17.72%) | ✅ |
| Failure rule triggered | ✅ |
| Decision stated (stop / continue / new hypothesis) | ✅ Stop |
| F-Squared explanation | ✅ |
| AI disclosure | ✅ Built with AI help |

---

## Checkout

| Item | Location |
|---|---|
| Lab 18 report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_18.md |
| Backtest script | https://github.com/WGdearY/TICKER-research/blob/main/backtest.py |
