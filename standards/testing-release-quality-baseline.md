---
id: std-testing-release-quality-baseline
kind: standard
status: active
owner: engineering
version: "0.11"
applies_to:
  - application-repositories
  - services
  - releaseable-products
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-github-deployment-environments
  - src-github-actions-pull-request-tested-source
  - src-github-actions-workflow-run-attempt
  - src-github-actions-workflow-attempt-jobs
  - src-playwright-test-retry-outcomes
  - src-microsoft-process-waitforexit
  - src-microsoft-robocopy-exit-codes
  - src-gnu-bash-pipeline-status
  - src-python-312-package-resources
  - src-postgresql-16-concurrent-indexes
  - src-postgresql-16-index-progress
last_verified: 2026-11-22
review_due: 2027-03-03
---

# Testing and Release Quality Baseline

## Purpose

Define the minimum evidence discipline for code changes, CI and releases without prescribing one test framework, one CI provider or one universal pipeline.

The objective is to match evidence to risk, keep build/test/deployment claims distinct, and prevent verification machinery from becoming a disproportionate operational cost.

## 1. Test the failure class, not the tool

Use the cheapest layer that can reliably catch the relevant defect.

Typical layers:

- pure/domain/unit tests for deterministic logic and invariants;
- component/module tests for local integration and interaction;
- database/policy tests for schema, constraints, authorization and migrations;
- integration tests for boundary contracts;
- end-to-end tests for critical user/business journeys;
- accessibility/visual/responsive tests where UI risk exists;
- synthetic/production smoke checks for deployed behavior.

No repository is required to implement every layer. The chosen set MUST reflect the actual failure risks.

## 2. Critical invariants require automated regression where practical

Rules involving money, permissions, tenant isolation, history, scheduling conflicts, entitlements, destructive actions, migrations or externally retried mutations SHOULD have automated regression coverage at the authoritative boundary.

Happy-path-only coverage is insufficient for permission/integrity-sensitive behavior.

## 3. Clean and reproducible setup

Automated verification SHOULD start from a known state.

Where setup/seed/migrations are part of the product:

- setup SHOULD be repeatable/idempotent where practical;
- test data MUST be non-production;
- reset/seed commands MUST be prevented from targeting Production accidentally;
- lockfiles/frozen dependency installation SHOULD be used where the ecosystem supports them.

When a Python release supports running a `.pyz` application that reads bundled
package data, run that entry point from a working directory outside the source
tree. Check the bytes the application reads against the expected ZIP member.
A resource present in the archive may be unreadable through a filesystem path
beside `__file__`. Compare the unpacked entry point and check how the packaged
application reports an omitted resource. See `src-python-312-package-resources`.

## 3A. Local SQL test containers: one bounded container per product

**Owner-approved cross-repository rule (2026-10-20).** For local database/integration testing, each Kappa-Bot vertical or independently tested platform product (including MelodIQ Core if it needs a database) MUST use **at most one local Docker test container**. This is a limit, not a requirement to create one. Every branch, agent, suite and repeated run of that product MUST reuse its single approved container. Prefer running products' database suites sequentially, with only the currently tested product's container active.

**Inventory and reuse before creating anything.**

