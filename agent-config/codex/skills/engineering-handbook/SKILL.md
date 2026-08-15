---
name: engineering-handbook
description: Apply Kappa-Bot cross-repository engineering governance and reusable workflows for non-trivial engineering changes, new-repository bootstrap, GitHub repository lifecycle, architecture or standards decisions, reuse/search-before-build, external-solution evaluation, repository adoption, verification, UI/UX quality, responsive/mobile behavior, PWA work, visual evidence, and handbook maintenance. Do not use for trivial repo-local edits fully covered by local instructions.
---

# Engineering Handbook

Use this skill as a router into the installed Engineering Handbook references. Do not load the entire reference bundle.

## Operating sequence

1. Read the repository's applicable `AGENTS.md` and repo-local decisions first for local facts, commands, architecture, product/brand constraints and gates.
2. Identify the engineering question or workflow that actually needs cross-repository guidance.
3. Load only the relevant files under `references/`; use `references/machine-readable/catalog.yaml` to discover canonical IDs and paths when needed.
4. Apply handbook precedence rather than treating every reference as equally normative.
5. Keep external facts, internal decisions, implementation, verification, and adoption distinct when the distinction materially affects the work.
6. If an expected reference is missing or appears inconsistent with the task, report the gap rather than inventing handbook guidance.

## Routing guide

- **New repository / project bootstrap:** load `references/playbooks/new-repository-bootstrap.md`, then `references/playbooks/repository-adoption.md` and `references/templates/AGENTS.repo.md`; load stack-specific material only if it exists and is applicable.
- **GitHub repository settings / merge strategy / rulesets / archival:** load `references/playbooks/github-repository-lifecycle.md`; load Git/workspace policy only when local branch behavior is part of the question.
- **Non-trivial engineering change:** load `references/playbooks/engineering-change.md` and only the policy documents needed by the affected scope.
- **UI/UX / frontend design / visual polish:** load `references/standards/ui-ux-quality-baseline.md` and `references/playbooks/frontend-quality-review.md`; add mobile/visual-evidence patterns only when relevant.
- **PWA / installability / offline/update behavior:** load `references/standards/web-pwa-baseline.md`; add `references/patterns/mobile-responsive-interaction.md` and/or `references/patterns/visual-evidence-integrity.md` when the scope requires them.
- **Mobile keyboard / overlays / gestures / camera / safe areas:** load `references/patterns/mobile-responsive-interaction.md` plus the UI quality Standard.
- **Visual acceptance / screenshot evidence / responsive evidence:** load `references/patterns/visual-evidence-integrity.md` plus the UI quality Standard.
- **Reuse / search-before-build:** load `references/policies/reuse-first.md`.
- **External library, framework, service, design system, or reference implementation:** load `references/playbooks/external-solution-evaluation.md`, `references/governance/source-authority.md`, and `references/policies/reuse-first.md`.
- **Repository adoption / AGENTS.md design:** load `references/playbooks/repository-adoption.md` and `references/templates/AGENTS.repo.md`.
- **Git/workspace hygiene:** load `references/policies/workspace-git-hygiene.md`.
- **Verification / Definition of Done / completion claims:** load `references/policies/verification-definition-of-done.md`.
- **Architecture or durable technical decision:** load the applicable repo-local architecture first, then `references/templates/decision.md`; load `references/governance/handbook-governance.md` if precedence or exceptions are relevant.
- **Source trust, licensing, or evidence quality:** load `references/governance/source-authority.md`.
- **Promoting project learning into reusable handbook knowledge:** load `references/governance/knowledge-promotion.md`.
- **Editing the Engineering Handbook itself:** load `references/CONTRIBUTING.md`, then the governance/policy documents affected by the change.
- **Codex global or skill adoption:** load the corresponding playbook under `references/playbooks/` and the relevant ADR under `references/decisions/` if rationale is needed.

## Context discipline

- Never bulk-read `references/` merely because the skill activated.
- Prefer one playbook plus the smallest set of supporting policies/standards/patterns/governance documents that can change the decision.
- Do not copy handbook prose into repo-local `AGENTS.md`, plans, or ADRs unless a concise quotation is genuinely necessary; reference the canonical artifact instead.
- Do not turn a recommendation, Pattern, Playbook, or external source into a `MUST` unless applicable active governance/policy/standard supports that force.
- Do not use UI/PWA guidance to overwrite repo-local product identity, branding, domain workflow or deliberate architecture.

## Durable outputs

When a plan, ADR, evaluation, or review materially depends on handbook guidance, name the relevant handbook artifact IDs or paths so the reasoning remains traceable.

Keep repo-specific conclusions in the consumer repository unless `references/governance/knowledge-promotion.md` justifies deliberate promotion.
