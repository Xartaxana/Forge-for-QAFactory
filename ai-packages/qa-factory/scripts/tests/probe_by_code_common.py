"""probe_by_code.py: the critic's red probe by code.

A temp project with a tiny test file and a stub in place of `run_suite.py` (`PROBE_RUN_SUITE`).
The stub reads the typed request the script wrote, imports the test module AS IT LIES ON DISK
at that moment and calls the one function the request selects, then writes pytest-shaped
junit evidence and the summary `run_suite.py` prints — so every verdict below comes from the
mutated bytes really running, not from a canned answer, and pytest is never launched.
"""
# Shared helpers of test_probe_by_code.py, split by tools/test_split.py (TD-11c).
import hashlib
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, cleanup, run_script, temp_dir, use_project
sys.path.insert(0, str(SCRIPTS))
import probe_by_code as PBC  # noqa: E402
import probe_entries as PE  # noqa: E402


PY = sys.executable


TASK = "PROBE-2"


DISPATCH = "S5-qa-code-critic-1"


TEST_FILE_REL = "tests/test_calc.py"


FAKE_RUN_SUITE = r'''
"""A stand-in for `run_suite.py --request FILE`: runs the ONE selected node in-process."""
import hashlib
import importlib.util
import json
import os
import sys
import traceback
from pathlib import Path

if os.environ.get("PROBE_STUB_LOG"):  # one line per launch: how often the runner really ran
    with open(os.environ["PROBE_STUB_LOG"], "a", encoding="utf-8") as log:
        log.write(sys.argv[-1] + "\n")
if os.environ.get("PROBE_STUB_CRASH") == "1":
    print("stub: boom, no summary today")
    sys.exit(1)
if any(a.endswith("pytest") or a == "pytest" for a in sys.argv[1:]):
    print(json.dumps({"status": "stub_refused", "error": "the stub never launches pytest"}))
    sys.exit(2)
request = json.loads(Path(sys.argv[sys.argv.index("--request") + 1]).read_text(encoding="utf-8"))
if request.get("purpose") != "red_probe":
    print(json.dumps({"status": "stub_refused", "error": "purpose must be red_probe, got " + str(request.get("purpose"))}))
    sys.exit(2)
iid = request["selected_instance_ids"][0]
node = request["command"]["selector_args"][iid][0]
cwd = Path(request["command"]["cwd"]).resolve()
file_part, tail = node.split("::", 1)
parts = tail.split("::")
func_name = parts[-1].split("[")[0]
test_path = (cwd / file_part).resolve()
sys.path.insert(0, str(cwd))
sys.path.insert(0, str(test_path.parent))   # pytest's own `prepend` import mode: the test file's folder, so a sibling helper imports
spec = importlib.util.spec_from_file_location("probe_target_module", test_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
target = module
for name in parts[:-1]:
    target = getattr(target, name)
    if isinstance(target, type):
        target = target()
function = getattr(target, func_name)


def frame_lines(exc):
    frames = [f for f in traceback.extract_tb(exc.__traceback__)
              if Path(f.filename).resolve() != Path(__file__).resolve()]
    lines = []
    for index, frame in enumerate(frames):
        try:
            shown = Path(frame.filename).resolve().relative_to(cwd).as_posix()
        except ValueError:
            shown = frame.filename
        tail = f"{type(exc).__name__}" if index == len(frames) - 1 else ""
        lines.append(f"{shown}:{frame.lineno}: {tail}".rstrip())
    return lines


status, message, text = "passed", "", ""
try:
    function()
except BaseException as exc:  # noqa: BLE001 — the stub reports whatever fired
    status = "failed"
    message = f"{type(exc).__name__}: {exc}"
    text = "\n".join(frame_lines(exc))

classname = file_part.replace("/", ".")[:-3] + ("." + ".".join(parts[:-1]) if parts[:-1] else "")
name = parts[-1]
if status == "passed":
    row = f'<testcase classname="{classname}" name="{name}"/>'
else:
    from xml.sax.saxutils import escape, quoteattr
    row = (f'<testcase classname="{classname}" name="{name}"><failure message={quoteattr(message)}>'
           f'{escape(text)}</failure></testcase>')
xml = (f'<testsuite tests="1" failures="{0 if status == "passed" else 1}" errors="0" skipped="0">'
       + row + "</testsuite>")
job = hashlib.sha256(request["idempotency_key"].encode()).hexdigest()[:20]
# The task's artifacts live under the PROJECT, which is not the run directory when the profile
# runs in a subdirectory (the run-directory test below).
project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or cwd).resolve()
task_root = project / "qa-factory" / "artifacts" / request["task"]
run_dir = task_root / "evidence" / "runs" / job
run_dir.mkdir(parents=True, exist_ok=True)
report = run_dir / "report.junit.xml"
report.write_text(xml, encoding="utf-8")
label = f"red_probe-{job}"
summary_path = run_dir / f"{label}.json"
seen = test_path.read_bytes()
summary = {"task": request["task"], "label": label, "exit_code": 0 if status == "passed" else 1,
           "execution_status": status, "purpose": "red_probe",
           "summary_path": summary_path.relative_to(project).as_posix(),
           "report_evidence": {"path": report.relative_to(task_root).as_posix(),
                               "sha256": hashlib.sha256(report.read_bytes()).hexdigest()},
           "stub_seen_sha256": hashlib.sha256(seen).hexdigest(),
           # t-2064 P4b: the walk's aggregate carries no statement text, so the stub keeps the mutated text it ran for a test to read
           "stub_seen_text": seen.decode("utf-8", "replace"),
           # t-2045 N2: the Python marker is joined at run time (`'-'.join(['qa-probe', '<token>'])`), so the mutated bytes hold
           # `'qa-probe'` and no longer the contiguous `probe-`; either spelling says the stub ran the mutated file
           "stub_seen_marker": b"probe-" in seen or b"'qa-probe'" in seen}
if os.environ.get("PROBE_STUB_REPORTER"):  # the real run_suite names its reporter; the default stub does not
    summary["reporter"] = os.environ["PROBE_STUB_REPORTER"]
summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8")
print("MINE (note): stub")
print(json.dumps(summary))
sys.exit(summary["exit_code"])
'''


