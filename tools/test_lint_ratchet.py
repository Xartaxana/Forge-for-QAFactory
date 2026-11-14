"""Tests for tools/lint_ratchet.py -- the pyflakes ratchet.

Keys: K1 clean tree + empty baseline -> 0; K2 a new unused import -> 1 naming path:line; K3 the same
finding baselined -> 0; K4 the finding moved down -> still 0 (identity has no line); K5 a second
identical finding over a count of 1 -> 1; K6 a finding gone while the baseline keeps it -> 1 "stale";
K7 --update then --check -> 0, byte-identical on a second --update; K8 a syntax error -> 1, --update
refuses and leaves the baseline bytes unchanged; K9 an undefined name -> 1; K10 empty / BOM / CRLF /
undecodable files do not crash; K11 pyflakes missing -> exit 2 with the pip sentence; K12 the shipped
baseline matches the real tree; K13 no backslash and no drive prefix in any shipped baseline path;
plus: a missing root and a missing baseline are exit 2, line-number arguments are normalised out of
the identity, __pycache__ and non-.py files are skipped. Each negative has its positive twin.
The tool's roots, repo and baseline are injected by argument: no test touches the real tree except K12/K13.
"""
import json
import pathlib
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import dup_ratchet as DRT  # noqa: E402
import lint_ratchet as LR  # noqa: E402

UNUSED = "import os\n"
CLEAN = "x = 1\n"


def make_repo(tmp_path, files):
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_bytes(content.encode("utf-8"))
    return tmp_path


def baseline_file(tmp_path, rows, version=None):
    import pyflakes
    p = tmp_path / "bl.json"
    doc = {"generated_by": "test", "pyflakes_version": version or pyflakes.__version__, "rows": rows}
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def go(tmp_path, capsys, *flags, baseline="bl.json", roots=("src",)):
    argv = list(flags) + ["--repo", str(tmp_path), "--baseline", str(tmp_path / baseline)]
    for r in roots:
        argv += ["--root", r]
    rc = LR.run(argv)
    return rc, capsys.readouterr().out


ROW_OS = {"path": "src/a.py", "class": "UnusedImport", "args": "os", "count": 1}


def test_k1_clean_tree_empty_baseline(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": CLEAN})
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys, "--check")
    assert rc == 0
    assert "lint ratchet: 0 findings, 0 in the baseline, 0 new, 0 stale" in out


def test_k2_new_finding_is_red_naming_path_and_line(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": "x = 1\nimport os\n"})
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys)
    assert rc == 1
    assert "src/a.py:2:" in out and "'os' imported but unused" in out
    assert "python tools/lint_ratchet.py --update" in out and "say why in the commit" in out


