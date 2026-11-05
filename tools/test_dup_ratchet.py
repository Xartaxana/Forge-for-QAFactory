"""Tests for tools/dup_ratchet.py -- the clone ratchet (B-417, t-518).

Keys: K1 clean tree -> 0; K2 a planted clone is red naming both locations and the door; K3 a known clone is
green; K4 moved lines / an edit above / CRLF / BOM stay green and `--update` is byte-identical; K5 a grown
group is red at count+1, green at the exact count; K6 a rename, a move to another file, a reorder stay green;
K7 more than 40 groups are never cut (and a cut report is exit 2); K8 an unreadable file is red and `--update`
refuses; K9 a missing / malformed baseline is exit 2; K10 basis drift is exit 2 (Python drift: green stands,
red is exit 2 naming both); K11 an empty scope is exit 2, a scope absent from the baseline (or the reverse)
is exit 2; K12 a dup_report JSON shape change is exit 2 naming the key; K13 a deleted file or copy is green and
listed, `--update` removes the row; K14 a carried group is green at the row's statement budget and red one
over; K15 a new clone beside a LIVE row is red; K15b a partly edited 3-copy clone is carried only onto its
lost member; K16 a clone dissolving into fragments is carried and DIVERGED is listed; K17 an extended clone
and two runs merged across a gap are red; K18 `--update` is deterministic (another hash seed); K19 the
`--update` listing; K20 the shipped baseline is green on the real tree (skipped while a scope is dirty);
K21 shipped paths are POSIX, relative, no line keys; K23 the CI yaml carries the gate (K22 is in
test_dup_report.py). Plus: `--report`, the EXCLUDES scope, the adversarial copies.
Every fixture is written into tmp_path; no test reads the real tree except K20/K21/K23.
"""
import copy
import itertools
import json
import os
import pathlib
import random
import re
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import dup_ratchet as DRT  # noqa: E402
import dup_report as DR  # noqa: E402
import lint_ratchet as LR  # noqa: E402
import test_lint_ratchet as LRT  # noqa: E402
from test_dup_report import FUNC_A, FUNC_B, SHARED6, put  # noqa: E402

SCRIPT = TOOLS / "dup_ratchet.py"


def big(name="f", edit=None, n=14):
    """A function of n+1 statements, every one different (a distinct callee per line); `edit` {line: prefix}
    renames that line's callee, so two copies differ exactly there."""
    edit = edit or {}
    lines = [f"def {name}(x):"] + [f"    r{i} = {edit.get(i, 'stage')}_{i}(x)" for i in range(1, n + 1)]
    return "\n".join(lines + [f"    return r{n}"]) + "\n"


@pytest.fixture(scope="module")
def outside_git_outcome(tmp_path_factory):
    """What `scope_changes` answers for a folder that is no git tree: ONE real `git status` per module (B-455). Every
    `--update` writes into such a tmp_path and prints the same warning; before this fixture each of ~50 tests paid its own
    `git status` process for it. A list when the folder is somehow inside a tree, else the RuntimeError."""
    folder = tmp_path_factory.mktemp("not_a_repo")
    try:
        return DRT.scope_changes(folder, {"s": (("src/*.py",), ())})
    except RuntimeError as exc:
        return exc


@pytest.fixture
def real_git_status():
    """A test that asks for this one keeps the real `scope_changes` (it inits a repo, or reads the real tree)."""


@pytest.fixture(autouse=True)
def cached_git_status(request, monkeypatch):
    if "real_git_status" in request.fixturenames:
        return
    outcome = request.getfixturevalue("outside_git_outcome")

    def cached(repo, scopes):
        if isinstance(outcome, RuntimeError):
            raise outcome
        return list(outcome)

    monkeypatch.setattr(DRT, "scope_changes", cached)


def ratchet(tmp_path, capsys, *flags, scope="src/*.py"):
    rc = DRT.run(["--repo", str(tmp_path), "--baseline", str(tmp_path / "bl.json"), "--scope", "s=" + scope, *flags])
    cap = capsys.readouterr()
    return rc, cap.out, cap.err


def update(tmp_path, capsys, **kw):
    rc, out, _ = ratchet(tmp_path, capsys, "--update", **kw)
    assert rc == 0, out
    return (tmp_path / "bl.json").read_bytes()


def make(tmp_path, capsys, files):
    """Write the files and record the baseline of that state."""
    put(tmp_path, files)
    return update(tmp_path, capsys)


PAIR = {"src/a.py": big("f"), "src/b.py": big("g")}


def summary(out, scope="s"):
    m = re.search(rf"^dup ratchet: {scope}: (\d+) groups, (\d+) known, (\d+) new, (\d+) grown, (\d+) carried, "
                  rf"(\d+) shrunk/gone \((\d+) diverged\)$", out, re.M)
    assert m, f"no summary line in:\n{out}"
    return tuple(int(v) for v in m.groups())      # groups, known, new, grown, carried, shrunk/gone, diverged


# ---------------------------------------------------------------- the basic verdicts

