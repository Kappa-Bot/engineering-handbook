---
id: gov-source-authority
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

# Source Authority

## Purpose

External sources support engineering decisions; they do not automatically become internal rules. Source authority and applicability are evaluated separately.

## Authority tiers

- **Tier A — Primary authority:** official specifications, standards, vendor/framework documentation, and other primary technical sources.
- **Tier B — Strong reference:** original implementations, mature reference projects, established design systems, and high-quality primary practitioner material.
- **Tier C — Supporting reference:** solid engineering handbooks, books, and editorial guidance that synthesize practice.
- **Tier D — Community evidence:** blogs, discussions, examples, and other community material requiring stronger validation before promotion.

A higher tier increases confidence in what the source says. It does not prove that the guidance applies universally to our products.

## Applicability

Every material source SHOULD declare `applies_to` in the external source registry. A Tier A source MAY be highly authoritative but relevant only to one tool, framework, product, or environment.

## Promotion constraint

Tier C or Tier D material MUST NOT become a mandatory cross-repository rule merely because it is persuasive. Prefer validation against Tier A or Tier B evidence when available and validate the rule internally before promotion.

## Traceability

Important external sources MUST receive a stable ID in `machine-readable/sources.yaml`. Internal documents SHOULD reference source IDs rather than duplicate URL, tier, language, volatility, and verification metadata.

## Freshness

Source review cadence SHOULD reflect volatility:

- high-volatility vendor/tool documentation: review frequently;
- medium-volatility framework or platform guidance: review periodically;
- low-volatility architectural methods and stable standards: review less frequently.

`last_verified` records when the source itself was checked. It is not proof that every internal statement depending on it remains correct forever.

## Language

Record `canonical_language` for important sources. Prefer the canonical or freshest language when translations lag or differ.

## Licensing and reuse

“Free to read” does not mean “licensed to copy.” Prefer synthesis and links over copying. Before redistributing or adapting substantial source material, verify and record the relevant license or reuse terms.
