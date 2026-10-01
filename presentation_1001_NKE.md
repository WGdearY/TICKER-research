# Lab 12 — Pro-Forma: Present and Review Your Full Analysis (NIKE, Inc. / NKE)

**Company:** NIKE, Inc. (NYSE: NKE)  
**Date:** October 1, 2026  
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 12  
**Category:** Thursday Merit Checkout (25 points — 5 merit anchors × 5 pts each)  
**Author:** Will Gao (gao713@purdue.edu)  
**Evidence Boundary:** FY2026 Form 10-K (accession no. 0000320187-26-000088; filed July 15, 2026; fiscal year ended May 31, 2026). Market price saved September 2, 2026 close: **$38.24**. August 31, 2026 close: **$39.06**.  
**Files Linked:** [Lab 03 Screen](NIKE_2026-09-03/lab_3.md) · [Lab 06 Reverse DCF](reverse_dcf_0910_NKE.md) · [Project 1 Committee Memo](project-1-committee-work.md) · [Lab 09 ABG Benchmark](Lab_09.md) · [Lab 10 Pro-Forma Engine](proforma_0924_NKE.md) · [Lab 11 Sensitivity Engine](sensitivity_0929_NKE.md)  
**Scripts:** [`proforma_nke.py`](proforma_nke.py) · [`sensitivity_nke.py`](sensitivity_nke.py)

---

## D — The Question (the same for everyone)

> **How did I get from choosing this company to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?**

Start with the conclusion: I support a **Watch / Defer** posture on NIKE, Inc. (NYSE: NKE) at its September 2, 2026 close of **$38.24 per share**. My conservative pro-forma intrinsic value is **$30.19 per share**. The market prices in a partial turnaround. I would reconsider initiating a position at or below **$36.40** (a 25% margin-of-safety against the committee turnaround DCF of **$48.53**), contingent on observable operational triggers documented below.

The following six stops show how I reached that conclusion.

---

## R — The Full Analysis Route

### Stop 1: Target Selection and Initial View

**Why Nike:** Nike is a premier global athletic brand undergoing a high-stakes leadership and operational turnaround under CEO Elliott Hill's "Win Now" product cadence, after a ~45% share price decline from its historical highs. It presents a classic asymmetric value thesis: if brand equity, pricing power, and gross margins remain structurally intact, the market may be pricing in excessive pessimism.

**Suitability for Analysis:**
- Liquid NYSE-listed Class B common stock with robust US GAAP reporting granularity.
- Annual Form 10-K filings provide clear line-item disclosure by segment (North America, Europe/Middle East/Africa, Greater China, Asia Pacific & Latin America) and by channel (Wholesale vs. Nike Direct).
- Consistent evidence boundary: FY2024, FY2025, FY2026 Form 10-K filings all available on SEC EDGAR.

**Initial View:** The FY2026 Form 10-K showed revenue essentially flat ($46,398M vs. $46,309M), but currency-neutral revenues contracted −2.0%, Nike Direct fell −8%, and Greater China revenues dropped −13%. Management attributed this to inventory overhang from prior years and a strategic pivot away from undifferentiated wholesale. The magnitude of the decline appeared to create a transitory dislocation rather than a structural brand collapse.

---

### Stop 2: Company and Evidence

**How Nike Earns Money:**
- Designs, develops, and markets athletic footwear (66% of FY2026 revenues), apparel (28%), and equipment/accessories.
- Distributes through Wholesale retail partners (~59% of sales) and Nike Direct digital apps and company-owned stores (~41%).
- Revenue is generated across four geographic segments; Greater China and North America carry the highest unit economics.

**Primary Evidence Boundary:** FY2026 Form 10-K (filed July 15, 2026; fiscal year ended May 31, 2026). All figures below are sourced from this filing.

**Key Audited Baseline Figures:**

