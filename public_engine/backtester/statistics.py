"""Performance statistics — Sharpe, drawdown, deflated Sharpe."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    if len(equity) < 2:
        return 0.0
    peak = equity.cummax()
    dd = (equity - peak) / peak.replace(0, np.nan)
    return float(dd.min())


def sharpe_ratio(daily_returns: pd.Series, rf: float = 0.0, periods: int = 252) -> float:
    if len(daily_returns) < 2:
        return 0.0
    excess = daily_returns - rf / periods
    std = excess.std()
    if std == 0 or not math.isfinite(std):
        return 0.0
    return float(excess.mean() / std * math.sqrt(periods))


def sortino_ratio(daily_returns: pd.Series, rf: float = 0.0, periods: int = 252) -> float:
    if len(daily_returns) < 2:
        return 0.0
    excess = daily_returns - rf / periods
    downside = np.minimum(excess.values, 0.0)
    semi = float(np.sqrt((downside ** 2).mean()))
    if semi == 0:
        return 0.0
    return float(excess.mean() / semi * math.sqrt(periods))


def calmar_ratio(ann_return: float, max_dd: float) -> float:
    if max_dd == 0:
        return 0.0
    return ann_return / abs(max_dd)


def deflated_sharpe_ratio(
    observed_sr: float,
    n_trials: int,
    n_observations: int,
    skew: float = 0.0,
    kurtosis: float = 3.0,
) -> float:
    """Simplified Bailey–Lopez de Prado DSR (public audit helper)."""
    if n_observations < 2 or n_trials < 1:
        return 0.0
    # Euler-Mascheroni approx for expected max SR under null
    euler = 0.5772156649
    expected_max = (
        (1 - euler) * _norm_ppf(1 - 1.0 / n_trials)
        + euler * _norm_ppf(1 - 1.0 / (n_trials * math.e))
    ) / math.sqrt(n_observations - 1)
    denom = 1 - skew * observed_sr + ((kurtosis - 1) / 4) * (observed_sr ** 2)
    if denom <= 0:
        return 0.0
    adjusted = observed_sr - expected_max * math.sqrt(denom)
    return adjusted


def _norm_ppf(p: float) -> float:
    """Approx inverse normal CDF (Acklam) — no scipy required."""
    if p <= 0 or p >= 1:
        return 0.0
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285901596191e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580619e02,
        -1.556989775450226e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041446e-03,
        3.224671290700397e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
        * q
        / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    )


def summarize_backtest(equity: pd.Series, periods: int = 252) -> dict[str, Any]:
    rets = equity.pct_change().dropna()
    ann = (equity.iloc[-1] / equity.iloc[0]) ** (periods / max(len(equity) - 1, 1)) - 1
    mdd = max_drawdown(equity)
    sr = sharpe_ratio(rets)
    return {
        "annualized_return": float(ann),
        "max_drawdown": float(mdd),
        "sharpe": float(sr),
        "sortino": float(sortino_ratio(rets)),
        "calmar": float(calmar_ratio(float(ann), mdd)),
        "deflated_sharpe": float(deflated_sharpe_ratio(sr, n_trials=1, n_observations=len(rets))),
        "n_bars": int(len(equity)),
    }
