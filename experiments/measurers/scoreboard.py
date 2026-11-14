#!/usr/bin/env python3
"""The run scoreboard of the forge (P1-v N6): assemble, compare, norms.

    python -B experiments/measurers/scoreboard.py assemble --task-root <the story's folder> --stand S --story T --arm factory \\
        --version V [--truth truth.yaml --judgment judgment.yaml] [--bar bar-<model>.yaml] [--model M] [--pass NORM WORD DATE]
    python -B experiments/measurers/scoreboard.py compare <scoreboard.yaml> [--previous FILE] [--bar FILE] [--findings]
    python -B experiments/measurers/scoreboard.py norms --check [--against OLD-norms.json]

One run, one YAML file `experiments/scoreboards/<stand>/<story>/<YYYYMMDD-HHMM>-<version>-<arm>.yaml` (UTC start). The COUNTERS are the
package's `run_counters.counters(task_root)` (imported through `paths.SCRIPTS`, precedent `code_friction.py`): this file parses no
`driver-*.jsonl` of its own (AR-13), it only hashes and counts the lines of the carriers it names under `run.sources`. The ROWS (which
counter, which unit, which direction is better) are data: `experiments/scoreboards/rows.json`; the NORMS are data:
`experiments/scoreboards/norms.json`, tighten-only (`norms --check`, K5; a raise needs `raised_by`, `reason` and the owner's `word`).
Money is a row (the owner, 13.11.2026): X1 is `task_price.task_price`, never a sum of cumulative `total_cost_usd`.

Invariants (spec 7.4-7.10): an unknown counter stays `unknown` in the row and in the comparison, never 0 and never a pass (FR-41);
a comparison is one metric per line; a dry/smoke/unknown/mixed run is never compared with a live one and judges no norm (K7);
an unreadable or absent rows/norms file is a red line naming it; an empty run folder or a broken judgment file is a refusal and
NOTHING is written; the same input gives the same bytes (no clock is read).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import paths

# The package's counters, found through paths.SCRIPTS (precedent: code_friction.py). At the END of sys.path so a package script can
# never shadow this folder's own modules. Absent: fail loudly naming the path, there is no local copy to fall back on.
for _name in ("run_counters.py", "task_price.py"):
    if not (paths.SCRIPTS / _name).is_file():
        raise ImportError("scoreboard: the package module is absent: %s (expected under ai-packages/qa-factory/scripts, found through "
                          "paths.SCRIPTS)" % (paths.SCRIPTS / _name))
if str(paths.SCRIPTS) not in sys.path:
    sys.path.append(str(paths.SCRIPTS))
import run_counters as RC  # noqa: E402
import task_price as TP  # noqa: E402
import yaml  # noqa: E402

SCOREBOARDS = paths.REPO / "experiments" / "scoreboards"
ROWS_FILE = SCOREBOARDS / "rows.json"
NORMS_FILE = SCOREBOARDS / "norms.json"
PILES = paths.REPO / "plans" / "piles"
SCHEMA = "scoreboard/1"
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
FILE_NAME = re.compile(r"(\d{8}-\d{4})-(.+)\.yaml")
SIMULATED = ("dry", "smoke")
MAX_NAMED = 20                      # a refusal names at most this many offending rows, then says how many more
SOURCES = (("driver-runs.jsonl", "driver_runs"), ("driver-questions.jsonl", "questions"), ("driver-answers.jsonl", "answers"),
           ("passed-by-person.jsonl", "passed_by_person"), ("brief-sizes.jsonl", "brief_sizes"), ("driver-timings.jsonl", "timings"))
MISSING = object()


class Refusal(Exception):
    """A refusal that names what is wrong; nothing is written."""


# --------------------------------------------------------------------------------------- reading the data files

def _read_text(path, what: str) -> str:
    path = Path(path)
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        raise Refusal(f"{what} {path} is absent")
    except UnicodeDecodeError as exc:
        raise Refusal(f"{what} {path} is not UTF-8 text ({exc.reason} at byte {exc.start})")
    except OSError as exc:
        raise Refusal(f"{what} {path} cannot be read ({exc.__class__.__name__})")


def _load_json(path, what: str) -> dict:
    text = _read_text(path, what)
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise Refusal(f"{what} {path} is not JSON ({exc})")
    if not isinstance(data, dict):
        raise Refusal(f"{what} {path} must hold one JSON object")
    return data


def _load_yaml(path, what: str) -> dict:
    text = _read_text(path, what)
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise Refusal(f"{what} {path} is not YAML ({str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__})")
    if data is None:
        raise Refusal(f"{what} {path} is empty")
    if not isinstance(data, dict):
        raise Refusal(f"{what} {path} must hold one mapping at the top")
    return data


def load_rows(path=None) -> dict:
    """rows.json: {"schema": "rows/1", "default_pile", "verdicts": {word: category}, "rows": {id: spec}}. Absent or broken: a refusal naming it."""
    path = Path(path or ROWS_FILE)
    doc = _load_json(path, "the rows file")
    rows = doc.get("rows")
    if doc.get("schema") != "rows/1" or not isinstance(rows, dict) or not rows:
        raise Refusal(f"the rows file {path} must carry schema rows/1 and a non-empty `rows` object")
    for rid, spec in rows.items():
        if not isinstance(spec, dict) or not isinstance(spec.get("name"), str) or not isinstance(spec.get("unit"), str):
            raise Refusal(f"the rows file {path}: row {rid} needs a `name` and a `unit`")
        if not any(k in spec for k in ("path", "ratio", "diff", "sum_of", "max_of", "count_of", "special", "quality")):
            raise Refusal(f"the rows file {path}: row {rid} names no way to get its value")
        if spec.get("better") not in (None, "lower", "higher"):
            raise Refusal(f"the rows file {path}: row {rid}: `better` is lower, higher or null")
    verdicts = doc.get("verdicts", {})
    if not isinstance(verdicts, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in verdicts.items()):
        raise Refusal(f"the rows file {path}: `verdicts` maps a verdict word to a category (both text)")
    return doc


def load_norms(path=None) -> dict:
    path = Path(path or NORMS_FILE)
    doc = _load_json(path, "the norms file")
    if doc.get("schema") != "norms/1" or not isinstance(doc.get("norms"), dict) or not isinstance(doc.get("raises", []), list):
        raise Refusal(f"the norms file {path} must carry schema norms/1, a `norms` object and a `raises` list")
    for nid, norm in doc["norms"].items():
        if not isinstance(norm, dict) or norm.get("kind") not in ("limit", "ratio_to_bar", "not_worse_than_bar") \
                or not isinstance(norm.get("row"), str) or (norm["kind"] != "not_worse_than_bar" and norm.get("op") not in ("<=", ">=")):
            raise Refusal(f"the norms file {path}: norm {nid} needs a `kind` (limit, ratio_to_bar, not_worse_than_bar), a `row` and, for a limit, an `op`")
    return doc


# --------------------------------------------------------------------------------------- counters -> rows

def _num(value):
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None


def _dig(obj, dotted: str):
    for part in dotted.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return MISSING
        obj = obj[part]
    return obj


def _paths_of(spec: dict) -> list:
    found = []
    for key in ("path", "sum_of", "max_of", "count_of"):
        if isinstance(spec.get(key), str):
            found.append(spec[key])
    for key in ("ratio", "diff"):
        for part in (spec.get(key) or {}).values():
            found += [part] if isinstance(part, str) else list(part)
    return found


def _counter_row(spec: dict, counters: dict) -> tuple:
    """(state, value, why) of one row from the counters. A counter that is not measured passes its state and reason on."""
    seen = []
    for dotted in _paths_of(spec):
        head = dotted.split(".")[0]
        row = counters.get(head)
        if not isinstance(row, dict) or "state" not in row:
            return "unknown", None, f"the counters carry no row {head}"
        if row["state"] != "measured":
            seen.append((row["state"], row.get("why", "")))
    if seen:
        state = "unknown" if any(s == "unknown" for s, _w in seen) else seen[0][0]
        return state, None, next((w for s, w in seen if s == state and w), "")
    if "path" in spec:
        value = _dig(counters, spec["path"])
        return ("measured", _num(value), "") if _num(value) is not None else ("unknown", None, f"the counter {spec['path']} is not a number")
    if "ratio" in spec:
        nums = [_num(_dig(counters, p)) for p in spec["ratio"]["num"]]
        dens = [_num(_dig(counters, p)) for p in spec["ratio"]["den"]]
        if None in nums or None in dens:
            return "unknown", None, "a counter of the ratio is not a number"
        if not sum(dens):
            return "unknown", None, "the denominator of the ratio is 0"
        return "measured", round(100.0 * sum(nums) / sum(dens), 1), ""
    if "diff" in spec:
        a, rest = _num(_dig(counters, spec["diff"]["a"])), [_num(_dig(counters, p)) for p in spec["diff"]["b"]]
        if a is None or None in rest:
            return "unknown", None, "a counter of the difference is not a number"
        if sum(rest) > a:
            return "unknown", None, "the seconds taken off exceed the whole: the record is inconsistent"
        return "measured", round(a - sum(rest), 2), ""
    if "sum_of" in spec or "max_of" in spec:
        key = "sum_of" if "sum_of" in spec else "max_of"
        table = _dig(counters, spec[key])
        if not isinstance(table, dict):
            return "unknown", None, f"the counter {spec[key]} is not a table"
        values = [_num(item.get(spec["field"])) if isinstance(item, dict) else None for item in table.values()]
        if None in values:
            return "unknown", None, f"an entry of {spec[key]} has no number under {spec['field']}"
        return "measured", (round(sum(values), 2) if key == "sum_of" else (max(values) if values else 0)), ""
    if "count_of" in spec:
        items = _dig(counters, spec["count_of"])
        return ("measured", len(items), "") if isinstance(items, list) else ("unknown", None, f"the counter {spec['count_of']} is not a list")
    return "unknown", None, "the row names no way to get its value"


def price_row(task_root: Path, run_class: str) -> dict:
    """X1: the task price from `task_price.task_price` (the one price answer): the agreement value, or the range with its note.
    Never a naive sum of cumulative `total_cost_usd` (trap T-cum)."""
    if run_class in SIMULATED:
        return {"state": "n/a", "value": None, "why": "stub roles: a dry or smoke run has no money"}
    try:
        result = TP.task_price(task_root.parent.parent, task_root.name)
    except Exception as exc:  # noqa: BLE001 - one unreadable carrier never takes the scoreboard down
        return {"state": "unknown", "value": None, "why": f"task_price failed ({exc.__class__.__name__})"}
    low, high = _num(result.get("price_low_usd")), _num(result.get("price_high_usd"))
    status, finding = result.get("status"), str(result.get("finding") or "").strip()
    if low is None or high is None:
        return {"state": "unknown", "value": None, "why": f"task_price has no price ({status}): {finding}".rstrip(": ")}
    if status == "incomplete":
        return {"state": "unknown", "value": None, "why": f"task_price is incomplete, the price is at least {round(low, 4)} usd: {finding}".rstrip(": ")}
    if low == high:
        return {"state": "measured", "value": round(low, 4), "why": f"task_price status {status}"}
    return {"state": "measured", "value": {"low": round(low, 4), "high": round(high, 4)},
            "why": f"range, task_price status {status}: {finding}".rstrip(": ")}


# --------------------------------------------------------------------------------------- the judgment (K1)

def _named(problems: list) -> str:
    shown = problems[:MAX_NAMED]
    more = len(problems) - len(shown)
    return "; ".join(shown) + (f"; ... and {more} more" if more else "")


def load_truth_cards(truth_doc: dict, version: str, path) -> list:
    versions = truth_doc.get("versions")
    if not isinstance(versions, list):
        raise Refusal(f"the truth file {path} has no `versions` list")
    for entry in versions:
        if isinstance(entry, dict) and entry.get("id") == version:
            cards = entry.get("cards")
            if not isinstance(cards, list) or not cards:
                raise Refusal(f"the truth file {path}: version {version} has no cards")
            return [str(c.get("id")) for c in cards if isinstance(c, dict)]
    raise Refusal(f"the truth file {path} has no version {version}")


def read_judgment(path, truth_path, arm: str, vocabulary: dict, truth_version=None) -> dict:
    """K1 (shape + joins, never content): every card of the named truth version has exactly one verdict row of this arm; an unknown card
    id, a card listed twice, a nested value where a scalar is expected, a verdict word outside the declared vocabulary, an empty file,
    non-UTF-8 bytes: each refused naming the row. Returns {"truth_version", "cards": {card id: {"verdict", "unsure"}}}."""
    truth = _load_yaml(truth_path, "the truth file")
    judgment = _load_yaml(path, "the judgment file")
    version = truth_version or judgment.get("evaluated_against_version")
    if not isinstance(version, str) or not version:
        raise Refusal(f"the judgment file {path} names no `evaluated_against_version` and no truth version was passed")
    truth_ids = load_truth_cards(truth, version, truth_path)
    rows = judgment.get("card_rows")
    if not isinstance(rows, list) or not rows:
        raise Refusal(f"the judgment file {path} has no `card_rows` list")
    letter = arm
    key = judgment.get("key")
    if isinstance(key, dict):
        letters = [k for k, v in key.items() if isinstance(v, dict) and v.get("arm") == arm]
        if len(letters) != 1:
            raise Refusal(f"the judgment file {path}: its key names {len(letters)} letters for arm {arm}, expected exactly one")
        letter = letters[0]
    problems, got = [], {}
    for index, row in enumerate(rows):
        where = f"row {index}"
        if not isinstance(row, dict):
            problems.append(f"{where} is not a mapping")
            continue
        card, verdict = row.get("card"), row.get("verdict")
        if isinstance(card, bool) or not isinstance(card, (int, str)):
            problems.append(f"{where}: `card` must be a scalar id")
            continue
        where = f"row {index} (card {card})"
        if row.get("arm") != letter:
            continue
        if str(card) not in truth_ids:
            problems.append(f"{where}: card {card} is not in truth version {version}")
        elif str(card) in got:
            problems.append(f"{where}: card {card} is listed twice for arm {arm}")
        if not isinstance(verdict, str) or not verdict.strip():
            problems.append(f"{where}: `verdict` must be a non-empty text")
        elif vocabulary and verdict not in vocabulary:
            problems.append(f"{where}: verdict word {verdict!r} is not in the vocabulary of rows.json")
        if not isinstance(row.get("unsure", False), bool):
            problems.append(f"{where}: `unsure` must be true or false")
        got.setdefault(str(card), {"verdict": verdict, "unsure": row.get("unsure") is True})
    problems += [f"card {card} of truth version {version} has no verdict row for arm {arm}" for card in truth_ids if card not in got]
    if problems:
        raise Refusal(f"the judgment file {path} is refused: {_named(problems)}")
    return {"truth_version": version, "cards": got}


def quality_rows(rows_doc: dict, judged, why_no: str) -> dict:
    """The QA rows. `judged` is read_judgment's answer, or None with `why_no` (no truth table, a stand without one)."""
    out, vocabulary = {}, rows_doc.get("verdicts") or {}
    for rid, spec in rows_doc["rows"].items():
        if "quality" not in spec:
            continue
        q = spec["quality"] or {}
        if judged is None:
            out[rid] = {"state": "unknown", "value": None, "why": why_no}
        elif q.get("from") != "card_rows":
            out[rid] = {"state": "unknown", "value": None, "why": q.get("why") or "the judgment file has no rows for this row (judgment/1)"}
        elif not vocabulary or not q.get("categories"):
            out[rid] = {"state": "unknown", "value": None, "why": "no verdict vocabulary or no categories are declared for this row in rows.json"}
        else:
            counted = [c for c in judged["cards"].values() if vocabulary.get(c["verdict"]) in q["categories"] and not c["unsure"]]
            unsure = sum(1 for c in judged["cards"].values() if c["unsure"])
            out[rid] = {"state": "measured", "value": len(counted), "why": f"{unsure} unsure card(s) are not counted" if unsure else ""}
    return out


