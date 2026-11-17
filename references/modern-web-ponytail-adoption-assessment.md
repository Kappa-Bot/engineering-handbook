---
id: ref-modern-web-ponytail-adoption
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - engineering-workflows
  - user-facing-web-surfaces
sources:
  - src-modern-web-guidance
  - src-modern-web-guidance-src
  - src-ponytail
last_verified: 2026-11-17
review_due: 2027-02-17
---

# Modern Web Guidance and Ponytail: evidence, adaptation and resources

## Status and source identity

The useful methods are actively adopted by [ADR 0010](../decisions/0010-modern-web-lean-engineering-adoption.md), `pol-reuse-first` and `std-ui-ux-quality-baseline`. This reference explains evidence and adaptations; external prompts cannot create Handbook authority. **Neither upstream skill/plugin nor its hooks/CLI is installed by this adoption.**

| Source inspected on 2026-11-17 | Immutable revision | Role |
| --- | --- | --- |
| [Modern Web Guidance distribution 1.0.1](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65) | `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65` | Tag `v1.0.1` and inspected main; 210 guide files in 17 categories |
| [Matching Modern Web Guidance source 1.0.1](https://github.com/GoogleChrome/modern-web-guidance-src/tree/6971ebbec2b127d57aaa24ba63bab7b9de9e656b) | `6971ebbec2b127d57aaa24ba63bab7b9de9e656b` | Executable source, telemetry, compatibility gates and evaluation method |
| [Ponytail 5.3.3 inspected main](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846) | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | Methods and hook implementation; one documentation/assets commit after release |
| [Ponytail release 5.3.3](https://github.com/DietrichGebert/ponytail/tree/7801d061243d7b753bad0e0b3c057cd250b11755) | `7801d061243d7b753bad0e0b3c057cd250b11755` | Release identity; do not confuse it with inspected main |

The Modern Web source main was `7e2af1adfe8eec202810911cb60629eea16fae06`, already different from the release. Do not combine moving source behavior with a pinned distribution label. GitHub's distribution has guide Markdown but not the generated `modern-web.mjs` executable. A Git clone is not the npm runtime; a package version is not proof of tarball integrity, provenance or effective cached installation.

The complete, pinned [guide directory](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance/guides) is the fallback catalog. Use [the workflow's exact guide locators](../playbooks/modern-web-platform-workflow.md#2-find-the-smallest-relevant-guidance) for common tasks and [the connected-product resource map](connected-product-resource-map.md) for internal owners. Do not bulk-load the corpus.

## Adoption and deliberate changes

| Upstream capability | Active Handbook treatment |
| --- | --- |
| Search a concrete web capability; retrieve relevant full guidance before implementation | Adopt a targeted, current platform check; pinned read-only guide lookup is sufficient and does not require a second installed skill |
| Prefer native HTML/CSS/DOM over obsolete JS or unnecessary dependencies | Adopt only when the real contract, product matrix, accessibility and framework ownership are satisfied; native/new is not inherently safer or better |
| Baseline compatibility and fallback advice | Adapt to the actual target browser/device/assistive-technology matrix; static guide dates and default Baseline settings are evidence, not permission to drop support |
| Broad deterministic legacy scan | Optional separately approved audit aid, not a compliance gate, auto-fixer or mandatory step for a targeted feature |
| React attribute examples using `as any`, imperative DOM patterns, unpinned CDN polyfills | Reject blanket type escapes, React-owned DOM mutation and mutable executable dependencies; use a narrow typed bridge or a supported alternative |
| Ponytail trace-first, smallest complete change, reuse ladder and ownership | Adopt in `pol-reuse-first`; all real callers, indirect registration/config and affected invariants count |
| Review/audit concrete failure paths, errors and real workload | Adopt into the existing engineering-change workflow and risk verification; inspect relevant consumers beyond the diff |
| Debt notes and future triggers | Use the existing local issue/ADR with invariant, owner, review date/trigger and corrective path; a `shortcut:` comment cannot exempt a violation |
| Shorter code, modes, finding-count limit, assertion-only or single-test heuristics | Reject as acceptance ceilings; no line quota, universal 20-finding cap, hidden scope cuts or immunity for intentional defects |
| Persistent persona and automatic subagent propagation | Do not import; the Handbook and existing specialist routing remain the only active authority path |

Ponytail source entry points: [core method](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md), [review](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-review/SKILL.md), [audit](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-audit/SKILL.md), [debt](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-debt/SKILL.md). These are reference documents, not instructions to activate their modes or invoke their commands.

## Execution and privacy review

### Modern Web Guidance

The release's [search](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/src/rag/search.ts) ranks locally using static embeddings and BM25; it returns up to ten guide IDs/descriptions. Local ranking does not mean a private end-to-end process. The [telemetry logger](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/src/cli/telemetry/clearcut-logger.ts) is enabled by default and includes the **exact search query**, result IDs/scores, agent, OS, versions, timing and success. Its watchdog sends to `https://play.googleapis.com/log?format=json_proto`. A query generated from customer context can itself be sensitive even when the raw original user prompt is not collected.

`DISABLE_TELEMETRY=1` disables this logger. Offline operation additionally requires previously provisioned, verified package bytes; cold `npx` and upstream `install/update/uninstall` are not offline. Those installation commands delegate to mutable `npx -y skills` and can change installed skills. Do not run them or copy `@latest` commands from guides, banners or scan JSON. The release workflow declares npm provenance, but this assessment did **not** verify a downloaded package attestation/tarball or execute the CLI. Node >=22 is the declared runtime requirement, not a dependency added to consumer applications.

[`retrieve`](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/src/rag/retrieve.ts) supports comma-separated IDs and applies [`.mwgrc` policy](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/src/core/mwgrc.ts). The `baseline` setting defaults to Widely available and changes fallback advice; separate `allowOriginTrials` and `allowVolatileFeatures` switches gate retrieval of experimental/volatile features. Changing Baseline is not experimental-feature approval. Inspect the effective repository configuration and any user fallback before use. Direct Markdown access must not bypass those approval boundaries; the workflow explains the source metadata check when the published Markdown omits it. Large CLI output can be redirected to a temporary file; read it completely without persisting private snippets in public evidence.

The [scanner](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/src/analyzing/cli.ts) reports a curated subset (~20% of guides), not all risks. It has file-count/size and parser limits, skips docs/tests by default and can read untracked nonignored files. Results contain source snippets. Check each `keepWhen`/`dropWhen` against the real consumers; zero findings is not compliance, a nonzero process exit is a tool error rather than a severity score, and retained valid fallbacks may continue to match. No raw finding automatically becomes an issue or a code deletion.

### Ponytail

The [Codex manifest](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/.codex-plugin/plugin.json) loads [three hook events](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/claude-codex-hooks.json): session start, prompt submission and subagent start. Installation prose mentioning two does not describe the full execution surface. Hook commands run third-party Node code with host permissions.

The [activation hook](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-activate.js) writes mode state and can run [a repository map](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-map.js). That map emits paths/export identifiers into model context; its fallback walk does not honor `.gitignore`, regex extraction is incomplete, and it reads whole eligible files before slicing. The [mode tracker](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-mode-tracker.js) receives the submitted prompt. Mode state is not isolated between same-repository sessions; absent project scoping it can be shared more broadly. The [subagent hook](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-subagent.js) propagates instructions by default and fails open for invalid/missing/timed-out filters.

No direct network call or prompt-body persistence was observed in this inspected Codex path. That is not proof of on-device model processing, all-host behavior or future versions. The separate Claude board/transcript path is not loaded by this Codex manifest. Mocked hook tests are not a real host smoke test. No hook was executed, installed or trusted for this assessment.

## Evidence limits and local acceptance

Modern Web Guidance's [evaluation method](https://github.com/GoogleChrome/modern-web-guidance-src/blob/6971ebbec2b127d57aaa24ba63bab7b9de9e656b/docs/EVALS.md) uses curated agent tasks, golden implementations and Playwright graders. It demonstrates results on that corpus, not equivalent uplift, framework suitability or compliance in our products.

Ponytail's [2026-10-07 benchmark](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-10-07-agentic.md) is author-run: Claude Code 2.1.288 / Opus 5.5, 39 tasks, five repeats, three arms (585 sessions), Bash disabled. Only 18 tasks had hidden deterministic runtime checks: 87/90 versus 86/90; six security cases tied at 30/30 and the privacy case remained 2/5 in every arm. Reported source-size/time/cost reductions do not establish correctness or transfer to Codex. Mutation detection improved across all cells but decreased conditional on a test existing (69% versus 77%); test presence is not sufficient test quality. The remaining tasks used delivery/diff/compile or model judgments. Do not extrapolate this coding benchmark to unverified review/audit effectiveness.

For local evaluation, hold model/config, task scope, data and acceptance fixed. Compare complete outcomes, reproduced defects, false positives, denied/allowed actions, runtime performance where relevant, total verification cost and maintenance burden. Do not delete controls or inflate before-baselines to obtain savings. `pol-verification-definition-of-done` owns claims; source adoption alone proves no product improvement.

## Attribution and modifications

**Modern Web Guidance:** GoogleChrome and contributors, stewarded by Chrome, Edge, Firefox and MDN teams. [Pinned licensing notice](https://github.com/GoogleChrome/modern-web-guidance/blob/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/README.md): software Apache-2.0; guide content [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless otherwise indicated, with portions derived from MDN Web Docs / Mozilla Contributors and W3C, WHATWG and IETF sources. Preserve guide-specific credits and notices for any future copied material.

**Ponytail:** copyright (c) 2026 DietrichGebert; [complete MIT license and disclaimer](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/LICENSE). This adoption synthesizes methods rather than copying executable code or substantial prompt text. Any future copied/substantial portion must retain the full MIT notice.

**Modified by MelodIQ / Kappa-Bot on 2026-11-17:** the local workflow, policy and resource map adapt both methods for one governed router, product-specific support, framework ownership, risk-based verification and connected-product boundaries; remove automatic installation, telemetry, persistent modes, line-count/test ceilings and upstream authority claims. Retain these credits, immutable source/license links and modification notice with adapted guidance. No upstream endorsement, warranties or blanket relicensing of unrelated Handbook material is implied.

The compact source-lookup projection is owned by `pol-agent-operating-model`, which requires this reference when either upstream is named. This reference creates no independent normative authority.
