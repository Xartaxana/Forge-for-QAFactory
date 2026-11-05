"""Tests for tools/dup_report.py -- the duplicate-code report (t-420, B-309).

Keys: two functions equal up to variable names form one group; different attribute names do not (and the
same attribute names do); a body under the threshold is not reported, one AT the threshold is; a 6-statement
fragment shared by two otherwise different functions is found, and a longer shared stretch is merged to its
maximal run (one group, not one per window); a repeated block inside one function is a fragment with both
ranges; an unparsable file is listed and the run completes; an empty set is a report; `--strict` splits a
group that differs only in a literal; two runs are byte-identical (also under another hash seed); `--json`
carries the same groups as the markdown; paths are relative with forward slashes; a usage error exits 2.
Plus: operators / keyword names / callee names are kept; windows never span two functions; a function clone
does not also appear as fragments; groups are ordered by statements x copies; `--top` limits the print
only; a long expression chain does not crash; the size limits of the spec (a 10 000-line file, 1 000 files).
Plus (B-417, the clone ratchet's reader): K22 a group's `fingerprint` is stable under a line shift and a file
move, differs between groups, is pinned to a literal (a normalisation change must bump NORMALISATION and
regenerate tools/dup-baseline.json) and never reaches the markdown; `--exclude` drops files and appears in
the options only when given.
Every fixture is written into tmp_path; no test reads the real tree.
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import time

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import dup_report as DR  # noqa: E402
from test_crap_report import no_path  # noqa: E402  (B-449 D1/D2: the one helper, not a second copy)

SCRIPT = TOOLS / "dup_report.py"
LOC = re.compile(r"^- `([^`]+):(\d+)-(\d+)` (.*)$", re.M)
GROUP = re.compile(r"^## (G\d+) (function|fragment): (\d+) statements, (\d+) lines, (\d+) copies$", re.M)


def put(tmp_path, files):
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    return tmp_path


def go(tmp_path, capsys, *flags, paths=("*.py",)):
    rc = DR.run(["--repo", str(tmp_path), "--paths", *paths, *flags])
    cap = capsys.readouterr()
    return rc, cap.out, cap.err


def groups_of(out):
    return GROUP.findall(out)


def head_value(out, label):
    m = re.search(r"^- " + re.escape(label) + r": (.*)$", out, re.M)
    assert m, f"no head line `{label}` in:\n{out}"
    return m.group(1)


FUNC_A = """def first(items, limit):
    total = 0
    for item in items:
        if item.status == "ok":
            total += item.size
    if total > limit:
        return None
    return total
"""
FUNC_B = """def second(rows, cap):
    acc = 0
    for row in rows:
        if row.status == "ok":
            acc += row.size
    if acc > cap:
        return None
    return acc
