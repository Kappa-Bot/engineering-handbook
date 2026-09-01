---
id: pat-durable-logical-agent-handoff
kind: pattern
status: active
owner: engineering
version: "1.0"
applies_to:
  - agentic-workflows
  - long-running-tasks
  - multi-agent-execution
sources:
  - src-openai-codex-agents
  - src-git-worktree
last_verified: 2026-09-02
review_due: 2026-12-02
---

# Durable Logical Agent Handoff

## Problem

A live agent thread can retain useful working context, but the thread is not durable project state. It may be stopped, compacted, closed, lost, moved between clients or interrupted by a machine restart. Assuming its hidden memory survives makes recovery unverifiable. Replacing agents casually is also expensive because each replacement rediscovers the repository, rereads authority and may reinterpret settled decisions.

## Pattern

Separate **logical role identity** from **runtime agent identity**.

```text
logical role
  stable role_id
  versioned charter
  durable run manifest
  exact authority/base/head references
  owned paths
  accepted evidence
  open findings
  next exact action

runtime generation
  current live handle
  actual model/reasoning
  started/ended timestamps
  context limitations
```

Reuse one live generation for its complete cohesive workstream while that context remains reliable. When the generation is lost, create a replacement generation for the same logical role from durable state.

## Required durable state

At minimum record:

```text
role_id
generation
status
mission
non_goals
actual_model
reasoning_effort
spawn_prefix
skills/resources actually used
base_sha
plan/spec paths and SHAs
owned_paths
read_only_paths
forbidden_paths
accepted_commits
verification_evidence
open_findings
blockers
next_action
live_handle when available
updated_at
```

The record may be Markdown, YAML or JSON according to repository conventions. It is not a transcript and must not copy hidden reasoning.

## Stable identity rules

- `role_id` stays stable across the initiative.
- `generation` increments whenever a new runtime agent replaces a stopped, closed, lost or post-restart generation.
- The actual model/reasoning configuration is recorded per generation.
- A respawned role verifies current repository state before editing.
- Accepted decisions remain authoritative by path/SHA, not by remembered conversation.
- Open findings and next action are explicit and bounded.

## Live-role reuse

Keep a live role active when:

- it still owns the same cohesive workstream;
- its authority and current-head references are current;
- its context remains reliable;
- retaining it saves more rediscovery than continued context size costs.

Do not keep a role alive merely to preserve identity. Park or close it after its workstream ends, after final handoff, or when stale assumptions make a clean replacement safer.

## Delta handoffs

After the kickoff packet, send only deltas:

```text
new head SHA
new/changed authority SHA
ownership transfer
new findings
new evidence
new milestone/task range
```

Do not paste the entire handbook, spec, plan or prior messages again when stable paths and hashes are sufficient.

## Ownership transfer

A path transfer is explicit:

1. outgoing role stops editing the path;
2. outgoing role records current head, uncommitted state and next action;
3. parent verifies the handoff;
4. incoming role records ownership before editing;
5. concurrent writes to that path remain prohibited.

## Recovery procedure

When a runtime generation disappears:

1. inspect the durable role record;
2. verify repository, branch/worktree and exact head;
3. preserve the stable `role_id` and increment `generation`;
4. select the actual replacement model/reasoning and record it;
5. provide the charter, authority references, owned paths, accepted commits, open findings and next action;
6. require a read-only reconciliation before changes;
7. update the manifest after reconciliation.

Never describe this as recovering the exact same agent or memory. It is a new process continuing the same logical role.

## Anti-patterns

- hidden conversation state as the only progress record;
- one fresh agent per microtask;
- respawning with no exact base/head/plan references;
- assigning the same file to two live writers;
- preserving enormous prompts instead of durable artifacts;
- claiming a requested model or skill was used without evidence;
- treating a role's completion message as final verification.

## Benefits

- restart-safe continuation;
- lower prompt duplication;
- fewer repository rediscovery cycles;
- stable responsibility and ownership;
- truthful model/process provenance;
- simpler review and cleanup.

## Related authority

- `std-owner-authorized-role-pods`
- `pb-owner-authorized-role-pod-execution`
- `ref-owner-authorized-role-manifest`
- `pol-verification-definition-of-done`
