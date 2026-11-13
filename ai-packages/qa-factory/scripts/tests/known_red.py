"""The `known_red` ledger: one reconcile for every test walk that must go red on a defect of main and still keep CI green.

A walk (P1-a: writer -> reader rounds; P1-b: price/route rows) is meant to turn red on a real defect. The canon on main must
still be green (CI rule), so the reds known today are named in a ledger section of the consumer's JSON fixture. This helper
is the ONE place that reads that section and judges the walk against it (AR-15; the consumers call `load` and `reconcile`
only and write no reconcile, counter or raise door of their own). Interface and outcomes: the P1-a spec, section 3.6.

It is a GATE (it decides whether the canon is green), so it errs only toward red (AR-28): an unknown row, a case-different id,
a kind-level row, a null `raised_by`, a duplicate id are all refusals. Ids are opaque and compared by exact string equality.
Every row names its own `raised_by`, so the number of rows is the ratchet and a raise is always named (AR-20). It writes nothing.
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

NODE_RE = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+[a-z]?$")
ROW_KEYS = ("node", "raised_by", "note")


@dataclass(frozen=True)
class Row:
    node: str
    raised_by: str
    note: str = ""


@dataclass(frozen=True)
class Verdict:
    ok: bool
    problems: tuple
    known: tuple


class LedgerError(ValueError):
    """The ledger cannot be trusted: names the file, the row id and what was expected."""


def _no_duplicates(pairs: list) -> dict:
    # json.loads would silently keep the last of two equal keys, and a duplicate row id is a ledger nobody can trust.
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise LedgerError(f"duplicate key {key!r}: every id appears once")
        out[key] = value
    return out


def load(path, section: str = "known_red") -> dict:
    """The rows of `section` in the JSON file at `path`. A missing section in an existing file is an empty ledger."""
    where = str(path)
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise LedgerError(f"{where}: cannot read the ledger file ({exc.__class__.__name__}); expected a JSON file with a "
                          f"{section!r} object") from exc
    try:
        data = json.loads(text, object_pairs_hook=_no_duplicates)
    except LedgerError as exc:
        raise LedgerError(f"{where}: {exc}") from exc
    except ValueError as exc:
        raise LedgerError(f"{where}: not valid JSON ({exc}); expected a JSON object holding {section!r}") from exc
    if not isinstance(data, dict):
        raise LedgerError(f"{where}: the top level is {type(data).__name__}; expected a JSON object")
    if section not in data:
        return {}
    raw = data[section]
    if not isinstance(raw, dict):
        raise LedgerError(f"{where}: section {section!r} is {type(raw).__name__}; expected an object of id -> row")
    rows: dict = {}
    for rid, body in raw.items():
        if not rid or rid != rid.strip():
            raise LedgerError(f"{where}: row id {rid!r} is empty or has leading/trailing whitespace; expected the walk's "
                              f"id string exactly")
        if not isinstance(body, dict):
            raise LedgerError(f"{where}: row {rid!r} is {type(body).__name__}; expected an object with node and raised_by")
        extra = sorted(set(body) - set(ROW_KEYS))
        if extra:
            raise LedgerError(f"{where}: row {rid!r} has unknown key(s) {extra}; expected only {list(ROW_KEYS)}")
        node = body.get("node")
        if not isinstance(node, str) or not NODE_RE.match(node):
            raise LedgerError(f"{where}: row {rid!r} node {node!r}; expected an id like FV1-1 (pattern {NODE_RE.pattern})")
        raised = body.get("raised_by")
        if not isinstance(raised, str) or not raised.strip():
            raise LedgerError(f"{where}: row {rid!r} raised_by {raised!r}; expected a non-empty string naming who allowed "
                              f"this raise (a critic verdict path or 'Lead, <date>')")
        note = body.get("note", "")
        if not isinstance(note, str):
            raise LedgerError(f"{where}: row {rid!r} note is {type(note).__name__}; expected a string")
        rows[rid] = Row(node=node, raised_by=raised, note=note)
    return rows


def reconcile(results: Mapping, ledger: Mapping, *, ledger_path: str) -> Verdict:
    """Judge a walk (`id -> True` green / `False` red; a crash counts as red) against the ledger.

    Only the exact value True is green: anything else is red, so the error can only go toward red.
    """
    problems: list = []
    known: list = []
    for rid in results:
        green = results[rid] is True
        if rid in ledger:
            if green:
                problems.append((rid, f"stale: {rid} is green; remove its known_red row (node {ledger[rid].node}) in this commit"))
            else:
                known.append((rid, f"known red: {rid} -> {ledger[rid].node}"))
        elif not green:
            problems.append((rid, f'new red: {rid} — fix it, or add "{rid}": {{"node": "<FV1-n or node id>", '
                                  f'"raised_by": "<verdict or word that names this raise>"}} to {ledger_path} known_red'))
    for rid in ledger:
        if rid not in results:
            problems.append((rid, f"unknown row: {rid} is not a row of this walk; rename it to the walk's id or remove it"))
    return Verdict(ok=not problems,
                   problems=tuple(msg for _rid, msg in sorted(problems, key=lambda item: item[0])),
                   known=tuple(msg for _rid, msg in sorted(known, key=lambda item: item[0])))
