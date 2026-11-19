# Code craft, maintenance and repository structure — implementation design

Date: 2026-11-19. Scope: the cross-repository Engineering Handbook and its Codex discovery/runtime projections, **not** changes to any product repository.

## Problem and outcome

The Handbook already owns reuse, supply-chain, architecture, testing and the general engineering workflow, but a coding task does not reliably lead an agent to one clear answer about names, modules, folder placement, libraries, code cleanup or safe refactoring. In particular, the generic intent registry does not recognise several ordinary code-edit verbs. The outcome is an efficient, discoverable end-to-end coding workflow and executable routing regressions, without a promise of zero possible defects.

## Approaches

1. **Expand the generic engineering-change playbook only:** minimal new files, but code-specific detail becomes difficult to discover and load selectively.
2. **Canonical coding standard plus focused playbook and typed discovery (chosen):** the standard owns cross-repository expectations; the focused playbook operationalizes them; existing policy/standards retain their original domains. Codex gets small, phase-specific context and accurate file discovery.
3. **One universal multi-language folder/naming/libraries tree:** apparently uniform, but would conflict with actual repository and framework conventions and encourages unnecessary churn.

The owner requested full implementation without repeated confirmation. The selected approach is an execution judgment, not a claim of an explicit prior choice between these three options.

## Canonical boundaries

- New `std-code-quality-organization-baseline` governs readable identifiers and units, cohesion, dependency direction, API boundaries, error handling, observability, comments and structurally safe code evolution. It prescribes no fixed package manager, syntax style, folder template, framework, library, formatter or LOC limit.
- New `pb-code-change-workflow` walks **local context → contract → tests → implementation → dependency decision → restructure/cleanup → verification → handoff**, proportionately. It links `pol-reuse-first`, `std-dependency-supply-chain-baseline`, `std-architecture-data-integrity-baseline`, `std-testing-release-quality-baseline` and existing security/UI standards without restating their normative text.
- The existing `pb-engineering-change` remains the one top-level engineering lifecycle. It routes code work to the focused guide. The existing supply-chain Standard remains the owner for library selection and version/lockfile/security/lifecycle requirements.
- Source code and tests keep the repository's existing local conventions (`AGENTS.md`, ADRs, tooling, language rules) unless explicitly and safely changed. No blind rename, mass move, new abstraction/dependency, or hidden behavior change under a “cleanup” label.
- No external package install, plugin, paid CI, arbitrary code execution from a registry, product-repository migration or deployment.

## Routing contract

- Declarative bilingual task recognition for `archetype:code-change`, `archetype:code-organization` and `archetype:dependency-selection`. Positive examples: implement a function, refactor a module, rename a variable, reorganize source folders, replace a package, select a library, repair source code, or change a source file.
- Review/diagnosis is **not** edit authorization. Questions, prohibited operations, marketing copy, docs/README prose, CSS class naming, user-folder housekeeping and generated/vendor source examples must not turn into an implementation task. Mixed positive/negative clauses preserve the affirmative code operation.
- Source path routing accounts for real code languages, tests and package manifests; excludes clearly generated/vendor and documentation/example paths. A repo's normal source conventions and manifests are discoverable through versioned landmarks; unknown paths remain unresolved, not guessed.
- Planning capsule asks about owner, contract, scope, reuse and dependency fit; implementation capsule covers names/module boundaries/errors and ordinary code changes; verification capsule covers semantic behavior, interfaces and risk-selected gates. Registry predicates and canonical unit IDs remain stable and testable; categorization never grants write authority.
- Search/knowledge tree returns the canonical code standard and code playbook in ES/EN queries. Skill/global baseline briefly route code tasks there; no second hand-maintained router is introduced.

## Acceptance and risk

- Regression tests exercise real `describe_task`, `build_repo_route`, `solve_context`, `search` and `knowledge_tree` behavior for Spanish and English positive, negative, mixed, path-only and no-authority cases; no source-text-only assertions.
- The compile/check/doctor/integrity commands and the entire engineering-context unittest suite pass on final bytes; no unnecessary generated output or hook/bootstrap semantics change.
- One read-only independent review checks contradictions, false-positive routes, missing gates, bundle contents and cross-repository scope before publication.
- Static/lexical discovery cannot prove perfect natural-language understanding; a `needs-discovery` or unresolved path still calls for agent judgment. Publication changes Handbook source; installed consumer snapshots need their existing safe refresh.