def test_k3_same_finding_in_baseline_is_green(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": UNUSED})
    baseline_file(tmp_path, [ROW_OS])
    rc, out = go(tmp_path, capsys)
    assert rc == 0
    assert "1 findings, 1 in the baseline, 0 new, 0 stale" in out


def test_k4_moved_finding_is_still_green(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": "\n" * 10 + UNUSED})
    baseline_file(tmp_path, [ROW_OS])
    rc, out = go(tmp_path, capsys)
    assert rc == 0, out


def test_k5_second_identical_finding_is_red(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": "def f():\n    import os\n\n\ndef g():\n    import os\n"})
    baseline_file(tmp_path, [ROW_OS])
    rc, out = go(tmp_path, capsys)
    assert rc == 1
    assert "1 new" in out and "2 now, 1 in the baseline" in out
    # twin: with the count recorded as 2 the same tree is green
    baseline_file(tmp_path, [dict(ROW_OS, count=2)])
    rc2, out2 = go(tmp_path, capsys)
    assert rc2 == 0, out2


def test_k6_finding_gone_but_baselined_is_stale_red(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": CLEAN})
    baseline_file(tmp_path, [ROW_OS])
    rc, out = go(tmp_path, capsys)
    assert rc == 1
    assert "stale" in out and "--update" in out and "0 findings, 0 in the baseline, 0 new, 1 stale" in out
    # a lower count is stale too; twin: the exact count is green
    make_repo(tmp_path, {"src/a.py": UNUSED})
    baseline_file(tmp_path, [dict(ROW_OS, count=3)])
    rc2, out2 = go(tmp_path, capsys)
    assert rc2 == 1 and "stale" in out2
    baseline_file(tmp_path, [ROW_OS])
    assert go(tmp_path, capsys)[0] == 0


def test_k7_update_then_check_and_deterministic(tmp_path, capsys):
    make_repo(tmp_path, {"src/b.py": "import sys\nimport os\n", "src/a.py": UNUSED + "import re\n"})
    rc, out = go(tmp_path, capsys, "--update", baseline="new-bl.json")
    assert rc == 0 and "4 rows added" in out, out
    for ident in ("src/b.py: UnusedImport sys  (0 -> 1)", "src/b.py: UnusedImport os  (0 -> 1)",
                  "src/a.py: UnusedImport os  (0 -> 1)", "src/a.py: UnusedImport re  (0 -> 1)"):
        assert "added: " + ident in out, out                               # every added identity is listed
    first = (tmp_path / "new-bl.json").read_bytes()
    rc, out = go(tmp_path, capsys, "--check", baseline="new-bl.json")
    assert rc == 0 and "0 new, 0 stale" in out
    rc, out = go(tmp_path, capsys, "--update", baseline="new-bl.json")
    assert rc == 0 and "0 rows added, 0 removed" in out and "added:" not in out and "grew:" not in out
    assert (tmp_path / "new-bl.json").read_bytes() == first
    # a count that went up is listed with old -> new; twin above: an unchanged row is not listed
    make_repo(tmp_path, {"src/b.py": "def f():\n    import sys\n\n\ndef g():\n    import sys\n    import os\n"})
    rc, out = go(tmp_path, capsys, "--update", baseline="new-bl.json")
    assert rc == 0 and "grew: src/b.py: UnusedImport sys  (1 -> 2)" in out, out
    make_repo(tmp_path, {"src/b.py": "import sys\nimport os\n"})
    assert go(tmp_path, capsys, "--update", baseline="new-bl.json")[0] == 0
    doc = json.loads(first.decode("utf-8"))
    assert "generated_by" in doc and first.endswith(b"\n") and b"\r" not in first
    keys = [(r["path"], r["class"], r["args"]) for r in doc["rows"]]
    assert keys == sorted(keys)
    # shrinking: fix one finding, --update removes its row
    make_repo(tmp_path, {"src/b.py": "import sys\n"})
    rc, out = go(tmp_path, capsys, "--update", baseline="new-bl.json")
    assert rc == 0 and "1 removed" in out, out


def test_k8_syntax_error_is_red_and_never_baselined(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": "x = 1\ndef broken(:\n    pass\n"})
    bl = baseline_file(tmp_path, [])
    before = bl.read_bytes()
    rc, out = go(tmp_path, capsys, "--check")
    assert rc == 1 and "src/a.py:2:" in out and "SyntaxError" in out
    assert "fix the file so it parses" in out and "non-.py name" in out      # the door, on --check ...
    rc, out = go(tmp_path, capsys, "--update")
    assert rc == 1 and "refused" in out and "src/a.py:2:" in out
    assert "fix the file so it parses" in out and "non-.py name" in out      # ... and on the --update refusal
    assert bl.read_bytes() == before
    # a baseline row that smuggles a SyntaxError in is an untrustworthy baseline: exit 2
    baseline_file(tmp_path, [{"path": "src/a.py", "class": "SyntaxError", "args": "x", "count": 1}])
    assert go(tmp_path, capsys, "--check")[0] == 2
    # twin: fixing the file makes --update work
    make_repo(tmp_path, {"src/a.py": CLEAN})
    baseline_file(tmp_path, [])
    assert go(tmp_path, capsys, "--update")[0] == 0


def test_k9_undefined_name_is_red(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": "print(nowhere)\n"})
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys)
    assert rc == 1 and "undefined name 'nowhere'" in out
    make_repo(tmp_path, {"src/a.py": "nowhere = 1\nprint(nowhere)\n"})
    assert go(tmp_path, capsys)[0] == 0


def test_k10_odd_files_do_not_crash(tmp_path, capsys):
    make_repo(tmp_path, {
        "src/empty.py": b"",
        "src/bom.py": b"\xef\xbb\xbfx = 1\n",
    })
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys)
    assert rc == 0 and "src/empty.py" not in out and "src/bom.py" not in out   # nothing to find, nothing crashes
    # CRLF key: ONE path -- the baseline is made from the LF form, the CRLF form of the same file is checked
    make_repo(tmp_path, {"src/x.py": b"import os\nx = 1\n"})
    assert go(tmp_path, capsys, "--update")[0] == 0
    make_repo(tmp_path, {"src/x.py": b"import os\r\nx = 1\r\n"})
    rc, out = go(tmp_path, capsys)
    assert rc == 0 and "1 findings, 1 in the baseline, 0 new, 0 stale" in out, out
    # twin: a second finding in the CRLF form is still seen
    make_repo(tmp_path, {"src/x.py": b"import os\r\nimport re\r\nx = 1\r\n"})
    rc, out = go(tmp_path, capsys)
    assert rc == 1 and "src/x.py:2:" in out
    make_repo(tmp_path, {"src/x.py": b"import os\nx = 1\n"})
    # undecodable and NUL bytes: a finding of their own class, red, refused by --update
    make_repo(tmp_path, {"src/bad.py": b"x = '\xff\xfe'\n", "src/nul.py": b"x = 1\x00\n"})
    rc, out = go(tmp_path, capsys)
    assert rc == 1 and "src/bad.py" in out and "src/nul.py" in out
    before = (tmp_path / "bl.json").read_bytes()
    rc, out = go(tmp_path, capsys, "--update")
    assert rc == 1 and (tmp_path / "bl.json").read_bytes() == before


def test_k11_pyflakes_missing_is_exit_2(tmp_path, capsys, monkeypatch):
    import pyflakes
    pinned = pyflakes.__version__
    make_repo(tmp_path, {"src/a.py": CLEAN})
    baseline_file(tmp_path, [])
    monkeypatch.setitem(sys.modules, "pyflakes.api", None)
    monkeypatch.setitem(sys.modules, "pyflakes", None)
    rc, out = go(tmp_path, capsys)
    assert rc == 2 and f"pyflakes is not installed: pip install pyflakes=={pinned}" in out   # the baseline's pin is named
    # a baseline that cannot be read gives the bare form
    rc, out = go(tmp_path, capsys, baseline="absent.json")
    assert rc == 2 and "pip install pyflakes" in out and "pip install pyflakes==" not in out
    monkeypatch.undo()                               # twin: with it present the same tree is green
    assert go(tmp_path, capsys)[0] == 0


def test_pyflakes_version_drift_is_exit_2(tmp_path, capsys):
    import pyflakes
    make_repo(tmp_path, {"src/a.py": UNUSED})
    baseline_file(tmp_path, [ROW_OS], version="0.0.1")
    rc, out = go(tmp_path, capsys)
    assert rc == 2
    assert "generated with pyflakes 0.0.1, this is " + pyflakes.__version__ in out
    assert "install pyflakes==0.0.1 or regenerate with --update" in out
    # a baseline that records no version is the same unknown
    doc = json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))
    del doc["pyflakes_version"]
    (tmp_path / "bl.json").write_text(json.dumps(doc), encoding="utf-8")
    assert go(tmp_path, capsys)[0] == 2
    # --update stamps the running version; the twin: then --check is green and the summary names the version
    assert go(tmp_path, capsys, "--update")[0] == 0
    assert json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))["pyflakes_version"] == pyflakes.__version__
    rc, out = go(tmp_path, capsys)
    assert rc == 0 and f"(pyflakes {pyflakes.__version__})" in out


def test_missing_root_and_missing_baseline_are_exit_2(tmp_path, capsys):
    make_repo(tmp_path, {"src/a.py": CLEAN})
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys, roots=("src", "nope"))
    assert rc == 2 and "`nope`" in out and "does not exist" in out
    assert "ai-packages/qa-factory/scripts" in out and "--root" in out     # the configured ROOTS and the flag are named
    rc, out = go(tmp_path, capsys, baseline="absent.json")
    assert rc == 2 and "--update" in out
    (tmp_path / "junk.json").write_text("{not json", encoding="utf-8")
    assert go(tmp_path, capsys, baseline="junk.json")[0] == 2


