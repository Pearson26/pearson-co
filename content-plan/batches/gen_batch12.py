#!/usr/bin/env python3
"""Batch 12 - CRM Consulting & Selection (70 records).

High-intent hiring language (universe: consultant crm, zoho crm consultants, best crm for X).
Holds the platform-vs-platform comparisons and best-CRM-for-[sector] content reserved from
Batch 3. Money-heavy. Volumes indicative (universe doc + domain knowledge). Idempotent on
batch==12.
"""
import json, os

PILLAR = "CRM Consulting & Selection"
PID = "crm-consulting"
BATCH = 12
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "crm-consulting"
DEF_MONEY = "crm-consultant-service"

WORDS = {"pillar": 2200, "money": 1450, "guide": 1650, "how-to": 1700,
         "comparison": 1550, "definition": 1150, "listicle": 1350, "template": 1250}
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
        "pillar": ["What CRM consulting and selection involve", "Why the right CRM and adviser matter",
                   "How Lauren helps you choose and get value", "What an engagement includes", "How to start"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["What to weigh up", "The options compared", "Which to choose and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it works", "A practical example"],
        "listicle": ["What to look for", "The shortlist, with who each suits", "How to decide"],
        "template": ["What the template covers", "How to use it", "A worked example"],
    }
    return t.get(ctype, t["guide"])

records = []
_idx = [0]

def r(title, slug, role, ctype, kw, vol, kd, ad=False, sec=None, ang=None, money=None, market="UK"):
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
        "title": title, "url_slug": slug, "target_market": market,
        "intent": ("commercial" if role in ("pillar", "money") else "informational"),
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams choosing a CRM or an adviser, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short shortlist or checklist so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillar
records.append(r("CRM consulting and selection", PILLAR_SLUG, "pillar", "pillar",
    "crm consulting", 480, 32, ad=False,
    sec=["crm consultant", "crm consultancy", "best crm for small business"],
    ang="A CRM consultant helps you choose the right CRM and get real value from it, rather than buying software that no one uses. This is how Lauren advises on selection, fit and the work that turns a CRM into a system your team trusts."))

