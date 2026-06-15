# The Pearson Co. — Content Engine (CLAUDE.md)

This repo is the source of truth for thepearsonco.com and its automated content engine.
It hosts Lauren Pearson's static website plus a programmatic-SEO workforce that publishes
3 high-quality blog/guide articles per scheduled run, built to rank for her clients' search terms.

Read this file at the start of every session. It is the single source of truth for rules.
Modelled on the patterns in `mortgagecompare-ae` (content plan) and `pet-transport` (worker structure).

---

## 1. What this is

- **Client:** The Pearson Co. (thepearsonco.com). Lauren Pearson, Dubai-based CRM / RevOps / hospitality-tech-expansion consultant.
- **Strategy:** a barbell. A small set of money pages on low-volume, high-intent commercial terms that win clients, fed by a larger body of authority content on high-volume informational terms that earns links and passes internal-link strength to the money pages. Pillar-and-cluster, not standalone posts. Quality over thinness.
- **Scale:** ~1,085 posts across 12 months, 3 per run, 14 pillars (RevOps confirmed).
- **The plan lives in** `content-plan/plan.md` (the execution queue the workforce reads) and `content-plan/content-plan.html` (the client-facing review dashboard).

## 2. Tech stack (locked)

- Plain **static HTML**, no build step. Same stack as the live site.
- **GitHub** repo `Pearson26/pearson-co` is the source of truth. The client's Claude account pushes to `main` via its GitHub connection (authorised as `Pearson26`); our build access is `ngindubai` as a write collaborator.
- **Netlify** hosts the site via **git continuous deployment** from this repo: branch `main`, **publish directory `site/`**, no build command. Every push to `main` auto-deploys in ~30-60s.
- The **website lives in `site/`**; the **engine** (workforce, scripts, content-plan, templates, docs) stays at the **repo root and is never deployed**.
- Articles are standalone `.html` files written into `site/blog/` (authority) and `site/services/` (pillar + money pages).

## 3. House style (non-negotiable, enforced by The Humaniser and The Auditor)

- **British English** throughout: optimise, organise, colour, behaviour, programme, centre, licence (noun) / license (verb), specialise, prioritise.
- **No em dashes anywhere. Zero tolerance.** Use commas, colons, brackets, full stops, or restructure. This applies to article body, titles, meta, JSON-LD, alt text, commit messages and docs.
- **Banned vocabulary** (client list, hard fail): delve, meticulous, comprehensive, leverage, seamless, robust.
  Extended blocklist (also fail): tapestry, vibrant, crucial, embark, groundbreaking, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm, unlock, unleash, elevate, navigate (figurative), landscape (figurative), testament, seamlessly, foster, dive in, in today's world, ever-evolving, fast-paced.
- **No AI tells:** no "it's not just X, it's Y", no rule-of-three padding, no "in conclusion", no significance inflation ("plays a pivotal role"), no copula avoidance ("serves as", "boasts"), no synonym cycling, no hedging stacks ("could potentially possibly"), no emoji in body, straight quotes only.
- **Voice:** Lauren Pearson's. Commercial growth and SaaS/CRM consultant. Plain, specific, practical, warm but not soft. Writes for founders and operators, not for Google. Uses contractions. Concrete deliverable and category names, never abstract consultancy phrasing (process maps and SOPs, not "process excellence"). Cites real figures and named sources where used.
- **Headings** carry an italic emphasis on the last phrase, using `<em>` (already styled plum in the CSS). Example: `Stronger pipelines. <em>Sustainable growth.</em>`
- **Light scheme only.** Never introduce dark-mode CSS. Background stays the site's ivory/white.

## 4. Design: articles must look native to the live site

Use the live site's system, NOT the agency-document look (`#7f466f` + Inter is for review documents only).

- Tokens (from `styles.css` `:root`): `--plum:#B784A7`, `--rose:#d9b5c6`, `--blush:#ead9d7`, `--cream:#f8f4ef`, `--ivory:#fffdf9`, `--ink:#2c2229`, `--muted:#746970`.
- Fonts: **Playfair Display** (h1/h2, display) + **DM Sans** (body). Already loaded via Google Fonts link.
- Every article uses `templates/article.html` as its shell: the site header/nav, footer, WhatsApp float, cookie banner, and loads `tracking-config.js` + `script.js`. Article-specific components are in `blog.css`.
- **Asset paths are root-relative** (`/styles.css`, `/blog.css`, `/logo-the-pearson-co.svg`, `/#contact`). The deploy root is `site/`, so `/styles.css` resolves to `site/styles.css`. Articles sit one level deep in `site/blog/` and `site/services/`.
- Byline author is **Lauren Pearson, Founder, The Pearson Co.** (never "Gareth", never a fake persona).
- Every article ends with a CTA block linking to the home contact section (`/#contact`) and, where relevant, the matching service/pillar page.

