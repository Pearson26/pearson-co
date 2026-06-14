#!/usr/bin/env python3
"""Batch 3 - CRM Implementation & Selection (70 records).

Semrush-researched US + UK clusters (June 2026 estimates; KD indicative). Money-heavy
pillar; the UK "CRM Services" paid campaign lands on this pillar. Platform-vs-platform and
"best CRM for [sector]" comparisons are reserved for Batch 12 (CRM Consulting & Selection).
Idempotent on batch==3. Run from repo root, then scripts/render_plan.py.
"""
import json, os

PILLAR = "CRM Implementation & Selection"
PID = "crm-implementation"
BATCH = 3
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "crm-implementation"

WORDS = {"pillar": 2200, "money": 1450, "guide": 1650, "how-to": 1700,
         "comparison": 1500, "definition": 1150, "listicle": 1350, "template": 1300, "benchmark": 1300}
ENGINES = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

def llm_phrasing(kw, ctype):
    k = kw.lower()
    if ctype == "how-to" and not k.startswith(("how", "what", "why")):
        return "how do I " + kw
    if ctype == "comparison" and not k.startswith(("best", "what", "which")):
        return "which is better, " + kw
    return kw

def outline(ctype):
    t = {
        "pillar": ["What CRM implementation and selection involve", "Why projects stall or fail",
                   "How Lauren runs an implementation", "Choosing the right CRM", "What an engagement includes"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["What to weigh up", "The options compared", "Which to choose and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it works", "A practical example"],
        "listicle": ["Why this matters", "The list, with how to apply each", "Where teams go wrong"],
        "template": ["What the template covers", "How to use it", "A worked example"],
        "benchmark": ["The headline numbers", "How the figures break down", "How to read your own data"],
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
    up = [] if role == "pillar" else ([PILLAR_SLUG] if role == "money" else [PILLAR_SLUG, money or "crm-implementation-services"])
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
        "external_links": [],
        "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
    }

# Pillar
records.append(r("CRM implementation and selection", PILLAR_SLUG, "pillar", "pillar", "UK", "commercial",
    "crm implementation", 2400, 32, ad=True,
    sec=["crm implementation services", "crm implementation consultant", "how to implement a crm"],
    ang="CRM implementation is the work of choosing, setting up and rolling out a CRM so a team actually uses it and leadership trusts the data. Most projects fail on adoption, not software. This is how Lauren leads selection and implementation for founder-led teams."))

# Money (14)
M = [
 ("CRM implementation services","crm-implementation-services","commercial","crm implementation services",480,20,True,["crm implementation company"]),
 ("CRM implementation consultant","crm-implementation-consultant","commercial","crm implementation consultant",210,18,True,["crm implementation consultancy"]),
 ("CRM implementation pricing","crm-implementation-cost","transactional","crm implementation cost",90,18,False,["crm implementation pricing"]),
 ("CRM audit","crm-audit","transactional","crm audit",50,12,True,["crm health check"]),
 ("HubSpot implementation","hubspot-implementation","commercial","hubspot crm implementation",390,26,False,["hubspot onboarding"]),
 ("Salesforce implementation","salesforce-implementation","commercial","salesforce crm implementation",320,30,False,["salesforce setup"]),
 ("Zoho CRM implementation","zoho-crm-implementation","commercial","zoho crm implementation",110,22,False,["zoho crm setup"]),
 ("Microsoft Dynamics CRM implementation","dynamics-crm-implementation","commercial","microsoft dynamics crm implementation",110,24,False,["dynamics 365 implementation"]),
 ("Pipedrive implementation","pipedrive-implementation","commercial","pipedrive implementation",50,18,False,["pipedrive setup"]),
 ("CRM data migration service","crm-data-migration","transactional","crm data migration",90,22,False,["crm migration service"]),
 ("CRM setup for startups","crm-setup-for-startups","commercial","crm for startups",70,20,False,["startup crm setup"]),
 ("CRM implementation partner","crm-implementation-partner","commercial","crm implementation partner",90,20,False,["crm implementation partners"]),
 ("CRM selection service","crm-selection-service","commercial","crm selection",50,18,False,["crm selection consultant"]),
 ("CRM onboarding and training","crm-onboarding","commercial","crm onboarding",40,18,False,["crm training"]),
]
for t, s, intent, kw, vol, kd, ad, sec in M:
    records.append(r(t, s, "money", "money", "UK", intent, kw, vol, kd, ad=ad, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

# Authority (55): (title, slug, type, kw, vol, kd, money)
A = [
 # Process & how-to
 ("The CRM implementation process","crm-implementation-process","how-to","crm implementation process",170,20,None),
 ("CRM implementation steps","crm-implementation-steps","how-to","crm implementation steps",170,20,None),
 ("How to implement a CRM","how-to-implement-a-crm","how-to","how to implement a crm",140,22,None),
 ("How to write a CRM implementation plan","crm-implementation-plan","guide","crm implementation plan",260,22,None),
 ("A CRM implementation plan template","crm-implementation-plan-template","template","crm implementation plan template",70,18,None),
 ("A CRM implementation checklist","crm-implementation-checklist","template","crm implementation checklist",70,18,None),
 ("A realistic CRM implementation timeline","crm-implementation-timeline","guide","crm implementation timeline",110,20,None),
 ("Building a CRM implementation roadmap","crm-implementation-roadmap","guide","crm implementation roadmap",90,20,None),
 ("The phases of a CRM implementation","crm-implementation-phases","guide","crm implementation phases",50,18,None),
 ("CRM implementation best practices","crm-implementation-best-practices","listicle","crm implementation best practices",140,20,None),
 ("CRM requirements gathering","crm-requirements-gathering","how-to","crm requirements",90,20,"crm-selection-service"),
 ("A CRM implementation project plan","crm-implementation-project-plan","guide","crm implementation project plan",140,22,None),
 ("How to plan a CRM rollout","crm-rollout-plan","how-to","crm rollout",70,18,"crm-onboarding"),
 ("A CRM go-live checklist","crm-go-live-checklist","template","crm go live checklist",40,18,None),
 # Cost & ROI
 ("How much does a CRM cost?","how-much-does-a-crm-cost","guide","how much does a crm cost",320,24,"crm-implementation-cost"),
 ("CRM pricing explained","crm-pricing-explained","guide","crm pricing",480,28,"crm-implementation-cost"),
 ("The ROI of a CRM","crm-roi","guide","crm roi",170,22,None),
 ("The hidden costs of a CRM","hidden-costs-of-crm","guide","crm costs",90,20,"crm-implementation-cost"),
 ("CRM total cost of ownership","crm-tco","guide","crm total cost of ownership",40,18,"crm-implementation-cost"),
 ("CRM implementation cost factors","crm-implementation-cost-factors","guide","crm implementation cost breakdown",40,18,"crm-implementation-cost"),
 # Why fail / challenges
 ("Why CRM implementations fail","why-crm-implementations-fail","guide","why crm implementations fail",70,18,"crm-implementation-consultant"),
 ("Common CRM implementation challenges","crm-implementation-challenges","guide","crm implementation challenges",70,18,None),
 ("CRM implementation mistakes to avoid","crm-implementation-mistakes","listicle","crm implementation mistakes",50,18,None),
 ("CRM implementation risks","crm-implementation-risks","guide","crm implementation risks",40,18,None),
 ("Barriers to CRM implementation","barriers-to-crm-implementation","guide","barriers to crm implementation",50,18,None),
 ("The CRM project failure rate","crm-implementation-failure-rate","benchmark","crm failure rate",40,18,None),
 # Selection / choosing
 ("How to choose a CRM","how-to-choose-a-crm","how-to","how to choose a crm",320,26,"crm-selection-service"),
 ("CRM selection criteria","crm-selection-criteria","guide","crm selection criteria",110,22,"crm-selection-service"),
 ("A CRM requirements checklist","crm-requirements-checklist","template","crm requirements checklist",70,18,"crm-selection-service"),
 ("A CRM RFP template","crm-rfp-template","template","crm rfp template",70,18,"crm-selection-service"),
 ("How to compare CRMs","crm-comparison-guide","comparison","crm comparison",480,30,"crm-selection-service"),
 ("Signs you need a CRM","signs-you-need-a-crm","guide","do i need a crm",320,24,None),
 ("When to implement a CRM","when-to-get-a-crm","guide","when to implement crm",50,18,None),
 ("A CRM buying guide","crm-buying-guide","guide","crm buying guide",90,20,"crm-selection-service"),
 ("Cloud CRM vs on-premise","cloud-vs-on-premise-crm","comparison","cloud crm vs on premise",50,18,None),
 ("CRM features to look for","crm-features-to-look-for","guide","crm features",320,26,None),
 ("CRM vs spreadsheets","crm-vs-spreadsheet","comparison","crm vs excel",110,20,None),
 ("Questions to ask in a CRM demo","crm-demo-questions","guide","crm demo questions",40,18,"crm-selection-service"),
 # Platform setup guides
 ("How to implement HubSpot CRM","how-to-implement-hubspot-crm","how-to","hubspot crm implementation",390,26,"hubspot-implementation"),
 ("How to implement Salesforce","how-to-implement-salesforce","how-to","salesforce crm implementation",320,30,"salesforce-implementation"),
 ("How to set up Zoho CRM","how-to-set-up-zoho-crm","how-to","zoho crm setup",110,22,"zoho-crm-implementation"),
 ("A Dynamics 365 CRM implementation guide","dynamics-365-implementation-guide","how-to","dynamics 365 crm implementation",110,24,"dynamics-crm-implementation"),
 ("A Pipedrive setup guide","pipedrive-setup-guide","how-to","pipedrive setup",70,18,"pipedrive-implementation"),
 ("A monday CRM setup guide","monday-crm-setup","how-to","monday crm setup",90,20,None),
 ("A NetSuite CRM implementation guide","netsuite-crm-implementation-guide","how-to","netsuite crm implementation",110,24,None),
 ("A CRM integration guide","crm-integration-guide","guide","crm integration",320,28,"crm-data-migration"),
 ("How to migrate CRM data","crm-data-migration-guide","how-to","crm data migration",90,22,"crm-data-migration"),
 # Data, team, examples, adoption-adjacent
 ("CRM data migration best practices","crm-data-migration-best-practices","guide","crm migration best practices",70,20,"crm-data-migration"),
 ("Who you need on a CRM implementation team","crm-implementation-team","guide","crm implementation team",40,18,None),
 ("CRM implementation examples","crm-implementation-examples","guide","crm implementation examples",50,18,None),
 ("CRM implementation KPIs","crm-implementation-kpis","guide","crm implementation kpis",30,18,None),
 ("Driving CRM adoption during rollout","crm-user-adoption-during-implementation","guide","crm user adoption",90,22,"crm-onboarding"),
 ("Testing a CRM before launch","crm-testing-before-launch","guide","crm testing",40,18,None),
 ("CRM customisation vs configuration","crm-customisation-vs-configuration","comparison","crm customisation",90,20,None),
 ("CRM implementation for small business","crm-implementation-for-small-business","guide","crm for small business",320,26,"crm-setup-for-startups"),
]
for t, s, ctype, kw, vol, kd, money in A:
    market = "global" if ctype in ("comparison", "definition", "benchmark", "template") else "UK"
    records.append(r(t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money,
        ang=f"A practical, plain-English answer to \"{kw}\" for founder-led teams choosing or rolling out a CRM, with a clear next step."))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    roles = {}
    for x in records:
        roles[x["role"]] = roles.get(x["role"], 0) + 1
    print(f"batch03: wrote {len(records)} records ({roles}). plan.json now {len(plan)} records.")

if __name__ == "__main__":
    main()