TEST_FILE = '''\
from calc import add
from hamcrest import assert_that, equal_to


def test_add():
    assert add(2, 2) == 4, "sum must be 4"


def test_dead_assert():
    total = add(1, 1)
    if total > 100:
        assert total == 2


def test_raises_first():
    raise RuntimeError("setup exploded")
    assert add(1, 1) == 2


def test_no_assert():
    add(1, 1)


class TestCalc:
    def test_method(self):
        result = add(3, 3)
        assert result in [6, 7]


def test_hamcrest():
    assert_that(add(2, 2), equal_to(4))


def test_multiline():
    assert add(
        2, 2
    ) == 4, (
        "sum must be 4"
    )
    assert True


def test_via_helper():
    from expectations import expect_sum
    expect_sum(add(2, 2), 4)
'''


CALC = "def add(a, b):\n    return a + b\n"


# The oracle outside the test: a helper module several tests share, which is how a real suite
# is written and what left `probe_by_code` with nothing to mutate on TP1-13797.
EXPECTATIONS = ('def expect_sum(actual, expected):\n'
                '    assert actual == expected, "sum must match"\n')


# A local stand-in for PyHamcrest: the assertion fires INSIDE this module, so pytest's last
# traceback line names hamcrest.py and the test's own line is an earlier frame — the shape
# every hamcrest-written project (TP1-13797's harness among them) reports.
HAMCREST = '''\
class _Matcher:
    def __init__(self, expected, negate=False):
        self.expected, self.negate = expected, negate

    def matches(self, actual):
        return (actual == self.expected) != self.negate

    def describe(self):
        return ("not " if self.negate else "") + repr(self.expected)


def equal_to(value):
    return _Matcher(value)


def is_not(matcher):
    return _Matcher(matcher.expected, not matcher.negate)


def assert_that(actual, matcher, reason=""):
    if not matcher.matches(actual):
        raise AssertionError(f"{reason}\\nExpected: {matcher.describe()}\\n     but: was {actual!r}")
'''


