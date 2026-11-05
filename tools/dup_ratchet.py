"""Clone ratchet -- no new clone group, and no new copy of a known one, reaches main unseen (BACKLOG B-417, t-518).

A GATE built on tools/dup_report.py (the measurement, B-309): the same reader (`dup_report.analyse`), one run per
scope, compared with a committed baseline, tools/dup-baseline.json. What it protects: "fixed in one place,
forgotten in the other" (owner, 04.10, 06.10) -- a copy that the report would show is stopped where a person can
still call the existing function instead. The baseline only shrinks; it grows by the Lead's word.

Modes:
  python tools/dup_ratchet.py --check     (default) compare the live groups with the baseline
  python tools/dup_ratchet.py --update    rewrite the baseline from the live groups (a deliberate act: say why in
                                          the commit); refuses while any file does not parse; warns about every
                                          uncommitted change inside a scope (the baseline describes the COMMITTED tree)
Options (for tests and odd checkouts; the defaults are the constants below):
  --repo PATH      the repository root (default: the parent of tools/)
  --baseline PATH  the baseline file (default: <--repo>/tools/dup-baseline.json)
  --scope NAME=GLOB  a scope, repeatable (one NAME may take several GLOBs); given at all, it replaces SCOPES and
                   EXCLUDES; the globs are relative to --repo
  --report DIR     first write DIR/dup-report-<scope>.md for every scope (dup_report's markdown, every group
                   shown), BEFORE any judgement -- also when the baseline is missing -- then judge as usual

Scopes are data (SCOPES, EXCLUDES): the product scripts, and tools/ WITHOUT its tests (tests repeat by design --
P16 -- and a test block copied once more must not turn every tools node red).

Identity of a group = its fingerprint (dup_report: the normalised code, no path, no line). A move, a rename, a
reorder, an edit above it, a CRLF or BOM form do not change it. A baseline row = scope, fingerprint, kind,
statements, copies, members [path, in] sorted, duplicates kept. NO line anywhere in the file.

Judgement per scope (the lines the report prints name every offender with `path:first-last in`):
  KNOWN    a live group whose fingerprint is a row, with no more copies than the row (fewer = SHRUNK, green, listed)
  GROWN    ... with more copies than the row: red
  CARRIED  a live group with no matching row that the code of an old row still accounts for: its members are a
           sub-multiset of the row's members, and the carried statements of that row (summed) stay at or below the
           row's `statements`; the row's fingerprint must not be live -- or be live and SHRUNK, and the carried
           group must contain a member the live group no longer has (a clone between copies that are still live
           copies of the row is never carried). Green, listed. Greedy by (-statements, fingerprint): a suboptimal
           match errs red. A group no single row can hold (a deletion elsewhere merged two fragment runs into one
           longer run) is charged across the eligible rows while their remaining budgets together cover it. A new
           fragment wholly inside another new group (a nested statement list) is judged with that group and not
           charged again (listed as "nested").
  NEW     anything else: red
  GONE / DIVERGED  a row with no live fingerprint: DIVERGED when every member path was read (the code changed in
           one place -- check the other copy), GONE when a member path was not (deleted, moved, unreadable).
           Both green, listed; `--update` removes them.
Always red, never baselined: a file that does not parse. `--update` refuses while one exists.
Error direction: it may err RED (an edit that changes both identities; the door is `--update` and a sentence in
the commit); it errs GREEN only for the carried groups above, an exact re-add of a GONE row's code before the next
`--update`, and what dup_report cannot see (equivalent code written differently, cross-scope copies, tests).

Exit codes (stdout carries the report; stderr carries the wall time):
  0  --check: nothing new, nothing grown, every file parsed; --update: baseline written
  1  --check: a new or grown group, or a file that does not parse; --update: refused because a file does not parse
  2  the tool cannot judge: the baseline is missing or malformed; its basis (normalisation, options) or its scopes
     differ from this run; a scope matched no files; dup_report raised a usage error; its JSON lacks a key the
     reader needs or its `groups` do not add up to `totals.groups`; or a red result under another Python minor
     than the baseline's (the baseline records "X.Y"; drift errs red, so a green result stands)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import dup_report
import gitcmd
import streams
from lint_ratchet import DOOR_PARSE

REPO = Path(__file__).resolve().parent.parent
SCOPES = {"scripts": dup_report.DEFAULT_PATHS, "tools": ("tools/*.py",)}              # data, not logic: add a scope here
EXCLUDES = {"tools": ("tools/test_*.py",)}
BASELINE_RELATIVE = "tools/dup-baseline.json"
GENERATED_BY = ("python tools/dup_ratchet.py --update (dup_report fingerprints; identity = scope + fingerprint, "
                "no path of a copy and no line)")
DOOR_NEW = ("remove the copy (call the existing function), or -- when the copy is deliberate and the Lead has agreed -- "
            "record it with `python tools/dup_ratchet.py --update` and say why in the commit")
DOOR_BASELINE = "record the current state with `python tools/dup_ratchet.py --update`"
DIVERGED_HINT = "changed in one place? check the other copy"
KINDS = ("function", "fragment")
BASIS_KEYS = ("normalisation", "python", "min_statements", "window", "strict", "with_imports")


class Cannot(Exception):
    """The tool cannot judge (exit 2): the sentence says what is missing and what to do."""


def python_minor() -> str:
    return "%d.%d" % sys.version_info[:2]


def current_basis(normalisation: int) -> dict:
    return {"normalisation": normalisation, "python": python_minor(), "min_statements": dup_report.DEFAULT_MIN_STATEMENTS,
            "window": dup_report.DEFAULT_WINDOW, "strict": False, "with_imports": False}


# ---------------------------------------------------------------- groups: live ones and baseline rows

@dataclass
class Clone:
    """One clone group: from the live report (with `locations`) or a baseline row (without)."""
    scope: str
    fingerprint: str
    kind: str
    statements: int
    copies: int
    members: list                                  # sorted [(path, in)], duplicates kept
    locations: list = field(default_factory=list)  # live only: the report's {path, first, last, in}

    @property
    def members_counter(self) -> Counter:
        return Counter(self.members)


def clones_of(scope: str, rep: dict) -> list:
    out = []
    for g in rep["groups"]:
        members = sorted((loc["path"], loc["in"]) for loc in g["locations"])
        out.append(Clone(scope, g["fingerprint"], g["kind"], g["statements"], g["copies"], members, g["locations"]))
    return out


def describe(clone: Clone, indent: str = "  ") -> list:
    lines = [f"{indent}{clone.kind}, {clone.statements} statements, {clone.copies} copies:"]
    if clone.locations:
        lines += [f"{indent}  {loc['path']}:{loc['first']}-{loc['last']} {loc['in']}" for loc in clone.locations]
    else:                                          # a baseline row carries no line
        lines += [f"{indent}  {path} {where}" for path, where in clone.members]
    return lines


# ---------------------------------------------------------------- the live side: one dup_report run per scope

@dataclass
class ScopeRun:
    name: str
    paths: tuple
    exclude: tuple
    rep: dict
    files: list                                    # the repo-relative files the scope's globs matched
    seconds: float

    @property
    def unreadable(self) -> list:
        return self.rep["unreadable"]

    @property
    def files_read(self) -> set:
        return set(self.files) - {u["path"] for u in self.unreadable}

    @property
    def definition(self) -> dict:
        return {"paths": list(self.paths), "exclude": list(self.exclude)}


def define_scopes(repo: Path, scope_args) -> dict:
    """{name: (paths, exclude)}: the SCOPES / EXCLUDES data, or `--scope NAME=GLOB` (no excludes)."""
    if not scope_args:
        return {name: (dup_report.normalise_patterns(repo, paths), dup_report.normalise_patterns(repo, EXCLUDES.get(name, ())))
                for name, paths in SCOPES.items()}
    given: dict = {}
    for item in scope_args:
        name, sep, glob = item.partition("=")
        if not (name and sep and glob):
            raise Cannot(f"--scope wants NAME=GLOB, got `{item}`")
        given.setdefault(name, []).append(glob)
    return {name: (dup_report.normalise_patterns(repo, globs), ()) for name, globs in given.items()}


def require(obj, key: str, where: str, scope: str, kind=None):
    if not isinstance(obj, dict) or key not in obj or (kind is not None and not isinstance(obj[key], kind)):
        raise Cannot(f"the dup_report JSON for scope `{scope}` lacks `{where}{key}`"
                     f"{'' if kind is None else ' of type ' + kind.__name__}: the reader and the report disagree on the "
                     f"shape, nothing was judged (bring tools/dup_ratchet.py and tools/dup_report.py back in line)")
    return obj[key]


def validate_report(rep: dict, scope: str) -> None:
    """A JSON that does not carry what the reader needs is never read as "no groups" (E11); `groups` cut short is the same."""
    totals = require(rep, "totals", "", scope, dict)
    for key in ("files_read", "files_unreadable", "groups"):
        require(totals, key, "totals.", scope, int)
    for u in require(rep, "unreadable", "", scope, list):
        require(u, "path", "unreadable[].", scope, str)
        require(u, "error", "unreadable[].", scope, str)
    require(require(rep, "fingerprint_basis", "", scope, dict), "normalisation", "fingerprint_basis.", scope, int)
    require(rep, "options", "", scope, dict)
    groups = require(rep, "groups", "", scope, list)
    for g in groups:
        for key, kind in (("fingerprint", str), ("kind", str), ("statements", int), ("copies", int), ("locations", list)):
            require(g, key, "groups[].", scope, kind)
        for loc in g["locations"]:
            for key, kind in (("path", str), ("first", int), ("last", int), ("in", str)):
                require(loc, key, "groups[].locations[].", scope, kind)
    if len(groups) != totals["groups"]:
        raise Cannot(f"scope `{scope}`: the report lists {len(groups)} groups but counts {totals['groups']}: a group is "
                     f"invisible (a cut-off?) -- nothing was judged")
    if len({g["fingerprint"] for g in groups}) != len(groups):
        raise Cannot(f"scope `{scope}`: two groups share a fingerprint -- the identity is not unique, nothing was judged")


def analyse_scopes(repo: Path, scopes: dict) -> list:
    runs = []
    for name, (paths, exclude) in scopes.items():
        started = time.monotonic()
        files = dup_report.resolve_files(repo, paths, exclude)             # once per scope: analyse reads the same list
        rep = dup_report.analyse(repo, paths, dup_report.DEFAULT_MIN_STATEMENTS, dup_report.DEFAULT_WINDOW, False,
                                 sys.maxsize, False, exclude, files)
        validate_report(rep, name)
        runs.append(ScopeRun(name, paths, exclude, rep, files, time.monotonic() - started))
    return runs


def require_files(runs: list) -> None:
    for run in runs:
        if not run.files:
            raise Cannot(f"scope `{run.name}` matched no files ({', '.join(run.paths)}"
                         f"{'; excluding ' + ', '.join(run.exclude) if run.exclude else ''}) -- nothing was checked; "
                         f"is --repo the repository root?")


def write_reports(directory: Path, runs: list) -> None:
    """dup_report's markdown for every scope, every group shown; a pure function of the tree."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        for run in runs:
            rep = dict(run.rep, options=dict(run.rep["options"], top=len(run.rep["groups"])))
            (directory / f"dup-report-{run.name}.md").write_text(dup_report.render_markdown(rep) + "\n",
                                                                  encoding="utf-8", newline="\n")
    except OSError as exc:
        raise Cannot(f"cannot write the report into {directory}: {exc}") from exc


