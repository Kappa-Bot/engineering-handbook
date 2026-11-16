from pathlib import Path
import unittest

from automation.engineering_context.handbook_source import extract_agent_context

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
        self.assertIn("`main` is the default persistent product branch", text)
        self.assertIn("Do not create or preserve a `qa`/`staging` branch as an environment boundary", text)
        self.assertIn("Production only", text)

    def test_unslop_is_mandatory_under_the_existing_ui_owner(self):
        path = "standards/ui-ux-quality-baseline.md"
        units = {unit.id: unit for unit in extract_agent_context(self.read(path), path)}
        method = units["ui-design-reconstruction"]
        self.assertEqual(method.source, "std-ui-ux-quality-baseline")
        self.assertEqual(method.force, "must")
        self.assertEqual(set(method.phase), {"planning", "implementation", "verification"})
        self.assertEqual(method.activate_when, ("risk:design-fit",))
        # Add the normative method without displacing phase-specific design-fit coverage.
        self.assertEqual(method.covers, ())
        self.assertEqual(units["ui-visual-verification"].force, "must")
        for entry in ("agent-config/codex/AGENTS.global.md",
                      "agent-config/codex/skills/engineering-handbook/SKILL.md"):
            text = self.read(entry)
            self.assertIn("Unslop", text)
            self.assertIn("std-ui-ux-quality-baseline", text)
            self.assertIn("pb-frontend-quality-review", text)

    def test_unslop_attribution_and_supersession_are_distributed(self):
        assessment = self.read("references/unslop-adoption-assessment.md")
        decision = self.read("decisions/0009-unslop-design-reconstruction.md")
        registry = self.read("machine-readable/sources.yaml")
        catalog = self.read("machine-readable/catalog.yaml")
        pin = "620163eedb3529d9cd23a3994ed8d287d06f760d"
        for text in (assessment, decision, registry):
            self.assertIn(pin, text)
        self.assertIn("CC BY 4.0", assessment)
        self.assertIn("Modified by MelodIQ / Kappa-Bot", assessment)
        self.assertIn("Supersession map", decision)
        for source in ("ref-unslop-adoption-assessment", "adr-0009-unslop-design-reconstruction"):
            self.assertIn(source, catalog)
        bundle = self.read("agent-config/codex/skills/engineering-handbook/bundle.json")
        for directory in ("standards", "patterns", "playbooks", "references", "decisions"):
            self.assertIn('"' + directory + '"', bundle)

    def test_nine_passes_do_not_reintroduce_retired_recipes(self):
        playbook = self.read("playbooks/frontend-quality-review.md")
        self.assertIn("### Nine-pass reconstruction", playbook)
        for name in ("Spacing", "Color", "Icons", "Copy", "Typography", "Layout", "Details", "Visuals", "Motion"):
            self.assertIn(name, playbook)
        context = self.read("patterns/design-context-layering.md")
        self.assertNotIn("Adopt this pattern incrementally", context)
        self.assertIn("supersed", context.lower())
        shell = self.read("patterns/operator-console-shell-interactions.md")
        self.assertNotIn("first desktop render must start compact", shell)
        delivery = self.read("playbooks/public-client-website-delivery.md")
        self.assertNotIn("computed type-family equality", delivery)
        hero = self.read("patterns/public-marketing-hero-motion.md")
        self.assertIn("Historical", hero)
        self.assertNotIn("preserve the photo's exposure and saturation across the entire image", hero)
        self.assertNotIn("21-scene-controls-autoplay-and-owner-authority-public-websites", playbook)


if __name__ == "__main__":
    unittest.main()
