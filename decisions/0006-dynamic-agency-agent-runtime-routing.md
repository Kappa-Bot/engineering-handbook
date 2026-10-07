---
id: adr-0006-dynamic-agency-agent-runtime-routing
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - codex
  - all-repositories
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-openai-models
  - src-openai-reasoning
  - src-openai-model-selection
  - src-agency-agents
last_verified: 2026-10-07
review_due: 2027-01-07
supersedes:
  - adr-0004-owner-authorized-compact-role-pods
---

# Replace fixed role pods with dynamic Agency Agents runtime routing

## Context

The fixed `parent / design-quality / delivery` topology solved an earlier coordination problem but also encoded two assumptions that no longer fit the operating model:

1. specialist identity was tied to a permanent role rather than the actual task;
2. model and reasoning effort were tied to that role rather than to uncertainty, impact, verification and context cost.

After adopting Agency Agents as the upstream specialist-persona catalog, retaining fixed internal roles would make those personas wrappers around a second Kappa-Bot taxonomy. It also encourages expensive defaults such as mandatory xhigh review or high-capability implementation even when a frozen contract can be implemented and verified cheaply.

## Decision

Adopt `DYNAMIC_AGENCY_AGENT_ROUTING`.

- The current controller remains responsible for continuity, integration and final claims; it is not a permanent specialist persona.
- Use zero spawned workers by default.
- Prefer deterministic tools, then direct controller execution, before spawning.
- Spawn an Agency Agents specialist only when its expected value exceeds context/coordination cost.
- Do not require `Agents Orchestrator`; it is an optional specialist for genuinely complex coordination.
- Select specialist persona, model and reasoning effort independently.
- Every spawn explicitly selects model and effort when supported.
- Prefer the efficient model tier for frozen, strongly verifiable implementation.
- Use Sol/Astra only when the task's reasoning/impact profile justifies the additional cost.
- Independent model review is risk-triggered rather than universal.
- Escalate by failure cause; do not automatically walk a Luna→Sol→Astra ladder.
- Optimize total tokens/resources to verified acceptance, not the cost of one isolated call.
- Keep routine concurrency at zero/one; two workers are reserved for truly independent work or required independent review.
- Keep sensitive-action, provider, billing and Production permissions governed separately.

## Model-routing intent

Current preferred model family mapping:

```text
efficient → GPT-6 Luna
balanced  → GPT-6.1 Sol
frontier  → GPT-6 Astra
```

These are current capabilities, not permanent aliases. Runtime must resolve the actual spawn allowlist and record requested/actual values.

Reasoning effort is selected separately:

```text
low     → mechanical / tightly constrained
medium  → normal bounded engineering; default cheap implementation
high    → interacting constraints / difficult diagnosis / integration
xhigh   → exceptional reasoning-heavy work with demonstrated need
max     → eval-gated exception only
```

## Consequences

### Positive

- Agency Agents becomes the real specialist taxonomy rather than a skin over fixed internal roles.
- Frozen implementation can move to Luna low/medium when verification is strong.
- Expensive reasoning is concentrated on unresolved decisions and difficult risk boundaries.
- Review cost becomes proportional to risk.
- A controller with rich existing context can finish small work directly instead of paying spawn/rediscovery overhead.
- Model-routing behavior can be evaluated independently from persona quality.

### Risks

- Dynamic routing requires better runtime judgment than a fixed role map.
- A cheap implementer is unsafe when semantics are not actually frozen or tests do not cover the material failure class.
- External persona/profile changes still require provenance.
- Runtime model availability changes, so requested names must never be reported as actual without observation.

## Rejected alternatives

### Keep fixed parent/design-quality/delivery roles

Rejected. It duplicates Agency Agents and hardcodes model semantics into organizational labels.

### Make Agents Orchestrator mandatory

Rejected. Its upstream workflow is intentionally comprehensive but introduces unnecessary planning/QA ceremony for small or strongly verified tasks.

### Always use Luna for implementation and Astra for review

Rejected. Implementation and review can each range from mechanical to highly ambiguous. Runtime difficulty, not job title, selects model/effort.

### Always escalate on failure

Rejected. Provider/environment/authority failures are not reasoning failures.

## Canonical implementation

- `std-agent-runtime-routing`
- `pb-agent-runtime-routing`
- `ref-agent-runtime-manifest`
- `machine-readable/agent-runtime-routing.v1.json`
- `ref-agency-agents-specialist-routing`
