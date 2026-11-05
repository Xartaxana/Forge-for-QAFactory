"""project_decisions._replace_table: ONE table replacer for the deferred decisions and the findings (B-309 e).

`_replace_findings` was `_replace_table` with another heading and another header, statement for statement. The golden
strings below were produced by BOTH old functions on the same fixtures BEFORE the merge (they were equal to each other
modulo the heading and the header) and are pasted here as literals: the merged function must reproduce them byte for byte,
for the section absent, present with a table, present with no table, last in the file, and with the next table beyond the
next heading (the shapes of the original's four branches).

Runnable on its own: `python -B scripts/tests/test_project_decisions_tables.py`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import check, check_eq, finish  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import project_decisions as PD  # noqa: E402

DD_ROWS = [
    {"id": "DD-1", "essence + where the marker is": "pipe | inside\nand a newline", "status": "open", "field_refs": "/a/b"},
    {"id": "DD-2", "essence + where the marker is": "plain", "status": "decided", "scope": "x"},
]
FB_ROWS = [
    {"id": "FB-1", "essence": "pipe | inside\nand a newline", "scope": "local-urgent", "status": "open"},
    {"id": "FB-2", "essence": "plain", "scope": "upstream-candidate", "witness/details": "w; idempotency:k", "decision": "-"},
]
DD_HEAD = "## Deferred decisions (onboarding/gates)"
FB_HEAD = "## Findings about the factory"
DD_TABLE = (
    "| id | essence + where the marker is | asked | ripeness trigger | created | status | decision with witness | field_refs"
    " | scope | owner | trigger_type | trigger_value | resolution_ref |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    "| DD-1 | pipe \\| inside and a newline |  |  |  | open |  | /a/b |  |  |  |  |  |\n"
    "| DD-2 | plain |  |  |  | decided |  |  | x |  |  |  |  |\n")
FB_TABLE = (
    "| id | essence | scope | witness/details | created | status | decision |\n"
    "|---|---|---|---|---|---|---|\n"
    "| FB-1 | pipe \\| inside and a newline | local-urgent |  |  | open |  |\n"
    "| FB-2 | plain | upstream-candidate | w; idempotency:k |  |  | - |\n")
OTHER = "## Other\n\ntext\n"
OLD = "| old | table |\n|---|---|\n| x | y |\n"


def fixtures(head: str) -> dict:
    """name -> (text in, text out given `table`): the out side is a template with `{t}` for the rendered table."""
    return {
        "section absent, empty file": ("", head + "\n\n{t}"),
        "section absent, prose last": ("# Title\n\nSome prose\n", "# Title\n\nSome prose\n\n" + head + "\n\n{t}"),
        "section with a table, another section after it": (f"# T\n\n{head}\n\n{OLD}\n{OTHER}", f"# T\n\n{head}\n\n{{t}}\n{OTHER}"),
        "section last, heading straight above the table (no blank line is added)": (f"# T\n\n{head}\n", f"# T\n\n{head}\n{{t}}"),
        "no table under the section, the next table is beyond the next heading": (
            f"# T\n\n{head}\n\n{OTHER}\n| late | table |\n|---|---|\n",
            f"# T\n\n{head}\n\n{{t}}{OTHER}\n| late | table |\n|---|---|\n"),
    }


def run(label: str, head: str, table: str, call) -> None:
    for name, (text, template) in fixtures(head).items():
        check_eq(f"{label}: {name}", call(text), template.format(t=table))


def test_the_deferred_decisions_are_the_default() -> None:
    run("G1 deferred decisions (defaults)", DD_HEAD, DD_TABLE, lambda text: PD._replace_table(text, DD_ROWS))
    run("G1 deferred decisions (named)", DD_HEAD, DD_TABLE,
        lambda text: PD._replace_table(text, DD_ROWS, PD.HEADING, PD.HEADER))


def test_the_findings_are_the_same_function_with_their_own_heading_and_header() -> None:
    run("G2 findings", FB_HEAD, FB_TABLE, lambda text: PD._replace_table(text, FB_ROWS, PD.FB_HEADING, PD.FB_HEADER))
    check("G2 the old findings copy is gone", not hasattr(PD, "_replace_findings"))


def test_no_rows_renders_the_header_alone_and_keeps_the_rest() -> None:
    text = f"# T\n\n{DD_HEAD}\n\n{OLD}\n{OTHER}"
    out = PD._replace_table(text, [])
    check_eq("G3 deferred decisions, no rows", out, f"# T\n\n{DD_HEAD}\n\n" + DD_TABLE.split("| DD-1")[0] + f"\n{OTHER}")
    text = f"# T\n\n{FB_HEAD}\n\n{OLD}\n{OTHER}"
    out = PD._replace_table(text, [], PD.FB_HEADING, PD.FB_HEADER)
    check_eq("G3 findings, no rows", out, f"# T\n\n{FB_HEAD}\n\n" + FB_TABLE.split("| FB-1")[0] + f"\n{OTHER}")


def test_a_section_is_found_by_its_own_heading_only() -> None:
    """The invariant of the parameter: the findings call never touches the decisions' table and the reverse."""
    both = f"# T\n\n{DD_HEAD}\n\n{DD_TABLE}\n{FB_HEAD}\n\n{FB_TABLE}"
    only_fb = PD._replace_table(both, [], PD.FB_HEADING, PD.FB_HEADER)
    check("G4 the decisions' rows survive a findings rewrite", "| DD-1 |" in only_fb and "| FB-1 |" not in only_fb)
    only_dd = PD._replace_table(both, [])
    check("G4 the findings' rows survive a decisions rewrite", "| FB-1 |" in only_dd and "| DD-1 |" not in only_dd)


if __name__ == "__main__":
    test_the_deferred_decisions_are_the_default()
    test_the_findings_are_the_same_function_with_their_own_heading_and_header()
    test_no_rows_renders_the_header_alone_and_keeps_the_rest()
    test_a_section_is_found_by_its_own_heading_only()
    finish("project_decisions_tables")
