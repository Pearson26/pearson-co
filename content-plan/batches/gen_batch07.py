#!/usr/bin/env python3
"""Batch 7 - Hospitality Tech & Middle East Expansion (85 records). The moat.

Head-term volumes from the keyword-universe doc (market entry strategy ~4,260 global,
hotel technology 2,850, restaurant technology 2,800, hospitality technology 2,010,
hospitality saas 150). Region-locked strings ("middle east market entry" = 0) are not
targeted; we rank for the vertical and market-entry terms and use the Middle East as the
angle. Long-tail volumes are indicative estimates. Idempotent on batch==7.
Run from repo root, then scripts/render_plan.py.
"""
import json, os

PILLAR = "Hospitality Tech & Middle East Expansion"
PID = "hospitality-expansion"
BATCH = 7
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "hospitality-tech-market-entry"
DEF_MONEY = "hospitality-tech-consultant"

WORDS = {"pillar": 2300, "money": 1450, "guide": 1650, "how-to": 1700,
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
        "pillar": ["The vertical and the opportunity", "Why the Middle East, and how to approach it",
                   "How Lauren supports market entry", "From plan to local traction", "What an engagement includes"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which fits and when", "How Lauren would decide"],
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
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\", written for hospitality technology firms, with the Middle East angle where it helps.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillar
records.append(r("Hospitality technology and Middle East market entry", PILLAR_SLUG, "pillar", "pillar", "global", "commercial",
    "hospitality technology", 2010, 40, ad=True,
    sec=["market entry strategy", "hotel technology", "restaurant technology"],
    ang="Hospitality technology firms, in hotels, restaurants and travel, win when their product meets a real local market need. Lauren helps these companies enter and grow across the Middle East with a practical market-entry strategy, local insight and fractional commercial support, so they gain traction without the cost of a full regional team."))

# Money (10)
ME = "middle-east-expansion-consulting"
M = [
 ("Market entry strategy consulting","market-entry-strategy-service","commercial","market entry strategy",4260,47,True,["market entry consultant"]),
 ("Middle East expansion consulting","middle-east-expansion-consulting","commercial","middle east expansion",260,30,False,["middle east market entry"]),
 ("UAE market entry service","uae-market-entry-service","commercial","uae market entry",170,28,False,["enter uae market"]),
 ("GCC market entry service","gcc-market-entry-service","commercial","gcc market entry",110,28,False,["gulf market entry"]),
 ("Hospitality tech market entry","hospitality-tech-market-entry-service","commercial","hospitality technology market entry",90,26,False,["hospitality tech expansion"]),
 ("Hotel technology consulting","hotel-tech-consulting","commercial","hotel technology consulting",110,28,False,["hotel tech advisory"]),
 ("Restaurant technology consulting","restaurant-tech-consulting","commercial","restaurant technology consulting",90,26,False,["restaurant tech advisory"]),
 ("Hospitality SaaS go-to-market","hospitality-saas-go-to-market","commercial","hospitality saas go to market",70,24,False,["hospitality saas growth"]),
 ("Commercial partnerships for hospitality tech","hospitality-tech-sales-partnerships","commercial","hospitality technology partnerships",50,22,False,["channel partnerships hospitality"]),
 ("Hospitality technology consultant","hospitality-tech-consultant","commercial","hospitality technology consultant",90,26,False,["hospitality tech consultant"]),
]
for t, s, intent, kw, vol, kd, ad, sec in M:
    records.append(r(t, s, "money", "money", "UAE", intent, kw, vol, kd, ad=ad, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and the outcomes to expect, with the Middle East as the focus."))

# Authority (74): (title, slug, type, kw, vol, kd, market, money)
A = [
 # Hotel technology (12)
 ("What is hotel technology?","what-is-hotel-technology","definition","hotel technology",2850,40,"global","hotel-tech-consulting"),
 ("Hotel technology trends","hotel-technology-trends","listicle","hotel technology trends",880,34,"global","hotel-tech-consulting"),
 ("Types of hotel technology","types-of-hotel-technology","guide","types of hotel technology",170,26,"global","hotel-tech-consulting"),
 ("A guide to hotel management software","hotel-management-software","comparison","hotel management software",1300,38,"global","hotel-tech-consulting"),
 ("Hotel PMS explained","hotel-pms-explained","definition","hotel pms",1900,38,"global","hotel-tech-consulting"),
 ("The best hotel technology","best-hotel-technology","comparison","best hotel technology",260,30,"global","hotel-tech-consulting"),
 ("Building a hotel tech stack","hotel-tech-stack","guide","hotel tech stack",110,24,"global","hotel-tech-consulting"),
 ("Contactless technology in hotels","contactless-hotel-technology","guide","contactless hotel technology",90,24,"global","hotel-tech-consulting"),
 ("Guest experience technology","hotel-guest-experience-technology","guide","guest experience technology",170,26,"global","hotel-tech-consulting"),
 ("Hotel revenue management technology","hotel-revenue-management-technology","guide","hotel revenue management",480,32,"global","hotel-tech-consulting"),
 ("How hotels choose technology","how-hotels-choose-technology","guide","how hotels buy technology",50,22,"global","hotel-tech-consulting"),
 ("The ROI of hotel technology","hotel-technology-roi","guide","hotel technology roi",40,22,"global","hotel-tech-consulting"),
 # Restaurant technology (12)
 ("What is restaurant technology?","what-is-restaurant-technology","definition","restaurant technology",2800,40,"global","restaurant-tech-consulting"),
 ("Restaurant technology trends","restaurant-technology-trends","listicle","restaurant technology trends",720,34,"global","restaurant-tech-consulting"),
 ("Types of restaurant technology","types-of-restaurant-technology","guide","types of restaurant technology",170,26,"global","restaurant-tech-consulting"),
 ("A guide to restaurant POS systems","restaurant-pos-systems","comparison","restaurant pos system",2400,40,"global","restaurant-tech-consulting"),
 ("A guide to restaurant management software","restaurant-management-software","comparison","restaurant management software",1000,36,"global","restaurant-tech-consulting"),
 ("The best restaurant technology","best-restaurant-technology","comparison","best restaurant technology",170,28,"global","restaurant-tech-consulting"),
 ("Building a restaurant tech stack","restaurant-tech-stack","guide","restaurant tech stack",90,24,"global","restaurant-tech-consulting"),
 ("Online ordering technology for restaurants","online-ordering-technology","guide","online ordering system",1300,38,"global","restaurant-tech-consulting"),
 ("Restaurant automation","restaurant-automation","guide","restaurant automation",480,30,"global","restaurant-tech-consulting"),
 ("Kitchen display systems explained","kitchen-display-systems","definition","kitchen display system",880,32,"global","restaurant-tech-consulting"),
 ("How restaurants choose technology","how-restaurants-choose-technology","guide","how restaurants buy technology",50,22,"global","restaurant-tech-consulting"),
 ("The ROI of restaurant technology","restaurant-technology-roi","guide","restaurant technology roi",40,22,"global","restaurant-tech-consulting"),
 # Hospitality technology / SaaS (12)
 ("Hospitality technology trends","hospitality-technology-trends","listicle","hospitality technology trends",720,34,"global","hospitality-tech-consultant"),
 ("What is hospitality SaaS?","what-is-hospitality-saas","definition","hospitality saas",150,26,"global","hospitality-saas-go-to-market"),
 ("Types of hospitality technology","types-of-hospitality-technology","guide","types of hospitality technology",90,24,"global","hospitality-tech-consultant"),
 ("A guide to hospitality management software","hospitality-management-software","comparison","hospitality management software",480,32,"global","hospitality-tech-consultant"),
 ("Building a hospitality tech stack","hospitality-tech-stack","guide","hospitality tech stack",70,22,"global","hospitality-tech-consultant"),
 ("Guest experience technology in hospitality","hospitality-guest-experience-technology","guide","guest experience technology hospitality",90,24,"global","hospitality-tech-consultant"),
 ("Hospitality technology companies to know","hospitality-technology-companies","listicle","hospitality technology companies",320,30,"global","hospitality-tech-consultant"),
 ("Hospitality technology trends for 2026","hospitality-technology-2026","listicle","hospitality technology 2026",110,26,"global","hospitality-tech-consultant"),
 ("How hospitality technology is sold","how-hospitality-tech-is-sold","guide","selling hospitality technology",40,22,"global","hospitality-saas-go-to-market"),
 ("Hospitality SaaS pricing models","hospitality-saas-pricing","guide","hospitality saas pricing",40,22,"global","hospitality-saas-go-to-market"),
 ("Driving hospitality technology adoption","hospitality-technology-adoption","guide","hospitality technology adoption",40,22,"global","hospitality-tech-consultant"),
 ("The hospitality technology buyer","hospitality-technology-buyer","guide","hospitality technology buyer",30,20,"global","hospitality-tech-consultant"),
 # Market entry strategy (16)
 ("What is a market entry strategy?","what-is-a-market-entry-strategy","definition","what is a market entry strategy",480,30,"global","market-entry-strategy-service"),
 ("A market entry strategy framework","market-entry-strategy-framework","guide","market entry strategy framework",320,30,"global","market-entry-strategy-service"),
 ("Types of market entry strategies","types-of-market-entry-strategies","guide","types of market entry strategies",480,30,"global","market-entry-strategy-service"),
 ("Market entry strategy examples","market-entry-strategy-examples","listicle","market entry strategy examples",320,28,"global","market-entry-strategy-service"),
 ("How to create a market entry strategy","how-to-create-a-market-entry-strategy","how-to","how to create a market entry strategy",170,26,"global","market-entry-strategy-service"),
 ("Market entry modes explained","market-entry-modes","definition","market entry modes",260,28,"global","market-entry-strategy-service"),
 ("Market entry barriers","market-entry-barriers","guide","market entry barriers",170,26,"global","market-entry-strategy-service"),
 ("Market entry risks","market-entry-risks","guide","market entry risks",110,24,"global","market-entry-strategy-service"),
 ("Go-to-market vs market entry","go-to-market-vs-market-entry","comparison","go to market vs market entry",70,22,"global","market-entry-strategy-service"),
 ("A market entry strategy for SaaS","market-entry-strategy-saas","guide","saas market entry strategy",90,24,"global","market-entry-strategy-service"),
 ("A market entry strategy for tech companies","market-entry-strategy-tech","guide","market entry strategy tech",70,24,"global","market-entry-strategy-service"),
 ("An international expansion strategy","international-expansion-strategy","guide","international expansion strategy",320,30,"global","market-entry-strategy-service"),
 ("Market entry research","market-entry-research","guide","market entry research",110,24,"global","market-entry-strategy-service"),
 ("Market sizing for entry","market-sizing","how-to","market sizing",480,30,"global","market-entry-strategy-service"),
 ("A market entry checklist","market-entry-checklist","template","market entry checklist",70,22,"global","market-entry-strategy-service"),
 ("A market entry strategy template","market-entry-strategy-template","template","market entry strategy template",90,22,"global","market-entry-strategy-service"),
 # Middle East / GCC / UAE angle (16)
 ("Expanding into the Middle East","expanding-into-the-middle-east","guide","expanding into the middle east",170,26,"UAE",ME),
 ("Entering the UAE market","entering-the-uae-market","guide","entering the uae market",110,24,"UAE","uae-market-entry-service"),
 ("A GCC market entry guide","gcc-market-entry-guide","guide","gcc market entry",110,26,"UAE","gcc-market-entry-service"),
 ("Doing business in the UAE","doing-business-in-the-uae","guide","doing business in the uae",480,30,"UAE","uae-market-entry-service"),
 ("Setting up a business in Dubai","setting-up-a-business-in-dubai","guide","setting up a business in dubai",1300,36,"UAE","uae-market-entry-service"),
 ("UAE market entry for tech companies","uae-market-entry-tech","guide","uae market entry tech",50,22,"UAE","uae-market-entry-service"),
 ("Selling SaaS in the Middle East","selling-saas-in-the-middle-east","guide","selling saas middle east",40,22,"UAE",ME),
 ("Hospitality technology in the Middle East","hospitality-tech-middle-east","guide","hospitality technology middle east",40,22,"UAE","hospitality-tech-market-entry-service"),
 ("Hotel technology in the GCC","hotel-tech-gcc","guide","hotel technology gcc",30,20,"UAE","hotel-tech-consulting"),
 ("Restaurant technology in the UAE","restaurant-tech-uae","guide","restaurant technology uae",30,20,"UAE","restaurant-tech-consulting"),
 ("Entering the Saudi Arabia market","entering-saudi-arabia-market","guide","saudi arabia market entry",170,26,"UAE","gcc-market-entry-service"),
 ("Expanding into the Middle East without a local team","middle-east-expansion-no-local-team","guide","middle east expansion without office",30,18,"UAE",ME),
 ("Finding distributors and partners in the Middle East","middle-east-distributors","guide","middle east distributors",40,20,"UAE","hospitality-tech-sales-partnerships"),
 ("Cultural considerations for doing business in the Middle East","middle-east-business-culture","guide","middle east business culture",320,28,"UAE",ME),
 ("The Middle East technology market","middle-east-tech-market","guide","middle east tech market",110,24,"UAE",ME),
 ("The GCC hospitality market","gcc-hospitality-market","guide","gcc hospitality market",70,22,"UAE","hospitality-tech-market-entry-service"),
 # GTM & commercial for the vertical (6)
 ("A go-to-market strategy for hospitality tech","gtm-for-hospitality-tech","guide","hospitality tech go to market",50,22,"global","hospitality-saas-go-to-market"),
 ("How to sell to hotels","selling-to-hotels","guide","selling to hotels",110,24,"global","hotel-tech-consulting"),
 ("How to sell to restaurants","selling-to-restaurants","guide","selling to restaurants",90,24,"global","restaurant-tech-consulting"),
 ("Partnerships for market entry","partnerships-for-market-entry","guide","channel partnerships market entry",70,22,"global","hospitality-tech-sales-partnerships"),
 ("A distribution strategy for new markets","distribution-strategy-new-markets","guide","distribution strategy",480,32,"global","market-entry-strategy-service"),
 ("Pricing for a new market","pricing-for-a-new-market","guide","pricing for new market",70,24,"global","market-entry-strategy-service"),
]
for t, s, ctype, kw, vol, kd, market, money in A:
    records.append(r(t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch07: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
