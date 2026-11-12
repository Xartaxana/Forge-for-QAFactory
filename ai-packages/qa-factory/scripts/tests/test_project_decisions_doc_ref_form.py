"""`project_decisions._refs` on a document ref `doc:<path under qa-factory>[#<anchor>]`: one table of cases (OH3-24 Q-a).

The ref is outside input (a person's or a role's words). Expected values come from the row's direction, not from the code's
output (FR-58): a `:` anywhere in the path is refused (a URL or a drive), `./` is normalised away, an empty `#` is dropped,
`..`, a leading `/`, an empty path are refused. A refusal says what is wrong, what is expected and how to write it (FR-1, FR-2).
Cases the direction leaves open (spaces inside the path, a very long path, non-ASCII) pin the CURRENT behaviour: accepted as
typed, never a crash.

Runnable on its own: `python -B scripts/tests/test_project_decisions_doc_ref_form.py`."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, cleanup, finish, run_script, temp_project  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import project_decisions as PD  # noqa: E402

LONG = "d/" * 400 + "x.md"
EXPECTED = ("doc:<path under qa-factory>", "[#<anchor>]", "`:`", "`..`")

# (case id, input, expected normalised ref, or None when refused)
CASES = [
    ("plain", "doc:strategy/test-strategy.md", "doc:strategy/test-strategy.md"),
    ("anchor", "doc:strategy/test-strategy.md#risk-and-impact-scale", "doc:strategy/test-strategy.md#risk-and-impact-scale"),
    ("prefix-case", "DOC:a/b.md", "doc:a/b.md"),
    ("backslashes", "doc:strategy\\a.md", "doc:strategy/a.md"),
    ("dot-slash", "doc:./x", "doc:x"),
    ("dot-slash-twice", "doc:././a/./b.md#h", "doc:a/b.md#h"),
    ("empty-anchor", "doc:a.md#", "doc:a.md"),
    ("dot-slash-empty-anchor", "doc:./a.md#", "doc:a.md"),
    ("colon-in-anchor", "doc:a.md#x:y", "doc:a.md#x:y"),
    ("spaces-around-path", "doc:  a/b.md  #h", "doc:a/b.md#h"),
    ("spaces-inside-path", "doc:my dir/a b.md", "doc:my dir/a b.md"),
    ("long-path", "doc:" + LONG, "doc:" + LONG),
    ("non-ascii", "doc:strategy/\u0434\u043e\u043a.md#\u0440\u0438\u0441\u043a", "doc:strategy/\u0434\u043e\u043a.md#\u0440\u0438\u0441\u043a"),
    ("url", "doc:https://x", None),
    ("url-bare", "doc:http:x", None),
    ("drive", "doc:C:/x.md", None),
    ("drive-backslash", "doc:C:\\x.md", None),
    ("colon-mid-path", "doc:a/b:c.md", None),
    ("empty", "doc:", None),
    ("empty-with-anchor", "doc:#h", None),
    ("blank", "doc:   ", None),
    ("only-dot", "doc:.", None),
    ("only-dot-slash", "doc:./", None),
    ("leading-slash", "doc:/etc/x", None),
    ("leading-backslash", "doc:\\x", None),
    ("parent", "doc:../x", None),
    ("nested-parent", "doc:a/../../x.md", None),
    ("dot-slash-then-parent", "doc:./../x", None),
    ("parent-after-dot", "doc:a/./../x", None),
]


def attempt(item):
    try:
        return PD._refs([item]), None
    except ValueError as exc:
        return None, str(exc)


for case_id, item, want in CASES:
    got, err = attempt(item)
    if want is None:
        check(f"{case_id}: refused", got is None and err is not None, f"accepted as {got!r}")
        if err is not None:
            missing = [e for e in EXPECTED if e not in err]
            check(f"{case_id}: refusal names the form, what is wrong and the way out", not missing, f"missing {missing} in {err!r}")
            check(f"{case_id}: refusal is one line", "\n" not in err, repr(err))
    else:
        check_eq(f"{case_id}: normalised", got, [want])

# OH3-24 Q-b / Q-c: on the command line a refusal of `add` and `resolve` is ONE stderr line and exit 2 (as `add-finding`), never a
# traceback (exit 1); a marker file that leaves the root (drive, `:`, leading `/`, `..`, backslash forms) is such a refusal.
ADD = ["add", "--essence", "e", "--asked", "q", "--field-ref", "doc:a/b.md#h"]
MARKER_CASES = ["C:/x.md", "C:x.md", "/x.md", "\\x.md", "../x.md", "a/../../x.md", "a\\..\\..\\x.md", "https://x"]


def cli(root, *args):
    return run_script("project_decisions.py", "--root", root, *args)


root = temp_project()
try:
    words = root / "words.txt"
    words.write_text("yes\n", encoding="utf-8")
    cases = [("add: bad doc ref", ["add", "--essence", "e", "--asked", "q", "--field-ref", "doc:https://x"], 2),
             ("add: blank asked", ["add", "--essence", "e", "--asked", " ", "--field-ref", "doc:a/b.md"], 2),
             ("add: good row", ADD, 0),
             ("resolve: unknown id", ["resolve", "--id", "DD-99", "--words-file", str(words), "--resolution-ref", "r"], 2),
             ("resolve: blank resolution ref", ["resolve", "--id", "DD-1", "--words-file", str(words), "--resolution-ref", " "], 2)]
    cases += [(f"resolve: marker file {m!r}", ["resolve", "--id", "DD-1", "--words-file", str(words), "--resolution-ref", "r",
                                                "--marker-file", m], 2) for m in MARKER_CASES]
    for name, args, code in cases:
        done = cli(root, *args)
        check_eq(f"{name}: exit code", done.returncode, code)
        if code == 2:
            lines = done.stderr.strip().splitlines()
            check(f"{name}: one stderr line, no traceback", len(lines) == 1 and "Traceback" not in done.stderr, done.stderr[-300:])
            check(f"{name}: the line names the action", lines and lines[0].startswith(
                "project_decisions: " + args[0] + " refused - "), done.stderr[-300:])
    # OH3-24 Q-d: the phase text's "a key stays by the person's word" record names a DOCUMENT ref (a bookkeeping row that writes
    # nothing into config.json); the command as the text prints it, with its ref taken from the text, is accepted by `add`.
    # (The `/profiles` record stays a pointer on purpose: the open row is what lifts the first-reader gate.)
    p4 = (PLUGIN_ROOT / "skills" / "qa-onboarding" / "phases" / "p4-generate.md").read_text(encoding="utf-8")
    kept = re.search(r"add --field-ref\s+(\S+) --essence \"environment integrations kept", p4)
    check("p4 text: the integrations-kept record is found", kept is not None)
    ref = kept.group(1) if kept else ""
    check("p4 text: the integrations-kept ref is a document ref", ref.startswith("doc:"), ref)
    done = cli(root, "add", "--field-ref", ref, "--essence", "environment integrations kept by the person's word: config.json",
               "--asked", "q")
    check_eq("p4 text: the printed command is accepted by add", done.returncode, 0)
    check_eq("p4 text: the row holds the document ref", json.loads(done.stdout or "{}").get("field_refs"), ref)
finally:
    cleanup(root)

finish("project_decisions doc ref form")
