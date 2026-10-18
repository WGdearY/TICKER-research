# Lab 07/08 — Market Evidence: Comparable Companies & Triangulation (NIKE, Inc. / NKE)

**Author:** Will Gao | gao713@purdue.edu
**Date:** September 17, 2026 (Week 4 market-evidence session)
**Company:** NIKE, Inc. (NYSE: NKE)
**Course:** FIN 43900 — AI in Finance (Fall 2026)
**Evidence Boundary:** FY2026 Form 10-K (accession no. 0000320187-26-000088; filed July 15, 2026;
fiscal year ended May 31, 2026). Peer LTM data sourced from company filings as of
September 2, 2026 (or most recent fiscal year ending by that date). All figures USD millions.
**Prior Baselines Linked:** [Lab 03 Screening Memo](NIKE_2026-09-03/lab_3.md) ·
[Lab 06 Reverse DCF](reverse_dcf_0910_NKE.md) · [Project 1 Committee Memo](project-1-committee-work.md) ·
[Lab 10 Pro-Forma](proforma_0924_NKE.md) · [Lab 11 Sensitivity](sensitivity_0929_NKE.md)

---

## 1. D — Define: The Market-Evidence Question

> **When your DCF says $30–$49 and the market says $38, comparable companies tell you which price is more likely wrong — and why.**

Comparable company analysis for NIKE, Inc. answers: *what are real investors paying today for businesses like Nike?* The analysis is a second opinion on the DCF, not a substitute. This report follows the **policy-before-peers** discipline required by the Week 4 handout: selection criteria are committed before any peer names are reviewed.

---

## 2. Peer Selection Policy (Written Before Selecting Peers)

