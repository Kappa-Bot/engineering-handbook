---
id: pat-editorial-reading-navigation
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - long-form-web-documents
  - editorial-reference-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-13
review_due: 2027-05-13
---

# Editorial Reading and Navigation

Use for regulations, manuals, technical references, procedures, and learning sequences people read, cite, resume or print. The reader's purpose determines the entry point. Apply [the UI baseline](../standards/ui-ux-quality-baseline.md) and the product's own design and content authority.

## Source and reading order

- Identify the document, audience and relevant edition or approval status before optional orientation. Put the title and status before the compact contents control in reading and keyboard order. Distinguish source text from summaries, navigation group names, training prompts and planning aids. Preserve source wording, order and meaningful relationships where fidelity is required.
- Organize entry points by reader intent, such as consulting the source, following a procedure or resuming training. Keep the first useful action and high-value destinations discoverable without waiting for motion. Use headings, lists and native links for stable structure. Measure line length, type size, line spacing and table density with representative copy in the actual font, across narrow and wide layouts. Use the product's typography and language to choose values.
- Keep real row/column headers and associations for tabular information. Wrap real long values, including references and identifiers, before choosing local scrolling for an intrinsically two-dimensional table. Keep the rest of the page within the reflow floor. Test that readers can find, select and copy complete values in context. Check a generated PDF or the intended print output from a focused deep link. Preserve headings, full table text and relationships across page breaks. Remove screen controls and focus rings from print while retaining visible focus on screen.
- Deliver the source in readable HTML when scripting is unavailable and the content is already known. Keep essential destinations as links. When saved progress or editable steps require scripting, expose a truthful reading view with the relevant sections available. Only expose working tracking controls and counters once they can reflect the user's action.

## Three distinct navigation states

1. **Shared destination.** Use stable IDs on meaningful headings or sections and real links to them. Let explicit navigation establish a shareable fragment and normal browser history. Test direct entry, internal activation, reload, invalid fragments, and Back/Forward. Keep a legitimate destination readable below any sticky header, including after breakpoint changes. Prefer native scroll and focus behavior. If scroll animation makes the location indeterminate or competes with restoration, settle the destination immediately.
2. **Live reading position.** Track the visible section independently of the shared URL. Mark the current location within the contents, for example with `aria-current="location"`. If groups auto-open as the reader scrolls, defer hiding a group while it contains focus. A deliberate jump should move focus to a meaningful, visible destination where needed, particularly when its trigger will become hidden. Keep the compact and wide index in sync from one destination list. Bound the index to the usable viewport and let readers collapse it when it would dominate the text.
3. **Resume or completion.** Return from a step to the relevant group or source. A last-viewed reference is a convenience, with an explicit entry point and valid fallback. Keep it separate from confirmed completion, authorization and any sensitive record data. Recover the actual route, fragment and focus after interruptions as appropriate.

For in-product discovery, test natural queries, exact titles or numbered targets, and near-misses where the same number occurs in body text. Prefer an exact intent match over incidental terms when the product recognizes that intent. Return the corresponding real destination and offer an actionable empty state. Use [Interaction Continuity](interaction-continuity.md) for the search input and results.

## Acceptance

Inspect actual first useful content, sticky-header clearance and focus at the destination. Use a narrow viewport, browser zoom where relevant, a representative long table and direct or restored deep links. Check readable no-script content, text selection and a real print artifact when those uses apply. Record which surfaces, engines and native modes were exercised. [Visual Evidence Integrity](visual-evidence-integrity.md) defines the evidence boundary.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "editorial-reading-contract",
      "type": "pattern",
      "text": "Put title, source and status before optional contents. Keep semantic headings and tables readable without scripts. Separate shareable fragment, live section, resume and completion. Preserve focused index links, visible anchor landings and history. Rank exact reading intent above incidental matches.",
      "source": "pat-editorial-reading-navigation",
      "covers": ["editorial-reading"],
      "activate_when": ["risk:editorial-reading"],
      "phase": ["planning", "implementation"],
      "priority": 94
    },
    {
      "id": "editorial-reading-verification",
      "type": "verification",
      "text": "Check title before the compact index, native deep-link arrival below sticky UI, active section versus URL, focused group and Back/Forward. Inspect narrow/zoomed real tables, no-script text, copy and the generated print output where applicable.",
      "source": "pat-editorial-reading-navigation",
      "covers": ["editorial-reading"],
      "activate_when": ["risk:editorial-reading"],
      "phase": ["verification"],
      "priority": 94
    }
  ]
}
```
