# Pipeline map: HubSpot

The engine writes into the existing HubSpot **Sales Pipeline** (`pipeline` id `default`).
The stages below are already configured in the account. This file is the contract the engine
uses so it always writes the correct internal value, not the label.

Account: `148645046` (EU1, currency AED, timezone US/Eastern).

## Stages (internal value -> label, probability)

| Order | Internal `dealstage` value | Label | Prob | Meaning / entry criteria |
|------|-----------------------------|-------|------|---------------------------|
| 1 | `appointmentscheduled` | New Enquiry | 10% | A lead has come in (scorecard, form, referral) and been intaked. Default entry stage. |
| 2 | `qualifiedtobuy` | Discovery Scheduled | 20% | Discovery call booked in the calendar. |
| 3 | `presentationscheduled` | Needs Assessment Complete | 30% | Discovery done, need and fit understood, scope forming. |
| 4 | `decisionmakerboughtin` | Proposal / Recommendation Sent | 50% | Written recommendation or proposal delivered. |
| 5 | `contractsent` | Negotiation / Commercial Review | 70% | Terms and price under discussion. |
| 6 | `closedwon` | Verbal Agreement | 90% | Verbal yes, paperwork pending. (Note the label override.) |
| 7 | `closedlost` | Won | 100% | Signed and won. (Note: this internal value carries the "Won" label here.) |
| 8 | `5492694205` | Lost | 0% | Lost or disqualified. Record the reason. |

**Important:** the labels for the last two stages are overridden in this account. Internal
`closedwon` shows as "Verbal Agreement" and internal `closedlost` shows as "Won". Always set
the stage by the intent in the "Meaning" column and confirm against the label, not by assuming
the usual HubSpot defaults. Before any run that closes deals, re-read the live stage list
(`get_properties` on `deals` for `dealstage`) in case the account has been reconfigured.

## Entry stage by lead type (Phase 1)

- Scorecard lead, contact form enquiry, referral, inbound DM: **New Enquiry** (`appointmentscheduled`).
- A lead who books a call directly (calendar link): **Discovery Scheduled** (`qualifiedtobuy`).

## What the engine sets on each object

### Contact (create or update, keyed on email)
- `email`, `firstname`, `lastname`
- `company` (and `jobtitle`, `phone` when known)
- `lifecyclestage` = `lead`
- `hs_lead_status` = `NEW`
- A **Note** associated to the contact carrying the raw capture payload: offer, source, score,
  band, per-question answers, and the lead's own message. This keeps the scorecard result on
  the record without needing a custom property.

### Deal (create, keyed on: no existing open deal for this contact)
- `dealname` = `"{Company or Name} Revenue Leak Review"`
- `pipeline` = `default`
- `dealstage` = entry stage from the table above
- `dealtype` = `newbusiness`
- `amount` = leave unset at New Enquiry unless Lauren gives a figure. Set once scope is known.
- Associate to the Contact (and Company if one is created).
- A **Note** on the deal summarising the qualification grade and the recommended next step.

### Task (create, on Lauren)
- `hs_task_subject` = `"Review & send first response for {Name} (Scorecard: {band})"`
- `hs_task_body` = the recommended action, the lead's score and top leaks, and a link to the
  Gmail draft the Scribe prepared.
- `hs_task_status` = `NOT_STARTED`
- `hs_task_priority` = `HIGH` for grade A, `MEDIUM` for B, `LOW` for C.
- `hs_timestamp` (due) = next business day. Associate to the Contact and Deal.

## Optional custom properties (only if Lauren adds them in HubSpot)

If Lauren creates these deal/contact properties in the HubSpot UI, the engine will populate
them instead of relying on the Note. The engine must not assume they exist; it checks first.
- `scorecard_score` (number), `scorecard_band` (single line), `lead_source_detail` (single line).

## SLAs (match the promise made on the site)

- **First response within one business day.** The site and the scorecard both promise this.
  The Rainmaker schedules the Task and the draft so Lauren can hit it.
- **Grade A leads:** draft ready same run, Task priority HIGH, suggest a call within 3 working days.
- **No open deal sits without a next action.** Every open deal has either a future-dated Task
  or a booked meeting. The Analyst flags any that do not.

## Deduplication

Before writing: `search_crm_objects` on contacts by `email`; if found, update rather than
create. Then check the contact's associated deals for an open one in `default`; if an open deal
exists, add a Note and a Task instead of creating a second deal.
