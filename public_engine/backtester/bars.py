"""OHLCV view for strategies — caps history at bar_index."""

from __future__ import annotations

import pandas as pd


class BarsView:
    """Slice of OHLCV through bar_index inclusive (no future bars)."""

    def __init__(self, df: pd.DataFrame, bar_index: int) -> None:
        self._df = df.iloc[: bar_index + 1]

    @property
    def close(self) -> pd.Series:
        return self._df["Close"]

    @property
    def open(self) -> pd.Series:
        return self._df["Open"]

    @property
    def high(self) -> pd.Series:
        return self._df["High"]

    @property
    def low(self) -> pd.Series:
        return self._df["Low"]

    @property
    def volume(self) -> pd.Series:
        return self._df["Volume"]

    def __len__(self) -> int:
        return len(self._df)
