---
id: pat-api-contract-evolution
kind: pattern
status: active
owner: engineering
version: "0.28"
applies_to:
  - http-apis
  - external-integrations
  - multi-consumer-interfaces
sources:
  - src-openapi-spec
  - src-sqlite-row-values
  - src-json-schema-2020-12-enum
  - src-json-schema-draft07-default
  - src-ajv-v6-default-assignment
  - src-typescript-narrowing-exhaustive-unions
  - src-rfc-9110
  - src-rfc-9457
  - src-rfc-9530
  - src-rfc-6266-content-disposition
  - src-rfc-8187-extended-field-parameters
  - src-rfc-8259-networked-json
  - src-rfc-4180-csv-records
  - src-python-312-csv-null-quoting
  - src-python-utf8-signature-codec
  - src-rfc-7396-json-merge-patch
  - src-ndjson-specification
  - src-whatwg-textdecoderstream
  - src-whatwg-fetch-response-abort
  - src-whatwg-fetch-content-coding
  - src-whatwg-html-form-submission
  - src-whatwg-html-form-entry-list
  - src-whatwg-html-inert-subtrees
  - src-whatwg-html-server-sent-events
  - src-aws-ecs-idempotency
  - src-whatwg-url-search-params
last_verified: 2026-11-22
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

For an existing JSON Merge Patch contract (`application/merge-patch+json`),
start with a known representation and compare the whole decoded result.
In a recursive object patch, check that omitted nested members keep their
prior values and that a member set to JSON `null` is removed. Check that a
supplied array replaces the entire prior array. If the contract accepts
non-object patch documents, verify whole-target replacement, including
literal top-level JSON `null` where allowed. See `src-rfc-7396-json-merge-patch`
§§2 and 4.

When an existing API schema declares a JSON Schema `default` annotation,
record the validation verdict and the object before and after validation.
Exercise an omitted optional property, explicit `null` where allowed, a
supplied value and a missing required property. If the existing pipeline
assigns defaults, verify which fields it fills and at which step. Inspect
changes to the input even when validation rejects it. See
`src-json-schema-draft07-default` §10.2 and
`src-ajv-v6-default-assignment` for an implementation example.

If an operation accepts an idempotency key, identify its scope and which request parameters define equivalent intent. Use contract fixtures to show that an equivalent retry after completion, while the key is valid, produces no additional intended effect. Record what the caller observes and what takes effect when it reuses the key with materially different parameters. Where applicable, cover a retry while the original operation is still in progress and a late retry after the key expires. Mark any outcome the contract leaves unspecified. [HTTP method semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) and [Amazon ECS API example](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_Idempotency.html).

For a filtered API that promises stable keyset pagination, include eligible
rows with equal leading sort values across a page boundary and rows the
filter excludes. On one fixed snapshot, follow the returned cursors to the
end. Compare the concatenated row identities, their order and their count
with an unpaged reference using the same filter and complete ordering.
Check that traversal resumes after the last row according to the
contract's tie-breaker. If the API promises consistency when data changes
between requests, verify that promise separately. See `src-sqlite-row-values`.

If an existing API uses `application/problem+json`, verify that the producer's
optional `status` matches its HTTP response. Record the observed HTTP status,
the advisory body value and the capture point when they differ. Generic HTTP
handling follows the observed status. Use the resolved `type` URI and documented
extensions for machine decisions. Treat `title` and occurrence-specific `detail`
as human-readable text that can be localized. Check safe user-facing recovery
copy and keep implementation diagnostics in authorized internal logs.
See `src-rfc-9457` §§3.1.1–3.2 and 5.

For an existing API that accepts ordered repeated values for a query name,
check the actual request target and the values the intended consumer reads.
Use distinct values and a repeated identical value to verify order and count.
If the contract distinguishes a blank value from an absent parameter, check
both. A scalar lookup exposes only one occurrence in `URLSearchParams`.
Verify the full list when a client or receiver projects tuples into an
object with one property per name. See `src-whatwg-url-search-params`.

For an existing server-side HTTP response reader that handles multiple
`Set-Cookie` field lines, compare the separate response lines with the
values the consumer exposes. Check their count, values and order, with
absent and single-line controls. Include a valid `Expires` date containing
a comma so the test can distinguish field lines from comma-delimited text.
See `src-rfc-9110` §5.3.

