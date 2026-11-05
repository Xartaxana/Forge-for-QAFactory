"""Tests for tools/digest_form.py and tools/md_table.py (t-797 F5-2, node N1): the reader of the scout digest form v1.

The invariant under test is I1: the reader may flag too much but must never say "no flags" about a claim without a trail, or a
negative without a positive control of the same call shape; and I2: it only reports. The example of the form is read from the
note docs/tasks/exchange-form.md, so the note and the reader cannot drift apart. Edges are the spec's section 5 (E1-E11).

Run from the repo root: python -m pytest tools/test_digest_form.py -q
"""
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

import digest_form as DF  # noqa: E402
import md_table  # noqa: E402

NOTE = ROOT / "docs" / "tasks" / "exchange-form.md"
HARNESS = ROOT / "gateway" / "PI_HARNESS.md"
DASH = "—"


def obj(id="a1", kind="claim", gist="g", paths="x.py:1", status="open", owner=DASH, links=DASH, ev="R1"):
    return "| " + " | ".join([id, kind, gist, paths, status, owner, links, ev]) + " |"


def trail(tid="R1", op="read", target="x.py", pattern="all", flags=DASH, result="read x.py:1", control=DASH):
    return "| " + " | ".join([tid, op, target, pattern, flags, result, control]) + " |"


def zero(tid="G1", control="G2", flags="-i content", target="tools/", pattern="`nope`", result="absent", op="grep"):
    return trail(tid, op, target, pattern, flags, result, control)


def found(tid="G2", flags="-i content", target="tools/", pattern="`yes`", result="found 2; a.py:1, b.py:2", op="grep"):
    return trail(tid, op, target, pattern, flags, result, DASH)


def digest(objects=(obj(),), trails=(trail(),), forks=None, not_done=None, key="digest: v1 t-1", pre="", objects_header=None,
           trail_header=None):
    lines = [pre] if pre else []
    lines += [key, "## Objects", objects_header or "| " + " | ".join(DF.OBJECTS_HEADER) + " |", "|---|---|---|---|---|---|---|---|"]
    lines += list(objects)
    lines += ["## Trail", trail_header or "| " + " | ".join(DF.TRAIL_HEADER) + " |", "|---|---|---|---|---|---|---|"]
    lines += list(trails)
    if forks is not None:
        lines += ["## Forks", forks]
    if not_done is not None:
        lines += ["## Not done", not_done]
    return "\n".join(lines) + "\n"


def flags_of(text):
    d = DF.parse(text)
    assert d is not None
    return DF.flags(d)


def example_block(text=None):
    """The t-794 example of the note: the fenced block that starts with its key line."""
    text = NOTE.read_text(encoding="utf-8") if text is None else text
    blocks = re.findall(r"^```\n(digest: v1 t-794\n.*?)\n```$", text, re.S | re.M)
    assert len(blocks) == 1, "the note must carry the t-794 example exactly once"
    return blocks[0]


# ----- the example of the note, the clean case, no key -----------------------------------------------------------------

def test_the_example_of_the_note_flags_exactly_the_two_it_names():
    d = DF.parse(example_block())
    assert d.task_id == "t-794" and (d.n_objects, d.n_trail) == (11, 17)
    assert DF.flags(d) == ["control_shape:G8", "zero_uncontrolled:q3b:G8"]


def test_negative_control_of_the_example_reader():
    """The extractor of the example fails on a text without it (and on a text with it twice): it cannot pass vacuously."""
    with pytest.raises(AssertionError):
        example_block("no example here")
    block = "```\n" + example_block() + "\n```\n"
    with pytest.raises(AssertionError):
        example_block(block + block)


def test_the_minimal_clean_digest_has_no_flags():
    d = DF.parse(digest())
    assert d.task_id == "t-1" and DF.flags(d) == []


FLAG_SHAPE = re.compile(r"[a-z]+(?:_[a-z]+)+(?::.*)?", re.S)       # a string literal that reads like a flag: snake_case[:anything]


def emitted_flag_names(source):
    """The flag names the source of a module can build: every string literal shaped like a flag, cut at its first colon, EXCEPT the
    FLAG_NAMES tuple itself (the list under test is not its own evidence). A single-word flag would not be seen: every flag so far
    has an underscore, and the corpus test below catches the rest."""
    tree = ast.parse(source)
    own = {id(c) for node in tree.body if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "FLAG_NAMES" for t in node.targets)
           for c in ast.walk(node)}
    return {n.value.split(":")[0] for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in own and FLAG_SHAPE.fullmatch(n.value)}


def test_the_flag_name_list_is_the_one_list_the_reader_note_and_corpus_agree_with():
    """t-863 (F6-14, the third item of t-808's leftovers): FLAG_NAMES lives once, in digest_form, and is checked against the code that
    EMITS the flags (a new flag in the reader but not in the list fails here), against the note, and against the real flags of every
    probe of this file."""
    source = Path(DF.__file__).read_text(encoding="utf-8")
    assert emitted_flag_names(source) == set(DF.FLAG_NAMES) | set(DF.TRANSCRIPT_FLAG_NAMES)
    assert len(set(DF.FLAG_NAMES)) == len(DF.FLAG_NAMES)
    note = NOTE.read_text(encoding="utf-8")
    assert [n for n in DF.FLAG_NAMES if n not in note] == []
    seen = {f.split(":")[0] for _, text in UNCOMFORTABLE for f in flags_of(text)} | {f.split(":")[0] for f in flags_of(example_block())}
    assert seen <= set(DF.FLAG_NAMES)


