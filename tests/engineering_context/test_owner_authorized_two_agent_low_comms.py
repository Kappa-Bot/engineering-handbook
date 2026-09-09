from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = ROOT / "machine-readable/owner-authorized-two-agent-low-comms.v1.json"


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


class OwnerAuthorizedTwoAgentLowCommsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        cls.standard = (ROOT / "standards/owner-authorized-role-pods.md").read_text(
            encoding="utf-8"
        )
        cls.policy = (ROOT / "policies/agent-operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.router = (
            ROOT / "agent-config/codex/skills/engineering-handbook/SKILL.md"
        ).read_text(encoding="utf-8")
        cls.catalog_records = parse_catalog_records(
            (ROOT / "machine-readable/catalog.yaml").read_text(encoding="utf-8")
        )
        cls.bundle = json.loads(
            (
                ROOT
                / "agent-config/codex/skills/engineering-handbook/bundle.json"
            ).read_text(encoding="utf-8")
        )

    def test_profile_is_explicit_opt_in_delta_of_role_pods(self) -> None:
        self.assertEqual(
            self.profile["schema"], "owner-authorized-two-agent-low-comms/v1"
        )
        self.assertEqual(
            self.profile["profile"], "OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS"
        )
        self.assertFalse(self.profile["default_enabled"])
        self.assertEqual(
            self.profile["inherits_from"],
            "machine-readable/owner-authorized-role-pods.v1.json",
        )
        self.assertTrue(self.profile["activation"]["requires_explicit_authorization"])
        self.assertTrue(self.profile["activation"]["requires_durable_reference"])

    def test_topology_freezes_master_and_implementer(self) -> None:
        topology = self.profile["topology"]
        self.assertEqual(topology["role_ids"], ["master", "implementer"])
        self.assertEqual(topology["exact_role_count"], 2)
        self.assertFalse(topology["nested_spawning"])
        self.assertFalse(topology["fanout"])
        self.assertTrue(topology["implementer_is_sole_diff_author"])
        self.assertFalse(topology["master_authors_implementation_diff"])

    def test_low_communication_contract_allows_only_three_dispatch_points(self) -> None:
        lifecycle = self.profile["lifecycle"]
        communication = self.profile["communication"]
        self.assertTrue(lifecycle["one_shot_default"])
        self.assertEqual(
            lifecycle["allowed_dispatches"],
            ["initial", "material-blocker", "final-handoff"],
        )
        self.assertTrue(lifecycle["final_handoff_required"])
        self.assertFalse(communication["progress_chatter"])
        self.assertFalse(communication["repeat_specs"])
        self.assertFalse(communication["repeat_diffs"])
        self.assertFalse(communication["repeat_logs"])
        self.assertTrue(communication["repository_over_conversation"])
        self.assertTrue(communication["deltas_only_after_initial"])

    def test_recovery_and_master_review_are_repository_bound(self) -> None:
        recovery = self.profile["recovery"]
        review = self.profile["review"]
        self.assertEqual(recovery["restart_from"], ["git", "repository"])
        self.assertTrue(recovery["reconcile_before_edit"])
        self.assertTrue(recovery["hidden_memory_is_not_required"])
        self.assertEqual(
            recovery["minimum_recovery_state"],
            [
                "run_id",
                "branch",
                "base_sha",
                "head_sha",
                "authority_refs",
                "owned_paths",
                "verification",
                "blockers",
                "next_action",
                "updated_at",
            ],
        )
        self.assertEqual(
            review["master_reviews_directly"],
            ["repository", "diff", "rendered-output", "gates"],
        )
        self.assertTrue(review["exact_head_required"])

    def test_profile_is_cataloged_bundled_and_referenced_without_rule_duplication(self) -> None:
        record = self.catalog_records["cfg-owner-authorized-two-agent-low-comms"]
        self.assertEqual(
            record["path"],
            "machine-readable/owner-authorized-two-agent-low-comms.v1.json",
        )
        self.assertIn(record["path"], self.bundle["include"])
        self.assertIn(
            "OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS",
            self.standard,
        )
        self.assertIn(
            "OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS",
            self.policy,
        )
        self.assertIn(
            "OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS",
            self.router,
        )
        self.assertIn("inherits_from", self.profile)
        self.assertNotIn("design-quality", self.profile["topology"]["role_ids"])
        self.assertNotIn("delivery", self.profile["topology"]["role_ids"])


if __name__ == "__main__":
    unittest.main()
