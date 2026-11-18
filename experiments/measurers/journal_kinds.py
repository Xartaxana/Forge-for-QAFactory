"""Which lines of a driver journal (state/driver-runs.jsonl) are calls and which are bookkeeping.

The ONE measurer-side reader of `no_call_kinds` in the package data
references/driver-journal-kinds.json (the CL4-1 N1 row, also read by scripts/task_price.py);
compare.driver_report and report_run.journal_from both go through it (cost-dashboard CD2-1; P18:
one true price). There is NO fallback list: a fallback would be a second list, so an unreadable
file stops the measurer (require(): one line, exit 2). Kinds match EXACTLY: `Window_Round` is a
call. A row whose kind is absent, empty, not a string or unknown stays a call (no silent drop).
A line that is not JSON is skipped, counted nowhere.
"""
import json
import sys

import paths

KINDS_PATH = paths.PACKAGE / "references" / "driver-journal-kinds.json"


class KindsError(Exception):
    pass


def service_kinds(path=None) -> frozenset:
    path = path or KINDS_PATH
    try:
        table = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:     # UnicodeDecodeError is a ValueError
        raise KindsError(f"cannot read service kinds: {path}: {exc.__class__.__name__}") from None
    kinds = table.get("no_call_kinds") if isinstance(table, dict) else None
    if not isinstance(kinds, list) or not all(isinstance(k, str) for k in kinds):
        raise KindsError(f"cannot read service kinds: {path}: no_call_kinds is absent or not a list of strings")
    return frozenset(kinds)


def require(path=None) -> frozenset:
    """For a measurer's main(): the kinds, or one line on stderr and exit code 2."""
    try:
        return service_kinds(path)
    except KindsError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(2) from None


def split_rows(text: str, path=None) -> tuple:
    """(call rows, number of bookkeeping rows) of a journal's text."""
    kinds = service_kinds(path)
    calls, bookkeeping = [], 0
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and isinstance(row.get("kind"), str) and row["kind"] in kinds:
            bookkeeping += 1
        else:
            calls.append(row)
    return calls, bookkeeping
