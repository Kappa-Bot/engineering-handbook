import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from automation.engineering_context.cli import _load_compiled
from automation.engineering_context.context_solver import DEFAULT_BUDGET, build_repo_route, solve_context
from automation.engineering_context.task_descriptor import describe_task


ROOT = Path(__file__).resolve().parents[2]
COMPILED = ROOT / "machine-readable/compiled"
PHASES = ("planning", "implementation", "verification")
PROFILE = {"detected": {"capabilities": {"frontend": True, "persistence": True, "auth": True}}}


class ModernWebLeanGuidanceTests(unittest.TestCase):
    def capsules(self, task, changed=()):
        descriptor = describe_task(task, PROFILE, changed)
        return descriptor, [solve_context(_load_compiled(COMPILED, phase), descriptor, phase) for phase in PHASES]

    def assert_route(self, task, archetype, unit, *, changed=()):
        descriptor, capsules = self.capsules(task, changed)
        self.assertIn(archetype, descriptor.archetypes, task)
        for phase, capsule in zip(PHASES, capsules):
            with self.subTest(task=task, changed=changed, phase=phase):
                self.assertIn(unit, {item["id"] for item in capsule.units})
                self.assertFalse(capsule.uncovered)
                self.assertLessEqual(capsule.estimated_tokens, DEFAULT_BUDGET.soft_max)
        return descriptor, capsules

    def test_browser_behavior_routes_native_compatibility_in_each_phase(self):
        for task in (
            "Replace the React dialog with a native accessible dialog.",
            "Corrige el formulario: Enter durante composición IME no debe enviarlo.",
            "Optimiza el INP y los skeletons de la tabla del CRM.",
            "Implement responsive CSS container queries with fallback.",
            "Audit browser HTML streaming compatibility, do not edit.",
            "Revisa los popovers y el foco en Firefox y Safari.",
            "Improve client-side image priority for LCP.",
            "Refactor the React hooks for sorting the table.",
            "Corrige la validación del formulario y sus errores accesibles.",
            "Fix the SQL query; implement a responsive React table.",
            "Fix hydration mismatch in React server components.",
            "Repair keyboard focus in a modal and tooltip.",
            "Fix a typo and implement CSS scroll animations.",
        ):
            with self.subTest(task=task):
                self.assert_route(task, "web-platform-change", "web-platform-compatibility")

    def test_changed_browser_sources_route_without_guessing_from_repo_stack(self):
        for path in ("src/components/Table.tsx", "app/contacts/page.tsx", "src/styles/forms.css", "src/client/dialog.ts", "src/views/Intake.vue", r"apps\web\src\components\Dialog.jsx"):
            with self.subTest(path=path):
                self.assert_route("Repair the affected behavior", "web-platform-change", "web-platform-compatibility", changed=(path,))

    def test_using_a_named_method_is_not_changing_its_runtime(self):
        for task in (
            "Actualiza el formulario de React con Modern Web Guidance",
            "Apply Modern Web Guidance to React hooks",
            "Update the CSS guided by Modern Web Guidance",
            "Refactor React hooks with Ponytail",
        ):
            with self.subTest(task=task):
                descriptor, _ = self.assert_route(task, "web-platform-change", "web-platform-compatibility")
                self.assertNotIn("agent-execution", descriptor.risks)
                self.assertNotIn("agent-tooling-change", descriptor.archetypes)

    def test_native_primitives_and_coordinated_tasks_keep_the_browser_owner(self):
        for task in (
            "Replace the custom disclosure with <details> and <summary>",
            "Usa <details> y <summary> para el acordeón accesible",
            "Replace the custom select with <select> and preserve keyboard focus",
            "Usa <select> y conserva el foco y el teclado",
            "Corrige el SQL y añade un formulario",
            "Fix SQL and add a native HTML form",
            "Review the React dialog against the documentation",
            "Corrige una errata y añade un formulario accesible",
        ):
            with self.subTest(task=task):
                self.assert_route(task, "web-platform-change", "web-platform-compatibility")

    def test_explicit_backend_owner_wins_over_html_or_form_vocabulary(self):
        for task in (
            "Fix the HTML sanitizer on the server",
            "Simplify the form validation code on the backend",
            "Corrige la validación del formulario en el servidor",
            "Fix server-side HTML escaping for the React form",
        ):
            with self.subTest(task=task):
                self.assertNotIn("web-platform-change", describe_task(task, PROFILE).archetypes)

    def test_visual_compound_words_retain_accessibility_without_ui_substrings(self):
        for task in ("Corrige los fallos visuales del CRM", "Fix screenreader announcements", "Handle fullscreen exit", "Audit visually hidden labels"):
            descriptor, capsules = self.capsules(task)
            with self.subTest(task=task):
                self.assertIn("frontend", descriptor.surfaces)
                self.assertIn("accessibility", descriptor.risks)
                for capsule in capsules:
                    self.assertIn("ui-accessibility-baseline", {item["id"] for item in capsule.units})

    def test_path_only_guidance_preserves_structural_evidence(self):
        descriptor = describe_task("Repair the affected behavior", PROFILE, ("src/components/Table.tsx",))
        self.assertFalse(any(item["source"] == "text-signal" and item["value"] == "web-platform-change" for item in descriptor.evidence))
        self.assertTrue(any(item["source"] == "change-structure" and item["value"] == "src/components/Table.tsx" for item in descriptor.evidence))

    def test_backend_docs_copy_and_generated_paths_do_not_trigger_modernization(self):
        for task, changed in (
            ("Optimize SQL query workload for the React table", ()),
            ("Build a background queue worker", ()),
            ("Fix GUID parsing in the server", ()),
            ("Review the modern-web-guidance license and README", ()),
            ("Documenta las guías CSS de modern-web-guidance", ()),
            ("Install modern-web-guidance for Codex", ()),
            ("Corrige solo una errata del botón", ("src/components/Submit.tsx",)),
            ("Fix only a typo in the React form label", ("app/contact/page.tsx",)),
            ("Repair the behavior", ("src/server/render.ts",)),
            ("Repair the behavior", ("app/actions.ts",)),
            ("Repair the behavior", ("docs/examples/dialog.html",)),
            ("Repair the behavior", ("src/emails/Welcome.tsx",)),
            ("Repair the behavior", (".next/static/output.css",)),
            ("Repair the behavior", ("node_modules/lib/component.tsx",)),
            ("Repair the behavior", ("src/components/Table.test.tsx",)),
            ("Integrate Modern Web Guidance into the Handbook for React forms", ()),
            ("Incorpora Ponytail al Handbook para formularios del CRM", ()),
            ("Integra Modern Web Guidance y Ponytail en el Handbook, con recursos para agentes personalizados y formularios web conectados al CRM", ()),
            ("Review React server handlers returning JSON", ()),
        ):
            with self.subTest(task=task, changed=changed):
                descriptor, capsules = self.capsules(task, changed)
                self.assertNotIn("web-platform-change", descriptor.archetypes)
                self.assertNotIn("browser-compatibility", descriptor.risks)
                for capsule in capsules:
                    self.assertNotIn("web-platform-compatibility", {item["id"] for item in capsule.units})

    def test_build_and_guid_are_not_ui_substrings(self):
        for task in ("Build a background queue worker", "Fix GUID parsing in the server", "Optimise SQL queries", "Review the build pipeline"):
            with self.subTest(task=task):
                self.assertNotIn("frontend", describe_task(task, PROFILE).surfaces)

    def test_lean_change_routes_completeness_not_line_count(self):
        for task in (
            "Apply Ponytail to simplify this API handler.",
            "Simplifica el código de permisos y elimina duplicación.",
            "Refactor the tenant-scoped mutation without changing its contract.",
            "Review the code and indirect callers for the smallest complete fix.",
            "Audita el código y sus consumidores, sin editar.",
            "Remove dead code and verify dynamic route registrations.",
            "Audit the API handler and update documentation",
        ):
            with self.subTest(task=task):
                self.assert_route(task, "lean-change", "minimum-complete-change")

    def test_source_research_and_copy_are_not_code_simplification(self):
        for task in ("Review Ponytail licensing", "Install Ponytail in Codex", "Simplifica el texto del correo", "Simplify the README", "Documenta Ponytail y sus hooks", "Audit the marketing copy"):
            with self.subTest(task=task):
                descriptor, _ = self.capsules(task)
                self.assertNotIn("lean-change", descriptor.archetypes)

    def test_named_sources_have_assessment_route_without_runtime_authority(self):
        for task in ("Review Modern Web Guidance", "Revisa Ponytail y modern-web-guidance", "Documenta Ponytail y sus hooks"):
            with self.subTest(task=task):
                descriptor, capsules = self.assert_route(task, "external-guidance-evaluation", "modern-web-lean-source-route")
                self.assertNotIn("deployment", descriptor.operations)
                self.assertNotIn("mutation", descriptor.operations)
                for capsule in capsules:
                    self.assertIn("pol-agent-operating-model", capsule.provenance)

    def test_named_plugin_install_also_keeps_existing_supply_chain_gate(self):
        for task in ("Install Ponytail", "Instala modern-web-guidance", "Update Ponytail plugin", "Actualiza el plugin de Modern Web Guidance", "Inspect Ponytail hooks", "Review the hooks for Modern Web Guidance"):
            with self.subTest(task=task):
                descriptor, capsules = self.capsules(task)
                self.assertIn("agent-execution", descriptor.risks)
                for capsule in capsules:
                    self.assertIn("agent-tools-review-execution-boundary", {item["id"] for item in capsule.units})

    def test_connected_products_resolve_boundary_owners(self):
        for task in (
            "Conecta el formulario de la web pública al CRM interno mediante API.",
            "Build a custom agent with CRM tools and approval before side effects.",
            "Revisa un agente personalizado que modifica contactos del CRM.",
            "Audit the public website to CRM webhook boundary, read only.",
            "Diseña agentes personalizados para clasificar solicitudes",
            "Build custom product agents with approval",
        ):
            with self.subTest(task=task):
                self.assert_route(task, "connected-product-change", "connected-product-resource-route")

    def test_product_agent_route_is_not_the_coding_host_or_one_css_fix(self):
        for task in ("Configure Codex agents", "Review a Claude Code hook", "Fix one margin in the CRM", "Write a public website headline", "Review the CRM sales copy"):
            with self.subTest(task=task):
                descriptor, _ = self.capsules(task)
                self.assertNotIn("connected-product-change", descriptor.archetypes)

    def test_integration_implementation_has_a_real_recovery_owner_without_deployment(self):
        descriptor, capsules = self.capsules("Audit the public website to CRM webhook boundary, read only.")
        implementation = capsules[1]
        self.assertIn("integration", descriptor.operations)
        self.assertNotIn("deployment", descriptor.operations)
        self.assertIn("operability-production-recovery", {item["id"] for item in implementation.units})
        self.assertIn("std-production-operability-baseline", implementation.provenance)
        self.assertIn("availability", implementation.covered)

    def test_explicit_intake_boundaries_do_not_become_a_hero_redesign(self):
        for task in (
            "Conecta el formulario de la página pública al CRM multiempresa mediante API, con permisos por organización; rechaza datos de otra empresa",
            "Implement tenant-scoped customer intake from the public website into the CRM API",
        ):
            with self.subTest(task=task):
                descriptor, capsules = self.capsules(task)
                self.assertIn("integration", descriptor.operations)
                self.assertIn("authorization", descriptor.operations)
                self.assertIn("tenant-isolation", descriptor.risks)
                self.assertNotIn("marketing-hero-change", descriptor.archetypes)
                self.assertNotIn("public-client-website", descriptor.archetypes)
                route = build_repo_route(PROFILE, descriptor)
                self.assertNotIn("database", route["avoid_by_default"])
                self.assertIn("authorization-negative", route["verification"])
                self.assertIn("cross-tenant-negative", route["verification"])
                self.assertIn("operability-production-recovery", {unit["id"] for unit in capsules[1].units})
                for capsule in capsules:
                    self.assertNotIn("ui-design-reconstruction", {unit["id"] for unit in capsule.units})
                    self.assertFalse(capsule.uncovered)

    def test_common_authorization_identifiers_keep_negative_gates(self):
        for task, tenant in (
            ("Fix the tenantId check in the CRM API", True),
            ("Review tenantID and tenant_key boundaries", True),
            ("Fix authorization in the CRM API", False),
            ("Fix rolesAllowed in the API handler", False),
            ("Fix permissionCheck in the API handler", False),
            ("Fix crossTenantId exposure in the CRM API", True),
            ("Fix request_tenant_id and RequestTenantID boundaries", True),
            ("Fix hasPermission in the CRM API", False),
            ("Review CheckUserPermissions and ROLE_ASSIGNMENT in the CRM API", False),
            ("Fix requestAuthorization and API_AUTHZ_CHECK in the CRM API", False),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn("authorization", descriptor.risks)
                route = build_repo_route(PROFILE, descriptor)
                self.assertIn("authorization-negative", route["verification"])
                if tenant:
                    self.assertIn("tenant-isolation", descriptor.risks)
                    self.assertIn("cross-tenant-negative", route["verification"])

        for task in ("Fix lieutenant spelling", "Review the permissionless parser", "Fix roleplay title"):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertNotIn("authorization", descriptor.risks)
                self.assertNotIn("tenant-isolation", descriptor.risks)

    def test_website_form_is_not_a_whole_website_request(self):
        for task in (
            "Build a public website form connected to CRM API",
            "Create a public website intake connected to the CRM API",
            "Build a public website's form connected to the CRM API",
            "Build a public website contact form connected to the CRM API",
            "Create a public website lead capture form connected to the CRM API",
            "Build a public website’s customer registration form connected to the CRM API",
            "Create a public website customer intake connected to the CRM API",
            "Build a public website CRM integration via API",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn("connected-product-change", descriptor.archetypes)
                self.assertNotIn("marketing-hero-change", descriptor.archetypes)
                self.assertNotIn("public-client-website", descriptor.archetypes)

    def test_observing_production_is_not_deploying_but_separate_release_is_retained(self):
        for task in (
            "Audit client-side form handling in production without edits",
            "Revisa en producción el formulario del CRM, solo lectura",
            "Inspect the production deployment without edits",
            "Inspect the form in production; do not deploy",
            "Revisa el formulario en producción; no despliegues nada",
            "Repair the form and verify the result in production",
        ):
            with self.subTest(task=task):
                descriptor, capsules = self.capsules(task)
                self.assertNotIn("deployment", descriptor.operations)
                self.assertFalse(descriptor.delivery.get("production_effect"))
                self.assertIn("production-observation", descriptor.archetypes)
                self.assertIn("operability-runtime-verification", {unit["id"] for unit in capsules[2].units})
        for task in (
            "Audit production read-only; then deploy the approved fix",
            "Revisa producción sin editar y despliega la corrección aprobada",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn("deployment", descriptor.operations)
                self.assertTrue(descriptor.delivery.get("production_effect"))
        for task in ("Fix the form; do not deploy", "Corrige el formulario sin desplegar"):
            descriptor = describe_task(task, PROFILE)
            self.assertNotIn("deployment", descriptor.operations)
            self.assertFalse(descriptor.delivery.get("production_effect"))

    def test_observed_release_identity_keeps_read_only_evidence(self):
        for task in (
            "Release provenance review: check the published SHA on the Production alias. Do not deploy.",
            "Deployment provenance audit: inspect the build ID served by the Production alias. Do not deploy.",
            "Comprueba el SHA desplegado en el alias de Preview frente al commit esperado.",
            "Audit the missing version receipt on the Production alias",
            "Verify whether the Production alias points to Preview",
        ):
            with self.subTest(task=task):
                descriptor, capsules = self.capsules(task)
                self.assertNotIn("deployment", descriptor.operations)
                self.assertFalse(descriptor.delivery["production_effect"])
                self.assertEqual(set(descriptor.intent), {"review"})
                for capsule in capsules:
                    self.assertIn("observed-release-provenance", capsule.required_evidence)
        for task in ("Verify the local Git commit SHA", "Audit the production logs; do not verify the published SHA",
                     "Review the README example of a published SHA on the Production alias"):
            with self.subTest(task=task):
                self.assertNotIn("release-provenance", describe_task(task, PROFILE).risks)

    def test_full_website_creation_keeps_design_even_when_connected_to_crm(self):
        for task in (
            "Build a public website connected to the CRM API",
            "Crea una web pública conectada al CRM mediante API",
            "Build a public website with a form connected to the CRM API",
            "Build a public website with a contact form connected to the CRM API",
            "Build a public website for clients with a lead capture form connected to CRM API",
            "Crea una página web de servicios con un formulario conectado al CRM mediante API",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn("public-client-website", descriptor.archetypes)
                self.assertIn("marketing-hero-change", descriptor.archetypes)
                self.assertIn("integration", descriptor.operations)

    def test_read_only_guidance_does_not_request_a_release(self):
        for task in (
            "Audita con Ponytail el código del CRM, sin editar.",
            "Audit browser dialogs with Modern Web Guidance, read only.",
            "Revisa el formulario web conectado al CRM, solo lectura.",
        ):
            descriptor, _ = self.capsules(task)
            with self.subTest(task=task):
                self.assertNotIn("mutation", descriptor.operations)
                self.assertNotIn("deployment", descriptor.operations)
                self.assertFalse(descriptor.delivery.get("production_effect"))

    def test_installed_bundle_runs_context_and_exposes_canonical_resources(self):
        # Exercise the real distribution script and runtime, not the text of an
        # installation example. This never touches the user's installed skills.
        with tempfile.TemporaryDirectory(prefix="handbook-guidance-") as temporary:
            target = Path(temporary) / "skills"
            script = ROOT / "automation/codex/handbook_update.py"
            for mode in ("Install", "Check"):
                result = subprocess.run([sys.executable, "-I", str(script), "bundle", "--source", str(ROOT), "--skills-home", str(target), *(["--check"] if mode == "Check" else [])], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = target / "engineering-handbook"
            references = installed / "references"
            self.assertEqual(list(target.glob("*/SKILL.md")), [installed / "SKILL.md"])
            for relative in (
                "references/modern-web-ponytail-adoption-assessment.md",
                "references/connected-product-resource-map.md",
                "playbooks/modern-web-platform-workflow.md",
                "policies/reuse-first.md",
            ):
                document = references / relative
                self.assertEqual(document.read_bytes(), (ROOT / relative).read_bytes())
                for href in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
                    if href.startswith(("https://", "http://", "#")):
                        continue
                    linked = (document.parent / href.split("#", 1)[0]).resolve()
                    self.assertTrue(linked.is_relative_to(references), href)
                    self.assertTrue(linked.is_file(), f"Broken distributed resource {relative} -> {href}")
            consumer = Path(temporary) / "consumer"
            consumer.mkdir()
            result = subprocess.run([
                sys.executable, "-m", "automation.engineering_context", "context",
                "--repo", str(consumer), "--handbook", "machine-readable/compiled",
                "--mode", "verify", "--task", "Audit browser form connected to CRM with Ponytail", "--metrics",
            ], cwd=references, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            ids = {item["id"] for item in payload["capsule"]["units"]}
            self.assertTrue({"web-platform-compatibility", "minimum-complete-change", "connected-product-resource-route", "modern-web-lean-source-route"}.issubset(ids), ids)
            self.assertFalse(payload["capsule"]["uncovered"])
            self.assertFalse(payload["descriptor"]["delivery"].get("production_effect"))
