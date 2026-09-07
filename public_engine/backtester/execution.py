"""Execution models — slippage, commission, capacity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionConfig:
    commission_rate: float = 0.001  # per trade notional
    slippage_bps: float = 5.0
    max_participation: float = 0.05  # max fraction of bar volume


@dataclass(frozen=True)
class FillResult:
    fill_price: float
    slippage_bps_applied: float
    commission_usd: float
    rejected: bool = False
    reject_reason: str = ""


def simulate_fill(
    side: str,
    reference_price: float,
    notional_usd: float,
    bar_volume: float,
    config: ExecutionConfig,
) -> FillResult:
    """
    Apply slippage against reference price and commission on notional.
    Reject if order exceeds participation cap (capacity realism).
    """
    if reference_price <= 0 or notional_usd <= 0:
        return FillResult(reference_price, 0.0, 0.0, True, "invalid_price_or_size")

    shares = notional_usd / reference_price
    if bar_volume > 0 and shares > bar_volume * config.max_participation:
        return FillResult(reference_price, 0.0, 0.0, True, "capacity_exceeded")

    slip_frac = config.slippage_bps / 10_000.0
    if side.upper() in ("BUY", "LONG", "REBALANCE_UP"):
        fill_price = reference_price * (1.0 + slip_frac)
    else:
        fill_price = reference_price * (1.0 - slip_frac)

    commission = notional_usd * config.commission_rate
    return FillResult(fill_price, config.slippage_bps, commission)
