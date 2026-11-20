---
id: pb-handbook-discovery-and-update
kind: playbook
status: active
owner: engineering
version: "1.4"
applies_to: [engineering-handbook, codex, developer-workstations, all-repositories]
sources: [src-openai-codex-hooks, src-openai-codex-skills, src-openai-codex-agents]
last_verified: 2026-11-20
review_due: 2027-02-19
---

# Discover guidance and refresh the Handbook before tasks

Operational owner for [ADR 0012](../decisions/0012-handbook-discovery-and-safe-preflight-update.md). Model/effort decisions remain in [the runtime Standard](../standards/agent-runtime-routing.md); this page does not duplicate that matrix.

## Three views, one set of identities

| Need | Entry point | What it proves |
| --- | --- | --- |
| Find a rule, procedure or reference | `search`, knowledge `tree` | Ranked lexical matches across the complete catalog, with stable IDs and active/historical states |
| Understand an activation | `explain`, execution `tree` | Matched/negated evidence, predicates, selected units, prerequisite graph and exclusions |
| Find the actual owner/files in a repository | repository `tree`, `profile-repo` | Existing discovered/declared paths, stable inspection order, unresolved/unsafe declared paths |
| Check generated configuration | `doctor`, `check` | Local index/graph/freshness/configuration checks; not runtime adoption or model entitlement |

From the canonical root, or the selected installed snapshot's `references/` directory:

```sh
python -m automation.engineering_context search --root . --query "invocación subagentes" --pretty
python -m automation.engineering_context tree --root . --kind knowledge --pretty
python -m automation.engineering_context tree --root . --kind execution --pretty
python -m automation.engineering_context tree --root . --kind repository --repo "<absolute-repo>" --task "Review authorization" --pretty
python -m automation.engineering_context explain --root . --repo "<absolute-repo>" --task "No migres datos; corrige permisos" --pretty
python -m automation.engineering_context doctor --root . --repo "<absolute-repo>" --pretty
```

Use `context --repo ... --handbook machine-readable/compiled --mode plan|implement|verify --task ...` for the compact working capsule. `--changed` is repeatable. `--historical` on search/knowledge tree makes archived/superseded/proposed records explicit. Lexical search does not claim semantic understanding; alias coverage is curated and testable. No-match means further discovery, not clearance.

`requires` edges impose a prerequisite; `related` only helps navigation; `supersedes` records replacement; `amends` records a partial change; `conflicts` must not contradict a required dependency. Unit prerequisites and document references are validated separately from user authorization. Cycles, unknown IDs, stale generated output and invalid rule operators fail checks.

Repository discovery reads paths and configuration, not commercial brief contents. Declared landmarks override detection only as explicit ownership data and must exist inside the repository without symlink traversal. Missing declarations are surfaced, not silently treated as inspected. Mixed UI/data/PWA tasks retain all relevant boundaries; UI exclusions cannot hide an explicitly required database.

## Context and effort budgets

The runtime prefers minimum direct coverage plus every applicable mandatory requirement. Advisory target/soft/hard/reserve token estimates are 900/1500/2500/350 for unclassified small tasks, 1500/2500/4000/500 for classified risk, and 3000/4500/6500/750 for multiple critical risks, broad risk or unresolved uncertainty. These are estimates, not provider token measurements. The reserve describes headroom for source escalation; it is not an enforced harness quota. Mandatory units can exceed hard budget with an explicit escalation rather than being dropped. Small known cases can still stay below 600 tokens.

`covered` refers only to detected risks. `needs-discovery`, `needs-resolution`, uncovered requirements and unresolved paths are not PASS states. Classification of a migration diff does not authorize running it; production observation does not authorize deploying.

## One-time local Codex enrollment

Requirements: Python 3.10+, Git, and a local Codex client that supports and trusts command hooks. The installed client/account remains the authority for model/effort availability. The source of the stable bootstrap should be reviewed before running it.

From an up-to-date trusted canonical checkout:

```sh
python automation/codex/handbook_update.py install
```

If replacing a previous unmanaged skill installation, retain it explicitly:

```sh
python automation/codex/handbook_update.py install --backup-existing
```

`--codex-home` and `--skills-home` support explicit isolated locations. Defaults are `CODEX_HOME` or the user's `.codex`, and the user's `.agents/skills`. The installer fetches canonical `main`, not uncommitted checkout content. It does not change `config.toml`, model defaults, user `AGENTS.md`, approvals, sandbox settings or credential configuration. A non-empty `AGENTS.override.md` blocks enrollment for deliberate reconciliation. Existing custom global instructions must be inspected for conflicts with the fresh baseline; no file rewrite is assumed to reload the session.

The installer writes one stable bootstrap/config and only one owned synchronous `SessionStart` group in `hooks.json`, removing the legacy owned `UserPromptSubmit` group while preserving all unrelated groups. Open `/hooks` in local Codex (or its supported hook-review UI), review/trust the root-only definition and start a fresh session. A canonical code update alone cannot change the existing local bootstrap; complete the explicit reviewed reinstall, with Codex sessions stopped and any legacy lock safely archived. **Do not bypass hook trust.** Source publication, installation, hook trust, client support and observed task-start execution are distinct gates. Cloud orchestration may not support local command hooks; use an explicit preflight in the supported execution environment rather than claiming universal automatic behavior.

