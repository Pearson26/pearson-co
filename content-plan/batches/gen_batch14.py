#!/usr/bin/env python3
"""Batch 14 - Go-to-Market Strategy (85 records). Final content batch.

Bridge into the expansion work (universe UAE 660, includes "go to market strategy dubai").
The GTM discipline specifically: GTM strategy, launch, positioning/ICP, pricing, channels and
sales strategy. Kept distinct from growth strategy (Batch 4) and market entry (Batch 7).
Volumes indicative (universe doc + domain knowledge). Idempotent on batch==14.
"""
import json, os

PILLAR = "Go-to-Market Strategy"
PID = "go-to-market"
BATCH = 14
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "go-to-market-strategy"
DEF_MONEY = "go-to-market-strategy-consulting"

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
        "pillar": ["What a go-to-market strategy is", "Why launches and new markets stall",
                   "How Lauren builds a GTM plan", "From plan to traction", "What an engagement includes"],
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
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams launching or entering a market, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short framework or checklist so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillar
records.append(r("Go-to-market strategy", PILLAR_SLUG, "pillar", "pillar",
    "go to market strategy", 2400, 47, ad=False,
    sec=["b2b go to market strategy", "go to market strategy framework", "product launch strategy"],
    ang="A go-to-market strategy is the plan for how you take a product or service to a market and win customers: who you target, what you say, how you reach them and how you sell. This is how Lauren builds a GTM plan that earns early traction, and the bridge into entering new markets like the Middle East."))

