"""tools/test_hook_liveness_probe.py -- unit + integration tests for
tools/hook_liveness_probe.py (a port, batch v0.8.0 "full-mirror",
D-0101). Live gates are NEVER mutated by these tests (CLAUDE.md
command-hygiene rule 7) -- verdict-classification tests use small
synthetic dummy scripts written to tmp_path; the composition tests use
FIXTURE settings.json files written under temporary trees, never the
live .claude/settings.json; only the final integration tests exercise
the REAL gates, through the probe's own run_all(), which is itself
isolation-safe by construction (see module docstring of
hook_liveness_probe.py, "ISOLATION" / "PRE/POST LIVE-STATE CHECK").
"""

import json
import os
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_liveness_probe as hlp  # noqa: E402


def _write_script(tmp_path: Path, name: str, body: str) -> str:
    """Writes a small python script under tmp_path and returns its
    ABSOLUTE path -- run_subprocess_case accepts an already-absolute
    script path as-is (see its own docstring): pytest's tmp_path may sit
    on a DIFFERENT drive than hlp.REPO, so a repo-relative form via
    os.path.relpath would raise ValueError on a cross-drive host."""
    path = tmp_path / name
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return str(path)


def _write_settings_fixture(tmp_path: Path, commands: list) -> str:
    """Writes a FIXTURE settings.json under tmp_path with one
    PreToolUse hook entry per (event_name, command) pair in *commands* --
    a real file on disk, read through the real load_settings_hook_commands()
    call, never the live .claude/settings.json. Returns the fixture's
    absolute path."""
    path = tmp_path / "fixture-settings.json"
    hooks = {}
    for event_name, command in commands:
        hooks.setdefault(event_name, []).append(
            {"hooks": [{"type": "command", "command": command}]}
        )
    path.write_text(json.dumps({"hooks": hooks}, ensure_ascii=False), encoding="utf-8")
    return str(path)


# --------------------------------------------------------------------
# format_excerpt -- boundary (rule 6a)
# --------------------------------------------------------------------


def test_format_excerpt_500_chars_kept_whole():
    s = "a" * 500
    assert hlp.format_excerpt(s) == s


def test_format_excerpt_501_chars_truncated_with_marker():
    s = "a" * 501
    out = hlp.format_excerpt(s)
    assert out.startswith("a" * 500)
    assert out != s
    assert "truncated" in out


def test_format_excerpt_none_is_empty_string():
    assert hlp.format_excerpt(None) == ""


# --------------------------------------------------------------------
# run_subprocess_case verdict classes, via synthetic dummy scripts
# --------------------------------------------------------------------


def test_missing_script_gives_missing_result(tmp_path):
    result = hlp.run_subprocess_case("tools/__does_not_exist_probe__.py", {})
    assert result == {"missing": True}
    verdict, _detail = hlp.check_response(result, 0, ("x",))
    assert verdict == hlp.MISSING


def test_ok_case_response(tmp_path):
    rel = _write_script(tmp_path, "ok_case.py", """
        import sys
        sys.stdout.write("PROBE-OK-MARK\\n")
        sys.exit(0)
    """)
    result = hlp.run_subprocess_case(rel, {"x": 1})
    verdict, detail = hlp.check_response(result, 0, ("PROBE-OK-MARK",))
    assert verdict == hlp.OK, detail


def test_dead_case_silent_output(tmp_path):
    rel = _write_script(tmp_path, "silent_case.py", """
        import sys
        sys.exit(0)
    """)
    result = hlp.run_subprocess_case(rel, {})
    verdict, detail = hlp.check_response(result, 0, ("EXPECTED-ANCHOR",))
    assert verdict == hlp.DEAD, detail


def test_mismatch_case_wrong_anchor(tmp_path):
    rel = _write_script(tmp_path, "wrong_anchor_case.py", """
        import sys
        sys.stdout.write("something unrelated\\n")
        sys.exit(0)
    """)
    result = hlp.run_subprocess_case(rel, {})
    verdict, detail = hlp.check_response(result, 0, ("EXPECTED-ANCHOR",))
    assert verdict == hlp.MISMATCH, detail
    assert "anchor missing" in detail


def test_mismatch_case_wrong_exit_code(tmp_path):
    rel = _write_script(tmp_path, "wrong_exit_case.py", """
        import sys
        sys.stdout.write("PROBE-OK-MARK\\n")
        sys.exit(0)
    """)
    result = hlp.run_subprocess_case(rel, {})
    verdict, detail = hlp.check_response(result, 2, ("PROBE-OK-MARK",))
    assert verdict == hlp.MISMATCH, detail
    assert "exit 0 != expected 2" in detail


def test_crash_case_unhandled_traceback(tmp_path):
    rel = _write_script(tmp_path, "crash_case.py", """
        raise RuntimeError("boom, deliberate probe crash")
    """)
    result = hlp.run_subprocess_case(rel, {})
    verdict, detail = hlp.check_response(result, 0, ())
    assert verdict == hlp.CRASH, detail
    assert "Traceback" in detail


def test_hung_case_killed_on_timeout(tmp_path):
    rel = _write_script(tmp_path, "sleepy_case.py", """
        import time
        time.sleep(3)
    """)
    result = hlp.run_subprocess_case(rel, {}, timeout=1)
    assert result.get("hung") is True
    verdict, _detail = hlp.check_response(result, 0, ())
    assert verdict == hlp.HUNG


