"""Append immutable live record (demo or from signal payload file)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from public_engine.backtester.execution import ExecutionConfig, simulate_fill
from public_engine.live.records import LiveRecord, LiveRecorder, signal_sha256, utc_now_iso


def main() -> None:
    p = argparse.ArgumentParser(description="Append public live record")
    p.add_argument("--demo", action="store_true", help="Write demo REBALANCE record")
    p.add_argument("--asset", default="DEMO")
    p.add_argument("--payload-file", type=Path, help="Private signal payload JSON (pre-hash)")
    p.add_argument(
        "--records-dir",
        type=Path,
        default=Path("public_engine/live_records"),
    )
    args = p.parse_args()

    if args.demo:
        payload = {
            "asset": args.asset,
            "target_weight": 0.15,
            "strategy": "mock_momentum_public",
            "bar_timestamp": utc_now_iso(),
        }
    elif args.payload_file:
        payload = json.loads(args.payload_file.read_text(encoding="utf-8"))
    else:
        raise SystemExit("Provide --demo or --payload-file")

    digest = signal_sha256(payload)
    fill = simulate_fill("BUY", reference_price=100.0, notional_usd=15_000.0, bar_volume=2_000_000.0, config=ExecutionConfig())

    record = LiveRecord(
        timestamp=utc_now_iso(),
        asset=str(payload.get("asset", args.asset)),
        action="REBALANCE",
        target_weight=float(payload.get("target_weight", 0.0)),
        execution_price_simulated=fill.fill_price,
        slippage_bps_applied=fill.slippage_bps_applied,
        transaction_fee_usd=fill.commission_usd,
        signal_sha256=digest,
        cash_after=98500.0,
    )

    recorder = LiveRecorder(args.records_dir)
    path = recorder.append(record)
    print(json.dumps({"appended": str(path), "record_id": record.record_id, "signal_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