PROVENANCE = {"profile_id": "unit", "timestamp": "2026-09-24T10:00:00Z", "environment_id": "local",
              "expected_source_revision": "source-1", "observed_runtime_identity": "build-1",
              "evidence_refs": ["probe"], "result": "matched",
              "provenance": {"technical_verification": True, "source_linkage": "exact",
                             "deployed_source_revision": "source-1"}}


OBLIGATION_REFS = [{"obligation_id": "OB-ADD-1", "obligation_hash": "ob-hash-1"}]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1), encoding="utf-8")


def entry(case: str, test: str, instance: str, **extra) -> dict:
    return {"case": case, "covers": [case], "file": TEST_FILE_REL, "test": test, "instance_id": instance,
            "selector": test,  # what `--mine` builds a node id from (the run the author's job came from)
            "case_version_links": [{"case_id": case, "version": "cv_1"}], **extra}


def seed_author_job(root: Path, profile_id: str = "") -> dict:
    """The author's run of TC-100 as a job in the story's job store, built by `build_mine_request` - the
    producer of `instance_contracts` - and never typed: the probe measures a test's identity from it.
    `profile_id` is what the author's call named: with two profiles over one test root and a manifest that names
    none, the author's own `--mine` is the one that needs `--profile` (EP1-16)."""
    import execution_request as ER
    cfg = json.loads((root / "qa-factory" / "config.json").read_text(encoding="utf-8"))
    request, _notes, _reuse, _verified = ER.build_mine_request(
        root, ["TC-100"], cfg=cfg, task=TASK, dispatch_id=DISPATCH, probe=lambda spec: PROVENANCE,
        profile_id=profile_id)
    store = ER.JobStore(root / "qa-factory" / "artifacts" / TASK / "state" / "execution-jobs")
    _action, job = store.begin(request)
    store.update(job, status="completed", execution_status="passed", freshness="fresh")
    return request