"""


def test_two_functions_equal_up_to_variable_names_form_one_group(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert [(g[1], g[4]) for g in groups_of(out)] == [("function", "2")]
    assert ("a.py", "1", "8", "first") in LOC.findall(out) and ("b.py", "1", "8", "second") in LOC.findall(out)
    assert head_value(out, "clone groups").startswith("1 (1 function, 0 fragment)")


def test_renaming_must_be_consistent_a_plus_b_is_not_a_plus_a(tmp_path, capsys):
    two = FUNC_A.replace("total += item.size", "total += item.size + limit")
    other = FUNC_B.replace("acc += row.size", "acc += row.size + row")
    put(tmp_path, {"a.py": two, "b.py": other})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and groups_of(out) == []


def test_different_attribute_names_do_not_form_a_group(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B.replace("row.status", "row.verdict")})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and groups_of(out) == [] and "No clone groups found." in out
    # positive twin: the same attribute name groups (test 1) -- and a differing OPERATOR splits too
    put(tmp_path, {"b.py": FUNC_B.replace("acc += row.size", "acc -= row.size")})
    _, out2, _ = go(tmp_path, capsys)
    assert groups_of(out2) == []


def test_different_keyword_argument_names_and_callees_do_not_form_a_group(tmp_path, capsys):
    base = "def {n}(x):\n    a = load(x, mode=1)\n    b = load(a, mode=2)\n    c = merge(a, b, {kw}=3)\n    d = {callee}(c)\n    return d.size\n"
    put(tmp_path, {"a.py": base.format(n="f", kw="strict", callee="finish")})
    put(tmp_path, {"b.py": base.format(n="g", kw="strict", callee="finish")})
    _, out, _ = go(tmp_path, capsys)
    assert [g[1] for g in groups_of(out)] == ["function"]          # the twin: equal -> grouped
    put(tmp_path, {"b.py": base.format(n="g", kw="loose", callee="finish")})
    _, out, _ = go(tmp_path, capsys)
    assert groups_of(out) == []
    put(tmp_path, {"b.py": base.format(n="g", kw="strict", callee="close")})
    _, out, _ = go(tmp_path, capsys)
    assert groups_of(out) == []


def test_a_body_under_the_threshold_is_not_reported(tmp_path, capsys):
    four = "def {n}(x):\n    a = x + 1\n    b = a + 2\n    c = b + 3\n    return c\n"
    five = "def {n}(x):\n    a = x + 1\n    b = a + 2\n    c = b + 3\n    d = c + 4\n    return d\n"
    put(tmp_path, {"a.py": four.format(n="f") + "\n\n" + four.format(n="g")})
    _, out, _ = go(tmp_path, capsys)
    assert groups_of(out) == []                                    # 4 statements: beyond (below) the threshold
    put(tmp_path, {"a.py": five.format(n="f") + "\n\n" + five.format(n="g")})
    _, out, _ = go(tmp_path, capsys)
    assert [(g[1], g[2]) for g in groups_of(out)] == [("function", "5")]   # exactly AT the threshold
    put(tmp_path, {"a.py": four.format(n="f") + "\n\n" + four.format(n="g")})
    _, out, _ = go(tmp_path, capsys, "--min-statements", "4")
    assert [(g[1], g[2]) for g in groups_of(out)] == [("function", "4")]   # the option moves the limit


def test_trivial_identical_bodies_pass_return_property_are_not_reported(tmp_path, capsys):
    src = ("class A:\n    @property\n    def size(self):\n        return self._size\n\n    def noop(self):\n        pass\n\n"
           "class B:\n    @property\n    def size(self):\n        return self._size\n\n    def noop(self):\n        pass\n")
    put(tmp_path, {"a.py": src})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and groups_of(out) == []


SHARED6 = """    a = fetch_alpha(x)
    b = fetch_beta(a)
    c = fetch_gamma(b)
    d = fetch_delta(c)
    e = fetch_epsilon(d)
    f = fetch_zeta(e)
"""
SHARED8 = SHARED6 + """    g = fetch_eta(f)
    h = fetch_theta(g)
