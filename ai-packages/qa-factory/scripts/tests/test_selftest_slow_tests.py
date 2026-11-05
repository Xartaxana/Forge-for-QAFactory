"""The slow-test list is a data file, scripts/slow_tests.json (F6-18, FR-13), and `selftest.py --slow-tests` diffs it.

Pins: the loader (present / absent / malformed / unknown keys), that `--fast` skips exactly the files the data file
names, the duration-line parser on verbatim lines of the nightly of 15.10 (job 27713550), the diff and its limit
(AT the limit and one beyond), `--update` (rewrites with the flag, never without it, never from an empty
measurement), the thresholds read from the file, and the exit codes of the real command line (2 = no list or nothing
measured, 1 = more changes than the limit).

The command-line cases run a COPY of selftest.py in a temp package, so the data file and the tests folder they see
are temp ones. Nothing here waits on the clock (FR-31)."""
import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, check_in, finish, temp_dir  # noqa: E402

sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import selftest as S  # noqa: E402

# Verbatim lines of ci-out/selftest.txt of the nightly 15.10 (pipeline 7920685, job 27713550). The third is a
# FAIL line: its detail follows the seconds, and the artifact shows the dash as `?`.
LINE_PASS_1 = "PASS tests: scripts/tests/test_manifest_from_tests.py  16.0s"
LINE_PASS_2 = "PASS tests: scripts/tests/test_no_move_seam.py  68.9s"
LINE_FAIL = ("FAIL tests: scripts/tests/test_story_run_loop_b.py  16.2s ? exit 1 ? Code checked the state "
             "precondition of each row of")


def lines_of(measured: dict) -> str:
    return "".join(f"PASS tests: scripts/tests/{n}  {s}s\n" for n, s in measured.items())


def data_text(files: dict, over=10, under=5, drift=5, **extra) -> str:
    body = {"measured_on": "2026-01-01", "source": "hand",
            "thresholds": {"slow_over_s": over, "fast_under_s": under}, "files": files}
    if drift is not None:
        body["max_drift"] = drift
    body.update(extra)
    return json.dumps(body, indent=2) + "\n"


def tests_dir_with(root: Path, names) -> Path:
    tests = root / "scripts" / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    for name in names:
        (tests / name).write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    return tests


def run_in_process(fn, *args, **kwargs):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fn(*args, **kwargs)
    return rc, out.getvalue(), err.getvalue()


def refused(path: Path) -> str | None:
    try:
        S.slow_tests(path)
    except S.SlowTestsError as exc:
        return str(exc)
    return None


