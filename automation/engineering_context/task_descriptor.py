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
    # A public hero task may be named without "UI"/"layout"; route its specific pattern.
    if any(w in text for w in ("hero", "landing page", "homepage", "home page", "marketing website", "public website", "client website", "web corporativa", "página web", "página de inicio")):
        surfaces.add("frontend"); archetypes.add("ui-flow-change"); archetypes.add("marketing-hero-change"); risks.add("hero-fidelity"); _evidence(evidence,"text-signal","archetype","marketing-hero-change")
    # A console shell is more specific than generic UI/marketing work. Restrict it
    # to operator/admin contexts or a standalone navigation rail, never public sites.
    operator_scope = any(w in text for w in (
        "consola", "console", "panel administrativo", "panel de administr",
        "admin panel", "admin dashboard", "administrative dashboard", "backoffice",
        "back office", "operator workspace", "workspace administrativo",
        "melodiq core", "melodiq-core", "dentalos", "dental os",
        "churchos", "church os", "ops os", "opsos", "b2b-platform",
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
    if whole_site_action and public_website_signal and (public_surface or not operator_scope):
        surfaces.add("frontend")
        archetypes.update(("ui-flow-change", "public-client-website"))
        risks.add("hero-fidelity")
        _evidence(evidence, "text-signal", "archetype", "public-client-website")

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
    if not public_surface and ((operator_scope and (shell_signal or new_console)) or rail_signal):
        surfaces.add("frontend"); archetypes.update(("ui-flow-change", "operator-console-shell-change"))
        risks.add("console-shell-fidelity")
        _evidence(evidence, "text-signal", "archetype", "operator-console-shell-change")
    if any(w in text for w in ("accessibility","a11y","keyboard","focus","reflow","wcag")):
        surfaces.add("frontend"); risks.add("accessibility"); _evidence(evidence,"text-signal","risk","accessibility")
    if any(w in text for w in ("performance","latency","slow","lcp","inp","cls","core web vitals")):
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
    if any(w in text for w in ("schema","column","migration","archived_at")):
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
