---
id: pb-marketing-context-and-content
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - marketing-workflows
  - public-marketing-websites
  - client-business-websites
sources:
  - src-marketingskills
last_verified: 2026-11-09
review_due: 2027-02-09
---

# Marketing context, content and conversion review

## Scope and authority

A task-scoped procedure for positioning, copywriting/editing, CRO, competitor research and sales collateral. This fills the commercial-context gap; it does not create a second design, SEO or truth standard. `pol-truthful-engineering` owns claim accuracy; `pb-public-client-website-delivery` owns complete site delivery; `std-public-web-discoverability-baseline` owns search prerequisites; `pat-design-context-layering` owns brand/design inheritance.

The selected external methods, pinned revision and MIT notice are in `ref-marketing-skills-adoption-assessment`. They are useful hypotheses and workflows, not proof of business uplift or new universal MUSTs. Apply only the sections relevant to the request.

## 1. Reuse the approved commercial context

Find the existing brand brief, product context, approved proposal or decision record before asking the owner to repeat it. Consumer-declared `commercial-context` landmarks take precedence over discovered `.agents/product-marketing.md`, `.claude/product-marketing.md`, legacy context files or `docs/marketing-context.md`. A filename is a discovery hint, not a mandate to copy or relocate information.

For missing context, use `tpl-product-marketing-context` in an authorized consumer location, or add its fields to the existing brief. Resolve only gaps that materially change the deliverable:

- Audience and job: who needs help, triggering situation, desired outcome, alternatives, decision maker and disqualifiers.
- Offer: what is available now, deliverables, service region/languages, dependencies, exclusions, approved pricing if relevant and the next useful action.
- Proof: dated source/owner for each material claim, permission to publish, actual results versus proposed capability, and demo/illustrative content.
- Voice: approved examples, useful vocabulary, objections and prohibited claims. Preserve client voice; do not impose the agency's identity on every business.
- Constraints: channels and contact endpoints, scope, approval owner, confidentiality, launch/indexability state and measurement availability.

Keep personal contacts, raw interviews, CRM records and confidential commercial evidence in their authorized private system; reference a sanitized conclusion when permitted. Do not place customer records in the public Handbook or emit them into generated context profiles.

## 2. Select the right writing operation

| Observed starting point | Procedure and output |
| --- | --- |
| Existing approved text; small correction requested | Make the requested edit, preserve voice/structure and explain any necessary factual correction; no full rewrite |
| Existing page performs poorly | Identify audience, traffic intent, real primary action and observed friction before rewriting; distinguish measured issues from hypotheses |
| New page, proposal or offer | Draft from the context: relevant customer problem, concrete available help, supportable proof and one clear next step |
| Missing evidence for a strong claim | Ask a material question or use accurate qualified language; do not invent numbers, case studies, team expertise or testimonials |

Use short, concrete language understandable by the intended buyer. Replace generic superlatives and feature inventories with relevant benefits that the offer can actually deliver. Preserve approved header/signature or other explicitly retained elements. A simple quote request need not become a SaaS signup funnel; a local business may prefer a call or a reviewable WhatsApp prefill.

Review in order: message clarity, match to intent, factual proof, action clarity, friction, accessibility and response feedback. Message fit is distinct from factual truth: a truthful page can still address the wrong audience or job. Rank recommendations by observed impact/risk, confidence and effort; an assumed impact is not measured uplift. Keep page sections only when they answer a distinct visitor question or support the next action. Route implementation to the existing website/UI patterns, not to a mandatory component checklist.

## 3. Competitor evidence and useful sales material

For each material competitor claim, record source URL, observation date, region/plan if relevant, and one of **observed / inferred / not observed**. “Not found on the inspected pages” is not “they do not offer it.” Separate the factual difference from its possible customer implication. Recheck changing prices/features before comparing publicly; avoid fabricated weaknesses, deceptive access or unauthorized account/contact actions.

Build collateral for a specific decision: a short proposal, one-page comparison, objection response or demo sequence. State the customer's next action early; explain current capabilities and boundaries rather than promising every possible integration. A demo script identifies real, simulated and unavailable steps. Any ROI example has explicit assumptions and is not a guaranteed saving. Channel qualification and handoff use `pb-lead-qualification-and-handoff`.

## 4. Verify and maintain

Before approval, check each material claim against the local proof record; test the actual CTA destination and content; preserve demo disclosures and the existing release gate. Confirm the message remains readable on its real surface. Record whether evidence was observed, missing or not tested. Use `pb-conversion-measurement-and-experiments` for outcome instrumentation or experimentation; editorial opinion is not an experiment result.

Update only changed facts/approved decisions in the existing context, with date and owner. Tentative learnings remain hypotheses until evidence and owner approval support promotion. Do not let a successful draft silently change pricing, ICP, brand rules or other repositories.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "marketing-context-and-proof",
      "type": "pattern",
      "force": "should",
      "text": "Use pb-marketing-context-and-content: reuse the approved local brief, audience/job, available offer, voice, proof and next action; preserve point-edit scope. Separate observed competitor facts from inference and unavailable evidence. Diagnose intent/CTA/friction before CRO changes; do not invent proof or uplift. Keep private facts local and route design/SEO to their existing owners.",
      "source": "pb-marketing-context-and-content",
      "covers": ["commercial-truth", "message-fit"],
      "activate_when": ["archetype:marketing-content-change"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 82
    }
  ]
}
```
