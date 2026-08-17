from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .canonical import context_id
from .task_descriptor import TaskDescriptor

@dataclass(frozen=True)
class ContextBudget:
    target:int=600
    soft_max:int=900
    hard_max:int=1400
    reserve:int=250
DEFAULT_BUDGET=ContextBudget()

@dataclass(frozen=True)
class ContextCapsule:
    id:str
    phase:str
    units:tuple[dict[str,Any],...]
    covered:tuple[str,...]
    uncovered:tuple[str,...]
    estimated_tokens:int
    escalations:tuple[dict[str,Any],...]
    provenance:tuple[str,...]
    required_evidence:tuple[str,...]=()
    candidate_count:int=0

    def to_dict(self)->dict[str,Any]:
        return {"id":self.id,"phase":self.phase,"units":[dict(x) for x in self.units],"covered":list(self.covered),"uncovered":list(self.uncovered),"estimated_tokens":self.estimated_tokens,"escalations":[dict(x) for x in self.escalations],"provenance":list(self.provenance),"required_evidence":list(self.required_evidence),"candidate_count":self.candidate_count}

def _descriptor_tags(d:TaskDescriptor)->set[str]: return d.predicates()

def _unit_matches(unit:dict[str,Any], tags:set[str], phase:str)->bool:
    phases=set(unit.get("phase",[]))
    if phases and phase not in phases:return False
    excludes=set(unit.get("excludes",[]))
    if excludes & tags:return False
    activates=set(unit.get("activate_when",[]))
    activate_all=set(unit.get("activate_all",[]))
    any_ok = not activates or bool(activates & tags)
    all_ok = not activate_all or activate_all.issubset(tags)
    return any_ok and all_ok

def _dedupe(units:list[dict[str,Any]])->list[dict[str,Any]]:
    merged={}
    for u in units:
        uid=u["id"]
        if uid not in merged: merged[uid]=dict(u); continue
        merged[uid]["sources"]=sorted(set(merged[uid].get("sources",[]))|set(u.get("sources",[])))
    return [merged[k] for k in sorted(merged)]

def _candidate_units(compiled:dict[str,Any], descriptor:TaskDescriptor, phase:str)->list[dict[str,Any]]:
    units=compiled.get("units",[])
    routing=compiled.get("routing",{})
    tags=_descriptor_tags(descriptor)
    if routing:
        ids=set()
        for tag in tags: ids.update(routing.get(tag,[]))
        by_id={u["id"]:u for u in units}
        candidates=[by_id[i] for i in sorted(ids) if i in by_id]
    else:
        candidates=list(units)
    return _dedupe([u for u in candidates if _unit_matches(u,tags,phase)])

