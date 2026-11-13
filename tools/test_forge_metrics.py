"""Tests for tools/forge_metrics.py (spec docs/tasks/specs/t-306-forge-metrics-v0.md, keys K1..K10
of the spec and its owner amendment) and for the WARN-only `feature` rule of
tools/journal_validator.py (K6).

Run from the repo root: python -m pytest tools/test_forge_metrics.py -q
"""
from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

import importlib.util

import journal_keys as jk
import journal_validator as jv

# TEMPORAL (B-402): until the Lead places the proposed module on the live path, the code under
# test is tools/forge_metrics.proposed.py (loaded by path); once that file is gone, the live module
# is imported. Both worlds must pass.
_PROPOSED = Path(__file__).resolve().parent / "forge_metrics.proposed.py"


def _load_fm():
    if _PROPOSED.exists():
        spec = importlib.util.spec_from_file_location("forge_metrics_proposed", _PROPOSED)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    import forge_metrics
    return forge_metrics


fm = _load_fm()

ROOT = Path(__file__).resolve().parent.parent
HAVE_GIT = shutil.which("git") is not None
needs_git = pytest.mark.skipif(not HAVE_GIT, reason="git is not installed")
# TEMPORAL (cutover O3, GM2-4): the journal does not travel to the new repository -- a fresh clone has no
# logs/routing-log.jsonl at all. The two tests that read THIS repo's journal skip there (nothing to read);
# every other test builds its own journal under tmp_path. Both worlds pass: here and in the clone.
needs_repo_journal = pytest.mark.skipif(not (ROOT / jv.JOURNAL_PATH).exists(),
                                        reason=f"{jv.JOURNAL_PATH} is not in this checkout (the journal does not "
                                               "travel to a fresh clone, cutover O3); nothing to read")


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------

def feat(fid, name, globs, root="package", stages=(), words=()):
    return {"id": fid, "name": name, "root": root, "globs": list(globs),
            "stages": list(stages), "words": list(words)}


def write_registry(path: Path, features) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema_version": 1, "features": features}), encoding="utf-8")
    return path


def reg(tmp_path, features):
    return fm.load_registry(write_registry(tmp_path / "plans" / "features.json", features))


def git(cwd, *args, date=None):
    env = dict(os.environ)
    if date:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    proc = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false", *args],
                          cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", env=env)
    assert proc.returncode == 0, f"git {args} failed: {proc.stderr}"
    return proc.stdout.strip()


def init_repo(path: Path, branch="main"):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "-b", branch)
    return path


def put(root: Path, rel: str, text: str = "x\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def commit_all(root: Path, msg: str, date: str):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg, date=date)
    return git(root, "rev-parse", "HEAD")


def ev_line(ts, tid, event="delegated", **kw):
    d = {"ts": ts, "event": event, "agent": "builder", "category": "implementation",
         "notes": "note " + tid, "task_id": tid, "model": "sonnet", "worker_ref": "cli:" + ts}
    d.update(kw)
    return json.dumps(d, ensure_ascii=False)


# ---------------------------------------------------------------------------------------------
# K1 -- the registry validates, no overlaps on the shipped table
# ---------------------------------------------------------------------------------------------

def test_k1_shipped_registry_validates_and_has_f01_to_f20():
    feats = fm.load_registry(ROOT / fm.REGISTRY_REL)
    ids = [f["id"] for f in feats]
    # Contiguous from F01, unique; the COUNT is not pinned: a new feature (F21 Codex/host, 02.10) is
    # registered by whoever brings it, and the registry must grow without breaking this test.
    assert sorted(ids) == [f"F{n:02d}" for n in range(1, len(ids) + 1)]
    assert len(ids) >= 20
    assert len(set(ids)) == len(ids)
    assert [f for f in feats if f["root"] == "repo"] and [f for f in feats if f["id"] == "F19"][0]["root"] == "repo"


def test_k1_shipped_registry_has_no_overlaps_across_the_package_file_list():
    feats = fm.load_registry(ROOT / fm.REGISTRY_REL)
    files = fm.package_files(ROOT)
    assert len(files) > 100, "the package walk found nothing -- a vacuous pass"
    assert fm.find_overlaps(feats, files) == []


def test_k1_negative_control_two_identical_globs_are_reported(tmp_path):
    feats = reg(tmp_path, [feat("F01", "a", ["scripts/x.py"]), feat("F02", "b", ["scripts/x.py"])])
    found = fm.find_overlaps(feats, [fm.PACKAGE + "/scripts/x.py", fm.PACKAGE + "/scripts/y.py"])
    assert [o["path"] for o in found] == [fm.PACKAGE + "/scripts/x.py"]
    assert found[0]["kind"] == "overlap" and found[0]["features"] == ["F01", "F02"]
    # the first feature in registry order wins the attribution
    assert fm.classify_path(feats, fm.PACKAGE + "/scripts/x.py") == "F01"


def test_k1_a_general_glob_ahead_of_a_specific_one_is_reported_as_shadowed(tmp_path):
    feats = reg(tmp_path, [feat("F01", "gen", ["scripts/*.py"]), feat("F02", "spec", ["scripts/story_run.py"])])
    found = fm.find_overlaps(feats, [fm.PACKAGE + "/scripts/story_run.py"])
    assert found and found[0]["kind"] == "shadowed"


def test_k1_shipped_registry_has_no_unattributed_tracked_package_file():
    """F6-49: the REAL registry covers every tracked package file (the direction t-1411 left red)."""
    tracked = fm.tracked_files(ROOT)
    if not tracked:
        pytest.skip("git ls-files is unavailable or empty here")
    feats = fm.load_registry(ROOT / fm.REGISTRY_REL)
    assert any(fm.split_root(p)[0] == "package" for p in tracked), "no package file tracked -- a vacuous pass"
    assert fm.unattributed_package_files(feats, tracked) == []


@pytest.mark.parametrize("tracked, offenders, warned", [
    (["ai-packages/qa-factory/scripts/x.py", "ai-packages/qa-factory/scripts/z.py"],
     ["ai-packages/qa-factory/scripts/z.py"], False),                                  # unattributed file reported
    (["ai-packages/qa-factory/scripts/x.py", "docs/other.md"], [], False),             # clean; a non-package file is not judged
    ([], [], True),                                                                    # empty ls-files: not checked, no fail
    (None, [], True),                                                                  # unavailable: not checked, no fail
], ids=["unattributed", "clean", "ls-files-empty", "ls-files-unavailable"])
@needs_git
def test_check_direction_d_tracked_package_files(tmp_path, monkeypatch, tracked, offenders, warned):
    root, base = _frepo(tmp_path)
    feats = reg(tmp_path, [feat("F01", "a", ["scripts/x.py"])])
    monkeypatch.setattr(fm, "tracked_files", lambda _root: tracked)
    found, _counts, _sha, warnings = fm.run_check(root, base, features=feats)
    assert [o[1] for o in found if o[0] == "d"] == offenders
    for o in found:
        if o[0] == "d":
            assert "matches no feature" in o[2] and "expected: add it to a feature in plans/features.json" in o[2]
    assert any(w.startswith("not checked: (d)") for w in warnings) is warned


def test_glob_semantics():
    rx, spec = fm.compile_glob("scripts/tests/test_*.py")
    assert rx.match("scripts/tests/test_a.py") and not rx.match("scripts/tests/sub/test_a.py")
    assert spec == len("scripts/tests/test_.py")
    rx2, _ = fm.compile_glob("tools/**")
    assert rx2.match("tools/a/b.py") and not rx2.match("toolsx/a.py")
    rx3, _ = fm.compile_glob("*")
    assert rx3.match("CLAUDE.md") and not rx3.match("a/b.md")


# ---------------------------------------------------------------------------------------------
# registry edges (spec section 7)
# ---------------------------------------------------------------------------------------------

def test_registry_missing_exits_2_names_the_file_and_writes_nothing(tmp_path, capsys):
    out = tmp_path / "out.md"
    rc = fm.main(["--write", "--out", str(out)], root=tmp_path)
    err = capsys.readouterr().err
    assert rc == 2 and not out.exists()
    assert "features.json" in err and "expected shape" in err


def test_registry_malformed_exits_2_nothing_written(tmp_path, capsys):
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "features.json").write_text("{not json", encoding="utf-8")
    out = tmp_path / "out.md"
    assert fm.main(["--write", "--out", str(out)], root=tmp_path) == 2
    assert not out.exists() and "not valid JSON" in capsys.readouterr().err
    write_registry(tmp_path / "plans" / "features.json", [{"id": "F1", "name": "x", "globs": ["a"]}])
    assert fm.main(["--write", "--out", str(out)], root=tmp_path) == 2
    assert not out.exists()


