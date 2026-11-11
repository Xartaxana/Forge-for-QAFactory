"""Tests of tools/language_sites.py (spec t-2065 node N1; TR2-15): every test builds its own tree under tmp_path, with a
synthetic git repository where a mode needs one. No test reads the live package (CI's single whole scan is that).

Mutations the suite is built to kill (named, not run by the builder -- builder-rules 7b):
  M-1 drop the `predicate-call` form (file_keys skips `cand in preds`)  -> test_a_chain_through_er_is_flagged,
      test_a_read_python_shape_is_flagged, test_c6_a_stale_list_is_red_and_predicates_clears_it
  M-2 take line numbers into the key                                    -> test_e1_edit_above_a_site_is_not_an_event
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import language_sites as L  # noqa: E402

PKG = L.PACKAGE_ROOT
SCRIPTS = PKG + "scripts/"
DET = {"assertion_probes": {"csharp": {"suffixes": [".cs"]}, "java": {"suffixes": [".java"]}}}
MARK = {"code_extensions": [".py", ".js", ".cs", ".go", ".kt"]}
SCRIPT_A = 'def f(p):\n    if p.suffix == ".py":\n        return p\n    return None\n'
QUOTE = "ordinary words of the owner, twelve plus"


# ------------------------------------------------------------------------------------------------ helpers
def sh(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t", "-c", "commit.gpgsign=false",
                    *args], check=True, capture_output=True)


def write(repo, rel, text):
    p = pathlib.Path(repo) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8") if isinstance(text, str) else text)


def commit(repo, msg="c"):
    sh(repo, "add", "-A")
    sh(repo, "commit", "-q", "-m", msg)


def head(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def key(script, qual, form, tok):
    return "%s%s|%s|%s|%s" % (SCRIPTS, script, qual, form, tok)


def row(k, count=1, kind="own-code", mech="OWN", since="t-1", **kw):
    d = {"key": k, "count": count, "mechanism": mech, "kind": kind, "since": since}
    if kind != "road" and "reason" not in kw:
        d["reason"] = "the factory reads its own script"
    d.update(kw)
    return d


def doc(rows, predicates=(), roots=(), **extra):
    d = L.new_doc(list(rows), predicates, roots)
    d.update(extra)
    return d


def word(quote=QUOTE, carrier="finding.md", who="owner"):
    return {"who": who, "date": "2026-11-06", "quote": quote, "carrier": carrier}


SCRIPT_A2 = 'def f(p):\n    if p.suffix == ".py":\n        return p\n    if p.suffix == ".py":\n        return p\n    return None\n'
ROW_A = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1")


def mk(tmp_path, scripts=None, baseline=True, rows=None, predicates=(), data=True, extra=None, commit_it=True, git=True,
       **docextra):
    """A package tree under tmp_path/r; `git=False` is for the tests that only read the working tree (no subprocess)."""
    repo = tmp_path / "r"
    repo.mkdir(parents=True)
    if git:
        sh(repo, "init", "-q")
    scripts = {"a.py": SCRIPT_A} if scripts is None else scripts
    for name, text in scripts.items():
        write(repo, SCRIPTS + name, text)
    if data:
        write(repo, PKG + L.DETECTORS_NAME, json.dumps(DET))
        write(repo, PKG + L.MARKERS_NAME, json.dumps(MARK))
    write(repo, "finding.md", "The owner said: " + QUOTE + " -- and nothing else.\n")
    for rel, text in (extra or {}).items():
        write(repo, rel, text)
    if baseline:
        write(repo, L.BASELINE_REL, L.dumps(doc([ROW_A] if rows is None else rows, predicates, **docextra)))
    if commit_it and git:
        commit(repo, "c0")
    return repo


def put(repo, d):
    write(repo, L.BASELINE_REL, L.dumps(d))


@pytest.fixture
def run(capsys):
    def _run(repo, *args):
        capsys.readouterr()
        code = L.main([*args, "--repo", str(repo)])
        o = capsys.readouterr()
        return code, o.out + o.err
    return _run


def toks(extra_suffix=(".go", ".kt", ".cs"), extra_lang=("csharp", "java")):
    d = json.loads(json.dumps(L.DEFAULT_TOKENS))
    d["suffix"] += list(extra_suffix)
    d["language"] += list(extra_lang)
    return L.Tokens(d)


def keys_of(src, files=None, **kw):
    k, p, e = L.scan_texts(files or {"m.py": src}, kw.pop("tokens", None) or toks(), **kw)
    assert not e, e
    return k


# ------------------------------------------------------------------------------------------------ T-A, T-B, T-M
FLAGGED = [
    ("suffix-eq", 'p.suffix == ".py"', "|.py"),
    ("suffix-lower-ne", 'p.suffix.lower() != ".py"', "|.py"),
    ("go", 'p.suffix == ".go"', "|.go"),
    ("endswith-tuple", 'str(x).endswith((".py", ".pyi"))', "|.pyi"),
    ("module-constant", 'PY = ".py"\nname.endswith(PY)', "|.py"),
    ("in-literal", '".py" in name', "|.py"),
    ("slice", 'name[-3:] == ".py"', "|.py"),
    ("splitext-set", 'import os\nos.path.splitext(n)[1] in {".py"}', "|.py"),
    ("fnmatch", 'from fnmatch import fnmatch\nfnmatch(n, "*.py")', "|.py"),
    ("fnmatch-attr-glob-class", 'import fnmatch\nfnmatch.fnmatch(n, "*.py[co]")', "|.py"),
    ("rglob", 'root.rglob("*.py")', "|.py"),
    ("path-match", 'Path(n).match("*.py")', "|.py"),
    ("fstring", 'name == f"{stem}.py"', "|.py"),
    ("concat", 'name.endswith("." + "py")', "|.py"),
    ("re-search", 'import re\nre.search(r"\\.py$", n)', "regex|.py"),
    ("re-compile-import", 'import re\nIMPORT_RE = re.compile(r"^\\s*import\\s+")', "regex|import"),
    ("re-from-import", 'from re import compile as c\nX = c(r"def\\s+x")', "regex|def"),
    ("ast-alias", 'import ast as a\na.parse(s)', "parser|ast.parse"),
    ("ast-from-alias", 'from ast import parse as p\np(s)', "parser|ast.parse"),
    ("tokenize-alias", 'import tokenize as tk\ntk.generate_tokens(r)', "parser|tokenize"),
    ("import-module", 'import importlib\nimportlib.import_module("ast")', "parser|ast.parse"),
    ("dunder-import", '__import__("ast")', "parser|ast.parse"),
    ("getattr", 'import ast\ngetattr(ast, "parse")', "parser|ast.parse"),
    ("pytest-in", '"pytest" in cmd', "|pytest"),
    ("pytest-eq", 'tool == "pytest"', "|pytest"),
    ("jest-eq", 'runner == "jest"', "|jest"),
    ("pytest-ne", 'reporter != "pytest"', "|pytest"),
    ("trx", 'reporter == "trx"', "|trx"),
    ("junit-xml", 'fmt == "junit-xml"', "|junit-xml"),
    ("project-eq", 'repo == "mybooks"', "|mybooks"),
    ("project-in", '"testproject1" in path', "|testproject1"),
    ("exe", 'Path(t).name.lower().removesuffix(".exe") == "pytest"', "|pytest"),
    ("ifexp", 'x = file[:-3] if file.endswith(".py") else file', "name-call|.py"),
    ("listcomp", '[r for r in rels if not r.lower().endswith(".py")]', "name-call|.py"),
    ("match-case", 'match x:\n    case ".py":\n        pass', "compare|.py"),
    ("lang-python", 'lang == "python"', "|python"),
    ("lang-typescript-row", 'row["language"] == "typescript"', "|typescript"),
    ("table-key", 'X = {"pytest": f}', "table-key|pytest"),
    ("method", 'class C:\n    def m(self, n):\n        return n.endswith(".py")', "|C.m|name-call|.py"),
    ("nested-function", 'def o():\n    def i(n):\n        return n == ".py"\n    return i', "|o.i|compare|.py"),
    ("lambda-in-function", 'def o():\n    return lambda n: n == ".py"', "|o|compare|.py"),
    ("module-level", 'if a == ".py":\n    pass', "|<module>|compare|.py"),
]


@pytest.mark.parametrize("src,needle", [pytest.param(s, n, id=i) for i, s, n in FLAGGED])
def test_a_flagged(src, needle):
    ks = keys_of(src)
    assert any(needle in k for k in ks), (needle, sorted(ks))


def test_a_chain_through_er_is_flagged():
    files = {"er.py": 'def h(n):\n    return n == "pytest"\ndef g(n):\n    return h(n)\ndef f(n):\n    return not g(n)\n',
             "k.py": 'import er as ER\nER.f(argv)\n'}
    ks, preds, _ = L.scan_texts(files, toks())
    assert {"er.h", "er.g", "er.f"} <= preds
    assert "k.py|<module>|predicate-call|er.f" in ks


def test_a_is_pytest_through_er_with_true_false_returns():
    files = {"node_ids.py": '_N = ("pytest", "py.test")\ndef is_pytest(name):\n    if name in _N:\n        return True\n    return False\n',
             "ex.py": 'import node_ids\ndef is_pytest_command(argv):\n    return node_ids.is_pytest(argv[0])\n',
             "c.py": 'import ex as ER\nif ER.is_pytest_command(a):\n    pass\n'}
    ks, preds, _ = L.scan_texts(files, toks())
    assert {"node_ids.is_pytest", "ex.is_pytest_command"} <= preds
    assert "c.py|<module>|predicate-call|ex.is_pytest_command" in ks


def test_a_read_python_shape_is_flagged():
    files = {"s5.py": 'import ast\nclass PyFile:\n    def __init__(self, path, text):\n        self.tree = ast.parse(text)\n'
                      'def read_python(path):\n    text = path.read_text()\n    return PyFile(path, text), ""\n',
             "o.py": 'from s5 import read_python\ndef g(p):\n    f, err = read_python(p)\n    return f\n'}
    ks, preds, _ = L.scan_texts(files, toks())
    assert {"s5.PyFile", "s5.read_python"} <= preds
    assert "o.py|g|predicate-call|s5.read_python" in ks and "s5.py|read_python|predicate-call|s5.PyFile" in ks


def test_a_parser_result_through_one_local_name():
    ks, preds, _ = L.scan_texts({"p.py": 'import ast\ndef rd(s):\n    t = ast.parse(s)\n    return t, ""\n',
                                 "q.py": 'from p import rd\nx = rd(1)\n'}, toks())
    assert "p.rd" in preds and "q.py|<module>|predicate-call|p.rd" in ks


def test_a_data_driven_kotlin_and_zig_join_through_the_data_files(tmp_path):
    repo = mk(tmp_path, scripts={"x.py": 'if lang == "kotlin":\n    pass\nif n.endswith(".zig"):\n    pass\n'}, data=False)
    write(repo, PKG + L.DETECTORS_NAME, json.dumps({"assertion_probes": {"kotlin": {"suffixes": [".kt"]}}}))
    write(repo, PKG + L.MARKERS_NAME, json.dumps({"code_extensions": [".py", ".zig"]}))
    t = L.Tokens(L.effective_tokens({"scan": L.DEFAULT_SCAN, "tokens": L.DEFAULT_TOKENS}, L.TreeSource(repo)))
    ks, _, _ = L.scan_texts({"x.py": 'if lang == "kotlin":\n    pass\nif n.endswith(".zig"):\n    pass\n'}, t)
    assert any(k.endswith("|kotlin") for k in ks) and any(k.endswith("|.zig") for k in ks)
    ks0, _, _ = L.scan_texts({"x.py": 'if lang == "kotlin":\n    pass\n'}, L.Tokens(L.DEFAULT_TOKENS))
    assert not ks0, "before the data row exists, the word is no token"


def test_a_bom_and_crlf_file_is_scanned(tmp_path):
    repo = mk(tmp_path, scripts={"a.py": b"\xef\xbb\xbfdef f(p):\r\n    if p.suffix == '.py':\r\n        return p\r\n".decode("utf-8")},
              rows=[], baseline=True, commit_it=False)
    write(repo, SCRIPTS + "a.py", b"\xef\xbb\xbfdef f(p):\r\n    if p.suffix == '.py':\r\n        return p\r\n")
    commit(repo)
    sc = L.scan_paths(L.TreeSource(repo), [SCRIPTS + "a.py"], toks())
    assert not sc.errors and list(sc.live) == [key("a.py", "f", "compare", ".py")]


def test_a_a_site_in_a_script_named_test_novelty_is_scanned(tmp_path, run):
    repo = mk(tmp_path, scripts={"test_novelty.py": SCRIPT_A.replace("def f", "def g")}, rows=[])
    code, out = run(repo, "--check")
    assert code == 1 and "test_novelty.py in g" in out


NOT_FLAGGED = [
    ("docstring", 'def f():\n    """pytest .py mybooks"""\n    return 1'),
    ("comment", '# pytest .py\nx = 1'),
    ("refusal-text", 'print("pytest is not installed; run python -m pytest")'),
    ("json-suffix", 'p.suffix == ".json"'),
    ("argv-not-compared", 'cmd = ["pytest", "-q"]\nrun(cmd)'),
    ("capability-key", 'row.get("has_frames")'),
    ("python-version-attr", 'x = cfg.python_version'),
    ("longer-word", 'x == "testproject1_access_token"'),
    ("constant-bool-helper", 'def is_charter(x):\n    return True\ndef g(y):\n    if is_charter(y):\n        pass'),
]


@pytest.mark.parametrize("src", [pytest.param(s, id=i) for i, s in NOT_FLAGGED])
def test_b_not_flagged(src):
    assert keys_of(src) == {}


def test_b_a_same_named_unrelated_function_is_not_a_site():
    files = {"h.py": 'def observe(p):\n    return p == "pytest"\n',
             "o.py": 'def observe():\n    return None\ndef g():\n    observe()\n',
             "n.py": 'def g():\n    observe()\n'}
    ks, preds, _ = L.scan_texts(files, toks())
    assert "h.observe" in preds
    assert not [k for k in ks if k.startswith("o.py") or k.startswith("n.py")]


def test_b_tests_dir_and_data_rows_are_not_scanned(tmp_path, run):
    repo = mk(tmp_path, rows=[ROW_A], extra={SCRIPTS + "tests/driver_golden.py": SCRIPT_A,
                                              PKG + "references/rows.json": '{"x": ".py", "y": "pytest"}'})
    code, out = run(repo, "--check")
    assert code == 0, out


def test_m_known_misses_are_not_detected():
    t = toks()
    assert not keys_of('x = s.startswith("#")')                                             # 1 a shape with no token
    assert not keys_of('from other import PY\nname.endswith(PY)')                           # 2 imported constant
    assert not keys_of('name.endswith("." + ext)')                                          # 2 token built at run time
    ks, preds, _ = L.scan_texts({"m.py": 'def kind(n):\n    if n.endswith(".py"):\n        return "py"\n    return "o"\n'
                                         'def g(n):\n    return kind(n)\n'}, t)                # 3 non-bool returns
    assert "m.kind" not in preds and not [k for k in ks if "predicate-call" in k]
    a = keys_of('if p.suffix == ".py":\n    go()\n')
    b = keys_of('if p.suffix != ".py":\n    go()\nelse:\n    other()\n')
    assert set(a) == set(b)                                                                   # 4 inverted in place
    assert keys_of('def f():\n    return 1\n') == {}                                         # 5 absence
    assert keys_of('x == "someproject"') == {}                                               # 7 unlisted project
    assert keys_of('ext == "py"\next == "ts"') == {}                                         # 9 bare short form
    assert not [k for k in keys_of('obj.is_pytest_command(x)') if "predicate-call" in k]     # 10 unknown object
    base = doc([row(key("a.py", "f", "compare", ".py"), mech="M1")])
    traded = doc([row(key("a.py", "g", "compare", ".py"), mech="M1")])
    assert not [i for i in L.compare_docs(base, traded)["items"] if i["red"]]                 # 8 trade in one file
    road = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1", word=word())
    far = row(key("b.py", "f", "compare", ".py"), kind="road", mech="M1", word=word(), moved_from=road["key"])
    res = L.compare_docs(doc([road]), doc([dict(far)]))                                      # 11 honest-looking move
    assert not [i for i in res["items"] if i["red"]] and any(i["type"] == "moved" for i in res["items"])


def test_m_text_files_are_outside_the_scan(tmp_path, run):
    repo = mk(tmp_path, extra={PKG + "references/test-code-patterns.md": "if ext == '.py': pytest\n"})
    assert run(repo, "--check")[0] == 0                                                      # 6 text


# ------------------------------------------------------------------------------------------------ the negative control, T-R
def test_negative_control_a_site_with_its_row_is_green_without_it_red(tmp_path, run):
    repo = mk(tmp_path)
    assert run(repo, "--check")[0] == 0
    put(repo, doc([]))
    code, out = run(repo, "--check")
    assert code == 1 and "C1" in out


def test_r_the_refusal_holds_the_three_doors_path_qualname_token(tmp_path, run):
    repo = mk(tmp_path, rows=[])
    code, out = run(repo, "--check")
    assert code == 1
    for part in ("a new branch on a language, the baseline holds no row for it", SCRIPTS + "a.py in f: compare on `.py` (line 2)",
                 "1. A data row", "2. The owner's word", "3. Not a language road", "docs/SIBLING_MAP.md axis 33",
                 "word {who, date, quote, carrier}", "`own-code` or `floor` and a `reason`", "moved_from"):
        assert part in out, part


def test_r_c3_c5_c6_refusals_name_expected_and_a_door(tmp_path, run):
    repo = mk(tmp_path, scripts={"b.py": 'def is_py(n):\n    return n.endswith(".py")\n'},
              rows=[row(key("b.py", "is_py", "name-call", ".py"))])
    code, out = run(repo, "--check")
    assert code == 1 and "C6" in out and "--predicates" in out and "Expected" in out


# ------------------------------------------------------------------------------------------------ the edges
def test_e1_edit_above_a_site_is_not_an_event(tmp_path, run):
    repo = mk(tmp_path)
    write(repo, SCRIPTS + "a.py", "# one\n# two\n\n\n" + SCRIPT_A)
    assert run(repo, "--check")[0] == 0


def test_e1_a_widened_token_is_a_new_key_and_an_inverted_branch_is_green(tmp_path, run):
    repo = mk(tmp_path)
    write(repo, SCRIPTS + "a.py", SCRIPT_A.replace('== ".py"', '!= ".py"'))
    assert run(repo, "--check")[0] == 0
    write(repo, SCRIPTS + "a.py", SCRIPT_A.replace('== ".py"', 'in (".py", ".pyi")'))
    code, out = run(repo, "--check")
    assert code == 1 and "`.pyi`" in out


def test_e2_a_rename_needs_its_row_moved(tmp_path, run):
    repo = mk(tmp_path)
    write(repo, SCRIPTS + "a.py", SCRIPT_A.replace("def f", "def g"))
    code, out = run(repo, "--check")
    assert code == 1 and "C1" in out and "C2" in out
    put(repo, doc([dict(ROW_A, key=key("a.py", "g", "compare", ".py"))]))
    assert run(repo, "--check", "--base", "HEAD")[0] == 0


def test_e2_a_split_is_two_moves_when_the_total_holds_and_the_fields_travel():
    big = row(key("a.py", "f", "compare", ".py"), count=2)
    parts = [row(key("a.py", "g", "compare", ".py")), row(key("a.py", "h", "compare", ".py"))]
    res = L.compare_docs(doc([big]), doc(parts))
    # fork 1: a removed row of count 2 covers two rows of count 1 inside the same (path, form, token, mechanism)
    assert sorted(i["type"] for i in res["items"]) == ["moved", "moved"]
    assert not reds(res)


def test_e3_new_language_row_in_a_data_file(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A, "u.py": 'x = 1\n'})
    write(repo, PKG + L.DETECTORS_NAME, json.dumps({"assertion_probes": dict(DET["assertion_probes"], go={"suffixes": [".go"]})}))
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 0, out                                              # `.go` is already a token; `go` is a word nothing branches on
    write(repo, SCRIPTS + "u.py", 'if tool == "go":\n    pass\n')
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "`go`" in out


@pytest.mark.parametrize("name,text", [
    pytest.param("detectors-malformed", "{nope", id="detectors-malformed"),
    pytest.param("detectors-no-probes", "{}", id="detectors-no-probes"),
    pytest.param("detectors-no-suffixes", '{"assertion_probes": {"x": {}}}', id="detectors-no-suffixes"),
])
def test_e3_a_malformed_data_file_is_exit_2_never_no_extra_tokens(tmp_path, run, name, text):
    repo = mk(tmp_path)
    write(repo, PKG + L.DETECTORS_NAME, text)
    code, out = run(repo, "--check")
    assert code == 2 and "detectors.json" in out


def test_e3_missing_markers_is_exit_2_and_the_shape_of_both_files_is_pinned(tmp_path, run):
    repo = mk(tmp_path)
    got = L.data_tokens(L.TreeSource(repo), PKG, True)
    assert got == {"suffix": sorted([".cs", ".java", ".py", ".js", ".go", ".kt"]), "language": ["csharp", "java"]}
    (repo / (PKG + L.MARKERS_NAME)).unlink()
    code, out = run(repo, "--check")
    assert code == 2 and "test-path-markers.json" in out


def test_e4_scan_by_location_not_by_name(tmp_path, run):
    repo = mk(tmp_path, rows=[], scripts={"test_novelty.py": SCRIPT_A, "tests/driver_golden.py": SCRIPT_A})
    code, out = run(repo, "--check")
    assert code == 1 and "test_novelty.py" in out and "driver_golden" not in out


def test_e5_a_generated_py_under_hooks_is_scanned(tmp_path, run):
    repo = mk(tmp_path, extra={PKG + "hooks/gen.py": SCRIPT_A})
    code, out = run(repo, "--check")
    assert code == 1 and "hooks/gen.py" in out


def test_e6_tools_is_outside_the_root(tmp_path, run):
    repo = mk(tmp_path, extra={"tools/own.py": SCRIPT_A})
    assert run(repo, "--check")[0] == 0


def test_e8_a_raise_needs_a_new_reason(tmp_path, run):
    old = row(key("a.py", "f", "compare", ".py"), reason="first reason")
    repo = mk(tmp_path, rows=[old])
    write(repo, SCRIPTS + "a.py", SCRIPT_A.replace('return p\n', 'return p\n    if p.suffix == ".py":\n        return p\n', 1))
    put(repo, doc([dict(old, count=2)]))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "under the same reason" in out
    put(repo, doc([dict(old, count=2, reason="second, different reason")]))
    assert run(repo, "--check", "--base", "HEAD")[0] == 0
    code, out = run(repo, "--raises", "--base", "HEAD")
    assert code == 0 and "raised" in out and "1 -> 2" in out.replace("count ", "") or "1 -> 2" in out


def test_e9_init_refuses_and_shrink_is_the_fix_commit_door(tmp_path, run):
    two = SCRIPT_A + 'def g(p):\n    if p.suffix == ".go":\n        return p\n'
    repo = mk(tmp_path, scripts={"a.py": two}, rows=[ROW_A, row(key("a.py", "g", "compare", ".go"))], git=False)
    code, out = run(repo, "--init")
    assert code == 1 and "exists" in out
    write(repo, SCRIPTS + "a.py", SCRIPT_A + "def g(p):\n    return None\n")
    code, out = run(repo, "--check")
    assert code == 1 and "C2" in out
    assert run(repo, "--shrink")[0] == 0
    assert run(repo, "--check")[0] == 0


def test_e10_partial_staging_reads_the_index(tmp_path, run):
    repo = mk(tmp_path)
    extra = SCRIPT_A + 'def g(p):\n    if p.suffix == ".go":\n        return p\n'
    write(repo, SCRIPTS + "a.py", extra)
    sh(repo, "add", "-A")
    write(repo, SCRIPTS + "a.py", SCRIPT_A)                            # the unstaged fix does not count
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "`.go`" in out
    sh(repo, "add", "-A")                                              # the fix is staged ...
    write(repo, SCRIPTS + "a.py", extra)                               # ... and the working tree holds a new site
    assert run(repo, "--check", "--staged")[0] == 0


def test_e11_a_script_that_does_not_parse_is_red_and_staged_judges_only_staged(tmp_path, run):
    repo = mk(tmp_path, extra={SCRIPTS + "bad.py": "def (:\n"})
    code, out = run(repo, "--check")
    assert code == 1 and "bad.py does not parse" in out and "line 1" in out
    write(repo, SCRIPTS + "a.py", SCRIPT_A + "# touched\n")
    sh(repo, "add", "-A")
    assert run(repo, "--check", "--staged")[0] == 0


def test_e12_rows_are_one_per_line_and_sorted_so_branches_merge():
    d = doc([row("z.py|f|compare|.py"), row("a.py|f|compare|.py")])
    lines = L.dumps(d).split("\n")
    row_lines = [ln for ln in lines if ln.strip().startswith('{"key"')]
    assert [json.loads(r.strip().rstrip(",") )["key"] for r in row_lines] == ["a.py|f|compare|.py", "z.py|f|compare|.py"]
    assert "\r" not in L.dumps(d) and json.loads(L.dumps(d))["schema"] == 1


def test_e14_a_deleted_script_leaves_stale_rows_unless_moved(tmp_path, run):
    repo = mk(tmp_path)
    sh(repo, "rm", "-q", SCRIPTS + "a.py")
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "C2" in out


def test_e15_an_empty_scan_is_not_green(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": "x = 1\n"})
    code, out = run(repo, "--check")
    assert code == 2 and "found 0 sites" in out and "1 rows" in out
    repo2 = mk(tmp_path / "two", scripts={}, rows=[])
    code, out = run(repo2, "--check")
    assert code == 2 and "0 files" in out


def test_e16_narrowing_the_scan_needs_a_basis_word(tmp_path, run):
    rb = row(key("b.py", "g", "compare", ".go"))
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A, "b.py": 'def g(p):\n    if p.suffix == ".go":\n        return p\n'}, rows=[ROW_A, rb])
    d = L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")
    d["scan"] = dict(d["scan"], exclude=d["scan"]["exclude"] + [SCRIPTS + "a.py"])
    put(repo, dict(d, rows=[rb]))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "C5" in out and "basis_word" in out
    put(repo, dict(d, rows=[rb], basis_word=word()))
    assert run(repo, "--check", "--base", "HEAD")[0] == 0


def test_e17_the_word_cases_through_check_word(tmp_path):
    repo = mk(tmp_path)
    src = L.TreeSource(repo)
    assert L.check_word(word(), src) is None
    assert "0 characters" in L.check_word(word(quote=""), src)
    assert "11 characters" in L.check_word(word(quote="elevenchars"), src)
    assert L.check_word(word(quote="  twelve   chars!  ok  "), src) is not None             # whitespace is squashed: "twelve chars! ok" not in the carrier
    assert "baseline" in L.check_word(word(carrier=L.BASELINE_REL), src)
    assert "`who`" in L.check_word(word(who=" "), src)
    assert "not a tracked file" in L.check_word(word(carrier="nowhere.md"), src)
    write(repo, "untracked.md", QUOTE)
    assert "not a tracked file" in L.check_word(word(carrier="untracked.md"), src)
    assert "does not stand" in L.check_word(word(quote="a long quote that is nowhere to be found"), src)
    assert "not a path inside" in L.check_word(word(carrier="../outside.md"), src)
    assert L.check_word("not a dict", src)
    assert L.check_word(word(), L.IndexSource(repo)) is None


def test_e17_a_quote_written_into_another_tracked_file_in_the_same_commit_passes(tmp_path, run):
    old = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1")
    repo = mk(tmp_path, rows=[old])
    write(repo, SCRIPTS + "a.py", SCRIPT_A2)
    write(repo, "new-carrier.md","Said today: a brand new twelve plus quote.\n")
    put(repo, doc([dict(old, count=2, word=word("a brand new twelve plus quote", "new-carrier.md"))]))
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 0, out


def test_e22_a_helper_gaining_a_site_makes_callers_new_until_rows_stand(tmp_path, run):
    b0, c0 = 'def is_py(n):\n    return True\n', 'from b import is_py\nif is_py(1):\n    pass\n'
    repo = mk(tmp_path, scripts={"b.py": b0, "c.py": c0}, rows=[])
    assert run(repo, "--check")[0] == 0
    write(repo, SCRIPTS + "b.py", 'def is_py(n):\n    return n.endswith(".py")\n')
    code, out = run(repo, "--check")
    assert code == 1 and "C6" in out and "c.py" in out and "b.py in is_py: name-call" in out
    assert run(repo, "--predicates")[0] == 0
    put(repo, doc([row(key("b.py", "is_py", "name-call", ".py")), row(key("c.py", "<module>", "predicate-call", "b.is_py"))],
                  ["b.is_py"]))
    assert run(repo, "--check")[0] == 0


def test_e23_a_token_grown_by_a_data_file_alone_runs_the_whole_scan(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A, "x.py": 'if lang == "kotlin":\n    pass\n'})
    write(repo, PKG + L.DETECTORS_NAME, json.dumps({"assertion_probes": dict(DET["assertion_probes"], kotlin={"suffixes": [".kt"]})}))
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "x.py in <module>: compare on `kotlin`" in out


def test_e24_the_effective_base_is_the_first_commit_adding_the_baseline(tmp_path, run):
    repo = mk(tmp_path, baseline=False)
    c0 = head(repo)
    write(repo, L.BASELINE_REL, L.dumps(doc([row(key("a.py", "f", "compare", ".py"), reason="first reason")])))
    commit(repo, "n2")
    code, out = run(repo, "--check", "--base", c0)
    assert code == 0 and "created here" in out
    write(repo, SCRIPTS + "a.py", SCRIPT_A + 'def g(p):\n    if p.suffix == ".py":\n        return p\n')
    put(repo, doc([row(key("a.py", "f", "compare", ".py"), count=1, reason="first reason"),
                   row(key("a.py", "g", "compare", ".py"), reason="x")]))
    commit(repo, "later")
    put(repo, doc([row(key("a.py", "f", "compare", ".py"), count=1, reason="first reason"),
                   row(key("a.py", "g", "compare", ".py"), reason="")]))
    code, out = run(repo, "--check", "--base", c0)
    assert code == 1 and "C3" in out and "effective base" in out


def test_e25_rev_with_no_baseline_or_no_package(tmp_path, run):
    repo = mk(tmp_path, baseline=False)
    code, out = run(repo, "--check", "--rev", "HEAD")
    assert code == 2 and "missing" in out
    sh(repo, "rm", "-q", "-r", PKG)
    sh(repo, "commit", "-q", "-m", "nopkg")
    code, out = run(repo, "--check", "--rev", "HEAD")
    assert code == 0 and "no package here" in out


# ------------------------------------------------------------------------------------------------ the worlds
MODES = {"whole": ["--check"], "rev": ["--check", "--rev", "HEAD"], "staged": ["--check", "--staged"]}


def trigger(repo):
    write(repo, SCRIPTS + "a.py", SCRIPT_A + "# touched\n")
    sh(repo, "add", "-A")


def test_w_one_fixture_through_three_readers_pins_equal_keys(tmp_path):
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A, "b.py": 'def is_py(n):\n    return n.endswith(".py")\n',
                                 "c.py": 'from b import is_py\nif is_py(1):\n    pass\n'})
    paths = [SCRIPTS + n for n in ("a.py", "b.py", "c.py")]
    got = [L.scan_paths(s, paths, toks()).live for s in (L.TreeSource(repo), L.IndexSource(repo), L.RevSource(repo, "HEAD"))]
    assert got[0] == got[1] == got[2] and len(got[0]) == 3


def test_w1_before_n3_nothing_calls_the_tool_it_runs_by_hand(tmp_path, run):
    repo = mk(tmp_path)
    assert not (repo / ".githooks").exists()
    assert run(repo, "--check")[0] == 0 and run(repo, "--totals")[0] == 0


@pytest.mark.parametrize("mode", ["whole", "rev", "staged"])
def test_w2_a_clone_with_no_package_is_exit_0_and_says_so(tmp_path, run, mode):
    if mode == "staged":
        repo = mk(tmp_path, baseline=False)
        sh(repo, "rm", "-q", "-r", PKG)
    else:
        repo = mk(tmp_path, scripts={}, baseline=False, data=False, extra={"tools/x.py": "x = 1\n"})
    code, out = run(repo, *MODES[mode])
    assert code == 0 and "no package here" in out


@pytest.mark.parametrize("mode", ["whole", "rev", "staged"])
def test_w3_package_without_a_baseline_is_exit_2(tmp_path, run, mode):
    repo = mk(tmp_path, baseline=False)
    if mode == "staged":
        trigger(repo)
    code, out = run(repo, *MODES[mode])
    assert code == 2 and "language-sites-baseline.json is missing" in out and "merge the branch" in out


def test_w4_a_deleted_baseline_is_exit_1_with_no_door(tmp_path, run):
    repo = mk(tmp_path)
    sh(repo, "rm", "-q", L.BASELINE_REL)
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "deleted by this commit" in out
    sh(repo, "commit", "-q", "-m", "gone")
    code, out = run(repo, "--check", "--rev", "HEAD", "--base", "HEAD~1")
    assert code == 1 and "deleted" in out
    repo2 = mk(tmp_path / "w", )
    (repo2 / L.BASELINE_REL).unlink()
    code, out = run(repo2, "--check", "--base", "HEAD")
    assert code == 1 and "deleted" in out


@pytest.mark.parametrize("mode", ["whole", "rev", "staged"])
def test_w5_an_unread_baseline_is_exit_2(tmp_path, run, monkeypatch, mode):
    repo = mk(tmp_path)
    if mode == "whole":
        (repo / L.BASELINE_REL).unlink()
        (repo / L.BASELINE_REL).mkdir()
    else:
        real = L._git_blob
        monkeypatch.setattr(L, "_git_blob", lambda r, spec: L.Unread("boom: bad object") if spec.endswith(L.BASELINE_REL) else real(r, spec))
        if mode == "staged":
            trigger(repo)
    code, out = run(repo, *MODES[mode])
    assert code == 2 and "W5" in out


def test_w6_creation_is_not_a_raise_but_c1_still_runs(tmp_path, run):
    repo = mk(tmp_path, baseline=False)
    write(repo, L.BASELINE_REL, L.dumps(doc([dict(ROW_A, count=1, kind="road")])))
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 0 and "created here" in out
    put(repo, doc([]))
    sh(repo, "add", "-A")
    code, out = run(repo, "--check", "--staged")
    assert code == 1 and "C1" in out


def test_w7_the_tool_runs_from_the_callers_tree_on_a_ref_that_lacks_it(tmp_path, run):
    repo = mk(tmp_path)
    assert not (repo / "tools" / "language_sites.py").exists()
    assert run(repo, "--check", "--rev", "HEAD")[0] == 0


@pytest.mark.parametrize("ref", ["0" * 40, "no-such-ref"])
def test_w8_a_base_that_does_not_resolve_is_exit_2_naming_it(tmp_path, run, ref):
    repo = mk(tmp_path)
    code, out = run(repo, "--check", "--base", ref)
    assert code == 2 and ref in out and "never narrow" in out
    code, out = run(repo, "--raises", "--base", ref)
    assert code == 2


# ------------------------------------------------------------------------------------------------ rules of C3, C5, C6, MOVE
def reds(res):
    return [i for i in res["items"] if i["red"]]


def test_c3a_a_raise_under_the_same_quote_or_reason_is_red_a_new_one_green():
    road = row(key("a.py", "f", "compare", ".py"), kind="road", word=word())
    assert reds(L.compare_docs(doc([road]), doc([dict(road, count=2)])))
    assert not reds(L.compare_docs(doc([road]), doc([dict(road, count=2, word=word("another twelve plus quote"))])))
    own = row(key("a.py", "f", "compare", ".py"), reason="one")
    assert reds(L.compare_docs(doc([own]), doc([dict(own, count=2)])))
    assert not reds(L.compare_docs(doc([own]), doc([dict(own, count=2, reason="two")])))
    assert reds(L.compare_docs(doc([road]), doc([dict(road, count=2, word=dict(word(), date="2027-01-01"))])))   # a date is no new word


def test_c3b_road_to_own_code_with_a_reason_and_a_raise_but_no_word_is_red():
    road = row(key("a.py", "f", "compare", ".py"), kind="road", word=word())
    cur = row(key("a.py", "f", "compare", ".py"), count=2, reason="it is our own script")
    assert reds(L.compare_docs(doc([road]), doc([cur])))


def test_c3c_a_relabel_alone_is_printed_and_red(tmp_path, run):
    road = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1")
    repo = mk(tmp_path, rows=[road])
    put(repo, doc([row(key("a.py", "f", "compare", ".py"), mech="M1", reason="own script now")]))
    code, out = run(repo, "--raises", "--base", "HEAD")
    assert code == 0 and "relabelled" in out and "RED" in out
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "relabelled" in out


def test_c3_own_code_and_floor_relabels_are_printed_not_red():
    a = row(key("a.py", "f", "compare", ".py"), reason="one")
    b = dict(a, kind="floor", reason="a declared floor")
    res = L.compare_docs(doc([a]), doc([b]))
    assert not reds(res) and any(i["type"] == "relabelled" for i in res["items"])
    res = L.compare_docs(doc([a]), doc([dict(a, mechanism="FLOOR")]))
    assert any(i["type"] == "re-mechanised" for i in res["items"]) and not reds(res)


def test_c3_removing_a_word_or_a_reason_is_red():
    road = row(key("a.py", "f", "compare", ".py"), kind="road", word=word())
    assert reds(L.compare_docs(doc([road]), doc([dict(road, word=None)])))
    own = row(key("a.py", "f", "compare", ".py"), reason="one")
    assert reds(L.compare_docs(doc([own]), doc([dict(own, reason="")])))


def test_c3_an_added_row_needs_the_fields_of_its_kind():
    assert reds(L.compare_docs(doc([]), doc([row("a.py|f|compare|.py", kind="road")])))
    assert reds(L.compare_docs(doc([]), doc([row("a.py|f|compare|.py", reason="")])))
    assert not reds(L.compare_docs(doc([]), doc([row("a.py|f|compare|.py", kind="road", word=word())])))


def test_move_rules():
    own = row(key("a.py", "f", "compare", ".py"), reason="the audit reads itself")
    same = dict(own, key=key("a.py", "g", "compare", ".py"))
    res = L.compare_docs(doc([own]), doc([same]))
    assert not reds(res) and [i["type"] for i in res["items"]] == ["moved"]
    # a cross-file own-code move with the same reason is red, with a new reason green and printed
    far = dict(own, key=key("b.py", "f", "compare", ".py"), moved_from=own["key"])
    assert reds(L.compare_docs(doc([own]), doc([far])))
    far2 = dict(far, reason="a different script, a different reason")
    res = L.compare_docs(doc([own]), doc([far2]))
    assert not reds(res) and any(i["type"] == "added" for i in res["items"])
    # a cross-file road move with moved_from is green and printed; without it, an added row and red
    road = row(key("a.py", "f", "compare", ".py"), kind="road", word=word())
    rfar = dict(road, key=key("b.py", "f", "compare", ".py"), moved_from=road["key"])
    res = L.compare_docs(doc([road]), doc([rfar]))
    assert not reds(res) and any("across files" in i["text"] for i in res["items"])
    assert reds(L.compare_docs(doc([road]), doc([dict(rfar, moved_from=None, word=None)])))
    # ... and with the word still on it (F2): leaving `moved_from` out is not a way past -- the word is repeated
    for mf in (None, "no|such|key|x"):
        assert reds(L.compare_docs(doc([road]), doc([dict(rfar, moved_from=mf)]))), mf
    assert reds(L.compare_docs(doc([own]), doc([dict(far, moved_from=None)])))                  # own-code, same reason
    # a move that raises the file's total is not a move: an ordinary added row
    res = L.compare_docs(doc([own]), doc([dict(same, count=2)]))
    assert [i["type"] for i in res["items"]] == ["added"]
    assert reds(L.compare_docs(doc([own]), doc([dict(same, count=2, reason="")])))


def test_c5_three_narrowings_red_without_basis_word_and_a_removed_site_green(tmp_path, run):
    b = {"b.py": 'def is_py(n):\n    return n.endswith(".py")\n'}
    rows = [row(key("b.py", "is_py", "name-call", ".py"))]
    repo = mk(tmp_path, scripts=b, rows=rows, predicates=["b.is_py"])
    assert run(repo, "--check", "--base", "HEAD")[0] == 0
    # a live predicate dropped
    put(repo, doc(rows, []))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "C5" in out and "still a predicate" in out
    put(repo, doc(rows, [], basis_word=word()))
    assert "C5" not in run(repo, "--check", "--base", "HEAD")[1]
    # a token removed through a data file
    put(repo, doc(rows, ["b.is_py"]))
    write(repo, PKG + L.MARKERS_NAME, json.dumps({"code_extensions": [".py", ".cs", ".go", ".kt"]}))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "tokens removed" in out and "suffix:.js" in out
    write(repo, PKG + L.MARKERS_NAME, json.dumps(MARK))
    # the scan root narrowed
    d = L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")
    put(repo, dict(d, scan=dict(d["scan"], root=PKG + "scripts/")))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "`scan` changed" in out
    # a predicate whose site was removed: green
    put(repo, doc([], []))
    write(repo, SCRIPTS + "b.py", 'def is_py(n):\n    return True\n')
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 0, out


def test_c5_a_stale_basis_word_does_not_license_a_new_narrowing(tmp_path, run):
    repo = mk(tmp_path, basis_word=word())
    d = L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")
    put(repo, dict(d, scan=dict(d["scan"], exclude=[]), rows=[ROW_A]))
    assert run(repo, "--check", "--base", "HEAD")[0] == 1


def test_c6_a_stale_list_is_red_and_predicates_clears_it(tmp_path, run):
    repo = mk(tmp_path, scripts={"b.py": 'def is_py(n):\n    return n.endswith(".py")\n',
                                 "c.py": 'from b import is_py\nif is_py(1):\n    pass\n'},
              rows=[row(key("b.py", "is_py", "name-call", ".py"))])
    code, out = run(repo, "--check")
    assert code == 1 and "C6" in out and "grew ['b.is_py']" in out
    code, out = run(repo, "--predicates")
    assert code == 0 and "grew b.is_py" in out
    d = L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")
    assert d["predicates"] == ["b.is_py"] and len(d["rows"]) == 1                  # no row was written
    code, out = run(repo, "--check")
    assert code == 1 and "c.py in <module>: predicate-call on `b.is_py`" in out and "C6" not in out
    put(repo, dict(d, rows=d["rows"] + [row(key("c.py", "<module>", "predicate-call", "b.is_py"))]))
    assert run(repo, "--check")[0] == 0


def test_inv_shrink_cannot_raise_predicates_writes_no_row_init_refuses(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A + 'def g(p):\n    if p.suffix == ".py":\n        return p\n    if p.suffix == ".go":\n        return 1\n'},
              rows=[dict(ROW_A, count=3)])
    assert run(repo, "--shrink")[0] == 0
    d = L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")
    assert [(r["key"], r["count"]) for r in d["rows"]] == [(ROW_A["key"], 1)]        # lowered 3 -> 1, the new keys are not added
    assert run(repo, "--predicates")[0] == 0
    assert len(L.load_doc((repo / L.BASELINE_REL).read_bytes(), "b")["rows"]) == 1
    code, out = run(repo, "--init")
    assert code == 1 and "exists" in out
    code, out = run(repo, "--check")
    assert code == 1 and "`.go`" in out


def test_init_writes_the_first_fill_and_refuses_a_second(tmp_path, run):
    repo = mk(tmp_path, baseline=False)
    code, out = run(repo, "--init")
    assert code == 0 and "wrote 1 rows" in out
    assert run(repo, "--check")[0] == 0
    code, out = run(repo, "--totals")
    assert code == 0 and "rows 1" in out and "wall time" in out and "road 1" in out
    assert run(repo, "--init")[0] == 1


def test_ar2_the_tool_never_reads_a_word_for_meaning(tmp_path, run):
    old = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1")
    repo = mk(tmp_path, rows=[old])
    write(repo, SCRIPTS + "a.py", SCRIPT_A2)
    write(repo, "finding.md", "nonsense that is no decision at all: zzzz qqqq wwww\n")
    put(repo, doc([dict(old, count=2, word=word("nonsense that is no decision", who="anyone"))]))
    commit(repo, "w")
    assert run(repo, "--check", "--base", "HEAD~1")[0] == 0


# ------------------------------------------------------------------------------------------------ round t-2092 (critic t-2088)
def test_f1_a_relabel_through_a_new_key_is_red_at_any_count():
    k_f, k_g = key("a.py", "f", "compare", ".py"), key("a.py", "g", "compare", ".py")
    for base_road in (row(k_f, count=2, kind="road", mech="M1"), row(k_f, count=2, kind="road", mech="M1", word=word())):
        curs = [row(k_g, count=2, mech="M1", reason="x"),                                      # no word at all
                row(key("b.py", "f", "compare", ".py"), count=2, mech="M1", reason="x"),       # another file, no moved_from
                row(k_g, count=2, mech="OWN", reason="x")]                                     # re-mechanised too
        if "word" in base_road:
            curs.append(row(k_g, count=2, mech="M1", reason="x", word=word()))                 # the base's own quote
        for cur in curs:
            assert reds(L.compare_docs(doc([base_road]), doc([cur]))), cur
    own_new = row(k_g, count=2, mech="M1", reason="x", word=word("a brand new twelve plus quote"))
    assert not reds(L.compare_docs(doc([row(k_f, count=2, kind="road", mech="M1")]), doc([own_new])))   # a new word buys it


def test_f1_end_to_end_rename_and_relabel_is_red_in_check_and_raises(tmp_path, run):
    road = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1")
    repo = mk(tmp_path, rows=[road])
    write(repo, SCRIPTS + "a.py", SCRIPT_A.replace("def f", "def g"))
    put(repo, doc([row(key("a.py", "g", "compare", ".py"), mech="M1", reason="x")]))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "C3" in out
    code, out = run(repo, "--raises", "--base", "HEAD")
    assert code == 0 and "RED" in out


def test_f2_a_raise_through_a_new_key_under_the_old_word_or_reason_is_red():
    k_f, k_g = key("a.py", "f", "compare", ".py"), key("a.py", "g", "compare", ".py")
    road = row(k_f, kind="road", word=word())
    assert reds(L.compare_docs(doc([road]), doc([road, row(k_g, count=9, kind="road", word=word())])))   # same word
    assert not reds(L.compare_docs(doc([road]), doc([road, row(k_g, count=9, kind="road", word=word("a new word of twelve plus"))])))
    own = row(k_f, reason="one")
    assert reds(L.compare_docs(doc([own]), doc([own, row(k_g, reason="one")])))                           # same reason
    assert not reds(L.compare_docs(doc([own]), doc([own, row(k_g, reason="two")])))
    # the same word on SEVERAL new rows of one commit is E22's "one word on all callers": not red
    fresh = word("a fresh twelve plus word")
    assert not reds(L.compare_docs(doc([road]), doc([road, row(k_g, kind="road", word=fresh),
                                                     row(key("a.py", "h", "compare", ".py"), kind="road", word=fresh)])))
    # a road total that rises without a new quote is red even when the added row's own fields look complete
    far = row(key("b.py", "f", "compare", ".py"), kind="road", word=word(), moved_from=k_f)
    assert reds(L.compare_docs(doc([road]), doc([road, far])))


def test_f3_whole_mode_judges_every_row_a_ghost_row_and_a_deleted_script_are_c2(tmp_path, run):
    ghost = row("ghost.py|f|compare|.py", count=7)
    repo = mk(tmp_path, rows=[ROW_A, dict(ghost, key=SCRIPTS + "ghost.py|f|compare|.py")])
    for args in (("--check",), ("--check", "--base", "HEAD"), ("--check", "--rev", "HEAD")):
        code, out = run(repo, *args)
        assert code == 1 and "C2" in out and "ghost.py" in out, (args, out)


def test_f3_whole_mode_and_staged_agree_on_a_deleted_script_with_no_predicate(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": SCRIPT_A, "b.py": "x = 1\n"}, rows=[ROW_A, row(key("b.py", "f", "compare", ".py"))])
    sh(repo, "rm", "-q", SCRIPTS + "b.py")                       # b.py had a row and no site: the ghost case
    for args in (("--check", "--staged"), ("--check",)):
        code, out = run(repo, *args)
        assert code == 1 and "C2" in out and "b.py" in out, (args, out)


def test_f4_a_redefined_qualname_keeps_the_earlier_sites():
    cases = {
        "dup-def": 'def f(n):\n    return n == ".py"\ndef f(n):\n    return 1\n',
        "property-setter": 'class C:\n    @property\n    def d(self):\n        return self.x == ".py"\n'
                           '    @d.setter\n    def d(self, v):\n        self.x = v\n',
        "try-except-def": 'try:\n    def r(n):\n        return n == ".py"\nexcept ImportError:\n    def r(n):\n        return 1\n',
        "else-def": 'if A:\n    def r(n):\n        return 1\nelse:\n    def r(n):\n        return n == ".py"\n',
    }
    for name, src in cases.items():
        assert [k for k in keys_of(src) if k.endswith("|compare|.py")], name


def test_f6_literal_arithmetic_and_assignment_shapes():
    for src in ('E = (".py",) + (".go",)\nn in E', 'E = [".py", ".rb"] + [".go"]\nn in E', 'E = {".py"} | {".go"}\nn in E',
                'A = B = ".py"\nn == B', 'A, B = ".py", ".ts"\nn == A', 'n == (".py" if a else ".go")',
                'A = (".py",)\nB = (".go",)\nE = A + B\nn in E'):
        ks = keys_of(src)
        assert any(k.endswith("compare|.py") for k in ks), (src, sorted(ks))
    ks = keys_of('E = (".py",) + (".go",)\nn in E')
    assert any(k.endswith("compare|.go") for k in ks) and any(k.endswith("compare|.py") for k in ks)
    assert not keys_of('name.endswith("." + "json")')                                      # a string `+` still concatenates


def test_f7_regex_shapes_a_group_after_a_dot_a_bracket_dot_and_more_functions():
    for pat in (r"\.(py|ts)$", r"\.(?:go)$", r"[.]py$", r"\.pyi?$"):
        ks = keys_of('import re\nre.search(r"%s", n)' % pat.replace("\\", "\\\\"))
        assert any("regex|.py" in k or "regex|.go" in k for k in ks), (pat, sorted(ks))
    assert any("regex|.pyi" in k for k in keys_of('import re\nre.search(r"\\.pyi?$", n)'))
    assert any("regex|.py" in k for k in keys_of('import re\nre.search(r"\\.pyi?$", n)') if not k.endswith(".pyi"))
    for fn in ("findall", "finditer", "subn"):
        assert keys_of('import re\nre.%s(r"pytest", n)' % fn), fn


def test_f8_closed_shapes_and_the_pinned_ones():
    for src in ('n.find(".py") != -1', 'n.count("pytest") > 0', 's.removeprefix("pytest")', 'case_ = 1\nmatch x:\n    case {"pytest": y}:\n        pass',
                'dict(pytest=1)', 'import re\nre.compile(r"^\\s*require\\s")', 'import re\nre.compile(r"#include\\s")',
                'import re\nre.compile(r"^\\s*using\\s")', 'import re\nre.compile(r"^function\\s")'):
        assert keys_of(src), src
    ks, preds, _ = L.scan_texts({"er.py": 'def is_p(c):\n    return c == "pytest"\n',
                                 "k.py": 'import er\nfrom er import is_p\ndef g(cs):\n    return filter(er.is_p, cs)\n'
                                         'chk = is_p\n'}, toks())
    assert "er.is_p" in preds and sum(len(v) for k, v in ks.items() if k.startswith("k.py") and k.endswith("er.is_p")) == 2
    # pinned (known misses 12 and 13): a function-local constant, a class attribute, a dotted module path
    assert not keys_of('def f(n):\n    E = ".py"\n    return n == E')
    assert not keys_of('class C:\n    E = ".py"\n    def f(self, n):\n        return n == E')
    assert not keys_of('import ast\nimport pkg.er\npkg.er.is_p(c)')
    # pinned (F8 remainder): the parser reached through a flag or a star import carries no `ast.parse` name
    assert not keys_of('import ast\ndef rd(s):\n    return compile(s, "f", "exec", ast.PyCF_ONLY_AST)')
    assert not keys_of('from ast import *\ndef rd(s):\n    return parse(s)')
    # pinned (fork 3): a syntax word counts only before whitespace, so `\\(`, a bare `#include` and `|class|` do not
    for pat in ('^\\s*require\\(', '#include', 'bug-class):', '|class|'):
        assert not keys_of('import re\nre.compile(r"%s")' % pat), pat


def test_f9_the_whole_word_is_compared_and_raises_prints_basis_word(tmp_path, run):
    old = row(key("a.py", "f", "compare", ".py"), kind="road", mech="M1", word=word())
    res = L.compare_docs(doc([old]), doc([dict(old, word=dict(word(), who="", carrier="nope.md"))]))
    assert [i["type"] for i in res["items"]] == ["reworded"] and res["words"]                # and C3b runs on it
    repo = mk(tmp_path, rows=[old], basis_word=word())
    put(repo, doc([old], basis_word=dict(word(), who="", carrier="nope.md")))
    code, out = run(repo, "--raises", "--base", "HEAD")
    assert "basis_word" in out and "RED  C3b" in out
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "C3b" in out
    put(repo, doc([dict(old, word=dict(word(), carrier="nope.md"))], basis_word=word()))
    code, out = run(repo, "--check", "--base", "HEAD")
    assert code == 1 and "C3b" in out


def test_f10_a_carry_follows_only_parser_rooted_names():
    files = {"er.py": 'def is_p(c):\n    return c == "pytest"\n',
             "w.py": 'import er\ndef w(c):\n    if c:\n        return "text"\n    return er.is_p(c)\n',
             "k.py": 'import w\ndef g(c):\n    return w.w(c)\n'}
    ks, preds, _ = L.scan_texts(files, toks())
    assert "er.is_p" in preds and "w.w" not in preds and not [k for k in ks if k.startswith("k.py")]
    parser = {"p.py": 'import ast\ndef rd(s):\n    return ast.parse(s), ""\n', "q.py": 'import p\ndef w(s):\n    return p.rd(s)\n'}
    assert {"p.rd", "q.w"} <= L.scan_texts(parser, toks())[1]                              # a parser result still carries


def test_f11_a_deep_chain_is_c7_and_an_unread_effective_base_is_exit_2(tmp_path, run, monkeypatch):
    chain = "x = " + " + ".join('"a"' for _ in range(700)) + "\n"
    # t-2113: the depth is relative to the interpreter's default limit; another test file of the same pytest process (dup_report's main,
    # copy_detector's) leaves `sys.setrecursionlimit(6000)` behind, and then 700 terms are read, not refused (CI 8062800, forge-check)
    kept = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        ks, preds, errs = L.scan_texts({"deep.py": chain}, toks())
    finally:
        sys.setrecursionlimit(kept)
    assert "deep.py" in errs and not ks
    repo = mk(tmp_path)
    assert run(repo, "--raises", "--staged", "--base", "HEAD")[0] == 2                       # no silent HEAD


# ------------------------------------------------------------------------------------------------ round t-2101 (re-review t-2099)
F10_FILES = {"er.py": 'def is_p(c):\n    return c == "pytest"\n',
             "w.py": 'import er\ndef w(c):\n    if c:\n        return "text"\n    return er.is_p(c)\n',
             "k.py": 'import w\ndef g(c):\n    return w.w(c)\n'}
PARSER_FILES = {"p.py": 'import ast\ndef rd(s):\n    return ast.parse(s), ""\n', "q.py": 'import p\ndef w(s):\n    return p.rd(s)\n'}


def test_d1_a_staged_seed_follows_the_same_names_as_the_whole_scan():
    whole_keys, preds, _ = L.scan_texts(F10_FILES, toks())
    infos = [L.analyze_text(p, t, toks()) for p, t in F10_FILES.items()]
    preds2, roots = L.compute_predicates(infos)
    assert preds2 == preds == {"er.is_p"} and roots == set()               # no parser root in this tree
    staged_keys, staged_preds, _ = L.scan_texts(F10_FILES, toks(), seed=preds, roots=roots)
    assert staged_preds == preds and staged_keys == whole_keys             # the stored `predicates` never seed the carry
    infos = [L.analyze_text(p, t, toks()) for p, t in PARSER_FILES.items()]
    assert L.compute_predicates(infos)[1] == {"p.rd", "q.w"}


@pytest.mark.parametrize("files, roots", [(F10_FILES, []), (PARSER_FILES, ["p.rd", "q.w"])])
def test_d1_end_to_end_init_stores_the_roots_and_staged_agrees_with_whole(tmp_path, run, files, roots):
    repo = mk(tmp_path, scripts=files, baseline=False)
    assert run(repo, "--init")[0] == 0
    assert json.loads((repo / L.BASELINE_REL).read_text(encoding="utf-8"))["predicate_roots"] == roots
    commit(repo, "baseline")
    for name in files:                                                    # every script staged: the carry is judged in staged mode
        write(repo, SCRIPTS + name, files[name] + "# touched\n")
    sh(repo, "add", "-A")
    for args in (("--check", "--staged"), ("--check",)):
        code, out = run(repo, *args)
        assert code == 0, (args, out)
    d = json.loads((repo / L.BASELINE_REL).read_text(encoding="utf-8"))      # C6 compares the roots too: a wrong list is red
    d["predicate_roots"] = d["predicate_roots"] + ["zz.ghost"]
    put(repo, d)
    code, out = run(repo, "--check")
    assert code == 1 and "C6" in out and "roots: zz.ghost" in out


def test_d2_a_relabel_through_a_new_key_is_red_beside_an_unrelated_road_raise():
    k_f, k_g, k_h = key("a.py", "f", "compare", ".py"), key("a.py", "g", "compare", ".py"), key("b.py", "h", "compare", ".py")
    base = doc([row(k_f, count=3, kind="road", mech="M1", word=word())])
    w2 = word("a different twelve plus word")
    own = row(k_g, count=3, mech="M1", reason="new reason x")
    road = row(k_h, count=3, kind="road", mech="M1", word=w2)
    res = L.compare_docs(base, doc([own, road]))
    assert [i["type"] for i in reds(res)] == ["budget"], res["items"]
    assert not reds(L.compare_docs(base, doc([road])))                             # control: the road alone, with its word
    assert not reds(L.compare_docs(base, doc([row(k_g, count=3, mech="M1", reason="x", word=w2), road])))   # a new word buys it


def test_d3_the_later_definition_of_a_qualname_takes_its_kind():
    caller = 'import er\ndef g(c):\n    return er.X(c)\n'
    ks, preds, _ = L.scan_texts({"er.py": 'class X:\n    pass\ndef X(n):\n    return n == ".py"\n', "k.py": caller}, toks())
    assert "er.X" in preds and any(k.endswith("k.py|g|predicate-call|er.X") or "|predicate-call|er.X" in k for k in ks)
    ks, preds, _ = L.scan_texts({"er.py": 'def X(n):\n    return n == ".py"\nclass X:\n    pass\n', "k.py": caller}, toks())
    assert "er.X" not in preds and not [k for k in ks if "predicate-call" in k]        # the class wins: no predicate


def test_fork1_a_part_of_a_row_may_move_when_cap_covers_it_the_fields_travel_and_the_total_holds():
    k_f, k_g = key("a.py", "f", "compare", ".py"), key("a.py", "g", "compare", ".py")
    for base_row, part in ((row(k_f, count=2, kind="road", mech="M1", word=word()),
                            row(k_g, kind="road", mech="M1", word=word())),
                           (row(k_f, count=2, kind="road", mech="M1"), row(k_g, kind="road", mech="M1")),
                           (row(k_f, count=2, mech="M1"), row(k_g, mech="M1"))):
        res = L.compare_docs(doc([base_row]), doc([dict(base_row, count=1), part]))
        assert [i["type"] for i in res["items"]] == ["moved"] and not reds(res), base_row
    # the copied word 1 -> 1+1 raises the total: still an added row, and red
    one = row(k_f, count=1, kind="road", mech="M1", word=word())
    assert reds(L.compare_docs(doc([one]), doc([one, row(k_g, kind="road", mech="M1", word=word())])))
    own = row(k_f, count=1, mech="M1")
    assert reds(L.compare_docs(doc([own]), doc([own, row(k_g, mech="M1")])))
    # cap not enough (2 -> 1 + 2) or fields not travelling (another reason on the part): not a move
    big = row(k_f, count=2, mech="M1")
    assert "moved" not in [i["type"] for i in L.compare_docs(doc([big]), doc([dict(big, count=1), row(k_g, count=2, mech="M1")]))["items"]]
    other = row(k_g, mech="M1", reason="another reason")
    assert "moved" not in [i["type"] for i in L.compare_docs(doc([big]), doc([dict(big, count=1), other]))["items"]]
    # the same part in ANOTHER file, with no `moved_from`, is not a move
    far = row(key("b.py", "g", "compare", ".py"), mech="M1")
    assert "moved" not in [i["type"] for i in L.compare_docs(doc([big]), doc([dict(big, count=1), far]))["items"]]


def test_fork2_the_budget_stays_global_and_its_refusal_names_the_case_and_the_way_out():
    k_f = key("a.py", "f", "compare", ".py")
    base = doc([row(k_f, count=1, kind="road", mech="M1", word=word())])
    unrelated = row(key("b.py", "f", "compare", ".py"), mech="M1", reason="an unrelated site")
    res = L.compare_docs(base, doc([unrelated]))
    red = [i for i in reds(res) if i["type"] == "budget"]
    assert red and "global per (form, token)" in red[0]["text"] and "two commits" in red[0]["text"]


def test_fork3_a_syntax_word_counts_only_before_whitespace():
    t = L.Tokens(L.DEFAULT_TOKENS)
    for pat in (r"^\s*(?:async\s+)?def\s+(\w+)", r"^class\s+(\w+)", r"^function\s", r"^(?:class |def )"):
        assert set(t.regex(pat)) & {"def", "class", "function"}, pat
    # whitespace after closing group / alternation characters counts, and EVERY word of the alternation with it (t-2104)
    assert {"def", "class"} <= set(t.regex(r"^\s*(?:async\s+)?(?:def|class)\s+(\w+)"))
    assert {"def", "func", "function"} <= set(t.regex(r"(def|func|function)\s"))
    assert {"def", "function", "func"} <= set(t.regex(r"\b(?:def|function|func|fn|void|public|sub)\b|\b(?:it|test)\s*\("))
    for pat in (r"bug-class):", r"|class|", r"^function\(", r"#include", r"(?:bug-class|x)"):
        assert not set(t.regex(pat)) & {"def", "class", "function", "include"}, pat


def test_fork3_the_live_regexes_blast_radius_and_variant_shape_are_detected_again():
    ks = keys_of('import re\nDEF_RE = re.compile(r"^\\s*(?:async\\s+)?(?:def|class)\\s+([^\\W\\d]\\w*)")\n')
    assert any(k.endswith("regex|def") for k in ks) and any(k.endswith("regex|class") for k in ks)
    src = ('import re\ndef function_span(s):\n    declares = re.compile(r"\\b(?:def|function|func|fn|void|public|private|'
           'protected|static|async|sub)\\b|\\b(?:it|test)\\s*\\(")\n')
    ks = keys_of(src)
    assert [k for k in ks if "function_span|regex|" in k and k.rsplit("|", 1)[1] in ("def", "func", "function")]
    # grammar.py:84 and :287 stay out
    assert not keys_of('import re\nre.compile(r"(bug-class):")') and not keys_of('import re\nre.compile(r"^(a|class|b)$")')


def test_t2104_staged_drops_a_stored_predicate_whose_file_is_rescanned():
    files = {"er.py": 'def is_p(c):\n    return c == "pytest"\n', "k.py": 'import er\ndef g(c):\n    return er.is_p(c)\n'}
    assert "er.is_p" in L.scan_texts(files, toks())[1]
    gone = dict(files, **{"er.py": 'def is_p(c):\n    return c\n'})                 # er.is_p stopped being a predicate
    whole_keys, preds, _ = L.scan_texts(gone, toks())
    assert "er.is_p" not in preds
    for kw in ({"seed": {"er.is_p", "k.g"}}, {"seed": {"er.is_p"}, "roots": {"er.is_p"}}):
        ks, sp, _ = L.scan_texts(gone, toks(), **kw)
        assert sp == preds and ks == whole_keys, kw
    # a file that is NOT rescanned keeps its stored names
    ks, sp, _ = L.scan_texts({"k.py": files["k.py"]}, toks(), seed={"er.is_p"})
    assert "er.is_p" in sp and any("|predicate-call|er.is_p" in k for k in ks)


def test_t2104_c5_a_narrowed_root_is_a_basis_item_and_equal_lists_are_not():
    base, cur = doc([], ["p.rd"], ["p.rd"]), doc([], ["p.rd"], [])
    assert [b["what"] for b in L.compare_docs(base, cur)["basis"]] == ["predicate_root"]
    assert not L.compare_docs(base, base)["basis"]


def test_empty_baseline_is_named_in_the_output(tmp_path, run):
    repo = mk(tmp_path, scripts={"a.py": "x = 1\n"}, rows=[])
    code, out = run(repo, "--check")
    assert code == 0 and "NO rows" in out
    repo2 = mk(tmp_path / "two", baseline=False)
    code, out = run(repo2, "--check")
    assert code == 2 and "missing" in out


def test_usage_errors_are_exit_2(tmp_path, run):
    repo = mk(tmp_path)
    assert run(repo, "--check", "--staged", "--base", "HEAD")[0] == 2
    assert run(repo, "--raises")[0] == 2
    assert L.main(["--check", "--shrink", "--repo", str(repo)]) == 2


if __name__ == "__main__":                       # the DoD's script entry: python -B tools/test_language_sites.py [pytest args]
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider", *sys.argv[1:]]))
