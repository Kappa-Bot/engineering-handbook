---
id: adr-0012-handbook-discovery-and-safe-preflight-update
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to: [engineering-handbook, codex, all-repositories]
sources: [src-openai-codex-hooks, src-openai-codex-skills, src-openai-codex-agents, src-openai-codex-subagents]
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Handbook Discovery 2.0 and safe pre-task updates

## Decision

The owner approved the Discovery 2.0 design and implementation on 2026-11-19, including automatic Handbook updates before Codex starts new tasks.

1. Cross-cutting triggers, repository landmarks and inspection routes have versioned declarative owners under `machine-readable/discovery/`. ES/EN evidence, negation and intent are distinct from permission. Existing complex visual-language recognizers remain tested feature extractors rather than a competing generic policy.
2. Compile the complete catalog into a local full-text discovery index and typed graph. Keep knowledge, execution and repository views distinct. Search includes documents without context projections; historical records are explicitly discoverable, not current-policy fallbacks.
3. Expose reasons, exclusions, unresolved paths and detected-risk-only coverage. Permit larger context budgets by risk and ambiguity without requiring unused tokens to be filled or truncating mandatory safeguards.
4. Replace **all active GPT-6 Luna selections** with GPT-6.1 Terra/high for bounded verified and supported visual work. Sol 6.2/high–xhigh and Astra 6.2/high–xhigh retain their substantive/complex task roles. Fallbacks require observed availability; Luna is prohibited, including fallback. This amends ADR 0011 item 3, preserving its other quality-first decisions and its historical text.
5. Enroll a workstation once into synchronous `SessionStart` (startup/resume/clear) and `UserPromptSubmit` preflights. Only the canonical HTTPS repository is fetched, into a dedicated object cache. No consumer checkout is pulled/reset, no candidate validator is executed and no new provider, GitHub Action or paid service is added.
6. Verify installed drift against a separately anchored previous manifest, require fast-forward history, validate the downloaded bundle/source-index hashes and stage recoverable activation. Pin an immutable snapshot per task. Preserve earlier snapshots and personal instructions; do not mutate the updater itself automatically.
7. Network failure may retain a verified last-known-good snapshot with `STALE_OFFLINE`. Drift, divergence, invalid manifests or an unverified first install block. Hook configuration/trust, files installed and active instruction loading are separate facts. Codex's supported local hooks are useful coordination, not a universal security or cloud enforcement boundary.

## Supersession and retained boundaries

The manual-only distribution choice in ADR 0002/0003 is superseded **for explicitly enrolled local Codex clients**. Manual PowerShell distribution remains supported. Existing instructions and those historical ADRs are not rewritten as if automatic enrollment had always existed.

Canonical authority remains in `pol-agent-operating-model`, `std-agent-runtime-routing`, source-authority governance and repository-local decisions. The discovery registry is executable mapping data, not an independent normative document. The operational owner is `pb-handbook-discovery-and-update`.

## Trust and limitations

HTTPS, Git object integrity, fast-forward checks and file hashes are not signed-release verification. Automatic updates deliberately trust the owner's canonical repository. A compromised maintainer or an attacker able to rewrite the same user's bootstrap/state is outside this mechanism's protection. The stable bootstrap requires an explicit reviewed reinstall for upgrades.

Codex client support and hook trust must be observed on each workstation. A Handbook commit does not install hooks, change a machine's model allowlist or retroactively reload a session. Preserve and explicitly reconcile customized `AGENTS.md`/non-empty `AGENTS.override.md`; the updater never silently overwrites them.

## Verification

Regression cases cover positive, negative, ambiguous and mixed tasks; catalog-wide search; typed graph validity; real paths; compiled freshness; safe Git ancestry; immutable snapshots; offline fallback; drift; path/symlink rejection; lock/activation recovery; hook preservation and portable bundle execution. Native Windows/Codex hook adoption remains a separate workstation acceptance gate.
