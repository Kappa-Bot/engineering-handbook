---
status: accepted
date: 2026-08-15
decision-makers:
  - engineering
consulted: []
informed: []
---

# Distribute global Codex instructions by explicit synchronization

## Context and problem statement

The Engineering Handbook already contains the canonical global Codex working agreements at `agent-config/codex/AGENTS.global.md`, but a source artifact has no operational value until a developer workstation can install and verify it safely.

Codex supports global guidance from its home directory and then layers project/directory instructions according to its own discovery rules. The handbook therefore needs a distribution mechanism without turning the installed file into a second source of truth.

## Decision drivers

- preserve the handbook as the canonical source;
- make adoption observable and reversible;
- never overwrite an existing developer instruction file silently;
- work well on the primary Windows/PowerShell workflow;
- avoid background services and speculative platform infrastructure;
- allow deterministic verification by file hash;
- keep runtime precedence owned by Codex rather than reimplemented internally.

## Considered options

### Manual copy only

Lowest implementation cost, but easy to forget, difficult to verify consistently, and prone to silent drift.

### Symlink from Codex home to the handbook checkout

Keeps the file physically connected to the source but couples runtime behavior to a particular checkout path and introduces avoidable Windows/filesystem friction. It also makes local branch changes immediately affect runtime instructions.

### Explicit synchronization script

Copies the canonical artifact on demand, compares SHA-256 hashes, supports a dry-run, refuses destructive replacement by default, and can preserve the previous target before installation.

## Decision outcome

Chosen option: **explicit synchronization script**.

`automation/codex/sync-global-agents.ps1` is the first executable handbook distribution asset. It supports two semantic operations:

- `Check`: compare the canonical source and installed target without modifying either;
- `Install`: copy the source into the resolved Codex home, with `-WhatIf` support and explicit backup requirement when a differing target already exists.

The installation target follows Codex's documented global location: `$CODEX_HOME/AGENTS.md`, or `~/.codex/AGENTS.md` when `CODEX_HOME` is unset.

The installed file is a **distributed artifact**, not an authoritative source. Changes intended for all repositories MUST be made in `agent-config/codex/AGENTS.global.md` and synchronized outward.

The script does not automatically pull Git, update itself, schedule background synchronization, or modify consumer repositories.

## Consequences

### Positive

- safe first real handbook-to-runtime adoption path;
- deterministic drift detection;
- reversible replacement of pre-existing workstation instructions;
- no daemon, package manager, symlink requirement, portal, or managed-device dependency;
- easy future integration into richer tooling without changing the canonical-source model.

### Tradeoffs

- synchronization remains an explicit developer action;
- a workstation can drift until `Check` is run again;
- PowerShell is the first supported executable path; other shells can be added only when actual adoption requires them.

## Verification

File synchronization is verified by SHA-256 equality. Runtime adoption requires a new Codex session and an observed instruction-summary probe because Codex discovers its instruction chain at session/run start.

## Sources

- `src-openai-codex-agents`
