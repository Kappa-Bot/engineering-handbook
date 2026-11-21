---
name: engineering-handbook
description: Use for Kappa-Bot repository engineering, Codex/subagent invocation and model routing, architecture/data, security, testing/release, APIs, UI/UX/PWA, connected products, marketing/SEO or Handbook maintenance; especially when task triggers, applicable guidance, repository owners or verification gates are unclear.
---

# Engineering Handbook

One generic router, with progressive disclosure. Canonical Markdown and permitted repository decisions own authority; generated indexes and classifications do not grant permission.

## Before a new task

1. Read applicable repository `AGENTS.md` and local decisions. Respect the actual instruction hierarchy.
2. Use the already-installed local Handbook snapshot or the deliberately selected manual update revision for the **whole task**, including delegated work. Read its `references/agent-config/codex/AGENTS.global.md` when available. Do not switch versions mid-task or trigger a refresh on delegation.
3. Automatic Handbook hooks are **disabled across coding agents**, including Codex, Claude Code, Cursor, Gemini CLI, Copilot/VS Code, Windsurf, Cline, OpenCode and other harnesses. Session starts, prompts, model/tool calls, continuations, plugins, stop/retries and subagents must not update or gate work. See `ref-coding-agent-hook-isolation` for provider differences and offline audit. The root parent may run `handbook-bootstrap/handbook_update.py doctor` or `preflight` **manually and explicitly**, never as an automatic task-start step. Follow `pb-handbook-discovery-and-update` for supported commands. Preserve user hooks and installed data; no consumer repo, personal settings or agent configuration is silently rewritten.
4. An invalid source, drift or manifest **stops only an explicitly requested manual update**, not Codex. Manual checks return nonzero on failure; no hook is installed and no automatic check runs. Use a last-known-good snapshot only when its integrity was verified; disclose unverified freshness and never claim compliance or publication checks passed without evidence. Emergency recovery uses the offline `rescue-hooks` command in `pb-handbook-discovery-and-update`, without deleting chats, disabling unrelated hooks or changing consumer repositories.
5. Trivial work can proceed under the current baseline and local authority without a context-query ceremony.

## Find guidance and actual files

For non-trivial, risky, ambiguous or cross-cutting work, run from the selected snapshot's `references/` directory and pass the consumer's absolute path:

```sh
python -m automation.engineering_context context --repo "<repo-root>" --handbook machine-readable/compiled --mode plan --task "<task>" --metrics
python -m automation.engineering_context explain --root . --repo "<repo-root>" --task "<task>" --pretty
python -m automation.engineering_context search --root . --query "<question or terms>" --pretty
python -m automation.engineering_context tree --root . --kind knowledge --pretty
python -m automation.engineering_context tree --root . --kind execution --pretty
python -m automation.engineering_context tree --root . --kind repository --repo "<repo-root>" --task "<task>" --pretty
python -m automation.engineering_context doctor --root . --repo "<repo-root>" --pretty
```

- Add repeated `--changed <path>` when known. A reviewed diff can require migration safeguards without authorizing execution.
- Use `descriptor`, `repo_route`, `capsule`, `discovery` and `planning_ir_seed`. `explain` exposes matched/negated rules, unit selection, exclusions and unresolved landmarks.
- Ranked reads keep `path` as the canonical catalog path. Use `local_availability` to open a local file from the selected `handbook-root` or find the relocated `SKILL.md` in the containing `skill-root` when its manifest entry and digest match. Checkout-only entries remain discoverable and show as unavailable. Read the applicable source for authority.
- CLI JSON uses Unicode escapes on legacy output encodings so ASCII-compatible text pipes retain all characters. A shell may re-encode redirected output when saving it.
- Search covers the full catalog, including pages without context units. ES/EN topic aliases supplement lexical ranking. Use `--historical` only for decision history, never as a current-policy fallback.
- `needs-discovery`, `needs-resolution`, uncovered risks and unresolved paths require targeted inspection. Empty coverage is **not** a safety PASS. The classifier is bounded language analysis, not an authorization engine.
- Read complete relevant canonical guidance when exact rules or unresolved decisions require it. Never truncate safeguards to satisfy an advisory budget.
- Re-run with `--mode implement` or `--mode verify` when scope/risk changes; use `--base-context` for deltas. Classification, prerequisite guidance, model choice and permission remain separate decisions.
- If the runtime is unavailable, use `references/machine-readable/catalog.yaml` and the topic map in `references/machine-readable/discovery/taxonomy.v1.json`; do not maintain a second hand-written domain router in this skill.

