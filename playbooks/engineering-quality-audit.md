---
id: pb-engineering-quality-audit
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - application-repositories
  - services
  - internal-consoles
  - public-websites
  - connected-products
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-w3c-wcag-22
  - src-webdev-core-web-vitals-thresholds
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Engineering Quality Audit — UX, UI, Performance, Security and Operations

## Purpose and boundaries

Use this Playbook for a cross-domain quality review or as the entrypoint to a focused quality discipline. It **orchestrates canonical owners**; it is not a second UI, security, privacy, performance or release Standard. A broad task means broad discovery, **not universal execution of expensive checks**. Determine relevant failure classes from the actual product, affected journeys, privileges, integrations and environment.

An **audit** is read-only. It may inspect code, local build artifacts, permitted evidence and authorized non-mutating environments; it does not itself authorize changing files, installing dependencies, running destructive tests, sending messages, creating issues, migrating data, deploying, spending money or changing third-party configuration. When the instruction separately says to fix, isolate and scope the fix; verify that no action is inferred from the advisory classifier. A compliance or risk assessment is not a declaration of legal certification.

The Handbook baseline is a quality floor. Product-specific design, operating context, browser/device contract, risk thresholds, budgets, claims and domain decisions remain local. Do not homogenize MelodIQ products into one generated-looking visual style. For an **authorized new or material internal-console redesign only**, the [visual direction catalog](../patterns/visual-direction-catalog.md) offers a scoped Glassmorphism starting candidate; Neumorphism and other directions remain selectable. Merely auditing or repairing one control is not permission to reskin a product.

## 1. Capture a reproducible review target

Record the shortest useful intake:

1. **Mandate:** read-only review, bounded fix, full authorized redesign or release decision; stop at the actual permission boundary.
2. **Subject:** repo/branch/merge base or commit and any dirty-tree delta; current deployed SHA/environment if relevant. Do not use `HEAD~1` as a universal review base.
3. **Product:** public marketing site, authenticated workspace, connected CRM, field/PWA, service/API, agent runtime or supporting tool; audience, tasks, critical user journeys, tenants and real devices/browsers.
4. **Contracts:** nearest `AGENTS.md`, local `DESIGN.md`, architecture/security/data decisions, relevant Handbook versions, tests and named product constraints.
5. **Evidence available:** implementation, rendered UI, design assets, telemetry, representative fixtures, CI outputs, authorized providers, remote environment and physical devices. Mark unknown/blocked sources explicitly.

Find the owning code and its entrypoints first. Use `search`, `tree`, `explain` and the repository route for inspect-first hints, then confirm actual imports, registrations, paths, data flow and consumers. An unresolved landmark is a prompt to inspect; absence of a path in the detector is **not proof** the control is absent. Pin source versions for the task; a fresh Handbook snapshot is not proof that a consumer repo has adopted it.

## 2. Select review domains by consequence

