#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files in the repo.

Includes the homepage, legal pages, and every published page in blog/ and services/.
Excludes thanks.html (noindex) and any 404 page. Run on every content run after
the Builder writes new pages.

lastmod policy: each URL carries the date its file last actually changed, taken
from the newest git commit touching that file. Files new or edited in the working
tree (the pages being published in the current run) get today's date. The old
behaviour stamped every URL with the run date, which made every lastmod value
identical after every run; Google documents that it ignores lastmod when the
values are not consistently accurate, so the sitemap gave it nothing to schedule
crawls from. changefreq and priority are omitted: Google ignores both fields.
"""
import datetime
import glob
import os
import subprocess

BASE = "https://thepearsonco.com"
SITE = "site"
EXCLUDE = {"thanks.html", "404.html"}
TODAY = datetime.date.today().isoformat()


def url_for(path: str) -> str:
    path = path.replace("\\", "/")
    if path == "index.html":
        return BASE + "/"
    if path.endswith("/index.html"):
        return BASE + "/" + path[:-len("index.html")]
    return f"{BASE}/{path}"


def run_git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True, check=True).stdout


def last_commit_dates() -> dict:
    """Map repo path to the committer date (YYYY-MM-DD) of the newest commit touching it."""
    out = run_git(["log", "--format=%x01%cs", "--name-only", "--", SITE])
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith("\x01"):
            current = line[1:].strip()
        elif line.strip() and current:
            dates.setdefault(line.strip(), current)
    return dates


def working_tree_changes() -> set:
    """Paths with uncommitted changes (pages written or edited mid-run) get today's date."""
    out = run_git(["status", "--porcelain", "--", SITE])
    changed = set()
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ")[-1]
        changed.add(path)
    return changed


def lastmod_for(repo_path: str, dates: dict, changed: set) -> str:
    if repo_path in changed:
        return TODAY
    known = dates.get(repo_path)
    if known:
        return known
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(repo_path)).isoformat()
    except OSError:
        return TODAY


def main():
    files = [f.replace("\\", "/")[len(SITE) + 1:] for f in glob.glob(f"{SITE}/**/*.html", recursive=True)]
    pages = sorted({f for f in files if os.path.basename(f) not in EXCLUDE})

    try:
        dates = last_commit_dates()
        changed = working_tree_changes()
    except (subprocess.CalledProcessError, FileNotFoundError):
        dates, changed = {}, set()

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lastmods = []
    for p in pages:
        lastmod = lastmod_for(f"{SITE}/{p}", dates, changed)
        lastmods.append(lastmod)
        lines += ["  <url>",
                  f"    <loc>{url_for(p)}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  "  </url>"]
    lines.append("</urlset>")
    open("site/sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"build_sitemap: wrote site/sitemap.xml with {len(pages)} URLs, "
          f"{len(set(lastmods))} distinct lastmod dates.")


if __name__ == "__main__":
    main()
