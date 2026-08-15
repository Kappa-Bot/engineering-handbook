---
id: gov-knowledge-promotion
kind: governance
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Knowledge Promotion

## Principle

Not every useful finding belongs in the handbook. The handbook contains deliberately promoted knowledge that has proven generalizable value.

## Promotion pipeline

```text
Problem or question
  -> Research / source
  -> Evaluation + evidence
  -> Reference
  -> Internally validated learning
  -> Generalizable?
       no  -> keep repo-local
       yes -> Pattern or Playbook
                -> Mandatory?
                     no  -> remain Pattern / Playbook
                     yes -> Standard or Policy
                              -> Enforceable with value?
                                   yes -> Rule / Hook / Script / CI / Ruleset / Gate
```

## Promotion criteria

Before promotion, determine:

- whether the problem recurs across repositories or is inherently local;
- whether a reusable solution already exists internally;
- whether a mature external solution is stronger than a new internal design;
- evidence that the guidance works in our environment;
- compatibility, maintenance, security, performance, accessibility, licensing, complexity, lock-in, and architectural fit where relevant;
- whether the artifact is descriptive, recommended, mandatory, or executable.

## Promotion rules

- Project learning MUST stay repo-local unless it is demonstrably generalizable.
- A source or research note MUST NOT jump directly into a mandatory Policy without internal evaluation and a clear applicability decision.
- A stable mandatory rule SHOULD become technically enforced when enforcement materially reduces drift, errors, or repeated work.
- Automation MUST NOT be added merely because a rule can be automated; the enforcement benefit must justify its complexity.
- Promotion SHOULD reduce duplicated reasoning, not create duplicated documentation.

## Demotion and retirement

When a promoted artifact no longer applies, use the document lifecycle rather than silently abandoning it. Repo-specific descendants may remain valid if their local context still supports them.
