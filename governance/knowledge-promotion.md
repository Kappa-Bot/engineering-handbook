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

Useful knowledge is not automatically handbook knowledge.

The handbook contains knowledge that has been intentionally promoted because it is reusable beyond one task or repository. Promotion is a decision, not a copy operation.

## Pipeline

```text
Problem / question
        ↓
Research / source
        ↓
Evaluation + evidence
        ↓
Reference
        ↓
Internally validated learning
        ↓
Generalizable?
   ┌────┴────┐
   no        yes
   ↓          ↓
repo-local   Pattern / Playbook
                 ↓
            Mandatory?
            ┌────┴────┐
            no        yes
            ↓          ↓
         remain     Standard / Policy
                        ↓
                 Enforceable with value?
                        ↓
          Rule / Hook / Script / CI / Ruleset / Gate
```

A source never skips the evaluation/applicability step simply because it is authoritative.

## Promotion questions

Before creating or promoting an artifact, answer:

1. Does the problem recur or plausibly recur across more than one repository?
2. Does an internal solution already exist?
3. Is the internal solution actually reusable, or tightly coupled to one product?
4. Does a mature external solution solve the problem better than a new internal design?
5. What evidence shows the guidance works in our environment?
6. Is the result descriptive, recommended, mandatory, or executable?
7. Would centralizing it reduce repeated reasoning or merely centralize noise?

## Classification

Use the narrowest useful class:

- **Reference** — research/evidence only.
- **Pattern** — reusable solution to a recurring problem.
- **Playbook** — reusable sequence for performing work.
- **Standard** — mandatory technical baseline for a defined scope.
- **Policy** — mandatory operating/governance behavior.
- **Executable asset** — automation that enforces or operationalizes stable guidance.

Do not make something a Policy merely because it is important. Choose the kind that matches the nature of the rule.

## Promotion rules

- Project learning MUST remain repo-local until it is demonstrably generalizable.
- A Reference MUST NOT be treated as normative merely because it is in the handbook.
- A Pattern or Playbook SHOULD accumulate real usage before being promoted to a mandatory Standard/Policy when practical.
- Mandatory guidance MUST define scope and, where legitimate, an exception model.
- Automation SHOULD follow a stable rule rather than precede it.
- Technical enforcement SHOULD be preferred when it materially reduces drift, error rate, repeated manual work, or misleading verification.
- Automation MUST NOT be introduced merely because automation is possible.

## Example: local learning to policy

```text
MovOps discovers repeated scratch-file pollution
        ↓
local cleanup lesson validated
        ↓
same issue observed elsewhere
        ↓
workspace hygiene pattern
        ↓
risk is universal and repeated
        ↓
workspace/git policy
        ↓
later: repo-doctor or hook, if enforcement proves worthwhile
```

## Demotion, supersession, and retirement

Promoted knowledge is not permanent by default.

When guidance stops being valid:

- update the canonical artifact if the topic remains stable;
- deprecate if migration time is needed;
- supersede if another artifact replaces it;
- retire when no longer applicable;
- preserve historical decisions when they explain the current architecture.

Do not silently abandon stale guidance.