def test_line_numbers_in_arguments_are_normalised(tmp_path, capsys):
    src = "import os\nimport os\n"
    make_repo(tmp_path, {"src/a.py": src})
    rc, out = go(tmp_path, capsys, "--update", baseline="n.json")
    assert rc == 0
    rows = json.loads((tmp_path / "n.json").read_text(encoding="utf-8"))["rows"]
    redef = [r for r in rows if r["class"] == "RedefinedWhileUnused"]
    assert redef and all("<line>" in r["args"] for r in redef)
    # twin: the same finding after the original moved down 5 lines is still green
    make_repo(tmp_path, {"src/a.py": "\n" * 5 + src})
    assert go(tmp_path, capsys, baseline="n.json")[0] == 0


@pytest.mark.parametrize("cls, src", [
    ("ImportShadowedByLoopVar", "import os\nfor os in range(3):\n    pass\n"),
    ("UndefinedLocal", "x = 1\n\n\ndef f():\n    print(x)\n    x = 2\n"),
])
def test_line_argument_classes_are_normalised(tmp_path, capsys, cls, src):
    make_repo(tmp_path, {"src/a.py": src})
    assert go(tmp_path, capsys, "--update", baseline="n.json")[0] == 0
    rows = json.loads((tmp_path / "n.json").read_text(encoding="utf-8"))["rows"]
    row = [r for r in rows if r["class"] == cls]
    assert row and "<line>" in row[0]["args"], rows
    # twin: the referenced line (the first definition) moved down -- nothing new, nothing stale
    moved = "\n" * 6 + src                                    # the first definition goes from line 1 to line 7
    make_repo(tmp_path, {"src/a.py": moved})
    rc, out = go(tmp_path, capsys, baseline="n.json")
    assert rc == 0 and "0 new, 0 stale" in out, out
    # negative control: a genuinely different finding is still red against the same baseline
    make_repo(tmp_path, {"src/a.py": moved + "import sys\n"})
    assert go(tmp_path, capsys, baseline="n.json")[0] == 1