def test_negative_control_of_the_flag_name_scan():
    """A reader that builds a flag the list does not name makes the scan differ; a name only in the list makes it differ the other way."""
    source = Path(DF.__file__).read_text(encoding="utf-8")
    known = set(DF.FLAG_NAMES) | set(DF.TRANSCRIPT_FLAG_NAMES)
    assert emitted_flag_names(source + '\nNEW = "brand_new_flag:" + "x"\n') - known == {"brand_new_flag"}
    assert known - emitted_flag_names(source.replace('"fence_unclosed:%d"', '"x"')) == {"fence_unclosed"}
    assert emitted_flag_names('FLAG_NAMES = ("only_in_list",)\n') == set()


@pytest.mark.parametrize("text", ["", "prose only\nwith lines", "digest: v2 t-1\n## Objects", "digest:v1 t-1", "x digest: v1 t-1",
                                  "## Objects\n| id |\n"])
def test_no_key_line_is_none(text):
    assert DF.parse(text) is None


# ----- E1 ids ------------------------------------------------------------------------------------------------------------

def test_e1_object_without_an_id_is_flagged_and_counted():
    d = DF.parse(digest(objects=[obj(id="")]))
    assert d.n_objects == 1
    assert DF.flags(d) == ["no_id:1"]


def test_e1_no_id_row_is_named_by_its_number_in_the_other_flags():
    assert flags_of(digest(objects=[obj(), obj(id="", ev=DASH)])) == ["no_id:2", "no_ev:#2"]


@pytest.mark.parametrize("bad", ["a b", "a,b", "a, b"])
def test_e1_id_with_a_space_or_a_comma(bad):
    assert flags_of(digest(objects=[obj(id=bad)])) == ["id_space:1"]


def test_e1_repeated_id_is_flagged_and_every_row_is_still_checked():
    assert flags_of(digest(objects=[obj(), obj(ev=DASH)])) == ["dup_id:a1", "no_ev:a1"]


# ----- E2 the gist limit, at and beyond it ----------------------------------------------------------------------------------

def test_e2_gist_of_20_words_is_clean_and_of_21_is_flagged():
    twenty = " ".join(["w"] * 20)
    assert flags_of(digest(objects=[obj(gist=twenty)])) == []
    assert flags_of(digest(objects=[obj(gist=twenty + " w")])) == ["gist_over:a1"]


def test_e2_words_are_str_split_words_nbsp_and_cyrillic_included():
    nbsp = " ".join(["слово"] * 21)
    assert flags_of(digest(objects=[obj(gist=nbsp)])) == ["gist_over:a1"]
    assert flags_of(digest(objects=[obj(gist=" ".join(["слово"] * 20))])) == []


def test_e2_a_huge_gist_is_flagged_once_and_not_cut():
    big = " ".join(["w"] * 50000)
    d = DF.parse(digest(objects=[obj(gist=big)]))
    assert DF.flags(d) == ["gist_over:a1"]
    assert d.object_rows[0][2] == big


# ----- E3 the trail of an object ---------------------------------------------------------------------------------------------

@pytest.mark.parametrize("ev", ["", DASH, ",", " , "])
def test_e3_an_object_with_no_ev_is_flagged(ev):
    assert flags_of(digest(objects=[obj(ev=ev)])) == ["no_ev:a1"]


def test_e3_unknown_tid_is_flagged_and_the_comparison_is_exact():
    assert flags_of(digest(objects=[obj(ev="R1,R9")])) == ["ev_unknown:a1:R9"]
    assert flags_of(digest(objects=[obj(ev="r1")])) == ["ev_unknown:a1:r1"]


def test_e3_a_trailing_comma_and_spaces_around_a_tid_are_ignored():
    assert flags_of(digest(objects=[obj(ev="R1,"), obj(id="a2", ev=" R1 , ")])) == []


# ----- E4 the closed grammar of result -----------------------------------------------------------------------------------------

@pytest.mark.parametrize("op,fl,result", [
    ("grep", "-i content", "found 1"), ("grep", "-i content", "found 12; a.py:1, b.py:3"), ("grep", "-i count", "count 3"),
    ("glob", DASH, "found 4; a, b"), ("glob", DASH, "absent"), ("grep", "-i count", "count 0"), ("grep", "-i", "absent"),
    ("read", DASH, "read plans/x.md:all"), ("read", DASH, "read a.py:1-10,40")])
def test_e4_results_inside_the_grammar_are_not_flagged_as_bad(op, fl, result):
    d = DF.parse(digest(objects=[obj(ev="G1")], trails=[trail("G1", op, "t", "`p`", fl, result, DASH)]))
    assert not [f for f in DF.flags(d) if f.startswith("bad_result")]


@pytest.mark.parametrize("op,fl,result", [
    ("grep", "-i content", "found 0"), ("grep", "-i content", "0"), ("grep", "-i content", "0 matches"),
    ("grep", "-i content", "found 007"), ("grep", "-i content", "found 1;"), ("grep", "-i content", "count 2"),
    ("grep", "-i content", "read a:1"), ("grep", "-i content", "none"), ("grep", "-i content", "Absent"),
    ("grep", "-i content", "found ٣"),
    ("grep", "-i count", "count 01"), ("grep", "-i count", "count"), ("grep", "-i count", "found 3"), ("grep", "-i count", "absent"),
    ("glob", DASH, "count 0"), ("glob", DASH, "found 0"),
    ("read", DASH, "absent"), ("read", DASH, "read a.py:"), ("read", DASH, "read :1"), ("read", DASH, "found 2"),
    ("read", DASH, "3 lines")])
def test_e4_a_result_outside_the_grammar_is_bad_result_and_is_neither_zero_nor_control(op, fl, result):
    text = digest(objects=[obj(ev="G1")], trails=[trail("G1", op, "t", "`p`", fl, result, DASH)])
    assert flags_of(text) == ["bad_result:G1"]


def test_e4_found_0_is_not_a_zero_so_it_asks_for_no_control():
    """U8: `found 0` read as a zero would earn zero_no_control instead of bad_result."""
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", DASH, result="found 0")])) == ["bad_result:G1"]


