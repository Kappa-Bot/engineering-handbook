from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
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

    def test_manual_v1_check_accepts_both_bundle_producers_and_rejects_invalid_receipts(self) -> None:
        pwsh = shutil.which("pwsh")
        if pwsh is None:
            self.skipTest("pwsh is unavailable")
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            source = root / "source"
            copy_compiled_source(source)
            ps_relative = Path("automation/codex/sync-handbook-skill.ps1")
            write_file(source / ps_relative, (ROOT / ps_relative).read_bytes())
            write_file(source / SCRIPT.relative_to(ROOT), SCRIPT.read_bytes())
            python_home = root / "python"
            powershell_home = root / "powershell"

            def run_python(home, *options):
                return subprocess.run([
                    sys.executable, "-I", "-B", "-X", "utf8", str(SCRIPT),
                    "bundle", "--source", str(source), "--skills-home", str(home), *options,
                ], cwd=root, capture_output=True, encoding="utf-8", check=False)

            def run_powershell(home, mode, *options):
                return subprocess.run([
                    pwsh, "-NoProfile", "-NonInteractive", "-File", str(source / ps_relative),
                    "-Mode", mode, "-SkillsHome", str(home), *options,
                ], cwd=root, capture_output=True, encoding="utf-8", check=False)

            for result in (run_python(python_home), run_powershell(powershell_home, "Install")):
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            python_target = python_home / "engineering-handbook"
            powershell_target = powershell_home / "engineering-handbook"
            self.assertEqual(snapshot_files(python_target), snapshot_files(powershell_target))
            for target in (python_target, powershell_target):
                write_file(target / "references/automation/engineering_context/__pycache__/fixture.pyc",
                           b"Generated cache")
            python_manifest = python_target / "install-manifest.json"
            powershell_manifest = powershell_target / "install-manifest.json"
            python_original = python_manifest.read_bytes()
            powershell_original = powershell_manifest.read_bytes()
            self.assertEqual(json.loads(python_original)["source_repository"], handbook_update.CANONICAL_REMOTE)
            self.assertEqual(json.loads(powershell_original.decode("utf-8-sig"))["source_repository"],
                             "Kappa-Bot/engineering-handbook")

            python_result = run_python(powershell_home, "--check")
            ps_result = run_powershell(python_home, "Check")
            self.assertEqual(python_result.returncode, 0, python_result.stdout + python_result.stderr)
            self.assertEqual(json.loads(python_result.stdout)["status"], "IN_SYNC")
            self.assertEqual(ps_result.returncode, 0, ps_result.stdout + ps_result.stderr)
            self.assertTrue(ps_result.stdout.startswith("IN_SYNC"), ps_result.stdout)
            self.assertEqual(python_manifest.read_bytes(), python_original)
            self.assertEqual(powershell_manifest.read_bytes(), powershell_original)
            self.assertFalse((root / "skill-backups").exists())

            original = json.loads(python_original)
            first_row, *other_rows = original["files"]
            invalid_receipts = {
                "wrong-source": dict(original, source_repository="Other/Repository"),
                "wrong-schema": dict(original, schema_version=3),
                "array-header": dict(original, skill_name=["engineering-handbook"],
                                     source_repository=[handbook_update.CANONICAL_REMOTE]),
                "array-root": [original],
                "files-object": dict(original, files=first_row),
                "array-row": dict(original, files=[[first_row], *other_rows]),
                **{
                    f"array-{field}": dict(original, files=[dict(first_row, **{field: [first_row[field]]}), *other_rows])
                    for field in ("install_path", "source_path", "sha256")
                },
                **{
                    f"wrong-case-{field}": dict(original, files=[dict(first_row, **{field: first_row[field].swapcase()}), *other_rows])
                    for field in ("install_path", "source_path")
                },
                "duplicate-row": dict(original, files=[*original["files"], first_row]),
            }
            for case, invalid in invalid_receipts.items():
                with self.subTest(case=case):
                    payload = json_bytes(invalid)
                    python_manifest.write_bytes(payload)
                    python_result = run_python(python_home, "--check")
                    ps_result = run_powershell(python_home, "Check")
                    self.assertEqual(python_result.returncode, 2, python_result.stdout + python_result.stderr)
                    expected_status = "BLOCKED" if case == "array-root" else "OUT_OF_SYNC"
                    self.assertEqual(json.loads(python_result.stdout)["status"], expected_status)
                    self.assertEqual(ps_result.returncode, 2, ps_result.stdout + ps_result.stderr)
                    self.assertTrue(ps_result.stdout.startswith("OUT_OF_SYNC"), ps_result.stdout)
                    self.assertEqual(python_manifest.read_bytes(), payload)

            preview = run_powershell(python_home, "Install", "-BackupExisting", "-WhatIf")
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertIn("PREVIEW", preview.stdout)
            self.assertEqual(python_manifest.read_bytes(), json_bytes(invalid_receipts["duplicate-row"]))
            self.assertFalse((root / "skill-backups").exists())

            enrolled = json_bytes(dict(original, schema_version=2))
            python_manifest.write_bytes(enrolled)
            python_result = run_python(python_home, "--backup-existing")
            ps_result = run_powershell(python_home, "Install", "-BackupExisting")
            self.assertEqual(python_result.returncode, 2, python_result.stdout + python_result.stderr)
            self.assertEqual(json.loads(python_result.stdout)["status"], "BLOCKED")
            self.assertIn("enrolled", json.loads(python_result.stdout)["reason"])
            self.assertNotEqual(ps_result.returncode, 0, ps_result.stdout + ps_result.stderr)
            self.assertIn("Enrolled Handbook target", ps_result.stdout + ps_result.stderr)
            self.assertEqual(python_manifest.read_bytes(), enrolled)
            self.assertFalse((root / "skill-backups").exists())

    def test_powershell_rechecks_verified_target_before_reporting_sync(self) -> None:
        pwsh = shutil.which("pwsh")
        if pwsh is None:
            self.skipTest("pwsh is unavailable")
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            source = root / "source"
            copy_compiled_source(source)
            ps_relative = Path("automation/codex/sync-handbook-skill.ps1")
            installer = source / ps_relative
            write_file(installer, (ROOT / ps_relative).read_bytes())
            write_file(source / SCRIPT.relative_to(ROOT), SCRIPT.read_bytes())
            skills_home = root / "skills"
            installed = skills_home / "engineering-handbook"
            prefix = [pwsh, "-NoProfile", "-NonInteractive", "-File"]
            initial = subprocess.run([
                *prefix, str(installer), "-Mode", "Install", "-SkillsHome", str(skills_home),
            ], cwd=root, capture_output=True, encoding="utf-8", check=False, timeout=45)
            self.assertEqual(initial.returncode, 0, initial.stdout + initial.stderr)
            self.assertIn("INSTALLED", initial.stdout)

            wrapper = root / "verify-barrier.ps1"
            wrapper.write_text("""param($Installer, $SkillsHome, $Mode, $Ready, $Resume)
$callback = {
    [IO.File]::AppendAllText($Ready, "verify`n")
    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    while (-not [IO.File]::Exists($Resume)) {
        if ([DateTime]::UtcNow -gt $deadline) { throw "Timed out at verifier barrier" }
        Start-Sleep -Milliseconds 20
    }
}.GetNewClosure()
Set-PSBreakpoint -Script $Installer -Command Assert-BundleFreshness -Action $callback | Out-Null
try {
    & $Installer -Mode $Mode -SkillsHome $SkillsHome
    exit $LASTEXITCODE
}
catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
""", encoding="utf-8")
            manifest = installed / "install-manifest.json"
            original_manifest = manifest.read_bytes()
            original_inventory = snapshot_files(installed)
            write_file(installed / "references/automation/engineering_context/__pycache__/fixture.pyc",
                       b"Generated cache")

            def invoke(mode, edit=None):
                stem = mode + ("-interleaved" if edit else "-quiet")
                ready, resume = root / f"{stem}.ready", root / f"{stem}.resume"
                if edit is None:
                    resume.touch()
                with subprocess.Popen([
                    *prefix, str(wrapper), str(installer), str(skills_home), mode, str(ready), str(resume),
                ], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8") as process:
                    try:
                        if edit is not None:
                            deadline = time.monotonic() + 25
                            while not ready.is_file() and process.poll() is None and time.monotonic() < deadline:
                                time.sleep(0.02)
                            if ready.is_file():
                                edit.write_bytes(edit.read_bytes() + b"\nBenign concurrent edit.\n")
                    finally:
                        resume.touch()
                    try:
                        stdout, stderr = process.communicate(timeout=40)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        self.fail(f"{stem} did not finish after releasing the verifier")
                self.assertTrue(ready.is_file(), stdout + stderr)
                self.assertEqual(ready.read_text(encoding="utf-8").splitlines(), ["verify"])
                return process.returncode, stdout, stderr

            modes = (
                ("Check", "IN_SYNC", "SKILL.md", 2),
                ("Install", "ALREADY_IN_SYNC", "references/agent-config/codex/AGENTS.global.md", 1),
            )
            for mode, success, relative, failure_code in modes:
                with self.subTest(mode=mode):
                    code, stdout, stderr = invoke(mode)
                    self.assertEqual(code, 0, stdout + stderr)
                    self.assertTrue(stdout.startswith(success + " "), stdout)
                    edit = installed / relative
                    original = edit.read_bytes()
                    try:
                        code, stdout, stderr = invoke(mode, edit)
                        self.assertEqual(edit.read_bytes(), original + b"\nBenign concurrent edit.\n")
                        self.assertEqual(code, failure_code, stdout + stderr)
                        self.assertFalse(stdout.startswith(success + " "), stdout)
                        if mode == "Check":
                            self.assertTrue(stdout.startswith("OUT_OF_SYNC "), stdout)
                        self.assertIn(f"{relative} changed during verification", stdout + stderr)
                        self.assertEqual(manifest.read_bytes(), original_manifest)
                        self.assertFalse((root / "skill-backups").exists())
                    finally:
                        edit.write_bytes(original)
            self.assertEqual(snapshot_files(installed), original_inventory)

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
