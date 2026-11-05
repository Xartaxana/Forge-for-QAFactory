"""Tests for tools/crap_report.py -- the CRAP report (t-519, B-418 = B-299).

Keys (the spec's K1..K16, the amendments B1..B8 of t-521 included):
K1 complexity per branch kind (if/elif, loops, handlers, ternary, boolean operands, comprehensions, match with
   its irrefutable trailing case, with/assert/else/finally = 0, lambda and nested-class statements count to the
   enclosing unit, a nested def's decorator and defaults too).  K2 coverage and CRAP of a hand coverage.py JSON,
   boundaries included.  K3 negative control: the same function ranks first uncovered and last covered.
K4 nested defs split lines and decision points.  K5 zero executable lines (a docstring-only def, a one-line def:
   coverage n/a, CRAP = c).  K6 no source: every row `none`, CRAP a bound.  K7 another tree: suffix attribution,
   an unmatched key, an ambiguous key, a file claimed twice.  K8 the golden record: accepted (hits stems vs the
   `.py` names, B1), accepted through a CRLF/LF conversion of the sha (B2), refused on a changed byte, on hits
   that do not match the record, on a covered_lines that is not the union.  K9 a recorded line beyond the end
   of the file, at and beyond the boundary.  K10 a hashes file: match, mismatch, no hash.  K11 an unparsable
   file is listed and the run completes.  K12 `--top`, usage errors, `--json` against markdown, determinism,
   relative ASCII output.  K13 sizes (no timing assertion).  K14 duplicate qualnames.  K15 `--require-coverage`.
   K16 the CI job `crap-measure` pinned by reading the yaml.
Every fixture is written into tmp_path; the real tree is read only by K16 (the yaml) and the import checks.
"""
import ast
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import crap_report as CR  # noqa: E402
import dup_report as DR  # noqa: E402

SCRIPT = TOOLS / "crap_report.py"


# ---------------------------------------------------------------- helpers

def put(root, files):
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
    return root


def hand_cov(files):
    """A coverage.py JSON text: files = {key: (executed lines, missing lines)}."""
    return json.dumps({"meta": {"version": "7.16.2"}, "files": {
        k: {"executed_lines": list(e), "missing_lines": list(m)} for k, (e, m) in files.items()}})


def go(root, capsys, *flags, paths=("*.py",)):
    rc = CR.run(["--repo", str(root), "--paths", *paths, *flags])
    cap = capsys.readouterr()
    return rc, cap.out, cap.err


def gj(root, capsys, *flags, paths=("*.py",)):
    rc, out, err = go(root, capsys, "--json", *flags, paths=paths)
    return rc, (json.loads(out) if out.strip() else None), err


def row(rep, name, path=None):
    found = [r for r in rep["rows"] if r["function"] == name and (path is None or r["path"] == path)]
    assert len(found) == 1, f"{name}: {len(found)} rows in {[r['function'] for r in rep['rows']]}"
    return found[0]


def branchy(name, c, first=1):
    """A function of complexity c with no decorators; -> (source text, its executable lines)."""
    if c == 1:
        return f"def {name}(x):\n    return x\n", [first + 1]
    body = "".join(f"    if x == {i}:\n        x = {i}\n" for i in range(c - 1))
    return f"def {name}(x):\n{body}", list(range(first + 1, first + 1 + 2 * (c - 1)))


def no_path(root, text):
    """The text names neither the temporary directory nor its (unique) last component: no absolute path leaks,
    even in the doubled-backslash form an ASCII escape gives a Windows path."""
    return str(root) not in text and root.name not in text


def head_line(out, label):
    m = re.search(r"^- " + re.escape(label) + r": (.*)$", out, re.M)
    assert m, f"no head line `{label}` in:\n{out}"
    return m.group(1)


# ---------------------------------------------------------------- K1 complexity

COMPLEXITY = {
    "plain": ("def f(x):\n    return x\n", 1),
    "if_elif_else": ("def f(x):\n    if x == 1:\n        return 1\n    elif x == 2:\n        return 2\n"
                     "    else:\n        return 3\n", 3),
    "for_with_else": ("def f(xs):\n    for x in xs:\n        pass\n    else:\n        pass\n", 2),
    "async_for_and_while": ("async def f(xs):\n    async for x in xs:\n        pass\n    while xs:\n        break\n", 3),
    "except_else_finally": ("def f():\n    try:\n        pass\n    except KeyError:\n        pass\n"
                            "    except (OSError, ValueError):\n        pass\n    else:\n        pass\n"
                            "    finally:\n        pass\n", 3),
    "except_star": ("def f():\n    try:\n        pass\n    except* KeyError:\n        pass\n", 2),
    "ternary": ("def f(x):\n    return 1 if x else 2\n", 2),
    "and_or": ("def f(a, b, c):\n    return a and b or c\n", 3),
    "three_operands": ("def f(a, b, c):\n    return a and b and c\n", 3),
    "comprehension_two_ifs": ("def f(xs):\n    return [x for x in xs if x if x > 1]\n", 4),
    "comprehension_two_generators": ("def f(xs, ys):\n    return {x: y for x in xs for y in ys}\n", 3),
    "match_wildcard": ("def f(x):\n    match x:\n        case 1:\n            return 1\n        case 2:\n"
                       "            return 2\n        case _:\n            return 3\n", 3),
    "match_capture": ("def f(x):\n    match x:\n        case 1:\n            return 1\n        case y:\n"
                      "            return y\n", 2),
    "match_guarded_wildcard": ("def f(x):\n    match x:\n        case 1:\n            return 1\n        case 2:\n"
                               "            return 2\n        case _ if x:\n            return 3\n", 4),
    "with_assert_zero": ("def f(x):\n    with x:\n        assert x\n", 1),
    "lambda_ternary_counts_to_outer": ("def f(x):\n    g = lambda y: 1 if y else 2\n    return g\n", 2),
    "nested_class_statements_count_to_outer": ("def f(x):\n    class K:\n        if x:\n            y = 1\n"
                                               "    return K\n", 2),
}


@pytest.mark.parametrize("source,expected", list(COMPLEXITY.values()), ids=list(COMPLEXITY))
def test_complexity_per_branch_kind(tmp_path, capsys, source, expected):
    put(tmp_path, {"a.py": source})
    rc, rep, _ = gj(tmp_path, capsys)
    assert rc == 0 and row(rep, "f")["complexity"] == expected


