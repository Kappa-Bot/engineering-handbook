---
id: std-web-pwa-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - installable-web-surfaces
  - pwa-capable-web-apps
sources:
  - src-w3c-appmanifest
  - src-w3c-service-workers
  - src-w3c-wcag-22
  - src-w3c-cssom-view
  - src-w3c-css-env
last_verified: 2026-08-15
review_due: 2026-11-15
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

## 10. Non-goals

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
