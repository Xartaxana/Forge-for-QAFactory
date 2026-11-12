#!/usr/bin/env python3
"""check_run.py - the coordinator's post-run acceptance of the walk (t-2006 sec 3 step 13; t-1957 sec 7 step 6). Read-only.

    python check_run.py --task-root <T> [--data walk-cases.json]

For each of the 23 cases of `walk-cases.json`:
  * a result record `work/walks/<W>/<case>.json` exists, and its Thens are exactly the case's Thens;
  * a SILENT case (no expected value) holds only `inconclusive` / `unreached` Thens: a `pass` or `fail` on it is a problem, named;
  * a LIMITED case (14, 21: a step the recorder lacks) holds only `inconclusive` / `unreached` and carries a `limitation`;
  * the record's attempt has a start AND an end probe row (`probes.jsonl`) and detector lines in `surprises.jsonl` (surprise_detection on).
And once: at least one `state/walks/<W>/batches/<case>-b<n>.json` answers `stopped` with a later call (b<n+1>) of the same item.
Failures are listed by name; nothing is written or repaired. Exit 1 on any problem.
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

UNDECIDED = ("inconclusive", "unreached")


def _json(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def _rows(path) -> list:
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def expected_thens(case) -> int:
    return 1 if case.get("silent") or not case.get("thens") else len(case["thens"])


def check_record(task_root, case, cid, record_path) -> list:
    problems = []
    record = _json(record_path)
    if record is None:
        return [f"{cid}: the result record {record_path.name} cannot be read"]
    thens = [t for t in record.get("thens") or [] if isinstance(t, dict)]
    want = set(range(1, expected_thens(case) + 1))
    got = {t.get("n") for t in thens}
    if got != want:
        problems.append(f"{cid}: the record holds Thens {sorted(map(str, got))}, the case has {sorted(want)}")
    undecided_only = bool(case.get("silent") or case.get("limited"))
    if undecided_only:
        kind = "a silent Then" if case.get("silent") else "a limited case"
        for t in thens:
            if t.get("result") not in UNDECIDED:
                problems.append(f"{cid}: Then {t.get('n')} is `{t.get('result')}` on {kind}: only inconclusive / unreached is allowed")
        if case.get("limited") and not str(record.get("limitation") or "").strip():
            problems.append(f"{cid}: a limited case ends inconclusive WITH a limitation; the record names none")
    attempt = str(record.get("attempt") or "")
    adir = task_root / "work" / "evidence" / "manual" / cid / attempt if attempt else None
    if adir is None or not adir.is_dir():
        problems.append(f"{cid}: the attempt '{attempt}' of the record has no folder under work/evidence/manual/{cid}")
        return problems
    whens = {r.get("when") for r in _rows(adir / "probes.jsonl")}
    for need in ("start", "end"):
        if need not in whens:
            problems.append(f"{cid}/{attempt}: no `{need}` probe row in probes.jsonl")
    if not any(r.get("line") == "detector" for r in _rows(adir / "surprises.jsonl")):
        problems.append(f"{cid}/{attempt}: surprise_detection is absent (no `detector` line in surprises.jsonl)")
    return problems


def stopped_then_continued(task_root) -> bool:
    for folder in sorted((task_root / "state" / "walks").glob("*/batches")) if (task_root / "state" / "walks").is_dir() else []:
        numbers = {}
        for path in folder.glob("*-b*.json"):
            found = re.fullmatch(r"(.+)-b([0-9]+)\.json", path.name)
            if found:
                numbers.setdefault(found.group(1), {})[int(found.group(2))] = (_json(path) or {}).get("status")
        for item, by_n in numbers.items():
            if any(status == "stopped" and (n + 1) in by_n for n, status in by_n.items()):
                return True
    return False


def check_run(task_root, data_path=MW.DATA) -> tuple:
    """(records found, problems)."""
    task_root = Path(task_root).resolve()
    data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    problems, found = [], 0
    for case in sorted(data["cases"], key=lambda c: c["card"]):
        cid = MW.case_id(data["ticket"], case["card"])
        records = sorted((task_root / "work" / "walks").glob(f"*/{cid}.json")) if (task_root / "work" / "walks").is_dir() else []
        if not records:
            problems.append(f"{cid}: no result record under work/walks/*/")
            continue
        found += 1
        problems += check_record(task_root, case, cid, records[-1])
    if not stopped_then_continued(task_root):
        problems.append("no stored call answer says `stopped` with a later call of the same item (state/walks/*/batches)")
    return found, problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-root", required=True)
    parser.add_argument("--data", default=str(MW.DATA))
    args = parser.parse_args(argv)
    found, problems = check_run(args.task_root, args.data)
    print(f"{found} records, {len(problems)} problems")
    for line in problems:
        print("  " + line)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
