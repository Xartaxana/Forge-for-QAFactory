#!/usr/bin/env python3
"""The free-agent bar's price and the release check of the run scoreboard (P1-v N7).

    python -B experiments/measurers/scoreboard_bar.py price --transcript T [--transcript T2 ...] [--result free-N.log ...] [--cfg cost.json]
    python -B experiments/measurers/scoreboard_bar.py release-check (--release V | --version V --lines FILE|-) [--norms norms.json] [--root DIR]
    python -B experiments/measurers/scoreboard.py release-check ...      (the same command, through scoreboard.py)
    python -B experiments/measurers/scoreboard.py compare --release V    (N6b: the producer of the lines; `release_lines` below)

`release-check --release V` runs `release_lines` and judges its lines; `--lines` judges a saved copy: ONE judge, two inputs.

PRICE (spec 3 item 2, B1-E5/E6): the free arm's price is its transcripts RE-PRICED by the catalogue, request by request, through the
helpers `compare.py` already uses for the same job (`price_seen`, `is_empty_marker`) and the rate rule of the package
(`cost_capture.resolve_rate`: the project's `rate_overrides` first, then the bundled catalogue). The host's `total_cost_usd` (the
`free-N.log` result) is only PRINTED beside the value, never part of it. A transcript that cannot be read, a missing one, an empty list,
a request the catalogue cannot price: the value is `unknown` with the reason, never 0 and never the host figure (FR-41, AR-28).

RELEASE CHECK (K3, F7 as the owner answered it, OQ2): the input is the `release:` lines `compare --release` prints. A line
`release: owner's word needed -- <row> <pair> ...` is cleared by a `worsened_passes` entry of the SAME row, version and pair with a word;
the line `release: owner's word needed -- <row> ratcheted, new bar <bar file> is better than the factory` (OQ2) is cleared by a
`bar_changes` entry `{bar, word, decision: keep|lift}` naming that bar file. Exit 0 when nothing is left, 1 with the list, 2 for an input
or a norms file that cannot be read (a named error, never a pass). Warnings never change the exit.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import compare as CMP
import paths
import scoreboard as SB



def _cost_capture():
    """The package's rate rule, imported when a price is asked for: importing `cost_capture` prints a WARN line about the developer config
    to stdout, which no other command of `scoreboard.py` (release-check, compare, norms) should carry."""
    if str(paths.SCRIPTS) not in sys.path:
        sys.path.append(str(paths.SCRIPTS))
    import cost_capture
    return cost_capture

NEEDED = "release: owner's word needed -- "
OQ2 = re.compile(r"(?P<row>\S+) ratcheted, new bar (?P<bar>\S+) is better than the factory")
PAIRED = re.compile(r"(?P<row>\S+) (?P<pair>[^\s/]+/\S+)(?: .*)?")
DECISIONS = ("keep", "lift")


# --------------------------------------------------------------------------------------- the bar's price

def _requests(path: Path) -> dict:
    """{message id: (model, usage)} of one transcript: the unique requests that carry a `usage` block, the same collection `compare.scan`
    makes (it does not expose it). Lines that are not JSON are skipped as there. Raises OSError / UnicodeDecodeError."""
    seen = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            message = item.get("message") if isinstance(item, dict) else None
            message = message if isinstance(message, dict) else {}
            if item.get("type") == "assistant" and isinstance(message.get("usage"), dict) and not CMP.is_empty_marker(message.get("model"), message["usage"]):
                seen[message.get("id") or item.get("uuid")] = (message.get("model"), message["usage"])
    return seen


def host_total(results) -> float | None:
    """The host's own `total_cost_usd` of the free arm's result file(s), summed; None when there is none or one cannot be read. A result
    file is one JSON object, or a log whose last JSON line is that object. PRINTED only."""
    total = 0.0
    for result in results or ():
        try:
            text = Path(result).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None
        found = None
        for candidate in [text] + text.strip().splitlines()[::-1]:
            try:
                data = json.loads(candidate)
            except ValueError:
                continue
            if isinstance(data, dict) and SB._num(data.get("total_cost_usd")) is not None:
                found = SB._num(data["total_cost_usd"])
                break
        if found is None:
            return None
        total += found
    return round(total, 4) if results else None


def bar_price(transcripts, cfg=None, results=()) -> dict:
    """{state, value, why, unpriced, host_total_usd}: the free arm's transcripts re-priced by the catalogue (sessions summed). `cfg` is the
    project's `cost` block (its `rate_overrides` are asked first, B1-E6) or None. `unknown` (value None) when the list is empty, a
    transcript is missing or unreadable, no request is found, or the catalogue cannot price a request: never 0, never the host's figure."""
    out = {"state": "unknown", "value": None, "why": "", "unpriced": 0, "host_total_usd": host_total(results)}
    paths_ = [Path(p) for p in (transcripts or ())]
    if not paths_:
        out["why"] = "no transcript of the free arm was given: nothing to re-price"
        return out
    CC = _cost_capture()
    total, requests, catalogue = 0.0, 0, CC.load_catalogue()
    for path in paths_:
        try:
            seen = _requests(path)
        except FileNotFoundError:
            out["why"] = f"the transcript {path.name} is absent (not recomputed)"
            return out
        except (OSError, UnicodeDecodeError) as exc:
            out["why"] = f"the transcript {path.name} cannot be read ({exc.__class__.__name__}) (not recomputed)"
            return out
        rate = {model: CC.resolve_rate(model, cfg, catalogue)[0] for model, _u in seen.values()}
        cost, unpriced = CMP.price_seen(rate, seen)
        out["unpriced"] += unpriced
        total, requests = total + cost, requests + len(seen)
    if out["unpriced"]:
        out["why"] = f"{out['unpriced']} request(s) the catalogue cannot price: the sum would be a lower bound, not a price"
    elif not requests:
        out["why"] = "the transcripts hold no request with a usage block (not recomputed)"
    else:
        out.update(state="measured", value=round(total, 4), why=f"{requests} request(s) of {len(paths_)} transcript(s) re-priced by the catalogue")
    return out


