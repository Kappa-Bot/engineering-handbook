# Handbook Compiler & Agent Context Pipeline — Design

Date: 2026-08-17
Status: proposed design
Branch: `docs/handbook-compiler-agent-context-design`

## Problem

The Engineering Handbook already provides governed cross-repository engineering knowledge with progressive disclosure, but agents still spend too much runtime effort on work that can be prepared deterministically:

- deciding which handbook artifacts matter;
- opening and discarding documents;
- rediscovering repository topology, capabilities, commands and verification routes;
- repeating the same planning questions across tasks;
- duplicating handbook prose inside plans/specifications;
- re-deriving context between planning, implementation and verification;
- inferring relationships that the handbook and repository already know.

This wastes tokens, I/O, inference and engineering time. It also makes equivalent tasks more dependent on the behavior of a specific coding model.

The target is not better search. The target is to make search through the handbook uncommon during normal coding work by compiling stable knowledge and repository orientation ahead of time.

## Desired outcome

Create an agent-neutral engineering context pipeline that moves repeatable reasoning to a cold path and leaves the hot path focused on novelty.

For a normal non-trivial task, Codex, Claude or another compatible coding agent should be able to obtain a compact, traceable context package containing:

1. a multidimensional task descriptor;
2. a precomputed repository route;
3. the minimum sufficient handbook knowledge;
4. planning decisions and invariants that must be resolved;
5. the verification evidence expected for the identified risks.

The system should avoid full handbook reads, broad repository rediscovery, embeddings, remote services and secondary model calls in the common case.

## Design principles

1. **Research broadly once; retrieve narrowly many times.**
2. **Never spend inference where hashes, metadata or deterministic computation can answer the question.**
3. **Compile knowledge for the decision being made, not for the document it came from.**
4. **Precompute orientation; reserve inference for novelty.**
5. **Structural evidence outranks natural-language guesses.**
6. **Minimum sufficient context beats maximum relevant context.**
7. **Generated artifacts are transparent, deterministic and inspectable.**
8. **Generated artifacts never become a second source of truth.**
9. **The protocol is model-neutral. Handbook authority must not depend on Codex-, Claude- or provider-specific reasoning.**
10. **Optimize total engineering cost, not context-token count in isolation.** A slightly larger capsule is preferable when it prevents replanning or rework.

## Scope

This design covers:

- an incremental Handbook Compiler;
- an incremental Repo Intelligence Compiler;
- a Task Descriptor Builder;
- deterministic routing and applicability;
- normalized knowledge units;
- minimum-cover context selection;
- planning, implementation and verification capsules;
- a Planning IR used as structured state behind specs/plans;
- deterministic plan validation;
- conformance derived from the same evidence model;
- cache/version/provenance rules;
- a small agent-facing entry point;
- efficiency and quality telemetry.

## Non-scope

The first implementation will not require:

- a vector database;
- embeddings over the handbook or source tree;
- a graph database;
- a long-running daemon;
- a remote context service;
- a second LLM/API call for classification;
- exhaustive AST indexing;
- indexing every private symbol;
- generation of every possible task capsule in advance;
- framework-specific intelligence for every ecosystem;
- replacing repo-local `AGENTS.md`, ADRs or canonical handbook Markdown;
- forcing every existing repository to adopt the pipeline immediately.

These may be evaluated later only if measured gaps justify them.

## High-level architecture

```text
                    COLD PATH

          AUTHORITATIVE HANDBOOK SOURCE
                     │
                     ▼
             Handbook Compiler
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 routing index  normalized units  compiled DAG
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              versioned compiled
                handbook state

Consumer repo ─► Repo Intelligence Compiler
                     │
                     ▼
             repo atlas / routes /
          capabilities / commands /
              verification map

══════════════════════════════════════════════════
                     HOT PATH

Task + repo facts + optional changed scope
                     │
                     ▼
            Task Descriptor Builder
                     │
             uncertainty only
                     │
                     ▼
          constrained agent completion
             (no second LLM call)
                     │
                     ▼
            Minimal Context Solver
                     │
                     ▼
               Context Capsule
                     │
                     ▼
                 Planning IR
                     │
             deterministic validate
               ┌─────┴─────┐
               ▼           ▼
              Spec        Plan
                            │
                            ▼
                Implementation Capsule
                            │
                            ▼
                    implementation
                            │
                            ▼
                  Verification Capsule
                            │
                            ▼
                        Evidence
```

