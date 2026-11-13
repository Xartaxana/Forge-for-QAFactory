"""Tests of tools/test_quarantine.py (TD-15.6a): one table per command, temporary git repositories, CI as a function argument."""
import json
import re
import shutil
import subprocess
import types
from datetime import date
from pathlib import Path

import pytest

import test_quarantine as tq

REPO = Path(__file__).resolve().parent.parent
TODAY = date(2026, 11, 25)
T = "ai-packages/qa-factory/scripts/tests/"
PLUGIN = "ai-packages/qa-factory/.claude-plugin/plugin.json"
ORIG_SCHEDULES = tq._schedules


@pytest.fixture(autouse=True)
def shim(monkeypatch):
    real = tq._pkg_module
    st, ip = real(REPO, "selftest"), real(REPO, "install_paths")        # the real loader, the live package readers
    fake = types.SimpleNamespace(
        test_layers=st.test_layers, TestLayersError=st.TestLayersError, slow_tests=st.slow_tests, SlowTestsError=st.SlowTestsError,
        render_slow_tests=st.render_slow_tests,
        gate_named_files=lambda texts: set(re.findall(r"test_[a-z0-9_]+\.py", " ".join(texts))))
    monkeypatch.setattr(tq, "_pkg_module", lambda root, name: fake if name == "selftest" else ip)
    monkeypatch.setattr(tq, "_schedules", lambda branch: "ok")
    monkeypatch.setattr(tq, "WALKER", _walk_as_listed)          # no real walk in a test: every facet listed in story.json passes, a red_then row carries its mark


def _walk_as_listed(story_id, base):
    story = json.loads((Path(base) / story_id / "story.json").read_text(encoding="utf-8-sig"))
    red = story.get("red_then") if isinstance(story.get("red_then"), dict) else {}
    return [R(f"{story_id}/{w['stage']}/{f}" + (" (red then: 3 rows)" if (w["stage"], f) == (red.get("stage"), red.get("facet")) else ""))
            for w in story.get("walk") or [] for f in w.get("facets") or []]


def R(name, kind="pass"):
    return types.SimpleNamespace(name=name, kind=kind, detail="")


def G(root, *a):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-C", str(root), *a],
                          check=True, capture_output=True, text=True).stdout.strip()


def W(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


GATE_WORDS = ["architecture:", "judgment:", "axes:", "piles-skip:"]


def gate_words(msg):
    """The first words of the last four lines of a prepared message: the package commit-gate lines."""
    return [line.split(" ", 1)[0] for line in msg.rstrip("\n").splitlines()[-4:]]


def head_sha(root):
    """HEAD read from the repository files (a loose ref, written by the commit just made): no git process. Falls back to git."""
    git = Path(root) / ".git"
    try:
        head = (git / "HEAD").read_text().strip()
        if head.startswith("ref: "):
            ref = (git / head[5:]).read_text().strip()
        else:
            ref = head
        if re.fullmatch(r"[0-9a-f]{40}", ref):
            return ref
    except OSError:
        pass
    return G(root, "rev-parse", "HEAD")


def commit(root, msg, **files):
    for rel, text in files.items():
        W(root, rel.replace("__", "/"), text)
    G(root, "add", "-A")
    G(root, "commit", "-q", "--allow-empty", "-m", msg)
    return head_sha(root)


def layers_json(keep=("test_k.py",), quar=("test_q1.py", "test_q2.py"), cohorts=("c1",), entry="0" * 40, pins=None, **extra):
    doc = {"schema_version": 1, "layers": ["scenario", "data_join", "table", "register", "gate_named", "detector"], "enforce_listing": True,
           "keep": {k: {"layer": "table", "why": "x"} for k in keep},
           "quarantine": {q: {"cohort": "c1", "entered": "2026-11-20", "release_at_entry": "0.10.9"} for q in quar},
           "pin_holds": pins or {}, "cohorts": {c: {"entered": "2026-11-20", "release_at_entry": "0.10.9", "commit_at_entry": entry, "phase": 1,
                                                    "replaced_by": {}} for c in cohorts}}
    doc.update(extra)
    return json.dumps(doc, indent=1)


_TPL = {"dir": None, "built": {}}


@pytest.fixture(scope="session", autouse=True)
def _template_dir(tmp_path_factory):
    _TPL["dir"] = tmp_path_factory.mktemp("tpl")


def from_template(key, dest, build):
    """The speed of this file (TD-15 debt 2): `build(root)` makes a git world ONCE per session in a template folder; a case gets a copy of it
    at `dest` (a plain folder copy, no git call), so every case stays independent and none builds its own repository. Returns what build returned."""
    if key not in _TPL["built"]:
        root = _TPL["dir"] / ("t%d" % len(_TPL["built"]))
        root.mkdir()
        _TPL["built"][key] = (root, build(root))
    root, out = _TPL["built"][key]
    shutil.copytree(root, dest)
    return out


def _build_repo(root, versions=()):
    G(root, "init", "-q")
    for n in ("test_k.py", "test_q1.py", "test_q2.py"):
        W(root, T + n, f"# {n}\n")
    W(root, PLUGIN, json.dumps({"version": "0.10.9"}))
    entry = commit(root, "base")
    for v in versions:
        commit(root, "release " + v, **{PLUGIN.replace("/", "__"): json.dumps({"version": v})})
    return entry


def repo(tmp_path, versions=()):
    root = tmp_path / "r"
    return root, from_template(("repo", tuple(versions)), root, lambda r: _build_repo(r, versions))


# --- R1-R6, releases ------------------------------------------------------------------------------------------------

def run_row(pipe, ver="0.12.0", complete=True, sha=None, **files):
    return {"kind": "run", "pipeline": pipe, "source": "schedule", "created_at": "2026-11-24T03:00:00Z", "sha": sha, "package_version": ver,
            "complete": complete, "files": files}


def red(*fails):
    return {"status": "red", "fails": list(fails), "seconds": 1}


def verdict(file="test_q1.py", sig=("a",), pipe=1, v="stale", **kw):
    return dict({"ts": "2026-11-24T10:00:00", "file": file, "signature": list(sig), "pipeline": pipe, "verdict": v, "by": "opus",
                 "reason": "r", "finding": "f.md" if v == "real_catch" else None, "task": None}, **kw)


def apply(root, entry, head, runs=(), verdicts=(), pulls=(), cohort0=False, config=True, **lk):
    W(root, "plans/test-quarantine/watch.jsonl", "".join(json.dumps(dict(r, sha=r.get("sha") or head)) + "\n" for r in (*runs, *pulls)))
    W(root, "plans/test-quarantine/verdicts.jsonl", "".join(json.dumps(v) + "\n" for v in verdicts))
    cfg = Path(root, tq.CONFIG_REL)
    cfg.unlink(missing_ok=True)
    if config:
        W(root, tq.CONFIG_REL, json.dumps({"branch": "br", "max_gap_days": 4}))
    W(root, T + "test_k.py", lk.pop("kept_text", "# k\n"))
    W(root, tq.LAYERS_REL, layers_json(entry=entry, cohorts=("c1", "c0") if cohort0 else ("c1",), **lk))


G1 = {"test_q1.py": red("a"), "test_q2.py": {"status": "green"}}
GREEN = {"test_q1.py": {"status": "green"}, "test_q2.py": {"status": "green"}}
V2 = ("0.11.0", "0.12.0")
# id: (versions, runs, verdicts, kept file text, failing rules)
RULES = {
    "ready": (V2, [run_row(1, **G1)], [verdict()], None, set()),
    "r2-zero-releases": ((), [run_row(1, "0.10.9", **GREEN)], [], None, {"R2"}),
    "r2-one-release": (("0.11.0",), [run_row(1, "0.11.0", **GREEN)], [], None, {"R2"}),
    "r2-rollback-not-a-release": (("0.11.0", "0.10.5", "0.10.7"), [run_row(1, "0.11.0", **GREEN)], [], None, {"R2"}),
    "r2-rollback-then-two": (("0.11.0", "0.10.5", "0.12.0"), [run_row(1, **GREEN)], [], None, set()),
    "r2-only-incomplete": (V2, [run_row(1, complete=False, **GREEN)], [], None, {"R2"}),
    "r2-run-below-R2": (V2, [run_row(1, "0.11.0", **GREEN)], [], None, {"R2"}),
    "r2-zero-file-run": (V2, [run_row(1)], [], None, {"R2"}),
    "r3-unexamined": (V2, [run_row(1, **G1)], [], None, {"R3"}),
    "r3-new-name": (V2, [run_row(1, **{"test_q1.py": red("a", "b")})], [verdict()], None, {"R3"}),
    "r4-conflict": (V2, [run_row(1, **G1)], [verdict(), verdict(v="flaky")], None, {"R4"}),
    "r4-identical-is-one": (V2, [run_row(1, **G1)], [verdict(), verdict()], None, set()),
    "r4-superseded": (V2, [run_row(1, **G1)], [verdict(v="flaky"), verdict(supersede="why")], None, set()),
    "r5-catch-not-landed": (V2, [run_row(1, **G1)], [verdict(v="real_catch")], None, {"R5"}),
    "r5-catch-landed": (V2, [run_row(1, **G1)], [verdict(v="real_catch"), {"kind": "land", "file": "test_q1.py", "pipeline": 1, "commit": "x"}],
                        None, set()),
    "r6-kept-imports-quarantined": (V2, [run_row(1, **GREEN)], [], "import test_q1\n", {"R6"}),
}


@pytest.fixture(scope="module")
def hists(tmp_path_factory):
    made = {}

    def get(versions):
        if versions not in made:
            made[versions] = repo(tmp_path_factory.mktemp("h"), versions) + (None,)
        root, entry, _ = made[versions]
        return root, entry, G(root, "rev-parse", "HEAD")
    return get


@pytest.mark.parametrize("case", RULES)
def test_rules_table(hists, case):
    versions, runs, verdicts, kept, failing = RULES[case]
    root, entry, head = hists(versions)
    apply(root, entry, head, runs, verdicts, kept_text=kept or "# k\n")
    data = tq.status_data(root, TODAY)
    c = data["cohorts"][0]
    assert not c.get("unknown"), c
    assert {rid for rid, ok, _ in c["rules"] if not ok} == failing
    assert c["ready"] == (not failing)


def test_rules_zero_rows_and_unknowns(hists):
    root, entry, head = hists(V2)
    apply(root, entry, head, [run_row(1, **GREEN)], cohort0=True)
    c0 = [c for c in tq.status_data(root, TODAY)["cohorts"] if c["id"] == "c0"][0]
    assert ("R1", False, "0 files in the cohort") in c0["rules"] and not c0["ready"]
    sfx, entry2, head2 = hists(("0.11.0", "0.12.0-rc1"))                       # a suffix: unknown, never READY (FR-59)
    apply(sfx, entry2, head2, [run_row(1, **GREEN)])
    assert "not N.N.N" in tq.status_data(sfx, TODAY)["cohorts"][0]["unknown"]
    apply(root, entry, head, [run_row(1, **GREEN)], config=False)
    assert "config.json" in tq.status_data(root, TODAY)["unknown"]
    apply(root, entry, head, [run_row(1, **GREEN)])
    W(root, tq.WATCH_REL, "{broken\n")
    assert "watch.jsonl" in tq.status_data(root, TODAY)["unknown"]


def test_signature_and_releases(hists):
    assert tq.signature({"status": "red", "fails": ["b", "a"]}) == ("a", "b")
    assert tq.signature({"status": "red", "fails": [], "crash": "ValueError: boom"}) == ("crash:ValueError",)
    assert [tq.signature({"status": s}) for s in ("timeout", "ran_nothing", "missing", "green")] == [("timeout",), ("ran_nothing",), ("missing",), ()]
    root, entry, head = hists(("0.11.0", "0.10.5", "0.12.0"))
    assert tq.releases(root, {"release_at_entry": "0.10.9", "commit_at_entry": entry}) == ["0.11.0", "0.12.0"]


COVER = {
    "stale-covers-subset": (("a",), [verdict(sig=("a", "b"))], True),
    "new-name-not-covered": (("a", "c"), [verdict(sig=("a", "b"))], False),
    "real-catch-covers": (("a",), [verdict(v="real_catch")], True),
    "flaky-without-green": (("a",), [verdict(v="flaky")], False),
    "other-file": (("a",), [verdict(file="test_q2.py")], False),
}


@pytest.mark.parametrize("case", COVER)
def test_covered_table(case):
    sig, verdicts, want = COVER[case]
    watch = [{"pipeline": 1, "sha": "s1", "files": {"test_q1.py": red("a")}}]
    assert tq.covered({"file": "test_q1.py", "signature": sig, "pipeline": 1}, verdicts, watch) is want
    watch.append({"pipeline": 2, "sha": "s1", "files": {"test_q1.py": {"status": "green"}}})   # green on the same sha: flaky now covers
    assert tq.covered({"file": "test_q1.py", "signature": sig, "pipeline": 1}, verdicts, watch) is (want or case == "flaky-without-green")


JUDGE = {   # file, flags, setup, exit, text
    "stale": ("test_q1.py", ["--verdict", "stale"], None, 0, "recorded"),
    "duplicate-without-supersede": ("test_q1.py", ["--verdict", "stale"], "twice", 1, "already exists"),
    "supersede": ("test_q1.py", ["--verdict", "real_catch", "--finding", "f.md", "--supersede", "why"], "twice", 0, "recorded"),
    "real-catch-without-finding": ("test_q1.py", ["--verdict", "real_catch"], None, 1, "needs --finding"),
    "flaky-without-pair": ("test_q1.py", ["--verdict", "flaky"], None, 1, "same sha"),
    "flaky-with-pair": ("test_q1.py", ["--verdict", "flaky"], "pair", 0, "recorded"),
    "green-file": ("test_q2.py", ["--verdict", "stale"], None, 1, "no red observation"),
}


@pytest.mark.parametrize("case", JUDGE)
def test_judge_table(tmp_path, capsys, case):
    f, flags, setup, rc, text = JUDGE[case]
    rows = [run_row(1, sha="s1", **G1)] + ([run_row(2, sha="s1", **GREEN)] if setup == "pair" else [])
    W(tmp_path, tq.WATCH_REL, "".join(json.dumps(r) + "\n" for r in rows))
    argv = ["judge", f, "--root", str(tmp_path), "--pipeline", "1", "--by", "opus", "--reason", "r"]
    if setup == "twice":
        assert tq.main(argv + ["--verdict", "stale"]) == 0
    assert tq.main(argv + flags) == rc
    assert text in capsys.readouterr().out


def test_land(tmp_path, capsys):
    root, entry = repo(tmp_path)
    W(root, tq.WATCH_REL, json.dumps(run_row(1, sha=entry, **G1)) + "\n")
    base = ["--root", str(root), "--pipeline", "1"]
    assert tq.main(["land", "test_q1.py", *base, "--commit", entry]) == 1                       # no real_catch yet
    assert tq.main(["judge", "test_q1.py", *base, "--verdict", "real_catch", "--finding", "f.md", "--by", "opus", "--reason", "r"]) == 0
    assert tq.main(["land", "test_q1.py", *base, "--commit", "deadbeef"]) == 1                  # not a commit of this clone
    assert tq.main(["land", "test_q1.py", *base, "--commit", entry]) == 0
    assert json.loads(Path(root, tq.VERDICTS_REL).read_text().splitlines()[-1])["kind"] == "land"


# --- status_line ----------------------------------------------------------------------------------------------------

def pull(at="2026-11-24T08:00:00", ci="ok", newest="2026-11-24T03:00:00Z"):
    return {"kind": "pull", "at": at, "ci": ci, "newest_watch_pipeline": 1, "newest_watch_at": newest}


LINES = {
    "waiting": (V2[:1], [run_row(1, "0.11.0", **G1)], [], [pull()], {}, ["releases since: 1 of 2 (0.11.0)", "watch ran 2026-11-24 (1 d ago), pulled 2026-11-24 (1 d ago)",
                                                                           "1 red, 1 unexamined, blind 0 -- delete when: complete watch on the 2nd release"]),
    "ready": (V2, [run_row(1, **G1)], [verdict()], [pull()], {}, ["READY TO DELETE cohort c1 -- 2 files since 2026-11-20", "1 stale, 0 flaky, 0 real catch moved",
                                                                  "purge --cohort c1 --owner-word"]),
    "not-pulled": (V2[:1], [run_row(1, "0.11.0", **GREEN)], [], [pull(at="2026-11-18T08:00:00")], {},
                   ["pulled 2026-11-18 (7 d ago) -- run: python tools/test_quarantine.py pull"]),
    "never-pulled": (V2[:1], [], [], [], {}, ["no watch run yet (entered 5 d ago)", "never pulled -- run: python tools/test_quarantine.py pull"]),
    "pull-unreachable": (V2[:1], [], [], [pull(ci="unreachable")], {}, ["last pull 2026-11-24 could not reach CI (unreachable)"]),
    "incomplete": (V2[:1], [run_row(i, "0.11.0", complete=False, **GREEN) for i in (1, 2, 3)], [], [pull()], {}, ["last 3 watch runs incomplete"]),
    "release-without-run": (V2, [run_row(1, "0.11.0", **GREEN)], [], [pull()], {}, ["release 0.12.0 has no complete watch run yet -- start it: web pipeline with QUARANTINE_WATCH=1 on br"]),
    "alert-catch": (V2, [run_row(1, **G1)], [verdict(v="real_catch")], [pull()], {}, ["TEST QUARANTINE ALERT: real catch 2026-11-24 -- test_q1.py: r (finding f.md)"]),
    "alert-watch-silent": (V2[:1], [], [], [pull(at="2026-11-30T08:00:00", newest="2026-11-20T03:00:00Z")], {},
                           ["ALERT: the watch has not run on CI for 10 d (last 2026-11-20, as of pull 2026-11-30)"]),
    "unknown-no-config": (V2[:1], [], [], [], {"config": False}, ["TEST QUARANTINE: status unknown (plans/test-quarantine/config.json is missing"]),
}


@pytest.mark.parametrize("case", LINES)
def test_status_line_table(hists, case):
    versions, runs, verdicts, pulls, kw, tokens = LINES[case]
    root, entry, head = hists(versions)
    apply(root, entry, head, runs, verdicts, pulls, **kw)
    text = "\n".join(tq.status_line(root, TODAY))
    for tok in tokens:
        assert tok in text


def test_status_line_empty_worlds_and_duplicates(hists, tmp_path):
    root, entry, head = hists(V2)
    apply(root, entry, head, [run_row(1, **G1), run_row(1, **G1)], [verdict(), verdict()])
    assert len(tq.status_data(root, TODAY)["cohorts"][0]["observations"]) == 1
    apply(root, entry, head, quar=())                                                        # layers file, empty quarantine
    assert tq.status_line(root, TODAY) == [] and tq.main(["status", "--root", str(root)]) == 0
    Path(root, tq.LAYERS_REL).unlink()                                                       # no layers file: nothing printed
    assert tq.status_line(root, TODAY) == []


# --- enter -----------------------------------------------------------------------------------------------------------

REQUIRED = ["S1", "gateA.words"]


class FakeCI:
    def __init__(self, sha, pool, report):
        self.sha, self.pool, self.report = sha, pool, report
        self.variables = {"REDUNDANCY_SCOPE": "keep", "TEST_REDUNDANCY": "1"}       # what the coverage pipeline was started with

    def pipeline_sha(self, pid):
        return self.sha

    def pipeline_variables(self, pid):
        if isinstance(self.variables, Exception):
            raise self.variables
        return self.variables

    def artifact(self, pid, job, path):
        if job == tq.SELFTEST_JOB and int(pid) in self.pool:
            return self.pool[int(pid)]
        if job == tq.COVERAGE_JOB and self.report is not None:
            return self.report
        raise tq.CIError("missing")

    def recent_pipelines(self, branch):
        return list(self.pool)


def passing(*names, fail=()):
    return "".join(f"{'FAIL' if n in fail else 'PASS'} tests: scripts/tests/{n}  1.0s\n" for n in names)


def story(synthetic=True, facets=(("S1", "accepted"), ("gateA", "decision"))):
    return json.dumps({"id": "x", "synthetic": synthetic, "walk": [{"stage": s, "facets": [f]} for s, f in facets]})


def enter_world(tmp_path):
    root = tmp_path / "e"
    head = from_template("enter", root, _build_enter)
    pool = {100: passing(*ENTER_KEEP, "test_old1.py", "test_old2.py", fail=("test_old1.py",)),
            99: passing("test_old1.py"), 98: passing("test_old1.py", fail=("test_old1.py",))}
    return root, FakeCI(head, pool, "- product lines covered: 900; by ok files: 5\nproduct lines total: 1200\n")


ENTER_KEEP = ["test_scenario_a.py", "test_scenario_b.py", "test_scenario_c.py", "test_gate.py"]


def _build_enter(root):
    G(root, "init", "-q")
    keep = ENTER_KEEP
    for n in (*keep, "test_old1.py", "test_old2.py"):
        W(root, T + n, "import os\n")
    for s in "abc":
        W(root, T + f"fixtures/stories/{s}/story.json", story())
    doc = json.loads(layers_json(keep=keep, quar=(), cohorts=(), enforce_listing=False, story_coverage_required=REQUIRED))
    doc["keep"].update({n: {"layer": "scenario", "why": "x"} for n in keep[:3]})
    W(root, tq.LAYERS_REL, json.dumps(doc))
    W(root, PLUGIN, json.dumps({"version": "0.10.9"}))
    W(root, tq.CONFIG_REL, json.dumps({"branch": "br", "max_gap_days": 4}))
    W(root, "plans/builder-rules.md", "the gate test_gate.py is run\n")
    W(root, tq.SLOW_REL, json.dumps({"measured_on": "x", "source": "y", "thresholds": {"slow_over_s": 10, "fast_under_s": 5}, "max_drift": 5,
                                     "files": {"test_old1.py": 12.4, "test_gate.py": 30}}))
    return commit(root, "base")


def _no_layers(root, ci, mp):
    Path(root, tq.LAYERS_REL).unlink()


def _no_config(root, ci, mp):
    Path(root, tq.CONFIG_REL).unlink()


def _stories(root, ci, mp):
    W(root, T + "fixtures/stories/c/story.json", story(synthetic=False))


def _coverage_gap(root, ci, mp):
    for s in "abc":
        W(root, T + f"fixtures/stories/{s}/story.json", story(facets=(("S1", "accepted"),)))


def _gate_names_moving(root, ci, mp):
    W(root, "plans/builder-rules.md", "the gate test_old1.py is run\n")


def _other_sha(root, ci, mp):
    ci.sha = "f" * 40


def _keep_fail(root, ci, mp):
    ci.pool[100] = passing("test_scenario_a.py", "test_scenario_b.py", "test_scenario_c.py", "test_gate.py", fail=("test_gate.py",))


def _pin(root, ci, mp):
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    doc["pin_holds"] = {"test_old2.py": "role pin"}
    W(root, tq.LAYERS_REL, json.dumps(doc))


def _all_pinned(root, ci, mp):
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    doc["pin_holds"] = {"test_old1.py": "role pin", "test_old2.py": "role pin"}
    W(root, tq.LAYERS_REL, json.dumps(doc))


def _sched(value):
    return lambda root, ci, mp: mp.setattr(tq, "_schedules", lambda branch: value)


def _no_report(root, ci, mp):
    ci.report = None


def _other_keep(root, ci, mp):
    mp.setattr(tq, "_blob_sections", lambda r, rev: {"keep": {"test_other.py": {}}, "quarantine": {}, "pin_holds": {}, "cohorts": {}})


def _two_pipelines(root, ci, mp):
    del ci.pool[98]


def _scope(variables, report=None):
    def mutate(root, ci, mp):
        ci.variables = variables
        if report is not None:
            ci.report = report
    return mutate


SCOPE_DOOR = "--var TEST_REDUNDANCY=1 --var REDUNDANCY_SCOPE=keep"
REPORT = "- product lines covered: 900; by ok files: 5\nproduct lines total: 1200\n"
ENTER = {
    "f-scope-full": (_scope({"REDUNDANCY_SCOPE": "full"}), "ran with scope 'full', not keep"),
    "f-scope-unset": (_scope({"TEST_REDUNDANCY": "1"}), "ran with scope 'full', not keep"),
    "f-scope-unknown-variables-unreadable": (_scope(tq.CIError("token_refused")), "could not be established"),
    "f-scope-unknown-names-the-door": (_scope(tq.CIError("unreachable")), SCOPE_DOOR),
    "f-scope-variable-beats-a-header-line": (_scope({"REDUNDANCY_SCOPE": "full"}, "- scope: keep\n" + REPORT), "ran with scope 'full', not keep"),
    "c1-no-layers": (_no_layers, "keep rows"), "c1-config-missing": (_no_config, "config.json"),
    "c2-story-not-synthetic": (_stories, "need 3 synthetic scenario stories"), "c2-coverage": (_coverage_gap, "missing coverage: gateA.words"),
    "c3-carrier-names-moving": (_gate_names_moving, "a carrier names files that are not keep rows: test_old1.py"),
    "c4-not-head": (_other_sha, "did not run on HEAD"), "c4-keep-fail": (_keep_fail, "no PASS line"),
    "c5-all-pinned": (_all_pinned, "no test file is outside keep, quarantine and pin_holds"),
    "c6-schedule-unknown": (_sched("unknown"), "the watch schedule cannot be confirmed"),
    "c6-schedule-missing": (_sched("missing"), 'cron "0 3 * * 1,4", branch br, variable QUARANTINE_WATCH=1'),
    "c7-no-report": (_no_report, "no coverage measurement"), "c7-other-keep-set": (_other_keep, "different keep set"),
    "c8-two-pipelines": (_two_pipelines, "run the full tier 1 more times"),
}


@pytest.mark.parametrize("case", ENTER)
def test_enter_refusals_table(tmp_path, monkeypatch, capsys, case):
    root, ci = enter_world(tmp_path)
    mutate, text = ENTER[case]
    mutate(root, ci, monkeypatch)
    before = Path(root, tq.LAYERS_REL).read_text() if Path(root, tq.LAYERS_REL).is_file() else None
    assert tq.main(["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101"], ci=ci) == 1
    assert text in capsys.readouterr().out
    assert (Path(root, tq.LAYERS_REL).read_text() if before is not None else None) == before     # a refusal writes nothing


def test_enter_default_schedule_stub_refuses(tmp_path, monkeypatch, capsys):
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_schedules", ORIG_SCHEDULES)                                      # the real reader, CI cannot be read: "unknown"

    def no_token(*a, **k):
        raise tq.CIError("token_refused")
    monkeypatch.setattr(tq, "GitlabCI", no_token)
    assert tq.main(["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101"], ci=ci) == 1
    assert "the watch schedule cannot be confirmed" in capsys.readouterr().out


OWNER = "the owner, 2026-11-11: the schedule comes later in the new repository"
ENTER_ARGV = ["--pipeline", "100", "--coverage-pipeline", "101"]


def test_enter_owner_word_passes_the_schedule_gate_and_is_recorded(tmp_path, monkeypatch, capsys):          # K
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_schedules", lambda branch: "unknown")
    argv = ["enter", "--root", str(root), *ENTER_ARGV]
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(argv, ci=ci) == 1                                                            # without the word: refused, and the door names it
    assert "--owner-word" in capsys.readouterr().out
    assert tq.main(argv + ["--owner-word", OWNER, "--dry-run"], ci=ci) == 0                      # dry run: the same line, nothing written
    assert "schedule not confirmed -- passed by the owner's word: " + OWNER in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()
    assert tq.main(argv + ["--owner-word", "  " + OWNER + "  "], ci=ci) == 0
    assert "schedule not confirmed -- passed by the owner's word: " + OWNER in capsys.readouterr().out
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())
    cohort = after["cohorts"]["100"]
    assert (cohort["owner_word"], cohort["owner_word_gates"]) == (OWNER, ["schedule"]) and "schedule_owner_word" not in cohort
    assert not {"keep_fail_at_entry", "keep_absent_at_entry"} & set(cohort) and set(after["quarantine"]) == {"test_old1.py", "test_old2.py"}
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert "schedule not confirmed -- passed by the owner's word: " + OWNER in msg and gate_words(msg) == GATE_WORDS


