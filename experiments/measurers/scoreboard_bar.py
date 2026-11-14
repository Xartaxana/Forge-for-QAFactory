#!/usr/bin/env python3
"""The free-agent bar's price and the release check of the run scoreboard (P1-v N7).

    python -B experiments/measurers/scoreboard_bar.py price --transcript T [--transcript T2 ...] [--result free-N.log ...] [--cfg cost.json]
    python -B experiments/measurers/scoreboard_bar.py release-check --version V --lines FILE|- [--norms norms.json]
    python -B experiments/measurers/scoreboard.py release-check --version V --lines FILE|-      (the same command, through scoreboard.py)

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

def bar_better_line(row: str, bar_file: str, better, factory, bar) -> str | None:
    """OQ2: the line `release: owner's word needed -- <row> ratcheted, new bar <bar file> is better than the factory` when the new bar is
    STRICTLY better than the factory's value on a ratcheted row (ranges: the whole bar range beyond the factory's whole range), else None.
    A value that is not a number or a range, or a row with no direction, is a refusal naming it: not-better is never assumed."""
    a, b = SB._range(factory), SB._range(bar)
    if a is None or b is None or better not in ("lower", "higher"):
        raise SB.Refusal(f"row {row}: the factory value {factory!r}, the bar value {bar!r} or the direction {better!r} cannot be compared")
    beats = b[1] < a[0] if better == "lower" else b[0] > a[1]
    return f"{NEEDED}{row} ratcheted, new bar {bar_file} is better than the factory" if beats else None


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


def release_check(lines, version: str, norms_path=None) -> tuple:
    """(exit code, printed lines). 0: no line needs the owner's word, or each has it recorded; 1: the list; a Refusal for unreadable input."""
    lines = [str(line).strip() for line in lines if str(line).strip()]
    if not lines:
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
    parser.add_argument("--version", required=True, help="the package version being released (a worsened_passes entry must name it)")
    parser.add_argument("--lines", required=True, help="the `compare --release` output: a file, or - for stdin")
    parser.add_argument("--norms", help="default experiments/scoreboards/norms.json")
    parser.set_defaults(run=cmd_release_check)


def cmd_release_check(args) -> int:
    try:
        if args.lines == "-":
            text = sys.stdin.read()
        else:
            text = SB._read_text(args.lines, "the release lines file")
        code, printed = release_check(text.splitlines(), args.version, args.norms)
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
