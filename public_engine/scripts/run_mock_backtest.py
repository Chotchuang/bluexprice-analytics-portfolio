"""Run mock backtest and optional tear sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from public_engine.backtester import EventDrivenEngine
from public_engine.reports.tear_sheet import write_tear_sheet
from public_engine.strategies.mock import MockMomentumStrategy, MockSmaCrossStrategy


def _synthetic_ohlcv(n: int = 500, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    ret = rng.normal(0.0003, 0.015, size=n)
    close = 100 * np.cumprod(1 + ret)
    open_ = np.roll(close, 1)
    open_[0] = close[0]
    high = np.maximum(open_, close) * (1 + rng.uniform(0, 0.005, n))
    low = np.minimum(open_, close) * (1 - rng.uniform(0, 0.005, n))
    vol = rng.integers(1_000_000, 5_000_000, size=n).astype(float)
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": vol},
        index=dates,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Public engine mock backtest")
    p.add_argument("--symbol", default="DEMO")
    p.add_argument("--strategy", choices=("momentum", "sma"), default="momentum")
    p.add_argument("--out-dir", type=Path, default=Path("public_engine/reports/output"))
    args = p.parse_args()

    ohlcv = _synthetic_ohlcv()
    strategy = MockMomentumStrategy() if args.strategy == "momentum" else MockSmaCrossStrategy()
    engine = EventDrivenEngine()
    result = engine.run(ohlcv, strategy)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.out_dir / f"{args.symbol.lower()}_metrics.json"
    metrics_path.write_text(json.dumps(result.metrics, indent=2), encoding="utf-8")

    html_path = write_tear_sheet(
        args.out_dir / f"{args.symbol.lower()}_tear_sheet.html",
        title=f"Public Engine Proof — {args.symbol} ({args.strategy})",
        metrics=result.metrics,
        records=[],
    )
    print(json.dumps({"metrics": result.metrics, "metrics_path": str(metrics_path), "html": str(html_path)}, indent=2))


if __name__ == "__main__":
    main()
