"""two profiles: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir
sys.path.insert(0, str(SCRIPTS))
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from probe_by_code_common import (  # noqa: E402
    FAKE_RUN_SUITE, TASK, TEST_FILE_REL, cleanup_beside, project, run,
)


def two_profiles_over_one_root(stub: Path) -> None:
    """EP1-16 (A-K4, A-K5): the 12586 shape - profiles `unit` and `ui` over one `tests/` root and one cwd. The probe
    used to hand the builder no profile, so a row that NAMED `unit` still met "profiles share the test root" and the
    mutation probe never ran. Now the row's profile reaches the builder (A-K1) and the probe runs and judges; a row
    that names none is still refused, not run under the first profile, and the refusal names the row door only -
    this tool has no `--profile` (FR-2)."""
    root = project(shared_second=True, row_profile="unit")
    try:
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        check("A-K4 two profiles, the row names `unit`: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        check_eq("A-K4 the probe is built, run and judged: intended_failure", record.get("verdict"), "intended_failure")
        check_not_in("A-K4 no refusal note", "MineRefusal", " ".join(str(n) for n in record.get("notes") or []))
        request = json.loads((root / "qa-factory" / "artifacts" / TASK / "work" / "probe-requests"
                              / "probe-walk-test_add-1.json").read_text(encoding="utf-8"))   # t-2064 P4b: a walk's request, per run
        check_eq("A-K4 the request runs under the profile the row names", request.get("profile_id"), "unit")
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = project(shared_second=True)
    try:
        original_k5 = (root / TEST_FILE_REL).read_bytes()
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        notes = " ".join(str(n) for n in record.get("notes") or [])
        check_eq("A-K5 two profiles, the row names none: not executed (nothing is proven by a refused run)",
                 record.get("verdict"), "not_executed")
        check_in("A-K5 the note says the profiles share the root", "profiles unit, ui share the test root `tests`", notes)
        check_in("A-K5 and names the manifest-row door", "`profile_id`", notes)
        check_not_in("A-K5 and NOT --profile, which this tool does not accept", "--profile", notes)
        check("A-K5 no request was written: nothing ran under the first profile",
              not list((root / "qa-factory" / "artifacts" / TASK / "work" / "probe-requests").glob("probe-*")))   # any name: a walk's are probe-walk-<IID>-<run>
        # RH1-8 F4: this is a LATE refusal (profile, in `build_mine_request`, after the mutant is written): the bytes must be back
        check_eq("A-K5 the bytes are back after the late refusal", (root / TEST_FILE_REL).read_bytes(), original_k5)
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = project(shared_second=True, row_profile="ghost")
    try:
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        text = " ".join([proc.stdout, proc.stderr] + [str(n) for n in record.get("notes") or []])
        check_in("A-K6 a profile the config does not hold is refused naming it", "`ghost`", text)
        check_in("A-K6 and the profile_ids the config does hold", "unit, ui", text)
        check_not_in("A-K6 not as a gap of the onboarding", "gap of the onboarding", text)
        check("A-K6 and no verdict of a run", record.get("verdict") != "intended_failure", str(record.get("verdict")))
    finally:
        cleanup(root)
        cleanup_beside(root)


def two_profiles_flow() -> None:
    stub_dir = temp_dir("qa-probe-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    try:
        two_profiles_over_one_root(stub)
    finally:
        cleanup(stub_dir)


def main() -> None:
    two_profiles_flow()
    finish("test_probe_by_code_two_profiles")


# split: runner piece 1
if __name__ == "__main__":
    main()
