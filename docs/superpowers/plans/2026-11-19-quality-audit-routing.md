# Cross-domain Quality Audit Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make UI/UX, accessibility, performance, security, privacy and reliability reviews reliably discoverable, routable and verifiable without silently authorizing edits or duplicating normative standards.

**Architecture:** Extend the existing versioned discovery registry and the few source feature recognizers proven wrong; add one cross-domain orchestration Playbook and a narrowly scoped cross-product privacy Standard; project units from canonical owners into the existing compiler. Use repository landmarks, phase capsules and end-to-end tests as the contract.

**Tech Stack:** Python 3 standard library, `unittest`, declarative JSON, Handbook Markdown `agent-context`, existing compile/doctor/integrity CLIs.

**Spec:** `docs/superpowers/specs/2026-11-19-cross-domain-quality-audit-routing-design.md`

## Global Constraints

- Existing docs own UI/Unslop, web platform, security identity, performance budgeting, observability, PWA, legal trust, testing/release; new orchestration MUST link rather than duplicate them.
- No automatic modification, issue creation, release, external provider calls, paid CI or subagent default from a review request.
- A material visual acceptance claim requires actually rendered states; an appsec claim requires tested relevant negative paths; remote/native checks remain unrun until exercised.
- The known internal-console Glass candidate is scoped to new or authorized redesign without active local choice; Neumorphism and solid remain optional design directions.
- Reject generated/vendor/docs paths as false application owners; prefer real nested repo signals; preserve zero/one/two-agent and cost boundaries.
- Maintain ES/EN parity and clause-local authorization semantics. Run all tests and compiler validations before publishing.

## Review Focus

1. `Audit the security of the CRM; redesign the README` selects security without converting the audit into app code changes.
2. `Do not audit security, review UX` must not borrow negated security signals.
3. `Measure LCP and SQL query latency on the public website` must not trigger hero reconstruction solely from the site noun.
4. `Audit privacy of the internal CRM` must find privacy owners even with no public cookies or marketing site.
5. A mixed UI/security/data task must not inherit UI-only avoid labels that hide a real protected backend boundary.

---

### Task 1: Reliable quality task recognition and repository routes

**Files:**
- Create: `tests/engineering_context/test_quality_audit_routing.py`
- Modify: `machine-readable/discovery/rules.v1.json`
- Modify: `machine-readable/discovery/routes.v1.json`
- Modify: `machine-readable/discovery/landmarks.v1.json`
- Modify: `automation/engineering_context/discovery_rules.py`
- Modify: `automation/engineering_context/task_descriptor.py`
- Modify: `automation/engineering_context/context_solver.py` only if mixed-route behavior proves incorrect

**Interfaces:**
- Consumes: `describe_task(text, profile, changed_paths=())`, `profile_repo(root)` and `build_repo_route(profile, descriptor)`.
- Produces: `quality-audit`, `ui-quality-review`, `accessibility-review`, `performance-review`, `security-review`, `privacy-review`, `reliability-review` archetypes and the corresponding `quality-coverage`, `ux-quality`, `accessibility`, `performance`, `security-exposure`, `privacy-exposure`, `availability` risks. New landmark labels `ui-interaction-tests`, `security-configuration`, `privacy-data-lifecycle`, `performance-evidence`, `runtime-observability`.

- [ ] **Step 1: Write table-driven, consumer-facing failing tests.** Assert exact archetypes/risks/intents and route labels for focused, global, mixed, negative, question, docs-only and path-only tasks; assert bounded status, no implied deploy/modify; assert owner paths from a temporary real repo.
- [ ] **Step 2: Run RED.** `python -m unittest tests.engineering_context.test_quality_audit_routing -v` — Expected: failures for missing quality archetypes/risk/route resolution, not a syntax error.
- [ ] **Step 3: Implement registry recognizers, routes and landmarks, then minimally repair proven text-scope/visual recognizer bugs.** No alternate hardcoded quality-router; clause-local condition for action+target+exclusions; route union retains protected boundaries.
- [ ] **Step 4: Run GREEN and affected classifier regressions.** `python -m unittest tests.engineering_context.test_quality_audit_routing.QualityReviewClassificationTests tests.engineering_context.test_code_craft_routing.CodeCraftClassificationTests tests.engineering_context.test_discovery_v2.DiscoveryRoutingTests -q` — Expected: all PASS. Defer existing compiled-capsule/CLI suites until Task 2 creates coverage units and Task 3 refreshes the derived compiled snapshot; otherwise stale-index and uncovered-risk failures are an expected intermediate state.
- [ ] **Step 5: Commit.** `git add` exact task files; `git commit -m "fix(handbook): route cross-domain quality reviews"`.

### Task 2: Canonical audit procedure and owner-level guidance units

