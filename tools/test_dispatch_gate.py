"""Unit/smoke tests for tools/dispatch_gate.py. Direct calls to
decide() for every branch, plus an echo-JSON subprocess smoke test
(mirrors the calling convention of tools/test_mechanism_gate.py).

Run from the repo root: python -m pytest tools/test_dispatch_gate.py
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dispatch_gate  # noqa: E402
import md_regions as _md_regions  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "dispatch_gate.py"
# FLIPPED (B-204/B-245): a relative path is a candidate by the ONE predicate (first segment = a
# top-level entry of the root); the old repo-relative prefix list is gone, the caller supplies the entries
_TOP = frozenset({"tools", "gateway", "docs"})


def _run_hook(payload) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload) if isinstance(payload, dict) else payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _builder_payload(prompt: str, description=None) -> dict:
    tool_input = {"subagent_type": "builder", "prompt": prompt}
    if description is not None:
        tool_input["description"] = description
    return {"tool_name": "Task", "tool_input": tool_input}


# B-201: a builder dispatch is checked for completeness by
# dispatch_manifest.check (tools/dispatch_manifest.py), called from decide().
# _manifest() builds a dispatch in the new form: header lines given:, owns:
# (absolute path), non-goals:, handoff:, edges:, DoD: (a command in
# backticks). Each keyword replaces one default line; a line given as None
# is left out.
# The owned path lies outside any repo root (a foreign drive) and the DoD
# command names an existing file, so the given-path WARN layer stays silent
# on a passing dispatch.
_OWNED_PATH = "Z:/factory-x/tools/x.py"
_DOD_LINE = "DoD: `python -m pytest tools/test_dispatch_gate.py -q`"


def _manifest(given="the whole repo", owns=_OWNED_PATH, non_goals="none", handoff="a short report",
              edges="none -- nothing to limit", dod=_DOD_LINE, prefix="", suffix="",
              siblings="none -- a test fixture", designer="skip -- a test fixture"):
    lines = []
    if given is not None:
        lines.append(f"given: {given}")
    if owns is not None:
        lines.append(f"owns: {owns}")
    if non_goals is not None:
        lines.append(f"non-goals: {non_goals}")
    if handoff is not None:
        lines.append(f"handoff: {handoff}")
    if edges is not None:
        lines.append(f"edges: {edges}")
    if dod is not None:
        lines.append(dod)
    if siblings is not None:
        lines.append(f"siblings: {siblings}")
    if designer is not None:
        lines.append(f"designer: {designer}")
    text = "\n".join(lines)
    return (prefix + "\n" if prefix else "") + text + ("\n" + suffix if suffix else "")


# F6-37: a critic/designer dispatch names one .md path directly inside its role folder (or carries a skip line).
_CRITIC_HANDOFF = "handoff: Z:/factory-x/docs/tasks/specs/reviews/t-1.md"
_DESIGNER_HANDOFF = "handoff: Z:/factory-x/docs/tasks/specs/t-1.md"
_HANDOFF_BY_KIND = {"critic": _CRITIC_HANDOFF, "designer": _DESIGNER_HANDOFF}

_R = "Z:/r"  # an absolute repo root outside any real drive
_REV = _R + "/docs/tasks/specs/reviews"
_SPEC = _R + "/docs/tasks/specs"


def _kind_payload(kind, prompt):
    return {"tool_name": "Task", "tool_input": {"subagent_type": kind, "prompt": prompt, "description": "opus: x"}}


def _many_paths():
    return "handoff: " + " ".join("%s/t-%d.md" % (_REV, i) for i in range(1000))


# (id, kind, prompt, code, text that the message must hold, text that the note must hold)
_NO_LINE = "no handoff: line"
_FOLDER_ROWS = [
    ("e1", "critic", "handoff: Z:\\r\\docs\\tasks\\handoffs\\t-1.md", 2, ["docs/tasks/specs/reviews", "none of them"], ""),
    ("e2", "critic", "handoff: Z:\\r\\docs\\tasks\\specs\\reviews\\t-1.md", 0, [], ""),
    ("e3", "designer", "handoff: %s/t-1.md" % _REV, 2, ["docs/tasks/specs, the designer's"], ""),
    ("e4", "designer", "handoff: %s/t-1.md" % _SPEC, 0, [], ""),
    ("e5", "critic", "Review the diff.", 2, [_NO_LINE], ""),
    ("e6", "critic", "handoff: docs/tasks/specs/reviews/t-1.md", 2, ["no absolute path", "write it as an absolute path"], ""),
    ("e7", "critic", "handoff: %s/<t>.md" % _REV, 2, ["no absolute path"], ""),
    ("e8", "critic", "handoff: %s/t-1.txt" % _REV, 2, ["none of them"], ""),
    ("e9", "critic", "handoff: %s/t-1.md %s/t-2.md" % (_REV, _REV), 2, ["2 distinct", "t-1.md", "t-2.md"], ""),
    ("e10", "critic", "handoff: %s/t-1.md %s/T-1.md" % (_REV, _REV.replace("/", "\\")), 0, [], ""),
    ("e11", "critic", "Review.\n```\nhandoff: %s/t-1.md\n```" % _REV, 2, [_NO_LINE], ""),
    ("e12", "critic", "Review.\n> handoff: %s/t-1.md" % _REV, 2, [_NO_LINE], ""),
    ("e13", "critic", "Review.\nmanifest-skip: handoff -- text report", 0, [], "sent without a report path on purpose"),
    ("e14", "critic", "Review.\nmanifest-skip: handoff", 2, [_NO_LINE], ""),
    ("e15", " Critic ", "handoff: Z:\\r\\docs\\tasks\\handoffs\\t-1.md", 2, ["none of them"], ""),
    ("e16-builder", "builder", "handoff: Z:/r/docs/other/t-1.md", 0, [], ""),
    ("e16-scout", "scout", "handoff: Z:/r/docs/other/t-1.md", 0, [], ""),
    ("e16-gp", "general-purpose", "handoff: Z:/r/docs/other/t-1.md", 0, [], ""),
    ("e16-namespaced", "foo:critic", "handoff: Z:/r/docs/other/t-1.md", 0, [], ""),
    ("e17", "critic", "handoff: %s/t-1.md\n%s" % (_REV, "x" * (_md_regions.MAX_TEXT_CHARS + 1)), 0, [], "not checked"),
    ("e18-empty", "critic", "", 2, [_NO_LINE], ""),
    ("e18-none", "critic", None, 2, [_NO_LINE], ""),
    ("e19", "critic", _many_paths(), 2, ["1000 distinct", "and 995 more"], ""),
    ("e20", "critic", "handoff: %s/\u043e\u0442\u0447\u0451\u0442.md" % _REV, 0, [], ""),
    ("e21", "critic", "```\nan unterminated fence\nhandoff: %s/t-1.md" % _REV, 0, [], ""),
]


@pytest.mark.parametrize("name,kind,prompt,code,message_has,note_has", _FOLDER_ROWS, ids=[r[0] for r in _FOLDER_ROWS])
def test_handoff_folder_check(name, kind, prompt, code, message_has, note_has):
    payload = _kind_payload(kind, prompt)
    dm = dispatch_gate._load_manifest_module()
    _is_builder, cut = dm.cut_payload(payload)
    got_code, message, note = dispatch_gate.handoff_folder_check(payload, cut, dm)
    assert got_code == code, (message, note)
    for part in message_has:
        assert part in message, (part, message)
    assert (note_has in note) if note_has else (note == ""), note
    if code == 2:
        assert message.startswith("HANDOFF PATH (CLAUDE.md rule 11, R11-h)")
        assert "Door:" in message or "add a line:" in message  # every refusal names a door


def test_handoff_folder_check_e19_shows_five_paths_only():
    payload = _kind_payload("critic", _many_paths())
    message = dispatch_gate.decide(payload)[1]
    assert message.count("/t-") == 5 and "t-4.md" in message and "t-5.md" not in message


def test_handoff_folder_check_e22_the_completeness_refusal_comes_first():
    prompt = "owns: Z:/r/x.py\nhandoff: Z:/r/docs/tasks/handoffs/t-1.md"
    code, message = dispatch_gate.decide(_kind_payload("critic", prompt))
    assert code == 2 and message.startswith("DISPATCH INCOMPLETE") and "HANDOFF PATH" not in message


def test_handoff_folder_check_e23_an_import_failure_is_a_note_and_a_pass(monkeypatch):
    monkeypatch.setitem(sys.modules, "handoff_gate", None)  # `import handoff_gate` now raises ImportError
    payload = _kind_payload("critic", "Review the diff.")
    decision = dispatch_gate.decide_full(payload)
    assert decision.code == 0
    assert any("HANDOFF CHECK: not checked (tools/handoff_gate.py did not import)" in n for n in decision.notes)


def test_handoff_folder_check_e25_a_failed_cut_is_a_note_and_a_pass(monkeypatch):
    # section_cut raising leaves cut None: an UNKNOWN, not "no handoff: line" (spec A.4: an unknown is never a refusal)
    dm = dispatch_gate._load_manifest_module()

    def boom(prompt):
        raise RuntimeError("boom")

    monkeypatch.setattr(dm, "section_cut", boom)
    payload = _kind_payload("critic", "Review.\n" + _CRITIC_HANDOFF)
    decision = dispatch_gate.decide_full(payload)
    assert decision.code == 0, decision.message
    assert any("HANDOFF CHECK: not checked" in n for n in decision.notes), decision.notes
    # direct call with no cut: the word is there -> note and pass; the word is absent -> still the refusal
    code, message, note = dispatch_gate.handoff_folder_check(payload, None, dm)
    assert code == 0 and message == "" and "HANDOFF CHECK: not checked" in note
    code, message, note = dispatch_gate.handoff_folder_check(_kind_payload("critic", "Review."), None, dm)
    assert code == 2 and _NO_LINE in message and "add a line:" in message


def test_decide_full_handoff_refusal_keeps_the_label_check_behind_it():
    payload = _kind_payload("critic", "Review.")
    payload["tool_input"]["description"] = "nolabel"
    assert "HANDOFF PATH" in dispatch_gate.decide(payload)[1]  # the handoff refusal is first
    payload["tool_input"]["prompt"] = "Review.\n" + _CRITIC_HANDOFF
    assert "worker's tier" in dispatch_gate.decide(payload)[1]  # a valid handoff reaches the label check as before


# ---------------------------------------------------------------------
# Not Task/Agent -- always passes.
# ---------------------------------------------------------------------


def test_non_task_tool_passes():
    exit_code, message = dispatch_gate.decide({"tool_name": "Bash", "tool_input": {}})
    assert exit_code == 0
    assert message == ""


def test_missing_tool_input_does_not_crash():
    exit_code, message = dispatch_gate.decide({"tool_name": "Task"})
    assert exit_code == 0


# ---------------------------------------------------------------------
# Check 1: DoD markers for builder.
# ---------------------------------------------------------------------


def test_builder_without_dod_markers_blocks():
    # old: message contained "no DoD" / "rule 11" (BLOCK_MESSAGE_NO_DOD)
    # new: the completeness refusal, DoD among the missing items
    exit_code, message = dispatch_gate.decide(
        _builder_payload("Just fix a typo in file x.py.", description="sonnet: fix typo")
    )
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message
    assert "DoD (no line)" in message
    assert "rule 11" in message


def test_builder_with_dod_literal_passes_check1():
    # old: "Fix the typo. DoD: test is green." -> 0; new: the same premise
    # (a passing builder dispatch with a DoD line) in the full new form
    exit_code, message = dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Fix the typo."), description="sonnet: fix")
    )
    assert exit_code == 0
    assert message == ""


def test_builder_without_siblings_line_is_refused_end_to_end_and_passes_with_it():
    # t-113 F2: the E1 form check reaches the gate -- a complete builder dispatch WITHOUT `siblings:` is refused
    # with the INCOMPLETE text naming siblings; the same dispatch with the line goes out
    exit_code, message = dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Fix the typo.", siblings=None), description="sonnet: fix")
    )
    assert exit_code == 2
    assert message.startswith("DISPATCH INCOMPLETE (CLAUDE.md rule 11): this builder dispatch does not go out.")
    assert "Missing: siblings (no line)." in message
    assert dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Fix the typo."), description="sonnet: fix")
    ) == (0, "")


def test_builder_with_acceptance_criteria_en_no_longer_a_dod_header():
    # old (..._passes_check1): the phrase "acceptance criteria" anywhere was a DoD marker
    # new: only a header line dod|witness|verification counts -> DoD is missing
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="Acceptance criteria: the test passes, run `python -m pytest x`"),
            description="sonnet: fix",
        )
    )
    assert exit_code == 2
    assert "DoD (no line)" in message


def test_builder_with_criteria_priyomki_cyrillic_no_longer_a_dod_header():
    # old (..._passes_check1): the Cyrillic phrase was a DoD marker
    # new: no Cyrillic DoD header exists (only ДАНО is bilingual) -> DoD is missing
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="Критерии приёмки: тест зелёный, `python -m pytest x`"),
            description="sonnet: fix",
        )
    )
    assert exit_code == 2
    assert "DoD (no line)" in message


def test_builder_with_witness_passes_check1():
    # old: "attach a witness." (a word in prose) -> 0; new: a witness: header with a command
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="witness: `python -m pytest tools/x.py -q`"), description="sonnet: fix"
        )
    )
    assert exit_code == 0, message


def test_builder_with_verification_run_en_passes_check1():
    # old: "run a verification run." (prose) -> 0; new: a verification: header with a command
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="Verification run: `python -m pytest tools/x.py -q`"),
            description="sonnet: fix",
        )
    )
    assert exit_code == 0, message


def test_builder_with_progon_cyrillic_no_longer_a_dod_header():
    # old (..._passes_check1): "проверочный прогон" in prose was a DoD marker
    # new: no such header key -> DoD is missing
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="Проверочный прогон: `python -m pytest x`"), description="sonnet: fix"
        )
    )
    assert exit_code == 2
    assert "DoD (no line)" in message


def test_dod_marker_case_insensitive():
    # old: "a fix. dod: green test." -> 0; new: a lowercase dod: header with a command
    exit_code, _ = dispatch_gate.decide(
        _builder_payload(_manifest(dod="dod: `python -m pytest x`"), description="sonnet: x")
    )
    assert exit_code == 0


# ---------------------------------------------------------------------
# Write-indicator word-boundary behavior (a Cyrillic root marker
# matches only as a standalone word, not as a substring of
# longer inflected words -- see WRITE_INDICATORS_RE / the test below).
# ---------------------------------------------------------------------


def test_pravj_word_boundary_does_not_match_poprav_or_isprav():
    # old: decide() on a builder prompt with "поправь"/"исправь" -> 0 (no write signal)
    # new: decide() no longer reads WRITE_INDICATORS_RE (a builder is always checked);
    # the word-boundary premise is pinned on the regex itself, which stays in the file
    assert not dispatch_gate.WRITE_INDICATORS_RE.search("Please, поправь опечатку in file x.py.")
    assert not dispatch_gate.WRITE_INDICATORS_RE.search("Please, исправь опечатку in file x.py.")


def test_pravj_word_boundary_still_matches_standalone_word():
    # old: decide() on "Правь file x.py" without a manifest -> 2 "context manifest"
    # new: the regex still matches the standalone word; decide() refuses the
    # manifest-less builder dispatch with the completeness message
    assert dispatch_gate.WRITE_INDICATORS_RE.search("DoD: test is green. Правь file x.py per the spec.")
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            "DoD: test is green. Правь file x.py per the spec.",
            description="sonnet: fix",
        )
    )
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message


# ---------------------------------------------------------------------
# Check 2: manifest on a writing builder dispatch.
# ---------------------------------------------------------------------


def test_builder_readonly_prompt_is_refused_without_the_full_form_and_passes_with_it():
    # old: a read-only builder prompt (no write signal) skipped check 2 -> 0
    # new: a builder is ALWAYS checked; the read-only prompt is refused, and the
    # same task written in the full form passes
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            "Read file x.py and tell me what's in it. DoD: an explicit yes/no answer.",
            description="sonnet: read",
        )
    )
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message
    exit_code2, message2 = dispatch_gate.decide(
        _builder_payload(
            _manifest(prefix="Read file x.py and tell me what's in it."), description="sonnet: read"
        )
    )
    assert exit_code2 == 0, message2


def test_builder_write_indicator_without_manifest_blocks():
    # old: "context manifest" / "given/owns" in the message; new: given and owns among the missing
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            "DoD: test is green. Edit file x.py per the spec.", description="sonnet: fix"
        )
    )
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message
    assert "given (no line)" in message
    assert "owns (no line)" in message


def test_builder_write_indicator_with_full_manifest_passes():
    # old: "MANIFEST: given -- ...; owns -- tools/x.py." inline; new: header lines, absolute owns path
    prompt = _manifest(prefix="Create file x.py.")
    exit_code, message = dispatch_gate.decide(
        _builder_payload(prompt, description="sonnet: write x")
    )
    assert exit_code == 0
    assert message == ""


def test_builder_write_indicator_with_only_owns_blocks():
    # old: owns present, given absent -> 2 "context manifest"; new: the same premise, given is named
    prompt = _manifest(given=None, prefix="Modify file x.py.")
    exit_code, message = dispatch_gate.decide(
        _builder_payload(prompt, description="sonnet: write x")
    )
    assert exit_code == 2
    assert "Missing: given (no line)." in message


def test_builder_write_indicator_with_only_given_blocks():
    # old: given present, owns absent -> 2 "context manifest"; new: the same premise, owns is named
    prompt = _manifest(owns=None, prefix="Create file x.py.")
    exit_code, message = dispatch_gate.decide(
        _builder_payload(prompt, description="sonnet: write x")
    )
    assert exit_code == 2
    assert "Missing: owns (no line)." in message


def test_builder_given_and_owns_both_present_passes():
    # old: inline "Given: ... owns: tools/x.py" -> 0; new: the full form (absolute owns path)
    prompt = _manifest(prefix="Create file x.py.")
    exit_code, _ = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: write x"))
    assert exit_code == 0


def test_builder_write_indicator_en_forms_without_manifest_block():
    for phrase in ["write file x.py", "create file x.py", "edit file x.py", "modify file x.py"]:
        exit_code, message = dispatch_gate.decide(
            _builder_payload(f"DoD: witness present. Please {phrase}.", description="sonnet: x")
        )
        assert exit_code == 2, phrase
        assert "DISPATCH INCOMPLETE" in message


# ---------------------------------------------------------------------
# Check 3: description starts with a leading token + separator.
# ---------------------------------------------------------------------


def test_missing_description_skips_check3():
    # old premise "a passing builder dispatch" kept; fixture in the full new form
    exit_code, message = dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Read the file."))
    )
    assert exit_code == 0
    assert message == ""


def test_description_with_no_separator_blocks():
    # fixture in the full new form, so the completeness check passes and the label check is reached
    exit_code, message = dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Read the file."), description="fixbugnow")
    )
    assert exit_code == 2
    assert "worker's tier" in message
    assert "rule 7" in message


def test_description_with_leading_token_and_separator_passes():
    # A FORM-only check (see module docstring): any leading token
    # followed by a space/colon/dash passes, regardless of whether the
    # token names a real tier -- this template has no fixed model list.
    for prefix in ["sonnet: ", "sonnet-", "sonnet ", "haiku: ", "opus: ", "fable: "]:
        exit_code, message = dispatch_gate.decide(
            _builder_payload(
                _manifest(prefix="Read the file."), description=f"{prefix}does the work"
            )
        )
        assert exit_code == 0, f"prefix {prefix!r} should pass, got {message!r}"


def test_description_check_applies_to_critic():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": "critic", "prompt": "Review the diff.\n" + _CRITIC_HANDOFF,
                       "description": "reviewthediff"},
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 2
    assert "worker's tier" in message


def test_description_check_applies_to_scout():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": "scout", "prompt": "Find the file.", "description": "findfile"},
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 2
    assert "worker's tier" in message


def test_description_check_passes_for_critic_with_leading_token():
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "critic",
            "prompt": "Review the diff.\n" + _CRITIC_HANDOFF,
            "description": "opus: review diff",
        },
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 0


# ---------------------------------------------------------------------
# Point 4: critic/scout -- checks 1 and 2 do not apply.
# ---------------------------------------------------------------------


def test_critic_without_dod_markers_not_blocked_by_check1():
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "critic",
            "prompt": "Review the diff, not a single DoD word here.\n" + _CRITIC_HANDOFF,
            "description": "opus: review",
        },
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 0


def test_scout_write_indicator_without_manifest_not_blocked_by_check2():
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "scout",
            "prompt": "Edit file x and create file notes.md (this is NOT builder, check 2 does not apply).",
            "description": "haiku: scout",
        },
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 0


# ---------------------------------------------------------------------
# Priority 1 -> 2 -> 3 when several checks fail at once.
# ---------------------------------------------------------------------


def test_priority_dod_wins_over_label():
    # old: "no DoD" wins over the label; new: the completeness refusal (DoD among the
    # missing) wins over the label, the label message is not reported
    exit_code, message = dispatch_gate.decide(
        _builder_payload("Edit file x.py.", description="fixitnow")
    )
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message
    assert "DoD (no line)" in message
    assert "worker's tier" not in message


def test_priority_manifest_wins_over_label():
    # old: "context manifest" wins over the label; new: a dispatch whose only gap is
    # owns, plus a bad label: the completeness refusal is the one reported
    prompt = _manifest(owns=None, prefix="Edit file x.py.")
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="fixitnow"))
    assert exit_code == 2
    assert "Missing: owns (no line)." in message
    assert "worker's tier" not in message


# ---------------------------------------------------------------------
# echo-JSON subprocess smoke tests.
# ---------------------------------------------------------------------


def test_echo_json_blocks_builder_without_dod():
    # old: "no DoD" on stderr; new: the completeness refusal, DoD among the missing
    result = _run_hook(_builder_payload("Just a fix.", description="sonnet: fix"))
    assert result.returncode == 2
    assert "DISPATCH INCOMPLETE" in result.stderr
    assert "DoD (no line)" in result.stderr


def test_echo_json_passes_builder_with_dod():
    # premise kept (a passing builder dispatch); fixture in the full new form
    result = _run_hook(
        _builder_payload(_manifest(prefix="Fix it."), description="sonnet: fix")
    )
    assert result.returncode == 0
    assert result.stderr == ""
    # FLIPPED (B-245): a builder dispatch without a cwd passes, and says so (P11)
    assert json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"] == (
        "PATH CHECK: paths unchecked: no cwd")


def test_echo_json_blocks_missing_manifest():
    # old: "context manifest" on stderr; new: given and owns among the missing
    result = _run_hook(
        _builder_payload("DoD: test is green. Edit file x.py.", description="sonnet: fix")
    )
    assert result.returncode == 2
    assert "DISPATCH INCOMPLETE" in result.stderr
    assert "given (no line)" in result.stderr


def test_echo_json_blocks_bad_label():
    # fixture in the full new form so the label check is reached
    result = _run_hook(
        _builder_payload(_manifest(prefix="Read the file."), description="fixbugnow")
    )
    assert result.returncode == 2
    assert "worker's tier" in result.stderr


def test_echo_json_malformed_json_fails_open():
    # old: exit 0 with empty stderr; new: still exit 0 (fail-open), but with the
    # UNCHECKED NOTE on stderr and additionalContext
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input="{not valid json",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "MANIFEST-UNCHECKED:" in result.stderr
    assert "payload unreadable: malformed JSON (JSONDecodeError)" in result.stderr
    assert "payload unreadable: malformed JSON" in json.loads(result.stdout)[
        "hookSpecificOutput"]["additionalContext"]


# ---------------------------------------------------------------------
# Byte-safe stdin: the hook must decode stdin as UTF-8 explicitly (not
# through the platform's locale encoding) -- proven with two forms,
# ASCII-safe \uXXXX escapes AND raw UTF-8 bytes fed without
# text=True/encoding on subprocess (the exact way a harness feeds a
# child process's stdin).
# ---------------------------------------------------------------------

_CYRILLIC_MANIFEST_PAYLOAD = {
    "tool_name": "Task",
    "tool_input": {
        "subagent_type": "builder",
        # old: one prose line "DoD: критерии приёмки ... Дано: ... owns: tools/x.py. Правь ..."
        # new: the full form, with the Cyrillic given header ДАНО: and Cyrillic body text
        "prompt": (
            "Правь файл x.py по спеке.\n"
            "ДАНО: репо целиком\n"
            "owns: C:/proj/tools/x.py\n"
            "non-goals: не трогать другие файлы\n"
            "handoff: краткий отчёт\n"
            "edges: none -- границ нет\n"
            "DoD: критерии приёмки — тест зелёный, `python -m pytest tools/x.py -q`\n"
            "siblings: none -- a test fixture\n"
        ),
        "description": "sonnet: fix",
    },
}


def test_cyrillic_markers_recognized_via_ascii_safe_json_escapes():
    raw = json.dumps(_CYRILLIC_MANIFEST_PAYLOAD, ensure_ascii=True).encode("ascii")
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")


def test_cyrillic_markers_recognized_via_raw_utf8_bytes():
    raw = json.dumps(_CYRILLIC_MANIFEST_PAYLOAD, ensure_ascii=False).encode("utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------
# Marker word-boundary hardening: a bare filename substring must not
# count as a real marker (DOD_MARKERS_RE, MANIFEST_GIVEN_RE,
# MANIFEST_OWNS_RE). Closed holes: a false match used to let a builder
# dispatch with no real marker slip past the corresponding check.
# ---------------------------------------------------------------------


def test_dod_gate_filename_substring_is_no_longer_a_dod_marker():
    """A basket mentioning tools/dod_gate.py, with no real DoD line
    anywhere else in the prompt, must still be refused -- "dod" as a
    substring of the filename is not a DoD header. (old: "no DoD" in the
    message; new: "DoD (no line)" among the missing items.)"""
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(given="tools/dod_gate.py for reference", dod=None, prefix="Just fix a typo."),
            description="sonnet: fix",
        )
    )
    assert exit_code == 2
    assert "Missing: DoD (no line)." in message


def test_dod_marker_colon_and_hyphen_forms_still_match():
    """The legal header forms still count: "DoD:" and "DoD-marker:" (a
    hyphen is a non-word char, up to 160 characters may sit between the key
    and the colon). old: "DoD-marker" in prose; new: as a header line."""
    exit_code, _ = dispatch_gate.decide(
        _builder_payload(_manifest(prefix="Fix the typo."), description="sonnet: fix")
    )
    assert exit_code == 0

    exit_code2, _ = dispatch_gate.decide(
        _builder_payload(
            _manifest(dod="DoD-marker: `python -m pytest tools/x.py -q`", prefix="Fix the typo."),
            description="sonnet: fix",
        )
    )
    assert exit_code2 == 0


def test_witness_echo_filename_substring_is_no_longer_a_dod_marker():
    """A basket mentioning tools/test_witness_echo.py, with no real
    witness line anywhere else, must still be refused -- "witness" inside
    the underscore-joined filename is not a header. (old: "no DoD"; new:
    "DoD (no line)".)"""
    exit_code, message = dispatch_gate.decide(
        _builder_payload(
            _manifest(
                given="tools/test_witness_echo.py for reference", dod=None, prefix="Just fix a typo."
            ),
            description="sonnet: fix",
        )
    )
    assert exit_code == 2
    assert "Missing: DoD (no line)." in message


def test_manifest_given_word_boundary_prodano_false_positive_fixed():
    """Covers the RU marker-pair false-positive case: a longer Russian
    word containing the given-marker as a mere substring ("продано"
    contains "дано") is not a given header -- a builder dispatch whose
    ONLY occurrence of that substring is inside "продано" is still refused
    for a missing given. (old: "context manifest"; new: "given (no line)".)"""
    prompt = _manifest(given=None, prefix="На складе всё продано.")
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
    assert exit_code == 2
    assert "Missing: given (no line)." in message


def test_manifest_given_real_forms_unaffected_by_word_boundary():
    """Legal given header forms keep matching: Given:, and the Russian
    "Дано:" / "ДАНО:" (case-insensitive). The old no-colon form
    "дано -- ..." is no longer a header (a header needs its colon): it
    is refused as a missing given."""
    for given_line in ("Given: the whole repo", "Дано: репо целиком", "ДАНО: репо целиком"):
        key, _sep, body = given_line.partition(": ")
        prompt = _manifest(given=None, prefix=f"{key}: {body}")
        exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
        assert exit_code == 0, message

    prompt = _manifest(given=None, prefix="дано -- репо целиком")
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
    assert exit_code == 2
    assert "Missing: given (no line)." in message


def test_owns_filename_substring_is_no_longer_an_owns_marker():
    """A basket mentioning a filename that merely CONTAINS "owns" as a
    substring (not the standalone word "owns") must not satisfy the
    owns item. (old: "context manifest"; new: "owns (no line)".)"""
    prompt = _manifest(
        given="tools/ownership_report.py for reference", owns=None, prefix="Правь file x.py."
    )
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
    assert exit_code == 2
    assert "Missing: owns (no line)." in message


def test_owns_real_marker_unaffected_by_word_boundary():
    prompt = _manifest(prefix="Edit file x.py.")
    exit_code, _ = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
    assert exit_code == 0


def test_readonly_dispatch_mentioning_ownership_filename_in_given_not_blocked():
    """The reverse edge of the same class: a builder dispatch in the full
    form whose given mentions a filename containing "owns" as a substring
    is not blocked. (old: a read-only prompt with no write signal skipped
    check 2; a builder is now always checked, so the premise is kept as
    "a passing dispatch" with a full manifest.)"""
    prompt = _manifest(given="tools/ownership_report.py", prefix="Tell me what it does.")
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: fix"))
    assert exit_code == 0, message


# =======================================================================
# Given-path WARN layer (Part A): extraction, root/foreign-tree
# handling, noise threshold, and the main()-level wiring.
# =======================================================================


def test_extract_given_candidates_absolute_and_repo_relative():
    prompt = (
        "Given: D:\\repo\\tools\\x.py and also tools/y.py and gateway/z.yaml for reference."
    )
    candidates = dispatch_gate.extract_given_candidates(prompt, _TOP)
    toks = [c[0] for c in candidates]
    assert "D:\\repo\\tools\\x.py" in toks
    assert "tools/y.py" in toks
    assert "gateway/z.yaml" in toks


def test_extract_given_candidates_dedup_and_order_of_first_appearance():
    prompt = "Given: tools/x.py, then again tools/x.py, then tools/y.py."
    candidates = dispatch_gate.extract_given_candidates(prompt, _TOP)
    toks = [c[0] for c in candidates]
    assert toks == ["tools/x.py", "tools/y.py"]


def test_extract_given_candidates_absolute_and_relative_forms_not_double_counted():
    """An absolute path like "D:/repo/tools/x.py" must not ALSO be
    picked up by the repo-relative regex as "tools/x.py" -- the
    negative lookbehind before the repo-relative prefix excludes a
    prefix immediately preceded by a path separator."""
    prompt = "Given: D:/repo/tools/x.py for reference."
    candidates = dispatch_gate.extract_given_candidates(prompt)
    toks = [c[0] for c in candidates]
    assert toks.count("tools/x.py") == 0
    assert "D:/repo/tools/x.py" in toks


def test_extract_given_candidates_placeholders_not_extracted():
    prompt = "Given: <path/to/file>, *.py, {name}.py, $VAR.py -- none of these are real paths."
    candidates = dispatch_gate.extract_given_candidates(prompt)
    assert candidates == []


@pytest.mark.skipif(
    os.name != "nt",
    reason="Windows path semantics: _is_under_root on drive-letter backslash paths (os.path.normpath is POSIX-flavoured on Linux)",
)
def test_is_under_root_true_inside_false_outside():
    assert dispatch_gate._is_under_root("D:\\repo\\tools\\x.py", "D:\\repo")
    assert not dispatch_gate._is_under_root("D:\\OtherTree\\x.py", "D:\\repo")


def test_find_missing_given_paths_existing_file_not_missing(tmp_path):
    (tmp_path / "tools").mkdir()
    real_file = tmp_path / "tools" / "x.py"
    real_file.write_text("# real")
    prompt = f"Given: {real_file} for reference."
    missing = dispatch_gate.find_missing_given_paths(prompt, str(tmp_path))
    assert missing == []


@pytest.mark.skipif(os.name != "nt", reason="B-302: the gate recognises only drive-absolute paths")
def test_find_missing_given_paths_missing_file_reported(tmp_path):
    missing_path = tmp_path / "tools" / "does_not_exist.py"
    prompt = f"Given: {missing_path} for reference."
    missing = dispatch_gate.find_missing_given_paths(prompt, str(tmp_path))
    assert missing == [str(missing_path)]


def test_find_missing_given_paths_foreign_tree_absolute_path_skipped(tmp_path):
    """An absolute path OUTSIDE repo_root (a foreign tree) is not
    checked at all -- neither reported missing nor treated as an
    error, even though it obviously does not exist under repo_root."""
    foreign = "D:\\SomeOtherTree\\nope.py"
    prompt = f"Given: {foreign} for reference."
    missing = dispatch_gate.find_missing_given_paths(prompt, str(tmp_path))
    assert missing == []


def test_find_missing_given_paths_existing_directory_not_reported(tmp_path):
    """A path candidate that resolves to an EXISTING DIRECTORY (not a
    file) is not reported missing -- os.path.exists() is true for
    directories too; documented behavior, not a bug to fix here."""
    (tmp_path / "tools").mkdir()
    # A directory won't normally match the file-extension-requiring
    # regexes, so simulate the documented case directly via the
    # lower-level helper: a repo-relative candidate whose resolved path
    # is a directory that happens to carry a dotted suffix.
    weird_dir = tmp_path / "tools" / "x.py"
    weird_dir.mkdir()
    prompt = "Given: tools/x.py for reference."
    missing = dispatch_gate.find_missing_given_paths(prompt, str(tmp_path))
    assert missing == []


def test_format_given_path_warn_empty_list_returns_empty_string():
    assert dispatch_gate.format_given_path_warn([]) == ""


def test_format_given_path_warn_threshold_boundary_10_vs_11():
    ten = [f"tools/f{i}.py" for i in range(10)]
    eleven = [f"tools/f{i}.py" for i in range(11)]

    warn_ten = dispatch_gate.format_given_path_warn(ten)
    assert "GIVEN-PATH WARN" in warn_ten
    for path in ten:
        assert path in warn_ten
    assert "first 3" not in warn_ten

    warn_eleven = dispatch_gate.format_given_path_warn(eleven)
    assert "11 paths do not exist" in warn_eleven
    assert "first 3" in warn_eleven
    for path in eleven[:3]:
        assert path in warn_eleven
    assert eleven[-1] not in warn_eleven


# --- critic finding: the path body is bounded to {0,300} instead of a
# greedy `*` (protection against quadratic backtracking on a
# pathological prompt). ------------------------------------------------

def test_extract_given_candidates_body_exactly_300_chars_extracted():
    body = "a" * 300
    prompt = f"Given: D:\\{body}.py for reference."
    candidates = dispatch_gate.extract_given_candidates(prompt)
    toks = [c[0] for c in candidates]
    assert f"D:\\{body}.py" in toks


def test_extract_given_candidates_body_301_chars_is_one_candidate_now():
    # FLIPPED: the 300-character regex truncation is gone with the regexes; a long token is ONE
    # absolute candidate (the section check classifies it; a foreign tree is never stat'ed)
    body = "a" * 301
    prompt = f"Given: D:\\{body}.py for reference."
    candidates = dispatch_gate.extract_given_candidates(prompt)
    assert [c[0] for c in candidates] == [f"D:\\{body}.py"]


def test_extract_given_candidates_pathological_input_under_5s():
    # Critic's measured form: "C:/"*20000 + "a"*20000 (the old regexes were quadratic on it).
    # FLIPPED: the token reader is linear and yields the one giant token as a candidate.
    pathological = "C:/" * 20000 + "a" * 20000
    start = time.monotonic()
    candidates = dispatch_gate.extract_given_candidates(pathological)
    elapsed = time.monotonic() - start
    assert elapsed < 5.0, f"took {elapsed:.2f}s -- quadratic regression?"
    assert len(candidates) == 1


def test_extract_given_candidates_1000_real_paths_previous_behavior():
    names = [f"tools/fake{i}.py" for i in range(1000)]
    prompt = "Given: " + ", ".join(names) + ". Read them all."
    start = time.monotonic()
    candidates = dispatch_gate.extract_given_candidates(prompt, _TOP)
    elapsed = time.monotonic() - start
    assert elapsed < 5.0, f"took {elapsed:.2f}s"
    toks = [c[0] for c in candidates]
    assert toks == names


def test_given_path_warn_non_task_agent_tool_returns_empty():
    assert dispatch_gate.given_path_warn({"tool_name": "Bash", "tool_input": {}}) == ""


def test_given_path_warn_empty_or_non_string_prompt_returns_empty():
    payload_missing_prompt = {"tool_name": "Task", "tool_input": {"subagent_type": "builder"}}
    assert dispatch_gate.given_path_warn(payload_missing_prompt) == ""

    payload_empty_prompt = {"tool_name": "Task", "tool_input": {"prompt": ""}}
    assert dispatch_gate.given_path_warn(payload_empty_prompt) == ""

    payload_non_string_prompt = {"tool_name": "Task", "tool_input": {"prompt": 12345}}
    assert dispatch_gate.given_path_warn(payload_non_string_prompt) == ""


def test_given_path_warn_non_dict_tool_input_returns_empty():
    payload = {"tool_name": "Task", "tool_input": "not a dict"}
    assert dispatch_gate.given_path_warn(payload) == ""


def test_given_path_warn_missing_cwd_is_silent_no_getcwd_fallback(monkeypatch, tmp_path):
    # FLIPPED (6.6, M7/M14): no payload["cwd"] -> the layer is silent; os.getcwd() is never the root
    monkeypatch.chdir(tmp_path)
    (tmp_path / "tools").mkdir()
    payload = {
        "tool_name": "Task",
        "tool_input": {"prompt": "Given: tools/does_not_exist_at_all.py for reference."},
    }
    assert dispatch_gate.given_path_warn(payload) == ""
    payload["cwd"] = str(tmp_path)
    assert "tools/does_not_exist_at_all.py" in dispatch_gate.given_path_warn(payload)


def test_given_path_warn_returns_empty_when_all_candidates_exist(tmp_path):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "x.py").write_text("# real")
    payload = {
        "tool_name": "Task",
        "tool_input": {"prompt": "Given: tools/x.py for reference."},
        "cwd": str(tmp_path),
    }
    assert dispatch_gate.given_path_warn(payload) == ""


# --- main()-level wiring: blocking verdict suppresses the WARN layer ---


def test_echo_json_blocking_verdict_suppresses_given_path_warn():
    """When decide() already blocks (missing DoD), the given-path WARN
    layer must not run at all -- no additionalContext on stdout, just
    the blocking stderr message and exit 2."""
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "builder",
            "prompt": "Given: tools/does_not_exist_anywhere.py. Just fix a typo.",
            "description": "sonnet: fix",
        },
    }
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 2
    # old: "no DoD"; new: the completeness refusal, DoD among the missing
    assert "DISPATCH INCOMPLETE" in result.stderr
    assert "DoD (no line)" in result.stderr
    assert result.stdout == ""


def test_echo_json_passing_dispatch_emits_given_path_warn_additional_context(tmp_path):
    """A dispatch that PASSES decide() but names a missing given-path
    gets the additionalContext JSON on stdout, exit 0."""
    (tmp_path / "tools").mkdir()  # a top-level entry: makes `tools/...` a path candidate under this root
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "critic",
            "prompt": "Review Given: tools/does_not_exist_anywhere_xyz.py for reference.\n\n" + _CRITIC_HANDOFF,
            "description": "opus: review",
        },
        "cwd": str(tmp_path),  # FLIPPED: the root is the payload cwd now (t-796: a tmp root, the gate writes traces under it)
    }
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert result.stderr == ""
    parsed = json.loads(result.stdout)
    warn_text = parsed["hookSpecificOutput"]["additionalContext"]
    assert "GIVEN-PATH WARN" in warn_text
    assert "tools/does_not_exist_anywhere_xyz.py" in warn_text


def test_echo_json_no_missing_given_paths_emits_no_stdout():
    """A dispatch mentioning only paths that genuinely exist (e.g. this
    very test file) emits no additionalContext at all."""
    payload = {
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "critic",
            "prompt": "Review tools/dispatch_gate.py for reference.\n\n" + _CRITIC_HANDOFF,
            "description": "opus: review",
        },
    }
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert result.stdout == ""


# =======================================================================
# Write-indicator discriminator: is_path_like_token /
# owns_declaration_has_path_token, and the removal of the bare
# "\bowns\b" alternative from WRITE_INDICATORS_RE.
# =======================================================================


def test_is_path_like_token_direct():
    assert dispatch_gate.is_path_like_token("D:/repo/tools/a.py") is True
    assert dispatch_gate.is_path_like_token("D:\\repo\\tools\\a.py") is True
    assert dispatch_gate.is_path_like_token("/repo/tools/a.py") is True
    assert dispatch_gate.is_path_like_token("tools/*.py") is True
    # A bare "*" with no slash (markdown bold decoration) is NOT a path.
    assert dispatch_gate.is_path_like_token("**Attention**:") is False
    assert dispatch_gate.is_path_like_token("the other side.**") is False
    # A relative path with no drive/slash prefix is not a path either
    # (rule 11's manifest requires ABSOLUTE write paths).
    assert dispatch_gate.is_path_like_token("tools/x.py") is False
    assert dispatch_gate.is_path_like_token("") is False
    assert dispatch_gate.is_path_like_token(None) is False


def test_owns_declaration_has_path_token_canonical_forms():
    assert dispatch_gate.owns_declaration_has_path_token(
        "owns (ABSOLUTE write paths): D:/repo/tools/x.py"
    ) is True
    assert dispatch_gate.owns_declaration_has_path_token(
        "**owns (ABSOLUTE write paths):**\n- D:/a.py\n- D:/b.py\n"
    ) is True
    # A bare owns: with a relative, non-path-like token is NOT a hit.
    assert dispatch_gate.owns_declaration_has_path_token("owns: tools/x.py.") is False
    assert dispatch_gate.owns_declaration_has_path_token("owns:") is False
    assert dispatch_gate.owns_declaration_has_path_token("") is False
    assert dispatch_gate.owns_declaration_has_path_token(None) is False


def test_owns_bare_word_no_longer_a_write_indicator():
    """The bare word "owns" appearing anywhere in the prompt (a topic
    mention, not a real declaration) must no longer, by itself, mark a
    builder dispatch as writing -- WRITE_INDICATORS_RE no longer
    carries "\\bowns\\b"."""
    assert not dispatch_gate.WRITE_INDICATORS_RE.search("let's discuss how owns works")
    # old: a BUILDER prompt discussing "owns" with a DoD word -> 0 (no write signal);
    # new: a builder is always checked, so the premise ("the bare word does not make
    # a dispatch a writing one") is pinned on a non-builder type: not checked -> 0
    prompt = "DoD: witness present. This dispatch discusses how owns works, read-only.\n\n" + _CRITIC_HANDOFF
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": "critic", "prompt": prompt, "description": "opus: x"},
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 0, message


def test_owns_declaration_with_absolute_path_still_requires_manifest():
    """An owns: declaration carrying a real absolute path token still
    marks a dispatch as writing -- a builder dispatch with such an owns
    line but no given still blocks. (old: "context manifest"; new: the
    completeness refusal names given.)"""
    prompt = "DoD: witness present. owns (ABSOLUTE write paths): D:/repo/tools/x.py."
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: x"))
    assert exit_code == 2
    assert "DISPATCH INCOMPLETE" in message
    assert "given (no line)" in message


def test_owns_declaration_with_absolute_path_and_given_passes():
    # old: an inline "Given: ... owns (ABSOLUTE write paths): D:/repo/tools/x.py." -> 0;
    # new: the full form, the owns header keeps its parenthetical
    prompt = _manifest(owns="D:/repo/tools/x.py").replace(
        "owns: ", "owns (ABSOLUTE write paths): ", 1
    )
    exit_code, message = dispatch_gate.decide(_builder_payload(prompt, description="sonnet: x"))
    assert exit_code == 0, message


# =======================================================================
# Role-type WARN layer: declared label tier vs. the model actually
# bound by the .claude/agents/*.md role file for subagent_type.
# =======================================================================


def _agent_payload(subagent_type=None, description=None, prompt="noop", cwd=None):
    tool_input = {"prompt": prompt}
    if subagent_type is not None:
        tool_input["subagent_type"] = subagent_type
    if description is not None:
        tool_input["description"] = description
    payload = {"tool_name": "Task", "tool_input": tool_input}
    if cwd is not None:
        payload["cwd"] = cwd
    return payload


def _scout_families():
    """(live_family, foreign_family) for scout.md's own binding.

    Route port, node D1 (DoD item 6): these tests derive their
    match/mismatch labels from the LIVE role file through the SAME
    resolver the gate itself uses, instead of pinning a model name --
    "model name as the test's own criterion" is a known failure class:
    the earlier hardcoded assumption "scout.md declares model: haiku"
    broke the moment scout.md was rebound to sonnet, with the gate
    itself fully intact (measured baseline before this edit: 6 of
    these tests failed on a clean run, not because the layer regressed
    but because the pin did). The tests' subject is the LOGIC
    (mismatch -> WARN, match -> silence), not a particular binding."""
    known, model = dispatch_gate._find_agent_role_model("scout")
    assert known and model, "scout.md must exist and carry model: (otherwise these tests are moot)"
    fam = dispatch_gate._model_family(model)
    assert fam, f"model {model!r} of scout.md's role file does not resolve to a known family"
    return fam, ("haiku" if fam != "haiku" else "sonnet")


def test_role_type_warn_known_role_family_mismatch_warns():
    # The label declares a family DELIBERATELY FOREIGN to scout.md's
    # live binding (binding-agnostic, see _scout_families).
    live, foreign = _scout_families()
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description=f"{foreign}: does recon")
    )
    assert "ROLE-TYPE WARN" in warn
    assert foreign in warn
    assert "scout" in warn
    assert live in warn


def test_role_type_warn_known_role_family_match_silent():
    # Positive control (symmetric with the mismatch above): the same
    # type, label matching the role file's LIVE model -> "".
    live, _foreign = _scout_families()
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description=f"{live}: does recon")
    )
    assert warn == ""


def test_role_type_warn_builder_opus_label_mismatch_warns():
    # builder.md declares model: sonnet; the label declares "opus:".
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="builder", description="opus: fix the file")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "opus" in warn
    assert "builder" in warn
    assert "sonnet" in warn


def test_role_type_warn_unknown_role_general_purpose_warns():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="general-purpose", description="opus: review the diff")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "general-purpose" in warn
    assert "no role file" in warn


def test_role_type_warn_unknown_role_arbitrary_string_warns():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="totally-unknown-role", description="fable: something")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "totally-unknown-role" in warn
    assert "no role file" in warn


def test_known_label_silent_general_purpose_same_label_warns():
    # A pin/positive-control pair in one test: a real role file with a
    # matching label is silent, the SAME label on an unresolvable type
    # warns -- proving the silence above isn't a broken layer.
    warn_critic = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="critic", description="opus: review the diff")
    )
    assert warn_critic == ""

    warn_unknown = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="general-purpose", description="opus: review the diff")
    )
    assert "ROLE-TYPE WARN" in warn_unknown
    assert "no role file" in warn_unknown


def test_subagent_type_case_and_whitespace_variants_silent():
    for variant in ("Builder", "BUILDER", "builder ", " Builder", "BuIlDeR"):
        warn = dispatch_gate.role_type_warn(
            _agent_payload(subagent_type=variant, description="sonnet: fix the file")
        )
        assert warn == "", f"variant {variant!r} should be silent, got {warn!r}"


def test_subagent_type_case_mismatch_still_warns_on_real_mismatch():
    # Regression guard paired with the test above: case does NOT mask
    # a real family mismatch -- "Scout" (different case) with a label
    # of a family foreign to the live binding still warns
    # (binding-agnostic, see _scout_families).
    _live, foreign = _scout_families()
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="Scout", description=f"{foreign}: does recon")
    )
    assert "ROLE-TYPE WARN" in warn


# --- Quote-stripping around name:/model: frontmatter values -----------


def test_strip_quotes_double_quotes():
    assert dispatch_gate._strip_quotes('"scout"') == "scout"


def test_strip_quotes_single_quotes():
    assert dispatch_gate._strip_quotes("'sonnet'") == "sonnet"


def test_strip_quotes_unquoted_unchanged():
    assert dispatch_gate._strip_quotes("scout") == "scout"


def test_strip_quotes_mismatched_quotes_unchanged():
    assert dispatch_gate._strip_quotes("'scout\"") == "'scout\""


def test_strip_quotes_quote_inside_value_not_stripped():
    assert dispatch_gate._strip_quotes('sco"ut') == 'sco"ut'
    assert dispatch_gate._strip_quotes('scout"') == 'scout"'
    assert dispatch_gate._strip_quotes('"scout') == '"scout'


def test_strip_quotes_too_short_unchanged():
    assert dispatch_gate._strip_quotes('"') == '"'
    assert dispatch_gate._strip_quotes("") == ""


def test_quoted_name_field_now_matches_and_reveals_real_mismatch(tmp_path, monkeypatch):
    (tmp_path / "randomname.md").write_text(
        '---\nname: "scout"\nmodel: "haiku"\n---\n\n# scout (quoted)\n', encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="sonnet: does recon")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "no role file" not in warn
    assert "haiku" in warn


def test_quoted_model_single_quotes_family_still_resolved(tmp_path, monkeypatch):
    (tmp_path / "custom.md").write_text(
        "---\nname: custom\nmodel: 'opus'\n---\n\n# custom\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn_match = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="custom", description="opus: review")
    )
    assert warn_match == ""
    warn_mismatch = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="custom", description="sonnet: review")
    )
    assert "ROLE-TYPE WARN" in warn_mismatch
    assert "opus" in warn_mismatch


# --- Filename match takes priority over a name: field conflict --------


def test_filename_match_takes_priority_over_name_field_conflict(tmp_path, monkeypatch):
    (tmp_path / "scout.md").write_text(
        "---\nname: not-scout\nmodel: sonnet\n---\n\n# scout by filename\n", encoding="utf-8"
    )
    (tmp_path / "other.md").write_text(
        "---\nname: scout\nmodel: haiku\n---\n\n# scout by name field\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="sonnet: does recon")
    )
    assert warn == ""

    warn_control = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="haiku: does recon")
    )
    assert "ROLE-TYPE WARN" in warn_control
    assert "sonnet" in warn_control


def test_builtin_harness_type_without_role_file_warns_legitimately():
    for builtin_type in ("Explore", "statusline-setup"):
        warn = dispatch_gate.role_type_warn(
            _agent_payload(subagent_type=builtin_type, description="sonnet: do something")
        )
        assert "ROLE-TYPE WARN" in warn
        assert "no role file" in warn


def test_role_type_warn_documented_limitation_critic_designer_opus_indistinguishable():
    # This kit's critic.md and designer.md both declare model: opus --
    # the layer compares FAMILY, not function, so this pair is
    # indistinguishable by design (documented limitation).
    warn_critic = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="critic", description="opus: review the diff")
    )
    warn_designer = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="designer", description="opus: draft a spec")
    )
    assert warn_critic == ""
    assert warn_designer == ""


# --- Table of empty/absent inputs (verbatim from the port's edge table) -


def test_role_type_warn_non_task_agent_tool_silent():
    warn = dispatch_gate.role_type_warn({"tool_name": "Bash", "tool_input": {}})
    assert warn == ""


def test_role_type_warn_claude_prefix_label_silent():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="claude: does recon")
    )
    assert warn == ""


def test_role_type_warn_missing_description_silent():
    warn = dispatch_gate.role_type_warn(_agent_payload(subagent_type="scout"))
    assert warn == ""


def test_role_type_warn_empty_description_silent():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="")
    )
    assert warn == ""


def test_role_type_warn_description_not_string_silent():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": "scout", "prompt": "x", "description": 12345},
    }
    warn = dispatch_gate.role_type_warn(payload)
    assert warn == ""


def test_role_type_warn_description_without_model_prefix_silent():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="fix it now")
    )
    assert warn == ""


def test_role_type_warn_subagent_type_missing_silent():
    warn = dispatch_gate.role_type_warn(_agent_payload(description="opus: x"))
    assert warn == ""


def test_role_type_warn_subagent_type_none_silent():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": None, "prompt": "x", "description": "opus: x"},
    }
    warn = dispatch_gate.role_type_warn(payload)
    assert warn == ""


def test_role_type_warn_subagent_type_empty_string_silent():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="", description="opus: x")
    )
    assert warn == ""


def test_role_type_warn_subagent_type_whitespace_only_silent():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="   ", description="opus: x")
    )
    assert warn == ""


def test_role_type_warn_subagent_type_number_silent():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": 42, "prompt": "x", "description": "opus: x"},
    }
    warn = dispatch_gate.role_type_warn(payload)
    assert warn == ""


def test_role_type_warn_subagent_type_dict_silent():
    payload = {
        "tool_name": "Task",
        "tool_input": {"subagent_type": {"a": 1}, "prompt": "x", "description": "opus: x"},
    }
    warn = dispatch_gate.role_type_warn(payload)
    assert warn == ""


def test_role_type_warn_payload_not_dict_silent():
    assert dispatch_gate.role_type_warn(None) == ""
    assert dispatch_gate.role_type_warn("not a dict") == ""
    assert dispatch_gate.role_type_warn([1, 2, 3]) == ""


def test_role_type_warn_tool_name_missing_silent():
    warn = dispatch_gate.role_type_warn({"tool_input": {"subagent_type": "scout"}})
    assert warn == ""


def test_role_type_warn_tool_input_not_dict_silent():
    warn = dispatch_gate.role_type_warn({"tool_name": "Task", "tool_input": "nope"})
    assert warn == ""


def test_role_type_warn_tool_input_missing_silent():
    warn = dispatch_gate.role_type_warn({"tool_name": "Task"})
    assert warn == ""


def test_role_type_warn_huge_description_does_not_hang():
    _live, foreign = _scout_families()
    huge_description = f"{foreign}: " + ("x" * 100_000)
    huge_prompt = "y" * 240_000
    start = time.monotonic()
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description=huge_description, prompt=huge_prompt)
    )
    elapsed = time.monotonic() - start
    assert elapsed < 5.0, f"took {elapsed:.2f}s"
    assert "ROLE-TYPE WARN" in warn  # foreign family != scout's live binding -- a real mismatch


def test_role_type_warn_known_role_without_model_in_frontmatter_silent(tmp_path, monkeypatch):
    (tmp_path / "custom.md").write_text(
        "---\nname: custom\ntools: Read\n---\n\n# custom\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="custom", description="opus: does something")
    )
    assert warn == ""


def test_role_type_warn_known_role_model_family_unrecognized_silent(tmp_path, monkeypatch):
    (tmp_path / "custom.md").write_text(
        "---\nname: custom\nmodel: llama-3.3-70b-versatile\n---\n\n# custom\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="custom", description="opus: does something")
    )
    assert warn == ""


def test_role_type_warn_matches_by_frontmatter_name_field_not_filename(tmp_path, monkeypatch):
    (tmp_path / "xyz.md").write_text(
        "---\nname: mytype\nmodel: opus\n---\n\n# mytype\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="mytype", description="sonnet: does something")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "opus" in warn


def test_role_type_warn_malformed_frontmatter_no_closing_fence_silent(tmp_path, monkeypatch):
    (tmp_path / "broken.md").write_text(
        "---\nname: broken\nmodel: opus\nno closing fence.\n", encoding="utf-8"
    )
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="broken", description="sonnet: does something")
    )
    assert warn == ""


def test_role_type_warn_agents_dir_missing_entirely_silent(tmp_path, monkeypatch):
    missing_dir = tmp_path / "does_not_exist"
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", missing_dir)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="general-purpose", description="opus: x")
    )
    assert warn == ""


def test_role_type_warn_agents_dir_exists_but_empty_warns_unknown(tmp_path, monkeypatch):
    monkeypatch.setattr(dispatch_gate, "AGENTS_DIR", tmp_path)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="builder", description="opus: x")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "no role file" in warn


def test_role_type_warn_unexpected_exception_inside_layer_fails_open(monkeypatch):
    def _boom(subagent_type_norm):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_gate, "_find_agent_role_model", _boom)
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="scout", description="sonnet: does recon")
    )
    assert warn == ""


def test_role_type_warn_agents_dir_present_positive_control():
    assert dispatch_gate.AGENTS_DIR.is_dir()


# =======================================================================
# ROLE_TYPE_WARN split -- PROJECT vs. BUILTIN_TYPE (route port, node D1;
# staff twin's split-warn fix): the branching LOGIC (what counts as an unknown
# role) is unchanged, only the TEXT differs by whether subagent_type is
# a known harness built-in (no role file expected) or a project role
# (a role file is expected but missing).
# =======================================================================


def test_role_type_warn_both_texts_share_byte_identical_prefix():
    prefix = "ROLE-TYPE WARN:"
    assert dispatch_gate.ROLE_TYPE_WARN_PROJECT.startswith(prefix)
    assert dispatch_gate.ROLE_TYPE_WARN_BUILTIN_TYPE.startswith(prefix)


def test_role_type_warn_both_texts_carry_no_role_file_substring():
    assert "no role file" in dispatch_gate.ROLE_TYPE_WARN_PROJECT
    assert "no role file" in dispatch_gate.ROLE_TYPE_WARN_BUILTIN_TYPE


def test_role_type_warn_builtin_type_uses_builtin_text():
    for builtin_type in ("general-purpose", "claude-code-guide", "Explore", "Plan", "statusline-setup"):
        warn = dispatch_gate.role_type_warn(
            _agent_payload(subagent_type=builtin_type, description="sonnet: do something")
        )
        assert "ROLE-TYPE WARN" in warn, builtin_type
        assert "no role file" in warn, builtin_type
        assert "expected" in warn, builtin_type  # BUILTIN_TYPE-specific phrase


def test_role_type_warn_unknown_type_not_in_list_uses_project_text():
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="totally-unknown-role-xyz", description="fable: something")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "no role file" in warn
    assert "add a role file" in warn
    assert "not yet in the known list" in warn  # a miss falls through, not a silent pass


def test_role_type_warn_builtin_match_is_case_insensitive():
    for variant in ("GENERAL-PURPOSE", "General-Purpose", " general-purpose "):
        warn = dispatch_gate.role_type_warn(
            _agent_payload(subagent_type=variant, description="sonnet: x")
        )
        assert "expected" in warn, f"variant={variant!r}"


def test_role_type_warn_mismatch_case_unaffected_by_split():
    # Regression guard: the MISMATCH branch (a role file IS found, the
    # family diverges) is untouched by the split -- verbatim old text,
    # no "no role file" substring.
    warn = dispatch_gate.role_type_warn(
        _agent_payload(subagent_type="builder", description="opus: fix the file")
    )
    assert "ROLE-TYPE WARN" in warn
    assert "opus" in warn
    assert "builder" in warn
    assert "sonnet" in warn
    assert "no role file" not in warn


# --- ROOT-ONLY GUARD on is_path_like_token (route port, node D1; staff
# twin ~:863-884): a bare root with no segment ("/", "C:\\") is NOT a
# path token; a root WITH a segment ("/etc", "C:\\x") IS -- both edges
# tested (rule 6a).
# =======================================================================


def test_is_path_like_token_bare_root_alone_is_not_a_token():
    for tok in ["/", "//", "///", "C:\\", "C:/", "\\", "", "   ", "."]:
        assert dispatch_gate.is_path_like_token(tok) is False, tok


def test_is_path_like_token_root_with_segment_is_a_token():
    for tok in ["/etc", "/etc/x", "C:\\x", "C:/x", "C:\\AI CRM\\x\\AGENTS.md", "//server/share"]:
        assert dispatch_gate.is_path_like_token(tok) is True, tok


def test_is_path_like_token_doubled_bare_root_still_not_a_token():
    # The class is "root without ANY segment", not "exactly one slash"
    # -- a doubled/tripled root with no segment stays False.
    for tok in ["//", "///", "C://"]:
        assert dispatch_gate.is_path_like_token(tok) is False, tok


# --- Invariants at the main()/subprocess level: WARN never replaces a
# block, exit-2 branches stay unreachable to the new code, stdout stays
# a single JSON object. ------------------------------------------------


def test_role_type_warn_not_computed_when_gate_blocks_check1():
    payload = _builder_payload("Just fix a typo.", description="opus: fix")
    payload["tool_input"]["subagent_type"] = "builder"
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 2
    # old: "no DoD"; new: the completeness refusal, DoD among the missing
    assert "DoD (no line)" in result.stderr.decode("utf-8", errors="replace")
    assert result.stdout == b""


def test_role_type_warn_never_sets_exit_2_or_permission_decision():
    # A mismatch (binding-agnostic, see _scout_families) guarantees the
    # WARN actually fires, so the subprocess-level invariants below
    # have something to check.
    _live, foreign = _scout_families()
    payload = _agent_payload(subagent_type="scout", description=f"{foreign}: does recon")
    payload["tool_input"]["prompt"] = "DoD: the test is green."
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    out = json.loads(result.stdout.decode("utf-8"))
    assert "permissionDecision" not in json.dumps(out)
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "ROLE-TYPE WARN" in ctx


def test_both_warn_layers_fire_single_json_object_given_path_first(tmp_path):
    # Same reasoning as above: a foreign-family label guarantees the
    # role-type WARN actually fires alongside the given-path one
    # (binding-agnostic, see _scout_families).
    _live, foreign = _scout_families()
    (tmp_path / "tools").mkdir()  # t-796: a tmp root (the gate writes its verdict under the payload cwd), with a `tools` entry
    repo_root = str(tmp_path)
    payload = _agent_payload(
        subagent_type="scout",
        description=f"{foreign}: recon",
        prompt="Given: tools/fake_does_not_exist.py. Find mentions.",
        cwd=repo_root,
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    stdout_lines = [ln for ln in result.stdout.decode("utf-8").splitlines() if ln.strip()]
    assert len(stdout_lines) == 1, "stdout must carry exactly one JSON object"
    out = json.loads(stdout_lines[0])
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "GIVEN-PATH WARN" in ctx
    assert "ROLE-TYPE WARN" in ctx
    assert ctx.index("GIVEN-PATH WARN") < ctx.index("ROLE-TYPE WARN")


def test_role_type_warn_silent_on_existing_dispatch_gate_own_test_suite_labels():
    warn = dispatch_gate.role_type_warn(
        _builder_payload("Fix it. DoD: test is green.", description="sonnet: fix")
    )
    assert warn == ""


def test_given_path_warn_layer_exception_is_swallowed_exit_0(monkeypatch):
    """Any exception raised inside the WARN layer must be swallowed by
    main()'s belt-and-suspenders try/except -- the blocking hook must
    never crash over a WARN-layer failure."""
    import dispatch_gate as dg

    def boom(*args):
        raise RuntimeError("boom")

    monkeypatch.setattr(dg, "given_path_warn", boom)
    payload = {"tool_name": "Task", "tool_input": {"prompt": "Given: tools/x.py."}}
    exit_code, message = dg.decide(payload)
    assert exit_code == 0
    # Simulate main()'s own try/except around the (now monkeypatched) call.
    try:
        warn = dg.given_path_warn(payload)
    except Exception:
        warn = ""
    assert warn == ""


# =======================================================================
# B-201 wiring (piece B): decide() calls dispatch_manifest.check in place of
# the old checks 1-2; main() adds the check's note to additionalContext and
# turns an unreadable payload / an exception in the check into exit 0 + the
# UNCHECKED NOTE (additionalContext and stderr). New tests -- no old test
# pinned any of this.
# =======================================================================

import dispatch_manifest  # noqa: E402

_SKIP_LINE = (
    "manifest-skip: given, owns, non-goals, handoff, edges, dod, siblings -- a throwaway probe, "
    "nothing is written"
)


def _hook_out(result):
    """(returncode, stdout-json-or-None, stderr) of a subprocess hook run."""
    out = json.loads(result.stdout) if result.stdout.strip() else None
    return result.returncode, out, result.stderr


def _context(out):
    return out["hookSpecificOutput"]["additionalContext"]


def test_decide_unchecked_when_check_raises_label_check_still_runs(monkeypatch):
    def boom(*args):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_manifest, "check_cut", boom)  # FLIPPED (B-204): decide builds the cut and calls check_cut
    # an incomplete builder dispatch is NOT refused when the check raised ...
    exit_code, message = dispatch_gate.decide(_builder_payload("Just a fix.", description="sonnet: fix"))
    assert (exit_code, message) == (0, "")
    # ... and the label check (last) still runs
    exit_code, message = dispatch_gate.decide(_builder_payload("Just a fix.", description="fixitnow"))
    assert exit_code == 2
    assert "worker's tier" in message


def test_decide_unchecked_when_manifest_import_fails(monkeypatch):
    def no_module():
        raise ImportError("dispatch_manifest is gone")

    monkeypatch.setattr(dispatch_gate, "_load_manifest_module", no_module)
    exit_code, message = dispatch_gate.decide(_builder_payload("Just a fix.", description="sonnet: fix"))
    assert (exit_code, message) == (0, "")


def test_decide_never_raises_on_odd_payloads():
    for payload in (
        None,
        [],
        "text",
        {"tool_name": "Task", "tool_input": "a string"},
        {"tool_name": "Task", "tool_input": ["a", "list"]},
        {"tool_name": "Agent"},
        {"tool_name": "Agent", "tool_input": None},
        {"tool_name": "Agent", "tool_input": {}},
        {"tool_name": "Agent", "tool_input": {"subagent_type": "builder", "prompt": None}},
    ):
        result = dispatch_gate.decide(payload)
        assert isinstance(result, tuple) and len(result) == 2, payload


def test_decide_empty_builder_prompt_is_refused_with_all_six_items():
    for prompt in (None, "", 42):
        payload = {"tool_name": "Agent", "tool_input": {"subagent_type": "builder", "prompt": prompt}}
        exit_code, message = dispatch_gate.decide(payload)
        assert exit_code == 2, prompt
        for item in ("given", "owns", "non-goals", "handoff", "edges", "DoD"):
            assert f"{item} (no line)" in message


def test_decide_builder_type_case_and_whitespace_is_checked():
    payload = {"tool_name": "Agent", "tool_input": {"subagent_type": "Builder ", "prompt": "Just a fix."}}
    exit_code, _ = dispatch_gate.decide(payload)
    assert exit_code == 2


def test_decide_non_builder_without_absolute_owns_is_not_checked():
    payload = {
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "general-purpose", "prompt": "Just look around.", "description": "sonnet: x"},
    }
    assert dispatch_gate.decide(payload) == (0, "")


def test_decide_writing_non_builder_is_checked():
    # a non-builder type with an owns section holding an absolute path is a writing dispatch
    payload = {
        "tool_name": "Agent",
        "tool_input": {
            "subagent_type": "general-purpose",
            "prompt": "owns: C:/proj/tools/x.py\nDo it.",
            "description": "sonnet: x",
        },
    }
    exit_code, message = dispatch_gate.decide(payload)
    assert exit_code == 2
    assert "this writing dispatch does not go out" in message


def test_main_full_manifest_builder_exit_0_silent():
    result = _run_hook(_builder_payload(_manifest(prefix="Fix it."), description="sonnet: fix"))
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    # FLIPPED (B-245): no cwd -> the pass carries the P11 note instead of silence
    assert _context(json.loads(result.stdout)) == "PATH CHECK: paths unchecked: no cwd"


def test_main_skip_note_joins_additional_context_exit_0():
    prompt = "Just a probe.\n" + _SKIP_LINE
    result = _run_hook(_builder_payload(prompt, description="sonnet: probe"))
    code, out, err = _hook_out(result)
    assert code == 0, err
    assert out is not None
    assert _context(out).startswith("MANIFEST-SKIP: dispatch sent without ")
    assert "a throwaway probe" in _context(out)
    assert err == ""  # a returned note goes to additionalContext only


def test_main_incomplete_builder_exit_2_message_on_stderr_no_stdout():
    result = _run_hook(_builder_payload("Just a fix.", description="sonnet: fix"))
    assert result.returncode == 2
    assert result.stderr.startswith("DISPATCH INCOMPLETE (CLAUDE.md rule 11)")
    assert result.stdout == ""


def test_main_completeness_refusal_wins_over_label_problem():
    result = _run_hook(_builder_payload("Just a fix.", description="fixitnow"))
    assert result.returncode == 2
    assert "DISPATCH INCOMPLETE" in result.stderr
    assert "worker's tier" not in result.stderr


def test_main_degraded_quote_read_exit_0_unchecked_note():
    # more than 200 inline spans on one line: md_regions reports a degraded read
    prompt = "owns: C:/proj/tools/x.py\n" + ("`a` " * 201)
    result = _run_hook(_builder_payload(prompt, description="sonnet: fix"))
    code, out, err = _hook_out(result)
    assert code == 0, err
    assert out is not None
    assert _context(out).startswith("MANIFEST-UNCHECKED: this dispatch was not checked")
    assert "quoted regions could not be read reliably" in _context(out)


def test_main_unreadable_agent_payloads_exit_0_with_unchecked_note_on_both_channels():
    for raw, detail in (
        ("[1, 2, 3]", "payload is not a JSON object (list)"),
        ('{"tool_name": "Agent", "tool_input": "a string"}', "tool_input is not a JSON object (str)"),
        ('{"tool_name": "Task"}', "tool_input is not a JSON object (NoneType)"),
    ):
        result = _run_hook(raw)
        code, out, err = _hook_out(result)
        assert code == 0, (raw, err)
        assert out is not None, raw
        expected = f"payload unreadable: {detail}"
        assert expected in _context(out), raw
        assert _context(out).startswith("MANIFEST-UNCHECKED:"), raw
        assert expected in err, raw  # the same text on stderr


def test_main_malformed_json_carries_the_unchecked_note_on_both_channels():
    # Lead's decision (t-106): malformed JSON is visible, unlike empty stdin
    for raw in ("{not valid json", "null-ish", '{"tool_name": "Agent", '):
        result = _run_hook(raw)
        code, out, err = _hook_out(result)
        assert code == 0, raw
        assert out is not None, raw
        assert _context(out).startswith("MANIFEST-UNCHECKED:"), raw
        assert "payload unreadable: malformed JSON (JSONDecodeError)" in _context(out), raw
        assert "payload unreadable: malformed JSON (JSONDecodeError)" in err, raw


def test_main_stdin_timeout_carries_the_unchecked_note_on_both_channels(monkeypatch, capsys):
    monkeypatch.setattr(dispatch_gate, "_read_stdin_bytes_deadline", lambda: (b"", True))
    # main() records the deadline hit in module state for the script-exit path: restore it
    monkeypatch.setitem(dispatch_gate._STDIN_DEADLINE_STATE, "hit", False)
    code = dispatch_gate.main()
    captured = capsys.readouterr()
    assert code == 0
    assert "stdin deadline exceeded" in captured.err  # the old line stays
    assert "payload unreadable: stdin deadline exceeded" in captured.err
    out = json.loads(captured.out)
    assert _context(out).startswith("MANIFEST-UNCHECKED:")
    assert "payload unreadable: stdin deadline exceeded" in _context(out)


def test_decide_can_still_raise_on_a_non_string_description():
    # as it truly behaves (TypeError in the label regex, as before B-201): decide() is NOT
    # a never-raises function; its callers guard it (main(), owns_gate, critic_snapshot)
    payload = {
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "critic", "prompt": "x\n" + _CRITIC_HANDOFF, "description": 5},
    }
    import pytest

    with pytest.raises(TypeError):
        dispatch_gate.decide(payload)


def test_main_exception_out_of_decide_exit_0_unchecked_note_on_both_channels():
    # the repro of the review: exit 1 with a traceback before this guard
    payload = {
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "critic", "prompt": "x\n" + _CRITIC_HANDOFF, "description": 5},
    }
    result = _run_hook(payload)
    code, out, err = _hook_out(result)
    assert code == 0, err
    assert "Traceback" not in err
    assert out is not None
    assert _context(out).startswith("MANIFEST-UNCHECKED:")
    assert "check failed: TypeError" in _context(out)
    assert "check failed: TypeError" in err


def test_main_a_real_refusal_is_still_exit_2_not_swallowed():
    # only exceptions are caught: an incomplete builder dispatch with a fine label stays exit 2
    result = _run_hook(_builder_payload("Just a fix.", description="sonnet: fix"))
    assert result.returncode == 2
    assert "MANIFEST-UNCHECKED" not in result.stderr


def test_main_keeps_old_silence_on_empty_stdin_and_on_a_non_agent_call():
    # empty / whitespace-only stdin (and a TTY, which reads as empty): silent exit 0,
    # as before -- test_p4_stdin_deadline.py pins the empty stdout
    for raw in ("", "   ", "\n"):
        result = _run_hook(raw)
        assert result.returncode == 0, raw
        assert result.stdout == "", raw
        assert result.stderr == "", raw
    # a non-Agent call is not checked, even with an odd tool_input: silent exit 0
    for payload in (
        {"tool_name": "Bash", "tool_input": "a string"},
        {"tool_name": "Bash"},
        {"tool_name": "Read", "tool_input": None},
    ):
        result = _run_hook(payload)
        assert result.returncode == 0, payload
        assert result.stdout == "", payload
        assert result.stderr == "", payload


def test_main_exception_in_check_exit_0_unchecked_note_on_both_channels(monkeypatch, capsys):
    def boom(*args):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_manifest, "check_cut", boom)  # FLIPPED (B-204): decide builds the cut and calls check_cut
    raw = json.dumps(_builder_payload("Just a fix.", description="sonnet: fix")).encode("utf-8")
    monkeypatch.setattr(dispatch_gate, "_read_stdin_bytes_deadline", lambda: (raw, False))
    code = dispatch_gate.main()
    captured = capsys.readouterr()
    assert code == 0
    out = json.loads(captured.out)
    assert _context(out).startswith("MANIFEST-UNCHECKED:")
    assert "check failed: RuntimeError" in _context(out)
    assert "check failed: RuntimeError" in captured.err


def test_main_failed_manifest_import_still_produces_the_unchecked_note(monkeypatch, capsys):
    def no_module():
        raise ModuleNotFoundError("dispatch_manifest is gone")

    monkeypatch.setattr(dispatch_gate, "_load_manifest_module", no_module)
    raw = json.dumps(_builder_payload("Just a fix.", description="sonnet: fix")).encode("utf-8")
    monkeypatch.setattr(dispatch_gate, "_read_stdin_bytes_deadline", lambda: (raw, False))
    code = dispatch_gate.main()
    captured = capsys.readouterr()
    assert code == 0
    assert "check failed: ModuleNotFoundError" in _context(json.loads(captured.out))


def test_unchecked_note_fallback_template_equals_the_modules():
    # the copy in dispatch_gate is used only when dispatch_manifest cannot be imported
    assert dispatch_gate._UNCHECKED_NOTE_FALLBACK == dispatch_manifest.UNCHECKED_NOTE_TEMPLATE


def test_manifest_note_comes_before_the_other_warn_parts(tmp_path):
    # a skip note plus a missing given-path: one JSON object, the manifest note first
    # FLIPPED (B-245, spec 6.5): the fake given path now REFUSES (a) ...
    (tmp_path / "tools").mkdir()  # a top-level entry: makes `tools/...` a path candidate under this tmp root (t-796)
    prompt = "Given: tools/fake_does_not_exist_b201.py\n" + _SKIP_LINE.replace("given, ", "")
    payload = _builder_payload(prompt, description="sonnet: probe")
    payload["cwd"] = str(tmp_path)
    result = _run_hook(payload)
    assert result.returncode == 2
    assert "tools/fake_does_not_exist_b201.py" in result.stderr
    assert payload["cwd"] in result.stderr and "manifest-skip: given|owns" in result.stderr
    # ... (b) with a skip line naming given it passes: the SKIP NOTE first, and NO
    # GIVEN-PATH WARN (the old layer no longer fires on paths inside the sections)
    prompt = "Given: tools/fake_does_not_exist_b201.py\n" + _SKIP_LINE + "\nmanifest-skip: given -- a probe\n"
    payload = _builder_payload(prompt, description="sonnet: probe")
    payload["cwd"] = str(tmp_path)
    code, out, err = _hook_out(_run_hook(payload))
    assert code == 0, err
    ctx = _context(out)
    assert ctx.startswith("MANIFEST-SKIP:") and "GIVEN-PATH WARN" not in ctx
    assert "PATH CHECK: the given paths were not checked on purpose" in ctx


# ---------------------------------------------------------------------
# t-575: the parallel cap and the push-before-launch WARN.
# ---------------------------------------------------------------------


def _cap():
    """The cap number lives ONCE, in dispatch_gate.PARALLEL_CAP (t-1140); every count below derives from it."""
    return dispatch_gate.PARALLEL_CAP


def _subagents_home(tmp_path, monkeypatch, n_fresh, n_old=0, session="sess-1"):
    folder = tmp_path / "proj" / session / "subagents"
    folder.mkdir(parents=True)
    now = time.time()
    for i in range(n_fresh):
        f = folder / ("agent-fresh%d.jsonl" % i)
        f.write_text("{}\n", encoding="utf-8")
        os.utime(f, (now - i, now - i))
        f.with_name("agent-fresh%d.meta.json" % i).write_text(json.dumps({"agentType": "builder"}), encoding="utf-8")
    for i in range(n_old):
        f = folder / ("agent-old%d.jsonl" % i)
        f.write_text("{}\n", encoding="utf-8")
        os.utime(f, (now - 2000, now - 2000))
    monkeypatch.setattr(dispatch_gate, "_projects_root", lambda: tmp_path)
    return folder


def _dispatch(prompt_extra="", **top):
    payload = _builder_payload(_manifest(suffix=prompt_extra), description="sonnet: fix")
    payload["session_id"] = "sess-1"
    payload.update(top)
    return payload


def _run_main(monkeypatch, capsys, payload):
    raw = json.dumps(payload).encode("utf-8")
    monkeypatch.setattr(dispatch_gate, "_read_stdin_bytes_deadline", lambda: (raw, False))
    code = dispatch_gate.main()
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_parallel_cap_full_cap_of_fresh_files_block_with_count_and_names(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2
    assert "%d writing-worker transcripts" % _cap() in err and "cap %d" % _cap() in err
    assert "agent-fresh0.jsonl" in err and "budget-skip: <reason>" in err


def test_parallel_cap_one_under_the_cap_fresh_files_pass(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() - 1)
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "")
    assert "PARALLEL CAP" not in out


def test_parallel_cap_old_files_do_not_count(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() - 1, n_old=_cap() + 1)
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 0


def test_parallel_cap_budget_skip_passes_with_a_note(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    code, out, err = _run_main(monkeypatch, capsys, _dispatch("budget-skip: the other writers are idle critics"))
    assert code == 0, err
    ctx = _context(json.loads(out))
    assert "BUDGET-SKIP: %d writing workers" % (_cap() + 1) in ctx and "the other writers are idle critics" in ctx


def test_parallel_cap_empty_skip_reason_does_not_pass(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    assert _run_main(monkeypatch, capsys, _dispatch("budget-skip:   "))[0] == 2


def test_parallel_cap_no_folder_no_session_or_unsafe_session_counts_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(dispatch_gate, "_projects_root", lambda: tmp_path)
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 0  # the folder does not exist
    payload = _dispatch()
    del payload["session_id"]
    assert _run_main(monkeypatch, capsys, payload)[0] == 0
    assert dispatch_gate.recent_subagent_files({"session_id": "../x"}) == []


def test_parallel_cap_ignores_non_dispatch_tools(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    assert dispatch_gate.parallel_cap_check({"tool_name": "Bash", "session_id": "sess-1"}) == (0, "", "")


# ---------------------------------------------------------------------
# D-0040: the parallel cap binds WRITING workers only. A worker's kind lives only in the first user line
# of its transcript (the dispatch prompt); the cap applies owns_declaration_has_path_token to it.
# ---------------------------------------------------------------------

_WRITER_PROMPT = "given: x\nowns: C:\\x\\y.py\nnon-goals: none"
_READER_PROMPT = "Review the diff in tools/x.py and report findings."


def _user_line(content):
    return json.dumps({"type": "user", "message": {"role": "user", "content": content}})


def _cap_folder(tmp_path, monkeypatch, workers, session="sess-1", kind=None):
    """workers: {file stem: first-line text, or None for an EMPTY file}; every file is fresh.
    kind: when given, an agent-<stem>.meta.json with that agentType is written beside every file
    (the sidecar the harness writes at launch)."""
    folder = tmp_path / "proj" / session / "subagents"
    folder.mkdir(parents=True)
    now = time.time()
    for i, (stem, first) in enumerate(workers.items()):
        f = folder / ("agent-%s.jsonl" % stem)
        f.write_text("" if first is None else first + "\n", encoding="utf-8")
        os.utime(f, (now - i, now - i))
        if kind is not None:
            (folder / ("agent-%s.meta.json" % stem)).write_text(
                json.dumps({"agentType": kind, "description": "x", "spawnDepth": 1}), encoding="utf-8")
    monkeypatch.setattr(dispatch_gate, "_projects_root", lambda: tmp_path)
    return folder


def _writers(n):
    return {"w%d" % i: _user_line(_WRITER_PROMPT) for i in range(n)}


def _reading_dispatch(**tool_input):
    ti = {"subagent_type": "critic", "prompt": _READER_PROMPT}
    ti.update(tool_input)
    if (ti["subagent_type"] in _HANDOFF_BY_KIND and isinstance(ti["prompt"], str)
            and "handoff" not in ti["prompt"].lower()):
        ti["prompt"] += "\n" + _HANDOFF_BY_KIND[ti["subagent_type"]]  # F6-37: a gated kind names its report path
    return {"tool_name": "Task", "session_id": "sess-1", "tool_input": ti}


def test_parallel_cap_d0040_a_writing_dispatch_over_the_cap_of_writers_is_blocked(tmp_path, monkeypatch, capsys):
    _cap_folder(tmp_path, monkeypatch, _writers(_cap()), kind="builder")  # both roads: the meta AND the owns line
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2
    assert "%d writing-worker transcripts" % _cap() in err and "cap %d" % _cap() in err
    assert "budget-skip: <reason>" in err


def test_parallel_cap_d0040_builder_meta_counts_without_an_owns_line(tmp_path, monkeypatch, capsys):
    """t-673: 36 of 321 real builder transcripts (09-30, before R11-f) carry no owns line; the meta
    (agentType builder) still counts them, so the (cap+1)-th writer cannot pass."""
    no_owns = {"b%d" % i: _user_line(_READER_PROMPT) for i in range(_cap())}
    _cap_folder(tmp_path, monkeypatch, no_owns, kind="builder")
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in err


def test_parallel_cap_d0040_critic_meta_without_an_owns_line_is_not_counted(tmp_path, monkeypatch, capsys):
    """The negative control of the case above: the same cap files, agentType critic -> they are readers."""
    no_owns = {"c%d" % i: _user_line(_READER_PROMPT) for i in range(_cap())}
    _cap_folder(tmp_path, monkeypatch, no_owns, kind="critic")
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "") and "PARALLEL CAP" not in out


def test_parallel_cap_d0040_a_reading_dispatch_is_neither_counted_nor_blocked(tmp_path, monkeypatch, capsys):
    _cap_folder(tmp_path, monkeypatch, _writers(_cap()))
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 2  # control: the same cap of writers block a writer
    code, out, err = _run_main(monkeypatch, capsys, _reading_dispatch())
    assert code == 0, err
    assert "writing-worker transcripts" not in out and "PARALLEL CAP" not in err  # t-847: a note, never a refusal


def test_parallel_cap_d0040_reading_workers_are_not_counted(tmp_path, monkeypatch, capsys):
    workers = _writers(_cap() - 1)
    workers["r_str"] = _user_line(_READER_PROMPT)
    workers["r_blocks"] = _user_line([{"type": "text", "text": _READER_PROMPT}])
    folder = _cap_folder(tmp_path, monkeypatch, workers)
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "")  # cap-1 writers counted, 2 readers not
    assert "PARALLEL CAP" not in out
    (folder / ("agent-w%d.jsonl" % (_cap() - 1))).write_text(_user_line(_WRITER_PROMPT) + "\n", encoding="utf-8")  # control
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in err  # the readers still are not in the count


def test_parallel_cap_d0040_unknown_first_line_counts_as_a_writer(tmp_path, monkeypatch, capsys):
    workers = _writers(_cap() - 2)
    workers["empty"] = None
    workers["malformed"] = "{not json"
    _cap_folder(tmp_path, monkeypatch, workers)
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in err


def test_parallel_cap_d0040_a_builder_without_owns_is_still_a_writing_dispatch(tmp_path, monkeypatch):
    _cap_folder(tmp_path, monkeypatch, _writers(_cap()))
    payload = _reading_dispatch(subagent_type="builder", prompt="do it, no manifest at all")
    code, message, _note = dispatch_gate.parallel_cap_check(payload)
    assert code == 2 and "%d writing-worker transcripts" % _cap() in message


def test_parallel_cap_d0040_is_writing_dispatch_edges():
    check = dispatch_gate.is_writing_dispatch
    assert check(_dispatch()) is True  # owns with a path
    assert check(_reading_dispatch()) is False
    assert check(_reading_dispatch(subagent_type="builder")) is True
    for prompt in (None, ["owns: C:\\x\\y.py"], 5):  # E5: a non-str prompt, only the type decides
        assert check(_reading_dispatch(prompt=prompt)) is False
        assert check(_reading_dispatch(prompt=prompt, subagent_type="builder")) is True
    assert check({"tool_name": "Task"}) is False and check({"tool_input": None}) is False  # no tool_input


def test_parallel_cap_d0040_budget_skip_still_passes_a_writing_dispatch(tmp_path, monkeypatch, capsys):
    """E6: the door is unchanged; the note counts writing workers."""
    _cap_folder(tmp_path, monkeypatch, _writers(_cap() + 1))
    code, out, err = _run_main(monkeypatch, capsys, _dispatch("budget-skip: the others are idle"))
    assert code == 0, err
    ctx = _context(json.loads(out))
    assert "BUDGET-SKIP: %d writing workers" % (_cap() + 1) in ctx and "the others are idle" in ctx


def test_parallel_cap_d0040_all_readers_never_produce_a_zero_count_refusal(tmp_path, monkeypatch, capsys):
    """E7: the refusal needs len(filtered files) >= the cap, so "0 writing-worker transcripts" cannot print."""
    _cap_folder(tmp_path, monkeypatch, {"r%d" % i: _user_line(_READER_PROMPT) for i in range(_cap() + 1)})
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "") and "PARALLEL CAP" not in out


# ---------------------------------------------------------------------
# t-847 (forge F6-1): a READER is neither counted nor blocked at the full cap, and a reader's worker
# transcript is not counted as a writer because its PROSE says "owns/non-goals/queue" (the live case 16.10:
# the token "/non-goals/queue" after the word "owns" read as a POSIX absolute path).
# ---------------------------------------------------------------------

_LIVE_DESIGNER_PROMPT = (
    "Task t-846 -- designer: draft the spec for conductor/3 node C3-18 from this Lead intent brief.\n"
    "\n"
    "What the draft contains: the numbered binding items in the house form: "
    "\u00a78 owns/non-goals/queue lines against the batches in work "
    "(conductor/2 C2-5s owns `story_run.py` under its fix round; C3-12 owns `controller.py`/`contract.py`/"
    "`story_step.py` right now -- name every shared file with a queue line), \u00a79 the forks.\n"
    "\n"
    "given: C:\\x\\finding.md\n"
    "non-goals: deciding the forks; code.\n"
    "handoff: C:\\x\\specs\\t-846-spec.md -- the draft."
)
_READER_KINDS = ["scout", "critic", "designer"]


def _cap_live_writers(tmp_path, monkeypatch):
    return _cap_folder(tmp_path, monkeypatch, _writers(_cap()), kind="builder")


def _add_worker(folder, stem, prompt, kind=None):
    f = folder / ("agent-%s.jsonl" % stem)
    f.write_text("" if prompt is None else _user_line(prompt) + "\n", encoding="utf-8")
    if kind is not None:
        f.with_name("agent-%s.meta.json" % stem).write_text(json.dumps({"agentType": kind}), encoding="utf-8")
    return f


def _cap_warning_lines(text):
    return [ln for ln in text.replace("\\n", "\n").splitlines() if "PARALLEL CAP" in ln]


@pytest.mark.parametrize("kind", _READER_KINDS)
def test_f61_a_reader_at_the_cap_of_live_writers_is_allowed_without_a_budget_skip(tmp_path, monkeypatch, capsys, kind):
    _cap_live_writers(tmp_path, monkeypatch)
    code, out, err = _run_main(monkeypatch, capsys, _reading_dispatch(subagent_type=kind))
    assert code == 0, err
    assert "PARALLEL CAP: %d writing-worker" % _cap() not in err and "budget-skip" not in err.lower()


@pytest.mark.parametrize("kind", _READER_KINDS + ["general-purpose"])
def test_f61_a_reader_at_the_full_cap_gets_one_warning_naming_all_the_writers(tmp_path, monkeypatch, capsys, kind):
    _cap_live_writers(tmp_path, monkeypatch)
    code, out, err = _run_main(monkeypatch, capsys, _reading_dispatch(subagent_type=kind))
    assert code == 0, err
    lines = _cap_warning_lines(_context(json.loads(out)))
    assert len(lines) == 1, lines
    assert lines[0].startswith("PARALLEL CAP: %d writers live (" % _cap())
    assert all("agent-w%d.jsonl" % i in lines[0] for i in range(_cap()))
    assert lines[0].endswith("this reader is not counted (D-0040)")


def test_f61_c_the_cap_plus_first_builder_is_still_refused(tmp_path, monkeypatch, capsys):
    """The control: the same cap of live writers, a writing (builder) dispatch -> the refusal, exit 2."""
    _cap_live_writers(tmp_path, monkeypatch)
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2
    assert "PARALLEL CAP: %d writing-worker transcripts" % _cap() in err and "budget-skip: <reason>" in err


def test_f61_d_a_scout_with_an_owns_header_and_a_path_is_a_writer_and_refused(tmp_path, monkeypatch, capsys):
    """D-0040: a reader given an inline owns manifest counts as a writer."""
    _cap_live_writers(tmp_path, monkeypatch)
    code, out, err = _run_main(monkeypatch, capsys, _reading_dispatch(subagent_type="scout", prompt=_manifest()))
    assert code == 2 and "PARALLEL CAP: %d writing-worker transcripts" % _cap() in err


def test_f61_e_the_live_case_a_designer_prose_about_owns_is_not_a_live_writer(tmp_path, monkeypatch, capsys):
    folder = _cap_folder(tmp_path, monkeypatch, _writers(_cap() - 1), kind="builder")
    designer = _add_worker(folder, "designer", _LIVE_DESIGNER_PROMPT, kind="designer")
    assert dispatch_gate.owns_declaration_has_path_token(_LIVE_DESIGNER_PROMPT) is False
    assert dispatch_gate.transcripts.is_writer(designer, dispatch_gate.owns_declaration_has_path_token) is False
    live = dispatch_gate.recent_subagent_files(_dispatch())
    assert sorted(f.name for f in live) == sorted("agent-w%d.jsonl" % i for i in range(_cap() - 1))
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())  # the later builder at cap-1 true writers
    assert code == 0, err


def test_f61_e_the_same_prose_in_a_dispatch_does_not_make_it_a_writing_dispatch():
    assert dispatch_gate.is_writing_dispatch(_reading_dispatch(subagent_type="designer", prompt=_LIVE_DESIGNER_PROMPT)) is False


def test_f61_edge_a_reader_with_a_budget_skip_line_is_allowed_as_today(tmp_path, monkeypatch, capsys):
    _cap_live_writers(tmp_path, monkeypatch)
    payload = _reading_dispatch(prompt=_READER_PROMPT + "\nbudget-skip: the writers are idle")
    code, out, err = _run_main(monkeypatch, capsys, payload)
    assert code == 0, err
    assert "BUDGET-SKIP" not in out  # no second door: the reader is not counted at all


@pytest.mark.parametrize("n_writers", [0, "cap-1"])
def test_f61_edge_a_reader_under_the_full_cap_gets_no_warning(tmp_path, monkeypatch, capsys, n_writers):
    n_writers = _cap() - 1 if n_writers == "cap-1" else n_writers
    _cap_folder(tmp_path, monkeypatch, _writers(n_writers), kind="builder")
    code, out, err = _run_main(monkeypatch, capsys, _reading_dispatch(subagent_type="scout"))
    assert (code, err) == (0, "")
    assert "PARALLEL CAP" not in out


def test_f61_edge_no_sidecar_and_an_unreadable_first_line_is_still_counted_as_a_writer(tmp_path, monkeypatch, capsys):
    """Today's documented answer, unchanged: an unknown kind with no readable prompt is a writer."""
    folder = _cap_folder(tmp_path, monkeypatch, _writers(_cap() - 1), kind="builder")
    _add_worker(folder, "unknown", None)  # empty file, no meta
    assert len(dispatch_gate.recent_subagent_files(_dispatch())) == _cap()
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in err