# --------------------------------------------------------------------------------------- norms (K2, K5)

def _stricter_or_equal(op: str, a, b) -> bool:
    return a <= b if op == "<=" else a >= b


def check_norms(doc: dict, against=None) -> list:
    """K5: a norm only tightens. Returns the problems (empty = green). The baseline of a norm is its `initial`, or the `to` of its
    last raise; a raise names `from` (the baseline before it), `to`, `raised_by`, `reason` and the owner's `word`. With `against` (the
    norms file as it was) the `initial` may not change, raises may only be appended, a dropped norm and a looser value without a new
    raise are refused."""
    problems, norms, raises = [], doc.get("norms", {}), doc.get("raises", [])
    by_norm = {}
    for index, raised in enumerate(raises):
        if not isinstance(raised, dict) or not all(isinstance(raised.get(k), str) and raised[k].strip() for k in ("norm", "raised_by", "reason", "word")):
            problems.append(f"raise {index} needs `norm`, `raised_by`, `reason` and the owner's `word` (all text, none empty)")
            continue
        if raised["norm"] not in norms:
            problems.append(f"raise {index} names an unknown norm {raised['norm']}")
            continue
        if _num(raised.get("from")) is None or _num(raised.get("to")) is None:
            problems.append(f"raise {index} ({raised['norm']}): `from` and `to` must be numbers")
            continue
        by_norm.setdefault(raised["norm"], []).append(raised)
    for nid, norm in norms.items():
        if not isinstance(norm, dict) or norm.get("kind") not in ("limit", "ratio_to_bar", "not_worse_than_bar"):
            problems.append(f"norm {nid}: `kind` is limit, ratio_to_bar or not_worse_than_bar")
            continue
        if not isinstance(norm.get("row"), str):
            problems.append(f"norm {nid}: `row` names a row of rows.json")
        if norm.get("ratcheted_since") is not None and not isinstance(norm["ratcheted_since"], str):
            problems.append(f"norm {nid}: `ratcheted_since` is a version or null")
        if norm["kind"] == "not_worse_than_bar":
            continue
        op = norm.get("op")
        if op not in ("<=", ">="):
            problems.append(f"norm {nid}: `op` is <= or >=")
            continue
        value, initial = norm.get("value"), norm.get("initial")
        if value is None and initial is None:
            continue                                        # not set yet: the norm is judged unknown until the Lead sets it
        if _num(value) is None or _num(initial) is None:
            problems.append(f"norm {nid}: `value` and `initial` are both numbers or both null")
            continue
        base = initial
        for raised in by_norm.get(nid, []):
            if raised["from"] != base:
                problems.append(f"norm {nid}: a raise starts from {raised['from']} but the baseline is {base}")
            if _stricter_or_equal(op, raised["to"], raised["from"]):
                problems.append(f"norm {nid}: a raise to {raised['to']} is not looser than {raised['from']}")
            base = raised["to"]
        if not _stricter_or_equal(op, value, base):
            problems.append(f"norm {nid}: value {value} is looser than its baseline {base} and no raise row names it "
                            f"(raise rows need `raised_by`, `reason`, the owner's `word`)")
    if against is not None:
        old_norms, old_raises = against.get("norms", {}), against.get("raises", [])
        if raises[:len(old_raises)] != old_raises:
            problems.append("raises may only be appended: an earlier raise row was changed or removed")
        for nid, old in old_norms.items():
            new = norms.get(nid)
            if not isinstance(new, dict) or not isinstance(old, dict):
                problems.append(f"norm {nid} was dropped (a dropped norm is a loosening)" if new is None else f"norm {nid} is not an object")
                continue
            if old.get("initial") is not None and new.get("initial") != old.get("initial"):   # a norm that was not set may be set once
                problems.append(f"norm {nid}: `initial` changed from {old.get('initial')} to {new.get('initial')}")
            old_v, new_v, op = old.get("value"), new.get("value"), old.get("op")
            if _num(old_v) is None:
                continue
            old_raises_n = sum(1 for r in old_raises if isinstance(r, dict) and r.get("norm") == nid)
            if _num(new_v) is None:
                problems.append(f"norm {nid}: value {old_v} was removed (an unset norm is a loosening)")
            elif op in ("<=", ">=") and not _stricter_or_equal(op, new_v, old_v) and len(by_norm.get(nid, [])) <= old_raises_n:
                problems.append(f"norm {nid}: value went from {old_v} to {new_v} with no new raise row")
    return problems