## Authority model

The existing distinction remains strict:

```text
AUTHORITATIVE SOURCE
handbook Markdown + repo-local canonical docs/decisions
        ↓
GENERATED / COMPILED ARTIFACTS
deterministic derived representations
        ↓
RUNTIME CONTEXT
only material selected for the current task
```

Rules:

- authoritative Markdown/registries and repo-local decisions remain the source of truth;
- compiled artifacts are generated and must not be manually edited;
- runtime capsules are derived and normally ephemeral;
- a generated file must carry enough provenance to reconstruct its authoritative inputs;
- compiled content may optimize or normalize representation but may not strengthen normative force;
- if compiled state conflicts with authoritative source, authoritative source wins and the compiled state is invalid.

## 1. Handbook Compiler

### Purpose

Convert governed handbook knowledge into compact representations optimized for routing, planning, implementation and verification.

The compiler should not create generic summaries of pages. It should extract or assemble normalized semantic units.

### Normalized knowledge unit types

Initial unit taxonomy:

- `constraint` — behavior that must/should be preserved according to authoritative force;
- `decision-question` — question a plan/spec must resolve when applicable;
- `risk` — named failure class or engineering concern;
- `pattern` — reusable implementation/architecture guidance;
- `anti-pattern` — approach that should not be taken in the applicable context;
- `verification` — evidence that can prove a risk or invariant;
- `escalation` — condition requiring a more detailed artifact or human/agent judgment;
- `route-hint` — link between a semantic need and additional context.

Example:

```json
{
  "id": "authz-authoritative-boundary",
  "type": "constraint",
  "text": "Enforce authorization at an authoritative server/data boundary.",
  "covers": ["authorization", "privilege", "tenant-isolation"],
  "force": "must",
  "sources": ["std-security-identity-baseline"],
  "estimated_tokens": 18
}
```

The exact text/force must be traceable to canonical handbook authority.

### Compiled views

The compiler should produce different views for different consumers instead of one universal compiled page:

```text
machine-readable/compiled/
├── manifest.json
├── graph.json
├── routing/
├── planning/
├── implementation/
└── verification/
```

A planner usually needs decision questions, invariants and risks. An implementer needs settled constraints, implementation boundaries and anti-patterns. A verifier needs evidence requirements and negative cases.

### Determinism

Given identical:

- authoritative content;
- compiler version/schema;
- dependency inputs;

the generated semantic content must be equivalent. Non-semantic volatile fields such as generation timestamps must not participate in output hashes.

### Content addressing and incremental compilation

Each compiled node should record fields equivalent to:

```json
{
  "source_hash": "sha256:...",
  "dependency_hash": "sha256:...",
  "compiler_schema": "1",
  "output_hash": "sha256:..."
}
```

If source hash, dependency hash and compiler schema are unchanged, compilation for that node is skipped.

Changes propagate through the dependency DAG only to affected descendants. A one-document edit must not force an unconditional whole-handbook rebuild.

### Versioning

Compiled handbook artifacts are versioned in Git because they are:

- cheap to store;
- immediately consumable by coding agents;
- reviewable in PR diffs;
- verifiable by CI using source → compile → zero-diff.

Generated status must be obvious. Manual edits are invalid.

## 2. Applicability metadata and routing

The current `applies_to` model is not sufficient for low-cost runtime routing. The compiled model should represent orthogonal dimensions.

Initial dimensions:

```yaml
intent:
  - create
  - modify
  - remove
  - investigate
  - release

surface:
  - frontend
  - backend
  - database
  - infrastructure
  - ci
  - documentation

operation:
  - read
  - mutation
  - migration
  - authentication
  - authorization
  - integration
  - deployment

risk:
  - tenant-isolation
  - privilege
  - credential
  - data-loss
  - compatibility
  - availability
  - accessibility
  - performance

capability:
  - auth
  - persistence
  - billing
  - ai
  - pwa
  - notifications
```