# Money (6)
GC = "go-to-market-strategy-consulting"; PL = "product-launch-consulting"; B2B = "b2b-gtm-strategy-service"; SAAS = "saas-gtm-strategy-service"; POS = "positioning-and-messaging-service"
M = [
 ("Go-to-market strategy consulting","go-to-market-strategy-consulting","go to market strategy consultant",170,30,["gtm consultant"]),
 ("Product launch consulting","product-launch-consulting","product launch consultant",110,28,["launch strategist"]),
 ("B2B go-to-market strategy","b2b-gtm-strategy-service","b2b go to market strategy",320,32,["b2b gtm"]),
 ("SaaS go-to-market strategy","saas-gtm-strategy-service","saas go to market strategy",480,34,["saas gtm strategy"]),
 ("Go-to-market strategy in the UAE","gtm-strategy-uae","go to market strategy dubai",90,26,["go to market uae"]),
 ("Positioning and messaging","positioning-and-messaging-service","positioning consultant",170,28,["messaging strategy"]),
]
for t, s, kw, vol, kd, sec in M:
    mk = "UAE" if s == "gtm-strategy-uae" else "global"
    records.append(r(t, s, "money", "money", kw, vol, kd, sec=sec, market=mk,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect."))

A = [
 # GTM foundations (12)
 ("What is a go-to-market strategy?","what-is-a-go-to-market-strategy","definition","what is a go to market strategy",480,32,GC),
 ("A go-to-market framework","go-to-market-framework","guide","go to market strategy framework",480,32,GC),
 ("Types of go-to-market strategies","types-of-go-to-market-strategies","guide","types of go to market strategy",170,28,GC),
 ("Go-to-market strategy examples","go-to-market-strategy-examples","listicle","go to market strategy examples",480,30,GC),
 ("How to create a go-to-market strategy","how-to-create-a-go-to-market-strategy","how-to","how to create a go to market strategy",320,30,GC),
 ("A go-to-market strategy template","go-to-market-strategy-template","template","go to market strategy template",880,32,GC),
 ("Go-to-market vs marketing strategy","gtm-vs-marketing-strategy","comparison","go to market vs marketing strategy",90,24,None),
 ("The components of a go-to-market strategy","go-to-market-strategy-components","guide","go to market strategy components",110,26,GC),
 ("Go-to-market motions explained","go-to-market-motion","definition","go to market motion",170,28,GC),
 ("A go-to-market strategy checklist","gtm-strategy-checklist","template","go to market checklist",90,24,GC),
 ("Why go-to-market strategies fail","why-gtm-strategies-fail","guide","why go to market fails",70,22,GC),
 ("A go-to-market strategy for startups","gtm-for-startups","guide","go to market strategy startups",170,28,GC),
 # By type / motion (12)
 ("A B2B go-to-market strategy","b2b-go-to-market-strategy","guide","b2b go to market strategy",320,30,B2B),
 ("A SaaS go-to-market strategy","saas-go-to-market-strategy","guide","saas go to market strategy",480,32,SAAS),
 ("Product-led go-to-market","product-led-go-to-market","guide","product led go to market",170,28,SAAS),
 ("Sales-led go-to-market","sales-led-go-to-market","guide","sales led go to market",110,26,B2B),
 ("A B2B SaaS go-to-market strategy","b2b-saas-go-to-market","guide","b2b saas go to market",170,28,SAAS),
 ("An enterprise go-to-market strategy","enterprise-go-to-market","guide","enterprise go to market",110,28,B2B),
 ("Product-led vs sales-led GTM","product-led-vs-sales-led-gtm","comparison","product led vs sales led",170,26,None),
 ("A channel-led go-to-market strategy","channel-led-go-to-market","guide","channel go to market",90,26,None),
 ("Go-to-market for a new product","go-to-market-new-product","guide","go to market new product",110,26,PL),
 ("Go-to-market for a new feature","go-to-market-new-feature","guide","feature launch",90,24,PL),
 ("A go-to-market strategy for services","go-to-market-for-services","guide","go to market for services",70,24,GC),
 ("Account-based go-to-market","account-based-go-to-market","guide","account based go to market",90,26,B2B),
 # Product launch (12)
 ("A product launch strategy","product-launch-strategy","guide","product launch strategy",1300,36,PL),
 ("A product launch plan","product-launch-plan","template","product launch plan",880,32,PL),
 ("A product launch checklist","product-launch-checklist","template","product launch checklist",480,28,PL),
 ("Product launch examples","product-launch-examples","listicle","product launch examples",320,26,PL),
 ("How to launch a product","how-to-launch-a-product","how-to","how to launch a product",880,32,PL),
 ("Product launch marketing","product-launch-marketing","guide","product launch marketing",480,30,PL),
 ("Soft launch vs hard launch","soft-launch-vs-hard-launch","comparison","soft launch vs hard launch",320,26,None),
 ("A product launch timeline","product-launch-timeline","guide","product launch timeline",170,24,PL),
 ("Building a launch plan","go-to-market-launch-plan","template","launch plan",880,32,PL),
 ("New product introduction explained","new-product-introduction","definition","new product introduction",480,28,PL),
 ("Product launch metrics","product-launch-metrics","guide","product launch metrics",110,24,PL),
 ("Product launch mistakes to avoid","product-launch-mistakes","listicle","product launch mistakes",110,24,PL),
 # Positioning, ICP, messaging (12)
 ("What is positioning?","what-is-positioning","definition","what is positioning",1300,34,POS),
 ("A positioning strategy","positioning-strategy","guide","positioning strategy",880,32,POS),
 ("Product positioning explained","product-positioning","definition","product positioning",1900,36,POS),
 ("A positioning framework","positioning-framework","guide","positioning framework",480,30,POS),
 ("What is a value proposition?","value-proposition","definition","value proposition",6600,42,POS),
 ("The value proposition canvas","value-proposition-canvas","guide","value proposition canvas",4400,40,POS),
 ("A unique value proposition","unique-value-proposition","definition","unique value proposition",1900,36,POS),
 ("What is an ideal customer profile?","ideal-customer-profile","definition","ideal customer profile",2400,38,POS),
 ("How to define your ICP","how-to-define-your-icp","how-to","how to define icp",320,28,POS),
 ("B2B buyer personas","buyer-personas-b2b","guide","b2b buyer persona",1300,34,POS),
 ("A messaging framework","messaging-framework","guide","messaging framework",880,32,POS),
 ("Competitive positioning","competitive-positioning","guide","competitive positioning",480,30,POS),
 # Pricing & packaging (8)
 ("A pricing strategy guide","pricing-strategy","guide","pricing strategy",6600,44,GC),
 ("A SaaS pricing strategy","saas-pricing-strategy","guide","saas pricing strategy",880,34,SAAS),
 ("Pricing models explained","pricing-models","definition","pricing models",2400,38,GC),
 ("Value-based pricing explained","value-based-pricing","definition","value based pricing",2900,40,GC),
 ("How to price a product","how-to-price-a-product","how-to","how to price a product",880,34,GC),
 ("Freemium vs free trial","freemium-vs-free-trial","comparison","freemium vs free trial",480,30,SAAS),
 ("Packaging and tiering","packaging-and-tiering","guide","saas packaging",170,26,SAAS),
 ("Penetration vs skimming pricing","penetration-vs-skimming","comparison","penetration pricing vs skimming",480,30,None),
 # Channels & sales strategy (12)
 ("A sales strategy guide","sales-strategy","guide","sales strategy",2900,40,GC),
 ("A sales strategy framework","sales-strategy-framework","guide","sales strategy framework",480,32,GC),
 ("A channel strategy","channel-strategy","guide","channel strategy",1300,34,None),
 ("Distribution channels explained","distribution-channels","definition","distribution channels",1900,36,None),
 ("Direct vs indirect sales","direct-vs-indirect-sales","comparison","direct vs indirect sales",320,28,None),
 ("A partnerships strategy","partnerships-strategy","guide","partnership strategy",880,32,None),
 ("Demand generation explained","demand-generation","definition","demand generation",2900,40,None),
 ("A lead generation strategy","lead-generation-strategy","guide","lead generation strategy",1300,36,None),
 ("Inbound vs outbound","inbound-vs-outbound","comparison","inbound vs outbound",1300,34,None),
 ("A sales playbook","sales-playbook","template","sales playbook",1900,36,B2B),
 ("A B2B sales strategy","b2b-sales-strategy","guide","b2b sales strategy",480,32,B2B),
 ("A multi-channel strategy","multi-channel-strategy","guide","multi channel strategy",480,30,None),
 # Market & launch readiness (10)
 ("Market research for a launch","market-research-for-launch","how-to","market research",6600,44,GC),
 ("How to do a competitive analysis","competitive-analysis","how-to","competitive analysis",6600,44,None),
 ("TAM, SAM and SOM explained","tam-sam-som","definition","tam sam som",4400,40,GC),
 ("Market segmentation explained","market-segmentation","definition","market segmentation",6600,44,None),
 ("Launch readiness","launch-readiness","guide","launch readiness",110,24,PL),
 ("The beachhead market strategy","beachhead-market","definition","beachhead market",480,30,GC),
 ("Reaching early adopters","early-adopters","guide","early adopters",2400,36,None),
 ("Product-market fit explained","product-market-fit","definition","product market fit",6600,44,GC),
 ("Go-to-market metrics and KPIs","go-to-market-metrics","guide","go to market metrics",110,24,GC),
 ("Go-to-market for the UAE","go-to-market-for-the-uae","guide","go to market uae",90,26,"gtm-strategy-uae"),
]
for t, s, ctype, kw, vol, kd, money in A:
    mk = "UAE" if s in ("go-to-market-for-the-uae",) else "global"
    records.append(r(t, s, "authority", ctype, kw, vol, kd, money=money, market=mk))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch14: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
