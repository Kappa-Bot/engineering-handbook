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

    def test_profile_is_opt_in_and_two_role_only(self) -> None:
        self.assertEqual(self.profile["schema"], "owner-authorized-role-pods/v1")
        self.assertEqual(self.profile["profile"], "OWNER_AUTHORIZED_ROLE_PODS")
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
        self.assertEqual(topology["maximum_subagent_count"], 2)
        self.assertEqual(
            topology["available_role_ids"], ["design-quality", "delivery"]
        )
        self.assertTrue(topology["role_selection_is_plan_specific"])
        self.assertEqual(topology["maximum_concurrent_subagents"], 2)
        self.assertFalse(topology["nested_spawning"])
        self.assertFalse(topology["third_subagent_allowed"])
        self.assertFalse(topology["microtask_per_agent"])
        self.assertIn("One subagent is valid", self.standard)
        self.assertIn("No third subagent role exists", self.standard)
        self.assertIn("Use only one pod when the second role would not save", self.playbook)

    def test_every_spawn_template_begins_with_caveman_ultra(self) -> None:
        spawn = self.profile["spawn"]
        self.assertEqual(spawn["required_prompt_prefix"], "/caveman Ultra")
        self.assertTrue(spawn["only_orchestrator_may_spawn_or_close"])
        self.assertTrue(spawn["record_actual_model_and_reasoning"])
        self.assertTrue(spawn["record_requested_model_and_reasoning"])
        self.assertTrue(
            spawn["fallback_requires_existing_authorization_and_cost_compliance"]
        )

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
            "Requested model/reasoning:",
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
            "Continuation/cost authority:",
        ):
            self.assertIn(required, prompt)
        self.assertIn("planned_subagent_count: <1 or 2>", self.reference)
        self.assertIn("active_role_ids:", self.reference)

    def test_owner_default_model_routing_is_frozen(self) -> None:
        orchestrator = self.profile["orchestrator"]
        self.assertEqual(orchestrator["owner_default_model_alias"], "Sol 6.1")
        self.assertEqual(orchestrator["owner_default_reasoning"], "high")

        roles = self.profile["roles"]
        self.assertEqual(set(roles), {"design-quality", "delivery"})
        self.assertEqual(
            roles["design-quality"]["owner_default_model_alias"], "Astra 6"
        )
        self.assertEqual(
            roles["design-quality"]["owner_default_reasoning"], "xhigh"
        )
        self.assertEqual(roles["delivery"]["owner_default_model_alias"], "Luna 6")
        self.assertEqual(roles["delivery"]["owner_default_reasoning"], "xhigh")
        self.assertFalse(roles["design-quality"]["implementation_diff_author"])
        self.assertTrue(roles["delivery"]["implementation_diff_author"])

        for document in (
            self.policy, self.playbook, self.global_agents, self.router_skill
        ):
            for expected in ("Sol 6.1 high", "Astra 6 xhigh", "Luna 6 xhigh"):
                self.assertIn(expected, document)
            self.assertNotIn("Terra ultra", document)
            self.assertNotIn("Sol 6.1 xhigh", document)
        self.assertIn("`Sol 6.1`, reasoning `high`", self.standard)
        self.assertIn("`Astra 6`, reasoning `xhigh`", self.standard)
        self.assertIn("`Luna 6`, reasoning `xhigh`", self.standard)
        self.assertIn("requested_model: Sol 6.1", self.reference)
        self.assertIn("requested_reasoning_effort: high", self.reference)
        self.assertIn("Astra 6 xhigh", self.reference)
        self.assertIn("Luna 6 xhigh", self.reference)

    def test_low_communication_budget_is_global_to_role_pods(self) -> None:
        communication = self.profile["communication"]
        self.assertTrue(communication["repository_over_conversation"])
        self.assertFalse(communication["direct_subagent_to_subagent"])
        self.assertEqual(
            communication["target_parent_dispatches_per_role_per_megaplan"], 1
        )
        self.assertEqual(communication["target_total_transmissions_per_role_per_megaplan"], 2)
        self.assertEqual(communication["hard_max_transmissions_per_role_per_megaplan"], 3)
        self.assertTrue(
            communication["third_transmission_requires_material_blocker_or_authority_delta"]
        )
        self.assertFalse(communication["progress_chatter"])
        self.assertTrue(communication["deltas_only_after_initial"])
        self.assertIn("one parent dispatch", self.standard.lower())
        self.assertIn("hard ceiling of three", self.playbook.lower())

        compatibility = json.loads(
            (ROOT / "machine-readable/owner-authorized-two-agent-low-comms.v1.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(
            compatibility["inherits_from"],
            "machine-readable/owner-authorized-role-pods.v1.json",
        )
        for limits in (communication, compatibility["communication"]):
            for safeguard in (
                "hard_max_applies_to_routine_transmissions_only",
                "necessary_safety_and_required_review_exceptions_allowed",
                "exceptions_require_durable_reason_and_observed_count",
                "message_budget_must_not_skip_gates_or_stop_executable_work",
            ):
                self.assertTrue(limits[safeguard], safeguard)
        self.assertTrue(
            self.profile["review"][
                "required_corrective_review_must_not_be_skipped_for_message_budget"
            ]
        )

    def test_exhaustive_execution_is_bounded_and_does_not_stop_at_checkpoints(self) -> None:
        execution = self.profile["execution"]
        for required in (
            "exhaustive_mode_requires_owner_authorization",
            "continue_until_authorized_feasible_scope_exhausted",
            "checkpoints_are_recovery_boundaries_not_stop_points",
            "blocked_dependency_does_not_stop_independent_work",
            "mandatory_evidence_still_blocks_its_gate",
            "respect_enforced_runtime_context_and_quota_limits",
            "forced_interruption_requires_durable_next_action",
        ):
            self.assertTrue(execution[required], required)
        for prohibited in (
            "routine_reapproval_required",
            "unrelated_scope_expansion_allowed",
            "background_or_unlimited_runtime_claims_allowed",
        ):
            self.assertFalse(execution[prohibited], prohibited)
        self.assertIn("## Authorized exhaustive execution and zero incremental cost", self.standard)
        self.assertIn("exhaustive_continuation_authorized:", self.reference)

    def test_zero_incremental_cost_includes_overages_and_uncertain_actions(self) -> None:
        cost = self.profile["cost_controls"]
        self.assertTrue(cost["applies_when_owner_requires_zero_incremental_cost"])
        self.assertEqual(cost["currency"], "EUR")
        self.assertEqual(cost["maximum_incremental_monetary_cost"], 0)
        self.assertFalse(cost["paid_upgrades_topups_or_separately_billed_api_calls_allowed"])
        self.assertFalse(cost["new_chargeable_resources_or_billable_overages_allowed"])
        for required in (
            "existing_service_is_not_proof_of_free_incremental_usage",
            "verify_included_entitlement_and_remaining_allowance_before_metered_action",
            "unknown_incremental_cost_blocks_that_action_only",
            "never_change_billing_limits_to_continue",
            "distinguish_cost_ceiling_from_observed_billing_evidence",
        ):
            self.assertTrue(cost[required], required)
        self.assertIn("incremental_cost_ceiling_eur:", self.reference)
        self.assertIn("billing_evidence:", self.reference)

    def test_normal_roles_are_persistent_and_consolidated(self) -> None:
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
        self.assertTrue(context["discover_actual_skills_mcp_cli_auth_and_permissions"])
        self.assertTrue(context["repository_test_commands_remain_authoritative_gates"])
        self.assertTrue(context["avoid_duplicate_cli_and_mcp_actions"])
        self.assertTrue(context["avoid_busy_polling_and_repeated_full_discovery"])

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
        self.assertTrue(
            any("Sol 6.1 high" in line and "Astra 6 xhigh" in line and "Luna 6 xhigh" in line for line in global_lines)
        )

        router_section = self.router_skill.split(
            "## Owner-authorized role pods\n", 1
        )[1].split("## Context and authority discipline\n", 1)[0]
        self.assertTrue(router_section.lstrip().startswith("Zero subagents remains the default."))
        self.assertIn("explicitly and durably authorizes subagents", router_section)
        self.assertIn("OWNER_AUTHORIZED_ROLE_PODS", router_section)
        self.assertIn("Astra 6", router_section)
        self.assertIn("Luna 6", router_section)

    def test_restart_semantics_never_claim_hidden_memory_recovery(self) -> None:
        self.assertIn("generation", self.pattern)
        self.assertIn("hidden memory", self.pattern.lower())
        self.assertIn("new runtime process", self.reference.lower())
        self.assertIn("do not assume hidden-memory continuity", self.reference)


if __name__ == "__main__":
    unittest.main()
