from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class SkillBundleTests(unittest.TestCase):
    def test_generated_python_cache_is_not_canonical_skill_source(self) -> None:
        with tempfile.TemporaryDirectory(prefix="handbook-skill-") as temporary:
            root = Path(temporary)
            script = root / "automation/codex/sync-handbook-skill.ps1"
            script.parent.mkdir(parents=True)
            shutil.copyfile(Path(__file__).resolve().parents[2] / script.relative_to(root), script)
            skill = root / "agent-config/codex/skills/engineering-handbook"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Canonical router", encoding="utf-8")
            (skill / "bundle.json").write_text(json.dumps({
                "schema_version": 1, "skill_name": "engineering-handbook",
                "include": ["automation/engineering_context"],
            }), encoding="utf-8")
            source = root / "automation/engineering_context"
            cache = source / "__pycache__"
            cache.mkdir(parents=True)
            (source / "router.py").write_text("# canonical", encoding="utf-8")
            (source / "router.pyc").write_bytes(b"legacy cache")
            (cache / "router.cpython-312.pyc").write_bytes(b"warm cache")
            target = root / "installed"

            def run(mode: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run([
                    "pwsh", "-NoProfile", "-File", str(script), "-Mode", mode,
                    "-SkillsHome", str(target),
                ], capture_output=True, text=True, check=False)

            installed = run("Install")
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            manifest = json.loads((target / "engineering-handbook/install-manifest.json").read_text(encoding="utf-8-sig"))
            paths = [entry["source_path"] for entry in manifest["files"]]
            self.assertIn("automation/engineering_context/router.py", paths)
            self.assertFalse(any("__pycache__" in path or path.endswith(".pyc") for path in paths), paths)
            (cache / "router.cpython-312.pyc").write_bytes(b"changed generated cache")
            installed_cache = target / "engineering-handbook/references/automation/engineering_context/__pycache__"
            installed_cache.mkdir()
            (installed_cache / "router.cpython-312.pyc").write_bytes(b"installed runtime cache")
            self.assertEqual(run("Check").returncode, 0)
            unexpected = target / "engineering-handbook/unexpected.txt"
            unexpected.write_text("not generated cache", encoding="utf-8")
            self.assertEqual(run("Check").returncode, 2)
            unexpected.unlink()
            (source / "router.py").write_text("# changed source", encoding="utf-8")
            self.assertEqual(run("Check").returncode, 2)