def test_e4_a_bad_result_cannot_be_a_control():
    flags = flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2"), found("G2", result="found 0")]))
    assert flags == ["control_shape:G1", "bad_result:G2", "zero_uncontrolled:a1:G1"]


def test_e4_count_zero_is_a_zero_and_needs_a_control():
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", DASH, flags="-i count", result="count 0")])) == [
        "zero_no_control:G1", "zero_uncontrolled:a1:G1"]


# ----- E5 the control of a zero row --------------------------------------------------------------------------------------------

def test_e5_a_good_control_is_clean_even_when_it_comes_later_in_the_table():
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2"), found("G2")])) == []
    assert flags_of(digest(objects=[obj(ev="G1,G2")], trails=[found("G2"), zero("G1", "G2")])) == []


@pytest.mark.parametrize("control,expected", [(DASH, "zero_no_control:G1"), ("", "zero_no_control:G1"),
                                              ("G9", "control_unknown:G1"), ("g2", "control_unknown:G1"),
                                              ("G2, G3", "control_unknown:G1")])
def test_e5_a_missing_or_unknown_control(control, expected):
    flags = flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", control), found("G2"), found("G3")]))
    assert flags == [expected, "zero_uncontrolled:a1:G1"]


@pytest.mark.parametrize("name,control_row", [
    ("other op", trail("G2", "glob", "tools/", "`yes`", "-i content", "found 2", DASH)),
    ("other target", found("G2", target="scripts/")),
    ("other flags", found("G2", flags="content")),
    ("extra flag", found("G2", flags="-i content type=py")),
    ("same pattern", found("G2", pattern="`nope`")),
    ("a read", trail("G2", "read", "tools/", "`yes`", "-i content", "read a.py:1", DASH))])
def test_e5_a_control_of_another_shape(name, control_row):
    flags = flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2"), control_row]))
    assert flags == ["control_shape:G1", "zero_uncontrolled:a1:G1"], name


def test_e5_flags_are_compared_as_a_set():
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2", flags="-i content"), found("G2", flags="content -i")])) == []


def test_e5_the_control_is_the_row_itself_or_a_zero():
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G1")])) == ["control_shape:G1", "zero_uncontrolled:a1:G1"]
    flags = flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2"), zero("G2", "G3", pattern="`other`"), found("G3")]))
    assert flags == ["control_shape:G1", "zero_uncontrolled:a1:G1"]


# ----- E6 case --------------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("fl", ["content", "content count"])
def test_e6_a_zero_grep_without_dash_i(fl):
    result = "count 0" if "count" in fl else "absent"
    flags = flags_of(digest(objects=[obj(ev="G1")], trails=[zero("G1", "G2", flags=fl, result=result),
                                                            found("G2", flags=fl, result="count 4" if "count" in fl else "found 1")]))
    assert flags == ["zero_case:G1"]


def test_e6_a_zero_glob_needs_no_dash_i_and_a_found_grep_either():
    glob0 = trail("G1", "glob", "tools/", "`*.zz`", DASH, "absent", "G2")
    glob1 = trail("G2", "glob", "tools/", "`*.py`", DASH, "found 3; a.py", DASH)
    assert flags_of(digest(objects=[obj(ev="G1")], trails=[glob0, glob1])) == []
    assert flags_of(digest(objects=[obj(ev="G2")], trails=[found("G2", flags="content")])) == []


# ----- E7 the object level -------------------------------------------------------------------------------------------------

def test_e7_any_zero_row_of_ev_without_a_good_control_flags_the_object():
    flags = flags_of(digest(objects=[obj(ev="G1,G3")], trails=[zero("G1", "G2"), found("G2"), zero("G3", "G2", target="x/")]))
    assert flags == ["control_shape:G3", "zero_uncontrolled:a1:G3"]


def test_e7_an_absent_object_must_stand_on_a_zero_row():
    assert flags_of(digest(objects=[obj(status="absent", ev="R1")])) == ["absent_no_negative:a1"]
    assert flags_of(digest(objects=[obj(status="absent", ev="G1")], trails=[zero("G1", "G2"), found("G2")])) == []
    assert flags_of(digest(objects=[obj(status="Absent.", ev="R1")])) == ["absent_no_negative:a1"]
    assert flags_of(digest(objects=[obj(status="present", ev="R1")])) == []


def test_e7_an_absent_object_on_an_uncontrolled_zero_gets_the_first_flag_not_the_second():
    flags = flags_of(digest(objects=[obj(status="absent", ev="G1")], trails=[zero("G1", DASH)]))
    assert flags == ["zero_no_control:G1", "zero_uncontrolled:a1:G1"]


def test_e7_an_object_whose_ev_is_only_a_bad_row_does_not_stand_as_a_negative():
    flags = flags_of(digest(objects=[obj(status="absent", ev="G1")], trails=[zero("G1", "G2", result="0")]))
    assert flags == ["bad_result:G1", "absent_no_negative:a1"]


# ----- E8 markup of rows -----------------------------------------------------------------------------------------------------

def test_e8_a_pipe_outside_backticks_is_a_bad_row_and_columns_do_not_shift():
    broken = "| G1 | grep | tools/ | `a`|`b` | -i | absent | G2 |"          # the pipe outside the backticks adds a cell
    d = DF.parse(digest(objects=[obj(ev="R1")], trails=[trail(), broken, found("G2")]))
    assert DF.flags(d) == ["bad_row:Trail:2"]
    assert d.n_trail == 3


def test_e8_a_bad_row_is_still_a_known_tid_for_the_objects_but_never_a_zero_or_a_control():
    broken = "| G1 | grep | tools/ | `a`|`b` | -i | absent | G2 |"
    flags = flags_of(digest(objects=[obj(status="absent", ev="G1")], trails=[broken, found("G2")]))
    assert flags == ["bad_row:Trail:1", "absent_no_negative:a1"]


