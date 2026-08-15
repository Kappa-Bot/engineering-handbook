---
id: pb-security-review
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - security-sensitive-changes
  - auth-changes
  - data-access-changes
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-owasp-authorization-cheat-sheet
  - src-owasp-secrets-management-cheat-sheet
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Security Review

Use for changes affecting identity, permissions, secrets, sensitive data, external callbacks/webhooks, production credentials or privileged workflows.

## 1. Identify the protected asset

State what can be harmed:

- account;
- tenant data;
- money/billing;
- privileged operation;
- secret;
- production environment;
- integrity/history;
- availability.

## 2. Identify actors and trust boundaries

List only actors relevant to the change:

- anonymous;
- authenticated user;
- operator/admin;
- service/automation;
- external provider;
- CI/deployment job.

Mark where untrusted input crosses into a trusted execution/data boundary.

## 3. Separate AuthN from AuthZ

Answer:

- how identity is established;
- where authorization is evaluated;
- what resource relationship matters;
- whether client state can bypass the decision.

## 4. Review privileged credentials

For every privileged key/token/role:

- where is it stored?
- where can it execute?
- can the browser/client see it?
- what is its blast radius?
- how is it rotated/revoked?
- can logs expose it?

## 5. Negative-path review

Test attempts that SHOULD fail:

- wrong role;
- wrong resource owner;
- wrong tenant;
- expired/revoked token;
- missing signature/secret;
- replay/duplicate where relevant;
- malformed/untrusted input;
- production operation from the wrong environment.

## 6. Use external catalogs proportionally

Use OWASP ASVS 5.0.0 and applicable OWASP Cheat Sheets to challenge the design.

Do not paste the entire ASVS checklist into every PR. Select requirements that match the changed threat surface.

## 7. Verify and report

Report:

- controls actually exercised;
- negative tests executed;
- external provider/security behavior actually tested;
- unrun penetration/device/production checks;
- residual risk or accepted exception.

A passing happy path is not sufficient evidence for a security boundary.
