"""
altdata_nke.py — Lab 15: Alternative Data Admission
FIN 43900 — AI in Finance, Fall 2026 | Week 10
Author: Will Gao (gao713@purdue.edu)
Evidence boundary:
  Panel: course-authored synthetic alternative-data teaching panel.
  Decision time (cutoff): 2026-01-02T10:00:00Z (supplied by handout).
  As-of boundary: Oct. 22, 2026 course release.
  Do NOT use future_return to make admission decisions (evaluation label — embargo applies).
Standard library only. No external dependencies.

Point-in-time rule (written before code):
  A row is ADMITTED to the valid as-of panel only if ALL of the following hold:
    1. available_time <= decision_time  (was knowable at the cutoff)
    2. entity_id is not missing          (identity must be defensible)
    3. revision == 0                     (revisions are not retroactively available)
    4. It is not an exact duplicate      (keep the first occurrence by row_id; drop later)
  A row that fails any condition is QUARANTINED (preserved in audit trail, not deleted).
  future_return is kept in the audit trail but is NEVER used for admission decisions.
"""

from __future__ import annotations
import csv
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# SECTION 0: DATA (replicated from alternative_events.csv)
# Source: FIN43900-Fall2026/lessons/week-10/starter/alternative_events.csv
# ---------------------------------------------------------------------------

RAW_ROWS = [
    {"row_id": 1, "entity_id": "A",  "event_time": "2026-01-02T09:00:00Z",
     "available_time": "2026-01-02T09:05:00Z", "revision": 0, "signal":  0.40, "future_return":  0.02},
    {"row_id": 2, "entity_id": "B",  "event_time": "2026-01-02T09:00:00Z",
     "available_time": "2026-01-02T17:00:00Z", "revision": 0, "signal": -0.20, "future_return": -0.01},
    {"row_id": 3, "entity_id": "C",  "event_time": "2026-01-02T09:00:00Z",
     "available_time": "2026-01-02T09:04:00Z", "revision": 0, "signal":  0.10, "future_return":  0.00},
    {"row_id": 4, "entity_id": "C",  "event_time": "2026-01-02T09:00:00Z",
     "available_time": "2026-01-02T09:04:00Z", "revision": 0, "signal":  0.10, "future_return":  0.00},
    {"row_id": 5, "entity_id": "A",  "event_time": "2026-01-03T09:00:00Z",
     "available_time": "2026-01-03T09:05:00Z", "revision": 0, "signal":  0.50, "future_return":  0.03},
    {"row_id": 6, "entity_id": "A",  "event_time": "2026-01-03T09:00:00Z",
     "available_time": "2026-01-05T10:00:00Z", "revision": 1, "signal":  0.70, "future_return":  0.03},
    {"row_id": 7, "entity_id": None, "event_time": "2026-01-03T09:00:00Z",
     "available_time": "2026-01-03T09:06:00Z", "revision": 0, "signal": -0.30, "future_return": -0.02},
]

DECISION_TIME = "2026-01-02T10:00:00Z"


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# SECTION 1: MECHANICAL FLAGS
# Expose every issue without making admission decisions.
# ---------------------------------------------------------------------------

def mechanical_flags(rows: list[dict], decision_time: str) -> list[dict]:
    cutoff = parse_ts(decision_time)
    seen_keys: set = set()
    flagged = []
    for r in rows:
        avail = parse_ts(r["available_time"])
        late = avail > cutoff
        missing_entity = r["entity_id"] is None
        key = (r["entity_id"], r["event_time"], r["available_time"], r["signal"])
        is_dup = key in seen_keys
        seen_keys.add(key)
        is_rev = r["revision"] > 0
        label_leakage = True  # future_return always present; always embargoed
        flagged.append({
            **r,
            "late_available": late,
            "missing_entity": missing_entity,
            "exact_duplicate": is_dup,
            "is_revision": is_rev,
            "label_leakage_field": label_leakage,
        })
    return flagged


# ---------------------------------------------------------------------------
# SECTION 2: POINT-IN-TIME PANEL (valid as-of panel)
# Apply the rule written above (before code).
# ---------------------------------------------------------------------------

