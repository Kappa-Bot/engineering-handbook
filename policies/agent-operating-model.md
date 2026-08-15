---
id: pol-agent-operating-model
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
last_verified: 2026-08-15
review_due: 2026-11-15
---

# Agent Operating Model

## Objective

Use coding agents as disciplined engineering workers without turning every task into a giant prompt, multi-agent ceremony, or permanent context dump.

## Context model

Permanent context MUST stay small.

Preferred layering:

```text
small global instructions
        +
small repo-local AGENTS.md
        +
current task
        ↓
load specialized skills / playbooks / references only when relevant
```

Universal rules belong in the handbook/global distribution artifact. Repo-specific commands, architecture, boundaries, and local decisions belong in the repo. Specialized procedures belong in focused artifacts rather than a giant `AGENTS.md`.

## Session and repository scope

- Default to one active engineering session per repository/task context.
- Keep one repository as the primary unit of work for a session.
- Do not mix unrelated repository changes into one task merely because the agent can access them.
- Cross-repository work SHOULD explicitly identify which repository owns each change and which handbook rule is being propagated.

## Subagents

- Use **zero subagents by default**.
- Subagents MAY be used when explicitly requested or when genuinely independent parallel work creates clear value.
- Do not create subagents simply because a methodology recommends them.
- Do not split work into multiple agents when coordination/context cost exceeds the work saved.

## Planning

Planning effort MUST be proportional to task complexity.

- Mechanical, obvious, low-risk work may proceed with a short internal plan.
- Multi-step, architectural, security-sensitive, migration-heavy, or ambiguous work SHOULD produce an explicit spec/plan before implementation.
- A plan MUST NOT become an excuse to postpone straightforward implementation after the design is already approved.

Keep task states distinct when relevant:

```text
research → decision → spec → plan → implementation → verification → adoption
```

Do not silently jump from exploration/research into implementation.

## Scope control

Agents MUST:

- keep the requested outcome primary;
- avoid unrelated refactors;
- avoid speculative abstractions;
- avoid cleanup outside the necessary change;
- make assumptions explicit when they materially affect the solution;
- prefer small, reviewable changes.

## Methodology

Use specialized engineering methods when they fit the work, including:

- brainstorming for unresolved creative/architecture decisions;
- implementation planning for non-trivial multi-step work;
- TDD where behavior can be expressed meaningfully as tests;
- systematic debugging before speculative fixes;
- verification-before-completion;
- code review appropriate to the risk.

Methodology defaults MUST NOT override explicit handbook policies such as the no-worktree default or zero-subagent default.

## Token/context efficiency

- Do not paste entire handbooks/research reports into task prompts when a stable ID/path suffices.
- Load the smallest relevant artifact set.
- Prefer links/IDs and focused summaries to duplicated policy prose.
- Keep generated progress reports concise unless detailed evidence is needed for a durable artifact.

## Handoff

At handoff, the agent SHOULD report:

- outcome delivered;
- files/areas changed;
- verification actually run;
- checks not run and why;
- remaining risks or dependencies;
- Git/workspace state when relevant.

The handoff MUST NOT imply success for unexecuted gates.
