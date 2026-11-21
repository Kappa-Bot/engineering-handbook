---
id: std-code-quality-organization-baseline
kind: standard
status: active
owner: engineering
version: "0.2"
applies_to:
  - application-repositories
  - services
  - libraries
  - engineering-tooling
sources:
  - src-nist-ssdf-11
  - src-ponytail
  - src-ecma262-promise-race
  - src-whatwg-dom-abort-signals
last_verified: 2026-11-21
review_due: 2027-02-19
---

# Code Quality, Naming and Repository Organization Baseline

## Purpose and authority

Set a reliable cross-repository minimum for writing, reviewing, renaming, moving, simplifying and maintaining code. It covers source code, tests, scripts and executable configuration when those artifacts are being changed. **It does not prescribe a programming language, architecture pattern, naming case, directory tree, specific library, formatter or file-size/LOC quota.**

Read the nearest repository `AGENTS.md`, decisions, public contracts, package/build configuration and existing conventions before deciding. The actual project/framework owns its syntax, naming style, generated-code lifecycle, package manager, directory layout and verification commands. Existing adequate local patterns SHOULD be kept; changing conventions is a scoped migration, not an automatic cleanup. More specific security, data, UI, operability and release Standards still govern their risks.

The procedural route for non-trivial code tasks is [Code Change and Maintenance Workflow](../playbooks/code-change-workflow.md). The top-level lifecycle stays in [Engineering Change](../playbooks/engineering-change.md).

## 1. Know the contract and owner before editing

Before a non-trivial change or review, identify the behavior being preserved or added, the owning module and boundaries, relevant consumers, observable failure modes, tests, and any compatibility obligation. Work outward from the actual entry point and data/side-effect path; do not infer ownership from the requested filename alone.

