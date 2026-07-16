# Memory — The Pearson Co. content engine

Durable facts and current state. Update the Current State block in every content commit.

## Current state
- Phase 1 (scaffold) complete. Repo seeded with the live site; engine in place.
- Phase 2 (the 12-month plan) COMPLETE: 1085 records across 14 pillars (15 pillar pages, 115 money, 955 authority) in `content-plan/plan.json`, rendered to `plan.md` + `plan-rows.js`, reviewable in `content-plan/content-plan.html`. Sequenced for publishing via `scripts/sequence_plan.py` (pillars + money front-loaded, authority round-robin; ~91/month).
- Volumes are live Semrush for batches 1-5 (Conversion, RevOps, CRM Implementation, Fractional+Growth, CJM part 1) and indicative (universe doc + domain knowledge) from batch 6 on. Refresh with Semrush when units are available, then re-run `render_plan.py`.
- 99 posts published: the 15 cornerstone pillar pages (seq 1-15), seq 16-39 (money pages across CRO, CRM, fractional, growth, market entry, ecommerce, RevOps pillars in site/services/), plus 60 authority posts in site/blog/: seq 145, 201, 355 published 2026-06-27; seq 356-358 published 2026-06-28; seq 359-361 published 2026-06-29; seq 362-364 and seq 365-367 published 2026-07-01; seq 368-370 published 2026-07-02; seq 371-373 published 2026-07-03; seq 374-376 published 2026-07-04; seq 377-379 published 2026-07-05; seq 380-382 published 2026-07-06; seq 383-385 published 2026-07-07; seq 386-388 published 2026-07-08; seq 389-391 published 2026-07-09; seq 392-394 published 2026-07-10; seq 395-397 published 2026-07-11; seq 398-400 published 2026-07-12; seq 401-403 published 2026-07-13; seq 404-406 published 2026-07-14; seq 407-409 published 2026-07-15; seq 410 (what-is-positioning), seq 411 (ecommerce-conversion-rate-benchmarks), seq 412 (revops-strategy-guide) published 2026-07-16. `next_index` = 413, routine resumes at seq 413.
- Netlify git continuous deployment is connected (push to main -> deploy). GA4 (G-3XWNSR5VHF) is live and consent-gated. Sitemap: https://thepearsonco.com/sitemap.xml (103 URLs, submit in GSC).
- The publishing routine (Strategist + 8 souls) is running: 3 posts/run, pointer-based from `build_state.json`. Each new post's publish date is set to the actual run date, not a fixed date; confirmed again this run (16 July 2026 on all three new posts, both in the visible byline and the JSON-LD datePublished/dateModified). This has now been correct on every new post across fourteen consecutive runs (2-16 July). The June-16 date the client keeps flagging belongs only to 21 older published pages (front-loaded pillar/money pages and early authority posts from the 16-26 June period) that still carry a hardcoded "16 June 2026" (or other June) byline date predating this rule; this remains out of scope for this 3-post authority-only routine, which cannot fix it within its normal scope, and stays flagged as a standalone bulk backdate-correction job for the client to schedule separately (raised repeatedly now).
- Slack live-link format changed this run: a single message containing multiple `[title](url)` markdown links (the previously "confirmed" format) was still bleeding a link into the following word in practice. **Fixed by sending each article as its own separate `slack_send_message` call**, with the raw URL as the very last character of that message and nothing after it, so there is no adjacent text for the link to merge with. Use one Slack message per article URL for every future notification; do not combine multiple links into a single multi-line message again.
- Watch items: (1) positioning-and-messaging-service (money page referenced by seq 410's up-link spec, not yet live), plus the standing backlog: salesforce-consultant (seq 407's target), crm-adoption-consulting (seq 408's target), customer-journey-mapping-service (seq 65), crm-automation-service (seq 96), sales-analytics-consulting (seq 104), uae-market-entry-service (seq 68), process-mapping-service (seq 85), sales-automation-service (seq 90), crm-selection-service (seq 54), sales-dashboard-service (seq 100), crm-consultant-for-startups (seq 122), crm-training-service (seq 123), b2b-gtm-strategy-service (seq 126), and the go-to-market pillar's remaining money pages are still not-started; this run's three posts link only to their live pillar/money pages since some specified target pages are not yet live. (2) link_graph.py reports the full graph clean (99 pages, 0 issues) as of this run; this run's three new posts were initially flagged as orphans, then fixed by adding an inbound Related-reading link from two sibling posts each (product-launch-strategy.html + sales-playbook.html; what-is-a-good-conversion-rate.html + how-to-calculate-conversion-rate.html; revops-framework.html + cac-and-ltv.html) before the graph reported clean. (3) At the start of the seventeenth run, a stale multi-ref `git fetch` briefly suggested `main` was 18 posts behind this session's branch; re-fetching confirmed `origin/main` already had all of them, so it was a false alarm, not an actual deploy gap. Always re-fetch a single ref to confirm before treating a branch-divergence reading as real.

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
