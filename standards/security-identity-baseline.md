---
id: std-security-identity-baseline
kind: standard
status: active
owner: engineering
version: "0.4"
applies_to:
  - applications
  - services
  - authenticated-surfaces
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-owasp-authorization-cheat-sheet
  - src-owasp-authentication-cheat-sheet
  - src-owasp-secrets-management-cheat-sheet
  - src-rfc-5869-hkdf
  - src-rfc-6265-cookie-scope
  - src-rfc-7519-jwt-time-claims
last_verified: 2026-11-21
review_due: 2027-02-15
---

# Security and Identity Baseline

## Purpose

Define the cross-repository minimum for identity, authorization, privileged operations, secrets and sensitive workflows without prescribing one identity provider, database, cloud or authorization library.

Security controls MUST exist at the boundary that actually protects the resource. UI composition is not a security boundary.

## 1. Authentication and authorization are distinct

Authentication establishes identity. Authorization decides whether that identity may perform an action on a resource.

Authenticated users MUST NOT be assumed authorized merely because they can reach a route, render a component or possess a valid session.

Sensitive reads and mutations MUST validate authorization at a server/data boundary that cannot be bypassed by modifying the client.

## 2. Deny by default and least privilege

When access is not explicitly permitted, protected operations SHOULD deny.

Privileges MUST be scoped to the smallest practical actor, resource, environment and duration.

Administrative/service credentials MUST NOT be exposed to client code or user-controlled execution contexts.

Do not widen a role merely to make implementation easier without reviewing the resulting access.

## 3. Validate authorization on every protected request

Protected object access and mutations MUST validate permission in the authoritative execution path.

Do not rely solely on:

- hidden navigation;
- disabled buttons;
- client role state;
- guessed-unlikely identifiers;
- obscured URLs;
- frontend filters.

Authorization logic SHOULD have automated regression coverage for horizontal escalation, vertical escalation and tenant/data-isolation risks where applicable.

## 4. Identity sources and local profiles

If an external identity provider is authoritative, local user/profile tables are derived application state unless explicitly designed otherwise.

Local snapshots MUST NOT silently override provider identity/security state without a deliberate contract.

Sensitive account lifecycle changes SHOULD have clear reconciliation behavior.

## 5. Secrets and privileged credentials

Secrets MUST:

- stay out of committed source and ordinary logs;
- be stored in an appropriate secret/configuration mechanism;
- be visible only to actors/jobs that need them;
- have a rotation/revocation path proportional to risk;
- not be copied into client-visible variables or bundles;
- not be printed merely to debug configuration.

CI/CD credentials SHOULD prefer short-lived/federated mechanisms where the platform supports them and the added setup is justified.

For a protocol that already uses HKDF to derive purpose-specific keys,
verify the exact bytes passed as `info`. Check the selected implementation
against a public test vector. With synthetic input key material, hold the
other inputs fixed, repeat one context and compare the expected results for
distinct documented purposes or versions. Check the bytes that encode the
context before comparing the outputs. Record test inputs and result
fingerprints from the synthetic fixture. See `src-rfc-5869-hkdf` §3.2 and Appendix A.

## 6. Tokens, access links and one-time credentials

Bearer-like links/tokens MUST be treated as credentials.

Where recovery of the raw value is not required, storing a verifier/hash rather than the raw token SHOULD be preferred.

Tokens/links SHOULD have, according to risk:

- sufficient entropy;
- bounded scope;
- expiration or revocation semantics;
- safe transport;
- no accidental logging/analytics capture;
- explicit rotation/reissue behavior.

Do not claim revocation when only a local/client representation is removed.

For a verifier that already uses signed JSON Web Tokens (JWT) with time claims,
use a fixed test clock and check immediately before, at and after each
applicable `nbf` or `exp` boundary. With zero clock tolerance, the `nbf`
boundary is included and the `exp` boundary is excluded. If the verifier
configures a bounded clock tolerance, check the effective acceptance window
under that policy. Record the tolerance and the configured signature and
claim verification outcome. See `src-rfc-7519-jwt-time-claims` §§4.1.4–4.1.5.

See `pat-token-secret-link-handling`.

## 7. Sensitive operations

Operations with elevated consequence SHOULD require stronger confirmation/re-authentication/authorization proportional to risk.

Examples:

- changing privileged identity/access;
- billing/financial actions;
- destructive data operations;
- production configuration;
- secret rotation;
- exports of sensitive data.

## 8. Abuse and automation

Public or high-value mutation surfaces SHOULD consider rate limiting, anti-automation, replay protection, idempotency or additional verification based on the actual abuse model.

Do not add CAPTCHA/Turnstile or similar controls mechanically to every form.

## 9. Security failures are explicit

Authorization, integrity or external-security failures MUST fail safely.

Do not convert a security failure into a successful-looking local fallback.

Apply `pol-truthful-engineering`.

## 10. Security verification

Verification depth is proportional to risk, but material auth/authz changes SHOULD include:

- unit/integration tests for policy logic;
- negative tests, not only allowed-path tests;
- cross-role/cross-tenant/object-access cases where relevant;
- secret/client-bundle review;
- real boundary testing for critical flows when practical.

OWASP ASVS 5.0.0 is the preferred application-security verification catalog; use applicable requirements rather than treating the whole standard as a mandatory checklist for every repo.

For a browser sign-out flow that already expires a session cookie, record the
delivered `Set-Cookie` expiry and inspect browser storage before and after
on the affected supported routes. Match the cookie name, effective domain
and path, including host-only scope where applicable. Verify removal of the
intended entry and expected behavior of any same-name entries in other scopes.
Redact cookie values. Record server-side session invalidation separately when
claimed. See `src-rfc-6265-cookie-scope` §§3.1, 4.1.2 and 5.3.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "security-authorization-boundary",
      "type": "decision-question",
      "text": "Where is authorization for the affected action and resource enforced at an authoritative server or data boundary?",
      "source": "std-security-identity-baseline",
      "covers": ["authorization", "tenant-isolation", "privilege"],
      "activate_when": ["operation:authorization", "risk:authorization", "risk:tenant-isolation", "risk:privilege"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 100
    },
    {
      "id": "security-authorization-negative-cases",
      "type": "verification",
      "text": "Verify denied paths and cross-role, cross-tenant, or object-access cases that are relevant to the changed authorization boundary.",
      "source": "std-security-identity-baseline",
      "covers": ["authorization", "tenant-isolation", "privilege"],
      "activate_when": ["operation:authorization", "risk:authorization", "risk:tenant-isolation", "risk:privilege"],
      "force": "should",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "security-credential-lifecycle",
      "type": "decision-question",
      "text": "What scope, expiration or revocation, transport, storage, and reissue semantics protect the affected bearer credential?",
      "source": "std-security-identity-baseline",
      "covers": ["credential"],
      "activate_when": ["risk:credential"],
      "force": "should",
      "phase": ["planning", "implementation"],
      "priority": 100
    },
    {
      "id": "security-credential-verification",
      "type": "verification",
      "text": "Verify the credential lifecycle and that privileged or raw credentials are not exposed through client code or ordinary logs.",
      "source": "std-security-identity-baseline",
      "covers": ["credential"],
      "activate_when": ["risk:credential"],
      "force": "should",
      "phase": ["verification"],
      "priority": 95
    }
  ]
}
```
