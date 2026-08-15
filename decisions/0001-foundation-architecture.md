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

Kappa-Bot needs a reusable engineering source of truth above individual products so engineering knowledge is not repeatedly rediscovered, copied, or embedded as oversized permanent agent context. The first version must establish governance without prematurely building a documentation platform.

## Decision drivers

- single authoritative source across products;
- low operational complexity;
- human-readable and agent-readable artifacts;
- progressive disclosure for agent context;
- traceable external sources;
- explicit knowledge promotion and lifecycle;
- ability to add enforcement later without requiring it now;
- avoidance of speculative platform work.

## Considered options

- Markdown + YAML + Git as the initial governed knowledge system.
- Introduce a documentation portal or Backstage immediately.
- Keep engineering knowledge distributed only across product repositories and prompts.

## Decision outcome

Chosen option: **Markdown + YAML + Git as Foundation v0.1**.

The Engineering Handbook is an independent repository. Governance, Policies, Standards, Patterns, Playbooks, References, templates, and executable assets are distinct artifact classes, but taxonomy folders are created only when real content exists.

There is one active canonical normative document per topic. Meaningful history is preserved through decision records and superseded artifacts rather than duplicated active pages.

`machine-readable/catalog.yaml` indexes internal handbook artifacts. `machine-readable/sources.yaml` independently registers external sources. Internal documents reference source IDs instead of duplicating source metadata.

The handbook is authoritative. Installed Codex instructions and copies in consumer repositories are generated or distributed artifacts that must remain traceable and regenerable rather than becoming second sources of truth.

Repo-local knowledge remains local unless deliberately promoted through the handbook's promotion process.

Automation is introduced only after a rule is stable and technical enforcement has demonstrated value.

## Consequences

### Positive

- very low infrastructure and maintenance cost;
- clear governance before scale;
- easy review through Git;
- compatible with future portals, catalogs, automation, or search without requiring them today;
- reduced permanent agent context and duplicated policy text.

### Negative / tradeoffs

- discovery is initially file- and catalog-based rather than portal-based;
- enforcement remains mostly procedural until later phases introduce stable automation;
- metadata discipline must be maintained manually in Foundation v0.1.

## Explicitly deferred

Foundation v0.1 does not add Backstage, a web portal, vector databases, embeddings, RAG, custom MCP, a custom search engine, repo-doctor, complex Codex hooks/rules, reusable GitHub CI, security/accessibility/PWA/performance baselines, Platform Core or MovOps migration, a documentation site generator, or sophisticated repository-wide semantic versioning.

## Source note

The decision-record structure is a lightweight internal adaptation informed by `src-madr` rather than a verbatim copy of the full MADR template.
