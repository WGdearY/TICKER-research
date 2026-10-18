# Video 2 Script Codebase Walkthrough

**Target duration:** 4 minutes 30 seconds. Record this as a script, then correct the generated transcript after recording.

This repository is a reproducible NIKE Project 1 valuation package. The README gives the decision, setup, run command, source boundary, and limitations. The final visible result is stored in `outputs/project1_visible_output.json`; it includes the as-of date, market price, recommendation, range, and model checks without requiring the grader to run code.

The core model is `proforma_nke.py`. It forecasts revenue, gross profit, SG&A, depreciation, interest, taxes, working capital, capex, debt repayment, cash, and FCFE across FY2027 through FY2031. The key financial logic is the linked relationship: revenue and gross margin determine gross profit; SG&A and depreciation determine EBIT; the balance sheet updates inventory, PP&E, other operating assets, debt, and equity; then FCFE and the cash plug complete the model. The script refuses to value an unbalanced model.

The deliberate break test is important. When I force FY2027 cash to opening cash instead of the linked cash value, the model throws a ValueError for a $757.2 million balance-sheet gap. This confirms the model does not silently value broken statements.

`sensitivity_nke.py` imports the same linked logic and uses deep copies of the input dictionary so each sensitivity starts clean. It tests revenue growth plus or minus one percentage point, gross margin plus or minus one percentage point, and capex from 1% to 2% of revenue. It runs every case through the balance-sheet check and reruns the base case at the end to confirm no state contamination.

The highest-risk financial claim is that the turnaround creates cash value, not merely accounting earnings. The capex test addresses that risk. At 1% of revenue, value is $32.60 per share; at 2%, it falls to $27.79. That $4.81 span is larger than the tested gross-margin or revenue spans, so it supports the watch/defer posture.

Finally, `scripts/project1_summary.py` executes the sensitivity suite and writes the self-contained JSON output. It requires only Python standard library modules and the repository source files. The known limitations are that the model has a 79.9% terminal-value share and that its operating recovery assumptions are analyst judgments, not company guidance.