def loader_cases(root: Path) -> None:
    shipped = S.slow_tests()
    check("the shipped data file loads and lists the two files the old tuple led with",
          {"test_words_doors.py", "test_story_run_words.py"} <= set(shipped["files"]))
    check_eq("the shipped thresholds are the 10 s / 5 s rule", shipped["thresholds"],
             {"slow_over_s": 10, "fast_under_s": 5})
    # The nightly measurement of 2026-10-23 measured `test_story_run_words.py` (8.5 s), so no shipped row is null any more;
    # a null row is covered below by `present.json` (`test_b.py: null`). The shipped rule: null or a positive number.
    check("a listed file carries a measurement or null, never a made-up number (0, a string)",
          all(v is None or (isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0)
              for v in shipped["files"].values()))
    check_eq("the shipped file is its own canonical rendering (an --update with nothing new changes no byte)",
             (PLUGIN_ROOT / "scripts" / "slow_tests.json").read_text(encoding="utf-8"),
             S.render_slow_tests(shipped))

    p = root / "present.json"
    p.write_text(data_text({"test_a.py": 12.5, "test_b.py": None}, over=11, under=4, drift=2,
                           future_key={"x": 1}, another=[1, 2]), encoding="utf-8")
    got = S.slow_tests(p)
    check_eq("present: files, thresholds, max_drift and dates come back; unknown keys are ignored",
             (got["files"], got["thresholds"], got["max_drift"], got["measured_on"], got["source"], got["notes"]),
             ({"test_a.py": 12.5, "test_b.py": None}, {"slow_over_s": 11, "fast_under_s": 4}, 2,
              "2026-01-01", "hand", []))
    check("unknown keys are not carried into the result", set(got) == {
        "measured_on", "source", "thresholds", "max_drift", "files", "notes"})

    absent = refused(root / "nothing-here.json")
    check("absent: refused, and the one line names the file", absent is not None
          and "nothing-here.json" in absent and "\n" not in absent)

    noted = root / "nodrift.json"
    noted.write_text(data_text({"test_a.py": 1.0}, drift=None), encoding="utf-8")
    got = S.slow_tests(noted)
    check_eq("max_drift absent: 5, and the result says so", got["max_drift"], 5)
    check_in("max_drift absent: the note names the field", "max_drift", got["notes"])

    bom = root / "bom.json"
    bom.write_bytes(b"\xef\xbb\xbf" + data_text({"test_a.py": 1.0}).encode("utf-8"))
    check("a file saved with a byte-order mark still loads", refused(bom) is None)

    bad = {
        "not JSON": "{ this is not json",
        "an empty file": "",
        "top level a list": "[]",
        "files missing": json.dumps({"thresholds": {"slow_over_s": 10, "fast_under_s": 5}}),
        "files a list": json.dumps({"thresholds": {"slow_over_s": 10, "fast_under_s": 5}, "files": []}),
        "thresholds missing": json.dumps({"files": {}}),
        "a threshold missing": json.dumps({"thresholds": {"slow_over_s": 10}, "files": {}}),
        "a threshold a string": json.dumps({"thresholds": {"slow_over_s": "10", "fast_under_s": 5}, "files": {}}),
        "a threshold negative": json.dumps({"thresholds": {"slow_over_s": -1, "fast_under_s": 5}, "files": {}}),
        "seconds a string": data_text({"test_a.py": "12"}),
        "seconds a bool": data_text({"test_a.py": True}),
        "seconds negative": data_text({"test_a.py": -3}),
        "a name with a folder": data_text({"fixtures/test_a.py": 12}),
        "an empty name": data_text({"": 12}),
        "max_drift a float": data_text({}, drift=2.5),
        "max_drift negative": data_text({}, drift=-1),
        "max_drift a bool": data_text({}, drift=True),
        "measured_on a number": data_text({}, measured_on=5),
    }
    for label, text in bad.items():
        f = root / "bad.json"
        f.write_text(text, encoding="utf-8")
        message = refused(f)
        check(f"malformed ({label}): refused with one line naming the file",
              message is not None and "bad.json" in message and "\n" not in message, repr(message))


def fast_skip_cases(root: Path) -> None:
    pkg = root / "fastpkg"
    tests = tests_dir_with(pkg, ["test_alpha_listed.py", "test_beta_unlisted.py"])
    listing = pkg / "listing.json"
    listing.write_text(data_text({"test_alpha_listed.py": 12.0}), encoding="utf-8")
    with patch.object(S, "PLUGIN_ROOT", pkg), patch.object(S, "TESTS_DIR", tests), \
            patch.object(S, "SLOW_TESTS_FILE", listing), patch.object(S, "RESULTS", []), \
            patch.dict(S.TEST_DURATIONS, clear=True):
        ok, out, _ = run_in_process(S.cmd_tests, 1, True)
    check("--fast: the file the data file names is not run", "test_alpha_listed.py" not in out, out)
    check("--fast: a file the data file does not name is run", "PASS tests: scripts" in out
          and "test_beta_unlisted.py" in out, out)
    check_in("--fast: the skipped count is printed", "1 file(s) skipped", out)
    with patch.object(S, "PLUGIN_ROOT", pkg), patch.object(S, "TESTS_DIR", tests), \
            patch.object(S, "SLOW_TESTS_FILE", listing), patch.object(S, "RESULTS", []), \
            patch.dict(S.TEST_DURATIONS, clear=True):
        ok_full, out_full, _ = run_in_process(S.cmd_tests, 1, False)
    check("the full run (not fast) runs the listed file too",
          "test_alpha_listed.py" in out_full and "test_beta_unlisted.py" in out_full, out_full)
    check("the full run prints no INFO staleness lines any more (the diff replaces them)",
          "INFO" not in out_full, out_full)