The taxonomy should remain small and evidence-driven. New dimensions/tags are added only when they materially improve routing.

### Predicates rather than phrase matching

Compiled handbook units/artifacts should use applicability predicates, for example:

```yaml
activate_when:
  any:
    - risk: privilege
    - risk: tenant-isolation
    - operation: authorization
    - capability: auth
```

Natural-language keywords may contribute weak evidence but must not be the authority model.

### Inverted indexes

The compiler should create inverted indexes such as:

```text
risk:tenant-isolation → [unit-a, unit-b]
operation:authorization → [unit-a, unit-c]
capability:pwa → [unit-x]
```

It must not precompute every combination such as `security+tenant+token`; combination indexes grow combinatorially and make maintenance less predictable.

## 3. Repo Intelligence Compiler

### Purpose

Precompute stable repository orientation so an agent can spend reasoning on the new task rather than rediscovering topology.

### Derived repo intelligence

A participating repository may expose generated artifacts conceptually equivalent to:

```text
.engineering/compiled/
├── manifest.json
├── repo.json
├── topology.json
├── capabilities.json
├── boundaries.json
├── commands.json
├── verification.json
├── routes.json
└── landmarks.json
```

The exact file split is an implementation detail; the logical contracts are required.

### Detected facts vs declared decisions

The compiler must distinguish:

**Detected fact**

- package manager;
- framework indicators;
- presence of migrations;
- CI workflows;
- test layers;
- PWA artifacts;
- known route/service/schema locations.

**Declared decision**

- authoritative persistence owner;
- domain authority;
- intentional offline limitation;
- architectural boundary;
- product-specific source of truth;
- permitted exception.

Detected facts may be regenerated. Declared decisions come from canonical repo-local sources such as `AGENTS.md`, ADRs or explicit engineering config and outrank derived guesses.

### Incremental profiling

Repo profiling should be segmented by its input set.

Examples:

```text
runtime/dependencies ← package manifests + lockfiles
ci/delivery          ← workflow/deployment config
persistence          ← migrations/schema config
pwa                  ← manifest/service-worker config
verification         ← scripts/workflows/test config
```

Changing an unrelated component file must not trigger rediscovery of package manager, deployment topology or migration mechanism.

### Stable landmarks, not exhaustive indexing

The compiler may derive high-value landmarks such as:

- public/exported service entrypoints;
- route handlers;
- server actions/mutations;
- repositories/data-access boundaries;
- schemas/migrations;
- test suites;
- central configuration entrypoints.

It should not build an exhaustive source-code search replacement or index every private function.

### Capability map

Example:

```json
{
  "capability": "quotes",
  "entrypoints": ["src/app/quotes", "src/server/quotes"],
  "persistence": ["supabase/migrations"],
  "tests": ["tests/quotes"],
  "depends_on": ["customers"],
  "boundaries": ["authenticated-server"]
}
```

This is navigation metadata, not a new architectural source of truth.

### Work routes / change archetypes

The repo compiler and handbook compiler together should support reusable change archetypes such as:

- `add-crud-capability`;
- `modify-domain-state`;
- `authenticated-mutation`;
- `external-integration`;
- `schema-change`;
- `background-job`;
- `ui-flow-change`;
- `visual-regression-fix`;
- `pwa-capability-change`;
- `production-release`.

An archetype describes likely inspection boundaries, required questions and evidence, not a rigid implementation recipe.

Example:

```yaml
authenticated-mutation:
  inspect:
    - domain-owner
    - server-mutation
    - authorization-boundary
    - persistence-owner
    - nearest-integration-tests
  require:
    - actor
    - resource
    - permission-boundary
    - state-transition
  verify:
    - allowed-case
    - denied-case
    - cross-tenant-case-if-applicable
```

### Command registry

Repo intelligence should expose verified commands and targeted verification routes when they can be derived or declared:

```json
{
  "commands": {
    "install": "pnpm install --frozen-lockfile",
    "lint": "pnpm lint",
    "typecheck": "pnpm typecheck",
    "unit": "pnpm test",
    "e2e": "pnpm test:e2e",
    "build": "pnpm build"
  }
}
```

Commands must never be invented. Unknown remains unknown.

### Versioning of repo intelligence

Stable, compact repo intelligence may be versioned in participating consumer repositories when doing so reduces repeated agent work and CI can verify freshness deterministically.

Task-specific capsules, transient scan outputs and large caches must not be committed.

Adoption is initially opt-in and proportional; repositories without compiled intelligence must remain usable through graceful fallback.

## 4. Task Descriptor Builder

### Purpose

Represent the task as structured facts rather than one broad label such as `security` or `frontend`.

Example:

```json
{
  "intent": ["modify"],
  "surfaces": ["backend"],
  "operations": ["mutation"],
  "capabilities": ["auth", "persistence"],
  "risks": ["authorization", "tenant-isolation"],
  "state": {
    "durable_change": true,
    "migration": false
  },
  "boundaries": {
    "external": false,
    "privileged": true
  },
  "delivery": {
    "production_effect": true
  }
}
```

### Evidence precedence

Descriptor evidence follows this order:

```text
explicit structured task fact
    >
repo-local declared decision
    >
repository structural evidence
    >
actual diff/change evidence
    >
deterministic textual signal
    >
agent semantic judgment
```

Actual changed scope can add risk even when the original task description omitted it. Natural-language claims must not suppress structural evidence.

Example: a task described as visual-only that modifies an authorization policy must be treated as a security-sensitive change as well.

### Two-stage enrichment

Pre-change planning and post-change verification have different evidence.

**Intent descriptor** — before implementation:

- task statement;
- repo profile;
- declared constraints;
- likely change route.

**Change descriptor** — after implementation/diff exists:

- actual changed files;
- changed boundaries;
- migration/config changes;
- newly exposed risks.

Verification uses the enriched change descriptor so implementation cannot silently broaden scope without broadening evidence requirements.

### No secondary LLM call

The deterministic builder may emit unresolved fields:

```json
{
  "uncertain": [
    {
      "field": "risks",
      "question": "Does this invitation act as a bearer credential?",
      "allowed": ["credential", "not-credential", "unknown"]
    }
  ]
}
```

The already-active coding agent may resolve only these constrained fields using the task/repo context it already has. The tooling itself does not invoke another LLM, provider or API.

The agent may answer `unknown`; uncertainty must not be converted into false certainty.

### Agent judgment cannot select authority directly

The agent may classify meaning into the closed taxonomy. It must not return arbitrary handbook documents as authority. Deterministic routing converts descriptor tags into applicable units/artifacts.

## 5. Minimal Context Solver

### Goal

Select the smallest sufficient set of normalized units that covers identified risks and required decisions while respecting normative precedence and context budgets.

The solver optimizes coverage, not document count.

Conceptual objective:

```text
maximize required-risk/decision coverage
─────────────────────────────────────────
token cost + redundancy + unnecessary scope
```

For the current handbook scale, a deterministic greedy weighted-set-cover strategy is sufficient. No probabilistic retrieval is required.

### Selection order

1. mandatory invariants/constraints;
2. mandatory decision questions;
3. minimum risk coverage;
4. required verification evidence;
5. optional patterns only while useful budget remains;
6. escalation references rather than full documents when detail is not yet necessary.

### Negative routing

The solver must explicitly support exclusion and non-applicability. Knowing what not to load is a first-class optimization.

Example:

```json
{
  "exclude": ["pwa", "visual-evidence", "performance-budget"]
}
```

Exclusion cannot override a higher-authority structural risk discovered from the repo/diff.

### Deduplication

Equivalent normalized constraints from multiple authoritative artifacts should appear once in a capsule with multiple provenance references.

```json
{
  "id": "authz-authoritative-boundary",
  "sources": [
    "std-security-identity-baseline",
    "pb-security-review"
  ]
}
```

### Context budgets

Budgets are defaults, not semantic hard limits:

