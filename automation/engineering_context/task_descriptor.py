from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .canonical import stable_hash

EVIDENCE_RANK={"explicit-structured":600,"declared-decision":500,"repo-structure":400,"change-structure":350,"text-signal":200,"agent-resolution":150}
PATH_SIGNALS={
    "surface:database":("migrations/","schema",".sql"),
    "surface:ci":(".github/workflows/",),
    "risk:authorization":("policy","policies","permission","authz","rls"),
    "risk:credential":("token","secret","invite","credential"),
    "capability:pwa":("manifest.webmanifest","service-worker","sw.js"),
}

@dataclass(frozen=True)
class TaskDescriptor:
    intent: tuple[str,...]=()
    surfaces: tuple[str,...]=()
    operations: tuple[str,...]=()
    capabilities: tuple[str,...]=()
    risks: tuple[str,...]=()
    state: dict[str,Any]|None=None
    boundaries: dict[str,Any]|None=None
    delivery: dict[str,Any]|None=None
    archetypes: tuple[str,...]=()
    uncertain: tuple[dict[str,Any],...]=()
    evidence: tuple[dict[str,Any],...]=()
    task_text: str=""
    id: str=""

    def __post_init__(self):
        if self.state is None: object.__setattr__(self,"state",{})
        if self.boundaries is None: object.__setattr__(self,"boundaries",{})
        if self.delivery is None: object.__setattr__(self,"delivery",{})
        if not self.id:
            object.__setattr__(self,"id",stable_hash(self.to_dict(include_id=False)))

    def to_dict(self, include_id: bool=True)->dict[str,Any]:
        d={"intent":list(self.intent),"surfaces":list(self.surfaces),"operations":list(self.operations),"capabilities":list(self.capabilities),"risks":list(self.risks),"state":self.state,"boundaries":self.boundaries,"delivery":self.delivery,"archetypes":list(self.archetypes),"uncertain":[dict(x) for x in self.uncertain],"evidence":[dict(x) for x in self.evidence],"task_text":self.task_text}
        if include_id:d["id"]=self.id
        return d

    @classmethod
    def for_test(cls, risks: tuple[str,...]=(), surfaces: tuple[str,...]=(), operations: tuple[str,...]=(), capabilities: tuple[str,...]=(), migration: bool=False, **kwargs):
        return cls(intent=("modify",),surfaces=surfaces,operations=operations,capabilities=capabilities,risks=risks,state={"migration":migration},boundaries={},delivery={},task_text="test",**kwargs)

    def predicates(self)->set[str]:
        out={f"intent:{x}" for x in self.intent}|{f"surface:{x}" for x in self.surfaces}|{f"operation:{x}" for x in self.operations}|{f"capability:{x}" for x in self.capabilities}|{f"risk:{x}" for x in self.risks}|{f"archetype:{x}" for x in self.archetypes}
        if self.state.get("migration"):out.add("state:migration")
        if self.boundaries.get("privileged"):out.add("boundary:privileged")
        if self.boundaries.get("external"):out.add("boundary:external")
        if self.delivery.get("production_effect"):out.add("delivery:production")
        return out

def _sorted(items:set[str])->tuple[str,...]: return tuple(sorted(items))

def _evidence(bucket:list[dict[str,Any]], source:str, signal:str, value:str):
    bucket.append({"source":source,"rank":EVIDENCE_RANK[source],"signal":signal,"value":value})