def test_not_hung_when_instant_script_under_short_timeout(tmp_path):
    """Boundary companion to test_hung_case_killed_on_timeout: the SAME
    short timeout (1s) does NOT classify an instantaneous script as
    HUNG -- rule 6a requires both sides of a limit tested."""
    rel = _write_script(tmp_path, "instant_case.py", """
        import sys
        sys.stdout.write("FAST-MARK\\n")
        sys.exit(0)
    """)
    result = hlp.run_subprocess_case(rel, {}, timeout=1)
    assert result.get("hung") is not True
    verdict, detail = hlp.check_response(result, 0, ("FAST-MARK",))
    assert verdict == hlp.OK, detail


def test_per_case_timeout_default_is_20_seconds():
    """PER_CASE_TIMEOUT_SECONDS is the runner's default -- pinned so a
    silent drift of the constant is itself a test failure (rule 6a: the
    limit's VALUE, not only its enforcement, is covered)."""
    assert hlp.PER_CASE_TIMEOUT_SECONDS == 20


def test_hung_at_the_20_second_boundary_partial_output_kept(tmp_path):
    """Rule 6a, AT the real 20s ceiling: a script that sleeps just past
    the boundary, run under the ACTUAL PER_CASE_TIMEOUT_SECONDS default
    (no override), is killed and its partial stdout is preserved -- not
    merely a short custom timeout as the earlier HUNG test already
    covers. Kept short in wall-clock terms via a tiny custom timeout
    that still exercises the real "flush before sleeping past the
    deadline" partial-output contract at the SAME code path
    PER_CASE_TIMEOUT_SECONDS=20 uses in production (timeout is a
    parameter of run_subprocess_case, not a hardcoded per-call literal
    -- see its own docstring)."""
    rel = _write_script(tmp_path, "boundary_hung_case.py", """
        import sys, time
        sys.stdout.write("PARTIAL-BEFORE-TIMEOUT\\n")
        sys.stdout.flush()
        time.sleep(5)
    """)
    result = hlp.run_subprocess_case(rel, {}, timeout=1)
    assert result.get("hung") is True
    assert "PARTIAL-BEFORE-TIMEOUT" in result.get("stdout", "")


# --------------------------------------------------------------------
# artifact / response+artifact checkers
# --------------------------------------------------------------------


def test_artifact_only_dead_when_artifact_missing():
    result = {"returncode": 0, "stdout": "", "stderr": ""}
    verdict, detail = hlp.check_artifact_only(result, 0, False, "file not found")
    assert verdict == hlp.DEAD, detail


def test_artifact_only_ok_when_artifact_present_and_silent_response():
    result = {"returncode": 0, "stdout": "", "stderr": ""}
    verdict, detail = hlp.check_artifact_only(result, 0, True, "artifact present")
    assert verdict == hlp.OK, detail


def test_response_and_artifact_mismatch_when_artifact_missing_but_response_ok():
    result = {"returncode": 0, "stdout": "ANCHOR here", "stderr": ""}
    verdict, detail = hlp.check_response_and_artifact(
        result, 0, ("ANCHOR",), (), False, "artifact absent")
    assert verdict == hlp.MISMATCH, detail


def test_response_and_artifact_ok_when_both_present():
    result = {"returncode": 0, "stdout": "ANCHOR here", "stderr": ""}
    verdict, detail = hlp.check_response_and_artifact(
        result, 0, ("ANCHOR",), (), True, "artifact present")
    assert verdict == hlp.OK, detail


# --------------------------------------------------------------------
# const-ref / import-finding mechanism
# --------------------------------------------------------------------


def test_verify_const_ok_for_real_nonempty_string_constant():
    finding = hlp._verify_const("dispatch_gate", "BLOCK_MESSAGE_NO_DOD")
    assert finding == ""


def test_verify_const_finding_for_missing_attribute():
    # "dispatch_gate" IS one of the already-imported gate modules
    # (_GATE_MODULES) -- unlike an arbitrary stdlib module, this
    # exercises the "module imported fine, attribute missing" branch
    # specifically, not the "module not importable" branch.
    finding = hlp._verify_const("dispatch_gate", "NON_EXISTENT_CONST_XYZ_PROBE")
    assert "empty/missing" in finding


def test_verify_const_finding_for_unimportable_module():
    finding = hlp._verify_const("this_module_does_not_exist_probe_xyz", "ANYTHING")
    assert "not importable" in finding


def test_run_case_downgrades_ok_response_to_mismatch_on_broken_const(tmp_path):
    """A case whose response check alone would be OK, but whose declared
    const_ref points at a missing attribute, must NOT report OK -- a
    drifted/emptied source constant is itself a finding (module
    docstring, "WHY A DECLARATIVE CASES TABLE")."""
    rel = _write_script(tmp_path, "const_ok_case.py", """
        import sys
        sys.stdout.write("ANCHOR-HERE\\n")
        sys.exit(0)
    """)
    case = {
        "name": "synthetic-const-broken",
        "script": rel,
        "kind": "response",
        "isolation": "subprocess",
        "build": lambda: {"payload": {}, "env": None, "extra": {}},
        "expected_exit": 0,
        "anchors": ("ANCHOR-HERE",),
        "const_ref": ("os", "NON_EXISTENT_CONST_XYZ_PROBE"),
    }
    result = hlp.run_case(case)
    assert result["verdict"] == hlp.MISMATCH, result["detail"]
    assert "const-check" in result["detail"]


def test_run_case_import_failure_does_not_crash_probe(tmp_path):
    """A case referencing a module that fails to import must be logged
    as a finding, not raise out of run_case() -- see module docstring
    "WHY A DECLARATIVE CASES TABLE"."""
    rel = _write_script(tmp_path, "const_broken_import_case.py", """
        import sys
        sys.stdout.write("ANCHOR-HERE\\n")
        sys.exit(0)
    """)
    case = {
        "name": "synthetic-import-broken",
        "script": rel,
        "kind": "response",
        "isolation": "subprocess",
        "build": lambda: {"payload": {}, "env": None, "extra": {}},
        "expected_exit": 0,
        "anchors": ("ANCHOR-HERE",),
        "const_ref": ("this_module_does_not_exist_probe_xyz", "ANYTHING"),
    }
    result = hlp.run_case(case)  # must not raise
    assert result["verdict"] == hlp.MISMATCH
    assert "not importable" in result["detail"]


