"""test_quarantine.py -- the quarantine of old package tests: what is in it, when it can go, and the guard that keeps it.

  python tools/test_quarantine.py enter --pipeline ID --coverage-pipeline ID [--dry-run] [--owner-word "<words, who, date>"]
  python tools/test_quarantine.py enter --phase2 FILE --replaced-by KEEP_ROW --pipeline ID [--dry-run]
  python tools/test_quarantine.py enter --rebase-entry COHORT NEW_SHA
  python tools/test_quarantine.py check            (K5: the commits since test-layers.json appeared)
  python tools/test_quarantine.py status           (R1-R6 per cohort, the observations, the verdicts)
  python tools/test_quarantine.py judge FILE --pipeline ID --verdict stale|real_catch|flaky --by TIER --reason TEXT
  python tools/test_quarantine.py land FILE --pipeline ID --commit SHA
  python tools/test_quarantine.py drop-keep FILE --reason TEXT
  python tools/test_quarantine.py split-keep OLD --into P1,P2[,...] [--shim [--importers A,B]] --reason TEXT
  python tools/test_quarantine.py pull [--pipeline ID]       (read the watch pipelines from CI into watch.jsonl)
  python tools/test_quarantine.py ci-summary --from GLOB [--out FILE]   (the CI job that merges the watch shards)
  python tools/test_quarantine.py purge --cohort ID --owner-word "<who, date>" [--dry-run] [--registries-done]

Spec docs/tasks/specs/td-15-scenarios-quarantine.md (sections C, D). The package file scripts/tests/test-layers.json is read ONLY
through selftest.test_layers() (AR-13); this tool writes its quarantine, cohorts and enforce_listing sections (one writer, AR-14).
The code reads and joins DATA (files, sha, versions, names); whether a red is a real catch is a role's verdict (judge), never a
guess here (AR-29). Exit codes: 0 ok, 1 refused or unknown, 2 call error / not implemented, 3 (pull) the watch is silent."""

import argparse
import ast
import glob
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
ROOT = _TOOLS.parent
PKG = "ai-packages/qa-factory"
TESTS_REL = PKG + "/scripts/tests"
LAYERS_REL = TESTS_REL + "/test-layers.json"
PLUGIN_REL = PKG + "/.claude-plugin/plugin.json"
SLOW_REL = PKG + "/scripts/slow_tests.json"
STATE_REL = "plans/test-quarantine"
CONFIG_REL, WATCH_REL, VERDICTS_REL = (STATE_REL + "/" + n for n in ("config.json", "watch.jsonl", "verdicts.jsonl"))
MIN_STORIES = 3
BASELINE_RUNS = 3
FORGE_CARRIERS = ("plans/builder-rules.md", ".gitlab-ci.yml", "docs/SIBLING_MAP.md", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md")
PACKAGE_PROSE = (PKG + "/design/architecture.md", PKG + "/design/factory-rules.md")
SELFTEST_JOB, SELFTEST_ART = "package-full-report", "ci-out/selftest.txt"
# .gitlab-ci.yml, job package-full (parallel: 2): jobs "package-full 1/2", "package-full 2/2", each keeps ci-out/selftest-shard-<i>-of-2.txt
SELFTEST_SHARDS, SELFTEST_SHARD_JOB, SELFTEST_SHARD_ART = 2, "package-full %d/2", "ci-out/selftest-shard-%d-of-2.txt"
COVERAGE_JOB, COVERAGE_ART = "test-redundancy", "ci-out/redundancy/test-redundancy.md"
PULL_DOOR = "run: python tools/test_quarantine.py pull"
VERDICTS = ("stale", "real_catch", "flaky")
CI_DOOR = "rerun when CI is reachable: python tools/ci_read.py jobs %s"


class Refusal(Exception):
    """The one-sentence refusal main() prints (what is wrong, what is expected, a door)."""


class Unknown(Refusal):
    """Something could not be established: never a pass (FR-59, AR-28)."""


CI_HOSTS = ("github", "gitlab")          # the values of "ci" in plans/test-quarantine/config.json; ci_reader() picks the reader


class CIError(Exception):
    def __init__(self, kind, text=""):
        super().__init__(text or kind)
        self.kind = kind          # unreachable | token_refused | missing


# --- plumbing ------------------------------------------------------------------------------------------------------

def _say(text=""):
    sys.stdout.write(str(text).encode("ascii", "replace").decode("ascii") + "\n")


_MODS: dict = {}


def _pkg_module(root, name):
    """A module of the package scripts/ loaded by path (the tool lives outside the package; AR-4: no host layout assumed)."""
    scripts = (Path(root) / PKG / "scripts").resolve()
    key = (str(scripts), name)
    if key not in _MODS:
        path = scripts / (name + ".py")
        if not path.is_file():
            raise Refusal(f"{PKG}/scripts/{name}.py is missing -- run from a checkout that holds {PKG}, or pass --root <checkout>")
        unique = "_tq_%s_%d" % (re.sub(r"\W", "_", name), len(_MODS))
        spec = importlib.util.spec_from_file_location(unique, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[unique] = mod
        added = str(scripts) not in sys.path
        if added:
            sys.path.insert(0, str(scripts))
        try:
            spec.loader.exec_module(mod)
        finally:
            if added:
                sys.path.remove(str(scripts))
        _MODS[key] = mod
    return _MODS[key]


def _selftest(root):
    return _pkg_module(root, "selftest")


def _git(root, *args):
    try:
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return 128, ""
    return p.returncode, p.stdout


def _head(root):
    rc, out = _git(root, "rev-parse", "HEAD")
    if rc or not out.strip():
        raise Unknown("git HEAD is unreadable here; expected a git checkout")
    return out.strip()


def _layers(root):
    st = _selftest(root)
    try:
        return st.test_layers(Path(root) / LAYERS_REL)
    except st.TestLayersError as exc:
        raise Refusal(str(exc)) from None


def _config(root):
    path = Path(root) / CONFIG_REL
    try:
        cfg = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        raise Unknown("plans/test-quarantine/config.json is missing -- write plans/test-quarantine/config.json "
                      "(spec td-15 section D.1)") from None
    except (OSError, ValueError):
        raise Unknown("plans/test-quarantine/config.json cannot be read as JSON -- fix plans/test-quarantine/config.json") from None
    if not isinstance(cfg, dict) or not isinstance(cfg.get("branch"), str) or not cfg["branch"]:
        raise Unknown("plans/test-quarantine/config.json names no branch -- write plans/test-quarantine/config.json")
    cfg.setdefault("max_gap_days", 4)
    if cfg.setdefault("ci", "gitlab") not in CI_HOSTS:
        raise Unknown("plans/test-quarantine/config.json names ci %r, and this tool reads %s only -- set \"ci\": \"github\" "
                      "or \"ci\": \"gitlab\", or extend the tool (spec td-15 section E2)" % (str(cfg["ci"])[:20], " and ".join(CI_HOSTS)))
    return cfg


def _jsonl(root, rel):
    path = Path(root) / rel
    if not path.is_file():
        return []
    rows = []
    try:
        for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if line.strip():
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("not an object")
                rows.append(row)
    except (OSError, ValueError):
        raise Unknown(f"{rel} line {n} cannot be read; expected one JSON object per line") from None
    return rows


def _append(root, rel, row):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, sort_keys=False) + "\n")


def _day(text):
    try:
        return date.fromisoformat(str(text)[:10])
    except ValueError:
        raise Unknown(f"the date {str(text)[:20]!r} is not YYYY-MM-DD") from None


def _version(root, text):
    """Version tuple of a strict N.N.N; a suffix or junk is UNKNOWN, never a pass (FR-59)."""
    ip = _pkg_module(root, "install_paths")
    if isinstance(text, str) and re.fullmatch(r"\d+(\.\d+)*", text.strip()):
        return ip._vtuple(text)
    raise Unknown(f"the version {str(text)[:30]!r} is not N.N.N")


def _vless(root, a, b):
    return _pkg_module(root, "install_paths")._vless(a, b)


def _write_layers(root, mutate):
    path = Path(root) / LAYERS_REL
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    mutate(raw)
    path.write_text(json.dumps(raw, indent=1) + "\n", encoding="utf-8", newline="\n")


def _blob_sections(root, rev):
    """The sections of test-layers.json at a revision (history is judged on blobs, not on the live file)."""
    rc, txt = _git(root, "show", f"{rev}:{LAYERS_REL}")
    if rc:
        return {"keep": {}, "quarantine": {}, "pin_holds": {}, "cohorts": {}}
    try:
        raw = json.loads(txt.lstrip("﻿"))
        return {k: dict(raw.get(k) or {}) for k in ("keep", "quarantine", "pin_holds", "cohorts")}
    except (ValueError, AttributeError, TypeError):
        raise Unknown(f"test-layers.json at {rev[:8]} cannot be read as JSON") from None


# --- the data functions ---------------------------------------------------------------------------------------------

def forge_texts(root):
    """The forge's carriers of test names, as texts for selftest.gate_named_files (the package does not read docs/, AR-4)."""
    out = []
    for rel in FORGE_CARRIERS:
        p = Path(root) / rel
        if p.is_file():
            out.append(p.read_text(encoding="utf-8", errors="replace"))
    return out


def _imports(text):
    names = set()
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def _import_pairs(read, kept, quarantined):
    """(kept file, quarantined file) pairs: a kept test imports a quarantined test module. `read(name)` gives the text."""
    pairs = []
    for name in sorted(kept):
        text = read(name)
        if text is None:
            continue
        pairs += [(name, m + ".py") for m in sorted(_imports(text)) if m + ".py" in quarantined]
    return pairs


def _read_test(root):
    def read(name):
        p = Path(root) / TESTS_REL / name
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None
    return read


def held_by_import(root):
    """[(kept file, quarantined file)]: the kept test that would lose an import (R6; TD-15.8 cuts these)."""
    layers = _layers(root)
    return _import_pairs(_read_test(root), _importers(layers), layers["quarantine"])


def signature(file_result):
    """A red's signature: the sorted FAIL names (the `+N more` marker included); a red with none -> crash:<type>."""
    status = file_result.get("status")
    if status in ("timeout", "ran_nothing", "missing"):
        return (status,)
    if status == "green":
        return ()
    fails = [str(f) for f in file_result.get("fails") or []]
    if fails:
        return tuple(sorted(fails))
    m = re.match(r"[A-Za-z_][\w.]*", str(file_result.get("crash") or ""))
    return ("crash:" + (m.group(0) if m else "unknown"),)


def _sha_of(watch, pipeline):
    for run in watch:
        if run.get("pipeline") == pipeline:
            return run.get("sha")
    return None


def _has_green(watch, name, sha):
    return bool(sha) and any(r.get("sha") == sha and (r.get("files") or {}).get(name, {}).get("status") == "green" for r in watch)


def covered(observation, verdicts, watch):
    """Is the observation (file, signature, pipeline) covered by a verdict? Names subset of the verdict's names; `flaky`
    only when the file also has a green result on the observation's sha. A new name is never covered."""
    names = set(observation["signature"])
    for v in verdicts:
        if v.get("file") != observation["file"] or not names <= set(v.get("signature") or []):
            continue
        if v.get("verdict") in ("stale", "real_catch"):
            return True
        if v.get("verdict") == "flaky" and _has_green(watch, observation["file"], _sha_of(watch, observation["pipeline"])):
            return True
    return False


def releases(root, cohort):
    """Distinct package versions on the first-parent history of HEAD after the cohort's commit_at_entry, each strictly
    above the entry version and every earlier one (a rollback or a repeat is no release). Unreadable -> Unknown."""
    row = cohort if isinstance(cohort, dict) else _layers(root)["cohorts"][cohort]
    best = _version(root, row.get("release_at_entry"))
    rc, out = _git(root, "log", "--first-parent", "--reverse", "--format=%H", f"{row.get('commit_at_entry')}..HEAD", "--", PLUGIN_REL)
    if rc:
        raise Unknown("the branch history after the cohort's commit_at_entry cannot be read -- fetch it or use enter --rebase-entry")
    found = []
    for sha in out.split():
        rc, txt = _git(root, "show", f"{sha}:{PLUGIN_REL}")
        try:
            ver = json.loads(txt.lstrip("﻿"))["version"] if not rc else None
        except (ValueError, KeyError, TypeError):
            ver = None
        tup = _version(root, ver)
        if _vless(root, best, tup):
            found.append(ver)
            best = tup
    return found


def _is_after(root, commit, sha, cache={}):
    if not isinstance(sha, str) or not sha:
        return False
    key = (str(root), commit, sha)
    if key not in cache:
        rc, _ = _git(root, "merge-base", "--is-ancestor", str(commit), sha)
        if rc not in (0, 1):
            raise Unknown(f"the run sha {sha[:8]} is not in this clone -- git fetch, then retry")
        cache[key] = rc == 0
    return cache[key]


def _watch_rows(root):
    rows = _jsonl(root, WATCH_REL)
    seen, runs = set(), []
    for r in rows:
        key = (r.get("pipeline"), r.get("retry") or 0)         # a re-read after Retry carries "retry": N (pull --pipeline)
        if r.get("kind") == "run" and key not in seen:
            seen.add(key)
            runs.append(r)
    pulls = [r for r in rows if r.get("kind") == "pull"]
    return runs, pulls


def _verdict_rows(root):
    rows = _jsonl(root, VERDICTS_REL)
    verdicts = [r for r in rows if r.get("verdict") in VERDICTS]
    lands = [r for r in rows if r.get("kind") == "land"]
    return verdicts, lands


def _key(v):
    return (v.get("file"), tuple(v.get("signature") or ()), v.get("pipeline"))


def _effective(verdicts):
    """(verdicts after --supersede chains and duplicates, keys that still disagree)."""
    per: dict = {}
    for v in verdicts:
        lst = per.setdefault(_key(v), [])
        if v.get("supersede"):
            lst[:] = []
        lst.append(v)
    out, conflicts = [], []
    for k, lst in per.items():
        words = {v["verdict"] for v in lst}
        out += [next(v for v in lst if v["verdict"] == w) for w in sorted(words)]
        if len(words) > 1:
            conflicts.append(k)
    return out, conflicts


def _observations(files, runs):
    """Every red observation, one per (file, signature, pipeline): a verdict covers only the observations covered() lets it cover."""
    seen: dict = {}
    for run in runs:
        for name in files:
            rec = (run.get("files") or {}).get(name)
            if not isinstance(rec, dict) or rec.get("status") in (None, "green", "not_run"):
                continue
            seen.setdefault((name, signature(rec), run.get("pipeline")), {"file": name, "signature": signature(rec), "pipeline": run.get("pipeline")})
    return list(seen.values())


