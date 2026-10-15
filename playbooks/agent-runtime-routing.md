---
id: pb-agent-runtime-routing
kind: playbook
status: active
owner: engineering
version: "1.1"
applies_to:
  - all-repositories
  - codex
  - multi-agent-execution
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-openai-models
  - src-openai-reasoning
  - src-agency-agents
last_verified: 2026-10-15
review_due: 2027-01-15
supersedes:
  - pb-owner-authorized-role-pod-execution
---

# Agent Runtime Routing

Use after the task is authorized. [The Standard](../standards/agent-runtime-routing.md) owns the rules and budgets; [the JSON profile](../machine-readable/agent-runtime-routing.v1.json) is its projection. Do not copy a second policy into consumer repositories.

## 1. Resume, do not rediscover

Keep the current repository session. Read its dirty state, current authority and pending task, then the relevant delta. Do not restart completed waves, load the entire Handbook or duplicate a conversation merely to obtain a fresh agent.

Prefer an existing deterministic tool, then direct controller work, then a justified specialist. For an owner-authorized multi-agent initiative, retain the valuable specialist work and required independent review; reduce its per-worker settings and context instead of removing the paradigm.

## 2. Prepare the economical runtime

At a cohesive boundary:

1. Inspect the actual Codex/harness version, available model IDs, effort choices and included account access.
2. Read the existing subagent defaults and the selected custom profile's model/effort settings. Preserve unrelated user configuration and upstream Agency persona content.
3. Where these fields are supported, apply the equivalent of this backstop, substituting an **observed** efficient model ID:

```toml
[agents]
default_subagent_model = "<observed efficient model ID>"
default_subagent_reasoning_effort = "low"
```

4. Keep agents enabled and enforce the Standard's normal concurrency through supported configuration/controller scheduling. Do not invent TOML keys or hard token caps. Existing runtime permissions are not changed by this backstop.
5. Verify resolved settings through the harness's supported readback or metadata on the first useful worker. Record requested and actual model/effort; use NOT_OBSERVED where unavailable. Do not spawn a dummy expensive worker merely to prove that agents exist.
6. An unsupported field is a configuration issue, not a reason to silently inherit the controller. Fix the mapping or use a documented already-authorized economical route; retain required independent review.

This repository update does **not** itself edit `~/.codex`, a developer workstation or an already running worker. Record adoption separately from policy publication. Do not hot-swap a useful worker mid-task solely to change its preset.

## 3. Select the specialist and contract

Search the current Agency Agents catalog, read the narrowest matching profile, and record its upstream revision. Refresh/reconcile between workstreams, not during a worker's responsibility. Orchestrator and overlapping senior/architect/reviewer personas are not a default team.

Classify uncertainty, dependency breadth, impact, verification strength and context-transfer cost. Identify frozen decisions and the few decisions actually owned by this task. Improve an incomplete contract before increasing effort.

## 4. Route model and effort explicitly

Use the Standard's current table. The principal change in revision 1.1 is **efficient/low for frozen bounded work with strong verification**, rather than medium by habit. Use medium when a named interaction warrants it. A balanced integrated reviewer is justified by the actual risk, not its persona name. High/frontier/xhigh/max require their documented exception conditions.

Set model and effort on every supported spawn. Check that custom profile settings and resumptions preserve the intended route. Record unsupported or unobserved values honestly; a requested low setting alone is not effective-runtime evidence.

## 5. Send one compact dispatch

```text
Specialist: selected slug/name @ observed revision.
Task: one cohesive outcome; task ID and base SHA.
Authority: current Handbook IDs + repo/spec/plan paths.
Frozen: decisions not to redesign. Open: only decisions owned here.
Writable: exact files/subtree. Read-only/forbidden: exact boundaries.
Acceptance: task-local criteria and interfaces.
Verify: focused commands and required final evidence.
Runtime: explicit observed-allowlist model + effort; route reason.
Return: diff/commits, real command results, findings/blockers, next action.
```

Use the Standard's advisory dispatch/handoff budgets, citing source paths and evidence rather than pasting them. Include any material fact needed for correctness even when it exceeds the budget; record the exception. No hidden reasoning, secrets, full transcripts or unbounded logs in handoffs.

## 6. Execute and diagnose economically

Keep one worker for its cohesive responsibility. Send only changed authority, head or blocker information. Use focused checks while fixing and completion events/waits rather than repeated progress polling. Serialize shared writes. Never let a worker spawn an uncontrolled second hierarchy.

Do not rerun a verified economical implementation on a stronger model for reassurance. At the Standard's repeated-failure boundary, diagnose the cause before another attempt: environment, authority, code defect, method, capability, context overload or changed risk. Do not implement an automatic model ladder. Return subsequent bounded tasks to the economy default after an exception.

## 7. Review the actual risk

Apply the unchanged independent-review triggers in the Standard. A low-risk mechanical change may need only tests and controller inspection. Security, tenancy, durable data, money and partial concurrency verification cannot lose required independence to meet a token target. The author is not an independent reviewer.

A compact review consumes the final diff, invariant list, focused tests and observed results, expanding only where an actual risk needs more context. Missing review capability means BLOCKED for that gate, not PASS or permission to weaken acceptance.

## 8. Integrate, measure and hand off

The controller reconciles outputs with the current head, preserves others' work, runs the required exact-candidate gates and makes final claims. Provider/Production actions retain their separate authorization and cost boundaries.

Record actual usage only when available, including retries and reused input. Null/NOT_OBSERVED is correct for unavailable counters. Do not claim percentage savings from a cheaper requested preset without comparable usage measurements.

The closing handoff names changed paths/commits, effective routing or its limitation, commands and exits, remaining findings and unrun gates. Distinguish policy published, local configuration applied, implementation verified and Production verified.
