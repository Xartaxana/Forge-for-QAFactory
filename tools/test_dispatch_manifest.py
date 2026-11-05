"""tools/test_dispatch_manifest.py -- battery for tools/dispatch_manifest.py
(B-201, piece A: the pure completeness check, docs/tasks/specs/t-090-dispatch-manifest.md).

K1-K8 are real dispatch prompts copied once into tools/fixtures/dispatch_manifest/
(K<n>.txt, UTF-8); the tests read only those repo copies. K5 and K6 are built
from K1.

Run: python -m pytest tools/test_dispatch_manifest.py -q
"""

import json
import re
import sys
import time
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import dispatch_manifest as dm  # noqa: E402
import md_regions  # noqa: E402

FIXTURES = TOOLS_DIR / "fixtures" / "dispatch_manifest"


def _fixture(name: str) -> str:
    return (FIXTURES / (name + ".txt")).read_bytes().decode("utf-8")


def payload(prompt, type_="builder"):
    return {"tool_name": "Task", "tool_input": {"subagent_type": type_, "prompt": prompt}}


def run(prompt, type_="builder"):
    return dm.check(payload(prompt, type_))


PARTS = {
    "given": "given: docs/tasks/x.md",
    "owns": "owns:\n- C:\\work\\x\\a.py",
    "nongoals": "non-goals: no edit outside owns",
    "handoff": "handoff: a short report",
    "edges": "edges: none -- pure function",
    "dod": "DoD: `python -m pytest tools/x.py -q`",
}


def build(**over):
    parts = dict(PARTS)
    parts.update(over)
    return "\n".join(v for v in parts.values() if v is not None) + "\n"


def fence(text):
    return "```\n" + text.rstrip("\n") + "\n```\n"


def quote(text):
    return "\n".join("> " + line for line in text.rstrip("\n").split("\n")) + "\n"


def missing_names(message):
    body = message.split("Missing: ", 1)[1].split(". Expected,", 1)[0]
    return re.findall(r"(?:^|, )([\w-]+) \(", body)


def missing_text(message):
    return message.split("Missing: ", 1)[1].split(". Expected,", 1)[0]


# =========================================================================
# The real prompts K1-K8
# =========================================================================


def test_K1_t083_attempt1_is_blocked_with_five_items():
    code, msg, note = run(_fixture("K1"))
    assert code == 2 and note == ""
    assert missing_names(msg) == ["given", "owns", "non-goals", "handoff", "edges"]
    assert msg.startswith("DISPATCH INCOMPLETE (CLAUDE.md rule 11): this builder dispatch does not go out.")
    assert "owns (no line)" in msg


@pytest.mark.parametrize("name", ["K2", "K3"])
def test_K2_K3_relative_owns_paths_are_blocked_on_owns_only(name):
    code, msg, note = run(_fixture(name))
    assert code == 2 and note == ""
    assert "owns" in missing_names(msg)
    assert missing_names(msg) == ["owns"]
    assert "owns (no absolute path could be read)" in msg


def test_K4_scout_is_not_checked():
    assert run(_fixture("K4"), "scout") == (0, "", "")


def test_K5_K1_plus_a_valid_skip_line_goes_out_with_a_skip_note():
    prompt = _fixture("K1") + "\nmanifest-skip: given, owns, non-goals, handoff, edges -- old-form dispatch, sent on purpose\n"
    code, msg, note = run(prompt)
    assert (code, msg) == (0, "")
    assert note.startswith("MANIFEST-SKIP:")
    assert note == (
        'MANIFEST-SKIP: dispatch sent without given, owns, non-goals, handoff, edges on purpose: '
        '"old-form dispatch, sent on purpose" -- the line stays in the prompt as the record.'
    )


def test_K6_unknown_skip_item_is_refused():
    prompt = _fixture("K1") + "\nmanifest-skip: given, colour -- because\n"
    code, msg, note = run(prompt)
    assert code == 2 and note == ""
    assert msg == (
        "MANIFEST-SKIP REFUSED: 'manifest-skip: given, colour -- because' -- unknown item 'colour'. "
        "Expected: manifest-skip: <item>[, <item>] -- <reason>; items: given, owns, non-goals, "
        "handoff, edges, dod; the reason is not empty."
    )


def test_K6_empty_reason_is_refused():
    for tail in ("--", "--   ", "— "):
        prompt = _fixture("K1") + "\nmanifest-skip: given, owns " + tail + "\n"
        code, msg, note = run(prompt)
        assert code == 2 and msg.startswith("MANIFEST-SKIP REFUSED:") and "-- no reason after --." in msg, tail


def test_K7_t091_written_in_the_form_passes_unchanged():
    assert run(_fixture("K7")) == (0, "", "")


def test_K8_critic_prompt_with_numbered_owns_overlap_is_not_checked():
    assert "6. Owns overlap:" in _fixture("K8")
    assert run(_fixture("K8"), "critic") == (0, "", "")


# =========================================================================
# The text of the messages (verbatim)
# =========================================================================

_EXPECTED_INCOMPLETE = (
    "DISPATCH INCOMPLETE (CLAUDE.md rule 11): this builder dispatch does not go out. "
    "Missing: given (no line), owns (no line), non-goals (no line), handoff (no line), "
    "edges (no line), DoD (no line). Expected, each as its own line outside code fences and "
    "quotes, starting with its name and a colon: given: (files/data the worker gets; a pointer "
    "to a persisted spec is allowed), owns: (the absolute paths the worker may write, never by "
    "pointer; on the owns line itself or on the lines right under it, with no blank line and no "
    "heading marks; a path with spaces in backticks), non-goals:, handoff:, edges: (the "
    "behavior at each limit, empty input and conflicting pair, or 'edges: none -- <why>'), "
    "DoD: (with the exact verification command in backticks, two words or more). To send it "
    "anyway on purpose, add a line: manifest-skip: <item>[, <item>] -- <reason>"
)