def judge_norms(norms_doc: dict, rows: dict, run_class: str, bar: dict | None, truth_version, rows_doc: dict) -> dict:
    """K2: measured value against the norm: green / red / unknown (never green on an unknown). No norm is judged on a non-live run (K7)."""
    out = {}
    for nid, norm in norms_doc["norms"].items():
        shown = {k: norm[k] for k in ("kind", "row", "op", "value", "unit") if k in norm}
        verdict, why = _judge_one(norm, rows, run_class, bar, truth_version, rows_doc)
        out[nid] = {"norm": shown, "verdict": verdict, **({"why": why} if why else {})}
    return out


def _judge_one(norm: dict, rows: dict, run_class: str, bar, truth_version, rows_doc) -> tuple:
    if run_class != "live":
        return "unknown", f"not judged: run class {run_class} (K7)"
    row = rows.get(norm.get("row"))
    if not isinstance(row, dict) or row.get("state") != "measured" or _num(row.get("value")) is None:
        return "unknown", f"row {norm.get('row')}: " + (row.get("why") or row.get("state", "absent") if isinstance(row, dict) else "absent")
    now = float(row["value"])
    if norm["kind"] == "not_worse_than_bar":
        bar_row = ((bar or {}).get("rows") or {}).get(norm["row"])
        if bar is None:
            return "unknown", "no bar file"
        bar_version = (bar.get("run") or {}).get("truth_version")
        if truth_version is None or bar_version != truth_version:
            return "unknown", f"not comparable: truth {truth_version} vs {bar_version}"
        if not isinstance(bar_row, dict) or bar_row.get("state") != "measured" or _num(bar_row.get("value")) is None:
            return "unknown", f"the bar has no measured {norm['row']}"
        better = (rows_doc["rows"].get(norm["row"]) or {}).get("better")
        if better is None:
            return "unknown", f"row {norm['row']} declares no direction (`better`), so worse is not decided"
        worse = now > bar_row["value"] if better == "lower" else now < bar_row["value"]
        return ("red", f"{now} against the bar {bar_row['value']}") if worse else ("green", "")
    if norm.get("value") is None:
        return "unknown", "the norm value is not set"
    limit, op = float(norm["value"]), norm["op"]
    measured = now
    if norm["kind"] == "ratio_to_bar":
        bar_row = ((bar or {}).get("rows") or {}).get(norm.get("bar_row"))
        if bar is None:
            return "unknown", "no bar file"
        if not isinstance(bar_row, dict) or bar_row.get("state") != "measured" or not _num(bar_row.get("value")):
            return "unknown", f"the bar has no measured non-zero {norm.get('bar_row')}"
        measured = round(now / float(bar_row["value"]), 2)
    ok = measured <= limit if op == "<=" else measured >= limit
    if not ok:
        return "red", f"{measured} against the norm {op} {limit}"
    guard = rows.get(norm.get("unknown_row")) if norm.get("unknown_row") else None
    if isinstance(guard, dict) and (guard.get("state") != "measured" or _num(guard.get("value")) is None or guard["value"] > limit):
        return "unknown", f"the `unknown` check count ({guard.get('value', guard.get('state'))}) is above the norm: it cannot be green (AR-28)"
    return "green", ""