When an existing HTTP contract redirects a `POST`, record the initial status
and `Location`. Check whether the supported client follows the redirect
and, if so, which method and body reach the target. A `303 See Other`
permits a retrieval request, such as a `GET` without the original form
body. A client that automatically follows a `307 Temporary Redirect` must
retain `POST`. Use a synthetic form value to check the body the contract
promises. Verify any claimed durable effect separately. See `src-rfc-9110`
sections 15.4.4 and 15.4.8.

For an existing HTTP contract that returns `405 (Method Not Allowed)`, record
the request method, target resource, response status and `Allow` together.
Compare the advertised methods with the current contract for that resource.
A present but empty `Allow` advertises no supported methods. An absent
`Allow` fails the `405` response contract. Where the same method is supported
on another fixture resource, record that result separately. Verify caller
authorization separately with approved fixtures. See `src-rfc-9110` §§10.2.1
and 15.5.6.

For an endpoint that already uses `Content-Digest` or `Repr-Digest`, verify
each field that is present. Record the algorithm and the selected
representation, including its content coding. For a `206 (Partial Content)`
response carrying one byte range, compare `Content-Digest` with a digest of
the returned range bytes and `Repr-Digest` with a digest of the complete
selected representation data. If only the range and advertised fields are
available, mark the whole-representation check unverified. Verify sender
identity or artifact provenance separately when either is claimed.
See `src-rfc-9530` §§2–3 and Appendix B.3.

When an endpoint already returns a `206 (Partial Content)` response with
`multipart/byteranges`, verify the boundary parameter and confirm that
`Content-Range` appears in each part and is absent from the HTTP header
section. With a known selected representation, compare each part's bytes
with its declared inclusive offsets, even when the parts arrive in a
different order from the requested ranges. See `src-rfc-9110` §§14.1.2,
14.4 and 15.3.7.2.

For an existing download that resumes with `If-Range`, keep the saved
prefix and validator tied to the same representation. Exercise a matching
validator and a changed representation with the same total length. For
the `206` path, verify the returned range and the assembled bytes against
the expected full representation. For a stale validator that yields a full
`200`, verify that the consumer uses the full new response as the completed
representation. Check any final digest or length that the contract promises.
See `src-rfc-9110` §13.1.5.

For an endpoint that already advertises a localized attachment name, verify
the delivered `Content-Disposition` field and the name suggested by the
supported client. When the contract uses `filename*`, verify its UTF-8
extended value. Check any promised `filename` fallback with the relevant
client or report that path as unverified. RFC 6266 prefers a valid
`filename*` for recipients that support both parameters. Treat the name as
advisory and check the completed content and media type independently.
See `src-rfc-6266-content-disposition` §§4.3 and 5 and
`src-rfc-8187-extended-field-parameters` §3.2.

For an existing form endpoint that accepts repeated entries under one field
name, compare the selected values, serialized form data and decoded receiver
values for the encoding in use, such as URL-encoded or multipart. Include
distinct values and a repeated equal value when the contract permits it.
Verify each entry and any order the application promises. Inspect the entries
before converting them to a map with one value per key, which can collapse
legitimate selections. See `src-whatwg-html-form-submission` §§4.10.22.4 and
4.10.22.6–8.

When an existing form makes an inactive section `inert`, check the actual
focus path and the request the form submits. A named, enabled field in
that section can retain a value and contribute it to the form even while
keyboard navigation skips the field. Compare with the enabled interactive
state and the flow's omission path, such as a disabled field. Observe what
the receiver gets and how it interprets a present or omitted value. See
`src-whatwg-html-inert-subtrees` §6.3 and `src-whatwg-html-form-entry-list`
§4.10.22.4.

When an existing API delivers interoperable JSON, verify UTF-8 and check the
start of the JSON bytes after any HTTP content decoding and before text parsing.
Networked JSON senders omit the leading byte order mark under RFC 8259 §8.1.
A tolerant consumer can accept a leading mark, so record the byte check
alongside the parsed result. This check concerns the start of the network
body. See `src-rfc-8259-networked-json` §8.1.

When an existing UTF-8 CSV contract accepts a leading byte-order mark as
optional, compare the decoded header and named field lookups on both
accepted forms. A reader that leaves `U+FEFF` on the first field name can
keep the expected record count while a required key is missing. If the
contract permits `U+FEFF` within a data value, verify that the reader
preserves it. See `src-rfc-4180-csv-records` §3 and
`src-python-utf8-signature-codec` for Python's optional-signature decoding.