def test_incomplete_text_is_verbatim():
    assert run("just some words\n") == (2, _EXPECTED_INCOMPLETE, "")


def test_unchecked_note_text_is_verbatim():
    line = "`a b` " * 201
    code, msg, note = run(build(given="given: " + line))
    assert (code, msg) == (0, "")
    assert note == (
        "MANIFEST-UNCHECKED: this dispatch was not checked for completeness (quoted regions "
        "could not be read reliably) -- it went out; check given, owns, non-goals, handoff, "
        "edges and DoD by eye."
    )


def test_missing_labels_no_line_empty_no_path_no_command():
    prompt = (
        "given:\n"
        "owns: docs/relative.md\n"
        "non-goals: none\nhandoff: report\nedges: none -- x\n"
        "DoD: run the tests\n"
    )
    code, msg, note = run(prompt)
    assert code == 2
    assert missing_text(msg) == (
        "given (empty), owns (no absolute path could be read), DoD (no command in backticks)"
    )
    code, msg, note = run("owns:\n\nnon-goals: a\nhandoff: b\nedges: c\nDoD: `x y`\ngiven: g\n")
    assert missing_text(msg) == "owns (empty)"


# =========================================================================
# Payload shapes and who is checked
# =========================================================================


@pytest.mark.parametrize("bad", [None, "text", ["a"], 3])
def test_non_dict_payload_raises(bad):
    with pytest.raises(Exception):
        dm.check(bad)


@pytest.mark.parametrize("bad", [None, "x", ["a"], 7])
def test_non_dict_tool_input_raises(bad):
    with pytest.raises(Exception):
        dm.check({"tool_input": bad})


def test_absent_tool_input_raises():
    with pytest.raises(Exception):
        dm.check({})


@pytest.mark.parametrize("prompt", [None, 123, ["x"], b"bytes", ""])
def test_builder_with_empty_or_odd_prompt_gets_all_six_items(prompt):
    code, msg, note = run(prompt)
    assert code == 2 and note == ""
    assert missing_names(msg) == ["given", "owns", "non-goals", "handoff", "edges", "DoD"]


def test_builder_with_absent_prompt_key_gets_all_six_items():
    code, msg, note = dm.check({"tool_input": {"subagent_type": "builder"}})
    assert code == 2 and len(missing_names(msg)) == 6


@pytest.mark.parametrize("prompt", [None, 123, ""])
def test_non_builder_with_odd_prompt_goes_out(prompt):
    assert run(prompt, "general-purpose") == (0, "", "")


def test_capital_builder_with_trailing_space_is_checked():
    code, msg, note = run("nothing here\n", "Builder ")
    assert code == 2 and "builder dispatch" in msg


def test_non_string_subagent_type_is_not_builder():
    assert run("nothing\n", None) == (0, "", "")
    assert dm.check({"tool_input": {"prompt": "nothing"}}) == (0, "", "")


def test_general_purpose_without_owns_header_goes_out():
    assert run("do something, no headers at all\n", "general-purpose") == (0, "", "")
    assert run("write the file\nowns nothing here\n", "general-purpose") == (0, "", "")


def test_non_builder_with_absolute_owns_is_a_writing_dispatch():
    prompt = "owns:\n- C:\\work\\x\\a.py\nsome text\n"
    code, msg, note = run(prompt, "general-purpose")
    assert code == 2 and "this writing dispatch does not go out" in msg
    assert missing_names(msg) == ["given", "non-goals", "handoff", "edges", "DoD"]
    assert run(build(), "general-purpose") == (0, "", "")


def test_non_builder_with_relative_owns_is_not_checked():
    assert run("owns: docs/x.md\n", "general-purpose") == (0, "", "")


def test_non_builder_owns_in_a_fence_is_not_checked():
    assert run(fence("owns: C:\\work\\x.py"), "general-purpose") == (0, "", "")


def test_full_form_passes():
    assert run(build()) == (0, "", "")


@pytest.mark.parametrize("item", ["given", "owns", "nongoals", "handoff", "edges", "dod"])
def test_each_item_missing_alone_is_named(item):
    code, msg, note = run(build(**{item: None}))
    expected = {"nongoals": "non-goals", "dod": "DoD"}.get(item, item)
    assert code == 2 and missing_names(msg) == [expected]


# =========================================================================
# Headers: form, limit, prefixes
# =========================================================================


def _given_with_gap(n):
    # "given" + n characters + ":"
    return "given" + " " + "x" * (n - 1) + ":" + " docs/x.md"


def test_header_limit_160_is_a_header_161_is_not():
    assert run(build(given=_given_with_gap(160))) == (0, "", "")
    code, msg, note = run(build(given=_given_with_gap(161)))
    assert code == 2 and missing_names(msg) == ["given"]
    assert run(build(given="given: docs/x.md")) == (0, "", "")  # 0 characters


def test_header_prefixes_and_case():
    for given in ("- given: g", "* GIVEN: g", "• Given: g", "**given**: g", "## given: g", "   given: g"):
        assert run(build(given=given)) == (0, "", ""), given


def test_numbered_list_prefix_is_not_a_header():
    for given in ("3. given: g", "1) given: g"):
        code, msg, note = run(build(given=given))
        assert code == 2 and missing_names(msg) == ["given"], given


def test_line_starting_with_a_backtick_is_not_a_header():
    code, msg, note = run(build(given="`given: g`"))
    assert code == 2 and missing_names(msg) == ["given"]


