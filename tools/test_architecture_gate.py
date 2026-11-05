"""Tests for tools/architecture_gate.py -- the commit-msg gate of the architecture rule (F6-29) and of the
`judgment:` line (D-0060, spec t-1765 node A5; built as architecture_gate_next.py, moved onto the live path by the Lead).

The gate runs against a throw-away git repository (the staged paths come from `git diff --cached`),
the pure decide() is also pinned directly."""
import json
import pathlib
import re
import subprocess
import sys

import pytest

import architecture_gate as ag

TOOLS = pathlib.Path(__file__).resolve().parent
SCRIPT = TOOLS / "architecture_gate.py"

INDEX = """# Architecture invariants - index

## A. First
- AR-1 — One
- AR-2 — Two
- AR-3 — Three

## B. Second
- AR-10 — Ten
"""
PKG = "ai-packages/qa-factory/scripts/x.py"
J = "\njudgment: none -- t\n"      # the line every old passing message now also carries


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture()
def repo(tmp_path):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    git(root, "init", "-q")
    (root / "docs" / "ARCHITECTURE_INDEX.md").write_text(INDEX, encoding="utf-8", newline="\n")
    return root


def stage(repo, rel):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n", encoding="utf-8")
    git(repo, "add", "--", rel)


def gate(repo, message, judgment=True):
    msg = repo / "COMMIT_EDITMSG"
    if judgment and "judgment:" not in message:
        message = message.rstrip("\r\n") + J
    msg.write_bytes(message.encode("utf-8"))
    return subprocess.run([sys.executable, str(SCRIPT), str(msg)], cwd=repo, capture_output=True,
                          text=True, encoding="utf-8")


def test_package_path_and_no_line_is_refused_with_the_whole_refusal(repo):
    stage(repo, PKG)
    r = gate(repo, "F6-1: change a script\n\nbody text\n")
    assert r.returncode == 1
    assert PKG in r.stderr and "no `architecture:` line" in r.stderr
    assert "architecture: AR-n[, AR-m] -- <how each is kept>" in r.stderr
    assert "architecture: none -- <reason" in r.stderr
    assert "AR-1, AR-2, AR-3, AR-10" in r.stderr and "Door:" in r.stderr
    print(r.stderr)


