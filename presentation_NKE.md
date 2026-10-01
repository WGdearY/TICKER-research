# Lab 12 — Pro-Forma: Present and Review Your Full Analysis (NIKE, Inc. / NKE)

**Company:** NIKE, Inc. (NYSE: NKE)  
**Date:** October 1, 2026  
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 12  
**Category:** Thursday Merit Checkout (25 points total — 5 merit anchors @ 5 pts each)  
**Author:** Will Gao (gao713@purdue.edu)  
**Evidence Boundary:** FY2026 Form 10-K (accession no. 0000320187-26-000088; filed July 15, 2026; fiscal year ended May 31, 2026). Market prices through September 2, 2026 close ($38.24) and August 31, 2026 close ($39.06).  
**Prior Baselines Linked:** [Lab 03 Screening Memo](NIKE_2026-09-03/lab_3.md) · [Lab 05 Engine & Checkpoints](FIN43900-Fall2026/lessons/week-03/starter/dcf_starter.py) · [Lab 06 Reverse DCF](reverse_dcf_0910_NKE.md) · [Project 1 Committee Memo](project-1-committee-work.md) · [Lab 09 ABG Benchmark](Lab_09.md) · [Lab 10 Pro-Forma Engine](proforma_0924_NKE.md) · [Lab 11 Sensitivity Engine](sensitivity_0929_NKE.md)

---

## 1. D — Discover & Define: The Synthesis Question

> **"How did I get from choosing this company to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?"**

This report documents the full end-to-end investment research arc for **NIKE, Inc. (NYSE: NKE)**, synthesizing primary SEC Form 10-K filings, three-statement financial modeling, valuation triangulation, one-at-a-time sensitivity analysis, and an in-person reciprocal peer review exchange.

---

## 2. R & I — The Full Six-Stop Analysis Presentation Route

### Stop 1: Target Selection & Initial View
* **Why Selected:** Nike is a premier global consumer athletic brand undergoing a high-stakes leadership and operational turnaround under CEO Elliott Hill's "Win Now" product cadence.
* **Suitability:** Robust US GAAP reporting with clear line-item granularity in annual Form 10-K filings; liquid Class B common stock (NYSE: NKE); accessible primary disclosures on wholesale versus Direct-to-Consumer (DTC) channels.
* **Initial View:** Following a ~45% share price decline from historical highs, market sentiment appeared excessively pessimistic. If brand equity, pricing power, and gross margins remained structurally intact, current market pricing could present an asymmetric entry point.

### Stop 2: Company Operations & Audited Primary Evidence Boundary
* **How Nike Earns Money:** Designing, developing, and marketing athletic footwear (66% of revenues), apparel (28%), and equipment/accessories through Wholesale retail partners (59% of sales) and Nike Direct digital apps and stores (41%).
* **Primary Evidence Boundary:** FY2026 Form 10-K (filed July 15, 2026, for the fiscal year ended May 31, 2026).
* **Key Audited Baseline Figures:**
  * **Revenues:** **$46,398M** (flat reported vs. $46,309M in FY25; down 2.0% currency-neutral).
  * **Gross Profit & Margin:** **$19,911M** (42.91% gross margin vs. 42.73% in FY25 and 44.56% in FY24).
  * **SG&A Expense:** **$16,114M** (Demand Creation: $4,754M; Operating Overhead: $11,360M).
  * **Operating Income (EBIT):** **$3,850M** (8.30% operating margin per 10-K ROIC reconciliation).
  * **Net Income & Diluted Shares:** **$3,108M** net income on **1,481.0M** diluted weighted-average shares.
  * **Capital Structure & Net Cash:** Total book debt of **$7,942M** ($2,000M current portion + $5,942M senior notes) against **$9,027M** in liquid cash and short-term investments, yielding a **$1,085M net cash position**.

