# Bluexprice — Market-Price Analytics for Portfolio Allocation

Status: In Development · Local case materials only
Evidence: Deterministic synthetic aggregates shaped like the research decision stack
Focus: Decision pipeline → filters/gates → action labels → portfolio monitoring

> In Development — research and portfolio demonstration. Not investment advice,
> not live trading performance, and not a production system.

## Executive Summary (60–90 seconds)

1. **The product of this project is a decision review, not a price chart.** Market-price cues are grouped into public families A–E, passed through filters/gates, then labeled as Buy, Sell, Wait Buy, Wait Sell, Hold, Warning Long, or Warning Short (with intensity 1/3 · 2/3 · 3/3).
2. **December 2025 (synthetic) was cautious:** Hold led the month; Warning Long/Short stayed active; filter pass rate was about **61.7%**. The stack prefers waiting when families conflict.
3. **Portfolio risk still needs a human review.** Cumulative indexed return finished about **−12.5%** versus **−2.6%** for the benchmark. Growth held ~**33.6%** of the book but ~**59.9%** of risk.
4. **Quality passed; the optional model did not.** 12/12 documented quality checks passed. Logistic regression underperformed the majority baseline (0.455 vs 0.500 balanced accuracy) and was **rejected**.
5. **Recommended next step:** monitor Wait versus Buy/Sell each month, investigate filter fails before allocation talk, and review Growth concentration — without claiming a trade.

## Business Problem

Investors and operators see many market-price cues. Without a structured review,
it is easy to jump from a chart to a conclusion. The business problem is:

> How do we turn many market-price cues into a small set of plain-language
> decisions — Buy / Sell / Wait / Hold / Warning — that a non-specialist can
> read, challenge, and monitor?

Secondary questions:

- Which cue families are active this period?
- Did review filters pass, hold, or fail?
- Is portfolio risk concentrated while decisions stay cautious?
- Is the evidence trustworthy enough to recommend anything?

## Analytical Objective

Show a repeatable analyst workflow that:

1. Validates data quality first.
2. Scores public cue families (A–E nicknames only — no private formulas).
3. Applies review filters/gates.
4. Assigns decision labels and intensity bands.
5. Aggregates monthly counts for monitoring.
6. Connects decisions to portfolio risk and a clear recommendation.
7. Treats machine learning as an optional experiment that can be rejected.

## Data and Scope

Public package uses **synthetic monthly aggregates** only. Daily private series,
exact formulas, feature recipes, and internal column ids are excluded (C-20).

| Public table | Role |
|---|---|
| `decision_action_summary.csv` | Counts of decision labels × intensity × filter result × cue family |
| `decision_pipeline_stages.csv` | Seven public stages from question → monitoring |
| `portfolio_performance_summary.csv` | Indexed/benchmark/net return, volatility, drawdown |
| `asset_allocation_summary.csv` | Contribution to return/risk, concentration |
| `data_quality_summary.csv` | Trust gate |
| `statistical_summary.csv` | Distribution context |
| `model_evaluation_summary.csv` | Optional prototype vs baseline |
| `analytics_pipeline.csv` | Ten-stage analyst workflow (includes decision filter stage) |
| `data_dictionary.csv` | Field definitions |

Local visual: [`reports/decision-review/decision-dashboard.html`](reports/decision-review/decision-dashboard.html)

## Decision Pipeline

```text
Market-price data
  → clean & quality gate
  → cue families A–E (public nicknames)
  → review filters (pass / hold / fail)
  → decision labels + intensity
  → monthly aggregate dashboard
  → recommendation & monitoring
```

### Public cue families (nicknames only)

| Code | Public name |
|---|---|
| A | Short-cycle structure |
| B | Fast confirmation |
| C | Consistency cross-check |
| D | Distance warning band |
| E | Multi-horizon context |

Private formula names and CSV flag ids are intentionally omitted.

### Decision vocabulary (star lexicon)

Buy · Sell · Wait Buy · Wait Sell · Hold · Warning Long · Warning Short
Intensity: **1/3 ≈ 33% · 2/3 ≈ 66% · 3/3 = 100%**

### Synthetic December 2025 decision mix

| Decision label | Count |
|---|---:|
| Hold | 13 |
| Warning Short | 10 |
| Warning Long | 9 |
| Buy | 8 |
| Wait Sell | 8 |
| Wait Buy | 7 |
| Sell | 5 |

Filter gates (Dec): pass 37 · hold 16 · fail 7 → **pass rate ≈ 61.7%**

Full-year synthetic mix (for monitoring shape): Hold 208 · Wait Buy 116 · Wait Sell 116 · Warning Long 83 · Warning Short 81 · Buy 68 · Sell 48 · year pass rate ≈ **62%**.

## Data Quality Before Decisions

All **12/12** documented quality checks passed (duplicates, missing values,
invalid prices/weights, reconciliation, freshness, and key uniqueness).

Quality failure would stop the decision dashboard refresh — performance talk
comes second.

## Portfolio and Risk Context

December 2025 synthetic snapshot:

- Indexed return (YTD): **−12.5%** vs benchmark **−2.6%**
- Monthly net return: **−3.2%**
- Volatility: **12.8%** (annualized from daily synthetic returns in-month)
- Maximum drawdown (month): **−3.2%**
- Growth: **33.6%** share · **59.9%** of risk · **−1.4 pp** return contribution

Interpretation: cautious decision labels + concentrated Growth risk → review
concentration and Wait/Warning trends before changing the book.

## Machine Learning (supporting only)

Chronological 70/30 holdout on synthetic features:

| Model | Balanced accuracy | Status |
|---|---:|---|
| Majority baseline | 0.500 | reference |
| Logistic regression | 0.455 | **rejected** |

Keeping the negative result is intentional. A prototype does not earn influence
until it beats a transparent baseline without leakage.

## Dashboard Communication

Three pages (HTML local; Tableau workbook not required for this package):

1. **Decision Overview** — labels, intensity, filter pass/hold/fail, cue families
2. **Portfolio & Risk** — return vs benchmark, contribution, concentration
3. **Validation & Pipeline** — quality, model literacy, decision stages

Reading order: Page 1 insight → recommendation → Page 2/3 for context.

## Recommendation and Monitoring

1. Treat Hold / Wait / Warning dominance as a feature of the review design, not a bug.
2. Each month, chart Wait Buy+Wait Sell versus Buy+Sell and the filter pass rate.
3. Investigate filter fails before discussing allocation changes.
4. Review Growth when risk contribution stays far above portfolio share.
5. Keep rejected models out of the decision path until validation improves.
6. Refresh only after quality checks pass.

## Limitations

- Synthetic demonstration data shaped like the research language — not live P&L.
- Public nicknames for cue families — not the private research implementation.
- No broker orders, no investment advice, no claim of alpha.
- Tableau Public and website publication are out of scope for this local package.

## What This Case Demonstrates

- Framing a business problem into a decision pipeline
- Filter/gate thinking before action labels
- Plain-language decision communication for non-technical readers
- SQL/Python-ready analyst workflow and data-quality discipline
- Portfolio risk context that supports monitoring recommendations
- Honest model evaluation (including rejection)
- Clear public/private boundary for proprietary research

## Paths

- Quant source of truth: the separate Quant research workspace
- Aggregate exports: `data/tableau_exports/`
- Contract: `docs/portfolio/BLUEXPRICE_PUBLIC_DATA_CONTRACT.md`
- This case folder: repository root
