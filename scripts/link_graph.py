#!/usr/bin/env python3
"""Audit the barbell internal-link graph.

The Connector wires links into the body as posts are written. This script verifies the
graph on every run: it confirms each published post's declared internal_links targets
exist, flags orphan pages (no inbound links), and flags money/pillar pages that are not
yet receiving enough inbound authority links to rank.

Reads content-plan/plan.json. Reports only (does not rewrite pages); act on its warnings.
"""
import json, os, re, glob
from collections import defaultdict

PLAN = "content-plan/plan.json"
MIN_INBOUND_MONEY = 3  # money/pillar pages want at least this many inbound authority links

def path_for(rec):
    folder = "services" if rec.get("role") in ("pillar", "money") else "blog"
    return f"site/{folder}/{rec['url_slug']}.html"

def live_links(path):
    """Internal links actually present in a published file."""
    if not os.path.exists(path):
        return []
    raw = open(path, encoding="utf-8").read()
    return re.findall(r'href="(/(?:blog|services)/[^"]+\.html)"', raw)

def main():
    if not os.path.exists(PLAN):
        print("link_graph: no content-plan/plan.json yet; nothing to audit.")
        return
    plan = {r["url_slug"]: r for r in json.load(open(PLAN, encoding="utf-8"))}
    published = {slug: r for slug, r in plan.items() if os.path.exists(path_for(r))}

    inbound = defaultdict(int)
    problems = []

    for slug, rec in published.items():
        p = path_for(rec)
        links = live_links(p)
        for href in links:
            target = os.path.basename(href)[:-5]
            inbound[target] += 1
            if target not in plan:
                problems.append(f"{p}: links to unknown target {href}")
            elif not os.path.exists(path_for(plan[target])):
                problems.append(f"{p}: links to unpublished page {href}")
        # authority posts should link up to pillar + a money page
        if rec.get("role") == "authority" and not links:
            problems.append(f"{p}: authority post with no internal links (must link up to pillar + money)")

    for slug, rec in published.items():
        if rec.get("role") in ("pillar", "money") and inbound[slug] < MIN_INBOUND_MONEY:
            problems.append(f"services/{slug}.html: only {inbound[slug]} inbound links (want >= {MIN_INBOUND_MONEY})")
        if inbound[slug] == 0 and rec.get("role") == "authority":
            problems.append(f"{path_for(rec)}: orphan (no inbound links)")

    print(f"link_graph: {len(published)} published pages audited.")
    if problems:
        print(f"  {len(problems)} issue(s):")
        for p in problems:
            print(f"   - {p}")
    else:
        print("  graph clean.")

if __name__ == "__main__":
    main()
