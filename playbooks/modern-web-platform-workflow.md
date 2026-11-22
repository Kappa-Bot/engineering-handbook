---
id: pb-modern-web-platform-workflow
kind: playbook
status: active
owner: engineering
version: "1.5"
applies_to:
  - user-facing-web-surfaces
  - browser-platform-changes
sources:
  - src-modern-web-guidance
  - src-modern-web-guidance-src
  - src-ponytail
  - src-w3c-aria-apg
  - src-whatwg-html-dialog-close-result
  - src-w3c-idle-callback-deadline
  - src-whatwg-html-native-image-lazy-loading
last_verified: 2026-11-21
review_due: 2027-02-17
---

# Modern web platform: choose, integrate and verify

## Purpose and authority

Use this workflow before materially adding/replacing browser HTML/CSS/client-side behavior or auditing its suitability. The [UI Standard](../standards/ui-ux-quality-baseline.md#modern-platform-and-browser-contract) owns its mandatory applicability; [Reuse First](../policies/reuse-first.md#minimum-complete-change) owns the minimum-complete decision. It complements Unslop's product direction, not a mandatory new visual treatment. Pure SQL/backend/infra work, documentation research and mechanical copy edits do not require a browser modernization exercise.

Start with **audit**, **bounded fix**, or **authorized redesign/modernization**. A match or a legacy finding grants no write, install, publication, data access or paid-service authority. For a connected website/CRM/product agent, first resolve [the relevant boundary owners](../references/connected-product-resource-map.md).

## 1. Establish the actual contract

Read local `AGENTS.md`, current decisions/`DESIGN.md`, package/lockfile and the relevant component, consumers and tests. Record only facts that change the decision:

- the user-visible capability and failure to fix, including implicit primitives such as a confirmation dialog;
- essential behavior versus optional enhancement, browser/device/assistive-technology support and accessibility obligations;
- React/Next or other framework ownership, client/server split, hydration, IDs and current CSS/component conventions;
- loading/empty/error/denied/confirmed states, data sensitivity and the actual integration/side effects;
- baseline evidence and acceptance for the affected journey, not a generic Lighthouse target.

Do not infer the supported browser floor from a developer's Chrome version or from Vercel deployment. If the product has no documented matrix, use a conservative supported implementation, identify the gap and obtain a material support decision before dropping behavior. For a material visual redesign, follow `pb-frontend-quality-review` and update the scoped design contract coherently.

## 2. Find the smallest relevant guidance

Translate the capability into two to five generic English action words, without customer names, record data, credentials, repository paths or framework/domain noise: `responsive data table`, `announce validation error`, `confirm modal dialog`, `reduce interaction latency`. Split distinct capabilities; do not retrieve unrelated top-ranked results merely to demonstrate usage.

The following links are pinned to distribution **1.0.1**, commit `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65`. Open the relevant complete Markdown, then its cited official specification/compatibility evidence when the decision depends on current support. A cached guide's support data is dated. The repository [full guide tree](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides) exposes all 210 guide files and categories, not only this shortlist. Preserve the SHA when following a README link that points to `main`.

| Need / search concept | Exact pinned guide |
| --- | --- |
| Native dialog and confirmation | [ui-components/dialog.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/ui-components/dialog.md) |
| Dense/responsive CRM table | [ui-atoms/responsive-table.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/ui-atoms/responsive-table.md), [ui-behaviors/sortable-table.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/ui-behaviors/sortable-table.md) |
| Responsive layout | [css/responsive-design.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/css/responsive-design.md) |
| Form validation and input composition | [forms/validate-input-after-interaction.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/forms/validate-input-after-interaction.md), [forms/ime-safe-enter-submit.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/forms/ime-safe-enter-submit.md) |
| Accessibility and async errors | [accessibility/accessibility.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/accessibility/accessibility.md), [accessibility/accessible-error-announcement.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/accessibility/accessible-error-announcement.md) |
| Interaction latency and heavy content | [performance/identify-inp-causes.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/performance/identify-inp-causes.md), [performance/defer-rendering-heavy-content.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/performance/defer-rendering-heavy-content.md) |
| Hero/image loading priority | [performance/optimize-image-priority.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/performance/optimize-image-priority.md) |
| Motion and reduced motion | [ui-behaviors/motion.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/ui-behaviors/motion.md) |
| Browser-side defense | [security/security.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/security/security.md), [security/sanitize-untrusted-html.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/security/sanitize-untrusted-html.md), [security/trusted-types.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/security/trusted-types.md) |
| Browser privacy mechanisms | [privacy/privacy.md](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides/privacy/privacy.md) |

If the shortlist is insufficient, inspect the pinned directory or [README catalog with descriptions](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/README.md), choose matching descriptions and follow the exact guide path. With an already-authorized read-only checkout, `rg --files skills/modern-web-guidance/guides` and a bounded `rg` query provide local discovery without a new executable. Do not invent IDs. A missing topic calls for primary framework/platform documentation, not irrelevant guidance. If network/reference access is blocked, use the local canonical synthesis and report the exact support evidence still missing; do not certify a new API from memory.

**Check experimental gates without a CLI:** published guide Markdown may omit the metadata used by `retrieve`. For an uncertain/new API, open `guides/<category>/<id>/guide.md` in the [matching source revision](https://github.com/GoogleChrome/modern-web-guidance-src/tree/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/guides), inspect frontmatter `web-feature-ids`, and compare those IDs to keys in [origin-trials.json](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/features/origin-trials.json) and [volatile-features.json](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/features/volatile-features.json). A match requires the separately authorized experimental-feature decision; unknown metadata is not approval. For example, `html-setters` and `html-streaming-setters` are volatile in this revision even when a rendered streaming guide only says Limited. Confirm current official support as well: absence from an old registry is not proof of present stability. Neither reading the Markdown nor changing Baseline waives this boundary.

### Optional CLI, only after separate execution approval

The read-only link path above is the default. Runtime adoption first needs the artifact/integrity/provenance, privileges, configuration, network and rollback review in `std-dependency-supply-chain-baseline`; [the assessment](../references/modern-web-ponytail-adoption-assessment.md#execution-and-privacy-review) records the current risks. Do not install anything just because this example exists.

For a separately approved, integrity-verified **pre-provisioned** npm package `modern-web-guidance@1.0.1` with Node >=22, run from the intended project root after inspecting effective `.mwgrc`. An isolated tool path avoids changing the application's dependencies. Set `DISABLE_TELEMETRY=1` in the actual child environment before every command; do not rely on a shell profile being loaded.

```sh
DISABLE_TELEMETRY=1 node "<approved-tool>/node_modules/modern-web-guidance/skills/modern-web-guidance/modern-web.mjs" search "responsive data table"
DISABLE_TELEMETRY=1 node "<approved-tool>/node_modules/modern-web-guidance/skills/modern-web-guidance/modern-web.mjs" retrieve "responsive-table,accessibility"
```

In PowerShell, set `$env:DISABLE_TELEMETRY = '1'` in the isolated command process, then invoke that same quoted `node` script path. These are command templates, not execution evidence. No `@latest`, broad runner allowlist, package installation, `install/update/uninstall` or feature-opt-in command is part of this workflow. Never include customer/private context in a search query. Do not loosen Origin Trial/volatile-feature gates to force retrieval or implementation.

Only a broad authorized modernization/audit warrants `legacy-scan <explicit-source-path> --json` through the same approved entry point. Review every finding's keep/drop rubric, actual source and cross-file usage. Preserve deliberate fallbacks and third-party code; do not chase a zero count. A targeted change uses relevant guides and behavior verification, not a repository scan. If a scan justifies issues, deduplicate them and record reproducible evidence, affected scope, impact and fix; audit authority alone does not authorize editing.

## 3. Choose the minimum complete implementation

Apply the reuse policy: remove speculative work, trace the owning implementation and its consumers, compare the suitable canonical component, suitable platform/standard library, existing dependency and readable local code. Justify a new dependency/abstraction by a real unmet invariant or cost. Do not replace an adequate component just to use a native API, or keep an inadequate one merely to minimize the patch.

For each material capability record a compact decision: **need → source/guide → support evidence/date → essential or enhancement → adopted/retained/deferred → fallback → verification**. Reuse the existing task/PR evidence; no separate report is required for every attribute change. An incompatible suggestion is a reasoned rejection, not a mandate to weaken types, support or product behavior.

## 4. Integrate safely with the real framework and product

| Tempting shortcut | Required adaptation for the affected contract |
| --- | --- |
| Native dialog or declarative commands solve everything | Verify focus entry/return, Escape, keyboard, name/description and dirty/destructive states. While the modal is open, try reaching a visible background control with the keyboard and activating it with keyboard and pointer. Verify that focus stays out of the background and the action is blocked. Record those outcomes separately from the declared modal semantics. Use a ref and supported `showModal()` when appropriate; light-dismiss must not discard work. Feature-test the exact behavior and retain a usable fallback. |
| Hide table headers and generate CSS labels for mobile cards | Preserve true table headers/relationships, stable row identity, sorting/filter/count/export truth and keyboard actions. Prefer semantic table + bounded scroll if a card conversion has not passed the target assistive-technology checks. |
| Copy an imperative sortable-table example into React | Keep React as owner of managed DOM and sorting state, semantic buttons and `aria-sort`. Do not rearrange managed nodes behind the renderer; feature-detected transitions remain optional. |
| Add modern JSX attributes using blanket `as any` | Use supported framework types or a narrowly typed, tested wrapper/augmentation at the actual boundary; no disabled type checks or global weakening. |
| Browser APIs in shared modules or experimental streaming | Keep browser-only access behind the supported client lifecycle. Preserve SSR/hydration, stable IDs and CSP. Browser Declarative Patching/HTML streaming is not React/Next Suspense/RSC and is not implicitly approved. |
| Speculation Rules mean Next.js optimization | “Next page” means the next navigation, not the framework. Coordinate router prefetch; avoid speculative private/session-sensitive reads, mutation endpoints, duplicate analytics and unbounded server cost. |
| `content-visibility` replaces data/loading work | Use it only for suitable independent below-fold content; check layout, focus, tabbing and find-in-page. It does not reduce SQL/network work or substitute for a truthful skeleton. |
| Lazy-load everything or wait for all data before showing the view | Expose the usable shell/available sections, reserve real geometry, and use supported framework streaming where appropriate. After identity/tenant/role resolution, overlap only independent reads; bound/deduplicate requests and preserve per-section errors and cache isolation. |
| Browser sanitization/privacy guide supplies end-to-end safety | Context-sensitive escaping/sanitization and CSP/Trusted Types must fit SSR and real sinks. They do not replace authorization, RLS, tenant-aware cache keys, server validation or the legal/consent owner. Never render untrusted agent output as trusted HTML. |

Do not import unpinned CDN polyfills or copy node_modules files. Use a reviewed pinned dependency only if it is the best compatible solution; no automatic polyfill for an optional enhancement. Browser built-in AI, WebMCP and experimental features require their own authority/support/data review; custom product agents do not make them necessary.

## 5. Verify the whole affected behavior

Use `pat-risk-based-verification-matrix`, not a line count or single-test quota. At the relevant boundary verify:

- original failure and successful behavior, fallback/unsupported path, interruption and errors;
- Chromium/Firefox/WebKit as applicable to the declared matrix, plus real Safari/device/assistive technology when an engine proxy cannot prove the requirement;
- keyboard, focus/announcement, touch/reflow/zoom, reduced motion and long/localized content;
- production-like build, SSR/hydration and CSP without unexpected console/network errors;
- persisted/denied/duplicate outcomes for a connected form/tool using isolated authorized test data, not uncontrolled live submissions;
- matched before/after user-journey performance where a performance claim is made: cache/device/network/data/build, samples and adverse changes as well as gains.

If a supported dialog close path removes or replaces its opener, exercise
that path using the keyboard, including a same-label replacement when the
interface renders one. Record the actual focused element after dismissal.
Check where the next `Tab` goes and exercise the intended next keyboard
action. See `src-w3c-aria-apg`.

When an existing workflow reads the `returnValue` of a reused native
`dialog`, confirm once, reopen the same element and use each applicable
dismissal path. `close()` without a result can retain the previous value.
Observe the current action and the value read by the consumer separately.
Where dismissal requires an empty result, verify the workflow's initialization
or explicit dismissal result in that opening. See `src-whatwg-html-dialog-close-result`.

When an existing browser workflow uses `requestIdleCallback()` with a
timeout, exercise an ordinary idle callback and one invoked after the
timeout expires. Record `didTimeout` and `timeRemaining()` at callback
entry. A timeout can cause the callback to run with no idle time
remaining. Check which deferred work actually finished and what the user
can do next, including when the result is still pending. See
`src-w3c-idle-callback-deadline` sections 4.3 and 5.2–5.3.

When an existing image uses `loading="lazy"`, verify the viewport journey
with space reserved for the image. Record whether the request starts while
the image is far offscreen. Then navigate to it and check the loaded or
decoded image, the rendered result and the box before and after load.
In a controlled test, hold the response to check the pending box and
surrounding content.
An eager control can show a request before usable image data arrives.
Record the browser and viewport because the loading distance can vary.
See `src-whatwg-html-native-image-lazy-loading`.

Follow `pat-performance-budgeting` for field versus lab metrics. Record first useful content, interaction-to-content and server/query workload when they matter; a skeleton screenshot or passing LCP does not prove task responsiveness. Retain security, data, legal and product gates. Missing required support/runtime evidence leaves acceptance incomplete, even if unit tests and the upstream scan pass.

Close with the relevant guide/decision, meaningful adaptation, actual checks and gaps in the ordinary delivery record. Do not mandate a repetitive upstream-branded section or claim applying a guide improves every product. [Attribution and changes](../references/modern-web-ponytail-adoption-assessment.md#attribution-and-modifications) apply to this adapted guidance.
