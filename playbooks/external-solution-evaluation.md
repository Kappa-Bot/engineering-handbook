---
id: pb-external-solution-evaluation
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# External Solution Evaluation

## Purpose

Evaluate an external library, framework, service, design system, reference implementation, method, or engineering practice before adopting it, adapting it, or using it as evidence.

This playbook operationalizes `pol-reuse-first` and `gov-source-authority`. It does not create a second approval process and does not require a document for every dependency choice.

Use it when the decision is expensive, durable, cross-cutting, security-sensitive, difficult to reverse, or likely to be reused across repositories.

## Decision outcomes

An evaluation should end in one of these relationships with the candidate:

- **adopt** — use substantially as provided;
- **adapt** — reuse the implementation or structure with deliberate changes;
- **learn** — reuse concepts/evidence but implement independently;
- **reject** — the candidate is not a fit for the current need;
- **defer** — evidence is insufficient or the decision is not yet needed.

These are decision outcomes, not lifecycle states for handbook documents.

## 1. Define the actual problem

Before comparing products or projects, state the capability needed and the constraints that matter.

Capture only what can change the decision, for example:

- required behavior;
- integration/runtime constraints;
- data or security boundaries;
- supported platforms;
- accessibility/performance requirements;
- acceptable operational burden;
- licensing or commercial constraints;
- migration/reversibility needs.

Avoid starting with “Should we use X?” when the real question is “What is the lowest-risk way to provide Y?”

## 2. Check internal reuse first

Before deep external research, confirm whether the current repository, handbook, another internal repository, or an existing internal asset already solves the need.

An external option should not displace a working internal solution without a material benefit.

Likewise, an internal solution should not be protected merely because it already exists if a mature external solution materially reduces risk, maintenance, or duplicated engineering effort.

## 3. Gather authoritative evidence

Separate candidate facts from commentary about the candidate.

Prefer evidence according to `gov-source-authority`:

1. specifications/standards and official documentation;
2. original implementation/project documentation;
3. mature reference material;
4. community evidence for discovery or gaps.

Register external sources in `machine-readable/sources.yaml` only when they materially support reusable handbook knowledge. A repo-local one-off evaluation may keep its evidence local instead of polluting the global source registry.

Record uncertainty explicitly. Do not convert an unverified assumption into a negative or positive finding.

## 4. Evaluate applicability

Evaluate the dimensions that could materially change the decision. Mark irrelevant dimensions as `not material` rather than inventing analysis.

Typical dimensions:

### Functional fit

- Does it solve the required problem without substantial unrelated machinery?
- Which required capabilities are missing?
- Which bundled capabilities create unwanted complexity?

### Maintenance and maturity

- Is the project/service actively maintained where that matters?
- Is there a stable release/support model appropriate to our use?
- Would ownership transfer to us if the upstream project stalls?

Popularity alone is not maintenance evidence.

### Security and trust boundary

Consider attack surface, dependency/supply-chain exposure, privilege/data access, update model, secrets, hosting, and whether the candidate moves a trust boundary.

Security depth should match the actual risk. Do not perform ceremonial security analysis for a static documentation helper, and do not treat a security-critical dependency as a cosmetic choice.

### Performance and resource cost

Evaluate only where the candidate could materially affect latency, startup, bundle/runtime cost, storage, compute, network, or operational limits.

Prefer measured evidence over reputation when performance is a decision driver.

### Accessibility and UX

For user-facing solutions, assess whether the candidate supports the applicable accessibility and interaction requirements without costly remediation.

### Licensing and commercial terms

Determine whether intended use, redistribution, modification, SaaS/commercial deployment, attribution, or generated artifacts are compatible with the actual terms.

“Open source”, “free”, and “free to read” are not interchangeable licensing conclusions.

### Operational complexity

Account for deployment, upgrades, observability, backups, incident handling, configuration, local development, and skills required to own it.

A feature-rich platform can be a worse solution than a small component if its operating cost dominates the value it provides.

### Lock-in and reversibility

Ask what becomes proprietary or difficult to migrate: data, APIs, workflows, runtime assumptions, UI/component contracts, hosting, or team knowledge.

Lock-in is a tradeoff, not an automatic rejection. Evaluate it against the value received and realistic migration cost.

### Architecture fit

Check compatibility with existing boundaries, deployment/runtime model, ownership, data model, and public contracts.

Do not distort a healthy architecture merely to accommodate a candidate unless the architectural change is itself the deliberate decision.

### Migration and adoption cost

Include integration effort, migration, retraining, coexistence period, rollback, and cleanup of the displaced solution.

A candidate can be better in isolation and still not justify migration today.

### Long-term ownership

Make explicit who owns:

- configuration and upgrades;
- defects or custom adaptations;
- vendor/upstream monitoring;
- migration if the solution is retired.

## 5. Compare credible alternatives

Do not build a comparison table with many weak options just to appear comprehensive.

Compare the smallest set that can realistically change the decision:

- current/internal solution where one exists;
- strongest external candidate(s);
- a small custom implementation when it is genuinely viable;
- “do nothing/defer” when the capability is optional.

Do not use weighted numeric scoring by default. Scores often hide subjective assumptions behind false precision. Use explicit tradeoffs unless repeatable procurement at scale later justifies a scoring model.

## 6. Resolve uncertainty proportionally

If uncertainty is material and cannot be resolved from evidence, run the smallest useful validation:

- focused spike;
- compatibility test;
- benchmark;
- accessibility check;
- license/legal review;
- security review;
- small integration proof.

A proof of concept should answer a decision question, not quietly become production code by inertia.

Delete or deliberately promote experimental artifacts after the decision; do not leave unexplained prototype debt in a consumer repository.

## 7. Record the decision only when useful

Use `templates/external-solution-evaluation.md` when the reasoning is worth preserving.

Keep the evaluation in the consumer repository when its applicability is local.

Promote a reusable evaluation or learning into the handbook only when it can prevent meaningful repeated research across repositories. Use `gov-knowledge-promotion` rather than creating a global reference automatically.

A durable architecture/platform choice may additionally require an ADR. The evaluation provides evidence; the ADR records the internal decision. Do not make one document pretend to be both when the distinction matters.

## 8. Define review triggers

Time-based re-evaluation is not always necessary. Prefer concrete triggers where possible:

- major upstream version or license change;
- security incident/advisory affecting the decision;
- repository architecture changes;
- significant cost/usage threshold;
- candidate maintenance becoming uncertain;
- a previously missing requirement becoming important;
- migration opportunity that changes switching cost.

If the evaluation becomes a handbook artifact, also use lifecycle metadata appropriate to that artifact.

## Compact decision rule

A candidate is ready to adopt/adapt when:

- the real problem and constraints are explicit;
- stronger internal reuse paths have been considered;
- material factual claims have adequate evidence;
- relevant fit/ownership risks are understood;
- credible alternatives have been compared;
- unresolved uncertainty is below the cost/risk threshold of the decision;
- the chosen relationship (`adopt`, `adapt`, `learn`, `reject`, `defer`) is explicit.

The goal is enough evidence to make a good reversible decision—not exhaustive research.