# --------------------------------------------------------------------------------------- compare (K4, K7)

def _range(value):
    if isinstance(value, dict):
        low, high = _num(value.get("low")), _num(value.get("high"))
        return (low, high) if low is not None and high is not None else None
    number = _num(value)
    return (number, number) if number is not None else None


def build_compare(doc: dict, previous: dict | None, previous_name, bar_name, rows_doc: dict) -> dict:
    """Per row {was, now, worse} against the previous scoreboard. `worse` is true/false only between two measured values of the SAME row;
    anything else is null with the reason; a first run has no `rows` at all; a dry/smoke/unknown/mixed run is `not_comparable` (K7)."""
    out = {"previous": previous_name or "none", "bar": bar_name or "none"}
    if previous is None:
        return out
    run, was_run = doc.get("run") or {}, previous.get("run") or {}
    for field in ("run_class", "arm"):
        if run.get(field) != was_run.get(field) or (field == "run_class" and run.get(field) != "live"):
            out["not_comparable"] = f"{field} {was_run.get(field)} vs {run.get(field)}"
            return out
    result = {}
    for rid, spec in rows_doc["rows"].items():
        now, was = (doc.get("rows") or {}).get(rid), (previous.get("rows") or {}).get(rid)
        if not isinstance(now, dict) or not isinstance(was, dict):
            result[rid] = {"was": None, "now": None, "worse": None, "why": "the row is absent in one of the two files"}
            continue
        if spec.get("truth_bound") and run.get("truth_version") != was_run.get("truth_version"):
            result[rid] = {"not_comparable": f"truth {was_run.get('truth_version')} vs {run.get('truth_version')}"}
            continue
        entry = {"was": was.get("value") if was.get("state") == "measured" else was.get("state"),
                 "now": now.get("value") if now.get("state") == "measured" else now.get("state"), "worse": None}
        a, b = (_range(was.get("value")) if was.get("state") == "measured" else None), (_range(now.get("value")) if now.get("state") == "measured" else None)
        if a is None or b is None:
            entry["why"] = "one of the two values is not measured: nothing to compare"
        elif spec.get("better") is None:
            entry["why"] = "the row declares no direction (`better`)"
        else:
            lower = spec["better"] == "lower"
            worse = b[0] > a[1] if lower else b[1] < a[0]
            better = b[1] < a[0] if lower else b[0] > a[1]
            entry["worse"] = worse
            if not worse and not better and (a[0] != a[1] or b[0] != b[1]) and b[0] != a[0]:
                entry["worse"], entry["why"] = None, "the two ranges overlap: worse is not decided"
            elif not worse and not better and a[0] == a[1] and b[0] == b[1]:
                entry["worse"] = False
        result[rid] = entry
    out["rows"] = result
    return out


