"""Shared by the parts test_probe_by_code_languages_{plan,cli,ts_playwright}.py (split from test_probe_by_code_languages.py,
TD-11c N9): the stand-in runner `LANG_RUN_SUITE`, the language table `LANGS`, the project builder `lang_project`, the CLI caller
`lrun` and the readers of what a probe leaves on disk. No scenario lives here (the one helper with checks is `refused`) and nothing
runs on import. `lrun` runs the CLI in this process by default (`in_process_script`) and as a child process with `real=True`.
"""
import contextlib
import io
import runpy
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json  # noqa: E402
import os  # noqa: E402
from harness import FIXTURES, SCRIPTS, check_eq, check_in, run_script, temp_dir  # noqa: E402
import acceptance  # noqa: E402
import hooklib  # noqa: E402
import probe_entries as PE  # noqa: E402
import probe_by_code as PBC  # noqa: E402
from test_probe_by_code import (DISPATCH, OBLIGATION_REFS, PROVENANCE, TASK, env_for, model_entries, seed_author_job, write_json)  # noqa: E402
from test_probe_by_code import tree_state as _tree_state  # noqa: E402


PY = sys.executable


FIX = FIXTURES / "probe-languages"


OLD_NS = 1_600_000_000 * 10 ** 9  # 2020: far from "now", so a mtime rule shows


