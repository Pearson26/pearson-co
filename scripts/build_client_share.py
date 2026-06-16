#!/usr/bin/env python3
"""Generate the client-facing overview to share with Lauren.

Reads content-plan/plan.json and writes content-plan/client-overview.html: a self-contained,
shareable page (agency brand) that explains the editorial process each article goes through
and shows the full 12-month schedule. Deliberately excludes the engine internals: no keyword
volumes, KD, LLM-layer, money/authority labels, tooling or automation. Run from repo root.
"""
import json, html
from collections import Counter, OrderedDict

PLAN = "content-plan/plan.json"

PILLAR_BLURB = {
    "conversion-funnel": "Turning existing website traffic into more enquiries.",
    "revops": "Connecting CRM, sales process, pipeline and reporting into one revenue system.",
    "crm-implementation": "Choosing, setting up and rolling out a CRM the team actually uses.",
    "fractional-leadership": "Senior sales and revenue leadership, part-time, for scaling teams.",
    "growth-consulting": "Finding and removing the constraints holding back revenue.",
    "customer-journey": "Mapping the full customer experience to find where it leaks.",
    "hospitality-expansion": "Hospitality technology firms entering and growing across the Middle East.",
    "process-sop": "Documenting how the business runs, as process maps and SOPs.",
    "crm-automation": "Making the CRM do the work, so the team sells instead of admins.",
    "reporting-forecasting": "Dashboards and forecasts leadership can actually trust.",
    "crm-consulting": "Choosing the right CRM and getting real value from it.",
    "crm-adoption": "Getting teams to genuinely use the CRM, day to day.",
    "sales-pipeline": "Tracking and moving deals from first contact to close.",
    "go-to-market": "Taking a product or service to a new market and winning customers.",
}
TYPE_LABEL = {
    "pillar": "Cornerstone page", "money": "Service page", "guide": "Guide",
    "how-to": "How-to guide", "comparison": "Comparison", "definition": "Explainer",
    "listicle": "Guide", "template": "Template", "benchmark": "Benchmarks",
}

STEPS = [
    ("Search and topic research",
     "Every article starts from what your buyers actually search for, checked against live search data, plus the way people now ask the same questions of AI assistants like ChatGPT and Gemini. We only write things there is real demand for."),
    ("Researched first draft",
     "Each piece is written from real facts, figures and proven frameworks, in your voice, for founders and operators. Where a statistic is used, it is from a named, dated source. Nothing is invented."),
    ("Voice and clarity edit",
     "The draft is edited into clear British English: plain, specific and practical. We strip out filler, clichés and generic phrasing, and never use em dashes, so it reads like you wrote it."),
    ("Search and AI-answer optimisation",
     "The article is structured to rank in Google and to be quoted by AI search engines: a clear direct answer near the top, a sensible heading structure, and the technical mark-up search engines and assistants look for."),
    ("Internal linking",
     "Each new article is woven into the rest of the site so it points readers, and search authority, towards your core service pages. The body of content lifts the pages that win clients."),
    ("Quality review",
     "Before anything publishes, a final review checks accuracy, sources, originality, a genuine and useful angle, and that it meets length and quality standards. If it does not pass, it does not go live."),
    ("Publishing and your Slack alert",
     "Approved articles publish straight to your website. You get a Slack message for every article that goes live, with the title and a link, so you always know what is being added."),
]

