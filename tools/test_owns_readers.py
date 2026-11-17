"""test_owns_readers.py -- tools/owns_readers.py through its API and CLI door: ONE tiny git repo built once for the file, one table of
cases (input -> the lines of the block). The row id names the case; the `quarantine-*` rows are one contiguous group, deleted with
owns_readers._quarantine_status when the quarantine section goes (spec section 2.3 (ii)-q). Time is never asserted (FR-31)."""
import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import owns_readers as orr  # noqa: E402
import test_quarantine as tq  # noqa: E402

TESTS = "ai-packages/qa-factory/scripts/tests/"
LAYERS = TESTS + "test-layers.json"
SLOW = "ai-packages/qa-factory/scripts/slow_tests.json"
NOTE = "tools/owns_readers.py docstring"
QUAR = "(quarantined: the canon does not run it; do not edit)"
GOOD_LAYERS = {"keep": {"test_keep.py": {}}, "quarantine": {"test_qowned.py": {}, "test_qreader.py": {}, "test_qall.py": {}}}
GOOD_SLOW = {"thresholds": {"slow_over_s": 10, "fast_under_s": 5}, "files": {"test_slow_null.py": None, "test_slow_3.py": 3}}


def _files() -> dict:
    f = {LAYERS: json.dumps(GOOD_LAYERS), SLOW: json.dumps(GOOD_SLOW)}
    for name in ("test_qowned", "test_slow_null", "test_slow_3", "test_keep"):
        f[TESTS + name + ".py"] = "x = 1\n"
    f[TESTS + "test_qreader.py"] = "# mod_qr.py\n"
    f[TESTS + "test_qall.py"] = "# mod_all.py\n"
    f["tools/mod_quiet.py"] = "x = 1\n"
    f["tools/test_mod_quiet.py"] = "import mod_quiet  # mod_quiet.py\n"
    f["tools/mod_count.py"] = "x = 1\n"
    f["tools/test_mod_count.py"] = "# mod_count.py\n"
    f["tools/test_zz_cnt.py"] = "# mod_count.py\n"
    f["tools/tool_count.py"] = "import mod_count\n"
    f["tools/mod_tier.py"] = "x = 1\n"
    f["tools/test_mod_tier_z.py"] = "# mod_tier\n"
    f["tools/test_aaa_full.py"] = "# mod_tier.py\n"
    f["tools/test_aab_stem.py"] = "# mod_tier here\n"
    f["tools/mod_data.py"] = "x = 1\n"
    f["tools/carrier_data.json"] = '{"k": "mod_data.py"}\n'
    f["tools/mod_cap.py"] = "x = 1\n"
    for i in range(26):
        f["tools/test_cap_%02d.py" % i] = "# mod_cap.py%s\n" % (" fn_cap" if i == 5 else "")
    f["tools/mod_dcap.py"] = "x = 1\n"
    for i in range(13):
        f["tools/dcap_%02d.json" % i] = '{"k": "mod_dcap.py"}\n'
    f["tools/mod_all.py"] = "x = 1\n"
    for i in range(26):
        f["tools/test_all_%02d.py" % i] = "# mod_all.py\n"
    f["tools/tool_all.py"] = "import mod_all\n"
    f["tools/mod_qr.py"] = "x = 1\n"
    f["tools/mod_names.py"] = "x = 1\n"
    f["tools/test_fn_hit_user.py"] = "fn_hit()\n"
    f["tools/tool_fn_hit.py"] = "fn_hit()\n"
    f["tools/test_cli_flag.py"] = "run('--part x')\n"
    for i in range(3):
        f["tools/dsmall/%s.py" % ("a_one", "b_two", "c_three")[i]] = "x = 1\n"
    f["tools/test_dsmall_user.py"] = "# a_one.py\n"
    for i in range(41):
        f["tools/dwide/f_%02d.py" % i] = "x = 1\n"
    f["tools/s0.md"] = "x\n"
    f["tools/test_short_a.py"] = "# the s0 stage\n"
    f["tools/s1.md"] = "x\n"
    f["tools/test_short_b.py"] = "# s1.md\n"
    f["tools/my dir/ф.py"] = "x = 1\n"
    f["tools/test_cyr.py"] = "# ф.py\n"
    f["tools/-x.py"] = "x = 1\n"
    f["tools/test_dash.py"] = "# -x.py\n"
    f["tools/mod_two_a.py"] = "x = 1\n"
    f["tools/mod_two_b.py"] = "x = 1\n"
    f["tools/test_two.py"] = "# mod_two_a.py mod_two_b.py\n"
    f["tools/mod_untr.py"] = "x = 1\n"
    f["tools/mod_t25.py"] = "x = 1\n"
    for i in range(25):
        f["tools/test_t25_%02d.py" % i] = "# mod_t25.py\n"
    f["tools/mod_d12.py"] = "x = 1\n"
    for i in range(12):
        f["tools/d12_%02d.json" % i] = '{"k": "mod_d12.py"}\n'
    for i in range(40):
        f["tools/d40/g_%02d.py" % i] = "x = 1\n"
    f["tools/mod_wf.py"] = "x = 1\n"
    f[".github/workflows/ci.yml"] = "run: python tools/mod_wf.py\n"
    f["tools/mod_hq.py"] = "x = 1\n"
    f[TESTS + "helper_hq.py"] = "# mod_hq.py\n"
    f["tools/mod_ord_a.py"] = "x = 1\n"
    f["tools/mod_ord_b.py"] = "x = 1\n"
    f["tools/tool_ord_a.py"] = "import mod_ord_a\n"
    f["tools/test_ord_b.py"] = "# mod_ord_b.py\n"
    f["tools/mod_bin.py"] = "x = 1\n"
    return f