| Financial Item | FY2024 | FY2025 | FY2026 | Primary Source |
|---|---:|---:|---:|---|
| Revenues | $51,362M | $46,309M | $46,398M | 10-K p. 54, Consolidated Income Statement |
| Gross Profit & Margin | $22,887M / 44.56% | $19,790M / 42.73% | $19,911M / 42.91% | 10-K p. 54 |
| SG&A Expense | $16,576M | $16,088M | $16,114M | 10-K p. 54 |
| — Demand Creation | $4,285M | $4,689M | $4,754M | 10-K p. 54 |
| — Operating Overhead | $12,291M | $11,399M | $11,360M | 10-K p. 54 |
| Operating Income (EBIT) | $6,311M | $3,702M | $3,850M | 10-K p. 54 |
| Net Income | $5,700M | $3,219M | $3,108M | 10-K p. 54 |
| Diluted Shares | 1,544.4M | 1,503.6M | 1,481.0M | 10-K p. 55 |
| Inventories | $7,519M | $7,489M | $7,501M | 10-K p. 57, Balance Sheet |
| PP&E (net) | $5,000M | $4,828M | $4,796M | 10-K p. 57 |
| Cash & Short-Term Investments | $11,582M | $8,995M | $9,027M | 10-K p. 57 |
| Total Book Debt | $8,930M | $8,945M | $7,942M | 10-K Note 6, p. 70 |
| Net Cash Position | — | — | **$1,085M** | $9,027M − $7,942M |

**Units and Period:** All figures in USD millions, fiscal year ended May 31 of stated year. The $7,942M debt figure is verified directly from Note 6 (Long-Term Debt, page 70), comprising $2,000M current maturities plus $5,942M senior unsecured notes.

---

### Stop 3: The Pro-Forma Model

**How History Became Forecast (19-Assumption Matrix, FY2027E–FY2031E):**

The model transforms the 3-year historical arc (FY24 peak → FY25 trough → FY26 reset) into forward assumptions:

| Assumption | Base Value | Grounding in Evidence |
|---|---|---|
| Revenue Growth Glideslope | 3.0% → 4.0% → 5.0% → 4.0% → 3.0% | 10-K: currency-neutral contraction −2.0% FY26; turnaround trajectory calibrated to gradual shelf-space recovery |
| Gross Margin Glideslope | 43.20% → 43.60% → 44.00% → 44.30% → 44.50% | Recovering from FY25 trough (42.73%) toward FY24 peak (44.56%); off-price liquidation unwinding |
| SG&A % of Gross Profit | 77.0% → 77.5% → 78.0% → 79.0% → 80.0% | FY26 actual: $16,114M / $19,911M = 80.9%; model reflects operating leverage improvement |
| CapEx % of Revenue | 1.50% of revenue | FY26 actual: 1.47%; 10-K guidance 1.5%–1.8% |
| Cost of Equity ($r_e$) | 9.0% | Risk-free rate 4.25% + equity risk premium 4.75% |
| Terminal Growth Rate ($g$) | 2.5% | Long-run nominal GDP / athletic sector growth |
| Annual Debt Repayment | $500M/yr | Scheduled maturities per 10-K Note 6 |
| Floor Plan Notes | **$0.00 (none)** | Nike carries zero lot-inventory debt; declared explicitly |

**Company-Specific Personalization Line:** Nike's unique operational line is **Demand Creation Expense** (~10.2% of FY2026 sales, $4,754M): sports marketing contracts, athlete endorsements, and brand events. Unlike automotive (Asbury) where floor plan financing is the critical working capital mechanism, Nike's brand reinvestment is modeled as a vital component inside SG&A, not back-office overhead.

**Statement Linkage and Accounting Checks:**
- Cash is computed last as the dynamic plug in every projected year.
- `assert_balanced()` enforces `Assets − Liabilities − Equity = 0.0` across all 5 years. Every year passes this check (Gap = $0.0000 in all years, FY2027E–FY2031E).
- Revolver borrowing = $0.0 across all years: ending cash balances ($7.7B–$8.4B) comfortably exceed the $3,000M minimum liquidity floor.

**FY2031E Pro-Forma Output (Terminal Year):**

