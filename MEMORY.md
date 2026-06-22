# Memory — The Pearson Co. content engine

Durable facts and current state. Update the Current State block in every content commit.

## Current state
- Phase 1 (scaffold) complete. Repo seeded with the live site; engine in place.
- Phase 2 (the 12-month plan) COMPLETE: 1085 records across 14 pillars (15 pillar pages, 115 money, 955 authority) in `content-plan/plan.json`, rendered to `plan.md` + `plan-rows.js`, reviewable in `content-plan/content-plan.html`. Sequenced for publishing via `scripts/sequence_plan.py` (pillars + money front-loaded, authority round-robin; ~91/month).
- Volumes are live Semrush for batches 1-5 (Conversion, RevOps, CRM Implementation, Fractional+Growth, CJM part 1) and indicative (universe doc + domain knowledge) from batch 6 on. Refresh with Semrush when units are available, then re-run `render_plan.py`.
- 30 posts published: the 15 cornerstone pillar pages (seq 1-15), seq 16-27 (CRO, CRM, fractional, growth, market entry, ecommerce money pages), plus seq 28-30 (b2b-conversion-rate-optimisation, landing-page-optimisation, conversion-rate-optimisation-strategy), all live in `site/services/`. `next_index` = 31, routine resumes at seq 31.
- Netlify git continuous deployment is connected (push to main -> deploy). GA4 (G-3XWNSR5VHF) is live and consent-gated. Sitemap: https://thepearsonco.com/sitemap.xml (34 URLs, submit in GSC).
- The publishing routine (Strategist + 8 souls) is running: 3 posts/run, pointer-based from `build_state.json`. Pre-existing watch item: `crm-adoption.html` pillar has only 2 inbound authority links (wants 3); will self-resolve once CRM Adoption authority posts publish.

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