def test_f61_edge_an_owns_header_inside_a_fence_or_a_quote_counts_as_a_writer_today(tmp_path, monkeypatch):
    """Pinned as is (the cap uses the bare predicate, not the region-aware twin): a fenced or quoted example
    of an owns header with a path reads as a declaration. Narrowing that is F6-8 (the shared cut), not this node."""
    for prompt in ("```\nowns: C:\\x\\y.py\n```", "> owns: C:\\x\\y.py"):
        assert dispatch_gate.owns_declaration_has_path_token(prompt) is True, prompt
        assert dispatch_gate.is_writing_dispatch(_reading_dispatch(prompt=prompt)) is True, prompt
    folder = _cap_folder(tmp_path, monkeypatch, {}, kind="builder")
    quoted = _add_worker(folder, "quoted", "Review.\n```\nowns: C:\\x\\y.py\n```", kind="scout")
    assert dispatch_gate.transcripts.is_writer(quoted, dispatch_gate.owns_declaration_has_path_token) is True


@pytest.mark.parametrize("prompt, expected", [
    ("owns: C:\\x\\y.py", True),                                  # the header, path on the line
    ("- owns: C:\\x\\y.py", True),                                # a bullet header
    ("**owns (ABSOLUTE write paths):** C:\\x\\y.py", True),       # a bold header with a parenthetical
    ("owns:\nC:\\x\\y.py", True),                                 # the path right under the header
    ("  owns: /tools/x.py", True),                                # an indented header
    ("see 5 owns/non-goals/queue lines", False),                  # the live case: prose, a glued slash
    ("C3-12 owns /tools/x.py right now", False),                  # prose with a real absolute path, no colon
    ("name every owns line: /tools/x.py is not a header here", False),  # prose, the colon is not after the key
    ("owns/non-goals/queue lines", False),                        # at line start but not a header (no colon)
])
def test_f61_owns_predicate_reads_the_header_form_only(prompt, expected):
    assert dispatch_gate.owns_declaration_has_path_token(prompt) is expected


