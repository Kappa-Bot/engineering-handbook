from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .canonical import stable_hash
from .discovery_rules import document_is_review_object, evaluate_rules, positive_text
from .visual_directions import detect_visual_styles

EVIDENCE_RANK={"explicit-structured":600,"declared-decision":500,"repo-structure":400,"change-structure":350,"text-signal":200,"agent-resolution":150}

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

def _visual_task_clauses(text: str, *, include_bounded: bool = False) -> list[str]:
    # Tool documentation, installation and explicitly bounded edits are not
    # invitations to reconstruct a screen, even when they mention a hero.
    clauses = []
    method = r"\b(?:unslop(?:ping)?|anti[- ]slop|ai[- ]slop|ai[- ]looking)\b"
    # Filter each action separately: a negated redesign or typo fix must not
    # erase an adjacent authorized design task or read-only visual audit.
    separator = (
        r"[.;,\n]|\b(?:and|but|then|y|pero|luego)\s+"
        r"(?=(?:fix|corrige|corregir|audit|audita|review|revisa|redesign|rediseñ|"
        r"design|diseñ|unslop|apply|aplica|polish|refine|pule|replantea|remove|elimina|quita|do not|no\s))"
    )
    for clause in re.split(separator, text):
        clause = re.sub(
            r"\b(?:do not|don['’]t|without|no|sin)\s+"
            r"(?:(?:un|una|a|any|el|la|the|hagas?|hacer)\s+){0,2}"
            r"(?:redesign(?:ing)?|rediseñ(?:a(?:r)?|o|es)|"
            r"(?:(?:apply|apliques|aplica(?:r)?)\s+)?unslop(?:ping)?)\b.*",
            "", clause,
        )
        # Documentation may be the product being reviewed rather than the
        # source being read. Distinguish the primary object of a review.
        reviewed_surface = re.match(
            r"\s*(?:review|revisa|audit|audita)\s+(?:(?:the|this|la|el|esta|este)\s+)?"
            r"(?:ui|interfaz|interface|screen|pantalla|dashboard|portal)\b", clause,
        )
        reference_subject = not reviewed_surface or re.match(
            r"\s+(?:readme|docs|documentation|documentaci[oó]n|licen[cs]e|licencia)\b",
            clause[reviewed_surface.end():],
        )
        if re.search(method, clause) and (
            re.match(r"\s*(?:please\s+)?(?:read|document(?:a|ar)?|describe|explain|research|install|instala(?:r)?)\b", clause)
            or (reference_subject and re.match(r"\s*(?:review|revisa|update|actualiza|polish|pule|audit|audita)\b", clause)
                and re.search(r"\b(?:readme|docs|documentation|documentaci[oó]n|licen[cs]e|licencia|installation|instalaci[oó]n)\b", clause))
            or re.match(r"\s*(?:unslop|anti[- ]slop)\s+(?:readme|docs|license|licencia|installation|instalaci[oó]n)\b", clause)
        ):
            continue
        if include_bounded:
            clauses.append(clause)
            continue
        if re.search(r"\b(?:only|solo|solamente|[uú]nicamente)\b", clause) and re.search(
            r"\b(?:one|single|un|una)\s+(?:(?:settings|de|la|el)\s+){0,2}(?:button|bot[oó]n|icon|icono|margin|margen)\b|"
            r"\b(?:typo|errata|border radius|padding)\b", clause,
        ):
            continue
        if re.search(r"\b(?:fix|corrige|corregir)\b", clause) and re.search(r"\b(?:typo|errata)\b", clause):
            continue
        clauses.append(clause)
    return clauses


CONSOLE_RAIL_MARKERS = (
    "sidebar", "side bar", "side-bar", "barra lateral", "menú lateral",
    "menu lateral", "navigation rail", "nav rail",
)
CONSOLE_SHELL_MARKERS = (
    "dark mode", "light mode", "modo oscuro", "modo claro",
    "theme toggle", "theme switch", "theme control", "cambio de tema",
    "selector de tema", "alternador de tema", "header",
    "shell", "cambio de pantalla", "cambios de pantalla",
    "transición de pantalla", "transiciones de pantalla",
    "transición entre pantallas", "transiciones entre pantallas",
    "transicion entre pantallas", "transiciones entre rutas",
    "transición entre rutas", "route transition", "route-stage",
    "screen transition", "screen change",
)
_CONSOLE_SHELL_COMPONENT = re.compile(
    r"\b(?:" + "|".join(map(re.escape, (*CONSOLE_RAIL_MARKERS, *CONSOLE_SHELL_MARKERS, "encabezado"))) + r")\b"
)


def _targets_console_shell(clause: str) -> bool:
    console = re.search(r"\b(?:console|consola|dashboard|admin panel|panel administrativo)\b", clause)
    part = _CONSOLE_SHELL_COMPONENT.search(clause)
    if console is None or part is None:
        return False
    if part.start() < console.start():
        return bool(re.search(r"\b(?:in|for|of|on|de|en|del|para)\b", clause[part.end():console.start()]))
    return bool(re.fullmatch(r"(?:['’]s)?\s+(?:(?:intern[ao]|administrativ[ao])\s+)?", clause[console.end():part.start()]))


