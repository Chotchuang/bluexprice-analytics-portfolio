# Public live-record payload contract

**As-of:** 2026-08-29 · C-20 / public-engine-proof unlock

## Allowed in public `live_records/*.jsonl`

| Field | Type | Notes |
|-------|------|-------|
| `timestamp` | ISO-8601 UTC | Decision or fill time |
| `asset` | string | Ticker symbol |
| `action` | string | e.g. `REBALANCE`, `HOLD` |
| `target_weight` | float | Portfolio weight target |
| `execution_price_simulated` | float | Fill price after friction |
| `slippage_bps_applied` | float | Basis points |
| `transaction_fee_usd` | float | Fee charged |
| `signal_sha256` | string | Hash of pre-reveal signal payload |
| `cash_after` | float | Optional audit |
| `record_id` | string | UUID |

## Forbidden in public exports

- Indicator formulas, Pine, feature recipes
- Internal signal fields or implementation-specific column names
- Model weights, hyperparameters that reverse-engineer alpha
- Full Blueprice CSV paths or batch JSON schemas

## Commitment flow

1. **Before** next bar price is known: compute `signal_sha256 = SHA256(canonical_json(signal_payload))`
2. Store hash in public log (or commit in CI)
3. **After** bar closes: reveal payload; verifier checks hash match

Canonical JSON: sorted keys, no whitespace, UTF-8.
