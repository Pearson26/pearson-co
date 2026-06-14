#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files in the repo.

Includes the homepage, legal pages, and every published page in blog/ and services/.
Excludes templates/, content-plan/ (noindex review tooling), thanks.html (noindex),
and any 404 page. Run on every content run after the Builder writes new pages.
"""
import os, glob, datetime

BASE = "https://thepearsonco.com"
TODAY = datetime.date.today().isoformat()
EXCLUDE = {"thanks.html", "404.html"}
EXCLUDE_DIRS = ("templates/", "content-plan/", "scripts/", "workforce/", ".github/")

def url_for(path: str) -> str:
    path = path.replace("\\", "/")
    if path == "index.html":
        return BASE + "/"
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
    files = [f.replace("\\", "/") for f in glob.glob("**/*.html", recursive=True)]
    pages = []
    for f in files:
        if any(f.startswith(d) for d in EXCLUDE_DIRS):
            continue
        if os.path.basename(f) in EXCLUDE:
            continue
        pages.append(f)
    pages = sorted(set(pages))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        cf = "weekly" if p == "index.html" else ("monthly" if p.startswith(("blog/", "services/")) else "yearly")
        lines += ["  <url>",
                  f"    <loc>{url_for(p)}</loc>",
                  f"    <lastmod>{TODAY}</lastmod>",
                  f"    <changefreq>{cf}</changefreq>",
                  f"    <priority>{priority(p)}</priority>",
                  "  </url>"]
    lines.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"build_sitemap: wrote sitemap.xml with {len(pages)} URLs.")

if __name__ == "__main__":
    main()
