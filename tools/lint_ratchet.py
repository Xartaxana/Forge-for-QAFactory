"""Lint ratchet -- a narrow "bugs only" check (pyflakes) over the package scripts and the Forge tools,
gated by a SHRINK-ONLY baseline of the findings that exist today (owner decision 03.10, t-394).

What it protects: a syntax error or an undefined name never reaches main unseen, and the count of
the other findings (unused import / variable, redefinition, f-string without placeholders ...) only
goes down. No formatter, no style rule, no type checker.

Modes:
  python tools/lint_ratchet.py --check     (default) compare the live findings with tools/lint-baseline.json
  python tools/lint_ratchet.py --update    rewrite the baseline from the live findings (a deliberate act:
                                           say why in the commit); refuses while any file does not parse
Options (for tests and odd checkouts; the defaults are the constants below):
  --repo PATH      the repository root (default: the parent of tools/)
  --root REL       a root, relative to the repo, repeatable (default: ROOTS)
  --baseline PATH  the baseline file (default: tools/lint-baseline.json)

Identity of a finding = (repo-relative POSIX path, the pyflakes message class name, the message
arguments joined). NO line and NO column: an unrelated edit above a finding does not make it "new".
Identical identities in one file are counted; the baseline stores a count per identity. Three classes
carry a line number inside their arguments ("from line N"): RedefinedWhileUnused,
ImportShadowedByLoopVar, UndefinedLocal -- the digits at argument position 1 are replaced by `<line>`.

Always red, never baselined: a file that does not parse (class `SyntaxError`) and a file that cannot be
read or decoded (class `UnexpectedError`). `--update` refuses while one exists, naming file and line.

Exit codes (stdout carries the report; stderr only crashes):
  0  --check: no new finding and no stale row; --update: baseline written
  1  --check: a new finding, a higher count, a stale baseline row, or a file that does not parse;
     --update: refused because a file does not parse
  2  the tool cannot judge: pyflakes is not installed, a root does not exist, the baseline is missing
     or malformed, or it was generated with another pyflakes version than the one running (a version
     drift must not read as new findings; the header key is `pyflakes_version`; an unknown is never a pass)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

import streams

REPO = Path(__file__).resolve().parent.parent
ROOTS = ("ai-packages/qa-factory/scripts", "tools")           # data, not logic: add a root here
BASELINE_DEFAULT = REPO / "tools" / "lint-baseline.json"
FATAL_CLASSES = ("SyntaxError", "UnexpectedError")            # never baselined
LINE_ARG_CLASSES = ("RedefinedWhileUnused", "ImportShadowedByLoopVar", "UndefinedLocal")  # args[1] is a line
SKIP_DIRS = ("__pycache__",)
GENERATED_BY = "python tools/lint_ratchet.py --update (pyflakes; identity = path + class + arguments, no line)"
DOOR_NEW = ("fix it, or -- when the finding is deliberate -- record it with "
            "`python tools/lint_ratchet.py --update` and say why in the commit")
DOOR_STALE = "stale baseline row(s) -- the finding is gone: run `python tools/lint_ratchet.py --update` to shrink the baseline"
PIP_SENTENCE = "pyflakes is not installed: pip install pyflakes"      # `==<baseline version>` is appended when known
DOOR_PARSE = ("fix the file so it parses; a deliberately unparsable fixture is kept under a non-.py name "
              "or written by its test into a temp dir")


class Finding:
    __slots__ = ("path", "line", "cls", "args", "text")

    def __init__(self, path: str, line: int, cls: str, args: tuple, text: str):
        self.path, self.line, self.cls, self.args, self.text = path, line, cls, args, text

    @property
    def identity(self) -> tuple:
        return (self.path, self.cls, ", ".join(self.args))


class Collector:
    """A pyflakes reporter that keeps the findings instead of printing them."""

    def __init__(self, rel: str):
        self.rel = rel
        self.found: list = []

    def unexpectedError(self, filename, msg):
        self.found.append(Finding(self.rel, 1, "UnexpectedError", (str(msg),), str(msg)))

    def syntaxError(self, filename, msg, lineno, offset, text):
        self.found.append(Finding(self.rel, max(lineno or 0, 1), "SyntaxError", (str(msg),), str(msg)))

    def flake(self, message):
        raw = message.message_args
        args = tuple(raw) if isinstance(raw, tuple) else (raw,)
        shown = [str(a) for a in args]
        if type(message).__name__ in LINE_ARG_CLASSES and len(shown) >= 2:
            shown[1] = "<line>"
        try:
            text = message.message % message.message_args
        except Exception:
            text = str(message)
        self.found.append(Finding(self.rel, message.lineno, type(message).__name__, tuple(shown), text))


def python_files(root_dir: Path):
    """Every .py under root_dir, sorted, `__pycache__` skipped."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        out.extend(Path(dirpath) / n for n in sorted(filenames) if n.endswith(".py"))
    return sorted(out, key=lambda p: p.as_posix())


def lint_tree(repo: Path, roots, checkpath) -> list:
    findings: list = []
    seen = set()
    for root in roots:
        for f in python_files(repo / root):
            rel = f.resolve().relative_to(repo.resolve()).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            col = Collector(rel)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                checkpath(str(f), col)
            findings.extend(col.found)
    return findings


def counts(findings) -> dict:
    out: dict = {}
    for f in findings:
        out[f.identity] = out.get(f.identity, 0) + 1
    return out