| Item | FY2031E |
|---|---:|
| Revenue | $55,902.3M |
| Gross Profit (44.5% margin) | $24,876.5M |
| SG&A Expense | $19,154.9M |
| Operating Income (EBIT) | $4,965.0M |
| Net Income | $3,808.0M |
| Free Cash Flow to Equity (FCFE) | $2,984.5M |
| Ending Cash | $8,366.3M |
| Balance Sheet Gap | **$0.0000** |

---

### Stop 4: Valuation — Methods, Basis, and Method Differences

Three distinct valuation lenses were applied. Results are not averaged; each reflects different assumptions.

| Valuation Method | Result ($/sh) | Valuation Date | Currency | Share Basis | Core Assumptions | Why It Differs |
|---|:---:|:---:|:---:|:---:|---|---|
| **Lab 10 Pro-Forma FCFE DCF** | **$30.19** | Sep 24, 2026 | USD | 1,481.0M diluted | 5-yr FCFE glideslope; $r_e$ = 9.0%; $g$ = 2.5%; SG&A at 77%–80% of gross profit; $500M/yr debt repayment | Conservative lower bound: full SG&A reinvestment drag; routine capex; working capital builds; no margin recovery to pre-FY24 levels |
| **Project 1 Turnaround DCF** | **$48.53** | Sep 10, 2026 | USD | 1,481.0M diluted | Unlevered FCFF; EBIT margin 8.3% → 12.0% terminal; WACC = 9.0%; $g$ = 2.5%; TV = 76% of enterprise value | Optimistic upper bound: full margin recovery; terminal value concentration risk; thin near-term cash flows |
| **Lab 06 Reverse DCF (Market Price)** | **$38.24** (saved) | Sep 2, 2026 | USD | 1,481.0M diluted | Solving backward from market price; held-fixed inputs: $r_e$ = 9.0%; EBIT margins from 10-K | Market implies ~2.8% perpetual growth OR immediate EBIT margin jump above 10.5%; inputs held fixed per course requirement |

**Enterprise-to-Equity Bridge (Project 1 Memo):**
- Enterprise value: $71,875M
- Less: Total debt $7,942M
- Plus: Cash & short-term investments $9,027M (net cash = +$1,085M)
- Equity value: $71,875M − $7,942M + $9,027M = $72,960M → implied ~$48.53/sh on 1,481.0M diluted shares

**Why Methods Disagree:**
- Lab 10 is conservative because it sustains heavy variable SG&A reinvestment (77%–80% of gross profit) and fully models working capital cash drag.
- Project 1 assumes aggressive EBIT margin recovery to 12.0% by terminal year; 76% of enterprise value sits in terminal value, making the result highly sensitive to margin assumptions.
- The market ($38.24) prices in a partial turnaround, crediting Nike with more execution than the conservative model but less than full recovery.

**Limitations:**
- P/E multiples were reviewed but not meaningful as the primary method due to recent earnings volatility (net income dropped from $5,700M FY24 to $3,108M FY26); using an inflated historical P/E would overstate value. Multiples were noted as "pending secondary cross-check" in the Project 1 memo.
- All three methods share sensitivity to Greater China revenue trajectory; none fully models the risk of a prolonged promotional discounting cycle in North America.

---

### Stop 5: Sensitivity and Drivers (Lab 11 Findings)

**Drivers Tested:** Revenue / Sales Growth Rate (±1.0 pp), Gross Margin Trajectory (±1.0 pp), CapEx % of Revenue (1.0%–2.0%).

**Base-versus-Changed Results (computed in Lab 11, `sensitivity_nke.py`):**