**Files:**
- Create: `playbooks/engineering-quality-audit.md`
- Create: `standards/privacy-data-handling-baseline.md`
- Modify: `playbooks/security-review.md`
- Modify: `playbooks/frontend-quality-review.md`
- Modify: `standards/ui-ux-quality-baseline.md`
- Modify: `patterns/performance-budgeting.md`
- Modify: `standards/production-operability-baseline.md` when reliability review unit activation needs it
- Modify: `standards/public-website-legal-trust-baseline.md` only to link specialized web vs cross-product privacy owner
- Modify: `tests/engineering_context/test_quality_audit_routing.py`

**Interfaces:**
- Consumes: Task 1's archetype/risk tags and `solve_context(compiled, descriptor, phase)`.
- Produces: phase-selected units `quality-audit-intake`, `quality-audit-closure`, `ux-journey-audit`, `ux-journey-evidence`, `security-attack-surface-review`, `security-review-negative-evidence`, `privacy-data-flow-review`, `privacy-boundary-evidence`, `performance-bottleneck-triage`, `ui-accessibility-functional-verification` from their canonical Markdown owners.

- [ ] **Step 1: Write RED tests for phase capsules, mandatory provenance, direct risk coverage, no automatic redesign for a security/performance audit, and retained existing coverage.** Compile into a temporary directory as the actual consumer does.
- [ ] **Step 2: Run RED.** `python -m unittest tests.engineering_context.test_quality_audit_routing -v` — Expected: new capsule assertions fail for missing units/provenance.
- [ ] **Step 3: Add the new Playbook/Standard and focused owner clarifications and context units.** Use the existing GDPR/OWASP/WCAG/Chrome source IDs, distinct field/transport/runtime evidence and explicit audit/fix/release boundaries. Do not add unrelated policies.
- [ ] **Step 4: Run GREEN.** `python -m unittest tests.engineering_context.test_quality_audit_routing -q` — Expected: all PASS.
- [ ] **Step 5: Commit.** `git add` exact task files; `git commit -m "docs(handbook): define holistic quality audit gates"`.

### Task 3: Discoverable catalog, search/tree, Codex entrypoints and compiled projection

**Files:**
- Modify: `machine-readable/catalog.yaml`
- Modify: `machine-readable/discovery/taxonomy.v1.json`
- Modify: `README.md`
- Modify: `agent-config/codex/AGENTS.global.md`
- Modify: `agent-config/codex/skills/engineering-handbook/SKILL.md`
- Modify: `templates/AGENTS.repo.md` only if the existing template omits any quality-review entrypoint
- Modify: `tests/engineering_context/test_quality_audit_routing.py`
- Regenerate: `machine-readable/compiled/*`

**Interfaces:**
- Consumes: Task 1 route and Task 2 canonical ID names.
- Produces: `search()`, `knowledge_tree()`, portable installed bundle and `check`/`doctor` all exposing the same active authorities; compiled phases include the new context units.

- [ ] **Step 1: Write RED end-to-end tests.** Search ES/EN queries; assert visible knowledge topic and canonical targets; bundle via the real handbook updater to a temporary target; verify generated content is actually present in the installed snapshot.
- [ ] **Step 2: Run RED.** `python -m unittest tests.engineering_context.test_quality_audit_routing -v` — Expected: missing topic/entrypoint/bundle assertions fail.
- [ ] **Step 3: Update catalog, taxonomy/edges and existing Codex entrypoints with brief links; regenerate compilation using `python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled`.** Expected: exit 0.
- [ ] **Step 4: Run GREEN.** `python -m unittest tests.engineering_context.test_quality_audit_routing -q` — Expected: all PASS.
- [ ] **Step 5: Commit.** `git add` exact source and generated files; `git commit -m "docs(handbook): expose quality reviews across discovery"`.

### Task 4: Full verification and scoped review

**Files:**
- No new source files unless verification reproduces a material defect; any fix follows RED→GREEN and gets its own commit.

**Interfaces:**
- Consumes: all three task deliveries.
- Produces: evidence ledger, clean branch, verified diff and publication-ready Git tree.

- [ ] **Step 1: Run all tests.** `python -m unittest discover -s tests/engineering_context -p 'test_*.py' -q` — Expected: 0 failures.
- [ ] **Step 2: Run compiler, check/doctor/integrity and `git diff --check`.** Expected: exit 0 and stable compiled snapshots.
- [ ] **Step 3: Review the whole change against the spec and this plan; classify findings by user consequence.** Use the requested independent review when allowed by instructions; one correction pass with RED→GREEN for material findings.
- [ ] **Step 4: Repeat full verification on the final tree; reconcile branch and publication authority.** Never equate local test PASS with remote installation or consumer adoption.
