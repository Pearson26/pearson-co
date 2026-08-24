#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files in the repo.

Includes the homepage, legal pages, and every published page in blog/ and services/.
Excludes thanks.html (noindex) and any 404 page. Run on every content run after
the Builder writes new pages.

lastmod policy: an article's lastmod is its own declared date, read from the
JSON-LD in the page itself (dateModified, falling back to datePublished), so it
matches the visible byline and the structured data Google already reads there.
That means only the articles actually published on a given day carry that day's
date. A post published in July keeps its July date even when a later run edits
it, which is what we want: each run adds inbound related-reading links to older
sibling posts, and a link addition is not a meaningful content change. To move a
post's lastmod, bump dateModified in the page's JSON-LD (and the visible byline);
the sitemap follows automatically.

The four pages with no Article JSON-LD (the homepage, the blog and services index
pages, privacy) fall back to the date of the newest git commit touching the file,
which is accurate for them: the blog index genuinely does change on a publish run.

Two earlier behaviours are gone. Every URL used to be stamped with the run date,
so all lastmod values were identical and moved forward together after every daily
run; Google ignores lastmod when the values are not consistently accurate, which
left the sitemap giving it nothing to schedule crawls from. changefreq and
priority are also dropped: Google ignores both fields.
"""
import datetime
import glob
import os
import re
import subprocess

BASE = "https://thepearsonco.com"
SITE = "site"
EXCLUDE = {"thanks.html", "404.html"}

DATE_RE = r'"{key}"\s*:\s*"(\d{{4}}-\d{{2}}-\d{{2}})'


def url_for(path: str) -> str:
    path = path.replace("\\", "/")
    if path == "index.html":
        return BASE + "/"
    if path.endswith("/index.html"):
        return BASE + "/" + path[:-len("index.html")]
    return f"{BASE}/{path}"


def declared_date(repo_path: str):
    """The page's own JSON-LD date: dateModified, else datePublished, else None."""
    try:
        html = open(repo_path, encoding="utf-8").read()
    except OSError:
        return None
    for key in ("dateModified", "datePublished"):
        m = re.search(DATE_RE.format(key=key), html)
        if m:
            return m.group(1)
    return None


def git_commit_dates() -> dict:
    """Map repo path to the committer date (YYYY-MM-DD) of the newest commit touching it."""
    try:
        out = subprocess.run(["git", "log", "--format=%x01%cs", "--name-only", "--", SITE],
                             capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith("\x01"):
            current = line[1:].strip()
        elif line.strip() and current:
            dates.setdefault(line.strip(), current)
    return dates


def lastmod_for(repo_path: str, git_dates: dict) -> str:
    declared = declared_date(repo_path)
    if declared:
        return declared
    known = git_dates.get(repo_path)
    if known:
        return known
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(repo_path)).isoformat()
    except OSError:
        return datetime.date.today().isoformat()


def main():
    files = [f.replace("\\", "/")[len(SITE) + 1:] for f in glob.glob(f"{SITE}/**/*.html", recursive=True)]
    pages = sorted({f for f in files if os.path.basename(f) not in EXCLUDE})
    git_dates = git_commit_dates()

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lastmods = []
    for p in pages:
        lastmod = lastmod_for(f"{SITE}/{p}", git_dates)
        lastmods.append(lastmod)
        lines += ["  <url>",
                  f"    <loc>{url_for(p)}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  "  </url>"]
    lines.append("</urlset>")
    open("site/sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")

    today = datetime.date.today().isoformat()
    print(f"build_sitemap: wrote site/sitemap.xml with {len(pages)} URLs, "
          f"{len(set(lastmods))} distinct lastmod dates, "
          f"{lastmods.count(today)} carrying today's date ({today}).")


if __name__ == "__main__":
    main()