```yaml
routing_target_tokens: 200
repo_route_target_tokens: 250
planning_capsule:
  target: 600
  soft_max: 900
  hard_max: 1400
  unresolved_risk_reserve: 250
verification_capsule_target_tokens: 600
```

The implementation must measure actual serialized token estimates consistently enough for comparative routing. Exact tokenizer parity across models is not required for v1.

If required authority cannot fit within the normal budget, correctness wins and the capsule records the escalation.

## 6. Context Capsules

Capsules are task-specific, derived and normally ephemeral.

### Planning capsule

Contains only what the planner needs, for example:

```text
Task type: authenticated tenant mutation

Repo route:
- existing invitation/domain service
- authorization boundary
- invitation persistence
- nearest integration tests

Applicable authority:
- pol-truthful-engineering
- std-security-identity-baseline
- std-architecture-data-integrity-baseline

Required decisions:
1. authoritative invitation state owner;
2. tenant authorization boundary;
3. token storage/transport semantics;
4. expiration/revocation behavior;
5. retry/idempotency semantics.

Constraints:
- UI state is not authorization.
- privileged credentials stay server-side.
- revocation claims require authoritative durable state.

Required evidence:
- allowed actor;
- denied role;
- foreign tenant denied;
- expired/revoked credential denied;
- retry/replay behavior defined.

Escalate:
- load token-handling detail only if credential design changes.
```

### Implementation capsule

Derived from the approved Planning IR. It should emphasize:

- objective and scope;
- files/boundaries likely affected;
- settled decisions;
- invariants;
- forbidden approaches;
- implementation sequence/dependencies where useful;
- required local commands/gates;
- unresolved assumptions.

It should not repeat the complete design discussion.

### Verification capsule

Derived from the enriched change descriptor + Planning IR + applicable evidence units.

It classifies evidence as:

- required;
- conditional;
- not applicable;
- unable to run/unknown.

It must preserve the handbook rule that `not run` is not `passed`.

### Capsule cache key

A capsule may be cached using stable inputs equivalent to:

```text
handbook-compiled-hash
+ repo-profile-hash
+ task-descriptor-hash
+ relevant Planning IR hash
+ capsule-schema-version
```

Cache misses generate a capsule cheaply; cache hits reuse it. The system must not pre-generate the combinatorial space of possible tasks.

## 7. Planning IR

### Purpose

Use one structured planning state as the basis for human-readable specs, implementation plans and reviews instead of repeatedly regenerating overlapping prose.

Example schema shape:

```yaml
schema: planning-ir/v1

task:
  objective: ...
  includes: [...]
  excludes: [...]

affected:
  capabilities: [...]
  boundaries: [...]

decisions:
  - id: invitation-source
    status: settled
    choice: invitations-table
    rationale: durable-revocation
    provenance:
      type: repo-decision
      ref: ...

invariants:
  - invitation-belongs-to-tenant
  - accepted-or-revoked-token-cannot-be-replayed

state_transitions:
  - from: issued
    to: accepted
  - from: issued
    to: revoked

risks:
  - id: tenant-isolation
    mitigation: authoritative-server-authorization

implementation:
  units: [...]

verification:
  required:
    - risk: tenant-isolation
      evidence: integration-test

unresolved: []
```

### Provenance

Important decisions distinguish origins such as:

- task requirement;
- handbook authority;
- repo-local decision;
- repository evidence;
- implementation discovery;
- explicit agent judgment.

A decision inherited from the handbook must preserve artifact ID. A business requirement must not be misrepresented as handbook authority.

### Views

Human-readable outputs are projections of the IR:

```text
Planning IR
   ├─ specification view
   ├─ implementation-plan view
   └─ review/verification view
```

The Markdown views should include only relevant sections. Empty universal-template sections are omitted rather than filled ceremonially.

### Delta planning

A requirement change should be able to invalidate affected IR nodes without conceptually rebuilding every unrelated decision.

For v1, this may be implemented conservatively using hashes/dependency declarations rather than sophisticated semantic incremental planning.

## 8. Deterministic plan validation

