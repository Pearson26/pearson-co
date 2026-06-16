# Pillar-page writing brief (internal)

You are writing ONE pillar page for The Pearson Co. (thepearsonco.com), Lauren Pearson's
consultancy. Work in this repo. Produce a finished, high-quality HTML page and SAVE it to
`site/services/<SLUG>.html` (pillar pages live in site/services/).

## Read first
- `CLAUDE.md` (the house rules)
- `templates/article.html` (the page shell you must fill; note every `{{PLACEHOLDER}}` and the live-site design)
- `workforce/the-wordsmith.md` and `workforce/the-optimiser.md` (voice and on-page SEO)

## Who you are writing as
Lauren Pearson: a Dubai-based CRM, revenue operations and hospitality-tech consultant, writing
for founders and operators of scaling and SaaS businesses. Plain, specific, practical, warm,
commercial. You write for people, not for Google.

## What a pillar page is
This is a category-defining page and a paid-ad landing page. It must: define the topic, explain
why it matters commercially, show how Lauren approaches it, set out what working with her
involves, and end with a clear call to action. Length 2,000 to 2,400 words of genuinely useful,
specific content. No padding.

## Fill the template
Use `templates/article.html` and fill EVERY `{{placeholder}}`. Leave none. This is role = pillar:
- Title tag 50 to 60 characters, primary keyword near the front, ending ` | The Pearson Co.`
- Meta description 150 to 160 characters, primary keyword once, a reason to click
- H1 with an italic emphasis on the last phrase using `<em>`; primary keyword in the H1, the first 100 words, one H2, the title and the meta
- `{{DIRECT_ANSWER}}`: a 40 to 60 word answer to the main query, self-contained
- Body: clear H2 and H3 structure, short and long sentences mixed, real substance
- FAQ: 5 to 6 question and answer pairs specific to this topic (fills `{{FAQ_HTML}}` as `<details>` blocks)
- CTA block: `{{CTA_*}}` pointing to `/#contact`
- `{{JSONLD}}`: valid JSON-LD with Article (author Lauren Pearson, publisher The Pearson Co.), FAQPage (matching the FAQ), BreadcrumbList (Home > Services > <NAME>), and Service (serviceType, provider The Pearson Co., areaServed Worldwide). No em dashes inside the JSON.
- Breadcrumb nav: Home > Services > <NAME>
- Keep the header nav, footer, WhatsApp float, cookie banner and both scripts from the template. Asset paths stay root-relative exactly as in the template (`/styles.css`, `/blog.css`, `/logo-the-pearson-co.svg`, `/tracking-config.js`, `/script.js`).

## Internal links
Link only to OTHER pillar pages that are going live now, at `/services/<slug>.html`, where genuinely
relevant (2 to 4 links, woven into the body naturally). Do NOT link to any blog or guide pages, or
anything not in this list of live slugs:
conversion-rate-optimisation, revenue-operations, crm-implementation, fractional-sales-leadership,
growth-consulting, customer-journey-mapping, hospitality-tech-market-entry, process-mapping,
standard-operating-procedures, crm-automation, sales-dashboards, crm-consulting, crm-adoption,
sales-pipeline-management, go-to-market-strategy.

## Hard rules (a reviewer will fail the page on any of these)
- British English: optimise, organise, colour, behaviour, prioritise, specialise.
- ZERO em dashes. No "—" and no en dash used as a dash. Use commas, colons, brackets or full stops.
- Do NOT use any of these words anywhere: delve, meticulous, comprehensive, leverage, seamless, robust, tapestry, vibrant, crucial, embark, groundbreaking, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm, unlock, unleash, elevate, foster, testament, ever-evolving, fast-paced, seamlessly.
- Byline is Lauren Pearson, Founder.
- Do not invent statistics, client names, testimonials or case studies. If you use a figure, keep it general or attribute it to a named, dated source. Never fabricate.
- Middle East / hospitality angle: where relevant, use the Middle East as the angle, not a region-locked keyword.

## Before you finish
Re-read your file. Confirm: no em dashes, none of the banned words, British spelling, no
`{{placeholder}}` left, valid HTML, the JSON-LD parses. Then reply with the saved file path and a
one-line confirmation that it passed your own em-dash and banned-word check.