- Inspect the Docker daemon, container identities/labels, owner, stopped/running state, images, ports, volumes and backups. Reuse the existing compatible product-owned container; do not replace, recreate, rename or repurpose it. Unknown ownership or incompatibility is a BLOCKED gate, not permission to delete.
- Default to **one minimal PostgreSQL container** with only the SQL extensions genuinely required by the product. Run application servers, Node, Playwright and orchestration on the host where feasible. Multiple isolated *test databases/schemas inside the same PostgreSQL process* may support fresh/upgrade/replay; no new container is allowed for each suite or branch.
- **MUST NOT** clone, replicate, replace, extend or run more containers for that product: no database replicas, sidecars, Docker Compose multi-service startup, automatic Testcontainers siblings, full Supabase local stacks, ancillary Redis/mail/storage/proxy containers or extra per-worker environments. Guard commands that implicitly start such containers; if they cannot be constrained, do not execute them.
- Use a previously approved, compatible minimal image. No speculative image build/upgrade/pull, privileged mode, public database exposure or restart policy. Restrict ports to loopback when needed, and impose the smallest verified bounded CPU, memory, connection and storage budgets sufficient for real tests. Exact image/extensions and limits are repo-local. Do not increase resources, add services or weaken assertions just to manufacture PASS.
- Preserve existing Docker volumes, backups, snapshots and user-owned data. **Never** remove/prune/replace Docker resources, use customer/Production data, attach unknown existing volumes, or create an unapproved remote/paid test environment.
- Run cheap non-DB gates before startup, avoid empty polling, perform SQL/integration testing at the narrowest justified cadence, and serialize conflicting workloads rather than starting copies. Preserve real concurrency verification through separate connections within the single database server.
- **Stop the single authorized container on completion, failure or abort**, using a reliable `finally`/exit guard scoped to this task's owned container; verify it is stopped. Do not delete it or stop unrelated containers. Preserve evidence and the existing named volumes/backups. Record container identity, whether reused/created, SQL gates actually run, resource measurements where available, and final stopped state.
- If a mandatory SQL/migration/RLS or integration gate cannot run correctly inside this one-container topology, report **BLOCKED** with the exact missing capability. A mock, Production SQL, another container or a wider stack is NOT an acceptable fallback. Request a narrowly scoped decision only if an alternative is genuinely required.

This is a **local test-resource/lifecycle rule**, not a Production runtime architecture rule. SQL correctness, durability, tenant isolation, release compatibility and genuine performance evidence remain mandatory when applicable; one-container budgeting does not waive them.

## 4. CI is a metered hot path

Automatic CI consumes wall-clock time, runner quota, provider capacity and developer attention. Treat that cost as part of the engineering design, not as free infrastructure.

Repositories SHOULD define an explicit latency/cost expectation for the high-frequency push/PR path when CI usage is metered, quota-limited or operationally significant. The exact budget is repository-local; the Handbook does not impose one universal duration.

Before adding or expanding an automatic job, establish:

- the material failure class it catches;
- why a cheaper existing layer cannot catch that failure reliably;
- how often the trigger is expected to fire;
- expected or measured wall-clock/runtime cost;
- whether the same commit is already verified by another trigger or environment;
- whether the evidence belongs on every push, only on affected changes, or only at release time.

Do not run expensive layers on every push merely because they exist. Full builds, local database startup, browser-engine installation, broad E2E/visual matrices, remote integration checks, deterministic seeding and deployment verification belong on the automatic hot path only when they provide distinct evidence that is worth their frequency and cost.

Prefer, where applicable:

- one small automatic source-quality job over several setup-heavy jobs;
- change/path classification when a gate is relevant only to a subset of files;
- a near-zero-cost documentation-only path;
- `cancel-in-progress` or equivalent for superseded runs;
- explicit job timeouts;
- safe dependency/tool caching when it materially reduces cost without hiding freshness problems;
- explicit/manual release workflows for expensive environment-specific verification.

Avoid paying for both pull-request and push workflows over the same effective commit unless those runs prove genuinely different acceptance boundaries.

After changing CI, inspect real run timing rather than assuming the optimization worked. A workflow that is logically smaller but still violates the repository's budget remains an unresolved operational defect.

When comparing CI latency, identify the workflow, triggering event, tested
revision and run attempt. Use the recorded timestamps to separate run creation
to first job start from first job start to last job finish. Keep each job's
duration when jobs overlap. Attribute a delay to the runner queue only with
queue-specific evidence. If the trigger time or workflow completion time is
unavailable, name the observed boundaries. A last-update timestamp alone cannot
establish workflow completion. Verify any billed usage separately. For GitHub
Actions, see `src-github-actions-workflow-run-attempt` and
`src-github-actions-workflow-attempt-jobs`.

## 5. Verification cadence is part of evidence design

The cheapest reliable evidence and the correct cadence are separate decisions.

A repository MAY use different gates at different frequencies, for example:

```text
high-frequency push/PR
  → hygiene / lint / type/domain tests

scope-dependent local or milestone verification
  → build / database / integration / browser / visual

explicit QA/Production release
  → migration / remote config / deployment / smoke / rollback evidence
```

This is not permission to skip required evidence. It is a requirement to run expensive evidence at the narrowest cadence that still protects the risk before acceptance or release.

A platform build performed by the deployment provider does not automatically require a second full CI build on every push; a second build is justified only when it catches a distinct failure earlier or more reliably.

## 6. Test portfolios have a lifecycle

