#!/usr/bin/env python3
"""Refresh mid-market FX rates in data/fintech-board.json.

Fetches daily mid-market reference rates from open.er-api.com (free,
no key, refreshed once a day) for each sending-region base currency
and writes the six receiving currencies into an "fx" block:

  "fx": {
    "updated": "2026-08-31",
    "source": "open.er-api.com (mid-market reference)",
    "rates": { "EUR": {"KES": 167.2, ...}, "USD": {...}, "AUD": {...} }
  }

If the API is unreachable the existing fx block is left untouched and
the script exits 0 (so the workflow's commit step simply finds no diff).
"""
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "fintech-board.json"

RECEIVE = ["KES", "NGN", "GHS", "UGX", "RWF", "ZAR"]


def fetch_base(base):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            payload = json.load(resp)
    except Exception as exc:  # network / HTTP / JSON errors alike
        print(f"WARN {base}: {exc}", file=sys.stderr)
        return None
    if payload.get("result") != "success":
        print(f"WARN {base}: API result={payload.get('result')}", file=sys.stderr)
        return None
    rates = payload.get("rates", {})
    out = {}
    for ccy in RECEIVE:
        if ccy in rates:
            # sensible precision: 2dp for big numbers, 4dp for small
            v = rates[ccy]
            out[ccy] = round(v, 2 if v >= 20 else 4)
    return out or None


def main():
    data = json.loads(DATA.read_text())
    bases = sorted({r["currency"] for r in data["regions"]})

    fresh = {}
    for base in bases:
        got = fetch_base(base)
        if got:
            fresh[base] = got

    if not fresh:
        print("No rates fetched; leaving existing fx block untouched.")
        return 0

    fx = data.get("fx", {})
    merged = fx.get("rates", {})
    merged.update(fresh)
    data["fx"] = {
        "updated": date.today().isoformat(),
        "source": "open.er-api.com (mid-market reference)",
        "rates": merged,
    }
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    got_pairs = sum(len(v) for v in fresh.values())
    print(f"OK — refreshed {len(fresh)} base currencies ({got_pairs} pairs), dated {data['fx']['updated']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