def test_key_variants():
    assert run(build(nongoals="non-goal: x", handoff="hand-off: x", edges="edge behaviour: x")) == (0, "", "")
    assert run(build(edges="Edge behavior: x")) == (0, "", "")
    assert run(build(edges="edge: x")) == (0, "", "")
    assert run(build(dod="Witness: `pytest -q`")) == (0, "", "")
    assert run(build(dod="verification run: `pytest -q`")) == (0, "", "")


def test_header_tail_counts_as_the_body():
    code, msg, note = run(build(given="given:"))
    assert missing_text(msg) == "given (empty)"
    code, msg, note = run(build(given="given:\n   \n\t\n"))
    assert missing_text(msg) == "given (empty)"
    assert run(build(given="given:\nbody on the next line")) == (0, "", "")


def test_section_ends_at_next_header():
    # `given:` has no body of its own; the next header must not be swallowed as its body.
    code, msg, note = run(build(given="given:", owns=PARTS["owns"]))
    assert missing_text(msg) == "given (empty)"


# =========================================================================
# Quoted text never counts
# =========================================================================


def test_manifest_inside_a_fence_is_not_a_manifest():
    code, msg, note = run(fence(build()))
    assert code == 2 and missing_names(msg) == ["given", "owns", "non-goals", "handoff", "edges", "DoD"]


def test_manifest_inside_a_blockquote_is_not_a_manifest():
    code, msg, note = run(quote(build()))
    assert code == 2 and len(missing_names(msg)) == 6


def test_one_header_quoted_the_rest_prose():
    code, msg, note = run(build(edges=None) + quote("edges: none -- quoted"))
    assert missing_names(msg) == ["edges"]
    code, msg, note = run(build(edges=None) + fence("edges: none -- fenced"))
    assert missing_names(msg) == ["edges"]
    assert run(build(edges=None) + "edges: none -- real\n") == (0, "", "")


def test_unterminated_fence_counts_as_prose():
    prompt = "```\n" + build()
    assert run(prompt) == (0, "", "")


def test_tilde_fence_is_quoted():
    code, msg, note = run("~~~\n" + build() + "~~~\n")
    assert code == 2


def test_skip_line_inside_a_fence_or_quote_is_ignored():
    for wrapped in (fence("manifest-skip: given -- r"), quote("manifest-skip: given -- r")):
        code, msg, note = run(build(given=None) + wrapped)
        assert code == 2 and missing_names(msg) == ["given"]
        assert "REFUSED" not in msg
    # a MALFORMED skip line inside a fence is ignored as well, not refused
    code, msg, note = run(build(given=None) + fence("manifest-skip: colour -- r"))
    assert code == 2 and msg.startswith("DISPATCH INCOMPLETE")


def test_owns_section_is_sliced_before_owns_gate_sees_it():
    # an absolute path elsewhere (given section, fence) is not an owned path
    prompt = build(given="given: C:\\work\\x\\elsewhere.py", owns="owns: docs/rel.md") + fence("C:\\work\\y\\z.py")
    code, msg, note = run(prompt)
    assert missing_names(msg) == ["owns"]
    # a path in the section AFTER owns (next header) is not part of the owns section
    prompt = build(owns="owns: docs/rel.md", nongoals="non-goals: C:\\work\\x\\a.py")
    code, msg, note = run(prompt)
    assert missing_names(msg) == ["owns"]


def test_owns_in_a_fence_is_a_false_block():
    code, msg, note = run(build(owns=fence("owns: C:\\work\\x\\a.py")))
    assert code == 2 and missing_names(msg) == ["owns"]


def test_dod_command_in_a_terminated_fence_counts_but_not_the_delimiters():
    dod = "DoD:\n" + fence("python -m pytest tools/x.py -q")
    assert run(build(dod=dod)) == (0, "", "")
    dod = "DoD:\n```bash\n```\n"  # only delimiters, nothing inside
    code, msg, note = run(build(dod=dod))
    assert missing_text(msg) == "DoD (no command in backticks)"
    dod = "DoD:\n" + fence("pytest")  # a one-token line
    assert missing_names(run(build(dod=dod))[1]) == ["DoD"]


def test_dod_command_in_a_blockquote_does_not_count():
    dod = "DoD:\n" + quote("run `python -m pytest tools/x.py -q`")
    assert missing_names(run(build(dod=dod))[1]) == ["DoD"]
    dod = "DoD:\n" + quote("```\npython -m pytest -q\n```")
    assert missing_names(run(build(dod=dod))[1]) == ["DoD"]


def test_dod_command_in_an_unterminated_fence_counts_as_prose_span():
    dod = "DoD: ```text with `pytest -q` inside\n"
    assert run(build(dod=dod)) == (0, "", "")


# =========================================================================
# Command limit
# =========================================================================


def test_command_limit_one_token_is_not_a_command_two_is():
    assert missing_names(run(build(dod="DoD: `pytest`"))[1]) == ["DoD"]
    assert run(build(dod="DoD: `pytest -q`")) == (0, "", "")


def test_command_named_limit_json_example_counts():
    # NAMED OPEN LIMIT: any 2-token code span in the DoD section counts, a JSON example included.
    assert run(build(dod='DoD: the payload looks like `{"a": 1}`')) == (0, "", "")


def test_command_in_another_section_does_not_count_for_dod():
    prompt = build(dod="DoD: nothing in backticks", given="given: `cat x.md`")
    assert missing_names(run(prompt)[1]) == ["DoD"]


def test_double_backtick_span_and_span_on_a_later_line_of_the_section():
    assert run(build(dod="DoD:\nrun ``python -m pytest -q`` now")) == (0, "", "")


# =========================================================================
# Pointers
# =========================================================================


