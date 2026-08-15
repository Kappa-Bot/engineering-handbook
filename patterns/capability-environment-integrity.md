---
id: pat-capability-environment-integrity
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - multi-environment-repositories
  - demos
  - production-applications
sources:
  - src-nist-ssdf-11
  - src-github-deployment-environments
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Capability and Environment Integrity

## Intent

Allow demos, mocks, previews and staged rollouts without allowing them to impersonate production capability.

## Capability matrix

For non-trivial repositories, keep an explicit mental or documented matrix:

| Capability | Local | Demo/Preview | QA | Production |
|---|---|---|---|---|
| persistence | ? | ? | ? | ? |
| authentication | ? | ? | ? | ? |
| authorization | ? | ? | ? | ? |
| external delivery | ? | ? | ? | ? |
| billing | ? | ? | ? | ? |
| migrations | ? | ? | ? | ? |
| offline behavior | ? | ? | ? | ? |
| observability | ? | ? | ? | ? |

Only document rows that matter.

## Promotion path

A capability often evolves through:

```text
contract/scaffold
→ local/mock implementation
→ real non-production integration
→ production integration
→ hardened/operated capability
```

Do not skip evidence between stages by renaming the capability.

## Safe demo pattern

A high-quality demo MAY combine:

- mock/local domain data;
- real UI workflows;
- selected real security boundaries;
- visible demo indicators;
- explicit non-production URLs/configuration.

Make the cheap/high-value real boundary real when doing so materially reduces misleading behavior. Keep expensive/deferred systems mocked when the mock is honest.

## Production rules

Production MUST NOT:

- auto-enable demo mode when a backend fails;
- seed/reset durable data through normal release paths;
- use placeholder credentials/tokens;
- silently downgrade authorization to UI hiding;
- treat Preview secrets/config as inherited Production configuration.

See `pol-truthful-engineering`.
