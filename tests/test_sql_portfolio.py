from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _build_demo_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript((ROOT / "sql/01_setup_demo.sql").read_text())
    connection.executescript((ROOT / "sql/02_analysis_views.sql").read_text())
    return connection


def test_demo_data_has_expected_grain() -> None:
    connection = _build_demo_database()
    rows = connection.execute("SELECT COUNT(*) FROM market_prices").fetchone()[0]
    unique_keys = connection.execute(
        "SELECT COUNT(*) FROM ("
        "SELECT observation_date, asset_id FROM market_prices "
        "GROUP BY observation_date, asset_id)"
    ).fetchone()[0]
    assert rows == 180 * 4
    assert unique_keys == rows


def test_portfolio_weights_sum_to_one() -> None:
    connection = _build_demo_database()
    failed_dates = connection.execute(
        "SELECT COUNT(*) FROM ("
        "SELECT observation_date FROM portfolio_weights "
        "GROUP BY observation_date "
        "HAVING ABS(SUM(target_weight) - 1.0) > 0.000001)"
    ).fetchone()[0]
    assert failed_dates == 0


def test_portfolio_view_has_cost_adjusted_returns() -> None:
    connection = _build_demo_database()
    row = connection.execute(
        "SELECT gross_portfolio_return, net_portfolio_return "
        "FROM portfolio_daily LIMIT 1"
    ).fetchone()
    assert row is not None
    assert row[1] < row[0]