def previous_of(path: Path):
    """(file, doc, notes): the newest EARLIER file of the same folder with run_class live and the same arm (K7); None when there is none.
    A candidate that cannot be read is named in `notes` (never silently skipped as `none`)."""
    match = FILE_NAME.fullmatch(path.name)
    notes = []
    if not match:
        return None, None, notes
    stamp, tail = match.group(1), match.group(2)
    arm = tail.rsplit("-", 1)[-1]
    best = None
    for other in sorted(path.parent.glob("*.yaml")):
        got = FILE_NAME.fullmatch(other.name)
        if not got or got.group(1) >= stamp or got.group(2).rsplit("-", 1)[-1] != arm or other.name.startswith("bar-"):
            continue
        try:
            data = _load_yaml(other, "an earlier scoreboard")
        except Refusal as exc:
            notes.append(f"RED: {exc}")
            continue
        run = data.get("run") if isinstance(data.get("run"), dict) else {}
        if data.get("schema") == SCHEMA and run.get("run_class") == "live" and run.get("arm") == arm:
            if best is None or (got.group(1), other.name) > (best[0], best[1].name):
                best = (got.group(1), other, data)
    return (best[1], best[2], notes) if best else (None, None, notes)


# --------------------------------------------------------------------------------------- assemble

def _sources(task_root: Path, counters: dict) -> list:
    bad = ((counters.get("U1") or {}).get("bad_lines")) or {}
    out = []
    for name, key in SOURCES:
        path = task_root / "state" / name
        if path.is_file():
            data = path.read_bytes()
            out.append({"file": f"state/{name}", "sha256": hashlib.sha256(data).hexdigest(), "lines": len(data.splitlines()),
                        "bad_lines": bad.get(key, 0) if isinstance(bad.get(key, 0), int) else 0})
    return out