Follow [Reuse First § Minimum complete change](../policies/reuse-first.md#minimum-complete-change) for dynamic consumers, unknown dead code, current invariants, duplication and least complete scope. A cleanup request alone does not authorize unrelated behavior changes, package upgrades, migrations, interface breaks or aesthetic redesigns. A read-only review does not authorize mutation.

## 2. Names are a domain interface

- Use the *established language/project naming convention* (including case, spelling, public API compatibility and generated names). Do not introduce a global `camelCase`, `snake_case` or folder-renaming rule into a different ecosystem.
- Names SHOULD convey domain role and intent, not just type or how a value was computed. Distinguish `accountId`, `tenantId` and `userId`; avoid hiding multiple concepts under `data`, `temp`, `utils` or `manager` where a precise name is available.
- Expose units, time basis, representation and side effects when ambiguous: `timeoutMs`, `durationSeconds`, `expiresAtUtc`, `grossAmountMinorUnits` are *illustrations*, not mandatory identifiers or one currency/time representation. Define the authoritative conversion and rounding boundary locally.
- Boolean names SHOULD make true/false meaningful (`isReady`, `canCancel`, `hasPermission` under matching local style); avoid a double negative, a getter that mutates, or a name that promises success before persistence actually completes.
- Keep abstractions, types, module names, public routes and tests consistent with their actual responsibility. Prefer precise domain terms over clever abbreviations; use conventional short names only in a small, unambiguous scope.
- Treat a public rename as a contract change: search static and dynamic usages, serialized fields, schemas, translations, tooling and downstream consumers as applicable. Use compatible aliases/deprecations only where a real migration needs them; remove them when the migration is verified complete.

## 3. Files, folders and dependency direction

- Group code by stable responsibility and change reason, respecting existing feature/domain/layer conventions. Colocate directly related code and tests where the repository's runner/framework supports it; keep build, generated and third-party material in their intended locations.
- A module SHOULD have an understandable purpose, inputs/outputs, ownership and side effects. Split when independently changing responsibilities or a real boundary justifies it; merge pass-through wrappers when they add no useful contract. Do not create one directory per file, a giant miscellaneous `utils` dumping ground, or a shared abstraction with no real consumers merely for visual tidiness.
- Make dependency direction intelligible. Avoid circular imports, hidden singleton state, runtime imports that mask cycles and domain logic depending on incidental UI/transport concerns. An exception is a conscious local design choice with a tested reason, not an invitation to restructure the repository blindly.
- Keep authoritative business checks and durable invariants at appropriate enforceable boundaries. Reuse [Architecture/Data Integrity](architecture-data-integrity-baseline.md) and [Security/Identity](security-identity-baseline.md) rather than restating authorization or persistence designs here.
- A folder move requires auditing exports, imports, module resolution, CLI entrypoints, build/test configuration, path aliases, case-sensitive filenames, generated references and packaging/distribution surfaces as applicable. Do not leave a parallel legacy tree by default.

**Illustrative only:** a feature-oriented repository may colocate `features/billing/invoice.*` and its tests; a conventional Python package or Java module may group by package instead. The right layout is what makes the *actual* owners and boundaries discoverable, not what matches this example.

## 4. Functions, errors, state and comments

- Keep externally observable behavior explicit: validate inputs at the right trust boundary, represent invalid states/errors deliberately, and preserve typed/validated interfaces where the local ecosystem supports them. Do not quietly swallow an exception, return fake success, broaden privileges, or hide a broken contract under a fallback.
- Make side effects legible. A query should not unexpectedly mutate; a retried mutation needs appropriate duplicate/atomicity semantics; async work must account for cancellation, timeouts, lifecycle cleanup and honest accepted-versus-completed states as applicable. Refer to [Production Operability](production-operability-baseline.md) for operational contracts.
- When verifying cancellation of asynchronous work, observe the caller and the underlying operation separately. For example, a timeout winning `Promise.race()` settles the caller's wait. An `AbortSignal` requests cancellation. In a controlled test, hold work before an observable step, trigger the timeout or abort, then allow pending work to proceed. Check the operation's own outcome and whether the step ran after the caller stopped waiting. If only the caller is observable, record the underlying outcome as unverified.
- Use deterministic, narrow helpers when they clarify a real repeated operation. Avoid speculative wrappers, unnecessary generic flags/options, premature framework swaps, “one-line” code golf or abstractions with a single hypothetical consumer.
- Comments SHOULD explain non-obvious *why*, invariant, security constraint, trade-off or external contract; names/types/tests express ordinary *what*. Do not leave misleading commented-out code, stale documentation or debt markers with no owner/next step; follow the existing debt contract in `pol-reuse-first`.
- Preserve explicit resource bounds and relevant failure behavior under load. Investigate measured hotspots and actual N+1/allocations/blocking work where material; do not optimize an unmeasured micro-path at the expense of correctness or clarity.

## 5. Libraries and toolchain are not style accessories

The canonical owner for dependency selection, lockfiles, security, license, provenance and upgrade lifecycle is [Dependency and Software Supply-Chain Baseline](dependency-supply-chain-baseline.md). For consequential or difficult choices use [External Solution Evaluation](../playbooks/external-solution-evaluation.md). Start from a suitable existing module, platform/standard library or already-installed package; choose a new one only for a demonstrated requirement. Confirm current official support, actual API/compatibility, transitive/security/licensing/maintenance implications and rollback path for the product's precise environment.

Use repository-owned formatters, linters, typecheckers, build/test tools and package manager; don't add a competing formatter or package manager merely to enforce this Standard. Changing tool versions, lint policies or lockfiles is a separate affected scope with its own checks.

## 6. Refactor/cleanup safely and prove the outcome

Before a behavior-preserving refactor, establish a meaningful existing test/characterization or other executable behavior evidence. Use focused incremental changes; check public API/signature/type/serialization, dynamic import/route/registry jobs, persistence/security, path/build/test wiring and consumer compatibility. Treat generated files according to their source generator, not hand edits that disappear on rebuild. If a required migration or breaking change is authorized, sequence producers and consumers explicitly and keep a rollback/forward-fix path proportionate to the risk.

For a behavior change, test the new expected contract first when meaningful; for a pure rename, run the existing behavior tests and tooling that would catch broken references. Unit tests alone do not prove runtime registrations, package consumption, authorization, accessibility, device behavior or Production state. Choose the smallest reliable evidence set under [Testing and Release Quality](testing-release-quality-baseline.md) and [Verification Definition of Done](../policies/verification-definition-of-done.md); include relevant negative, edge and integration cases.

Review with a concrete failure mode, effect and correction. Report what actually ran and what remains unverified. No blanket “everything correct” claim from lint, typecheck or a short test run.

## Applicability, exceptions and adoption

New or changed code uses the repository's current conventions without bulk rewriting legacy files. Existing products are **not** required to re-layout or rename entire codebases to adopt this baseline. When conventions conflict, resolve against local active architecture and higher-priority security/data contracts; record an intentional durable exception where future contributors would otherwise repeat the debate. Universal stylistic preferences are not sufficient grounds for a breaking migration.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "code-task-owner-and-contract",
      "type": "decision-question",
      "text": "For code work, inspect local conventions, owning flow, callers and public contracts; identify requested outcome, affected invariants and meaningful tests. Follow pb-code-change-workflow for non-trivial work; review does not authorize edits.",
      "source": "std-code-quality-organization-baseline",
      "covers": ["change-completeness"],
      "activate_when": ["archetype:code-change"],
      "force": "must",
      "phase": ["planning"],
      "priority": 90
    },
    {
      "id": "code-craft-implementation",
      "type": "constraint",
      "text": "Use project-owned naming, modules, folder layout, formatting and package tools. Preserve explicit domain boundaries, types, errors and side effects; avoid speculative helpers, ambiguous units and unrelated cleanup.",
      "source": "std-code-quality-organization-baseline",
      "covers": ["change-completeness"],
      "activate_when": ["archetype:code-change"],
      "force": "must",
      "phase": ["implementation"],
      "priority": 90
    },
    {
      "id": "code-craft-verification",
      "type": "verification",
      "text": "Verify affected behavior and consumers with actual repo tests, formatting/lint/type/build and risk-specific integration gates; check edge/negative/error paths and report each unrun gate honestly.",
      "source": "std-code-quality-organization-baseline",
      "covers": ["change-completeness"],
      "activate_when": ["archetype:code-change"],
      "force": "must",
      "phase": ["verification"],
      "priority": 90
    },
    {
      "id": "code-organization-safety",
      "type": "constraint",
      "text": "For code renames, moves, deduplication or refactors, trace static/dynamic consumers, exports/routes/config/tests and generated/build paths. Preserve behavior, data and access contracts; migrate breaking paths deliberately, not as incidental cleanup.",
      "source": "std-code-quality-organization-baseline",
      "covers": ["change-completeness"],
      "activate_when": ["archetype:code-organization"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 95
    }
  ]
}
```
