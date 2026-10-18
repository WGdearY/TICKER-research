# Project 1 Validation and AI Use Record

## Decision version and boundary

**Target:** NIKE, Inc. (NYSE: NKE)  
**Decision:** Watch/defer a new 12-month position.  
**As-of boundary:** FY2026 Form 10-K filed July 15, 2026; September 2, 2026 regular-session close of $38.24.  
**Reproducible run:** `python3 scripts/project1_summary.py`; no third-party package, credential, or live request is required.

## Data and convention ledger

| Material input | Source | As-of | Definition and treatment | Risk |
|---|---|---|---|---|
| Revenue | FY2026 10-K, income statement | May 31, 2026 | $46,398m historical forecast base | Recovery differs from reported results. |
| Cash and short-term investments | FY2026 10-K, balance sheet | May 31, 2026 | $9,027m; added in enterprise-to-equity bridge | Some cash may be operational. |
| Debt | FY2026 10-K, Note 6 | May 31, 2026 | $7,942m current plus long-term debt; subtracted in bridge | Book and market values may differ. |
| Diluted shares | FY2026 10-K, Note 10 | FY2026 | 1,481.0m weighted-average shares used for modeled per-share values | Different from point-in-time shares outstanding. |
| Market price | Historical price tables, cross-checked | Sep. 2, 2026 | $38.24 regular-session close | Non-primary market-data source; outside the filing date. |

## Validation register

| Claim or output | Failure mode | Test and expected direction | Actual result | Disposition |
|---|---|---|---|---|
| Linked pro-forma | Accounting identity fails | Assets less liabilities and equity must equal zero each forecast year. | 0.0 in FY2027-FY2031. | Pass. |
| Refusal control | Model values an unbalanced statement | Force FY2027 cash to opening cash; model should refuse. | Raises `ValueError` with a $757.2m gap. | Pass. |
| Sensitivity isolation | Inputs contaminate the base case | Rerun base after all cases; outputs should match initial base. | FY2031 EBIT $4,965.0m, FCFE $2,984.5m, value $30.19 both times. | Pass. |
| Market bridge | Share convention hides a mismatch | Point-in-time shares should approximate market price; weighted-average shares may differ. | $39.13 bridge cross-check versus $39.06 August 31 close. | Pass with convention difference disclosed. |
| Valuation range | One method creates false precision | Preserve differing methods rather than average them. | FCFE base $30.19, FCFF recovery $48.53, comps median $45.55. | Range set at $30-$49; no mechanical average. |

## Locked changed-input record preserved from the pre-run sensitivity evidence

This record is preserved from `sensitivity_0929_NKE.md`; it is not recreated after the fact. The document records a pre-run timestamp of **2026-09-29T14:10:45-04:00** and a baseline commit identifier of **41f5beb**. That identifier is retained as historical evidence even though it is not available in the current cloned history.

| Precommit time | Material input | Old to new value | Human prediction before run | Expected decision effect |
|---|---|---|---|---|
| 2026-09-29T14:10:45-04:00 | Gross-margin trajectory | Base to +1.0 percentage point in every forecast year | EBIT, FCFE, and value should rise; FY2031 FCFE was expected to rise about $107m and value about $1.07 per share because no additional working capital or capex is required. | Support the recovery case but not remove the need for conditions. |

| Before/after output | Actual decision effect | Reconciliation | Evidence |
|---|---|---|---|
| FY2031 EBIT $4,965.0m to $5,093.6m; FY2031 FCFE $2,984.5m to $3,091.6m; value $30.19 to $31.26. | No action change: watch/defer remains. | Direction and expected FCFE/value magnitude matched the preserved prediction. | `../sensitivity_0929_NKE.md`, Locked Changed-Input Record and sensitivity table. |

## Named AI-use register

| Tool/model surface | Interaction date | Material task | Independent check | Disposition and effect |
|---|---|---|---|---|
| Codex / GPT-5 | Sep.-Oct. 2026 | Organize filing facts, create draft documentation, and surface model-check ideas. | FY2026 10-K, source ledger, arithmetic, and executable model results. | Modified/accepted only where reconciled; supports documentation, not the decision by itself. |
| Web research through Codex | Sep. 2026 | Locate primary filing and historical-price references. | SEC filing is primary; price was cross-checked. | Accepted with the stated as-of boundary. |

## Limitations and monitoring

Do not initiate until the $36.40 price trigger or reported recovery evidence is met. Re-run the analysis after each quarterly filing. Escalate if NIKE Direct or Greater China weakens, if EBIT-margin recovery lags the model, or if the cash classification changes.
