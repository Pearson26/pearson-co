# Intake runbook: the hybrid loop, step by step

This is the exact procedure the Rainmaker runs to turn a new lead into worked pipeline. It uses
the tools available to the assistant: Gmail, HubSpot, and (Phase 2) Apollo. Every prospect-facing
artefact is a **draft**. Nothing is sent.

Run it on demand ("run a sales intake") or on a schedule Lauren approves (see the end).

## Preconditions

- HubSpot connected (Contacts, Deals, Tasks writable). Confirmed for this account.
- Gmail connected for `lauren@thepearsonco.com`.
- Read `SALES-ENGINE.md`, `pipeline.md`, `icp.md`, `sequences.md` first.

## Step 0: Load state

Read `sales-engine/sales_state.json`. Note `last_run` and `last_lead_email`. Only process leads
that arrived after `last_run`, plus anything Lauren names explicitly.

## Step 1: Pull new leads (Prospector)

Scorecard and contact-form leads arrive as email to `lauren@thepearsonco.com` via FormSubmit.

- Gmail: `search_threads` with a query such as
  `newer_than:2d (subject:"Revenue Leak Scorecard" OR subject:"website enquiry" OR from:formsubmit)`.
  Widen the window if `last_run` is older.
- For each new thread, `get_message` and parse the FormSubmit table into fields:
  `name`, `email` (the reply-to), `company`, `team_size`, `offer`, `source`, `score`, `band`,
  `answers`, `message`.
- Skip anything already processed (match on email + arrival time against `last_lead_email` and
  the CRM). Collect the rest as the run's lead list.

## Step 2: Qualify (Qualifier)

For each lead, score fit and intent per `icp.md`, assign a grade (A/B/C/D), and decide:
- **A, B, C:** proceed to CRM write.
- **D (out of profile or spam):** do not create a deal. If a real person wrote in, draft a brief,
  kind decline or redirect. Note the reason and move on.

## Step 3: Write to HubSpot (per lead, in order)

Always deduplicate first.

1. **Find or create the Contact.**
   - `search_crm_objects` on `contacts` filtering `email = {email}`.
   - If found: keep its id, update only missing fields.
   - If not: `manage_crm_objects` create a contact with `email`, `firstname`, `lastname`,
     `company`, `lifecyclestage=lead`, `hs_lead_status=NEW`.
2. **Check for an existing open deal** on that contact in pipeline `default`. If one exists, do
   not create a second. Add a Note and a Task instead, then skip to step 4.
3. **Create the Deal.**
   - `dealname = "{company or name} Revenue Leak Review"`, `pipeline=default`,
     `dealstage=appointmentscheduled` (New Enquiry), `dealtype=newbusiness`.
   - Associate the deal to the contact.
4. **Attach a Note** (to the contact, and to the deal) with the full capture payload: offer,
   source, score, band, answers, the lead's message, and the qualification grade with a one-line
   reason. This is the record of why the deal exists and what the lead said.
5. **Create a Task on Lauren.**
   - Subject: `Review & send first response for {name} (Scorecard: {band})`.
   - Body: the grade, score, top three leaks, the recommended next step, and a pointer to the
     Gmail draft from step 4 of the Scribe.
   - `hs_task_status=NOT_STARTED`, priority by grade (A=HIGH, B=MEDIUM, C=LOW),
     due next business day. Associate to the contact and deal.

## Step 4: Draft the first response (Scribe)

- Pick the right template from `sequences.md` by grade and lead type.
- Fill every merge field from the real lead data (`first_name`, `score`, `band`, `leak_1`,
  `leak_2`, plain consequences). If a field cannot be filled truthfully, cut that line.
- Gmail: `create_draft` addressed to the lead's email, from Lauren, subject and body from the
  template. **Draft only.** Do not send.
- For grade A, also draft the discovery-call invite (template 4) so Lauren can send whichever fits.

## Step 5: Report and record (Analyst)

- Build the run summary: leads pulled, grades, deals created vs updated, drafts waiting, and any
  D declines. Flag anything that needs Lauren today (grade A, or a deal with no next action).
- Update `sales-engine/sales_state.json`: `last_run` (now), increment `leads_processed` and
  `deals_created_total`, refresh `deals_open` (recount from HubSpot), set `last_lead_email`, and
  add a one-line `notes` entry.
- Append a row to `sales-engine/SALES-LOG.md` (date, leads, deals, drafts, notes).
- Post the summary to Lauren with the count of drafts waiting for approval.

## The human gate (Lauren's part)

1. Open Gmail drafts. Read each one. Edit in her own words as needed.
2. Send the ones she is happy with. Book calls.
3. Move the HubSpot deal stage as reality changes (call booked -> Discovery Scheduled, etc.).
4. Mark the Task done.

The engine never performs steps 1 to 4. It prepares them.

## Scheduling (optional, Lauren's call)

The intake can run automatically on a cadence (for example, twice a day) using a scheduled
routine, still drafting only and never sending. This keeps the funnel warm without a person
watching the inbox. Do not create the schedule without Lauren asking; when she does, the routine
runs this runbook and posts the Analyst summary.

## Phase 2 hook (outbound, off by default)

When Lauren switches on outbound, the Prospector builds a target list in Apollo against the ICP,
enriches it, and the same steps 3 to 5 apply, with a cold-friendly first-touch template. Outbound
still drafts only. See `roles/the-prospector.md`.
