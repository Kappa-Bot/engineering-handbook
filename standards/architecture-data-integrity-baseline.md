---
id: std-architecture-data-integrity-baseline
kind: standard
status: active
owner: engineering
version: "0.15"
applies_to:
  - application-repositories
  - services
  - data-backed-products
sources:
  - src-nist-ssdf-11
  - src-madr
  - src-rfc-9110
  - src-postgresql-19-serialization-failures
  - src-sqlite-create-table-constraints
  - src-sqlite-strict-any
  - src-sqlite-conflict-algorithms
  - src-sqlite-row-values
  - src-ecma262-json-stringify
  - src-sqlite-foreign-keys
  - src-sqlite-savepoints
  - src-sqlite-wal-snapshot-isolation
  - src-rfc-4180-csv-records
  - src-rfc-1952-gzip-members
last_verified: 2026-11-21
review_due: 2027-02-15
---

# Architecture and Data Integrity Baseline

## Purpose

Define the minimum cross-repository architecture/data discipline without prescribing a universal framework, database, cloud, monorepo layout or backend topology.

The Standard favors explicit boundaries and truthful state over premature abstraction.

## 1. Name sources of truth

For each durable concern that can materially diverge, the repository MUST identify the authoritative source of truth.

Typical concerns include identity, authorization, product/domain state, billing, files, configuration, schedules, audit records and deployment state.

Duplicated representations MAY exist for caching, denormalization, search or integration, but their ownership and reconciliation semantics MUST be clear.

See `pat-source-of-truth-boundaries`.

## 2. Keep domain decisions out of incidental UI state

Business invariants that affect permissions, money, history, scheduling, entitlements, inventory, reporting or external behavior MUST NOT exist only as presentation conditions.

Place durable rules behind a boundary that can be verified independently from a particular screen.

The exact architecture is repo-local: server functions, domain services, database constraints/RLS, RPCs, application services or another appropriate mechanism may satisfy the requirement.

## 3. Prefer the smallest architecture that is honest

Do not introduce a backend, queue, event bus, repository abstraction, generic platform package or distributed component solely because it may be useful later.

Likewise, do not keep a local/mock implementation after the product claims durable production behavior if that implementation can create false confidence.

Complexity is justified by a current invariant, verified scale need, security boundary, integration need, operability need or demonstrated reuse.

## 4. Generalization requires consumers

A product-specific implementation SHOULD remain product-specific until another real consumer or strong independent evidence demonstrates a stable reusable boundary.

Do not extract a generic core merely because names can be parameterized.

When reuse emerges, identify:

- what is genuinely common;
- what remains tenant/product/domain policy;
- compatibility/versioning expectations;
- migration path for existing consumers;
- what evidence demonstrates the abstraction is better than duplication.

## 5. Data integrity before convenience

Where data has operational, financial, legal, security or historical meaning:

- invalid state transitions MUST be rejected rather than silently normalized;
- destructive operations SHOULD be replaced by status/revocation/void/audit semantics when history matters;
- generated identifiers/tokens MUST have documented uniqueness/security requirements;
- idempotency SHOULD be used for retried external or mutation workflows where duplicate effects are harmful;
- migrations MUST be treated as executable changes to production state, not ordinary source edits;
- seed/reset tooling MUST be scoped so Production cannot be reset accidentally.

