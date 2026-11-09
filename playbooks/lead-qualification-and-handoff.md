---
id: pb-lead-qualification-and-handoff
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - marketing-workflows
  - business-development
sources:
  - src-marketingskills
  - src-boe-lssi
  - src-eu-gdpr
last_verified: 2026-11-09
review_due: 2027-02-09
---

# Lead qualification and commercial handoff

## Scope

Use for approved prospect research, qualification, lead scoring, RevOps stage definitions and sales handoff. `pb-marketing-context-and-content` owns audience/offer/proof; this procedure owns the transition from sourced opportunity to a traceable next action. `ref-marketing-skills-adoption-assessment` records provenance and exclusions.

This is not permission to scrape lists, enrich personal profiles, buy access, send messages, deploy CRM workflows or schedule recurring work. Research, draft creation, CRM edits and sending are separate actions with separate task authorization. Existing owner limits, CRM stages and data boundaries remain in force.

## 1. Inspect the existing system and qualify evidence

Use the approved ICP and current CRM as the source of truth. Inspect the existing columns, stage meanings, duplicate policy and latest activity before adding information. Keep the owner's compact schema; a useful finding can be a concise note instead of another permanent column.

For each approved business, capture only what supports a decision:

| Decision | Evidence to keep in the authorized private record |
| --- | --- |
| Fit / no fit / unresolved | Real service, region, apparent business need and disqualifier; identify assumptions |
| Website status | Verified business/domain match and checked URL/date; distinguish a broken site, social-only presence and “not located” from confirmed absence |
| Contact quality | Public source and date, relevant business role/channel, confidence; a syntactically valid address is not verified delivery |
| Priority | Applicable local criterion plus evidence; lack of a website can be a priority when the owner approved that strategy, not a universal rule |
| Next step | Responsible owner, current stage, material unanswered question and permitted next action |

Prefer source-backed observations over invented numeric precision. Unknown budget, headcount or purchase intent stays unknown. Do not infer sensitive personal traits or repurpose patient, congregation, prayer or clinical data for prospecting. Minimize collection, authorized access and retention under the applicable data-processing basis; public availability is not unlimited reuse permission.

## 2. Keep contact permission separate from fit

For Spain, apply the current LSSI-CE Article 21 channel rules separately from GDPR processing requirements. Promotional email/equivalent electronic communications generally require prior request or express authorization; the prior-contract exception has conditions, including lawful contact acquisition and the sender's own similar products/services. Provide the required simple, free objection/withdrawal route and honor suppression. Do not generalize that exception to every former contact or every channel.

An address published on a website, business status, a purchased list, deliverability verification or a claimed GDPR legitimate interest does **not by itself** establish permission to send electronic marketing. Verify the actual channel, relationship/permission or applicable exception, sender identity, data source, transparency and objection handling with the responsible owner. If the basis is uncertain, leave outbound action blocked and identify the missing evidence; this procedure is not individualized legal clearance. Recheck current official sources for another jurisdiction or a materially different channel.

Internal drafts may be prepared within the task's authority while permission is unresolved, clearly marked **not approved for sending**. Never describe a draft as sent or a successful tool delivery as recipient interest. A valid contact, a lawful channel, a qualified prospect and a customer are different facts.

## 3. Handoff without changing the CRM by stealth

Reuse approved stages. Define entry/exit evidence only where missing: who owns the next action, what must be observed before transition, and how acceptance/rejection or a blocked state is recorded. A proposal sent is not a signed contract; a demo viewed is not an accepted price; an unanswered message is not a lost deal.

When authorized to update records, check identity/deduplication and fresh activity first, make the narrow edit, preserve history and verify persisted values. Respect existing “frozen”, suppression and customer states. Do not create a parallel tracker, bulk overwrite the CRM or infer an approval from silence.

Handoff format: **business and fit evidence → current stage → permitted next action → owner → unresolved question**. Use dates or response targets only when the owner actually agreed them. Sending, enrollment in a sequence and reminders require their own authorization; no default cadence follows from this playbook.

## Verification

Use synthetic or minimized examples. Check source/date and business identity, honest unknowns, priority under the approved strategy, no duplicate stage owner, channel gate independent of fit, suppression handling and readback of authorized CRM edits. Report draft/researched/updated/sent distinctly; retain confidential evidence only in its authorized system. Commercial success requires actual outcome evidence, not an attractive record.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "lead-qualification-permission-boundary",
      "type": "pattern",
      "force": "should",
      "text": "Use pb-lead-qualification-and-handoff: qualify with dated business evidence and honest unknowns; preserve the existing CRM/stages, owner and next action. Public/valid contact details do not establish outbound permission: check the channel's LSSI/GDPR basis and suppression separately. Drafts pending permission are not approved to send. Keep private/sensitive data out of public artifacts; verify only authorized record changes.",
      "source": "pb-lead-qualification-and-handoff",
      "covers": ["outreach-privacy"],
      "activate_when": ["archetype:lead-qualification"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 90
    }
  ]
}
```
