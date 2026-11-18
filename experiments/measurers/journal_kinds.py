"""Which lines of a driver journal (state/driver-runs.jsonl) are calls and which are bookkeeping.

One list, read by compare.driver_report and report_run.journal (cost-dashboard CD2-1; P18: one
true price). Before this, window_round / process / launched / gate_repair rows were counted as
`claude -p` calls in by_kind / by_role. Kinds match EXACTLY: `Window_Round` is a call. A row whose
kind is absent, empty, not a string or unknown stays a call (no silent drop). A line that is not
JSON is skipped as before, counted nowhere.
"""
import json

SERVICE_KINDS = frozenset({"window_round", "process", "launched", "gate_repair", "held"})


def is_service(row) -> bool:
    return isinstance(row, dict) and isinstance(row.get("kind"), str) and row["kind"] in SERVICE_KINDS


def split_rows(text: str) -> tuple:
    """(call rows, number of bookkeeping rows) of a journal's text."""
    calls, bookkeeping = [], 0
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if is_service(row):
            bookkeeping += 1
        else:
            calls.append(row)
    return calls, bookkeeping
