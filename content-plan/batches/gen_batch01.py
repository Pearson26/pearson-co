#!/usr/bin/env python3
"""Batch 1 - Conversion & Funnel Optimisation (95 records).

Holds the Semrush-researched cluster for this pillar and emits full records into
content-plan/plan.json (idempotent: replaces any existing batch==1 records).
Volumes are Semrush UK estimates (June 2026); KD is indicative. Run from repo root,
then run scripts/render_plan.py.
"""
import json, os

PILLAR = "Conversion & Funnel Optimisation"
PID = "conversion-funnel"
BATCH = 1
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "conversion-rate-optimisation"

WORDS = {"pillar": 2200, "money": 1450, "guide": 1700, "how-to": 1700,
         "comparison": 1500, "definition": 1150, "listicle": 1350, "benchmark": 1350}

ENGINES = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

def llm_phrasing(kw, ctype):
    k = kw.lower()
    if ctype in ("how-to",) and not k.startswith(("how", "what", "why")):
        return "how do I " + kw
    if ctype == "comparison" and not k.startswith(("best", "what")):
        return "what is the best " + kw
    if ctype == "benchmark" and not k.startswith(("what", "average")):
        return "what is a good " + kw
    return kw

def outline(ctype, kw):
    t = {
        "pillar": ["What it is and why it matters commercially", "Where revenue leaks in the funnel",
                   "How Lauren approaches it", "What an engagement includes", "Results and what to expect"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["What to look for", "The options compared", "Which to choose and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it is measured", "A practical example"],
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
    if role == "pillar":
        up = []
    elif role == "money":
        up = [PILLAR_SLUG]
    else:
        up = [PILLAR_SLUG, money or "conversion-rate-optimisation-services"]
    return {
        "seq": None, "batch": BATCH, "pillar": PILLAR, "pillar_id": PID,
        "role": role, "content_type": ctype, "is_ad_landing": ad,
        "title": title, "url_slug": slug, "target_market": market, "intent": intent,
        "primary_keyword": kw, "primary_volume": vol, "primary_kd": kd,
        "secondary_keywords": sec or [],
        "llm_layer_keywords": [{"engine": ENGINES[i % 4], "phrasing": llm_phrasing(kw, ctype)}],
        "direct_answer": ang or "",
        "h2_outline": outline(ctype, kw),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": lateral or []},
        "external_links": [],
        "schema_required": schema,
        "ai_overview_play": "Lead with a direct definition and a short checklist so it lifts into AI overviews.",
        "status": "not-started",
    }

# ---- Pillar (1) ----
records.append(r("Conversion and funnel optimisation", PILLAR_SLUG, "pillar", "pillar", "UK", "commercial",
    "conversion rate optimisation", 3600, 38, ad=True,
    sec=["cro", "conversion optimisation", "increase conversion rate"],
    ang="Conversion rate optimisation finds and fixes where a website and sales funnel lose ready-to-buy visitors, then proves the lift with testing. This is how Lauren turns existing traffic into more enquiries without spending more on ads."))

# ---- Money / service pages (12) ----
M = [
 ("Conversion rate optimisation services", "conversion-rate-optimisation-services", "commercial", "conversion rate optimisation services", 1900, 20, True, ["cro services","conversion optimisation services"]),
 ("Conversion rate optimisation consultant", "conversion-rate-optimisation-consultant", "commercial", "conversion rate optimisation consultant", 390, 22, True, ["cro consultant","conversion optimisation consultant"]),
 ("Conversion rate optimisation audit", "conversion-rate-optimisation-audit", "transactional", "conversion rate optimisation audit", 260, 22, True, ["cro audit","conversion audit"]),
 ("B2B conversion rate optimisation", "b2b-conversion-rate-optimisation", "commercial", "b2b conversion rate optimisation", 140, 20, False, ["b2b cro"]),
 ("Ecommerce conversion rate optimisation", "ecommerce-conversion-rate-optimisation", "commercial", "ecommerce conversion rate optimisation", 320, 25, False, ["ecommerce cro"]),
 ("SaaS conversion rate optimisation", "saas-conversion-rate-optimisation", "commercial", "saas conversion rate optimisation", 90, 22, False, ["saas cro"]),
 ("Sales funnel optimisation", "sales-funnel-optimisation", "commercial", "sales funnel optimisation", 110, 22, False, ["funnel optimisation"]),
 ("Sales funnel audit", "sales-funnel-audit", "transactional", "sales funnel audit", 70, 20, False, ["funnel review"]),
 ("Lead management and routing setup", "lead-management-setup", "transactional", "lead management process", 110, 24, False, ["lead routing","lead management setup"]),
 ("Landing page optimisation service", "landing-page-optimisation", "commercial", "landing page optimisation", 140, 25, False, ["landing page conversion"]),
 ("Conversion rate optimisation UK", "conversion-rate-optimisation-uk", "commercial", "conversion rate optimisation uk", 390, 22, True, ["cro agency uk","cro uk"]),
 ("Conversion rate optimisation strategy", "conversion-rate-optimisation-strategy", "commercial", "conversion rate optimisation strategy", 140, 20, False, ["cro strategy"]),
]
for t, s, intent, kw, vol, kd, ad, sec in M:
    records.append(r(t, s, "money", "money", "UK", intent, kw, vol, kd, ad=ad, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how the engagement runs and the outcomes to expect."))

# ---- Authority (82): (title, slug, type, kw, vol, kd, money_link) ----
A = [
 # Foundations
 ("What is conversion rate optimisation?","what-is-conversion-rate-optimisation","definition","what is conversion rate optimisation",480,20,None),
 ("What is a good conversion rate?","what-is-a-good-conversion-rate","definition","what is a good conversion rate",320,22,None),
 ("How to calculate conversion rate","how-to-calculate-conversion-rate","how-to","how to calculate conversion rate",210,15,None),
 ("What is CRO in marketing?","what-is-cro-in-marketing","definition","what is cro in marketing",110,18,None),
 ("Conversion rate optimisation explained for founders","conversion-rate-optimisation-explained","guide","conversion rate optimisation explained",70,18,None),
 ("CRO and SEO: how they work together","cro-vs-seo","comparison","cro and seo",260,25,None),
 ("Macro vs micro conversions explained","macro-vs-micro-conversions","definition","micro conversions",90,18,None),
 ("Conversion rate vs click-through rate","conversion-rate-vs-click-through-rate","comparison","conversion rate vs ctr",70,15,None),
 # How-to / improve
 ("How to improve your conversion rate","how-to-improve-conversion-rate","how-to","how to improve conversion rate",110,22,"conversion-rate-optimisation-audit"),
 ("How to increase your conversion rate","how-to-increase-conversion-rate","how-to","how to increase conversion rate",110,22,"conversion-rate-optimisation-audit"),
 ("How to increase website conversions","how-to-increase-website-conversion-rate","how-to","increase website conversions",110,24,None),
 ("How to improve B2B website conversion","improve-b2b-website-conversion","how-to","b2b website conversion",70,20,"b2b-conversion-rate-optimisation"),
 ("How to boost your conversion rate","how-to-boost-conversion-rate","how-to","boost conversion rate",110,20,"conversion-rate-optimisation-audit"),
 ("How to optimise a landing page for conversions","how-to-optimise-a-landing-page","how-to","landing page optimisation",140,25,"landing-page-optimisation"),
 ("How to run a CRO programme","how-to-run-a-cro-programme","how-to","cro programme",50,20,"conversion-rate-optimisation-services"),
 ("How to do a conversion audit, step by step","how-to-do-a-conversion-audit","how-to","conversion audit",90,22,"conversion-rate-optimisation-audit"),
 ("How to set CRO goals and KPIs","cro-goals-and-kpis","guide","cro kpis",40,18,None),
 ("How to prioritise CRO experiments","how-to-prioritise-cro-experiments","how-to","cro prioritisation",30,18,None),
 ("How to build a CRO roadmap","how-to-build-a-cro-roadmap","how-to","cro roadmap",30,18,"conversion-rate-optimisation-strategy"),
 ("How to measure CRO impact","how-to-measure-cro-impact","how-to","measure cro",30,18,None),
 # Techniques
 ("Conversion rate optimisation techniques that work","conversion-rate-optimisation-techniques","listicle","conversion rate optimisation techniques",50,18,None),
 ("Conversion rate optimisation best practices","conversion-rate-optimisation-best-practices","listicle","conversion rate optimisation best practice",40,18,None),
 ("Conversion rate optimisation strategies","conversion-rate-optimisation-strategies","listicle","conversion rate optimisation strategies",70,20,"conversion-rate-optimisation-strategy"),
 ("A guide to A/B testing for conversion","ab-testing-for-conversion","guide","a/b testing",320,30,None),
 ("A/B testing mistakes to avoid","ab-testing-mistakes","listicle","a/b testing mistakes",50,20,None),
 ("Multivariate testing explained","multivariate-testing-explained","definition","multivariate testing",110,25,None),
 ("Using heatmaps for CRO","using-heatmaps-for-cro","how-to","heatmaps",210,25,None),
 ("Using session recordings to find friction","session-recordings-for-cro","how-to","session recordings",90,22,None),
 ("Form optimisation to lift conversions","form-optimisation","how-to","form optimisation",70,22,None),
 ("Call-to-action optimisation that converts","cta-optimisation","how-to","call to action optimisation",50,20,None),
 ("Social proof and conversions","social-proof-and-conversions","guide","social proof",320,28,None),
 ("Reducing friction in checkout and forms","reducing-friction-in-checkout","how-to","checkout optimisation",90,24,"ecommerce-conversion-rate-optimisation"),
 ("Page speed and conversion rate","page-speed-and-conversion-rate","guide","page speed conversion",70,22,None),
 ("Mobile conversion rate optimisation","mobile-conversion-rate-optimisation","guide","mobile conversion rate",90,22,None),
 # Funnel
 ("What is a sales funnel?","what-is-a-sales-funnel","definition","what is a sales funnel",260,20,"sales-funnel-optimisation"),
 ("Sales funnel stages explained","sales-funnel-stages","guide","sales funnel stages",480,25,"sales-funnel-optimisation"),
 ("Sales funnel examples","sales-funnel-examples","listicle","sales funnel examples",210,22,"sales-funnel-optimisation"),
 ("A B2B sales funnel guide","b2b-sales-funnel-guide","guide","b2b sales funnel",90,22,"b2b-conversion-rate-optimisation"),
 ("How to build a sales funnel","how-to-build-a-sales-funnel","how-to","how to create a sales funnel",110,24,"sales-funnel-optimisation"),
 ("Sales funnel vs marketing funnel","sales-funnel-vs-marketing-funnel","comparison","sales funnel vs marketing funnel",70,18,None),
 ("Top, middle and bottom of funnel explained","top-middle-bottom-of-funnel","guide","tofu mofu bofu",90,20,None),
 ("Where your sales funnel leaks revenue","where-your-sales-funnel-leaks","guide","sales funnel leaks",40,18,"sales-funnel-audit"),
 ("How to fix a leaking sales funnel","how-to-fix-a-leaking-sales-funnel","how-to","fix sales funnel",30,18,"sales-funnel-audit"),
 ("Funnel conversion benchmarks by stage","funnel-conversion-benchmarks","benchmark","funnel conversion rate",70,22,None),
 ("The purchase funnel explained","purchase-funnel-explained","definition","purchase funnel",170,22,None),
 ("Customer funnel mapping","customer-funnel-mapping","guide","customer funnel",90,22,None),
 ("Funnel metrics that matter","funnel-metrics-that-matter","guide","funnel metrics",50,20,None),
 ("A SaaS sales funnel guide","saas-sales-funnel-guide","guide","saas sales funnel",70,22,"saas-conversion-rate-optimisation"),
 ("A sales funnel for service businesses","sales-funnel-for-service-businesses","guide","sales funnel for services",40,18,None),
 ("Funnel-stage conversion rates","funnel-stage-conversion-rates","benchmark","funnel stage conversion rates",30,18,None),
 # Lead management
 ("What is lead management?","what-is-lead-management","definition","lead management process",110,22,"lead-management-setup"),
 ("The lead management process, step by step","lead-management-process-steps","how-to","lead management steps",50,20,"lead-management-setup"),
 ("Lead routing best practices","lead-routing-best-practices","guide","lead routing",110,24,"lead-management-setup"),
 ("Speed to lead: why response time decides the deal","speed-to-lead","guide","lead response time",90,22,"lead-management-setup"),
 ("Lead scoring basics","lead-scoring-basics","guide","lead scoring",320,30,None),
 ("Lead qualification frameworks compared","lead-qualification-frameworks","guide","lead qualification",210,26,None),
 ("MQL vs SQL explained","mql-vs-sql","definition","mql vs sql",260,24,None),
 ("Lead nurturing for B2B","lead-nurturing-for-b2b","guide","lead nurturing",390,30,None),
 ("Reducing lead leakage in your CRM","reducing-lead-leakage","guide","lead leakage",30,18,"lead-management-setup"),
 ("Lead management software compared","lead-management-software-compared","comparison","lead management software",590,35,"lead-management-setup"),
 # Metrics & benchmarks
 ("Average conversion rate by industry","average-conversion-rate-by-industry","benchmark","average conversion rate",320,25,None),
 ("B2B conversion rate benchmarks","b2b-conversion-rate-benchmarks","benchmark","b2b conversion rate",110,22,"b2b-conversion-rate-optimisation"),
 ("SaaS conversion rate benchmarks","saas-conversion-rate-benchmarks","benchmark","saas conversion rate",90,22,"saas-conversion-rate-optimisation"),
 ("Ecommerce conversion rate benchmarks","ecommerce-conversion-rate-benchmarks","benchmark","ecommerce conversion rate",210,25,"ecommerce-conversion-rate-optimisation"),
 ("Landing page conversion benchmarks","landing-page-conversion-benchmarks","benchmark","landing page conversion rate",70,22,"landing-page-optimisation"),
 ("What is a good lead-to-customer rate?","good-lead-to-customer-rate","benchmark","lead to customer conversion rate",50,20,None),
 ("Cost per conversion explained","cost-per-conversion-explained","definition","cost per conversion",170,22,None),
 ("The conversion rate formula, with examples","conversion-rate-formula","definition","conversion rate formula",210,18,None),
 # Tools & comparisons
 ("The best CRO tools","best-cro-tools","comparison","conversion rate optimisation tools",140,28,None),
 ("The best A/B testing tools","best-ab-testing-tools","comparison","a/b testing tools",210,30,None),
 ("The best heatmap tools","best-heatmap-tools","comparison","heatmap tools",170,26,None),
 ("Google Optimize alternatives","google-optimize-alternatives","comparison","google optimize alternative",320,28,None),
 ("CRO tools for small teams","cro-tools-for-small-teams","comparison","cro tools",260,26,None),
 ("Setting up GA4 for conversion tracking","ga4-for-cro","how-to","ga4 conversion tracking",140,25,None),
 ("The best landing page builders","best-landing-page-builders","comparison","landing page builder",480,35,"landing-page-optimisation"),
 ("Free CRO tools worth using","free-cro-tools","listicle","free cro tools",50,20,None),
 # Industry / use-case
 ("An ecommerce CRO guide","ecommerce-cro-guide","guide","ecommerce conversion rate optimisation",320,25,"ecommerce-conversion-rate-optimisation"),
 ("Shopify conversion rate optimisation","shopify-conversion-rate-optimisation","guide","shopify conversion rate optimisation",110,24,"ecommerce-conversion-rate-optimisation"),
 ("A SaaS CRO guide","saas-cro-guide","guide","saas conversion rate optimisation",90,22,"saas-conversion-rate-optimisation"),
 ("Improving hotel and hospitality website conversion","hotel-website-conversion","guide","hotel website conversion",50,20,None),
 ("CRO for lead-generation websites","cro-for-lead-generation-websites","guide","lead generation website",110,24,"lead-management-setup"),
 ("CRO for B2B service businesses","cro-for-b2b-service-businesses","guide","b2b cro",140,22,"b2b-conversion-rate-optimisation"),
]
for t, s, ctype, kw, vol, kd, money in A:
    market = "global" if ctype in ("definition", "benchmark", "comparison") else "UK"
    records.append(r(t, s, "authority", ctype, market, "informational", kw, vol, kd, money=money,
        ang=f"A practical, plain-English answer to \"{kw}\" for founder-led teams, with a clear next step."))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    roles = {}
    for r_ in records:
        roles[r_["role"]] = roles.get(r_["role"], 0) + 1
    print(f"batch01: wrote {len(records)} records ({roles}). plan.json now {len(plan)} records.")

if __name__ == "__main__":
    main()
