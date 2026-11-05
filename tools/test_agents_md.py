"""Tests for tools/agents_md.py -- the generated AGENTS.md for Codex users.

Every test works on a temp copy of the repo (--repo); the real AGENTS.md is never written here.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
REAL = TOOLS.parent
SCRIPT = TOOLS / "agents_md.py"
sys.path.insert(0, str(TOOLS))
import agents_md  # noqa: E402

SETTINGS = {
    "hooks": {
        "SessionStart": [{"hooks": [{"type": "command", "command": "python tools/hook_a.py"}]}],
        "PreToolUse": [
            {"matcher": "Task|Agent", "hooks": [
                {"type": "command", "command": "python tools/hook_b.py"},
                {"type": "command", "command": "node other/thing.js"}]},
        ],
    }
}
VALIDATOR = 'TIER_ORDER = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}\n'
ROLE = "---\nname: %s\ndescription: does %s | with a pipe\nmodel: m-%s\ntools: Read, Grep\n---\n\nbody\n"


def run(*args):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


def make_repo(root, claude="# Top\n\n@PROJECT.md\n\n@docs/IDX.md\n", extra=None):
    """A small but complete repo tree under `root`."""
    files = {
        "CLAUDE.md": claude,
        "PROJECT.md": "# Project\n\nproject text\n",
        "docs/IDX.md": "- idx line\n",
        ".claude/settings.json": json.dumps(SETTINGS),
        ".claude/agents/alpha.md": ROLE % ("alpha", "alpha", "alpha"),
        ".claude/agents/beta.md": ROLE % ("beta", "beta", "beta"),
        "tools/journal_validator.py": VALIDATOR,
        "tools/hook_a.py": '"""Hook A does a thing.\n\nMore text.\n"""\n',
        "tools/hook_b.py": "x = 1\n",
    }
    files.update(extra or {})
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            p.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
    for rel, content in files.items():
        if content is None and (root / rel).exists():
            (root / rel).unlink()
    return root


@pytest.fixture
def repo(tmp_path):
    return make_repo(tmp_path / "r")


@pytest.fixture(scope="module")
def real_copy(tmp_path_factory):
    """A copy of the real sources (not the real AGENTS.md) with a fresh generated output."""
    root = tmp_path_factory.mktemp("real")
    for rel in ("CLAUDE.md", "PROJECT.md", "docs/FACTORY_RULES_INDEX.md", "docs/ARCHITECTURE_INDEX.md",
                ".claude/settings.json"):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REAL / rel, root / rel)
    shutil.copytree(REAL / ".claude" / "agents", root / ".claude" / "agents")
    (root / "tools").mkdir()
    for f in (REAL / "tools").glob("*.py"):
        if not f.name.startswith("test_"):
            shutil.copyfile(f, root / "tools" / f.name)
    assert run("--repo", root).returncode == 0
    return root


def out_of(root):
    return (root / "AGENTS.md").read_bytes().decode("utf-8")


# ---------------------------------------------------------------- expansion

def test_both_imports_expanded_with_markers(repo):
    assert run("--repo", repo).returncode == 0
    text = out_of(repo)
    assert "<!-- begin PROJECT.md -->\n# Project\n\nproject text\n<!-- end PROJECT.md -->" in text
    assert "<!-- begin docs/IDX.md -->\n- idx line\n<!-- end docs/IDX.md -->" in text
    assert "\n@PROJECT.md\n" not in text and "\n@docs/IDX.md\n" not in text


def test_real_imports_expanded(real_copy):
    text = out_of(real_copy)
    assert "<!-- begin PROJECT.md -->" in text and "<!-- end PROJECT.md -->" in text
    assert "<!-- begin docs/FACTORY_RULES_INDEX.md -->" in text
    assert "<!-- end docs/FACTORY_RULES_INDEX.md -->" in text
    assert "\n@PROJECT.md\n" not in text
    assert "\n@docs/FACTORY_RULES_INDEX.md\n" not in text


def test_fenced_import_not_expanded(tmp_path):
    root = make_repo(tmp_path / "r", claude="# Top\n\n```\n@PROJECT.md\n```\n\n~~~\n@PROJECT.md\n~~~\n")
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "```\n@PROJECT.md\n```" in text and "~~~\n@PROJECT.md\n~~~" in text
    assert "<!-- begin PROJECT.md -->" not in text


FENCED_CLAUDE = ("# Top\n\n```\n@PROJECT.md\n```\n\n~~~\n@PROJECT.md\n~~~\n\n```sh\n~~~\n@PROJECT.md\n```\n\n"
                 "  ```\n@PROJECT.md\n  ```\n\n@docs/IDX.md\n")
FENCED_BODY = ("# Top\n\n```\n@PROJECT.md\n```\n\n~~~\n@PROJECT.md\n~~~\n\n```sh\n~~~\n@PROJECT.md\n```\n\n"
               "  ```\n@PROJECT.md\n  ```\n\n<!-- begin docs/IDX.md -->\n- idx line\n<!-- end docs/IDX.md -->")


def test_whole_body_of_a_fixture_with_fenced_blocks_is_pinned(tmp_path):
    """F6-16: the body (CLAUDE.md with its imports) of a fixture whose fences hold `@import` lines is the same text as before the
    fence reader moved to md_table.fence_walk: a fenced import is kept as text, a mark of the other kind inside a block does not close
    it, an import after the blocks is expanded."""
    root = make_repo(tmp_path / "r", claude=FENCED_CLAUDE)
    assert "\n".join(agents_md.build_body(root)) == FENCED_BODY
    assert run("--repo", root).returncode == 0
    assert FENCED_BODY in out_of(root)


def test_a_fence_opened_with_tildes_and_closed_with_backticks_is_not_closed(tmp_path):
    """The closing mark must be of the opening kind (md_table.fence_walk): the import after the mismatching mark is still inside."""
    root = make_repo(tmp_path / "r", claude="# Top\n\n~~~\n```\n@PROJECT.md\n")
    assert "\n".join(agents_md.build_body(root)) == "# Top\n\n~~~\n```\n@PROJECT.md"
    root = make_repo(tmp_path / "s", claude="# Top\n\n~~~\n```\n~~~\n@PROJECT.md\n")
    assert "<!-- begin PROJECT.md -->" in "\n".join(agents_md.build_body(root))


@pytest.mark.parametrize("claude", ["# Top\n\n````\n```\n@PROJECT.md\n````\n", "# Top\n\n```\n```sh\n@PROJECT.md\n```\n"])
def test_a_shorter_run_or_a_closer_with_an_info_string_does_not_close_a_block(tmp_path, claude):
    """CommonMark closing rule (md_table.fence_walk, F6-16): the import line stays text inside the block, as before the reader moved."""
    root = make_repo(tmp_path / "r", claude=claude)
    assert "\n".join(agents_md.build_body(root)) == claude.rstrip("\n")


def test_the_fence_reader_is_md_table_and_agents_md_holds_no_fence_regex():
    import md_table
    src = SCRIPT.read_text(encoding="utf-8")
    assert "md_table.fence_walk(" in src and agents_md.md_table is md_table
    assert not hasattr(agents_md, "FENCE_RE") and "`{3" not in src


def test_import_after_a_closed_fence_is_expanded(tmp_path):
    root = make_repo(tmp_path / "r", claude="# Top\n\n```\ncode\n```\n\n@PROJECT.md\n")
    assert run("--repo", root).returncode == 0
    assert "<!-- begin PROJECT.md -->" in out_of(root)


def test_inline_import_not_expanded(tmp_path):
    root = make_repo(tmp_path / "r", claude="# Top\n\nsee @PROJECT.md now\n@PROJECT.md trailing\n"
                                           "  @PROJECT.md\n")
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "see @PROJECT.md now" in text and "@PROJECT.md trailing" in text
    assert "<!-- begin PROJECT.md -->" not in text


def test_missing_import_exit_2_names_it(tmp_path):
    root = make_repo(tmp_path / "r", claude="# Top\n\n@docs/NOPE.md\n")
    r = run("--repo", root)
    assert r.returncode == 2 and "docs/NOPE.md" in r.stderr
    assert not (root / "AGENTS.md").exists()


def test_missing_claude_md_exit_2(tmp_path):
    root = make_repo(tmp_path / "r", extra={"CLAUDE.md": None})
    r = run("--repo", root)
    assert r.returncode == 2 and "CLAUDE.md" in r.stderr


def test_import_outside_repo_exit_2(tmp_path):
    root = make_repo(tmp_path / "r", claude="# Top\n\n@../outside.md\n")
    (tmp_path / "outside.md").write_text("x")
    r = run("--repo", root)
    assert r.returncode == 2 and "outside" in r.stderr


def test_cycle_exit_2_names_chain(tmp_path):
    root = make_repo(tmp_path / "r", claude="@a.md\n",
                     extra={"a.md": "@b.md\n", "b.md": "@a.md\n"})
    r = run("--repo", root)
    assert r.returncode == 2 and "cycle" in r.stderr
    assert "CLAUDE.md -> a.md -> b.md -> a.md" in r.stderr


def _chain(tmp_path, depth):
    """CLAUDE.md -> f1.md -> ... -> f<depth>.md (the last one is plain text)."""
    extra = {}
    for i in range(1, depth + 1):
        extra["f%d.md" % i] = ("@f%d.md\n" % (i + 1)) if i < depth else "leaf\n"
    return make_repo(tmp_path / "r", claude="@f1.md\n", extra=extra)


def test_depth_5_ok_and_depth_6_exit_2(tmp_path):
    ok = _chain(tmp_path, 5)
    assert run("--repo", ok).returncode == 0
    assert "<!-- begin f5.md -->\nleaf\n<!-- end f5.md -->" in out_of(ok)
    other = tmp_path / "six"
    other.mkdir()
    bad = _chain(other, 6)
    r = run("--repo", bad)
    assert r.returncode == 2 and "depth" in r.stderr and "f6.md" in r.stderr


def test_nested_import_resolves_relative_to_importing_file(tmp_path):
    root = make_repo(tmp_path / "r", claude="@docs/a.md\n",
                     extra={"docs/a.md": "@b.md\n", "docs/b.md": "deep\n"})
    assert run("--repo", root).returncode == 0
    assert "<!-- begin docs/b.md -->\ndeep\n<!-- end docs/b.md -->" in out_of(root)


def test_empty_import_keeps_markers(tmp_path):
    root = make_repo(tmp_path / "r", extra={"PROJECT.md": ""})
    assert run("--repo", root).returncode == 0
    assert "<!-- begin PROJECT.md -->\n<!-- end PROJECT.md -->" in out_of(root)


def test_crlf_sources_normalized(tmp_path):
    root = make_repo(tmp_path / "r", claude=b"# Top\r\n\r\n@PROJECT.md\r\n".decode(),
                     extra={"PROJECT.md": b"a\r\nb\r\n".decode()})
    (root / "CLAUDE.md").write_bytes(b"# Top\r\n\r\n@PROJECT.md\r\n")
    (root / "PROJECT.md").write_bytes(b"a\r\nb\r\n")
    assert run("--repo", root).returncode == 0
    data = (root / "AGENTS.md").read_bytes()
    assert b"\r" not in data and not data.startswith(b"\xef\xbb\xbf")
    assert "<!-- begin PROJECT.md -->\na\nb\n<!-- end PROJECT.md -->" in data.decode("utf-8")


# ---------------------------------------------------------------- setup section

def test_every_real_hook_command_in_table(real_copy):
    text = out_of(real_copy)
    data = json.loads((REAL / ".claude" / "settings.json").read_text(encoding="utf-8"))
    n = 0
    for groups in data["hooks"].values():
        for group in groups:
            for hook in group["hooks"]:
                assert "`%s`" % hook["command"] in text
                n += 1
    assert n >= 10
    assert "| Event | Matcher | Command | Purpose |" in text
    assert "Task\\|Agent" in text                       # pipes escaped inside table cells


def test_real_hook_purposes_are_docstring_first_paragraphs(real_copy):
    text = out_of(real_copy)
    first = agents_md._docstring_first_paragraph(real_copy, "hygiene_gate")
    assert first.startswith("hygiene_gate.py") and agents_md._cell(first) in text
    assert len(first) > len("hygiene_gate.py -- PreToolUse hook for command hygiene, for the")


def test_hook_purpose_is_the_whole_first_paragraph(tmp_path):
    settings = {"hooks": {"Stop": [{"hooks": [{"type": "command",
                                                "command": "python tools/hook_c.py"}]}]}}
    root = make_repo(tmp_path / "r", extra={
        ".claude/settings.json": json.dumps(settings),
        "tools/hook_c.py": '"""Blocks the turn\nfrom ending early.\n\nSecond paragraph stays out.\n"""\n'})
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "| Stop | `(none)` | `python tools/hook_c.py` | Blocks the turn from ending early. |" in text
    assert "Second paragraph" not in text


def test_tool_names_sentence_follows_the_settings(tmp_path):
    settings = json.loads(json.dumps(SETTINGS))
    settings["hooks"]["PostToolUse"] = [{"matcher": "Zap|MultiEdit|NotebookEdit", "hooks": [
        {"type": "command", "command": "python tools/hook_a.py"}]}]
    root = make_repo(tmp_path / "r", extra={".claude/settings.json": json.dumps(settings)})
    assert run("--repo", root).returncode == 0
    sentence = [ln for ln in out_of(root).split("\n") if ln.startswith("Configure the equivalent")][0]
    assert "events SessionStart, PreToolUse, PostToolUse" in sentence
    assert "tools Task, Agent, Zap, MultiEdit, NotebookEdit" in sentence
    assert "Stop" not in sentence                       # only what the settings carry


def test_real_tool_names_sentence_has_multiedit(real_copy):
    sentence = [ln for ln in out_of(real_copy).split("\n") if ln.startswith("Configure the equivalent")][0]
    assert "MultiEdit" in sentence and "NotebookEdit" in sentence and "SubagentStop" in sentence


def test_roles_sorted_case_independently(tmp_path):
    root = make_repo(tmp_path / "r", extra={".claude/agents/Zed.md": ROLE % ("Zed", "zed", "zed")})
    assert run("--repo", root).returncode == 0
    names = re.findall(r"^\| (alpha|beta|Zed) \|", out_of(root), re.M)
    assert names == ["alpha", "beta", "Zed"]                # a plain sorted() puts Zed first


def test_every_real_role_file_in_table(real_copy):
    text = out_of(real_copy)
    roles = sorted((REAL / ".claude" / "agents").glob("*.md"))
    assert len(roles) >= 5
    for f in roles:
        assert re.search(r"^\| %s \|" % re.escape(f.stem), text, re.M), f.name
    assert "| Role | Model | Tools | Description |" in text


def test_tier_words_from_validator(repo, real_copy):
    assert run("--repo", repo).returncode == 0
    text = out_of(repo)
    for word in ("haiku", "sonnet", "opus", "fable"):
        assert "`%s`" % word in text
    real_text = out_of(real_copy)
    for word in agents_md.tier_words(real_copy):
        assert "`%s`" % word in real_text
    assert set(agents_md.tier_words(real_copy)) == {"haiku", "sonnet", "opus", "fable"}


def test_tier_words_follow_the_validator_not_a_constant(tmp_path):
    root = make_repo(tmp_path / "r", extra={"tools/journal_validator.py":
                                            'TIER_ORDER = {"zeta": 0, "omega": 1}\n'})
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "`zeta`, `omega`" in text and "`fable`" not in text


def test_missing_validator_exit_2(tmp_path):
    root = make_repo(tmp_path / "r", extra={"tools/journal_validator.py": "x = 1\n"})
    r = run("--repo", root)
    assert r.returncode == 2 and "TIER_ORDER" in r.stderr


def test_hook_purposes_and_edges(repo):
    assert run("--repo", repo).returncode == 0
    text = out_of(repo)
    assert "| SessionStart | `(none)` | `python tools/hook_a.py` | Hook A does a thing. |" in text
    assert "| PreToolUse | `Task\\|Agent` | `python tools/hook_b.py` | (no docstring) |" in text
    assert "| PreToolUse | `Task\\|Agent` | `node other/thing.js` | (external command) |" in text


def test_settings_without_hooks(tmp_path):
    root = make_repo(tmp_path / "r", extra={".claude/settings.json": '{"model": "x"}'})
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "no hooks configured" in text and "| Event |" not in text


def test_settings_malformed_exit_2(tmp_path):
    root = make_repo(tmp_path / "r", extra={".claude/settings.json": "{not json"})
    r = run("--repo", root)
    assert r.returncode == 2 and "settings.json" in r.stderr


def test_role_without_frontmatter(tmp_path):
    root = make_repo(tmp_path / "r", extra={".claude/agents/gamma.md": "# just text\n"})
    assert run("--repo", root).returncode == 0
    text = out_of(root)
    assert "| gamma | (no frontmatter) | (no frontmatter) | (no frontmatter) |" in text
    assert "| alpha | m-alpha | Read, Grep | does alpha \\| with a pipe |" in text


def test_journal_note_covers_basis_for_non_claude_models(repo):
    assert run("--repo", repo).returncode == 0
    text = out_of(repo)
    assert "Work done by a non-Claude model still carries a `basis` on its `accepted` event" in text
    assert "function-tier words, not model ids" in text
    assert '"critic"' in text and '"queued-to-lead"' in text and '"judge"' in text


def test_git_hooks_and_journal_sections(repo):
    assert run("--repo", repo).returncode == 0
    text = out_of(repo)
    assert "git config core.hooksPath .githooks" in text
    assert text.rstrip("\n").split("\n")[-1].startswith("Journal note:")
    assert text.index("## Codex setup (this repository is built for Claude Code)") > text.index("project text")


# ---------------------------------------------------------------- size notice

NOTICE_RE = re.compile(r"This file is (\d+) bytes; .*`project_doc_max_bytes = (\d+)`")


def notice_numbers(data):
    m = NOTICE_RE.search(data.decode("utf-8"))
    assert m, "no size notice"
    return int(m.group(1)), int(m.group(2))


def test_size_notice_equals_real_size(repo):
    assert run("--repo", repo).returncode == 0
    data = (repo / "AGENTS.md").read_bytes()
    n, limit = notice_numbers(data)
    assert n == len(data)
    assert limit == -(-len(data) // 16384) * 16384


def test_real_size_notice(real_copy):
    data = (real_copy / "AGENTS.md").read_bytes()
    n, limit = notice_numbers(data)
    assert n == len(data) and limit >= n and limit % 16384 == 0 and limit - n < 16384


def _repo_of_size(root, target):
    """Tune PROJECT.md filler until the generated file is exactly `target` bytes."""
    make_repo(root)
    filler = 0
    for _ in range(50):
        (root / "PROJECT.md").write_text("x" * filler + "\n", encoding="utf-8")
        size = len(agents_md.build(root))
        if size == target:
            return root
        filler = max(0, filler + target - size)
    raise AssertionError("cannot tune the size to %d" % target)


@pytest.mark.parametrize("target,limit", [
    (16384 * 2 - 1, 16384 * 2),      # just below a boundary
    (16384 * 2, 16384 * 2),          # AT the boundary: the file fits exactly
    (16384 * 2 + 1, 16384 * 3),      # BEYOND it
    (16384 * 3, 16384 * 3),
    (16384 * 3 + 1, 16384 * 4),
])
def test_size_notice_at_and_beyond_a_16384_multiple(tmp_path, target, limit):
    root = _repo_of_size(tmp_path / "r", target)
    assert run("--repo", root).returncode == 0
    data = (root / "AGENTS.md").read_bytes()
    assert len(data) == target
    assert notice_numbers(data) == (target, limit)


def test_size_stays_exact_across_digit_boundaries():
    """The notice names its own size: exact even where the digit count of the size or of the
    limit changes (99999/100000, 98304/98305)."""
    checked = 0
    for centre in (9999, 10000, 16384, 32768, 98304, 99999, 100000, 114688):
        for k in range(centre - 400, centre + 40):
            data = agents_md.assemble(["x" * k], ["setup"])
            n, limit = notice_numbers(data)
            assert n == len(data), (k, n, len(data))
            assert limit == -(-n // 16384) * 16384
            checked += 1
    assert checked > 3000


def test_wrong_expected_size_is_detected(repo):
    """Control for the size test: comparing the notice with a deliberately wrong number differs."""
    assert run("--repo", repo).returncode == 0
    data = (repo / "AGENTS.md").read_bytes()
    n, _ = notice_numbers(data)
    assert n != len(data) + 1


# ---------------------------------------------------------------- --check

def test_check_0_after_write(repo):
    assert run("--repo", repo).returncode == 0
    assert run("--repo", repo, "--check").returncode == 0


def test_check_1_after_source_edit(repo):
    assert run("--repo", repo).returncode == 0
    (repo / "PROJECT.md").write_text("# Project\n\nchanged\n", encoding="utf-8")
    r = run("--repo", repo, "--check")
    assert r.returncode == 1 and "stale" in r.stdout


def test_check_1_when_missing(repo):
    r = run("--repo", repo, "--check")
    assert r.returncode == 1 and "missing" in r.stdout


def test_check_refusal_names_the_fix_with_repo(repo):
    """K4 (B-470): the stale/missing refusal names the regeneration command WITH --repo <this tree>, so it
    regenerates exactly the tree that was checked, from a git worktree or any cwd."""
    missing = run("--repo", repo, "--check")
    assert "--repo %s" % repo.resolve() in missing.stdout
    assert run("--repo", repo).returncode == 0
    (repo / "PROJECT.md").write_text("# Project\n\nchanged\n", encoding="utf-8")
    stale = run("--repo", repo, "--check")
    assert stale.returncode == 1 and "stale" in stale.stdout
    assert "python tools/agents_md.py --repo %s and stage AGENTS.md" % repo.resolve() in stale.stdout


def test_check_1_on_crlf_copy(repo):
    """The byte comparison stays strict: a CRLF checkout is refused; .gitattributes pins LF."""
    assert run("--repo", repo).returncode == 0
    path = repo / "AGENTS.md"
    fresh = path.read_bytes()
    assert b"\r" not in fresh
    path.write_bytes(fresh.replace(b"\n", b"\r\n"))
    r = run("--repo", repo, "--check")
    assert r.returncode == 1 and "stale" in r.stdout


def test_gitattributes_pins_agents_md_to_lf():
    lines = (REAL / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "AGENTS.md text eol=lf" in [ln.strip() for ln in lines]


def test_check_never_writes(repo):
    run("--repo", repo, "--check")
    assert not (repo / "AGENTS.md").exists()


def test_check_2_on_broken_source(tmp_path):
    root = make_repo(tmp_path / "r", claude="@nope.md\n")
    assert run("--repo", root, "--check").returncode == 2


def test_output_is_deterministic(repo):
    assert run("--repo", repo).returncode == 0
    first = (repo / "AGENTS.md").read_bytes()
    assert run("--repo", repo).returncode == 0
    assert (repo / "AGENTS.md").read_bytes() == first


def test_paths_resolve_from_script_not_cwd(repo, tmp_path):
    r = subprocess.run([sys.executable, "-B", str(SCRIPT), "--repo", str(repo)],
                       capture_output=True, text=True, cwd=str(tmp_path))
    assert r.returncode == 0 and (repo / "AGENTS.md").is_file()
