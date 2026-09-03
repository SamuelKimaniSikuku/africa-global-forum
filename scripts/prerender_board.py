#!/usr/bin/env python3
"""Prerender the static SEO block on /corridor-board/ from data/fintech-board.json.

Regenerates, between PRERENDER markers, a crawlable HTML section listing every
corridor with today's mid-market rate and AGF picks — so search engines and
AI crawlers that don't execute JavaScript still see the full content.

Also bumps:
  - "dateModified" values in the board page's JSON-LD
  - the /corridor-board/ <lastmod> in sitemap.xml

Run after scripts/refresh_rates.py.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "fintech-board.json"
PAGE = ROOT / "corridor-board" / "index.html"
SITEMAP = ROOT / "sitemap.xml"

START = "<!-- PRERENDER:START -->"
END = "<!-- PRERENDER:END -->"


def build_block(data):
    fx = data.get("fx", {})
    rates = fx.get("rates", {})
    updated = fx.get("updated", "")
    apps_by_slug = {a["slug"]: a for a in data["apps"]}

    parts = []
    parts.append('<h2 class="board-static-title">Today&rsquo;s exchange rates &mdash; every corridor at a glance</h2>')
    if updated:
        parts.append(f'<p class="board-static-updated mono">Mid-market reference rates &middot; updated {updated} &middot; refreshed automatically every day</p>')

    for region in data["regions"]:
        base = region["currency"]
        note = f' <span class="board-static-note">({region["currencyNote"]})</span>' if region.get("currencyNote") else ""
        parts.append(f'<h3 class="board-static-region">From {region["label"]} ({base}){note}</h3>')
        parts.append('<table class="board-static-table"><thead><tr><th>Home country</th><th>Rate today</th><th>AGF picks</th></tr></thead><tbody>')
        for country in data["countries"]:
            key = f'{region["key"]}→{country["key"]}'
            rate = rates.get(base, {}).get(country["currency"])
            rate_txt = f'1 {base} = {rate:,} {country["currency"]}' if rate else "—"
            picks = data["agf_picks"].get(key, [])
            picks_txt = ", ".join(apps_by_slug[s]["name"] for s in picks if s in apps_by_slug) or "—"
            parts.append(
                f'<tr><td>{country["flag"]} {country["label"]}</td>'
                f'<td class="board-static-rate">{rate_txt}</td>'
                f'<td>{picks_txt}</td></tr>'
            )
        parts.append("</tbody></table>")

    app_names = ", ".join(a["name"] for a in data["apps"])
    parts.append(f'<p class="board-static-apps">Apps compared on this board: {app_names}.</p>')
    return "\n".join(parts)


def main():
    data = json.loads(DATA.read_text())
    today = date.today().isoformat()

    # 1. Prerender block
    html = PAGE.read_text()
    if START not in html or END not in html:
        sys.exit("PRERENDER markers not found in corridor-board/index.html")
    pre = html.index(START) + len(START)
    post = html.index(END)
    html = html[:pre] + "\n" + build_block(data) + "\n" + html[post:]

    # 2. JSON-LD dateModified bumps (WebPage + Dataset on this page only)
    html = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{today}"', html)
    PAGE.write_text(html)

    # 3. Sitemap lastmod for /corridor-board/
    sm = SITEMAP.read_text()
    sm = re.sub(
        r'(<loc>https://africaglobalforum\.com/corridor-board/</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
        rf'\g<1>{today}\g<2>',
        sm,
    )
    SITEMAP.write_text(sm)

    print(f"OK — prerendered block + dateModified + sitemap lastmod set to {today}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
