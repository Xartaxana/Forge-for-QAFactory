"""Tests for tools/test_split.py (TD-11 node T-3): the splitter of one test file into parts, and its no-lost-check proof.

ONE parameterised table over tiny fixture sources built in tmp_path (a stub `harness` and `runner_lib` stand beside the
source, so the generated parts really run as scripts). Each case names one behaviour of the door
(`--map ... --dry-run|--apply`, `--draft`) or of the proof; a refusal case also asserts that NOTHING was written.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
from unittest import mock

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import test_split as ts  # noqa: E402

HARNESS = '''import sys
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name)
    return bool(ok)


def check_eq(name, got, expected):
    return check(name, got == expected)


def finish(label):
    bad = sum(1 for r in RESULTS if not r)
    print(f"=== {label}: {len(RESULTS) - bad}/{len(RESULTS)} ok ===")
    sys.exit(1 if bad else 0)
'''
RUNNER_LIB = '''def run_scenarios(side_by_side, in_process):
    for one in list(side_by_side) + list(in_process):
        one()
'''

HEAD = '''"""Demo tests."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq  # noqa: E402
from runner_lib import run_scenarios  # noqa: E402

TASK = "QA-1"


def helper(x):
    return x + 1


# --- group a -------------------------------------------------------------------------
def a_one():
    check("a1", helper(1) == 2)
    check_eq("a1b", json.dumps(1), "1")


def a_two():
    check("a2", True)


# --- group b -------------------------------------------------------------------------

def b_one():
    check_eq("b1", TASK, "QA-1")


def b_two():
    check("b2", True)


def never_run():
    check("never", True)


'''
SRC_RUN = HEAD + '''def main() -> None:
    run_scenarios([a_one, b_one], [a_two, b_two])
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_CALLS = HEAD + '''def main():
    a_one()
    b_one()
    a_two()
    b_two()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_BAD_RUNNER = HEAD + '''def main():
    if len(sys.argv) > 1:
        a_one()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_LOOP = '''"""Loop demo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, finish  # noqa: E402

START = 5


def scenario(fn):
    fn()


def a_one():
    check("a1", START == 5)


def b_one():
    check_eq("b1", START, 5)


def b_two():
    check("b2", True)


SCENARIOS = (a_one, b_one, b_two)

# `test_loop.py a_one` runs only that one
for _fn in SCENARIOS:
    if not sys.argv[1:] or _fn.__name__ in sys.argv[1:]:
        scenario(_fn)

finish("test_loop")
'''
SRC_STATEMENT = HEAD.replace("TASK = \"QA-1\"\n", "TASK = \"QA-1\"\nTABLE = {}\nfor _k in range(3):\n    TABLE[_k] = _k\nos.chdir(os.getcwd())\n") \
    .replace("import json\n", "import json\nimport os\n") + SRC_RUN[len(HEAD):]
IMPORTER = "import test_demo as D\nfrom test_demo import TASK\nprint(D.helper(1), TASK)\n"

# --- the runner shapes of the real tree (T-B1) -------------------------------------------------------------------------------
SRC_GUARD_CALLS = HEAD + '''if __name__ == "__main__":
    a_one()
    b_one()
    a_two()
    b_two()
    harness.finish("test_demo")
'''
SRC_FOR_IN_MAIN = HEAD + '''def main() -> None:
    for scenario in (a_one, b_one, a_two, b_two):
        scenario()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_BY_NAME_MAIN = HEAD + '''SCENARIOS = [a_one, b_one, a_two, b_two]


def main() -> None:
    wanted = sys.argv[1:]
    chosen = [s for s in SCENARIOS if not wanted or any(s.__name__.startswith(prefix) for prefix in wanted)]
    if not chosen:
        sys.exit(f"test_demo: no scenario starts with {wanted}")
    run_scenarios([], chosen)
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_SCRIPT = '''"""A module-level script."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402

DATA = [1, 2]
check("script 1", len(DATA) == 2)
check("script 2", True)
harness.finish("test_demo")
'''
SRC_MINI = '''"""Mini."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402


def a_one():
    check("a", True)


def b_one():
    check("b", True)


def main():
    a_one()
    b_one()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
MINI_HOMES = {"a_one": ("def", "a"), "b_one": ("def", "b")}

# --- the classes in which a green proof used to hide a changed run (T-B2) -----------------------------------------------------
SRC_COMMON_CHECK = SRC_RUN.replace('TASK = "QA-1"\n', 'TASK = "QA-1"\nSEEN = check("m1", True)\ncheck("m2", True)\n')
SRC_STMT_BEFORE_IMPORT = '''"""Demo."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402

os.environ["DEMO_K"] = "1"
import runner_lib  # noqa: E402


def a_one():
    check("a", runner_lib is not None and json is not None)


def b_one():
    check("b", True)


def main():
    a_one()
    b_one()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_REBIND = SRC_RUN.replace('TASK = "QA-1"\n', 'FLAG = False\nif sys.argv[1:]:\n    FLAG = True\nTASK = "QA-1"\n')
SRC_LATE_IMPORT = SRC_RUN.replace("def main() -> None:", "from json import dumps as helper  # noqa: E402\n\n\ndef main() -> None:")
SRC_GLOBAL = SRC_RUN.replace('TASK = "QA-1"\n', 'TASK = "QA-1"\nSTATE = 0\n\n\ndef bump():\n    global STATE\n    STATE += 1\n') \
    .replace('check("a2", True)', 'bump()\n    check("a2", STATE == 1)')
SRC_MUTATION = SRC_RUN.replace('TASK = "QA-1"\n', 'TASK = "QA-1"\nITEMS = [1]\nITEMS.append(2)\n')
SRC_NESTED_CALL = SRC_LOOP.replace("def scenario(fn):", 'def extra():\n    check("x1", True)\n\n\ndef scenario(fn):') \
    .replace("        scenario(_fn)\n", "        scenario(_fn)\n        extra()\n")
SRC_NESTED_CHECKER = SRC_LOOP.replace("def scenario(fn):", 'def checker(n):\n    check("x1", n == 1)\n\n\ndef scenario(fn):') \
    .replace("        scenario(_fn)\n", "        scenario(_fn)\n        checker(1)\n")

# --- F1/F2 of node N2: an import kept for its sys.path effect; a closing in every part -----------------------------------------
# `path_helper` (beside the test) puts `../libdir/` on sys.path; `libmod` lives there and only a part that imported `path_helper` finds it
PATH_HELPER = 'import sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent / "libdir"))\n\n\ndef marker():\n    return 2\n'
SRC_PATHFX = '''"""Demo."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402
from path_helper import marker  # noqa: E402
import libmod  # noqa: E402