def _importers(layers):
    """The files whose imports R6, held-by-import and the K5 edge check guard: keep rows and pin-held files (both run in the canon)."""
    return set(layers["keep"]) | set(layers["pin_holds"])


def _rule_rows(root, cid, layers, runs, verdicts, lands):
    row = layers["cohorts"][cid]
    files = sorted(n for n, r in layers["quarantine"].items() if r.get("cohort") == cid)
    rels = releases(root, row)
    complete = [r for r in runs if r.get("complete") is True and _is_after(root, row.get("commit_at_entry"), r.get("sha"))]
    obs = _observations(files, complete)
    eff, conflicts = _effective(verdicts)
    unexamined = [o for o in obs if not covered(o, eff, runs)]
    catches = [v for v in eff if v["verdict"] == "real_catch" and v.get("file") in files]
    unlanded = [v for v in catches if not any(l.get("file") == v["file"] and l.get("pipeline") == v.get("pipeline") for l in lands)]
    held = [p for p in _import_pairs(_read_test(root), _importers(layers), layers["quarantine"]) if p[1] in files]
    qualifying = None
    if len(rels) >= 2:
        r2 = _version(root, rels[1])
        for run in complete:
            if not any(n in (run.get("files") or {}) for n in files):
                continue
            try:
                if not _vless(root, _version(root, run.get("package_version")), r2):
                    qualifying = run
                    break
            except Unknown:
                continue
    rules = [
        ("R1", bool(files), f"{len(files)} files in the cohort"),
        ("R2", qualifying is not None, f"releases since entry {len(rels)} of 2" + (
            f"; complete watch on {qualifying['package_version']}" if qualifying else "; no complete watch run on the 2nd release yet")),
        ("R3", not unexamined, f"{len(unexamined)} unexamined of {len(obs)} observations"),
        ("R4", not conflicts, f"{len(conflicts)} conflicting verdict keys"),
        ("R5", not unlanded, f"{len(unlanded)} real catches without land"),
        ("R6", not held, f"{len(held)} kept files import this cohort's files"),
    ]
    blind = 0
    for name in files:
        mine = [o for o in obs if o["file"] == name]
        stale = [v for v in eff if v["verdict"] == "stale" and v.get("file") == name]
        if not mine or not all(any(set(o["signature"]) <= set(v.get("signature") or ()) for v in stale) for o in mine):
            continue
        order = [r.get("pipeline") for r in runs]
        last = max((order.index(v.get("pipeline")) for v in stale if v.get("pipeline") in order), default=-1)
        if not any(r.get("files", {}).get(name, {}).get("status") == "green" for r in runs[last + 1:]):
            blind += 1
    counts = {w: len([v for v in eff if v["verdict"] == w and v.get("file") in files]) for w in VERDICTS}
    return {"id": cid, "entered": row.get("entered"), "release_at_entry": row.get("release_at_entry"), "files": files, "rules": rules,
            "ready": all(ok for _, ok, _ in rules), "releases": rels, "observations": obs, "unexamined": unexamined,
            "red": len(obs), "blind": blind, "counts": counts, "conflicts": conflicts, "unlanded": unlanded, "held": held,
            "qualifying": qualifying["package_version"] if qualifying else None}


def status_data(root, today=None):
    """Everything `status` and the session line print, from local files only (no network)."""
    root, today = Path(root), today or date.today()
    out = {"no_quarantine": False, "unknown": None, "cohorts": [], "alerts": [], "complete_runs": 0, "runs": [], "pulls": [],
           "head_version": None, "branch": None, "max_gap_days": 4}
    if not (root / LAYERS_REL).is_file():                  # no test-layers.json: no quarantine, and no package needed to say so (D.5)
        out["no_quarantine"] = True
        return out
    try:
        layers = _layers(root)
    except Refusal as exc:
        out["unknown"] = str(exc)
        return out
    if layers["absent"] or not layers["quarantine"]:
        out["no_quarantine"] = True
        return out
    try:
        cfg = _config(root)
        runs, pulls = _watch_rows(root)
        verdicts, lands = _verdict_rows(root)
        out.update(runs=runs, pulls=pulls, branch=cfg["branch"], max_gap_days=cfg["max_gap_days"])
        try:
            out["head_version"] = _pkg_module(root, "install_paths").plugin_version(Path(root) / PKG)
        except ValueError:
            out["head_version"] = None
        for cid in sorted(layers["cohorts"]):
            try:
                out["cohorts"].append(_rule_rows(root, cid, layers, runs, verdicts, lands))
            except Refusal as exc:
                out["cohorts"].append({"id": cid, "unknown": str(exc), "ready": False})
        out["alerts"] = _alerts(layers, runs, pulls, verdicts, lands, cfg, today)
    except Refusal as exc:
        out["unknown"] = str(exc)
    return out


def _alerts(layers, runs, pulls, verdicts, lands, cfg, today):
    out, limit = [], 2 * int(cfg["max_gap_days"])
    ok_pulls = [p for p in pulls if p.get("ci") == "ok"]
    entries = [_day(c.get("entered")) for c in layers["cohorts"].values() if c.get("entered")]
    cannot = ("TEST QUARANTINE ALERT: the watch cannot be confirmed on CI (%s) -- tell the owner: the pull cannot reach CI, or the schedule on "
              "%s is missing or failing; try python tools/test_quarantine.py pull (docs/RUNBOOK.md section 7)")
    if ok_pulls and entries:
        last = ok_pulls[-1]
        as_of = _day(last.get("at"))
        newest = last.get("newest_watch_at")
        gap = (as_of - _day(newest)).days if newest else (as_of - min(entries)).days
        if gap > limit:
            out.append("TEST QUARANTINE ALERT: the watch has not run on CI for %d d (last %s, as of pull %s) -- tell the owner: "
                       "the schedule on %s is missing or failing (docs/RUNBOOK.md section 7)"
                       % (gap, _day(newest) if newest else "never", as_of, cfg["branch"]))
        elif (today - as_of).days > limit:                 # later failed pulls do not refresh what the last good one knew
            out.append(cannot % ("last successful pull %s, %d d ago" % (as_of, (today - as_of).days), cfg["branch"]))
    elif entries and (today - min(entries)).days > limit:  # no pull yet, or none that reached CI (refused, unreachable)
        out.append(cannot % ("no successful pull since the entry on %s, %d d ago; %d pull(s) recorded"
                             % (min(entries), (today - min(entries)).days, len(pulls)), cfg["branch"]))
    eff, _ = _effective(verdicts)
    for v in eff:
        if v["verdict"] == "real_catch" and not any(l.get("file") == v.get("file") and l.get("pipeline") == v.get("pipeline") for l in lands):
            out.append("TEST QUARANTINE ALERT: real catch %s -- %s: %s (finding %s); its case is owed as a scenario/table row -- tell the owner"
                       % (str(v.get("ts"))[:10], v.get("file"), str(v.get("reason"))[:100], v.get("finding")))
    return out


def _cohort_line(c, d, today):
    pulls, runs = d["pulls"], d["runs"]
    if c.get("unknown"):
        return "TEST QUARANTINE: status unknown (%s)" % c["unknown"][:150]
    if c["ready"]:
        return ("TEST QUARANTINE: READY TO DELETE cohort %s -- %d files since %s; complete watch on %s (2nd release since %s); "
                "every red examined (%d stale, %d flaky, %d real catch moved); blind %d. Tell the owner; on her word: "
                'python tools/test_quarantine.py purge --cohort %s --owner-word "<who, date>"'
                % (c["id"], len(c["files"]), c["entered"], c["qualifying"], c["release_at_entry"], c["counts"]["stale"],
                   c["counts"]["flaky"], c["counts"]["real_catch"], c["blind"], c["id"]))
    n = len(c["releases"])
    rel = "releases since: %d of 2" % min(n, 2) + (" (%s)" % ", ".join(c["releases"][:2]) if n else "")
    dates = [_day(r.get("created_at")) for r in runs if r.get("created_at")]
    watch = ("watch ran %s (%d d ago)" % (max(dates), (today - max(dates)).days) if dates
             else "no watch run yet (entered %d d ago)" % (today - _day(c["entered"])).days)
    pulled = "never pulled"
    stale = True
    if pulls:
        pd = _day(pulls[-1].get("at"))
        pulled = "pulled %s (%d d ago)" % (pd, (today - pd).days)
        stale = (today - pd).days > int(d["max_gap_days"])
    if stale:
        pulled += " -- " + PULL_DOOR
    line = ("TEST QUARANTINE: %d files since %s (cohort %s, entered at %s); %s; %s, %s; %d red, %d unexamined, blind %d -- delete when: "
            "complete watch on the 2nd release + 0 unexamined + every catch moved"
            % (len(c["files"]), c["entered"], c["id"], c["release_at_entry"], rel, watch, pulled, c["red"], len(c["unexamined"]), c["blind"]))
    if pulls and pulls[-1].get("ci") not in (None, "ok"):
        line += "; last pull %s could not reach CI (%s)" % (_day(pulls[-1].get("at")), pulls[-1]["ci"])
    if len(runs) >= 3 and all(r.get("complete") is not True for r in runs[-3:]):
        line += "; last 3 watch runs incomplete (not_run files) -- see the quarantine-watch job"
    done = [_tuple_or_none(r.get("package_version")) for r in runs if r.get("complete") is True]
    done = [t for t in done if t]
    head = d.get("head_version")
    if head and done and _newer(head, max(done)):
        line += "; release %s has no complete watch run yet -- start it: web pipeline with QUARANTINE_WATCH=1 on %s" % (head, d["branch"])
    return line


def _tuple_or_none(text):
    return tuple(int(p) for p in text.split(".")) if isinstance(text, str) and re.fullmatch(r"\d+(\.\d+)*", text) else None


def _newer(head, tup):
    h = _tuple_or_none(head)
    if h is None:
        return False
    w = max(len(h), len(tup))
    return h + (0,) * (w - len(h)) > tup + (0,) * (w - len(tup))


def status_line(root, today=None):
    """The session-start lines (spec D.5 (1)): ALERTs first, then one line per cohort. No file or an empty quarantine: none."""
    d = status_data(root, today)
    if d["no_quarantine"]:
        return []
    if d["unknown"]:
        return ["TEST QUARANTINE: status unknown (%s)" % d["unknown"][:150]]
    return d["alerts"] + [_cohort_line(c, d, today or date.today()) for c in d["cohorts"]]


# --- enter / drop-keep ---------------------------------------------------------------------------------------------

class GitlabCI:
    """The reader of CI used by enter: ci_read's request, no other network code. Tests pass their own object."""

    def __init__(self, token=None):
        import ci_read
        self._ci = ci_read
        if token is None:
            try:
                name, _ = ci_read.token_env_name()
            except ci_read.TokenEnvRefusal as exc:
                raise CIError("token_refused", str(exc)) from None
            token = os.environ.get(name)
        if not token:
            raise CIError("token_refused", "the GitLab token variable is not set")
        self.token = token

    def _get(self, path):
        try:
            return self._ci.request(self._ci._api(path), self.token)
        except urllib.error.HTTPError as exc:
            raise CIError({401: "token_refused", 403: "token_refused", 404: "missing"}.get(exc.code, "unreachable"), f"HTTP {exc.code}") from None
        except (urllib.error.URLError, OSError, ValueError):
            raise CIError("unreachable") from None

    def pipeline_sha(self, pid):
        return str(json.loads(self._get(f"/pipelines/{pid}")).get("sha") or "")

    def artifact(self, pid, job, path):
        for j in json.loads(self._get(f"/pipelines/{pid}/jobs?per_page=100")):
            if j.get("name") == job:
                return self._get("/jobs/%s/artifacts/%s" % (j["id"], urllib.parse.quote(path, safe="/")))
        raise CIError("missing", f"no job {job} in pipeline {pid}")

    def pipeline_variables(self, pid):
        """{key: value} of the variables the pipeline was started with (GET /pipelines/:id/variables; needs a token that may read them)."""
        rows = json.loads(self._get(f"/pipelines/{pid}/variables"))
        return {str(r["key"]): str(r.get("value")) for r in rows}

    def recent_pipelines(self, branch, n=20):
        rows = json.loads(self._get("/pipelines?ref=%s&per_page=%d" % (urllib.parse.quote(branch, safe=""), n)))
        return [r["id"] for r in rows]


