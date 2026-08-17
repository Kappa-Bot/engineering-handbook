import json
import tempfile
import unittest
from pathlib import Path

from automation.engineering_context.canonical import canonical_json, stable_hash
from automation.engineering_context.handbook_source import AgentContextError, extract_agent_context
from automation.engineering_context.handbook_compile import compile_handbook, check_compiled_fresh
from automation.engineering_context.task_descriptor import describe_task
from automation.engineering_context.context_solver import solve_context, build_repo_route
from automation.engineering_context.planning_ir import PlanningIR, VerificationRequirement, new_planning_ir, validate_planning_ir, capsule_delta
from automation.engineering_context.conformance import project_conformance


def source_doc(source_id, units, prose="Canonical prose"):
    return f'''---\nid: {source_id}\n---\n\n# X\n\n{prose}\n\n```json agent-context\n{json.dumps({"units": units}, indent=2)}\n```\n'''


def unit(uid, covers=(), activate_when=(), *, activate_all=(), phase=("planning",), force=None, priority=50, kind="decision-question"):
    data = {"id": uid, "type": kind, "text": f"{uid} text", "source": "std-test", "covers": list(covers), "activate_when": list(activate_when), "phase": list(phase), "priority": priority}
    if activate_all:
        data["activate_all"] = list(activate_all)
    if force:
        data["force"] = force
    return data