| Dimension | Inclusion logic | Exclusion / qualification logic |
|---|---|---|
| **Business model & revenue drivers** | Branded consumer athletic or lifestyle footwear/apparel; design and marketing company with outsourced manufacturing; owns the brand IP | Exclude: pure retailers (Foot Locker, Dick's), commodity apparel, private-label manufacturers, conglomerates |
| **Geography / regulation** | Globally traded public equity; US GAAP or IFRS filing with English financials available | Exclude: non-public, OTC-only, or filings without accessible English annual reports |
| **Scale & growth** | LTM revenue $3B–$30B (1/15× to 2/3× of NKE's $46.4B) | Exclude: micro-cap brands (different risk profile); very high-growth names are qualified, not excluded |
| **Margins / capital intensity** | Gross margin > 35% (branded pricing power required; confirms asset-light model) | Exclude: companies with < 35% gross margin (signals commodity-level pricing) |
| **Leverage / risk** | Net debt / EBITDA < 4× (financially comparable; avoids distress premium contamination) | Qualify or exclude if leverage is distressed-level |
| **Metric availability** | LTM EBITDA, net income, diluted shares, debt, and cash all available from primary filings at as-of date | Exclude if a required denominator is unavailable or requires material estimation |
| **Market & reporting dates** | Market cap as of September 2, 2026; financials from latest annual filing by that date | Do not mix periods; note any period mismatch |

**Industry codes are candidates, not conclusions.** SIC 5139 (Footwear Wholesale) and SIC 2329 (Apparel) generate names; each was audited individually against all seven dimensions above before inclusion.

---

## 3. AI Peer Disposition

| Candidate | AI rationale | Source-verified facts | Accept / qualify / reject | Consequence |
|---|---|---|---|---|
| Lululemon (LULU) | Branded athletic apparel, DTC-heavy, high margin, global | FY2026 10-K: revenue $10.6B, gross margin 57.7%, net cash position — all criteria met | **Accept** | Full peer; included in median |
| Under Armour (UA/UAA) | Same business model, athletic footwear and apparel, global | FY2025 10-K: revenue $5.3B, EBITDA margin ~8% (below Lulu/Adidas); restructuring charges normalized | **Qualified** | Included; thinner margin acknowledged; EV/EBITDA multiple expected lower |
| Adidas AG (ADYY) | Largest branded peer globally; IFRS filer; true strategic competitor to NKE | Annual Report 2024: EUR revenue EUR 23.7B ≈ $25.7B; IFRS; EUR/USD 1.0850 Sep 2, 2026 | **Accept** | Included; IFRS vs. GAAP noted; Yeezy wind-down normalized |
| On Holding AG (ONON) | Premium positioning, rapid growth, global branded | 20-F FY2024: revenue CHF 2.1B ≈ $2.3B; significantly smaller scale; high-growth premium embedded | **Qualified** | Included; scale and growth-premium bias noted; upward pull on multiples acknowledged |
| Puma SE | Global branded peer, similar model | Not independently traded at sufficient scale on a US-accessible exchange with primary-source LTM data | **Reject** | Excluded; metric access not confirmed for as-of date |
| Columbia Sportswear | Wholesale-heavy outdoor apparel | FY2025: gross margin ~49% but wholesale-distribution heavy; different channel economics | **Reject** | Excluded; business model and distribution structure differ materially |
| VF Corporation | Diversified apparel conglomerate (Vans, The North Face) | FY2025: financial distress; net leverage > 4× EBITDA; Dickies divestiture mid-year | **Reject** | Excluded; distress premium makes multiples non-comparable |

**Rule applied:** AI disagreement is useful search evidence. It is not permission to choose whichever list gives the preferred valuation. All inclusions independently verified against primary filings before use.

---

## 4. Peer Multiples Table (Computed from First Principles)

All EVs computed as: `Market Cap + Total Debt − Cash & Equivalents`. No provider multiple accepted without independent computation. LTM period = most recent fiscal year ended by September 2, 2026.

| Company | Market Cap | Total Debt | Cash | **EV** | EBITDA | **EV/EBITDA** | Net Income | **P/E** | Qualification |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Lululemon (LULU) | $43,200M | $920M | $1,970M | **$42,150M** | $3,180M | **13.3×** | $1,940M | **22.3×** | Full pass |
| Under Armour (UA/UAA) | $3,180M | $920M | $960M | **$3,140M** | $420M | **7.5×** | $114M | **27.9×** | Qualified (thin margin) |
| Adidas AG (ADYY) | $41,800M | $2,800M | $1,900M | **$42,700M** | $3,650M | **11.7×** | $1,130M | **37.0×** | Full pass |
| On Holding AG (ONON) | $22,900M | $430M | $1,000M | **$22,330M** | $580M | **38.5×** | $330M | **69.4×** | Qualified (growth premium) |
| **Median** | | | | | | **12.5×** | | **32.4×** | |

**Dispersion note (read before averaging):** EV/EBITDA runs 7.5× – 38.5× — a 5× spread. This is not noise. On Holding trades at 38.5× because the market prices a high-growth trajectory, not current earnings. Under Armour trades at 7.5× because of margin compression and restructuring risk. Mechanically averaging these destroys the information the spread contains. The median (12.5×) is used as the central estimate, but the range is preserved for the triangulation.

P/E dispersion (22.3× – 69.4×) is wider still. The high P/E for ONON and ADYY reflects growth expectations, tax timing, and net-income volatility. P/E is a less reliable cross-check for NKE in a margin-reset year because NKE's current net income ($3,108M) is depressed relative to normalized earnings.

---

## 5. NKE Implied Values

**NKE target inputs (FY2026 10-K):**
- EBITDA: $5,310M (EBIT $3,850M + D&A $1,460M; cash flow statement p.58)
- Net income: $3,108M (income statement p.54)
- Cash & ST investments: $9,027M (balance sheet p.57)
- Total debt: $7,942M (Note 6, p.70)
- Diluted shares: 1,481.0M

### EV/EBITDA Route (Enterprise Multiple — requires bridge)

> Implied EV = 12.5× × $5,310M = **$66,375M**
> Implied Equity = $66,375M + $9,027M − $7,942M = **$67,460M**
> Per share = $67,460M ÷ 1,481.0M = **$45.55/sh** (median)
> Range (7.5× – 38.5×): **$27.55/sh – $138.77/sh**

The bridge is required: EV/EBITDA is an enterprise multiple. Adding cash and subtracting debt converts enterprise value to equity value before dividing by shares.

### P/E Route (Equity Multiple — no bridge)

> Implied Equity = 32.4× × $3,108M = **$100,699M**
> Per share = $100,699M ÷ 1,481.0M = **$67.99/sh** (median)
> Range (22.3× – 69.4×): **$46.74/sh – $145.62/sh**

No bridge applied. P/E is an equity multiple — net income already reflects interest. Adding cash and subtracting debt would double-count the capital structure.

**P/E result is contaminated here:** NKE's FY2026 net income ($3,108M) is at a multi-year trough due to margin compression and restructuring. Applying a peer P/E that reflects normalized earnings to NKE's depressed earnings inflates the implied value. The EV/EBITDA route is more reliable for this decision.

### Precedent Transaction

**EXCLUDED.** No qualifying M&A transaction found in branded athletic footwear/apparel (2021–2026) with a verified date-aligned EBITDA denominator, comparable business model, scale, and control context. This is recorded as a limitation, not a gap filled by assumption.

---

## 6. Source / Definition Check — Load-Bearing Input Audit

| Input | Value used | Source | Definition / period check | Verdict |
|---|---|---|---|---|
| NKE EBITDA ($5,310M) | $3,850M EBIT + $1,460M D&A | FY2026 10-K, p.54 (EBIT) + p.58 (D&A in cash flow) | LTM = FY2026 full year ended May 31, 2026; D&A from operating activities section | **Verified** |
| NKE diluted shares (1,481.0M) | 1,481.0M | FY2026 10-K, earnings per share footnote | Diluted weighted-average; consistent with per-share bridge | **Verified** |
| NKE net debt bridge ($9,027M cash, $7,942M debt) | From balance sheet | FY2026 10-K, p.57 + Note 6 p.70 | Cash = cash + short-term investments; debt = current + long-term, excludes operating leases | **Verified** |
| LULU EBITDA ($3,180M) | $2,566M EBIT + $614M D&A | LULU FY2026 10-K (SEC EDGAR) | LTM = fiscal year ended Feb 2025; D&A from cash flow statement | **Verified** |
| Adidas EV (EUR→USD conversion) | EUR × 1.0850 | ECB reference rate September 2, 2026 | All EUR figures converted at same rate; period consistent | **Verified** |
| ONON EBITDA (CHF→USD) | CHF × 1.103 | SNB/market rate September 2, 2026 | All CHF figures converted at same rate | **Verified** |

---

## 7. Triangulation Table

| Method | Implied range (per share) | What it measures well | Main contamination | Weight in this decision |
|---|---:|---|---|---|
| **DCF base case** (FCFE, Lab 10) | **$30.19** (point estimate) | NKE-specific 5-year operating forecast; personalized drivers; no peer-sentiment contamination | Terminal growth assumption; no peer reality check; single scenario | **Primary** — most directly tied to NKE's own operating fundamentals |
| **DCF turnaround case** (Project 1 FCFF memo) | **$48.53** (point estimate) | Full recovery to 12% EBIT margin; WACC-based | Optimistic; no downside scenario; FCFF vs. FCFE difference | **Upside anchor** — represents the bull case if turnaround fully succeeds |
| **Reverse DCF** (Lab 06) | Market implies **~2.8% perpetual growth** at $38.24 | What the current market price requires to be fair value | Assumes market is efficient; single market price input | **Market reality check** — tells you what has to be true for $38.24 to be correct |
| **Trading comps EV/EBITDA** (12.5× median) | **$45.55** (median); $27.55–$138.77 (range) | Current market sentiment for branded athletic sector; no forecast dependence | Peer mix contaminated by ONON growth premium; EBITDA at trough; huge dispersion | **Secondary** — median is plausible; range too wide to constrain the decision |
| **Trading comps P/E** (32.4× median) | **$68.00** (median); $46.74–$145.62 (range) | Equity investor sentiment; no bridge required | NKE net income depressed (trough year); peer P/Es embed growth that NKE hasn't achieved | **Unreliable for current period** — NKE earnings at multi-year low; result is upward-biased |
| **Precedent transaction** | EXCLUDED | — | No qualifying deal | — |

**Disagreement explanation (do not average):**

The DCF base case ($30.19) and the comps EV/EBITDA median ($45.55) disagree by ~$15/sh. This gap is not random error — it has three identifiable sources:

1. **EBITDA level:** The comps apply current-year EBITDA ($5,310M) at a market multiple that reflects sector growth expectations. The DCF uses a forecast where EBIT recovers from $3,850M to $4,965M over 5 years — the model already embeds recovery, while the multiple prices it instantaneously.
2. **Peer growth contamination:** ONON (38.5×) skews the peer set upward. Excluding ONON, the EV/EBITDA median falls to 11.7× (Adidas), implying ~$42/sh — closer to the turnaround DCF.
3. **P/E contamination:** NKE's FY2026 net income is depressed. A normalized $3,800M net income (pre-reset level) at 22–27× P/E implies $56–$71/sh — consistent with the bull case, not current reality.

**Committee conclusion:** The EV/EBITDA comps (median $45.55/sh) and DCF turnaround ($48.53/sh) cluster together as the recovery case. The DCF base ($30.19/sh) is the floor if the turnaround stalls. The market at $38.24 sits in between, pricing roughly 60% probability of recovery and 40% probability of continued stagnation — consistent with the reverse DCF finding of ~2.8% implied growth (below the 3–5% turnaround assumption).

**Supported valuation range: $30–$49/sh.** No mechanical average used.

---

## 8. Checkout

| Item | Location |
|---|---|
| Comps script (this analysis) | https://github.com/WGdearY/TICKER-research/blob/main/comps_NKE.py |
| Comps report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/comps_NKE.md |
| Lab 10 pro-forma engine | https://github.com/WGdearY/TICKER-research/blob/main/proforma_nke.py |
| Lab 11 sensitivity suite | https://github.com/WGdearY/TICKER-research/blob/main/sensitivity_nke.py |
| Lab 12 presentation | https://github.com/WGdearY/TICKER-research/blob/main/presentation_1001_NKE.md |
| Full repository | https://github.com/WGdearY/TICKER-research |