LANG_RUN_SUITE = r'''
"""A stand-in for `run_suite.py --request FILE` for a test that is not Python."""
import hashlib
import json
import os
import signal
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

request = json.loads(Path(sys.argv[sys.argv.index("--request") + 1]).read_text(encoding="utf-8"))
cfg = json.loads(os.environ["LANG_STUB"])
mode = cfg.get("mode", "normal")
if os.environ.get("PROBE_STUB_LOG"):
    with open(os.environ["PROBE_STUB_LOG"], "a", encoding="utf-8") as log:
        log.write(sys.argv[-1] + "\n")
if mode == "kill_holding_lock":
    os.kill(os.getppid(), signal.SIGTERM)  # the role's shell call is killed: no `finally` ever runs
    sys.exit(3)
if request.get("purpose") != "red_probe":
    print(json.dumps({"status": "stub_refused", "error": "purpose must be red_probe"}))
    sys.exit(2)
cwd = Path(request["command"]["cwd"]).resolve()
project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or cwd).resolve()
test_path = (project / cfg["file"]).resolve()
raw = test_path.read_bytes()
lines = raw.decode("utf-8-sig").splitlines()
hit = cfg.get("hit", cfg["after"]) in lines[cfg["line"] - 1]   # t-1968 N1: a marked statement is not `after` byte for byte
# t-2064 P4b: a walk runs EVERY check of the body, one inverted at a time; `also` lists the other checks of the fixture ([line, after]): the
# row fails when any of them holds its inverted statement, so each check of the plan meets the failure the first one always met
hit = hit or any(n <= len(lines) and a in lines[n - 1] for n, a in cfg.get("also", []))
status = "failed" if hit else "passed"
if mode == "pass_anyway":
    status = "passed"
if mode == "error_row" and hit:
    status = "error"
if mode == "skipped_row":
    status = "skipped"
site_line = cfg["line"] + (3 if mode == "wrong_line" else 0)
stack = cfg["lib"] + cfg["stack"] if mode == "lib_frames_first" else ([] if mode == "no_frames" else cfg["stack"])
stack = [s.replace("{path}", test_path.as_posix()).replace("{line}", str(site_line)) for s in stack]
message = cfg["drift"] if mode == "drifted_message" else cfg["message"]
# t-2064 N3b: the runner prints the token the way the mutated check would (the marker is joined at run time, so it is in the
# message and in no echo of the source): read from the bytes this stub was handed. `drifted_message` and `wrong_line` print none -
# the failure text a library wrote, which only the code critic judges
import re
found = re.search(r"qa-probe[\"',\s]+([0-9a-f]{12})", raw.decode("utf-8-sig"))
if found and mode not in ("drifted_message", "wrong_line"):
    message = "qa-probe-" + found.group(1) + " " + message
ids = [cfg["report_id"]]
if mode == "no_row":
    ids = ["Some.Other.Test"]
if mode == "two_rows":
    ids = ids * 2


def trx_row(test_id):
    outcome = {"passed": "Passed", "failed": "Failed", "error": "Error", "skipped": "NotExecuted"}[status]
    info = ""
    if status in ("failed", "error", "skipped"):
        info = ("<Output><ErrorInfo><Message>" + escape(message) + "</Message><StackTrace>" + escape("\n".join(stack))
                + "</StackTrace></ErrorInfo></Output>")
    return f'<UnitTestResult testName={quoteattr(test_id)} outcome="{outcome}" testId="g-1">{info}</UnitTestResult>'


def junit_row(test_id):
    classname, _, name = test_id.partition("::")
    body = ""
    if status == "failed":
        body = (f"<failure message={quoteattr(message)} type={quoteattr(cfg.get('type', 'Error'))}>"
                + escape(cfg.get("text_prefix", "").replace("{message}", message) + "\n".join(stack)) + "</failure>")
    elif status == "error":
        body = f"<error message={quoteattr(message)} type=\"RuntimeError\">{escape(chr(10).join(stack))}</error>"
    elif status == "skipped":
        body = "<skipped message=\"not run\"/>"
    return f"<testcase classname={quoteattr(classname)} name={quoteattr(name)}>{body}</testcase>"


reporter = cfg["reporter"]
if reporter == "trx":
    xml = ('<TestRun xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010"><Results>'
           + "".join(trx_row(i) for i in ids) + "</Results><TestDefinitions><UnitTest id=\"g-1\"><TestMethod "
           + f'className={quoteattr(cfg["report_id"].rpartition(".")[0])} name={quoteattr(cfg["report_id"].rpartition(".")[2])}/>'
           + "</UnitTest></TestDefinitions></TestRun>")
else:
    xml = "<testsuites><testsuite name=\"s\">" + "".join(junit_row(i) for i in ids) + "</testsuite></testsuites>"
job = hashlib.sha256(request["idempotency_key"].encode()).hexdigest()[:20]
task_root = project / "qa-factory" / "artifacts" / request["task"]
run_dir = task_root / "evidence" / "runs" / job
run_dir.mkdir(parents=True, exist_ok=True)
report = run_dir / ("report.trx" if reporter == "trx" else "report.junit.xml")
report.write_text(xml, encoding="utf-8")
label = f"red_probe-{job}"
summary_path = run_dir / f"{label}.json"
summary = {"task": request["task"], "label": label, "exit_code": 0 if status == "passed" else 1,
           "execution_status": status, "purpose": "red_probe", "reporter": reporter,
           "summary_path": summary_path.relative_to(project).as_posix(),
           "report_evidence": {"path": report.relative_to(task_root).as_posix(),
                               "sha256": hashlib.sha256(report.read_bytes()).hexdigest()},
           "stub_seen_sha256": hashlib.sha256(raw).hexdigest(), "stub_seen_prefix": raw[:3].hex(), "stub_seen_text": raw.decode("utf-8-sig"),
           "stub_seen_crlf": raw.count(b"\r\n"), "stub_hit": hit,
           "stub_selected": request.get("selected_instance_ids"),
           "stub_argv": request["command"].get("argv"), "stub_selector_args": request["command"].get("selector_args")}
summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8")
print(json.dumps(summary))
sys.exit(summary["exit_code"])
'''


