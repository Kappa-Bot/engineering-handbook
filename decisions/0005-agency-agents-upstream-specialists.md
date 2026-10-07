---
id: adr-0005-agency-agents-upstream-specialists
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - codex
  - all-repositories
sources:
  - src-agency-agents
  - src-agency-agents-app
  - src-openai-codex-agents
last_verified: 2026-10-07
review_due: 2027-01-07
---

# Adopt Agency Agents as the upstream specialist-persona catalog

## Routing supersession

ADR-0006 supersedes this decision's temporary assumption that Agency Agents profiles must live inside fixed `parent / design-quality / delivery` roles. The durable part of this ADR remains active: Agency Agents is the upstream specialist-persona catalog, profiles should normally remain upstream-managed, and Handbook/repo authority outranks persona instructions.

## Context

Kappa-Bot already has a deliberately small execution topology: a parent orchestrator plus, when explicitly authorized, the persistent `design-quality` and `delivery` roles. Maintaining another Kappa-Bot-specific library of engineering personas would duplicate community work, increase prompt drift and force us to maintain specialist content that is not part of our product authority.

Agency Agents provides a large, actively maintained, MIT-licensed catalog of specialist personas with Codex conversion/install support. Its value is specialization, not governance.

## Decision

Adopt Agency Agents as the **default upstream specialist-persona catalog** for engineering work.

- Keep `parent = Sol 6.1 high`, `design-quality = Astra 6 xhigh`, and `delivery = Luna 6 xhigh` as the owner-default execution topology.
- Apply Agency Agents specialist profiles **inside** those roles. A profile does not create a third delegated role or nested agent.
- Prefer upstream profiles unchanged and benefit from community updates. Kappa-Bot-specific forks are exceptional and require repeated evidence that upstream cannot satisfy a durable requirement.
- Select specialists dynamically from the current catalog; keep only a small fast-path mapping in the Handbook.
- Refresh/reconcile upstream specialist content at safe boundaries between cohesive runs, record the observed revision for material use, and fall back to the last known-good revision when refresh fails.
- Keep process methods separate from specialist personas. The Handbook owns required planning/verification behavior; optional process skills can assist but are not the agent taxonomy.
- Handbook Governance/Policy/Standards, permitted repo-local authority and approved task scope always outrank external persona instructions.

## Consequences

### Positive

- Community improvements can flow into Kappa-Bot without maintaining a parallel persona fork.
- Codex can choose specialists by actual task competency rather than by a fixed home-grown roster.
- The two-role low-communication topology remains intact.
- Specialist content can evolve without bloating permanent Handbook context.

### Costs and risks

- External persona changes are a supply-chain/input change and can alter behavior.
- Reproducibility requires recording the material upstream revision.
- Updating the Agency Agents application is not by itself evidence that installed personas were reconciled.
- External instructions must be treated as subordinate to Kappa-Bot authority and permissions.

## Rejected alternatives

### Maintain Kappa-Bot copies of every useful persona

Rejected. It forfeits upstream maintenance and creates prompt drift.

### Install/activate the entire catalog for every task

Rejected. It wastes context and makes routing less deterministic.

### Replace Sol/Astra/Luna roles with Agency Agents display-name roles

Rejected. Specialist identity and execution topology solve different problems.

### Spawn one subagent per specialist

Rejected. It violates the compact role-pod model and multiplies coordination cost.

## Operational reference

Use `ref-agency-agents-specialist-routing` for selection, role application, update/reconciliation and fast-path guidance.
