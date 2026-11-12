"""`project_decisions._refs` on a document ref `doc:<path under qa-factory>[#<anchor>]`: one table of cases (OH3-24 Q-a).

The ref is outside input (a person's or a role's words). Expected values come from the row's direction, not from the code's
output (FR-58): a `:` anywhere in the path is refused (a URL or a drive), `./` is normalised away, an empty `#` is dropped,
`..`, a leading `/`, an empty path are refused. A refusal says what is wrong, what is expected and how to write it (FR-1, FR-2).
Cases the direction leaves open (spaces inside the path, a very long path, non-ASCII) pin the CURRENT behaviour: accepted as
typed, never a crash.

Runnable on its own: `python -B scripts/tests/test_project_decisions_doc_ref_form.py`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import check, check_eq, finish  # noqa: E402

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

finish("project_decisions doc ref form")