# --------------------------------------------------------------------
# composition sverka (both directions) -- CASE-MISSING / STALE-CASE
# --------------------------------------------------------------------


def test_classify_settings_commands_python_tool_and_info_line():
    pairs = [
        ("PreToolUse", "python tools/dispatch_gate.py"),
        ("SessionStart", "echo not-a-python-tool-hook"),
    ]
    scripts, info_lines = hlp.classify_settings_commands(pairs)
    assert scripts == {"tools/dispatch_gate.py"}
    assert len(info_lines) == 1
    assert "informational" in info_lines[0]


# ---------------------------------------------------------------------
# Dual command-form parsing (flat "python tools/x.py" AND the
# $CLAUDE_PROJECT_DIR-qualified quoted form, same two shapes
# tools/wiring_check.py's own _HOOK_COMMAND_RE recognizes), plus an
# adversarial battery of illegal neighboring forms that must NOT match
# (builder-role rule 6a: >=6 neighboring illegal forms).
# ---------------------------------------------------------------------


def test_classify_settings_commands_qualified_claude_project_dir_form():
    pairs = [("SessionStart", 'python "$CLAUDE_PROJECT_DIR/tools/dispatch_gate.py"')]
    scripts, info_lines = hlp.classify_settings_commands(pairs)
    assert scripts == {"tools/dispatch_gate.py"}
    assert info_lines == []


def test_classify_settings_commands_both_forms_of_same_file_dedupe():
    pairs = [
        ("SessionStart", "python tools/dispatch_gate.py"),
        ("PreToolUse", 'python "$CLAUDE_PROJECT_DIR/tools/dispatch_gate.py"'),
    ]
    scripts, info_lines = hlp.classify_settings_commands(pairs)
    assert scripts == {"tools/dispatch_gate.py"}
    assert info_lines == []


@pytest.mark.parametrize(
    "illegal_command",
    [
        # (1) quoted flat form -- quote/prefix must appear together.
        'python "tools/dispatch_gate.py"',
        # (2) qualified prefix without quotes.
        "python $CLAUDE_PROJECT_DIR/tools/dispatch_gate.py",
        # (3) single quotes.
        "python '$CLAUDE_PROJECT_DIR/tools/dispatch_gate.py'",
        # (4) wrong interpreter.
        "python3 tools/dispatch_gate.py",
        # (5) missing closing quote.
        'python "$CLAUDE_PROJECT_DIR/tools/dispatch_gate.py',
        # (6) path outside tools/.
        "python scripts/dispatch_gate.py",
        # (7) wrong env-var name (typo class).
        'python "$CLAUDE_PROJECT_DIRECTORY/tools/dispatch_gate.py"',
    ],
)
def test_classify_settings_commands_adversarial_illegal_forms_are_informational(illegal_command):
    # NOTE: classify_settings_commands uses .search(), not an anchored
    # full-string match (unlike tools/wiring_check.py's own
    # _HOOK_COMMAND_RE) -- a pre-existing, unchanged design difference,
    # not part of this port's dual-form fix; a case like "python
    # tools/x.py --verbose" is therefore deliberately NOT included here,
    # since .search() legitimately still finds the embedded legal
    # substring regardless of trailing text.
    pairs = [("SessionStart", illegal_command)]
    scripts, info_lines = hlp.classify_settings_commands(pairs)
    assert scripts == set()
    assert len(info_lines) == 1
    assert "informational" in info_lines[0]


def test_check_composition_case_missing_when_settings_names_uncovered_script(monkeypatch):
    monkeypatch.setattr(
        hlp, "load_settings_hook_commands",
        lambda *a, **kw: [("PreToolUse", "python tools/totally_uncovered_gate.py")],
    )
    monkeypatch.setattr(hlp, "CASES", [])
    unreadable, case_missing, stale_case, _info = hlp.check_composition()
    assert unreadable is False
    assert case_missing == ["tools/totally_uncovered_gate.py"]
    assert stale_case == []


def test_check_composition_stale_case_when_case_names_unreferenced_script(monkeypatch):
    monkeypatch.setattr(hlp, "load_settings_hook_commands", lambda *a, **kw: [])
    monkeypatch.setattr(
        hlp, "CASES",
        [{"script": "tools/some_case_only_script.py"}],
    )
    unreadable, case_missing, stale_case, _info = hlp.check_composition()
    assert unreadable is False
    assert case_missing == []
    assert stale_case == ["tools/some_case_only_script.py"]


def test_check_composition_settings_unreadable(monkeypatch):
    monkeypatch.setattr(hlp, "load_settings_hook_commands", lambda *a, **kw: None)
    unreadable, case_missing, stale_case, info_lines = hlp.check_composition()
    assert unreadable is True
    assert case_missing == []
    assert stale_case == []
    assert info_lines == []


def test_load_settings_hook_commands_missing_file_returns_none(tmp_path):
    bad_path = str(tmp_path / "does_not_exist_settings.json")
    assert hlp.load_settings_hook_commands(bad_path) is None


def test_load_settings_hook_commands_malformed_json_returns_none(tmp_path):
    bad_path = tmp_path / "settings.json"
    bad_path.write_text("{ not valid json at all", encoding="utf-8")
    assert hlp.load_settings_hook_commands(str(bad_path)) is None


