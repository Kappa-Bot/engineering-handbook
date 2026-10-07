---
id: pb-agent-runtime-routing
kind: playbook
status: active
owner: engineering
version: "1.0"
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
last_verified: 2026-10-07
review_due: 2027-01-07
supersedes:
  - pb-owner-authorized-role-pod-execution
---

# Agent Runtime Routing

Use this playbook after normal task authority is established.

## 1. Decide whether a model worker is needed

Ask in order:

1. Can an existing deterministic tool/script do it?
2. Can the current controller finish it more cheaply than transferring context to a worker?
3. Would one specialist materially improve quality, isolate context or move implementation to a cheaper model?
4. Is independent review required by `std-agent-runtime-routing`?

Stop at the first adequate route.

## 2. Select the specialist

Search the current Agency Agents catalog for the narrowest relevant profile. Read the current profile before use.

Prefer one primary specialist. Add another only for a distinct responsibility; do not stack overlapping "senior", "architect", "reviewer" personas ceremonially.

`Agents Orchestrator` is selected only for genuinely complex decomposition/coordination, never merely because agents are being used.

## 3. Classify runtime difficulty

Record only material dimensions:

```text
decision_uncertainty: low | medium | high
dependency_breadth: local | repository | cross-system
impact: low | medium | high | critical
verification_strength: strong | partial | weak
context_transfer_cost: low | medium | high
```

Then determine whether the cheap implementer gate is satisfied.

## 4. Choose model and effort

Fast path:

```text
tool/script                         → no spawn
mechanical specialist              → Luna low
frozen + strongly verified build   → Luna medium
bounded tricky build               → Luna high or Sol medium
complex repo/cross-component       → Sol medium/high
high-ambiguity/high-impact reason  → Astra high
exceptional reasoning              → Astra xhigh
max                                 → eval-gated exception
```

Resolve actual model IDs/efforts against the current spawn allowlist. Set **both** explicitly.

Do not infer model from persona name. Do not infer effort from "reviewer" versus "implementer".

## 5. Build the minimal dispatch

A spawn receives:

```text
Agency Agent profile + observed upstream revision
task outcome
authority/spec/plan refs
decision already frozen vs still open
writable/read-only/forbidden scope
acceptance criteria
verification required
requested model + effort
routing reason
cost/sensitive-action constraints
handoff target
```

Prefer isolated/minimal context when supported. Do not fork an entire conversation merely for convenience.

## 6. Execute economically

During implementation:

- keep the same worker for the cohesive responsibility;
- use focused tests while fixing;
- send only material authority/head/blocker deltas;
- do not ask for progress chatter;
- avoid duplicate MCP/CLI operations;
- stop a worker from exploring adjacent cleanup unless scope requires it.

If a cheap worker succeeds against strong verification, do not re-run the implementation on a stronger model for reassurance.

## 7. Handle failure by cause

```text
environment failure      → fix environment
authority ambiguity      → resolve authority
clear code defect        → same worker fixes
bad/repeated hypothesis  → change method/specialist
insufficient reasoning   → raise effort or model
context overload         → narrow/restart from durable state
new risk                 → reclassify + review gate
```

Avoid changing model and effort simultaneously unless necessary.

## 8. Decide review

If the Standard's independent-review triggers do not apply and deterministic verification is strong, the controller may inspect the diff and close the task without another model worker.

If review is required, route the reviewer independently using the same model/effort heuristics. Do not default review to Astra.

## 9. Integrate and verify

The controller:

- reconciles worker output with current head;
- runs the required exact-head gates;
- verifies provider/Production state only when relevant and authorized;
- reports unrun/unreachable evidence truthfully;
- closes only after critical/important blocking findings are resolved or explicitly dispositioned.

## Codex routing backstop

Where supported, configure a deliberate efficient subagent default such as:

```toml
[agents]
default_subagent_model = "<current efficient model from the spawn allowlist>"
default_subagent_reasoning_effort = "medium"
```

This prevents accidental inheritance of an expensive controller configuration. Explicit per-spawn model and effort remain required.
