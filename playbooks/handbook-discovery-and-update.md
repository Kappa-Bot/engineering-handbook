---
id: pb-handbook-discovery-and-update
kind: playbook
status: active
owner: engineering
version: "1.6"
applies_to: [engineering-handbook, codex, developer-workstations, all-repositories]
sources: [src-openai-codex-hooks, src-openai-codex-skills, src-openai-codex-agents]
last_verified: 2026-11-21
review_due: 2027-02-19
---

# Discover guidance and update the Handbook manually across coding agents

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

In `context --metrics`, `full_source_reads` counts full documents included in the capsule and reports its scope as `capsule`. `freshness_verification` reports the local recompilation that checks the compiled corpus. Filesystem activity and end-to-end latency require separate benchmark measurements.

With `--base-context`, `added_units` carries new or revised records to insert or replace by ID. Supply a previous CLI result, its bare capsule, or a compact receipt with a context ID and a `unit_ids` array. Full capsules verify unchanged units by comparing their records. A compact receipt verifies reuse when its context ID matches. Across different context IDs, the delta resends units whose prior records were unavailable. If a full capsule includes a nonempty `unit_ids` list, the inventories must agree.

`covered` refers only to detected risks. `needs-discovery`, `needs-resolution`, uncovered requirements and unresolved paths are not PASS states. Classification of a migration diff does not authorize running it; production observation does not authorize deploying.

## Runtime isolation for all coding-agent clients

