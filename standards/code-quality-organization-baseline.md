---
id: std-code-quality-organization-baseline
kind: standard
status: active
owner: engineering
version: "0.12"
applies_to:
  - application-repositories
  - services
  - libraries
  - engineering-tooling
sources:
  - src-nist-ssdf-11
  - src-ponytail
  - src-ecma262-promise-race
  - src-python-312-asyncio-wait-for
  - src-python-312-asyncio-task-group
  - src-python-312-exception-group-handlers
  - src-ecma262-promise-aggregation
  - src-ecma262-async-from-sync-iterator
  - src-whatwg-dom-abort-signals
  - src-whatwg-streams-pipe-to
  - src-whatwg-streams-async-iterator
  - src-nodejs-24-arraybuffer-messageport
  - src-whatwg-html-structured-error-data
  - src-whatwg-html-text-field-length
  - src-unicode-uax29-text-segmentation
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
- When an existing text field has a length contract, identify the unit at
  each boundary that enforces it. A limit in UTF-8 bytes, Unicode code points,
  UTF-16 code units or extended grapheme clusters can produce different
  results. Use composed and decomposed forms of the same text and a
  supplementary character to verify what the interface accepts and what the
  receiver validates. HTML text `maxlength` uses UTF-16 code units. Retain
  the product's existing normalization policy. See
  `src-whatwg-html-text-field-length` and `src-unicode-uax29-text-segmentation`.
- Make side effects legible. A query should not unexpectedly mutate; a retried mutation needs appropriate duplicate/atomicity semantics; async work must account for cancellation, timeouts, lifecycle cleanup and honest accepted-versus-completed states as applicable. Refer to [Production Operability](production-operability-baseline.md) for operational contracts.
- When verifying cancellation of asynchronous work, observe the caller and the underlying operation separately. For example, a timeout winning `Promise.race()` settles the caller's wait. An `AbortSignal` requests cancellation. In a controlled test, hold work before an observable step, trigger the timeout or abort, then allow pending work to proceed. Check the operation's own outcome and whether the step ran after the caller stopped waiting. If only the caller is observable, record the underlying outcome as unverified.
- When existing Python code directly awaits an unshielded task with
  `asyncio.wait_for()`, hold the task’s cleanup after it receives
  `CancelledError` from the timeout. Observe whether the caller is still
  waiting. Release cleanup and check the caller’s outcome. A task that
  propagates cancellation makes `wait_for()` raise `TimeoutError`. A task
  that handles cancellation and returns a value can deliver that value to
  the caller. Check any cleanup exception separately and use completion
  before the timeout as a control. See `src-python-312-asyncio-wait-for`.
- When an existing Python `asyncio.TaskGroup` reports failures, hold a sibling
  in cancellation cleanup after another task fails. Check that the group waits
  for cleanup. Compare a sibling that propagates cancellation with one whose
  cleanup raises a separate exception. The group can report both the initiating
  failure and the cleanup failure. If the caller handles selected exceptions
  with `except*`, check which exceptions it handles and which it still receives.
  See `src-python-312-asyncio-task-group` and `src-python-312-exception-group-handlers`.
- When an existing cancellation contract rejects work before admission, call
  the operation with an `AbortSignal` that is already aborted. The one-shot
  `abort` event is dispatched when the signal changes state. A later listener
  misses that event. Check the initial signal state and verify the promised
  rejection and reason. Observe registration, startup and effects separately
  to verify whether the operation skipped admission. Use ordinary success and
  cancellation after work starts as controls. See `src-whatwg-dom-abort-signals`
  §3.3.
- When concurrent tasks share a resource that must remain available through their last use, hold one task just before a resource access in a controlled test and let a sibling fail. Record when the caller observes failure and when cleanup releases the resource. For example, `Promise.all()` can reject while a sibling is still running. Resume the held task and verify that its last use precedes release, or observe that cancellation ended its use. Include child work that still uses the resource after its parent's promise settles. Check the failure reported to the caller against the existing contract. See `src-ecma262-promise-aggregation`.
- When an existing Node.js binary handoff sends an owned `ArrayBuffer`
  through a `MessagePort`, verify the receiver's promised bytes and view
  ranges. Compare clone and transfer behavior with multiple sender views of
  the same buffer. A clone leaves those views usable. Transferring the
  backing buffer detaches it for every sender view. Check detachment or actual
  usability, since an attached view can have zero length. See
  `src-nodejs-24-arraybuffer-messageport`.
- Use deterministic, narrow helpers when they clarify a real repeated operation. Avoid speculative wrappers, unnecessary generic flags/options, premature framework swaps, “one-line” code golf or abstractions with a single hypothetical consumer.
- Comments SHOULD explain non-obvious *why*, invariant, security constraint, trade-off or external contract; names/types/tests express ordinary *what*. Do not leave misleading commented-out code, stale documentation or debt markers with no owner/next step; follow the existing debt contract in `pol-reuse-first`.
- Preserve explicit resource bounds and relevant failure behavior under load. Investigate measured hotspots and actual N+1/allocations/blocking work where material; do not optimize an unmeasured micro-path at the expense of correctness or clarity.

- When an existing structured-clone handoff sends a JavaScript `Error` for
  a recovery decision, verify the fields used by the receiving code. The
  receiver can get the error name and message while application-owned fields
  such as `code` are absent. Test the real handoff and the recipient's decision.
  If the contract sends an explicit record, check each required field on that
  path as well. See `src-whatwg-html-structured-error-data`.

- When an existing pipeline uses `ReadableStream.pipeTo()`, test a failed
  destination write with the configured options. Observe the pipe promise,
  the source cancellation and the remaining source data separately. A
  destination failure can cancel the source. With `preventCancel`, the
  source can remain available after that failure. If cancellation can
  fail, check which error reaches the caller and which error the source
  received. Verify a successful write and close as controls. See
  `src-whatwg-streams-pipe-to`.

- When an existing consumer exits `ReadableStream` iteration early, check
  the source cancellation, reader lock and unread chunks separately. A default
  `break` releases the reader while the caller can still be waiting for source
  cancellation. Hold the cleanup and observe which data a new reader gets.
  If cleanup can fail, observe the caller's outcome. If the flow uses
  `values({ preventCancel: true })` to resume reading, check the remaining
  chunks through completion. Include an ordinary full read as a control. See
  `src-whatwg-streams-async-iterator` §4.2.5.

- When an existing `for await...of` loop adapts a synchronous iterator that
  returns promise values, test rejection from a live item and from a terminal
  result if the source can produce both. Both can reject the consumer. A
  rejected terminal result can do so without calling the iterator's `return`
  method. Check the observed error and source cleanup separately, with normal
  completion and a consumer interruption as controls. See
  `src-ecma262-async-from-sync-iterator`.

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