| Domain | Primary authority | Inspect and challenge | Evidence that can close relevant findings |
| --- | --- | --- | --- |
| **User experience / design quality** | [UI/UX Standard](../standards/ui-ux-quality-baseline.md), [Frontend Quality Review](frontend-quality-review.md) | Real user journeys, information hierarchy, terminology, task completion, navigation/focus continuity, errors, loading/empty/partial/success states, content stress, motion, material fit, authentic product identity, AI slop | Rendered before/after, task walkthrough and relevant UI/browser interaction checks, including narrow/mobile/desktop and theme variants |
| **Accessibility / responsive** | [UI/UX Standard](../standards/ui-ux-quality-baseline.md), [Mobile interactions](../patterns/mobile-responsive-interaction.md) | WCAG 2.2 AA target, semantic controls, keyboard, focus visibility/order/occlusion, naming, contrast, zoom/reflow, touch, reduced motion, dialogs/forms, screen readers where needed | Automated checks **plus** actual manual keyboard/rendered inspection and relevant assistive technology/device evidence; no scanner-only PASS |
| **Performance / resource cost** | [Performance Budgeting](../patterns/performance-budgeting.md), [Modern Web Workflow](modern-web-platform-workflow.md) | Critical path, LCP/INP/CLS, loading/hydration, JS/images/fonts, layout/paint/motion, API and SQL latency/fan-out, cache isolation, data shape, concurrency, bandwidth/server workload | Matched representative baseline/comparison, timings/distributions, query plans or traces as applicable; field ≠ synthetic proxy |
| **Security / abuse** | [Security and Identity](../standards/security-identity-baseline.md), [Security Review](security-review.md), [Supply Chain](../standards/dependency-supply-chain-baseline.md) | Assets and trust boundaries; authn/authz/tenant isolation, input/output injection, XSS/CSRF/SSRF/CORS/CSP, storage/uploads, secrets, session/token lifecycle, external calls, webhooks/replay, rate limits, dependencies | Relevant negative-path tests at enforceable server/data boundaries, config/secret scans and targeted manual/authorized provider verification; scanners alone do not prove security |
| **Privacy / data lifecycle** | [Privacy/Data Handling](../standards/privacy-data-handling-baseline.md); for Spanish client web [Public Legal/Trust](../standards/public-website-legal-trust-baseline.md) and [consent audit](spanish-client-website-privacy-consent-audit.md) | Data purposes/roles, consent and pre-consent network, analytics/PII leakage, exports/logs, photos/attachments, retention, erasure, demo/test isolation, external processors/transfers and legal-owner approvals | Trace real input → processing/storage → recipient → deletion; network/storage/role tests where material; unsupported legal or provider claims remain open |
| **Data, API and failure integrity** | [Architecture/Data](../standards/architecture-data-integrity-baseline.md), [Code Craft](../standards/code-quality-organization-baseline.md), [Testing/Release](../standards/testing-release-quality-baseline.md) | Schema changes, source of truth, stale/partial states, lost writes, async accepted/persisted/completed, idempotency, pagination, ordering, backfills, service/API contracts, retries and concurrency | Existing+upgrade fixtures, affected integration/contract tests, negative/recovery cases and real consumer behavior as required |
| **Reliability, observability and release** | [Production Operability](../standards/production-operability-baseline.md), [Quality/Release Review](quality-release-review.md), [Production Readiness](production-readiness-review.md) | Runtime errors, alert usefulness, timeouts, external failures, capacity, environment isolation, CI evidence/cost, safe rollback, actual deployment identity | Attributable logs/metrics/traces and authorized smoke/recovery checks; distinguish code/build, deployed target, migration and live environment |

The table is a **menu, not an every-push gate**. A UI-only typography fix may need a small render/keyboard pass, not a database, penetration test and Production deploy. A broad security/privacy review may need the server/data boundary even if its user-visible symptom is a broken button. PWA/mobile, marketing claims/search, agent tooling and specific regulated data activate their existing specialized owners when present.

## 3. Walk the real journeys and threat paths

For each relevant domain and critical user journey:

1. State the expected user or system outcome and its **failure mode**, not just the component name.
2. Trace `entrypoint → ownership → authorization/consent → data/service → response → UI/consumer` **only through the boundaries actually involved**. A synthetic fixture cannot prove a live provider or a real tenant behaves identically.
3. Inspect happy, empty, pending, delayed/partial, invalid, denied, replay/duplicate, error, cancellation, retry and recovery states that are materially possible. Include cross-role/cross-tenant, older data and interrupted transitions where they determine correctness.
4. Select the [risk-based verification matrix](../patterns/risk-based-verification-matrix.md): cheapest reliable evidence, environment, cost/cadence, gate status. Prioritize deterministic tests; use browser/device/remote checks when they add distinct evidence. Respect monetary and environment permissions.
5. Compare baseline and candidate under representative content, data size, cache and hardware. A skeleton, visual screenshot, green linter, low Lighthouse score or presence of a security header is not by itself proof of the user journey or threat control.