# ---------------------------------------------------------------- the baseline

@dataclass
class Baseline:
    basis: dict
    scopes: dict
    rows: list

    def rows_of(self, scope: str) -> list:
        return [r for r in self.rows if r.scope == scope]


def parse_row(raw, scopes: dict) -> Clone:
    if not isinstance(raw, dict):
        raise ValueError("a row is not an object")
    for key in ("first", "last"):
        if key in raw:
            raise ValueError(f"a row carries `{key}`: the identity has no line")
    scope, fp, kind = raw["scope"], raw["fingerprint"], raw["kind"]
    if scope not in scopes or not isinstance(fp, str) or kind not in KINDS:
        raise ValueError(f"row {scope!r}/{fp!r} has an unknown scope, kind or fingerprint")
    statements, copies, members = raw["statements"], raw["copies"], raw["members"]
    if not isinstance(statements, int) or statements < 1:
        raise ValueError(f"row {fp!r} has no positive `statements`")
    if not isinstance(copies, int) or copies < 2:
        raise ValueError(f"row {fp!r} has `copies` {copies!r}: a clone has at least two")
    if not (isinstance(members, list) and len(members) == copies
            and all(isinstance(m, list) and len(m) == 2 and all(isinstance(x, str) for x in m) for m in members)):
        raise ValueError(f"row {fp!r}: `members` must be {copies} pairs [path, in]")
    return Clone(scope, fp, kind, statements, copies, sorted(tuple(m) for m in members))


