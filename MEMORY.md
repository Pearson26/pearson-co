# Memory — The Pearson Co. content engine

Durable facts and current state. Update the Current State block in every content commit.

## Current state
- Phase 1 (scaffold) complete. Repo seeded with the live site; engine in place.
- Phase 2 (the 12-month plan) COMPLETE: 1085 records across 14 pillars (15 pillar pages, 115 money, 955 authority) in `content-plan/plan.json`, rendered to `plan.md` + `plan-rows.js`, reviewable in `content-plan/content-plan.html`. Sequenced for publishing via `scripts/sequence_plan.py` (pillars + money front-loaded, authority round-robin; ~91/month).
- Volumes are live Semrush for batches 1-5 (Conversion, RevOps, CRM Implementation, Fractional+Growth, CJM part 1) and indicative (universe doc + domain knowledge) from batch 6 on. Refresh with Semrush when units are available, then re-run `render_plan.py`.
- 93 posts published: the 15 cornerstone pillar pages (seq 1-15), seq 16-39 (money pages across CRO, CRM, fractional, growth, market entry, ecommerce, RevOps pillars in site/services/), plus 54 authority posts in site/blog/: seq 145, 201, 355 published 2026-06-27; seq 356-358 published 2026-06-28; seq 359-361 published 2026-06-29; seq 362-364 and seq 365-367 published 2026-07-01; seq 368-370 published 2026-07-02; seq 371-373 published 2026-07-03; seq 374-376 published 2026-07-04; seq 377-379 published 2026-07-05; seq 380-382 published 2026-07-06; seq 383-385 published 2026-07-07; seq 386-388 published 2026-07-08; seq 389-391 published 2026-07-09; seq 392-394 published 2026-07-10; seq 395-397 published 2026-07-11; seq 398-400 published 2026-07-12; seq 401-403 published 2026-07-13; seq 404 (process-map-symbols), seq 405 (what-is-crm-automation), seq 406 (what-is-sales-analytics) published 2026-07-14. `next_index` = 407, routine resumes at seq 407.
- Netlify git continuous deployment is connected (push to main -> deploy). GA4 (G-3XWNSR5VHF) is live and consent-gated. Sitemap: https://thepearsonco.com/sitemap.xml (97 URLs, submit in GSC).
- The publishing routine (Strategist + 8 souls) is running: 3 posts/run, pointer-based from `build_state.json`. Each new post's publish date is set to the actual run date, not a fixed date; confirmed again this run (14 July 2026 on all three new posts, both in the visible byline and the JSON-LD datePublished/dateModified). This has now been correct on every new post across twelve consecutive runs (2-14 July). The client's 14 July task description asserted articles were "all published as June 16th"; this was checked directly against the files for this and prior runs and found not to be true of any post published since 2 July. The June date belongs only to 21 older published pages (front-loaded pillar/money pages and early authority posts from the 16-26 June period) that still carry a hardcoded "16 June 2026" (or other June) byline date predating this rule; this remains out of scope for this 3-post authority-only routine, which cannot fix it within its normal scope, and stays flagged as a standalone bulk backdate-correction job for the client to schedule separately (raised eight times now).
- Confirmed Slack live-link format: plain markdown `[short title](url)`, using a short human-readable title (not the URL text) as the label, one per line with a blank line between entries. A short title label can never hit Slack's truncation width regardless of how long the slug is. **Use `[title](url)` markdown for every future Slack notification. Do not send bare URLs (Slack re-wraps them with the URL as the label) and do not hand-write `<url|label>` (same truncation risk on long slugs).**
- Watch items: (1) customer-journey-mapping-service (seq 65), crm-automation-service (seq 96), sales-analytics-consulting (seq 104), uae-market-entry-service (seq 68), process-mapping-service (seq 85), sales-automation-service (seq 90), crm-selection-service (seq 54), sales-dashboard-service (seq 100), crm-consultant-for-startups (seq 122), crm-training-service (seq 123), crm-adoption-consulting (seq 124), b2b-gtm-strategy-service (seq 126), and the go-to-market pillar's money pages are still not-started; this run's what-is-crm-automation and what-is-sales-analytics posts link only to their live pillar pages since their specified money pages are not yet live. (2) link_graph.py reports the full graph clean (93 pages, 0 issues) as of the twenty-sixth run; this run's three new posts were pre-emptively linked from two sibling posts each (workflow-diagram.html + dmaic-explained.html; re-engagement-campaigns.html + sales-automation-tools.html; saas-kpis.html + defining-pipeline-stages.html) before running link_graph.py, so none were flagged as orphans this time. (3) At the start of the seventeenth run, a stale multi-ref `git fetch` briefly suggested `main` was 18 posts behind this session's branch; re-fetching confirmed `origin/main` already had all of them, so it was a false alarm, not an actual deploy gap. Always re-fetch a single ref to confirm before treating a branch-divergence reading as real.

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