def parser_cases() -> None:
    got = S.parse_durations("\n".join([LINE_PASS_1, LINE_PASS_2, LINE_FAIL]) + "\n")
    check_eq("parser: three verbatim lines of the 15.10 artifact (two PASS, one FAIL with detail after the seconds)",
             got, {"test_manifest_from_tests.py": 16.0, "test_no_move_seam.py": 68.9,
                   "test_story_run_loop_b.py": 16.2})
    cut = "\n".join([
        "PASS tests: scripts/tests/test_cut_a.py  1",          # cut inside the number
        "PASS tests: scripts/tests/test_cut_b.py  12.",        # cut after the point
        "PASS tests: scripts/tests/test_cut_c.p",              # cut inside the name
        "PASS tests: scripts/tests/test_cut_d.py  3.4",        # the `s` lost
        "PASS tests: scripts/tests/test_whole.py  5.5s"])
    check_eq("parser: a line cut mid-way is skipped, a whole one after it still counts, nothing raises",
             S.parse_durations(cut), {"test_whole.py": 5.5})
    outside = "\n".join([
        "PASS tests: scripts/tests/fixtures/test_in_a_folder.py  30.0s",
        "PASS tests: scripts/other/test_elsewhere.py  30.0s",
        "PASS selftest-scripts: form_selftest.py  30.0s",
        "tests: slowest 5 — test_infra_failure.py 110.0s, test_story_run_s0.py 85.2s",
        "tests: INFO over 10s but not in SLOW_TESTS (add to selftest.py): test_x.py",
        "PASS tests: scripts/tests/test_inside.py  2.0s"])
    check_eq("parser: a duration line for a file outside scripts/tests/, and the summary lines, are ignored",
             S.parse_durations(outside), {"test_inside.py": 2.0})
    check_eq("parser: two runs of one file (a retry) - the LAST duration wins",
             S.parse_durations("PASS tests: scripts/tests/test_r.py  90.0s\n"
                               "FAIL tests: scripts/tests/test_r.py  120.5s ? exit 1\n"
                               "PASS tests: scripts/tests/test_r.py  40.2s\n"),
             {"test_r.py": 40.2})
    check_eq("parser: a Windows run prints backslashes and CRLF - still read",
             S.parse_durations("PASS tests: scripts\\tests\\test_win.py  7.0s\r\n"), {"test_win.py": 7.0})
    check_eq("parser: empty text is no measurement", S.parse_durations(""), {})


NAMES = ["over_new.py", "at_ten.py", "listed_fast.py", "listed_five.py", "listed_mid.py", "listed_unmeasured.py",
         "unlisted_small.py"]
LISTED = {"listed_fast.py": 20.0, "listed_five.py": 20.0, "listed_mid.py": 20.0, "listed_unmeasured.py": None,
          "gone.py": 15.0}
MEASURED = {"over_new.py": 12.0, "at_ten.py": 10.0, "listed_fast.py": 4.9, "listed_five.py": 5.0,
            "listed_mid.py": 7.0, "unlisted_small.py": 1.0, "ghost.py": 99.0}


def diff_cases(root: Path) -> None:
    pkg = root / "diffpkg"
    tests = tests_dir_with(pkg, NAMES)
    listing = pkg / "listing.json"
    listing.write_text(data_text(LISTED), encoding="utf-8")
    data = S.slow_tests(listing)
    diff = S.slow_tests_diff(data, MEASURED, tests)
    check_eq("diff: over the threshold and not listed = added (exactly 10.0 is not over)",
             diff["added"], [("over_new.py", 12.0)])
    check_eq("diff: listed and under the fast threshold = removed (exactly 5.0 is not under)",
             diff["removed"], [("listed_fast.py", 4.9)])
    check_eq("diff: listed and gone from disk = missing; measured-only and gone from disk is ignored",
             diff["missing"], ["gone.py"])
    check_eq("diff: the rest is unchanged - between the thresholds, unmeasured, small and unlisted",
             diff["unchanged"], 5)
    check_eq("diff: changes = added + removed + missing", diff["changes"], 3)

    # the thresholds come from the FILE: a different rule, the same measurement, a different diff
    strict = root / "strict.json"
    strict.write_text(data_text(LISTED, over=20, under=8), encoding="utf-8")
    diff2 = S.slow_tests_diff(S.slow_tests(strict), MEASURED, tests)
    check_eq("thresholds from the file: over 20 s adds nothing", diff2["added"], [])
    check_eq("thresholds from the file: under 8 s removes the 4.9, the 5.0 and the 7.0",
             [n for n, _ in diff2["removed"]], ["listed_fast.py", "listed_five.py", "listed_mid.py"])


