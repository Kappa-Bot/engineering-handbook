---
id: ref-platform-core-performance-security-handoff-2026-10-10
kind: reference
status: active
owner: engineering
version: "0.2"
applies_to:
  - engineering-handbook
  - platform-core
sources: []
last_verified: 2026-10-10
review_due: 2027-01-10
---

# Platform Core: source integration and unreleased security handoff (2026-10-10)

> **Source-only integration completed 2026-10-10.** The owner's earlier pause
> was superseded for Git/source integration, not for commercial hosting, CI,
> live customer data, MCP, WAF, cron or production release. This is a
> non-normative dated evidence handoff, **not** a passing full test suite,
> independent security acceptance, or a deployed version. No background
> monitoring or scheduled work is implied.

The Engineering Handbook is public. This entry intentionally contains **no
secrets, provider/project IDs, private tenant details, operational IPs, access
tokens, exploitable configuration values, or unpublished vulnerability specifics**.
The private Platform Core repository owns its exact commands, settings,
provider observations and release decisions. Do not duplicate them here.

## Canonical locations and provenance

- **Consumer:** [Kappa-Bot/b2b-platform](https://github.com/Kappa-Bot/b2b-platform)
  (private). Its `AGENTS.md`, security contract, active completion plan and
  operations runbook take precedence for repo-local execution.
- **Previous live Production baseline:** source
  [`55c4bc1a`](https://github.com/Kappa-Bot/b2b-platform/commit/55c4bc1ae6ba8e1477cb1c2cdd381d85e959eea5)
  was the latest observed READY deployment. This is not a claim about any
  subsequent provider configuration.
- **Integrated repository source:** [PR #87](https://github.com/Kappa-Bot/b2b-platform/pull/87)
  merged the prepared performance, security and official MelodIQ Systems v8
  identity on `main`. [PR #88](https://github.com/Kappa-Bot/b2b-platform/pull/88)
  preserved the standalone bodyless HTTP fix's ancestry and retired its
  temporary branch. Exact final source:
  [`1fb472a8`](https://github.com/Kappa-Bot/b2b-platform/commit/1fb472a810e2b9795aba1840f1937e6aea793aee).
  Repository branch readback shows only `main` and `qa`, zero open PRs.
- **Historical original observation:** the feature source
  [`d0851c2d`](https://github.com/Kappa-Bot/b2b-platform/commit/d0851c2d668c42339f4c941c013fde00971297e4)
  and standalone HTTP fix
  [`f55587de`](https://github.com/Kappa-Bot/b2b-platform/commit/f55587de701916a53c0ec3e4caed96a0eba7a669)
  remain accessible by immutable commit. Avoid applying either a second time.
- **Detailed private operator notes:**
  [Platform Core abuse-protection runbook](https://github.com/Kappa-Bot/b2b-platform/blob/d0851c2d668c42339f4c941c013fde00971297e4/docs/operations/platform-core-abuse-protection.md),
  [Core operating runbook](https://github.com/Kappa-Bot/b2b-platform/blob/d0851c2d668c42339f4c941c013fde00971297e4/docs/operations/runbook.md),
  [canonical verification](https://github.com/Kappa-Bot/b2b-platform/blob/d0851c2d668c42339f4c941c013fde00971297e4/docs/development/testing.md).
  Check the *latest current* versions when resuming; the pinned links preserve
  this handoff's evidence.

## Source integrated, NOT deployed or independently accepted

| Area | Prepared change | Boundary that must remain intact |
| --- | --- | --- |
| Data reads | Request-scoped deduplication, smaller authorized directory/summary read shapes, deferred secondary probes and bounded search | No cross-user or cross-tenant persistent authorization cache |
| Navigation | SPA transitions, demand-loaded customer/runtime/commercial sections, visible loading and pending feedback | Route-level authority stays on the server; never treat a navigation hint as a grant |
| Mutations | Remove duplicate full-page refreshes when the canonical receipt and targeted authoritative read suffice | Preserve idempotency, current-state/version checks, support scope and audit; re-read when a mutation affects other records |
| DB/region | Proposed closer compute region; reduced nonessential diagnostic writes and public readiness probe fan-out | Measure actual cold/warm latency and pool effects before rollout; never assume a configured region is the running one |
| API ingress | Bound request URL, header and streamed body sizes; reject invalid input before expensive initialization | Preserve valid uploads, signed callbacks, explicit errors, Fastify parsing, and fail-closed authorization |
| Abuse controls | Per-instance, verified-principal throttling and explicit retry feedback | Not a distributed WAF quota; do not rate-limit service providers with arbitrary human/browser-IP budgets |
| Response safety | HTTP bodyless-status handling, cache-control and conservative response security headers | Retain authentication/OAuth, signed webhooks, service identity and no-secret-logging behavior |

The integrated source includes code and test declarations, **not evidence
that these changes work in production**. The main source merge triggered
two unexpected Vercel production-target builds even with `[skip ci]`;
both were promptly canceled and read back `CANCELED`. The previous
observed READY deployment remained on the older source. No migration,
provider WAF activation, scheduled job or production customer mutation
was performed through this source integration. Corporate branding uses
the exact approved restricted v8 raster derivatives, verified 8/8 by
SHA-256, not any invalidated Orbit or reconstructed SVG logo.
Canonical brand authority: [MelodIQ Systems DESIGN](../brands/melodiq-systems/DESIGN.md).

## Unverified / blocked gates at the pause

- **NOT RUN:** the Core repository's one canonical `pnpm check`, full typecheck,
  lint, production build, real-PostgreSQL integration, Playwright journeys, and
  independent security review on the final prepared HEAD. Added regression
  cases were authored but not executed; reconcile the repository's hard case
  ceiling before claiming the gate.
- **NOT MEASURED:** before/after p50/p95 user navigation and API latency,
  database round trips, query count, cold starts, request retries and memory
  pressure. No percentage improvement claim is warranted.
- **NOT VERIFIED:** hosted compute placement, real browser/device accessibility,
  large valid asset requests, current provider quotas/costs, and production
  compatibility of the complete change set.
- **EDGE RATE LIMIT NOT ACTIVE FROM THIS WORK:** attempts to inspect/stage a
  project-specific firewall rule could not be completed through the provider
  connection. Provider-managed baseline mitigation and separately configured
  edge quotas must not be conflated. Details are retained in the private Core
  runbook. Do not overwrite unknown firewall configuration to force success.
- **READ-ONLY DATABASE ADVISORIES:** findings exist but are not proven hot
  queries or an authorization to change extensions, subscription tiers or
  dozens of indexes. Use actual plans/telemetry and the private runbook.

## Resume sequence — only if the owner reopens the task

1. Re-read current Handbook Governance/Policy, Core `AGENTS.md`, the Core
   operating/security docs and the owner-imposed integration/release pause.
   Reconcile changed Git HEADs and competing work before editing; do not
   cherry-pick or merge an unreviewed change.
2. **Verify before merging:** run the exact consumer repo canonical check on
   the final commit, including applicable negative tests for authN/authZ,
   tenant isolation, idempotency/replay, HTTP body limits, legitimate uploads,
   signed callbacks, OAuth, `429` and `Retry-After`, and browser accessibility,
   loading and SPA navigation. Count executed cases rather than files.
3. **Measure before claiming performance:** compare like-for-like route/data
   volume, warm/cold state, p50/p95 and server/database call counts, baseline
   versus candidate. Investigate N+1 and service fan-out without bypassing RLS.
4. **Establish provider evidence:** verify region, pool/connections, free-tier
   allowance and exact firewall capabilities through the current authorized
   project account. Respect the zero-incremental-cost ceiling. Do not add a
   database write/read per request merely to implement rate limiting.
5. **Stage abuse rules separately:** log-only, narrowly scoped candidate
   rules at the actual edge; inspect legitimate traffic and false positives.
   Protect service runtimes, provider signatures, jobs and auth paths with
   their own semantics. Promote to enforcement only after scoped review and
   an explicit owner release decision. Never assume per-worker counters are
   distributed or turn on blanket Attack Mode as routine configuration.
6. **Controlled release, if authorized later:** satisfy the consumer's
   CI/PR/main, source provenance, migration, provider and deployment gates;
   prepare rollback; deploy a verified revision; test real admin/API behavior
   and failure/abuse signals. Provider changes and application releases have
   separate approvals and evidence. No tenant lifecycle, commerce, cron job
   or production data mutation is implied.

**Current state:** The feature and standalone fix refs were retired after
merging; preserve their immutable commits and private Core runbook as evidence.
Full consumer `pnpm check`, independent UX/security review, lawful commercial
hosting, intentional release, MCP/Auth and real ChurchOS/COGOP integration
are still gated. This reference does not create an automation or authorize
production deployment.

## Candidate reusable lessons (not promoted to a standard)

- Read shapes and authorization are separate: make ordinary navigation
  bounded, but keep every protected operation under current canonical access.
- Load expensive secondary views only when requested and reconcile a mutation
  at the narrowest proven authoritative scope; avoid silent stale success.
- Enforce inexpensive input budgets before costly dependencies; edge,
  per-process and authenticated-principal rate limits are distinct layers.
- Prove security/performance changes with real negative paths and comparable
  field or hosted measurements before promoting them to stronger Handbook
  guidance.

Related Handbook guidance: [performance budgeting](../patterns/performance-budgeting.md),
[security review](../playbooks/security-review.md),
[production readiness](../playbooks/production-readiness-review.md),
[verification truth](../policies/verification-definition-of-done.md).
