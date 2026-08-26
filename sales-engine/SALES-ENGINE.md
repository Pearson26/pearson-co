# The Pearson Co.: Sales Engine (SALES-ENGINE.md)

The content engine fills the top of the funnel. This engine turns that attention into
self-generated pipeline: qualified opportunities in HubSpot, worked in a repeatable,
mostly-automated loop, with a human gate on anything that reaches a prospect.

Read this file at the start of every sales run. It is the single source of truth for how
The Pearson Co. builds and works its own pipeline. It sits alongside `CLAUDE.md` (the
content rules) and mirrors the `/workforce/` pattern: a small set of role "souls", chained
by an orchestrator, against explicit gates.

---

## 1. What this is

- **Owner:** Lauren Pearson, The Pearson Co. (Dubai). CRM / RevOps / hospitality-tech consultant.
- **Goal:** a steady flow of self-sourced, well-qualified sales conversations, tracked as deals
  in the existing HubSpot pipeline, without buying leads and without a full-time SDR.
- **Model:** **hybrid.** The engine does the top of the funnel on its own: capture, enrich,
  qualify, stage, draft. A human (Lauren) approves and sends anything that a prospect sees, and
  books the meetings. Nothing is emailed or messaged to a prospect automatically.
- **Phase 1 (live now): self-generated inbound.** The website generates enquiries through a
  lead magnet (the Revenue Leak Scorecard) and the contact form. The engine intakes each one
  into HubSpot and prepares the first response. Outbound prospecting (Apollo) is Phase 2 and is
  documented but not switched on until Lauren asks.

## 2. The funnel, end to end

```
   ATTRACT            CAPTURE              QUALIFY            CONVERSATION         PIPELINE
   content    ->   scorecard / form  ->   fit + intent  ->  discovery call  ->   deal worked
   (engine)        (site)                 (engine)          (human)              (human + engine)
```

- **Attract** is the content engine's job (blog, service pages). Not repeated here.
- **Capture** happens on the site: `site/revenue-scorecard.html` (the lead magnet) and the
  homepage contact form. Both carry a `source` and, for the scorecard, a `score`, `band` and
  `answers` payload so every lead arrives pre-qualified.
- **Qualify, stage, draft** is this engine (roles in `/sales-engine/roles/`).
- **Conversation and close** stay with Lauren. The engine prepares, never impersonates.

## 3. The roles (`/sales-engine/roles/*.md`)

Five souls, chained by The Rainmaker per run. Each file is the role's full charter.

1. **The Rainmaker**: orchestrator. Reads `sales_state.json`, pulls new leads, runs the roles
   per lead, stages the deal, records what happened, reports.
2. **The Prospector**: sourcing. Phase 1: reads inbound (Gmail enquiries, scorecard leads).
   Phase 2: builds and enriches target lists via Apollo. Never contacts anyone.
3. **The Qualifier**: scores each lead against the ICP (`icp.md`): fit and intent, A/B/C/D.
   Decides pursue, nurture, or decline, and sets the entry stage.
4. **The Scribe**: writes the human-gated outreach (first response, discovery invite,
   follow-up) in Lauren's voice, from `sequences.md`. Saves as a Gmail **draft**. Never sends.
5. **The Analyst**: pipeline reporting: what came in, stage movement, conversion, what needs
   Lauren's attention today.

## 4. The run loop (per sales run)

The Rainmaker executes this. One run handles all new leads since the last run.

1. **Pull** new leads: unread scorecard / enquiry emails in Gmail, plus any lead Lauren flags.
2. For each lead, in order:
   - **Prospector:** extract name, work email, company, and the captured payload (score, band,
     answers, message, source). Enrich lightly with public context.
   - **Qualifier:** score against the ICP. Assign grade and entry stage. If out of profile,
     mark decline-with-a-kind-reply and stop.
   - **CRM write:** create or update the **Contact**, create the **Deal** at the entry stage in
     the Sales Pipeline, associate them, set the source and score properties, and create a
     **Task** for Lauren with the recommended next action and timing. (Mappings in `pipeline.md`.)
   - **Scribe:** draft the first response as a Gmail draft addressed to the lead, plus a
     discovery-call invite where the grade warrants it. Leave both unsent.
