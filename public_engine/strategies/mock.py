"""Baseline mock strategies for public proof."""

from __future__ import annotations

import pandas as pd

from public_engine.strategies.base import BarSeries, Signal, Strategy


class MockMomentumStrategy(Strategy):
    """Long if N-day return > 0 else flat. Public baseline only."""

    def __init__(self, lookback: int = 20) -> None:
        self.lookback = lookback

    def on_bar(self, bars: BarSeries, bar_index: int) -> Signal:
        if bar_index < self.lookback:
            return Signal(0.0, "warmup")
        close = bars.close.iloc[: bar_index + 1]
        ret = close.iloc[-1] / close.iloc[-1 - self.lookback] - 1.0
        weight = 1.0 if ret > 0 else 0.0
        return Signal(weight, f"momentum_{self.lookback}d")


class MockSmaCrossStrategy(Strategy):
    """Fast/slow SMA cross — public baseline."""

    def __init__(self, fast: int = 10, slow: int = 30) -> None:
        self.fast = fast
        self.slow = slow

    def on_bar(self, bars: BarSeries, bar_index: int) -> Signal:
        need = max(self.fast, self.slow)
        if bar_index < need:
            return Signal(0.0, "warmup")
        close = bars.close.iloc[: bar_index + 1]
        fast_ma = close.rolling(self.fast).mean().iloc[-1]
        slow_ma = close.rolling(self.slow).mean().iloc[-1]
        weight = 1.0 if fast_ma > slow_ma else 0.0
        return Signal(weight, "sma_cross")


class MockNoiseStrategy(Strategy):
    """Deterministic pseudo-noise for stress tests (seeded)."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def on_bar(self, bars: BarSeries, bar_index: int) -> Signal:
        import hashlib

        key = f"{self.seed}:{bar_index}".encode()
        h = int(hashlib.sha256(key).hexdigest()[:8], 16)
        weight = 1.0 if h % 2 == 0 else 0.0
        return Signal(weight, "noise")