def test_given_pointer_passes_owns_pointer_fails():
    assert run(build(given="given: docs/tasks/x.md")) == (0, "", "")
    code, msg, note = run(build(owns="owns: see docs/tasks/x.md"))
    assert missing_names(msg) == ["owns"]


# =========================================================================
# Owns: extraction in its new role
# =========================================================================


def test_owns_inline_and_bullets_and_backticked_path_with_spaces():
    assert run(build(owns="owns: C:\\work\\x\\a.py")) == (0, "", "")
    assert run(build(owns="owns: C:/proj/x/a.py, C:/proj/x/b.py")) == (0, "", "")
    assert run(build(owns="owns:\n- `C:\\work area\\x.py`")) == (0, "", "")
    assert run(build(owns="owns:\n1. /c/proj/x.py")) == (0, "", "")
    assert run(build(owns="**owns**: /home/u/a.py")) == (0, "", "")


def test_owns_absolute_glob_kept_relative_glob_dropped():
    assert run(build(owns="owns: C:\\work\\x\\*.py")) == (0, "", "")
    for owns in ("owns: tools/*.py", "owns: everything in tools/*.py", "owns:\n- tools/**/*.py"):
        assert missing_names(run(build(owns=owns))[1]) == ["owns"], owns


def test_owns_false_blocks_are_allowed_direction():
    cases = [
        "owns: tools/x.py",                     # relative
        "owns: ~/x/a.py",                       # home-relative
        "owns: \\\\server\\share\\a.py",        # UNC
        "owns: tools/*.py\n- C:\\work\\x\\a.py",  # a relative glob on the owns line hides the next line
        "owns: **bold**",                       # markdown emphasis
        "owns: C:\\",                           # bare roots
        "owns: /",
        "owns:",
    ]
    for owns in cases:
        code, msg, note = run(build(owns=owns))
        assert code == 2 and missing_names(msg) == ["owns"], owns


def test_owns_continuation_limit_40_passes_41_is_unreadable():
    def owns(n):
        return "owns:\n" + "\n".join("- C:\\work\\f%d.py" % i for i in range(n))

    assert run(build(owns=owns(40))) == (0, "", "")
    code, msg, note = run(build(owns=owns(41)))
    assert code == 2 and missing_text(msg) == "owns (no absolute path could be read)"


def test_owns_duplicate_sections_any_one_qualifies():
    prompt = build(owns="owns: docs/rel.md") + "owns: C:\\work\\x\\a.py\n"
    assert run(prompt) == (0, "", "")


def test_named_open_limit_absolute_path_merely_mentioned_in_owns_counts():
    # pinned as CURRENT behaviour: a false pass, not fixed here
    assert run(build(owns="owns: C:/proj/x/a.py is not decided yet")) == (0, "", "")
    assert run(build(owns="owns: C:/proj/x/a.py (maybe, ask first)")) == (0, "", "")


def test_named_open_limit_bullet_path_with_spaces_without_backticks_is_cut():
    import owns_gate

    section = "owns:\n- C:/work area/x.py"
    assert owns_gate.extract_owns_paths(section) == ["C:/work"]
    assert run(build(owns=section)) == (0, "", "")


def test_named_open_limit_prose_line_given_the_above_counts_as_a_given_header():
    prompt = build(given=None) + "Given the above, we go ahead: sure\n"
    assert run(prompt) == (0, "", "")


def test_named_open_limit_deliberate_degraded_read_lets_a_dispatch_out_with_the_note():
    prompt = "`a b` " * 201 + "\nno manifest at all\n"
    code, msg, note = run(prompt)
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")


def test_skip_em_dash_separator_stays_legal_and_bare_skip_is_unchanged():
    code, msg, note = run(build(given=None) + "manifest-skip: given \u2014 pointer\n")
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-SKIP:")
    code, msg, note = run(build() + "manifest-skip: given\n")
    assert code == 2 and "-- no reason after --." in msg


# =========================================================================
# Named false blocks and the header-word limit (added after the critic's review)
# =========================================================================


def test_named_false_block_heading_mark_before_owns_then_bullets():
    code, msg, note = run(build(owns="## Owns:\n- C:\\work\\x\\a.py"))
    assert code == 2 and missing_text(msg) == "owns (no absolute path could be read)"


def test_named_false_block_blank_line_between_owns_and_bullets():
    code, msg, note = run(build(owns="owns:\n\n- C:\\work\\x\\a.py"))
    assert code == 2 and missing_text(msg) == "owns (no absolute path could be read)"


def test_named_false_block_dod_one_token_span_with_prose_after_it():
    code, msg, note = run(build(dod="DoD: `pytest` green"))
    assert code == 2 and missing_text(msg) == "DoD (no command in backticks)"


def test_named_open_limit_prose_line_opening_with_a_key_word_is_a_header_for_every_key():
    # the prose line IS taken as the header: with a body under it the item counts as present ...
    assert run(build(edges="Edge cases are listed below:\nnone")) == (0, "", "")
    assert run(build(handoff="Handoff to the critic happens later:\na report")) == (0, "", "")
    assert run(build(nongoals="Non-goals of the earlier task were different:\nnone")) == (0, "", "")
    # ... and alone it is "(empty)", not "(no line)": it was recognised as a header
    code, msg, note = run(build(edges="Edge cases are listed below:"))
    assert code == 2 and missing_text(msg) == "edges (empty)"
    code, msg, note = run(build(handoff="Handoff to the critic happens later:"))
    assert code == 2 and missing_text(msg) == "handoff (empty)"


# =========================================================================
# Degraded read: 200 checked, 201 unchecked
# =========================================================================


