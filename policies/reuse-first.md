---
id: pol-reuse-first
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Reuse First

## Rule

Before designing a new engineering solution, search for a suitable existing one. New design is the last step, not the first reflex.

## Search order

1. The current repository.
2. The Engineering Handbook.
3. Other internal repositories where reuse is permitted and relevant.
4. Internal patterns, templates, skills, playbooks, or platform capabilities.
5. External solutions.
6. Only then, design a new solution.

## External search priority

When external research is justified, prefer in this order:

1. official standards, specifications, and primary vendor/framework documentation;
2. original implementations and mature reference projects;
3. established design systems and high-quality engineering handbooks;
4. community material requiring validation.

Use `governance/source-authority.md` to classify evidence.

## Evaluation

Do not adopt a solution because it merely exists. Evaluate relevant tradeoffs including:

- functional fit;
- maintenance and maturity;
- security;
- performance;
- accessibility;
- license and redistribution constraints;
- implementation and operational complexity;
- vendor or architectural lock-in;
- compatibility with the current architecture;
- cost of owning a custom alternative.

## Outcome

If an existing solution is adequate, prefer reuse or adaptation. If a new solution is necessary, document why existing alternatives did not fit when that reasoning will matter to future maintainers.
