# Routine entrypoint: build the next posts

You are running a scheduled publishing routine for The Pearson Co. content engine.
Act as The Strategist. Follow CLAUDE.md and the souls in /workforce exactly.

## Steps
1. Read `CLAUDE.md`, `build_state.json`, and `content-plan/plan.md`.
2. Take the next **3** records with `seq >= build_state.next_index`, in order. (Floor 1 if quality requires; never exceed 3.)
3. For each record, run the pipeline using the soul files:
   The Researcher → The Wordsmith → The Humaniser → (The Optimiser + The Interrogator) → The Connector → The Builder → The Auditor.
   - On `REVISE`, fix the named failures and re-audit. Publish nothing that has not passed.
4. After the batch is approved:
   - `python scripts/link_graph.py`
   - `python scripts/blog_index.py`
   - `python scripts/build_sitemap.py`
   - `python scripts/style_gate.py site/blog/ site/services/` (any hit blocks the commit; fix and re-run)
   - `python scripts/verify_state.py --write`
5. Update `BUILD-PLAN.md` (session-log row) and `MEMORY.md` (Current State) in the same commit.
6. Commit once and push to `main`:
   `git add -A && git commit -m "Publish N posts (seq X-Y): <slug>, <slug>, <slug>" && git push origin main`
7. Post the live review block: each new URL on its own line, grouped new vs changed, with pillar and role.

## Guardrails
- Push to `main` only. One commit per run, all files bundled.
- British English, no em dashes, no banned words. The style gate must pass.
- Do not modify the homepage, styles.css or script.js. Do not invent posts outside `plan.md`.
- If the queue is exhausted, stop and report.
