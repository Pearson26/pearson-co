#!/usr/bin/env python3
"""Batch 4 - Fractional Sales Leadership (35) + Growth Consulting (25) = 60 records.

Two small priority pillars. Semrush-researched US/global clusters (June 2026 estimates;
KD indicative). Both are ad-landing pillars. Idempotent on batch==4.
Run from repo root, then scripts/render_plan.py.
"""
import json, os

BATCH = 4
PLAN = "content-plan/plan.json"
WORDS = {"pillar": 2100, "money": 1450, "guide": 1650, "how-to": 1700,
         "comparison": 1500, "definition": 1150, "listicle": 1350, "benchmark": 1300}
ENGINES = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

def llm_phrasing(kw, ctype):
    k = kw.lower()
    if ctype == "how-to" and not k.startswith(("how", "what", "why", "when")):
        return "how do I " + kw
    if ctype == "comparison" and not k.startswith(("best", "what", "which")):
        return "which is better, " + kw
    return kw

def outline(ctype):
    t = {
        "pillar": ["What it is and who it is for", "Why businesses choose this", "How Lauren works this way",
                   "What an engagement includes", "Cost and what to expect"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which you need and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it works", "A practical example"],
        "listicle": ["Why this matters", "The list, with how to apply each", "Where teams go wrong"],
        "benchmark": ["The headline numbers", "How the figures break down", "How to read your own data"],
    }
    return t.get(ctype, t["guide"])

records = []
_idx = [0]

def r(pillar, pid, pillar_slug, default_money, title, slug, role, ctype, market, intent, kw, vol, kd, ad=False, sec=None, ang=None, money=None):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role in ("pillar", "money"):
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    up = [] if role == "pillar" else ([pillar_slug] if role == "money" else [pillar_slug, money or default_money])
    return {
        "seq": None, "batch": BATCH, "pillar": pillar, "pillar_id": pid,
        "role": role, "content_type": ctype, "is_ad_landing": ad,
        "title": title, "url_slug": slug, "target_market": market, "intent": intent,
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or "",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
    }

# ===================== Fractional Sales Leadership (35) =====================
FP, FID, FSLUG, FMON = "Fractional Sales Leadership", "fractional-leadership", "fractional-sales-leadership", "fractional-sales-director"
records.append(r(FP, FID, FSLUG, FMON, "Fractional sales leadership", FSLUG, "pillar", "pillar", "US", "commercial",
    "fractional sales leadership", 260, 22, ad=True,
    sec=["fractional sales director", "fractional cro", "fractional vp of sales"],
    ang="Fractional sales leadership gives a growing business a senior sales or revenue leader part-time, for a fraction of a full-time cost. It suits founder-led teams that have outgrown founder-led selling but are not ready for a full-time hire. This is how Lauren supports that stage, including across the Middle East."))
FM = [
 ("Fractional sales director","fractional-sales-director","fractional sales director",90,18,True,["fractional head of sales"]),
 ("Fractional CRO","fractional-cro","fractional cro",90,18,True,["fractional chief revenue officer"]),
 ("Fractional sales manager","fractional-sales-manager","fractional sales manager",390,24,False,["fractional sales management"]),
 ("Fractional commercial director","fractional-commercial-director","fractional commercial director",40,16,False,["fractional commercial leader"]),
 ("Fractional VP of sales","fractional-vp-of-sales","fractional vp of sales",210,22,False,["fractional vp sales"]),
 ("Fractional head of sales","fractional-head-of-sales","fractional head of sales",70,18,False,["interim head of sales"]),
]
for t, s, kw, vol, kd, ad, sec in FM:
    records.append(r(FP, FID, FSLUG, FMON, t, s, "money", "money", "US", "commercial", kw, vol, kd, ad=ad, sec=sec,
        ang=f"What Lauren offers as a {t.lower()}, who it suits, how the engagement runs and the outcomes to expect."))
FA = [
 ("What is fractional sales leadership?","what-is-fractional-sales-leadership","definition","fractional sales leadership meaning",50,16,None),
 ("What is a fractional sales director?","what-is-a-fractional-sales-director","definition","what is a fractional sales director",50,16,None),
 ("What is a fractional CRO?","what-is-a-fractional-cro","definition","what is a fractional cro",70,16,"fractional-cro"),
 ("Fractional CRO meaning","fractional-cro-meaning","definition","fractional cro meaning",70,16,"fractional-cro"),
 ("What is a fractional sales manager?","what-is-a-fractional-sales-manager","definition","what is a fractional sales manager",50,16,"fractional-sales-manager"),
 ("What does a fractional CRO do?","what-does-a-fractional-cro-do","definition","what does a cro do",480,24,"fractional-cro"),
 ("Fractional sales management explained","fractional-sales-management-explained","guide","fractional sales management",210,20,"fractional-sales-manager"),
 ("Fractional vs full-time sales director","fractional-vs-full-time-sales-director","comparison","fractional vs full time sales director",40,16,None),
 ("Fractional vs interim sales leadership","fractional-vs-interim-sales-leadership","comparison","fractional vs interim",40,16,None),
 ("When to hire a fractional sales director","when-to-hire-a-fractional-sales-director","guide","when to hire a fractional sales director",40,16,"fractional-sales-director"),
 ("When to hire a fractional CRO","when-to-hire-a-fractional-cro","guide","when to hire a fractional cro",30,16,"fractional-cro"),
 ("How much does a fractional sales director cost?","fractional-sales-director-cost","guide","fractional sales director cost",40,16,"fractional-sales-director"),
 ("How much does a fractional CRO cost?","fractional-cro-cost","guide","fractional cro cost",40,16,"fractional-cro"),
 ("The benefits of fractional sales leadership","benefits-of-fractional-sales-leadership","listicle","benefits of fractional sales leadership",40,16,None),
 ("Fractional sales leadership for startups","fractional-sales-leadership-for-startups","guide","fractional sales leadership for startups",30,16,None),
 ("Fractional sales leadership for SaaS","fractional-sales-leadership-for-saas","guide","fractional sales leadership saas",30,16,None),
 ("A fractional CRO for startups","fractional-cro-for-startups","guide","fractional cro for startups",30,16,"fractional-cro"),
 ("How fractional sales leadership works","how-fractional-sales-leadership-works","guide","how fractional sales leadership works",30,16,None),
 ("Fractional sales leader vs sales consultant","fractional-vs-sales-consultant","comparison","fractional vs sales consultant",30,16,None),
 ("Signs you need a fractional sales director","signs-you-need-a-fractional-sales-director","guide","signs you need a fractional sales director",30,16,"fractional-sales-director"),
 ("The fractional sales leader role explained","fractional-sales-leader-role","guide","fractional sales leader",140,20,None),
 ("A guide to the fractional VP of sales","fractional-vp-of-sales-guide","guide","fractional vp of sales",210,22,"fractional-vp-of-sales"),
 ("The fractional chief sales officer role","fractional-chief-sales-officer","guide","fractional chief sales officer",140,20,None),
 ("Fractional revenue leadership explained","fractional-revenue-leadership","guide","fractional revenue leadership",40,16,"fractional-cro"),
 ("Fractional sales models compared","fractional-sales-models","comparison","fractional sales model",40,16,None),
 ("How to hire a fractional sales leader","how-to-hire-a-fractional-sales-leader","how-to","how to hire a fractional sales leader",30,16,"fractional-sales-director"),
 ("Fractional sales leadership for hospitality tech","fractional-sales-leadership-hospitality-tech","guide","fractional sales leadership hospitality",20,14,None),
 ("Fractional sales leadership for Middle East expansion","fractional-sales-leadership-middle-east","guide","fractional sales leadership middle east",20,14,None),
]
for t, s, ctype, kw, vol, kd, money in FA:
    market = "global" if ctype in ("definition", "comparison") else "US"
    records.append(r(FP, FID, FSLUG, FMON, t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money,
        ang=f"A clear, practical answer to \"{kw}\" for founder-led teams weighing senior sales help, with a clear next step."))

# ===================== Growth Consulting (25) =====================
GP, GID, GSLUG, GMON = "Growth Consulting & Strategy", "growth-consulting", "growth-consulting", "business-growth-consultant"
records.append(r(GP, GID, GSLUG, GMON, "Growth consulting", GSLUG, "pillar", "pillar", "global", "commercial",
    "business growth consulting", 880, 30, ad=True,
    sec=["growth consultant", "growth strategy consulting", "business growth consultant"],
    ang="Growth consulting helps founder-led businesses find and remove the constraints holding back revenue, then build a practical plan to scale. Lauren works on the commercial engine behind growth: CRM, process, pipeline and the route to market, not vanity tactics."))
GM = [
 ("Business growth consultant","business-growth-consultant","business growth consultant",480,26,True,["growth consultant"]),
 ("Growth strategy consultant","growth-strategy-consultant","growth strategy consultant",260,24,False,["growth strategy consulting"]),
 ("Business growth advisor","business-growth-advisor","business growth advisor",390,26,False,["growth advisor"]),
 ("Growth consulting services","growth-consulting-services","business growth consulting services",390,26,False,["growth consulting"]),
]
for t, s, kw, vol, kd, sec in [(m[0], m[1], m[2], m[3], m[4], m[5]) for m in [
 ("Business growth consultant","business-growth-consultant","business growth consultant",480,26,["growth consultant"]),
 ("Growth strategy consultant","growth-strategy-consultant","growth strategy consultant",260,24,["growth strategy consulting"]),
 ("Business growth advisor","business-growth-advisor","business growth advisor",390,26,["growth advisor"]),
 ("Growth consulting services","growth-consulting-services","business growth consulting services",390,26,["growth consulting"]),
]]:
    ad = (s == "business-growth-consultant")
    records.append(r(GP, GID, GSLUG, GMON, t, s, "money", "money", "global", "commercial", kw, vol, kd, ad=ad, sec=sec,
        ang=f"What Lauren's {t.lower()} engagement covers, who it suits, how it runs and the outcomes to expect."))
GA = [
 ("What is a growth consultant?","what-is-a-growth-consultant","definition","what is a growth consultant",90,18,None),
 ("What does a growth consultant do?","what-does-a-growth-consultant-do","definition","what does a growth consultant do",50,18,None),
 ("How to build a business growth strategy","business-growth-strategy","guide","business growth strategy",720,32,None),
 ("A growth strategy framework","growth-strategy-framework","guide","growth strategy framework",480,30,None),
 ("Business growth strategies that work","business-growth-strategies","listicle","business growth strategies",3600,40,None),
 ("How to grow your business","how-to-grow-your-business","guide","how to grow your business",1600,38,None),
 ("How to grow a small business","how-to-grow-a-small-business","guide","how to grow a small business",1000,36,None),
 ("Growth strategy examples","growth-strategy-examples","listicle","growth strategy examples",260,24,None),
 ("When to hire a growth consultant","when-to-hire-a-growth-consultant","guide","when to hire a growth consultant",30,16,"business-growth-consultant"),
 ("How much does a growth consultant cost?","growth-consultant-cost","guide","growth consultant cost",30,16,"business-growth-consultant"),
 ("Growth consultant vs business coach","growth-consultant-vs-business-coach","comparison","growth consultant vs business coach",40,18,None),
 ("Growth consulting vs management consulting","growth-vs-management-consulting","comparison","growth consulting vs management consulting",30,16,None),
 ("Types of growth strategy","types-of-growth-strategy","guide","types of growth strategy",170,22,None),
 ("How to run a growth diagnostic","growth-diagnostic","how-to","growth audit",40,16,"growth-consulting-services"),
 ("How to scale a business","how-to-scale-a-business","guide","scaling a business",320,28,None),
 ("Founder-stage growth: a guide","founder-stage-growth","guide","founder led growth",40,16,None),
 ("Growth levers explained","growth-levers","guide","growth levers",90,20,None),
 ("Product-led vs sales-led growth","product-led-vs-sales-led-growth","comparison","product led vs sales led growth",110,22,None),
 ("A growth strategy for SaaS","growth-strategy-for-saas","guide","saas growth strategy",170,24,None),
 ("Business expansion strategies","business-expansion-strategies","listicle","business expansion strategies",260,24,None),
]
for t, s, ctype, kw, vol, kd, money in GA:
    market = "global"
    records.append(r(GP, GID, GSLUG, GMON, t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money,
        ang=f"A practical, plain-English answer to \"{kw}\" for founder-led teams, with a clear next step."))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch04: wrote {len(records)} records. by pillar: {dict(Counter(x['pillar'] for x in records))}. plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