For a direct check, run the installed script, using the actual resolved path:

```sh
python "<codex-home>/handbook-bootstrap/handbook_update.py" doctor
python "<codex-home>/handbook-bootstrap/handbook_update.py" preflight
```

`doctor` verifies local state and reports the baseline file, the single root `SessionStart` hook, absence of the legacy per-prompt hook, and any global override separately. `READY_FOR_CLIENT_VERIFICATION` means only that the local files are present; hook execution, trust and client support remain `NOT_OBSERVED`. It does not contact the network. `preflight` checks remote freshness **once at each root/master-parent macro-execution boundary** (`SessionStart`: startup/resume/clear). The automatic hook has an 18-second preflight time budget and must never stop message delivery if the deadline, lock, local verification, Git transport or candidate integrity fails. It does not run for each new user prompt or continuation. An additional check is explicit and is initiated by the root parent only. It deliberately avoids compact/fork/subagent events and in-turn tool hooks. Each delegate receives the parent's pinned snapshot and does not independently refresh it. A non-empty global override added after installation also blocks preflight until explicitly reconciled.

## Update contract

| State | Meaning | Required handling |
| --- | --- | --- |
| `CURRENT` | Canonical remote checked; installed revision matches | Pin the returned immutable snapshot |
| `UPDATED` | Verified fast-forward candidate staged and activated | Use the new snapshot for this task, not earlier active tasks |
| `STALE_OFFLINE` | Recognized transport unavailability; previous installation and snapshot verified | Pin the verified last-known-good copy; remote freshness unverified. No new release claim based on it. |
| `STALE_REJECTED` | A fetched revision failed ancestry, data/hash, source/index or other update validation; previous snapshot **reverified** | Never activate candidate. Pin only the reverified prior immutable snapshot, disclose the precise rejected reason, do not treat current remote as trusted or release-ready. |
| `BLOCKED` | Manual operation or local validation failed and returned nonzero | Stop this update and all unverified/high-risk changes, **not the user's ability to send messages**. The automatic hook emits an advisory `continue:true` warning and no verified snapshot if the local copy cannot be checked. |
| `VERIFIED_LOCAL` | Doctor checked local hashes only | Not evidence of current remote state or active hooks |
| `SHADOWED` | Non-empty global override detected | Preserve it and resolve the intended instruction source explicitly |

An auto hook is an **advisory availability boundary**, not a source-authority bypass. A failing root hook returns `continue:true`, no `decision:block` or `stopReason`, and clear warning/context when no valid snapshot could be pinned. Explicit manual `preflight` still returns nonzero on failure. A rejected candidate is never installed, and a local snapshot with drift/corruption is never reclassified as trusted stale. This distinction protects user messaging while retaining strict safety and release checks. An agent without a verified Handbook snapshot may continue discussion, but must not claim compliance or carry out high-risk changes/publications based on it.

The stable bootstrap fetches only `https://github.com/Kappa-Bot/engineering-handbook.git`, with isolated Git config, no credential helpers, prompts, hooks, submodules, checkout filters or user-checkout updates. It validates the exact Git object snapshot, minimum runtime/entrypoint, complete registry inventory, catalog/source/index hashes, JSON object/collection contracts, included paths, case collisions, regular-file modes, size bounds and artifact inventory. All model selectors, including preferred, backstop and fallback values, are checked against the Luna prohibition. Candidate Python is not executed to validate itself. Runtime code is used only after the owner-trusted bundle is activated.

A persistent OS-owned file lock serializes writers and releases automatically if a process exits abnormally; the lock file remains on disk to avoid inode-replacement races. A journal enables rollback if activation is interrupted. Immutable snapshots are constructed and verified under unique staging names before an atomic rename publishes their final name; a partial pre-journal write therefore does not poison retries of that revision. Installed files are compared to the **previous** manifest anchored in separate state, never merely compared with the new remote content. Unexpected edits/files or modified manifests block instead of being reclassified as an ordinary old version. Python bytecode caches are excluded; symlinks/reparse points are not accepted.

Every task is pointed to an immutable snapshot under `handbook-bootstrap/snapshots/`. Prior copies stay available while other sessions update the discoverable skill. Do not garbage-collect snapshots while a session may still reference them. The bootstrap and skill target must share a filesystem for recoverable directory renames. Update network/processing deadlines are bounded; failed hooks/client timeouts are not a universal enforcement boundary—confirm the preflight result before work.

No prompt text or transcript is read, logged or transmitted by the bootstrap. HTTPS and fast-forward integrity are **not** signatures or protection against a compromised canonical maintainer or same-user attacker. The bootstrap never silently self-updates: a changed bootstrap contract requires an explicit reviewed reinstall.

## Recovery and manual alternative

### Offline emergency recovery of Codex messages

