# Handbook Discovery 2.0 implementation plan

> Execute with the executing-plans workflow; use test-driven development and verification-before-completion. Root implements; independent read-only reconnaissance and final security review provide separate evidence.

**Goal:** implement the approved discovery design and a safe task-start Handbook update path.

**Architecture:** standard-library Python, declarative JSON registries, generated catalog index, existing context compiler and backwards-compatible CLI. A separate stable bootstrap owns installation/update; downloaded code is never executed to validate itself.

**Stack:** Python 3.10+, Git, JSON, Markdown, existing optional PowerShell entrypoints. No service or dependency additions.

### Task 1: freeze contracts and reproduce regressions

- Add `tests/engineering_context/test_discovery_v2.py` and fail-first cases for negation, intent, Spanish migration, false credential/SQL/docs signals, agent TOML paths, real landmarks and registry errors.
- Add `tests/engineering_context/test_handbook_update.py` covering safe installation and preflight state transitions with local Git fixtures and mocked transport only.
- Run focused tests and observe failures before implementing each area.

### Task 2: explicit discovery rules and real repository paths

- Add `machine-readable/discovery/` registries and `automation/engineering_context/discovery_rules.py`.
- Refactor generic mappings in `task_descriptor.py` to registry evaluation; preserve tested visual feature extractors and existing descriptor consumers.
- Extend `repo_profile.py` and `context_solver.py` with verified landmarks, stable priority order, unresolved results and adaptive budgets.
- Run old/new descriptor and repository tests.

### Task 3: catalog index, graph, search, trees and explanations

- Add `automation/engineering_context/discovery.py`, compile the full catalog and typed graph, integrate with `handbook_compile.py` and `cli.py`.
- Implement `search`, `tree`, `explain`, `doctor`; retain all existing commands and context contracts.
- Verify bilingual queries, active/historical filters, invalid graphs, byte stability, catalog coverage and prose-index invalidation.

### Task 4: safe installation and pre-task update

- Add `automation/codex/handbook_update.py` and portable install/refresh/doctor entrypoints.
- Isolate Git configuration/transport, enforce origin/history constraints, validate paths and manifests, preserve user files, lock/stage/journal/rollback activation.
- Merge synchronous owned hooks idempotently, supply fresh-baseline context and expose stale/blocked states honestly.
- Verify failure and recovery paths; test the portable installed runtime, retaining PowerShell compatibility.

### Task 5: model routes and canonical documentation

- Replace active Luna selections with Terra and validate allowlist/fallback behavior. Retain historical evidence.
- Update the single router skill, bundle, global baseline, routing/adoption docs, README, sources and catalog; add ADR 0012 and discovery/update playbook without duplicate normative owners.
- Recompile generated artifacts, run focused contracts then full verification.

### Task 6: independent review and publication

- Fresh capable reviewer audits the complete branch, particularly update integrity and authority boundaries. Address findings and rerun affected checks plus final full gates.
- Publish with `[skip ci]`, expected-main-SHA protection and exact tree verification. Do not claim a Windows workstation installation unless directly observed.
