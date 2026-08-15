---
id: gov-handbook-governance
kind: governance
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Handbook Governance

## Purpose

This document defines the authority, scope, precedence, canonicality, ownership, and exception model of the Engineering Handbook.

## Authority and scope

The handbook is the canonical source for engineering rules intentionally shared across Kappa-Bot repositories. Consumer repositories remain authoritative for their own local architecture and product decisions when those decisions do not conflict with applicable handbook governance or policy.

The handbook does not replace external obligations such as law, contracts, platform requirements, security obligations, or other non-negotiable constraints.

## Normative language

- **MUST / MUST NOT**: mandatory unless an explicitly permitted and scoped exception exists.
- **SHOULD / SHOULD NOT**: expected default; deviations require a concrete reason.
- **MAY**: optional.

## Precedence

When applicable guidance conflicts, use this order:

1. External non-negotiable obligations.
2. Active Handbook Governance.
3. Applicable active Policy.
4. Applicable active Standard.
5. Approved repo-local decision or explicitly permitted exception.
6. Pattern.
7. Playbook.
8. Reference or research.

A repo-local ADR MUST NOT silently override a Policy. A deviation from mandatory handbook guidance is valid only where the governing document permits an exception and the exception is explicit, scoped, and recorded where material.

A direct owner instruction may activate a permitted exception, such as explicitly requesting a Git worktree, but it does not silently rewrite handbook policy.

Runtime precedence of Codex or other tools is defined by those tools themselves. This handbook governs the authoritative engineering content and how distributed artifacts are produced; it does not redefine vendor runtime precedence.

## Canonicality

There MUST be at most one active canonical normative document per topic. New material SHOULD update or supersede that document rather than create a competing active rule.

Historical decisions and superseded records MAY be retained when they explain why the current state exists.

## Ownership

`owner: engineering` denotes responsibility for maintaining the artifact, reviewing its continued applicability, and resolving conflicts. More granular ownership may be introduced only when real organizational needs justify it.

## Exceptions

Exceptions MUST be:

- permitted by the applicable governing document;
- explicit rather than inferred;
- as narrow and temporary as practical;
- documented when they materially affect maintainability, safety, architecture, delivery, or future decisions.

## Changes to governance

Changes to precedence, lifecycle, authority, canonicality, or promotion rules are governance changes and SHOULD be accompanied by a decision record when they materially alter the operating model.
