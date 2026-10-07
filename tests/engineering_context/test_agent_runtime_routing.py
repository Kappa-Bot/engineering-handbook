from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def catalog_section(text: str, artifact_id: str) -> str:
    marker = f"  - id: {artifact_id}\n"
    if marker not in text:
        raise AssertionError(f"missing catalog id: {artifact_id}")
    return text.split(marker, 1)[1].split("\n  - id: ", 1)[0]


class DynamicAgentRuntimeRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(
            (ROOT / "machine-readable/agent-runtime-routing.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.standard = (ROOT / "standards/agent-runtime-routing.md").read_text(
            encoding="utf-8"
        )
        cls.playbook = (ROOT / "playbooks/agent-runtime-routing.md").read_text(
            encoding="utf-8"
        )
        cls.manifest = (ROOT / "references/agent-runtime-manifest.md").read_text(
            encoding="utf-8"
        )
        cls.specialists = (
            ROOT / "references/agency-agents-specialist-routing.md"
        ).read_text(encoding="utf-8")
        cls.policy = (ROOT / "policies/agent-operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.global_agents = (
            ROOT / "agent-config/codex/AGENTS.global.md"
        ).read_text(encoding="utf-8")
        cls.router = (
            ROOT / "agent-config/codex/skills/engineering-handbook/SKILL.md"
        ).read_text(encoding="utf-8")
        cls.catalog = (ROOT / "machine-readable/catalog.yaml").read_text(
            encoding="utf-8"
        )
        cls.sources = (ROOT / "machine-readable/sources.yaml").read_text(
            encoding="utf-8"
        )
        cls.bundle = json.loads(
            (
                ROOT
                / "agent-config/codex/skills/engineering-handbook/bundle.json"
            ).read_text(encoding="utf-8")
        )
        cls.adoption = (ROOT / "playbooks/codex-global-adoption.md").read_text(
            encoding="utf-8"
        )
        cls.adr = (
            ROOT / "decisions/0006-dynamic-agency-agent-runtime-routing.md"
        ).read_text(encoding="utf-8")

    def test_dynamic_topology_has_no_fixed_roles(self) -> None:
        self.assertEqual(self.profile["profile"], "DYNAMIC_AGENCY_AGENT_ROUTING")
        self.assertEqual(self.profile["status"], "active")
        topology = self.profile["topology"]
        self.assertEqual(topology["default_spawn_count"], 0)
        self.assertEqual(topology["normal_worker_count"], 1)
        self.assertEqual(topology["routine_max_concurrent_workers"], 2)
        self.assertFalse(topology["fixed_role_taxonomy"])
        self.assertFalse(topology["nested_spawning_default"])
        self.assertTrue(topology["agents_orchestrator_is_optional_specialist"])

    def test_execution_order_prefers_no_spawn(self) -> None:
        self.assertEqual(
            self.profile["execution_order"],
            [
                "deterministic_tool_or_script",
                "controller_direct_execution",
                "one_agency_agents_specialist",
                "second_independent_specialist_if_distinct_value_or_required_review",
            ],
        )
        self.assertIn("Use **zero subagents by default**.", self.standard)
        self.assertIn("A matching profile is not sufficient reason to spawn.", self.specialists)

    def test_cheap_implementer_is_explicit_default_when_safe(self) -> None:
        cheap = self.profile["cheap_implementer"]
        self.assertTrue(cheap["preferred_when_contract_frozen_and_verification_strong"])
        self.assertEqual(cheap["current_preferred_model"], "gpt-6-luna")
        self.assertEqual(cheap["preferred_effort"], "medium")
        self.assertTrue(cheap["low_effort_for_truly_mechanical_work"])
        self.assertIn("Cheap implementer gate", self.standard)
        self.assertIn("Luna medium", self.playbook)

    def test_model_and_effort_are_independent_and_explicit(self) -> None:
        spawn = self.profile["spawn_configuration"]
        self.assertTrue(spawn["explicit_model_required_when_supported"])
        self.assertTrue(spawn["explicit_reasoning_effort_required_when_supported"])
        self.assertTrue(spawn["do_not_rely_on_controller_inheritance"])
        self.assertFalse(spawn["silent_model_or_effort_substitution"])
        for document in (self.standard, self.policy, self.global_agents, self.router):
            self.assertIn("model", document.lower())
            self.assertIn("reasoning effort", document.lower())
        self.assertNotIn("parent = Sol 6.1", self.global_agents)
        self.assertNotIn("design-quality = Astra", self.global_agents)
        self.assertNotIn("delivery = Luna", self.global_agents)

    def test_expensive_effort_is_not_default(self) -> None:
        effort = self.profile["effort_routing"]
        self.assertIn("exceptional", effort["xhigh"])
        self.assertIn("exception", effort["max"])
        routes = self.profile["model_routing"]["routes"]
        max_route = next(r for r in routes if r["case"] == "max_effort")
        self.assertEqual(max_route["selection"], "eval_gated_exception_only")
        self.assertIn("eval-gated exception only", self.standard)
        self.assertIn("Astra xhigh", self.playbook)

    def test_failure_does_not_trigger_automatic_model_ladder(self) -> None:
        escalation = self.profile["escalation"]
        self.assertFalse(escalation["automatic_model_ladder"])
        self.assertEqual(escalation["environment_failure"], "fix_or_isolate_environment")
        self.assertEqual(escalation["authority_ambiguity"], "resolve_authority")
        self.assertEqual(escalation["clear_code_defect"], "same_worker_may_fix")
        self.assertEqual(
            escalation["insufficient_reasoning"], "raise_effort_or_model"
        )
        self.assertTrue(escalation["prefer_change_one_routing_variable_at_a_time"])
        self.assertIn("Escalation by cause", self.standard)

    def test_independent_review_is_risk_triggered(self) -> None:
        review = self.profile["review"]
        self.assertFalse(review["independent_review_default"])
        self.assertTrue(review["reviewer_uses_same_model_effort_routing"])
        self.assertTrue(review["astra_is_not_default_reviewer"])
        self.assertTrue(review["implementation_author_is_not_independent_reviewer"])
        self.assertGreaterEqual(len(review["mandatory_for"]), 6)
        self.assertIn("Independent review", self.standard)
        self.assertIn("Do not default review to Astra", self.playbook)

    def test_active_documents_use_dynamic_routing(self) -> None:
        for document in (self.policy, self.global_agents, self.router):
            self.assertIn("Agency Agents", document)
            self.assertIn("std-agent-runtime-routing", document)
            self.assertNotIn("OWNER_AUTHORIZED_ROLE_PODS", document)
            self.assertNotIn("OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS", document)

    def test_catalog_bundle_and_sources_are_current(self) -> None:
        active = (
            "std-agent-runtime-routing",
            "pb-agent-runtime-routing",
            "ref-agent-runtime-manifest",
            "cfg-agent-runtime-routing",
        )
        for artifact_id in active:
            self.assertIn("status: active", catalog_section(self.catalog, artifact_id))
        self.assertIn(
            "status: accepted",
            catalog_section(self.catalog, "adr-0006-dynamic-agency-agent-runtime-routing"),
        )
        for legacy_id in (
            "std-owner-authorized-role-pods",
            "pb-owner-authorized-role-pod-execution",
            "ref-owner-authorized-role-manifest",
            "cfg-owner-authorized-role-pods",
            "cfg-owner-authorized-two-agent-low-comms",
        ):
            self.assertIn("status: superseded", catalog_section(self.catalog, legacy_id))
        self.assertIn("machine-readable/agent-runtime-routing.v1.json", self.bundle["include"])
        for source_id in (
            "src-openai-models",
            "src-openai-reasoning",
            "src-openai-model-selection",
        ):
            self.assertIn(f"  - id: {source_id}\n", self.sources)

    def test_codex_backstop_does_not_replace_explicit_routing(self) -> None:
        self.assertIn("default_subagent_model", self.adoption)
        self.assertIn("default_subagent_reasoning_effort", self.adoption)
        self.assertIn("does **not** replace per-spawn routing", self.adoption)

    def test_agency_orchestrator_is_optional_not_canonical_parent(self) -> None:
        self.assertIn("Agents Orchestrator", self.specialists)
        self.assertIn("**optional**", self.specialists)
        self.assertIn("Make Agents Orchestrator mandatory", self.adr)


if __name__ == "__main__":
    unittest.main()