def price_line(priced: dict) -> str:
    """One printed line: the value (or `unknown: <why>`) and, beside it and apart from it, the host's figure."""
    host = priced.get("host_total_usd")
    shown = f"{priced['value']} usd (re-priced by the catalogue)" if priced["state"] == "measured" else f"unknown: {priced['why']}"
    return f"bar price: {shown}; host total_cost_usd: {'not given' if host is None else host} (the host's figure, printed only, not part of the value)"


# --------------------------------------------------------------------------------------- the OQ2 line

def beats(row: str, better, a_value, b_value) -> bool:
    """`a` is STRICTLY better than `b` (ranges: the whole range of `a` beyond the whole range of `b`). A value that is not a number or a range,
    or a row with no direction, is a refusal naming the row: not-better is never assumed."""
    a, b = SB._range(a_value), SB._range(b_value)
    if a is None or b is None or better not in ("lower", "higher"):
        raise SB.Refusal(f"row {row}: the values {a_value!r} and {b_value!r} or the direction {better!r} cannot be compared")
    return a[1] < b[0] if better == "lower" else a[0] > b[1]


def bar_better_line(row: str, bar_file: str, better, factory, bar) -> str | None:
    """OQ2: the line `release: owner's word needed -- <row> ratcheted, new bar <bar file> is better than the factory` when the new bar is
    STRICTLY better than the factory's value on a ratcheted row, else None (the comparison is `beats`)."""
    return f"{NEEDED}{row} ratcheted, new bar {bar_file} is better than the factory" if beats(row, better, bar, factory) else None


# --------------------------------------------------------------------------------------- compare --release (B2)

def _flat(text) -> str:
    return " ".join(SB._scrub(str(text)).split())


def _boards(root: Path, version: str) -> tuple:
    """({(stand, story): (stamp, path, doc)}: the newest factory scoreboard of `version` per folder, any run class; whether a LIVE factory
    scoreboard of ANOTHER version exists (a previous release); notes for the files that could not be read)."""
    mine, other, notes = {}, False, []
    for path in sorted(root.glob("*/*/*.yaml")) if root.is_dir() else []:
        match = SB.FILE_NAME.fullmatch(path.name)
        if not match or not match.group(2).endswith("-factory"):
            continue
        try:
            doc = SB._load_yaml(path, "a scoreboard")
        except SB.Refusal as exc:
            notes.append(f"release: note -- {_flat(exc)}")
            continue
        if doc.get("schema") != SB.SCHEMA or not isinstance(doc.get("rows"), dict):
            continue
        key = (path.parent.parent.name, path.parent.name)
        if match.group(2) == f"{version}-factory":
            if key not in mine or (match.group(1), path.name) > (mine[key][0], mine[key][1].name):
                mine[key] = (match.group(1), path, doc)
        elif isinstance(doc.get("run"), dict) and doc["run"].get("run_class") == "live":
            other = True
    return mine, other, notes


