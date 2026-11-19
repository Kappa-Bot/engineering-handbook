---
id: pat-visual-direction-catalog
kind: pattern
status: active
owner: engineering
version: "1.0"
applies_to:
  - authenticated-operational-consoles
  - user-facing-surfaces
  - vertical-products
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-19
review_due: 2027-02-19
---

# MelodIQ visual-direction catalog: selectable product materials

## Decision and boundaries

MelodIQ Systems maintains a **catalog of visual directions**, not a single portfolio skin. Material is one design axis alongside product semantics, typography, palette, density, imagery, motion, navigation grammar and interaction. A selected material never turns an unrelated component into the same component, determines tenant identity or overrides the [UI/UX quality Standard](../standards/ui-ux-quality-baseline.md).

**Scoped starting default:** for a **new or already-authorized material redesign of an authenticated internal operator/admin console**, select **Glassmorphism** if the current product has no explicit applicable material choice. It is an initial design hypothesis to test against actual content and rendered evidence, **not an instruction to re-skin an existing console**, update every product or ship a theme. The product's current explicit `DESIGN.md` wins over the default; a new owner-authorized task can supersede a prior aesthetic within the authorized scope. A genuine contrast, density, performance or accessibility failure is reason to select another direction and document it.

For marketing/public sites, member/patient self-service, kiosks, field work, editorial documents and clinical/financial specialty surfaces, **no material is inherited** just because the product belongs to MelodIQ. The owner/product chooses. Operator-console shell interactions are independent of material choice. A style request does not authorize a redesign, permission change, branding change, data migration, paid service, third-party asset or release.

## Initial catalog

| Direction | Visual language and suitable jobs | Mandatory guardrails | Canonical detail |
| --- | --- | --- | --- |
| **Glassmorphism** (`glassmorphism`) | Restrained translucent navigation/context over a solid active-data plane; limited elevated context. **Scoped internal-console starting default.** | Never stack glass cards over legible data or rely on blur to identify an action; check composite contrast, fallback and performance. | [Operator Glass](operator-glass-surface-material.md) |
| **Neumorphism** (`neumorphism`, *neomorphism*, *neumorfismo*, *soft UI*) | Selective raised/inset tactile cues, where physical affordance supports the task. **Explicitly selectable**, including internal consoles. | Borders, focus, labels, status, error and pressed/disabled signals work **without shadows**; dense records remain readable and solid. | [Accessible Neumorphism](operator-neumorphic-surface-material.md) |
| **Solid/editorial** (`solid-editorial`) | Opaque surfaces with strong hierarchy and restrained elevation for reading, dense operations, forms and constrained devices. | Still requires deliberate visual identity, responsive layout, semantic states and non-generic composition. | [UI/UX Quality Baseline](../standards/ui-ux-quality-baseline.md) |

The versioned machine-readable inventory is [`machine-readable/visual-directions.v1.json`](../machine-readable/visual-directions.v1.json); it owns canonical IDs, bilingual aliases, valid surfaces and the **only** default map. Add a future visual direction as a validated catalog entry plus a real reference document, not by duplicating keyword tables, silently editing a model prompt or forcing a new shared UI package. The compiler's discovery taxonomy indexes this Pattern under ES/EN searches; the stable four-file discovery registry remains unchanged.

## Selection precedence

1. An **explicit, authorized task-specific visual decision** for the target product/surface, subject to protected domain, tenant, accessibility and release constraints.
2. The **current explicit local product `DESIGN.md` / applicable design contract**. In a material redesign a prior aesthetic can be superseded deliberately; record the new decision instead of leaving two active instructions.
3. The catalog's **Glassmorphism starting default for an internal console only**, if the target work is new or a material redesign already authorized.
4. **Product-owned open decision** on all other surfaces; ask only if the missing choice materially affects the deliverable. A valid, deliberate solid alternative is preferable to failed glass/neumorphic aesthetics.

