WITH checks AS (
    SELECT
        'duplicate price keys' AS check_name,
        COUNT(*) AS failed_rows
    FROM (
        SELECT observation_date, asset_id
        FROM market_prices
        GROUP BY observation_date, asset_id
        HAVING COUNT(*) > 1
    )

    UNION ALL

    SELECT
        'missing or non-positive prices',
        COUNT(*)
    FROM market_prices
    WHERE close_price IS NULL OR close_price <= 0

    UNION ALL

    SELECT
        'dates with portfolio weight not equal to 1',
        COUNT(*)
    FROM (
        SELECT observation_date
        FROM portfolio_weights
        GROUP BY observation_date
        HAVING ABS(SUM(target_weight) - 1.0) > 0.000001
    )

    UNION ALL

    SELECT
        'positions without matching prices',
        COUNT(*)
    FROM portfolio_weights AS w
    LEFT JOIN market_prices AS p
      ON w.observation_date = p.observation_date
     AND w.asset_id = p.asset_id
    WHERE p.asset_id IS NULL
)
SELECT
    check_name,
    failed_rows,
    CASE WHEN failed_rows = 0 THEN 'PASS' ELSE 'REVIEW' END AS status
FROM checks
ORDER BY check_name;