3. **Analyst:** produce the run summary (new leads, grades, deals created, drafts waiting) and
   record it. Update `sales_state.json` and the log.
4. **Hand to Lauren:** post the summary with the count of drafts waiting for approval. Lauren
   reviews drafts, edits, sends, and books calls.

## 5. Hard rules (the gate)

- **Human gate on outbound. Always.** The engine drafts; Lauren sends. No email, WhatsApp,
  LinkedIn message or meeting invite goes to a prospect without Lauren pressing send. Drafts
  only.
- **Never fabricate a prospect, a quote, a case study, a figure, or a testimonial.** If a
  detail is not known, leave it out or ask Lauren.
- **One source of truth: HubSpot.** Every worked lead is a Contact + Deal there. No shadow
  pipeline in a spreadsheet.
- **Respect consent and privacy.** Only work leads who reached out or who fit the ICP for
  legitimate B2B outreach. Honour unsubscribes and "not interested" immediately, in the CRM.
- **Lauren's voice, house style.** All prospect-facing copy follows the `CLAUDE.md` house
  style: British English, no em dashes, no banned vocabulary, no AI tells, straight quotes,
  warm and specific. Drafts that fail this are rewritten before Lauren sees them.
- **Deduplicate.** Before creating a Contact or Deal, search HubSpot by email and by company.
  Update, do not duplicate. Never create a second open deal for a lead who already has one.
- **Pointer-based, not date-based.** Progression is tracked by `sales_state.json`, not by
  guessing what ran when.

## 6. State (`sales-engine/sales_state.json`)

Holds `last_run` (ISO), `leads_processed`, `deals_open`, `deals_created_total`,
`last_lead_email`, and `notes`. The Rainmaker updates it in the same step it records a run.
Never hand-edit the counts if a reconcile step is available; prefer to recount from HubSpot.

## 7. The offers (`offers.md`)

Self-generated pipeline needs a reason for a stranger to raise their hand. Phase 1 offers:

- **The Revenue Leak Scorecard** (live): a free self-assessment at `/revenue-scorecard.html`.
  The magnet. Produces graded, self-qualified leads.
- **The 30-minute Revenue Leak Review** (the tripwire consult): a short, specific call that
  turns a scorecard result into a first conversation. The natural next step the Scribe offers
  A and B grades.

Full definitions, positioning and the qualifying logic live in `offers.md`.

## 8. Definitions of done

- **A captured lead is done** when there is a HubSpot Contact + Deal at the right stage, with
  source and score set, associated, and a Task on Lauren for the next action.
- **A first response is done** when a house-style draft, addressed to the lead and referencing
  their actual score and leaks, is waiting in Gmail for Lauren to approve.
- **A sales run is done** when every new lead is intaked, every draft is written, the Analyst
  summary is posted, and `sales_state.json` and the log are updated.

## 9. Directory map

```
/sales-engine/
  SALES-ENGINE.md        <- this charter
  pipeline.md            <- HubSpot pipeline map: stages, criteria, property mappings, SLAs
  icp.md                 <- ideal customer profile + fit/intent scoring
  offers.md              <- the self-generated pipeline offers
  sequences.md           <- human-gated outreach templates (all drafts, never auto-send)
  intake-runbook.md      <- the exact hybrid loop, step by step, with the tool calls
  sales_state.json       <- engine state (pointer + counts)
  roles/
    the-rainmaker.md the-prospector.md the-qualifier.md the-scribe.md the-analyst.md
```

## 10. Permanent facts

- Hybrid. The engine builds pipeline and drafts; Lauren approves and sends. No exceptions.
- HubSpot is the pipeline. The Sales Pipeline stages are already defined (see `pipeline.md`).
- Phase 1 is self-generated inbound. Phase 2 (Apollo outbound) is documented, switched off.
- House style and privacy apply to every prospect-facing word.
