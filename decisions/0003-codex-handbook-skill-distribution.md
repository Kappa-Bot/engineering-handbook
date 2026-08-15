---
status: accepted
date: 2026-08-15
decision-makers:
  - engineering
consulted: []
informed: []
---

# Distribute handbook knowledge through one user-level Codex router skill

## Context and problem statement

The handbook now contains cross-repository governance, policies, playbooks, templates, and source metadata. Loading all of this into `AGENTS.global.md` would increase permanent context and duplicate canonical documents. Copying the same documents into every consumer repository would create drift and second sources of truth.

Codex skills provide task-specific progressive disclosure and a user-level discovery scope that applies across repositories. The handbook needs a local distribution model that preserves canonical source ownership while allowing Codex to load specialized guidance only when needed.

## Decision drivers

- keep global prompt context small;
- make specialized guidance discoverable across all repositories used by one developer;
- avoid one skill per handbook artifact and the resulting initial skill-list pressure;
- preserve handbook documents as canonical sources;
- make installed references generated, traceable, replaceable, and verifiable;
- avoid symlink/path coupling to one local checkout;
- avoid plugin/platform infrastructure until broader distribution actually exists;
- support the primary Windows/PowerShell workflow.

## Considered options

### Put more handbook content in global AGENTS.md

Simple distribution, but permanently loads specialized material into every task and duplicates canonical content.

### Copy handbook docs into every repository

Makes files locally visible but causes multi-repository drift and bloats repo-local context/maintenance.

### One Codex skill per policy or playbook

Provides fine-grained invocation but increases the number of initially advertised skills and makes routing/maintenance noisier than the current scale requires.

### Symlink a user skill to a handbook checkout

Keeps references physically connected but couples runtime behavior to a local checkout path/branch and adds avoidable filesystem friction.

### One user-level router skill with generated references

Provides a single discovery surface, lets the selected skill route to only necessary references, and keeps installed reference files generated from canonical handbook sources.

### Package a plugin immediately

Appropriate for reusable distribution to other people or bundled connectors, but unnecessary infrastructure for the current single-developer rollout.

## Decision outcome

Chosen option: **one user-level `engineering-handbook` Codex router skill with generated references**.

Canonical authoring lives under:

`agent-config/codex/skills/engineering-handbook/`

The user installation target is:

`$HOME/.agents/skills/engineering-handbook`

`SKILL.md` is maintained canonically in this repository. `bundle.json` defines which canonical handbook areas become generated installed references. `automation/codex/sync-handbook-skill.ps1` builds/verifies the installed copy.

The generated `references/` tree MUST NOT become independently maintained. Any durable change belongs in the canonical handbook file and is propagated by synchronization.

The router MUST instruct Codex to load only relevant references; activation of the skill is not permission to read the entire bundle.

The global `AGENTS.global.md` may contain only a compact hint to use the skill when cross-repository specialized guidance is needed.

## Distribution boundary

This decision intentionally uses local USER-scope Skills for one developer's environment. If distribution expands to other people, centrally managed environments, or connector bundles, evaluate a plugin rather than extending the sync script into an ad-hoc package manager.

## Consequences

### Positive

- low permanent token cost;
- one discoverable cross-repository skill instead of many;
- canonical handbook ownership remains clear;
- references are available offline after installation;
- hash-based drift detection is possible;
- no per-repository copies, symlinks, portal, MCP, or plugin required.

### Tradeoffs

- installed references duplicate files on disk, although not as independent sources;
- synchronization is explicit and can drift until checked;
- the first installer is PowerShell-specific;
- one broad router skill depends on a well-scoped description and routing instructions to avoid over-activation.

## Re-evaluation triggers

Revisit this decision when:

- more users need the handbook skill;
- multiple handbook skills become clearly more precise than one router;
- the skill needs connector dependencies or managed distribution;
- the bundle becomes large enough that local generated mirroring is operationally awkward;
- observed implicit activation is too broad or too narrow despite description tuning.

## Sources

- `src-openai-codex-skills`
