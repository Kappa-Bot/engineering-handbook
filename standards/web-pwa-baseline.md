---
id: std-web-pwa-baseline
kind: standard
status: active
owner: engineering
version: "0.2"
applies_to:
  - installable-web-surfaces
  - pwa-capable-web-apps
sources:
  - src-w3c-appmanifest
  - src-w3c-service-workers
  - src-w3c-wcag-22
  - src-w3c-cssom-view
  - src-w3c-css-env
last_verified: 2026-10-10
review_due: 2027-01-10
---

# Web / PWA Quality Baseline

## Purpose

Define what "PWA" quality means when an installable or progressively enhanced web-app surface is intentionally part of the product.

**PWA is not mandatory for every website or every route.** A manifest, service worker, offline cache, push channel or install prompt MUST NOT be added merely to satisfy a technology checklist.

The baseline is capability- and outcome-driven:

```text
surface that benefits from app-like use
        ↓
explicit install/scope decision
        ↓
manifest + platform behavior as needed
        ↓
optional service-worker capabilities only when justified
        ↓
truthful lifecycle/offline/update UX
        ↓
browser + native-device verification where required
```

## 1. Decide the installable surface first

Before adding PWA metadata/capabilities, define:

- which surface or route family is intended to be installable;
- the user/job that benefits from installation;
- the launch destination;
- whether the public site and private application should share or separate install behavior;
- which capabilities, if any, need service-worker/background behavior.

Prefer the **smallest coherent installable scope that provides product value**.

A public marketing site and an authenticated operations app hosted on the same domain MAY intentionally have different PWA behavior. Do not advertise installation on unrelated public surfaces solely because an admin/app surface is installable.

## 2. Manifest contract

An intentional installable surface MUST have a deliberate Web App Manifest contract appropriate to the product, including the applicable:

- stable application identity (`id`);
- launch URL (`start_url`);
- scope;
- name/short name;
- icon set;
- display mode;
- theme/background metadata where useful.

Manifest values MUST correspond to real routable product surfaces.

Shortcuts SHOULD be limited to high-value, stable destinations. Do not expose internal/debug/demo routes as launcher shortcuts.

Do not lock orientation by default. An orientation restriction requires a real product/hardware reason and MUST be validated against the affected device workflows.

If installed icon/brand changes are operationally important and launcher/browser caching can make stale identity materially confusing, use explicit brand/build versioning or equivalent cache-busting provenance rather than assuming launcher assets refresh immediately.

## 3. Installation is not security

Installation MUST NOT be treated as authentication, authorization, device trust, tenancy or secure storage.

An installed web app keeps the web application's security model unless the product explicitly adds other controls. Public/mock/demo surfaces MUST remain truthfully labeled regardless of installation state.

Install UI SHOULD communicate only what installation actually changes (for example launch convenience or standalone display) and MUST NOT imply unsupported offline/security capabilities.

## 4. Service workers are optional capabilities

The Web App Manifest and Service Workers are separate platform mechanisms. Do not add a service worker solely because the product is called a PWA.

Introduce a service worker only when one or more concrete capabilities justify its lifecycle/operational complexity, for example:

- intentionally offline-capable reads/workflows;
- controlled asset/runtime caching;
- background/push capabilities;
- request handling that materially improves the product.

If a service worker exists, its install/activate/update behavior, scope and cache lifecycle become production behavior and MUST be tested accordingly.

A no-op or fake `fetch` handler is not a quality feature.

## 5. Connectivity contract

For product features affected by connectivity, classify the behavior explicitly when it matters:

- **offline-capable** — intended to complete without network;
- **cached/read-only** — prior data/shell remains useful but mutation requires network;
- **network-required** — action cannot truthfully complete offline.

Do not silently queue or report success for a mutation unless the product has an explicit durable synchronization/reconciliation contract.

An offline fallback SHOULD preserve useful orientation and recovery actions. A generic "you are offline" page is insufficient when the product can safely expose cached/read-only value, and unnecessary when no offline capability is promised.

## 6. Update and build provenance

Installed apps can stay open longer and can expose stale assets/data more visibly than ordinary short browser visits.

When stale-version ambiguity can affect support, demonstrations, branding or release confidence, expose concise build provenance such as app version/commit/build time in an appropriate support/settings location.

If a service worker controls updates:

- define how a waiting/updated worker reaches users;
- avoid silently mixing incompatible shell/data versions;
- preserve user work across reload/update boundaries;
- verify the old→new lifecycle, not only a clean install.

