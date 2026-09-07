"""Risk helpers — position caps (public-safe)."""

from __future__ import annotations


def clip_weight(weight: float, max_abs: float = 1.0, max_leverage: float = 1.0) -> float:
    cap = min(max_abs, max_leverage)
    return max(-cap, min(cap, weight))
