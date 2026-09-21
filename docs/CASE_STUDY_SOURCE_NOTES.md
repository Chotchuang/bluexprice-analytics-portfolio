# Bluexprice Case Study — Source and QA Notes

Updated: 2026-09-07
Status: Local full package with decision layer

## Reporting job

- Audience: readers interested in product operations, data analysis, and business analysis
- Success: a first-time reader understands decision pipeline → evidence → recommendation in 60–90 seconds
- Gap closed vs prior draft: prior case showed generic DA skills only; this revision leads with decision labels and filters

## Approved evidence

Quant exports (copied to `data/tableau_exports/`):

- `decision_action_summary.csv`
- `decision_pipeline_stages.csv`
- `portfolio_performance_summary.csv`
- `asset_allocation_summary.csv`
- `statistical_summary.csv`
- `data_quality_summary.csv`
- `model_evaluation_summary.csv`
- `analytics_pipeline.csv`
- `data_dictionary.csv`

Contract / spec:

- Quant research workspace contract and dashboard specification

Visual:

- `reports/decision-review/decision-dashboard.html`

## Claim boundaries

- Synthetic demonstration shaped like research vocabulary — not live P&L
- Public cue-family nicknames only
- No private formulas, feature recipes, or internal CSV flag ids
- Website publication is outside the scope of this local package
