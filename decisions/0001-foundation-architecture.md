---
status: accepted
date: 2026-08-15
decision-makers:
  - engineering
consulted: []
informed: []
---

# Establish the Engineering Handbook Foundation architecture

## Context and problem statement

Kappa-Bot needs a reusable engineering source of truth above individual products. Engineering practices, agent instructions, source evaluations, and reusable decisions are otherwise repeatedly rediscovered, duplicated across prompts/repos, or loaded as oversized permanent context.

The first version must establish governance and a promotion/distribution mechanism without prematurely building a documentation platform.

## Decision drivers

- one authoritative cross-repository source;
- low operational complexity and near-zero infrastructure cost;
- human-readable and agent-readable knowledge;
- progressive disclosure and token/context efficiency;
- explicit separation of external evidence from internal decisions;
- traceable external sources;
- one current canonical normative topic without losing meaningful history;
- explicit lifecycle and promotion;
- future ability to enforce stable rules technically;
- no speculative platform work before real adoption data exists.

## Considered options

1. **Markdown + YAML + Git** as a minimal governed knowledge system.
2. **Backstage / engineering portal immediately**, providing catalog, templates, docs tooling, and a richer developer portal from day one.
3. **Distributed knowledge only**, leaving practices in product repositories, prompts, and personal notes.

## Decision outcome

Chosen option: **Markdown + YAML + Git for Foundation v0.1**.

The Engineering Handbook is an independent repository above individual products.

The conceptual taxonomy distinguishes Governance, Policies, Standards, Patterns, Playbooks, References, Templates, executable automation, and repo-local decisions. Folders are created only when the first real artifact exists; the conceptual taxonomy does not require empty directories.

There is at most one active canonical normative document per topic. Historical decisions and superseded artifacts may remain immutable when they explain the current state.

`machine-readable/catalog.yaml` indexes internal artifacts. `machine-readable/sources.yaml` separately registers external sources. Governed documents refer to stable source IDs rather than duplicating URL/tier/license/freshness metadata.

The handbook is the **authoritative source**. Copies installed into Codex configuration or consumer repositories are **generated/distributed artifacts**, not independent sources of truth. Runtime context should load only the smallest material required for the current task.

Repo-local knowledge remains local unless deliberately promoted through the knowledge-promotion process.

Automation follows stable policy. A rule may later become a Codex rule/hook, script, repo-doctor check, linter, test, CI gate, GitHub ruleset, or deployment gate when enforcement materially reduces drift/errors/repeated work.

## Why not a portal now

Backstage and similar engineering platforms provide valuable concepts: software catalog metadata, ownership, templates/golden paths, and docs-as-code. Those concepts inform the long-term direction, but deploying a portal before enough knowledge/assets exist would add infrastructure and maintenance before it solves a demonstrated discovery problem.

Foundation therefore copies the **concepts**, not the platform.

## Documentation model

The normative taxonomy describes **what authority an artifact has**. A later documentation-experience model such as Diátaxis may describe **how a reader consumes it** (tutorial, how-to, explanation, reference). These dimensions should not be conflated.

Decision records use a lightweight MADR-inspired structure rather than an invented bespoke ADR format.

## Consequences

### Positive

- minimal infrastructure and operating cost;
- clear governance before scale;
- Git-native review/history;
- low permanent agent context;
- source traceability without URL duplication;
- compatible with future portal/search/automation without depending on them now;
- repo-specific decisions remain close to their code.

### Negative / tradeoffs

- discovery is initially file/catalog based;
- metadata and lifecycle consistency are manual in v0.1;
- most policy enforcement is procedural until later automation is justified;
- consumers must deliberately distribute/install canonical agent artifacts.

## Explicitly deferred

Foundation v0.1 does not add:

- Backstage or another web portal;
- vector databases, embeddings, RAG, or a custom MCP knowledge server;
- a custom search engine;
- repo-doctor;
- complex Codex rules/hooks;
- reusable GitHub CI;
- security/accessibility/PWA/performance/observability/testing baselines;
- Platform Core or MovOps migration;
- a documentation site generator;
- sophisticated repository-wide semantic versioning.

## Sources / evidence

- `src-openai-codex-agents`
- `src-openai-codex-skills`
- `src-openai-codex-rules`
- `src-openai-codex-hooks`
- `src-backstage`
- `src-diataxis`
- `src-madr`