When a PostgreSQL Serializable operation already retries SQLSTATE `40001` (`serialization_failure`), start a fresh transaction and rerun the reads and application logic that choose statements and values. Use a controlled conflict that changes a read-dependent decision. Check the committed outcome and the failure reported when the caller reaches its attempt limit. If the operation triggers an external effect, verify that retrying an aborted attempt cannot duplicate it. Record delivery separately from the database commit. [PostgreSQL §13.5](https://www.postgresql.org/docs/19/mvcc-serialization-failure-handling.html).

When checking SQLite connection setup that promises foreign-key enforcement,
read back `PRAGMA foreign_keys` on the connection that performs the write.
SQLite leaves the setting unchanged when a transaction is already open,
even if the assignment reports no error. If the driver can start a
transaction during setup, compare that order with setup before the
transaction. In an isolated fixture with an immediate foreign key, check
whether a missing-parent insert is rejected and which rows a separate
connection sees after rollback. See `src-sqlite-foreign-keys` §2.

When an existing SQLite transaction uses deferred foreign keys, verify
enforcement on the tested connection before starting the transaction.
Use a fixture where a write succeeds with an unresolved reference. Observe
the rejected `COMMIT` and whether the transaction remains open. Read the
committed rows from a separate connection after the failed commit and again
after the application's supported repair and successful commit or rollback.
Record the statement result and committed result separately. See
`src-sqlite-foreign-keys` §§2 and 4.2.

When an existing SQLite multi-row statement can hit a uniqueness constraint,
check what remains after an error under the chosen conflict algorithm. `ABORT`
backs out changes made by that statement and keeps work from earlier statements
in the transaction. `FAIL` can leave changes made before the conflict in the
failed statement pending. Put the conflict between two otherwise valid rows in
an isolated fixture. Record the error and pending rows, then use a separate
connection to verify which rows are visible before and after the workflow's
intended commit or rollback. See `src-sqlite-conflict-algorithms`.

In existing SQLite workflows that use nested savepoints, observe the
writer's transaction state and read the committed values from a separate
connection after a successful `RELEASE`. An inner `RELEASE` leaves the
enclosing transaction open. Exercise outer rollback of the released changes
and confirm visibility after a successful outer `COMMIT` on a separate
run. Where a `SAVEPOINT` starts the transaction, releasing it commits if
that release closes the outermost transaction. See `src-sqlite-savepoints`
§§2–3.

When an existing SQLite WAL operation reads before writing in the same
transaction, use a separate connection to commit a change that alters the
write decision. Record the extended result when the read transaction tries
to write. After `SQLITE_BUSY_SNAPSHOT`, check that the open transaction
still reads its old snapshot. For a supported retry, verify that it ends the
stale transaction, repeats the reads and recomputes the decision in a fresh
transaction. Check the committed result from the separate connection. See
`src-sqlite-wal-snapshot-isolation`.

For APIs that already use `If-Match` on writes, check the current
representation after normal request checks and before mutation effects.
Concrete entity tags match only when both are strong and their opaque values
are identical. `*` checks whether a current representation exists.
Verify the documented response behavior and confirm a rejected precondition
adds no mutation effects. If the API acknowledges an already-applied change,
verify it adds no second effect. To establish lost-update protection, verify
that the version check remains effective at the authoritative commit boundary.
Use authorized competing writes with the same starting strong tag and inspect
the final persisted state and durable effects.
See `src-rfc-9110` §§8.8.3.2, 13.1.1 and 13.2.1.

For APIs that already use `If-None-Match: *` for create-if-absent writes,
verify absence of a current representation at the authoritative create
boundary after normal request checks. For an otherwise valid write with a
failed condition, verify `412 (Precondition Failed)`. With authorized
competing creates for the same target, inspect the final representation and
durable effects. When the fixture starts without a current representation
and a create request succeeds, verify exactly one committed creation and its
intended effects, even if both clients previously observed absence. When the
target already has a
current representation, verify zero new creations and preservation of that
representation and its durable effects.
See `src-rfc-9110` §§13.1.2 and 13.2.

When an existing CSV export promises a record count or record set, parse the
completed file using its declared delimiter, quoting and header rules.
A quoted field can span physical lines. Compare the parsed records and
representative field values with the promised data after accounting for the
header. Include a multiline field when the contract permits one. Record
which consumer parsed the file when compatibility with that consumer is
part of the claim. See `src-rfc-4180-csv-records` §§2–3 for the common CSV
form and its header convention.

When an existing `.gz` import or export permits concatenated gzip members,
verify the promised output with the intended consumer. Use two members with
distinct content. Check that the consumer reads through the end of the final
member and produces the combined data in order. With an incomplete final
member, distinguish any records already emitted from successful completion
of the whole file. Check the consumer's documented handling of partial
results. See `src-rfc-1952-gzip-members` §§2.2–2.3.

## 6. Schema and authorization are part of architecture

When the data platform supports server-side constraints or row/data policies, use them where they materially protect invariants or tenant/user isolation.

When a SQLite keyset query promises `NULLS LAST` on a nullable leading sort
key, test a page ending just before the first `NULL` and another ending
inside the `NULL` group. Even with a unique tie-breaker, a row-value `>`
comparison can yield SQL `NULL`, so the `WHERE` clause skips that row.
Follow the actual cursor through the final empty page. Compare the ordered
IDs with the same filtered, unpaged query on one snapshot, including the
remaining IDs within the `NULL` group. See `src-sqlite-row-values` §2.1
and `pat-api-contract-evolution`.

When a SQLite `ANY` column must preserve the exact spelling of an
identifier, check whether the table is `STRICT` and what type the driver
binds. Use two distinct text spellings of the same number, including
leading zeros, and an integer binding as a control. After a successful
commit, read back the stored values and `typeof(column)` from another
connection. In an ordinary table, `ANY` can convert both text spellings
to the same integer. In a `STRICT` table, `ANY` preserves the text it
receives. See `src-sqlite-strict-any` §3.

When verifying an existing SQLite `CHECK` on nullable inputs, include a
passing value, a failing value and an input that makes the expression
`NULL` if it can yield that result. A numeric zero violates the check.
A `NULL` result does not. If the contract distinguishes an omitted value
from an explicit `NULL`, test both against the schema's default and any
`NOT NULL` constraint. Record which writes failed and why, then read back
the resulting rows. See `src-sqlite-create-table-constraints` §§3.2, 3.7–3.8.

When an existing JavaScript handoff uses `JSON.stringify()` for optional
fields, compare the encoded member names and array positions with the
values the receiver decodes. An object member with `undefined` is omitted
under ordinary serialization. An array element with `undefined` or an
empty position with no inherited value becomes `null` at that index.
Include explicit `null`, a missing member and any supported zero, false
or empty text controls. Verify the receiver's declared interpretation.
See `src-ecma262-json-stringify` §25.5.4.

Client filters and hidden routes MUST NOT be the sole protection for sensitive data.

Provider-specific mechanisms such as PostgreSQL constraints, RLS, Supabase policies or equivalent remain repo-local implementation choices.

## 7. Environment-specific architecture is allowed

Demo, local, Preview, QA and Production MAY intentionally use different components when the difference is explicit and cannot be mistaken for production equivalence.

Use `pol-truthful-engineering` and `pat-capability-environment-integrity`.

## 8. Durable architecture decisions

Record a repo-local ADR/decision when a choice changes long-lived boundaries, source-of-truth ownership, persistence strategy, security model, integration contract, deployment topology, compatibility obligations or costly future migration.

Do not create ADRs for routine implementation detail.

## 9. Definition of done

An architecture/data change is complete when:

- authoritative owners are clear;
- invariants are enforced at an appropriate boundary;
- failure and retry semantics are understood;
- migrations/data transformations have a verification path where applicable;
- mock/demo/production differences are explicit;
- premature reusable abstractions were avoided or justified;
- durable decisions are recorded when future contributors would otherwise need to rediscover them.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "architecture-authoritative-owner",
      "type": "decision-question",
      "text": "What is the authoritative source of truth for each durable concern changed by this task?",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["capability:persistence", "operation:mutation", "operation:migration"],
      "force": "must",
      "phase": ["planning"],
      "priority": 92
    },
    {
      "id": "architecture-migrations-are-production-state",
      "type": "constraint",
      "text": "Treat migrations as executable changes to production state rather than ordinary source edits.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
    {
      "id": "architecture-migration-verification",
      "type": "verification",
      "text": "Verify the migration or data transformation path when the change alters durable state.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "must",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "architecture-generalization-needs-evidence",
      "type": "constraint",
      "text": "Keep product-specific implementations local until another real consumer or strong evidence demonstrates a stable reusable boundary.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["compatibility"],
      "activate_when": ["intent:create", "intent:modify"],
      "force": "should",
      "phase": ["planning"],
      "priority": 35
    }
  ]
}
```
