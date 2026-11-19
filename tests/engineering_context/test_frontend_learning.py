import unittest
from pathlib import Path

from automation.engineering_context.cli import _load_compiled
from automation.engineering_context.context_solver import DEFAULT_BUDGET, solve_context
from automation.engineering_context.task_descriptor import describe_task


COMPILED = Path(__file__).resolve().parents[2] / "machine-readable/compiled"
PHASES = ("planning", "implementation", "verification")
PROFILE = {"detected": {"capabilities": {}}}
EDITORIAL = (
    "editorial-reading-contract",
    "editorial-reading-contract",
    "editorial-reading-verification",
)
INTERACTION = (
    "interaction-continuity-contract",
    "interaction-continuity-contract",
    "interaction-continuity-verification",
)
DESIGN = (
    "design-purpose-before-treatment",
    "design-purpose-before-treatment",
    "frontend-design-fit-review",
)
OPERATION = (
    "frontend-operation-feedback",
    "frontend-operation-feedback",
    "frontend-operation-feedback-verification",
)
THEME = (
    "theme-continuity-contract",
    "theme-continuity-contract",
    "theme-continuity-verification",
)
HERO = (
    "marketing-hero-brief-and-source",
    "marketing-hero-photo-fidelity",
    "marketing-hero-live-acceptance",
)
SCENARIOS = (
    ("A", "Crea una web para consultar un reglamento extenso con tablas y una versión imprimible.", (EDITORIAL,)),
    ("B", "Diseña una landing con un hero visual y animaciones.", (HERO, DESIGN, INTERACTION)),
    ("C", "Crea un índice dinámico con navegación por anclas y seguimiento de lectura.", (EDITORIAL,)),
    ("D", "Implementa un toggle light/dark animado, interrumpible y accesible.", (THEME, INTERACTION)),
    ("E", "Diseña un panel administrativo con altas, bajas, filtros y feedback de guardado.", (OPERATION, DESIGN)),
    ("F", "Audita una web con demasiadas tarjetas, colores, efectos y textos genéricos.", (DESIGN,)),
    ("G", "Corrige un dropdown que falla al alternar hover, clic y teclado.", (INTERACTION,)),
    ("H", "Revisa una interfaz que supera pruebas funcionales pero tiene una experiencia visual mediocre.", (DESIGN,)),
)
MOBILE_CAPTURE = "mobile-keyboard-capture-loop"
MOBILE_OVERLAY = "mobile-one-routine-overlay"
FILTER = "ui-filter-selection-truth"
TEMPORAL = "visual-evidence-temporal-input"
PROVENANCE = "visual-evidence-bind-provenance"
TARGETED = set(EDITORIAL + INTERACTION + DESIGN + OPERATION + THEME)


