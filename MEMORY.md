# Memory — The Pearson Co. content engine

Durable facts and current state. Update the Current State block in every content commit.

## Current state
- Phase 1 (scaffold) complete. Repo seeded with the live site; engine in place.
- Phase 2 (the 12-month plan) COMPLETE: 1085 records across 14 pillars (15 pillar pages, 115 money, 955 authority) in `content-plan/plan.json`, rendered to `plan.md` + `plan-rows.js`, reviewable in `content-plan/content-plan.html`. Sequenced for publishing via `scripts/sequence_plan.py` (pillars + money front-loaded, authority round-robin; ~91/month).
- Volumes are live Semrush for batches 1-5 (Conversion, RevOps, CRM Implementation, Fractional+Growth, CJM part 1) and indicative (universe doc + domain knowledge) from batch 6 on. Refresh with Semrush when units are available, then re-run `render_plan.py`.
- 60 posts published: the 15 cornerstone pillar pages (seq 1-15), seq 16-39 (money pages across CRO, CRM, fractional, growth, market entry, ecommerce, RevOps pillars in site/services/), plus 21 authority posts in site/blog/: seq 145, 201, 355 published 2026-06-27; seq 356 (cac-and-ltv), seq 357 (crm-implementation-project-plan), seq 358 (fractional-revenue-leadership) published 2026-06-28; seq 359 (founder-stage-growth), seq 360 (csat-explained), seq 361 (types-of-market-entry-strategies) published 2026-06-29; seq 362 (dmaic-explained), seq 363 (re-engagement-campaigns), seq 364 (saas-kpis) published 2026-07-01; seq 365 (best-crm-for-ecommerce), seq 366 (crm-adoption-metrics), seq 367 (defining-pipeline-stages) published 2026-07-01; seq 368 (distribution-channels), seq 369 (using-heatmaps-for-cro), seq 370 (revenue-operations-software) published 2026-07-02; seq 371 (crm-implementation-timeline), seq 372 (fractional-sales-models), seq 373 (when-to-hire-a-growth-consultant) published 2026-07-03. `next_index` = 374, routine resumes at seq 374.
- Netlify git continuous deployment is connected (push to main -> deploy). GA4 (G-3XWNSR5VHF) is live and consent-gated. Sitemap: https://thepearsonco.com/sitemap.xml (64 URLs, submit in GSC).
- The publishing routine (Strategist + 8 souls) is running: 3 posts/run, pointer-based from `build_state.json`. Each new post's publish date is set to the actual run date, not a fixed date. The live-link Slack notification uses Slack's `<url|label>` syntax, one link per line, so links render cleanly instead of bleeding into adjacent text. Watch items: (1) revops-implementation (seq 40) and go-to-market-strategy-consulting (seq 127) money pages are still not-started; the authority posts that would naturally link to them (revenue-operations-software, distribution-channels) currently link to a live sibling money/pillar page instead, revisit once those money pages publish. (2) link_graph.py reports the full graph clean (60 pages, 0 issues) as of the fifteenth run; the three new posts from this run (crm-implementation-timeline, fractional-sales-models, when-to-hire-a-growth-consultant) each received an inbound link from their cluster's existing live authority post to avoid orphan status.

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
