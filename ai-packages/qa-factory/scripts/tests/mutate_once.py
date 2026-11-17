"""One mutation, one test file, a byte-copy rollback: the runner behind a probe (a builder's witness, a critic's bounded probe).

Two forms, one run:

    python -B scripts/tests/mutate_once.py [--root <dir>] <spec.json> <mutation id>
    python -B scripts/tests/mutate_once.py --root <dir> --id <name> --target <path> --old <text> --new <text> --test <path> [--pytest]

The spec file is JSON: {"target": "story_run.py", "test": "tests/test_x.py", "mutations": {"<id>": {"old": "...", "new": "..."}}};
`target` and `test` are paths under `scripts/` (or under `--root` when it is given). The inline form writes no file: the mutant is
named in the command. Paths are relative to `--root`; a path that resolves outside it is refused. A value that starts with `-`
is written `--old=<text>`.

The runner checks everything BEFORE touching the target: the paths are inside the root, the test file exists, the target is UTF-8,
`old` is non-empty and occurs EXACTLY ONCE, `new` differs from `old`, a `.py` mutant compiles. It takes a byte copy of the target,
writes the mutant, runs the ONE test file (`python -B <test>`, or `python -B -m pytest -q <test>` with `--pytest`; the output goes
to a temporary file outside the root, the child is killed after TIMEOUT_S seconds), restores the target FROM THE COPY at once,
compares sha256 before and after, and only then reads the output. It prints the test's last summary line, the first FAIL lines,
the sha line and a last line `outcome: <word>`.

Exit 0 `killed` (the test failed an assertion), 1 `survived` (the test passed), 2 `restore-mismatch` (sha256 after differs from
before; wins over everything), 3 `invalid` (the mutant does not compile, the child timed out, the output was unreadable, or the
test file failed without an assertion: no `=== ` summary line or no FAIL line; pytest: collection error, usage error, no tests),
64 a refusal before touching (nothing printed as an outcome). The runner may err toward `invalid` or `survived`, never toward
`killed`. Whether a printed FAIL line is a real kill (an import error is not) is the reader's judgment.
"""
import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
TIMEOUT_S = 60
REAP_S = 5
SUMMARY_RE = re.compile(r"\b\d+ (?:failed|passed|errors?|skipped|deselected|warnings?|xfailed|xpassed)\b.*\bin [\d.]+s")
FAILED_RE = re.compile(r"\b(\d+) failed\b")


