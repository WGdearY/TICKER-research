# Lab 15 — Alternative Data Admission

**Author:** Will Gao | gao713@purdue.edu
**Date:** October 22, 2026
**Course:** FIN 43900 — AI in Finance (Fall 2026), Lab 15 / Week 10
**Panel provenance:** Course-authored synthetic alternative-data teaching panel. Not real data. No real entities or securities.
**Decision cutoff:** `2026-01-02T10:00:00Z`
**Script:** [altdata_nke.py](https://github.com/WGdearY/TICKER-research/blob/main/altdata_nke.py)

---

## Prework Record (Written Before Running — No AI)

**1. Timestamp that controls admissibility:**
`available_time` — not `event_time`. An event happening at 09:00 does not mean the data was in your information set at 09:00. The data vendor processes, validates, and delivers the record at `available_time`. Using `event_time` as the cutoff creates lookahead bias: you would be using information that hadn't reached you yet.

**2. One row I expect to be unavailable at the cutoff (`2026-01-02T10:00:00Z`):**
Row 2 (entity B) — `available_time` is `2026-01-02T17:00:00Z`, seven hours after the cutoff. This row should be quarantined.

---

## Part 1 — Intended Decision and Information Cutoff

**Decision:** Determine whether the supplied 7-row panel may be used as-is for a historical signal test (back-test).
**Information cutoff:** `2026-01-02T10:00:00Z` — the portfolio/research decision time supplied by the handout.
**Evaluation label embargo:** `future_return` is present in the panel for later evaluation only. It may **not** be used to choose the sample, construct the rule, select a threshold, or make the admission decision.

---

## Part 2 — Data Card

| Field | Evidence or value | Unknown / limitation | Decision consequence |
|---|---|---|---|
| **Source / owner and collection method** | Course-authored synthetic panel; fictional vendor | Vendor identity, collection method, and data-feed infrastructure are not supplied | Cannot verify vendor reliability; treat as unknown provenance for any real use |
| **License / use boundary** | Course practice only — not real data | No license terms exist; this panel has no commercial use boundary | Acceptable for classroom exercise only; no external use |
| **Population / unit / coverage** | 7 observations; 3 fictional entities (A, B, C); two event dates (Jan 2–3, 2026) | Coverage is illustrative; no real market, sector, or geography stated | Cannot infer completeness or representativeness |
| **Entity identifier and mapping** | `entity_id`: single-letter synthetic IDs (A, B, C); row 7 has no entity ID | Row 7 has a missing identifier — entity cannot be mapped | Row 7 is inadmissible on identity grounds; cannot be used even if timing were valid |
| **Event, availability, decision, revision time** | `event_time`: when event occurred; `available_time`: when data was deliverable; `decision_time`: `2026-01-02T10:00:00Z`; `revision`: 1 = corrected record | No vendor SLA or delivery-lag documentation supplied | Admission rule must rely on `available_time`; event_time alone is insufficient |
| **Missingness / duplicates / revisions** | 1 missing entity (row 7); 1 exact duplicate (rows 3 and 4 identical); 1 revision (row 6, revision=1) | No documentation on revision frequency or correction policy | Duplicates and revisions must be handled explicitly; revision is not retroactively available |
| **PII / privacy and retention** | Synthetic data — no real persons, no PII | N/A for teaching panel | No privacy concern for this exercise; real alternative data would require a PII audit |
| **Evaluation label and embargo** | `future_return` is the evaluation label; supplied for later evaluation only | Cannot be used for admission, rule design, threshold selection, or sample construction | Embargo is absolute — any use of `future_return` before the evaluation stage contaminates the test |

---

## Part 3 — Mechanical Flags (All 7 Rows Preserved)

| Row ID | Entity | Event time | Available time | Late? | Missing ID? | Exact dup? | Revision? |
|---:|---|---|---|---|---|---|---|
| 1 | A | 2026-01-02 09:00Z | 2026-01-02 09:05Z | No | No | No | No |
| 2 | B | 2026-01-02 09:00Z | 2026-01-02 **17:00Z** | **Yes** | No | No | No |
| 3 | C | 2026-01-02 09:00Z | 2026-01-02 09:04Z | No | No | No | No |
| 4 | C | 2026-01-02 09:00Z | 2026-01-02 09:04Z | No | No | **Yes** | No |
| 5 | A | 2026-01-03 09:00Z | 2026-01-03 09:05Z | **Yes** | No | No | No |
| 6 | A | 2026-01-03 09:00Z | **2026-01-05 10:00Z** | **Yes** | No | No | **Yes** |
| 7 | *(MISSING)* | 2026-01-03 09:00Z | 2026-01-03 09:06Z | **Yes** | **Yes** | No | No |

**Label leakage field:** `future_return` is present in all 7 rows. It is embargoed and never used for admission.

---

## Part 4 — AI Claim Dispositions

> AI asked to draft source/cleanup claims. Every material claim tagged below.

| Claim (AI-generated) | Tag | Independent verification |
|---|---|---|
| "Row 2 is late because its available_time of 17:00 is after the 10:00 cutoff — it should be excluded" | `supported` | Verified: `2026-01-02T17:00:00Z > 2026-01-02T10:00:00Z` — correct and consistent with the point-in-time rule |
| "Rows 3 and 4 are exact duplicates and one should be dropped" | `supported` | Verified: both rows have identical entity_id=C, event_time, available_time, revision=0, signal=0.10 — confirmed exact duplicate |
| "Row 6 is a revised record; the original signal was 0.50 (row 5) and the revision corrected it to 0.70" | `assumption-dependent` | Plausible inference from row_id and matching entity/event_time, but the panel does not document which row 6 revises; revision linkage is an invented assumption not stated in the data |
| "Row 7 has no entity_id because the vendor anonymized it for privacy" | `unsupported — invented provenance` | No privacy or anonymization rule is documented anywhere in the panel or course materials; this is fabricated reasoning; row 7's missing ID is a data quality issue, not a design feature |
| "future_return can be used to validate which rows have accurate signals before admission" | `unsupported` | Explicitly prohibited: handout states future_return "cannot be used to choose the historical sample, rule, threshold, or disposition" — this is the evaluation label embargo |

**Unsupported / invented provenance disposition:**
Row 7 missing-ID claim: **rejected**. The AI invented a privacy rationale with no basis in the data card or course documentation. Row 7 remains quarantined due to missing entity identity, not anonymization.
Future-return validation claim: **rejected**. Using future_return for admission would constitute label leakage — the fundamental error this lab is designed to prevent.

---

## Part 5 — Point-in-Time Rule (Written Before Code)

> Written in plain language before any code was run.

**Admission rule:**
A row is admitted to the valid as-of panel only if **all four** conditions hold:
1. `available_time <= decision_time` — the record was deliverable before the portfolio decision cutoff
2. `entity_id` is not missing — identity must be defensible for mapping to a position
3. `revision == 0` — revised records are not retroactively available; only the original was in the information set at delivery
4. The row is not an exact duplicate — keep the first occurrence by row_id; drop all later identical records

A row failing any condition is **quarantined** (preserved in the audit trail; not deleted).
`future_return` is retained in the audit trail but is never used in any admission step.

---

## Part 6 — Row-Level Admission Table

| Row ID | Event time | Available time | Issue(s) | Disposition | Reason |
|---:|---|---|---|---|---|
| 1 | 2026-01-02 09:00Z | 2026-01-02 09:05Z | None | **ADMIT** | Passes all point-in-time rules |
| 2 | 2026-01-02 09:00Z | 2026-01-02 17:00Z | Late available | **QUARANTINE** | available_time 17:00 > cutoff 10:00 |
| 3 | 2026-01-02 09:00Z | 2026-01-02 09:04Z | None | **ADMIT** | Passes all rules; first of the duplicate pair |
| 4 | 2026-01-02 09:00Z | 2026-01-02 09:04Z | Exact duplicate | **QUARANTINE** | Identical to row 3; later occurrence dropped |
| 5 | 2026-01-03 09:00Z | 2026-01-03 09:05Z | Late available | **QUARANTINE** | Event on Jan 3 — not available by Jan 2 cutoff |
| 6 | 2026-01-03 09:00Z | 2026-01-05 10:00Z | Late + revision | **QUARANTINE** | Available Jan 5 only; also a revision |
| 7 | 2026-01-03 09:00Z | 2026-01-03 09:06Z | Late + missing entity | **QUARANTINE** | Missing entity_id and available after cutoff |

### Row Funnel

```
Total rows:                 7
  └── Late (avail > cutoff): 4  (rows 2, 5, 6, 7)
  └── Missing entity:        1  (row 7 — also late)
  └── Exact duplicate:       1  (row 4 — also passes timing but duplicate)
  └── Revision:              1  (row 6 — also late)
QUARANTINED:                 5  (rows 2, 4, 5, 6, 7)
ADMITTED:                    2  (rows 1, 3)
```

---

## Part 7 — Naive vs. Valid Panel Comparison

**Point-in-time rule change tested once. Prediction written before running.**

### Naive Panel (event_time as cutoff — incorrect)

Admits all rows where `event_time <= 2026-01-02T10:00:00Z`, ignoring `available_time`:

| Rows admitted | Entities | Signal mean |
|---|---|---|
| 3 (rows 1, 2, 3) | A, B, C | **0.1000** |

**Contamination:** Row 2 (entity B, signal = -0.20) is included. Its `available_time` is 17:00 — it was not in the information set at 10:00. Using the naive panel silently imports future information into the historical test.

### Valid Panel (available_time as cutoff — correct)

| Rows admitted | Entities | Signal mean |
|---|---|---|
| 2 (rows 1, 3) | A, C | **0.2500** |

**Quantified difference:**
- Row count: naive 3 vs. valid 2 (−1 row)
- Signal mean: naive 0.1000 vs. valid 0.2500 (delta = +0.1500)
- The naive panel underestimates the signal by 0.15 because it includes entity B's negative signal that was not yet available — a lookahead bias that would produce misleading backtest results.

### Changed Cutoff Experiment

**Pre-run prediction (written before execution):**
Tightening the cutoff from `10:00` to `09:04:00Z` — Row 1 (entity A, available at 09:05) becomes late and moves to quarantine. Row 3 (entity C, available at 09:04) remains admitted (09:04 ≤ 09:04). Valid panel shrinks from 2 to 1 row. Signal mean changes from 0.25 to 0.10.

**Actual result:**
- Admitted: 1 row (row 3 only)
- Signal mean: 0.1000
- Prediction confirmed ✓ — panel shrinks from 2 to 1; mean changes from 0.2500 to 0.1000
- Mandate effect: tighter cutoff increases data quality (less lookahead risk) but reduces sample size

---

## Part 8 — Decision Record

| Element | Content |
|---|---|
| **Action** | **QUARANTINE / PROSPECTIVE-TEST** — the valid 2-row panel (rows 1 and 3) is technically admissible for a historical test, but the sample is too small (2 rows, 2 entities, 1 event date) to support any reliable signal inference. Research must wait or run prospectively with more data. |
| **As-of / revision / duplicate rule** | Cutoff: `2026-01-02T10:00:00Z`; admit on `available_time <= cutoff`; revision=0 required; exact duplicates: keep first by row_id; all quarantined rows preserved in audit trail |
| **Unsupported AI claim and disposition** | "Row 7's missing entity_id is due to privacy anonymization" — **rejected**; invented provenance with no basis in panel or documentation; row 7 quarantined for missing identity |
| **Most consequential limitation** | Only 2 rows admitted; single event date (Jan 2, 2026); no evidence of panel completeness; cannot determine if entities A and C represent the full population or a biased subset |
| **Missing evidence** | Vendor SLA and delivery-lag documentation; revision frequency and correction policy; confirmation that row 6 revises row 5 (or a different original); panel completeness certification |
| **Monitoring / recheck trigger** | If vendor supplies a revised panel with documented available_time for all records, re-run the mechanical flags; if missing entity in row 7 is resolved (vendor provides entity_id), re-evaluate for prospective use |
| **Reversal condition** | Research may proceed to a full historical test if: (a) vendor certifies panel completeness with timestamped delivery receipts, (b) all revisions are linkable to their original records, and (c) the panel covers ≥ 30 event dates across ≥ 10 entities with verified available_times |

---

## Submission Checklist

| Required item | Status |
|---|---|
| Prework record (pre-run predictions, no AI) | ✅ Part 0 |
| Intended decision and information cutoff stated | ✅ Part 1 |
| Data card (all 8 fields filled or marked unknown) | ✅ Part 2 |
| All 7 rows preserved in audit trail | ✅ Parts 3 & 6 |
| Mechanical flags (late, missing, dup, revision, label) | ✅ Part 3 |
| AI claim dispositions (all tagged, invented provenance rejected) | ✅ Part 4 |
| Point-in-time rule written in plain language before code | ✅ Part 5 |
| Row-level disposition table | ✅ Part 6 |
| Row funnel with counts and reasons | ✅ Part 6 |
| Naive vs. valid panel comparison (quantified) | ✅ Part 7 |
| Changed cutoff — predicted before run, result recorded | ✅ Part 7 |
| Decision record (all 6 elements) | ✅ Part 8 |
| future_return never used for admission | ✅ All sections |
| AI disclosure | ✅ Part 4 |

---

## Checkout

| Item | Location |
|---|---|
| Lab 15 script | https://github.com/WGdearY/TICKER-research/blob/main/altdata_nke.py |
| Lab 15 report (this file) | https://github.com/WGdearY/TICKER-research/blob/main/Lab_15.md |
| Lab 14 portfolio script | https://github.com/WGdearY/TICKER-research/blob/main/portfolio_nke.py |
| Full repository | https://github.com/WGdearY/TICKER-research |