Before implementation, the pipeline validates structural completeness against the task descriptor and selected planning contracts.

Examples:

```text
tenant-isolation risk + no authorization decision
→ invalid/incomplete plan

migration=true + no migration verification
→ incomplete plan

credential risk + no lifecycle semantics
→ incomplete plan

external integration + no failure/retry semantics
→ incomplete plan when applicable
```

Validation checks presence/relationships, not whether an architectural choice is intrinsically good. Semantic quality remains a review responsibility.

## 9. Conformance derived from the same model

Do not build a separate compliance scanner with parallel semantics.

Conformance can be derived as:

```text
applicable requirements
-
demonstrated evidence
-
explicit legitimate exception
=
gaps / unknowns
```

Inputs already exist in:

- repo profile;
- task/change descriptor;
- handbook compiled requirements;
- Planning IR;
- verification evidence.

This allows conformance reporting without repeating classification/retrieval logic.

## 10. Agent-facing interface

The preferred long-term interface is one small entry point rather than multiple unrelated commands.

Conceptually:

```bash
engineering context --mode plan --task "Add tenant invitations with expiration"
engineering context --mode implement --spec <planning-ir-or-spec>
engineering context --mode verify --change <ref-or-working-tree>
```

The implementation may expose subcommands internally, but the agent-facing contract should remain simple.

### Expected plan-mode result

The output should make these objects available without broad discovery:

- task descriptor;
- unresolved descriptor fields, if any;
- repo route;
- applicable authority IDs;
- context capsule;
- planning contract;
- verification contract;
- provenance/compiled revision.

### Global agent instructions

Once this pipeline is mature, global agent instructions can become smaller. A future version may reduce normal handbook usage to a protocol such as:

1. read repo-local instructions;
2. obtain engineering context for non-trivial work;
3. follow supplied repo routes and constraints;
4. escalate only when the capsule/evidence indicates ambiguity or conflict;
5. verify using the supplied evidence contract;
6. do not bulk-read the handbook.

This design must not prematurely remove the existing router until the replacement is validated.

## 11. Graceful degradation

The system must remain useful when preprocessing is absent or stale.

Fallback order:

```text
valid compiled handbook + valid repo intelligence
→ full optimized path

valid compiled handbook + missing repo intelligence
→ lazy/minimal repo profiling for requested route

missing/stale compiled handbook
→ current generic handbook router / canonical source

unresolved semantic novelty
→ constrained judgment by active coding agent

conflict with authority
→ canonical source + explicit escalation
```

A cache or compiler failure must not cause fabricated certainty or silently suppress handbook authority.

## 12. Data integrity and stale-state behavior

Every generated root should expose:

- schema version;
- authoritative input hashes;
- dependency hashes;
- output hash;
- compiler version;
- provenance references.

The runtime should be able to detect stale generated state before trusting it.

If stale state cannot be refreshed, output must identify that limitation rather than presenting stale context as current.

## 13. Portability and implementation constraints

The core compiler/context tooling should be portable and low-dependency.

Preferred initial properties:

- Python or another already-available portable runtime with minimal dependencies;
- real YAML/JSON parsing rather than regex pretending to be a general parser;
- deterministic filesystem/Git inspection;
- no required cloud service;
- no required PowerShell runtime for core integrity/context operations;
- explicit schemas/versioning for machine-readable contracts.

The existing PowerShell integrity checker is not considered passed unless actually executed; a future portable checker may supersede it only through an explicit migration.

## 14. Performance model

The design separates cold-path work from hot-path work.

### Cold path

Runs when authoritative knowledge or relevant repo structure changes:

- parse changed inputs;
- update affected semantic units;
- update affected DAG nodes;
- update affected repo-profile segments;
- recompute hashes/indexes only where invalidated.

### Hot path

Normal task behavior should approximate:

```text
read small manifests
→ obtain/reuse repo profile
→ build task descriptor
→ direct inverted-index lookup
→ solve minimal context
→ emit capsule
```

No full handbook parse, embeddings or exhaustive repo scan should be needed in the normal case.

## 15. Efficiency telemetry