"""


def two_functions_sharing(shared, last_var):
    one = "def one(x):\n    x = start_one()\n" + shared + f"    return {last_var}\n"
    two = "def two(x):\n    x = other_start(1, 2)\n" + shared + f"    emit({last_var})\n    log_done()\n"
    return {"a.py": one, "b.py": two}


def test_a_six_statement_fragment_shared_by_two_different_functions_is_found(tmp_path, capsys):
    put(tmp_path, two_functions_sharing(SHARED6, "f"))
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert [(g[1], g[2], g[4]) for g in groups_of(out)] == [("fragment", "6", "2")]
    assert LOC.findall(out) == [("a.py", "3", "8", "one"), ("b.py", "3", "8", "two")]


def test_overlapping_windows_are_merged_to_the_maximal_run(tmp_path, capsys):
    put(tmp_path, two_functions_sharing(SHARED8, "h"))
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert [(g[1], g[2], g[3], g[4]) for g in groups_of(out)] == [("fragment", "8", "8", "2")]   # one group, 8 not 6
    assert LOC.findall(out) == [("a.py", "3", "10", "one"), ("b.py", "3", "10", "two")]
    # the window option moves the minimum: a shared stretch of 6 is not a clone at --window 7
    put(tmp_path, two_functions_sharing(SHARED6, "f"))
    _, out2, _ = go(tmp_path, capsys, "--window", "7")
    assert groups_of(out2) == []


def test_a_repeated_block_inside_one_function_is_a_fragment_with_both_ranges(tmp_path, capsys):
    src = "def solo(x):\n    first_call(x)\n" + SHARED6 + "    middle_call(x)\n" + SHARED6 + "    last_call(x)\n"
    put(tmp_path, {"a.py": src})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert [(g[1], g[2], g[4]) for g in groups_of(out)] == [("fragment", "6", "2")]
    assert LOC.findall(out) == [("a.py", "3", "8", "solo"), ("a.py", "10", "15", "solo")]


def test_a_function_clone_is_not_reported_again_as_fragments(tmp_path, capsys):
    f = "def {n}(x):\n" + SHARED8 + "    return h\n"
    put(tmp_path, {"a.py": f.format(n="f"), "b.py": f.format(n="g")})
    _, out, _ = go(tmp_path, capsys)
    assert [(g[1], g[2]) for g in groups_of(out)] == [("function", "9")]
    assert head_value(out, "groups dropped as lying inside a larger function clone") == "1"


def test_windows_never_span_two_functions(tmp_path, capsys):
    six = ["call_a(1)", "call_b(1)", "call_c(1)", "call_d(1)", "call_e(1)", "call_f(1)"]
    split = "def f():\n" + "".join(f"    {s}\n" for s in six[:3]) + "\n\ndef g():\n" + "".join(f"    {s}\n" for s in six[3:])
    flat = "".join(f"{s}\n" for s in six)
    put(tmp_path, {"split.py": split, "flat.py": flat})
    _, out, _ = go(tmp_path, capsys)
    assert groups_of(out) == []                                    # the def breaks the stretch
    one_function = "def h():\n" + "".join(f"    {s}\n" for s in six)
    put(tmp_path, {"split.py": one_function})
    _, out, _ = go(tmp_path, capsys)
    assert [(g[1], g[2]) for g in groups_of(out)] == [("fragment", "6")]   # the twin: one list -> found


IMPORTS = ("import os\nimport sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).parent))\n"
           "from json import dumps\nimport re\n")                     # 6 statements: four imports kinds + the bootstrap line
REAL6 = "".join(line[4:] + "\n" for line in SHARED6.splitlines())    # SHARED6 at module level


def test_an_import_only_block_is_not_reported_by_default_and_is_with_imports(tmp_path, capsys):
    put(tmp_path, {"a.py": IMPORTS + "run_a(1)\n", "b.py": IMPORTS + "run_b(2)\nrun_c(3)\n"})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and groups_of(out) == [] and "No clone groups found." in out
    rc, out, _ = go(tmp_path, capsys, "--with-imports")                 # the twin: the flag restores the old behaviour
    assert rc == 0
    assert [(g[1], g[2], g[4]) for g in groups_of(out)] == [("fragment", "6", "2")]
    assert LOC.findall(out) == [("a.py", "1", "6", "<module>"), ("b.py", "1", "6", "<module>")]


def test_each_kind_of_import_statement_alone_breaks_a_window(tmp_path, capsys):
    kinds = ["import os", "from os import path", "sys.path.insert(0, '.')", "sys.path.append('.')"]
    for kind in kinds:
        body = "".join(f"call_{i}(1)\n" for i in range(5))
        put(tmp_path, {"a.py": body + kind + "\ncall_6(1)\n", "b.py": body + kind + "\ncall_6(1)\n"})
        _, out, _ = go(tmp_path, capsys)
        assert groups_of(out) == [], kind                               # the five calls are too few, the sixth is cut off
        _, out, _ = go(tmp_path, capsys, "--with-imports")
        assert [(g[1], g[2]) for g in groups_of(out)] == [("fragment", "7")], kind
    # a sys.path call that is not the bootstrap is an ordinary statement
    other = "".join(f"call_{i}(1)\n" for i in range(3)) + "paths.insert(0, 1)\nitems.append(2)\ncall_9(1)\n"
    put(tmp_path, {"a.py": other, "b.py": other})
    _, out, _ = go(tmp_path, capsys)
    assert [(g[1], g[2]) for g in groups_of(out)] == [("fragment", "6")]


def test_a_real_fragment_next_to_imports_is_still_found(tmp_path, capsys):
    put(tmp_path, {"a.py": IMPORTS + REAL6 + "end_one()\n", "b.py": IMPORTS + "mid_two()\n" + REAL6})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert [(g[1], g[2], g[4]) for g in groups_of(out)] == [("fragment", "6", "2")]
    assert LOC.findall(out) == [("a.py", "7", "12", "<module>"), ("b.py", "8", "13", "<module>")]   # the imports are out
    _, out2, _ = go(tmp_path, capsys, "--with-imports")
    assert sorted((g[1], g[2]) for g in groups_of(out2)) == [("fragment", "6"), ("fragment", "6")]   # the flag: the imports are a group of their own too


def test_the_options_line_names_the_imports_setting(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A})
    _, out, _ = go(tmp_path, capsys)
    assert head_value(out, "options") == "min-statements 5, window 6, strict no, imports excluded, top 40"
    _, out, _ = go(tmp_path, capsys, "--with-imports")
    assert head_value(out, "options") == "min-statements 5, window 6, strict no, imports included, top 40"
    _, js, _ = go(tmp_path, capsys, "--json", "--with-imports")
    assert json.loads(js)["options"]["with_imports"] is True


def test_an_unparsable_file_is_listed_and_the_run_completes(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B, "broken.py": "def broken(:\n    pass\n", "bad.py": "x = 1\x00\n"})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert head_value(out, "files unreadable") == "2" and head_value(out, "files read") == "2"
    assert re.search(r"^- `broken.py`: SyntaxError: .* \(line 1\)$", out, re.M)
    assert re.search(r"^- `bad.py`: ", out, re.M)
    assert [g[1] for g in groups_of(out)] == ["function"]          # the readable pair is still compared


def test_an_empty_directory_and_a_clone_free_tree_are_reports(tmp_path, capsys):
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert head_value(out, "files read") == "0" and "No Python files matched the paths" in out
    assert head_value(out, "duplicated lines") == "0 of 0 (0.0%)"
    put(tmp_path, {"a.py": FUNC_A})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0 and "No clone groups found." in out and head_value(out, "files read") == "1"


def test_strict_splits_a_group_that_differs_only_in_a_literal(tmp_path, capsys):
    f = "def {n}(x):\n    limit = {k}\n    name = '{s}'\n    a = check(x, limit)\n    b = send(a, name)\n    return b\n"
    put(tmp_path, {"a.py": f.format(n="f", k=10, s="alpha"), "b.py": f.format(n="g", k=20, s="beta")})
    _, out, _ = go(tmp_path, capsys)
    assert [g[1] for g in groups_of(out)] == ["function"]
    _, strict_out, _ = go(tmp_path, capsys, "--strict")
    assert groups_of(strict_out) == [] and "strict yes" in strict_out
    put(tmp_path, {"b.py": f.format(n="g", k=10, s="alpha")})       # the twin: equal literals stay one group
    _, strict_out, _ = go(tmp_path, capsys, "--strict")
    assert [g[1] for g in groups_of(strict_out)] == ["function"]


def test_docstrings_and_comments_do_not_matter_but_the_literal_type_does(tmp_path, capsys):
    f = 'def {n}(x):\n    """{doc}"""\n    # {doc}\n    a = x + {lit}\n    b = a * 2\n    c = b - 3\n    d = c / 4\n    return d\n'
    put(tmp_path, {"a.py": f.format(n="f", doc="one", lit="1"), "b.py": f.format(n="g", doc="another one", lit="9")})
    _, out, _ = go(tmp_path, capsys)
    assert [g[1] for g in groups_of(out)] == ["function"]
    put(tmp_path, {"b.py": f.format(n="g", doc="x", lit="'text'")})
    _, out, _ = go(tmp_path, capsys)
    assert groups_of(out) == []                                    # an int is not a str


def test_output_is_byte_identical_on_two_runs_and_under_another_hash_seed(tmp_path):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B, "sub/c.py": FUNC_A.replace("first", "third")})
    put(tmp_path, two_functions_sharing(SHARED8, "h") | {"sub/d.py": "def one(x):\n    x = start_one()\n" + SHARED8})

    def once(seed):
        env = dict(os.environ, PYTHONHASHSEED=str(seed))
        r = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(tmp_path), "--paths", "*.py", "sub/*.py"],
                           capture_output=True, env=env)
        assert r.returncode == 0, r.stderr
        return r.stdout

    first, second, third = once(1), once(1), once(12345)
    assert first == second == third and b"## G1" in first
    assert b"\r" not in first and str(tmp_path).encode() not in first


def test_json_carries_the_same_groups_as_the_markdown(tmp_path, capsys):
    put(tmp_path, {"c.py": FUNC_A, "d.py": FUNC_B} | two_functions_sharing(SHARED8, "h"))
    _, md, _ = go(tmp_path, capsys)
    rc, js, _ = go(tmp_path, capsys, "--json")
    assert rc == 0
    doc = json.loads(js)
    from_md = [(g[0], g[1], int(g[2]), int(g[3]), int(g[4])) for g in groups_of(md)]
    from_json = [(g["id"], g["kind"], g["statements"], g["lines"], g["copies"]) for g in doc["groups"]]
    assert from_md == from_json and len(from_json) == 2
    locs_md = [(p, int(s), int(e), n) for p, s, e, n in LOC.findall(md)]
    locs_json = [(loc["path"], loc["first"], loc["last"], loc["in"]) for g in doc["groups"] for loc in g["locations"]]
    assert locs_md == locs_json
    assert doc["totals"]["groups"] == 2 and doc["totals"]["files_read"] == 4
    assert doc["options"] == {"paths": ["*.py"], "min_statements": 5, "window": 6, "strict": False, "top": 40}


FINGERPRINT_FUNC_A = "b8b786321c5ff1dc234da1141d025d34a6534d4b"       # FUNC_A / FUNC_B, normalisation 1
FINGERPRINT_SHARED6 = "d086d7320ea298cc86f034c2334ca980802b78d9"       # the SHARED6 fragment, normalisation 1
BUMP = "normalisation changed: bump NORMALISATION and regenerate tools/dup-baseline.json in the same commit"


def groups_json(tmp_path, capsys, *flags, paths=("*.py",)):
    rc, js, _ = go(tmp_path, capsys, "--json", *flags, paths=paths)
    assert rc == 0
    return json.loads(js)


def test_k22_a_fingerprint_is_stable_under_a_line_shift_and_a_file_move_and_differs_between_groups(tmp_path, capsys):
    shared = {"s/" + name: text for name, text in two_functions_sharing(SHARED6, "f").items()}
    put(tmp_path, {"f1.py": FUNC_A, "f2.py": FUNC_B} | shared)
    paths = ("*.py", "s/*.py", "zz/*.py")
    first = groups_json(tmp_path, capsys, paths=paths)["groups"]
    before = {g["kind"]: g["fingerprint"] for g in first}
    assert len(before) == 2 and len(set(before.values())) == 2          # a function group and a fragment group differ
    put(tmp_path, {"f2.py": "import os\nVALUE = 1\n\n\n" + FUNC_B})       # a line shift
    (tmp_path / "zz").mkdir()
    for moved in ("f1.py", "s/a.py"):                                    # a file move: each group's FIRST member goes to the end
        (tmp_path / moved).rename(tmp_path / "zz" / moved.replace("/", "_"))
    second = groups_json(tmp_path, capsys, paths=paths)["groups"]
    assert [[loc["path"] for loc in g["locations"]] for g in first] != [[loc["path"] for loc in g["locations"]] for g in second]
    assert {g["kind"]: g["fingerprint"] for g in second} == before


def test_k22_the_fingerprint_of_the_func_a_pair_is_pinned_so_a_normalisation_change_is_loud(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B})
    pinned = {g["fingerprint"] for g in groups_json(tmp_path, capsys)["groups"]}
    assert pinned == {FINGERPRINT_FUNC_A}, BUMP
    put(tmp_path, two_functions_sharing(SHARED6, "f"))
    assert {g["fingerprint"] for g in groups_json(tmp_path, capsys)["groups"]} == {FINGERPRINT_SHARED6}, BUMP
    assert groups_json(tmp_path, capsys)["fingerprint_basis"] == {"normalisation": DR.NORMALISATION}


def test_k22_the_markdown_does_not_carry_the_fingerprint(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A, "b.py": FUNC_B})
    _, md, _ = go(tmp_path, capsys)
    assert FINGERPRINT_FUNC_A not in md and "fingerprint" not in md and md.startswith("# Duplicate code report\n")
    assert [g[0] for g in groups_of(md)] == ["G1"] and head_value(md, "options") == "min-statements 5, window 6, strict no, imports excluded, top 40"


def test_exclude_drops_matching_files_and_is_written_to_the_options_only_when_given(tmp_path, capsys):
    put(tmp_path, {"t/test_a.py": FUNC_A, "t/real.py": FUNC_B, "t/other.py": FUNC_A})
    default = groups_json(tmp_path, capsys, paths=("t/*.py",))
    assert default["totals"]["files_read"] == 3 and "exclude" not in default["options"]
    rep = groups_json(tmp_path, capsys, "--exclude", "t/test_*.py", paths=("t/*.py",))
    assert rep["totals"]["files_read"] == 2 and rep["options"]["exclude"] == ["t/test_*.py"]
    assert [loc["path"] for g in rep["groups"] for loc in g["locations"]] == ["t/other.py", "t/real.py"]
    both = groups_json(tmp_path, capsys, "--exclude", "t/test_*.py", "t/real.py", paths=("t/*.py",))
    assert both["totals"]["files_read"] == 1 and both["groups"] == []
    rc, _, err = go(tmp_path, capsys, "--exclude", str(tmp_path.parent / "x" / "*.py"), paths=("t/*.py",))
    assert rc == 2 and "outside --repo" in err


def test_the_markdown_names_the_exclusion_only_when_there_is_one(tmp_path, capsys):
    put(tmp_path, {"t/test_a.py": FUNC_A, "t/real.py": FUNC_B, "t/other.py": FUNC_A})
    _, plain, _ = go(tmp_path, capsys, paths=("t/*.py",))
    assert "- exclude:" not in plain and head_value(plain, "files read") == "3"        # the default output is unchanged
    assert plain.splitlines()[:4] == ["# Duplicate code report", "", "- paths: `t/*.py`",       # byte for byte: options follows paths
                                      "- options: min-statements 5, window 6, strict no, imports excluded, top 40"]
    _, md, _ = go(tmp_path, capsys, "--exclude", "t/test_*.py", "t/real.py", paths=("t/*.py",))
    assert head_value(md, "exclude") == "`t/test_*.py`, `t/real.py`" and head_value(md, "paths") == "`t/*.py`"
    assert md.splitlines()[:4] == ["# Duplicate code report", "", "- paths: `t/*.py`", "- exclude: `t/test_*.py`, `t/real.py`"]
    assert head_value(md, "options") == "min-statements 5, window 6, strict no, imports excluded, top 40"


def test_the_usage_text_and_the_help_keep_the_min_statements_line_aligned(monkeypatch):
    """B-455 / critic t-534 F-6: `--min-statements N` once lost a space and no longer lined up with its neighbours."""
    assert "    --min-statements N   function clones: the smallest body that counts (default 5)\n" in DR.__doc__
    columns = {len(m.group(0)) for m in re.finditer(r"^    --[^\n]*?\s{2,}(?=\S)", DR.__doc__, re.M)}
    assert columns == {25}                                          # every option of the usage block describes itself in one column
    monkeypatch.setenv("COLUMNS", "100")
    help_lines = DR.build_parser().format_help().splitlines()
    assert "  --min-statements N    smallest function body that counts (default 5)" in help_lines


def test_paths_are_relative_with_forward_slashes(tmp_path, capsys):
    put(tmp_path, {"pkg/sub/a.py": FUNC_A, "pkg/other/b.py": FUNC_B})
    rc, out, _ = go(tmp_path, capsys, paths=("pkg/**/*.py",))
    assert rc == 0
    assert [(p, n) for p, _, _, n in LOC.findall(out)] == [("pkg/other/b.py", "second"), ("pkg/sub/a.py", "first")]
    assert "\\" not in out and str(tmp_path) not in out and tmp_path.as_posix() not in out
    # an absolute glob inside the repo is accepted and printed relative; one outside is a usage error
    rc, out, _ = go(tmp_path, capsys, paths=((tmp_path / "pkg" / "sub").as_posix() + "/*.py",))
    assert rc == 0 and head_value(out, "files read") == "1" and tmp_path.as_posix() not in out
    assert head_value(out, "paths") == "`pkg/sub/*.py`"             # the options line is relative too
    rc, _, err = go(tmp_path, capsys, paths=(str(tmp_path.parent / "elsewhere" / "*.py"),))
    assert rc == 2 and "outside --repo" in err


def test_groups_are_ordered_by_statements_times_copies_and_top_limits_the_print_only(tmp_path, capsys):
    small = "def {n}(x):\n    a = x + 1\n    b = a + 2\n    c = b + 3\n    d = c + 4\n    return d\n"
    big = "def {n}(x):\n" + "".join(f"    v{i} = step_{i}(x)\n" for i in range(12)) + "    return v11\n"
    put(tmp_path, {"s.py": small.format(n="s1") + "\n\n" + small.format(n="s2") + "\n\n" + small.format(n="s3"),
                   "b.py": big.format(n="b1") + "\n\n" + big.format(n="b2")})
    _, out, _ = go(tmp_path, capsys)
    assert [(g[0], g[2], g[4]) for g in groups_of(out)] == [("G1", "13", "2"), ("G2", "5", "3")]     # 26 before 15
    _, top1, _ = go(tmp_path, capsys, "--top", "1")
    assert [g[0] for g in groups_of(top1)] == ["G1"]
    assert head_value(top1, "clone groups").endswith("shown 1") and head_value(top1, "clone groups").startswith("2 (")


def test_a_usage_error_exits_2(tmp_path):
    def code(*args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True).returncode

    assert code("--repo", str(tmp_path), "--min-statements", "many") == 2
    assert code("--repo", str(tmp_path), "--no-such-option") == 2
    assert code("--repo", str(tmp_path), "--window", "1") == 2
    assert code("--repo", str(tmp_path), "--top", "0") == 2
    assert code("--repo", str(tmp_path / "missing")) == 2
    assert code("--repo", str(tmp_path)) == 0                      # the twin: a valid call on an empty tree
    assert DR.run(["--repo", str(tmp_path), "--window", "x"]) == 2  # run() returns it too, no SystemExit leaks


def test_wall_time_goes_to_stderr_only(tmp_path, capsys):
    put(tmp_path, {"a.py": FUNC_A})
    rc, out, err = go(tmp_path, capsys)
    assert rc == 0 and re.search(r"files read in \d+\.\d+s", err) and "files read in" not in out


def test_a_very_long_expression_chain_does_not_crash_the_run(tmp_path, capsys):
    chain = " + ".join(["1"] * 4000)
    put(tmp_path, {"a.py": f"def f():\n    x = {chain}\n    return x\n", "b.py": FUNC_A})
    rc, out, _ = go(tmp_path, capsys)
    assert rc == 0
    assert int(head_value(out, "files read")) + int(head_value(out, "files unreadable")) == 2


def test_a_10000_line_file_and_a_1000_file_set_finish_in_time(tmp_path, capsys):
    block = "def f{i}(x):\n    a = x + {i}\n    b = a * 2\n    c = b - 3\n    d = c / 4\n    if d > {i}:\n        return d\n    return a\n\n\n"
    big = "".join(block.format(i=i) for i in range(1000))           # 10 000 lines
    assert big.count("\n") >= 10000
    put(tmp_path, {"big.py": big})
    started = time.monotonic()
    rc, out, _ = go(tmp_path, capsys)
    one_file = time.monotonic() - started
    assert rc == 0 and one_file < 120
    put(tmp_path, {f"many/m{i}.py": block.format(i=i) + FUNC_A.replace("first", f"fn{i}") for i in range(1000)})
    started = time.monotonic()
    rc, out, _ = go(tmp_path, capsys, paths=("many/*.py",))
    many = time.monotonic() - started
    assert rc == 0 and many < 120 and head_value(out, "files read") == "1000"
    print(f"10000-line file: {one_file:.1f}s; 1000 files: {many:.1f}s")


# ---------------------------------------------------------------- B-449: describe_error never prints the path of an OSError

LEAF = "secret_leaf_b449.py"


def os_errors(tmp_path):
    """The OSError shapes of D1, each built with an absolute path (and a second one) that str() would print."""
    abs1, abs2 = str(tmp_path / LEAF), str(tmp_path / "other_dir_b449" / LEAF)
    return [
        PermissionError(13, "Permission denied", abs1),
        FileNotFoundError(2, "No such file or directory", abs1, None, abs2),
        OSError(abs1),
        OSError(None, "Access is denied.", abs1, 5),      # Windows turns it into PermissionError; the type is not pinned
    ]


def test_d1_describe_error_of_an_oserror_names_the_reason_and_never_a_path(tmp_path):
    cases = os_errors(tmp_path)
    expected = ["PermissionError: Permission denied", "FileNotFoundError: No such file or directory",
                "OSError: cannot be read"]
    assert [DR.describe_error(e) for e in cases[:3]] == expected
    for exc in cases:
        text = DR.describe_error(exc)
        assert no_path(tmp_path, text) and LEAF not in text and "other_dir_b449" not in text, text
    assert DR.describe_error(cases[3]).endswith(": Access is denied.")
    assert LEAF in str(cases[0])                                  # control: str(exc) does carry the path


def test_d1_the_reason_is_one_line_and_cut_at_200_characters(tmp_path):
    p = str(tmp_path / LEAF)
    at, beyond = "a" * 200, "a" * 201
    assert DR.describe_error(OSError(5, at, p)) == f"OSError: {at}"
    assert DR.describe_error(OSError(5, beyond, p)) == f"OSError: {at}"
    assert DR.describe_error(OSError(5, "first line\nsecond line", p)) == "OSError: first line"
    assert DR.describe_error(OSError(5, "", p)) == "OSError: cannot be read"


def test_d2_an_unreadable_file_is_listed_with_its_reason_and_no_absolute_path(tmp_path, capsys, monkeypatch):
    put(tmp_path, {"a.py": FUNC_A, "bad.py": FUNC_B})
    original = pathlib.Path.read_bytes

    def refuse(self):
        if self.name == "bad.py":
            raise PermissionError(13, "Permission denied", str(self))
        return original(self)

    monkeypatch.setattr(pathlib.Path, "read_bytes", refuse)
    rc, out, err = go(tmp_path, capsys)
    assert rc == 0 and "- `bad.py`: PermissionError: Permission denied" in out.splitlines()
    assert no_path(tmp_path, out) and no_path(tmp_path, err)
    rc, js, err = go(tmp_path, capsys, "--json")
    assert json.loads(js)["unreadable"] == [{"path": "bad.py", "error": "PermissionError: Permission denied"}]
    assert no_path(tmp_path, js)


def test_d3_main_sets_up_the_streams_with_lf_newlines(tmp_path, monkeypatch):
    put(tmp_path, {"a.py": FUNC_A})
    calls = []
    monkeypatch.setattr(DR.streams, "utf8_stdio", lambda **kw: calls.append(kw))
    assert DR.main(["--repo", str(tmp_path), "--paths", "*.py"]) == 0
    assert calls == [{"newline": "\n"}]