LANGS = {
    "csharp": dict(
        marker=False,     # xunit `Assert.Equal` takes no message: no token, so the critic judges (N3b)
        fixture="CalcTests.cs", file="tests/CalcTests.cs", root_test="tests", iid="Adds", test="CalcTests.Adds",
        selector="CalcTests.Adds", selector_args=["--filter", "FullyQualifiedName~CalcTests.Adds"],
        report_id="Acme.Tests.CalcTests.Adds", reporter="trx",
        argv=["dotnet", "test", "--logger", "trx;LogFileName={report_path}"],
        first="            Assert.Equal(4, Calc.Add(2, 2));", after="Assert.NotEqual(4, Calc.Add(2, 2));",
        # t-2064 P4b: the fixture's body has a SECOND check, one line below (the walk runs it): (lines below the first, its inverted text, takes a
        # marker). `Assert.True(cond)` takes a message in xunit, so the factory's token rides on it where `Assert.Equal` of the first takes none
        also=[(1, "Assert.False(note.Length > 0", True)],
        message="Assert.NotEqual() Failure: Values are equal\nExpected: Not 4\nActual:   4",
        drift="Assert.NotEqual() has failed: the values were equal", type="Xunit.Sdk.NotEqualException",
        text_prefix="",
        stack=["   at Acme.Tests.CalcTests.Adds() in {path}:line {line}"],
        lib=["   at Xunit.Assert.NotEqual[T](T expected, T actual) in /_/src/xunit.assert/Asserts/EqualityAsserts.cs:line 372",
             "   at System.RuntimeMethodHandle.InvokeMethod(Object target, Signature sig)"]),
    "java": dict(
        marker=True,      # JUnit `assertEquals(.., message)` takes one (M-J5): the stub reads the token from the mutated bytes
        fixture="CalcTest.java", file="src/test/java/com/acme/CalcTest.java", root_test="src/test", iid="adds",
        test="CalcTest.adds", selector="CalcTest#adds", selector_args=["-Dtest=CalcTest#adds"],
        report_id="com.acme.CalcTest::adds()", reporter="junit-xml",
        argv=["mvn", "-q", "test", "-Dsurefire.reportsFile={report_path}"],
        first="        assertEquals(4, Calc.add(2, 2));", after="assertNotEquals(4, Calc.add(2, 2));",
        hit="assertNotEquals(4, Calc.add(2, 2)",    # the real run carries the factory's message marker after the last argument (N1)
        message="expected: not equal but was: <4>", drift="the values should have been different",
        type="org.opentest4j.AssertionFailedError", text_prefix="org.opentest4j.AssertionFailedError: {message}\n",
        stack=["\tat com.acme.CalcTest.adds(CalcTest.java:{line})",
               "\tat java.base/java.lang.reflect.Method.invoke(Method.java:568)"],
        lib=["\tat org.junit.jupiter.api.AssertionUtils.fail(AssertionUtils.java:55)",
             "\tat org.junit.jupiter.api.AssertNotEquals.failEqual(AssertNotEquals.java:179)"]),
    "typescript": dict(
        marker=False,     # jest `expect(..).toBe` outside @playwright/test takes none (M-TS2 has a `source` condition)
        fixture="sum.test.ts", file="src/sum.test.ts", root_test="src", iid="adds", test="adds",
        selector="adds", selector_args=["src/sum.test.ts", "-t", "adds"],
        report_id="calc adds::calc adds", reporter="junit-xml",
        argv=["npx", "jest", "--ci", "--outputFile={report_path}"],
        first="    expect(sum(1, 2)).toBe(3);", after="expect(sum(1, 2)).not.toBe(3);",
        message="expect(received).not.toBe(expected) // Object.is equality\n\nExpected: not 3\nReceived: 3",
        drift="the received value was 3, which must not be", type="Error", text_prefix="Error: {message}\n\n",
        stack=["      at Object.<anonymous> ({path}:{line}:20)",
               "      at Promise.then.completed (/x/node_modules/jest-circus/build/utils.js:298:28)",
               "      at new Promise (<anonymous>)"],
        lib=["      at Object.toBe (/x/node_modules/expect/build/index.js:1:1)",
             "      at node:internal/process/task_queues:95:5"]),
}


