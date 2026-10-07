from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class LegacyRolePodsSupersededTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(
            (ROOT / "machine-readable/owner-authorized-role-pods.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.standard = (ROOT / "standards/owner-authorized-role-pods.md").read_text(
            encoding="utf-8"
        )
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
        cls.adr = (
            ROOT / "decisions/0004-owner-authorized-compact-role-pods.md"
        ).read_text(encoding="utf-8")

    def test_legacy_profile_is_superseded(self) -> None:
        self.assertEqual(self.profile["status"], "superseded")
        self.assertEqual(
            self.profile["superseded_by"],
            "machine-readable/agent-runtime-routing.v1.json",
        )
        self.assertIn("status: superseded", self.standard)
        self.assertIn("superseded_by: std-agent-runtime-routing", self.standard)
        self.assertIn("status: superseded", self.adr)
        self.assertIn("ADR-0006", self.adr)

    def test_legacy_profile_is_not_active_routing_authority(self) -> None:
        for document in (self.policy, self.global_agents, self.router):
            self.assertNotIn("OWNER_AUTHORIZED_ROLE_PODS", document)
            self.assertNotIn("OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS", document)
            self.assertNotIn("parent = Sol 6.1", document)
            self.assertNotIn("design-quality = Astra", document)
            self.assertNotIn("delivery = Luna", document)

    def test_catalog_marks_legacy_standard_and_profile_superseded(self) -> None:
        for artifact_id in (
            "std-owner-authorized-role-pods",
            "cfg-owner-authorized-role-pods",
        ):
            marker = f"  - id: {artifact_id}\n"
            section = self.catalog.split(marker, 1)[1].split("\n  - id: ", 1)[0]
            self.assertIn("status: superseded", section)


if __name__ == "__main__":
    unittest.main()
