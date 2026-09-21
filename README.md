# Bluexprice — Market-Price Analytics for Portfolio Allocation

Status: In Development  
Purpose: Public portfolio demonstration  
Scope: Research and analytical engineering, not investment advice

## Project overview

Bluexprice explores how market-price data can be turned into structured
portfolio decisions. The project combines exploratory data analysis, portfolio
risk measurement, backtesting controls, and machine-learning experiments.

This public repository demonstrates the analytical pipeline and validation
approach without publishing the private signal formulas used in the main
research system.

## Business question

How can an analyst compare market-price behaviour, portfolio risk, and model
quality before turning a research signal into a portfolio recommendation?

## What this repository demonstrates

- A modular event-driven backtesting engine
- Next-bar execution to reduce look-ahead bias
- Transaction fees, slippage, and capacity checks
- Portfolio risk and performance summaries
- Mock strategies used only for public demonstration
- Tests for leakage, future-data access, and execution assumptions
- Reproducible demo outputs and an audit-friendly live-record format

## Public analytical pipeline

```text
Demo / synthetic market-price data
    -> data-quality checks
    -> exploratory analysis
    -> cue families A–E (public nicknames only)
    -> review filters (pass / hold / fail)
    -> decision labels (Buy / Sell / Wait / Hold / Warning) + intensity
    -> portfolio risk monitoring
    -> recommendation and next review
```

Private research formulas stay in Quant and are not copied here.

## Current public output

- `public_engine/reports/output/demo_tear_sheet.html`
- `public_engine/reports/output/demo_metrics.json`
- `public_engine/live_records/live.jsonl`

All current outputs use demo inputs or mock strategies. They are not evidence
of live investment performance.

## Case study

The local [case study](CASE_STUDY.md) leads with the **decision
pipeline** (cue families A–E → filters/gates → Buy/Sell/Wait/Hold/Warning
labels), then portfolio risk, quality, and an optional rejected model. Open the
local HTML review:

[`reports/decision-review/decision-dashboard.html`](reports/decision-review/decision-dashboard.html)

Aggregate CSVs: [`data/tableau_exports/`](data/tableau_exports/).

This local material is separate from the portfolio website and Tableau Public.

## SQL analysis

The [`sql/`](sql/) section shows practical analytical SQL: relational tables,
data-quality checks, joins, CTEs, rolling windows, ranking, portfolio-cost
analysis, and Tableau-ready summary outputs. It uses deterministic demo data
and does not contain private market signals.

## Python analysis

The [`python_analysis/`](python_analysis/) section extends the SQL outputs with
data validation, exploratory summaries, contribution-versus-risk analysis,
chronological model comparison, and reader-ready charts. The executed
[`notebook`](notebooks/bluexprice_python_eda.ipynb) documents the analysis from
inputs to takeaways.

## Quick start

```bash
python -m pip install -r requirements.txt
python -m public_engine.scripts.run_mock_backtest --symbol DEMO
bash scripts/run_python_analysis.sh
pytest -q
```

## Public/private boundary

The private Bluexprice research repository contains proprietary signal logic,
feature recipes, and model-development work. Those materials are intentionally
excluded here. The public boundary is documented in
[`public_engine/PAYLOAD_CONTRACT.md`](public_engine/PAYLOAD_CONTRACT.md).

## Development approach

AI-assisted development was used for parts of the implementation. The project
owner defines the analytical questions, reviews the outputs, tests the logic,
interprets the results, and controls what is suitable for public disclosure.

## Roadmap

1. Build and review the Tableau Public dashboard from sanitized summary tables.
2. Finalize the case study after dashboard QA.
3. Connect the approved case study to the portfolio website.

## Limitations

- The project is still in development.
- Public strategies are intentionally simple mock examples.
- Historical or simulated results do not guarantee future performance.
- Machine-learning scores are model-evaluation evidence, not profitability proof.
