---
id: ref-internal-ui-pwa-donor-audit
kind: reference
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - ui-ux
  - pwa
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-w3c-appmanifest
  - src-w3c-service-workers
  - src-w3c-cssom-view
  - src-w3c-css-env
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Internal UI/PWA Donor Audit — 2026-08-15

## Status

This is supporting internal evidence, not a normative Standard.

It records the audit that informed:

- `std-ui-ux-quality-baseline`;
- `std-web-pwa-baseline`;
- `pat-mobile-responsive-interaction`;
- `pat-visual-evidence-integrity`;
- `pb-frontend-quality-review`.

The goal was not to choose a "best repository". It was to extract the strongest validated decisions across mature internal products, reject local/outdated practices, and combine the remainder with primary external standards.

## Audited repositories

### CCSE-AI-Coach

Audited main tree: `4aaada8d5cfcf132d7873585124beb94f7ddf32d`.

Strong reusable evidence:

- Playwright E2E plus Vitest/Testing Library rather than visual confidence from code review alone;
- explicit security/content/release checks;
- internal UI package boundary;
- semantic light/dark/system theme discipline identified later as a donor for MovOps;
- concise architecture/safety constraints in `AGENT_CONTEXT.md`.

Do not promote:

- CCSE-specific study/business/backend semantics;
- its legacy `AGENT_CONTEXT.md` filename as the new cross-repository agent contract.

Alignment note: engineering discipline is broadly aligned, but the repo predates the handbook's current hierarchical `AGENTS.md` adoption model.

## Aluminio Bartra webapp

Audited main tree: `d227118151f90e8b625d31c4ce86eac3375f02f1`.

Strong reusable evidence:

- explicit product/brand UX principles rather than generic SaaS aesthetics;
- one-primary-action/card and work-intent grouping in the Alicia operational interface;
- proactive accessible validation, optional uploads, search/empty states, `aria-live` feedback;
- `@axe-core/playwright` in the testing stack;
- PWA scoped to `/alicia`, while the public commercial site deliberately does not expose install metadata;
- no service worker/offline/cache/push added merely to call the admin "PWA";
- versioned install-icon routes/cache-busting and private admin shortcuts;
- safe-area/mobile-keyboard behavior.

Do not promote:

- Bartra's ivory/graphite/bronze palette, radius or brand assets;
- Alicia-specific workflow labels;
- exact component composition as a universal admin design.

Key promoted principle: **PWA by valuable product surface, not automatically by domain/application.**

## COGOP Barcelona Attendance

Audited main tree: `e7bd5ad1e8c02cded380dd17c8f007481af37dc7`.

Strong reusable evidence:

- separate E2E, visual and responsive QA plus release-quality gate;
- virtual keyboard/`visualViewport` treated as product behavior;
- bottom navigation must adapt to editable focus/keyboard;
- safe areas and local horizontal strips;
- fix responsive geometry instead of hiding it with global overflow clipping;
- gestures have ownership; scrolling/content inside a sheet must remain usable;
- camera/scanner UX depends on physical workflow, not one global camera assumption;
- real-device verification for installed-PWA/keyboard/camera behavior;
- mobile docs preserve practical lessons learned after implementation.

Rejected/outdated/local evidence:

- a later COGOP delta that disables page zoom (`maximumScale`/`userScalable=false`) conflicts with the accessibility direction adopted by `std-ui-ux-quality-baseline` and MUST NOT be promoted;
- exact navigation counts, scanner modes and layout values remain product-specific.

Alignment note: COGOP already has a small root `AGENTS.md`, but it currently contains only a Next.js-specific freshness rule rather than the full repo-local adoption contract.

## MovOps OS

Audited main tree: `3c8de888357f04e8f50dddb1d84bf7dd540b2dbe`.

Strongest reusable evidence:

- explicit donor reuse from Bartra/COGOP/CCSE, taking only practices stronger than the current implementation;
- evidence-first visual QA: semantic-state assertions before capture;
- detection of pseudo-states (many files, few unique images) rather than trusting screenshot counts;
- viewport/project/theme/state provenance and content hashes;
- distinction between CSS viewport and actual image pixels/device scale;
- scenario isolation to prevent localStorage/draft contamination;
- dedicated cross-browser project/evidence identity;
- required-state matrices instead of screenshot-count vanity metrics;
- bounding/containment checks because transforms can clip content without document overflow;
- explicit client-visible defect ledger;
- one dominant readable motion beat, one dominant conversion CTA, consistent page-header grammar and content-driven sizing;
- explicit native-device checks reported honestly rather than fabricated;
- private installable app surface while public/configurator remain ordinary web surfaces.

Do not promote:

- Agurto-specific brand/story/3D composition;
- exact viewport list as universal;
- the historical multi-agent execution contract (`docs/AGENT_EXECUTION.md`), which allows up to six workers and predates the current handbook policy of zero subagents by default;
- repository-specific phase/acceptance numbering.

Key promoted principle: **visual evidence must prove semantic state and provenance, not merely exist.**

## Cross-repository conclusions

The four repositories are **philosophically aligned** with the handbook's evidence/reuse/production-quality goals, but structurally they predate parts of the current agent/governance model.

Their UI/PWA practice is ahead of the pre-audit handbook because the handbook had no canonical UI/PWA Standards yet.

The strongest combined model is not any single donor:

```text
Bartra
brand-led UX + scoped PWA + build/brand provenance
        +
COGOP
mobile physical interaction truth
        +
CCSE
semantic theme/testing discipline
        +
MovOps
semantic visual-evidence integrity + donor reuse
        +
primary standards
WCAG/APG/Manifest/Service Workers/CSS viewport & safe-area specs
        ↓
new handbook UI/PWA baseline
```

## Promotion rule learned from this audit

The handbook is the canonical baseline, **not proof that a mature product repository cannot contain a better practice**.

For new transversal, architecture-significant or quality-sensitive work, it can be rational to compare relevant mature internal implementations even when the handbook already has a usable baseline.

When a donor practice is stronger:

1. validate that it is generalizable;
2. challenge it against primary external sources where applicable;
3. promote the improved synthesis upward;
4. then consume the canonical handbook version in future work.

Do not make ordinary local tasks perform a portfolio-wide audit when it has low probability of changing the result.