def _frontend_quality_signals(text: str) -> dict[str, str | None]:
    interface = re.search(
        r"\b(?:ui|ux|interface|interfaz|web|website|landing|hero|homepage|bot[oó]n|button|"
        r"dialog|modal|drawer|menu|men[uú]|dashboard|panel administrativo|crm|scroll|"
        r"page|p[aá]gina|site|route transition)\b",
        text,
    )
    reading_surface = re.search(
        r"\b(?:web(?:site)?|sitio(?: web)?|p[aá]gina|site|portal|reader|lector)"
        r"(?: (?:p[uú]blic[oa]|public|interactiv[oa]|interactive))?\s+(?:para|to|for|de|of)\s+"
        r"(?:(?:consultar|leer|navegar|browse|read(?:ing)?|consult|navigate)\s+)?"
        r"(?:(?:un|una|el|la|los|las|a|an|the|printable|online|technical|digital)\s+){0,3}"
        r"(?:reglamentos?|normativas?|manual(?:es)?|procedimientos?|documentaci[oó]n|"
        r"gu[ií]as?|regulations?|rulebooks?|handbooks?|manuals?|procedures?|documentation|guides?)\b",
        text,
    )
    reading_navigation = re.search(
        r"\b(?:navegaci[oó]n por anclas|"
        r"seguimiento de lectura|volver a (?:la |mi )?[uú]ltima lectura|"
        r"sticky (?:index|table of contents)|anchor navigation|reading (?:position|progress)|resume reading|"
        r"interactive (?:document(?:ation)?|manual|handbook)|(?:documentaci[oó]n|manual) interactiv[oa])\b",
        text,
    )
    document_query = re.search(
        r"\b(?:search|b[uú]squeda|buscador)\b.{0,50}\b(?:week|semana|chapter|cap[ií]tulo|apartado)\s+\d+\b",
        text,
    )
    reading = reading_surface or reading_navigation or document_query or (
        interface and re.search(
            r"\b(?:table of contents|[ií]ndice (?:del documento|din[aá]mico)|printable (?:manual|regulations?|handbook))\b",
            text,
        )
    )
    theme = re.search(
        r"\b(?:light\s*[/–-]\s*dark|dark\s*[/–-]\s*light|dark mode|light mode|"
        r"modo oscuro|modo claro|theme (?:switch|toggle|control|transition|change)|"
        r"(?:cambio|selector|alternador|transici[oó]n) de tema)\b",
        text,
    )
    control = re.search(r"\b(?:dropdown|disclosure|popover|men[uú] desplegable|search results?|resultados de b[uú]squeda)\b", text)
    competing_input = re.search(r"\b(?:hover|puntero|pointer|t[aá]ctil|touch|teclado|keyboard|scroll|foco|focus|clic|click)\b", text)
    motion = re.search(r"\b(?:animaci[oó]n|animaciones|animad[oa]s?|animations?|animated|motion|transiciones?|transitions?)\b", text)
    feedback = re.search(
        r"\b(?:feedback (?:de guardado|al guardar)|confirmaci[oó]n (?:de guardado|al guardar)|"
        r"(?:save|submission|mutation) (?:feedback|confirmation)|feedback (?:after|on) (?:saving|submission)|"
        r"estados? de guardado)\b",
        text,
    )
    backend_context = re.search(r"\b(?:sql|database|backend|api|postgresql|elasticsearch|base de datos)\b", text)
    collection = (interface or not backend_context) and re.search(
        r"\b(?:ui|interface|interfaz|pantalla|dashboard|crm|panel|list(?:a|ado)?|"
        r"tabl[ae]s?|collection|colecci[oó]n|search results?|resultados de b[uú]squeda)\b",
        text,
    )
    filters = re.search(r"\b(?:filters?|filtr(?:os?|ar|ad[oa]s?))\b", text)
    mobile = re.search(r"\b(?:mobile|m[oó]vil(?:es)?|ios|android|touch|t[aá]ctil)\b", text)
    capture = re.search(
        r"\b(?:keyboard|teclado|forms?|formularios?|capture|captura|search|b[uú]squeda|scanner|esc[aá]ner|ime)\b",
        text,
    )
    overlay = re.search(
        r"\b(?:modals?|drawers?|sheets?|overlays?|di[aá]logos?|dialogs?|popovers?|men[uú] desplegable|dropdown)\b",
        text,
    )
    design = re.search(
        r"\b(?:ai slop|visual quality|calidad visual|jerarqu[ií]a visual|direcci[oó]n art[ií]stica|"
        r"art direction|visual hierarchy|experiencia visual|visual experience|generic (?:copy|layout|design)|"
        r"(?:textos?|dise[ñn]o) gen[eé]ric[oa]s?|(?:demasiadas|exceso de) tarjetas|too many cards)\b",
        text,
    )
    new_composition = re.search(
        r"\b(?:diseñ(?:a|ar)|rediseñ(?:a|ar)|(?:re)?design)\s+"
        r"(?:(?!(?:api|backend|database|sql|base de datos)\b)\w+[\s-]+){0,4}"
        r"(?:web|website|site|p[aá]gina|landing|screen|pantalla|interface|interfaz|app|"
        r"aplicaci[oó]n|dashboard|panel|consola|crm)\b",
        text,
    )
    record_action = re.search(r"\b(?:crud|altas|bajas|guardar|saving|archive|delete|create records?)\b", text)
    scripted_control = re.search(r"\b(?:checklists?|listas? de verificaci[oó]n|progress bars?|barras? de progreso)\b", text)
    scripting_fallback = re.search(r"\b(?:no[- ]js|without (?:scripts?|javascript)|sin (?:scripts?|javascript))\b", text)
    visual_review = re.search(r"\b(?:visual|layout|dise[ñn]o|design)\b", text)
    signals = (
        (reading, "editorial-reading", "editorial-reading"),
        (theme, "theme-change", "theme-continuity"),
        (theme or (control and competing_input) or (motion and (interface or control))
         or (scripted_control and scripting_fallback), "interaction-continuity", "interaction-continuity"),
        ((feedback and (interface or not backend_context)) or (collection and filters and record_action),
         "operation-feedback", "operation-feedback"),
        (collection and filters, "collection-filter-change", None),
        (mobile and capture, "mobile-input-flow", None),
        (mobile and overlay, "mobile-overlay-change", None),
        ((design and (interface or visual_review)) or new_composition, "design-fit", "design-fit"),
    )
    return {archetype: risk for matched, archetype, risk in signals if matched}


