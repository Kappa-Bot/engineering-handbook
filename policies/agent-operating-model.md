---
id: pol-agent-operating-model
kind: policy
status: active
owner: engineering
version: "0.3"
applies_to:
  - all-repositories
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-git-worktree
last_verified: 2026-09-02
review_due: 2026-12-02
---

# Agent Operating Model

## Objective

Use coding agents as disciplined engineering workers without turning every task into a giant prompt, multi-agent ceremony, or permanent context dump.

The Engineering Handbook governs **all engineering work across repositories**. That does not mean every task loads the whole handbook: trivial work may need only the distributed global baseline plus repo-local instructions, while non-trivial/risky work resolves specialized handbook context progressively.

## Context model

Permanent context MUST stay small.

Preferred layering:

```text
small global handbook baseline
        +
small repo-local AGENTS.md
        +
current task
        ↓
resolve focused handbook context / skills / references only when relevant
```

Universal rules belong in the handbook/global distribution artifact. Repo-specific commands, architecture, boundaries, product/domain facts and local decisions belong in the repo. Specialized procedures belong in focused artifacts rather than a giant `AGENTS.md`.

For non-trivial work, prefer the deterministic `engineering-handbook` context router and its delta modes over manually reading broad handbook sections. For trivial repo-local work, do not manufacture a context query or documentation ceremony when the global baseline and local authority already decide the task.

## Session and repository scope

- Default to one active engineering session per repository/task context.
- Keep one repository as the primary unit of work for a session.
- Do not mix unrelated repository changes into one task merely because the agent can access them.
- Cross-repository work SHOULD explicitly identify which repository owns each change and which handbook rule is being propagated.

## Subagents

- Use **zero subagents by default**.
- Subagents MAY be used only after an explicit owner request or permitted repository-local authorization has been recorded as an unambiguous durable activation in the approved task/run manifest.
- General permission to edit a repository is not permission to spawn subagents.
- Do not create subagents simply because a methodology recommends them.
- Do not split work into multiple agents when coordination/context cost exceeds the work saved.

### Owner-authorized role pods

When explicit durable authorization exists, use `OWNER_AUTHORIZED_ROLE_PODS` rather than ad-hoc agent proliferation.

Canonical authority:

- `std-owner-authorized-role-pods` defines activation, topology, model/skill routing, ownership and verification constraints;
- `pb-owner-authorized-role-pod-execution` defines the execution loop;
- `pat-durable-logical-agent-handoff` defines continuity across compaction, agent loss and machine restart;
- `ref-owner-authorized-role-manifest` provides the compact run/role/handoff records;
- `machine-readable/owner-authorized-role-pods.v1.json` is the consistency-checked machine-readable profile.

The normal topology is the parent orchestrator plus at most **two persistent subagents**: one consolidated `design-quality` pod and one consolidated `delivery` pod. One pod is valid. A third subagent is exceptional and requires a documented independent workstream or uncovered review risk.

Under this profile:

- maximum concurrent subagents is two;
- nested spawning is prohibited;
- only the parent orchestrator spawns, integrates, replaces and closes;
- one role owns the complete cohesive workstream instead of one agent per microtask;
- the same live role is reused across milestones while its context remains reliable;
- every Kappa-Bot spawn prompt begins with `/caveman Ultra`;
- a stopped/lost/post-restart role resumes as a new generation from durable state, never from assumed hidden memory;
- exact model, reasoning, skills, ownership, commits, evidence and next action are recorded truthfully;
- subagent reports never replace parent exact-head verification.

## Planning

Planning effort MUST be proportional to task complexity.

- Mechanical, obvious, low-risk work may proceed with a short internal plan.
- Multi-step, architectural, security-sensitive, migration-heavy, or ambiguous work SHOULD produce an explicit spec/plan before implementation.
- A plan MUST NOT become an excuse to postpone straightforward implementation after the design is already approved.

Keep task states distinct when relevant:

```text
research → decision → spec → plan → implementation → verification → adoption
```

Do not silently jump from exploration/research into implementation.

## Scope control

Agents MUST:

- keep the requested outcome primary;
- avoid unrelated refactors;
- avoid speculative abstractions;
- avoid cleanup outside the necessary change;
- make assumptions explicit when they materially affect the solution;
- prefer small, reviewable changes.

## Methodology

Use specialized engineering methods when they fit the work, including:

- brainstorming for unresolved creative/architecture decisions;
- implementation planning for non-trivial multi-step work;
- TDD where behavior can be expressed meaningfully as tests;
- systematic debugging before speculative fixes;
- verification-before-completion;
- code review appropriate to the risk.

Methodology defaults MUST NOT override explicit handbook policies such as the no-worktree or zero-subagent default. Explicit activation of `OWNER_AUTHORIZED_ROLE_PODS` is the narrow opt-in exception to the latter, not a new default.

## Skill routing

Treat installed skills as focused expertise, not a checklist to invoke performatively.

The default portfolio workflow is:

- `caveman` / `/caveman Ultra` when available and applicable for high-efficiency orchestration;
- Superpowers process skills for the exact stage/risk (`brainstorming`, planning, TDD, debugging, verification, review, branch completion, etc.);
- `ui-ux-pro-max`, `taste` and `impeccable` for materially visual UI/UX work where their output can change design quality;
- Emil Kowalski skills selectively for interaction craft: `emil-design-eng`, `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `pick-ui-library`, `prototype`, `ask-sonner`, `write-swift` as the task actually requires.

Rules:

- Discover the exact installed skill/resource before relying on it; do not claim a skill was used when unavailable.
- Use the **smallest skill set that can materially improve the decision or verification**.
- Do not invoke all design/motion skills for every frontend edit.
- `prototype` is appropriate when materially different alternatives are worth comparing, not for settled/mechanical UI.
- Animation skills are appropriate when motion exists or is genuinely under consideration; first ask whether motion should exist at all.
- Library-specific skills apply only when that library/decision is relevant.
- Skills inform implementation but do not override Handbook Governance/Policies/Standards or repo-local product/architecture authority.
- Under role pods, assign skills per role/stage and send deltas after kickoff; do not duplicate the whole skill portfolio into every prompt.

For material design work, apply `pat-design-context-layering` and `pb-frontend-quality-review` before using external precedents as inspiration.

## Token/context efficiency

- Do not paste entire handbooks/research reports into task prompts when a stable ID/path suffices.
- Load the smallest relevant artifact set.
- Prefer links/IDs and focused summaries to duplicated policy prose.
- Keep generated progress reports concise unless detailed evidence is needed for a durable artifact.
- Store deep reusable knowledge centrally; retrieve narrow task-specific context.
- Do not load an entire external design corpus or every installed skill merely to signal rigor.
- When a repo has a compact, authoritative design contract, prefer it over re-explaining the same visual rules in each prompt.
- For role pods, provide one complete kickoff packet and subsequent authority/head/finding/evidence deltas only.

## Handoff

At handoff, the agent SHOULD report:

- outcome delivered;
- files/areas changed;
- verification actually run;
- checks not run and why;
- remaining risks or dependencies;
- Git/workspace state when relevant.

The handoff MUST NOT imply success for unexecuted gates. Long-running role-pod work additionally follows `pat-durable-logical-agent-handoff`.