class ShardCI(FakeCI):
    """FakeCI where the report artifact of `no_report` pipelines is missing and the shard artifacts come from `shards` {(pid, i): text}
    (an absent key is a missing artifact, a CIError value is raised); every artifact call is logged in `calls`."""

    def __init__(self, base, no_report=(), shards=None):
        super().__init__(base.sha, base.pool, base.report)
        self.no_report, self.shards, self.calls = set(no_report), shards or {}, []

    def artifact(self, pid, job, path):
        self.calls.append((int(pid), job, path))
        if job.startswith("package-full "):
            got = self.shards.get((int(pid), int(job.split()[1][0])))
            if isinstance(got, Exception):
                raise got
            if got is None:
                raise tq.CIError("missing")
            return got
        if job == tq.SELFTEST_JOB and int(pid) in self.no_report:
            raise tq.CIError("missing")
        return super().artifact(pid, job, path)


def _split_shards(text, pid=100):
    lines = text.splitlines(keepends=True)
    return {(pid, 1): "".join(lines[:3]), (pid, 2): "".join(lines[3:])}


def test_selftext_report_present_never_requests_the_shards(tmp_path, capsys):          # TD-15
    root, base = enter_world(tmp_path)
    ci = ShardCI(base, shards=_split_shards(base.pool[100]))
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    assert ci.calls and not [c for c in ci.calls if c[1].startswith("package-full ")]


def test_selftext_report_missing_reads_both_shards_joined_and_parsed_across_both(tmp_path, capsys):          # TD-15
    root, base = enter_world(tmp_path)
    ci = ShardCI(base, no_report=[100], shards=_split_shards(base.pool[100]))
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    assert [c[1:] for c in ci.calls if c[0] == 100 and c[1].startswith("package-full ")] == [
        ("package-full 1/2", "ci-out/selftest-shard-1-of-2.txt"), ("package-full 2/2", "ci-out/selftest-shard-2-of-2.txt")]
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())
    assert set(after["quarantine"]) == {"test_old1.py", "test_old2.py"}                  # test_old2.py is on shard 2 only


def test_selftext_report_and_one_shard_missing_refuses_naming_the_shard(tmp_path, capsys):          # TD-15, FR-41
    root, base = enter_world(tmp_path)
    shards = _split_shards(base.pool[100])
    del shards[(100, 2)]
    ci = ShardCI(base, no_report=[100], shards=shards)
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 1
    out = capsys.readouterr().out
    assert "pipeline 100 has no ci-out/selftest.txt (package-full-report) and no ci-out/selftest-shard-2-of-2.txt (package-full 2/2)" in out
    assert Path(root, tq.LAYERS_REL).read_text() == before


def test_selftext_report_missing_and_shards_unreachable_keeps_the_ci_said_refusal(tmp_path, capsys):          # TD-15
    root, base = enter_world(tmp_path)
    ci = ShardCI(base, no_report=[100], shards={(100, 1): tq.CIError("unreachable")})
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 1
    assert "CI said unreachable" in capsys.readouterr().out


def test_baseline_reads_shards_for_a_report_less_run_and_skips_one_with_a_missing_shard():          # TD-15
    base = FakeCI("sha", {100: "", 99: "", 98: "", 97: passing("test_old1.py")}, None)
    shards = {(99, 1): passing("test_old1.py"), (99, 2): passing("test_old1.py", fail=("test_old1.py",)),
              (98, 1): passing("test_x.py", fail=("test_x.py",))}                          # run 98 has no shard 2: skipped whole
    ci = ShardCI(base, no_report=[99, 98], shards=shards)
    ctx = types.SimpleNamespace(ci=ci)
    red, flaky = tq._baseline(ctx, types.SimpleNamespace(pipeline=100), {"branch": "br"}, passing("test_old1.py"), {"test_old1.py", "test_x.py"})
    assert (red, flaky) == ({"test_old1.py"}, {"test_old1.py"})


def _earlier_pipeline(root, ci):
    """The pipelines ran on the current commit; then HEAD moves on by one commit. Returns (pipeline sha, new HEAD)."""
    earlier = ci.sha
    W(root, "note.txt", "one more commit\n")
    return earlier, commit(root, "one more commit")


def test_enter_owner_word_passes_a_pipeline_off_head_and_records_its_sha(tmp_path, capsys):          # K, TD-15
    root, ci = enter_world(tmp_path)
    earlier, new_head = _earlier_pipeline(root, ci)
    argv = ["enter", "--root", str(root), *ENTER_ARGV]
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(argv, ci=ci) == 1                                                            # no word: refused, the door names the option
    out = capsys.readouterr().out
    assert "did not run on HEAD" in out and "--owner-word" in out
    line = "pipeline 100 ran on %s, not on HEAD %s -- passed by the owner's word: %s" % (earlier[:9], new_head[:9], OWNER)
    assert tq.main(argv + ["--owner-word", OWNER, "--dry-run"], ci=ci) == 0                      # dry run: the line, nothing written
    assert line in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()
    assert tq.main(argv + ["--owner-word", OWNER], ci=ci) == 0
    cohort = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert (cohort["owner_word"], cohort["owner_word_gates"], cohort["pipeline_sha"]) == (OWNER, ["head"], earlier)
    assert "coverage_measured_on" not in cohort
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert line in msg and gate_words(msg) == GATE_WORDS