def _put(root: Path, rel: str, body) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body if isinstance(body, bytes) else body.encode("utf-8"))


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    base = tmp_path_factory.mktemp("owns_readers_world")
    root = base / "repo"
    root.mkdir()

    def g(*args):
        r = subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                            "-c", "core.autocrlf=false", *args], capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stderr
        return r.stdout.strip()

    g("init", "-q")
    for rel, body in _files().items():
        _put(root, rel, body)
    _put(root, "tools/test_bin.py", b"\x00\x01mod_bin.py\x00")
    g("add", "-A")
    g("commit", "-q", "-m", "base")
    main_sha = g("rev-parse", "HEAD")
    g("update-ref", "refs/remotes/origin/main", main_sha)

    def variant(name, rel, body):
        g("checkout", "-q", "-b", name, main_sha)
        if body is None:
            (root / rel).unlink()
        else:
            _put(root, rel, body)
        g("add", "-A")
        g("commit", "-q", "-m", name)

    variant("nolayers", LAYERS, None)
    variant("badlayers", LAYERS, "{not json")
    variant("nosection", LAYERS, json.dumps({"keep": {"test_keep.py": {}}}))
    variant("badslow", SLOW, json.dumps({"files": {}}))
    g("checkout", "-q", "--detach", main_sha)
    _put(root, "docs/only_in_tree.md", "uncommitted\n")
    _put(root, "copy/test_mod_untr.py", "# mod_untr.py mod_untr\n")
    outside = base / "elsewhere"
    outside.mkdir()
    return SimpleNamespace(root=root, sha=main_sha, outside=outside)


class FakeGit:
    """gitcmd.git that fails for one git subcommand (rc, stderr) and is the real one otherwise."""

    def __init__(self, real, sub, rc):
        self.real, self.sub, self.rc = real, sub, rc

    def __call__(self, root, *args, **kw):
        if args and args[0] == self.sub:
            return (self.rc, b"", b"fatal: boom") if kw.get("stderr") else (self.rc, b"fatal: boom")
        return self.real(root, *args, **kw)


def C(case_id, paths, has=(), lacks=(), count=(), order=(), lines=None, given=(), names=(), base="origin/main",
      readers=False, all_=False, patch=None):
    return dict(id=case_id, paths=list(paths), has=list(has), lacks=list(lacks), count=list(count), order=list(order),
                lines=lines, given=list(given), names=list(names), base=base, readers=readers, all_=all_, patch=patch)


