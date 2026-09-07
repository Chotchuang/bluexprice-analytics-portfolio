# Python Analysis Validation Report

Overall assessment: Ready to share with caveats

## Question

Can a compact Python workflow validate the public demo data, compare portfolio
contribution with risk, show the impact of estimated execution costs, and test
simple models without exposing private Bluexprice logic?

## Data and method

- 720 deterministic synthetic observations across 4 generic assets
- Public SQL outputs only
- Prior-observation features; no same-row target leakage
- Chronological 70/30 train/test holdout
- Majority baseline, logistic regression, and random forest
- Simplified fixed portfolio weights, fees, and slippage

## Verified checks

- Duplicate daily keys: 0
- Missing prices: 0
- Non-positive prices: 0
- Portfolio months missing: 0
- Feature rows use observations earlier than their target row
- Model test set occurs after the training period
- Gross and net portfolio summaries reconcile with the SQL outputs

## Important caveat

The random-forest F1 score is approximately 0.99, while the majority baseline
is approximately 0.81. This is not credible evidence of real-market predictive
power. The demo generator creates simple deterministic patterns and the target
class is imbalanced toward positive observations. The result demonstrates the
evaluation workflow only.

## Sharing rule

Share the workflow, checks, charts, and limitations. Do not describe the model
score as alpha, profitability, production performance, or proof that the method
will generalize to real market data.

