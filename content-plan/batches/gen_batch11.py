#!/usr/bin/env python3
"""Batch 11 - Sales Reporting, Dashboards & Forecasting (95 records).

High commercial value (universe UK 1,210 / US 5,300; dashboard CPCs above $13). Money +
authority. Dashboards, forecasting, sales metrics/KPIs, reporting and analytics. Avoids the
RevOps metrics already covered in Batch 2 (NRR, sales velocity, win rate, pipeline coverage,
CAC/LTV). Volumes indicative (universe doc + domain knowledge). Idempotent on batch==11.
"""
import json, os

PILLAR = "Sales Reporting, Dashboards & Forecasting"
PID = "reporting-forecasting"
BATCH = 11
PLAN = "content-plan/plan.json"
PILLAR_SLUG = "sales-dashboards"
DEF_MONEY = "sales-dashboard-service"

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
        "pillar": ["What sales reporting, dashboards and forecasting cover", "Why pipeline visibility matters",
                   "How Lauren sets up reporting", "From dashboard to decision", "What an engagement includes"],
        "money": ["Who this is for", "What is included", "How the engagement works", "Outcomes and proof"],
        "how-to": ["The short answer", "Step by step", "A worked example", "Common mistakes"],
        "guide": ["The short answer", "How it works in practice", "What good looks like", "Pitfalls to avoid"],
        "comparison": ["The short answer", "How they differ", "Which to use and when", "How Lauren would decide"],
        "definition": ["The short answer", "Why it matters", "How it is calculated", "A practical example"],
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
        "direct_answer": ang or f"A practical, plain-English answer to \"{kw}\" for founder-led teams that need clearer pipeline visibility, with a clear next step.",
        "h2_outline": outline(ctype),
        "word_count_target": WORDS.get(ctype if role != "money" else "money", 1500),
        "internal_links": {"up": up, "lateral": []},
        "external_links": [], "schema_required": schema,
        "ai_overview_play": "Lead with a direct answer and a short checklist or metric list so it lifts into AI overviews.",
        "status": "not-started", "volume_source": "indicative",
    }

# Pillar
records.append(r("Sales reporting, dashboards and forecasting", PILLAR_SLUG, "pillar", "pillar",
    "sales dashboard", 1900, 30, ad=False,
    sec=["sales forecasting", "crm dashboard", "sales reporting"],
    ang="Sales reporting, dashboards and forecasting turn CRM data into a clear picture of what is happening and what comes next, so leadership can trust the numbers and act early. This is how Lauren builds dashboards and a forecast your team will actually use."))

DASH = "sales-dashboard-service"; CRMD = "crm-dashboard-service"; FC = "sales-forecasting-service"; RPT = "reporting-setup-service"; ANA = "sales-analytics-consulting"; FCM = "sales-forecast-model-service"
M = [
 ("Sales dashboard build service","sales-dashboard-service","sales dashboard",1900,30,["build a sales dashboard"]),
 ("CRM dashboard service","crm-dashboard-service","crm dashboard",1000,30,["crm dashboard setup"]),
 ("Sales forecasting service","sales-forecasting-service","sales forecasting",2400,36,["sales forecast consulting"]),
 ("Sales reporting setup","reporting-setup-service","sales reporting",1300,32,["reporting setup"]),
 ("Sales analytics consulting","sales-analytics-consulting","sales analytics",880,32,["revenue analytics consulting"]),
 ("Revenue reporting service","revenue-reporting-service","revenue reporting",320,28,["board reporting"]),
 ("HubSpot dashboard service","hubspot-dashboard-service","hubspot dashboard",480,30,["hubspot reporting"]),
 ("Salesforce dashboard service","salesforce-dashboard-service","salesforce dashboard",1300,34,["salesforce reporting"]),
 ("Power BI sales dashboard service","power-bi-dashboard-service","power bi sales dashboard",480,32,["power bi reporting"]),
 ("Sales forecast model service","sales-forecast-model-service","sales forecast model",170,26,["forecasting model build"]),
]
for t, s, kw, vol, kd, sec in M:
    records.append(r(t, s, "money", "money", kw, vol, kd, sec=sec,
        ang=f"What Lauren's {t.lower()} covers, who it suits, how it runs and what you get."))