# ---------------------------------------------------------------------
# t-855 (forge F6-8): ONE owns predicate. "Does this dispatch / worker own a path" is answered by
# dispatch_manifest.has_owned_paths (the cut + owned_paths); the parallel-writer limit and handoff_gate ask
# the same question, so one dispatch gets one answer on both gates. The class's one rule: an owns of
# RELATIVE paths only is no declaration -- a reader for the limit and for handoff_gate alike.
# ---------------------------------------------------------------------

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "dispatch_manifest"
_REL_ONLY_OWNS = ["owns: tools/x.py\nnon-goals: none", "owns:\ntools/x.py\ntools/y.py", "- owns: tools/*.py, docs/z.md"]
_ONE_ANSWER_DISPATCHES = {
    "abs-header": "given: x\nowns: C:\\x\\y.py\nnon-goals: none",
    "posix-header": "owns: /w/tools/x.py\nnon-goals: none",
    "bullet": "- owns: C:\\x\\y.py",
    "bold": "**owns (ABSOLUTE write paths):** C:\\x\\y.py",
    "next-lines": "owns:\n- C:\\x\\a.py\n- C:\\x\\b.py\n",
    "backticks-with-spaces": "owns: `C:\\Program Files\\x y.py`",
    "relative-only-1": _REL_ONLY_OWNS[0],
    "relative-only-lines": _REL_ONLY_OWNS[1],
    "relative-only-bullet-glob": _REL_ONLY_OWNS[2],
    "bare-owns": "owns:",
    "live-designer-prose": _LIVE_DESIGNER_PROMPT,
    "prose-with-abs-path": "C3-12 owns /tools/x.py right now",
    "K1": (_FIXTURES_DIR / "K1.txt").read_bytes().decode("utf-8"),
    "K2": (_FIXTURES_DIR / "K2.txt").read_bytes().decode("utf-8"),
    "K3": (_FIXTURES_DIR / "K3.txt").read_bytes().decode("utf-8"),
    "K4": (_FIXTURES_DIR / "K4.txt").read_bytes().decode("utf-8"),
    "K7": (_FIXTURES_DIR / "K7.txt").read_bytes().decode("utf-8"),
    "K8": (_FIXTURES_DIR / "K8.txt").read_bytes().decode("utf-8"),
}


