"""Event-driven backtester — signal at T, execute at T+1 (anti-lookahead)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from public_engine.backtester.bars import BarsView
from public_engine.backtester.execution import ExecutionConfig, simulate_fill
from public_engine.backtester.risk import clip_weight
from public_engine.backtester.statistics import summarize_backtest
from public_engine.strategies.base import Strategy


@dataclass
class BacktestResult:
    equity: pd.Series
    trades: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


class EventDrivenEngine:
    """
    Bar loop:
    - Strategy sees history through bar i (close i known)
    - Order fills at bar i+1 open (no peek at i+1 close when deciding)
    """

    def __init__(
        self,
        initial_cash: float = 100_000.0,
        execution: ExecutionConfig | None = None,
    ) -> None:
        self.initial_cash = initial_cash
        self.execution = execution or ExecutionConfig()

    def run(self, ohlcv: pd.DataFrame, strategy: Strategy) -> BacktestResult:
        required = {"Open", "High", "Low", "Close", "Volume"}
        missing = required - set(ohlcv.columns)
        if missing:
            raise ValueError(f"OHLCV missing columns: {missing}")

        df = ohlcv.copy()
        cash = self.initial_cash
        shares = 0.0
        equity_rows: list[tuple[pd.Timestamp, float]] = []
        trades: list[dict[str, Any]] = []
        pending_weight: float | None = None

        for i in range(len(df)):
            ts = df.index[i]
            close = float(df["Close"].iloc[i])
            mark = cash + shares * close
            equity_rows.append((ts, mark))

            if pending_weight is not None:
                target_w = pending_weight
                pending_weight = None
                target_value = mark * target_w
                current_value = shares * close
                delta = target_value - current_value
                if abs(delta) > 1e-6:
                    side = "BUY" if delta > 0 else "SELL"
                    open_px = float(df["Open"].iloc[i])
                    vol = float(df["Volume"].iloc[i])
                    fill = simulate_fill(side, open_px, abs(delta), vol, self.execution)
                    if not fill.rejected:
                        trade_shares = delta / fill.fill_price
                        shares += trade_shares
                        cash -= delta
                        cash -= fill.commission_usd
                        trades.append(
                            {
                                "timestamp": str(ts),
                                "side": side,
                                "fill_price": fill.fill_price,
                                "slippage_bps": fill.slippage_bps_applied,
                                "commission_usd": fill.commission_usd,
                                "shares_delta": trade_shares,
                            }
                        )

            if i >= len(df) - 1:
                break

            sig = strategy.on_bar(BarsView(df, i), i)
            pending_weight = clip_weight(sig.target_weight)

        equity = pd.Series(
            [e for _, e in equity_rows],
            index=pd.DatetimeIndex([t for t, _ in equity_rows]),
            name="equity",
        )
        metrics = summarize_backtest(equity)
        return BacktestResult(equity=equity, trades=trades, metrics=metrics)