### Stop 3: The Three-Statement Pro-Forma Engine
* **How History Became Forecast:** Transformed 3-year historical 10-K trends (FY24 peak $\to$ FY25 trough $\to$ FY26 reset) into a 19-assumption matrix modeling FY2027E–FY2031E.
* **The Personalization Line:** **Floor Plan Financing is declared as `"none"` ($0.0)**. Unlike automotive dealerships (Asbury / ABG), Nike carries zero lot inventory debt. Instead, Nike's unique operational line is **Demand Creation Expense** (~10.2% of sales / $4.75B/yr) within SG&A—a vital operational brand reinvestment rather than back-office overhead.
* **Statement Linkage & Checks:** Cash is computed last as the dynamic plug. **`assert_balanced()`** programmatically enforces $\text{Assets} - \text{Liabilities} - \text{Equity} = 0.0$ in every year. Revolver borrowing is $0.0 across all years because cash balances remain between $7.7B and $8.4B, well above the $3,000M minimum liquidity floor.

### Stop 4: Valuation Methods, Triangulation & Divergence
We evaluate three distinct valuation lenses without artificially averaging conflicting results:

| Valuation Lens | Output Value | Primary Driver / Core Assumption | Reason for Disagreement & Methodology Limitation |
|---|---:|---|---|
| **Base Pro-Forma DCF (Lab 10)** | **$30.19 / share** | 5-year FCFE glideslope; gross margin 43.2% $\to$ 44.5%; 77% SG&A ratio; 9.0% $r_e$; 2.5% $g$. | **Conservative Lower Bound:** Reflects heavy variable SG&A reinvestment and routine capex, resulting in moderate FCFE expansion. |
| **Turnaround DCF (Project 1 Memo)** | **$48.53 / share** | Unlevered FCFF; EBIT margin expanding aggressively from 8.3% to 12.0% by FY31E; 9.0% WACC; 2.5% $g$. | **Optimistic Upper Bound:** 76% of enterprise value is concentrated in the terminal value; assumes complete profit margin recovery. |
| **Reverse DCF (Lab 06)** | **$38.24 / share** (Market Close) | Solves backward from market price ($38.24 on Sept 2, 2026). | Implies the market is pricing in either **~2.8% perpetual growth** or requiring an immediate EBIT margin jump above 10.5%. |

* **Method Disagreement Synthesis:** The market price of $38.24 reflects a pricing posture that credits Nike with partial turnaround success, trading at a 27% premium over our conservative pro-forma base ($30.19) while discounting the committee's full-recovery scenario ($48.53).

### Stop 5: Sensitivity & Key Operating Drivers (Lab 11 Findings)
* **Tested Drivers:** Revenue/Sales Growth Rate ($\pm 1.0\text{ pp}$), Gross Margin Trajectory ($\pm 1.0\text{ pp}$), and CapEx % of Revenue (1.0% to 2.0%).
* **Output Spans Across Tested Ranges:**
  * **Operating Profit (EBIT):** **Revenue / Sales Growth** is the dominant driver (**$531.3M span**), more than doubling Gross Margin ($257.2M) and CapEx ($251.8M).
  * **Free Cash Flow to Equity (FCFE):** **CapEx % of Revenue** ($507.9M span) and **Gross Margin** ($214.2M span) dominate Revenue Growth ($162.6M span).
  * **Value per Diluted Share:** **CapEx** leads value ($4.81/sh span), followed by **Gross Margin** ($2.14/sh span) and **Revenue Growth** ($1.14/sh span).
* **Causal Transmission & Reinvestment Drag:** Compounding top-line sales growth creates massive dollar operating leverage, but consumes cash through working capital ($\Delta\text{Inventory}$ and receivables) and dollar capex. Gross Margin gains improve unit realization on existing volume without requiring working capital cash drain.
* **Range Qualification:** Driver rankings are strictly conditioned **"over these ranges"**; widening Revenue Growth to $\pm 2.0\text{ pp}$ expands its EBIT span to **$1,063.1M ($1.06 Billion)** and elevates its value span to $2.27/sh, surpassing Gross Margin.

### Stop 6: Conditional Recommendation & Reinvestment Triggers
* **Current Posture:** **Watch / Defer.**
* **Trigger Price:** Do not initiate a position at $38.24; reconsider opening a 12-month position at or below **$36.40 per share** (providing a 25% margin of safety against the committee turnaround DCF).
* **Observable Filing Triggers to Revisit:**
  1. Consecutive quarterly Form 10-Q filings showing Nike Direct digital traffic returning to positive currency-neutral comps.
  2. Gross margins stabilizing above 43.5% without promotional markdown accruals.
  3. Greater China wholesale channel revenues stabilizing year-over-year.

