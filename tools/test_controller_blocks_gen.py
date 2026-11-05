"""Tests for tools/controller-blocks-gen.py - the generator of design/controller-blocks.md (C4-4).

The generator walks `controller.py` for every refusal and gives it a route. A refusal whose message is a
variable carries no literal, so its route comes from `BY_SEGMENT`, keyed by the source of the block. The
per-reference loops of `validate` collect `(ValueError, issue)` / `(StateConflict, issue)`; before C4-4 the
table knew only the `raise` spellings of those, so the map lost the explanation of the `prepare` row and
had no row for the loops.

Run from the repo root: python -m pytest tools/test_controller_blocks_gen.py -q
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

_spec = importlib.util.spec_from_file_location("controller_blocks_gen", TOOLS / "controller-blocks-gen.py")
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

CLASSES = frozenset({"ValueError", "StateConflict"})
CONTROLLER = gen.SRC.read_text(encoding="utf-8")

FIXTURE = '''
def check(refs, other):
    problems = []
    for ref in refs:
        issue = other(ref)
        if issue:
            problems.append((ValueError, issue))
    for ref in refs:
        issue = other(ref)
        if issue:
            problems.append((StateConflict, issue))
    return problems
'''


def routed(src: str):
    rows = gen.collect_rows(src, CLASSES)
    unknown = gen.route_rows(rows)
    return rows, unknown


def test_each_issue_pair_is_routed_to_its_own_explanation():
    rows, unknown = routed(FIXTURE)
    assert unknown == []
    by_seg = {row["seg"]: row for row in rows}
    assert sorted(by_seg) == ["(StateConflict, issue)", "(ValueError, issue)"]
    for seg, row in by_seg.items():
        assert (row["route"], row["note"]) == gen.BY_SEGMENT[seg]
        assert row["fn"] == "check"       # not a CALLER_FUNCTIONS name: only the table can have placed it
    assert by_seg["(ValueError, issue)"]["note"].startswith("a reference in the request that does not resolve")
    assert by_seg["(StateConflict, issue)"]["note"].startswith("dispatch a successor with the same scope and inputs")
    assert by_seg["(ValueError, issue)"]["note"] != by_seg["(StateConflict, issue)"]["note"]


def test_a_shape_not_in_the_table_stays_unclassified():
    """NEGATIVE control: a pair whose message is another variable has no route, and the generator would refuse."""
    src = FIXTURE.replace("(ValueError, issue)", "(ValueError, problem)").replace("(StateConflict, issue)",
                                                                                   "(StateConflict, problem)")
    rows, unknown = routed(src)
    assert len(rows) == 2 and len(unknown) == 2
    assert {row["route"] for row in unknown} == {"?"}
    assert {row["seg"] for row in unknown} == {"(ValueError, problem)", "(StateConflict, problem)"}


def test_the_old_raise_spellings_have_no_route_any_more():
    """The table keys the collected pair; a loop that raises its first reference alone is no longer a known shape."""
    src = "def check(ref, other):\n    issue = other(ref)\n    raise ValueError(issue)\n"
    rows, unknown = routed(src)
    assert [row["seg"] for row in rows] == ["raise ValueError(issue)"] and len(unknown) == 1


def test_every_block_of_the_controller_has_a_route():
    rows, unknown = routed(CONTROLLER)
    assert rows and unknown == [], [(row["line"], row["fn"], row["head"][:60]) for row in unknown]


def test_prepare_row_has_the_specific_explanation_and_the_loops_are_blocks():
    rows, _ = routed(CONTROLLER)
    pairs = [row for row in rows if row["seg"] in ("(ValueError, issue)", "(StateConflict, issue)")]
    assert {row["fn"] for row in pairs} == {"prepare", "validate"}
    prepare = [row for row in pairs if row["fn"] == "prepare"]
    assert [row["note"] for row in prepare] == [gen.BY_SEGMENT["(ValueError, issue)"][1]]
    assert not [row for row in prepare if row["note"].startswith("the request is malformed")]
    # the six per-reference loops of `validate`: reconcile, request_cancel, accept, policy, code_only, Gate A carry
    in_validate = [row["seg"] for row in pairs if row["fn"] == "validate"]
    # (C4-10: request_cancel's references are request fields, so only reconcile's stay StateConflict)
    assert sorted(in_validate) == ["(StateConflict, issue)"] * 1 + ["(ValueError, issue)"] * 5


def test_the_story_class_reference_pair_is_one_site_and_routes_to_a_command():
    """t-913 Q1/Q2: `(StateConflict, issue)` is ONE site - `reconcile_dispatch`'s stored successor evidence - routed to the
    command (a successor replaces the receipt, FR-2 and FR-57); `request_cancel`'s request-field references are `caller`."""
    rows, _ = routed(CONTROLLER)
    story = [row for row in rows if row["seg"] == "(StateConflict, issue)"]
    assert len(story) == 1, "a second site with this segment needs its own key: the table keys the segment alone"
    assert (story[0]["route"], story[0]["fn"]) == ("command", "validate")
    lines = CONTROLLER.splitlines()
    assert "successor evidence" in " ".join(lines[story[0]["line"] - 3:story[0]["line"] + 2])
    cancel = [row for row in rows if row["seg"] == "(ValueError, issue)"
              and "cancellation" in " ".join(lines[row["line"] - 1:row["line"] + 2])]
    assert len(cancel) == 1 and cancel[0]["route"] == "caller"
    # NEGATIVE control: the same pair in the old class would be the story's, with the command route
    assert gen.BY_SEGMENT["(ValueError, issue)"][0] == "caller" and gen.BY_SEGMENT["(StateConflict, issue)"][0] == "command"


