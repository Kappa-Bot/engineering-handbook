from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class PromotedPolicyContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_ui_standard_requires_human_safe_errors(self):
        text = self.read("standards/ui-ux-quality-baseline.md")
        self.assertIn("### Human-safe error presentation", text)
        self.assertIn("MUST NOT render raw transport, backend, provider or internal diagnostic text as ordinary product copy", text)
        self.assertIn("recovery action", text)
        self.assertIn("observability", text)

    def test_workspace_policy_requires_persistent_branch_closure(self):
        text = self.read("policies/workspace-git-hygiene.md")
        self.assertIn("## Persistent branch allowlist and initiative closure", text)
        self.assertIn("`main` plus optional `qa`", text)
        self.assertIn("unexplained non-persistent remote branches", text)
        self.assertIn("unique work", text)

    def test_github_lifecycle_operationalizes_branch_inventory(self):
        text = self.read("playbooks/github-repository-lifecycle.md")
        self.assertIn("### Persistent branch closure gate", text)
        self.assertIn("remote branch inventory", text)
        self.assertIn("open task PRs", text)
        self.assertIn("unique commits", text)

    def test_codex_global_instructions_surface_both_defaults(self):
        text = self.read("agent-config/codex/AGENTS.global.md")
        self.assertIn("Never surface raw backend/transport/provider diagnostics as ordinary user-facing product copy", text)
        self.assertIn("persistent remote branches are `main` plus optional `qa`", text)


if __name__ == "__main__":
    unittest.main()