Do not add a manual "update" control unless it is connected to a real update lifecycle the product can explain and test.

## 7. Responsive installed-shell behavior

Installed display modes do not remove responsive/accessibility obligations.

The installable surface MUST still meet `std-ui-ux-quality-baseline`, including zoom/reflow, focus and target-size requirements.

For edge-anchored controls:

- respect CSS safe-area environment variables where device geometry requires them;
- ensure fixed/bottom navigation does not obscure focused/editable content;
- use the visual viewport when the virtual keyboard changes the actually usable area and the UI behavior depends on it.

Apply `pat-mobile-responsive-interaction` for keyboard, safe-area, gesture or camera-heavy installed workflows.

## 8. Browser/OS limitations are part of truthfulness

Installation prompts, launcher icon refresh, standalone chrome, update timing and background capabilities vary by user agent/OS.

The product MUST NOT claim that a browser automation check proves native launcher/installed behavior that was not actually tested.

When launcher identity, installed display, virtual keyboard, camera permissions or OS-level behavior is release-critical, verify on representative real devices/platforms or record the gate as **not run**.

Automation and emulation are valuable regression layers; they are not a substitute for physical-device certification when the requirement itself is physical/OS-specific.

## 9. PWA verification

The verification plan SHOULD be derived from the capabilities actually claimed.

For a manifest-only/install-shortcut surface, verify at least:

- manifest route/metadata and intended scope;
- launch URL resolves correctly;
- public/private surfaces expose installation only where intended;
- icons/assets resolve and use the intended identity;
- installed/standalone layout remains usable at representative device sizes.

If service-worker/offline capabilities exist, additionally verify:

- registration scope;
- install/activate/update lifecycle;
- cached/offline behavior by feature class;
- mutation/reconciliation semantics;
- stale/upgrade behavior;
- cache invalidation/data-safety boundaries.

For material visual PWA acceptance, apply `pat-visual-evidence-integrity`.

## 10. Release discovery and update delivery

An app installed for daily operational use SHOULD **discover** updated builds in the background when the page is opened, revisited, focused or reconnected. Update discovery is not equivalent to immediately reloading.

**Low-latency, low-cost version authority:**

- Serve a tiny, tenant-data-free `GET /api/.../version` that returns a validated immutable **build** identity. `Cache-Control: no-store` applies. Never query business tables, sessions or the tenant branding database merely to determine whether source code changed.
- Check on first visible load, then focus, page-show, visibility restoration and reconnect, with a bounded cooldown (typically minutes, not seconds). Coalesce simultaneous probes, avoid starting a cooldown or a request while offline/hidden, and ignore failed/malformed/non-200 responses.
- Distinguish a **build update** (JS/CSS/runtime contract) from a **brand/icon revision** (stable mark bytes may change independently). Do not encode tenant identity into a build version or make a logo-only change force immediate application reload.
- A rollback to an earlier release is also a version mismatch: do not rely on a lexicographic or numeric greater-than comparison of Git SHAs.
- A build-specific query/URL identity may be used on explicit refresh to bypass stale HTML caches. Do not append sensitive tokens or entire business state to the URL.

**Apply safely, never silently discard work:**

1. Show a quiet, accessible, nonblocking update indicator with a clear `Actualizar` action and a deferral affordance if the user is actively working.
2. Detect changed controls (inputs, checkboxes, radio, selects, textareas, file attachments) and provide **explicit product-owned dirty/busy markers** for controlled React editors, pending mutations and in-memory drafts that are not expressed by DOM form defaults.
3. If a refresh may lose work, ask for confirmation in a real modal dialog with a name, focus management, Escape, keyboard loop, viewport-safe geometry and distinct `Seguir editando` / `Descartar y actualizar` actions. No forced reload on a mutation promise, payment, upload, approval, draft or unsaved Job.
4. Automatic update **application** MAY occur at a verified safe waypoint (for example an idle dashboard) only when visible, online, free of dirty/pending state and user inactivity has met a deliberate threshold. Active task routes require user choice. If the application cannot reliably prove the safe point, offer the update rather than guessing.
5. Apply a new worker independently of the page only if the runtime/data compatibility contract supports it; do not make `skipWaiting()` or `controllerchange` silently overwrite the currently loaded UI's unsaved state.

**Negative tests are essential:** rejected probe, offline/hidden tab, concurrent focus events, rollback, malformed version, dirty form, contenteditable, pending mutation, keyboard-only confirmation and theme/motion/320px reflow. Successful TypeScript/unit checks alone do not prove the installed old→new update journey.

