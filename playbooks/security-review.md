---
id: pb-security-review
kind: playbook
status: active
owner: engineering
version: "0.4"
applies_to:
  - security-sensitive-changes
  - auth-changes
  - data-access-changes
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-w3c-csp3-policy-delivery
  - src-w3c-reporting-api
  - src-owasp-authorization-cheat-sheet
  - src-owasp-secrets-management-cheat-sheet
last_verified: 2026-11-21
review_due: 2027-02-19
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

### Review the actual attack surface, not only login

For the selected actors and entrypoints, include the relevant subset of:

| Boundary | Failure classes to challenge |
| --- | --- |
| Browser to server | XSS/output encoding, CSRF on state changes, CORS origin/credential configuration, CSP and browser security headers; a browser-only guard never grants access |
| HTTP/API/server action | Input/size/content-type validation, injection, broken object-level authorization, unsafe redirects, SSRF/server-side fetch, pagination and resource-exhaustion bounds |
| Session/token/identity | Session fixation, expiration/revocation, replay, MFA/recovery or account enumeration when applicable, tenant/role escalation and leaked bearer links |
| File/media/storage | Upload type/content and metadata, malware/active content risk, private object access, signed URL scope/expiry, processing isolation and deletion |
| External integration | Webhook signatures, replay/idempotency, provider response trust, retries, timeouts, least-privilege secrets and egress boundaries |
| Dependencies and automation | Actual resolved versions, known vulnerabilities/exposure, licensing and maintenance, CI token permissions, untrusted scripts/plugins/hooks |
| Operations and data | Sensitive logs/traces, backups/restore access, environment separation, rate/abuse limits, unsafe debug endpoints and failure recovery |

Do not infer an exploit from a missing file or a single scanner warning; trace the actual code path, framework defaults, deployed configuration and reachable attack scenario. Conversely, a security header in source, a green dependency scan or a hidden button is not proof that its effective boundary is safe. A finding should name the actor, input/resource, trust crossing, exploit precondition and real consequence.

For an HTTP-delivered Content Security Policy review, identify the route, environment and representation. Record the policy and relevant directives actually delivered in each observed response header. The browser enforces each `Content-Security-Policy` and monitors each `Content-Security-Policy-Report-Only`. Both can be present. Record any applicable document-level policy separately. Match existing browser evidence for a trusted, permitted user flow to the same target and policy revision. Treat earlier reports as historical telemetry. Mark current delivery or flow behavior *UNVERIFIED* wherever matching observations are missing.

When an existing CSP reporting path is in scope, treat all violation report
fields as untrusted. Correlate report details with independently observed
delivery for the reviewed route, environment, representation and policy
revision. Before displaying or retaining report data, keep only approved
fields needed for triage. Check for unnecessary URL path or query details,
referrers and violation samples. Display report values as plain text. Follow
`std-privacy-data-handling-baseline` for access and retention. See
`src-w3c-csp3-policy-delivery` §§5 and 7.5 and `src-w3c-reporting-api` §8.1.

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

For each applicable threat from the table, prove the protected boundary with a representative denied/invalid case and confirm that no forbidden side effect persisted. Test allowed paths as well: a universally denying policy is not correct authorization. Use isolated, owner-authorized fixtures and controlled inputs. A read-only audit does not authorize intrusive scanning, exploit attempts against production, changing WAF/CORS settings or executing destructive payloads.

## 6. Use external catalogs proportionally

Use OWASP ASVS 5.0.0 and applicable OWASP Cheat Sheets to challenge the design.

Do not paste the entire ASVS checklist into every PR. Select requirements that match the changed threat surface.

A [paused Platform Core implementation handoff](../references/platform-core-performance-security-handoff-2026-10-10.md)
illustrates why local per-process throttling, edge rate limiting and
authenticated authorization are separate controls. The implementation is
**not yet verified or released**; it is evidence to review, not a security
approval or an automatic WAF rule.

## 7. Verify and report

Report:

- controls actually exercised;
- negative tests executed;
- external provider/security behavior actually tested;
- unrun penetration/device/production checks;
- residual risk or accepted exception.

A passing happy path is not sufficient evidence for a security boundary.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "security-attack-surface-review",
      "type": "decision-question",
      "text": "For an app-security review, identify assets, actors, entrypoints and trust boundaries, then choose relevant OWASP ASVS 5.0.0 areas. Inspect enforceable authz/tenant checks, browser/API injection, CORS/CSP/CSRF/SSRF, tokens, uploads, external callbacks, secrets, dependencies and abuse paths only where present. Review is not exploit or edit authority.",
      "source": "pb-security-review",
      "covers": ["security-exposure"],
      "activate_when": ["archetype:security-review", "risk:security-exposure"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 100
    },
    {
      "id": "browser-csp-enforcement-evidence",
      "type": "verification",
      "force": "must",
      "text": "Record the route, environment and representation. For each observed response policy, distinguish enforced Content-Security-Policy from monitored Content-Security-Policy-Report-Only and identify the relevant directives. Both headers can coexist. Match existing browser evidence for a trusted, permitted user flow to this target and policy revision. Separate prior telemetry from current delivery and mark missing delivery or flow observations UNVERIFIED.",
      "source": "pb-security-review",
      "covers": [],
      "activate_when": [
        "archetype:browser-csp-enforcement-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 94
    },
    {
      "id": "security-review-negative-evidence",
      "type": "verification",
      "text": "Verify relevant denied and allowed paths at the real protected server/data/config boundary, including horizontal/vertical/tenant escalation, malicious inputs, replay, secrets and provider isolation where applicable. Classify unsupported scanner findings and unrun intrusive/live checks honestly; no security PASS from source scan alone.",
      "source": "pb-security-review",
      "covers": ["security-exposure"],
      "activate_when": ["archetype:security-review", "risk:security-exposure"],
      "force": "must",
      "phase": ["verification"],
      "priority": 100
    }
  ]
}
```
