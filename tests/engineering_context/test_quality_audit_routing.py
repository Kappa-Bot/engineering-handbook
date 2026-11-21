from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from automation.engineering_context.cli import _load_compiled
from automation.engineering_context.context_solver import build_repo_route, solve_context
from automation.engineering_context.discovery import build_discovery, knowledge_tree, search
from automation.engineering_context.handbook_compile import compile_handbook
from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import describe_task


ROOT = Path(__file__).resolve().parents[2]
EMPTY = {"detected": {"capabilities": {}, "landmarks": {}}}


class QualityReviewClassificationTests(unittest.TestCase):
    def test_public_hreflang_review_requests_route_evidence_without_launch_authority(self):
        unit_id = "public-locale-alternate-route-evidence"
        tasks = (
            "Audit hreflang and reciprocal alternate URLs for the English and Spanish public pricing pages.",
            "Verifica el hreflang y las canónicas de las rutas públicas en español e inglés.",
            "Audita los enlaces alternativos recíprocos de las páginas públicas en inglés y español.",
            "Do not change hreflang; audit hreflang for the public locale URLs.",
            "Audit hreflang on live public pricing pages using the docs as supporting material.",
        )
        for phase in ("planning", "verification"):
            compiled = _load_compiled(ROOT / "machine-readable/compiled", phase)
            for task in tasks:
                with self.subTest(task=task, phase=phase):
                    descriptor = describe_task(task, EMPTY)
                    self.assertIn("public-locale-alternate-review", descriptor.archetypes)
                    self.assertNotIn("modify", descriptor.intent)
                    self.assertFalse(descriptor.delivery["production_effect"])
                    capsule = solve_context(compiled, descriptor, phase)
                    item = next(unit for unit in capsule.units if unit["id"] == unit_id)
                    self.assertEqual(item["source"], "std-public-web-discoverability-baseline")
                    self.assertEqual(item["type"], "verification")
                    self.assertEqual(item["force"], "must")
                    self.assertIn("locale-alternate-integrity", capsule.covered)
                    self.assertIn("reciprocal", item["text"])
                    self.assertIn("XML sitemap", item["text"])
                    self.assertIn("NOT RUN", item["text"])

            for task in (
                "Review the hreflang settings label wording for the site's public English and Spanish URLs.",
                "Revisa el hreflang de la documentación de un sitio web público.",
                "Review `hreflang` documentation for the public pricing pages.",
                "Review hreflang on the private admin console's locale URLs.",
                "Do not review hreflang on the public English and Spanish pages.",
                "Audit the root lang attribute on a public page.",
                "Review the translated Spanish button copy on the public website.",
                "Audit robots.txt and noindex behavior on the public website.",
                "Review hreflang for the public website documentation.",
                "Inspect hreflang in the public site guide.",
                "Verifica el hreflang del sitio web público de la guía de integración.",
                "Inspect hreflang as explained by the guide for public pricing pages.",
                "Revisa el hreflang que documenta el manual de las rutas públicas.",
            ):
                with self.subTest(task=task, phase=phase):
                    descriptor = describe_task(task, EMPTY)
                    capsule = solve_context(compiled, descriptor, phase)
                    self.assertNotIn("public-locale-alternate-review", descriptor.archetypes)
                    self.assertNotIn(unit_id, {unit["id"] for unit in capsule.units})

    def test_forced_colors_review_routes_only_actual_interface_state_evidence(self):
        unit_id = "ui-forced-colors-state-evidence"
        positive = (
            "Audit keyboard focus and selected tabs in Windows High Contrast on the settings page.",
            "Comprueba que el foco sigue visible con colores forzados en el formulario.",
            "Audit forced-colors support for focused inputs in the existing interface.",
            "Revisa las opciones marcadas en el alto contraste de Windows.",
            "Review Windows High Contrast on the form, using the guide only as supporting evidence.",
            "Revisa el alto contraste de Windows en el formulario usando el manual como evidencia de apoyo.",
        )
        negative = (
            "Review text contrast and keyboard focus in the public contact form.",
            "Audit the application's high-contrast theme colors and selected tabs.",
            "Review the Windows High Contrast settings label wording in the app.",
            "Review focus indicators in the Windows High Contrast user guide for the checkout form.",
            "Review Windows High Contrast on forms as depicted in the CSS guide.",
            "Review focus state training examples in Windows High Contrast.",
            "Revisa el alto contraste de Windows en formularios descritos en un manual para corregir la traducción.",
            "Do not audit forced-colors; review ordinary keyboard focus in the form.",
            "Apply Neumorphism to the internal operator console.",
        )
        for phase in ("planning", "verification"):
            compiled = _load_compiled(ROOT / "machine-readable/compiled", phase)
            for task in positive + negative:
                with self.subTest(task=task, phase=phase):
                    descriptor = describe_task(task, EMPTY)
                    capsule = solve_context(compiled, descriptor, phase)
                    selected = {unit["id"]: unit for unit in capsule.units}
                    if task in negative:
                        self.assertNotIn(unit_id, selected)
                        continue
                    self.assertIn("accessibility-forced-colors-review", descriptor.archetypes)
                    self.assertNotIn("modify", descriptor.intent)
                    self.assertFalse(descriptor.delivery["production_effect"])
                    self.assertIn("forced-colors-visibility", capsule.covered)
                    self.assertIn(unit_id, capsule.required_evidence)
                    self.assertEqual(selected[unit_id]["source"], "std-ui-ux-quality-baseline")
                    self.assertIn("native OS contrast-theme or emulated", selected[unit_id]["text"])
                    self.assertIn("NOT RUN", selected[unit_id]["text"])

    def test_focused_quality_audits_are_classified_without_write_authority(self):
        cases = (
            ("Audita la UX y UI del CRM", {"ui-quality-review"}, {"ux-quality"}),
            ("Review the usability of the admin dashboard", {"ui-quality-review"}, {"ux-quality"}),
            ("Revisa la accesibilidad con teclado y zoom en la web", {"accessibility-review"}, {"accessibility"}),
            ("Audit WCAG and screen reader support in forms", {"accessibility-review"}, {"accessibility"}),
            ("Review LCP INP CLS and SQL query latency", {"performance-review"}, {"performance"}),
            ("Revisa el rendimiento de las consultas SQL y las páginas del dashboard", {"performance-review"}, {"performance"}),
            ("Audita la seguridad y privacidad de la app", {"security-review", "privacy-review"}, {"security-exposure", "privacy-exposure"}),
            ("Revisa las vulnerabilidades de la API y la configuración CORS", {"security-review"}, {"security-exposure"}),
            ("Audit cookies consent and GDPR on website", {"privacy-review"}, {"privacy-exposure"}),
            ("Review data retention and deletion in the internal CRM", {"privacy-review"}, {"privacy-exposure"}),
            ("Review error rates and observability in production", {"reliability-review"}, {"availability"}),
            ("Revisa los errores de runtime y la recuperación en producción", {"reliability-review"}, {"availability"}),
        )
        for task, archetypes, risks in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertTrue(archetypes.issubset(descriptor.archetypes), descriptor.to_dict())
                self.assertTrue(risks.issubset(descriptor.risks), descriptor.to_dict())
                self.assertNotIn("modify", descriptor.intent)
                self.assertFalse(descriptor.delivery["production_effect"])

    def test_holistic_review_expands_only_relevant_domains(self):
        cases = (
            ("Realiza una revisión integral de UX, UI, performance, seguridad y privacidad",
             {"quality-audit", "ui-quality-review", "performance-review", "security-review", "privacy-review"}),
            ("Haz una auditoría global del producto",
             {"quality-audit"}),
            ("Carry out a holistic engineering quality audit of the product",
             {"quality-audit"}),
            ("Auditoría de todo el repo: UX, UI, performance, seguridad y privacidad",
             {"quality-audit", "ui-quality-review", "performance-review", "security-review", "privacy-review"}),
            ("Audit everything in the repository", {"quality-audit"}),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertTrue(expected.issubset(descriptor.archetypes), descriptor.to_dict())
                self.assertIn("review", descriptor.intent)
                self.assertNotIn("modify", descriptor.intent)
                self.assertFalse(descriptor.delivery["production_effect"])

    def test_natural_review_headers_resolve_speciality_without_implicit_edits(self):
        cases = (
            ("Complete a security review of the API", {"security-review"}),
            ("Haz un análisis de seguridad del CRM", {"security-review"}),
            ("Conduct a security audit of the API", {"security-review"}),
            ("Realiza una auditoría de seguridad del CRM", {"security-review"}),
            ("Haz una revisión de accesibilidad", {"accessibility-review"}),
            ("Perform a performance audit", {"performance-review"}),
            ("Do a security audit of the API", {"security-review"}),
            ("Efectúa una auditoría de fiabilidad del servicio", {"reliability-review"}),
            ("Reliability review of the service", {"reliability-review"}),
            ("Audit the quality of the product", {"quality-audit"}),
            ("Check UX, accessibility, security and privacy", {
                "ui-quality-review", "accessibility-review", "security-review", "privacy-review"
            }),
            ("Realiza una auditoría integral de UX, seguridad, privacidad, rendimiento, accesibilidad y fiabilidad", {
                "quality-audit", "ui-quality-review", "security-review", "privacy-review",
                "performance-review", "accessibility-review", "reliability-review"
            }),
            ("Review the visual quality of the public website", {"ui-quality-review"}),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertTrue(expected.issubset(descriptor.archetypes), descriptor.to_dict())
                self.assertIn("review", descriptor.intent)
                self.assertNotIn("modify", descriptor.intent)
                if "quality-audit" in expected:
                    self.assertIn("quality-coverage", descriptor.risks)

    def test_nominal_exclusions_are_not_review_domains(self):
        cases = (
            ("Review the UX, not security", {"ui-quality-review"}),
            ("Review UX, excluding privacy and security", {"ui-quality-review"}),
            ("Review UX without security or privacy", {"ui-quality-review"}),
            ("Revisa UX, sin privacidad ni seguridad", {"ui-quality-review"}),
            ("Review UX, not security; audit privacy", {"ui-quality-review", "privacy-review"}),
            ("Review security and UX, excluding privacy", {"security-review", "ui-quality-review"}),
            ("Revisa UX, pero no audites seguridad", {"ui-quality-review"}),
        )
        domains = {"ui-quality-review", "security-review", "privacy-review", "performance-review", "reliability-review", "accessibility-review"}
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(expected, set(descriptor.archetypes) & domains, descriptor.to_dict())

    def test_quality_remediation_is_writable_only_on_explicit_action(self):
        for task, expected in (
            ("Fix XSS vulnerabilities in the API", "security-review"),
            ("Corrige los problemas de accesibilidad del formulario", "accessibility-review"),
            ("Optimiza el rendimiento de las consultas SQL", "performance-review"),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertIn("modify", descriptor.intent)
                self.assertIn(expected, descriptor.archetypes)

    def test_questions_prohibitions_and_docs_only_do_not_route_product_reviews(self):
        cases = (
            ("Do not audit security", set()),
            ("No audites seguridad; revisa la UI", {"ui-quality-review"}),
            ("How should I audit security?", set()),
            ("¿Cómo auditar privacidad?", set()),
            ("Review documentation about GDPR requirements", set()),
            ("Review README security instructions", set()),
            ("Security audit documentation", set()),
            ("Revisa la guía del handbook sobre performance", set()),
            ("Audit the security of the CRM; rename the README", {"security-review"}),
            ("Revisa UX del CRM; no audites seguridad", {"ui-quality-review"}),
        )
        names = {"quality-audit", "ui-quality-review", "performance-review", "security-review", "privacy-review", "accessibility-review", "reliability-review"}
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(expected, set(descriptor.archetypes) & names, descriptor.to_dict())
                if task != "Audit the security of the CRM; rename the README":
                    self.assertNotIn("modify", descriptor.intent, task)

    def test_performance_measurement_is_not_hero_reconstruction(self):
        for task in (
            "Measure LCP, INP, CLS and hydration in public website",
            "Audit page load performance on a public website",
            "Measure LCP of the hero image on the public website",
            "Measure the performance of the animated landing hero",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertIn("performance-review", descriptor.archetypes)
                self.assertNotIn("marketing-hero-change", descriptor.archetypes)
                self.assertNotIn("hero-fidelity", descriptor.risks)

    def test_noun_first_and_scanning_quality_requests_are_not_lost(self):
        cases = (
            ("Security audit of the API", "security-review"),
            ("Privacy review of internal CRM", "privacy-review"),
            ("Performance audit of SQL queries", "performance-review"),
            ("Accessibility audit of forms", "accessibility-review"),
            ("UX review of the dashboard", "ui-quality-review"),
            ("Scan the repository for XSS vulnerabilities", "security-review"),
            ("Escanea seguridad y vulnerabilidades del backend", "security-review"),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertIn(expected, descriptor.archetypes)
                self.assertIn("review", descriptor.intent)
                self.assertNotIn("modify", descriptor.intent)

    def test_supporting_documentation_does_not_erase_actual_product_review(self):
        descriptor = describe_task("Review the security of the API and document it in README", EMPTY)
        self.assertIn("security-review", descriptor.archetypes)
        self.assertNotIn("modify", descriptor.intent)
        descriptor = describe_task("Audit the privacy of the CRM and compare the handbook guidance", EMPTY)
        self.assertIn("privacy-review", descriptor.archetypes)
        self.assertNotIn("modify", descriptor.intent)

    def test_document_object_is_not_application_audit_but_auxiliary_sources_are(self):
        domains = {"ui-quality-review", "security-review", "privacy-review", "performance-review", "reliability-review", "accessibility-review", "quality-audit"}
        for task in (
            "Review the security guide",
            "Review the API security documentation",
            "Review the privacy policy documentation",
            "Haz una revisión de la guía de accesibilidad",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertFalse(domains & set(descriptor.archetypes), descriptor.to_dict())
                if task == "Review the API security documentation":
                    self.assertNotIn("code-change", descriptor.archetypes)
                    self.assertNotIn("external-integration", descriptor.archetypes)
        for task, expected in (
            ("Audit reliability of the server and use README as reference", "reliability-review"),
            ("Review the security of the API using docs as evidence", "security-review"),
            ("Revisa la accesibilidad de la web con el handbook como referencia", "accessibility-review"),
        ):
            with self.subTest(task=task):
                self.assertIn(expected, describe_task(task, EMPTY).archetypes)

    def test_targeted_quality_routes_and_mixed_boundaries(self):
        cases = (
            ("Revisa la UX del dashboard", {"ui-surface", "design-primitives", "ui-interaction-tests"}),
            ("Revisa las vulnerabilidades de la API y CORS", {"security-configuration", "authorization-boundary", "integration-boundary"}),
            ("Audit GDPR retention and consent in the CRM", {"privacy-data-lifecycle", "consent-owner"}),
            ("Review LCP and SQL query latency", {"performance-evidence", "persistence-owner"}),
            ("Audit production failures and recovery", {"runtime-observability", "release-config"}),
            ("Audita UX, seguridad y rendimiento SQL del CRM", {"ui-surface", "security-configuration", "persistence-owner", "performance-evidence"}),
        )
        for task, labels in cases:
            with self.subTest(task=task):
                route = build_repo_route(EMPTY, describe_task(task, EMPTY))
                self.assertTrue(labels.issubset(route["inspect_first"]), route)
        route = build_repo_route(EMPTY, describe_task("Audita la seguridad del dashboard y la autorización del tenant", EMPTY))
        self.assertNotIn("database", route["avoid_by_default"])
        for task in (
            "Review the dashboard UX and cross-tenant permissions",
            "Revisa la UX del dashboard y los permisos entre tenants",
            "Check UX, accessibility, security and privacy",
        ):
            with self.subTest(task=task):
                route = build_repo_route(EMPTY, describe_task(task, EMPTY))
                self.assertNotIn("database", route["avoid_by_default"])
                if "tenant" in task:
                    self.assertIn("persistence-owner", route["inspect_first"])

    def test_real_landmarks_and_path_only_quality_signals(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            owners = (
                "src/components/dashboard.tsx",
                "e2e/accessibility/login.spec.ts",
                "src/security/csp.ts",
                "src/middleware.ts",
                "src/lib/privacy/retention.ts",
                "src/consent/preferences.ts",
                "src/lib/performance/metrics.ts",
                "lighthouse.config.js",
                "src/instrumentation.ts",
                "src/lib/db/query.ts",
                "tests/performance/dashboard.spec.ts",
                "docs/security/csp.ts",
                "docs/examples/playwright.config.ts",
                "docs/performance/lighthouse.config.js",
                "vendor/lib/privacy/retention.ts",
                "generated/security/csp.ts",
                "src/lib/consent.ts",
                "src/privacy/requests/erase.ts",
                "src/privacy.generated.ts",
            )
            for name in owners:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            profile = profile_repo(root)
            landmarks = profile["detected"]["landmarks"]
            for label, owner in (
                ("ui-interaction-tests", "e2e/accessibility/login.spec.ts"),
                ("security-configuration", "src/security/csp.ts"),
                ("security-configuration", "src/middleware.ts"),
                ("privacy-data-lifecycle", "src/lib/privacy/retention.ts"),
                ("privacy-data-lifecycle", "src/lib/consent.ts"),
                ("privacy-data-lifecycle", "src/privacy/requests/erase.ts"),
                ("performance-evidence", "lighthouse.config.js"),
                ("runtime-observability", "src/instrumentation.ts"),
            ):
                with self.subTest(label=label, owner=owner):
                    self.assertIn(owner, landmarks[label])
            for label in ("security-configuration", "privacy-data-lifecycle"):
                self.assertTrue(all(not p.startswith(("docs/", "vendor/", "generated/")) for p in landmarks[label]))
            self.assertNotIn("docs/examples/playwright.config.ts", landmarks["ui-interaction-tests"])
            self.assertNotIn("docs/performance/lighthouse.config.js", landmarks["performance-evidence"])
            self.assertNotIn("src/privacy.generated.ts", landmarks["privacy-data-lifecycle"])
            route = build_repo_route(profile, describe_task("Audit security, GDPR and performance", profile))
            self.assertIn("src/security/csp.ts", route["resolved"]["security-configuration"])
            for path, expected in (
                ("src/security/csp.ts", "security-review"),
                ("src/lib/privacy/retention.ts", "privacy-review"),
                ("src/lib/consent.ts", "privacy-review"),
                ("src/privacy/requests/erase.ts", "privacy-review"),
                ("src/lib/performance/metrics.ts", "performance-review"),
            ):
                with self.subTest(changed=path):
                    descriptor = describe_task("Review the changed file", profile, (path,))
                    self.assertIn(expected, descriptor.archetypes)
                    self.assertNotIn("modify", descriptor.intent)
            self.assertNotIn("privacy-review", describe_task(
                "Review the changed file", profile, ("src/privacy.generated.ts",)
            ).archetypes)


class QualityReviewContextTests(unittest.TestCase):
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

    def test_database_backup_restore_evidence_is_scoped_to_a_read_only_review(self):
        unit_id = "operability-database-backup-restore-evidence"
        for task, expected in (
            ("Review evidence that the configured database backups can restore the application's durable records.", True),
            ("Audita la evidencia de restauración de las copias de seguridad de la base de datos.", True),
            ("Verify the application's database backup restore evidence using the runbook as a reference.", True),
            ("Review the provider's public database backup restore documentation.", False),
            ("Review the database backup restore label in the settings screen.", False),
            ("Review the database backup restore evidence as a reference for the release note.", False),
            ("Review the database backup restore runbook wording in the admin documentation.", False),
            ("Inspect database backup restore steps from the public operations manual.", False),
            ("Revisa la copia de seguridad y restauración de la base de datos descritas en la documentación del proveedor únicamente para mejorar el texto.", False),
            ("Review the release report using database backup restore evidence as a reference.", False),
            ("Do not review database backup restore evidence; review the release notice.", False),
            ("Review restoration of a Git branch after the merge.", False),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertFalse(descriptor.operations)
                self.assertFalse(descriptor.delivery["production_effect"])
                for phase in ("planning", "verification"):
                    _, capsule = self.selected(task, phase)
                    self.assertEqual(unit_id in capsule.required_evidence, expected)

    def test_holistic_review_has_intake_and_closure_without_implicit_mutations(self):
        task = "Realiza una revisión integral de UX, UI, performance, seguridad y privacidad"
        for phase, expected in (
            ("planning", "quality-audit-intake"),
            ("implementation", "quality-audit-intake"),
            ("verification", "quality-audit-closure"),
        ):
            with self.subTest(phase=phase):
                units, capsule = self.selected(task, phase)
                self.assertIn(expected, units)
                self.assertFalse(capsule.uncovered, capsule.to_dict())
                self.assertIn("pb-engineering-quality-audit", capsule.provenance)
        self.assertNotIn("modify", describe_task(task, EMPTY).intent)

    def test_rendered_language_markup_selects_scoped_accessibility_evidence(self):
        unit_id = "ui-language-semantics-evidence"
        for task in (
            "Verify the rendered page's root lang matches the visible language after switching locales.",
            "Comprueba que el atributo lang de la página coincide con el idioma visible.",
            "Review the lang attribute on French passages inside the English page.",
            "Verifica el marcado lang de los fragmentos franceses dentro de una página en inglés.",
            "Audit language of page and language of parts on the localized routes.",
            "Verify whether the default human language of this web page can be programmatically determined.",
            "Verify whether the human language of each passage or phrase can be programmatically determined.",
            "Audit the rendered <html lang=\"en\"> after the switch, using documentation only as supporting evidence.",
            'Audit the rendered <html lang="en"> after switching the page to Spanish.',
            "Verify whether the language of the page is programmatically determined after switching locales.",
            "Revisa si se puede determinar programáticamente el idioma de la página.",
            "Audita el idioma de la página y el idioma de las partes según WCAG 2.2 3.1.1 y 3.1.2.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(descriptor.intent, ("review",))
                self.assertFalse(descriptor.operations)
                self.assertIn("accessibility-review", descriptor.archetypes)
                for phase in ("planning", "verification"):
                    units, capsule = self.selected(task, phase)
                    self.assertIn(unit_id, capsule.required_evidence)
                    self.assertIn("std-ui-ux-quality-baseline", capsule.provenance)
                    if phase == "verification":
                        self.assertIn("ui-accessibility-functional-verification", units)
        for task in (
            "Review the <html lang=\"en\"> code example in the translator documentation.",
            "Review SEO hreflang for alternate locale URLs.",
            "Revisa la traducción de los botones y los rótulos en español.",
            "Review the button label 'HTML lang' on the locale selector.",
            "Review the HTML lang documentation.",
            "Review the rendered page's root lang binding label preset in the configuration panel.",
            "Review language of page settings label wording.",
            "Review the README documenting the HTML lang attribute.",
            "No audites el atributo lang de la página; revisa las traducciones.",
            "Audit WCAG keyboard and zoom in the app.",
        ):
            with self.subTest(task=task):
                self.assertNotIn(unit_id, self.selected(task, "verification")[0])

    def test_accessible_authentication_selects_step_level_evidence(self):
        unit_id = "ui-accessible-authentication-evidence"
        for task in (
            "Audit whether the sign-in flow allows autofill from a password manager.",
            "Verifica que el código de un solo uso se pueda pegar en el paso de autenticación.",
            "Review WCAG 2.2 3.3.8 Accessible Authentication (Minimum) on the actual sign-in flow.",
            "Audit accessible authentication on the sign-in flow.",
            "Revisa la autenticación accesible durante el inicio de sesión.",
            "Comprueba si un gestor de contraseñas puede autocompletar el formulario de inicio de sesión.",
            "Audit whether the sign-in flow offers an accessible alternative to a memorization or transcription test.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(descriptor.intent, ("review",))
                self.assertFalse(descriptor.operations)
                for phase in ("planning", "verification"):
                    _, capsule = self.selected(task, phase)
                    self.assertIn(unit_id, capsule.required_evidence)
        for task in (
            "Review the password manager label in the onboarding guide.",
            "Audit API rate limits for authentication attempts.",
            "Review whether users can paste their title into the search field.",
            "Review password manager autofill on the sign-in form label.",
            "Review accessible authentication on the sign-in flow label.",
            "Review accessible authentication in the onboarding guide.",
            "Do not review password manager autofill on the login form; review the help text.",
        ):
            with self.subTest(task=task):
                self.assertNotIn(unit_id, self.selected(task, "verification")[0])

    def test_domain_contracts_are_available_in_each_phase(self):
        cases = (
            ("Audit the UX of the CRM dashboard", "ux-journey-audit", "ux-journey-evidence", "pb-frontend-quality-review"),
            ("Audita la seguridad de la API y CORS", "security-attack-surface-review", "security-review-negative-evidence", "pb-security-review"),
            ("Review GDPR retention and deletion in the CRM", "privacy-data-flow-review", "privacy-boundary-evidence", "std-privacy-data-handling-baseline"),
            ("Review SQL query latency and LCP", "performance-bottleneck-triage", "performance-measure-before-optimization", "pat-performance-budgeting"),
            ("Audit WCAG keyboard and zoom in the app", "ui-accessibility-baseline", "ui-accessibility-functional-verification", "std-ui-ux-quality-baseline"),
            ("Review production failures and recovery", "operability-production-recovery", "operability-runtime-verification", "std-production-operability-baseline"),
        )
        for task, planning_unit, verification_unit, source in cases:
            with self.subTest(task=task):
                for phase in ("planning", "implementation", "verification"):
                    units, capsule = self.selected(task, phase)
                    self.assertFalse(capsule.uncovered, (phase, capsule.to_dict()))
                    self.assertIn(source, capsule.provenance)
                    if phase == "planning":
                        self.assertIn(planning_unit, units)
                    if phase == "verification":
                        self.assertIn(verification_unit, units)

    def test_self_service_account_erasure_selects_privacy_evidence(self):
        for task in (
            "Audit whether users can delete their own account in the internal app",
            "Comprueba si los usuarios pueden eliminar su propia cuenta en la aplicación",
            "Audit the user's account erasure request workflow",
            "Audit the self-service account erasure flow for signed-in members",
            "Audita el flujo de solicitudes de supresión de la cuenta del usuario",
        ):
            with self.subTest(task=task):
                self.assertIn("privacy-data-flow-review", self.selected(task, "planning")[0])
                self.assertIn("privacy-boundary-evidence", self.selected(task, "verification")[0])
                self.assertNotIn("modify", describe_task(task, EMPTY).intent)
        for task in (
            "Review whether CI service accounts can delete their own accounts",
            "Audit whether service users can delete their own accounts in the automation console",
            "Review whether users can change their own account name",
            "Review whether users can delete their own account shortcut in the app",
            "Review the README explaining how users can delete their own account",
            "Review the settings layout; do not check whether users can delete their own account",
        ):
            with self.subTest(task=task):
                self.assertNotIn("privacy-review", describe_task(task, EMPTY).archetypes)

    def test_signed_in_members_owned_account_scope(self):
        cases = (
            ("Review whether signed-in members can delete their own account", True),
            ("Revisa si los miembros autenticados pueden eliminar sus propias cuentas", True),
            ("Revisa si la cliente autenticada puede borrar su propia cuenta de la aplicación", True),
            ("Review whether signed-in members can delete their own account using the button label as evidence", True),
            ("Review whether a signed-in customer can erase their account via the account erasure workflow", True),
            ("Review whether signed-in members can delete another member's account", False),
            ("Review whether signed-in members can delete their own account shortcut", False),
            ("Review whether signed-in members can delete their own account button from the dashboard", False),
            ("Review whether signed-in members can delete their own account workflow from the list", False),
            ("Review the button label 'signed-in members can delete their own account'", False),
            ("Revisa el texto del botón «los miembros autenticados pueden eliminar sus propias cuentas»", False),
            ("Revisa si los miembros autenticados pueden borrar sus propias cuentas de servicio desde el portal", False),
        )
        for task, expected in cases:
            with self.subTest(task=task):
                planned, _ = self.selected(task, "planning")
                verified, capsule = self.selected(task, "verification")
                self.assertEqual("privacy-data-flow-review" in planned, expected)
                self.assertEqual("privacy-boundary-evidence" in verified, expected)
                self.assertEqual("privacy-boundary-evidence" in capsule.required_evidence, expected)
                self.assertNotIn("modify", describe_task(task, EMPTY).intent)

    def test_product_ai_grounding_review_selects_scoped_existing_evidence_method(self):
        unit_id = "product-ai-grounding-evidence"
        for task in (
            "Review citation accuracy for the in-product AI assistant using the user guide as evidence.",
            "Review whether the in-product LLM assistant cites its approved source for each answer.",
            "Revisa si el asistente de IA del producto cita fuentes aprobadas en sus respuestas.",
            "Audit whether the in-product AI assistant cites approved sources for its answers.",
            "Audit whether the in-product AI assistant grounds support answers in approved knowledge.",
            "Revisa si el asistente de IA del producto se abstiene cuando no hay fuentes.",
            "Verify grounded answers and no-source abstention for the AI assistant in the product.",
            "Verifica la exactitud de las citas del asistente de IA de la aplicación.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, EMPTY)
                self.assertEqual(descriptor.intent, ("review",))
                self.assertFalse(descriptor.operations)
                for phase in ("planning", "verification"):
                    units, capsule = self.selected(task, phase)
                    self.assertIn(unit_id, units)
                    self.assertIn(unit_id, capsule.required_evidence)
                    self.assertIn("pat-risk-based-verification-matrix", capsule.provenance)
        for task in (
            "Review whether the in-product AI assistant cites approved sources links from the sidebar.",
            "Revisa la exactitud de las citas del asistente de IA de la aplicación en la guía de usuario.",
            "Review the in-product AI assistant's citation accuracy dashboard label for clarity.",
            "Review citation accuracy for the in-product AI assistant's user guide.",
            "Verify grounded support answers and missing-source fallback for the deterministic FAQ.",
            "Review the in-product AI assistant's prompt for grounded answers.",
            "Review the in-product AI assistant's grounded answer label.",
            "Review citation accuracy for the AI assistant in the product documentation.",
            "Revisa la documentación sobre la abstención sin fuentes del asistente de IA de la aplicación.",
            "Review the layout; do not review grounded answers for the in-product AI assistant.",
            "Audit Google AI Overviews supporting-link eligibility for a public website.",
            "Review grounded answers for the coding agent's handoff.",
            "Compare AI provider recommendations for the product.",
        ):
            with self.subTest(task=task):
                self.assertNotIn(unit_id, self.selected(task, "verification")[0])

    def test_public_privacy_review_reaches_web_legal_owner_but_internal_does_not(self):
        public = "Audit cookies consent and GDPR on public website"
        internal = "Audit privacy and data retention of the internal CRM"
        self.assertIn("public-privacy-review", describe_task(public, EMPTY).archetypes)
        self.assertNotIn("public-privacy-review", describe_task(internal, EMPTY).archetypes)
        public_units, _ = self.selected(public, "planning")
        internal_units, _ = self.selected(internal, "planning")
        self.assertIn("public-legal-trust-plan", public_units)
        self.assertNotIn("public-legal-trust-plan", internal_units)
        internal_web = "Audit privacy of the internal web app"
        self.assertIn("privacy-review", describe_task(internal_web, EMPTY).archetypes)
        self.assertNotIn("public-privacy-review", describe_task(internal_web, EMPTY).archetypes)
        for phase in ("planning", "implementation", "verification"):
            units, _ = self.selected(internal_web, phase)
            self.assertNotIn("public-legal-trust-plan", units)
        for public_policy in (
            "Review the public website privacy policy",
            "Revisa la política de privacidad de la web pública",
        ):
            with self.subTest(public_policy=public_policy):
                descriptor = describe_task(public_policy, EMPTY)
                self.assertIn("public-privacy-review", descriptor.archetypes)
                self.assertNotIn("privacy-review", descriptor.archetypes)
                self.assertIn("public-legal-trust-plan", self.selected(public_policy, "planning")[0])

    def test_hero_performance_measurements_skip_design_reconstruction_in_every_phase(self):
        for task in (
            "Measure LCP of the hero image on the public website",
            "Review the visual quality of the public website",
            "Measure the performance of the animated landing hero",
        ):
            for phase in ("planning", "implementation", "verification"):
                with self.subTest(task=task, phase=phase):
                    units, _ = self.selected(task, phase)
                    # The shared Unslop rubric may guide a read-only review;
                    # hero composition contracts must not be selected merely
                    # because the measured UI contains a hero element.
                    self.assertNotIn("marketing-hero-brief-and-source", units)
                    self.assertNotIn("marketing-hero-live-acceptance", units)

    def test_natural_domain_requests_activate_phase_specific_evidence(self):
        for task, planning, verification in (
            ("Conduct a security audit of the API", "security-attack-surface-review", "security-review-negative-evidence"),
            ("Haz una revisión de accesibilidad", "ui-accessibility-baseline", "ui-accessibility-functional-verification"),
            ("Perform a performance audit", "performance-bottleneck-triage", "performance-measure-before-optimization"),
            ("Reliability review of the service", "operability-production-recovery", "operability-runtime-verification"),
        ):
            with self.subTest(task=task):
                self.assertIn(planning, self.selected(task, "planning")[0])
                self.assertIn(verification, self.selected(task, "verification")[0])

    def test_read_only_security_performance_audit_does_not_select_design_reconstruction(self):
        task = "Review security vulnerabilities and SQL performance on the public website"
        for phase in ("planning", "implementation", "verification"):
            units, capsule = self.selected(task, phase)
            self.assertNotIn("ui-design-reconstruction", units)
            self.assertNotIn("frontend-design-fit-review", units)
            self.assertFalse(capsule.uncovered)
        for phase in ("planning", "verification"):
            units, _ = self.selected("Review README security documentation", phase)
            self.assertNotIn("security-attack-surface-review", units)
            self.assertNotIn("quality-audit-intake", units)


class QualityReviewDiscoveryTests(unittest.TestCase):
    def test_canonical_quality_review_sources_are_findable_by_topic(self):
        index = build_discovery(ROOT)
        cases = (
            ("auditoría integral calidad ux rendimiento seguridad privacidad", "pb-engineering-quality-audit"),
            ("privacy data handling retention deletion CRM", "std-privacy-data-handling-baseline"),
            ("auditar seguridad api csrf cors xss", "pb-security-review"),
            ("evaluar rendimiento sql latencia lcp inp", "pat-performance-budgeting"),
            ("revisar accesibilidad teclado foco zoom WCAG", "std-ui-ux-quality-baseline"),
            ("revisión UX calidad visual motion responsive", "pb-frontend-quality-review"),
        )
        for query, expected in cases:
            with self.subTest(query=query):
                hits = search(index, query, limit=15)
                self.assertIn(expected, {hit["id"] for hit in hits}, [hit["id"] for hit in hits])
        self.assertEqual("std-privacy-data-handling-baseline", search(index, "privacidad CRM interno", limit=1)[0]["id"])
        tree = knowledge_tree(index)
        topics = {topic["id"]: {child["id"] for child in topic["children"]} for topic in tree["children"]}
        for topic, target in (
            ("quality-audit", "pb-engineering-quality-audit"),
            ("ux-ui", "pb-frontend-quality-review"),
            ("performance", "pat-performance-budgeting"),
            ("security", "pb-security-review"),
            ("privacy", "std-privacy-data-handling-baseline"),
            ("reliability", "std-production-operability-baseline"),
        ):
            with self.subTest(topic=topic):
                self.assertIn(target, topics[topic])

    def test_installed_codex_snapshot_contains_live_quality_sources_and_compiled_routes(self):
        with tempfile.TemporaryDirectory() as td:
            result = subprocess.run([
                sys.executable, "-I", str(ROOT / "automation/codex/handbook_update.py"),
                "bundle", "--source", str(ROOT), "--skills-home", td,
            ], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = Path(td) / "engineering-handbook/references"
            for path in (
                "playbooks/engineering-quality-audit.md",
                "standards/privacy-data-handling-baseline.md",
                "playbooks/security-review.md",
                "machine-readable/discovery/rules.v1.json",
                "machine-readable/compiled/discovery.json",
            ):
                with self.subTest(path=path):
                    self.assertTrue((installed / path).is_file(), path)
            run = subprocess.run([
                sys.executable, "-m", "automation.engineering_context", "search",
                "--root", str(installed), "--query", "audit security privacy performance",
            ], cwd=installed, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertIn("pb-engineering-quality-audit", run.stdout)


if __name__ == "__main__":
    unittest.main()
