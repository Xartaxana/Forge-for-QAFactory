"""tools/test_dispatch_cut.py -- battery for the ONE cut of a dispatch text (B-204, t-608):
dispatch_manifest.section_cut / owned_paths / given_paths / path_candidates / split_new_marker.
Rows A1-A13 (adversarial) each run with LF and CRLF; P-rows that belong to the cut (P2, P7-P9,
P19, P22, P23). The path CHECK rows (refusals, doors, notes) are in test_dispatch_gate.py.

Run: python -m pytest tools/test_dispatch_cut.py -q
"""

import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dispatch_gate  # noqa: E402
import dispatch_manifest as dm  # noqa: E402
import md_regions  # noqa: E402
import owns_gate  # noqa: E402


@pytest.fixture(params=["\n", "\r\n"], ids=["LF", "CRLF"])
def eol(request):
    return request.param


def text(eol, *lines):
    return eol.join(lines) + eol


def owned(prompt):
    return [o.path for o in dm.owned_paths(dm.section_cut(prompt))]


# ---- A1-A13 ---------------------------------------------------------------------------------


_REST = ("given: x", "non-goals: none", "handoff: r", "edges: none -- x", "DoD: `python -m pytest x.py -q`")


def registered(eol, tmp_path, *lines):
    """The `owns` of the registry line a complete dispatch gets through owns_gate.decide (None: no line)."""
    registry = tmp_path / "reg.jsonl"
    payload = {"tool_name": "Task", "tool_input": {"prompt": text(eol, *lines, *_REST), "description": "sonnet: t"},
               "cwd": "D:\\ctl"}
    owns_gate.decide(payload, registry_path=registry)
    return json.loads(registry.read_text(encoding="utf-8").splitlines()[-1])["owns"] if registry.exists() else None


def test_A1_prose_with_owns_word_does_not_hijack_the_real_header(eol, tmp_path):
    prompt = text(eol, "Attempt 1 owns: D:/old/a.py was wrong.", "owns: D:/r/b.py")
    cut = dm.section_cut(prompt)
    assert [o.path for o in dm.owned_paths(cut)] == ["D:/r/b.py"]
    assert cut.sections["owns"][0].header_line == 1
    # the registry holds what the checker counts, not the prose line's tail (today: "D:/old/a.py was wrong")
    assert registered(eol, tmp_path, "Attempt 1 owns: D:/old/a.py was wrong.", "owns: D:/r/b.py") == ["D:/r/b.py"]


def test_A2_two_owns_sections_are_a_union_equal_to_the_checker(eol):
    prompt = text(eol, "Owns: D:/r/a.py, was the old plan", "owns: D:/r/b.py")
    assert owned(prompt) == ["D:/r/a.py", "D:/r/b.py"]


def test_A3_unclosed_fence_is_prose_for_the_cut_and_the_registry(eol):
    prompt = text(eol, "```", "given: x", "owns: D:/r/a.py")
    cut = dm.section_cut(prompt)
    assert not any(cut.quoted)
    assert owned(prompt) == ["D:/r/a.py"]
    assert cut.unterminated and dm.fence_start(cut, 2) == 0


def test_A4_a_fence_that_closes_inside_the_manifest_quotes_given_and_owns(eol):
    prompt = text(eol, "```", "given: x", "owns: D:/r/a.py", "```", "non-goals: none")
    cut = dm.section_cut(prompt)
    assert cut.sections["given"] == [] and cut.sections["owns"] == []
    assert cut.quoted_owns_headers == [2]
    assert dm.check({"tool_input": {"subagent_type": "builder", "prompt": prompt}})[0] == 2


def test_A5_blockquote_owns_is_a_quoted_header_not_a_section(eol):
    prompt = text(eol, "> owns: D:/r/a.py", "Edit file x.py")
    cut = dm.section_cut(prompt)
    assert cut.sections["owns"] == [] and cut.quoted_owns_headers == [0]
    assert owned(prompt) == []