def test_e8_a_pipe_inside_backticks_is_data():
    assert flags_of(digest(objects=[obj(ev="G1,G2")], trails=[zero("G1", "G2", pattern="`a|b|c`"), found("G2", pattern="`d|e`")])) == []


def test_e8_an_object_row_with_a_wrong_cell_count():
    assert flags_of(digest(objects=[obj(), "| a2 | claim | g | x | open | " + DASH + " |"])) == ["bad_row:Objects:2"]


def test_e8_an_unknown_op_or_an_empty_tid_is_a_bad_row():
    flags = flags_of(digest(trails=[trail(), trail("R2", op="run"), trail(tid="")]))
    assert flags == ["bad_row:Trail:2", "bad_row:Trail:3"]


def test_e8_a_repeated_tid_is_flagged_and_the_later_row_is_not_read():
    flags = flags_of(digest(trails=[trail(), zero("R1", DASH)]))
    assert flags == ["dup_tid:R1"]


def test_e8_a_tid_with_a_space_inside_is_flagged_and_trailing_space_is_not_part_of_the_tid():
    assert flags_of(digest(objects=[obj(ev="R 1")], trails=[trail("R 1")])) == ["tid_space:1"]
    assert flags_of(digest(objects=[obj(ev="R1 ")], trails=[trail("R1 ")])) == []


@pytest.mark.parametrize("which", ["objects", "trail"])
def test_e8_a_header_that_is_not_the_exact_one_is_flagged_and_its_rows_are_not_read(which):
    swapped = "| kind | id | gist | paths | status | owner | links | ev |"
    short = "| tid | op | target | pattern / range | flags | result |"
    if which == "objects":
        text = digest(objects_header=swapped, objects=[obj(id="", ev=DASH)])
        assert flags_of(text) == ["bad_header:Objects"]
    else:
        text = digest(trail_header=short, trails=[zero("R1", DASH)])
        assert flags_of(text) == ["ev_unknown:a1:R1", "bad_header:Trail"]


def test_e8_a_section_without_a_table_is_a_bad_header():
    text = "digest: v1 t-1\n## Objects\nnothing here\n## Trail\n" + "| " + " | ".join(DF.TRAIL_HEADER) + " |\n|---|---|---|---|---|---|---|\n"
    assert flags_of(text) == ["bad_header:Objects"]


# ----- E9 sections -------------------------------------------------------------------------------------------------------------

def test_e9_a_section_twice_the_first_is_read():
    text = digest() + "## Trail\n" + "| " + " | ".join(DF.TRAIL_HEADER) + " |\n|---|---|---|---|---|---|---|\n" + zero("R7", DASH) + "\n"
    assert flags_of(text) == ["dup_section:Trail"]


def test_e9_missing_required_sections():
    text = "digest: v1 t-1\n## Not done\nnothing\n"
    assert flags_of(text) == ["no_section:Objects", "no_section:Trail"]
    assert flags_of("digest: v1 t-1\n") == ["no_section:Objects", "no_section:Trail"]


def test_e9_a_heading_is_the_exact_name():
    text = digest().replace("## Objects", "## objects")
    assert flags_of(text) == ["no_section:Objects", "unknown_section:objects"]


def test_e9_forks_are_optional_and_end_with_the_literal_line():
    assert flags_of(digest(forks=None)) == []
    assert flags_of(digest(forks="A fork.\nthis needs a decision from a tier above.")) == []
    assert flags_of(digest(forks="A fork.\nthis needs a decision from a tier above.\n", not_done="x")) == []
    assert flags_of(digest(forks="A fork. I recommend A.")) == ["forks_no_line"]
    assert flags_of(digest(forks="")) == ["forks_no_line"]


def test_e9_not_done_is_optional():
    assert flags_of(digest(not_done="No Bash.")) == []


# ----- E10 the key --------------------------------------------------------------------------------------------------------------

def test_e10_a_preamble_before_the_key_is_flagged_and_reading_starts_at_the_key():
    d = DF.parse(digest(pre="Here is my digest:"))
    assert d.task_id == "t-1" and DF.flags(d) == ["key_not_first"]


def test_e10_a_fence_around_the_digest_is_flagged_and_still_read():
    d = DF.parse("```\n" + digest() + "```\n")
    assert DF.flags(d) == ["key_not_first"] and d.n_objects == 1


def test_e10_blank_lines_before_the_key_are_not_a_preamble():
    assert flags_of("\n\n" + digest()) == []


def test_e10_a_key_without_a_task_id():
    d = DF.parse(digest(key="digest: v1"))
    assert d.task_id is None and DF.flags(d) == ["key_no_task"]


# ----- the input forms and the safe direction -------------------------------------------------------------------------------------

def test_crlf_and_cr_read_like_lf():
    lf = digest(objects=[obj(), obj(id="a2", ev="G1")], trails=[trail(), zero("G1", DASH)], forks="f\nthis needs a decision from a tier above.")
    expect = flags_of(lf)
    assert expect                                   # the fixture carries real flags, so the comparison is not vacuous
    assert flags_of(lf.replace("\n", "\r\n")) == expect
    assert flags_of(lf.replace("\n", "\r")) == expect


def test_cyrillic_cells_are_read_like_any_other():
    text = digest(objects=[obj(id="вопрос1", gist="смысл", paths="файл.py:1", status="открыто", ev="Р1")], trails=[trail("Р1", target="файл.py")])
    assert flags_of(text) == []
    other = digest(objects=[obj(id="вопрос1", ev="Р1")], trails=[trail("Р2", target="файл.py")])
    assert flags_of(other) == ["ev_unknown:вопрос1:Р1"]


# ----- t-810 (the critic's FX-1 / FX-2): rows outside the first table, comments and fences ----------------------------------------