class FrontendLearningTests(unittest.TestCase):
    def test_unslop_and_material_redesign_receive_design_context_in_every_phase(self):
        tasks = (
            "Unslop this dashboard.",
            "Apply anti-slop to the settings screen.",
            "Elimina el AI slop de esta pantalla.",
            "Quita el aspecto generado por IA de esta interfaz.",
            "Review this AI-looking interface.",
            "Audita el diseño de esta pantalla con Unslop, sin editarla.",
            "Haz un rediseño agresivo de Ops OS.",
            "Redesign MelodIQ Core.",
            "Unslop Church OS.",
            "Unslop Core.",
            "Replantea la composición de DentalOS.",
            "Polish this interface.",
            "Refine the layout of the onboarding screen.",
            "Pule la interfaz de este producto.",
            "Rediseña las pantallas del panel.",
            "Redesign a settings screen backed by a SQL API.",
            "Audit this dashboard for AI slop; do not change it.",
            "Redesign this dashboard and fix a typo in the title.",
            "Do not redesign the API, redesign the UI.",
            "Without redesigning it, audit this dashboard for AI slop.",
            "Rediseña este panel y corrige una errata en el título.",
            "No rediseñes la API, rediseña la interfaz.",
            "Unslop this console.",
            "Rediseña las aplicaciones internas.",
            "Sin rediseñar esta pantalla, revisa su calidad visual.",
            "Redesign the website and fix a typo.",
            "Fix SQL query and remove AI slop from this dashboard.",
            "Revisa la UI del portal de documentación con Unslop.",
            "Review the interface of this documentation portal using Unslop.",
            "Read the UI and apply Unslop to the dashboard.",
        )
        for task in tasks:
            descriptor = describe_task(task, PROFILE)
            with self.subTest(task=task):
                self.assertIn("frontend", descriptor.surfaces)
                self.assertIn("design-fit", descriptor.archetypes)
                self.assertIn("design-fit", descriptor.risks)
            for index, phase in enumerate(PHASES):
                with self.subTest(task=task, phase=phase):
                    capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                    ids = {unit["id"] for unit in capsule.units}
                    self.assertIn(DESIGN[index], ids)
                    self.assertIn("ui-design-reconstruction", ids)
                    self.assertFalse(capsule.uncovered)
                    self.assertLessEqual(capsule.estimated_tokens, DEFAULT_BUDGET.target)
                    if phase == "verification":
                        self.assertIn(PROVENANCE, ids)
                        self.assertIn(DESIGN[index], capsule.required_evidence)

    def test_unslop_mentions_backend_tasks_and_micro_edits_do_not_request_redesign(self):
        tasks = (
            "Document the Unslop license.",
            "Revisa la licencia de Unslop antes de usarlo en Ops OS.",
            "Read Unslop documentation for dashboard examples.",
            "Read the Unslop hero documentation.",
            "Unslop docs for the homepage.",
            "Update the anti-slop README for the UI team.",
            "Instala la skill Unslop para Codex en MelodIQ Core.",
            "Install Unslop for future dashboard work.",
            "Explain how Unslop redesigns a screen.",
            "Documenta cómo Unslop rediseña una pantalla.",
            "Design an API for a React app.",
            "Redesign the SQL API backing Ops OS.",
            "Unslop the backend API for Church OS.",
            "Refine the database schema in DentalOS.",
            "Polish SQL queries for the dashboard.",
            "Unslop MelodIQ Core backend.",
            "Polish the core library.",
            "Polish the core algorithm.",
            "Redesign core modules.",
            "Do not apply Unslop to this screen; fix the backend API.",
            "No apliques Unslop a la interfaz; corrige solo SQL.",
            "Polish the dashboard API.",
            "Unslop the dashboard API.",
            "Remove AI slop from backend code for the interface.",
            "Tighten the spacing on a single settings button.",
            "Polish only the border radius of one button in this interface.",
            "Corrige solo el margen de un botón, sin rediseñar esta pantalla.",
            "Fix a typo in this screen without redesigning the interface.",
            "Fix only a typo in the hero, no redesign.",
            "Corrige solo el padding del hero.",
            "Fix a typo in the public website hero without redesigning it.",
            "No rediseñes Ops OS; corrige un margen.",
            "Do not redesign this dashboard; fix only one icon.",
            "Polish the copy of the Unslop installation guide.",
            "Review the UI documentation for Unslop.",
        )
        for task in tasks:
            descriptor = describe_task(task, PROFILE)
            with self.subTest(task=task):
                self.assertNotIn("design-fit", descriptor.archetypes)
                self.assertNotIn("design-fit", descriptor.risks)
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                    ids = {unit["id"] for unit in capsule.units}
                    self.assertFalse((set(DESIGN) | {"ui-design-reconstruction"}) & ids, ids)

    def test_visual_routing_does_not_grant_mutation_or_release_authority(self):
        for task in (
            "Unslop Ops OS.",
            "Audit MelodIQ Core with Unslop, read only.",
            "Without redesigning it, audit this dashboard for AI slop.",
            "Sin rediseñar esta pantalla, revisa su calidad visual.",
        ):
            with self.subTest(task=task):
                descriptor = describe_task(task, PROFILE)
                self.assertIn("design-fit", descriptor.risks)
                self.assertNotIn("mutation", descriptor.operations)
                self.assertNotIn("deployment", descriptor.operations)
                self.assertFalse(descriptor.delivery["production_effect"])
                self.assertFalse(descriptor.state["durable_change"])

    def test_bounded_visual_edits_keep_the_accessibility_baseline(self):
        for task in (
            "Corrige solo el padding del hero.",
            "Fix a typo in this screen without redesigning the interface.",
            "Corrige solo el margen de un botón, sin rediseñar esta pantalla.",
        ):
            descriptor = describe_task(task, PROFILE)
            with self.subTest(task=task):
                self.assertIn("frontend", descriptor.surfaces)
                self.assertIn("accessibility", descriptor.risks)
                self.assertNotIn("design-fit", descriptor.risks)
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                    ids = {unit["id"] for unit in capsule.units}
                    self.assertIn("ui-accessibility-baseline", ids)
                    self.assertFalse((set(DESIGN) | {"ui-design-reconstruction"}) & ids, ids)

    def test_eight_tasks_receive_their_contract_at_each_stage(self):
        for label, task, contracts in SCENARIOS:
            descriptor = describe_task(task, PROFILE)
            for index, phase in enumerate(PHASES):
                with self.subTest(scenario=label, phase=phase):
                    capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                    ids = {unit["id"] for unit in capsule.units}
                    expected = {contract[index] for contract in contracts}
                    self.assertTrue(expected.issubset(ids), ids)
                    self.assertFalse(capsule.uncovered)
                    self.assertLessEqual(capsule.estimated_tokens, DEFAULT_BUDGET.target)
                    self.assertFalse({MOBILE_CAPTURE, MOBILE_OVERLAY} & ids)
                    self.assertFalse({"pb-public-client-website-delivery", "pat-operator-console-shell-interactions"} & set(capsule.provenance))
                    self.assertEqual("pat-public-marketing-hero-motion" in capsule.provenance, label == "B")
                    self.assertEqual(FILTER in ids, label == "E" and phase != "planning")
                    if phase == "verification":
                        self.assertTrue(expected.issubset(capsule.required_evidence))
                        self.assertEqual(TEMPORAL in ids, INTERACTION in contracts)
                        self.assertEqual(PROVENANCE in ids, DESIGN in contracts)

    def test_unrelated_tasks_do_not_receive_the_new_guidance(self):
        tasks = (
            "Fix dynamic indexes in PostgreSQL.",
            "Corrige el índice dinámico de la base de datos.",
            "Edit the table of contents in a Markdown manual.",
            "Read the handbook before reviewing the React UI.",
            "Design an API for a React app.",
            "Improve database filters in a PostgreSQL table.",
            "Trace backend mutation feedback and retry in the API.",
            "Tighten the spacing on a single settings button.",
        )
        for task in tasks:
            descriptor = describe_task(task, PROFILE)
            for phase in PHASES:
                with self.subTest(task=task, phase=phase):
                    capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                    ids = {unit["id"] for unit in capsule.units}
                    self.assertFalse((TARGETED | {MOBILE_CAPTURE, MOBILE_OVERLAY, FILTER}) & ids, ids)

    def test_english_tasks_and_adjacent_owners_keep_their_intent(self):
        cases = (
            ("Build a website for reading a printable manual with tables.", "planning",
             {"editorial-reading-contract"}, {"public-client-website-brief", "marketing-hero-brief-and-source"}),
            ("Build a website for a repair business with a guide to its services.", "planning",
             {"public-client-website-brief", "design-purpose-before-treatment"}, {"editorial-reading-contract"}),
            ("Crea un sitio web de documentación técnica para el producto.", "planning",
             {"editorial-reading-contract"}, {"public-client-website-brief"}),
            ("Design an onboarding screen for returning customers.", "planning",
             {"design-purpose-before-treatment"}, {"public-client-website-brief"}),
            ("Design a settings screen backed by an API.", "planning",
             {"design-purpose-before-treatment"}, {"public-client-website-brief"}),
            ("Improve the homepage hero for a site to read regulations.", "planning",
             {"editorial-reading-contract"}, {"marketing-hero-brief-and-source"}),
            ("Create an interactive handbook with a sticky table of contents.", "verification",
             {"editorial-reading-verification"}, {"public-client-website-live-handoff"}),
            ("Corrige el buscador que devuelve otra semana para la consulta semana 6.", "implementation",
             {"editorial-reading-contract"}, {"public-client-website-implementation"}),
            ("Fix dark mode and theme transition in DentalOS.", "verification",
             {"theme-continuity-verification", "operator-console-shell-live-acceptance", TEMPORAL}, set()),
            ("Review the visual hierarchy of a checkout interface.", "verification",
             {"frontend-design-fit-review", PROVENANCE}, {"marketing-hero-live-acceptance"}),
            ("Fix the dropdown when switching between pointer and keyboard.", "verification",
             {"interaction-continuity-verification", TEMPORAL}, {MOBILE_CAPTURE, MOBILE_OVERLAY}),
            ("Design an admin dashboard with filters and save confirmation.", "verification",
             {"frontend-operation-feedback-verification", FILTER}, {"operator-console-shell-live-acceptance"}),
            ("Fix checklist controls without JavaScript.", "verification",
             {"interaction-continuity-verification"}, {"editorial-reading-verification"}),
            ("Fix mobile search and the keyboard capture loop.", "implementation",
             {MOBILE_CAPTURE}, {MOBILE_OVERLAY, FILTER}),
            ("Fix the mobile dialog overlay.", "implementation", {MOBILE_OVERLAY}, {MOBILE_CAPTURE, FILTER}),
            ("Repair the filters on the orders list.", "verification",
             {FILTER}, {MOBILE_CAPTURE, MOBILE_OVERLAY, "frontend-operation-feedback-verification"}),
            ("Measure the performance of the animated landing hero.", "verification",
             {"performance-measure-before-optimization", TEMPORAL}, {"marketing-hero-live-acceptance", "marketing-hero-photo-fidelity"}),
        )
        for task, phase, expected, unwanted in cases:
            with self.subTest(task=task, phase=phase):
                descriptor = describe_task(task, PROFILE)
                capsule = solve_context(_load_compiled(COMPILED, phase), descriptor, phase)
                ids = {unit["id"] for unit in capsule.units}
                self.assertTrue(expected.issubset(ids), ids)
                self.assertFalse(unwanted & ids, ids)
                self.assertFalse(capsule.uncovered)
