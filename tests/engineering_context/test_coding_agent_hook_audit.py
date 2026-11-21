"""Regressions for the offline coding-agent hook inventory and scoped repair."""
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
from io import StringIO
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
        self.assertFalse(self.u.is_owned_bootstrap_command("echo " + self.owned(), self.script))

    def test_supported_user_clients_are_discovered_without_repo_scan(self):
        targets = self.u.discover(self.home, [], [])
        clients = {target.client for target in targets if target.editable}
        self.assertTrue({"codex", "claude-code", "cursor", "gemini-cli",
                         "github-copilot", "windsurf"}.issubset(clients))
        self.assertFalse(any(target.scope == "project" for target in targets))

    def test_audit_reports_candidate_limits_without_reading_omitted_files(self):
        plugin_dir = ".config/opencode/plugins/local"
        child_two = self.installed(f"{plugin_dir}/b.txt", {})
        child_one = self.installed(f"{plugin_dir}/a.txt", {})
        with patch.object(self.u, "MAX_TARGETS", 9), patch.object(self.u, "MAX_SCRIPT_CHILDREN", 2):
            quiet = self.u.run(home=self.home, projects=[], extras=[], apply=False, clients_stopped=False)
            self.assertEqual(quiet["checked"], 2)
            self.assertEqual(quiet["coverage"]["limit_hits"], [])
            self.installed(f"{plugin_dir}/c.txt", {})
            extra = self.installed("explicit.json", {})
            text = StringIO()
            with redirect_stdout(text), patch.object(self.u, "_safe_file", wraps=self.u._safe_file) as checked:
                self.assertEqual(self.u.main(["--home", str(self.home), "--extra-file", str(extra)]), 0)
            self.assertEqual([args.args[0] for args in checked.call_args_list], [child_one, child_two])
            self.assertEqual(text.getvalue().count("Coverage: partial local inventory"), 1)
            report = self.u.run(home=self.home, projects=[], extras=[extra], apply=False, clients_stopped=False)
            self.assertEqual(report["coverage"]["limit_hits"], [
                {"bound": "script_directory_children", "candidate_count": 3, "limit": 2,
                 "omitted_candidates": 1, "client": "opencode", "scope": "audit-only",
                 "path": str(self.home / plugin_dir)},
                {"bound": "targets", "candidate_count": 10, "limit": 9, "omitted_candidates": 1},
            ])
            self.assertEqual(report["warnings"], [])
            self.assertEqual(report["changed_files"], [])

            project = self.home / "project"
            for n in reversed(range(10)):
                self.installed(f"project/.github/hooks/{n}.json", {})
            project_report = self.u.run(home=self.home, projects=[project], extras=[],
                                        apply=False, clients_stopped=False)
            self.assertEqual(project_report["coverage"]["limit_hits"], [
                report["coverage"]["limit_hits"][0],
                {"bound": "directory", "candidate_count": 10, "limit": 9,
                 "omitted_candidates": 1, "client": "github-copilot", "scope": "project",
                 "path": str(project / ".github/hooks")},
                {"bound": "targets", "candidate_count": 26, "limit": 9, "omitted_candidates": 17},
            ])

    def test_explicit_home_ignores_ambient_client_directories(self):
        path = self.installed("ambient/.codex/hooks.json", {"hooks": {"SessionStart": [
            {"command": self.owned()},
        ]}})
        original = path.read_bytes()
        env = {"CODEX_HOME": str(path.parent), "CLAUDE_CONFIG_DIR": str(self.home / "ambient/.claude"),
               "COPILOT_HOME": str(self.home / "ambient/.copilot")}
        with patch.object(self.u.os, "environ", env):
            self.assertTrue(all(not item.path.is_relative_to(self.home / "ambient")
                                for item in self.u.discover(self.home, [], [])))
            self.assertIn(path, {item.path for item in self.u.discover(self.home, [], [], use_environment=True)})
            report = self.u.run(home=self.home, projects=[], extras=[], apply=True, clients_stopped=True)
        self.assertFalse(report["changed_files"])
        self.assertEqual(path.read_bytes(), original)

    def test_mixed_nested_group_removes_only_exact_owned_hook(self):
        own = {"type": "command", "command": self.owned()}
        foreign = {"type": "command", "command":
                   "python /foreign/handbook_update.py preflight --hook"}
        other = {"type": "command", "command": "security-guard --mode enforce"}
        before = {"hooks": {"SessionStart": [{"matcher": "startup", "hooks": [own, other]}],
                            "BeforeTool": [{"hooks": [foreign]}], "OtherEvent": []},
                  "custom": {"enabled": True}}
        after, count = self.u.strip_config(before, self.script)
        self.assertEqual(count, 1)
        self.assertEqual(after["hooks"]["OtherEvent"], [])
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

    def test_ambiguous_user_config_is_warned_and_preserved_in_both_modes(self):
        path = self.home / ".codex/hooks.json"
        hook = json.dumps({"SessionStart": [{"command": self.owned()}]})
        for repeated in (
            '"unrelated":"first","unrelated":"second"',
            r'"settings":{"th\u0065me":"first","theme":"second"}',
        ):
            original = b"\xef\xbb\xbf" + ('{' + repeated + ',\r\n"hooks":' + hook + '}\r\n').encode("utf-8")
            path.write_bytes(original)
            for apply in (False, True):
                with self.subTest(repeated=repeated, apply=apply):
                    report = self.u.run(home=self.home, projects=[], extras=[],
                                        apply=apply, clients_stopped=apply)
                    self.assertEqual(report["warnings"], [{
                        "client": "codex", "path": str(path), "issue": "duplicate JSON member",
                        "action": "not modified",
                    }])
                    self.assertEqual(report["owned_entries"], 0)
                    self.assertEqual(report["changed_files"], [])
                    self.assertEqual(path.read_bytes(), original)
                    self.assertFalse((self.home / ".agents/handbook-hook-backups").exists())

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

    def test_copilot_platform_commands_and_exec_args_are_reported_read_only(self):
        project = self.home / "workspace"
        path = self.installed("workspace/.github/hooks/handbook.json", {
            "version": 1,
            "hooks": {"sessionStart": [
                {"type": "command", "bash": self.owned()},
                {"type": "command", "powershell": self.owned()},
                {"type": "command", "exec": "python", "args": ["-I", str(self.script), "preflight", "--hook"]},
            ]},
        })
        original = path.read_bytes()
        report = self.u.run(home=self.home, projects=[project], extras=[],
                            apply=True, clients_stopped=True)
        self.assertEqual(report["owned_entries"], 0)
        self.assertEqual(report["suspected_entries"], 3)
        self.assertFalse(report["changed_files"])
        self.assertEqual(path.read_bytes(), original)

    def test_user_command_with_a_platform_override_requires_review(self):
        path = self.installed(".copilot/hooks/handbook.json", {"hooks": {"sessionStart": [
            {"type": "command", "command": self.owned(), "powershell": "echo keep"},
        ]}})
        original = path.read_bytes()
        report = self.u.run(home=self.home, projects=[], extras=[], apply=True, clients_stopped=True)
        self.assertEqual(report["owned_entries"], 0)
        self.assertEqual(report["suspected_entries"], 1)
        self.assertFalse(report["changed_files"])
        self.assertEqual(path.read_bytes(), original)

    def test_opaque_windows_override_is_reviewed_without_claiming_ownership(self):
        path = self.installed(".codex/hooks.json", {"hooks": {"SessionStart": [{
            "type": "command", "command": "echo keep",
            "commandWindows": "powershell.exe -NoProfile -EncodedCommand AAAA",
        }]}})
        original = path.read_bytes()
        report = self.u.run(home=self.home, projects=[], extras=[], apply=True, clients_stopped=True)
        self.assertEqual(report["owned_entries"], 0)
        self.assertEqual(report["opaque_entries"], 1)
        self.assertIn("REVIEW_OPAQUE_PLATFORM_COMMAND", [item["classification"] for item in report["findings"]])
        self.assertFalse(report["changed_files"])
        self.assertEqual(path.read_bytes(), original)

    def test_nested_command_in_a_hybrid_group_is_reported_without_editing(self):
        path = self.installed(".copilot/hooks/handbook.json", {"hooks": {"SessionStart": [{
            "matcher": "startup", "bash": "echo keep", "hooks": [{"command": self.owned()}],
        }]}})
        original = path.read_bytes()
        report = self.u.run(home=self.home, projects=[], extras=[], apply=True, clients_stopped=True)
        self.assertEqual(report["owned_entries"], 0)
        self.assertEqual(report["suspected_entries"], 1)
        self.assertFalse(report["changed_files"])
        self.assertEqual(path.read_bytes(), original)

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
        path.parent.mkdir(parents=True, exist_ok=True)
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
