import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from automation.engineering_context.canonical import canonical_json, stable_hash
from automation.engineering_context.cli import _load_compiled, cmd_context, main
from automation.engineering_context.conformance import project_conformance
from automation.engineering_context.context_solver import ContextBudget, solve_context, build_repo_route
from automation.engineering_context.discovery import search
from automation.engineering_context.handbook_compile import compile_handbook, check_compiled_fresh
from automation.engineering_context.handbook_source import AgentContextError, extract_agent_context
from automation.engineering_context.planning_ir import PlanningIR, VerificationRequirement, new_planning_ir, validate_planning_ir, capsule_delta, planning_ir_from_dict
from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import TaskDescriptor, describe_task, merge_agent_resolution

ROOT = Path(__file__).resolve().parents[2]
COMPILED = ROOT / "machine-readable" / "compiled"


def load_compiled(phase="planning"):
    view = json.loads((COMPILED / f"{phase}.json").read_text(encoding="utf-8"))
    routing = json.loads((COMPILED / "routing.json").read_text(encoding="utf-8"))
    return {"units": view["units"], "routing": routing}


def source_doc(source_id, units, prose="Canonical prose"):
    return f'''---\nid: {source_id}\n---\n\n# X\n\n{prose}\n\n```json agent-context\n{json.dumps({"units": units}, indent=2)}\n```\n'''


def unit(uid, covers=(), activate_when=(), *, activate_all=(), phase=("planning",), force=None, priority=50, kind="decision-question"):
    data = {"id": uid, "type": kind, "text": f"{uid} text", "source": "std-test", "covers": list(covers), "activate_when": list(activate_when), "phase": list(phase), "priority": priority}
    if activate_all:
        data["activate_all"] = list(activate_all)
    if force:
        data["force"] = force
    return data


def compiled_unit(raw, tokens=20):
    return {**raw, "sources": [raw.get("source", "std-test")], "estimated_tokens": tokens}


