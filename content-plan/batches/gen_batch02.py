#!/usr/bin/env python3
"""Batch 2 - Revenue Operations (RevOps) (95 records).

Semrush-researched US cluster (June 2026 estimates; KD indicative). RevOps is the
confirmed umbrella pillar. Emits into content-plan/plan.json (idempotent on batch==2).
Run from repo root, then scripts/render_plan.py.
"""
import json, os

PILLAR = "Revenue Operations (RevOps)"
PID = "revops"
BATCH = 2
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "revenue-operations"

WORDS = {"pillar": 2300, "money": 1450, "guide": 1700, "how-to": 1700,
         "comparison": 1500, "definition": 1150, "listicle": 1350, "benchmark": 1350}
ENGINES = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

def llm_phrasing(kw, ctype):
    k = kw.lower()
    if ctype == "how-to" and not k.startswith(("how", "what", "why")):
        return "how do I " + kw
    if ctype == "comparison" and not k.startswith(("best", "what")):
        return "what is the difference, " + kw
    if ctype == "benchmark" and not k.startswith(("what", "average")):
        return "what is a good " + kw
    return kw

def outline(ctype):
    t = {
        "pillar": ["What RevOps is and why it matters", "The cost of disconnected revenue systems",
                   "How Lauren builds a RevOps system", "What an engagement includes", "What good looks like"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which you need and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it is measured or applied", "A practical example"],
        "listicle": ["Why this matters", "The list, with how to apply each", "Where teams go wrong"],
        "benchmark": ["The headline numbers", "How the figures break down", "How to read your own data"],
    }
    return t.get(ctype, t["guide"])

records = []
_idx = [0]

def r(title, slug, role, ctype, market, intent, kw, vol, kd, ad=False, sec=None, ang=None, money=None, lateral=None):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role in ("pillar", "money"):
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    up = [] if role == "pillar" else ([PILLAR_SLUG] if role == "money" else [PILLAR_SLUG, money or "revops-consulting"])
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
        "internal_links": {"up": up, "lateral": lateral or []},
        "external_links": [],
        "schema_required": schema,
        "ai_overview_play": "Lead with a direct definition and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
    }

# Pillar
records.append(r("Revenue operations (RevOps)", PILLAR_SLUG, "pillar", "pillar", "global", "commercial",
    "revenue operations", 2400, 38, ad=True,
    sec=["revops", "what is revops", "revenue operations consulting"],
    ang="Revenue operations (RevOps) brings CRM, sales process, pipeline and reporting into one connected system so revenue becomes predictable. This is the umbrella for how Lauren helps founder-led and SaaS teams remove the friction between marketing, sales and customer success."))

