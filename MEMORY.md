# Memory — The Pearson Co. content engine

Durable facts and current state. Update the Current State block in every content commit.

## Current state
- Phase 1 (scaffold) complete. Repo seeded with the live site; engine in place.
- Phase 2 (the 12-month plan) COMPLETE: 1085 records across 14 pillars (15 pillar pages, 115 money, 955 authority) in `content-plan/plan.json`, rendered to `plan.md` + `plan-rows.js`, reviewable in `content-plan/content-plan.html`. Sequenced for publishing via `scripts/sequence_plan.py` (pillars + money front-loaded, authority round-robin; ~91/month).
- Volumes are live Semrush for batches 1-5 (Conversion, RevOps, CRM Implementation, Fractional+Growth, CJM part 1) and indicative (universe doc + domain knowledge) from batch 6 on. Refresh with Semrush when units are available, then re-run `render_plan.py`.
- 51 posts published: the 15 cornerstone pillar pages (seq 1-15), seq 16-39 (money pages across CRO, CRM, fractional, growth, market entry, ecommerce, RevOps pillars in site/services/), plus 12 authority posts in site/blog/: seq 145, 201, 355 published 2026-06-27; seq 356 (cac-and-ltv), seq 357 (crm-implementation-project-plan), seq 358 (fractional-revenue-leadership) published 2026-06-28; seq 359 (founder-stage-growth), seq 360 (csat-explained), seq 361 (types-of-market-entry-strategies) published 2026-06-29; seq 362 (dmaic-explained), seq 363 (re-engagement-campaigns), seq 364 (saas-kpis) published 2026-07-01. `next_index` = 365, routine resumes at seq 365.
- Netlify git continuous deployment is connected (push to main -> deploy). GA4 (G-3XWNSR5VHF) is live and consent-gated. Sitemap: https://thepearsonco.com/sitemap.xml (55 URLs, submit in GSC).
- The publishing routine (Strategist + 8 souls) is running: 3 posts/run, pointer-based from `build_state.json`. Watch items: (1) crm-adoption.html pillar has only 2 inbound authority links; will self-resolve once CRM Adoption cluster publishes. (2) crm-implementation-project-plan (seq 357) is an orphan with no inbound links; fix in next run by adding a link from crm-consulting.html or crm-implementation.html. (3) dmaic-explained, re-engagement-campaigns, saas-kpis (seq 362-364) are new orphans; will self-resolve as cluster posts add inbound links.

## Fixed decisions
- Repo `Pearson26/pearson-co`; push to `main` via `gh` as `ngindubai` (accepted write collaborator).
- Static HTML, no build step. Netlify publish dir = repo root.
- Articles match the **live site** design (#B784A7, Playfair Display + DM Sans), not the agency-document look (#7f466f + Inter, which is for review documents only).
- Authority articles -> `/blog/<slug>.html`; pillar + money pages -> `/services/<slug>.html`. Root-relative asset paths.
- Byline author is Lauren Pearson, Founder.
- Barbell strategy: small set of money pages fed by a large body of authority content; pillar-and-cluster.
- 14 pillars, RevOps confirmed as a full pillar (umbrella adopted).

## Content rules (see CLAUDE.md for the full list)
- British English. No em dashes, ever. Banned words: delve, meticulous, comprehensive, leverage, seamless, robust (+ extended blocklist).
- Light scheme only. Headings use an italic last phrase via `<em>`.
- Every regulatory/statistical claim is sourced; no invented data or client names.

## Mistakes to avoid
- Do not push to a feature branch; deploy only fires on `main`.
- Do not modify index.html / styles.css / script.js during a content run (sitewide changes are a separate job).
- Do not pick work by date; progression is by pointer (`next_index`).
- Do not enable tracking IDs or wire Netlify without an explicit instruction.