def printed_cases(root: Path) -> None:
    pkg = root / "printpkg"
    tests = tests_dir_with(pkg, NAMES + ["extra_new.py"])
    art = pkg / "artifact.txt"
    listing = pkg / "listing.json"

    def run(measured: dict, drift: int):
        art.write_text(lines_of(measured), encoding="utf-8")
        listing.write_text(data_text(LISTED, drift=drift), encoding="utf-8")
        with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
            return run_in_process(S.cmd_slow_tests, str(art), False)

    rc, out, _ = run(MEASURED, 3)
    check_eq("limit: 3 changes AT a limit of 3 = exit 0", rc, 0)
    check_in("limit: the summary line", "slow tests: 3 change(s) (limit 3)", out)
    check_in("diff text: added line", "+ over_new.py 12.0s", out)
    check_in("diff text: removed line", "- listed_fast.py 4.9s", out)
    check_in("diff text: missing line", "- gone.py (missing)", out)
    check_in("diff text: unchanged line", "= 5 unchanged", out)

    rc, out, _ = run({**MEASURED, "extra_new.py": 30.0}, 3)
    check_eq("limit: 4 changes, one BEYOND a limit of 3 = exit 1", rc, 1)
    check_in("limit: the summary line says 4", "slow tests: 4 change(s) (limit 3)", out)
    check_in("limit beyond: the way out is named", "--update", out)

    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
        listing.write_text(data_text(LISTED, drift=None), encoding="utf-8")
        rc, out, _ = run_in_process(S.cmd_slow_tests, str(art), False)
    check_in("max_drift absent: the diff prints the note", "max_drift is absent", out)
    check_in("max_drift absent: and the limit is 5", "(limit 5)", out)


def update_cases(root: Path) -> None:
    pkg = root / "updpkg"
    tests = tests_dir_with(pkg, NAMES)
    art = pkg / "selftest-x.txt"
    listing = pkg / "listing.json"
    art.write_text(lines_of(MEASURED), encoding="utf-8")
    listing.write_text(data_text(LISTED, drift=1), encoding="utf-8")   # 3 changes > 1: red without the flag
    before = listing.read_bytes()

    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
        rc, out, _ = run_in_process(S.cmd_slow_tests, str(art), False)
    check_eq("no --update: more changes than the limit = exit 1", rc, 1)
    check("no --update: the data file is not rewritten (same bytes)", listing.read_bytes() == before)

    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
        rc, out, _ = run_in_process(S.cmd_slow_tests, str(art), True, "2026-02-03")
    check_eq("--update: exit 0 even though the diff is over the limit", rc, 0)
    new = json.loads(listing.read_text(encoding="utf-8"))
    check_eq("--update: files = measured-over in, listed-under out, missing out, between kept with fresh seconds, "
             "unmeasured kept as it was",
             new["files"], {"over_new.py": 12.0, "listed_five.py": 5.0, "listed_mid.py": 7.0,
                            "listed_unmeasured.py": None})
    check_eq("--update: measured_on is today's date as given", new["measured_on"], "2026-02-03")
    check_eq("--update: source is the --from file name", new["source"], "selftest-x.txt")
    check_eq("--update: thresholds and max_drift carry over", (new["thresholds"], new["max_drift"]),
             ({"slow_over_s": 10, "fast_under_s": 5}, 1))
    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
        rc, out, _ = run_in_process(S.cmd_slow_tests, str(art), False)
    check("after --update the same measurement shows 0 changes and exits 0", rc == 0
          and "slow tests: 0 change(s)" in out, out)

    # the local-run form: the durations of THIS process's --tests run, source "local run"
    listing.write_text(data_text({"listed_mid.py": 7.0}, drift=1), encoding="utf-8")
    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing), \
            patch.dict(S.TEST_DURATIONS, {"scripts/tests/over_new.py": 12.34}, clear=True):
        rc, out, _ = run_in_process(S.cmd_slow_tests, None, True, "2026-02-04")
    new = json.loads(listing.read_text(encoding="utf-8"))
    check_eq("--update without --from: source is 'local run', the 12.34 is kept to one decimal",
             (rc, new["source"], new["files"]), (0, "local run", {"listed_mid.py": 7.0, "over_new.py": 12.3}))


