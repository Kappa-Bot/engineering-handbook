---
id: ref-agent-runtime-manifest
kind: reference
status: active
owner: engineering
version: "1.1"
applies_to:
  - agentic-workflows
  - multi-agent-execution
  - codex
sources:
  - src-openai-codex-agents
  - src-openai-codex-subagents
  - src-openai-codex-config-reference
  - src-agency-agents
last_verified: 2026-11-18
review_due: 2027-02-18
supersedes:
  - ref-owner-authorized-role-manifest
---

# Agent Runtime Manifest

Create durable routing state only when a spawned worker or long-running initiative needs recovery/provenance. Do not create manifests for trivial direct work.

## Workstream record

```yaml
schema: agent-runtime-workstream/v1
run_id: <stable id>
repository: <owner/repo>
authority_ref: <task/spec/plan or owner instruction>
delegation_authorization: <explicit user request or applicable repo/skill instruction>
base_sha: <sha>
target_branch: <branch>
agency_agents:
  upstream_revision: <observed commit/tag or NOT_OBSERVED>
  reconciliation_state: <CURRENT | OUTDATED | MODIFIED | UNAVAILABLE | NOT_CHECKED>
routing:
  decision_uncertainty: low | medium | high
  dependency_breadth: local | repository | cross-system
  impact: low | medium | high | critical
  verification_strength: strong | partial | weak
  context_transfer_cost: low | medium | high
  cheap_implementer_eligible: true | false
runtime_client: <Codex CLI | app | IDE | Responses API | Agents API | other>
runtime_version: <observed version or NOT_OBSERVED>
workers: []
sensitive_authority:
  paid_actions: false
  provider_resource_creation: false
  destructive_external_actions: false
verification:
  required: []
  passed: []
  failed: []
  not_run: []
next_action: <exact action>
updated_at: <ISO-8601>
```

## Worker record

```yaml
worker_id: <stable id>
generation: 1
specialist:
  slug: <Agency Agents slug>
  name: <display name>
  upstream_revision: <commit/tag>
native_codex_agent_type: <installed type/name or N/A>
native_custom_agent_file: <path or N/A>
native_custom_agent_model_effort_override: <present | absent | NOT_OBSERVED>
mission: <one cohesive responsibility>
routing_reason:
  - <material reason>
requested_model: <resolved model/preset>
requested_reasoning_effort: low | medium | high | xhigh | max | <client-specific supported value>
actual_model: <observed value or NOT_OBSERVED>
actual_reasoning_effort: <observed value or NOT_OBSERVED>
fallback_reason: <why a model/effort was changed, or N/A>
scope:
  writable_paths: []
  read_only_paths: []
  forbidden_paths: []
acceptance: []
verification:
  required: []
  passed: []
  failed: []
  not_run: []
independent_review_required: true | false
accepted_commits: []
findings:
  critical: []
  important: []
  minor: []
blockers: []
next_action: <exact action>
```

## Dispatch template

```text
Delegation authority: <explicit authorization reference>.
Native agent: <installed Codex type / N/A>, custom TOML overrides checked.
Specialist: <Agency Agent slug/name> @ <upstream revision> when used.
Outcome: <bounded outcome>.
Authority: <paths/SHAs>.
Frozen decisions: <what must not be redesigned>.
Open decisions: <only decisions this worker owns>.
Writable: <paths>.
Forbidden: <paths/actions>.
Acceptance: <criteria>.
Verification: <commands/evidence>.
Requested runtime: <model> / <reasoning effort>.
Routing reason: <short material reasons>.
Return: commits/diff, verification, findings/blockers, next exact action. No progress chatter.
```

Do not store hidden chain-of-thought, secrets, copied handbooks or large logs in the manifest.
