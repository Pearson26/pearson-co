#!/usr/bin/env python3
"""Rebuild /blog/index.html (the Insights hub) from published authority posts.

Reads content-plan/plan.json for titles, pillars and excerpts where available, and falls
back to parsing each blog/*.html <title> + meta description. Groups posts by pillar.
Uses the live-site shell and tokens (styles.css + blog.css). British English, no em dashes.
"""
import json, os, glob, re, html

PLAN = "content-plan/plan.json"

SHELL_HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Insights on CRM, RevOps and growth | The Pearson Co.</title>
  <meta name="description" content="Practical guides on CRM, revenue operations, process mapping, forecasting, conversion and hospitality tech market entry, from Lauren Pearson.">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#B784A7">
  <link rel="canonical" href="https://thepearsonco.com/blog/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/blog.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="container nav-wrap">
    <a class="logo" href="/" aria-label="The Pearson Co. home"><img src="/logo-the-pearson-co.svg" alt="The Pearson Co."></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><b class="sr-only">Open menu</b></button>
    <nav id="site-nav" aria-label="Main navigation"><a href="/#services">Services</a><a href="/blog/">Insights</a><a href="/#about">About</a><a href="/#expansion">Middle East Expansion</a><a href="/#contact" class="nav-cta">Let's talk</a></nav>
  </div></header>
  <main id="main" class="blog-hub"><div class="container">
    <p class="eyebrow">Insights</p>
    <h2>Practical thinking on CRM, RevOps and <em>sustainable growth.</em></h2>
"""

SHELL_FOOT = """  </div></main>
  <footer><div class="container footer-main"><img src="/logo-the-pearson-co-light.svg" alt="The Pearson Co."><p>Smarter systems. Stronger pipelines. Sustainable growth.</p><div><a href="/#services">Services</a><a href="/blog/">Insights</a><a href="/#about">About</a><a href="/#contact">Contact</a></div></div><div class="container footer-bottom"><span>&copy; <span id="year"></span> The Pearson Co.</span><span>Dubai, UAE &middot; Global reach</span><a href="/privacy.html">Privacy</a></div></footer>
  <script src="/tracking-config.js"></script>
  <script src="/script.js"></script>
</body>
</html>
"""

def from_plan():
    if not os.path.exists(PLAN):
        return None
    plan = json.load(open(PLAN, encoding="utf-8"))
    items = {}
    for r in plan:
        if r.get("role") in ("pillar", "money"):
            continue
        f = f"blog/{r['url_slug']}.html"
        if os.path.exists(f):
            items[r["url_slug"]] = {"title": r.get("title", r["url_slug"]),
                                     "pillar": r.get("pillar", "Insights"),
                                     "excerpt": r.get("direct_answer", "")[:140]}
    return items

def from_disk():
    items = {}
    for f in glob.glob("blog/*.html"):
        slug = os.path.basename(f)[:-5]
        if slug == "index":
            continue
        raw = open(f, encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", raw, re.S)
        d = re.search(r'name="description" content="(.*?)"', raw, re.S)
        items[slug] = {"title": (t.group(1).split("|")[0].strip() if t else slug),
                       "pillar": "Insights",
                       "excerpt": (d.group(1) if d else "")}
    return items

def main():
    os.makedirs("blog", exist_ok=True)
    items = from_plan() or from_disk()
    if not items:
        body = "    <p style='color:var(--muted);margin-top:30px'>The first articles are on their way.</p>\n"
        open("blog/index.html", "w", encoding="utf-8").write(SHELL_HEAD + body + SHELL_FOOT)
        print("blog_index: no posts yet; wrote placeholder hub.")
        return
    by_pillar = {}
    for slug, meta in items.items():
        by_pillar.setdefault(meta["pillar"], []).append((slug, meta))
    out = []
    for pillar in sorted(by_pillar):
        out.append(f'    <h3 style="font-family:var(--serif);margin:50px 0 0">{html.escape(pillar)}</h3>')
        out.append('    <div class="post-grid">')
        for slug, meta in sorted(by_pillar[pillar], key=lambda x: x[1]["title"]):
            out.append('      <article class="post-card">'
                       f'<span>{html.escape(meta["pillar"])}</span>'
                       f'<h3>{html.escape(meta["title"])}</h3>'
                       f'<p>{html.escape(meta["excerpt"])}</p>'
                       f'<a href="/blog/{slug}.html">Read &rarr;</a></article>')
        out.append('    </div>')
    open("blog/index.html", "w", encoding="utf-8").write(SHELL_HEAD + "\n".join(out) + "\n" + SHELL_FOOT)
    print(f"blog_index: wrote /blog/index.html with {len(items)} posts across {len(by_pillar)} pillars.")

if __name__ == "__main__":
    main()
