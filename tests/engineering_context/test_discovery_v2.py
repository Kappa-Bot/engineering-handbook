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


class KnowledgeDiscoveryTests(unittest.TestCase):
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

    def test_canonical_integrity_includes_paths_metadata_and_sources(self):
        from automation.engineering_context.discovery import check_integrity
        self.assertEqual(check_integrity(ROOT), [])
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "machine-readable").mkdir()
            (root / "machine-readable/catalog.yaml").write_text("version: 1\ndocuments:\n  - id: missing\n    kind: policy\n    path: policies/missing.md\n    status: active\n    applies_to: [all]\n")
            (root / "machine-readable/sources.yaml").write_text("sources:\n")
            self.assertTrue(any("missing" in issue for issue in check_integrity(root)))

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

    def test_adaptive_budget_never_claims_unmatched_task_is_safe(self):
        from automation.engineering_context.context_solver import budget_for, assessment_status
        simple = describe_task("Correct a typo", EMPTY)
        risky = describe_task("Migra datos y cambia permisos y secretos en producción", EMPTY)
        self.assertGreater(budget_for(risky).hard_max, budget_for(simple).hard_max)
        self.assertEqual(assessment_status(simple), "needs-discovery")


if __name__ == "__main__":
    unittest.main()
