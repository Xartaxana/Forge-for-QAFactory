#!/usr/bin/env python3
"""The probe runner `mutate_once.py`: one table over its outcome table, the adversarial inputs and the restore invariant.

Each row builds a tiny target (`mod.py`) and a tiny test file in a temp root, calls `main()` in-process and checks the exit
code, the last printed line (`outcome: <word>`) and that the target is byte-identical afterwards (and untouched, by mtime,
when the run was refused or the mutant did not compile). Expected values come from the outcome table of the forge test rules
spec, section 5.3 (docs/tasks/specs/20261117-forge-test-rules-spec.md), not from the runner's output.

Run: python -B scripts/tests/test_mutate_once.py    or    python -m pytest scripts/tests/test_mutate_once.py -q
"""
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mutate_once as MO  # noqa: E402

TARGET = b"VALUE = 1\nOTHER = 2\n"
OLD, KILL, LIVE = "VALUE = 1", "VALUE = 9", "VALUE = 1  # same value"

# a script-form test: prints a FAIL line and a `=== ` summary, exits 1 when VALUE changed
SCRIPT = ("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nimport mod\n"
          "bad = mod.VALUE != 1\nprint('FAIL value changed' if bad else 'ok')\nprint('=== 1 checks, %d failed' % bad)\n"
          "sys.exit(1 if bad else 0)\n")
SCRIPT_NO_SUMMARY = SCRIPT.replace("print('=== 1 checks, %d failed' % bad)\n", "")
SCRIPT_NO_FAIL = SCRIPT.replace("print('FAIL value changed' if bad else 'ok')", "print('ok')")
SCRIPT_CRASH = ("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nimport mod\n"
                "if mod.VALUE != 1:\n    raise RuntimeError('crash before any summary')\n")
SCRIPT_LOOP = SCRIPT_CRASH.replace("raise RuntimeError('crash before any summary')", "while True:\n        pass")
# a test that runs a grandchild holding its stdout (the output file), then hangs: the grandchild outlives the kill
SCRIPT_GRANDCHILD = SCRIPT_CRASH.replace(
    "raise RuntimeError('crash before any summary')",
    "import subprocess, time\n    subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(8)'], stdout=sys.stdout, "
    "stderr=sys.stderr)\n    time.sleep(60)")
PYTEST = "from mod import VALUE\n\n\ndef test_value():\n    assert VALUE == 1\n"
PYTEST_EMPTY = "from mod import VALUE\n"

OUT, NO_OUTCOME = "outcome", None


def case(name, *, test=SCRIPT, target=TARGET, old=OLD, new=KILL, exit=0, outcome="killed", pytest_form=False, **extra):
    return pytest.param(dict(test=test, target=target, old=old, new=new, exit=exit, outcome=outcome, pytest=pytest_form, **extra),
                        id=name)