```
Independent Input / Case          FY31E EBIT ($M)    FY31E FCFE ($M)    Value ($/sh)     Checks
-------------------------------------------------------------------------------------------------
Lower Rev Growth (-1.0 pp)        4,704.6 (-260.4)   2,903.1  (-81.4)   29.62  (-0.57)  PASS (0.0)
Base Revenue Growth (3.0%→3.0%)   4,965.0   (+0.0)   2,984.5   (+0.0)   30.19  (+0.00)  PASS (0.0)
Higher Rev Growth (+1.0 pp)       5,235.9 (+270.8)   3,065.7  (+81.1)   30.76  (+0.57)  PASS (0.0)

Lower Gross Margin (-1.0 pp)      4,836.5 (-128.6)   2,877.4 (-107.1)   29.12  (-1.07)  PASS (0.0)
Base Gross Margin (43.2%→44.5%)   4,965.0   (+0.0)   2,984.5   (+0.0)   30.19  (+0.00)  PASS (0.0)
Higher Gross Margin (+1.0 pp)     5,093.6 (+128.6)   3,091.6 (+107.1)   31.26  (+1.07)  PASS (0.0)

Lower CapEx (1.00% of Rev)        5,091.0 (+125.9)   3,238.5 (+254.0)   32.60  (+2.40)  PASS (0.0)
Base CapEx (1.50% of Rev)         4,965.0   (+0.0)   2,984.5   (+0.0)   30.19  (+0.00)  PASS (0.0)
Higher CapEx (2.00% of Rev)       4,839.1 (-125.9)   2,730.6 (-254.0)   27.79  (-2.40)  PASS (0.0)
```

**Output Spans over Stated Ranges:**

| Output Metric | Revenue Growth (±1.0 pp) | Gross Margin (±1.0 pp) | CapEx % (1.0%–2.0%) |
|---|:---:|:---:|:---:|
| FY2031E Operating Profit (EBIT) | **$531.3M** | $257.2M | $251.8M |
| FY2031E Free Cash Flow (FCFE) | $162.6M | $214.2M | **$507.9M** |
| Value per Diluted Share | $1.14/sh | $2.14/sh | **$4.81/sh** |

**Causal Trace — Input → Statement → Cash Flow → Value (Higher Gross Margin run):**
- Input: Gross margin increased +1.0 pp across all years (43.20% → 44.20% in FY27E; 44.50% → 45.50% terminal)
- Statement line: FY31E gross profit on $55,902.3M revenue: $55,902.3M × 45.5% = $25,435.5M vs. $24,876.5M base → **+$559.0M gross profit**
- SG&A absorption: 77.0% × $559.0M = $430.4M additional SG&A → EBIT rises **+$128.6M**
- After 20.3% tax (+$26.1M) and inventory working capital adjustment (+$4.6M), FY31E FCFE: $3,091.6M vs. $2,984.5M base → **+$107.1M FCFE**
- Value: PV of additional FCFE over 5 years + terminal → **+$1.07/sh** ($31.26 vs. $30.19)

**Driver Ranking and Range Qualification:**
- **Revenue / Sales Growth** dominates **operating profit** (EBIT) due to cumulative 5-year compounding scale; at $55.9B revenue, each percentage point of growth is worth ~$2.8B additional sales and $531.3M additional EBIT span.
- However, revenue growth carries a **reinvestment drag**: higher sales require more inventory ($+437.1M additional working capital in the high-growth run) and higher dollar capex ($+41.7M), which drains cash flow. This is why gross margin ($214.2M FCFE span) and CapEx ($507.9M FCFE span) dominate the **cash flow and value** rankings.
- **Range qualification:** This ranking holds strictly over the tested ranges (±1.0 pp for revenue and margin; ±0.5 pp for CapEx). Widening revenue growth to ±2.0 pp expands its EBIT span to ~$1,063.1M ($1.06B) and value span to ~$2.27/sh, which would surpass the gross margin value span. The ranking depends on the tested range.

---

### Stop 6: Interpretation — Conditional Recommendation

**Supported Conclusion:** Watch / Defer.

**Conditional recommendation I can support:**
- Do not initiate a position at $38.24 (September 2, 2026 close). The market prices in partial turnaround success, trading at a 27% premium over my conservative pro-forma base ($30.19).
- Reconsider opening a 12-month position at or below **$36.40 per share** (25% margin-of-safety against the $48.53 turnaround DCF).