def solve_context(compiled:dict[str,Any], descriptor:TaskDescriptor, phase:str, budget:ContextBudget=DEFAULT_BUDGET)->ContextCapsule:
    if phase not in {"planning","implementation","verification"}: raise ValueError("invalid phase")
    candidates=_candidate_units(compiled,descriptor,phase)
    required=set(descriptor.risks)
    covered:set[str]=set(); selected:list[dict[str,Any]]=[]; escalations=[]; total=0
    by_id={u["id"]:u for u in candidates}

    dependency_ids=set()
    for u in candidates: dependency_ids.update(u.get("requires",[]))
    all_units={u["id"]:u for u in compiled.get("units",[])}
    for rid in sorted(dependency_ids):
        u=all_units.get(rid)
        if u and _unit_matches(u,_descriptor_tags(descriptor),phase) and rid not in by_id:
            candidates.append(u); by_id[rid]=u

    remaining=list(candidates)
    force_weight={"must":4.0,"must-not":4.0,"should":1.5,"may":1.0,None:1.0}
    while required-covered:
        best=None; best_key=None
        for u in remaining:
            new=set(u.get("covers",[]))&(required-covered)
            if not new: continue
            cost=max(1,int(u.get("estimated_tokens",1))); priority=max(1,int(u.get("priority",50)))
            score=((len(new)**2)*priority*force_weight.get(u.get("force"),1.0))/cost
            key=(score,-cost,u["id"])
            if best is None or key>best_key:
                best=u;best_key=key
        if best is None: break
        cost=int(best.get("estimated_tokens",0)); projected=total+cost
        if projected>budget.hard_max and best.get("force") not in {"must","must-not"}:
            break
        if projected>budget.hard_max:
            escalations.append({"type":"hard-budget-crossed","unit":best["id"],"estimated_tokens":projected})
        selected.append(best); total=projected; covered.update(set(best.get("covers",[]))&required); remaining=[u for u in remaining if u["id"]!=best["id"]]

    # After minimum risk coverage, include only directly applicable normative requirements.
    # Do not fill spare budget with optional guidance: unused tokens are a feature.
    generic_prefixes=("intent:",)
    tags=_descriptor_tags(descriptor)
    for u in sorted(remaining,key=lambda x:(-int(x.get("priority",50)),int(x.get("estimated_tokens",1)),x["id"])):
        if u.get("force") not in {"must","must-not"}: continue
        activates=set(u.get("activate_when",[])) | set(u.get("activate_all",[]))
        specific={a for a in activates if not a.startswith(generic_prefixes)}
        if not (specific & tags): continue
        cost=int(u.get("estimated_tokens",0))
        if total+cost>budget.hard_max:
            escalations.append({"type":"normative-budget-crossed","unit":u["id"],"estimated_tokens":total+cost})
            continue
        selected.append(u); total+=cost

    uncovered=tuple(sorted(required-covered))
    if uncovered: escalations.append({"type":"uncovered-required","risks":list(uncovered),"action":"load canonical guidance or resolve explicitly"})
    selected=_dedupe(selected)
    provenance=tuple(sorted({s for u in selected for s in u.get("sources",[u.get("source")]) if s}))
    evidence=tuple(sorted(u["id"] for u in selected if u.get("type")=="verification"))
    cid=context_id(phase,descriptor.id,[u["id"] for u in selected],uncovered)
    return ContextCapsule(cid,phase,tuple(selected),tuple(sorted(covered)),uncovered,total,tuple(escalations),provenance,evidence,len(candidates))

ARCTYPE_ROUTE={
    "authenticated-mutation":{"inspect_first":["domain-mutation","authorization-boundary","persistence-owner","nearest-tests"],"avoid":["pwa"]},
    "schema-change":{"inspect_first":["persistence-owner","migrations","nearest-tests"],"avoid":["pwa"]},
    "external-integration":{"inspect_first":["integration-boundary","domain-owner","nearest-tests"],"avoid":[]},
    "ui-flow-change":{"inspect_first":["ui-surface","design-primitives","nearest-tests"],"avoid":["database"]},
    "visual-regression-fix":{"inspect_first":["ui-surface","design-primitives","nearest-tests"],"avoid":["database","pwa"]},
    "pwa-capability-change":{"inspect_first":["pwa","ui-surface","nearest-tests"],"avoid":[]},
    "production-release":{"inspect_first":["ci","release-config","verification"],"avoid":[]},
    "background-job":{"inspect_first":["domain-owner","persistence-owner","nearest-tests"],"avoid":["pwa"]},
    "modify-domain-state":{"inspect_first":["domain-owner","persistence-owner","nearest-tests"],"avoid":["pwa"]},
    "add-crud-capability":{"inspect_first":["domain-owner","persistence-owner","nearest-tests"],"avoid":[]},
}

def build_repo_route(profile:dict, descriptor:TaskDescriptor)->dict[str,Any]:
    inspect=[];avoid=[]
    for a in descriptor.archetypes:
        spec=ARCTYPE_ROUTE.get(a,{})
        inspect.extend(spec.get("inspect_first",[]));avoid.extend(spec.get("avoid",[]))
    if "authorization" in descriptor.risks: inspect.append("authorization-boundary")
    if descriptor.state.get("migration"): inspect.extend(["persistence-owner","migrations"])
    landmarks={**profile.get("detected",{}).get("landmarks",{}),**profile.get("declared",{}).get("landmarks",{})}
    resolved={label:landmarks.get(label,[]) for label in sorted(set(inspect))}
    commands=profile.get("detected",{}).get("commands",{})
    verification=[]
    if "authorization" in descriptor.risks: verification.append("authorization-negative")
    if "tenant-isolation" in descriptor.risks: verification.append("cross-tenant-negative")
    if "credential" in descriptor.risks: verification.append("credential-lifecycle")
    if descriptor.state.get("migration"): verification.append("migration-validation")
    return {"inspect_first":sorted(set(inspect)),"resolved":resolved,"inspect_if":[],"avoid_by_default":sorted(set(avoid)),"commands":commands,"verification":verification}