def test_k1_clean_tree_is_green(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": FUNC_A})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (0, 0, 0, 0, 0, 0, 0)


def test_k2_a_planted_clone_is_red_naming_both_locations_and_the_door(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": FUNC_A})
    put(tmp_path, {"src/b.py": FUNC_B})                      # the plant
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[2] == 1
    assert "src/a.py:1-8 first" in out and "src/b.py:1-8 second" in out
    assert "function, 7 statements, 2 copies" in out
    assert "python tools/dup_ratchet.py --update" in out and "say why in the commit" in out and "call the existing function" in out
    # the twin: take the plant away and it is green again
    (tmp_path / "src" / "b.py").unlink()
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0


def test_k3_a_known_clone_is_green(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": FUNC_A, "src/b.py": FUNC_B})
    rc, out, err = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (1, 1, 0, 0, 0, 0, 0)
    assert re.search(r"s \d+ files in \d+\.\ds", err) and "files in" not in out      # the wall time: stderr only


ADVERSARIAL = {
    "byte copy": FUNC_A,
    "renamed locals": FUNC_B,
    "changed literals": FUNC_A.replace('"ok"', '"other"'),
}


@pytest.mark.parametrize("copy_text", ADVERSARIAL.values(), ids=ADVERSARIAL.keys())
def test_adversarial_copies_of_a_known_clone_stay_red(tmp_path, capsys, copy_text):
    make(tmp_path, capsys, {"src/a.py": FUNC_A, "src/b.py": FUNC_B})
    put(tmp_path, {"src/c.py": copy_text})                    # a third copy, in a file added in the same diff
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[3] == 1 and "3 now, 2 in the baseline" in out


def test_k4_moved_lines_an_edit_above_crlf_and_bom_stay_green_and_update_is_byte_identical(tmp_path, capsys):
    first = make(tmp_path, capsys, {"src/a.py": FUNC_A, "src/b.py": FUNC_B})
    shifted_a = "import os\nVALUE = 3\n\n\n" + FUNC_A
    crlf_bom_b = b"\xef\xbb\xbf" + FUNC_B.replace("\n", "\r\n").encode("utf-8")
    put(tmp_path, {"src/a.py": shifted_a})
    (tmp_path / "src" / "b.py").write_bytes(crlf_bom_b)
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (1, 1, 0, 0, 0, 0, 0)
    assert update(tmp_path, capsys) == first


def test_k5_a_grown_group_is_red_at_count_plus_one_and_green_at_the_exact_count(tmp_path, capsys):
    make(tmp_path, capsys, PAIR)
    put(tmp_path, {"src/c.py": big("h")})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[3] == 1 and "3 now, 2 in the baseline" in out
    (tmp_path / "src" / "c.py").unlink()
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[3] == 0                  # the exact count


def test_k6_a_rename_a_move_to_another_file_and_a_reorder_stay_green(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f") + "\n\n" + FUNC_A, "src/b.py": big("g")})
    put(tmp_path, {"src/a.py": FUNC_A + "\n\n" + big("renamed"), "src/b.py": "", "src/moved.py": big("g")})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (1, 1, 0, 0, 0, 0, 0)


# ---------------------------------------------------------------- the limits of the reader

def many_pairs(count):
    one = "def p{i}(x):\n" + "".join(f"    v{j} = op{{i}}_{j}(x)\n" for j in range(5)) + "    return v4\n"
    return {"src/a.py": "\n\n".join(one.format(i=i) for i in range(count)),
            "src/b.py": "\n\n".join(one.format(i=i).replace(f"def p{i}", f"def q{i}") for i in range(count))}


def test_k7_more_than_40_groups_are_never_cut_and_a_cut_report_is_exit_2(tmp_path, capsys, monkeypatch):
    make(tmp_path, capsys, many_pairs(45))
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[:3] == (45, 45, 0)
    real = DR.analyse
    monkeypatch.setattr(DR, "analyse", lambda repo, paths, ms, w, st, top, wi=False, ex=(), files=None:
                        real(repo, paths, ms, w, st, 40, wi, ex, files))
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and "lists 40 groups but counts 45" in out


def test_the_41st_group_is_red(tmp_path, capsys):
    make(tmp_path, capsys, many_pairs(40))
    put(tmp_path, many_pairs(41))
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[:3] == (41, 40, 1)


def test_k8_an_unreadable_file_is_red_and_update_refuses(tmp_path, capsys):
    before = make(tmp_path, capsys, PAIR)
    put(tmp_path, {"src/broken.py": "def broken(:\n    pass\n"})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and "files that do not parse" in out and "src/broken.py: SyntaxError" in out and LR.DOOR_PARSE in out
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 1 and "--update refused" in out and (tmp_path / "bl.json").read_bytes() == before
    (tmp_path / "src" / "broken.py").unlink()                   # the twin: parsable again
    assert ratchet(tmp_path, capsys)[0] == 0


def test_the_door_of_an_unreadable_file_is_the_lint_ratchets_own_text():
    assert DRT.DOOR_PARSE is LR.DOOR_PARSE and DRT.SCOPES["scripts"] is DR.DEFAULT_PATHS


# ---------------------------------------------------------------- cannot judge: exit 2

def test_k9_a_missing_baseline_is_exit_2_with_the_update_door(tmp_path, capsys):
    put(tmp_path, PAIR)
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and "does not exist" in out and "python tools/dup_ratchet.py --update" in out


def written(tmp_path, capsys):
    make(tmp_path, capsys, PAIR)
    return json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))


MALFORMED = {
    "copies below two": lambda d: d["rows"].__setitem__(0, d["rows"][0] | {"copies": 1, "members": [["src/a.py", "f"]]}),
    "duplicate scope+fingerprint": lambda d: d["rows"].append(copy.deepcopy(d["rows"][0])),
    "a row with first/last": lambda d: d["rows"][0].update({"first": 1, "last": 8}),
    "a member with lines": lambda d: d["rows"][0].__setitem__("members", [["src/a.py", "f", 1], ["src/b.py", "g", 1]]),
    "copies and members disagree": lambda d: d["rows"][0].update({"copies": 3}),
    "an unknown scope": lambda d: d["rows"][0].update({"scope": "nowhere"}),
    "no rows key": lambda d: d.pop("rows"),
    "no basis": lambda d: d.pop("basis"),
}


@pytest.mark.parametrize("damage", MALFORMED.values(), ids=MALFORMED.keys())
def test_k9_a_malformed_baseline_is_exit_2(tmp_path, capsys, damage):
    doc = written(tmp_path, capsys)
    assert ratchet(tmp_path, capsys)[0] == 0                    # the twin: the undamaged baseline is green
    damage(doc)
    (tmp_path / "bl.json").write_text(json.dumps(doc), encoding="utf-8")
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and "malformed" in out and "--update" in out


@pytest.mark.parametrize("text", ["{not json", "[]", "null", ""], ids=["bad json", "a list", "null", "empty file"])
def test_k9_a_baseline_that_is_not_a_document_is_exit_2(tmp_path, capsys, text):
    put(tmp_path, PAIR)
    (tmp_path / "bl.json").write_text(text, encoding="utf-8")
    assert ratchet(tmp_path, capsys)[0] == 2


def test_k10_basis_drift_is_exit_2_with_the_update_door(tmp_path, capsys):
    doc = written(tmp_path, capsys)
    for key, value in (("normalisation", 99), ("window", 7), ("min_statements", 4), ("strict", True), ("with_imports", True)):
        drifted = copy.deepcopy(doc)
        drifted["basis"][key] = value
        (tmp_path / "bl.json").write_text(json.dumps(drifted), encoding="utf-8")
        rc, out, _ = ratchet(tmp_path, capsys)
        assert rc == 2 and key in out and "--update" in out, key


def test_k10_python_drift_a_green_result_stands_and_a_red_one_is_exit_2_naming_both(tmp_path, capsys):
    doc = written(tmp_path, capsys)
    doc["basis"]["python"] = "2.7"
    (tmp_path / "bl.json").write_text(json.dumps(doc), encoding="utf-8")
    assert ratchet(tmp_path, capsys)[0] == 0
    put(tmp_path, {"src/c.py": big("h")})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and "Python 2.7" in out and DRT.python_minor() in out and "3 now, 2 in the baseline" in out


def test_k11_an_empty_scope_is_exit_2_naming_it_and_a_clone_free_scope_is_green(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": FUNC_A})
    rc, out, _ = ratchet(tmp_path, capsys, scope="nothing/*.py")
    assert rc == 2 and "scope `s` matched no files" in out
    rc, out, _ = ratchet(tmp_path, capsys, "--update", scope="nothing/*.py")
    assert rc == 2
    assert ratchet(tmp_path, capsys)[0] == 0                    # files read, no groups: green
    make(tmp_path, capsys, PAIR)
    (tmp_path / "src" / "a.py").unlink()
    (tmp_path / "src" / "b.py").unlink()                        # the same scope definition, now matching nothing
    (tmp_path / "src" / "keep.txt").write_text("not python", encoding="utf-8")
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and "scope `s` matched no files" in out


def test_k11_a_scope_absent_from_the_baseline_or_from_the_run_is_exit_2(tmp_path, capsys):
    make(tmp_path, capsys, PAIR)
    argv = ["--repo", str(tmp_path), "--baseline", str(tmp_path / "bl.json")]
    assert DRT.run([*argv, "--scope", "s=src/*.py", "--scope", "t=src/*.py"]) == 2
    assert "scopes differ" in capsys.readouterr().out
    assert DRT.run([*argv, "--scope", "t=src/*.py"]) == 2
    assert "scopes differ" in capsys.readouterr().out
    assert DRT.run([*argv, "--scope", "s=src/a.py"]) == 2         # the same name, another definition
    assert "defined differently" in capsys.readouterr().out
    assert DRT.run([*argv, "--scope", "s=src/*.py"]) == 0         # the twin


SHAPE_DAMAGE = {
    "fingerprint_basis": lambda rep: rep.pop("fingerprint_basis"),
    "totals.groups": lambda rep: rep["totals"].pop("groups"),
    "unreadable": lambda rep: rep.pop("unreadable"),
    "groups[].fingerprint": lambda rep: rep["groups"][0].pop("fingerprint"),
    "groups[].locations[].in": lambda rep: rep["groups"][0]["locations"][0].pop("in"),
}


@pytest.mark.parametrize("key", SHAPE_DAMAGE, ids=list(SHAPE_DAMAGE))
def test_k12_a_dup_report_shape_change_is_exit_2_naming_the_key(tmp_path, capsys, monkeypatch, key):
    make(tmp_path, capsys, PAIR)
    real = DR.analyse

    def damaged(*args, **kwargs):
        rep = real(*args, **kwargs)
        SHAPE_DAMAGE[key](rep)
        return rep

    monkeypatch.setattr(DR, "analyse", damaged)
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 2 and f"lacks `{key}`" in out and "nothing was judged" in out


def test_k12_the_real_dup_report_json_carries_every_key_the_reader_needs(tmp_path, capsys):
    put(tmp_path, PAIR)
    assert DR.run(["--repo", str(tmp_path), "--paths", "src/*.py", "--json", "--top", "1000"]) == 0
    rep = json.loads(capsys.readouterr().out)
    DRT.validate_report(rep, "s")                                # raises Cannot on a missing key
    assert rep["fingerprint_basis"] == {"normalisation": DR.NORMALISATION}
    assert [g["fingerprint"] for g in rep["groups"]] and "exclude" not in rep["options"]


def test_k13_a_deleted_file_is_gone_a_deleted_copy_is_shrunk_and_update_removes_the_rows(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f"), "src/b.py": big("g"), "src/c.py": big("h"), "src/x.py": FUNC_A, "src/y.py": FUNC_B})
    (tmp_path / "src" / "c.py").unlink()                          # 3 copies -> 2: shrunk
    (tmp_path / "src" / "y.py").unlink()                          # the pair loses a file: gone
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (1, 1, 0, 0, 0, 2, 0)
    assert "shrunk in s" in out and "2 now, 3 in the baseline" in out
    assert "gone from s" in out and "src/y.py" in out
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0 and "1 rows (0 added, 1 removed, 0 grew)" in out
    assert len(json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))["rows"]) == 1
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[5] == 0                       # tightened: nothing listed any more


# ---------------------------------------------------------------- carrying: identity survives an edit only within the old code

def test_k14_a_carried_group_is_green_at_the_budget_and_red_one_over(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f"), "src/b.py": big("g")})        # 15 statements x 2
    put(tmp_path, {"src/a.py": big("f", {5: "alt"}), "src/b.py": big("g", {5: "alt"})})   # edited alike: 15 statements
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[2:5] == (0, 0, 1) and "carried in s" in out and "15 statements" in out
    put(tmp_path, {"src/a.py": big("f", {5: "alt"}, n=15), "src/b.py": big("g", {5: "alt"}, n=15)})  # 16: one over
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[2:5] == (1, 0, 0) and "function, 16 statements, 2 copies" in out


def sharing_pair(name_a, name_b):
    """Two different functions that share one 6-statement fragment (and nothing else): a fragment group."""
    return ("def %s(x):\n    x = start_one()\n" % name_a + SHARED6 + "    return f\n",
            "def %s(x):\n    x = other_start(1, 2)\n" % name_b + SHARED6 + "    emit(f)\n    log_done()\n")


def test_k15_a_new_clone_beside_a_live_row_is_red_even_inside_the_rows_places_and_budget(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f"), "src/b.py": big("f")})        # the row: f x2, 15 statements
    # the new fragment lives in a SECOND function that is also named f (the same `in`): its members are a
    # sub-multiset of the row's and its 6 statements fit the budget -- only "a live row is never a
    # fallback" keeps it red
    tail_a, tail_b = sharing_pair("f", "f")
    put(tmp_path, {"src/a.py": big("f") + "\n\n" + tail_a, "src/b.py": big("f") + "\n\n" + tail_b})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and "fragment, 6 statements, 2 copies" in out and summary(out)[1:5] == (1, 1, 0, 0)


def three_copies(c_edit, tail=False):
    """f x3 (20 statements); c is edited on `c_edit`; a and b get a second function after f: with `tail` it is
    named f too (the same `in` as the row's members), else g_a / g_b -- the two share a fresh 6-statement fragment."""
    tail_a, tail_b = sharing_pair("f", "f") if tail else sharing_pair("g_a", "g_b")
    return {"src/a.py": big("f", n=19) + "\n\n" + tail_a, "src/b.py": big("f", n=19) + "\n\n" + tail_b,
            "src/c.py": big("f", c_edit, n=19)}


EDIT_MIDDLE = {i: "alt" for i in range(8, 14)}                    # c: statements 8-13 differ; 7 + 7 statements stay shared


def test_k15b_a_partly_edited_clone_is_carried_onto_its_lost_member_only(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f", n=19), "src/b.py": big("f", n=19), "src/c.py": big("f", n=19)})
    put(tmp_path, {"src/c.py": big("f", EDIT_MIDDLE, n=19)})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[1:6] == (1, 0, 0, 2, 1) and "carried in s" in out and "shrunk in s" in out
    # a new fragment between the two UNEDITED copies, in other functions (g_a, g_b): not the row's members -> red
    put(tmp_path, three_copies(EDIT_MIDDLE))
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[2] == 1 and "fragment, 6 statements, 2 copies" in out


def test_k15b_the_lost_member_condition_decides_when_every_other_condition_holds(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f", n=19), "src/b.py": big("f", n=19), "src/c.py": big("f", n=19)})
    put(tmp_path, three_copies(EDIT_MIDDLE, tail=True))           # the fragment's members ARE (a, f) and (b, f); 14 + 6 <= 20
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[2] == 1 and "fragment, 6 statements, 2 copies" in out
    assert "carried in s" in out                                  # the two 7-statement fragments are still carried


def test_k16_a_clone_dissolving_into_fragments_is_carried_and_diverged_is_listed(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f"), "src/b.py": big("f")})
    put(tmp_path, {"src/a.py": big("f", {8: "alt_a"}), "src/b.py": big("f", {8: "alt_b"})})
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out) == (2, 0, 0, 0, 2, 1, 1)
    assert "diverged in s (green; changed in one place? check the other copy)" in out
    assert "src/a.py f" in out and "src/b.py f" in out           # the row's members, no line


def nested_function(name, last):
    """13 statements: five calls, an `if` with a 6-statement body (dup_report finds that body as a fragment of its
    own), and a last call that makes two copies differ."""
    return (f"def {name}(x):\n" + "".join(f"    r{i} = stage_{i}(x)\n" for i in range(1, 6)) + "    if x:\n"
            + "".join(f"        q{i} = inner_{i}(x)\n" for i in range(1, 7)) + f"    {last}(x)\n")


def test_f1_an_edit_in_one_copy_of_a_clone_with_a_nested_block_is_green_and_not_charged_twice(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": nested_function("f", "final"), "src/b.py": nested_function("f", "final")})
    put(tmp_path, {"src/b.py": nested_function("f", "other")})    # the last line of ONE copy
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0, out
    assert summary(out) == (1, 0, 0, 0, 1, 1, 1)                  # the 12-statement top fragment is carried; the nested 6 is not a group of its own
    assert "nested in s" in out and "fragment, 6 statements, 2 copies" in out and "diverged in s" in out


def seven_shared(name, lo):
    """pre / t_lo..t7 / post: copies with lo=1 share t1..t7, one with lo=2 shares only t2..t7."""
    return (f"def f(x):\n    pre_{name}()\n" + "".join(f"    t{i} = step_{i}(x)\n" for i in range(lo, 8))
            + f"    post_{name}()\n")


def test_f2_a_deletion_that_merges_two_fragment_rows_into_one_longer_run_is_a_shrink_not_red(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": seven_shared("a", 1), "src/b.py": seven_shared("b", 1),
                            "src/c.py": seven_shared("c", 1), "src/d.py": seven_shared("d", 2)})   # rows: 6x3 and 6x4
    put(tmp_path, {"src/d.py": "def f(x):\n    helper(x)\n"})   # d's copy replaced by a call: t1..t7 is now ONE run of 7 x 3
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0, out
    assert summary(out) == (1, 0, 0, 0, 1, 2, 2) and "fragment, 7 statements, 3 copies" in out
    put(tmp_path, {"src/e.py": seven_shared("e", 1)})             # the twin: a fourth copy in a new file is no shrink
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out)[2] == 1 and "fragment, 7 statements, 4 copies" in out


def test_f3_the_places_condition_a_new_clone_in_other_functions_is_red_under_a_dissolved_row(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f", n=19), "src/b.py": big("f", n=19)})       # the row: 20 statements x 2
    tail_a, tail_b = sharing_pair("g_a", "g_b")
    differently = {"src/a.py": big("f", {i: "alt_a" for i in range(8, 14)}, n=19) + "\n\n" + tail_a,
                   "src/b.py": big("f", {i: "alt_b" for i in range(8, 14)}, n=19) + "\n\n" + tail_b}
    put(tmp_path, differently)       # 14 statements carried (7 + 7), 6 left in the budget; the new 6-statement clone fits it
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and summary(out) == (3, 0, 1, 0, 2, 1, 1)
    assert "fragment, 6 statements, 2 copies" in out and "src/a.py:" in out and "diverged in s" in out


def test_the_baseline_rows_are_read_sorted_so_the_file_order_never_decides(tmp_path, capsys):
    doc = written_pairs(tmp_path, capsys)
    ordered = [(r["scope"], r["kind"], r["fingerprint"]) for r in doc["rows"]]
    assert len(ordered) == 2
    doc["rows"].reverse()
    (tmp_path / "bl.json").write_text(json.dumps(doc), encoding="utf-8")
    loaded = DRT.load_baseline(tmp_path / "bl.json")
    assert [(r.scope, r.kind, r.fingerprint) for r in loaded.rows] == sorted(ordered)
    assert ratchet(tmp_path, capsys)[0] == 0


def clone_pair_files(k, prefix="src"):
    """The k-th clone pair: two functions that differ from every other pair's on every line (so n pairs = n function rows)."""
    edit = {i: f"pair{k}" for i in range(1, 15)}
    return {f"{prefix}/p{k}a.py": big("f", edit), f"{prefix}/p{k}b.py": big("g", edit)}


def row_orders(n):
    """Every order of n rows up to 3 (all 6 at n=3); beyond that the reverse and four seeded shuffles."""
    if n <= 3:
        return list(itertools.permutations(range(n)))
    return [list(range(n))[::-1]] + [random.Random(seed).sample(range(n), n) for seed in range(4)]


@pytest.mark.parametrize("n_rows", [0, 1, 3, 5])
def test_k24_a_baseline_in_any_row_order_gives_the_same_verdict_and_the_same_output(tmp_path, capsys, n_rows):
    """B-455 / critic t-534 F-5: `load_baseline` sorts with the key `--update` writes; the verdict is red (a NEW pair
    planted after the baseline), so the output carries a listing to compare. At 0, 1 and n rows."""
    files = {"src/clean.py": FUNC_A}
    for k in range(n_rows):
        files |= clone_pair_files(k)
    make(tmp_path, capsys, files)
    doc = json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))
    assert len(doc["rows"]) == n_rows
    put(tmp_path, clone_pair_files(99))                                          # NEW: no row accounts for it
    results = set()
    for order in row_orders(n_rows):
        shuffled = dict(doc, rows=[doc["rows"][i] for i in order])
        (tmp_path / "bl.json").write_text(json.dumps(shuffled), encoding="utf-8")
        loaded = DRT.load_baseline(tmp_path / "bl.json")
        assert [(r.scope, r.kind, r.fingerprint) for r in loaded.rows] == sorted(
            (r["scope"], r["kind"], r["fingerprint"]) for r in doc["rows"])          # the key --update writes them in
        rc, out, _ = ratchet(tmp_path, capsys)
        results.add((rc, out))
    assert len(results) == 1
    (rc, out), = results
    assert rc == 1 and summary(out)[:3] == (n_rows + 1, n_rows, 1)


def test_k24_a_row_twice_in_the_baseline_is_exit_2_whatever_the_order(tmp_path, capsys):
    """Today's behaviour, named (B-455): a duplicated row is a malformed baseline, never first-fit'd and never merged."""
    make(tmp_path, capsys, clone_pair_files(0) | clone_pair_files(1))
    doc = json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))
    first, second = doc["rows"]
    for rows in ([first, first, second], [first, second, first], [second, first, first]):
        (tmp_path / "bl.json").write_text(json.dumps(dict(doc, rows=rows)), encoding="utf-8")
        rc, out, _ = ratchet(tmp_path, capsys)
        assert rc == 2 and "appears twice" in out and "is malformed" in out


GOLDEN_REPORT = """# Duplicate code report

- paths: `src/*.py`
- options: min-statements 5, window 6, strict no, imports excluded, top 2
- files read: 4
- files unreadable: 1
- functions: 4
- clone groups: 2 (2 function, 0 fragment), shown 2
- groups dropped as lying inside a larger function clone: 1
- duplicated lines: 48 of 48 (100.0%)

## Unreadable files

- `src/bad.py`: SyntaxError: invalid syntax (line 1)

## G1 function: 15 statements, 16 lines, 2 copies

- `src/a.py:1-16` f
- `src/b.py:1-16` g

## G2 function: 7 statements, 8 lines, 2 copies

- `src/c.py:1-8` first
- `src/d.py:1-8` second

"""


def test_k25_resolve_files_runs_once_per_scope_and_the_report_is_the_golden_one(tmp_path, monkeypatch, capsys):
    """B-455: `analyse_scopes` resolves the files once and hands the list to `analyse`; the output is unchanged (the golden
    text was produced by the code BEFORE the change, on this same tree)."""
    put(tmp_path, {"src/a.py": big("f"), "src/b.py": big("g"), "src/c.py": FUNC_A, "src/d.py": FUNC_B, "src/bad.py": "def (:\n",
                   "lib/x.py": FUNC_A, "lib/y.py": FUNC_B})
    calls = []
    real = DR.resolve_files

    def counting(repo, patterns, exclude=()):
        calls.append(tuple(patterns))
        return real(repo, patterns, exclude)

    monkeypatch.setattr(DR, "resolve_files", counting)
    out_dir = tmp_path / "ci-out"
    DRT.run(["--repo", str(tmp_path), "--baseline", str(tmp_path / "bl.json"), "--scope", "s=src/*.py", "--scope", "t=lib/*.py",
             "--report", str(out_dir)])
    capsys.readouterr()
    assert calls == [("src/*.py",), ("lib/*.py",)]                                # two scopes, two resolutions, not four
    assert (out_dir / "dup-report-s.md").read_bytes().decode("utf-8") == GOLDEN_REPORT


def test_k25_analyse_given_the_files_reads_those_and_none_given_resolves_them(tmp_path):
    put(tmp_path, {"src/a.py": big("f"), "src/b.py": big("g"), "src/c.py": big("h")})
    both = DR.analyse(tmp_path, ("src/*.py",), 5, 6, False, 40)
    assert both["totals"]["files_read"] == 3 and both == DR.analyse(tmp_path, ("src/*.py",), 5, 6, False, 40, False, (),
                                                                       ["src/a.py", "src/b.py", "src/c.py"])
    two = DR.analyse(tmp_path, ("src/*.py",), 5, 6, False, 40, False, (), ["src/a.py", "src/b.py"])
    assert two["totals"]["files_read"] == 2                                       # the list given is the list read
    assert DR.analyse(tmp_path, ("src/*.py",), 5, 6, False, 40, False, (), [])["totals"]["files_read"] == 0   # [] is not None


def test_k26_one_git_status_call_through_gitcmd_and_its_output_parsed(monkeypatch, tmp_path, real_git_status):
    seen = []

    def fake(root, *args, **kw):
        seen.append((root, args, kw))
        return 0, b' M src/a.py\n?? src/new one.py\nR  old.py -> src/moved.py\n M "quoted.py"\n', b""

    monkeypatch.setattr(DRT.gitcmd, "git", fake)
    changes = DRT.scope_changes(tmp_path, {"s": (("src/*.py",), ("src/t_*.py",))})
    assert len(seen) == 1 and seen[0][0] == tmp_path and seen[0][2] == {"stderr": True}
    assert seen[0][1] == ("status", "--porcelain", "--untracked-files=all", "--", ":(glob)src/*.py", ":(exclude,glob)src/t_*.py")
    assert changes == ["src/a.py", "src/new one.py", "src/moved.py", "quoted.py"]
    monkeypatch.setattr(DRT.gitcmd, "git", lambda *a, **k: (128, b"", b"fatal: not a git repository\n"))
    with pytest.raises(RuntimeError, match=r"^git status failed: fatal: not a git repository$"):
        DRT.status_changes(tmp_path, ["src"])
    monkeypatch.setattr(DRT.gitcmd, "git", lambda *a, **k: (-1, b"", b"[WinError 2] no git"))
    with pytest.raises(RuntimeError, match=r"^git status unavailable: \[WinError 2\] no git$"):
        DRT.status_changes(tmp_path, ["src"])


def written_pairs(tmp_path, capsys):
    make(tmp_path, capsys, {"src/a.py": big("f"), "src/b.py": big("g"), "src/c.py": FUNC_A, "src/d.py": FUNC_B})
    return json.loads((tmp_path / "bl.json").read_text(encoding="utf-8"))


def test_k17_an_extended_clone_and_two_runs_merged_across_a_gap_are_red(tmp_path, capsys):
    shared_p = "".join(f"    p{i} = first_{i}(x)\n" for i in range(6))
    shared_q = "".join(f"    q{i} = second_{i}(x)\n" for i in range(6))

    def mk(gap_a, gap_b):
        return {"src/a.py": "def a(x):\n    pre_a()\n" + shared_p + f"    gap_{gap_a}(x)\n" + shared_q + "    post_a()\n",
                "src/b.py": "def b(x):\n    pre_b(1)\n" + shared_p + f"    gap_{gap_b}(x)\n" + shared_q + "    post_b(2)\n"}

    make(tmp_path, capsys, mk("one", "two"))                      # two 6-statement runs, apart
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 0 and summary(out)[:3] == (2, 2, 0)
    put(tmp_path, mk("same", "same"))                             # the gap closes: one 13-statement run
    rc, out, _ = ratchet(tmp_path, capsys)
    assert rc == 1 and "fragment, 13 statements, 2 copies" in out and summary(out)[2] == 1


# ---------------------------------------------------------------- --update: determinism and its listing

def test_k18_update_is_deterministic_also_under_another_hash_seed(tmp_path):
    put(tmp_path, {"src/a.py": big("f"), "src/b.py": big("g"), "src/c.py": FUNC_A, "src/d.py": FUNC_B})

    def once(seed, name):
        env = dict(os.environ, PYTHONHASHSEED=str(seed))
        r = subprocess.run([sys.executable, str(SCRIPT), "--update", "--repo", str(tmp_path), "--scope", "s=src/*.py",
                            "--baseline", str(tmp_path / name)], capture_output=True, env=env)
        assert r.returncode == 0, r.stdout + r.stderr
        return (tmp_path / name).read_bytes()

    first, second, third = once(1, "one.json"), once(1, "two.json"), once(12345, "three.json")
    assert first == second == third and b"\r" not in first and first.endswith(b"\n")
    assert str(tmp_path).encode() not in first


def test_k19_the_update_listing_names_every_added_and_grown_row(tmp_path, capsys):
    put(tmp_path, PAIR)
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0 and "baseline written: 1 rows (1 added, 0 removed, 0 grew)" in out
    assert "  added: s" in out and "src/a.py:1-16 f" in out and "src/b.py:1-16 g" in out
    put(tmp_path, {"src/c.py": big("h"), "src/d.py": FUNC_A, "src/e.py": FUNC_B})
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0 and "baseline written: 2 rows (1 added, 0 removed, 1 grew)" in out
    assert "  grew: s (2 -> 3 copies)" in out and "  added: s" in out


def git(tmp_path, *args):
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   check=True, capture_output=True)


def test_update_warns_about_every_uncommitted_change_in_a_scope_and_only_those(tmp_path, capsys, real_git_status):
    put(tmp_path, PAIR | {"notes/readme.py": "x = 1\n"})
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "first")
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0 and "warning" not in out                       # a clean tree prints nothing
    put(tmp_path, {"src/a.py": big("f") + "# touched\n", "src/new.py": FUNC_A, "notes/readme.py": "x = 2\n"})
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0
    assert "warning: uncommitted change in a scope: src/a.py" in out
    assert "warning: uncommitted change in a scope: src/new.py" in out
    assert "notes/readme.py" not in out