ABS_PATH = re.compile(r"[A-Za-z]:[\\/][^\s'\",;)]*|(?<![\w.:-])/(?:[\w.~-]+/)+[\w.~-]*")


def _scrub(text: str) -> str:
    """A reason copied from the counters may name an absolute path of this machine; a scoreboard stores none (AR-4)."""
    return ABS_PATH.sub("<path>", text)


def _safe(token, what: str) -> str:
    if not isinstance(token, str) or not TOKEN.fullmatch(token) or ".." in token:
        raise Refusal(f"{what} {token!r} is not a plain name (letters, digits, dot, dash, underscore)")
    return token


def assemble(task_root, stand, story, arm, version, rows_path=None, norms_path=None, truth=None, judgment=None, truth_version=None,
             bar=None, models=(), passes=(), started=None, out_root=None) -> tuple:
    """(path, text, notes). Raises Refusal before anything is written; the caller writes `text` to `path` (the one write site)."""
    rows_doc, norms_doc = load_rows(rows_path), load_norms(norms_path)
    for what, token in (("the stand", stand), ("the story", story), ("the arm", arm), ("the version", version)):
        _safe(token, what)
    task_root = Path(task_root)
    if not task_root.is_dir():
        raise Refusal(f"the run folder {task_root} does not exist")
    if not any(p.is_file() for p in task_root.rglob("*")):
        raise Refusal(f"the run folder {task_root} is empty: there is nothing to measure")
    counters = RC.counters(task_root)
    run_class = (counters.get("run") or {}).get("run_class", "unknown")
    judged, why_no = None, f"no truth table for {stand}/{story}"
    if truth is not None or judgment is not None:
        if truth is None or judgment is None:
            raise Refusal("--truth and --judgment go together: a judgment is read against a truth file")
        judged = read_judgment(judgment, truth, arm, rows_doc.get("verdicts") or {}, truth_version)
    quality = quality_rows(rows_doc, judged, why_no)
    rows = {}
    for rid, spec in rows_doc["rows"].items():
        if "quality" in spec:
            item, source = quality[rid], "judgment x truth"
        elif spec.get("special") == "price":
            item, source = price_row(task_root, run_class), "task_price.task_price"
        else:
            state, value, why = _counter_row(spec, counters)
            item, source = {"state": state, "value": value, "why": why}, "run_counters." + "+".join(sorted({p.split(".")[0] for p in _paths_of(spec)}))
        rows[rid] = {"name": spec["name"], "value": item["value"], "unit": spec["unit"], "source": source, "state": item["state"],
                     **({"why": _scrub(item["why"])} if item.get("why") else {})}
    first = RC.DJ.parse_ts(((counters.get("T1") or {}).get("first"))) if started is None else RC.DJ.parse_ts(started)
    if first is None:
        raise Refusal("the start time of the run is unknown (no readable time in the carriers): pass --started <ISO time with offset>")
    from datetime import timezone
    first = first.astimezone(timezone.utc)
    name = f"{first:%Y%m%d-%H%M}-{version}-{arm}.yaml"
    folder = Path(out_root or SCOREBOARDS) / stand / story
    path = folder / name
    bar_doc = _load_yaml(bar, "the bar file") if bar else None
    run = {"stand": stand, "story": story, "arm": arm, "task": task_root.name, "run_class": run_class,
           "package": {"version": version, "fingerprint": "unknown: run_counters does not expose it"},
           "models": sorted(models) or ["unknown: no --model given"], "started": first.isoformat(),
           "truth_version": judged["truth_version"] if judged else None, "sources": _sources(task_root, counters)}
    doc = {"schema": SCHEMA, "run": run, "rows": rows}
    doc["norms"] = judge_norms(norms_doc, rows, run_class, bar_doc, run["truth_version"], rows_doc)
    for entry in passes:
        if entry[0] not in norms_doc["norms"] or not entry[1].strip():
            raise Refusal(f"--pass {entry[0]!r}: a known norm and the owner's word are needed")
    doc["passes"] = [{"norm": n, "word": w, "date": d} for n, w, d in passes]
    notes = []
    previous_file, previous_doc, skipped = previous_of(path)
    notes += skipped
    doc["compare"] = build_compare(doc, previous_doc, previous_file.name if previous_file else None, Path(bar).name if bar else None, rows_doc)
    return path, yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=120), notes


# --------------------------------------------------------------------------------------- compare: printing, findings

