#!/usr/bin/env python3
"""Assign the 12-month publish order (seq) across the whole plan.

Front-loads so paid can launch onto live pages, then spreads authority content across the
year so every month mixes pillars. Order:
  1. all pillar pages (by pillar priority)
  2. ad-landing money pages (priority, then volume desc)
  3. remaining money pages (priority, then volume desc)
  4. authority posts, round-robin across pillars in priority order (volume desc within pillar)
Also stamps `month` (1-12) at 3 posts/run. Idempotent; re-run any time. Run from repo root,
then scripts/render_plan.py and scripts/verify_state.py --write.
"""
import json, os
from collections import defaultdict

PLAN = "content-plan/plan.json"
PRIORITY = [
    "conversion-funnel", "revops", "crm-implementation", "fractional-leadership",
    "growth-consulting", "customer-journey", "hospitality-expansion", "process-sop",
    "crm-automation", "reporting-forecasting", "crm-consulting", "crm-adoption",
    "sales-pipeline", "go-to-market",
]
def prio(pid):
    return PRIORITY.index(pid) if pid in PRIORITY else len(PRIORITY)

def vol(rec):
    try:
        return int(rec.get("primary_volume") or 0)
    except (TypeError, ValueError):
        return 0

def main():
    plan = json.load(open(PLAN, encoding="utf-8"))

    pillars = sorted([r for r in plan if r["role"] == "pillar"], key=lambda r: (prio(r["pillar_id"]), r["url_slug"]))
    money_ad = sorted([r for r in plan if r["role"] == "money" and r.get("is_ad_landing")],
                      key=lambda r: (prio(r["pillar_id"]), -vol(r)))
    money_rest = sorted([r for r in plan if r["role"] == "money" and not r.get("is_ad_landing")],
                        key=lambda r: (prio(r["pillar_id"]), -vol(r)))

    # authority: round-robin across pillars in priority order, volume desc within a pillar
    by_pillar = defaultdict(list)
    for r in plan:
        if r["role"] == "authority":
            by_pillar[r["pillar_id"]].append(r)
    for pid in by_pillar:
        by_pillar[pid].sort(key=lambda r: -vol(r))
    order_pids = sorted(by_pillar.keys(), key=prio)
    authority = []
    idx = 0
    remaining = sum(len(v) for v in by_pillar.values())
    while remaining:
        for pid in order_pids:
            if idx < len(by_pillar[pid]):
                authority.append(by_pillar[pid][idx])
                remaining -= 1
        idx += 1

    ordered = pillars + money_ad + money_rest + authority
    assert len(ordered) == len(plan), f"sequencing lost records: {len(ordered)} vs {len(plan)}"

    PER_MONTH = 91  # ~1085 / 12, at 3 posts per run
    for i, rec in enumerate(ordered, start=1):
        rec["seq"] = i
        rec["month"] = min(12, (i - 1) // PER_MONTH + 1)

    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"sequence_plan: assigned seq 1..{len(ordered)}. "
          f"Month 1 = {sum(1 for r in ordered[:PER_MONTH])} posts "
          f"({sum(1 for r in ordered[:PER_MONTH] if r['role']=='pillar')} pillar, "
          f"{sum(1 for r in ordered[:PER_MONTH] if r['role']=='money')} money).")

if __name__ == "__main__":
    main()