OH = "| " + " | ".join(DF.OBJECTS_HEADER) + " |"
OSEP = "|---|---|---|---|---|---|---|---|"
TH = "| " + " | ".join(DF.TRAIL_HEADER) + " |"
TSEP = "|---|---|---|---|---|---|---|"
OBJ_OK = [OH, OSEP, obj()]
TRAIL_OK = [TH, TSEP, trail()]
HIDDEN = obj(id="b1", status="absent", ev=DASH)          # an `absent` claim with no trail: the object every probe tries to hide


def raw(objects_lines, trail_lines, tail=(), key="digest: v1 t-1"):
    """A digest whose Objects and Trail sections are given line by line (the `digest()` helper always writes one clean table)."""
    return "\n".join([key, "## Objects", *objects_lines, "## Trail", *trail_lines, *tail]) + "\n"


# (name, text, the flag NAME that must come out): the critic's probes P1-P5 and P9-P11 of t-808, every one a claim that was dropped
# with flags=0 before the stray-row check
STRAY_PROBES = [
    ("P1 a second Objects table after a blank line", raw(OBJ_OK + ["", OH, OSEP, HIDDEN], TRAIL_OK), "stray_row:Objects:"),
    ("P2 a row after a prose line", raw(OBJ_OK + ["a prose line", HIDDEN], TRAIL_OK), "stray_row:Objects:"),
    ("P3 an indented row", raw(OBJ_OK + ["  " + HIDDEN], TRAIL_OK), "stray_row:Objects:"),
    ("P4 a second Trail table with an uncontrolled zero", raw(OBJ_OK, TRAIL_OK + ["", TH, TSEP, zero("Z1", DASH)]), "stray_row:Trail:"),
    ("P5 a fenced example table first, the real table after", raw(["```", OH, OSEP, obj(id="ex"), "```", OH, OSEP, HIDDEN], TRAIL_OK), "no_ev:b1"),
    ("P9 a data row of dashes", raw(OBJ_OK + ["| -- | -- | -- | -- | -- | -- | -- | -- |"], TRAIL_OK), "stray_row:Objects:"),
    ("P10 an unknown section holding a table", raw(OBJ_OK, TRAIL_OK, tail=["## Extra objects", OH, OSEP, HIDDEN]), "unknown_section:Extra objects"),
    ("P11 a table under each ### sub-heading", raw(["### group A", OH, OSEP, obj(), "### group B", OH, OSEP, HIDDEN], TRAIL_OK), "stray_row:Objects:"),
]

UNCOMFORTABLE = [
    *[(name, text) for name, text, _ in STRAY_PROBES],
    ("no ev", digest(objects=[obj(ev=DASH)])),
    ("unknown ev", digest(objects=[obj(ev="Z9")])),
    ("zero without control", digest(trails=[zero("R1", DASH)])),
    ("zero with a control of another shape", digest(trails=[zero("R1", "G2"), found("G2", target="elsewhere/")])),
    ("found 0", digest(trails=[zero("R1", "G2", result="found 0"), found("G2")])),
    ("absent with no negative", digest(objects=[obj(status="absent")])),
    ("pipe outside backticks", digest(trails=["| R1 | grep | tools/ | `a`|`b` | -i | absent | G2 |"])),
    ("wrong header", digest(trail_header="| tid | op |")),
    ("repeated tid", digest(trails=[trail(), trail()])),
    ("tid with a space", digest(trails=[trail("R 1")])),
    ("zero grep, no -i", digest(trails=[zero("R1", "G2", flags="content"), found("G2", flags="content")])),
    ("an unclosed fence hides a row and the Trail", raw(OBJ_OK + ["```", HIDDEN], TRAIL_OK)),
    ("an unclosed fence in the last section", digest(not_done="```\nhidden")),
]


@pytest.mark.parametrize("name,text", UNCOMFORTABLE, ids=[n for n, _ in UNCOMFORTABLE])
def test_the_safe_direction_an_uncomfortable_input_is_never_flags_zero(name, text):
    assert flags_of(text), name


@pytest.mark.parametrize("name,text,expected", STRAY_PROBES, ids=[n for n, _, _ in STRAY_PROBES])
def test_the_stray_probes_come_out_with_their_own_flag_name(name, text, expected):
    assert any(f.startswith(expected) for f in flags_of(text)), (name, flags_of(text))


def test_stray_rows_are_numbered_inside_the_section_heading_being_line_1():
    text = raw(OBJ_OK + ["", OH, OSEP, HIDDEN], TRAIL_OK)
    assert flags_of(text) == ["stray_row:Objects:6", "stray_row:Objects:7", "stray_row:Objects:8"]
    assert flags_of(raw(OBJ_OK + ["a prose line", HIDDEN], TRAIL_OK)) == ["stray_row:Objects:6"]
    assert flags_of(raw(OBJ_OK + ["| -- | -- | -- | -- | -- | -- | -- | -- |"], TRAIL_OK)) == ["stray_row:Objects:5"]
    assert flags_of(raw(["### group A", OH, OSEP, obj(), "### group B", OH, OSEP, HIDDEN], TRAIL_OK)) == \
        ["stray_row:Objects:7", "stray_row:Objects:8", "stray_row:Objects:9"]


def test_only_objects_and_trail_have_tables_a_pipe_line_in_forks_or_not_done_is_not_stray():
    table = "| a | b |\n|---|---|\n| 1 | 2 |"
    assert flags_of(digest(forks=table + "\nthis needs a decision from a tier above.", not_done=table)) == []


def test_a_wrong_header_followed_by_a_correct_table_flags_the_header_and_the_whole_second_table():
    swapped = "| kind | id | gist | paths | status | owner | links | ev |"
    text = raw([swapped, OSEP, obj(id="", ev=DASH), "", OH, OSEP, obj()], TRAIL_OK)
    assert flags_of(text) == ["bad_header:Objects", "stray_row:Objects:6", "stray_row:Objects:7", "stray_row:Objects:8"]