def _shown(value) -> str:
    return f"{value['low']}..{value['high']}" if isinstance(value, dict) else str(value)


def render_compare(doc: dict, comp: dict, norms: dict, norms_doc: dict, rows_doc: dict, name: str) -> list:
    lines = [f"compare: {name}", f"previous: {comp['previous']}", f"bar: {comp['bar']}"]
    if "not_comparable" in comp:
        lines.append(f"not comparable: {comp['not_comparable']}")
    for rid, entry in (comp.get("rows") or {}).items():
        unit = rows_doc["rows"][rid]["unit"]
        if "not_comparable" in entry:
            lines.append(f"{rid}: not comparable: {entry['not_comparable']}")
        else:
            verdict = {True: "worse", False: "not worse", None: "undecided"}[entry["worse"]]
            lines.append(f"{rid}: was {_shown(entry['was'])}, now {_shown(entry['now'])} {unit} -- {verdict}" + (f" ({entry['why']})" if entry.get("why") else ""))
    passed = {p["norm"]: p for p in doc.get("passes") or []}
    for nid, item in norms.items():
        line = f"norm {nid} [{item['norm'].get('row')}]: {item['verdict']}" + (f" -- {item['why']}" if item.get("why") else "")
        lines.append(line + (f" (passed by the owner's word: {passed[nid]['word']}, {passed[nid]['date']})" if nid in passed else ""))
        spec, row = norms_doc["norms"][nid], (doc.get("rows") or {}).get(item["norm"].get("row")) or {}
        if item["verdict"] == "green" and spec.get("kind") == "limit" and spec.get("value") is not None and _num(row.get("value")) is not None \
                and not _stricter_or_equal(spec["op"], spec["value"], row["value"]):
            lines.append(f"can tighten: {nid} {spec['value']} -> {row['value']}")
    worsened = {rid for rid, e in (comp.get("rows") or {}).items() if e.get("worse") is True}
    owner = [n for n, s in norms_doc["norms"].items() if s.get("ratcheted_since") and s.get("row") in worsened and n not in passed]
    red = [n for n, i in norms.items() if i["verdict"] == "red" and n not in passed and n not in owner]
    if owner:
        lines.append(f"release: owner's word needed -- {', '.join(owner)}")
    if red:
        lines.append(f"release: warning -- red norm(s): {', '.join(red)}")
    unknown = [n for n, i in norms.items() if i["verdict"] == "unknown" and n not in passed]
    if unknown and doc["run"].get("run_class") == "live":
        lines.append(f"release: warning -- unknown norm(s), not green: {', '.join(unknown)}")
    return lines


def write_findings(doc: dict, comp: dict, rows_doc: dict, name: str, root=None) -> tuple:
    """K4: one finding file per worsened row, in the pile rows.json names (default live-runs). Returns (paths, card lines for the Lead).
    The date in a file name is the run's own start date (no clock is read)."""
    written, cards = [], []
    date = str(doc["run"]["started"])[:10].replace("-", "")
    for rid, entry in (comp.get("rows") or {}).items():
        if entry.get("worse") is not True:
            continue
        spec = rows_doc["rows"][rid]
        pile = _safe(spec.get("pile") or rows_doc.get("default_pile") or "live-runs", "the pile")
        file = Path(root or PILES) / pile / "findings" / f"{date}-scoreboard-{rid.lower()}-{doc['run']['arm']}.md"
        row = doc["rows"][rid]
        text = "\n".join([
            f"# Табло: строка {rid} ({spec['name']}) стала хуже",
            "",
            f"id: — | кучка: `{pile}` | от: `scoreboard.py compare --findings` | приоритет: П2 | кандидат наверх: нет",
            "",
            "## Что не так",
            "",
            f"Строка {rid} ({spec['name']}): было {_shown(entry['was'])} {spec['unit']}, стало {_shown(entry['now'])} {spec['unit']}; "
            f"лучше — когда {'меньше' if spec.get('better') == 'lower' else 'больше'}. Источник строки: {row.get('source')}.",
            f"Сравнивались `{name}` и `{comp['previous']}` (один прогон на одну строку; единицы совпадают).",
            "Сырые записи в репозиторий не копируются; их хэши и число строк — в разделе `run.sources` файла табло:",
            *[f"- `{s['file']}`: sha256 `{s['sha256']}`, строк {s['lines']}, нечитаемых {s['bad_lines']}" for s in doc["run"].get("sources") or []],
            "",
            "## Свидетель",
            "",
            f"`python -B experiments/measurers/scoreboard.py compare experiments/scoreboards/{doc['run']['stand']}/{doc['run']['story']}/{name}`",
            "",
            "Решение владельца нужно: нет.",
            "",
            "## Куда",
            "",
            f"Строка в таблице «Содержание» карточки кучки `{pile}` и узел в невзятой пачке этой кучки (PROJECT.md «Командная работа» п. 2).",
            ""])
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8", newline="\n")
        written.append(file)
        cards.append(f"card row, pile {pile}: path {file.name} | type: scoreboard worsened row | essence: {rid} {_shown(entry['was'])} -> {_shown(entry['now'])} "
                     f"{spec['unit']} | node: - | owner decision: no")
    return written, cards


# --------------------------------------------------------------------------------------- the command line

def _red(message: str) -> int:
    print(f"RED: {message}", file=sys.stderr)
    return 2