def _new_console_signal(text: str) -> bool:
    return any(w in text for w in (
        "nueva", "nuevo", "crear", "diseña", "diseñar", "desarroll",
        "implement", "build", "design", "create", "new ", "montar",
    )) and any(w in text for w in (
        "consola", "console", "dashboard", "panel administrativo", "admin panel",
        "operator workspace", "workspace administrativo", "backoffice",
    ))


def _design_fit_signal(text: str) -> bool:
    # A product name narrows context; it never grants mutation or release rights.
    surface = (
        r"(?:ui|ux|interfaces?|interfaz|web|websites?|sites?|p[aá]ginas?|landings?|"
        r"hero|homepage|screens?|pantallas?|apps?|aplicaci[oó]n(?:es)?|dashboards?|panels?|"
        r"consol[ea]s?|crm|frontend|workspaces?)"
    )
    # Bare Core is a standalone target, not the adjective in "core algorithm".
    product = r"(?:melodiq[ -]core|core(?!\s+\w)|ops[ -]?os|church[ -]?os|dental[ -]?os)"
    method = r"\b(?:unslop(?:ping)?|anti[- ]slop|ai[- ]slop|ai[- ]looking)\b"
    backend_object = r"(?:api|backend|database|sql|postgresql|base de datos|server|queries|consultas|schema)"
    backend = rf"\b{backend_object}\b"
    product_non_ui = rf"{backend}|\b(?:library|parser)\b"
    action = r"(?:unslop|(?:re)?design(?:ing)?|(?:re)?diseñ(?:a|ar|o)|polish|refine|pule|pulir|replantea|replantear)"
    bridge = (
        rf"(?:(?!(?:{backend_object}|buttons?|bot[oó]n|margins?|margen|padding|"
        r"border|radius|typo|errata)\b)\w+[\s-]+){0,6}"
    )
    for clause in _visual_task_clauses(text):
        if re.search(rf"\b{action}\s+{bridge}{surface}\b(?!\s+{backend_object}\b)", clause):
            return True
        if re.search(rf"\b{action}\s+{bridge}{product}\b", clause) and not re.search(product_non_ui, clause):
            return True
        target = re.search(rf"\b{surface}\b", clause)
        product_target = re.search(rf"\b{product}\b", clause)
        backend_target = re.search(backend, clause)
        # "Unslop the backend API for this UI" is not UI redesign. A screen
        # explicitly designed above may still be backed by an API/database.
        if backend_target and (target is None or backend_target.start() < target.start()):
            continue
        if target and re.match(rf"(?:['’]s)?\s+{backend_object}\b", clause[target.end():]):
            continue
        if target is None and re.search(product_non_ui, clause):
            continue
        design = re.search(
            rf"{method}|\b(?:visual quality|calidad visual|jerarqu[ií]a visual|direcci[oó]n art[ií]stica|"
            r"art direction|visual hierarchy|experiencia visual|visual experience|generic (?:copy|layout|design)|"
            r"(?:aspecto|apariencia) generad[oa] por (?:ia|ai)|"
            r"(?:textos?|dise[ñn]o) gen[eé]ric[oa]s?|(?:demasiadas|exceso de) tarjetas|too many cards)\b",
            clause,
        )
        if design and (target or product_target or re.search(r"\b(?:visual|layout|dise[ñn]o|design)\b", clause)):
            return True
    return False


def _frontend_quality_signals(text: str) -> dict[str, str | None]:
    interface = re.search(
        r"\b(?:ui|ux|interface|interfaz|web|website|landing|hero|homepage|bot[oó]n|button|"
        r"dialog|modal|drawer|menu|men[uú]|dashboard|panel administrativo|crm|scroll|"
        r"page|p[aá]gina|site|screens?|pantallas?|route transition)\b",
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
    record_action = re.search(r"\b(?:crud|altas|bajas|guardar|saving|archive|delete|create records?)\b", text)
    scripted_control = re.search(r"\b(?:checklists?|listas? de verificaci[oó]n|progress bars?|barras? de progreso)\b", text)
    scripting_fallback = re.search(r"\b(?:no[- ]js|without (?:scripts?|javascript)|sin (?:scripts?|javascript))\b", text)
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
        (_design_fit_signal(text), "design-fit", "design-fit"),
    )
    return {archetype: risk for matched, archetype, risk in signals if matched}


GUIDANCE_SOURCE = r"(?:modern[ -]web[ -]guidance|ponytail)"
TECHNICAL_ACTION = (
    r"(?:fix|repair|correct|corrige|corregir|add|añade|añadir|agrega|agregar|"
    r"implement\w*|audit\w*|review|revisa\w*|refactor\w*|simplif\w*|"
    r"update|actualiza\w*|replace|sustituye|build|create|crea\w*|design|diseña\w*|"
    r"deploy\w*|despliega|desplegar|release|publica\w*|verify|verifica\w*|inspect|check|comprueba)"
)


