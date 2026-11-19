---
id: pb-code-change-workflow
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - application-repositories
  - services
  - libraries
  - engineering-tooling
sources:
  - src-nist-ssdf-11
  - src-ponytail
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Code Change and Maintenance Workflow

Use for writing code, reviewing its quality, cleaning or refactoring implementation, renaming symbols, reorganizing folders/modules and choosing or replacing libraries. This is the **code-specific execution path within** [Engineering Change Workflow](engineering-change.md); it is not another general lifecycle, a new agent persona or permission to edit a repository under review.

The normative code craft baseline is [Code Quality, Naming and Repository Organization](../standards/code-quality-organization-baseline.md). `pol-reuse-first` owns minimum-complete scope, `std-dependency-supply-chain-baseline` owns dependency decisions and `pol-verification-definition-of-done` owns truthful verification.

## 1. Orient and establish the change contract

1. Inspect actual repository state and instructions: nearest `AGENTS.md`, README/architecture/ADRs, language/framework versions, package manifests/lockfile, existing source folders, tests and local tooling. Separate requested intent from permission to mutate or deploy.
2. Locate the authoritative entry point, ownership boundary and affected consumers, including exports, API endpoints, jobs, scripts, generated clients, translations and persistence where relevant. Ask which behavior/invariant must remain or change.
3. State a compact acceptance contract: before/after behavior, allowed changes, non-scope, error/negative cases, compatibility/deprecation need and actual verification commands. A one-line rename needs no new spec file; a durable ownership change may need a repo-local ADR.
4. Check existing canonical implementation, adequate platform primitives, installed dependencies and relevant proven internal patterns. Stop when a semantically complete suitable option is found. Do not turn discovery into research paralysis.

## 2. Choose the right coding action

| Intent | Primary action | Key failure to avoid |
| --- | --- | --- |
| Add/change behavior | Establish expected contract and test it where meaningful; implement at the real owner | Happy-path code that omits permission, error or existing consumer behavior |
| Fix a bug | Reproduce original failure, localize cause, write a regression, correct minimally | Patching the symptom or declaring success without rechecking the failure |
| Rename symbols or files | Find static and dynamic consumers, assess public/serialized contract, use language tooling when reliable | Breaking imports, persisted keys, case-sensitive paths or external clients |
| Refactor/simplify | Characterize current behavior first; then split/merge by cohesive responsibility | Deleting checks, introducing a second ownership path or unnecessary abstraction |
| Reorganize folders | Map runtime/package/build/test/export entrypoints and dependency direction; move incrementally | A cosmetic tree that breaks resolution or splits a feature across unrelated owners |
| Select/change a library | Apply supply-chain owner, compare fit and total cost, pin/install only if authorized | Unverified compatibility, transitive risk, lockfile drift or parallel packages |
| Review only | Report verified defects, hypotheses and unrun gates; recommend concrete fixes | Treating read access or audit findings as write/deployment authority |

## 3. Name, place and implement

- Choose names from the actual domain, units and local convention. Validate public names and serialization separately from local variables; an IDE rename is a helper, not proof of safety.
- Respect existing feature/package/layer layout; place new code close to the owning behavior. Extract only when a real boundary, repeated consumer or separately changing responsibility earns it. Preserve domain/authorization separation and eliminate needless indirection only with evidence.
- Make input validation, errors, side effects, async transitions and resource limits explicit. Prefer clear typed interfaces and honest state over silent fallbacks, broad exception suppression or unexplained magic behavior. Respect the Security, Architecture/Data and Production Operability Standards for affected boundaries.
- Follow existing formatter/linter/typechecker and test style. Keep comments for non-obvious reasons, not narration; update contract docs with real behavior rather than recording implementation speculation.
- Use reversible, focused changes. When a rename/move crosses package or public API boundaries, plan old/new consumer compatibility, generated-code regeneration and deletion of transitional paths at the appropriate gate.

## 4. Make dependency decisions explicit, proportionately

Before adding, removing or replacing a package:

1. Check the repository/package manager, current version graph, available native/standard-library or installed alternatives and the actual missing capability.
2. Compare *for the product's environment*: functionality/API and version/runtime support from current official docs; security/provenance, licenses, maintainer support, transitive size, performance, accessibility where relevant, deployment/runtime limitations, maintenance burden and exit cost.
3. Check actual permissions and supply-chain effects before executing install/upgrade/scripts. Pin/freeze resolution using each ecosystem or workspace's existing mechanism; avoid conflicting managers/lockfiles **within the same dependency scope** unless deliberately supported. Polyglot repositories can legitimately have multiple managers. Don't commit vendor folders by accident. A lockfile generated for an unreviewed package is not approval.
4. Verify real call sites, API changes, transitive security/licensing, build/package and rollback or removal of the displaced solution. Durable, costly decisions may need the local ADR; routine package choices need only a brief PR reason.

The normative details and exceptions belong in [Dependency and Software Supply-Chain Baseline](../standards/dependency-supply-chain-baseline.md), not in another policy here.

## 5. Close the actual failure classes

Select gates by affected boundary, using project-local commands:

| Change | Minimum relevant evidence to consider (not a universal command list) |
| --- | --- |
| Local pure function | Focused behavior/edge tests, formatter/lint/typecheck where available |
| Rename/module move | Existing contract tests, import/type/build/package resolution, dynamic routes/registries and downstream exports |
| Dependency change | Immutable install/lockfile reproducibility, actual API/integration/build, relevant license/security and runtime support |
| Persistence/auth/money | Authoritative boundary/negative and isolation tests, migration and backward compatibility, real side effects as authorized |
| UI/browser | Real rendered interaction, accessibility, responsive/device and framework/browser compatibility in addition to build/unit |
| Async/integration | Failure/retry/idempotency, timeouts/cancellation, producer/consumer wiring and observable completion |

Start with fast targeted verification, then the affected broader suite. Run every required repository gate for the accepted scope, not every expensive suite by habit; use permitted local test resources and never create paid branches/containers/environments as a side effect of “just running tests”. A failed check is a failure, not a reason to weaken tests or silently skip it. Read-only reviews may identify missing gates without running live mutations.

Before handoff, inspect the diff plus impacted consumers: no accidental new dependency, renamed public contract, orphaned code/test/script, copied secret, divergent generated artifact, unrelated folder churn or behavior lost during cleanup. Report verified result, test commands/exit results, unrun gates, known compatibility risks and whether any deployment/adoption actually happened.

## Navigation and exceptions

For a new module, use repository discovery/manifest and test landmarks first; for refactors, inspect source owners and consumers before rearranging. The Handbook's `code-change`, `code-organization` and `dependency-selection` routing flags are **advice to inspect**, not a license to operate. The absence of a discovered path means inspect manually or declare a verified local landmark; do not invent a folder or infer an unused symbol from an empty textual search.

This workflow deliberately leaves TypeScript/Python/Rust/Go idioms, feature-vs-layer layout, dependency versions, build tools and package publishing to the consumer repository. An authorized redesign of those choices gets its own compatibility and verification plan; an ordinary code fix does not trigger it.