def project(provenance: bool = True, *, shared_second: bool = False, row_profile: str = "") -> Path:
    """`shared_second`: a second profile `ui` over the SAME test root and the same cwd (the 12586 shape: the path
    cannot tell the profiles apart, and `_profile_cwd` still has one directory to give). `row_profile`: the profile
    every manifest row names (`profile_id`)."""
    root = temp_dir("qa-probe-code-")
    (root / "tests").mkdir()
    (root / "tests" / "test_calc.py").write_text(TEST_FILE, encoding="utf-8")
    (root / "calc.py").write_text(CALC, encoding="utf-8")
    (root / "hamcrest.py").write_text(HAMCREST, encoding="utf-8")
    (root / "tests" / "expectations.py").write_text(EXPECTATIONS, encoding="utf-8")   # a helper under the test root: a product-side one is never hopped into (B1)
    bin_dir = root.parent / (root.name + "-bin")
    bin_dir.mkdir()
    fake_pytest = bin_dir / "pytest"  # named pytest: the request builder's own pytest check
    fake_pytest.write_text("import sys; sys.exit(3)\n", encoding="utf-8")
    probe_script = root.parent / (root.name + "-runtime-probe.py")
    probe_script.write_text("import json\nprint(json.dumps(" + repr(PROVENANCE) + "))\n", encoding="utf-8")
    profiles = [{"profile_id": "unit", "selected": True, "roots": {"test": "tests"},
                 "commands": {"one_test": {"argv": [PY, str(fake_pytest), "--junitxml", "{report_path}"],
                                           "cwd": "."}},
                 "reporter": {"kind": "junit-xml"}, "selectors": {"verified": True}}]
    if shared_second:
        profiles.append(dict(json.loads(json.dumps(profiles[0])), profile_id="ui"))
    write_json(root / "qa-factory" / "config.json", {
        "tests_root": "tests", "app_root": ".",
        "profiles": profiles,
        "execution": {"runtime_probes": {"unit": {"argv": [PY, str(probe_script)], "cwd": ".",
                                                   "timeout_s": 20}}}})
    task_root = root / "qa-factory" / "artifacts" / TASK
    write_json(task_root / "pipeline.json", {"stages": {"S5": {"status": "running"}},
                                             "first_test_run_at": "2026-09-24T09:00:00+00:00"})
    scope = ["TC-100", "TC-101", "TC-102", "TC-103", "TC-104", "TC-105", "TC-106", "TC-107"]
    write_json(task_root / "state" / "controller.json", {
        "schema_version": "2", "revision": "1", "source_revision": "source-1",
        "dispatches": {DISPATCH: {"id": DISPATCH, "stage": "S5", "role": "qa-code-critic",
                                  "status": "running", "scope": scope, "budget": {"requests": 50}}}})
    # test_add is bound to its bytes the way manifest_from_tests.py binds every row: the raw sha256
    # of the file (`TestFile.content_sha`), which is also what validate_artifacts enforces.
    bound = {"test_content_sha": PBC.sha256((root / TEST_FILE_REL).read_bytes())}
    named = {"profile_id": row_profile} if row_profile else {}
    write_json(task_root / "work" / "automation-manifest.json", {"tests": [
        entry("TC-100", "test_add", "test_add", obligation_refs=OBLIGATION_REFS, trace_binding=bound,
              obligation_ids=["OB-ADD-1"], defect_location="calc.py:2", assertion_id="add_returns_sum", **named),
        entry("TC-101", "test_dead_assert", "test_dead_assert"),
        entry("TC-102", "test_raises_first", "test_raises_first"),
        entry("TC-103", "test_no_assert", "test_no_assert"),
        entry("TC-104", "test_method", "test_method"),
        entry("TC-105", "test_hamcrest", "test_hamcrest"),
        entry("TC-106", "test_multiline", "test_multiline"),
        entry("TC-107", "test_via_helper", "test_via_helper"),
    ]})
    # The author's green run block over exactly these bytes of test_add: the probe binds its
    # `input_hash` to it through the function's own sha, never to a whole-file guess. That sha is the
    # one the author's job carries (`instance_contracts`): one derivation, and the probe's identity
    # of the test is measured from the same job.
    request = seed_author_job(root, "unit" if shared_second else "")
    sha = request["instance_contracts"]["test_add"]["instance_content_sha"]
    # `runtime_provenance` is where a receipt's `build_id` comes from (proof_level.binding_facts);
    # a project whose author run block carries none has no receipt to write, and says so.
    block = {"schema_version": 2, "dispatch_id": "S5-qa-automator-1", "purpose": "initial",
             "results": [{"instance_id": "test_add", "status": "passed", "instance_content_sha": sha,
                          "source_fingerprint": {"source_sha": "source-1", "test_content_sha": "author-tcs-1"}}]}
    if provenance:
        block["runtime_provenance"] = {"observed_runtime_identity": "build-1", "environment_id": "env-1"}
    write_json(task_root / "work" / "run-blocks" / "20260924T090000000000Z-author1.json", block)
    return root


def env_for(root: Path, stub: Path, **extra) -> dict:
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root), PROBE_RUN_SUITE=str(stub))
    env.pop("PROBE_STUB_CRASH", None)
    env.update(extra)
    return env