def describe_task(task_text: str, repo_profile: dict, changed_paths: tuple[str,...]=()) -> TaskDescriptor:
    text=task_text.lower()
    intent={"modify"}; surfaces=set(); operations=set(); capabilities=set(); risks=set(); archetypes=set(); evidence=[]; uncertain=[]
    state={"durable_change":False,"migration":False}; boundaries={"external":False,"privileged":False}; delivery={"production_effect":False}
    detected=repo_profile.get("detected",{})
    caps=detected.get("capabilities",{})
    for c,v in caps.items():
        if v: _evidence(evidence,"repo-structure",f"repo-capability:{c}","true")

    # Agent extensions can execute with the host's authority. Keep these signals
    # specific: React hooks, webhooks, ECC cryptography and memory leaks are not
    # agent-tooling or learned-authority changes.
    host_pattern = r"(?:codex|claude(?: code)?|coding agents?|agentes? de c[oó]digo)"
    extension_pattern = r"(?:plugins?|hooks?|skills?|configuration|config|settings|configuraci[oó]n)"
    agent_host = bool(re.search(rf"\b{host_pattern}\b", text))
    # Relate the extension to its host, not merely two words anywhere in a
    # sentence (e.g. React hooks in a dashboard named Codex).
    extension_text = re.sub(r"\b(?:react|preact)[ -]hooks?\b", "", text)
    host_extension = re.search(
        rf"\b{host_pattern}(?:['’]s)?\s+{extension_pattern}\b|"
        rf"\b{extension_pattern}\s+(?:de|del|for|of|para|to|in|en)\s+(?:the\s+)?{host_pattern}\b|"
        rf"\b(?:configure|configurar|configura|install|instalar|instala)\s+{host_pattern}\b",
        extension_text,
    )
    ecc_workflow = "everything-claude-code" in text or "affaan-m/ecc" in text or (
        re.search(r"\becc\b", text) and any(w in text for w in ("coding workflow", "agent workflow", "flujo de agentes", "claude", "codex"))
    )
    if re.search(r"\bmcp\b", text) or host_extension or ecc_workflow or any(w in text for w in ("agent plugin", "agent hook", "agent skill", "plugin de agente", "hook de agente", "skill de agente")):
        archetypes.add("agent-tooling-change"); risks.add("agent-execution")
        _evidence(evidence, "text-signal", "archetype", "agent-tooling-change")
    agent_learning_context = agent_host or ecc_workflow or re.search(r"\b(?:agents?|agentes?)\b", text)
    memory_signal = re.search(r"\b(?:memory|memories|memoria|memorias)\b", text) and not any(w in text for w in ("memory leak", "memory usage", "fuga de memoria", "consumo de memoria"))
    learning_signal = any(w in text for w in ("continuous-learning", "continuous learning", "aprendizaje continuo", "learned rules", "reglas aprendidas", "learned instincts"))
    if (agent_learning_context and (memory_signal or learning_signal)) or "continuous-learning-v2" in text:
        archetypes.add("agent-learning-change"); risks.add("learned-authority")
        _evidence(evidence, "text-signal", "archetype", "agent-learning-change")

    if any(w in text for w in ("spacing","layout","visual","screen","button","card","ux","ui")):
        surfaces.add("frontend"); archetypes.add("ui-flow-change"); _evidence(evidence,"text-signal","surface","frontend")
    quality_signals = _frontend_quality_signals(text)
    if quality_signals:
        surfaces.add("frontend")
        archetypes.add("ui-flow-change")
    for archetype, risk in quality_signals.items():
        archetypes.add(archetype)
        _evidence(evidence, "text-signal", "archetype", archetype)
        if risk:
            risks.add(risk)
    editorial = "editorial-reading" in quality_signals
    # The front page of a reading surface can need a different hierarchy from a marketing hero.
    explicit_marketing_surface = re.search(
        r"\b(?:landing(?: page)?|marketing website|client website|business website|web corporativa)\b", text
    )
    generic_home = any(w in text for w in ("homepage", "home page", "public website", "página web", "página de inicio"))
    if explicit_marketing_surface or (not editorial and (generic_home or re.search(r"\bhero\b", text))):
        surfaces.add("frontend")
        archetypes.update(("ui-flow-change", "marketing-hero-change"))
        risks.update(("hero-fidelity", "design-fit"))
        _evidence(evidence, "text-signal", "archetype", "marketing-hero-change")
    # A console shell is more specific than generic UI/marketing work. Restrict it
    # to operator/admin contexts or a standalone navigation rail, never public sites.
    operator_scope = any(w in text for w in (
        "consola", "console", "panel administrativo", "panel de administr",
        "admin panel", "admin dashboard", "administrative dashboard", "backoffice",
        "back office", "operator workspace", "workspace administrativo",
        "melodiq core", "melodiq-core", "dentalos", "dental os",
        "churchos", "church os", "ops os", "opsos", "agurto os", "b2b-platform",
    ))
    rail_signal = any(w in text for w in (
        "sidebar", "side bar", "side-bar", "barra lateral", "menú lateral",
        "menu lateral", "navigation rail", "nav rail",
    ))
    shell_signal = rail_signal or any(w in text for w in (
        "dark mode", "light mode", "modo oscuro", "modo claro",
        "theme toggle", "theme switch", "theme control", "cambio de tema",
        "selector de tema", "alternador de tema", "header",
        "shell", "cambio de pantalla", "cambios de pantalla",
        "transición de pantalla", "transiciones de pantalla",
        "transición entre pantallas", "transiciones entre pantallas",
        "transicion entre pantallas", "transiciones entre rutas",
        "transición entre rutas", "route transition", "route-stage",
        "screen transition", "screen change",
    ))
    new_console = operator_scope and any(w in text for w in (
        "nueva", "nuevo", "crear", "diseña", "diseñar", "desarroll",
        "implement", "build", "design", "create", "new ", "montar",
    ))
    public_surface = any(w in text for w in (
        "public website", "public site", "marketing website", "landing page",
        "web corporativa", "blog corporativo", "sitio público", "web pública",
        "página pública", "uribe villa", "uribevilla", "mudanzasagurto",
    ))
    # Complete public-site work is a distinct archetype from an isolated hero,
    # sidebar, review or backend change. Route the website delivery playbook
    # automatically for creation/redesign briefs in either language, but keep
    # authenticated operator surfaces out even if a prompt says "web".
    public_website_signal = public_surface or any(w in text for w in (
        "web para", "web de empresa", "web de servicios", "página web",
        "pagina web", "sitio web para", "website for", "client website",
        "business website", "service website", "commercial website",
    ))
    whole_site_action = any(w in text for w in (
        "haz una web", "hacer una web", "crea una web", "crear una web",
        "monta una web", "montar una web", "nueva web", "nuevo sitio",
        "new website", "build a website", "build a site", "create a website",
        "website redesign", "rediseñar la web", "rediseña la web",
        "redesign the website", "complete the website", "termina la web",
        "completa la web", "desarrolla la web", "diseña la web",
    )) or (
        public_website_signal and any(w in text for w in (
            "create", "build", "crea", "crear", "construir", "construye",
            "diseña", "diseñar", "desarrolla", "monta", "montar",
            "rediseña", "rediseñar", "redesign", "rebuild",
        ))
    )
    if whole_site_action and public_website_signal and (public_surface or not operator_scope) and (not editorial or explicit_marketing_surface):
        surfaces.add("frontend")
        archetypes.update(("ui-flow-change", "public-client-website"))
        risks.update(("hero-fidelity", "commercial-truth", "design-fit"))
        _evidence(evidence, "text-signal", "archetype", "public-client-website")

    # Commercial procedures are opt-in by task, not ambient rules for all UI,
    # analytics or CRM work. A lead screw, currency conversion and code review
    # are deliberately not marketing signals.
    copy_text = re.sub(r"\b(?:copy constructor|file copy command)\b", "", text)
    commercial_copy = re.search(r"\b(?:el copy|(?:website|marketing|ad|sales) copy|copy (?:for|on) (?:the |a )?(?:pricing|landing|home|service|product) page)\b", copy_text)
    if commercial_copy or re.search(r"\b(?:product-marketing|copywriting|copy-editing|cro|competitor-profiling|sales-enablement)\b", text) or any(w in text for w in (
        "marketing context", "contexto comercial", "propuesta comercial",
        "argumentario comercial", "competitor analysis", "análisis de competencia",
        "analiza la competencia", "conversion rate optimization", "landing copy",
        "optimización de conversiones", "optimiza la conversión", "posicionamiento comercial",
        "landing page copy", "redacción comercial",
    )):
        archetypes.add("marketing-content-change"); risks.update(("commercial-truth", "message-fit"))
        _evidence(evidence, "text-signal", "archetype", "marketing-content-change")
    qualify_business = re.search(r"\b(?:cualificar?|cualificaci[oó]n|calificar?|calificaci[oó]n|qualify|qualifying|qualification)\b.{0,64}\b(?:leads?|negocios|empresas|prospectos?|business(?:es)?|prospects?)\b", text)
    if qualify_business or re.search(r"\b(?:prospecting|prospecci[oó]n|revops|cold[- ]email|lead[- ]scoring|lead[- ]qualification)\b", text) or any(w in text for w in (
        "cualifica leads", "cualificación de leads", "calificación de leads",
        "seguimiento de leads", "sales handoff", "lead handoff", "qualify leads",
    )):
        archetypes.add("lead-qualification"); risks.add("outreach-privacy")
        _evidence(evidence, "text-signal", "archetype", "lead-qualification")
    experiment_signal = bool(re.search(r"\ba/b[- ]test(?:s|ing)?\b|\bab-testing\b|\b(?:pruebas?|experimentos?|tests?|variantes?|variants?) a/b\b", text)) or any(w in text for w in (
        "experimento de marketing", "experimento de conversión", "marketing experiment",
    ))
    if experiment_signal:
        archetypes.add("marketing-experiment"); risks.add("experiment-validity")
        _evidence(evidence, "text-signal", "archetype", "marketing-experiment")
    channel_conversions = re.search(r"\b(?:whatsapp|phone|form|checkout|lead) conversions?\b|\bconversiones de (?:whatsapp|formularios?|leads?|presupuestos?|compras)\b", text)
    measure_requests = re.search(r"\b(?:mide|medir|medici[oó]n|track|measure|count)\b.{0,64}\b(?:solicitudes? de presupuesto|quote requests?|(?:contact )?form submissions?)\b", text)
    if experiment_signal or channel_conversions or measure_requests or re.search(r"\b(?:conversion[- ]tracking|ga4)\b", text) or any(w in text for w in (
        "medición de conversiones", "medir conversiones",
        "conversion measurement", "marketing analytics", "analítica de marketing",
        "analytics event", "evento de conversión", "attribution tracking",
    )):
        archetypes.add("conversion-measurement"); risks.update(("measurement-integrity", "marketing-privacy"))
        _evidence(evidence, "text-signal", "archetype", "conversion-measurement")
    # Indexing by itself is also a database/internal-search operation. Require
    # public discovery context, while preserving explicit SEO/robots signals.
    public_indexing = re.search(r"\b(?:indexaci[oó]n|indexing)\b", text) and re.search(r"\b(?:google|bing|web|website|public site|sitio web|search console|buscadores)\b", text)
    search_signal = public_indexing or bool(re.search(r"\b(?:seo|noindex|sitemap|robots\.txt|json-ld|schema\.org|site-architecture)\b", text)) or any(w in text for w in (
        "schema markup", "datos estructurados", "structured data", "arquitectura web",
        "internal linking", "enlazado interno",
    ))
    agent_discovery_signal = bool(re.search(r"\b(?:rfc\s*8288|dns-aid|llms\.txt|text/markdown|markdown for agents|agent discoverability|http link headers)\b", text)) or any(w in text for w in (
        "public documentation", "documentación pública", "public api", "api pública",
        "public agent service", "servicio público de agentes", "descubrimiento de agentes",
    ))
    if search_signal or agent_discovery_signal or "public-client-website" in archetypes:
        archetypes.add("public-discoverability-change"); risks.update(("search-exposure", "commercial-truth"))
        _evidence(evidence, "text-signal", "archetype", "public-discoverability-change")

    # Targeted components still receive their own pattern without requiring
    # the entire site playbook. Do not confuse "code review" with testimonials.
    if not operator_scope and any(w in text for w in (
        "galería", "galeria", "gallery", "interactive selector",
        "image accordion", "selector de imágenes", "selector de imagenes",
    )):
        surfaces.add("frontend")
        archetypes.add("public-site-gallery")
        _evidence(evidence, "text-signal", "archetype", "public-site-gallery")
    if not operator_scope and any(w in text for w in (
        "reseñas", "resenas", "opiniones de clientes", "testimonials",
        "testimonial", "google reviews", "review marquee", "review cards",
    )):
        surfaces.add("frontend")
        archetypes.add("public-site-reviews")
        _evidence(evidence, "text-signal", "archetype", "public-site-reviews")
    if not public_surface and ((operator_scope and (shell_signal or (new_console and "operation-feedback" not in quality_signals))) or rail_signal):
        surfaces.add("frontend"); archetypes.update(("ui-flow-change", "operator-console-shell-change"))
        risks.add("console-shell-fidelity")
        _evidence(evidence, "text-signal", "archetype", "operator-console-shell-change")
    # Glass is an optional operator material, not a default for public websites
    # or every console shell. Route only when requested in a relevant context.
    glass_signal = any(w in text for w in (
        "glassmorphism", "glass morphism", "frosted glass",
        "efecto cristal", "efecto vidrio", "vidrio esmerilado",
    ))
    glass_operator_scope = operator_scope or any(w in text for w in (
        "crm interno", "crm internal", "internal crm", "app interna",
        "aplicación interna", "internal app", "internal workspace",
    ))
    if glass_signal and glass_operator_scope and not public_surface:
        surfaces.add("frontend"); archetypes.update(("ui-flow-change", "operator-glass-material-change"))
        risks.add("glass-material-fidelity")
        _evidence(evidence, "text-signal", "archetype", "operator-glass-material-change")
    if any(w in text for w in ("accessibility","a11y","keyboard","focus","reflow","wcag")):
        surfaces.add("frontend"); risks.add("accessibility"); _evidence(evidence,"text-signal","risk","accessibility")
    if any(w in text for w in ("performance","latency","slow","lcp","inp","cls","core web vitals")) or (
        "interaction-continuity" in quality_signals and re.search(r"\b(?:rendimiento|fluidez|fotogramas|frame pacing|jank)\b", text)
    ):
        risks.add("performance"); _evidence(evidence,"text-signal","risk","performance")
    if any(w in text for w in ("backend","server","mutation","update","create","delete","archive")):
        surfaces.add("backend")
    if any(w in text for w in ("authenticated","permission","role","tenant")):
        operations.add("authorization"); capabilities.add("auth"); risks.add("authorization"); boundaries["privileged"]=True
    if "tenant" in text:
        risks.add("tenant-isolation")
    if any(w in text for w in ("integration","webhook","api provider","external")):
        operations.add("integration"); boundaries["external"]=True; archetypes.add("external-integration"); risks.update(("availability","compatibility"))
    if any(w in text for w in ("deploy","release","production")):
        operations.add("deployment"); delivery["production_effect"]=True; archetypes.add("production-release"); risks.update(("availability","compatibility"))
    # Remove only explicit search-markup phrases. A mixed task can still contain
    # a database schema/migration and must retain its data-loss safeguards.
    database_text = re.sub(r"\bschema(?:\.org|\s+markup)\b", "", text)
    if any(w in database_text for w in ("schema","column","migration","archived_at")):
        operations.add("migration"); capabilities.add("persistence"); surfaces.add("database"); state["migration"]=True; state["durable_change"]=True; archetypes.add("schema-change"); risks.update(("data-loss","compatibility"))
    if any(w in text for w in ("create","update","archive","delete","mutation")):
        operations.add("mutation"); state["durable_change"]=bool(caps.get("persistence"))
        if state["durable_change"]: capabilities.add("persistence")
    if any(w in text for w in ("authenticated","tenant")) and "mutation" in operations:
        archetypes.add("authenticated-mutation")
    if "invitation" in text or "invite" in text:
        operations.add("mutation"); capabilities.add("auth"); risks.add("authorization"); risks.add("tenant-isolation"); archetypes.add("authenticated-mutation")
        if caps.get("persistence"): capabilities.add("persistence"); state["durable_change"]=True
        if any(w in text for w in ("expiring", "expiration", "expiry", "token", "link")):
            risks.add("credential")
        else:
            uncertain.append({"field":"risks","question":"Does this invitation act as a bearer credential?","allowed":["credential","not-credential","unknown"]})
    if any(w in text for w in ("token","secret","credential")):
        risks.add("credential")
    if "pwa" in text or "service worker" in text:
        capabilities.add("pwa"); archetypes.add("pwa-capability-change"); surfaces.add("frontend")
    if any(w in text for w in ("background job","cron","queue")):
        archetypes.add("background-job"); surfaces.add("backend")

    for raw_path in changed_paths:
        path=raw_path.lower().replace("\\","/")
        agent_path = "/" + path.removeprefix("./")
        if agent_path.endswith(("/product-marketing.md", "/product-marketing-context.md", "/marketing-context.md")):
            archetypes.add("marketing-content-change"); risks.update(("commercial-truth", "message-fit"))
            _evidence(evidence, "change-structure", "archetype:marketing-content-change", raw_path)
        if re.search(r"/(?:robots|sitemap)(?:\.[a-z]+)+$", agent_path):
            archetypes.add("public-discoverability-change"); risks.update(("search-exposure", "commercial-truth"))
            _evidence(evidence, "change-structure", "archetype:public-discoverability-change", raw_path)
        if re.search(r"/(?:analytics|tracking)/(?:conversion[s-]?|marketing-events)[^/]*\.[a-z]+$", agent_path):
            archetypes.add("conversion-measurement"); risks.update(("measurement-integrity", "marketing-privacy"))
            _evidence(evidence, "change-structure", "archetype:conversion-measurement", raw_path)
        learning_path = any(marker in agent_path for marker in (
            "/.claude/homunculus/", "/ecc-homunculus/", "/skills/continuous-learning/", "/skills/continuous-learning-v2/",
        ))
        if learning_path:
            archetypes.add("agent-learning-change"); risks.add("learned-authority")
            _evidence(evidence, "change-structure", "archetype:agent-learning-change", raw_path)
        if learning_path or agent_path.endswith((
            "/.mcp.json", "/.codex/config.toml", "/.claude/settings.json", "/.claude/settings.local.json",
            "/hooks/codex-hooks.json", "/scripts/hooks/session-start-bootstrap.js", "/scripts/hooks/plugin-hook-bootstrap.js",
        )) or any(marker in agent_path for marker in (
            "/.claude/hooks/", "/.claude/skills/", "/.codex/skills/", "/.agents/skills/", "/.codex-plugin/", "/.claude-plugin/",
        )):
            archetypes.add("agent-tooling-change"); risks.add("agent-execution")
            _evidence(evidence, "change-structure", "archetype:agent-tooling-change", raw_path)
        if "migrations/" in path or path.endswith(".sql"):
            surfaces.add("database"); operations.add("migration"); capabilities.add("persistence"); state["migration"]=True; state["durable_change"]=True; archetypes.add("schema-change"); risks.update(("data-loss","compatibility")); _evidence(evidence,"change-structure","migration",raw_path)
        if path.startswith(".github/workflows/"):
            surfaces.add("ci"); _evidence(evidence,"change-structure","surface",raw_path)
        if any(k in path for k in ("policy","policies","permission","authz","rls")):
            risks.add("authorization"); operations.add("authorization"); boundaries["privileged"]=True; _evidence(evidence,"change-structure","risk:authorization",raw_path)
        if any(k in path for k in ("token","secret","invite","credential")):
            risks.add("credential"); _evidence(evidence,"change-structure","risk:credential",raw_path)
        if any(k in path for k in ("manifest.webmanifest","service-worker","sw.js")):
            capabilities.add("pwa"); surfaces.add("frontend")
        if any(k in path for k in ("accessibility","a11y")):
            surfaces.add("frontend"); risks.add("accessibility"); _evidence(evidence,"change-structure","risk:accessibility",raw_path)

    if "frontend" in surfaces:
        risks.add("accessibility")

    if "mutation" in operations and "authorization" in operations: archetypes.add("authenticated-mutation")
    if "mutation" in operations and state["durable_change"] and not archetypes: archetypes.add("modify-domain-state")
    if surfaces=={"frontend"} and any(w in text for w in ("spacing","visual")): archetypes.add("visual-regression-fix")

    return TaskDescriptor(intent=_sorted(intent),surfaces=_sorted(surfaces),operations=_sorted(operations),capabilities=_sorted(capabilities),risks=_sorted(risks),state=state,boundaries=boundaries,delivery=delivery,archetypes=_sorted(archetypes),uncertain=tuple(uncertain),evidence=tuple(evidence),task_text=task_text)

