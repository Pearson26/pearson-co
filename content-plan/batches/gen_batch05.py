#!/usr/bin/env python3
"""Batch 5 - Customer Journey Mapping, part 1 (60 records).

Semrush-researched US cluster (June 2026 estimates; KD indicative). Largest top-of-funnel
authority pillar (120 total, split 60+60); also an ad-landing pillar. Part 1 covers
foundations, how-to/process, templates, tools, components and core examples/by-type.
Idempotent on batch==5. Run from repo root, then scripts/render_plan.py.
"""
import json, os

PILLAR = "Customer Journey Mapping"
PID = "customer-journey"
BATCH = 5
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "customer-journey-mapping"
DEF_MONEY = "customer-journey-mapping-service"

WORDS = {"pillar": 2300, "money": 1400, "guide": 1650, "how-to": 1700,
         "comparison": 1500, "definition": 1150, "listicle": 1350, "template": 1250}
ENGINES = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

def llm_phrasing(kw, ctype):
    k = kw.lower()
    if ctype == "how-to" and not k.startswith(("how", "what", "why")):
        return "how do I " + kw
    if ctype == "comparison" and not k.startswith(("best", "what", "which")):
        return "what is the difference, " + kw
    return kw

def outline(ctype):
    t = {
        "pillar": ["What customer journey mapping is", "Why it matters for revenue", "How Lauren runs a mapping engagement",
                   "From map to action", "What an engagement includes"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which you need and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it works", "A practical example"],
        "listicle": ["Why this matters", "The list, with how to apply each", "Where teams go wrong"],
        "template": ["What the template covers", "How to use it", "A worked example"],
    }
    return t.get(ctype, t["guide"])

records = []
_idx = [0]

def r(title, slug, role, ctype, market, intent, kw, vol, kd, ad=False, sec=None, ang=None, money=None):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role in ("pillar", "money"):
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    up = [] if role == "pillar" else ([PILLAR_SLUG] if role == "money" else [PILLAR_SLUG, money or DEF_MONEY])
    return {
        "seq": None, "batch": BATCH, "pillar": PILLAR, "pillar_id": PID,
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
        "ai_overview_play": "Lead with a direct definition and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
    }

# Pillar
records.append(r("Customer journey mapping", PILLAR_SLUG, "pillar", "pillar", "global", "commercial",
    "customer journey mapping", 5400, 43, ad=True,
    sec=["customer journey map", "how to create a customer journey map", "customer journey mapping tools"],
    ang="Customer journey mapping lays out every step a customer takes with a business, from first awareness to loyalty, so you can see where they get stuck and where revenue leaks. Done well, it turns scattered assumptions into a shared, evidence-based plan. This is how Lauren runs mapping and turns the map into action."))

# Money (4)
M = [
 ("Customer journey mapping service","customer-journey-mapping-service","customer journey mapping services",140,20,["customer journey mapping"]),
 ("Customer journey mapping workshop","customer-journey-mapping-workshop","customer journey mapping workshop",90,18,["journey mapping workshop"]),
 ("Customer journey mapping consultant","customer-journey-mapping-consultant","customer journey mapping consultants",170,18,["customer journey consultant"]),
 ("Customer experience consulting","customer-experience-consulting","customer journey consulting",390,24,["cx consulting"]),
]
for t, s, kw, vol, kd, sec in M:
    records.append(r(t, s, "money", "money", "global", "commercial", kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

# Authority (55)
A = [
 # Foundations
 ("What is a customer journey map?","what-is-a-customer-journey-map","definition","what is a customer journey map",720,28,None),
 ("What is customer journey mapping?","what-is-customer-journey-mapping","definition","what is customer journey mapping",590,28,None),
 ("Customer journey definition","customer-journey-definition","definition","customer journey definition",480,24,None),
 ("What is a customer journey?","what-is-a-customer-journey","definition","what is a customer journey",480,24,None),
 ("Customer journey map vs customer experience map","customer-journey-vs-experience-map","comparison","customer experience map vs customer journey map",110,20,None),
 ("Customer journey map vs user journey map","customer-journey-vs-user-journey","comparison","user journey vs customer journey",90,18,None),
 ("The benefits of customer journey mapping","benefits-of-customer-journey-mapping","listicle","benefits of customer journey mapping",110,18,None),
 ("Why customer journey mapping matters","why-customer-journey-mapping-matters","guide","why customer journey mapping",50,18,None),
 ("Customer journey map vs sales funnel","customer-journey-vs-funnel","comparison","customer journey vs funnel",70,18,None),
 ("Customer journey mapping explained","customer-journey-mapping-explained","guide","customer journey mapping explained",70,18,None),
 # How-to & process
 ("How to create a customer journey map","how-to-create-a-customer-journey-map","how-to","how to create a customer journey map",880,30,None),
 ("The customer journey mapping process","customer-journey-mapping-process","how-to","customer journey mapping process",140,22,None),
 ("How to build a customer journey map","how-to-build-a-customer-journey-map","how-to","how to build a customer journey map",110,22,None),
 ("Customer journey mapping steps","customer-journey-mapping-steps","how-to","customer journey mapping steps",90,20,None),
 ("How to run a customer journey mapping workshop","how-to-run-a-journey-mapping-workshop","how-to","customer journey mapping workshop",90,20,"customer-journey-mapping-workshop"),
 ("How to map the customer journey","how-to-map-the-customer-journey","how-to","mapping the customer journey",390,26,None),
 ("Customer journey mapping best practices","customer-journey-mapping-best-practices","listicle","customer journey mapping best practices",70,18,None),
 ("Customer journey mapping mistakes to avoid","customer-journey-mapping-mistakes","listicle","customer journey mapping mistakes",40,16,None),
 ("What data you need for journey mapping","customer-journey-data-sources","guide","customer journey data",40,18,None),
 ("How to keep a customer journey map up to date","how-to-update-a-customer-journey-map","how-to","maintaining a customer journey map",30,16,None),
 # Templates
 ("A customer journey map template","customer-journey-map-template","template","customer journey map template",1900,32,None),
 ("A customer experience journey map template","customer-experience-journey-map-template","template","customer experience journey map template",720,28,None),
 ("A free customer journey map template","free-customer-journey-map-template","template","free customer journey map template",110,20,None),
 ("A customer journey map template for Excel","customer-journey-map-template-excel","template","customer journey map excel",90,18,None),
 ("A customer journey map template for PowerPoint","customer-journey-map-template-powerpoint","template","customer journey map powerpoint",50,18,None),
 ("A customer journey map template for Canva","customer-journey-map-canva","template","customer journey map canva",50,18,None),
 ("A B2B customer journey map template","b2b-customer-journey-map-template","template","b2b customer journey map template",90,20,None),
 ("A SaaS customer journey map template","saas-customer-journey-map-template","template","saas customer journey map template",40,18,None),
 # Tools & software
 ("The best customer journey mapping tools","best-customer-journey-mapping-tools","comparison","customer journey mapping tools",1000,30,None),
 ("Customer journey mapping software compared","customer-journey-mapping-software","comparison","customer journey mapping software",880,30,None),
 ("Free customer journey mapping tools","free-customer-journey-mapping-tools","comparison","free customer journey mapping tools",90,20,None),
 ("Customer journey mapping tools for small business","cjm-tools-for-small-business","comparison","customer journey mapping tools small business",40,18,None),
 ("Mapping the customer journey in HubSpot","hubspot-customer-journey-map","guide","hubspot customer journey map",170,22,None),
 ("Building a customer journey map in Figma","figma-customer-journey-map","guide","figma journey map",90,20,None),
 ("AI for customer journey mapping","ai-customer-journey-mapping","guide","ai customer journey map",110,24,None),
 ("Customer journey analytics tools","customer-journey-analytics-tools","comparison","customer journey analytics",1000,30,None),
 # Components
 ("The customer journey stages","customer-journey-stages","guide","customer journey stages",1000,28,None),
 ("Customer journey map stages explained","customer-journey-map-stages","guide","customer journey map stages",170,22,None),
 ("Customer journey touchpoints","customer-journey-touchpoints","guide","customer journey touchpoints",590,26,None),
 ("Customer touchpoints explained","customer-touchpoints-explained","definition","customer touchpoints",320,24,None),
 ("Using personas in journey mapping","customer-personas-for-journey-mapping","guide","customer personas",480,28,None),
 ("Finding pain points in the customer journey","customer-journey-pain-points","guide","customer journey pain points",110,20,None),
 ("Mapping customer emotions","mapping-customer-emotions","guide","customer emotions journey",40,16,None),
 ("Customer journey phases explained","customer-journey-phases","guide","customer journey phases",90,18,None),
 ("Moments of truth in the customer journey","moments-of-truth","definition","moments of truth customer experience",110,20,None),
 # Examples & by-type
 ("Customer journey map examples","customer-journey-map-examples","listicle","customer journey map examples",880,28,None),
 ("A B2B customer journey map guide","b2b-customer-journey-map","guide","b2b customer journey map",480,26,None),
 ("B2B customer journey mapping","b2b-customer-journey-mapping","guide","b2b customer journey mapping",260,24,None),
 ("A SaaS customer journey map","saas-customer-journey-map","guide","saas customer journey",170,22,None),
 ("An ecommerce customer journey map","ecommerce-customer-journey-map","guide","ecommerce customer journey map",320,24,None),
 ("The ecommerce customer journey","ecommerce-customer-journey","guide","ecommerce customer journey",880,30,None),
 ("A B2B customer journey map example","customer-journey-map-example-b2b","listicle","b2b customer journey example",110,20,None),
 ("A simple customer journey map","simple-customer-journey-map","guide","simple customer journey map",110,20,None),
 ("Digital customer journey mapping","digital-customer-journey-mapping","guide","digital customer journey mapping",480,26,None),
 ("The customer decision journey","customer-decision-journey","definition","customer decision journey",480,26,None),
]
for t, s, ctype, kw, vol, kd, money in A:
    records.append(r(t, s, "authority", ctype, "global", "informational", kw, vol, kd, money=money,
        ang=f"A practical, plain-English answer to \"{kw}\" for founder-led teams, with a clear next step."))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch05: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
