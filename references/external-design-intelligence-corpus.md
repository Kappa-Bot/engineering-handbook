---
id: ref-external-design-intelligence-corpus
kind: reference
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - user-facing-surfaces
  - design-research
sources:
  - src-awesome-design-md
  - src-emil-ui-skills
last_verified: 2026-08-31
review_due: 2027-02-28
---

# External Design Intelligence Corpus

## Purpose

Evaluate `VoltAgent/awesome-design-md` and `emilkowalski/skills` as reusable design evidence without turning external aesthetics or personal preferences into cross-repository style law.

This is a **Reference**, not a Standard. It exists to reduce repeated research and improve design reasoning.

## Findings

### `awesome-design-md`

The repository provides a broad corpus of analyzed `DESIGN.md` files derived from real product and marketing surfaces. The useful unit is not a named visual skin; it is the explicit decision structure captured for each reference: atmosphere, semantic color roles, typography, geometry, spacing, component states, layout, depth, responsive behavior and guardrails.

Use the corpus as precedent evidence for questions such as:

- how information density changes component treatment;
- how a commercial surface differs from an operational workspace;
- how a product reserves accent color for action or meaning;
- how hierarchy, whitespace, borders, imagery and typography carry identity;
- how different products deliberately avoid the same generic SaaS composition.

Do **not**:

- assign one external brand as the permanent style for one internal product;
- average many references into a synthetic visual soup;
- copy proprietary fonts, logos, assets or brand-specific trade dress;
- copy an external token set wholesale when product constraints differ;
- treat a reference's visual rule as a cross-repository `MUST`.

### Emil Kowalski skills

The skills repository is especially useful for interaction craft: animation purpose, curves/durations, gesture feel, reduced-motion awareness, avoiding unnecessary animation, prototyping alternatives and choosing mature UI primitives instead of hand-rolling them without reason.

The useful lesson is **decision quality**, not mandatory use of a particular animation library, component package or aesthetic.

## Corpus strategy

Use the whole corpus as an **indexed learning base**, but retrieve narrowly at task time.

```text
broad corpus
    -> pattern extraction
    -> internal design guidance
    -> task classification
    -> 1-3 relevant precedents when needed
    -> product-owned design decision
```

Do not load dozens of external `DESIGN.md` files into routine implementation context. This adds tokens, contradictory cues and imitation pressure without proportional value.

## Reference routing

Choose references by the design problem, not by brand admiration.

| Problem | Useful precedent families |
| --- | --- |
| dense operational software | Linear, Airtable, Sentry, PostHog, Stripe-like product surfaces |
| consumer intake / guided flow | Airbnb and other low-friction marketplace/service flows |
| restrained premium marketing | Apple and high-end product/editorial references |
| developer / technical product | Vercel, Supabase, developer-tool references |
| expressive/cinematic marketing | Runway, Framer and other motion-led references |
| trust-heavy transactional UI | mature fintech/payment references |
| scheduling / availability | scheduling-product references |
| data-heavy inspection | analytics/observability references |

The table is a discovery aid, not an approved recipe. A task may use a different precedent when its actual users, workflow or brand justify it.

## What should be promoted internally

Promote only the generalizable decision logic that survives comparison with internal products and applicable standards. Examples:

- design context should be layered rather than globally skinned;
- product/surface intent should drive density and interaction grammar;
- visual identity should come from coherent rules, not decoration count;
- motion should communicate causality/orientation/character and should disappear from frequent operations when it adds latency;
- design references should be retrieved selectively;
- tenant branding should remain bounded by platform/vertical interaction contracts;
- visual review should explicitly reject generic generated-template output when the product requires distinct identity.

Product-specific palettes, exact typography, marketing compositions and domain semantics remain local.

## Licensing and reuse

Both referenced repositories were verified as MIT-licensed on 2026-08-31. Internal guidance should still prefer synthesis over bulk copying so that provenance remains clear and internal contracts describe our products rather than donor brands.
