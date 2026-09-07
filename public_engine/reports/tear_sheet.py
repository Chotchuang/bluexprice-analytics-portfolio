"""HTML tear sheet from live records (public-safe)."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def render_tear_sheet_html(
    title: str,
    metrics: dict[str, Any],
    records: list[dict[str, Any]],
) -> str:
    metrics_json = html.escape(json.dumps(metrics, indent=2))
    rows = ""
    for r in records[-50:]:
        rows += (
            "<tr>"
            f"<td>{html.escape(str(r.get('timestamp', '')))}</td>"
            f"<td>{html.escape(str(r.get('asset', '')))}</td>"
            f"<td>{html.escape(str(r.get('action', '')))}</td>"
            f"<td>{r.get('target_weight', '')}</td>"
            f"<td>{r.get('execution_price_simulated', '')}</td>"
            f"<td>{html.escape(str(r.get('signal_sha256', ''))[:16])}…</td>"
            "</tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }}
    pre {{ background: #f6f6f6; padding: 1rem; overflow: auto; }}
    .disclaimer {{ color: #666; font-size: 0.9rem; margin-top: 2rem; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p>Historical simulation / live audit log — not trading advice.</p>
  <h2>Summary metrics</h2>
  <pre>{metrics_json}</pre>
  <h2>Recent live records (last 50)</h2>
  <table>
    <thead><tr>
      <th>Time</th><th>Asset</th><th>Action</th><th>Weight</th><th>Fill</th><th>Hash</th>
    </tr></thead>
    <tbody>{rows or '<tr><td colspan="6">No records</td></tr>'}</tbody>
  </table>
  <p class="disclaimer">C-20 public export — no proprietary signal formulas.</p>
</body>
</html>"""


def write_tear_sheet(
    path: Path,
    title: str,
    metrics: dict[str, Any],
    records: list[dict[str, Any]],
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_tear_sheet_html(title, metrics, records), encoding="utf-8")
    return path
