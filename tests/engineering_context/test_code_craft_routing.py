from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from automation.engineering_context.cli import _load_compiled
from automation.engineering_context.context_solver import build_repo_route, solve_context
from automation.engineering_context.discovery import build_discovery, knowledge_tree, search
from automation.engineering_context.discovery_rules import validate_registry
from automation.engineering_context.handbook_compile import compile_handbook
from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import describe_task


ROOT = Path(__file__).resolve().parents[2]
EMPTY = {"detected": {"capabilities": {}}}


class CodeCraftClassificationTests(unittest.TestCase):
    def test_code_authoring_and_maintenance_actions_are_discoverable(self):
        cases = (
            ("Implement a Python parsing function", {"code-change"}),
            ("Escribe una función para validar facturas", {"code-change"}),
            ("Refactor the billing module", {"code-change", "code-organization"}),
            ("Refactoriza el módulo de pagos", {"code-change", "code-organization"}),
            ("Rename the requestTimeout variable", {"code-change", "code-organization"}),
            ("Renombra la variable precioTotal", {"code-change", "code-organization"}),
            ("Reorganiza las carpetas de src para agrupar módulos", {"code-change", "code-organization"}),
            ("Clean up dead code in the API handler", {"code-change", "code-organization"}),
            ("Limpia el código duplicado del servidor", {"code-change", "code-organization"}),
            ("Repair the TypeScript source module", {"code-change"}),
            ("Fix API", {"code-change"}),
            ("Simplifica el código repetido del proyecto", {"code-change", "code-organization"}),
            ("Split the payment module into focused responsibilities", {"code-change", "code-organization"}),
            ("Extract the invoice function into a smaller module", {"code-change", "code-organization"}),
            ("Change the source code", {"code-change"}),
            ("Update the Python function", {"code-change"}),
            ("Modifica la función de cálculo", {"code-change"}),
            ("Reestructura el módulo de facturación", {"code-change", "code-organization"}),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertTrue(expected.issubset(descriptor.archetypes), task)
                self.assertIn("modify", descriptor.intent, task)

    def test_dependency_selection_is_not_implicit_install_authority(self):
        cases = (
            ("Choose a library for CSV parsing", False),
            ("Elige una librería para procesar imágenes", False),
            ("Evaluate dependencies for the new worker", False),
            ("Replace the installed npm package for image resizing", True),
            ("Sustituye la dependencia externa de PDF", True),
        )
        for task, mutation in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertIn("dependency-selection", descriptor.archetypes)
                self.assertEqual("modify" in descriptor.intent, mutation)

    def test_review_questions_and_negations_preserve_authorization_boundary(self):
        read_only = (
            "Review variable naming in the codebase",
            "Revisa el nombre de variables del código sin editar",
            "How should I organize source folders and modules?",
            "Do not refactor or rename the module",
            "No renombres variables ni reorganices el código",
            "Don't clean up the source code",
            "No escribas código ni refactorices los módulos",
            "Do not replace the package or refactor the module",
            "Do not refactor, rename or reorganize the source modules",
            "No refactorices, renombres ni reorganices los módulos",
            "¿Cómo puedo refactorizar el módulo y renombrar la variable?",
            "Review how to split the module and extract helpers without editing anything",
            "Review the plan to refactor and rename the module; do not edit",
        )
        for task in read_only:
            with self.subTest(task=task):
                self.assertNotIn("modify", describe_task(task, EMPTY).intent)
        for task in ("Do not refactor or rename the module", "No renombres variables ni reorganices el código",
                     "Don't clean up the source code", "No escribas código ni refactorices los módulos",
                     "Do not replace the package or refactor the module",
                     "Do not refactor, rename or reorganize the source modules",
                     "No refactorices, renombres ni reorganices los módulos"):
            with self.subTest(negative=task):
                self.assertNotIn("code-organization", describe_task(task, EMPTY).archetypes)
                self.assertNotIn("code-change", describe_task(task, EMPTY).archetypes)
        self.assertNotIn("dependency-selection", describe_task("Do not replace the package or refactor the module", EMPTY).archetypes)
        descriptor = describe_task("No refactorices; corrige la función de cálculo", EMPTY)
        self.assertIn("code-change", descriptor.archetypes)
        self.assertNotIn("code-organization", descriptor.archetypes)
        self.assertIn("modify", descriptor.intent)

    def test_code_and_document_actions_are_scoped_per_clause(self):
        cases = (
            ("Refactor the README code examples; fix the billing module", {"code-change"}),
            ("Fix the invoice function; rename the README", {"code-change"}),
            ("Review the README code examples", set()),
            ("Rename the variable in the README code sample", set()),
            ("Renombra la variable del ejemplo en la documentación", set()),
        )
        for task, want in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(set(descriptor.archetypes) & {"code-change", "code-organization"}, want)
                if task.startswith("Review"):
                    self.assertNotIn("modify", descriptor.intent)

    def test_non_code_prose_and_files_do_not_route_to_organization(self):
        non_code = (
            "Document variable naming conventions in the Handbook",
            "Refactor the README code examples",
            "Organiza los archivos de fotos en Descargas",
            "Rename the CSS class for the button",
            "Clean up the marketing copy",
            "Elige el nombre de marca de la empresa",
            "Review the Python documentation",
            "Review API documentation",
            "Update the README code examples",
            "Review the documentation about dependency versions",
            "Rename the folder for family pictures",
            "Reorganiza las carpetas de mi escritorio",
        )
        for task in non_code:
            with self.subTest(task=task):
                self.assertNotIn("code-organization", describe_task(task, EMPTY).archetypes)
        self.assertNotIn("dependency-selection", describe_task("Review the documentation about dependency versions", EMPTY).archetypes)

    def test_real_source_paths_route_but_examples_and_vendor_do_not(self):
        for path in (
            "src/core/parser.py", "apps/api/src/handlers/billing.ts", "lib/queue.go",
            "src/components/checkout.tsx", "tests/test_invoice.py", "src/domain/service.rs",
            "src/ui/selector.vue", "src/styles/forms.css", "src/query/report.sql",
            "src/index.mjs",
        ):
            with self.subTest(path=path):
                descriptor = describe_task("Repair the affected behavior", EMPTY, (path,))
                self.assertIn("code-change", descriptor.archetypes)
        for path in (
            "docs/examples/parser.py", "node_modules/foo/index.js", ".next/server/chunk.js",
            "dist/worker.ts", "src/generated/client.ts", "src/types/generated.d.ts",
            "vendor/foo/billing.go", "README.md", "tests/fixtures/example.py",
            "docs/examples/form.html", "src/ui/generated/client.vue",
            "src/types/foo.d.ts", "src/__fixtures__/a.ts",
        ):
            with self.subTest(excluded=path):
                descriptor = describe_task("Review the changed file", EMPTY, (path,))
                self.assertNotIn("code-change", descriptor.archetypes)

    def test_package_manifests_route_without_guessing_language(self):
        for path in ("package.json", "apps/api/pyproject.toml", "Cargo.toml", "go.mod", "Gemfile", "pom.xml"):
            with self.subTest(path=path):
                descriptor = describe_task("Review the changed file", EMPTY, (path,))
                self.assertIn("dependency-selection", descriptor.archetypes)
                self.assertNotIn("modify", descriptor.intent)
        for path in ("generated/package.json", "docs/package.json", "vendor/foo/Cargo.toml", "tests/fixtures/pyproject.toml"):
            with self.subTest(excluded=path):
                descriptor = describe_task("Review the changed file", EMPTY, (path,))
                self.assertNotIn("dependency-selection", descriptor.archetypes)

    def test_routes_resolve_existing_code_and_package_owners_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ("src/billing/invoice.py", "tests/test_invoice.py", "pyproject.toml"):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# fixture\n", encoding="utf-8")
            profile = profile_repo(root)
            for task, expected_labels in (
                ("Refactor the billing module", ("source-owner", "nearest-tests")),
                ("Choose a library for the parser", ("dependency-manifest", "source-owner")),
            ):
                with self.subTest(task=task):
                    route = build_repo_route(profile, describe_task(task, profile))
                    for label in expected_labels:
                        self.assertIn(label, route["inspect_first"])
                        self.assertTrue(route["resolved"][label], label)
            self.assertIn("src/billing/invoice.py", profile["detected"]["landmarks"]["source-owner"])
            self.assertIn("pyproject.toml", profile["detected"]["landmarks"]["dependency-manifest"])

    def test_source_and_manifest_landmarks_exclude_disguised_decoys(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            names = (
                "src/index.mjs", "src/types/foo.d.ts", "src/__fixtures__/a.ts",
                "src/generated/client.ts", "docs/package.json", "vendor/foo/Cargo.toml",
                "generated/package.json", "tests/fixtures/pyproject.toml", "src/package.json",
                "tests/test_invoice.py", "pyproject.toml",
            )
            for name in names:
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("fixture", encoding="utf-8")
            profile = profile_repo(root)
            code_paths = set(profile["detected"]["landmarks"]["source-owner"])
            package_paths = set(profile["detected"]["landmarks"]["dependency-manifest"])
            self.assertIn("src/index.mjs", code_paths)
            self.assertEqual({"src/index.mjs"}, code_paths)
            self.assertEqual({"src/package.json", "pyproject.toml"}, package_paths)
            code_route = build_repo_route(profile, describe_task("Refactor the module", profile))
            dependency_route = build_repo_route(profile, describe_task("Choose a library for CSV", profile))
            self.assertEqual(["src/index.mjs"], code_route["resolved"]["source-owner"])
            self.assertEqual(["pyproject.toml", "src/package.json"], dependency_route["resolved"]["dependency-manifest"])

    def test_clause_scope_cannot_mix_in_a_different_path_or_unknown_mode(self):
        for mode, condition in (
            ("clause", {"all": [{"text": "code"}, {"path": "package\\.json"}]}),
            ("unknown", {"text": "code"}),
        ):
            with self.subTest(scope=mode):
                with self.assertRaises(ValueError):
                    validate_registry({"schema": "discovery-rules/v1", "rules": [
                        {"id": "invalid", "scope": mode, "when": condition, "emit": ["archetype:code-change"]}
                    ]})


class CodeCraftContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.compiled = Path(cls._tmp.name)
        compile_handbook(ROOT, cls.compiled)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def selected(self, task, phase):
        descriptor = describe_task(task, EMPTY)
        capsule = solve_context(_load_compiled(self.compiled, phase), descriptor, phase)
        return {unit["id"] for unit in capsule.units}, capsule

    def test_code_tasks_receive_contract_implementation_and_verification_by_phase(self):
        cases = (
            ("Implement a Python parsing function", "planning", "code-task-owner-and-contract"),
            ("Escribe una función para validar facturas", "implementation", "code-craft-implementation"),
            ("Repair the TypeScript source module", "verification", "code-craft-verification"),
            ("Refactor the billing module", "implementation", "code-organization-safety"),
            ("Renombra la variable precioTotal", "verification", "code-organization-safety"),
        )
        for task, phase, expected in cases:
            with self.subTest(task=task, phase=phase):
                selected, capsule = self.selected(task, phase)
                self.assertIn(expected, selected)
                self.assertFalse(capsule.uncovered)
                self.assertLessEqual(capsule.estimated_tokens, capsule.budget.soft_max)

    def test_dependency_decisions_receive_existing_supply_chain_owner(self):
        for task in ("Choose a library for CSV parsing", "Elige una librería para procesar imágenes",
                     "Replace the installed npm package for image resizing"):
            for phase in ("planning", "implementation", "verification"):
                with self.subTest(task=task, phase=phase):
                    selected, capsule = self.selected(task, phase)
                    self.assertIn("dependency-choice-review", selected)
                    self.assertIn("std-dependency-supply-chain-baseline", capsule.provenance)
                    self.assertFalse(capsule.uncovered)

    def test_prose_and_unauthorized_renames_do_not_inherit_code_contract(self):
        for task in ("Write the marketing copy", "Review the README", "Document variable naming conventions in the Handbook",
                     "Do not refactor or rename the module", "Rename the CSS class for the button"):
            with self.subTest(task=task):
                selected, _ = self.selected(task, "implementation")
                self.assertNotIn("code-organization-safety", selected)
                if task != "Rename the CSS class for the button":
                    self.assertNotIn("code-craft-implementation", selected)

    def test_mixed_docs_and_code_request_selects_only_the_code_owners(self):
        for task, organization in (
            ("Refactor the README code examples; fix the billing module", False),
            ("Fix the invoice function; rename the README", False),
            ("Renombra la variable del módulo; documenta el ejemplo en README", True),
        ):
            with self.subTest(task=task):
                units, capsule = self.selected(task, "implementation")
                self.assertIn("code-craft-implementation", units)
                self.assertEqual("code-organization-safety" in units, organization)
                self.assertFalse(capsule.uncovered)
        units, _ = self.selected("Review the README code examples", "implementation")
        self.assertNotIn("code-craft-implementation", units)


class CodeCraftDiscoveryTests(unittest.TestCase):
    def test_spanish_and_english_code_guidance_resolve_to_canonical_sources(self):
        index = build_discovery(ROOT)
        for task, expected in (
            ("renombrar variables refactorizar carpetas código", "std-code-quality-organization-baseline"),
            ("code change workflow folder organization", "pb-code-change-workflow"),
        ):
            with self.subTest(task=task):
                hits = search(index, task, limit=10)
                self.assertIn(expected, {hit["id"] for hit in hits})
        knowledge = knowledge_tree(index)
        code = [topic for topic in knowledge["children"] if topic["id"] == "code-craft"]
        self.assertEqual(len(code), 1)
        self.assertEqual({"std-code-quality-organization-baseline", "pb-code-change-workflow"},
                         {child["id"] for child in code[0]["children"]})

    def test_installed_bundle_exposes_canonical_coding_guidance(self):
        with tempfile.TemporaryDirectory() as td:
            result = subprocess.run([
                sys.executable, "-I", str(ROOT / "automation/codex/handbook_update.py"),
                "bundle", "--source", str(ROOT), "--skills-home", td,
            ], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = Path(td) / "engineering-handbook/references"
            for path in ("standards/code-quality-organization-baseline.md", "playbooks/code-change-workflow.md"):
                self.assertTrue((installed / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