def test_a_section_with_only_a_sub_heading_has_no_table_and_no_stray_rows():
    assert flags_of(raw(["### group A"], TRAIL_OK)) == ["bad_header:Objects"]


def test_an_unknown_section_is_named_once_however_many_times_it_comes():
    text = digest(not_done="x") + "## Extra\nx\n## Extra\ny\n## Other\nz\n"
    assert flags_of(text) == ["unknown_section:Extra", "unknown_section:Other"]


# ----- t-810 FX-2: comments and fences ------------------------------------------------------------------------------------------

@pytest.mark.parametrize("pre", ["<!-- note -->", "<!-- a\nb\nc -->", "<!-- one --> <!-- two -->", "```\nan example\n| not | data |\n```",
                                 "<!-- c -->\n```\nx\n```\n\n"])
def test_a_comment_or_a_closed_fence_before_the_key_is_not_a_preamble(pre):
    assert flags_of(pre + "\n" + digest()) == []


def test_a_preamble_after_a_comment_is_still_a_preamble():
    assert flags_of("<!-- c -->\nHere is my digest:\n" + digest()) == ["key_not_first"]


def test_the_fence_around_the_digest_is_the_container_not_a_skipped_block():
    d = DF.parse("```\n" + digest() + "```\n")
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)
    d = DF.parse("```markdown\n" + raw(OBJ_OK + ["```", HIDDEN, "```"], TRAIL_OK) + "```\n")       # an inner example fence is still blanked
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)


def test_an_unclosed_fence_after_the_key_is_flagged_by_its_line_and_what_follows_it_is_not_read():
    d = DF.parse(raw(OBJ_OK + ["```", HIDDEN], TRAIL_OK))                       # line 6 opens it; the row, the Trail heading and its table are hidden
    assert (d.n_objects, d.n_trail) == (1, 0)
    assert DF.flags(d) == ["ev_unknown:a1:R1", "no_section:Trail", "fence_unclosed:6"]
    assert flags_of(digest(not_done="```\nhidden")) == ["fence_unclosed:11"]
    assert flags_of(digest() + "~~~\n") == ["fence_unclosed:10"]


def test_a_fence_pair_after_the_key_is_not_flagged_and_a_mark_of_the_other_kind_inside_does_not_close_it():
    assert flags_of(digest(not_done="```\nx\n```")) == []
    assert flags_of(digest(not_done="~~~\n```\nx\n~~~")) == []
    assert flags_of(digest(not_done="```\n~~~\nx\n```")) == []
    assert flags_of(digest(not_done="```\n~~~\nx")) == ["fence_unclosed:11"]               # the ~~~ inside does not close the ``` block


@pytest.mark.parametrize("tail", ["", "\n", "\n\n   \n\t\n"])
def test_the_container_fence_closes_on_the_last_non_blank_line_blank_lines_after_it_do_not_matter(tail):
    d = DF.parse("```\n" + digest() + "```" + tail)
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)
    d = DF.parse("~~~markdown\n" + digest() + "~~~" + tail)
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)


CONTAINER_PROBES = [
    ("a line of prose after the closing fence", "```\n" + digest() + "```\nthanks\n", 11),
    ("a closing mark of the other character", "```\n" + digest() + "~~~\n", 11),
    ("an inner fence nothing closes, the last mark closes the container", "```\n" + raw(OBJ_OK + ["```", HIDDEN], TRAIL_OK) + "```\n", 7),
    ("no closing mark at all, an inner one open", "```\n" + digest(not_done="~~~\nx"), 12),
]


@pytest.mark.parametrize("name,text,line", CONTAINER_PROBES, ids=[n for n, _, _ in CONTAINER_PROBES])
def test_in_a_container_only_the_last_non_blank_closing_mark_is_free_any_other_unclosed_fence_is_flagged(name, text, line):
    assert "fence_unclosed:%d" % line in flags_of(text), name


@pytest.mark.parametrize("opener,closer", [("````", "```"), ("```", "```sh"), ("~~~~", "~~~"), ("```", "~~~")],
                         ids=["4-backticks-met-by-3", "3-backticks-met-by-sh", "4-tildes-met-by-3", "backticks-met-by-tildes"])
def test_the_container_is_closed_by_the_fence_grammar_not_by_a_looser_rule(opener, closer):
    """t-870 F-3: the container closes exactly as `md_table.fence_walk` closes a block -- a shorter run, an info string and a mark
    of the other kind do not close it, so the wrong closer is the body's own fence mark and nothing closes it: flagged by its line
    (11), like the other container probes. Before the fix the first two cases flagged nothing."""
    assert "fence_unclosed:11" in flags_of(opener + "\n" + digest() + closer + "\n")


@pytest.mark.parametrize("opener,closer", [("````", "````"), ("```", "````"), ("~~~~", "~~~~~~"), ("```sh", "```")])
def test_a_container_closed_by_a_run_as_long_or_longer_is_free(opener, closer):
    d = DF.parse(opener + "\n" + digest() + closer + "\n")
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)


def test_a_comment_inside_the_container_is_the_digests_own_the_container_is_an_envelope_not_code():
    """t-870 F-4, the Lead's answer: the container fence is a transport envelope, so it is unwrapped FIRST and the comments inside it
    are comments again -- a closed one hides its rows (no stray_row), an unclosed one is flagged `comment_unclosed` by its line."""
    assert flags_of("```\n" + raw(OBJ_OK + ["<!--", HIDDEN, "-->"], TRAIL_OK) + "```\n") == ["key_not_first"]
    assert flags_of("```\n" + raw(OBJ_OK + ["<!-- an example"], TRAIL_OK) + "```\n") == ["key_not_first", "comment_unclosed:7"]
    assert flags_of(raw(OBJ_OK + ["<!--", HIDDEN, "-->"], TRAIL_OK)) == []                  # no container: the same


