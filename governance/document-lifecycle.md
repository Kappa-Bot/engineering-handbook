---
id: gov-document-lifecycle
kind: governance
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Document Lifecycle

## Normative lifecycle states

Foundation v0.1 uses only these states for governed handbook documents:

- `proposed` — under consideration and not authoritative.
- `active` — current canonical guidance within its scope.
- `deprecated` — still present but discouraged and expected to be replaced or retired.
- `superseded` — replaced by another identified artifact.
- `retired` — no longer applicable and retained only when historical value justifies it.

Do not add new lifecycle states without a demonstrated need.

## Canonical rule

There MUST be at most one `active` canonical normative document for a topic. A replacement SHOULD mark the previous artifact `superseded` and link both directions where useful.

## Metadata

Normative governance, policy, and standard documents MUST include:

- `id`
- `kind`
- `status`
- `owner`
- `version`
- `applies_to`
- `sources`
- `last_verified`
- `review_due`

Use `supersedes` and `superseded_by` only when applicable.

## Review

`review_due` is a review trigger, not an automatic expiration. A document remains active until deliberately changed, deprecated, superseded, or retired, unless an external obligation makes it invalid sooner.

Reviews SHOULD verify both internal applicability and the freshness of material external sources.

## Versioning

Foundation v0.1 uses lightweight document versions. Do not introduce a sophisticated repository-wide semantic-versioning system until distribution or compatibility requirements make it necessary.

## Decision records

Decision records are historical evidence and use their own decision status such as `proposed`, `accepted`, `deprecated`, or `superseded`. They are not periodically rewritten merely to look current. If a decision changes, prefer a new decision record that supersedes the old one.