def test_enter_owner_word_passes_the_head_gate_with_the_schedule_gate_sorted(tmp_path, monkeypatch, capsys):          # K, TD-15
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_schedules", lambda branch: "missing")
    _earlier_pipeline(root, ci)
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    assert json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]["owner_word_gates"] == ["head", "schedule"]


def test_enter_owner_word_does_not_pass_an_unreadable_pipeline_commit(tmp_path, capsys):          # K, TD-15, FR-41
    root, ci = enter_world(tmp_path)
    for bad in ("", "f" * 40):
        ci.sha = bad
        assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 1
        assert "did not run on HEAD" in capsys.readouterr().out
    assert "owner_word" not in Path(root, tq.LAYERS_REL).read_text()


def test_enter_owner_word_does_not_pass_a_red_story_on_a_pipeline_off_head(tmp_path, capsys):          # K, TD-15
    root, ci = enter_world(tmp_path)
    _earlier_pipeline(root, ci)
    ci.pool[100] = passing(*ENTER_KEEP, fail=("test_scenario_a.py",))
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 1
    assert "need 3 synthetic scenario stories" in capsys.readouterr().out
    assert "owner_word" not in Path(root, tq.LAYERS_REL).read_text()


def test_enter_owner_word_passes_a_coverage_keep_set_measured_earlier(tmp_path, monkeypatch, capsys):          # K, TD-15
    root, ci = enter_world(tmp_path)
    _other_keep(root, ci, monkeypatch)
    argv = ["enter", "--root", str(root), *ENTER_ARGV]
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(argv, ci=ci) == 1                                                            # no word: refused, the door names the option
    out = capsys.readouterr().out
    assert "different keep set" in out and "--owner-word" in out
    line = "coverage pipeline 101 measured 1 keep file(s), HEAD has 4 -- passed by the owner's word: " + OWNER
    assert tq.main(argv + ["--owner-word", OWNER, "--dry-run"], ci=ci) == 0
    assert line in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()
    assert tq.main(argv + ["--owner-word", OWNER], ci=ci) == 0
    cohort = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert (cohort["owner_word_gates"], cohort["coverage_measured_on"]) == (["coverage_keep_set"], "101") and "pipeline_sha" not in cohort
    assert line in Path(root, "ci-out/quarantine-enter-msg.txt").read_text()


def test_enter_owner_word_does_not_pass_an_unreadable_coverage_keep_set(tmp_path, monkeypatch, capsys):          # K, TD-15, FR-41
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_blob_sections", lambda r, rev: {"keep": {}, "quarantine": {}, "pin_holds": {}, "cohorts": {}})
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 1
    assert "different keep set" in capsys.readouterr().out


def test_enter_owner_word_is_not_a_pass_for_anything_else_and_not_empty(tmp_path, monkeypatch, capsys):    # K
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_schedules", lambda branch: "missing")
    argv = ["enter", "--root", str(root), *ENTER_ARGV]
    for empty in ("", "   "):
        assert tq.main(argv + ["--owner-word", empty], ci=ci) == 1
        assert "--owner-word needs the owner's words" in capsys.readouterr().out
    ci.pool[100] = passing(*ENTER_KEEP, fail=("test_scenario_a.py",))                             # a red scenario story: still refused with the word
    assert tq.main(argv + ["--owner-word", OWNER], ci=ci) == 1
    assert "need 3 synthetic scenario stories" in capsys.readouterr().out
    assert "owner_word" not in Path(root, tq.LAYERS_REL).read_text()


FAIL_LINE = "keep rows with a FAIL line in pipeline 100 -- passed by the owner's word: " + OWNER + " -- 1 file(s): test_gate.py"
ABSENT_LINE = "keep rows with no line at all (never measured) in pipeline 100 -- passed by the owner's word: " + OWNER + " -- 1 file(s): test_gate.py"


def test_enter_owner_word_passes_a_failing_keep_row_and_records_it_with_its_words(tmp_path, capsys):          # K, B2
    root, ci = enter_world(tmp_path)                                                            # the schedule is confirmed (the shim says "ok")
    argv = ["enter", "--root", str(root), *ENTER_ARGV]
    _keep_fail(root, ci, None)
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(argv, ci=ci) == 1                                                            # no word: refused, the door names the option
    out = capsys.readouterr().out
    assert "no PASS line" in out and "--owner-word" in out
    assert tq.main(argv + ["--owner-word", OWNER, "--dry-run"], ci=ci) == 0                      # dry run: the line, nothing written
    assert FAIL_LINE in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()
    assert tq.main(argv + ["--owner-word", OWNER], ci=ci) == 0
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert after["keep_fail_at_entry"] == ["test_gate.py"] and (after["owner_word"], after["owner_word_gates"]) == (OWNER, ["red_keep"])
    assert not {"keep_absent_at_entry", "schedule_owner_word", "red_keep_at_entry"} & set(after)
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert FAIL_LINE in msg and "schedule not confirmed" not in msg       # the words stand in the message when only this gate was passed


def test_enter_owner_word_lists_an_absent_keep_row_apart_from_a_failing_one(tmp_path, capsys):                 # K, B2c, FR-41
    root, ci = enter_world(tmp_path)
    ci.pool[100] = passing("test_scenario_a.py", "test_scenario_b.py", "test_scenario_c.py")        # test_gate.py has no line at all
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    out = capsys.readouterr().out
    assert ABSENT_LINE in out and "with a FAIL line" not in out
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert after["keep_absent_at_entry"] == ["test_gate.py"] and "keep_fail_at_entry" not in after
    assert ABSENT_LINE in Path(root, "ci-out/quarantine-enter-msg.txt").read_text()


def test_enter_owner_word_keeps_fail_and_absent_rows_in_two_sorted_lists(tmp_path, capsys):                    # K, B2c
    root, ci = enter_world(tmp_path)
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    doc["keep"].update({"test_z_gate.py": {"layer": "table", "why": "x"}, "test_a_gate.py": {"layer": "table", "why": "x"}})
    W(root, tq.LAYERS_REL, json.dumps(doc))
    for n in ("test_z_gate.py", "test_a_gate.py"):
        W(root, T + n, "import os\n")
    ci.sha = commit(root, "two more keep rows")                                                 # the keep set the CI pipelines measured is HEAD's
    ci.pool[100] = passing("test_scenario_a.py", "test_scenario_b.py", "test_scenario_c.py", "test_z_gate.py", fail=("test_z_gate.py",))
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0       # test_gate.py, test_a_gate.py: no line
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert after["keep_fail_at_entry"] == ["test_z_gate.py"] and after["keep_absent_at_entry"] == ["test_a_gate.py", "test_gate.py"]
    out = capsys.readouterr().out
    assert "with a FAIL line in pipeline 100 -- passed by the owner's word: " + OWNER + " -- 1 file(s): test_z_gate.py" in out
    assert "no line at all (never measured) in pipeline 100 -- passed by the owner's word: " + OWNER + " -- 2 file(s): test_a_gate.py, test_gate.py" in out


def test_enter_owner_word_passing_both_gates_records_one_word_and_both_gates(tmp_path, monkeypatch, capsys):   # K, B2b
    root, ci = enter_world(tmp_path)
    monkeypatch.setattr(tq, "_schedules", lambda branch: "missing")
    _keep_fail(root, ci, None)
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())["cohorts"]["100"]
    assert (after["owner_word"], after["owner_word_gates"]) == (OWNER, ["red_keep", "schedule"]) and "schedule_owner_word" not in after
    assert after["keep_fail_at_entry"] == ["test_gate.py"]
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert FAIL_LINE in msg and "schedule not confirmed -- passed by the owner's word: " + OWNER in msg


def test_enter_owner_word_that_passed_no_gate_records_no_owner_word_fields(tmp_path, capsys):                  # K, edge
    root, ci = enter_world(tmp_path)                                                            # keep all PASS, the shim answers "ok"
    assert tq.main(["enter", "--root", str(root), *ENTER_ARGV, "--owner-word", OWNER], ci=ci) == 0
    out = capsys.readouterr().out
    assert "keep rows with" not in out and "schedule not confirmed" not in out
    text = Path(root, tq.LAYERS_REL).read_text()
    assert not any(k in text for k in ("owner_word", "keep_fail_at_entry", "keep_absent_at_entry", "red_keep_at_entry"))


def test_enter_success_dry_run_and_write(tmp_path, capsys):
    root, ci = enter_world(tmp_path)
    argv = ["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101"]
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(argv + ["--dry-run"], ci=ci) == 0 and Path(root, tq.LAYERS_REL).read_text() == before
    out = capsys.readouterr().out
    for tok in ("quarantine enter: 2 files (2 lines) to quarantine, 4 kept (by layer: scenario 3, table 1)", "held by import: 0", "held by pins: 0",
                "slow_tests.json -1 rows", "red at entry: 1, flaky at entry: 1", "canon after the move covers 900 of 1200 lines", "dry run"):
        assert tok in out, tok
    assert tq.main(argv, ci=ci) == 0
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())
    assert after["enforce_listing"] is True and set(after["quarantine"]) == {"test_old1.py", "test_old2.py"} and after["cohorts"]["100"]["phase"] == 1
    row = after["quarantine"]["test_old1.py"]
    assert (row["cohort"], row["red_at_entry"], row["flaky_at_entry"], row["seconds"]) == ("100", True, True, 12.4)
    assert "test_old1.py" not in json.loads(Path(root, tq.SLOW_REL).read_text())["files"]
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert msg.startswith("quarantine-enter: cohort 100") and "covers 900 of 1200 product lines (pipeline 101)" in msg
    assert gate_words(msg) == GATE_WORDS
    assert "git commit -F ci-out/quarantine-enter-msg.txt" in capsys.readouterr().out
    assert tq.main(argv, ci=ci) == 1                                                            # the cohort exists: refused


def test_enter_c5_pin_held_file_stays_in_the_canon(tmp_path, capsys):
    root, ci = enter_world(tmp_path)
    _pin(root, ci, None)                                                                        # test_old2.py is pin-held
    argv = ["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101"]
    assert tq.main(argv, ci=ci) == 0
    out = capsys.readouterr().out
    assert "quarantine enter: 1 files" in out and "held by pins: 1" in out
    after = json.loads(Path(root, tq.LAYERS_REL).read_text())
    assert set(after["quarantine"]) == {"test_old1.py"} and "test_old2.py" in after["pin_holds"]
    assert "held by pins: 1" in Path(root, "ci-out/quarantine-enter-msg.txt").read_text()


def test_enter_keep_and_pin_row_is_not_counted_as_pin_held(tmp_path, capsys):
    root, ci = enter_world(tmp_path)
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    doc["pin_holds"] = {"test_gate.py": "role pin"}
    W(root, tq.LAYERS_REL, json.dumps(doc))
    assert tq.main(["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101", "--dry-run"], ci=ci) == 0
    assert "held by pins: 0" in capsys.readouterr().out


def _build_det(root):
    _build_enter(root)
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    doc["keep"]["test_det.py"] = {"layer": "detector", "why": "x", "named_by": ["a:1"], "replaced_by": None}
    doc["keep"]["test_gate.py"]["layer"] = "gate_named"
    W(root, T + "test_det.py", "x = 1\n")
    W(root, tq.LAYERS_REL, json.dumps(doc))
    return commit(root, "det")


def det_world(tmp_path):
    root = tmp_path / "e"
    sha = from_template("det", root, _build_det)
    pool = {100: passing("test_scenario_a.py", "test_det.py"), 99: passing("test_old1.py"), 98: passing("test_old1.py", fail=("test_old1.py",))}
    return root, FakeCI(sha, pool, "- product lines covered: 900; by ok files: 5\nproduct lines total: 1200\n")


PHASE2 = {
    "a-not-a-detector": (["--phase2", "test_gate.py", "--replaced-by", "test_scenario_a.py"], None, "not a keep row of layer detector"),
    "b-replacement-wrong-layer": (["--phase2", "test_det.py", "--replaced-by", "test_gate.py"], None, "not a keep row of a scenario"),
    "c-carrier-names-it": (["--phase2", "test_det.py", "--replaced-by", "test_scenario_a.py"], "the gate test_det.py is run\n", "a carrier still names test_det.py"),
    "d-pin": (["--phase2", "test_det.py", "--replaced-by", "test_scenario_a.py"], "PIN", "held by a pin"),
    "b-replacement-red": (["--phase2", "test_det.py", "--replaced-by", "test_scenario_b.py"], None, "not green in pipeline 100"),
    "ok": (["--phase2", "test_det.py", "--replaced-by", "test_scenario_a.py"], None, "phase 2: test_det.py -> test_scenario_a.py"),
}


@pytest.mark.parametrize("case", PHASE2)
def test_enter_phase2_table(tmp_path, capsys, case):
    root, ci = det_world(tmp_path)
    flags, extra, text = PHASE2[case]
    if extra == "PIN":
        doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
        doc["pin_holds"] = {"test_det.py": "role pin"}
        W(root, tq.LAYERS_REL, json.dumps(doc))
    elif extra:
        W(root, "plans/builder-rules.md", extra)
    assert tq.main(["enter", "--root", str(root), "--pipeline", "100", *flags], ci=ci) == (0 if case == "ok" else 1)
    assert text in capsys.readouterr().out
    if case == "ok":
        doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
        assert "test_det.py" in doc["quarantine"] and "test_det.py" not in doc["keep"]
        assert list(doc["cohorts"].values())[-1]["replaced_by"] == {"test_det.py": "test_scenario_a.py"}
        msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
        assert msg.startswith("quarantine-enter: phase2 test_det.py -> test_scenario_a.py") and gate_words(msg) == GATE_WORDS


def test_drop_keep_and_held_by_import(tmp_path, capsys):
    root, entry = repo(tmp_path)
    apply(root, entry, entry, kept_text="from test_q1 import x\n")
    assert tq.held_by_import(root) == [("test_k.py", "test_q1.py")]
    argv = ["drop-keep", "test_k.py", "--root", str(root)]
    assert tq.main(argv + ["--reason", " "]) == 1 and tq.main(["drop-keep", "test_zz.py", "--root", str(root), "--reason", "x"]) == 1
    assert tq.main(argv + ["--reason", "dup of a table row"]) == 0 and not Path(root, T + "test_k.py").exists()
    msg = Path(root, "ci-out/keep-drop-msg.txt").read_text()
    assert msg.startswith("keep-drop: test_k.py -- dup of a table row\n") and gate_words(msg) == GATE_WORDS


ROW = {"layer": "detector", "why": "AR-25 proof", "named_by": ["design/state-exits.md:34"], "replaced_by": None, "covers": ["tests/story_step_common.py"]}


def split_world(tmp_path, disk=("test_k_a.py", "test_k_b.py"), old_on_disk=False):
    """A plain folder: a keep section [test_first.py, test_k.py (the full row), test_last.py], one pin row, two quarantine rows."""
    root = tmp_path / "s"
    doc = json.loads(layers_json(keep=("test_first.py", "test_last.py"), pins={"test_pin.py": "role pin"}))
    doc["keep"] = {"test_first.py": {"layer": "table", "why": "x"}, "test_k.py": dict(ROW), "test_last.py": {"layer": "table", "why": "x"}}
    W(root, tq.LAYERS_REL, json.dumps(doc, indent=1) + "\n")
    for n in ("test_pin.py",) + disk + (("test_k.py",) if old_on_disk else ()):
        W(root, T + n, f"# {n}\n")
    return root