def _handoff_gate_lets_it_write_anywhere(text):
    """handoff_gate's verdict for a worker of UNKNOWN kind running this dispatch: pass = a writing worker
    (an owns path), refused = a reader locked to its handoff file."""
    import handoff_gate
    folders = list(dispatch_manifest.HANDOFF_DIRS.values())
    return handoff_gate._gate(None, folders, text, "/elsewhere/z.py", "/")[0] == 0


@pytest.mark.parametrize("name", list(_ONE_ANSWER_DISPATCHES))
def test_f68_one_dispatch_one_answer_at_the_limit_and_at_handoff_gate(name):
    text = _ONE_ANSWER_DISPATCHES[name]
    limit_counts_a_writer = dispatch_gate.is_writing_dispatch(_reading_dispatch(subagent_type="scout", prompt=text))
    assert limit_counts_a_writer is dispatch_gate.owns_declaration_has_path_token(text)
    assert limit_counts_a_writer is _handoff_gate_lets_it_write_anywhere(text), name
    assert limit_counts_a_writer is bool(dispatch_manifest.owned_paths(dispatch_manifest.section_cut(text))), name


def test_f68_the_pair_is_not_vacuous_it_holds_writers_and_readers_on_both_sides():
    answers = {n: dispatch_gate.owns_declaration_has_path_token(t) for n, t in _ONE_ANSWER_DISPATCHES.items()}
    assert answers["abs-header"] and answers["bullet"] and answers["next-lines"] and answers["backticks-with-spaces"]
    assert not answers["relative-only-1"] and not answers["live-designer-prose"] and not answers["bare-owns"]