## Delegation and invocation

`pol-agent-operating-model` and `std-agent-runtime-routing` own the gate and model/reasoning effort matrix. Use `pb-agent-runtime-routing` for invocation, `ref-agency-agents-specialist-routing` for Agency Agents personas, and `ref-agent-runtime-manifest` for durable worker state when warranted.

Zero workers is the ordinary baseline unless applicable higher-priority instructions, repository/skill policy or explicit user direction activate delegation. A persona match alone is not sufficient. Choose deterministic tooling, direct work, one useful specialist, then a second worker only for distinct parallel value or required independence. Routine limit: two workers, no nested spawning by default.

Use available Terra 6.1/high for bounded verified work and visual/browser tasks; Sol 6.2/high for substantive engineering, Sol/xhigh for difficult integration, and Astra 6.2/high–xhigh for demanding architecture/security/data reasoning. **Never select GPT-6 Luna, including as a fallback.** On observed Terra unavailability, use the Standard's available Sol fallback; never silently substitute. `max` is evidence-gated; more tokens do not authorize extra monetary charges, new providers or GitHub Actions.

Set model **and reasoning effort** explicitly where the actual tool supports overrides. Inspect native custom-agent TOML and the client allowlist; native agent types are not Agency personas, and CLI configuration is not Responses/Agents API configuration. Record requested and observed settings; use `NOT_OBSERVED` rather than inventing effective values. Some tools require isolated context to override model/effort: follow their real schema, not a universal spawn payload. Escalate by cause, not an automatic model ladder.

Independent review follows the Standard's security/data/money/production/contracts/concurrency/high-impact risk gates. Tests and controller diff inspection can suffice for strongly verified low/medium-risk work. The implementation author is not its own independent reviewer.

## Product and skill boundaries

Code authoring, refactoring, variable/module renaming, folder reorganization and dependency selection resolve through `std-code-quality-organization-baseline`, `pb-code-change-workflow` and the existing `std-dependency-supply-chain-baseline`; no universal language style, folder layout or package choice. `archetype:code-change`, `archetype:code-organization` and `archetype:dependency-selection` provide scoped ES/EN routing and real repo landmarks. Review, negated operations and package evaluation do not grant edit/install authority.

Holistic UX/UI/performance/security/privacy/reliability reviews enter via `pb-engineering-quality-audit` and its existing owners, not a universal checklist. Focused ES/EN quality archetypes select the real UI/interaction, security/config, personal-data lifecycle, SQL/performance or runtime evidence paths. `std-privacy-data-handling-baseline` covers personal-data engineering in internal CRMs, apps and agents; public Spanish websites additionally use their existing legal/trust Standard. A read-only audit does not authorize remediation, redesign, intrusive scans, issue creation, load tests, provider changes or release. Missing rendered/negative/remote/native evidence is incomplete and must be reported.

Use the smallest relevant process/craft skill set. Product-specific architecture, brands and provider choices remain local. Material visual work uses Unslop under `std-ui-ux-quality-baseline`, `pat-design-context-layering` and `pb-frontend-quality-review`. Resolve `pat-visual-direction-catalog` for actual material direction: scoped Glassmorphism **starting default only for new/authorized internal consoles without a local choice**, Neumorphism/solid selectable, no live style picker. Resolve `pat-operator-console-shell-interactions` separately for shell mechanics after local `DESIGN.md`. Audits and narrow fixes do not authorize reconstruction. Modern Web Guidance/Ponytail are source methods with pinned local assessments, not automatically installed plugins. Patterns, playbooks and external references cannot silently gain normative force.

## Maintaining the Handbook

Edit canonical owners and versioned registries, add positive/negative/mixed regression cases, and register new artifacts in the catalog. Regenerate and validate:

```sh
python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled
python -m automation.engineering_context check --root .
python -m automation.engineering_context doctor --root .
python -m unittest discover -s tests/engineering_context -p 'test_*.py'
```

Keep substantive source change, generated bundle, installed files, hook trust, active-session instructions and observed model availability as distinct evidence states. See `pb-handbook-discovery-and-update` for installation, rollback and failure recovery.
