#!/usr/bin/env python3
"""Registry preflight (FG7-92): which registry checks a change can break, run narrowly, as ADVICE.

Owner's word 18.11: registry misses (a unit with no census row, a family name with no driver-layers row, a reader-shaped
JSON function, a test file with no keep row, a new pyflakes finding) reached main because a builder's narrow DoD never ran
the registry checks. This file holds THE one rule table (`RULES`: changed path -> narrow check) and three doors:

  python -B tools/registry_preflight.py check <id>... [--root DIR] [--paths REL...]   run named checks in-process
  python -B tools/registry_preflight.py run [--repo DIR] [--base origin/main] [--head HEAD]   diff -> rows -> children
  rules_for(paths) / command_for(paths)   the pure reader API for dispatch_new.py (FG7-93)

It never stops a merge (row FG7-94: branches merge, main may go red, one fixer repairs it): a red, a crash and a timeout
are printed, never raised into wave. Exit codes: 0 nothing red and nothing unjudged, 1 any red, 2 else any `cannot judge`.
A check that cannot run is `cannot judge`, never `ok`. Every narrow call imports the TREE's modules (a rename there makes
the row `cannot judge`, not wrong). Whole-file runs of the canon-class test files are never done here.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import shlex
import shutil
import subprocess
import sys
import time
from fnmatch import fnmatchcase
from pathlib import Path

import lint_ratchet

HERE = Path(__file__).resolve()
REPO = HERE.parent.parent
PKG = "ai-packages/qa-factory"
SCRIPTS = PKG + "/scripts"
TESTS = SCRIPTS + "/tests"
CHECK_TIMEOUT = 30.0            # seconds per row (module constant: a test moves it)
TOTAL_BUDGET = 60.0             # seconds per run
NO_RULE_SHOW = 10
PROBLEM_SHOW = 5
MARK = "registry preflight:"
_clock = time.monotonic         # a seam for tests
_normcase = os.path.normcase    # a seam for tests (the Windows prefix fold)

# (glob, ad_only): ad_only signs select on an added/deleted/renamed path only (a content edit changes no role name, no listing)
_SCRIPTS_PY = (SCRIPTS + "/*.py", False)
RULES = (
    ("census", (_SCRIPTS_PY, (TESTS + "/fixtures/judgment-census.json", False), (PKG + "/references/stages.json", False),
                (PKG + "/agents/*.md", True)),
     "a check unit with no census row, a stale row, a raised ceiling (C1-C5)"),
    ("driver-layers", (_SCRIPTS_PY, (TESTS + "/fixtures/*-layers.json", False)),
     "a family name with no map row, L1-L12 on the real maps"),
    ("read-json", (_SCRIPTS_PY,), "a reader-shaped JSON function outside KEPT, a stale KEPT row"),
    ("test-layers", ((TESTS + "/test-layers.json", False), (SCRIPTS + "/slow_tests.json", False), (TESTS + "/test_*.py", True)),
     "malformed layers data, a keep row naming no file, an unlisted new test file, a broken named_by"),
    ("lint", tuple((r.strip("/") + "/**/*.py", False) for r in lint_ratchet.ROOTS),     # read from the module, never copied
     "a new pyflakes finding, a file that does not parse, a stale baseline row, a hand-input match"),
)
IDS = tuple(r[0] for r in RULES)


class CannotJudge(Exception):
    """A narrow call that cannot run or whose answer cannot be trusted: the row reads `cannot judge`."""


class Report:
    def __init__(self):
        self.rows = []            # (id, state, seconds, lines); state in ok | red | cannot
        self.no_rule = []
        self.empty = False
        self.failed = None        # the text when no diff could be read (no row exists then)

    def code(self):
        if any(r[1] == "red" for r in self.rows):
            return 1
        return 2 if self.failed or any(r[1] == "cannot" for r in self.rows) else 0


# ---- the pure reader API (no git, no subprocess, no file read)
def _segs(path):
    return [s for s in path.split("/") if s not in ("", ".")]


def _m(g, p):
    if not g:
        return not p
    if g[0] == "**":
        return any(_m(g[1:], p[i:]) for i in range(len(p) + 1))
    return bool(p) and fnmatchcase(p[0], g[0]) and _m(g[1:], p[1:])


def _anc(g, p):
    """p is a directory above (or on the way to) what g signs: err toward selecting more. Without a file read a path whose
    last segment has a dot is a file, not a directory (a dotted directory name is the one miss)."""
    if p and "." in p[-1]:
        return False
    if not p:
        return True
    return bool(g) and (g[0] == "**" or (fnmatchcase(p[0], g[0]) and _anc(g[1:], p[1:])))


def select(entries):
    """ids of the rows selected by [(repo-relative posix path, status A|D|M)], table order, no duplicates."""
    out = []
    for rid, signs, _why in RULES:
        for glob, ad_only in signs:
            if any((st in "AD" or not ad_only) and (_m(_segs(glob), _segs(p)) or _anc(_segs(glob), _segs(p)))
                   for p, st in entries):
                out.append(rid)
                break
    return out


def _entry(path, repo):
    """(rel, status) for an owns-line path (absolute or relative, either slash, ` (new)` marker), None when outside the repo."""
    text = str(path).strip()
    status = "M"
    if text.endswith("(new)"):
        text, status = text[:-5].rstrip(), "A"
    text = text.replace("\\", "/")
    if text[:1] == "/" or (len(text) > 1 and text[1] == ":"):
        prefix = Path(repo).as_posix().rstrip("/")
        if _normcase(text[:len(prefix)]) != _normcase(prefix) or text[len(prefix):len(prefix) + 1] not in ("/", ""):
            return None
        text = text[len(prefix):]
    rel = "/".join(_segs(text))
    return (rel, status) if ".." not in rel.split("/") else None


def _entries(paths, repo):
    return [e for e in (_entry(p, repo or REPO) for p in paths) if e is not None]


def rules_for(paths, repo=None):
    return select(_entries(paths, repo))


def _lint_paths(rels):
    roots = tuple(r.strip("/") + "/" for r in lint_ratchet.ROOTS)
    return [r for r in rels if r.endswith(".py") and r.startswith(roots)]


def command_for(paths, repo=None):
    entries = _entries(paths, repo)
    ids = select(entries)
    lint = _lint_paths(sorted({r for r, _s in entries}))
    if "lint" in ids and not lint:
        ids.remove("lint")          # a directory owns path names no file: `check lint` would have nothing to narrow to
    if not ids:
        return None
    cmd = "python -B tools/registry_preflight.py check " + " ".join(ids)
    if "lint" in ids:
        cmd += " --paths " + " ".join(shlex.quote(p) if any(c in p for c in " '\"") else p for p in lint)
    return cmd


# ---- the narrow calls (in-process, on the tree's modules); a problem list, [] = ok, raise = cannot judge
def _sys_path(root):
    for rel in (SCRIPTS, TESTS):
        p = str(Path(root) / rel)
        if p in sys.path:
            sys.path.remove(p)
        sys.path.insert(0, p)


def _fail_lines(text):
    return [ln[5:] for ln in text.splitlines() if ln.startswith("FAIL ")]


def _check_census(root, paths):
    import harness
    import test_judgment_census as T
    probs = T.analyse(harness.PLUGIN_ROOT, T.load_census())["problems"]
    return [t for k in ("C1", "C2", "C3", "C4", "C5") for t in probs[k]]


def _check_driver_layers(root, paths):
    import test_driver_layers as T
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        T.real_maps()
    return _fail_lines(buf.getvalue())


def _check_read_json(root, paths):
    import test_read_json as T
    found, unparsed = T.census(Path(root) / SCRIPTS)
    new, stale = T.census_verdict(found, T.KEPT)
    return ([f"reader-shaped JSON function not in KEPT: {n} ({found[n]})" for n in new]
            + [f"stale KEPT row (no such reader any more): {n}" for n in stale] + [f"did not parse: {n}" for n in unparsed])


def _check_test_layers(root, paths):
    import selftest as S
    try:
        layers = S.test_layers()
        S.slow_tests()
    except (S.TestLayersError, S.SlowTestsError) as exc:
        return [str(exc)]
    files = [Path(root) / r for r, _s in _entries(paths, root) if r.startswith(TESTS + "/test_") and r.endswith(".py")
             and "/" not in r[len(TESTS) + 1:] and (Path(root) / r).is_file()]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = S._listing_ok(layers, files, True)
    return [] if ok else (_fail_lines(buf.getvalue()) or ["the test listing is not ok"])


def _check_lint(root, paths):
    py = _lint_paths(sorted({r for r, _s in _entries(paths, root)}))
    if not py:
        raise CannotJudge("no .py path under the lint roots named (--paths); the whole run is CI's")
    cmd = [sys.executable, "-B", str(Path(root) / "tools" / "lint_ratchet.py"), "--check", "--repo", str(root)]
    for p in py:
        cmd += ["--path", p]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=CHECK_TIMEOUT)
    if p.returncode == 0:
        return []
    last = (p.stdout.strip().splitlines() or p.stderr.strip().splitlines() or ["no output"])[-1]
    if p.returncode != 1:
        raise CannotJudge(f"lint_ratchet exit {p.returncode}: {last}"[:200])
    lines = [ln.strip() for ln in p.stdout.splitlines() if ln.startswith("  ")]
    return lines or p.stdout.strip().splitlines()


CALLS = {"census": _check_census, "driver-layers": _check_driver_layers, "read-json": _check_read_json,
         "test-layers": _check_test_layers, "lint": _check_lint}


# ---- lines
def _flat(problems):
    return [ln.rstrip() for t in problems for ln in str(t).splitlines() if ln.strip()]


def row_lines(rid, state, secs, detail=()):
    """The printed lines of one row; for a red, `detail` is the problem lines (cut to PROBLEM_SHOW + `+k more`)."""
    if state == "ok":
        return [f"{MARK} {rid} ok ({secs:.1f} s)"]
    if state == "cannot":
        return [f"{MARK} {rid} cannot judge ({detail})"]
    shown = ["  " + ln.strip() if not ln.startswith("  ") else ln for ln in list(detail)[:PROBLEM_SHOW]]
    more = [f"  +{len(detail) - PROBLEM_SHOW} more"] if len(detail) > PROBLEM_SHOW else []
    return [f"{MARK} {rid} RED ({secs:.1f} s)"] + shown + more


def _summary(rows):
    r = sum(1 for x in rows if x[1] != "cannot")
    return (f"{MARK} {r} run, {sum(1 for x in rows if x[1] == 'red')} red, {sum(1 for x in rows if x[1] == 'cannot')} cannot judge "
            f"-- the merge goes on (advice; owner 18.11, FG7-94)")


def _why(exc):
    return f"{type(exc).__name__}: {exc}"[:200]


# ---- the `check` door (in-process)
def check(ids, root, paths, out=print):
    _sys_path(root)
    rows = []
    for rid in ids:
        t0 = _clock()
        try:
            problems = _flat(CALLS[rid](root, paths))
            state, detail = ("red", problems) if problems else ("ok", ())
        except (Exception, SystemExit) as exc:          # SystemExit: an imported test module that finishes by itself
            state, detail = "cannot", _why(exc)
        secs = _clock() - t0
        rows.append((rid, state, secs, row_lines(rid, state, secs, detail)))
        for ln in rows[-1][3]:
            out(ln)
    return rows


# ---- the `run` door
def _git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", str(repo), "-c", "core.quotepath=false", *args], capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        return 255, "", type(exc).__name__
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace").strip()


def _run_child(argv, timeout):
    p = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def _judge(rc, out, err):
    """(state, detail) of one child's answer: only exit 0 is ok, only exit 1 is red."""
    if rc == 0:
        return "ok", ()
    if rc == 1:
        return "red", [ln for ln in out.splitlines() if ln.startswith("  ")]
    for ln in out.splitlines():
        if "cannot judge (" in ln and ln.endswith(")"):
            return "cannot", ln[ln.index("cannot judge (") + 14:-1]
    tail = (err.strip().splitlines() or out.strip().splitlines() or ["no output"])[-1]
    return "cannot", f"exit {rc}: {tail}"[:200]


