#!/usr/bin/env python3
"""Send the "new article live" Slack notification for published posts.

Usage:
    python scripts/notify_slack.py                    # the slugs from the last BUILD-PLAN.md run
    python scripts/notify_slack.py <slug> [<slug> ...] # specific slugs

For each slug, reads the pillar from content-plan/plan.json and the page title
straight from the built HTML's <title> tag, then POSTs one Slack message with
one "New article live: <title> (<pillar>) <url>" line per article, matching
ROUTINE-PROMPT.md step 8 (unfurl_links and unfurl_media disabled).

Requires SLACK_WEBHOOK_URL in the environment. Posts to #build-seo-pages.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def last_run_slugs():
    path = os.path.join(ROOT, "BUILD-PLAN.md")
    with open(path) as f:
        rows = [line for line in f if line.startswith("|")]
    cols = [c.strip() for c in rows[-1].split("|")]
    return [s.strip() for s in cols[4].split(",") if s.strip()]


def page_title(slug, role):
    folder = "blog" if role == "authority" else "services"
    path = os.path.join(ROOT, "site", folder, f"{slug}.html")
    with open(path) as f:
        html = f.read()
    match = re.search(r"<title>([^<|]*)", html)
    return folder, match.group(1).strip() if match else slug


def build_message(slugs):
    with open(os.path.join(ROOT, "content-plan", "plan.json")) as f:
        plan = {r["url_slug"]: r for r in json.load(f)}
    lines = []
    for slug in slugs:
        record = plan.get(slug)
        if not record:
            print(f"warning: {slug} not in plan.json, skipping", file=sys.stderr)
            continue
        folder, title = page_title(slug, record["role"])
        url = f"https://thepearsonco.com/{folder}/{slug}.html"
        lines.append(f"New article live: {title} ({record['pillar']}) {url}")
    return "\n".join(lines)


def send(text):
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        sys.exit("SLACK_WEBHOOK_URL is not set.")
    payload = json.dumps(
        {"text": text, "unfurl_links": False, "unfurl_media": False}
    ).encode()
    req = urllib.request.Request(
        webhook, data=payload, headers={"Content-type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        print(f"Slack responded {resp.status}")


if __name__ == "__main__":
    slugs = sys.argv[1:] or last_run_slugs()
    text = build_message(slugs)
    if not text:
        sys.exit("Nothing to send.")
    print(text)
    send(text)
