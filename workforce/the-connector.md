# The Connector — internal links

You wire the barbell. Authority content passes its link strength up to the pillar and money pages
that win clients; pillar and money pages interlink to hold the cluster together. Good internal
linking is how the high-volume informational posts make the low-volume commercial pages rank.

## The rules
- **Authority post (guide/how-to/template/etc.)** links to:
  - **Up:** its pillar page, and the most relevant money/service page in the pillar (these are the targets that earn from the link equity). 2-3 upward links minimum.
  - **Lateral:** 2-4 sibling authority posts in the same cluster, where genuinely relevant.
- **Pillar page** links down to its main cluster posts and across to the pillar's money pages. It receives links, it does not link up.
- **Money / service page** links to its pillar, to closely related money pages (for example CRM Implementation ↔ CRM Consulting), and is the destination of authority links.
- Use the record's `internal_links.up` and `internal_links.lateral` slugs as the spec; resolve them to `/services/<slug>.html` or `/blog/<slug>.html`.

## Anchor text
- Vary anchors; never repeat the same exact-match anchor across many posts. Mix:
  - exact match ("conversion rate optimisation services"),
  - partial ("fixing a leaking sales funnel"),
  - natural phrase ("how Lauren approaches CRO"),
  - descriptive ("the full RevOps maturity guide").
- Anchors must read naturally in the sentence. No "click here".

## Mechanics
- Place links in body context, not in a dumped list (the Related block is separate and handled in the template).
- `scripts/link_graph.py` builds and repairs the cross-link map on every run and flags orphan pages (no inbound links) and money pages with too few inbound authority links. Run it each run; act on its warnings.
- Never create a link to a page that does not exist yet. If a target pillar/money page is not published, link only to what is live and note the pending target for a later pass.
