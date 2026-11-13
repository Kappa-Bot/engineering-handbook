---
id: pat-interaction-continuity
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - user-facing-web-surfaces
  - interactive-web-controls
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-w3c-css-view-transitions-1
last_verified: 2026-11-13
review_due: 2027-05-13
---

# Interaction Continuity

Apply when motion, a transient layer or multiple input sources can change what the user sees or controls. The [UI baseline](../standards/ui-ux-quality-baseline.md) defines the quality floor. The product owns the visual direction, input priorities and timing.

## Commit the interaction independently of the effect

Define the trigger, visible and accessible state, input owner, focus destination, and completion or interruption behavior. Apply semantic state and available content when the action takes effect. Let animation explain the result while focus, hit targets, layout and reading remain usable. Limit transitions to the properties with a specific job. Prefer shared, product-owned tokens by purpose such as press, opening and progress.

| Effect or state | Fit | Implementation and interruption check |
|---|---|---|
| Fade or slide on opening and closing | Relate a transient layer to its trigger or indicate dismissal. | Keep the active focus target readable from entry. On dismissal, remove hidden controls from input and restore focus promptly. Cancel the old exit on reopen. Keep essential headings, tables and actions available on initial render. |
| Elevation, scale or press | Clarify hover or activation on an appropriate pointer. | Keep the hit area stable through pointer-down/up. Supply equivalent focus and touch feedback. Test crossing the boundary during press and remove spatial motion under reduced motion where it adds no information. |
| Border, color or opacity | Distinguish selection, emphasis or input feedback. | Preserve contrast at intermediate frames, apply the focus indicator immediately, and keep the boundary from moving surrounding content. Use a semantic state or visible non-color cue where needed. |
| Progress and orientation indicators | Reflect a real task update, selection or reading position. | Update accessible values with the underlying change. A transform can reduce layout work if geometry stays fixed. Confirm what was measured and how much work remains using [Performance Budgeting](performance-budgeting.md). |
| Scroll or route entry | Orient after a meaningful navigation or deliberate scroll action. | Preserve destination, Back/Forward restoration and focus. Skip interpolation when it hides a deep link or competes with native navigation. Keep available content visible during entry. |
| Loading and confirmation | Explain real pending work and the confirmed outcome. | Tie the visible and announced state to the operation. Reserve useful space, avoid artificial waiting, and keep recovery available. See [Frontend Quality Review §6](../playbooks/frontend-quality-review.md#6-define-states-and-content-stress). |

Repeated input should reach the intended final state even if a previous animation is pending, completing or cancelling. Use the transition API's cancellation mechanism where available. Prevent old callbacks from overwriting newer intent or removing the current transition's state. Test both reduced motion at startup and a preference change during motion when that path can be active. Where a control depends on scripts for persistence or meaningful feedback, preserve the readable content and expose the control only when it can work.

## Disclosures and search

- Use a named trigger and ordinary links for a group of navigation destinations. Expose expanded state and the associated panel. If fine-pointer hover previews the panel, keep preview separate from explicit activation. A click arriving just after hover should do what the user intended. Scope delay/grace to pointer preview and clear pending timers when ownership changes. Keep an open panel operable while focus is inside and reconcile focus before hiding its links.
- Check the sequence hover → click → leave, focus into or out of the group, optional arrow shortcuts, Escape, outside dismissal, repeated activation and touch. Keyboard entry can show the final panel immediately. Touch uses deliberate activation and retains scrolling and tap geometry.
- In a search combobox with listbox results, keep DOM focus in the input and the active descendant tied to an existing option. Reset or reconcile the active result when the query changes. Keyboard movement can scroll the selected result into view. A stationary pointer over that moving list should not override the keyboard selection. Intentional pointer movement can retake selection without forcing another scroll. On modal dismissal, restore the opener or another logical target if the opener is gone. Check query, focus, list scroll and page scroll separately.

## Theme changes

- Define precedence between an explicit preference, system scheme and fallback. Apply the available authoritative preference before first content paint and keep the semantic `color-scheme` consistent. With scripts off, CSS can follow the system scheme even when client storage is unavailable. Keep storage or save failure truthful.
- Apply linked foreground and background roles together, including active/hover controls and surfaces. Palette interpolation can leave a readable final pair illegible between frames. Verify early and intermediate contrast and settled appearance, including the immediate fallback.
- Make a curtain or other capture-based effect optional. Feature-detect the API and switch immediately on unsupported, rejected or reduced-motion paths. For a native View Transition, participating live elements can be excluded from hit testing. Keep the active document interactive during the animation or skip/cancel the visual effect when it would mask focus or swallow input. One tested approach clips away the old visual layer over the live document after the update. The direction and duration belong to the product. Validate the actual target engines.
- Check first paint and reload in the system schemes, rapid repeat before capture and during the effect, keyboard focus and a separate click while moving, reduced motion, API absence, and cleanup after success or interruption. Verify final preference, focus and scroll with actual browser events. [Visual Evidence Integrity](visual-evidence-integrity.md) covers the temporal proof.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "interaction-continuity-contract",
      "type": "pattern",
      "text": "Apply real state and visible focus immediately. Separate hover preview, click/touch activation and keyboard selection. Guard against stale callbacks and stationary pointers. Preserve stable targets, readable no-script content, working controls and immediate reduced-motion feedback.",
      "source": "pat-interaction-continuity",
      "covers": ["interaction-continuity"],
      "activate_when": ["risk:interaction-continuity"],
      "phase": ["planning", "implementation"],
      "priority": 94
    },
    {
      "id": "interaction-continuity-verification",
      "type": "verification",
      "text": "Exercise hover-to-click, keyboard takeover, Escape/focus return, rapid repeat, touch, reduced motion and no-script fallback as applicable. Assert event destination, scroll, usable focus and that exposed controls work.",
      "source": "pat-interaction-continuity",
      "covers": ["interaction-continuity"],
      "activate_when": ["risk:interaction-continuity"],
      "phase": ["verification"],
      "requires": ["visual-evidence-temporal-input"],
      "priority": 96
    },
    {
      "id": "theme-continuity-contract",
      "type": "pattern",
      "text": "Define preference precedence and first paint. Change foreground/background together, use CSS system fallback for script-free reading, and keep latest intent through repeated activation. Skip or cancel visual capture when it would mask focus or swallow input.",
      "source": "pat-interaction-continuity",
      "covers": ["theme-continuity"],
      "activate_when": ["risk:theme-continuity"],
      "phase": ["planning", "implementation"],
      "priority": 96
    },
    {
      "id": "theme-continuity-verification",
      "type": "verification",
      "text": "Verify first paint, reload and initial system scheme, then repeat input before and during capture. Check intermediate contrast, live focus/hit targets, unchanged reading position, reduced motion, API absence and final preference/cleanup.",
      "source": "pat-interaction-continuity",
      "covers": ["theme-continuity"],
      "activate_when": ["risk:theme-continuity"],
      "phase": ["verification"],
      "requires": ["visual-evidence-temporal-input"],
      "priority": 96
    }
  ]
}
```