def test_inline_spans_200_are_read_201_are_not():
    spans = lambda n: "`a b` " * n  # noqa: E731
    code, msg, note = run(build(given="given: " + spans(200)))
    assert (code, msg, note) == (0, "", "")  # complete read, full manifest
    code, msg, note = run("some words " + spans(200) + "\n")
    assert code == 2  # complete read, an incomplete dispatch is blocked
    code, msg, note = run("some words " + spans(201) + "\n")
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")


def test_lines_each_holding_a_span_second_degraded_route_at_and_beyond_the_limit():
    # md_regions.MAX_REGIONS = 20,000; a line "`a b`\n" costs 2 regions (span + line end), so the
    # real limit is 10,000 lines checked / 10,001 unchecked. It is SHAPE-DEPENDENT: for a line
    # with prose around the span ("text `a b` more") 9,999 are read and 10,000 are not.
    import md_regions

    assert md_regions.MAX_REGIONS == 20_000
    code, msg, note = run("`a b`\n" * 10_000)
    assert code == 2 and note == ""  # complete read, incomplete dispatch
    code, msg, note = run("`a b`\n" * 10_001)
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")
    code, msg, note = run("text `a b` more\n" * 9_999)
    assert code == 2 and note == ""
    code, msg, note = run("text `a b` more\n" * 10_000)
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")


def test_degraded_read_of_a_non_builder_with_owns_word_is_unchecked_note():
    prompt = "owns: C:\\work\\x.py\n" + "`a b` " * 201 + "\n"
    code, msg, note = run(prompt, "general-purpose")
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")
    # without the word "owns" no note is made for a non-builder
    assert run("`a b` " * 201 + "\n", "scout") == (0, "", "")


def test_text_over_the_scanner_limit_is_unchecked_not_blocked():
    prompt = "x" * 2_000_001
    code, msg, note = run(prompt)
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")


# =========================================================================
# Skip lines
# =========================================================================


def test_skip_all_six_at_once_is_legal():
    prompt = "words only\nmanifest-skip: given, owns, non-goals, handoff, edges, dod -- spike, no worker needed\n"
    code, msg, note = run(prompt)
    assert (code, msg) == (0, "")
    assert note == (
        'MANIFEST-SKIP: dispatch sent without given, owns, non-goals, handoff, edges, DoD on purpose: '
        '"spike, no worker needed" -- the line stays in the prompt as the record.'
    )


def test_skip_grammar_variants():
    for line in (
        "manifest-skip: given -- r",
        "MANIFEST-SKIP:given — r",
        "  - manifest-skip:  given ,  GIVEN --r",
        "* Manifest-Skip: Given -- reason with -- dashes inside",
    ):
        code, msg, note = run(build(given=None) + line + "\n")
        assert (code, msg) == (0, "") and note.startswith("MANIFEST-SKIP:"), line


def test_partial_skip_reports_only_the_remaining_items():
    prompt = build(given=None, edges=None) + "manifest-skip: given -- not needed\n"
    code, msg, note = run(prompt)
    assert code == 2 and missing_names(msg) == ["edges"] and note == ""


def test_present_section_beats_a_skip_naming_it():
    code, msg, note = run(build() + "manifest-skip: given, owns -- r\n")
    assert (code, msg, note) == (0, "", "")


def test_skip_is_partly_effective_only_on_missing_items_in_the_note():
    code, msg, note = run(build(given=None) + "manifest-skip: given, owns -- r\n")
    assert code == 0 and "without given on" in note and "owns" not in note.split("on purpose")[0]


def test_skip_line_ends_a_section():
    prompt = build(given="given:") + "manifest-skip: given -- r\n"
    assert run(prompt)[0] == 0  # the skip line is not the body of `given:`, it waives the empty item
    prompt = build(given="given:\nmanifest-skip: edges -- r", edges=None)
    code, msg, note = run(prompt)
    # the skip line is not the body of `given:`; it waives `edges` (no line), `given` stays empty
    assert code == 2 and missing_text(msg) == "given (empty)"


def test_malformed_skip_lines_are_refused_with_the_reason():
    cases = {
        "manifest-skip: colour -- r": "unknown item 'colour'",
        "manifest-skip: given, -- r": "unknown item ''",
        "manifest-skip: -- r": "unknown item ''",
        "manifest-skip: given": "no reason after --",
        "manifest-skip: given --": "no reason after --",
        "manifest-skip: given --   ": "no reason after --",
        "manifest-skip: colour --": "unknown item 'colour'",
        # text but no separator: decided BEFORE the items are looked at
        "manifest-skip: given because pointer": "no reason after --",
        "manifest-skip: given – pointer": "no reason after --",  # en dash is not a separator
        "manifest-skip: given - pointer": "no reason after --",  # nor is a single hyphen
        "manifest-skip: colour": "no reason after --",
        # unchanged: an unknown item next to a real separator
        "manifest-skip: given, bogus -- reason": "unknown item 'bogus'",
    }
    for line, why in cases.items():
        code, msg, note = run(build() + line + "\n")
        assert code == 2 and note == "", line
        assert msg.startswith("MANIFEST-SKIP REFUSED: '%s' -- %s. Expected:" % (line.strip(), why)), (line, msg)


def test_malformed_skip_wins_over_incomplete():
    code, msg, note = run("nothing\nmanifest-skip: colour -- r\n")
    assert msg.startswith("MANIFEST-SKIP REFUSED:")


def test_skip_in_a_non_checked_dispatch_is_ignored():
    assert run("manifest-skip: colour -- r\n", "scout") == (0, "", "")


