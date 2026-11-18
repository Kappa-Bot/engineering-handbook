---
id: pb-agent-runtime-routing
kind: playbook
status: active
owner: engineering
version: "2.0"
applies_to:
  - all-repositories
  - codex
  - multi-agent-execution
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-openai-models
  - src-openai-reasoning
  - src-openai-codex-subagents
  - src-openai-codex-config-reference
  - src-openai-responses-multi-agent
  - src-openai-agents-api-multi-agent
  - src-agency-agents
last_verified: 2026-11-18
review_due: 2027-02-18
supersedes:
  - pb-owner-authorized-role-pod-execution
---

# Agent Runtime Routing

Use after the task is authorized. [The Standard](../standards/agent-runtime-routing.md) owns the rules and budgets; [the JSON profile](../machine-readable/agent-runtime-routing.v1.json) is its projection. Do not copy a second policy into consumer repositories.

## 1. Resume, do not rediscover

Keep the current repository session. Read its dirty state, current authority and pending task, then the relevant delta. Do not restart completed waves, load the entire Handbook or duplicate a conversation merely to obtain a fresh agent.

Prefer an existing deterministic tool, then direct controller work, then a justified specialist. Delegation must first be authorized explicitly by the user or an applicable repository/skill instruction. When authorized, preserve independent work/review where useful; do not replace substantive analysis with automatic low-effort routing or multiply workers solely because a model is available.

## 2. Discover the real Codex runtime and configure a quality-first backstop

At a cohesive boundary:

1. Identify Codex CLI, desktop/app, IDE, cloud or an API harness. Check its real version, spawn tool schema, model/effort allowlist, tool permissions and included account access. The public API catalog alone is insufficient.
2. Inspect the existing `config.toml`, `[agents]` settings and any native custom agent files (`.codex/agents/*.toml` in-repo, `$CODEX_HOME/agents/*.toml` globally). Keep upstream Agency persona contents and unrelated settings intact.
3. For a compatible current Codex **local** installation and an observed available Sol model, use this *illustrative* backstop after merging with the user's existing configuration (not as a replacement file):

<!-- subagent-config-example -->
```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 2
default_subagent_model = "gpt-6.2-sol"
default_subagent_reasoning_effort = "high"
```

4. If Sol 6.2 is not on that client's actual picker/allowlist, **do not paste an invalid ID**. Choose an observed supported compatibility model/effort (`gpt-6.1-sol` / high is a possible IDE fallback), document it, and keep the user's existing service tier/permissions. The concurrency key caps child threads only, not the primary; a session can impose a lower limit.
5. Do **not** copy `[agents]` into an Agents API or Responses API request. Those runtimes expose different `multi_agent` session/request fields; nor do you need to install an obsolete `[features] multi_agent` flag just because an old guide used it. Use the actual advertised schema.
6. Verify the resolved values through readback or metadata on the first **useful authorized** worker. Record requested and actual model/effort (or `NOT_OBSERVED`), including any custom-file override. Do not spawn a dummy worker or make extra billable requests for configuration validation.

This Handbook update does **not** edit `~/.codex`, a developer workstation or an already running worker. Record adoption separately from policy publication. Do not hot-swap useful workers solely to change labels.

### Native Codex agent files are not Agency Agents personas

Local Codex offers `default`, `worker` and `explorer` plus optional project/global TOML agent types. Each custom file needs `name`, `description` and `developer_instructions`, and may set `model`/`model_reasoning_effort`. A specialist persona from Agency Agents can inform that agent's task instructions, but reading a persona does not make it a registered Codex `agent_type`; discover the actual installed types before invocation. Avoid duplicating the upstream specialist catalog as dozens of overlapping native agent files.

For a team-owned native profile, a **valid minimal** project file looks like:

```toml
name = "handbook_reviewer"
description = "Independent evidence-focused review for a previously authored engineering change."
model = "gpt-6.2-sol"
model_reasoning_effort = "high"
developer_instructions = """
Review the actual diff and relevant contracts. Do not edit files.
Report concrete defects, impacted paths, severity, reproduction and remaining uncertainty.
Never grant yourself extra permissions or suppress required verification.
"""
```

**Override precedence matters:** model/effort in the selected custom agent file win; absent that, explicit spawn values win over `[agents]` defaults, which win over parent values. If a different model is selected without an effort, Codex may use that model's default. A custom file setting only `model` preserves previously resolved effort and can produce an incompatible combination. Check both fields together, and do not assume that `--model`, a spawn argument, profile text or resumption overrode the custom TOML.

Custom agent files **cannot** elevate sandbox/approval/provider/MCP permissions. "Read-only" instructions do not create a read-only sandbox. Configure those controls on the parent session, and enforce write ownership operationally. The installed runtime is authoritative about which capability-reduction flags actually exist.

## 3. Select the specialist and contract

Search the current Agency Agents catalog, read the narrowest matching profile, and record its upstream revision. Refresh/reconcile between workstreams, not during a worker's responsibility. Orchestrator and overlapping senior/architect/reviewer personas are not a default team.

Classify uncertainty, dependency breadth, impact, verification strength and context-transfer cost. Identify frozen decisions and the few decisions actually owned by this task. Give the worker adequate source material and reasoning budget instead of shrinking the dispatch until it loses critical semantics.

## 4. Route model and effort explicitly

