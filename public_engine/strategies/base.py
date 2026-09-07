"""Abstract strategy — no Blueprice imports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class BarSeries(Protocol):
    """OHLCV history available up to and including the signal bar."""

    @property
    def close(self) -> pd.Series: ...

    @property
    def open(self) -> pd.Series: ...

    @property
    def high(self) -> pd.Series: ...

    @property
    def low(self) -> pd.Series: ...

    @property
    def volume(self) -> pd.Series: ...


@dataclass(frozen=True)
class Signal:
    """Target portfolio weight in [-1, 1] at decision bar close."""

    target_weight: float
    reason: str = "mock"


class Strategy(ABC):
    @abstractmethod
    def on_bar(self, bars: BarSeries, bar_index: int) -> Signal:
        """Compute signal using data up to bar_index inclusive."""