def _changed(repo, base, head):
    rc, out, err = _git(repo, "diff", "--name-status", "--no-renames", "-z", f"{base}...{head}")
    if rc != 0:
        raise CannotJudge(f"git diff: {err[:200]}")
    parts = out.split("\0")
    return [(parts[i + 1], parts[i][:1]) for i in range(0, len(parts) - 1, 2) if parts[i]]


def preflight(repo, base, head, out=print, runner=None):
    runner = runner or _run_child
    rep, lines = Report(), []

    def say(text):
        lines.append(text)
        out(text)

    try:
        entries = _changed(repo, base, head)
    except CannotJudge as exc:
        rep.failed = str(exc)
        say(f"{MARK} cannot judge ({exc})")
        return rep
    if not entries:
        rep.empty = True
        say(f"{MARK} no change against {base}")
        return rep
    ids = select(entries)
    rep.no_rule = [p for p, st in entries if not select([(p, st)])]
    if rep.no_rule:
        k = len(rep.no_rule) - NO_RULE_SHOW
        say(f"{MARK} no rule for {len(rep.no_rule)} file(s): {', '.join(rep.no_rule[:NO_RULE_SHOW])}" + (f" +{k} more" if k > 0 else ""))
    if ids:
        _run_rows(repo, head, ids, entries, rep, say, runner)
    say(_summary(rep.rows))
    return rep


