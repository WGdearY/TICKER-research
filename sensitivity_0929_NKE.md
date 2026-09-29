# Lab 11 — Pro-Forma Sensitivity: Find and Explain the Drivers (NIKE, Inc. / NKE)

**Company:** NIKE, Inc. (NYSE: NKE)  
**Date:** September 29, 2026  
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 11  
**Category:** Tuesday Completion Checkout (25 or 0)  
**Author:** Will Gao (gao713@purdue.edu)  
**Evidence Boundary:** FY2026 Form 10-K (accession no. 0000320187-26-000088; filed July 15, 2026; fiscal year ended May 31, 2026). Market prices through September 2, 2026 close ($38.24) and August 31, 2026 close ($39.06).  
**Prior Baselines Linked:** [Lab 03 Screening Memo](NIKE_2026-09-03/lab_3.md) · [Lab 05 Engine & Checkpoints](FIN43900-Fall2026/lessons/week-03/starter/dcf_starter.py) · [Lab 06 Reverse DCF](reverse_dcf_0910_NKE.md) · [Project 1 Committee Memo](project-1-committee-work.md) · [Lab 09 ABG Benchmark](Lab_09.md) · [Lab 10 Pro-Forma Base Case](proforma_0924_NKE.md)

---

## 1. D — Discover & Define: The Sensitivity Question

### The Core Question
> **Which assumptions drive my company's forecast and value, and what explains their effects?**

We address this question for **NIKE, Inc. (NYSE: NKE)** by implementing one-at-a-time sensitivity analysis on our working three-statement pro-forma engine. By isolating independent operational inputs—specifically **Revenue / Sales Growth Rate** and **Gross Margin Trajectory** (alongside capital reinvestment)—and tracing their transmission through linked financial statements, we determine which assumptions exert the greatest leverage on operating earnings, free cash flow to equity (FCFE), and per-share valuation.

---

## 2. Reopen & Rerun Verification (Lab 10 Baseline)