def test_f68_the_predicate_is_a_thin_call_to_the_one_reader(monkeypatch):
    calls = []

    def spy(text, include_quoted=False):
        calls.append((text, include_quoted))
        return "sentinel"

    monkeypatch.setattr(dispatch_gate._load_manifest_module(), "has_owned_paths", spy)
    assert dispatch_gate.owns_declaration_has_path_token("any text") == "sentinel"
    assert calls == [("any text", True)]  # the limit counts a quoted example too (t-847's pin)
    assert dispatch_gate._region_aware_owns_declaration_has_path_token("other", object()) == "sentinel"
    assert calls[-1] == ("other", False)  # check 2's region-aware twin leaves quoted owns out
    calls.clear()
    assert dispatch_gate.owns_declaration_has_path_token("") is False and dispatch_gate.owns_declaration_has_path_token(None) is False
    assert calls == []  # an empty / non-str prompt never reaches the reader


def test_f68_there_is_no_second_owns_header_grammar_in_dispatch_gate():
    for name in ("_OWNS_HEADER_RE", "_owns_header_marker", "_owns_region_has_path_token", "_OWNS_TOKEN_SPLIT_RE",
                 "_OWNS_MARKER_JUNK_ONLY_RE", "_OWNS_DECLARATION_PREFIX_RE", "_section_stop"):
        assert not hasattr(dispatch_gate, name), name


