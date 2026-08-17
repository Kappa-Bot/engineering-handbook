# Handbook Compiler & Agent Context Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, model-neutral pipeline that compiles handbook knowledge and repository orientation ahead of time, then gives coding agents the minimum sufficient context for planning, implementation, and verification.

**Architecture:** Python standard-library tooling compiles explicit structured `agent-context` blocks embedded in authoritative handbook Markdown into versioned JSON indexes. Consumer repositories can be incrementally profiled into a compact repo atlas. A multidimensional task descriptor plus repo facts drives a deterministic minimum-cover solver that emits planning/implementation/verification capsules and a structured Planning IR; semantic ambiguity is surfaced to the already-active agent rather than causing a second model call.

**Tech Stack:** Python 3.11+ standard library only (`argparse`, `dataclasses`, `hashlib`, `json`, `pathlib`, `re`, `subprocess`, `unittest`); Markdown remains authoritative; generated machine artifacts are deterministic JSON; Git/GitHub Actions provide freshness verification.

## Global Constraints

- Zero subagents by default for this repository; use `superpowers:executing-plans` for implementation unless the user explicitly overrides this preference.
- Do not add embeddings, a vector database, graph database, daemon, remote context service, or secondary LLM/API call.
- Do not add a runtime third-party dependency merely to parse handbook metadata.
- Authoritative handbook Markdown and repo-local canonical decisions remain the source of truth; compiled files are generated views only.
- Semantic units MUST be explicitly structured in authoritative Markdown; the compiler MUST NOT infer normative meaning from arbitrary prose.
- Generated handbook artifacts are versioned in Git and MUST be byte-stable for identical semantic inputs.
- Task-specific capsules and transient caches MUST NOT be committed.
- Structural/diff evidence may add risk; natural-language task wording may not suppress structurally demonstrated risk.
- The hot path MUST prefer deterministic lookup over repository rediscovery or full handbook reads.
- Planner, implementer, and verifier receive different compact views rather than one universal context dump.
- Context selection optimizes total engineering cost, not token count in isolation.
- Default planning capsule budget: target 600 estimated tokens, soft maximum 900, hard maximum 1400, with 250 tokens reserved for unresolved-risk escalation.
- Full canonical handbook reads are escalation behavior, not normal routing behavior.
- Existing repositories without compiled intelligence MUST remain usable through graceful fallback.
- No claim that a verification gate passed unless it was actually executed and observed.

---

## File Structure

Create the context engine as one focused Python package under existing `automation/` rather than as another agent skill. Keep the current generic handbook skill as the agent-facing router/fallback.

```text
automation/
├── __init__.py
└── engineering_context/
    ├── __init__.py
    ├── __main__.py
    ├── canonical.py          # stable JSON, hashing, token estimates, IDs
    ├── handbook_source.py    # explicit agent-context block extraction/validation
    ├── handbook_compile.py   # DAG/index/view compilation + incremental manifest
    ├── repo_profile.py       # detected/declared repo intelligence
    ├── task_descriptor.py    # multidimensional task/change descriptor
    ├── context_solver.py     # applicability, dedupe, weighted minimum cover, budgets
    ├── planning_ir.py        # Planning IR, validation, views/deltas
    ├── conformance.py        # required vs demonstrated vs exception projection
    └── cli.py                # single agent/tooling entry point

tests/
└── engineering_context/
    ├── __init__.py
    ├── test_canonical.py
    ├── test_handbook_source.py
    ├── test_handbook_compile.py
    ├── test_repo_profile.py
    ├── test_task_descriptor.py
    ├── test_context_solver.py
    ├── test_planning_ir.py
    ├── test_conformance.py
    ├── test_cli.py
    └── fixtures/
        ├── handbook/
        ├── repos/
        │   ├── ts_web/
        │   └── sparse_repo/
        └── tasks/

machine-readable/
└── compiled/
    ├── manifest.json
    ├── graph.json
    ├── routing.json
    ├── planning.json
    ├── implementation.json
    └── verification.json

.github/workflows/
└── handbook-context.yml
```

Authoritative handbook pages that receive `agent-context` blocks in this PR:

```text
policies/truthful-engineering.md
policies/reuse-first.md
policies/verification-definition-of-done.md
standards/architecture-data-integrity-baseline.md
standards/security-identity-baseline.md
standards/testing-release-quality-baseline.md
standards/production-operability-baseline.md
standards/dependency-supply-chain-baseline.md
standards/ui-ux-quality-baseline.md
standards/web-pwa-baseline.md
patterns/authorization-privileged-boundaries.md
patterns/token-secret-link-handling.md
patterns/risk-based-verification-matrix.md
patterns/release-provenance-environment-gates.md
patterns/observability-signals.md
patterns/api-contract-evolution.md
patterns/performance-budgeting.md
patterns/mobile-responsive-interaction.md
patterns/visual-evidence-integrity.md
```

Integration files modified near the end:

```text
README.md
CONTRIBUTING.md
agent-config/codex/AGENTS.global.md
agent-config/codex/skills/engineering-handbook/SKILL.md
machine-readable/catalog.yaml
```

The existing `automation/handbook/check-integrity.ps1` stays authoritative for its current checks during this PR. The new Python pipeline adds its own portable `check` gate; replacement of every legacy registry check is not required to make the context pipeline useful and is deferred unless implementation proves it can be done without weakening validation.

---

### Task 1: Canonical Data Primitives

**Files:**
- Create: `automation/__init__.py`
- Create: `automation/engineering_context/__init__.py`
- Create: `automation/engineering_context/canonical.py`
- Create: `tests/engineering_context/__init__.py`
- Create: `tests/engineering_context/test_canonical.py`

**Interfaces:**
- Produces: `canonical_json(value: object) -> str`
- Produces: `sha256_text(value: str) -> str`
- Produces: `stable_hash(value: object) -> str`
- Produces: `estimate_tokens(text: str) -> int`
- Produces: `context_id(*parts: object) -> str`
- Later tasks consume these functions for deterministic manifests, cache keys, and budget calculations.

- [ ] **Step 1: Write failing deterministic serialization/hash tests**

```python
# tests/engineering_context/test_canonical.py
import unittest

from automation.engineering_context.canonical import (
    canonical_json,
    context_id,
    estimate_tokens,
    stable_hash,
)


class CanonicalTests(unittest.TestCase):
    def test_canonical_json_sorts_keys_and_has_no_incidental_whitespace(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}\n')

    def test_stable_hash_is_order_independent_for_object_keys(self):
        self.assertEqual(stable_hash({"a": 1, "b": 2}), stable_hash({"b": 2, "a": 1}))

    def test_context_id_changes_when_any_input_changes(self):
        first = context_id("handbook-a", "repo-a", {"risk": ["credential"]})
        second = context_id("handbook-a", "repo-a", {"risk": ["privilege"]})
        self.assertNotEqual(first, second)

    def test_token_estimator_is_deterministic_and_nonzero_for_text(self):
        self.assertGreater(estimate_tokens("authorization at server boundary"), 0)
        self.assertEqual(estimate_tokens("same text"), estimate_tokens("same text"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify failure**

Run:

```bash
python -m unittest tests.engineering_context.test_canonical -v
```

Expected: import/module failure because the package/functions do not exist yet.

- [ ] **Step 3: Implement minimal canonical primitives**

```python
# automation/engineering_context/canonical.py
from __future__ import annotations

