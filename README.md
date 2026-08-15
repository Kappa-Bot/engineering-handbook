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

Foundation v0.1 contains only the categories that already have real content. Empty `standards/`, `patterns/`, `playbooks/`, `references/`, and `automation/` folders are intentionally absent.

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
5. Load specialized future patterns/playbooks/references only if the task requires them.
6. Verify according to the repository's real gates and `policies/verification-definition-of-done.md`.

### Adding knowledge

Do not add a page merely because something was learned. First determine whether it is generalizable. Use `governance/knowledge-promotion.md`.

### Adding an external source

Register material sources in `machine-readable/sources.yaml`, evaluate authority separately from applicability, and prefer synthesis + links over copying. Use `governance/source-authority.md`.

## Source vs distribution vs runtime

Three layers must remain distinct:

```text
AUTHORITATIVE SOURCE
engineering-handbook
        ↓
GENERATED / INSTALLED ARTIFACTS
~/.codex, consumer repos, CI configuration, etc.
        ↓
RUNTIME CONTEXT
only what the current tool/task actually loads
```

A copied global `AGENTS.md` or repo template is a distribution artifact, not a second source of truth. Copies should be traceable and regenerable from this repository.

## Foundation v0.1 scope

Foundation v0.1 establishes the mechanism for governing knowledge. It deliberately does **not** implement:

- Backstage or another engineering portal;
- vector search, embeddings, RAG, or a custom MCP knowledge server;
- repo-doctor or complex Codex hooks/rules;
- reusable GitHub CI;
- security, accessibility, PWA, performance, observability, or testing standards;
- Platform Core or MovOps migration;
- a generated documentation site;
- sophisticated repository-wide semantic versioning.

Those areas are introduced only when they have a real artifact, real adoption need, and evidence that the added mechanism pays for itself.

## Repository map

```text
engineering-handbook/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── governance/
├── policies/
├── agent-config/codex/
├── templates/
├── decisions/
└── machine-readable/
```

Start with `governance/handbook-governance.md`, then read the policy relevant to the work at hand.
