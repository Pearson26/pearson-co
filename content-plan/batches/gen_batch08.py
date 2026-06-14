#!/usr/bin/env python3
"""Batch 8 - Process Mapping & SOP Creation, part 1 (75 records).

Largest-demand pillar (SOP cluster ~2,310, process-mapping cluster ~1,760 per the
keyword-universe doc; ~729 keywords combined). Two hubs: SOPs and process mapping, so two
pillar pages. Part 1 covers SOP foundations/how-to/templates and process-mapping
foundations/how-to/tools/documentation. Part 2 adds the restaurant/food/hospitality SOP
sub-cluster, department/industry SOPs and process-improvement methodologies.
Volumes indicative (universe doc + domain knowledge). Idempotent on batch==8.
"""
import json, os

PILLAR = "Process Mapping & SOP Creation"
PID = "process-sop"
BATCH = 8
PLAN = "content-plan/plan.json"
SOP_HUB = "standard-operating-procedures"
PM_HUB = "process-mapping"

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
        "pillar": ["What it is and why it matters commercially", "Where undocumented process costs a business",
                   "How Lauren documents process", "What an engagement includes", "Templates and handover"],
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

def r(title, slug, role, ctype, kw, vol, kd, hub, ad=False, sec=None, ang=None, money=None, market="global"):
    i = _idx[0]; _idx[0] += 1
    schema = ["Article", "FAQPage", "BreadcrumbList"]
    if role in ("pillar", "money"):
        schema.append("Service")
    if ctype == "how-to":
        schema.append("HowTo")
    if role == "pillar":
        up = []
    elif role == "money":
        up = [hub]
    else:
        up = [hub] + ([money] if money else [])
    return {
        "seq": None, "batch": BATCH, "pillar": PILLAR, "pillar_id": PID,
        "role": role, "content_type": ctype, "is_ad_landing": ad,
        "title": title, "url_slug": slug, "target_market": market, "intent": ("commercial" if role in ("pillar", "money") else "informational"),
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams documenting how their business runs, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist or template so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillars (2)
records.append(r("Standard operating procedures (SOPs)", SOP_HUB, "pillar", "pillar",
    "standard operating procedure", 2310, 28, SOP_HUB, ad=False,
    sec=["sop", "how to write an sop", "sop template"],
    ang="A standard operating procedure (SOP) captures how a task should be done, every time, so quality holds as a business grows and onboarding gets faster. This is how Lauren turns the way your business actually runs into clear, usable SOPs your team will follow."))
records.append(r("Process mapping", PM_HUB, "pillar", "pillar",
    "process mapping", 1760, 32, PM_HUB, ad=False,
    sec=["process map", "how to create a process map", "business process mapping"],
    ang="Process mapping draws out how work really flows through a business, step by step, so you can see the bottlenecks, handoffs and revenue leaks. This is how Lauren maps your processes and turns the picture into practical improvement."))

# Money (7)
M = [
 ("SOP creation service","sop-creation-service","sop writing service",90,22,SOP_HUB,["sop creation","sop development"]),
 ("Process mapping service","process-mapping-service","process mapping services",110,22,PM_HUB,["process mapping consultant"]),
 ("SOP consultant","sop-consultant","sop consultant",70,20,SOP_HUB,["sop specialist"]),
 ("Process improvement consulting","process-improvement-consulting","process improvement consultant",170,26,PM_HUB,["business process consultant"]),
 ("Restaurant SOP service","restaurant-sop-service","restaurant sop",320,24,SOP_HUB,["food sop","restaurant standard operating procedures"]),
 ("SOP template pack","sop-template-pack","sop templates",480,28,SOP_HUB,["sop template library"]),
 ("Process documentation service","process-documentation-service","process documentation services",90,22,PM_HUB,["business process documentation"]),
]
for t, s, kw, vol, kd, hub, sec in M:
    records.append(r(t, s, "money", "money", kw, vol, kd, hub, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and what you get."))

# Authority (66): (title, slug, type, kw, vol, kd, hub, money)
SOPM = "sop-creation-service"; SOPT = "sop-template-pack"; PMM = "process-mapping-service"; PIM = "process-improvement-consulting"; PDM = "process-documentation-service"
A = [
 # SOP foundations & how-to (16)
 ("What is a standard operating procedure?","what-is-a-standard-operating-procedure","definition","what is a standard operating procedure",390,24,SOP_HUB,None),
 ("What is an SOP?","what-is-an-sop","definition","what is an sop",320,22,SOP_HUB,None),
 ("How to write an SOP","how-to-write-an-sop","how-to","how to write an sop",880,30,SOP_HUB,SOPM),
 ("How to create an SOP","how-to-create-an-sop","how-to","how to create an sop",320,26,SOP_HUB,SOPM),
 ("SOP format explained","sop-format","guide","sop format",480,26,SOP_HUB,None),
 ("How to structure an SOP","sop-structure","guide","sop structure",110,22,SOP_HUB,None),
 ("Types of SOPs","types-of-sops","guide","types of sop",110,22,SOP_HUB,None),
 ("SOP best practices","sop-best-practices","listicle","sop best practices",90,20,SOP_HUB,None),
 ("SOP examples","sop-examples","listicle","sop examples",880,28,SOP_HUB,SOPT),
 ("Why SOPs matter","why-sops-matter","guide","importance of sop",320,24,SOP_HUB,None),
 ("SOP vs work instruction","sop-vs-work-instruction","comparison","sop vs work instruction",110,20,SOP_HUB,None),
 ("SOP vs policy","sop-vs-policy","comparison","sop vs policy",170,20,SOP_HUB,None),
 ("SOP vs process","sop-vs-process","comparison","sop vs process",90,18,SOP_HUB,None),
 ("How to implement SOPs","how-to-implement-sops","how-to","how to implement sops",90,20,SOP_HUB,SOPM),
 ("The SOP approval process","sop-approval-process","guide","sop approval process",70,20,SOP_HUB,None),
 ("An SOP numbering system","sop-numbering-system","guide","sop numbering system",110,20,SOP_HUB,None),
 # SOP templates (14)
 ("A standard operating procedure template","sop-template","template","standard operating procedure template",260,26,SOP_HUB,SOPT),
 ("A free SOP template","free-sop-template","template","free sop template",320,24,SOP_HUB,SOPT),
 ("An SOP template for Word","sop-template-word","template","sop template word",480,26,SOP_HUB,SOPT),
 ("An SOP template for Google Docs","sop-template-google-docs","template","sop template google docs",90,20,SOP_HUB,SOPT),
 ("An SOP template for Excel","sop-template-excel","template","sop template excel",90,20,SOP_HUB,SOPT),
 ("An SOP checklist template","sop-checklist-template","template","sop checklist",110,20,SOP_HUB,SOPT),
 ("An SOP manual template","sop-manual-template","template","sop manual",320,24,SOP_HUB,SOPT),
 ("An HR SOP template","hr-sop-template","template","hr sop",90,20,SOP_HUB,SOPT),
 ("A finance SOP template","finance-sop-template","template","finance sop",70,20,SOP_HUB,SOPT),
 ("A sales SOP template","sales-sop-template","template","sales sop",110,20,SOP_HUB,SOPT),
 ("A customer service SOP template","customer-service-sop-template","template","customer service sop",110,20,SOP_HUB,SOPT),
 ("An IT SOP template","it-sop-template","template","it sop",90,20,SOP_HUB,SOPT),
 ("An onboarding SOP template","onboarding-sop-template","template","onboarding sop",90,20,SOP_HUB,SOPT),
 ("An SOP template for small business","sop-template-for-small-business","template","small business sop",110,20,SOP_HUB,SOPT),
 # Process mapping foundations & how-to (18)
 ("What is process mapping?","what-is-process-mapping","definition","what is process mapping",480,26,PM_HUB,None),
 ("What is a process map?","what-is-a-process-map","definition","what is a process map",880,28,PM_HUB,None),
 ("How to create a process map","how-to-create-a-process-map","how-to","how to create a process map",320,26,PM_HUB,PMM),
 ("Process mapping steps","process-mapping-steps","how-to","process mapping steps",110,22,PM_HUB,PMM),
 ("Process map symbols explained","process-map-symbols","guide","process map symbols",1300,30,PM_HUB,None),
 ("Process mapping techniques","process-mapping-techniques","guide","process mapping techniques",170,24,PM_HUB,None),
 ("Types of process maps","types-of-process-maps","guide","types of process maps",320,24,PM_HUB,None),
 ("Process mapping examples","process-mapping-examples","listicle","process mapping examples",480,26,PM_HUB,None),
 ("Process map vs flowchart","process-map-vs-flowchart","comparison","process map vs flowchart",320,24,PM_HUB,None),
 ("Process flow diagrams explained","process-flow-diagram","definition","process flow diagram",2400,36,PM_HUB,None),
 ("Swimlane diagrams explained","swimlane-diagram","definition","swimlane diagram",1900,34,PM_HUB,None),
 ("BPMN explained","bpmn-explained","definition","bpmn",4400,42,PM_HUB,None),
 ("Value stream mapping explained","value-stream-mapping","definition","value stream mapping",4400,42,PM_HUB,PIM),
 ("Process mapping best practices","process-mapping-best-practices","listicle","process mapping best practices",90,20,PM_HUB,None),
 ("Business process mapping","business-process-mapping","guide","business process mapping",480,28,PM_HUB,PMM),
 ("The benefits of process mapping","process-mapping-benefits","listicle","benefits of process mapping",90,20,PM_HUB,None),
 ("As-is vs to-be process maps","as-is-vs-to-be-process-map","comparison","as is to be process",110,20,PM_HUB,PIM),
 ("How to run a process mapping workshop","process-mapping-workshop","how-to","process mapping workshop",70,20,PM_HUB,PMM),
 # Process mapping tools & templates (10)
 ("Business process mapping tools","process-mapping-tools","comparison","business process mapping tools",320,26,PM_HUB,None),
 ("The best process mapping software","best-process-mapping-software","comparison","process mapping software",880,32,PM_HUB,None),
 ("Free process mapping tools","free-process-mapping-tools","comparison","free process mapping tools",170,22,PM_HUB,None),
 ("A process map template","process-map-template","template","process map template",480,26,PM_HUB,None),
 ("A process flowchart template","process-flowchart-template","template","flowchart template",1900,34,PM_HUB,None),
 ("A swimlane diagram template","swimlane-template","template","swimlane template",320,24,PM_HUB,None),
 ("Process mapping in Visio","process-mapping-in-visio","guide","visio process map",320,26,PM_HUB,None),
 ("Process mapping in Lucidchart","process-mapping-in-lucidchart","guide","lucidchart process map",170,24,PM_HUB,None),
 ("Process mapping in Excel","process-mapping-in-excel","guide","process map excel",170,24,PM_HUB,None),
 ("Process mapping in PowerPoint","process-mapping-in-powerpoint","guide","process map powerpoint",110,22,PM_HUB,None),
 # Process documentation & workflow (8)
 ("What is process documentation?","process-documentation","definition","process documentation",880,30,PM_HUB,PDM),
 ("How to document a process","how-to-document-a-process","how-to","how to document a process",480,28,PM_HUB,PDM),
 ("A process documentation template","process-documentation-template","template","process documentation template",170,22,PM_HUB,PDM),
 ("Workflow vs process","workflow-vs-process","comparison","workflow vs process",320,24,PM_HUB,None),
 ("What is a workflow?","what-is-a-workflow","definition","what is a workflow",1300,32,PM_HUB,None),
 ("Process vs procedure","business-process-vs-procedure","comparison","process vs procedure",480,26,PM_HUB,None),
 ("Standard work explained","standard-work-explained","definition","standard work",880,30,PM_HUB,None),
 ("Process mapping for small business","process-mapping-for-small-business","guide","process mapping small business",50,18,PM_HUB,PMM),
]
for t, s, ctype, kw, vol, kd, hub, money in A:
    records.append(r(t, s, "authority", ctype, kw, vol, kd, hub, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch08: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
