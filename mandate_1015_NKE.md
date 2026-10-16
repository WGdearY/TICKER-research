# Lab 13 — Portfolio Mandate Defense

**Author:** Will Gao | gao713@purdue.edu  
**Date:** October 15, 2026  
**Case:** Week 8 Common CIO Case — Meridian Foundation Reserve (fictional, course-authored)  
**Ticker scope:** N/A — this is a mandate-structure exercise, not a Project 2 security analysis

---

## Part 1 — Human-First: Statement Classification

> Completed before any AI input. Each CIO statement is classified as an **objective**,  
> **hard constraint**, **preference**, **aspiration**, or **unverifiable promise**.

| # | CIO Statement (from case, verbatim or paraphrased) | Classification | Reason |
|---|---|---|---|
| 1 | Policy objective is CPI + 4% net of costs over rolling 5-year periods | **Objective** | Measurable, time-bounded, net-of-cost — it is the stated purpose of the mandate |
| 2 | 7-year policy horizon, quarterly review, annual rebalancing | **Hard constraint** | Defined governance cycle; deviating requires committee action |
| 3 | Reserve distributes $750,000 at end of each calendar quarter | **Hard constraint** | Fixed scheduled cash outflow; portfolio must fund it |
| 4 | At least 12 months of distributions must remain in cash or daily-liquid government securities | **Hard constraint** | Explicit liquidity floor: $3,000,000 minimum in daily-liquid instruments at all times |
| 5 | Benchmark is 60% broad global equities / 40% U.S. investment-grade bonds | **Hard constraint** | Named policy benchmark; performance measurement is referenced to it |
| 6 | Long-only, no borrowing, no short sales, no derivatives | **Hard constraint** | Four explicit prohibitions stated without qualification |
| 7 | Single issuer may not exceed 8% | **Hard constraint** | Stated as a maximum; enforceable at the position level |
| 8 | Annual turnover should not exceed 25% unless committee approves exception | **Preference** (near-hard) | "Should not" language allows exception; but exception requires documented committee approval, making it functionally a soft constraint |
| 9 | At least 90% redeemable within 5 business days under ordinary market conditions | **Hard constraint** | Explicit percentage threshold; "ordinary market conditions" qualifier is the only softness |
| 10 | "The reserve cannot have a calendar-year loss greater than 10%" | **Aspiration / Unverifiable promise** | No enforcement rule, probability, or breach-response supplied; aspirational unless a drawdown trigger and response plan are defined |
| 11 | No sector, climate, social, tax, active-management, or home-bias preference stated | **Not a constraint** — absence of preference | Signals the mandate leaves these to analyst judgment; not enforceable |
| 12 | Committee has not defined whether pilot optimizes return, tracking error, drawdown, distribution probability, or another tradeoff | **Missing fact — requires escalation** | No optimizer objective can be operationalized until this is resolved |

**Missing facts identified before AI:**
- Optimization criterion for the pilot (return, tracking error, drawdown risk, or distribution-funding probability)
- Loss-limit enforcement mechanism (breach trigger, response plan, probability level)
- Whether the 25% turnover cap resets annually at calendar year-end or rolling 12 months

---

## Part 2 — Complete Mandate Record

**Decision user:** Meridian Foundation investment committee  
**Decision:** Authorize analysis and a small pilot allocation for the $100M reserve — not execute trades today  
**As-of date:** October 15, 2026  
**Currency / share basis:** USD; fund-level NAV (not per-share)

| Mandate element | Operational value | Governing fact |
|---|---|---|
| **Objective** | CPI + 4.0% net of estimated costs, measured over rolling 5-year periods | CIO stated objective; measurable against CPI releases and fee schedules |
| **Benchmark** | 60% broad global equities / 40% U.S. investment-grade bonds | Case, sentence 5; named policy benchmark |
| **Naive baseline** | Static 60/40 allocation, no rebalancing, no active tilt — used as the minimum-complexity comparison | Standard practice; no competing baseline stated in case |
| **Horizon / rebalancing** | 7-year policy horizon; quarterly review; annual rebalancing | Case, sentences 2–3 |
| **Risk measure** | Calendar-year portfolio return; loss limit stated as > -10% in any calendar year | Case, sentence on loss; note: no probability or enforcement rule supplied |
| **Liquidity rule** | $3,000,000 in cash or daily-liquid government securities at all times (= 4 quarters × $750,000); 90% of total portfolio redeemable within 5 business days under ordinary market conditions | Case, sentences 4 and 9 |
| **Constraints (4+)** | (1) Long-only, no borrowing, no short sales, no derivatives; (2) Single issuer ≤ 8% of portfolio; (3) Annual turnover ≤ 25% (committee exception required); (4) $3M liquidity floor in daily-liquid government securities; (5) 90% of portfolio within 5-day redemption | Case, sentences 6–9 |
| **Universe** | Any instrument compatible with the above constraints; no sector, geographic, or style restriction stated | Case, sentence 11 |
| **Unresolved ambiguity** | Optimization criterion for the pilot is undefined; loss-limit has no enforcement mechanism or breach-response plan | Case, sentence 12 and sentence on "cannot have" |

**Precommitted validation tests:**