The pipeline should be measurable before optimization claims become standards.

Useful metrics:

- deterministic descriptor hit rate;
- unresolved-field rate;
- average/p50/p95 capsule estimated tokens;
- full canonical-document escalation rate;
- unused retrieved-unit rate;
- missing-context/replan rate;
- plan-validator failure rate;
- compiled cache hit rate;
- repo-profile segment cache hit rate;
- incremental compiler no-op rate.

Initial hypotheses, not normative thresholds:

```text
deterministic classification > 90%
semantic unresolved/fallback < 10%
full canonical reads uncommon in normal tasks
unused capsule context approaches zero
```

Measurements should challenge these hypotheses before hard thresholds are adopted.

## 16. Evaluation across coding agents

The protocol should permit the same prepared engineering context to be supplied to Codex and Claude without changing handbook authority.

Comparisons should focus on structured outcomes rather than prose style:

- scope completeness;
- unresolved assumptions;
- invariant coverage;
- risk coverage;
- missing decisions;
- verification coverage;
- unsupported assumptions;
- implementation complexity/rework;
- total context consumed where measurable.

The purpose is not to force agents to produce identical plans. It is to ensure they start with equivalent authoritative context and that differences reflect reasoning about the novel task rather than different handbook retrieval behavior.

## 17. Security and privacy

Compiled repo intelligence must not capture secret values.

It may record facts such as:

- a secret/config name exists;
- a boundary uses privileged credentials;
- a workflow consumes environment-scoped secrets.

It must not persist secret contents, raw credentials, sensitive runtime payloads or unrestricted application data.

Task/runtime capsules follow the same rule unless the user explicitly provides sensitive material required for the current operation and the environment permits it.

## 18. Failure handling

Expected failure states include:

- malformed canonical metadata;
- dependency-cycle or invalid graph;
- stale compiled output;
- unsupported repo structure;
- contradictory repo decisions;
- insufficient descriptor evidence;
- context budget exceeded by mandatory authority;
- missing command/evidence mapping.

The system should fail with structured diagnostics and a safe escalation path. It must not silently drop mandatory knowledge merely to remain within a token budget.

## 19. Compatibility and adoption

Adoption is staged.

The existing canonical handbook, catalog, source registry, global instructions and generic `engineering-handbook` skill remain valid during transition.

Initial implementation should prove the pipeline against the handbook itself and one or more representative consumer repositories before making it the default routing path.

A consumer repo should be able to adopt preprocessing without copying handbook authority into repo-local files.

## Acceptance criteria

The design is successfully implemented when all of the following are observable:

- [ ] Handbook compiled outputs are deterministic, generated, inspectable and versioned.
- [ ] Unchanged handbook nodes are skipped using source/dependency/schema hashes.
- [ ] Routing uses structured applicability and inverted indexes rather than combinatorial task keys.
- [ ] Repo intelligence distinguishes generated facts from declared authoritative decisions.
- [ ] Repo profiling can invalidate/recompute independent segments rather than rescanning everything unconditionally.
- [ ] Normal task routing produces a multidimensional descriptor instead of only a broad domain label.
- [ ] Unresolved classification produces a constrained taxonomy question and does not invoke a second LLM/API.
- [ ] Structural repo/diff evidence can add risk that the task prose omitted.
- [ ] The context solver selects normalized units and deduplicates equivalent guidance.
- [ ] Context selection supports explicit non-applicability/negative routing.
- [ ] Planning, implementation and verification receive purpose-specific capsules.
- [ ] The Planning IR preserves scope, decisions, invariants, risks, verification and provenance.
- [ ] Plans can be structurally rejected as incomplete before implementation for defined missing-risk relationships.
- [ ] Verification enriches the task descriptor using the actual changed scope.
- [ ] Conformance is derived from the same applicability/evidence model rather than a parallel rule engine.
- [ ] A repo without generated intelligence still works through a documented graceful fallback.
- [ ] No secret values are written to generated repo intelligence.
- [ ] The optimized path does not require embeddings, a vector DB, remote context service or mandatory secondary model call.
- [ ] The system emits metrics sufficient to evaluate whether token/I/O/inference savings are real.
- [ ] Codex and Claude can consume the same model-neutral context contracts.

