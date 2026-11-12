#!/usr/bin/env python3
"""make_walk_cases.py - writes the 23 walk cases and their plan rows for the live proof of the walker (t-2006 sec 1-2).

    python make_walk_cases.py --task-root <the story's folder, qa-factory/artifacts/LOCAL-1> [--cases-dir DIR] [--data FILE]

Reads `walk-cases.json` (next to this script) and the row TS-15 of `<task-root>/work/test-plan.json` (the template of a manual-agent row).
Writes `<cases-dir>/LOCAL-1_TC_1NN.md` (default cases dir: `<project>/test-cases/walk`, the project being `task-root/../../..`) and appends the rows
`TS-1NN` to `rows` of the plan. Idempotent: a file or a row already there is replaced, never doubled. Nothing else is touched.

Text rules (spec t-2006 sec 1): Given/Steps/Thens come from the data only (the cards' steps-by-hand and expected-with-source fields); a silent
requirement gets the observation form (worked example D): one Then, a source word other than `unknown`, `inconclusive` only. No credential value
is ever written: the sign-in sentence names the actor.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "walk-cases.json"
TEMPLATE_ROW = "TS-15"
LOGIN = ('open /login, fill-account [data-testid="login-email-input"] {a} user, '
         'fill-account [data-testid="login-password-input"] {a} secret, click [data-testid="login-submit-button"], '
         "wait for the page to leave /login.")
LOGIN_IF = "If the header shows no signed-in user: " + LOGIN
RESET = "Open /cart and remove every line."
SILENT_THEN = ("NO EXPECTED VALUE - the requirements are silent (P20). Record {observe}. Give this Then `inconclusive` with a `limitation` "
               '"requirement silent" and the facts as observations; never pass or fail.')
BASIS = "experiments/mybooks/add-to-cart-disputed-places.md card {n}"
POLICY_LINE = "Evidence policy: ui; the page, the field values, the messages, the badge and the cart after each action."


def case_id(ticket, card) -> str:
    return f"{ticket}_TC_{100 + int(card)}"


def row_id(card) -> str:
    return f"TS-{100 + int(card)}"


def expand(text: str) -> str:
    """`{LOGIN:<actor>}` -> the sign-in sentence of that actor (a name, never a value)."""
    return re.sub(r"\{LOGIN:([a-z]+)\}", lambda m: "Sign in: " + LOGIN.format(a=m.group(1)), text)


def then_oracles(case, ticket) -> list:
    if case.get("silent") or not case.get("thens"):
        return [{"then": 1, "source": "spec", "ref": f"card {case['card']}: requirement silent; observation only (P20)"}]
    return [{"then": i, "source": t["source"], "ref": t["ref"]} for i, t in enumerate(case["thens"], 1)]


def then_lines(case) -> list:
    if case.get("silent") or not case.get("thens"):
        return [SILENT_THEN.format(observe=case.get("observe") or "what the page shows")]
    return [t["text"] for t in case["thens"]]


def preconditions(case) -> list:
    out = [{"id": "PC-1", "kind": "service", "what": "the stand UI is reachable", "check": {"stand_frontend": "the walk drives the live stand"}}]
    for number, actor in enumerate(case.get("actors") or [], 2):
        name = next(iter(actor.values()))
        what = f"the seed {name} account" if "stand_account" in actor else "the same user in a second browser"
        out.append({"id": f"PC-{number}", "kind": "account", "what": what, "check": actor})
    return out


def case_text(case, ticket, updated) -> str:
    n = case["card"]
    front = [
        "---",
        f"id: {case_id(ticket, n)}",
        f"title: {case['title']}",
        "area: walk",
        "priority: P1",
        "status: Draft",
        "channel: manual-agent",
        "reuse_decision: new",
        f"updated: {updated}",
        f"task: {ticket}",
        "covers: [" + ", ".join(case["covers"]) + "]",
        f"defect_class: {case['defect_class']}",
        f"basis: {BASIS.format(n=n)}",
        "preconditions: " + json.dumps(preconditions(case), ensure_ascii=False),
        "then_oracles: " + json.dumps(then_oracles(case, ticket), ensure_ascii=False),
        "---",
        "",
        "Requirements: " + ", ".join(case["covers"]),
        f"Plan row: {row_id(n)}",
        "",
        POLICY_LINE,
        "",
        "## Given",
        case["given"],
        "",
        "## Steps",
    ]
    steps = []
    for who in case.get("login") or []:
        steps.append(LOGIN_IF.format(a=who))
    if case.get("reset_cart", True):
        steps.append(RESET)
    steps += [expand(s) for s in case["steps"]]
    front += [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    front += ["", "## Then"] + [f"{i}. {t}" for i, t in enumerate(then_lines(case), 1)]
    if case.get("teardown"):
        front += ["", "## Teardown"] + [f"{i}. {t}" for i, t in enumerate(case["teardown"], 1)]
    return "\n".join(front) + "\n"


def make_row(template, case) -> dict:
    n, r = case["card"], case["row"]
    rid, oid, pid = row_id(n), f"OB-{100 + n}", f"P{100 + n}-c1"
    row = copy.deepcopy(template)
    covers = case["covers"]
    row.update({
        "id": rid, "what": f"Walk card {n}: {r['what']}", "requirements": list(covers), "walks": [],
        "defect_hypothesis": f"{case['defect_class']}: {case['title']}",
        "impact": "moderate", "verification_depth": "normal", "design_review_required": False,
        "oracle": r["oracle"], "disposition": "manual-agent", "reason": f"live proof of the walker, t-1957 sec 7; card {n}", "level": "e2e-ui",
        "rung_basis": {"kind": "judgement", "ref": "steps known in advance, walked as a person keys them"},
        "technique": r["technique"], "required_scenarios": list(r["scenarios"]),
        "risk_rationale": f"walk card {n}: {case['title']}", "risk_source_refs": [f"register:{c}" for c in covers],
        "test_level_rationale": "walked on the live stand to prove the walker; the steps are known in advance",
        "observable": f"live-stand:walk card {n}", "source_conflict": False, "oracle_unknown": False,
    })
    ob = copy.deepcopy(template["coverage_obligations"][0])
    ob.update({
        "obligation_id": oid, "oracle_source_ref": BASIS.format(n=n).replace(" card ", "#"),
        "evidence_policy": "ui", "behavior": r["behavior"], "observation_boundary": r["boundary"], "completion_condition": r["completion"],
        "applicable_scenarios": [pid], "oracle_status": "resolved", "decision": "manual-agent", "execution_scope": "current_task",
        "coverage_links": [], "requirement_refs": [{"ref": c, "revision": "r1"} for c in covers], "planned_check_refs": [pid],
    })
    ob["sufficiency_review"] = dict(ob.get("sufficiency_review") or {}, author_dispatch_id="t-2006-walk-prep",
                                    rationale=f"card {n} of the disputed places")
    ob["observation_contract"] = {"claim_kind": ["ordinary"], "oracle_ref": {"ref": covers[0], "revision": "r1"}, "controls": [],
                                  "completion_ref": pid, "independent_expectations": [], "source_conflicts": [],
                                  "surfaces": [{"id": f"S-{100 + n}", "boundary": "UI", "status": "planned", "assertion_ref": pid}]}
    row["coverage_obligations"] = [ob]
    delta = copy.deepcopy(template["coverage_delta"])
    delta["entries"] = [{"obligation_id": oid, "disposition": "gap", "rationale": "walked by hand",
                         "gap_reason": "no automated test planned for the walk"}]
    delta["planned_instance_ids"] = []
    row["coverage_delta"] = delta
    return row


def build(task_root, cases_dir=None, data_path=DATA) -> dict:
    task_root = Path(task_root).resolve()
    data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    cases = sorted(data["cases"], key=lambda c: c["card"])
    plan_path = task_root / "work" / "test-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    rows = plan["rows"]
    template = next((r for r in rows if r.get("id") == TEMPLATE_ROW), None)
    if template is None:
        raise SystemExit(f"the plan {plan_path} has no row {TEMPLATE_ROW} to copy the form of a manual-agent row from")
    target = Path(cases_dir) if cases_dir else task_root.parents[2] / "test-cases" / "walk"
    target.mkdir(parents=True, exist_ok=True)
    ours = {row_id(c["card"]) for c in cases}
    kept = [r for r in rows if r.get("id") not in ours]
    new_rows = [make_row(template, c) for c in cases]
    plan["rows"] = kept + new_rows
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written = []
    for c in cases:
        path = target / f"{case_id(data['ticket'], c['card'])}.md"
        path.write_text(case_text(c, data["ticket"], data["updated"]), encoding="utf-8", newline="\n")
        written.append(path.name)
    return {"cases": written, "rows": [r["id"] for r in new_rows], "target": str(target), "plan": str(plan_path)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-root", required=True)
    parser.add_argument("--cases-dir")
    parser.add_argument("--data", default=str(DATA))
    args = parser.parse_args(argv)
    out = build(args.task_root, args.cases_dir, args.data)
    print(f"{len(out['cases'])} cases written to {out['target']}; {len(out['rows'])} rows set in {out['plan']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