H0 = "readers: 0 outside owns, 0 lines below -- base origin/main "
CASES = [
    C("quiet", ["tools/mod_quiet.py", "tools/test_mod_quiet.py"], lines=1,
      has=[H0, "(literal mention; known misses: %s)" % NOTE, "re:^readers: 0 outside owns, 0 lines below -- base origin/main {sha8} "]),
    C("count-default", ["tools/mod_count.py"], has=["readers: 3 outside owns, 1 lines below",
                                                      "- more: tools/mod_count.py -- 2 test, 1 code readers not listed (--readers / --all lists them)"],
      lacks=["- outside:"]),
    C("readers-list", ["tools/mod_count.py"], readers=True,
      has=["readers: 3 outside owns, 3 lines below", "- outside: tools/test_mod_count.py (test) names tools/mod_count.py",
           "- outside: tools/test_zz_cnt.py (test) names tools/mod_count.py", "- more: tools/mod_count.py -- 1 code readers"],
      lacks=["tool_count.py (code)"],
      order=["- outside: tools/test_mod_count.py", "- outside: tools/test_zz_cnt.py", "- more:"]),
    C("order-tiers", ["tools/mod_tier.py"], readers=True,
      order=["- outside: tools/test_mod_tier_z.py", "- outside: tools/test_aaa_full.py", "- outside: tools/test_aab_stem.py"]),
    C("data-carrier", ["tools/mod_data.py"], has=["readers: 1 outside owns, 1 lines below",
                                                   "- more: tools/mod_data.py -- 1 data readers"], lacks=["- data:"]),
    C("data-carrier-listed", ["tools/mod_data.py"], readers=True,
      has=["- data: tools/carrier_data.json names tools/mod_data.py"], lacks=["- more:"]),
    C("test-cap", ["tools/mod_cap.py"], readers=True, count=[("- outside:", 25), ("- hot:", 1)],
      has=["- hot: tools/mod_cap.py -- 26 test readers; pass --names <the functions or keys you change> for a usable list",
           "- more: tools/mod_cap.py -- 1 test readers not listed"], order=["- hot:", "- outside:", "- more:"]),
    C("hot-with-names", ["tools/mod_cap.py"], names=["fn_cap"], readers=True, count=[("- outside:", 0)],
      has=["- names: tools/test_cap_05.py (test) names fn_cap", "- more: tools/mod_cap.py -- 26 test readers"], lacks=["- hot:"]),
    C("test-cap-at", ["tools/mod_t25.py"], readers=True, count=[("- outside:", 25), ("- hot:", 0), ("- more:", 0)],
      has=["readers: 25 outside owns, 25 lines below"]),
    C("data-cap-at", ["tools/mod_d12.py"], readers=True, count=[("- data:", 12), ("- more:", 0)]),
    C("data-cap", ["tools/mod_dcap.py"], readers=True, count=[("- data:", 12)],
      has=["- more: tools/mod_dcap.py -- 1 data readers"]),
    C("all-lifts", ["tools/mod_all.py"], all_=True, count=[("- outside:", 28)],
      has=["tools/tool_all.py (code) names tools/mod_all.py", QUAR, "test_qall.py"], lacks=["- more:", "- hot:"]),
    # --- the quarantine rows: ONE contiguous group, deleted with owns_readers._quarantine_status ---
    C("quarantine-owned", [TESTS + "test_qowned.py"],
      has=["- quarantined: %stest_qowned.py (owned) -- the canon does not run it; a case goes to a keep file" % TESTS]),
    C("quarantine-reader-count", ["tools/mod_qr.py"], has=["readers: 1 outside owns", "- more: tools/mod_qr.py -- 1 quarantined readers"],
      lacks=["1 test", "- outside:", "quarantine: unknown"]),
    C("quarantine-layers-absent", ["tools/mod_qr.py"], base="nolayers",
      has=["quarantine: unknown (test-layers.json absent at", "- more: tools/mod_qr.py -- 1 test (quarantine unknown) readers"],
      lacks=["- quarantined:", "? quarantined"]),
    C("quarantine-layers-absent-listed", ["tools/mod_qr.py"], base="nolayers", readers=True,
      has=["- outside: %stest_qreader.py (test, quarantine unknown) names tools/mod_qr.py" % TESTS], lacks=["- more:"]),
    C("quarantine-unknown-code-reader-no-mark", ["tools/mod_hq.py"], base="nolayers",
      has=["- more: tools/mod_hq.py -- 1 code readers not listed"], lacks=["(quarantine unknown)", "? quarantined"]),
    C("quarantine-show-fails", [TESTS + "test_qowned.py"], given=["docs/nofile.md"], patch=("quarantine-show", 128),
      has=["quarantine: unknown (test-layers.json present at", "but read empty)", "- absent: docs/nofile.md (given)"],
      lacks=["- quarantined:"]),
    C("quarantine-malformed", [TESTS + "test_qowned.py"], given=["docs/nofile.md"], base="badlayers",
      has=["quarantine: unknown (test-layers.json at", "is not JSON)", "- absent: docs/nofile.md (given)"], lacks=["- quarantined:"]),
    C("quarantine-section-gone", [TESTS + "test_qowned.py"], base="nosection", lacks=["- quarantined:", "quarantine: unknown"]),
    # --- end of the quarantine group ---
    C("slow-owned", [TESTS + "test_slow_null.py"], given=[TESTS + "test_slow_3.py"],
      has=["- slow: %stest_slow_null.py (owned) -- listed slow: not run locally, judged by the batch canon" % TESTS,
           "- slow: %stest_slow_3.py (given)" % TESTS]),
    C("slow-malformed", [TESTS + "test_slow_null.py"], base="badslow", has=["slow: unknown ("], lacks=["- slow:"]),
    C("absent-given", ["tools/mod_quiet.py"], given=["docs/only_in_tree.md"],
      has=["- absent: docs/only_in_tree.md (given) -- not on origin/main {sha8}; a worktree builder cannot read it"]),
    C("absent-owned", ["tools/zz_nowhere.py"], has=["- absent: tools/zz_nowhere.py (owned) -- not on origin/main"]),
    C("new-exists", ["tools/mod_quiet.py (new)"], has=["- exists: tools/mod_quiet.py (new) -- already on origin/main {sha8}"]),
    C("new-absent", ["tools/zz_new.py (new)"], lines=1, lacks=["- absent:", "- exists:"]),
    C("untracked-copy", ["tools/mod_untr.py"], lines=1, has=["readers: 0 outside owns, 0 lines below"]),
    C("names-hit", ["tools/mod_names.py"], names=["fn_hit"],
      has=["readers: 0 outside owns", "- names: tools/test_fn_hit_user.py (test) names fn_hit",
           "- more: name fn_hit -- 1 code readers not listed"]),
    C("names-absent", ["tools/mod_quiet.py"], names=["nosuch_zz"],
      has=["- absent: name nosuch_zz -- not named anywhere on origin/main {sha8}"]),
    C("names-new-absent", ["tools/mod_quiet.py"], names=["g_new_zz (new)"], lacks=["- absent:", "- exists:"]),
    C("names-new-exists", ["tools/mod_quiet.py"], names=["fn_hit (new)"],
      has=["- exists: name fn_hit (new) -- already named by 2 files on {sha8}"]),
    C("names-nonword", ["tools/mod_quiet.py"], names=["--part"],
      has=["- names: tools/test_cli_flag.py (test) names --part"], lacks=["absent: name --part", "unknown"]),
    C("names-cap-at", ["tools/mod_quiet.py"], names=["nq_%02d" % i for i in range(20)], count=[("- absent: name nq_", 20)],
      lacks=["unsearched"]),
    C("names-cap", ["tools/mod_quiet.py"], names=["nm_%02d" % i for i in range(21)], count=[("- absent: name nm_", 20)],
      has=["- unsearched: 1 more names over the cap"], lacks=["nm_20"]),
    C("base-missing", ["tools/mod_quiet.py"], base="origin/nope", lines=1,
      has=["readers: unknown -- base origin/nope does not resolve here (git: ", "); nothing was searched"],
      lacks=["0 outside", "quarantine", "not quarantined"]),
    C("base-sha", ["tools/mod_quiet.py"], base="{sha}", has=["-- base {sha} {sha8} ("]),
    C("grep-rc-128", ["tools/mod_quiet.py"], given=["docs/only_in_tree.md"], patch=("grep", 128),
      has=["readers: unknown -- git grep exited 128 (fatal: boom); 1 lines below -- base origin/main {sha8}",
           "- absent: docs/only_in_tree.md (given)"], lacks=["0 outside owns"]),
    C("grep-timeout", ["tools/mod_quiet.py"], given=["docs/only_in_tree.md"], patch=("grep", -1),
      has=["readers: unknown -- git grep exited -1 (fatal: boom)", "- absent: docs/only_in_tree.md (given)"],
      lacks=["0 outside owns"]),
    C("lstree-fails", ["tools/mod_quiet.py"], given=["docs/only_in_tree.md"], patch=("ls-tree", 128),
      has=["presence: unknown (git ls-tree exited 128", "quarantine: unknown (", "slow: unknown ("],
      lacks=["- absent:", "- exists:"]),
    C("outside-repo", ["{outside}/x.py"], has=["- unsearched: x.py (outside the repo; pass the repo path)",
                                               "readers: unknown -- no owned path was searched (1 unsearched below); 1 lines below -- base"],
      lacks=["{outside}", "{outside_posix}", "0 outside owns"]),
    C("outside-dotdot", ["../outside.py"], has=["readers: unknown -- no owned path was searched (1 unsearched below)",
                                                "- unsearched: outside.py (outside the repo"], lacks=["0 outside owns"]),
    C("mixed-searched-and-unsearched", ["../outside.py", "tools/mod_two_a.py"], readers=True,
      has=["readers: 1 outside owns, 2 lines below; unsearched: 1 paths -- base origin/main ",
           "- unsearched: outside.py (outside the repo"], lacks=["unknown --"]),
    C("empty-list", [], lines=1, has=["readers: unknown -- no owned path was searched (0 unsearched below); 0 lines below -- base"],
      lacks=["0 outside owns"]),
    C("control-char-path-only", ["tools/a\tb.py"], has=["readers: unknown -- no owned path was searched (1 unsearched below)",
                                                       "- unsearched: 1 paths with a control character (not searched)"],
      lacks=["0 outside owns", "a\tb"]),
    C("control-char-path-mixed", ["tools/mod_two_a.py", "tools/a\tb.py"],
      has=["readers: 1 outside owns, 2 lines below; unsearched: 1 paths -- base"]),
    C("control-char-name", ["tools/mod_quiet.py"], names=["a\tb"], has=["- unsearched: 1 names with a control character (not searched)"],
      lacks=["a\tb"]),
    C("regex-meta-names", ["tools/mod_quiet.py"], names=["a.b*", "[x]"],
      has=["- absent: name a.b* -- not named anywhere", "- absent: name [x] -- not named anywhere"], lacks=["unknown"]),
    C("cyrillic-name", ["tools/mod_quiet.py"], names=["\u0444.py", "\u043a\u0443\u0447\u043a\u0430"],
      has=["- names: tools/test_cyr.py (test) names \u0444.py", "- absent: name \u043a\u0443\u0447\u043a\u0430 -- not named anywhere"]),
    C("path-cap-at", ["tools/zz_p%03d.py (new)" % i for i in range(orr.dispatch_manifest.PATH_CAP)], lines=1,
      has=["readers: 0 outside owns, 0 lines below -- base"], lacks=["unsearched"]),
    C("path-cap-beyond", ["tools/zz_p%03d.py (new)" % i for i in range(orr.dispatch_manifest.PATH_CAP + 1)],
      has=["readers: 0 outside owns, 1 lines below; unsearched: 1 paths -- base", "- unsearched: 1 more paths over the cap"]),
    C("dir-small", ["tools/dsmall"], has=["readers: 1 outside owns"], lacks=["- unsearched:"]),
    C("dir-at-cap", ["tools/d40"], lines=1, has=["readers: 0 outside owns, 0 lines below -- base"], lacks=["unsearched"]),
    C("dir-wide", ["tools/dwide"], has=["- unsearched: tools/dwide holds 41 files; readers not counted -- name the files",
                                        "readers: unknown -- no owned path was searched (1 unsearched below)"], lacks=["0 outside owns"]),
    C("short-stem-not-a-reader", ["tools/s0.md"], lines=1, has=["readers: 0 outside owns"]),
    C("short-stem-named", ["tools/s1.md"], has=["readers: 1 outside owns"]),
    C("space-cyrillic", ["tools/my dir/ф.py"], has=["readers: 1 outside owns"]),
    C("dash-name", ["tools/-x.py"], has=["readers: 1 outside owns"], lacks=["unknown"]),
    C("two-owned-one-line", ["tools/mod_two_a.py", "tools/mod_two_b.py"], readers=True,
      has=["readers: 1 outside owns, 1 lines below",
           "- outside: tools/test_two.py (test) names tools/mod_two_a.py, tools/mod_two_b.py"]),
    C("workflow-reader", ["tools/mod_wf.py"], readers=True, all_=True,
      has=["- outside: .github/workflows/ci.yml (code) names tools/mod_wf.py"]),
    C("two-owned-test-before-code", ["tools/mod_ord_a.py", "tools/mod_ord_b.py"], all_=True,
      order=["- outside: tools/test_ord_b.py", "- outside: tools/tool_ord_a.py"]),
    C("binary-skipped", ["tools/mod_bin.py"], lines=1, has=["readers: 0 outside owns"]),
]