Test count is not a quality objective by itself. Permanent tests SHOULD remain mapped to current product risks and current consumers.

Delete, merge or replace tests when:

- stronger lower-level coverage now proves the same invariant;
- a product path or consumer no longer exists;
- the test preserves implementation history rather than current behavior;
- several cases duplicate the same failure class without meaningful additional coverage;
- setup cost is disproportionate to the distinct risk being protected.

Repositories MAY define a permanent test budget or layer allocation when growth has become a recurring cost problem. A budget MUST NOT be evaded by moving functional assertions into custom runners or scripts.

## 7. Scripts, workflows and verification helpers need current consumers

A script, workflow, fixture generator or verification helper SHOULD have an identifiable current caller or operator procedure.

One-off migration/import/repair helpers SHOULD be removed after their purpose is complete unless a current runbook or recurring operation still depends on them. Do not keep automation merely because it once helped a release.

When a helper is retained for recovery, the recovery path and safety boundary SHOULD remain discoverable from current documentation.

When a .NET verification helper collects child process output through
asynchronous handlers, record the exit code and completion of each required
stream separately. A finite `Process.WaitForExit(timeout)` can return `true`
while a handler still has output to record. In a local test, have the child emit its final
stdout or stderr line. Pause the parent handler after it receives that line
and let the child exit before the handler records it. Check the expected line and
end of each required stream within the helper's existing time budget. If
that budget expires, report the observed process outcome and identify which
output remains unverified. See `src-microsoft-process-waitforexit`.

When a Windows release helper uses Robocopy, record its native exit code.
`1` can indicate a successful copy. `2` and `3` can report extra destination
files, respectively without and with files copied. A code of `8` or higher
reports at least one failure. Check the promised paths at the destination
and compare their hashes when the release requires exact bytes. A rerun can
return `0` while a file outside the copy selection is still missing. If the
release promises an exact inventory, check for extra files as well. See
`src-microsoft-robocopy-exit-codes`.

When an existing Bash verification step pipes output through `tee` or
another final sink, make an earlier stage fail after writing controlled
output. Record the pipeline status and each stage's result before a later
command replaces `PIPESTATUS`. By default the pipeline reports the last
command's status. With `pipefail`, it reports the rightmost nonzero status,
if any. Check the wrapper's reported result and the actual delivered bytes
separately. Include a run where all stages succeed. See
`src-gnu-bash-pipeline-status`.

## 8. CI evidence is scoped evidence

A green CI result means only that the configured jobs completed successfully for that commit/run.

When an existing CI gate claims exact pull-request candidate verification,
record the job's tested source. Use the resolved checkout commit or the
immutable revision used to obtain the tested source archive. Compare that
revision with the approved candidate independently of the run's head
metadata. On GitHub Actions `pull_request` runs for open, mergeable PRs,
`actions/checkout` with its defaults checks out the PR merge ref. Record the
tested merge SHA and label that result as merge validation. See
`src-github-actions-pull-request-tested-source`.

CI MUST NOT be described as proving:

- remote deployment succeeded, unless deployment was part of the run;
- production configuration is correct, unless verified;
- native-device behavior was tested, unless it was;
- visual correctness, unless rendered evidence was inspected/validated;
- external integrations are live, unless exercised;
- security beyond the controls actually checked.

For a gate that already retries tests, retain the first attempt and retry
outcomes for the exact revision and runner configuration. Report a first-pass
success separately from a success after an initial failure. Record the
runner's classification and the gate result under the repository's existing
policy. For example, Playwright can report a test as flaky after it passes on
retry. See `src-playwright-test-retry-outcomes`.

Apply `pol-truthful-engineering`.

## 9. Release identity and target are explicit

A release/deployment flow SHOULD be able to identify:

- exact source commit/build;
- target environment;
- configuration/secrets scope;
- migrations/data changes;
- deployment result;
- smoke/health evidence;
- rollback/forward-fix path where consequence justifies it.

For higher-risk production promotion, expected commit/SHA or equivalent immutable build identity SHOULD be checked rather than deploying an ambiguous moving branch state.

A repository MAY require a cheap successful CI record for the exact release SHA while keeping expensive release evidence outside that automatic workflow. Documentation-only commits SHOULD not be forced through unrelated runtime/browser/database work solely to obtain an exact-SHA quality marker.

