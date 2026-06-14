#!/usr/bin/env python3
"""Batch 10 - CRM Automation & Workflow (95 records).

Warmest, least-contested CRM intent (universe cluster ~450, KD ~35). Money + authority.
CRM/sales/marketing automation, what-to-automate use-cases, platform workflows, email and
sales automation. CRM-context slugs keep this distinct from Batch 9's general process
automation. Volumes indicative (universe doc + domain knowledge). Idempotent on batch==10.
"""
import json, os

PILLAR = "CRM Automation & Workflow"
PID = "crm-automation"
BATCH = 10
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "crm-automation"
DEF_MONEY = "crm-automation-service"

WORDS = {"pillar": 2200, "money": 1450, "guide": 1650, "how-to": 1700,
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
        "pillar": ["What CRM automation is and why it matters", "Where teams waste time on manual work",
                   "How Lauren automates a CRM", "What to automate first", "What an engagement includes"],
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

def r(title, slug, role, ctype, kw, vol, kd, ad=False, sec=None, ang=None, money=None, market="global"):
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
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams whose CRM holds data but does not do the work, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillar
records.append(r("CRM automation and workflow", PILLAR_SLUG, "pillar", "pillar",
    "crm automation", 450, 35, ad=False,
    sec=["crm workflow automation", "sales automation", "crm automation software"],
    ang="CRM automation makes your CRM do the work, routing leads, chasing follow-ups, updating records and triggering the right next step, so your team sells instead of admin. This is how Lauren decides what to automate first and builds workflows your team trusts."))

# Money (10)
CA = "crm-automation-service"; WFA = "crm-workflow-automation"; SA = "sales-automation-service"; MA = "marketing-automation-service"; EA = "email-automation-setup"; LA = "lead-automation-service"
M = [
 ("CRM automation service","crm-automation-service","crm automation services",90,24,["crm automation"]),
 ("CRM workflow automation","crm-workflow-automation","crm workflow automation",70,22,["workflow automation crm"]),
 ("Sales automation service","sales-automation-service","sales automation",1300,36,["sales process automation"]),
 ("Marketing automation service","marketing-automation-service","marketing automation services",480,34,["marketing automation setup"]),
 ("CRM automation audit","crm-automation-audit","crm workflow audit",40,18,["automation audit"]),
 ("HubSpot automation service","hubspot-automation-service","hubspot workflow automation",170,28,["hubspot automation"]),
 ("Salesforce automation service","salesforce-automation-service","salesforce automation",480,34,["salesforce flow"]),
 ("Zoho CRM automation service","zoho-automation-service","zoho crm automation",110,24,["zoho workflow"]),
 ("Email automation setup","email-automation-setup","email automation",2900,40,["email automation services"]),
 ("Lead automation service","lead-automation-service","lead automation",170,26,["lead routing automation"]),
]
for t, s, kw, vol, kd, sec in M:
    records.append(r(t, s, "money", "money", kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

# Authority (84): (title, slug, type, kw, vol, kd, money)
A = [
 # Foundations (12)
 ("What is CRM automation?","what-is-crm-automation","definition","what is crm automation",320,24,None),
 ("What is sales automation?","what-is-sales-automation","definition","what is sales automation",320,26,SA),
 ("What is marketing automation?","what-is-marketing-automation","definition","what is marketing automation",1900,36,MA),
 ("CRM workflow automation explained","crm-workflow-automation-explained","definition","crm workflow automation",70,22,WFA),
 ("The benefits of CRM automation","crm-automation-benefits","listicle","crm automation benefits",90,20,None),
 ("CRM automation examples","crm-automation-examples","listicle","crm automation examples",170,24,None),
 ("Sales automation vs marketing automation","sales-vs-marketing-automation","comparison","sales automation vs marketing automation",110,22,None),
 ("CRM automation vs marketing automation","crm-vs-marketing-automation","comparison","crm vs marketing automation",90,22,None),
 ("Types of CRM automation","types-of-crm-automation","guide","types of crm automation",70,20,None),
 ("How CRM automation works","how-crm-automation-works","guide","how crm automation works",50,20,None),
 ("The ROI of CRM automation","crm-automation-roi","guide","crm automation roi",40,20,None),
 ("CRM automation statistics","crm-automation-statistics","listicle","crm automation statistics",110,22,None),
 # What to automate / use-cases (16)
 ("What to automate in your CRM first","what-to-automate-in-your-crm","guide","what to automate in crm",90,22,CA),
 ("CRM automation ideas","crm-automation-ideas","listicle","crm automation ideas",110,22,None),
 ("Sales tasks worth automating","sales-tasks-to-automate","listicle","sales tasks to automate",90,22,SA),
 ("Marketing tasks worth automating","marketing-tasks-to-automate","listicle","marketing tasks to automate",70,22,MA),
 ("Lead assignment automation","lead-assignment-automation","guide","lead assignment automation",110,24,LA),
 ("Lead nurturing automation","lead-nurturing-automation","guide","lead nurturing automation",170,26,LA),
 ("Follow-up automation","follow-up-automation","guide","follow up automation",110,22,SA),
 ("Automating CRM data entry","data-entry-automation-crm","guide","crm data entry automation",90,22,CA),
 ("Deal stage automation","deal-stage-automation","guide","deal stage automation",50,20,SA),
 ("Task automation in your CRM","task-automation-crm","guide","crm task automation",70,20,CA),
 ("Reminder and alert automation","reminder-automation","guide","crm reminders automation",40,18,CA),
 ("Pipeline automation","pipeline-automation","guide","sales pipeline automation",90,22,SA),
 ("Quote and proposal automation","quote-automation","guide","quote automation",110,24,SA),
 ("Contract and e-signature automation","contract-automation","guide","contract automation",320,28,None),
 ("Reporting automation","reporting-automation","guide","automated reporting",480,30,None),
 ("Customer onboarding automation","onboarding-automation","guide","onboarding automation",170,24,CA),
 # How-to & setup (12)
 ("How to automate your CRM","how-to-automate-your-crm","how-to","how to automate crm",90,22,CA),
 ("How to set up CRM workflows","how-to-set-up-crm-workflows","how-to","how to set up crm workflows",70,22,WFA),
 ("How to automate sales follow-ups","how-to-automate-sales-follow-ups","how-to","automate sales follow up",70,22,SA),
 ("How to automate lead routing","how-to-automate-lead-routing","how-to","automate lead routing",90,24,LA),
 ("How to build a CRM workflow","how-to-build-a-crm-workflow","how-to","build a crm workflow",50,20,WFA),
 ("CRM automation best practices","crm-automation-best-practices","listicle","crm automation best practices",70,20,None),
 ("CRM automation mistakes to avoid","crm-automation-mistakes","listicle","crm automation mistakes",50,18,None),
 ("How to automate data entry","how-to-automate-data-entry","how-to","automate data entry",170,24,CA),
 ("How to automate email sequences","how-to-automate-email-sequences","how-to","automate email sequences",110,24,EA),
 ("Map the workflow before you automate","map-before-you-automate","guide","map workflow before automating",40,18,None),
 ("A CRM automation checklist","crm-automation-checklist","template","crm automation checklist",40,18,CA),
 ("A CRM automation strategy","crm-automation-strategy","guide","crm automation strategy",50,20,CA),
 # Platform-specific (16)
 ("A guide to HubSpot workflows","hubspot-workflows-guide","guide","hubspot workflows",1300,34,"hubspot-automation-service"),
 ("HubSpot automation examples","hubspot-automation-examples","listicle","hubspot automation examples",170,26,"hubspot-automation-service"),
 ("A guide to Salesforce Flow","salesforce-flow-guide","guide","salesforce flow",2400,40,"salesforce-automation-service"),
 ("Salesforce process automation","salesforce-process-automation","guide","salesforce process automation",320,30,"salesforce-automation-service"),
 ("Zoho CRM workflow rules","zoho-workflow-rules","guide","zoho crm workflow",170,26,"zoho-automation-service"),
 ("Pipedrive automation","pipedrive-automation","guide","pipedrive automation",320,28,None),
 ("monday.com automation","monday-automation","guide","monday automation",480,30,None),
 ("Using Zapier with your CRM","zapier-for-crm","guide","zapier crm",480,30,None),
 ("Using Make with your CRM","make-for-crm","guide","make crm automation",170,26,None),
 ("CRM API automation","crm-api-automation","guide","crm api automation",70,24,None),
 ("HubSpot vs Salesforce automation","hubspot-vs-salesforce-automation","comparison","hubspot vs salesforce automation",90,24,None),
 ("The best CRM automation software","best-crm-automation-software","comparison","crm automation software",170,28,None),
 ("The best CRM automation tools","best-crm-automation-tools","comparison","crm automation tools",110,26,None),
 ("Workflow automation tools for CRM","crm-workflow-automation-tools","comparison","workflow automation tools",1300,36,None),
 ("AI in CRM automation","ai-crm-automation","guide","ai crm automation",170,28,None),
 ("Chatbots and CRM automation","chatbot-crm-automation","guide","chatbot crm",320,30,None),
 # Email / marketing automation (16)
 ("A guide to email automation","email-automation-guide","guide","email automation",2900,40,EA),
 ("Email drip campaigns explained","email-drip-campaigns","definition","drip campaign",1900,36,EA),
 ("Email sequences that convert","email-sequences","guide","email sequences",1000,32,EA),
 ("Lead scoring automation","lead-scoring-automation","guide","lead scoring automation",170,26,LA),
 ("Marketing automation workflows","marketing-automation-workflows","guide","marketing automation workflows",480,30,MA),
 ("Marketing automation examples","marketing-automation-examples","listicle","marketing automation examples",480,30,MA),
 ("Marketing automation for B2B","marketing-automation-for-b2b","guide","b2b marketing automation",480,32,MA),
 ("Marketing automation for SaaS","marketing-automation-for-saas","guide","saas marketing automation",170,28,MA),
 ("Email automation best practices","email-automation-best-practices","listicle","email automation best practices",110,22,EA),
 ("Abandoned cart automation","abandoned-cart-automation","guide","abandoned cart email",1300,34,None),
 ("Re-engagement campaign automation","re-engagement-campaigns","guide","re engagement campaign",480,30,None),
 ("Welcome email automation","welcome-email-automation","guide","welcome email sequence",880,32,EA),
 ("CRM triggers explained","crm-triggers-explained","definition","crm triggers",90,22,WFA),
 ("If-then automation rules explained","if-then-automation-rules","guide","automation rules",170,24,None),
 ("Automation vs manual processes","automation-vs-manual","comparison","automation vs manual",110,22,None),
 ("When not to automate","when-not-to-automate","guide","when not to automate",40,18,None),
 # Sales automation + segment (12)
 ("A guide to sales automation","sales-automation-guide","guide","sales automation guide",320,30,SA),
 ("The best sales automation tools","sales-automation-tools","comparison","sales automation tools",480,32,SA),
 ("Sales sequence automation","sales-sequence-automation","guide","sales sequences",480,30,SA),
 ("Sales cadence explained","sales-cadence","definition","sales cadence",1000,32,SA),
 ("Automating the sales process","automating-the-sales-process","guide","sales process automation",170,26,SA),
 ("Automated sales follow-up templates","sales-follow-up-templates","template","sales follow up templates",320,26,SA),
 ("Automating proposals and quotes","automating-proposals","guide","proposal automation",170,26,SA),
 ("Sales automation for small business","sales-automation-small-business","guide","sales automation small business",90,22,SA),
 ("CRM automation for startups","crm-automation-for-startups","guide","crm automation startups",40,18,CA),
 ("CRM automation for small business","crm-automation-for-small-business","guide","crm automation small business",90,22,CA),
 ("CRM automation for agencies","crm-automation-for-agencies","guide","crm automation agencies",40,18,CA),
 ("Workflow automation examples for CRM","crm-workflow-automation-examples","listicle","crm workflow examples",70,20,WFA),
]
for t, s, ctype, kw, vol, kd, money in A:
    records.append(r(t, s, "authority", ctype, kw, vol, kd, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch10: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