Use the Standard's current task matrix. Ordinary substantial engineering and review now start at **Sol 6.2/high**; more coupled investigations at Sol/xhigh; difficult architecture/security/data reviews can use Astra/high–xhigh upfront; Luna/high handles bounded, clear, verifiable work. Terra/high is optional for real visual/browser interaction if that client supports it. `medium` is a legitimate bounded alternative; `max` requires a concrete evidenced reason. `ultra` is not automatically a CLI-compatible effort and `/caveman Ultra` is a separate optional method.

Set model **and** effort on every supported spawn. Inspect native custom-file precedence, resolved agent type, custom skills/capabilities, real model support and resumption before relying on that pair. Record unsupported/unobserved values honestly; a requested setting is not effective-runtime evidence.

### Invocation checklist by client

| Surface | How to invoke | What not to assume |
| --- | --- | --- |
| Codex CLI | Explicitly request the delegated work and role(s), inspect via `/subagents`; `config.toml` and optional native agent files affect routing | `/subagents` is a thread UI, not an authorization or fixed spawn schema |
| Codex desktop/app or IDE | Request delegation in the chat; use the actual available subagent threads/controls and model picker | App/IDE availability, agent types and selected effort may differ |
| Native spawn tool | Pass only advertised `model`, `reasoning_effort`, agent-type and context-fork fields, if they exist; specify both model and effort | Do not invent `agent_type`, `fork_turns`, `close_agent` or support for model overrides if absent |
| Responses API | Configure `multi_agent` at request level where supported | Not `[agents]`, `.codex/agents/` or local CLI flags |
| Agents API | Configure `agent.multi_agent` for session/agent where supported | Not the same configuration or lifecycle as Responses or CLI |

If a tool accepts isolated vs full context forks, send **the minimal context that preserves local authority** and paths/SHAs; do not presume identical fork override support across harness versions. Distinguish supported lifecycle actions (`followup_task`, `send_message`, wait, interrupt, close) from older versions; do not busy-poll or recreate a worker merely because a close tool is absent.

Example user-level CLI/app request for a sufficiently isolated review (only after delegation is authorized):

```text
Delegate two independent read-only reviews of this branch against main.
Worker A: trace authorization/tenant/data correctness; return file references and reproductions.
Worker B: inspect concurrency, missing tests and release regressions; return evidence only.
Where supported, use Sol 6.2/high for both; if the installed client cannot route that model,
report the observed fallback. Do not edit files, trigger GitHub Actions, deploy or spend money.
Wait for both; deduplicate findings, verify them against the diff, then report blockers.
```

## 5. Send one compact dispatch

```text
Delegation authorization: exact user/repo/skill reference.
Native type: selected installed Codex agent type, if applicable.
Specialist: selected Agency persona slug/name @ observed revision, if useful.
Task: one cohesive outcome; task ID and base SHA.
Authority: current Handbook IDs + repo/spec/plan paths.
Frozen: decisions not to redesign. Open: only decisions owned here.
Writable: exact files/subtree. Read-only/forbidden: exact boundaries.
Acceptance: task-local criteria and interfaces.
Verify: focused commands and required final evidence.
Runtime: requested supported model + effort; inspected native TOML overrides; route reason.
Return: diff/commits, real command results, findings/blockers, next action.
```

Use the Standard's enlarged advisory dispatch/handoff budgets, citing source paths and evidence rather than pasting them. Include any material fact needed for correctness even when it exceeds the budget; record the reason. No hidden reasoning, secrets, full transcripts or unbounded logs in handoffs.

## 6. Execute with sufficient depth and diagnose by cause

Keep one worker for its cohesive responsibility. Send only changed authority, head or blocker information. Use focused checks while fixing and completion events/waits rather than repeated progress polling. Serialize shared writes. Never let a worker spawn an uncontrolled second hierarchy.

Do not rerun a verified implementation on a stronger model merely for reassurance. At the Standard's repeated-failure boundary, diagnose the cause before another attempt: environment, authority, code defect, method, capability, context overload or changed risk. Do not implement an automatic model ladder. Route subsequent tasks on their own merits; do not inherit an emergency `max` or force Luna/low.

## 7. Review the actual risk

Apply the unchanged independent-review triggers in the Standard. A low-risk mechanical change may need only tests and controller inspection. Security, tenancy, durable data, money and partial concurrency verification cannot lose required independence to meet a token target. The author is not an independent reviewer.

A thorough review consumes the final diff, relevant contracts/invariants, focused tests and observed results, expanding where risk needs more context. Sol/high–xhigh is normal for integrated review and Astra/high–xhigh for complex security/architecture. Missing review capability means BLOCKED for that gate, not PASS or permission to weaken acceptance.

## 8. Integrate, measure and hand off

The controller reconciles outputs with the current head, preserves others' work, runs the required exact-candidate gates and makes final claims. Provider/Production actions retain their separate authorization and cost boundaries.

Record actual usage only when available, including retries and reused input. Null/NOT_OBSERVED is correct for unavailable counters. Higher reasoning usage is authorized within included entitlements, **not a grant of extra API credits or paid services**. Do not claim quality or cost improvements without comparable evidence. Do not activate GitHub Actions or paid CI to prove this routing.

The closing handoff names changed paths/commits, effective routing or its limitation, commands and exits, remaining findings and unrun gates. Distinguish policy published, local configuration applied, implementation verified and Production verified.