def main():
    plan = sorted(json.load(open(PLAN, encoding="utf-8")), key=lambda r: r.get("seq") or 0)
    # trimmed, shareable rows only
    rows = [{"m": r.get("month", 1), "p": r.get("pillar", ""),
             "t": r.get("title", ""), "ty": TYPE_LABEL.get(r.get("content_type"), "Guide")}
            for r in plan]
    # pillar summary in plan (priority) order
    pillar_counts = OrderedDict()
    for r in plan:
        pillar_counts.setdefault(r["pillar"], {"id": r["pillar_id"], "n": 0})
        pillar_counts[r["pillar"]]["n"] += 1
    total = len(plan)

    steps_html = "\n".join(
        f'<div class="step"><div class="snum">{i+1}</div><div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div></div>'
        for i, (t, d) in enumerate(STEPS))
    summary_html = "\n".join(
        f'<tr><td class="kw">{html.escape(name)}</td><td class="muted">{html.escape(PILLAR_BLURB.get(v["id"],""))}</td><td class="num">{v["n"]}</td></tr>'
        for name, v in pillar_counts.items())
    data_json = json.dumps(rows, ensure_ascii=False)

    page = TEMPLATE.replace("{{TOTAL}}", str(total)).replace("{{STEPS}}", steps_html)
    page = page.replace("{{SUMMARY}}", summary_html).replace("{{DATA}}", data_json)
    open("content-plan/client-overview.html", "w", encoding="utf-8").write(page)
    print(f"build_client_share: wrote content-plan/client-overview.html ({total} scheduled articles).")