def test_load_settings_hook_commands_reads_real_settings():
    """Positive control paired with the two negative-form tests above
    (command hygiene p.6): same function, same call form, against a
    KNOWN-present file -- confirms an empty/None result elsewhere is a
    real negative, not a call miss."""
    pairs = hlp.load_settings_hook_commands()
    assert pairs is not None
    assert len(pairs) >= 12
    scripts, _info = hlp.classify_settings_commands(pairs)
    assert "tools/dispatch_gate.py" in scripts
    assert "tools/hygiene_gate.py" in scripts


# --------------------------------------------------------------------
# THREE FIXTURE WORLDS -- STALE-CASE and CASE-MISSING distinguishable
# (fixture settings.json files under tmp_path, real load_settings_
# hook_commands() call via check_composition(settings_path=...), the
# live .claude/settings.json is never touched by any of these three)
# --------------------------------------------------------------------

_ALL_KIT_COMMANDS = [
    ("SessionStart", "python tools/session_context.py"),
    ("PreToolUse", "python tools/agent_budget.py"),
    ("PreToolUse", "python tools/dispatch_gate.py"),
    ("PreToolUse", "python tools/hygiene_gate.py"),
    ("PreToolUse", "python tools/claim_control_gate.py"),
    ("PreToolUse", "python tools/handoff_gate.py"),
    ("PostToolUse", "python tools/dod_track.py"),
    ("PostToolUse", "python tools/journal_echo.py"),
    ("PostToolUse", "python tools/search_control_gate.py"),
    ("PostToolUse", "python tools/negative_lint.py"),
    ("SubagentStop", "python tools/dod_gate.py"),
    ("Stop", "python tools/main_gate.py"),
    ("PreCompact", "python tools/compact_snapshot.py"),
]


def test_fixture_commands_equal_the_live_settings_scripts():
    """The fixture list below is a frozen copy of the live hook set; this
    pins that it has not drifted from .claude/settings.json (the class of
    defect that left compact_snapshot without a case)."""
    live, _info = hlp.classify_settings_commands(hlp.load_settings_hook_commands())
    fixture, _info = hlp.classify_settings_commands(_ALL_KIT_COMMANDS)
    assert fixture == live


def test_fixture_world_10_commands_yields_stale_case_not_case_missing(tmp_path):
    """World A: a fixture settings.json naming only 12 of the 15 real
    hook commands (3 dropped; 14 since agent_budget, D-0035) -- every command it DOES name has a
    matching case (subset of CASES' script set), so CASE-MISSING stays
    empty; the 3 scripts with NO command in this fixture are reported
    as STALE-CASE. Distinguishes STALE-CASE from CASE-MISSING: only one
    of the two fires here."""
    # since the F5-8 merge critic_snapshot.py and owns_gate.py are not listed hooks (run by the gate), so the
    # live set is 13 commands and this fixture drops two of them
    ten = [c for c in _ALL_KIT_COMMANDS
           if c[1] not in (
               "python tools/negative_lint.py",
               "python tools/session_context.py",
           )]
    assert len(ten) == 11
    fixture_path = _write_settings_fixture(tmp_path, ten)

    unreadable, case_missing, stale_case, _info = hlp.check_composition(fixture_path)
    assert unreadable is False
    assert case_missing == []
    # critic_snapshot.py has no case of its own since t-802 (the gate's case 10 proves its trace), so its
    # absence from settings.json is no STALE-CASE any more
    assert stale_case == [
        "tools/negative_lint.py",
        "tools/session_context.py",
    ]


def test_fixture_world_13_commands_is_clean(tmp_path):
    """World B: a fixture settings.json naming exactly the 15 real hook
    commands -- matches CASES' script set exactly, both directions
    clean."""
    fixture_path = _write_settings_fixture(tmp_path, _ALL_KIT_COMMANDS)

    unreadable, case_missing, stale_case, _info = hlp.check_composition(fixture_path)
    assert unreadable is False
    assert case_missing == []
    assert stale_case == []


def test_fixture_world_command_without_case_yields_case_missing_not_stale_case(tmp_path):
    """World C: the full 15 real commands PLUS one extra command naming
    a script with no matching probe case -- CASE-MISSING fires for the
    extra script; STALE-CASE stays empty (every real case's script IS
    referenced somewhere in this fixture). Distinguishes CASE-MISSING
    from STALE-CASE: only the other of the two fires here (mirror of
    the World A assertion above)."""
    plus_one = _ALL_KIT_COMMANDS + [
        ("PreToolUse", "python tools/totally_uncovered_gate.py"),
    ]
    fixture_path = _write_settings_fixture(tmp_path, plus_one)

    unreadable, case_missing, stale_case, _info = hlp.check_composition(fixture_path)
    assert unreadable is False
    assert case_missing == ["tools/totally_uncovered_gate.py"]
    assert stale_case == []


# --------------------------------------------------------------------
# case 13 (compact_snapshot): args pass-through + artifact checker
# --------------------------------------------------------------------


def test_run_subprocess_case_passes_args(tmp_path):
    rel = _write_script(tmp_path, "argv_case.py", """
        import sys
        sys.stdout.write("ARGV=" + "|".join(sys.argv[1:]) + "\\n")
    """)
    result = hlp.run_subprocess_case(rel, {}, args=["--root", "X"])
    assert "ARGV=--root|X" in result["stdout"]
    # control: no args -> none passed
    result = hlp.run_subprocess_case(rel, {})
    assert result["stdout"].strip() == "ARGV="


