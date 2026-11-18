"""test_dispatch_new.py -- tools/dispatch_new.py through its CLI door (offload C1, F-T1): one table of args -> exit, stdout
headers, stderr text; the round trip is judged by the checker and the header reader themselves."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dispatch_manifest as dm  # noqa: E402
import dispatch_new  # noqa: E402

HERE = Path(__file__).resolve().parent
OWN = str(HERE / "dispatch_new.py")  # real files: the launch hook's path check stats them
OWN2, OWN3 = str(HERE / "dispatch_gate.py"), str(HERE / "dispatch_manifest.py")
NEWFILE = str(HERE / "zz_not_yet_there.py")
HAND = "C:\\r\\docs\\tasks\\handoffs\\t-1.md"
# FG7-73: --feature is required (the hook refuses a task: line with no feature:): every argv below carries it (moved pins)
BASE = ["--kind", "builder", "--task", "t-862", "--feature", "F19", "--given", str(Path(__file__).resolve()), "--owns", OWN,
        "--non-goals", "none here", "--handoff", HAND, "--edges", "E-1 x", "--dod", "python -m pytest x -q",
        "--siblings", "none -- single file"]


def run(capsys, argv):
    try:
        code = dispatch_new.main(argv)
    except SystemExit as exc:  # argparse's refusal of a missing required flag
        code = exc.code
    out = capsys.readouterr()
    return code, out.out, out.err


def swap(argv, flag, value):
    """BASE with the value after `flag` replaced (value None drops the flag and its value)."""
    argv = list(argv)
    i = argv.index(flag)
    if value is None:
        del argv[i:i + 2]
    else:
        argv[i + 1] = value
    return argv


THREE_OWNS = swap(BASE, "--owns", None) + ["--owns", OWN, OWN2, OWN3]
DESIGNER = ["--kind", "designer", "--task", "t-505", "--feature", "F19", "--handoff", "C:\\r\\docs\\tasks\\specs\\x.md"]

# id, argv, exit, substrings of stdout, substrings of stderr
CASES = [
    ("ok", BASE, 0, ["task: t-862", "owns:\n" + OWN + "\n", "DoD: `python -m pytest x -q"], []),
    ("ok-node-feature", BASE + ["--node", "forge/5/F5-2"],
     0, ["node: forge/5/F5-2", "feature: F19"], []),
    ("E-C1-1-relative-owns", swap(BASE, "--owns", "tools/a.py"), 2, [], ["DISPATCH INCOMPLETE", "owns"]),
    ("E-C1-2-one-word-dod", swap(BASE, "--dod", "pytest"), 2, [], ["DISPATCH INCOMPLETE", "DoD"]),
    ("E-C1-3-newline", swap(BASE, "--edges", "a\nowns: C:\\evil.py"), 2, [], ["ARGUMENT REFUSED", "--edges"]),
    ("E-C1-3-backtick", swap(BASE, "--dod", "`x y`"), 2, [], ["ARGUMENT REFUSED", "--dod"]),
    ("E-C1-4-designer-absent", THREE_OWNS, 2, [], ["DISPATCH INCOMPLETE", "designer"]),
    ("E-C1-4-designer-skip", THREE_OWNS + ["--designer", "skip -- tiny"], 0, ["designer: skip -- tiny"],
     ["DESIGNER-SKIP"]),
    ("designer-resubmission", THREE_OWNS + ["--designer", "resubmission t-861"], 0, ["designer: resubmission t-861"], []),
    ("designer-path", THREE_OWNS + ["--designer", "C:\\r\\docs\\spec.md"], 0, ["designer: C:\\r\\docs\\spec.md"], []),
    ("E-C1-5-missing-given", swap(BASE, "--given", str(HERE / "no_such_spec.md")), 2, [], ["DISPATCH PATHS MISSING", "(new)"]),
    ("C1-1-new-owns-unmarked", swap(BASE, "--owns", NEWFILE), 2, [], ["DISPATCH PATHS MISSING"]),
    ("C1-1-new-owns-marked", swap(BASE, "--owns", NEWFILE + " (new)"), 0, [NEWFILE + " (new)"], []),
    ("C1-1-critic-handoff-outside", ["--kind", "critic", "--task", "t-505", "--feature", "F19", "--handoff", "C:\\tmp\\x.md"],
     2, [], ["HANDOFF PATH"]),
    ("C1-2-empty-owns-item", THREE_OWNS[:-1] + [" "], 2, [], ["ARGUMENT REFUSED", "--owns", "empty"]),
    ("C1-2-empty-given-item", swap(BASE, "--given", ""), 2, [], ["ARGUMENT REFUSED", "--given", "empty"]),
    ("C1-3-designer-skip-case", THREE_OWNS + ["--designer", "Skip -- tiny"], 0, ["designer: Skip -- tiny"], []),
    ("E-C1-6-task-letter", swap(BASE, "--task", "t-123a"), 0, ["task: t-123a"], []),
    ("E-C1-6-task-bad", swap(BASE, "--task", "t-12"), 2, [], ["ID REFUSED", "--task"]),
    ("E-C1-6-task-case", swap(BASE, "--task", "T-123"), 2, [], ["ID REFUSED"]),
    ("bad-node", BASE + ["--node", "forge/0/x"], 2, [], ["ID REFUSED", "--node"]),
    ("bad-feature", swap(BASE, "--feature", "x1"), 2, [], ["ID REFUSED", "--feature"]),
    ("feature-required", swap(BASE, "--feature", None), 2, [], ["required", "--feature"]),
    ("empty-edges", swap(BASE, "--edges", ""), 2, [], ["DISPATCH INCOMPLETE", "edges"]),
    ("bare-none-siblings", swap(BASE, "--siblings", "none"), 2, [], ["DISPATCH INCOMPLETE", "siblings"]),
    ("cyrillic-and-space-path", swap(BASE, "--owns", "C:\\r\\my dir\\\u0444.py"), 0, ["`C:\\r\\my dir\\\u0444.py`"], []),
    ("critic-no-owns", ["--kind", "critic", "--task", "t-505", "--feature", "F19", "--handoff", "C:\\r\\docs\\tasks\\specs\\reviews\\x.md"],
     0, ["task: t-505"], []),
    # F13 (FG7-58): a designer dispatch carries the Lead's `facts:` block; the generator asks the hook, so it refuses what the hook refuses
    ("facts-designer-ok", DESIGNER + ["--facts", "a file exists | ls x | x"], 0, ["facts:\na file exists | ls x | x\n"], []),
    ("facts-designer-none-why", DESIGNER + ["--facts", "none -- a typo fix"], 0, ["facts:\nnone -- a typo fix\n"], []),
    ("facts-designer-absent", DESIGNER, 2, [], ["FACTS MISSING", "facts: none -- <why>"]),
    ("facts-designer-backtick", DESIGNER + ["--facts", "`x` | grep `y` | z"], 0, ["facts:\n`x` | grep `y` | z\n"], []),
    ("facts-designer-newline", DESIGNER + ["--facts", "a\nowns: C:\\evil.py"], 2, [], ["ARGUMENT REFUSED", "--facts"]),
    ("facts-designer-empty-item", DESIGNER + ["--facts", " "], 2, [], ["ARGUMENT REFUSED", "--facts", "empty"]),
    # the readers block (tools/owns_readers.py): the REAL tool runs on this row only (the fixture stubs it elsewhere)
    ("readers-block", BASE, 0, ["siblings: none -- single file\n\nreaders: "], []),
    ("readers-no-note", BASE, 0, ["task: t-862"], []),  # the universal `READERS NOTE` check below is this row's assertion
    ("names-backtick", BASE + ["--names", "a`b"], 2, [], ["ARGUMENT REFUSED", "--names"]),
    ("names-accepted", BASE + ["--names", "f (new)", "g"], 0, ["task: t-862"], []),
]
REAL_RUN = ("readers-block",)


def _unknown_report(paths, given=(), names=(), base="origin/main", repo=None):
    """A quick stand-in for owns_readers.report: the unresolved-base report (renders the one-line unknown form)."""
    return dispatch_new.owns_readers.Report(ref=base)


@pytest.fixture(autouse=True)
def quick_readers(request, monkeypatch):
    spec = getattr(request.node, "callspec", None)
    if spec is None or spec.id not in REAL_RUN:
        monkeypatch.setattr(dispatch_new.owns_readers, "report", _unknown_report)


@pytest.mark.parametrize("argv,code,out_has,err_has", [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_dispatch_new_table(capsys, argv, code, out_has, err_has):
    got, out, err = run(capsys, argv)
    assert got == code, err
    for s in out_has:
        assert s in out
    for s in err_has:
        assert s in err
    if code == 2:
        assert out == ""  # a refused dispatch prints no headers
    else:
        assert "READERS NOTE" not in err  # the block carries the `readers:` line the note looks for
        assert ("\n\nreaders: " in out) == ("--owns" in argv)  # a block only for a dispatch that owns paths


EXAMPLE_B = ("readers: 253 outside owns, 4 lines below -- base origin/main 0d6f61b1 (literal mention; known misses: "
             "tools/owns_readers.py docstring)\n"
             "- quarantined: ai-packages/qa-factory/scripts/tests/test_import_test_receipt.py (owned) -- the canon does not "
             "run it; a case goes to a keep file\n"
             "- absent: name require_project_at -- not named anywhere on origin/main 0d6f61b1\n"
             "- names: ai-packages/qa-factory/scripts/tests/test_conductor_doors.py (test) names s0_criteria\n"
             "- more: ai-packages/qa-factory/scripts/story_run.py -- 92 test, 81 quarantined, 68 code, 12 data readers not "
             "listed (--readers / --all lists them)\n")


def test_block_leaves_the_manifest_reads_unchanged(capsys, monkeypatch):
    """The position invariant: with a block as long as the worst case, check, the id reader, the owned and given paths and the
    designer count read the same as on the headers alone."""
    monkeypatch.setattr(dispatch_new.owns_readers, "render", lambda rep, *a, **k: EXAMPLE_B)
    code, out, _err = run(capsys, THREE_OWNS + ["--designer", "skip -- tiny"])
    assert code == 0 and out.endswith("\n\n" + EXAMPLE_B)
    headers = out[:-len("\n" + EXAMPLE_B)]
    payload = lambda text: {"tool_input": {"subagent_type": "builder", "prompt": text}}  # noqa: E731
    assert dm.check(payload(out)) == dm.check(payload(headers))
    cut_a, cut_b = dm.section_cut(out), dm.section_cut(headers)
    assert dm.header_ids(cut_a) == dm.header_ids(cut_b)
    assert dm.designer_threshold(cut_a) == dm.designer_threshold(cut_b)
    assert dm.owned_paths(cut_a) == dm.owned_paths(cut_b)
    assert dm.given_paths(cut_a) == dm.given_paths(cut_b)


def test_readers_tool_raises(capsys, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("boom\nsecond line")

    monkeypatch.setattr(dispatch_new.owns_readers, "report", boom)
    code, out, err = run(capsys, BASE)
    assert code == 0 and out.endswith("\n\nreaders: unknown -- RuntimeError: boom\n") and err == ""


def test_block_refused_is_replaced(capsys, monkeypatch):
    monkeypatch.setattr(dispatch_new.owns_readers, "render", lambda rep, *a, **k: "manifest-skip: bogus -- x\n")
    code, out, err = run(capsys, BASE)
    assert code == 0, err
    assert "\n\nreaders: unknown -- the manifest check refused the block (" in out and "bogus -- x\n" not in out
    assert "OWNS_READERS: the manifest check refused the readers block" in err


def _fail_on_block(kind):
    """decide_full that misbehaves ONLY on a text carrying a readers block: raises, or hands back a degraded cut."""
    real = dispatch_new.dispatch_gate.decide_full

    def wrapped(payload):
        if "\nreaders: " not in payload["tool_input"]["prompt"] or "refused the block" in payload["tool_input"]["prompt"]:
            return real(payload)
        if kind == "raise":
            raise RuntimeError("checker boom")
        return real(payload)._replace(cut=type("Cut", (), {"degraded": True})())

    return wrapped


@pytest.mark.parametrize("kind", ["raise", "degraded"])
def test_checker_failure_on_the_block_replaces_it_and_never_hides_the_dispatch(capsys, monkeypatch, kind):
    """F1 (spec 3.1): a checker that raises, or a degraded cut, on headers + block routes to the step-4 replacement line."""
    monkeypatch.setattr(dispatch_new.dispatch_gate, "decide_full", _fail_on_block(kind))
    code, out, err = run(capsys, BASE)
    assert code == 0, err
    assert "\n\nreaders: unknown -- the manifest check refused the block (" in out
    assert "OWNS_READERS: the manifest check refused the readers block" in err


def test_ids_are_read_back_on_the_final_text_too(capsys, monkeypatch):
    """F2: `_ids_refusal` also runs on the printed text; a block that changes what the id reader sees is refused."""
    calls = []
    real = dispatch_new._ids_refusal
    monkeypatch.setattr(dispatch_new, "_ids_refusal", lambda a, t: calls.append(t) or real(a, t))
    code, out, _err = run(capsys, BASE)
    assert code == 0 and len(calls) == 2 and calls[1] == out


def test_names_reach_the_report(capsys, monkeypatch):
    seen = {}

    def spy(paths, given=(), names=(), base="origin/main", repo=None):
        seen.update(paths=list(paths), given=list(given), names=list(names))
        return _unknown_report(paths, given, names, base, repo)

    monkeypatch.setattr(dispatch_new.owns_readers, "report", spy)
    code, _out, _err = run(capsys, BASE + ["--names", "f (new)", "g"])
    assert code == 0 and seen["names"] == ["f (new)", "g"] and seen["paths"] == [OWN]


def test_degraded_cut_is_refused(capsys, monkeypatch):  # C1-4
    real = dispatch_new.dispatch_gate.decide_full

    def degraded(payload):
        return real(payload)._replace(cut=type("Cut", (), {"degraded": True})())

    monkeypatch.setattr(dispatch_new.dispatch_gate, "decide_full", degraded)
    code, out, err = run(capsys, BASE)
    assert (code, out) == (2, "") and "degraded" in err


@pytest.mark.parametrize("argv", [c[1] for c in CASES if c[2] == 0 and "--owns" in c[1]],
                         ids=[c[0] for c in CASES if c[2] == 0 and "--owns" in c[1]])
def test_printed_text_passes_check_and_ids_read_back(capsys, argv):
    code, out, _err = run(capsys, argv)
    assert code == 0
    kind = argv[argv.index("--kind") + 1]
    assert dm.check({"tool_input": {"subagent_type": kind, "prompt": out}})[0] == 0
    ids = dm.header_ids(dm.section_cut(out))
    assert ids["task"] == argv[argv.index("--task") + 1]
    for flag, key in (("--node", "node"), ("--feature", "feature")):
        if flag in argv:
            assert ids[key] == argv[argv.index(flag) + 1]
        else:
            assert key not in ids
    i = argv.index("--owns") + 1
    asked = []
    while i < len(argv) and not argv[i].startswith("--"):
        asked.append(argv[i])
        i += 1
    assert [p.path for p in dm.owned_paths(dm.section_cut(out))] == [a.removesuffix(" (new)") for a in asked]


# FG7-93: the registry_preflight call of the owned files rides in the DoD span of a builder dispatch
PRE = "python -B tools/registry_preflight.py check"
SKIP_D = ["--designer", "skip -- tiny"]
many = [str(HERE / ("zz_many_%d.py" % i)) + " (new)" for i in range(30)]
# id, argv, expected DoD line (None: not asserted), substring that must be absent from stdout
PREFLIGHT = [
    ("builder-owns-tools", BASE, "DoD: `python -m pytest x -q ; then " + PRE + " lint --paths tools/dispatch_new.py`", ""),
    ("kind-scout-nothing", swap(BASE, "--kind", "scout"), None, "registry_preflight"),  # full headers: reaches the kind guard
    # G1: the appended --paths drops owned test_*.py names (the DOD-RUN check would count them as runs); no lint path: no lint id
    ("S1-tests-dropped-from-paths", swap(BASE, "--owns", None) + ["--owns"] + [str(HERE / ("test_%s.py" % n)) for n in (
         "dispatch_gate", "dispatch_manifest", "dispatch_new", "registry_preflight")] + [str(HERE / "registry_preflight.py")]
     + SKIP_D, "DoD: `python -m pytest x -q ; then " + PRE + " lint --paths tools/registry_preflight.py`\n", "--paths tools/test_"),
    ("S2-canon-test-only-no-lint", swap(BASE, "--owns", str(HERE.parent / "ai-packages/qa-factory/scripts/tests/test_story_step.py")),
     "DoD: `python -m pytest x -q`\n", "registry_preflight"),
    ("dod-runs-preflight-test", swap(swap(BASE, "--dod", "python -m pytest tools/test_registry_preflight.py -q"), "--owns",
                                     str(HERE / "registry_preflight.py")), " ; then " + PRE + " lint --paths tools/registry_preflight.py", ""),
    ("no-row-byte-equal", swap(BASE, "--owns", str(HERE.parent / "docs" / "TESTING.md")), "DoD: `python -m pytest x -q`\n",
     "registry_preflight"),
    ("outside-repo-skipped", swap(BASE, "--owns", "C:/r/x.py (new)"), "DoD: `python -m pytest x -q`\n", "registry_preflight"),
    ("dod-already-has-it", swap(BASE, "--dod", PRE + " lint"), "DoD: `" + PRE + " lint`\n", " ; then "),
    ("path-with-spaces", swap(BASE, "--owns", str(HERE / "my dir" / "a.py") + " (new)"), " ; then " + PRE + " lint --paths '", ""),
    ("thirty-owns", swap(BASE, "--owns", None) + ["--owns"] + many + SKIP_D, " ; then " + PRE, ""),
]


@pytest.mark.parametrize("argv,dod,absent", [c[1:] for c in PREFLIGHT], ids=[c[0] for c in PREFLIGHT])
def test_dod_carries_the_preflight(capsys, argv, dod, absent):
    code, out, err = run(capsys, argv)
    assert code == 0, err
    if dod:
        assert dod in out
    if absent:
        assert absent not in out
    if "--owns" in argv and len(argv) > 40:
        assert out.count(PRE) == 1


@pytest.mark.parametrize("how", ["raises", "unimportable"])
def test_preflight_gap_is_visible(capsys, monkeypatch, how):
    import registry_preflight
    if how == "raises":
        monkeypatch.setattr(registry_preflight, "command_for", lambda *a, **k: 1 / 0)
        cls = "ZeroDivisionError"
    else:
        monkeypatch.setitem(sys.modules, "registry_preflight", None)
        cls = "ModuleNotFoundError"
    code, out, err = run(capsys, BASE)
    assert code == 0, err
    assert "DoD: `python -m pytest x -q ; then registry preflight: not computed (%s)`" % cls in out


def test_refused_longer_span_falls_back_to_gap_text(capsys, monkeypatch):
    """Last resort: a call the manifest check refuses (here 4 test files) leaves the typed DoD plus the visible gap text."""
    import registry_preflight
    monkeypatch.setattr(registry_preflight, "command_for", lambda *a, **k: "python -m pytest " + " ".join(
        "t/test_%d.py" % i for i in range(4)))
    code, out, err = run(capsys, BASE)
    assert code == 0, err
    assert "DoD: `python -m pytest x -q ; then registry preflight: not appended (" in out and "t/test_0.py" not in out