def _fill(text: str, world) -> str:
    return (text.replace("{sha8}", world.sha[:8]).replace("{sha}", world.sha)
            .replace("{outside_posix}", world.outside.as_posix()).replace("{outside}", str(world.outside)))


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_owns_readers_table(case, world, monkeypatch):
    if case["patch"]:
        sub, rc = case["patch"]
        if sub == "quarantine-show":
            real = tq._git
            monkeypatch.setattr(tq, "_git", lambda root, *a: (rc, "") if a and a[0] == "show" else real(root, *a))
        else:
            monkeypatch.setattr(orr.gitcmd, "git", FakeGit(orr.gitcmd.git, sub, rc))
    paths = [_fill(p, world) for p in case["paths"]]
    rep = orr.report(paths, case["given"], case["names"], _fill(case["base"], world), repo=world.root)
    text = orr.render(rep, case["readers"], case["all_"])
    lines = text.splitlines()
    assert lines[0].startswith("readers: "), text
    assert re.search(r"(\d+) lines below", lines[0]) is None or int(re.search(r"(\d+) lines below", lines[0]).group(1)) == len(lines) - 1, text
    if case["lines"] is not None:
        assert len(lines) == case["lines"], text
    for want in case["has"]:
        want = _fill(want, world)
        assert (re.search(want[3:], text, re.M) if want.startswith("re:") else want in text), (want, text)
    for bad in case["lacks"]:
        assert _fill(bad, world) not in text, (bad, text)
    for prefix, n in case["count"]:
        assert sum(1 for l in lines if l.startswith(prefix)) == n, (prefix, text)
    at = -1
    for part in case["order"]:
        nxt = text.find(part, at + 1)
        assert nxt > at, ("order", part, text)
        at = nxt


def test_cli_door(world, capsys):
    """E-1 (no path: exit 2 with a door) and the CLI round (exit 0, the block on stdout)."""
    assert orr.main(["--repo", str(world.root), "--paths", " "]) == 2
    assert "OWNS_READERS REFUSED: no path given -- pass --paths <owned path>..." in capsys.readouterr().err
    assert orr.main(["--repo", str(world.root), "--paths", "tools/mod_quiet.py", "tools/test_mod_quiet.py"]) == 0
    assert capsys.readouterr().out.startswith("readers: 0 outside owns, 0 lines below -- base origin/main ")