def test_two_skip_lines_give_one_note_per_contributing_line():
    # PINNED (spec is silent): each skip line that waives something contributes its own SKIP NOTE line.
    prompt = build(given=None, edges=None) + "manifest-skip: given -- r1\nmanifest-skip: edges, given -- r2\n"
    code, msg, note = run(prompt)
    assert code == 0
    lines = note.split("\n")
    assert len(lines) == 2
    assert 'without given on purpose: "r1"' in lines[0]
    assert 'without edges on purpose: "r2"' in lines[1]


def test_duplicate_sections_are_satisfied_if_any_one_qualifies():
    prompt = build(given="given:") + "given: docs/x.md\n"
    assert run(prompt) == (0, "", "")
    prompt = build(dod="DoD: no command") + "DoD: `pytest -q`\n"
    assert run(prompt) == (0, "", "")


# =========================================================================
# Non-ASCII
# =========================================================================


def test_cyrillic_dano_counts_as_given_escaped_and_raw():
    raw_payload = payload(build(given="ДАНО: docs/x.md"))
    escaped = json.loads(json.dumps(raw_payload, ensure_ascii=True))
    assert "\\u" in json.dumps(raw_payload, ensure_ascii=True)
    raw_bytes = json.dumps(raw_payload, ensure_ascii=False).encode("utf-8")
    from_bytes = json.loads(raw_bytes.decode("utf-8"))
    for p in (raw_payload, escaped, from_bytes):
        assert dm.check(p) == (0, "", "")
    assert run(build(given="дано: docs/x.md")) == (0, "", "")


def test_other_cyrillic_headers_count_as_missing_false_block():
    for over in ({"owns": "Владеет:\n- C:\\work\\x\\a.py"}, {"nongoals": "Не цели: ничего"}, {"handoff": "Сдача: отчёт"}, {"edges": "Края: нет"}):
        code, msg, note = run(build(**over))
        key = next(iter(over))
        assert code == 2 and missing_names(msg) == [{"nongoals": "non-goals"}.get(key, key)], over
    escaped = json.loads(json.dumps(payload(build(nongoals="Не цели: ничего")), ensure_ascii=True))
    assert dm.check(escaped)[0] == 2


# =========================================================================
# No length cap; speed
# =========================================================================


def test_million_character_prompt_finishes_under_5_seconds():
    filler = "filler line of ordinary prose\n" * 34000  # about 1,020,000 characters
    prompt = build() + filler
    assert len(prompt) > 1_000_000
    t0 = time.perf_counter()
    result = run(prompt)
    assert time.perf_counter() - t0 < 5
    assert result == (0, "", "")


def test_million_character_single_line_finishes_under_5_seconds():
    prompt = build() + "z" * 1_000_000 + "\n"
    t0 = time.perf_counter()
    assert run(prompt) == (0, "", "")
    assert time.perf_counter() - t0 < 5


def test_owns_line_with_5000_paren_groups_finishes_under_5_seconds():
    prompt = build(owns="owns: " + "()" * 5000 + " C:\\work\\x\\a.py")
    t0 = time.perf_counter()
    result = run(prompt)
    assert time.perf_counter() - t0 < 5
    assert result == (0, "", "")  # owns_gate strips the parenthetical groups and reads the path


# =========================================================================
# Purity, failure propagation
# =========================================================================


def test_no_output_and_no_top_level_sibling_imports(capsys):
    run(build())
    run("nothing\n")
    run(fence(build()))
    out = capsys.readouterr()
    assert out.out == "" and out.err == ""
    src = (TOOLS_DIR / "dispatch_manifest.py").read_text(encoding="utf-8")
    assert not re.search(r"^\s*print\(", src, re.M)
    assert "sys.stderr" not in src and "open(" not in src
    for name in ("owns_gate", "dispatch_gate", "md_regions"):
        assert not re.search(r"^(?:import|from) %s\b" % name, src, re.M), name


def test_internal_exception_propagates_out_of_check(monkeypatch):
    import owns_gate

    def boom(_text):
        raise RuntimeError("boom")

    # FLIPPED (B-204): the checker reads owned paths through owned_paths(cut), which
    # uses owns_gate's token helper -- that is the seam an internal error comes from now
    monkeypatch.setattr(owns_gate, "_first_token_path", boom)
    with pytest.raises(RuntimeError):
        run(build())


def test_failed_owns_gate_import_propagates(monkeypatch):
    monkeypatch.setitem(sys.modules, "owns_gate", None)
    with pytest.raises(ImportError):
        run(build())


def test_failed_md_regions_import_propagates(monkeypatch):
    monkeypatch.setitem(sys.modules, "md_regions", None)
    with pytest.raises(ImportError):
        run(build())


def test_check_does_not_touch_the_payload():
    p = payload(build())
    snapshot = json.dumps(p, sort_keys=True)
    dm.check(p)
    assert json.dumps(p, sort_keys=True) == snapshot


# =========================================================================
# handoff_paths (t-744 F5-1 N3) and the shared loop with given_paths
# =========================================================================

_TOP = {"tools", "docs", "plans"}


def _hp(prompt):
    return dm.handoff_paths(dm.section_cut(prompt))


@pytest.mark.parametrize("name,expected", [
    ("K1", []), ("K2", []), ("K3", []), ("K4", []), ("K8", []),
    ("K7", [(r"C:\proj\docs\tasks\specs\t-089-split-test-story-run.md", 2, 2, False)]),
])
def test_given_paths_on_the_real_prompts_is_pinned_across_the_shared_loop(name, expected):
    # pinned on the pre-refactor output (the given_paths of HEAD e9b310df): the loop is now _section_paths
    got = dm.given_paths(dm.section_cut(_fixture(name)), None)
    assert [tuple(g) for g in got] == expected