# Money (14)
CC = "crm-consultant-service"; CY = "crm-consultancy"; OPT = "crm-optimisation-service"; STR = "crm-strategy-consulting"
M = [
 ("CRM consultant","crm-consultant-service","crm consultant",480,30,["crm consulting"]),
 ("CRM consultancy","crm-consultancy","crm consultancy",320,28,["crm consulting firm"]),
 ("HubSpot consultant","hubspot-consultant","hubspot consultant",880,34,["hubspot consulting"]),
 ("Salesforce consultant","salesforce-consultant","salesforce consultant",1900,40,["salesforce consulting"]),
 ("Zoho CRM consultant","zoho-crm-consultant","zoho crm consultant",320,28,["zoho consultant"]),
 ("Pipedrive consultant","pipedrive-consultant","pipedrive consultant",170,24,["pipedrive expert"]),
 ("monday CRM consultant","monday-crm-consultant","monday crm consultant",110,22,["monday.com consultant"]),
 ("CRM consultant for startups","crm-consultant-for-startups","crm consultant startups",70,22,["startup crm consultant"]),
 ("CRM consultant for small business","crm-consultant-for-small-business","crm consultant small business",90,22,["small business crm consultant"]),
 ("CRM for real estate","crm-consultant-real-estate","crm for real estate",1300,36,["real estate crm consultant"]),
 ("CRM for recruitment","crm-consultant-recruitment","crm for recruitment",480,30,["recruitment crm consultant"]),
 ("CRM for professional services","crm-consultant-professional-services","crm for professional services",170,26,["professional services crm"]),
 ("CRM strategy consulting","crm-strategy-consulting","crm strategy",480,30,["crm strategy consultant"]),
 ("CRM optimisation service","crm-optimisation-service","crm optimisation",320,28,["crm optimization"]),
]
for t, s, kw, vol, kd, sec in M:
    records.append(r(t, s, "money", "money", kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

A = [
 # Platform comparisons (14)
 ("Salesforce vs HubSpot","salesforce-vs-hubspot","comparison","salesforce vs hubspot",2400,40,"salesforce-consultant"),
 ("HubSpot vs Zoho CRM","hubspot-vs-zoho","comparison","hubspot vs zoho",880,34,"hubspot-consultant"),
 ("HubSpot vs Pipedrive","hubspot-vs-pipedrive","comparison","hubspot vs pipedrive",880,34,"hubspot-consultant"),
 ("Salesforce vs Zoho CRM","salesforce-vs-zoho","comparison","salesforce vs zoho",480,32,"salesforce-consultant"),
 ("Zoho CRM vs Pipedrive","zoho-vs-pipedrive","comparison","zoho vs pipedrive",320,28,"zoho-crm-consultant"),
 ("monday CRM vs HubSpot","monday-vs-hubspot","comparison","monday vs hubspot",320,30,"monday-crm-consultant"),
 ("HubSpot vs Salesforce vs Zoho","hubspot-vs-salesforce-vs-zoho","comparison","hubspot vs salesforce vs zoho",170,30,None),
 ("The best CRM software","best-crm-software","comparison","best crm software",6600,44,None),
 ("CRM software comparison","crm-software-comparison","comparison","crm software comparison",480,32,None),
 ("A HubSpot review","hubspot-review","comparison","hubspot review",1300,34,"hubspot-consultant"),
 ("A Salesforce review","salesforce-review","comparison","salesforce review",880,34,"salesforce-consultant"),
 ("A Zoho CRM review","zoho-crm-review","comparison","zoho crm review",880,32,"zoho-crm-consultant"),
 ("A Pipedrive review","pipedrive-review","comparison","pipedrive review",1300,34,"pipedrive-consultant"),
 ("A monday CRM review","monday-crm-review","comparison","monday crm review",320,28,"monday-crm-consultant"),
 # Best CRM for [sector] (16)
 ("The best CRM for small business","best-crm-for-small-business","comparison","best crm for small business",6600,44,"crm-consultant-for-small-business"),
 ("The best CRM for startups","best-crm-for-startups","comparison","best crm for startups",1900,38,"crm-consultant-for-startups"),
 ("The best CRM for real estate","best-crm-for-real-estate","comparison","best crm for real estate",2400,40,"crm-consultant-real-estate"),
 ("The best CRM for recruitment","best-crm-for-recruitment","comparison","best crm for recruitment",880,34,"crm-consultant-recruitment"),
 ("The best CRM for consultants","best-crm-for-consultants","comparison","best crm for consultants",480,32,CC),
 ("The best CRM for SaaS","best-crm-for-saas","comparison","best crm for saas",480,32,None),
 ("The best CRM for B2B","best-crm-for-b2b","comparison","best crm for b2b",480,32,None),
 ("The best CRM for ecommerce","best-crm-for-ecommerce","comparison","best crm for ecommerce",880,34,None),
 ("The best CRM for nonprofits","best-crm-for-nonprofits","comparison","best crm for nonprofits",1300,36,None),
 ("The best CRM for hospitality","best-crm-for-hospitality","comparison","best crm for hospitality",170,26,None),
 ("The best CRM for hotels","best-crm-for-hotels","comparison","best crm for hotels",320,28,None),
 ("The best CRM for restaurants","best-crm-for-restaurants","comparison","best crm for restaurants",170,26,None),
 ("The best CRM for professional services","best-crm-for-professional-services","comparison","best crm for professional services",170,26,"crm-consultant-professional-services"),
 ("The best CRM for financial advisors","best-crm-for-financial-advisors","comparison","best crm for financial advisors",880,34,None),
 ("The best CRM for agencies","best-crm-for-agencies","comparison","best crm for agencies",480,30,None),
 ("The best free CRM","best-free-crm","comparison","best free crm",6600,42,None),
 # Consultant / hiring guides (12)
 ("What does a CRM consultant do?","what-does-a-crm-consultant-do","definition","what does a crm consultant do",170,22,CC),
 ("What is CRM consulting?","what-is-crm-consulting","definition","what is crm consulting",110,22,CY),
 ("When to hire a CRM consultant","when-to-hire-a-crm-consultant","guide","when to hire a crm consultant",70,20,CC),
 ("How to choose a CRM consultant","how-to-choose-a-crm-consultant","how-to","how to choose a crm consultant",90,22,CC),
 ("How much does a CRM consultant cost?","crm-consultant-cost","guide","crm consultant cost",110,22,CC),
 ("Signs you need a CRM consultant","signs-you-need-a-crm-consultant","guide","signs you need a crm consultant",40,18,CC),
 ("CRM consultant vs CRM developer","crm-consultant-vs-developer","comparison","crm consultant vs developer",40,18,None),
 ("The benefits of a CRM consultant","benefits-of-a-crm-consultant","listicle","benefits of crm consultant",40,18,CC),
 ("CRM consulting services explained","crm-consulting-services-explained","guide","crm consulting services",170,24,CY),
 ("Questions to ask a CRM consultant","crm-consultant-questions","guide","crm consultant questions",40,18,CC),
 ("Hiring a HubSpot consultant","hiring-a-hubspot-consultant","guide","hire hubspot consultant",170,26,"hubspot-consultant"),
 ("Hiring a Salesforce consultant","hiring-a-salesforce-consultant","guide","hire salesforce consultant",170,28,"salesforce-consultant"),
 # Selection deep-dives (13)
 ("A CRM guide for small business","crm-for-small-business-guide","guide","crm for small business",1300,34,"crm-consultant-for-small-business"),
 ("A CRM guide for startups","crm-for-startups-guide","guide","crm for startups",880,32,"crm-consultant-for-startups"),
 ("Do you need a CRM consultant?","do-you-need-a-crm-consultant","guide","do i need a crm consultant",40,18,CC),
 ("Working with a CRM migration consultant","crm-migration-consultant","guide","crm migration consultant",70,22,CC),
 ("A CRM optimisation guide","crm-optimisation-guide","guide","crm optimisation",320,28,OPT),
 ("How to get the most from your CRM","get-the-most-from-your-crm","guide","get more from your crm",70,20,OPT),
 ("A CRM health check","crm-health-check","guide","crm health check",110,22,OPT),
 ("How to run a CRM review","crm-review-process","how-to","crm review",90,22,OPT),
 ("How to switch CRM","switching-crm","how-to","switching crm",170,24,"crm-migration-consultant"),
 ("CRM vs a marketing automation platform","crm-vs-marketing-platform","comparison","crm vs marketing automation",110,22,None),
 ("Open source CRM explained","open-source-crm","comparison","open source crm",1900,36,None),
 ("The best CRM for a service business","crm-for-service-business","guide","crm for service business",320,28,None),
 ("How to write CRM requirements","crm-requirements-guide","how-to","crm requirements",90,22,STR),
]
for t, s, ctype, kw, vol, kd, money in A:
    market = "global" if ctype == "comparison" else "UK"
    records.append(r(t, s, "authority", ctype, kw, vol, kd, money=money, market=market))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch12: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
