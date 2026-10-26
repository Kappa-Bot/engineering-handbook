---
id: ref-external-design-intelligence-corpus
kind: reference
status: active
owner: engineering
version: "0.2"
applies_to:
  - engineering-handbook
  - user-facing-surfaces
  - design-research
sources:
  - src-awesome-design-md
  - src-emil-ui-skills
  - src-ruucm-shadergradient
  - src-paper-design-shaders
  - src-paper-design-liquid-logo
  - src-dashersw-liquid-glass-js
  - src-mdn-webgl-best-practices
  - src-w3c-wcag-22
last_verified: 2026-10-26
review_due: 2027-01-26
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

## Shader, Liquid-Metal and Glass Effects (2026-10-26)

### Decision context and evidence limit

Animated shaders, metallic logo treatments and refractive glass can contribute distinctive product character, especially in commercial storytelling and sales demonstrations. They are **not** a replacement for interaction feedback, navigation clarity, responsive behavior or a coherent visual thesis. This evaluation is based on upstream documentation, repository code and stated licensing, **not** measured integration or a production/browser benchmark in MelodIQ products.

The current `std-ui-ux-quality-baseline` remains the normative motion/accessibility authority; `pat-design-context-layering`, `pb-frontend-quality-review` and `std-dependency-supply-chain-baseline` govern product fit and implementation review. This Reference creates no new organization-wide requirement or default dependency.

### Candidate outcomes

| Candidate | Outcome | Evidence and useful scope | Limitation / adoption boundary |
| --- | --- | --- | --- |
| **ShaderGradient** (`src-ruucm-shadergradient`) | **Adopt selectively after a pilot** | MIT React/Vue 3D animated gradient renderer; v2 separates renderer and controls, and documents pixel density, lazy-load settings and React/R3F compatibility. Candidate for a deliberate hero, demo entrance or bounded expressive marketing surface. | Three.js/React Three Fiber and GPU work introduce runtime cost. Match React/R3F versions, verify SSR/fallback behavior and benchmark target devices. Never turn it into a mandatory site or CRM background. |
| **Paper Shaders**, including `LiquidMetal` (`src-paper-design-shaders`) | **Adopt selectively after a pilot** | Apache-2.0 canvas-shader library with vanilla/React packages, custom logo/image masks, configurable animation and static frames. Candidate for brand treatments, sales media and a carefully scoped public surface. | The project warns that breaking changes may occur under `0.0.x`; pin the exact version and test updates. A logo treatment must preserve the original approved brand assets and legibility. |
| **Paper LiquidLogo app** (`src-paper-design-liquid-logo`) | **Learn / reference only** | Useful demonstration of liquid-metal brand expression, built with Paper Shaders. | Its application repository uses **PolyForm Shield 1.0.0**, including a noncompete condition; it is not an MIT/Apache general-purpose component library. Do not transplant its application code into commercial products by default. If any reuse is proposed, evaluate the actual intended use and license separately. Prefer the Apache-licensed Paper Shaders library. |
| **LiquidGlass JS** (`src-dashersw-liquid-glass-js`) | **Learn; reject as-is for production** | MIT proof of concept with refractive glass containers and controls. Useful as a visual/technical reference. | Single-commit repository, no released npm/React package (both remain roadmap items), keyboard/accessibility work deferred; its current implementation uses click-driven `div` controls and `html2canvas(document.body)` snapshots cached for its glass texture. This is a poor fit for frequently changing, sensitive authenticated workspaces. |

### Product/surface routing

- **Commercial/portfolio/showroom surfaces:** expressive GPU treatments MAY be considered for a *small, intentional* region when they reinforce actual brand or story and outperform a static/CSS treatment for the intended audience. They are not a substitute for customer imagery, typography, hierarchy and real interaction design.
- **Authenticated operational CRM, clinical or tenant-data screens:** default to stable semantic controls and light CSS materials. Prefer useful feedback, skeletons, state transitions and reduced latency. Do not adopt full-document screenshot/refraction tricks for decorative effects: the additional rendering/copy of potentially sensitive content needs justification and scrutiny even if no exfiltration is demonstrated.
- **Logo/marketing assets:** experiment with Paper Shaders or render approved static/short-loop derivatives; keep the original brand source, contrast and readable fallbacks intact. Rights over source code, logos and any outputs must be evaluated separately.

### Gate for any repo-local pilot

1. **Benefit:** identify the precise product/brand/user problem and compare against static artwork, CSS `backdrop-filter` or existing primitives. Reject a treatment added solely for fashionable glass/gradient decoration.
2. **Legal/dependency:** verify the *actual* package license, notice/redistribution obligations, version pin, transitive graph and compatibility before adding code. Paper LiquidLogo's source license must not be confused with Paper Shaders' Apache-2.0 license.
3. **Functional/accessibility:** never put essential text, primary navigation or input semantics inside a GPU-only effect; use real buttons/links with keyboard/focus semantics, readable contrast, a usable no-WebGL fallback, and reduced-motion handling. Apply `src-w3c-wcag-22`.
4. **Runtime/performance:** lazy-load bounded effects, limit canvas resolution/pixel budget, stop rendering when hidden/offscreen or unnecessary, clean up GPU resources, recover from context loss when relevant, and compare representative mobile/desktop behavior. Evaluate LCP/INP/CLS plus interaction responsiveness, GPU memory and scrolling; consult `src-mdn-webgl-best-practices`.
5. **Privacy and ownership:** do not render whole private DOM documents into shader textures without a documented use case and data-boundary review; avoid unnecessary external media/script calls and preserve tenant isolation.
6. **Evidence:** verify Chrome/Firefox/WebKit and representative mobile or actual target devices where material. Report visual, accessibility, motion and performance checks as **not run** until observed. A passing build or a beautiful upstream demo does not prove production suitability.

Promote a reusable implementation pattern only after a repo-local pilot shows a measurable, generalizable benefit. Re-evaluate these candidates on major upstream changes, license changes, maintenance deterioration or changed product needs. The catalog is **permission to evaluate**, not global deployment approval.