| Test | Benchmark / baseline | Perturbation | Holdout | Cost / failure condition |
|---|---|---|---|---|
| Benchmark tracking | 60/40 naive baseline | ±5% equity weight shift | Q1–Q2 2026 return period | Tracking error > 4% signals excessive active risk |
| Liquidity floor | $3,000,000 minimum at all times | Stress: equity drawdown 20% in one quarter | Full 7-year horizon | Any quarter where liquid buffer < $3M = mandate breach |
| Distribution coverage | 4 quarters funded without forced sale | Scenario: 2-quarter equity decline | Rolling 4-quarter lookback | Forced sale of illiquid asset = failure |
| Turnover cap | 25% annual limit | Rebalancing-triggered turnover model | Calendar year | Turnover > 25% without committee record = constraint breach |
| Concentration cap | 8% per issuer | Index rebalancing pushes one name above cap | Monthly | Any position > 8% = hard breach |

---

## Part 3 — Two AI Interpretation Dispositions

> Prompt given to each system (exact common prompt from case):  
> *"Propose two materially different operational interpretations of the Meridian Foundation mandate. For each interpretation, list the objective, hard constraints, assumptions you had to invent, validation tests, and the one CIO question that must be answered before optimization. Do not choose securities or produce an allocation."*

### System A — Interpretation 1: Distribution-First (Safety Bias)

**Stated by system:** Objective is to ensure distributions are funded throughout the 7-year horizon; CPI + 4% is aspirational and secondary. Pilot should minimize probability of distribution failure rather than maximize expected return.

| Claim | Tag | Governing fact |
|---|---|---|
| Distribution funding is the primary objective | **Unsupported** | Case states CPI + 4% is the objective; distributions are a liquidity constraint, not the stated objective |
| 12-month liquid buffer covers 4 quarters = $3M | **Supported** | Case, sentence 4: "at least twelve months of scheduled distributions" = 4 × $750,000 |
| CPI + 4% is "aspirational" | **Requires clarification** | Case calls it the objective; whether it is enforceable or aspirational depends on committee governance not supplied |
| Pilot should use a liability-matching framework | **Unsupported** | Case does not specify the optimization framework; this is an invented assumption |
| Loss limit of >-10% is a hard constraint | **Requires clarification** | Case says the CIO "says" it; no probability level or enforcement mechanism is stated — case explicitly flags this gap |
| One CIO question before optimization | "Is the primary success criterion funding every distribution, or achieving CPI + 4%?" | **Supported** — maps directly to the unresolved case ambiguity |

### System B — Interpretation 2: Return-First (Active-Management Bias)

**Stated by system:** Objective is to beat the 60/40 benchmark by achieving CPI + 4%, using the 7-year horizon to tolerate short-term volatility; distributions and the loss limit are constraints but do not override return-seeking.

| Claim | Tag | Governing fact |
|---|---|---|
| CPI + 4% is the primary objective, benchmark is secondary | **Supported** | Case states CPI + 4% as objective and 60/40 as the benchmark; these are distinct roles |
| Horizon of 7 years allows equity overweight vs. naive 60/40 | **Requires clarification** | Case does not authorize deviation from the 60/40 benchmark; overweight requires a stated active-management preference that is absent |
| 90% liquidity rule allows 10% in less-liquid assets (e.g., private credit) | **Requires clarification** | Technically consistent with the 90% rule but contradicts long-only, no-derivatives language; depends on whether private credit counts as a derivative substitute |
| Annual rebalancing creates turnover headroom | **Supported** | Case specifies annual rebalancing; 25% cap is stated separately |
| Loss limit is a soft guardrail, not a hard constraint | **Supported** | Case explicitly notes no enforcement rule or breach-response is supplied |
| One CIO question before optimization | "Should the pilot minimize tracking error to the 60/40 benchmark or maximize probability of meeting CPI + 4%?" | **Supported** — maps directly to the unresolved optimization criterion gap |

### Cross-System Assessment

Agreement between the two systems that the optimization criterion is unresolved does **not** resolve the CIO's missing preference. Both interpretations invent assumptions about which objective dominates. Neither system can choose between distribution-first and return-first without a CIO answer. This confirms the escalation requirement — do not proceed to optimization.

---

## Part 4 — Minimum Escalation Question

**Before any optimization can proceed, the committee must answer:**

> **"Is the primary success criterion for the pilot (a) maximizing probability of funding every scheduled distribution throughout the 7-year horizon, or (b) achieving the stated CPI + 4% objective over rolling 5-year periods — and what is the committee's response plan if a calendar-year loss exceeds 10%?"**

**Why this question cannot be bypassed:**

- Without knowing (a) vs. (b), the pilot optimizer's objective function cannot be specified.
- Both AI interpretations invented a priority ranking that is absent from the CIO facts.
- The loss-limit statement has no enforcement mechanism; silently treating it as a hard constraint or as aspirational changes the portfolio's risk posture materially.
- No allocation, optimization run, or asset selection should proceed until this answer is recorded in the committee minutes.

---

## Checkout

| Item | Location |
|---|---|
| Lab 13 mandate record (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_13.md |
| Lab 10 pro-forma engine | https://github.com/WGdearY/TICKER-research/blob/main/proforma_nke.py |
| Lab 11 sensitivity suite | https://github.com/WGdearY/TICKER-research/blob/main/sensitivity_nke.py |
| Lab 12 presentation | https://github.com/WGdearY/TICKER-research/blob/main/presentation_1001_NKE.md |
| Full repository | https://github.com/WGdearY/TICKER-research |