def model_entries(root: Path, stub, test: str, instance: str, dispatch: str = DISPATCH, task: str = TASK) -> None:
    """t-2064 P4b: a call with no `--at` and no `--oracle` walks every check and needs a model entry per check. This writes the
    window's model file (`work/probe-models/<dispatch>.json`) with one `invert` entry per key `--plan` lists, so the wrappers below keep
    taking the inversion road through the loader a critic's file goes through. NOT used by `run_close` (S6 is no role: it inverts by itself)."""
    try:
        env = env_for(root, stub) if stub else dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
        keys = PE.plan_keys(["--task", task, "--instance", instance, "--test", test], root=root, env=env)
        if keys:    # an EMPTY plan is the probe's refusal to read: a file of no entries would be a byte the wrapper wrote, not the probe
            PE.write_invert_entries(root / "qa-factory" / "artifacts" / task, dispatch, keys=keys)
    except RuntimeError:
        pass    # `--plan` refuses (no such instance, a file that is not there): no world to write entries for; the probe's own refusal is what the test reads


def run(root: Path, stub: Path, test: str, instance: str, mutation: str = "invert", **extra):
    model_entries(root, stub, test, instance)
    proc = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--test", test,
                      "--instance", instance, "--mutation", mutation, "--json",
                      cwd=root, env=env_for(root, stub, **extra))
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    try:
        payload = json.loads("\n".join(lines)) if lines and lines[0].startswith("{") else {}
    except ValueError:
        payload = {}
    return proc, payload


def mutated_line(root: Path, record: dict, line: int) -> str:
    """Line `line` (1-based) of the mutated bytes the stub ran for the walk's first run (`stub_seen_text` of its evidence summary)."""
    task_root = root / "qa-factory" / "artifacts" / TASK
    ref = record.get("evidence_ref")
    summary = json.loads((task_root / ref).read_text(encoding="utf-8")) if ref else {}
    lines = str(summary.get("stub_seen_text") or "").splitlines()
    return lines[line - 1] if len(lines) >= line else ""


def read_check_record(root: Path, instance: str, which: int = 0) -> dict:
    """The `which`-th per-check record of the instance (`work/probes/checks/`, in file name order): what a walk writes beside its aggregate."""
    directory = root / "qa-factory" / "artifacts" / TASK / "work" / "probes" / "checks"
    files = sorted(directory.glob(f"{instance}--*.json")) if directory.is_dir() else []
    return json.loads(files[which].read_text(encoding="utf-8")) if len(files) > which else {}


def read_record(root: Path, instance: str) -> dict:
    path = root / "qa-factory" / "artifacts" / TASK / "work" / "probes" / f"{instance}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def snapshot(root: Path) -> dict:
    """{path: sha256 or 'dir'} of everything a probe can write inside the story - records, requests,
    receipts, jobs, the manifest - so 'nothing was written' is compared, not asserted."""
    task = task_of(root)
    found = {}
    for sub in ("work/probes", "work/probe-requests", "work/sensitivity-receipts", "state/execution-jobs"):
        base = task / sub
        found[sub] = "dir" if base.is_dir() else "absent"
        for path in sorted(base.rglob("*")) if base.is_dir() else []:
            found[path.relative_to(task).as_posix()] = PBC.sha256(path.read_bytes()) if path.is_file() else "dir"
    manifest = task / "work" / "automation-manifest.json"
    found["manifest"] = PBC.sha256(manifest.read_bytes()) if manifest.is_file() else "absent"
    return found


def give_word(root: Path, at: str, match: str = "already probed on these bytes") -> None:
    """A person's recorded word for the repeat block, said at `at` (orchestrator: waiver.py)."""
    path = task_of(root) / "pipeline.json"
    pipeline = json.loads(path.read_text(encoding="utf-8"))
    pipeline["stage_overrides"] = [{"stage": "S5", "match": match, "decision": "probe it again, I asked", "at": at}]
    write_json(path, pipeline)


def cleanup_beside(root: Path) -> None:
    for extra in root.parent.glob(root.name + "-*"):
        if extra.is_dir():
            cleanup(extra)
        else:
            extra.unlink(missing_ok=True)


