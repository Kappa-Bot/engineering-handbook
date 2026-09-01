from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "machine-readable/owner-authorized-role-pods.v1.json"


def parse_catalog_records(text: str) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.startswith("  - id: "):
            artifact_id = line.removeprefix("  - id: ").strip()
            current = {"id": artifact_id}
            records[artifact_id] = current
            continue
        if current is None or not line.startswith("    ") or ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        current[key] = value.strip()
    return records


def text_block_after_heading(markdown: str, heading: str) -> str:
    section_marker = f"## {heading}\n"
    if section_marker not in markdown:
        raise AssertionError(f"missing heading: {heading}")
    section = markdown.split(section_marker, 1)[1]
    if "```text\n" not in section:
        raise AssertionError(f"missing text block after heading: {heading}")
    return section.split("```text\n", 1)[1].split("\n```", 1)[0]


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
        cls.policy = (ROOT / "policies/agent-operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.catalog = (ROOT / "machine-readable/catalog.yaml").read_text(
            encoding="utf-8"
        )
        cls.catalog_records = parse_catalog_records(cls.catalog)
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
        self.assertTrue(
            self.profile["activation"]["requires_durable_authorization_reference"]
        )
        topology = self.profile["topology"]
        self.assertEqual(topology["minimum_subagent_count"], 1)
        self.assertEqual(topology["maximum_normal_subagent_count"], 2)
        self.assertEqual(
            topology["available_normal_role_ids"], ["design-quality", "delivery"]
        )
        self.assertTrue(topology["role_selection_is_plan_specific"])
        self.assertEqual(topology["maximum_concurrent_subagents"], 2)
        self.assertFalse(topology["nested_spawning"])
        self.assertEqual(topology["exceptional_maximum_subagent_count"], 3)
        self.assertFalse(topology["microtask_per_agent"])
        self.assertIn("One subagent is valid", self.standard)
        self.assertIn("Use only one pod when the second role would not save", self.playbook)

    def test_every_spawn_template_begins_with_caveman_ultra(self) -> None:
        spawn = self.profile["spawn"]
        self.assertEqual(spawn["required_prompt_prefix"], "/caveman Ultra")
        self.assertTrue(spawn["only_orchestrator_may_spawn_or_close"])
        self.assertTrue(spawn["record_actual_model_and_reasoning"])

        self.assertIn(
            "Every Kappa-Bot subagent spawn prompt under this profile MUST begin exactly:\n\n"
            "```text\n/caveman Ultra\n```",
            self.standard,
        )
        self.assertIn(
            "Each spawn prompt begins exactly:\n\n```text\n/caveman Ultra\n```",
            self.playbook,
        )

        for heading in (
            "Compact kickoff prompt",
            "Delta continuation prompt",
            "Replacement-generation prompt",
        ):
            prompt = text_block_after_heading(self.reference, heading)
            self.assertTrue(
                prompt.startswith("/caveman Ultra\n"),
                f"{heading} must start with /caveman Ultra",
            )

    def test_kickoff_packet_contains_every_required_field(self) -> None:
        prompt = text_block_after_heading(self.reference, "Compact kickoff prompt")
        for required in (
            "Logical role:",
            "Actual model/reasoning:",
            "Run manifest:",
            "Role manifest:",
            "Authority:",
            "Mission:",
            "Non-goals:",
            "Writable paths:",
            "Forbidden paths:",
            "Required verification:",
            "Handoff path:",
        ):
            self.assertIn(required, prompt)
        self.assertIn("planned_subagent_count: <1 or 2>", self.reference)
        self.assertIn("active_role_ids:", self.reference)

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

    def test_required_canonical_artifacts_are_cataloged_in_their_own_records(self) -> None:
        expected = {
            "std-owner-authorized-role-pods": "standards/owner-authorized-role-pods.md",
            "pb-owner-authorized-role-pod-execution": "playbooks/owner-authorized-role-pod-execution.md",
            "pat-durable-logical-agent-handoff": "patterns/durable-logical-agent-handoff.md",
            "ref-owner-authorized-role-manifest": "references/owner-authorized-role-manifest.md",
            "cfg-owner-authorized-role-pods": "machine-readable/owner-authorized-role-pods.v1.json",
            "adr-0004-owner-authorized-compact-role-pods": "decisions/0004-owner-authorized-compact-role-pods.md",
        }
        for artifact_id, path in expected.items():
            record = self.catalog_records.get(artifact_id)
            self.assertIsNotNone(record, artifact_id)
            self.assertEqual(record["path"], path)
            self.assertTrue((ROOT / path).is_file(), path)

    def test_default_and_opt_in_routing_clauses_are_explicit(self) -> None:
        policy_lines = self.policy.splitlines()
        self.assertIn("- Use **zero subagents by default**.", policy_lines)
        self.assertIn(
            "- Subagents MAY be used only after an explicit owner request or permitted "
            "repository-local authorization has been recorded as an unambiguous durable "
            "activation in the approved task/run manifest.",
            policy_lines,
        )

        global_lines = self.global_agents.splitlines()
        self.assertIn(
            "- Use zero subagents by default. Use them only when explicitly requested or "
            "when permitted repo-local authority genuinely benefits from independent work.",
            global_lines,
        )
        self.assertTrue(
            any(
                line.startswith("- When subagents are explicitly authorized, resolve ")
                and "OWNER_AUTHORIZED_ROLE_PODS" in line
                and "std-owner-authorized-role-pods" in line
                and "pb-owner-authorized-role-pod-execution" in line
                for line in global_lines
            )
        )

        router_section = self.router_skill.split(
            "## Owner-authorized role pods\n", 1
        )[1].split("## Context and authority discipline\n", 1)[0]
        self.assertTrue(
            router_section.lstrip().startswith("Zero subagents remains the default.")
        )
        self.assertIn(
            "explicitly and durably authorizes subagents", router_section
        )
        self.assertIn("OWNER_AUTHORIZED_ROLE_PODS", router_section)

    def test_restart_semantics_never_claim_hidden_memory_recovery(self) -> None:
        self.assertIn("generation", self.pattern)
        self.assertIn("hidden memory", self.pattern.lower())
        self.assertIn("new runtime process", self.reference.lower())
        self.assertIn("do not assume hidden-memory continuity", self.reference)


if __name__ == "__main__":
    unittest.main()
