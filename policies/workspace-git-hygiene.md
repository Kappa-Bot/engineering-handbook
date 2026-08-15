---
id: pol-workspace-git-hygiene
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources:
  - src-git-worktree
  - src-git-branch
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Workspace and Git Hygiene

## Objective

Keep repository state understandable, recoverable, and safe. Cleanup must never be more dangerous than the mess it is trying to remove.

## Default topology

- Use one normal working tree by default.
- Use a short-lived branch per task/PR when the repository workflow calls for branches.
- Git worktrees are **exceptional**, not automatic.
- A worktree MAY be used when explicitly requested or when real, unavoidable same-repository parallelism clearly justifies it.

A methodology or agent convenience is not sufficient reason to create a worktree.

## Start-of-task checks

Before material edits, establish enough state to avoid overwriting or mixing work:

- correct repository;
- expected base branch/ref;
- current working tree status;
- relevant local instructions;
- existing uncommitted/user changes that must be preserved.

Do not demand a pristine tree when legitimate user work is intentionally present; account for it explicitly instead.

## Repository artifacts

- Scratch, temporary, review, generated inspection, and disposable files SHOULD live in OS temp or another non-repo location when practical.
- Any file intentionally left in the repository MUST be a real product, source, configuration, test, documentation, or other deliberate artifact.
- Do not commit logs, ad-hoc dumps, temporary patches, screenshots, or analysis files unless the repository explicitly treats them as durable evidence.

## Cleanup safety

Agents MUST NOT:

- delete unmerged branches merely because they look old;
- delete user-authored uncommitted work;
- use indiscriminate destructive cleanup such as broad `git branch -D` loops;
- rewrite published history unless explicitly required and authorized;
- force-push merely to simplify cleanup;
- remove files whose ownership/purpose is unclear without first establishing safety.

Cleanup automation, when introduced, MUST delete only state proven safe by deterministic rules (for example, clearly merged branches).

## Branch lifecycle

- Prefer short task branches.
- After merge, stale remote task branches SHOULD be deleted when repository policy permits it.
- Local cleanup SHOULD use merge knowledge and pruning rather than guessing from branch names or age.
- Persistent branches are repository-specific and MUST NOT be invented by universal policy.

GitHub automatic remote-branch deletion may be adopted later as repository automation; Foundation v0.1 documents the desired hygiene but does not enforce it yet.

## Worktrees

When a worktree exception is used:

- record why normal single-checkout operation was insufficient;
- ensure the worktree has an intentional branch/base;
- avoid multiple agents editing overlapping files unless the coordination model explicitly handles it;
- remove the worktree only after confirming its work is safely merged/preserved.

## Handoff state

A normal handoff SHOULD leave:

- no accidental scratch/untracked artifacts;
- no unexplained temporary directories;
- no abandoned task branches created by the current work;
- all user/unmerged work preserved;
- Git state understandable to the next operator.

A dirty tree is not automatically a failed handoff when the dirt is intentional and explicitly accounted for.
