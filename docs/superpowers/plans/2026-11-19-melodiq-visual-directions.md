# MelodIQ Visual Directions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** deliver an expandable, product-selected visual-direction catalog with a scoped internal-console Glassmorphism default and optional Neumorphism, correcting Handbook routing and visual-policy contradictions.

**Architecture:** the machine-readable catalog is data, validated/resolved by a small standard-library module and exposed through existing CLI/discovery. Canonical Patterns own human guidance. Existing task/context compiler receives scoped evidence; product repositories own active visual implementation.

**Tech Stack:** Python 3.10+, JSON, Markdown, existing unittest suite and deterministic compiler.

**Spec:** `docs/superpowers/specs/2026-11-19-melodiq-visual-direction-catalog-design.md`

## Global Constraints

- Owner selected approach A, product-level direction; runtime/per-user selector B is deferred.
- Explicit authorized task direction > explicit current local design > default `internal-console: glassmorphism` > no default for non-console surfaces.
- No automatic UI migration, new shared package, arbitrary executable registry fields, new paid service or GitHub Actions cost.
- UI/UX quality, accessibility, product/tenant identity, clinical/financial truth and actual visual acceptance remain controlling.
- One normal branch/worktree; preserve meaningful Nov 16 history and all unrelated edits.

## Review Focus

1. Local explicit `neumorphism` or `solid-editorial` must override the glass default; an authorized explicit task choice can supersede the local aesthetic.
2. Public web/field/clinical phrases must never receive the internal-console default merely because they mention a MelodIQ product.
3. Negated or contrasted styles (e.g. “no glass, use neumorphism”) must not silently select the rejected material.
4. A console redesign without an explicit material should find the catalog; minor text fixes and CRM backend/auth changes must not trigger material redesign.
5. Unknown/invalid catalog entries and stale bundle/compiled references must fail explicitly; a future valid entry must be selectable without a hardcoded route change.

---

### Task 1: Selectable machine-readable catalog and CLI

**Files:**
- Create: `machine-readable/visual-directions.v1.json`, `automation/engineering_context/visual_directions.py`, `tests/engineering_context/test_visual_directions.py`
- Modify: `automation/engineering_context/cli.py`, `automation/engineering_context/discovery.py`

**Interfaces:**
- `load_visual_catalog(root: Path) -> dict`: validate `melodiq-visual-directions/v1`, unique/valid style IDs, aliases, references, allowed surfaces and defaults; no code execution.
- `resolve_visual_direction(root: Path, surface: str, task_style: str | None = None, local_style: str | None = None) -> dict`: chosen ID or `None`, source, reference and explanation; explicit unknown styles raise `ValueError`.
- `detect_visual_styles(text: str, root: Path | None = None) -> tuple[str, ...]`: normalized catalog aliases, negative style mentions excluded; ambiguity retained for agent resolution.
- `visual-directions --root ... [--surface ...] [--style ...] [--local-style ...]`: JSON result or catalog listing, no runtime UI preference.

- [ ] Write tests for default, explicit, local, public undecided, rejected/unknown and extensible choices; malformed catalogs, CLI listing/selection and integrity failures. Regression that would fail: wrong precedence or silent style fallback.
- [ ] Run focused unittest and observe RED for absent catalog/resolver/command.
- [ ] Implement data and minimal resolver/CLI/integrity integration.
- [ ] Run focused unittest to GREEN; run existing discovery/integrity tests.

### Task 2: Task-trigger and capsule routing

**Files:**
- Modify: `automation/engineering_context/task_descriptor.py`, `automation/engineering_context/discovery_rules.py` only if negative language requires it, `tests/engineering_context/test_contract_pipeline.py`, `tests/engineering_context/test_visual_directions.py`
- Create: no extra routing registry; use the existing visual feature-extractor boundary.

**Interfaces:**
- `archetype:operator-visual-direction-choice` for materially visual new/redesigned internal consoles; `archetype:operator-neumorphic-material-change` for explicitly selected internal Neumorphism; existing `operator-glass-material-change` retained for explicit internal Glassmorphism.
- Ordinary public sites, backend work, read-only explanations and micro-edits do not inherit the default. A style mention does not grant mutation authority.

- [ ] Write RED regression tests for ES/EN default internal redesign, explicit Neumorphism/Glass, public exclusion, read-only/no-op/negated styles, backend and micro-edit exclusions; assert phase capsules once canonical units exist.
- [ ] Run focused tests and observe expected failures.
- [ ] Implement minimal scoped evidence/routing; remove duplicate hardcoded style aliases in favor of catalog data.
- [ ] Run routing/front-end/marketing tests to GREEN.

### Task 3: Canonical design and distribution reconciliation

**Files:**
- Create: `patterns/visual-direction-catalog.md`, `patterns/operator-neumorphic-surface-material.md`, `decisions/0013-melodiq-visual-direction-catalog.md`
- Modify: `patterns/operator-glass-surface-material.md`, `patterns/design-context-layering.md`, `patterns/operator-console-shell-interactions.md`, `standards/ui-ux-quality-baseline.md`, `playbooks/frontend-quality-review.md`, `README.md`, `agent-config/codex/AGENTS.global.md`, `agent-config/codex/skills/engineering-handbook/SKILL.md`, `agent-config/codex/skills/engineering-handbook/bundle.json`, `machine-readable/catalog.yaml`, `machine-readable/discovery/taxonomy.v1.json`, generated `machine-readable/compiled/*`.

**Interfaces:**
- One catalog-selection context unit, glass material acceptance and Neumorphism-specific acceptance; all cross-references use catalog IDs. `search`/knowledge tree can find the catalog with Spanish/English aliases. No release/adoption claim.

- [ ] Write RED tests that search/discover the new catalog and select expected compiled units for internal/explicit material tasks; validate distribution includes catalog source. Test user-visible routing, not mere prose substrings.
- [ ] Run focused tests to confirm RED.
- [ ] Add canonical material guidance, scoped default, historical amendment and minimal links; register sources/catalog/taxonomy and bundle.
- [ ] Regenerate the compiled corpus; run context/search/integrity/freshness tests to GREEN.

### Task 4: Contradiction audit and release verification

**Files:**
- Modify only directly conflicting visual documents or regressions surfaced by the audit.

**Interfaces:**
- `python -m automation.engineering_context check --root .`, `doctor`, `integrity`, all `tests/engineering_context/test_*.py`, `git diff --check`.

- [ ] Search active canonical Markdown, global baseline and router for outdated “glass never default” or implicit runtime-toggle claims; make scoped fixes with regression evidence where executable.
- [ ] Run full fresh suite and compiled/integrity checks, inspect changed-file diff and verify no product UI repository was mutated.
- [ ] Request a read-only whole-branch review for routing, default boundaries, negation and generated/distribution consistency. Fix material findings with one RED→GREEN pass.
- [ ] Integrate/publish only within user-authorized repository workflow; report exact commit/tree and observed verification. Native consumer adoption remains a separate gate.
