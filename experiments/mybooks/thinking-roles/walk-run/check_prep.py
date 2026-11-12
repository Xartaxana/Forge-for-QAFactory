#!/usr/bin/env python3
"""check_prep.py - read-only checks of the walk preparation (t-2006 sec 3 steps 3 and 8).

    python check_prep.py --task-root <T> --stage cases [--cases-dir DIR] [--package-scripts DIR] [--no-validate]
    python check_prep.py --task-root <T> --stage ready --package-scripts DIR

stage `cases` (before the state changes): every case of `walk-cases.json` has its file; the file's `then_oracles` words are all inside the
package's THEN_ORACLE_WORDS and number the same as its `## Then` items (a silent case still has one); its `covers` meets the
`requirements` of its plan row; the plan holds the row; `planning_contract.validate_plan` is clean on the new rows only.
Prints `<n> cases, <m> problems`; exit 1 when m > 0, each problem naming the case. The validate_plan run needs the package scripts
(`--package-scripts`); without them that part is NOT passed silently (AR-28): it is a problem, unless `--no-validate` says so out loud.

stage `ready` (after gate A is recorded): calls `manual_evidence.prepare_request` for each case with the obligations the plan maps to it and
prints `<n> prepared, <m> refused, <k> unprepared` with the refusal words. It writes nothing. Exit 1 unless all are prepared.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_walk_cases as MW  # noqa: E402

# Mirror of contract.THEN_ORACLE_WORDS (package contract.py:894); with --package-scripts the package's own tuple is used.
THEN_ORACLE_WORDS = ("requirement", "ac", "spec", "precedent", "person", "unknown")
THEN_ITEM = re.compile(r"^\s*([0-9]+)[.)]\s+(.*\S)\s*$")
FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)


def front_line(text: str, key: str):
    block = FRONT.match(text)
    if not block:
        return None
    found = re.search(r"(?m)^" + re.escape(key) + r":[ \t]*(.*?)[ \t]*$", block.group(1))
    return found.group(1) if found else None


def then_items(text: str) -> list:
    out, inside = [], False
    for line in text.splitlines():
        if line.strip().startswith("## "):
            inside = line.strip().lower().startswith("## then")
            continue
        found = THEN_ITEM.match(line) if inside else None
        if found:
            out.append(found.group(2))
    return out


def load_package(scripts_dir):
    """The package's scripts on sys.path; returns (contract module words, planning_contract) or (None, why)."""
    if not scripts_dir:
        return None, "no --package-scripts given"
    path = Path(scripts_dir)
    if not (path / "planning_contract.py").is_file():
        return None, f"{path} holds no planning_contract.py"
    sys.path.insert(0, str(path))
    try:
        import planning_contract  # noqa: WPS433
        import contract
    except Exception as exc:  # noqa: BLE001 - reported, not hidden
        return None, f"the package scripts could not be imported ({type(exc).__name__}: {exc})"
    return (tuple(getattr(contract, "THEN_ORACLE_WORDS", THEN_ORACLE_WORDS)), planning_contract), ""


