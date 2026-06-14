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
