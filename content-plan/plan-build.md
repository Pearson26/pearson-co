# Plan build — batch cadence

The 12-month plan (~1,085 records) is built in 14 managed batches, then sequenced. Full scope,
delivered in reviewable pieces. Say **"build next"** to generate the next batch.

## What one batch does
1. Research the pillar's keywords with the Semrush MCP: head terms, the long tail, volumes, KD, intent, and the live SERP gap. (UAE database for the regional CRM/process terms; UK/US for the discovered and global clusters, per the keyword universe.)
2. Write the pillar's records into `content-plan/plan.json`: 1 pillar page, the money/service pages, and the authority cluster, each a full record (title, slug, primary + secondary keywords with volume and KD, LLM-layer phrasings, intent, content type, role, ad-landing flag, direct-answer, H2 outline, internal-link targets, schema, word target).
3. `python scripts/render_plan.py` to regenerate `plan-rows.js` (dashboard) and `plan.md` (readable).
4. Update `plan-build-state.json` (advance `next_batch`, counts) and commit once to `main`.
5. Report the batch summary and the dashboard link, then wait for the next "build next".

## Batch order (priority-first; the seven ad-landing pillars lead so paid can launch)
| Batch | Pillar | Records | Why here |
|------:|--------|--------:|----------|
| 1 | Conversion & Funnel Optimisation | 95 | UK CRO is the paid standout |
| 2 | Revenue Operations (RevOps) | 95 | ad-landing, confirmed umbrella |
| 3 | CRM Implementation & Selection | 70 | ad-landing (UK CRM Services) |
| 4 | Fractional Sales Leadership + Growth Consulting | 60 | two small ad-landing pillars together |
| 5 | Customer Journey Mapping (part 1) | 60 | ad-landing, largest top-of-funnel audience |
| 6 | Customer Journey Mapping (part 2) | 60 | authority cluster |
| 7 | Hospitality Tech & Middle East Expansion | 85 | the moat |
| 8 | Process Mapping & SOP Creation (part 1) | 75 | largest demand in the project |
| 9 | Process Mapping & SOP Creation (part 2) | 75 | largest demand in the project |
| 10 | CRM Automation & Workflow | 95 | warmest CRM intent |
| 11 | Sales Reporting, Dashboards & Forecasting | 95 | high value, high CPC |
| 12 | CRM Consulting & Selection | 70 | high intent |
| 13 | CRM Adoption + Sales Pipeline Management | 65 | two small authority pillars together |
| 14 | Go-to-Market Strategy | 85 | bridge to expansion |
| Final | Sequencing pass | - | assign 12-month publish `seq`, front-loading the 15 pillar pages + priority money pages so paid lands on live pages |

Total: 1,085 records.

## Notes
- `seq` (publish order) is left null during batch build and assigned in the final sequencing pass, so build order does not lock publish order.
- Each record matches the schema in ARCHITECTURE.md section 3.
- Dashboard for review: `content-plan/content-plan.html` (open it; it reads `plan-rows.js`). It is `noindex` and uses the agency-document brand (#7f466f, Inter), distinct from the live-site article design.
- This is the plan-build phase. Publishing the articles (the Strategist run loop, 3 posts per "build next") begins only after the plan is complete and Netlify is connected.