The manual-only rule applies to **any** code-agent harness that consumes this Handbook: Codex, Claude Code, Cursor, Gemini CLI, VS Code/Copilot, Windsurf, Cline, OpenCode and future clients. The Handbook MUST NOT register a lifecycle hook, prompt check, tool gate, stop/retry hook, model hook, plugin callback, MCP interceptor, watcher or startup job that automatically fetches, verifies, upgrades, repairs or blocks the Handbook. A single client can merge user, project, agent-scoped, plugin, remote and managed hooks; a local clean \`hooks.json\` is insufficient proof that no other source runs.

This availability rule **does not** remove authorization, sandbox, enterprise policy, secret protection, legal/financial controls or explicitly authorized test/release checks. A failed Handbook lookup must not block an unrelated permitted task, but an unrun integrity check is not a PASS or permission to deploy.

Consult [the code-agent interoperability reference](../references/code-agent-hook-isolation.md) for current provider-specific paths and lifecycle differences. The portable audit command uses only Python's standard library and no network:

\`\`\`sh
python -I automation/agents/handbook_hook_audit.py --json
python -I automation/agents/handbook_hook_audit.py --project "/path/to/repo" --json
\`\`\`

The default is **read-only**. To remove an exact owned legacy user hook, first close affected code agents, inspect the findings, then explicitly opt in:

\`\`\`sh
python -I automation/agents/handbook_hook_audit.py --apply --clients-stopped --json
\`\`\`

Only a recognized command calling the **exact** installed \`handbook-bootstrap/handbook_update.py preflight --hook\` may be removed; unknown scripts, managed hooks, project hooks and all unrelated security hooks are **never automatically modified**. Source file backups are written before changes. If a host uses executable script hooks/plugins or proprietary settings, do a provider-specific manual review instead of treating it like Codex JSON. Neither this audit nor a Handbook commit proves client runtime recovery.

## Manual-only local Handbook installation

Requirements: Python 3.10+ and Git for **explicit** installation and updates. Codex does not require command hooks, network access, or a startup preflight. The installed client/account remains the authority for model/effort availability. Review the trusted bootstrap before running it.

From an up-to-date trusted canonical checkout:

```sh
python automation/codex/handbook_update.py install
```

If replacing a previous unmanaged skill installation, retain it explicitly:

```sh
python automation/codex/handbook_update.py install --backup-existing
```

To adopt a verified publication, pass its full `main` commit SHA from the matching trusted checkout:

```sh
python automation/codex/handbook_update.py install --expected-revision <published-main-sha>
```

The pinned installation checks the revision actually fetched from canonical `main` and matches the executing bootstrap to that commit. A different revision or pending activation recovery stops the installation before changing the active bundle. Use the installed offline `doctor` for the post-install receipt; manual `preflight` can advance the active revision.

`--codex-home` and `--skills-home` support explicit isolated locations. Defaults are `CODEX_HOME` or the user's `.codex`, and the user's `.agents/skills`. The installer reads the bundle from canonical `main`. It preserves `config.toml`, model defaults, user `AGENTS.md`, approvals, sandbox settings and credential configuration. A non-empty `AGENTS.override.md` blocks that **manual installation** pending explicit reconciliation. Review any custom global instructions for conflicts with the fresh baseline and verify loading in a fresh session.

The installer writes the stable local bootstrap/config **without registering any Handbook hook**. It removes only legacy Handbook-owned `SessionStart`/`UserPromptSubmit` groups from `hooks.json`, preserving unrelated user/project hooks and installed snapshots. Existing Codex sessions and custom global instructions are not rewritten. An explicit manual update is the only operation that fetches the canonical remote; a commit to `main` never forces a workstation refresh. Open `/hooks` in Codex to inspect all effective hook sources if an unexplained stop persists: user-level `doctor` cannot prove there are no project, system or plugin hooks.

For a direct check, run the installed script, using the actual resolved path:

```sh
python "<codex-home>/handbook-bootstrap/handbook_update.py" doctor
python "<codex-home>/handbook-bootstrap/handbook_update.py" preflight
```

`doctor` verifies local hashes, the global baseline, the owned hook definitions in the user-level `hooks.json` and any global override. It returns nonzero if it finds an owned legacy handler or a handler that pairs a historical invocation with a custom platform command. The execution status is then `NOT_VERIFIED`. `READY_FOR_MANUAL_USE` means that the local knowledge and owned hook configuration checks passed. Runtime activation and other hook sources require their own evidence. `doctor` is offline. `preflight` checks remote freshness **only when explicitly invoked** from the root/manual command. No startup/resume/clear, message, continuation, tool or subagent event triggers an update. Delegates use their parent's selected knowledge revision. Legacy `--hook` invocations are deliberately inert (`continue:true`) to protect older installations pending offline rescue.

## Update contract

| State | Meaning | Required handling |
| --- | --- | --- |
| `CURRENT` | Canonical remote checked; installed revision matches | Pin the returned immutable snapshot |
| `UPDATED` | Verified fast-forward candidate staged and activated | Use the new snapshot for this task, not earlier active tasks |
| `STALE_OFFLINE` | Recognized transport unavailability; previous installation and snapshot verified | Pin the verified last-known-good copy; remote freshness unverified. No new release claim based on it. |
| `STALE_REJECTED` | A fetched revision failed ancestry, data/hash, source/index or other update validation; previous snapshot **reverified** | Never activate candidate. Pin only the reverified prior immutable snapshot, disclose the precise rejected reason, do not treat current remote as trusted or release-ready. |
| `BLOCKED` | Explicit manual operation or local validation failed and returned nonzero | Do not apply the invalid update or claim checks passed. Codex messages and unrelated work are not blocked. |
| `VERIFIED_LOCAL` | Doctor checked local hashes only | Not evidence of current remote state or active hooks |
| `SHADOWED` | Non-empty global override detected | Preserve it and resolve the intended instruction source explicitly |

The Handbook is **not part of Codex's runtime gate**. No automatic Handbook hook is installed, so GitHub outages, stale locks, candidate integrity errors or broken local state cannot trigger an automatic Handbook stop. Explicit `install` and `preflight` still validate sources and may return nonzero; a rejected candidate is never installed and local drift is never reclassified as trusted stale. An unverified knowledge snapshot must not be reported as current or as proof that quality/release gates have passed. Product-specific authorization and security restrictions continue to apply.

The stable bootstrap fetches only `https://github.com/Kappa-Bot/engineering-handbook.git`, with isolated Git config, no credential helpers, prompts, hooks, submodules, checkout filters or user-checkout updates. It validates the exact Git object snapshot, minimum runtime/entrypoint, complete registry inventory, catalog/source/index hashes, JSON object/collection contracts, included paths, case collisions, regular-file modes, size bounds and artifact inventory. All model selectors, including preferred, backstop and fallback values, are checked against the Luna prohibition. Candidate Python is not executed to validate itself. Runtime code is used only after the owner-trusted bundle is activated.

