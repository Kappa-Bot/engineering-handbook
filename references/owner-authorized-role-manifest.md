---
id: ref-owner-authorized-role-manifest
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to:
  - agentic-workflows
  - multi-agent-execution
  - codex
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
last_verified: 2026-09-02
review_due: 2026-12-02
---

# Owner-Authorized Role Manifest

Use this reference only after `OWNER_AUTHORIZED_ROLE_PODS` has been explicitly activated. Copy the compact fields needed by the consumer repository; do not turn the template into a parallel project-management system.

## Run manifest

```yaml
schema: owner-authorized-role-pod-run/v1
run_id: <stable initiative id>
status: PLANNING | ACTIVE | BLOCKED | VERIFYING | CLOSED
repository: <owner/repo>
owner_authorization: <exact durable reference>
authorization_recorded_at: <ISO-8601>
base_sha: <40-char SHA>
target_branch: <branch>
approved_spec:
  path: <repo path>
  sha256: <content hash or exact commit SHA>
approved_plan:
  path: <repo path>
  sha256: <content hash or exact commit SHA>
profile: OWNER_AUTHORIZED_ROLE_PODS
spawn_prefix: /caveman Ultra
nested_subagents: false
planned_subagent_count: <1 or 2>
active_role_ids:
  - <design-quality and/or delivery>
maximum_concurrent_subagents: 2
exceptional_third_role:
  enabled: false
  reason: null
scope:
  included: []
  excluded: []
authority:
  paid_actions: false
  provider_resource_creation: false
  destructive_external_actions: false
orchestrator:
  actual_model: <record actual alias/model>
  reasoning_effort: <record actual level>
roles:
  - role_id: <active role id>
    generation: 1
    manifest: roles/<active role id>.md
created_at: <ISO-8601>
updated_at: <ISO-8601>
```

For the normal two-pod topology, `active_role_ids` contains `design-quality` and `delivery`, and `roles` contains one entry for each. A one-pod run records only the selected cohesive role. A third role is never implied by this template and requires the documented exception.

## Role manifest

```yaml
schema: owner-authorized-logical-role/v1
run_id: <same run id>
role_id: design-quality | delivery | <approved exceptional role>
generation: 1
status: PLANNED | ACTIVE | PARKED | BLOCKED | VERIFYING | CLOSED
live_handle: <runtime handle when available>
actual_model: <record actual alias/model>
reasoning_effort: <record actual level>
spawn_prefix: /caveman Ultra
mission: <one cohesive workstream>
non_goals: []
authority:
  spec_path: <path>
  spec_ref: <commit/hash>
  plan_path: <path>
  plan_ref: <commit/hash>
workspace:
  branch: <branch>
  worktree: <path or null>
  base_sha: <40-char SHA>
  observed_head_sha: <40-char SHA>
ownership:
  writable_paths: []
  read_only_paths: []
  forbidden_paths: []
skills:
  applicable: []
  not_applicable: []
tools: []
accepted_commits: []
verification:
  required: []
  passed: []
  failed: []
  not_run: []
handoff_path: <repo path>
findings:
  critical: []
  important: []
  minor: []
blockers: []
next_action: <one exact bounded action>
started_at: <ISO-8601>
updated_at: <ISO-8601>
ended_at: null
```

## Compact kickoff prompt

Every spawn prompt starts with the required prefix:

```text
/caveman Ultra

Logical role: <role_id>, generation <n>.
Actual model/reasoning: <record actual values>.
Run manifest: <path>@<sha>.
Role manifest: <path>@<sha>.
Authority: <spec path>@<sha>; <plan path>@<sha>.
Mission: <one cohesive responsibility>.
Non-goals: <explicit exclusions>.
Writable paths: <paths>.
Forbidden paths: <paths>.
Required verification: <checks>.
Handoff path: <path>.
Complete <milestone/task range>, update the durable role manifest, and return commits, verification and findings only.
Do not spawn subagents.
```

## Delta continuation prompt

```text
/caveman Ultra

Continue logical role <role_id>, generation <n>, using the same live thread.
New head: <sha>.
Changed authority/evidence/findings: <small delta or paths>.
Next exact action: <action>.
Reconcile the delta, update the manifest and continue. Do not reload unrelated context.
```

## Replacement-generation prompt

Use this only when the prior runtime generation is no longer available:

```text
/caveman Ultra

Resume logical role <role_id> as generation <n+1>. This is a new runtime process; do not assume hidden-memory continuity.
Read <run manifest>@<sha> and <role manifest>@<sha>.
Verify repository, branch/worktree and current head before editing.
Reconcile accepted commits, open findings, owned paths and next action, then update the manifest with the actual model/reasoning and continue.
Do not spawn subagents.
```

## Handoff record

```yaml
schema: owner-authorized-role-handoff/v1
run_id: <run id>
from_role: <role id + generation>
to_role: <role id + generation or parent>
head_sha: <40-char SHA>
transferred_paths: []
accepted_commits: []
verification: []
open_findings: []
blockers: []
next_action: <exact action>
created_at: <ISO-8601>
```

## Evidence discipline

A manifest records observed facts and pointers. It does not contain hidden chain-of-thought, copied handbooks, secrets, large logs or screenshots. Store detailed evidence in dedicated repository artifacts and reference them by path and SHA.