@pytest.mark.parametrize("owns", ["owns: tools/x.py", "owns:\ntools/*.py", "- owns: tools/a.py, tools/b.py"])
def test_f68_rare_case_a_relative_only_owns_is_a_reader_for_the_limit(tmp_path, monkeypatch, capsys, owns):
    """The class's one rule, limit side (handoff_gate side: test_handoff_gate.py): a worker of UNKNOWN kind (no
    sidecar) whose owns holds relative paths only is not a writer and not counted; before t-855 it was."""
    prompt = "Review it.\ngiven: docs/a.md\n" + owns + "\nnon-goals: none"
    assert dispatch_gate.is_writing_dispatch(_reading_dispatch(subagent_type="general-purpose", prompt=prompt)) is False
    folder = _cap_folder(tmp_path, monkeypatch, _writers(_cap() - 1), kind="builder")
    unknown = _add_worker(folder, "unknown", prompt)  # no meta: kind unknown, decided by the prompt
    assert dispatch_gate.transcripts.is_writer(unknown, dispatch_gate.owns_declaration_has_path_token) is False
    assert sorted(f.name for f in dispatch_gate.recent_subagent_files(_dispatch())) == sorted(
        "agent-w%d.jsonl" % i for i in range(_cap() - 1))
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())  # the later builder at cap-1 true writers
    assert code == 0, err


def test_f68_a_worker_of_unknown_kind_with_an_absolute_owns_path_is_still_counted(tmp_path, monkeypatch, capsys):
    folder = _cap_folder(tmp_path, monkeypatch, _writers(_cap() - 1), kind="builder")
    _add_worker(folder, "unknown", "Do it.\nowns: C:\\x\\y.py\nnon-goals: none")
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in err


def test_f68_known_divergence_a_quoted_owns_is_counted_by_the_limit_and_ignored_by_handoff_gate():
    """Pinned as the t-847 answer (test_f61_edge_an_owns_header_inside_a_fence_or_a_quote_counts_as_a_writer_today):
    the limit counts a fenced or quoted owns header with an absolute path -- the safe side of a cap -- while
    handoff_gate reads quoted text as prose and locks such a worker to its handoff file."""
    for text in ("Review.\n```\nowns: C:\\x\\y.py\n```", "Review.\n> owns: C:\\x\\y.py"):
        assert dispatch_gate.owns_declaration_has_path_token(text) is True
        assert _handoff_gate_lets_it_write_anywhere(text) is False


def _fake_git(answers, calls=None):
    """answers: {tuple(git args): stdout}; a missing key is a git error (rc 128)."""
    def run(args, **kwargs):
        if calls is not None:
            calls.append((args, kwargs.get("cwd")))
        out = answers.get(tuple(args[1:]))
        return subprocess.CompletedProcess(args, 0 if out is not None else 128, stdout=(out or "") + "\n", stderr="")
    return run


AHEAD = ("rev-list", "--count", "refs/remotes/origin/main..refs/heads/main")
LOCAL_MAIN = ("rev-parse", "refs/heads/main")
ORIGIN_MAIN = ("rev-parse", "refs/remotes/origin/main")


def _worktree_dispatch():
    return {"tool_name": "Agent", "cwd": "Z:/r", "tool_input": {"isolation": "worktree"}}


def test_push_before_launch_warns_when_main_is_ahead_of_origin(monkeypatch, capsys):
    calls = []
    git = {AHEAD: "3", LOCAL_MAIN: "aaa1111", ORIGIN_MAIN: "bbb2222"}
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git(git, calls))
    payload = _dispatch(cwd="Z:/repo")
    payload["tool_input"]["isolation"] = "worktree"
    code, out, err = _run_main(monkeypatch, capsys, payload)
    ctx = _context(json.loads(out))
    assert code == 0
    assert "aaa1111" in ctx and "bbb2222" in ctx and "3 commit(s) ahead" in ctx and "push main first" in ctx
    assert "create the worktree yourself from main" in ctx and "merge aaa1111 first" not in ctx
    assert "git -C <repo> worktree add <path> -b <branch> main" in ctx  # the one door text of both WARNs (NB3)
    assert all(cwd == "Z:/repo" for _a, cwd in calls)


def test_push_before_launch_silent_when_origin_is_ahead_or_equal(monkeypatch):
    """t-576 F7: only LOCAL commits missing on origin matter; origin ahead of main must not warn."""
    shas = {LOCAL_MAIN: "aaa", ORIGIN_MAIN: "bbb"}
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git({AHEAD: "0", **shas}))
    assert dispatch_gate.push_before_launch_warn(_worktree_dispatch()) == ""  # origin ahead: shas differ, count 0
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git({AHEAD: "1", **shas}))
    assert "1 commit(s) ahead" in dispatch_gate.push_before_launch_warn(_worktree_dispatch())


def test_push_before_launch_silent_on_other_isolation_and_git_errors(monkeypatch):
    base = _worktree_dispatch()
    git = {AHEAD: "2", LOCAL_MAIN: "aaa", ORIGIN_MAIN: "bbb"}
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git(git))
    assert dispatch_gate.push_before_launch_warn({**base, "tool_input": {}}) == ""
    assert dispatch_gate.push_before_launch_warn({**base, "tool_input": {"isolation": "none"}}) == ""
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git({LOCAL_MAIN: "aaa"}))  # no origin/main
    assert dispatch_gate.push_before_launch_warn(base) == ""
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git({AHEAD: "not a number"}))
    assert dispatch_gate.push_before_launch_warn(base) == ""

    def boom(*a, **k):
        raise OSError("git is not installed")

    monkeypatch.setattr(dispatch_gate.subprocess, "run", boom)
    assert dispatch_gate.push_before_launch_warn(base) == ""


def _base_git(refs, ahead=(), rc_other=1, calls=None):
    """Fake git for worktree_base_warn: refs = for-each-ref output lines (local ones carry no `origin/`);
    `ahead` = ref names whose is-ancestor exit is 1; every other is-ancestor exit is `rc_other` (None = OSError)."""
    def run(args, **kwargs):
        if calls is not None:
            calls.append(args)
        rest = tuple(args[1:])
        if rest[:1] == ("for-each-ref",):
            if refs is None:
                return subprocess.CompletedProcess(args, 128, stdout="", stderr="")
            assert rest == ("for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes"), rest
            full = [("refs/remotes/" if r.startswith("origin/") else "refs/heads/") + r for r in refs]
            return subprocess.CompletedProcess(args, 0, stdout="\n".join(full) + "\n", stderr="")
        if rest[:2] == ("merge-base", "--is-ancestor"):
            if rc_other is None:
                raise OSError("no git")
            name = rest[2].split("/", 2)[2] if rest[2].startswith("refs/heads/") else rest[2][len("refs/remotes/"):]
            return subprocess.CompletedProcess(args, 1 if name in ahead else rc_other, stdout="", stderr="")
        if rest == ORIGIN_MAIN:
            return subprocess.CompletedProcess(args, 0, stdout="bbb2222\n", stderr="")
        return subprocess.CompletedProcess(args, 128, stdout="", stderr="")
    return run


def _base_payload(prompt, **tool_input):
    return {"tool_name": "Agent", "cwd": "Z:/r", "tool_input": {"isolation": "worktree", "prompt": prompt, **tool_input}}


_MANY = ["wip/b%d" % i for i in range(7)]
_BASE_ROWS = [
    ("b1", "Base: pile/x/batch-1 please", ["pile/x/batch-1"], ["pile/x/batch-1"], 1,
     ["WORKTREE BASE", "pile/x/batch-1", "bbb2222", "git -C <repo> worktree add <path> -b <branch> pile/x/batch-1"]),
    ("b2", "Base: pile/x/batch-1 please", ["pile/x/batch-1"], [], 0, None),
    ("b4", "from main, origin/main, HEAD", ["main", "origin/main"], ["main", "origin/main"], 1, None),
    ("b5", " ".join(_MANY), _MANY, _MANY, 1, ["(2 more names not checked)", "wip/b4"]),
    ("b6", " ".join(_MANY[:5]), _MANY, _MANY, 1, ["wip/b4"]),
    ("b7a", "base `wip/oh8-6`", ["wip/oh8-6"], ["wip/oh8-6"], 1, ["wip/oh8-6"]),
    ("b7b", "base wip/oh8-6, then more", ["wip/oh8-6"], ["wip/oh8-6"], 1, ["wip/oh8-6"]),
    ("b8", "base wip/x", ["wip/x"], ["wip/x"], 128, None),
    ("b8a", "base wip/x", ["wip/x"], ["wip/x"], 1, ["wip/x"]),
    ("b8b", "base wip/x", ["wip/x"], [], 0, None),
    ("b8c", "base wip/x", ["wip/x"], [], None, None),
    ("b9a", None, ["wip/x"], ["wip/x"], 1, None),
    ("b9b", "", ["wip/x"], ["wip/x"], 1, None),
    ("b9c", "prose " * 50000, ["wip/x"], ["wip/x"], 1, None),
    ("b10", "base wip/\u0432\u0435\u0442\u043a\u0430 now", ["wip/\u0432\u0435\u0442\u043a\u0430"], ["wip/\u0432\u0435\u0442\u043a\u0430"], 1,
     ["wip/\u0432\u0435\u0442\u043a\u0430"]),
    ("b11", "base wip/x", ["wip/x", "origin/wip/x"], ["wip/x"], 1, ["wip/x"]),
    ("b14", "base pile/x", ["origin/pile/x"], ["pile/x", "origin/pile/x"], 1, None),
]


@pytest.mark.parametrize("row,prompt,refs,ahead,rc_other,expect", _BASE_ROWS, ids=[r[0] for r in _BASE_ROWS])
def test_worktree_base_warn(monkeypatch, row, prompt, refs, ahead, rc_other, expect):
    """B.4 rows: a WARN only for an isolation dispatch naming a branch origin/main lacks; every error is silence."""
    calls = []
    # rc_other 128 / None model a failing merge-base; for the other rows `ahead` decides exit 1 vs 0
    other = 0 if rc_other == 1 else rc_other
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _base_git(refs, ahead=ahead if rc_other == 1 else (), rc_other=other,
                                                                   calls=calls))
    if row == "b8":
        monkeypatch.setattr(dispatch_gate.subprocess, "run", _base_git(refs, rc_other=128))
    out = dispatch_gate.worktree_base_warn(_base_payload(prompt), None)
    if row != "b8":  # one for-each-ref call serves both the known names and the local/remote split (NB1)
        assert sum(1 for a in calls if a[1:2] == ["for-each-ref"]) == 1, (row, calls)
    if expect is None:
        assert out == "", row
    else:
        assert all(part in out for part in expect), (row, out)
        assert out.startswith("WORKTREE BASE")
    if row == "b6":
        assert "more names" not in out
    if row == "b11":
        assert sum(1 for a in calls if a[1:3] == ["merge-base", "--is-ancestor"]) == 1
        assert [a for a in calls if a[1:3] == ["merge-base", "--is-ancestor"]][0][3] == "refs/heads/wip/x"


def test_worktree_base_warn_b3_only_host_worktrees(monkeypatch):
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _base_git(["wip/x"], ahead=["wip/x"]))
    prompt = "base wip/x"
    assert "WORKTREE BASE" in dispatch_gate.worktree_base_warn(_base_payload(prompt), None)
    for payload in ({"tool_name": "Agent", "cwd": "Z:/r", "tool_input": {"prompt": prompt}},
                    _base_payload(prompt, isolation="none"),
                    {**_base_payload(prompt), "tool_name": "Bash"},
                    {"tool_name": "Agent", "cwd": "Z:/r", "tool_input": None}):
        assert dispatch_gate.worktree_base_warn(payload, None) == ""


def test_worktree_base_warn_b8_for_each_ref_fails(monkeypatch):
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _base_git(None))
    assert dispatch_gate.worktree_base_warn(_base_payload("base wip/x"), None) == ""

    def boom(*a, **k):
        raise OSError("git is not installed")

    monkeypatch.setattr(dispatch_gate.subprocess, "run", boom)
    assert dispatch_gate.worktree_base_warn(_base_payload("base wip/x"), None) == ""


def test_worktree_base_warn_b12_push_warn_pins_the_qualified_argv(monkeypatch):
    git = {AHEAD: "2", LOCAL_MAIN: "aaa", ORIGIN_MAIN: "bbb"}  # the fake answers ONLY the qualified argv
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _fake_git(git))
    assert "PUSH BEFORE LAUNCH" in dispatch_gate.push_before_launch_warn(_worktree_dispatch())


def test_worktree_base_warn_b13_quoted_names_do_not_count(monkeypatch):
    monkeypatch.setattr(dispatch_gate.subprocess, "run", _base_git(["wip/x"], ahead=["wip/x"]))
    fenced = "Review.\n```\nbase wip/x\n```\nend"
    cut = dispatch_manifest.section_cut(fenced)
    assert not cut.degraded
    assert dispatch_gate.worktree_base_warn(_base_payload(fenced), cut) == ""
    # control: the same name in prose is found through the same cut
    prose = "Review.\nbase wip/x\nend"
    assert "wip/x" in dispatch_gate.worktree_base_warn(_base_payload(prose), dispatch_manifest.section_cut(prose))


def _finish(folder, name):
    """Turn agent-<name>.jsonl into a finished worker transcript (its last tool_use is SubagentHandback)."""
    call = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": "SubagentHandback",
                                                          "input": {"message": "done"}}]}}
    path = folder / ("agent-%s.jsonl" % name)
    path.write_text(json.dumps(call) + "\n" + json.dumps({"type": "user", "message": {"content": "ok"}}) + "\n",
                    encoding="utf-8")
    return path