A persistent OS-owned file lock serializes writers and releases automatically if a process exits abnormally; the lock file remains on disk to avoid inode-replacement races. A journal enables rollback if activation is interrupted. Immutable snapshots are constructed and verified under unique staging names before an atomic rename publishes their final name; a partial pre-journal write therefore does not poison retries of that revision. Installed files are compared to the **previous** manifest anchored in separate state, never merely compared with the new remote content. Unexpected edits/files or modified manifests block instead of being reclassified as an ordinary old version. Python bytecode caches are excluded; symlinks/reparse points are not accepted.

Explicit installation/update preserves immutable snapshots under `handbook-bootstrap/snapshots/`. A task may use the last selected snapshot without auto-refresh. Prior copies stay available for concurrent sessions; never garbage-collect a referenced snapshot. The bootstrap and skill target must share a filesystem for recoverable directory renames. Update time budgets and validation failures apply only to deliberate manual update commands, not to message delivery.

No prompt text or transcript is read, logged or transmitted by the bootstrap. HTTPS and fast-forward integrity are **not** signatures or protection against a compromised canonical maintainer or same-user attacker. The bootstrap never silently self-updates: a changed bootstrap contract requires an explicit reviewed reinstall.

## Recovery and manual alternative

### Offline emergency recovery of Codex messages

When the installed bootstrap is outdated, a create-exclusive `update.lock` persists, or canonical `main` temporarily fails validation, **do not repeatedly retry `install` or delete anything in `.codex`**. From a reviewed copy of this repository (not the possibly broken installed bootstrap), with Codex fully closed and no updater process running:

```sh
python -I automation/codex/handbook_update.py rescue-hooks --codex-home "<codex-home>" --check
python -I automation/codex/handbook_update.py rescue-hooks --codex-home "<codex-home>"
```

This command is entirely offline. It checks the existing `hooks.json`, backs up the original bytes under `handbook-bootstrap/backups` before writing and removes only exact Handbook-owned `SessionStart` and retired `UserPromptSubmit` handlers. A mixed group keeps its matcher and other handlers. Rescue and installation preserve a handler with a custom platform command and report the pending review. `--check` reports the result without modifying the file. Malformed hooks require manual review. After rescue, use `doctor` to verify that both owned definitions are removed and send a harmless prompt in Codex to test message delivery. Use the current manual-only installer for future explicit installs. An installed bootstrap changes only on explicit installation from a verified source.


- On local drift, preserve and diff the edited files; promote intentional changes to canonical source or move personal rules to their real owner. Do not force automatic replacement.
- On divergence/rewind, inspect canonical history. Do not reset trusted state simply to make the check pass.
- On an interrupted update, retain `activation.json`, the named backup/stage, `state.json` and immutable snapshots. The current OS-held `update.lock` is persistent by design: **never delete or rename it as ordinary cleanup**. During a one-time migration from the old create-exclusive lock, first verify that no updater process is active, archive the legacy lock (do not delete it), explicitly reinstall the reviewed manual-only bootstrap, then run an explicit preflight to recover the journal. An orphan `.handbook-snapshot-stage-*` is unpublished and does not prevent a retry; do not rename it manually into a trusted snapshot. Never remove a live lock or blindly restore an unverified backup.
- To recover from old automatic enrollment, stop affected sessions and run the scoped offline `rescue-hooks` command. Preserve existing state, snapshots, backups and unrelated hooks; no automatic enrollment is restored by a current manual-only install. For a deliberate knowledge rollback, inspect the retained prior snapshot and explicitly install the chosen reviewed version.
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

Source tests cover Git ancestry, object materialization, manual install/refresh and preservation of unrelated hooks. Native Windows acceptance is independent of Linux/unit coverage. **No Handbook task-start hook is expected or required.** Publication requires no GitHub Actions run or paid service.