def test_A6_two_prose_blocks_are_a_union(eol):
    prompt = text(eol, "owns: D:/r/a.py", "", "owns: D:/r/b.py")
    assert owned(prompt) == ["D:/r/a.py", "D:/r/b.py"]


def test_A7_no_manifest_no_sections(eol):
    cut = dm.section_cut(text(eol, "just prose", "more prose"))
    assert all(v == [] for v in cut.sections.values()) and cut.block is None
    assert dm.check({"tool_input": {"subagent_type": "builder", "prompt": "just prose"}})[0] == 2


@pytest.mark.parametrize("sep", ["\u2028", "\x85"])
def test_A8_unicode_line_boundaries_give_the_same_lines_for_every_reader(sep):
    prompt = "owns: D:/r/a.py" + sep + "given: x"
    cut = dm.section_cut(prompt)
    assert cut.lines == prompt.splitlines() and len(cut.lines) == 2
    assert [o.path for o in dm.owned_paths(cut)] == ["D:/r/a.py"] and cut.sections["given"]
    assert owns_gate.extract_owns_paths(prompt) == ["D:/r/a.py"]


def test_A9_ten_million_chars_degrade_and_stay_under_5_seconds(tmp_path):
    prompt = "owns: D:/r/a.py\n" + ("filler line of ordinary prose\n" * 333_334)
    assert len(prompt) >= 10_000_000
    t0 = time.perf_counter()
    cut = dm.section_cut(prompt)
    assert cut.degraded and cut.reason == "text_too_large" and not any(cut.quoted)
    assert [o.path for o in dm.owned_paths(cut)] == ["D:/r/a.py"]  # the registry reads the all-prose cut
    payload = {"tool_name": "Task", "tool_input": {"subagent_type": "builder", "prompt": prompt}}
    t1 = time.perf_counter()
    code, msg, note = dm.check(payload)
    assert (code, msg) == (0, "") and note.startswith("MANIFEST-UNCHECKED:")
    t2 = time.perf_counter()
    owns_gate.decide(dict(payload, cwd="D:\\ctl"), registry_path=tmp_path / "r.jsonl")
    t3 = time.perf_counter()
    assert dispatch_gate.decide(dict(payload, cwd="D:\\ctl")) == (0, "")
    t4 = time.perf_counter()
    print("A9 timings (%d chars): section_cut+owned_paths %.2fs, check %.2fs, owns_gate.decide %.2fs, "
          "dispatch_gate.decide %.2fs" % (len(prompt), t1 - t0, t2 - t1, t3 - t2, t4 - t3))
    for spent in (t2 - t1, t3 - t2, t4 - t3):  # the spec's budget: each reader under 5 s
        assert spent < 5
    assert t4 - t0 < 5 * 4


def test_A10_exactly_2_000_000_is_a_full_read_and_one_more_is_degraded():
    base = "owns: D:/r/a.py\n"
    full = base + "x" * (2_000_000 - len(base))
    assert len(full) == 2_000_000
    assert not dm.section_cut(full).degraded
    assert dm.section_cut(full + "x").degraded


def test_A10b_two_million_chars_twenty_thousand_regions_hundred_thousand_lines_under_5_seconds():
    spans = "text `a b` more\n" * 9_900  # ~19,800 regions: just under MAX_REGIONS (20,000)
    prompt = spans + ("y" * 19 + "\n") * 90_100  # 1.96M chars: just under MAX_TEXT_CHARS, 100,000 lines
    assert 1_900_000 < len(prompt) <= md_regions.MAX_TEXT_CHARS and len(prompt.splitlines()) == 100_000
    t0 = time.perf_counter()
    cut = dm.section_cut(prompt)
    spent = time.perf_counter() - t0
    print("A10b timing (%d chars, %d regions, %d lines): section_cut %.2fs"
          % (len(prompt), len(cut.regions), len(cut.lines), spent))
    assert not cut.degraded and spent < 5