SPLIT_REFUSALS = {                  # name: (argv tail after OLD, disk, old on disk, text of the refusal)
    "old-not-a-keep-row": (["test_zz.py", "--into", "test_zz_a.py"], ("test_zz_a.py",), False, "test_zz.py is not a keep row"),
    "old-is-a-quarantine-row": (["test_q1.py", "--into", "test_q1_a.py"], ("test_q1_a.py",), False, "test_q1.py is not a keep row"),
    "old-is-a-pin-row": (["test_pin.py", "--into", "test_pin_a.py"], ("test_pin_a.py",), False, "test_pin.py is not a keep row"),
    "part-is-a-keep-row": (["test_k.py", "--into", "test_k_a.py,test_first.py"], ("test_k_a.py", "test_first.py"), False, "part test_first.py is already a row of keep"),
    "part-is-a-pin-row": (["test_k.py", "--into", "test_k_a.py,test_pin.py"], ("test_k_a.py", "test_pin.py"), False, "part test_pin.py is already a row of pin_holds"),
    "part-not-on-disk": (["test_k.py", "--into", "test_k_a.py,test_k_gone.py"], ("test_k_a.py",), False, "part test_k_gone.py is not on disk"),
    "part-is-quarantined": (["test_k.py", "--into", "test_k_a.py,test_q1.py"], ("test_k_a.py", "test_q1.py"), False, "quarantine name"),
    "part-equals-old": (["test_k.py", "--into", "test_k_a.py,test_k.py"], ("test_k_a.py",), True, "part test_k.py is the old file itself"),
    "part-not-old-stem": (["test_k.py", "--into", "test_k_a.py,test_brand_new.py"], ("test_k_a.py", "test_brand_new.py"), False,
                          "part test_brand_new.py is not named test_k_<topic>.py"),
    "into-empty": (["test_k.py", "--into", ""], (), False, "--into is empty"),
    "into-empty-name": (["test_k.py", "--into", "test_k_a.py,,test_k_b.py"], ("test_k_a.py", "test_k_b.py"), False, "--into is empty"),
    "into-duplicate": (["test_k.py", "--into", "test_k_a.py,test_k_a.py"], ("test_k_a.py",), False, "names a part twice"),
    "reason-blank": (["test_k.py", "--into", "test_k_a.py", "--reason", "  "], ("test_k_a.py",), False, "the reason is empty"),
    "no-shim-old-on-disk": (["test_k.py", "--into", "test_k_a.py"], ("test_k_a.py",), True, "delete the old file in this change or pass --shim"),
    "shim-old-missing": (["test_k.py", "--into", "test_k_a.py", "--shim"], ("test_k_a.py",), False, "not on disk"),
}


@pytest.mark.parametrize("case", SPLIT_REFUSALS)
def test_split_keep_refusals_write_nothing(tmp_path, capsys, case):
    tail, disk, old_on_disk, text = SPLIT_REFUSALS[case]
    root = split_world(tmp_path, disk, old_on_disk)
    layers_before = Path(root, tq.LAYERS_REL).read_bytes()
    argv = ["split-keep", tail[0], "--root", str(root)] + tail[1:] + ([] if "--reason" in tail else ["--reason", "why"])
    assert tq.main(argv) == 1
    out = capsys.readouterr().out
    assert text in out and out.startswith("split-keep refused:")
    assert Path(root, tq.LAYERS_REL).read_bytes() == layers_before and not Path(root, "ci-out").exists()


def test_split_keep_without_shim_inherits_removes_old_and_writes_the_message(tmp_path, capsys):
    root = split_world(tmp_path)
    assert tq.main(["split-keep", "test_k.py", "--into", "test_k_a.py,test_k_b.py", "--reason", "slow file", "--root", str(root)]) == 0
    keep = json.loads(Path(root, tq.LAYERS_REL).read_text())["keep"]
    assert list(keep) == ["test_first.py", "test_k_a.py", "test_k_b.py", "test_last.py"]                  # in the old row's place
    for p in ("test_k_a.py", "test_k_b.py"):
        assert keep[p] == dict(ROW, why="AR-25 proof (part of test_k.py split, TD-11c)") and list(keep[p]) == list(ROW)
    msg = Path(root, "ci-out/keep-split-msg.txt").read_text()
    assert msg.startswith("keep-split: test_k.py -> test_k_a.py, test_k_b.py -- slow file\n") and gate_words(msg) == GATE_WORDS
    assert tq.main(["split-keep", "test_k.py", "--into", "test_k_a.py", "--reason", "again", "--root", str(root)]) == 1      # the row is gone


def test_split_keep_with_shim_rewrites_the_old_row(tmp_path, capsys):
    root = split_world(tmp_path, old_on_disk=True)
    assert tq.main(["split-keep", "test_k.py", "--into", "test_k_a.py,test_k_b.py", "--shim", "--importers", "test_x.py,test_y.py",
                    "--reason", "importers", "--root", str(root)]) == 0
    keep = json.loads(Path(root, tq.LAYERS_REL).read_text())["keep"]
    assert list(keep) == ["test_first.py", "test_k.py", "test_k_a.py", "test_k_b.py", "test_last.py"]
    # the pinned value: the helper as T-3 writes it, tests/<stem without test_>_common.py; named_by empty (E4)
    assert keep["test_k.py"] == dict(ROW, layer="data_join", covers=["tests/k_common.py"], named_by=[],
                                     why="split shim: re-exports for test_x.py, test_y.py; checks live in test_k_a.py, test_k_b.py")
    assert keep["test_k_a.py"]["covers"] == ROW["covers"] and keep["test_k_b.py"]["layer"] == "detector"


def test_split_keep_adds_the_common_file_to_part_covers_when_on_disk(tmp_path, capsys):
    root = split_world(tmp_path)
    W(root, T + "k_common.py", "# helper\n")
    assert tq.main(["split-keep", "test_k.py", "--into", "test_k_a.py,test_k_b.py", "--reason", "slow", "--root", str(root)]) == 0
    keep = json.loads(Path(root, tq.LAYERS_REL).read_text())["keep"]
    assert keep["test_k_a.py"]["covers"] == ROW["covers"] + ["tests/k_common.py"] == keep["test_k_b.py"]["covers"]


# --- split-keep door of K5 --------------------------------------------------------------------------------------------

LINE = "split\n\nkeep-split: test_k.py -> test_k_a.py, test_k_b.py -- slow"
SHIM_ROW = {"layer": "data_join", "why": "split shim: re-exports for importers; checks live in parts", "named_by": [], "covers": ["tests/k_common.py"]}


def _split_commit(msg, parts=("test_k_a.py", "test_k_b.py"), pop=True, add=True, old_file=False, shim=False, layer="table", on_disk=True):
    """One commit: the part files and rows; the old row removed (pop) or rewritten as a shim; the old file deleted unless old_file."""
    def run(root):
        for p in parts if on_disk else ():
            W(root, T + p, f"# {p}\n")
        if not old_file:
            G(root, "rm", "-q", T + "test_k.py")

        def mutate(d):
            if shim:
                d["keep"]["test_k.py"] = dict(SHIM_ROW)
            elif pop:
                d["keep"].pop("test_k.py")
            for p in parts if add else parts[:1]:
                d["keep"][p] = {"layer": layer, "why": "x"}
        relayers(root, msg, mutate)
    return run


SPLIT_CHECK = {
    "keep-split-accepted": (_split_commit(LINE), 0, "0 violation"),
    "keep-split-shim-accepted": (_split_commit(LINE, old_file=True, shim=True), 0, "0 violation"),
    "keep-split-part-not-in-keep": (_split_commit(LINE, add=False), 1, "names part test_k_b.py which is not a keep row added by this commit"),
    "keep-split-part-file-not-in-tree": (_split_commit(LINE, on_disk=False), 1, "part test_k_a.py, which is not in this commit's tree"),
    "keep-split-part-is-an-older-row": (_split_commit("split\n\nkeep-split: test_k.py -> test_k_a.py, test_last.py -- x", parts=("test_k_a.py",)), 1,
                                        "part test_last.py which is not a keep row added by this commit"),
    "keep-split-part-not-old-stem": (_split_commit("split\n\nkeep-split: test_k.py -> test_k_a.py, test_other.py -- x",
                                                   parts=("test_k_a.py", "test_other.py")), 1, "part test_other.py, not named test_k_<topic>.py"),
    "keep-split-part-layer-differs": (_split_commit(LINE, layer="scenario"), 1, "part test_k_a.py has layer scenario, the old row had table"),
    "keep-split-old-row-removed-file-stays-no-shim": (_split_commit(LINE, old_file=True), 1,
                                                      "whose row was removed while the file is still in this commit's tree"),
    "keep-split-old-file-stays-row-not-a-shim": (_split_commit(LINE, old_file=True, pop=False), 1, "its row is not a shim row"),
    "keep-split-old-file-gone-row-stays": (_split_commit(LINE, pop=False), 1, "whose file is gone but whose row stays"),
    "keep-split-old-not-a-keep-row": (_split_commit("split\n\nkeep-split: test_nope.py -> test_nope_a.py -- x", parts=("test_nope_a.py",), old_file=True, pop=False),
                                      1, "test_nope.py, which is not a keep row in the parent"),
    "bare-removal-still-refused": (_split_commit("split"), 1, "keep row test_k.py was removed"),
    "returns-from-quarantine-plain-new-file-still-refused": (lambda r: _returns(r), 1, "keep row test_q2.py returns a file that was in quarantine"),
    "keep-drop-still-accepted": (lambda r: _keep_dropped(r), 0, "0 violation"),        # helpers of the K5 section below, bound at call time
    "layer-change-without-line-is-as-before": (lambda r: relayers(r, "retype", lambda d: d["keep"]["test_k.py"].update(layer="scenario")), 0, "0 violation"),
}


@pytest.mark.parametrize("case", SPLIT_CHECK)
def test_check_keep_split_door(tmp_path, capsys, case):
    root = base_repo(tmp_path)
    action, rc, text = SPLIT_CHECK[case]
    action(root)
    assert tq.main(["check", "--root", str(root)]) == rc
    assert text in capsys.readouterr().out


def test_stubs_and_no_layers(tmp_path, capsys):
    assert tq.main(["check", "--root", str(tmp_path)]) == 0 and "no test-layers.json" in capsys.readouterr().out
    assert tq.main(["enter", "--pipeline", "1", "--coverage-pipeline", "2", "--root", str(tmp_path)]) == 1
    assert "keep rows" in capsys.readouterr().out                                              # absent file: enter says so and refuses
    assert tq.main(["status", "--root", str(tmp_path)]) == 0 and "no quarantine" in capsys.readouterr().out
    assert tq.status_line(tmp_path) == []


# --- check (K5) ------------------------------------------------------------------------------------------------------

def _build_base(root):
    entry = _build_repo(root)
    commit(root, "quarantine-enter: init", **{tq.LAYERS_REL.replace("/", "__"): layers_json(entry=entry)})
    return entry


def base_repo(tmp_path):
    root = tmp_path / "r"
    from_template("base", root, _build_base)
    return root


def edit(root, msg, rel="test_q1.py", text="# changed\n"):
    return commit(root, msg, **{(T + rel).replace("/", "__"): text})


def relayers(root, msg, mutate):
    doc = json.loads(Path(root, tq.LAYERS_REL).read_text())
    mutate(doc)
    return commit(root, msg, **{tq.LAYERS_REL.replace("/", "__"): json.dumps(doc)})


def _later_door(root):
    sha = edit(root, "edit without a door")
    commit(root, "quarantine-edit: test_q1.py -- later, another commit")
    return sha


def _accept(root):
    sha = edit(root, "edit without a door")
    commit(root, f"quarantine-accept: {sha[:8]} -- the owner knows")


def _rename(root):
    G(root, "mv", T + "test_q1.py", T + "test_z.py")
    commit(root, "rename")


def _delete(root):
    G(root, "rm", "-q", T + "test_q1.py")
    commit(root, "delete")


def _merge(root):
    G(root, "checkout", "-q", "-b", "side")
    edit(root, "side edit\n\nquarantine-edit: test_q1.py -- reason in the second parent")
    G(root, "checkout", "-q", "-")
    commit(root, "main moves on", plain__txt="x")
    G(root, "merge", "-q", "--no-ff", "-m", "merge side", "side")


def _keep_removed(root):
    relayers(root, "drop it", lambda d: d["keep"].pop("test_k.py"))


def _keep_dropped(root):
    G(root, "rm", "-q", T + "test_k.py")
    relayers(root, "keep-drop: test_k.py -- duplicate of a table row", lambda d: d["keep"].pop("test_k.py"))


def _returns(root):
    def mv(d):
        d["quarantine"].pop("test_q2.py")
        d["keep"]["test_q2.py"] = {"layer": "table", "why": "back"}
    relayers(root, "quarantine-purge: c1", mv)


def _pins(root):
    relayers(root, "pin", lambda d: d["pin_holds"].update({"test_k.py": "role pin"}))


def _edge(msg):
    return lambda root: edit(root, msg, "test_k.py", "import test_q1\n")


def _bad_entry(root):
    relayers(root, "quarantine-enter: moved", lambda d: d["cohorts"]["c1"].update(commit_at_entry="deadbeef" * 5))


def _row_added(root):
    relayers(root, "add a row", lambda d: d["quarantine"].update({"test_n.py": {"cohort": "c1", "entered": "x", "release_at_entry": "0.10.9"}}))


CHECK = {
    "control": (lambda r: None, 0, "0 violation(s)"),
    "edit-no-door": (lambda r: edit(r, "plain"), 1, "quarantined file test_q1.py was changed"),
    "edit-with-door": (lambda r: edit(r, "x\n\nquarantine-edit: test_q1.py -- reason"), 0, "0 violation"),
    "delete": (_delete, 1, "quarantined file test_q1.py"), "rename": (_rename, 1, "quarantined file test_q1.py"),
    "door-in-another-commit": (_later_door, 1, "quarantined file test_q1.py"),
    "merge-door-in-second-parent": (_merge, 0, "0 violation"),
    "keep-removed-no-door": (_keep_removed, 1, "keep row test_k.py was removed"), "keep-drop-door": (_keep_dropped, 0, "0 violation"),
    "returns-from-quarantine": (_returns, 1, "keep row test_q2.py returns a file that was in quarantine"),
    "row-added-no-door": (_row_added, 1, "quarantine row test_n.py was added"),
    "pin-after-enter": (_pins, 1, "pin_holds row test_k.py was added after the first quarantine-enter"),
    "new-import-edge": (_edge("edge"), 1, "new import edge test_k.py -> test_q1.py"),
    "import-door": (_edge("edge\n\nquarantine-import: test_k.py -> test_q1.py -- copy later"), 0, "0 violation"),
    "accept-later": (_accept, 0, "0 violation"),
    "rewritten-history": (_bad_entry, 1, "history was rewritten"),
}


@pytest.mark.parametrize("case", CHECK)
def test_check_table(tmp_path, capsys, case):
    root = base_repo(tmp_path)
    action, rc, text = CHECK[case]
    action(root)
    assert tq.main(["check", "--root", str(root)]) == rc
    assert text in capsys.readouterr().out


WORDING = {                                                  # OF4-13: (action, text the refusal output must carry)
    "no-doubled-or": (lambda r: edit(r, "plain"), "; or a later commit line"),
    "bare-name-hint": (lambda r: edit(r, "plain"), "(the bare file name, no folder) in this commit message"),
}