The deterministic resolver evaluates the **style precedence**, not authorization: `python -m automation.engineering_context visual-directions --root . --surface internal-console --local-style neumorphism` returns the local decision, while adding `--style solid-editorial` returns the explicit task choice. It sets `authorizes_ui_change: false` and `runtime_user_toggle: false`. Unknown IDs and ambiguous aliases fail rather than falling back silently. A returned starting default does not prove the task was authorized or that the screen passes QA.

When working in a product repository and the task permits modifying its design contract, record the decision briefly in the **existing** product-owned `DESIGN.md` (do not generate duplicate authoritative DESIGN files):

```yaml
# Illustrative local design-contract fields, NOT a mandated shared schema.
surface: internal-console
visual_direction: neumorphism
decision: Explicit product design choice for this authorized redesign
supersedes: Prior local material choice, if any
reason: Task hierarchy and measured rendered evidence
exceptions: Solid financial tables and forced-colors controls
```

Keep material, dark/light modes, color/brand, density, animation and device adaptation separate. A designer may choose Glassmorphism for a console while keeping its charts, cells and forms opaque; choosing Neumorphism does not require every control to be embossed. Neither direction entails a per-user runtime chooser.

## Routing, implementation and visual QA

The task descriptor marks `operator-visual-direction-choice` for real internal-console design/redesign, including when no style was mentioned. An **explicit** style change adds `operator-glass-material-change` or `operator-neumorphic-material-change` only in operator scope. Rejected styles and mere comparisons are not adoption; public style requests can consult this catalog **without** acquiring the internal default or operator-specific material gates. Backend fixes, doc explanations, copy/typo micro-edits and isolated sidebar mechanics do not grant a material redesign.

For approved material work, inspect real (or explicitly identified fixture) states at useful widths and heights, 320 CSS px and 200% zoom; evaluate  keyboard, touch, screen-reader semantics, focus, hover/pressed/selected/disabled/error/saving states, actual text/non-text contrast, forced colors, reduced motion, theme changes if supported, overlay stacking and fallback with effects disabled. Keep important data on stable opaque surfaces; protect scroll/paint performance and product/tenant identity. Distinguish design prototyping from deployment evidence and disclose unrun browser/device/accessibility gates. The [Frontend Quality Review](../playbooks/frontend-quality-review.md) nine-pass method and the [Modern Web Platform Workflow](../playbooks/modern-web-platform-workflow.md) remain operational owners, not duplicated here.

**Deferred project B:** a user-facing live Glass/Neumorphism selector, user preference persistence, transition/migration behavior, all-style state coverage and runtime rollout are outside this phase. This source publication changes Handbook guidance only. No MelodIQ application is claimed to have adopted the catalog until its own repository and rendered product have separate evidence.

## Agent context projection

```json agent-context
{
  "units": [
    {
      "id": "visual-direction-selection-contract",
      "type": "decision-question",
      "text": "Resolve an authorized design task against current local DESIGN.md, then the scoped Glassmorphism candidate for new/authorized internal-console material design only. Neumorphism/solid are selectable; public surfaces have no default. Test task hierarchy and rendered accessibility. Style does not authorize redesign, release or a user toggle.",
      "source": "pat-visual-direction-catalog",
      "covers": ["visual-direction-fit"],
      "activate_when": ["archetype:visual-direction-choice", "archetype:operator-visual-direction-choice"],
      "phase": ["planning", "implementation"],
      "priority": 86,
      "force": "should"
    },
    {
      "id": "visual-direction-material-regression-gates",
      "type": "verification",
      "text": "Verify authorized product style against local DESIGN.md, readable data, contrast, focus/states, 320px/200% zoom, input/assistive-tech, forced-colors, no-effects fallback and performance. Document unrun gates and any product UI not changed; a starting default is not adoption or a live user toggle.",
      "source": "pat-visual-direction-catalog",
      "covers": ["visual-direction-fit"],
      "activate_when": ["archetype:visual-direction-choice", "archetype:operator-visual-direction-choice"],
      "phase": ["verification"],
      "priority": 84,
      "force": "should"
    }
  ]
}
```