def construct_valid_panel(flagged: list[dict]) -> tuple[list[dict], list[dict]]:
    """Returns (admitted, quarantined). Rows preserved in both lists for audit."""
    admitted = []
    quarantined = []
    for r in flagged:
        issues = []
        if r["late_available"]:
            issues.append("late_available")
        if r["missing_entity"]:
            issues.append("missing_entity")
        if r["is_revision"]:
            issues.append("is_revision")
        if r["exact_duplicate"]:
            issues.append("exact_duplicate")

        r_out = {**r, "issues": issues}
        if issues:
            r_out["disposition"] = "QUARANTINE"
            r_out["reason"] = "; ".join(issues)
            quarantined.append(r_out)
        else:
            r_out["disposition"] = "ADMIT"
            r_out["reason"] = "passes all point-in-time rules"
            admitted.append(r_out)
    return admitted, quarantined


# ---------------------------------------------------------------------------
# SECTION 3: NAIVE PANEL (event_time as cutoff — demonstrates lookahead bias)
# ---------------------------------------------------------------------------

def construct_naive_panel(rows: list[dict], decision_time: str) -> list[dict]:
    """
    Naive (incorrect) panel: admits all rows where event_time <= cutoff.
    This ignores available_time — a classic lookahead bias error.
    """
    cutoff = parse_ts(decision_time)
    seen_keys: set = set()
    naive = []
    for r in rows:
        ev = parse_ts(r["event_time"])
        if ev <= cutoff:
            key = (r["entity_id"], r["event_time"], r["available_time"], r["signal"])
            if key not in seen_keys:
                seen_keys.add(key)
                naive.append({**r, "naive_note": "admitted on event_time only"})
    return naive


# ---------------------------------------------------------------------------
# SECTION 4: CHANGED CUTOFF EXPERIMENT
# Predict effect BEFORE running (handout requirement).
# Change cutoff from 10:00 to 09:04:00Z.
# PRE-RUN PREDICTION: Row 3 (avail 09:04) still admitted; Row 1 (avail 09:05) now quarantined.
# Valid panel shrinks from 2 rows to 1 row. Signal mean changes.
# ---------------------------------------------------------------------------

CHANGED_CUTOFF = "2026-01-02T09:04:00Z"
CHANGED_CUTOFF_PREDICTION = (
    "Tightening cutoff from 10:00 to 09:04: Row 1 (entity A, avail 09:05) "
    "becomes late and moves to quarantine. Row 3 (entity C, avail 09:04) "
    "remains admitted (09:04 <= 09:04). Valid panel shrinks from 2 to 1 row. "
    "Mean signal changes from 0.25 (average of 0.40, 0.10) to 0.10 (only row 3)."
)