def test_given_paths_with_a_root_is_pinned_across_the_shared_loop():
    top = {"tools", "docs", "plans"}
    assert [tuple(g) for g in dm.given_paths(dm.section_cut(_fixture("K2")), top)] == [
        ("tools/", 4, 4, False), ("docs/FINDINGS.md", 4, 4, False)]
    assert [tuple(g) for g in dm.given_paths(dm.section_cut(_fixture("K3")), top)] == [
        ("plans/builder-rules.md", 3, 2, False)]
    mixed = ("given: tools/a.py (new), `docs/b/c.md`\n- plans/d.md\n> tools/quoted.py\n\ntools/after_blank.py\n"
             "owns: D:/r/x.py\n" + r"given: C:\r\e.py, tools/a.py" + "\nDoD: `x y`\n")
    cut = dm.section_cut(mixed)
    assert [tuple(g) for g in dm.given_paths(cut, top)] == [
        ("tools/a.py", 0, 0, True), ("docs/b/c.md", 0, 0, False), ("plans/d.md", 1, 0, False),
        (r"C:\r\e.py", 6, 6, False)]
    assert [tuple(g) for g in dm.given_paths(cut, None)] == [("docs/b/c.md", 0, 0, False), (r"C:\r\e.py", 6, 6, False)]


def test_handoff_paths_on_the_header_line_and_the_lines_under_it():
    assert _hp(r"handoff: C:\w\docs\tasks\specs\reviews\t-1.md -- the verdict" + "\n") == [
        r"C:\w\docs\tasks\specs\reviews\t-1.md"]
    assert _hp("handoff:\n/w/docs/a.md\n/w/docs/b.md\n\n/w/docs/after_blank.md\n") == ["/w/docs/a.md", "/w/docs/b.md"]
    assert _hp(r"handoff: the report file `C:\w x\docs\t-1.md` and /w/docs/t-2.md" + "\n") == [
        r"C:\w x\docs\t-1.md", "/w/docs/t-2.md"]


def test_handoff_paths_strips_the_new_marker_and_deduplicates():
    assert _hp("handoff: /w/docs/t-1.md (new), /w/docs/t-1.md\n") == ["/w/docs/t-1.md"]


def test_handoff_paths_drops_relative_paths_placeholders_and_urls():
    assert _hp("handoff: docs/tasks/handoffs/t-1.md and `docs/x/y.md`\n") == []
    assert _hp("handoff: /w/docs/<task-id>-f5-1.md and /w/docs/{x}.md and https://example.com/w/a.md\n") == []


def test_handoff_paths_never_reads_a_quoted_line():
    assert _hp("handoff:\n> /w/docs/quoted.md\n/w/docs/real.md\n") == ["/w/docs/real.md"]
    assert _hp("```\nhandoff: /w/docs/fenced.md\n```\n") == []
    assert _hp("> handoff: /w/docs/quoted.md\n") == []


def test_handoff_paths_stops_at_the_next_header_and_reads_every_handoff_section():
    prompt = "handoff: /w/docs/a.md\nedges: none -- /w/docs/not-a-handoff.md\nhandoff: /w/docs/b.md\n"
    assert _hp(prompt) == ["/w/docs/a.md", "/w/docs/b.md"]


def test_handoff_paths_of_a_degraded_cut_and_of_no_section():
    assert _hp("") == [] and _hp("no manifest here /w/docs/a.md\n") == []
    assert dm.handoff_paths(dm.section_cut(None)) == []


def test_handoff_dirs_is_data_with_the_four_roles():
    assert dm.HANDOFF_DIRS == {"critic": "docs/tasks/specs/reviews", "designer": "docs/tasks/specs",
                               "builder": "docs/tasks/handoffs", "scout": "docs/tasks/specs/reports"}


# =========================================================================
# has_owned_paths (t-855, forge F6-8): THE yes/no "does this text declare an owned path", on the one cut
# =========================================================================

_OWNED = r"C:\x\y.py"

# (text, default answer = handoff_gate's question, include_quoted answer = the parallel-writer limit's)
_HAS_OWNED_TABLE = [
    ("owns: C:\\x\\y.py", True, True),                                     # the header, the path on the line
    ("- owns: C:\\x\\y.py", True, True),                                   # a bullet header
    ("**owns:** C:\\x\\y.py", True, True),                                 # a bold header, the colon inside the stars
    ("**owns (ABSOLUTE write paths):** C:\\x\\y.py", True, True),          # a bold header with a parenthetical
    ("## owns: C:\\x\\y.py", True, True),                                  # a heading mark
    ("  owns: /tools/x.py", True, True),                                   # an indented header, a POSIX path
    ("owns:\nC:\\x\\y.py", True, True),                                    # the R11-f form: the path on the next line
    ("owns:\n- C:\\x\\a.py\n- C:\\x\\b.py\n", True, True),                 # a bullet list under the header
    ("owns: `C:\\Program Files\\x y.py`", True, True),                     # a backticked path with spaces
    ("owns: tools/x.py", False, False),                                    # RELATIVE only: not a declaration
    ("owns: tools/*.py", False, False),                                    # a relative glob: the same
    ("owns:\ntools/x.py", False, False),                                   # relative on the next line: the same
    ("owns:\ntools/x.py\nC:\\x\\y.py", False, False),                      # the run under a header stops at a non-path line
    ("owns:\nC:\\x\\y.py\ntools/x.py", True, True),                        # ... and keeps what it read before it
    ("owns:", False, False),
    ("see 5 owns/non-goals/queue lines", False, False),                    # prose, a glued slash (the live case)
    ("C3-12 owns /tools/x.py right now", False, False),                    # prose with an absolute path, no colon
    ("name every owns line: /tools/x.py is not a header here", False, False),  # the colon is not after the key
    ("> owns: C:\\x\\y.py", False, True),                                  # a blockquoted example
    ("```\nowns: C:\\x\\y.py\n```", False, True),                          # a fenced example (t-847's pinned answer)
    ("```\nowns:\nC:\\x\\y.py\n```", False, True),                         # a fenced header, the path under it
    ("> owns: tools/x.py", False, False),                                  # quoted AND relative
    ("```\nowns: C:\\x\\y.py", True, True),                                # an unterminated fence is prose
    ("", False, False),
]


