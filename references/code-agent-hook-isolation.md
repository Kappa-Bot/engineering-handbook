---
id: ref-coding-agent-hook-isolation
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to: [coding-agents, developer-workstations, agent-plugins, engineering-handbook]
sources: [src-claude-code-hooks-reference, src-cursor-hooks-reference, src-gemini-cli-hooks-reference, src-vscode-agent-hooks-reference, src-cline-hooks-reference, src-opencode-hooks-reference]
last_verified: 2026-11-20
review_due: 2027-02-20
---

# Coding-agent runtime isolation and Handbook hook compatibility

This is an interoperability reference for the existing [Handbook discovery/update playbook](../playbooks/handbook-discovery-and-update.md), not a replacement runtime policy. It records what was inspected and where local recovery can be safely attempted.

## Cross-client rule

**Engineering Handbook checks, knowledge refreshes and discovery are manual operations, not agent lifecycle gates.** They must not auto-run on prompt submission, session start/resume, model call, tool call, subagent, compaction, stop, retry, IDE launch, workspace open or plugin activation.

The rule applies regardless of host (terminal, desktop, IDE, cloud worker), vendor or agent framework. It covers only **Handbook-owned freshness/discovery/installation hooks**, not permission enforcement, sandboxing, product-specific authorization, safeguards around secrets or explicit user-requested verification. Those independent security boundaries must not be disabled in the name of restoring productivity.

An instruction file/skill can provide static guidance without running a command; reading it does not authorize registering a hook, adding an MCP server, running a package installation, changing approval settings or blocking a prompt. If knowledge is unavailable, state the limitation; don't restart or self-repair on every turn.

## Different clients, different failure and discovery contracts

