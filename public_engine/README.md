# Public Engine Proof

**Status:** active public demonstration component

Self-contained backtest and live-record package for public portfolio use.  
Contains mock strategies only — no private Bluexprice alpha, formulas, or
production-data coupling.

## What this proves (public-safe)

| Pillar | Module |
|--------|--------|
| Decoupled event engine | `public_engine/backtester/engine.py` |
| Market friction | `public_engine/backtester/execution.py` |
| Statistical rigor | `public_engine/backtester/statistics.py` + `tests/test_bias.py` |
| Immutable live log | `public_engine/live/` + `live_records/` |
| Tear sheet (live/OOS) | `public_engine/reports/tear_sheet.py` |

## Quick start

```bash
# Mock backtest (momentum · next-bar execution · slippage)
python -m public_engine.scripts.run_mock_backtest --symbol DEMO

# Append one live record (demo payload)
python -m public_engine.scripts.append_live_record --demo

# Tests
pytest tests/test_public_engine.py -q
```

## Public vs private boundary

See [PAYLOAD_CONTRACT.md](PAYLOAD_CONTRACT.md).  
Private alpha emits only: timestamp, asset, action, target_weight, fill, fees, `signal_sha256`.

## Repository boundary

This package is intentionally independent from the private research system.
Only mock strategies and demo outputs belong in this public repository.
