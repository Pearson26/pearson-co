# The Pearson Co. — Content Engine Architecture

Prepared 14 June 2026. For sign-off before the 12-month plan and the worker repo are generated.
Modelled on `mortgagecompare-ae` (content-plan format) and `pet-transport` (worker structure), adapted for The Pearson Co. on Netlify.

---

## 0. What I confirmed before designing this

- **Reference 1 — `ngindubai/mortgagecompare-ae`**: client-facing HTML plan dashboard (`/content-plan/`) + per-post records carrying SEO keyword + volume + KD, a dual-layer "LLM keyword" block (the GEO layer), a 40–60 word direct-answer block, H2 outline, internal-link slugs, schema list, and a status field. 23 clusters → 249 posts, pillar pages first.
- **Reference 2 — `ngindubai/pet-transport`**: a "workforce" of worker souls chained by an orchestrator (research → write → humanise/AI-gate → SEO → link-graph → audit → build → deploy), pointer-based progression in `build_state.json`, per-run caps, docs-update-every-commit, post-deploy live-link review. Deploys via GitHub Actions on push to `main`.
- **Live site `thepearsonco.com`**: plain static HTML on Netlify. `index.html` (single page, anchor sections `#services #about #expansion #contact`) + `privacy.html` + `thanks.html`. No blog yet. Sitemap has 2 URLs. Netlify form posts to `thanks.html`. `data-track` analytics hooks via `tracking-config.js` + `script.js`.
- **Live design tokens** (from `styles.css`): `--plum:#B784A7`, `--rose:#d9b5c6`, `--cream:#f8f4ef`, `--ivory:#fffdf9`, `--ink:#2c2229`; fonts `Playfair Display` (display/headings) + `DM Sans` (body); `em{color:var(--plum)}` (the italic-last-phrase house style is already in the CSS). Components present: `.site-header/.nav-wrap`, `.button`, `.eyebrow`, `.section/.container`, `.contact` form, `footer`, `.whatsapp-float`, `.cookie-banner`.
- **Netlify account**: email/password login bounced (no error, no redirect); dashboard shows "Last used GitHub" + "Log in with a Git provider". Strong signal the account is GitHub-linked and the site is on **git-based continuous deployment**. One open item below.