def cmd_assemble(args) -> int:
    try:
        path, text, notes = assemble(args.task_root, args.stand, args.story, args.arm, args.version, args.rows, args.norms, args.truth,
                                     args.judgment, args.truth_version, args.bar, args.model or (), [tuple(p) for p in args.passed or []],
                                     args.started, args.out_root)
    except Refusal as exc:
        return _red(str(exc))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")           # the one write site of a scoreboard file
    for note in notes:
        print(note)
    print(f"wrote {path}")
    return 0


def cmd_compare(args) -> int:
    try:
        rows_doc, norms_doc = load_rows(args.rows), load_norms(args.norms)
        path = Path(args.scoreboard)
        doc = _load_yaml(path, "the scoreboard")
        if doc.get("schema") != SCHEMA or not isinstance(doc.get("run"), dict) or not isinstance(doc.get("rows"), dict):
            raise Refusal(f"the scoreboard {path} is not a {SCHEMA} file")
        if args.previous:
            previous_file, previous_doc, notes = Path(args.previous), _load_yaml(args.previous, "the previous scoreboard"), []
        else:
            previous_file, previous_doc, notes = previous_of(path)
        bar_path = Path(args.bar) if args.bar else (path.parent / doc["compare"]["bar"] if isinstance(doc.get("compare"), dict)
                                                    and doc["compare"].get("bar") not in (None, "none") else None)
        bar_doc = _load_yaml(bar_path, "the bar file") if bar_path else None
    except Refusal as exc:
        return _red(str(exc))
    comp = build_compare(doc, previous_doc, previous_file.name if previous_file else None, bar_path.name if bar_path else None, rows_doc)
    norms = judge_norms(norms_doc, doc["rows"], doc["run"].get("run_class"), bar_doc, doc["run"].get("truth_version"), rows_doc)
    for note in notes:
        print(note)
    for line in render_compare(doc, comp, norms, norms_doc, rows_doc, path.name):
        print(line)
    if args.findings:
        written, cards = write_findings(doc, comp, rows_doc, path.name, args.findings_root)
        for item in written:
            print(f"finding: {item}")
        for card in cards:
            print(card)
    return 0


def cmd_norms(args) -> int:
    try:
        doc = load_norms(args.norms)
        old = load_norms(args.against) if args.against else None
    except Refusal as exc:
        return _red(str(exc))
    if not args.check:
        for nid, norm in doc["norms"].items():
            print(f"{nid}: row {norm.get('row')} {norm.get('op', '')} {norm.get('value')} {norm.get('unit', '')} "
                  f"(initial {norm.get('initial')}, ratcheted since {norm.get('ratcheted_since')})")
        return 0
    problems = check_norms(doc, old)
    for problem in problems:
        print(f"RED: {problem}")
    print("norms: " + ("red" if problems else "green"))
    return 1 if problems else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, prog="scoreboard.py")
    sub = parser.add_subparsers(dest="command", required=True, metavar="{assemble,compare,norms,release-check}")
    a = sub.add_parser("assemble", help="read one run's counters and write its scoreboard file (nothing is written on a refusal)")
    a.add_argument("--task-root", required=True, help="the story's folder, qa-factory/artifacts/<KEY> (outside the repo)")
    a.add_argument("--stand", required=True)
    a.add_argument("--story", required=True)
    a.add_argument("--arm", required=True, help="factory or free")
    a.add_argument("--version", required=True, help="the package version of the run")
    a.add_argument("--truth", help="truth/<story>.yaml; with --judgment the QA rows are read, without them QA rows are unknown")
    a.add_argument("--judgment", help="judgment.yaml (the blind evaluation); shape is checked by K1")
    a.add_argument("--truth-version", help="default: the judgment's evaluated_against_version")
    a.add_argument("--bar", help="the free-agent bar file the norms that name a bar are judged against")
    a.add_argument("--model", action="append", help="a model id of the run (repeatable)")
    a.add_argument("--pass", dest="passed", nargs=3, action="append", metavar=("NORM", "WORD", "DATE"), help="record the owner's word that passes a red norm (P13)")
    a.add_argument("--started", help="the run's start (ISO, with offset) when the carriers hold none")
    a.add_argument("--rows", help="rows.json (default experiments/scoreboards/rows.json)")
    a.add_argument("--norms", help="norms.json (default experiments/scoreboards/norms.json)")
    a.add_argument("--out-root", help="default experiments/scoreboards")
    a.set_defaults(run=cmd_assemble)
    c = sub.add_parser("compare", help="print a scoreboard against the previous one and the norms; --findings writes a finding per worsened row")
    c.add_argument("scoreboard")
    c.add_argument("--previous", help="default: the newest earlier live file of the same arm in the same folder")
    c.add_argument("--bar")
    c.add_argument("--findings", action="store_true", help="write one finding file per worsened row (the pile named by rows.json)")
    c.add_argument("--findings-root", help="default plans/piles")
    c.add_argument("--rows")
    c.add_argument("--norms")
    c.set_defaults(run=cmd_compare)
    n = sub.add_parser("norms", help="print the norms; --check refuses a norms file that loosened without a raise row (K5)")
    n.add_argument("--check", action="store_true")
    n.add_argument("--against", help="the norms file as it was before the edit (git show ...:norms.json)")
    n.add_argument("--norms")
    n.set_defaults(run=cmd_norms)
    r = sub.add_parser("release-check", help="K3: exit 0 only when no `compare --release` line needs the owner's word, or each has it recorded")
    import scoreboard_bar                       # here, not at the top: scoreboard_bar imports this module (release-check lives there, N7)
    scoreboard_bar.add_release_check_arguments(r)
    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
