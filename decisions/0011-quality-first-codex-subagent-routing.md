---
id: adr-0011-quality-first-codex-subagent-routing
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - codex
  - all-repositories
sources:
  - src-openai-models
  - src-openai-model-selection
  - src-openai-reasoning
  - src-openai-codex-subagents
  - src-openai-codex-config-reference
  - src-openai-responses-multi-agent
  - src-openai-agents-api-multi-agent
last_verified: 2026-11-18
review_due: 2027-02-18
---

# Quality-first Codex delegation, model and reasoning routing (November 2026)

## Context

ADR 0006 removed fixed parent/design-quality/delivery roles and made persona, model and effort independent. Its October 2026 economy revision subsequently defaulted most frozen implementation to Luna/low and constrained stronger reasoning to exceptions. That cost-minimization bias no longer matches the owner's 2026-11-18 instruction to invest more tokens and reasoning effort to improve technical quality, while retaining the existing incremental monetary ceiling and the two-subagent working preference.

Current official Codex documentation also distinguishes native custom agent files from upstream personas, explicitly defines `[agents]` defaults and custom-file precedence, and separates Codex local settings from Responses API and Agents API multi-agent configuration. These distinctions were missing or underspecified in the older routing documentation.

## Decision

1. Retain dynamic Agency Agents specialization, zero subagents by default, explicit delegation activation and at most two concurrent subagents without further owner authorization. Do not revive permanently bound design/delivery roles.
2. Route normal substantial coding, diagnosis and integration to GPT-6.2 Sol/high where actually available; raise to xhigh for complex coupling. Route demanding architecture, authorization, data or adversarial review to GPT-6.2 Astra/high–xhigh without a forced low-model failure first.
3. Use GPT-6 Luna/high for bounded or read-heavy tasks, optional GPT-6.1 Terra/high for supported visual/browser work, and GPT-6.1 Sol/high as an observed compatibility fallback. Choose based on task complexity, client availability and actual tools, not persona names.
4. Keep `max` as a demonstrated-benefit exception; do not confuse client-specific `ultra`, `/caveman Ultra` or Responses API reasoning parameters with a universally available Codex CLI setting.
5. Set model **and** effort at spawn where possible. Inspect selected native agent TOML: its fields override explicit spawn values, then `[agents]` defaults apply, then parent/model defaults. Prefer a compatible Sol/high backstop and a two-child cap on supported local Codex installations; verify observed effective runtime before reporting it.
6. Treat permission/sandbox and monetary authority independently from model choice, native agent type, custom skills and upstream persona. No automatic GitHub Actions, additional API credits, new provider or paid runtime tier.
7. Expand advisory dispatch/handoff targets (3,000 input tokens and 650 words; larger material contracts as needed). Never truncate scope, tests, safety constraints or review just to fit a small prompt.

## Consequences

- More reasoning tokens and latency may be consumed per authorized engineering workstream; this is deliberate, **not** authorization for charges outside included usage.
- Sol/high is a preference, not a universal optimum. Representative verification and actual effective settings govern claims; no numerical quality/cost improvement is asserted without comparable evidence.
- A custom native agent file can silently replace an intended model or effort; dispatch must inspect profile precedence and disclose `NOT_OBSERVED` when runtime evidence is absent.
- Older clients may require an available compatibility model/effort. A public API model catalog alone cannot prove a particular Codex spawn allowlist.
- The historical fixed-role and October low-effort policies remain archived evidence. This ADR supersedes the **cost-first routing decisions** of ADR 0006, not its retained dynamic-persona separation and zero-spawn default.

## Canonical implementation

- `std-agent-runtime-routing`
- `pol-agent-operating-model`
- `pb-agent-runtime-routing`
- `ref-agent-runtime-manifest`
- `pb-codex-global-adoption`
- `machine-readable/agent-runtime-routing.v1.json`
- `agent-config/codex/AGENTS.global.md`
- `agent-config/codex/skills/engineering-handbook/SKILL.md`
