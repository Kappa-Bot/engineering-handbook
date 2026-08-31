---
id: pat-design-context-layering
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - user-facing-surfaces
  - multi-tenant-products
  - vertical-products
sources:
  - src-awesome-design-md
  - src-emil-ui-skills
last_verified: 2026-08-31
review_due: 2027-02-28
---

# Design Context Layering

## Problem

Shared platforms and Vertical products need consistency without making every product, tenant and surface look identical. AI-assisted implementation amplifies the failure modes at both extremes:

- unconstrained generation creates inconsistent, generic template UI;
- one giant shared design system erases product/domain identity and encourages inappropriate reuse.

## Pattern

Resolve design context in layers. Each layer narrows the decision space without replacing the responsibilities below it.

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

It MUST NOT define a common portfolio art direction.

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

For material UI work, prefer a compact project-owned design contract over repeated prompt prose. The contract should communicate only durable decisions such as:

- visual and UX thesis;
- density and geometry;
- semantic color roles;
- typography hierarchy;
- surface/elevation model;
- interaction and motion character;
- responsive priorities;
- prohibited visual patterns;
- tenant customization boundary.

Use an existing repo-local `DESIGN.md`, `MASTER.md`, design-system document or equivalent when one already exists. Do not create `DESIGN.md` merely because this Pattern exists.

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

## Anti-slop guardrails

Treat these as review smells, not absolute bans:

- card grids used as the default answer to every hierarchy problem;
- cards nested inside cards without meaningful grouping;
- excessive pills, badges or icon-in-rounded-square tiles;
- decorative gradients, glass, blur, glow or shadows without product meaning;
- every section centered and every feature expressed as the same repeated unit;
- generic dashboard shells copied from framework defaults;
- low-value KPI cards or charts where direct text/table values communicate better;
- arbitrary hard-coded colors, radii, spacing or motion that fork established tokens;
- `transition: all` and motion added uniformly rather than by interaction purpose;
- large empty volume that pushes frequent operational work below the useful viewport;
- tenant branding implemented by allowing arbitrary CSS/JS.

When a smell is justified by real product/brand intent, keep it deliberately and verify the result rather than applying the list mechanically.

## Token/context discipline

Store deep design knowledge once and retrieve narrowly.

For routine work, a short local design contract plus the relevant surface/component rules should be enough. Deep reference retrieval is reserved for ambiguous or high-value design decisions.

Do not paste an entire external design corpus, all installed design skills or the full handbook into a task prompt. Skill and reference invocation should be proportional to the decision being made.

## Adoption rule

Adopt this Pattern incrementally. Existing products keep validated art direction and contracts; they do not need a redesign merely to conform to this abstraction. Use the Pattern when creating or materially evolving a surface, or when repeated inconsistency shows a real need for stronger design contracts.