TEMPLATE = r"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light only">
<title>The Pearson Co. | Your Content Programme</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,400;0,500;0,600;1,500&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{color-scheme:light only;--plum:#7f466f;--plum-deep:#4a2840;--ink:#2b2430;--muted:#786b75;--hair:#e6dbe3;--cream:#faf5f8}
  html{background:#fff}*{box-sizing:border-box}
  body{margin:0;background:#fff;color:var(--ink);font-family:"Inter",system-ui,sans-serif;font-size:16px;line-height:1.6}
  .wrap{max-width:1000px;margin:0 auto;padding:0 24px;background:#fff;min-height:100vh}
  h1,h2,h3{font-family:"Inter Tight",system-ui,sans-serif;font-weight:500;letter-spacing:-.02em;color:var(--plum-deep);line-height:1.1}
  em{font-style:italic;color:var(--plum)}
  .eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--plum);font-weight:500}
  .muted{color:var(--muted)}
  header{padding:72px 0 38px;border-bottom:1px solid var(--hair)}
  header h1{font-size:clamp(2.2rem,5.5vw,3.4rem);margin:16px 0 18px}
  header .lede{font-size:1.12rem;max-width:60ch;color:var(--ink)}
  .meta{margin-top:28px;font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);display:flex;gap:24px;flex-wrap:wrap}
  .meta b{color:var(--plum-deep);font-weight:500}
  section{padding:46px 0;border-bottom:1px solid var(--hair)}
  h2{font-size:clamp(1.6rem,4vw,2.1rem);margin:0 0 10px}
  .intro{max-width:64ch;color:var(--ink)}
  .step{display:flex;gap:20px;padding:20px 0;border-top:1px solid var(--hair)}
  .step:first-of-type{border-top:none}
  .snum{flex:0 0 auto;width:40px;height:40px;border-radius:50%;border:1.5px solid var(--plum);color:var(--plum);font-family:"Inter Tight";font-weight:600;display:grid;place-items:center}
  .step h3{font-size:1.15rem;margin:6px 0 6px}
  .step p{margin:0;color:var(--muted);max-width:62ch}
  table{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:18px}
  th{text-align:left;font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--hair)}
  th.num,td.num{text-align:right;font-family:"IBM Plex Mono",monospace;white-space:nowrap}
  td{padding:10px 12px;border-bottom:1px solid var(--hair);vertical-align:top}
  td.kw{font-weight:500;color:var(--ink)}
  .stat-row{display:flex;gap:40px;flex-wrap:wrap;margin:22px 0 0}
  .stat b{display:block;font-family:"Inter Tight";font-size:2.4rem;color:var(--plum);font-weight:600;line-height:1}
  .stat span{font-size:13px;color:var(--muted)}
  .controls{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:20px}
  .controls select,.controls input{font-family:"Inter";font-size:13px;padding:8px 10px;border:1px solid var(--hair);border-radius:8px;background:#fff;color:var(--ink)}
  .controls .count{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted)}
  tbody tr:hover{background:var(--cream)}
  .tag{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:var(--plum);border:1px solid var(--hair);border-radius:999px;padding:2px 8px;white-space:nowrap}
  footer{padding:40px 0 80px;font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);line-height:1.8}
  .wordmark{font-family:"Inter Tight";font-weight:600;font-size:1.1rem;color:var(--plum-deep)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <span class="eyebrow">Your content programme</span>
    <h1>A year of content, written and researched to <em>win the right clients.</em></h1>
    <p class="lede">This is how your blog and guides get made, and the full twelve-month schedule of what is coming. Every article is researched, written and checked to a consistent standard before it reaches your site.</p>
    <div class="meta"><span>Prepared for <b>Lauren Pearson</b></span><span>The Pearson Co.</span><span>{{TOTAL}} articles over 12 months</span></div>
  </header>

  <section>
    <span class="eyebrow">How every article is made</span>
    <h2>Seven steps, <em>every time.</em></h2>
    <p class="intro">No article is published on a whim. Each one moves through the same structured process, so quality and accuracy stay consistent across the whole programme.</p>
    <div style="margin-top:24px">{{STEPS}}</div>
  </section>

  <section>
    <span class="eyebrow">The programme at a glance</span>
    <h2>Fourteen themes, <em>built around your services.</em></h2>
    <div class="stat-row">
      <div class="stat"><b>{{TOTAL}}</b><span>articles in total</span></div>
      <div class="stat"><b>14</b><span>content themes</span></div>
      <div class="stat"><b>3</b><span>published per day</span></div>
      <div class="stat"><b>12</b><span>month rollout</span></div>
    </div>
    <p class="intro" style="margin-top:22px">The most valuable pages, the ones that explain your services, are published first so they are live early. The wider library of guides then builds month by month, each piece supporting those core pages.</p>
    <table><thead><tr><th>Theme</th><th>Focus</th><th class="num">Articles</th></tr></thead><tbody>{{SUMMARY}}</tbody></table>
  </section>

  <section>
    <span class="eyebrow">The full schedule</span>
    <h2>Everything that is <em>coming.</em></h2>
    <p class="intro">Browse the complete schedule below. Filter by month or by theme. Timings are shown as months from launch.</p>
    <div class="controls">
      <select id="f-month"><option value="">All months</option></select>
      <select id="f-pillar"><option value="">All themes</option></select>
      <input id="f-search" type="search" placeholder="Search titles">
      <span class="count" id="count"></span>
    </div>
    <table id="sched"><thead><tr><th>Month</th><th>Theme</th><th>Title</th><th>Format</th></tr></thead><tbody></tbody></table>
  </section>

  <footer>
    <div class="wordmark">The Pearson Co.</div>
    Smarter systems. Stronger pipelines. Sustainable growth.<br>
    Your 12-month content programme &middot; prepared for review
  </footer>
</div>
<script>
const ROWS = {{DATA}};
const $=s=>document.querySelector(s);
const esc=s=>(s==null?'':String(s)).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const months=[...new Set(ROWS.map(r=>r.m))].sort((a,b)=>a-b);
const pillars=[...new Set(ROWS.map(r=>r.p))].sort();
months.forEach(m=>{const o=document.createElement('option');o.value=m;o.textContent='Month '+m;$('#f-month').appendChild(o);});
pillars.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;$('#f-pillar').appendChild(o);});
function render(){
  const fm=$('#f-month').value, fp=$('#f-pillar').value, q=$('#f-search').value.toLowerCase();
  const tb=$('#sched tbody'); tb.innerHTML=''; let n=0;
  ROWS.forEach(r=>{
    if(fm && String(r.m)!==fm) return;
    if(fp && r.p!==fp) return;
    if(q && !r.t.toLowerCase().includes(q)) return;
    n++;
    tb.insertAdjacentHTML('beforeend',`<tr><td class="num">${r.m}</td><td>${esc(r.p)}</td><td class="kw">${esc(r.t)}</td><td><span class="tag">${esc(r.ty)}</span></td></tr>`);
  });
  $('#count').textContent=n+' of '+ROWS.length+' articles';
}
['#f-month','#f-pillar'].forEach(s=>$(s).addEventListener('change',render));
$('#f-search').addEventListener('input',render);
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
