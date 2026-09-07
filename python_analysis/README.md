# Python EDA and Model Exploration

This analysis uses Python to turn the public SQL outputs into a small,
decision-ready portfolio review.

## Questions answered

1. Are the inputs complete enough to analyse?
2. How large is the difference between gross and cost-adjusted demo results?
3. Which assets contribute more return, and what risk accompanies them?
4. Can simple models beat a majority-class baseline on the synthetic data?

## Skills demonstrated

- Loading and validating structured data with pandas
- Exploratory summaries and grouped analysis
- Feature construction using prior observations only
- Chronological train/test separation
- Baseline, logistic-regression, and random-forest comparison
- Clear charts and reusable CSV outputs
- Business interpretation with explicit limitations

Run the analysis:

```bash
bash scripts/run_python_analysis.sh
```

Open the executed notebook at
`notebooks/bluexprice_python_eda.ipynb` for the reader-facing walkthrough.

## Scope

This is applied analyst-level Python. It demonstrates that the author can use
Python to structure a question, inspect data, compare methods, validate an
output, and communicate a result. It does not claim specialist machine-learning
engineering or production model ownership.