@pytest.mark.parametrize("case", WORDING)
def test_check_refusal_wording(tmp_path, capsys, case):
    root = base_repo(tmp_path)
    action, text = WORDING[case]
    action(root)
    assert tq.main(["check", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert text in out and "or or" not in out


def test_check_rebase_entry_repairs(tmp_path, capsys):
    root = base_repo(tmp_path)
    _bad_entry(root)
    assert tq.main(["check", "--root", str(root)]) == 1
    head = G(root, "rev-parse", "HEAD")
    assert tq.main(["enter", "--root", str(root), "--rebase-entry", "c1", "deadbeef"]) == 1                # not a commit: refused
    assert tq.main(["enter", "--root", str(root), "--rebase-entry", "c1", head]) == 0
    assert tq.main(["check", "--root", str(root)]) == 0
    msg = Path(root, "ci-out/quarantine-enter-msg.txt").read_text()
    assert msg.startswith("quarantine-enter: rebase c1\n") and gate_words(msg) == GATE_WORDS


# --- TD-15.6b: pull, ci-summary, _schedules, _ci_pipelines (no git repository: CI is an argument, the records are plain files) ---------------

def plain_root(tmp_path, quar=("test_q1.py", "test_q2.py"), runs=(), pulls=()):
    root = tmp_path / "w"
    W(root, tq.CONFIG_REL, json.dumps({"branch": "br", "max_gap_days": 4}))
    W(root, tq.LAYERS_REL, layers_json(quar=quar))
    W(root, PLUGIN, json.dumps({"version": "0.10.9"}))
    if runs or pulls:
        W(root, tq.WATCH_REL, "".join(json.dumps(r) + "\n" for r in (*runs, *pulls)))
    return root


def watch_rows(root):
    return [json.loads(x) for x in Path(root, tq.WATCH_REL).read_text().splitlines()] if Path(root, tq.WATCH_REL).is_file() else []


def shard_file(root, i, n, expected, files, sha="a" * 40, ver="0.11.0"):
    W(root, f"ci-out/quarantine-watch-{i}-of-{n}.json",
      json.dumps({"sha": sha, "package_version": ver, "shard": f"{i}/{n}", "expected": expected, "files": files}))


Q1, Q2 = {"test_q1.py": {"status": "green"}}, {"test_q2.py": {"status": "green"}}
LONG = "x" * 200
CI_ENV = {"CI_PIPELINE_ID": "77", "CI_PIPELINE_SOURCE": "schedule", "CI_PIPELINE_CREATED_AT": "2026-11-24T03:00:05Z"}
# id: (quarantine, shards [(i, n, expected, files)], complete, tokens in the printed text)
SUMMARY = {
    "shard-missing": (("test_q1.py", "test_q2.py"), [(1, 2, ["test_q1.py"], Q1)], False,
                      ["2 files -- 1 green, 0 red, 0 timeout, 0 ran nothing, 0 missing, 1 not run; complete: no", "  not_run: test_q2.py"]),
    "union-differs-from-the-section": (("test_q1.py", "test_q2.py"), [(1, 2, ["test_q1.py"], Q1), (2, 2, [], {})], False,
                                       ["1 not run; complete: no", "  not_run: test_q2.py"]),
    "all-there": (("test_q1.py", "test_q2.py"), [(1, 2, ["test_q1.py"], Q1), (2, 2, ["test_q2.py"], Q2)], True,
                  ["quarantine watch aaaaaaaa (package 0.11.0, pipeline 77, source schedule): 2 files -- 2 green", "complete: yes",
                   "examine in a forge session: python tools/test_quarantine.py pull, then status"]),
    "expected-without-result": (("test_q1.py",), [(1, 1, ["test_q1.py"], {})], False, ["1 files -- 0 green", "1 not run; complete: no"]),
    "empty-quarantine-zero-line": ((), [(1, 2, [], {}), (2, 2, [], {})], True,
                                   ["0 files -- 0 green, 0 red, 0 timeout, 0 ran nothing, 0 missing, 0 not run; complete: yes"]),
    "no-shard-at-all": (("test_q1.py",), [], False, ["quarantine watch unknown (package unknown, pipeline 77", "1 not run; complete: no"]),
    "red-and-timeout-lines": (("test_q1.py", "test_q2.py"),
                              [(1, 1, ["test_q1.py", "test_q2.py"], {"test_q1.py": {"status": "red", "fails": [LONG, "b", "+12 more"]},
                                                                      "test_q2.py": {"status": "timeout"}})], True,
                              ["1 red, 1 timeout", "  red: test_q1.py  " + "x" * 160 + " (+13 more)", "  timeout: test_q2.py"]),
    "red-with-a-crash-only": (("test_q1.py",), [(1, 1, ["test_q1.py"], {"test_q1.py": {"status": "red", "fails": [], "crash": "ImportError: z"}})],
                              True, ["  red: test_q1.py  ImportError: z"]),
}


@pytest.mark.parametrize("case", SUMMARY)
def test_ci_summary_table(tmp_path, case):
    quar, shards, complete, tokens = SUMMARY[case]
    root = plain_root(tmp_path, quar=quar)
    for i, n, expected, files in shards:
        shard_file(root, i, n, expected, files)
    rec, lines = tq.ci_summary(root, sorted(Path(root, "ci-out").glob("*.json")) if shards else [], CI_ENV)
    text = "\n".join(lines)
    assert rec["complete"] is complete and rec["pipeline"] == 77 and rec["source"] == "schedule"
    for tok in tokens:
        assert tok in text
    assert set(rec["files"]) == set(quar) | {n for _, _, e, _ in shards for n in e}


def test_ci_summary_two_shas_or_a_broken_shard_is_incomplete(tmp_path):
    root = plain_root(tmp_path)
    shard_file(root, 1, 2, ["test_q1.py"], Q1, sha="a" * 40)
    shard_file(root, 2, 2, ["test_q2.py"], Q2, sha="b" * 40)
    assert tq.ci_summary(root, sorted(Path(root, "ci-out").glob("*.json")), CI_ENV)[0]["complete"] is False
    shard_file(root, 2, 2, ["test_q2.py"], Q2, sha="a" * 40)
    paths = sorted(Path(root, "ci-out").glob("*.json"))
    assert tq.ci_summary(root, paths, CI_ENV)[0]["complete"] is True
    W(root, "ci-out/quarantine-watch-2-of-2.json", "{not json")                                  # an unreadable shard is a missing shard
    rec, _ = tq.ci_summary(root, paths, CI_ENV)
    assert rec["complete"] is False and rec["files"]["test_q2.py"]["status"] == "not_run"


def test_ci_summary_cli_writes_the_record_and_needs_from(tmp_path, capsys):
    root = plain_root(tmp_path)
    shard_file(root, 1, 1, ["test_q1.py", "test_q2.py"], {**Q1, **Q2})
    assert tq.main(["ci-summary", "--root", str(root), "--from", "ci-out/quarantine-watch-*.json", "--out", "ci-out/quarantine-watch.json"]) == 0
    assert "complete: yes" in capsys.readouterr().out
    assert json.loads(Path(root, "ci-out/quarantine-watch.json").read_text())["complete"] is True
    assert tq.main(["ci-summary", "--root", str(root)]) == 2 and "--from" in capsys.readouterr().out


class WatchCI:
    """CI as an argument: pipelines = [(id, source, created_at, has the report job)], records = {id: record}, schedules = [(id, ref, active, vars)]."""

    def __init__(self, pipelines=(), records=None, schedules=(), down=None, page_size=None):
        self.pipelines, self.records, self.schedules, self.down, self.calls = list(pipelines), records or {}, list(schedules), down, []
        self.page_size = page_size            # rows per page of the list call; None = everything on page 1, nothing after

    def _get(self, path):
        self.calls.append(path)
        if self.down:
            raise tq.CIError(self.down)
        if path.startswith("/pipelines?ref="):
            page = int(re.search(r"&page=(\d+)$", path).group(1)) if "&page=" in path else 1
            size = self.page_size or len(self.pipelines)
            rows = self.pipelines[(page - 1) * size:page * size] if size else []
            return json.dumps([{"id": i, "source": s, "created_at": c, "sha": "s%d" % i} for i, s, c, _ in rows])
        m = re.fullmatch(r"/pipelines/(\d+)/jobs\?per_page=100", path)
        if m:
            has = next(h for i, _, _, h in self.pipelines if i == int(m.group(1)))
            return json.dumps([{"name": tq.WATCH_REPORT_JOB if has else "forge-check"}])
        m = re.fullmatch(r"/pipelines/(\d+)", path)
        if m:
            i, s, c, _ = next(p for p in self.pipelines if p[0] == int(m.group(1)))
            return json.dumps({"id": i, "source": s, "created_at": c, "sha": "s%d" % i})
        if path.startswith("/pipeline_schedules?"):
            return json.dumps([{"id": i, "ref": ref, "active": act} for i, ref, act, _ in self.schedules])
        m = re.fullmatch(r"/pipeline_schedules/(\d+)", path)
        if m:
            return json.dumps({"variables": next(v for i, _, _, v in self.schedules if i == int(m.group(1)))})
        raise AssertionError(path)

    def artifact(self, pid, job, path):
        assert job == tq.WATCH_REPORT_JOB and path == tq.WATCH_ART
        if int(pid) not in self.records:
            raise tq.CIError("missing")
        return json.dumps(self.records[int(pid)])


REC = {"complete": True, "package_version": "0.11.0", "files": {"test_q1.py": {"status": "green"}}}
P1 = (11, "schedule", "2026-11-24T03:00:12.5Z", True)


def test_pull_records_a_new_run_and_the_pull_row_with_two_separate_times(tmp_path, capsys):
    root = plain_root(tmp_path)
    ci = WatchCI([P1, (10, "push", "2026-11-23T01:00:00Z", False)], {11: REC})
    assert tq.main(["pull", "--root", str(root)], ci=ci, today=TODAY) == 0
    run, row = watch_rows(root)
    assert run == {"kind": "run", "pipeline": 11, "source": "schedule", "created_at": "2026-11-24T03:00:12.5Z", "sha": "s11",
                   "package_version": "0.11.0", "complete": True, "files": REC["files"]}
    assert row == {"kind": "pull", "at": "2026-11-25T00:00:00", "ci": "ok", "newest_watch_pipeline": 11, "newest_watch_at": "2026-11-24T03:00:12.5Z"}
    assert "1 new watch run(s), 0 skipped; newest watch pipeline 11" in capsys.readouterr().out


def test_pull_on_a_recorded_pipeline_skips_it_and_still_writes_the_pull_row(tmp_path, capsys):
    root = plain_root(tmp_path)
    ci = WatchCI([P1], {11: REC})
    assert tq.main(["pull", "--root", str(root)], ci=ci, today=TODAY) == 0
    assert tq.main(["pull", "--root", str(root), "--pipeline", "11"], ci=ci, today=TODAY) == 0
    assert "pipeline 11 already recorded -- skipped" in capsys.readouterr().out
    assert tq.main(["pull", "--root", str(root)], ci=ci, today=TODAY) == 0                      # nothing newer than the last record: no run row
    kinds = [r["kind"] for r in watch_rows(root)]
    assert kinds == ["run", "pull", "pull", "pull"]
    assert watch_rows(root)[-1]["newest_watch_pipeline"] == 11                                  # the recorded run is still the newest watch run


def test_pull_with_a_pipeline_id_and_an_artifact_not_ready(tmp_path, capsys):
    root = plain_root(tmp_path)
    ci = WatchCI([P1], {})
    assert tq.main(["pull", "--root", str(root), "--pipeline", "11"], ci=ci, today=TODAY) == 0
    out = capsys.readouterr().out
    assert "pipeline 11 has no watch record yet" in out and "pull --pipeline 11" in out
    assert [r["kind"] for r in watch_rows(root)] == ["pull"] and watch_rows(root)[0]["newest_watch_pipeline"] is None   # B3 (d): no record, no watch time
    ci.records[11] = REC
    assert tq.main(["pull", "--root", str(root), "--pipeline", "11"], ci=ci, today=TODAY) == 0
    assert [r["kind"] for r in watch_rows(root)] == ["pull", "run", "pull"]


def test_pull_ci_unreachable_exits_1_with_the_line_and_writes_the_pull_row(tmp_path, capsys):
    root = plain_root(tmp_path)
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI(down="unreachable"), today=TODAY) == 1
    assert "ci: unreachable" in capsys.readouterr().out
    assert watch_rows(root) == [{"kind": "pull", "at": "2026-11-25T00:00:00", "ci": "unreachable", "newest_watch_pipeline": None, "newest_watch_at": None}]


def test_pull_token_refused_exits_1_with_its_own_line(tmp_path, capsys, monkeypatch):
    def refused(*a, **k):
        raise tq.CIError("token_refused")
    monkeypatch.setattr(tq, "GitlabCI", refused)
    root = plain_root(tmp_path)
    assert tq.main(["pull", "--root", str(root)], today=TODAY) == 1
    assert "ci: token_refused" in capsys.readouterr().out and watch_rows(root)[0]["ci"] == "token_refused"
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI(down="token_refused"), today=TODAY) == 1       # a 401 in the middle of the pull: the same
    assert watch_rows(root)[-1]["ci"] == "token_refused"


def test_pull_when_the_watch_has_not_run_for_nine_days_exits_3_with_the_alert(tmp_path, capsys):
    old = dict(run_row(5, "0.11.0", **GREEN), created_at="2026-11-16T03:00:00Z")
    root = plain_root(tmp_path, runs=[old])
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=TODAY) == 3
    out = capsys.readouterr().out
    assert ("TEST QUARANTINE ALERT: the watch has not run on CI for 9 d (last 2026-11-16, as of pull 2026-11-25) -- tell the owner: "
            "the schedule on br is missing or failing (docs/RUNBOOK.md section 7)") in out
    assert watch_rows(root)[-1]["newest_watch_at"] == "2026-11-16T03:00:00Z" and watch_rows(root)[-1]["at"].startswith("2026-11-25")
    # 8 days is still inside 2 x max_gap_days
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=date(2026, 11, 24)) == 0


def test_pull_never_run_and_entered_long_ago_exits_3_but_a_young_entry_does_not(tmp_path, capsys):
    root = plain_root(tmp_path)                                                                   # entered 2026-11-20
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=date(2026, 11, 28)) == 0   # 8 d
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=date(2026, 11, 29)) == 3   # 9 d
    assert "(last never, as of pull 2026-11-29)" in capsys.readouterr().out


def test_pull_empty_quarantine_and_no_layers_do_not_alert(tmp_path):
    root = plain_root(tmp_path, quar=())
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=date(2026, 12, 30)) == 0
    Path(root, tq.LAYERS_REL).unlink()
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([]), today=date(2026, 12, 30)) == 0


def test_pull_without_a_config_is_a_refusal_not_a_crash(tmp_path, capsys):
    root = plain_root(tmp_path)
    Path(root, tq.CONFIG_REL).unlink()
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([])) == 1 and "config.json" in capsys.readouterr().out


def test_pipelines_filters_by_source_job_and_time(tmp_path):
    ci = WatchCI([(14, "web", "2026-11-26T01:00:00Z", True), (13, "merge_request_event", "2026-11-25T01:00:00Z", True),
                  (12, "push", "2026-11-24T01:00:00Z", False), (11, "schedule", "2026-11-23T01:00:00Z", True),
                  (10, "api", "2026-11-20T01:00:00Z", True)])
    got = tq._ci_pipelines("br/x", tq.WATCH_SOURCES, ci)
    assert [p["id"] for p in got] == [10, 11, 14]                                                 # oldest first; the MR and the no-job ones are out
    assert [p["id"] for p in tq._ci_pipelines("br", tq.WATCH_SOURCES, ci, after="2026-11-23T01:00:00Z")] == [14]
    assert ci.calls[0] == "/pipelines?ref=br%2Fx&per_page=50"
    with pytest.raises(tq.CIError):
        tq._ci_pipelines("br", tq.WATCH_SOURCES, WatchCI(down="unreachable"))


WATCH_VAR = [{"key": "QUARANTINE_WATCH", "value": "1"}]
SCHEDULES = {
    "ok": ([(1, "br", True, WATCH_VAR)], "ok"),
    "ok-full-ref": ([(1, "refs/heads/br", True, WATCH_VAR)], "ok"),
    "ok-second-of-two": ([(1, "main", True, WATCH_VAR), (2, "br", True, [{"key": "A", "value": "1"}, *WATCH_VAR])], "ok"),
    "no-schedule-is-missing": ([], "missing"),
    "schedule-without-the-variable-is-missing": ([(1, "br", True, [{"key": "OTHER", "value": "1"}])], "missing"),
    "variable-with-another-value-is-missing": ([(1, "br", True, [{"key": "QUARANTINE_WATCH", "value": "0"}])], "missing"),
    "schedule-without-any-variables-is-missing": ([(1, "br", True, None)], "missing"),
    "other-branch-is-missing": ([(1, "main", True, WATCH_VAR)], "missing"),
    "inactive-is-missing": ([(1, "br", False, WATCH_VAR)], "missing"),
}


@pytest.mark.parametrize("case", SCHEDULES)
def test_schedules_table(case):
    rows, want = SCHEDULES[case]
    assert ORIG_SCHEDULES("br", WatchCI(schedules=rows)) == want


@pytest.mark.parametrize("kind", ["unreachable", "token_refused", "missing"])
def test_schedules_unreadable_ci_is_unknown_never_ok(kind):
    assert ORIG_SCHEDULES("br", WatchCI(down=kind)) == "unknown"


def test_schedules_reads_the_list_then_each_schedule_on_the_branch_only():
    ci = WatchCI(schedules=[(1, "main", True, WATCH_VAR), (2, "br", True, WATCH_VAR)])
    assert ORIG_SCHEDULES("br", ci) == "ok"
    assert ci.calls == ["/pipeline_schedules?scope=active&per_page=100", "/pipeline_schedules/2"]