# ---------------------------------------------------------------------------------------------
# K2 -- row attribution order
# ---------------------------------------------------------------------------------------------

def _two(tmp_path):
    feats = reg(tmp_path, [
        feat("F05", "controller", ["scripts/controller.py"], stages=["S2"], words=["контроллер"]),
        feat("F06", "driver", ["scripts/story_run.py"], words=["драйвер"]),
        feat("F07", "questions", ["scripts/gate_brief.py"], words=["вопрос"]),
    ])
    index = fm.FileIndex([fm.PACKAGE + "/scripts/controller.py", fm.PACKAGE + "/scripts/story_run.py",
                          fm.PACKAGE + "/scripts/gate_brief.py"])
    return feats, index


def test_k2_tag_wins_over_files(tmp_path):
    feats, index = _two(tmp_path)
    a = fm.attribute_text("`story_run.py` падает [F07]", feats, index)
    assert (a["feature"], a["by"]) == ("F07", "tag")


def test_k2_files_only_and_second_feature_goes_to_also(tmp_path):
    feats, index = _two(tmp_path)
    a = fm.attribute_text("правка в `story_run.py` и `controller.py`", feats, index)
    assert (a["feature"], a["by"], a["also"]) == ("F05", "files", ["F06"])   # first in registry order


def test_k2_words_only_then_seed_then_none(tmp_path):
    feats, index = _two(tmp_path)
    assert fm.attribute_text("вопрос человеку непонятен", feats, index)["by"] == "words"
    a = fm.attribute_text("вопрос на стадии S2 и S2", feats, index)
    assert (a["feature"], a["by"]) == ("F05", "words")           # two stage hits beat one word
    a = fm.attribute_text("нет ничего узнаваемого", feats, index, seed_feature="F06")
    assert (a["feature"], a["by"]) == ("F06", "seed")
    a = fm.attribute_text("нет ничего узнаваемого", feats, index)
    assert (a["feature"], a["by"]) == (None, "none")


def test_k2_an_unregistered_tag_is_not_a_tag(tmp_path):
    feats, index = _two(tmp_path)
    assert fm.attribute_text("see [F99] and FR-12", feats, index)["by"] == "none"


def test_token_resolution_handles_line_numbers_and_module_function(tmp_path):
    index = fm.FileIndex([fm.PACKAGE + "/scripts/check_delivery.py", "tools/kb_publish.py"])
    assert index.resolve("`check_delivery.reason_owner()`") == [fm.PACKAGE + "/scripts/check_delivery.py"]
    assert index.resolve("story_run.py:2026") == []
    assert index.resolve("tools/kb_publish.py:12-40") == ["tools/kb_publish.py"]
    assert index.resolve("check_delivery") == [fm.PACKAGE + "/scripts/check_delivery.py"]


def test_backlog_row_parsing_skips_non_utf8_and_keeps_line_number():
    raw = ("| B-001 | text `a.py` | src | новое, 30.09 | P1 |\n").encode("utf-8") + \
          b"| B-002 | bad \xff\xfe bytes | src | st |\n" + \
          ("| B-003 | ok | src | st | P1 |\n").encode("utf-8")
    rows, skipped = fm.parse_backlog_text(raw)
    assert [r["id"] for r in rows] == ["B-001", "B-003"] and skipped == [2]
    assert fm.row_date(rows[0]) == "2026-09-30"


def test_row_closure_and_live_marks():
    rows, _ = fm.parse_backlog_text("| B-001 | Сделано 30.09: ok | найдено живьём | st | |\n".encode("utf-8"))
    r = fm.attribute_rows(rows, [feat_compiled()], fm.FileIndex([]), {})[0]
    assert r["closed"] and r["live"]


def feat_compiled():
    return {"id": "F01", "name": "x", "root": "package", "globs": ["a"], "stages": [], "words": [],
            "_globs": [("a",) + fm.compile_glob("a")]}


# ---------------------------------------------------------------------------------------------
# K3 -- the oracle: Table C of the hand attribution
# ---------------------------------------------------------------------------------------------

# Files of Table C whose registry feature differs from the table's, with the reason. EMPTY: the
# shipped registry reproduces all 65 oracle rows (the 66th, test_role_commands.py, is "n/c" in
# the table, so there is no oracle for it). The spec allows at most 5.
K3_EXCEPTIONS: dict = {}


def test_k3_table_c_oracle():
    rows = fm.parse_seed_table_c(ROOT / fm.SEED_REL)
    if not rows:
        pytest.skip(f"{fm.SEED_REL} is not in this checkout (the seed is optional); no oracle to compare")
    assert len(rows) >= 60, f"Table C parsed to {len(rows)} rows -- the parser lost the table"
    feats = fm.load_registry(ROOT / fm.REGISTRY_REL)
    mismatched = {}
    for rel, want in rows:
        if want == "n/c":
            continue
        got = fm.classify_path(feats, fm.PACKAGE + "/" + rel)
        if got != want:
            mismatched[rel] = (want, got)
    assert len(K3_EXCEPTIONS) <= 5
    assert mismatched == K3_EXCEPTIONS, f"Table C disagrees on {mismatched}"


def test_k3_negative_control_a_wrong_registry_disagrees_with_the_oracle(tmp_path):
    rows = fm.parse_seed_table_c(ROOT / fm.SEED_REL)
    if not rows:
        pytest.skip("seed absent")
    wrong = reg(tmp_path, [feat("F15", "everything", ["**"])])
    bad = [rel for rel, want in rows if want not in ("n/c", "F15")
           and fm.classify_path(wrong, fm.PACKAGE + "/" + rel) != want]
    assert len(bad) > 5


# ---------------------------------------------------------------------------------------------
# K4 -- journal attribution
# ---------------------------------------------------------------------------------------------

def test_k4_journal_attribution(tmp_path):
    feats, index = _two(tmp_path)
    lines = [
        ev_line("2026-10-02T10:00:00", "t-001", feature="F06"),
        ev_line("2026-10-02T10:01:00", "t-002", notes="fix `controller.py` after the run"),
        ev_line("2026-10-02T10:02:00", "t-003", notes="the gates [F07] again"),
        ev_line("2026-10-02T10:03:00", "t-002", event="accepted", notes="ok", worker_ref=None),
        ev_line("2026-10-02T10:04:00", "t-004", notes="nothing recognisable"),
        ev_line("2026-10-02T10:05:00", "t-005", feature="F99", notes="[F06] in notes does not rescue an unknown value"),
    ]
    events, skipped = fm.parse_journal_text("\n".join(lines).encode("utf-8"))
    assert skipped == []
    got = fm.attribute_events(events, feats, index)
    by_line = {e["line"]: e for e in got}
    assert (by_line[1]["feature"], by_line[1]["by"]) == ("F06", "field")
    assert (by_line[2]["feature"], by_line[2]["by"]) == ("F05", "files")
    assert (by_line[3]["feature"], by_line[3]["by"]) == ("F07", "tag")
    assert (by_line[4]["feature"], by_line[4]["by"]) == ("F05", "task")      # inherited from its delegated
    assert (by_line[5]["feature"], by_line[5]["by"]) == (None, "none")
    assert by_line[6]["feature"] is None and by_line[6]["invalid"] == "F99"   # unknown value = unclassified
    assert by_line[4]["key"] == by_line[2]["key"] == ("", "t-002")             # B-402: the key is (label, task_id)