def test_pycache_and_non_py_are_skipped_and_roots_recurse(tmp_path, capsys):
    make_repo(tmp_path, {
        "src/__pycache__/junk.py": UNUSED,
        "src/notes.txt": UNUSED,
        "src/deep/er/c.py": UNUSED,
    })
    baseline_file(tmp_path, [])
    rc, out = go(tmp_path, capsys)
    assert rc == 1 and "src/deep/er/c.py:1:" in out
    assert "__pycache__" not in out and "notes.txt" not in out


PKG = "ai-packages/qa-factory/scripts"
HAND_ROW = {"path": PKG + "/tests/test_a.py", "class": "HandReaderInput", "args": "RR-x", "count": 1}
HAND_FILES = {
    PKG + "/tests/fixtures/form-rounds.json": json.dumps({"hand_inputs": {"RR-x": ["Plan row:\\s*TS-\\d+"]}}),
    PKG + "/tests/test-layers.json": json.dumps({"quarantine": {"test_q.py": {}}}),
    PKG + "/tests/test_a.py": "x = 'Plan row: TS-1'\n",
    PKG + "/tests/test_q.py": "x = 'Plan row: TS-2'\n",
    PKG + "/tests/test_field_producers.py": "x = 'Plan row: TS-3'\n",
}


def _hand_go(tmp_path, capsys, files, rows, *flags, roots=(PKG,)):
    make_repo(tmp_path, dict(HAND_FILES, **files))
    baseline_file(tmp_path, rows)
    return go(tmp_path, capsys, *flags, roots=roots)