def test_watch_pipelines_branch_literal_equals_config():
    # The CI file is .github/workflows/quarantine-watch.yml since the move (FG7-9, risk 3): the push branch of the watch is read
    # from it. A watch schedule that starts no other job is the GitHub form of the old `QUARANTINE_WATCH != "1"` rules: the watch
    # is a workflow of its own (tools/test_workflows.py holds the cron and the start events).
    cfg = json.loads(Path(REPO, tq.CONFIG_REL).read_text(encoding="utf-8"))
    text = Path(REPO, ".github", "workflows", "quarantine-watch.yml").read_text(encoding="utf-8")
    literals = set(re.findall(r"^\s*branches:\s*\[([^\]]+)\]", text, re.M))
    assert literals == {cfg["branch"]} and cfg["branch"] == "main"
    assert cfg["schedule_variable"] == tq.WATCH_VARIABLE


# --- TD-15.6c: purge ------------------------------------------------------------------------------------------------------
import ast

PG_REAL_PKG = tq._pkg_module          # the real loader, taken before any monkeypatch
PG_TESTS = T.rstrip("/")
PG_SCRIPTS = "ai-packages/qa-factory/scripts/"
PG_TIMEOUTS = '''"""mini selftest"""
TEST_TIMEOUTS = {
    "test_k.py": 600,
    # why q1 is slow (a comment of a deleted row)
    "test_q1.py": 600,
    "test_q2.py": 900,
    # keep note: q3 stays
    "test_q3.py": 700,
}
'''
PG_DRIVER = '''{"schema": 1,
 "names": [],
 "source_readers": [
  {"file": "test_q1.py", "function": "f", "count": 1, "targets": ["x"]},
  {"file": "test_k.py", "function": "g", "count": 1, "targets": ["y"]}
 ],
 "source_mentions": [
  {"file": "test_q2.py", "function": "<module>", "count": 1, "why": "text"}
 ]
}
'''
PG_FEATURES = '''{
  "schema_version": 1,
  "features": [
    {
      "id": "F01",
      "root": "package",
      "globs": [
        "scripts/tests/test_k.py",
        "scripts/tests/test_q1.py"
      ]
    },
    {
      "id": "F02",
      "root": "package",
      "globs": [
        "scripts/tests/test_q2.py"
      ]
    }
  ]
}
'''


def pg_layers(entry, extra_cohort=False):
    q = {n: {"cohort": c, "entered": "2026-11-20", "release_at_entry": "0.10.9"}
         for n, c in (("test_q1.py", "c1"), ("test_q2.py", "c1"), ("test_q3.py", "c2"))}
    coh = {c: {"entered": "2026-11-20", "release_at_entry": "0.10.9", "commit_at_entry": entry, "phase": 1, "replaced_by": {}}
           for c in (("c1", "c2", "c3") if extra_cohort else ("c1", "c2"))}
    return json.dumps({"schema_version": 1, "layers": ["scenario", "data_join", "table", "register", "gate_named", "detector"],
                       "enforce_listing": True, "keep": {"test_k.py": {"layer": "table", "why": "x"}}, "quarantine": q,
                       "pin_holds": {"test_q2.py": {"why": "pin"}}, "cohorts": coh}, indent=1)


@pytest.fixture(scope="module")
def pg_base(tmp_path_factory):
    """ONE mini package in ONE git repository, built once for the whole table; a case works on a copy."""
    root = tmp_path_factory.mktemp("purge") / "r"
    root.mkdir()
    G(root, "init", "-q")
    files = {
        PLUGIN: json.dumps({"version": "0.10.9"}),
        PG_SCRIPTS + "selftest.py": PG_TIMEOUTS,
        PG_SCRIPTS + "slow_tests.json": json.dumps({"measured_on": "2026-11-01", "source": "hand", "thresholds": {"slow_over_s": 10, "fast_under_s": 5},
                                                    "max_drift": 5, "files": {"test_k.py": 20.0, "test_q1.py": 30.0, "test_q3.py": 40.0}}, indent=2),
        T + "test_k.py": "import helper_keep\nFX = 'x'\n",
        T + "test_q1.py": "import helper_keep\nimport helper_gone\nFX = ('lit_gone', 'lit_kept')\n",
        T + "test_q2.py": "FX = ('lit_gone', 'lit_joint')\n",
        T + "test_q3.py": "FX = 'lit_q3'\n",
        T + "helper_keep.py": "X = 1\n", T + "helper_gone.py": "import helper_deep\n", T + "helper_deep.py": "Y = 2\n", T + "helper_orphan.py": "Z = 3\n",
        T + "fixtures/lit_gone/a.txt": "a", T + "fixtures/lit_kept/a.txt": "a", T + "fixtures/lit_joint/a.txt": "a", T + "fixtures/lit_q3/a.txt": "a",
        T + "fixtures/driver-layers.json": PG_DRIVER,
        "ai-packages/qa-factory/references/stage-joints.json": json.dumps({"joints": [{"fixture": "lit_joint"}]}),
        "plans/features.json": PG_FEATURES,
        "plans/builder-rules.md": "see test_q1.py for the rule\n",
    }
    for rel, text in files.items():
        W(root, rel, text)
    W(root, T + "test_k.py", "import helper_keep\nFX = 'lit_kept'\n")
    entry = commit(root, "base")
    commit(root, "release 0.11.0", **{PLUGIN.replace("/", "__"): json.dumps({"version": "0.11.0"})})
    sha = commit(root, "release 0.12.0", **{PLUGIN.replace("/", "__"): json.dumps({"version": "0.12.0"})})
    run = run_row(1, "0.12.0", sha=sha, **{"test_q1.py": red("a"), "test_q2.py": {"status": "green"}})
    commit(root, "state", **{
        "plans/test-quarantine/watch.jsonl": json.dumps(run) + "\n", "plans/test-quarantine/verdicts.jsonl": json.dumps(verdict()) + "\n",
        "plans/test-quarantine/config.json": json.dumps({"branch": "br", "max_gap_days": 4}), tq.LAYERS_REL.replace("/", "__"): pg_layers(entry)})
    return root


@pytest.fixture
def pg(pg_base, tmp_path, shim, monkeypatch):
    st, ip = PG_REAL_PKG(REPO, "selftest"), PG_REAL_PKG(REPO, "install_paths")
    monkeypatch.setattr(tq, "_pkg_module", lambda root, name: st if name == "selftest" else ip)
    lint = []
    monkeypatch.setattr(tq, "_purge_lint", lambda root: (lint.append(str(root)) or (0, "clean")))
    root = tmp_path / "w"
    shutil.copytree(pg_base, root)
    return types.SimpleNamespace(root=root, lint=lint)