class GithubCI(GitlabCI):
    """The reader of CI on GitHub (FG7-10). It answers the SAME paths `GitlabCI._get` answers, in the same shapes, so the readers
    above it (pull, _ci_pipelines, _schedules, enter) stay one code path for both hosts: a pipeline is a workflow run, its jobs are
    the run's jobs, a job's artifact file is the member of the run's artifact named like the job. The network code is ci_read's
    (`_open`, the repository of `origin`, the token variable of tools/dev.config.yaml); nothing else is opened here.
    What GitHub does not have is said, not guessed: a schedule has no variables, the watch is a workflow of its own
    (quarantine-watch.yml), so a run of THAT workflow is what `QUARANTINE_WATCH=1` was, and the schedule is active when the
    workflow is active on GitHub and its file here carries a cron. An unknown path is `missing`."""

    WATCH_WORKFLOW = "quarantine-watch.yml"
    EVENTS = {"schedule": "schedule", "workflow_dispatch": "web", "repository_dispatch": "api", "push": "push"}

    def __init__(self, token=None, root=None):
        import ci_read
        self._ci = ci_read
        self.root = Path(ROOT if root is None else root)
        try:
            door = os.environ.get(ci_read.REPO_DOOR, "")
            repo = ci_read._repo_name(door) if door else ci_read._origin_repo_path(ci_read.split_origin(ci_read.origin_url(self.root))[1])
            if token is None:
                name, _ = ci_read.github_backend(repo or "", self.root).token_env_name()
                token = os.environ.get(name)
        except ci_read.common.Refusal as exc:
            raise CIError("token_refused", str(exc)) from None
        if not repo:
            raise CIError("unreachable", "origin does not name a GitHub repository (owner/repo)")
        if not token:
            raise CIError("token_refused", "the GitHub token variable is not set")
        self.token = token
        self._base = "%s/repos/%s" % (ci_read.API, repo)
        self._workflow_of = {}                 # run id -> the path of its workflow file, as the lists and the run say it

    def _raw(self, path):
        try:
            return self._ci._open(self._base + path, self.token, limit=self._ci.MAX_ARTIFACT_BYTES)[1]
        except urllib.error.HTTPError as exc:
            raise CIError({401: "token_refused", 403: "token_refused", 404: "missing"}.get(exc.code, "unreachable"), f"HTTP {exc.code}") from None
        except (urllib.error.URLError, OSError, ValueError):
            raise CIError("unreachable") from None

    def _json(self, path):
        try:
            return json.loads(self._raw(path).decode("utf-8", errors="replace"))
        except ValueError:
            raise CIError("unreachable", "the answer is not JSON") from None

    def _pipeline(self, run):
        """A workflow run in the shape of a pipeline row: id, sha, source, created_at."""
        self._workflow_of[str(run.get("id"))] = str(run.get("path") or "")
        return {"id": run.get("id"), "sha": run.get("head_sha"), "source": self.EVENTS.get(run.get("event"), run.get("event")),
                "created_at": run.get("created_at"), "ref": run.get("head_branch")}

    def _is_watch(self, pid):
        if str(pid) not in self._workflow_of:
            self._pipeline(self._json("/actions/runs/%s" % pid))
        return self._workflow_of[str(pid)].endswith("/" + self.WATCH_WORKFLOW)

    def _cron_here(self):
        try:
            text = (self.root / ".github" / "workflows" / self.WATCH_WORKFLOW).read_text(encoding="utf-8")
        except OSError:
            return False
        return bool(re.search(r"^\s*schedule:\s*\n\s*-\s*cron:", text, re.M))

    def _get(self, path):
        """The GitLab path, answered from GitHub as the JSON text GitLab would give."""
        head, _, query = path.partition("?")
        args = urllib.parse.parse_qs(query)
        one = re.fullmatch(r"/pipelines/(\d+)(/jobs|/variables)?", head)
        if head == "/pipelines":
            runs = self._json("/actions/runs?branch=%s&per_page=%s&page=%s" % (
                urllib.parse.quote(args.get("ref", [""])[0], safe=""), args.get("per_page", ["20"])[0], args.get("page", ["1"])[0]))
            return json.dumps([self._pipeline(r) for r in runs.get("workflow_runs") or []])
        if one and one.group(2) is None:
            return json.dumps(self._pipeline(self._json("/actions/runs/%s" % one.group(1))))
        if one and one.group(2) == "/variables":
            return json.dumps([{"key": WATCH_VARIABLE, "value": "1"}] if self._is_watch(one.group(1)) else [])
        if one:                                 # /jobs: only a watch run can carry the watch jobs -- no request for the others
            if not self._is_watch(one.group(1)):
                return "[]"
            jobs = self._json("/actions/runs/%s/jobs?per_page=100" % one.group(1)).get("jobs") or []
            return json.dumps([{"id": j.get("id"), "name": j.get("name")} for j in jobs])
        if head == "/pipeline_schedules":
            flow = self._json("/actions/workflows/%s" % self.WATCH_WORKFLOW)
            if flow.get("state") != "active" or not self._cron_here():
                return "[]"
            return json.dumps([{"id": self.WATCH_WORKFLOW, "active": True, "ref": self._json("").get("default_branch")}])
        if head == "/pipeline_schedules/%s" % self.WATCH_WORKFLOW:
            return json.dumps({"variables": [{"key": WATCH_VARIABLE, "value": "1"}]})
        raise CIError("missing", "no GitHub form of %s" % head[:60])

    def artifact(self, pid, job, path):
        """The file `path` a job kept: the member of the run's artifact named like the job (the whole path, else its file name)."""
        rows = self._json("/actions/runs/%s/artifacts?per_page=100" % pid).get("artifacts") or []
        found = [r for r in rows if r.get("name") == job and not r.get("expired")]
        if not found:
            raise CIError("missing", f"no artifact {job} in run {pid}")
        raw = self._raw("/actions/artifacts/%s/zip" % urllib.parse.quote(str(found[0].get("id")), safe=""))
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                names = archive.namelist()
                member = path if path in names else path.rsplit("/", 1)[-1]
                if member not in names:
                    raise CIError("missing", f"{path} is not in the artifact {job} of run {pid}")
                return archive.read(member).decode("utf-8", errors="replace")
        except zipfile.BadZipFile:
            raise CIError("missing", f"the artifact {job} of run {pid} is not a readable zip") from None


def ci_reader(root=None):
    """The CI reader the config names ("ci": github | gitlab). The one place that picks the host."""
    root = Path(ROOT if root is None else root)
    return GithubCI(root=root) if _config(root).get("ci") == "github" else GitlabCI()


# --- the watch: pull, ci-summary, the schedule and pipeline readers --------------------------------------------------

WATCH_JOB, WATCH_REPORT_JOB, WATCH_ART = "quarantine-watch", "quarantine-watch-report", "ci-out/quarantine-watch.json"
WATCH_SOURCES = ("schedule", "web", "api", "push")
WATCH_VARIABLE = "QUARANTINE_WATCH"
_FAILS_MARKER = re.compile(r"^\+(\d+) more$")


def _ts(text):
    """An ISO time from CI as an aware datetime, or None."""
    try:
        t = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def _plain_ref(ref):
    ref = str(ref or "")
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def _schedules(branch, ci=None):
    """GET /projects/:id/pipeline_schedules (through ci_read.request). "ok": an active schedule on `branch` carries
    QUARANTINE_WATCH=1; "missing": none does (no schedule, or one without the variable); "unknown": CI could not be read."""
    try:
        ci = ci_reader() if ci is None else ci
        for row in json.loads(ci._get("/pipeline_schedules?scope=active&per_page=100")):
            if row.get("active") is False or _plain_ref(row.get("ref")) != branch:
                continue
            detail = json.loads(ci._get("/pipeline_schedules/%s" % row["id"]))
            if any(v.get("key") == WATCH_VARIABLE and str(v.get("value")) == "1" for v in detail.get("variables") or []):
                return "ok"
        return "missing"
    except (CIError, ValueError, TypeError, KeyError, AttributeError):
        return "unknown"


PIPELINE_PAGES = 10          # pages of 50 read per call: the cap, stated in the text when it is hit
PIPELINE_PER_PAGE = 50


def _ci_pipelines(branch, sources, ci=None, after=None, capped=None):
    """Pipelines of `branch` from any of `sources` that carry the job quarantine-watch-report, created after the time `after`
    (None: all that the pages hold), oldest first: [{"id", "source", "created_at", "sha"}]. CI lists pipelines newest first, so the read
    is COMPLETE (no cap line) when it reaches an empty page, a page shorter than PIPELINE_PER_PAGE (the end of the list), or a page whose
    oldest row is at or below the floor `after` (everything newer was on the pages already read). Only PIPELINE_PAGES FULL pages that
    never reached the floor are a cut: a line naming it is appended to the list `capped` (if given); the page after the tenth is not
    read, so a list of exactly ten full pages is reported cut, never complete on an unknown. CI errors propagate."""
    ci = ci_reader() if ci is None else ci
    floor = _ts(after) if after else None
    found, ref, list_ended = [], urllib.parse.quote(branch, safe=""), False
    for page in range(1, PIPELINE_PAGES + 1):
        rows = json.loads(ci._get("/pipelines?ref=%s&per_page=%d%s" % (ref, PIPELINE_PER_PAGE, "" if page == 1 else "&page=%d" % page)))
        times = [_ts(r.get("created_at")) for r in rows]
        for r, made in zip(rows, times):
            if r.get("source") not in sources or (floor and made and made <= floor):
                continue
            if any(j.get("name") == WATCH_REPORT_JOB for j in json.loads(ci._get("/pipelines/%s/jobs?per_page=100" % r["id"]))):
                found.append({"id": r["id"], "source": r.get("source"), "created_at": r.get("created_at"), "sha": r.get("sha")})
        dated = [t for t in times if t]
        if len(rows) < PIPELINE_PER_PAGE or (floor and dated and min(dated) <= floor):
            list_ended = True
            break
    if not list_ended and capped is not None:
        capped.append("the pipeline list of %s was cut at %d pages of %d (%d pipelines); older watch pipelines may be missing -- read each "
                      "with: python tools/test_quarantine.py pull --pipeline <id>" % (branch, PIPELINE_PAGES, PIPELINE_PER_PAGE,
                                                                                      PIPELINE_PAGES * PIPELINE_PER_PAGE))
    return sorted(found, key=lambda p: _ts(p["created_at"]) or datetime.min.replace(tzinfo=timezone.utc))


def _newest(items):
    """(id, created_at) of the newest of [(id, created_at)], or (None, None)."""
    dated = [(i, c) for i, c in items if _ts(c)]
    return max(dated, key=lambda x: _ts(x[1])) if dated else (None, None)


def _watch_run_row(ci, p):
    """(run row, None) of one watch pipeline read from its report artifact, or (None, the line to print) when it cannot be used yet.
    CI errors other than a missing artifact propagate."""
    try:
        rec = json.loads(ci.artifact(p["id"], WATCH_REPORT_JOB, WATCH_ART))
        if not isinstance(rec, dict):
            raise ValueError("not an object")
    except CIError as exc:
        if exc.kind != "missing":
            raise
        return None, ("pipeline %s has no watch record yet (the job is not finished, or the artifact expired); retry: "
                      "python tools/test_quarantine.py pull --pipeline %s" % (p["id"], p["id"]))
    except ValueError:
        return None, "pipeline %s: the watch record cannot be read as JSON -- skipped" % p["id"]
    return {"kind": "run", "pipeline": p["id"], "source": p.get("source") or rec.get("source"),
            "created_at": p.get("created_at") or rec.get("created_at"), "sha": p.get("sha") or rec.get("sha"),
            "package_version": rec.get("package_version"), "complete": rec.get("complete") is True,
            "files": rec.get("files") if isinstance(rec.get("files"), dict) else {}}, None


def pull(root, ci=None, pipeline=None, today=None):
    """The pull of D.2: (exit code, lines to print). Appends run rows of the watch pipelines not recorded yet and ALWAYS one pull row
    (the pull time and the newest watch pipeline time are separate fields, so "the watch stopped" and "nobody pulled" differ)."""
    root = Path(root)
    cfg = _config(root)
    runs, _ = _watch_rows(root)
    known = {str(r.get("pipeline")) for r in runs}
    at = "%sT00:00:00" % today.isoformat() if today else datetime.now().isoformat(timespec="seconds")

    def pull_row(state, newest=(None, None)):
        _append(root, WATCH_REL, {"kind": "pull", "at": at, "ci": state, "newest_watch_pipeline": newest[0], "newest_watch_at": newest[1]})

    try:
        ci = ci_reader(root) if ci is None else ci
    except CIError as exc:
        pull_row(exc.kind)
        return 1, ["ci: %s" % exc.kind]
    lines, new, skipped, capped = [], 0, 0, []
    found, recorded = [], list(runs)           # `recorded`: the run rows that exist (the newest watch time comes from these only)
    try:
        if pipeline:
            info = json.loads(ci._get("/pipelines/%s" % pipeline))
            found = [{"id": info["id"], "source": info.get("source"), "created_at": info.get("created_at"), "sha": info.get("sha")}]
        else:
            last = _newest([(r.get("pipeline"), r.get("created_at")) for r in runs])[1]
            found = _ci_pipelines(cfg["branch"], WATCH_SOURCES, ci, after=last, capped=capped)
        for p in found:
            if str(p["id"]) in known and not pipeline:         # asked for by id, a recorded pipeline is re-read (the flaky door: Retry)
                skipped += 1
                lines.append("pipeline %s already recorded -- skipped" % p["id"])
                continue
            same = [r for r in recorded if str(r.get("pipeline")) == str(p["id"])]
            row, note = _watch_run_row(ci, p)
            if row is None:
                lines.append(note)
                continue
            if same:
                if any(r.get("files") == row["files"] and r.get("complete") == row["complete"] for r in same):
                    skipped += 1
                    lines.append("pipeline %s already recorded -- skipped (the record is unchanged)" % p["id"])
                    continue
                row["retry"] = len(same)
            _append(root, WATCH_REL, row)
            recorded.append(row)
            known.add(str(p["id"]))
            new += 1
    except (CIError, ValueError, KeyError, TypeError) as exc:
        state = exc.kind if isinstance(exc, CIError) and exc.kind != "missing" else "unreachable"
        pull_row(state)
        return 1, lines + ["ci: %s" % state]
    newest = _newest([(r.get("pipeline"), r.get("created_at")) for r in recorded])
    pull_row("ok", newest)
    lines.append("pull: %d new watch run(s), %d skipped; newest watch pipeline %s (%s)" % (new, skipped, newest[0] or "none", newest[1] or "never"))
    alert = [a for a in status_data(root, today)["alerts"] if a.startswith("TEST QUARANTINE ALERT: the watch ")]
    if capped:                                                 # an incomplete list is an unknown, never "nothing newer" (FR-59)
        return 1, lines + ["pull: " + capped[0]] + alert
    return (3, lines + alert) if alert else (0, lines)


def ci_summary(root, paths, env=None):
    """The summary of D.1: (record, lines). `paths` are the shard files of selftest --watch-out; complete only if every shard
    I/N is there from one sha, the union of their `expected` equals the quarantine rows of this checkout and each has a result."""
    env = os.environ if env is None else env
    shards = []
    for p in sorted(paths):
        try:
            d = json.loads(Path(p).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and isinstance(d.get("files"), dict):
            shards.append(d)
    forms = [re.fullmatch(r"(\d+)/(\d+)", str(d.get("shard"))) for d in shards]
    forms = [(int(m.group(1)), int(m.group(2))) for m in forms if m]
    totals = {n for _, n in forms}
    all_shards = len(totals) == 1 and {i for i, _ in forms} == set(range(1, max(totals) + 1))
    expected = {n for d in shards for n in d.get("expected") or []}
    layers = _layers(root)
    quarantine = set() if layers["absent"] else set(layers["quarantine"])
    merged = {}
    for d in shards:
        merged.update(d["files"])
    files = {n: merged.get(n) or {"status": "not_run"} for n in sorted(quarantine | expected)}
    shas = {d.get("sha") for d in shards if d.get("sha")}
    complete = bool(all_shards and expected == quarantine and all(n in merged for n in expected) and len(shas) <= 1)
    sha = next(iter(shas)) if len(shas) == 1 else (env.get("CI_COMMIT_SHA") if not shas else None)
    version = next((d.get("package_version") for d in shards if d.get("package_version")), None)
    pid = env.get("CI_PIPELINE_ID")
    rec = {"pipeline": int(pid) if str(pid).isdigit() else pid, "source": env.get("CI_PIPELINE_SOURCE"),
           "created_at": env.get("CI_PIPELINE_CREATED_AT"), "sha": sha, "package_version": version, "complete": complete, "files": files}
    count = {k: sum(1 for e in files.values() if e.get("status") == k) for k in ("green", "red", "timeout", "ran_nothing", "missing", "not_run")}
    lines = ["quarantine watch %s (package %s, pipeline %s, source %s): %d files -- %d green, %d red, %d timeout, %d ran nothing, "
             "%d missing, %d not run; complete: %s"
             % ((sha or "unknown")[:8], version or "unknown", rec["pipeline"], rec["source"], len(files), count["green"], count["red"],
                count["timeout"], count["ran_nothing"], count["missing"], count["not_run"], "yes" if complete else "no")]
    for name, e in files.items():
        st = e.get("status")
        if st == "green":
            continue
        if st != "red":
            lines.append("  %s: %s" % (st, name))
            continue
        fails = [f for f in e.get("fails") or [] if not _FAILS_MARKER.match(str(f))]
        extra = sum(int(m.group(1)) for m in (_FAILS_MARKER.match(str(f)) for f in e.get("fails") or []) if m)
        first = str(fails[0])[:160] if fails else (str(e.get("crash") or "no FAIL line")[:160])
        more = max(len(fails) - 1, 0) + extra
        lines.append("  red: %s  %s%s" % (name, first, " (+%d more)" % more if more else ""))
    lines.append("examine in a forge session: python tools/test_quarantine.py pull, then status")
    return rec, lines
# --- end of the watch -----------------------------------------------------------------------------------------------


_SELFTEST_LINE = re.compile(r"^(PASS|FAIL) tests: scripts[\\/]tests[\\/]([^\\/\s]+\.py)", re.M)


def _selftest_results(text):
    res = {}
    for word, name in _SELFTEST_LINE.findall(text):
        res[name] = "FAIL" if word == "FAIL" or res.get(name) == "FAIL" else "PASS"
    return res


WALKER = None       # tests inject a fake `walker(story_id, base) -> [result with .name, .kind]`; None = the package's scenario_walk.results_for


def _default_walker(root):
    return _pkg_module(root, "tests/scenario_walk").results_for


_RED_MARK = re.compile(r" \(red then: (\d+) rows\)")


def _walk_pairs(results, listed):
    """{(stage, facet): [rest of the names]} of the listed pairs that a PASS line judged and no FAIL line contradicts; NOTE lines judge nothing."""
    passed, failed = {}, set()
    for r in results:
        _id, sep, rest = str(r.name).partition("/")
        if not sep:
            continue
        for pair in listed:
            head = "%s/%s" % pair
            if rest == head or rest.startswith(head + " ("):
                if r.kind == "pass":
                    passed.setdefault(pair, []).append(rest)
                elif r.kind == "fail":
                    failed.add(pair)
    return {p: v for p, v in passed.items() if p not in failed}


def _story_facets(root, name, walker=None):
    """(is synthetic, facets a walk PASS judged) of the story behind test_scenario_<id>.py; the walk list of story.json is the frame and the
    walk result decides; unreadable story or absent folder -> (False, set()); a walker that raises -> (synthetic, set())."""
    want = name[len("test_scenario_"):-3]
    base = Path(root) / TESTS_REL / "fixtures" / "stories"
    for d in (sorted(base.iterdir()) if base.is_dir() else []):
        if d.name.replace("-", "_") != want:
            continue
        try:
            story = json.loads((d / "story.json").read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            return False, set()
        synthetic = story.get("synthetic") is True
        skipped = {(n.get("stage"), n.get("facet")) for n in story.get("not_walked") or [] if isinstance(n, dict)}
        listed = {(w.get("stage"), f) for w in story.get("walk") or [] if isinstance(w, dict)
                  for f in w.get("facets") or [] if (w.get("stage"), f) not in skipped}
        try:
            results = list((walker or WALKER or _default_walker(root))(d.name, base))
        except Exception:
            return synthetic, set()
        passed = _walk_pairs(results, {p for p in listed if all(isinstance(x, str) for x in p)})
        got = set(passed)
        red = story.get("red_then")
        if isinstance(red, dict):
            marks = [_RED_MARK.search(rest) for rest in passed.get((red.get("stage"), red.get("facet")), [])]
            if any(m and int(m.group(1)) >= 1 for m in marks) and _red_then_carried(d, red, got):
                got.add((RED_THEN, RED_THEN))
        return synthetic, got
    return False, set()


RED_THEN = "red_then"       # the coverage item, and the marker `_story_facets` adds when a story carries it


def _red_then_carried(folder, red, got):
    """A story carries a recorded red Then when its story.json holds `red_then: {stage, facet, evidence}`, that (stage, facet) is among
    its passed facets (walked, not skipped), and the evidence file (a path inside the story folder) exists (spec A.5, C.2 condition 2)."""
    if not isinstance(red, dict) or not all(isinstance(red.get(k), str) and red.get(k) for k in ("stage", "facet", "evidence")):
        return False
    if (red["stage"], red["facet"]) not in got:
        return False
    base = Path(folder).resolve()
    path = (base / red["evidence"]).resolve()
    return not Path(red["evidence"]).is_absolute() and path.is_relative_to(base) and path.is_file()


def _covered_required(required, got):
    def has(item):
        if item.endswith(".words"):
            return (item.split(".")[0], "decision") in got
        if item == RED_THEN:
            return (RED_THEN, RED_THEN) in got
        return any(stage == item for stage, _ in got)
    return [r for r in required if not has(r)]


def _refuse_enter(what, door):
    raise Refusal(f"quarantine enter refused: {what} -- {door}")


def _ci_call(fn, pid):
    try:
        return fn()
    except CIError as exc:
        if exc.kind == "missing":
            raise
        _refuse_enter("CI said %s" % exc.kind.replace("_", " "), CI_DOOR % pid)


def _need_ci(ctx):
    if ctx.ci is None:
        try:
            ctx.ci = ci_reader(ctx.root)
        except CIError as exc:
            _refuse_enter("CI cannot be read (%s)" % exc.kind.replace("_", " "), CI_DOOR % "<id>")
    return ctx.ci


def _short(names, n=5):
    return ", ".join(names[:n]) + (" +%d more" % (len(names) - n) if len(names) > n else "")


def _lines_of(root, names):
    total = 0
    for n in names:
        p = Path(root) / TESTS_REL / n
        total += len(p.read_text(encoding="utf-8", errors="replace").splitlines()) if p.is_file() else 0
    return total


def _write_msg(root, name, lines):
    out = Path(root) / "ci-out" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return "git commit -F ci-out/" + name


def _gate_lines(ars, how, why):
    """The package commit-gate lines every prepared message ends with (architecture, judgment, axes, piles-skip): all five commands
    change package files (test-layers.json, test files)."""
    return ["", "architecture: %s -- %s" % (ars, how), "judgment: none -- %s" % why,
            "axes: not a mechanism (a data move made by tools/test_quarantine.py; the mechanism block is in the TD-15.6a commit)",
            "piles-skip: TD-15 -- the owner's word 10.11.2026, docs/tasks/test-diet.md"]


def _selftest_text(ci, pid):
    """The selftest text of a pipeline: the report artifact; when it is missing (the report job is skipped by a red shard), the
    shard artifacts joined by a newline. One shard missing too is a CIError('missing') naming it, never a partial text."""
    try:
        return ci.artifact(pid, SELFTEST_JOB, SELFTEST_ART)
    except CIError as exc:
        if exc.kind != "missing":
            raise
        report_miss = f"{SELFTEST_ART} ({SELFTEST_JOB})"
    parts = []
    for i in range(1, SELFTEST_SHARDS + 1):
        job, art = SELFTEST_SHARD_JOB % i, SELFTEST_SHARD_ART % i
        try:
            parts.append(ci.artifact(pid, job, art))
        except CIError as exc:
            if exc.kind != "missing":
                raise
            raise CIError("missing", f"no {report_miss} and no {art} ({job})") from None
    return "\n".join(parts)


def _selftext(ctx, pid):
    try:
        return _ci_call(lambda: _selftest_text(_need_ci(ctx), pid), pid)
    except CIError as exc:
        _refuse_enter(f"pipeline {pid} has {exc}", CI_DOOR % pid)


def cmd_enter(args, ctx):
    root = ctx.root
    if args.rebase_entry:
        return _enter_rebase(args, ctx)
    if args.phase2:
        return _enter_phase2(args, ctx)
    if not args.pipeline or not args.coverage_pipeline:
        raise Refusal("enter needs --pipeline and --coverage-pipeline (or --phase2/--rebase-entry)")
    word = " ".join((args.owner_word or "").split())
    if args.owner_word is not None and not word:
        raise Refusal("quarantine enter refused: --owner-word needs the owner's words -- pass --owner-word \"<the owner's words, who, date>\" or leave it out")
    layers = _layers(root)
    if layers["absent"] or not layers["keep"]:
        _refuse_enter("test-layers.json is absent or has no keep rows", "write it first (node TD-15.2)")
    cfg = _config(root)
    keep, quarantine = layers["keep"], layers["quarantine"]
    cohort = str(args.pipeline)
    if cohort in layers["cohorts"]:
        _refuse_enter(f"cohort {cohort} already exists", "use a new pipeline id, or enter --phase2 for one detector")
    tests = sorted(p.name for p in (Path(root) / TESTS_REL).glob("test_*.py"))
    moving = [n for n in tests if n not in keep and n not in quarantine and n not in layers["pin_holds"]]
    if not moving:
        _refuse_enter("no test file is outside keep, quarantine and pin_holds", "nothing to move")
    named = sorted(_selftest(root).gate_named_files(forge_texts(root)))
    if [n for n in named if n not in keep]:
        _refuse_enter("a carrier names files that are not keep rows: " + _short([n for n in named if n not in keep]),
                      "add a keep row (layer gate_named) for each, or remove the name from the carrier")
    text = _selftext(ctx, args.pipeline)
    stories = [(n, _story_facets(root, n)) for n in sorted(keep) if keep[n].get("layer") == "scenario" and re.fullmatch(r"test_scenario_.+\.py", n)]
    stories = [(n, f) for n, (syn, f) in stories if syn]
    results = _selftest_results(text)
    if len(stories) < MIN_STORIES or any(results.get(n) != "PASS" for n, _ in stories):
        _refuse_enter(f"need {MIN_STORIES} synthetic scenario stories, all PASS in pipeline {args.pipeline} (found {len(stories)})",
                      "capture or record a story (TD-15.5.k / TD-15.5r)")
    missing = _covered_required(layers.get("story_coverage_required", []), set().union(*(f for _, f in stories)))
    if missing:
        _refuse_enter("missing coverage: " + ", ".join(missing), "capture or record a story that walks them (TD-15.5.k / TD-15.5r)")
    head, pipe_sha, pipeline_sha = _head(root), _ci_call(lambda: _need_ci(ctx).pipeline_sha(args.pipeline), args.pipeline), ""
    if pipe_sha != head:
        door = "run a web pipeline on the current HEAD, then enter again"
        rc, full = _git(root, "rev-parse", "--verify", pipe_sha + "^{commit}") if re.fullmatch(r"[0-9a-f]{40}", pipe_sha or "") else (1, "")
        if not word or rc or not full.strip():           # an unreadable pipeline commit is an unknown: never passed, even with the word
            _refuse_enter(f"pipeline {args.pipeline} did not run on HEAD",
                          door + ' ; or, if the owner says the last finished pipeline may stand, pass --owner-word "<the owner\'s words, who, date>"')
        pipeline_sha = full.strip()                      # a person's word passes this gate and is recorded (P13)
        _say("pipeline %s ran on %s, not on HEAD %s -- passed by the owner's word: %s" % (args.pipeline, pipeline_sha[:9], head[:9], word))
    bad =[n for n in sorted(keep) if results.get(n) != "PASS"]
    keep_fail, keep_absent = [], []
    if bad:
        hard = [n for n in bad if re.fullmatch(r"test_scenario_.+\.py", n)]
        if not word or hard:
            _refuse_enter(f"pipeline {args.pipeline} has no PASS line for keep rows: " + _short(bad),
                          CI_DOOR % args.pipeline + (" ; or, for keep rows that are not scenario stories, pass --owner-word \"<the owner's words, who, date>\"" if not hard else ""))
        # a person's word passes both lists and is recorded (P13); a FAIL line is a measured red, a missing line is never measured (FR-41): two lists
        keep_fail = sorted(n for n in set(bad) if results.get(n) == "FAIL")
        keep_absent = sorted(n for n in set(bad) if results.get(n) != "FAIL")
        if keep_fail:
            _say(_keep_line("keep rows with a FAIL line", args.pipeline, keep_fail, word))
        if keep_absent:
            _say(_keep_line("keep rows with no line at all (never measured)", args.pipeline, keep_absent, word))
    schedule_passed = False
    if _schedules(cfg["branch"]) != "ok":
        if not word:
            _refuse_enter("the watch schedule cannot be confirmed", 'ask the owner to create it: Settings -> CI/CD -> Schedules, cron "0 3 * * 1,4", '
                          "branch %s, variable QUARANTINE_WATCH=1; then record it in docs/RUNBOOK.md section 7; or, if the owner says it may wait, "
                          "pass --owner-word \"<the owner's words, who, date>\"" % cfg["branch"])
        schedule_passed = True                              # a person's word passes this one gate and is recorded (P13)
        _say("schedule not confirmed -- passed by the owner's word: %s" % word)
    covered_lines, total, keep_set_line = _coverage(root, ctx, args, keep, word)
    red, flaky = _baseline(ctx, args, cfg, text, moving)
    return _enter_write(root, args, layers, moving, cohort, covered_lines, total, red, flaky, schedule_passed, keep_fail, keep_absent, word,
                        pipeline_sha, keep_set_line)


def _keep_line(what, pipeline, names, word):
    """The line for keep rows passed by the owner's word: what they are, how many, which, and the words themselves."""
    return "%s in pipeline %s -- passed by the owner's word: %s -- %d file(s): %s" % (what, pipeline, word, len(names), ", ".join(names))


def _coverage(root, ctx, args, keep, word=""):
    """(covered lines, total, the passed-keep-set line or ""): a different keep set is refused, unless the owner's word passes it and the
    measured set could be read at all (an empty set is an unreadable blob, an unknown: never passed)."""
    pid = args.coverage_pipeline
    sha = _ci_call(lambda: _need_ci(ctx).pipeline_sha(pid), pid)
    measured = set(_blob_sections(root, sha)["keep"])
    keep_set_line = ""
    if measured != set(keep):
        if not word or not measured:
            _refuse_enter(f"the coverage pipeline {pid} measured a different keep set than HEAD",
                          'run test-redundancy with REDUNDANCY_SCOPE=keep on HEAD ; or, if the owner says the earlier measurement may stand, '
                          'pass --owner-word "<the owner\'s words, who, date>"')
        keep_set_line = "coverage pipeline %s measured %d keep file(s), HEAD has %d -- passed by the owner's word: %s" % (pid, len(measured), len(keep), word)
        _say(keep_set_line)
    try:
        report = _ci_call(lambda: _need_ci(ctx).artifact(pid, COVERAGE_JOB, COVERAGE_ART), pid)
    except CIError:
        report = ""
    m = re.search(r"product lines covered:\s*(\d+)", report)
    if not m:
        _refuse_enter(f"pipeline {pid} has no coverage measurement ({COVERAGE_JOB})", "run a web pipeline with TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep")
    scope = _coverage_scope(ctx, pid, report)
    if scope is None:
        _refuse_enter(f"the scope of coverage pipeline {pid} could not be established (the report names none and the pipeline variables "
                      "cannot be read)", "run a web pipeline with --var TEST_REDUNDANCY=1 --var REDUNDANCY_SCOPE=keep, then enter with its id "
                      "(a token that reads pipeline variables is needed to confirm it)")
    if scope != "keep":
        _refuse_enter(f"the coverage pipeline {pid} ran with scope {scope[:20]!r}, not keep",
                      "run a web pipeline with --var TEST_REDUNDANCY=1 --var REDUNDANCY_SCOPE=keep on HEAD")
    t = re.search(r"product lines (?:total|in scope):\s*(\d+)", report)
    return int(m.group(1)), (t.group(1) if t else "?"), keep_set_line


def _coverage_scope(ctx, pid, report):
    """The scope the coverage pipeline ran with, or None when it cannot be established: the pipeline's MEASURED REDUNDANCY_SCOPE variable
    first (a pipeline run without it ran the full scope: "full"), and a `scope: <word>` line of the report header only when the
    variables cannot be read (no producer writes that line today: test_redundancy.render_md emits none)."""
    try:
        variables = _need_ci(ctx).pipeline_variables(pid)
    except (CIError, AttributeError, ValueError, TypeError):
        m = re.search(r"^[-*\s]*scope:\s*`?([\w-]+)", report, re.M | re.I)
        return m.group(1).lower() if m else None
    return str(variables.get("REDUNDANCY_SCOPE") or "full").strip().lower()


def _baseline(ctx, args, cfg, text, moving):
    pool = {str(args.pipeline): text}
    try:
        ids = _ci_call(lambda: _need_ci(ctx).recent_pipelines(cfg["branch"]), args.pipeline)
        for pid in ids:
            if len(pool) >= BASELINE_RUNS:
                break
            if str(pid) not in pool:
                try:
                    pool[str(pid)] = _selftest_text(_need_ci(ctx), pid)
                except CIError as exc:
                    if exc.kind != "missing":
                        raise
    except CIError:
        _refuse_enter("CI said unreachable while reading the baseline", CI_DOOR % args.pipeline)
    if len(pool) < BASELINE_RUNS:
        _refuse_enter(f"only {len(pool)} package-full-report runs on {cfg['branch']}", "run the full tier %d more times" % (BASELINE_RUNS - len(pool)))
    per = [_selftest_results(t) for t in pool.values()]
    red = {n for n in moving if any(r.get(n) == "FAIL" for r in per)}
    flaky = {n for n in red if any(r.get(n) == "PASS" for r in per)}
    return red, flaky


def _enter_write(root, args, layers, moving, cohort, covered_lines, total, red, flaky, schedule_passed=False, keep_fail=(), keep_absent=(), word="",
                 pipeline_sha="", keep_set_line=""):
    keep, today = layers["keep"], date.today().isoformat()
    release, commit = _pkg_module(root, "install_paths").plugin_version(Path(root) / PKG), _head(root)
    st = _selftest(root)
    secs, slow_removed, slow_data = {}, 0, None
    if (Path(root) / SLOW_REL).is_file():
        try:
            slow_data = st.slow_tests(Path(root) / SLOW_REL)
        except st.SlowTestsError as exc:
            raise Refusal(f"quarantine enter refused: {exc} -- fix scripts/slow_tests.json first")
        secs = {n: s for n, s in slow_data["files"].items() if n in moving and isinstance(s, (int, float))}
        slow_removed = len([n for n in slow_data["files"] if n in moving])
    held = _import_pairs(_read_test(root), _importers(layers), set(moving))
    pin_held = [n for n in layers["pin_holds"] if n not in keep]
    layer_counts: dict = {}
    for r in keep.values():
        layer_counts[r["layer"]] = layer_counts.get(r["layer"], 0) + 1
    prose = _prose_mentions(root, set(moving))
    lines = _lines_of(root, moving)
    summary = ("quarantine enter: %d files (%d lines) to quarantine, %d kept (by layer: %s); held by import: %d (kept -> quarantined, %s); "
               "held by pins: %d; slow_tests.json -%d rows; red at entry: %d, flaky at entry: %d; canon after the move covers %d of %s lines; "
               "prose mentions to fix by hand: %s"
               % (len(moving), lines, len(keep), ", ".join(f"{k} {v}" for k, v in sorted(layer_counts.items())), len(held),
                  ", ".join(f"{a}->{b}" for a, b in held) or "none", len(pin_held), slow_removed, len(red), len(flaky), covered_lines, total,
                  _short(prose, 20) if prose else "none"))
    msg = ["quarantine-enter: cohort %s (%d files, entered at %s)" % (cohort, len(moving), release), summary,
           "canon after the move covers %d of %s product lines (pipeline %s)" % (covered_lines, total, args.coverage_pipeline)]
    if schedule_passed:
        msg.append("schedule not confirmed -- passed by the owner's word: %s" % word)
    if pipeline_sha:
        msg.append("pipeline %s ran on %s, not on HEAD %s -- passed by the owner's word: %s" % (args.pipeline, pipeline_sha[:9], commit[:9], word))
    if keep_set_line:
        msg.append(keep_set_line + " (the coverage number was measured on that earlier set)")
    if keep_fail:
        msg.append(_keep_line("keep rows with a FAIL line", args.pipeline, keep_fail, word))
    if keep_absent:
        msg.append(_keep_line("keep rows with no line at all (never measured)", args.pipeline, keep_absent, word))
    gates = sorted(g for g, passed in (("red_keep", keep_fail or keep_absent), ("schedule", schedule_passed), ("head", pipeline_sha),
                                       ("coverage_keep_set", keep_set_line)) if passed)
    msg += _gate_lines("AR-14", "the quarantine and cohorts sections are written only by test_quarantine.py enter; keep rows move, none is invented",
                       "the tool moved files by recorded CI results; whether a red is a real catch stays with judge")
    _say(summary)
    if held:
        raise Refusal("quarantine enter refused: %d kept or pin-held file(s) import a file about to move (%s) -- cut the import first "
                      "(TD-15.8); enter writes no quarantine-import line, the check would refuse the commit" % (len(held), _short([f"{a}->{b}" for a, b in held], 3)))
    if args.dry_run:
        _say("dry run: nothing written")
        return 0

    def mutate(raw):
        raw.setdefault("cohorts", {})[cohort] = {"entered": today, "release_at_entry": release, "commit_at_entry": commit, "phase": 1, "replaced_by": {}}
        if gates:                                            # ONE word, the gates it passed; a word that passed nothing is not recorded
            raw["cohorts"][cohort]["owner_word"] = word
            raw["cohorts"][cohort]["owner_word_gates"] = gates
        if pipeline_sha:
            raw["cohorts"][cohort]["pipeline_sha"] = pipeline_sha
        if keep_set_line:
            raw["cohorts"][cohort]["coverage_measured_on"] = str(args.coverage_pipeline)
        if keep_fail:
            raw["cohorts"][cohort]["keep_fail_at_entry"] = list(keep_fail)
        if keep_absent:
            raw["cohorts"][cohort]["keep_absent_at_entry"] = list(keep_absent)
        q = raw.setdefault("quarantine", {})
        for n in moving:
            row = {"cohort": cohort, "entered": today, "release_at_entry": release, "commit_at_entry": commit,
                   "red_at_entry": n in red, "flaky_at_entry": n in flaky}
            if n in secs:
                row["seconds"] = secs[n]
            q[n] = row
        raw["enforce_listing"] = True
    _write_layers(root, mutate)
    if slow_data is not None and slow_removed:
        slow_data["files"] = {n: s for n, s in slow_data["files"].items() if n not in moving}
        (Path(root) / SLOW_REL).write_text(st.render_slow_tests(slow_data), encoding="utf-8", newline="\n")
    _say(_write_msg(root, "quarantine-enter-msg.txt", msg))
    return 0


def _prose_mentions(root, names):
    out = []
    pat = re.compile(r"test_[A-Za-z0-9_]+\.py")
    for rel in FORGE_CARRIERS + PACKAGE_PROSE:
        p = Path(root) / rel
        if p.is_file():
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if any(m in names for m in pat.findall(line)):
                    out.append(f"{rel}:{n}")
    return out


def _enter_phase2(args, ctx):
    root, name, row = ctx.root, args.phase2, args.replaced_by
    layers = _layers(root)
    keep = layers["keep"]
    if keep.get(name, {}).get("layer") != "detector":
        _refuse_enter(f"{name} is not a keep row of layer detector", "phase 2 moves detectors only")
    if not row or row not in keep or keep[row].get("layer") not in ("scenario", "data_join", "table"):
        _refuse_enter(f"{row} is not a keep row of a scenario, data_join or table layer", "name the replacement row with --replaced-by")
    if not args.pipeline:
        raise Refusal("enter --phase2 needs --pipeline")
    if name in layers["pin_holds"]:
        _refuse_enter(f"{name} is held by a pin", "finish the role-rules wave (TD-5.3) for it first")
    if name in _selftest(root).gate_named_files(forge_texts(root)):
        _refuse_enter(f"a carrier still names {name}", "edit the carrier (SIBLING_MAP, architecture.md, ...) in the same prepared commit")
    if _ci_call(lambda: _need_ci(ctx).pipeline_sha(args.pipeline), args.pipeline) != _head(root):
        _refuse_enter(f"pipeline {args.pipeline} did not run on HEAD", "run a web pipeline on the current HEAD")
    if _selftest_results(_selftext(ctx, args.pipeline)).get(row) != "PASS":
        _refuse_enter(f"{row} is not green in pipeline {args.pipeline}", CI_DOOR % args.pipeline)
    cid = "%s-%s" % (args.pipeline, name[:-3])
    today = date.today().isoformat()
    release, commit = _pkg_module(root, "install_paths").plugin_version(Path(root) / PKG), _head(root)
    if args.dry_run:
        _say(f"quarantine enter: phase 2: {name} -> {row} (cohort {cid}); dry run: nothing written")
        return 0

    def mutate(raw):
        raw["cohorts"][cid] = {"entered": today, "release_at_entry": release, "commit_at_entry": commit, "phase": 2, "replaced_by": {name: row}}
        raw["keep"].pop(name)
        raw["quarantine"][name] = {"cohort": cid, "entered": today, "release_at_entry": release, "commit_at_entry": commit,
                                   "red_at_entry": False, "flaky_at_entry": False}
    _write_layers(root, mutate)
    _say("quarantine enter: phase 2: %s -> %s (cohort %s)" % (name, row, cid))
    _say(_write_msg(root, "quarantine-enter-msg.txt", [f"quarantine-enter: phase2 {name} -> {row}"] + _gate_lines(
        "AR-14", "the detector's keep row moves to quarantine only through enter --phase2, the one writer", "the tool moved one detector after the "
        "replacement row was green in CI; the replacement is judged by the role that named it")))
    return 0


def _enter_rebase(args, ctx):
    cohort, sha = args.rebase_entry
    layers = _layers(ctx.root)
    if cohort not in layers["cohorts"]:
        _refuse_enter(f"no cohort {cohort}", "name one of: " + ", ".join(sorted(layers["cohorts"])))
    rc, full = _git(ctx.root, "rev-parse", "--verify", sha + "^{commit}")
    if rc or _git(ctx.root, "merge-base", "--is-ancestor", full.strip(), "HEAD")[0]:
        _refuse_enter(f"{sha} is not a commit on the history of HEAD", "give the commit that now stands where the entry commit stood")
    full = full.strip()

    def mutate(raw):
        raw["cohorts"][cohort]["commit_at_entry"] = full
        for r in raw["quarantine"].values():
            if r.get("cohort") == cohort:
                r["commit_at_entry"] = full
    _write_layers(ctx.root, mutate)
    _say(f"quarantine enter: cohort {cohort} commit_at_entry is now {full[:8]}")
    _say(_write_msg(ctx.root, "quarantine-enter-msg.txt", [f"quarantine-enter: rebase {cohort}"] + _gate_lines(
        "AR-14", "commit_at_entry of the cohort is rewritten only by enter --rebase-entry, the one writer", "the tool replaced one commit id "
        "after a history rewrite; no verdict moves")))
    return 0


def cmd_drop_keep(args, ctx):
    layers = _layers(ctx.root)
    if args.file not in layers["keep"]:
        raise Refusal(f"drop-keep refused: {args.file} is not a keep row -- name a file of the keep section")
    if not (args.reason or "").strip():
        raise Refusal("drop-keep refused: the reason is empty -- give --reason TEXT, it goes into the commit message")

    def mutate(raw):
        raw["keep"].pop(args.file)
    _write_layers(ctx.root, mutate)
    path = Path(ctx.root) / TESTS_REL / args.file
    if path.is_file():
        path.unlink()
    _say(f"drop-keep: {args.file} removed from keep and deleted")
    _say(_write_msg(ctx.root, "keep-drop-msg.txt", [f"keep-drop: {args.file} -- {args.reason.strip()}"] + _gate_lines(
        "AR-14", "a keep row is dropped only by drop-keep, the one writer, with the reason in this message", "the person gave the reason "
        "(--reason); the tool deleted the row and the file and judged nothing")))
    return 0


SPLIT_WHY = " (part of %s split, TD-11c)"


def _split_refusal(why, expected):
    return Refusal(f"split-keep refused: {why} -- {expected}")


def _split_common(old):
    """(covers entry, file name) of the helper file the split tool writes for OLD: <stem without the test_ prefix>_common.py."""
    stem = Path(old).stem
    stem = stem[5:] if stem.startswith("test_") else stem
    return f"tests/{stem}_common.py", f"{stem}_common.py"


def cmd_split_keep(args, ctx):
    """One keep row becomes N part rows (TD-11c, F3): the one writer of the rows of a split. Everything is checked before anything is
    written; a refusal leaves the registry and the message file as they were."""
    old, root = args.old, Path(ctx.root)
    layers = _layers(ctx.root)
    reason = (args.reason or "").strip()
    parts = [p.strip() for p in (args.into or "").split(",")]
    if not (args.into or "").strip() or any(not p for p in parts):
        raise _split_refusal("--into is empty or holds an empty name", "give --into P1,P2 (the part files, comma-separated, no empty name)")
    if len(set(parts)) != len(parts):
        raise _split_refusal("--into names a part twice", "name every part once")
    if not reason:
        raise _split_refusal("the reason is empty", "give --reason TEXT, it goes into the commit message")
    if old not in layers["keep"]:
        raise _split_refusal(f"{old} is not a keep row", "name a file of the keep section (python tools/test_quarantine.py status lists them)")
    prefix = Path(old).stem + "_"
    for p in parts:
        if p == old:
            raise _split_refusal(f"part {p} is the old file itself", "a part has a new name; keep the old name only as a shim with --shim")
        if p in layers["quarantine"]:
            raise _split_refusal(f"part {p} is a quarantine name -- a quarantined file never returns",
                                 "give the part another name; put the case in a scenario or table row")
        for sec in ("keep", "quarantine", "pin_holds"):
            if p in layers[sec]:
                raise _split_refusal(f"part {p} is already a row of {sec}", "name only new files; a row that exists is not made twice")
        if not (p.startswith(prefix) and p.endswith(".py")):
            raise _split_refusal(f"part {p} is not named {prefix}<topic>.py", f"a part carries the old file's stem: {prefix}<topic>.py")
        if not (root / TESTS_REL / p).is_file():
            raise _split_refusal(f"part {p} is not on disk under {TESTS_REL}", "create the part files in this change first, then run split-keep")
    on_disk = (root / TESTS_REL / old).is_file()
    if args.shim and not on_disk:
        raise _split_refusal(f"--shim is given but {old} is not on disk", "write the shim file in this change, or run without --shim")
    if not args.shim and on_disk:
        raise _split_refusal(f"{old} is still on disk and no --shim is given", "delete the old file in this change or pass --shim")

    common_rel, common_name = _split_common(old)
    importers = [i.strip() for i in (getattr(args, "importers", None) or "").split(",") if i.strip()]

    def mutate(raw):
        keep, row, rebuilt = raw["keep"], raw["keep"][old], {}
        for name, val in keep.items():
            if name != old:
                rebuilt[name] = val
                continue
            if args.shim:
                shim = dict(row)
                shim["layer"] = "data_join"
                shim["why"] = f"split shim: re-exports for {', '.join(importers) or 'importers'}; checks live in " + ", ".join(parts)
                shim["covers"] = [common_rel]                   # the helper file as T-3 writes it (no test_ prefix)
                shim["named_by"] = []                           # the shim is never the named proof (E4)
                rebuilt[old] = shim
            for p in parts:
                new = dict(row)
                new["why"] = str(row.get("why", "")) + SPLIT_WHY % old
                if (root / TESTS_REL / common_name).is_file() and common_rel not in (row.get("covers") or []):
                    new["covers"] = list(row.get("covers") or []) + [common_rel]
                rebuilt[p] = new
        keep.clear()
        keep.update(rebuilt)
    _write_layers(ctx.root, mutate)
    _say(f"split-keep: {old} -> {', '.join(parts)}" + (" (old row rewritten as a shim)" if args.shim else " (old row removed)"))
    _say(_write_msg(ctx.root, "keep-split-msg.txt", [f"keep-split: {old} -> {', '.join(parts)} -- {reason}"] + _gate_lines(
        "AR-14", "a keep row is split only by split-keep, the one writer, with the reason in this message", "the person gave the reason "
        "(--reason); the tool copied the row to each part and judged nothing")))
    return 0


# --- check (K5) -----------------------------------------------------------------------------------------------------

_DOORS = {
    "split": re.compile(r"^keep-split:\s*(\S+)\s*->\s*(.+?)\s*--\s*\S", re.M),
    "edit": re.compile(r"^quarantine-edit:\s*(\S+)\s*--\s*\S", re.M),
    "purge": re.compile(r"^quarantine-purge:\s*\S", re.M),
    "enter": re.compile(r"^quarantine-enter:\s*\S", re.M),
    "drop": re.compile(r"^keep-drop:\s*(\S+)\s*--\s*\S", re.M),
    "import": re.compile(r"^quarantine-import:\s*(\S+)\s*->\s*(\S+)\s*--\s*\S", re.M),
    "accept": re.compile(r"^quarantine-accept:\s*([0-9a-fA-F]{7,40})\s*--\s*\S", re.M),
}
_ACCEPT = 'or a later commit line "quarantine-accept: <sha> -- <reason>"'


def _edit_refusal(n):
    return (f"quarantined file {n} was changed, deleted or renamed -- expected a line 'quarantine-edit: {n} -- <reason>' "
            f"(the bare file name, no folder) in this commit message")


def _commits(root, first):
    out = []
    for rng, flag in ((first, ["-1"]), (f"{first}..HEAD", [])):
        rc, txt = _git(root, "log", "--reverse", "--topo-order", *flag, "--format=%H%x1f%P%x1f%B%x1e", rng)
        if rc:
            raise Unknown("git history cannot be read for the quarantine check")
        for rec in txt.split("\x1e"):
            if rec.strip():
                sha, parents, msg = (rec.strip("\n").split("\x1f", 2) + ["", ""])[:3]
                out.append((sha.strip(), parents.split(), msg))
    return out


def _union(secs):
    return {k: {n: v for s in secs for n, v in s[k].items()} for k in ("keep", "quarantine", "pin_holds")}


def _touch(root, sha):
    rc, txt = _git(root, "diff-tree", "--no-commit-id", "-r", "--cc", "--root", "--name-status", "-M", sha)
    rows = []
    for line in txt.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            rows.append((parts[0], parts[1:]))
    return rows


def _tree_blobs(root, rev, cache):
    """{test file name: blob id} of the test folder at a revision: ONE `ls-tree` per revision, kept in `cache`."""
    key = ("tree", rev)
    if key not in cache:
        rc, txt = _git(root, "ls-tree", "-r", "-z", rev, "--", TESTS_REL + "/")        # -z: paths are raw, never quoted
        names = {}
        for line in txt.split("\0") if not rc else []:
            meta, _, path = line.partition("\t")
            parts = meta.split()
            if len(parts) == 3 and parts[1] == "blob" and path.startswith(TESTS_REL + "/") and "/" not in path[len(TESTS_REL) + 1:]:
                names[path[len(TESTS_REL) + 1:]] = parts[2]
        cache[key] = names
    return cache[key]


def _blob_text(root, sha, cache):
    """The text of a blob, read ONCE per blob id in a run (`cache` keyed by the id)."""
    key = ("blob", sha)
    if key not in cache:
        rc, txt = _git(root, "cat-file", "blob", sha)
        cache[key] = None if rc else txt
    return cache[key]


def _edges(root, rev, sec, cache):
    importers = _importers(sec)
    key = (rev, tuple(sorted(importers)), tuple(sorted(sec["quarantine"])))
    if key not in cache:
        tree = _tree_blobs(root, rev, cache)

        def read(name):
            return _blob_text(root, tree[name], cache) if name in tree else None
        cache[key] = set(_import_pairs(read, importers, sec["quarantine"]))
    return cache[key]


def _blob_id(root, rev, rel):
    rc, out = _git(root, "rev-parse", "--verify", "-q", f"{rev}:{rel}")
    return None if rc else out.strip()


def _removed_by(root, sec, parents, new):
    """{keep|quarantine: the rows THIS commit removes}. One parent: the rows it had and the result lacks. A merge is judged by the
    merge-base B (three-way): a row in B that the result lacks is the merge's unless some parent already lacked it (that parent's own
    commits removed it and were judged there); a row not in B that some parent added must be in the result. No merge-base (unrelated
    histories): the union of the parents' rows."""
    out = {"keep": set(), "quarantine": set()}
    if not parents:
        return out
    base = None
    if len(parents) > 1:
        rc, txt = _git(root, "merge-base", "--octopus", *parents)
        base = txt.split()[0] if not rc and txt.split() else None
    for k in out:
        held = [set(sec(p)[k]) for p in parents]
        missing = set().union(*held) - set(new[k])
        if base is None:
            out[k] = missing
        else:
            b = set(sec(base)[k])
            out[k] = {n for n in missing if n not in b or all(n in h for h in held)}
    return out


def _merge_edits(root, sec, sha, parents, new, msg, flagged):
    """Quarantine files a merge changes without a door, though no combined diff shows it (the merge took one side's blob; --cc lists
    only paths that differ from EVERY parent). Judged elsewhere only when another parent Q brought the same blob, held the row, and the
    merge-base held it too (Q's commits judged the edit). No merge-base: nothing here (the union rule and --cc stay)."""
    rc, txt = _git(root, "merge-base", "--octopus", *parents)
    if rc or not txt.split():
        return []
    base = sec(txt.split()[0])["quarantine"]
    out = []
    for n in sorted(set(new["quarantine"]) - flagged):
        if _DOORS["purge"].search(msg) or n in _DOORS["edit"].findall(msg):
            continue
        rel, holders = f"{TESTS_REL}/{n}", [p for p in parents if n in sec(p)["quarantine"]]
        res = _blob_id(root, sha, rel)
        blobs = {p: _blob_id(root, p, rel) for p in holders}
        if any(blobs[p] != res and not any(q != p and blobs.get(q, "-") == res and n in base for q in holders) for p in holders):
            out.append(_edit_refusal(n))
    return out


def _split_problems(root, sha, sold, parts, old, new, gone):
    """What is wrong with a `keep-split: OLD -> P1, P2 -- why` line in the commit SHA, judged on that commit's tree (rule 15): every part is
    a keep row ADDED here, named <OLD stem>_*, on disk in the tree, inheriting OLD's layer; and OLD is either absent from the tree with
    its row removed, or present with its row replaced by a shim row (named_by empty, 'split shim' why). [] = the line is honest."""
    fix = "(python tools/test_quarantine.py split-keep writes the rows)"
    orow, prefix = old["keep"].get(sold), Path(sold).stem + "_"
    if orow is None:
        return [f"keep-split line names {sold}, which is not a keep row in the parent -- name a kept file {fix}"]
    for p in parts:
        if p not in new["keep"] or p in old["keep"]:
            return [f"keep-split line for {sold} names part {p} which is not a keep row added by this commit -- {fix} or fix the line"]
        if not (p.startswith(prefix) and p.endswith(".py")):
            return [f"keep-split line for {sold} names part {p}, not named {prefix}<topic>.py -- a part carries the old file's stem"]
        if _blob_id(root, sha, f"{TESTS_REL}/{p}") is None:
            return [f"keep-split line for {sold} names part {p}, which is not in this commit's tree under {TESTS_REL} -- add the file"]
        if new["keep"][p].get("layer") != orow.get("layer"):
            return [f"keep-split line for {sold}: part {p} has layer {new['keep'][p].get('layer')}, the old row had {orow.get('layer')} -- a part inherits the layer"]
    if _blob_id(root, sha, f"{TESTS_REL}/{sold}") is None:
        if sold not in gone["keep"]:
            return [f"keep-split line names {sold}, whose file is gone but whose row stays -- remove the row ({fix})"]
        return []
    srow = new["keep"].get(sold)
    if srow is None:
        return [f"keep-split line names {sold}, whose row was removed while the file is still in this commit's tree -- "
                f"delete the old file or keep it as a shim row (split-keep --shim)"]
    if srow.get("named_by") or not str(srow.get("why", "")).startswith("split shim"):
        return [f"keep-split line names {sold}, which is still on disk but its row is not a shim row (named_by empty, why 'split shim: ...') -- "
                f"run split-keep --shim or delete the old file"]
    return []


def check_history(root):
    """[(sha, what is wrong and the door)] for every commit since test-layers.json appeared, accepted ones removed."""
    rc, txt = _git(root, "log", "--diff-filter=A", "--format=%H", "--", LAYERS_REL)
    shas = txt.split()
    if rc or not shas:
        return []
    commits = _commits(root, shas[-1])
    secs, ever_q, edges, bad = {}, set(), {}, []
    first_enter = None

    def sec(rev):
        if rev not in secs:
            secs[rev] = _blob_sections(root, rev)
        return secs[rev]

    for i, (sha, parents, msg) in enumerate(commits):
        new = sec(sha)
        old = _union([sec(p) for p in parents]) if parents else {"keep": {}, "quarantine": {}, "pin_holds": {}}
        gone = _removed_by(root, sec, parents, new)         # a merge's own removals only: a side's were judged in the side's commits
        found = []
        touched = _touch(root, sha)
        names = {p for _, ps in touched for p in ps}
        flagged = set()
        for n in sorted(old["quarantine"]):
            if f"{TESTS_REL}/{n}" in names and not (
                    _DOORS["purge"].search(msg) or n in [m for m in _DOORS["edit"].findall(msg)]):
                flagged.add(n)
                found.append(_edit_refusal(n))
        if len(parents) > 1:
            found += _merge_edits(root, sec, sha, parents, new, msg, flagged)
        for n in sorted(gone["quarantine"]):
            if not _DOORS["purge"].search(msg):
                found.append(f"quarantine row {n} was removed -- expected 'quarantine-purge: <cohort>' in this commit message")
        for n in sorted(set(new["quarantine"]) - set(old["quarantine"])):
            if not _DOORS["enter"].search(msg):
                found.append(f"quarantine row {n} was added -- expected 'quarantine-enter: <what>' in this commit message")
        split_ok = set()
        for sold, plist in _DOORS["split"].findall(msg):
            problems = _split_problems(root, sha, sold, re.split(r"\s*,\s*", plist.strip()), old, new, gone)
            found += problems
            if not problems:
                split_ok.add(sold)
        split_named = {s for s, _ in _DOORS["split"].findall(msg)}
        for n in sorted(gone["keep"]):
            dropped = n in _DOORS["drop"].findall(msg) and any(s.startswith("D") and f"{TESTS_REL}/{n}" in ps for s, ps in touched)
            if n in split_named and n not in split_ok and not (_DOORS["enter"].search(msg) or dropped):
                continue                                    # the split line's own refusal above names the part
            if not (_DOORS["enter"].search(msg) or dropped or n in split_ok):
                found.append(f"keep row {n} was removed -- expected 'quarantine-enter:' (moved) or 'keep-drop: {n} -- <reason>' with the file deleted in this commit")
        ever_q |= set(old["quarantine"]) | set(new["quarantine"])
        for n in sorted((set(new["keep"]) - set(old["keep"])) & ever_q):
            found.append(f"keep row {n} returns a file that was in quarantine -- a quarantined test never returns; put its case as a scenario or table row (no door)")
        if first_enter is not None:
            for n in sorted(set(new["pin_holds"]) - set(old["pin_holds"])):
                found.append(f"pin_holds row {n} was added after the first quarantine-enter -- a pin cannot be added once files moved")
        if first_enter is None and _DOORS["enter"].search(msg):
            first_enter = i
        if any(p.startswith(TESTS_REL + "/") and p.endswith(".py") or p == LAYERS_REL for p in names):
            for kept, quar in sorted(_edges(root, sha, new, edges) - (set().union(*(_edges(root, p, sec(p), edges) for p in parents)) if parents else set())):
                if (kept, quar) not in _DOORS["import"].findall(msg):
                    found.append(f"new import edge {kept} -> {quar} (kept -> quarantined) -- expected 'quarantine-import: {kept} -> {quar} -- <reason>'")
        for text in found:
            accepted = any(sha.lower().startswith(s.lower()) for _, _, later in commits[i + 1:] for s in _DOORS["accept"].findall(later))
            if not accepted:
                bad.append((sha, text))
    return bad


def _rebase_problems(root, layers):
    out = []
    for cid, row in sorted(layers["cohorts"].items()):
        if _git(root, "merge-base", "--is-ancestor", str(row.get("commit_at_entry")), "HEAD")[0]:
            out.append(f"cohort {cid}: commit_at_entry {str(row.get('commit_at_entry'))[:8]} is not an ancestor of HEAD (history was rewritten) -- "
                       f"python tools/test_quarantine.py enter --rebase-entry {cid} <new sha>")
    return out


def cmd_check(args, ctx):
    path = Path(ctx.root) / LAYERS_REL
    if not path.is_file():
        _say("no test-layers.json")
        return 0
    layers = _layers(ctx.root)
    bad = check_history(ctx.root)
    problems = _rebase_problems(ctx.root, layers)
    for sha, text in bad:
        _say(f"quarantine check: {sha[:8]}: {text}; {_ACCEPT}")
    for p in problems:
        _say("quarantine check: " + p)
    _say("quarantine check: %d violation(s)" % (len(bad) + len(problems)))
    return 1 if bad or problems else 0


# --- status / judge / land ------------------------------------------------------------------------------------------

def cmd_status(args, ctx):
    d = status_data(ctx.root, ctx.today)
    if d["no_quarantine"]:
        _say("no quarantine")
        return 0
    if d["unknown"]:
        _say("TEST QUARANTINE: status unknown (%s)" % d["unknown"])
        return 1
    for line in status_line(ctx.root, ctx.today):
        _say(line)
    unknown = 0
    for c in d["cohorts"]:
        if c.get("unknown"):
            unknown += 1                                    # its line was printed above by status_line; an unknown is exit 1, never 0
            continue
        _say(f"cohort {c['id']}: {'READY' if c['ready'] else 'not ready'}")
        for rid, ok, detail in c["rules"]:
            _say(f"  {rid} {'pass' if ok else 'fail'}: {detail}")
        for o in c["observations"]:
            mark = "unexamined" if o in c["unexamined"] else "examined"
            _say("  red: %s (pipeline %s, %s) %s" % (o["file"], o["pipeline"], mark, ",".join(o["signature"])[:120]))
        for k in c["conflicts"]:
            _say("  conflict: %s %s" % (k[0], k[2]))
        _say(f"  blind: {c['blind']} files")
    return 1 if unknown else 0


def cmd_judge(args, ctx):
    runs, _ = _watch_rows(ctx.root)
    run = next((r for r in runs if str(r.get("pipeline")) == str(args.pipeline)), None)
    rec = (run or {}).get("files", {}).get(args.file)
    if run is None or not isinstance(rec, dict) or rec.get("status") in (None, "green", "not_run"):
        raise Refusal(f"judge refused: no red observation of {args.file} in pipeline {args.pipeline} of watch.jsonl -- run pull, then name a red file")
    if args.verdict not in VERDICTS:
        raise Refusal("judge refused: --verdict must be one of " + ", ".join(VERDICTS))
    if not args.by or not (args.reason or "").strip() or "\n" in args.reason:
        raise Refusal("judge refused: --by and a one-line --reason are required -- say who judged and why")
    if args.verdict == "real_catch" and not args.finding:
        raise Refusal("judge refused: a real_catch needs --finding <path> -- write the finding file in the pile (PROJECT.md, Teamwork, item 2)")
    sig = list(signature(rec))
    if args.verdict == "flaky":
        sha = run.get("sha")
        same = [(r.get("files") or {}).get(args.file, {}).get("status") for r in runs if r.get("sha") == sha]
        if not ("green" in same and any(s not in (None, "green", "not_run") for s in same)):
            raise Refusal(f"judge refused: no red and green of {args.file} on the same sha -- retry the quarantine-watch job of pipeline "
                          f"{args.pipeline} (GitLab: Retry), then re-read it: python tools/test_quarantine.py pull --pipeline {args.pipeline}")
    row = {"ts": datetime.now().isoformat(timespec="seconds"), "file": args.file, "signature": sig, "pipeline": run.get("pipeline"),
           "verdict": args.verdict, "by": args.by, "reason": args.reason.strip(), "finding": args.finding, "task": args.task}
    key = _key(row)
    if any(_key(v) == key for v in _verdict_rows(ctx.root)[0]) and not args.supersede:
        raise Refusal(f"judge refused: a verdict on ({args.file}, pipeline {args.pipeline}) already exists -- add --supersede \"<why>\" to replace it")
    if args.supersede:
        row["supersede"] = args.supersede
    _append(ctx.root, VERDICTS_REL, row)
    _say(f"judge: {args.file} pipeline {args.pipeline} {args.verdict} recorded")
    return 0


def cmd_land(args, ctx):
    verdicts, _ = _verdict_rows(ctx.root)
    if not any(v["verdict"] == "real_catch" and v.get("file") == args.file and str(v.get("pipeline")) == str(args.pipeline) for v in verdicts):
        raise Refusal(f"land refused: no real_catch verdict for {args.file} in pipeline {args.pipeline} -- judge it first")
    if _git(ctx.root, "cat-file", "-e", str(args.commit) + "^{commit}")[0]:
        raise Refusal(f"land refused: commit {args.commit} is not in this clone -- name the commit that holds the scenario or table row")
    run = next((r for r in _watch_rows(ctx.root)[0] if str(r.get("pipeline")) == str(args.pipeline)), {})
    _append(ctx.root, VERDICTS_REL, {"ts": datetime.now().isoformat(timespec="seconds"), "kind": "land", "file": args.file,
                                     "pipeline": run.get("pipeline", args.pipeline), "commit": args.commit})
    _say(f"land: {args.file} pipeline {args.pipeline} moved in {args.commit[:8]}")
    return 0


# --- pull / ci-summary / purge -------------------------------------------------------------------------------------

def cmd_pull(args, ctx):
    code, lines = pull(ctx.root, ctx.ci, args.pipeline, ctx.today)
    for line in lines:
        _say(line)
    return code


def cmd_ci_summary(args, ctx):
    if not args.from_glob:
        _say("ci-summary needs --from \"<glob of the shard files>\" (and --out <file> for the record)")
        return 2
    pattern = args.from_glob if os.path.isabs(args.from_glob) else str(Path(ctx.root) / args.from_glob)
    rec, lines = ci_summary(ctx.root, glob.glob(pattern))
    if args.out:
        out = Path(args.out) if os.path.isabs(args.out) else Path(ctx.root) / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
    for line in lines:
        _say(line)
    return 0


def cmd_purge(args, ctx):
    """Spec D.6: delete a READY cohort on the owner's word. Everything is computed and checked first, then written (a refusal
    leaves the tree as it was); the commit itself is prepared (ci-out/quarantine-purge-msg.txt), not made."""
    root = Path(ctx.root)
    word = " ".join((args.owner_word or "").split())
    if not word:
        _purge_refuse("--owner-word is empty; expected who gave the word and when",
                      "deletion is only on the owner's word: ask her, then pass --owner-word \"<who, date>\"")
    layers = _layers(root)
    if layers["absent"] or not (layers["quarantine"] or layers["cohorts"]):
        raise Refusal("purge refused: there is no quarantine, nothing to purge -- status says `no quarantine`")
    cid = args.cohort
    if not cid or cid not in layers["cohorts"]:
        _purge_refuse(f"--cohort {cid!r} names no cohort (known: {', '.join(sorted(layers['cohorts'])) or 'none'})",
                      "pass --cohort <id> as status prints it")
    deleted = sorted(n for n, r in layers["quarantine"].items() if r.get("cohort") == cid)
    if not deleted:
        _say(f"quarantine purge: cohort {cid} has no files; nothing changed")
        return 0
    d = status_data(root, ctx.today)
    cohort = next((c for c in d["cohorts"] if c["id"] == cid), None)
    if d["unknown"] or cohort is None or cohort.get("unknown"):
        why = d["unknown"] or (cohort or {}).get("unknown") or "cohort not found in the status"
        _purge_refuse(f"the state of cohort {cid} is unknown ({str(why)[:150]})",
                      "fix what status names, then retry; an unknown is never READY")
    if not cohort["ready"]:
        bad = "; ".join(f"{rid}: {detail}" for rid, ok, detail in cohort["rules"] if not ok)
        _purge_refuse(f"cohort {cid} is not READY TO DELETE ({bad})",
                      "python tools/test_quarantine.py status prints every rule; purge only when all pass")
    plan = _purge_plan(root, layers, cid, deleted, args)
    if args.dry_run:
        _say(_purge_summary(plan, dry=True))
        return 0
    _purge_apply(root, plan, cid, word)
    plan["commit"] = _write_msg(root, "quarantine-purge-msg.txt",
                                [f"tests: purge quarantine cohort {cid} ({len(deleted)} files)", "", f"quarantine-purge: {cid}",
                                 f"owner-word: {word}"] + _gate_lines(
                                    "AR-14, AR-25", "the cohort rows leave only through purge, the one writer, on the owner's word; purge is the "
                                    "way out of a READY cohort", "the tool deleted what status called READY on the owner's word; the READY "
                                    "verdict is the role's and the owner's"))
    rc, out = _purge_lint(root)
    _say("lint ratchet --check: exit %d" % rc)
    for line in out.splitlines()[:5]:
        _say("  " + line)
    _say(_purge_summary(plan, dry=False))
    return 0


def _purge_refuse(what, door):
    raise Refusal(f"purge refused: {what} -- {door}")


def _purge_lint(root):
    try:
        p = subprocess.run([sys.executable, "-B", str(_TOOLS / "lint_ratchet.py"), "--check", "--repo", str(root)], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=600)
    except (OSError, subprocess.SubprocessError) as exc:
        return 2, "lint_ratchet could not run: %s" % exc
    return p.returncode, p.stdout


def _purge_text(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _purge_py_files(sdir):
    """Every .py under the package scripts/, except fixture folders and caches (the files that can import or read)."""
    out = []
    for p in sorted(Path(sdir).rglob("*.py")):
        rel = p.relative_to(sdir).parts
        if "__pycache__" in rel or ("tests" in rel[:1] and "fixtures" in rel[1:2]):
            continue
        out.append(p)
    return out


def _purge_helpers(tdir, py_files, deleted):
    """(helpers to delete, kept files that import a deleted test): a helper of scripts/tests/ reached from the deleted files
    and from no remaining file, transitively. A remaining file importing a deleted test is a refusal's fact."""
    mods = {p.stem: p for p in py_files if p.parent == Path(tdir)}

    def deps(path):
        return {m for m in _imports(_purge_text(path)) if m in mods}
    cands, todo = set(), [Path(tdir) / n for n in deleted]
    while todo:
        for m in deps(todo.pop()):
            if not m.startswith("test_") and m not in cands:
                cands.add(m)
                todo.append(mods[m])
    roots = [p for p in py_files if p.name not in deleted and p.stem not in cands]
    broken = sorted(p.name for p in roots if any(m + ".py" in deleted for m in _imports(_purge_text(p))))
    reached, todo = set(), list(roots)
    while todo:
        for m in deps(todo.pop()):
            if m in cands and m not in reached:
                reached.add(m)
                todo.append(mods[m])
    return sorted(mods[m].name for m in cands - reached), broken


def _purge_named(text, name):
    return re.search(r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])", text) is not None


def _purge_dynamic(path):
    """[line] where a remaining file builds a fixture path from a non-literal part or walks a fixture folder (K10)."""
    text = _purge_text(path)
    if "fixture" not in text.lower():
        return []
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return [1]
    lines = []
    for node in ast.walk(tree):
        try:
            src = ast.unparse(node).lower()
        except Exception:                                   # unparse is only a filter; a node it cannot print is not dynamic
            continue
        if "fixture" not in src:
            continue
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and not isinstance(node.right, ast.Constant):
            lines.append(node.lineno)
        elif isinstance(node, ast.JoinedStr) and any(isinstance(v, ast.FormattedValue) for v in node.values):
            lines.append(node.lineno)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in ("iterdir", "glob", "rglob", "listdir", "walk", "scandir"):
                lines.append(node.lineno)
            elif node.func.attr in ("join", "joinpath") and any(not isinstance(a, ast.Constant) for a in node.args):
                lines.append(node.lineno)
    return sorted(set(lines))


def _purge_corpus(root, skip):
    """(relative name, text) of every remaining text file of the package outside the fixture folders: tests, helpers, histories,
    registries. `skip` = absolute paths about to be deleted."""
    pkg, fx = Path(root) / PKG, Path(root) / TESTS_REL / "fixtures"
    out = []
    for p in sorted(pkg.rglob("*")):
        if not p.is_file() or p in skip or "__pycache__" in p.parts or p.suffix not in (".py", ".json", ".md", ".txt", ".yml", ".yaml", ".toml"):
            continue
        if fx in p.parents:
            continue
        out.append((p.relative_to(pkg).as_posix(), _purge_text(p)))
    for p in sorted(fx.glob("*")):                       # a registry file lying directly in fixtures/ is a carrier as well
        if p.is_file() and p not in skip and p.suffix in (".json", ".md", ".txt"):
            out.append((p.relative_to(pkg).as_posix(), _purge_text(p)))
    return out


def _purge_timeouts(text, names):
    """(new text, rows removed): TEST_TIMEOUTS entries of `names` removed by their `ast` line ranges; comments and every other
    line stay. A parse failure, a shared line or a changed key set is a refusal."""
    door = "remove them by hand in the same change, then pass --registries-done"
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError) as exc:
        raise Refusal(f"purge refused: selftest.py does not parse ({str(exc)[:80]}) -- {door}") from None
    node = None
    for n in tree.body:
        targets = n.targets if isinstance(n, ast.Assign) else [n.target] if isinstance(n, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == "TEST_TIMEOUTS" for t in targets) and isinstance(n.value, ast.Dict):
            node = n.value
    if node is None:
        if any(_purge_named(text, n) for n in names):
            raise Refusal(f"purge refused: selftest.py names a deleted file but has no TEST_TIMEOUTS dict literal -- {door}")
        return text, 0
    spans = []
    for k, v in zip(node.keys, node.values):
        key = k.value if isinstance(k, ast.Constant) and isinstance(k.value, str) else None
        spans.append((key, (k or v).lineno, v.end_lineno))
    drop = [s for s in spans if s[0] in names]
    if not drop:
        return text, 0
    clash = [s[0] for s in drop if s[1] <= node.lineno or s[2] >= node.end_lineno
             or any(o is not s and not (o[2] < s[1] or o[1] > s[2]) for o in spans)]
    if clash:
        raise Refusal("purge refused: TEST_TIMEOUTS entries share a line with the braces or another entry: "
                      f"{', '.join(clash)} -- {door}")
    gone = {i for s in drop for i in range(s[1], s[2] + 1)}
    new = "".join(ln for i, ln in enumerate(text.splitlines(keepends=True), 1) if i not in gone)
    try:
        again = ast.parse(new)
    except (SyntaxError, ValueError):
        raise Refusal(f"purge refused: selftest.py would not parse after the edit -- {door}") from None
    after = [n for n in again.body if (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "TEST_TIMEOUTS" for t in n.targets))
             or (isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == "TEST_TIMEOUTS")]
    keys = [k.value for k in after[-1].value.keys if isinstance(k, ast.Constant)] if after else None
    if keys != [s[0] for s in spans if s[0] not in names and s[0] is not None]:
        raise Refusal(f"purge refused: the TEST_TIMEOUTS rows of kept files would change -- {door}")
    return new, len(drop)


def _purge_repair(kept_lines, expected, rel):
    new = re.sub(r",(\r?\n\s*[\]}])", r"\1", "".join(kept_lines))
    try:
        ok = json.loads(new) == expected
    except ValueError:
        ok = False
    if not ok:
        raise Refusal(f"purge refused: {rel} cannot be edited line by line (a row spans lines or shares one) -- "
                      "edit it by hand in the same change, then pass --registries-done")
    return new


def _purge_driver_layers(text, names, rel):
    raw = json.loads(text.lstrip("﻿"))
    sections = ("source_readers", "source_mentions")
    expected = dict(raw)
    n = 0
    for sec in sections:
        rows = raw.get(sec) or []
        keep = [r for r in rows if not (isinstance(r, dict) and r.get("file") in names)]
        n += len(rows) - len(keep)
        if sec in raw:
            expected[sec] = keep
    if not n:
        return text, 0
    state, kept = [None], []
    for ln in text.splitlines(keepends=True):
        s = ln.strip()
        m = re.match(r'"(source_readers|source_mentions)"\s*:\s*\[', s)
        if m:
            state[0] = m.group(1)
        elif state[0] and s.startswith("]"):
            state[0] = None
        elif state[0] and s.startswith("{"):
            try:
                row = json.loads(s.rstrip(","))
            except ValueError:
                row = None
            if isinstance(row, dict) and row.get("file") in names:
                continue
        kept.append(ln)
    return _purge_repair(kept, expected, rel), n


def _purge_features(text, names, rel):
    raw = json.loads(text.lstrip("﻿"))
    globs = {"scripts/tests/" + n for n in names}
    n = 0
    for feat in raw.get("features", []):
        if isinstance(feat, dict) and isinstance(feat.get("globs"), list):
            keep = [g for g in feat["globs"] if g not in globs]
            n += len(feat["globs"]) - len(keep)
            feat["globs"] = keep
    if not n:
        return text, 0
    kept = []
    for ln in text.splitlines(keepends=True):
        try:
            val = json.loads(ln.strip().rstrip(","))
        except ValueError:
            val = None
        if isinstance(val, str) and val in globs:
            continue
        kept.append(ln)
    return _purge_repair(kept, raw, rel), n


def _purge_slow(root, names, tdir):
    """(new text or None, rows removed): slow_tests.json through the package's own updater with an empty measurement; rows of
    benched files of OTHER cohorts that still exist are put back (only the named cohort goes)."""
    path = Path(root) / SLOW_REL
    if not path.is_file():
        return None, 0
    st = _selftest(root)
    try:
        data = st.slow_tests(path)
        new = st.slow_tests_updated(data, {}, data["measured_on"], data["source"], tdir)
    except (st.SlowTestsError, st.TestLayersError) as exc:
        raise Refusal(f"purge refused: slow_tests.json cannot be updated ({str(exc)[:150]}) -- fix it, then retry") from None
    for n, secs in data["files"].items():
        if n not in new["files"] and n not in names and (Path(tdir) / n).is_file():
            new["files"][n] = secs
    text = st.render_slow_tests(new)
    return (text if text != _purge_text(path) else None), len(set(data["files"]) & set(names))


def _purge_plan(root, layers, cid, deleted, args):
    root, names = Path(root), set(deleted)
    tdir = root / TESTS_REL
    py = _purge_py_files(root / PKG / "scripts")
    helpers, broken = _purge_helpers(tdir, py, names)
    if broken:
        _purge_refuse("kept files import a file of the cohort: " + ", ".join(broken),
                      "cut the import (TD-15.8) or move the file out of the cohort; purge deletes nothing a kept file reads")
    gone = {tdir / n for n in deleted} | {tdir / h for h in helpers}
    plan = {"deleted": deleted, "helpers": helpers, "lines": _lines_of(root, deleted), "cohort": cid,
            "tests_dir": tdir, "folders": [], "kept": [], "used_by": [], "dynamic": [], "candidates": [], "by_hand": []}
    texts = " ".join(_purge_text(p) for p in gone if p.suffix == ".py")
    fx = tdir / "fixtures"
    cands = sorted(p.name for p in fx.iterdir() if p.is_dir() and _purge_named(texts, p.name)) if fx.is_dir() else []
    corpus = _purge_corpus(root, gone)
    for name in cands:
        users = sorted({rel for rel, text in corpus if _purge_named(text, name)})
        if users:
            plan["kept"].append(name)
            plan["used_by"] += users
        else:
            plan["candidates"].append(name)
    dyn = [f"{p.relative_to(root).as_posix()}:{ln}" for p in py if p not in gone and p.name not in names for ln in _purge_dynamic(p)[:1]]
    if dyn:
        plan["dynamic"] = dyn
    else:
        plan["folders"] = plan["candidates"]
    edits = {}
    jobs = (("TEST_TIMEOUTS", root / PKG / "scripts" / "selftest.py", lambda t: _purge_timeouts(t, names)),
            ("driver-layers.json", fx / "driver-layers.json", lambda t: _purge_driver_layers(t, names, "driver-layers.json")),
            ("features.json", root / "plans" / "features.json", lambda t: _purge_features(t, names, "features.json")))
    counts = {}
    for label, path, fn in jobs:
        counts[label] = 0
        if not path.is_file():
            continue
        try:
            text, counts[label] = fn(path.read_text(encoding="utf-8", errors="replace"))
        except (Refusal, ValueError) as exc:
            if not args.registries_done:
                raise exc if isinstance(exc, Refusal) else Refusal(
                    f"purge refused: {label} cannot be read ({str(exc)[:80]}) -- fix it, or edit it by hand and pass --registries-done")
            plan["by_hand"].append(label)
            continue
        if counts[label]:
            edits[path] = text
    slow_text, counts["slow_tests.json"] = _purge_slow(root, names, tdir)
    if slow_text is not None:
        edits[root / SLOW_REL] = slow_text
    plan["counts"], plan["edits"] = counts, edits
    plan["named"] = _purge_named_in_text(root, deleted)
    return plan


