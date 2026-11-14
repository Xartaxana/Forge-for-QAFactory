"""test_dispatch_new.py -- tools/dispatch_new.py through its CLI door (offload C1, F-T1): one table of args -> exit, stdout
headers, stderr text; the round trip is judged by the checker and the header reader themselves."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dispatch_manifest as dm  # noqa: E402
import dispatch_new  # noqa: E402

OWN = "C:\\r\\tools\\a.py"
HAND = "C:\\r\\docs\\tasks\\handoffs\\t-1.md"
BASE = ["--kind", "builder", "--task", "t-862", "--given", "C:\\r\\spec.md", "--owns", OWN,
        "--non-goals", "none here", "--handoff", HAND, "--edges", "E-1 x", "--dod", "python -m pytest x -q",
        "--siblings", "none -- single file"]


def run(capsys, argv):
    code = dispatch_new.main(argv)
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


THREE_OWNS = swap(BASE, "--owns", None) + ["--owns", OWN, "C:\\r\\tools\\b.py", "C:\\r\\tools\\c.py"]

# id, argv, exit, substrings of stdout, substrings of stderr
CASES = [
    ("ok", BASE, 0, ["task: t-862", "owns:\nC:\\r\\tools\\a.py\n", "DoD: `python -m pytest x -q`"], []),
    ("ok-node-feature", BASE + ["--feature", "F19", "--node", "forge/5/F5-2"],
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
    ("E-C1-5-missing-given", swap(BASE, "--given", "C:\\no\\such\\file.md"), 0, ["C:\\no\\such\\file.md"],
     ["--given path(s) not found"]),
    ("E-C1-6-task-letter", swap(BASE, "--task", "t-123a"), 0, ["task: t-123a"], []),
    ("E-C1-6-task-bad", swap(BASE, "--task", "t-12"), 2, [], ["ID REFUSED", "--task"]),
    ("E-C1-6-task-case", swap(BASE, "--task", "T-123"), 2, [], ["ID REFUSED"]),
    ("bad-node", BASE + ["--node", "forge/0/x"], 2, [], ["ID REFUSED", "--node"]),
    ("bad-feature", BASE + ["--feature", "x1"], 2, [], ["ID REFUSED", "--feature"]),
    ("empty-edges", swap(BASE, "--edges", ""), 2, [], ["DISPATCH INCOMPLETE", "edges"]),
    ("bare-none-siblings", swap(BASE, "--siblings", "none"), 2, [], ["DISPATCH INCOMPLETE", "siblings"]),
    ("cyrillic-and-space-path", swap(BASE, "--owns", "C:\\r\\my dir\\\u0444.py"), 0, ["`C:\\r\\my dir\\\u0444.py`"], []),
    ("critic-no-owns", ["--kind", "critic", "--task", "t-505", "--handoff", "C:\\r\\docs\\tasks\\specs\\reviews\\x.md"],
     0, ["task: t-505"], []),
]


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
    assert [p.path for p in dm.owned_paths(dm.section_cut(out))] == asked