def _action_clauses(text: str) -> list[str]:
    separator = (
        r"[;\n]|(?<=[.!?])\s+|\b(?:and|but|then|y|pero|luego|despu[eé]s)\s+"
        rf"(?={TECHNICAL_ACTION}\b)"
    )
    return [re.sub(r"^(?:then|luego|despu[eé]s|please)\s+", "", clause.strip()) for clause in re.split(separator, text) if clause.strip()]


def _guidance_tooling_signal(text: str) -> bool:
    # The named source must be the tool being changed/inspected, not merely the
    # method used to update a form or ordinary React hooks.
    articles = r"(?:(?:the|a|an|el|la|un|una|de|del|for|of|para|installed|plugin|skill|package|cli)\s+){0,5}"
    runtime = r"(?:hooks?|plugins?|skills?|cli|configuration|configuraci[oó]n|runtime)"
    return bool(re.search(
        rf"\b(?:install|instala\w*|update|upgrade|actualiza\w*|configure|configura\w*)\s+{articles}{GUIDANCE_SOURCE}\b|"
        rf"\b{GUIDANCE_SOURCE}(?:['’]s)?\s+{runtime}\b|"
        rf"\b{runtime}\s+(?:de|del|for|of|para)\s+(?:the\s+)?{GUIDANCE_SOURCE}\b", text,
    ))


def _implementation_clauses(text: str) -> list[str]:
    """Keep the object of each technical action, not every mentioned reference."""
    clauses = []
    for clause in _action_clauses(text):
        if document_is_review_object(clause):
            continue
        if re.match(r"(?:integrat\w*|integra\w*|incorpora\w*)\b", clause) and re.search(
            rf"\b{GUIDANCE_SOURCE}\b.*\b(?:handbook|agents\.md|skill\.md)\b", clause
        ):
            continue
        if re.match(r"(?:read|research|explain|document\w*|describe|write|escribe)\b", clause) and re.search(
            rf"\b(?:{GUIDANCE_SOURCE}|handbook|readme|docs|documentation|documentaci[oó]n|gu[ií]as?|licen[cs]ing|licen[cs]e|licencia)\b", clause
        ):
            continue
        if re.search(r"\b(?:typo|errata)\b", clause):
            continue
        target = re.sub(rf"^{TECHNICAL_ACTION}\s+(?:(?:the|this|a|el|la|los|las|un|una)\s+)*", "", clause)
        if re.match(
            r"(?:handbook|agents\.md|skill\.md|licen[cs]ing|licen[cs]e|licencia|readme|documentation|documentaci[oó]n|docs|(?:marketing |sales |website )?copy|texto|correo)\b", target
        ) or re.match(
            rf"{GUIDANCE_SOURCE}\s+(?:licen[cs]ing|licen[cs]e|licencia|readme|docs|documentation)\b", target
        ):
            continue
        if re.match(r"(?:install|instala(?:r)?)\b", clause):
            continue
        if _guidance_tooling_signal(clause) and re.match(r"(?:update|upgrade|actualiza\w*|configure|configura\w*)\b", clause):
            continue
        if re.match(r"(?:do not|don't|no|sin)\s+(?:change|modify|edit|cambies|modifiques|edites)\b", clause):
            continue
        clauses.append(clause)
    return clauses


def _web_platform_signal(clauses: list[str]) -> bool:
    browser = (
        r"\b(?:html|css|dom|browser|navegador(?:es)?|client[- ]side|frontend|react|preact|"
        r"vue|svelte|jsx|tsx|dialog(?:s)?|di[aá]logos?|modals?|popovers?|tooltips?|dropdowns?|form(?:s)?|formularios?|"
        r"accordions?|acorde[oó]n(?:es)?|disclosures?|screen[- ]?readers?|fullscreen|"
        r"skeletons?|inp|lcp|cls|hydration|hidrataci[oó]n|container queries|"
        r"view transitions?|scroll[- ]driven|responsive (?:table|layout)|tabla (?:interactiva|responsive))\b"
    )
    browser += r"|<(?:details|summary|select|option|input|button|dialog|table)\b"
    backend = r"(?:sql|database|backend|server|servidor|postgres(?:ql)?|rls|api route|api handler|base de datos)"
    for clause in clauses:
        match = re.search(browser, clause)
        if not match:
            continue
        server = re.search(rf"\b{backend}\b", clause)
        hydration = re.search(r"\b(?:hydration|hidrataci[oó]n)\b", clause)
        # "Optimize SQL for the React table" is a backend target, while
        # "Fix React table backed by SQL" still changes browser behavior.
        if server and server.start() < match.start() and not hydration:
            continue
        if not hydration and re.search(rf"\b(?:on|in|inside|within|en|del)\s+(?:(?:the|el|la)\s+)?{backend}\b", clause):
            continue
        if re.search(r"\b(?:react|next(?:\.js)?)\s+server\b", clause) and not re.search(
            r"\b(?:hydration|hidrataci[oó]n|css|dom|focus|foco)\b", clause
        ):
            continue
        return True
    return False