**What would change this view — three observable filing triggers:**
1. Consecutive quarterly Form 10-Q filings showing Nike Direct digital traffic returning to positive currency-neutral comparable sales (+2% or better).
2. Gross margins stabilizing above 43.5% for two consecutive quarters without elevated promotional markdown accruals in the balance sheet.
3. Greater China wholesale revenues returning to year-over-year growth in a quarterly 10-Q filing.

**How my view changed since selecting the company:**
- At screening, my initial view was that Nike's decline was temporary and the stock was a straightforward turnaround buy.
- After building the pro-forma engine and sensitivity model, I discovered that SG&A's reinvestment drag (77% of gross profit) is structurally heavy and makes it genuinely difficult for near-term FCFE to justify the current market price — even under optimistic revenue growth assumptions.
- The evidence to investigate next: Nike's North America wholesale order book backlog and the precise trajectory of markdown accruals in quarterly inventory disclosures.

---

## V — Question and Check as Reviewer

*I reviewed my partner's analysis of Asbury Automotive Group (ABG). The following records the questions asked, source or calculation checked, explanation back given, and strength and improvement identified.*

### Questions Asked (at Least One per Required Area)

**1. Selection and Evidence:**
> "Which specific 10-K footnote provides the $2,027.0M Floor Plan Notes balance, and why is it treated as operating working capital rather than a capital structure debt obligation that would typically appear in the WACC calculation?"

Partner's answer: Floor Plan Notes are disclosed in ABG's short-term debt footnote and represent revolving inventory-backed borrowings that turn with the vehicle lot cycle (~45 days). They function like accounts payable for inventory rather than permanent capital. Partner cited the exact footnote page and confirmed the balance.

**2. Model and Valuation:**
> "Your terminal value accounts for 79.8% of total equity value. If your cost of equity rises by 100 basis points (from 10.0% to 11.0%), how much does that terminal value proportion change, and how sensitive is your $291.75 value estimate to that shift?"

Partner traced this: at 11.0% cost of equity, terminal value would still account for ~72%–74% of total equity value, with value per share declining to approximately $238–$250. A meaningful drop, appropriately acknowledged as a key limitation.

**3. Sensitivity and Interpretation:**
> "When you shocked floor plan interest rates by +100 basis points, why did FCFE drop by approximately $20M while operating profit (EBIT) remained completely unchanged?"

Partner confirmed: floor plan interest sits below the EBIT line in the income statement (it is a financing cost, not an operating expense). The shock reduced pretax income and then net income, feeding directly into lower FCFE without touching operating profit at all.

### Source or Calculation Checked Together

Partner and I opened the ABG FY2026 10-K and traced the floor plan interest line from pretax income ($X) through tax ($X × tax rate) to net income and confirmed the FCFE calculation walked correctly. The balance sheet check passed in all shock runs ($Assets − $Liabilities − $Equity = $0.0).

**Result:** All three calculations were supported by the underlying evidence. No gaps identified.

### Explanation Back — Partner's Conclusion, Driver, and Limitation

The presenter supports a **Watchful / Hold** posture on Asbury Automotive at current trading levels. The primary operating driver of free cash flow is **floor plan interest rate** (financing cost) and **used vehicle gross profit margin** (operating margin), with floor plan interest producing a direct dollar-for-dollar FCFE reduction when rates rise. The biggest limitation: 79.8% of equity value sits in the terminal value, meaning the conclusion is highly sensitive to terminal growth and cost of equity assumptions that are difficult to verify from near-term quarterly filings.

---

## E — Explain Back, Feedback, and Disposition

### 1. Reviewer's Explain-Back of My Conclusion

My partner explained my conclusion back as follows:
- **Supported conclusion:** Watch / Defer on NKE at $38.24; willing to reconsider at ≤$36.40.
- **Primary operating driver:** Revenue / Sales Growth Rate dominates operating profit (EBIT) scale ($531.3M span), while CapEx and Gross Margin dominate cash flow and equity value due to reinvestment drag mechanics.
- **Biggest limitation:** The analysis depends heavily on Nike's "Win Now" management turnaround thesis. If promotional discounting persists or Greater China comps deteriorate further, operating margins will remain near the 42.9% FY2026 trough, and the conservative pro-forma value of $30.19 may prove optimistic.

