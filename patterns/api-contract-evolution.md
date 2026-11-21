---
id: pat-api-contract-evolution
kind: pattern
status: active
owner: engineering
version: "0.8"
applies_to:
  - http-apis
  - external-integrations
  - multi-consumer-interfaces
sources:
  - src-openapi-spec
  - src-json-schema-2020-12-enum
  - src-typescript-narrowing-exhaustive-unions
  - src-rfc-9110
  - src-rfc-9457
  - src-rfc-9530
  - src-rfc-6266-content-disposition
  - src-rfc-8187-extended-field-parameters
  - src-rfc-8259-networked-json
  - src-whatwg-html-server-sent-events
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

Before adding a value to a closed response enum, verify behavior in existing
independently deployed consumers that depend on that set. A strict decoder
can reject the new value. A consumer that handles every old case may need
another case when compiling against the expanded contract. Exercise the new
response value with representative supported consumers and check any
documented unknown-value behavior. Record producer schema and consumer
compatibility as separate observations. See
`src-json-schema-2020-12-enum` and
`src-typescript-narrowing-exhaustive-unions`.

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

For an endpoint that already advertises a localized attachment name, verify
the delivered `Content-Disposition` field and the name suggested by the
supported client. When the contract uses `filename*`, verify its UTF-8
extended value. Check any promised `filename` fallback with the relevant
client or report that path as unverified. RFC 6266 prefers a valid
`filename*` for recipients that support both parameters. Treat the name as
advisory and check the completed content and media type independently.
See `src-rfc-6266-content-disposition` §§4.3 and 5 and
`src-rfc-8187-extended-field-parameters` §3.2.

When an existing API delivers interoperable JSON, verify UTF-8 and check the
start of the JSON bytes after any HTTP content decoding and before text parsing.
Networked JSON senders omit the leading byte order mark under RFC 8259 §8.1.
A tolerant consumer can accept a leading mark, so record the byte check
alongside the parsed result. This check concerns the start of the network
body. See `src-rfc-8259-networked-json` §8.1.

For an existing server-sent event stream consumed through `EventSource`,
record the reconnect request's `Last-Event-ID` and the application result
separately. The header reports the browser's last event ID. A complete
`id`-only block can advance that ID without dispatching a message. In a
local test, compare consumers that receive the same event while only one
applies it. Verify the result claimed for each consumer at its application
boundary. If only the reconnect header was observed, report application
of the event as unverified. See `src-whatwg-html-server-sent-events`
§§9.2.4 and 9.2.6.

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