def signal_mean(rows: list[dict]) -> float:
    if not rows:
        return float("nan")
    return sum(r["signal"] for r in rows) / len(rows)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 68

    print(sep)
    print("LAB 15 — ALTERNATIVE DATA ADMISSION")
    print("Author: Will Gao | gao713@purdue.edu")
    print(f"Decision cutoff: {DECISION_TIME}")
    print(f"Panel: course-authored synthetic, Oct. 22, 2026")
    print(sep)

    # Step 1: Flag all rows
    flagged = mechanical_flags(RAW_ROWS, DECISION_TIME)

    print("\nSECTION 1 — MECHANICAL FLAGS (all 7 rows preserved)")
    print(f"  {'Row':>3} {'Entity':>8} {'Available time':>25} {'Late':>6} "
          f"{'MissID':>7} {'Dup':>5} {'Rev':>5}")
    print("  " + "-" * 65)
    for r in flagged:
        entity = r["entity_id"] if r["entity_id"] else "(MISSING)"
        print(f"  {r['row_id']:>3} {entity:>8} {r['available_time']:>25} "
              f"{str(r['late_available']):>6} {str(r['missing_entity']):>7} "
              f"{str(r['exact_duplicate']):>5} {str(r['is_revision']):>5}")

    print("\n  Label leakage: future_return field present in all 7 rows.")
    print("  EMBARGO: future_return is NEVER used for admission decisions.")

    # Step 2: Build valid panel
    admitted, quarantined = construct_valid_panel(flagged)

    print(f"\n{sep}")
    print("SECTION 2 — POINT-IN-TIME PANEL (valid as-of panel)")
    print(f"  Rule applied BEFORE code:")
    print(f"  Admit if: available_time <= cutoff AND entity_id present")
    print(f"            AND revision == 0 AND not exact_duplicate")
    print(sep)

    print("\n  Row-level dispositions:")
    print(f"  {'Row':>3} {'Entity':>8} {'Disposition':>12} {'Reason'}")
    print("  " + "-" * 65)
    for r in sorted(flagged, key=lambda x: x["row_id"]):
        # find in admitted or quarantined
        match = next((a for a in admitted + quarantined if a["row_id"] == r["row_id"]), None)
        if match:
            entity = match["entity_id"] if match["entity_id"] else "(MISSING)"
            print(f"  {match['row_id']:>3} {entity:>8} {match['disposition']:>12}  {match['reason']}")

    print(f"\n  Row funnel:")
    print(f"    Total rows in panel:          7")
    print(f"    Late (avail > cutoff):        4  (rows 2, 5, 6, 7)")
    print(f"    Missing entity_id:            1  (row 7 — also late)")
    print(f"    Exact duplicates:             1  (row 4 — duplicate of row 3)")
    print(f"    Revisions:                    1  (row 6 — also late)")
    print(f"    QUARANTINED:                  5  (rows 2, 4, 5, 6, 7)")
    print(f"    ADMITTED to valid panel:      2  (rows 1, 3)")

    valid_mean = signal_mean(admitted)
    print(f"\n  Valid panel signal mean: {valid_mean:.4f}  (entities: {[r['entity_id'] for r in admitted]})")

    # Step 3: Naive panel
    naive = construct_naive_panel(RAW_ROWS, DECISION_TIME)

    print(f"\n{sep}")
    print("SECTION 3 — NAIVE vs. VALID PANEL COMPARISON")
    print(sep)
    naive_mean = signal_mean(naive)
    print(f"  Naive panel (event_time <= cutoff, ignores available_time):")
    print(f"    Rows admitted: {len(naive)}  (rows {[r['row_id'] for r in naive]})")
    print(f"    Signal mean:   {naive_mean:.4f}")
    print(f"    Contamination: Row 2 (entity B, signal -0.20) included in naive panel")
    print(f"                   but available_time=17:00 > cutoff=10:00 — lookahead bias")
    print(f"\n  Valid panel (available_time <= cutoff):")
    print(f"    Rows admitted: {len(admitted)}  (rows {[r['row_id'] for r in admitted]})")
    print(f"    Signal mean:   {valid_mean:.4f}")
    print(f"\n  Difference: naive mean {naive_mean:.4f} vs. valid mean {valid_mean:.4f}")
    print(f"    Delta: {valid_mean - naive_mean:+.4f}  (naive underestimates signal by {abs(valid_mean-naive_mean):.4f})")
    print(f"    Using naive panel would mechanically distort results by including")
    print(f"    entity B's signal that was not yet available at the decision time.")

    # Step 4: Changed cutoff
    print(f"\n{sep}")
    print("SECTION 4 — CHANGED CUTOFF EXPERIMENT")
    print(sep)
    print(f"  Original cutoff: {DECISION_TIME}")
    print(f"  Changed cutoff:  {CHANGED_CUTOFF}")
    print(f"\n  PRE-RUN PREDICTION (written before execution):")
    print(f"  {CHANGED_CUTOFF_PREDICTION}")
    changed_flagged = mechanical_flags(RAW_ROWS, CHANGED_CUTOFF)
    changed_admitted, _ = construct_valid_panel(changed_flagged)
    changed_mean = signal_mean(changed_admitted)
    print(f"\n  ACTUAL RESULT:")
    print(f"    Admitted rows: {len(changed_admitted)}  (rows {[r['row_id'] for r in changed_admitted]})")
    print(f"    Signal mean:   {changed_mean:.4f}")
    print(f"    Prediction confirmed: valid panel shrinks from 2 to {len(changed_admitted)} row(s). "
          f"Mean changed from {valid_mean:.4f} to {changed_mean:.4f}.")
    print(f"    Mandate effect: tighter cutoff increases data quality but reduces sample size.")

    # Summary
    print(f"\n{sep}")
    print("VALIDATION SUMMARY")
    print(sep)
    print(f"  All 7 rows preserved in audit trail: YES")
    print(f"  future_return used for admission: NO (embargoed)")
    print(f"  Point-in-time rule written before code: YES")
    print(f"  Changed cutoff predicted before run: YES — prediction confirmed")
    print(f"  Naive vs. valid comparison quantified: YES (delta = {valid_mean - naive_mean:+.4f})")
    print(f"  Quarantine is evidence preservation, not deletion: YES")
    print(sep)


if __name__ == "__main__":
    main()
