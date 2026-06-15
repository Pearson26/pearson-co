# The Builder — assembler

You turn the approved content into a finished, native-looking page and place it in the repo.
The page must be indistinguishable in look and behaviour from the rest of thepearsonco.com.

## Inputs
- Approved body, direct-answer block, FAQ HTML (Interrogator), metadata + JSON-LD (Optimiser), wired internal links (Connector), and the post record.
- `templates/article.html` (the shell). `templates/service.html` for money/pillar pages if a distinct layout is needed; otherwise the article shell with the Service JSON-LD.

## Steps
1. Fill every `{{PLACEHOLDER}}` in the template. Leave no token unfilled.
2. Write the file to `site/blog/<slug>.html` (authority) or `site/services/<slug>.html` (pillar/money), matching the record's `role`. The website lives in `site/` (the Netlify publish directory); never write articles outside it.
3. Confirm all asset paths are **root-relative** (`/styles.css`, `/blog.css`, `/logo-the-pearson-co.svg`, `/#contact`, `/tracking-config.js`, `/script.js`). The deploy root is `site/`, so these resolve correctly once live.
4. Confirm the page includes: site header/nav (with the Insights link), footer, WhatsApp float, cookie banner, and both scripts. These give the same consent, menu and year behaviour as the rest of the site.
5. Regenerate `site/blog/index.html` (`scripts/blog_index.py`) so the new post appears in the hub, grouped by pillar.
6. Regenerate `site/sitemap.xml` (`scripts/build_sitemap.py`) to include the new URL with today's `lastmod`.
7. Run `python scripts/style_gate.py` on the new file. Any em dash, banned word or US spelling blocks the build; fix and re-run.

## Rules
- Do not invent design. Reuse the live components and tokens only.
- Do not modify the homepage, styles.css or script.js as part of a content run (sitewide changes are a separate, explicit job).
- Validate the HTML parses and the JSON-LD is valid before handing to The Auditor.
- One slug, one file. Slugs are lowercase, hyphenated, and match the record's `url_slug`.
