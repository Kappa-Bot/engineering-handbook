---
id: pat-api-contract-evolution
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - http-apis
  - external-integrations
  - multi-consumer-interfaces
sources:
  - src-openapi-spec
last_verified: 2026-08-15
review_due: 2027-02-15
---

# API Contract and Evolution

## Intent

Make interfaces explicit when independent consumers or external integrations make accidental breaking change expensive.

## When a formal contract is valuable

Use an explicit API contract when one or more apply:

- external/customer integration;
- independently deployed client/server;
- multiple consumers maintained separately;
- generated clients/documentation provide real value;
- compatibility/deprecation needs durable governance.

Do not create an OpenAPI document for every trivial server route merely to satisfy documentation ceremony.

## Contract content

A meaningful contract SHOULD cover, as applicable:

- endpoint/operation and methods;
- request/response schemas;
- authentication/authorization expectations;
- errors/status semantics;
- pagination/filtering;
- idempotency/retry behavior;
- rate/usage constraints;
- version/deprecation behavior.

OpenAPI is the preferred standard description format when formalizing HTTP API contracts unless repo/context provides a stronger reason otherwise.

## Evolution

Prefer additive compatible changes when reasonable.

Breaking changes require a deliberate migration/version/deprecation strategy proportional to the number and independence of consumers.

Do not keep obsolete compatibility forever without evidence; define retirement conditions.

## Source of truth

Choose whether the contract is:

- design-first/canonical specification;
- generated from implementation;
- generated from typed schemas.

Whichever model is selected, avoid two independently maintained “canonical” contracts that can drift.

## Verification

Where breakage would be harmful, use schema/contract tests, generated-client checks or consumer integration tests to detect drift.

A syntactically valid OpenAPI document does not prove implementation behavior unless the implementation is also checked against it.
