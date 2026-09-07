"""Live record schema and immutable commitment hashing."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def signal_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def verify_signal_sha256(payload: dict[str, Any], expected: str) -> bool:
    return signal_sha256(payload) == expected


@dataclass
class LiveRecord:
    timestamp: str
    asset: str
    action: str
    target_weight: float
    execution_price_simulated: float
    slippage_bps_applied: float
    transaction_fee_usd: float
    signal_sha256: str
    cash_after: float | None = None
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_public_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


class LiveRecorder:
    """Append-only JSONL writer — no in-place edits."""

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def append(self, record: LiveRecord, filename: str = "live.jsonl") -> Path:
        path = self.directory / filename
        line = json.dumps(record.to_public_dict(), ensure_ascii=False) + "\n"
        with path.open("a", encoding="utf-8") as f:
            f.write(line)
        return path

    @staticmethod
    def read_all(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows
