"""owns_readers.py -- facts about the files a dispatch owns or is given, read from the BASE TREE: who names them, which test
files are quarantined or slow, which paths or names are not on the base. Data for the dispatcher, the plan critic and the
builder; it gathers, it decides nothing (P27): no verdict word, never "the spec is complete", never a refusal.

    python -B tools/owns_readers.py --paths <p>... [--given <p>...] [--names <n>...] [--base <ref>] [--repo <dir>]
                                    [--readers] [--all]

  --paths    owned paths (absolute or repo-relative; a trailing " (new)" marks a new file). At least one: none -> exit 2.
  --given    given paths: presence and layer status only; readers are not counted for them.
  --names    names the spec changes or introduces (a function, key, flag, constant); " (new)" marks one the change CREATES.
             At most 20 are searched; the rest are named in one `unsearched` line.
  --base     the tree searched (default origin/main; any ref or sha). The tool never fetches; the header prints the sha.
  --repo     the repository root (default: the parent of tools/).
  --readers  list the reader files (tests first) instead of counting them; --all lifts every listing cap and also lists the
             code and quarantined readers (implies --readers).
Python API (what tools/dispatch_new.py calls): report(paths, given=(), names=(), base="origin/main", repo=None) -> Report;
render(report, readers=False, all_=False) -> str. Writes nothing. Output shape, kinds and caps: spec section 2.2 and 2.4;
the scope globs and the caps are DATA in tools/owns_readers.json.

An unknown is printed as unknown, never as zero readers, "not quarantined", "not slow", "present" or "absent" (FR-59, AR-28):
a git call that fails gives a header segment (`quarantine|slow|presence|names: unknown (<why>)`, or `readers: unknown -- git
grep exited <rc>`), and the rest of the block is kept.

KNOWN MISSES (the plan critic's duty starts here; each one is answered in docs/tasks/critic-diff-brief.md item 13 (d)):
  1. transitive readers (a test imports `a`, which imports the owned `b`): for a package path `scenario_walk.py
     --witness-for` is the transitive list;
  2. a path built from pieces, a name read from data, `importlib` with a computed string;
  3. a pin on a VALUE without the file name (a frozen dict pinning `qa-retro-analyst 14075`): `--names` only;
  4. stems under 4 characters (those are searched by file name only);
  5. readers outside the scope (docs, plans: prose readers are the designer's own walk);
  6. a stale base: the tool does not fetch; the header prints the sha it searched;
  7. a common-word stem of 4+ characters over-counts (`contract` is a whole word in 537 scope files against 96 naming
     `contract.py`): counted, never dropped; in a listing it sinks to the third tier.
Forge tests (tools/) have no layer registry, so no layer status is printed for them (no such data row exists: a difference
of data, not a branch on a name). `tools/test_quarantine.py` and `tools/test_split.py` are TOOLS named `test_*`: counted as
tests (over-report, never a reader dropped).

Git reads go through tools/gitcmd.git, EXCEPT the `git show` inside the reused `test_quarantine._blob_sections`, which
runs `test_quarantine._git` (its own subprocess runner: timeout 120, any exception -> rc 128). Imports of other code, each
a named dependence (a rename breaks it into `unknown`, never into a wrong fact): `test_quarantine._blob_sections`,
`._pkg_module`, `.Unknown`; `selftest._slow_tests_problem` (the shape validator of the one reader of slow_tests.json).
Slow = MEMBERSHIP in the `files` of slow_tests.json (the reader's meaning); no threshold is applied.

REMOVAL (the owner's open question of 17.11.2026 on deleting the quarantine): `_quarantine_status`, its call, the
`quarantined` kind, the `Q quarantined` part of `more` and the test rows `quarantine-*` of tools/test_owns_readers.py are
deleted TOGETHER with the quarantine section of test-layers.json. Until then the function is right in both worlds: with the
section present it reports, with the section gone (keep present) it is quiet. If tools/test_quarantine.py goes too,
`_slow_status`'s loader (`_pkg_module`) moves first.

TWO QUESTIONS, TWO ANSWERS (spec section 2.7; plans/builder-rules.md 7b): `scenario_walk.py --witness-for <path>` answers what
to RUN for a package path (the keep `covers` plus the import closure; the DoD names it); this tool answers what must not
break or be edited (literal readers, layer status, presence). Their convergence is a queued node, not stated here.

Exit: 0 printed; 2 no path given (a door in the text). Spec: docs/tasks/specs/20261116-spec-facts-by-code-spec.md.
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import dispatch_manifest  # noqa: E402
import gitcmd  # noqa: E402
import streams  # noqa: E402

CONFIG_FILE = _TOOLS_DIR / "owns_readers.json"
METHOD = "literal mention; known misses: tools/owns_readers.py docstring"
KIND_ORDER = ("hot", "quarantined", "slow", "absent", "exists", "names", "outside", "data", "more", "unsearched")
SHARD = 80                      # patterns per git call (command-line length)
_WORDY = re.compile(r"[A-Za-z0-9_](?:.*[A-Za-z0-9_])?", re.S)
_DRIVE = re.compile(r"[A-Za-z]:[/\\]")
QUAR_NOTE = "(quarantined: the canon does not run it; do not edit)"


# --- data --------------------------------------------------------------------------------------------------------------

_CFG: dict = {}


def _config() -> dict:
    """tools/owns_readers.json with the scope rows compiled to regexes for classifying a hit (cached)."""
    if not _CFG:
        raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
        scope = raw["scope"]
        raw["_rows"] = [(cls, [_glob_re(g) for g in scope[cls]]) for cls in ("tests", "data", "code")]
        raw["_specs"] = [":(glob)" + g for cls in ("tests", "data", "code") for g in scope[cls]] + \
                        [":(exclude,glob)" + g for g in scope["exclude"]]
        _CFG.update(raw)
    return _CFG


def _glob_re(glob: str):
    """A pathspec glob (`:(glob)` semantics: `*` stays inside a directory, `**/` is zero or more directories)."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob.startswith("/**", i) and i + 3 == len(glob):
            out.append("/.*")
            i += 3
        elif glob.startswith("**", i):
            out.append(".*")
            i += 2
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def _classify(path: str) -> str:
    """test / data / code by the first scope row that matches; a hit no row matches is counted as code (over-report)."""
    for cls, rows in _config()["_rows"]:
        if any(r.match(path) for r in rows):
            return "test" if cls == "tests" else cls
    return "code"


# --- the report ----------------------------------------------------------------------------------------------------------

@dataclass
class Reader:
    path: str
    cls: str                     # test | data | code
    quarantined: object          # True | False | None (unknown: the registry could not be read)
    slow: bool
    layered: bool                # under the package tests directory
    tier: int                    # 0 namesake test_<stem>*, 1 names the full file name, 2 stem only


@dataclass
class Subject:
    kind: str                    # path | name
    label: str
    readers: list = field(default_factory=list)


@dataclass
class Report:
    ref: str
    sha: str = ""
    base_why: str = ""
    grep_fail: str = ""
    segments: dict = field(default_factory=dict)       # quarantine | slow | presence | names -> why
    facts: dict = field(default_factory=dict)          # kind -> ready lines (no reader counts)
    subjects: list = field(default_factory=list)
    names_searched: bool = False


def _first_line(raw) -> str:
    text = gitcmd.as_text(raw) if isinstance(raw, (bytes, bytearray)) else str(raw or "")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines[0][:160] if lines else "no message"


def _fact(rep: Report, kind: str, text: str) -> None:
    rep.facts.setdefault(kind, []).append("- %s: %s" % (kind, text))


def _wordable(pat: str) -> bool:
    return bool(_WORDY.fullmatch(pat))


def _git(repo, *args):
    """gitcmd.git with stderr; a runner that raises is rc -1 (never an exception to the caller)."""
    try:
        return gitcmd.git(repo, *args, stderr=True)
    except Exception as exc:  # noqa: BLE001
        return -1, b"", str(exc).encode("utf-8", "replace")


def _resolve(repo, ref: str):
    """(sha, why): the commit `ref` names, or None and the first line git gave."""
    if not ref or ref.startswith("-"):
        return None, "a base ref that is empty or starts with '-' is not read as a ref"
    rc, out, err = _git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    sha = gitcmd.as_text(out).strip().split("\n")[0] if rc == 0 else ""
    if rc == 0 and re.fullmatch(r"[0-9a-f]{40,64}", sha):
        return sha, ""
    return None, _first_line(err or out)


# --- inputs --------------------------------------------------------------------------------------------------------------

@dataclass
class _Item:
    label: str
    rel: str = ""
    new: bool = False
    outside: bool = False
    bad: bool = False


def _split_new(raw) -> tuple:
    text = str(raw).strip()
    if text.lower().endswith(" (new)"):
        return text[:-6].rstrip(), True
    return text, False


def _item(raw, repo_real: Path, mark_new: bool) -> _Item | None:
    text, new = _split_new(raw) if mark_new else (str(raw).strip(), False)
    if not text:
        return None
    if any(ord(c) < 32 for c in text):
        return _Item(label="", bad=True)
    if os.path.isabs(text) or _DRIVE.match(text):
        if _DRIVE.match(text) and os.name != "nt":
            return _Item(label=posixpath.basename(text.replace("\\", "/")), new=new, outside=True)
        try:
            rel = Path(os.path.realpath(text)).relative_to(repo_real).as_posix()
        except ValueError:
            return _Item(label=posixpath.basename(text.replace("\\", "/")), new=new, outside=True)
    else:
        rel = posixpath.normpath(text.replace("\\", "/"))
        if rel == ".." or rel.startswith("../"):
            return _Item(label=posixpath.basename(rel), new=new, outside=True)
    return _Item(label=rel, rel=rel, new=new)


def _under(rel: str, f: str) -> bool:
    return rel == "." or f == rel or f.startswith(rel.rstrip("/") + "/")


# --- git facts -----------------------------------------------------------------------------------------------------------

def _ls_tree(repo, sha: str, rels: list):
    """(set of files under the literal paths | None, why). rc != 0 is UNKNOWN."""
    rc, out, err = _git(repo, "ls-tree", "-r", "-z", "--name-only", "--full-tree", sha, "--", *rels)
    if rc != 0:
        return None, "git ls-tree exited %s (%s)" % (rc, _first_line(err or out))
    return {f for f in out.decode("utf-8", "replace").split("\0") if f}, ""


def _quarantine_status(repo, sha: str, present):
    """(set of quarantined file names | None, why). The tool's ONLY use of test_quarantine._blob_sections. Registry presence
    comes from the ls-tree of the caller (True / False / None = unknown); every failure is None, never an empty set."""
    sha8 = sha[:8]
    if present is None:
        return None, "the presence of test-layers.json could not be listed"
    if not present:
        return None, "test-layers.json absent at %s" % sha8
    try:
        import test_quarantine as tq
        try:
            sections = tq._blob_sections(str(repo), sha)
        except tq.Unknown:
            return None, "test-layers.json at %s is not JSON" % sha8
    except Exception as exc:  # noqa: BLE001
        return None, "test-layers.json could not be read (%s)" % type(exc).__name__
    if not sections.get("keep") and not sections.get("quarantine"):
        return None, "test-layers.json present at %s but read empty" % sha8
    return set(sections.get("quarantine") or {}), ""


def _slow_status(repo, sha: str, present):
    """(set of slow test file names | None, why): MEMBERSHIP in `files` of slow_tests.json, shape judged by the one reader's
    validator selftest._slow_tests_problem (loaded from this tool's own checkout)."""
    sha8 = sha[:8]
    rel = _config()["layers"]["slow_registry"]
    if present is None:
        return None, "the presence of slow_tests.json could not be listed"
    if not present:
        return None, "slow_tests.json absent at %s" % sha8
    rc, out, err = _git(repo, "show", "%s:%s" % (sha, rel))
    if rc != 0:
        return None, "git show exited %s (%s)" % (rc, _first_line(err or out))
    try:
        raw = json.loads(gitcmd.as_text(out).lstrip("﻿"))
    except ValueError:
        return None, "slow_tests.json at %s is not JSON" % sha8
    try:
        import test_quarantine as tq
        problem = tq._pkg_module(_TOOLS_DIR.parent, "selftest")._slow_tests_problem(raw)
    except Exception as exc:  # noqa: BLE001
        return None, "the selftest module did not load (%s)" % type(exc).__name__
    if problem:
        return None, "slow_tests.json at %s: %s" % (sha8, problem)
    return set(raw["files"]), ""


def _groups(pats) -> list:
    """Pattern groups for git calls: whole-word patterns apart from plain ones (S-8), no pattern a substring of another in
    one group (git -o prints only the longest match at a position), at most SHARD patterns per call."""
    calls = []
    for word in (True, False):
        chosen = sorted({p for p in pats if _wordable(p) == word}, key=lambda p: (-len(p), p))
        groups: list = []
        for p in chosen:
            for g in groups:
                if not any(p in q for q in g):
                    g.append(p)
                    break
            else:
                groups.append([p])
        for g in groups:
            calls.extend((word, g[i:i + SHARD]) for i in range(0, len(g), SHARD))
    return calls


def _grep(repo, sha: str, pats, specs=None):
    """(set of (path, pattern) hits, '' | failure text). `git grep -I -o -z -F`; rc 0 hits, 1 none, anything else (128, -1)
    is a failure of the whole search (UNKNOWN, never zero hits). Every pattern follows -e and every path follows `--`."""
    hits: set = set()
    prefix = sha + ":"
    for word, group in _groups(pats):
        args = ["grep", "-I", "-o", "-z", "-F"] + (["-w"] if word else [])
        for p in group:
            args += ["-e", p]
        args.append(sha)
        if specs:
            args += ["--", *specs]
        rc, out, err = _git(repo, *args)
        if rc not in (0, 1):
            return hits, "git grep exited %s (%s)" % (rc, _first_line(err or out))
        for line in out.decode("utf-8", "replace").split("\n"):
            head, sep, match = line.partition("\0")
            if sep and head.startswith(prefix):
                hits.add((head[len(prefix):], match))
    return hits, ""


# --- report --------------------------------------------------------------------------------------------------------------

def report(paths, given=(), names=(), base="origin/main", repo=None) -> Report:
    repo = Path(repo) if repo else _TOOLS_DIR.parent
    cfg = _config()
    rep = Report(ref=base)
    sha, why = _resolve(repo, base)
    if sha is None:
        rep.base_why = why
        return rep
    rep.sha = sha
    sha8 = sha[:8]
    repo_real = Path(os.path.realpath(repo))
    caps, layers = cfg["caps"], cfg["layers"]

    owned = [i for i in (_item(p, repo_real, True) for p in paths) if i]
    given_items = [i for i in (_item(p, repo_real, False) for p in given) if i]
    bad = [i for i in owned + given_items if i.bad]
    if bad:
        _fact(rep, "unsearched", "%d paths with a control character (not searched)" % len(bad))
    combined = [("owned", i) for i in owned if not i.bad] + [("given", i) for i in given_items if not i.bad]
    if len(combined) > dispatch_manifest.PATH_CAP:
        over = len(combined) - dispatch_manifest.PATH_CAP
        combined = combined[:dispatch_manifest.PATH_CAP]
        _fact(rep, "unsearched", "%d more paths over the cap" % over)
    for role, it in combined:
        if it.outside:
            _fact(rep, "unsearched", "%s (outside the repo; pass the repo path)" % it.label)
    inside = [(role, it) for role, it in combined if not it.outside]

    # (iv) presence: ONE ls-tree over owned, given and the two registries (literal paths)
    reg_q, reg_s = layers["quarantine_registry"], layers["slow_registry"]
    listing, ls_why = _ls_tree(repo, sha, sorted({it.rel for _, it in inside} | {reg_q, reg_s}))
    if listing is None:
        rep.segments["presence"] = ls_why
    q_present = None if listing is None else reg_q in listing
    s_present = None if listing is None else reg_s in listing

    owned_files: list = []                       # repo-relative files whose readers are searched
    for role, it in inside:
        is_dir = listing is not None and it.rel not in listing and any(_under(it.rel, f) for f in listing)
        if is_dir:
            members = sorted(f for f in listing if _under(it.rel, f))
            if role == "owned":
                if len(members) > caps["dir_cap"]:
                    _fact(rep, "unsearched", "%s holds %d files; readers not counted -- name the files"
                          % (it.rel, len(members)))
                else:
                    owned_files.extend(members)
            continue
        if role == "owned":
            owned_files.append(it.rel)
        if listing is None:
            continue
        if it.rel not in listing and not it.new:
            _fact(rep, "absent", "%s (%s) -- not on %s %s; a worktree builder cannot read it" % (it.rel, role, base, sha8))
        elif it.rel in listing and it.new and role == "owned":
            _fact(rep, "exists", "%s (new) -- already on %s %s" % (it.rel, base, sha8))
    owned_files = list(dict.fromkeys(owned_files))
    owned_set = set(owned_files)

    # (ii) layer status
    q_set, q_why = _quarantine_status(repo, sha, q_present)
    if q_set is None:
        rep.segments["quarantine"] = q_why
    s_set, s_why = _slow_status(repo, sha, s_present)
    if s_set is None:
        rep.segments["slow"] = s_why
    tests_dir = layers["tests_dir"]
    status_seen: set = set()
    status_files = [(f, "owned") for f in owned_files] + [(it.rel, "given") for role, it in inside if role == "given"]
    for f, role in status_files:
        if f.startswith(tests_dir) and (f, role) not in status_seen:
            status_seen.add((f, role))
            name = posixpath.basename(f)
            if q_set is not None and name in q_set:
                _fact(rep, "quarantined", "%s (%s) -- the canon does not run it; a case goes to a keep file" % (f, role))
            if s_set is not None and name in s_set:
                _fact(rep, "slow", "%s (%s) -- listed slow: not run locally, judged by the batch canon" % (f, role))

    # names
    name_items: list = []
    bad_names = 0
    for raw in names:
        text, new = _split_new(raw)
        if not text:
            continue
        if any(ord(c) < 32 for c in text):
            bad_names += 1
        elif text not in [n for n, _ in name_items]:
            name_items.append((text, new))
    if bad_names:
        _fact(rep, "unsearched", "%d names with a control character (not searched)" % bad_names)
    if len(name_items) > caps["names_cap"]:
        _fact(rep, "unsearched", "%d more names over the cap" % (len(name_items) - caps["names_cap"]))
        name_items = name_items[:caps["names_cap"]]
    rep.names_searched = bool(name_items)

    # (i)+(v) one scope search for owned-file patterns and names
    pmap: dict = {}
    for idx, f in enumerate(owned_files):
        base_name = posixpath.basename(f)
        stem = posixpath.splitext(base_name)[0]
        pmap.setdefault(base_name, []).append(("full", idx))
        if len(stem) >= 4 and stem != base_name:
            pmap.setdefault(stem, []).append(("stem", idx))
    for n, (name, _new) in enumerate(name_items):
        pmap.setdefault(name, []).append(("name", n))
    subjects = [Subject("path", f) for f in owned_files] + [Subject("name", n) for n, _ in name_items]
    rep.subjects = subjects
    if pmap:
        hits, fail = _grep(repo, sha, list(pmap), cfg["_specs"])
        if fail:
            rep.grep_fail = fail
        else:
            _attach(rep, hits, pmap, owned_files, owned_set, name_items, q_set, s_set, tests_dir)

    # (v) name presence over the whole tree
    if name_items:
        present, fail = _grep(repo, sha, [n for n, _ in name_items])
        if fail:
            rep.segments["names"] = fail
        else:
            files: dict = {}
            for path, pat in present:
                files.setdefault(pat, set()).add(path)
            for name, new in name_items:
                k = len(files.get(name, ()))
                if not k and not new:
                    _fact(rep, "absent", "name %s -- not named anywhere on %s %s" % (name, base, sha8))
                elif k and new:
                    _fact(rep, "exists", "name %s (new) -- already named by %d files on %s" % (name, k, sha8))
    return rep


def _attach(rep, hits, pmap, owned_files, owned_set, name_items, q_set, s_set, tests_dir) -> None:
    """Turn the hits into the readers of each subject (a hit inside an owned file is dropped)."""
    found: dict = {}                              # (subject index, path) -> {"full", "stem", "name"}
    for path, pat in hits:
        for role, idx in pmap.get(pat, ()):
            sidx = idx if role != "name" else len(owned_files) + idx
            if path in owned_set:
                continue
            found.setdefault((sidx, path), set()).add(role)
    for (sidx, path), roles in found.items():
        subject = rep.subjects[sidx]
        layered = path.startswith(tests_dir)
        name = posixpath.basename(path)
        cls = _classify(path)
        tier = 2
        if subject.kind == "name":
            tier = 0
        else:
            stem = posixpath.splitext(posixpath.basename(subject.label))[0]
            if name.startswith("test_" + stem):
                tier = 0
            elif "full" in roles:
                tier = 1
        quarantined = None if (layered and q_set is None) else (layered and name in q_set)
        slow = bool(layered and s_set is not None and name in s_set)
        subject.readers.append(Reader(path, cls, quarantined, slow, layered, tier))
    for s in rep.subjects:
        s.readers.sort(key=lambda r: (r.tier, r.path))


# --- render --------------------------------------------------------------------------------------------------------------

def _desc(r: Reader) -> str:
    return "test, slow" if r.cls == "test" and r.slow else r.cls


def render(rep: Report, readers: bool = False, all_: bool = False) -> str:
    if not rep.sha:
        return "readers: unknown -- base %s does not resolve here (git: %s); nothing was searched\n" % (
            rep.ref, rep.base_why or "no message")
    caps = _config()["caps"]
    tcap, dcap = caps["test_cap"], caps["data_cap"]
    readers = readers or all_
    out = {k: list(v) for k, v in rep.facts.items()}
    merged = {"names": {}, "outside": {}, "data": {}}      # kind -> reader path -> [text, [subjects]]

    def add(kind, r, text, subject):
        slot = merged[kind].setdefault(r.path, [text, []])
        slot[1].append(subject)

    outside_readers: set = set()
    for s in rep.subjects:
        tests = [r for r in s.readers if r.cls == "test" and r.quarantined is not True]
        quar = [r for r in s.readers if r.cls == "test" and r.quarantined is True]
        code = [r for r in s.readers if r.cls == "code"]
        data = [r for r in s.readers if r.cls == "data"]
        if s.kind == "path":
            outside_readers.update(r.path for r in s.readers)
            if len(tests) > tcap and not rep.names_searched and not all_:
                out.setdefault("hot", []).append(
                    "- hot: %s -- %d test readers; pass --names <the functions or keys you change> for a usable list"
                    % (s.label, len(tests)))
            list_tests, list_data = [], []
            if readers:
                hidden = len(tests) > tcap and rep.names_searched and not all_
                list_tests = [] if hidden else (tests if all_ else tests[:tcap])
                list_data = data if all_ else data[:dcap]
            for r in list_tests:
                add("outside", r, "(%s)" % _desc(r), s.label)
            for r in list_data:
                add("data", r, "", s.label)
        else:
            list_tests = tests if all_ else tests[:tcap]
            list_data = data if all_ else data[:dcap]
            for r in list_tests + list_data:
                add("names", r, "(%s)" % _desc(r), s.label)
        list_quar, list_code = (quar, code) if all_ else ([], [])
        for r in list_code:
            add("outside", r, "(code)", s.label)
        for r in list_quar:
            add("outside", r, "(%s) %s" % (_desc(r), QUAR_NOTE), s.label)
        parts = []
        for count, word in ((len(tests) - len(list_tests), "test"), (len(quar) - len(list_quar), "quarantined")):
            if count:
                parts.append("%d %s" % (count, word))
        if any(r.layered and r.quarantined is None for r in s.readers):
            parts.append("? quarantined")
        for count, word in ((len(code) - len(list_code), "code"), (len(data) - len(list_data), "data")):
            if count:
                parts.append("%d %s" % (count, word))
        if parts:
            subj = s.label if s.kind == "path" else "name %s" % s.label
            out.setdefault("more", []).append(
                "- more: %s -- %s readers not listed (--readers / --all lists them)" % (subj, ", ".join(parts)))
    for kind, slots in merged.items():
        for path, (text, subjects) in slots.items():
            joined = ", ".join(dict.fromkeys(subjects))
            if kind == "data":
                out.setdefault(kind, []).append("- data: %s names %s" % (path, joined))
            else:
                out.setdefault(kind, []).append("- %s: %s %s names %s" % (kind, path, text, joined))
    lines = [l for k in KIND_ORDER for l in out.get(k, ())]
    tail = "".join("; %s: unknown (%s)" % (k, rep.segments[k]) for k in ("quarantine", "slow", "presence", "names")
                   if k in rep.segments)
    base = "base %s %s (%s)" % (rep.ref, rep.sha[:8], METHOD)
    if rep.grep_fail:
        head = "readers: unknown -- %s; %d lines below -- %s" % (rep.grep_fail, len(lines), base)
    else:
        head = "readers: %d outside owns, %d lines below -- %s" % (len(outside_readers), len(lines), base)
    return "\n".join([head + tail] + lines) + "\n"


# --- CLI -----------------------------------------------------------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="owns_readers.py", description=__doc__.splitlines()[0])
    ap.add_argument("--paths", nargs="*", default=[])
    ap.add_argument("--given", nargs="*", default=[])
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--repo")
    ap.add_argument("--readers", action="store_true")
    ap.add_argument("--all", dest="all_", action="store_true")
    return ap


def main(argv=None) -> int:
    streams.utf8_stdio()
    args = _parser().parse_args(argv)
    if not any(p.strip() for p in args.paths):
        print("OWNS_READERS REFUSED: no path given -- pass --paths <owned path>...", file=sys.stderr)
        return 2
    try:
        text = render(report(args.paths, args.given, args.names, args.base, args.repo), args.readers, args.all_)
    except Exception as exc:  # noqa: BLE001
        text = "readers: unknown -- %s: %s\n" % (type(exc).__name__, _first_line(str(exc)))
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