class PipelineContractTests(unittest.TestCase):
    def test_agent_tooling_context_routes_trust_boundary_in_each_phase(self):
        profile = {"detected": {"capabilities": {}}}
        tasks = (
            ("Evaluate ECC for our coding workflow", ()),
            ("Revisa los hooks de Codex y el servidor MCP", ()),
            ("Review execution settings", (".codex/config.toml",)),
            ("Review execution settings", (".claude/hooks/check.js",)),
            ("Review execution settings", (".mcp.json",)),
            ("Review execution settings", (".agents/skills/review/SKILL.md",)),
            ("Review execution settings", (".claude/settings.json",)),
            ("Review execution settings", (".codex-plugin/plugin.json",)),
            ("Review execution settings", ("apps/web/.mcp.json",)),
            ("Review execution settings", (".\\.codex\\config.toml",)),
            ("Install a Claude Code plugin", ()),
            ("Install a plugin in Codex", ()),
            ("Instala un plugin en Codex", ()),
            ("Update hook configuration", ("hooks/codex-hooks.json",)),
            ("Repair session bootstrap", ("scripts/hooks/session-start-bootstrap.js",)),
            ("Repair plugin bootstrap", ("scripts/hooks/plugin-hook-bootstrap.js",)),
        )
        for task, changed in tasks:
            with self.subTest(task=task, changed=changed):
                descriptor = describe_task(task, profile, changed)
                self.assertIn("agent-tooling-change", descriptor.archetypes)
                self.assertIn("agent-execution", descriptor.risks)
                for phase in ("planning", "implementation", "verification"):
                    capsule = solve_context(load_compiled(phase), descriptor, phase)
                    self.assertIn("agent-tools-review-execution-boundary", {u["id"] for u in capsule.units})
                    self.assertIn("agent-execution", capsule.covered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_learning_routes_reviewed_promotion_not_global_observation(self):
        for task, changed in (
            ("Configurar aprendizaje continuo y memoria del agente", ()),
            ("Update Codex memory", ()),
            ("Actualiza la memoria de Codex", ()),
            ("Persist learned rules for the coding agent", ()),
            ("Review the learner", (".claude/skills/continuous-learning-v2/SKILL.md",)),
            ("Review observed rules", (".claude/homunculus/instincts/personal/review.yaml",)),
            ("Review observed rules", (".local/share/ecc-homunculus/instincts/personal/review.yaml",)),
            ("Review observed rules", ("custom/data/ecc-homunculus/instincts/personal/review.yaml",)),
            ("Review the observer", ("skills/continuous-learning-v2/agents/observer-loop.sh",)),
        ):
            with self.subTest(task=task, changed=changed):
                descriptor = describe_task(task, {"detected": {"capabilities": {}}}, changed)
                self.assertIn("agent-learning-change", descriptor.archetypes)
                for phase in ("planning", "implementation", "verification"):
                    capsule = solve_context(load_compiled(phase), descriptor, phase)
                    ids = {u["id"] for u in capsule.units}
                    self.assertIn("agent-learning-reviewed-promotion", ids)
                    self.assertIn("learned-authority", capsule.covered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_agent_guidance_does_not_pollute_unrelated_context(self):
        for task, changed in (
            ("Fix React hooks in the settings page", ("src/hooks/useForm.ts",)),
            ("Repair the payment webhook", ("src/webhooks/payment.ts",)),
            ("Diagnose a server memory leak", ("src/cache.ts",)),
            ("Correct a typo in the handbook", ("README.md",)),
            ("Add ECC support to the cryptography backend", ("src/crypto/ecc.py",)),
            ("Tune the continuous learning rate of an online recommender", ("src/learner.py",)),
            ("Fix React hooks in Codex dashboard", ("src/hooks/useForm.ts",)),
            ("Diagnose a memory leak in Codex dashboard", ("src/cache.ts",)),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, {"detected": {"capabilities": {}}}, changed)
                self.assertNotIn("agent-tooling-change", descriptor.archetypes)
                self.assertNotIn("agent-learning-change", descriptor.archetypes)
                for phase in ("planning", "implementation", "verification"):
                    ids = {u["id"] for u in solve_context(load_compiled(phase), descriptor, phase).units}
                    self.assertNotIn("agent-tools-review-execution-boundary", ids)
                    self.assertNotIn("agent-learning-reviewed-promotion", ids)

    def test_cli_json_remains_readable_through_legacy_pipes(self):
        query = "Política — 日本語"
        command = [sys.executable, "-B", "-m", "automation.engineering_context",
                   "search", "--root", str(ROOT), "--query", query]
        for options in ([], ["--pretty"]):
            with self.subTest(options=options):
                emit = [*command, *options]
                utf8 = subprocess.run(emit, cwd=ROOT, capture_output=True,
                                      env={**os.environ, "PYTHONIOENCODING": "utf-8"})
                legacy = subprocess.run(emit, cwd=ROOT, capture_output=True,
                                        env={**os.environ, "PYTHONIOENCODING": "cp1252"})
                self.assertEqual(utf8.returncode, 0, utf8.stderr)
                self.assertEqual(legacy.returncode, 0, legacy.stderr)
                self.assertEqual(json.loads(legacy.stdout), json.loads(utf8.stdout))
                self.assertEqual(json.loads(legacy.stdout)["query"], query)
                self.assertTrue(legacy.stdout.isascii())
                self.assertIn(query.encode("utf-8"), utf8.stdout)

    def test_canonical_json_and_hash_are_order_stable(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}\n')
        self.assertEqual(stable_hash({"a":1,"b":2}), stable_hash({"b":2,"a":1}))

    def test_source_parser_ignores_free_prose(self):
        self.assertEqual(extract_agent_context("# prose only", "x.md"), [])

    def test_source_parser_rejects_source_mismatch(self):
        bad = unit("u")
        bad["source"] = "wrong"
        with self.assertRaises(AgentContextError):
            extract_agent_context(source_doc("std-test", [bad]), "x.md")

    def test_source_parser_rejects_non_string_type_and_force(self):
        bad_type = unit("bad-type"); bad_type["type"] = ["constraint"]
        with self.assertRaises(AgentContextError):
            extract_agent_context(source_doc("std-test", [bad_type]), "bad-type.md")
        bad_force = unit("bad-force"); bad_force["force"] = ["must"]
        with self.assertRaises(AgentContextError):
            extract_agent_context(source_doc("std-test", [bad_force]), "bad-force.md")

    def test_agent_context_rejects_duplicate_object_members(self):
        doc = source_doc("std-test", [unit("sample", covers=("risk", "risk"), force="must")])
        for original, replacement, member in (
            ('"units": [', '"units": [], "units": [', "units"),
            ('"force": "must"', '"force": "may", "force": "must"', "force"),
            ('"priority": 50', r'"priority": 50, "prior\u0069ty": 50', "priority"),
            ('"units": [', '"extra": {"note": 1, "note": 2}, "units": [', "note"),
        ):
            with self.subTest(member=member):
                with self.assertRaisesRegex(AgentContextError, rf"source\.md: duplicate agent-context JSON member '{member}'"):
                    extract_agent_context(doc.replace(original, replacement), "source.md")

        valid = doc.replace('"units": [', '"extra": {"note": 1, "Note": 2}, "units": [')
        parsed = extract_agent_context(valid, "source.md")
        self.assertEqual(parsed[0].covers, ("risk", "risk"))

    def test_source_parser_rejects_boolean_priority(self):
        for value in (False, True):
            with self.subTest(value=value):
                with self.assertRaisesRegex(AgentContextError, "priority must be integer from 0 to 100"):
                    extract_agent_context(source_doc("std-test", [unit("sample", priority=value)]), "priority.md")
        for value in (0, 50, 100):
            with self.subTest(value=value):
                parsed = extract_agent_context(source_doc("std-test", [unit("sample", priority=value)]), "priority.md")
                self.assertEqual(parsed[0].priority, value)

    def test_compiler_is_byte_stable_and_prose_only_change_does_not_invalidate_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"standards").mkdir(); out=root/"compiled"
            u=unit("u", ("compatibility",), ("risk:compatibility",))
            path=root/"standards/x.md"; path.write_text(source_doc("std-test", [u], "first prose"))
            compile_handbook(root,out); before={p.name:p.read_bytes() for p in out.iterdir()}
            second=compile_handbook(root,out)
            self.assertEqual(second.changed_files, ())
            path.write_text(source_doc("std-test", [u], "editorial prose changed"))
            third=compile_handbook(root,out); after={p.name:p.read_bytes() for p in out.iterdir()}
            self.assertEqual(third.changed_files, ())
            self.assertEqual(before, after)
            self.assertEqual(check_compiled_fresh(root,out), [])

    def test_compiler_repairs_an_older_planning_phase_without_reusing_it(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "standards/test.md"
            source.parent.mkdir()
            output = root / "machine-readable/compiled"
            planning = output / "planning.json"
            record = unit("sample")
            source.write_text(source_doc("std-test", [record]), encoding="utf-8")
            compile_handbook(root, output)
            older_phase = planning.read_bytes()
            record["text"] = "Current source wording"
            source.write_text(source_doc("std-test", [record]), encoding="utf-8")
            compile_handbook(root, output)
            expected = {path.name: path.read_bytes() for path in output.iterdir()}
            self.assertEqual(compile_handbook(root, output).skipped_sources, ("std-test",))

            planning.write_bytes(older_phase)
            self.assertTrue(check_compiled_fresh(root, output))
            repaired = compile_handbook(root, output)
            self.assertEqual(repaired.changed_files, ("planning.json",))
            self.assertEqual(repaired.skipped_sources, ())
            self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, expected)
            self.assertEqual(check_compiled_fresh(root, output), [])

            malformed = json.loads(planning.read_bytes())
            malformed["units"][0]["text"] = "Incomplete Unicode scalar " + chr(0xD800)
            planning.write_text(json.dumps(malformed), encoding="utf-8")
            repaired = compile_handbook(root, output)
            self.assertEqual(repaired.changed_files, ("planning.json",))
            self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, expected)

            manifest = output / "manifest.json"
            legacy = json.loads(manifest.read_bytes())
            legacy.pop("artifact_hashes")
            manifest.write_text(canonical_json(legacy), encoding="utf-8")
            planning.write_bytes(older_phase)
            regenerated = compile_handbook(root, output)
            self.assertEqual(regenerated.skipped_sources, ())
            self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, expected)
            self.assertEqual(compile_handbook(root, output).skipped_sources, ("std-test",))

    def test_compiler_uses_canonical_units_even_with_a_self_consistent_cached_phase(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "standards" / "cache.md"
            source.parent.mkdir()
            output = root / "machine-readable" / "compiled"
            current = unit("required-review")
            current["force"] = "must"
            current["text"] = "Current source requires the synthetic receipt."
            source.write_text(source_doc("std-test", [current, unit("second-unit")]), encoding="utf-8")
            compile_handbook(root, output)
            expected = {path.name: path.read_bytes() for path in output.iterdir()}
            manifest_path = output / "manifest.json"
            planning_path = output / "planning.json"

            for drift in ("cached-record", "partial-unit-ids", "null-source-entry"):
                with self.subTest(drift=drift):
                    manifest = json.loads(manifest_path.read_bytes())
                    if drift == "cached-record":
                        planning = json.loads(planning_path.read_bytes())
                        planning["units"][0]["force"] = "may"
                        planning_path.write_text(canonical_json(planning), encoding="utf-8", newline="\n")
                        manifest["artifact_hashes"]["planning.json"] = stable_hash(planning)
                    elif drift == "partial-unit-ids":
                        manifest["sources"]["std-test"]["unit_ids"] = ["second-unit"]
                    else:
                        manifest["sources"]["std-test"] = None
                    manifest_path.write_text(canonical_json(manifest), encoding="utf-8", newline="\n")
                    self.assertEqual(compile_handbook(root, output).skipped_sources, ())
                    self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, expected)
                    self.assertEqual(check_compiled_fresh(root, output), [])
            self.assertEqual(compile_handbook(root, output).skipped_sources, ("std-test",))

    def test_compiler_checks_phase_prerequisites_before_replacing_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "standards/example.md"
            path.parent.mkdir()
            output = root / "machine-readable/compiled"
            dependent = unit("phase-dependent", phase=("planning", "verification"))
            dependent["requires"] = ["phase-prerequisite"]
            prerequisite = unit("phase-prerequisite", phase=())
            path.write_text(source_doc("std-test", [dependent, prerequisite]), encoding="utf-8")
            compile_handbook(root, output)
            previous = {item.name: item.read_bytes() for item in output.iterdir()}

            for dependent_phases, prerequisite_phases, missing in (
                (["planning", "verification"], ["verification"], "planning"),
                (None, ["planning"], "implementation, verification"),
            ):
                with self.subTest(dependent_phases=dependent_phases, prerequisite_phases=prerequisite_phases):
                    narrowed = {**dependent, "phase": dependent_phases}
                    if dependent_phases is None:
                        narrowed.pop("phase")
                    target = {**prerequisite, "phase": prerequisite_phases}
                    path.write_text(source_doc("std-test", [narrowed, target]), encoding="utf-8")
                    with self.assertRaisesRegex(
                        AgentContextError,
                        f"unit phase-dependent requires phase-prerequisite, unavailable in phases: {missing}",
                    ):
                        compile_handbook(root, output)
                    self.assertEqual({item.name: item.read_bytes() for item in output.iterdir()}, previous)

    def test_compiler_rejects_duplicate_source_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"standards").mkdir()
            (root/"standards/a.md").write_text(source_doc("std-test", [unit("a")]))
            (root/"standards/b.md").write_text(source_doc("std-test", [unit("b")]))
            with self.assertRaises(AgentContextError):
                compile_handbook(root, root/"compiled")

    def test_catalog_disables_inactive_context_even_with_warm_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "standards/x.md"
            source.parent.mkdir()
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            output = catalog.parent / "compiled"
            markdown = source_doc("std-test", [unit("u", activate_when=("risk:compatibility",))]).replace(
                "id: std-test\n", "id: std-test\nkind: standard\nstatus: active\n", 1
            )
            catalog_source = (
                "documents:\n  - id: std-test\n    kind: standard\n"
                "    path: standards/x.md\n    status: active\n    applies_to: [handbook]\n"
            )
            source.write_text(markdown, encoding="utf-8")
            catalog.write_text(catalog_source, encoding="utf-8")
            compile_handbook(root, output)
            active = json.loads((output / "planning.json").read_bytes())
            self.assertEqual([item["id"] for item in active["units"]], ["u"])
            self.assertEqual(json.loads((output / "routing.json").read_bytes()), {"risk:compatibility": ["u"]})

            source.write_text(markdown.replace("status: active", "status: superseded"), encoding="utf-8")
            with self.assertRaisesRegex(AgentContextError, "context source/catalog status mismatch"):
                compile_handbook(root, output)
            catalog.write_text(catalog_source.replace("status: active", "status: superseded"), encoding="utf-8")
            compile_handbook(root, output)
            self.assertEqual(json.loads((output / "planning.json").read_bytes())["units"], [])
            self.assertEqual(json.loads((output / "manifest.json").read_bytes())["sources"], {})
            self.assertEqual(json.loads((output / "routing.json").read_bytes()), {})
            index = json.loads((output / "discovery.json").read_bytes())
            self.assertEqual(search(index, "std-test"), [])
            self.assertEqual([item["id"] for item in search(index, "std-test", historical=True)], ["std-test"])
            self.assertFalse(any(edge["type"] == "projects" for edge in index["edges"]))

    def test_catalog_rejects_uncataloged_context_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "standards/x.md"
            source.parent.mkdir()
            source.write_text(source_doc("std-test", [unit("u")]), encoding="utf-8")
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            catalog.write_text("documents:\n", encoding="utf-8")
            with self.assertRaisesRegex(AgentContextError, "not a governed catalog entry"):
                compile_handbook(root, catalog.parent / "compiled")

            catalog.unlink()
            (catalog.parent / "discovery").mkdir()
            with self.assertRaisesRegex(AgentContextError, "missing catalog for Handbook discovery"):
                compile_handbook(root, catalog.parent / "compiled")

    def test_profile_reads_utf8_package_signature_and_hashes_original_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package.json"
            manifest = b'{"scripts":{"test":"node --version"},"dependencies":{"next-auth":"1.0.0"}}'
            package.write_bytes(manifest)
            plain = profile_repo(root)
            package.write_bytes(b"\xef\xbb\xbf" + manifest)
            signed = profile_repo(root)
            self.assertEqual(signed["detected"], plain["detected"])
            self.assertEqual(signed["detected"]["commands"], {"test": "node --version"})
            self.assertTrue(signed["detected"]["capabilities"]["auth"])
            for segment in ("runtime", "verification"):
                self.assertNotEqual(signed["meta"]["segment_hashes"][segment], plain["meta"]["segment_hashes"][segment])
            package.write_bytes(b"\xef\xbb")
            with self.assertRaises(UnicodeDecodeError):
                profile_repo(root)

    def test_profile_reports_malformed_package_metadata_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package.json"
            for value, message in (
                ([], "package.json must be a JSON object"),
                ({"scripts": None}, "package.json scripts must be a JSON object"),
                ({"dependencies": []}, "package.json dependencies must be a JSON object"),
                ({"devDependencies": "fixture"}, "package.json devDependencies must be a JSON object"),
            ):
                with self.subTest(value=value):
                    package.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message):
                        profile_repo(root)
            package.write_text('{"scripts":{"test":"python -m unittest"}}', encoding="utf-8")
            self.assertEqual(profile_repo(root)["detected"]["commands"], {"test": "python -m unittest"})

    def test_load_compiled_requires_all_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises((FileNotFoundError, ValueError)):
                _load_compiled(Path(td), "planning")

    def test_context_rejects_incomplete_compiled_input_before_traversing_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wrong = root / "wrong"
            wrong.mkdir()
            (wrong / "manifest.json").write_text('{"files": []}', encoding="utf-8")
            regular = root / "file.json"
            regular.write_text("{}", encoding="utf-8")
            for directory in (root / "absent", regular, wrong):
                with self.subTest(directory=directory):
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with (
                        mock.patch("automation.engineering_context.cli.verified_compiled_payloads") as freshness,
                        redirect_stdout(stdout),
                        redirect_stderr(stderr),
                    ):
                        self.assertEqual(main([
                            "context", "--repo", str(root), "--handbook", str(directory),
                            "--mode", "plan", "--task", "Review pagination behavior",
                        ]), 2)
                    freshness.assert_not_called()
                    self.assertEqual(stdout.getvalue(), "")
                    self.assertIn("--handbook must point to a complete compiled context directory", stderr.getvalue())
                    self.assertIn("graph.json", stderr.getvalue())

    def test_context_reports_metric_scope_and_rejects_stale_compiled_corpus(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"standards").mkdir(); compiled=root/"machine-readable/compiled"
            source=root/"standards/x.md"; u=unit("freshness", ("performance",), ("risk:performance",))
            source.write_text(source_doc("std-test", [u])); compile_handbook(root, compiled)
            repo=root/"consumer"; repo.mkdir()
            args=SimpleNamespace(mode="plan", repo=repo, task="reduce API latency", changed=[], handbook=compiled, base_context=None, metrics=True, pretty=False)
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(cmd_context(args), 0)
            payload = json.loads(output.getvalue())
            metrics = payload["metrics"]
            self.assertEqual(metrics["estimated_tokens_scope"], "selected-unit-text")
            capsule = payload["capsule"]
            self.assertEqual(metrics["estimated_tokens"], sum(unit["estimated_tokens"] for unit in capsule["units"]))
            self.assertEqual(metrics["canonical_capsule_utf8_bytes"], len(canonical_json(capsule).encode("utf-8")))
            self.assertEqual(metrics["full_source_reads"], 0)
            self.assertEqual(metrics["full_source_reads_scope"], "capsule")
            self.assertEqual(metrics["freshness_verification"], "local_recompile")

            u["text"]="changed contract text"; source.write_text(source_doc("std-test", [u]))
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    cmd_context(args)

    def test_activate_all_requires_every_predicate(self):
        u=unit("pwa-mutation", ("data-loss",), (), activate_all=("capability:pwa","operation:mutation"))
        compiled={"units":[compiled_unit(u,10)],"routing":{"capability:pwa":["pwa-mutation"],"operation:mutation":["pwa-mutation"]}}
        only_mutation=describe_task("update record", {"detected":{"capabilities":{"persistence":True}}})
        self.assertEqual(solve_context(compiled, only_mutation, "planning").units, ())

    def test_marketing_hero_tasks_route_to_the_specific_pattern_without_misrouting_webhooks(self):
        descriptor=describe_task("Refine the Tommy animated hero on a public website", {"detected":{"capabilities":{}}})
        self.assertIn("frontend", descriptor.surfaces)
        self.assertIn("marketing-hero-change", descriptor.archetypes)
        self.assertIn("hero-fidelity", descriptor.risks)
        capsule=solve_context(load_compiled("planning"), descriptor, "planning")
        self.assertIn("marketing-hero-brief-and-source", {u["id"] for u in capsule.units})
        webhook=describe_task("repair webhook failure", {"detected":{"capabilities":{}}})
        self.assertNotIn("marketing-hero-change", webhook.archetypes)

    def test_new_public_client_websites_route_to_the_complete_delivery_playbook(self):
        profile={"detected":{"capabilities":{}}}
        for task in (
            "Haz una web para Pinturas García con un hero, galería y reseñas de demo",
            "Create a website for an independent painting business",
            "Rediseña la web corporativa de un estudio",
            "Build a public website for a local service provider",
        ):
            with self.subTest(task=task):
                descriptor=describe_task(task, profile)
                self.assertIn("public-client-website", descriptor.archetypes)
                self.assertIn("frontend", descriptor.surfaces)
                for phase, expected in (
                    ("planning", "public-client-website-brief"),
                    ("implementation", "public-client-website-implementation"),
                    ("verification", "public-client-website-live-handoff"),
                ):
                    capsule=solve_context(load_compiled(phase), descriptor, phase)
                    self.assertIn(expected, {u["id"] for u in capsule.units})

    def test_gallery_and_reviews_patterns_route_alone_and_without_console_leakage(self):
        profile={"detected":{"capabilities":{}}}
        gallery=describe_task("Mejora la galería interactiva de fotografías", profile)
        self.assertIn("public-site-gallery", gallery.archetypes)
        self.assertNotIn("public-client-website", gallery.archetypes)
        reviews=describe_task("Añade reseñas ficticias claramente etiquetadas", profile)
        self.assertIn("public-site-reviews", reviews.archetypes)
        self.assertNotIn("public-client-website", reviews.archetypes)
        for descriptor, expected in (
            (gallery, "public-gallery-responsive-selector"),
            (reviews, "public-reviews-demo-safe-marquee"),
        ):
            capsule=solve_context(load_compiled("implementation"), descriptor, "implementation")
            self.assertIn(expected, {u["id"] for u in capsule.units})
        for task in (
            "Create a website for the DentalOS admin console",
            "Add a gallery to the ChurchOS operator dashboard",
            "Fix code reviews in the backend",
            "Repair an external review webhook",
        ):
            with self.subTest(task=task):
                descriptor=describe_task(task, profile)
                self.assertNotIn("public-client-website", descriptor.archetypes)
                self.assertNotIn("public-site-gallery", descriptor.archetypes)
                self.assertNotIn("public-site-reviews", descriptor.archetypes)

    def test_comparison_handle_and_evidence_require_an_affirmative_comparator_task(self):
        profile = {"detected": {"capabilities": {}}}
        views = {phase: load_compiled(phase) for phase in ("implementation", "verification")}
        implementation_id = "public-comparison-drag-handle-contract"
        verification_id = "public-comparison-drag-verification"
        for query, expected in (
            ("Implement a before/after photo comparison slider on the services page", True),
            ("Implementa un comparador de fotos antes y después en la página de tratamientos", True),
            ("Test the before/after slider without changing the site's typography", True),
            ("No crear una galería; añade un comparador de imágenes antes/después", True),
            ("Do not add a photo gallery, but implement a before/after photo slider", True),
            ("Replace the static screenshot with a before/after photo slider", True),
            ("Implementa un slider para comparar las fotos de antes y después en la página de servicios", True),
            ("Build a public website for a local painting business", False),
            ("Crea una web para una empresa de pintura; no crear una galería ni un comparador de fotos antes y después", False),
            ("Improve the interactive photo gallery on the services page", False),
            ("Use a static photo grid with before and after photos", False),
            ("Use a static gallery instead of an image comparison slider", False),
            ("Crea una web sin galería ni comparador de fotos antes y después", False),
            ("Use a static screenshot of the before/after photo slider", False),
            ("Replace the before/after photo slider with a static image grid", False),
            ("Sustituye el comparador de fotos antes y después por una galería estática", False),
            ("Add a range slider to compare SQL latency before and after the index change", False),
            ("Design an internal admin console with a before/after photo comparison slider", False),
            ("Add an image gallery and do not add a before/after slider", False),
            ("Implementa un slider para comparar la latencia SQL antes y después de optimizar", False),
            ("Usa una galería estática sin un slider para comparar las fotos de antes y después", False),
        ):
            with self.subTest(query=query):
                descriptor = describe_task(query, profile)
                self.assertEqual("public-image-comparator" in descriptor.archetypes, expected)
                implementation = solve_context(views["implementation"], descriptor, "implementation")
                verification = solve_context(views["verification"], descriptor, "verification")
                self.assertEqual(implementation_id in {u["id"] for u in implementation.units}, expected)
                self.assertEqual(verification_id in {u["id"] for u in verification.units}, expected)
                self.assertEqual(verification_id in verification.required_evidence, expected)
                seed = new_planning_ir(descriptor, verification)
                self.assertEqual(verification_id in {item.id for item in seed.verification}, expected)

    def test_operator_console_shell_tasks_route_without_confusing_public_surfaces(self):
        profile={"detected":{"capabilities":{}}}
        examples=(
            "Implementa la sidebar en ChurchOS",
            "Pon dark mode en DentalOS",
            "Diseña una nueva consola administrativa",
            "Mejora las transiciones de pantalla en MelodIQ Core",
            "Fix the navigation rail",
        )
        for task in examples:
            with self.subTest(task=task):
                descriptor=describe_task(task, profile)
                self.assertIn("operator-console-shell-change", descriptor.archetypes)
                self.assertIn("frontend", descriptor.surfaces)
                self.assertIn("console-shell-fidelity", descriptor.risks)
        for task in ("Añadir sidebar a un blog corporativo", "Poner dark mode en una web corporativa",
                     "Refine the public website hero", "Corrige permisos en DentalOS"):
            with self.subTest(task=task):
                self.assertNotIn("operator-console-shell-change", describe_task(task, profile).archetypes)

    def test_operator_console_shell_context_is_compiled_and_selected_in_every_phase(self):
        pattern=(ROOT/"patterns/operator-console-shell-interactions.md").read_text(encoding="utf-8")
        units=extract_agent_context(pattern, "patterns/operator-console-shell-interactions.md")
        by_phase={phase: next(u for u in units if phase in u.phase)
                  for phase in ("planning", "implementation", "verification")}
        self.assertEqual(len(units), 3)
        manifest=json.loads((COMPILED/"manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["sources"]["pat-operator-console-shell-interactions"]["path"],
                         "patterns/operator-console-shell-interactions.md")
        descriptor=describe_task("Implementa la sidebar de ChurchOS", {"detected":{"capabilities":{}}})
        for phase, expected in by_phase.items():
            with self.subTest(phase=phase):
                selected=solve_context(load_compiled(phase), descriptor, phase)
                self.assertIn(expected.id, {u["id"] for u in selected.units})

    def test_operator_glass_material_routes_only_when_requested_for_operator_work(self):
        profile={"detected":{"capabilities":{}}}
        for task in (
            "Aplica Glassmorphism a la consola de MelodIQ Core",
            "Diseña el CRM interno con efecto cristal",
            "Use frosted glass for the ChurchOS operator workspace",
            "Mejora el efecto vidrio en Agurto OS",
        ):
            with self.subTest(task=task):
                descriptor=describe_task(task, profile)
                self.assertIn("operator-glass-material-change", descriptor.archetypes)
                self.assertIn("glass-material-fidelity", descriptor.risks)
                self.assertIn("frontend", descriptor.surfaces)
                for phase, expected in (
                    ("planning", "operator-glass-material-adoption-decision"),
                    ("verification", "operator-glass-material-conditional-acceptance"),
                ):
                    selected=solve_context(load_compiled(phase), descriptor, phase)
                    self.assertIn(expected, {u["id"] for u in selected.units})
        for task in (
            "Glassmorphism para la web pública de Uribe Villa",
            "Diseña con glassmorphism la landing page corporativa",
            "Implementa la sidebar en ChurchOS",
        ):
            with self.subTest(task=task):
                descriptor=describe_task(task, profile)
                self.assertNotIn("operator-glass-material-change", descriptor.archetypes)

    def test_operator_glass_material_has_canonical_compiled_source(self):
        pattern=(ROOT/"patterns/operator-glass-surface-material.md").read_text(encoding="utf-8")
        units=extract_agent_context(pattern, "patterns/operator-glass-surface-material.md")
        self.assertEqual(len(units), 2)
        manifest=json.loads((COMPILED/"manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["sources"]["pat-operator-glass-surface-material"]["path"],
                         "patterns/operator-glass-surface-material.md")

    def test_codex_distribution_keeps_console_shell_router_discoverable(self):
        bundle=json.loads((ROOT/"agent-config/codex/skills/engineering-handbook/bundle.json").read_text(encoding="utf-8"))
        self.assertTrue({"patterns", "machine-readable/compiled", "automation/engineering_context"}.issubset(set(bundle["include"])))
        for path in (ROOT/"agent-config/codex/AGENTS.global.md",
                     ROOT/"agent-config/codex/skills/engineering-handbook/SKILL.md"):
            self.assertIn("pat-operator-console-shell-interactions", path.read_text(encoding="utf-8"))
        for script in ("sync-global-agents.ps1", "sync-handbook-skill.ps1"):
            content=(ROOT/"automation/codex"/script).read_text(encoding="utf-8")
            self.assertIn('"Check"', content)
            self.assertIn('"Install"', content)

    def test_repo_capability_is_not_automatically_task_capability(self):
        d=describe_task("fix visual spacing", {"detected":{"capabilities":{"pwa":True,"persistence":True,"auth":True}}})
        self.assertNotIn("pwa", d.capabilities)
        self.assertNotIn("persistence", d.capabilities)
        self.assertIn("accessibility", d.risks)

    def test_concurrent_postgres_index_evidence_stays_scoped_to_the_migration(self):
        unit_id = "testing-postgres-concurrent-index-evidence"
        profile = {"detected": {"capabilities": {}}}
        for task, expected in (
            ("Review the PostgreSQL migration that runs CREATE INDEX CONCURRENTLY.", True),
            ("Plan a PostgreSQL migration with a concurrent index build.", True),
            ("Audita el CREATE UNIQUE INDEX CONCURRENTLY de la migración de PostgreSQL.", True),
            ("Revisa la creación de un índice concurrente en la migración de PostgreSQL.", True),
            ("Review PostgreSQL documentation for CREATE INDEX CONCURRENTLY.", False),
            ("Review the CREATE INDEX CONCURRENTLY example in the migration guide.", False),
            ("Review the SQLite migration with CREATE INDEX CONCURRENTLY.", False),
            ("Verify a PostgreSQL migration that creates a regular index.", False),
            ("No revises la migración de PostgreSQL con un índice concurrente.", False),
            ("Do not run CREATE INDEX CONCURRENTLY on the PostgreSQL migration.", False),
            ("Do not use CREATE INDEX CONCURRENTLY. Keep the existing PostgreSQL index.", False),
            ("Explain what CREATE INDEX CONCURRENTLY means in PostgreSQL.", False),
            ("Review the existing PostgreSQL migration runbook that describes CREATE INDEX CONCURRENTLY.", False),
            ("Plan the PostgreSQL migration without using CREATE INDEX CONCURRENTLY.", False),
            ("Verify the runner does not wrap CREATE INDEX CONCURRENTLY in a transaction.", True),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, profile)
                self.assertFalse(descriptor.delivery["production_effect"])
                for phase in ("planning", "verification"):
                    capsule = solve_context(load_compiled(phase), descriptor, phase)
                    self.assertEqual(unit_id in capsule.required_evidence, expected)

    def test_migration_descriptor_adds_direct_risks(self):
        d=describe_task("add archived_at column and migration", {"detected":{"capabilities":{"persistence":True}}})
        self.assertTrue(d.state["migration"])
        self.assertIn("persistence", d.capabilities)
        self.assertEqual(set(d.risks), {"compatibility","data-loss"})

    def test_expiring_invitation_is_deterministically_credential_sensitive(self):
        d=describe_task("add expiring tenant invitation links", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        self.assertEqual(set(d.risks), {"authorization","credential","tenant-isolation"})
        self.assertEqual(d.uncertain, ())

    def test_generic_invitation_keeps_constrained_uncertainty(self):
        d=describe_task("add tenant invitation", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        self.assertEqual(d.uncertain[0]["allowed"], ["credential","not-credential","unknown"])

    def test_unknown_risk_resolution_keeps_uncertainty(self):
        d=describe_task("add tenant invitation", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        resolved=merge_agent_resolution(d, {"risks":["unknown"]})
        self.assertEqual(resolved.risks, d.risks)
        self.assertEqual(resolved.uncertain, d.uncertain)
        with self.assertRaises(ValueError):
            merge_agent_resolution(d, {"risks":["unknown","credential"]})

    def test_solver_prefers_dense_direct_coverage_and_does_not_fill_budget(self):
        units=[]
        for raw in [
            unit("dense", ("authorization","tenant-isolation"), ("risk:authorization",), force="must", priority=90),
            unit("partial-a", ("authorization",), ("risk:authorization",), force="must", priority=100),
            unit("partial-b", ("tenant-isolation",), ("risk:tenant-isolation",), force="must", priority=100),
            unit("optional", (), ("risk:authorization",), priority=100),
        ]:
            units.append(compiled_unit(raw))
        compiled={"units":units,"routing":{"risk:authorization":["dense","partial-a","optional"],"risk:tenant-isolation":["partial-b"]}}
        d=describe_task("tenant permission", {"detected":{"capabilities":{}}})
        capsule=solve_context(compiled,d,"planning")
        ids=[x["id"] for x in capsule.units]
        self.assertIn("dense", ids)
        self.assertNotIn("optional", ids)
        self.assertEqual(capsule.uncovered, ())

    def test_indexed_solver_keeps_units_without_positive_predicates(self):
        required = dict(unit("always", force="must"), requires=["prerequisite"])
        excluded = dict(unit("excluded", force="must"), excludes=["intent:review"])
        all_only = unit("all-only", activate_all=("intent:review", "operation:migration"), force="must")
        records = [required, excluded, all_only, unit("prerequisite", force="should")]
        view = {"units": [compiled_unit(record, 5) for record in records]}
        routing = {"intent:review": ["all-only"], "operation:migration": ["all-only"]}
        for text, phase, expected in (
            ("Review the release note", "planning", ["always", "prerequisite"]),
            ("Review the PostgreSQL migration", "planning", ["all-only", "always", "prerequisite"]),
            ("Review the release note", "verification", []),
        ):
            with self.subTest(text=text, phase=phase):
                descriptor = describe_task(text, {"detected": {"capabilities": {}}})
                indexed = solve_context(dict(view, routing=routing), descriptor, phase)
                self.assertEqual([item["id"] for item in indexed.units], expected)
                self.assertEqual(indexed.to_dict(), solve_context(view, descriptor, phase).to_dict())

    def test_solver_includes_requires_closure(self):
        dependency=compiled_unit(unit("dependency", (), (), force="should"), 7)
        parent=compiled_unit(unit("parent", ("performance",), ("risk:performance",), force="must"), 11); parent["requires"]=["dependency"]
        compiled={"units":[dependency,parent],"routing":{"risk:performance":["parent"]}}
        d=describe_task("reduce API latency", {"detected":{"capabilities":{}}})
        capsule=solve_context(compiled,d,"planning")
        self.assertEqual({x["id"] for x in capsule.units}, {"dependency","parent"})

    def test_deep_requires_chain_compiles_and_resolves(self):
        ids = [f"chain-{number:04d}" for number in range(1120)]
        units = []
        for index, uid in enumerate(ids):
            row = unit(uid, force="must" if index == 0 else None)
            row["text"] = "x"
            row["requires"] = ids[index + 1:index + 2]
            units.append(row)

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "standards" / "chain.md"
            source.parent.mkdir()
            source.write_text(source_doc("std-test", units), encoding="utf-8")
            output = root / "machine-readable" / "compiled"
            compile_handbook(root, output)
            compiled = _load_compiled(output, "planning")
            descriptor = describe_task("Inspect the example item.", {})

            capsule = solve_context(compiled, descriptor, "planning")

        self.assertEqual([row["id"] for row in capsule.units], ids)
        self.assertEqual(capsule.estimated_tokens, len(ids))
        self.assertLess(capsule.estimated_tokens, capsule.budget.hard_max)
        self.assertEqual(capsule.escalations, ())

    def test_requires_diamond_preserves_budget_and_dependency_order(self):
        descriptor = describe_task("reduce API latency", {})
        head = compiled_unit(unit("head", descriptor.risks, ("risk:performance",), force="should"), 1)
        head["requires"] = ["right", "left"]
        left = compiled_unit(unit("left"), 1)
        left["requires"] = ["shared"]
        right = compiled_unit(unit("right"), 1)
        right["requires"] = ["shared"]
        compiled = {"units": [head, left, right, compiled_unit(unit("shared"), 1)]}

        optional = solve_context(
            compiled, descriptor, "planning", ContextBudget(1, 2, 3, 0)
        )
        self.assertEqual(optional.units, ())
        self.assertIn("performance", optional.uncovered)
        exact = solve_context(
            compiled, descriptor, "planning", ContextBudget(1, 2, 4, 0)
        )
        self.assertEqual([row["id"] for row in exact.units], ["head", "left", "right", "shared"])
        self.assertEqual(exact.estimated_tokens, 4)
        self.assertEqual(exact.escalations, ())

        head["force"] = "must"
        mandatory = solve_context(
            compiled, descriptor, "planning", ContextBudget(1, 1, 1, 0)
        )
        self.assertEqual(
            mandatory.escalations,
            (
                {"type": "hard-budget-crossed", "unit": "left", "estimated_tokens": 2},
                {"type": "hard-budget-crossed", "unit": "right", "estimated_tokens": 3},
                {"type": "hard-budget-crossed", "unit": "head", "estimated_tokens": 4},
            ),
        )

    def test_solver_keeps_mandatory_authority_over_hard_budget(self):
        mandatory=compiled_unit(unit("mandatory", (), ("intent:modify",), force="must"), 200)
        compiled={"units":[mandatory],"routing":{"intent:modify":["mandatory"]}}
        d=describe_task("update documentation", {"detected":{"capabilities":{}}})
        capsule=solve_context(compiled,d,"planning", ContextBudget(target=20,soft_max=40,hard_max=50,reserve=0))
        self.assertEqual([x["id"] for x in capsule.units], ["mandatory"])
        self.assertTrue(any(x["type"]=="normative-budget-crossed" for x in capsule.escalations))

    def test_intent_only_mandatory_is_selected_but_not_risk_coverage(self):
        generic=compiled_unit(unit("generic", ("performance",), ("intent:modify",), force="must"), 9)
        compiled={"units":[generic],"routing":{"intent:modify":["generic"]}}
        d=describe_task("reduce API latency", {"detected":{"capabilities":{}}})
        capsule=solve_context(compiled,d,"planning")
        self.assertEqual([x["id"] for x in capsule.units], ["generic"])
        self.assertIn("performance", capsule.uncovered)
        self.assertNotIn("performance", capsule.covered)

    def test_unmatched_nonintent_alternative_cannot_claim_direct_risk_coverage(self):
        generic = compiled_unit(unit("generic", ("availability",), ("intent:modify", "operation:deployment"), force="must"), 9)
        compiled = {"units": [generic], "routing": {"intent:modify": ["generic"], "operation:deployment": ["generic"]}}
        observation = TaskDescriptor.for_test(risks=("availability",))
        capsule = solve_context(compiled, observation, "planning")
        self.assertEqual({item["id"] for item in capsule.units}, {"generic"})
        self.assertIn("availability", capsule.uncovered)
        self.assertNotIn("availability", capsule.covered)
        deployment = TaskDescriptor.for_test(risks=("availability",), operations=("deployment",))
        self.assertIn("availability", solve_context(compiled, deployment, "planning").covered)

    def test_repo_route_is_narrow(self):
        profile={"detected":{"landmarks":{"migrations":["migrations"],"tests":["tests"]},"commands":{"test":"pytest"}},"declared":{"landmarks":{}}}
        d=describe_task("add archived_at column and migration", {"detected":{"capabilities":{"persistence":True}}})
        route=build_repo_route(profile,d)
        self.assertIn("migrations", route["inspect_first"])
        self.assertIn("pwa", route["avoid_by_default"])

    def test_pwa_profile_distinguishes_legacy_manifest_content_and_fingerprints_it(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = root / "manifest.json"
            manifest.write_text('{"name":"Build","files":[]}', encoding="utf-8")
            generic = profile_repo(root)
            self.assertFalse(generic["detected"]["capabilities"]["pwa"])
            self.assertEqual(generic["detected"]["landmarks"]["pwa"], [])

            manifest.write_text('{"name":"Portal","icons":[{"src":"icon.png"}]}', encoding="utf-8")
            web = profile_repo(root, generic)
            self.assertTrue(web["detected"]["capabilities"]["pwa"])
            self.assertEqual(web["detected"]["landmarks"]["pwa"], ["manifest.json"])
            manifest.write_bytes(manifest.read_bytes() + b" ")
            revised = profile_repo(root, web)
            self.assertNotIn("runtime", revised["meta"]["reused_segments"])
            self.assertIn("discovery-tree", revised["meta"]["reused_segments"])

            for data in (b"broken", b'{"start_url":false,"name":"Portal","display":[],"icons":{}}', b"[]"):
                with self.subTest(data=data):
                    manifest.write_bytes(data)
                    self.assertEqual(profile_repo(root)["profile_hash"], generic["profile_hash"])

    def test_pwa_evidence_stays_within_the_selected_repository(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            for name in ("manifest.json", "site.webmanifest", "sw.js"):
                (root / name).touch()
            resolve = Path.resolve

            def resolve_candidate(path, *args, **kwargs):
                if path.parent == root:
                    return root.parent / path.name
                return resolve(path, *args, **kwargs)

            with mock.patch.object(Path, "resolve", resolve_candidate), mock.patch.object(
                Path, "read_bytes", side_effect=AssertionError("external manifest opened")
            ):
                profile = profile_repo(root)
            self.assertFalse(profile["detected"]["capabilities"]["pwa"])
            self.assertNotIn("site.webmanifest", profile["detected"]["landmarks"]["pwa"])

    def test_pwa_profile_uses_worker_basenames_and_webmanifest_extension(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "fixture-sw.js").touch()
            (root / "asset-manifest.json").write_text('{"start_url":"/"}', encoding="utf-8")
            self.assertFalse(profile_repo(root)["detected"]["capabilities"]["pwa"])
            for name in ("service-worker.js", "sw.js", "clinic.webmanifest"):
                with self.subTest(name=name):
                    indicator = root / name
                    indicator.touch()
                    profile = profile_repo(root)
                    self.assertTrue(profile["detected"]["capabilities"]["pwa"])
                    self.assertEqual(profile["detected"]["landmarks"]["pwa"], [name])
                    indicator.unlink()

    def test_repo_profile_directory_hash_changes_with_file_content(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); workflows=root/".github/workflows"; workflows.mkdir(parents=True)
            workflow=workflows/"ci.yml"; workflow.write_text("name: one\n")
            first=profile_repo(root); workflow.write_text("name: two\n"); second=profile_repo(root, first)
            self.assertNotEqual(first["meta"]["segment_hashes"]["delivery"], second["meta"]["segment_hashes"]["delivery"])
            self.assertNotEqual(first["profile_hash"], second["profile_hash"])

    def test_profile_requires_an_existing_directory_before_creating_output(self):
        from automation.engineering_context.repo_profile import InvalidRepositoryRoot, write_repo_profile

        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            missing = scratch / "missing"
            as_file = scratch / "file.txt"
            as_file.write_text("inert fixture", encoding="utf-8")
            for invalid, output in ((missing, missing / "profile-output"),
                                    (as_file, scratch / "outside-output")):
                with self.subTest(invalid=invalid):
                    with self.assertRaisesRegex(InvalidRepositoryRoot, "must be an existing directory"):
                        profile_repo(invalid)
                    with self.assertRaisesRegex(InvalidRepositoryRoot, "must be an existing directory"):
                        write_repo_profile(invalid, output)
                    stderr, stdout = io.StringIO(), io.StringIO()
                    with redirect_stderr(stderr), redirect_stdout(stdout):
                        self.assertEqual(main(["profile-repo", "--repo", str(invalid), "--output", str(output)]), 2)
                    self.assertIn(str(invalid.resolve()), stderr.getvalue())
                    self.assertEqual(stdout.getvalue(), "")
                    self.assertFalse(output.exists())
            self.assertFalse(missing.exists())
            self.assertEqual(as_file.read_text(encoding="utf-8"), "inert fixture")
            empty = scratch / "empty"
            empty.mkdir()
            self.assertEqual(profile_repo(empty)["schema"], "repo-profile/v1")

    def test_profile_excludes_metadata_behind_outside_directory_aliases(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td).resolve()
            root, outside = scratch / "root", scratch / "separate"
            root.mkdir()
            (outside / "workflows").mkdir(parents=True)
            (outside / "workflows/check.yml").write_text("name: inert fixture\\n", encoding="utf-8")
            (outside / "context.json").write_text('{"decisions":{"fixture":"external"}}', encoding="utf-8")
            empty = profile_repo(root)
            for location in (".github", ".engineering", "tests"):
                alias = root / location
                if os.name == "nt":
                    made = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(outside)],
                                          capture_output=True, timeout=10)
                    if made.returncode:
                        self.skipTest("junction creation unavailable in the Windows test fixture")
                else:
                    alias.symlink_to(outside, target_is_directory=True)
            self.assertEqual(profile_repo(root), empty)
            (outside / "workflows/check.yml").write_text("name: changed fixture\\n", encoding="utf-8")
            self.assertEqual(profile_repo(root), empty)

    @unittest.skipUnless(os.name == "nt", "Windows exposes directory junctions to os.walk")
    def test_profile_prunes_an_ancestor_junction_without_deduplicating_siblings(self):
        from automation.engineering_context.repo_profile import _walk_files

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            content = root / "content"
            content.mkdir()
            (content / "fixture.txt").write_text("Inert file", encoding="utf-8")
            native_walk = os.walk
            aliases = []

            def bounded_walk(path, *args, **kwargs):
                for count, rows in enumerate(native_walk(path, *args, **kwargs)):
                    if count == 8:
                        self.fail("profile traversal descended repeatedly through the ancestor junction")
                    yield rows

            try:
                for link, target in ((content / "back", root), (root / "sibling-a", content),
                                     (root / "sibling-b", content), (root / "tests", root)):
                    result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
                                            capture_output=True, timeout=10)
                    if result.returncode:
                        self.skipTest("junction creation unavailable in the Windows test fixture")
                    aliases.append(link)
                with mock.patch("automation.engineering_context.repo_profile.os.walk", side_effect=bounded_walk):
                    files = _walk_files(root, root)
                    self.assertEqual(_walk_files(root, root / "tests"), [])
                    profile = profile_repo(root)
                self.assertEqual([path.relative_to(root).as_posix() for path in files],
                                 ["content/fixture.txt", "sibling-a/fixture.txt", "sibling-b/fixture.txt"])
                self.assertFalse(profile["detected"]["verification"]["tests"])

                valid = ["sibling-a", "sibling-b/fixture.txt", "content/fixture.txt", "content/fixture.txt"]
                invalid = ["content/back", "content/back/content/fixture.txt"]
                config = root / ".engineering/context.json"
                config.parent.mkdir()
                config.write_text(json.dumps({"landmarks": {"fixture": valid + invalid}}), encoding="utf-8")
                declared = profile_repo(root)["declared"]
                self.assertEqual(declared["landmarks"]["fixture"], valid)
                self.assertEqual(declared["invalid_landmarks"], [
                    {"label": "fixture", "path": path, "reason": "missing-or-unsafe-path"} for path in invalid
                ])
            finally:
                for alias in reversed(aliases):
                    alias.rmdir()

    def test_doctor_flags_invalid_package_json_while_profile_keeps_other_signals(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "tests").mkdir()
            (root / "tests/sample.py").write_text("# Inert source fixture", encoding="utf-8")
            package = root / "package.json"
            for content in ('{"scripts":{', " ", '{"scripts":{},}'):
                with self.subTest(content=content):
                    package.write_text(content, encoding="utf-8")
                    profile = profile_repo(root)
                    self.assertEqual(profile["detected"]["commands"], {})
                    self.assertTrue(profile["detected"]["verification"]["tests"])
                    self.assertEqual(profile["meta"]["input_problems"], ["invalid JSON in package.json"])
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(["doctor", "--root", str(ROOT), "--repo", str(root)]), 1)
                    diagnosis = json.loads(output.getvalue())
                    self.assertFalse(diagnosis["ok"])
                    self.assertEqual(diagnosis["problems"], ["invalid JSON in package.json"])
                    self.assertEqual(package.read_text(encoding="utf-8"), content)
            package.write_bytes(b'\xef\xbb\xbf{"scripts":{"fixture":"node --test"}}')
            valid = profile_repo(root)
            self.assertNotIn("input_problems", valid["meta"])
            self.assertEqual(valid["detected"]["commands"], {"fixture": "node --test"})

    def test_profile_cli_excludes_only_its_own_output(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            root = scratch / "consumer"
            tests = root / "tests"
            vendor = tests / "vendor" / "repo.json"
            vendor.parent.mkdir(parents=True)
            vendor_bytes = b'{"fixture": 1}'
            vendor.write_bytes(vendor_bytes)

            def cli(output=None):
                command = [sys.executable, "-B", "-m", "automation.engineering_context",
                           "profile-repo", "--repo", str(root)]
                if output is not None:
                    command.extend(["--output", str(output)])
                result = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8",
                                        check=False, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return json.loads(result.stdout)

            read_only = cli()
            outside = cli(scratch / "external")
            self.assertEqual(read_only, outside)
            reports = [cli(tests) for _ in range(3)]
            self.assertEqual([report["profile_hash"] for report in reports],
                             [read_only["profile_hash"]] * 3)
            segments = read_only["meta"]["segment_hashes"]
            self.assertEqual([report["meta"]["segment_hashes"] for report in reports], [segments] * 3)
            self.assertEqual(reports[0]["meta"]["reused_segments"], [])
            self.assertEqual(reports[1]["meta"]["reused_segments"], sorted(segments))
            self.assertEqual(reports[2], reports[1])
            self.assertEqual(json.loads((tests / "repo.json").read_text(encoding="utf-8")), reports[2])
            self.assertEqual(vendor.read_bytes(), vendor_bytes)
            self.assertNotEqual(cli()["meta"]["segment_hashes"]["verification"], segments["verification"])

            vendor.write_bytes(b'{"fixture": 2}')
            revised = cli(tests)
            self.assertNotEqual(revised["profile_hash"], read_only["profile_hash"])
            self.assertNotEqual(revised["meta"]["segment_hashes"]["verification"], segments["verification"])
            self.assertEqual(revised["meta"]["segment_hashes"]["discovery-tree"], segments["discovery-tree"])

    def test_profile_omits_only_its_own_declared_output_landmark(self):
        from automation.engineering_context.repo_profile import write_repo_profile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "reports"
            sibling = output / "vendor" / "repo.json"
            sibling.parent.mkdir(parents=True)
            sibling.write_bytes(b'{"vendor":true}')
            context = root / ".engineering" / "context.json"
            context.parent.mkdir()
            context.write_text(json.dumps({"landmarks": {"inventory": [
                "reports/repo.json", "reports/vendor/repo.json", "reports/missing.json",
            ]}}), encoding="utf-8")

            read_only_before = profile_repo(root)["declared"]
            self.assertIn("reports/repo.json", {item["path"] for item in read_only_before["invalid_landmarks"]})
            first = write_repo_profile(root, output)
            second = write_repo_profile(root, output)
            self.assertEqual(first["profile_hash"], second["profile_hash"])
            self.assertEqual(first["declared"], second["declared"])
            self.assertEqual(first["declared"]["landmarks"]["inventory"], ["reports/vendor/repo.json"])
            self.assertEqual([item["path"] for item in first["declared"]["invalid_landmarks"]], ["reports/missing.json"])
            read_only_after = profile_repo(root)["declared"]
            self.assertEqual(read_only_after["landmarks"]["inventory"],
                             ["reports/repo.json", "reports/vendor/repo.json"])
            self.assertEqual(sibling.read_bytes(), b'{"vendor":true}')

    def test_planning_ir_surfaces_uncovered_risk(self):
        d=describe_task("reduce API latency", {"detected":{"capabilities":{}}})
        capsule=solve_context({"units":[],"routing":{}},d,"planning")
        ir=new_planning_ir(d,capsule)
        self.assertTrue(any(x.get("id","").startswith("uncovered:") for x in ir.unresolved))

    def test_plan_validator_requires_authz_decision(self):
        ir=PlanningIR.for_test(risks=("tenant-isolation",), decisions=())
        self.assertIn("missing-authorization-decision", {i.code for i in validate_planning_ir(ir)})

    def test_plan_validator_requires_migration_evidence(self):
        ir=PlanningIR.for_test(migration=True, verification=())
        self.assertIn("missing-migration-verification", {i.code for i in validate_planning_ir(ir)})

    def test_planning_ir_preserves_and_rejects_unsupported_schema(self):
        ir=planning_ir_from_dict({"schema":"planning-ir/v999","context_id":"x","task":{},"affected":{}})
        self.assertEqual(ir.schema, "planning-ir/v999")
        self.assertIn("unsupported-planning-ir-schema", {i.code for i in validate_planning_ir(ir)})

    def test_planning_ir_checks_only_the_consumed_state_and_delivery_flags(self):
        for field, flag in (("state", "migration"), ("delivery", "production_effect")):
            with self.subTest(field=field):
                self.assertEqual(getattr(planning_ir_from_dict({}), field), {})
                for value in ({}, {"other": [1]}, {flag: True, "other": None}, {flag: False}):
                    self.assertEqual(getattr(planning_ir_from_dict({field: value}), field), value)
                for invalid in (None, [], "false", 0, False):
                    with self.assertRaisesRegex(ValueError, f"'{field}' must be a JSON object"):
                        planning_ir_from_dict({field: invalid})
                for invalid in (None, 0, 1, "false", [], {}):
                    with self.assertRaisesRegex(ValueError, rf"'{field}\.{flag}' must be a boolean"):
                        planning_ir_from_dict({field: {flag: invalid}})

    def test_planning_ir_string_arrays_preserve_values_and_reject_wrong_shapes(self):
        for key in ("risks", "operations", "uncovered", "provenance"):
            with self.subTest(key=key):
                self.assertEqual(getattr(planning_ir_from_dict({}), key), ())
                self.assertEqual(getattr(planning_ir_from_dict({key: []}), key), ())
                values = ["second", "first", "second"]
                self.assertEqual(getattr(planning_ir_from_dict({key: values}), key), tuple(values))
                for invalid in ("one", 7, None, {"name": "one"}, ["one", 2]):
                    with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, key):
                        planning_ir_from_dict({key: invalid})

    def test_validate_plan_reports_malformed_operations_and_preserves_valid_requirements(self):
        seed = PlanningIR.for_test(operations=("integration",)).to_dict()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "plan.json"
            for operations, issue in (
                (["integration"], "missing-integration-failure-semantics"),
                ("integration", "invalid-planning-ir-shape"),
                (1, "invalid-planning-ir-shape"),
            ):
                with self.subTest(operations=operations):
                    path.write_text(json.dumps({**seed, "operations": operations}), encoding="utf-8")
                    out = io.StringIO()
                    with redirect_stdout(out):
                        self.assertEqual(main(["validate-plan", "--input", str(path)]), 1)
                    receipt = json.loads(out.getvalue())
                    self.assertFalse(receipt["valid"])
                    self.assertEqual([entry["code"] for entry in receipt["issues"]], [issue])
                    if issue == "invalid-planning-ir-shape":
                        self.assertIn("operations", receipt["issues"][0]["message"])

    def test_validate_plan_reports_malformed_record_shapes(self):
        cases = (
            ({"decisions": {}}, "decisions"),
            ({"verification": ""}, "verification"),
            ({"unresolved": None}, "unresolved"),
            ({"decisions": [{}]}, "decisions[0].id"),
            ({"decisions": [{"id": "fixture"}, {"id": " \u2003 "}]}, "decisions[1].id"),
            ({"verification": [{"id": ["fixture"]}]}, "verification[0].id"),
            ({"unresolved": [False]}, "unresolved[0]"),
            ({"unresolved": [{"risk": ["fixture"]}]}, "unresolved[0].risk"),
            ({"verification": [{"id": "fixture", "unexpected": True}]}, "verification[0]"),
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.json"
            for payload, field in cases:
                with self.subTest(payload=payload):
                    path.write_text(json.dumps(payload), encoding="utf-8")
                    output, errors = io.StringIO(), io.StringIO()
                    with redirect_stdout(output), redirect_stderr(errors):
                        self.assertEqual(main(["validate-plan", "--input", str(path)]), 1)
                    receipt = json.loads(output.getvalue())
                    self.assertFalse(receipt["valid"])
                    self.assertEqual([issue["code"] for issue in receipt["issues"]], ["invalid-planning-ir-shape"])
                    self.assertIn(f"'{field}'", receipt["issues"][0]["message"])
                    self.assertEqual(errors.getvalue(), "")

    def test_validate_plan_rejects_duplicate_wire_members_before_semantics(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.json"
            for source, member in (
                ('{"state":{"migration":true},"state":{"migration":false}}', "state"),
                (r'{"state":{"migr\u0061tion":true,"migration":false}}', "migration"),
                ('{"risks":["tenant-isolation"],"decisions":[{"id":"scope","id":"authz"}]}', "id"),
            ):
                with self.subTest(member=member):
                    path.write_text(source, encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(["validate-plan", "--input", str(path)]), 1)
                    receipt = json.loads(output.getvalue())
                    self.assertEqual(receipt, {"valid": False, "issues": [{
                        "code": "invalid-planning-ir-shape",
                        "message": f"Planning IR has duplicate JSON member {member!r}.",
                        "severity": "error",
                    }]})

            path.write_text('{"decisions":[{"id":"scope"},{"id":"owner"}]}', encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["validate-plan", "--input", str(path)]), 0)
            self.assertEqual(json.loads(output.getvalue()), {"valid": True, "issues": []})

    def test_planning_ir_preserves_valid_record_options_and_sparse_unresolved(self):
        payload = {
            "decisions": [{"id": "AUTHZ / decision v2", "choice": "keep", "reason": None}],
            "verification": [{"id": "Local evidence / v2", "evidence_class": "sample", "source": "fixture"}],
            "risks": ["tenant-isolation"],
            "unresolved": [{"risk": "performance", "custom": {"data": [1]}}, {"risk": None}],
            "uncovered": ["performance"],
        }
        ir = planning_ir_from_dict(payload)
        self.assertEqual(validate_planning_ir(ir), ())
        self.assertEqual(ir.decisions[0].id, payload["decisions"][0]["id"])
        self.assertEqual(ir.decisions[0].choice, "keep")
        self.assertEqual(ir.to_dict()["verification"], payload["verification"])
        self.assertEqual(ir.to_dict()["unresolved"], payload["unresolved"])

    def test_planning_ir_invariant_records_keep_text_and_legacy_optional_values(self):
        cases = (
            ({}, "invariants"),
            ([False], "invariants[0]"),
            ([{"text": "Missing ID"}], "invariants[0].id"),
            ([{"id": " \u2003 "}], "invariants[0].id"),
            ([{"id": "Rule", "text": ["not text"]}], "invariants[0].text"),
            ([{"id": "Rule", "source": True}], "invariants[0].source"),
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.json"
            for raw, location in cases:
                with self.subTest(raw=raw):
                    path.write_text(json.dumps({"invariants": raw}), encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(["validate-plan", "--input", str(path)]), 1)
                    issues = json.loads(output.getvalue())["issues"]
                    self.assertEqual([entry["code"] for entry in issues], ["invalid-planning-ir-shape"])
                    self.assertIn(f"'{location}'", issues[0]["message"])

        text = {"id": " Regla / revisión ", "text": " Original words ", "source": "Repo Owner"}
        legacy = {"id": "legacy", "text": None, "source": None}
        sparse = planning_ir_from_dict({"invariants": (text, legacy, {"id": "id-only"})})
        self.assertEqual(sparse.to_dict()["invariants"], [text, {"id": "legacy"}, {"id": "id-only"}])

    def test_context_delta_reuses_exact_units_and_preserves_removed_ids(self):
        from automation.engineering_context.context_solver import ContextCapsule
        current = ContextCapsule(
            "new", "planning",
            ({"id": "a", "text": "same"}, {"id": "b", "text": "new copy"}, {"id": "c"}, {"id": "d"}),
            (), (), 1, (), (),
        )
        previous_units = {"a": {"id": "a", "text": "same"}, "b": {"id": "b", "text": "old copy"}}
        delta = capsule_delta("old", {"a", "b", "c", "e"}, current, previous_units=previous_units)
        self.assertEqual([unit["id"] for unit in delta["added_units"]], ["b", "c", "d"])
        self.assertEqual(delta["removed_unit_ids"], ["e"])
        self.assertEqual(delta["unchanged_unit_count"], 1)

        no_base = capsule_delta(None, {"e"}, current, previous_units=previous_units)
        self.assertEqual([unit["id"] for unit in no_base["added_units"]], ["a", "b", "c", "d"])
        self.assertEqual(no_base["removed_unit_ids"], [])
        self.assertEqual(no_base["unchanged_unit_count"], 0)

    def test_context_delta_cli_accepts_full_and_id_only_bases(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "standards/receipt.md"
            source.parent.mkdir()
            compiled = root / "machine-readable/compiled"
            repo = root / "consumer"
            repo.mkdir()
            prior = unit("changed", ("privacy-exposure",), ("archetype:privacy-review",), force="must")
            constant = unit("constant", ("privacy-exposure",), ("archetype:privacy-review",), force="must")
            command = [
                "context", "--repo", str(repo), "--handbook", str(compiled), "--mode", "plan",
                "--task", "Review data retention and deletion in the internal CRM", "--metrics",
            ]

            def run(*extra):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(main([*command, *extra]), 0)
                return json.loads(output.getvalue())

            source.write_text(source_doc("std-test", [prior, constant]), encoding="utf-8")
            compile_handbook(root, compiled)
            old = run()
            self.assertEqual({unit["id"] for unit in old["capsule"]["units"]}, {"changed", "constant"})

            latest = dict(prior, text="A newer mandatory placeholder.")
            source.write_text(source_doc("std-test", [latest, constant]), encoding="utf-8")
            compile_handbook(root, compiled)
            current = run()
            self.assertNotEqual(current["context_id"], old["context_id"])
            base = root / "base.json"
            cases = (
                (old, ["changed"], 1),
                ({"id": old["context_id"], "unit_ids": ["constant", "changed", "changed"], "capsule": None},
                 ["changed", "constant"], 0),
                ({"context_id": current["context_id"], "unit_ids": ["constant", "changed", "changed"]},
                 [], 2),
            )
            for receipt, updated_ids, unchanged in cases:
                with self.subTest(updated_ids=updated_ids):
                    base.write_text(json.dumps(receipt), encoding="utf-8")
                    result = run("--base-context", str(base))
                    delta = result["capsule"]["delta"]
                    self.assertEqual([unit["id"] for unit in delta["added_units"]], updated_ids)
                    self.assertEqual(delta["removed_unit_ids"], [])
                    self.assertEqual(delta["unchanged_unit_count"], unchanged)
                    self.assertEqual(result["metrics"]["context_delta"], unchanged)
                    if "changed" in updated_ids:
                        self.assertEqual(delta["added_units"][0]["text"], latest["text"])

    def test_context_delta_rejects_duplicate_base_wire_members(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "handbook"
            machine = root / "machine-readable"
            machine.mkdir(parents=True)
            (machine / "catalog.yaml").write_text("documents:\n", encoding="utf-8")
            compiled = machine / "compiled"
            compile_handbook(root, compiled)
            repo = Path(directory) / "consumer"
            repo.mkdir()
            base = Path(directory) / "receipt.json"
            command = ["context", "--handbook", str(compiled), "--repo", str(repo), "--mode", "plan",
                       "--task", "Review the example guide", "--base-context", str(base)]
            for payload, member in (
                (r'{"context_id":"a","context_\u0069d":"b","unit_ids":[]}', "context_id"),
                ('{"id":"a","capsule":{"id":"a","units":[],"units":[]}}', "units"),
                (r'{"id":"a","units":[{"id":"unit","text":"old","t\u0065xt":"current"}]}', "text"),
            ):
                with self.subTest(member=member):
                    base.write_text(payload, encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output), self.assertRaises(ValueError) as invalid:
                        main(command)
                    self.assertEqual(str(invalid.exception), f"Base context has duplicate JSON member {member!r}.")
                    self.assertEqual(output.getvalue(), "")

    def test_context_delta_reconstructs_across_phases_and_rejects_invalid_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "standards/receipt.md"
            source.parent.mkdir()
            compiled = root / "machine-readable/compiled"
            repo = root / "consumer"
            repo.mkdir()
            base = root / "base.json"
            units = [
                unit(uid, ("privacy-exposure",), ("archetype:privacy-review",), phase=phases, force="must")
                for uid, phases in (("constant", ("planning", "verification")), ("old-only", ("planning",)),
                                    ("new-only", ("verification",)))
            ]
            source.write_text(source_doc("std-test", units), encoding="utf-8")
            compile_handbook(root, compiled)

            def run(mode, *extra):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(main([
                        "context", "--repo", str(repo), "--handbook", str(compiled), "--mode", mode,
                        "--task", "Review data retention and deletion in the internal CRM", *extra,
                    ]), 0)
                return json.loads(output.getvalue())

            planning = run("plan")
            verification = run("verify")
            old_units = {record["id"]: record for record in planning["capsule"]["units"]}
            new_units = {record["id"]: record for record in verification["capsule"]["units"]}
            self.assertEqual(set(old_units), {"constant", "old-only"})
            self.assertEqual(set(new_units), {"constant", "new-only"})
            accepted = {
                "envelope": planning,
                "bare-capsule": planning["capsule"],
                "legacy": {"id": planning["context_id"], "unit_ids": ["constant", "old-only", "constant"]},
                "matching-mixed": dict(planning, unit_ids=["old-only", "constant"]),
                "empty-optional-ids": dict(planning, unit_ids=[]),
            }
            for name, record in accepted.items():
                with self.subTest(receipt=name):
                    base.write_text(json.dumps(record), encoding="utf-8")
                    delta = run("verify", "--base-context", str(base))["capsule"]["delta"]
                    self.assertEqual(delta["removed_unit_ids"], ["old-only"])
                    reconstructed = dict(old_units)
                    for uid in delta["removed_unit_ids"]:
                        reconstructed.pop(uid)
                    reconstructed.update({unit["id"]: unit for unit in delta["added_units"]})
                    self.assertEqual(reconstructed, new_units)
                    self.assertEqual(delta["unchanged_unit_count"], 0 if name == "legacy" else 1)

            invalid = {
                "partial-mixed": (dict(planning, unit_ids=["constant"]), "do not match"),
                "extra-mixed": (dict(planning, unit_ids=["constant", "old-only", "additional"]), "do not match"),
                "scalar-ids": ({"id": planning["context_id"], "unit_ids": "old-only"}, "must be an array"),
                "null-ids": ({"id": planning["context_id"], "unit_ids": None}, "must be an array"),
                "missing-inventory": ({"id": planning["context_id"]}, "requires capsule units"),
                "missing-id": ({"unit_ids": ["constant", "old-only"]}, "requires a nonempty string ID"),
                "boolean-id": ({"context_id": False, "unit_ids": ["constant", "old-only"]}, "requires a nonempty string ID"),
                "empty-id-fallback": (dict(planning, context_id=""), "requires a nonempty string ID"),
                "invalid-context-id": (dict(planning, context_id="different"), "does not match its capsule"),
            }
            for name, (record, message) in invalid.items():
                with self.subTest(receipt=name):
                    base.write_text(json.dumps(record), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message):
                        run("verify", "--base-context", str(base))

    def test_doctor_reports_nonobject_repository_context(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repository"
            root.mkdir()
            handbook = Path(td) / "handbook"
            machine = handbook / "machine-readable"
            machine.mkdir(parents=True)
            (machine / "catalog.yaml").write_text("version: 1\ndocuments:\n", encoding="utf-8")
            (machine / "agent-runtime-routing.v1.json").write_text(
                '{"model_routing":{"routes":[]}}', encoding="utf-8",
            )
            compile_handbook(handbook, machine / "compiled")
            options = ["doctor", "--root", str(handbook), "--repo", str(root)]
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(options), 0)
            self.assertTrue(json.loads(output.getvalue())["ok"])

            declaration = root / ".engineering/context.json"
            declaration.parent.mkdir()
            cases = (({"landmarks": {}}, None), ([], "repo context must be a JSON object"),
                     (True, "repo context must be a JSON object"), (None, "repo context must be a JSON object"),
                     ({"schema": "repo-context/v999"}, "unsupported repo context schema"))
            for payload, problem in cases:
                with self.subTest(payload=payload):
                    declaration.write_text(json.dumps(payload), encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(options), 1 if problem else 0)
                    receipt = json.loads(output.getvalue())
                    self.assertEqual(receipt["ok"], problem is None)
                    self.assertEqual(receipt["problems"], [problem] if problem else [])

    def test_conformance_does_not_treat_not_run_as_passed(self):
        class C: required_evidence=("authz-negative",)
        ir=PlanningIR.for_test(verification=(VerificationRequirement("authz-negative"),))
        result=project_conformance(C(),ir,({"id":"authz-negative","status":"not-run"},))
        self.assertEqual(result["demonstrated"], [])
        self.assertEqual(result["gaps"], ["authz-negative"])

    def test_conformance_accepts_the_serialized_planning_seed(self):
        descriptor = describe_task("Verify a Production release and its rollback readiness", {})
        capsule = solve_context(load_compiled("verification"), descriptor, "verification")
        ir = new_planning_ir(descriptor, capsule)
        seed = json.loads(canonical_json(ir.to_dict()))
        self.assertTrue(seed["verification"])
        self.assertTrue(all(isinstance(record, dict) for record in seed["verification"]))
        requirement = seed["verification"][0]["id"]
        evidence = ({"id": requirement, "status": "not-run"},)

        typed = project_conformance(capsule, ir, evidence)
        received = project_conformance(json.loads(canonical_json(capsule.to_dict())), seed, evidence)
        self.assertEqual(received, typed)
        self.assertIn(requirement, received["gaps"])
        self.assertEqual(received["demonstrated"], [])

    def test_conformance_retains_supplied_exception_records(self):
        descriptor = describe_task("Verify a Production release and its rollback readiness", {})
        capsule = solve_context(load_compiled("verification"), descriptor, "verification")
        seed = json.loads(canonical_json(new_planning_ir(descriptor, capsule).to_dict()))
        requirement = seed["verification"][0]["id"]
        preview = {"id": requirement, "reason": "Preview receipt", "scope": {"environment": "preview"}}
        qa = {"id": requirement, "reason": "QA receipt", "scope": {"environment": "qa"}}
        auxiliary = {"id": "auxiliary-fixture", "reason": "Separate scope"}
        exceptions = (preview, auxiliary, qa)

        for status, field in (("failed", "failed"), ("not-run", "not_run"), ("blocked", "blocked")):
            with self.subTest(status=status):
                evidence = ({"id": requirement, "status": status, "reason": "Fixture observation"},)
                omitted = project_conformance(capsule.to_dict(), seed, evidence)
                self.assertIn(requirement, omitted["gaps"])
                self.assertEqual(omitted["exception_records"], [])
                projection = project_conformance(capsule.to_dict(), seed, evidence, exceptions)
                self.assertEqual(projection[field], [requirement])
                self.assertEqual(projection["demonstrated"], [])
                self.assertNotIn(requirement, projection["gaps"])
                self.assertEqual(projection["exceptions"], sorted({requirement, "auxiliary-fixture"}))
                received = json.loads(canonical_json(projection))
                self.assertEqual(received["exception_records"], list(exceptions))

    def test_conformance_validates_evidence_ids_without_coercing_text(self):
        seed = PlanningIR.for_test(verification=("exact fixture",))
        for value in (True, 17, ["nested"], {"value": "nested"}, " \u202f "):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "evidence id must be a nonblank string"):
                    project_conformance({}, seed, ({"id": value, "status": "passed"},))
        rows = ({"id": " exact fixture ", "status": "passed"}, {"id": "évidence", "status": "blocked"})
        receipt = project_conformance({}, seed, rows)
        self.assertEqual(receipt["demonstrated"], [" exact fixture "])
        self.assertEqual(receipt["blocked"], ["évidence"])
        self.assertEqual(receipt["gaps"], ["exact fixture"])
        self.assertEqual(receipt["evidence"], {row["id"]: row for row in rows})

    def test_conformance_rejects_duplicate_evidence_ids(self):
        class C: required_evidence=("x",)
        ir=PlanningIR.for_test(verification=(VerificationRequirement("x"),))
        with self.assertRaises(ValueError):
            project_conformance(C(),ir,({"id":"x","status":"passed"},{"id":"x","status":"failed"}))

    def test_not_applicable_requires_reason(self):
        class C: required_evidence=("x",)
        ir=PlanningIR.for_test()
        with self.assertRaises(ValueError):
            project_conformance(C(),ir,({"id":"x","status":"not-applicable"},))

    def test_not_applicable_blank_text_cannot_close_a_required_observation(self):
        descriptor = describe_task("Verify a Production release and its rollback readiness", {})
        capsule = solve_context(load_compiled("verification"), descriptor, "verification")
        ir = new_planning_ir(descriptor, capsule)
        requirement = ir.verification[0].id
        exceptions = (
            {"id": requirement, "scope": {"repository": "inert fixture"}, "reason": "Caller exception"},
            {"id": requirement, "scope": {"repository": "separate fixture"}},
        )
        wire = json.loads(canonical_json({"capsule": capsule.to_dict(), "ir": ir.to_dict()}))
        for ctx, plan in ((capsule, ir), (wire["capsule"], wire["ir"])):
            for blank in (" ", "\t\r\n", "\u00a0\u2003\u202f"):
                with self.subTest(wire=isinstance(ctx, dict), blank=repr(blank)):
                    record = {"id": requirement, "status": "not-applicable", "reason": blank}
                    with self.assertRaisesRegex(ValueError, "not-applicable requires reason or exception"):
                        project_conformance(ctx, plan, (record,))
                    excepted = project_conformance(ctx, plan, (record,), exceptions)
                    self.assertNotIn(requirement, excepted["gaps"])
                    self.assertEqual(excepted["exception_records"], list(exceptions))
                    self.assertEqual(excepted["evidence"][requirement], record)

            for reason in ("  Inert fixture lacks a deployed endpoint.  ", {"summary": "Documented by caller"}):
                record = {"id": requirement, "status": "not-applicable", "reason": reason}
                valid = project_conformance(ctx, plan, (record,))
                self.assertEqual(valid["evidence"][requirement], record)
                self.assertNotIn(requirement, valid["gaps"])

            extra = {"id": "inert-extra", "status": "not-applicable", "reason": " "}
            extra_projection = project_conformance(ctx, plan, (extra,))
            self.assertIn(requirement, extra_projection["gaps"])
            self.assertEqual(extra_projection["evidence"]["inert-extra"], extra)

    def test_not_applicable_bare_scalars_cannot_close_required_evidence(self):
        ir = PlanningIR.for_test(verification=("language-check",))
        for plan in (ir, ir.to_dict()):
            for reason in (True, 2, -1, 0.75):
                with self.subTest(wire=isinstance(plan, dict), reason=reason):
                    record = {"id": "language-check", "status": "not-applicable", "reason": reason}
                    with self.assertRaisesRegex(ValueError, "not-applicable requires reason or exception"):
                        project_conformance({}, plan, (record,))

                    exception = {"id": "language-check", "scope": {"surface": "fixture"}}
                    excepted = project_conformance({}, plan, (record,), (exception,))
                    self.assertEqual(excepted["gaps"], [])
                    self.assertEqual(excepted["exception_records"], [exception])
                    self.assertEqual(excepted["evidence"]["language-check"], record)

                    extra = {**record, "id": "fixture-extra"}
                    informational = project_conformance({}, plan, (extra,))
                    self.assertEqual(informational["gaps"], ["language-check"])
                    self.assertEqual(informational["evidence"]["fixture-extra"], extra)
                    self.assertEqual(informational["demonstrated"], [])

    def test_invalid_handbook_root_preserves_outputs_and_reports_freshness_problem(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            source = work / "source"
            source.mkdir()
            (source / "policy.md").write_text(source_doc("std-test", [unit("current")]), encoding="utf-8")
            output = work / "compiled"
            compile_handbook(source, output)
            known_good = {file.name: file.read_bytes() for file in output.iterdir()}

            for invalid in (work / "absent", source / "policy.md"):
                with self.subTest(invalid=invalid):
                    error = f"Handbook source root must be an existing directory ({invalid.resolve()})."
                    stderr = io.StringIO()
                    with redirect_stderr(stderr):
                        self.assertEqual(main(["compile-handbook", "--root", str(invalid), "--output", str(output)]), 2)
                    self.assertEqual(stderr.getvalue().strip(), error)
                    self.assertEqual(check_compiled_fresh(invalid, output), [error])
                    self.assertEqual({file.name: file.read_bytes() for file in output.iterdir()}, known_good)

            missing = work / "absent"
            with self.assertRaisesRegex(AgentContextError, "Handbook source root must be an existing directory"):
                compile_handbook(missing, missing / "machine-readable/compiled")
            self.assertFalse(missing.exists())

    def test_freshness_check_with_unavailable_temporary_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "policy.md").write_text(source_doc("std-test", [unit("u")]), encoding="utf-8")
            compiled = root / "compiled"
            compile_handbook(root, compiled)
            with mock.patch("tempfile.TemporaryDirectory", side_effect=PermissionError("fixture")):
                self.assertEqual(check_compiled_fresh(root, compiled), [])
                (compiled / "routing.json").write_text("{}", encoding="utf-8")
                (compiled / "graph.json").unlink()
                self.assertEqual(check_compiled_fresh(root, compiled), [
                    f"missing {compiled / 'graph.json'}",
                    f"stale {compiled / 'routing.json'}",
                ])

    def test_profile_derives_declared_values_and_segment_hash_from_one_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / ".engineering/context.json"
            source.parent.mkdir()
            raw = b'{\r\n  "decisions": {"scope": "first"}\r\n}\r\n'
            source.write_bytes(raw)
            reads = []
            original_open = Path.open

            def open_once(path, *args, **kwargs):
                if path == source:
                    reads.append(path)
                    self.assertEqual(len(reads), 1, "declaration file reopened during profiling")
                return original_open(path, *args, **kwargs)

            with mock.patch.object(Path, "open", open_once):
                profile = profile_repo(root)
            self.assertEqual(reads, [source])
            self.assertEqual(profile["declared"]["decisions"], {"scope": "first"})
            expected = stable_hash([(".engineering/context.json", hashlib.sha256(raw).hexdigest())])
            self.assertEqual(profile["meta"]["segment_hashes"]["declared"], expected)

    def test_profile_runtime_segment_tracks_pnpm_workspace_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "pnpm-workspace.yaml"
            catalog.write_text("catalog:\n  fixture-library: ^1.2.3\n", encoding="utf-8")
            first = profile_repo(root)
            self.assertIn("runtime", profile_repo(root, previous=first)["meta"]["reused_segments"])
            catalog.write_text("catalog:\n  fixture-library: ^2.2.3\n", encoding="utf-8")
            changed = profile_repo(root, previous=first)
            self.assertNotIn("runtime", changed["meta"]["reused_segments"])
            self.assertNotEqual(first["profile_hash"], changed["profile_hash"])
            self.assertEqual(first["meta"]["segment_hashes"]["declared"], changed["meta"]["segment_hashes"]["declared"])

    def test_checked_in_compiled_corpus_is_fresh(self):
        self.assertEqual(check_compiled_fresh(ROOT, COMPILED), [])

    def test_real_corpus_expiring_tenant_invitation_fits_budget_and_covers_risks(self):
        descriptor=describe_task("add expiring tenant invitation links", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        capsule=solve_context(load_compiled(), descriptor, "planning")
        self.assertEqual(capsule.uncovered, ())
        self.assertEqual(set(capsule.covered), set(descriptor.risks))
        self.assertLess(capsule.estimated_tokens, 600)

    def test_real_corpus_visual_accessibility_change_fits_budget_and_covers_risks(self):
        descriptor=describe_task("fix visual spacing and focus targets", {"detected":{"capabilities":{"pwa":True,"persistence":True,"auth":True}}})
        capsule=solve_context(load_compiled(), descriptor, "planning")
        self.assertIn("accessibility", descriptor.risks)
        self.assertEqual(capsule.uncovered, ())
        self.assertEqual(set(capsule.covered), set(descriptor.risks))
        self.assertLess(capsule.estimated_tokens, 600)

    def test_real_corpus_migration_change_fits_budget_and_covers_risks(self):
        descriptor=describe_task("add archived_at column and migration", {"detected":{"capabilities":{"persistence":True}}})
        capsule=solve_context(load_compiled(), descriptor, "planning")
        self.assertEqual(set(descriptor.risks), {"compatibility","data-loss"})
        self.assertEqual(capsule.uncovered, ())
        self.assertEqual(set(capsule.covered), set(descriptor.risks))
        self.assertLess(capsule.estimated_tokens, 600)

    def test_real_corpus_includes_intent_only_mandatory_policy_units(self):
        planning=solve_context(load_compiled("planning"), describe_task("add a new helper", {"detected":{"capabilities":{}}}), "planning")
        self.assertIn("reuse-before-new-design", {x["id"] for x in planning.units})
        verification=solve_context(load_compiled("verification"), describe_task("modify helper", {"detected":{"capabilities":{}}}), "verification")
        ids={x["id"] for x in verification.units}
        self.assertIn("verification-evidence-before-claims", ids)
        self.assertIn("verification-unrun-status", ids)


if __name__ == "__main__":
    unittest.main()