def test_a_real_code_fence_inside_the_wrapped_digest_still_protects_its_comment_opener():
    d = DF.parse("```\n" + raw(OBJ_OK + ["```", "<!-- an example", "```"], TRAIL_OK) + "```\n")
    assert DF.flags(d) == ["key_not_first"] and (d.n_objects, d.n_trail) == (1, 1)         # the opener is code: no comment_unclosed


def test_a_fenced_heading_in_the_body_is_not_a_second_section():
    assert flags_of(digest(not_done="```\n## Trail\n| tid |\n```")) == []                                       # P7


def test_a_fence_inside_objects_after_its_table_is_blanked_no_stray_row_and_no_data():
    d = DF.parse(raw(OBJ_OK + ["```", HIDDEN, "```"], TRAIL_OK))
    assert DF.flags(d) == [] and d.n_objects == 1


@pytest.mark.parametrize("comment", [[HIDDEN.join(["<!-- ", " -->"])], ["<!--", HIDDEN, "-->"]])
def test_a_closed_comment_inside_a_table_section_hides_its_lines_one_line_or_many(comment):
    d = DF.parse(raw(OBJ_OK + comment, TRAIL_OK))
    assert DF.flags(d) == [] and d.n_objects == 1


def test_a_multi_line_comment_keeps_the_line_numbers_of_the_flags_after_it():
    text = raw(OBJ_OK + ["<!-- a", "b -->", "", OH, OSEP, HIDDEN], TRAIL_OK)
    assert flags_of(text) == ["stray_row:Objects:8", "stray_row:Objects:9", "stray_row:Objects:10"]


def test_an_unclosed_comment_is_flagged_by_its_line_and_hides_nothing_from_the_reader():
    assert flags_of(digest(not_done="<!-- hidden")) == ["comment_unclosed:11"]
    assert flags_of("<!-- x\n" + digest()) == ["key_not_first", "comment_unclosed:1"]
    assert flags_of(raw(OBJ_OK + ["<!-- never closed", HIDDEN], TRAIL_OK)) == ["stray_row:Objects:6", "comment_unclosed:6"]


def test_a_bold_key_is_not_a_key():
    assert DF.parse("**digest: v1 t-1**\n## Objects\n") is None                                                # P12


def test_the_bom_is_an_escape_in_the_source_and_a_bom_before_the_key_is_still_found():
    assert chr(0xFEFF) not in Path(DF.__file__).read_text(encoding="utf-8")
    assert flags_of(DF.BOM + digest()) == []


def test_many_unclosed_comment_openers_are_read_in_bounded_time():
    started = time.monotonic()
    DF.flags(DF.parse(digest(not_done="<!-- " * 3000)))
    assert time.monotonic() - started < 20


def test_magnitude_thousands_of_rows_are_read_once_and_cleanly():
    objects = [obj(id="o%d" % i, ev="T%d" % i) for i in range(3000)]
    trails = [trail("T%d" % i) for i in range(3000)]
    started = time.monotonic()
    d = DF.parse(digest(objects=objects, trails=trails))
    assert DF.flags(d) == [] and (d.n_objects, d.n_trail) == (3000, 3000)
    assert time.monotonic() - started < 20


def test_parse_and_flags_do_not_raise_on_hostile_text():
    for text in ["digest: v1 t-1\n## Objects\n|\n|||\n## Trail\n|`\n| ``` |\n", "digest: v1\n" + "`" * 5000 + "\n## Objects\n" + "| `" * 3000,
                 "digest: v1 t-1\n## Objects\n| " + " | ".join(DF.OBJECTS_HEADER) + " |\n" + "| " * 20000]:
        d = DF.parse(text)
        DF.flags(d)


# ----- the harness text of the gateway scouts teaches the SAME form (t-863, F6-14; SIBLING_MAP axis 2) ---------------------------

def test_the_pi_harness_teaches_the_v1_form_with_the_names_of_the_reader():
    """One source of the names: the section markers and the two table headers the harness quotes are built from digest_form's
    constants, so a rename in the reader fails here; and the old form ("End with a Trail block") is gone."""
    text = " ".join(HARNESS.read_text(encoding="utf-8").split())            # the prompt is wrapped: compare single-spaced
    wanted = ["digest: v1 <task_id>", *("## " + name for name in DF.KNOWN_SECTIONS),
              "`| " + " | ".join(DF.OBJECTS_HEADER) + " |`", "`| " + " | ".join(DF.TRAIL_HEADER) + " |`", "docs/tasks/exchange-form.md"]
    assert [w for w in wanted if w not in text] == []
    assert "End with a" not in text and "Answer as a DIGEST" not in text


def test_the_pi_harness_wording_is_the_wording_of_scout_rule_10():
    """No third wording: the clauses the harness shares with `.claude/agents/scout.md` rule 10 are the same words."""
    rule = " ".join((ROOT / ".claude" / "agents" / "scout.md").read_text(encoding="utf-8").split())
    text = " ".join(HARNESS.read_text(encoding="utf-8").split())
    for clause in ("begins with the line `digest: v1 <task_id>` (no fence around the digest)", "ONE row per object, ONE claim per row",
                   "one row per search or read, EXACTLY as run"):
        assert clause in rule and clause in text, clause


# ----- the trail against the transcript: the pure half (t-863, F6-14; handback_extract pins the end-to-end half) -----------------------

def _rows(*trails, ev="R1"):
    return DF.parse(digest(objects=[obj(ev=ev)], trails=list(trails)))


def test_trail_backing_without_calls_is_unchecked_and_never_unbacked():
    d = _rows(trail("R1", target="nowhere.py"))
    assert DF.trail_backing_flags(d, None) == ["trail_unchecked"]
    assert DF.trail_backing_flags(d, []) == ["trail_unbacked:1"]