### Design discrepancy to resolve (flagged)
The handoff "House style" section specifies `#7f466f` plum and Inter Tight / Inter / IBM Plex Mono. The **live website** uses `#B784A7` and Playfair Display / DM Sans. These are two different looks:
- **Agency deliverable documents** (keyword universe, ads strategy, the client-facing content-plan I'll build for Lauren to review) → `#7f466f` + Inter family. Keep as-is.
- **Blog/guide articles** (published to her site) → must match the **live site** (`#B784A7` + Playfair/DM Sans) so they look native.

Recommendation: build articles in the live-site design, the plan deliverable in the agency-document design. Confirm before build.

---

## 1. Repository and Netlify deploy design

### Repo
Create `ngindubai/pearson-co` (private), matching the pattern of the other client sites on the account (`mortgagecompare-ae`, `insurecompare-ae`). Seed it with a faithful copy of her current live site (`index.html`, `styles.css`, `script.js`, `tracking-config.js`, `privacy.html`, `thanks.html`, `sitemap.xml`, `robots.txt`, images, logo) so the repo is the single source of truth, then add the content engine on top.

```
pearson-co/
  index.html  styles.css  script.js  tracking-config.js  privacy.html  thanks.html
  robots.txt  sitemap.xml
  /assets/ (logo, images, favicon)
  /blog/            <- authority articles (guides, how-tos, templates, comparisons)
  /services/        <- money + pillar pages (the ad landing pages live here)
  /blog/index.html  <- blog hub (regenerated each run)
  /content-plan/
    content-plan.html        <- client-facing plan dashboard (noindex), Lauren reviews
    plan.md                  <- execution file the worker reads (all ~1,085 records)
    plan-rows.js             <- same records as JS for the dashboard
  /workforce/                <- the worker souls (see section 5)
  /.github/
    workflows/deploy.yml     <- Netlify deploy (see below)
    prompts/build-next.prompt.md
  build_state.json  BUILD-PLAN.md  MEMORY.md  CLAUDE.md
  scripts/ (link_graph.py, build_sitemap.py, blog_index.py, verify_state.py, style_gate.py)
```

URL scheme (matches her flat static-HTML site):
- Pillar / money pages: `/services/{slug}.html`
- Authority articles: `/blog/{slug}.html`

### Deploy — recommended: Netlify Git continuous deployment
Site already appears GitHub-linked. Point the Netlify site at `pearson-co`, branch `main`, **publish directory = repo root, no build command** (plain HTML). Every push to `main` auto-deploys in ~30–60s. The Claude routine pushes finished HTML + updated `sitemap.xml` + `/blog/index.html` in one commit to `main` (the pet-transport lesson: routine must push to `main`, not a feature branch, or deploy never fires). No FTP, no Hugo.

The internal-link graph, blog index and sitemap are regenerated **locally inside the routine** before commit (so there is no Netlify build step to maintain).

### Deploy — fallback (no touching her Netlify git settings): GitHub Actions + Netlify CLI
If her site is currently a manual/drag-drop deploy and we do not want to re-point it, mirror the pet-transport GitHub-Actions pattern: on push to `main`, run the link-graph + sitemap scripts, then `netlify deploy --prod --dir=.` using `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID` repo secrets.

```yaml
# .github/workflows/deploy.yml (fallback)
name: Deploy to Netlify
on: { push: { branches: [main] } }
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: python scripts/link_graph.py && python scripts/blog_index.py && python scripts/build_sitemap.py
      - name: Deploy
        run: npx netlify-cli deploy --prod --dir=. --site=$NETLIFY_SITE_ID --auth=$NETLIFY_AUTH_TOKEN
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

**Open infra item:** confirm which GitHub repo Lauren's Netlify site is connected to (needs a working Netlify login, via GitHub). Until then I cannot point the engine at the live deploy. Two ways forward: (a) get into Netlify via the GitHub provider button, or (b) Lauren connects the new `pearson-co` repo to her Netlify site herself (Site → Build & deploy → link repository, publish dir = root).

---

## 2. The 12-month allocation (≈1,085 posts, 3/day)

RevOps **confirmed** as a full pillar. Roles per pillar from the handoff. Within each pillar the barbell holds: a small set of pillar + money pages (high-intent commercial), a large body of authority content (informational, link-earning, links up to the money/pillar pages). Money/authority splits are indicative, to refine.

| # | Pillar | Role | Pillar pages | Money/service pages | Authority posts | Total |
|---|--------|------|:---:|:---:|:---:|:---:|
| 1 | Process Mapping & SOP Creation | money + authority | 2 | 13 | 135 | 150 |
| 2 | Customer Journey Mapping | authority | 1 | 4 | 115 | 120 |
| 3 | CRM Automation & Workflow | money + authority | 1 | 10 | 84 | 95 |
| 4 | Revenue Operations (RevOps) | money + authority | 1 | 10 | 84 | 95 |
| 5 | Sales Reporting, Dashboards & Forecasting | money + authority | 1 | 10 | 84 | 95 |
| 6 | Conversion & Funnel Optimisation | money + authority | 1 | 12 | 82 | 95 |
| 7 | Go-to-Market Strategy | money + authority | 1 | 6 | 78 | 85 |
| 8 | Hospitality Tech & ME Expansion | money | 1 | 10 | 74 | 85 |
| 9 | CRM Implementation & Selection | money | 1 | 14 | 55 | 70 |
| 10 | CRM Consulting & Selection | money | 1 | 14 | 55 | 70 |
| 11 | Fractional Sales Leadership | money | 1 | 6 | 28 | 35 |
| 12 | CRM Adoption | authority | 1 | 2 | 32 | 35 |
| 13 | Sales Pipeline Management | authority | 1 | 0 | 29 | 30 |
| 14 | Growth Consulting & Strategy | authority | 1 | 4 | 20 | 25 |
| | **Totals** | | **15** | **115** | **955** | **1,085** |

Barbell at a glance: ~130 pillar+money pages (the client-winning core) feeding ~955 authority posts. Trim 5 to land on the 1,080 buffer if preferred.

### Front-loaded sequencing (so paid can launch)
The six Google Ads campaigns each land on a pillar page (CRO, Fractional, CRM Implementation, RevOps, Growth Consulting + Customer Journey, UAE Local → CRM/Expansion). So **Month 1 builds all 15 pillar pages + the highest-intent money pages first**, prioritising the seven ad-landing pillars: Conversion & Funnel, Fractional Sales Leadership, CRM Implementation, RevOps, Growth Consulting, Customer Journey, Hospitality & Expansion. Months 2–12 fill the authority clusters, each post linking up to its now-live pillar and money pages. Paid and organic then build the same pages.

---

## 3. Per-post record schema (execution file `plan.md` / `plan-rows.js`)

Every post is one record. Combines the handoff's required fields with the richer mortgagecompare schema (the GEO/LLM layer, direct-answer, schema list).

```yaml
- seq: 17                       # pointer index 1..1085 (progression is by this, never by date)
  month: 1
  pillar: "Conversion & Funnel Optimisation"
  pillar_id: conversion-funnel
  role: pillar | money | authority
  content_type: pillar page | service page | guide | how-to | template | comparison | listicle | sector brief | definition
  is_ad_landing: true           # doubles as a Google Ads landing page
  title: "Conversion rate optimisation services for B2B SaaS"
  url_slug: conversion-rate-optimisation-services      # -> /services/{slug}.html or /blog/{slug}.html
  target_market: UK | UAE | US | global
  intent: commercial | informational | transactional
  primary_keyword: "conversion rate optimisation services"
  primary_volume: 1900
  primary_kd: 22
  secondary_keywords: ["cro agency", "conversion rate optimisation company"]
  llm_layer_keywords:           # the GEO layer - how AI engines phrase the query
    - { engine: ChatGPT,    phrasing: "best CRO service for a B2B SaaS funnel" }
    - { engine: Claude,     phrasing: "who fixes low conversion rates in a sales funnel" }
    - { engine: Perplexity, phrasing: "conversion rate optimisation consultant UK" }
  direct_answer: "A 40-60 word answer block placed near the top for snippets and AI overviews."
  h2_outline: ["Where B2B funnels leak", "What a CRO engagement covers", "How we measure lift", "FAQ"]
  word_count_target: 1500
  internal_links:
    up:      [conversion-funnel, conversion-audit]    # authority -> pillar + money (barbell)
    lateral: [customer-journey-mapping, lead-management-process]
  external_links: ["one or two authoritative sources"]
  schema_required: [Article, FAQPage, BreadcrumbList]   # + Service on money pages, HowTo on process/how-to posts
  ai_overview_play: "Lead with a definition + a 5-point checklist so it lifts cleanly into AI answers."
  status: not-started | in-progress | drafted | published
```

The client-facing `content-plan.html` renders these as an interactive 12-month calendar (filter by pillar/role/market, per-post writing-brief modal, status tracking), `noindex`, in the agency-document brand.

---

## 4. House style and quality gates (baked into the workers)

- **British English** throughout (optimise, colour, organisation).
- **No em dashes anywhere** — zero tolerance. Use commas, colons, brackets, full stops, or restructure.
- **Banned vocabulary**: the handoff list — *delve, meticulous, comprehensive, leverage, seamless, robust* — extended with the pet-transport Tier-1 list (*tapestry, vibrant, crucial, embark, groundbreaking, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm*).
- **Voice**: Lauren's — commercial growth/SaaS consultant, plain English, specific, no fluff; headings carry the italic-last-phrase emphasis (`<em>` = plum, already in her CSS).
- **Light scheme only**: `color-scheme: light only`, opaque background, as the handoff requires.
- **Quality gates** (Auditor): minimum useful length per content type; one unique angle per post; no thin duplication across a cluster (>15% body overlap rejects); internal links present (authority → pillar + money); valid schema; claims sourced; correct live-site template, nav, footer, contact CTA and tracking hooks.

---

## 5. The worker roster (adapted from pet-transport's 14 souls)

Pet-transport's souls are logistics-specific (e.g. The Geographer for country regulations). For a B2B consultancy blog the workforce is **9 roles**: a topic-research worker, the AI gate, and the five other quality workers you asked for, plus the orchestrator and the builder as infrastructure. Each is a `/workforce/**/*.md` soul file with a charter, exactly like the reference.

| Worker | Stage | Job |
|--------|-------|-----|
| **The Strategist** (orchestrator) | plan | Reads `build_state.json`, takes the next 3 records from `plan.md` by pointer, loads the workers, marks in-progress → done, updates docs, posts live links. |
| **The Researcher** (topic research) | research | Gathers real facts, figures, frameworks and 1–2 authoritative sources for the topic; pulls SERP/keyword context via the Semrush MCP. The "topic research worker". |
| **The Wordsmith** | write | Drafts the article to the brief in Lauren's voice, British English, barbell internal-link intent, content-type structure. |
| **The Humaniser** (AI gate) | gate | Strips em dashes (0 tolerance) and banned vocabulary; runs the anti-AI-pattern pass (significance inflation, rule-of-three, copula avoidance, "not just X but Y", synonym cycling, etc.); varies burstiness/sentence rhythm. The explicit "AI gate". |
| **The Optimiser** (on-page SEO + GEO) | seo | Title/meta (rotated formulas, unique), H-hierarchy, keyword placement, canonical, OG, image alt, JSON-LD (Article/FAQPage/BreadcrumbList; Service on money pages; HowTo on process/how-to posts), the GEO layer (direct-answer block + `llms.txt` + LLM-phrasing coverage). |
| **The Interrogator** (FAQ) | seo | Unique FAQPage Q&A per post, no duplication across the cluster. |
| **The Connector** (internal links) | links | Enforces the barbell: authority → pillar + money pages; pillar/money interlink; lateral within-cluster links; anchor-text variation. Runs `link_graph.py`. |
| **The Builder** (assembler) | build | Renders the standalone `.html` in the **live-site** template (Playfair/DM Sans, plum, nav, footer, contact CTA, WhatsApp float, cookie banner, tracking hooks), writes to `/blog/` or `/services/`, regenerates `/blog/index.html` + `sitemap.xml`. |
| **The Auditor** (QA gate) | gate | Final pass: house-style scan (em-dash = 0, banned-word = 0, British spelling), length, uniqueness, schema validity, links present, sourcing, design integrity. APPROVED / REVISE. |

Run flow per routine: Strategist picks 3 → for each post: Researcher → Wordsmith → Humaniser → Optimiser + Interrogator → Connector → Builder → Auditor (reject loops back) → commit all 3 + sitemap + blog index in one push to `main` → Netlify deploys → post the 3 live URLs for review.

A light **Watchdog** check (post-deploy: 200s, no broken links, schema parses) runs after the push, mirroring pet-transport's live-link review gate.

---

## 6. Scheduling and progression

- **Pointer-based**, never date-based. `build_state.json`: `{ next_index, posts_published, last_published_slug, last_updated, notes }`. `verify_state.py` reconciles the count from disk (never hand-edited), as in pet-transport.
- **Per-run cap: 3 posts**, inside the **15-routine daily cap**. The plan totals ~1,085, so steady state is one 3-post run per day (~365 days). Month 1 can use a few extra daily runs to front-load the 15 pillar pages + priority money pages before paid launches.
- **Docs update every commit**: `BUILD-PLAN.md` session log + `build_state.json` + `MEMORY.md`, bundled with the content — the pet-transport anti-drift rule.
- The cloud Claude routine (the account Lauren will create) runs the Strategist entrypoint prompt on schedule and pushes to `main`.

---

## 7. Open items to confirm before I build

1. **Article design** — confirm articles use the **live-site** look (`#B784A7`, Playfair/DM Sans) while the plan deliverable keeps the agency-document look (`#7f466f`, Inter). (My recommendation.)
2. **Repo + deploy** — OK to create `ngindubai/pearson-co`, seed it with a copy of her live site, and use **Netlify Git continuous deployment** (push to `main` → auto-deploy)? And can we get a working Netlify login (via GitHub) to confirm/point the connected repo, or will Lauren connect the repo her side?
3. **Allocation table** — sign off the per-pillar money/authority weighting in section 2 (or adjust), and whether to trim to exactly 1,080.
4. **Schema enrichment** — confirm you want the GEO/LLM-layer + direct-answer + schema fields carried per post (richer than the handoff's minimum, matching mortgagecompare).

Once these are locked, I generate: the full `plan.md` (all ~1,085 records) + `plan-rows.js`, the client-facing `content-plan.html`, the nine `/workforce` soul files, the orchestrator prompt, the scripts, `build_state.json`/`BUILD-PLAN.md`/`MEMORY.md`/`CLAUDE.md`, and the deploy workflow — then we wire the routine.