def _collision_lines():
    return [
        ev_line("2026-10-02T10:01:00", "t-002", notes="fix `controller.py` after the run"),             # 1: F05 by files
        ev_line("2026-10-02T10:03:00", "t-002", event="accepted", notes="ok", worker_ref=None),          # 2
        ev_line("2026-10-02T10:06:00", "t-002", notes="a second clone's t-002", worker_ref="cli:other"),  # 3: the other clone
        ev_line("2026-10-02T10:08:00", "t-003", event="defect_found", ref="t-002", notes="late defect"),  # 4: ref to t-002
        ev_line("2026-10-02T10:09:00", "t-004", event="defect_found", ref="t-002@other", notes="late defect"),  # 5
    ]


def _attribute(tmp_path, segments):
    feats, index = _two(tmp_path)
    events, skipped = fm.parse_journal_text("\n".join(_collision_lines()).encode("utf-8"))
    assert skipped == []
    return {e["line"]: e for e in fm.attribute_events(events, feats, index, segments)}


def _declared_other(line_no=3):
    ident = jk.identity(json.loads(_collision_lines()[line_no - 1]))
    return jk.Segments(1, [("other", "t-002 was issued by both clones", (ident,))])


def test_b402_declared_instance_is_its_own_key_and_inherits_nothing(tmp_path):
    got = _attribute(tmp_path, _declared_other())
    assert got[1]["key"] == got[2]["key"] == ("", "t-002") and got[3]["key"] == ("other", "t-002")
    assert (got[2]["feature"], got[2]["by"]) == ("F05", "task")            # the accepted of the undeclared instance
    assert (got[3]["feature"], got[3]["by"]) == (None, "none")             # the other clone's instance: no inheritance


def test_b402_undeclared_collision_is_glued_into_one_instance(tmp_path):
    for segs in (None, jk.NO_SEGMENTS):
        got = _attribute(tmp_path, segs)
        assert got[3]["key"] == ("", "t-002")
        assert (got[3]["feature"], got[3]["by"]) == ("F05", "task")        # glued, as the hooks read it


def test_b402_defect_found_ref_goes_through_ref_key(tmp_path):
    got = _attribute(tmp_path, _declared_other())
    assert (got[4]["feature"], got[4]["by"]) == ("F05", "ref")             # a bare ref: the carrier's (undeclared) side
    assert (got[5]["feature"], got[5]["by"]) == (None, "none")             # t-002@other: that instance has no feature
    got = _attribute(tmp_path, jk.NO_SEGMENTS)
    assert (got[4]["feature"], got[4]["by"]) == ("F05", "ref")
    assert (got[5]["feature"], got[5]["by"]) == (None, "none")             # a label no segment holds names nothing


