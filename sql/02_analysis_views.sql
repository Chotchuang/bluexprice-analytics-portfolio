DROP VIEW IF EXISTS portfolio_daily;
DROP VIEW IF EXISTS asset_returns;

CREATE VIEW asset_returns AS
WITH price_lag AS (
    SELECT
        observation_date,
        asset_id,
        close_price,
        volume,
        LAG(close_price) OVER (
            PARTITION BY asset_id
            ORDER BY observation_date
        ) AS previous_close
    FROM market_prices
)
SELECT
    observation_date,
    asset_id,
    close_price,
    volume,
    CASE
        WHEN previous_close IS NULL THEN NULL
        ELSE (close_price / previous_close) - 1
    END AS daily_return,
    AVG(close_price) OVER (
        PARTITION BY asset_id
        ORDER BY observation_date
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) AS rolling_20_observation_price
FROM price_lag;

CREATE VIEW portfolio_daily AS
SELECT
    r.observation_date,
    COUNT(*) AS asset_count,
    SUM(w.target_weight) AS total_weight,
    SUM(w.target_weight * r.daily_return) AS gross_portfolio_return,
    SUM(
        w.target_weight * r.daily_return
        - (w.target_weight * c.slippage_bps / 10000.0)
        - (c.transaction_fee / 100000.0)
    ) AS net_portfolio_return,
    SUM(c.transaction_fee) AS transaction_fees,
    SUM(w.target_weight * c.slippage_bps) AS weighted_slippage_bps
FROM asset_returns AS r
JOIN portfolio_weights AS w
  ON r.observation_date = w.observation_date
 AND r.asset_id = w.asset_id
JOIN execution_costs AS c
  ON r.observation_date = c.observation_date
 AND r.asset_id = c.asset_id
WHERE r.daily_return IS NOT NULL
GROUP BY r.observation_date;

