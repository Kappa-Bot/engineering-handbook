# Handbook Discovery 2.0

Status: approved by the owner in the 2026-11-19 implementation request.

## Outcome and boundaries

Make engineering guidance discoverable by task, actual repository paths and explicit reasons. Replace active GPT-6 Luna routes with GPT-6.1 Terra; preserve historical decisions. Use higher reasoning and context budgets according to risk, not indiscriminate maximum effort. No new hosted service, paid tier, GitHub Actions execution, consumer-repository refactor or extra Git worktree is required.

## Architecture

1. A versioned declarative registry owns cross-cutting task triggers, ES/EN aliases, negative conditions and repository landmarks. Complex existing visual-language recognizers remain named, tested feature extractors, not a second generic routing policy. Rules produce provenance; absence of a match is not evidence of safety.
2. A compiled catalog-wide local search index includes canonical documents without embedded context units. Knowledge, execution and repository trees share stable IDs. Typed edges distinguish prerequisites, related guidance and supersession. Invalid references and dependency cycles fail validation.
3. `context`, `search`, `tree`, `explain` and `doctor` expose progressive disclosure, actual paths, exclusions, unresolved landmarks and coverage limitations. Repository discovery does not read commercial facts or secret contents. Token budgets expand with risk and uncertainty; mandatory safeguards are never truncated.
4. A standalone Python bootstrap performs synchronous preflight updates from the canonical HTTPS repository before new Codex tasks. It uses a dedicated object cache, verifies fast-forward history and bundle integrity, stages activation, detects installed drift against the previous manifest and retains a recoverable previous snapshot. It never resets a consumer checkout or overwrites user instructions. Network failure permits only an intact last-known-good snapshot with an explicit stale status.
5. Installation merges owned SessionStart/UserPromptSubmit hooks without replacing other hooks. Hook support/trust and session instruction loading remain client responsibilities. The hook supplies fresh-baseline reading instructions; updating files does not claim to retroactively reload session policy. The stable bootstrap is not silently self-updated. HTTPS and fast-forward checks are not signature verification.

## Acceptance

- No active runnable route selects GPT-6 Luna, including fallback routes.
- Bilingual, negative, mixed-domain and ambiguous requests have regression coverage. Review and observation never imply authorization to modify or deploy.
- All catalog documents are searchable; trees and explanations use real IDs/paths and stable ordering. Graph, stale-output and invalid-registry errors are actionable.
- Installer/updater tests cover offline fallback, drift, invalid paths, remote/history checks, locking, rollback and preservation of user-owned configuration.
- Final source/corpus tests, compiled freshness, integrity and independent security review are observed before publication. Workstation adoption is reported separately from code publication.