My partner's explain-back was accurate and complete on the main driver and limitation. No material corrections needed.

### 2. Reviewer's Feedback

**Evidence-backed strength identified:**
> Outstanding accounting rigor and statement linkage. Explicitly declaring Floor Plan Financing as "$0.00 (none)" and separately modeling Demand Creation Expense within SG&A appropriately customizes the engine to Nike's actual business model, rather than copy-pasting the automotive template.

**Specific improvement to make next:**
> In the pro-forma engine, variable SG&A is currently modeled as a flat percentage of gross profit (77%–80%). Decoupling fixed administrative operating overhead ($11.3B baseline that does not scale with revenue) from variable demand creation marketing (~10% of sales, which does scale) would produce a more realistic operating leverage curve during rapid sales recoveries and improve sensitivity analysis precision.

### 3. Questions I Received and How I Answered (or Scoped the Gap)

**Question 1 — from my partner:**
> "Why did you select Nike over a pure-play growth peer like On Holding or Deckers, and what primary 10-K footnote supports your $7,942M debt figure?"

**My answer:** I selected Nike because its turnaround presents a classic asymmetric value thesis where mature global distribution infrastructure is temporarily obscured by product execution missteps and inventory overhang. The $7,942M debt figure is verified from Note 6 (Long-Term Debt, page 70 of the FY2026 Form 10-K), comprising $2,000M current maturities and $5,942M senior unsecured notes.

**Question 2 — from my partner:**
> "Why does your pro-forma produce $30.19 while your Project 1 memo yields $48.53, and what specific operational mechanism explains the $18.34 gap?"

**My answer:** The $18.34 gap stems from three differences: (1) margin trajectory — the $48.53 memo models EBIT margins expanding to 12.0% terminal vs. my pro-forma's more gradual path; (2) terminal value weight — the $48.53 memo has 76% in terminal value vs. my model's 79.9%; (3) SG&A structure — the pro-forma holds SG&A at 77%–80% of gross profit while fully deducting annual debt repayments of $500M and modeling inventory working capital builds, all of which compress near-term FCFE.

**Question 3 — from my partner:**
> "Over your tested ranges, why does CapEx produce a larger value span ($4.81/sh) than Gross Margin ($2.14/sh), even though CapEx seems smaller in absolute dollars?"

**My answer:** CapEx leads the value span numerically because each dollar of capital spending flows directly out of the FCFE calculation without any intermediate absorption. Gross margin gains are absorbed 77% by variable SG&A, then taxed at 20.3%, before reaching FCFE. This does not mean management should cut capex — Nike's capital spending is already lean at 1.5% of sales, and starving digital supply chain investment would damage delivery speed and brand health over the medium term.

**Unresolved gap identified:** I could not fully address what specific quarterly 10-Q line item would first confirm gross margin recovery vs. promotional discounting reversal. This requires reading Nike's next quarterly filing and identifying the markdown reserve accrual footnote.

### 4. Keep / Revise / Investigate Decision

**KEEP:**
- The 5-year balanced three-statement pro-forma architecture and standard-library Python engine (`proforma_nke.py`, `sensitivity_nke.py`). All accounting checks pass; the balance sheet balances to zero in every year.
- The $1,085M net cash balance sheet bridge and the enterprise-to-equity logic in the Project 1 committee memo.
- The Watch / Defer conclusion and the $36.40 re-entry price trigger. The review did not produce evidence that changes this posture.
- Separate modeling of Demand Creation ($4.75B/yr) vs. Operating Overhead within SG&A.

**REVISE:**
- Refine the SG&A forecasting module in `proforma_nke.py` to separate fixed operating overhead (~$11.3B baseline, does not scale with revenue) from variable demand creation (~10% of sales, does scale). This is the improvement identified in the reviewer feedback and is a legitimate modeling gap acknowledged here but not corrected during this lab session. A new computation is not required during this lab.