## 5. The workforce (`/workforce/*.md`)

Nine worker souls, chained per run by The Strategist. Each soul file is the worker's full charter.

1. **The Strategist** — orchestrator. Reads `build_state.json`, takes the next 3 records from `content-plan/plan.md` by pointer, runs the workers per post, marks progress, updates docs, posts live links.
2. **The Researcher** — topic research. Real facts, figures, frameworks, 1–2 authoritative sources; SERP/keyword context via the Semrush MCP.
3. **The Wordsmith** — writes the draft to the brief in Lauren's voice, British English, with barbell internal-link intent.
4. **The Humaniser** — the AI gate. Removes em dashes (0), banned vocabulary, AI patterns; tunes sentence rhythm.
5. **The Optimiser** — on-page SEO + GEO: title/meta, H-hierarchy, canonical, OG, image alt, JSON-LD, the direct-answer block and LLM-phrasing coverage.
6. **The Interrogator** — unique FAQPage Q&A per post.
7. **The Connector** — barbell internal links: authority → pillar + money; pillar/money interlink; lateral within cluster; varied anchors.
8. **The Builder** — renders the standalone `.html` from `templates/article.html`, writes to `site/blog/` or `site/services/`, regenerates `site/blog/index.html` and `site/sitemap.xml`.
9. **The Auditor** — final QA gate: style scan (em-dash=0, banned=0, British spelling), length, uniqueness, schema validity, links present, sourcing, design integrity. APPROVED / REVISE.

**Run flow:** Strategist picks 3 → for each: Researcher → Wordsmith → Humaniser → Optimiser + Interrogator → Connector → Builder → Auditor (reject loops back to Wordsmith/Humaniser) → commit all 3 + sitemap + blog index in one push to `main` → post the 3 URLs for review.

## 6. Progression and caps (pointer-based, never date-based)

- `build_state.json` holds `next_index` (the next unpublished `seq` in `plan.md`), `posts_published`, `last_published_slug`, `last_updated`, `notes`.
- **Per run: 3 posts.** Inside the platform's 15-routine daily cap. Steady state is one 3-post run per day.
- Advance `next_index` by the number actually published, in the same commit.
- `python scripts/verify_state.py --write` reconciles counts from disk. Never hand-edit the counts.

## 7. Mandatory docs update (every commit)

Every commit that adds or changes pages bundles:
1. the content files,
2. `BUILD-PLAN.md` (a session-log row: date, posts done, slugs, what's next),
3. `build_state.json` (via `verify_state.py --write`),
4. `MEMORY.md` ("Current State" block).
This prevents drift between docs and reality.

## 8. Quality gates (The Auditor rejects on any failure)

- Minimum useful length per content type (see The Auditor soul).
- One unique angle per post; no thin duplication across a cluster (>15% body overlap rejects).
- Internal links present and correct (authority → its pillar + money pages).
- Valid JSON-LD (Article + FAQPage + BreadcrumbList; Service on money pages; HowTo on process/how-to posts).
- Claims sourced; figures plausible and dated.
- Correct template, nav, footer, contact CTA, tracking includes, root-relative paths.
- Style scan passes (run `python scripts/style_gate.py <file>`): 0 em dashes, 0 banned words, British spelling.

## 9. Directory map

```
/ (repo root - engine + docs, NOT deployed)
  /site/        <- Netlify publish directory (the live website only)
    index.html privacy.html thanks.html styles.css script.js tracking-config.js
    favicon.svg site.webmanifest robots.txt sitemap.xml llms.txt logo-*.svg lauren-pearson-lilac-final.png
    blog.css                       <- article components (uses live CSS vars)
    /blog/        index.html + authority articles
    /services/    pillar + money pages (ad landing pages)
  /templates/   article.html (the shell)
  /workforce/   the 9 soul files
  /content-plan/ plan.json (canonical), plan.md, plan-rows.js, content-plan.html, plan-build-state.json, batches/
  /scripts/     style_gate.py, build_sitemap.py, blog_index.py, link_graph.py, verify_state.py, render_plan.py, sequence_plan.py
  /.github/     prompts/build-next.prompt.md, workflows/deploy.yml
  CLAUDE.md BUILD-PLAN.md MEMORY.md build_state.json ARCHITECTURE.md README.md
```

## 10. Permanent facts

- Push to `main`. The deploy (once connected) only fires on `main`, never on feature branches.
- Articles match the live site, not the agency documents.
- No em dashes, ever. British English, always.
- The plan is the queue; progression is by pointer, not date.
- Do not enable tracking IDs or wire Netlify without an explicit instruction.