def test_parallel_cap_leaves_finished_transcripts_out(tmp_path, monkeypatch, capsys):
    """t-576 F5: cap fresh files, one of them handed back -> cap-1 live workers -> the dispatch passes."""
    folder = _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 2  # the cap of workers live: blocked (control)
    _finish(folder, "fresh0")
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "")
    live = dispatch_gate.recent_subagent_files({"session_id": "sess-1"})
    assert sorted(f.name for f in live) == sorted("agent-fresh%d.jsonl" % i for i in range(1, _cap()))


def test_parallel_cap_cap_live_still_block_and_all_finished_count_zero(tmp_path, monkeypatch, capsys):
    folder = _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 2
    for i in range(_cap()):
        _finish(folder, "fresh%d" % i)
    assert dispatch_gate.recent_subagent_files({"session_id": "sess-1"}) == []
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 0


# ---------------------------------------------------------------------
# B-245 (t-614): the PATH CHECK in decide_full -- branch A, rows P1-P23. The root is payload["cwd"]
# (a temp tree here); a refusal names the missing paths, the root and the doors.
# ---------------------------------------------------------------------


def _root(tmp_path):
    (tmp_path / "tools").mkdir(exist_ok=True)
    (tmp_path / "tools" / "have.py").write_bytes(b"x = 1\n")
    return tmp_path


def _pdecide(root, given="tools/have.py", owns=None, suffix="", cwd=True, description="sonnet: x"):
    owns = owns if owns is not None else str(root / "tools" / "have.py")
    payload = _builder_payload(_manifest(given=given, owns=owns, suffix=suffix), description=description)
    if cwd:
        payload["cwd"] = str(root)
    return dispatch_gate.decide_full(payload)


def test_P1_missing_given_path_refuses_with_path_root_and_doors(tmp_path):
    root = _root(tmp_path)
    d = _pdecide(root, given="tools/gone.py")
    assert d.code == 2
    assert "given: tools/gone.py" in d.message and str(root) in d.message
    assert "(new)" in d.message and "manifest-skip: given|owns -- <reason>" in d.message


def test_P2_P3_P4_owns_new_marker(tmp_path):
    root = _root(tmp_path)
    gone = str(root / "tools" / "gone.py")
    assert _pdecide(root, owns=gone).code == 2
    d = _pdecide(root, owns=gone + " (new)")
    assert d.code == 0 and [r.status for r in d.paths if r.kind == "owns"] == ["new"]
    d = _pdecide(root, owns=str(root / "tools" / "have.py") + " (new)")  # P3: exists -> a note, no refusal
    assert d.code == 0 and any("marked new but exists" in n for n in d.notes)
    d = _pdecide(root, given="tools/gone.py (new)")  # P4: (new) never excuses a given path
    assert d.code == 2 and "(new) is for owns only" in d.message


def test_P5_outside_root_is_not_checked(tmp_path):
    (tmp_path / "r").mkdir()
    root = _root(tmp_path / "r")
    d = _pdecide(root, given="`../foreign/nope.py`", owns=str(tmp_path / "foreign" / "nope.py") + " (new)")
    assert d.code == 0
    assert [r.status for r in d.paths if r.kind == "given"] == ["outside"]


def test_P6_P8_glob_and_prose_never_refuse(tmp_path):
    root = _root(tmp_path)
    d = _pdecide(root, given="tools/*.nothing https://example.com/tools/x.py <tools/x.py> $X/tools/y",
                 owns=str(root / "tools" / "*.zzz"))
    assert d.code == 0 and "glob" in [r.status for r in d.paths]


def test_P10_path_after_a_blank_line_in_given_is_not_read(tmp_path):
    assert _pdecide(_root(tmp_path), given="tools/have.py\n\ntools/gone.py").code == 0


def test_P11_no_cwd_is_a_note_not_a_check(tmp_path):
    d = _pdecide(_root(tmp_path), given="tools/gone.py", cwd=False)
    assert d.code == 0 and d.notes == ["PATH CHECK: paths unchecked: no cwd"]


def test_P12_degraded_read_never_refuses(tmp_path):
    d = _pdecide(_root(tmp_path), given="tools/gone.py " + "`a b` " * 201)
    assert d.code == 0 and any("degraded read" in n for n in d.notes)


def test_P13_cap_200_checked_201st_is_a_note(tmp_path):
    root = _root(tmp_path)
    for i in range(201):
        (root / "tools" / ("f%d.py" % i)).write_text("", encoding="utf-8")
    lines = ["tools/f%d.py" % i for i in range(201)]
    # the owns path counts first: 1 owns + 199 given are checked at the cap, 2 given are beyond it
    d = _pdecide(root, given="\n".join(lines))
    assert d.code == 0 and any("2 beyond the first 200" in n for n in d.notes)
    (root / "tools" / "f198.py").unlink()  # the 200th live candidate: checked -> refused
    assert _pdecide(root, given="\n".join(lines)).code == 2
    (root / "tools" / "f198.py").write_text("", encoding="utf-8")
    (root / "tools" / "f200.py").unlink()  # beyond the cap: never silent, never a refusal
    d = _pdecide(root, given="\n".join(lines))
    assert d.code == 0 and any("beyond the first 200" in n for n in d.notes)


def test_P14_directory_exists_or_needs_new(tmp_path):
    root = _root(tmp_path)
    assert _pdecide(root, given="tools/").code == 0
    assert _pdecide(root, owns=str(root / "newdir") + "/").code == 2
    assert _pdecide(root, owns=str(root / "newdir") + "/ (new)").code == 0


def test_P15_skip_waives_only_the_item_it_names(tmp_path):
    root = _root(tmp_path)
    d = _pdecide(root, given="tools/gone.py", suffix="manifest-skip: given -- carried by the spec")
    assert d.code == 0 and any("given paths were not checked on purpose" in n for n in d.notes)
    d = _pdecide(root, owns=str(root / "tools" / "gone.py"), suffix="manifest-skip: given -- carried by the spec")
    assert d.code == 2  # a skip naming another item waives nothing here


def test_P18_exception_in_the_path_check_is_a_note_and_the_label_check_still_runs(tmp_path, monkeypatch):
    root = _root(tmp_path)

    def boom(*a):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_gate, "_path_check", boom)
    d = _pdecide(root, given="tools/gone.py")
    assert d.code == 0 and any("paths not checked: RuntimeError" in n for n in d.notes)
    assert _pdecide(root, description="nolabel").code == 2


def test_P19_P20_P21_unknowns_are_notes_never_refusals(tmp_path):
    root = _root(tmp_path)
    assert _pdecide(root, given="tools/have.py (docstring EDGE (c) only)").code == 0  # P19
    # P20: prose between the key and the colon -> the header is not a bare declaration
    payload = _builder_payload(_manifest(given=None, prefix="Given that it was renamed: tools/old.py was the name"),
                               description="sonnet: x")
    payload["cwd"] = str(root)
    d = dispatch_gate.decide_full(payload)
    assert d.code == 0 and any("not a bare declaration" in n for n in d.notes)
    # P21: a line inside an unterminated fence
    payload = _builder_payload("```\n" + _manifest(given="tools/gone.py"), description="sonnet: x")
    payload["cwd"] = str(root)
    d = dispatch_gate.decide_full(payload)
    assert d.code == 0 and any("inside an unterminated fence opened at line 1" in n for n in d.notes)


def test_P22_P23_a_command_in_given_and_the_dod_test_path_never_block(tmp_path):
    root = _root(tmp_path)
    assert _pdecide(root, given="`git diff origin/main...HEAD` and `python tools/gone.py --check`").code == 0
    d = _pdecide(root)  # the DoD names tools/test_dispatch_gate.py: never a given path
    assert d.code == 0 and all(r.path != "tools/test_dispatch_gate.py" for r in d.paths)


@pytest.mark.parametrize("wrap", ["%s", "`%s`"])
def test_f626_an_owns_path_with_a_function_list_passes_the_path_check_by_the_path_alone(tmp_path, wrap):
    """t-877 (D-0048): `owns: <path> (f1, f2)` -- the path is found and checked as the PATH, the list is no part of it."""
    root = _root(tmp_path)
    have = wrap % str(root / "tools" / "have.py")
    d = _pdecide(root, owns=have + " (take_answer, Driver.fallback_person)")
    assert d.code == 0, d.message
    assert [(r.kind, r.status, r.path) for r in d.paths if r.kind == "owns"] == [("owns", "ok", str(root / "tools" / "have.py"))]
    # the control: a MISSING path with the same list is still refused, and the refusal names the path without the list
    gone = str(root / "tools" / "gone.py")
    d = _pdecide(root, owns=wrap % gone + " (take_answer, fallback_person)")
    assert d.code == 2 and "owns: %s" % gone in d.message and "take_answer" not in d.message


def test_decide_keeps_the_pair_and_main_prints_the_path_lines(tmp_path, monkeypatch, capsys):
    root = _root(tmp_path)
    payload = _builder_payload(_manifest(given="tools/have.py", owns=str(root / "tools" / "have.py")),
                               description="sonnet: x")
    payload["cwd"] = str(root)
    assert dispatch_gate.decide(payload) == (0, "")
    code, out, err = _run_main(monkeypatch, capsys, payload)
    ctx = _context(json.loads(out))
    assert code == 0 and ctx.startswith("PATH CHECK: paths checked under the root:")
    assert "tools/have.py (6 bytes, 1 lines)" in ctx


def test_top_level_entries_has_both_spellings_of_case_and_is_none_when_unreadable(tmp_path):
    (tmp_path / "Tools").mkdir()
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    names = dispatch_gate.top_level_entries(str(tmp_path))
    assert {"Tools", "tools", "README.md", "readme.md"} <= names
    assert dispatch_gate.top_level_entries(str(tmp_path / "nope")) is None  # absent root
    assert dispatch_gate.top_level_entries(str(tmp_path / "README.md")) is None  # a file, not a root


def test_freshness_relative_anchor_needs_a_top_level_entry_of_the_root(tmp_path):
    """The relative anchor is a path only by the ONE predicate: `tools/..` (first segment an entry of the
    root) is checked, `../side/..` (leaving the root) is not -- it would be stat'ed under the old join."""
    root = tmp_path / "root"
    (root / "tools").mkdir(parents=True)
    (root / "tools" / "short.py").write_text("a\nb\n", encoding="utf-8")
    (tmp_path / "side").mkdir()
    (tmp_path / "side" / "short.py").write_text("a\nb\n", encoding="utf-8")

    def warn(prompt):
        return dispatch_gate.freshness_warn(
            {"tool_name": "Task", "tool_input": {"prompt": prompt}, "cwd": str(root)})

    assert warn("see tools/short.py:50").startswith("FRESHNESS WARN:")  # positive control: the layer fires
    assert warn("see ../side/short.py:50") == ""
    assert warn("see nodir/short.py:50") == ""


def test_main_decide_full_raising_is_a_note_exit_0_and_the_other_layers_still_run(tmp_path, monkeypatch, capsys):
    root = _root(tmp_path)

    def boom(payload):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_gate, "decide_full", boom)
    payload = {"tool_name": "Task", "cwd": str(root),
               "tool_input": {"subagent_type": "critic", "description": "opus: look",
                              "prompt": "Given: tools/gone.py for reference."}}
    code, out, err = _run_main(monkeypatch, capsys, payload)
    ctx = _context(json.loads(out))
    assert code == 0
    assert "check failed: RuntimeError" in ctx and "check failed: RuntimeError" in err
    assert "GIVEN-PATH WARN" in ctx and "tools/gone.py" in ctx  # the edge Decision has no cut: the layer cuts itself


def test_main_exception_in_the_path_check_is_a_note_and_the_label_check_still_runs(tmp_path, monkeypatch, capsys):
    root = _root(tmp_path)

    def boom(*a):
        raise RuntimeError("boom")

    monkeypatch.setattr(dispatch_gate, "_path_check", boom)
    payload = _builder_payload(_manifest(given="tools/gone.py"), description="sonnet: x")
    payload["cwd"] = str(root)
    code, out, err = _run_main(monkeypatch, capsys, payload)
    assert code == 0 and "PATH CHECK: paths not checked: RuntimeError" in _context(json.loads(out))
    payload = _builder_payload(_manifest(given="tools/gone.py"), description="nolabel")
    payload["cwd"] = str(root)
    code, out, err = _run_main(monkeypatch, capsys, payload)
    assert code == 2 and "worker's tier" in err


# ---------------------------------------------------------------------
# t-789 / t-796 (forge F5-8): the gate's verdict and the ONE-PROCESS readers. dispatch_gate.main() judges the
# dispatch; only on "allow" it runs critic_snapshot.run_after_gate and owns_gate.run_after_gate in the SAME
# process (the runtime starts the hooks of one matcher together, so no later hook can read a file in time);
# logs/dispatch_verdict.json is the written verdict for later readers and is read by no hook. Killing file of
# the writer, the key, claim_trace, the order, the exit codes and the concurrent-start tests: this one (the
# readers' own entry points and their both-worlds behaviour are pinned in their files).
# ---------------------------------------------------------------------

import tempfile  # noqa: E402
from datetime import datetime  # noqa: E402

import critic_snapshot  # noqa: E402
import owns_gate  # noqa: E402

_TOOLS = Path(__file__).resolve().parent


def _carrier(root):
    return json.loads((root / "logs" / "dispatch_verdict.json").read_text(encoding="utf-8"))


def _with_cwd(root, payload=None, tool_use_id=None):
    payload = payload or _dispatch()
    payload["cwd"] = str(root)
    if tool_use_id is not None:
        payload["tool_use_id"] = tool_use_id
    return payload


def _critic_payload(root, tool_use_id=None, prompt="Review the diff."):
    # F6-37: a critic dispatch names its report path (the manifest's placeholder handoff line is replaced)
    prompt = prompt.replace("handoff: a short report", _CRITIC_HANDOFF)
    if "handoff" not in prompt.lower():
        prompt += "\n" + _CRITIC_HANDOFF
    payload = _agent_payload("critic", "opus: review the diff", prompt, cwd=str(root))
    if tool_use_id is not None:
        payload["tool_use_id"] = tool_use_id
    return payload


def _registry_rows(root):
    path = root / "logs" / "owns_registry.jsonl"
    return len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0


def _spy_readers(monkeypatch, calls, codes=None, raises=None):
    """Replace both run_after_gate entry points by recorders; calls gets (name, carrier verdict at call time)."""
    for name, module in (("critic_snapshot", critic_snapshot), ("owns_gate", owns_gate)):
        def spy(payload, name=name):
            carrier = _carrier(Path(payload["cwd"]))["verdict"]
            calls.append((name, carrier))
            if raises and name in raises:
                raise RuntimeError("boom")
            return (codes or {}).get(name, 0)
        monkeypatch.setattr(module, "run_after_gate", spy)


def test_carrier_key_is_the_tool_use_id_when_the_payload_has_one(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    payload = _with_cwd(root, tool_use_id="toolu_01KeyKeyKey")
    code, out, err = _run_main(monkeypatch, capsys, payload)
    assert (code, err) == (0, "")
    rec = _carrier(root)
    assert set(rec) == {"ts", "verdict", "reason", "key", "key_kind"}
    assert (rec["verdict"], rec["key"], rec["key_kind"]) == ("allow", "toolu_01KeyKeyKey", "tool_use_id")


def test_verdict_key_without_an_id_is_the_content_key_with_the_prompt_length():
    k = dispatch_gate.verdict_key
    base = _dispatch("x" * 5000)
    same_head = _dispatch("x" * 5000)
    same_head["tool_input"]["prompt"] += "a tail differs beyond 4 KB"
    other_label = _dispatch("x" * 5000)
    other_label["tool_input"]["description"] = "opus: other"
    key, kind = k(base)
    assert kind == "content" and key.endswith(":%d" % len(base["tool_input"]["prompt"]))
    assert k(base) == k(_dispatch("x" * 5000))  # the same dispatch, the same key
    assert k(base) != k(same_head) and k(base) != k(other_label)  # the whole prompt, the length, the description
    assert k(_dispatch("a")) != k(_dispatch("b"))
    for no_id in ("", None, 7):  # not a usable id -> the content key, as if absent
        assert k(_dispatch(tool_use_id=no_id))[1] == "content"
    assert k({}) == k({"tool_input": []}) == k("not a dict") == ("", "")
    assert k(_dispatch(tool_use_id="toolu_1")) == ("toolu_1", "tool_use_id")


def test_cap_refusal_writes_refuse_and_runs_no_reader(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls)
    for payload in (_with_cwd(root, tool_use_id="toolu_cap_b"), _critic_payload(root, "toolu_cap_c", _manifest())):  # a critic that owns paths counts as a writer
        payload["session_id"] = "sess-1"
        code, out, err = _run_main(monkeypatch, capsys, payload)
        assert code == 2 and "PARALLEL CAP" in err
        assert _carrier(root)["verdict"] == "refuse" and "PARALLEL CAP" in _carrier(root)["reason"]
    assert calls == []  # on "refuse" neither reader runs: no race, no key, no poll
    assert not (root / ".claude").exists() and _registry_rows(root) == 0


def test_completeness_refusal_is_a_refuse_and_runs_no_reader(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls)
    payload = _with_cwd(root, _builder_payload(_manifest(), description="nolabel"), "toolu_nolabel")
    assert _run_main(monkeypatch, capsys, payload)[0] == 2
    assert _carrier(root)["verdict"] == "refuse" and calls == []


def test_allow_runs_snapshot_then_registry_after_the_verdict_is_written(tmp_path, monkeypatch, capsys):
    """The negative control of the refuse tests; the order is today's settings.json order."""
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() - 1)
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls)
    assert _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_ok"))[0] == 0
    assert calls == [("critic_snapshot", "allow"), ("owns_gate", "allow")]


def test_budget_skip_pass_is_an_allow_and_runs_the_readers(tmp_path, monkeypatch, capsys):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls)
    payload = _with_cwd(root, _dispatch("budget-skip: the other writers are idle critics"), "toolu_skip")
    assert _run_main(monkeypatch, capsys, payload)[0] == 0
    assert _carrier(root)["verdict"] == "allow" and [name for name, _ in calls] == ["critic_snapshot", "owns_gate"]


