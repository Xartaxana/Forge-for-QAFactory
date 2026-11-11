"""Behaviour of tools/test_redundancy.py through its CLI door: `report` on hand-built coverage data, and `run` +
`report` over a tiny fake package. Both need coverage.py (the data file is its format) and skip without it.

Verification: python -m pytest tools/test_test_redundancy.py -q -p no:cacheprovider
"""
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

TOOL = pathlib.Path(__file__).resolve().parent / "test_redundancy.py"
CASES = {
    # a's lines are all shared (line 3 with b, lines 1-2 with the RED c): a is a candidate; b keeps line 4
    "shared-with-red-and-ok": dict(
        ctx={"a.py": {1, 2, 3}, "b.py": {3, 4}, "c.py": {1, 2}},
        runs={"a.py": (0, 5.0), "b.py": (0, 1.0), "c.py": (1, 2.0)},
        status={"a.py": "ok", "b.py": "ok", "c.py": "red"}, unique={"a.py": 0, "b.py": 1, "c.py": 0},
        candidates=["a.py"], greedy=["a.py", "b.py"], no_context=0),
    # a line under the empty context is never unique to a file, and the empty context is no file row
    "no-context-line": dict(
        ctx={"a.py": {1, 2}, "": {1}},
        runs={"a.py": (0, 1.0)},
        status={"a.py": "ok"}, unique={"a.py": 1}, candidates=[], greedy=["a.py"], no_context=1),
    # zero lines is not-measured, a timeout is red even with exit 0, a tie goes to the faster file
    "not-measured-timeout-tie": dict(
        ctx={"fast.py": {1}, "slow.py": {2}, "t.py": {3}},
        runs={"fast.py": (0, 1.0), "slow.py": (0, 9.0), "z.py": (0, 1.0), "t.py": (0, 900.0, True)},
        status={"fast.py": "ok", "slow.py": "ok", "z.py": "not-measured", "t.py": "red"},
        unique={"fast.py": 1, "slow.py": 1, "z.py": 0, "t.py": 1}, candidates=[], greedy=["fast.py", "slow.py"],
        no_context=0),
}


def report(tmp_path, data_path, runs_path):
    return subprocess.run([sys.executable, "-B", str(TOOL), "report", "--data", str(data_path), "--runs", str(runs_path),
                           "--out", str(tmp_path / "rep")], capture_output=True, text=True)


@pytest.mark.parametrize("name", sorted(CASES))
def test_report_counts_covered_and_unique_lines_per_test_file(tmp_path, name):
    coverage_data = pytest.importorskip("coverage.sqldata")
    case = CASES[name]
    data = coverage_data.CoverageData(basename=str(tmp_path / ".coverage"))
    for ctx, lines in case["ctx"].items():
        data.set_context(ctx)
        data.add_lines({"/pkg/scripts/p.py": sorted(lines)})
    data.write()
    runs = [{"file": f, "exit": v[0], "seconds": v[1], "timed_out": len(v) > 2 and v[2]} for f, v in case["runs"].items()]
    (tmp_path / "runs.json").write_text(json.dumps(runs), encoding="utf-8")
    done = report(tmp_path, tmp_path / ".coverage", tmp_path / "runs.json")
    assert done.returncode == 0, done.stderr
    rep = json.loads((tmp_path / "rep" / "test-redundancy.json").read_text(encoding="utf-8"))
    rows = {f["file"]: f for f in rep["files"]}
    assert {k: r["status"] for k, r in rows.items()} == case["status"]
    assert {k: r["unique"] for k, r in rows.items()} == case["unique"]
    assert [g["file"] for g in rep["greedy"]] == case["greedy"]
    assert rep["totals"]["lines_under_no_context"] == case["no_context"]
    md = (tmp_path / "rep" / "test-redundancy.md").read_text(encoding="utf-8")
    table_a = md.split("## A.")[1].split("## B.")[0]
    assert [f for f in rows if f"| {f} |" in table_a] == case["candidates"]


STUB_SELFTEST = ("import json, pathlib\n"
                 "def test_layers(path=None):\n"
                 "    try:\n"
                 "        raw = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))\n"
                 "    except FileNotFoundError:\n"
                 "        return {'keep': {}, 'absent': True}\n"
                 "    return {'keep': dict(raw.get('keep', {})), 'absent': False}\n")


def keep_package(tmp_path, keep, layers=True):
    """A tiny package: p1.py, p2.py, tests a/b/c; selftest.py is a stub with the real test_layers() signature."""
    pkg = tmp_path / "pkg"
    (pkg / "scripts" / "tests").mkdir(parents=True)
    (pkg / "scripts" / "selftest.py").write_text(STUB_SELFTEST, encoding="utf-8")
    (pkg / "scripts" / "p1.py").write_text("def f():\n    return 1\n\n\ndef g():\n    return 2\n", encoding="utf-8")
    (pkg / "scripts" / "p2.py").write_text("def h():\n    return 3\n", encoding="utf-8")
    head = "import pathlib, sys\nsys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))\n"
    for name, body in {"test_a": "import p1\np1.f()\n", "test_b": "import p1\np1.g()\n", "test_c": "import p2\np2.h()\n"}.items():
        (pkg / "scripts" / "tests" / f"{name}.py").write_text(head + body, encoding="utf-8")
    if layers:
        (pkg / "scripts" / "tests" / "test-layers.json").write_text(json.dumps({"keep": {k: {} for k in keep}}), encoding="utf-8")
    return pkg


