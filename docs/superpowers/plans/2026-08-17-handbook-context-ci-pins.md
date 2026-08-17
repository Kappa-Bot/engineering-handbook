# Handbook Context CI Immutable Pins

This companion resolves the execution-time action pins referenced by Task 14 of `2026-08-17-handbook-compiler-agent-context-pipeline.md`.

Use these immutable full commit SHAs in `.github/workflows/handbook-context.yml`:

```yaml
- uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
- uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
```

They were resolved from the official Git refs `refs/tags/v4` and `refs/tags/v5` on 2026-08-17. Before implementation, re-check the official tag refs; if either floating major tag has moved, use the then-current full SHA and record the change in the implementation commit/PR evidence. The workflow itself must never commit a floating action tag.
