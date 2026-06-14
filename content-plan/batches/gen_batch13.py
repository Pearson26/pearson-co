#!/usr/bin/env python3
"""Batch 13 - CRM Adoption (35) + Sales Pipeline Management (30) = 65 records.

Two authority pillars. CRM Adoption is Lauren's own specialism (failed adoption is often the
real problem behind a CRM enquiry). Sales Pipeline supports the CRM and forecasting pillars.
De-duplicated against pipeline/velocity terms in Batches 2 and 11. Volumes indicative.
Idempotent on batch==13.
"""
import json, os

BATCH = 13
PLAN = "content-plan/plan.json"
WORDS = {"pillar": 2100, "money": 1450, "guide": 1650, "how-to": 1700,
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
        "pillar": ["What it is and why it matters", "The real cost of getting it wrong",
                   "How Lauren approaches it", "What good looks like", "What an engagement includes"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which to use and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it works", "A practical example"],
        "listicle": ["Why this matters", "The list, with how to apply each", "Where teams go wrong"],
        "template": ["What the template covers", "How to use it", "A worked example"],
    }
    return t.get(ctype, t["guide"])

records = []
_idx = [0]

def r(pillar, pid, pslug, dmoney, title, slug, role, ctype, kw, vol, kd, sec=None, ang=None, money=None, market="global"):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role in ("pillar", "money"):
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    if role == "pillar":
        up = []
    elif role == "money":
        up = [pslug]
    else:
        up = [pslug] + ([money] if money else [])
    return {
        "seq": None, "batch": BATCH, "pillar": pillar, "pillar_id": pid,
        "role": role, "content_type": ctype, "is_ad_landing": False,
        "title": title, "url_slug": slug, "target_market": market,
        "intent": ("commercial" if role in ("pillar", "money") else "informational"),
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# ===================== CRM Adoption (35) =====================
AP, AID, ASLUG, AMON = "CRM Adoption", "crm-adoption", "crm-adoption", "crm-adoption-consulting"
records.append(r(AP, AID, ASLUG, AMON, "CRM adoption", ASLUG, "pillar", "pillar",
    "crm adoption", 480, 28, sec=["crm user adoption", "crm adoption strategy", "why crm fails"],
    ang="CRM adoption is whether your team actually uses the CRM, day to day, the way it was meant to be used. Most CRM disappointment is an adoption problem, not a software one. This is Lauren's specialism: getting teams to use the CRM so the data, and the decisions built on it, can be trusted."))
ADM = [
 ("CRM adoption consulting","crm-adoption-consulting","crm adoption consulting",70,22,["crm adoption services"]),
 ("CRM training service","crm-training-service","crm training",480,28,["crm team training"]),
]
for t, s, kw, vol, kd, sec in ADM:
    records.append(r(AP, AID, ASLUG, AMON, t, s, "money", "money", kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))
TRN = "crm-training-service"
ADA = [
 ("What is CRM adoption?","what-is-crm-adoption","definition","what is crm adoption",170,22,None),
 ("CRM adoption rate explained","crm-adoption-rate","definition","crm adoption rate",110,22,None),
 ("How to measure CRM adoption","how-to-measure-crm-adoption","how-to","measure crm adoption",70,20,None),
 ("A CRM adoption strategy","crm-adoption-strategy","guide","crm adoption strategy",170,24,None),
 ("CRM adoption best practices","crm-adoption-best-practices","listicle","crm adoption best practices",90,20,None),
 ("Why CRM adoption fails","why-crm-adoption-fails","guide","why crm adoption fails",90,20,None),
 ("CRM user adoption explained","crm-user-adoption","guide","crm user adoption",170,22,None),
 ("CRM adoption challenges","crm-adoption-challenges","guide","crm adoption challenges",70,20,None),
 ("The benefits of strong CRM adoption","benefits-of-crm-adoption","listicle","benefits of crm adoption",40,18,None),
 ("CRM adoption metrics","crm-adoption-metrics","guide","crm adoption metrics",70,20,None),
 ("How to improve CRM adoption","how-to-improve-crm-adoption","how-to","how to improve crm adoption",170,24,AMON),
 ("How to get your team to use the CRM","get-your-team-to-use-the-crm","how-to","get team to use crm",90,22,AMON),
 ("A CRM adoption plan","crm-adoption-plan","template","crm adoption plan",70,20,AMON),
 ("CRM change management","crm-change-management","guide","crm change management",170,24,AMON),
 ("A CRM training plan","crm-training-plan","template","crm training plan",110,22,TRN),
 ("CRM training best practices","crm-training-best-practices","listicle","crm training best practices",70,20,TRN),
 ("CRM onboarding for teams","crm-onboarding-for-teams","guide","crm onboarding",90,22,TRN),
 ("CRM gamification","crm-gamification","guide","crm gamification",170,24,None),
 ("Incentivising CRM use","incentivising-crm-use","guide","crm incentives",40,18,None),
 ("CRM adoption for sales teams","crm-adoption-for-sales-teams","guide","crm adoption sales teams",50,18,AMON),
 ("Why CRM projects fail","why-crm-projects-fail","guide","why crm fails",320,26,AMON),
 ("Signs of poor CRM adoption","signs-of-poor-crm-adoption","listicle","poor crm adoption",40,18,AMON),
 ("CRM data quality and adoption","crm-data-quality-and-adoption","guide","crm data quality",480,28,None),
 ("Making your CRM easier to use","making-crm-easier-to-use","guide","crm ease of use",40,18,None),
 ("CRM adoption after implementation","crm-adoption-after-implementation","guide","crm adoption after launch",30,16,AMON),
 ("How to revive a dead CRM","reviving-a-dead-crm","guide","unused crm",40,18,AMON),
 ("Running a CRM adoption survey","crm-adoption-survey","how-to","crm adoption survey",30,16,None),
 ("Using CRM champions to drive adoption","crm-champions","guide","crm champions",40,18,None),
 ("Getting executive buy-in for the CRM","executive-buy-in-for-crm","guide","crm executive buy in",40,18,None),
 ("How to fix low CRM adoption","fix-low-crm-adoption","how-to","low crm adoption",50,18,AMON),
 ("CRM adoption for remote teams","crm-adoption-for-remote-teams","guide","crm adoption remote teams",40,18,None),
 ("CRM adoption KPIs","crm-adoption-kpis","guide","crm adoption kpis",40,18,None),
]
for t, s, ctype, kw, vol, kd, money in ADA:
    records.append(r(AP, AID, ASLUG, AMON, t, s, "authority", ctype, kw, vol, kd, money=money))

# ===================== Sales Pipeline Management (30) =====================
PP, PID2, PSLUG = "Sales Pipeline Management", "sales-pipeline", "sales-pipeline-management"
# No dedicated money page for this authority pillar; cross-link to other pillars' money pages.
records.append(r(PP, PID2, PSLUG, None, "Sales pipeline management", PSLUG, "pillar", "pillar",
    "sales pipeline management", 90, 24, sec=["what is sales pipeline management", "sales pipeline stages"],
    ang="Sales pipeline management is how you track and move deals from first contact to close, so you can see what is real, what is stuck and what is coming. It sits alongside your CRM and forecasting work, and it is where reliable forecasts begin."))
PA = [
 ("What is sales pipeline management?","what-is-sales-pipeline-management","definition","what is sales pipeline management",90,22,None),
 ("What is a sales pipeline?","what-is-a-sales-pipeline","definition","what is a sales pipeline",480,26,None),
 ("Sales pipeline stages","sales-pipeline-stages","guide","sales pipeline stages",880,30,None),
 ("Sales pipeline vs sales funnel","sales-pipeline-vs-funnel","comparison","sales pipeline vs funnel",320,24,None),
 ("Sales pipeline management best practices","sales-pipeline-best-practices","listicle","sales pipeline management best practices",110,22,None),
 ("The benefits of pipeline management","benefits-of-pipeline-management","listicle","benefits of sales pipeline management",50,18,None),
 ("How to build a sales pipeline","how-to-build-a-sales-pipeline","how-to","how to build a sales pipeline",320,26,None),
 ("How to manage a sales pipeline","how-to-manage-a-sales-pipeline","how-to","how to manage a sales pipeline",170,24,None),
 ("Sales pipeline examples","sales-pipeline-examples","listicle","sales pipeline examples",170,22,None),
 ("A sales pipeline template","sales-pipeline-template","template","sales pipeline template",880,30,None),
 ("Defining your pipeline stages","defining-pipeline-stages","guide","define pipeline stages",110,22,None),
 ("Pipeline stage probabilities","pipeline-stage-probabilities","guide","pipeline stage probability",70,20,"sales-forecast-model-service"),
 ("How to run a sales pipeline review","sales-pipeline-review","how-to","sales pipeline review",110,22,None),
 ("Pipeline hygiene","pipeline-hygiene","guide","pipeline hygiene",90,20,"crm-optimisation-service"),
 ("Weighted pipeline explained","weighted-pipeline","definition","weighted pipeline",170,24,"sales-forecasting-service"),
 ("Moving deals through the pipeline","moving-deals-through-pipeline","guide","move deals through pipeline",40,18,None),
 ("What a healthy sales pipeline looks like","healthy-sales-pipeline","guide","healthy sales pipeline",110,22,None),
 ("Sales pipeline mistakes to avoid","sales-pipeline-mistakes","listicle","sales pipeline mistakes",70,20,None),
 ("How to clean your sales pipeline","how-to-clean-your-pipeline","how-to","clean sales pipeline",50,18,"crm-optimisation-service"),
 ("Managing multiple sales pipelines","managing-multiple-pipelines","guide","multiple sales pipelines",70,20,None),
 ("Pipeline management in HubSpot","pipeline-management-in-hubspot","guide","hubspot pipeline",320,26,"hubspot-consultant"),
 ("Pipeline management in Salesforce","pipeline-management-in-salesforce","guide","salesforce pipeline",480,30,"salesforce-consultant"),
 ("Pipeline management in Pipedrive","pipeline-management-in-pipedrive","guide","pipedrive pipeline",170,24,"pipedrive-consultant"),
 ("The best sales pipeline software","sales-pipeline-software","comparison","sales pipeline software",880,32,None),
 ("Pipeline management for small business","pipeline-management-for-small-business","guide","pipeline management small business",50,18,None),
 ("The B2B sales pipeline","sales-pipeline-stages-b2b","guide","b2b sales pipeline",170,24,None),
 ("Pipeline vs forecast","pipeline-vs-forecast","comparison","pipeline vs forecast",70,20,"sales-forecasting-service"),
 ("Deal management explained","deal-management","guide","deal management",320,26,None),
 ("Sales stage definitions","sales-stage-definitions","guide","sales stages",480,28,None),
]
for t, s, ctype, kw, vol, kd, money in PA:
    records.append(r(PP, PID2, PSLUG, None, t, s, "authority", ctype, kw, vol, kd, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch13: wrote {len(records)} records. by pillar: {dict(Counter(x['pillar'] for x in records))}. plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
