# Human-Safe Errors and Repository Closure — Design

**Status:** APPROVED  
**Date:** 2026-09-08  
**Authority:** direct owner instruction, promoted from recurring MovOps/ChurchOS operational evidence

## Problem

Two cross-repository failure modes have repeated enough to require canonical governance rather than repo-local fixes:

1. operator-facing UIs can leak raw backend/transport/provider diagnostics into product copy, producing messages such as JSON bodies, snake_case error codes, internal identifiers or provider terminology;
2. completed initiatives can leave temporary branches, PRs, worktrees, scripts, tests, workflows or generated artifacts behind, making repository authority and release topology progressively harder to understand.

The existing Handbook already requires useful error states, truthful engineering, safe Git cleanup and current consumers for durable repository machinery. The missing piece is an explicit closure contract for these two failure modes.

## Decisions

### Human-safe error boundary

User-facing product surfaces MUST translate internal failures into stable, human-readable product messages with an actionable recovery path where one exists.

Raw transport bodies, provider exceptions, stack traces, database/RPC/table names, capabilities, UUIDs used only for internals, HTTP implementation terminology and machine-oriented error codes MUST NOT be rendered as ordinary product copy.

Internal diagnostic detail remains available to server logs/observability and engineering tools. A deliberately safe support/request reference MAY be shown when it helps recovery without exposing privileged internals.

Security/integrity failures still fail closed. Human-safe copy is presentation, not a fallback that converts failure into success.

### Repository closure hygiene

For actively managed Kappa-Bot product repositories, the default persistent remote branch allowlist is:

```text
main
qa   # only when the repository actually has a preproduction/integration branch
```

A different persistent branch set requires explicit current repo-local authority. Active task branches (`feature/*`, `feat/*`, `fix/*`, `docs/*`, `chore/*`, bot/dependency branches and equivalents) are temporary.

An initiative cannot be called closed while unexplained non-persistent branches, open task PRs, abandoned worktrees, unexplained stashes, or unique unintegrated commits created by that initiative remain.

Cleanup MUST be evidence-based. Unique work is integrated, transferred or deliberately retained before deletion. Force-moving refs or broad destructive deletion is not an acceptable way to fabricate a clean topology.

### Repository machinery lifecycle

The existing Handbook rule remains authoritative: tests, scripts, docs, workflows, fixtures and generated artifacts require current consumers. Initiative closure includes resolving temporary machinery created by the initiative and removing or consolidating obsolete machinery once its consumer is gone.

## Scope

This Handbook amendment changes only cross-repository governance and Codex global instructions. It does not directly mutate any consumer repository branches, runtime, CI or deployment configuration.

Consumer repositories will adopt/enforce these rules through their own bounded convergence work.

## Agent-context decision

This amendment does not change compiled `agent-context` projections. The two rules are added to the always-loaded Codex global instructions and canonical policy/standard prose. This keeps the compiled corpus byte-stable while making the new defaults immediately available to Codex.

A future compiler/context initiative may add narrow projections if evidence shows the global baseline is insufficient.

## Verification

The Handbook change is complete when:

- canonical UI/UX guidance explicitly forbids raw technical diagnostic leakage into ordinary user-facing copy;
- canonical Git hygiene defines the active Kappa-Bot persistent-branch default and closure gate without weakening preservation of unique work;
- the GitHub lifecycle playbook operationalizes a safe branch inventory/resolution loop;
- Codex global instructions include both rules;
- a mechanical contract test protects the promoted wording/semantics;
- existing engineering-context compiled artifacts remain fresh because no projection changed;
- Handbook integrity and engineering-context tests pass on the exact commit.
