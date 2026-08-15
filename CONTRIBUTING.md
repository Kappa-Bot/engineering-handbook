# Contributing

Changes to the Engineering Handbook must preserve authority, traceability, and a single source of truth.

## Change flow

1. Define the engineering problem or learning.
2. Search for an existing internal solution before creating a new artifact.
3. Research external sources only where they materially improve the decision.
4. Register important external sources in `machine-readable/sources.yaml`.
5. Separate source facts from internal decisions and evaluate applicability.
6. Keep non-generalizable knowledge repo-local.
7. Promote generalizable knowledge using `governance/knowledge-promotion.md`.
8. Update the canonical document rather than creating a competing page for the same topic.
9. Update `machine-readable/catalog.yaml` and lifecycle metadata.
10. Verify the change and report only checks actually executed.

## Normative changes

A change that creates or strengthens a MUST, MUST NOT, or organization-wide SHOULD requires explicit rationale, applicable evidence, and consistency with `governance/handbook-governance.md`.

External authority does not by itself make a rule universally applicable. Source authority and internal applicability are separate decisions.

## Pull request expectations

A handbook change should state:

- the problem being solved;
- whether it is governance, policy, standard, pattern, playbook, reference, template, decision, or executable asset;
- affected repositories or scopes;
- source IDs used;
- compatibility or migration impact when applicable;
- verification performed.

Do not mix unrelated refactors or cleanup into the same change.
