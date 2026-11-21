---
id: pat-api-contract-evolution
kind: pattern
status: active
owner: engineering
version: "0.4"
applies_to:
  - http-apis
  - external-integrations
  - multi-consumer-interfaces
sources:
  - src-openapi-spec
  - src-rfc-9110
  - src-rfc-9457
  - src-rfc-9530
  - src-aws-ecs-idempotency
last_verified: 2026-11-21
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

If an operation accepts an idempotency key, identify its scope and which request parameters define equivalent intent. Use contract fixtures to show that an equivalent retry after completion, while the key is valid, produces no additional intended effect. Record what the caller observes and what takes effect when it reuses the key with materially different parameters. Where applicable, cover a retry while the original operation is still in progress and a late retry after the key expires. Mark any outcome the contract leaves unspecified. [HTTP method semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) and [Amazon ECS API example](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_Idempotency.html).

If an existing API uses `application/problem+json`, verify that the producer's
optional `status` matches its HTTP response. Record the observed HTTP status,
the advisory body value and the capture point when they differ. Generic HTTP
handling follows the observed status. Use the resolved `type` URI and documented
extensions for machine decisions. Treat `title` and occurrence-specific `detail`
as human-readable text that can be localized. Check safe user-facing recovery
copy and keep implementation diagnostics in authorized internal logs.
See `src-rfc-9457` §§3.1.1–3.2 and 5.

For an endpoint that already uses `Content-Digest` or `Repr-Digest`, verify
each field that is present. Record the algorithm and the selected
representation, including its content coding. For a `206 (Partial Content)`
response carrying one byte range, compare `Content-Digest` with a digest of
the returned range bytes and `Repr-Digest` with a digest of the complete
selected representation data. If only the range and advertised fields are
available, mark the whole-representation check unverified. Verify sender
identity or artifact provenance separately when either is claimed.
See `src-rfc-9530` §§2–3 and Appendix B.3.

A syntactically valid OpenAPI document does not prove implementation behavior unless the implementation is also checked against it.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "api-contract-when-consumers-independent",
      "type": "decision-question",
      "text": "Does this interface have external or independently deployed consumers, compatibility obligations, or generated-client value that justify a formal contract?",
      "source": "pat-api-contract-evolution",
      "covers": ["compatibility"],
      "activate_when": ["operation:integration", "boundary:external"],
      "phase": ["planning"],
      "priority": 80
    },
    {
      "id": "api-contract-single-source",
      "type": "constraint",
      "text": "Choose one authoritative API contract model and avoid independently maintained canonical contracts that can drift.",
      "source": "pat-api-contract-evolution",
      "covers": ["compatibility"],
      "activate_when": ["operation:integration", "boundary:external"],
      "phase": ["planning", "implementation"],
      "priority": 78
    },
    {
      "id": "api-contract-drift-verification",
      "type": "verification",
      "text": "Where interface breakage is harmful, verify implementation compatibility using schema, contract, generated-client, or consumer integration evidence; syntax alone is insufficient.",
      "source": "pat-api-contract-evolution",
      "covers": ["compatibility"],
      "activate_when": ["operation:integration", "boundary:external"],
      "phase": ["verification"],
      "priority": 90
    }
  ]
}
```
