---
id: ref-ecc-adoption-assessment
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - agent-workflows
sources:
  - src-ecc
last_verified: 2026-11-05
review_due: 2027-02-05
---

# ECC adoption assessment

## Evidence boundary

**Source:** the original [affaan-m/ECC](https://github.com/affaan-m/ECC/tree/b38be6a7f6350964d59328b52f0624e1d1d552d1), commit `b38be6a7f6350964d59328b52f0624e1d1d552d1`, inspected 2026-11-05. **Handbook comparison base:** `2f396d9e84ef2616e3ed60de33f6ff16633922b8`.

This is source inspection and applicability analysis, not execution of ECC, an independent certification, a measured benchmark or an installed consumer. GitHub stars, advertised skill counts and self-assigned scores are not acceptance evidence. The owner selected this source rather than the older WorldFlowAI re-upload; only the original is registered as `src-ecc`.

## Capability disposition

Paths below are relative to the pinned source above. `adapt` means original Handbook synthesis of the useful procedure, not vendoring the file. `learn` retains existing stronger coverage; `defer` does not authorize installation.

| Upstream capability / source path | Disposition | Existing canonical owner / outcome |
| --- | --- | --- |
| Research-first, planning, TDD and iterative retrieval (`skills/search-first`, `skills/tdd-workflow`, `skills/iterative-retrieval`) | learn | `pol-reuse-first`, `pb-engineering-change`, `std-testing-release-quality-baseline`; keep proportional planning and meaningful tests, not mandatory ceremony |
| Verification (`skills/verification-loop/SKILL.md`) | adapt | `pb-quality-release-review`; capture command completion and full change scope; local gates and target acceptance stay separate |
| Browser QA (`skills/browser-qa/SKILL.md`) | adapt | `pb-frontend-quality-review`, `pat-visual-evidence-integrity`; safe journeys and honest missing-baseline status |
| UI craft (`skills/make-interfaces-feel-better/SKILL.md`) | adapt | `pb-frontend-quality-review`; optical/content/motion checks under product-owned design authority |
| Production audit (`skills/production-audit/SKILL.md`) | learn | `pb-production-readiness-review`; blockers and missing evidence, not a 0–100 readiness score |
| Agent evaluation (`skills/agent-eval/SKILL.md`) | adapt methodology | `pb-external-solution-evaluation`; controlled comparison and observed total cost to acceptance; linked CLI is a separate dependency |
| Independent reviewer (`docs/ASTRA-REVIEW-GUIDE.md`) | learn | `std-agent-runtime-routing`, `pb-quality-release-review`; independent evidence/context without fixed model or universal reviewer |
| Context accounting (`skills/context-budget/SKILL.md`) | learn | `pol-agent-operating-model`, `std-agent-runtime-routing`; distinguish estimates from observed provider usage; preserve compact router |
| Continuous learning (`skills/continuous-learning-v2/SKILL.md`) | adapt governance only | `gov-knowledge-promotion`; reviewed, scoped lessons with evidence and retirement; no observer/daemon or automatic global promotion |
| Config security (`skills/security-scan/SKILL.md`) | learn / defer scanner | `std-dependency-supply-chain-baseline`, `pb-security-review`; scanner findings are evidence, not certification or authority to auto-fix permissions |
| MCP policy (`docs/MCP-CONNECTOR-POLICY.md`, `.mcp.json`) | learn | Choose task-relevant supported tools; do not remove existing connectors merely because ECC prefers another interface |
| Native plugin / hook runtime (`.codex-plugin/README.md`, `hooks/codex-hooks.json`) | defer execution | Review actual installed contents and permissions before enabling; registration is not successful runtime verification |
| Full catalog, legacy sync, model presets, autonomous loops | reject as defaults | Preserve the single router, Agency Agents, explicit model/effort routing, bounded correction and existing operational limits |

Language/framework recipes, marketing, logistics, healthcare and other domain skills are not a portfolio-wide import. Evaluate only if a concrete consumer needs them; existing architecture, security, data and design standards remain canonical. No medical/legal/compliance authority is inferred from an upstream skill title.

## Important findings and adaptation limits

- The verification example's secret-pattern searches are useful hints, not a sufficient security gate. Its `git diff HEAD~1` does not necessarily cover a branch, staged work or untracked files. A universal 80% coverage target and recurring 15-minute verification are not promoted.
- Browser QA has a valuable no-baseline warning. The reusable result is **absence of a comparable baseline cannot prove no regression**; it does not prevent an explicit new-design review. Fixed viewport lists, pixel tolerances and claims about percentages of WCAG coverage are not copied.
- UI craft is subordinate to tokens, semantics and measured usability. No universal blur, outline, radius formula, scale transform or animation duration is adopted. The upstream craft file also credits `linus707` / PR #1659.
- `skills/agent-eval/SKILL.md` describes a separately maintained `agent-eval` CLI; reviewing that document does not prove ECC ships that executable or authorize installing it.
- Local storage is not a guarantee of local-only analysis: `skills/continuous-learning-v2/agents/observer-loop.sh` launches Claude with read/write tools to analyze observations. Do not promise that recorded prompts/tool outputs remain on-device when a model/provider processes them. No personal histories were accessed in this assessment.
- The pinned native Codex hook manifest contains a `SessionStart` hook, not the full Claude hook set. Upstream documents explicit trust and cache/runtime checks. Verify the effective bytes and dependencies; a displayed plugin version alone is insufficient provenance.
- The MCP default and model choices are upstream environment decisions. They do not justify extra provider access, universal tool counts, disabling working integrations, or abandoning the existing runtime routing policy.

## License and maintenance

The pinned [LICENSE](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/LICENSE) is MIT, copyright 2026 Affaan Mustafa. This integration links and synthesizes rather than copying source files. Preserve the full upstream notices if substantial material is later copied/adapted; evaluate separately licensed dependencies and linked services independently.

For a future refresh, compare against this pinned revision, classify each relevant delta, verify changed claims and update the source/assessment only after review. An upstream release does not automatically strengthen a Handbook rule or change an installed environment. Reopen on a material security/runtime change, consumer failure, documented contradictory evidence or the review date.

## Validation and unknowns

Observed: source provenance/license, relevant upstream documents and existing Handbook ownership. Delivery validation belongs to the actual change's tests/CI and PR, not a static promise in this reference.

Not established: ECC execution on the owner's workstation, consumer adoption, behavioral improvement, token savings, latency reduction or cost reduction. Use the controlled comparison in `pb-external-solution-evaluation` before making those claims. `adr-0007-selective-ecc-handbook-adoption` records the authorized decision.
