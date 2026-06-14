#!/usr/bin/env python3
"""Batch 9 - Process Mapping & SOP Creation, part 2 (75 records). Completes the pillar (150).

Restaurant/food/hospitality SOP sub-cluster (suits her hospitality clients), industry and
department SOPs/processes, and process-improvement methodologies + workflow automation.
Volumes indicative (universe doc + domain knowledge). Idempotent on batch==9.
"""
import json, os

PILLAR = "Process Mapping & SOP Creation"
PID = "process-sop"
BATCH = 9
PLAN = "content-plan/plan.json"
SOP_HUB = "standard-operating-procedures"
PM_HUB = "process-mapping"

WORDS = {"money": 1450, "guide": 1650, "how-to": 1700, "comparison": 1500,
         "definition": 1150, "listicle": 1350, "template": 1250}
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

def r(title, slug, role, ctype, kw, vol, kd, hub, sec=None, ang=None, money=None):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role == "money":
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    up = [hub] if role == "money" else [hub] + ([money] if money else [])
    return {
        "seq": None, "batch": BATCH, "pillar": PILLAR, "pillar_id": PID,
        "role": role, "content_type": ctype, "is_ad_landing": False,
        "title": title, "url_slug": slug, "target_market": "global",
        "intent": ("commercial" if role == "money" else "informational"),
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams documenting and improving how their business runs.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist or template so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Money (6)
M = [
 ("Hospitality SOP service","hospitality-sop-service","hotel sop",320,24,SOP_HUB,["hospitality standard operating procedures"]),
 ("Process optimisation consulting","process-optimisation-consulting","process optimisation",1300,34,PM_HUB,["process optimization consultant"]),
 ("Workflow automation service","workflow-automation-service","workflow automation",2400,40,PM_HUB,["business process automation"]),
 ("Business process management consulting","business-process-management-consulting","business process management",4400,44,PM_HUB,["bpm consultant"]),
 ("Operations manual service","operations-manual-service","operations manual",480,28,SOP_HUB,["company operations manual"]),
 ("Lean process consulting","lean-process-consulting","lean consulting",320,30,PM_HUB,["lean process improvement"]),
]
for t, s, kw, vol, kd, hub, sec in M:
    records.append(r(t, s, "money", "money", kw, vol, kd, hub, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and what you get."))

HSOP = "hospitality-sop-service"; RSOP = "restaurant-sop-service"; SOPM = "sop-creation-service"; OPM = "operations-manual-service"
PIM = "process-improvement-consulting"; POPT = "process-optimisation-consulting"; WFA = "workflow-automation-service"; BPM = "business-process-management-consulting"; LEAN = "lean-process-consulting"; PMM = "process-mapping-service"

A = [
 # Restaurant / food / hospitality SOP sub-cluster (16)
 ("Restaurant SOP examples","restaurant-sop-examples","listicle","restaurant sop examples",170,22,SOP_HUB,RSOP),
 ("A restaurant opening checklist","restaurant-opening-checklist","template","restaurant opening checklist",320,24,SOP_HUB,RSOP),
 ("A restaurant closing checklist","restaurant-closing-checklist","template","restaurant closing checklist",480,24,SOP_HUB,RSOP),
 ("A kitchen SOP guide","kitchen-sop","guide","kitchen sop",170,22,SOP_HUB,RSOP),
 ("A food safety SOP guide","food-safety-sop","guide","food safety sop",320,24,SOP_HUB,RSOP),
 ("A HACCP plan explained","haccp-plan","definition","haccp plan",1900,34,SOP_HUB,RSOP),
 ("A restaurant cleaning checklist","restaurant-cleaning-sop","template","restaurant cleaning checklist",170,22,SOP_HUB,RSOP),
 ("A bar SOP guide","bar-sop","guide","bar standard operating procedures",90,20,SOP_HUB,HSOP),
 ("A hotel SOP guide","hotel-sop","guide","hotel sop",320,24,SOP_HUB,HSOP),
 ("A housekeeping SOP guide","housekeeping-sop","guide","housekeeping sop",480,26,SOP_HUB,HSOP),
 ("A front desk SOP guide","front-desk-sop","guide","front desk sop",110,20,SOP_HUB,HSOP),
 ("A restaurant training manual","restaurant-training-manual","template","restaurant training manual",320,24,SOP_HUB,RSOP),
 ("A cafe SOP guide","cafe-sop","guide","cafe sop",50,18,SOP_HUB,RSOP),
 ("A food truck SOP guide","food-truck-sop","guide","food truck sop",40,18,SOP_HUB,RSOP),
 ("A restaurant operations manual","restaurant-operations-manual","template","restaurant operations manual",170,22,SOP_HUB,OPM),
 ("Hospitality SOP examples","hospitality-sop-examples","listicle","hospitality sop",110,20,SOP_HUB,HSOP),
 # Industry SOPs (13)
 ("A manufacturing SOP guide","manufacturing-sop","guide","manufacturing sop",320,24,SOP_HUB,SOPM),
 ("A warehouse SOP guide","warehouse-sop","guide","warehouse sop",320,24,SOP_HUB,SOPM),
 ("A healthcare SOP guide","healthcare-sop","guide","healthcare sop",110,22,SOP_HUB,SOPM),
 ("A logistics SOP guide","logistics-sop","guide","logistics sop",70,20,SOP_HUB,SOPM),
 ("A retail SOP guide","retail-sop","guide","retail sop",110,20,SOP_HUB,SOPM),
 ("A cleaning SOP guide","cleaning-sop","guide","cleaning sop",480,26,SOP_HUB,SOPM),
 ("A construction SOP guide","construction-sop","guide","construction sop",70,20,SOP_HUB,SOPM),
 ("A laboratory SOP guide","laboratory-sop","guide","laboratory sop",480,26,SOP_HUB,SOPM),
 ("A pharmacy SOP guide","pharmacy-sop","guide","pharmacy sop",320,24,SOP_HUB,SOPM),
 ("IT SOP examples","it-sop-examples","listicle","it sop examples",70,20,SOP_HUB,SOPM),
 ("An ecommerce SOP guide","ecommerce-sop","guide","ecommerce sop",90,20,SOP_HUB,SOPM),
 ("An agency SOP guide","agency-sop","guide","agency sop",70,20,SOP_HUB,SOPM),
 ("A property management SOP guide","property-management-sop","guide","property management sop",70,20,SOP_HUB,SOPM),
 # Department processes (10)
 ("The procurement process","procurement-process","guide","procurement process",480,28,PM_HUB,PMM),
 ("The accounts payable process","accounts-payable-process","guide","accounts payable process",480,28,PM_HUB,PMM),
 ("The order-to-cash process","order-to-cash-process","guide","order to cash process",880,32,PM_HUB,PMM),
 ("The procure-to-pay process","procure-to-pay-process","guide","procure to pay",1300,34,PM_HUB,PMM),
 ("The employee onboarding process","employee-onboarding-process","guide","employee onboarding process",880,30,PM_HUB,SOPM),
 ("The invoice approval process","invoice-approval-process","guide","invoice approval process",170,22,PM_HUB,PMM),
 ("The expense approval process","expense-approval-process","guide","expense approval process",110,22,PM_HUB,PMM),
 ("Sales process steps","sales-process-steps","guide","sales process steps",320,26,PM_HUB,PMM),
 ("The customer onboarding process","customer-onboarding-process-sop","guide","customer onboarding process",480,28,PM_HUB,SOPM),
 ("The hiring process, mapped","hiring-process-map","guide","hiring process",880,30,PM_HUB,PMM),
 # Process improvement methodologies (16)
 ("Process improvement explained","process-improvement","definition","process improvement",1900,34,PM_HUB,PIM),
 ("Business process improvement","business-process-improvement","guide","business process improvement",880,32,PM_HUB,PIM),
 ("Process optimisation explained","process-optimisation","definition","process optimization",1300,34,PM_HUB,POPT),
 ("Lean process improvement","lean-process-improvement","guide","lean process improvement",320,28,PM_HUB,LEAN),
 ("Six Sigma explained","six-sigma-explained","definition","six sigma",9900,46,PM_HUB,LEAN),
 ("DMAIC explained","dmaic-explained","definition","dmaic",1900,36,PM_HUB,LEAN),
 ("Kaizen explained","kaizen-explained","definition","kaizen",6600,44,PM_HUB,LEAN),
 ("Business process management explained","business-process-management","definition","business process management",4400,44,PM_HUB,BPM),
 ("Business process reengineering explained","business-process-reengineering","definition","business process reengineering",2400,38,PM_HUB,PIM),
 ("Continuous improvement explained","continuous-improvement","definition","continuous improvement",4400,42,PM_HUB,PIM),
 ("Process standardisation","process-standardisation","guide","process standardization",320,26,PM_HUB,POPT),
 ("Process efficiency","process-efficiency","guide","process efficiency",480,28,PM_HUB,POPT),
 ("Process improvement examples","process-improvement-examples","listicle","process improvement examples",480,28,PM_HUB,PIM),
 ("A process improvement plan","process-improvement-plan","template","process improvement plan",320,26,PM_HUB,PIM),
 ("The PDCA cycle explained","pdca-cycle","definition","pdca cycle",2400,36,PM_HUB,LEAN),
 ("The Gemba walk explained","gemba-walk","definition","gemba walk",1300,32,PM_HUB,LEAN),
 # Workflow / automation (8)
 ("Workflow management explained","workflow-management","definition","workflow management",880,32,PM_HUB,WFA),
 ("A guide to workflow automation","workflow-automation-guide","guide","workflow automation",2400,40,PM_HUB,WFA),
 ("Business process automation explained","business-process-automation","definition","business process automation",1900,38,PM_HUB,WFA),
 ("How to automate a process","how-to-automate-a-process","how-to","how to automate a process",90,22,PM_HUB,WFA),
 ("Workflow diagrams explained","workflow-diagram","definition","workflow diagram",1600,34,PM_HUB,PMM),
 ("Workflow examples","workflow-examples","listicle","workflow examples",320,26,PM_HUB,PMM),
 ("Process mining explained","process-mining","definition","process mining",4400,42,PM_HUB,POPT),
 ("Robotic process automation explained","rpa-explained","definition","robotic process automation",4400,44,PM_HUB,WFA),
 # SOP management / maintenance / software (6)
 ("The best SOP software","sop-software","comparison","sop software",480,30,SOP_HUB,None),
 ("How to manage SOPs","how-to-manage-sops","how-to","sop management",110,22,SOP_HUB,SOPM),
 ("How to keep SOPs up to date","how-to-update-sops","how-to","updating sops",50,18,SOP_HUB,SOPM),
 ("How to train your team on SOPs","sop-training","guide","sop training",170,22,SOP_HUB,SOPM),
 ("Digital SOPs explained","digital-sops","guide","digital sop",70,20,SOP_HUB,SOPM),
 ("SOP compliance","sop-compliance","guide","sop compliance",90,22,SOP_HUB,SOPM),
]
for t, s, ctype, kw, vol, kd, hub, money in A:
    records.append(r(t, s, "authority", ctype, kw, vol, kd, hub, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch09: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