When the installed bootstrap is outdated, a create-exclusive `update.lock` persists, or canonical `main` temporarily fails validation, **do not repeatedly retry `install` or delete anything in `.codex`**. From a reviewed copy of this repository (not the possibly broken installed bootstrap), with Codex fully closed and no updater process running:

```sh
python -I automation/codex/handbook_update.py rescue-hooks --codex-home "<codex-home>" --check
python -I automation/codex/handbook_update.py rescue-hooks --codex-home "<codex-home>"
```

This command is entirely offline. It checks the existing `hooks.json`, backs up its original bytes under `handbook-bootstrap/backups` and removes only the exact Handbook-owned `SessionStart` and retired `UserPromptSubmit` command groups. Other hooks, credentials, projects, `state.json`, journals and snapshots remain untouched. `--check` is non-mutating. On malformed hooks it reports failure without overwriting. After rescue, test sending a harmless prompt in Codex; **this does not prove the entire client is repaired**. Once canonical source + compiled outputs verify as a coherent tree, explicitly reinstall the reviewed bootstrap and check `doctor` returns `SessionStart=PRESENT`, `UserPromptSubmit=REMOVED`. Never use an unverified source, disable unrelated hooks, or assume an ordinary GitHub commit upgrades the installed bootstrap.


- On local drift, preserve and diff the edited files; promote intentional changes to canonical source or move personal rules to their real owner. Do not force automatic replacement.
- On divergence/rewind, inspect canonical history. Do not reset trusted state simply to make the check pass.
- On an interrupted update, retain `activation.json`, the named backup/stage, `state.json` and immutable snapshots. The current OS-held `update.lock` is persistent by design: **never delete or rename it as ordinary cleanup**. During a one-time migration from the old create-exclusive lock, first verify that no updater process is active, archive the legacy lock (do not delete it), explicitly reinstall the reviewed bootstrap/hooks, then run preflight to recover the journal. An orphan `.handbook-snapshot-stage-*` is unpublished and does not prevent a retry; do not rename it manually into a trusted snapshot. Never remove a live lock or blindly restore an unverified backup.
- To roll back deliberately, stop affected sessions and disable only the single owned `SessionStart` hook through the supported UI. Preserve the current copy and state, inspect the retained prior snapshot/backup, and explicitly install the desired reviewed version. Automatic preflight will otherwise follow canonical `main` again; disabling enrollment is part of deliberate rollback. Do not delete unrelated hooks or overrides.
- Manual distribution remains available through `sync-handbook-skill.ps1` and the portable `handbook_update.py bundle --source <checkout> --skills-home <skills-home>` (`--check`, `--backup-existing`). Manual bundles are not enrolled and must not be reported as automatic. Do not use the manual installer on an enrolled target; reconcile enrollment first.

## Maintaining and verifying the source

### Publish a complete tree, never a temporary source/index mismatch

Source, catalog, registries and the generated `machine-readable/compiled` inventory must be committed together. Regenerate locally, run `check`, `doctor` and focused tests, inspect the diff, then merge/push one coherent commit with expected-head protection. If any gate is unrun or fails, leave the candidate in a separate branch/PR: **do not apply source changes to `main` as individual GitHub Contents writes followed later by an index fix**. This was the cause of the observed `candidate canonical source/index drift` during client repair. A versioned preflight consumes the exact committed source and never runs downloaded candidate Python. No additional services or paid CI are required.


Edit `rules.v1.json` for generic activation, `routes.v1.json` for inspection order, `landmarks.v1.json` for real-path discovery, and `taxonomy.v1.json` for topic aliases/typed document links. Visual-language recognizers are named and tested in the descriptor module. Add bilingual positive, negative and mixed-domain regressions before changing behavior. Register new canonical artifacts once; do not rebuild a duplicate router in the skill text.

Registry rules normally evaluate the whole positive task. For rules that combine **an action, its object and exclusions**, use `"scope":"clause"` so all predicates belong to one affirmative instruction; otherwise a README-only operation can mask or contaminate a separate code change. Focused UX/UI, accessibility, performance, security, privacy and reliability rules use `"scope":"quality-clause"`: the shared lexical layer identifies ES/EN audit/review and remediation heads, filters explicitly excluded disciplines and distinguishes a reviewed document from a product review using that document as reference. The declarative registry remains the sole domain-to-owner mapper; no second quality router is introduced. Both clause scopes prohibit path predicates. This is bounded lexical parsing, not an authorization engine: preserve question/negation scope and escalate ambiguous intent. A public website privacy-policy document has its own legal/trust route and does not imply an application security audit. `landmarks.v1.json` must exclude vendor/generated/example decoys consistently across alternatives and recognize genuine nested owners.

```sh
python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled
python -m automation.engineering_context check --root .
python -m automation.engineering_context doctor --root .
python -m unittest discover -s tests/engineering_context -p 'test_*.py'
```

Local tests include real Git ancestry/object materialization and portable installed-runtime execution. Windows quoting is structurally tested; native Windows PowerShell and an actual Codex task-start hook are separate adoption evidence, never inferred from Linux tests. Publication requires no GitHub Actions run or paid service.
