# Video 2 Recording Cue Sheet — NIKE Codebase Walkthrough

Use this while recording. It is a speaking guide, not the final corrected transcript. The final transcript must be made after the recording so it matches the actual audio and timestamps.

## Before starting OBS

1. Open VS Code in the `TICKER-research` folder.
2. Open these tabs: `README.md`, `outputs/project1_visible_output.json`, `proforma_nke.py`, and `sensitivity_nke.py`.
3. Open Terminal and paste this command. Press Enter before recording:

```sh
cd "/Users/wgdeary/FIN439 work folder/TICKER-research"
```

4. Copy this command to your clipboard before recording. Do not run it yet:

```sh
python3 scripts/project1_summary.py
```

5. Also copy this command somewhere easy to select, such as a TextEdit note or the line below. It will be used later:

```sh
python3 proforma_nke.py
```

## Read this while recording

**[README.md visible]**

Hi, this is my FIN 439 Project 1 codebase walkthrough for NIKE. This repository is a reproducible valuation package. The README gives the decision, source boundary, run command, and limitations. My conclusion is Watch/Defer, with a supported range of $30 to $49 per share.

**[Terminal visible — paste and run `python3 scripts/project1_summary.py`]**

A clean user can reproduce the result with this command. It uses no third-party packages, credentials, or live data request. It runs the linked model and sensitivity suite and writes the visible output.

**[Open `outputs/project1_visible_output.json`]**

This output shows the as-of date, $38.24 market price, recommendation, valuation range, reconsideration conditions, accounting check, and sensitivity results. The base FCFE value is $30.19 per share.

**[Open `proforma_nke.py`]**

The core model is in proforma_nke.py. Revenue and gross margin determine gross profit. SG&A and depreciation determine EBIT. The model then updates inventory, PP&E, debt, equity, cash, and FCFE. The valuation is based on linked financial statements, not disconnected assumptions.

**[Terminal visible — paste and run `python3 proforma_nke.py`]**

This command also runs the deliberate break test. It forces FY2027 cash to opening cash rather than the linked cash value. The model raises a ValueError for a $757.2 million balance-sheet gap. This is an expected pass because the model refuses to value an unbalanced balance sheet.

**[Open `sensitivity_nke.py`, then return to the JSON output]**

This file tests revenue growth, gross margin, and capex sensitivity using clean base inputs for each run. The most material result is capex: value is $32.60 per share at 1 percent of revenue and $27.79 at 2 percent. That $4.81 difference shows that cash conversion is a major risk.

The main limitation is that 79.9 percent of the FCFE base value comes from terminal value, and the recovery assumptions are analyst judgments. This is why the conclusion remains Watch/Defer. Thank you.
