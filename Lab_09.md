# Lab 09 — Pro-Forma Build: The Engine and the Known Answer
**Company / Case:** Asbury Automotive Group (NYSE: ABG)  
**Date:** September 22, 2026  
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 09  
**Author:** Will Gao (gao713@purdue.edu)  
**File Artifacts:** [`proforma.py`](proforma.py) · [GitHub Repository](https://github.com/WGdearY/TICKER-research)

---

## 1. D — The Question & Core Valuation Judgments

> **"What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?"**

### The Three Judgments that Carry the ABG Valuation
1. **Organic Revenue Growth (1.8% per year):** Reflects a mature automotive dealership market matching long-term vehicle replacement rates and modest inflation, excluding inorganic M&A.
2. **Gross Margin (17.05%):** Anchored to post-pandemic dealership normalization across new, used, F&I, and parts/service operations.
3. **SG&A ÷ Gross Profit Operating Leverage Fade (66.5% in 2026 → 64.5% in 2028–2030):** Represents 200 bps of structural cost discipline and operating leverage as administrative costs scale slower than gross profit.

### Why Cash is the Last Line the Model Computes
Cash cannot be predicted as an independent percentage of revenue. In a coherent three-statement model, **cash is the final reconciliation plug** resulting from:
* Operating earnings (Net Income + non-cash D&A + impairment)
* Reinvestment needs (Capex, changes in inventory, other operating working capital)
* Debt financing dynamics (Floor plan loan draws, contractual term debt repayments)
* Shareholder distributions (Discretionary share buybacks)

If cash were forecasted independently or held arbitrarily constant, the balance sheet would not balance, signaling that the statements have disconnected from underlying cash flows.

---

## 2. R — The Assumption Set and Opening Balance Sheet

### Opening Balance Sheet (FY2025 in USD Millions)
* **Assets:** Cash: `$40.4` · Inventory: `$2,135.8` · PP&E (net): `$3,070.4` · Other Assets: `$6,371.6`  
  * **Total Assets:** **`$11,618.2M`**
* **Liabilities & Equity:** Floor Plan Notes: `$2,027.0` · Term Debt: `$3,572.0` · Revolver: `$0.0` · Other Liabilities: `$2,127.5` · Equity: `$3,891.7`  
  * **Total Liabilities & Equity:** **`$11,618.2M`**
* **Historical Revenue:** `$17,999.0M`

### The 15 Labeled Assumptions

| Assumption | ABG Value | Label | Economic Rationale |
|---|---|---|---|
| Organic revenue growth | 1.8% a year | `judgment` | Mature volume growth matching population and GDP |
| Gross margin | 17.05% | `judgment` | Dealership composite margin across vehicle and service sales |
| SG&A ÷ gross profit | 66.5% (2026), 65.5% (2027), 64.5% (2028–2030) | `judgment` | Fixed-cost dilution and technology operating leverage |
| Depreciation ÷ opening PP&E | 82.4 ÷ 3,070.4 (~2.68%) | `history` | FY2025 actual depreciation rate on physical assets |
| Non-cash impairment | $120M / year | `judgment` | Franchise right and goodwill amortization/impairment |
| Capital expenditures (Capex) | $250M / year | `guidance` | Management guidance for dealership facility updates |
| Tax rate | 25.5% | `judgment` | Blended statutory Federal and state corporate tax rate |
| Inventory days | 2,135.8 ÷ (17,999.0 − 3,071.7) × 365 (~52.23 days) | `history` | FY2025 days-sales-in-inventory across vehicle lots |
| Floor plan loans ÷ inventory | 2,027.0 ÷ 2,135.8 (~94.91%) | `history` | FY2025 manufacturer financing penetration rate |
| Other working capital | 0.8% of change in revenue | `judgment` | Incremental receivables and payables from sales growth |
| Minimum cash / Revolver limit / Rate | $25M / $850M / 6.0% | `history/judgment` | Operating liquidity buffer and credit facility terms |
| Debt repayment / Share buyback | $150M / $150M a year | `judgment` | Balanced capital allocation: deleveraging and buybacks |
| Interest rates: Floor plan / Term debt | 4.67% / 5.44% | `history` | FY2025 weighted-average effective borrowing costs |
| Cost of equity / Terminal growth | 10.0% / 2.5% | `judgment` | Equity discount rate and long-run sustainable GDP growth |
| Diluted common shares | 17.951349 million | `fact` | Form 10-Q (June 30, 2026) diluted share count |

---

## 3. I & V — The Three Statements, Checks, and Known-Answer Proof

The model implemented in [`proforma.py`](proforma.py) produces the following audited statements:

### 1. Income Statement (USD Millions)
| Line Item | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---:|---:|---:|---:|---:|
| **Revenue** | **18,323.0** | 18,652.8 | 18,988.5 | 19,330.3 | **19,678.3** |
| Gross Profit | 3,124.1 | 3,180.3 | 3,237.5 | 3,295.8 | 3,355.1 |
| SG&A Expense | 2,077.5 | 2,083.1 | 2,088.2 | 2,125.8 | 2,164.1 |
| Depreciation | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| Impairment (non-cash) | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| **Operating Income (EBIT)** | **844.2** | 890.3 | 938.1 | 954.5 | **971.4** |
| Interest Expense | 289.0 | 282.5 | 276.1 | 269.7 | 263.4 |
| Pretax Income | 555.2 | 607.8 | 661.9 | 684.8 | 708.0 |
| Income Tax (25.5%) | 141.6 | 155.0 | 168.8 | 174.6 | 180.5 |
| **Net Income** | **413.6** | 452.8 | 493.1 | 510.1 | **527.5** |

### 2. Balance Sheet (USD Millions)
| Line Item | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---:|---:|---:|---:|---:|
| **Cash & Equivalents** | **101.8** | 206.9 | 356.6 | 527.5 | **719.8** |
| Inventory | 2,174.7 | 2,213.8 | 2,253.7 | 2,294.2 | 2,335.5 |
| PP&E (net) | 3,238.0 | 3,401.1 | 3,559.8 | 3,714.3 | 3,864.6 |
| Other Assets | 6,254.2 | 6,136.8 | 6,019.5 | 5,902.3 | 5,785.0 |
| **TOTAL ASSETS** | **11,768.7** | **11,958.6** | **12,189.6** | **12,438.2** | **12,704.9** |
| Floor Plan Notes Payable | 2,063.9 | 2,101.0 | 2,138.9 | 2,177.4 | 2,216.5 |
| Term Debt | 3,422.0 | 3,272.0 | 3,122.0 | 2,972.0 | 2,822.0 |
| Revolving Credit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Other Liabilities | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 |
| Total Liabilities | 7,613.4 | 7,500.5 | 7,388.4 | 7,276.9 | 7,166.0 |
| Common Stockholders' Equity | 4,155.3 | 4,458.1 | 4,801.2 | 5,161.4 | 5,538.9 |
| **TOTAL LIABILITIES & EQUITY** | **11,768.7** | **11,958.6** | **12,189.6** | **12,438.2** | **12,704.9** |

### 3. Cash Flow / FCFE Statement (USD Millions)
| Line Item | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---:|---:|---:|---:|---:|
| Net Income | 413.6 | 452.8 | 493.1 | 510.1 | 527.5 |
| (+) Depreciation | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| (+) Non-cash Impairment | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| (-) Capital Expenditures | -250.0 | -250.0 | -250.0 | -250.0 | -250.0 |
| (-) Change in Inventory | -38.9 | -39.1 | -39.8 | -40.6 | -41.3 |
| (-) Change in Other Working Capital | -2.6 | -2.6 | -2.7 | -2.7 | -2.8 |
| (+) Change in Floor Plan Notes | 36.9 | 37.1 | 37.8 | 38.5 | 39.2 |
| (-) Term Debt Repayment | -150.0 | -150.0 | -150.0 | -150.0 | -150.0 |
| **Free Cash Flow to Equity (FCFE)** | **211.4** | **255.1** | **299.7** | **320.9** | **342.3** |
| (-) Share Buybacks | -150.0 | -150.0 | -150.0 | -150.0 | -150.0 |
| (+/-) Net Revolver Draw / (Repayment) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Net Change in Cash | 61.4 | 105.1 | 149.7 | 170.9 | 192.3 |
| **Ending Cash Balance** | **101.8** | **206.9** | **356.6** | **527.5** | **719.8** |

---

## 4. Balance & Liquidity Checks

| Metric | 2026E | 2027E | 2028E | 2029E | 2030E | Status |
|---|---:|---:|---:|---:|---:|:---:|
| **Assets − Liabilities − Equity** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** | **PERFECT BALANCE** |
| **Cash Balance ($\ge \$25M$)** | $101.8 | $206.9 | $356.6 | $527.5 | $719.8 | **LIQUIDITY PASS** |

### Benchmark Reconciliation Table
| Target Metric | FY2026E Model | FY2026E Benchmark | FY2030E Model | FY2030E Benchmark | Status |
|---|---:|---:|---:|---:|:---:|
| **Revenue** | $18,323.0M | $18,323.0M | $19,678.3M | $19,678.3M | **PASS** |
| **Operating Income** | $844.2M | $844.2M | $971.4M | $971.4M | **PASS** |
| **Net Income** | $413.6M | $413.6M | $527.5M | $527.5M | **PASS** |
| **Free Cash Flow to Equity** | $211.4M | $211.4M | $342.3M | $342.3M | **PASS** |
| **Year-End Cash** | $101.8M | $101.8M | $719.8M | $719.8M | **PASS** |
| **Assets − Liab − Equity** | **0.0** | **0.0** | **0.0** | **0.0** | **PASS** |
| **Value Per Diluted Share** | **$291.75** | **$291.75** | — | — | **PASS** |

---

## 5. Valuation Proof (Cost of Equity = 10.0%, Terminal Growth = 2.5%)

* **PV of 5-Year Explicit FCFE:**  
  $$\sum_{t=1}^{5} \frac{\text{FCFE}_t}{(1.10)^t} = \$192.2 + \$210.8 + \$225.2 + \$219.2 + \$212.5 = \mathbf{\$1,059.9M}$$
* **Terminal Value at 2030E:**  
  $$\text{Terminal Cash Flow}_{2031\text{E}} = (\$342.3\text{M} + \$150.0\text{M}) \times 1.025 = \mathbf{\$504.6M}$$  
  $$\text{Terminal Value}_{2030\text{E}} = \frac{\$504.6\text{M}}{0.10 - 0.025} = \mathbf{\$6,727.8M}$$
* **PV of Terminal Value:**  
  $$\text{PV}(\text{TV}) = \frac{\$6,727.8\text{M}}{(1.10)^5} = \mathbf{\$4,177.5M}$$
* **Total Equity Value:**  
  $$\text{Equity Value} = \$1,059.9\text{M} + \$4,177.5\text{M} = \mathbf{\$5,237.3M}$$
* **Share of Value after 2030 (TV %):**  
  $$\frac{\$4,177.5\text{M}}{\$5,237.3\text{M}} = \mathbf{79.8\%} \quad (\approx 80\%)$$
* **Value per Diluted Share:**  
  $$\frac{\$5,237.3\text{M}}{17.951349\text{M shares}} = \mathbf{\$291.75}$$

---

## 6. Swap-and-Break Test: Enforcing Model Integrity

### The Test
In `proforma.py`, run the intentional failure test where 2026 ending cash is forced to the opening balance of `$40.4M` rather than the computed `$101.8M`.

### The Result
The model immediately aborts valuation and raises a descriptive `ValueError`:
```text
ValueError: Balance sheet check failed in FY2026E: Gap is -61.4 (Assets != Liabilities + Equity)
```

### What the `-$61.4M` Gap Tells the Analyst Before Reading Code
The gap of **`-$61.4M`** is the net change in cash generated by operations in 2026 ($101.8 - 40.4 = +61.4$) with the sign flipped. It tells the analyst immediately that cash on the balance sheet failed to capture the cash flows generated by the business. A model that runs and outputs a share price despite an unbalanced balance sheet is defective; the `assert_balanced` check prevents false valuations from ever reaching an investment committee.

---

## 7. Floor Plan Financing: Learn on Your Own

1. **What is it?** Floor plan financing consists of short-term revolving collateralized loans provided by automotive captive finance arms (e.g., Ford Credit, GM Financial) or commercial banks to finance dealership new and used vehicle inventory.
2. **How does it work in the model?** Dealerships borrow to put cars on the lot. As inventory expands with sales growth ($+38.9\text{M}$ in 2026), floor plan notes automatically expand by 94.9% of that amount ($+36.9\text{M}$). This acts as an operating cash inflow in FCFE, cushioning working capital drag.
3. **Why removing it collapses cash by ~$1.1 Billion:** If dealerships had to finance their inventory lots purely from cash with zero floor plan loans, the working capital burden would absorb ~$\$$2.0B+ of capital immediately. In the tutorial video, removing the floor plan mechanism causes Asbury's projected cash to crater to **$-1.1 Billion**, demonstrating that automotive retail cannot exist as a business without captive inventory financing.