def _run_rows(repo, head, ids, entries, rep, say, runner):
    tree = Path(repo) / ".claude" / "worktrees" / f"preflight-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    rc, _o, err = _git(repo, "worktree", "add", "--detach", str(tree), head)
    if rc != 0:
        for rid in ids:
            rep.rows.append((rid, "cannot", 0.0, row_lines(rid, "cannot", 0.0, f"worktree add: {err[:150]}")))
            say(rep.rows[-1][3][0])
        return
    try:
        paths = _lint_paths(sorted({p for p, _s in entries}))
        t_start = _clock()
        for rid in ids:
            left = TOTAL_BUDGET - (_clock() - t_start)
            t0 = _clock()
            if left <= 0:
                state, detail = "cannot", "budget spent"
            else:
                tmo = min(CHECK_TIMEOUT, left)
                argv = [sys.executable, "-B", str(HERE), "check", rid, "--root", str(tree)] + (["--paths", *paths] if paths else [])
                try:
                    state, detail = _judge(*runner(argv, tmo))
                except subprocess.TimeoutExpired:
                    state, detail = "cannot", f"timeout after {tmo:g} s"
                except Exception as exc:
                    state, detail = "cannot", _why(exc)
            secs = _clock() - t0
            # a child's red lines are already cut to PROBLEM_SHOW + `+k more`: cutting twice would lose the count
            ls = [f"{MARK} {rid} RED ({secs:.1f} s)"] + list(detail) if state == "red" else row_lines(rid, state, secs, detail)
            rep.rows.append((rid, state, secs, ls))
            for ln in ls:
                say(ln)
    finally:
        _drop(repo, tree, say)


