"""User-visible catalog selection contracts, independent of visual prose."""
from __future__ import annotations

from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


class VisualDirectionCatalogTests(unittest.TestCase):
    def test_internal_default_can_be_overridden_by_local_and_task_choices(self):
        from automation.engineering_context.visual_directions import resolve_visual_direction

        cases = (
            ("internal-console", None, None, "glassmorphism", "default"),
            ("internal-console", None, "neumorphism", "neumorphism", "local-design"),
            ("internal-console", "solid-editorial", "neumorphism", "solid-editorial", "explicit-task"),
            ("internal-console", "neumorphism", None, "neumorphism", "explicit-task"),
            ("public-site", None, None, None, "product-owned"),
            ("field", None, None, None, "product-owned"),
            ("self-service", None, None, None, "product-owned"),
            ("clinical-data", None, None, None, "product-owned"),
            ("public-site", "glassmorphism", None, "glassmorphism", "explicit-task"),
        )
        for surface, task_style, local_style, want, source in cases:
            with self.subTest(surface=surface, task=task_style, local=local_style):
                result = resolve_visual_direction(ROOT, surface, task_style, local_style)
                self.assertEqual(result["selected"], want)
                self.assertEqual(result["source"], source)
                self.assertFalse(result["authorizes_ui_change"])
                if want:
                    self.assertTrue((ROOT / result["reference"]).is_file())
        with self.assertRaises(ValueError):
            resolve_visual_direction(ROOT, "internal-console", "unknown-future-theme")
        with self.assertRaises(ValueError):
            resolve_visual_direction(ROOT, "internal-console", "glassmorphism", "unknown-local-style")

    def test_catalog_is_extensible_but_rejects_ambiguous_or_unsafe_entries(self):
        from automation.engineering_context.visual_directions import load_visual_catalog, resolve_visual_direction

        original = load_visual_catalog(ROOT)
        self.assertEqual(original["schema"], "melodiq-visual-directions/v1")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "machine-readable/visual-directions.v1.json"
            path.parent.mkdir(parents=True)
            for item in original["directions"]:
                target = root / item["reference"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# fixture")
            future = root / "patterns/future-material.md"
            future.write_text("# future")
            for case in ("duplicate-id", "duplicate-alias", "blank-normalized-alias", "bad-reference", "bad-default", "missing-reference", "future-valid"):
                data = copy.deepcopy(original)
                if case == "duplicate-id":
                    data["directions"].append(copy.deepcopy(data["directions"][0]))
                elif case == "duplicate-alias":
                    data["directions"][1]["aliases"].append(data["directions"][0]["aliases"][0])
                elif case == "blank-normalized-alias":
                    data["directions"][1]["aliases"].append("\u0301")
                elif case == "bad-reference":
                    data["directions"][0]["reference"] = "../outside.md"
                elif case == "bad-default":
                    data["default_by_surface"]["internal-console"] = "retired-style"
                elif case == "missing-reference":
                    data["directions"][0]["reference"] = "patterns/missing.md"
                else:
                    data["directions"].append({"id": "future-material", "title": "Future", "aliases": ["future material"], "reference": "patterns/future-material.md", "status": "active", "best_for": ["a justified future use"], "avoid": ["unverified blanket adoption"]})
                path.write_text(json.dumps(data), encoding="utf-8")
                with self.subTest(case=case):
                    if case == "future-valid":
                        self.assertEqual(resolve_visual_direction(root, "internal-console", "future-material")["selected"], "future-material")
                    else:
                        with self.assertRaises(ValueError):
                            load_visual_catalog(root)

    def test_mentions_follow_aliases_and_do_not_treat_rejected_styles_as_choices(self):
        from automation.engineering_context.visual_directions import detect_visual_styles

        cases = (
            ("Aplica glassmorphism a la consola", ("glassmorphism",)),
            ("Usa neumorfismo para la interfaz", ("neumorphism",)),
            ("Use neomorphism in the admin UI", ("neumorphism",)),
            ("No uses glassmorphism; aplica neumorphism", ("neumorphism",)),
            ("Do not apply glassmorphism, use neumorphism", ("neumorphism",)),
            ("No quiero glassmorphism, prefiero neumorphism", ("neumorphism",)),
            ("No uses glassmorphism y usa neumorfismo en la consola interna", ("neumorphism",)),
            ("Avoid glassmorphism and use neomorphism in the console", ("neumorphism",)),
            ("Compara glassmorphism y neumorphism", ("glassmorphism", "neumorphism")),
            ("Glassmorphism no, prefiero neumorphism", ("neumorphism",)),
            ("Prefiero neumorphism frente a glassmorphism", ("neumorphism",)),
            ("Apply neumorphism instead of glassmorphism", ("neumorphism",)),
            ("Explica el concepto sin elegir estilo", ()),
        )
        for query, want in cases:
            with self.subTest(query=query):
                self.assertEqual(detect_visual_styles(query), want)

    def test_context_uses_the_selected_verified_visual_catalog_once(self):
        from automation.engineering_context import cli, visual_directions
        from automation.engineering_context.handbook_compile import compile_handbook

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            visual_path = root / visual_directions.CATALOG_PATH
            visual_path.parent.mkdir()
            (visual_path.parent / "catalog.yaml").write_text(
                "documents:\n  - id: visual-fixture\n    kind: registry\n"
                "    path: machine-readable/visual-directions.v1.json\n"
                "    status: active\n    applies_to: [all]\n", encoding="utf-8"
            )
            catalog = visual_directions.load_visual_catalog(ROOT)
            for item in catalog["directions"]:
                path = root / item["reference"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Fixture\n", encoding="utf-8")
            visual_path.write_text(json.dumps(catalog), encoding="utf-8")
            compiled = visual_path.parent / "compiled"
            compile_handbook(root, compiled)
            index = json.loads((compiled / "discovery.json").read_text(encoding="utf-8"))
            old_hash = index["documents"][0]["source_hash"]

            alias = "lucent f\u00edxture finish"
            next(item for item in catalog["directions"] if item["id"] == "glassmorphism")["aliases"].append(f"\u202f{alias}\u2003")
            visual_path.write_text(json.dumps(catalog), encoding="utf-8")
            args = ["context", "--repo", str(root), "--handbook", str(compiled), "--mode", "verify",
                    "--task", f"Apply {alias} to the internal workspace."]
            with self.assertRaisesRegex(RuntimeError, "compiled handbook context is stale"):
                cli.main(args)
            with self.assertRaisesRegex(ValueError, "differs from the verified discovery index"):
                visual_directions.load_visual_catalog(root, expected_source_hash=old_hash)
            compile_handbook(root, compiled)
            self.assertEqual(visual_directions.resolve_visual_direction(root, "internal-console", alias)["selected"], "glassmorphism")
            self.assertEqual(visual_directions.resolve_visual_direction(root, "internal-console", local_style=alias)["source"], "local-design")
            output = io.StringIO()
            with (
                patch.object(cli, "load_visual_catalog", wraps=visual_directions.load_visual_catalog) as loaded,
                patch.object(visual_directions, "load_visual_catalog", side_effect=AssertionError("ambient catalog read")),
                redirect_stdout(output),
            ):
                self.assertEqual(cli.main(args), 0)
                loaded.assert_called_once()
            descriptor = json.loads(output.getvalue())["descriptor"]
            self.assertIn("operator-glass-material-change", descriptor["archetypes"])

    def test_declared_visual_catalog_requires_compiled_source_binding(self):
        from automation.engineering_context import cli

        entry = {"path": cli.VISUAL_CATALOG_PATH.as_posix()}
        for field in ({}, {"source_hash": None}, {"source_hash": ""}, {"source_hash": "unsigned"}):
            with self.subTest(field=field), patch.object(cli, "load_visual_catalog") as loader:
                with self.assertRaisesRegex(RuntimeError, "Recompile the selected Handbook"):
                    cli._selected_visual_catalog(ROOT, {"documents": [{**entry, **field}]})
                loader.assert_not_called()
        self.assertIsNone(cli._selected_visual_catalog(ROOT, {"documents": []}))

    def test_visual_catalog_cli_lists_and_resolves_without_mutating_product_ui(self):
        from automation.engineering_context.cli import main

        def run(*args):
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["visual-directions", "--root", str(ROOT), *args])
            self.assertEqual(code, 0)
            return json.loads(output.getvalue())

        listing = run()
        self.assertEqual({item["id"] for item in listing["directions"]}, {"glassmorphism", "neumorphism", "solid-editorial"})
        resolved = run("--surface", "internal-console", "--local-style", "neumorphism")
        self.assertEqual(resolved["selected"], "neumorphism")
        self.assertEqual(resolved["source"], "local-design")
        self.assertFalse(resolved["authorizes_ui_change"])
        self.assertEqual(run("--surface", "internal-console", "--style", "neumorfismo")["selected"], "neumorphism")

    def test_operator_direction_routing_defaults_and_explicit_choices(self):
        from automation.engineering_context.task_descriptor import describe_task

        profile = {"detected": {"capabilities": {}}}
        for task in (
            "Rediseña el dashboard interno de MelodIQ Core",
            "Design a new ChurchOS operator console",
            "Diseña una nueva consola administrativa",
            "Mejora el diseño visual de la consola Ops OS",
        ):
            with self.subTest(task=task):
                result = describe_task(task, profile)
                self.assertIn("operator-visual-direction-choice", result.archetypes)
                self.assertIn("visual-direction-choice", result.archetypes)
                self.assertNotIn("operator-glass-material-change", result.archetypes)

        for task, expected, excluded in (
            ("Aplica glassmorphism a la consola interna", "operator-glass-material-change", "operator-neumorphic-material-change"),
            ("Aplica neumorfismo a la consola interna", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("No uses glassmorphism; aplica neumorphism a la consola interna", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("Use soft UI for the admin dashboard", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("I prefer neumorphism for the admin console", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("I want glassmorphism for the internal dashboard", "operator-glass-material-change", "operator-neumorphic-material-change"),
            ("Please switch the admin UI to neumorphism", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("Set the internal console to glassmorphism", "operator-glass-material-change", "operator-neumorphic-material-change"),
            ("Cambia la consola interna a neumorphism", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("Nuevo dashboard interno de MelodIQ Core con neumorphism", "operator-neumorphic-material-change", "operator-glass-material-change"),
            ("Aplica solid-editorial a la consola interna", "operator-visual-direction-choice", "operator-glass-material-change"),
        ):
            with self.subTest(task=task):
                result = describe_task(task, profile)
                self.assertIn(expected, result.archetypes)
                self.assertNotIn(excluded, result.archetypes)
                self.assertIn("operator-visual-direction-choice", result.archetypes)

    def test_visual_routing_does_not_bleed_into_unrelated_tasks(self):
        from automation.engineering_context.task_descriptor import describe_task

        profile = {"detected": {"capabilities": {}}}
        for task in (
            "Fix API in ChurchOS CRM",
            "Corrige una errata en el dashboard interno",
            "Implementa la sidebar de ChurchOS",
            "Explica neumorphism en la consola interna",
            "No rediseñes la consola interna",
            "Apply glassmorphism to a public marketing website",
            "Design a new public website for MelodIQ",
            "Review README documentation about glassmorphism for the internal console",
            "Review the README documenting glassmorphism implementation for the admin console",
            "Review DESIGN.md describing existing glassmorphism in ChurchOS",
            "Revisa la documentación de neumorfismo de MelodIQ Core",
            "Analyze README documentation about neumorphism for the internal console",
            "Evalúa la documentación sobre glassmorphism de MelodIQ Core",
            "Design the ChurchOS patient portal, not the internal console",
            "Design a ChurchOS patient portal in neumorphism",
            "Rediseña el portal para pacientes de DentalOS",
            "Create the DentalOS self-service app in neumorphism",
            "Design the MelodIQ Core field kiosk in glassmorphism",
            "Build a public member portal with glassmorphism in ChurchOS",
            "Design a ChurchOS customer-facing landing with glassmorphism",
            "Design a client-facing ChurchOS dashboard with neumorphism",
            "Diseña una pantalla de cita para pacientes de DentalOS con neumorfismo",
            "Create a ChurchOS donation page for members in glassmorphism",
        ):
            with self.subTest(task=task):
                result = describe_task(task, profile)
                self.assertNotIn("operator-visual-direction-choice", result.archetypes)
                self.assertNotIn("operator-neumorphic-material-change", result.archetypes)
                self.assertNotIn("operator-glass-material-change", result.archetypes)
                if any(term in task.lower() for term in ("patient", "pacientes", "self-service", "kiosk", "member portal")):
                    self.assertNotIn("operator-console-shell-change", result.archetypes)
        public = describe_task("Apply glassmorphism to a public marketing website", profile)
        self.assertIn("visual-direction-choice", public.archetypes)

        for switched in (
            "No uses glassmorphism y usa neumorfismo en la consola interna",
            "Avoid glassmorphism and use neomorphism in the admin console",
            "Review current glassmorphism in the console, then adopt neumorphism",
            "Audita el glassmorphism actual de la consola y aplica neumorfismo",
            "Compare glassmorphism with neumorphism for the admin console and then apply neumorphism",
            "Do not apply glassmorphism and apply neumorphism to the console",
        ):
            with self.subTest(switched=switched):
                descriptor = describe_task(switched, profile)
                self.assertIn("operator-neumorphic-material-change", descriptor.archetypes)
                self.assertNotIn("operator-glass-material-change", descriptor.archetypes)

        for undecided in (
            "Design a new internal console; review existing glassmorphism before choosing a material",
            "Rediseña la consola interna; audita el neumorfismo actual antes de decidir",
        ):
            with self.subTest(undecided=undecided):
                descriptor = describe_task(undecided, profile)
                self.assertIn("operator-visual-direction-choice", descriptor.archetypes)
                self.assertNotIn("operator-glass-material-change", descriptor.archetypes)
                self.assertNotIn("operator-neumorphic-material-change", descriptor.archetypes)

        for audit in ("Audita glassmorphism en la consola interna", "Evalúa neumorfismo en el CRM interno"):
            with self.subTest(audit=audit):
                descriptor = describe_task(audit, profile)
                self.assertIn("operator-visual-direction-choice", descriptor.archetypes)
                self.assertNotIn("operator-glass-material-change", descriptor.archetypes)
                self.assertNotIn("operator-neumorphic-material-change", descriptor.archetypes)

        for scoped in (
            "Design a new ChurchOS internal console, not the patient portal",
            "Design an internal console and a patient portal for ChurchOS",
            "Rediseña la consola interna y el portal de pacientes de DentalOS",
        ):
            with self.subTest(scoped=scoped):
                descriptor = describe_task(scoped, profile)
                self.assertIn("operator-visual-direction-choice", descriptor.archetypes)
                self.assertNotIn("operator-glass-material-change", descriptor.archetypes)
                self.assertNotIn("operator-neumorphic-material-change", descriptor.archetypes)

        mixed = describe_task("Apply neumorphism to the ChurchOS patient portal; build a new internal console", profile)
        self.assertIn("operator-visual-direction-choice", mixed.archetypes)
        self.assertNotIn("operator-neumorphic-material-change", mixed.archetypes)

    def test_public_and_operator_materials_follow_their_own_clauses(self):
        from automation.engineering_context.task_descriptor import describe_task

        for task, operator_choice, material in (
            ("Apply neumorphism to the public marketing website; fix a typo in the internal console sidebar", False, None),
            ("Aplica neumorfismo a la web pública; corrige una errata en la barra lateral de la consola interna", False, None),
            ("Apply neumorphism to the public marketing site; build a new internal console", True, None),
            ("Aplica glassmorphism a la consola interna; corrige una errata en la web pública", True, "glass"),
            ("Use glassmorphism for the public website and the internal console", True, "glass"),
            ("Apply glassmorphism to the public website and neumorphism to the internal console", True, "neumorphic"),
            ("Aplica neumorfismo a la consola interna y glassmorphism a la web pública", True, "neumorphic"),
            ("Compare glassmorphism and neumorphism for the internal console; test the public website", True, None),
            ("Apply glassmorphism to the public website using the internal console as a reference", False, None),
            ("Aplica neumorfismo a la web pública y deja la consola interna sin cambios", False, None),
            ("Apply Neumorphism to the public website and build a new internal console.", True, None),
            ("Compare neumorphism and glassmorphism for the public website; apply glassmorphism to the internal dashboard.", True, "glass"),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, {})
                self.assertIn("visual-direction-choice", descriptor.archetypes)
                self.assertEqual("operator-visual-direction-choice" in descriptor.archetypes, operator_choice)
                for style in ("glass", "neumorphic"):
                    self.assertEqual(f"operator-{style}-material-change" in descriptor.archetypes, material == style)

    def test_shell_component_work_preserves_shell_without_console_material_default(self):
        from automation.engineering_context.task_descriptor import describe_task

        for task, expect_direction in (
            ("Implement the internal console sidebar", False),
            ("Design the internal console's sidebar", False),
            ("Implementa un menú lateral para la consola interna", False),
            ("Implement the internal dashboard header", False),
            ("Implement a theme toggle for the internal console", False),
            ("Implementa un selector de tema para la consola interna", False),
            ("Build a new internal console with a theme toggle", True),
            ("Build a new internal console with a sidebar", True),
            ("Diseña una consola interna nueva con barra lateral", True),
            ("Implement the internal console sidebar; build a new internal console", True),
            ("Apply glassmorphism to the internal console sidebar", True),
        ):
            with self.subTest(task=task):
                result = describe_task(task, {})
                self.assertIn("operator-console-shell-change", result.archetypes)
                self.assertEqual("operator-visual-direction-choice" in result.archetypes, expect_direction)

    def test_material_comparison_requests_selection_not_simultaneous_adoption(self):
        from automation.engineering_context.task_descriptor import describe_task
        from automation.engineering_context.discovery_rules import positive_text

        self.assertIn("apply neumorphism", positive_text("Do not apply glassmorphism and apply neumorphism to the console").lower())

        descriptor = describe_task("Compara glassmorphism y neumorphism para la consola interna", {"detected": {"capabilities": {}}})
        self.assertIn("visual-direction-choice", descriptor.archetypes)
        self.assertIn("operator-visual-direction-choice", descriptor.archetypes)
        self.assertNotIn("operator-glass-material-change", descriptor.archetypes)
        self.assertNotIn("operator-neumorphic-material-change", descriptor.archetypes)

    def test_context_search_and_distribution_retain_material_owners(self):
        from automation.engineering_context.context_solver import solve_context
        from automation.engineering_context.discovery import search, check_integrity
        from automation.engineering_context.task_descriptor import describe_task

        profile = {"detected": {"capabilities": {}}}
        compiled = ROOT / "machine-readable/compiled"
        routing = json.loads((compiled / "routing.json").read_text(encoding="utf-8"))
        for task, expected in (
            ("Rediseña la consola de MelodIQ Core", ("visual-direction-selection-contract", "visual-direction-material-regression-gates")),
            ("Aplica glassmorphism al CRM interno", ("operator-glass-material-adoption-decision", "operator-glass-material-conditional-acceptance")),
            ("Aplica neumorphism a la consola interna", ("operator-neumorphic-material-decision", "operator-neumorphic-material-acceptance")),
        ):
            descriptor = describe_task(task, profile)
            for phase, expected_material in zip(("planning", "verification"), expected):
                with self.subTest(task=task, phase=phase):
                    view = json.loads((compiled / f"{phase}.json").read_text(encoding="utf-8"))
                    ids = {u["id"] for u in solve_context({"units": view["units"], "routing": routing}, descriptor, phase).units}
                    self.assertIn("visual-direction-" + ("selection-contract" if phase == "planning" else "material-regression-gates"), ids)
                    self.assertIn(expected_material, ids)
        index = json.loads((compiled / "discovery.json").read_text(encoding="utf-8"))
        found = search(index, "neumorfismo consola interna", limit=12)
        ids = {entry["id"] for entry in found}
        self.assertIn("pat-visual-direction-catalog", ids)
        self.assertIn("pat-operator-neumorphic-surface-material", ids)
        first_catalog_hit = search(index, "catálogo visual neumorphism", limit=4)[0]
        self.assertEqual(first_catalog_hit["id"], "pat-visual-direction-catalog")
        edge_set = {(edge["from"], edge["to"], edge["type"]) for edge in index["edges"]}
        self.assertIn(("topic:visual-directions", "pat-visual-direction-catalog", "contains"), edge_set)
        self.assertIn(("pat-visual-direction-catalog", "pat-operator-neumorphic-surface-material", "contains"), edge_set)
        bundle = json.loads((ROOT / "agent-config/codex/skills/engineering-handbook/bundle.json").read_text(encoding="utf-8"))
        self.assertIn("machine-readable/visual-directions.v1.json", bundle["include"])
        self.assertFalse(check_integrity(ROOT))

    def test_catalog_symlink_and_broken_distribution_are_rejected(self):
        from automation.engineering_context.visual_directions import load_visual_catalog
        from automation.engineering_context.discovery import require_visual_bundle

        data = (ROOT / "machine-readable/visual-directions.v1.json").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "catalog-outside.json"
            target.write_text(data, encoding="utf-8")
            link = root / "machine-readable/visual-directions.v1.json"
            link.parent.mkdir(parents=True)
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                load_visual_catalog(root)
        bundle_path = ROOT / "agent-config/codex/skills/engineering-handbook/bundle.json"
        original = json.loads(bundle_path.read_text(encoding="utf-8"))
        self.assertIsNone(require_visual_bundle(original))
        original["include"].remove("machine-readable/visual-directions.v1.json")
        with self.assertRaises(ValueError):
            require_visual_bundle(original)


if __name__ == "__main__":
    unittest.main()