def empty_measurement_cases(root: Path) -> None:
    pkg = root / "emptypkg"
    tests = tests_dir_with(pkg, NAMES)
    listing = pkg / "listing.json"
    listing.write_text(data_text(LISTED), encoding="utf-8")
    before = listing.read_bytes()
    blank = pkg / "no-durations.txt"
    blank.write_text("tests: INFO over 10s but not in SLOW_TESTS: a.py\n=== qa-factory selftest: 1/1 ok ===\n",
                     encoding="utf-8")
    with patch.object(S, "TESTS_DIR", tests), patch.object(S, "SLOW_TESTS_FILE", listing):
        rc, out, err = run_in_process(S.cmd_slow_tests, str(blank), True)
        check("--update from a file with NO duration lines: exit 2, stderr says so, nothing on stdout",
              rc == 2 and "no test durations" in err and out == "", f"{rc!r} {err!r} {out!r}")
        check("--update from an empty measurement: the data file is untouched (no empty list written)",
              listing.read_bytes() == before)
        rc, _, err = run_in_process(S.cmd_slow_tests, str(blank), False)
        check_eq("the diff of an empty measurement is exit 2 too, never a green 'nothing changed'", rc, 2)
        with patch.dict(S.TEST_DURATIONS, clear=True):
            rc, _, err = run_in_process(S.cmd_slow_tests, None, True)
        check("--update with no --from and no --tests run: exit 2, file untouched",
              rc == 2 and listing.read_bytes() == before and "--tests" in err, err)
        rc, _, err = run_in_process(S.cmd_slow_tests, str(pkg / "no-such-artifact.txt"), True)
        check("--from a file that does not exist: exit 2 naming it", rc == 2 and "no-such-artifact.txt" in err, err)


def cli(args, files_text: str | None, root: Path, name: str, tests=(), artifact: str | None = None):
    """Run a COPY of selftest.py in a temp package: the data file and tests folder it sees are temp ones."""
    pkg = root / name
    scripts = pkg / "scripts"
    tests_dir_with(pkg, tests)
    for module in ("selftest.py", "content_size.py", "console_io.py"):
        shutil.copy2(PLUGIN_ROOT / "scripts" / module, scripts / module)
    if files_text is not None:
        (scripts / "slow_tests.json").write_text(files_text, encoding="utf-8")
    if artifact is not None:
        (pkg / "selftest.txt").write_text(artifact, encoding="utf-8")
    argv = [a.replace("@ART", str(pkg / "selftest.txt")) for a in args]
    p = subprocess.run([sys.executable, "-B", str(scripts / "selftest.py"), *argv], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(pkg), timeout=120)
    return p, scripts / "slow_tests.json"


