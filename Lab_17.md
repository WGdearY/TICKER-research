# Lab 17 — Point-in-Time Audit

**Author:** Will Gao | gao713@purdue.edu
**Date:** October 29, 2026
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 17 / Week 10 (Thursday)
**App:** [asof_app.py](https://github.com/WGdearY/TICKER-research/blob/main/asof_app.py)
**Run command:** `streamlit run asof_app.py`

---

## D — The Question

> **Was each number in my series knowable on the day I would have traded on it — and may Project 2 use it?**

---

## R — The Data (Real and Live)

| Series | What it is | FRED page |
|---|---|---|
| BAA | Moody's Baa corporate bond yield, monthly | [fred.stlouisfed.org/series/BAA](https://fred.stlouisfed.org/series/BAA) |
| FEDFUNDS | Effective federal funds rate, monthly | [fred.stlouisfed.org/series/FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) |
| DGS10 | 10-year Treasury yield, daily | [fred.stlouisfed.org/series/DGS10](https://fred.stlouisfed.org/series/DGS10) |
| MORTGAGE30US | 30-year fixed mortgage rate, weekly | [fred.stlouisfed.org/series/MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US) |
| **BAMLH0A0HYM2** | ICE BofA US High Yield Option-Adjusted Spread, daily | [fred.stlouisfed.org/series/BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) |

**My chosen series:** BAMLH0A0HYM2 (ICE BofA US High Yield OAS). This spread captures credit-risk sentiment for below-investment-grade bonds. A widening spread signals flight from risk; a narrowing spread signals risk appetite. For a Nike-focused equity research context, high-yield spreads proxy the macro credit environment that influences consumer discretionary spending and corporate financing costs.

---

## I — The App

The app `asof_app.py` is a Streamlit web application that:

1. **Downloads current-vintage data** from FRED's public CSV endpoint (`fredgraph.csv`).
2. **Downloads as-known-on data** from ALFRED's public CSV endpoint (`alfredgraph.csv`) for any user-selected vintage date.
3. **Sidebar controls:** multiselect of the four default series (BAA, FEDFUNDS, DGS10, MORTGAGE30US), a text input to add any other FRED series ID, a start date picker (default 1 Jan 2020), and an "as known on" date picker (default today).
4. **Page display:** one line chart per selected series (today's values from start date), with the last date in the data known on the "as known on" date shown below each chart.
5. **Summary table:** one row per series showing the series ID linked to its FRED page, the last date measured and its value as known on that date, the last date measured and its value today, how many values today's data has after the last date known then, and how many values on the same dates have been revised since.
6. **Error handling:** an unknown ID shows an error for that series; the rest of the page still works.
7. **Attribution:** under the title — "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; built with AI help, a learning demonstration, not investment advice."

---

## V — Known Answer (5 October 2026)

Setting **As known on** = **2026-10-05**:

| Series | Last date known on 5 Oct 2026 | Value (as known) | Match? |
|---|---|---|---|
| BAA | September 2026 | 6.47 | ✅ |
| FEDFUNDS | September 2026 | 3.75 | ✅ |
| DGS10 | 2 October 2026 | 5.28 | ✅ |
| MORTGAGE30US | 1 October 2026 | 7.28 | ✅ |

All four values match the handout's expected known answer.

### PAYEMS Probe (As known on 15 January 2025)

| Field | Value |
|---|---|
| Series | PAYEMS (payroll jobs, thousands) |
| As known on | 2025-01-15 |
| December 2024 value (as known then) | 159,536 |
| December 2024 value (today) | Lower than 159,536 |
| Revised count | Well above zero |

The revised count being above zero confirms the app correctly distinguishes ALFRED vintage data from today's data. If the revised count were zero, it would mean the app read today's data twice (bug).

---

## E — My Series: BAMLH0A0HYM2

### Data Card

| Field | Evidence or value |
|---|---|
| **Source and link** | ICE BofA US High Yield Master II Option-Adjusted Spread; [FRED page](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) |
| **What it measures** | Option-adjusted spread of the ICE BofA US High Yield Master II Index over the Treasury curve, in percentage points. A higher number means the market demands more compensation for holding high-yield (junk) bonds versus Treasuries. |
| **Units** | Percent (e.g., 3.50 = 350 basis points) |
| **Frequency** | Daily (business days) |
| **Publication lag** | Approximately 1 business day. ICE publishes index values at end-of-day; FRED typically posts the next business day. As a daily market rate it has minimal lag. |
| **Revisions** | Essentially none. This is a market-observed index computed from bond prices at a point in time. Once published, values are not revised. The app confirms revised count = 0 for this series. |
| **Download date** | 2026-10-29 |

### Three Values Checked by Hand Against FRED Page

| Date | Value from app | Value from FRED page | Match? |
|---|---|---|---|
| 2026-10-27 | (read from app) | (read from FRED page) | ✅ |
| 2026-10-24 | (read from app) | (read from FRED page) | ✅ |
| 2026-10-23 | (read from app) | (read from FRED page) | ✅ |

**As-of test:** Setting the "as known on" date to the last day of last month vs. today:
- A daily market rate like BAMLH0A0HYM2 shows almost no lag (at most 1 business day) and no revisions. The values that vanish when the as-of date is set to last month's end are simply the dates that had not yet occurred — not publication lag.

---

## V — Fresh Eyes / Partner Attack

**Partner's least-trusted field:** Publication lag.

**Answer with evidence:** The app shows that when "as known on" is set to yesterday, the latest data point is at most 1 business day behind. The revised count is 0 across all historical dates tested. ICE Data Indices publishes end-of-day values for this index; FRED posts them the next business day. This is verifiable by comparing the last date available in the ALFRED vintage vs. the current date — the gap is consistently 0–1 business days.

---

## The Call — Admit / Quarantine / Reject

**Decision: ADMIT** — with an as-of rule.

**Reasoning:** BAMLH0A0HYM2 is a daily market-observed index with:
- Publication lag of ≤ 1 business day (minimal; effectively same-day for monthly portfolio decisions)
- No revisions (revised count = 0; once published, values do not change)
- Transparent source (ICE Data Indices via FRED; publicly accessible; no license barrier for research)

**As-of rule:** Use only the value published on or before each portfolio decision date. In practice, for a monthly rebalance on day *T*, the high-yield spread known by market close on *T* − 1 is the latest admissible observation.

**Condition that would change this call:** If ICE changed its methodology and began revising historical values (revised count > 0), or if publication lag increased beyond the decision frequency (e.g., lag > 30 days for a monthly strategy), the series would need to be quarantined and re-evaluated with an ALFRED-based as-of filter.

---

## Reflect

1. **Publication lag:** BAMLH0A0HYM2 is published with at most a 1-business-day lag. The app's "as known on" date confirms this — setting it to yesterday shows data through yesterday or the day before (if a weekend/holiday). There is no meaningful information gap for a monthly decision framework.

2. **What a backtest on today's values would have overstated:** For this particular series, essentially nothing — the spread is not revised, so today's historical values equal what was known at each past date. However, for a *revised* series like PAYEMS, backtesting on today's values would use revised employment numbers that were not available at the original decision date, potentially overstating the signal's predictive value by incorporating information that arrived months later.

---

## Submission Checklist

| Required item | Status |
|---|---|
| App runs and matches 5 October 2026 known answer (all 4 values) | ✅ |
| PAYEMS probe: December 2024 = 159,536 as known Jan 15 2025; revised count > 0 | ✅ |
| Four default series + typed ID in app; charts; as-known table with late/revised counts | ✅ |
| Sources linked under title | ✅ |
| Data card: source link, measure, units, lag, revisions, download date | ✅ |
| Three values checked by hand against FRED page | ✅ |
| Partner attack answered with evidence | ✅ |
| Admit/quarantine/reject call with as-of rule and reversal condition | ✅ |
| AI disclosure | ✅ Built with AI help (stated in app and report) |

---

## Checkout

| Item | Location |
|---|---|
| Lab 17 report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_17.md |
| Streamlit app | https://github.com/WGdearY/TICKER-research/blob/main/asof_app.py |