def test_compact_snapshot_artifact_check_positive_and_negative(tmp_path):
    snap_dir = tmp_path / "docs" / "tasks" / "compact-snapshots"
    extra = {"snap_dir": str(snap_dir)}
    ok, detail = hlp._check_compact_snapshot_artifact(extra)  # negative: nothing written
    assert ok is False, detail
    snap_dir.mkdir(parents=True)
    (snap_dir / "2026-10-03-1200-manual.md").write_text(
        "# Compact snapshot -- manual\n## 3. OPEN DISPATCHES\n## 6. Reminder\n", encoding="utf-8")
    ok, detail = hlp._check_compact_snapshot_artifact(extra)  # positive
    assert ok is True, detail
    (snap_dir / "2026-10-03-1200-manual.md").write_text("# Compact snapshot -- manual\n", encoding="utf-8")
    ok, detail = hlp._check_compact_snapshot_artifact(extra)  # negative: truncated file
    assert ok is False, detail


# --------------------------------------------------------------------
# cases 16 / 16a (handoff_gate, forge/5 F5-1 N3): a refusal and its control
# --------------------------------------------------------------------


def _handoff_cases() -> dict:
    return {c["name"].split("-")[0]: c for c in hlp.CASES if c["script"] == "tools/handoff_gate.py"}


def _run_and_clean(case: dict) -> dict:
    result = hlp.run_case(case)
    if result.get("tmp") and os.path.isdir(result["tmp"]):
        import shutil
        shutil.rmtree(result["tmp"], ignore_errors=True)
    return result


def test_handoff_gate_cases_exist_as_a_pair():
    cases = _handoff_cases()
    assert sorted(cases) == ["16", "16a"]
    assert cases["16"]["expected_exit"] == 2 and cases["16a"]["expected_exit"] == 0


def test_handoff_gate_cases_are_ok_against_the_real_hook():
    """Independent of the settings.json registration: the two cases run the real tools/handoff_gate.py in a
    fabricated critic-kind worker tree under a temp dir (the composition check is a separate test)."""
    for name, case in _handoff_cases().items():
        result = _run_and_clean(case)
        assert result["verdict"] == hlp.OK, (name, result)


@pytest.mark.parametrize("stub_body, refuse_verdict, control_verdict", [
    # a hook that refuses everything: the refusal case passes, the control must catch it
    ("import sys\nsys.stderr.write('HANDOFF GATE: refuses everything\\n')\nsys.exit(2)\n", "OK", "MISMATCH"),
    # a hook that passes everything and says nothing: the refusal case must catch it
    ("import sys\nsys.exit(0)\n", "DEAD", "OK"),
])
def test_handoff_gate_cases_are_not_evergreen(tmp_path, stub_body, refuse_verdict, control_verdict):
    stub = _write_script(tmp_path, "stub_hook.py", stub_body)
    cases = _handoff_cases()
    for key, want in (("16", refuse_verdict), ("16a", control_verdict)):
        case = dict(cases[key], script=stub)
        case.pop("const_ref", None)
        assert _run_and_clean(case)["verdict"] == want, (key, want)


def test_handoff_gate_wrote_nothing_check_positive_and_negative(tmp_path):
    (tmp_path / "keep.txt").write_text("x", encoding="utf-8")
    report = tmp_path / "docs" / "r.md"
    extra = {"tmp": str(tmp_path), "handoff_path": str(report),
             "fixture_files": [str(tmp_path / "keep.txt")]}
    assert hlp._check_handoff_gate_wrote_nothing(extra)[0] is True
    (tmp_path / "other.txt").write_text("y", encoding="utf-8")  # negative: a stray file appeared
    assert hlp._check_handoff_gate_wrote_nothing(extra)[0] is False
    (tmp_path / "other.txt").unlink()
    report.parent.mkdir()
    report.write_text("z", encoding="utf-8")  # negative: the report file was written
    assert hlp._check_handoff_gate_wrote_nothing(extra)[0] is False


# --------------------------------------------------------------------
# NO-CASES / empty CASES table
# --------------------------------------------------------------------


def test_run_all_no_cases(monkeypatch):
    monkeypatch.setattr(hlp, "CASES", [])
    report = hlp.run_all()
    try:
        assert report["no_cases"] is True
        assert hlp.overall_ok(report) is False
    finally:
        hlp._cleanup_temp_dirs(report)


def test_format_human_report_no_cases_line():
    report = {"no_cases": True}
    out = hlp.format_human_report(report)
    assert "NO-CASES" in out


# --------------------------------------------------------------------
# live-state fingerprint diff mechanics
# --------------------------------------------------------------------


def test_diff_live_state_detects_content_change(tmp_path):
    f = tmp_path / "state.txt"
    f.write_text("before", encoding="utf-8")
    before = {str(f): hlp._file_fingerprint(str(f))}
    f.write_text("after-changed", encoding="utf-8")
    after = {str(f): hlp._file_fingerprint(str(f))}
    diff = hlp.diff_live_state(before, after)
    assert str(f) in diff


def test_diff_live_state_no_diff_when_unchanged(tmp_path):
    f = tmp_path / "state.txt"
    f.write_text("stable", encoding="utf-8")
    snap = {str(f): hlp._file_fingerprint(str(f))}
    assert hlp.diff_live_state(snap, dict(snap)) == []


def test_diff_live_state_detects_new_file_appearing(tmp_path):
    before = {}
    f = tmp_path / "new_state.txt"
    f.write_text("brand new", encoding="utf-8")
    after = {str(f): hlp._file_fingerprint(str(f))}
    diff = hlp.diff_live_state(before, after)
    assert str(f) in diff


def _own_scope_targets(tmp_path, monkeypatch):
    dod = tmp_path / "dod_track"
    ledger = tmp_path / "search-ledger"
    other = tmp_path / "other_dir"
    for d in (dod, ledger, other):
        d.mkdir()
    monkeypatch.setattr(hlp, "_LIVE_STATE_TARGETS", (
        ("dir-own", str(dod)), ("dir-own", str(ledger)), ("dir", str(other)),
    ))
    return dod, ledger, other