def shown(path: Path) -> str:
    """A path for a message: relative to the working directory when it lies under it (the CI log carries no absolute path)."""
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_baseline(path: Path) -> Baseline:
    """The baseline, or a Cannot with a sentence: a baseline that cannot be trusted never judges (E1, E2)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise Cannot(f"the baseline {shown(path)} does not exist; {DOOR_BASELINE}") from exc
    except (OSError, ValueError) as exc:
        raise Cannot(f"cannot read the baseline {shown(path)} ({type(exc).__name__}: {exc}); {DOOR_BASELINE}") from exc
    try:
        basis, scopes = parse_header(data)
        rows, seen = [], set()
        for raw in data["rows"]:
            row = parse_row(raw, scopes)
            if (row.scope, row.fingerprint) in seen:
                raise ValueError(f"the row {row.scope}/{row.fingerprint} appears twice")
            seen.add((row.scope, row.fingerprint))
            rows.append(row)
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        raise Cannot(f"the baseline {shown(path)} is malformed ({type(exc).__name__}: {exc}); {DOOR_BASELINE}") from exc
    rows.sort(key=lambda r: (r.scope, r.kind, r.fingerprint))    # the file's row order never decides a verdict (first fit)
    return Baseline(basis, scopes, rows)


def parse_header(data) -> tuple:
    basis, scopes = data["basis"], data["scopes"]
    if not isinstance(basis, dict) or [k for k in BASIS_KEYS if k not in basis]:
        raise ValueError(f"`basis` must be an object with {', '.join(BASIS_KEYS)}")
    if not isinstance(scopes, dict) or not all(isinstance(d, dict) and isinstance(d.get("paths"), list)
                                               and isinstance(d.get("exclude"), list) for d in scopes.values()):
        raise ValueError("`scopes` must map a name to {paths: [...], exclude: [...]}")
    return basis, scopes


def baseline_text(runs: list, normalisation: int) -> str:
    rows = []
    for run in runs:
        for c in clones_of(run.name, run.rep):
            rows.append({"scope": c.scope, "fingerprint": c.fingerprint, "kind": c.kind, "statements": c.statements,
                         "copies": c.copies, "members": [list(m) for m in c.members]})
    rows.sort(key=lambda r: (r["scope"], r["kind"], r["fingerprint"]))
    doc = {"generated_by": GENERATED_BY, "basis": current_basis(normalisation),
           "scopes": {run.name: run.definition for run in runs}, "total": len(rows), "rows": rows}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def compare_basis(base: Baseline, normalisation: int) -> None:
    """Normalisation or options drift: every fingerprint would move, so it must not read as new groups (E12)."""
    now = current_basis(normalisation)
    drift = [f"{k}: {base.basis[k]!r} in the baseline, {now[k]!r} now" for k in BASIS_KEYS if k != "python" and base.basis[k] != now[k]]
    if drift:
        raise Cannot("the baseline was generated on another basis (" + "; ".join(drift) + "): bump and regenerate in the "
                     "same commit -- " + DOOR_BASELINE)


def compare_scopes(base: Baseline, runs: list) -> None:
    mine = {run.name: run.definition for run in runs}
    if set(base.scopes) != set(mine):
        raise Cannot(f"the scopes differ: the baseline has {sorted(base.scopes)}, this run {sorted(mine)}; {DOOR_BASELINE}")
    for name, d in mine.items():
        if base.scopes[name] != d:
            raise Cannot(f"scope `{name}` is defined differently: the baseline has {base.scopes[name]}, this run {d}; "
                         f"{DOOR_BASELINE}")


# ---------------------------------------------------------------- the judgement

class Slot:
    """What an old row still accounts for: a statement budget, and the members that may be carried onto it."""

    def __init__(self, row: Clone, lost):
        self.row, self.lost, self.budget = row, lost, row.statements

    def eligible(self, group: Clone) -> bool:
        """The places condition (E7): the group's members are a sub-multiset of the row's; and for a live SHRUNK row
        the group holds a member the live group lost (A2). The budget is judged apart (`charge`)."""
        members = group.members_counter
        if self.lost is not None and not (members & self.lost):
            return False                           # a clone among copies that are still live copies of the row
        return not (members - self.row.members_counter)


def charge(group: Clone, slots: list) -> list:
    """The rows that pay for `group`: one slot that holds all of it, else -- a deletion elsewhere can merge two
    fragment runs into one longer run (F-2) -- the eligible slots whose remaining budgets together cover it. []
    when nobody can: the group is NEW."""
    able = [s for s in slots if s.eligible(group)]
    one = next((s for s in able if group.statements <= s.budget), None)
    payers = [one] if one else able
    if sum(s.budget for s in payers) < group.statements:
        return []
    left, rows = group.statements, []
    for s in payers:
        take = min(s.budget, left)
        if take:
            s.budget -= take
            left -= take
            rows.append(s.row)
    return rows


def inside(outer: Clone, group: Clone) -> bool:
    """Every location of `group` lies within a location of `outer`, in the same file and the same function."""
    return all(any(o["path"] == loc["path"] and o["in"] == loc["in"] and o["first"] <= loc["first"] and loc["last"] <= o["last"]
                   for o in outer.locations) for loc in group.locations)


def drop_nested(groups: list) -> tuple:
    """dup_report reports a fragment for every statement list, nested ones too: a fragment wholly inside another new
    group is the same duplicated code once more, and must not be charged twice (F-1; mirrors dup_report.drop_covered).
    -> (kept, nested)."""
    kept, nested = [], []
    for g in groups:
        covered = g.kind == "fragment" and any(o is not g and o.statements > g.statements and inside(o, g) for o in groups)
        (nested if covered else kept).append(g)
    return kept, nested


@dataclass
class Verdict:
    live: list
    known: list                                    # [(group, row)]: matched by fingerprint, no more copies than the row
    grown: list                                    # [(group, row)]
    carried: list                                  # [(group, [rows that pay])]
    new: list
    nested: list                                   # new fragments inside another new group: not judged apart
    gone: list                                     # rows with no live fingerprint, a member path not read
    diverged: list                                 # rows with no live fingerprint, every member path read

    @property
    def shrunk(self) -> list:
        return [(g, row) for g, row in self.known if g.copies < row.copies]

    @property
    def red(self) -> bool:
        return bool(self.new or self.grown)


def carry_slots(rows: list, live: list, known: list) -> list:
    live_fps = {g.fingerprint for g in live}
    lost = {row.fingerprint: row.members_counter - g.members_counter for g, row in known if g.copies < row.copies}
    slots = []
    for row in rows:
        if row.fingerprint not in live_fps:
            slots.append(Slot(row, None))
        elif row.fingerprint in lost:              # live and SHRUNK: only its lost members may be carried
            slots.append(Slot(row, lost[row.fingerprint]))
    return slots                                   # a live row at its full count, or grown, is never a fallback


def judge_scope(rows: list, live: list, read_files) -> Verdict:
    by_fp = {r.fingerprint: r for r in rows}
    known, grown, unmatched = [], [], []
    for g in live:
        row = by_fp.get(g.fingerprint)
        if row is None:
            unmatched.append(g)
        elif g.copies > row.copies:
            grown.append((g, row))
        else:
            known.append((g, row))
    unmatched, nested = drop_nested(unmatched)
    slots, carried = carry_slots(rows, live, known), []
    for g in sorted(unmatched, key=lambda g: (-g.statements, g.fingerprint)):
        paying = charge(g, slots)
        if paying:
            carried.append((g, paying))
    taken = {id(g) for g, _ in carried}
    live_fps = {g.fingerprint for g in live}
    vanished = [r for r in rows if r.fingerprint not in live_fps]
    gone_ids = {id(g) for g in nested}
    return Verdict([g for g in live if id(g) not in gone_ids], known, grown, carried,
                   [g for g in unmatched if id(g) not in taken], nested,
                   [r for r in vanished if any(p not in read_files for p, _ in r.members)],
                   [r for r in vanished if all(p in read_files for p, _ in r.members)])


def summary_line(name: str, v: Verdict) -> str:
    s = len(v.shrunk) + len(v.gone) + len(v.diverged)
    return (f"dup ratchet: {name}: {len(v.live)} groups, {len(v.known)} known, {len(v.new)} new, {len(v.grown)} grown, "
            f"{len(v.carried)} carried, {s} shrunk/gone ({len(v.diverged)} diverged)")


def print_verdict(name: str, v: Verdict) -> None:
    print(summary_line(name, v))
    if v.new:
        print(f"new group(s) in {name}:")
        for g in v.new:
            print("\n".join(describe(g)))
    if v.grown:
        print(f"grown group(s) in {name} (more copies than the baseline):")
        for g, row in v.grown:
            print("\n".join(describe(g)) + f"\n    ({g.copies} now, {row.copies} in the baseline)")
    if v.carried:
        print(f"carried in {name} (green: the code of an old row, same places, within its size):")
        for g, rows in v.carried:
            paid = ", ".join(f"{r.fingerprint[:12]} ({r.kind}, {r.statements} statements)" for r in rows)
            print("\n".join(describe(g)) + f"\n    (carried onto the baseline row(s) {paid})")
    if v.nested:
        print(f"nested in {name} (green: wholly inside another new group above, judged with it):")
        for g in v.nested:
            print("\n".join(describe(g)))
    if v.shrunk:
        print(f"shrunk in {name} (green, fewer copies than the baseline):")
        for g, row in v.shrunk:
            print("\n".join(describe(g)) + f"\n    ({g.copies} now, {row.copies} in the baseline)")
    if v.diverged:
        print(f"diverged in {name} (green; {DIVERGED_HINT}):")
        for row in v.diverged:
            print("\n".join(describe(row)))
    if v.gone:
        print(f"gone from {name} (green; a member file was deleted, moved or is unreadable):")
        for row in v.gone:
            print("\n".join(describe(row)))


def print_unreadable(runs: list) -> bool:
    bad = [(run.name, u) for run in runs for u in run.unreadable]
    if bad:
        print("files that do not parse (always red, never baselined):")
        for name, u in bad:
            print(f"  {u['path']}: {u['error']}  [{name}]")
        print(DOOR_PARSE)
    return bool(bad)


def check(baseline_path: Path, runs: list, normalisation: int) -> int:
    base = load_baseline(baseline_path)
    compare_basis(base, normalisation)
    compare_scopes(base, runs)
    verdicts = [(run.name, judge_scope(base.rows_of(run.name), clones_of(run.name, run.rep), run.files_read))
                for run in runs]
    for name, v in verdicts:
        print_verdict(name, v)
    red = print_unreadable(runs)
    if any(v.red for _, v in verdicts):
        red = True
        print(DOOR_NEW)
    if red and base.basis["python"] != python_minor():
        print(f"dup ratchet: the baseline was generated under Python {base.basis['python']}, this is {python_minor()}: "
              f"the fingerprints may differ between minors -- run it under Python {base.basis['python']} or regenerate "
              f"with --update")
        return 2
    return 1 if red else 0


# ---------------------------------------------------------------- --update

def status_changes(repo: Path, pathspec) -> list:
    """The `git status --porcelain` entries under the pathspecs, one call (tools/gitcmd.py), the paths as git prints them.
    Raises RuntimeError with the reason when git cannot say. The one git-status reader of this tool and of the
    lint ratchet's real-tree skip (tools/test_lint_ratchet.py)."""
    rc, out, err = gitcmd.git(repo, "status", "--porcelain", "--untracked-files=all", "--", *pathspec, stderr=True)
    if rc == -1:                                   # gitcmd: git missing, did not start, or timed out (the message is in err)
        raise RuntimeError(f"git status unavailable: {err.decode('utf-8', 'replace')}")
    if rc != 0:
        raise RuntimeError(f"git status failed: {err.decode('utf-8', 'replace').strip()[:80]}")
    return [line[3:].split(" -> ")[-1].strip('"') for line in out.decode("utf-8", "replace").splitlines() if len(line) > 3]