def _bars(root: Path, stand: str, story: str, notes: list) -> list:
    """[(label `<stand>/<story>/bar-<model>.yaml`, model id, doc)] of the bar files of one folder."""
    found, folder = [], root / stand / story
    for path in sorted(folder.glob("bar-*.yaml")) if folder.is_dir() else []:
        try:
            found.append((f"{stand}/{story}/{path.name}", path.name[len("bar-"):-len(".yaml")], SB._load_yaml(path, "a bar file")))
        except SB.Refusal as exc:
            notes.append(f"release: note -- {_flat(exc)}")
    return found


def _element_line(rid: str, better, el: dict, board, version: str) -> str:
    """The ONE line of one ratcheted element (amendment B2, table B1 of the base spec): worse / not decided / unknown / no value / no
    comparable measurement / ok. Every doubt is `owner's word needed`; nothing unknown reads as `not worse` (FR-41, AR-28)."""
    pre = f"{NEEDED}{rid} {el['pair']} "
    if board is None:
        return pre + "no value in this release (no scoreboard for the pair)"
    run = board.get("run") if isinstance(board.get("run"), dict) else {}
    if run.get("run_class") != "live":
        return pre + f"no comparable measurement (run class {run.get('run_class')} vs live)"
    models = [str(m) for m in run.get("models") or []] if isinstance(run.get("models"), list) else []
    if el["factory_model"] not in models:
        return pre + f"no comparable measurement (factory model {el['factory_model']} vs {', '.join(models) or 'unknown'})"
    item = board["rows"].get(rid)
    if not isinstance(item, dict):
        return pre + f"unknown: the scoreboard has no row {rid}"
    state, value = item.get("state"), item.get("value")
    prev = SB._range(el["value"])
    if state == "at_least":
        bound = SB._num(value)
        if bound is None:
            return pre + f"unknown: the lower bound of {rid} is not a number"
        if better == "lower" and bound > prev[1]:
            return pre + f"was {SB._shown(el['value'])} ({el['since']}) now at least {SB._shown(value)} ({version})"
        return pre + f"not decided: lower bound ({SB._shown(value)})"
    if state not in ("measured", "one_source", "range"):
        return pre + f"unknown: {_flat(item.get('why') or state)}"
    now = SB._range(value)
    if now is None:
        return pre + f"unknown: the value of {rid} is not a number"
    worse, fine = (now[0] > prev[1], now[1] <= prev[0]) if better == "lower" else (now[1] < prev[0], now[0] >= prev[1])
    if worse:
        return pre + f"was {SB._shown(el['value'])} ({el['since']}) now {SB._shown(value)} ({version})"
    if fine:
        return f"release: ok -- {rid} {el['pair']} not worse"
    return pre + f"not decided: range ({SB._shown(value)})"


