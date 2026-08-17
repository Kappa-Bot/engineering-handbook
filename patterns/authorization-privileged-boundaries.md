---
id: pat-authorization-privileged-boundaries
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - authenticated-applications
  - multi-role-systems
  - multi-tenant-systems
sources:
  - src-owasp-authorization-cheat-sheet
  - src-owasp-authorization-regression-testing-cheat-sheet
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Authorization and Privileged Boundaries

## Intent

Keep permission decisions enforceable and testable instead of scattering them across UI conditions.

## Pattern

```text
request
  → authenticate actor/session if required
  → resolve authoritative role/claims/relationship
  → authorize action + resource
  → perform mutation/read
  → audit material privileged action where needed
  → return minimum necessary data
```

## Guidance

- Put authorization close to the protected operation/data boundary.
- Centralize reusable policy resolution where doing so reduces inconsistent checks.
- Keep role names coarse when possible; use resource/relationship attributes when a single RBAC role would become over-permissive.
- Server-side filtering MUST be applied before sensitive rows/objects are returned.
- Privileged administrative paths SHOULD be visibly distinct in code/configuration and tests.
- Service-role/admin credentials SHOULD be inaccessible to browser/client bundles.

## Regression matrix

For each protected capability, consider:

| Actor | Own resource | Other user's resource | Other tenant | Admin-only operation |
|---|---:|---:|---:|---:|
| anonymous | deny/allow explicit | deny | deny | deny |
| regular user | explicit | explicit deny | deny | deny |
| operator | explicit | explicit | explicit tenant scope | deny/explicit |
| admin | explicit | explicit | explicit scope | explicit |

The exact matrix is product-specific. The pattern is to make policy testable.

## Common failure modes

- UI hides a button but API accepts the action.
- A server endpoint checks only `isAuthenticated`.
- Object IDs can be changed to access another user's data.
- A service role is reused for ordinary user requests.
- Authorization is evaluated before canonical resource ownership is loaded.
- A new feature bypasses the old centralized policy path.

Use automated authorization regression tests when the surface is important enough to justify them.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "authz-pattern-request-resource-boundary",
      "type": "pattern",
      "text": "Resolve the authoritative actor/relationship, authorize the action plus resource at the protected boundary, then perform the operation and return only necessary data.",
      "source": "pat-authorization-privileged-boundaries",
      "covers": ["authorization", "tenant-isolation", "privilege"],
      "activate_when": ["operation:authorization", "risk:authorization", "risk:tenant-isolation", "risk:privilege"],
      "phase": ["planning", "implementation"],
      "priority": 88
    },
    {
      "id": "authz-pattern-regression-matrix",
      "type": "verification",
      "text": "Exercise allowed and denied actor/resource combinations, including other-user, other-tenant, and admin-only paths where applicable.",
      "source": "pat-authorization-privileged-boundaries",
      "covers": ["authorization", "tenant-isolation", "privilege"],
      "activate_when": ["risk:authorization", "risk:tenant-isolation", "risk:privilege"],
      "phase": ["verification"],
      "priority": 92
    }
  ]
}
```
