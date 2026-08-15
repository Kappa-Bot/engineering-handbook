# Engineering Handbook

The Engineering Handbook is the canonical engineering knowledge and operating-system repository for Kappa-Bot products.

Its job is not to collect notes. Its job is to turn engineering knowledge into a governed system that can be discovered, evaluated, promoted, distributed, applied, verified, versioned, and retired without repeatedly reinventing the same decisions.

## Mission

The handbook exists to make good engineering the default across repositories while keeping permanent agent context small.

The intended flow is:

```text
Engineering Handbook
        ↓
small global agent instructions
        +
small repo-local instructions
        ↓
current task
        ↓
load only the specialized policy / pattern / playbook / reference needed
```

This is progressive disclosure: broad rules stay small and stable; specialized knowledge is loaded only when it becomes relevant.

## Core principles

- **Reuse first. Search before build.**
- **Single source of truth.** One active canonical normative document per topic.
- **Human-readable + agent-readable.** Markdown for people and agents; YAML indexes for discovery.
- **Evidence before claims.** Verification status must reflect checks actually executed.
- **Production-minded, not speculative.** Prefer boring, proven mechanisms until scale or evidence justifies more complexity.
- **No silent scope creep.** Keep changes narrow and reviewable.
- **No documentation cemetery.** Create taxonomy folders only when a real artifact exists.
- **Prefer enforceable rules over repeated reminders** once the rule is stable and enforcement has clear value.
- **Repo-specific knowledge stays repo-specific** unless deliberately promoted.

## Taxonomy

The conceptual taxonomy is larger than the current folder tree.

| Kind | Purpose | Normative? |
|---|---|---|
| Governance | Authority, precedence, lifecycle, promotion | Yes |
| Policy | Mandatory cross-repository behavior | Yes |
| Standard | Technical baseline for a defined scope | Yes |
| Pattern | Reusable technical/UX/architecture solution | No, unless referenced by a normative artifact |
| Playbook | Repeatable operating procedure | No, unless referenced by a normative artifact |
| Reference | Research and supporting evidence | No |
| Template | Reusable starting artifact | Only where explicitly required |
| Executable asset | Script, rule, hook, CI, ruleset, gate, skill | Enforces or assists a stable rule |
| Decision | Historical record of a durable choice | Records authority; does not replace current policy |

Folders are created only when the first real artifact exists. `playbooks/` and `automation/` now exist because real adoption workflows require them.

## Authority model

When applicable guidance conflicts, use this order:

```text
External non-negotiable obligations
        ↓
Handbook Governance
        ↓
Applicable active Policy
        ↓
Applicable active Standard
        ↓
Approved repo-local decision / permitted exception
        ↓
Pattern
        ↓
Playbook
        ↓
Reference / research
```

See `governance/handbook-governance.md` for the full exception and canonicality model.

## How to use the handbook

### Starting a task

1. Read the consumer repository's `AGENTS.md` and local decisions.
2. Search the current repository for an existing solution.
3. Use `machine-readable/catalog.yaml` to discover applicable handbook artifacts.
4. Follow the applicable active policies.
5. Load specialized patterns/playbooks/references only if the task requires them.
6. Verify according to the repository's real gates and `policies/verification-definition-of-done.md`.

### Adopting a repository

Use `playbooks/repository-adoption.md`. A repository-level `AGENTS.md` should contain verified **local** commands, architecture boundaries, decisions, and local gates—not a copy of universal handbook policy.

Start from `templates/AGENTS.repo.md`, remove every section that does not add durable local value, and verify the resulting instruction chain in a fresh Codex run.

### Adding knowledge

Do not add a page merely because something was learned. First determine whether it is generalizable. Use `governance/knowledge-promotion.md`.

### Adding an external source

Register material sources in `machine-readable/sources.yaml`, evaluate authority separately from applicability, and prefer synthesis + links over copying. Use `governance/source-authority.md`.

## Source vs distribution vs runtime

Three layers must remain distinct:

```text
AUTHORITATIVE SOURCE
engineering-handbook and repo-local canonical docs
        ↓
GENERATED / INSTALLED ARTIFACTS
global config copies and other deliberately generated outputs
        ↓
RUNTIME CONTEXT
only what the current tool/task actually loads
```

The global `AGENTS.md` installed into Codex home is a distribution artifact, not a second source of truth. A consumer repository's own maintained `AGENTS.md`, however, is the canonical source for that repository's local agent instructions; it should reference rather than duplicate universal handbook guidance.

## Current Codex adoption

The canonical global Codex instructions live at `agent-config/codex/AGENTS.global.md`.

Codex reads global instructions from `$CODEX_HOME/AGENTS.md`; when `CODEX_HOME` is unset the default home is `~/.codex`. Repo and directory-level `AGENTS.md` files are then layered on top according to Codex's own discovery rules.

Use the global adoption playbook:

```powershell
# Check whether the installed global instructions match the handbook.
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check

# Preview a safe installation. Existing differing instructions are never overwritten silently.
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -BackupExisting -WhatIf

# Install, backing up an existing differing AGENTS.md first.
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -BackupExisting
```

After installation, start a **new Codex session** before validating behavior because Codex discovers the instruction chain once per run/session.

See `playbooks/codex-global-adoption.md` and `decisions/0002-codex-global-distribution.md`.

## Foundation v0.1 scope

Foundation v0.1 established the mechanism for governing knowledge. It deliberately did **not** implement Backstage, vector search/RAG, custom MCP knowledge infrastructure, repo-doctor, complex Codex hooks/rules, reusable GitHub CI, cross-cutting product standards, product migrations, or a generated documentation site.

Post-Foundation adoption remains intentionally incremental: first distribute the global instructions, then establish a minimal repository-local contract, and only then use pilot repositories to decide what further automation or standards earn their complexity.

## Repository map

```text
engineering-handbook/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── governance/
├── policies/
├── agent-config/codex/
├── playbooks/
├── automation/codex/
├── templates/
├── decisions/
└── machine-readable/
```

Start with `governance/handbook-governance.md`, then read the policy or playbook relevant to the work at hand.
