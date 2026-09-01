from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "machine-readable/owner-authorized-role-pods.v1.json"


class OwnerAuthorizedRolePodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        cls.standard = (ROOT / "standards/owner-authorized-role-pods.md").read_text(
            encoding="utf-8"
        )
        cls.playbook = (
            ROOT / "playbooks/owner-authorized-role-pod-execution.md"
        ).read_text(encoding="utf-8")
        cls.pattern = (
            ROOT / "patterns/durable-logical-agent-handoff.md"
        ).read_text(encoding="utf-8")
        cls.reference = (
            ROOT / "references/owner-authorized-role-manifest.md"
        ).read_text(encoding="utf-8")
        cls.catalog = (ROOT / "machine-readable/catalog.yaml").read_text(
            encoding="utf-8"
        )
        cls.global_agents = (
            ROOT / "agent-config/codex/AGENTS.global.md"
        ).read_text(encoding="utf-8")
        cls.router_skill = (
            ROOT / "agent-config/codex/skills/engineering-handbook/SKILL.md"
        ).read_text(encoding="utf-8")

    def test_profile_is_opt_in_and_compact(self) -> None:
        self.assertEqual(
            self.profile["schema"], "owner-authorized-role-pods/v1"
        )
        self.assertEqual(
            self.profile["profile"], "OWNER_AUTHORIZED_ROLE_PODS"
        )
        self.assertFalse(self.profile["default_enabled"])
        self.assertTrue(
            self.profile["activation"][
                "requires_explicit_owner_or_repo_authorization"
            ]
        )
        topology = self.profile["topology"]
        self.assertEqual(topology["normal_subagent_count"], 2)
        self.assertEqual(
            topology["normal_role_ids"], ["design-quality", "delivery"]
        )
        self.assertEqual(topology["maximum_concurrent_subagents"], 2)
        self.assertFalse(topology["nested_spawning"])
        self.assertEqual(topology["exceptional_maximum_subagent_count"], 3)
        self.assertFalse(topology["microtask_per_agent"])

    def test_every_spawn_uses_caveman_ultra_and_actual_model_is_recorded(self) -> None:
        spawn = self.profile["spawn"]
        self.assertEqual(spawn["required_prompt_prefix"], "/caveman Ultra")
        self.assertTrue(spawn["only_orchestrator_may_spawn_or_close"])
        self.assertTrue(spawn["record_actual_model_and_reasoning"])
        for document in (self.standard, self.playbook, self.reference):
            self.assertIn("/caveman Ultra", document)

    def test_normal_roles_are_persistent_and_consolidated(self) -> None:
        roles = self.profile["roles"]
        self.assertEqual(set(roles), {
            "design-quality",
            "delivery",
            "exceptional-independent-review",
        })
        self.assertEqual(
            roles["design-quality"]["owner_default_model_alias"], "Sol"
        )
        self.assertEqual(
            roles["delivery"]["owner_default_model_alias"], "Luna"
        )
        self.assertFalse(
            roles["exceptional-independent-review"]["enabled_by_default"]
        )
        lifecycle = self.profile["lifecycle"]
        self.assertTrue(
            lifecycle["reuse_same_live_handle_for_complete_cohesive_workstream"]
        )
        self.assertFalse(lifecycle["replace_between_milestones"])
        self.assertTrue(lifecycle["durable_manifest_required"])
        self.assertTrue(lifecycle["hidden_memory_is_not_durable_state"])

    def test_single_writer_and_delta_context_rules_are_frozen(self) -> None:
        ownership = self.profile["ownership"]
        self.assertTrue(ownership["exclusive_writer_per_path"])
        self.assertTrue(
            ownership["parallel_write_heavy_work_requires_disjoint_paths"]
        )
        context = self.profile["context_efficiency"]
        self.assertTrue(context["one_complete_kickoff_packet"])
        self.assertTrue(context["subsequent_prompts_are_deltas"])
        self.assertTrue(context["reference_canonical_paths_and_shas"])
        self.assertTrue(context["route_only_applicable_skills"])

    def test_required_canonical_artifacts_are_cataloged(self) -> None:
        expected = {
            "std-owner-authorized-role-pods": "standards/owner-authorized-role-pods.md",
            "pb-owner-authorized-role-pod-execution": "playbooks/owner-authorized-role-pod-execution.md",
            "pat-durable-logical-agent-handoff": "patterns/durable-logical-agent-handoff.md",
            "ref-owner-authorized-role-manifest": "references/owner-authorized-role-manifest.md",
            "cfg-owner-authorized-role-pods": "machine-readable/owner-authorized-role-pods.v1.json",
            "adr-0004-owner-authorized-compact-role-pods": "decisions/0004-owner-authorized-compact-role-pods.md",
        }
        for artifact_id, path in expected.items():
            self.assertIn(f"- id: {artifact_id}", self.catalog)
            self.assertIn(f"path: {path}", self.catalog)
            self.assertTrue((ROOT / path).is_file(), path)

    def test_global_and_router_entrypoints_preserve_zero_default_and_route_opt_in(self) -> None:
        for text in (self.global_agents, self.router_skill):
            self.assertIn("zero subagents", text.lower())
            self.assertIn("OWNER_AUTHORIZED_ROLE_PODS", text)
            self.assertIn("std-owner-authorized-role-pods", text)
            self.assertIn("pb-owner-authorized-role-pod-execution", text)

    def test_restart_semantics_never_claim_hidden_memory_recovery(self) -> None:
        self.assertIn("generation", self.pattern)
        self.assertIn("hidden memory", self.pattern.lower())
        self.assertIn("new runtime process", self.reference.lower())
        self.assertIn("do not assume hidden-memory continuity", self.reference)


if __name__ == "__main__":
    unittest.main()
