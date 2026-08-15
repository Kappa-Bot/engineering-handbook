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

## Purpose

Lifecycle metadata tells humans and agents whether a governed artifact is current, transitional, historical, or no longer applicable.

Foundation v0.1 deliberately keeps the state model small.

## Governed-document states

- `proposed` — under consideration; not authoritative.
- `active` — current canonical guidance within its declared scope.
- `deprecated` — still present, but use is discouraged and replacement/retirement is expected.
- `superseded` — replaced by another identified artifact.
- `retired` — no longer applicable; retained only when historical value justifies it.

Do not add lifecycle states merely to express workflow details that belong in Git/PR status.

## Canonical rule

There MUST be at most one `active` canonical normative document per topic.

A replacement SHOULD:

1. identify the new canonical artifact;
2. mark the old artifact `superseded` where appropriate;
3. set `superseded_by` / `supersedes` when useful;
4. update `machine-readable/catalog.yaml`;
5. preserve history if it explains future decisions.

## Required metadata

Active governance, policy, and standard documents MUST declare:

- `id`
- `kind`
- `status`
- `owner`
- `version`
- `applies_to`
- `sources`
- `last_verified`
- `review_due`

`version` is the document's lightweight content version, not a repository release promise.

## Review model

`review_due` is a trigger for deliberate review, not automatic expiration.

A review should check:

- whether the problem still exists;
- whether scope/applicability changed;
- whether referenced material sources are still valid;
- whether exceptions have become the de facto default;
- whether the rule can now be enforced more cheaply/reliably;
- whether adoption experience suggests simplification.

If nothing material changed, update review metadata only after actually performing the review.

## Versioning

Foundation v0.1 uses simple versions such as `0.1`, `0.2`, `1.0` per governed document.

Do not introduce repository-wide semantic compatibility guarantees until distributed artifacts or consumer automation make them necessary.

## Decision records

ADRs are historical evidence, not ordinary active policies.

Decision records use statuses such as `proposed`, `accepted`, `deprecated`, or `superseded`. When a decision changes materially, prefer a new ADR that supersedes the old one instead of rewriting the historical context.

## Templates and distributed artifacts

Templates and generated/installed agent configuration may have their own release/distribution metadata later. Until that need is real, their canonical source remains the file tracked in this repository.
