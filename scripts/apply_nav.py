#!/usr/bin/env python3
"""Apply the site navigation (Services dropdown + Knowledge Hub) across all pages.

- Appends the dropdown CSS to site/styles.css and the dropdown JS to site/script.js (idempotent).
- Replaces the <nav id="site-nav"> block in every page with the new nav (root-relative, so it
  works on the homepage and every sub-page).
- Updates footer links (Services -> /services/, Insights -> Knowledge Hub).
Re-runnable. Run from repo root.
"""
import re, glob, os

NEW_NAV = '''<nav id="site-nav" aria-label="Main navigation">
        <div class="has-dropdown">
          <button type="button" class="nav-drop-toggle" aria-expanded="false" aria-controls="services-menu">Services <span class="caret" aria-hidden="true">&#9662;</span></button>
          <div class="dropdown" id="services-menu">
            <a href="/services/revenue-operations.html">Revenue operations</a>
            <a href="/services/crm-consulting.html">CRM consulting &amp; implementation</a>
            <a href="/services/process-mapping.html">Process mapping &amp; SOPs</a>
            <a href="/services/conversion-rate-optimisation.html">Conversion &amp; funnel optimisation</a>
            <a href="/services/hospitality-tech-market-entry.html">Hospitality tech &amp; market entry</a>
            <a class="dropdown-all" href="/services/">View all services &#8594;</a>
          </div>
        </div>
        <a href="/blog/">Knowledge Hub</a>
        <a href="/#about">About</a>
        <a href="/#contact" class="nav-cta">Let's talk</a>
      </nav>'''

CSS = """

/* ---- nav dropdown (Services) + Knowledge Hub ---- */
.has-dropdown{position:relative;display:flex;align-items:center}
.nav-drop-toggle{font:inherit;font-weight:600;font-size:.78rem;color:inherit;background:none;border:0;cursor:pointer;display:inline-flex;align-items:center;gap:6px;padding:0}
.nav-drop-toggle:hover{color:var(--plum)}
.nav-drop-toggle .caret{font-size:.7em;transition:transform .2s}
.has-dropdown.open .nav-drop-toggle .caret{transform:rotate(180deg)}
.dropdown{position:absolute;top:calc(100% + 16px);left:0;min-width:290px;background:var(--ivory);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);padding:10px;display:none;flex-direction:column;gap:2px;z-index:40}
.dropdown::before{content:"";position:absolute;top:-20px;left:0;right:0;height:20px}
.has-dropdown.open>.dropdown{display:flex}
.dropdown a{display:block;padding:11px 15px;border-radius:9px;font-size:.8rem;font-weight:600;color:var(--ink);white-space:nowrap}
.dropdown a:hover{background:var(--cream);color:var(--plum)}
.dropdown .dropdown-all{margin-top:6px;border-top:1px solid var(--line);border-radius:0;color:var(--plum)}
@media(hover:hover) and (min-width:921px){.has-dropdown:hover>.dropdown,.has-dropdown:focus-within>.dropdown{display:flex}}
@media(max-width:920px){
  .has-dropdown{flex-direction:column;align-items:stretch}
  .nav-drop-toggle{justify-content:space-between;padding:6px 0;font-size:.85rem}
  .dropdown{position:static;box-shadow:none;border:0;border-left:2px solid var(--line);border-radius:0;min-width:0;margin:2px 0 6px 6px;padding:0}
  .dropdown a{white-space:normal}
}
"""

JS = """

// services dropdown
document.querySelectorAll('.nav-drop-toggle').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const parent = btn.closest('.has-dropdown');
    const open = parent.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
});
document.addEventListener('click', (e) => {
  document.querySelectorAll('.has-dropdown.open').forEach((d) => {
    if (!d.contains(e.target)) {
      d.classList.remove('open');
      const t = d.querySelector('.nav-drop-toggle');
      if (t) t.setAttribute('aria-expanded', 'false');
    }
  });
});
"""

def append_once(path, marker, text):
    s = open(path, encoding="utf-8").read()
    if marker in s:
        return False
    open(path, "a", encoding="utf-8").write(text)
    return True

def main():
    print("css appended:", append_once("site/styles.css", "nav dropdown (Services)", CSS))
    print("js appended:", append_once("site/script.js", "services dropdown", JS))

    nav_re = re.compile(r'<nav id="site-nav"[^>]*>.*?</nav>', re.S)
    files = ["site/index.html", "templates/article.html"] + glob.glob("site/**/*.html", recursive=True)
    for f in sorted(set(files)):
        if not os.path.exists(f):
            continue
        s = open(f, encoding="utf-8").read()
        orig = s
        if 'id="site-nav"' in s:
            s = nav_re.sub(NEW_NAV, s)
        # footer + stray link updates
        s = s.replace('<a href="/blog/">Insights</a>', '<a href="/blog/">Knowledge Hub</a>')
        s = s.replace('<a href="/#services">Services</a>', '<a href="/services/">Services</a>')
        s = s.replace('<a href="#services">Services</a>', '<a href="/services/">Services</a><a href="/blog/">Knowledge Hub</a>')
        if s != orig:
            open(f, "w", encoding="utf-8").write(s)
            print("updated nav:", f)

if __name__ == "__main__":
    main()
