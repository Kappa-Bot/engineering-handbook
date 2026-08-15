---
id: gov-source-authority
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

# Source Authority

## Principle

External sources provide evidence. They do not automatically become internal rules.

Two questions must always be evaluated separately:

1. **Authority:** how trustworthy is the source about the thing it describes?
2. **Applicability:** how well does that guidance fit our actual repositories, products, constraints, and operating model?

A Tier A source can be highly authoritative and still be irrelevant outside one tool or framework.

## Authority tiers

| Tier | Meaning | Typical sources | Promotion expectation |
|---|---|---|---|
| A | Primary authority | official specifications, standards, vendor/framework docs, primary technical docs | Preferred evidence for factual/tool behavior |
| B | Strong reference | original implementations, mature reference projects, established design systems, original methods | Strong evidence; evaluate fit |
| C | Supporting synthesis | engineering handbooks, books, editorial guidance | Validate important claims against stronger sources when possible |
| D | Community evidence | blogs, discussions, snippets, examples | Useful for discovery; requires validation before promotion |

Tier measures source authority, not universal truth.

## Applicability dimensions

When a source materially influences a decision, evaluate the relevant dimensions:

- environment and technology fit;
- maintenance maturity;
- security implications;
- performance implications;
- accessibility implications;
- licensing/reuse terms;
- operational complexity;
- vendor or architecture lock-in;
- compatibility with existing architecture;
- whether the source describes a mandatory standard or merely a recommended practice.

Do not manufacture scores when qualitative evaluation is enough.

## Promotion constraints

- Tier C or D guidance MUST NOT become a cross-repository `MUST` merely because it sounds persuasive.
- Prefer Tier A or B validation for mandatory technical behavior when such authority exists.
- Even Tier A guidance requires an internal applicability decision before becoming handbook policy.
- A source MAY directly justify a factual statement about its own product while still not justifying a universal engineering rule.

## Registry

Material external sources that support handbook knowledge or deliberately promoted cross-repository guidance MUST receive a stable ID in `machine-readable/sources.yaml`.

A one-off repo-local evaluation MAY keep its evidence and links in the consumer repository. If that learning is later promoted into the handbook, its material external sources MUST then be registered centrally.

Recommended source metadata:

- stable `id`;
- title;
- authority `tier`;
- source `kind`;
- canonical URL;
- `canonical_language`;
- `applies_to`;
- lifecycle/status;
- `last_verified`;
- `review_due`;
- `volatility`;
- license/reuse information where material.

Internal handbook documents SHOULD reference source IDs rather than duplicating URL, tier, language, license, and freshness metadata.

## Freshness and volatility

Review cadence should match how fast the source can change.

| Volatility | Typical material | Suggested cadence |
|---|---|---|
| high | agent/tool/vendor configuration and product docs | roughly quarterly or before a material change |
| medium | platform/framework/Git/GitHub behavior | roughly every 6 months or before a material change |
| low | stable architecture/documentation methods | roughly annually or when the source changes materially |

`last_verified` means the source itself was checked on that date. It does not guarantee that every derived internal rule remains correct indefinitely.

## Canonical language

Record `canonical_language`. A translation MAY be convenient for humans but MUST NOT silently replace the freshest canonical version when the translation lags.

## Licensing and copying

“Free to read” is not the same as “licensed to copy or adapt.”

Default behavior:

1. synthesize the idea in our own language;
2. link/reference the source ID when the source is centrally registered, otherwise preserve the repo-local primary reference;
3. preserve attribution/license metadata when adaptation is material;
4. avoid bulk copying external handbooks into this repository.

When license terms are unclear, prefer linking and original synthesis.
