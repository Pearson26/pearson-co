#!/usr/bin/env python3
"""Reconcile build_state.json against what is actually on disk.

Source of truth for progression. Reads content-plan/plan.json (the machine mirror of
plan.md), checks which records have a published HTML file, and computes:
  - posts_published : how many plan records are live
  - next_index      : the smallest seq with no published file (the pointer)

Usage:
    python scripts/verify_state.py            # report only
    python scripts/verify_state.py --write    # write reconciled values into build_state.json

Never hand-edit the counts in build_state.json; run this instead.
"""
import json, os, sys, datetime

PLAN = "content-plan/plan.json"
STATE = "build_state.json"

def path_for(rec):
    role = rec.get("role", "authority")
    folder = "services" if role in ("pillar", "money") else "blog"
    return f"{folder}/{rec['url_slug']}.html"

def main():
    write = "--write" in sys.argv
    if not os.path.exists(PLAN):
        print("verify_state: no content-plan/plan.json yet; nothing to reconcile.")
        return 0
    plan = json.load(open(PLAN, encoding="utf-8"))
    plan = sorted(plan, key=lambda r: r["seq"])

    published, missing = [], []
    for rec in plan:
        (published if os.path.exists(path_for(rec)) else missing).append(rec)

    posts_published = len(published)
    next_index = missing[0]["seq"] if missing else (plan[-1]["seq"] + 1 if plan else 1)
    last_slug = published[-1]["url_slug"] if published else None

    print(f"verify_state: {posts_published}/{len(plan)} published. next_index = {next_index}.")
    # warn on gaps (published out of order)
    gap = [r["seq"] for r in published if r["seq"] >= next_index]
    if gap:
        print(f"  WARNING: posts published past the pointer (out of order): {gap}")

    if write:
        state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
        state.update({
            "next_index": next_index,
            "posts_published": posts_published,
            "last_published_slug": last_slug,
            "total_planned": len(plan),
            "last_updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        state.setdefault("notes", "")
        json.dump(state, open(STATE, "w", encoding="utf-8"), indent=2)
        print(f"verify_state: wrote {STATE}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