def test_b402_compute_reads_the_declaration_of_its_root_and_never_fails_on_a_broken_one(tmp_path, capsys):
    feats, _index = _two(tmp_path)
    root = tmp_path / "r"
    (root / "logs").mkdir(parents=True)
    lines = _collision_lines()
    lines[0] = ev_line("2026-10-02T10:01:00", "t-002", feature="F05")                   # attributed by its field
    (root / "logs" / "routing-log.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    base = fm.compute(root, "2026-09-26", use_seed=False, features=feats)
    assert base["unclassified"]["events"]["names"] == ["t-004@5"]                       # lines 2, 3 inherit F05, 4 by ref
    capsys.readouterr()
    (root / "logs" / "journal-segments.json").write_text("{broken", encoding="utf-8")
    again = fm.compute(root, "2026-09-26", use_seed=False, features=feats)
    assert again == base                                                    # a broken file reads as none
    err = capsys.readouterr().err
    assert "the task-key declaration is unreadable" in err and "colliding task ids are read as one task" in err
    (root / "logs" / "journal-segments.json").write_text(jk.dumps_declaration(_declared_other()), encoding="utf-8")
    declared = fm.compute(root, "2026-09-26", use_seed=False, features=feats)
    assert declared["unclassified"]["events"]["names"] == ["t-002@3", "t-004@5"]        # line 3: its own instance now
    assert capsys.readouterr().err == ""


# ---------------------------------------------------------------------------------------------
# K5 -- metrics on a fixture repo
# ---------------------------------------------------------------------------------------------

def _fixture_repo(tmp_path):
    root = init_repo(tmp_path / "r")
    write_registry(root / "plans" / "features.json", [
        feat("F05", "controller", ["scripts/brief_pack.py"]),
        feat("F06", "driver", ["scripts/story_run.py"]),
        feat("F19", "forge", ["docs/**", "plans/**", "tools/**"], root="repo"),
    ])
    pk = root / fm.PACKAGE
    put(pk, "scripts/story_run.py", "a\n")
    put(pk, "scripts/brief_pack.py", "a\n")
    put(pk, "scripts/stray.py", "a\n")
    commit_all(root, "c1", "2026-10-01T12:00:00")
    put(pk, "scripts/story_run.py", "b\n")
    commit_all(root, "c2", "2026-10-02T12:00:00")
    put(pk, "scripts/story_run.py", "c\n")
    put(root, "docs/note.md", "n\n")
    commit_all(root, "c3", "2026-10-03T12:00:00")
    return root


@needs_git
def test_k5_rework_counts_and_top_files(tmp_path):
    root = _fixture_repo(tmp_path)
    d = fm.compute(root, "2026-09-26")
    assert d["git"] == "ok" and d["totals"]["package_commits"] == 3
    assert d["features"]["F06"]["rework_commits"] == 3
    assert d["features"]["F05"]["rework_commits"] == 1
    assert d["features"]["F06"]["top_files"][0] == {"file": fm.PACKAGE + "/scripts/story_run.py", "commits": 3}
    assert d["features"]["F19"]["rework_commits"] == 0          # the package log never lists the repo features
    assert d["unclassified"]["package_files_on_disk"]["names"] == [fm.PACKAGE + "/scripts/stray.py"]
    assert d["unclassified"]["files_in_window_commits"]["names"] == [fm.PACKAGE + "/scripts/stray.py"]
    assert d["totals"]["process_doc_commits"] == 2 and d["totals"]["process_tax"] == 0.67   # c1 adds plans/features.json, c3 docs/note.md
    assert d["weekly"] == [{"week": "2026-W40", "rows": 0, "package_commits": 3, "process_doc_commits": 2}]
    assert d["features"]["F06"]["fragility_order"] == 1


@needs_git
def test_k5_empty_window_prints_zeros_not_an_error(tmp_path):
    root = _fixture_repo(tmp_path)
    d = fm.compute(root, "2026-12-31")
    assert d["git"] == "ok" and d["totals"]["package_commits"] == 0
    assert all(p["rework_commits"] == 0 and p["top_files"] == [] for p in d["features"].values())
    text = fm.render_markdown(d)
    assert "| F06 | driver | 0 | 0 | 0 | 0% | 0 (0+0) | 0 | - | 0 |" in text    # zeros in the table, not an error
    assert "Process tax: 0 commits touching `docs/` or `plans/` per 0 package commits = n/d" in text   # 0/0 is undefined, said so


def test_git_unavailable_still_succeeds_with_nd_columns(tmp_path, monkeypatch):
    root = tmp_path / "plain"
    write_registry(root / "plans" / "features.json", [feat("F06", "driver", ["scripts/story_run.py"])])
    put(root / fm.PACKAGE, "scripts/story_run.py")
    put(root, "plans/BACKLOG.md", "| B-001 | `story_run.py` broke | live run | новое, 02.10 | P1 |\n")
    monkeypatch.setattr(fm, "_run_git", lambda *a, **k: None)
    d = fm.compute(root, "2026-09-26")
    assert d["git"] == "n/d" and d["features"]["F06"]["rework_commits"] is None
    assert d["features"]["F06"]["rows_total"] == 1 and "rework_commits" not in d["totals"]["rank_metrics"]
    assert "n/d" in fm.render_markdown(d)


def test_seed_absent_is_said_and_rows_fall_back_to_files_or_words(tmp_path, monkeypatch):
    root = tmp_path / "noseed"
    write_registry(root / "plans" / "features.json", [feat("F06", "driver", ["scripts/story_run.py"], words=["драйвер"])])
    put(root / fm.PACKAGE, "scripts/story_run.py")
    put(root, "plans/BACKLOG.md", "| B-001 | `story_run.py` | s | st | |\n| B-002 | драйвер молчит | s | st | |\n| B-003 | ничего | s | st | |\n")
    monkeypatch.setattr(fm, "_run_git", lambda *a, **k: None)
    d = fm.compute(root, "2026-09-26")
    assert d["seed"] == "absent"
    assert d["totals"]["rows_by"] == {"tag": 0, "files": 1, "words": 1, "seed": 0, "none": 1}
    assert d["unclassified"]["rows"]["names"] == ["B-003"]


# ---------------------------------------------------------------------------------------------
# K6 -- the journal validator WARNs (not FAILs) on a missing / unknown `feature`
# ---------------------------------------------------------------------------------------------

NOW = datetime.datetime(2026, 10, 3, 12, 0, 0)
KNOWN = {"F01", "F06", "F07"}
HEAD = ev_line("2026-10-01T08:00:00", "t-001") + "\n"


def _decide(*new, known=KNOWN):
    return jv.decide_with_warnings(HEAD + "".join(l + "\n" for l in new), HEAD, NOW, known)


def test_k6_missing_feature_on_new_delegated_is_a_warn_and_exit_code_is_unchanged():
    new = ev_line("2026-10-02T09:00:00", "t-002")
    code, violations, warnings = _decide(new)
    assert (code, violations) == jv.decide(HEAD + new + "\n", HEAD, NOW)
    assert code == 0 and violations == []
    assert len(warnings) == 1 and "no 'feature' field" in warnings[0] and "plans/features.json" in warnings[0]


def test_k6_unknown_feature_value_is_a_warn_naming_the_registry():
    code, _v, warnings = _decide(ev_line("2026-10-02T09:00:00", "t-002", feature="F99"))
    assert code == 0 and len(warnings) == 1 and "'F99'" in warnings[0] and "plans/features.json" in warnings[0]


def test_k6_accepted_and_defect_found_are_covered_a_known_value_is_silent():
    lines = [
        ev_line("2026-10-02T09:00:00", "t-002", feature="F06"),
        ev_line("2026-10-02T09:05:00", "t-002", event="accepted", agent="builder", by="opus", witness="1 passed"),
        ev_line("2026-10-02T09:10:00", "t-002", event="defect_found", ref="t-002", feature="F07"),
    ]
    code, _v, warnings = _decide(*lines)
    assert code == 0 and len(warnings) == 1 and "event='accepted'" in warnings[0]


def test_k6_negative_control_an_event_dated_2026_10_01_gets_no_warn():
    code, _v, warnings = _decide(ev_line("2026-10-01T23:59:59", "t-002"))
    assert code == 0 and warnings == []


def test_k6_other_events_are_never_warned():
    new = json.dumps({"ts": "2026-10-02T09:00:00", "event": "dispatch_skipped", "agent": "designer",
                      "category": "spec", "notes": "n"})
    code, _v, warnings = _decide(new)
    assert code == 0 and warnings == []


def test_k6_an_unreadable_registry_skips_the_value_check_but_keeps_the_missing_field_warn(tmp_path, monkeypatch):
    assert jv.load_feature_ids(tmp_path / "nope.json") is None
    monkeypatch.setattr(jv, "load_feature_ids", lambda path=None: None)       # known=None -> the registry is unreadable
    new_bad = ev_line("2026-10-02T09:00:00", "t-002", feature="F99")
    new_none = ev_line("2026-10-02T09:01:00", "t-003")
    code, _v, warnings = jv.decide_with_warnings(HEAD + new_bad + "\n" + new_none + "\n", HEAD, NOW, known=None)
    assert code == 0 and len(warnings) == 1 and "t-003" in warnings[0]          # F99 cannot be judged, the missing field can


def test_k6_the_shipped_registry_ids_are_what_the_validator_loads():
    ids = jv.load_feature_ids()
    assert ids is not None and {"F01", "F19", "F20"} <= ids


def test_k6_a_real_failure_still_fails_and_keeps_its_warning_channel_separate():
    bad = ev_line("2026-10-02T09:00:00", "t-009")                 # task id novelty violated -> a real FAIL
    code, violations, warnings = _decide(bad)
    assert code == 1 and any("novelty" in v for v in violations)
    assert len(warnings) == 1 and all("WARN" not in v for v in violations)


@needs_repo_journal
def test_the_repo_journal_still_validates_clean_unstaged_path_is_silent():
    # main() returns 0 silently when the journal is not staged; decide() on the on-disk file
    # against itself (no new lines) is the pure equivalent
    text = (ROOT / jv.JOURNAL_PATH).read_text(encoding="utf-8")
    assert jv.decide_with_warnings(text, text, NOW) == (0, [], [])


# ---------------------------------------------------------------------------------------------
# K7 -- parallel clones: merge=union on the journal
# ---------------------------------------------------------------------------------------------

def test_k7_gitattributes_holds_the_union_line():
    lines = [l.strip() for l in (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()]
    assert "logs/routing-log.jsonl merge=union" in lines


@needs_git
def test_k7_two_tails_merged_by_union_the_next_commit_validates_like_before(tmp_path):
    root = init_repo(tmp_path / "j")
    put(root, ".gitattributes", "logs/routing-log.jsonl merge=union\n")
    put(root, "logs/routing-log.jsonl", ev_line("2026-10-02T08:00:00", "t-001") + "\n")
    commit_all(root, "base", "2026-10-02T08:30:00")
    git(root, "checkout", "-q", "-b", "other")
    with open(root / "logs/routing-log.jsonl", "a", newline="\n") as f:
        f.write(ev_line("2026-10-02T09:00:00", "t-002") + "\n")
    commit_all(root, "other tail", "2026-10-02T09:30:00")
    git(root, "checkout", "-q", "main")
    with open(root / "logs/routing-log.jsonl", "a", newline="\n") as f:
        f.write(ev_line("2026-10-02T10:00:00", "t-002", agent="scout") + "\n")     # the same t-002 in the other clone
        f.write(ev_line("2026-10-02T10:05:00", "t-003") + "\n")
    commit_all(root, "main tail", "2026-10-02T10:30:00")
    ours = git(root, "show", "HEAD:logs/routing-log.jsonl") + "\n"
    git(root, "merge", "--no-edit", "other")                                         # no conflict, no pre-commit hook
    merged = (root / "logs/routing-log.jsonl").read_text(encoding="utf-8")
    assert merged.count("\n") == 4                                                   # both tails are in
    head_now = git(root, "show", "HEAD:logs/routing-log.jsonl") + "\n"
    assert head_now == merged
    now = datetime.datetime(2026, 10, 3, 12, 0, 0)

    # (1) the commit that follows the merge: exit code is what it is on a journal with no merge
    nxt = ev_line("2026-10-02T11:00:00", "t-004") + "\n"
    after_merge = jv.decide_with_warnings(merged + nxt, merged, now, known=set())
    plain = jv.decide_with_warnings(ours + nxt, ours, now, known=set())
    assert after_merge[0] == plain[0] == 0
    assert len(after_merge[2]) == len(plain[2]) == 1          # the only WARN is the missing `feature` on the new line

    # (2) DOCUMENTED, not changed (a question for the Lead): the merged file validated AGAINST ITS
    # FIRST PARENT (what a hand-made merge commit through pre-commit would present) fails ONLY on ts
    # monotonicity of the interleaved tail; no other rule fires, "ts from the future" is unaffected.
    code, violations, _w = jv.decide_with_warnings(merged, ours, now, known=set())
    assert code == 1 and len(violations) == 1 and "ts is not monotonic" in violations[0]


# ---------------------------------------------------------------------------------------------
# K8 -- the report on THIS repo
# ---------------------------------------------------------------------------------------------

def _fingerprint():
    parts = []
    for rel in (fm.BACKLOG_REL, fm.JOURNAL_REL, fm.REGISTRY_REL):
        st = (ROOT / rel).stat()
        parts.append((rel, st.st_size, st.st_mtime_ns))
    parts.append(fm._run_git(ROOT, "rev-parse", "HEAD"))
    parts.append(fm._run_git(ROOT, "status", "--porcelain", "--", fm.PACKAGE, "tools", "docs", "plans", "logs"))
    return parts


@needs_repo_journal
def test_k8_write_on_this_repo_twice_gives_identical_bytes(tmp_path):
    out = tmp_path / "forge-metrics.md"
    before = _fingerprint()
    assert fm.main(["--write", "--out", str(out)]) == 0
    first = out.read_bytes()
    assert fm.main(["--write", "--out", str(out)]) == 0
    second = out.read_bytes()
    if first != second and _fingerprint() != before:
        pytest.skip("the repo (journal/backlog/git) changed between the two runs; determinism is per repo state")
    assert first == second
    text = first.decode("utf-8")
    for n in range(1, 21):
        assert f"| F{n:02d} |" in text
    for must in ("## Unclassified", "package files on disk matching no feature", "backlog rows with no attribution",
                 "journal events with no attribution", "Window: commits and journal events since", "Counting commands:",
                 "git log --since=", "## Per week"):
        assert must in text
    assert b"\r" not in first


def test_k8_json_mode_prints_the_same_data(capsys):
    assert fm.main(["--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    shipped = {f["id"] for f in fm.load_registry(ROOT / fm.REGISTRY_REL)}
    assert set(data["features"]) == shipped and "unclassified" in data


# ---------------------------------------------------------------------------------------------
# K9 / K10 -- --check and --warn
# ---------------------------------------------------------------------------------------------

def _check_repo(tmp_path):
    root = init_repo(tmp_path / "c")
    write_registry(root / "plans" / "features.json", [
        feat("F06", "driver", ["scripts/story_run.py"]),
        feat("F19", "forge", ["docs/**", "plans/**", "tools/**", "logs/**"], root="repo"),
    ])
    put(root / fm.PACKAGE, "scripts/story_run.py")
    put(root, "plans/BACKLOG.md", "| B-001 | `story_run.py` broke | live run | новое, 02.10 | P1 |\n")
    put(root, "logs/routing-log.jsonl", ev_line("2026-10-02T08:00:00", "t-001", feature="F06") + "\n")
    base = commit_all(root, "base", "2026-10-02T08:30:00")
    # the second developer's branch: one untagged row, one unclassified file, one event without feature
    with open(root / "plans/BACKLOG.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("| B-002 | Интеграция Codex: новый хост | owner | новое, 02.10 | P2 |\n")
    put(root / fm.PACKAGE, "scripts/codex_roles.py")
    with open(root / "logs/routing-log.jsonl", "a", encoding="utf-8", newline="\n") as f:
        f.write(ev_line("2026-10-02T09:00:00", "t-002") + "\n")
    return root, base


@needs_git
def test_k9_check_names_three_offenders_with_their_doors_and_exits_1(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    rc = fm.main(["--check", "--base", base], root=root)
    err = capsys.readouterr().err
    assert rc == 1
    assert "3 offender(s)" in err
    assert "B-002" in err and "no attribution" in err
    assert "scripts/codex_roles.py" in err and "matches no feature" in err
    assert "line 2 delegated t-002" in err and "no `feature` field" in err
    assert fm.DOOR_ROW in err and fm.DOOR_FILE in err and fm.DOOR_EVENT in err
    assert "F21 Codex integration" in err
    assert "line 1" not in err                      # the old, attributed event is not an offender


@needs_git
def test_k9_the_same_repo_tagged_registered_and_fielded_exits_0(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    # tag the row
    p = root / "plans/BACKLOG.md"
    p.write_text(p.read_text(encoding="utf-8").replace("новый хост |", "новый хост [F21] |"), encoding="utf-8", newline="\n")
    # register the feature (a new feature = a new row)
    write_registry(root / "plans" / "features.json", [
        feat("F06", "driver", ["scripts/story_run.py"]),
        feat("F21", "Codex integration", ["scripts/codex_*.py"]),
        feat("F19", "forge", ["docs/**", "plans/**", "tools/**", "logs/**"], root="repo"),
    ])
    # add the field
    j = root / "logs/routing-log.jsonl"
    lines = j.read_text(encoding="utf-8").splitlines()
    lines[1] = ev_line("2026-10-02T09:00:00", "t-002", feature="F21")
    j.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    rc = fm.main(["--check", "--base", base], root=root)
    out = capsys.readouterr()
    assert rc == 0 and "ok" in out.out and "new rows 1" in out.out and "new package files 1" in out.out
    assert out.err == ""


@needs_git
def test_k9_check_writes_nothing(tmp_path):
    root, base = _check_repo(tmp_path)
    before = git(root, "status", "--porcelain")
    stamp = {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file() and ".git" not in p.parts}
    fm.main(["--check", "--base", base], root=root)
    assert git(root, "status", "--porcelain") == before
    assert stamp == {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file() and ".git" not in p.parts}


@needs_git
def test_k9_an_unknown_feature_value_on_a_new_event_is_an_offender(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    j = root / "logs/routing-log.jsonl"
    lines = j.read_text(encoding="utf-8").splitlines()
    lines[1] = ev_line("2026-10-02T09:00:00", "t-002", feature="F77")
    j.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    assert fm.main(["--check", "--base", base], root=root) == 1
    assert "'F77'" in capsys.readouterr().err


@needs_git
def test_k9_events_before_the_cutoff_are_not_offenders(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    j = root / "logs/routing-log.jsonl"
    lines = j.read_text(encoding="utf-8").splitlines()
    lines[1] = ev_line("2026-10-01T09:00:00", "t-002")               # dated before 2026-10-02
    j.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    fm.main(["--check", "--base", base], root=root)
    assert "delegated t-002" not in capsys.readouterr().err


@needs_git
def test_k9_a_crlf_working_copy_does_not_make_old_events_look_new(tmp_path, capsys):
    # found on the real repo: core.autocrlf=true gives CRLF on disk, LF in the base commit
    root, base = _check_repo(tmp_path)
    j = root / "logs/routing-log.jsonl"
    j.write_bytes(j.read_bytes().replace(b"\n", b"\r\n"))
    p = root / "plans/BACKLOG.md"
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    assert fm.main(["--check", "--base", base], root=root) == 1
    err = capsys.readouterr().err
    assert "3 offender(s)" in err and "B-001" not in err
    # the counts are the sensitive part: only the ONE new event needs a feature, the old CRLF line is not new
    assert "new rows 1," in err and "new events needing a feature 1)" in err


@needs_git
def test_k10_warn_prints_the_same_text_and_exits_0(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    assert fm.main(["--check", "--base", base], root=root) == 1
    blocking = capsys.readouterr().err.splitlines()
    assert fm.main(["--check", "--base", base, "--warn"], root=root) == 0
    warned = capsys.readouterr().out.splitlines()
    assert blocking[1:] == warned[1:] and blocking[0].split(":", 1)[1] == warned[0].split(":", 1)[1]
    assert warned[0].startswith("WARN")


@needs_git
def test_k10_warn_never_blocks_even_when_the_registry_or_base_is_broken(tmp_path, capsys):
    root, _base = _check_repo(tmp_path)
    assert fm.main(["--check", "--base", "no-such-ref", "--warn"], root=root) == 0
    assert fm.main(["--check", "--base", "no-such-ref"], root=root) == 2
    (root / "plans" / "features.json").write_text("{", encoding="utf-8")
    assert fm.main(["--check", "--warn"], root=root) == 0
    assert fm.main(["--check"], root=root) == 2
    capsys.readouterr()


@needs_git
def test_default_base_is_the_merge_base_with_main_else_head_minus_1(tmp_path):
    root, base = _check_repo(tmp_path)
    git(root, "checkout", "-q", "-b", "feature")
    sha2 = commit_all(root, "second", "2026-10-02T12:00:00")
    assert fm.resolve_base(root, None) == base                    # main exists: the fork point
    other = init_repo(tmp_path / "nomain", branch="trunk")
    put(other, "a.txt")
    first = commit_all(other, "one", "2026-10-02T08:00:00")
    put(other, "b.txt")
    commit_all(other, "two", "2026-10-02T09:00:00")
    assert fm.resolve_base(other, None) == first                  # no main: HEAD~1
    with pytest.raises(fm.BaseError):
        fm.resolve_base(other, "no-such-ref")
    assert sha2 != base


def test_proposed_hook_files_are_sh_and_call_the_generator():
    merge = ROOT / ".githooks" / "pre-merge-commit.proposed"
    tail = ROOT / ".githooks" / "pre-commit.proposed-tail"
    if not merge.exists() and not tail.exists():
        pytest.skip("the Lead already placed the proposed hooks on their live paths")
    if merge.exists():
        t = merge.read_text(encoding="utf-8")
        assert t.startswith("#!/bin/sh") and "set -e" in t and "python tools/forge_metrics.py --check" in t
        assert "\r" not in t
    if tail.exists():
        t = tail.read_text(encoding="utf-8")
        assert "python tools/forge_metrics.py --check --base HEAD --warn" in t and "\r" not in t


# ---------------------------------------------------------------------------------------------
# K12 (t-581, F0-4) -- --check (c) reads EVERY journal path, a developer file by its own path
# ---------------------------------------------------------------------------------------------

DEV_FILE = "logs/journal/dev2.jsonl"
DEV_CREATED = json.dumps({"ts": "2026-10-02T08:10:00", "event": "journal_created", "agent": "lead",
                          "category": "process", "notes": "the journal of this clone"})


@needs_git
def test_k12_a_new_event_without_a_feature_in_a_new_developer_file_is_named_with_the_path(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    put(root, DEV_FILE, DEV_CREATED + "\n" + ev_line("2026-10-02T10:00:00", "t-001") + "\n")
    assert fm.main(["--check", "--base", base], root=root) == 1
    err = capsys.readouterr().err
    assert "4 offender(s)" in err and "new events needing a feature 2" in err
    assert "(logs/journal/dev2.jsonl line 2 delegated t-001) has no `feature` field" in err
    assert "(line 2 delegated t-002)" in err                       # the history's offender keeps its old form, no path
    assert "routing-log.jsonl line" not in err


@needs_git
def test_k12_control_the_same_event_with_a_registered_feature_is_not_an_offender(tmp_path, capsys):
    root, base = _check_repo(tmp_path)
    put(root, DEV_FILE, DEV_CREATED + "\n" + ev_line("2026-10-02T10:00:00", "t-001", feature="F06") + "\n")
    fm.main(["--check", "--base", base], root=root)
    err = capsys.readouterr().err
    assert "dev2.jsonl" not in err and "new events needing a feature 2)" in err        # counted, attributed
    put(root, DEV_FILE, DEV_CREATED + "\n" + ev_line("2026-10-02T10:00:00", "t-001", feature="F77") + "\n")
    fm.main(["--check", "--base", base], root=root)
    assert "(logs/journal/dev2.jsonl line 2 delegated t-001) names feature 'F77'" in capsys.readouterr().err


@needs_git
def test_k12_only_the_lines_added_to_a_file_the_base_has_are_new(tmp_path, capsys):
    root, _base = _check_repo(tmp_path)
    write_registry(root / "plans" / "features.json", [feat("F06", "driver", ["scripts/story_run.py", "scripts/codex_roles.py"]),
                                                      feat("F19", "forge", ["docs/**", "plans/**", "tools/**", "logs/**"], root="repo")])  # (d): codex_roles.py is tracked now
    put(root, DEV_FILE, DEV_CREATED + "\n" + ev_line("2026-10-02T10:00:00", "t-001") + "\n")     # untagged, but COMMITTED below
    base2 = commit_all(root, "second base", "2026-10-02T11:00:00")
    with open(root / DEV_FILE, "a", encoding="utf-8", newline="\n") as f:
        f.write(ev_line("2026-10-02T12:00:00", "t-002") + "\n")
    assert fm.main(["--check", "--base", base2], root=root) == 1
    err = capsys.readouterr().err
    assert "1 offender(s)" in err and "logs/journal/dev2.jsonl line 3 delegated t-002" in err
    assert "line 2 delegated t-001" not in err


@needs_git
def test_k12_crlf_in_a_developer_file_does_not_make_its_old_events_look_new(tmp_path, capsys):
    root, _base = _check_repo(tmp_path)
    write_registry(root / "plans" / "features.json", [feat("F06", "driver", ["scripts/story_run.py", "scripts/codex_roles.py"]),
                                                      feat("F19", "forge", ["docs/**", "plans/**", "tools/**", "logs/**"], root="repo")])  # (d): codex_roles.py is tracked now
    put(root, DEV_FILE, DEV_CREATED + "\n" + ev_line("2026-10-02T10:00:00", "t-001") + "\n")
    base2 = commit_all(root, "second base", "2026-10-02T11:00:00")
    p = root / DEV_FILE
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    assert fm.main(["--check", "--base", base2], root=root) == 0
    assert "ok" in capsys.readouterr().out


@needs_git
def test_k12_the_journal_paths_are_the_history_first_then_the_developer_files_in_name_order(tmp_path):
    root, base = _check_repo(tmp_path)
    put(root, "logs/journal/zed.jsonl", DEV_CREATED + "\n")
    put(root, DEV_FILE, DEV_CREATED + "\n")
    put(root, "logs/journal/Bad Name.jsonl", "x\n")               # not a journal file: not listed
    assert fm._journal_paths(root, base) == ["logs/routing-log.jsonl", DEV_FILE, "logs/journal/zed.jsonl"]


# ---------------------------------------------------------------------------------------------
# K13 (t-598, F0-9) -- a finding file (plans/piles/<slug>/findings/*.md) is a row
# ---------------------------------------------------------------------------------------------

BACKLOG_FROZEN = "| B-001 | `story_run.py` broke | live run | new, 02.10 | P1 |\n\n## Закрыто\n"


def card_text(slug, feats):
    return (f"# Pile {slug} (`{slug}`)\n\nприоритет: П1 | фичи: {feats} | стенд: не нужен | зона: `tools/`\n\n"
            "## Пачки\n\n| № | Что | Строки | Размер | Статус | Взял | Ветка | MR |\n|---|---|---|---|---|---|---|---|\n"
            "| 1 | x | — | S | ожидает | — | — | — |\n")


def finding_text(slug, body="the text", header=True):
    head = f"id: — | кучка: `{slug}` | от: me, 08.10 | приоритет: П2 | кандидат наверх: нет\n\n" if header else ""
    return f"# A finding\n\n{head}{body}\n"


def pile(root, slug, feats, **findings):
    """plans/piles/<slug>/ with a card and findings {file name: text}."""
    put(root, f"plans/piles/{slug}/README.md", card_text(slug, feats))
    for name, text in findings.items():
        put(root, f"plans/piles/{slug}/findings/{name}", text)


def _frepo(tmp_path):
    """A base commit WITHOUT plans/piles; returns (root, base). Registry F06 + F19."""
    root = init_repo(tmp_path / "f")
    write_registry(root / "plans" / "features.json", [
        feat("F06", "driver", ["scripts/story_run.py"]),
        feat("F19", "forge", ["docs/**", "plans/**", "tools/**", "logs/**"], root="repo"),
    ])
    put(root / fm.PACKAGE, "scripts/story_run.py")
    put(root, "plans/BACKLOG.md", BACKLOG_FROZEN)
    return root, commit_all(root, "base", "2026-10-08T08:00:00")


def test_k13_attribution_order_tag_then_card_then_none_and_unknown_tag_is_unclassified():
    ids = {"F06", "F19"}
    assert fm.attribute_finding("see [F06] here", "F19", ids) == {"feature": "F06", "by": "tag", "unknown": []}
    assert fm.attribute_finding("no tag", "F19", ids) == {"feature": "F19", "by": "card", "unknown": []}
    assert fm.attribute_finding("no tag", None, ids) == {"feature": None, "by": "none", "unknown": []}
    # an unregistered bracketed tag: unclassified even though the card could answer; a registered tag beside it wins
    assert fm.attribute_finding("[F99] only", "F19", ids) == {"feature": None, "by": "none", "unknown": ["F99"]}
    assert fm.attribute_finding("[F99] and F06", "F19", ids)["feature"] == "F06"
    assert fm.attribute_finding("a key F12 pressed", None, ids)["unknown"] == []      # bare Fnn prose is no tag claim


@needs_git
def test_k13_new_findings_are_counted_attributed_and_unclassified_ones_never_fail(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-tagged.md": finding_text("alpha", "touches [F06]"),
                                  "20261008-by-card.md": finding_text("alpha")})
    pile(root, "beta", "—", **{"20261008-loose.md": finding_text("beta")})
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr()
    assert "new rows 0 (all attributed), new findings 3 (1 unclassified)," in out.out
    assert "plans/piles/beta/findings/20261008-loose.md" in out.out and "not an offender" in out.out
    assert out.err == ""
    pile(root, "beta", "F06")                                # the card now names a feature: nothing is unclassified
    fm.main(["--check", "--base", base], root=root)
    assert "new findings 3 (all attributed)" in capsys.readouterr().out


@needs_git
def test_k13_only_findings_added_since_the_base_are_new_and_an_old_base_makes_all_new(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-one.md": finding_text("alpha")})
    base2 = commit_all(root, "with piles", "2026-10-08T09:00:00")
    put(root, "plans/piles/alpha/findings/20261008-two.md", finding_text("alpha"))
    fm.main(["--check", "--base", base2], root=root)
    assert "new findings 1 (all attributed)" in capsys.readouterr().out
    fm.main(["--check", "--base", base], root=root)                       # the base predates plans/piles
    assert "new findings 2 (all attributed)" in capsys.readouterr().out


@needs_git
def test_k13_a_finding_with_header_errors_is_counted_attributed_by_the_card_and_warned_once(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-broken.md": finding_text("alpha", header=False)})
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    assert "new findings 1 (all attributed)" in out                       # counted, and the card attributed it
    warned = [l for l in out.splitlines() if "WARN finding" in l]
    assert len(warned) == 1 and "plans/piles/alpha/findings/20261008-broken.md" in warned[0] and "header" in warned[0]


@needs_git
def test_k13_an_unknown_tag_warns_and_leaves_the_finding_unclassified(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-odd.md": finding_text("alpha", "belongs to [F99]")})
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    assert "new findings 1 (1 unclassified)" in out
    assert "unknown feature F99" in out and "20261008-odd.md" in out


@needs_git
def test_k13_without_plans_piles_check_and_report_read_as_before(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    assert "finding" not in out and out.count("\n") == 1
    data = fm.compute(root, "2026-09-26")
    assert "findings" not in data["totals"] and "findings" not in data["unclassified"]
    assert all("findings_total" not in p for p in data["features"].values())
    text = fm.render_markdown(data)
    assert "indings" not in text and "| rows | open |" in text


@needs_git
def test_k13_an_unreadable_piles_tree_is_one_warning_not_a_crash(tmp_path, capsys):
    root, base = _check_repo(tmp_path)                    # its BACKLOG has no "## Закрыто": piles.load_tree refuses it
    pile(root, "alpha", "F19", **{"20261008-one.md": finding_text("alpha")})
    assert fm.main(["--check", "--base", base, "--warn"], root=root) == 0
    out = capsys.readouterr().out
    assert "WARN findings not read" in out and "new findings" not in out


@needs_git
def test_k13_the_report_lists_findings_per_feature_next_to_rows(tmp_path):
    root, _base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-a.md": finding_text("alpha"), "20261008-b.md": finding_text("alpha", "[F06]")})
    pile(root, "beta", "—", **{"20261008-c.md": finding_text("beta")})
    d = fm.compute(root, "2026-09-26")
    assert (d["features"]["F19"]["findings_total"], d["features"]["F06"]["findings_total"]) == (1, 1)
    assert d["unclassified"]["findings"] == {"count": 1, "names": ["beta/20261008-c.md"]}
    assert d["totals"]["findings"] == 3 and d["totals"]["findings_by"] == {"tag": 1, "card": 1, "none": 1}
    text = fm.render_markdown(d)
    assert "| F | feature | rows | findings | open |" in text
    assert "- findings with no attribution: **1** - `beta/20261008-c.md`" in text
    assert "; findings: every `*.md` under `plans/piles/*/findings/`" in text
    assert "Findings: 3 parsed; attributed by tag 1, pile card 1, none 1." in text


# ---------------------------------------------------------------------------------------------
# K14 (t-620, F2-8 = B-471) -- a rename is not a new finding; an unreadable finding; an unknown [Fnn] tag
# ---------------------------------------------------------------------------------------------

FDIR_A = "plans/piles/alpha/findings/"
NEW_FINDINGS = "new findings "


def _new_findings(capsys, root, base):
    """-> (check output, the 'new findings N' count it printed)."""
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    return out, int(out.split(NEW_FINDINGS, 1)[1].split(" ", 1)[0])


@needs_git
def test_k14_a_rename_is_not_a_new_finding_and_still_warns(tmp_path, capsys):
    root, _base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-x.md": finding_text("alpha", header=False)})
    base2 = commit_all(root, "with piles", "2026-10-08T09:00:00")
    git(root, "mv", FDIR_A + "20261008-x.md", FDIR_A + "B-480-x.md")              # the batch assembly names it B-480
    out, n = _new_findings(capsys, root, base2)
    assert n == 0 and "new findings 0 (all attributed)" in out, out
    warned = [l for l in out.splitlines() if "WARN finding" in l]
    assert len(warned) == 1 and FDIR_A + "B-480-x.md" in warned[0]               # a renamed finding is still judged for its header


@needs_git
def test_k14_two_candidates_on_one_slug_are_both_new(tmp_path, capsys):
    root, _base = _frepo(tmp_path)                                               # spec 7.3 (a): one renamed is undecidable
    pile(root, "alpha", "F19", **{"20261008-dubl.md": finding_text("alpha")})
    base2 = commit_all(root, "with piles", "2026-10-08T09:00:00")
    (root / FDIR_A / "20261008-dubl.md").unlink()
    put(root, FDIR_A + "B-480-dubl.md", finding_text("alpha"))
    put(root, FDIR_A + "20261009-dubl.md", finding_text("alpha"))
    assert _new_findings(capsys, root, base2)[1] == 2


@needs_git
@pytest.mark.parametrize("closed,expect_new", [(True, 1), (False, 0)])           # the control: an OPEN B-200 pairs as a rename
def test_k14_a_finding_the_backlog_closed_is_no_rename_source(tmp_path, capsys, closed, expect_new):
    root, _base = _frepo(tmp_path)                                               # spec 7.3 (b)
    if closed:
        put(root, "plans/BACKLOG.md", BACKLOG_FROZEN + "| B-200 | **cleanup** | w | s | P1 |\n")
    pile(root, "alpha", "F19", **{"B-200-cleanup.md": finding_text("alpha")})
    base2 = commit_all(root, "with piles", "2026-10-08T09:00:00")
    (root / FDIR_A / "B-200-cleanup.md").unlink()                                # what `close` does to a finding
    put(root, FDIR_A + "20261009-cleanup.md", finding_text("alpha"))
    assert _new_findings(capsys, root, base2)[1] == expect_new


@pytest.mark.parametrize("current,base,closed,expect", [
    (["plans/piles/a/findings/B-480-x.md"], ["plans/piles/a/findings/20261008-x.md"], set(), {"plans/piles/a/findings/B-480-x.md"}),
    (["plans/piles/a/findings/B-480-x.md"], ["plans/piles/b/findings/20261008-x.md"], set(), set()),     # another pile
    (["plans/piles/a/findings/B-480-x.md"], ["plans/piles/a/findings/20261008-y.md"], set(), set()),     # another slug
    (["plans/piles/a/findings/B-480.md"], ["plans/piles/a/findings/B-481.md"], set(), set()),             # no slug is never paired
    (["plans/piles/a/findings/B-480-x.md"], ["plans/piles/a/findings/B-200-x.md"], {"B-200"}, set()),     # the base id is closed
    (["plans/piles/a/findings/odd name.md"], ["plans/piles/a/findings/20261008-x.md"], set(), set()),     # the pattern rejects the name
    (["plans/piles/a/findings/B-480-x.md", "plans/piles/a/findings/B-481-x.md"], ["plans/piles/a/findings/20261008-x.md"], set(), set()),
])
def test_k14_rename_pairing_is_one_to_one_on_pile_and_slug(current, base, closed, expect):
    assert fm.renamed_finding_paths(current, set(base), closed) == expect


@needs_git
def test_k14_an_unreadable_finding_is_one_warning_and_unclassified_whatever_the_card_says(tmp_path, capsys):
    root, _base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-ok.md": finding_text("alpha")})
    base2 = commit_all(root, "with piles", "2026-10-08T09:00:00")
    (root / FDIR_A / "20261009-bad.md").write_bytes(b"# t\n\n\xff\xfe [F06]\n")     # the card names F19; the bytes are not text
    out, n = _new_findings(capsys, root, base2)
    assert n == 1 and "new findings 1 (1 unclassified)" in out, out
    warned = [l for l in out.splitlines() if "WARN finding" in l]
    assert len(warned) == 1 and "20261009-bad.md: unreadable (not valid UTF-8" in warned[0], warned
    assert warned[0].endswith("-- unclassified; save it as UTF-8")
    base3 = commit_all(root, "the bad file lands", "2026-10-08T10:00:00")
    out, n = _new_findings(capsys, root, base3)                                  # now it is a BASE file: counted by nobody, warned by nobody
    assert n == 0 and "WARN finding" not in out, out


@needs_git
def test_k14_an_unreadable_finding_is_unclassified_in_the_report_too(tmp_path):
    root, _base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-ok.md": finding_text("alpha")})
    (root / FDIR_A / "20261009-bad.md").write_bytes(b"\xff\xfe")
    d = fm.compute(root, "2026-09-26")
    assert d["unclassified"]["findings"] == {"count": 1, "names": ["alpha/20261009-bad.md"]}
    assert d["features"]["F19"]["findings_total"] == 1


BACKLOG_NEW_ROW = "| B-001 | `story_run.py` broke | live run | new, 02.10 | P1 |\n| B-002 | `story_run.py` also [F99] | live | new, 09.10 | P1 |\n"


@needs_git
def test_k14_a_new_row_with_an_unknown_tag_warns_in_check_and_on_compute_stderr(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    put(root, "plans/BACKLOG.md", BACKLOG_FROZEN.replace(BACKLOG_FROZEN.split("\n")[0] + "\n", BACKLOG_NEW_ROW, 1))
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    assert "new rows 1 (all attributed)" in out                                  # attribution itself is unchanged: B-002 has its file
    warned = [l.strip() for l in out.splitlines() if "WARN row" in l]
    assert len(warned) == 1 and warned[0].startswith("WARN row B-002 (line ") and warned[0].endswith(
        "): unknown feature F99 (not in plans/features.json) -- the tag is ignored; register the feature or fix the tag"), warned
    fm.compute(root, "2026-09-26")
    err = capsys.readouterr().err
    assert "forge_metrics: WARN row B-002 (line " in err and "unknown feature F99" in err and "B-001" not in err


@needs_git
def test_k14_a_row_that_is_not_new_does_not_warn_in_check_and_a_clean_tree_is_silent_on_compute(tmp_path, capsys):
    root, _base = _frepo(tmp_path)
    put(root, "plans/BACKLOG.md", BACKLOG_FROZEN.replace(BACKLOG_FROZEN.split("\n")[0] + "\n", BACKLOG_NEW_ROW, 1))
    base2 = commit_all(root, "the tagged row lands", "2026-10-08T09:00:00")
    assert fm.main(["--check", "--base", base2], root=root) == 0
    assert "WARN row" not in capsys.readouterr().out                             # --check names NEW rows only
    clean, _b = _frepo(tmp_path / "clean")
    fm.compute(clean, "2026-09-26")
    assert capsys.readouterr().err == ""


@needs_git
def test_k14_an_unknown_tag_beside_a_registered_one_warns_and_attributes_by_the_registered_tag(tmp_path, capsys):
    root, base = _frepo(tmp_path)
    pile(root, "alpha", "F19", **{"20261008-both.md": finding_text("alpha", "touches [F06] and [F99]")})
    assert fm.main(["--check", "--base", base], root=root) == 0
    out = capsys.readouterr().out
    assert "new findings 1 (all attributed)" in out
    warned = [l.strip() for l in out.splitlines() if "WARN finding" in l]
    assert warned == ["WARN finding plans/piles/alpha/findings/20261008-both.md: unknown feature F99 "
                      "(not in plans/features.json) -- ignored; attributed by tag F06"]


@needs_git
def test_k14_run_check_carries_the_warning_lines_apart_from_the_counters(tmp_path):
    """F-10: the warning lines (row tag warnings, then finding warnings) are their own return item, not lists in `counts`."""
    root, base = _frepo(tmp_path)
    put(root, "plans/BACKLOG.md", BACKLOG_FROZEN.replace(BACKLOG_FROZEN.split("\n")[0] + "\n", BACKLOG_NEW_ROW, 1))
    pile(root, "alpha", "F19", **{"20261008-both.md": finding_text("alpha", "touches [F06] and [F99]")})
    offenders, counts, sha, warnings = fm.run_check(root, base)
    assert offenders == [] and sha == base
    assert len(warnings) == 2 and warnings[0].startswith("WARN row B-002") and warnings[1].startswith("WARN finding ")
    assert "row_warnings" not in counts and "finding_warnings" not in counts
    assert [k for k, v in counts.items() if not isinstance(v, int)] == ["unclassified_finding_files"]


def test_k14_attribute_finding_returns_the_unknown_tag_beside_a_registered_one():
    ids = {"F06", "F19"}
    assert fm.attribute_finding("[F99] and F06", "F19", ids) == {"feature": "F06", "by": "tag", "unknown": ["F99"]}
    assert fm.attribute_finding("[F06] [F98] [F99]", None, ids)["unknown"] == ["F98", "F99"]     # sorted