class PipelineContractTests(unittest.TestCase):
    def test_canonical_json_and_hash_are_order_stable(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}\n')
        self.assertEqual(stable_hash({"a":1,"b":2}), stable_hash({"b":2,"a":1}))

    def test_source_parser_ignores_free_prose(self):
        self.assertEqual(extract_agent_context("# prose only", "x.md"), [])

    def test_source_parser_rejects_source_mismatch(self):
        bad = unit("u")
        bad["source"] = "wrong"
        with self.assertRaises(AgentContextError):
            extract_agent_context(source_doc("std-test", [bad]), "x.md")

    def test_compiler_is_byte_stable_and_prose_only_change_does_not_invalidate_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"standards").mkdir(); out=root/"compiled"
            u=unit("u", ("compatibility",), ("risk:compatibility",))
            path=root/"standards/x.md"; path.write_text(source_doc("std-test", [u], "first prose"))
            compile_handbook(root,out); before={p.name:p.read_bytes() for p in out.iterdir()}
            second=compile_handbook(root,out)
            self.assertEqual(second.changed_files, ())
            path.write_text(source_doc("std-test", [u], "editorial prose changed"))
            third=compile_handbook(root,out); after={p.name:p.read_bytes() for p in out.iterdir()}
            self.assertEqual(third.changed_files, ())
            self.assertEqual(before, after)
            self.assertEqual(check_compiled_fresh(root,out), [])

    def test_activate_all_requires_every_predicate(self):
        u=unit("pwa-mutation", ("data-loss",), (), activate_all=("capability:pwa","operation:mutation"))
        compiled={"units":[{**u,"sources":["std-test"],"estimated_tokens":10}],"routing":{"capability:pwa":["pwa-mutation"],"operation:mutation":["pwa-mutation"]}}
        only_mutation=describe_task("update record", {"detected":{"capabilities":{"persistence":True}}})
        self.assertEqual(solve_context(compiled, only_mutation, "planning").units, ())

    def test_repo_capability_is_not_automatically_task_capability(self):
        d=describe_task("fix visual spacing", {"detected":{"capabilities":{"pwa":True,"persistence":True,"auth":True}}})
        self.assertNotIn("pwa", d.capabilities)
        self.assertNotIn("persistence", d.capabilities)
        self.assertIn("accessibility", d.risks)

    def test_migration_descriptor_adds_direct_risks(self):
        d=describe_task("add archived_at column and migration", {"detected":{"capabilities":{"persistence":True}}})
        self.assertTrue(d.state["migration"])
        self.assertIn("persistence", d.capabilities)
        self.assertEqual(set(d.risks), {"compatibility","data-loss"})

    def test_expiring_invitation_is_deterministically_credential_sensitive(self):
        d=describe_task("add expiring tenant invitation links", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        self.assertEqual(set(d.risks), {"authorization","credential","tenant-isolation"})
        self.assertEqual(d.uncertain, ())

    def test_generic_invitation_keeps_constrained_uncertainty(self):
        d=describe_task("add tenant invitation", {"detected":{"capabilities":{"persistence":True,"auth":True}}})
        self.assertEqual(d.uncertain[0]["allowed"], ["credential","not-credential","unknown"])

    def test_solver_prefers_dense_direct_coverage_and_does_not_fill_budget(self):
        units=[]
        for raw in [
            unit("dense", ("authorization","tenant-isolation"), ("risk:authorization",), force="must", priority=90),
            unit("partial-a", ("authorization",), ("risk:authorization",), force="must", priority=100),
            unit("partial-b", ("tenant-isolation",), ("risk:tenant-isolation",), force="must", priority=100),
            unit("optional", (), ("risk:authorization",), priority=100),
        ]:
            raw["sources"]=["std-test"]; raw["estimated_tokens"]=20; units.append(raw)
        compiled={"units":units,"routing":{"risk:authorization":["dense","partial-a","optional"],"risk:tenant-isolation":["partial-b"]}}
        d=describe_task("tenant permission", {"detected":{"capabilities":{}}})
        capsule=solve_context(compiled,d,"planning")
        ids=[x["id"] for x in capsule.units]
        self.assertIn("dense", ids)
        self.assertNotIn("optional", ids)
        self.assertEqual(capsule.uncovered, ())

    def test_repo_route_is_narrow(self):
        profile={"detected":{"landmarks":{"migrations":["migrations"],"tests":["tests"]},"commands":{"test":"pytest"}},"declared":{"landmarks":{}}}
        d=describe_task("add archived_at column and migration", {"detected":{"capabilities":{"persistence":True}}})
        route=build_repo_route(profile,d)
        self.assertIn("migrations", route["inspect_first"])
        self.assertIn("pwa", route["avoid_by_default"])

    def test_planning_ir_surfaces_uncovered_risk(self):
        d=describe_task("reduce API latency", {"detected":{"capabilities":{}}})
        capsule=solve_context({"units":[],"routing":{}},d,"planning")
        ir=new_planning_ir(d,capsule)
        self.assertTrue(any(x.get("id","").startswith("uncovered:") for x in ir.unresolved))

    def test_plan_validator_requires_authz_decision(self):
        ir=PlanningIR.for_test(risks=("tenant-isolation",), decisions=())
        self.assertIn("missing-authorization-decision", {i.code for i in validate_planning_ir(ir)})

    def test_plan_validator_requires_migration_evidence(self):
        ir=PlanningIR.for_test(migration=True, verification=())
        self.assertIn("missing-migration-verification", {i.code for i in validate_planning_ir(ir)})

    def test_context_delta_only_sends_added_units(self):
        from automation.engineering_context.context_solver import ContextCapsule
        current=ContextCapsule("new","planning",({"id":"a"},{"id":"b"}),(),(),1,(),())
        delta=capsule_delta("old", {"a"}, current)
        self.assertEqual([x["id"] for x in delta["added_units"]], ["b"])
        self.assertEqual(delta["unchanged_unit_count"],1)

    def test_conformance_does_not_treat_not_run_as_passed(self):
        class C: required_evidence=("authz-negative",)
        ir=PlanningIR.for_test(verification=(VerificationRequirement("authz-negative"),))
        result=project_conformance(C(),ir,({"id":"authz-negative","status":"not-run"},))
        self.assertEqual(result["demonstrated"], [])
        self.assertEqual(result["gaps"], ["authz-negative"])

    def test_not_applicable_requires_reason(self):
        class C: required_evidence=("x",)
        ir=PlanningIR.for_test()
        with self.assertRaises(ValueError):
            project_conformance(C(),ir,({"id":"x","status":"not-applicable"},))


if __name__ == "__main__":
    unittest.main()