When a CSV contract distinguishes null from an empty string, export both
in the same named column alongside a nonempty control. Compare the encoded
fields, then check the value and type each supported reader returns for
each record. Python's default CSV writer can serialize `None` and `""`
identically. With `QUOTE_NOTNULL`, Python 3.12 can write an unquoted empty
field for null and a quoted empty string while its reader returns `""` for both.
Verify that the consumer recovers the distinction the contract promises.
See `src-python-312-csv-null-quoting`.

When an existing JSON contract promises exact integers, check the wire
value and how each supported consumer decodes it. Test adjacent integers
around the supported range boundary. A consumer using IEEE 754 binary64
numbers can decode distinct large integers to the same value. Keep the
verified numeric range with the consumer evidence. If the contract already
allows a separate exact representation, exercise that path too. See
`src-rfc-8259-networked-json` section 6.

For a successful HTTP response whose contract distinguishes no content from
JSON content, verify the status and received body before invoking the parser.
An expected `204 (No Content)` response ends after the header section. A
response that promises JSON must carry a JSON value. An allowed literal `null`
is valid JSON, and zero bytes cannot supply that value. Check the decoded
value or lack of content at the supported consumer boundary. If the operation
also claims a durable effect, verify that effect separately. See `src-rfc-9110`
§§6.4.1 and 15.3.5 and `src-rfc-8259-networked-json` §§2–3.

When verifying an existing API's negotiated `HEAD` metadata, pair `HEAD`
with `GET` for the same target, representation state and negotiation inputs,
such as `Accept-Language` and `Accept-Encoding`. If `HEAD` sends a
`Content-Length` field, compare that value with the matched `GET` content's
octet count before decoding any content coding. Record an omitted optional
length separately from a mismatched value. Verify any claim that `HEAD`
sent no content at a capture point that can observe the response bytes.
See `src-rfc-9110` §§8.6 and 9.3.2.

For an existing server-sent event stream consumed through `EventSource`,
record the reconnect request's `Last-Event-ID` and the application result
separately. The header reports the browser's last event ID. A complete
`id`-only block can advance that ID without dispatching a message. In a
local test, compare consumers that receive the same event while only one
applies it. Verify the result claimed for each consumer at its application
boundary. If only the reconnect header was observed, report application
of the event as unverified. See `src-whatwg-html-server-sent-events`
§§9.2.4 and 9.2.6.

When an existing Fetch API consumer supports cancellation during a download,
use a fixture that sends the response headers and part of the promised body,
then holds the rest. Record the status and the bytes the consumer has read.
Abort while the next body read is pending and check its outcome. That read
can reject even though `fetch()` already fulfilled with a successful response.
Compare cancellation before the headers arrive with an ordinary read through
the end of the body. Verify any claimed server-side effect separately.
See `src-whatwg-fetch-response-abort`.

When an existing Fetch consumer verifies the bytes of a coded response,
read the body to completion in that client. Record `Content-Encoding`,
`Content-Length`, and the number of decoded bytes the reader received.
The header can describe the encoded content while Fetch exposes decoded
bytes. Use the same content without coding as a control. If the contract
promises the encoded bytes, verify them at a capture point that observes
the encoded body. Check the bytes or digest at the representation the
contract promises. See `src-whatwg-fetch-content-coding` §4.7 and
`src-rfc-9110` §§8.4 and 8.6.

When an existing streaming HTTP API uses an optional receipt field defined
for trailers, record any initial `Trailer` declaration. Read the response
to its end with the supported client, then check which trailer fields and
values the client exposes. In a fixture, keep the declaration and content
the same while sending the optional field in one response and omitting
it in another. If the client cannot expose trailers, report receipt of
the field as unverified. Verify any claimed application outcome separately.
See `src-rfc-9110` sections 6.5 and 6.6.2.

For an existing UTF-8 NDJSON API output read incrementally, split a synthetic
fixture inside a multibyte character, across a record and between the CR and
LF bytes of a delimiter. Exercise both LF and CRLF and compare the decoded
field values, record order and count with a whole-buffer reference. Check the
consumer's result when input ends inside a record or without its required final
newline. Report any complete prefix separately from the terminal condition.
Verify any claimed application completion separately. See
`src-ndjson-specification` §§3.1–3.2 and `src-whatwg-textdecoderstream` §7.5.

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