# Money (10)
M = [
 ("RevOps consultant","revops-consultant","commercial","revenue operations consultant",390,22,["revops consultant"]),
 ("RevOps consulting services","revops-consulting","commercial","revenue operations consulting",720,25,["revops consulting"]),
 ("RevOps as a service","revops-as-a-service","commercial","revops as a service",260,24,["managed revops"]),
 ("RevOps audit","revops-audit","transactional","revops audit",40,18,["revenue operations assessment"]),
 ("RevOps implementation","revops-implementation","commercial","revops implementation",110,22,["revenue operations implementation"]),
 ("Fractional RevOps leader","fractional-revops-leader","commercial","fractional revops",40,18,["fractional revenue operations"]),
 ("B2B revenue operations","b2b-revenue-operations","commercial","b2b revenue operations",90,20,["b2b revops"]),
 ("SaaS revenue operations","saas-revenue-operations","commercial","revenue operations saas",140,22,["saas revops"]),
 ("RevOps strategy engagement","revops-strategy","commercial","revops strategy",210,24,["revenue operations strategy"]),
 ("RevOps for HubSpot","hubspot-revops","commercial","hubspot revenue operations",110,26,["hubspot revops"]),
]
for t, s, intent, kw, vol, kd, sec in M:
    records.append(r(t, s, "money", "money", "US", intent, kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

# Authority (84): (title, slug, type, kw, vol, kd, money)
A = [
 # Foundations
 ("What is RevOps?","what-is-revops","definition","what is revops",880,28,None),
 ("What is revenue operations?","what-is-revenue-operations","definition","what is revenue operations",590,28,None),
 ("RevOps meaning, in plain English","revops-meaning","definition","revops meaning",390,22,None),
 ("RevOps definition and scope","revops-definition","definition","revops definition",170,20,None),
 ("Revenue operations explained for founders","revenue-operations-explained","guide","revenue operations explained",90,20,None),
 ("Why RevOps matters for growing businesses","why-revops-matters","guide","why revops",50,18,None),
 ("RevOps vs sales ops","revops-vs-sales-ops","comparison","revops vs sales ops",260,20,None),
 ("Revenue operations vs sales operations","revenue-operations-vs-sales-operations","comparison","revenue operations vs sales operations",260,20,None),
 ("RevOps vs marketing ops","revops-vs-marketing-ops","comparison","revops vs marketing ops",40,18,None),
 ("What does a RevOps function actually do?","what-does-revops-do","definition","what does revops do",90,18,None),
 # Strategy & frameworks
 ("A RevOps framework","revops-framework","guide","revops framework",210,22,"revops-consulting"),
 ("A revenue operations framework","revenue-operations-framework","guide","revenue operations framework",90,20,"revops-consulting"),
 ("How to build a RevOps strategy","revops-strategy-guide","guide","revops strategy",210,24,"revops-strategy"),
 ("A revenue operations strategy guide","revenue-operations-strategy-guide","guide","revenue operations strategy",170,22,"revops-strategy"),
 ("The RevOps maturity model","revops-maturity-model","guide","revops maturity model",40,18,"revops-consulting"),
 ("How to build a RevOps function","how-to-build-a-revops-function","how-to","build revops function",30,18,"revops-consulting"),
 ("RevOps best practices","revops-best-practices","listicle","revenue operations best practices",90,20,None),
 ("RevOps for founders","revops-for-founders","guide","revops for founders",40,18,"revops-consulting"),
 ("RevOps for startups","revops-for-startups","guide","revops for startups",40,18,"revops-consulting"),
 ("When to hire for RevOps","when-to-hire-revops","guide","when to hire revops",30,18,"fractional-revops-leader"),
 ("The RevOps operating model","revops-operating-model","guide","revenue operations operating model",40,18,"revops-consulting"),
 ("Aligning sales, marketing and customer success","aligning-sales-marketing-cs","guide","sales and marketing alignment",320,30,None),
 # Team & roles
 ("Revenue operations team structure","revenue-operations-team-structure","guide","revenue operations team structure",210,22,"revops-consulting"),
 ("The RevOps org chart","revops-org-chart","guide","revenue operations org chart",140,20,"revops-consulting"),
 ("RevOps roles explained","revops-roles-explained","guide","revops roles",50,18,None),
 ("What does a RevOps manager do?","what-does-a-revops-manager-do","definition","revenue operations manager",320,22,None),
 ("The director of revenue operations role","director-of-revenue-operations-role","guide","director of revenue operations",140,20,None),
 ("A RevOps job description template","revops-job-description","guide","revops job description",110,18,None),
 ("The RevOps analyst role","revops-analyst-role","guide","revenue operations analyst",170,20,None),
 ("How big should your RevOps team be?","revops-team-size","guide","revops team",170,20,"fractional-revops-leader"),
 ("Your first RevOps hire","first-revops-hire","guide","first revops hire",30,18,"fractional-revops-leader"),
 ("The skills a RevOps leader needs","revops-skills","guide","revops skills",40,18,None),
 # Processes & components
 ("RevOps and your CRM","revops-and-crm","guide","revops crm",50,20,"revops-implementation"),
 ("RevOps data management","revops-data-management","guide","revops data management",40,20,"revops-implementation"),
 ("RevOps and lead management","revops-lead-management","guide","revops lead management",40,20,None),
 ("RevOps and forecasting","revops-forecasting","guide","revops forecasting",40,20,None),
 ("RevOps and pipeline management","revops-pipeline-management","guide","revops pipeline management",40,20,None),
 ("RevOps and reporting","revops-reporting","guide","revops reporting",40,20,None),
 ("RevOps and process mapping","revops-process-mapping","guide","revops process",40,20,None),
 ("Building a RevOps tech stack","revops-tech-stack","guide","revops tech stack",90,22,"revops-implementation"),
 ("A guide to RevOps automation","revops-automation-guide","guide","revops automation",170,24,"revops-implementation"),
 ("RevOps data hygiene","revops-data-hygiene","guide","crm data hygiene",90,22,"revops-implementation"),
 ("The RevOps metrics that matter","revops-metrics","guide","revops metrics",50,20,None),
 ("Revenue operations KPIs","revops-kpis","guide","revenue operations kpis",70,20,None),
 ("RevOps and the customer journey","revops-and-customer-journey","guide","revops customer journey",30,18,None),
 ("Quote to cash, explained","quote-to-cash","definition","quote to cash",320,28,None),
 ("Lead to revenue: the full process","lead-to-revenue","guide","lead to revenue",90,20,None),
 ("RevOps systems integration","revops-systems-integration","guide","revops integration",40,20,"revops-implementation"),
 # Metrics & benchmarks
 ("Revenue operations metrics","revenue-operations-metrics","guide","revenue operations metrics",70,20,None),
 ("What is revenue leakage?","what-is-revenue-leakage","definition","revenue leakage",170,22,None),
 ("Net revenue retention explained","net-revenue-retention","definition","net revenue retention",480,32,None),
 ("Pipeline coverage ratio explained","pipeline-coverage-ratio","definition","pipeline coverage ratio",110,22,None),
 ("Sales velocity explained","sales-velocity","definition","sales velocity",320,28,None),
 ("CAC and LTV explained","cac-and-ltv","definition","cac ltv ratio",260,26,None),
 ("Win rate benchmarks","win-rate-benchmarks","benchmark","sales win rate",170,24,None),
 ("RevOps dashboard metrics","revops-dashboard-metrics","guide","revops dashboard",90,22,None),
 # Tools & software
 ("The best RevOps tools","best-revops-tools","comparison","revops tools",140,26,"revops-implementation"),
 ("Revenue operations software compared","revenue-operations-software","comparison","revenue operations software",260,28,"revops-implementation"),
 ("RevOps platforms compared","revops-platforms-compared","comparison","revops platform",140,26,"revops-implementation"),
 ("Salesforce vs HubSpot for RevOps","salesforce-vs-hubspot-revops","comparison","salesforce vs hubspot",2400,40,"hubspot-revops"),
 ("HubSpot for RevOps","hubspot-for-revops","guide","hubspot revops",140,24,"hubspot-revops"),
 ("RevOps tools for startups","revops-tools-for-startups","comparison","revops tools startups",40,18,None),
 ("CPQ software explained","cpq-software","comparison","cpq software",1600,40,None),
 ("Revenue intelligence tools","revenue-intelligence-tools","comparison","revenue intelligence",480,32,None),
 ("Data enrichment tools for RevOps","data-enrichment-tools","comparison","data enrichment tools",320,30,None),
 ("Free RevOps tools","free-revops-tools","listicle","free revops tools",30,18,None),
 # Sales ops adjacent
 ("What is sales operations?","what-is-sales-operations","definition","what is sales operations",320,24,None),
 ("Sales operations strategy","sales-operations-strategy","guide","sales operations strategy",110,22,None),
 ("Sales operations team structure","sales-operations-team-structure","guide","sales operations team structure",110,22,None),
 ("Sales operations best practices","sales-operations-best-practices","listicle","sales operations best practices",50,18,None),
 ("Sales ops vs RevOps","sales-ops-vs-revops","comparison","sales ops vs revops",110,20,None),
 ("Sales operations tools","sales-operations-tools","comparison","sales operations tools",110,24,None),
 ("Sales operations metrics","sales-operations-metrics","guide","sales operations metrics",50,18,None),
 ("Marketing operations explained","marketing-operations-explained","definition","marketing operations",480,32,None),
 ("Customer success operations explained","customer-success-operations","definition","customer success operations",90,20,None),
 ("Deal desk explained","deal-desk-explained","definition","deal desk",260,26,None),
 # Use-case / outcomes
 ("RevOps for SaaS","revops-for-saas","guide","revenue operations saas",140,22,"saas-revenue-operations"),
 ("RevOps for B2B businesses","revops-for-b2b","guide","b2b revenue operations",90,20,"b2b-revenue-operations"),
 ("RevOps for agencies","revops-for-agencies","guide","revops for agencies",40,18,"revops-consulting"),
 ("RevOps for professional services","revops-for-professional-services","guide","revops professional services",30,18,"revops-consulting"),
 ("The ROI of RevOps","revops-roi","guide","revops roi",40,18,"revops-consulting"),
 ("Signs you need RevOps","signs-you-need-revops","guide","signs you need revops",30,18,"revops-consulting"),
 ("A RevOps implementation roadmap","revops-implementation-roadmap","how-to","revops implementation roadmap",40,18,"revops-implementation"),
 ("How to approach a RevOps project","revops-project-approach","guide","revops project",30,18,"revops-consulting"),
]
for t, s, ctype, kw, vol, kd, money in A:
    market = "global" if ctype in ("definition", "comparison", "benchmark") else "US"
    records.append(r(t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money,
        ang=f"A practical, plain-English answer to \"{kw}\" for founder-led and SaaS teams, with a clear next step."))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    roles = {}
    for x in records:
        roles[x["role"]] = roles.get(x["role"], 0) + 1
    print(f"batch02: wrote {len(records)} records ({roles}). plan.json now {len(plan)} records.")

if __name__ == "__main__":
    main()