---

## 3. V — Reviewer's Cross-Examination & Live Calculation Check

During the peer review exchange, the reviewer executed substantive cross-examination across all three mandatory areas:

### 1. Selection & Evidence Question
* **Reviewer's Question:** *"Why did you select Nike over a pure-play growth peer like On Holding or Deckers, and what primary SEC 10-K footnote supports your $7,942M debt figure?"*
* **Presenter's Answer:** *"I selected Nike because its turnaround presents a classic asymmetric value thesis where mature global distribution infrastructure is temporarily obscured by product execution missteps. The $7,942M debt figure is verified directly from Note 6 (Long-Term Debt, page 70 of the FY2026 Form 10-K), comprising $2,000M in current maturities and $5,942M in senior unsecured notes."*

### 2. Model & Valuation Question
* **Reviewer's Question:** *"Why does your pro-forma model produce $30.19 while your Project 1 memo yields $48.53, and what specific operational mechanism explains the $18.34 difference?"*
* **Presenter's Answer:** *"The $18.34 gap stems from margin trajectory and cash reinvestment assumptions. The $48.53 committee DCF models EBIT margin expanding aggressively to 12.0% with terminal value accounting for 76% of enterprise value. The $30.19 pro-forma model is more conservative: it holds SG&A at 77% of gross profit, deducts annual debt repayments of $500M, and fully models the working capital cash drag of inventory builds."*

### 3. Sensitivity & Interpretation Question
* **Reviewer's Question:** *"Over your tested ranges, why does CapEx produce a larger value span ($4.81/sh) than Gross Margin ($2.14/sh), and does that mean management should prioritize capital cuts over brand marketing?"*
* **Presenter's Answer:** *"CapEx leads the numerical value span over this tested range because capital spending flows dollar-for-dollar out of cash flow, whereas gross margin gains are ~77% absorbed by variable SG&A and taxed at 20.3%. However, this does not mean management should starve capital: Nike's capex is already lean at 1.5% of sales. The strategic imperative remains brand health and gross margin realization."*

### 4. Live Calculation & Evidence Audit
Presenter and reviewer audited the higher gross margin run (+1.0 pp) together:
* **Calculation Walk:** At 45.50% terminal gross margin on $55,902.3M revenue, gross profit expands by $+\$559.0\text{M}$. Variable SG&A absorbs $77.0\% \times \$559.0\text{M} = +\$430.4\text{M}$, increasing EBIT by $+\$128.6\text{M}$. After 20.3% taxes ($+\$26.1\text{M}$) and inventory working capital adjustment ($+\$4.6\text{M}$ due to lower COGS), final-year FCFE increases by exactly:
  $$\Delta\text{FCFE} = 3,091.6 - 2,984.5 = \mathbf{+\$107.1\text{M}}$$
* **Audit Result:** The calculation walked through the linked statements with 100% precision. Independent variables (tax rate, debt repayment, capex) remained strictly at base values.

---

## 4. E — Explain-Back, Actionable Feedback & Disposition

### 1. Reviewer's Explain-Back
* **Supported Valuation Conclusion:** The presenter supports a **Watch/Defer** posture at current trading levels ($38.24), waiting for either price compression toward the $36.40 margin-of-safety trigger or empirical proof of turnaround in upcoming 10-Q filings.
* **Primary Operating Driver:** **Revenue / Sales Growth** is the dominant driver of top-line operating profit scale ($531.3M EBIT span), while **CapEx % of revenue** and **Gross Margin** dominate cash flow and equity value due to working capital flow-through mechanics.
* **Primary Limitation:** The analysis is heavily reliant on the management "Win Now" turnaround thesis. If promotional discounting in North America persists or Greater China comps decline further, operating margins will remain stuck near the 42.8% trough.