def check_cases(task_root, cases_dir=None, scripts_dir=None, data_path=MW.DATA, validate=True) -> tuple:
    """(n cases, problems)."""
    task_root = Path(task_root).resolve()
    data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    target = Path(cases_dir) if cases_dir else task_root.parents[2] / "test-cases" / "walk"
    plan = json.loads((task_root / "work" / "test-plan.json").read_text(encoding="utf-8"))
    rows = {r.get("id"): r for r in plan.get("rows") or []}
    words, planning = THEN_ORACLE_WORDS, None
    problems = []
    if validate:
        loaded, why = load_package(scripts_dir)
        if loaded is None:
            problems.append(f"validate_plan was not run: {why} (give --package-scripts, or --no-validate to say it is skipped)")
        else:
            words, planning = loaded
    new_rows = []
    for case in sorted(data["cases"], key=lambda c: c["card"]):
        cid = MW.case_id(data["ticket"], case["card"])
        path = target / f"{cid}.md"
        if not path.is_file():
            problems.append(f"{cid}: the case file is missing ({path})")
            continue
        text = path.read_text(encoding="utf-8")
        raw = front_line(text, "then_oracles")
        try:
            oracles = json.loads(raw) if raw is not None else None
        except ValueError:
            oracles = None
        if not isinstance(oracles, list) or not oracles:
            problems.append(f"{cid}: `then_oracles` is missing or is not one line of JSON")
            oracles = []
        for entry in oracles:
            source = str((entry or {}).get("source") or "").strip()
            if source not in words:
                problems.append(f"{cid}: Then {entry.get('then')} has the source word '{source}', outside THEN_ORACLE_WORDS ({' | '.join(words)})")
        thens = then_items(text)
        if not thens:
            problems.append(f"{cid}: the case has no `## Then` item")
        elif len(thens) != len(oracles):
            problems.append(f"{cid}: {len(thens)} Then item(s) but {len(oracles)} `then_oracles` entr(ies)")
        covers = re.findall(r"R-[0-9]+", front_line(text, "covers") or "")
        row = rows.get(MW.row_id(case["card"]))
        if row is None:
            problems.append(f"{cid}: the plan holds no row {MW.row_id(case['card'])}")
            continue
        new_rows.append(row)
        refs = {ref.get("ref") for ob in row.get("coverage_obligations") or [] for ref in ob.get("requirement_refs") or [] if isinstance(ref, dict)}
        if not covers or not (set(covers) & refs):
            problems.append(f"{cid}: `covers` {covers} meets no requirement_refs of {row.get('id')} ({sorted(r for r in refs if r)})")
        if not any(ob.get("decision") == "manual-agent" and ob.get("evidence_policy") == "ui" for ob in row.get("coverage_obligations") or []):
            problems.append(f"{cid}: the row {row.get('id')} is not a manual-agent obligation with the evidence policy word `ui`")
    if planning is not None and new_rows:
        problems += [f"plan: {error}" for error in planning.validate_plan(new_rows)]
    return len(data["cases"]), problems


def check_ready(task_root, case_ids, ME, C, plan_rows) -> dict:
    """Runs `ME.prepare_request` for each case; {prepared: [...], refused: [(case, words)], unprepared: [(case, words)]}. Writes nothing."""
    task = Path(task_root).resolve()
    rows = plan_rows(task)
    out = {"prepared": [], "refused": [], "unprepared": []}
    for case in case_ids:
        try:
            ids = sorted(ME._case_obligation_mapping(task, rows, case))
            ME.prepare_request(task, case, ids)
            out["prepared"].append(case)
        except ME.Refused as exc:
            out["unprepared" if getattr(exc, "walkable", False) else "refused"].append((case, str(exc)))
        except Exception as exc:  # noqa: BLE001 - a crash is a refusal with its type, never a pass
            out["refused"].append((case, f"{type(exc).__name__}: {' '.join(str(exc).split())[:300]}"))
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-root", required=True)
    parser.add_argument("--stage", required=True, choices=["cases", "ready"])
    parser.add_argument("--cases-dir")
    parser.add_argument("--package-scripts")
    parser.add_argument("--no-validate", action="store_true")
    parser.add_argument("--data", default=str(MW.DATA))
    args = parser.parse_args(argv)
    if args.stage == "cases":
        n, problems = check_cases(args.task_root, args.cases_dir, args.package_scripts, args.data, validate=not args.no_validate)
        print(f"{n} cases, {len(problems)} problems")
        for line in problems:
            print("  " + line)
        return 1 if problems else 0
    loaded, why = load_package(args.package_scripts)
    if loaded is None:
        print(f"ready: the package scripts are needed ({why})")
        return 1
    import contract as C  # noqa: WPS433
    import manual_evidence as ME  # noqa: WPS433
    from coverage_contract import plan_rows  # noqa: WPS433
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    ids = [MW.case_id(data["ticket"], c["card"]) for c in sorted(data["cases"], key=lambda c: c["card"])]
    got = check_ready(args.task_root, ids, ME, C, plan_rows)
    print(f"{len(got['prepared'])} prepared, {len(got['refused'])} refused, {len(got['unprepared'])} unprepared")
    for case, words in got["refused"] + got["unprepared"]:
        print(f"  {case}: {words}")
    return 0 if len(got["prepared"]) == len(ids) else 1


if __name__ == "__main__":
    sys.exit(main())
