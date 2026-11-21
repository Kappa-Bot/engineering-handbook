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

    def test_api_contract_schema_does_not_erase_or_invent_database_migrations(self):
        for task, changed, migration in (
            ("Verify input validation and compatible error semantics for a changed API request schema", (), False),
            ("Verifica los errores compatibles del esquema de solicitud de la API", (), False),
            ("Verify the API request body schema; review the existing database connection", (), False),
            ("Review the API request schema documentation", ("docs/api-request.md",), False),
            ("No migres la base de datos; revisa el esquema de respuesta de la API", (), False),
            ("Review the API request schema; review the PostgreSQL migration diff", (), True),
            ("Verifica el esquema de solicitud de la API y el esquema de la base de datos que cambió", (), True),
            ("Verify the API response schema", ("db/migrations/001.sql",), True),
        ):
            with self.subTest(task=task, changed=changed):
                descriptor = describe_task(task, EMPTY, changed)
                self.assertIn("review", descriptor.intent)
                self.assertNotIn("modify", descriptor.intent)
                self.assertEqual("schema-change" in descriptor.archetypes, migration)
                self.assertEqual("migration" in descriptor.operations, migration)
                self.assertEqual(descriptor.state["migration"], migration)
                self.assertEqual("data-loss" in descriptor.risks, migration)
                route = build_repo_route(EMPTY, descriptor)
                self.assertEqual("migration-validation" in route["verification"], migration)

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


    def test_registry_readers_reject_duplicate_json_members_before_writing(self):
        from automation.engineering_context.discovery_rules import load_registry
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            machine = root / "machine-readable"
            registries = machine / "discovery"
            output = machine / "compiled"
            registries.mkdir(parents=True)
            (machine / "catalog.yaml").write_text("documents:\n", encoding="utf-8")
            compile_handbook(root, output)
            previous = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in output.iterdir()}

            bases = {
                "rules": '{"schema":"discovery-rules/v1","rules":[]}',
                "landmarks": '{"schema":"discovery-landmarks/v1","landmarks":{}}',
                "routes": '{"schema":"discovery-routes/v1","routes":{}}',
                "taxonomy": '{"schema":"discovery-taxonomy/v1","topics":[]}',
            }
            for name, base in bases.items():
                with self.subTest(name=name):
                    file = registries / f"{name}.v1.json"
                    file.write_text(base[:-1] + ',"fixture":{"nested":0,"nested":1}}', encoding="utf-8")
                    diagnostic = rf"{name}\.v1\.json: duplicate discovery registry JSON member 'nested'"
                    with patch("automation.engineering_context.discovery_rules.REGISTRY_DIR", registries):
                        with self.assertRaisesRegex(ValueError, diagnostic):
                            load_registry(file.name)
                    with self.assertRaisesRegex(ValueError, diagnostic):
                        compile_handbook(root, output)
                    self.assertEqual(
                        {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in output.iterdir()},
                        previous,
                    )
                    file.unlink()

    def test_discovery_rules_report_invalid_rows_scope_and_regexp(self):
        from automation.engineering_context.discovery_rules import validate_registry

        rule = {"id": "fixture", "when": {"text": "example"}, "emit": ["intent:inspect"]}
        cases = (
            ([rule, None], "rules[1] must be an object"),
            ([dict(rule, scope=[])], "invalid rule scope: fixture"),
            ([dict(rule, when={"text": "["})], "invalid discovery text regex"),
            ([dict(rule, when={"path": "("})], "invalid discovery path regex"),
            ([dict(rule, when={"text": "a{100000000000}"})], "invalid discovery text regex"),
        )
        for rows, diagnostic in cases:
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError) as found:
                    validate_registry({"schema": "discovery-rules/v1", "rules": rows})
                self.assertIn(diagnostic, str(found.exception))

    def test_route_registry_rejects_malformed_inspection_specs(self):
        from automation.engineering_context.discovery import build_discovery
        from automation.engineering_context.discovery_rules import load_registry

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable" / "discovery"
            registry.mkdir(parents=True)
            path = registry / "routes.v1.json"
            cases = (
                ({"gate": "wrong"}, "routes['gate'] must be an object"),
                ({"gate": {"inspect_first": "first"}}, "routes['gate'].inspect_first must be an array of strings"),
                ({"gate": {"inspect_first": [None]}}, "routes['gate'].inspect_first must be an array of strings"),
                ({"gate": {"avoid": {"path": True}}}, "routes['gate'].avoid must be an array of strings"),
            )
            with patch("automation.engineering_context.discovery_rules.REGISTRY_DIR", registry):
                for routes, diagnostic in cases:
                    with self.subTest(routes=routes):
                        path.write_text(json.dumps({"routes": routes}), encoding="utf-8")
                        for read in (lambda: load_registry(path.name), lambda: build_discovery(root)):
                            with self.assertRaises(ValueError) as error:
                                read()
                            self.assertIn(diagnostic, str(error.exception))
                routes = {"empty": {}, "later": {"inspect_first": ["first", "second"], "extra": {"keep": True}}}
                original = {"routes": routes}
                path.write_text(json.dumps(original), encoding="utf-8")
                self.assertEqual(load_registry(path.name), original)
                self.assertEqual(build_discovery(root)["route_order"], ["empty", "later"])


    def test_manual_doctor_rejects_wrong_model_route_shapes(self):
        from automation.engineering_context.cli import main
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            machine = root / "machine-readable"
            compile_handbook(root, machine / "compiled")
            path = machine / "agent-runtime-routing.v1.json"
            for routes, diagnostic in (
                ({}, "model_routing.routes must be an array"),
                ([None], "model_routing.routes[0] must be an object"),
                ([{"model": []}], "model_routing.routes[0].model must be a nonblank string"),
            ):
                with self.subTest(routes=routes):
                    path.write_text(json.dumps({"model_routing": {"routes": routes}}), encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(["doctor", "--root", str(root)]), 1)
                    self.assertIn(diagnostic, json.loads(output.getvalue())["problems"][0])
            path.write_text(json.dumps({"model_routing": {"routes": [{"selection": "fixture"}]}}), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["doctor", "--root", str(root)]), 0)

    def test_manual_doctor_checks_current_model_tier_recommendations(self):
        from automation.engineering_context.cli import main
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            machine = root / "machine-readable"
            compile_handbook(root, machine / "compiled")
            path = machine / "agent-runtime-routing.v1.json"
            routes = [{"selection": "require-observation"}]
            for tiers, exit_code in (
                ({"efficient": "gpt-6-luna"}, 1),
                ({"future-visual": "GpT-6-LuNa"}, 1),
                ({"future-visual": "fixture-model-with-unobserved-availability"}, 0),
            ):
                with self.subTest(tiers=tiers):
                    runtime = {"model_routing": {"routes": routes, "current_tiers": tiers}}
                    path.write_text(json.dumps(runtime), encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(main(["doctor", "--root", str(root)]), exit_code)
                    problems = ["blocked model remains in active tier recommendation"] if exit_code else []
                    self.assertEqual(json.loads(output.getvalue())["problems"], problems)

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

    def test_discovery_and_context_use_the_views_compared_for_freshness(self):
        from automation.engineering_context.cli import main
        from automation.engineering_context.handbook_compile import OUTPUT_FILES

        compiled = ROOT / "machine-readable" / "compiled"
        read_bytes = Path.read_bytes
        read_text = Path.read_text

        with tempfile.TemporaryDirectory() as directory:
            commands = (
                ["search", "--root", str(ROOT), "--query", "gov-source-authority"],
                ["tree", "--root", str(ROOT), "--kind", "execution"],
                ["doctor", "--root", str(ROOT)],
                ["explain", "--root", str(ROOT), "--repo", directory, "--task", "Review keyboard focus"],
                ["context", "--handbook", str(compiled), "--repo", directory, "--mode", "verify", "--task", "Review keyboard focus"],
            )
            for command in commands:
                with self.subTest(command=command[0]):
                    reads: list[tuple[str, str]] = []

                    def track_bytes(path, *args, **kwargs):
                        if path.parent == compiled and path.name in OUTPUT_FILES:
                            reads.append((path.name, "bytes"))
                        return read_bytes(path, *args, **kwargs)

                    def track_text(path, *args, **kwargs):
                        if path.parent == compiled and path.name in OUTPUT_FILES:
                            reads.append((path.name, "text"))
                        return read_text(path, *args, **kwargs)

                    with patch.object(Path, "read_bytes", track_bytes), patch.object(Path, "read_text", track_text):
                        with redirect_stdout(io.StringIO()) as response:
                            self.assertEqual(main(command), 0)
                    self.assertIsInstance(json.loads(response.getvalue()), dict)
                    self.assertCountEqual(reads, [(name, "bytes") for name in OUTPUT_FILES])

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

    def test_knowledge_tree_fallback_ids_are_unique_across_history_views(self):
        from automation.engineering_context.discovery import knowledge_tree

        def document(uid, kind, status="active"):
            return {"id": uid, "title": uid, "kind": kind, "path": f"{uid}.md", "status": status}

        topics = [
            {"id": "pattern", "title": "Pattern topic", "artifacts": ["example"]},
            {"id": "kind:pattern", "title": "Historical topic", "artifacts": []},
        ]
        index = {"topics": topics, "documents": [
            document("example", "reference"), document("current", "pattern"),
            document("historical", "kind:pattern", "retired"),
            document("reserved", "kind:kind:pattern", "superseded"),
        ]}
        current = knowledge_tree(index)["children"]
        historical = knowledge_tree(index, historical=True)["children"]
        for groups in (current, historical):
            ids = [group["id"] for group in groups]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(ids[:2], ["pattern", "kind:pattern"])
            self.assertEqual(groups[0]["children"], [index["documents"][0]])
            by_label = {group["title"]: group["id"] for group in groups}
            self.assertEqual(by_label["pattern"], "kind:kind:kind:kind:pattern")
        self.assertEqual(by_label["kind:pattern"], "kind:kind:kind:pattern")
        self.assertEqual(by_label["kind:kind:pattern"], "kind:kind:pattern")

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

    def test_catalog_headers_describe_one_document_sequence(self):
        from automation.engineering_context.discovery import read_catalog

        row = ("  - id: guide\n    kind: template\n    path: notes/Guía.md\n"
               "    status: active\n    applies_to: [engineering-handbook]\n")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            for body, error in (
                ("version: 1\nversion: 2\n", "duplicate catalog header version at line 2"),
                ("documents:\n" + row + "documents:\n", "duplicate catalog header documents at line 7"),
                ("documents: [other]\n", "unsupported catalog documents value at line 1"),
                ("documents: []\n" + row, "catalog record outside documents at line 2"),
                (row + "documents:\n", "catalog documents header follows records at line 6"),
                ("documents:\nversion: 1\n" + row, "catalog record outside documents at line 3"),
            ):
                with self.subTest(body=body):
                    catalog.write_text(body, encoding="utf-8")
                    with self.assertRaises(ValueError) as rejected:
                        read_catalog(root)
                    self.assertEqual(str(rejected.exception), error)
            for body, count in ((row, 1), ("version: '0.1'\n" + row, 1), ("documents: # owned rows\n" + row, 1),
                                ("documents:\n" + row + "version: 1\n", 1), ("documents: [ ] # empty\n", 0)):
                catalog.write_text(body, encoding="utf-8")
                self.assertEqual([item["path"] for item in read_catalog(root)], ["notes/Guía.md"] * count)

    def test_catalog_rejects_case_collisions_without_normalizing_visible_paths(self):
        from automation.engineering_context.discovery import read_catalog

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()

            def row(uid, path):
                return (
                    f"  - id: {uid}\n"
                    "    kind: entrypoint\n"
                    f"    path: {path}\n"
                    "    status: active\n"
                    "    applies_to: [engineering-handbook]\n"
                )

            first = row("doc-guide", "notes/Guide.md")
            for uid, path, error in (
                ("doc-work", "notes/Guía-Work.md", None),
                ("doc-dot", "./notes/Guide.md", "noncanonical catalog path: ./notes/Guide.md"),
                ("doc-nested-dot", "notes/./Guide.md", "noncanonical catalog path: notes/./Guide.md"),
                ("doc-slash", "notes//Guide.md", "noncanonical catalog path: notes//Guide.md"),
                ("doc-trailing", "notes/Guide.md/", "noncanonical catalog path: notes/Guide.md/"),
                ("doc-other", "notes/.release-notes.v2.md", None),
                ("doc-other", "notes/Guide.md", "duplicate catalog identity: doc-other"),
                ("doc-guide", "notes/Else.md", "duplicate catalog identity: doc-guide"),
                ("doc-alias", "notes/guide.md", "case-colliding catalog paths: notes/Guide.md and notes/guide.md"),
            ):
                with self.subTest(uid=uid, path=path):
                    catalog.write_text("version: 1\ndocuments:\n" + first + row(uid, path), encoding="utf-8")
                    if error:
                        with self.assertRaises(ValueError) as rejected:
                            read_catalog(root)
                        self.assertEqual(str(rejected.exception), error)
                    else:
                        self.assertEqual([entry["path"] for entry in read_catalog(root)], ["notes/Guide.md", path])

            distinct_unicode_paths = ["notes/Straße.md", "notes/Strasse.md"]
            catalog.write_text(
                "version: 1\ndocuments:\n"
                + row("doc-street-a", distinct_unicode_paths[0])
                + row("doc-street-b", distinct_unicode_paths[1]),
                encoding="utf-8",
            )
            self.assertEqual([entry["path"] for entry in read_catalog(root)], distinct_unicode_paths)

    def test_catalog_governed_lifecycle_preserves_historical_and_other_kind_statuses(self):
        from automation.engineering_context.discovery import read_catalog

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            for kind, status in (
                ("reference", "actvie"), ("policy", "Active"), ("standard", "deprecated"),
                ("pattern", "archived"), ("playbook", "draft"), ("decision", "accepted"),
                ("implementation-plan", "accepted"), ("entrypoint", "project-specific"),
            ):
                with self.subTest(kind=kind, status=status):
                    catalog.write_text(
                        f"documents:\n  - id: fixture\n    kind: {kind}\n    path: fixture.md\n"
                        f"    status: {status}\n    applies_to: [handbook]\n", encoding="utf-8",
                    )
                    if status in {"actvie", "Active"}:
                        with self.assertRaisesRegex(ValueError, f"invalid governed catalog status: fixture: {status}"):
                            read_catalog(root)
                    else:
                        self.assertEqual(read_catalog(root)[0]["status"], status)

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

    def test_powershell_integrity_reads_utf8_catalog_paths(self):
        import shutil
        import subprocess

        shells = [path for name in ("pwsh", "powershell") if (path := shutil.which(name))]
        if not shells:
            self.skipTest("PowerShell is unavailable")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            docs = root / "standards"
            docs.mkdir()
            machine = root / "machine-readable"
            machine.mkdir()
            catalog = ["documents:\n"]
            for uid, name in (("std-accented", "Café y revisión.md"), ("std-hanzi", "发布 检查.md")):
                (docs / name).write_text(
                    f"---\nid: {uid}\nkind: standard\nstatus: active\nowner: engineering\n"
                    "version: 0.1\napplies_to: [fixture]\nsources: []\n"
                    "last_verified: 2026-01-15\nreview_due: 2028-01-01\n---\n\n# Fixture\n",
                    encoding="utf-8",
                )
                catalog.append(f"  - id: {uid}\n    kind: standard\n    path: standards/{name}\n"
                               "    status: active\n    applies_to: [fixture]\n")
            (machine / "sources.yaml").write_text("sources:\n", encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook",
                                          "include": ["standards"]}), encoding="utf-8")
            script = Path("automation/handbook/check-integrity.ps1")
            (root / script.parent).mkdir(parents=True)
            shutil.copyfile(ROOT / script, root / script)
            rows = "".join(catalog)
            for source, error in (
                (rows + "version: 1\n", None),
                ("documents: # open sequence\n    kind: standard\n", "catalog field outside documents at line 2"),
                (rows + "version: 1\n    path: standards/Ausente.md\n", "catalog field outside documents"),
            ):
                (machine / "catalog.yaml").write_text(source, encoding="utf-8")
                for shell in shells:
                    with self.subTest(shell=Path(shell).name, source=source):
                        result = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                                capture_output=True, text=True, errors="replace", timeout=30)
                        if error:
                            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                            self.assertIn(error, " ".join(result.stderr.split()))
                        else:
                            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                            self.assertEqual(result.stdout.strip(), "PASS handbook-integrity catalog=2 sources=0")

    def test_powershell_integrity_reports_short_markdown_by_document_kind(self):
        import shutil
        import subprocess

        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            self.skipTest("PowerShell is unavailable")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "sources.yaml").write_text("sources:\n", encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook",
                                          "include": ["docs"]}), encoding="utf-8")
            script = Path("automation/handbook/check-integrity.ps1")
            (root / script.parent).mkdir(parents=True)
            shutil.copyfile(ROOT / script, root / script)
            (root / "docs").mkdir()
            records = ["documents:\n"]
            for name, kind, content in (
                ("heading", "entrypoint", "# Start here"),
                ("empty-intro", "entrypoint", ""),
                ("short-policy", "policy", "# Missing metadata"),
                ("empty-policy", "policy", ""),
            ):
                relative = f"docs/{name}.md"
                (root / relative).write_text(content, encoding="utf-8")
                records.append(f"  - id: {name}\n    kind: {kind}\n    path: {relative}\n"
                               "    status: active\n    applies_to: [all]\n")
            (registry / "catalog.yaml").write_text("".join(records), encoding="utf-8")
            run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                 capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
            self.assertEqual(run.stderr, "")
            self.assertCountEqual([line for line in run.stdout.splitlines() if line.startswith("ERROR ")], [
                "ERROR missing-frontmatter:short-policy:docs/short-policy.md",
                "ERROR missing-frontmatter:empty-policy:docs/empty-policy.md",
            ])
            self.assertIn("FAIL handbook-integrity errors=2", run.stdout)

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

    def test_source_registry_rejects_repeated_known_fields_in_each_entry(self):
        import shutil
        import subprocess
        from automation.engineering_context.discovery import check_integrity

        row = (
            "  - id: src-test\n    tier: A\n    url: https://example.invalid\n"
            "    title: Fixture\n    kind: reference\n    canonical_language: en\n"
            "    applies_to: [all]\n    status: active\n    last_verified: 2024-02-29\n"
            "    review_due: 2025-02-28\n    volatility: low\n    reuse: link\n    version: 1\n"
        )
        duplicate = (
            "    tier: U\n    URL:\n    url: https://example.invalid/other\n    id: src-shadow\n"
            "    review_due: 2100-04-31\n    version: 0\n    fixture_only: first\n"
            "    fixture_only: second\n    fixture_nested:\n      last_verified: inert\n"
        )
        expected = [f"duplicate-source-field:src-test:{key}" for key in ("id", "review_due", "tier", "url", "version")]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "catalog.yaml").write_text("documents:\n", encoding="utf-8")
            rows = row.replace("  - id: src-test\n", "  - id: src-test\n" + duplicate)
            rows += row.replace("  - id: src-test\n", "  - id: src-valid\n")
            (registry / "sources.yaml").write_bytes(("sources:\n" + rows).replace("\n", "\r\n").encode("utf-8"))
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

    def test_active_governed_review_dates_are_calendar_dates_without_expiry(self):
        import shutil
        import subprocess
        from automation.engineering_context.discovery import check_integrity

        cases = (
            ("bad-day", "active", "2100-02-29", "2100-03-01"),
            ("bad-due", "active", "2024-02-29", "2024-04-31"),
            ("reversed", "active", "2026-01-01", "2025-12-31"),
            ("empty", "active", "", "''"),
            ("overdue", "active", "'2000-02-29'", '"2000-02-29"'),
            ("retired", "retired", "older-unknown", "older-unknown"),
        )
        expected = [
            "invalid-document-date:bad-day:last_verified", "invalid-document-date:bad-due:review_due",
            "document-review-precedes-verification:reversed", "invalid-document-date:empty:last_verified",
            "invalid-document-date:empty:review_due",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "sources.yaml").write_text("sources:\n", encoding="utf-8")
            (root / "policies").mkdir()
            records = ["documents:\n"]
            for uid, status, verified, due in cases:
                relative = f"policies/{uid}.md"
                records.append(f"  - id: {uid}\n    kind: policy\n    path: {relative}\n"
                               f"    status: {status}\n    applies_to: [all]\n")
                (root / relative).write_text(
                    f"---\nid: {uid}\nkind: policy\nstatus: {status}\nowner: engineering\nversion: 1\n"
                    f"applies_to: [all]\nsources: []\nlast_verified: {verified}\nreview_due: {due}\n---\n# Fixture\n",
                    encoding="utf-8",
                )
            adr = root / "decisions/legacy.md"
            adr.parent.mkdir()
            adr.write_text("---\nstatus: superseded\n---\n# Legacy decision\n", encoding="utf-8")
            records.append("  - id: legacy\n    kind: decision\n    path: decisions/legacy.md\n"
                           "    status: superseded\n    applies_to: [all]\n")
            (registry / "catalog.yaml").write_text("".join(records), encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            visual = "machine-readable/visual-directions.v1.json"
            (root / visual).write_text("{}", encoding="utf-8")
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook",
                                          "include": [visual]}), encoding="utf-8")
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertCountEqual(check_integrity(root), expected)
            shell = shutil.which("pwsh") or shutil.which("powershell")
            if shell:
                script = Path("automation/handbook/check-integrity.ps1")
                (root / script.parent).mkdir(parents=True)
                shutil.copyfile(ROOT / script, root / script)
                result = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertCountEqual([line[6:] for line in result.stdout.splitlines() if line.startswith("ERROR ")],
                                      expected)

    def test_compiled_discovery_uses_one_catalog_read_per_build(self):
        from automation.engineering_context.canonical import stable_hash
        from automation.engineering_context.discovery import build_discovery
        from automation.engineering_context.handbook_compile import verified_compiled_payloads

        catalog = ROOT / "machine-readable" / "catalog.yaml"
        target = ROOT / "machine-readable" / "compiled"
        original = Path.read_text
        catalog_hash = stable_hash(original(catalog, encoding="utf-8"))
        reads: list[Path] = []

        def watch(path, *args, **kwargs):
            if path == catalog:
                reads.append(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", watch):
            payloads, problems = verified_compiled_payloads(ROOT, target)
        self.assertEqual(problems, [])
        self.assertEqual(reads, [catalog])
        self.assertEqual(payloads["discovery.json"]["catalog_source_hash"], catalog_hash)

        reads.clear()
        with patch.object(Path, "read_text", watch):
            direct = build_discovery(ROOT)
        self.assertEqual(reads, [catalog])
        self.assertEqual(direct["catalog_source_hash"], catalog_hash)

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

    def test_taxonomy_edge_shapes_are_checked_before_amendment_and_graph_projection(self):
        from automation.engineering_context.discovery import build_discovery

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "machine-readable/discovery/taxonomy.v1.json"
            path.parent.mkdir(parents=True)
            topic = {"id": "fixture", "title": "Fixture", "artifacts": []}
            other = {"id": "other", "title": "Other", "artifacts": []}
            edge = {"from": "topic:fixture", "to": "topic:other", "type": "related"}
            for edges, error in (
                ({}, "edges must be a list"),
                ("", "edges must be a list"),
                ([edge, None], "edges[1] must be an object"),
                ([{"to": "topic:other", "type": "related"}], "edges[0].from must be a string"),
                ([{**edge, "type": []}], "edges[0].type must be a string"),
            ):
                with self.subTest(edges=edges):
                    path.write_text(json.dumps({"topics": [topic, other], "edges": edges}), encoding="utf-8")
                    with self.assertRaises(ValueError) as failed:
                        build_discovery(root)
                    self.assertEqual(str(failed.exception), "taxonomy.v1.json: " + error)

            path.write_text(json.dumps({"topics": [topic, other], "edges": [edge, {**edge, "note": "context"}]}), encoding="utf-8")
            self.assertEqual(build_discovery(root)["edges"], [edge])

    def test_complete_catalog_id_precedes_lexical_matches_among_visible_documents(self):
        from automation.engineering_context.discovery import search

        def document(uid, terms, status="active"):
            return {"id": uid, "title": uid, "path": f"{uid}.md", "kind": "reference",
                    "status": status, "excerpt": "", "amended_by": [], "length": sum(terms.values()),
                    "terms": terms}

        index = {"documents": [document("change", {"change": 1, "other": 7}),
                               document("changes", {"change": 8}),
                               document("the", {"other": 1}, status="superseded")]}
        lexical = search(index, "change.")
        self.assertEqual([hit["id"] for hit in lexical], ["changes", "change"])
        self.assertEqual(search(index, "  CHANGE ", limit=1), lexical[1:])
        self.assertEqual(search(index, "the"), [])
        archived = search(index, "the", historical=True)
        self.assertEqual([(hit["id"], hit["score"], hit["matched_terms"]) for hit in archived],
                         [("the", 0.0, [])])

    def test_taxonomy_topics_require_typed_fields_and_catalog_members(self):
        from automation.engineering_context.discovery import build_discovery

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "machine-readable/discovery/taxonomy.v1.json"
            path.parent.mkdir(parents=True)
            first = {"id": "topic-one", "title": "One", "artifacts": [], "optional_note": "retain"}
            second = {"id": "topic-two", "title": "Two", "artifacts": [], "aliases": [""]}
            for topics, diagnostic in (
                ({}, "topics must be a list"),
                ([first, False], "topics[1] must be an object"),
                ([{**first, "id": " "}], "topics[0].id must be a nonblank string"),
                ([{**first, "title": 1}], "topics[0].title must be a nonblank string"),
                ([{**first, "artifacts": ""}], "topics[0].artifacts must be a list"),
                ([{**first, "artifacts": [False]}], "topics[0].artifacts[0] must be a string"),
                ([{**first, "aliases": {"alias": "not a list"}}], "topics[0].aliases must be a list"),
                ([{**first, "aliases": ["alias", False]}], "topics[0].aliases[1] must be a string"),
            ):
                with self.subTest(topics=topics):
                    path.write_text(json.dumps({"topics": topics}), encoding="utf-8")
                    with self.assertRaises(ValueError) as failure:
                        build_discovery(root)
                    self.assertEqual(str(failure.exception), "taxonomy.v1.json: " + diagnostic)

            path.write_text(json.dumps({"topics": [{**first, "artifacts": ["topic:topic-two"]}, second]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid discovery edge:"):
                build_discovery(root)
            path.write_text(json.dumps({"topics": [second, first]}), encoding="utf-8")
            self.assertEqual(build_discovery(root)["topics"], [second, first])

    def test_search_amendments_use_the_same_distinct_relationships_as_the_graph(self):
        from automation.engineering_context.discovery import build_discovery, search

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "machine-readable" / "discovery"
            registry.mkdir(parents=True)
            catalog = ["documents:"]
            for uid in ("target", "prior", "later"):
                name = f"{uid}.md"
                (root / name).write_text(f"# {uid} record\n", encoding="utf-8")
                catalog.extend((f"  - id: {uid}", "    kind: entrypoint", f"    path: {name}",
                                "    status: active", "    applies_to: [all]"))
            (registry.parent / "catalog.yaml").write_text("\n".join(catalog) + "\n", encoding="utf-8")
            first = {"from": "prior", "to": "target", "type": "amends"}
            second = {"from": "later", "to": "target", "type": "amends"}
            (registry / "taxonomy.v1.json").write_text(
                json.dumps({"edges": [first, second, dict(first, editor_note="same relationship")]}),
                encoding="utf-8",
            )
            index = build_discovery(root)
            exact = search(index, "target", limit=1)[0]
            self.assertEqual(exact["id"], "target")
            self.assertEqual(exact["amended_by"], ["later", "prior"])
            self.assertEqual([edge for edge in index["edges"] if edge["type"] == "amends"], [second, first])

    def test_empty_atx_heading_does_not_become_document_title(self):
        from automation.engineering_context.discovery import build_discovery, search

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            machine = root / "machine-readable"
            machine.mkdir()
            (machine / "catalog.yaml").write_text(
                "documents:\n  - id: heading-fixture\n    kind: entrypoint\n"
                "    path: heading.md\n    status: active\n    applies_to: [all]\n", encoding="utf-8",
            )
            for text, title in (
                ("#\nParagraph\n\n# Actual heading\n", "Actual heading"),
                ("# \t \nParagraph\n", "heading fixture"),
                ("# ###\nParagraph\n", "heading fixture"),
                ("#\t## Real content\n", "## Real content"),
                ("# \u00a0Résumé conservé\n", "Résumé conservé"),
                ("# \u202fÉtendue conservée\n", "Étendue conservée"),
                ("# \u00a0###\n\n# Suite\n", "###"),
            ):
                with self.subTest(text=text):
                    (root / "heading.md").write_text(text, encoding="utf-8")
                    hits = search(build_discovery(root), "heading-fixture", limit=1)
                    self.assertEqual(hits[0]["title"], title)

    def test_all_catalog_entries_and_spanish_alias_search(self):
        from automation.engineering_context.discovery import build_discovery, search
        index = build_discovery(ROOT)
        self.assertGreater(len(index["documents"]), 125)
        hits = search(index, "invocación subagentes", limit=10)
        self.assertIn("pb-agent-runtime-routing", {hit["id"] for hit in hits})
        self.assertTrue(all(hit["status"] not in {"superseded", "retired"} for hit in hits))
        self.assertEqual(search(index, "zxqvnotarealword"), [])

    def test_discovery_navigation_and_search_use_the_same_markdown_read(self):
        from automation.engineering_context.discovery import build_discovery, search

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = root / "machine-readable/catalog.yaml"
            catalog.parent.mkdir()
            source = root / "docs/current.MD"
            source.parent.mkdir()
            first = "# Copperkestrel title\n\n[Old target](earlier.md#old)\n"
            second = "# Silvermagpie title\n\n[New target](later.md#new)\n"
            source.write_text(first, encoding="utf-8")
            records = ["documents:\n"]
            for uid, doc in (("doc-current", source), ("doc-earlier", source.with_name("earlier.md")),
                             ("doc-later", source.with_name("later.md"))):
                if doc != source:
                    doc.write_text(f"# {uid}\n", encoding="utf-8")
                records.append(f"  - id: {uid}\n    kind: entrypoint\n    path: {doc.relative_to(root).as_posix()}\n"
                               "    status: active\n    applies_to: [all]\n")
            catalog.write_text("".join(records), encoding="utf-8")
            stable = build_discovery(root)

            original = Path.read_text
            reads = []

            def read_and_replace(path, *args, **kwargs):
                text = original(path, *args, **kwargs)
                if path == source:
                    reads.append(text)
                    if len(reads) == 1:
                        replacement = source.with_name("replacement.txt")
                        replacement.write_text(second, encoding="utf-8")
                        replacement.replace(source)
                return text

            with patch.object(Path, "read_text", read_and_replace):
                captured = build_discovery(root)
            self.assertEqual(reads, [first])
            self.assertEqual(captured, stable)
            self.assertEqual(search(captured, "Copperkestrel")[0]["id"], "doc-current")
            self.assertEqual(captured["edges"], [{"from": "doc-current", "to": "doc-earlier", "type": "related"}])
            self.assertEqual(build_discovery(root)["edges"],
                             [{"from": "doc-current", "to": "doc-later", "type": "related"}])

    def test_frontmatter_identity_is_unique_across_governed_and_decision_markdown(self):
        for suffix in (".md", ".MD"):
            with self.subTest(suffix=suffix):
                self._check_frontmatter_identity_in_markdown(suffix)

    def _check_frontmatter_identity_in_markdown(self, suffix):
        import shutil
        import subprocess
        from automation.engineering_context.discovery import build_discovery, check_integrity
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "sources.yaml").write_text("sources:\n", encoding="utf-8")
            visual = "machine-readable/visual-directions.v1.json"
            (root / visual).write_text("{}", encoding="utf-8")
            bundle = root / "agent-config/codex/skills/engineering-handbook/bundle.json"
            bundle.parent.mkdir(parents=True)
            bundle.write_text(json.dumps({"schema_version": 1, "skill_name": "engineering-handbook",
                                          "include": [visual]}), encoding="utf-8")
            entries = (
                ("policy-fixture", "policy", f"policies/fixture{suffix}", "active",
                 "---\nid: policy-fixture\nkind: policy\nstatus: superseded\nstatus: active\nowner: engineering\n"
                 "version: 1\napplies_to:\n  - all\nsources: []\nsources: []\nlast_verified: 2026-11-21\n"
                 f"review_due: 2027-02-21\n---\n# Policy\n\n[Legacy ADR](../decisions/legacy{suffix})\n"),
                ("legacy-adr", "decision", f"decisions/legacy{suffix}", "superseded",
                 "---\nstatus: superseded\n---\n# Legacy ADR\n"),
                ("entry-fixture", "entrypoint", "docs/ordinary.md", "active",
                 "---\nstatus: draft\nstatus: active\n---\n# Ordinary Markdown\n"),
            )
            catalog = ["documents:\n"]
            for uid, kind, relative, status, body in entries:
                path = root / relative
                path.parent.mkdir()
                path.write_text(body, encoding="utf-8")
                catalog.append(f"  - id: {uid}\n    kind: {kind}\n    path: {relative}\n"
                               f"    status: {status}\n    applies_to: [all]\n")
            (registry / "catalog.yaml").write_text("".join(catalog), encoding="utf-8")
            expected = ["duplicate-frontmatter-identity:policy-fixture:status", "invalid-source-references:policy-fixture"]
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertCountEqual(check_integrity(root), expected)
            with self.assertRaisesRegex(ValueError, expected[0]):
                build_discovery(root)
            with self.assertRaisesRegex(ValueError, expected[0]):
                compile_handbook(root, registry / "compiled")

            shell = shutil.which("pwsh") or shutil.which("powershell")
            if shell:
                script = Path("automation/handbook/check-integrity.ps1")
                (root / script.parent).mkdir(parents=True)
                shutil.copyfile(ROOT / script, root / script)
                check = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(root / script)],
                                       capture_output=True, text=True, timeout=30)
                self.assertEqual(check.returncode, 1, check.stdout + check.stderr)
                self.assertCountEqual([line[6:] for line in check.stdout.splitlines() if line.startswith("ERROR ")],
                                      expected)

            policy = root / entries[0][2]
            policy.write_text(entries[0][4].replace("status: superseded\n", "").replace("sources: []\n", "", 1),
                              encoding="utf-8")
            unit = {"id": "unit-source-fixture", "source": "policy-fixture", "force": "must", "type": "constraint",
                    "text": "Review this local fixture.", "activate_when": ["intent:review"],
                    "covers": [], "phase": ["planning"]}
            with policy.open("a", encoding="utf-8") as stream:
                stream.write("\n" + chr(96) * 3 + "json agent-context\n" + json.dumps({"units": [unit]})
                             + "\n" + chr(96) * 3 + "\n")
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertEqual(check_integrity(root), [])
            build = compile_handbook(root, registry / "compiled")
            self.assertIn("planning.json", build.changed_files)
            planning = json.loads((registry / "compiled/planning.json").read_text(encoding="utf-8"))
            self.assertEqual([row["id"] for row in planning["units"]], ["unit-source-fixture"])
            self.assertIn({"from": "policy-fixture", "to": "legacy-adr", "type": "related"},
                          build_discovery(root)["edges"])

            decision = root / entries[1][2]
            decision.write_text(entries[1][4].replace("status: superseded", "status: accepted\nstatus: superseded"),
                                encoding="utf-8")
            decision_problem = "duplicate-frontmatter-identity:legacy-adr:status"
            with patch("automation.engineering_context.discovery.load_visual_catalog"):
                self.assertEqual(check_integrity(root), [decision_problem])
            with self.assertRaisesRegex(ValueError, decision_problem):
                compile_handbook(root, registry / "compiled")


    def test_governed_prose_cannot_be_indexed_under_a_conflicting_catalog_identity(self):
        from automation.engineering_context.discovery import build_discovery, search
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry = root / "machine-readable"
            registry.mkdir()
            (registry / "catalog.yaml").write_text(
                "documents:\n  - id: pol-note\n    kind: policy\n    path: policies/note.MD\n"
                "    status: active\n    applies_to: [all]\n", encoding="utf-8")
            doc = root / "policies/note.MD"
            doc.parent.mkdir()
            prose = ("---\nid: pol-note\nkind: policy\nstatus: active\nowner: engineering\nversion: 1\n"
                     "applies_to: [all]\nsources: []\nlast_verified: 2026-11-21\nreview_due: 2027-02-21\n"
                     "---\n# Prose policy\n")
            doc.write_text(prose, encoding="utf-8")
            self.assertEqual(search(build_discovery(root), "pol-note")[0]["id"], "pol-note")
            quoted = prose.replace("id: pol-note", 'id: "pol-note"').replace("status: active", "status: 'active'  ")
            doc.write_text(quoted, encoding="utf-8")
            self.assertEqual(search(build_discovery(root), "pol-note")[0]["id"], "pol-note")
            for key, old, new in (("id", "pol-note", "pol-other"), ("kind", "policy", "reference"),
                                  ("status", "active", "superseded"), ("id", "pol-note", '"pol-other"'),
                                  ("kind", "policy", "'reference'"), ("status", "active", "active'")):
                with self.subTest(key=key):
                    doc.write_text(prose.replace(f"{key}: {old}", f"{key}: {new}", 1), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, f"metadata mismatch: pol-note:{key}"):
                        compile_handbook(root, registry / "compiled")

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

    def test_list_fence_keeps_later_navigation_without_reviving_earlier_standalone_examples(self):
        from automation.engineering_context.discovery import build_discovery

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "references").mkdir()
            (root / "machine-readable").mkdir()
            names = ("owner", "visible", "sample", "metadata")
            catalog = ["documents:"]
            for name in names:
                path = f"references/{name}.md"
                catalog.extend((f"  - id: ref-{name}", "    kind: reference", f"    path: {path}",
                                "    status: active", "    applies_to: [fixture]"))
                (root / path).write_text(f"# {name}\n", encoding="utf-8")
            (root / "machine-readable/catalog.yaml").write_text("\n".join(catalog), encoding="utf-8")
            owner = root / "references/owner.md"
            header = "---\nid: ref-owner\nnote: '[Metadata](metadata.md)'\n---\n"
            example = "```text\n[Earlier example](sample.md)\n```\n"
            separate_section = "- Ordinary item.\n\n## New section\n\n  ~~~text\n  [Example](sample.md)\n  ~~~\n"
            for list_example in ("- ```text\n  sample\n  ```\n", "1. Notes\n\n   ~~~text\n   sample\n", separate_section):
                with self.subTest(list_example=list_example):
                    owner.write_text(header + example + list_example + "\n[Visible](visible.md)\n", encoding="utf-8")
                    index = build_discovery(root)
                    related = {edge["to"] for edge in index["edges"] if edge["from"] == "ref-owner" and edge["type"] == "related"}
                    self.assertEqual(related, {"ref-visible"})

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

    def test_discovery_emits_related_links_from_prose_outside_supported_fences(self):
        from automation.engineering_context.discovery import build_discovery

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "standards").mkdir()
            (root / "references").mkdir()
            (root / "machine-readable").mkdir()
            owner, linked, alias, sample = "std-links", "ref-linked", "ref-alias", "ref-example"
            docs = ((owner, "standard", "standards/links.md"), (linked, "reference", "references/linked.md"),
                    (alias, "reference", "references/alias.md"), (sample, "reference", "references/example.md"))
            catalog = ["documents:\n"]
            for uid, kind, path in docs:
                catalog.append(
                    f"  - id: {uid}\n    kind: {kind}\n    path: {path}\n    status: active\n    applies_to: [all]\n"
                )
                (root / path).write_text(f"---\nid: {uid}\nkind: {kind}\nstatus: active\n---\n# Fixture\n", encoding="utf-8")
            (root / "machine-readable/catalog.yaml").write_text("".join(catalog), encoding="utf-8")
            path = root / "standards/links.md"
            path.write_text(path.read_text(encoding="utf-8") + (
                "\n[Real link](../references/linked.md#section)\n"
                "\n```text\n[Example](../references/example.md)\n```\n"
                "\n~~~markdown\n[Example](../references/example.md)\n~~~\n"
                "\n````markdown\n```text\nshort fence\n```\n"
                "[Still fenced](../references/example.md)\n````\n"
                "\n[Alias](../references/./alias.md#section)\n"
            ), encoding="utf-8")
            index = build_discovery(root, {
                "fixture-child": {"source": owner, "requires": ["fixture-parent"]},
                "fixture-parent": {"source": owner},
            })
            self.assertEqual({edge["to"] for edge in index["edges"] if edge["from"] == owner and
                              edge["type"] == "related"}, {linked, alias})
            self.assertIn({"from": "unit:fixture-child", "to": "unit:fixture-parent", "type": "requires"}, index["edges"])
            excerpt = next(doc["excerpt"] for doc in index["documents"] if doc["id"] == owner)
            self.assertNotIn("example.md", excerpt)

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

    def test_supersession_graph_accepts_deep_lineage_and_identifies_a_cycle(self):
        from automation.engineering_context.discovery import validate_edges

        lineage = [f"ref-version-{i:04d}" for i in range(1150)]
        edges = [
            {"from": current, "to": previous, "type": "supersedes"}
            for current, previous in zip(lineage, lineage[1:])
        ]
        validate_edges(set(lineage), edges)
        edges.append({"from": lineage[-1], "to": lineage[0], "type": "supersedes"})
        with self.assertRaisesRegex(ValueError, "cyclic supersedes dependency: ref-version-0000"):
            validate_edges(set(lineage), edges)


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
