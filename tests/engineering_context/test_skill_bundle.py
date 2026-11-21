from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from automation.codex import handbook_update
from automation.codex.handbook_update import BUNDLE_SOURCE, SKILL_SOURCE, digest, json_bytes, local_bundle, snapshot_files
from automation.engineering_context.handbook_compile import compile_handbook


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "automation/codex/handbook_update.py"


def write_file(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def copy_compiled_source(source: Path) -> None:
    for relative, content in local_bundle(ROOT).items():
        source_path = SKILL_SOURCE if relative == "SKILL.md" else relative.removeprefix("references/")
        write_file(source / source_path, content)
    write_file(source / BUNDLE_SOURCE, (ROOT / BUNDLE_SOURCE).read_bytes())
    compile_handbook(source, source / "machine-readable/compiled")


class SkillBundleTests(unittest.TestCase):
    def test_generated_python_cache_is_not_canonical_skill_source(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            write_file(root / SKILL_SOURCE, b"Canonical router")
            write_file(root / BUNDLE_SOURCE, json_bytes({
                "schema_version": 1, "skill_name": "engineering-handbook",
                "include": ["automation/engineering_context"],
            }))
            source = root / "automation/engineering_context"
            write_file(source / "router.py", b"# canonical")
            write_file(source / "router.pyc", b"legacy cache")
            write_file(source / "__pycache__/router.cpython-312.pyc", b"warm cache")
            self.assertEqual(local_bundle(root), {
                "SKILL.md": b"Canonical router",
                "references/automation/engineering_context/router.py": b"# canonical",
            })

    def test_manual_install_preserves_a_v2_target_created_during_verification(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            skills_home = root / "skills"
            target = skills_home / "engineering-handbook"
            enrolled_files = {"SKILL.md": b"Concurrent enrollment"}
            enrolled_manifest = handbook_update.make_manifest(enrolled_files, "a" * 40)

            def enroll(_files: dict[str, bytes]) -> None:
                skills_home.mkdir()
                handbook_update.write_snapshot(target, enrolled_files, enrolled_manifest)

            with (
                patch.object(handbook_update, "local_bundle", return_value={"SKILL.md": b"Manual bundle"}),
                patch.object(handbook_update, "verify_frozen_bundle", side_effect=enroll),
                self.assertRaisesRegex(handbook_update.UpdateBlocked, "target changed"),
            ):
                handbook_update.manual_bundle(root, skills_home)

            self.assertEqual(snapshot_files(target), enrolled_files)
            self.assertEqual((target / "install-manifest.json").read_bytes(), json_bytes(enrolled_manifest))
            self.assertEqual(list(skills_home.iterdir()), [target])
            self.assertFalse((root / "skill-backups").exists())

    def test_manual_install_preserves_both_versions_if_target_appears_after_backup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            skills_home = root / "skills"
            target = skills_home / "engineering-handbook"
            write_file(target / "SKILL.md", b"Original manual bundle")
            write_file(target / "install-manifest.json", json_bytes({"schema_version": 1, "files": []}))
            enrolled_files = {"SKILL.md": b"Concurrent enrollment"}
            enrolled_manifest = handbook_update.make_manifest(enrolled_files, "a" * 40)
            move = handbook_update.move_manual_bundle

            def overlap(source: Path, destination: Path) -> None:
                if source.name == "bundle" and destination == target:
                    handbook_update.write_snapshot(target, enrolled_files, enrolled_manifest)
                move(source, destination)

            with (
                patch.object(handbook_update, "local_bundle", return_value={"SKILL.md": b"Replacement"}),
                patch.object(handbook_update, "verify_frozen_bundle"),
                patch.object(handbook_update, "move_manual_bundle", side_effect=overlap),
                self.assertRaisesRegex(handbook_update.UpdateBlocked, "backup preserved"),
            ):
                handbook_update.manual_bundle(root, skills_home, backup_existing=True)

            self.assertEqual(snapshot_files(target), enrolled_files)
            self.assertEqual((target / "install-manifest.json").read_bytes(), json_bytes(enrolled_manifest))
            backups = list((root / "skill-backups").iterdir())
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "SKILL.md").read_bytes(), b"Original manual bundle")
            self.assertEqual(list(skills_home.iterdir()), [target])

    @unittest.skipUnless(os.name == "posix", "POSIX regular-file recovery")
    def test_manual_rollback_keeps_regular_file_created_during_recovery(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            skills_home = root / "skills"
            target = skills_home / "engineering-handbook"
            write_file(target, b"Original manual file")
            move = handbook_update.move_manual_bundle
            link = os.link

            def stop_activation(source: Path, destination: Path) -> None:
                if source.name == "bundle" and destination == target:
                    raise OSError("Activation interrupted")
                move(source, destination)

            def new_file_before_recovery(source: Path, destination: Path) -> None:
                write_file(target, b"Concurrent manual file")
                link(source, destination)

            with (
                patch.object(handbook_update, "local_bundle", return_value={"SKILL.md": b"Replacement"}),
                patch.object(handbook_update, "verify_frozen_bundle"),
                patch.object(handbook_update, "move_manual_bundle", side_effect=stop_activation),
                patch.object(os, "link", side_effect=new_file_before_recovery),
                self.assertRaisesRegex(handbook_update.UpdateBlocked, "backup preserved"),
            ):
                handbook_update.manual_bundle(root, skills_home, backup_existing=True)

            self.assertEqual(target.read_bytes(), b"Concurrent manual file")
            (backup,) = (root / "skill-backups").iterdir()
            self.assertEqual(backup.read_bytes(), b"Original manual file")

    def test_manual_bundle_verifies_frozen_bytes_before_install_or_in_sync(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            source = root / "source"
            copy_compiled_source(source)
            skills_home = root / "skills"
            installed = skills_home / "engineering-handbook"
            backups = root / "skill-backups"

            def run(*args: str, isolated: bool = True) -> tuple[int, dict]:
                flags = ["-I", "-B", "-X", "utf8"] if isolated else ["-B", "-X", "utf8"]
                result = subprocess.run([sys.executable, *flags, str(SCRIPT), *args],
                                        cwd=root, capture_output=True, encoding="utf-8", check=False)
                self.assertTrue(result.stdout, result.stderr)
                return result.returncode, json.loads(result.stdout)

            def bundle(*options: str, isolated: bool = True) -> tuple[int, dict]:
                return run("bundle", "--source", str(source), "--skills-home", str(skills_home), *options, isolated=isolated)

            code, result = bundle(isolated=False)
            self.assertEqual((code, result["status"]), (0, "INSTALLED"), result)
            manifest = installed / "install-manifest.json"
            original_manifest = manifest.read_bytes()
            self.assertEqual(json.loads(original_manifest)["schema_version"], 1)
            original_files = snapshot_files(installed)
            write_file(installed / "references/automation/engineering_context/__pycache__/router.pyc", b"disposable cache")
            code, result = bundle("--check")
            self.assertEqual((code, result["status"]), (0, "IN_SYNC"), result)

            code, result = run("verify-bundle", "--references", str(installed / "references"))
            self.assertEqual((code, result["status"]), (0, "VERIFIED"), result)
            self.assertEqual(result["freshness_verification"], "local_recompile")
            installed_references = installed / "references"
            consumer = root / "consumer"
            consumer.mkdir()
            context = subprocess.run([
                sys.executable, "-B", "-X", "utf8", "-m", "automation.engineering_context", "context",
                "--repo", str(consumer), "--handbook", "machine-readable/compiled", "--mode", "plan",
                "--task", "Review GDPR retention and deletion in the CRM",
            ], cwd=installed_references, capture_output=True, encoding="utf-8", check=False)
            self.assertEqual(context.returncode, 0, context.stdout + context.stderr)
            self.assertEqual(json.loads(context.stdout)["schema"], "agent-context/v1")

            document = source / "governance/document-lifecycle.md"
            original_document = document.read_bytes()
            document.write_bytes(original_document + b"\nBenign stale-source fixture.\n")
            code, result = bundle("--backup-existing")
            self.assertEqual((code, result["status"]), (2, "BLOCKED"), result)
            self.assertIn("stale", result["reason"])
            self.assertEqual(snapshot_files(installed), original_files)
            self.assertEqual(manifest.read_bytes(), original_manifest)
            self.assertFalse(backups.exists())
            self.assertEqual(list(skills_home.iterdir()), [installed])
            document.write_bytes(original_document)

            artifact = "machine-readable/compiled/planning.json"
            original_artifact = (source / artifact).read_bytes()
            drifted_artifact = original_artifact.replace(b"\n", b"\r\n")
            self.assertNotEqual(drifted_artifact, original_artifact)
            (source / artifact).write_bytes(drifted_artifact)
            # Model a stale v1 installation copied by an older manual installer.
            (installed_references / artifact).write_bytes(drifted_artifact)
            drifted_manifest = json.loads(original_manifest)
            for entry in drifted_manifest["files"]:
                if entry["install_path"] == f"references/{artifact}":
                    entry["sha256"] = digest(drifted_artifact)
            manifest.write_bytes(json_bytes(drifted_manifest))
            code, result = bundle("--check")
            self.assertEqual((code, result["status"]), (2, "BLOCKED"), result)
            self.assertIn("planning.json", result["reason"])
            self.assertEqual((installed_references / artifact).read_bytes(), drifted_artifact)
            self.assertEqual(manifest.read_bytes(), json_bytes(drifted_manifest))
            self.assertFalse(backups.exists())

            (source / artifact).write_bytes(original_artifact)
            code, result = bundle("--backup-existing")
            self.assertEqual((code, result["status"]), (0, "INSTALLED"), result)
            backup = Path(result["backup"])
            self.assertEqual(backup.parent, backups)
            self.assertEqual((backup / "references" / artifact).read_bytes(), drifted_artifact)
            self.assertEqual(snapshot_files(installed), original_files)

    def test_powershell_preview_and_stale_replacement_preserve_installation(self) -> None:
        pwsh = shutil.which("pwsh")
        if pwsh is None:
            self.skipTest("pwsh is unavailable")
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            source = root / "source"
            copy_compiled_source(source)
            ps_relative = Path("automation/codex/sync-handbook-skill.ps1")
            script = source / ps_relative
            write_file(script, (ROOT / ps_relative).read_bytes())
            write_file(source / SCRIPT.relative_to(ROOT), SCRIPT.read_bytes())
            skills_home = root / "skills"
            installed = skills_home / "engineering-handbook"
            backup_root = root / "skill-backups"
            previous_backup = backup_root / "engineering-handbook.backup-existing/SKILL.md"
            write_file(previous_backup, b"Previous backup")

            def run(*options: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run([
                    pwsh, "-NoProfile", "-NonInteractive", "-File", str(script),
                    "-Mode", "Install", "-SkillsHome", str(skills_home), *options,
                ], cwd=root, capture_output=True, encoding="utf-8", check=False)

            result = run()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("INSTALLED", result.stdout)
            manifest = installed / "install-manifest.json"
            original_manifest = manifest.read_bytes()
            self.assertEqual(json.loads(original_manifest.decode("utf-8-sig"))["schema_version"], 1)
            original_files = snapshot_files(installed)
            original_backups = list(backup_root.iterdir())

            document = source / "governance/document-lifecycle.md"
            original_document = document.read_bytes()
            document.write_bytes(original_document + b"\nBenign stale-source fixture.\n")
            result = run("-BackupExisting", "-WhatIf")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PREVIEW", result.stdout)
            self.assertEqual(snapshot_files(installed), original_files)
            self.assertEqual(manifest.read_bytes(), original_manifest)
            self.assertEqual(list(backup_root.iterdir()), original_backups)

            result = run("-BackupExisting")
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Handbook corpus verification failed", result.stdout + result.stderr)
            self.assertIn("stale", result.stdout + result.stderr)
            self.assertEqual(snapshot_files(installed), original_files)
            self.assertEqual(manifest.read_bytes(), original_manifest)
            self.assertEqual(list(backup_root.iterdir()), original_backups)
            self.assertEqual(previous_backup.read_bytes(), b"Previous backup")
            self.assertEqual(list(skills_home.iterdir()), [installed])

            document.write_bytes(original_document)
            local_file = installed / "notes.txt"
            write_file(local_file, b"Previous local notes")
            result = run("-BackupExisting")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("INSTALLED", result.stdout)
            (backup,) = set(backup_root.iterdir()) - set(original_backups)
            self.assertEqual((backup / local_file.name).read_bytes(), b"Previous local notes")
            self.assertEqual(snapshot_files(installed), original_files)