A = [
 # Dashboards: foundations + how-to (14)
 ("What is a sales dashboard?","what-is-a-sales-dashboard","definition","what is a sales dashboard",480,26,DASH),
 ("How to build a sales dashboard","how-to-build-a-sales-dashboard","how-to","how to build a sales dashboard",320,28,DASH),
 ("Sales dashboard examples","sales-dashboard-examples","listicle","sales dashboard examples",880,30,DASH),
 ("Sales dashboard metrics","sales-dashboard-metrics","guide","sales dashboard metrics",170,24,DASH),
 ("Sales dashboard best practices","sales-dashboard-best-practices","listicle","sales dashboard best practices",90,22,DASH),
 ("What is a CRM dashboard?","what-is-a-crm-dashboard","definition","what is a crm dashboard",320,26,CRMD),
 ("CRM dashboard examples","crm-dashboard-examples","listicle","crm dashboard examples",480,28,CRMD),
 ("CRM dashboard metrics","crm-dashboard-metrics","guide","crm dashboard metrics",110,22,CRMD),
 ("Sales dashboard design principles","sales-dashboard-design","guide","sales dashboard design",170,24,DASH),
 ("Building a real-time sales dashboard","real-time-sales-dashboard","guide","real time sales dashboard",110,24,DASH),
 ("An executive sales dashboard","executive-sales-dashboard","guide","executive sales dashboard",170,24,DASH),
 ("A sales rep dashboard","sales-rep-dashboard","guide","sales rep dashboard",90,22,DASH),
 ("A sales manager dashboard","sales-manager-dashboard","guide","sales manager dashboard",110,22,DASH),
 ("A sales KPI dashboard","sales-kpi-dashboard","guide","sales kpi dashboard",320,26,DASH),
 # Dashboard templates & tools (12)
 ("A sales dashboard template","sales-dashboard-template","template","sales dashboard template",880,28,DASH),
 ("A CRM dashboard template","crm-dashboard-template","template","crm dashboard template",320,26,CRMD),
 ("A sales dashboard in Excel","excel-sales-dashboard","guide","excel sales dashboard",1300,34,DASH),
 ("A sales dashboard in Google Sheets","google-sheets-sales-dashboard","guide","google sheets sales dashboard",480,30,DASH),
 ("A sales dashboard in Power BI","power-bi-sales-dashboard","guide","power bi sales dashboard",480,32,"power-bi-dashboard-service"),
 ("A sales dashboard in Tableau","tableau-sales-dashboard","guide","tableau sales dashboard",320,30,ANA),
 ("Sales dashboards in HubSpot","hubspot-sales-dashboard","guide","hubspot dashboard",480,30,"hubspot-dashboard-service"),
 ("Sales dashboards in Salesforce","salesforce-sales-dashboard","guide","salesforce dashboard",1300,34,"salesforce-dashboard-service"),
 ("The best sales dashboard software","best-sales-dashboard-software","comparison","sales dashboard software",480,30,None),
 ("Sales dashboard tools","sales-dashboard-tools","comparison","sales dashboard tools",320,28,None),
 ("A free sales dashboard template","free-sales-dashboard-template","template","free sales dashboard template",170,24,DASH),
 ("A sales dashboard in Looker Studio","looker-studio-sales-dashboard","guide","looker studio sales dashboard",170,26,ANA),
 # Forecasting: foundations + methods (16)
 ("What is sales forecasting?","what-is-sales-forecasting","definition","what is sales forecasting",880,30,FC),
 ("How to forecast sales","how-to-forecast-sales","how-to","how to forecast sales",480,30,FC),
 ("Sales forecasting methods","sales-forecasting-methods","guide","sales forecasting methods",880,30,FC),
 ("Sales forecasting models","sales-forecasting-models","guide","sales forecasting models",480,30,FCM),
 ("A sales forecast template","sales-forecast-template","template","sales forecast template",1300,32,FCM),
 ("Sales forecasting examples","sales-forecasting-examples","listicle","sales forecasting examples",320,26,FC),
 ("How to improve sales forecast accuracy","sales-forecast-accuracy","guide","sales forecast accuracy",170,24,FC),
 ("Demand forecasting explained","demand-forecasting","definition","demand forecasting",2400,38,FC),
 ("Revenue forecasting explained","revenue-forecasting","definition","revenue forecasting",880,32,FC),
 ("Pipeline forecasting","pipeline-forecasting","guide","pipeline forecasting",170,26,FC),
 ("Bottom-up vs top-down forecasting","bottom-up-vs-top-down-forecasting","comparison","bottom up vs top down forecasting",110,22,FC),
 ("Sales forecasting for startups","sales-forecasting-for-startups","guide","sales forecasting for startups",170,26,FC),
 ("Sales forecasting in Excel","sales-forecasting-in-excel","guide","sales forecasting excel",480,30,FCM),
 ("Sales forecasting best practices","sales-forecasting-best-practices","listicle","sales forecasting best practices",110,22,FC),
 ("How to set sales quotas","quota-setting","how-to","sales quota setting",320,28,FC),
 ("The best sales forecasting software","sales-forecasting-software","comparison","sales forecasting software",480,32,None),
 # Sales metrics & KPIs (18) - avoids Batch 2 RevOps metrics
 ("The sales KPIs that matter","sales-kpis","listicle","sales kpis",1000,30,ANA),
 ("Sales metrics explained","sales-metrics","guide","sales metrics",1300,32,ANA),
 ("The sales metrics that matter most","sales-metrics-that-matter","listicle","sales metrics that matter",90,22,ANA),
 ("Sales KPI examples","sales-kpi-examples","listicle","sales kpi examples",170,24,ANA),
 ("Sales performance metrics","sales-performance-metrics","guide","sales performance metrics",320,26,ANA),
 ("Revenue metrics explained","revenue-metrics","guide","revenue metrics",320,28,ANA),
 ("SaaS metrics explained","saas-metrics","definition","saas metrics",2400,38,ANA),
 ("SaaS KPIs explained","saas-kpis","listicle","saas kpis",880,32,ANA),
 ("Sales conversion metrics","sales-conversion-metrics","guide","sales conversion rate metrics",110,22,ANA),
 ("Sales pipeline metrics","pipeline-metrics","guide","sales pipeline metrics",170,24,ANA),
 ("Sales activity metrics","sales-activity-metrics","guide","sales activity metrics",110,22,ANA),
 ("Leading vs lagging indicators","leading-vs-lagging-indicators","comparison","leading vs lagging indicators",880,30,None),
 ("Quota attainment explained","quota-attainment","definition","quota attainment",480,28,ANA),
 ("Average deal size explained","average-deal-size","definition","average deal size",480,28,None),
 ("Sales cycle length explained","sales-cycle-length","definition","sales cycle length",880,30,None),
 ("ARR vs MRR explained","arr-and-mrr","definition","arr vs mrr",1300,34,None),
 ("Churn rate explained","churn-rate","definition","churn rate",6600,42,None),
 ("Bookings vs billings vs revenue","bookings-billings-revenue","comparison","bookings vs revenue",90,22,None),
 # Reporting: foundations + how-to (14)
 ("What is sales reporting?","what-is-sales-reporting","definition","what is sales reporting",320,24,RPT),
 ("How to create a sales report","how-to-create-a-sales-report","how-to","how to create a sales report",320,26,RPT),
 ("A sales report template","sales-report-template","template","sales report template",1300,32,RPT),
 ("Sales report examples","sales-report-examples","listicle","sales report examples",320,26,RPT),
 ("Types of sales reports","types-of-sales-reports","guide","types of sales reports",170,22,RPT),
 ("A weekly sales report","weekly-sales-report","template","weekly sales report",320,26,RPT),
 ("A monthly sales report","monthly-sales-report","template","monthly sales report",320,26,RPT),
 ("A sales performance report","sales-performance-report","guide","sales performance report",170,24,RPT),
 ("A sales pipeline report","sales-pipeline-report","guide","sales pipeline report",170,24,RPT),
 ("CRM reporting explained","crm-reporting","guide","crm reporting",480,28,CRMD),
 ("Automating your sales reports","automated-sales-reports","guide","automated sales reports",110,24,RPT),
 ("Sales reporting best practices","sales-reporting-best-practices","listicle","sales reporting best practices",90,22,RPT),
 ("Board reporting for sales","board-reporting-sales","guide","board reporting",480,30,"revenue-reporting-service"),
 ("RevOps reporting","revops-reporting-guide","guide","revops reporting",70,22,ANA),
 # Analytics & advanced (10)
 ("What is sales analytics?","what-is-sales-analytics","definition","sales analytics",880,32,ANA),
 ("Predictive sales analytics","predictive-sales-analytics","guide","predictive sales analytics",170,28,ANA),
 ("Revenue analytics explained","revenue-analytics","definition","revenue analytics",320,28,ANA),
 ("Pipeline analytics","pipeline-analytics","guide","pipeline analytics",110,24,ANA),
 ("How to analyse sales data","sales-data-analysis","how-to","sales data analysis",320,28,ANA),
 ("How to read a sales dashboard","how-to-read-a-sales-dashboard","guide","read a sales dashboard",40,18,DASH),
 ("Common dashboard mistakes","dashboard-mistakes","listicle","dashboard mistakes",90,20,DASH),
 ("Building a single source of truth for reporting","single-source-of-truth-reporting","guide","single source of truth",1900,34,RPT),
 ("AI in sales forecasting","ai-in-sales-forecasting","guide","ai sales forecasting",170,28,FC),
 ("Setting up reporting in a new CRM","reporting-in-a-new-crm","guide","crm reporting setup",70,22,RPT),
]
for t, s, ctype, kw, vol, kd, money in A:
    records.append(r(t, s, "authority", ctype, kw, vol, kd, money=money))

def main():
    plan = json.load(open(PLAN, encoding="utf-8")) if os.path.exists(PLAN) else []
    plan = [p for p in plan if p.get("batch") != BATCH]
    plan.extend(records)
    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"batch11: wrote {len(records)} records ({dict(Counter(x['role'] for x in records))}). plan.json now {len(plan)}.")

if __name__ == "__main__":
    main()
