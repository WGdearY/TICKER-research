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

We address this question by adding one-at-a-time sensitivity analysis to our working 5-year pro-forma model for **NIKE, Inc. (NYSE: NKE)**. By isolating independent operating inputs, tracing them through linked financial statements, verifying accounting balance checks, and testing range dependencies, we determine which operational variables exert the greatest leverage over Nike's operating profit, free cash flow to equity (FCFE), and per-share equity value.

---

## 2. Reopen & Rerun Verification (Lab 10 Baseline)

Prior to conducting sensitivity testing, the base 5-year pro-forma engine ([`proforma_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_nke.py)) was executed from the terminal to establish and verify our baseline:

* **Command:** `python3 proforma_nke.py`
* **Base FY2031E Operating Profit (EBIT):** **$4,965.0M**
* **Base FY2031E Free Cash Flow to Equity (FCFE):** **$2,984.5M**
* **Base Intrinsic Value per Diluted Share:** **$30.19** (on 1,481.0M diluted shares)
* **Accounting Checks:** `Assets − Liabilities − Equity = 0.0` for all 5 projected years (FY2027E–FY2031E). Cash year-end remains above the $3,000M minimum operating liquidity floor in every period.

---

## 3. R — Represent: Operating Drivers, Ranges & Comparison Framework

### 1. Selection of Two Operating Drivers Already in the Model
We select two independent operational drivers from our Lab 10 assumption matrix, avoiding calculated statement totals:
1. **Driver 1: Gross Margin Trajectory (Operating Margin Driver)**
   * *Base Assumption:* Year-by-year glideslope [43.20%, 43.60%, 44.00%, 44.30%, 44.50%] reflecting supply chain normalization and reduced promotional markdowns recovering toward FY24 pre-discount levels (44.56%).
   * *Comparison Range:* $\pm 1.0\text{ percentage point}$ (pp) across all 5 forecast years.
     * Lower: [42.20%, 42.60%, 43.00%, 43.30%, 43.50%] (Trough lingering near FY25/FY26 levels).
     * Higher: [44.20%, 44.60%, 45.00%, 45.30%, 45.50%] (Rapid full-price DTC recovery).
   * *Reason for Range:* Nike's 3-year historical gross margin fluctuated between 42.73% (FY25 trough) and 44.56% (FY24 peak), spanning 1.83 percentage points. A $\pm 1.0$ pp range directly mirrors plausible operational upside from product innovation versus downside promotional drag.
2. **Driver 2: Capital Spending as % of Revenue (Operating Reinvestment Driver)**
   * *Base Assumption:* 1.50% of revenue in each forecast year ($716.8M in FY27E scaling to $838.5M in FY31E).
   * *Comparison Range:* 1.00% to 2.00% of revenue ($\pm 0.50\text{ percentage points}$ of revenue).
     * Lower: 1.00% of revenue ($477.9M in FY27E $\to$ $559.0M in FY31E).
     * Higher: 2.00% of revenue ($955.8M in FY27E $\to$ $1,118.0M in FY31E).
   * *Reason for Range:* Nike's historical CapEx ranged from 1.44% ($742M in FY24) to 1.50% ($695M in FY25) and 1.47% ($684M in FY26), while management guidance targets 1.5%–1.8% of sales. A tested range of 1.0% to 2.0% evaluates the boundary between severe maintenance capital rationing (1.0%) and aggressive supply-chain automation/regional distribution center expansion (2.0%).

### 2. Tested Input Ranges & Specifications

| Driver Name | Input Type & Scale | Base Input | Lower Run Input | Higher Run Input | Affected Years | Source / Grounding |
|---|---|:---:|:---:|:---:|:---:|---|
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

* **Record Timestamp:** `2026-09-29T14:06:50-04:00`
* **Git Commit Pre-Run Baseline:** `b65e778`
* **Prediction Formulation:**
  1. **Gross Margin Shift (+1.0 pp across all years):**
     * *Expected Direction:* Positive across EBIT, FCFE, and Value.
     * *Expected Magnitude:* In FY31E, +1.0 pp margin on $55,902M revenue increases gross profit by $\approx \$559\text{M}$. Because SG&A is modeled as 77% of gross profit, SG&A will absorb $\approx \$430\text{M}$, leaving $\approx +\$129\text{M}$ to flow to EBIT. After 20.3% taxes, net income and FCFE should rise by $\approx +\$100\text{M}$ to $+\$110\text{M}$. Value per share should increase by $\approx +\$1.00$ to $+\$1.20$/share.
  2. **CapEx Shift (+0.50 pp of revenue across all years):**
     * *Expected Direction:* Negative for FCFE and Value; negative for EBIT over time due to higher depreciation.
     * *Expected Magnitude:* In FY31E, 2.0% CapEx requires $\$1,118.0\text{M}$ vs $\$838.5\text{M}$ base, increasing direct cash outflow by $-\$279.5\text{M}$. Over 5 years, higher cumulative capex expands the net PP&E asset base, raising annual depreciation by $\approx \$126\text{M}$ in FY31E (which reduces EBIT by $-\$126\text{M}$). FCFE should drop by $\approx -\$250\text{M}$, and Value per share should fall by $\approx -\$2.20$ to $-\$2.50$/share.
  3. **Predicted Dominant Driver:** I predict that **CapEx as % of revenue will dominate Gross Margin in FCFE and Value per share spans**, because CapEx flows 100% directly out of cash flow, whereas Gross Margin gains are ~77% absorbed by SG&A overhead and ~20% taxed.

#### Partner Exchange 1 — Predict, Then Question
* **Presenter (Will Gao):** Explained the predicted transmission mechanism: CapEx changes impact cash flow with 100% flow-through, while Gross Margin improvements are diluted by variable SG&A reinvestment.
* **Partner's Question:** *"What evidence from Nike's 10-K filings supports your chosen range of 1.0% to 2.0% for capex, given that recent actual capex was ~1.47%?"*
* **Presenter's Response:** *"Management guidance in MD&A explicitly targets routine IT and supply chain reinvestment at 1.5%–1.8% of sales; 1.0% represents a strict maintenance-only capital holiday during a downturn, while 2.0% tests accelerated regional direct-to-consumer automated distribution center investments."*

---

## 4. I — Implement: Sensitivity Analysis Architecture & Execution

The sensitivity analysis was implemented in [`sensitivity_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_nke.py), utilizing Python standard library only.
* **Input Isolation:** The script defines `get_base_inputs()` returning an independent dictionary. Each run uses `copy.deepcopy()` to guarantee zero state contamination.
* **Linked Recalculation:** When an input changes, all linked accounting quantities dynamically recalculate:
  * Gross Margin changes dynamically alter Gross Profit $\to$ SG&A expense $\to$ Operating Profit $\to$ COGS $\to$ Inventory turnover $\to$ Taxes $\to$ FCFE $\to$ Cash.
  * CapEx changes dynamically alter Net PP&E asset balances $\to$ future Depreciation $\to$ Operating Income $\to$ Cash Flow reinvestment $\to$ FCFE $\to$ Cash.
* **Accounting Verification:** Every run enforces `assert_balanced()` verifying `Assets − Liabilities − Equity = 0.0`.
* **Base Restoration:** The base inputs are rerun at the conclusion of the test suite and asserted to match the pre-analysis base.

---

## 5. V — Validate: Results Table, Output Spans & Evidence Audit

### 1. One-at-a-Time Sensitivity Results Table

All values in USD millions ($M), except value per share ($/sh). All changes ($\Delta$) are signed relative to base.

```
==============================================================================================================
FIN 43900 LAB 11 — ONE-AT-A-TIME SENSITIVITY TABLE (NIKE, INC. / NKE)
==============================================================================================================
Independent Input / Case         FY31E EBIT ($M)    FY31E FCFE ($M)    Value ($/sh)     Checks    
--------------------------------------------------------------------------------------------------------------
Lower (-1.0 pp: 42.20% -> 43.50%)   4836.5 (-128.6)    2877.4 (-107.1)    29.12 (-1.07)  PASS (0.0)
Base (43.20% -> 44.50%)            4965.0 (  +0.0)    2984.5 (  +0.0)    30.19 (+0.00)  PASS (0.0)
Higher (+1.0 pp: 44.20% -> 45.50%)   5093.6 (+128.6)    3091.6 (+107.1)    31.26 (+1.07)  PASS (0.0)
--------------------------------------------------------------------------------------------------------------
Lower (1.00% of Rev, -0.5 pp)      5091.0 (+125.9)    3238.5 (+254.0)    32.60 (+2.40)  PASS (0.0)
Base (1.50% of Rev)                4965.0 (  +0.0)    2984.5 (  +0.0)    30.19 (+0.00)  PASS (0.0)
Higher (2.00% of Rev, +0.5 pp)     4839.1 (-125.9)    2730.6 (-254.0)    27.79 (-2.40)  PASS (0.0)
==============================================================================================================
```

### 2. Output Spans Table Over Stated Ranges
Output Span = $\max(\text{valid results}) - \min(\text{valid results})$ across Lower, Base, and Higher runs.

```
================================================================================
OUTPUT SPANS OVER TESTED RANGES (MAX − MIN ACROSS VALID RUNS)
================================================================================
Output Metric                  Gross Margin Span (±1.0 pp) CapEx % Span (1.0%–2.0%)
--------------------------------------------------------------------------------
FY2031E Operating Profit (EBIT) $   257.2 M                $   251.8 M
FY2031E Free Cash Flow (FCFE)  $   214.2 M                $   507.9 M
Value per Diluted Share        $    2.14 /sh              $    4.81 /sh
================================================================================
```

### 3. Restored Base Check Verification
```text
=== Restored Base Verification ===
Base Initial  : EBIT = $4965.0 M | FCFE = $2984.5 M | Value = $30.19
Base Restored : EBIT = $4965.0 M | FCFE = $2984.5 M | Value = $30.19
[SUCCESS] Restored-base check passed! No input or state contamination occurred.
```

### 4. Partner Exchange 2 — Checking Each Other's Evidence
* **Audit of Higher Margin Run:** Partner hand-verified the signed change from base:
  $$\Delta\text{FCFE} = 3,091.6 - 2,984.5 = \mathbf{+\$107.1\text{M}}$$
* **Statement Tracing:**
  * Gross margin increases from 44.50% to 45.50% (+1.0 pp) on FY31E revenue of $55,902.3M.
  * Gross profit increases from $24,876.5M to $25,435.5M (+$559.0M).
  * SG&A expense (modeled at 77.0% of gross profit) increases by $559.0M \times 77.0\% = +\$430.4M.
  * Operating profit (EBIT) increases by $559.0M - $430.4M = +\$128.6M ($5,093.6M vs $4,965.0M).
  * Income taxes rise by $\$128.6\text{M} \times 20.3\% = +\$26.1\text{M}$, so net income rises by $+\$102.5M.
  * Working capital adjusts: lower COGS slightly reduces inventory by $4.6M, freeing up operating cash.
  * Final FY31E FCFE rises by exactly $+\$107.1M ($3,091.6M vs $2,984.5M).
* **Isolation Confirmation:** Partner inspected variables and verified that Revenue Growth (3.0%), CapEx (1.5%), Tax Rate (20.3%), and Debt Repayment ($500M) stayed strictly at base values during this run.
* **Check Performed on Partner's Model:** I audited my partner's revenue growth shock, confirmed their balance sheet checks balanced to 0.0, and verified that their inventory days moved working capital dynamically without hardcoding cash.

---

## 6. E — Evolve: Find the Driver & Range Dependency

### 1. Main Driver Identification Over Stated Ranges
* **Operating Profit (EBIT):** **Gross Margin Trajectory** is the slightly larger driver over these ranges, producing an output span of **$257.2M** compared to **$251.8M** for CapEx.
* **Free Cash Flow to Equity (FCFE):** **CapEx % of Revenue** is by far the dominant driver, producing an output span of **$507.9M**, which is **2.37 times larger** than Gross Margin's span ($214.2M).
* **Value per Diluted Share:** **CapEx % of Revenue** is the dominant valuation driver, producing an output span of **$4.81 per share** ($32.60 vs $27.79), compared to **$2.14 per share** ($31.26 vs $29.12) for Gross Margin.

### 2. Explanation of Causal Mechanics: Why Does CapEx Lead Value?
1. **Flow-Through Dilution:** A 1.0 pp increase in gross margin adds $559M to gross profit, but under Nike's operational structure, **77.0% is absorbed by variable SG&A** (overhead and performance marketing), and 20.3% of the remainder is paid in taxes. Only **19.2%** of gross profit gains reach equity cash flow.
2. **Direct Reinvestment Impact:** In contrast, capital expenditures represent a **100% direct cash outflow** deducted from FCFE. Over a 5-year forecast, a $\pm 0.5$ pp shift in CapEx alters cash deployment by over $1.3 billion, heavily driving terminal cash flow and discounted equity value.

---

### 3. Range Dependency Demonstration: Halving the Gross Margin Range

To demonstrate that driver rankings are strictly conditioned **"over these ranges"** rather than representing immutable business truths, we halved the Gross Margin comparison range to $\pm 0.50\text{ percentage points}$ (keeping CapEx unchanged):

```
================================================================================
RANGE DEPENDENCY DEMONSTRATION: HALVED GROSS MARGIN RANGE (±0.5 pp)
================================================================================
Lower (-0.5 pp)           EBIT: $ 4900.8 M | FCFE: $ 2931.0 M | Value: $ 29.66 /sh
Base                      EBIT: $ 4965.0 M | FCFE: $ 2984.5 M | Value: $ 30.19 /sh
Higher (+0.5 pp)          EBIT: $ 5029.3 M | FCFE: $ 3038.1 M | Value: $ 30.73 /sh
--------------------------------------------------------------------------------
Halved Margin Spans: EBIT = $128.6 M | FCFE = $107.1 M | Value = $1.07 /sh
```

* **Observation:** Halving the input range from $\pm 1.0$ pp to $\pm 0.5$ pp cuts the output spans exactly in half:
  * EBIT span drops from $257.2M to $128.6M.
  * FCFE span drops from $214.2M to $107.1M.
  * Value per share span drops from $2.14/sh to $1.07/sh.
* **Key Takeaway:** If an analyst narrows the margin range to $\pm 0.5$ pp while maintaining CapEx at $1.0\%–2.0\%$, CapEx sweeps all three output spans (EBIT, FCFE, and Value). This proves that **sensitivity rankings reflect the width of the analyst's chosen range, not just the underlying corporate sensitivity.**

#### Partner Exchange 3 — Explain & Compare
* **Partner's Question:** *"Does CapEx dominating value mean Nike should focus its turnaround on capital rationing rather than fixing brand pricing?"*
* **Presenter's Response:** *"No. CapEx dominates the numerical span over this tested range because capex cuts flow dollar-for-dollar into cash flow, whereas gross margin gains are diluted by variable SG&A in our model. However, Nike's strategic existential risk is demand creation and gross margin erosion; CapEx is already low at 1.5% of sales, so further capital cuts offer limited economic upside in reality."*

---

## 7. Sensitivity — Learn on Your Own

1. **What is one-at-a-time sensitivity?**  
   One-at-a-time sensitivity is a financial modeling technique where exactly one independent operational input is varied across predefined high, base, and low values while holding all other independent inputs strictly constant. This isolates the marginal transmission mechanism of each variable through the integrated financial statements to determine its specific impact on profits, cash flows, and valuation.
2. **How does the chosen input range affect the ranking?**  
   The ranking of operating drivers by output span is directly determined by the width of the chosen input range. As proven in Section 6, artificially widening one variable's range or narrowing another immediately shifts which driver appears dominant. A sensitivity ranking is therefore only valid with the qualification **"over these tested ranges"** and must be evaluated alongside the empirical uncertainty of each input.
3. **Explain why a sensitivity table is not a forecast probability.**  
   A sensitivity table displays deterministic mathematical responses ("what-if" calculations); it does not assign likelihoods or probabilities to any tested endpoint. An input with a huge output span might have a 99% probability of staying within a tight corridor, while an input with a modest span might face radical macroeconomic uncertainty. Sensitivity tests model mechanics, not probability distributions.

---

## 8. Reflect

1. **Which driver mattered most over your ranges?**  
   Over the tested ranges ($\pm 1.0$ pp on Gross Margin vs $\pm 0.5$ pp of revenue on CapEx), **CapEx as % of revenue mattered most for Free Cash Flow to Equity (span of $507.9M)** and **Value per Share (span of $4.81/sh)**, while **Gross Margin Trajectory mattered slightly more for Operating Profit (span of $257.2M)**.
2. **Which result surprised you?**  
   I was surprised by how heavily Nike's operational SG&A structure blunts gross margin flow-through. Because Nike expenses ~10% of sales on Demand Creation and incurs substantial operating overhead (~77%–80% of gross profit), less than 20 cents of every incremental gross profit dollar reaches free cash flow. In contrast, capital expenditures bypass the income statement and hit free cash flow directly, making capex assumptions surprisingly potent in equity valuation.

---

## 9. Artifact and Script Registry

| Deliverable Name | Repository Path | Description |
|---|---|---|
| **Python Sensitivity Script** | [`sensitivity_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_nke.py) | Standalone Python 3 engine executing one-at-a-time sensitivity analysis, check blocks, and base restoration. |
| **Lab 11 Primary Report (Date-Ticker)** | [`sensitivity_0929_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_0929_NKE.md) | Authoritative Lab 11 markdown submission document containing all tables, checks, and partner exchanges. |
| **Lab 11 Primary Report (Standard / Ticker)** | [`sensitivity_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_NKE.md) · [`Lab_11.md`](file:///Users/wgdeary/FIN439%20work%20folder/Lab_11.md) | Synced cross-referenced file names ensuring accessibility across all evaluation mechanisms. |
| **Base Pro-Forma Model (Lab 10)** | [`proforma_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_nke.py) · [`proforma_0924_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_0924_NKE.md) | Verified 5-year balanced pro-forma foundation. |
| **GitHub Target Repository** | [`WGdearY/TICKER-research`](https://github.com/WGdearY/TICKER-research) | Main remote submission repository. |
