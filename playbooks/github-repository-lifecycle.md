---
id: pb-github-repository-lifecycle
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - github-repositories
sources:
  - src-github-pull-request-merges
  - src-github-auto-delete-branches
  - src-github-rulesets
  - src-github-archive-repositories
last_verified: 2026-08-15
review_due: 2027-02-15
---

# GitHub Repository Lifecycle

## Purpose

Configure and operate a GitHub repository proportionally from active development through retirement without turning every repository into a copy of a large-enterprise governance model.

This playbook describes **when** GitHub controls add value. It is not a universal Policy requiring the same merge settings, rulesets, reviewers, checks, or automation in every repository.

Use it with:

- `pb-new-repository-bootstrap` when creating a new repository;
- `pol-workspace-git-hygiene` for local branch/workspace behavior;
- `pb-engineering-change` for PR and verification flow;
- repo-local decisions when settings materially affect collaboration or delivery.

## Principle: enforce demonstrated needs

GitHub settings SHOULD reduce a concrete failure mode, not merely make the repository look mature.

Examples of real reasons to add enforcement:

- accidental direct or force pushes to a critical branch;
- multiple contributors need a consistent review path;
- a reliable CI check must pass before merge;
- release/deployment requirements must be respected;
- branch/tag deletion or naming needs protection;
- auditability requires visible repository rules.

Examples that are not sufficient by themselves:

- another company uses the setting;
- GitHub exposes the option;
- a generated template enabled it;
- “production repository” without a specific risk or gate.

## 1. Establish repository metadata and ownership

At repository creation or adoption, make deliberate choices about:

- repository owner/account or organization;
- name and description;
- visibility;
- default branch;
- license when distribution requires one;
- successor/related repository links where ownership could be confused.

These settings should match the repository's actual business/engineering role. Do not publish a private business repository or add an open-source license accidentally through a generic scaffold.

## 2. Configure merge methods deliberately

GitHub can allow or disable merge commits, squash merges, and rebase merges per repository.

For the current short-lived task-branch operating model, **squash merge is the preferred default when intermediate branch commits are iteration noise**. It gives the base branch one coherent change commit while preserving the PR discussion/history in GitHub.

This is not a mandate to squash meaningful history. A repository MAY allow another merge method when it has a concrete reason, for example:

- meaningful multi-commit history should survive intact;
- a release/integration workflow depends on merge commits;
- rebase merge is intentionally used to preserve individual commits while maintaining linear history.

Avoid enabling every merge method merely because GitHub supports them if that produces inconsistent history with no benefit.

## 3. Delete merged task branches when safe

GitHub can automatically delete head branches after pull requests merge. For repositories using short-lived task branches, this SHOULD normally be enabled when repository rules and branch relationships allow it.

Automatic deletion reduces stale branch accumulation and removes manual cleanup work. GitHub rules or branch protections may prevent deletion in some cases, so failure to delete MUST NOT be “fixed” by force-moving or destroying refs.

Long-lived release/integration branches are a repository-specific design and should not be treated as disposable task branches.

## 4. Use auto-merge only when merge requirements exist

GitHub auto-merge can merge a PR after its required reviews/checks are satisfied.

It is useful when a PR is already approved but waiting on deterministic requirements. It adds little value when a repository has no meaningful merge requirements or when a human decision is still expected immediately before merge.

Do not enable auto-merge as a substitute for defining the actual required gates.

## 5. Decide whether branch/ruleset enforcement is justified

Do not create protection rules before deciding what they protect against.

A practical progression is:

### Low collaboration / low consequence

Examples: early prototype, solo experimental repository.

Possible state:

- short-lived branches and PRs by convention;
- no required ruleset yet;
- manual verification according to the repo-local contract.

This is acceptable while the cost of accidental bypass remains low.

### Solo or small-team repository with meaningful delivery risk

Consider protecting the default branch when direct/force pushes, accidental deletion, or bypass of reliable checks would create material recovery cost.

Only require status checks that actually exist, are stable, and are expected for the targeted change scope.

### Multi-contributor repository

Consider enforcing the PR path, applicable status checks, and review requirements where ownership/review genuinely reduces risk.

Do not require an approval count that the actual team cannot satisfy without ritual self-approval or blocking normal work.

### High-impact / regulated / shared platform repository

