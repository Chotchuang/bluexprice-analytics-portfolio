PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS portfolio_daily;
DROP VIEW IF EXISTS asset_returns;
DROP TABLE IF EXISTS execution_costs;
DROP TABLE IF EXISTS portfolio_weights;
DROP TABLE IF EXISTS market_prices;
DROP TABLE IF EXISTS assets;

CREATE TABLE assets (
    asset_id TEXT PRIMARY KEY,
    asset_group TEXT NOT NULL,
    risk_band TEXT NOT NULL,
    base_price REAL NOT NULL CHECK (base_price > 0),
    trend_rate REAL NOT NULL,
    cycle_seed INTEGER NOT NULL
);

CREATE TABLE market_prices (
    observation_date TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    close_price REAL NOT NULL CHECK (close_price > 0),
    volume INTEGER NOT NULL CHECK (volume > 0),
    PRIMARY KEY (observation_date, asset_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE portfolio_weights (
    observation_date TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    target_weight REAL NOT NULL CHECK (target_weight BETWEEN 0 AND 1),
    PRIMARY KEY (observation_date, asset_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE execution_costs (
    observation_date TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    slippage_bps REAL NOT NULL CHECK (slippage_bps >= 0),
    transaction_fee REAL NOT NULL CHECK (transaction_fee >= 0),
    PRIMARY KEY (observation_date, asset_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

INSERT INTO assets VALUES
    ('ASSET_A', 'Growth Equity', 'High',   100.0, 0.00070, 3),
    ('ASSET_B', 'Quality Equity', 'Medium', 80.0, 0.00045, 5),
    ('ASSET_C', 'Defensive Equity', 'Low',  60.0, 0.00025, 7),
    ('ASSET_D', 'Diversifier', 'Medium',    40.0, 0.00035, 9);

WITH RECURSIVE calendar(day_number, observation_date) AS (
    SELECT 0, DATE('2025-01-01')
    UNION ALL
    SELECT day_number + 1, DATE(observation_date, '+1 day')
    FROM calendar
    WHERE day_number < 179
)
INSERT INTO market_prices (observation_date, asset_id, close_price, volume)
SELECT
    c.observation_date,
    a.asset_id,
    ROUND(
        a.base_price
        * (1 + c.day_number * a.trend_rate)
        * (1 + (((c.day_number * a.cycle_seed) % 19) - 9) * 0.0015),
        4
    ) AS close_price,
    800000 + ((c.day_number * a.cycle_seed * 7919) % 600000) AS volume
FROM calendar AS c
CROSS JOIN assets AS a;

INSERT INTO portfolio_weights (observation_date, asset_id, target_weight)
SELECT
    observation_date,
    asset_id,
    CASE asset_id
        WHEN 'ASSET_A' THEN 0.35
        WHEN 'ASSET_B' THEN 0.30
        WHEN 'ASSET_C' THEN 0.20
        WHEN 'ASSET_D' THEN 0.15
    END AS target_weight
FROM market_prices;

INSERT INTO execution_costs (
    observation_date,
    asset_id,
    slippage_bps,
    transaction_fee
)
SELECT
    observation_date,
    asset_id,
    2.0 + (CAST(STRFTIME('%d', observation_date) AS INTEGER) % 4),
    0.75 + (CAST(STRFTIME('%m', observation_date) AS INTEGER) * 0.05)
FROM market_prices;

