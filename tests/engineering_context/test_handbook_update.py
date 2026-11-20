from __future__ import annotations

import copy
import base64
import hashlib
import importlib.util
import json
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[2]


def updater():
    spec = importlib.util.spec_from_file_location("handbook_update", ROOT / "automation/codex/handbook_update.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpdateSafetyTests(unittest.TestCase):
    def setUp(self):
        self.u = updater()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "skills/engineering-handbook"
        self.bootstrap = self.root / "codex/handbook-bootstrap"
        self.bootstrap.mkdir(parents=True)
        self.config = {"schema": "handbook-install/v2", "remote": self.u.CANONICAL_REMOTE,
                       "bootstrap": str(self.bootstrap), "target": str(self.target),
                       "codex_home": str(self.bootstrap.parent), "revision": "a" * 40}

    def snapshot(self, text="old"):
        files = {"SKILL.md": text.encode(), "references/README.md": b"readme"}
        manifest = self.u.make_manifest(files, "a" * 40)
        self.u.activate(self.config, files, manifest)
        return files, manifest

    def test_local_drift_blocks_update_without_touching_it(self):
        self.snapshot()
        (self.target / "SKILL.md").write_text("user edit")
        with self.assertRaisesRegex(self.u.UpdateBlocked, "drift"):
            self.u.activate(self.config, {"SKILL.md": b"new"}, self.u.make_manifest({"SKILL.md": b"new"}, "b" * 40))
        self.assertEqual((self.target / "SKILL.md").read_text(), "user edit")

    def test_modified_manifest_and_unexpected_file_are_not_trusted(self):
        self.snapshot()
        manifest_path = self.target / "install-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["revision"] = "b" * 40
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.verify_installed(self.config)

    def test_safe_activation_retains_previous_and_recovers_crash(self):
        self.snapshot()
        files = {"SKILL.md": b"new"}
        self.u.activate(self.config, files, self.u.make_manifest(files, "b" * 40))
        self.assertEqual((self.target / "SKILL.md").read_text(), "new")
        backups = list((self.bootstrap / "backups").glob("*/SKILL.md"))
        self.assertTrue(any(p.read_text() == "old" for p in backups))
        self.assertEqual(self.u.verify_installed(self.config)["revision"], "b" * 40)

    def test_paths_symlinks_case_collisions_and_invalid_hashes_rejected(self):
        for bad in ({"../escape": b"x"}, {"/absolute": b"x"}, {"C:/drive": b"x"}, {"refs/A": b"x", "refs/a": b"y"}, {"refs/CON": b"x"}, {"refs/a.": b"x"}, {"refs/a": b"x", "refs/a/b": b"y"}):
            files = {"SKILL.md": b"valid", **bad}
            with self.subTest(files=files), self.assertRaises(self.u.UpdateBlocked):
                self.u.make_manifest(files, "a" * 40)
        self.snapshot()
        destination = self.root / "outside"; destination.write_text("outside")
        (self.target / "references/README.md").unlink()
        (self.target / "references/README.md").symlink_to(destination)
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.verify_installed(self.config)

    def test_lock_serializes_refresh_and_does_not_steal_live_lock(self):
        with self.u.update_lock(self.bootstrap), patch.object(self.u, "LOCK_WAIT_SECONDS", 0.05):
            with self.assertRaisesRegex(self.u.UpdateBlocked, "lock"):
                with self.u.update_lock(self.bootstrap):
                    self.fail("second writer entered")

    def test_kernel_lock_persists_but_releases_ownership(self):
        with self.u.update_lock(self.bootstrap):
            marker = json.loads((self.bootstrap / "update.lock").read_text())
            self.assertEqual(marker["schema"], self.u.LOCK_FORMAT)
        self.assertTrue((self.bootstrap / "update.lock").exists())
        with self.u.update_lock(self.bootstrap):
            self.assertEqual(json.loads((self.bootstrap / "update.lock").read_text())["schema"], self.u.LOCK_FORMAT)

    def test_legacy_exclusive_lock_is_not_stolen(self):
        lock = self.bootstrap / "update.lock"
        old = '{"pid":123,"created":1}'
        lock.write_text(old)
        with self.assertRaisesRegex(self.u.UpdateBlocked, "legacy"):
            with self.u.update_lock(self.bootstrap):
                self.fail("legacy writer bypassed")
        self.assertEqual(lock.read_text(), old)

    def test_no_root_prompt_refresh_even_if_old_hook_is_installed(self):
        source = self.bootstrap / "handbook_update.py"
        old = self.u.merge_hooks({}, source)
        user = {"hooks": [{"type": "command", "command": "echo keep-me"}]}
        old["hooks"]["UserPromptSubmit"] = [
            {"hooks": [{"type": "command", "command": f"python -I {source} preflight --hook --event UserPromptSubmit"}]},
            user,
        ]
        merged = self.u.merge_hooks(old, source)
        self.assertEqual(merged["hooks"]["UserPromptSubmit"], [user])
        stream = io.StringIO()
        with patch.object(self.u, "load_config", side_effect=AssertionError("prompt read config")), redirect_stdout(stream):
            result = self.u.main(["preflight", "--hook", "--event", "UserPromptSubmit"])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(stream.getvalue()), {"continue": True, "suppressOutput": True})

    def test_offline_uses_only_verified_last_known_good(self):
        self.snapshot()
        with patch.object(self.u, "fetch_revision", side_effect=self.u.NetworkUnavailable("offline")):
            result = self.u.refresh(self.config)
            self.assertEqual(result["status"], "STALE_OFFLINE")
        (self.target / "SKILL.md").write_text("user edit")
        with patch.object(self.u, "fetch_revision", side_effect=self.u.NetworkUnavailable("offline")):
            with self.assertRaises(self.u.UpdateBlocked):
                self.u.refresh(self.config)

    def test_rejected_remote_candidate_uses_verified_old_snapshot_without_install(self):
        self.snapshot()
        original = self.u.verify_installed(self.config)
        with patch.object(self.u, "fetch_revision", return_value=("b" * 40, self.root / "cache")), \
             patch.object(self.u, "require_fast_forward"), \
             patch.object(self.u, "bundle_from_git", side_effect=self.u.UpdateBlocked("candidate canonical source/index drift")):
            result = self.u.refresh(self.config)
        self.assertEqual(result["status"], "STALE_REJECTED")
        self.assertFalse(result["remote_checked"])
        self.assertIn("candidate canonical source/index drift", result["rejected_reason"])
        self.assertEqual(result["snapshot"], original["snapshot"])
        self.assertEqual(self.u.verify_installed(self.config), original)

    def test_invalid_local_snapshot_is_never_reclassified_as_trusted_stale(self):
        self.snapshot()
        (self.target / "SKILL.md").write_text("unverified edit")
        with patch.object(self.u, "fetch_revision") as fetch, \
             self.assertRaisesRegex(self.u.UpdateBlocked, "drift"):
            self.u.refresh(self.config)
        fetch.assert_not_called()

    def test_root_hook_still_continues_on_stale_lock_and_rejects_manual_preflight(self):
        self.bootstrap.joinpath("update.lock").write_text('{"pid":123,"created":1}')
        output = io.StringIO()
        with patch.object(self.u, "load_config", return_value=self.config), \
             redirect_stdout(output):
            code = self.u.main(["preflight", "--hook", "--event", "SessionStart"])
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertTrue(result["continue"])
        self.assertNotIn("decision", result)
        self.assertNotIn("stopReason", result)
        self.assertIn("legacy update.lock", result["systemMessage"])

        output = io.StringIO()
        with patch.object(self.u, "load_config", return_value=self.config), \
             redirect_stdout(output):
            code = self.u.main(["preflight"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "BLOCKED")

    def test_rescue_hooks_is_offline_scoped_and_preserves_user_hooks(self):
        script = self.bootstrap / "handbook_update.py"
        hooks_path = self.bootstrap.parent / "hooks.json"
        retained = {"hooks": [{"type": "command", "command": "echo user-own-command"}]}
        old = self.u.merge_hooks({}, script)
        old["hooks"]["UserPromptSubmit"] = [
            {"hooks": [{"type": "command", "command": f"python -I {script} preflight --hook --event UserPromptSubmit"}]},
            retained,
        ]
        original = {"hooks": {**old["hooks"], "PreToolUse": [retained]}, "extra": "preserved"}
        hooks_path.write_text(json.dumps(original))
        with patch.object(self.u, "fetch_revision", side_effect=AssertionError("rescue touched remote")):
            preview = self.u.rescue_hooks(self.bootstrap.parent, check=True)
            self.assertEqual(preview["status"], "NEEDS_RESCUE")
            self.assertEqual(preview["removed"], 2)
            self.assertEqual(json.loads(hooks_path.read_text()), original)
            repaired = self.u.rescue_hooks(self.bootstrap.parent)
            self.assertEqual(repaired["status"], "RESCUED")
            new = json.loads(hooks_path.read_text())
            self.assertEqual(new["extra"], "preserved")
            self.assertEqual(new["hooks"]["UserPromptSubmit"], [retained])
            self.assertEqual(new["hooks"]["PreToolUse"], [retained])
            self.assertNotIn("SessionStart", new["hooks"])
            self.assertEqual(json.loads(Path(repaired["backup"]).read_text()), original)
            self.assertEqual(self.u.rescue_hooks(self.bootstrap.parent)["status"], "NO_OWNED_HOOKS")

    def test_rescue_refuses_malformed_hooks_without_overwriting(self):
        hooks_path = self.bootstrap.parent / "hooks.json"
        hooks_path.write_text('{"hooks":{"SessionStart":"incorrect type"}}')
        before = hooks_path.read_bytes()
        with self.assertRaisesRegex(self.u.UpdateBlocked, "hook"):
            self.u.rescue_hooks(self.bootstrap.parent)
        self.assertEqual(hooks_path.read_bytes(), before)

    def test_hook_timeout_is_advisory_but_manual_timeout_is_error(self):
        with patch.object(self.u, "load_config", return_value=self.config), \
             patch.object(self.u, "refresh", side_effect=self.u.UpdateBlocked("preflight time budget exhausted")):
            stream = io.StringIO()
            with redirect_stdout(stream):
                code = self.u.main(["preflight", "--hook"])
            self.assertEqual(code, 0)
            result = json.loads(stream.getvalue())
            self.assertTrue(result["continue"])
            self.assertIn("time budget", result["systemMessage"])
            stream = io.StringIO()
            with redirect_stdout(stream):
                code = self.u.main(["preflight"])
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(stream.getvalue())["status"], "BLOCKED")

    def test_git_environment_cannot_rewrite_transport_or_read_prompt(self):
        with patch.dict("os.environ", {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "url.file:///tmp/.insteadOf", "GIT_CONFIG_VALUE_0": "https://", "GIT_SSH_COMMAND": "malicious", "GIT_CONFIG_GLOBAL": "/tmp/evil"}):
            environment = self.u.git_environment(self.bootstrap)
        self.assertNotIn("GIT_CONFIG_COUNT", environment)
        self.assertNotIn("GIT_SSH_COMMAND", environment)
        self.assertEqual(environment["GIT_CONFIG_GLOBAL"], self.u.os.devnull)
        self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(environment["GIT_ALLOW_PROTOCOL"], "https")

    def test_hooks_merge_is_idempotent_and_preserves_unrelated_hooks(self):
        existing = {"hooks": {"SessionStart": [{"matcher": "startup", "hooks": [{"type": "command", "command": "echo user-hook"}]}]}, "custom": True}
        merged = self.u.merge_hooks(copy.deepcopy(existing), self.bootstrap / "handbook_update.py")
        self.assertEqual(merged["hooks"]["SessionStart"][0], existing["hooks"]["SessionStart"][0])
        self.assertTrue(merged["custom"])
        self.assertEqual(self.u.merge_hooks(copy.deepcopy(merged), self.bootstrap / "handbook_update.py"), merged)
        self.assertNotIn("UserPromptSubmit", merged["hooks"])
        self.assertEqual(merged["hooks"]["SessionStart"][-1]["matcher"], "startup|resume|clear")
        self.assertNotIn("SubagentStart", merged["hooks"])
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.merge_hooks({"hooks": []}, self.bootstrap / "handbook_update.py")

    def test_reinstall_with_new_python_does_not_duplicate_owned_hooks(self):
        script = self.bootstrap / "handbook_update.py"
        with patch("sys.executable", "/old/python"):
            existing = self.u.merge_hooks({}, script)
        with patch("sys.executable", "/new/python"):
            merged = self.u.merge_hooks(existing, script)
        self.assertEqual(len(merged["hooks"]["SessionStart"]), 1)
        self.assertNotIn("UserPromptSubmit", merged["hooks"])
        self.assertIn("/new/python", merged["hooks"]["SessionStart"][0]["hooks"][0]["command"])

    def test_override_is_reported_and_user_agents_file_is_not_replaced(self):
        self.snapshot()
        agents = self.bootstrap.parent / "AGENTS.md"; agents.write_text("my instructions")
        override = self.bootstrap.parent / "AGENTS.override.md"; override.write_text("higher priority")
        state = self.u.doctor(self.config)
        self.assertEqual(state["global_instruction_status"], "SHADOWED")
        self.assertEqual(agents.read_text(), "my instructions")

    def test_missing_extra_and_immutable_snapshot_drift_are_blocked(self):
        self.snapshot()
        extra = self.target / "custom.txt"; extra.write_text("user file")
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.verify_installed(self.config)
        extra.unlink()
        state = self.u.verify_installed(self.config)
        (Path(state["snapshot"]) / "SKILL.md").write_text("edited immutable snapshot")
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.verify_installed(self.config)

    def test_interrupted_activation_rolls_back_without_losing_either_copy(self):
        self.snapshot()
        old = self.u.verify_installed(self.config)
        real_replace = self.u.os.replace
        def interrupt(source, destination):
            if Path(source).name.startswith(".handbook-stage-") and Path(destination) == self.target:
                raise SystemExit("power loss")
            return real_replace(source, destination)
        files = {"SKILL.md": b"new"}
        with patch.object(self.u.os, "replace", side_effect=interrupt):
            with self.assertRaises(SystemExit):
                self.u.activate(self.config, files, self.u.make_manifest(files, "b" * 40))
        self.assertTrue((self.bootstrap / "activation.json").exists())
        self.u.recover_activation(self.config)
        self.assertEqual(self.u.verify_installed(self.config), old)
        self.assertEqual((Path(old["snapshot"]) / "SKILL.md").read_text(), "old")
        self.assertTrue(list(self.target.parent.glob(".handbook-stage-*/SKILL.md")))

    def test_windows_hook_uses_literal_arguments_with_spaces_and_apostrophes(self):
        script = Path("C:/Users/O'Brien & Co/handbook_update.py")
        hooks = self.u.merge_hooks({}, script)
        handler = hooks["hooks"]["SessionStart"][0]["hooks"][0]
        windows = handler["commandWindows"]
        decoded = base64.b64decode(windows.split()[-1]).decode("utf-16-le")
        self.assertIn("O''Brien & Co", decoded)
        self.assertIn("'-I'", decoded)
        self.assertNotIn("-ExecutionPolicy", windows)

    def test_hook_failure_warns_without_blocking_or_reading_prompt(self):
        stream = io.StringIO()
        with redirect_stdout(stream), patch("sys.stdin") as stdin:
            stdin.read.side_effect = AssertionError("must not read prompt")
            code = self.u.main(["preflight", "--hook", "--event", "SessionStart", "--config", str(self.root / "missing.json")])
        self.assertEqual(code, 0)
        output = json.loads(stream.getvalue())
        self.assertTrue(output["continue"])
        self.assertNotIn("decision", output)
        self.assertNotIn("stopReason", output)
        self.assertIn("preflight unavailable", output["systemMessage"])
        self.assertIn("No immutable Handbook snapshot", output["hookSpecificOutput"]["additionalContext"])

    def test_partial_snapshot_is_not_published_and_same_revision_can_retry(self):
        self.snapshot()
        previous = self.u.verify_installed(self.config)
        files = {"SKILL.md": b"new", "references/README.md": b"new readme"}
        manifest = self.u.make_manifest(files, "b" * 40)
        real_write = self.u.write_snapshot
        def interrupt(path, contents, metadata):
            if path.parent == self.bootstrap / "snapshots":
                path.mkdir()
                (path / "SKILL.md").write_bytes(contents["SKILL.md"])
                raise SystemExit("power loss during snapshot construction")
            return real_write(path, contents, metadata)
        with patch.object(self.u, "write_snapshot", side_effect=interrupt):
            with self.assertRaises(SystemExit):
                self.u.activate(self.config, files, manifest)
        self.assertEqual(self.u.verify_installed(self.config), previous)
        self.assertFalse((self.bootstrap / "activation.json").exists())
        result = self.u.activate(self.config, files, manifest)
        self.assertEqual(result["revision"], "b" * 40)
        self.assertEqual((Path(result["snapshot"]) / "references/README.md").read_bytes(), b"new readme")

    def test_candidate_contract_rejects_missing_runtime_catalog_drift_and_malformed_types(self):
        original = self.u.local_bundle(ROOT)
        self.u.validate_candidate(original)
        cases = []
        files = dict(original)
        files.pop("references/automation/engineering_context/__main__.py")
        cases.append(("missing runtime entrypoint", files))
        files = dict(original)
        files.pop("references/automation/engineering_context/visual_directions.py")
        cases.append(("missing visual module", files))
        files = dict(original)
        files.pop("references/machine-readable/visual-directions.v1.json")
        cases.append(("missing visual registry", files))
        files = dict(original)
        files["references/machine-readable/visual-directions.v1.json"] = b"{invalid JSON"
        cases.append(("malformed visual registry", files))
        files = dict(original)
        registry_path = "references/machine-readable/visual-directions.v1.json"
        visual = json.loads(files[registry_path]); visual["default_by_surface"]["public-site"] = "glassmorphism"
        files[registry_path] = self.u.json_bytes(visual)
        cases.append(("wrong visual default scope", files))
        files = dict(original)
        visual = json.loads(files[registry_path]); visual["surfaces"].remove("internal-console")
        files[registry_path] = self.u.json_bytes(visual)
        cases.append(("missing internal console surface", files))
        files = dict(original)
        visual = json.loads(files[registry_path]); visual["directions"][1]["aliases"].append("glassmorphism")
        files[registry_path] = self.u.json_bytes(visual)
        cases.append(("ambiguous visual aliases", files))
        files = dict(original)
        visual = json.loads(files[registry_path]); visual["directions"][1]["aliases"].append("\u0301")
        files[registry_path] = self.u.json_bytes(visual)
        cases.append(("blank normalized visual alias", files))
        files = dict(original)
        catalog = "references/machine-readable/catalog.yaml"
        files[catalog] = files[catalog].replace(b"status: active", b"status: retired", 1)
        cases.append(("catalog drift", files))
        for path in ("manifest.json", "discovery.json", "planning.json"):
            files = dict(original)
            files["references/machine-readable/compiled/" + path] = b"[]"
            cases.append(("non-object " + path, files))
        for name, files in cases:
            with self.subTest(case=name), self.assertRaises(self.u.UpdateBlocked):
                self.u.validate_candidate(files)

    def test_every_executable_model_selector_rejects_luna(self):
        original = self.u.local_bundle(ROOT)
        self.u.validate_candidate(original)
        path = "references/machine-readable/agent-runtime-routing.v1.json"
        for field in ("preferred", "backstop", "tier", "route", "fallback"):
            files = dict(original); runtime = json.loads(files[path])
            if field == "preferred":
                runtime["cheap_implementer"]["current_preferred_model"] = "gpt-6-luna"
            elif field == "backstop":
                runtime["spawn_configuration"]["backstop_model"] = "gpt-6-luna"
            elif field == "tier":
                runtime["model_routing"]["current_tiers"]["efficient"] = "gpt-6-luna"
            elif field == "route":
                runtime["model_routing"]["routes"][0]["model"] = "gpt-6-luna"
            else:
                runtime["model_routing"]["fallback_models"] = ["gpt-6-luna"]
            files[path] = self.u.json_bytes(runtime)
            with self.subTest(field=field), self.assertRaisesRegex(self.u.UpdateBlocked, "Luna"):
                self.u.validate_candidate(files)

    def test_candidate_rejects_wrong_nested_collection_types(self):
        original = self.u.local_bundle(ROOT)
        self.u.validate_candidate(original)
        manifest_path = "references/machine-readable/compiled/manifest.json"
        cases = (("artifact_hashes", []), ("documents", None), ("routes", []))
        for field, value in cases:
            files = dict(original)
            manifest = json.loads(files[manifest_path])
            if field == "artifact_hashes":
                manifest[field] = value
            elif field == "documents":
                path = "references/machine-readable/compiled/discovery.json"
                index = json.loads(files[path]); index[field] = value
                index["index_hash"] = self.u.stable_hash({key: item for key, item in index.items() if key != "index_hash"})
                files[path] = self.u.json_bytes(index)
                manifest["discovery_hash"] = index["index_hash"]
                manifest["artifact_hashes"]["discovery.json"] = self.u.stable_hash(index)
            else:
                path = "references/machine-readable/agent-runtime-routing.v1.json"
                runtime = json.loads(files[path]); runtime["model_routing"]["routes"] = {"invalid": "route"}
                files[path] = self.u.json_bytes(runtime)
            files[manifest_path] = self.u.json_bytes(manifest)
            with self.subTest(field=field), self.assertRaises(self.u.UpdateBlocked):
                self.u.validate_candidate(files)

    def test_malformed_candidate_returns_structured_hook_block(self):
        files = self.u.local_bundle(ROOT)
        files["references/machine-readable/compiled/manifest.json"] = b"[]"
        output = io.StringIO()
        with patch.object(self.u, "load_config", return_value=self.config), patch.object(self.u, "refresh", side_effect=lambda _: self.u.validate_candidate(files)), redirect_stdout(output):
            code = self.u.main(["preflight", "--hook", "--event", "SessionStart"])
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertTrue(result["continue"])
        self.assertNotIn("stopReason", result)
        self.assertIn("candidate JSON object", result["systemMessage"])

    def test_only_network_unavailability_can_use_offline_fallback(self):
        for message, expected in (
            ("Could not resolve host: github.com", self.u.NetworkUnavailable),
            ("Failed to connect to github.com port 443: Connection timed out", self.u.NetworkUnavailable),
            ("SSL certificate problem: unable to get local issuer certificate", self.u.UpdateBlocked),
            ("fatal: fsck error in packed object", self.u.UpdateBlocked),
            ("fatal: couldn't find remote ref refs/heads/main", self.u.UpdateBlocked),
            ("fatal: Authentication failed", self.u.UpdateBlocked),
            ("unclassified fetch failure", self.u.UpdateBlocked),
        ):
            result = subprocess.CompletedProcess(["git", "fetch"], 128, stdout=b"", stderr=message.encode())
            with self.subTest(message=message), patch.object(self.u, "prepare_cache", return_value=self.root / "cache"), patch.object(self.u, "git_command", return_value=result), self.assertRaises(expected):
                self.u.fetch_revision(self.config)

    def test_doctor_separates_files_hook_definitions_and_unobserved_execution(self):
        self.snapshot()
        result = self.u.doctor(self.config)
        self.assertEqual(result.get("global_baseline"), "MISSING")
        self.assertEqual(result.get("hook_definitions"), {"SessionStart": "MISSING", "UserPromptSubmit": "REMOVED"})
        self.assertEqual(result["hook_trust_and_client_support"], "NOT_OBSERVED")
        self.assertNotEqual(result["global_instruction_status"], "FRESH_BASELINE_VIA_HOOK")

    def test_override_added_after_install_blocks_refresh_without_fetching(self):
        self.snapshot()
        (self.bootstrap.parent / "AGENTS.override.md").write_text("new override")
        with patch.object(self.u, "fetch_revision") as fetch:
            with self.assertRaisesRegex(self.u.UpdateBlocked, "override|shadows"):
                self.u.refresh(self.config)
        fetch.assert_not_called()

    def git(self, repo, *args):
        result = subprocess.run(["git", "-c", "user.name=Handbook test", "-c", "user.email=handbook-test@example.invalid", "-C", str(repo), *args], capture_output=True, check=True)
        return result.stdout.decode().strip()

    def test_real_git_fast_forward_accepts_only_ancestry(self):
        repo = self.root / "history"; repo.mkdir()
        self.git(repo, "init", "-b", "main")
        source = repo / "file.txt"; source.write_text("a")
        self.git(repo, "add", "."); self.git(repo, "commit", "-m", "first")
        first = self.git(repo, "rev-parse", "HEAD")
        source.write_text("b"); self.git(repo, "commit", "-am", "second")
        second = self.git(repo, "rev-parse", "HEAD")
        self.u.require_fast_forward(self.config, repo / ".git", first, second)
        with self.assertRaisesRegex(self.u.UpdateBlocked, "rewound"):
            self.u.require_fast_forward(self.config, repo / ".git", second, first)
        self.git(repo, "checkout", "-b", "divergent", first)
        source.write_text("c"); self.git(repo, "commit", "-am", "divergent")
        branch = self.git(repo, "rev-parse", "HEAD")
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.require_fast_forward(self.config, repo / ".git", second, branch)

    def test_dedicated_git_cache_rejects_config_rewrites_and_symlinks(self):
        cache = self.u.prepare_cache(self.config)
        (cache / "config").write_text('[url "file:///tmp/"]\n insteadOf = https://\n')
        with self.assertRaisesRegex(self.u.UpdateBlocked, "configuration drift"):
            self.u.prepare_cache(self.config)
        (cache / "config").write_bytes(self.u.CACHE_CONFIG)
        outside = self.root / "outside"; outside.write_text("not a Git ref")
        (cache / "FETCH_HEAD").symlink_to(outside)
        with self.assertRaises(self.u.UpdateBlocked):
            self.u.prepare_cache(self.config)

    def test_real_git_bundle_materializes_objects_and_rejects_stale_artifacts(self):
        repo = self.root / "source"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.git(repo, "init", "-b", "main"); self.git(repo, "add", "."); self.git(repo, "commit", "-m", "candidate")
        revision = self.git(repo, "rev-parse", "HEAD")
        files = self.u.bundle_from_git(self.config, repo / ".git", revision)
        self.assertIn("references/machine-readable/compiled/discovery.json", files)
        # Worktree changes cannot alter the pinned Git object snapshot.
        (repo / "README.md").write_text("dirty worktree")
        self.assertEqual(files, self.u.bundle_from_git(self.config, repo / ".git", revision))
        self.git(repo, "commit", "-am", "stale source")
        with self.assertRaisesRegex(self.u.UpdateBlocked, "source/index drift"):
            self.u.bundle_from_git(self.config, repo / ".git", self.git(repo, "rev-parse", "HEAD"))

    def test_refresh_does_not_replace_local_copy_on_divergent_history(self):
        self.snapshot()
        with patch.object(self.u, "fetch_revision", return_value=("b" * 40, self.root / "cache")), patch.object(self.u, "require_fast_forward", side_effect=self.u.UpdateBlocked("divergent")):
            with self.assertRaises(self.u.UpdateBlocked):
                self.u.refresh(self.config)
        self.assertEqual((self.target / "SKILL.md").read_text(), "old")

    def test_manual_installer_cannot_replace_enrolled_target(self):
        self.snapshot()
        with patch.object(self.u, "local_bundle", return_value={"SKILL.md": b"manual replacement"}):
            with self.assertRaisesRegex(self.u.UpdateBlocked, "enrolled"):
                self.u.manual_bundle(ROOT, self.target.parent, backup_existing=True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "old")

    def test_complete_enrollment_preserves_user_configuration_and_runs_installed_doctor(self):
        repo = self.root / "enrollment-source"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.git(repo, "init", "-b", "main"); self.git(repo, "add", "."); self.git(repo, "commit", "-m", "enrollment candidate")
        revision = self.git(repo, "rev-parse", "HEAD")
        agents = self.bootstrap.parent / "AGENTS.md"; agents.write_text("personal instructions")
        hooks_path = self.bootstrap.parent / "hooks.json"
        user_group = {"hooks": [{"type": "command", "command": "echo user-hook"}]}
        hooks_path.write_text(json.dumps({"hooks": {"UserPromptSubmit": [user_group]}}))
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text("old unmanaged personal skill")
        with patch.object(self.u, "fetch_revision", return_value=(revision, repo / ".git")):
            result = self.u.install(self.bootstrap.parent, self.target.parent, backup_existing=True)
            again = self.u.install(self.bootstrap.parent, self.target.parent)
        self.assertEqual(result["revision"], revision)
        self.assertEqual(again["revision"], revision)
        self.assertEqual(agents.read_text(), "personal instructions")
        hooks = json.loads(hooks_path.read_text())["hooks"]
        self.assertEqual(len(hooks["UserPromptSubmit"]), 1)
        self.assertEqual(hooks["UserPromptSubmit"][0], user_group)
        self.assertTrue(any(p.read_text() == "old unmanaged personal skill" for p in (self.bootstrap / "backups").glob("*/SKILL.md")))
        script = self.bootstrap / "handbook_update.py"
        checked = subprocess.run([sys.executable, "-I", str(script), "doctor"], capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        diagnosed = json.loads(checked.stdout)
        self.assertEqual(diagnosed["status"], "VERIFIED_LOCAL")
        self.assertEqual(diagnosed["global_instruction_status"], "READY_FOR_CLIENT_VERIFICATION")
        self.assertEqual(diagnosed["hook_definitions"], {"SessionStart": "PRESENT", "UserPromptSubmit": "REMOVED"})
        self.assertEqual(diagnosed["hook_execution"], "NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main()