def test_a_nested_defs_decorator_and_defaults_count_to_the_enclosing_unit(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(a, b):\n    @d(a or b)\n    def g(z=a and b):\n        return z\n    return g\n"})
    _, rep, _ = gj(tmp_path, capsys)
    assert (row(rep, "f")["complexity"], row(rep, "f.g")["complexity"]) == (3, 1)


# ---------------------------------------------------------------- K2, K3 coverage and CRAP

@pytest.mark.parametrize("c,ran,expected", [(3, 1, 6.7969), (1, 0, 2.0), (5, 0, 30.0), (5, 8, 5.0), (4, 3, 6.0)],
                         ids=["c3-cov25", "c1-cov0", "c5-cov0", "c5-cov1", "c4-cov50"])
def test_crap_of_a_hand_coverage_json(tmp_path, capsys, c, ran, expected):
    text, lines = branchy("f", c)
    put(tmp_path, {"a.py": text, "cov.json": hand_cov({"a.py": (lines[:ran], lines[ran:])})})
    rc, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    r = row(rep, "f")
    assert rc == 0 and r["crap"] == pytest.approx(expected, abs=1e-4) and not r["crap_is_bound"]
    assert r["coverage"] == pytest.approx(ran / len(lines), abs=1e-4)


def test_the_markdown_cells_carry_one_decimal(tmp_path, capsys):
    text, lines = branchy("f", 3)
    put(tmp_path, {"a.py": text, "cov.json": hand_cov({"a.py": (lines[:1], lines[1:])})})
    _, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert "| 1 | a.py:1 | f | 3 | 25.0% | 6.8 |" in out


def three_functions(tmp_path, covered):
    """a (c=4), b (c=2), c_ (c=3) in one file; `covered` = the names fully executed, the others fully missing."""
    text, spans, first = "", {}, 1
    for name, c in (("a", 4), ("b", 2), ("c_", 3)):
        part, lines = branchy(name, c, first)
        text, spans[name], first = text + part, lines, first + part.count("\n")
    ran = [n for k in covered for n in spans[k]]
    miss = [n for k, v in spans.items() if k not in covered for n in v]
    return put(tmp_path, {"a.py": text, "cov.json": hand_cov({"a.py": (ran, miss)})})


def test_negative_control_the_same_function_ranks_first_uncovered_and_last_covered(tmp_path, capsys):
    three_functions(tmp_path, covered=("b", "c_"))
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert [r["function"] for r in rep["rows"]][0] == "a"
    three_functions(tmp_path, covered=("a",))
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert [r["function"] for r in rep["rows"]] == ["c_", "b", "a"]


def test_a_line_listed_as_executed_and_missing_counts_as_missing(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"a.py": ([2], [2])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert row(rep, "f")["coverage"] == 0.0


# ---------------------------------------------------------------- K4, K5 lines of a unit

NESTED = ("def outer(x):\n"          # 1
          "    if x:\n"              # 2
          "        y = 1\n"          # 3
          "    @deco\n"              # 4
          "    def inner(z):\n"      # 5
          "        if z:\n"          # 6
          "            return 1\n"   # 7
          "        return 2\n"       # 8
          "    return inner\n")      # 9


def test_a_nested_def_splits_decision_points_and_lines_from_its_outer_unit(tmp_path, capsys):
    put(tmp_path, {"a.py": NESTED, "cov.json": hand_cov({"a.py": ([2, 3, 4, 5, 6, 9], [7, 8])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    outer, inner = row(rep, "outer"), row(rep, "outer.inner")
    assert (outer["complexity"], inner["complexity"]) == (2, 2)
    # outer owns lines 2, 3, 4 (the nested decorator), 5 (the nested def line), 9: all executed
    assert outer["coverage"] == 1.0
    # inner owns 6, 7, 8: one executed of three
    assert inner["coverage"] == pytest.approx(1 / 3, abs=1e-4)


def test_a_nested_class_body_runs_with_its_function_so_its_lines_belong_to_the_function(tmp_path, capsys):
    # critic t-538 F1: the class body's missed branch must lower f's coverage (it errs toward MORE crap)
    put(tmp_path, {"a.py": "def f(x):\n    y = 1\n    class K:\n        if x:\n            z = 1\n    return K\n",
                   "cov.json": hand_cov({"a.py": ([2, 3, 6], [4, 5])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    r = row(rep, "f")
    assert r["complexity"] == 2 and r["coverage"] == pytest.approx(0.6) and r["crap"] == pytest.approx(2.256, abs=1e-4)


def test_a_method_of_a_nested_class_is_still_cut_out_of_the_function(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    class K:\n        a = 1\n        def m(self):\n            return 2\n"
                           "    return K\n",
                   "cov.json": hand_cov({"a.py": ([2, 3, 4, 6], [5])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert (row(rep, "f")["coverage"], row(rep, "f.K.m")["coverage"]) == (1.0, 0.0)


@pytest.mark.parametrize("source,executed", [
    ("def f():\n    \"\"\"only a docstring\"\"\"\n", []),
    ("def f(): return 1\n", [1]),
    ("@deco\ndef f(): return 1\n", [1, 2]),
], ids=["docstring-only", "one-line-def", "decorated-one-line-def"])
def test_a_unit_with_no_executable_line_of_its_own_prints_na_and_costs_its_complexity(tmp_path, capsys, source, executed):
    put(tmp_path, {"a.py": source, "cov.json": hand_cov({"a.py": (executed, [])})})
    rc, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert rc == 0 and "| f | 1 | n/a | 1.0 |" in out


def test_na_never_ranks_above_an_uncovered_function_of_the_same_complexity(tmp_path, capsys):
    text, lines = branchy("g", 1, first=3)
    put(tmp_path, {"a.py": "def f(): return 1\n\n" + text, "cov.json": hand_cov({"a.py": ([1], lines)})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert [r["function"] for r in rep["rows"]] == ["g", "f"]


# ---------------------------------------------------------------- K6, E2 no usable source

def test_without_a_source_every_function_is_unmeasured_and_its_crap_a_bound(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    if x:\n        return 1\n    return 2\n"})
    rc, out, err = go(tmp_path, capsys)
    assert rc == 0 and "files read in" in err
    assert head_line(out, "coverage source").startswith("none -- every function counted at coverage 0")
    assert "upper bound" in out and "| 1 | a.py:1 | f | 2 | none | <=6.0 |" in out
    _, rep, _ = gj(tmp_path, capsys)
    r = row(rep, "f")
    assert r["coverage"] is None and r["crap_is_bound"] and r["crap"] == 6.0
    assert (rep["totals"]["measured"], rep["totals"]["unmeasured"]) == (0, 1)


@pytest.mark.parametrize("content", [None, "not json {", "[1, 2]", '{"a": 1}', '{"files": 3}'],
                         ids=["missing", "bad-json", "not-an-object", "unknown-shape", "files-not-a-dict"])
def test_a_broken_source_never_yields_numbers_and_names_itself(tmp_path, capsys, content):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n"})
    if content is not None:
        put(tmp_path, {"cov.json": content})
    rc, out, err = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert rc == 0 and "`cov.json` unusable" in head_line(out, "coverage source") and "| none | <=2.0 |" in out
    assert no_path(tmp_path, out)
    assert go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), "--require-coverage")[0] == 1


# ---------------------------------------------------------------- K7 attribution of record keys

def test_a_key_from_another_tree_is_attributed_by_its_suffix_and_an_unknown_one_is_counted(tmp_path, capsys):
    put(tmp_path, {"pkg/a.py": "def f(x):\n    return x\n", "pkg/b.py": "def g(x):\n    return x\n",
                   "cov.json": hand_cov({"/other/root/pkg/a.py": ([2], []), "C:\\elsewhere\\pkg\\b.py": ([2], []),
                                         "/other/root/pkg/zzz.py": ([1], [])})})
    rc, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("pkg/*.py",))
    cov = rep["coverage"]
    assert rc == 0 and cov["counts"] == {"matched": 2, "unmatched": 1, "ambiguous": 0, "refused": 0}
    assert cov["names"]["unmatched"] == [".../pkg/zzz.py"] and cov["entries"] == 3
    assert cov["names"]["matched"] == ["pkg/a.py", "pkg/b.py"]       # the scanned repo path, not the record's key
    assert row(rep, "f")["coverage"] == 1.0 and row(rep, "g")["coverage"] == 1.0
    assert not any(token in json.dumps(rep) for token in ("/other/root", "elsewhere", "C:"))


def test_no_absolute_key_of_the_record_reaches_the_output_whatever_its_group(tmp_path, capsys):
    src = "def f(x):\n    return x\n"
    put(tmp_path, {"a.py": src, "pkg/a.py": src, "b.py": src, "c.py": src,
                   "cov.json": hand_cov({"/home/someone/r/pkg/a.py": ([2], []),            # ambiguous (a.py, pkg/a.py)
                                         "C:/work/someone/proj/b.py": ([2, 99], []),      # refused: beyond the file
                                         "/home/someone/other/zz.py": ([1], []),           # unmatched
                                         "/home/someone/c.py": ([2], [])})})               # matched
    flags = ("--coverage", str(tmp_path / "cov.json"))
    both = ("*.py", "pkg/*.py")
    _, rep, _ = gj(tmp_path, capsys, *flags, paths=both)
    names = rep["coverage"]["names"]
    assert names["matched"] == ["c.py"] and names["refused"][0]["name"] == "b.py"
    assert names["unmatched"] == [".../other/zz.py"] and names["ambiguous"] == [".../pkg/a.py"]
    _, out, _ = go(tmp_path, capsys, *flags, paths=both)
    assert "someone" not in out and "someone" not in json.dumps(rep) and "C:" not in out


def test_a_backslash_key_is_printed_with_forward_slashes(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"pkg\\zzz.py": ([1], [])})})
    _, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert "  - unmatched: `pkg/zzz.py`" in out


def test_an_absolute_key_under_repo_is_made_relative(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({str(tmp_path / "a.py"): ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert rep["coverage"]["counts"]["matched"] == 1 and no_path(tmp_path, json.dumps(rep))


def test_the_suffix_match_stops_at_a_path_boundary(tmp_path, capsys):
    put(tmp_path, {"pkg/a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"/r/xpkg/a.py": ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("pkg/*.py",))
    assert rep["coverage"]["counts"]["unmatched"] == 1 and row(rep, "f")["coverage"] is None
    put(tmp_path, {"cov.json": hand_cov({"/r/xa.py": ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("pkg/*.py",))
    assert rep["coverage"]["counts"]["unmatched"] == 1


def test_a_key_with_two_candidates_is_ambiguous_and_never_attributed(tmp_path, capsys):
    src = "def f(x):\n    return x\n"
    put(tmp_path, {"a.py": src, "pkg/a.py": src, "cov.json": hand_cov({"/r/pkg/a.py": ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("a.py", "pkg/a.py"))
    assert rep["coverage"]["counts"]["ambiguous"] == 1 and rep["totals"]["measured"] == 0


def test_a_file_claimed_by_two_entries_is_ambiguous_for_both(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n",
                   "cov.json": hand_cov({"/r1/a.py": ([2], []), "/r2/a.py": ([], [2])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert rep["coverage"]["counts"]["ambiguous"] == 2 and row(rep, "f")["coverage"] is None


# The report of the fixture below, recorded from the code BEFORE judge() stopped renaming its entries (B-456, t-609).
GOLDEN_FIXTURE_REPORT = (
    '# CRAP report\n'
    '\n'
    '- paths: `*.py`, `pkg/*.py`\n'
    "- formula: CRAP = c^2 x (1 - cov)^3 + c; c = 1 + if/elif, for, while, except, ternary, comprehension generator and its ifs, match case (not a final bare `case _`), boolean operand after the first; cov = line coverage of the function's own lines\n"
    '- coverage source: `cov.json` (coverage.py)\n'
    '- bytes not verified: no --coverage-hashes, a record of other bytes whose lines all fit reads as current\n'
    '- record entries: 7; matched 2; unmatched 1; ambiguous 3; refused 1\n'
    '  - matched: `c.py`, `pkg/b.py`\n'
    '  - unmatched: `.../x/zz.py`\n'
    '  - ambiguous: `.../pkg/a.py`, `.../r1/e.py`, `e.py`\n'
    "  - refused: `d.py` (a recorded line (99) is beyond the file's 4 lines: the record measured other bytes)\n"
    '- functions in files with no usable record are counted at coverage 0: their CRAP is an upper bound (printed `<=N`)\n'
    '- files read: 6\n'
    '- files unreadable: 0\n'
    '- functions: 6\n'
    '- measured: 2\n'
    '- unmeasured: 4\n'
    '- shown: 6\n'
    '\n'
    '| # | path:line | function | complexity | coverage | CRAP |\n'
    '|---|---|---|---|---|---|\n'
    '| 1 | a.py:1 | f | 2 | none | <=6.0 |\n'
    '| 2 | d.py:1 | f | 2 | none | <=6.0 |\n'
    '| 3 | e.py:1 | f | 2 | none | <=6.0 |\n'
    '| 4 | pkg/a.py:1 | f | 2 | none | <=6.0 |\n'
    '| 5 | c.py:1 | f | 2 | 66.7% | 2.1 |\n'
    '| 6 | pkg/b.py:1 | f | 2 | 100.0% | 2.0 |\n'
    '\n'
)


def test_the_report_of_a_mixed_record_is_byte_equal_to_the_golden_one_of_every_group(tmp_path, capsys):
    src = "def f(x):\n    if x:\n        return 1\n    return 2\n"
    put(tmp_path, {rel: src for rel in ("a.py", "pkg/a.py", "pkg/b.py", "c.py", "d.py", "e.py")})
    put(tmp_path, {"cov.json": json.dumps({"files": {
        str(tmp_path / "c.py"): {"executed_lines": [2, 3], "missing_lines": [4]},     # absolute, under --repo: matched
        "/other/root/pkg/b.py": {"executed_lines": [2, 3, 4], "missing_lines": []},   # a foreign tree's suffix: matched
        "/home/x/pkg/a.py": {"executed_lines": [2], "missing_lines": []},             # two candidates: ambiguous
        "/home/x/zz.py": {"executed_lines": [1], "missing_lines": []},                # unmatched
        "d.py": {"executed_lines": [2, 99], "missing_lines": []},                     # a line beyond the file: refused
        "e.py": {"executed_lines": [2], "missing_lines": [3]},                        # two entries claim e.py: both
        "/r1/e.py": {"executed_lines": [2], "missing_lines": []}}})})                 # ambiguous
    rc, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("*.py", "pkg/*.py"))
    assert rc == 0 and out == GOLDEN_FIXTURE_REPORT


def judge_inputs(tmp_path, *names):
    """-> (the Source of one entry per name, the arguments judge() takes after it); every entry covers pkg/a.py."""
    put(tmp_path, {"pkg/a.py": "def f(x):\n    return x\n"})
    scanned = ["pkg/a.py"]
    parsed, _ = CR.parse_files(tmp_path, scanned)
    return CR.Source("cov.json", "coverage.py", [CR.Entry(n, executed=[2]) for n in names]), (None, parsed, scanned, tmp_path)


@pytest.mark.parametrize("which", ["relative", "absolute under repo", "foreign absolute", "backslash relative"])
def test_judge_returns_a_verdict_and_leaves_its_entries_alone_also_when_judged_twice(tmp_path, which):
    name = {"relative": "pkg/a.py", "absolute under repo": None, "foreign absolute": "/other/root/pkg/a.py",
            "backslash relative": "pkg\\a.py"}[which]
    name = name or str(tmp_path / "pkg" / "a.py")
    source, rest = judge_inputs(tmp_path, name)
    before = [(e.name, sorted(e.executed), e.missing) for e in source.entries]
    first = CR.judge(source, *rest)
    assert [(e.name, sorted(e.executed), e.missing) for e in source.entries] == before     # no rename, no change
    assert CR.judge(source, *rest) == first and first[1]["matched"] == ["pkg/a.py"]
    assert [e.name for e in source.entries] == [before[0][0]]


def test_judge_relativises_each_entry_once(tmp_path, monkeypatch):
    names = ["pkg/a.py", str(tmp_path / "pkg" / "a.py"), "/other/root/zz.py", "pkg\\b.py"]
    source, rest = judge_inputs(tmp_path, *names)
    calls = []
    real = CR.relativise
    monkeypatch.setattr(CR, "relativise", lambda key, repo: calls.append(key) or real(key, repo))
    CR.judge(source, *rest)
    assert len(calls) == len(names)                       # not twice per entry (judge's own pass, then attribute's)
    calls.clear()
    CR.judge(source, *rest)
    assert len(calls) == len(names)                       # and the second judgement starts from the same names


def test_files_absent_from_the_record_are_unmeasured_and_counted(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "b.py": "def g(x):\n    return x\n",
                   "cov.json": hand_cov({"a.py": ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert (rep["totals"]["measured"], rep["totals"]["unmeasured"], rep["totals"]["files_measured"]) == (1, 1, 1)
    assert row(rep, "g")["crap_is_bound"] and not row(rep, "f")["crap_is_bound"]


# ---------------------------------------------------------------- K8 the golden record

GOLDEN_SRC = "def f(x):\n    if x:\n        y = 1\n        z = 2\n    return x\n"


def make_golden(root, source=GOLDEN_SRC, sha=None, tests=("test_a.py", "test_b.py"), stems=None, covered=None,
                scripts="scripts"):
    """scripts/story_run.py plus golden/coverage-n0.json and golden/coverage-hits/*.json: lines 2, 3, 5 ran
    (the two hits files overlap on line 3), line 4 never ran."""
    raw = source if isinstance(source, bytes) else source.encode("utf-8")
    put(root, {f"{scripts}/story_run.py": raw})
    stems = [t[:-3] for t in tests] if stems is None else stems
    for stem, lines in zip(stems, ([2, 3], [3, 5], [5])):
        put(root, {f"golden/coverage-hits/{stem}.json": json.dumps({"story_run.py": lines})})
    record = {"schema": 1, "python": "3.13", "story_run_sha256": sha or hashlib.sha256(raw).hexdigest(),
              "covered_lines": 3 if covered is None else covered, "executable_lines": 4, "never_run_lines": 1,
              "never_run": [{"function": "f", "guard": "if-body", "home": "", "lines": [4, 4]}],
              "test_files_in_the_record": list(tests)}
    put(root, {"golden/coverage-n0.json": json.dumps(record, indent=1)})
    return root / "golden" / "coverage-n0.json"


def golden_run(root, capsys, record):
    rc, rep, _ = gj(root, capsys, "--coverage", str(record), paths=("scripts/*.py",))
    return rc, rep


def lf_to_crlf(raw):
    return raw.replace(b"\n", b"\r\n")


def test_the_golden_is_accepted_and_its_functions_are_measured(tmp_path, capsys):
    rc, rep = golden_run(tmp_path, capsys, make_golden(tmp_path))
    assert rc == 0 and rep["coverage"]["kind"] == "driver golden"
    assert rep["coverage"]["counts"] == {"matched": 1, "unmatched": 0, "ambiguous": 0, "refused": 0}
    r = row(rep, "f")
    assert r["coverage"] == 0.75 and r["crap"] == pytest.approx(2.0625, abs=1e-4) and r["path"] == "scripts/story_run.py"


@pytest.mark.parametrize("disk,recorded", [
    ("lf", "crlf"),            # the record carries the CRLF working-tree sha, the checkout is LF (B-409)
    ("crlf", "lf"),
    ("mixed", "lf"),
    ("mixed", "crlf"),
], ids=["lf-file-crlf-sha", "crlf-file-lf-sha", "mixed-file-lf-sha", "mixed-file-crlf-sha"])
def test_a_line_ending_conversion_of_the_golden_sha_is_accepted(tmp_path, capsys, disk, recorded):
    lf = GOLDEN_SRC.encode()
    on_disk = {"lf": lf, "crlf": lf_to_crlf(lf), "mixed": lf.replace(b"\n", b"\r\n", 2)}[disk]
    sha = hashlib.sha256(lf if recorded == "lf" else lf_to_crlf(lf)).hexdigest()
    rc, rep = golden_run(tmp_path, capsys, make_golden(tmp_path, source=on_disk, sha=sha))
    assert rep["coverage"]["counts"]["matched"] == 1, rep["coverage"]["names"]["refused"]


def test_a_changed_byte_inside_a_line_refuses_the_golden_in_every_line_ending_form(tmp_path, capsys):
    recorded = hashlib.sha256(GOLDEN_SRC.encode()).hexdigest()
    other = GOLDEN_SRC.replace("y = 1", "y = 2").encode()
    for on_disk in (other, lf_to_crlf(other)):
        rc, rep = golden_run(tmp_path, capsys, make_golden(tmp_path, source=on_disk, sha=recorded))
        assert rc == 0 and rep["coverage"]["counts"]["refused"] == 1
        assert "story_run_sha256" in rep["coverage"]["names"]["refused"][0]["reason"]
        assert row(rep, "f")["coverage"] is None and row(rep, "f")["crap_is_bound"]


@pytest.mark.parametrize("kwargs,reason", [
    ({"stems": ["test_a", "test_c"]}, "do not match test_files_in_the_record"),
    ({"stems": ["test_a"], "tests": ("test_a.py",)}, "hold 2 distinct lines"),
    ({"covered": 99}, "covered_lines 99"),
], ids=["hits-stem-differs", "hits-union-short", "covered-lines-differs"])
def test_a_golden_whose_hits_do_not_match_its_record_is_refused_with_the_reason(tmp_path, capsys, kwargs, reason):
    rc, rep = golden_run(tmp_path, capsys, make_golden(tmp_path, **kwargs))
    refused = rep["coverage"]["names"]["refused"]
    assert rc == 0 and rep["coverage"]["counts"]["refused"] == 1 and reason in refused[0]["reason"]
    _, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "golden/coverage-n0.json"), paths=("scripts/*.py",))
    assert reason in out


def test_a_golden_without_its_hits_directory_is_refused(tmp_path, capsys):
    record = make_golden(tmp_path)
    for f in (record.parent / "coverage-hits").glob("*.json"):
        f.unlink()
    (record.parent / "coverage-hits").rmdir()
    _, rep = golden_run(tmp_path, capsys, record)
    assert rep["coverage"]["counts"]["refused"] == 1 and rep["totals"]["measured"] == 0


def test_the_goldens_basename_key_is_attributed_to_the_one_path_that_ends_with_it(tmp_path, capsys):
    record = make_golden(tmp_path)
    put(tmp_path, {"other/story_run.py": GOLDEN_SRC})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(record), paths=("scripts/*.py", "other/*.py"))
    assert rep["coverage"]["counts"]["ambiguous"] == 1 and rep["totals"]["measured"] == 0
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(record), paths=("other/*.py",))
    assert rep["coverage"]["counts"]["matched"] == 1, "a basename key matches the path that ends with it"
    (tmp_path / "scripts" / "story_run.py").unlink()
    put(tmp_path, {"scripts/other.py": GOLDEN_SRC})
    _, rep = golden_run(tmp_path, capsys, record)
    assert rep["coverage"]["counts"]["unmatched"] == 1


# ---------------------------------------------------------------- K9 beyond the end of the file

@pytest.mark.parametrize("trailing_newline,line,refused", [
    (True, 5, False), (True, 6, True), (False, 5, False), (False, 6, True),
], ids=["nl-at-end", "nl-beyond", "no-nl-at-end", "no-nl-beyond"])
def test_a_recorded_line_beyond_the_files_last_line_refuses_it_at_and_beyond_the_boundary(
        tmp_path, capsys, trailing_newline, line, refused):
    text = "def f(x):\n    a = 1\n    b = 2\n    c = 3\n    return x" + ("\n" if trailing_newline else "")
    for kind, files in (("executed", ([2, line], [])), ("missing", ([2], [line]))):
        put(tmp_path, {"a.py": text, "cov.json": hand_cov({"a.py": files})})
        _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
        counts = rep["coverage"]["counts"]
        assert (counts["refused"], counts["matched"]) == ((1, 0) if refused else (0, 1)), kind
        if refused:
            assert "beyond the file's 5 lines" in rep["coverage"]["names"]["refused"][0]["reason"]
            assert row(rep, "f")["crap_is_bound"]


# ---------------------------------------------------------------- K10 the hashes file

def hashes_run(tmp_path, capsys, lines, extra=()):
    put(tmp_path, {"hashes.txt": "".join(line + "\n" for line in lines)})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"),
                   "--coverage-hashes", str(tmp_path / "hashes.txt"), *extra)
    return rep


def test_a_hashes_file_accepts_a_matching_file_in_both_sha256sum_forms_and_refuses_the_rest(tmp_path, capsys):
    src = b"def f(x):\n    return x\n"
    put(tmp_path, {"a.py": src, "b.py": src, "cov.json": hand_cov({"a.py": ([2], []), "b.py": ([2], [])})})
    good = hashlib.sha256(src).hexdigest()
    rep = hashes_run(tmp_path, capsys, [f"{good}  a.py", f"{good} *b.py"])
    assert rep["coverage"]["counts"]["matched"] == 2 and rep["coverage"]["bytes_verified"]
    rep = hashes_run(tmp_path, capsys, [f"{good}  a.py", f"{'0' * 64}  b.py"])
    assert rep["coverage"]["counts"]["matched"] == 1 and rep["coverage"]["counts"]["refused"] == 1
    assert "differs from the hashes file" in rep["coverage"]["names"]["refused"][0]["reason"]
    rep = hashes_run(tmp_path, capsys, [f"{good}  a.py", "garbage line"])
    assert rep["coverage"]["names"]["refused"][0]["name"] == "b.py"
    assert rep["coverage"]["names"]["refused"][0]["reason"].startswith("no hash")
    assert rep["coverage"]["hashes"]["ignored"] == 1


def test_a_hash_taken_on_the_other_line_ending_form_still_matches(tmp_path, capsys):
    src = b"def f(x):\n    return x\n"
    put(tmp_path, {"a.py": src, "cov.json": hand_cov({"a.py": ([2], [])})})
    rep = hashes_run(tmp_path, capsys, [hashlib.sha256(lf_to_crlf(src)).hexdigest() + "  a.py"])
    assert rep["coverage"]["counts"]["matched"] == 1


def test_an_unreadable_hashes_file_leaves_every_file_unmeasured(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"a.py": ([2], [])})})
    rc, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"),
                    "--coverage-hashes", str(tmp_path / "nope.txt"))
    assert rc == 0 and "`nope.txt` unusable" in head_line(out, "hashes") and "bytes not verified" not in out
    assert "| none | <=2.0 |" in out and no_path(tmp_path, out)


def test_without_a_hashes_file_a_coverage_py_record_says_bytes_not_verified(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"a.py": ([2], [])})})
    _, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert "- bytes not verified:" in out
    _, out, _ = go(tmp_path, capsys, "--coverage", str(make_golden(tmp_path)), paths=("scripts/*.py",))
    assert "bytes not verified" not in out


# ---------------------------------------------------------------- K11 unparsable files

@pytest.mark.parametrize("name,content,error", [
    ("syntax.py", "def f(:\n", "SyntaxError"),
    ("nul.py", b"x = 1\x00\n", "(SyntaxError|ValueError)"),
    ("encoding.py", b"# coding: nonexistent-codec\nx = 1\n", "SyntaxError"),
], ids=["syntax", "null-byte", "unknown-encoding"])
def test_an_unparsable_file_is_listed_skipped_and_the_run_completes(tmp_path, capsys, name, content, error):
    put(tmp_path, {name: content, "ok.py": "def f(x):\n    return x\n"})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and "## Unreadable files" in out and re.search(rf"- `{name}`: {error}", out)
    assert head_line(out, "files read") == "1" and head_line(out, "files unreadable") == "1"
    assert "| ok.py:1 | f |" in out


def test_a_very_long_expression_chain_does_not_abort_the_run(tmp_path, capsys):
    put(tmp_path, {"deep.py": "def f(x):\n    return x" + " + x" * 30000 + "\n", "ok.py": "def g(x):\n    return x\n"})
    rc, rep, _ = gj(tmp_path, capsys)
    assert rc == 0 and rep["totals"]["files_read"] + rep["totals"]["files_unreadable"] == 2
    assert row(rep, "g")["complexity"] == 1


def test_an_empty_set_is_a_report(tmp_path, capsys):
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and head_line(out, "functions") == "0" and "No functions found" in out


# ---------------------------------------------------------------- K12 flags, determinism, output form

def fixture_tree(tmp_path):
    for i in range(4):
        text, _ = branchy(f"f{i}", i + 1)
        put(tmp_path, {f"m{i}.py": text})
    return tmp_path


def test_top_limits_the_print_only_and_prints_every_row_at_and_beyond_the_count(tmp_path, capsys):
    fixture_tree(tmp_path)
    _, rep, _ = gj(tmp_path, capsys, "--top", "2")
    assert (len(rep["rows"]), rep["totals"]["functions"], rep["totals"]["shown"]) == (2, 4, 2)
    assert [r["function"] for r in rep["rows"]] == ["f3", "f2"]
    for top in ("4", "5", "9999999999999999999"):
        _, rep, _ = gj(tmp_path, capsys, "--top", top)
        assert len(rep["rows"]) == 4


@pytest.mark.parametrize("flags", [["--top", "0"], ["--top", "-3"], ["--top", "x"], ["--nonsense"],
                                   ["--repo", "NOPE"], ["--paths", "/definitely/outside/*.py"]],
                         ids=["top0", "top-negative", "top-not-a-number", "unknown-option", "repo-not-a-dir",
                              "absolute-glob-outside"])
def test_a_usage_error_exits_2_and_says_so(tmp_path, capsys, flags):
    flags = [str(tmp_path / "missing-dir") if f == "NOPE" else f for f in flags]
    rc = CR.run(["--repo", str(tmp_path), *flags])             # a later --repo overrides the first
    cap = capsys.readouterr()
    assert rc == 2 and not cap.out


def test_help_exits_0(capsys):
    assert CR.run(["--help"]) == 0
    assert "--require-coverage" in capsys.readouterr().out


def test_json_carries_the_same_rows_as_the_markdown(tmp_path, capsys):
    three_functions(tmp_path, covered=("b",))
    flags = ["--coverage", str(tmp_path / "cov.json")]
    _, out, _ = go(tmp_path, capsys, *flags)
    _, rep, _ = gj(tmp_path, capsys, *flags)
    md = re.findall(r"^\| (\d+) \| (\S+):(\d+) \| (\S+) \| (\d+) \| (\S+) \| (\S+) \|$", out, re.M)
    assert md == [(str(r["rank"]), r["path"], str(r["line"]), r["function"], str(r["complexity"]),
                   "none" if r["coverage"] is None else f"{100 * r['coverage']:.1f}%",
                   ("<=" if r["crap_is_bound"] else "") + f"{r['crap']:.1f}") for r in rep["rows"]]
    assert all(len(str(r["crap"]).split(".")[-1]) <= 4 for r in rep["rows"])


def test_ranking_is_crap_then_complexity_then_path_then_line(tmp_path, capsys):
    # c=2 uncovered: 6.0.  c=3 covered fully: 3.0.  c=1 uncovered twice in one file: 2.0 and 2.0 (line order).
    # c=2 covered fully in a LATER file: also 2.0, and it wins the tie on complexity, not on path
    a, la = branchy("a2", 2)
    b, lb = branchy("b3", 3)
    c1, lc = branchy("c1", 1, first=1)
    c2, ld = branchy("c1b", 1, first=3)
    z, lz = branchy("z2", 2)
    put(tmp_path, {"a.py": a, "b.py": b, "c.py": c1 + c2, "z.py": z, "cov.json": hand_cov({
        "a.py": ([], la), "b.py": (lb, []), "c.py": ([], lc + ld), "z.py": (lz, [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"))
    assert [r["function"] for r in rep["rows"]] == ["a2", "b3", "z2", "c1", "c1b"]
    assert [r["crap"] for r in rep["rows"]] == [6.0, 3.0, 2.0, 2.0, 2.0]


def test_output_is_ascii_relative_and_pipe_safe(tmp_path, capsys):
    put(tmp_path, {"sub/caf\u00e9.py": "def f(x):\n    return x\n", "cov.json": hand_cov({})})
    _, out, _ = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), paths=("sub/*.py",))
    assert out.isascii() and no_path(tmp_path, out) and "caf\\xe9.py" in out
    assert CR.cell("a|b") == "a\\|b"


def test_a_source_outside_the_repo_is_printed_as_its_basename(tmp_path, capsys):
    repo = tmp_path / "repo"
    put(repo, {"a.py": "def f(x):\n    return x\n"})
    put(tmp_path, {"outside.json": hand_cov({"a.py": ([2], [])})})
    _, out, _ = go(repo, capsys, "--coverage", str(tmp_path / "outside.json"))
    assert head_line(out, "coverage source") == "`outside.json` (coverage.py)" and no_path(tmp_path, out)


def test_two_runs_are_byte_identical_also_under_another_hash_seed(tmp_path):
    three_functions(tmp_path, covered=("b",))
    outs = []
    for seed in ("1", "2"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        done = subprocess.run([sys.executable, "-B", str(SCRIPT), "--repo", str(tmp_path), "--paths", "*.py",
                               "--coverage", str(tmp_path / "cov.json")], capture_output=True, env=env)
        assert done.returncode == 0, done.stderr
        outs.append(done.stdout)
    assert outs[0] == outs[1] and outs[0].count(b"\r") == 0


def test_measured_only_leaves_the_unmeasured_rows_out_of_the_table_but_not_out_of_the_head(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "b.py": "def g(x):\n    return x\n",
                   "cov.json": hand_cov({"a.py": ([2], [])})})
    _, rep, _ = gj(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), "--measured-only")
    assert [r["function"] for r in rep["rows"]] == ["f"] and rep["totals"]["unmeasured"] == 1


# ---------------------------------------------------------------- K13 sizes (no timing assertion: FR-31)

def test_a_ten_thousand_line_file_completes(tmp_path, capsys):
    put(tmp_path, {"big.py": "def f(x):\n    return x\n" * 5000})
    rc, rep, _ = gj(tmp_path, capsys, "--top", "3")
    assert rc == 0 and rep["totals"]["functions"] == 5000 and len(rep["rows"]) == 3


def test_a_thousand_files_complete(tmp_path, capsys):
    put(tmp_path, {f"d{i % 10}/m{i}.py": "def f(x):\n    return x\n" for i in range(1000)})
    put(tmp_path, {"cov.json": hand_cov({f"d{i % 10}/m{i}.py": ([2], []) for i in range(1000)})})
    rc, rep, _ = gj(tmp_path, capsys, "--top", "3", "--coverage", str(tmp_path / "cov.json"), paths=("d*/*.py",))
    assert rc == 0 and rep["totals"]["files_read"] == 1000 and rep["coverage"]["counts"]["matched"] == 1000


# ---------------------------------------------------------------- K14 names

def test_qualnames_are_dotted_and_duplicates_are_separate_rows_told_apart_by_line(tmp_path, capsys):
    put(tmp_path, {"a.py": ("class K:\n"
                            "    @property\n    def v(self):\n        return 1\n"
                            "    @v.setter\n    def v(self, value):\n        pass\n"
                            "    async def run(self):\n        def helper():\n            return 2\n"
                            "        return helper\n"
                            "if True:\n    def twice():\n        return 1\nelse:\n    def twice():\n        return 2\n"
                            "g = lambda x: 1 if x else 2\n")})
    _, rep, _ = gj(tmp_path, capsys)
    assert sorted((r["function"], r["line"]) for r in rep["rows"]) == [
        ("K.run", 8), ("K.run.helper", 9), ("K.v", 3), ("K.v", 6), ("twice", 13), ("twice", 16)]


# ---------------------------------------------------------------- K15 --require-coverage

def test_require_coverage_turns_a_missing_capture_into_exit_1_and_nothing_else(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"a.py": ([2], [])}),
                   "other.json": hand_cov({"zzz.py": ([1], [])})})
    assert go(tmp_path, capsys, "--require-coverage")[0] == 1                                        # no source
    assert go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), "--require-coverage")[0] == 0
    assert go(tmp_path, capsys, "--coverage", str(tmp_path / "other.json"), "--require-coverage")[0] == 1
    assert go(tmp_path, capsys, "--coverage", str(tmp_path / "other.json"))[0] == 0                  # not asked
    assert go(tmp_path, capsys, "--require-coverage", paths=("nothing/*.py",))[0] == 1               # 0 files


def test_require_coverage_is_also_exit_1_when_every_entry_is_refused(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    return x\n", "cov.json": hand_cov({"a.py": ([99], [])})})
    rc, _, err = go(tmp_path, capsys, "--coverage", str(tmp_path / "cov.json"), "--require-coverage")
    assert rc == 1 and "no file of the scope was measured" in err


# ---------------------------------------------------------------- reuse of dup_report's reader (B3)

def test_the_file_set_reader_is_dup_reports_not_a_copy():
    for name in ("normalise_patterns", "resolve_files", "UsageError", "describe_error", "RECURSION_LIMIT",
                 "physical_lines", "DEFAULT_PATHS", "REPO"):
        assert getattr(CR, name) is getattr(DR, name), name


# K16 (the CI job `crap-measure` pinned by reading the yaml) lives in tools/test_ci_layout.py since GM1-5: that file is
# the one place that judges the jobs of .gitlab-ci.yml.


# ---------------------------------------------------------------- B-449: the stream setup is tools/streams.py

def test_c1_main_sets_up_the_streams_with_lf_newlines(tmp_path, monkeypatch):
    put(tmp_path, {"a.py": "x = 1\n"})
    calls = []
    monkeypatch.setattr(CR.streams, "utf8_stdio", lambda **kw: calls.append(kw))
    assert CR.main(["--repo", str(tmp_path), "--paths", "*.py"]) == 0
    assert calls == [{"newline": "\n"}]


# ---------------------------------------------------------------- t-667 D1: the opt-in `--lines` / `--depth` columns
# The expected numbers below are counted by hand from the fixture text (the code under test is not their source):
# `lines` is the function's own lines (first body line to the last, nested def bodies out) minus its docstring,
# `depth` the deepest nesting of if / for / while / try / with / match (t-625's M rule).

def measures(tmp_path, capsys, source, name="f"):
    """-> (lines, depth) of the function `name` in `source`, read from the JSON of a run with both flags on."""
    put(tmp_path, {"a.py": source})
    rc, rep, _ = gj(tmp_path, capsys, "--lines", "--depth")
    assert rc == 0
    r = row(rep, name)
    return r["lines"], r["depth"]


def with_docstring(n_body_lines):
    """A function with a 3-line docstring and `n_body_lines` plain statements."""
    return 'def f(x):\n    """first\n    second\n    third"""\n' + "    x += 1\n" * n_body_lines


@pytest.mark.parametrize("n", [59, 60, 61, 62], ids=["below-60", "at-60", "beyond-61", "62"])
def test_d1_lines_at_60_and_beyond_with_a_three_line_docstring(tmp_path, capsys, n):
    # the docstring (3 lines) is not counted: 60 statements are 60 lines, 61 are 61 -- the 60/61 edge of S6
    assert measures(tmp_path, capsys, with_docstring(n)) == (n, 0)


@pytest.mark.parametrize("n", [2, 3, 4, 5], ids=["2", "AT-3", "BEYOND-4", "5"])
def test_d1_depth_at_3_and_beyond_4(tmp_path, capsys, n):
    body = "".join("    " * (i + 1) + "if x:\n" for i in range(n)) + "    " * (n + 1) + "pass\n"
    assert measures(tmp_path, capsys, "def f(x):\n" + body) == (n + 1, n)


def test_d1_an_elif_chain_of_five_is_depth_1(tmp_path, capsys):
    chain = "def f(x):\n    if x == 0:\n        pass\n" + "".join(
        f"    elif x == {i}:\n        pass\n" for i in range(1, 5)) + "    else:\n        pass\n"
    assert measures(tmp_path, capsys, chain) == (12, 1)               # if + four elifs + else, a `pass` under each
    assert measures(tmp_path, capsys, chain.replace("elif x == 4", "elif x == 4 and x")) == (12, 1)
    # an `if` inside an elif body is one level below the chain's level
    nested = "def f(x):\n    if x:\n        pass\n    elif x > 1:\n        if x > 2:\n            pass\n"
    assert measures(tmp_path, capsys, nested) == (5, 2)


def test_d1_a_long_elif_chain_is_walked_without_recursion(tmp_path, capsys):
    chain = "def f(x):\n    if x == 0:\n        pass\n" + "".join(
        f"    elif x == {i}:\n        pass\n" for i in range(1, 300))
    assert measures(tmp_path, capsys, chain) == (600, 1)


LEVEL_CASES = {
    "if": ("def f(x):\n    if x:\n        pass\n", 1),
    "for": ("def f(x):\n    for i in x:\n        pass\n", 1),
    "async-for": ("async def f(x):\n    async for i in x:\n        pass\n", 1),
    "while": ("def f(x):\n    while x:\n        pass\n", 1),
    "with": ("def f(x):\n    with x:\n        pass\n", 1),
    "async-with": ("async def f(x):\n    async with x:\n        pass\n", 1),
    "try-except-else-finally": ("def f(x):\n    try:\n        pass\n    except KeyError:\n        pass\n"
                                "    else:\n        pass\n    finally:\n        pass\n", 1),
    "match-case": ("def f(x):\n    match x:\n        case 1:\n            pass\n        case 2:\n            pass\n", 1),
    "match-case-body-adds-none": ("def f(x):\n    match x:\n        case 1:\n            y = 1\n            z = 2\n"
                                  "        case _:\n            y = 3\n", 1),
    "if-in-a-case-body": ("def f(x):\n    match x:\n        case 1:\n            if x:\n                pass\n", 2),
    "if-in-an-except-body": ("def f(x):\n    try:\n        pass\n    except KeyError:\n        if x:\n"
                             "            pass\n", 2),
    "with-try-match-nested": ("def f(x):\n    with x:\n        try:\n            match x:\n                case 1:\n"
                              "                    pass\n        finally:\n            pass\n", 3),
    "no-statement-level": ("def f(x):\n    y = [i for i in x if i]\n    return 1 if y else 2\n", 0),
    "lambda-body-is-not-entered": ("def f(x):\n    return lambda y: [i for i in y if i]\n", 0),
}


@pytest.mark.parametrize("source,want", list(LEVEL_CASES.values()), ids=list(LEVEL_CASES))
def test_d1_each_statement_kind_adds_one_level_and_a_case_body_none(tmp_path, capsys, source, want):
    assert measures(tmp_path, capsys, source)[1] == want


@pytest.mark.skipif(sys.version_info < (3, 11), reason="`except*` needs 3.11")
def test_d1_try_star_adds_one_level(tmp_path, capsys):
    assert measures(tmp_path, capsys, "def f(x):\n    try:\n        pass\n    except* KeyError:\n        pass\n")[1] == 1


def test_d1_a_nested_def_keeps_the_parents_depth_and_counts_from_zero_in_its_own_row(tmp_path, capsys):
    src = ("def outer(x):\n"                  # 1
           "    if x:\n"                      # 2   level 1 in outer
           "        def inner(y):\n"          # 3
           "            if y:\n"              # 4   level 1 in inner
           "                if y:\n"          # 5   level 2 in inner
           "                    return 1\n"   # 6
           "        return inner\n"           # 7
           "    return None\n")               # 8
    put(tmp_path, {"a.py": src})
    _, rep, _ = gj(tmp_path, capsys, "--lines", "--depth")
    outer, inner = row(rep, "outer"), row(rep, "outer.inner")
    assert (outer["depth"], inner["depth"]) == (1, 2)
    assert outer["lines"] == 4 and inner["lines"] == 3         # outer: lines 2, 3 (the nested def line), 7, 8; not 4-6
    # the same def at the top of the outer function: the outer depth is its own statements only
    assert measures(tmp_path, capsys, "def f(x):\n    def g(y):\n        if y:\n            if y:\n                pass\n"
                                      "    return g\n")[1] == 0


def test_d1_a_nested_class_body_counts_toward_lines_and_not_toward_depth(tmp_path, capsys):
    src = ("def f(x):\n"                      # 1
           "    class K:\n"                   # 2
           "        if x:\n"                  # 3
           "            y = 1\n"              # 4
           "        def m(self):\n"           # 5
           "            if x:\n"              # 6
           "                return 1\n"       # 7
           "    return K\n")                  # 8
    put(tmp_path, {"a.py": src})
    _, rep, _ = gj(tmp_path, capsys, "--lines", "--depth")
    assert (row(rep, "f")["lines"], row(rep, "f")["depth"]) == (5, 0)     # 2, 3, 4, 5 (the method's def line), 8
    assert (row(rep, "f.K.m")["lines"], row(rep, "f.K.m")["depth"]) == (2, 1)
    # at module level a method is a plain row
    put(tmp_path, {"b.py":"class K:\n    def m(self, x):\n        for i in x:\n            pass\n"})
    _, rep, _ = gj(tmp_path, capsys, "--lines", "--depth", paths=("b.py",))
    assert (row(rep, "K.m")["lines"], row(rep, "K.m")["depth"]) == (2, 1)


@pytest.mark.parametrize("source,want", [
    ("def f(): return 1\n", (0, 0)),
    ("@deco\ndef f(): return 1\n", (0, 0)),
    ("def f(): 'doc'\n", (0, 0)),
    ("def f():\n    \"\"\"only a docstring\"\"\"\n", (0, 0)),
    ("def f():\n    \"\"\"a\n    docstring\n    of three\n    lines\"\"\"\n", (0, 0)),
    ("def f():\n    \"\"\"one\"\"\"\n    return 1\n", (1, 0)),
    ("def f():\n    x = 1\n    \"\"\"not a docstring: it is not first\"\"\"\n", (2, 0)),
    ("def f(a,\n      b):\n    return a\n", (1, 0)),
    ("@deco\ndef f(a,\n      b):\n    '''doc'''\n    return a\n", (1, 0)),
], ids=["one-liner", "decorated-one-liner", "one-line-docstring-on-the-def-line", "docstring-only",
        "multi-line-docstring-only", "docstring-then-a-line", "late-string-is-code", "multi-line-signature",
        "decorated-multi-line-signature-and-docstring"])
def test_d1_the_edges_of_lines(tmp_path, capsys, source, want):
    assert measures(tmp_path, capsys, source) == want


def test_d1_lines_comes_from_the_one_counter_and_is_never_negative(tmp_path, capsys, monkeypatch):
    # one counter (I-one-counter): `lines` is len(Unit.lines()) less the docstring, not a second span walk
    put(tmp_path, {"a.py": with_docstring(4)})
    seen = []
    real = CR.Unit.lines
    monkeypatch.setattr(CR.Unit, "lines", lambda self: seen.append(self.name) or real(self))
    _, rep, _ = gj(tmp_path, capsys, "--lines")
    assert row(rep, "f")["lines"] == 4 and seen == ["f"]
    monkeypatch.undo()
    units = CR.collect_units("a.py", ast.parse("def f(x):\n    '''d'''\n"))
    assert units[0].code_lines() == 0 and units[0].lines() == {2}


def test_d1_the_keys_exist_only_with_the_flags(tmp_path, capsys):
    put(tmp_path, {"a.py": "def f(x):\n    if x:\n        return 1\n    return 2\n"})
    base_keys = {"path", "line", "function", "complexity", "coverage", "crap", "crap_is_bound", "rank"}
    for flags, extra in (([], set()), (["--lines"], {"lines"}), (["--depth"], {"depth"}),
                         (["--depth", "--lines"], {"lines", "depth"})):
        _, rep, _ = gj(tmp_path, capsys, *flags)
        assert set(rep["rows"][0]) == base_keys | extra, flags
        assert set(rep["options"]) == {"paths", "top", "measured_only"} | extra, flags
        assert all(rep["options"][k] is True for k in extra)
    _, rep, _ = gj(tmp_path, capsys, "--depth", "--lines")
    assert list(rep["rows"][0]) == ["path", "line", "function", "complexity", "lines", "depth",
                                    "coverage", "crap", "crap_is_bound", "rank"]


def small_fixture(tmp_path):
    """a.py: f (complexity 2, 3 own lines, depth 1, coverage 2 of 3 lines); b.py: g (a 2-line docstring and one
    statement, so 1 line, depth 0), unmeasured."""
    put(tmp_path, {"a.py": "def f(x):\n    if x:\n        return 1\n    return 2\n",
                   "b.py": 'def g(x):\n    """doc\n    more"""\n    return x\n',
                   "cov.json": hand_cov({"a.py": ([2, 3], [4])})})
    return ("--coverage", str(tmp_path / "cov.json"))


GOLDEN_SMALL_JSON = """{
  "options": {
    "paths": [
      "*.py"
    ],
    "top": 40,
    "measured_only": false
  },
  "coverage": {
    "source": "cov.json",
    "kind": "coverage.py",
    "error": null,
    "bytes_verified": false,
    "hashes": null,
    "hash_lines_unattributed": 0,
    "entries": 1,
    "counts": {
      "matched": 1,
      "unmatched": 0,
      "ambiguous": 0,
      "refused": 0
    },
    "names": {
      "matched": [
        "a.py"
      ],
      "unmatched": [],
      "ambiguous": [],
      "refused": []
    }
  },
  "totals": {
    "files_read": 2,
    "files_unreadable": 0,
    "files_measured": 1,
    "functions": 2,
    "measured": 1,
    "unmeasured": 1,
    "shown": 2
  },
  "unreadable": [],
  "rows": [
    {
      "path": "a.py",
      "line": 1,
      "function": "f",
      "complexity": 2,
      "coverage": 0.6667,
      "crap": 2.1481,
      "crap_is_bound": false,
      "rank": 1
    },
    {
      "path": "b.py",
      "line": 1,
      "function": "g",
      "complexity": 1,
      "coverage": null,
      "crap": 2.0,
      "crap_is_bound": true,
      "rank": 2
    }
  ]
}
"""                                      # recorded from the code BEFORE t-667 D1 (git 79ea49ee), byte for byte


def test_d1_the_default_json_is_byte_equal_to_the_golden_one(tmp_path, capsys):
    # S11: the CI artifact is the `--json` output (.gitlab-ci.yml:237); `options` carries no new key unless a flag is on
    flags = small_fixture(tmp_path)
    rc, out, _ = go(tmp_path, capsys, "--json", *flags)
    assert rc == 0 and out == GOLDEN_SMALL_JSON


def small_markdown(columns, header, separator, rows):
    head = (f"# CRAP report\n\n- paths: `*.py`\n- formula: {CR.FORMULA}\n" + columns +
            "- coverage source: `cov.json` (coverage.py)\n"
            "- bytes not verified: no --coverage-hashes, a record of other bytes whose lines all fit reads as current\n"
            "- record entries: 1; matched 1; unmatched 0; ambiguous 0; refused 0\n  - matched: `a.py`\n"
            "- functions in files with no usable record are counted at coverage 0: their CRAP is an upper bound "
            "(printed `<=N`)\n- files read: 2\n- files unreadable: 0\n- functions: 2\n- measured: 1\n"
            "- unmeasured: 1\n- shown: 2\n\n")
    return head + header + "\n" + separator + "\n" + rows + "\n\n"


def test_d1_the_markdown_with_and_without_the_flags_is_byte_equal_to_the_golden_ones(tmp_path, capsys):
    flags = small_fixture(tmp_path)
    plain = small_markdown("", "| # | path:line | function | complexity | coverage | CRAP |", "|---|---|---|---|---|---|",
                           "| 1 | a.py:1 | f | 2 | 66.7% | 2.1 |\n| 2 | b.py:1 | g | 1 | none | <=2.0 |")
    both = small_markdown(
        "- lines: the function's own lines (L(f), the CRAP rule) minus its docstring; depth: nested "
        "if/for/while/try/with/match (an elif adds none; nested def, class and lambda bodies are not counted)\n",
        "| # | path:line | function | complexity | lines | depth | coverage | CRAP |", "|---|---|---|---|---|---|---|---|",
        "| 1 | a.py:1 | f | 2 | 3 | 1 | 66.7% | 2.1 |\n| 2 | b.py:1 | g | 1 | 1 | 0 | none | <=2.0 |")
    only_lines = small_markdown(
        "- lines: the function's own lines (L(f), the CRAP rule) minus its docstring\n",
        "| # | path:line | function | complexity | lines | coverage | CRAP |", "|---|---|---|---|---|---|---|",
        "| 1 | a.py:1 | f | 2 | 3 | 66.7% | 2.1 |\n| 2 | b.py:1 | g | 1 | 1 | none | <=2.0 |")
    assert go(tmp_path, capsys, *flags)[1] == plain
    assert go(tmp_path, capsys, "--lines", "--depth", *flags)[1] == both
    assert go(tmp_path, capsys, "--depth", "--lines", *flags)[1] == both            # the order of the flags is free
    assert go(tmp_path, capsys, "--lines", *flags)[1] == only_lines
    assert go(tmp_path, capsys, "--lines", "--depth", "--require-coverage", *flags)[0] == 0


def test_d1_the_flags_change_neither_the_ranking_nor_the_rows_nor_an_exit_code(tmp_path, capsys):
    three_functions(tmp_path, covered=("b",))
    flags = ["--coverage", str(tmp_path / "cov.json")]
    _, plain, _ = gj(tmp_path, capsys, *flags, "--top", "2")
    _, both, _ = gj(tmp_path, capsys, *flags, "--top", "2", "--lines", "--depth")
    def strip(rows):
        return [{k: v for k, v in r.items() if k not in ("lines", "depth")} for r in rows]

    assert strip(both["rows"]) == plain["rows"] and both["totals"] == plain["totals"]
    _, plain, _ = gj(tmp_path, capsys, *flags, "--measured-only")
    _, both, _ = gj(tmp_path, capsys, *flags, "--measured-only", "--lines", "--depth")
    assert strip(both["rows"]) == plain["rows"]
    assert CR.run(["--repo", str(tmp_path), "--top", "0", "--lines"]) == 2
    assert CR.run(["--repo", str(tmp_path / "missing"), "--depth"]) == 2
    capsys.readouterr()


def test_d1_an_unreadable_file_is_listed_as_today_and_has_no_row(tmp_path, capsys):
    put(tmp_path, {"bad.py": "def f(:\n", "ok.py": "def g(x):\n    return x\n"})
    rc, out, _ = go(tmp_path, capsys, "--lines", "--depth")
    assert rc == 0 and "## Unreadable files" in out and "- `bad.py`: SyntaxError" in out
    assert "| 1 | ok.py:1 | g | 1 | 1 | 0 | none | <=2.0 |" in out and "bad.py:" not in out.split("| # |")[1]


def test_d1_help_names_both_flags(capsys):
    assert CR.run(["--help"]) == 0
    out = capsys.readouterr().out
    assert "--lines" in out and "--depth" in out


def test_d1_a_ten_thousand_line_function_and_a_deep_nest_complete_with_both_flags(tmp_path, capsys):
    put(tmp_path, {"big.py": "def f(x):\n" + "    x += 1\n" * 10000,
                   "deep.py": "def g(x):\n    return x" + " + x" * 30000 + "\n"})
    rc, rep, _ = gj(tmp_path, capsys, "--lines", "--depth")
    assert rc == 0 and (row(rep, "f")["lines"], row(rep, "f")["depth"]) == (10000, 0)
    assert rep["totals"]["files_read"] + rep["totals"]["files_unreadable"] == 2
    levels = 90                                              # below the parser's indentation limit of 100
    nest = "def h(x):\n" + "".join("    " * (i + 1) + "if x:\n" for i in range(levels)) + "    " * (levels + 1) + "pass\n"
    assert measures(tmp_path, capsys, nest, name="h")[1] == levels
    put(tmp_path, {"many.py": "def f(x):\n    if x:\n        return x\n    return x\n" * 5000})
    rc, rep, _ = gj(tmp_path, capsys, "--lines", "--depth", "--top", "3", paths=("many.py",))
    assert rc == 0 and rep["totals"]["functions"] == 5000 and rep["rows"][0]["lines"] == 3
