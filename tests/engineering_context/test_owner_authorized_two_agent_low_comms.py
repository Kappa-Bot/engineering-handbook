from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class LegacyTwoAgentLowCommsSupersededTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(
            (
                ROOT
                / "machine-readable/owner-authorized-two-agent-low-comms.v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.policy = (ROOT / "policies/agent-operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.router = (
            ROOT / "agent-config/codex/skills/engineering-handbook/SKILL.md"
        ).read_text(encoding="utf-8")
        cls.catalog = (ROOT / "machine-readable/catalog.yaml").read_text(
            encoding="utf-8"
        )

    def test_legacy_low_comms_profile_is_superseded(self) -> None:
        self.assertEqual(self.profile["status"], "superseded")
        self.assertEqual(
            self.profile["superseded_by"],
            "machine-readable/agent-runtime-routing.v1.json",
        )

    def test_active_routing_does_not_require_exact_two_agent_taxonomy(self) -> None:
        for document in (self.policy, self.router):
            self.assertNotIn("OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS", document)
            self.assertNotIn("only these delegated role types", document)

    def test_catalog_marks_legacy_profile_superseded(self) -> None:
        marker = "  - id: cfg-owner-authorized-two-agent-low-comms\n"
        section = self.catalog.split(marker, 1)[1].split("\n  - id: ", 1)[0]
        self.assertIn("status: superseded", section)


if __name__ == "__main__":
    unittest.main()