def scope_changes(repo: Path, scopes: dict) -> list:
    """The uncommitted entries inside a scope: the baseline must describe the COMMITTED tree. RuntimeError when git cannot say."""
    spec = [":(glob)" + p for paths, _ in scopes.values() for p in paths]
    spec += [":(exclude,glob)" + e for _, exclude in scopes.values() for e in exclude]
    return status_changes(repo, spec)


def warn_uncommitted(repo: Path, scopes: dict) -> None:
    try:
        changes = scope_changes(repo, scopes)
    except RuntimeError as exc:
        print(f"warning: {exc}; uncommitted changes in a scope were not looked for")
        return
    for path in changes:
        print(f"warning: uncommitted change in a scope: {path}")


def update(repo: Path, baseline_path: Path, runs: list, scopes: dict, normalisation: int) -> int:
    if print_unreadable(runs):
        print("dup ratchet: --update refused -- a file that does not parse can never be baselined; the baseline is unchanged")
        return 1
    warn_uncommitted(repo, scopes)
    try:
        old = {(r.scope, r.fingerprint): r for r in load_baseline(baseline_path).rows}
    except Cannot:
        old = {}
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(baseline_text(runs, normalisation), encoding="utf-8", newline="\n")
    live = {(c.scope, c.fingerprint): c for run in runs for c in clones_of(run.name, run.rep)}
    added = [k for k in live if k not in old]
    grew = [k for k in live if k in old and live[k].copies > old[k].copies]
    removed = [k for k in old if k not in live]
    print(f"dup ratchet: baseline written: {len(live)} rows ({len(added)} added, {len(removed)} removed, {len(grew)} grew)")
    for label, keys in (("added", added), ("grew", grew)):         # a grown baseline must be readable in the command's own output
        for key in sorted(keys, key=lambda k: (k[0], live[k].kind, k[1])):
            was = f" ({old[key].copies} -> {live[key].copies} copies)" if key in old else ""
            print(f"  {label}: {key[0]}{was}")
            print("\n".join(describe(live[key], "    ")))
    return 0