def test_allowed_dispatch_leaves_its_traces_once_through_the_real_readers(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    (root).mkdir()
    (root / "a.txt").write_text("hello", encoding="utf-8")
    assert _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_b1"))[0] == 0
    assert _registry_rows(root) == 1 and not (root / ".claude" / "critic_snapshot.json").exists()
    assert sorted(p.name for p in (root / ".claude" / "dispatch_claims").iterdir()) == ["toolu_b1.owns_gate"]
    assert _run_main(monkeypatch, capsys, _critic_payload(root, "toolu_c1"))[0] == 0
    assert (root / ".claude" / "critic_snapshot.json").exists() and _registry_rows(root) == 1


def test_the_readers_overlap_warning_is_folded_into_the_gates_one_json_object(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    root.mkdir()
    owns_gate._append_registry(root / "logs" / "owns_registry.jsonl", datetime.now(), "other-session", str(root),
                               "sonnet: live", [_OWNED_PATH])
    code, out, err = _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_ov"))
    assert (code, err) == (0, "")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 1, out
    assert "OWNS OVERLAP" in json.loads(lines[0])["hookSpecificOutput"]["additionalContext"]


def test_a_reader_refusal_refuses_the_dispatch_and_the_final_carrier_says_so(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls, codes={"owns_gate": 2})
    code, out, err = _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_r2"))
    assert code == 2 and "owns_gate returned exit 2" in err
    assert _carrier(root)["verdict"] == "refuse"
    _spy_readers(monkeypatch, [], codes={"critic_snapshot": 0, "owns_gate": 0})  # control: both 0 -> allowed
    assert _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_r0"))[0] == 0
    assert _carrier(root)["verdict"] == "allow"


def test_a_reader_that_raises_costs_one_stderr_line_and_the_other_still_runs(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    calls = []
    _spy_readers(monkeypatch, calls, raises={"critic_snapshot"})
    code, out, err = _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_rz"))
    assert code == 0 and err.count("critic_snapshot did not run (RuntimeError)") == 1
    assert [name for name, _ in calls] == ["critic_snapshot", "owns_gate"]


def test_a_payload_without_cwd_runs_no_reader_and_writes_no_carrier(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(owns_gate, "run_after_gate", lambda p: pytest.fail("no cwd: no reader"))
    monkeypatch.setattr(critic_snapshot, "run_after_gate", lambda p: pytest.fail("no cwd: no reader"))
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())  # no cwd, no tool_use_id
    assert code == 0 and err == ""  # (the gate's own "paths unchecked: no cwd" note is on stdout, as before)
    assert not (tmp_path / "logs").exists() and not (tmp_path / ".claude").exists()


def test_unwritable_carrier_is_one_stderr_line_no_leftover_and_the_readers_still_run(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"
    (root / "logs" / "dispatch_verdict.json").mkdir(parents=True)  # os.replace onto a directory fails
    code, out, err = _run_main(monkeypatch, capsys, _with_cwd(root, tool_use_id="toolu_uw"))
    assert code == 0 and err.count("verdict carrier logs/dispatch_verdict.json not written") == 1
    assert _registry_rows(root) == 1  # the reader ran
    assert [p.name for p in (root / "logs").glob("*.tmp")] == []  # the atomic writer removed its temp file


def test_the_carrier_is_written_with_the_repositorys_atomic_writer(tmp_path, monkeypatch):
    import dod_track

    seen = []
    monkeypatch.setattr(dod_track, "_atomic_write_text", lambda path, text: seen.append((path, json.loads(text))))
    payload = _with_cwd(tmp_path, tool_use_id="toolu_aw")
    dispatch_gate.write_verdict(payload, "refuse", "r" * 500)
    (path, record), = seen
    assert path == tmp_path / "logs" / "dispatch_verdict.json"
    assert record["verdict"] == "refuse" and len(record["reason"]) == dispatch_gate.VERDICT_REASON_CHARS


def test_claim_trace_first_asker_wins_per_reader_and_per_tool_use_id(tmp_path):
    p = {"tool_use_id": "toolu_c", "cwd": str(tmp_path)}
    assert dispatch_gate.claim_trace(p, "owns_gate") is True
    assert dispatch_gate.claim_trace(p, "owns_gate") is False  # the second run for the same id stays silent
    assert dispatch_gate.claim_trace(p, "critic_snapshot") is True  # the other reader is its own claim
    assert dispatch_gate.claim_trace({"tool_use_id": "toolu_d", "cwd": str(tmp_path)}, "owns_gate") is True
    assert sorted(m.name for m in (tmp_path / ".claude" / "dispatch_claims").iterdir()) == [
        "toolu_c.critic_snapshot", "toolu_c.owns_gate", "toolu_d.owns_gate"]


def test_claim_trace_without_a_usable_key_never_withholds_a_trace(tmp_path):
    for payload in ({"cwd": str(tmp_path)}, {"tool_use_id": "", "cwd": str(tmp_path)},
                    {"tool_use_id": "toolu_x"}, {"tool_use_id": 5, "cwd": str(tmp_path)},
                    {"tool_use_id": "../escape", "cwd": str(tmp_path)}, {"tool_use_id": "a/b", "cwd": str(tmp_path)},
                    {"tool_use_id": "x" * 129, "cwd": str(tmp_path)}, "not a dict", None):
        assert dispatch_gate.claim_trace(payload, "owns_gate") is True
        assert dispatch_gate.claim_trace(payload, "owns_gate") is True, payload  # twice: never zero times
    assert not (tmp_path / ".claude").exists() and not (tmp_path.parent / "escape.owns_gate").exists()
    (tmp_path / ".claude").write_text("a file where the folder belongs", encoding="utf-8")
    assert dispatch_gate.claim_trace({"tool_use_id": "toolu_io", "cwd": str(tmp_path)}, "owns_gate") is True


def test_claim_trace_prunes_markers_older_than_an_hour(tmp_path):
    folder = tmp_path / ".claude" / "dispatch_claims"
    assert dispatch_gate.claim_trace({"tool_use_id": "toolu_old", "cwd": str(tmp_path)}, "owns_gate")
    old, now = folder / "toolu_old.owns_gate", time.time()
    os.utime(old, (now - dispatch_gate.CLAIM_MAX_AGE_SECONDS - 5, now - dispatch_gate.CLAIM_MAX_AGE_SECONDS - 5))
    assert dispatch_gate.claim_trace({"tool_use_id": "toolu_new", "cwd": str(tmp_path)}, "owns_gate")
    assert [m.name for m in folder.iterdir()] == ["toolu_new.owns_gate"]


def test_a_gate_that_dies_after_allow_leaves_no_claim_so_the_standalone_readers_still_write(tmp_path):
    """The carrier says allow but the readers never ran in the gate: no marker exists, so each standalone hook
    (today's settings.json) does its work."""
    payload = _with_cwd(tmp_path, tool_use_id="toolu_die")
    dispatch_gate.write_verdict(payload, "allow")
    assert not (tmp_path / ".claude").exists()
    assert dispatch_gate.claim_trace(payload, "owns_gate") and dispatch_gate.claim_trace(payload, "critic_snapshot")


# --- the concurrent-start tests (t-792 B3): REAL scripts, started together, as the runtime does -----------


def _race_sandbox(tmp_path, n_workers):
    """A root with `n_workers` live builder transcripts of session sid1 under a sandbox HOME, so the REAL
    parallel cap refuses the (cap+1)-th writer when n_workers == PARALLEL_CAP."""
    root = Path(tempfile.mkdtemp(prefix="race-", dir=str(tmp_path)))
    folder = root / "home" / ".claude" / "projects" / "proj" / "sid1" / "subagents"
    folder.mkdir(parents=True)
    for i in range(n_workers):
        (folder / ("agent-a%d.jsonl" % i)).write_text(
            json.dumps({"type": "user", "message": {"role": "user", "content": "owns: x"}}) + "\n", encoding="utf-8")
        (folder / ("agent-a%d.meta.json" % i)).write_text(json.dumps({"agentType": "builder"}), encoding="utf-8")
    (root / "logs").mkdir()
    (root / "a.txt").write_text("hello", encoding="utf-8")
    env = dict(os.environ, HOME=str(root / "home"), USERPROFILE=str(root / "home"))
    return root, env


def _race_payload(root, kind, tool_use_id):
    handoff = "report" if kind != "critic" else str(root / "docs" / "tasks" / "specs" / "reviews" / "t-1.md")  # F6-37
    prompt = "given: none\nowns: %s (new)\nnon-goals: none\nhandoff: %s\nedges: none\nDoD: `python -m pytest x -q`\nsiblings: none -- a test fixture\nWrite." % (
        root / "x.py", handoff)
    payload = {"tool_name": "Agent", "cwd": str(root), "session_id": "sid1",
               "transcript_path": str(root / "home" / "x.jsonl"),
               "tool_input": {"subagent_type": kind, "description": "sonnet: probe", "prompt": prompt}}
    if tool_use_id:
        payload["tool_use_id"] = tool_use_id
    return payload


def _race_trial(tmp_path, trial, scripts, kind, n_workers, with_id=True):
    """Start every script in `scripts` TOGETHER (all processes alive before any gets its stdin), then feed
    the same payload to all, wait. Returns (gate returncode or None, registry rows, snapshot written)."""
    root, env = _race_sandbox(tmp_path, n_workers)
    raw = json.dumps(_race_payload(root, kind, "toolu_race_%d" % trial if with_id else None)).encode("utf-8")
    procs = [subprocess.Popen([sys.executable, str(_TOOLS / script)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, cwd=str(root), env=env) for script in scripts]
    for proc in procs:
        proc.stdin.write(raw)
        proc.stdin.close()
    codes = {}
    for script, proc in zip(scripts, procs):
        proc.stdout.read(), proc.stderr.read()
        codes[script] = proc.wait()
    return codes.get("dispatch_gate.py"), _registry_rows(root), (root / ".claude" / "critic_snapshot.json").exists()


def _race(tmp_path, scripts, kind, n_workers, trials=10, with_id=True):
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(lambda t: _race_trial(tmp_path, t, scripts, kind, n_workers, with_id), range(trials)))


@pytest.mark.parametrize("kind", ["builder", "critic"])
def test_race_one_process_cap_refusal_leaves_no_trace_in_0_of_10(tmp_path, kind):
    """The arrangement of settings.json after the merge: the gate alone on the matcher. The cap of live writers ->
    the real cap refuses; 0 of 10 dispatches leave a registry row or a snapshot."""
    results = _race(tmp_path, ["dispatch_gate.py"], kind, n_workers=_cap())
    assert [r[0] for r in results] == [2] * 10  # the cap really refused every one (the control of the measure)
    assert sum(r[1] for r in results) == 0 and sum(r[2] for r in results) == 0, results


@pytest.mark.parametrize("kind", ["builder", "critic"])
def test_race_the_old_arrangement_started_together_leaves_false_traces(tmp_path, kind):
    """The CONTROL that proves the measure sees a false trace: the three hooks as separate processes, started
    together (today's settings.json) -- the standalone readers cannot know of the cap, so every refused
    dispatch still gets its trace. This is the arrangement the one-process shape removes."""
    results = _race(tmp_path, ["dispatch_gate.py", "critic_snapshot.py", "owns_gate.py"], kind, n_workers=_cap(), trials=5)
    assert [r[0] for r in results] == [2] * 5
    false_traces = sum(1 for r in results if r[1] or r[2])
    assert false_traces == 5, results


def test_race_allowed_dispatch_writes_each_trace_exactly_once_in_both_worlds(tmp_path):
    """cap-1 live writers -> allowed. One process (after the merge): one registry row. All three started together
    (settings.json today, the claim markers): still ONE row, never two, never zero."""
    one = _race(tmp_path, ["dispatch_gate.py"], "builder", n_workers=_cap() - 1, trials=5)
    assert [(r[0], r[1]) for r in one] == [(0, 1)] * 5
    both = _race(tmp_path, ["dispatch_gate.py", "critic_snapshot.py", "owns_gate.py"], "builder", n_workers=_cap() - 1, trials=5)
    assert [(r[0], r[1]) for r in both] == [(0, 1)] * 5
    critic = _race(tmp_path, ["dispatch_gate.py", "critic_snapshot.py", "owns_gate.py"], "critic", n_workers=_cap() - 1, trials=5)
    assert all(r[0] == 0 and r[2] for r in critic), critic  # the snapshot exists in every trial


def test_race_without_a_tool_use_id_a_trace_is_never_lost(tmp_path):
    """No id in the payload (the live field is not yet observed): nothing to key a claim on, so while both
    worlds coexist the trace may be written twice, never zero times; the gate alone writes it once."""
    both = _race(tmp_path, ["dispatch_gate.py", "owns_gate.py"], "builder", n_workers=_cap() - 1, trials=5, with_id=False)
    assert all(r[0] == 0 and r[1] >= 1 for r in both), both
    one = _race(tmp_path, ["dispatch_gate.py"], "builder", n_workers=_cap() - 1, trials=5, with_id=False)
    assert [r[1] for r in one] == [1] * 5


# --- t-844 F6-9: a transcripts that is absent or BROKEN is said loudly, and the cap still counts ------------

_BROKEN_TRANSCRIPTS = [("def broken(:\n", "SyntaxError"), ("raise RuntimeError('boom')\n", "RuntimeError")]
_SHADOW_RUNNER = ("import runpy, sys; sys.path.insert(0, sys.argv[1]); "
                  "runpy.run_path(sys.argv[2], run_name='__main__')")


def _gate_run(tmp_path, payload, source=None, style="sibling", cwd=None, env=None):
    """The REAL dispatch_gate.py as a subprocess. `source` (a transcripts.py) is made FIRST on the path: style
    "sibling" through sys.path[0] (the sibling-module fallback finds it), style "package" through
    PYTHONPATH/<pkg>/tools/transcripts.py (`from tools import transcripts` finds it). None = the healthy gate."""
    run_env = {**os.environ, **(env or {}), "PYTHONPATH": ""}
    argv = [sys.executable, str(SCRIPT)]
    if source is not None and style == "sibling":
        (tmp_path / "shadow").mkdir(exist_ok=True)
        (tmp_path / "shadow" / "transcripts.py").write_text(source, encoding="utf-8")
        argv = [sys.executable, "-c", _SHADOW_RUNNER, str(tmp_path / "shadow"), str(SCRIPT)]
    elif source is not None:
        (tmp_path / "pkg" / "tools").mkdir(parents=True, exist_ok=True)
        (tmp_path / "pkg" / "tools" / "transcripts.py").write_text(source, encoding="utf-8")
        run_env["PYTHONPATH"] = str(tmp_path / "pkg")
    return subprocess.run(argv, input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8",
                          cwd=str(cwd or tmp_path), env=run_env)


def _one_import_line(r, exc_name):
    lines = r.stderr.splitlines()
    assert len(lines) == 1 and "Traceback" not in r.stderr and len(lines[0]) <= 200, r.stderr
    assert "dispatch_gate: transcripts did not import (%s" % exc_name in lines[0]


@pytest.mark.parametrize("style", ["sibling", "package"])
@pytest.mark.parametrize("source, exc_name", _BROKEN_TRANSCRIPTS)
def test_a_broken_transcripts_gives_one_stderr_line_and_the_hook_lives(tmp_path, source, exc_name, style):
    r = _gate_run(tmp_path, {"tool_name": "Read", "tool_input": {}}, source, style)
    assert r.returncode == 0 and r.stdout == ""
    _one_import_line(r, exc_name)


def test_a_healthy_transcripts_leaves_stderr_empty(tmp_path):
    """The NEGATIVE control of the two tests around it: same payload, the real module, nothing on stderr."""
    r = _gate_run(tmp_path, {"tool_name": "Read", "tool_input": {}})
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_a_module_missing_inside_transcripts_is_loud(tmp_path):
    """A ModuleNotFoundError of ANOTHER module raised while importing transcripts is a broken module: loud."""
    r = _gate_run(tmp_path, {"tool_name": "Read", "tool_input": {}}, "import no_such_dependency_of_transcripts\n")
    assert r.returncode == 0 and r.stdout == ""
    _one_import_line(r, "ModuleNotFoundError")


def test_a_missing_transcripts_is_silent(tmp_path):
    """transcripts ITSELF absent (a COPY of the gate with no transcripts.py beside it, no `tools` package) stays
    silent on stderr as before; the cap's own sentence is what says the module was not there."""
    folder = tmp_path / "alone"
    folder.mkdir()
    for name in ("dispatch_gate.py", "md_regions.py"):
        (folder / name).write_bytes((_TOOLS / name).read_bytes())
    r = subprocess.run([sys.executable, str(folder / "dispatch_gate.py")], input=json.dumps(
        {"tool_name": "Read", "tool_input": {}}), capture_output=True, text=True, encoding="utf-8", cwd=str(folder),
        env={**os.environ, "PYTHONPATH": ""})
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_a_long_multiline_import_error_is_still_one_short_line(tmp_path):
    r = _gate_run(tmp_path, {"tool_name": "Read", "tool_input": {}},
                  "raise RuntimeError('x' * 500 + '\\nsecond line\\nthird')\n")
    assert r.returncode == 0
    _one_import_line(r, "RuntimeError")


@pytest.mark.parametrize("source, exc_name", _BROKEN_TRANSCRIPTS)
def test_with_a_broken_transcripts_the_cap_still_counts_every_fresh_file_live(tmp_path, source, exc_name):
    """The fallback path RUNS on a broken module (not only a missing one): the cap of live writers -> the
    (cap+1)-th is refused with the PARALLEL CAP text and the TRANSCRIPTS_MISSING sentence; cap-1 -> allowed,
    and the note carries the sentence. The import line comes first on stderr either way."""
    root, env = _race_sandbox(tmp_path, _cap())
    refused = _gate_run(tmp_path, _race_payload(root, "builder", "toolu_a"), source, cwd=root, env=env)
    assert refused.returncode == 2
    assert refused.stderr.startswith("dispatch_gate: transcripts did not import (%s" % exc_name)
    assert "PARALLEL CAP: %d writing-worker transcripts" % _cap() in refused.stderr
    assert dispatch_gate.TRANSCRIPTS_MISSING in refused.stderr
    root3, env3 = _race_sandbox(tmp_path, _cap() - 1)
    allowed = _gate_run(tmp_path, _race_payload(root3, "builder", "toolu_b"), source, cwd=root3, env=env3)
    assert allowed.returncode == 0
    _one_import_line(allowed, exc_name)
    assert dispatch_gate.TRANSCRIPTS_MISSING in allowed.stdout


def test_package_style_missing_still_tries_the_sibling(tmp_path):
    """The inner invariant: no `tools` package on the path (ImportError) -> the sibling transcripts.py of the
    gate is the one used; the healthy cap run refuses the (cap+1)-th writer with NO TRANSCRIPTS_MISSING sentence."""
    root, env = _race_sandbox(tmp_path, _cap())
    r = _gate_run(tmp_path, _race_payload(root, "builder", "toolu_c"), cwd=root, env=env)
    assert r.returncode == 2 and "PARALLEL CAP: %d writing-worker transcripts" % _cap() in r.stderr
    assert dispatch_gate.TRANSCRIPTS_MISSING not in r.stderr and "did not import" not in r.stderr


def test_t857_a_writer_whose_handback_is_followed_by_short_lines_is_not_counted_live(tmp_path, monkeypatch, capsys):
    """F6-19, the live case of t-744: a 74 KB SubagentHandback line, then the short result lines the harness
    writes after it. The cap of fresh writers, one of them in that shape -> cap-1 live, the dispatch passes (before
    the fix is_finished said no, the finished writer held a cap slot)."""
    folder = _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    assert _run_main(monkeypatch, capsys, _dispatch())[0] == 2  # the cap live: blocked (control)
    hand_back = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": "SubagentHandback",
                                                               "input": {"message": "w" * 74_000}}]}}
    result = json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}})
    (folder / "agent-fresh0.jsonl").write_text(json.dumps(hand_back) + "\n" + (result + "\n") * 5, encoding="utf-8")
    live = dispatch_gate.recent_subagent_files({"session_id": "sess-1"})
    assert sorted(f.name for f in live) == sorted("agent-fresh%d.jsonl" % i for i in range(1, _cap()))
    code, out, err = _run_main(monkeypatch, capsys, _dispatch())
    assert (code, err) == (0, "")
