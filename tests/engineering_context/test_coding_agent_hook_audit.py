"""Regression definitions for offline coding-agent hook isolation.

This test module is intentionally NOT executed during the 2026-11-20
manual-testing handoff. Run it locally before considering any client repaired.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def load_audit():
    spec = importlib.util.spec_from_file_location(
        "handbook_hook_audit", ROOT / "automation/agents/handbook_hook_audit.py"
    )
    import sys
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CodingAgentHookIsolationTests(unittest.TestCase):
    def setUp(self):
        self.u = load_audit()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.script = self.home / ".codex/handbook-bootstrap/handbook_update.py"
        self.script.parent.mkdir(parents=True)

    def installed(self, name, data):
        path = self.home / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def owned(self):
        return f"python -I {self.script} preflight --hook --event SessionStart"

    def test_exact_command_and_foreign_scripts_not_confused(self):
        self.assertTrue(self.u.is_owned_bootstrap_command(self.owned(), self.script))
        self.assertFalse(self.u.is_owned_bootstrap_command(
            "python -I /foreign/handbook_update.py preflight --hook", self.script
        ))
        self.assertFalse(self.u.is_owned_bootstrap_command(
            f"python -I {self.script} preflight", self.script
        ))
        self.assertFalse(self.u.is_owned_bootstrap_command(
            "python -I /foreign/handbook_update.py update --hook", self.script
        ))

    def test_supported_user_clients_are_discovered_without_repo_scan(self):
        targets = self.u.discover(self.home, [], [])
        clients = {target.client for target in targets if target.editable}
        self.assertTrue({"codex", "claude-code", "cursor", "gemini-cli",
                         "github-copilot", "windsurf"}.issubset(clients))
        self.assertFalse(any(target.scope == "project" for target in targets))

    def test_mixed_nested_group_removes_only_exact_owned_hook(self):
        own = {"type": "command", "command": self.owned()}
        foreign = {"type": "command", "command":
                   "python /foreign/handbook_update.py preflight --hook"}
        other = {"type": "command", "command": "security-guard --mode enforce"}
        before = {"hooks": {"SessionStart": [{"matcher": "startup", "hooks": [own, other]}],
                            "BeforeTool": [{"hooks": [foreign]}]},
                  "custom": {"enabled": True}}
        after, count = self.u.strip_config(before, self.script)
        self.assertEqual(count, 1)
        self.assertEqual(after["hooks"]["SessionStart"][0]["hooks"], [other])
        self.assertEqual(after["hooks"]["BeforeTool"], [{"hooks": [foreign]}])
        self.assertEqual(after["custom"], before["custom"])
        self.assertEqual(before["hooks"]["SessionStart"][0]["hooks"], [own, other])

    def test_cursor_and_gemini_direct_entries_remove_only_owned(self):
        for name, event in (
            (".cursor/hooks.json", "beforeSubmitPrompt"),
            (".gemini/settings.json", "BeforeAgent"),
            (".codeium/windsurf/hooks.json", "pre_user_prompt"),
        ):
            with self.subTest(name=name):
                path = self.installed(name, {"hooks": {
                    event: [{"command": self.owned()}, {"command": "safe-command"}]}})
                report = self.u.run(home=self.home, projects=[], extras=[],
                                    apply=True, clients_stopped=True)
                self.assertFalse(report["warnings"])
                data = json.loads(path.read_text())
                self.assertEqual(data["hooks"][event], [{"command": "safe-command"}])
                self.assertTrue(any(change["path"] == str(path) for change in report["changed_files"]))

    def test_audit_does_not_modify_other_clients_or_configs(self):
        path = self.installed(".claude/settings.json", {"hooks": {"SessionStart": [
            {"hooks": [{"type": "command", "command": self.owned()}]}]}})
        old = path.read_bytes()
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=False, clients_stopped=False)
        self.assertEqual(old, path.read_bytes())
        self.assertEqual(report["owned_entries"], 1)
        self.assertFalse(report["changed_files"])

    def test_user_only_mutation_never_rewrites_project_files(self):
        project = self.home / "workspace"
        path = project / ".github/hooks/hook.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"hooks": {"SessionStart": [
            {"command": self.owned()}]}}))
        old = path.read_bytes()
        report = self.u.run(home=self.home, projects=[project], extras=[],
                            apply=True, clients_stopped=True)
        self.assertEqual(path.read_bytes(), old)
        self.assertFalse(report["changed_files"])
        self.assertEqual(report["owned_entries"], 1)
        self.assertIn("PROJECT_REVIEW_REQUIRED", [
            x["classification"] for x in report["findings"]])

    def test_concurrent_edit_preserves_original_and_stops(self):
        path = self.installed(".codex/hooks.json", {"hooks": {"SessionStart": [
            {"command": self.owned()}]}})
        before = path.read_bytes()
        with patch.object(self.u, "_atomic_update",
                          side_effect=RuntimeError("concurrent mutation")):
            report = self.u.run(home=self.home, projects=[], extras=[],
                                apply=True, clients_stopped=True)
        self.assertEqual(before, path.read_bytes())
        self.assertTrue(report["warnings"])
        self.assertFalse(report["changed_files"])

    def test_bom_and_crlf_are_preserved_and_backup_contains_exact_bytes(self):
        path = self.home / ".copilot/hooks/handbook.json"
        path.parent.mkdir(parents=True)
        old = b"\xef\xbb\xbf" + json.dumps({
            "hooks": {"SessionStart": [{"command": self.owned()}]},
            "other": "preserved"
        }, indent=2).replace("\n", "\r\n").encode("utf-8") + b"\r\n"
        path.write_bytes(old)
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=True, clients_stopped=True)
        self.assertFalse(report["warnings"])
        updated = path.read_bytes()
        self.assertTrue(updated.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(updated.endswith(b"\r\n"))
        self.assertIn(b"\r\n", updated)
        self.assertEqual(json.loads(updated.decode("utf-8-sig"))["other"], "preserved")
        change = next(c for c in report["changed_files"] if c["path"] == str(path))
        self.assertEqual(Path(change["backup"]).read_bytes(), old)

    def test_unknown_script_files_only_reported(self):
        path = self.home / ".cline/hooks/BeforeAgent.sh"
        path.parent.mkdir(parents=True)
        path.write_text("#!/bin/sh\npython handbook_update.py preflight --hook\n")
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=True, clients_stopped=True)
        self.assertEqual(path.read_text().splitlines()[0], "#!/bin/sh")
        self.assertFalse(any(c["path"] == str(path) for c in report["changed_files"]))
        self.assertIn("REVIEW_SCRIPT_ONLY", [x["classification"] for x in report["findings"]])

    def test_nested_opencode_plugin_is_audit_only(self):
        path = self.home / ".config/opencode/plugins/custom/index.ts"
        path.parent.mkdir(parents=True)
        path.write_text('const plugin = () => "handbook_update.py preflight --hook";')
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=True, clients_stopped=True)
        self.assertTrue(path.exists())
        self.assertIn("REVIEW_SCRIPT_ONLY", [entry["classification"]
                         for entry in report["findings"]])
        self.assertFalse(any(x["path"] == str(path) for x in report["changed_files"]))

    def test_private_backup_symlink_refused_without_edit(self):
        path = self.installed(".codex/hooks.json", {"hooks": {"SessionStart": [
            {"command": self.owned()}]}})
        original = path.read_bytes()
        outside = self.home / "outside"
        outside.mkdir()
        link = self.home / ".agents"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest("directory symlinks unavailable")
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=True, clients_stopped=True)
        self.assertTrue(report["warnings"])
        self.assertEqual(path.read_bytes(), original)

    def test_malformed_json_fails_closed_without_overwrite(self):
        path = self.home / ".codex/hooks.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"hooks": "invalid"}')
        original = path.read_bytes()
        report = self.u.run(home=self.home, projects=[], extras=[],
                            apply=True, clients_stopped=True)
        self.assertTrue(report["warnings"])
        self.assertEqual(path.read_bytes(), original)

    def test_apply_requires_clients_stopped_acknowledgment(self):
        with self.assertRaises(ValueError):
            self.u.run(home=self.home, projects=[], extras=[],
                       apply=True, clients_stopped=False)


if __name__ == "__main__":
    unittest.main()