def test_known_id_passes(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: AR-3 -- kept: the test runs\n")
    assert r.returncode == 0 and r.stderr == ""


def test_several_known_ids_pass(repo):
    stage(repo, PKG)
    assert gate(repo, "x\n\narchitecture: AR-1, AR-10 -- both kept by one reader\n").returncode == 0


def test_unknown_id_is_named(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: AR-99 -- kept\n")
    assert r.returncode == 1 and "AR-99" in r.stderr and "unknown invariant id" in r.stderr


def test_none_with_a_reason_passes(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: none -- the changelog fragment only\n")
    assert r.returncode == 0 and r.stderr == ""


@pytest.mark.parametrize("line", ["architecture: none --", "architecture: none --   ", "architecture: none",
                                  "architecture: AR-3 --", "architecture: AR-3", "architecture: AR-3 — kept"])
def test_empty_reason_or_missing_dashes_is_refused(line):
    code, text = ag.decide("x\n\n" + line + "\n", [PKG], INDEX)
    assert code == 1 and "Expected, as its own line" in text


def test_none_with_an_empty_reason_is_refused_end_to_end(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: none --\n")
    assert r.returncode == 1 and "no reason after the dashes" in r.stderr


@pytest.mark.parametrize("ids", ["ar-3", "AR3", "AR-03x", "none, AR-3", "AR-3,, AR-1", "AR-"])
def test_ids_are_exact(ids):
    code, text = ag.decide("x\n\narchitecture: %s -- kept\n" % ids, [PKG], INDEX)
    assert code == 1, ids
    assert "not an invariant id" in text or "unknown invariant id" in text


def test_no_package_path_needs_no_line_and_is_silent(repo):
    stage(repo, "tools/other.py")
    r = gate(repo, "plain message\n")
    assert r.returncode == 0 and r.stdout == "" and r.stderr == ""


def test_no_package_path_with_the_index_missing_is_untouched(repo):
    (repo / "docs" / "ARCHITECTURE_INDEX.md").unlink()
    stage(repo, "docs/other.md")
    assert gate(repo, "plain message\n").returncode == 0


def test_index_missing_names_the_generator(repo):
    (repo / "docs" / "ARCHITECTURE_INDEX.md").unlink()
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: none -- a reason\n")
    assert r.returncode == 1 and "python tools/architecture_index.py" in r.stderr and "missing" in r.stderr


def test_index_with_no_ids_is_refused(repo):
    (repo / "docs" / "ARCHITECTURE_INDEX.md").write_text("# nothing\n", encoding="utf-8")
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: none -- a reason\n")
    assert r.returncode == 1 and "python tools/architecture_index.py" in r.stderr


def test_changelog_fragment_alone_still_needs_the_line(repo):
    stage(repo, "ai-packages/qa-factory/changelog.d/F6-29.md")
    assert gate(repo, "x\n").returncode == 1
    assert gate(repo, "x\n\narchitecture: none -- the changelog fragment only\n").returncode == 0


def commit(repo, message="c"):
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--no-verify", "-m", message)


def test_a_rename_out_of_the_package_needs_the_line(repo):
    stage(repo, PKG)
    commit(repo)
    (repo / "attic").mkdir()
    git(repo, "mv", PKG, "attic/x.py")
    r = gate(repo, "move it out\n")
    assert r.returncode == 1 and PKG in r.stderr and "no `architecture:` line" in r.stderr
    assert gate(repo, "move it out\n\narchitecture: none -- the file leaves the package\n").returncode == 0


def test_a_rename_into_the_package_needs_the_line(repo):
    stage(repo, "attic/y.py")
    commit(repo)
    (repo / "ai-packages" / "qa-factory").mkdir(parents=True)
    git(repo, "mv", "attic/y.py", "ai-packages/qa-factory/y.py")
    r = gate(repo, "move it in\n")
    assert r.returncode == 1 and "ai-packages/qa-factory/y.py" in r.stderr
    assert gate(repo, "move it in\n\narchitecture: AR-1 -- kept\n").returncode == 0


def test_a_deletion_of_a_package_file_needs_the_line(repo):
    stage(repo, PKG)
    commit(repo)
    git(repo, "rm", "-q", "--", PKG)
    r = gate(repo, "drop it\n")
    assert r.returncode == 1 and PKG in r.stderr


def test_a_rename_inside_other_paths_is_silent(repo):
    stage(repo, "tools/a.py")
    commit(repo)
    git(repo, "mv", "tools/a.py", "tools/b.py")
    assert gate(repo, "plain\n").returncode == 0


def merge_in_progress(repo):
    """A repo with a clean `git merge --no-ff --no-commit side` under way: MERGE_HEAD exists and the
    package file of `side` is staged."""
    stage(repo, "tools/base.py")
    commit(repo)
    git(repo, "checkout", "-q", "-b", "side")
    stage(repo, PKG)
    commit(repo, "side adds the package file")
    git(repo, "checkout", "-q", "-")
    stage(repo, "tools/main-only.py")
    commit(repo, "main moves on")
    git(repo, "merge", "-q", "--no-ff", "--no-commit", "side")


def test_a_merge_commit_is_exempt_and_a_plain_commit_is_not(repo):
    merge_in_progress(repo)
    r = gate(repo, "Merge branch 'side'\n")
    assert r.returncode == 0 and r.stderr == ""                # the merge touches the package, no line, passes
    commit(repo, "Merge branch 'side'")                        # the merge is done: MERGE_HEAD is gone
    stage(repo, "ai-packages/qa-factory/scripts/y.py")
    assert gate(repo, "Merge branch 'side'\n").returncode == 1  # the same text on a non-merge commit is refused
    assert gate(repo, "plain\n\narchitecture: AR-2 -- kept\n").returncode == 0


def test_a_line_inside_a_fenced_block_counts_as_absent(repo):
    stage(repo, PKG)
    fenced = "x\n\n```\narchitecture: AR-3 -- kept\n```\n"
    assert gate(repo, fenced).returncode == 1
    quoted = "x\n\n> architecture: AR-3 -- kept\n"
    assert gate(repo, quoted).returncode == 1
    assert gate(repo, fenced + "\narchitecture: AR-3 -- kept\n").returncode == 0     # the real line after it


def test_a_comment_line_never_counts(repo):
    stage(repo, PKG)
    assert gate(repo, "x\n\n# architecture: AR-3 -- kept\n").returncode == 1


def test_two_good_lines_pass_silently(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: AR-1 -- kept by the test\narchitecture: AR-10 -- kept by the reader\n")
    assert r.returncode == 0 and r.stderr == ""


def test_every_line_is_judged_a_bad_second_or_first_line_refuses(repo):
    stage(repo, PKG)
    r = gate(repo, "x\n\narchitecture: AR-1 -- kept\narchitecture: AR-99 -- second and wrong\n")
    assert r.returncode == 1 and "AR-99" in r.stderr and "unknown invariant id" in r.stderr
    assert "WARN" not in r.stderr and "(1 of 2 judged)" in r.stderr
    r = gate(repo, "x\n\narchitecture: AR-99 -- first and wrong\narchitecture: AR-1 -- kept\n")
    assert r.returncode == 1 and "AR-99" in r.stderr and "(1 of 2 judged)" in r.stderr
    r = gate(repo, "x\n\narchitecture: AR-98 -- a\narchitecture: none --\narchitecture: AR-97 -- b\n")
    assert r.returncode == 1 and "(3 of 3 judged)" in r.stderr
    assert "AR-98" in r.stderr and "AR-97" in r.stderr and "no reason after the dashes" in r.stderr


def test_a_squash_message_with_an_indented_pair_of_good_lines_passes(repo):
    stage(repo, PKG)
    msg = "Squashed commits\n\n    architecture: AR-1 -- kept in the first commit\n" \
          "    architecture: none -- the second only reworded a comment\n"
    r = gate(repo, msg)
    assert r.returncode == 0 and r.stderr == ""


def test_the_gate_reads_the_index_the_generator_writes():
    """F-3: the gate's INDEX_ID_RE is the twin of render()'s `- AR-%d — %s`; nothing else ties them."""
    import architecture_index as gen
    opener_text = "".join("## %s. S\n**AR-%d — Title %d.**\n" % ("ABCD"[(n - 1) % 4], n, n) for n in range(1, 31))
    sections, _ = gen.scan(opener_text)
    printed = gen.render(sections)
    ids = ag.known_ids(printed)
    assert ids == ["AR-%d" % n for n in range(1, 31)]
    assert all(ag.ID_RE.fullmatch(i) and ag.INDEX_ID_RE.match("- %s — x" % i) for i in ids)
    for bad in ("AR-01", "ar-1", "AR-1a", "AR-0"):
        assert not ag.ID_RE.fullmatch(bad), bad
        assert not ag.INDEX_ID_RE.search("- %s — x" % bad), bad


def test_known_ids_over_the_real_index_equal_the_real_openers_in_order():
    root = TOOLS.parent
    source = (root / "ai-packages" / "qa-factory" / "design" / "architecture.md").read_text(encoding="utf-8")
    body = source.split("\n## How a change walks this map")[0]
    wanted = ["AR-%s" % n for n in re.findall(r"^\*\*AR-(\d+) — ", body, re.MULTILINE)]
    index = (root / "docs" / "ARCHITECTURE_INDEX.md").read_text(encoding="utf-8")
    assert wanted and ag.known_ids(index) == wanted


def test_a_crlf_message_is_read(repo):
    stage(repo, PKG)
    assert gate(repo, "x\r\n\r\narchitecture: AR-2 -- kept\r\n").returncode == 0


def test_missing_message_path_argument_is_refused():
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode == 1 and "need a path" in r.stderr


def test_decide_is_pure_and_silent_off_the_package():
    assert ag.decide("anything", ["tools/a.py"], None) == (0, "")
    assert ag.decide("", [PKG], INDEX)[0] == 1
    assert ag.decide("architecture: AR-1 -- ok" + J, [PKG], INDEX) == (0, "")


def test_more_than_five_paths_are_abbreviated():
    code, text = ag.decide("x", ["ai-packages/qa-factory/f%d.py" % i for i in range(8)], INDEX)
    assert code == 1 and "... and 3 more" in text


# ---- t-1765 A5: the `judgment:` line and the census cross-check ---------------------------------------------

ARCH = "x\n\narchitecture: none -- r\n"
CENSUS = ag.CENSUS_REL


def census(**ceilings):
    ratchet = {"word-list": 5, "meaning-proxy": 2, "meaning": 1, "breach": 0, "blocks_overrides": 3, "safety": 4,
               "blocking_per_role": {"scout": 2, "builder": 1}}
    ratchet.update(ceilings)
    return json.dumps({"ratchet": ratchet})


def dec(judgment, head=None, index=None, arch=ARCH, idx=INDEX):
    msg = arch + (("judgment: " + judgment + "\n") if judgment is not None else "")
    return ag.decide(msg, [PKG], idx, head, index)


def test_no_judgment_line_is_refused_with_the_four_forms():
    code, text = dec(None)
    assert code == 1 and "no `judgment:` line" in text
    for form in ("judgment: none --", "judgment: adds data check <unit>", "to role", "to code"):
        assert form in text


def test_judgment_none_passes():
    assert dec("none -- x") == (0, "")


def test_judgment_moves_to_role_passes():
    assert dec("moves A to role -- y") == (0, "")


def test_judgment_moves_without_target_is_refused():
    code, text = dec("moves A -- y")
    assert code == 1 and "not `moves <what> to role` or `moves <what> to code`" in text


def test_judgment_adds_data_check_passes():
    assert dec("adds data check u -- z") == (0, "")


@pytest.mark.parametrize("line", ["adds data check -- z", "adds data check", "none --", "none", "moves A to code --",
                                  "moves A to role", "moves to code -- y", "bogus -- y"])
def test_judgment_bad_forms_are_refused(line):
    code, text = dec(line)
    assert code == 1 and "`judgment:" in text and "judgment: moves <what> to code" in text


def test_world_i_no_census_anywhere_is_silent():
    assert dec("none -- x", None, None) == (0, "")


def test_world_ii_census_created_passes_under_none():
    assert dec("none -- census created", None, census()) == (0, "")


def test_world_ii_unreadable_head_warns_and_passes():
    code, text = dec("none -- repair", "{not json", census())
    assert code == 0 and "census in HEAD unreadable; treated as absent (world ii): the index census becomes the base" in text
    assert "compared against" not in text


def test_world_iii_deleted_census_refuses_none_and_data_check_and_passes_moves_to_code():
    for line in ("none -- x", "adds data check u -- z", "moves A to role -- y"):
        code, text = dec(line, census(), None)
        assert code == 1 and "census deleted by this commit" in text, line
    assert dec("moves A to code -- y", census(), None) == (0, "")


def test_world_iv_equal_blobs_are_silent():
    assert dec("none -- x", census(), census()) == (0, "")


def test_world_v_raise_of_word_list_needs_moves_to_code():
    new = census(**{"word-list": 6})
    for line in ("none -- x", "adds data check u -- z"):
        code, text = dec(line, census(), new)
        assert code == 1 and "word-list 5 → 6" in text, line
    assert dec("moves A to code -- y", census(), new) == (0, "")


def test_world_v_raise_only_of_safety_refuses_none_passes_data_check():
    new = census(safety=5)
    code, text = dec("none -- x", census(), new)
    assert code == 1 and "safety 4 → 5" in text
    assert dec("adds data check u -- z", census(), new) == (0, "")
    assert dec("moves A to code -- y", census(), new) == (0, "")


def test_world_v_raise_in_blocking_per_role_is_weak_and_named_dotted():
    new = census(blocking_per_role={"scout": 3, "builder": 1})
    code, text = dec("none -- x", census(), new)
    assert code == 1 and "blocking_per_role.scout 2 → 3" in text
    assert dec("adds data check u -- z", census(), new) == (0, "")


def test_world_v_mixed_raise_needs_code_and_names_every_key():
    new = census(safety=5, meaning=2)
    code, text = dec("adds data check u -- z", census(), new)
    assert code == 1 and "safety 4 → 5" in text and "meaning 1 → 2" in text


def test_new_key_above_zero_is_a_raise_new_zero_and_vanished_are_not():
    base = json.loads(census())["ratchet"]
    with_new = dict(base, extra=2)
    assert dec("none -- x", census(), json.dumps({"ratchet": with_new}))[0] == 1
    assert dec("none -- x", census(), json.dumps({"ratchet": dict(base, extra=0)})) == (0, "")
    gone = {k: v for k, v in base.items() if k != "meaning"}
    assert dec("none -- x", census(), json.dumps({"ratchet": gone})) == (0, "")


def test_lowering_a_ceiling_is_not_a_raise():
    assert dec("none -- x", census(), census(**{"word-list": 1})) == (0, "")


@pytest.mark.parametrize("blob", ["{broken", "[]", json.dumps({"other": 1}), json.dumps({"ratchet": []}),
                                  json.dumps({"ratchet": {"word-list": "3"}}),
                                  json.dumps({"ratchet": {"word-list": -1}}),
                                  json.dumps({"ratchet": {"word-list": 1.5}}),
                                  json.dumps({"ratchet": {"word-list": True}}), ""])
def test_broken_index_blob_is_refused_naming_the_path_whatever_the_line(blob):
    for head in (None, census()):
        code, text = dec("moves A to code -- y", head, blob)
        assert code == 1 and CENSUS in text, (blob, head)


def test_no_ar_index_and_no_judgment_line_is_one_refusal_naming_both():
    code, text = ag.decide("x\n", [PKG], None)
    assert code == 1 and text.count("architecture_gate: commit touches") == 1
    assert "docs/ARCHITECTURE_INDEX.md is missing" in text and "no `judgment:` line" in text
    assert "architecture: AR-n" in text and "judgment: none --" in text


def test_missing_ar_index_never_leaves_judgment_unchecked():
    code, text = ag.decide("architecture: none -- r\njudgment: moves A -- y\n", [PKG], None)
    assert code == 1 and "is missing" in text and "`judgment: moves A`" in text


def test_unreadable_census_does_not_remove_the_architecture_refusal():
    code, text = ag.decide("x\njudgment: none -- x\n", [PKG], INDEX, None, "{broken")
    assert code == 1 and "no `architecture:` line" in text and CENSUS in text


def test_empty_message_refuses_both_kinds():
    code, text = ag.decide("", [PKG], INDEX)
    assert code == 1 and "no `architecture:` line" in text and "no `judgment:` line" in text


def test_judgment_line_inside_a_fence_or_quote_is_not_counted():
    fenced = ARCH + "\n```\njudgment: none -- x\n```\n"
    assert ag.decide(fenced, [PKG], INDEX)[0] == 1
    assert ag.decide(ARCH + "\n> judgment: none -- x\n", [PKG], INDEX)[0] == 1
    assert ag.decide(fenced + "\njudgment: none -- x\n", [PKG], INDEX) == (0, "")


def test_every_judgment_line_is_judged():
    code, text = dec("none -- x\njudgment: moves A -- y")
    assert code == 1 and "(1 of 2 judged)" in text


def test_no_package_path_is_silent_before_any_read():
    assert ag.decide("", ["tools/a.py"], None, "{x", "{y") == (0, "")


def test_prose_matches_is_parameterised_not_copied():
    assert [m.group(1).strip() for m in ag._prose_matches("judgment: none -- a\n", ag.JUDGMENT_RE)] == ["none -- a"]
    assert ag._prose_matches("judgment: none -- a\n") == []


def census_repo(repo, head=None, index=None):
    """head: committed census text (None = none), index: staged census text (None = the file is gone / absent)."""
    rel = CENSUS
    if head is not None:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(head, encoding="utf-8")
        git(repo, "add", "--", rel)
        commit(repo, "census")
        if index is None:
            git(repo, "rm", "-q", "--", rel)
    if index is not None:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(index, encoding="utf-8")
        git(repo, "add", "--", rel)
    stage(repo, PKG)


def test_end_to_end_reads_the_blobs_through_git(repo):
    census_repo(repo, census(), census(**{"word-list": 9}))
    r = gate(repo, ARCH + "judgment: none -- x\n")
    assert r.returncode == 1 and "word-list 5 → 9" in r.stderr
    assert gate(repo, ARCH + "judgment: moves A to code -- y\n").returncode == 0


def test_end_to_end_deleted_census(repo):
    census_repo(repo, census(), None)
    r = gate(repo, ARCH + "judgment: none -- x\n")
    assert r.returncode == 1 and "census deleted by this commit" in r.stderr
    assert gate(repo, ARCH + "judgment: moves A to code -- y\n").returncode == 0


def test_end_to_end_census_created_and_absent(repo):
    census_repo(repo, None, census())
    stage(repo, "ai-packages/qa-factory/scripts/y.py")
    assert gate(repo, ARCH + "judgment: none -- census created\n").returncode == 0


def test_end_to_end_no_judgment_line_is_refused(repo):
    stage(repo, PKG)
    r = gate(repo, ARCH, judgment=False)
    assert r.returncode == 1 and "no `judgment:` line" in r.stderr


def test_a_merge_commit_is_exempt_from_both_lines(repo):
    merge_in_progress(repo)
    r = gate(repo, "Merge branch 'side'\n", judgment=False)
    assert r.returncode == 0 and r.stderr == ""


# ---- t-1780 fix round: F1 (absent vs failed), F2 (broken-census text), F3 (builder forks), Q3 ----------------

def test_fork1_unknown_raised_key_is_strong():
    base = json.loads(census())["ratchet"]
    new = json.dumps({"ratchet": dict(base, foo=2)})
    for line in ("none -- x", "adds data check u -- z"):
        code, text = dec(line, census(), new)
        assert code == 1 and "foo (new) → 2" in text, line
    assert dec("moves A to code -- y", census(), new) == (0, "")


def test_fork2_two_judgment_lines_form_and_level():
    code, text = dec("none -- x\njudgment: moves A -- y")
    assert code == 1 and "(1 of 2 judged)" in text and "`judgment: moves A`" in text
    assert dec("none -- x\njudgment: moves A to code -- y", census(), census(**{"word-list": 6})) == (0, "")


def test_fork3_head_json_without_ratchet_warns_and_is_world_ii():
    new = census(**{"word-list": 99})
    for head in (json.dumps({"other": 1}), json.dumps({"ratchet": {"x": "3"}})):
        code, text = dec("none -- x", head, new)
        assert code == 0 and "census in HEAD unreadable; treated as absent (world ii)" in text, head


def test_fork4_deleted_census_with_unreadable_head_needs_moves_to_code():
    code, text = dec("none -- x", "{x", None)
    assert code == 1 and "census deleted by this commit" in text
    assert dec("moves A to code -- y", "{x", None) == (0, "")


def test_census_as_the_only_staged_package_path_needs_the_line(repo):
    path = repo / CENSUS
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(census(), encoding="utf-8")
    git(repo, "add", "--", CENSUS)
    r = gate(repo, ARCH, judgment=False)
    assert r.returncode == 1 and "no `judgment:` line" in r.stderr
    assert gate(repo, ARCH + "judgment: none -- census created\n").returncode == 0


def test_broken_index_census_refusal_states_expected_and_offers_no_none_door():
    code, text = dec("moves A to code -- y", census(), "{broken")
    assert code == 1 and "a JSON object with a `ratchet` object of integer ceilings >= 0 at " + CENSUS in text
    assert "judgment: none" not in text


def _fake_git(code, err=b"", out=b"", unborn=False):
    def fake(root, *args, timeout=120, stderr=False):
        if args[:1] == ("rev-parse",):
            return (1 if unborn else 0), b""
        return (code, out, err) if stderr else (code, out)
    return fake


def test_show_failure_refuses_naming_could_not_be_read_even_with_moves_to_code(monkeypatch):
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(-1, b"timed out"))
    head = ag._show("HEAD:" + CENSUS)
    assert isinstance(head, ag.Unread)
    code, text = ag.decide(ARCH + "judgment: moves A to code -- y\n", [PKG], INDEX, head, census())
    assert code == 1 and "could not be read: timed out" in text and "judgment: none" not in text
    code, text = ag.decide(ARCH + "judgment: none -- x\n", [PKG], INDEX, census(), ag._show(":" + CENSUS))
    assert code == 1 and "census in the index could not be read" in text


@pytest.mark.parametrize("err", [b"fatal: path 'p' does not exist in 'HEAD'", b"fatal: path 'p' exists on disk, but not in the index"])
def test_show_absent_blob_is_none(monkeypatch, err):
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(128, err))
    assert ag._show("HEAD:p") is None and ag._show(":p") is None


def test_show_unborn_head_is_none_but_other_128_is_unread(monkeypatch):
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(128, b"fatal: invalid object name 'HEAD'.", unborn=True))
    assert ag._show("HEAD:p") is None
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(128, b"fatal: bad object", unborn=False))
    assert isinstance(ag._show("HEAD:p"), ag.Unread)


def test_bom_prefixed_blob_is_parsed_not_refused(monkeypatch):
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(0, out=b"\xef\xbb\xbf" + census().encode("utf-8")))
    blob = ag._show(":" + CENSUS)
    assert ag.decide(ARCH + "judgment: none -- x\n", [PKG], INDEX, census(), blob) == (0, "")


def test_zero_byte_index_blob_is_refused_naming_the_path(monkeypatch):
    monkeypatch.setattr(ag.gitcmd, "git", _fake_git(0, out=b""))
    blob = ag._show(":" + CENSUS)
    assert blob == ""
    code, text = ag.decide(ARCH + "judgment: moves A to code -- y\n", [PKG], INDEX, None, blob)
    assert code == 1 and CENSUS in text
    code, text = ag.decide(ARCH + "judgment: none -- x\n", [PKG], INDEX, "", census())
    assert code == 0 and "census in HEAD unreadable" in text


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