import hashlib
import json
import math
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def estimate_tokens(text: str) -> int:
    # Deliberately cheap and deterministic. This is a budget heuristic, not tokenizer truth.
    return max(1, math.ceil(len(text.encode("utf-8")) / 4)) if text else 0


def context_id(*parts: Any) -> str:
    return stable_hash(list(parts))
```

- [ ] **Step 4: Run the test and the package-wide test discovery**

```bash
python -m unittest tests.engineering_context.test_canonical -v
python -m unittest discover -s tests/engineering_context -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/__init__.py automation/engineering_context/__init__.py automation/engineering_context/canonical.py tests/engineering_context
git commit -m "feat: add deterministic context primitives"
```

---

### Task 2: Explicit Authoritative Agent-Context Blocks

**Files:**
- Create: `automation/engineering_context/handbook_source.py`
- Create: `tests/engineering_context/test_handbook_source.py`
- Create fixture: `tests/engineering_context/fixtures/handbook/security.md`
- Create fixture: `tests/engineering_context/fixtures/handbook/invalid.md`
- Modify initially: `policies/truthful-engineering.md`
- Modify initially: `standards/security-identity-baseline.md`

**Interfaces:**
- Produces dataclass: `KnowledgeUnit`
- Produces: `extract_source_id(markdown: str) -> str`
- Produces: `extract_agent_context(markdown: str, path: str) -> list[KnowledgeUnit]`
- A structured block is fenced exactly as ` ```json agent-context` ... ` ``` `.
- Compiler MUST reject unknown unit types, missing IDs, mismatched `source`, duplicate IDs within a page, invalid force, and malformed JSON.

**Required `KnowledgeUnit` fields:**

```python
@dataclass(frozen=True)
class KnowledgeUnit:
    id: str
    type: str
    text: str
    source: str
    covers: tuple[str, ...]
    activate_when: tuple[str, ...]
    force: str | None = None
    phase: tuple[str, ...] = ()
    priority: int = 50
    requires: tuple[str, ...] = ()
    excludes: tuple[str, ...] = ()
```

Allowed types: `constraint`, `decision-question`, `risk`, `pattern`, `anti-pattern`, `verification`, `escalation`, `route-hint`.

Allowed force: `must`, `must-not`, `should`, `may`, or omitted.

- [ ] **Step 1: Write failing parser/schema tests**

```python
# tests/engineering_context/test_handbook_source.py
import unittest
from pathlib import Path

from automation.engineering_context.handbook_source import AgentContextError, extract_agent_context

FIXTURES = Path(__file__).parent / "fixtures" / "handbook"


class HandbookSourceTests(unittest.TestCase):
    def test_extracts_explicit_units_without_interpreting_free_prose(self):
        units = extract_agent_context((FIXTURES / "security.md").read_text(), "security.md")
        self.assertEqual([u.id for u in units], ["authz-boundary", "authz-negative-case"])
        self.assertEqual(units[0].source, "std-test-security")
        self.assertIn("risk:privilege", units[0].activate_when)

    def test_rejects_source_mismatch(self):
        with self.assertRaises(AgentContextError):
            extract_agent_context((FIXTURES / "invalid.md").read_text(), "invalid.md")

    def test_free_markdown_without_block_yields_no_units(self):
        self.assertEqual(extract_agent_context("# Title\nNormal prose only.\n", "plain.md"), [])
