# Engineering Handbook

The Engineering Handbook is the engineering source of truth for Kappa-Bot products and repositories.

Its purpose is to turn engineering knowledge into a governed system: discover, evaluate, decide, document, distribute, verify, version, and retire practices without repeatedly reinventing them.

## What this repository is

- A versioned source of engineering governance, policies, standards, patterns, playbooks, references, templates, and enforceable assets.
- The canonical source for reusable engineering rules that apply across repositories.
- A registry of evaluated external sources and internally promoted knowledge.

## What this repository is not

- A general-purpose wiki or note dump.
- A copy of external handbooks or vendor documentation.
- A place for repo-specific decisions that are not generalizable.
- A software portal, search platform, RAG system, or Backstage installation in Foundation v0.1.

## Core principle

**Reuse first. Search before build.** Prefer an existing internal or mature external solution when it fits the problem better than inventing a new one.

## Taxonomy

- **Governance** defines authority, precedence, lifecycle, and promotion rules.
- **Policies** define mandatory cross-repository behavior.
- **Standards** define technical baselines when they are introduced.
- **Patterns** capture reusable solutions.
- **Playbooks** capture repeatable procedures.
- **References** preserve supporting research and evaluated sources.
- **Templates and executable assets** turn stable knowledge into repeatable practice.
- **Repo-local decisions** remain in consumer repositories unless deliberately promoted.

Folders for Standards, Patterns, Playbooks, References, and Automation are created only when the first real artifact exists.

## Start here

1. Read `governance/handbook-governance.md` for authority and precedence.
2. Read `governance/source-authority.md` before promoting external guidance.
3. Read `governance/knowledge-promotion.md` before turning project learning into handbook content.
4. Read the applicable active policies under `policies/`.
5. Use `machine-readable/catalog.yaml` to discover internal artifacts and `machine-readable/sources.yaml` to resolve external source metadata.

## Consumption model

The handbook is the authoritative source. Installed Codex instructions or copies placed in consumer repositories are distributed artifacts and must remain traceable to this repository rather than becoming independent sources of truth.