## 11. Installation UX is platform-specific

An install card SHOULD distinguish **installed**, **install prompt available**, **manual instruction**, **requested but not confirmed**, **dismissed**, and **error** states.

- `beforeinstallprompt` is not universally available; manual browser-menu instructions must remain useful when it never fires.
- iPhone/iPad, Android, Windows, macOS and Linux use different controls. Detect the platform conservatively and show a short primary pathway, with other device instructions behind progressive disclosure.
- Do not label the app **installed** immediately after a user accepts a browser prompt: rely on `appinstalled`, standalone display mode or other evidence. An accepted `userChoice` with no install event may mean a requested/unknown state.
- Explain the real value (launch from home screen/desktop, standalone chrome) without suggesting offline access to protected business data, stronger authorization or background sync that does not exist.
- Installation is user-initiated; avoid forced modals, repeated banners, gamified rewards or blocking workflow gates. Preserve focus, legible instructions, reduced motion and 44px-class controls where sensible.

## 12. CacheStorage / service-worker threat model

For an authenticated or multi-tenant product, the service worker is a **privileged persistence boundary**. The cache policy MUST be explicit per response category; URLs alone are insufficient for general authenticated content.

| Request class | Default | Required qualification |
| --- | --- | --- |
| Versioned build assets such as `/_next/static/` | Public cache permitted | Same origin, safe status/content-type and verified immutability; cache-first can improve return-visit latency |
| Tenant logo/favicon/PWA/public art | Tenant/build scoped, public cache permitted | Do not cache another tenant's bytes in a shared namespace; review URL and icon version |
| Offline informational shell | Precache deliberately | Fixed, nonpersonalized noindex page; no authentication or business-data claims |
| Authenticated app HTML, server components, Jobs, customer documents, reports, session/auth APIs | **Network-only** | Never infer safe caching because the request is GET; don't put private payloads or access links into CacheStorage |
| Write actions, uploads, payments, commands, approvals | **Network-only** | No fake queued success or implicit background replay |
| Published member/customer content explicitly designed for offline reads | Only under a separate validated contract | Require server trust marker, tenant/user partition, no-store/privacy review, logout/revocation purge and a repeatable negative test |

A safe shell-only worker SHOULD:
- constrain control scope (e.g. private `/app/` instead of an entire marketing domain);
- use a namespaced cache key with **policy version + tenant/identity + immutable build ID**;
- verify same-origin, GET, public response success, disallow `private`/`no-store`/`Set-Cookie` responses and avoid broad `/tenants/` or `/api/` prefix matching;
- cache hashed static resources separately in behavior from stable-URL logos, where a fresh network response should be preferred;
- serve **network-first** authenticated navigation and show a static offline explanation only on network failure, without caching the private HTML itself;
- delete only known obsolete caches that this worker owns, not caches of other tenants/apps on the origin;
- keep worker registration failures additive: authenticated online workflows must still function normally.

Cache names are not an authorization boundary. Tenant permission checks remain server-owned, and a distinct tenant-origin/scope must be chosen for genuine multi-tenant sessions rather than relying on a query string for isolation.

## 13. Installed-app polish and connectivity truth

Use app-like feedback as **operational clarity**, not decoration:

- A connectivity indicator can use `navigator.onLine` as a best-effort *hint*, never as proof the API or database is reachable. Disappear automatically on reconnect without reloading active work; a failed command still needs its own visible retry/error state.
- A slow route should show local progress/skeleton feedback and preserve navigation/context; do not globally freeze the shell for one report request.
- Standalone/mobile shell: handle safe-area insets, bottom navigation versus keyboard/visual viewport, native focus, correct scroll restoration and meaningful offline fallback.
- Notifications for updates/connectivity should not take over the screen, hide controls or create duplicate `aria-live` noise. A blocking confirmation is justified only when the user deliberately selects a destructive refresh.
- Shortcuts and icon titles should match the real private product. Host, manifest, Apple icon, maskable icon and exported logo must resolve the **same tenant identity**.

## 14. Icon and launcher refresh policy

Persisted platform launchers often cache icons beyond HTTP revalidation. Corrected HTTP responses do **not** prove that an installed launcher has refreshed.