```

Fixture `security.md` must contain frontmatter `id: std-test-security` and:

````markdown
```json agent-context
{
  "units": [
    {
      "id": "authz-boundary",
      "type": "constraint",
      "text": "Enforce authorization at an authoritative server/data boundary.",
      "source": "std-test-security",
      "covers": ["authorization", "privilege", "tenant-isolation"],
      "activate_when": ["operation:authorization", "risk:privilege"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
    {
      "id": "authz-negative-case",
      "type": "verification",
      "text": "Verify an unauthorized actor is denied.",
      "source": "std-test-security",
      "covers": ["authorization"],
      "activate_when": ["operation:authorization"],
      "phase": ["verification"],
      "priority": 90
    }
  ]
}
```
````

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_handbook_source -v
```

Expected: FAIL because parser/dataclass do not exist.

- [ ] **Step 3: Implement strict extraction without a general Markdown/YAML inference layer**

Implementation requirements:

```python
AGENT_CONTEXT_OPEN = "```json agent-context"
ALLOWED_TYPES = {
    "constraint", "decision-question", "risk", "pattern",
    "anti-pattern", "verification", "escalation", "route-hint",
}
ALLOWED_PHASES = {"planning", "implementation", "verification"}
ALLOWED_FORCE = {"must", "must-not", "should", "may"}
```

`extract_source_id()` must parse only a top-level frontmatter scalar matching `^id:\s*([^\s]+)\s*$` between the first two `---` delimiters. It is intentionally **not** a YAML parser. All agent semantics live in JSON blocks.

`extract_agent_context()` must use `json.loads()` only on explicit blocks and never derive `text`, `covers`, force, or applicability from surrounding prose.

- [ ] **Step 4: Add the first real source blocks and run tests**

Add small, non-duplicative structured blocks to `policies/truthful-engineering.md` and `standards/security-identity-baseline.md`. Every unit text must be a compact faithful expression of an already-authoritative statement in that page; do not strengthen force.

Run:

```bash
python -m unittest tests.engineering_context.test_handbook_source -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/handbook_source.py tests/engineering_context/test_handbook_source.py tests/engineering_context/fixtures/handbook policies/truthful-engineering.md standards/security-identity-baseline.md
git commit -m "feat: add explicit handbook agent context contracts"
```

---

### Task 3: Incremental Handbook Compiler and Versioned Views

**Files:**
- Create: `automation/engineering_context/handbook_compile.py`
- Create: `tests/engineering_context/test_handbook_compile.py`
- Generate: `machine-readable/compiled/manifest.json`
- Generate: `machine-readable/compiled/graph.json`
- Generate: `machine-readable/compiled/routing.json`
- Generate: `machine-readable/compiled/planning.json`
- Generate: `machine-readable/compiled/implementation.json`
- Generate: `machine-readable/compiled/verification.json`

**Interfaces:**
- Produces: `compile_handbook(root: Path, output_dir: Path) -> CompileResult`
- Produces: `check_compiled_fresh(root: Path, output_dir: Path) -> list[str]`
- `CompileResult` exposes `changed_files: tuple[str, ...]`, `skipped_sources: tuple[str, ...]`, and `handbook_hash: str`.
- Compiled views contain normalized unit records, not page summaries.

- [ ] **Step 1: Write failing compile/determinism/incremental tests**

```python
# tests/engineering_context/test_handbook_compile.py
import tempfile
import unittest
from pathlib import Path

from automation.engineering_context.handbook_compile import compile_handbook


class HandbookCompileTests(unittest.TestCase):
    def test_recompile_without_source_change_is_byte_stable(self):
        fixture = Path(__file__).parent / "fixtures" / "handbook"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "compiled"
            first = compile_handbook(fixture, out)
            first_bytes = {p.name: p.read_bytes() for p in out.glob("*.json")}
            second = compile_handbook(fixture, out)
            second_bytes = {p.name: p.read_bytes() for p in out.glob("*.json")}
            self.assertEqual(first_bytes, second_bytes)
            self.assertTrue(second.skipped_sources)
            self.assertEqual(first.handbook_hash, second.handbook_hash)

    def test_planning_view_excludes_verification_only_unit(self):
        fixture = Path(__file__).parent / "fixtures" / "handbook"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "compiled"
            compile_handbook(fixture, out)
            planning = (out / "planning.json").read_text()
            self.assertNotIn('"authz-negative-case"', planning)
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_handbook_compile -v
```

Expected: FAIL because compiler does not exist.

- [ ] **Step 3: Implement compiler, inverted routing index, dependency graph, and hashes**

Manifest schema must contain:

```json
{
  "schema": "handbook-compiled/v1",
  "compiler_schema": 1,
  "handbook_hash": "sha256:...",
  "sources": {
    "std-test-security": {
      "path": "security.md",
      "source_hash": "sha256:...",
      "dependency_hash": "sha256:...",
      "output_hash": "sha256:..."
    }
  }
}
```

`routing.json` maps normalized predicates to unit IDs. Example:

```json
{
  "operation:authorization": ["authz-boundary", "authz-negative-case"],
  "risk:privilege": ["authz-boundary"]
}
```

`graph.json` represents `requires` edges only; no recursive runtime discovery is allowed.

Compilation rules:

1. discover `*.md` under canonical handbook taxonomy directories plus policies/standards/patterns/playbooks/governance;
2. parse only explicit blocks;
3. reject duplicate global unit IDs;
4. canonical-sort records by `id` and predicates lexicographically;
5. omit volatile timestamps from hashed/generated semantic output;
6. skip unchanged source parsing when `source_hash` and compiler schema match the previous manifest; reuse previous normalized source units from the existing view data;
7. propagate changes only across explicit `requires` descendants.

- [ ] **Step 4: Generate real compiled output twice and verify zero semantic diff on second run**

Run:

```bash
python -m automation.engineering_context.handbook_compile . machine-readable/compiled
python -m automation.engineering_context.handbook_compile . machine-readable/compiled
python -m unittest tests.engineering_context.test_handbook_compile -v
```

Expected: second compile reports no changed compiled files; tests PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/handbook_compile.py tests/engineering_context/test_handbook_compile.py machine-readable/compiled
git commit -m "feat: compile handbook context deterministically"
```

---

### Task 4: Repo Intelligence Compiler

**Files:**
- Create: `automation/engineering_context/repo_profile.py`
- Create: `tests/engineering_context/test_repo_profile.py`
- Create fixtures under: `tests/engineering_context/fixtures/repos/ts_web/`
- Create fixtures under: `tests/engineering_context/fixtures/repos/sparse_repo/`

**Interfaces:**
- Produces: `profile_repo(root: Path, previous: dict | None = None) -> dict`
- Produces: `write_repo_profile(root: Path, output_dir: Path) -> dict`
- Optional authoritative repo config path: `.engineering/context.json`
- Generated output path in a consumer repo: `.engineering/compiled/`
- Detected facts and declared decisions MUST be separate keys.

- [ ] **Step 1: Write failing profile tests**

```python
# tests/engineering_context/test_repo_profile.py
import unittest
from pathlib import Path

from automation.engineering_context.repo_profile import profile_repo

FIXTURES = Path(__file__).parent / "fixtures" / "repos"


class RepoProfileTests(unittest.TestCase):
    def test_detects_high_value_repo_facts(self):
        profile = profile_repo(FIXTURES / "ts_web")
        self.assertEqual(profile["detected"]["package_manager"], "pnpm")
        self.assertTrue(profile["detected"]["capabilities"]["persistence"])
        self.assertIn("test", profile["detected"]["commands"])

    def test_declared_decision_is_not_rewritten_as_detected_fact(self):
        profile = profile_repo(FIXTURES / "ts_web")
        self.assertEqual(profile["declared"]["decisions"]["persistence_owner"], "postgres")

    def test_sparse_repo_preserves_unknowns(self):
        profile = profile_repo(FIXTURES / "sparse_repo")
        self.assertIsNone(profile["detected"]["package_manager"])
        self.assertEqual(profile["detected"]["commands"], {})
```

Fixture `ts_web/.engineering/context.json`:

```json
{
  "schema": "repo-context/v1",
  "decisions": {
    "persistence_owner": "postgres",
    "offline_writes": "unsupported"
  },
  "landmarks": {
    "domain-mutation": ["src/server/moves/create.ts"]
  }
}
```

Fixture `ts_web/package.json` must include scripts `test`, `lint`, `build`; create `pnpm-lock.yaml`, `supabase/migrations/001.sql`, `.github/workflows/ci.yml`, and `tests/moves.test.ts` as zero/minimal-content markers.

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_repo_profile -v
```

Expected: FAIL because profiler does not exist.

- [ ] **Step 3: Implement bounded structural detection**

Detection must be limited to high-value landmarks and known metadata:

```python
LOCKFILES = {
    "pnpm-lock.yaml": "pnpm",
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
    "bun.lockb": "bun",
}

MIGRATION_HINTS = ("supabase/migrations", "migrations", "prisma/migrations")
TEST_HINTS = ("tests", "test", "__tests__", "e2e")
PWA_HINTS = ("manifest.webmanifest", "manifest.json", "service-worker.js", "sw.js")
```

Do not recursively parse application source. Read `package.json` scripts exactly if present. Read `.engineering/context.json` exactly if present. Record segment hashes for `runtime`, `delivery`, `persistence`, `verification`, and `declared` so later runs can reuse unchanged segments.

- [ ] **Step 4: Prove incremental segment reuse**

Extend the test to pass a previous profile, alter only an unrelated fixture component, and assert `runtime`, `delivery`, and `persistence` segment hashes remain unchanged.

Run:

```bash
python -m unittest tests.engineering_context.test_repo_profile -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/repo_profile.py tests/engineering_context/test_repo_profile.py tests/engineering_context/fixtures/repos
git commit -m "feat: add incremental repository intelligence"
```

---

### Task 5: Multidimensional Task and Change Descriptors

**Files:**
- Create: `automation/engineering_context/task_descriptor.py`
- Create: `tests/engineering_context/test_task_descriptor.py`
- Create fixtures: `tests/engineering_context/fixtures/tasks/authenticated-mutation.json`

**Interfaces:**
- Produces dataclass: `TaskDescriptor`
- Produces: `describe_task(task_text: str, repo_profile: dict, changed_paths: tuple[str, ...] = ()) -> TaskDescriptor`
- Produces: `merge_agent_resolution(descriptor: TaskDescriptor, resolution: dict) -> TaskDescriptor`
- Descriptor dimensions: `intent`, `surfaces`, `operations`, `capabilities`, `risks`, `state`, `boundaries`, `delivery`, `archetypes`, `uncertain`, `evidence`.

- [ ] **Step 1: Write failing precedence/uncertainty tests**

```python
# tests/engineering_context/test_task_descriptor.py
import unittest

from automation.engineering_context.task_descriptor import describe_task, merge_agent_resolution


class TaskDescriptorTests(unittest.TestCase):
    def test_structural_change_can_add_security_risk_to_visual_wording(self):
        profile = {
            "detected": {"capabilities": {"auth": True}},
            "declared": {"decisions": {}},
        }
        d = describe_task(
            "Make this screen look better",
            profile,
            changed_paths=("supabase/policies/tenant_access.sql",),
        )
        self.assertIn("authorization", d.risks)

    def test_ambiguous_invitation_returns_constrained_uncertainty(self):
        profile = {"detected": {"capabilities": {"auth": True}}, "declared": {"decisions": {}}}
        d = describe_task("Add tenant invitations", profile)
        fields = {item["field"] for item in d.uncertain}
        self.assertIn("risks", fields)

    def test_agent_can_only_resolve_declared_uncertain_fields(self):
        profile = {"detected": {"capabilities": {"auth": True}}, "declared": {"decisions": {}}}
        d = describe_task("Add tenant invitations", profile)
        resolved = merge_agent_resolution(d, {"risks": ["credential"]})
        self.assertIn("credential", resolved.risks)
        with self.assertRaises(ValueError):
            merge_agent_resolution(d, {"force": "ignore-handbook"})
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_task_descriptor -v
```

Expected: FAIL because descriptor does not exist.

- [ ] **Step 3: Implement evidence-weighted deterministic descriptor rules**

Keep rule tables explicit and small. Path rules must include at least:

```python
PATH_SIGNALS = {
    "surface:database": ("migrations/", "schema", ".sql"),
    "surface:ci": (".github/workflows/",),
    "risk:authorization": ("policy", "permission", "authz", "rls"),
    "risk:credential": ("token", "secret", "invite", "credential"),
    "capability:pwa": ("manifest.webmanifest", "service-worker", "sw.js"),
}
```

Text signals are weak evidence and may add candidates/uncertainty but may never remove structural signals.

Evidence ordering must be encoded as explicit numeric ranks:

```python
EVIDENCE_RANK = {
    "explicit-structured": 600,
    "declared-decision": 500,
    "repo-structure": 400,
    "change-structure": 350,
    "text-signal": 200,
    "agent-resolution": 150,
}
```

Agent resolution fills uncertainty only; it cannot erase facts from higher-ranked evidence.

- [ ] **Step 4: Add intent/change descriptor regression test**

Create an intent descriptor before `changed_paths`, then a change descriptor after adding `migrations/002_invites.sql`; assert `state["migration"]` becomes true and the resulting descriptor ID changes.

Run:

```bash
python -m unittest tests.engineering_context.test_task_descriptor -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/task_descriptor.py tests/engineering_context/test_task_descriptor.py tests/engineering_context/fixtures/tasks
git commit -m "feat: derive deterministic task descriptors"
```

---

### Task 6: Minimum-Cover Context Solver and Token Budgets

**Files:**
- Create: `automation/engineering_context/context_solver.py`
- Create: `tests/engineering_context/test_context_solver.py`

**Interfaces:**
- Produces: `solve_context(compiled: dict, descriptor: TaskDescriptor, phase: str, budget: ContextBudget = DEFAULT_BUDGET) -> ContextCapsule`
- `ContextBudget(target=600, soft_max=900, hard_max=1400, reserve=250)` for planning by default.
- `ContextCapsule` exposes `id`, `phase`, `units`, `covered`, `uncovered`, `estimated_tokens`, `escalations`, `provenance`.

- [ ] **Step 1: Write failing selection/dedup/budget tests**

```python
# tests/engineering_context/test_context_solver.py
import unittest

from automation.engineering_context.context_solver import ContextBudget, solve_context
from automation.engineering_context.task_descriptor import TaskDescriptor


class ContextSolverTests(unittest.TestCase):
    def test_selects_smaller_unit_that_covers_same_risks(self):
        compiled = {
            "units": [
                {"id": "small", "text": "server authz", "covers": ["authorization", "privilege"], "estimated_tokens": 10, "priority": 90, "phase": ["planning"]},
                {"id": "large", "text": "long duplicate guidance", "covers": ["authorization", "privilege"], "estimated_tokens": 200, "priority": 90, "phase": ["planning"]},
            ]
        }
        d = TaskDescriptor.for_test(risks=("authorization", "privilege"))
        capsule = solve_context(compiled, d, "planning")
        self.assertEqual([u["id"] for u in capsule.units], ["small"])

    def test_same_semantic_unit_is_emitted_once_with_multiple_sources(self):
        compiled = {"units": [
            {"id": "authz", "text": "server authz", "covers": ["authorization"], "sources": ["std-a", "pb-b"], "estimated_tokens": 10, "priority": 90, "phase": ["planning"]}
        ]}
        d = TaskDescriptor.for_test(risks=("authorization",))
        capsule = solve_context(compiled, d, "planning")
        self.assertEqual(len(capsule.units), 1)
        self.assertEqual(capsule.units[0]["sources"], ["std-a", "pb-b"])

    def test_hard_budget_never_silently_drops_required_uncovered_risk(self):
        compiled = {"units": []}
        d = TaskDescriptor.for_test(risks=("credential",))
        capsule = solve_context(compiled, d, "planning", ContextBudget(10, 20, 30, 5))
        self.assertEqual(capsule.uncovered, ("credential",))
        self.assertTrue(capsule.escalations)
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_context_solver -v
```

Expected: FAIL because solver/capsule do not exist.

- [ ] **Step 3: Implement deterministic greedy weighted set cover**

Candidate score for each iteration:

```python
new_coverage = len(required - covered & set(unit["covers"]))
score = (new_coverage * max(1, unit.get("priority", 50))) / max(1, unit["estimated_tokens"])
```

Selection rules:

1. candidates must match phase;
2. candidates are retrieved from inverted predicates first, not by scanning canonical Markdown;
3. mandatory `requires` are included before optional guidance;
4. duplicate unit IDs collapse and merge provenance;
5. select units by descending score, then deterministic ID tie-break;
6. reserve is not consumed by optional units;
7. crossing soft max is allowed only to cover a previously uncovered required risk/invariant;
8. hard max may only be crossed by a force-`must` unit that is itself required; record an escalation if that happens;
9. any uncovered required risk produces an explicit escalation rather than fake completion.

- [ ] **Step 4: Add negative routing and phase-view tests**

Add tests proving a unit with `excludes=["surface:frontend"]` is not selected for a frontend-only descriptor and a verification-only unit is not in a planning capsule.

Run:

```bash
python -m unittest tests.engineering_context.test_context_solver -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/context_solver.py tests/engineering_context/test_context_solver.py
git commit -m "feat: solve minimum sufficient agent context"
```

---

### Task 7: Planning IR, Deterministic Validation, and Context Delta

**Files:**
- Create: `automation/engineering_context/planning_ir.py`
- Create: `tests/engineering_context/test_planning_ir.py`

**Interfaces:**
- Produces dataclasses: `PlanningIR`, `Decision`, `Invariant`, `VerificationRequirement`
- Produces: `new_planning_ir(descriptor: TaskDescriptor, capsule: ContextCapsule) -> PlanningIR`
- Produces: `validate_planning_ir(ir: PlanningIR) -> tuple[ValidationIssue, ...]`
- Produces: `render_plan_view(ir: PlanningIR) -> str`
- Produces: `render_spec_view(ir: PlanningIR) -> str`
- Produces: `capsule_delta(previous_id: str | None, previous_unit_ids: set[str], current: ContextCapsule) -> dict`

- [ ] **Step 1: Write failing IR validation/delta tests**

```python
# tests/engineering_context/test_planning_ir.py
import unittest

from automation.engineering_context.planning_ir import PlanningIR, validate_planning_ir


class PlanningIRTests(unittest.TestCase):
    def test_tenant_risk_requires_authorization_decision(self):
        ir = PlanningIR.for_test(risks=("tenant-isolation",), decisions=())
        issues = validate_planning_ir(ir)
        self.assertIn("missing-authorization-decision", {i.code for i in issues})

    def test_migration_requires_migration_verification(self):
        ir = PlanningIR.for_test(migration=True, verification=())
        issues = validate_planning_ir(ir)
        self.assertIn("missing-migration-verification", {i.code for i in issues})
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_planning_ir -v
```

Expected: FAIL because IR/validator do not exist.

- [ ] **Step 3: Implement Planning IR schema and initial deterministic validation rules**

Minimum IR serialized shape:

```json
{
  "schema": "planning-ir/v1",
  "context_id": "sha256:...",
  "task": {"objective": "...", "scope": [], "exclusions": []},
  "affected": {"capabilities": [], "boundaries": []},
  "decisions": [],
  "invariants": [],
  "state_transitions": [],
  "risks": [],
  "implementation_units": [],
  "verification": [],
  "unresolved": [],
  "provenance": []
}
```

Initial validation rules:

```text
risk tenant-isolation or privilege -> authorization decision required
risk credential -> credential lifecycle decision required
state.migration=true -> migration verification required
operation:integration -> failure/retry semantics decision required
production effect + deployment operation -> release identity/target verification required
uncovered capsule risk -> unresolved entry required
```

Validator reports issues; it never auto-invents the missing decision.

- [ ] **Step 4: Implement delta delivery and view renderers**

`capsule_delta()` returns:

```json
{
  "base_context_id": "...",
  "current_context_id": "...",
  "added_units": [],
  "removed_unit_ids": [],
  "unchanged_unit_count": 0
}
```

If no base context ID is supplied, return the full current unit set. The spec/plan renderers must render only populated sections and reference handbook unit/source IDs instead of duplicating canonical explanatory prose.

Run:

```bash
python -m unittest tests.engineering_context.test_planning_ir -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/planning_ir.py tests/engineering_context/test_planning_ir.py
git commit -m "feat: add structured planning IR and validation"
```

---

### Task 8: Conformance Projection and Evidence States

**Files:**
- Create: `automation/engineering_context/conformance.py`
- Create: `tests/engineering_context/test_conformance.py`

**Interfaces:**
- Produces: `project_conformance(capsule: ContextCapsule, ir: PlanningIR, evidence: tuple[dict, ...], exceptions: tuple[dict, ...] = ()) -> dict`
- Evidence status vocabulary: `passed`, `failed`, `not-run`, `not-applicable`.
- Conformance is derived as `required - demonstrated - declared exception`; it is not a parallel policy system.

- [ ] **Step 1: Write failing evidence-state tests**

```python
# tests/engineering_context/test_conformance.py
import unittest

from automation.engineering_context.conformance import project_conformance


class ConformanceTests(unittest.TestCase):
    def test_not_run_is_not_counted_as_demonstrated(self):
        result = project_conformance(
            capsule={"required_evidence": ["authz-negative"]},
            ir={"verification": ["authz-negative"]},
            evidence=({"id": "authz-negative", "status": "not-run"},),
        )
        self.assertIn("authz-negative", result["gaps"])

    def test_declared_exception_is_distinct_from_passed(self):
        result = project_conformance(
            capsule={"required_evidence": ["physical-device"]},
            ir={"verification": ["physical-device"]},
            evidence=(),
            exceptions=({"id": "physical-device", "reason": "not applicable to backend-only change"},),
        )
        self.assertIn("physical-device", result["exceptions"])
        self.assertNotIn("physical-device", result["demonstrated"])
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_conformance -v
```

Expected: FAIL because conformance module does not exist.

- [ ] **Step 3: Implement pure conformance projection**

No filesystem or network I/O in this module. Validate status vocabulary and preserve provenance of required evidence. `failed` and `not-run` remain gaps; `not-applicable` is accepted only when accompanied by an applicability reason or declared exception.

- [ ] **Step 4: Run tests**

```bash
python -m unittest tests.engineering_context.test_conformance -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/conformance.py tests/engineering_context/test_conformance.py
git commit -m "feat: derive engineering conformance from evidence"
```

---

### Task 9: Unified Agent-Facing CLI

**Files:**
- Create: `automation/engineering_context/cli.py`
- Create: `automation/engineering_context/__main__.py`
- Create: `tests/engineering_context/test_cli.py`

**Interfaces:**
- Single entry point: `python -m automation.engineering_context <command>`
- Commands: `compile-handbook`, `profile-repo`, `context`, `validate-plan`, `check`.
- `context --mode` values: `plan`, `implement`, `verify`.
- Default output: compact JSON to stdout; `--pretty` is human inspection only.

- [ ] **Step 1: Write failing CLI contract tests**

```python
# tests/engineering_context/test_cli.py
import json
import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "automation.engineering_context", *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_help_exposes_single_context_entry_point(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("context", result.stdout)
        self.assertIn("compile-handbook", result.stdout)

    def test_context_outputs_machine_readable_json(self):
        result = self.run_cli(
            "context",
            "--repo", "tests/engineering_context/fixtures/repos/ts_web",
            "--handbook", "machine-readable/compiled",
            "--mode", "plan",
            "--task", "Add tenant invitation expiration",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "plan")
        self.assertIn("context_id", payload)
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_cli -v
```

Expected: FAIL because `__main__`/CLI do not exist.

- [ ] **Step 3: Implement commands by composing existing modules**

Required command contracts:

```text
compile-handbook --root PATH --output PATH
profile-repo --repo PATH [--output PATH]
context --repo PATH --handbook PATH --mode plan|implement|verify --task TEXT [--changed PATH ...] [--base-context FILE]
validate-plan --input planning-ir.json
check --root PATH
```

`context` output must contain only:

```json
{
  "schema": "agent-context/v1",
  "mode": "plan",
  "context_id": "sha256:...",
  "descriptor": {},
  "repo_route": {},
  "capsule": {},
  "uncertain": [],
  "planning_ir_seed": {}
}
```

For `implement`, include settled decisions/invariants and omit planning questions already resolved. For `verify`, include required evidence, actual changed-scope risks, and unresolved evidence gaps.

`check` must run: source-block validation, compiled freshness comparison in a temporary directory, duplicate unit ID validation, graph dependency validation, and byte-stability validation. It must not claim to replace checks still unique to `check-integrity.ps1`.

- [ ] **Step 4: Run CLI tests plus a real handbook `check`**

```bash
python -m unittest tests.engineering_context.test_cli -v
python -m automation.engineering_context check --root .
```

Expected: PASS / exit 0.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/cli.py automation/engineering_context/__main__.py tests/engineering_context/test_cli.py
git commit -m "feat: expose unified engineering context CLI"
```

---

### Task 10: Backfill Core Handbook Contracts and Compile Full Initial Context

**Files:**
- Modify: `policies/reuse-first.md`
- Modify: `policies/verification-definition-of-done.md`
- Modify: `standards/architecture-data-integrity-baseline.md`
- Modify: `standards/testing-release-quality-baseline.md`
- Modify: `standards/production-operability-baseline.md`
- Modify: `standards/dependency-supply-chain-baseline.md`
- Modify: `standards/ui-ux-quality-baseline.md`
- Modify: `standards/web-pwa-baseline.md`
- Modify: `patterns/authorization-privileged-boundaries.md`
- Modify: `patterns/token-secret-link-handling.md`
- Modify: `patterns/risk-based-verification-matrix.md`
- Modify: `patterns/release-provenance-environment-gates.md`
- Modify: `patterns/observability-signals.md`
- Modify: `patterns/api-contract-evolution.md`
- Modify: `patterns/performance-budgeting.md`
- Modify: `patterns/mobile-responsive-interaction.md`
- Modify: `patterns/visual-evidence-integrity.md`
- Regenerate: `machine-readable/compiled/*.json`
- Create: `tests/engineering_context/test_real_handbook_context.py`

**Interfaces:**
- No new Python API.
- Goal: enough explicit structured coverage for current router domains to make the compiled path useful immediately.

- [ ] **Step 1: Add failing real-handbook coverage expectations**

```python
# tests/engineering_context/test_real_handbook_context.py
import json
import unittest
from pathlib import Path


class RealHandbookContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.planning = json.loads(Path("machine-readable/compiled/planning.json").read_text())
        cls.routing = json.loads(Path("machine-readable/compiled/routing.json").read_text())

    def test_core_risks_have_planning_routes(self):
        for key in (
            "risk:authorization",
            "risk:credential",
            "risk:data-loss",
            "risk:availability",
            "risk:accessibility",
            "risk:performance",
        ):
            self.assertIn(key, self.routing)

    def test_core_operations_have_planning_routes(self):
        for key in ("operation:migration", "operation:deployment", "operation:integration"):
            self.assertIn(key, self.routing)
```

- [ ] **Step 2: Run and verify expected failures for missing coverage**

```bash
python -m unittest tests.engineering_context.test_real_handbook_context -v
```

Expected: FAIL for predicates not yet represented in explicit blocks.

- [ ] **Step 3: Add compact structured blocks to the listed authoritative pages**

Rules for every added unit:

1. one unit = one reusable semantic statement;
2. keep text compact; do not reproduce paragraphs;
3. `force` must match the source page exactly;
4. planning questions state what a plan must resolve, not the answer;
5. patterns are conditional guidance, not upgraded to normative force;
6. verification units describe evidence/failure classes, not tool fashion;
7. route hints point to canonical source IDs when deeper reading is justified;
8. avoid duplicate semantic units; when multiple pages support the same unit, one canonical unit carries multiple source IDs only if authority is equivalent and traceable.

- [ ] **Step 4: Regenerate and run all context tests**

```bash
python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled
python -m unittest discover -s tests/engineering_context -v
python -m automation.engineering_context check --root .
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add policies standards patterns machine-readable/compiled tests/engineering_context/test_real_handbook_context.py
git commit -m "docs: compile core handbook planning contracts"
```

---

### Task 11: Repo Routes, Change Archetypes, and Verification Routes

**Files:**
- Modify: `automation/engineering_context/repo_profile.py`
- Modify: `automation/engineering_context/task_descriptor.py`
- Modify: `automation/engineering_context/context_solver.py`
- Create: `tests/engineering_context/test_repo_routes.py`

**Interfaces:**
- Produces route projection in context output: `repo_route.inspect_first`, `repo_route.inspect_if`, `repo_route.avoid_by_default`, `repo_route.commands`, `repo_route.verification`.
- Archetypes supported initially: `add-crud-capability`, `modify-domain-state`, `authenticated-mutation`, `external-integration`, `schema-change`, `background-job`, `ui-flow-change`, `visual-regression-fix`, `pwa-capability-change`, `production-release`.

- [ ] **Step 1: Write failing route tests**

```python
# tests/engineering_context/test_repo_routes.py
import unittest
from pathlib import Path

from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import describe_task
from automation.engineering_context.context_solver import build_repo_route


class RepoRouteTests(unittest.TestCase):
    def test_authenticated_mutation_routes_to_server_authz_persistence_and_tests(self):
        root = Path(__file__).parent / "fixtures" / "repos" / "ts_web"
        profile = profile_repo(root)
        descriptor = describe_task("Add authenticated move update", profile)
        route = build_repo_route(profile, descriptor)
        labels = set(route["inspect_first"])
        self.assertIn("domain-mutation", labels)
        self.assertIn("authorization-boundary", labels)
        self.assertIn("persistence-owner", labels)
        self.assertIn("nearest-tests", labels)

    def test_backend_route_avoids_unrelated_pwa_by_default(self):
        root = Path(__file__).parent / "fixtures" / "repos" / "ts_web"
        profile = profile_repo(root)
        descriptor = describe_task("Change backend move state", profile)
        route = build_repo_route(profile, descriptor)
        self.assertIn("pwa", route["avoid_by_default"])
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_repo_routes -v
```

Expected: FAIL because route projection is incomplete/not implemented.

- [ ] **Step 3: Implement archetype-driven route projection**

Archetype routing tables must contain labels/landmark classes, not provider-specific hardcoded paths. Repo profile resolves labels to declared/detected paths where known. Unknown landmarks remain unresolved and are surfaced; they are not guessed.

Verification routing maps descriptor risks to the cheapest reliable evidence class already known from compiled verification units and repo command registry.

- [ ] **Step 4: Run route and CLI tests**

```bash
python -m unittest tests.engineering_context.test_repo_routes tests.engineering_context.test_cli -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/repo_profile.py automation/engineering_context/task_descriptor.py automation/engineering_context/context_solver.py tests/engineering_context/test_repo_routes.py
git commit -m "feat: precompute agent repository work routes"
```

---

### Task 12: Efficiency Metrics and Regression Scenarios

**Files:**
- Create: `tests/engineering_context/test_efficiency.py`
- Create fixture: `tests/engineering_context/fixtures/tasks/scenarios.json`
- Modify: `automation/engineering_context/cli.py`

**Interfaces:**
- `context --metrics` includes deterministic local metrics only; no telemetry is sent anywhere.
- Metrics: candidate unit count, selected unit count, estimated capsule tokens, full-source escalations, uncovered risks, repo-profile segment reuse, context ID/base delta stats.

- [ ] **Step 1: Write failing budget/regression tests**

Fixture scenarios must include at least:

```json
[
  {
    "name": "tenant-invitation",
    "task": "Add expiring tenant invitations",
    "expected_risks": ["authorization", "credential", "tenant-isolation"],
    "planning_soft_max": 900
  },
  {
    "name": "visual-only",
    "task": "Adjust spacing on the move detail card",
    "expected_surfaces": ["frontend"],
    "planning_soft_max": 900
  },
  {
    "name": "schema-change",
    "task": "Add archived_at to moves",
    "changed": ["supabase/migrations/002_moves_archived.sql"],
    "planning_soft_max": 900
  }
]
```

Test requirements:

```python
self.assertLessEqual(payload["metrics"]["estimated_tokens"], scenario["planning_soft_max"])
self.assertEqual(payload["metrics"]["full_source_reads"], 0)
self.assertEqual(payload["metrics"]["uncovered_required"], 0)
```

If a scenario legitimately needs escalation, change the scenario expectation explicitly rather than weakening the assertion globally.

- [ ] **Step 2: Run and verify failures where current routing is inefficient/incomplete**

```bash
python -m unittest tests.engineering_context.test_efficiency -v
```

Expected: one or more FAIL until metrics/scenario routing is complete.

- [ ] **Step 3: Add metrics output and tune metadata/routing, not prose summarization**

Do not solve an over-budget capsule by truncating mandatory constraints. First remove duplicates, tighten predicates, improve negative routing, or split overly broad semantic units.

- [ ] **Step 4: Run full test suite and record local benchmark output**

```bash
python -m unittest discover -s tests/engineering_context -v
python -m automation.engineering_context context --repo tests/engineering_context/fixtures/repos/ts_web --handbook machine-readable/compiled --mode plan --task "Add expiring tenant invitations" --metrics --pretty
```

Expected: tests PASS; output explicitly reports the selected units and estimated token budget.

- [ ] **Step 5: Commit**

```bash
git add automation/engineering_context/cli.py tests/engineering_context/test_efficiency.py tests/engineering_context/fixtures/tasks/scenarios.json
git commit -m "test: add context efficiency regression scenarios"
```

---

### Task 13: Codex/Agent Integration with Graceful Fallback

**Files:**
- Modify: `agent-config/codex/skills/engineering-handbook/SKILL.md`
- Modify: `agent-config/codex/AGENTS.global.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

**Interfaces:**
- Generic skill remains the only handbook skill.
- Preferred non-trivial flow: obtain compiled context first when the tooling/compiled state is available; otherwise use the existing manual progressive-disclosure routing.
- No Codex-specific semantic authority is introduced.

- [ ] **Step 1: Add documentation assertions to CLI/integration tests**

In `tests/engineering_context/test_cli.py`, add:

```python
from pathlib import Path


def test_codex_skill_points_to_compiled_context_without_removing_fallback(self):
    text = Path("agent-config/codex/skills/engineering-handbook/SKILL.md").read_text()
    self.assertIn("python -m automation.engineering_context", text)
    self.assertIn("fallback", text.lower())
    self.assertNotIn("bulk-read", text.lower())
```

Because the existing file currently says `Do not bulk-read`, change the assertion to verify the positive prohibition phrase exactly after editing, for example:

```python
self.assertIn("Do not bulk-read", text)
```

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests.engineering_context.test_cli -v
```

Expected: FAIL because current skill does not yet expose the new CLI flow.

- [ ] **Step 3: Update integration docs minimally**

`SKILL.md` sequence for non-trivial work:

```text
1. Read repo-local AGENTS/decisions.
2. If compiled context tooling is available, request the applicable plan/implement/verify capsule.
3. Follow supplied repo routes and escalation hints.
4. Do not bulk-read handbook references.
5. If compiled context is absent/stale/fails validation, fall back to the existing manual routing guide.
6. Canonical handbook source always wins over compiled output.
```

`AGENTS.global.md` gets only the minimum signal needed to invoke the generic router/context pipeline; do not embed taxonomy/budgets there.

README documents cold path vs hot path and authoritative/generated/runtime separation. CONTRIBUTING requires updating structured agent-context units when a normative change materially changes the compiled decision contract.

- [ ] **Step 4: Run integration tests and compile/check**

```bash
python -m unittest tests.engineering_context.test_cli -v
python -m automation.engineering_context check --root .
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add agent-config/codex/skills/engineering-handbook/SKILL.md agent-config/codex/AGENTS.global.md README.md CONTRIBUTING.md tests/engineering_context/test_cli.py
git commit -m "docs: route agents through compiled engineering context"
```

---

### Task 14: Catalog, CI Freshness Gate, and Final Verification

**Files:**
- Modify: `machine-readable/catalog.yaml`
- Create: `.github/workflows/handbook-context.yml`
- Modify if needed: `agent-config/codex/skills/engineering-handbook/bundle.json`
- Test/verify existing: `automation/handbook/check-integrity.ps1`

**Interfaces:**
- Catalog registers the context compiler executable asset and compiled manifest/registry artifacts using the existing multiline checker-compatible YAML style.
- GitHub Actions runs Python stdlib tests plus `engineering_context check` on PR/push.
- Existing PowerShell integrity checker remains a separate gate until its semantics are deliberately ported.

- [ ] **Step 1: Add failing catalog/compiled freshness checks to `check`**

Extend `check` so it verifies:

```text
compiled manifest exists
compiled source hashes match authoritative sources
recompile-to-temp produces byte-identical machine-readable/compiled files
all compiled source IDs are present in catalog when the catalog entry exists for that governed artifact
no compiled path escapes machine-readable/compiled
```

For catalog membership, implement a narrow line-oriented reader for the existing registry schema that recognizes only multiline entries beginning exactly with `  - id:` and their four-space-indented scalar fields. Document that this is a schema-specific registry reader, not a YAML parser. Do not accept flow-map YAML silently.

- [ ] **Step 2: Create CI workflow**

`.github/workflows/handbook-context.yml`:

```yaml
name: Handbook context

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<PINNED_FULL_SHA>
      - uses: actions/setup-python@<PINNED_FULL_SHA>
        with:
          python-version: "3.11"
      - run: python -m unittest discover -s tests/engineering_context -v
      - run: python -m automation.engineering_context check --root .
```

During implementation, resolve each official action tag to the current immutable full commit SHA using GitHub/official action metadata before committing. Do not leave a tag or the placeholder above in the final workflow.

- [ ] **Step 3: Update catalog and bundle only where required**

Add checker-compatible multiline entries for:

```text
exe-engineering-context
registry-compiled-handbook-context
```

If the installed generic skill bundle needs the generated compiled JSON available outside the handbook repo, update `bundle.json` to include the smallest required compiled files. Do not bundle repo-specific capsules or caches.

- [ ] **Step 4: Run every available local gate**

Run:

```bash
python -m unittest discover -s tests/engineering_context -v
python -m automation.engineering_context check --root .
python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled
git diff --exit-code -- machine-readable/compiled
```

If PowerShell exists:

```powershell
pwsh -File .\automation\handbook\check-integrity.ps1
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check
```

If `pwsh` is unavailable, explicitly record those three gates as **not run**; do not substitute manual inspection and call them passed.

- [ ] **Step 5: Perform deterministic smoke scenarios**

Run:

```bash
python -m automation.engineering_context context --repo tests/engineering_context/fixtures/repos/ts_web --handbook machine-readable/compiled --mode plan --task "Add expiring tenant invitations" --metrics --pretty
python -m automation.engineering_context context --repo tests/engineering_context/fixtures/repos/ts_web --handbook machine-readable/compiled --mode plan --task "Adjust spacing on the move detail card" --metrics --pretty
python -m automation.engineering_context context --repo tests/engineering_context/fixtures/repos/ts_web --handbook machine-readable/compiled --mode verify --task "Archive moves" --changed supabase/migrations/002_moves_archived.sql --metrics --pretty
```

Verify each output contains a stable context ID, bounded selected units, explicit unresolved fields if any, repo routes, and no full handbook-source contents.

- [ ] **Step 6: Commit**

```bash
git add machine-readable/catalog.yaml machine-readable/compiled .github/workflows/handbook-context.yml agent-config/codex/skills/engineering-handbook/bundle.json
git commit -m "ci: verify compiled engineering context freshness"
```

- [ ] **Step 7: Pre-PR scope and integrity review**

Run:

```bash
git status --short
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

Confirm the diff contains only the approved spec/plan, context pipeline, tests/fixtures, explicit handbook metadata, generated compiled artifacts, minimal agent integration, catalog, and CI. No unrelated cleanup.

---

## Final Acceptance Criteria

PR #11 is ready for review only when all of the following are demonstrated or explicitly reported as not run:

- [ ] A normal task can obtain context through one `python -m automation.engineering_context context ...` entry point.
- [ ] The compiler reads only explicit structured agent-context units and does not infer normative semantics from arbitrary Markdown prose.
- [ ] Identical semantic input produces byte-stable compiled JSON.
- [ ] Unchanged handbook sources are skipped/reused incrementally.
- [ ] Repo intelligence separates detected facts from declared decisions and preserves unknowns as unknown.
- [ ] Task descriptors are multidimensional and structural evidence cannot be suppressed by weaker natural-language signals.
- [ ] No secondary LLM/API call exists in tooling; ambiguity is returned as constrained unresolved fields.
- [ ] The context solver uses inverted routing plus deterministic minimum-cover selection, deduplication, negative routing, and budgets.
- [ ] Planning, implementation, and verification produce distinct views.
- [ ] Planning IR validation catches at least tenant/privilege authz gaps, credential lifecycle gaps, migration evidence gaps, integration failure-semantics gaps, and production release identity gaps.
- [ ] Context IDs allow delta delivery without resending unchanged units.
- [ ] Conformance distinguishes passed, failed, not-run, not-applicable, and declared exception.
- [ ] Core current handbook domains have initial structured coverage sufficient for the regression scenarios.
- [ ] Agent integration has a graceful fallback to current manual progressive disclosure when compiled context is missing/stale.
- [ ] Generated compiled handbook state is versioned and CI verifies source → compile → zero diff.
- [ ] Context/runtime caches and task capsules are not committed.
- [ ] The standard-library Python test suite passes.
- [ ] `python -m automation.engineering_context check --root .` passes.
- [ ] Existing PowerShell gates are run if available; otherwise their status is explicitly `not run`.
- [ ] No full handbook read is required in the normal regression scenarios.
- [ ] Planning regression scenarios stay at or under the 900-token soft maximum unless a scenario explicitly demonstrates a justified escalation.

## Deferred Until Evidence Justifies It

Do not add these during PR #11:

```text
vector/embedding search
graph database
remote context service
long-running daemon
LLM router service
framework-specific exhaustive AST indexes
universal source-code symbol database
auto-generated normative statements
full replacement of every legacy integrity check without equivalence tests
automatic Platform Core abstractions
```

The first production data from this pipeline should decide whether any of them are worth adding.