def run_tool(pkg, out, *extra, env=None):
    return subprocess.run([sys.executable, "-B", str(TOOL), "run", "--package", str(pkg), "--out", str(out), "--jobs", "2",
                           *extra], capture_output=True, text=True, env=env)


def test_keep_only_runs_the_keep_files_and_the_report_carries_both_product_lines_lines(tmp_path):
    pytest.importorskip("coverage")
    pkg = keep_package(tmp_path, ["test_a.py", "test_c.py", "test_gone.py"])
    hook = tmp_path / "hook"                       # a sitecustomize stands in for the CI job's .pth file
    hook.mkdir()
    (hook / "sitecustomize.py").write_text("import coverage\ncoverage.process_startup()\n", encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": str(hook)}
    out = tmp_path / "out"
    done = run_tool(pkg, out, "--keep-only", env=env)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "test_gone.py" in done.stdout and "absent on disk" in done.stdout       # the missing row: named, run goes on
    runs = json.loads((out / "runs.json").read_text(encoding="utf-8"))
    assert [r["file"] for r in runs] == ["test_a.py", "test_c.py"]               # test_b is not a keep row
    done = report(tmp_path, out / "data" / ".coverage", out / "runs.json")
    assert done.returncode == 0, done.stderr
    md = (tmp_path / "rep" / "test-redundancy.md").read_text(encoding="utf-8")
    covered = re.search(r"product lines covered:\s*(\d+)", md)
    total = re.search(r"product lines total:\s*(\d+)", md)
    assert covered and total and int(covered.group(1)) <= int(total.group(1))


def test_report_without_readable_sources_says_total_unknown_not_a_number(tmp_path):
    coverage_data = pytest.importorskip("coverage.sqldata")
    data = coverage_data.CoverageData(basename=str(tmp_path / ".coverage"))
    data.set_context("a.py")
    data.add_lines({"/nowhere/scripts/p.py": [1, 2]})
    data.write()
    (tmp_path / "runs.json").write_text(json.dumps([{"file": "a.py", "exit": 0, "seconds": 1.0, "timed_out": False}]), encoding="utf-8")
    assert report(tmp_path, tmp_path / ".coverage", tmp_path / "runs.json").returncode == 0
    md = (tmp_path / "rep" / "test-redundancy.md").read_text(encoding="utf-8")
    assert re.search(r"product lines covered:\s*2", md) and re.search(r"product lines total:\s*unknown", md)


@pytest.mark.parametrize("keep,layers", [([], True), (["test_a.py"], False), (["test_gone.py"], True)],
                         ids=["empty-keep", "no-layers-file", "keep-names-only-absent-files"])
def test_keep_only_refuses_with_the_door_and_measures_nothing(tmp_path, keep, layers):
    pkg = keep_package(tmp_path, keep, layers)
    out = tmp_path / "out"
    done = run_tool(pkg, out, "--keep-only")
    assert done.returncode == 1
    assert "run TD-15.2 first" in done.stderr
    assert not (out / "runs.json").exists() and not (out / "data").exists()


def test_keep_only_with_only_is_refused_naming_both_flags(tmp_path):
    pkg = keep_package(tmp_path, ["test_a.py"])
    done = run_tool(pkg, tmp_path / "out", "--keep-only", "--only", "test_a.py")
    assert done.returncode == 2
    assert "--keep-only" in done.stderr and "--only" in done.stderr


def test_run_then_report_on_a_tiny_package(tmp_path):
    pytest.importorskip("coverage")
    pkg = tmp_path / "pkg"
    (pkg / "scripts" / "tests").mkdir(parents=True)
    (pkg / "scripts" / "p1.py").write_text("def f():\n    return 1\n\n\ndef g():\n    return 2\n", encoding="utf-8")
    (pkg / "scripts" / "p2.py").write_text("def h():\n    return 3\n", encoding="utf-8")
    head = "import pathlib, sys\nsys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))\n"
    bodies = {"test_a_overlap": "import p1\np1.f()\n", "test_b_wide": "import p1\np1.f()\np1.g()\n",
              "test_c_nothing": "print('no import')\n"}
    for name, body in bodies.items():
        (pkg / "scripts" / "tests" / f"{name}.py").write_text(head + body, encoding="utf-8")
    hook = tmp_path / "hook"                       # a sitecustomize stands in for the CI job's .pth file
    hook.mkdir()
    (hook / "sitecustomize.py").write_text("import coverage\ncoverage.process_startup()\n", encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": str(hook)}
    out = tmp_path / "out"
    done = subprocess.run([sys.executable, "-B", str(TOOL), "run", "--package", str(pkg), "--out", str(out),
                           "--jobs", "2"], capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stdout + done.stderr
    runs = json.loads((out / "runs.json").read_text(encoding="utf-8"))
    assert [(r["file"], r["exit"], r["timed_out"]) for r in runs] == [(f"{n}.py", 0, False) for n in sorted(bodies)]
    done = report(tmp_path, out / "data" / ".coverage", out / "runs.json")
    assert done.returncode == 0, done.stderr
    rows = {f["file"]: f for f in json.loads((tmp_path / "rep" / "test-redundancy.json").read_text(encoding="utf-8"))["files"]}
    assert rows["test_a_overlap.py"]["status"] == "ok" and rows["test_a_overlap.py"]["unique"] == 0
    assert rows["test_b_wide.py"]["unique"] >= 1
    assert rows["test_c_nothing.py"]["status"] == "not-measured"
