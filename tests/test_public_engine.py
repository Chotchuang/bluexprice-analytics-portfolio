"""Tests for public engine proof — lookahead, commitment, friction."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from public_engine.backtester.engine import EventDrivenEngine
from public_engine.backtester.execution import ExecutionConfig, simulate_fill
from public_engine.live.records import LiveRecorder, signal_sha256, verify_signal_sha256
from public_engine.strategies.base import BarSeries, Signal, Strategy
from public_engine.strategies.mock import MockMomentumStrategy


class PeekFutureStrategy(Strategy):
    """If engine allows lookahead, final bar return is known at bar 0."""

    def on_bar(self, bars: BarSeries, bar_index: int) -> Signal:
        if bar_index == 0 and len(bars.close) > 2:
            future = bars.close.iloc[-1] / bars.close.iloc[0] - 1
            if future > 0.5:
                return Signal(1.0, "peek")
        return Signal(0.0, "flat")


def _toy_ohlcv() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=5, freq="B")
    close = pd.Series([100.0, 101.0, 102.0, 103.0, 200.0], index=dates)
    return pd.DataFrame(
        {
            "Open": close.shift(1).fillna(close.iloc[0]),
            "High": close * 1.01,
            "Low": close * 0.99,
            "Close": close,
            "Volume": [1e6] * 5,
        },
        index=dates,
    )


def test_no_lookahead_blocks_future_peek():
    """Strategy that would peek the final spike must not trade early."""
    engine = EventDrivenEngine(initial_cash=10_000.0)
    result = engine.run(_toy_ohlcv(), PeekFutureStrategy())
    assert not result.trades


def test_momentum_runs_without_error():
    dates = pd.date_range("2023-01-01", periods=80, freq="B")
    rng = np.random.default_rng(1)
    close = 50 * np.cumprod(1 + rng.normal(0, 0.01, len(dates)))
    df = pd.DataFrame(
        {
            "Open": close,
            "High": close * 1.01,
            "Low": close * 0.99,
            "Close": close,
            "Volume": np.full(len(dates), 2e6),
        },
        index=dates,
    )
    engine = EventDrivenEngine()
    result = engine.run(df, MockMomentumStrategy(lookback=10))
    assert result.metrics["n_bars"] == len(dates)
    assert "sharpe" in result.metrics


def test_slippage_increases_buy_price():
    fill = simulate_fill("BUY", 100.0, 1000.0, 1e7, ExecutionConfig(slippage_bps=10))
    assert fill.fill_price > 100.0
    assert fill.slippage_bps_applied == 10.0


def test_capacity_rejects_oversized_order():
    fill = simulate_fill("BUY", 100.0, 1_000_000.0, 1000.0, ExecutionConfig(max_participation=0.05))
    assert fill.rejected
    assert fill.reject_reason == "capacity_exceeded"


def test_signal_hash_stable():
    payload = {"asset": "DEMO", "target_weight": 0.1, "t": "2026-08-29T00:00:00Z"}
    h1 = signal_sha256(payload)
    h2 = signal_sha256(dict(sorted(payload.items())))
    assert h1 == h2
    assert verify_signal_sha256(payload, h1)


def test_live_recorder_append_only(tmp_path: Path):
    rec = LiveRecorder(tmp_path)
    from public_engine.live.records import LiveRecord

    r = LiveRecord(
        timestamp="2026-08-29T12:00:00Z",
        asset="DEMO",
        action="HOLD",
        target_weight=0.0,
        execution_price_simulated=100.0,
        slippage_bps_applied=0.0,
        transaction_fee_usd=0.0,
        signal_sha256="abc",
    )
    path = rec.append(r, filename="test.jsonl")
    rec.append(r, filename="test.jsonl")
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    row = json.loads(lines[0])
    assert row["asset"] == "DEMO"