def _drop(repo, tree, say):
    """The order of wave.Wave.drop; a failure is one line, never a raise (the sweep cleans a leftover copy later)."""
    try:
        _git(repo, "worktree", "remove", "--force", str(tree))
        if tree.exists():
            shutil.rmtree(tree, ignore_errors=True)
        _git(repo, "worktree", "prune")
        if tree.exists():
            say(f"{MARK} the temporary tree {tree} was not removed; the worktree sweep cleans it later")
    except Exception as exc:
        say(f"{MARK} the temporary tree {tree} was not removed ({_why(exc)})")


def _parser():
    ap = argparse.ArgumentParser(prog="registry_preflight.py", description="registry checks by changed files (advice, never a gate)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="run named checks in-process on a tree")
    c.add_argument("ids", nargs="*")
    c.add_argument("--root", default=str(REPO))
    c.add_argument("--paths", nargs="*", default=[], metavar="REL")
    r = sub.add_parser("run", help="read a diff, select rows, run them in child processes")
    r.add_argument("--repo", default=str(REPO))
    r.add_argument("--base", default="origin/main")
    r.add_argument("--head", default="HEAD")
    return ap


def main(argv=None):
    try:
        import streams
        streams.utf8_stdio()
    except Exception:
        pass
    a = _parser().parse_args(argv)
    if a.cmd == "run":
        return preflight(a.repo, a.base, a.head).code()
    bad = [i for i in a.ids if i not in CALLS]
    if bad or not a.ids:
        print(f"unknown check {', '.join(bad) or '(none named)'}; known: {', '.join(IDS)}")
        return 2
    rows = check(a.ids, Path(a.root), a.paths)
    rep = Report()
    rep.rows = rows
    return rep.code()


if __name__ == "__main__":
    sys.exit(main())