def release_lines(version: str, norms_doc: dict, root=None) -> list:
    """`compare --release <version>`: the lines to print. One line per ELEMENT of `ratchets` in norms.json (not per row of a scoreboard), in the
    texts of amendment B2; then, for the other rows: `release: warning` for a red one, `can ratchet:` for a measured one better than a bar;
    the OQ2 line for a new bar better than the factory on a ratcheted row; `release: no previous release` when nothing was ratcheted and no
    live scoreboard of another version exists. A version that is not a plain name is a refusal."""
    SB._safe(version, "the release version")
    root = Path(root or SB.SCOREBOARDS)
    mine, other_live, notes = _boards(root, version)
    rows = norms_doc.get("rows") or {}
    ratcheted = {(rid, el["pair"]) for rid, row in rows.items() for el in row.get("ratchets", [])}
    lines, oq2 = [], set()
    if not ratcheted and not other_live:
        lines.append("release: no previous release -- ratchet not judged")
    for rid, row in rows.items():
        for el in row.get("ratchets", []):
            stand, story = el["bar"].split("/")[:2]
            board = (mine.get((stand, story)) or (None, None, None))[2]
            lines.append(_element_line(rid, row.get("better"), el, board, version))
            if board is None or board.get("run", {}).get("run_class") != "live":
                continue
            item = board["rows"].get(rid)
            for label, _model, bar_doc in _bars(root, stand, story, notes):
                bar_row = (bar_doc.get("rows") or {}).get(rid)
                if label == el["bar"] or label in oq2 or not isinstance(item, dict) or not isinstance(bar_row, dict) \
                        or item.get("state") != "measured" or bar_row.get("state") != "measured":
                    continue
                try:
                    line = bar_better_line(rid, label, row.get("better"), item.get("value"), bar_row.get("value"))
                except SB.Refusal:
                    continue                    # an unreadable value is not "better"; the element line above already speaks for the row
                if line:
                    oq2.add(label)
                    lines.append(line)
    seen = set()
    for (stand, story), (_stamp, path, board) in sorted(mine.items()):
        run = board.get("run") if isinstance(board.get("run"), dict) else {}
        if run.get("run_class") != "live":
            continue
        passed = {p.get("norm") for p in board.get("passes") or [] if isinstance(p, dict)}
        for nid, item in (board.get("norms") or {}).items():
            norm = item.get("norm") if isinstance(item, dict) and isinstance(item.get("norm"), dict) else {}
            rid = norm.get("row")
            if not isinstance(item, dict) or item.get("verdict") != "red" or nid in passed or rid is None \
                    or any(r == rid and p.endswith("/" + story) for r, p in ratcheted):
                continue
            shown = SB._shown((board["rows"].get(rid) or {}).get("value"))
            against = norm.get("value") if norm.get("value") is not None else _flat(item.get("why") or "unknown")
            line = f"release: warning -- {rid} red: {shown} against norm {against}"
            if line not in seen:
                seen.add(line)
                lines.append(line)
        for label, model, bar_doc in _bars(root, stand, story, notes):
            for rid, row in rows.items():
                item, bar_row = board["rows"].get(rid), (bar_doc.get("rows") or {}).get(rid)
                pair = f"{model}/{story}"
                if row.get("better") not in ("lower", "higher") or (rid, pair) in ratcheted or not isinstance(item, dict) \
                        or not isinstance(bar_row, dict) or item.get("state") != "measured" or bar_row.get("state") != "measured" \
                        or SB._num(item.get("value")) is None or SB._num(bar_row.get("value")) is None:
                    continue
                if beats(rid, row["better"], item["value"], bar_row["value"]):
                    lines.append(f"can ratchet: {rid} {pair} {SB._shown(item['value'])} better than bar {label} ({SB._shown(bar_row['value'])})")
    return lines + notes


# --------------------------------------------------------------------------------------- release-check

def _answers(norms_path) -> tuple:
    """(worsened_passes by row, bar_changes, notes) read from norms.json through scoreboard.load_norms (the one reader). Absent file, or a
    file of an older shape without the keys: read as empty. A file that cannot be read, or a key of the wrong shape: a Refusal."""
    path = Path(norms_path or SB.NORMS_FILE)
    if not path.exists():
        return {}, [], []
    doc = SB.load_norms(path)
    rows, changes, notes = doc.get("rows", {}), doc.get("bar_changes", []), []
    if not isinstance(rows, dict) or not isinstance(changes, list):
        raise SB.Refusal(f"the norms file {path}: `rows` must be an object and `bar_changes` a list")
    passes = {}
    for rid, spec in rows.items():
        listed = spec.get("worsened_passes", []) if isinstance(spec, dict) else None
        if not isinstance(listed, list):
            raise SB.Refusal(f"the norms file {path}: row {rid}: `worsened_passes` must be a list")
        passes[rid] = [p for p in listed if isinstance(p, dict)]
    good = []
    for index, item in enumerate(changes):
        if not isinstance(item, dict) or not isinstance(item.get("bar"), str) or not isinstance(item.get("word"), str) or not item["word"].strip() \
                or item.get("decision") not in DECISIONS:
            notes.append(f"release: note -- bar_changes entry {index} ignored: it needs a `bar`, the owner's `word` and a decision (keep or lift)")
            continue
        good.append(item)
    return passes, good, notes


