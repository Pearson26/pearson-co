#!/usr/bin/env python3
"""Batch 6 - Customer Journey Mapping, part 2 (60 authority records).

Completes the CJM pillar (120 total). Volumes are INDICATIVE estimates (Semrush API units
exhausted; grounded in the keyword-universe doc, prior Semrush pulls and domain knowledge),
to be refreshed when units are topped up. Idempotent on batch==6.
Run from repo root, then scripts/render_plan.py.
"""
import json, os

PILLAR = "Customer Journey Mapping"
PID = "customer-journey"
BATCH = 6
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "customer-journey-mapping"
DEF_MONEY = "customer-journey-mapping-service"

WORDS = {"guide": 1650, "how-to": 1700, "comparison": 1500, "definition": 1150,
         "listicle": 1350, "template": 1250}
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

def r(title, slug, ctype, kw, vol, kd, money=None):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if ctype == "how-to":
        schema.append("HowTo")
    return {
        "seq": None, "batch": BATCH, "pillar": PILLAR, "pillar_id": PID,
        "role": "authority", "content_type": ctype, "is_ad_landing": False,
        "title": title, "url_slug": slug, "target_market": "global", "intent": "informational",
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": f"A practical, plain-English answer to \"{kw}\" for founder-led teams, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype, 1500),
        "internal_links": {"up": [PILLAR_SLUG, money or DEF_MONEY], "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct definition and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
        "volume_source": "indicative",
    }

CONS = "customer-journey-mapping-consultant"
CX = "customer-experience-consulting"
WS = "customer-journey-mapping-workshop"

A = [
 # Industry-specific (14)
 ("An insurance customer journey map","insurance-customer-journey-map","guide","insurance customer journey map",390,24,CONS),
 ("A retail customer journey map","retail-customer-journey-map","guide","retail customer journey map",170,22,CONS),
 ("A banking customer journey map","banking-customer-journey-map","guide","retail banking customer journey map",140,22,CONS),
 ("A healthcare patient journey map","healthcare-customer-journey-map","guide","patient journey map",320,24,CONS),
 ("A hotel guest journey map","hotel-guest-journey-map","guide","hotel guest journey",90,20,CONS),
 ("A restaurant customer journey map","restaurant-customer-journey","guide","restaurant customer journey",50,18,CONS),
 ("A travel customer journey map","travel-customer-journey-map","guide","travel customer journey",110,20,CONS),
 ("A student journey map for education","education-student-journey-map","guide","student journey map",90,20,CONS),
 ("An automotive customer journey map","automotive-customer-journey","guide","automotive customer journey",70,20,CONS),
 ("A telecom customer journey map","telecom-customer-journey-map","guide","telecom customer journey",50,18,CONS),
 ("A fintech customer journey map","fintech-customer-journey","guide","fintech customer journey",40,18,CONS),
 ("A real estate customer journey map","real-estate-customer-journey","guide","real estate customer journey",50,18,CONS),
 ("A B2B SaaS customer journey map","b2b-saas-customer-journey","guide","b2b saas customer journey",70,20,CONS),
 ("A donor journey map for nonprofits","nonprofit-donor-journey-map","guide","donor journey map",40,18,CONS),
 # Stage & lifecycle (12)
 ("The awareness stage of the customer journey","awareness-stage-journey","guide","awareness stage customer journey",90,20,None),
 ("The consideration stage of the customer journey","consideration-stage-journey","guide","consideration stage customer journey",70,20,None),
 ("The decision stage of the customer journey","decision-stage-journey","guide","decision stage customer journey",70,20,None),
 ("The retention stage of the customer journey","retention-stage-journey","guide","customer retention journey",110,22,None),
 ("The advocacy stage of the customer journey","advocacy-stage-journey","guide","customer advocacy",170,22,None),
 ("The customer onboarding journey","customer-onboarding-journey","guide","customer onboarding journey",320,26,None),
 ("The post-purchase customer journey","post-purchase-journey","guide","post purchase journey",90,20,None),
 ("The customer lifecycle stages","customer-lifecycle-stages","definition","customer lifecycle",880,30,None),
 ("Customer lifecycle vs customer journey","customer-lifecycle-vs-journey","comparison","customer lifecycle vs journey",40,18,None),
 ("The renewal journey","renewal-journey-map","guide","renewal customer journey",40,18,None),
 ("The win-back journey","win-back-journey","guide","win back customer",110,22,None),
 ("The customer loyalty journey","loyalty-journey-map","guide","customer loyalty journey",70,20,None),
 # CX concepts (12)
 ("CX vs UX explained","cx-vs-ux","comparison","cx vs ux",320,26,CX),
 ("Voice of the customer explained","voice-of-the-customer","definition","voice of the customer",1900,34,CX),
 ("Net promoter score (NPS) explained","nps-explained","definition","net promoter score",4400,42,CX),
 ("Customer satisfaction score (CSAT) explained","csat-explained","definition","customer satisfaction score",880,30,CX),
 ("Customer effort score (CES) explained","customer-effort-score","definition","customer effort score",480,28,CX),
 ("Service blueprints explained","service-blueprint","definition","service blueprint",1900,34,CX),
 ("Empathy maps explained","empathy-map","definition","empathy map",2400,36,CX),
 ("Experience map vs journey map","experience-map-vs-journey-map","comparison","experience map",480,28,CX),
 ("Building a customer feedback loop","customer-feedback-loop","guide","customer feedback",1300,32,CX),
 ("Touchpoint analysis explained","touchpoint-analysis","guide","touchpoint analysis",70,20,CX),
 ("The omnichannel customer journey","omnichannel-customer-journey","guide","omnichannel customer journey",140,24,CX),
 ("How to improve customer satisfaction","customer-satisfaction-guide","guide","customer satisfaction",2400,36,CX),
 # Operational & measurement (12)
 ("A guide to customer journey analytics","customer-journey-analytics-guide","guide","customer journey analytics",1000,30,None),
 ("Customer journey KPIs","customer-journey-kpis","guide","customer journey kpis",50,18,None),
 ("How to measure the customer journey","how-to-measure-customer-journey","how-to","measure customer journey",40,18,None),
 ("Connecting your journey map to your CRM","journey-map-to-crm","guide","customer journey crm",90,22,None),
 ("Linking the customer journey to revenue","linking-journey-map-to-revenue","guide","customer journey revenue",40,18,None),
 ("Customer journey orchestration","customer-journey-orchestration","guide","customer journey orchestration",320,28,None),
 ("Personalisation across the customer journey","personalisation-in-the-journey","guide","customer journey personalisation",90,22,None),
 ("How to reduce customer friction","reducing-customer-friction","guide","customer friction",170,22,None),
 ("Current state vs future state journey maps","current-vs-future-state-journey-map","comparison","future state journey map",70,20,None),
 ("How to run a customer journey audit","customer-journey-audit","how-to","customer journey audit",90,20,CONS),
 ("Mapping the buyer journey","mapping-the-buyer-journey","guide","buyer journey",880,30,None),
 ("Buyer journey vs customer journey","buyer-journey-vs-customer-journey","comparison","buyer journey vs customer journey",70,20,None),
 # Touchpoints, channels, formats (10)
 ("The website in the customer journey","website-in-the-customer-journey","guide","website customer journey",90,20,None),
 ("Email in the customer journey","email-in-the-customer-journey","guide","email customer journey",70,20,None),
 ("The customer support journey","customer-support-journey","guide","customer support journey",90,20,None),
 ("Sales touchpoints in the customer journey","sales-touchpoints","guide","sales touchpoints",110,20,None),
 ("A day-in-the-life map","day-in-the-life-map","guide","day in the life map",90,20,WS),
 ("A service blueprint template","service-blueprint-template","template","service blueprint template",480,26,None),
 ("An empathy map template","empathy-map-template","template","empathy map template",880,28,None),
 ("A customer journey map for startups","customer-journey-map-for-startups","guide","startup customer journey",70,20,None),
 ("A customer journey map for small business","customer-journey-map-for-small-business","guide","small business customer journey",90,20,None),
 ("Who should own the customer journey map?","who-owns-the-customer-journey","guide","customer journey ownership",30,16,None),
]
for t, s, ctype, kw, vol, kd, money in A:
    records.append(r(t, s, ctype, kw, vol, kd, money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"batch06: wrote {len(records)} authority records. plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
