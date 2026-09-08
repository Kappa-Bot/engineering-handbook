# Human-Safe Errors and Repository Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote human-safe frontend error handling and evidence-based repository closure into canonical Kappa-Bot engineering governance.

**Architecture:** Strengthen existing canonical artifacts rather than creating duplicate policies. Put human-safe error presentation in the UI/UX Standard, branch/closure semantics in Workspace/Git Hygiene, operational branch cleanup in the GitHub lifecycle playbook, and immediate always-loaded defaults in Codex global instructions. Add a small contract test; do not change compiled agent-context projections.

**Tech Stack:** Markdown governance, Codex global instructions, Python unittest.

**Spec:** `docs/superpowers/specs/2026-09-08-human-safe-errors-repository-closure-design.md`

## Global Constraints

- Do not create a new normative topic when an existing canonical artifact owns it.
- Preserve unique/unmerged work; cleanup must be evidence-based and non-destructive.
- Active Kappa-Bot product repositories default to persistent `main` plus optional `qa`; exceptions require explicit current repo-local authority.
- Ordinary user-facing product copy must never expose raw internal diagnostics.
- Keep compiled agent-context projections unchanged in this amendment.

---

### Task 1: Promote human-safe error presentation

**Files:**
- Modify: `standards/ui-ux-quality-baseline.md`
- Test: `tests/engineering_context/test_promoted_policy_contracts.py`

**Interfaces:**
- Consumes: existing UI/UX interaction-state and Definition-of-Done rules.
- Produces: canonical `Human-safe error presentation` contract.

- [ ] **Step 1: Add a contract test**

Assert that `standards/ui-ux-quality-baseline.md` contains the human-safe error heading and forbids raw transport/provider/internal diagnostics as ordinary product copy.

- [ ] **Step 2: Confirm the new assertion fails against the previous baseline**

Run:

```text
python -m unittest tests.engineering_context.test_promoted_policy_contracts -v
```

Expected before implementation: FAIL because the promoted contract is absent.

- [ ] **Step 3: Strengthen the UI/UX Standard**

Add a normative subsection under interaction states that requires product-safe messages, recovery guidance, internal-only diagnostics and fail-closed behavior. Add the corresponding Definition-of-Done bullet. Do not alter the `json agent-context` block.

- [ ] **Step 4: Run the focused contract test**

Expected: PASS.

### Task 2: Promote branch allowlist and closure hygiene

**Files:**
- Modify: `policies/workspace-git-hygiene.md`
- Modify: `playbooks/github-repository-lifecycle.md`
- Test: `tests/engineering_context/test_promoted_policy_contracts.py`

**Interfaces:**
- Consumes: existing safe-cleanup and short-lived-branch rules.
- Produces: explicit Kappa-Bot persistent-branch default plus initiative closure gate.

- [ ] **Step 1: Extend the contract test**

Require the Workspace/Git policy to state `main` plus optional `qa` as the active Kappa-Bot project default and require unexplained non-persistent branches/unique work to be resolved before closure.

Require the GitHub lifecycle playbook to include a persistent-branch inventory/resolution procedure.

- [ ] **Step 2: Strengthen Workspace/Git Hygiene**

Add a `Persistent branch allowlist and initiative closure` section. Preserve the prohibition on deleting uncertain/unique work and force-moving refs.

- [ ] **Step 3: Operationalize the rule in the GitHub lifecycle playbook**

Add a safe inventory loop: classify persistent branches, open PRs, unique commits and merged/superseded branches; integrate/transfer unique work first; delete only proven-safe task refs; block initiative closure on unexplained residue.

- [ ] **Step 4: Run the focused contract test**

Expected: PASS.

### Task 3: Make both defaults immediate for Codex

**Files:**
- Modify: `agent-config/codex/AGENTS.global.md`
- Test: `tests/engineering_context/test_promoted_policy_contracts.py`

**Interfaces:**
- Consumes: canonical rules from Tasks 1–2.
- Produces: always-loaded concise agent defaults without copying implementation detail.

- [ ] **Step 1: Extend the contract test**

Assert the global instructions contain one concise human-safe-error bullet and one concise persistent-branch/closure bullet.

- [ ] **Step 2: Update global instructions**

Add only compact summary bullets; canonical detail remains in the Standard/Policy/Playbook.

- [ ] **Step 3: Run the focused contract test**

Expected: PASS.

### Task 4: Exact-head verification and commit

**Files:**
- Create: `docs/superpowers/specs/2026-09-08-human-safe-errors-repository-closure-design.md`
- Create: `docs/superpowers/plans/2026-09-08-human-safe-errors-repository-closure.md`
- Modify: files from Tasks 1–3.

**Interfaces:**
- Produces: one coherent Handbook authority commit.

- [ ] **Step 1: Run engineering-context tests**

```text
python -m unittest discover -s tests/engineering_context -p 'test_*.py' -v
```

Expected: PASS.

- [ ] **Step 2: Verify compiled corpus freshness**

```text
python -m automation.engineering_context check --root . --pretty
```

Expected: PASS with no stale compiled files.

- [ ] **Step 3: Run Handbook integrity**

```text
pwsh -File ./automation/handbook/check-integrity.ps1
```

Expected: PASS.

- [ ] **Step 4: Commit directly to `main` without creating a temporary branch**

Commit message:

```text
docs: govern human-safe errors and repository closure
```

- [ ] **Step 5: Observe the exact-main GitHub Actions verification**

The `engineering-context` workflow must complete successfully for the new SHA before reporting the Handbook change as fully verified.