def test_update_outside_a_git_tree_says_it_could_not_look(tmp_path, capsys, real_git_status):
    put(tmp_path, PAIR)
    rc, out, _ = ratchet(tmp_path, capsys, "--update")
    assert rc == 0 and "warning: git status" in out and "were not looked for" in out


# ---------------------------------------------------------------- the real scopes, the report, the shipped files

def default_scope_repo(tmp_path, tools_files):
    return put(tmp_path, {"ai-packages/qa-factory/scripts/only.py": FUNC_A} | tools_files)


def test_the_tools_scope_leaves_out_tools_tests_and_the_scripts_scope_does_not(tmp_path, capsys):
    default_scope_repo(tmp_path, {"tools/test_a.py": FUNC_A, "tools/test_b.py": FUNC_B, "tools/real.py": FUNC_A})
    rc = DRT.run(["--repo", str(tmp_path), "--update"])
    out = capsys.readouterr().out
    assert rc == 0 and "baseline written: 0 rows" in out          # the tests' copies are not counted; only.py and real.py are in different scopes
    doc = json.loads((tmp_path / "tools" / "dup-baseline.json").read_text(encoding="utf-8"))
    assert doc["scopes"] == {"scripts": {"paths": ["ai-packages/qa-factory/scripts/*.py"], "exclude": []},
                             "tools": {"paths": ["tools/*.py"], "exclude": ["tools/test_*.py"]}}
    put(tmp_path, {"tools/other.py": FUNC_B})                     # a real tools copy next to real.py: a clone
    rc = DRT.run(["--repo", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1 and "tools/real.py" in out and "tools/other.py" in out and "tools/test_a.py" not in out
    assert summary(out, "tools")[2] == 1 and summary(out, "scripts")[:3] == (0, 0, 0)


def test_report_writes_a_markdown_per_scope_before_any_judgement_even_without_a_baseline(tmp_path, capsys):
    default_scope_repo(tmp_path, {"tools/a.py": FUNC_A, "tools/b.py": FUNC_B})
    out_dir = tmp_path / "ci-out"
    rc = DRT.run(["--repo", str(tmp_path), "--report", str(out_dir)])
    assert rc == 2 and "does not exist" in capsys.readouterr().out    # no baseline: cannot judge -- the reports exist all the same
    scripts_md = (out_dir / "dup-report-scripts.md").read_text(encoding="utf-8")
    tools_md = (out_dir / "dup-report-tools.md").read_text(encoding="utf-8")
    assert scripts_md.startswith("# Duplicate code report") and tools_md.startswith("# Duplicate code report")
    assert "- clone groups: 1 (1 function, 0 fragment), shown 1" in tools_md and "top 1" in tools_md
    assert "No clone groups found." in scripts_md and "\r" not in tools_md
    assert DRT.run(["--repo", str(tmp_path), "--update"]) == 0       # --report composes with the judgement as well
    capsys.readouterr()
    assert DRT.run(["--repo", str(tmp_path), "--report", str(out_dir)]) == 0


def test_a_bad_scope_argument_is_exit_2(tmp_path, capsys):
    assert DRT.run(["--repo", str(tmp_path), "--scope", "nogob"]) == 2
    assert "NAME=GLOB" in capsys.readouterr().out
    assert DRT.run(["--repo", str(tmp_path / "missing")]) == 2
    assert DRT.run(["--no-such-option"]) == 2


def real_tree_dirty() -> str:
    reason = LRT._package_tree_dirty()                            # the lint ratchet's own skip, reused (A10)
    if reason:
        return reason
    scopes = {name: (paths, DRT.EXCLUDES.get(name, ())) for name, paths in DRT.SCOPES.items()}
    try:
        changes = DRT.scope_changes(REPO, scopes)
    except RuntimeError as exc:
        return str(exc)
    return f"uncommitted change in a scope: {changes[0]}" if changes else ""


def test_k20_the_shipped_baseline_is_green_on_the_real_tree(capsys, real_git_status):
    reason = real_tree_dirty()
    if reason:
        pytest.skip("K20 skipped: " + reason + "; the integrator regenerates tools/dup-baseline.json with --update at the commit")
    rc = DRT.run(["--check"])                                     # never a byte comparison: a shrink is green and must stay green
    out = capsys.readouterr().out
    assert rc == 0, out


def test_k21_shipped_paths_are_posix_and_relative_with_no_line_keys():
    doc = json.loads((TOOLS / "dup-baseline.json").read_text(encoding="utf-8"))
    assert doc["rows"], "the shipped baseline has no rows"
    for r in doc["rows"]:
        assert not ({"first", "last"} & set(r)), r
        for path, _ in r["members"]:
            assert "\\" not in path and not path.startswith("/") and not (len(path) > 1 and path[1] == ":"), path
    for d in doc["scopes"].values():
        assert all("\\" not in p for p in d["paths"] + d["exclude"])
    assert (TOOLS / "dup-baseline.json").read_bytes().endswith(b"\n")       # LF on write (K18); a Windows checkout may show CRLF


# K23 (the CI yaml carries the gate in forge-check and the report in package-full) lives in tools/test_ci_layout.py since
# GM1-5: that file is the one place that judges the jobs of .gitlab-ci.yml.