def test_trail_backing_counts_the_unmatched_rows_and_names_them_by_number_only():
    d = _rows(trail("R1", target="a.py"), trail("R2", target="b.py"), trail("R3", target="c.py"), ev="R1,R2,R3")
    calls = [DF.ToolCall("Read", "/r/b.py")]
    assert DF.trail_backing_flags(d, calls) == ["trail_unbacked:2"]
    assert DF.trail_backing_flags(d, calls + [DF.ToolCall("Read", "/r/a.py"), DF.ToolCall("Read", "/r/c.py")]) == []


@pytest.mark.parametrize("call", [DF.ToolCall("Grep", "/r/x.py", "x.py"), DF.ToolCall("Glob", "/r/x.py", "x.py"), DF.ToolCall("Read", "/r/y.py"),
                                  DF.ToolCall("Read", None), DF.ToolCall("Read", 7)])
def test_a_read_row_stands_only_behind_a_read_of_its_file(call):
    assert DF.trail_backing_flags(_rows(trail("R1", target="x.py")), [call]) == ["trail_unbacked:1"]


@pytest.mark.parametrize("name", ["Read", "Glob", "Bash"])
def test_a_grep_row_stands_only_behind_a_grep(name):
    d = _rows(found("G1"), ev="G1")
    assert DF.trail_backing_flags(d, [DF.ToolCall(name, "/r/tools", "yes")]) == ["trail_unbacked:1"]
    assert DF.trail_backing_flags(d, [DF.ToolCall("Grep", "/r/tools", "xx yes xx")]) == []


def test_an_untrusted_row_is_flagged_by_the_reader_and_not_counted_as_unbacked():
    d = _rows(trail("R1", target="x.py"), "| R2 | grep | tools/ | `a`|`b` | -i | absent | G2 |", trail("R1", target="dup.py"))
    assert DF.flags(d) == ["bad_row:Trail:2", "dup_tid:R1"]
    assert DF.trail_backing_flags(d, [DF.ToolCall("Read", "/r/x.py")]) == []


def test_a_digest_whose_trail_header_is_wrong_has_no_rows_to_check():
    d = DF.parse(digest(trail_header="| tid | op |"))
    assert DF.trail_backing_flags(d, []) == []
    assert DF.trail_backing_flags(d, None) == ["trail_unchecked"]


# ----- the leaf and the copy ------------------------------------------------------------------------------------------------------

def test_digest_form_imports_none_of_the_heavy_modules():
    """The DoD command: a reader that handback_extract imports must not pull piles and its five friends (spec F9)."""
    code = ("import sys; sys.path.insert(0, 'tools'); import digest_form; "
            "print(sorted(m for m in ('piles', 'forge_metrics', 'journal_validator', 'gitcmd') if m in sys.modules))")
    done = subprocess.run([sys.executable, "-I", "-c", code], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "[]"


def test_piles_uses_the_table_reader_of_md_table_the_very_same_objects():
    """Since node N3 `piles` imports the table reader and the two line filters from md_table: one copy, not a literal one -- the
    names are the same objects (identity), so a change to the reader is one change."""
    import piles
    for name in ("split_pipes", "split_cells", "walk_table", "table_after", "md_lines_outside_fences", "_blank_comments"):
        assert getattr(piles, name) is getattr(md_table, name), name
    # `_code_mask` and `TABLE_RULE_RE` are md_table's internals: piles does not use them and does not re-export them
    # (the lint ratchet refuses an unused import); the copy check below still forbids a second definition of either.
    source = Path(piles.__file__).read_text(encoding="utf-8")
    assert not re.search(r"^(def (_code_mask|split_pipes|split_cells|walk_table|table_after|md_lines_outside_fences|_blank_comments)\b"
                         r"|TABLE_RULE_RE\s*=)", source, re.M), "piles.py carries its own copy again"


_LOADED_FROM_TOOLS = (
    "import json, os, sys\n"
    "tools, scratch, name = sys.argv[1:4]\n"
    "sys.path[:0] = [tools, scratch]\n"
    "__import__(name)\n"
    "root = os.path.realpath(tools) + os.sep\n"
    "print(json.dumps(sorted(m for m, mod in sys.modules.items() if m != name and getattr(mod, '__file__', None)\n"
    "                        and os.path.realpath(mod.__file__).startswith(root))))\n"
)


def _tools_modules_loaded_by(module: str, scratch: Path) -> list[str]:
    """Names in sys.modules, after `import <module>` in a fresh interpreter, whose file lives under tools/ (the module itself
    left out). A module with no `__file__` (a namespace package, a builtin) is not under tools."""
    done = subprocess.run([sys.executable, "-I", "-c", _LOADED_FROM_TOOLS, str(TOOLS), str(scratch), module], cwd=str(ROOT),
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def test_md_table_is_a_leaf_it_imports_nothing_of_tools(tmp_path):
    """Every module of tools/ is a possible import, not a hand list of five: after `import md_table` NO module whose file is under
    tools/ is loaded."""
    assert _tools_modules_loaded_by("md_table", tmp_path) == []


def test_the_leaf_check_sees_a_module_of_tools_a_scratch_importer_pulls_in(tmp_path):
    """Negative control: a scratch module that imports `piles` (which loads md_table and more of tools/) fails the same check."""
    (tmp_path / "scratch_importer.py").write_text("import piles\n", encoding="utf-8")
    loaded = _tools_modules_loaded_by("scratch_importer", tmp_path)
    assert "piles" in loaded and "md_table" in loaded, loaded


def test_md_table_reads_a_table_under_a_heading():
    lines = ["## A", "", "| a | b |", "|---|---|", "| 1 | `x|y` |", "text", "| later |"]
    assert md_table.table_after(lines, "A") == (["a", "b"], [(["1", "`x|y`"], 5)])