For material frontend reviews, follow [Frontend Quality Review](frontend-quality-review.md) for task hierarchy, nine-pass Unslop diagnosis, states, responsive/zoom and actual rendered verification. A design audit can identify systemic visual issues **without changing the composition**. A requested reconstruction is a separate authorized action.

For material security reviews, use the [Security Review](security-review.md) to select **applicable** OWASP ASVS 5.0.0 areas by the threat boundary; never claim the entire catalog was checked from a small scan. For privacy, data collection/storage/retention and provider decisions require actual product facts and appropriate legal-owner approval.

## 4. Record findings as actionable evidence

Deduplicate by **same root cause + affected owner/contract + failure condition**, not by identical screenshot or phrasing. The report/issue for each material finding needs:

- **Where:** repository, exact path/route/entrypoint, relevant commit and environment.
- **Who/what:** actor, device/browser/tenant, affected journey and invariant.
- **How to reproduce:** concrete steps/input, precondition, expected vs observed, failure evidence, tool and date; redact credentials and private customer data.
- **Impact:** user/business/security/privacy consequence, justified severity, scope and confidence; distinguish observed fact from inference.
- **Authority:** canonical Handbook owner plus relevant local contract, without making an advisory source mandatory.
- **Repair:** minimal viable correction or bounded design reconstruction, verification needed, known unknowns and a stable dedup key.

Classify `Critical`, `Important`, `Minor` by likely consequence, not cosmetic count. Findings may be security-sensitive: avoid publicly exposing an exploit, secret, private identifier or unsafe reproduction material in an issue. Route disclosure and visibility according to repo policy. A read-only audit records findings; **issue creation requires existing independent authority**, such as the owner's recurring compliance-issue mandate. In an authorized periodic scan, add only new actionable/deduplicated findings; if there are no new issues, remain silent as requested. Do not manufacture issues for clean runs.

## 5. Separate review, correction, closure and publication

**Audit outcome:** enumerate observed evidence and reproducible findings; distinguish `PASSED`, `FAILED`, `NOT_RUN`, `BLOCKED`, `NOT_APPLICABLE` per relevant gate. An empty finding list is *not* proof that all domains passed.

**Authorized fix:** trace affected consumers; add a meaningful reproducer, correct the owning layer, verify the actual failure class and regressions, then update evidence for that candidate revision. Do not silently expand into architecture, data, branding, law, third-party providers or release.

**Quality closure:** reread all material findings against the final tested bytes; attach before/after evidence when it changes the acceptance decision. Report open, deferred, blocked or intentionally scoped exclusions. Do not claim independent review from the author's own read.

**Release:** only if independently authorized, apply [Quality and Release Review](quality-release-review.md) and target-specific readiness gates. Git merge, successful build, Preview, SQL migration, deployed SHA, server logs, production smoke and a physical-device pass are separate proof states. No new metered CI job or external payment is implied.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "quality-audit-intake",
      "type": "decision-question",
      "text": "For a holistic quality review, pin the real repo/revision, user journeys, local authority, relevant domains and readable evidence. Review is read-only; select UX/a11y/performance/security/privacy/data/reliability owners by actual risk, not a global checklist or permission to fix.",
      "source": "pb-engineering-quality-audit",
      "covers": ["quality-coverage"],
      "activate_when": ["archetype:quality-audit"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 100
    },
    {
      "id": "quality-audit-closure",
      "type": "verification",
      "text": "For each relevant quality domain, attribute actual evidence to tested revision/environment, distinguish passed/failed/not run/blocked/not applicable, deduplicate actionable root causes and retain residual risk. Missing rendered, server, remote or native proof remains incomplete, not PASS; issue publication requires separate authority.",
      "source": "pb-engineering-quality-audit",
      "covers": ["quality-coverage"],
      "activate_when": ["archetype:quality-audit"],
      "force": "must",
      "phase": ["verification"],
      "priority": 100
    }
  ]
}
```