def release_check(lines, version: str, norms_path=None, produced=False) -> tuple:
    """(exit code, printed lines). 0: no line needs the owner's word, or each has it recorded; 1: the list; a Refusal for unreadable input.
    `produced`: the lines come straight from `release_lines` (the direct road), so an empty list is a real "nothing to judge", not a missing
    input; from `--lines` an empty input stays a refusal."""
    lines = [str(line).strip() for line in lines if str(line).strip()]
    if not lines and not produced:
        raise SB.Refusal("no `release:` line was given: `compare --release` was not run or printed nothing, and nothing is not a pass")
    passes, changes, notes = _answers(norms_path)
    open_, printed = [], list(notes)
    for line in lines:
        if not line.startswith(NEEDED):
            printed.append(line)
            continue
        rest = line[len(NEEDED):]
        oq2, paired = OQ2.fullmatch(rest), PAIRED.fullmatch(rest)
        if oq2:
            word = next((c for c in changes if c["bar"] == oq2["bar"]), None)
        elif paired:
            word = next((p for p in passes.get(paired["row"], []) if p.get("version") == version and p.get("pair") == paired["pair"]
                         and isinstance(p.get("word"), str) and p["word"].strip()), None)
        else:
            word = None
        if word:
            printed.append(f"release: owner's word recorded -- {rest} ({word['word']})")
        else:
            open_.append(line)
            printed.append(line)
    if open_:
        printed.append(f"release-check: owner's word needed for {len(open_)} line(s): " + SB._named([f"[{line[len(NEEDED):]}]" for line in open_]))
        return 1, printed
    printed.append("release-check: ok")
    return 0, printed


# --------------------------------------------------------------------------------------- the command line

def add_release_check_arguments(parser) -> None:
    parser.add_argument("--release", metavar="VERSION", help="the direct road: run `compare --release VERSION` and judge its lines (norms.json and the scoreboards are read)")
    parser.add_argument("--version", help="with --lines: the package version being released (a worsened_passes entry must name it)")
    parser.add_argument("--lines", help="the other input: a saved `compare --release` output, a file, or - for stdin")
    parser.add_argument("--norms", help="default experiments/scoreboards/norms.json")
    parser.add_argument("--root", help="with --release: the scoreboards folder (default experiments/scoreboards)")
    parser.set_defaults(run=cmd_release_check)


def cmd_release_check(args) -> int:
    try:
        if (args.release is None) == (args.lines is None):
            raise SB.Refusal("release-check takes exactly one input: `--release VERSION` (it runs compare --release itself) or `--lines FILE|-` with `--version V`")
        if args.release is not None:
            lines, produced, version = release_lines(args.release, SB.load_norms(args.norms), args.root), True, args.release
        else:
            if not args.version:
                raise SB.Refusal("`--lines` needs `--version V`: a worsened_passes entry is matched by version")
            text = sys.stdin.read() if args.lines == "-" else SB._read_text(args.lines, "the release lines file")
            lines, produced, version = text.splitlines(), False, args.version
        code, printed = release_check(lines, version, args.norms, produced)
    except SB.Refusal as exc:
        return SB._red(str(exc))
    for line in printed:
        print(line)
    return code


def cmd_price(args) -> int:
    cfg = None
    if args.cfg:
        try:
            cfg = SB._load_json(args.cfg, "the cost config")
        except SB.Refusal as exc:
            return SB._red(str(exc))
    print(price_line(bar_price(args.transcript or [], cfg, args.result or [])))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, prog="scoreboard_bar.py")
    sub = parser.add_subparsers(dest="command", required=True, metavar="{price,release-check}")
    p = sub.add_parser("price", help="re-price the free arm's transcripts by the catalogue; the host's total is printed beside it")
    p.add_argument("--transcript", action="append", help="a free-arm session transcript (repeatable: a resume is several)")
    p.add_argument("--result", action="append", help="a free-N.log result file (its total_cost_usd is printed only)")
    p.add_argument("--cfg", help="the project's cost block as JSON (rate_overrides)")
    p.set_defaults(run=cmd_price)
    r = sub.add_parser("release-check", help="exit 0 only when no release line needs the owner's word, or each has it recorded")
    add_release_check_arguments(r)
    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