def cli_cases(root: Path) -> None:
    p, _ = cli(["--slow-tests", "--from", "@ART"], None, root, "cli-absent", NAMES, lines_of(MEASURED))
    check("CLI: no data file with --slow-tests = exit 2, ONE stderr line naming slow_tests.json",
          p.returncode == 2 and len(p.stderr.strip().splitlines()) == 1 and "slow_tests.json" in p.stderr
          and p.stdout == "", f"{p.returncode} {p.stderr!r} {p.stdout!r}")
    for flag in (["--fast"], ["--tests"], []):
        p, _ = cli(flag, None, root, "cli-absent-" + (flag[0].strip("-") if flag else "all"))
        check(f"CLI: no data file with {flag or 'a flagless run'} = exit 2 before anything runs (no silent fast tier)",
              p.returncode == 2 and len(p.stderr.strip().splitlines()) == 1 and "slow_tests.json" in p.stderr
              and "PASS" not in p.stdout, f"{p.returncode} {p.stderr!r} {p.stdout[:200]!r}")
    p, _ = cli(["--slow-tests", "--from", "@ART"], "{ not json", root, "cli-bad", NAMES, lines_of(MEASURED))
    check("CLI: a malformed data file = exit 2, one line naming the file",
          p.returncode == 2 and len(p.stderr.strip().splitlines()) == 1 and "slow_tests.json" in p.stderr, p.stderr)

    p, _ = cli(["--slow-tests", "--from", "@ART"], data_text(LISTED, drift=2), root, "cli-over", NAMES,
               lines_of(MEASURED))
    check("CLI: --slow-tests --from <artifact> with 3 changes over a limit of 2 = exit 1, the diff on stdout",
          p.returncode == 1 and "+ over_new.py 12.0s" in p.stdout and "slow tests: 3 change(s) (limit 2)" in p.stdout
          and "=== qa-factory selftest" not in p.stdout, f"{p.returncode} {p.stdout!r}")
    p, _ = cli(["--slow-tests", "--from", "@ART"], data_text(LISTED, drift=3), root, "cli-at", NAMES,
               lines_of(MEASURED))
    check_eq("CLI: the same 3 changes AT a limit of 3 = exit 0", p.returncode, 0)

    # --tests --slow-tests in ONE call: the durations of this process's own run are the measurement (the two temp
    # test files finish in well under 5 s, so the listed one that ran is `-`, and the listed one gone is missing)
    p, _ = cli(["--tests", "--jobs", "1", "--slow-tests"], data_text({"test_l_fast.py": 20.0, "test_l_gone.py": 15.0}),
               root, "cli-local", ["test_l_fast.py", "test_l_new.py"])
    check("CLI: --tests --slow-tests in one call measures that run: 2 changes, within the limit, exit 0, "
          "and the selftest summary still prints",
          p.returncode == 0 and "slow tests: 2 change(s) (limit 5)" in p.stdout and "- test_l_fast.py" in p.stdout
          and "- test_l_gone.py (missing)" in p.stdout and "= 1 unchanged" in p.stdout
          and "=== qa-factory selftest: 2/2 ok ===" in p.stdout,
          f"{p.returncode} {p.stdout[-400:]!r} {p.stderr[-200:]!r}")
    p, _ = cli(["--slow-tests"], data_text(LISTED), root, "cli-nomeasure", NAMES)
    check("CLI: --slow-tests with neither --from nor --tests = exit 2 and says what to pass",
          p.returncode == 2 and "--from" in p.stderr and "--tests" in p.stderr, p.stderr)
    p, _ = cli(["--update"], data_text(LISTED), root, "cli-update-alone", NAMES)
    check_eq("CLI: --update without --slow-tests is refused (exit 2)", p.returncode, 2)
    p, _ = cli(["--slow-tests", "--fast"], data_text(LISTED), root, "cli-fast", NAMES)
    check_eq("CLI: --slow-tests with --fast is refused (exit 2)", p.returncode, 2)

    p, target = cli(["--slow-tests", "--from", "@ART", "--update"], data_text(LISTED, drift=1), root, "cli-update",
                    NAMES, lines_of(MEASURED))
    new = json.loads(target.read_text(encoding="utf-8"))
    check("CLI: --update rewrites the file, exit 0, source = the file name, measured_on = a date",
          p.returncode == 0 and new["source"] == "selftest.txt" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", new["measured_on"])
          and "over_new.py" in new["files"] and "listed_fast.py" not in new["files"], f"{p.returncode} {new!r}")
    p, target = cli(["--slow-tests", "--from", "@ART", "--update"], data_text(LISTED, drift=1), root, "cli-empty",
                    NAMES, "=== qa-factory selftest: 1/1 ok ===\n")
    check("CLI: --update from an output with no duration lines = exit 2 and the list is not emptied",
          p.returncode == 2 and json.loads(target.read_text(encoding="utf-8"))["files"] == LISTED, p.stderr)


def main() -> None:
    root = temp_dir("slow-tests-")
    try:
        loader_cases(root)
        fast_skip_cases(root)
        parser_cases()
        diff_cases(root)
        printed_cases(root)
        update_cases(root)
        empty_measurement_cases(root)
        cli_cases(root)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    finish("test_selftest_slow_tests")


if __name__ == "__main__":
    main()
