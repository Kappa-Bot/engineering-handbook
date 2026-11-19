---
id: pat-design-context-layering
kind: pattern
status: active
owner: engineering
version: "0.2"
applies_to:
  - user-facing-surfaces
  - multi-tenant-products
  - vertical-products
sources:
  - src-awesome-design-md
  - src-emil-ui-skills
  - src-unslop
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Design Context Layering

## Problem

Shared platforms and Vertical products need consistency without making every product, tenant and surface look identical. AI-assisted implementation amplifies the failure modes at both extremes:

- unconstrained generation creates inconsistent, generic template UI;
- one giant shared design system erases product/domain identity and encourages inappropriate reuse.

## Pattern

Resolve design context in layers. Each layer establishes responsibilities, not an immunity for its current visual implementation. The reconstruction contract in [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction) governs material design work, including replacement of weak local decisions in an authorized redesign.

```text
Engineering Handbook quality/accessibility/engineering floor
        ↓
Platform executable contracts and safe primitives
        ↓
Vertical product semantics and interaction grammar
        ↓
Surface intent / role / usage frequency
        ↓
Tenant brand identity within allowed controls
        ↓
Page, state and component composition
```

This is a design-resolution model, not a requirement that every repository contain directories matching these labels.

## Layer responsibilities

### Handbook

Own cross-repository quality and operating guidance: accessibility, truthful states, responsive integrity, verification, design-research discipline, interaction-quality principles and agent/context efficiency.

It MUST NOT define a universal portfolio art direction. The owner-approved [visual-direction catalog](visual-direction-catalog.md) defines a **limited Glassmorphism starting default for new or already-authorized internal-console material design** without overriding current product `DESIGN.md`, authentic tenant identity or any non-console surface. This does not import a shared palette or component shell.

### Platform

Own only proven reusable implementation contracts: semantic primitives, safe theming/branding boundaries, accessibility behavior, interaction foundations and other cross-Vertical mechanisms.

Platform primitives MUST NOT smuggle the Platform Admin's own art direction into customer products.

### Vertical

Own domain semantics and reusable product grammar: what information matters, repeated workflows, domain-specific components, density requirements and the interpretation of Platform configuration/branding contracts.

A Vertical should reuse Platform mechanics without outsourcing its product design decisions to Platform.

### Surface / role

The same product may require materially different design behavior by context. Examples include:

- public/commercial storytelling;
- consumer intake or wizard;
- repeated operator workspace;
- owner/executive decision surface;
- kiosk/field/touch-heavy surface;
- settings/admin/data-inspection surface.

Surface classification changes density, disclosure, motion tolerance, target sizing and information hierarchy. It does not require a separate brand.

### Tenant

Tenant identity may specialize allowed visual identity such as logos, approved colors, approved typography choices, imagery and bounded shape/density presets when the Platform/Vertical contract supports them.

Tenant customization MUST NOT arbitrarily replace accessibility, interaction semantics, authorization, workflow truth or domain invariants.

### Local / branch / site / resource

A local unit is operational scope, **not a new design-system tier by default**. Give it distinct visual identity only when the product explicitly supports that requirement. Avoid combinatorial theme inheritance for every organizational resource.

## Design contracts

For material UI work, use a compact project-owned design contract rather than repeated prompt prose. Separate **fixed facts and invariants** (capabilities, domain meaning, rights, permissions, truthful claims) from **revisable design decisions**. The latter include:

- visual and UX thesis;
- density and geometry;
- semantic color roles;
- typography hierarchy;
- surface/elevation model;
- interaction and motion character;
- responsive priorities;
- rejected visual patterns with the defect and scope that justify rejection;
- tenant customization boundary.

Use an existing repo-local `DESIGN.md`, `MASTER.md`, design-system document or equivalent when one already exists. Do not create `DESIGN.md` merely because this Pattern exists.

For a redesign that authorizes a new direction, explicitly mark which decisions are replaced and why. Change tokens, representative components and affected screens together so old and new systems do not silently coexist. Inspect dependent consumers before changing shared primitives; redesign authority for one surface does not authorize collateral changes elsewhere. Move historical rationale out of the active contract when it conflicts with the replacement, retaining its decision trail.

## Reference intelligence

External references are precedent evidence, not skins.

For a materially ambiguous design problem:

1. inspect current product evidence and existing local contracts;
2. classify the surface and user task;
3. identify the exact unresolved design question;
4. retrieve the smallest relevant internal/external reference set;
5. extract principles and tradeoffs;
6. make a product-owned decision;
7. implement with existing primitives where possible;
8. render/review the actual result.

Use `ref-external-design-intelligence-corpus` for external precedent discovery.

## Anti-slop review

Name the audience, surface, first useful decision and product-specific evidence. Then require each treatment to earn its place. In material redesign, **remove or replace an unjustified treatment rather than preserving it until someone proves measurable harm**. Template interchangeability, incoherent emphasis and unsupported copy are defects even if the page passes functional tests. Distinctive typography, expressive motion, gradients and rich materials can still serve a deliberate product decision; their mere presence or absence proves nothing.