def a_one():
    check("a", libmod.VALUE == json.loads("1"))


def b_one():
    check("b", marker() == 2)


def main():
    a_one()
    b_one()
    harness.finish("test_demo")


if __name__ == "__main__":
    main()
'''
SRC_OTHER_TEST = SRC_PATHFX.replace("import libmod  # noqa: E402\n", "import libmod  # noqa: E402\nimport test_other  # noqa: E402\n")
SRC_GUARD_MAIN = HEAD + '''def c_one():
    check("c", True)


def main():
    a_one()
    b_one()
    a_two()
    b_two()
    harness.finish("test_demo")


if __name__ == "__main__":
    c_one()
    main()
'''
SRC_NO_CLOSING = SRC_GUARD_MAIN.replace('    harness.finish("test_demo")\n', "")
SRC_TWO_CLOSINGS = HEAD + '''def c_one():
    check("c", True)


def main1():
    a_one()
    harness.finish("first")


def main2():
    b_one()
    harness.finish("second")


if __name__ == "__main__":
    main1()
    c_one()
    main2()
'''
RUN_HOMES = {"TASK": ("assign", "c"), "helper": ("def", "c"), "a_one": ("def", "a"), "a_two": ("def", "a"),
             "b_one": ("def", "b"), "b_two": ("def", "b"), "never_run": ("def", "b")}
LOOP_HOMES = {"START": ("assign", "c"), "scenario": ("def", "c"), "a_one": ("def", "a"), "b_one": ("def", "b"), "b_two": ("def", "b")}
GUARD_HOMES = dict(RUN_HOMES, c_one=("def", "k"))          # three parts: a, b and k (k's one scenario is called by the guard itself)
PARTS_ABK = ("a", "b", "k")


def make_map(stem, homes, shim=False, statements=None, parts=("a", "b")):
    common = ("" if not stem.startswith("test_") else stem[5:]) + "_common"
    names = {"c": common, **{p: f"{stem}_{p}" for p in parts}}
    return {"source": stem + ".py", "common": common, "shim": shim, "parts": [names[p] for p in parts],
            "names": [{"name": n, "kind": k, "home": names[h]} for n, (k, h) in homes.items()],
            "statements": [{"line": ln, "home": names[h]} for ln, h in (statements or [])]}


def world(tmp_path, source, map_, extra=None, newline="\n", name="test_demo.py"):
    repo = tmp_path / "repo"
    tests = repo / ts.TESTS_REL
    tests.mkdir(parents=True)
    (tests / "harness.py").write_text(HARNESS, encoding="utf-8")
    (tests / "runner_lib.py").write_text(RUNNER_LIB, encoding="utf-8")
    (tests / name).write_bytes(source.replace("\n", newline).encode("utf-8"))
    for fname, text in (extra or {}).items():
        (tests / fname).write_text(text, encoding="utf-8")
    mp = tmp_path / "map.json"
    mp.write_text(json.dumps(map_), encoding="utf-8")
    return repo, tests, mp


def snapshot(tests):
    return {p.name: p.read_bytes() for p in sorted(tests.iterdir())}


def door(repo, mp, mode, capsys):
    code = ts.main(["--map", str(mp), mode, "--repo", str(repo)])
    cap = capsys.readouterr()
    return code, cap.out + cap.err


def run_part(tests, name, *args):
    done = subprocess.run([sys.executable, "-B", str(tests / name), *args], cwd=tests, capture_output=True, text=True)
    return done.returncode, done.stdout


def tally(out):
    return [l for l in out.splitlines() if l.startswith("=== ")]


def tampered(plan, name, old, new, imports=False):
    files = {n: ts.to_bytes(plan, t) for n, t in plan.files.items()}
    text = files[name].decode("utf-8")
    assert old in text, (old, text)
    files[name] = text.replace(old, new, 1).encode("utf-8")
    return ts.prove(plan, files, imports=imports)


# ----------------------------------------------------------------------------------------------- the cases

def case_run_scenarios_two_list(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0, out
    assert "PROOF: ok" in out and not (tests / "test_demo.py").exists()
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    b = (tests / "test_demo_b.py").read_text(encoding="utf-8")
    assert "run_scenarios([\n        a_one,\n    ], [\n        a_two,\n    ])" in a
    assert "run_scenarios([\n        b_one,\n    ], [\n        b_two,\n    ])" in b
    assert 'harness.finish("test_demo_a")' in a and 'harness.finish("test_demo_b")' in b
    assert "# --- group b" in b and "# --- group b" not in a        # the free section marker went with the first name below it
    assert "import json" in a and "import json" not in b            # imports reduced to what each part uses
    assert "from demo_common import" in a and "never_run" in b
    assert "never_run" not in a
    assert run_part(tests, "test_demo_a.py")[0] == 0
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 3/3 ok ==="]
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 2/2 ok ==="]      # never_run stays unrun
    assert "UNREACHED: `never_run`" in out


def case_main_with_direct_calls(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_CALLS, make_map("test_demo", RUN_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0, out
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    assert a.index("    a_one()") < a.index("    a_two()") and "b_one()" not in a
    assert 'harness.finish("test_demo_a")' in a and '"__main__"' in a
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 2/2 ok ==="]


def case_module_loop_with_argv_filter(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_LOOP, make_map("test_loop", LOOP_HOMES), name="test_loop.py")
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0, out
    b = (tests / "test_loop_b.py").read_text(encoding="utf-8")
    assert "SCENARIOS = (\n    b_one,\n    b_two,\n)" in b and "def a_one" not in b
    assert "if not sys.argv[1:] or _fn.__name__ in sys.argv[1:]:" in b and 'finish("test_loop_b")' in b
    assert tally(run_part(tests, "test_loop_b.py")[1]) == ["=== test_loop_b: 2/2 ok ==="]
    assert tally(run_part(tests, "test_loop_b.py", "b_two")[1]) == ["=== test_loop_b: 1/1 ok ==="]       # the argv filter is kept


def case_shim_with_an_importer(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES, shim=True), extra={"test_user.py": IMPORTER})
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0, out
    assert "IMPORTERS found (spec 2.6): test_user.py: TASK, helper" in out
    shim = (tests / "test_demo.py").read_text(encoding="utf-8")
    assert ts.SHIM_MARK in shim and '__all__ = ["TASK", "helper"]' in shim and "def test_" not in shim
    assert "check(" not in shim.replace("no checks", "")
    assert run_part(tests, "test_demo.py")[0] == 0 and "no checks of its own" in run_part(tests, "test_demo.py")[1]
    code, ran = run_part(tests, "test_demo.py", "--all")
    assert code == 0 and "test_demo_a: 3/3 ok" in ran and "test_demo_b: 2/2 ok" in ran
    done = subprocess.run([sys.executable, "-B", str(tests / "test_user.py")], cwd=tests, capture_output=True, text=True)
    assert done.stdout.strip() == "2 QA-1"                                                   # the importer still works, unedited


def case_no_shim_refused_because_an_importer_exists(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES), extra={"test_user.py": IMPORTER})
    before = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 2 and "other tests import the source" in out and "test_user.py" in out
    assert snapshot(tests) == before


def case_name_used_by_two_parts_but_homed_in_a_part(tmp_path, capsys):
    homes = dict(RUN_HOMES, helper=("def", "a"), b_two=("def", "b"))
    src = SRC_RUN.replace('check("b2", True)', 'check("b2", helper(2) == 3)')
    repo, tests, mp = world(tmp_path, src, make_map("test_demo", homes))
    before = snapshot(tests)
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 2 and "`helper` (homed in `test_demo_a`) is used by `test_demo_b`" in out and "home `helper` in common" in out
    assert snapshot(tests) == before


def case_unplaced_statement_refused_then_placed_with_a_warning(tmp_path, capsys):
    homes = dict(RUN_HOMES, TABLE=("assign", "c"))
    repo, tests, mp = world(tmp_path, SRC_STATEMENT, make_map("test_demo", homes))
    before = snapshot(tests)
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 2 and "has no place" in out and "for _k in range(3)" in out and "os.chdir(os.getcwd())" in out
    assert snapshot(tests) == before
    lines = {l.split(":")[0] for l in SRC_STATEMENT.splitlines()}
    loop_line = SRC_STATEMENT.splitlines().index("for _k in range(3):") + 1
    chdir_line = SRC_STATEMENT.splitlines().index("os.chdir(os.getcwd())") + 1
    mp.write_text(json.dumps(make_map("test_demo", homes, statements=[(loop_line, "c"), (chdir_line, "c")])), encoding="utf-8")
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 0, out
    assert "WARNING: line %d runs at import and touches the world" % chdir_line in out and "once per part" in out
    assert lines and snapshot(tests) == before


def case_unrecognised_runner_refused(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_BAD_RUNNER, make_map("test_demo", RUN_HOMES))
    before = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    line = SRC_BAD_RUNNER.splitlines().index("    if len(sys.argv) > 1:") + 1
    assert code == 2 and f"test_demo.py:{line}: runner statement not recognised" in out
    assert snapshot(tests) == before


def case_proof_a_fails_when_a_part_drops_a_check(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    lines, ok = tampered(plan, "test_demo_a.py", '    check("a2", True)', "    pass")
    assert not ok and any(l.startswith("(a)") and "FAILED" in l for l in lines) and lines[-1] == "PROOF: FAILED"


def case_proof_c_fails_on_a_duplicated_scenario(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    lines, ok = tampered(plan, "test_demo_a.py", "        a_one,\n    ]", "        a_one,\n        a_one,\n    ]")
    assert not ok and any(l.startswith("(c)") and "FAILED" in l for l in lines)


def case_proof_d_fails_on_a_tampered_body(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    lines, ok = tampered(plan, "demo_common.py", "return x + 1", "return x + 2")
    assert not ok and any(l.startswith("(d)") and "FAILED" in l and "helper" in l for l in lines)
    assert any(l.startswith("(a)") and "ok" in l for l in lines)       # the check count alone would not have seen it


def case_rerun_says_nothing_to_do(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    assert door(repo, mp, "--apply", capsys)[0] == 0
    after = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "nothing to do" in out and snapshot(tests) == after
    # and the same for a shim
    tmp2 = tmp_path / "second"
    tmp2.mkdir()
    repo2, tests2, mp2 = world(tmp2, SRC_RUN, make_map("test_demo", RUN_HOMES, shim=True), extra={"test_user.py": IMPORTER})
    assert door(repo2, mp2, "--apply", capsys)[0] == 0
    after2 = snapshot(tests2)
    code, out = door(repo2, mp2, "--apply", capsys)
    assert code == 0 and "already a shim" in out and snapshot(tests2) == after2


def case_a_half_written_target_is_refused(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES), extra={"test_demo_a.py": "x = 1\n"})
    before = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 2 and "test_demo_a.py exists and the map does not fully explain it" in out
    assert snapshot(tests) == before


def case_a_row_is_missing_or_unknown_refuses_and_writes_nothing(tmp_path, capsys):
    homes = {k: v for k, v in RUN_HOMES.items() if k != "never_run"}
    homes["ghost"] = ("def", "a")
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", homes))
    before = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 2 and "name `never_run` has no row" in out and "`ghost` is not a top-level name" in out
    assert snapshot(tests) == before


def case_dry_run_writes_nothing_and_prints_the_proof(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    before = snapshot(tests)
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 0 and snapshot(tests) == before
    for key in ("(a) check call sites (AST sites, not executed checks): source 6, parts 6 + common 0 + shim 0",
                "(b) top-level names", "(c) run list", "(c2) run sites read again from the plain AST of the old file",
                "(d) byte identity", "(compile) 3 written file(s) compile", "(f) closing: each of 2 part runner(s) holds exactly one",
                "(g) import: 2 written file(s) (test_demo_a.py, test_demo_b.py) each imported alone", "NOT RUN HERE: spec 2.5 (e)",
                "PROOF: ok", "ROW BLOCK"):
        assert key in out, key
    assert "provisional seconds" in out


def case_crlf_source_keeps_its_newlines_and_a_mixed_one_is_refused(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES), newline="\r\n")
    assert door(repo, mp, "--apply", capsys)[0] == 0
    raw = (tests / "test_demo_a.py").read_bytes()
    assert raw.count(b"\r\n") == raw.count(b"\n") > 10 and raw.isascii()
    tmp2 = tmp_path / "mixed"
    tmp2.mkdir()
    repo2, tests2, mp2 = world(tmp2, SRC_RUN, make_map("test_demo", RUN_HOMES))
    (tests2 / "test_demo.py").write_bytes(SRC_RUN.replace("\n", "\r\n", 3).encode("utf-8"))
    before = snapshot(tests2)
    code, out = door(repo2, mp2, "--dry-run", capsys)
    assert code == 2 and "mixed newlines" in out and snapshot(tests2) == before
    (tests2 / "test_demo.py").write_bytes(b"\xef\xbb\xbf" + SRC_RUN.encode("utf-8"))
    code, out = door(repo2, mp2, "--dry-run", capsys)
    assert code == 2 and "BOM" in out


def case_draft_prints_every_name_its_runs_and_the_importers(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, {}, extra={"test_user.py": IMPORTER})
    code = ts.main(["--draft", ts.TESTS_REL + "/test_demo.py", "--repo", str(repo)])
    cap = capsys.readouterr()
    assert code == 0
    draft = json.loads(cap.out)
    rows = {r["name"]: r for r in draft["names"]}
    assert set(rows) == set(RUN_HOMES) and draft["shim"] is True and all(r["home"] == "" for r in rows.values())
    assert rows["a_one"]["_runs"] == ["func:main:arg0"] and rows["b_two"]["_runs"] == ["func:main:arg1"]
    assert rows["never_run"].get("_runs") is None and rows["a_one"]["_section"].startswith("# --- group a")
    assert draft["_notes"]["importers"] == {"test_user.py": ["TASK", "helper"]}
    assert draft["_notes"]["runner_names_not_in_names"] == ["main"]
    assert cap.err.startswith("draft: test_demo.py: 7 names (6 defs, 0 classes, 1 assignments)")
    assert "0 refused construct(s)" in cap.err
    # the draft is not a map yet: every home is empty, so the door refuses it and names the rows
    mp.write_text(json.dumps(dict(draft, parts=["test_demo_a"], shim=True)), encoding="utf-8")
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 2 and "home `` is not a part" in out


def case_the_door_exit_codes(tmp_path, capsys):
    assert ts.main(["--map", str(tmp_path / "none.json"), "--dry-run", "--repo", str(tmp_path)]) == 1
    capsys.readouterr()
    assert ts.main(["--dry-run"]) == 1
    capsys.readouterr()
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert ts.main(["--map", str(bad), "--apply", "--repo", str(tmp_path)]) == 1


def refused_case(tmp_path, capsys, source, homes, keys, stmts=(), stem="test_demo", extra=None, parts=("a", "b"), shim=False):
    """The map is refused with exit 2, every key is in the text, no proof line is printed and the tree is unchanged."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    lines = source.splitlines()
    statements = [(lines.index(text) + 1, home) for text, home in stmts]
    repo, tests, mp = world(tmp_path, source, make_map(stem, homes, statements=statements, parts=parts, shim=shim), extra=extra,
                            name=stem + ".py")
    before = snapshot(tests)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 2, out
    for key in keys:
        assert key in out, (key, out)
    assert "PROOF" not in out and "refused: nothing was written" in out and snapshot(tests) == before
    return out


# the runner shapes of the real tree (T-B1) -----------------------------------------------------------------------------------

def case_guard_of_direct_scenario_calls(tmp_path, capsys):
    """test_handoff_values: no `main`, an `if __name__` block that calls every scenario and finishes."""
    repo, tests, mp = world(tmp_path, SRC_GUARD_CALLS, make_map("test_demo", RUN_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    assert '__name__ == "__main__"' in a and "b_one()" not in a and a.index("    a_one()") < a.index("    a_two()")
    assert 'harness.finish("test_demo_a")' in a and "def a_one" in a and "def main" not in a
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 3/3 ok ==="]
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 2/2 ok ==="]


def case_for_over_a_literal_tuple_inside_main(tmp_path, capsys):
    """test_no_move_seam: `for scenario in (<names>): scenario()` inside `main`."""
    repo, tests, mp = world(tmp_path, SRC_FOR_IN_MAIN, make_map("test_demo", RUN_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out and "(c2)" in out, out
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    assert "for scenario in (\n        a_one,\n        a_two,\n    ):\n        scenario()" in a and "b_one" not in a
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 3/3 ok ==="]
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 2/2 ok ==="]


def case_run_scenarios_with_an_empty_first_list_in_a_by_name_main(tmp_path, capsys):
    """test_story_run_freshness: `chosen` is built from SCENARIOS, then `run_scenarios([], chosen)`."""
    repo, tests, mp = world(tmp_path, SRC_BY_NAME_MAIN, make_map("test_demo", RUN_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    assert "ARGV test_demo_a.py: a_one, a_two" in out and "ARGV test_demo_b.py: b_one, b_two" in out
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    assert "SCENARIOS = [\n    a_one,\n    a_two,\n]" in a and "run_scenarios([], chosen)" in a
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 3/3 ok ==="]
    assert tally(run_part(tests, "test_demo_a.py", "a_two")[1]) == ["=== test_demo_a: 1/1 ok ==="]
    code, ran = run_part(tests, "test_demo_a.py", "b_one")             # a name that moved to the other part: an error, not a green
    assert code != 0 and tally(ran) == []


def case_module_level_script_is_refused_by_the_draft_and_the_map(tmp_path, capsys):
    """test_grounding_table: checks run at module level and no scenario function exists: not supported, said by both doors."""
    repo, tests, mp = world(tmp_path, SRC_SCRIPT, {})
    code = ts.main(["--draft", ts.TESTS_REL + "/test_demo.py", "--repo", str(repo)])
    cap = capsys.readouterr()
    assert code == 2 and "1 refused construct(s)" in cap.err
    assert "module-level script" in cap.err and "not supported" in cap.err and "2 check call site(s)" in cap.err
    homes = {"DATA": ("assign", "a")}
    refused_case(tmp_path / "again", capsys, SRC_SCRIPT, homes, ["module-level script", "not supported by this tool"],
                 stmts=[('check("script 1", len(DATA) == 2)', "a"), ('check("script 2", True)', "a"), ('harness.finish("test_demo")', "a")],
                 parts=("a",))


# the classes in which the proof used to stay green while the run changed (T-B2) -------------------------------------------------

def case_module_level_check_homed_in_common_is_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_COMMON_CHECK, dict(RUN_HOMES, SEEN=("assign", "c")), [
        "a module-level assign that runs 1 check call site(s) is homed in common",
        "a module-level statement that runs 1 check call site(s) is homed in common"], stmts=[('check("m2", True)', "c")])


def case_scenario_call_nested_in_a_by_name_consumer_is_refused(tmp_path, capsys):
    homes = dict(LOOP_HOMES, extra=("def", "c"))
    refused_case(tmp_path, capsys, SRC_NESTED_CALL, homes, ["also calls a top-level function directly (`extra()`)"],
                 stem="test_loop")
    homes = dict(LOOP_HOMES, checker=("def", "c"))
    refused_case(tmp_path / "second", capsys, SRC_NESTED_CHECKER, homes, ["calls `checker`, a function that holds checks"],
                 stem="test_loop")
    # the block's own once-per-entry wrapper (handed the loop variable) may hold a check: test_infra_failure's `scenario(_fn)`
    (tmp_path / "third").mkdir()
    wrapped = SRC_LOOP.replace("    fn()\n", '    fn()\n    check("ran", True)\n', 1)
    repo, tests, mp = world(tmp_path / "third", wrapped, make_map("test_loop", LOOP_HOMES), name="test_loop.py")
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 0 and "PROOF: ok" in out, out


def case_statement_before_an_import_is_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_STMT_BEFORE_IMPORT, MINI_HOMES,
                 ["this statement runs before the import/sys.path line at"], stmts=[('os.environ["DEMO_K"] = "1"', "a")])


def case_conditional_rebinding_across_homes_is_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_REBIND, dict(RUN_HOMES, FLAG=("assign", "a")), ["`FLAG` is bound by statements homed apart"],
                 stmts=[("if sys.argv[1:]:", "c")])


def case_late_import_that_shadows_a_def_is_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_LATE_IMPORT, RUN_HOMES, ["`helper` is defined here and imported again later"])


def case_global_rebinding_of_a_common_name_read_by_a_part_is_refused(tmp_path, capsys):
    homes = dict(RUN_HOMES, STATE=("assign", "c"), bump=("def", "c"))
    refused_case(tmp_path, capsys, SRC_GLOBAL, homes, ["`global STATE` rebinds a name homed in common that a part reads"])


def case_mutating_statement_homed_apart_from_its_name_is_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_MUTATION, dict(RUN_HOMES, ITEMS=("assign", "c")), [
        "a module-level statement uses `ITEMS`, homed in `demo_common`, while it is homed in `test_demo_a`"],
        stmts=[("ITEMS.append(2)", "a")])


# the rest of the fix round: rollback, map shape, importer writes, empty edges, the second reading of the run list ----------------

def case_rollback_never_deletes_an_identical_target(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_RUN, make_map("test_demo", RUN_HOMES))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    (tests / "test_demo_a.py").write_bytes(ts.to_bytes(plan, plan.files["test_demo_a.py"]))     # left by an interrupted run
    before = snapshot(tests)
    real = ts.os.replace

    def failing(src, dst):
        if pathlib.Path(dst).name == "test_demo_b.py":
            raise OSError("disk full (test)")
        return real(src, dst)

    with mock.patch.object(ts.os, "replace", failing):
        code, out = door(repo, mp, "--apply", capsys)
    assert code == 1 and "rolled back" in out, out
    assert snapshot(tests) == before          # the identical part stays; no other part, no common, the source intact, no temp file


def case_a_non_string_part_is_refused_not_a_traceback(tmp_path, capsys):
    data = make_map("test_demo", RUN_HOMES)
    data["parts"] = ["test_demo_a", 5]
    repo, tests, mp = world(tmp_path, SRC_RUN, data)
    (tests / "test_demo.py").unlink()                    # the "already split?" road is the one that read the parts first
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 2 and "`parts` must hold strings only" in out and "Traceback" not in out


def case_an_importer_writing_through_the_module_alias_is_refused(tmp_path, capsys):
    extra = {"test_user.py": "import test_demo as D\nD.TASK = 'x'\n",
             "test_user2.py": "from unittest import mock\nimport test_demo as D\nmock.patch.object(D, 'helper')\n"}
    refused_case(tmp_path, capsys, SRC_RUN, RUN_HOMES, ["test_user.py:2: writes `D.TASK` through the module",
                                                        "test_user2.py:3: `object(D, ...)` patches the module"], extra=extra, shim=True)


def case_no_runner_block_and_a_part_without_a_scenario_are_refused(tmp_path, capsys):
    refused_case(tmp_path, capsys, HEAD, RUN_HOMES, ["part `test_demo_a` holds no scenario", "part `test_demo_b` holds no scenario"])
    homes = dict(RUN_HOMES, b_one=("def", "a"), b_two=("def", "a"), never_run=("def", "a"))
    refused_case(tmp_path / "second", capsys, SRC_RUN, homes, ["part `test_demo_b` holds no scenario"])


def case_a_map_that_homes_nothing_in_common_writes_no_common(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_MINI, make_map("test_demo", MINI_HOMES))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    assert not (tests / "demo_common.py").exists() and "from demo_common import" not in (tests / "test_demo_a.py").read_text(encoding="utf-8")
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 1/1 ok ==="]
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 1/1 ok ==="]


def case_proof_c2_reads_the_run_list_without_the_classifier(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_FOR_IN_MAIN, make_map("test_demo", RUN_HOMES))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    lines, ok = tampered(plan, "test_demo_a.py", "        a_two,\n", "")
    assert not ok and any(l.startswith("(c2)") and "FAILED differing: ['a_two']" in l for l in lines)


# F1 and F2 of node N2 (the cut of test_no_move_seam): an import kept for its path effect, a closing in every part --------------

def pathfx_world(tmp_path, source=SRC_PATHFX, extra=None):
    repo, tests, mp = world(tmp_path, source, make_map("test_demo", MINI_HOMES),
                            extra=dict({"path_helper.py": PATH_HELPER}, **(extra or {})))
    (tests.parent / "libdir").mkdir()                       # beside the tests dir, so a snapshot of the tests dir stays files only
    (tests.parent / "libdir" / "libmod.py").write_text("VALUE = 1\n", encoding="utf-8")
    return repo, tests, mp


def case_import_proof_fails_when_a_part_lacks_the_import_that_makes_its_path(tmp_path, capsys):
    repo, tests, mp = pathfx_world(tmp_path)
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    kept = "import path_helper  # noqa: E402\ndel path_helper  " + ts.KEEP_MARK + "\n"
    assert kept in plan.files["test_demo_a.py"]
    lines, ok = tampered(plan, "test_demo_a.py", kept, "", imports=True)             # what the tool used to write
    g = [l for l in lines if l.startswith("(g)")]
    assert not ok and len(g) == 1 and "FAILED" in g[0] and "test_demo_a.py: exit 1" in g[0] and "ModuleNotFoundError" in g[0]
    assert "test_demo_b.py" not in g[0].split("FAILED")[1] and lines[-1] == "PROOF: FAILED"
    lines, ok = ts.prove(plan, {n: ts.to_bytes(plan, t) for n, t in plan.files.items()}, imports=True)
    assert ok and any(l.startswith("(g) import: 2 written file(s)") and l.endswith("-> ok") for l in lines)
    # a timeout is a failed proof naming the part
    with mock.patch.object(ts, "IMPORT_TIMEOUT", 0.001):
        lines, ok = ts.prove(plan, {n: ts.to_bytes(plan, t) for n, t in plan.files.items()}, imports=True)
    assert not ok and "test_demo_a.py: timed out after 0.001 s" in [l for l in lines if l.startswith("(g)")][0]
    # --apply: a failed import proof is raised after the temp files were written and before any rename; the tree is as it was
    before = snapshot(tests)
    with mock.patch.object(ts, "import_failures", lambda *a: ["test_demo_a.py: exit 1: boom"]):
        code, out = door(repo, mp, "--apply", capsys)
    assert code == 2 and "(g) import" in out and "boom" in out and "PROOF: FAILED" in out and snapshot(tests) == before


def case_path_effect_import_kept_as_import_and_del_and_the_parts_run_alone(tmp_path, capsys):
    repo, tests, mp = pathfx_world(tmp_path)
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out and "(g) import" in out, out
    a = (tests / "test_demo_a.py").read_text(encoding="utf-8")
    b = (tests / "test_demo_b.py").read_text(encoding="utf-8")
    assert "import path_helper  # noqa: E402\ndel path_helper  " + ts.KEEP_MARK in a            # a uses no name of it: kept for the path
    assert a.index("import path_helper") < a.index("import libmod")                              # in the old order: before what needs it
    assert "path_helper" in b and "del path_helper" not in b and "from path_helper import marker" in b
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 1/1 ok ==="]       # it found `libmod`
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 1/1 ok ==="]
    if importlib.util.find_spec("pyflakes"):                                                      # pyflakes ignores `# noqa`
        flakes = subprocess.run([sys.executable, "-m", "pyflakes", str(tests / "test_demo_a.py"), str(tests / "test_demo_b.py")],
                                capture_output=True, text=True)
        assert flakes.returncode == 0 and flakes.stdout == "", flakes.stdout
    assert "KEPT FOR ITS sys.path EFFECT: test_demo_a.py keeps" in out and "line 9: `from path_helper import marker" in out
    # the same tree read again is the same (nothing to do), and the kept lines are header, not a segment of the part
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "nothing to do" in out


def case_dropped_imports_are_listed_and_a_test_file_import_is_reported_not_kept(tmp_path, capsys):
    repo, tests, mp = pathfx_world(tmp_path, SRC_OTHER_TEST, extra={"test_other.py": "X = 1\n"})
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    drop = {l.split(" does not use ")[0]: l for l in out.splitlines() if l.startswith("DROPPED IMPORT:")}
    assert "line 2: `import json`" in drop["DROPPED IMPORT: test_demo_b.py"] and "line 10: `import libmod`" in drop[
        "DROPPED IMPORT: test_demo_b.py"]
    assert "line 11: `import test_other`" in drop["DROPPED IMPORT: test_demo_a.py"]          # dropped, listed, not kept
    assert "line 9:" not in drop["DROPPED IMPORT: test_demo_a.py"]                            # the path_helper line is kept instead
    assert any(l.startswith("REPORTED: test_demo.py:11: `import test_other") and "imports the test file `test_other`" in l
               for l in out.splitlines())
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    assert all("test_other" not in t for t in plan.files.values())                                      # no part keeps another test


def case_a_part_with_only_stdlib_imports_keeps_no_helper_import(tmp_path, capsys):
    repo, tests, mp = pathfx_world(tmp_path)
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    only_std = ts.header_text(plan, {"json"}, set(), part="x", keep_path=True)
    assert not any("path_helper" in l for l in only_std) and "import json" in only_std
    with_local = ts.header_text(plan, {"json", "libmod"}, set(), part="x", keep_path=True)
    assert "import path_helper  # noqa: E402" in with_local
    common_side = ts.header_text(plan, {"json", "libmod"}, set(), part="x")              # not a part: proof (g) is its net
    assert not any("path_helper" in l for l in common_side)
    assert plan.import_notes["x"]["dropped"] and plan.import_notes["x"]["kept_path"] == []


def case_the_closing_is_copied_into_every_part_and_each_part_runs_alone(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_GUARD_MAIN, make_map("test_demo", GUARD_HOMES, parts=PARTS_ABK))
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    for part in ("a", "b", "k"):
        text = (tests / f"test_demo_{part}.py").read_text(encoding="utf-8")
        assert text.count("harness.finish(") == 1 and f'harness.finish("test_demo_{part}")' in text
    k = (tests / "test_demo_k.py").read_text(encoding="utf-8")
    assert "def main" not in k and '__name__ == "__main__"' in k and k.rstrip().endswith('    harness.finish("test_demo_k")')   # the guard's end
    assert "CLOSING: test_demo_k.py got the old runner's closing (line %d: harness.finish(\"test_demo\"))" % (
        SRC_GUARD_MAIN.splitlines().index('    harness.finish("test_demo")') + 1) in out
    assert "CLOSING: test_demo_a.py" not in out and "CLOSING: test_demo_b.py" not in out       # their own `main` closes them
    assert tally(run_part(tests, "test_demo_k.py")[1]) == ["=== test_demo_k: 1/1 ok ==="]
    assert run_part(tests, "test_demo_k.py")[0] == 0
    assert tally(run_part(tests, "test_demo_a.py")[1]) == ["=== test_demo_a: 3/3 ok ==="]
    assert tally(run_part(tests, "test_demo_b.py")[1]) == ["=== test_demo_b: 2/2 ok ==="]


def case_a_runner_without_any_closing_is_refused_naming_file_line_and_the_door(tmp_path, capsys):
    refused_case(tmp_path, capsys, SRC_NO_CLOSING, GUARD_HOMES, [
        "test_demo.py:%d: part `test_demo_a` would have no closing call" % (SRC_NO_CLOSING.splitlines().index("def main():") + 1),
        "map key `closing`"], parts=PARTS_ABK)


def case_different_closings_are_refused_and_the_map_key_closing_decides(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_TWO_CLOSINGS, make_map("test_demo", GUARD_HOMES, parts=PARTS_ABK))
    before = snapshot(tests)
    code, out = door(repo, mp, "--dry-run", capsys)
    lines = SRC_TWO_CLOSINGS.splitlines()
    first, second = lines.index('    harness.finish("first")') + 1, lines.index('    harness.finish("second")') + 1
    assert code == 2 and "part `test_demo_k` takes its scenarios from blocks with different closings (lines %d, %d)" % (first, second) in out
    assert "map key `closing`" in out and "PROOF" not in out and snapshot(tests) == before
    data = json.loads(mp.read_text(encoding="utf-8"))
    mp.write_text(json.dumps(dict(data, closing=7)), encoding="utf-8")                  # a line that holds no finish: refused, lines named
    code, out = door(repo, mp, "--dry-run", capsys)
    assert code == 2 and "map key `closing` must be the line of a `finish" in out and f"{first}, {second}" in out and snapshot(tests) == before
    mp.write_text(json.dumps(dict(data, closing=second)), encoding="utf-8")
    code, out = door(repo, mp, "--apply", capsys)
    assert code == 0 and "PROOF: ok" in out, out
    k = (tests / "test_demo_k.py").read_text(encoding="utf-8")
    assert k.count("finish(") == 1 and 'harness.finish("second_k")' in k and "first" not in k
    assert tally(run_part(tests, "test_demo_k.py")[1]) == ["=== second_k: 1/1 ok ==="]


def case_proof_f_each_runner_holds_exactly_one_closing_call(tmp_path, capsys):
    repo, tests, mp = world(tmp_path, SRC_GUARD_MAIN, make_map("test_demo", GUARD_HOMES, parts=PARTS_ABK))
    plan = ts.build_plan(json.loads(mp.read_text(encoding="utf-8")), repo)
    files = {n: ts.to_bytes(plan, t) for n, t in plan.files.items()}
    lines, ok = ts.prove(plan, files)
    assert ok and "(f) closing: each of 3 part runner(s) holds exactly one closing call (finish) -> ok" in lines
    lines, ok = tampered(plan, "test_demo_k.py", '    harness.finish("test_demo_k")\n', "")                 # a part with no tally
    assert not ok and any(l.startswith("(f)") and "FAILED test_demo_k.py holds 0" in l for l in lines)
    lines, ok = tampered(plan, "test_demo_k.py", '    harness.finish("test_demo_k")', '    harness.finish("test_demo_k")\n    harness.finish("again")')
    assert not ok and any(l.startswith("(f)") and "FAILED test_demo_k.py holds 2" in l for l in lines)


CASES = [
    ("run_scenarios_two_list_split_in_two_parts", case_run_scenarios_two_list),
    ("main_with_direct_calls", case_main_with_direct_calls),
    ("module_level_loop_with_argv_filter", case_module_loop_with_argv_filter),
    ("shim_with_an_importer", case_shim_with_an_importer),
    ("no_shim_refused_because_an_importer_exists", case_no_shim_refused_because_an_importer_exists),
    ("name_used_by_two_parts_but_homed_in_a_part_refused", case_name_used_by_two_parts_but_homed_in_a_part),
    ("unplaced_module_level_statement_refused_then_placed", case_unplaced_statement_refused_then_placed_with_a_warning),
    ("unrecognised_runner_refused", case_unrecognised_runner_refused),
    ("proof_a_fails_when_a_part_drops_a_check", case_proof_a_fails_when_a_part_drops_a_check),
    ("proof_c_fails_on_a_duplicated_scenario", case_proof_c_fails_on_a_duplicated_scenario),
    ("proof_d_byte_identity_fails_on_a_tampered_body", case_proof_d_fails_on_a_tampered_body),
    ("rerun_after_apply_says_nothing_to_do", case_rerun_says_nothing_to_do),
    ("half_written_target_refused", case_a_half_written_target_is_refused),
    ("missing_or_unknown_row_refused_writes_nothing", case_a_row_is_missing_or_unknown_refuses_and_writes_nothing),
    ("dry_run_writes_nothing_and_prints_the_proof", case_dry_run_writes_nothing_and_prints_the_proof),
    ("crlf_kept_mixed_and_bom_refused", case_crlf_source_keeps_its_newlines_and_a_mixed_one_is_refused),
    ("draft_prints_names_runs_importers", case_draft_prints_every_name_its_runs_and_the_importers),
    ("door_exit_codes", case_the_door_exit_codes),
    ("T-B1 guard_of_direct_scenario_calls_is_cut", case_guard_of_direct_scenario_calls),
    ("T-B1 for_over_a_literal_tuple_inside_main_is_cut", case_for_over_a_literal_tuple_inside_main),
    ("T-B1 run_scenarios_empty_first_list_in_a_by_name_main_is_cut", case_run_scenarios_with_an_empty_first_list_in_a_by_name_main),
    ("T-B1 module_level_script_refused_by_draft_and_map", case_module_level_script_is_refused_by_the_draft_and_the_map),
    ("T-B2.1 module_level_check_homed_in_common_refused", case_module_level_check_homed_in_common_is_refused),
    ("T-B2.2 scenario_call_nested_in_a_by_name_consumer_refused", case_scenario_call_nested_in_a_by_name_consumer_is_refused),
    ("T-B2.3 statement_before_an_import_refused", case_statement_before_an_import_is_refused),
    ("T-B2.4 conditional_rebinding_across_homes_refused", case_conditional_rebinding_across_homes_is_refused),
    ("T-B2.5 late_import_that_shadows_a_def_refused", case_late_import_that_shadows_a_def_is_refused),
    ("T-B2.6 global_rebinding_of_a_common_name_read_by_a_part_refused", case_global_rebinding_of_a_common_name_read_by_a_part_is_refused),
    ("T-B2.7 mutating_statement_homed_apart_from_its_name_refused", case_mutating_statement_homed_apart_from_its_name_is_refused),
    ("T-F5 rollback_never_deletes_an_identical_target", case_rollback_never_deletes_an_identical_target),
    ("T-F6 non_string_part_refused_not_a_traceback", case_a_non_string_part_is_refused_not_a_traceback),
    ("T-F4 importer_writing_through_the_module_alias_refused", case_an_importer_writing_through_the_module_alias_is_refused),
    ("edge no_runner_block_and_a_part_without_a_scenario_refused", case_no_runner_block_and_a_part_without_a_scenario_are_refused),
    ("edge map_homing_nothing_in_common_writes_no_common", case_a_map_that_homes_nothing_in_common_writes_no_common),
    ("proof_c2_reads_the_run_list_without_the_classifier", case_proof_c2_reads_the_run_list_without_the_classifier),
    ("F1a import_proof_fails_when_a_part_lacks_the_import_that_makes_its_path", case_import_proof_fails_when_a_part_lacks_the_import_that_makes_its_path),
    ("F1b path_effect_import_kept_as_import_and_del_and_the_parts_run_alone", case_path_effect_import_kept_as_import_and_del_and_the_parts_run_alone),
    ("F1b dropped_imports_listed_and_a_test_file_import_reported_not_kept", case_dropped_imports_are_listed_and_a_test_file_import_is_reported_not_kept),
    ("F1 edge part_with_only_stdlib_imports_keeps_no_helper_import", case_a_part_with_only_stdlib_imports_keeps_no_helper_import),
    ("F2 closing_copied_into_every_part_and_each_part_runs_alone", case_the_closing_is_copied_into_every_part_and_each_part_runs_alone),
    ("F2 runner_without_any_closing_refused_with_file_line_and_door", case_a_runner_without_any_closing_is_refused_naming_file_line_and_the_door),
    ("F2 different_closings_refused_and_the_map_key_closing_decides", case_different_closings_are_refused_and_the_map_key_closing_decides),
    ("proof_f_each_runner_holds_exactly_one_closing_call", case_proof_f_each_runner_holds_exactly_one_closing_call),
]


@pytest.mark.parametrize("case", [c for _, c in CASES], ids=[i for i, _ in CASES])
def test_split_table(case, tmp_path, capsys):
    case(tmp_path, capsys)
