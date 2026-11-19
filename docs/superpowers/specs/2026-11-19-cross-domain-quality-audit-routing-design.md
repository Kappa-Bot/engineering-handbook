# Cross-domain quality audit and routing — design

Date: 2026-11-19. Status: accepted by the owner's standing instruction to implement the same Handbook consolidation across UX, UI, performance, security and adjacent review disciplines without repeated confirmation.

## Intent

Make quality review an inspectable and reliable first-class Codex workflow. Today a prompt such as `Audita la seguridad y privacidad de la app` produces no relevant archetype or risk; `Revisa el rendimiento de SQL y el dashboard` can prioritize UI without locating the database or performance evidence. The canonical standards are substantial but not consistently reachable from prompts, repository landmarks, context phases, the knowledge tree or portable entrypoints.

The intended consumers are Codex reviewing MelodIQ/Kappa-Bot public sites, internal consoles, connected CRMs, agentic products, services and integration boundaries. A review must produce actionable, scoped findings and truthful evidence, without assuming every project uses the same aesthetic, stack, data model, performance budget or hosting provider.

## Goals and acceptance

1. One auditable entrypoint for an **overall quality audit** and focused routes for **UX/UI**, **accessibility**, **performance**, **security**, **privacy** and **production/reliability**. Combine them when a prompt spans domains; avoid treating UI as the owner of SQL, security or privacy.
2. Review requests remain read-only. Classification and context selection are advisory, never edit, issue-creation, deployment or provider authority. Explicit separate fix instructions retain their own scope, even when joined with a review.
3. Codex finds the actual owning code/config/test/evidence before judging. If a file/credential/browser/remote environment is unavailable, report a missing gate, not a green result.
4. Put baseline rules in their canonical Standards/Patterns; put the review sequence, risk matrix and finding format in a focused Playbook. Do not clone rules or install domain skills for an existing topic.
5. Make the compiled context phase-specific: planning asks what to inspect, implementation constrains authorized fixes, verification demands actual evidence. A broad audit activates domain checks without forcing a redesign, package upgrade, migration or universal CI/browser run.
6. Make ES/EN discovery and routing testable through real consumer outputs, negative clauses, docs-only prompts, mixed domains, path-only changes, phase capsules and a portable installed snapshot.
7. Preserve MelodIQ's existing visual direction catalog (scoped internal-console glass candidate; alternative Neumorphism/solid) and existing PWA, modern-browser, legal, architecture, supply-chain, observability and release owners.

## Non-goals / anti-goals

- No changes to consumer product repositories, CI triggers, production deployments or scheduled recurring audits in this task.
- No global numeric performance, visual score, universal OWASP checklist, universal UX component library or arbitrary count of renders/tests.
- No consent/retention/legal approval manufactured from generic engineering defaults; public Spanish web obligations remain with the existing legal/trust baseline and specialist playbook.
- No automatic creation of GitHub issues or modification in a read-only audit, although authorized recurring workflows may deduplicate findings into issues.
- No model/agent invocation change or new paid service.

## Approaches considered

1. **Add a giant quality checklist to global AGENTS.md.** Easy to see initially but duplicates authoritative standards, occupies permanent context and cannot route by task. Rejected.
2. **One new catch-all quality Standard.** Might describe domains but competes with existing UI, security, performance, data and release authorities; poor change ownership. Rejected.
3. **One orchestration Playbook plus precise registry routing and small owner-level gaps.** Keeps normative ownership, makes tasks searchable and preserves efficient phase/risk selection. Selected.

## Architecture

### Task recognition and repo discovery

The versioned `machine-readable/discovery/rules.v1.json` owns bounded positive-text archetype/risk recognition. Focused review archetypes use `quality-clause` scope: the shared lexical layer normalizes affirmative review/change heads in Spanish and English, strips explicit nominal exclusions and recognizes when a document is the **object** rather than merely a reference; the registry still owns every domain-to-owner mapping. Pure document reviews do not masquerade as application audits, while public-website privacy-policy reviews intentionally reach the existing public legal/trust owner. New terms must be exercised through the real descriptor and compiled capsules. The task descriptor's existing visual-specialist recognizers remain the owner of intricate design/style detection. Fix only proven recognizer errors, notably hero LCP measurements falsely selecting marketing-hero reconstruction and generic security/API audits incorrectly selecting lean-code review.

Routes in `routes.v1.json` inspect relevant **real** repo landmarks. Add the minimal missing landmark families for security configuration, privacy/data lifecycle, performance evidence, UI interaction tests and runtime observability. An unresolved landmark signals inspection, not its absence in the product. A cross-domain task produces a union of relevant inspection labels without applying an unrelated route's `avoid` to a protected security/privacy/data boundary.

`taxonomy.v1.json` gives separate discoverable topics for quality auditing, UI/UX, browser/accessibility, performance, security, **internal engineering privacy versus public website legal/privacy**, reliability and release; edges link the orchestrator to canonical owners. No new graph engine or hardcoded fallback router.

### Canonical guidance

`playbooks/engineering-quality-audit.md` owns the audit sequence: determine mandate/scope, inspect authority and representative journeys, choose domains, construct failure-mode/evidence matrix, execute the cheapest reliable relevant gates, classify/deduplicate findings, record provenance, distinguish review/fix/release, and verify closure. It links rather than restates the UI, security, privacy, performance, architecture, supply-chain, PWA, legal, operability and release Standards/Playbooks.

`standards/privacy-data-handling-baseline.md` fills the missing **cross-product engineering privacy** baseline for internal CRMs, apps and agentic services: purpose/data flow/roles, minimization, least exposure, retention and deletion contracts, consent gating where actually required, logging and data exports, production/demo isolation, provider/processor evidence and truthful limitations. Legal determination and regional public website copy stay with the existing specialist legal/trust owner. Cite already registered EU/AEPD primary sources; avoid creating a second website legal Standard.

Focused incremental clarifications in existing canonical owners cover security attack-surface review beyond login, UX journey/read-only review vs redesign, performance across client/server/DB/workload, accessibility evidence and truthful audit gates. Context units activate only on their respective detected risks or archetypes, with bounded must/should selection. Generic `intent:review` alone must never trigger every domain.

### Evidence and lifecycle

For every material finding record: exact asset/route, affected actor/journey/tenant, triggering condition, severity and realistic impact, observed evidence with revision/environment, canonical rule, proposed minimal fix, remaining unknowns and dedup key. A release readiness decision is separate from the quality audit and cannot be synthesized from a completed checklist. A periodic issue workflow acts only when separately authorized, deduplicates by stable cause and is silent when no actionable new findings exist.

## Tests and failure classes

- ES/EN focused and global review prompts, including read-only verbs and authorized fix prompts.
- Negative and question prompts (`no audites`, `do not audit`, `how to audit`), docs-only prompts and multi-clause instructions with different targets.
- Mixed security + UI, performance + SQL + UI, cookies/consent + public web and privacy + internal CRM.
- Real nested path landmarks; generated/vendor/docs fixtures do not masquerade as application owners.
- Planning/implementation/verification capsule provenance and risk coverage; no mandatory redesign for read-only performance/security audits, no arbitrary new spend/release.
- Search/tree/portable bundle exposes every new canonical artifact; regeneration is deterministic.

## Release and limitations

Only modify the Handbook. Execute targeted RED→GREEN tests, full repo suite, compiler check/doctor/integrity and a fresh diff review. Publication to shared `main` is a separate external side effect guarded by the current remote head and repository policy. Installing the new version into every consumer requires its existing enrollment/preflight; a Handbook publish is not proof of adoption.
