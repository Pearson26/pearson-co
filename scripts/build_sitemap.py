#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files in the repo.

Includes the homepage, legal pages, and every published page in blog/ and services/.
Excludes templates/, content-plan/ (noindex review tooling), thanks.html (noindex),
and any 404 page. Run on every content run after the Builder writes new pages.

lastmod is stable: a page keeps the date it first entered the sitemap and only new
pages get today's date. Stamping every page with today on every run makes lastmod
untrustworthy, and Google discounts unreliable lastmod values, which hurts crawl
scheduling. Carrying the dates forward from the existing sitemap keeps the signal
honest and works under shallow CI clones (no git history needed).
"""
import os, glob, re, datetime

BASE = "https://thepearsonco.com"
TODAY = datetime.date.today().isoformat()
EXCLUDE = {"thanks.html", "404.html"}
EXCLUDE_DIRS = ("templates/", "content-plan/", "scripts/", "workforce/", ".github/")
SITEMAP_PATH = "site/sitemap.xml"

def existing_lastmods() -> dict:
    """Map of loc -> lastmod from the current sitemap, so unchanged pages keep their date."""
    try:
        xml = open(SITEMAP_PATH, encoding="utf-8").read()
    except FileNotFoundError:
        return {}
    pairs = {}
    for block in re.findall(r"<url>(.*?)</url>", xml, re.DOTALL):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        mod = re.search(r"<lastmod>(.*?)</lastmod>", block)
        if loc and mod:
            pairs[loc.group(1).strip()] = mod.group(1).strip()
    return pairs

def url_for(path: str) -> str:
    path = path.replace("\\", "/")
    if path == "index.html":
        return BASE + "/"
    if path.endswith("/index.html"):
        return BASE + "/" + path[:-len("index.html")]
    return f"{BASE}/{path}"

def priority(path: str) -> str:
    if path == "index.html":
        return "1.0"
    if path.startswith("services/"):
        return "0.8"
    if path.startswith("blog/") and path.endswith("index.html"):
        return "0.6"
    if path.startswith("blog/"):
        return "0.6"
    if path == "privacy.html":
        return "0.2"
    return "0.5"

def main():
    SITE = "site"
    files = [f.replace("\\", "/")[len(SITE) + 1:] for f in glob.glob(f"{SITE}/**/*.html", recursive=True)]
    pages = sorted({f for f in files if os.path.basename(f) not in EXCLUDE})
    known = existing_lastmods()

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    new_count = 0
    for p in pages:
        url = url_for(p)
        lastmod = known.get(url, TODAY)
        if url not in known:
            new_count += 1
        cf = "weekly" if p == "index.html" else ("monthly" if p.startswith(("blog/", "services/")) else "yearly")
        lines += ["  <url>",
                  f"    <loc>{url}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  f"    <changefreq>{cf}</changefreq>",
                  f"    <priority>{priority(p)}</priority>",
                  "  </url>"]
    lines.append("</urlset>")
    open(SITEMAP_PATH, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"build_sitemap: wrote {SITEMAP_PATH} with {len(pages)} URLs ({new_count} new, {len(pages) - new_count} carried forward).")

if __name__ == "__main__":
    main()
