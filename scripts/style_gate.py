#!/usr/bin/env python3
"""Style gate for The Pearson Co. content engine.

Mechanical backstop behind The Humaniser and The Auditor. Scans HTML files for the
non-negotiables in CLAUDE.md: no em dashes, no banned vocabulary, British spelling.

Usage:
    python scripts/style_gate.py                 # scan blog/ and services/
    python scripts/style_gate.py blog/foo.html   # scan specific files

Exit code 0 = clean, 1 = violations found (blocks the commit).
British-spelling and banned-word checks ignore content inside <script>, <style>,
and HTML tags, so JSON-LD keys and CSS are not flagged.
"""
import sys, re, glob

BANNED = [
    # client list (hard fail)
    "delve", "meticulous", "comprehensive", "leverage", "seamless", "robust",
    # extended blocklist
    "tapestry", "vibrant", "crucial", "embark", "groundbreaking", "synergy",
    "transformative", "paramount", "multifaceted", "myriad", "cornerstone",
    "reimagine", "empower", "catalyst", "invaluable", "bustling", "nestled",
    "realm", "unlock", "unleash", "elevate", "foster", "testament",
    "ever-evolving", "fast-paced", "seamlessly",
]

# US -> British spellings to flag (word-boundary, case-insensitive)
US_SPELLINGS = [
    "optimize", "optimized", "optimizing", "optimization",
    "organize", "organized", "organizing", "organization",
    "specialize", "specialized", "specializing",
    "prioritize", "prioritized", "analyze", "analyzed", "analyzing",
    "color", "colors", "behavior", "behaviors", "favor", "favorite",
    "center", "centers", "program", "programs", "license",  # license noun vs verb is contextual; flag for review
    "fulfill", "enrollment", "modeling", "labeled", "traveled", "canceled",
]

EXEMPT_LICENSE = False  # set True if "license" verb usage is intended somewhere

def strip_non_prose(html: str) -> str:
    """Remove script/style blocks and tags so we test visible prose + attributes lightly."""
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S | re.I)
    return html

def check_file(path: str):
    issues = []
    try:
        raw = open(path, encoding="utf-8").read()
    except Exception as e:
        return [f"could not read: {e}"]

    # 1) em dashes anywhere in the file (including JSON-LD, meta)
    for ch, name in [("—", "em dash (—)"), ("–", "en dash (–)")]:
        n = raw.count(ch)
        if n:
            issues.append(f"{n} x {name}")
    # " - " used as a sentence dash (en/em substitute) in visible prose
    prose = strip_non_prose(raw)
    spaced_dash = len(re.findall(r"\S \- \S", prose))
    if spaced_dash:
        issues.append(f"{spaced_dash} x spaced hyphen used as a dash ( - ); restructure")

    text = re.sub(r"<[^>]+>", " ", prose).lower()  # visible text only

    # 2) banned vocabulary
    for w in BANNED:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", text))
        if n:
            issues.append(f"{n} x banned word '{w}'")

    # 3) US spelling
    for w in US_SPELLINGS:
        if w == "license" and EXEMPT_LICENSE:
            continue
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", text))
        if n:
            issues.append(f"{n} x US spelling '{w}'")

    # 4) curly quotes and emoji in visible text
    if "“" in text or "”" in text or "‘" in text or "’" in text:
        issues.append("curly quotes present; use straight quotes")
    return issues

def main():
    args = sys.argv[1:]
    if args:
        files = args
    else:
        files = glob.glob("blog/**/*.html", recursive=True) + glob.glob("services/**/*.html", recursive=True)
    if not files:
        print("style_gate: no files to scan.")
        return 0
    total = 0
    for f in sorted(set(files)):
        issues = check_file(f)
        if issues:
            total += len(issues)
            print(f"FAIL {f}")
            for i in issues:
                print(f"   - {i}")
        else:
            print(f"OK   {f}")
    if total:
        print(f"\nstyle_gate: {total} violation(s). Fix before commit.")
        return 1
    print("\nstyle_gate: clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