def test_A12_continuation_limit_40_is_read_41_is_blind(eol):
    def prompt(n):
        return text(eol, "owns:", *["- D:/r/f%d.py" % i for i in range(n)])

    assert len(owned(prompt(40))) == 40
    assert owned(prompt(41)) == []


def test_A13_relative_glob_is_dropped_by_the_absolute_filter(eol):
    assert owned(text(eol, "owns: tools/*.py")) == []
    assert owned(text(eol, "owns: D:/r/tools/*.py")) == ["D:/r/tools/*.py"]


def test_A11_inline_code_owns_marker_is_not_a_header_and_registry_stays_blind(tmp_path):
    prompt = "- `owns:` D:/r/a.py\nEdit file x.py\n"
    cut = dm.section_cut(prompt)
    assert cut.sections["owns"] == [] and cut.quoted_owns_headers == []  # BLIND, not QUOTED (A11b)
    code, out = owns_gate.decide({"tool_name": "Task", "tool_input": {"prompt": prompt}, "cwd": "D:\\ctl"},
                                 registry_path=tmp_path / "r.jsonl")
    assert out["hookSpecificOutput"]["additionalContext"] == owns_gate.BLIND_OWNS_WARN_MESSAGE


# ---- the quoted flag equals the polarity of dispatch_gate._is_quoted at every line start -------


def test_quoted_flag_equals_is_quoted_at_each_line_start():
    prompt = text("\n", "prose", "> quote `a b` x", "> ```", "> fenced in quote", "> ```", "```py", "owns: x",
                  "```", "~~~", "tilde", "~~~", "tail", "```", "unterminated")
    cut = dm.section_cut(prompt)
    regions = md_regions.scan(prompt).regions
    starts = [r.start for r in regions]
    import bisect

    for i, off in enumerate(cut.offsets):
        k = bisect.bisect_right(starts, off) - 1
        region = regions[k] if k >= 0 and regions[k].start <= off < regions[k].end else None
        assert bool(cut.quoted[i]) == dispatch_gate._is_quoted(region), i


# ---- (new): read PER PATH at line level (M3 / M13) ----------------------------------------------


def test_P2_new_marker_binds_per_path_and_is_not_registered(eol):
    prompt = text(eol, "owns: D:/r/a.py (new), D:/r/b.py")
    got = dm.owned_paths(dm.section_cut(prompt))
    assert [(o.path, o.is_new) for o in got] == [("D:/r/a.py", True), ("D:/r/b.py", False)]
    prompt = text(eol, "owns:", "- D:/r/c.py (NEW) -- created here", "- D:/r/d.py")
    assert [(o.path, o.is_new) for o in dm.owned_paths(dm.section_cut(prompt))] == [
        ("D:/r/c.py", True), ("D:/r/d.py", False)]
    assert dm.split_new_marker("owns: D:/a (new), D:/b") == ("owns: D:/a, D:/b", {"D:/a"})


def test_P2b_new_marker_binds_to_one_path_on_a_continuation_line_too(eol):
    # the marker is on the SECOND path of the line: the first stays required-to-exist
    prompt = text(eol, "owns:", "D:/r/tools/missing.py -- rewrite; see D:/r/tools/new.py (new)",
                  "D:/r/tools/a.py  (new) -- extra spaces", "D:/r/tools/b.py -- no marker")
    assert [(o.path, o.is_new) for o in dm.owned_paths(dm.section_cut(prompt))] == [
        ("D:/r/tools/missing.py", False), ("D:/r/tools/a.py", True), ("D:/r/tools/b.py", False)]
    # `(new)` with no path before it marks nothing
    prompt = text(eol, "owns:", "D:/r/tools/c.py -- (new)")
    assert [(o.path, o.is_new) for o in dm.owned_paths(dm.section_cut(prompt))] == [("D:/r/tools/c.py", False)]


