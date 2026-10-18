# FIN 439 Project 1 - NIKE Investment Decision

This repository supports an equity-research decision for an investment committee with no current NIKE, Inc. (NYSE: NKE) position.

**Recommendation:** Watch/defer. Do not initiate at the September 2, 2026 close of $38.24. The supported valuation range is **$30-$49 per share**. Reconsider at or below $36.40, or when reported revenue and margin evidence supports a turnaround.

## Reproduce the visible output

No third-party Python packages are required. From the repository root:

```sh
python3 scripts/project1_summary.py
```

The command runs the linked five-year FCFE model and its one-at-a-time sensitivity suite, checks the accounting identities, and writes `outputs/project1_visible_output.json`. The output records the material inputs, as-of date, decision, valuation range, and test results without requiring a notebook or live market-data request.

## Repository map

- `scripts/project1_summary.py` - reproducible Project 1 output generator
- `proforma_nke.py` - linked five-year FCFE model and balance-sheet refusal check
- `sensitivity_nke.py` - one-at-a-time growth, gross-margin, and capex sensitivity suite
- `comps_NKE.py` - comparable-companies calculation
- `docs/` - final submission records, memo source, video scripts, and manifest
- `outputs/project1_visible_output.json` - saved visible executed output

## Sources and limitations

The principal source boundary is NIKE's FY2026 Form 10-K (filed July 15, 2026; fiscal year ended May 31, 2026) and the September 2, 2026 closing price. See `docs/decision-memo.md` and `docs/validation-and-ai-use.md` for sources, conventions, assumptions, and known limitations. The forecast is an analyst scenario, not company guidance or investment advice. No credentials or API keys are required; `.env.example` is intentionally empty.