- Use one tenant-owned icon source and separate transparent favicon, Apple touch, regular square and maskable safe-area derivatives.
- Version icon URLs with a stable **asset digest/revision** (for example `?v=<approved-asset-revision>`) when bytes materially change. Build version and artwork revision are different dimensions.
- Manifest responses can be no-store while a platform still retains an old launcher. Do not promise forced replacement or delete the user's installation; provide reinstall instructions when an OS cannot be made to refresh.
- Keep user-visible app name as text/manifest metadata, not baked into the monogram unless a distinct approved logo variant requires it.
- Preserve minimal tenant prefixes and validate cross-tenant URLs; a per-tenant static path by itself is not permission enforcement.

## 15. Operational release checklist

For any service-worker/manifest/update change, record on **the exact source/deployment**:

1. Version endpoint: schema, cache headers, **zero provider/tenant business reads**, cooldown/coalescing and rollback handling.
2. Static worker: registration scope, worker URL identity, cache namespace, allowed requests, no-store/private denials, install→activate→cleanup and offline navigation. Tests must prove that session/tenant/user data cannot accidentally be cached.
3. Update UI: dirty form and non-form editor, pending commands, keyboard/Escape/focus, responsive modal at 320/390px and reduced motion, deferral and safe idle updates.
4. Installation: no manifest on unrelated public surfaces, real manifest metadata, icon sizes/masking, prompt/manual/dismissed/accepted/installed behavior, platform instructions.
5. Reconnection: route remains usable online if SW registration fails, offline indicator is truthful, no phantom write-success or playback promise.
6. Host release: immutable commit/version → CI → Vercel/host READY and mapped canonical alias → public `/manifest`, icon and health fetches → authenticated private shell smoke **only with legitimate sessions**.
7. Physical platform: Android/iOS installed launch, icon cache update, keyboard, safe-area and navigation as applicable. If not actually run, mark **NOT RUN**. No browser emulation success substitutes for OS certification.

**Representative internal evidence (not universal source authority):** ChurchOS `main@82289cad369df6cdc9415ab307335a5b8213d2a6` has a background version watcher, dirty-form confirmation, device-guided installation, tenant-scoped member offline policy and dedicated install E2E. Agurto Ops `main` as inspected 2026-10-10 provided a private scoped PWA, offline shell and version watcher but required stronger dirty-modal, platform/install and tenant-cache controls. Copy the generalizable behavior, **not** ChurchOS member data-offline rules into a private operations CRM. These are source audits, not independent physical-device acceptance.

## 16. Non-goals

This Standard does not require:

- a service worker;
- offline-first architecture;
- push notifications;
- background sync;
- a custom install banner;
- a particular PWA library/plugin;
- one manifest for an entire domain;
- portrait-only behavior;
- pretending native-device validation occurred in CI.

Add those only when product value and verified behavior justify them.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "pwa-installable-surface-decision",
      "type": "decision-question",
      "text": "Which coherent route surface benefits from installation, what launches, and which PWA capabilities are actually justified?",
      "source": "std-web-pwa-baseline",
      "covers": ["compatibility"],
      "activate_when": ["capability:pwa", "archetype:pwa-capability-change"],
      "force": "must",
      "phase": ["planning"],
      "priority": 82
    },
    {
      "id": "pwa-connectivity-contract",
      "type": "decision-question",
      "text": "Classify connectivity-sensitive behavior as offline-capable, cached/read-only, or network-required and define synchronization semantics before reporting offline mutation success.",
      "source": "std-web-pwa-baseline",
      "covers": ["availability", "data-loss"],
      "activate_when": [],
      "activate_all": ["capability:pwa", "operation:mutation"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 90
    },
    {
      "id": "pwa-native-evidence-boundary",
      "type": "verification",
      "text": "Do not infer native launcher, installed-shell, virtual-keyboard, camera, or OS behavior from browser automation; verify representative devices when release-critical or record the gate as not run.",
      "source": "std-web-pwa-baseline",
      "covers": ["compatibility", "accessibility"],
      "activate_when": ["capability:pwa", "archetype:pwa-capability-change"],
      "force": "must",
      "phase": ["verification"],
      "priority": 95
    },
    {
      "id": "pwa-service-worker-only-for-capability",
      "type": "constraint",
      "text": "Do not add a service worker merely as a PWA badge; its lifecycle and caches become production behavior only when a concrete capability justifies them.",
      "source": "std-web-pwa-baseline",
      "covers": ["availability"],
      "activate_when": ["capability:pwa"],
      "force": "must-not",
      "phase": ["planning", "implementation"],
      "priority": 65
    }
  ]
}
```
