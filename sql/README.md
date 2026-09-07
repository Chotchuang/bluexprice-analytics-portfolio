# SQL Portfolio Analysis

This section demonstrates practical SQL used to answer portfolio-analysis
questions. It is intentionally scoped as applied analytical work rather than
database engineering.

## Business questions

1. Are the demo inputs complete, unique, and internally consistent?
2. Which assets show the strongest recent market-price trend?
3. What did the portfolio produce before and after estimated execution costs?
4. Which assets contributed most to portfolio return and risk?

## SQL techniques demonstrated

- Relational table design and constraints
- Joins across prices, weights, costs, and asset reference data
- Common table expressions (CTEs)
- `LAG`, rolling windows, and ranking functions
- Conditional data-quality checks
- Monthly aggregation and contribution analysis
- Reproducible CSV outputs for later Tableau work

## Run

```bash
bash scripts/run_sql_analysis.sh
```

The command rebuilds a local SQLite database and refreshes the CSV files under
`data/`. All records are deterministic demo data; no private Bluexprice data or
signal formulas are used.

## Interpretation boundary

The return fields are simple sums of daily demo returns for an educational
comparison. They are not a production performance claim. The SQL layer exists
to demonstrate how analytical questions, data validation, and decision-ready
tables can be connected clearly.

