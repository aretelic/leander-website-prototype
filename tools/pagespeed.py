#!/usr/bin/env python3
"""Run Google PageSpeed Insights (Lighthouse) on every page of the published prototype.

Usage:
    python3 tools/pagespeed.py                 # mobile and desktop, all pages
    python3 tools/pagespeed.py --strategy mobile
    PSI_KEY=your-api-key python3 tools/pagespeed.py   # optional key: higher rate limits

Writes reports/pagespeed.md (a table you can read) and reports/pagespeed.json (raw scores
and the failing accessibility checks). Only uses the Python standard library.
The site must be published first: PageSpeed Insights tests public URLs.
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://aretelic.github.io/leander-website-prototype/"
API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]


def pages():
    out = []
    for p in sorted(ROOT.rglob("index.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in ("content", "tools", "reports", ".git"):
            continue
        path = "" if str(rel) == "index.html" else str(rel.parent) + "/"
        out.append(path)
    return out


def run(path, strategy, key):
    q = [("url", BASE + path), ("strategy", strategy)] + [("category", c) for c in CATEGORIES]
    if key:
        q.append(("key", key))
    url = API + "?" + urllib.parse.urlencode(q)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                data = json.load(r)
            lr = data["lighthouseResult"]
            scores = {c: round((lr["categories"][c]["score"] or 0) * 100) for c in CATEGORIES}
            audits = lr["audits"]
            metrics = {
                "LCP": audits["largest-contentful-paint"]["displayValue"],
                "CLS": audits["cumulative-layout-shift"]["displayValue"],
                "TBT": audits["total-blocking-time"]["displayValue"],
            }
            a11y_fails = [
                {"id": ref["id"], "title": audits[ref["id"]]["title"],
                 "items": [i.get("node", {}).get("snippet", "")[:160] for i in (audits[ref["id"]].get("details") or {}).get("items", [])[:5]]}
                for ref in lr["categories"]["accessibility"]["auditRefs"]
                if ref.get("weight", 0) > 0 and audits[ref["id"]].get("score") is not None and audits[ref["id"]]["score"] < 1
            ]
            perf_tips = [
                {"id": k, "title": v["title"], "savings": v.get("displayValue", "")}
                for k, v in audits.items()
                if v.get("details", {}).get("type") == "opportunity" and (v.get("score") or 1) < 0.9
            ]
            return {"path": "/" + path, "strategy": strategy, "scores": scores, "metrics": metrics,
                    "accessibility_failures": a11y_fails, "performance_opportunities": perf_tips}
        except Exception as e:  # rate limits and timeouts: back off and retry
            err = str(e)
            time.sleep(10 * (attempt + 1))
    return {"path": "/" + path, "strategy": strategy, "error": err}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="both")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    key = os.environ.get("PSI_KEY")
    strategies = ["mobile", "desktop"] if args.strategy == "both" else [args.strategy]
    jobs = [(p, s) for s in strategies for p in pages()]
    print(f"Testing {len(jobs)} page runs against {BASE} …", flush=True)
    with ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(lambda j: run(j[0], j[1], key), jobs))
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    (out / "pagespeed.json").write_text(json.dumps(results, indent=1))
    lines = [f"# PageSpeed Insights report\n\nTested {time.strftime('%d %b %Y %H:%M')} against {BASE}. Scores out of 100.\n"]
    for s in strategies:
        rows = [r for r in results if r["strategy"] == s]
        lines.append(f"\n## {s.title()}\n\n| Page | Performance | Accessibility | Best practices | SEO* | LCP | CLS |\n|---|---|---|---|---|---|---|")
        for r in rows:
            if "error" in r:
                lines.append(f"| {r['path']} | error: {r['error'][:60]} | | | | | |")
                continue
            sc, m = r["scores"], r["metrics"]
            lines.append(f"| {r['path']} | {sc['performance']} | {sc['accessibility']} | {sc['best-practices']} | {sc['seo']} | {m['LCP']} | {m['CLS']} |")
    fails = {}
    for r in results:
        for f in r.get("accessibility_failures", []):
            fails.setdefault(f["title"], set()).add(r["path"])
    lines.append("\n## Accessibility checks that failed\n")
    lines += [f"- **{t}** on {len(p)} page(s): {', '.join(sorted(p)[:6])}{' …' if len(p) > 6 else ''}" for t, p in sorted(fails.items())] or ["None."]
    lines.append("\n*SEO is expected to be low: every page is deliberately set to `noindex` while this is a prototype.*\n")
    (out / "pagespeed.md").write_text("\n".join(lines))
    print((out / "pagespeed.md").read_text())


if __name__ == "__main__":
    sys.exit(main())