# --- a test that is not Python -----------------------------------------------------------------------

def tree_state(root: Path) -> dict:
    """Every file under the project with its bytes' sha256 and mtime: a refusal changes none."""
    return {p.relative_to(root).as_posix(): (sha256_of(p), p.stat().st_mtime_ns)
            for p in sorted(root.rglob("*")) if p.is_file()}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- the live receipt (D-0010): written, accepted unchanged, published, never downgrading -----------

def task_of(root: Path) -> Path:
    return root / "qa-factory" / "artifacts" / TASK


def manifest_of(root: Path) -> dict:
    return json.loads((task_of(root) / "work" / "automation-manifest.json").read_text(encoding="utf-8"))


def row_of(root: Path, iid: str = "test_add") -> dict:
    return next(t for t in manifest_of(root)["tests"] if t.get("instance_id") == iid)


def binding_of(root: Path, oid: str = "OB-ADD-1") -> dict:
    return next((b for b in manifest_of(root).get("obligation_bindings") or []
                 if b.get("obligation_id") == oid), {})


def receipt_files(root: Path, stem: str = "test_add") -> list:
    directory = task_of(root) / "work" / "sensitivity-receipts"
    return sorted(directory.glob(f"{stem}-live-*.json")) if directory.is_dir() else []


class _LoggedStream:
    """A stdout/stderr stand-in that writes into one shared list, so the ORDER of everything `main` does
    (the calls it makes and what it prints on which stream) is compared, not only the final text."""

    def __init__(self, log: list, tag: str):
        self.log, self.tag = log, tag

    def write(self, text: str) -> int:
        self.log.append((self.tag, text))
        return len(text)

    def flush(self) -> None:
        pass


def _main_in_process(argv: list, probe=None, publish=("", False), release=None) -> tuple:
    """(the exit code, the log) of `probe_by_code.main()` run in this process with `probe`, `publish_binding`
    and `release_copy` replaced: `probe` is the record it returns (or the exception it raises); `publish` is
    (the line it returns, whether it fills `record["publish"]`); `release` the dict (or exception) of the door."""
    import contextlib
    log: list = []

    def fake_probe(*args, **kwargs):
        log.append(("call", "probe", args, kwargs))
        if isinstance(probe, Exception):
            raise probe
        return probe

    def fake_publish(task, task_root, record):
        log.append(("call", "publish", (task, Path(task_root).as_posix())))
        if publish[1]:
            record["publish"] = {"published": True}
        return publish[0]

    def fake_release(root, what):
        log.append(("call", "release", (Path(root).as_posix(), what)))
        if isinstance(release, Exception):
            raise release
        return release

    saved = (PBC.probe, PBC.publish_binding, PBC.release_copy, sys.argv)
    PBC.probe, PBC.publish_binding, PBC.release_copy = fake_probe, fake_publish, fake_release
    sys.argv = ["probe_by_code.py", *argv]
    try:
        with contextlib.redirect_stdout(_LoggedStream(log, "out")), contextlib.redirect_stderr(_LoggedStream(log, "err")):
            try:
                PBC.main()
                code = "returned"
            except SystemExit as exc:
                code = exc.code
    finally:
        PBC.probe, PBC.publish_binding, PBC.release_copy, sys.argv = saved
    return code, log


def _streams(log: list) -> tuple:
    return ("".join(t for tag, t, *_ in log if tag == "out"), "".join(t for tag, t, *_ in log if tag == "err"))


def _calls(log: list) -> list:
    return [entry[1] for entry in log if entry[0] == "call"]


# --- t-043 C: a second probe of the same bytes is answered (D-0018) -------------------------------------

class fresh:
    """A project of its own (`project()` plus `use_project`), removed with what lies beside it."""
    def __enter__(self) -> Path:
        self.root = project()
        use_project(self.root)
        return self.root

    def __exit__(self, *_exc) -> None:
        cleanup(self.root)
        cleanup_beside(self.root)
