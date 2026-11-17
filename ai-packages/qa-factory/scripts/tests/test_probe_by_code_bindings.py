"""bindings: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir
sys.path.insert(0, str(SCRIPTS))
import probe_by_code as PBC  # noqa: E402
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from probe_by_code_common import DISPATCH, PY, TASK, TEST_FILE_REL, cleanup_beside, project  # noqa: E402


def the_author_binding_is_the_latest_block_by_the_clock() -> None:
    """t-149 F-order: `author_binding` reads the blocks in the story's one order (the block's own clock, a
    reparse right after the block it supersedes), not file-name order: the reparse of an OLD attempt whose id
    starts with a letter sorts after every `2026...` block by name and used to be 'the latest' block."""
    task = temp_dir("qa-probe-binding-order-")
    try:
        runs = task / "work" / "run-blocks"
        runs.mkdir(parents=True)

        def block(name: str, attempt: str, started: str, test_sha: str, **extra) -> None:
            row = {"instance_id": "t[p]", "instance_content_sha": "fn-sha",
                   "source_fingerprint": {"test_content_sha": test_sha}}
            (runs / name).write_text(json.dumps({
                "attempt_id": attempt, "block_id": attempt, "attempt_started_at": started,
                "dispatch_id": "D-" + attempt, "results": [row], **extra}), encoding="utf-8")
        first = "20260930T050000000000Z-f302aa.json"
        block(first, "f302aa", "2026-09-30T05:00:00+00:00", "sha-old")
        block("20260930T051000000000Z-b2bb.json", "b2bb", "2026-09-30T05:10:00+00:00", "sha-new")
        block("f302aa-reparse-0123.json", "f302aa", "2026-09-30T05:00:00+00:00", "sha-old-reparse",
              reparse_of="work/run-blocks/" + first, supersedes_block_id="f302aa")
        got = PBC.author_binding(task, "t[p]", "fn-sha")
        check_eq("F-order: the latest block that ran this very function is the later ATTEMPT's, not the old "
                 "attempt's reparse (which sorts last by file name)",
                 got, {"run_block": "work/run-blocks/20260930T051000000000Z-b2bb.json",
                       "test_content_sha": "sha-new", "dispatch_id": "D-b2bb", "status": None})   # TQ1-25: the row's own status rides along
        check_eq("an empty function sha binds nothing", PBC.author_binding(task, "t[p]", ""), None)
        check_eq("a sha no block ran binds nothing", PBC.author_binding(task, "t[p]", "other"), None)
        check_eq("an instance no block ran binds nothing", PBC.author_binding(task, "other[p]", "fn-sha"), None)
        (runs / "20260930T052000000000Z-bad.json").write_text("{not json", encoding="utf-8")
        check_eq("an unreadable block is skipped, as before", PBC.author_binding(task, "t[p]", "fn-sha")["test_content_sha"],
                 "sha-new")
    finally:
        cleanup(task)


def n2_k7_the_red_probe_reads_the_stand_as_the_run_does() -> None:
    """K-N2.7 (t-300 N2, S8): `probe_by_code.probe_runtime` is a delegate of `run_suite.probe_runtime`: ONE reader, ONE exception
    class, ONE message. It held a copy that took `matched` only, so a person's word reached the role's own `--mine` and not the
    critic's red probe, and a probe that compared nothing (`no_changed_file`) was refused here and taken there (B-255 a)."""
    import run_suite
    from execution_request import ProvenanceRefused
    work = temp_dir("qa-probe-n2-k7-")
    try:
        head = "a" * 40
        image = "image:sha256:" + "b" * 64
        base = {"profile_id": "api", "timestamp": "2026-10-02T12:00:00+00:00", "environment_id": "localhost",
                "expected_source_revision": head, "observed_runtime_identity": image, "evidence_refs": ["probe/x"],
                "result": "matched", "provenance": {"technical_verification": True, "source_linkage": "exact",
                                                    "deployed_source_revision": head}}
        shapes = {
            "M": base,
            "NA1": {**base, "result": "not_applicable", "observed_runtime_identity": "", "evidence_refs": [], "provenance": {},
                    "reason_code": "no_changed_file"},
            "PC": {**base, "result": "person_confirmed", "evidence_refs": ["probe/pc"],
                   "provenance": {"technical_verification": False, "identity_kind": "person_confirmed"},
                   "person_confirmation": {"words": "yes", "at": "2026-10-02T11:00:00+00:00", "task": "T-1", "kind": "deployed",
                                           "revision": head}},
            "U": {**base, "result": "unknown", "evidence_refs": [], "provenance": {"technical_verification": False},
                  "error": "which build the stand runs could not be read", "remedy": "tell me how to read it", "asks_person": "how"},
            "MM": {**base, "result": "mismatched", "provenance": {**base["provenance"], "deployed_source_revision": "d" * 40}},
            "NA2": {**base, "result": "not_applicable", "observed_runtime_identity": "", "evidence_refs": [], "provenance": {}}}

        def read(reader, shape):
            script = work / f"probe-{shape}.py"
            script.write_text("import json; print(json.dumps(" + repr(shapes[shape]) + "))", encoding="utf-8")
            try:
                return "returned", reader({"argv": [PY, str(script)], "cwd": str(work), "timeout_s": 30})["result"]
            except Exception as exc:  # the class and the text are what is compared
                return type(exc).__name__, str(exc)
        for shape in shapes:
            mine, theirs = read(PBC.probe_runtime, shape), read(run_suite.probe_runtime, shape)
            check_eq(f"K-N2.7 {shape}: the red probe's reader and the run's say the same thing (class and text)", mine, theirs)
        check_eq("K-N2.7 B-255 a: a probe that compared nothing (`no_changed_file`) is returned here too",
                 read(PBC.probe_runtime, "NA1"), ("returned", "not_applicable"))
        check_eq("K-N2.7: a person's word is returned (the role's `--mine` and the critic's probe agree)",
                 read(PBC.probe_runtime, "PC"), ("returned", "person_confirmed"))
        check_eq("K-N2.7: an `unknown` raises ProvenanceRefused, with the probe's own words",
                 (read(PBC.probe_runtime, "U")[0], "which build the stand runs could not be read. tell me how to read it"
                  in read(PBC.probe_runtime, "U")[1]), (ProvenanceRefused.__name__, True))
        check_eq("K-N2.7 control: `matched` is returned as it always was", read(PBC.probe_runtime, "M"), ("returned", "matched"))
        check_eq("K-N2.7 control: NA without its reason code raises (it compared nothing and did not say why)",
                 read(PBC.probe_runtime, "NA2")[0], ProvenanceRefused.__name__)
        scripts = Path(PBC.__file__).resolve().parent
        mine_text = (scripts / "probe_by_code.py").read_text(encoding="utf-8")
        other = (scripts / "execution_request.py").read_text(encoding="utf-8")
        check("K-N2.7 source control: the same search shape finds a `validate_runtime_provenance(` call in execution_request.py",
              "validate_runtime_provenance(" in other)
        check("K-N2.7: and probe_by_code.py has none of its own (the copy is gone)", "validate_runtime_provenance(" not in mine_text)
    finally:
        cleanup(work)