def pg_tree(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(Path(root).rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(root).parts and "ci-out" not in p.relative_to(root).parts}


def pg_run(pg, capsys, *argv):
    rc = tq.main(["purge", "--root", str(pg.root), *argv])
    return rc, capsys.readouterr().out


def pg_invariant(root):
    """purge deletes nothing a kept test reads: every module a remaining .py imports and every fixture folder it names exists."""
    tdir = Path(root) / T
    have = {p.stem for p in tdir.glob("*.py")}
    folders = {p.name for p in (tdir / "fixtures").iterdir() if p.is_dir()}
    for p in tdir.glob("*.py"):
        text = p.read_text()
        for m in tq._imports(text):
            assert m in have or m not in ("helper_keep", "helper_gone", "helper_deep", "test_q1", "test_q2"), (p.name, m)
        if p.name == "test_k.py":
            assert "lit_kept" in folders and "lit_joint" in folders and "lit_q3" in folders


WORD = "the owner, 2026-12-01"


def _k_imports_q1(root):
    W(root, T + "test_k.py", "import test_q1\n")


def _timeouts_one_line(root):
    W(root, PG_SCRIPTS + "selftest.py", 'TEST_TIMEOUTS = {\n    "test_k.py": 600,\n    "test_q1.py": 600, "test_q2.py": 900,\n}\n')


def _timeouts_broken(root):
    W(root, PG_SCRIPTS + "selftest.py", PG_TIMEOUTS + "def (\n")


def _third_cohort(root):
    W(root, tq.LAYERS_REL, pg_layers(G(root, "rev-parse", "HEAD~3"), extra_cohort=True))


# id: (mutation of the copy, argv, exit code, text in the output, tree unchanged by the call)
PURGE_REFUSALS = {
    "empty-word": (None, ["--cohort", "c1", "--owner-word", "  "], 1, "--owner-word is empty", True),
    "no-word": (None, ["--cohort", "c1"], 1, "deletion is only on the owner's word", True),
    "no-cohort-arg": (None, ["--owner-word", WORD], 1, "known: c1, c2", True),
    "unknown-cohort": (None, ["--cohort", "zz", "--owner-word", WORD], 1, "names no cohort", True),
    "not-ready": (None, ["--cohort", "c2", "--owner-word", WORD], 1, "cohort c2 is not READY TO DELETE (R2:", True),
    "kept-imports-cohort": (_k_imports_q1, ["--cohort", "c1", "--owner-word", WORD], 1, "R6:", True),
    "timeouts-shared-line": (_timeouts_one_line, ["--cohort", "c1", "--owner-word", WORD], 1, "share a line", True),
    "timeouts-unparseable": (_timeouts_broken, ["--cohort", "c1", "--owner-word", WORD], 1, "does not parse", True),
    "empty-cohort": (_third_cohort, ["--cohort", "c3", "--owner-word", WORD], 0, "cohort c3 has no files; nothing changed", True),
    "dry-run": (None, ["--cohort", "c1", "--owner-word", WORD, "--dry-run"], 0, "quarantine purge (dry run): 2 test files would be deleted", True),
}


@pytest.mark.parametrize("case", PURGE_REFUSALS)
def test_purge_refusals_and_dry_run(pg, capsys, case):
    mutate, argv, rc, text, same = PURGE_REFUSALS[case]
    if mutate:
        mutate(pg.root)
    before = pg_tree(pg.root)
    got, out = pg_run(pg, capsys, *argv)
    assert (got, text in out) == (rc, True), out
    assert (pg_tree(pg.root) == before) is same
    assert not Path(pg.root, "ci-out/quarantine-purge-msg.txt").exists() and pg.lint == []


def test_purge_deletes_exactly_the_cohort_and_what_only_it_used(pg, capsys):
    rc, out = pg_run(pg, capsys, "--cohort", "c1", "--owner-word", WORD)
    root = Path(pg.root)
    tdir = root / T
    assert rc == 0, out
    assert sorted(p.name for p in tdir.glob("*.py")) == ["helper_keep.py", "helper_orphan.py", "test_k.py", "test_q3.py"]   # c2 and kept stay
    assert sorted(p.name for p in (tdir / "fixtures").iterdir()) == ["driver-layers.json", "lit_joint", "lit_kept", "lit_q3"]
    pg_invariant(root)
    # TEST_TIMEOUTS: parseable, kept rows intact, deleted rows gone, comments untouched
    text = (root / PG_SCRIPTS / "selftest.py").read_text()
    table = ast.literal_eval(ast.parse(text).body[1].value)
    assert table == {"test_k.py": 600, "test_q3.py": 700}
    assert "# keep note: q3 stays" in text and "# why q1 is slow" in text
    # the registries
    drv = json.loads((tdir / "fixtures/driver-layers.json").read_text())
    assert [r["file"] for r in drv["source_readers"]] == ["test_k.py"] and drv["source_mentions"] == []
    feats = json.loads((root / "plans/features.json").read_text())
    assert [f["globs"] for f in feats["features"]] == [["scripts/tests/test_k.py"], []]
    slow = json.loads((root / PG_SCRIPTS / "slow_tests.json").read_text())
    assert sorted(slow["files"]) == ["test_k.py", "test_q3.py"]             # the other cohort's row is not touched
    lay = json.loads((root / tq.LAYERS_REL).read_text())
    assert (sorted(lay["quarantine"]), sorted(lay["cohorts"]), lay["pin_holds"]) == (["test_q3.py"], ["c2"], {})
    last = json.loads((root / tq.VERDICTS_REL).read_text().splitlines()[-1])
    assert (last["kind"], last["cohort"], last["owner_word"], last["files"]) == ("purge", "c1", WORD, ["test_q1.py", "test_q2.py"])
    msg = (root / "ci-out/quarantine-purge-msg.txt").read_text()
    assert "quarantine-purge: c1" in msg and WORD in msg and gate_words(msg) == GATE_WORDS
    assert pg.lint == [str(root)]
    for piece in ("quarantine purge: 2 test files deleted (", "1 fixture folders deleted (2 kept: used by ",
                  "2 helpers deleted; registries: TEST_TIMEOUTS -2, slow_tests.json -1, driver-layers.json -2, features.json -2; "
                  "still named in text: plans/builder-rules.md:1; commit: git commit -F ci-out/quarantine-purge-msg.txt"):
        assert piece in out, out
    assert "lint ratchet --check: exit 0" in out
    # what remains is a coherent quarantine: c1 is gone, c2 is still judged by status
    assert [c["id"] for c in tq.status_data(root)["cohorts"]] == ["c2"]


def test_purge_dynamic_fixture_path_keeps_every_fixture_and_lists_candidates(pg, capsys):
    W(pg.root, T + "test_k.py", "import helper_keep\nfrom pathlib import Path\nFX = Path('fixtures') / name\n")
    rc, out = pg_run(pg, capsys, "--cohort", "c1", "--owner-word", WORD)
    assert rc == 0, out
    assert sorted(p.name for p in Path(pg.root, T, "fixtures").iterdir()) == ["driver-layers.json", "lit_gone", "lit_joint", "lit_kept", "lit_q3"]
    assert not Path(pg.root, T + "test_q1.py").exists()
    assert "0 fixture folders deleted" in out and "NOT deleted: a kept file builds a fixture path dynamically" in out
    assert "test_k.py:3" in out and "candidates left: lit_gone" in out


def test_purge_registries_done_passes_over_what_cannot_be_edited(pg, capsys):
    _timeouts_one_line(pg.root)
    rc, out = pg_run(pg, capsys, "--cohort", "c1", "--owner-word", WORD, "--registries-done")
    assert rc == 0 and "(by hand: TEST_TIMEOUTS)" in out, out
    assert Path(pg.root, PG_SCRIPTS + "selftest.py").read_text().count("test_q2.py") == 1        # left for the person
    assert not Path(pg.root, T + "test_q2.py").exists()


def test_purge_skips_a_cohort_file_already_deleted_from_disk(pg, capsys):                      # N7
    Path(pg.root, T + "test_q1.py").unlink()                                                    # one file absent (the other, test_q2.py, is pin-held: present)
    assert Path(pg.root, T + "test_q2.py").is_file()
    rc, out = pg_run(pg, capsys, "--cohort", "c1", "--owner-word", WORD)
    assert rc == 0, out
    assert out.count("already absent:") == 1 and "already absent: test_q1.py" in out and "already absent: test_q2.py" not in out
    lay = json.loads(Path(pg.root, tq.LAYERS_REL).read_text())
    assert sorted(lay["quarantine"]) == ["test_q3.py"] and sorted(lay["cohorts"]) == ["c2"]     # both rows left the registry
    assert not Path(pg.root, T + "test_q2.py").exists()                                         # the present one went on being deleted
    assert json.loads(Path(pg.root, tq.VERDICTS_REL).read_text().splitlines()[-1])["files"] == ["test_q1.py", "test_q2.py"]


# --- the fix round on the critic verdict t-2375 (B1..B3, N2, N3, N4, debts 4 and 5) --------------------------------------------------------

LK = tq.LAYERS_REL.replace("/", "__")


def gx(root, *a):
    """git that may fail (a conflicting merge): (rc, out)."""
    p = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-C", str(root), *a],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def merge_with(root, *branches, msg="merge", files=None):
    """A merge commit of `branches` into the checked-out one; `files` {rel: text} overwrite the result (a conflict resolution)."""
    gx(root, "merge", "--no-commit", "--no-ff", *branches)
    for rel, text in (files or {}).items():
        W(root, rel, text)
    G(root, "add", "-A")
    G(root, "commit", "-q", "-m", msg)
    return head_sha(root)


def fork_world(tmp_path, row_before, quar=("test_q1.py",)):
    """A repo whose layers file exists; the fork point `side` holds the quarantine rows when `row_before`, else not."""
    root = tmp_path / "r"

    def build(r):
        entry = _build_repo(r)
        commit(r, "quarantine-enter: init" if row_before else "layers", **{LK: layers_json(entry=entry, quar=quar if row_before else ())})
        return entry, G(r, "rev-parse", "--abbrev-ref", "HEAD")
    entry, main = from_template(("fork", row_before, tuple(quar)), root, build)
    return root, entry, main


def texts(root):
    return [t for _, t in tq.check_history(root)]


def test_merge_that_takes_the_side_without_a_row_the_main_entered_is_judged(tmp_path):         # B1 HOLE
    root, entry, main = fork_world(tmp_path, False)
    G(root, "checkout", "-q", "-b", "side")
    side_doc = layers_json(entry=entry, quar=(), keep=("test_k.py", "test_k2.py"))
    commit(root, "side keeps more", **{LK: side_doc})
    G(root, "checkout", "-q", main)
    commit(root, "quarantine-enter: q1", **{LK: layers_json(entry=entry, quar=("test_q1.py",))})
    merge_sha = merge_with(root, "side", msg="merge side", files={tq.LAYERS_REL: side_doc})
    bad = tq.check_history(root)
    assert [s for s, _ in bad] == [merge_sha] and "quarantine row test_q1.py was removed" in bad[0][1]
    commit(root, f"quarantine-accept: {merge_sha[:8]} -- the owner knows")
    assert tq.check_history(root) == []                                                         # the accept door still works


def test_merge_that_takes_a_side_edit_of_a_file_the_main_quarantined_is_judged(tmp_path):      # B1 HOLE2
    root, entry, main = fork_world(tmp_path, False)
    G(root, "checkout", "-q", "-b", "side")
    edit(root, "side edits the file before it was quarantined")
    G(root, "checkout", "-q", main)
    commit(root, "quarantine-enter: q1", **{LK: layers_json(entry=entry, quar=("test_q1.py",))})
    merge_sha = merge_with(root, "side", msg="merge side")
    bad = tq.check_history(root)
    assert [s for s, _ in bad] == [merge_sha] and "quarantined file test_q1.py was changed" in bad[0][1]
    assert tq.main(["check", "--root", str(root)]) == 1
    G(root, "reset", "-q", "--hard", "HEAD~1")
    merge_with(root, "side", msg="merge side\n\nquarantine-edit: test_q1.py -- the side's edit, taken knowingly")
    assert tq.check_history(root) == []                                                         # the door in the merge message


def test_merge_control_both_parents_hold_the_row_and_the_merge_drops_it(tmp_path):             # B1 CONTROL
    root, entry, main = fork_world(tmp_path, True, quar=("test_q1.py", "test_q2.py"))
    G(root, "checkout", "-q", "-b", "side")
    commit(root, "side plain", plain__txt="s")
    G(root, "checkout", "-q", main)
    commit(root, "main plain", other__txt="m")
    doc = layers_json(entry=entry, quar=("test_q1.py",))
    merge_sha = merge_with(root, "side", msg="merge side", files={tq.LAYERS_REL: doc})
    bad = tq.check_history(root)
    assert [s for s, _ in bad] == [merge_sha] and "quarantine row test_q2.py was removed" in bad[0][1]


def test_row_dropped_on_a_side_is_reported_once_on_the_side_commit(tmp_path):                  # B1 FIX
    root, entry, main = fork_world(tmp_path, True, quar=("test_q1.py", "test_q2.py"))
    G(root, "checkout", "-q", "-b", "side")
    side = relayers(root, "side drops a row", lambda d: d["quarantine"].pop("test_q2.py"))
    G(root, "checkout", "-q", main)
    commit(root, "main plain", other__txt="m")
    merge_with(root, "side", msg="merge side")
    bad = tq.check_history(root)
    assert [s for s, _ in bad] == [side] and "quarantine row test_q2.py was removed" in bad[0][1]


def test_merge_whose_parents_both_lack_a_row_the_base_has_is_not_a_violation_of_the_merge(tmp_path):
    root, entry, main = fork_world(tmp_path, True, quar=("test_q1.py", "test_q2.py"))
    G(root, "checkout", "-q", "-b", "s1")
    one = relayers(root, "s1 drops", lambda d: d["quarantine"].pop("test_q2.py"))
    G(root, "checkout", "-q", main)
    G(root, "checkout", "-q", "-b", "s2")
    two = relayers(root, "s2 drops", lambda d: d["quarantine"].pop("test_q2.py"))
    merge_with(root, "s1", msg="merge s1")
    assert sorted(s for s, _ in tq.check_history(root)) == sorted([one, two])                   # only the two commits that dropped it


def test_octopus_merge_is_judged_over_all_parents(tmp_path):
    root, entry, main = fork_world(tmp_path, True, quar=("test_q1.py", "test_q2.py"))
    for b in ("a", "b"):
        G(root, "checkout", "-q", "-b", b, main)
        commit(root, "plain " + b, **{b + "__txt": b})
    G(root, "checkout", "-q", main)
    merge_sha = merge_with(root, "a", "b", msg="octopus", files={tq.LAYERS_REL: layers_json(entry=entry, quar=("test_q1.py",))})
    assert len(G(root, "log", "-1", "--format=%P").split()) == 3
    assert [s for s, _ in tq.check_history(root)] == [merge_sha]


def test_merge_without_a_base_falls_back_to_the_union_of_the_parents(monkeypatch):
    rows = {"p1": {"test_q1.py": {}, "test_q2.py": {}}, "p2": {"test_q1.py": {}}}
    sec = lambda p: {"keep": {}, "quarantine": rows[p]}
    new = {"keep": {}, "quarantine": {"test_q1.py": {}}}
    monkeypatch.setattr(tq, "_git", lambda root, *a: (1, ""))                                  # merge-base: none
    assert tq._removed_by("r", sec, ["p1", "p2"], new)["quarantine"] == {"test_q2.py"}


def test_a_flaky_verdict_covers_only_observations_with_a_green_on_their_own_sha(hists):        # B2
    root, entry, head = hists(V2)
    prev = G(root, "rev-parse", "HEAD~1")
    runs = [run_row(1, sha=prev, **G1), run_row(2, sha=prev, **GREEN), run_row(3, sha=head, **G1)]
    apply(root, entry, head, runs, [verdict(v="flaky")])
    c = tq.status_data(root, TODAY)["cohorts"][0]
    assert [o["pipeline"] for o in c["unexamined"]] == [3] and {r for r, ok, _ in c["rules"] if not ok} == {"R3"} and not c["ready"]
    assert not any("READY" in line for line in tq.status_line(root, TODAY))
    apply(root, entry, head, [*runs, run_row(4, sha=head, **GREEN)], [verdict(v="flaky")])    # control: the green on the later sha
    assert tq.status_data(root, TODAY)["cohorts"][0]["ready"] is True


def _alerts_of(tmp_path, pulls, today, **kw):
    root = plain_root(tmp_path, pulls=pulls, **kw)                                              # entered 2026-11-20, limit 8 d
    return [a for a in tq.status_data(root, today)["alerts"] if "the watch" in a]


ALERT_WORLDS = {   # B3: pulls, today, fires
    "no-pull-8d": ([], date(2026, 11, 28), False),
    "no-pull-9d": ([], date(2026, 11, 29), True),
    "only-refused-9d": ([pull(at="2026-11-26T08:00:00", ci="token_refused", newest=None)], date(2026, 11, 29), True),
    "only-unreachable-young": ([pull(at="2026-11-24T08:00:00", ci="unreachable", newest=None)], date(2026, 11, 25), False),
    "last-good-pull-then-a-month-of-failures": ([pull(at="2026-11-21T08:00:00", newest="2026-11-21T03:00:00Z"),
                                                 pull(at="2026-11-30T08:00:00", ci="unreachable", newest=None)], date(2026, 12, 1), True),
    "good-recent-pull-control": ([pull(at="2026-11-24T08:00:00")], date(2026, 11, 25), False),
}


@pytest.mark.parametrize("case", ALERT_WORLDS)
def test_watch_alert_worlds(tmp_path, case):
    pulls, today, fires = ALERT_WORLDS[case]
    alerts = _alerts_of(tmp_path, pulls, today)
    assert bool(alerts) is fires, alerts
    assert not fires or "cannot be confirmed" in alerts[0]


def test_watch_alert_is_computed_from_the_recorded_rows_without_ci(tmp_path, capsys):
    root = plain_root(tmp_path, pulls=[pull(at="2026-11-30T08:00:00", ci="unreachable", newest=None)])
    assert tq.main(["status", "--root", str(root)], today=date(2026, 12, 1)) == 1               # no git here: the cohort is unknown, exit 1 (N10)
    assert "TEST QUARANTINE ALERT: the watch cannot be confirmed on CI" in capsys.readouterr().out


def test_config_ci_other_than_a_read_host_is_an_unknown_with_a_door(tmp_path):
    root = plain_root(tmp_path)
    W(root, tq.CONFIG_REL, json.dumps({"ci": "jenkins", "branch": "br", "max_gap_days": 4}))
    d = tq.status_data(root, TODAY)
    assert "reads github and gitlab only" in d["unknown"] and 'set "ci": "github"' in d["unknown"]
    for host in ("gitlab", "github"):                      # both hosts are read (FG7-10)
        W(root, tq.CONFIG_REL, json.dumps({"ci": host, "branch": "br", "max_gap_days": 4}))
        assert tq.status_data(root, TODAY)["unknown"] is None


class FakeGithub(tq.GithubCI):
    """GithubCI with the network replaced by a table {GitHub path: object | bytes}; the GitLab-shaped answers are the real code."""

    def __init__(self, table, root):
        self.root, self._workflow_of, self.table, self.asked = Path(root), {}, table, []

    def _raw(self, path):
        self.asked.append(path)
        if path not in self.table:
            raise tq.CIError("missing", "HTTP 404")
        body = self.table[path]
        return body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")


def _gh_run(rid, event, path, at):
    return {"id": rid, "head_sha": "a" * 40, "event": event, "path": ".github/workflows/" + path, "created_at": at, "head_branch": "br"}


def _zip_of(members):
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, text in members.items():
            z.writestr(name, text)
    return buf.getvalue()


def test_pull_reads_the_watch_runs_of_github_and_asks_no_jobs_of_other_workflows(tmp_path):   # FG7-10
    root = plain_root(tmp_path)
    W(root, tq.CONFIG_REL, json.dumps({"ci": "github", "branch": "br", "max_gap_days": 4}))
    record = {"package_version": "0.10.9", "complete": True, "files": {"test_a.py": "pass"}}
    ci = FakeGithub({
        "/actions/runs?branch=br&per_page=50&page=1": {"workflow_runs": [
            _gh_run(7, "push", "forge-check.yml", "2026-11-24T10:00:00Z"),
            _gh_run(5, "schedule", "quarantine-watch.yml", "2026-11-24T03:00:00Z"),
            _gh_run(4, "workflow_dispatch", "nightly.yml", "2026-11-23T07:00:00Z")]},
        "/actions/runs/5/jobs?per_page=100": {"jobs": [{"id": 51, "name": "quarantine-watch"}, {"id": 52, "name": "quarantine-watch-report"}]},
        "/actions/runs/5/artifacts?per_page=100": {"artifacts": [{"id": 900, "name": "quarantine-watch-report", "expired": False}]},
        "/actions/artifacts/900/zip": _zip_of({"quarantine-watch.json": json.dumps(record)}),
    }, root)
    code, lines = tq.pull(root, ci=ci, today=TODAY)
    rows = watch_rows(root)
    assert code == 0, lines
    assert [r["kind"] for r in rows] == ["run", "pull"]
    assert rows[0]["pipeline"] == 5 and rows[0]["source"] == "schedule" and rows[0]["complete"] is True and rows[0]["files"] == record["files"]
    assert rows[1]["ci"] == "ok" and rows[1]["newest_watch_pipeline"] == 5
    assert not [p for p in ci.asked if p.startswith(("/actions/runs/7/", "/actions/runs/4/"))]     # no request per foreign run


def test_github_reader_answers_the_shapes_the_readers_ask(tmp_path):                            # FG7-10: both forms of the answer
    root = plain_root(tmp_path)
    W(root, ".github/workflows/quarantine-watch.yml", "on:\n  schedule:\n    - cron: \"0 3 * * 1,4\"\n")
    table = {"/actions/runs/5": _gh_run(5, "workflow_dispatch", "quarantine-watch.yml", "2026-11-12T03:00:00Z"),
             "/actions/runs/7": _gh_run(7, "push", "forge-check.yml", "2026-11-24T10:00:00Z"),
             "/actions/workflows/quarantine-watch.yml": {"state": "active"}, "": {"default_branch": "br"},
             "/actions/runs/5/artifacts?per_page=100": {"artifacts": [{"id": 1, "name": "quarantine-watch-report", "expired": True}]}}
    ci = FakeGithub(table, root)
    assert ci.pipeline_sha(5) == "a" * 40
    assert json.loads(ci._get("/pipelines/5"))["source"] == "web"                               # a dispatch is the GitLab "web"
    assert ci.pipeline_variables(5) == {"QUARANTINE_WATCH": "1"} and ci.pipeline_variables(7) == {}
    assert ORIG_SCHEDULES("br", ci) == "ok" and ORIG_SCHEDULES("other", ci) == "missing"
    table["/actions/workflows/quarantine-watch.yml"] = {"state": "disabled_manually"}
    assert ORIG_SCHEDULES("br", ci) == "missing"
    del table["/actions/workflows/quarantine-watch.yml"]
    assert ORIG_SCHEDULES("br", ci) == "unknown"                                                # CI could not be read: never a pass
    with pytest.raises(tq.CIError) as exc:
        ci.artifact(5, "quarantine-watch-report", "ci-out/quarantine-watch.json")              # an expired artifact is missing
    assert exc.value.kind == "missing"
    with pytest.raises(tq.CIError):
        ci._get("/merge_requests")                                                             # no GitHub form: said, not guessed


def test_pull_reads_a_recorded_pipeline_again_when_asked_and_the_flaky_door_works(tmp_path, capsys):   # N4
    root = plain_root(tmp_path)
    first = dict(REC, files={"test_q1.py": red("a")})
    ci = WatchCI([P1], {11: first})
    assert tq.main(["pull", "--root", str(root)], ci=ci, today=TODAY) == 0
    base = ["--root", str(root), "--pipeline", "11"]
    assert tq.main(["judge", "test_q1.py", *base, "--verdict", "flaky", "--by", "opus", "--reason", "r"]) == 1       # no green on the sha yet
    assert "pull --pipeline 11" in capsys.readouterr().out
    ci.records[11] = dict(REC, files={"test_q1.py": {"status": "green"}})                       # the job was retried: same pipeline, new record
    assert tq.main(["pull", *base], ci=ci, today=TODAY) == 0
    assert [(r["kind"], r.get("retry")) for r in watch_rows(root)] == [("run", None), ("pull", None), ("run", 1), ("pull", None)]
    assert tq.main(["judge", "test_q1.py", *base, "--verdict", "flaky", "--by", "opus", "--reason", "r"]) == 0
    assert tq.main(["pull", *base], ci=ci, today=TODAY) == 0                                    # unchanged record: nothing new
    assert [r["kind"] for r in watch_rows(root)].count("run") == 2


def test_pull_newest_watch_time_comes_from_recorded_runs_only(tmp_path):                       # B3 (d)
    root = plain_root(tmp_path)
    assert tq.main(["pull", "--root", str(root)], ci=WatchCI([P1], {}), today=TODAY) == 0       # the pipeline has no record
    assert watch_rows(root)[-1]["newest_watch_pipeline"] is None and watch_rows(root)[-1]["newest_watch_at"] is None


def test_enter_refuses_before_writing_when_a_kept_file_imports_a_moving_one(tmp_path, capsys):   # N2
    root, ci = enter_world(tmp_path)
    W(root, T + "test_gate.py", "import test_old1\n")
    before = Path(root, tq.LAYERS_REL).read_text()
    for extra in ([], ["--dry-run"]):
        assert tq.main(["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101", *extra], ci=ci) == 1
        assert "import a file about to move (test_gate.py->test_old1.py)" in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()


def test_pin_held_importer_counts_as_a_kept_file_in_r6_and_held_by_import(tmp_path):            # N3
    root, entry = repo(tmp_path)
    W(root, T + "test_p.py", "import test_q1\n")
    apply(root, entry, entry, pins={"test_p.py": {"why": "pin"}})
    assert tq.held_by_import(root) == [("test_p.py", "test_q1.py")]
    c = tq.status_data(root, TODAY)["cohorts"][0]
    assert "R6" in {r for r, ok, _ in c["rules"] if not ok} and not c["ready"]


def test_check_new_import_edge_from_a_pin_held_file(tmp_path, capsys):                          # N3, the K5 edge check
    root, entry = repo(tmp_path)
    commit(root, "pin file", **{(T + "test_p.py").replace("/", "__"): "# p\n"})
    commit(root, "quarantine-enter: init", **{LK: layers_json(entry=entry, pins={"test_p.py": {"why": "pin"}})})
    assert tq.main(["check", "--root", str(root)]) == 0
    edit(root, "edge", "test_p.py", "import test_q1\n")
    assert tq.main(["check", "--root", str(root)]) == 1
    assert "new import edge test_p.py -> test_q1.py" in capsys.readouterr().out


def test_status_on_a_root_without_the_package_names_what_is_missing_and_the_door(tmp_path, monkeypatch):   # debt 4
    root = tmp_path / "np"
    W(root, tq.LAYERS_REL, layers_json())
    monkeypatch.setattr(tq, "_pkg_module", PG_REAL_PKG)
    lines = tq.status_line(root, TODAY)
    assert len(lines) == 1 and "selftest.py is missing" in lines[0] and "run from a checkout that holds ai-packages/qa-factory" in lines[0]
    Path(root, tq.LAYERS_REL).unlink()
    assert tq.status_line(root, TODAY) == []                                                    # no layers file: no lines, no package needed


STORY_FILE = "ai-packages/qa-factory/scripts/tests/fixtures/stories/s1/"
RED = {"stage": "S7", "facet": "accepted", "evidence": "work/triage.json"}
RED_CASES = {      # red_then in story.json, not_walked rows, files of the story folder -> is the red Then carried (coverage item red_then)
    "covered": (RED, [], ["work/triage.json"], True),
    "no-red_then-key": (None, [], ["work/triage.json"], False),
    "stage-not-walked": (dict(RED, stage="S6"), [], ["work/triage.json"], False),
    "facet-not-walked": (dict(RED, facet="handed"), [], ["work/triage.json"], False),
    "facet-listed-as-not-walked": (RED, [{"stage": "S7", "facet": "accepted", "why": "w"}], ["work/triage.json"], False),
    "evidence-missing": (RED, [], [], False),
    "evidence-outside-the-story": (dict(RED, evidence="../s2/triage.json"), [], ["../s2/triage.json"], False),
    "evidence-absolute": (dict(RED, evidence="/etc/hosts"), [], [], False),
    "red_then-not-an-object": ("S7/accepted", [], ["work/triage.json"], False),
    "red_then-without-evidence": ({"stage": "S7", "facet": "accepted"}, [], ["work/triage.json"], False),
}


@pytest.mark.parametrize("case", RED_CASES)
def test_story_facets_red_then_is_carried_by_a_walked_facet_and_its_evidence(tmp_path, case):
    red, not_walked, files, want = RED_CASES[case]
    story = {"id": "s1", "task": "T", "synthetic": True, "walk": [{"stage": "S7", "facets": ["accepted"]}], "not_walked": not_walked}
    if red is not None:
        story["red_then"] = red
    W(tmp_path, STORY_FILE + "story.json", json.dumps(story))
    for rel in files:
        W(tmp_path, STORY_FILE + rel, "{}")
    synthetic, got = tq._story_facets(tmp_path, "test_scenario_s1.py", walker=lambda sid, base: [R("s1/S7/accepted (red then: 3 rows)")])
    assert synthetic is True
    assert tq._covered_required(["red_then"], got) == ([] if want else ["red_then"])
    assert ("S7", "accepted") in got or not_walked                                             # the walk itself is untouched


def _facets_of(tmp_path, results, red=None, walk=(("S7", "accepted"),), folder="local-1-0108", evidence=True):
    story = {"id": "s1", "task": "T", "synthetic": True, "walk": [{"stage": s, "facets": [f]} for s, f in walk]}
    if red:
        story["red_then"] = red
    sdir = "ai-packages/qa-factory/scripts/tests/fixtures/stories/" + folder + "/"
    W(tmp_path, sdir + "story.json", json.dumps(story))
    if evidence:
        W(tmp_path, sdir + "work/triage.json", "{}")
    seen = []

    def walker(sid, base):
        seen.append((sid, Path(base).name))
        if isinstance(results, Exception):
            raise results
        return results
    out = tq._story_facets(tmp_path, "test_scenario_" + folder.replace("-", "_") + ".py", walker=walker)
    assert seen == [(folder, "stories")]                                                        # the folder name, hyphens kept
    return out


P = "local-1-0108/S7/accepted"
FACET_CASES = {
    "pass-counts": ([R(P)], {("S7", "accepted")}),
    "note-only-not-counted": ([R(P, "note")], set()),
    "fail-not-counted": ([R(P, "fail")], set()),
    "pass-and-fail-not-counted": ([R(P), R(P, "fail")], set()),
    "final-state-suffix-counts": ([R(P + " (final state)")], {("S7", "accepted")}),
    "amended-suffix-counts": ([R(P + " (amended: x)")], {("S7", "accepted")}),
    "world-changed-not-counted": ([R(P + "/world-changed")], set()),
    "variant-not-counted": ([R("local-1-0108/variant/v1")], set()),
    "amendments-load-not-counted": ([R("local-1-0108/amendments"), R("local-1-0108/load")], set()),
    "longer-facet-name-not-counted": ([R(P + "-more")], set()),
    "pair-not-listed-not-counted": ([R("local-1-0108/S7/handed")], set()),
    "empty-walk-result": ([], set()),
    "walker-raises": (RuntimeError("boom"), set()),
}


@pytest.mark.parametrize("case", FACET_CASES)
def test_story_facets_counts_only_pairs_a_walk_pass_judged(tmp_path, case):
    results, want = FACET_CASES[case]
    synthetic, got = _facets_of(tmp_path, results)
    assert synthetic is True and got == want


RED_WALK = {"stage": "S7", "facet": "accepted", "evidence": "work/triage.json"}
RED_MARK_CASES = {
    "rows-covers": ([R(P + " (red then: 2 rows)")], True),
    "not-a-triage-file-does-not-cover": ([R(P + " (red then: evidence is not a triage file)")], False),
    "zero-rows-does-not-cover": ([R(P + " (red then: 0 rows)")], False),
    "no-mark-does-not-cover": ([R(P)], False),
    "pair-is-a-note": ([R(P + " (red then: 2 rows)", "note")], False),
}


@pytest.mark.parametrize("case", RED_MARK_CASES)
def test_story_facets_red_then_needs_the_mark_with_rows_on_the_pass_of_its_pair(tmp_path, case):
    results, want = RED_MARK_CASES[case]
    _, got = _facets_of(tmp_path, results, red=RED_WALK)
    assert ((tq.RED_THEN, tq.RED_THEN) in got) is want


def test_story_facets_red_mark_without_the_evidence_file_does_not_cover(tmp_path):
    _, got = _facets_of(tmp_path, [R(P + " (red then: 2 rows)")], red=RED_WALK, evidence=False)
    assert (tq.RED_THEN, tq.RED_THEN) not in got and ("S7", "accepted") in got


def test_covered_required_red_then_is_not_a_facet_name_any_more():
    assert tq._covered_required(["red_then", "S7"], {("S7", "red_then")}) == ["red_then"]       # the old, uncountable form no longer covers it
    assert tq._covered_required(["red_then"], {("red_then", "red_then")}) == []


# --- the TD-15 theme 3 debts (t-2514): blob cache, status exit, absent file, paging, scope, no-package line --------------------------------

def test_check_history_reads_each_blob_once_and_keeps_its_verdicts(tmp_path, monkeypatch):      # debt 1
    root, entry = repo(tmp_path)
    keep = tuple("test_k%02d.py" % i for i in range(12))
    for n in keep:
        W(root, T + n, f"# {n}\n")
    commit(root, "quarantine-enter: init", **{LK: layers_json(entry=entry, keep=keep)})
    c1 = edit(root, "plain")                                                                    # a quarantined file edited, no door
    c2 = edit(root, "edge", "test_k00.py", "import test_q1\n")                                  # a new kept -> quarantined import edge
    edit(root, "again", "test_k01.py", "# changed\n")                                           # touches tests, adds no edge
    want = [(c1, "quarantined file test_q1.py was changed, deleted or renamed -- expected a line 'quarantine-edit: test_q1.py -- <reason>' "
                 "(the bare file name, no folder) in this commit message"),
            (c2, "new import edge test_k00.py -> test_q1.py (kept -> quarantined) -- expected 'quarantine-import: test_k00.py -> test_q1.py -- <reason>'")]
    calls = []
    real = tq._git
    monkeypatch.setattr(tq, "_git", lambda r, *a: calls.append(a) or real(r, *a))
    assert tq.check_history(root) == want                                                       # the same result object as before the cache
    blob_reads = [a for a in calls if a[0] == "cat-file"]
    assert len(blob_reads) == len({a[-1] for a in blob_reads})                                  # no blob is read twice
    assert not any(a[0] == "show" and "/test_k" in a[-1] for a in calls)                        # no `git show` per keep file any more
    assert len(calls) <= 45, len(calls)                                                         # 6 revisions x (12 keep files) was 70+ calls before


def test_status_exits_1_when_a_cohort_is_unknown_and_0_for_known_ones(hists, capsys):          # N10
    sfx, entry, head = hists(("0.11.0", "0.12.0-rc1"))                                          # a version suffix: the cohort is unknown
    apply(sfx, entry, head, [run_row(1, **GREEN)])
    assert tq.main(["status", "--root", str(sfx)], today=TODAY) == 1
    assert "status unknown" in capsys.readouterr().out
    root, entry, head = hists(V2)
    apply(root, entry, head, [run_row(1, **G1)], [verdict()])
    assert tq.main(["status", "--root", str(root)], today=TODAY) == 0                           # known cohort: still 0
    apply(root, entry, head, [run_row(1, **GREEN)])
    assert tq.main(["status", "--root", str(root)], today=TODAY) == 0                           # known and not ready: 0 as well


def _paged(n_pipelines, size=50):
    """CI holding n pipelines, NEWEST FIRST like GitLab (ids and times grow with the id), `size` rows a page (the page size the code asks for)."""
    rows = [(i, "schedule", "2026-11-24T%02d:%02d:00Z" % (i // 60, i % 60), True) for i in range(n_pipelines, 0, -1)]
    return WatchCI(rows, {i: REC for i, *_ in rows}, page_size=size)


def _list_calls(ci):
    return len([c for c in ci.calls if c.startswith("/pipelines?ref=")])


PAGES = {   # pipelines held by CI, floor id (None = no floor) -> (list calls made, pipelines found, cap hit)
    "one-partial-page": (30, None, 1, 30, False),
    "one-full-page-then-an-empty-one": (50, None, 2, 50, False),
    "two-pages-the-second-partial": (75, None, 2, 75, False),
    "nine-full-pages-then-an-empty-page": (450, None, 10, 450, False),
    "ten-full-pages-the-cap": (500, None, 10, 500, True),
    "eleven-pages-beyond-the-cap": (550, None, 10, 500, True),
    "partial-tenth-page-is-the-end": (460, None, 10, 460, False),
    "floor-on-page-2-of-a-600-long-list": (600, 520, 2, 80, False),          # ids 521..600 are newer than the floor; row 520 is on page 2
    "floor-on-page-1": (600, 580, 1, 20, False),
    "floor-is-the-newest-nothing-new": (600, 600, 1, 0, False),
    "ten-full-pages-all-above-the-floor": (600, 50, 10, 500, True),         # the floor (id 50) is on page 12: not reached, a real cut
}


@pytest.mark.parametrize("case", PAGES)
def test_ci_pipelines_paging_stops_at_the_floor_a_short_page_or_the_cap(case):                  # N5, B1
    held, floor_id, read, found, hit = PAGES[case]
    ci, capped = _paged(held), []
    after = None if floor_id is None else "2026-11-24T%02d:%02d:00Z" % (floor_id // 60, floor_id % 60)
    got = tq._ci_pipelines("br", tq.WATCH_SOURCES, ci, after=after, capped=capped)
    assert (_list_calls(ci), len(got), bool(capped)) == (read, found, hit)
    if hit:
        assert "cut at 10 pages of 50 (500 pipelines)" in capped[0] and "pull --pipeline <id>" in capped[0]
    assert ci.calls[0] == "/pipelines?ref=br&per_page=50" and "/pipelines?ref=br&per_page=50&page=%d" % (read + 1) not in ci.calls


def test_ci_pipelines_exactly_ten_full_pages_is_reported_cut_the_eleventh_is_not_read():              # B1: never "complete" on an unknown
    ci, capped = _paged(500), []
    tq._ci_pipelines("br", tq.WATCH_SOURCES, ci, capped=capped)
    assert len(capped) == 1 and _list_calls(ci) == 10


def test_ci_pipelines_empty_first_page_is_no_pipelines_and_no_cap():
    ci, capped = WatchCI([]), []
    assert tq._ci_pipelines("br", tq.WATCH_SOURCES, ci, capped=capped) == [] and capped == []
    assert [c for c in ci.calls if c.startswith("/pipelines?ref=")] == ["/pipelines?ref=br&per_page=50"]


def test_pull_reads_a_second_page_and_refuses_to_call_a_cut_list_complete(tmp_path, capsys):   # N5
    root = plain_root(tmp_path)
    assert tq.main(["pull", "--root", str(root)], ci=_paged(4), today=TODAY) == 0
    assert [r["kind"] for r in watch_rows(root)].count("run") == 4
    root2 = tmp_path / "other"
    root2.mkdir()
    root2 = plain_root(root2)
    capsys.readouterr()
    assert tq.main(["pull", "--root", str(root2)], ci=_paged(550), today=TODAY) == 1            # 11 pages held, 10 read
    out = capsys.readouterr().out
    assert "pull: the pipeline list of br was cut at 10 pages of 50 (500 pipelines)" in out
    assert [r["kind"] for r in watch_rows(root2)].count("run") == 500                           # what was read is still recorded


def test_ls_tree_reads_a_path_with_a_space_and_a_non_ascii_character_and_skips_a_nested_one(tmp_path):   # N6
    root = tmp_path / "lt"
    root.mkdir()
    G(root, "init", "-q")
    names = ["test_plain.py", "test_a b.py", "test_café.py"]
    for n in names:
        W(root, T + n, "# %s\n" % n)
    W(root, T + "fixtures/test_nested.py", "# nested\n")
    commit(root, "tree")
    got = tq._tree_blobs(root, "HEAD", {})
    assert sorted(got) == sorted(names)                                                         # not quoted, not dropped; the nested file is not a top-level one
    assert all(re.fullmatch(r"[0-9a-f]{40}", sha) for sha in got.values())


def _scope_world(tmp_path, variables, report):
    root, ci = enter_world(tmp_path)
    ci.variables, ci.report = variables, report
    return root, ci


SCOPES = {   # variables of the coverage pipeline, report text -> (exit, text in the output)
    "variable-keep": ({"REDUNDANCY_SCOPE": "keep"}, REPORT, 0, "dry run"),
    "header-keep-variables-unreadable": (tq.CIError("token_refused"), "- scope: keep\n" + REPORT, 0, "dry run"),
    "measured-variable-beats-a-header-line": ({"REDUNDANCY_SCOPE": "full"}, "- scope: keep\n" + REPORT, 1, "ran with scope 'full', not keep"),
    "measured-keep-beats-a-header-other": ({"REDUNDANCY_SCOPE": "keep"}, "- scope: full\n" + REPORT, 0, "dry run"),
    "unreadable-variables-and-no-header": (tq.CIError("token_refused"), REPORT, 1, SCOPE_DOOR),
    "variable-other": ({"REDUNDANCY_SCOPE": "all"}, REPORT, 1, "ran with scope 'all', not keep"),
    "variable-absent-is-the-full-scope": ({}, REPORT, 1, "ran with scope 'full', not keep"),
    "unknown": (tq.CIError("missing"), REPORT, 1, SCOPE_DOOR),
}


@pytest.mark.parametrize("case", SCOPES)
def test_enter_checks_the_coverage_scope_and_never_passes_on_an_unknown(tmp_path, capsys, case):   # N6, FR-59
    variables, report, rc, text = SCOPES[case]
    root, ci = _scope_world(tmp_path, variables, report)
    before = Path(root, tq.LAYERS_REL).read_text()
    assert tq.main(["enter", "--root", str(root), "--pipeline", "100", "--coverage-pipeline", "101", "--dry-run"], ci=ci) == rc
    assert text in capsys.readouterr().out
    assert Path(root, tq.LAYERS_REL).read_text() == before and not Path(root, "ci-out/quarantine-enter-msg.txt").exists()


def test_status_line_on_a_root_without_layers_and_without_the_package_loads_nothing(tmp_path, monkeypatch):   # debt 5
    def forbidden(*a, **k):
        raise AssertionError("the package selftest must not be loaded when there is no test-layers.json")
    monkeypatch.setattr(tq, "_pkg_module", forbidden)
    assert tq.status_line(tmp_path / "nothing-here", TODAY) == []
    assert tq.main(["status", "--root", str(tmp_path / "nothing-here")]) == 0