def first_line(lang: str, data: bytes = None) -> int:
    """The 1-based line of the fixture's first assertion (found, not typed: the fixture may be edited)."""
    spec = LANGS[lang]
    text = (data if data is not None else (FIX / spec["fixture"]).read_bytes()).decode("utf-8-sig")
    return text.splitlines().index(spec["first"]) + 1


def stub_cfg(lang: str, mode: str = "normal", **over) -> dict:
    spec = LANGS[lang]
    cfg = {key: spec[key] for key in ("file", "after", "message", "drift", "type", "text_prefix", "stack", "lib",
                                      "reporter", "report_id", "hit") if key in spec}
    cfg.update(mode=mode, line=first_line(lang))
    cfg["also"] = [[cfg["line"] + offset, text] for offset, text, _marker in spec.get("also", [])]
    cfg.update(over)
    return cfg


def check_lines(lang: str) -> list:
    """The 1-based lines of the fixture body's checks, in the order the plan walks them (t-2064 P4b: every check, not the first only)."""
    first = first_line(lang)
    return [first] + [first + offset for offset, _text, _marker in LANGS[lang].get("also", [])]


def check_markers(lang: str) -> list:
    """Per check of `check_lines`: does its form take the factory's message marker (the fixture's, never read back from a record)?"""
    return [LANGS[lang]["marker"]] + [marker for _offset, _text, marker in LANGS[lang].get("also", [])]