| Symptom and likely cause | Defect threshold | Alternative and fitting use | Acceptance |
|---|---|---|---|
| Every item is a card, cards are nested, or sections have identical weight. A component template drove composition. | Readers cannot tell what is primary or compare related facts. | Give continuous prose, lists and exact lookup their own forms. Separate cards fit independently selectable items or a comparison that benefits from distinct boundaries. | Ask a reviewer to identify the next action and compare real items at representative widths. |
| Pills, badges, icon tiles and decorative numbers repeat titles. Each block inherited a template label. | Decoration competes with a real status or repeats text without improving recognition. | Keep distinct status and category cues, with text or shape as needed. A single approval-status label or a recognizable action icon can carry meaning. | Remove one layer and compare comprehension. Check that remaining icons have appropriate text alternatives and states still make sense without color. |
| Reflections, gradients, blur and heavy shadows are applied to every surface. The material has no assigned role. | Decorative depth flattens hierarchy, obscures content or adds measurable cost in a frequent flow. | Reserve material for meaningful boundaries. A translucent navigation layer can distinguish persistent controls over a solid reading plane. | Inspect content through and around the surface in both themes, including scroll, focus and intermediate frames. Measure the relevant cost when the effect is material. |
| Oversized hero, chrome or empty bands delay essential content. A showcase composition was copied into a routine task. | At an ordinary narrow or short viewport, a user must pass decorative space or repeated labels before reaching the main destination. | Shorten chrome or start with the document and its most useful entry points. A large photographic hero fits an approved story when it keeps the proposition and action available. | Identify the first useful content and action on load, at narrow and short sizes, and during menu/focus states. |
| Generic headlines, promises, helper paragraphs or identical sections recur across pages. Copy was written before the content job was known. | A reader cannot tell who it is for, what is available, or what happens next. A status or claim has no source. | Write the concrete audience, action, consequence or constraint in the product's language. A branded headline can sit alongside a precise description. Use a relevant reason or recovery hint where it changes a decision. | Trace material claims to approved facts. Compare pages side by side and remove copy that repeats adjacent controls. Verify that the CTA and status describe the actual outcome. |
| An entrance hides available content, hover changes the meaning of a click, or decoration looks like completed work. Visual state was allowed to lead semantic state. | Users must wait to read, lose an action, or see a confirmation before its source can verify it. | Let the real state drive feedback. Use a restrained indicator for a confirmed transition or a useful motion cue with stable hit targets. | Check first frame, mixed input and interruption. Test pending, failure and confirmed state. See [Interaction Continuity](interaction-continuity.md). |

Keep token choices with the owning product and preserve the tenant customization boundary. Compare the current design with a materially better composed alternative using the same content and state; a simpler variant can isolate the contribution of an effect. Do not reduce the choice to "old style versus plain grey". Choose the result that best serves the task and product character, including a complete structural replacement when needed. Use [Frontend Quality Review](../playbooks/frontend-quality-review.md) for the direction, nine passes and acceptance record.

## Token/context discipline

Store deep design knowledge once and retrieve narrowly.

For routine work, a short local design contract plus the relevant surface/component rules should be enough. Deep reference retrieval is reserved for ambiguous or high-value design decisions.

Do not paste an entire external design corpus, all installed design skills or the full handbook into a task prompt. Skill and reference invocation should be proportional to the decision being made.

## Adoption and supersession

The 2026-11-16 owner-authorized Unslop adoption **replaces the earlier incremental-preservation default**. In material redesign, an existing palette, layout, type scale, hero or glass treatment has no grandfathered status. Reconstruct systemic problems; refine genuinely local defects; retain an excellent solution only because current evidence supports it. A small task or read-only audit does not become an unsolicited portfolio redesign.

This is not a universal art direction. The Handbook supplies a demanding design method and one scoped internal-console starting default from the [visual catalog](visual-direction-catalog.md); each product still supplies its content, visual world and resulting contract. The limited default is evaluated only on the next authorized new console or material redesign after refreshing the consumer bundle. Source publication is not proof that applications or workstations adopted it.

Direction and anti-slop methodology materially adapt Unslop by Damir Sokolovsky (@heydamir), CC BY 4.0; [attribution and substantial changes](../references/unslop-adoption-assessment.md#attribution-and-reuse) are retained centrally.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "design-purpose-before-treatment",
      "type": "decision-question",
      "text": "Assess DESIGN.md as evidence, not a frozen skin. Define audience/task, character, product world, focal content and signature. Diagnose generic composition, effects and copy; reconstruct systemic defects and supersede weak design choices within the authorized scope.",
      "source": "pat-design-context-layering",
      "covers": ["design-fit"],
      "activate_when": ["risk:design-fit"],
      "phase": ["planning", "implementation"],
      "priority": 95
    }
  ]
}
```
