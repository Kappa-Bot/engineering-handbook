# Code Craft and Repository Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** establish a discoverable end-to-end code-writing/cleanup/organization baseline and repair Codex routing for real code, dependency and refactoring tasks.

**Architecture:** one code-quality Standard owns cross-repository constraints and one focused Playbook explains the lifecycle; existing dependency/reuse/release owners retain their contracts. The versioned rule, taxonomy, route and landmark registries drive the existing classifier, compiled context capsules and search without a new router.

**Tech Stack:** Python standard library, JSON, Markdown, unittest, existing Handbook compiler.

**Spec:** `docs/superpowers/specs/2026-11-19-code-craft-and-repository-structure-design.md`

## Global Constraints

- No product-repository edits, universal technology/folder/naming mandate, paid tool, new automatic CI job, plugin installation or unreviewed host hook.
- Keep one active canonical owner for each concern: reuse, dependencies, architecture, security, verification, coding craft and the engineering lifecycle.
- Classification is guidance, never authorization; questions, negations, docs and generated/vendor examples must not produce code-edit authority.
- Preserve current consumers, existing local conventions, public contracts and reversible migration safety.
- No arbitrary test-count/LOC quota; evidence depth follows actual risk and scope.

## Review Focus

1. Renaming a variable/function/module and reorganizing a source folder should select coding guidance in Spanish and English without authorizing an edit from a review-only request.
2. A code or dependency change recognized from paths alone should still find the right owners, while README/code examples, vendored/generated assets, and CSS class names should not trigger organizational refactors.
3. Negated actions such as “do not refactor or rename” must not become positive changes; an independent subsequent “fix the code” should still match.
4. Library decisions must reference existing reuse/security/lockfile policy, not prescribe a universal dependency or reject an already suitable standard-library API.
5. Refactor/move checks must cover dynamic consumers, external APIs, tests, generated files, compatibility, data/security semantics and verification without treating no textual match as dead-code proof.

---

### Task 1: Coding-task classification and file-route regressions

**Files:**
- Create: `tests/engineering_context/test_code_craft_routing.py`
- Modify: `machine-readable/discovery/rules.v1.json`, `machine-readable/discovery/routes.v1.json`, `machine-readable/discovery/landmarks.v1.json`, `automation/engineering_context/discovery_rules.py` (only for observed negation gaps).

**Interfaces:**
- `describe_task(task_text, repo_profile, changed_paths=()) -> TaskDescriptor` exposes `code-change`, `code-organization`, `dependency-selection` archetypes and correct intent.
- `build_repo_route(profile, descriptor) -> dict` orders `source-owner`, `nearest-tests`, `dependency-manifest` where applicable and resolves real paths without inventing them.

- [ ] Write table-driven ES/EN task and path tests for positive, negative, mixed, documentation and generated/vendor cases. Break caught: missing archetype, false edit intent, missing/unsafe file landmark.
- [ ] Run `python -m unittest tests.engineering_context.test_code_craft_routing -v` and observe the expected RED assertions.
- [ ] Add only needed registry rules/negation grammar/landmarks/routes.
- [ ] Rerun the focused test to GREEN and run `python -m unittest tests.engineering_context.test_discovery_v2 tests.engineering_context.test_modern_web_lean_guidance`.
- [ ] Commit task sources after checks.

### Task 2: Canonical code standard, focused playbook and capsule owners

**Files:**
- Create: `standards/code-quality-organization-baseline.md`, `playbooks/code-change-workflow.md`
- Modify: `playbooks/engineering-change.md`, `standards/dependency-supply-chain-baseline.md`, `tests/engineering_context/test_code_craft_routing.py`

**Interfaces:**
- `std-code-quality-organization-baseline` contains phase-scoped `json agent-context` units `code-task-owner-and-contract`, `code-craft-implementation`, `code-craft-verification`, `code-organization-safety`.
- `std-dependency-supply-chain-baseline` retains selection authority, adds a scoped `dependency-choice-review` context unit.
- `pb-code-change-workflow` is operational guidance, not a competing policy or mandatory new repository file.

- [ ] Write tests that compile the handbook to an ephemeral directory and assert selected capsule units for code, structure and dependency tasks, plus absence for prose-only requests. Break caught: code standard not discoverable at the appropriate phase, or too-broad mandatory routing.
- [ ] Run the focused test and observe RED for the missing canonical units.
- [ ] Write the baseline and procedural playbook; link the lifecycle and dependency owner with explicit exception/compatibility rules, scoped metadata and valid projection.
- [ ] Compile to the tracked compiled directory and rerun the focused/context-contract tests to GREEN; inspect token budgets.
- [ ] Commit task sources after checks.

### Task 3: Discovery, distribution and integration

**Files:**
- Modify: `machine-readable/catalog.yaml`, `machine-readable/discovery/taxonomy.v1.json`, `README.md`, `agent-config/codex/AGENTS.global.md`, `agent-config/codex/skills/engineering-handbook/SKILL.md`, generated `machine-readable/compiled/*`.
- Include: specification and plan under `docs/superpowers/...` in the catalog.

**Interfaces:**
- `search` and `knowledge_tree` resolve canonical code craft/flow by ES/EN aliases; generic installed skill points to the canonical source without a parallel router.

- [ ] Add test for real discovery search and knowledge-tree grouping plus bundle/integrity inclusion (not prose substring checks). Break caught: code guidance exists but agents cannot find it.
- [ ] Run the focused test RED for missing catalog/taxonomy links.
- [ ] Register the new artifacts once, add short entrypoint links, regenerate compiled context, and keep bundle contract unchanged if existing directory includes suffice.
- [ ] Run discovery, context and bundle tests to GREEN and `python -m automation.engineering_context check --root .`.
- [ ] Commit task sources after checks.

### Task 4: Whole-corpus conflict and completion gate

**Files:**
- Modify only any directly conflicting active source or material regression identified in the full review.

**Interfaces:**
- `python -m automation.engineering_context check --root .`, `doctor`, `integrity`, the full `tests/engineering_context/test_*.py` suite, and `git diff --check`.

- [ ] Search active Markdown and source registries for contradictory naming, folder, dependency, cleanup and code ownership rules; record any evidence-backed focused corrections.
- [ ] Run every listed fresh gate and inspect changed-file diff, generated drift and tests for false positives and authority boundaries.
- [ ] Obtain one read-only independent final review; grade findings by actual consequences and fix Critical/Important with RED→GREEN and fresh suite.
- [ ] Integrate/publish through the existing authorized Handbook route, verify remote SHA/tree exactly and report the installed-consumer refresh boundary separately.
