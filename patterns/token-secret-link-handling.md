---
id: pat-token-secret-link-handling
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - bearer-tokens
  - access-links
  - api-secrets
  - qr-credentials
sources:
  - src-owasp-secrets-management-cheat-sheet
  - src-owasp-authentication-cheat-sheet
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Token, Secret and Access-Link Handling

## Intent

Treat any value that grants authority as a credential, even when it looks like a URL, QR code, API key or temporary invite.

## Classify first

Before implementation, decide whether the value is:

- public identifier;
- opaque lookup key;
- bearer credential;
- one-time credential;
- revocable access link;
- long-lived API secret;
- signing/encryption key.

Do not give public-identifier handling to bearer credentials.

## Storage

If the server only needs to verify a presented random token and does not need to recover the original, prefer storing a cryptographic verifier/hash.

If the raw value must be recovered, use an appropriate secrets/encrypted-storage design instead of pretending hashing is reversible.

## Lifecycle

Define:

- creation source/entropy;
- scope;
- expiry;
- revocation;
- rotation/reissue;
- logging/redaction;
- leak response.

High-value long-lived credentials deserve more rigorous lifecycle automation than low-risk temporary links.

## Transport and observability

Credentials MUST NOT be intentionally included in:

- source control;
- analytics payloads;
- error messages;
- normal logs;
- screenshots/evidence unless explicitly redacted.

Be cautious with URL credentials because browser history, referrers, screenshots and monitoring can create secondary copies.

## CI/CD

Secrets exposed to CI MUST be scoped to the minimum jobs/environments that need them.

Prefer environment-protected or short-lived credentials where available.

Do not run untrusted code with production secrets.

## Lost credential

A lost bearer link/token is normally reissued/rotated, not reconstructed from a stored hash.

If product UX requires recovery, design that recovery explicitly rather than weakening storage semantics.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "token-classify-authority-value",
      "type": "decision-question",
      "text": "Classify the value as public identifier, opaque lookup key, bearer or one-time credential, revocable access link, API secret, or signing/encryption key before choosing storage and transport semantics.",
      "source": "pat-token-secret-link-handling",
      "covers": ["credential"],
      "activate_when": ["risk:credential"],
      "phase": ["planning"],
      "priority": 96
    },
    {
      "id": "token-hash-when-verification-only",
      "type": "pattern",
      "text": "When the server only needs to verify a presented random token and does not need to recover it, prefer storing a cryptographic verifier or hash rather than the raw token.",
      "source": "pat-token-secret-link-handling",
      "covers": ["credential"],
      "activate_when": ["risk:credential"],
      "phase": ["implementation"],
      "priority": 86
    },
    {
      "id": "token-no-credential-leak",
      "type": "constraint",
      "text": "Do not intentionally place credentials in source control, analytics payloads, error messages, normal logs, or unredacted screenshots and evidence.",
      "source": "pat-token-secret-link-handling",
      "covers": ["credential"],
      "activate_when": ["risk:credential"],
      "force": "must-not",
      "phase": ["implementation", "verification"],
      "priority": 100
    }
  ]
}
```