def _browser_source_path(raw_path: str) -> bool:
    path = "/" + raw_path.lower().replace("\\", "/").removeprefix("./")
    if re.search(r"/(?:node_modules|\.next|dist|build|coverage|docs|__tests__|tests|fixtures|__fixtures__|emails?|server|api)/", path):
        return False
    if re.search(r"\.(?:test|spec|server|d)\.[a-z]+$", path):
        return False
    return bool(re.search(r"\.(?:tsx|jsx|css|scss|html|vue|svelte)$", path) or (
        re.search(r"/(?:components?|client|browser|hooks)/", path) and re.search(r"\.[cm]?[jt]s$", path)
    ))


def _lean_change_signal(clauses: list[str]) -> bool:
    for clause in clauses:
        code = re.search(r"\b(?:code|c[oó]digo|api|handler|mutation|mutaci[oó]n|module|m[oó]dulo|component\w*|function|funci[oó]n|logic|l[oó]gica|callers?|consumidores|crm|browser|form|hooks?)\b", clause)
        code_review_target = re.search(r"\b(?:code|c[oó]digo|api|handler|mutation|mutaci[oó]n|module|m[oó]dulo|component\w*|function|funci[oó]n|logic|l[oó]gica|callers?|consumidores|hooks?)\b", clause)
        focused_quality = re.search(
            r"\b(?:security|seguridad|privacy|privacidad|performance|rendimiento|"
            r"accessibility|accesibilidad|reliability|fiabilidad|usability|usabilidad)\b", clause
        )
        if (code and re.search(r"\b(?:ponytail|simplif\w*|refactor\w*|deduplic\w*)\b", clause)) or (
            code_review_target and not focused_quality and re.search(r"\b(?:review|revisa|audit|audita)\b", clause)
        ):
            return True
        if re.search(r"\b(?:dead code|c[oó]digo muerto|smallest complete (?:fix|change)|minimum complete change)\b", clause):
            return True
    return False


def _connected_product_signal(clauses: list[str]) -> bool:
    for clause in clauses:
        if re.search(r"\b(?:custom (?:product )?agents?|product agents?|agentes? (?:personalizad[oa]s?|de producto)|sales agents?)\b", clause):
            return True
        if re.search(r"\bcrm\b", clause) and re.search(r"\b(?:website|public (?:site|web)|web p[uú]blica|webhook|api|agents?|agentes?)\b", clause):
            return True
        if re.search(r"\bcrm\b", clause) and re.search(r"\b(?:form|formulario)\b", clause) and re.search(r"\b(?:connect\w*|conect\w*|ingress|intake|ingesta)\b", clause):
            return True
    return False


def _site_composition_signal(clauses: list[str]) -> bool:
    for clause in clauses:
        # Merely naming a hero as the subject of an LCP measurement does not
        # ask for photography, animation, reskinning or layout reconstruction.
        if re.search(r"\b(?:hero|first viewport|primer viewport)\b", clause) and re.match(
            r"\s*(?:build|create|design|redesign|rebuild|refine|improve|polish|change|"
            r"modify|update|fix|crea\w*|constru\w*|diseñ\w*|disen\w*|rediseñ\w*|"
            r"redisen\w*|mejora\w*|pule|refina\w*|cambia\w*|modifica\w*|actualiza\w*|corrig\w*)\b", clause,
        ):
            return True
        site = re.search(
            r"\b(?:build|create|design|redesign|rebuild|crea|crear|diseña|rediseña|construye|monta|haz)\s+"
            r"(?:(?:a|an|the|this|our|my|new|public|client|marketing|business|complete|una|un|la|el|nueva|nuevo)\s+){0,5}"
            r"(?:website|site|landing|web|p[aá]gina web|sitio web)\b", clause,
        )
        if site:
            # Inspect the noun phrase rather than only the next word: a
            # "website customer contact form" is a component, while a
            # "website with a contact form" is a whole-site request.
            noun_phrase = re.split(
                r"\b(?:with|without|for|from|to|via|of|in|on|and|but|that|which|"
                r"con|sin|para|desde|hacia|mediante|a|al|de|del|en|y|pero|que)\b|[;,:.]",
                clause[site.end():], maxsplit=1,
            )[0]
            if not re.search(r"\b(?:forms?|formularios?|intake|api|webhooks?|endpoints?|integrations?|integraci[oó]n)\b", noun_phrase):
                return True
    return False


def _production_clauses(text: str) -> list[str]:
    relevant = []
    for clause in _action_clauses(text):
        # A prohibition is not an order. Keep an earlier observation and any
        # separate affirmative release clause rather than negating the request.
        clause = re.sub(
            r"\b(?:do not|don['’]t|never|without|no|sin)\s+(?:deploy\w*|release|desplieg\w*|desplegar)\b.*", "", clause,
        )
        if re.search(r"\b(?:production|producci[oó]n|deploy\w*|desplieg\w*|desplegar|release)\b", clause):
            relevant.append(clause)
    return relevant


def _production_is_observed(clauses: list[str]) -> bool:
    for clause in clauses:
        if re.match(r"(?:deploy\w*|despliega|desplegar|release)\b", clause):
            return False
        if not (re.match(r"(?:audit\w*|review|revisa\w*|inspect|check|comprueba|verify|verifica)\b", clause) or re.search(
            r"\b(?:read[- ]only|without edits|solo lectura|sin editar|sin cambios)\b", clause
        )):
            return False
    return True