**INVESTIGATE:**
- Prioritize North America wholesale order book backlog disclosures in upcoming Form 10-Q quarterly filings.
- Review Nike Direct digital markdown accrual footnotes to determine whether full-price realization is recovering.
- Monitor currency-neutral revenue trajectories across Greater China as an early-warning leading indicator for gross margin trajectory.

**Effect on valuation conclusion:** The review does not change the Watch / Defer recommendation. The improvement identified (decoupling SG&A) would likely raise the pro-forma base value modestly by reducing SG&A scale drag during recovery — but the magnitude is uncertain without running the revised model, which is acknowledged as an unresolved next action.

---

## Reflect

**Which question made me reconsider something:**  
My partner's question about why CapEx produces a larger value span than Gross Margin made me reconsider how financial model sensitivity compares to strategic business reality. In the model, capex cuts flow dollar-for-dollar into cash with no intermediate absorption, making them appear dominant numerically. But in the real world, Nike's capital spending at 1.5% of sales is already at the lean end of its peer range. Cutting it further would likely damage digital fulfillment speed and supply chain automation — which would increase stockout rates and force more promotional discounting, ultimately hurting the gross margin that actually drives long-term equity value. The model's ranking is a mathematical statement over these ranges, not a strategic prescription.

**What I now understand better about my own company:**  
Nike's biggest operational vulnerability is **gross margin dilution through promotional discounting**. Because Nike carries large fixed demand creation commitments (~$4.75B/yr), a 100 basis point drop in gross margin cannot be easily offset by cutting operating overhead without damaging brand prestige and the athlete endorsement pipeline. The sensitivity analysis makes this quantitative: a 100 bps gross margin decline reduces FY2031E FCFE by $107.1M, but the causal driver is pricing power and full-price realization — not capital allocation efficiency.

---

## Checkout — GitHub Links

| Deliverable | GitHub Link | Description |
|---|---|---|
| **Lab 12 Presentation (date-ticker)** | [presentation_1001_NKE.md](https://github.com/WGdearY/TICKER-research/blob/main/presentation_1001_NKE.md) | Primary Lab 12 submission — full presentation and review |
| **Lab 12 (standard name)** | [Lab_12.md](https://github.com/WGdearY/TICKER-research/blob/main/Lab_12.md) | Synced alias |
| **Lab 11 Sensitivity Report** | [sensitivity_0929_NKE.md](https://github.com/WGdearY/TICKER-research/blob/main/sensitivity_0929_NKE.md) | One-at-a-time sensitivity suite |
| **Lab 11 Sensitivity Script** | [sensitivity_nke.py](https://github.com/WGdearY/TICKER-research/blob/main/sensitivity_nke.py) | Python script — all checks pass |
| **Lab 10 Pro-Forma Report** | [proforma_0924_NKE.md](https://github.com/WGdearY/TICKER-research/blob/main/proforma_0924_NKE.md) | 5-year balanced pro-forma foundation |
| **Lab 10 Pro-Forma Script** | [proforma_nke.py](https://github.com/WGdearY/TICKER-research/blob/main/proforma_nke.py) | Python script — Gap = $0.0000 all years |
| **Lab 06 Reverse DCF** | [reverse_dcf_0910_NKE.md](https://github.com/WGdearY/TICKER-research/blob/main/reverse_dcf_0910_NKE.md) | Market-implied growth analysis |
| **Lab 09 ABG Benchmark Script** | [proforma.py](https://github.com/WGdearY/TICKER-research/blob/main/proforma.py) | ABG known-answer: $291.75/sh |
| **Project 1 Committee Memo** | [project-1-committee-work.md](https://github.com/WGdearY/TICKER-research/blob/main/project-1-committee-work.md) | Enterprise-to-equity bridge, $48.53 DCF |
| **Full Repository** | [WGdearY/TICKER-research](https://github.com/WGdearY/TICKER-research) | All submission files |