def lang_project(lang: str, *, data: bytes = None, argv=None, verified: bool = True, extra_entries=(),
                 protected=None, files: dict = None, entry_extra: dict = None, mtime_ns=None) -> Path:
    """A project whose manifest names ONE test of `lang` (instance `spec["iid"]`, case TC-100), bound to the raw
    sha256 of its file as manifest_from_tests.py binds every row, with the author's green run block."""
    spec = LANGS[lang]
    root = temp_dir("qa-probe-lang-")
    target = root / spec["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data if data is not None else (FIX / spec["fixture"]).read_bytes())
    if mtime_ns is not None:
        os.utime(target, ns=(mtime_ns, mtime_ns))
    for name, content in (files or {}).items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(content)
    probe_script = root.parent / (root.name + "-runtime-probe.py")
    probe_script.write_text("import json\nprint(json.dumps(" + repr(PROVENANCE) + "))\n", encoding="utf-8")
    config = {
        "tests_root": spec["root_test"], "app_root": ".",
        "profiles": [{"profile_id": "unit", "selected": True, "roots": {"test": spec["root_test"]},
                      "commands": {"one_test": {"argv": list(argv or spec["argv"]), "cwd": "."}},
                      "reporter": {"kind": spec["reporter"]}, "selectors": {"verified": verified}}],
        "execution": {"runtime_probes": {"unit": {"argv": [PY, str(probe_script)], "cwd": ".", "timeout_s": 20}}}}
    if protected is not None:
        config["protected_app_paths"] = protected
    write_json(root / "qa-factory" / "config.json", config)
    task_root = root / "qa-factory" / "artifacts" / TASK
    write_json(task_root / "pipeline.json", {"stages": {"S5": {"status": "running"}},
                                             "first_test_run_at": "2026-09-24T09:00:00+00:00"})
    ids = ["TC-100"] + [e["case"] for e in extra_entries]
    write_json(task_root / "state" / "controller.json", {
        "schema_version": "2", "revision": "1", "source_revision": "source-1",
        "dispatches": {DISPATCH: {"id": DISPATCH, "stage": "S5", "role": "qa-code-critic", "status": "running",
                                  "scope": ids, "budget": {"requests": 50}}}})
    bound = {"test_content_sha": PBC.sha256(target.read_bytes())}
    entry = {"case": "TC-100", "covers": ["TC-100"], "file": spec["file"], "test": spec["test"],
             "instance_id": spec["iid"], "selector": spec["selector"], "selector_args": list(spec["selector_args"]),
             "report_test_id": spec["report_id"], "case_version_links": [{"case_id": "TC-100", "version": "cv_1"}],
             "obligation_refs": OBLIGATION_REFS, "trace_binding": bound, "obligation_ids": ["OB-ADD-1"],
             "defect_location": "calc:2", "assertion_id": "add_returns_sum"}
    entry.update(entry_extra or {})
    write_json(task_root / "work" / "automation-manifest.json", {"tests": [entry]})
    seed_author_job(root)  # the author's run of THIS test; rows that would make that refuse come after it
    write_json(task_root / "work" / "automation-manifest.json", {"tests": [entry] + list(extra_entries)})
    block = {"schema_version": 2, "dispatch_id": "S5-qa-automator-1", "purpose": "initial",
             "results": [{"instance_id": spec["iid"], "status": "passed",
                          "source_fingerprint": {"source_sha": "source-1", "test_content_sha": "author-tcs-1"}}],
             "runtime_provenance": {"observed_runtime_identity": "build-1", "environment_id": "env-1"}}
    write_json(task_root / "work" / "run-blocks" / "20260924T090000000000Z-author1.json", block)
    return root


def write_entries(root: Path, keys: list) -> None:
    """The window's model file with one `invert` entry per key, written only when its bytes differ (a refusal test takes its tree
    snapshot AFTER calling this, and a rewrite of the same bytes would move the mtime the snapshot compares)."""
    path = root / "qa-factory" / "artifacts" / TASK / "work" / "probe-models" / f"{DISPATCH}.json"
    wanted = json.dumps({"models": [{"check": key, "invert": PE.DEFAULT_REASON} for key in keys]})
    if not path.is_file() or path.read_text(encoding="utf-8") != wanted:
        PE.write_invert_entries(root / "qa-factory" / "artifacts" / TASK, DISPATCH, keys=list(keys))


@contextlib.contextmanager
def clean_state(env: dict):
    """The state of this test process a CLI call could change - `os.environ` (replaced by `env`), `sys.argv`, `sys.path`,
    `sys.dont_write_bytecode` - taken before and put back after, so every in-process call starts as a child process would: from the
    same state. The project root `hooklib` caches per process is pinned to the call's `CLAUDE_PROJECT_DIR` (`pin_project_root`, the
    door the selftests use) and given back by `selftest_root_restored`. The script itself runs in a fresh namespace per call
    (`runpy`), so its own globals never carry over; the library modules it imports stay cached, as they are for any test. The
    working directory is NOT touched (the project is named by `CLAUDE_PROJECT_DIR`, and the launcher of a stand-in runner runs
    it with an explicit `cwd`)."""
    saved = (dict(os.environ), list(sys.argv), list(sys.path), sys.dont_write_bytecode)
    os.environ.clear()
    os.environ.update(env)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True
    try:
        with hooklib.selftest_root_restored():
            hooklib.pin_project_root(env["CLAUDE_PROJECT_DIR"])
            yield
    finally:
        os.environ.clear()
        os.environ.update(saved[0])
        sys.argv[:] = saved[1]
        sys.path[:] = saved[2]
        sys.dont_write_bytecode = saved[3]


def in_process_script(script: Path, argv: list, env: dict) -> subprocess.CompletedProcess:
    """`python -B <script> <argv>` run IN THIS PROCESS (`runpy`, `__main__`: a fresh namespace per call, so no module global of the script
    survives from one call to the next), under `env`: a CompletedProcess of its exit code, stdout and stderr. For a case that does not
    check the script as a process (the interpreter's exit, a signal); the cases that do pass `real=True` to `lrun`."""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with clean_state(env), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        sys.argv = [str(script), *[str(a) for a in argv]]
        try:
            runpy.run_path(str(script), run_name="__main__")
        except SystemExit as stop:
            code = stop.code
    if code is None:
        code = 0
    elif not isinstance(code, int):
        err.write(f"{code}\n")
        code = 1
    return subprocess.CompletedProcess([str(script), *[str(a) for a in argv]], code, out.getvalue(), err.getvalue())


def in_process_model_entries(root: Path, stub, test: str, instance: str) -> None:
    """`model_entries` of test_probe_by_code without the child process: the same `--plan` read (`PE.plan_keys` in this process, under the
    environment the child would get) and the same `invert` entry per key; a refusal of `--plan` writes nothing."""
    with clean_state(env_for(root, stub)):
        try:
            keys = PE.plan_keys(["--task", TASK, "--instance", instance, "--test", test])
        except RuntimeError:
            return
    if keys:
        PE.write_invert_entries(root / "qa-factory" / "artifacts" / TASK, DISPATCH, keys=keys)


def lrun(root: Path, stub: Path, node: str, instance: str, cfg: dict, *args, real: bool = False, **env):
    """The CLI, as a role runs it: (process, parsed JSON of stdout or {}). `real=True` runs it as a child process (the call whose exit
    code and stdout are the contract under test); the default runs the same script in this process (`in_process_script`; its
    stand-in runner is still a child process, as the tool launches it). t-2064 P4b: a call with no `--at` and no `--oracle` walks every
    check and needs a model entry per check, so the window's model file is written first (`model_entries`). `--at <line>` is a plan of the
    one selected row on the same road and needs the entry of THAT key (`<file of the node>:<line>`, written by hand: `--plan` need not list
    it, a line of an ambiguous declaration is not on the plan); `--oracle` needs the keys of the helper's checks, which the section that
    passes it writes (none here)."""
    if "--oracle" not in args:
        if "--at" in args:
            at = str(args[args.index("--at") + 1])
            write_entries(root, [at if ":" in at else f"{node.split('::')[0]}:{at}"])
        elif real:
            model_entries(root, stub, node, instance)
        else:
            in_process_model_entries(root, stub, node, instance)
    argv = ["--task", TASK, "--dispatch", DISPATCH, "--test", node, "--instance", instance, "--json", *args]
    call_env = env_for(root, stub, LANG_STUB=json.dumps(cfg), PROBE_SCRIPTS_DIR=str(SCRIPTS), **env)
    if real:
        proc = run_script("probe_by_code.py", *argv, cwd=root, env=call_env)
    else:
        proc = in_process_script(SCRIPTS / "probe_by_code.py", argv, call_env)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    try:
        payload = json.loads("\n".join(lines)) if lines and lines[0].startswith("{") else {}
    except ValueError:
        payload = {}
    return proc, payload


def tree_state(root: Path) -> dict:
    """Every file under the project with its bytes' sha256 and mtime, but for the lock files of
    `qa-factory/state/probe-copies/`: a lock is taken BEFORE the test is first read and is never deleted (the
    `event_store.lock` convention, B-373 a), so a refusal that comes after it leaves an empty lock file - not a
    change of anything the author or the story owns, which is what a refusal must leave alone."""
    return {k: v for k, v in _tree_state(root).items()
            if not (k.startswith("qa-factory/state/probe-copies/") and k.endswith(".lock")) and not _tool_refusal_file(root, k)}


def tree_state_with_entries(root: Path, stub: Path, node: str, instance: str) -> dict:
    """`tree_state` taken AFTER the window's model file is written (TR2-14): `lrun` writes that file before the call, which is world and not
    the probe's work (same bytes, `model_entries`), so a snapshot taken before it would report the file as a change the refusal made."""
    model_entries(root, stub, node, instance)
    return tree_state(root)


def refusal_record_of(root: Path, instance: str) -> tuple:
    """(`refused`, `verdict`) of the instance's record on disk, or (None, None): the positive half of "the tree is unchanged" for a refusal of
    the TOOL, which `tree_state` leaves out (TR2-14)."""
    path = task_of(root) / "work" / "probes" / f"{instance}.json"
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return (None, None)
    return (body.get("refused"), body.get("verdict"))


def _tool_refusal_file(root: Path, rel: str) -> bool:
    """Is `rel` the record `refused: tool` that a refusal of the TOOL leaves (EP1-36)? It is the one file a refusal may add; a
    test that says "the tree is unchanged" means the author's file, the copies and the story's other files. Those records have
    their own tests (`tool_refusal_record`)."""
    if "/work/probes/" not in rel or not rel.endswith(".json"):
        return False
    try:
        return json.loads((root / rel).read_text(encoding="utf-8")).get("refused") == "tool"
    except (OSError, ValueError, AttributeError):
        return False


def task_of(root: Path) -> Path:
    return root / "qa-factory" / "artifacts" / TASK


def node_of(lang: str) -> str:
    return f"{LANGS[lang]['file']}::{LANGS[lang]['test']}"


def refused(label: str, proc, payload, *needles: str) -> str:
    check_eq(f"{label}: exit 2, refused", (proc.returncode, payload.get("status")), (2, "refused"))
    text = payload.get("error", "")
    for needle in needles:
        check_in(f"{label}: says {needle!r}", needle, text)
    check_in(f"{label}: and that nothing was changed", "Nothing was changed", text)
    return text


def copies_left(root: Path) -> list:
    folder = root / "qa-factory" / "state" / "probe-copies"
    return sorted(p.name for p in folder.glob("*") if p.suffix != ".lock") if folder.is_dir() else []


def window_gaps(root: Path, record: dict, iid: str) -> list:
    """The record's `window_probe` dropped into a schema-2 window instance: the gaps `validate_window` finds."""
    item = {"schema_version": 2, "instance_id": iid, "input_hash": record["input_hash"], "outcome": "passed",
            "execution_fingerprint": "fp-1", "review": {"verdict": "approved", "input_hash": record["input_hash"]},
            "obligation_ids": record["obligation_ids"], "obligation_refs": OBLIGATION_REFS,
            "obligation_hash": record["obligation_hash"], "assertion_id": record["assertion_id"],
            "defect_location": record["defect_location"], "change_disposition": "new_or_changed",
            "change_basis_ref": "manifest:TC-100", "probe": record["window_probe"], "evidence_refs": record["evidence_refs"]}
    window = {"schema_version": 2, "input_hash": "window-1", "required_quality_checks": [], "quality_receipts": [],
              "instances": [item]}
    return acceptance.validate_window(window, task_of(root))


WRAP = {
    "csharp": ("using Xunit;\n\nnamespace Acme\n{\n    public class T\n    {\n        [Fact]\n        public void Adds()\n        {\n"
               "            {stmt}\n        }\n    }\n}\n", "t/T.cs::T.Adds"),
    "java": ("package com.acme;\n\nclass CalcTest {\n    @Test\n    void adds() {\n        {stmt}\n    }\n}\n",
             "t/CalcTest.java::CalcTest.adds"),
    "typescript": ("describe('c', () => {\n  test('adds', () => {\n    {stmt}\n  });\n});\n", "t/x.test.ts::adds"),
}


def plan(lang: str, text, *, at=None, node: str = None, oracle: str = "", instance: str = "IID", entry=None):
    """`plan_detector_mutation` over `text` (str or bytes) as the language `lang` reads `node`: (mutated str, detail, context)."""
    spec = PBC.parse_node(node or WRAP[lang][1])
    if entry is not None:
        spec["entry"] = entry
    data = text if isinstance(text, bytes) else text.encode("utf-8")
    mutated, detail, context = PBC.plan_detector_mutation(data, spec, instance, at, oracle, "", "t/file")
    return mutated, detail, context


def refusal_of(fn) -> str:
    try:
        fn()
    except PBC.Refusal as exc:
        return str(exc)
    return ""


def said(record: dict) -> str:
    """Everything the aggregate says in words: its notes and the note of each check row (t-2064 P4b: the old record's `notes` were both)."""
    return " ".join(list(record.get("notes") or []) + [str(r.get("note") or "") for r in record.get("checks") or []])