def test_P2c_a_typo_path_beside_a_marked_one_on_a_continuation_line_is_refused(tmp_path):
    root = tmp_path.as_posix()
    prompt = "\n".join(["given: x", "owns:",
                        "%s/tools/missing.py -- rewrite; see %s/tools/new.py (new)" % (root, root),
                        "non-goals: none", "handoff: r", "edges: none -- x",
                        "DoD: `python -m pytest x.py -q`"]) + "\n"
    d = dispatch_gate.decide_full({"tool_name": "Task", "cwd": str(tmp_path),
                                   "tool_input": {"prompt": prompt, "description": "sonnet: t"}})
    assert d.code == 2 and "missing.py" in d.message
    assert [(Path(p.path).name, p.status) for p in d.paths] == [("missing.py", "missing")]


def test_P19_a_note_in_brackets_is_cut_never_part_of_the_path(eol):
    prompt = text(eol, "owns: D:/r/md_regions.py (docstring EDGE (c) only), D:/r/w.json (only if X)")
    assert owned(prompt) == ["D:/r/md_regions.py", "D:/r/w.json"]
    prompt = text(eol, "owns: `D:/r/Program Files (x86)/a.py`")
    assert owned(prompt) == ["D:/r/Program Files (x86)/a.py"]  # an explicit span is kept whole


# ---- path_candidates: the ONE predicate -------------------------------------------------------


TOP = frozenset({"tools", "docs"})


def test_P7_P22_backticked_spans():
    assert dm.path_candidates("`C:\\path with spaces\\a.py`", TOP) == ["C:\\path with spaces\\a.py"]
    assert dm.path_candidates("`git diff origin/main...HEAD` and `python tools/x.py --check`", TOP) == []
    assert dm.path_candidates("see `other/dir/x.py`", TOP) == ["other/dir/x.py"]  # backticked with a slash


def test_P8_url_and_placeholders_are_never_candidates():
    assert dm.path_candidates("https://tools/x.py <tools/x.py> {tools/y} $X/z tools/<n>.py", TOP) == []


def test_P9_anchors_and_trailing_punctuation_are_stripped_the_drive_colon_kept():
    line = "tools/a.py:805-815, tools/b.py~:805 tools/c.py::test_x tools/d.py#L10. (tools/e.py), C:/r/f.py:3"
    assert dm.path_candidates(line, TOP) == [
        "tools/a.py", "tools/b.py", "tools/c.py", "tools/d.py", "tools/e.py", "C:/r/f.py"]


def test_F3_relative_word_needs_a_top_level_entry_of_the_root():
    assert dm.path_candidates("tools/a.py yes/no and/or ../x/y.py", TOP) == ["tools/a.py"]
    assert dm.path_candidates("tools/a.py", None) == []  # the rule is off without the root's entries


# ---- given_paths: P23 / P10 (M9) -------------------------------------------------------------


def test_P23_given_never_crosses_the_next_header(eol):
    prompt = text(eol, "given: tools/a.py", "- tools/b.py", "owns: D:/r/x.py", "DoD: `python -m pytest tools/x.py`")
    got = dm.given_paths(dm.section_cut(prompt), TOP)
    assert [g.path for g in got] == ["tools/a.py", "tools/b.py"]


def test_P10_given_stops_at_the_first_blank_line_and_skips_quoted_lines(eol):
    prompt = text(eol, "given: tools/a.py", "> tools/quoted.py", "tools/c.py", "", "tools/after_blank.py")
    assert [g.path for g in dm.given_paths(dm.section_cut(prompt), TOP)] == ["tools/a.py", "tools/c.py"]


def test_cut_raises_nothing_on_non_string_and_empty_input():
    for bad in (None, 5, b"x", ""):
        cut = dm.section_cut(bad)
        assert cut.lines == [] and cut.block is None and not cut.degraded