def _purge_named_in_text(root, names):
    rels = list(FORGE_CARRIERS) + list(PACKAGE_PROSE) + [PKG + "/references/gate-registry.json", PKG + "/references/stage-joints.json",
                                                      PKG + "/scripts/install_smoke.py"]
    found = []
    for rel in rels:
        for i, line in enumerate(_purge_text(Path(root) / rel).splitlines(), 1):
            if any(_purge_named(line, n) for n in names):
                found.append(f"{rel}:{i}")
    return found


def _purge_apply(root, plan, cid, word):
    root, tdir = Path(root), plan["tests_dir"]
    for path, text in plan["edits"].items():
        path.write_text(text, encoding="utf-8", newline="")
    for n in plan["deleted"] + plan["helpers"]:
        if (tdir / n).is_file():
            (tdir / n).unlink()
        else:                                               # deleted earlier (a quarantine-edit): nothing to remove, the rows still go
            _say("already absent: %s" % n)
    for f in plan["folders"]:
        shutil.rmtree(tdir / "fixtures" / f)
    gone = set(plan["deleted"])

    def mutate(raw):
        raw["quarantine"] = {n: r for n, r in raw.get("quarantine", {}).items() if r.get("cohort") != cid}
        raw.get("cohorts", {}).pop(cid, None)
        if "pin_holds" in raw:
            raw["pin_holds"] = {n: r for n, r in raw["pin_holds"].items() if n not in gone}
    _write_layers(root, mutate)
    _append(root, VERDICTS_REL, {"ts": datetime.now().isoformat(timespec="seconds"), "kind": "purge", "cohort": cid,
                                 "owner_word": word, "files": plan["deleted"]})


def _purge_summary(plan, dry):
    c = plan["counts"]
    kept = "%d kept" % len(plan["kept"]) + (": used by " + _short(sorted(set(plan["used_by"])), 3) if plan["kept"] else "")
    reg = ", ".join(f"{k} -{c[k]}" for k in ("TEST_TIMEOUTS", "slow_tests.json", "driver-layers.json", "features.json"))
    if plan["by_hand"]:
        reg += " (by hand: %s)" % ", ".join(plan["by_hand"])
    line = ("quarantine purge%s: %d test files %s (%d lines), %d fixture folders %s (%s), %d helpers %s; registries: %s; "
            "still named in text: %s"
            % (" (dry run)" if dry else "", len(plan["deleted"]), "would be deleted" if dry else "deleted", plan["lines"],
               len(plan["folders"]), "would be deleted" if dry else "deleted", kept, len(plan["helpers"]),
               "would be deleted" if dry else "deleted", reg, _short(plan["named"], 5) or "none"))
    if plan["dynamic"]:
        line += ("; fixture folders NOT deleted: a kept file builds a fixture path dynamically (%s); candidates left: %s"
                 % (_short(plan["dynamic"], 3), _short(plan["candidates"], 8) or "none"))
    return line if dry else line + "; commit: " + plan["commit"]
# --- end of purge ---------------------------------------------------------------------------------------------------


class Ctx:
    def __init__(self, root, ci=None, today=None):
        self.root, self.ci, self.today = Path(root), ci, today


def build_parser():
    ap = argparse.ArgumentParser(prog="test_quarantine.py", description=__doc__.split("\n")[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        p = sub.add_parser(name, parents=[common])
        p.set_defaults(func=func)
        return p
    e = add("enter", cmd_enter)
    e.add_argument("--pipeline")
    e.add_argument("--coverage-pipeline")
    e.add_argument("--dry-run", action="store_true")
    e.add_argument("--owner-word", default=None)
    e.add_argument("--phase2")
    e.add_argument("--replaced-by")
    e.add_argument("--rebase-entry", nargs=2, metavar=("COHORT", "NEW_SHA"))
    add("check", cmd_check)
    add("status", cmd_status)
    j = add("judge", cmd_judge)
    j.add_argument("file")
    j.add_argument("--pipeline", required=True)
    j.add_argument("--verdict", required=True, choices=VERDICTS)
    j.add_argument("--by", required=True)
    j.add_argument("--reason", required=True)
    j.add_argument("--finding")
    j.add_argument("--task")
    j.add_argument("--supersede")
    ln = add("land", cmd_land)
    ln.add_argument("file")
    ln.add_argument("--pipeline", required=True)
    ln.add_argument("--commit", required=True)
    pl = add("pull", cmd_pull)
    pl.add_argument("--pipeline")
    cs = add("ci-summary", cmd_ci_summary)
    cs.add_argument("--from", dest="from_glob")
    cs.add_argument("--out")
    pg = add("purge", cmd_purge)
    pg.add_argument("--cohort")
    pg.add_argument("--owner-word")
    pg.add_argument("--dry-run", action="store_true")
    pg.add_argument("--registries-done", action="store_true")
    dk = add("drop-keep", cmd_drop_keep)
    dk.add_argument("file")
    dk.add_argument("--reason", required=True)
    sk = add("split-keep", cmd_split_keep)
    sk.add_argument("old")
    sk.add_argument("--into", required=True)
    sk.add_argument("--shim", action="store_true")
    sk.add_argument("--importers", default="")
    sk.add_argument("--reason", required=True)
    return ap


def main(argv=None, ci=None, today=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    try:
        return args.func(args, Ctx(args.root or ROOT, ci, today))
    except Refusal as exc:
        _say(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
