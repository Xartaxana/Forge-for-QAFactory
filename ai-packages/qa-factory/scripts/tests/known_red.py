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
WORLD_SECTION = "not_in_world"           # the second ratcheted section: a row that names a gap of the round's WORLD, not a defect of main
WORLD_KEYS = ("reason", "raised_by")


@dataclass(frozen=True)
class Row:
    node: str
    raised_by: str
    note: str = ""
    reason: str = ""                     # `not_in_world` rows only: why the round's world lacks the input


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


def _read(path, section: str):
    """The parsed top-level object of the JSON file at `path` (duplicate keys refused); a LedgerError names the file."""
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
    return data


def load(path, section: str = "known_red") -> dict:
    """The rows of `section` in the JSON file at `path`: ONE loader for both ratcheted sections (`known_red`: node + raised_by [+ note];
    `not_in_world`: reason + raised_by). A missing section in an existing file is an empty ledger."""
    where = str(path)
    data = _read(path, section)
    if section not in data:
        return {}
    raw = data[section]
    if not isinstance(raw, dict):
        raise LedgerError(f"{where}: section {section!r} is {type(raw).__name__}; expected an object of id -> row")
    world = section == WORLD_SECTION
    keys = WORLD_KEYS if world else ROW_KEYS
    rows: dict = {}
    for rid, body in raw.items():
        if not rid or rid != rid.strip():
            raise LedgerError(f"{where}: row id {rid!r} is empty or has leading/trailing whitespace; expected the walk's "
                              f"id string exactly")
        if not isinstance(body, dict):
            raise LedgerError(f"{where}: row {rid!r} is {type(body).__name__}; expected an object with {' and '.join(keys[:2])}")
        extra = sorted(set(body) - set(keys))
        if extra:
            raise LedgerError(f"{where}: row {rid!r} has unknown key(s) {extra}; expected only {list(keys)}")
        raised = body.get("raised_by")
        if not isinstance(raised, str) or not raised.strip():
            raise LedgerError(f"{where}: row {rid!r} raised_by {raised!r}; expected a non-empty string naming who allowed "
                              f"this raise (a critic verdict path or 'Lead, <date>')")
        if world:
            reason = body.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise LedgerError(f"{where}: row {rid!r} reason {reason!r}; expected a non-empty string saying what the world lacks")
            rows[rid] = Row(node="", raised_by=raised, reason=reason)
            continue
        node = body.get("node")
        if not isinstance(node, str) or not NODE_RE.match(node):
            raise LedgerError(f"{where}: row {rid!r} node {node!r}; expected an id like FV1-1 (pattern {NODE_RE.pattern})")
        note = body.get("note", "")
        if not isinstance(note, str):
            raise LedgerError(f"{where}: row {rid!r} note is {type(note).__name__}; expected a string")
        rows[rid] = Row(node=node, raised_by=raised, note=note)
    return rows


def pin_problem(path, section: str, count: int):
    """None when `pins.<section>` of the file equals `count`, else the sentence that fails the check. The pin is a shrink-only ratchet
    in BOTH directions, the same strictness as the file's other pins (equality): a count above it is a raise nobody named in this commit,
    a count below it is a stale pin that must be lowered. A pin that is absent or not an int (a bool is not one) never passes (AR-28)."""
    data = _read(path, section)
    pins = data.get("pins")
    pin = pins.get(section) if isinstance(pins, dict) else None
    if not isinstance(pin, int) or isinstance(pin, bool):
        return f"pins.{section} is {pin!r}; expected an int in {path} (the number of {section} rows, currently {count})"
    if count > pin:
        return f"{section} holds {count} rows, above pins.{section} {pin}: a raise is named in the verdict and edits the pin in the same commit"
    if count < pin:
        return f"stale pin: {section} holds {count} rows, below pins.{section} {pin}: lower the pin to {count}"
    return None


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