def merge_agent_resolution(descriptor: TaskDescriptor, resolution: dict) -> TaskDescriptor:
    allowed_fields={item["field"] for item in descriptor.uncertain}
    if not set(resolution).issubset(allowed_fields):
        raise ValueError("agent resolution may only fill declared uncertain fields")
    risks=set(descriptor.risks); uncertain=list(descriptor.uncertain); evidence=list(descriptor.evidence)
    if "risks" in resolution:
        values=resolution["risks"]
        if not isinstance(values,list): raise ValueError("risks resolution must be a list")
        if "unknown" in values:
            if values != ["unknown"]:
                raise ValueError("unknown risk resolution cannot be combined with concrete values")
            return descriptor
        allowed_values=set()
        for item in uncertain:
            if item["field"]=="risks": allowed_values.update(item.get("allowed",[]))
        for value in values:
            if value=="not-credential": continue
            if value not in allowed_values: raise ValueError(f"invalid risk resolution {value}")
            risks.add(value); _evidence(evidence,"agent-resolution","risk",value)
        uncertain=[item for item in uncertain if item["field"]!="risks"]
    return TaskDescriptor(intent=descriptor.intent,surfaces=descriptor.surfaces,operations=descriptor.operations,capabilities=descriptor.capabilities,risks=_sorted(risks),state=dict(descriptor.state),boundaries=dict(descriptor.boundaries),delivery=dict(descriptor.delivery),archetypes=descriptor.archetypes,uncertain=tuple(uncertain),evidence=tuple(evidence),task_text=descriptor.task_text)