def second_hop_name_in_two_files_is_refused() -> None:
    """t-2162 fix round: the B2 rule at the second hop - a name with a check in two files two hops away is refused, naming each file:line and
    the `--at` door (one helper, `_declared_in_files`); with ONE such file the refusal is the single-door one, as before."""
    root = temp_dir("qa-probe-second-hop-")
    try:
        (root / "tests").mkdir()
        (root / "tests" / "test_x.py").write_text("from helpers import shop\n\n\ndef test_x():\n    shop(1)\n", encoding="utf-8")
        (root / "tests" / "helpers.py").write_text("import page_a\nimport page_b\n\n\ndef shop(n):\n    verify(n)\n", encoding="utf-8")
        (root / "tests" / "page_a.py").write_text("def verify(n):\n    assert n == 1, 'a'\n", encoding="utf-8")
        (root / "tests" / "page_b.py").write_text("def verify(n):\n    assert n == 2, 'b'\n", encoding="utf-8")
        spec = PBC.parse_node("tests/test_x.py::test_x", root)
        path = root / spec["file"]
        text = path.read_text(encoding="utf-8")
        cfg = {"tests_root": "tests"}
        try:
            PBC.find_oracle(text, spec, path, root, [], None, cfg)
            check("second hop, two files: refused", False, "no refusal")
        except PBC.ToolRefusal as refusal:
            for word in ("tests/page_a.py", "tests/page_b.py", "--at <file>:<line>", "no body is mutated"):
                check_in(f"second hop, two files: the refusal says {word}", word, str(refusal))
        (root / "tests" / "page_b.py").write_text("def other(n):\n    pass\n", encoding="utf-8")
        try:
            PBC.find_oracle(text, spec, path, root, [], None, cfg)
            check("second hop, one file: refused", False, "no refusal")
        except PBC.ToolRefusal as refusal:
            check_in("second hop, one file: the single door is kept", "one hop further, in `verify`", str(refusal))
            check_not_in("second hop, one file: no two-file refusal", "no body is mutated", str(refusal))
    finally:
        cleanup(root)


