from __future__ import annotations

import json
import io
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from automation.engineering_context.context_solver import build_repo_route
from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import describe_task


ROOT = Path(__file__).resolve().parents[2]
EMPTY = {"detected": {"capabilities": {}}}


class DiscoveryRoutingTests(unittest.TestCase):
    def test_questions_and_log_review_are_not_release_or_modify(self):
        for task in ("How to build and deploy to production?", "Inspect build and deployment logs",
                     "Explain how to build and deploy to production",
                     "Explica cómo construir y desplegar en producción",
                     "How to build, deploy and monitor production?"):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY)
                self.assertNotIn("modify", d.intent)
                self.assertNotIn("production-release", d.archetypes)
                self.assertFalse(d.delivery["production_effect"])
        d = describe_task("Review X, then deploy Y", EMPTY)
        self.assertIn("modify", d.intent)
        self.assertIn("production-release", d.archetypes)

    def test_coordinated_negation_keeps_both_actions_prohibited(self):
        for task in ("Do not deploy and migrate the database", "Please do not deploy and migrate the database",
                     "Por favor, no despliegues y migres la base de datos"):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY)
                self.assertNotIn("modify", d.intent)
                self.assertNotIn("migration", d.operations)
                self.assertFalse(d.delivery["production_effect"])
        d = describe_task("No migres; corrige permisos", EMPTY)
        self.assertNotIn("migration", d.operations)
        self.assertIn("modify", d.intent)
        self.assertIn("authorization", d.risks)

    def test_landmarks_resolve_real_case_sensitive_filenames(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ("AGENTS.md", "Dockerfile", "Makefile", "src/auth.ts"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("content")
            landmarks = profile_repo(root)["detected"]["landmarks"]
            for label, name in (("agent-configuration", "AGENTS.md"), ("release-config", "Dockerfile"),
                                ("verification", "Makefile"), ("authorization-boundary", "src/auth.ts")):
                with self.subTest(label=label):
                    self.assertIn(name, landmarks[label])

    def test_negated_migration_is_not_a_migration(self):
        for task in ("No cambies el schema ni hagas migrations", "Do not migrate the database", "No migres la base de datos; revisa la UI"):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY)
                self.assertNotIn("schema-change", d.archetypes)
                self.assertNotIn("migration", d.operations)
                self.assertNotIn("modify", d.intent)

    def test_spanish_and_english_migrations_have_equivalent_safeguards(self):
        for task in ("Migrar base de datos", "Añade una columna al esquema", "Migrate database", "Add a schema column"):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY)
                self.assertIn("schema-change", d.archetypes)
                self.assertIn("data-loss", d.risks)
                self.assertTrue(d.state["migration"])

    def test_review_and_production_observation_are_not_mutation_authority(self):
        for task in ("Consulta producción", "Revisa producción sin desplegar", "Inspect production", "Explain how tokens are counted"):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY)
                self.assertNotIn("modify", d.intent)
                self.assertNotIn("production-release", d.archetypes)
                self.assertFalse(d.delivery["production_effect"])
        self.assertIn("production-observation", describe_task("Consulta producción", EMPTY).archetypes)
        self.assertIn("production-release", describe_task("Despliega la versión en producción", EMPTY).archetypes)

    def test_non_credentials_and_read_only_sql_and_policy_docs(self):
        for task, paths in (
            ("Explain how tokens are counted", ()),
            ("Lee la consulta SQL", ("reports/select.sql",)),
            ("Revisa la política de seguridad", ("docs/security-policy.md",)),
        ):
            with self.subTest(task=task):
                d = describe_task(task, EMPTY, paths)
                self.assertNotIn("credential", d.risks)
                self.assertNotIn("schema-change", d.archetypes)
                self.assertNotIn("authorization", d.risks)
        self.assertIn("credential", describe_task("Rotate the access token", EMPTY).risks)

    def test_mixed_negation_preserves_authorization_and_actual_changes(self):
        d = describe_task("No migres datos; corrige los permisos de acceso", EMPTY)
        self.assertNotIn("schema-change", d.archetypes)
        self.assertIn("authorization", d.risks)
        self.assertIn("modify", d.intent)
        d = describe_task("Review migration diff, do not execute it", EMPTY, ("db/migrations/001.sql",))
        self.assertIn("data-loss", d.risks)
        self.assertNotIn("modify", d.intent)

    def test_api_and_custom_agent_configuration_have_explicit_routes(self):
        d = describe_task("Fix API", EMPTY)
        self.assertIn("external-integration", d.archetypes)
        d = describe_task("Review configuration", EMPTY, (".codex/agents/reviewer.toml",))
        self.assertIn("agent-tooling-change", d.archetypes)
        self.assertTrue(any(e.get("rule_id") for e in d.evidence))

    def test_real_deep_paths_and_invalid_declared_paths_are_explained(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ui = root / "apps/web/src/features/settings/components/page.tsx"
            ui.parent.mkdir(parents=True); ui.write_text("export default 1")
            migration = root / "db/migrations/001.sql"
            migration.parent.mkdir(parents=True); migration.write_text("select 1")
            config = root / ".engineering/context.json"
            config.parent.mkdir(); config.write_text(json.dumps({"landmarks": {"authorization-boundary": ["src/missing.ts", "../outside"]}}))
            p = profile_repo(root)
            d = describe_task("Rediseña la UI y migra el esquema con permisos", p)
            route = build_repo_route(p, d)
            self.assertIn(ui.relative_to(root).as_posix(), route["resolved"]["ui-surface"])
            self.assertIn(migration.relative_to(root).as_posix(), route["resolved"]["migrations"])
            self.assertNotIn("database", route["avoid_by_default"])
            self.assertTrue(route["unresolved"])
            self.assertTrue(p["declared"]["invalid_landmarks"])
            before = p["profile_hash"]
            (ui.parent / "other.tsx").write_text("export default 2")
            self.assertNotEqual(before, profile_repo(root)["profile_hash"])

    def test_registry_rejects_unknown_operators_and_duplicate_ids(self):
        from automation.engineering_context.discovery_rules import validate_registry
        for rules in (
            [{"id": "unsafe", "when": {"eval": "print(1)"}, "emit": ["risk:data-loss"]}],
            [{"id": "same", "when": {"text": "sql"}, "emit": ["risk:data-loss"]}] * 2,
        ):
            with self.assertRaises(ValueError):
                validate_registry({"schema": "discovery-rules/v1", "rules": rules})


    def test_endpoint_rate_limit_review_selects_existing_security_owner(self):
        for task, expected in (
            ("Audit rate limits for a public API endpoint", True),
            ("Revisa el límite de solicitudes del endpoint público", True),
            ("Review the animation frame rate limit in a dashboard", False),
            ("Review the animation frame rate limit in the API documentation preview", False),
            ("Inspect the display refresh rate limit field in the monitor API response", False),
            ("Inspect the request rate limit on the API endpoint serving the monitor", True),
            ("Review API rate limits alongside the animation frame-rate limit", True),
            ("Review documentation on API rate limits", False),
            ("Do not audit API rate limits; review typography", False),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, {})
                self.assertEqual("security-review" in descriptor.archetypes, expected)

    def test_per_pr_preview_database_routes_supabase_branch_authority(self):
        for task, expected in (
            ("Configure Supabase to provision a Preview database for each GitHub pull request", True),
            ("Configura Supabase para aprovisionar una base de datos Preview por cada pull request", True),
            ("Enable per-PR Preview databases in Supabase", True),
            ("Set up a Supabase Preview database for every pull request", True),
            ("Configura una base de datos de Preview de Supabase por cada PR", True),
            ("Provision a Preview database for every PR in the existing Supabase project", True),
            ("Configure Supabase to prevent automation that creates a Preview database for each GitHub pull request", False),
            ("Configure Supabase to reuse the existing Preview database rather than create one for each GitHub pull request", False),
            ("Reuse the existing Supabase database for each Vercel Preview", False),
            ("Enable reuse of the existing Supabase Preview database for each pull request", False),
            ("Habilita la reutilización de la base de datos Preview existente de Supabase por cada pull request", False),
            ("Provision a static site for each pull request using the existing Preview database on Supabase", False),
            ("Review whether Supabase would provision a Preview database for each pull request", False),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, {})
                self.assertEqual("supabase-database-branch-creation" in descriptor.archetypes, expected)

class KnowledgeDiscoveryTests(unittest.TestCase):
    def test_supabase_database_branch_creation_surfaces_the_owner_prerequisite(self):
        from automation.codex.handbook_update import local_bundle
        from automation.engineering_context.context_solver import solve_context
        from automation.engineering_context.discovery import search
        from automation.engineering_context.discovery_rules import load_registry

        compiled = ROOT / "machine-readable/compiled"
        routing = json.loads((compiled / "routing.json").read_bytes())
        index = json.loads((compiled / "discovery.json").read_bytes())
        views = {
            phase: json.loads((compiled / f"{phase}.json").read_bytes())
            for phase in ("planning", "implementation", "verification")
        }
        archetype = "supabase-database-branch-creation"
        unit_id = "supabase-database-branch-owner-authorization"
        cases = (
            ("Create a free Supabase database branch for Preview QA", True),
            ("Crear una rama gratuita de base de datos de Supabase para QA", True),
            ("Enable automatic Supabase Preview database branching", True),
            ("Conecta la integración de GitHub que crea una rama de base de datos de Supabase", True),
            ("Merge the Git branch that creates a Supabase Preview database branch", True),
            ("Configura GitHub para que cree automáticamente una rama de base de datos de Supabase", True),
            ("Habilita la ramificación automática de Supabase para Preview", True),
            ("Push the Git branch that triggers automatic Supabase Preview branching", True),
            ("Create a Git feature branch in a repository that uses Supabase", False),
            ("Create a Git branch; review Supabase database branches", False),
            ("Create a Git branch to document Supabase database branch creation", False),
            ("Create a Git branch to document automatic Supabase database branching", False),
            ("Enable automatic branching in Git for a Supabase client", False),
            ("Merge the Git branch that creates documentation for Supabase database branches", False),
            ("Inspect existing Supabase database branches", False),
            ("Do not create a Supabase database branch; run local SQL tests", False),
            ("No habilites ramificación automática de Supabase; ejecuta las pruebas SQL locales", False),
            ("Run the local PostgreSQL verification for this Supabase app", False),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(archetype in descriptor.archetypes, expected)
                for phase, view in views.items():
                    capsule = solve_context({**view, "routing": routing}, descriptor, phase)
                    selected = [unit for unit in capsule.units if unit["id"] == unit_id]
                    self.assertEqual(bool(selected), expected, phase)
                    if selected:
                        self.assertEqual(selected[0]["force"], "must")
                        self.assertEqual(selected[0]["source"], "pol-agent-operating-model")
                        self.assertEqual(selected[0]["covers"], [])
        entry = next(rule for rule in load_registry()["rules"] if rule["id"] == archetype)
        self.assertEqual(entry["emit"], [f"archetype:{archetype}"])

        owner = next(doc for doc in index["documents"] if doc["id"] == "pol-agent-operating-model")
        self.assertIn("all-repositories", owner["applies_to"])
        self.assertIsNotNone(owner["source_hash"])
        for query in (
            "Find the Handbook rule for Supabase database branches and Edgard approval",
            "¿Quién autoriza crear una rama de base de datos de Supabase?",
        ):
            with self.subTest(query=query):
                self.assertIn(owner["id"], {result["id"] for result in search(index, query, limit=5)})
        distributed = (ROOT / "agent-config/codex/AGENTS.global.md").read_text(encoding="utf-8")
        self.assertIn("## Supabase database branches", distributed)
        self.assertIn("Edgard's explicit prior authorization is required", distributed)
        self.assertIn("policies/agent-operating-model.md#supabase-database-branches", distributed)
        installed_policy = "references/policies/agent-operating-model.md"
        self.assertIn(f"`{installed_policy}`", distributed)
        self.assertIn("### Supabase database branches", local_bundle(ROOT)[installed_policy].decode("utf-8"))

    def test_compiler_is_lf_byte_stable_under_windows_text_translation(self):
        from automation.engineering_context.handbook_compile import compile_handbook, OUTPUT_FILES
        # Emulate Windows text-mode newline conversion on this Linux executor;
        # this is a portable contract test, not native Windows execution.
        def windows_write_text(path, data, encoding=None, errors=None, newline=None):
            if newline is None:
                data = data.replace("\n", "\r\n")
            path.write_bytes(data.encode(encoding or "utf-8"))
            return len(data)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); output = root / "compiled"
            with patch.object(Path, "write_text", new=windows_write_text):
                compile_handbook(root, output)
            for name in OUTPUT_FILES:
                self.assertNotIn(b"\r\n", (output / name).read_bytes(), name)

    def test_authority_registry_revision_changes_context_identity(self):
        from automation.engineering_context.canonical import stable_hash
        from automation.engineering_context.cli import main
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            compiled = root / "machine-readable/compiled"
            compiled.parent.mkdir()
            consumer = root / "consumer"
            consumer.mkdir()
            (compiled.parent / "catalog.yaml").write_text(
                "documents:\n  - id: registry-sources\n    kind: registry\n"
                "    path: machine-readable/sources.yaml\n    status: active\n    applies_to: [handbook]\n",
                encoding="utf-8",
            )
            registry = compiled.parent / "sources.yaml"
            original = b"sources:\n  - id: src-fixture\n    revision: previous\n"
            revised = original.replace(b"previous", b"revised")
            registry.write_bytes(original)

            def context():
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(main(["context", "--repo", str(consumer), "--handbook", str(compiled),
                                           "--mode", "plan", "--task", "Read the project guidance"]), 0)
                return json.loads(output.getvalue())

            compile_handbook(root, compiled)
            before = context()
            registry.write_bytes(revised)
            with self.assertRaisesRegex(RuntimeError, "compiled handbook context is stale"):
                context()
            rebuilt = compile_handbook(root, compiled)
            self.assertCountEqual(rebuilt.changed_files, ["discovery.json", "manifest.json"])
            after = context()
            self.assertNotEqual(before["discovery"]["index_hash"], after["discovery"]["index_hash"])
            self.assertNotEqual(before["context_id"], after["context_id"])
            self.assertEqual(before["capsule"]["units"], after["capsule"]["units"])
            index = json.loads((compiled / "discovery.json").read_bytes())
            record = next(doc for doc in index["documents"] if doc["id"] == "registry-sources")
            self.assertEqual(record["source_hash"], stable_hash(revised.decode("utf-8")))
            self.assertNotIn("revised", record["terms"])

            registry.write_bytes(revised.replace(b"\n", b"\r\n"))
            self.assertEqual(compile_handbook(root, compiled).changed_files, ())
            self.assertEqual(context()["context_id"], after["context_id"])

    def test_navigation_cli_returns_structured_results(self):
        from automation.engineering_context.cli import main
        commands = [
            ["search", "--query", "invocación subagentes"],
            ["tree", "--kind", "knowledge"],
            ["tree", "--kind", "execution"],
            ["tree", "--kind", "repository", "--repo", str(ROOT), "--task", "Review Codex hooks"],
            ["explain", "--repo", str(ROOT), "--task", "No migres datos; revisa permisos"],
            ["doctor"],
            ["integrity"],
        ]
        for args in commands:
            with self.subTest(command=args[0]):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main([*args, "--root", str(ROOT)])
                self.assertEqual(code, 0)
                payload = json.loads(output.getvalue())
                if args[0] == "explain":
                    self.assertNotIn("migration", payload["descriptor"]["operations"])
                    self.assertTrue(payload["rules"])
                if args[0] == "search":
                    self.assertTrue(payload["results"])

    def test_navigation_checks_only_the_routing_registries_it_uses(self):
        from automation.engineering_context.cli import main
        from automation.engineering_context.discovery_rules import load_registry
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            compiled = root / "machine-readable/compiled"
            registries = root / "machine-readable/discovery"
            registries.mkdir(parents=True)
            catalog = registries.parent / "catalog.yaml"
            empty_catalog = "version: 1\ndocuments:\n"
            catalog.write_text(empty_catalog, encoding="utf-8")
            (registries.parent / "agent-runtime-routing.v1.json").write_text(
                '{"model_routing":{"routes":[]}}', encoding="utf-8"
            )
            common = ["--repo", str(root), "--task", "Review documentation"]
            commands = {
                "context": ["context", "--handbook", str(compiled), "--mode", "plan", *common],
                "explain": ["explain", "--root", str(root), *common],
                "repository": ["tree", "--root", str(root), "--kind", "repository", *common],
                "execution": ["tree", "--root", str(root), "--kind", "execution"],
                "knowledge": ["tree", "--root", str(root), "--kind", "knowledge"],
                "search": ["search", "--root", str(root), "--query", "documentation"],
                "doctor": ["doctor", "--root", str(root), "--repo", str(root)],
                "doctor_index": ["doctor", "--root", str(root)],
            }
            routing = {"context", "explain", "repository"}
            for registry, blocked in (
                ("rules.v1.json", routing),
                ("landmarks.v1.json", routing | {"doctor"}),
                ("routes.v1.json", routing | {"execution"}),
            ):
                path = registries / registry
                data = load_registry(registry)
                # An undeclared registry and matching content in another root both remain supported.
                for variant in ("absent", "matching", "different", "missing-declared"):
                    if variant == "matching":
                        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    elif variant == "different":
                        path.write_text(json.dumps({**data, "fixture": "different registry"}), encoding="utf-8")
                    elif variant == "missing-declared":
                        path.unlink()
                        catalog.write_text(
                            empty_catalog + "  - id: fixture-registry\n    kind: registry\n"
                            f"    path: machine-readable/discovery/{registry}\n"
                            "    status: active\n    applies_to: [all]\n",
                            encoding="utf-8",
                        )
                    compile_handbook(root, compiled)
                    for name, args in commands.items():
                        with self.subTest(registry=registry, variant=variant, command=name):
                            output = io.StringIO()
                            with redirect_stdout(output):
                                if variant in {"different", "missing-declared"} and name in blocked:
                                    reason = "differs" if variant == "different" else "is missing"
                                    diagnostic = f"{registry} {reason}"
                                    if name == "doctor":
                                        self.assertEqual(main(args), 1)
                                        self.assertIn(diagnostic, json.loads(output.getvalue())["problems"][0])
                                    else:
                                        with self.assertRaisesRegex(RuntimeError, diagnostic):
                                            main(args)
                                        self.assertFalse(output.getvalue())
                                else:
                                    self.assertEqual(main(args), 0)
                                    self.assertIsInstance(json.loads(output.getvalue()), dict)
                catalog.write_text(empty_catalog, encoding="utf-8")

    def test_route_priority_is_part_of_freshness_and_the_checked_routes_are_used(self):
        from automation.engineering_context.cli import main
        from automation.engineering_context.discovery_rules import load_registry
        from automation.engineering_context.handbook_compile import check_compiled_fresh, compile_handbook

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry_dir = root / "machine-readable/discovery"
            registry_dir.mkdir(parents=True)
            (registry_dir.parent / "catalog.yaml").write_text("version: 1\ndocuments:\n", encoding="utf-8")
            registry_name = "routes.v1.json"
            path = registry_dir / registry_name
            compiled = root / "machine-readable/compiled"
            original_registry = load_registry(registry_name)
            original_routes = original_registry["routes"]
            reordered_routes = dict(reversed(list(original_routes.items())))
            reordered_registry = {**original_registry, "routes": reordered_routes}
            task = "Review the security of the product; audit the privacy of the product"
            args = ["--root", str(root), "--repo", str(root), "--task", task]

            def invoke(command):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(main(command), 0)
                return json.loads(output.getvalue())

            path.write_text(json.dumps(original_registry), encoding="utf-8")
            compile_handbook(root, compiled)
            first_index = json.loads((compiled / "discovery.json").read_text(encoding="utf-8"))
            first = invoke(["explain", *args])["repo_route"]["inspect_first"]
            self.assertEqual(first[0], "security-configuration")

            path.write_text(json.dumps(reordered_registry), encoding="utf-8")
            self.assertTrue(check_compiled_fresh(root, compiled))
            compile_handbook(root, compiled)
            second_index = json.loads((compiled / "discovery.json").read_text(encoding="utf-8"))
            self.assertEqual(first_index["registry_hashes"], second_index["registry_hashes"])
            self.assertNotEqual(first_index["index_hash"], second_index["index_hash"])
            with self.assertRaisesRegex(RuntimeError, "routes.v1.json differs"):
                invoke(["explain", *args])

            current = original_registry

            def runtime_registry(name):
                return current if name == registry_name else load_registry(name)

            with patch("automation.engineering_context.cli.load_registry", side_effect=runtime_registry):
                current = reordered_registry
                second = invoke(["explain", *args])["repo_route"]["inspect_first"]
                self.assertEqual(second[0], "privacy-data-lifecycle")
                tree = invoke(["tree", "--root", str(root), "--kind", "execution"])
                self.assertEqual(tree["route_order"], list(reordered_routes))

                original_routes["privacy-review"]["inspect_first"] = ["fresh-route-label", *original_routes["privacy-review"]["inspect_first"]]
                path.write_text(json.dumps(reordered_registry), encoding="utf-8")
                compile_handbook(root, compiled)
                third = invoke(["explain", *args])["repo_route"]["inspect_first"]
                self.assertEqual(third[0], "fresh-route-label")

            # The default direct caller keeps the checkout registry.
            self.assertEqual(build_repo_route(profile_repo(root), describe_task(task, {}))["inspect_first"], first)

    def test_canonical_integrity_includes_paths_metadata_and_sources(self):
        from automation.engineering_context.discovery import check_integrity
        self.assertEqual(check_integrity(ROOT), [])
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "machine-readable").mkdir()
            (root / "machine-readable/catalog.yaml").write_text("version: 1\ndocuments:\n  - id: missing\n    kind: policy\n    path: policies/missing.md\n    status: active\n    applies_to: [all]\n")
            (root / "machine-readable/sources.yaml").write_text("sources:\n")
            self.assertTrue(any("missing" in issue for issue in check_integrity(root)))

    def test_source_references_resolve_each_declared_member(self):
        import shutil
        import subprocess
        from automation.engineering_context.discovery import check_integrity

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "sources.yaml").write_bytes((ROOT / "machine-readable/sources.yaml").read_bytes())
            fixtures = {
                "inline": ('sources: [src-madr, "src-madr",]\n', ""),
                "block": ("sources:\n  - 'src-madr'\n", ""),
                "scalar": ("sources: 'src-madr'\n", ""),
                "empty": ("sources: []\n", ""),
                "unknown-block": ("sources:\n  - evidence-madr\n", "evidence-madr"),
                "unknown-inline": ("sources: [src-madr, evidence-missing]\n", "evidence-missing"),
                "unknown-scalar": ("sources: evidence-scalar\n", "evidence-scalar"),
                "bad-shape": ("sources: {id: src-madr}\n", None),
                "bad-member": ("sources: [src-madr, , src-madr]\n", None),
                "blank": ("sources:\n", None),
                "duplicate": ("sources: src-madr\nsources: []\n", None),
                "unknown-prose": ("sources: []\n", "src-unregistered-prose"),
                "unknown-repeat": ("sources: [evidence-repeat, evidence-repeat]\n", "evidence-repeat"),
                "crlf-vertical-scalar": ("sources:\v 'src-madr'\v\n", ""),
                "crlf-bad-member": ("sources: [src-madr\vbad]\n", None),
            }
            source_docs = root / "standards"
            source_docs.mkdir()
            records, expected, expected_native = ["documents:\n"], [], []
            for uid, (declaration, problem) in fixtures.items():
                path = f"standards/{uid}.md"
                records.append(f"  - id: {uid}\n    kind: standard\n    path: {path}\n    status: active\n    applies_to: [all]\n")
                prose = "\nsrc-unregistered-prose\nsrc-unregistered-prose\n" if uid == "unknown-prose" else ""
                delimiter = "---\v" if uid.startswith("crlf-") else "---"
                (root / path).write_text(
                    f"{delimiter}\nid: {uid}\nkind: standard\nstatus: active\nowner: engineering\nversion: 1\n"
                    f"applies_to: [all]\n{declaration}last_verified: 2026-11-21\nreview_due: 2027-02-21\n{delimiter}\n# Fixture\n{prose}",
                    encoding="utf-8",
                    newline="\r\n" if uid.startswith("crlf-") else "\n",
                )
                if problem is None:
                    expected.append(f"invalid-source-references:{uid}")
                    expected_native.append(f"invalid-source-references:{uid}")
                elif problem:
                    expected.append(f"unknown source: {uid}:{problem}")
                    expected_native.append(f"unknown-source-id:{uid}:{problem}")
                    if uid == "unknown-prose":
                        expected_native.append(f"unknown-source-id:{uid}:{problem}")
            (root / "decisions").mkdir()
            (root / "decisions/legacy.md").write_text("---\nstatus: accepted\n---\n# Historical fixture\n", encoding="utf-8")
            records.append("  - id: legacy\n    kind: decision\n    path: decisions/legacy.md\n    status: accepted\n    applies_to: [all]\n")
            (registry / "catalog.yaml").write_text("".join(records), encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            visual = "machine-readable/visual-directions.v1.json"
            (root / visual).write_text("{}", encoding="utf-8")
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook", "include": [visual]}), encoding="utf-8")
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertCountEqual(check_integrity(root), expected)

            shell = shutil.which("pwsh") or shutil.which("powershell")
            if shell:
                script = Path("automation/handbook/check-integrity.ps1")
                (root / script.parent).mkdir(parents=True)
                shutil.copyfile(ROOT / script, root / script)
                run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                     capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                self.assertCountEqual([line[6:] for line in run.stdout.splitlines() if line.startswith("ERROR ")], expected_native)

    def test_source_review_dates_are_calendar_dates_in_order(self):
        import shutil
        import subprocess
        from automation.engineering_context.discovery import check_integrity

        cases = (
            ("quoted-leap-day", "'2000-02-29'", '"2000-02-29"'),
            ("future", "2096-02-29", "2096-03-01"),
            ("bad-verified", "2100-02-29", "2100-03-01"),
            ("bad-due", "2024-02-29", "2024-04-31"),
            ("compact", "20240229", "2024-03-01"),
            ("reversed", "2026-01-01", "2025-12-31"),
        )
        expected = [
            "invalid-source-date:bad-verified:last_verified", "invalid-source-date:bad-due:review_due",
            "invalid-source-date:compact:last_verified", "source-review-precedes-verification:reversed",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "catalog.yaml").write_text("documents:\n", encoding="utf-8")
            record = (
                "  - id: {}\n    title: Date fixture\n    tier: A\n    kind: reference\n"
                "    url: https://example.invalid\n    canonical_language: en\n    applies_to: [all]\n"
                "    status: active\n    last_verified: {}\n    review_due: {}\n"
                "    volatility: low\n    reuse: link\n"
            )
            (registry / "sources.yaml").write_text("sources:\n" + "".join(record.format(*row) for row in cases), encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            visual = "machine-readable/visual-directions.v1.json"
            (root / visual).write_text("{}", encoding="utf-8")
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook", "include": [visual]}), encoding="utf-8")
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertCountEqual(check_integrity(root), expected)

            shell = shutil.which("pwsh") or shutil.which("powershell")
            if shell:
                script = Path("automation/handbook/check-integrity.ps1")
                (root / script.parent).mkdir(parents=True)
                shutil.copyfile(ROOT / script, root / script)
                run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                     capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                self.assertCountEqual([line[6:] for line in run.stdout.splitlines() if line.startswith("ERROR ")], expected)

    def test_integrity_compares_active_governed_scope_as_a_set(self):
        from automation.engineering_context.discovery import check_integrity, read_catalog

        hook = "ref-coding-agent-hook-isolation"
        donor = "ref-internal-ui-pwa-donor-audit"
        config = "cfg-codex-global-agents"
        decision = "adr-0004-owner-authorized-compact-role-pods"
        records = {row["id"]: row for row in read_catalog(ROOT) if row["id"] in (hook, donor, config, decision)}
        for uid in (hook, donor):
            records[uid]["applies_to"].reverse()
        for uid in (config, decision):
            records[uid]["applies_to"] = ["catalog-only-scope"]
        with patch("automation.engineering_context.discovery.read_catalog", return_value=list(records.values())):
            self.assertEqual(check_integrity(ROOT), [])
            records[hook]["applies_to"].remove("agent-plugins")
            records[donor]["applies_to"].remove("pwa")
            records[donor]["applies_to"].append("user-facing-web-surfaces")
            self.assertCountEqual(check_integrity(ROOT), [
                f"metadata mismatch: {hook}:applies_to",
                f"metadata mismatch: {donor}:applies_to",
            ])

    def test_all_catalog_entries_and_spanish_alias_search(self):
        from automation.engineering_context.discovery import build_discovery, search
        index = build_discovery(ROOT)
        self.assertGreater(len(index["documents"]), 125)
        hits = search(index, "invocación subagentes", limit=10)
        self.assertIn("pb-agent-runtime-routing", {hit["id"] for hit in hits})
        self.assertTrue(all(hit["status"] not in {"superseded", "retired"} for hit in hits))
        self.assertEqual(search(index, "zxqvnotarealword"), [])

    def test_decision_status_matches_its_markdown_before_discovery(self):
        from automation.engineering_context.discovery import build_discovery, check_integrity, search
        from automation.engineering_context.handbook_compile import compile_handbook
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            decision = root / "decisions/legacy.md"
            decision.parent.mkdir()
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            (catalog.parent / "sources.yaml").write_text("sources:\n", encoding="utf-8")
            row = (
                "documents:\n  - id: adr-legacy\n    kind: decision\n"
                "    path: decisions/legacy.md\n    status: superseded\n    applies_to: [handbook]\n"
            )
            catalog.write_text(row, encoding="utf-8")
            decision.write_text("---\nstatus: superseded\n---\n# Legacy routing policy\n", encoding="utf-8")
            output = catalog.parent / "compiled"
            compile_handbook(root, output)
            index = build_discovery(root)
            self.assertEqual(search(index, "legacy routing"), [])
            self.assertEqual(search(index, "legacy routing", historical=True)[0]["status"], "superseded")

            catalog.write_text(row.replace("status: superseded", "status: accepted"), encoding="utf-8")
            message = "metadata mismatch: adr-legacy:status"
            self.assertIn(message, check_integrity(root))
            with self.assertRaisesRegex(ValueError, message):
                compile_handbook(root, output)

            catalog.write_text(row.replace("kind: decision", "kind: template"), encoding="utf-8")
            self.assertIn("metadata mismatch: adr-legacy:kind", check_integrity(root))
            with self.assertRaisesRegex(ValueError, "metadata mismatch: adr-legacy:kind"):
                build_discovery(root)

            catalog.write_text(row, encoding="utf-8")
            for metadata, key in (("id: wrong\nstatus: superseded", "id"),
                                  ("kind: standard\nstatus: superseded", "kind"),
                                  ("date: 2026-11-21", "status")):
                with self.subTest(metadata=metadata):
                    decision.write_text(f"---\n{metadata}\n---\n# Legacy routing policy\n", encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, f"metadata mismatch: adr-legacy:{key}"):
                        build_discovery(root)

    def test_routing_decision_discovery_links_partial_and_complete_replacements(self):
        from automation.engineering_context.discovery import build_discovery, search
        index = build_discovery(ROOT)
        fixed_roles = "adr-0004-owner-authorized-compact-role-pods"
        upstream_catalog = "adr-0005-agency-agents-upstream-specialists"
        dynamic_routing = "adr-0006-dynamic-agency-agent-runtime-routing"
        quality_routing = "adr-0011-quality-first-codex-subagent-routing"
        manual_updates = "adr-0012-handbook-discovery-and-safe-preflight-update"
        for decision, amendment in ((upstream_catalog, dynamic_routing),
                                    (dynamic_routing, quality_routing),
                                    (quality_routing, manual_updates)):
            with self.subTest(decision=decision):
                entry = next(item for item in search(index, decision, limit=100) if item["id"] == decision)
                self.assertEqual(entry["status"], "accepted")
                self.assertIn(amendment, entry["amended_by"])
                self.assertNotIn({"from": amendment, "to": decision, "type": "supersedes"}, index["edges"])
        self.assertIn({"from": dynamic_routing, "to": fixed_roles, "type": "supersedes"}, index["edges"])
        self.assertNotIn(fixed_roles, {item["id"] for item in search(index, fixed_roles, limit=100)})
        archived = search(index, fixed_roles, limit=100, historical=True)
        self.assertIn(fixed_roles, {item["id"] for item in archived})

    def test_invalid_typed_graph_dependencies_and_cycles(self):
        from automation.engineering_context.discovery import validate_edges
        nodes = {"a", "b"}
        for edges in (
            [{"from": "a", "to": "missing", "type": "requires"}],
            [{"from": "a", "to": "b", "type": "requires"}, {"from": "b", "to": "a", "type": "requires"}],
            [{"from": "a", "to": "b", "type": "unknown"}],
        ):
            with self.assertRaises(ValueError):
                validate_edges(nodes, edges)

    def test_manual_handbook_adoption_review_routes_existing_evidence_only(self):
        from automation.engineering_context.cli import _load_compiled
        from automation.engineering_context.context_solver import solve_context

        view = _load_compiled(ROOT / "machine-readable/compiled", "verification")
        unit_id = "manual-handbook-adoption-evidence"
        for task in (
            "Audit the existing manual Engineering Handbook skill installation on Windows.",
            "Verifica que el manifiesto del bundle instalado del Engineering Handbook coincide con el checkout de confianza.",
            "No actives hooks ni descargues nada; revisa la instalación manual ya existente del Engineering Handbook.",
            "Verify the installed Engineering Handbook bundle using README as a reference.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(descriptor.intent, ("review",))
                self.assertFalse(descriptor.operations)
                capsule = solve_context(view, descriptor, "verification")
                self.assertIn(unit_id, capsule.required_evidence)
                self.assertIn("pb-handbook-discovery-and-update", capsule.provenance)
        for task in (
            "Install the Engineering Handbook skill manually on Windows.",
            "Actualiza el Engineering Handbook instalado en Windows.",
            "Review the installed Engineering Handbook bundle manifest documentation.",
            "Revisa la documentación de la instalación manual existente del Engineering Handbook.",
            "Audit the employee handbook and onboarding documentation.",
            "Audit the label next to the installed Engineering Handbook bundle.",
            "Audit the existing installation of our reporting utility alongside the Engineering Handbook docs.",
            "Do not audit the existing Engineering Handbook installation; review support logs.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertNotIn("handbook-manual-adoption-review", descriptor.archetypes)
                self.assertNotIn(unit_id, solve_context(view, descriptor, "verification").required_evidence)

    def test_adaptive_budget_never_claims_unmatched_task_is_safe(self):
        from automation.engineering_context.context_solver import budget_for, assessment_status
        simple = describe_task("Correct a typo", EMPTY)
        risky = describe_task("Migra datos y cambia permisos y secretos en producción", EMPTY)
        self.assertGreater(budget_for(risky).hard_max, budget_for(simple).hard_max)
        self.assertEqual(assessment_status(simple), "needs-discovery")


if __name__ == "__main__":
    unittest.main()
