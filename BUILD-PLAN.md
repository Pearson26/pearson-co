# Build plan and session log

How the content engine runs, and a log of every session. Update this file in every commit
that changes pages (the mandatory docs-update rule in CLAUDE.md).

## The run rhythm
- One run publishes up to **3 posts** (floor 1 if quality requires), inside the 15-routine daily cap.
- Pointer-based: take the next records from `content-plan/plan.md` by `seq >= build_state.next_index`.
- Each run: research → write → humanise → SEO + FAQ → link → build → audit, then rebuild link graph + blog index + sitemap, run the style gate, reconcile state, commit once to `main`, post live links.
- Quality first. Never lower the bar to hit three.

## Phases
1. **Scaffold (done):** repo seeded with the live site; CLAUDE.md, workforce, templates, blog.css, scripts, state and docs in place.
2. **Plan:** generate `content-plan/plan.md` + `plan.json` + `plan-rows.js` (all ~1,085 records, Semrush-researched) and the client-facing `content-plan.html`.
3. **Front-load (Month 1):** build the 15 pillar pages + the seven ad-landing pillars and priority money pages first, so paid can launch onto live pages.
4. **Fill (Months 2-12):** authority clusters, each post linking up to its pillar and money pages.
5. **Connect Netlify + go live:** point the Netlify site at this repo on `main`; enable the deploy workflow; add tracking IDs when ready.

## Allocation (indicative, from ARCHITECTURE.md, to refine)
Process Mapping & SOP 150 · Customer Journey Mapping 120 · CRM Automation 95 · RevOps 95 ·
Reporting/Dashboards/Forecasting 95 · Conversion & Funnel 95 · Go-to-Market 85 · Hospitality & Expansion 85 ·
CRM Implementation 70 · CRM Consulting 70 · Fractional Leadership 35 · CRM Adoption 35 ·
Sales Pipeline 30 · Growth Consulting 25. Total ~1,085.

## Session log
| Date | Work | Posts | Slugs | Next |
|------|------|-------|-------|------|
| 2026-06-14 | Seeded repo with the live website files. | 0 | (site files) | Build the engine scaffold. |
| 2026-06-14 | Scaffolded the content engine: CLAUDE.md, 9 workforce souls, article template, blog.css, scripts (style_gate, sitemap, blog_index, verify_state, link_graph), state and docs, orchestrator prompt, deploy workflow (inert). | 0 | (engine) | Generate the 12-month plan (plan.md / plan.json / content-plan.html). |
| 2026-06-14 | Plan infrastructure + Batch 1 of 14: Conversion & Funnel Optimisation, 95 records (1 pillar, 12 money, 82 authority), Semrush-researched UK cluster. plan.json/plan.md/dashboard live. | 0 (plan) | conversion-rate-optimisation + 94 | Batch 2: Revenue Operations (RevOps), 95. |
| 2026-06-14 | Batch 2 of 14: Revenue Operations (RevOps), 95 records (1 pillar, 10 money, 84 authority), Semrush-researched US cluster. Total plan 190/1085. | 0 (plan) | revenue-operations + 94 | Batch 3: CRM Implementation & Selection, 70. |
| 2026-06-14 | Batch 3 of 14: CRM Implementation & Selection, 70 records (1 pillar, 14 money, 55 authority), Semrush US+UK clusters. Platform-vs and best-CRM-for-X reserved for Batch 12. Total plan 260/1085. | 0 (plan) | crm-implementation + 69 | Batch 4: Fractional Sales Leadership + Growth Consulting, 60. |
| 2026-06-14 | Batch 4 of 14: Fractional Sales Leadership (35) + Growth Consulting (25), 60 records, Semrush US/global clusters. Both ad-landing pillars. Total plan 320/1085. | 0 (plan) | fractional-sales-leadership, growth-consulting + 58 | Batch 5: Customer Journey Mapping (part 1), 60. |
| 2026-06-14 | Batch 5 of 14: Customer Journey Mapping part 1, 60 records (1 pillar, 4 money, 55 authority), Semrush US cluster. Sixth ad-landing pillar. Total plan 380/1085. NOTE: Semrush API units exhausted mid-batch; batches 6-14 may use indicative volumes (universe doc + prior pulls) until units topped up. | 0 (plan) | customer-journey-mapping + 59 | Batch 6: Customer Journey Mapping (part 2), 60. |
| 2026-06-14 | Batch 6 of 14: Customer Journey Mapping part 2, 60 authority records (indicative volumes). CJM pillar now complete at 120. Total plan 440/1085. | 0 (plan) | 60 CJM authority posts | Batch 7: Hospitality Tech & Middle East Expansion, 85. |
| 2026-06-14 | Batch 7 of 14: Hospitality Tech & Middle East Expansion, 85 records (1 pillar, 10 money, 74 authority). Grounded in universe-doc head terms; vertical + market-entry terms with the ME as the angle. Total plan 525/1085. | 0 (plan) | hospitality-tech-market-entry + 84 | Batch 8: Process Mapping & SOP (part 1), 75. |
| 2026-06-14 | Batch 8 of 14: Process Mapping & SOP Creation part 1, 75 records (2 pillar hubs SOP + process mapping, 7 money, 66 authority). SOP + process-mapping foundations, how-to, templates, tools, documentation. Total plan 600/1085. | 0 (plan) | standard-operating-procedures, process-mapping + 73 | Batch 9: Process Mapping & SOP (part 2), 75. |
| 2026-06-14 | Batch 9 of 14: Process Mapping & SOP part 2, 75 records (6 money, 69 authority). Restaurant/food/hospitality SOP sub-cluster, industry+department SOPs, process-improvement methodologies (lean, six sigma, BPM), workflow automation. Pillar complete at 150. Total plan 675/1085. | 0 (plan) | 6 money + 69 authority | Batch 10: CRM Automation & Workflow, 95. |
| 2026-06-14 | Batch 10 of 14: CRM Automation & Workflow, 95 records (1 pillar, 10 money, 84 authority). CRM/sales/marketing automation, what-to-automate use-cases, platform workflows (HubSpot/Salesforce/Zoho/Zapier), email + sales automation. Total plan 770/1085. | 0 (plan) | crm-automation + 94 | Batch 11: Sales Reporting, Dashboards & Forecasting, 95. |
| 2026-06-14 | Batch 11 of 14: Sales Reporting, Dashboards & Forecasting, 95 records (1 pillar, 10 money, 84 authority). Dashboards, forecasting methods/models, sales metrics/KPIs (no overlap with Batch 2 RevOps metrics), reporting, analytics. Total plan 865/1085. | 0 (plan) | sales-dashboards + 94 | Batch 12: CRM Consulting & Selection, 70. |
| 2026-06-14 | Batch 12 of 14: CRM Consulting & Selection, 70 records (1 pillar, 14 money, 55 authority). Platform-vs-platform comparisons + best-CRM-for-[sector] (reserved from Batch 3), consultant hiring guides, selection deep-dives. Total plan 935/1085. | 0 (plan) | crm-consulting + 69 | Batch 13: CRM Adoption + Sales Pipeline Management, 65. |
| 2026-06-15 | Batch 13 of 14: CRM Adoption (35) + Sales Pipeline Management (30), 65 records. Adoption = Lauren's specialism (drive adoption, change mgmt, training, reviving a dead CRM); pipeline supports CRM/forecasting. Total plan 1000/1085. | 0 (plan) | crm-adoption, sales-pipeline-management + 63 | Batch 14: Go-to-Market Strategy, 85 (final), then sequencing pass. |
