-- Question 1: Which assets show the strongest recent market-price trend?
WITH latest_date AS (
    SELECT MAX(observation_date) AS observation_date
    FROM asset_returns
),
recent_prices AS (
    SELECT
        r.asset_id,
        a.asset_group,
        a.risk_band,
        r.close_price,
        r.rolling_20_observation_price,
        (r.close_price / r.rolling_20_observation_price) - 1 AS price_vs_rolling_average
    FROM asset_returns AS r
    JOIN assets AS a ON r.asset_id = a.asset_id
    JOIN latest_date AS d ON r.observation_date = d.observation_date
)
SELECT
    asset_id,
    asset_group,
    risk_band,
    ROUND(close_price, 2) AS close_price,
    ROUND(price_vs_rolling_average * 100, 2) AS price_vs_rolling_average_pct,
    DENSE_RANK() OVER (
        ORDER BY price_vs_rolling_average DESC
    ) AS market_price_rank
FROM recent_prices
ORDER BY market_price_rank;

-- Question 2: What did the portfolio produce each month after estimated costs?
SELECT
    STRFTIME('%Y-%m', observation_date) AS month,
    COUNT(*) AS observation_days,
    ROUND(SUM(gross_portfolio_return) * 100, 2) AS gross_return_sum_pct,
    ROUND(SUM(net_portfolio_return) * 100, 2) AS net_return_sum_pct,
    ROUND(SUM(transaction_fees), 2) AS transaction_fees,
    ROUND(AVG(weighted_slippage_bps), 2) AS average_weighted_slippage_bps
FROM portfolio_daily
GROUP BY STRFTIME('%Y-%m', observation_date)
ORDER BY month;

-- Question 3: How did each asset contribute to return and risk by month?
WITH monthly_asset AS (
    SELECT
        STRFTIME('%Y-%m', r.observation_date) AS month,
        r.asset_id,
        a.asset_group,
        AVG(w.target_weight) AS average_weight,
        SUM(r.daily_return) AS return_sum,
        AVG(r.daily_return) AS average_daily_return,
        AVG(r.daily_return * r.daily_return) AS average_squared_return
    FROM asset_returns AS r
    JOIN portfolio_weights AS w
      ON r.observation_date = w.observation_date
     AND r.asset_id = w.asset_id
    JOIN assets AS a ON r.asset_id = a.asset_id
    WHERE r.daily_return IS NOT NULL
    GROUP BY STRFTIME('%Y-%m', r.observation_date), r.asset_id, a.asset_group
)
SELECT
    month,
    asset_id,
    asset_group,
    ROUND(average_weight * 100, 2) AS average_weight_pct,
    ROUND(return_sum * 100, 2) AS return_sum_pct,
    ROUND(average_weight * return_sum * 100, 2) AS contribution_to_return_pct,
    ROUND(
        SQRT(MAX(average_squared_return - average_daily_return * average_daily_return, 0))
        * SQRT(252) * 100,
        2
    ) AS annualized_volatility_pct
FROM monthly_asset
ORDER BY month, contribution_to_return_pct DESC;