# ---------------------------------------------------------------- command line

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="the clone ratchet over the product scripts and tools/ (a gate on dup_report)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare with the baseline (default)")
    mode.add_argument("--update", action="store_true", help="rewrite the baseline from the live groups")
    ap.add_argument("--repo", default=str(REPO), help="repository root")
    ap.add_argument("--baseline", default=None, help="baseline file (default: <repo>/" + BASELINE_RELATIVE + ")")
    ap.add_argument("--scope", action="append", metavar="NAME=GLOB", help="a scope (repeatable); replaces SCOPES and EXCLUDES")
    ap.add_argument("--report", default=None, metavar="DIR", help="write DIR/dup-report-<scope>.md for every scope first")
    return ap


def run(argv=None) -> int:
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:                      # argparse: 2 on a usage error, 0 on --help
        return int(exc.code or 0)
    repo = Path(args.repo).resolve()
    baseline_path = Path(args.baseline) if args.baseline else repo / BASELINE_RELATIVE
    try:
        if not repo.is_dir():
            raise Cannot("--repo is not a directory")
        scopes = define_scopes(repo, args.scope)
        runs = analyse_scopes(repo, scopes)
        print("dup ratchet: " + ", ".join(f"{r.name} {len(r.files)} files in {r.seconds:.1f}s" for r in runs), file=sys.stderr)
        if args.report:
            write_reports(Path(args.report), runs)
        require_files(runs)
        normalisation = runs[0].rep["fingerprint_basis"]["normalisation"]
        if args.update:
            return update(repo, baseline_path, runs, scopes, normalisation)
        return check(baseline_path, runs, normalisation)
    except dup_report.UsageError as exc:
        print(f"dup ratchet: dup_report refused the call: {exc}")
        return 2
    except Cannot as exc:
        print(f"dup ratchet: {exc}")
        return 2


def main(argv=None) -> int:
    streams.utf8_stdio()
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