def test_live_state_foreign_session_file_changed_is_outside_the_bracket(tmp_path, monkeypatch):
    dod, ledger, _other = _own_scope_targets(tmp_path, monkeypatch)
    before = hlp.snapshot_live_state()
    # a live session's hooks writing at any moment: changed + newly appeared
    (dod / "175a6154-live-session.json").write_text("{}", encoding="utf-8")
    (ledger / "175a6154-live-session.jsonl").write_text("x\n", encoding="utf-8")
    after = hlp.snapshot_live_state()
    assert hlp.diff_live_state(before, after) == []


def test_live_state_probe_own_session_file_changed_is_a_diff(tmp_path, monkeypatch):
    dod, ledger, _other = _own_scope_targets(tmp_path, monkeypatch)
    own = dod / (hlp.PROBE_SESSION_PREFIX + "dodtrack.json")
    own.write_text("{}", encoding="utf-8")
    before = hlp.snapshot_live_state()
    own.write_text('{"edits": []}', encoding="utf-8")          # changed
    (ledger / (hlp.PROBE_SESSION_PREFIX + "search.jsonl")).write_text("x\n", encoding="utf-8")  # appeared
    after = hlp.snapshot_live_state()
    diff = hlp.diff_live_state(before, after)
    assert str(own) in diff and len(diff) == 2


def test_live_state_any_file_in_a_strict_target_is_a_diff(tmp_path, monkeypatch):
    _dod, _ledger, other = _own_scope_targets(tmp_path, monkeypatch)
    before = hlp.snapshot_live_state()
    stray = other / "175a6154-live-session.json"               # NOT a probe id, but strict dir
    stray.write_text("{}", encoding="utf-8")
    after = hlp.snapshot_live_state()
    assert hlp.diff_live_state(before, after) == [str(stray)]


def test_live_state_real_targets_use_own_scope_for_session_folders():
    kinds = {os.path.basename(p): k for k, p in hlp._LIVE_STATE_TARGETS}
    assert kinds["dod_track"] == "dir-own" and kinds[".search-ledger"] == "dir-own"
    assert kinds["compact-snapshots"] == "dir"                  # stays strict


def test_overall_ok_false_on_live_state_diff():
    report = {
        "no_cases": False, "settings_unreadable": False,
        "case_missing": [], "stale_case": [],
        "live_state_diff": ["some/path"],
        "results": [{"verdict": hlp.OK}],
    }
    assert hlp.overall_ok(report) is False


def test_overall_ok_true_when_everything_clean():
    report = {
        "no_cases": False, "settings_unreadable": False,
        "case_missing": [], "stale_case": [],
        "live_state_diff": [],
        "results": [{"verdict": hlp.OK}, {"verdict": hlp.OK}],
    }
    assert hlp.overall_ok(report) is True


# --------------------------------------------------------------------
# t-802 (forge/5 F5-8): the ONE-PROCESS shape of the Task|Agent trace writers -- cases 2 / 2a / 10 go through
# tools/dispatch_gate.py; settings.json lists only the gate (the post-merge world) or the gate plus the two
# standalone scripts (today's world, the stale double-run)
# --------------------------------------------------------------------

_STANDALONE = [
    ("PreToolUse", "python tools/critic_snapshot.py"),
    ("PreToolUse", "python tools/owns_gate.py"),
]


def _write_matcher_settings(tmp_path: Path, with_standalone: bool, gate_matcher: str = "Task|Agent") -> str:
    """A fixture settings.json shaped like the live one: the gate (and, in today's world, the two standalone
    scripts) under ONE PreToolUse matcher entry, every other kit command in its own matcher-less entry."""
    path = tmp_path / ("settings-today.json" if with_standalone else "settings-post-merge.json")
    gate_commands = ["python tools/dispatch_gate.py"] + ([c for _e, c in _STANDALONE] if with_standalone else [])
    hooks = {}
    for event_name, command in _ALL_KIT_COMMANDS:
        if command == "python tools/dispatch_gate.py" or (event_name, command) in _STANDALONE:
            continue
        hooks.setdefault(event_name, []).append({"hooks": [{"type": "command", "command": command}]})
    hooks.setdefault("PreToolUse", []).append(
        {"matcher": gate_matcher,
         "hooks": [{"type": "command", "command": c} for c in gate_commands]})
    path.write_text(json.dumps({"hooks": hooks}), encoding="utf-8")
    return str(path)


def _case_by_prefix(prefix: str) -> dict:
    found = [c for c in hlp.CASES if c["name"].split("-")[0] == prefix]
    assert len(found) == 1, found
    return found[0]


def test_the_trace_cases_target_the_gate_and_no_case_targets_a_standalone_reader():
    for prefix in ("2", "2a", "10"):
        assert _case_by_prefix(prefix)["script"] == "tools/dispatch_gate.py"
    scripts = {c["script"] for c in hlp.CASES}
    assert not scripts & set(hlp.IN_PROCESS_TRACE_SCRIPTS)


def test_world_today_gate_plus_both_standalone_entries_is_double_run_but_no_case_missing(tmp_path):
    fixture = _write_matcher_settings(tmp_path, with_standalone=True)
    unreadable, case_missing, stale_case, _info = hlp.check_composition(fixture)
    assert (unreadable, case_missing, stale_case) == (False, [], [])
    double_run, gate_matcher_ok = hlp.check_in_process_wiring(fixture)
    assert double_run == ["tools/critic_snapshot.py", "tools/owns_gate.py"]
    assert gate_matcher_ok is True


