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
  - src-openai-codex-rules
  - src-openai-codex-hooks
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Agent Operating Model

## Objective

Agents should receive the smallest durable context that reliably preserves engineering discipline, then load specialized knowledge only when the task requires it.

## Permanent context

- Global agent instructions MUST remain small and operational.
- Repo-local `AGENTS.md` files SHOULD contain repository-specific purpose, commands, constraints, and Definition of Done rather than duplicate universal handbook policy.
- Specialized workflows SHOULD live in focused skills, playbooks, references, or executable assets when those artifacts actually exist.
- The handbook is the authoritative source; installed or copied agent configuration is a distributed artifact, not a second source of truth.

## Default execution model

- Use **zero subagents by default**.
- Use a subagent only when explicitly requested or when genuinely independent parallel work provides clear value and does not compromise context, cost, or control.
- Keep one active working session scoped to one repository whenever practical.
- Keep one repository per working folder/session unless a task intrinsically requires coordinated cross-repository work.
- Plan in proportion to complexity. Do not create heavyweight plans for trivial changes, and do not begin complex implementation without first resolving material design decisions.

## Scope control

Agents MUST:

- avoid silent scope expansion;
- avoid unrelated refactors and cleanup;
- preserve user work;
- distinguish research, decision, specification, implementation, verification, and adoption states;
- prefer small reviewable changes;
- expose uncertainty instead of inventing completion evidence.

## Progressive disclosure

Do not preload large handbooks, research corpora, or specialized instructions into every task. Load only the canonical artifacts relevant to the current work.

## Enforcement

When a stable policy can be enforced reliably and the enforcement cost is justified, prefer technical enforcement over repeated prose reminders. Enforcement mechanisms are introduced separately and do not belong in Foundation v0.1 merely because they are possible.