@pytest.mark.parametrize("case", [
    "new hand literal -> exit 1 new finding",
    "removed literal -> exit 1 stale",
    "quarantined file not counted",
    "bad regex -> exit 2",
    "missing form-rounds.json -> exit 2",
    "package root not among --root -> not run line",
])
def test_hand_input_line(tmp_path, capsys, case):
    if case == "new hand literal -> exit 1 new finding":
        rc, out = _hand_go(tmp_path, capsys, {}, [])
        assert rc == 1 and "test_a.py:1: Plan row: TS-1  [HandReaderInput]" in out and "python tools/lint_ratchet.py --update" in out
        rc, out = _hand_go(tmp_path, capsys, {}, [HAND_ROW])                       # twin: recorded -> green
        assert rc == 0, out
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/test_a.py": "a = 'Plan row: TS-1 Plan row: TS-2'\n"}, [HAND_ROW])
        assert rc == 1 and "2 now, 1 in the baseline" in out                       # one finding per match, count per identity
        rc, out = _hand_go(tmp_path, capsys, {}, [], "--update")
        assert rc == 0 and f"added: {PKG}/tests/test_a.py: HandReaderInput RR-x  (0 -> 1)" in out
    elif case == "removed literal -> exit 1 stale":
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/test_a.py": "x = 1\n"}, [HAND_ROW])
        assert rc == 1 and "stale baseline row(s):" in out and "HandReaderInput RR-x" in out and "--update" in out
    elif case == "quarantined file not counted":
        rc, out = _hand_go(tmp_path, capsys, {}, [HAND_ROW])
        assert rc == 0 and "1 findings, 1 in the baseline" in out and "test_q.py" not in out and "test_field_producers" not in out
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/test-layers.json": json.dumps({"quarantine": {}})}, [HAND_ROW])
        assert rc == 1 and "test_q.py" in out                                      # twin: unquarantined -> counted
    elif case == "bad regex -> exit 2":
        bad = json.dumps({"hand_inputs": {"RR-x": ["(unclosed"]}})
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/fixtures/form-rounds.json": bad}, [])
        assert rc == 2 and "RR-x" in out and "(unclosed" in out and "cannot judge" in out
        empty = json.dumps({"hand_inputs": {}})                                    # twin: no families -> zero findings, no error
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/fixtures/form-rounds.json": empty}, [])
        assert rc == 0, out
        notobj = json.dumps({"hand_inputs": []})
        rc, out = _hand_go(tmp_path, capsys, {PKG + "/tests/fixtures/form-rounds.json": notobj}, [])
        assert rc == 2 and "hand_inputs" in out
    elif case == "missing form-rounds.json -> exit 2":
        make_repo(tmp_path, {k: v for k, v in HAND_FILES.items() if not k.endswith("form-rounds.json")})
        baseline_file(tmp_path, [])
        rc, out = go(tmp_path, capsys, roots=(PKG,))
        assert rc == 2 and "cannot judge" in out and "form-rounds.json" in out
        (tmp_path / PKG / "tests" / "fixtures").mkdir(parents=True)
        (tmp_path / PKG / "tests" / "fixtures" / "form-rounds.json").write_text("{not json", encoding="utf-8")
        rc, out = go(tmp_path, capsys, roots=(PKG,))
        assert rc == 2 and "not JSON" in out
        make_repo(tmp_path, HAND_FILES)
        (tmp_path / PKG / "tests" / "test-layers.json").write_text("{not json", encoding="utf-8")
        assert go(tmp_path, capsys, roots=(PKG,))[0] == 2                          # test-layers.json unreadable
    else:
        make_repo(tmp_path, dict(HAND_FILES, **{"src/a.py": CLEAN}))
        baseline_file(tmp_path, [])
        rc, out = go(tmp_path, capsys, roots=(PKG, "src"))                         # twin: root present -> judged (red: new literal)
        assert rc == 1 and "hand-input line: not run" not in out
        rc, out = go(tmp_path, capsys, roots=("src",))
        assert rc == 0 and "hand-input line: not run (package scripts root not among --root)" in out


def _package_tree_dirty() -> str:
    try:
        changes = DRT.status_changes(REPO, ["ai-packages"])       # the one git-status reader (B-455), not a second subprocess
    except RuntimeError as exc:
        return str(exc)
    return "uncommitted package edits (another session's work moves the findings)" if changes else ""


def test_the_real_tree_skip_reads_git_through_dup_ratchets_one_status_reader(monkeypatch):
    """B-455: no second git-status subprocess here; the verdict (clean / dirty / git cannot say) is the reader's, mapped."""
    calls = []

    def reader(repo, pathspec):
        calls.append((repo, list(pathspec)))
        return answer[0]

    answer = [[]]
    monkeypatch.setattr(DRT, "status_changes", reader)
    assert _package_tree_dirty() == ""
    answer[0] = ["ai-packages/qa-factory/x.py"]
    assert _package_tree_dirty().startswith("uncommitted package edits")
    answer[0] = RuntimeError("git status failed: fatal")

    def raising(repo, pathspec):
        raise answer[0]

    monkeypatch.setattr(DRT, "status_changes", raising)
    assert _package_tree_dirty() == "git status failed: fatal"
    assert calls == [(REPO, ["ai-packages"])] * 2


def test_k12_shipped_baseline_matches_the_real_tree(capsys):
    reason = _package_tree_dirty()
    if reason:
        pytest.skip("K12 skipped: " + reason + "; the integrator regenerates tools/lint-baseline.json with --update at the commit")
    rc = LR.run(["--check"])
    out = capsys.readouterr().out
    assert rc == 0, out


def test_k13_shipped_baseline_paths_are_posix_and_relative():
    doc = json.loads((TOOLS / "lint-baseline.json").read_text(encoding="utf-8"))
    assert doc["rows"], "the shipped baseline has no rows"
    for r in doc["rows"]:
        p = r["path"]
        assert "\\" not in p, p
        assert not (len(p) > 1 and p[1] == ":"), p
        assert not p.startswith("/"), p
        assert r["class"] not in LR.FATAL_CLASSES