def test_the_story_root_refusal_pair_is_one_site_of_the_cli_root():
    """CX1-10 (t-946 F-4): `(ValueError, str(exc))` is the key of ONE site - `_cli_story_root` passing on the refusal of
    `hooklib.story_root` - routed to the caller. The table keys the segment alone: a second site with this segment, in any
    function, would be handed that note, so it needs its own key."""
    rows, _ = routed(CONTROLLER)
    root = [row for row in rows if row["seg"] == "(ValueError, str(exc))"]
    assert len(root) == 1, "a second site with this segment needs its own key: the table keys the segment alone"
    assert (root[0]["route"], root[0]["fn"]) == ("caller", "_cli_story_root")
    assert root[0]["note"] == gen.BY_SEGMENT["(ValueError, str(exc))"][1]
    # NEGATIVE control: the same segment written twice (a copy of the site in another function) is found as two sites
    twice = CONTROLLER + "\n\ndef _other(a):\n    problems = []\n    try:\n        a()\n    except ValueError as exc:\n" \
                         "        problems.append((ValueError, str(exc)))\n    Controller._raise_all(problems)\n"
    again, _ = routed(twice)
    assert len([row for row in again if row["seg"] == "(ValueError, str(exc))"]) == 2


def test_no_loop_of_the_controller_raises_its_first_bad_reference_alone():
    """The class of C4-4: a reference loop refuses through `_raise_all`, never with `raise X(issue)`."""
    rows, _ = routed(CONTROLLER)
    assert [row for row in rows if row["seg"] in ("raise ValueError(issue)", "raise StateConflict(issue)")] == []


def functions_missing(names, src: str) -> set:
    defined = {node.name for node in ast.walk(ast.parse(src)) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    return set(names) - defined


def test_caller_functions_names_only_functions_the_controller_defines():
    assert functions_missing(gen.CALLER_FUNCTIONS, CONTROLLER) == set()
    # NEGATIVE control: the same helper names a function that is gone (`validate_known_paths`, deleted by C3-11)
    assert functions_missing(gen.CALLER_FUNCTIONS | {"validate_known_paths"}, CONTROLLER) == {"validate_known_paths"}