B355_I_ROWS = [
    # (label, cfg, project-relative path, expected) - `_in_test_root` reads `roots.test` / `tests_root` through `is_test_path`
    ("World N: tests_root, a file under it", {"tests_root": "tests"}, "tests/x.py", True),
    ("World N: roots.test of a profile", {"profiles": [{"profile_id": "api", "roots": {"test": "backend/tests"}}]}, "backend/tests/a.py", True),
    ("World N: a path beside the root", {"tests_root": "tests"}, "src/x.py", False),
    ("World N: a usual test name alone (markers) never passes", {}, "src/test_x.py", False),
    ("World N: protected path wins over the root", {"tests_root": "tests", "protected_app_paths": ["tests"]}, "tests/x.py", False),
    ("World N: tests_root `.` is ignored (names the whole project)", {"tests_root": "."}, "src/x.py", False),
    ("World N: tests_root above the root is ignored", {"tests_root": ".."}, "src/x.py", False),
    ("World R: a test_locations entry alone does not pass", {"test_locations": ["src/legacy/checks"]}, "src/legacy/checks/a.py", False),
    ("World R: both carriers name the path -> True",
     {"test_locations": ["tests"], "tests_root": "tests"}, "tests/x.py", True),
    ("World R: protected wins over both carriers",
     {"test_locations": ["tests"], "tests_root": "tests", "protected_app_paths": ["tests"]}, "tests/x.py", False),
    ("World R: the record is kept, tests_root still recognises its place",
     {"test_locations": ["src/legacy/checks"], "tests_root": "tests"}, "tests/x.py", True),
    ("World R: the record is kept, a usual name outside it is not a test root",
     {"test_locations": ["src/legacy/checks"], "tests_root": "tests"}, "src/test_x.py", False),
    ("World R: an absolute path is refused first", {"tests_root": "tests"}, "/tests/x.py", False),
    ("World R: a path that climbs out is refused first", {"tests_root": "tests"}, "../tests/x.py", False),
]


def b355_i_in_test_root_reads_the_one_reader() -> None:
    """B-355 node I: `_in_test_root` answers through `test_locations.is_test_path` (`by == "config"`, source `roots.test` /
    `tests_root`); one table, the label names the row."""
    for label, cfg, rel, expected in B355_I_ROWS:
        check_eq(f"B355-I {label}", PBC._in_test_root(cfg, rel), expected)


OF4_6_ROOTS = ["tests", "./tests/", ".", "..", "../x", "", "/srv/tests", "/tests"]


OF4_6_PATHS = ["tests/a.py", "a.py", "x/tests/a.py"]


def of4_6_expected(root: str, rel: str) -> bool:
    """The requirement, not the code: a root names a folder INSIDE the project; `.` (the whole project), a root above it,
    an empty one and an absolute one own nothing (refusal only toward False). Under a real root a path is owned if it is
    that folder or lies in it, and only then."""
    if root in ("tests", "./tests/"):
        return rel.startswith("tests/")
    return False


def of4_6_profiles_owning_and_in_test_root_agree() -> None:
    """OF4-6: `execution_request.profiles_owning` (reads `roots.test` itself) and `probe_by_code._in_test_root` (through
    `test_locations`) give ONE answer for every root x path of the table; the expectation is the requirement above."""
    import execution_request as ER
    for root in OF4_6_ROOTS:
        cfg = {"profiles": [{"profile_id": "api", "roots": {"test": root}}]}
        for rel in OF4_6_PATHS:
            want = of4_6_expected(root, rel)
            check_eq(f"OF4-6 root {root!r} path {rel!r}: _in_test_root", PBC._in_test_root(cfg, rel), want)
            check_eq(f"OF4-6 root {root!r} path {rel!r}: profiles_owning", bool(ER.profiles_owning(cfg, rel)), want)


def _rec(n: int):
    import detector_verdict as DV
    return DV.Record(f"problem {n}", check=f"execution_request:k10p{n}", expected=f"Sentence {n}.", door=f"door {n}")


# K10p/pbc-told/<printer>/<case>: the records of a refusal -> the checks the printed JSON's `told` holds (every distinct one, in order)
PBC_TOLD_CASES = {"one-record": ([1], [1]), "two-records": ([1, 2], [1, 2]), "repeated-check": ([1, 2, 1], [1, 2])}


PBC_PRINTERS = ("plan", "tool", "refusal")