def load_baseline(path: Path):
    """The baseline as ({identity: count}, pyflakes_version); raises ValueError with a sentence when it cannot be trusted."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data["rows"]
        version = data.get("pyflakes_version")
        out = {}
        for r in rows:
            ident = (r["path"], r["class"], r["args"])
            if r["class"] in FATAL_CLASSES:
                raise ValueError(f"row {ident!r} is a {r['class']}: those are never baselined")
            if not isinstance(r["count"], int) or r["count"] < 1:
                raise ValueError(f"row {ident!r} has no positive count")
            out[ident] = r["count"]
        return out, version
    except OSError as exc:
        raise ValueError(f"cannot read the baseline {path}: {exc}") from exc
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"the baseline {path} is malformed ({type(exc).__name__}: {exc})") from exc


def format_baseline(cnt: dict, version: str) -> str:
    rows = [{"path": p, "class": c, "args": a, "count": n} for (p, c, a), n in sorted(cnt.items())]
    doc = {"generated_by": GENERATED_BY, "pyflakes_version": version, "total": sum(cnt.values()), "rows": rows}
    return json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def run(argv=None) -> int:
    ap = argparse.ArgumentParser(description="pyflakes ratchet over the package scripts and tools/")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare with the baseline (default)")
    mode.add_argument("--update", action="store_true", help="rewrite the baseline from the live findings")
    ap.add_argument("--repo", default=str(REPO), help="repository root")
    ap.add_argument("--root", action="append", metavar="REL", help="a root relative to the repo (repeatable)")
    ap.add_argument("--baseline", default=None, help="baseline file")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    baseline_path = Path(args.baseline) if args.baseline else (repo / "tools" / "lint-baseline.json")
    try:
        import pyflakes.api as pyflakes_api  # noqa: F401  (the missing-module case is the point)
    except ImportError:
        pinned = None
        try:
            pinned = load_baseline(baseline_path)[1]
        except ValueError:
            pass
        print(f"{PIP_SENTENCE}=={pinned}" if pinned else PIP_SENTENCE)
        return 2

    import pyflakes
    version = str(getattr(pyflakes, "__version__", "unknown"))
    roots = tuple(args.root) if args.root else ROOTS
    for root in roots:
        d = repo / root
        if not d.is_dir():
            print(f"lint ratchet: the root `{root}` does not exist under {repo.as_posix()} -- nothing was checked; "
                  f"the configured ROOTS are {', '.join(ROOTS)} (override with `--root REL`, repeatable, relative to `--repo`)")
            return 2

    findings = lint_tree(repo, roots, pyflakes_api.checkPath)
    fatal = [f for f in findings if f.cls in FATAL_CLASSES]
    live = counts([f for f in findings if f.cls not in FATAL_CLASSES])

    if args.update:
        if fatal:
            print("lint ratchet: --update refused -- a file that does not parse can never be baselined:")
            for f in fatal:
                print(f"  {f.path}:{f.line}: {f.cls}: {f.text}")
            print(DOOR_PARSE)
            return 1
        old = None
        if baseline_path.is_file():
            try:
                old = load_baseline(baseline_path)[0]
            except ValueError:
                old = None
        old = old or {}
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(format_baseline(live, version), encoding="utf-8", newline="\n")
        added = sum(1 for k in live if k not in old)
        removed = sum(1 for k in old if k not in live)
        changed = sum(1 for k in live if k in old and live[k] != old[k])
        print(f"lint ratchet: baseline written: {len(live)} rows, {sum(live.values())} findings "
              f"({added} rows added, {removed} removed, {changed} with a changed count)")
        # a grown baseline must be readable in the command's own output: every added row and every count that went up
        for k in sorted(live):
            if k not in old:
                print(f"  added: {k[0]}: {k[1]} {k[2]}  (0 -> {live[k]})")
            elif live[k] > old[k]:
                print(f"  grew: {k[0]}: {k[1]} {k[2]}  ({old[k]} -> {live[k]})")
        return 0

    try:
        base, base_version = load_baseline(baseline_path)
    except ValueError as exc:
        print(f"lint ratchet: {exc}; record the current state with `python tools/lint_ratchet.py --update`")
        return 2
    if base_version != version:
        print(f"lint ratchet: the baseline was generated with pyflakes {base_version or 'an unrecorded version'}, "
              f"this is {version}: install pyflakes=={base_version or '<the baseline version>'} or regenerate with --update")
        return 2

    total = sum(live.values())
    new_n = sum(max(n - base.get(k, 0), 0) for k, n in live.items())
    stale_n = sum(max(n - live.get(k, 0), 0) for k, n in base.items())
    covered = total - new_n
    print(f"lint ratchet: {total} findings, {covered} in the baseline, {new_n} new, {stale_n} stale (pyflakes {version})")
    bad = False
    if fatal:
        bad = True
        print("files that do not parse (always red, never baselined):")
        for f in fatal:
            print(f"  {f.path}:{f.line}: {f.cls}: {f.text}")
        print(DOOR_PARSE)
    offenders = [k for k, n in live.items() if n > base.get(k, 0)]
    if offenders:
        bad = True
        print("new finding(s):")
        for f in findings:
            if f.cls not in FATAL_CLASSES and f.identity in offenders:
                print(f"  {f.path}:{f.line}: {f.text}  [{f.cls}]")
        for k in offenders:
            if base.get(k, 0):
                print(f"  ({k[0]} {k[1]}: {live[k]} now, {base[k]} in the baseline)")
        print(DOOR_NEW)
    stale = sorted(k for k, n in base.items() if n > live.get(k, 0))
    if stale:
        bad = True
        print("stale baseline row(s):")
        for k in stale:
            print(f"  {k[0]}: {k[1]} {k[2]}  ({live.get(k, 0)} now, {base[k]} in the baseline)")
        print(DOOR_STALE)
    return 1 if bad else 0


def main(argv=None) -> int:
    streams.utf8_stdio()
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
