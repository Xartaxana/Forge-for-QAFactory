"""probe_by_code.py --mutation alternative: the red probe models a case's declared reading B (TQ1-25, t-739 + t-750).

A temp project, the stub `PROBE_RUN_SUITE` of test_probe_by_code (it really imports and runs the mutated test), a case
that declares `alternatives`, and two tests of the same Then: the night TC-001 shape `update_date > stamp` (passes under a
completion stamp: the weak oracle) and the manual shape `stamp <= t_done - tolerance` (fails under it: the strong one).
Keys K10-K32 are the spec's (t-739 section 2.4 and 3.2, the plan review's B-1..B-3); the judge table (K17) is pure.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import check, check_eq, check_in, cleanup, finish, run_script, temp_dir  # noqa: E402
from harness import mark_project, use_project  # noqa: E402

import contract as C  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
from test_probe_by_code import (DISPATCH, FAKE_RUN_SUITE, PROVENANCE, PY, TASK, _calls, _main_in_process,  # noqa: E402
                                _streams, cleanup_beside, env_for, snapshot, task_of, write_json)

STAMP_REL = "tests/test_stamp.py"
STAMP = '''\
T_DONE = 160.0
TOLERANCE = 5.0


def read_stamp():
    return 100.5


def unused():
    stamp = read_stamp()
    return stamp


def test_weak():
    stamp = read_stamp()
    update_date = T_DONE + 1.0
    assert update_date > stamp, "Then 2: the stamp precedes the completion"


def test_strong():
    stamp = read_stamp()
    assert stamp <= T_DONE - TOLERANCE, "Then 2: the stamp is the trigger, not the completion"


def test_both():
    stamp = read_stamp()
    assert stamp <= T_DONE - TOLERANCE, "Then 2: the stamp is the trigger, not the completion"


def test_untaken():
    stamp = read_stamp()
    if T_DONE < 0:
        marker = read_stamp()
    assert stamp <= T_DONE - TOLERANCE, "Then 2: untaken"


def test_after():
    stamp = read_stamp()
    assert stamp <= T_DONE - TOLERANCE, "Then 2: after"
    later = read_stamp()


def test_nested():
    stamp = read_stamp()

    def inner():
        return read_stamp()
    assert stamp <= T_DONE - TOLERANCE, "Then 2: nested"


def test_helper():
    helper_assert(read_stamp())


def helper_assert(stamp):
    assert stamp <= T_DONE - TOLERANCE, "Then 2: in a helper"
'''
HELPERS = "def reader():\n    return 100.5\n"
TS_REL = "tests/stamp.spec.ts"
INSTANCES = ("test_weak", "test_strong", "test_both", "test_untaken", "test_after", "test_nested")
ALT = '[{"id": "ALT-1", "then": 2, "reading": "the stamp is taken at completion", "ref": "R-2"}]'
MODEL = {"alternative": "TC-001:ALT-1", "find": "stamp = read_stamp()", "replace": "stamp = T_DONE"}


def case_text(case: str, alternatives=ALT) -> str:
    key = f"alternatives: {alternatives}\n" if alternatives is not None else ""
    return f"---\nid: {case}\n{key}---\n# {case}\n\n## Then\n1. the request is accepted\n2. the stamp is the trigger time\n"


def assert_line(text: str, function: str) -> int:
    lines = text.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith(f"def {function}("))
    return next(i + 1 for i in range(start, len(lines)) if lines[i].strip().startswith("assert "))


def entry(iid: str, file: str = STAMP_REL, covers=("TC-001",)) -> dict:
    return {"case": covers[0], "covers": list(covers), "file": file, "test": iid, "instance_id": iid, "selector": iid,
            "case_version_links": [{"case_id": c, "version": "cv_1"} for c in covers]}


def alt_project(*, extra_tests=(), alternatives=ALT) -> Path:
    import execution_request as ER
    root = temp_dir("qa-probe-alt-")
    (root / "tests").mkdir()
    (root / STAMP_REL).write_bytes(STAMP.encode("utf-8"))   # LF on every platform
    (root / "tests" / "helpers.py").write_text(HELPERS, encoding="utf-8")
    (root / TS_REL).write_text("test('stamp', () => { expect(1).toBe(1); });\n", encoding="utf-8")
    (root / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    bin_dir = root.parent / (root.name + "-bin")
    bin_dir.mkdir()
    fake_pytest = bin_dir / "pytest"
    fake_pytest.write_text("import sys; sys.exit(3)\n", encoding="utf-8")
    probe_script = root.parent / (root.name + "-runtime-probe.py")
    probe_script.write_text("import json\nprint(json.dumps(" + repr(PROVENANCE) + "))\n", encoding="utf-8")
    profiles = [{"profile_id": "unit", "selected": True, "roots": {"test": "tests"},
                 "commands": {"one_test": {"argv": [PY, str(fake_pytest), "--junitxml", "{report_path}"], "cwd": "."}},
                 "reporter": {"kind": "junit-xml"}, "selectors": {"verified": True}}]
    write_json(root / "qa-factory" / "config.json", {
        "tests_root": "tests", "app_root": ".", "profiles": profiles,
        "execution": {"runtime_probes": {"unit": {"argv": [PY, str(probe_script)], "cwd": ".", "timeout_s": 20}}}})
    task = root / "qa-factory" / "artifacts" / TASK
    write_json(task / "pipeline.json", {"stages": {"S5": {"status": "running"}},
                                        "first_test_run_at": "2026-09-24T09:00:00+00:00"})
    write_json(task / "state" / "controller.json", {
        "schema_version": "2", "revision": "1", "source_revision": "source-1",
        "dispatches": {DISPATCH: {"id": DISPATCH, "stage": "S5", "role": "qa-code-critic", "status": "running",
                                  "scope": ["TC-001", "TC-002"], "budget": {"requests": 50}}}})
    (task / "work" / "test-cases").mkdir(parents=True)
    (task / "work" / "test-cases" / "TC-001.md").write_text(case_text("TC-001", alternatives), encoding="utf-8")
    (task / "work" / "test-cases" / "TC-002.md").write_text(case_text("TC-002", alternatives), encoding="utf-8")
    tests = [entry(iid) for iid in INSTANCES if iid != "test_both"]
    tests.append(entry("test_both", covers=("TC-001", "TC-002")))
    tests.extend(extra_tests)
    bindings = [{"case": "TC-001", "then": 2, "instance_id": iid, "assertion_ref": f"{STAMP_REL}:{assert_line(STAMP, iid)}",
                 "status": "covered"} for iid in INSTANCES]
    bindings.append({"case": "TC-002", "then": 2, "instance_id": "test_both", "status": "covered",
                     "assertion_ref": f"{STAMP_REL}:{assert_line(STAMP, 'test_both')}"})
    write_json(task / "work" / "automation-manifest.json", {"tests": tests, "then_bindings": bindings})
    cfg = json.loads((root / "qa-factory" / "config.json").read_text(encoding="utf-8"))
    request, _n, _r, _v = ER.build_mine_request(root, ["TC-001", "TC-002"], cfg=cfg, task=TASK, dispatch_id=DISPATCH,
                                                probe=lambda spec: PROVENANCE)
    store = ER.JobStore(task / "state" / "execution-jobs")
    _action, job = store.begin(request)
    store.update(job, status="completed", execution_status="passed", freshness="fresh")
    rows = [{"instance_id": iid, "status": "passed", "instance_content_sha": c["instance_content_sha"],
             "source_fingerprint": {"source_sha": "source-1", "test_content_sha": "author-" + iid}}
            for iid, c in request["instance_contracts"].items()]
    write_json(task / "work" / "run-blocks" / "20260924T090000000000Z-author1.json", {
        "schema_version": 2, "dispatch_id": "S5-qa-automator-1", "purpose": "initial", "results": rows,
        "runtime_provenance": {"observed_runtime_identity": "build-1", "environment_id": "env-1"}})
    return root


def put_model(root: Path, name: str, doc) -> str:
    path = task_of(root) / "work" / "probe-models" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc if isinstance(doc, str) else json.dumps(doc), encoding="utf-8")
    return "work/probe-models/" + name


def parse(proc) -> dict:
    text = proc.stdout.strip()
    try:
        return json.loads(text) if text.startswith("{") else {}
    except ValueError:
        return {}


def alt(root: Path, stub: Path, iid: str = "test_weak", token: str = "TC-001:ALT-1", model="m.json", extra=(), test=None,
        env=None, mutation="alternative"):
    argv = ["--task", TASK, "--dispatch", DISPATCH, "--test", test or f"{STAMP_REL}::{iid}", "--instance", iid,
            "--mutation", mutation, "--json", *extra]
    if token is not None:
        argv += ["--alternative", token]
    if model is not None:
        argv += ["--model", "work/probe-models/" + model if "/" not in model else model]
    proc = run_script("probe_by_code.py", *argv, cwd=root, env=env_for(root, stub, **(env or {})))
    return proc, parse(proc)


def record_of(root: Path, iid: str, case: str = "TC-001", alt_id: str = "ALT-1") -> dict:
    path = PBC.alternative_record_path(task_of(root), iid, case, alt_id)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def report(root: Path, stub: Path, *extra) -> list:
    proc = run_script("probe_by_code.py", "--task", TASK, "--alternatives", "--json", *extra, cwd=root, env=env_for(root, stub))
    check_eq("report: exit 0", proc.returncode, 0)
    try:
        return json.loads(proc.stdout)
    except ValueError:
        return []


def row_of(rows: list, iid: str, token: str = "TC-001:ALT-1") -> dict:
    return next((r for r in rows if r["instance"] == iid and r["alternative"] == token), {})


def stat_text(root: Path) -> bytes:
    return (root / STAMP_REL).read_bytes()


def with_stub(body) -> None:
    stub_dir = temp_dir("qa-probe-alt-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    root = alt_project()
    try:
        body(root, stub)
    finally:
        cleanup(root)
        cleanup_beside(root)
        cleanup(stub_dir)


def stub_log_lines(root: Path) -> int:
    log = root / "stub.log"
    return len(log.read_text(encoding="utf-8").splitlines()) if log.is_file() else 0


def k10_the_pair(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    original = stat_text(root)
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    proc, weak = alt(root, stub, "test_weak", env=env)
    check_eq("K10 weak oracle: exit 0, no_failure (it passes under a completion stamp)", (proc.returncode, weak.get("verdict")),
             (0, "no_failure"))
    check_eq("K10 weak: the author's bytes are back (sha equal before/after)", PBC.sha256(stat_text(root)), PBC.sha256(original))
    check_eq("K10 weak: restore verified from the copy", (weak.get("restore") or {}).get("verified"), True)
    check_eq("K10 weak: author_green and reach are the verdict's inputs", (weak.get("author_green"), (weak.get("reach") or {}).get("ok")),
             (True, True))
    proc, strong = alt(root, stub, "test_strong", env=env)
    check_eq("K10 strong oracle: exit 0, intended_failure (it fails under a completion stamp)",
             (proc.returncode, strong.get("verdict")), (0, "intended_failure"))
    check_eq("K10 strong: the bytes are back", PBC.sha256(stat_text(root)), PBC.sha256(original))
    check_eq("K10 strong: the failure is AT the Then's own assert", strong.get("actual_location"),
             f"{STAMP_REL}:{assert_line(STAMP, 'test_strong')}")
    print("witness K10: sha256 before", PBC.sha256(original), "after", PBC.sha256(stat_text(root)))
    # B-2 record shape: the names the exit and print paths read
    for key in ("mutated_file", "test_file_sha256", "expected_reason", "record", "test_node", "instance_content_sha"):
        check(f"B-2 the record carries `{key}`", key in strong and strong[key] is not None, str(sorted(strong)))
    check_eq("B-2 mutated_file names the test file here", (strong["mutated_file"] or {}).get("path"), STAMP_REL)
    check_eq("K11 mutation_kind alternative_model, proof_level null (never a level the window reads)",
             (strong.get("mutation_kind"), strong.get("proof_level")), ("alternative_model", None))


def k11_no_live_receipt(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    before = snapshot(root)
    invert_path = task_of(root) / "work" / "probes" / "test_strong.json"
    proc, got = alt(root, stub, "test_strong")
    check_eq("K11 alternative probe ran", got.get("verdict"), "intended_failure")
    after = snapshot(root)
    new = sorted(set(after) - set(before))
    check("K11 only alternative-owned files appeared (record, request, job): no receipt, no invert record",
          all(("alternative" in p or "probe-alt-" in p or "execution-jobs" in p) for p in new if p not in
              ("work/probe-requests", "work/probes", "work/probes/alternative")), str(new))
    check("K11 work/probes/<IID>.json (the invert record) was not written", not invert_path.exists())
    check("K11 no live receipt", not any("sensitivity-receipts" in p and after[p] not in ("dir", "absent") for p in after),
          str(after))
    check_eq("K11 the manifest is untouched", after["manifest"], before["manifest"])
    check("K11 the request file is probe-alt-<stem>, never probe-<IID>",
          (task_of(root) / "work" / "probe-requests" / ("probe-alt-" + PBC.alternative_record_path(
              task_of(root), "test_strong", "TC-001", "ALT-1").stem + ".json")).is_file()
          and not (task_of(root) / "work" / "probe-requests" / "probe-test_strong.json").exists())
    request = json.loads((task_of(root) / got["request"]).read_text(encoding="utf-8"))
    check_eq("K11 built_by.mutation_kind names the alternative", (request.get("built_by") or {}).get("mutation_kind"),
             "alternative_model")
    proc2, inv = alt(root, stub, "test_strong", token=None, model=None, mutation="invert")
    check_eq("K11 an invert probe afterwards still runs (its own slot)", (proc2.returncode, inv.get("verdict")),
             (0, "intended_failure"))
    check("K11 and the invert record is at its own path", invert_path.is_file())


def k12_unknown_answers(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}

    def unknown(label: str, **kw) -> None:
        before = snapshot(root)
        files = (root / STAMP_REL).read_bytes()
        proc, got = alt(root, stub, env=env, **kw)
        check_eq(f"K12 {label}: exit 1, an unknown ANSWER", (proc.returncode, got.get("verdict")), (1, "unknown"))
        check_eq(f"K12 {label}: work/ and the test are unchanged", (snapshot(root), (root / STAMP_REL).read_bytes()),
                 (before, files))
        check(f"K12 {label}: it says why", bool(got.get("why")), str(got))

    unknown("an undeclared ALT", token="TC-001:ALT-9")
    case1 = task_of(root) / "work" / "test-cases" / "TC-001.md"
    text = case1.read_text(encoding="utf-8")
    case1.write_text(case_text("TC-001", None), encoding="utf-8")
    unknown("a case without the key", token="TC-001:ALT-1")
    case1.write_text(case_text("TC-001", "not json"), encoding="utf-8")
    unknown("a malformed key", token="TC-001:ALT-1")
    case1.write_text(text, encoding="utf-8")
    case1.rename(case1.with_name("TC-001.md.gone"))
    unknown("the case file is absent", token="TC-001:ALT-1")
    case1.with_name("TC-001.md.gone").rename(case1)
    case1.write_text(text.replace('"then": 2', '"then": 5'), encoding="utf-8")
    unknown("a Then that is not in the case", token="TC-001:ALT-1")
    case1.write_text(text.replace(', "ref": "R-2"', ""), encoding="utf-8")
    unknown("t-768 B-2: an ALT with no `ref` (the report's `case_unreadable` too: ONE validity rule)", token="TC-001:ALT-1")
    case1.write_text(case_text("TC-001", ALT[:-1] + ", " + ALT[1:]), encoding="utf-8")     # ALT-1 twice
    unknown("t-768 B-2: a duplicate ALT id", token="TC-001:ALT-1")
    case1.write_text(text, encoding="utf-8")
    manifest = task_of(root) / "work" / "automation-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    kept = list(data["then_bindings"])
    data["then_bindings"] = [r for r in kept if r["instance_id"] != "test_weak"]
    write_json(manifest, data)
    unknown("no covered binding", token="TC-001:ALT-1")
    check_eq("K12 the stub never ran", stub_log_lines(root), 0)
    data["then_bindings"] = kept
    write_json(manifest, data)


def k13_k21_gaps(root: Path, stub: Path) -> None:
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    put_model(root, "g.json", {"alternative": "TC-001:ALT-1", "gap": "the stamp is read inside the product"})
    original = stat_text(root)
    proc, got = alt(root, stub, "test_weak", model="g.json", env=env)
    check_eq("K13 a model gap: exit 1, the record is `gap`, cause model",
             (proc.returncode, got.get("verdict"), got.get("cause")), (1, "gap", "model"))
    check_eq("K13 the test bytes are unchanged and the stub never ran", (stat_text(root), stub_log_lines(root)), (original, 0))
    check_eq("K13 the record is on disk, `gap`", record_of(root, "test_weak").get("verdict"), "gap")
    # K21: a test that is not Python
    manifest = task_of(root) / "work" / "automation-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["tests"].append(entry("ts_stamp", TS_REL))
    data["then_bindings"].append({"case": "TC-001", "then": 2, "instance_id": "ts_stamp", "assertion_ref": f"{TS_REL}:1",
                                  "status": "covered"})
    write_json(manifest, data)
    ts_original = (root / TS_REL).read_bytes()
    proc, got = alt(root, stub, "ts_stamp", model=None, test=f"{TS_REL}::stamp", env=env)
    check_eq("K21 a non-Python test on a declared ALT: exit 1, gap, cause tooling, no --model needed",
             (proc.returncode, got.get("verdict"), got.get("cause")), (1, "gap", "tooling"))
    check_in("K21 the language and the red_sandbox door are named", "red_sandbox.py --probe", got.get("door", ""))
    check_eq("K21 the language", got.get("language"), "typescript")
    check_eq("K21 nothing was mutated", ((root / TS_REL).read_bytes(), stub_log_lines(root)), (ts_original, 0))
    before = snapshot(root)
    proc, got = alt(root, stub, "ts_stamp", token="TC-001:ALT-9", model=None, test=f"{TS_REL}::stamp", env=env)
    check_eq("K21 an UNDECLARED ALT on a non-Python test: unknown, no record", (proc.returncode, got.get("verdict")),
             (1, "unknown"))
    check_eq("K21 and nothing was written", snapshot(root), before)


def k14_refusals(root: Path, stub: Path) -> None:
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    original = stat_text(root)

    def refused(label: str, doc=None, *, name="r.json", token="TC-001:ALT-1", iid="test_weak", model=None, extra=(),
                want=None, mutation="alternative") -> None:
        if doc is not None:
            put_model(root, name, doc)
        before = snapshot(root)
        proc, got = alt(root, stub, iid, token=token, model=model if model is not None else name, extra=extra, env=env,
                        mutation=mutation)
        check_eq(f"K14 {label}: exit 2, refused", (proc.returncode, got.get("status")), (2, "refused"))
        if want:
            check_in(f"K14 {label}: the text names the problem", want, got.get("error", ""))
        check_eq(f"K14 {label}: the tree is snapshot-equal and the stub never ran", (snapshot(root), stat_text(root),
                                                                                    stub_log_lines(root)), (before, original, 0))

    base = dict(MODEL)
    refused("find absent", dict(base, find="stamp = nowhere()"), want="0 times")
    refused("find twice (the whole function)", dict(base, find="stamp"), want="times")
    refused("find inside the asserting statement", dict(base, find="update_date > stamp", replace="update_date < stamp"),
            want="inversion")
    refused("line-break count differs", dict(base, replace="stamp = T_DONE\n"), want="line breaks")
    refused("replace == find (no code changed)", dict(base, replace="stamp = read_stamp()"), want="changes no code")
    refused("replace differs only by a trailing comment", dict(base, replace="stamp = read_stamp()  # B"), want="changes no code")
    refused("the mutated text does not parse", dict(base, replace="stamp = ("), want="not parse")
    refused("find matches only module level", dict(base, find="TOLERANCE = 5.0", replace="TOLERANCE = 500.0"), want="0 times")
    refused("model alternative differs from the token", dict(base, alternative="TC-001:ALT-2"), want="exactly")
    refused("both find and gap", dict(base, gap="why"), want="EXACTLY ONE")
    refused("neither find nor gap", {"alternative": "TC-001:ALT-1"}, want="EXACTLY ONE")
    refused("a bare ALT-1 token", base, token="ALT-1", want="<case>:ALT-<n>")
    refused("a case the instance does not cover", dict(base, alternative="TC-002:ALT-1"), token="TC-002:ALT-1",
            want="does not cover")
    refused("--oracle with alternative", base, extra=("--oracle", "x::y"), want="--oracle or --at")
    refused("--at with alternative", base, extra=("--at", "3"), want="--oracle or --at")
    refused("--model missing on a Python test", model="", token="TC-001:ALT-1", want="--model")
    outside = temp_dir("qa-probe-alt-out-")
    (outside / "m.json").write_text(json.dumps(base), encoding="utf-8")
    refused("model outside work/probe-models", model=str(outside / "m.json"), want="not under")
    link = task_of(root) / "work" / "probe-models" / "link.json"
    try:
        os.symlink(outside / "m.json", link)
        refused("a symlink out of work/probe-models", model="link.json", want="not under")
    except (OSError, NotImplementedError):
        check("K14 symlink: not creatable on this machine (the resolve() check is the same code path as the outside file)", True)
    cleanup(outside)
    # F-B: a product file outside the test roots
    refused("a model in a product file (outside the test roots)", dict(base, function="calc.py::add", find="return a + b",
                                                                       replace="return a - b"), want="red_sandbox.py --probe")
    refused("`function` that is not [<file>.py::]<name>", dict(base, function="x::y"), want="`function`")
    (task_of(root) / "work" / "probe-models" / "bin.json").write_bytes(b"\xff\xfe\x00{")
    refused("a non-UTF-8 model file", model="bin.json", want="not UTF-8")
    put_model(root, "empty.json", "")
    refused("an empty model file", model="empty.json", want="empty or not valid JSON")
    refused("a model that is a list", [], name="list.json", want="not one object")
    # CLI misuse (K22): nothing read
    before = snapshot(root)
    for label, extra, kw in (("--alternative without --mutation alternative", ("--alternative", "TC-001:ALT-1"), {"mutation": "invert", "token": None, "model": None}),
                             ("--mutation alternative without --alternative", (), {"token": None}),
                             ("--supersede without --mutation alternative", ("--supersede", "why"), {"mutation": "invert", "token": None, "model": None}),
                             ("--model without --mutation alternative", ("--model", "work/probe-models/m.json"), {"mutation": "invert", "token": None, "model": None}),
                             ("--supersede empty", ("--supersede", ""), {}),
                             ("--supersede 301 characters", ("--supersede", "x" * 301), {})):
        proc, got = alt(root, stub, extra=extra, env=env, **kw)
        check_eq(f"K22 {label}: exit 2, refused, nothing read or written", (proc.returncode, got.get("status"), snapshot(root)),
                 (2, "refused", before))


def k15_limits(root: Path, stub: Path) -> None:
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    unique = "stamp = read_stamp()"
    # find AT 2000 characters (padded with a comment-free expression, unique) accepted; 2001 refused by length
    pad = " " * (PBC.MODEL_TEXT_MAX - len(unique))
    long_find = unique + pad
    check_eq("K15 find length AT the limit", len(long_find), 2000)
    try:
        PBC.load_model(task_of(root), put_model(root, "f2000.json", dict(MODEL, find=long_find)), "TC-001:ALT-1")
        got = "accepted"
    except PBC.Refusal:
        got = "refused"
    check_eq("K15 find 2000: accepted by the length rule", got, "accepted")
    for label, doc, want in (("find 2001", dict(MODEL, find=long_find + " "), "`find`"),
                             ("replace 2001", dict(MODEL, replace="x" * 2001), "`replace`"),
                             ("gap 301", {"alternative": "TC-001:ALT-1", "gap": "g" * 301}, "`gap`"),
                             ("gap 300 accepted below", None, None)):
        if doc is None:
            continue
        try:
            PBC.load_model(task_of(root), put_model(root, "lim.json", doc), "TC-001:ALT-1")
            got = "accepted"
        except PBC.Refusal as exc:
            got = "refused" if want in str(exc) else "wrong refusal"
        check_eq(f"K15 {label}: refused naming the limit", got, "refused")
    check_eq("K15 gap 300 accepted", PBC.load_model(task_of(root), put_model(root, "g300.json", {"alternative": "TC-001:ALT-1",
                                                                                              "gap": "g" * 300}),
                                                    "TC-001:ALT-1")["gap"], "g" * 300)
    check_eq("K15 replace of 0 chars passes the length rule", PBC.load_model(
        task_of(root), put_model(root, "r0.json", dict(MODEL, replace="")), "TC-001:ALT-1")["replace"], "")
    body = json.dumps(dict(MODEL, replace="x")).ljust(PBC.MODEL_FILE_MAX)
    put_model(root, "f16384.json", body)
    check_eq("K15 model file AT 16384 bytes is read", PBC.load_model(task_of(root), "work/probe-models/f16384.json",
                                                                     "TC-001:ALT-1")["replace"], "x")
    put_model(root, "f16385.json", body + " ")
    try:
        PBC.load_model(task_of(root), "work/probe-models/f16385.json", "TC-001:ALT-1")
        got = "accepted"
    except PBC.Refusal as exc:
        got = "refused" if "16384" in str(exc) else "wrong"
    check_eq("K15 model file 16385 bytes: refused naming the limit", got, "refused")
    put_model(root, "m.json", MODEL)
    before = snapshot(root)
    for count, ok in ((300, True), (301, False)):
        proc, got = alt(root, stub, "test_weak", extra=("--supersede", "s" * count), env=env)
        check_eq(f"K15 --supersede {count} characters", proc.returncode != 2, ok)
    # an alternative with replace "" is stopped by the guards, not by the length rule
    put_model(root, "del.json", dict(MODEL, find="stamp = read_stamp()", replace=""))
    proc, got = alt(root, stub, "test_strong", model="del.json", env=env)
    check_eq("K15 a deletion of the value is a model like another: the assert then fails by a NameError, wrong_location",
             (proc.returncode, got.get("verdict")), (0, "wrong_location"))
    del before


def k16_encoding(root: Path, stub: Path) -> None:
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    path = task_of(root) / "work" / "probe-models" / "bom.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\xef\xbb\xbf" + json.dumps(MODEL).encode("utf-8"))
    proc, got = alt(root, stub, "test_strong", model="bom.json", env=env)
    check_eq("K16 a model with a BOM is read", (proc.returncode, got.get("verdict")), (0, "intended_failure"))
    # non-ASCII find in a UTF-8 test; a 2-line -> 2-line find inside parentheses
    text = (root / STAMP_REL).read_bytes().decode("utf-8")
    text += ('\n\ndef test_unicode():\n    stamp = read_stamp()  # éè\n    label = ("été",\n             read_stamp())\n'
             '    assert label[1] <= T_DONE - TOLERANCE, "Then 2: unicode"\n')
    (root / STAMP_REL).write_bytes(text.encode("utf-8"))
    manifest = task_of(root) / "work" / "automation-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["tests"].append(entry("test_unicode"))
    data["then_bindings"].append({"case": "TC-001", "then": 2, "instance_id": "test_unicode", "status": "covered",
                                  "assertion_ref": f"{STAMP_REL}:{assert_line(text, 'test_unicode')}"})
    write_json(manifest, data)
    put_model(root, "u.json", dict(MODEL, find='("été",\n             read_stamp())',
                                   replace='("été",\n             T_DONE)'))
    proc, got = alt(root, stub, "test_unicode", model="u.json", env=env)
    check("K16 a non-ASCII 2-line find inside parentheses works (the model is read, planned and run: not refused)",
          got.get("status") != "refused" and got.get("model_find") is not None, str(got)[:300])
    check_eq("K16 ... and the author's bytes are back", (root / STAMP_REL).read_bytes(), text.encode("utf-8"))
    # CRLF test, LF find
    crlf = text.replace("\n", "\r\n")
    (root / STAMP_REL).write_bytes(crlf.encode("utf-8"))
    put_model(root, "lf.json", dict(MODEL, find="stamp = read_stamp()\n    update_date", replace="stamp = T_DONE\n    update_date"))
    proc, got = alt(root, stub, "test_weak", model="lf.json", env=env)
    check_eq("K16 CRLF test with an LF `find`: refused", (proc.returncode, got.get("status")), (2, "refused"))
    check_in("K16 and the text names CRLF", "CRLF", got.get("error", ""))
    (root / STAMP_REL).write_bytes(STAMP.encode("utf-8"))


def k17_judge_table() -> None:
    spans = [(10, 10)]
    spec = {"file": STAMP_REL}
    at = f"{STAMP_REL}:10"
    ok = (True, "")

    def judged(label: str, observed: dict, green, reach, want: str) -> None:
        verdict = PBC.judge_alternative(observed, spans, green, reach, spec)[0]
        check_eq(f"K17 {label}", verdict, want)

    judged("passed, green, reach -> no_failure", {"status": "passed"}, True, ok, "no_failure")
    judged("passed, green, reach NOT shown -> incomplete (K24)", {"status": "passed"}, True, (False, "after"), "incomplete")
    judged("a5 passed, author red -> incomplete", {"status": "passed"}, False, ok, "incomplete")
    judged("passed, author unknown -> incomplete", {"status": "passed"}, None, ok, "incomplete")
    judged("failed by assertion at the Then, green -> intended_failure",
           {"status": "failed", "failure_kind": "assertion", "location": at}, True, ok, "intended_failure")
    judged("the same, author red -> incomplete", {"status": "failed", "failure_kind": "assertion", "location": at}, False, ok,
           "incomplete")
    judged("the same, author unknown -> incomplete", {"status": "failed", "failure_kind": "assertion", "location": at}, None,
           ok, "incomplete")
    judged("the frame inside the span (a library tail) -> intended_failure",
           {"status": "failed", "failure_kind": "assertion", "location": "lib/h.py:3", "test_file_frame": at}, True, ok,
           "intended_failure")
    judged("a1 a TypeError at/before the assert -> wrong_location",
           {"status": "failed", "failure_kind": "exception", "location": f"{STAMP_REL}:9"}, True, ok, "wrong_location")
    judged("a TypeError AT the assert line -> wrong_location (not an assertion)",
           {"status": "failed", "failure_kind": "exception", "location": at}, True, ok, "wrong_location")
    judged("a2 another assert fires -> wrong_location", {"status": "failed", "failure_kind": "assertion",
                                                         "location": f"{STAMP_REL}:20"}, True, ok, "wrong_location")
    judged("failed, no location read -> incomplete", {"status": "failed", "failure_kind": "assertion"}, True, ok, "incomplete")
    judged("error status -> incomplete", {"status": "error"}, True, ok, "incomplete")
    judged("skipped -> not_executed", {"status": "skipped"}, True, ok, "not_executed")
    judged("a location in ANOTHER file at the same number -> wrong_location",
           {"status": "failed", "failure_kind": "assertion", "location": "tests/other.py:10"}, True, ok, "wrong_location")


def k18_author_unknown(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    bound = PBC.author_binding(task_of(root), "test_strong", C.load_json(task_of(root) / "work" / "run-blocks"
                                                                             / "20260924T090000000000Z-author1.json")
                               ["results"][1]["instance_content_sha"])
    check_eq("K18 author_binding returns the row's status", (bound or {}).get("status"), "passed")
    # a red author row -> False -> incomplete even though the model fails at the assert
    block = task_of(root) / "work" / "run-blocks" / "20260924T090000000000Z-author1.json"
    data = json.loads(block.read_text(encoding="utf-8"))
    for row in data["results"]:
        if row["instance_id"] == "test_strong":
            row["status"] = "failed"
    write_json(block, data)
    proc, got = alt(root, stub, "test_strong")
    check_eq("K18 a red author row + a failing run -> incomplete, never intended_failure", (proc.returncode, got.get("verdict")),
             (1, "incomplete"))
    check_eq("K18 author_green False", got.get("author_green"), False)
    block.unlink()
    proc, got = alt(root, stub, "test_strong")
    check_eq("K18 no run block at all -> author_green None -> incomplete", (got.get("verdict"), got.get("author_green")),
             ("incomplete", None))


def k19_repeat_and_supersede(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    proc, first = alt(root, stub, "test_strong", env=env)
    check_eq("K19 first probe", first.get("verdict"), "intended_failure")
    proc, again = alt(root, stub, "test_strong", env=env)
    check_eq("K19 a second identical call: already_probed, exit 0", (proc.returncode, again.get("verdict")), (0, "already_probed"))
    check_eq("K19 ... the stub log holds ONE line", stub_log_lines(root), 1)
    check_in("K19 the answer names the door", "--supersede", again.get("words", ""))
    proc, third = alt(root, stub, "test_strong", env=env, extra=("--supersede", "wrong seam"))
    check_eq("K19 --supersede runs again", (proc.returncode, third.get("verdict"), stub_log_lines(root)),
             (0, "intended_failure", 2))
    sup = third.get("superseded") or []
    check_eq("K19 the new record holds the old verdict with the reason", [(s.get("verdict"), s.get("reason")) for s in sup],
             [("intended_failure", "wrong seam")])
    rows = report(root, stub)
    check_eq("K20 the report shows `superseded: 1 (prior: intended_failure)`", row_of(rows, "test_strong").get("superseded"),
             ["intended_failure"])


def k20_report(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    alt(root, stub, "test_strong")
    alt(root, stub, "test_weak")
    put_model(root, "g.json", {"alternative": "TC-001:ALT-1", "gap": "the stamp is read inside the product"})
    alt(root, stub, "test_both", model="g.json")
    rows = report(root, stub)
    strong, weak, both, never = (row_of(rows, i) for i in ("test_strong", "test_weak", "test_both", "test_untaken"))
    check_eq("K20 proven", strong.get("state"), "proven")
    check_eq("K20 the proven row prints the model", (strong.get("model_find"), strong.get("model_replace")),
             ("stamp = read_stamp()", "stamp = T_DONE"))
    check_eq("K20 not_separated, WITH the model beside it (B-3)", (weak.get("state"), weak.get("model_find")),
             ("not_separated", "stamp = read_stamp()"))
    check_eq("K20 gap", both.get("state"), "gap")
    check_eq("K20 unknown: declared, never probed", never.get("state"), "unknown")
    check_in("K20 the unknown row carries the flags to add", "--mutation alternative --alternative TC-001:ALT-1 --model "
             "work/probe-models/<any name>.json", never.get("flags", ""))
    check_in("K20 and the model skeleton", '"find"', never.get("skeleton", ""))
    proc = run_script("probe_by_code.py", "--task", TASK, "--alternatives", cwd=root, env=env_for(root, stub))
    check_in("K20 the human line: <instance> <case>:<ALT> Then <n>: <state> - <why>", "test_strong TC-001:ALT-1 Then 2: proven",
             proc.stdout)
    check_in("K20 the human line carries `model:` beside proven", "model: stamp = read_stamp() -> stamp = T_DONE", proc.stdout)
    # a case without the key -> no row; a malformed key -> case_unreadable
    case1 = task_of(root) / "work" / "test-cases" / "TC-001.md"
    case2 = task_of(root) / "work" / "test-cases" / "TC-002.md"
    case1.write_text(case_text("TC-001", None), encoding="utf-8")
    case2.write_text(case_text("TC-002", "not json"), encoding="utf-8")
    rows = report(root, stub)
    check("K20 a case without the key has no row", not [r for r in rows if r["case"] == "TC-001"], str(rows))
    check_eq("K20 a malformed key is case_unreadable (never 'nothing owed')",
             [r["state"] for r in rows if r["case"] == "TC-002"], ["case_unreadable"])
    # a story with no models and no records prints unknown for the owed rows, no error
    case1.write_text(case_text("TC-001"), encoding="utf-8")
    case2.write_text(case_text("TC-002"), encoding="utf-8")


def k24_reach(root: Path, stub: Path) -> None:
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    for label, iid, doc in (
            ("a model in an untaken branch", "test_untaken", dict(MODEL, find="marker = read_stamp()", replace="marker = T_DONE")),
            ("a model naming a helper the test never calls", "test_strong", dict(MODEL, function="unused")),
            ("a model AFTER the assert", "test_after", dict(MODEL, find="later = read_stamp()", replace="later = T_DONE")),
            ("a model inside a nested def", "test_nested", dict(MODEL, find="return read_stamp()", replace="return T_DONE"))):
        put_model(root, "k24.json", doc)
        proc, got = alt(root, stub, iid, model="k24.json", env=env)
        check_eq(f"K24 {label}: a pass is incomplete (reach), never no_failure", (proc.returncode, got.get("verdict")),
                 (1, "incomplete"))
        check_in(f"K24 {label}: the reach reason is said", "reach", " ".join(got.get("mismatches") or []))
        check_eq(f"K24 {label}: the bytes are back", stat_text(root), STAMP.encode("utf-8"))
    # the reach rule itself, pure
    import ast
    text = STAMP.encode("utf-8")
    tree = ast.parse(text.decode("utf-8"))
    func = PBC.locate(tree, [], "test_weak")
    starts = PBC._line_starts(text)
    idx = text.index(b"stamp = read_stamp()", text.index(b"def test_weak"))
    check_eq("K24 pure: the straight-line model reaches the assert", PBC.model_reach(
        func, (idx, idx + 20), [(assert_line(STAMP, "test_weak"),) * 2], starts)[0], True)
    check_eq("K24 pure: a model on another statement's line range after the assert does not", PBC.model_reach(
        func, (idx, idx + 20), [(func.lineno + 1,) * 2], starts)[0], False)


def k25_two_cases(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    proc, got = alt(root, stub, "test_both")
    check_eq("K25 TC-001:ALT-1 of the two-case instance is proven", got.get("verdict"), "intended_failure")
    rows = report(root, stub)
    check_eq("K25 the unmodelled case's row is unknown", row_of(rows, "test_both", "TC-002:ALT-1").get("state"), "unknown")
    p1 = PBC.alternative_record_path(task_of(root), "test_both", "TC-001", "ALT-1")
    p2 = PBC.alternative_record_path(task_of(root), "test_both", "TC-002", "ALT-1")
    check("K25 the two records live at different paths", p1 != p2 and p1.is_file() and not p2.exists())
    p2.write_bytes(p1.read_bytes())
    rows = report(root, stub)
    check_eq("K25 a record copied over TC-002's path keeps its `case` field: unknown (names another case)",
             row_of(rows, "test_both", "TC-002:ALT-1").get("state"), "unknown")
    check_in("K25 ... and says so", "another case", row_of(rows, "test_both", "TC-002:ALT-1").get("why", ""))


def k26_stale(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    alt(root, stub, "test_strong", env=env)
    check_eq("K26 proven first", row_of(report(root, stub), "test_strong").get("state"), "proven")
    original = stat_text(root)
    # (d) a neighbour's comment-only edit keeps it proven (the per-test identity is equal)
    (root / STAMP_REL).write_bytes(original.replace(b"def unused():", b"# a neighbour's comment\ndef unused():"))
    # lines moved by one: re-bind the Then and re-measure through the author's job is the author's move; the identity of the
    # test is what is under test here, so the binding is rewritten and the raw sha differs while the per-test one may not
    (root / STAMP_REL).write_bytes(original)
    # (a) the test function's bytes change (a weakened assert)
    (root / STAMP_REL).write_bytes(original.replace(b"T_DONE - TOLERANCE, \"Then 2: the stamp is the trigger",
                                                    b"T_DONE + TOLERANCE, \"Then 2: the stamp is the trigger", 1))
    check_eq("K26 (a) the test's bytes changed -> stale, never proven", row_of(report(root, stub), "test_strong").get("state"),
             "stale")
    (root / STAMP_REL).write_bytes(original)
    check_eq("K26 restored bytes -> proven again", row_of(report(root, stub), "test_strong").get("state"), "proven")
    # (b) the case's reading changes
    case1 = task_of(root) / "work" / "test-cases" / "TC-001.md"
    text = case1.read_text(encoding="utf-8")
    case1.write_text(text.replace("taken at completion", "taken at the end of the run"), encoding="utf-8")
    check_eq("K26 (b) the reading changed -> stale", row_of(report(root, stub), "test_strong").get("state"), "stale")
    case1.write_text(text, encoding="utf-8")
    # (c) the Then is rebound to another assert line
    manifest = task_of(root) / "work" / "automation-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    saved = json.dumps(data)
    for row in data["then_bindings"]:
        if row["instance_id"] == "test_strong":
            row["assertion_ref"] = f"{STAMP_REL}:12"
    write_json(manifest, data)
    check_eq("K26 (c) the Then is rebound -> stale", row_of(report(root, stub), "test_strong").get("state"), "stale")
    manifest.write_text(saved, encoding="utf-8")
    # a stale record does not answer already_probed: the probe runs again
    (root / STAMP_REL).write_bytes(original.replace(b"T_DONE - TOLERANCE, \"Then 2: the stamp is the trigger",
                                                    b"T_DONE - TOLERANCE - 1.0, \"Then 2: the stamp is the trigger", 1))
    proc, got = alt(root, stub, "test_strong", env=env)
    check_eq("K26 a stale record does not answer already_probed: it ran again (the author's green is for the OLD bytes: incomplete)",
             (got.get("verdict"), stub_log_lines(root)), ("incomplete", 2))
    check_eq("K26 ... and the replaced record is kept in superseded[] with its stale reason",
             [str(s.get("reason")).startswith("stale:") for s in got.get("superseded") or []], [True])
    (root / STAMP_REL).write_bytes(original)
    # m-4: a gap goes stale too
    put_model(root, "g.json", {"alternative": "TC-001:ALT-1", "gap": "cannot model it"})
    alt(root, stub, "test_untaken", model="g.json")
    check_eq("K26 a gap is a gap while the reading and the test stand", row_of(report(root, stub), "test_untaken").get("state"), "gap")
    case1.write_text(text.replace("taken at completion", "taken at some other time"), encoding="utf-8")
    check_eq("K26 m-4 a gap goes stale when the reading changes", row_of(report(root, stub), "test_untaken").get("state"), "stale")
    case1.write_text(text, encoding="utf-8")


def k27_helper_assert(root: Path, stub: Path) -> None:
    put_model(root, "m.json", MODEL)
    manifest = task_of(root) / "work" / "automation-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["tests"].append(entry("test_helper"))
    data["then_bindings"].append({"case": "TC-001", "then": 2, "instance_id": "test_helper", "status": "covered",
                                  "assertion_ref": "tests/helpers.py:2"})
    write_json(manifest, data)
    before = snapshot(root)
    proc, got = alt(root, stub, "test_helper")
    check_eq("K27 the assertion lives in a helper: unknown, naming the helper, nothing written",
             (proc.returncode, got.get("verdict"), snapshot(root)), (1, "unknown", before))
    check_in("K27 the helper is named", "tests/helpers.py:2", got.get("why", ""))


def k28_target_lock(root: Path, stub: Path) -> None:
    """A model `function` in another file under the test root takes that file's lock and restores a dead probe's copy of it BEFORE
    its bytes are read as the original."""
    helper = root / "tests" / "helpers.py"
    put_model(root, "h.json", dict(MODEL, function="tests/helpers.py::reader", find="return 100.5", replace="return 160.0"))
    original = helper.read_bytes()
    killed = original.replace(b"100.5", b"160.0")
    key, shown = PBC.copy_key(helper, root)
    directory = PBC.copy_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    orig, meta = PBC.copy_files(directory, key)
    orig.write_bytes(original)
    write_json(meta, {"path": shown, "original_sha": PBC.sha256(original), "mutated_sha": PBC.sha256(killed),
                      "original_mtime_ns": helper.stat().st_mtime_ns, "started_at": "2026-09-24T09:00:00+00:00",
                      "timeout_s": 60, "statement_before": "return 100.5", "statement_after": "return 160.0", "line": 2})
    helper.write_bytes(killed)                    # a dead probe left the helper mutated, with its copy on disk
    proc, got = alt(root, stub, "test_strong", model="h.json")
    check_eq("K28 the dead probe's copy of the helper was restored before the probe read it as the original",
             (helper.read_bytes(), (got.get("mutated_file") or {}).get("sha256")), (original, PBC.sha256(original)))
    check_eq("K28 the model landed in the helper and the helper's bytes are back", (got.get("mutated_file") or {}).get("path"),
             "tests/helpers.py")


def k29_k30_exit_and_print(root: Path) -> None:
    """B-2: the exit and print paths read the alternative record without an exception, and an unverified restore of a HELPER
    target names the helper. `probe` is replaced by records, so the branch no stub run reaches is pinned too."""
    mark_project(root)
    use_project(root)
    argv = ["--task", TASK, "--dispatch", DISPATCH, "--test", f"{STAMP_REL}::test_strong", "--instance", "test_strong",
            "--mutation", "alternative", "--alternative", "TC-001:ALT-1", "--model", "work/probe-models/m.json"]
    full = {"instance_id": "test_strong", "alternative": "TC-001:ALT-1", "verdict": "intended_failure", "why": "",
            "expected_location": f"{STAMP_REL}:20", "expected_reason": "alternative TC-001:ALT-1",
            "actual_location": f"{STAMP_REL}:20", "actual_reason": "AssertionError: m", "record": "work/probes/alternative/x.json",
            "evidence_ref": "evidence/e.json", "restore": {"verified": True}, "notes": ["n1"],
            "test_node": f"{STAMP_REL}::test_strong", "test_file_sha256": "f" * 64,
            "mutated_file": {"path": STAMP_REL, "sha256": "a" * 64}}
    answers = {"unknown": {"verdict": "unknown", "instance_id": "test_strong", "alternative": "TC-001:ALT-1", "why": "a why",
                           "notes": []},
               "gap": {"verdict": "gap", "instance_id": "test_strong", "alternative": "TC-001:ALT-1", "why": "a gap",
                       "record": "work/probes/alternative/x.json", "door": "red_sandbox.py --probe", "notes": ["n"],
                       "restore": None},
               "already_probed": {"verdict": "already_probed", "instance_id": "test_strong", "alternative": "TC-001:ALT-1",
                                  "words": "already probed", "notes": []},
               "intended_failure": full}
    wanted = {"unknown": 1, "gap": 1, "already_probed": 0, "intended_failure": 0}
    for name, record in answers.items():
        for extra in ((), ("--json",)):
            code, log = _main_in_process(argv + list(extra), dict(record, notes=list(record.get("notes") or [])))
            out, err = _streams(log)
            check_eq(f"K30 {name} {'--json' if extra else 'text'}: exit {wanted[name]}, prints, no exception, never published",
                     (code, bool(out.strip()), "Traceback" in err, "publish" in _calls(log)),
                     (wanted[name], True, False, False))
    # K29: an unverified restore with a helper target prints the helper's path and exits 1 with no traceback
    helper = dict(full, restore={"verified": False, "copy": "qa-factory/state/probe-copies/k.orig"},
                  mutated_file={"path": "tests/helpers.py", "sha256": "b" * 64})
    code, log = _main_in_process(argv, helper)
    out, err = _streams(log)
    check_eq("K29 an unverified restore of a helper target: exit 1, the HELPER is named, not the test",
             (code, "tests/helpers.py" in err, "Traceback" in err, "publish" in _calls(log)), (1, True, False, False))
    check_in("K29 the undo names the copy over the helper", "tests", err.split("stop and")[-1] if "stop and" in err else err)


def k31_value_equivalent(root: Path, stub: Path) -> None:
    """B-3: a model that changes code but not the value is `unknown` with the model named, never `no_failure` (never test_defect)."""
    env = {"PROBE_STUB_LOG": str(root / "stub.log")}
    for replace in ("stamp = read_stamp() + 0", "stamp = (read_stamp()) * 1", "stamp = +read_stamp()"):
        put_model(root, "eq.json", dict(MODEL, replace=replace))
        before = snapshot(root)
        proc, got = alt(root, stub, "test_weak", model="eq.json", env=env)
        check_eq(f"K31 {replace!r}: exit 1, unknown (the critic's non-model)", (proc.returncode, got.get("verdict")), (1, "unknown"))
        check_in(f"K31 {replace!r}: the model is named", "stamp = read_stamp()", got.get("why", ""))
        check_eq(f"K31 {replace!r}: nothing ran, nothing was written", (snapshot(root), stub_log_lines(root)), (before, 0))
    check_eq("K31 pure: a real change is a change", PBC.model_changes_value(MODEL)[0], True)
    check_eq("K31 pure: an unparsable pair is taken as a change", PBC.model_changes_value({"find": "x = (", "replace": "x = 1"})[0],
             True)


def k23_record_path() -> None:
    task = Path("T")
    check_eq("K23 kind alternative", PL.probe_record_path(task, "i--TC-1--ALT-1", kind="alternative"),
             task / "work" / "probes" / "alternative" / "i--TC-1--ALT-1.json")
    check_eq("K23 kind product unchanged", PL.probe_record_path(task, "i", kind="product"), task / "work" / "probes" / "product" / "i.json")
    check_eq("K23 kind empty unchanged", PL.probe_record_path(task, "i"), task / "work" / "probes" / "i.json")
    check_eq("K23 a qualified case is one file name", PBC.alternative_record_path(task, "i", "feedback-api/TC-3", "ALT-1").name,
             "i--feedback-api-TC-3--ALT-1.json")


def main() -> None:
    k17_judge_table()
    k23_record_path()
    for body in (k10_the_pair, k11_no_live_receipt, k12_unknown_answers, k13_k21_gaps, k14_refusals, k15_limits, k16_encoding,
                 k18_author_unknown, k19_repeat_and_supersede, k20_report, k24_reach, k25_two_cases, k26_stale,
                 k27_helper_assert, k28_target_lock, k31_value_equivalent):
        with_stub(body)
    root = alt_project()
    try:
        k29_k30_exit_and_print(root)
    finally:
        cleanup(root)
        cleanup_beside(root)
    finish("test_probe_by_code_alternative")


if __name__ == "__main__":
    main()