@pytest.mark.parametrize("text, plain, with_quoted", _HAS_OWNED_TABLE)
def test_has_owned_paths_on_the_header_forms(text, plain, with_quoted):
    assert dm.has_owned_paths(text) is plain, text
    assert dm.has_owned_paths(text, include_quoted=True) is with_quoted, text


@pytest.mark.parametrize("text, _plain, _with_quoted", _HAS_OWNED_TABLE)
def test_has_owned_paths_default_is_the_question_owned_paths_answers(text, _plain, _with_quoted):
    """The one rule: the default IS bool(owned_paths(section_cut(text))) -- what handoff_gate asks."""
    assert dm.has_owned_paths(text) is bool(dm.owned_paths(dm.section_cut(text)))


@pytest.mark.parametrize("value", [None, 5, ["owns: C:\\x\\y.py"], b"owns: C:\\x\\y.py"])
def test_has_owned_paths_of_a_non_str_is_false(value):
    assert dm.has_owned_paths(value) is False and dm.has_owned_paths(value, include_quoted=True) is False


def test_has_owned_paths_a_real_header_beside_a_quoted_example_counts_by_default():
    text = "Review.\n> owns: tools/x.py\nowns: " + _OWNED + "\n"
    assert dm.has_owned_paths(text) is True


def test_has_owned_paths_degraded_cut_still_reads_the_header_lines():
    """A degraded read (every line is prose) keeps the header form: the answer is the owned_paths one."""
    text = "owns: " + _OWNED + "\n" + "x" * (md_regions.MAX_TEXT_CHARS + 10)
    assert dm.section_cut(text).degraded is True
    assert dm.has_owned_paths(text) is True


# =========================================================================
# t-877 (forge F6-26, D-0048): an owns line may carry a FUNCTION LIST after the path -- `path (f1, f2)`. The path is
# still found and still the whole path (the list is a note, never part of the token); a RELATIVE path with a list is
# still no declaration.
# =========================================================================

_SR = r"C:\proj\scripts\story_run.py"
_FN_LIST_TABLE = [
    ("owns: " + _SR + " (take_answer, fallback_person)", [_SR]),                       # the bare form
    ("owns: " + _SR + " (Driver.take_answer, last_resort)", [_SR]),                    # a Class.name member
    ("owns: `" + _SR + "` (take_answer, fallback_person)", [_SR]),                     # the BACKTICKED path, then the list
    ("owns: " + _SR + " (a, b), " + _OWNED + " (c)", [_SR, _OWNED]),                   # two paths, a list on each
    ("owns:\n" + _SR + " (take_answer, last_resort)\n" + _OWNED + "\n", [_SR, _OWNED]),  # the R11-f form: lines under the header
    ("owns: `C:\\Program Files\\x y.py` (f1, f2)", ["C:\\Program Files\\x y.py"]),    # a backticked path with spaces keeps its space
    ("owns: `" + _SR + "`", [_SR]),                                                    # control: no list, as before
    # t-880 F-5: form 1 INSIDE the backticks (the form the batch cells take), on the header and under it
    ("owns: `" + _SR + " (take_answer, fallback_person)`", [_SR]),
    ("owns: `" + _SR + " (Driver.take_answer, +new_one)`, `" + _OWNED + " (c)`", [_SR, _OWNED]),
    ("owns:\n`" + _SR + " (take_answer, last_resort)`\n`" + _OWNED + "`\n", [_SR, _OWNED]),
    ("owns:\n- `" + _SR + " (take_answer, last_resort)`\n", [_SR]),
    ("owns: `C:\\Program Files\\x y.py (f1, f2)`", ["C:\\Program Files\\x y.py"]),     # a space inside the path survives the cut
    ("owns: `C:\\Program Files\\x (1).py`", ["C:\\Program Files\\x (1).py"]),           # a bracket that is no function list stays in the path
]


@pytest.mark.parametrize("text, paths", _FN_LIST_TABLE)
def test_f626_an_owns_path_with_a_function_list_is_found_as_the_path_alone(text, paths):
    assert dm.has_owned_paths(text) is True and dm.has_owned_paths(text, include_quoted=True) is True
    assert [o.path for o in dm.owned_paths(dm.section_cut(text))] == paths


@pytest.mark.parametrize("text", ["owns: story_run.py (take_answer)", "owns: `scripts/story_run.py` (take_answer, last_resort)"])
def test_f626_a_relative_path_with_a_function_list_is_still_no_declaration(text):
    """The NEGATIVE control: the list does not turn a relative path into an owned one."""
    assert dm.has_owned_paths(text) is False and dm.owned_paths(dm.section_cut(text)) == []


def test_f626_an_unclosed_backtick_span_is_left_whole():
    """The cut applies to a CLOSED span only: `C:\\x\\y.py (f1 has no closing mark, so nothing is cut at ' ('."""
    assert dm._cut_note("`C:\\x\\y.py (f1") == "`C:\\x\\y.py (f1"
    assert dm._cut_note("`C:\\x\\y.py` (f1") == "`C:\\x\\y.py`"
    assert dm._cut_note("`C:\\x\\y.py`(f1") == "`C:\\x\\y.py`(f1"          # no space before the bracket: not the note form
