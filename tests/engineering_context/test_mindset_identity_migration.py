"""Explicit locator migration; repository identity and snapshot hashes stay stable."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
OLD = "https://github.com/Kappa-Bot/engineering-handbook.git"
NEW = "https://github.com/Kappa-Bot/melodiq-mindset.git"
PIN = "b" * 40


def load_updater():
    spec = importlib.util.spec_from_file_location("mindset_migration_updater", ROOT / "automation/codex/handbook_update.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MindsetIdentityMigrationTests(unittest.TestCase):
    def setUp(self):
        self.u = load_updater()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "codex"
        self.skills = self.root / "skills"
        self.bootstrap = self.home / "handbook-bootstrap"
        self.bootstrap.mkdir(parents=True)
        self.target = self.skills / "engineering-handbook"
        self.config_path = self.bootstrap / "config.json"
        self.script = self.bootstrap / "handbook_update.py"
        self.script.write_bytes(b"old bootstrap")
        self.config = {"schema": "handbook-install/v2", "remote": OLD,
                       "bootstrap": str(self.bootstrap), "target": str(self.target),
                       "codex_home": str(self.home), "git_executable": "git",
                       "bootstrap_sha256": hashlib.sha256(self.script.read_bytes()).hexdigest()}
        self.config_path.write_bytes(self.u.json_bytes(self.config))
        self.files = {"SKILL.md": b"old verified router"}
        self.state = self.u.activate(self.config, self.files, self.u.make_manifest(self.files, "a" * 40))

    def test_legacy_snapshot_identity_and_v2_manifest_are_not_rewritten(self):
        self.assertEqual(self.u.make_manifest(self.files, "a" * 40)["source_repository"], OLD)
        self.assertEqual(self.u.verify_installed({**self.config, "remote": NEW}), self.state)

    def test_exact_new_locator_is_loaded_and_fetch_uses_it_without_fallback(self):
        self.config_path.write_bytes(self.u.json_bytes({**self.config, "remote": NEW}))
        self.assertEqual(self.u.load_config(self.config_path)["remote"], NEW)
        cache = self.root / "cache"
        calls = []
        def git(config, args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, stdout=(PIN + "\n").encode(), stderr=b"")
        with patch.object(self.u, "prepare_cache", return_value=cache), patch.object(self.u, "git_command", side_effect=git):
            self.assertEqual(self.u.fetch_revision({**self.config, "remote": NEW}), (PIN, cache))
        self.assertEqual(calls[0][-2:], [NEW, "refs/heads/main"])
        self.assertEqual(len(calls), 2)

    def test_unrecognized_remote_is_not_fetched_or_loaded(self):
        for remote in (NEW + "/", "https://github.com/Other/melodiq-mindset.git", "file:///tmp/fixture", OLD + "?foo=bar", [NEW]):
            with self.subTest(remote=remote):
                self.config_path.write_bytes(self.u.json_bytes({**self.config, "remote": remote}))
                with self.assertRaises(self.u.UpdateBlocked):
                    self.u.load_config(self.config_path)
                with patch.object(self.u, "prepare_cache", side_effect=AssertionError("unexpected remote access")), self.assertRaises(self.u.UpdateBlocked):
                    self.u.fetch_revision({**self.config, "remote": remote})

    def test_migration_needs_explicit_pin_and_does_not_modify_install(self):
        before = self.config_path.read_bytes()
        with patch.object(self.u, "fetch_revision", side_effect=AssertionError("unpinned migration fetch")), self.assertRaisesRegex(self.u.UpdateBlocked, "expected-revision"):
            self.u.install(self.home, self.skills, repository_location="mindset")
        self.assertEqual(self.config_path.read_bytes(), before)
        self.assertEqual(self.u.verify_installed(self.config), self.state)

    def test_wrong_remote_head_does_not_change_config_or_active_bundle(self):
        before = self.config_path.read_bytes()
        with patch.object(self.u, "fetch_revision", return_value=("c" * 40, self.root / "cache")), patch.object(self.u, "bundle_from_git", side_effect=AssertionError("mismatched pin read")), self.assertRaisesRegex(self.u.UpdateBlocked, "expected canonical main"):
            self.u.install(self.home, self.skills, repository_location="mindset", expected_revision=PIN)
        self.assertEqual(self.config_path.read_bytes(), before)
        self.assertEqual(self.u.verify_installed(self.config), self.state)

    def test_explicit_migration_preserves_previous_revision_and_default_locator(self):
        observed = []
        def fetch(config):
            observed.append(config["remote"])
            return PIN, self.root / "cache"
        new_files = {"SKILL.md": b"new verified router"}
        with patch.object(self.u, "fetch_revision", side_effect=fetch), patch.object(self.u, "bundle_from_git", return_value=new_files) as bundle, patch.object(self.u, "require_fast_forward") as ancestor:
            self.u.install(self.home, self.skills, repository_location="mindset", expected_revision=PIN)
            self.assertEqual(ancestor.call_args.args[-2:], ("a" * 40, PIN))
            self.assertEqual(bundle.call_args.kwargs["expected_bootstrap"], (ROOT / "automation/codex/handbook_update.py").read_bytes())
            self.assertEqual(self.u.load_config(self.config_path)["remote"], NEW)
            self.u.install(self.home, self.skills)
        self.assertEqual(observed, [NEW, NEW])
        self.assertEqual(self.u.verify_installed(self.config)["revision"], PIN)
        self.assertEqual(json.loads((self.target / "install-manifest.json").read_bytes())["source_repository"], OLD)
        self.assertEqual(self.u.verify_snapshot(Path(self.state["snapshot"]), self.state["manifest_sha256"])["revision"], "a" * 40)

    def test_new_locator_cannot_be_silently_selected_for_first_install(self):
        with patch.object(self.u, "fetch_revision", side_effect=AssertionError("unpinned new installation fetch")), self.assertRaisesRegex(self.u.UpdateBlocked, "expected-revision"):
            self.u.install(self.root / "fresh-codex", self.root / "fresh-skills", repository_location="mindset")

    def test_legacy_config_cannot_be_edited_into_unapproved_locator(self):
        self.config_path.write_bytes(self.u.json_bytes({**self.config, "remote": "https://example.org/repo.git"}))
        with patch.object(self.u, "fetch_revision", side_effect=AssertionError("unexpected fetch")), self.assertRaises(self.u.UpdateBlocked):
            self.u.install(self.home, self.skills, repository_location="mindset", expected_revision=PIN)


if __name__ == "__main__":
    unittest.main()