def _printed_json(printer: str, exc: Exception) -> dict:
    """Raise `exc` into the real one-JSON printer of `printer` (`_plan_cli`, and `main`'s ToolRefusal / Refusal handlers) and parse
    the one line it prints. The raise sits where the printer's own `try` reads the story, so nothing else of the call runs."""
    import contextlib
    import io

    def boom(*_a, **_k):
        raise exc
    names = {"plan": ("parse_node", ["--plan", "--task", TASK, "--instance", "test_add", "--test", f"{TEST_FILE_REL}::test_add"]),
             "tool": ("probe", ["--task", TASK, "--dispatch", DISPATCH, "--test", f"{TEST_FILE_REL}::test_add", "--instance", "test_add"]),
             "refusal": ("probe", ["--task", TASK, "--dispatch", DISPATCH, "--test", f"{TEST_FILE_REL}::test_add", "--instance", "test_add"])}
    target, argv = names[printer]
    saved = {name: getattr(PBC, name) for name in (target, "story_root", "project_root", "artifacts_dir", "load_config",
                                                   "_record_tool_refusal")}
    saved_argv = sys.argv
    PBC.story_root = lambda *a, **k: Path(".")
    PBC.project_root = lambda *a, **k: Path(".")
    PBC.artifacts_dir = lambda *a, **k: Path(".")
    PBC.load_config = lambda *a, **k: {}
    PBC._record_tool_refusal = lambda *a, **k: None
    setattr(PBC, target, boom)
    sys.argv = ["probe_by_code.py", *argv]
    out = io.StringIO()
    code = None
    try:
        with contextlib.redirect_stdout(out):
            try:
                PBC.main()
            except SystemExit as stop:
                code = stop.code
    finally:
        sys.argv = saved_argv
        for name, value in saved.items():
            setattr(PBC, name, value)
    check_eq(f"K10p/pbc-told/{printer}: exit 2, one line", (code, len(out.getvalue().strip().splitlines())), (2, 1))
    return json.loads(out.getvalue().strip().splitlines()[-1])


def k10p_pbc_told_is_printed() -> None:
    """K10p/pbc-told: a pre-action `Refusal` / `ToolRefusal` carrying records reaches the one-JSON printer with EVERY distinct check in
    `told` (`told_fields`, the one builder), in order, `error` unchanged. The proof a later card (K1b) reads before it moves a row off
    the page for the probe road: a row is carried by these printers only."""
    for printer in PBC_PRINTERS:
        for case, (given, wanted) in PBC_TOLD_CASES.items():
            cls = PBC.ToolRefusal if printer == "tool" else PBC.Refusal
            got = _printed_json(printer, cls("probe_by_code: refused for the table", *[_rec(n) for n in given]))
            check_eq(f"K10p/pbc-told/{printer}/{case}: status, error unchanged, every distinct check in order",
                     (got.get("status"), got.get("error"), [e.get("check") for e in got.get("told", [])]),
                     ("refused", "probe_by_code: refused for the table", [_rec(n).check for n in wanted]))
    # one row per execution_request id a pre-action Refusal of probe_by_code cites, provoked through its real function
    root = project()
    try:
        cfg = {"profiles": [{"profile_id": "unit", "roots": {"test": "tests"}}]}
        for label, fn, rid in (
                ("_profile_cwd", lambda: PBC._profile_cwd(cfg, TEST_FILE_REL, "nope"), "execution_request:profile"),
                ("_dispatch_context", lambda: PBC._dispatch_context(root, TASK, root / "qa-factory" / "artifacts" / TASK,
                                                                    "S5-qa-code-critic-9", "TC-100", False),
                 "execution_request:active_dispatch")):
            try:
                fn()
                exc = None
            except PBC.Refusal as stop:
                exc = stop
            check_eq(f"K10p/pbc-told/{rid}/{label}: a pre-action Refusal that carries the row, printed by the refusal printer",
                     (exc is not None and [r.check for r in exc.records] == [rid]) and
                     [e.get("check") for e in _printed_json("refusal", exc).get("told", [])], [rid])
    finally:
        cleanup(root)
        cleanup_beside(root)


def main() -> None:
    k10p_pbc_told_is_printed()
    of4_6_profiles_owning_and_in_test_root_agree()
    b355_i_in_test_root_reads_the_one_reader()
    second_hop_name_in_two_files_is_refused()
    n2_k7_the_red_probe_reads_the_stand_as_the_run_does()
    the_author_binding_is_the_latest_block_by_the_clock()
    finish("test_probe_by_code_bindings")


# split: runner piece 1
if __name__ == "__main__":
    main()