More explicit branch/tag rules, required checks, deployment gates, review ownership, or organization-level rulesets may be justified. Treat this as a separate enforcement design rather than silently inheriting settings from a low-risk repo.

## 6. Prefer understandable enforcement

GitHub rulesets can apply controls to branches/tags and multiple rulesets can apply at the same time; active rulesets are also visible to repository readers. Legacy branch protection rules remain supported, but only one branch protection rule applies at a time when multiple patterns overlap.

For new complex enforcement, prefer the mechanism that makes the resulting rules easiest to understand and maintain. Do not migrate working protection rules solely for novelty.

Availability varies by GitHub plan, repository visibility, and ruleset type. Verify current product availability before making a repository setting a mandatory operating requirement.

## 7. Required checks must represent real gates

A required status check is useful only when the underlying check is a trustworthy merge gate.

Before requiring one:

- the check exists on the target repository;
- its trigger covers the intended PR changes;
- false failures are acceptably rare;
- the team/owner knows how to diagnose it;
- the check's runtime/cost is proportionate;
- the repository can still handle exceptional recovery through an explicit bypass/exception model where appropriate.

Do not require a future CI job by name before the workflow exists and has proven stable.

## 8. Keep PR lifecycle aligned with the engineering workflow

For a normal change:

```text
short branch
  → implementation
  → applicable verification
  → PR / review when required
  → merge
  → delete merged task branch
```

PR metadata should communicate the outcome, material tradeoffs, verification actually performed, and any required gate not run.

Repository rules should reinforce this flow only where enforcement reduces meaningful drift.

## 9. Treat repository setting changes as engineering changes when material

A setting change is not “just admin” when it changes how code reaches the default branch, who can bypass controls, or how history is retained.

For material changes:

- state the problem being solved;
- identify affected contributors/automation;
- verify existing workflows will still function;
- record a repo-local decision when the setting establishes a durable operating constraint;
- roll out gradually/evaluate first when GitHub provides an appropriate non-enforcing mode and the risk warrants it.

Do not create an ADR for every checkbox toggle.

## 10. Handle dormant repositories explicitly

A repository that is not currently receiving feature work does not automatically need deletion or archival.

Clarify whether it is:

- still maintained for fixes/security updates;
- temporarily dormant;
- superseded by another repository;
- permanently retired.

Update the README/description when active ownership or successor information has materially changed.

## 11. Archive before deleting when history still matters

GitHub archive makes a repository read-only and signals that it is no longer actively maintained. GitHub recommends resolving/closing open work and updating repository information before archival.

Prefer archival over deletion when the repository still has value as:

- implementation/history evidence;
- dependency or integration reference;
- audit/business record;
- migration/successor context;
- source for future knowledge promotion.

Before archiving:

1. identify the successor or reason for retirement in README/description where useful;
2. resolve, close, or deliberately transfer open PRs/issues;
3. ensure critical release/artifact/deployment information is preserved elsewhere if archival affects operations;
4. confirm no active automation depends on writes to the repository;
5. archive through GitHub.

Archived repository data becomes read-only until the repository is unarchived.

## 12. Delete only with an explicit retention decision

Deletion is appropriate only when retention has no required engineering, business, legal, operational, or migration value and the owner consciously accepts the loss/recovery model.

Do not use deletion as routine “cleanup” for repositories that are merely old or quiet.

This playbook does not define legal/business retention periods; external obligations outrank handbook guidance.

## Review triggers

Re-evaluate GitHub lifecycle settings when:

- contributors/teams increase;
- the repository becomes production/shared/platform-critical;
- stable CI checks are introduced or removed;
- deployment/release process changes;
- ownership moves between users/organizations;
- GitHub plan/feature availability changes;
- a recurring human error suggests a rule can reduce real drift;
- a repository enters maintenance, superseded, or retirement state.

## Definition of done

GitHub repository lifecycle configuration is fit for purpose when:

- merge methods match the intended history model;
- merged task branches are cleaned up safely;
- enabled enforcement corresponds to real risks/gates;
- required checks are real and operable;
- bypass/exception behavior is understood where enforcement exists;
- dormant/retired repositories communicate their state;
- archival/deletion is deliberate and preserves required traceability;
- no GitHub control is being treated as a substitute for an undefined engineering process.
