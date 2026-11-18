---
id: pb-handbook-discovery-and-update
kind: playbook
status: active
owner: engineering
version: "1.0"
applies_to: [engineering-handbook, codex, developer-workstations, all-repositories]
sources: [src-openai-codex-hooks, src-openai-codex-skills, src-openai-codex-agents]
last_verified: 2026-11-19
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

The installer writes one stable bootstrap/config and owned synchronous groups in `hooks.json`, preserving all unrelated groups. Open `/hooks` in local Codex (or its supported hook-review UI), review/trust the exact definitions and start a fresh session. **Do not bypass hook trust.** Source publication, installation, hook trust, client support and observed task-start execution are distinct gates. Cloud orchestration may not support local command hooks; use an explicit preflight in the supported execution environment rather than claiming universal automatic behavior.

For a direct check, run the installed script, using the actual resolved path:

```sh
python "<codex-home>/handbook-bootstrap/handbook_update.py" doctor
python "<codex-home>/handbook-bootstrap/handbook_update.py" preflight
```

`doctor` verifies local state and reports the baseline file, the two exact hook definitions, and any global override separately. `READY_FOR_CLIENT_VERIFICATION` means only that the local files are present; hook execution, trust and client support remain `NOT_OBSERVED`. It does not contact the network. `preflight` checks remote freshness before each new prompt, plus startup/resume/clear. It deliberately avoids compact/fork/subagent events and in-turn tool hooks. Each delegate receives the parent's pinned snapshot and does not independently refresh it. A non-empty global override added after installation also blocks preflight until explicitly reconciled.

## Update contract

| State | Meaning | Required handling |
| --- | --- | --- |
| `CURRENT` | Canonical remote checked; installed revision matches | Pin the returned immutable snapshot |
| `UPDATED` | Verified fast-forward candidate staged and activated | Use the new snapshot for this task, not earlier active tasks |
| `STALE_OFFLINE` | Recognized transport unavailability; previous installation and snapshot verified | Continue only on that last-known-good copy and disclose unverified remote freshness; TLS, object-integrity, authentication, unknown fetch errors and whole-process deadlines block instead |
| `BLOCKED` | Drift, malformed manifest, divergence, invalid paths/config, lock or unsupported contract | Do not start substantive work until reconciled |
| `VERIFIED_LOCAL` | Doctor checked local hashes only | Not evidence of current remote state or active hooks |
| `SHADOWED` | Non-empty global override detected | Preserve it and resolve the intended instruction source explicitly |

The stable bootstrap fetches only `https://github.com/Kappa-Bot/engineering-handbook.git`, with isolated Git config, no credential helpers, prompts, hooks, submodules, checkout filters or user-checkout updates. It validates the exact Git object snapshot, minimum runtime/entrypoint, complete registry inventory, catalog/source/index hashes, JSON object/collection contracts, included paths, case collisions, regular-file modes, size bounds and artifact inventory. All model selectors, including preferred, backstop and fallback values, are checked against the Luna prohibition. Candidate Python is not executed to validate itself. Runtime code is used only after the owner-trusted bundle is activated.

A single lock serializes writers; a journal enables rollback if activation is interrupted. Immutable snapshots are constructed and verified under unique staging names before an atomic rename publishes their final name; a partial pre-journal write therefore does not poison retries of that revision. Installed files are compared to the **previous** manifest anchored in separate state, never merely compared with the new remote content. Unexpected edits/files or modified manifests block instead of being reclassified as an ordinary old version. Python bytecode caches are excluded; symlinks/reparse points are not accepted.

Every task is pointed to an immutable snapshot under `handbook-bootstrap/snapshots/`. Prior copies stay available while other sessions update the discoverable skill. Do not garbage-collect snapshots while a session may still reference them. The bootstrap and skill target must share a filesystem for recoverable directory renames. Update network/processing deadlines are bounded; failed hooks/client timeouts are not a universal enforcement boundary—confirm the preflight result before work.

No prompt text or transcript is read, logged or transmitted by the bootstrap. HTTPS and fast-forward integrity are **not** signatures or protection against a compromised canonical maintainer or same-user attacker. The bootstrap never silently self-updates: a changed bootstrap contract requires an explicit reviewed reinstall.

## Recovery and manual alternative

- On local drift, preserve and diff the edited files; promote intentional changes to canonical source or move personal rules to their real owner. Do not force automatic replacement.
- On divergence/rewind, inspect canonical history. Do not reset trusted state simply to make the check pass.
- On an interrupted update, retain `activation.json`, the named backup/stage, `state.json` and immutable snapshots. Once no updater process is running, move a stale `update.lock` aside, then run preflight; it validates and recovers the journal before fetching. An orphan `.handbook-snapshot-stage-*` is unpublished and does not prevent a retry; do not rename it manually into a trusted snapshot. Never remove a live lock or blindly restore an unverified backup.
- To roll back deliberately, stop affected sessions and disable only the two owned hooks through the supported UI. Preserve the current copy and state, inspect the retained prior snapshot/backup, and explicitly install the desired reviewed version. Automatic preflight will otherwise follow canonical `main` again; disabling enrollment is part of deliberate rollback. Do not delete unrelated hooks or overrides.
- Manual distribution remains available through `sync-handbook-skill.ps1` and the portable `handbook_update.py bundle --source <checkout> --skills-home <skills-home>` (`--check`, `--backup-existing`). Manual bundles are not enrolled and must not be reported as automatic. Do not use the manual installer on an enrolled target; reconcile enrollment first.

## Maintaining and verifying the source

Edit `rules.v1.json` for generic activation, `routes.v1.json` for inspection order, `landmarks.v1.json` for real-path discovery, and `taxonomy.v1.json` for topic aliases/typed document links. Visual-language recognizers are named and tested in the descriptor module. Add bilingual positive, negative and mixed-domain regressions before changing behavior. Register new canonical artifacts once; do not rebuild a duplicate router in the skill text.

```sh
python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled
python -m automation.engineering_context check --root .
python -m automation.engineering_context doctor --root .
python -m unittest discover -s tests/engineering_context -p 'test_*.py'
```

Local tests include real Git ancestry/object materialization and portable installed-runtime execution. Windows quoting is structurally tested; native Windows PowerShell and an actual Codex task-start hook are separate adoption evidence, never inferred from Linux tests. Publication requires no GitHub Actions run or paid service.