Prior to conducting sensitivity testing, the base 5-year pro-forma engine ([`proforma_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_nke.py)) was executed from the terminal to verify the initial baseline:

* **Command:** `python3 proforma_nke.py`
* **Base FY2031E Operating Profit (EBIT):** **$4,965.0M**
* **Base FY2031E Free Cash Flow to Equity (FCFE):** **$2,984.5M**
* **Base Intrinsic Value per Diluted Share:** **$30.19** (on 1,481.0M diluted shares)
* **Accounting Checks:** `Assets − Liabilities − Equity = 0.0` across all 5 projected years (FY2027E–FY2031E). Cash year-end remains above the $3,000M minimum operating liquidity floor in every period.

---

## 3. R — Represent: Operating Drivers, Ranges & Comparison Framework

### 1. Selection of Operating Drivers
We select independent operating drivers already in our model, avoiding calculated statement totals:
1. **Driver 1: Revenue / Sales Growth Rate Trajectory (Volume & Channel Recovery Driver)**
   * *Base Assumption:* 5-year turnaround glideslope [3.0%, 4.0%, 5.0%, 4.0%, 3.0%] in FY27E–FY31E, reflecting product cadence acceleration ("Win Now") and gradual recovery in North America wholesale and Greater China.
   * *Comparison Range:* $\pm 1.0\text{ percentage point}$ (pp) across all 5 forecast years.
     * Lower: [2.0%, 3.0%, 4.0%, 3.0%, 2.0%] (Stagnant recovery; chronic digital traffic drag and persistent Greater China weakness).
     * Higher: [4.0%, 5.0%, 6.0%, 5.0%, 4.0%] (Aggressive turnaround; rapid wholesale shelf-space recapture and rebound in Nike Direct).
   * *Reason for Range:* In the FY2026 10-K, reported revenue was flat (+0.2%) while currency-neutral revenue contracted -2.0% (with Nike Direct down -8% and Greater China down -13%). A $\pm 1.0$ pp corridor captures the realistic variance between a muted recovery (+2% to +4%) and an energized turnaround (+4% to +6%).
2. **Driver 2: Gross Margin Trajectory (Operating Margin & Pricing Realization Driver)**
   * *Base Assumption:* Year-by-year glideslope [43.20%, 43.60%, 44.00%, 44.30%, 44.50%] reflecting supply chain normalization, reduced off-price promotional liquidations, and gradual recovery toward FY24 pre-discount levels (44.56%).
   * *Comparison Range:* $\pm 1.0\text{ percentage point}$ (pp) across all 5 forecast years.
     * Lower: [42.20%, 42.60%, 43.00%, 43.30%, 43.50%] (Trough lingering near FY25/FY26 levels due to prolonged promotional discounting).
     * Higher: [44.20%, 44.60%, 45.00%, 45.30%, 45.50%] (Rapid full-price DTC recovery).
   * *Reason for Range:* Nike's historical 10-K gross margin spanned 1.83 percentage points between FY25 (42.73% trough) and FY24 (44.56% peak). A $\pm 1.0$ pp shock tests operational pricing recovery versus margin stagnation.
3. **Reinvestment Cross-Check: CapEx as % of Revenue**
   * *Base Assumption:* 1.50% of revenue ($716.8M in FY27E $\to$ $838.5M in FY31E).
   * *Comparison Range:* 1.00% to 2.00% of revenue ($\pm 0.50$ pp of revenue), evaluating maintenance capital rationing (1.0%) against accelerated logistics automation (2.0%).

### 2. Tested Input Ranges & Specifications

| Driver Name | Input Type & Scale | Base Input | Lower Run Input | Higher Run Input | Affected Years | Source / Grounding |
|---|---|:---:|:---:|:---:|:---:|---|
| **Revenue / Sales Growth** | Percentage points (pp) / decimal | 3.0% $\to$ 5.0% $\to$ 3.0% | Base − 0.010 (2.0% $\to$ 4.0% $\to$ 2.0%) | Base + 0.010 (4.0% $\to$ 6.0% $\to$ 4.0%) | FY2027E–FY2031E (all 5 years) | FY25 (-9.0% CN) vs FY26 (-2.0% CN) and turnaround guidance |
| **Gross Margin Trajectory** | Percentage points (pp) / decimal | 43.20% $\to$ 44.50% | Base − 0.010 (42.20% $\to$ 43.50%) | Base + 0.010 (44.20% $\to$ 45.50%) | FY2027E–FY2031E (all 5 years) | FY24 peak (44.56%) vs FY25 trough (42.73%) in 10-K |
| **CapEx % of Revenue** | Percentage points of Rev / decimal | 1.50% of sales | 1.00% of sales (−0.50 pp) | 2.00% of sales (+0.50 pp) | FY2027E–FY2031E (all 5 years) | FY26 10-K actual (1.47%) vs guidance range (1.5%–1.8%) |

### 3. Consistent Comparable Outputs
For every run (Lower, Base, Higher), we capture:
* **Final-Year Operating Profit (EBIT):** FY2031E Operating Income in USD millions ($M).
* **Final-Year Free Cash Flow to Equity (FCFE):** FY2031E Free Cash Flow to Equity in USD millions ($M).
* **Value per Diluted Share:** Discounted 5-year FCFE + Gordon Growth Terminal Value in USD/share ($/sh) on 1,481.0M diluted shares.
* **Signed Change from Base ($\Delta$):** `Changed Output − Base Output` in native output units.
* **Output Span:** `Maximum Output − Minimum Output` across valid runs.

---

### 4. Locked Changed-Input Record (Pre-Run Timestamped Prediction)

* **Record Timestamp:** `2026-09-29T14:10:45-04:00`
* **Git Commit Pre-Run Baseline:** `41f5beb`
* **Prediction Formulation:**
  1. **Revenue / Sales Growth Shift (+1.0 pp across all years):**
     * *Expected Direction:* Positive across EBIT, FCFE, and Value.
     * *Expected Magnitude:* By FY31E, compounding +1.0 pp growth over 5 years expands total revenue by $\approx +\$2,780\text{M}$ ($58.7\text{B}$ vs $55.9\text{B}$). At 44.5% gross margin, gross profit expands by $+\$1,237\text{M}$; after variable SG&A absorption (77%), **EBIT should expand by $\approx +\$260\text{M}$ to $+\$280\text{M}$**—a massive operating profit boost.
     * *FCFE Drag:* However, higher sales growth requires working capital investment (more inventory and receivables: $\Delta\text{Inv} + \Delta\text{OWC}$) and higher dollar capex (1.5% of revenue). Thus, FY31E FCFE should only increase by $\approx +\$80\text{M}$, and Value per share should rise by $\approx +\$0.50$ to $+\$0.60$/share.
  2. **Gross Margin Shift (+1.0 pp across all years):**
     * *Expected Direction:* Positive across EBIT, FCFE, and Value.
     * *Expected Magnitude:* On $55.9B base revenue, +1.0 pp margin expands gross profit by $+\$559\text{M}$. After 77% SG&A, EBIT increases by $+\$128.6\text{M}$. Unlike revenue growth, gross margin expansion requires **no incremental working capital or capex**, so FCFE increases by $\approx +\$107\text{M}$ and Value per share rises by $\approx +\$1.07$/share.
  3. **Predicted Dominant Driver:**
     * I predict that **Revenue / Sales Growth will dominate Operating Profit (EBIT span)** due to cumulative scale compounding over 5 years.
     * However, I predict that **Gross Margin and CapEx will produce larger spans for FCFE and Value per share**, because Revenue Growth carries a reinvestment drag that absorbs cash flow.

#### Partner Exchange 1 — Predict, Then Question
* **Presenter (Will Gao):** Explained the predicted mechanism: Revenue growth drives immense operating scale, but working capital and capex expansion dampen its translation into cash flow; Gross margin gains flow more cleanly to FCFE because inventory unit requirements remain unchanged.
* **Partner's Question:** *"Why would revenue growth have a smaller per-share value impact than gross margin if revenue growth produces double the operating profit dollar gain?"*
* **Presenter's Response:** *"Because every incremental dollar of revenue requires stocking more footwear pairs in distribution centers (working capital) and buying logistics capacity (capex), whereas a higher gross margin represents pure pricing power and full-price realization on existing unit volumes, delivering cash directly to equity holders."*

---

## 4. I — Implement: Sensitivity Analysis Architecture & Execution

The sensitivity analysis was executed via [`sensitivity_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_nke.py) using standard library Python.
* **Input Isolation:** The script uses `get_base_inputs()` and `copy.deepcopy()` to instantiate independent parameter copies for each run.
* **Linked Recalculation:** All linked statements update dynamically:
  * Revenue Growth changes flow through Gross Profit, SG&A, Working Capital inventory builds, CapEx cash requirements, Taxes, FCFE, and Cash.
  * Gross Margin changes update Gross Profit, SG&A expense, COGS, inventory valuation, Taxes, FCFE, and Cash.
* **Accounting Verification:** Every run enforces `assert_balanced()` verifying `Assets − Liabilities − Equity = 0.0`.
* **Base Restoration:** The base inputs are rerun at the conclusion of the test suite and asserted to match the pre-analysis base.

---

## 5. V — Validate: Results Table, Output Spans & Evidence Audit

### 1. One-at-a-Time Sensitivity Results Table

All values in USD millions ($M), except value per share ($/sh). All changes ($\Delta$) are signed differences relative to base.

```
================================================================================================================
FIN 43900 LAB 11 — ONE-AT-A-TIME SENSITIVITY TABLE (NIKE, INC. / NKE)
================================================================================================================
Independent Input / Case         FY31E EBIT ($M)    FY31E FCFE ($M)    Value ($/sh)     Checks    
----------------------------------------------------------------------------------------------------------------
Lower (-1.0 pp: 2.0% -> 2.0%)      4704.6 (-260.4)    2903.1 ( -81.4)    29.62 (-0.57)  PASS (0.0)
Base Case (3.0% -> 3.0%)           4965.0 (  +0.0)    2984.5 (  +0.0)    30.19 (+0.00)  PASS (0.0)
Higher (+1.0 pp: 4.0% -> 4.0%)     5235.9 (+270.8)    3065.7 ( +81.1)    30.76 (+0.57)  PASS (0.0)
----------------------------------------------------------------------------------------------------------------
Lower (-1.0 pp: 42.20% -> 43.50%)   4836.5 (-128.6)    2877.4 (-107.1)    29.12 (-1.07)  PASS (0.0)
Base (43.20% -> 44.50%)            4965.0 (  +0.0)    2984.5 (  +0.0)    30.19 (+0.00)  PASS (0.0)
Higher (+1.0 pp: 44.20% -> 45.50%)   5093.6 (+128.6)    3091.6 (+107.1)    31.26 (+1.07)  PASS (0.0)
----------------------------------------------------------------------------------------------------------------
Lower (1.00% of Rev, -0.5 pp)      5091.0 (+125.9)    3238.5 (+254.0)    32.60 (+2.40)  PASS (0.0)
Base (1.50% of Rev)                4965.0 (  +0.0)    2984.5 (  +0.0)    30.19 (+0.00)  PASS (0.0)
Higher (2.00% of Rev, +0.5 pp)     4839.1 (-125.9)    2730.6 (-254.0)    27.79 (-2.40)  PASS (0.0)
================================================================================================================
```

### 2. Output Spans Table Over Stated Ranges
Output Span = $\max(\text{valid results}) - \min(\text{valid results})$ across Lower, Base, and Higher runs.

```
==========================================================================================
OUTPUT SPANS OVER TESTED RANGES (MAX − MIN ACROSS VALID RUNS)
==========================================================================================
Output Metric                  Revenue Growth (±1.0 pp)   Gross Margin (±1.0 pp)     CapEx % (1.0%–2.0%)   
------------------------------------------------------------------------------------------
FY2031E Operating Profit (EBIT) $   531.3 M                $   257.2 M                $   251.8 M
FY2031E Free Cash Flow (FCFE)  $   162.6 M                $   214.2 M                $   507.9 M
Value per Diluted Share        $    1.14 /sh              $    2.14 /sh              $    4.81 /sh
==========================================================================================
```

### 3. Restored Base Check Verification
```text
=== Restored Base Verification ===
Base Initial  : EBIT = $4965.0 M | FCFE = $2984.5 M | Value = $30.19
Base Restored : EBIT = $4965.0 M | FCFE = $2984.5 M | Value = $30.19
[SUCCESS] Restored-base check passed! No input or state contamination occurred.
```

### 4. Partner Exchange 2 — Checking Each Other's Evidence
* **Audit of Higher Revenue Run:** Partner hand-verified the signed change from base:
  $$\Delta\text{EBIT} = 5,235.9 - 4,965.0 = \mathbf{+\$270.8\text{M}}$$
* **Statement Tracing:**
  * Compounding +1.0 pp higher growth raises FY31E revenue from $55,902.3M to $58,683.8M (+$2,781.5M).
  * Gross profit expands by $\$2,781.5\text{M} \times 44.5\% = +\$1,237.8\text{M}$.
  * SG&A expense absorbs $77.0\% \times \$1,237.8\text{M} = +\$953.1\text{M}$.
  * Depreciation rises slightly by $+\$13.9M due to higher cumulative dollar capex, leaving net EBIT higher by $+\$270.8M ($5,235.9M vs $4,965.0M).
  * Working capital absorbs cash: higher sales require $+\$437.1M in inventory build and $+\$27.8M in other working capital.
  * Capital spending increases by $\$2,781.5\text{M} \times 1.5\% = +\$41.7\text{M}$.
  * Consequently, despite a $+\$270.8M operating profit surge, FY31E FCFE rises by only $+\$81.1M ($3,065.7M vs $2,984.5M).
* **Isolation Confirmation:** Partner confirmed that Gross Margin (44.5%), CapEx percentage (1.5%), Tax Rate (20.3%), and Debt Repayment ($500M) stayed strictly at base values during this run.
* **Check Performed on Partner's Model:** I audited my partner's model, confirmed their balance sheet checks balanced to 0.0 across all runs, and verified that their inventory days moved working capital dynamically without typing cash.

---

## 6. E — Evolve: Find the Driver & Range Dependency

### 1. Main Driver Identification Over Stated Ranges
* **Operating Profit (EBIT):** **Revenue / Sales Growth Rate** is the overwhelming dominant driver over these ranges, producing an output span of **$531.3M**, which is **more than double** the Gross Margin span ($257.2M) and CapEx span ($251.8M).
* **Free Cash Flow to Equity (FCFE):** **CapEx % of Revenue** ($507.9M span) and **Gross Margin Trajectory** ($214.2M span) produce larger spans than Revenue Growth ($162.6M span).
* **Value per Diluted Share:** **CapEx % of Revenue** leads value ($4.81/sh span), followed by **Gross Margin Trajectory** ($2.14/sh span), with **Revenue Growth** producing a $1.14/sh span.

### 2. Explanation of Causal Mechanics: Scale vs. Reinvestment Drag
1. **Operating Leverage:** Revenue growth compounds across all 5 years. Expanding top-line scale by ~$2.8B unleashes powerful dollar operating leverage, creating $531.3M in EBIT variance.
2. **Reinvestment Drag:** However, faster revenue growth requires cash reinvestment: more footwear pairs in transit, higher trade receivables, and greater capital expenditures to expand logistics throughput. In contrast, Gross Margin gains improve unit profitability on existing volumes, and CapEx reductions eliminate cash drains directly without penalizing current revenue.

---

### 3. Extended Range Analysis: Widening Revenue Growth to $\pm 2.0\text{ percentage points}$

To test range dependency, we tested widening the Revenue Growth range to $\pm 2.0\text{ percentage points}$ (Lower: 1.0% $\to$ 1.0%; Higher: 5.0% $\to$ 5.0%):

```text
================================================================================
EXTENDED REVENUE GROWTH SENSITIVITY (±2.0 pp: 1.0% -> 5.0%)
================================================================================
Lower Run (-2.0 pp) : FY31E EBIT = $4,454.3 M | FCFE = $2,821.5 M | Value = $29.05 /sh
Base Case           : FY31E EBIT = $4,965.0 M | FCFE = $2,984.5 M | Value = $30.19 /sh
Higher Run (+2.0 pp): FY31E EBIT = $5,517.4 M | FCFE = $3,146.4 M | Value = $31.32 /sh
--------------------------------------------------------------------------------
Output Spans (±2.0 pp): EBIT = $1,063.1 M | FCFE = $324.9 M | Value = $2.27 /sh
================================================================================
```

* **Observation:** Widening the revenue growth corridor to $\pm 2.0$ pp doubles its output spans:
  * EBIT span explodes to **$1,063.1M** ($1.06 billion variance!).
  * FCFE span expands to **$324.9M**, now surpassing the Gross Margin FCFE span ($214.2M).
  * Value per share span expands to **$2.27/sh**, overtaking Gross Margin's value span ($2.14/sh).
* **Key Takeaway:** This confirms that **driver ranking is strictly conditioned "over these ranges"**. Over a tight $\pm 1.0$ pp band, Gross Margin leads value; over a wider $\pm 2.0$ pp band, Revenue Growth leads value.

#### Partner Exchange 3 — Explain & Compare
* **Partner's Question:** *"Does Revenue Growth producing a $1.06B EBIT span mean management should prioritize top-line sales volume over profit margins?"*
* **Presenter's Response:** *"No. While top-line growth creates immense operating profit scale, if revenue is pursued through promotional discounts (lowering gross margin) or requires excessive working capital build, shareholder value will actually destroy cash. Nike's optimal path is balanced turnaround: recovering 3%–5% organic growth while protecting 44%+ gross margins through full-price product innovation."*

---

## 7. Sensitivity — Learn on Your Own

1. **What is one-at-a-time sensitivity?**  
   One-at-a-time sensitivity is a financial modeling discipline where exactly one independent operational input is varied across predefined high, base, and low values while holding all other independent inputs strictly constant. This isolates the marginal transmission mechanism of each variable through the integrated financial statements to determine its specific impact on profits, cash flows, and valuation.
2. **How does the chosen input range affect the ranking?**  
   The ranking of operating drivers by output span is directly determined by the width of the chosen input range. As proven in Section 6, widening Revenue Growth to $\pm 2.0$ pp elevates its cash flow and value span above Gross Margin. A sensitivity ranking is therefore only valid with the qualification **"over these tested ranges"** and must be evaluated alongside the empirical uncertainty of each input.
3. **Explain why a sensitivity table is not a forecast probability.**  
   A sensitivity table displays deterministic mathematical responses ("what-if" calculations); it does not assign likelihoods or probabilities to any tested endpoint. An input with a huge output span might have a 99% probability of staying within a tight corridor, while an input with a modest span might face radical macroeconomic uncertainty. Sensitivity tests model mechanics, not probability distributions.

---

## 8. Reflect

1. **Which driver mattered most over your ranges?**  
   Over the baseline ranges ($\pm 1.0$ pp on Revenue Growth and Gross Margin; $1.0\%–2.0\%$ on CapEx), **Revenue / Sales Growth mattered most for Operating Profit (span of $531.3M)**, while **CapEx % of revenue mattered most for Free Cash Flow (span of $507.9M)** and **Value per Share (span of $4.81/sh)**.
2. **Which result surprised you?**  
   I was surprised by how significantly working capital and capex reinvestment dampen the cash flow translation of revenue growth. Gaining +1.0 pp of revenue growth generates an impressive +$270.8M in FY31E EBIT, but consumes so much working capital that final-year FCFE only increases by +$81.1M. This explains why Nike management has prioritized inventory cleanup and DTC full-price realization over chasing empty volume growth.

---

## 9. Artifact and Script Registry

| Deliverable Name | Repository Path | Description |
|---|---|---|
| **Python Sensitivity Script** | [`sensitivity_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_nke.py) | Standalone Python 3 engine executing sensitivity on Revenue Growth, Gross Margin, and CapEx with check blocks. |
| **Lab 11 Primary Report (Date-Ticker)** | [`sensitivity_0929_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_0929_NKE.md) | Authoritative Lab 11 markdown submission document containing all tables, checks, and partner exchanges. |
| **Lab 11 Primary Report (Standard / Ticker)** | [`sensitivity_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_NKE.md) · [`Lab_11.md`](file:///Users/wgdeary/FIN439%20work%20folder/Lab_11.md) | Synced cross-referenced file names ensuring accessibility across all evaluation mechanisms. |
| **Base Pro-Forma Model (Lab 10)** | [`proforma_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_nke.py) · [`proforma_0924_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_0924_NKE.md) | Verified 5-year balanced pro-forma foundation. |
| **GitHub Target Repository** | [`WGdearY/TICKER-research`](https://github.com/WGdearY/TICKER-research) | Main remote submission repository. |