CASES = [
    # killed / survived, both forms
    case("script-failed-with-summary-and-FAIL-line-is-killed"),
    case("script-passed-is-survived", new=LIVE, exit=1, outcome="survived"),
    case("pytest-one-failed-is-killed", test=PYTEST, pytest_form=True),
    case("pytest-passed-is-survived", test=PYTEST, pytest_form=True, new=LIVE, exit=1, outcome="survived"),
    # never toward killed: failures that are not an assertion
    case("script-nonzero-without-summary-is-invalid", test=SCRIPT_NO_SUMMARY, exit=3, outcome="invalid"),
    case("script-nonzero-without-FAIL-line-is-invalid", test=SCRIPT_NO_FAIL, exit=3, outcome="invalid"),
    case("script-crash-before-summary-is-invalid", test=SCRIPT_CRASH, exit=3, outcome="invalid"),
    case("pytest-import-broken-by-mutant-is-invalid", test=PYTEST, pytest_form=True, new="import no_such_module_xyz",
         exit=3, outcome="invalid"),
    case("pytest-file-with-no-tests-is-invalid", test=PYTEST_EMPTY, pytest_form=True, exit=3, outcome="invalid"),
    # compile check: invalid, nothing touched
    case("py-mutant-with-syntax-error-is-invalid-untouched", new="VALUE = (", exit=3, outcome="invalid", untouched=True),
    # byte fidelity: BOM and CRLF survive mutation and restore
    case("bom-and-crlf-target-restored-byte-identical", target=b"\xef\xbb\xbfVALUE = 1\r\nOTHER = 2\r\n"),
    # pre-touch refusals, exit 64, no outcome line, nothing touched
    case("old-text-absent-is-refused", old="NOT THERE", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("old-text-twice-is-refused", target=b"VALUE = 1\nVALUE = 1\n", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("empty-old-is-refused", old="", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("new-equal-to-old-is-refused", new=OLD, exit=64, outcome=NO_OUTCOME, untouched=True),
    case("target-not-utf8-is-refused", target=b"VALUE = 1\n\xff\xfe\n", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("target-outside-root-is-refused", target_arg="../outside.py", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("test-outside-root-is-refused", test_arg="../outside_test.py", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("test-file-absent-is-refused", test_arg="missing_test.py", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("unknown-argument-is-refused", argv_extra=["--bogus"], exit=64, outcome=NO_OUTCOME, untouched=True),
    case("inline-form-without-root-is-refused", drop="--root", exit=64, outcome=NO_OUTCOME, untouched=True),
    case("one-positional-only-is-refused", raw_argv=["only-a-spec.json"], exit=64, outcome=NO_OUTCOME, untouched=True),
    # the spec-file form (back-compat) and its refusals
    case("spec-file-form-killed", spec_file=True),
    case("spec-file-unknown-id-is-refused", spec_file=True, spec_id="nope", exit=64, outcome=NO_OUTCOME, untouched=True),
    # timeout: the child killed, the target restored at once, the grandchild not waited for
    case("timeout-mutant-loops-forever-is-invalid-restored", test=SCRIPT_LOOP, exit=3, outcome="invalid", timeout=0.5),
    case("timeout-with-grandchild-holding-output-is-invalid-and-fast", test=SCRIPT_GRANDCHILD, exit=3, outcome="invalid",
         timeout=0.5, wall_under=6),
    # the output file cannot be read after the restore
    case("unreadable-output-is-invalid-restore-verified", exit=3, outcome="invalid", unreadable=True),
    # sha after != before wins over every other outcome
    case("restore-mismatch-wins-over-killed", exit=2, outcome="restore-mismatch", sha_differs=True),
]


def build(tmp_path, spec):
    root = tmp_path / "root"
    root.mkdir()
    (tmp_path / "outside.py").write_bytes(TARGET)
    (tmp_path / "outside_test.py").write_text(SCRIPT, encoding="utf-8")
    (root / "mod.py").write_bytes(spec["target"])
    (root / "check.py").write_text(spec["test"], encoding="utf-8")
    return root


def argv_of(root, spec, tmp_path):
    if "raw_argv" in spec:
        return ["mutate_once.py"] + spec["raw_argv"]
    target, test = spec.get("target_arg", "mod.py"), spec.get("test_arg", "check.py")
    if spec.get("spec_file"):
        import json
        path = tmp_path / "spec.json"
        path.write_text(json.dumps({"target": target, "test": test, "mutations": {"m1": {"old": spec["old"], "new": spec["new"]}}}),
                        encoding="utf-8")
        return ["mutate_once.py", "--root", str(root), str(path), spec.get("spec_id", "m1")]
    argv = ["mutate_once.py", "--root", str(root), "--id", "m1", "--target", target, "--old", spec["old"], "--new", spec["new"],
            "--test", test] + (["--pytest"] if spec["pytest"] else []) + spec.get("argv_extra", [])
    if spec.get("drop"):
        index = argv.index(spec["drop"])
        del argv[index:index + 2]
    return argv


@pytest.mark.parametrize("spec", CASES)
def test_outcome_table(spec, tmp_path, monkeypatch, capsys):
    """Expected exit and outcome word per row: spec section 5.3 outcome table; the target is byte-identical afterwards on every row."""
    root = build(tmp_path, spec)
    before = (root / "mod.py").read_bytes()
    mtime = (root / "mod.py").stat().st_mtime_ns
    monkeypatch.setattr(MO, "TIMEOUT_S", spec.get("timeout", 60))
    if spec.get("unreadable"):
        real = Path.read_text

        def read_text(self, *a, **k):
            if self.name == "output.txt":
                raise PermissionError("the output file cannot be read")
            return real(self, *a, **k)
        monkeypatch.setattr(Path, "read_text", read_text)
    if spec.get("sha_differs"):
        calls = iter(["before-hash", "after-hash"])
        monkeypatch.setattr(MO, "sha", lambda data: next(calls))
    started = time.monotonic()
    code = MO.main(argv_of(root, spec, tmp_path))
    wall = time.monotonic() - started
    lines = capsys.readouterr().out.strip().splitlines()
    last = lines[-1] if lines else ""
    assert code == spec["exit"], f"exit {code}: {lines[-4:]}"
    if spec["outcome"] is None:
        assert not any(line.startswith("outcome:") for line in lines), lines    # a refusal prints no outcome
        assert lines and lines[0].startswith("refused:"), lines
    else:
        assert last == f"outcome: {spec['outcome']}", lines[-4:]
    assert (root / "mod.py").read_bytes() == before, "the target is not byte-identical after the run"
    if spec.get("untouched"):
        assert (root / "mod.py").stat().st_mtime_ns == mtime, "the target was written although the run was refused"
    if "wall_under" in spec:
        assert wall < spec["wall_under"], f"the run took {wall:.1f} s: the restore or the run waited for the grandchild"


def test_no_arguments_prints_usage_naming_root():
    """Spec section 5.3 Interface: the usage text names --root (the critic's signal for a pre-S-E runner); exit 64."""
    done = subprocess.run([sys.executable, "-B", str(HERE / "mutate_once.py")], capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 64 and "--root" in done.stdout


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