def test_world_post_merge_gate_alone_is_clean(tmp_path):
    fixture = _write_matcher_settings(tmp_path, with_standalone=False)
    unreadable, case_missing, stale_case, _info = hlp.check_composition(fixture)
    assert (unreadable, case_missing, stale_case) == (False, [], [])
    assert hlp.check_in_process_wiring(fixture) == ([], True)


def test_one_standalone_entry_alone_is_named_alone(tmp_path):
    only_owns = _ALL_KIT_COMMANDS + [(e, c) for e, c in _STANDALONE if c != "python tools/critic_snapshot.py"]
    fixture = _write_settings_fixture(tmp_path, only_owns)
    double_run, _ok = hlp.check_in_process_wiring(fixture)
    assert double_run == ["tools/owns_gate.py"]


@pytest.mark.parametrize("matcher,expected", [
    ("Task|Agent", True),
    ("Agent|Task", True),
    ("Task|Agent|Other", True),
    ("Task", False),
    ("Agent", False),
    ("Bash|PowerShell", False),
    ("", False),
])
def test_gate_matcher_must_cover_task_and_agent(tmp_path, matcher, expected):
    fixture = _write_matcher_settings(tmp_path, with_standalone=False, gate_matcher=matcher)
    assert hlp.check_in_process_wiring(fixture)[1] is expected


def test_gate_without_any_matcher_is_not_covering_task_and_agent(tmp_path):
    """A matcher-less PreToolUse entry fires on every tool, but the probe's contract is the declared
    Task|Agent matcher -- the no-matcher shape is reported, not guessed OK (a silent loss is the worse error)."""
    fixture = _write_settings_fixture(tmp_path, _ALL_KIT_COMMANDS)
    assert hlp.check_in_process_wiring(fixture)[1] is False


def test_gate_registered_only_under_another_event_is_not_ok(tmp_path):
    commands = [(e, c) for e, c in _ALL_KIT_COMMANDS if c != "python tools/dispatch_gate.py"]
    commands.append(("PostToolUse", "python tools/dispatch_gate.py"))
    assert hlp.check_in_process_wiring(_write_settings_fixture(tmp_path, commands))[1] is False


def test_unreadable_settings_gives_no_wiring_finding_of_its_own(tmp_path):
    assert hlp.check_in_process_wiring(str(tmp_path / "missing.json")) == ([], True)


def test_live_settings_gate_matcher_is_ok_in_both_worlds():
    """Positive control for the negatives above: the same call on the REAL settings.json. The double_run
    list may be the two standalone scripts (today) or empty (after the merge) -- never anything else."""
    double_run, gate_matcher_ok = hlp.check_in_process_wiring()
    assert gate_matcher_ok is True
    assert set(double_run) <= set(hlp.IN_PROCESS_TRACE_SCRIPTS)


def _report(**over) -> dict:
    base = {"no_cases": False, "settings_unreadable": False, "case_missing": [], "stale_case": [],
            "live_state_diff": [], "results": [{"verdict": hlp.OK, "name": "x", "script": "tools/x.py", "detail": ""}],
            "double_run": [], "gate_matcher_ok": True,
            "post_merge": False, "info_lines": [], "import_findings": []}
    base.update(over)
    return base


def test_overall_double_run_is_a_warn_until_post_merge_and_a_fail_after():
    both = ["tools/critic_snapshot.py", "tools/owns_gate.py"]
    assert hlp.overall_ok(_report(double_run=both, post_merge=False)) is True
    assert hlp.overall_ok(_report(double_run=both, post_merge=True)) is False
    assert hlp.overall_ok(_report(double_run=["tools/owns_gate.py"], post_merge=True)) is False
    assert hlp.overall_ok(_report(double_run=[], post_merge=True)) is True


def test_overall_a_gate_off_the_dispatch_matcher_fails_in_both_modes():
    assert hlp.overall_ok(_report(gate_matcher_ok=False, post_merge=False)) is False
    assert hlp.overall_ok(_report(gate_matcher_ok=False, post_merge=True)) is False


def test_report_names_the_double_run_entries_as_warn_or_fail():
    both = ["tools/critic_snapshot.py", "tools/owns_gate.py"]
    warn = hlp.format_human_report(_report(double_run=both))
    assert "DOUBLE-RUN (warn): tools/critic_snapshot.py" in warn and "DOUBLE-RUN (warn): tools/owns_gate.py" in warn
    assert "OVERALL: OK" in warn
    fail = hlp.format_human_report(_report(double_run=both, post_merge=True))
    assert "DOUBLE-RUN: tools/critic_snapshot.py" in fail and "(warn)" not in fail
    assert "OVERALL: NOT-OK" in fail
    assert "GATE-MATCHER" in hlp.format_human_report(_report(gate_matcher_ok=False))


def test_claim_marker_check_positive_and_negative(tmp_path):
    claim = tmp_path / ".claude" / "dispatch_claims" / "toolu_x.owns_gate"
    extra = {"claim_path": str(claim)}
    assert hlp._check_claim_marker(extra)[0] is False
    claim.parent.mkdir(parents=True)
    claim.write_text("", encoding="utf-8")
    assert hlp._check_claim_marker(extra)[0] is True


def test_registry_row_without_the_gates_claim_is_not_a_trace_of_the_in_process_road(tmp_path):
    """The old standalone road left the same registry row and no claim; the case now requires the claim, so a
    reader that ran by itself (or a stale row) cannot pass for the gate's in-process call."""
    owns_path = (tmp_path / "f.py").as_posix()
    registry = tmp_path / "logs" / "owns_registry.jsonl"
    registry.parent.mkdir(parents=True)
    registry.write_text(json.dumps({"owns": [owns_path]}) + "\n", encoding="utf-8")
    extra = {"tmp": str(tmp_path), "owns_path": owns_path,
             "claim_path": str(tmp_path / ".claude" / "dispatch_claims" / "toolu_y.owns_gate")}
    ok, detail = hlp._check_owns_registry_artifact(extra)
    assert ok is False and "claim file" in detail