## Verification strategy for the implementation

The future implementation plan should include evidence for:

- deterministic recompilation: same inputs produce equivalent outputs;
- incremental behavior: unrelated input changes do not invalidate unrelated compiled segments;
- stale-state detection;
- routing correctness on representative task fixtures;
- negative-routing correctness;
- descriptor precedence when task prose conflicts with structural evidence;
- minimum-context selection and deduplication;
- budget/escalation behavior;
- Planning IR schema validation;
- plan-completeness validation;
- no-secret fixtures for repo intelligence;
- graceful fallback with no compiled repo profile;
- agent-neutral fixture outputs independent of Codex/Claude-specific configuration;
- comparison against the current handbook router for context size and missed guidance.

## Risks and mitigations

### Over-engineering the compiler

Risk: building a knowledge platform more complex than the handbook warrants.

Mitigation: v1 uses files, hashes, small schemas, deterministic indexes and simple algorithms. No graph database, embeddings or remote service.

### Metadata becoming a second handbook

Risk: authors duplicate rules into routing metadata.

Mitigation: semantic units remain traceable to canonical artifacts; generated representations are derived and not manually authoritative.

### Stale generated repo intelligence

Risk: agents trust an outdated route.

Mitigation: input hashes, segment invalidation, freshness checks and fallback to repo discovery when stale.

### Excessive taxonomy

Risk: hundreds of tags recreate the complexity being removed.

Mitigation: taxonomy grows only from demonstrated routing need; broad tags alone do not justify new dimensions.

### Context minimization removes critical nuance

Risk: a tiny capsule causes bad engineering decisions.

Mitigation: mandatory authority outranks budgets; unresolved conditions preserve escalation links; total rework cost is part of optimization.

### Model dependence leaks into routing

Risk: Codex and Claude select different handbook authority.

Mitigation: agents may resolve constrained semantic fields but deterministic tooling maps the resulting descriptor to authoritative context.

## Durable decisions proposed by this design

Subject to implementation validation, the following are intended to become durable architecture decisions:

1. Handbook knowledge is compiled ahead of time into transparent generated representations.
2. Versioned compiled handbook artifacts are permitted because CI can prove source/compiled synchronization.
3. Runtime task capsules remain ephemeral.
4. Repository orientation is preprocessed incrementally where adoption provides measurable value.
5. Routing is multidimensional and deterministic-first.
6. The active coding agent, not a secondary model service, resolves residual semantic ambiguity through a constrained schema.
7. Planning IR is the structured state behind specs/plans/reviews.
8. Conformance derives from the same applicability and evidence model.
9. The system remains agent-neutral and does not encode handbook authority in model-specific prompts.

These decisions should be promoted to ADRs only when the implementation plan identifies the stable boundaries and the first implementation validates them.

## Existing solutions / reuse check

- Current handbook: reuse the existing canonical taxonomy, catalog, generic router, source authority model, knowledge promotion, truthful engineering, verification semantics and repo-local `AGENTS.md` model.
- Existing machine-readable assets: evolve rather than replace `machine-readable/catalog.yaml` and source registries where they remain canonical.
- Existing task-spec template: retain as a human view; Planning IR should eventually render task-specific views rather than require every empty section.
- External infrastructure: not required for v1 because current scale can be handled deterministically with local files/indexes.

## Open implementation questions intentionally deferred to the implementation plan

These do not change the approved architecture and should be resolved by repository evidence during planning:

- exact Python package/module layout;
- exact JSON Schema versus equivalent validation mechanism;
- exact generated file split where one file is cheaper than several;
- tokenizer/estimator used for approximate context cost;
- whether consumer-repo compiled intelligence is committed by default or only for selected repos after measurement;
- exact first representative consumer repository/fixtures;
- migration path from the PowerShell integrity checker;
- exact integration surface with the existing generic handbook skill.

The implementation plan should choose the smallest design that satisfies the acceptance criteria and preserve a migration path rather than implement speculative extensibility.