| Client/harness | Relevant user/project sources | Risky event examples | Safe handling |
| --- | --- | --- | --- |
| Codex desktop/CLI/IDE | User \`~/.codex/hooks.json\`; additional user/project/managed/plugin sources resolved by the client | \`SessionStart\`, \`UserPromptSubmit\`, \`PreToolUse\` | Installed Handbook bootstrap now enrolls **zero** hooks; remove only the exact legacy bootstrap \`preflight --hook\` entries |
| Claude Code (terminal, desktop, IDE) | \`~/.claude/settings.json\`, \`.claude/settings.json\`, \`.claude/settings.local.json\`; plugins/managed sources can also participate | \`SessionStart\`, \`UserPromptSubmit\`, \`PreToolUse\`, \`Stop\` | Preserve unrelated hooks. A failure/exit-2/deny decision can alter or stop a turn; don't transplant Codex JSON output into Claude hooks |
| Cursor | \`~/.cursor/hooks.json\`, \`.cursor/hooks.json\`; plugin/team/cloud sources differ | \`beforeSubmitPrompt\`, \`beforeShellExecution\`, \`stop\` | Prompt hooks may block submission, and exit 2 can deny execution. Cloud agents do not inherit the local user file |
| Gemini CLI | \`~/.gemini/settings.json\`, \`.gemini/settings.json\`; relevant hooks nested in \`hooks\` | \`BeforeAgent\`, \`BeforeTool\`, \`AfterAgent\`, \`BeforeModel\` | Exit 2 means a block; \`BeforeAgent\` deny may discard the prompt. Never register Handbook freshness in these events |
| VS Code / GitHub Copilot | \`~/.copilot/settings.json\`, \`~/.copilot/hooks/*.json\`, \`.github/hooks/*.json\`, \`.github/copilot/settings*.json\`, plus agent-scoped, plugin and organizational controls | \`userPromptSubmitted\` / \`preToolUse\` depending on harness and version | Several sources may run together. Local setting \`chat.useHooks\` does not guarantee that the Copilot harness is disabled. Review the selected harness in \`/hooks\` |
| Cline extension/CLI | \`~/Documents/Cline/Hooks/\`, \`.clinerules/hooks/\`; CLI may use \`~/.cline/hooks/\`, \`.cline/hooks/\` | \`TaskStart\`, \`UserPromptSubmit\`, \`PreToolUse\`, \`TaskResume\` | Hook bodies are executable files, not generic JSON config entries. Inventory only; review scripts in the client and do not delete them automatically |
| Windsurf/Cascade | Known user \`~/.codeium/windsurf/hooks.json\` (JetBrains may use \`~/.codeium/hooks.json\`); \`.windsurf/hooks.json\`; managed/team hooks may differ | \`pre_user_prompt\`, \`pre_run_command\`, \`pre_write_code\` | Treat these paths as candidates, not proof of effective registration. Workspace and managed hook sources require their own review |
| OpenCode | Local packages/plugins under \`~/.config/opencode/plugins/\` or configured plugin directories; project \`.opencode/plugins/\` | V1 \`tool.execute.before\` or V2 \`session.hook("prompt")\` / \`tool.hook("execute.before")\` | Hooks are code executed by a plugin runtime, not JSON hook groups. Inventory source files; remove/disable only the exact reviewed extension through the appropriate runtime UI |

The named events are **illustrations, not a complete vendor-neutral event schema**. Client versions, remote execution, enterprise policy, installed plugins and custom agents may contribute additional sources. A developer workstation audit cannot certify an organization-managed remote agent or an app it has never inspected.

Official references: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Cursor hooks](https://cursor.com/docs/hooks), [Gemini CLI hooks](https://geminicli.com/docs/hooks/reference/), [VS Code agent hooks](https://code.visualstudio.com/docs/agent-customization/hooks), [Cline hooks](https://docs.cline.bot/customization/hooks), [OpenCode plugin hooks](https://opencode.ai/docs/build/plugins/server). Windsurf hook locations may vary by editor/integration and were partially corroborated from the client-specific documentation mirrored by community integrations; verify the installed client before touching them.

## Offline, bounded inventory and recovery

The standard-library tool [\`automation/agents/handbook_hook_audit.py\`](../automation/agents/handbook_hook_audit.py) uses **no network calls, model requests, processes or third-party packages**. It inspects a fixed list of user-level paths and only explicitly named project roots; it does **not** recursively enumerate a developer's entire home or all repositories. It does not read conversations or tool event payloads. Its result lists paths, counts and classes, never command bodies or tokens.

Run from a trusted local checkout:

\`\`\`sh
python -I automation/agents/handbook_hook_audit.py --json
python -I automation/agents/handbook_hook_audit.py --project "/path/to/workspace" --json
\`\`\`

To change a local configuration, first close the affected clients and examine the report. Then explicitly authorize removal:

\`\`\`sh
python -I automation/agents/handbook_hook_audit.py --apply --clients-stopped --json
\`\`\`

The only automatically removable entries are JSON command hooks that invoke the **exact** installed \`~/.codex/handbook-bootstrap/handbook_update.py\` with \`preflight --hook\`. All unknown Handbook-looking commands are reported, not deleted. The script backs up original bytes (user-private local \`~/.agents/handbook-hook-backups/\`), preserves unrelated keys and hooks, and checks for on-disk modification before atomic replacement. Workspace/project hooks, custom-agent hooks, scripts, plugins, managed controls, TOML, YAML, JSONC and unknown files remain **read-only**.

An extra file from an unfamiliar agent can be inspected with \`--extra-file /path/to/config.json\`; it will never be rewritten. The option \`--project\` audits a **specific** workspace only. Removing a listed user-owned hook is not the same as proving no other hook source can block. Never delete a file, wipe \`.codex\`, disable all hooks globally or loosen the user's permission/sandbox policies as a shortcut.

## How to distinguish causes of an agent stopping

1. Capture the exact lifecycle stage: prompt not admitted, model not started, tool denied, response incomplete, session resume failed, or app UI not persisting messages.
2. Inspect **resolved** hooks in the selected client/harness: user, project, custom agent, plugin, managed and remote layers. A file audit sees only what its local adapter knows.
3. If the report identifies an exact Handbook-owned legacy hook, back it up and remove it using the scoped offline tool. Leave unrelated security hooks intact.
4. Retry a harmless prompt **only when the owner wants to test**. If an agent stops again, examine the real client logs, error code, provider limits, runtime/session state and permissions. Do not assert that the Handbook caused the stop solely because an old hook existed.
5. If a code or install problem remains, keep a factual finding in the owning repository with the app/version, exact error and smallest reproduction. No consumer deployment, CI or paid services follow from this reference.

## Non-guarantees

This inventory cannot repair the private cloud agents, inaccessible enterprise-managed hooks, plugin code it cannot parse safely, arbitrary shell wrappers, or unknown future coding clients. It must mark these as **not inspected**, not silently treat them as clean. New integrations are adapter additions supported by official source review, with regressions and explicit user installation; they are never automatically enabled by a Handbook release.