class Refusal(Exception):
    """A pre-touch refusal: the message says what is wrong, what is expected and which argument fixes it."""


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Refusal(f"bad arguments: {message}; expected `<spec.json> <mutation id>` or `--root <dir> --id <name> --target <path> "
                      f"--old <text> --new <text> --test <path> [--pytest]` (run with no arguments for the usage text)")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def say(text: str) -> None:
    """Print without ever raising on a console that cannot show a character of the test's output."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    print(text.encode(encoding, "replace").decode(encoding, "replace"))


def _parse(argv: list):
    parser = _Parser(add_help=False)
    parser.add_argument("spec", nargs="?")
    parser.add_argument("mutation", nargs="?")
    for flag in ("root", "id", "target", "old", "new", "test"):
        parser.add_argument("--" + flag)
    parser.add_argument("--pytest", action="store_true")
    return parser.parse_args(argv)


def _resolve(root: Path, given: str, what: str) -> Path:
    path = (root / given).resolve()
    if path != root and root not in path.parents:
        raise Refusal(f"the {what} path {given!r} resolves outside --root {str(root)!r}; expected a path inside the root, "
                      f"relative to it: fix the --{what} argument (or the spec's `{what}`)")
    return path


def _plan(args) -> dict:
    """Everything that can be refused before the target is touched. Returns the facts of the run."""
    inline = any(getattr(args, name) is not None for name in ("id", "target", "old", "new", "test"))
    if inline:
        missing = [n for n in ("root", "id", "target", "old", "new", "test") if getattr(args, n) is None]
        if args.spec is not None or args.mutation is not None or missing:
            raise Refusal("bad arguments: the inline form takes no spec file and needs "
                          + ", ".join("--" + n for n in ("root", "id", "target", "old", "new", "test"))
                          + (f"; missing: {', '.join('--' + n for n in missing)}" if missing else "")
                          + "; fix the command line")
        ident, target_rel, test_rel, old, new = args.id, args.target, args.test, args.old, args.new
    else:
        if args.spec is None or args.mutation is None:
            raise Refusal("bad arguments: expected `<spec.json> <mutation id>` or the inline form; fix the command line")
        import json
        try:
            spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
            ident, target_rel, test_rel = args.mutation, spec["target"], spec["test"]
            old, new = spec["mutations"][args.mutation]["old"], spec["mutations"][args.mutation]["new"]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise Refusal(f"the spec file {args.spec!r} cannot give mutation {args.mutation!r}: {type(exc).__name__}: {exc}; "
                          f"expected JSON with `target`, `test` and `mutations.<id>.old/new`; fix the spec file or the id")
        if not all(isinstance(v, str) for v in (target_rel, test_rel, old, new)):
            raise Refusal(f"the spec file {args.spec!r}: `target`, `test`, `old` and `new` must be strings; fix the spec file")
    root = Path(args.root).resolve() if args.root is not None else SCRIPTS
    target, test = _resolve(root, target_rel, "target"), _resolve(root, test_rel, "test")
    if not target.is_file():
        raise Refusal(f"the target {target_rel!r} is not a file under {str(root)!r}; fix the target path")
    if not test.is_file():
        raise Refusal(f"the test file {test_rel!r} does not exist under {str(root)!r}; expected an existing test file: fix the "
                      f"test path")
    original = target.read_bytes()
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError:
        raise Refusal(f"the target {target_rel!r} is not UTF-8; the runner mutates only UTF-8 text: choose another target")
    if old == "":
        raise Refusal(f"{ident}: `old` is empty; expected the exact text to replace, found exactly once in the target: fix --old")
    if old == new:
        raise Refusal(f"{ident}: `new` equals `old`, so nothing would change; expected a different text: fix --new")
    found = text.count(old)
    if found != 1:
        raise Refusal(f"{ident}: the anchor is found {found} times, expected exactly 1; nothing was touched: lengthen or "
                      f"shorten --old until it occurs once")
    return {"id": ident, "target": target, "test": test, "root": root, "cwd": args.root is not None, "pytest": args.pytest,
            "original": original, "mutated": text.replace(old, new).encode("utf-8"), "text": text.replace(old, new)}


def _classify(pytest_form: bool, code: int, lines: list) -> tuple:
    """(outcome, summary line, FAIL lines) of a finished child that was not timed out and whose output was read."""
    fails = [line for line in lines if line.startswith("FAIL")]
    if pytest_form:
        summary = [line for line in lines if SUMMARY_RE.search(line)]
        last = summary[-1].strip() if summary else "no summary line"
        counts = FAILED_RE.search(last)
        if code == 0:
            return "survived", last, fails
        return ("killed" if code == 1 and counts and int(counts.group(1)) >= 1 else "invalid"), last, fails
    summary = [line for line in lines if line.startswith("=== ")]
    last = summary[-1] if summary else "no summary line (a crash?)"
    if code == 0:
        return "survived", last, fails
    return ("killed" if summary and fails else "invalid"), last, fails


def run_probe(plan: dict) -> int:
    target, test, root = plan["target"], plan["test"], plan["root"]
    before = sha(plan["original"])
    if target.suffix == ".py":
        try:
            compile(plan["mutated"], str(target), "exec")      # bytes: a BOM or a coding line is the compiler's to read
        except (SyntaxError, ValueError) as exc:
            say(f"--- {plan['id']}: the mutated {target.name} does not compile ({type(exc).__name__}: {exc}); nothing was touched")
            say("outcome: invalid")
            return 3
    argv = [sys.executable, "-B"] + (["-m", "pytest", "-q", "-p", "no:cacheprovider"] if plan["pytest"] else []) + [str(test)]
    timed_out, code, started_ok = False, None, False
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as scratch:
        out_path = Path(scratch) / "output.txt"
        proc = None
        try:
            target.write_bytes(plan["mutated"])
            with open(out_path, "wb") as sink:
                proc = subprocess.Popen(argv, stdout=sink, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                        cwd=str(root) if plan["cwd"] else None)
            started_ok = True
            try:
                code = proc.wait(timeout=TIMEOUT_S)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
        finally:
            target.write_bytes(plan["original"])          # at once: never waits for the child, a grandchild or the output
        if proc is not None and timed_out:
            try:
                proc.wait(REAP_S)
            except subprocess.TimeoutExpired:
                pass
        after = sha(target.read_bytes())
        output, unreadable = "", ""
        try:
            output = out_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            unreadable = f"{type(exc).__name__}: {exc}"
    lines = output.splitlines()
    outcome, last, fails = _classify(plan["pytest"], code if code is not None else 0, lines)
    if timed_out:
        outcome, last = "invalid", f"timed out after {TIMEOUT_S} s, the child was killed and the target restored"
    elif unreadable or not started_ok:
        outcome, last = "invalid", f"the output file could not be read ({unreadable or 'the child did not start'})"
    say(f"--- {plan['id']}: {test.name} exit={code}; {last}; FAIL lines: {len(fails)}")
    for line in fails[:3]:
        say("    " + line[:160])
    say(f"    sha256 {target.name} before {before} after {after} equal={before == after}")
    if before != after:
        say("outcome: restore-mismatch")
        return 2
    say(f"outcome: {outcome}")
    return {"killed": 0, "survived": 1, "invalid": 3}[outcome]


def main(argv: list) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 64
    try:
        plan = _plan(_parse(argv[1:]))
    except Refusal as exc:
        say(f"refused: {exc}")
        return 64
    return run_probe(plan)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