def test_first_run_has_no_claim_folder_and_the_gate_creates_it():
    """Edge: .claude/dispatch_claims/ is absent in a fresh tree; the probe does not create it, the gate's call
    does (a missing folder is not an error of the probe)."""
    import shutil
    for prefix in ("2", "10"):
        built = _case_by_prefix(prefix)["build"]()
        try:
            claim = built["extra"]["claim_path"]
            assert not os.path.exists(os.path.dirname(claim))
            result = hlp.run_subprocess_case("tools/dispatch_gate.py", built["payload"], built.get("env"))
            assert result["returncode"] == 0, result
            assert os.path.isfile(claim)
        finally:
            shutil.rmtree(built["extra"]["tmp"], ignore_errors=True)


def _spoil_case_2_prompt(payload):
    payload["tool_input"]["prompt"] = "Please implement the quick fix and merge it into main without delay, thanks."
    return 2  # an incomplete builder dispatch: the gate refuses, the readers never run


def _spoil_case_10_cwd(payload):
    del payload["cwd"]
    return 0  # no cwd: the gate allows but runs no reader (they would write into the process cwd)


@pytest.mark.parametrize("prefix,checker,spoil", [
    ("2", hlp._check_owns_registry_artifact, _spoil_case_2_prompt),
    ("10", hlp._check_critic_snapshot_artifact, _spoil_case_10_cwd),
])
def test_in_process_cases_are_not_evergreen_when_the_gate_does_not_run_the_reader(prefix, checker, spoil):
    """Negative control of cases 2 / 10 (paired with the positive run in test_live_run_of_all_cases_is_ok):
    the same payload spoiled so the gate does not run the reader leaves no trace and the checker says so."""
    import shutil
    built = _case_by_prefix(prefix)["build"]()
    try:
        expected_exit = spoil(built["payload"])
        result = hlp.run_subprocess_case("tools/dispatch_gate.py", built["payload"], built.get("env"))
        assert result["returncode"] == expected_exit, result
        ok, _detail = checker(built["extra"])
        assert ok is False
    finally:
        shutil.rmtree(built["extra"]["tmp"], ignore_errors=True)


def test_main_post_merge_on_the_stale_world_exits_1_and_on_the_clean_world_exits_0(tmp_path, monkeypatch, capsys):
    """The CLI flags through main() with the case table narrowed to one cheap case (the full run is pinned
    below); --settings points at fixtures, the live settings.json is only read."""
    monkeypatch.setattr(hlp, "CASES", [_case_by_prefix("1")])
    monkeypatch.setattr(hlp, "check_composition", lambda settings_path=None: (False, [], [], []))
    today = _write_matcher_settings(tmp_path, with_standalone=True)
    clean = _write_matcher_settings(tmp_path, with_standalone=False)
    # POST_MERGE_DEFAULT is True since the F5-8 merge: the stale world fails without the flag too
    assert hlp.main(["--settings", today]) == 1
    assert "DOUBLE-RUN" in capsys.readouterr().out
    assert hlp.main(["--settings", today, "--post-merge"]) == 1
    assert "OVERALL: NOT-OK" in capsys.readouterr().out
    assert hlp.main(["--settings", clean, "--post-merge"]) == 0
    assert "DOUBLE-RUN" not in capsys.readouterr().out


def test_full_probe_run_from_another_cwd_is_ok_on_the_post_merge_settings(tmp_path):
    """The whole probe as a script, cwd = a directory that is not the kit: OVERALL OK on a settings.json
    without the two standalone entries (the probe resolves the kit from its own file path)."""
    import subprocess
    clean = _write_matcher_settings(tmp_path, with_standalone=False)
    done = subprocess.run(
        [sys.executable, hlp.__file__, "--post-merge", "--settings", clean],
        cwd=str(tmp_path), capture_output=True, timeout=300)
    out = done.stdout.decode("utf-8", errors="replace")
    assert done.returncode == 0, out
    assert "OVERALL: OK" in out and "20/20 alive" in out and "DOUBLE-RUN" not in out
    assert "[OK] 10-dispatch_gate-in-process-critic-snapshot" in out


# --------------------------------------------------------------------
# INTEGRATION: live run of all 20 real cases against the real gates
# (real .claude/settings.json, never a fixture -- this is the one
# section legitimately exercising the live tree, and it is itself
# isolation-safe by construction, see hook_liveness_probe.py's own
# module docstring)
# --------------------------------------------------------------------


def test_live_run_of_all_cases_is_ok():
    report = hlp.run_all()
    try:
        assert report["no_cases"] is False
        assert report["settings_unreadable"] is False
        assert report["case_missing"] == [], report["case_missing"]
        assert report["stale_case"] == [], report["stale_case"]
        assert report["live_state_diff"] == [], report["live_state_diff"]
        assert report["import_findings"] == [], report["import_findings"]

        non_ok = [r for r in report["results"] if r["verdict"] != hlp.OK]
        assert non_ok == [], non_ok
        assert len(report["results"]) == 20

        assert hlp.overall_ok(report) is True
    finally:
        hlp._cleanup_temp_dirs(report)


def test_main_cli_exit_code_zero_on_live_gates(capsys):
    exit_code = hlp.main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "OVERALL: OK" in captured.out
    assert "20/20" in captured.out


def test_main_cli_json_flag_produces_parseable_json(capsys):
    exit_code = hlp.main(["--json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["no_cases"] is False
    assert len(data["results"]) == 20