### 2. Reviewer's Actionable Feedback
* **Evidence-Backed Strength:** Outstanding accounting rigor and statement linkage. Modeling Demand Creation explicitly within SG&A and declaring Floor Plan as "none" appropriately customizes the engine to Nike's business model.
* **Specific Improvement for Next Iteration:** In the pro-forma engine, variable SG&A is currently linked as a flat percentage of gross profit (77%–80%). Decoupling fixed administrative overhead from variable demand creation marketing would provide a more realistic operating leverage curve during rapid sales recoveries.

### 3. Post-Review Disposition: Keep, Revise, Investigate
* **What to KEEP:**
  * Keep the 5-year balanced pro-forma three-statement architecture and Python standard-library engine.
  * Keep the $1,085M net cash balance sheet bridge and the 15.47% D&A on opening PP&E schedule.
  * Keep the Watch/Defer posture and the $36.40 re-entry price trigger.
* **What to REVISE:**
  * Refine the SG&A forecasting module in `proforma_nke.py` to separate fixed operating overhead ($11.3B baseline) from variable demand creation (modeled at ~10% of sales).
* **What to INVESTIGATE:**
  * Prioritize researching subsequent Form 10-Q quarterly reports to monitor:
    1. North America wholesale order book backlog.
    2. Nike Direct digital markdown accruals.
    3. Currency-neutral revenue trajectories across Greater China.

---

## 5. Review Performed on Partner's Company

* **Partner's Target Company:** Automotive / Dealership Target (Asbury Automotive Group / ABG).
* **Questions Asked:**
  1. *Selection/Evidence:* "Which 10-K footnote provides the $2,027.0M Floor Plan Notes balance, and why is it treated as operating working capital rather than capital structure debt?"
  2. *Valuation:* "Why does your terminal value account for 79.8% of total equity value, and how sensitive is that proportion to your 10.0% cost of equity?"
  3. *Sensitivity:* "When you shocked floor plan interest rates by +100 bps, why did FCFE drop by $20M while operating profit remained completely unchanged?"
* **Audit Result:** Partner successfully traced the floor plan interest walk through pretax income and verified that floor plan interest sits below EBIT, confirming statement integrity.
* **Feedback Given:** Commended partner's floor plan modeling; recommended stress-testing used vehicle gross profit margins under credit contraction scenarios.

---

## 6. Reflect

1. **Which question made you reconsider something?**  
   My partner's question regarding whether CapEx dominating the value span meant management should prioritize capital cuts over marketing made me reconsider how financial model sensitivity compares to strategic reality. In a mathematical model, capex cuts flow dollar-for-dollar into cash, but in the real world, starving digital supply chain automation would destroy brand delivery speed and long-term customer retention.
2. **What do you now understand better about your own company?**  
   I now understand that Nike's biggest operational vulnerability is **gross margin dilution through promotional discounting**. Because Nike carries high fixed demand creation commitments ($4.75B/yr), a 100 bps drop in gross margin cannot easily be offset by cutting operating overhead without damaging brand prestige.

---

## 7. Artifact and Script Registry

| Deliverable Name | Repository Path | Description |
|---|---|---|
| **Lab 12 Presentation Report (Date-Ticker)** | [`presentation_1001_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/presentation_1001_NKE.md) | Authoritative Lab 12 submission report containing the 6-stop presentation route and peer review audit. |
| **Lab 12 Presentation Report (Standard)** | [`Lab_12.md`](file:///Users/wgdeary/FIN439%20work%20folder/Lab_12.md) | Synced Lab 12 checkout report. |
| **Pro-Forma Base Engine (Lab 10)** | [`proforma_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_nke.py) · [`proforma_0924_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/proforma_0924_NKE.md) | 5-year balanced pro-forma foundation. |
| **Sensitivity Engine (Lab 11)** | [`sensitivity_nke.py`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_nke.py) · [`sensitivity_0929_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/sensitivity_0929_NKE.md) | One-at-a-time sensitivity suite across Revenue Growth, Gross Margin, and CapEx. |
| **Reverse DCF (Lab 06)** | [`reverse_dcf_0910_NKE.md`](file:///Users/wgdeary/FIN439%20work%20folder/reverse_dcf_0910_NKE.md) | Reverse DCF market-implied growth analysis. |
| **GitHub Target Repository** | [`WGdearY/TICKER-research`](https://github.com/WGdearY/TICKER-research) | Main remote submission repository. |