def _identifier_components(text: str) -> set[str]:
    # Preserve meaningful identifier words before lowercasing. Substrings
    # would confuse "lieutenant" with "tenant"; prefix-only matching loses
    # crossTenantId, hasPermission and request_tenant_id.
    expanded = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", expanded)
    return set(re.findall(r"[^\W\d_]+", expanded.lower()))


def describe_task(task_text: str, repo_profile: dict, changed_paths: tuple[str,...]=()) -> TaskDescriptor:
    text=positive_text(task_text).lower()
    intent=set(); surfaces=set(); operations=set(); capabilities=set(); risks=set(); archetypes=set(); evidence=[]; uncertain=[]
    state={"durable_change":False,"migration":False}; boundaries={"external":False,"privileged":False}; delivery={"production_effect":False}
    detected=repo_profile.get("detected",{})
    caps=detected.get("capabilities",{})
    for c,v in caps.items():
        if v: _evidence(evidence,"repo-structure",f"repo-capability:{c}","true")

    guidance_source = bool(re.search(rf"\b{GUIDANCE_SOURCE}\b", text))
    if guidance_source:
        archetypes.add("external-guidance-evaluation")
        _evidence(evidence, "text-signal", "archetype", "external-guidance-evaluation")
        if _guidance_tooling_signal(text):
            archetypes.add("agent-tooling-change"); risks.add("agent-execution")
            _evidence(evidence, "text-signal", "archetype", "agent-tooling-change")
    technical_clauses = _implementation_clauses(text)
    browser_paths = [path for path in changed_paths if _browser_source_path(path)]
    browser_text = _web_platform_signal(technical_clauses)
    if browser_text or (technical_clauses and browser_paths):
        archetypes.add("web-platform-change"); surfaces.add("frontend"); risks.add("browser-compatibility")
        if browser_text:
            _evidence(evidence, "text-signal", "archetype", "web-platform-change")
        for path in browser_paths:
            _evidence(evidence, "change-structure", "surface:frontend", path)
    if _lean_change_signal(technical_clauses):
        archetypes.add("lean-change"); risks.add("change-completeness")
        _evidence(evidence, "text-signal", "archetype", "lean-change")
    if _connected_product_signal(technical_clauses):
        archetypes.add("connected-product-change")
        _evidence(evidence, "text-signal", "archetype", "connected-product-change")

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

    baseline_text = "; ".join(_visual_task_clauses(text, include_bounded=True))
    if re.search(r"\b(?:spacing|layouts?|visual(?:es|ly|mente)?|screens?|screen[- ]?readers?|fullscreen|buttons?|cards?|ux|ui)\b", text) or re.search(
        r"\b(?:hero|pantallas?|interfaz|bot[oó]n|dashboard|console|consola)\b", baseline_text,
    ):
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
    visual_text = "; ".join(_visual_task_clauses(text))
    # The front page of a reading surface can need a different hierarchy from a marketing hero.
    explicit_marketing_surface = re.search(
        r"\b(?:landing(?: page)?|marketing website|client website|business website|web corporativa)\b", visual_text
    )
    site_composition = _site_composition_signal(technical_clauses)
    generic_home = any(w in visual_text for w in ("homepage", "home page", "public website", "página web", "página de inicio")) or (
        "connected-product-change" in archetypes and site_composition
    )
    # A site's API/intake is not a request to rebuild its hero. Preserve a real
    # composition request in another clause of a connected-product task.
    connected_boundary_only = "connected-product-change" in archetypes and not site_composition
    visual_composition_action = any(re.match(
        r"\s*(?:build|create|design|redesign|rebuild|refine|improve|polish|change|"
        r"modify|update|fix|crea\w*|constru\w*|diseñ\w*|disen\w*|rediseñ\w*|"
        r"redisen\w*|mejora\w*|pule|refina\w*|cambia\w*|modifica\w*|actualiza\w*|corrig\w*)\b", clause,
    ) for clause in _visual_task_clauses(text))
    visual_composition_request = bool(visual_composition_action and (
        site_composition or _design_fit_signal(text)
        or re.search(r"\b(?:hero|art direction|visual hierarchy|jerarquia visual|visual design|diseno visual|composicion visual)\b", visual_text)
    ))
    if not connected_boundary_only and visual_composition_request and (
        explicit_marketing_surface or (not editorial and (generic_home or re.search(r"\bhero\b", visual_text)))
    ):
        surfaces.add("frontend")
        archetypes.update(("ui-flow-change", "marketing-hero-change"))
        risks.update(("hero-fidelity", "design-fit"))
        _evidence(evidence, "text-signal", "archetype", "marketing-hero-change")
    # A console shell is more specific than generic UI/marketing work. Restrict it
    # to operator/admin contexts or a standalone navigation rail, never public sites.
    operator_scope = any(w in text for w in (
        "consola", "console", "panel administrativo", "panel de administr",
        "admin panel", "admin dashboard", "admin ui", "internal dashboard",
        "administrative dashboard", "backoffice",
        "back office", "operator workspace", "workspace administrativo",
        "melodiq core", "melodiq-core", "dentalos", "dental os",
        "churchos", "church os", "ops os", "opsos", "agurto os", "b2b-platform",
    ))
    rail_signal = any(marker in text for marker in CONSOLE_RAIL_MARKERS)
    shell_signal = rail_signal or any(marker in text for marker in CONSOLE_SHELL_MARKERS)
    new_console = operator_scope and _new_console_signal(visual_text)
    public_markers = (
        "public website", "public site", "marketing website", "marketing site", "landing page",
        "web corporativa", "blog corporativo", "sitio público", "web pública",
        "página pública", "uribe villa", "uribevilla", "mudanzasagurto",
    )
    public_surface = any(w in text for w in public_markers)
    # A product name identifies a vertical, not an authenticated operator UI.
    # Patient/member portals and field/kiosk surfaces have their own direction
    # even when their implementation shares the same CRM or brand.
    non_operator_markers = (
        "patient portal", "patient-facing", "patient dashboard",
        "portal de pacientes", "portal para pacientes", "portal del paciente",
        "portal paciente", "member portal", "portal de miembros", "portal de socios",
        "self-service", "self service", "autoservicio", "autogestión", "autogestion",
        "kiosk", "kiosco", "quiosco", "field app", "field kiosk",
        "app de campo", "aplicación de campo", "aplicacion de campo",
        "customer-facing", "client-facing", "consumer-facing", "customer portal",
        "client portal", "product landing", "landing comercial", "landing de clientes",
        "para pacientes", "for patients", "for members", "para socios",
    )
    non_operator_surface = any(w in text for w in non_operator_markers)
    explicit_operator_markers = (
        "internal console", "consola interna", "admin console", "operator console",
        "consola administrativa", "panel administrativo", "admin panel",
        "admin dashboard", "admin ui", "internal dashboard", "dashboard interno", "administrative dashboard",
        "panel de administración", "panel de administracion",
        "backoffice", "back office", "operator workspace", "workspace administrativo",
        "internal crm", "crm interno", "internal workspace", "app interna",
    )
    # A positive explicit internal target wins in a mixed brief; brand/product
    # names alone never override a specified patient, public or field surface.
    def targets_operator(clause: str) -> bool:
        for marker in explicit_operator_markers:
            for occurrence in re.finditer(r"(?<!\w)" + re.escape(marker) + r"(?!\w)", clause):
                before, after = clause[:occurrence.start()], clause[occurrence.end():]
                if re.search(r"\b(?:not|no|sin|from|instead of|rather than|en lugar de|en vez de|leave|keep|deja|mant[eé]n)\s+"
                             r"(?:(?:the|la|el|un|una)\s+)?$", before):
                    continue
                if not re.match(r"\s+(?:as (?:an? |the )?(?:reference|example)|como (?:referencia|ejemplo)|unchanged|untouched|as is|sin cambios|intact[oa])\b", after):
                    return True
        return False

    explicit_operator_scope = any(targets_operator(clause) for clause in re.split(r"[;,\n]|\b(?:but|pero|then|luego)\b", text))
    operator_visual_scope = explicit_operator_scope or (operator_scope and not non_operator_surface and not public_surface)
    # Complete public-site work is a distinct archetype from an isolated hero,
    # sidebar, review or backend change. Route the website delivery playbook
    # automatically for creation/redesign briefs in either language, but keep
    # authenticated operator surfaces out even if a prompt says "web".
    public_website_markers = public_markers + (
        "web para", "web de empresa", "web de servicios", "página web",
        "pagina web", "sitio web para", "website for", "client website",
        "business website", "service website", "commercial website",
    )
    public_website_signal = any(marker in text for marker in public_website_markers)
    whole_site_action = any(w in visual_text for w in (
        "haz una web", "hacer una web", "crea una web", "crear una web",
        "monta una web", "montar una web", "nueva web", "nuevo sitio",
        "new website", "build a website", "build a site", "create a website",
        "website redesign", "rediseñar la web", "rediseña la web",
        "redesign the website", "complete the website", "termina la web",
        "completa la web", "desarrolla la web", "diseña la web",
    )) or (
        public_website_signal and any(w in visual_text for w in (
            "create", "build", "crea", "crear", "construir", "construye",
            "diseña", "diseñar", "desarrolla", "monta", "montar",
            "rediseña", "rediseñar", "redesign", "rebuild",
        ))
    )
    if not connected_boundary_only and whole_site_action and public_website_signal and (public_surface or not operator_scope) and (not editorial or explicit_marketing_surface):
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
    google_ai_eligibility = public_website_signal and any(
        any(marker in clause for marker in public_website_markers)
        and (
            re.search(r"\bnosnippet\b", clause)
            or (re.search(r"\b(?:google(?:['’]s)? (?:search )?ai (?:overviews|mode)|(?:modo ia|vistas? creadas? con ia) de google)\b", clause)
                and re.search(r"\b(?:eligib\w*|elegib\w*|supporting[ -]links?|enlaces?|snippet)\b", clause))
        )
        for clause in _action_clauses(text)
    )
    search_signal = public_indexing or google_ai_eligibility or bool(re.search(r"\b(?:seo|noindex|sitemap|robots\.txt|json-ld|schema\.org|site-architecture)\b", text)) or any(w in text for w in (
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
    if (operator_visual_scope and (shell_signal or (new_console and "operation-feedback" not in quality_signals))) or (rail_signal and not public_surface and not non_operator_surface):
        surfaces.add("frontend"); archetypes.update(("ui-flow-change", "operator-console-shell-change"))
        risks.add("console-shell-fidelity")
        _evidence(evidence, "text-signal", "archetype", "operator-console-shell-change")
    # The default internal-console direction is a design-selection decision,
    # never permission to reskin a product or force a material on a small edit.
    material_operator_scope = operator_visual_scope or (not non_operator_surface and not public_surface and any(w in text for w in (
        "crm interno", "crm internal", "internal crm", "app interna",
        "aplicación interna", "internal app", "internal workspace",
    )))
    # Match the actual requested object/action, not a material keyword in a
    # README, design guide or a noun such as "implementation". Separate a
    # read-only style audit from a request to adopt a material.
    reference_task = re.compile(
        r"^\s*(?:please\s+|por favor\s+)?(?:review|revisa\w*|audit\w*|"
        r"audita\w*|read|lee|document\w*|documenta\w*|"
        r"analy[sz]e\w*|analiza\w*|eval[uú]a\w*|evaluar|"
        r"inspect\w*|inspecciona\w*|consulta\w*|examina\w*)\s+"
        r"(?:(?:the|this|a|el|la|los|las|un|una)\s+)?"
        r"(?:[\w-]+\s+){0,3}(?:readme(?:\.md)?|design\.md|docs|"
        r"documentation|documentaci[oó]n|handbook|manual|gu[ií]a)\b",
    )
    style_clauses = [visual_clause
                     for task_clause in re.split(
                         r"[;,\n]|\b(?:but|pero|then|luego)\b|"
                         r"\b(?:and|y)\s+(?=(?:usa|usar|use|apply|aplica|build|"
                         r"elige|choose|prefiero|quiero|no|do not|avoid|evita)\b)",
                         text,
                     )
                     if not reference_task.match(task_clause.strip())
                     for visual_clause in _visual_task_clauses(task_clause)]
    style_matches = {}

    def styles_in(clause: str) -> tuple[str, ...]:
        if clause not in style_matches:
            style_matches[clause] = detect_visual_styles(clause)
        return style_matches[clause]

    styles = styles_in("; ".join(style_clauses))
    material_action_pattern = re.compile(
        r"^\s*(?:(?:and|y)\s+)?(?:please\s+|por favor\s+)?(?:(?:i|we)\s+)?"
        r"(?:aplic\w*|apply|use|usa|usar|utiliza\w*|emplea\w*|pon|poner|"
        r"mejor\w*|implement(?:a\w*|ed|ing|s)?|diseñ\w*|design|"
        r"rediseñ\w*|redesign|crea\w*|build|adopta\w*|adopt|"
        r"selecciona\w*|elige\w*|choose|select|prefiero|quiero|"
        r"prefer|want|switch|set|cambia\w*|change)\b"
    )
    adoption_clauses = [clause for clause in style_clauses if material_action_pattern.match(clause)]
    review_clauses = [clause for clause in style_clauses if re.match(
        r"^\s*(?:please\s+|por favor\s+)?(?:revisa\w*|review\w*|"
        r"audita\w*|audit\w*|eval[uú]a\w*|evaluar|assess\w*|"
        r"analiza\w*|analy[sz]e\w*|compara\w*|comparar|compare\w*)\b",
        clause,
    )]
    style_selection = bool(styles) and bool(adoption_clauses or review_clauses or len(styles) > 1)
    mixed_surfaces = material_operator_scope and (public_surface or non_operator_surface)
    operator_clauses, operator_styles = style_clauses, styles
    operator_text = visual_text
    design_fit = "design-fit" in quality_signals
    new_operator_console = new_console
    if mixed_surfaces:
        operator_clauses = [clause for clause in style_clauses if targets_operator(clause)]
        operator_text = "; ".join(operator_clauses)
        operator_styles = styles_in(operator_text) if operator_clauses else ()
        design_fit = _design_fit_signal(operator_text)
        new_operator_console = _new_console_signal(operator_text)
    operator_actions = [clause for clause in adoption_clauses if clause in operator_clauses]
    operator_review = any(clause in review_clauses for clause in operator_clauses)
    operator_style_selection = bool(operator_styles) and bool(operator_actions or operator_review or len(operator_styles) > 1)
    material_clauses = [clause for clause in operator_clauses if not _targets_console_shell(clause)]
    nominal_styles = operator_styles
    if len(material_clauses) != len(operator_clauses):
        operator_text = "; ".join(material_clauses)
        design_fit = _design_fit_signal(operator_text)
        new_operator_console = _new_console_signal(operator_text)
        nominal_styles = styles_in(operator_text)
    design_selection = bool(material_clauses) and material_operator_scope and (
        design_fit or (new_operator_console and bool(re.search(r"\b(?:consola|console|dashboard|panel administrativo|admin panel)\b", operator_text)))
    )
    adopted = set()
    for clause in operator_actions:
        clause_styles = styles_in(clause)
        if len(clause_styles) == 1:
            adopted.add(clause_styles[0])
        elif len(clause_styles) > 1 and mixed_surfaces:
            # Parallel objects can assign one named material to each surface.
            # Keep an unassigned pair of styles as a comparison.
            parts = re.split(r"\b(?:and|y)\b", clause)
            if len(parts) == 2 and any(
                any(marker in part for marker in (*public_markers, *non_operator_markers))
                and not targets_operator(part) and len(styles_in(part)) == 1 for part in parts
            ):
                for part in parts:
                    if targets_operator(part):
                        part_styles = styles_in(part)
                        if len(part_styles) == 1:
                            adopted.add(part_styles[0])
    # A nominal "New console with Neumorphism" can also express adoption.
    if not adopted and design_selection and not operator_review and not operator_actions and len(nominal_styles) == 1:
        adopted.add(nominal_styles[0])
    adopted_style = next(iter(adopted)) if len(adopted) == 1 else None
    if style_selection or design_selection:
        surfaces.add("frontend")
        risks.add("visual-direction-fit")
        archetypes.add("visual-direction-choice")
        _evidence(evidence, "text-signal", "archetype", "visual-direction-choice")
    if material_operator_scope and (design_selection or operator_style_selection):
        archetypes.add("operator-visual-direction-choice")
        _evidence(evidence, "text-signal", "archetype", "operator-visual-direction-choice")
        if adopted_style:
            for style, archetype, risk in (
                ("glassmorphism", "operator-glass-material-change", "glass-material-fidelity"),
                ("neumorphism", "operator-neumorphic-material-change", "neumorphic-material-fidelity"),
            ):
                if style == adopted_style:
                    archetypes.update(("ui-flow-change", archetype))
                    risks.add(risk)
                    _evidence(evidence, "text-signal", "archetype", archetype)
    # Generic task/path policy has one declarative owner. Visual/commercial
    # recognizers above are retained as tested feature extractors.
    tags, rule_evidence = evaluate_rules(task_text, changed_paths)
    evidence.extend(rule_evidence)
    sets = {"intent": intent, "surface": surfaces, "operation": operations,
            "capability": capabilities, "risk": risks, "archetype": archetypes}
    for tag in sorted(tags):
        prefix, value = tag.split(":", 1)
        if prefix in sets:
            sets[prefix].add(value)
        elif prefix == "state":
            state[value.replace("-", "_")] = True
        elif prefix == "boundary":
            boundaries[value] = True
        elif prefix == "delivery":
            delivery["production_effect"] = value == "production"
    # Identifier tokenization is a language feature, not substring routing.
    identifier_components = _identifier_components(positive_text(task_text))
    authorization_identifier = identifier_components & {"role", "roles", "permission", "permissions", "authorization", "authorisation", "authz"}
    tenant_signal = bool(identifier_components & {"tenant", "tenants"} or re.search(r"\b(?:tenantid|multi[- ]?tenan\w*|multiempresa|multi-empresa|otra empresa|otra organizaci[oó]n|other tenant|cross-tenant)\b", text))
    if tenant_signal or authorization_identifier or re.search(r"\b(?:authenticated|authori[sz]ation|authz|permissions?|roles?|autenticad[oa]s?|permisos?|rol|autorizaci[oó]n)\b", text):
        operations.add("authorization"); capabilities.add("auth"); risks.add("authorization"); boundaries["privileged"]=True
    if tenant_signal:
        risks.add("tenant-isolation")
    if "mutation" in operations:
        state["durable_change"] = state["durable_change"] or bool(caps.get("persistence"))
        if state["durable_change"]: capabilities.add("persistence")
    if any(w in text for w in ("authenticated","tenant")) and "mutation" in operations:
        archetypes.add("authenticated-mutation")
    if any(e.get("rule_id") == "invitation-auth" and e.get("decision") == "matched" for e in rule_evidence):
        if caps.get("persistence"): capabilities.add("persistence"); state["durable_change"]=True
        if any(w in text for w in ("expiring", "expiration", "expiry", "token", "link")):
            risks.add("credential")
        else:
            uncertain.append({"field":"risks","question":"Does this invitation act as a bearer credential?","allowed":["credential","not-credential","unknown"]})

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

    if "frontend" in surfaces:
        risks.add("accessibility")

    if "mutation" in operations and "authorization" in operations: archetypes.add("authenticated-mutation")
    if "mutation" in operations and state["durable_change"] and not archetypes: archetypes.add("modify-domain-state")
    if surfaces=={"frontend"} and any(w in text for w in ("spacing","visual")): archetypes.add("visual-regression-fix")

    # Name retained feature extractors in explanations as well as registry rules.
    for item in evidence:
        item.setdefault("rule_id", "feature:" + item["signal"] + ":" + item["value"])
        item.setdefault("decision", "matched")

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
