import json
import re
import tempfile
import unittest
from pathlib import Path

from automation.engineering_context.cli import _load_compiled
from automation.engineering_context.context_solver import build_repo_route, solve_context
from automation.engineering_context.handbook_source import extract_agent_context
from automation.engineering_context.repo_profile import profile_repo
from automation.engineering_context.task_descriptor import describe_task


ROOT = Path(__file__).resolve().parents[2]
PROFILE = {"detected": {"capabilities": {}}}
PHASES = ("planning", "implementation", "verification")
MARKETING_ARCHETYPES = {
    "marketing-content-change", "lead-qualification", "conversion-measurement",
    "marketing-experiment", "public-discoverability-change",
}


class MarketingAdoptionTests(unittest.TestCase):
    def capsule(self, task, phase, changed=()):
        descriptor = describe_task(task, PROFILE, changed)
        compiled = _load_compiled(ROOT / "machine-readable/compiled", phase)
        return descriptor, solve_context(compiled, descriptor, phase)

    def test_new_websites_and_agent_discovery_route_the_canonical_standard(self):
        for task in (
            "Crea una web para una empresa de mudanzas",
            "Add RFC 8288 Link headers and Markdown for Agents",
            "Comprueba el registro DNS-AID de la documentación pública",
            "Publish a public API and its documentation",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertIn("std-public-web-discoverability-baseline", capsule.provenance)
                    self.assertFalse(descriptor.state["migration"])
                    if phase == "verification":
                        self.assertIn("public-agent-discovery-http-evidence", capsule.required_evidence)

    def test_private_dashboard_maintenance_does_not_route_publication(self):
        _, capsule = self.capsule("Fix keyboard navigation in the authenticated CRM dashboard", "verification")
        self.assertNotIn("public-agent-discovery-http-evidence", capsule.required_evidence)

    def test_commercial_brief_copy_and_competitor_work_route_in_both_languages(self):
        for task in (
            "Prepare product-marketing context for a local service business",
            "Improve copywriting and CRO for a quote form",
            "Redacta una propuesta comercial para una clínica",
            "Analiza la competencia y prepara un argumentario comercial",
            "Use competitor-profiling and sales-enablement",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertIn("marketing-content-change", descriptor.archetypes)
                    self.assertIn("commercial-truth", capsule.covered)
                    self.assertIn("pb-marketing-context-and-content", capsule.provenance)
                    self.assertFalse(capsule.uncovered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_prospecting_and_revops_route_permission_separately_from_priority(self):
        for task in (
            "Cualifica leads españoles de negocios locales sin web",
            "Draft a cold email for local businesses",
            "Diseña el lead scoring y las etapas de RevOps",
            "Planifica prospección comercial y seguimiento de leads",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertIn("lead-qualification", descriptor.archetypes)
                    self.assertIn("outreach-privacy", capsule.covered)
                    self.assertIn("lead-qualification-permission-boundary", {u["id"] for u in capsule.units})
                    self.assertFalse(capsule.uncovered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_measurement_and_experiments_have_phase_specific_evidence(self):
        for task in (
            "Fix conversion tracking for a contact form",
            "Mide las conversiones de WhatsApp sin confundir clic con lead",
            "Configura GA4 para solicitudes de presupuesto",
            "Design an A/B test with low traffic",
            "Diseña un experimento de marketing para una clínica",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertIn("conversion-measurement", descriptor.archetypes)
                    self.assertIn("measurement-integrity", capsule.covered)
                    self.assertIn("marketing-privacy", capsule.covered)
                    if phase == "verification":
                        self.assertIn("conversion-end-to-end-evidence", capsule.required_evidence)
                    if "marketing-experiment" in descriptor.archetypes:
                        self.assertIn("experiment-validity", capsule.covered)
                    self.assertFalse(capsule.uncovered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_seo_and_schema_use_existing_search_owner_not_database_migrations(self):
        for task in (
            "Audita el SEO y la indexación de la demo privada",
            "Improve AI SEO without changing private route access",
            "Add schema markup and JSON-LD for a local business",
            "Revisa datos estructurados y arquitectura web",
            "Use site-architecture for navigation and internal linking",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertIn("public-discoverability-change", descriptor.archetypes)
                    self.assertFalse(descriptor.state["migration"])
                    self.assertIn("search-exposure", capsule.covered)
                    self.assertIn("std-public-web-discoverability-baseline", capsule.provenance)
                    self.assertFalse(capsule.uncovered)
                    self.assertLess(capsule.estimated_tokens, 600)

    def test_database_schema_remains_a_migration_even_in_mixed_marketing_task(self):
        for task, changed in (
            ("Change the database schema", ()),
            ("Add schema markup and migrate the database schema", ()),
            ("Fix JSON-LD", ("supabase/migrations/20261109_leads.sql",)),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE, changed)
                self.assertTrue(descriptor.state["migration"])
                self.assertIn("data-loss", descriptor.risks)

    def test_natural_language_does_not_require_an_upstream_skill_name(self):
        for task, archetype in (
            ("Qualify leads for local businesses", "lead-qualification"),
            ("Track WhatsApp conversions", "conversion-measurement"),
            ("Design A/B tests for a local business", "marketing-experiment"),
            ("Prepara una prueba A/B para una web", "marketing-experiment"),
            ("Optimiza la conversión de un formulario de presupuesto", "marketing-content-change"),
            ("Edit landing page copy for a local clinic", "marketing-content-change"),
            ("Improve copy for the pricing page", "marketing-content-change"),
            ("Track contact form submissions", "conversion-measurement"),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn(archetype, descriptor.archetypes)

    def test_realistic_requests_keep_their_procedural_boundaries(self):
        for task, expected in (
            (
                "Cualifica cinco negocios españoles sin web y prepara borradores; solo sabemos los correos públicos y no hay permiso de envío acreditado.",
                {"pb-lead-qualification-and-handoff"},
            ),
            (
                "Mejora el copy de una demo dental noindex; las fotos/resultados y reseñas son de muestra, el CTA abre WhatsApp.",
                {"pb-marketing-context-and-content", "std-public-web-discoverability-baseline"},
            ),
            (
                "Mide solicitudes de presupuesto; el formulario reintenta, a veces falla el backend y casi no hay tráfico, pero quiero declarar ganadora una variante A/B esta semana.",
                {"pb-conversion-measurement-and-experiments"},
            ),
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    descriptor, capsule = self.capsule(task, phase)
                    self.assertTrue(expected.issubset(capsule.provenance), capsule.provenance)
                    self.assertFalse(capsule.uncovered)
                    route = build_repo_route(PROFILE, descriptor)
                    if "pb-lead-qualification-and-handoff" in expected:
                        self.assertIn("outreach-privacy", capsule.covered)
                        self.assertIn("channel-permission", route["inspect_first"])
                        self.assertIn("crm-owner", route["inspect_first"])
                    if "variante A/B" in task:
                        self.assertIn("marketing-experiment", descriptor.archetypes)
                        self.assertIn("experiment-validity", capsule.covered)
                        self.assertIn("measurement-integrity", capsule.covered)
                        self.assertIn("marketing-privacy", capsule.covered)
                        self.assertIn("conversion-contract", route["inspect_first"])
                        self.assertIn("experiment-contract", route["inspect_first"])
                        if phase == "verification":
                            self.assertIn("conversion-end-to-end-evidence", capsule.required_evidence)

    def test_copy_and_seo_keep_both_owners_when_truth_coverage_overlaps(self):
        for phase in PHASES:
            with self.subTest(phase=phase):
                _, capsule = self.capsule("Improve copywriting and SEO for a local clinic", phase)
                self.assertIn("pb-marketing-context-and-content", capsule.provenance)
                self.assertIn("std-public-web-discoverability-baseline", capsule.provenance)
                self.assertFalse(capsule.uncovered)
                self.assertLess(capsule.estimated_tokens, 600)

    def test_search_indexing_is_scoped_to_public_discovery(self):
        for task in (
            "Revisa la indexación de Google y Elasticsearch",
            "Revisa la indexación de mi sitio web",
            "Fix search indexing for a public website",
        ):
            with self.subTest(task=task):
                self.assertIn("public-discoverability-change", describe_task(task, PROFILE).archetypes)

    def test_changed_paths_route_context_and_search_without_guessing_private_content(self):
        for changed, archetype in (
            ((".agents/product-marketing.md",), "marketing-content-change"),
            (("docs/marketing-context.md",), "marketing-content-change"),
            (("app/robots.ts",), "public-discoverability-change"),
            (("public/sitemap.xml",), "public-discoverability-change"),
            (("src/analytics/conversions.ts",), "conversion-measurement"),
        ):
            with self.subTest(changed=changed):
                descriptor = describe_task("Update the relevant contract", PROFILE, changed)
                self.assertIn(archetype, descriptor.archetypes)

    def test_generic_engineering_and_private_glass_do_not_load_marketing(self):
        for task, changed in (
            ("Fix currency conversion rounding", ("src/currency-conversion.ts",)),
            ("Calcula conversiones de divisas", ()),
            ("Optimize the database schema", ("db/schema.sql",)),
            ("Fix React hooks in the settings page", ("src/hooks/useForm.ts",)),
            ("Improve glassmorphism in the ChurchOS admin console", ()),
            ("Refactor the lead screw calculation in a CAD tool", ()),
            ("Repair an experiment fixture for unit tests", ()),
            ("Correct a typo in the handbook", ("README.md",)),
            ("Fix the code review pipeline", ()),
            ("Tune service analytics for CPU usage", ()),
            ("Corrige la indexación de Elasticsearch", ()),
            ("Fix search indexing in PostgreSQL", ()),
            ("Optimiza la indexación de documentos en un índice interno", ()),
            ("Repara el copy constructor de una clase C++", ()),
            ("Improve the file copy command", ()),
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE, changed)
                self.assertFalse(MARKETING_ARCHETYPES & set(descriptor.archetypes))
                for phase in PHASES:
                    _, capsule = self.capsule(task, phase, changed)
                    self.assertFalse(any(p in capsule.provenance for p in (
                        "pb-marketing-context-and-content", "pb-lead-qualification-and-handoff",
                        "pb-conversion-measurement-and-experiments",
                    )))

    def test_full_website_keeps_delivery_owner_and_commercial_truth(self):
        for task in (
            "Create a website for a local painting business",
            "Haz una web para una clínica con reseñas de demo",
        ):
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    _, capsule = self.capsule(task, phase)
                    self.assertIn("pb-public-client-website-delivery", capsule.provenance)
                    self.assertIn("commercial-truth", capsule.covered)

    def test_profile_discovers_only_paths_and_respects_declared_context_owner(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / ".agents").mkdir()
            (repo / ".agents/product-marketing.md").write_text("CONFIDENTIAL CLIENT DATA", encoding="utf-8")
            profile = profile_repo(repo)
            descriptor = describe_task("Prepare product-marketing context", profile)
            route = build_repo_route(profile, descriptor)
            self.assertEqual(route["resolved"]["commercial-context"], [".agents/product-marketing.md"])
            self.assertNotIn("CONFIDENTIAL CLIENT DATA", json.dumps(profile))
            (repo / ".engineering").mkdir()
            (repo / ".engineering/context.json").write_text(json.dumps({
                "schema": "repo-context/v1",
                "landmarks": {"commercial-context": ["docs/approved-brief.md"]},
            }), encoding="utf-8")
            route = build_repo_route(profile_repo(repo), descriptor)
            self.assertEqual(route["resolved"]["commercial-context"], ["docs/approved-brief.md"])

    def test_procedural_adoption_does_not_silently_gain_normative_force(self):
        for path in (
            "playbooks/marketing-context-and-content.md",
            "playbooks/lead-qualification-and-handoff.md",
            "playbooks/conversion-measurement-and-experiments.md",
        ):
            with self.subTest(path=path):
                units = extract_agent_context((ROOT / path).read_text(encoding="utf-8"), path)
                self.assertTrue(units)
                self.assertTrue(all(u.force in ("should", "may") for u in units))

    def test_registry_and_assessment_share_an_immutable_upstream_revision(self):
        source = (ROOT / "machine-readable/sources.yaml").read_text(encoding="utf-8")
        assessment = (ROOT / "references/marketing-skills-adoption-assessment.md").read_text(encoding="utf-8")
        entry = source.split("  - id: src-marketingskills\n", 1)[1].split("  - id:", 1)[0]
        sha = re.search(r"revision: ([0-9a-f]{40})\n", entry).group(1)
        self.assertIn(sha, assessment)
        catalog = (ROOT / "machine-readable/catalog.yaml").read_text(encoding="utf-8")
        for artifact in (
            "pb-marketing-context-and-content", "pb-lead-qualification-and-handoff",
            "pb-conversion-measurement-and-experiments", "tpl-product-marketing-context",
            "ref-marketing-skills-adoption-assessment", "adr-0008-selective-marketing-skills-adoption",
        ):
            self.assertIn(f"id: {artifact}\n", catalog)
        skills = list((ROOT / "agent-config/codex/skills").glob("*/SKILL.md"))
        self.assertEqual([p.parent.name for p in skills], ["engineering-handbook"])


if __name__ == "__main__":
    unittest.main()