## 10. Environment progression

Local, Preview, QA/Staging and Production MAY use different verification depths.

Production promotion SHOULD add evidence for risks that cannot be proven locally, such as:

- remote environment configuration;
- real provider integration;
- migration state;
- environment-specific authorization/secrets;
- deployment health;
- production-safe smoke.

The exact environment names are repo-local.

## 11. Database/migration release safety

When a release changes persistent schema/data:

- migration order and target MUST be explicit;
- compatibility with currently deployed code SHOULD be considered;
- destructive migrations need a deliberate recovery/forward-fix plan;
- Production seeds/resets MUST NOT run as ordinary release setup;
- schema verification SHOULD occur after applying migrations when the platform allows it.

For a PostgreSQL migration using `CREATE INDEX CONCURRENTLY` (including `UNIQUE`), the plan or review must identify the server version and verify that the migration runner issues this statement outside a transaction block. Budget for two table scans, contention with writers, waits for old snapshots, and CPU/I/O load. During an authorized run, `pg_stat_progress_create_index` can identify the active phase and waits. After an attempt, compare the index definition and validity in the catalog with the intended result. A failed build can leave an invalid index that adds write overhead. A unique index that fails during its second scan can continue enforcing uniqueness. Record the remaining state and scope any recovery or retry to the target and authorization already established for it.

Database startup and exhaustive DB verification are often expensive. Their cost does not justify omitting them when schema/data risk changes; instead, place them in the scope-dependent or release gate that protects the change without charging unrelated pushes.

## 12. Physical/native checks

When acceptance depends on real hardware/browser/PWA/camera/keyboard/printing/device behavior, automation/emulation does not automatically replace physical validation.

Record such checks as `passed`, `failed` or `not run/not performed`.

## 13. Release Definition of Done

A release-relevant change is complete when:

- applicable automated layers pass;
- target/build identity is known;
- migrations/config changes are accounted for;
- critical negative paths are covered;
- remote/native/visual gates are either executed or explicitly unrun;
- no evidence claim exceeds what the gates actually demonstrated;
- verification cadence did not silently omit a required risk boundary merely to reduce CI cost.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "testing-risk-based-evidence",
      "type": "decision-question",
      "text": "What is the cheapest reliable evidence that catches each material failure class introduced by this change?",
      "source": "std-testing-release-quality-baseline",
      "covers": [],
      "activate_when": ["intent:modify", "intent:release"],
      "phase": ["planning"],
      "priority": 55
    },
    {
      "id": "testing-release-identity",
      "type": "verification",
      "text": "Verify the exact source/build identity and target environment for a production release or deployment.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["availability", "compatibility"],
      "activate_when": ["operation:deployment", "delivery:production"],
      "force": "should",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "testing-migration-release-safety",
      "type": "verification",
      "text": "Verify migration order and target, schema/data result, and relevant compatibility or recovery behavior for persistent-state releases.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["data-loss", "compatibility"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "should",
      "phase": ["verification"],
      "priority": 96
    },
    {
      "id": "testing-postgres-concurrent-index-evidence",
      "type": "verification",
      "text": "For a PostgreSQL concurrent index build, confirm server version and runner execution outside a transaction block. Account for two table scans, writer and old-snapshot waits, and CPU/I/O load. After an authorized attempt verify the intended index definition and catalog validity. If invalid, assess write overhead and possible continuing uniqueness enforcement after a second-scan failure, and identify the authorized recovery scope.",
      "source": "std-testing-release-quality-baseline",
      "covers": [],
      "activate_when": ["archetype:postgres-concurrent-index"],
      "force": "must",
      "phase": ["planning", "verification"],
      "priority": 96
    },
    {
      "id": "testing-ci-evidence-scope",
      "type": "constraint",
      "text": "A green CI result proves only the configured jobs that actually ran for that commit or run.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["availability"],
      "activate_when": ["surface:ci", "operation:deployment"],
      "force": "must",
      "phase": ["verification"],
      "priority": 88
    },
    {
      "id": "testing-migration-compatibility-plan",
      "type": "decision-question",
      "text": "What compatibility with currently deployed code and recovery or forward-fix behavior must this migration preserve?",
      "source": "std-testing-release-quality-baseline",
      "covers": ["compatibility"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "should",
      "phase": ["planning"],
      "priority": 96
    }
  ]
}
```
