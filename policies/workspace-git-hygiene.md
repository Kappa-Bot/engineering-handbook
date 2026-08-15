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

## Working model

- Use one normal working tree by default.
- Use a short-lived branch per coherent task or pull request when branch-based work is appropriate.
- Git worktrees MUST NOT be created by default.
- A worktree MAY be used only when explicitly requested or when real, unavoidable parallelism in the same repository clearly justifies the additional workspace.

## Workspace cleanliness

- Temporary, scratch, review, generated diagnostic, and throwaway files MUST NOT be left in the repository unless they are intentional project artifacts.
- Use the operating system temporary directory for transient files when practical.
- Handoff SHOULD leave the working tree clean or clearly account for every remaining change.
- Do not leave abandoned worktrees, task branches, or generated debris after their purpose is complete.

## Safe cleanup

- Never delete or overwrite unmerged user work merely to obtain a clean state.
- Never use indiscriminate destructive branch cleanup such as broad `git branch -D` operations.
- Before deleting a branch, worktree, file, or other potentially valuable state, establish that it is merged, intentionally disposable, or explicitly approved for removal.
- Do not force a ref update or destructive history rewrite unless the task explicitly requires it and the consequences are understood.

## Branch lifecycle

Merged remote task branches SHOULD be deleted when they no longer provide value. Repository settings MAY automate deletion of merged branches when compatible with the team workflow.

## Handoff

A Git handoff MUST state material uncommitted changes, unpushed commits, unresolved conflicts, or unmerged branches that remain. Silence MUST NOT be used to imply cleanliness.
