"""Unit/smoke tests for tools/dod_gate.py -- covers the base
invariant (edit vs. green run ordering), the per-agent filter (a
worker's own records only, main-thread and other workers' edits are
invisible), the doc-only exemption (.md/.json/.jsonl), and the
2-consecutive-blocks safety valve.

Run from the repo root: python -m pytest tools/test_dod_gate.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dod_gate  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "dod_gate.py"


def _run_hook(payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _stop_payload(cwd: str, session_id: str = "sess-x", agent_id: str = "agent-1") -> dict:
    return {
        "session_id": session_id,
        "cwd": cwd,
        "hook_event_name": "SubagentStop",
        "agent_type": "builder",
        "agent_id": agent_id,
        "stop_hook_active": False,
    }


# ---------------------------------------------------------------------
# evaluate() -- pure logic. Records carry agent_id="agent-1"; calls
# pass agent_id="agent-1" explicitly to match the per-agent filter.
# ---------------------------------------------------------------------


def test_evaluate_no_edits_no_violation():
    violation, reason = dod_gate.evaluate({"edits": [], "runs": []}, agent_id="agent-1")
    assert violation is False
    assert reason == "no-edits"


def test_evaluate_edit_without_any_run_is_violation():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:00.000000", "agent_id": "agent-1"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_edit_with_only_red_run_is_violation():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:00.000000", "agent_id": "agent-1"}],
        "runs": [
            {"ts": "2026-07-16T10:00:01.000000", "outcome": "red", "agent_id": "agent-1"}
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_green_run_before_edit_is_violation():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:05.000000", "agent_id": "agent-1"}],
        "runs": [
            {"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"}
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "green-before-last-edit"


def test_evaluate_green_run_after_edit_is_not_violation():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:00.000000", "agent_id": "agent-1"}],
        "runs": [
            {"ts": "2026-07-16T10:00:05.000000", "outcome": "green", "agent_id": "agent-1"}
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "green-after-last-edit"


# ---------------------------------------------------------------------
# Per-agent filter -- pure logic.
# ---------------------------------------------------------------------


def test_evaluate_agent_id_filters_out_other_agents_edits():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-y"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-x")
    assert violation is False
    assert reason == "no-edits"


def test_evaluate_agent_id_filters_out_main_edits():
    # The core case: main-thread edits (agent_id=None) are invisible
    # to a SubagentStop evaluation for any agent_id.
    track = {
        "edits": [{"ts": "t1", "agent_id": None}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "no-edits"


def test_evaluate_agent_id_own_edit_visible_among_others():
    track = {
        "edits": [
            {"ts": "t0", "agent_id": None},
            {"ts": "t1", "agent_id": "agent-y"},
            {"ts": "t2", "agent_id": "agent-x"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-x")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_agent_id_cross_agent_green_run_not_counted():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-x"}],
        "runs": [{"ts": "t2", "outcome": "green", "agent_id": "agent-y"}],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-x")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_agent_id_own_green_run_after_own_edit_passes():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-x"}],
        "runs": [{"ts": "t2", "outcome": "green", "agent_id": "agent-x"}],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-x")
    assert violation is False
    assert reason == "green-after-last-edit"


def test_evaluate_fallback_no_agent_id_excludes_main_includes_subagent():
    track = {
        "edits": [
            {"ts": "t1", "agent_id": None},
            {"ts": "t2", "agent_id": "agent-1"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track)
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_fallback_no_agent_id_only_main_edits_is_no_edits():
    track = {"edits": [{"ts": "t1", "agent_id": None}], "runs": []}
    violation, reason = dod_gate.evaluate(track)
    assert violation is False
    assert reason == "no-edits"


def test_evaluate_fallback_no_agent_id_missing_key_treated_as_main():
    track = {"edits": [{"ts": "t1"}], "runs": []}
    violation, reason = dod_gate.evaluate(track)
    assert violation is False
    assert reason == "no-edits"


# ---------------------------------------------------------------------
# Doc-only rule (.md/.json/.jsonl), on the agent_id-filtered subset.
# ---------------------------------------------------------------------


def test_evaluate_doc_only_md_edits_no_violation():
    track = {
        "edits": [{"ts": "t1", "file_path": "docs/NOTES.md", "agent_id": "agent-1"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_doc_only_json_edits_no_violation():
    track = {
        "edits": [
            {"ts": "t1", "file_path": ".claude/settings.json", "agent_id": "agent-1"}
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_doc_only_jsonl_routing_log_edit_no_violation():
    track = {
        "edits": [
            {"ts": "t1", "file_path": "logs/routing-log.jsonl", "agent_id": "agent-1"}
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_doc_only_extension_case_insensitive():
    track = {
        "edits": [{"ts": "t1", "file_path": "docs/NOTES.MD", "agent_id": "agent-1"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_doc_only_multiple_edits_all_qualifying():
    track = {
        "edits": [
            {"ts": "t1", "file_path": "docs/NOTES.md", "agent_id": "agent-1"},
            {"ts": "t2", "file_path": "logs/routing-log.jsonl", "agent_id": "agent-1"},
            {"ts": "t3", "file_path": ".claude/settings.json", "agent_id": "agent-1"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_doc_only_subset_for_agent_ignores_other_agents_non_doc_edit():
    track = {
        "edits": [
            {"ts": "t1", "file_path": "docs/NOTES.md", "agent_id": "agent-1"},
            {"ts": "t2", "file_path": "tools/x.py", "agent_id": "agent-2"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_unknown_file_path_none_is_fail_closed():
    track = {
        "edits": [{"ts": "t1", "file_path": None, "agent_id": "agent-1"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_missing_file_path_key_is_fail_closed():
    track = {"edits": [{"ts": "t1", "agent_id": "agent-1"}], "runs": []}
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_mixed_md_and_py_edits_invariant_applies():
    track = {
        "edits": [
            {"ts": "t1", "file_path": "README.md", "agent_id": "agent-1"},
            {"ts": "t2", "file_path": "tools/x.py", "agent_id": "agent-1"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_mixed_extensions_with_green_run_after_last_edit_not_violation():
    track = {
        "edits": [
            {"ts": "2026-07-16T10:00:00.000000", "file_path": "README.md", "agent_id": "agent-1"},
            {"ts": "2026-07-16T10:00:01.000000", "file_path": "tools/x.py", "agent_id": "agent-1"},
        ],
        "runs": [
            {"ts": "2026-07-16T10:00:05.000000", "outcome": "green", "agent_id": "agent-1"}
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "green-after-last-edit"


# ---------------------------------------------------------------------
# Doc-only "whole-or-nothing" over edits_after_green of THIS agent, not
# its whole history (ported fix -- same class as main_gate.py).
# ---------------------------------------------------------------------


def test_evaluate_doc_only_exempt_after_green_even_with_earlier_code_edit():
    track = {
        "edits": [
            {"ts": "2026-07-16T09:00:00.000000", "agent_id": "agent-1", "file_path": "tools/x.py"},
            {"ts": "2026-07-16T10:00:10.000000", "agent_id": "agent-1", "file_path": "README.md"},
        ],
        "runs": [
            {"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"},
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_code_edit_after_green_still_blocks():
    track = {
        "edits": [
            {"ts": "2026-07-16T09:00:00.000000", "agent_id": "agent-1", "file_path": "README.md"},
            {"ts": "2026-07-16T10:00:10.000000", "agent_id": "agent-1", "file_path": "tools/x.py"},
        ],
        "runs": [
            {"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"},
        ],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "green-before-last-edit"


def test_evaluate_mixed_edits_after_green_blocks():
    track = {
        "edits": [
            {"ts": "2026-07-16T10:00:10.000000", "agent_id": "agent-1", "file_path": "README.md"},
            {"ts": "2026-07-16T10:00:11.000000", "agent_id": "agent-1", "file_path": "tools/x.py"},
        ],
        "runs": [{"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"}],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "green-before-last-edit"


def test_evaluate_edit_exactly_at_green_ts_boundary_not_after_green():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:00.000000", "agent_id": "agent-1", "file_path": "tools/x.py"}],
        "runs": [{"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"}],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "green-after-last-edit"


def test_evaluate_no_green_run_at_all_doc_only_over_full_history_unchanged():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1", "file_path": "README.md"}],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


# ---------------------------------------------------------------------
# Rule #1: fixed -- known code-less dotfiles without a suffix
# (.gitignore/.gitattributes/.editorconfig) count as doc-only.
# ---------------------------------------------------------------------


def test_evaluate_gitignore_edit_no_violation():
    track = {"edits": [{"ts": "t1", "file_path": ".gitignore", "agent_id": "agent-1"}], "runs": []}
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_gitignore_uppercase_name_still_doc_only():
    track = {"edits": [{"ts": "t1", "file_path": ".GITIGNORE", "agent_id": "agent-1"}], "runs": []}
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_gitattributes_and_editorconfig_doc_only():
    for name in (".gitattributes", ".editorconfig"):
        track = {"edits": [{"ts": "t1", "file_path": name, "agent_id": "agent-1"}], "runs": []}
        violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
        assert violation is False, name
        assert reason == "doc-only-edits-exempt", name


def test_evaluate_gitignore_edit_after_green_does_not_extinguish_exemption():
    track = {
        "edits": [{"ts": "2026-07-16T10:00:10.000000", "file_path": ".gitignore", "agent_id": "agent-1"}],
        "runs": [{"ts": "2026-07-16T10:00:00.000000", "outcome": "green", "agent_id": "agent-1"}],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is False
    assert reason == "doc-only-edits-exempt"


def test_evaluate_dotfile_not_in_known_list_still_fail_closed():
    track = {"edits": [{"ts": "t1", "file_path": ".env", "agent_id": "agent-1"}], "runs": []}
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


def test_evaluate_mixed_gitignore_and_code_invariant_applies():
    track = {
        "edits": [
            {"ts": "t1", "file_path": ".gitignore", "agent_id": "agent-1"},
            {"ts": "t2", "file_path": "tools/x.py", "agent_id": "agent-1"},
        ],
        "runs": [],
    }
    violation, reason = dod_gate.evaluate(track, agent_id="agent-1")
    assert violation is True
    assert reason == "no-green-run"


# ---------------------------------------------------------------------
# decide() -- gate_state / 2-consecutive-blocks safety valve.
# ---------------------------------------------------------------------


def test_decide_blocks_on_first_violation():
    track = {"edits": [{"ts": "t1", "agent_id": "agent-1"}], "runs": []}
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 2
    assert "blocked" in message
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 1
    entry = updated["gate_log"][-1]
    assert entry["action"] == "blocked"
    assert "ts" in entry and entry["ts"]
    assert entry["agent_id"] == "agent-1"


def test_decide_blocks_again_on_second_consecutive_violation():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 1}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 2
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 2


def test_decide_skips_on_third_consecutive_violation_safety_valve():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 2}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0
    assert "safety valve" in message
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 0
    entry = updated["gate_log"][-1]
    assert entry["action"] == "skipped_after_2_blocks"
    assert "ts" in entry and entry["ts"]
    assert entry["agent_id"] == "agent-1"


# ---------------------------------------------------------------------
# F2 (release-gate v0.8.1, ported from tools/dod_gate.py's own
# attempt-2 fix): the safety valve APPENDS a PERSISTENT fact into
# gate_state.per_agent[<agent>]["unsafe_completions"] (a list, not a
# single overwritable key -- same dict "consecutive_blocks" already
# lives in). This is the fact tools/session_context.py's GATE
# BREAK-GLASS surfacing reads on the next SessionStart.
# ---------------------------------------------------------------------


def test_decide_records_unsafe_completion_on_safety_valve():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 2}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0
    facts = updated["gate_state"]["per_agent"]["agent-1"]["unsafe_completions"]
    assert len(facts) == 1
    assert facts[0]["reason"] == "no-green-run"
    assert facts[0]["ts"]
    assert facts[0]["agent_id"] == "agent-1"


def test_decide_unsafe_completion_fallback_agent_id_none_records_none():
    # Defensive fallback branch (agent_id=None) -- the fact's own "agent_id"
    # value is honestly None too, not invented.
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"__none__": {"consecutive_blocks": 2}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id=None)
    assert exit_code == 0
    facts = updated["gate_state"]["per_agent"]["__none__"]["unsafe_completions"]
    assert facts[0]["agent_id"] is None


def test_decide_unsafe_completion_not_erased_by_later_green_run():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 2}}},
    }
    _, _, after_valve = dod_gate.decide(track, agent_id="agent-1")
    assert len(after_valve["gate_state"]["per_agent"]["agent-1"]["unsafe_completions"]) == 1

    green_track = {
        "edits": [{"ts": "2026-07-16T10:00:00.000000", "agent_id": "agent-1"}],
        "runs": [{"ts": "2026-07-16T10:00:05.000000", "outcome": "green", "agent_id": "agent-1"}],
        "gate_state": after_valve["gate_state"],
    }
    exit_code, message, after_green = dod_gate.decide(green_track, agent_id="agent-1")
    assert exit_code == 0
    assert message == ""
    facts = after_green["gate_state"]["per_agent"]["agent-1"]["unsafe_completions"]
    assert len(facts) == 1
    assert facts[0]["reason"] == "no-green-run"


def test_decide_unsafe_completion_isolated_per_agent():
    # agent-x's unsafe_completions must not leak into agent-y's own
    # per_agent entry when agent-y trips ITS OWN valve independently.
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-x"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-x": {"consecutive_blocks": 2}}},
    }
    _, _, after_x = dod_gate.decide(track, agent_id="agent-x")

    track_y = {
        "edits": [{"ts": "t1", "agent_id": "agent-y"}],
        "runs": [],
        "gate_state": {
            "per_agent": {
                "agent-x": after_x["gate_state"]["per_agent"]["agent-x"],
                "agent-y": {"consecutive_blocks": 2},
            }
        },
    }
    _, _, after_y = dod_gate.decide(track_y, agent_id="agent-y")
    y_facts = after_y["gate_state"]["per_agent"]["agent-y"]["unsafe_completions"]
    x_facts = after_y["gate_state"]["per_agent"]["agent-x"]["unsafe_completions"]
    assert y_facts[0]["agent_id"] == "agent-y"
    assert x_facts[0]["agent_id"] == "agent-x"


def test_decide_unsafe_completion_collision_two_valve_trips_both_kept():
    # Two consecutive valve trips of the SAME agent in the same session
    # must leave BOTH facts in the list (append, never overwrite).
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 2}}},
    }
    _, _, after_first = dod_gate.decide(track, agent_id="agent-1")
    assert len(after_first["gate_state"]["per_agent"]["agent-1"]["unsafe_completions"]) == 1

    track2 = {**track, "gate_state": after_first["gate_state"]}
    _, _, after_block1 = dod_gate.decide(track2, agent_id="agent-1")
    assert after_block1["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 1
    track3 = {**track, "gate_state": after_block1["gate_state"]}
    _, _, after_block2 = dod_gate.decide(track3, agent_id="agent-1")
    assert after_block2["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 2

    track4 = {**track, "gate_state": after_block2["gate_state"]}
    _, _, after_second = dod_gate.decide(track4, agent_id="agent-1")
    facts = after_second["gate_state"]["per_agent"]["agent-1"]["unsafe_completions"]
    assert len(facts) == 2


def test_decide_resets_counter_on_success():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-1"}],
        "runs": [{"ts": "t2", "outcome": "green", "agent_id": "agent-1"}],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 1}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0
    assert message == ""
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 0


def test_decide_no_edits_passes_without_touching_counter():
    track = {"edits": [], "runs": [], "gate_state": {"consecutive_blocks": 0, "per_agent": {}}}
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0
    assert message == ""
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 0
    assert "gate_log" not in updated


def test_decide_doc_only_edits_pass_without_touching_counter():
    track = {
        "edits": [
            {"ts": "t1", "file_path": "logs/routing-log.jsonl", "agent_id": "agent-1"}
        ],
        "runs": [],
        "gate_state": {"per_agent": {"agent-1": {"consecutive_blocks": 1}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0
    assert message == ""
    assert updated["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 0


def test_decide_main_only_edits_pass_ignoring_other_agent_id():
    track = {"edits": [{"ts": "t1", "agent_id": None}], "runs": []}
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-1")
    assert exit_code == 0


# ---------------------------------------------------------------------
# consecutive_blocks is isolated PER-AGENT (not session-global).
# ---------------------------------------------------------------------


def test_decide_consecutive_blocks_isolated_per_agent():
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-x"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-x": {"consecutive_blocks": 2}}},
    }
    exit_code_x, message_x, updated = dod_gate.decide(track, agent_id="agent-x")
    assert exit_code_x == 0
    assert "safety valve" in message_x

    # agent-y, meeting a block for the FIRST time in the same track --
    # blocked NORMALLY (a session-global counter would let it skip too).
    track_y = {
        "edits": [{"ts": "t1", "agent_id": "agent-y"}],
        "runs": [],
        "gate_state": updated["gate_state"],
    }
    exit_code_y, message_y, updated_y = dod_gate.decide(track_y, agent_id="agent-y")
    assert exit_code_y == 2
    assert updated_y["gate_state"]["per_agent"]["agent-y"]["consecutive_blocks"] == 1
    assert updated_y["gate_state"]["per_agent"]["agent-x"]["consecutive_blocks"] == 0


def test_decide_agent_x_exhausted_valve_does_not_skip_agent_y_first_block():
    # Boundary: agent-x has ALREADY exhausted the valve (per_agent
    # counter==2, not yet reset), agent-y sees a block for the first
    # time in the same decide() call -- must block (not 0).
    track = {
        "edits": [{"ts": "t1", "agent_id": "agent-y"}],
        "runs": [],
        "gate_state": {"per_agent": {"agent-x": {"consecutive_blocks": 2}}},
    }
    exit_code, message, updated = dod_gate.decide(track, agent_id="agent-y")
    assert exit_code == 2
    assert updated["gate_state"]["per_agent"]["agent-y"]["consecutive_blocks"] == 1
    assert updated["gate_state"]["per_agent"]["agent-x"]["consecutive_blocks"] == 2  # untouched


def test_decide_fallback_no_agent_id_uses_dedicated_fallback_key():
    track = {"edits": [{"ts": "t1", "agent_id": "agent-1"}], "runs": []}
    exit_code, message, updated = dod_gate.decide(track, agent_id=None)
    assert exit_code == 2
    assert updated["gate_state"]["per_agent"]["__none__"]["consecutive_blocks"] == 1


def test_load_track_backward_compat_old_flat_gate_state(tmp_path):
    # Old track with a FLAT gate_state (pre-per-agent) reads without
    # raising -- "per_agent" is added via setdefault, the old field is
    # not removed.
    path = tmp_path / "track.json"
    path.write_text(json.dumps({"edits": [], "runs": [], "gate_state": {"consecutive_blocks": 3}}))
    track = dod_gate._load_track(path)
    assert track["gate_state"]["consecutive_blocks"] == 3  # old field preserved
    assert track["gate_state"]["per_agent"] == {}


# ---------------------------------------------------------------------
# echo-JSON subprocess smoke tests -- full block -> run -> skip scenario
# plus doc-only and per-agent scenarios.
# ---------------------------------------------------------------------


def _write_track(tmp_path: Path, session_id: str, data: dict) -> Path:
    path = tmp_path / ".claude" / "dod_track" / f"{session_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_echo_json_no_track_file_passes(tmp_path):
    result = _run_hook(_stop_payload(str(tmp_path), "sess-none"), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert not (tmp_path / ".claude" / "dod_track" / "sess-none.json").exists()


def test_echo_json_main_edits_do_not_block_clean_subagent(tmp_path):
    session_id = "sess-main-only"
    _write_track(
        tmp_path,
        session_id,
        {"edits": [{"ts": "t1", "tool_name": "Edit", "agent_id": None}], "runs": []},
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_blocks_when_own_edit_without_run(tmp_path):
    session_id = "sess-block"
    _write_track(
        tmp_path,
        session_id,
        {"edits": [{"ts": "t1", "tool_name": "Edit", "agent_id": "agent-1"}], "runs": []},
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 2
    assert "blocked" in result.stderr

    track = json.loads((tmp_path / ".claude" / "dod_track" / f"{session_id}.json").read_text())
    assert track["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 1


def test_echo_json_worker_not_blocked_by_other_workers_unrun_edit(tmp_path):
    session_id = "sess-parallel"
    _write_track(
        tmp_path,
        session_id,
        {"edits": [{"ts": "t1", "tool_name": "Edit", "agent_id": "agent-y"}], "runs": []},
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-x"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_passes_when_own_green_run_after_own_edit(tmp_path):
    session_id = "sess-green"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "2026-07-16T10:00:00.000000", "tool_name": "Edit", "agent_id": "agent-1"}
            ],
            "runs": [
                {
                    "ts": "2026-07-16T10:00:05.000000",
                    "tool_name": "Bash",
                    "command": "python -m pytest tools/ -q",
                    "outcome": "green",
                    "agent_id": "agent-1",
                }
            ],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_blocks_when_green_run_belongs_to_other_agent(tmp_path):
    session_id = "sess-green-other-agent"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "2026-07-16T10:00:00.000000", "tool_name": "Edit", "agent_id": "agent-1"}
            ],
            "runs": [
                {
                    "ts": "2026-07-16T10:00:05.000000",
                    "tool_name": "Bash",
                    "command": "python -m pytest tools/ -q",
                    "outcome": "green",
                    "agent_id": "agent-2",
                }
            ],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 2
    assert "blocked" in result.stderr


def test_echo_json_safety_valve_after_two_consecutive_blocks(tmp_path):
    session_id = "sess-valve"
    _write_track(
        tmp_path,
        session_id,
        {"edits": [{"ts": "t1", "agent_id": "agent-1"}], "runs": []},
    )

    r1 = _run_hook(_stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path)
    assert r1.returncode == 2

    r2 = _run_hook(_stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path)
    assert r2.returncode == 2

    r3 = _run_hook(_stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path)
    assert r3.returncode == 0
    assert "safety valve" in r3.stderr

    track = json.loads((tmp_path / ".claude" / "dod_track" / f"{session_id}.json").read_text())
    assert track["gate_state"]["per_agent"]["agent-1"]["consecutive_blocks"] == 0
    actions = [g["action"] for g in track["gate_log"]]
    assert actions == ["blocked", "blocked", "skipped_after_2_blocks"]

    r4 = _run_hook(_stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path)
    assert r4.returncode == 2


def test_echo_json_agent_y_not_skipped_by_agent_x_exhausted_valve(tmp_path):
    # agent-x has already exhausted the safety valve (2 blocks
    # accumulated), agent-y stops for the FIRST time in the same track
    # -- must block normally, not skip via the other agent's counter.
    session_id = "sess-cross-agent-valve"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "t1", "agent_id": "agent-x"},
                {"ts": "t2", "agent_id": "agent-y"},
            ],
            "runs": [],
            "gate_state": {"per_agent": {"agent-x": {"consecutive_blocks": 2}}},
        },
    )
    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-y"), cwd=tmp_path
    )
    assert result.returncode == 2
    assert "blocked" in result.stderr

    track = json.loads((tmp_path / ".claude" / "dod_track" / f"{session_id}.json").read_text())
    assert track["gate_state"]["per_agent"]["agent-y"]["consecutive_blocks"] == 1
    assert track["gate_state"]["per_agent"]["agent-x"]["consecutive_blocks"] == 2  # untouched


def test_echo_json_doc_only_exempt_after_green_with_earlier_code_edit(tmp_path):
    # subprocess-level: an early code edit by this worker + a green run
    # + a doc-only edit AFTER the green run -- SubagentStop is NOT blocked.
    session_id = "sess-t265-dod-gate"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "2026-07-16T09:00:00.000000", "tool_name": "Edit", "agent_id": "agent-1", "file_path": "tools/x.py"},
                {"ts": "2026-07-16T10:00:10.000000", "tool_name": "Edit", "agent_id": "agent-1", "file_path": "README.md"},
            ],
            "runs": [
                {
                    "ts": "2026-07-16T10:00:00.000000",
                    "tool_name": "Bash",
                    "command": "python -m pytest tools/ -q",
                    "outcome": "green",
                    "agent_id": "agent-1",
                }
            ],
        },
    )
    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_gitignore_edit_after_green_does_not_extinguish_exemption(tmp_path):
    session_id = "sess-gitignore-after-green"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "2026-07-16T10:00:10.000000", "tool_name": "Edit", "file_path": ".gitignore", "agent_id": "agent-1"}
            ],
            "runs": [
                {
                    "ts": "2026-07-16T10:00:00.000000",
                    "tool_name": "Bash",
                    "command": "python -m pytest tools/ -q",
                    "outcome": "green",
                    "agent_id": "agent-1",
                }
            ],
        },
    )
    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_doc_only_md_edit_passes_without_run(tmp_path):
    session_id = "sess-doc-only-md"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {
                    "ts": "t1",
                    "tool_name": "Edit",
                    "file_path": "docs/NOTES.md",
                    "agent_id": "agent-1",
                }
            ],
            "runs": [],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_doc_only_jsonl_routing_log_edit_passes_without_run(tmp_path):
    session_id = "sess-doc-only-jsonl"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {
                    "ts": "t1",
                    "tool_name": "Edit",
                    "file_path": "logs/routing-log.jsonl",
                    "agent_id": "agent-1",
                }
            ],
            "runs": [],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_doc_only_subset_for_agent_ignores_other_agents_non_doc_edit(tmp_path):
    session_id = "sess-doc-only-subset"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {
                    "ts": "t1",
                    "tool_name": "Edit",
                    "file_path": "docs/NOTES.md",
                    "agent_id": "agent-1",
                },
                {
                    "ts": "t2",
                    "tool_name": "Edit",
                    "file_path": "tools/x.py",
                    "agent_id": "agent-2",
                },
            ],
            "runs": [],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_echo_json_unknown_file_path_still_blocks(tmp_path):
    session_id = "sess-unknown-path"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "t1", "tool_name": "Edit", "file_path": None, "agent_id": "agent-1"}
            ],
            "runs": [],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 2
    assert "blocked" in result.stderr


def test_echo_json_mixed_extensions_still_blocks(tmp_path):
    session_id = "sess-mixed"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {
                    "ts": "t1",
                    "tool_name": "Edit",
                    "file_path": "README.md",
                    "agent_id": "agent-1",
                },
                {
                    "ts": "t2",
                    "tool_name": "Edit",
                    "file_path": "tools/x.py",
                    "agent_id": "agent-1",
                },
            ],
            "runs": [],
        },
    )

    result = _run_hook(
        _stop_payload(str(tmp_path), session_id, agent_id="agent-1"), cwd=tmp_path
    )
    assert result.returncode == 2
    assert "blocked" in result.stderr


def test_echo_json_fallback_payload_without_agent_id_excludes_main_includes_subagent(tmp_path):
    session_id = "sess-fallback"
    _write_track(
        tmp_path,
        session_id,
        {
            "edits": [
                {"ts": "t1", "tool_name": "Edit", "agent_id": None},
                {"ts": "t2", "tool_name": "Edit", "agent_id": "agent-1"},
            ],
            "runs": [],
        },
    )
    payload = _stop_payload(str(tmp_path), session_id)
    del payload["agent_id"]

    result = _run_hook(payload, cwd=tmp_path)
    assert result.returncode == 2
    assert "blocked" in result.stderr


def test_echo_json_fallback_payload_without_agent_id_main_only_passes(tmp_path):
    session_id = "sess-fallback-main-only"
    _write_track(
        tmp_path,
        session_id,
        {"edits": [{"ts": "t1", "tool_name": "Edit", "agent_id": None}], "runs": []},
    )
    payload = _stop_payload(str(tmp_path), session_id)
    del payload["agent_id"]

    result = _run_hook(payload, cwd=tmp_path)
    assert result.returncode == 0, result.stderr


# ---------------------------------------------------------------------
# Byte-safe stdin: raw UTF-8 bytes without text=True/encoding on
# subprocess must not crash the hook.
# ---------------------------------------------------------------------


def test_echo_json_raw_utf8_bytes_stdin_no_crash(tmp_path):
    payload = _stop_payload(str(tmp_path), "sess-utf8")
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=raw,
        cwd=str(tmp_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0


def test_echo_json_malformed_json_fails_open():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input="{not valid json",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert result.stderr == ""


# ---------------------------------------------------------------------
# B2: "handoff missing" -- one table (spec fg-context-and-hygiene, B2).
# A worker transcript under tmp_path holds the dispatch; the stop
# payload's transcript_path points at the session file next to it.
# ---------------------------------------------------------------------

HANDOFFS = "docs/tasks/handoffs"


def _dispatch_with(handoff_lines: str) -> str:
    parts = ["Do the work.", "given: docs/x.md", "owns:", "C:/nowhere/x.py", "non-goals: none"]
    if handoff_lines:
        parts.append(handoff_lines)
    parts += ["edges: none -- x", "DoD: `python -m pytest -q`"]
    return "\n".join(parts) + "\n"


def _worker(tmp_path: Path, dispatch: str, agent_id: str = "w1", ts: str | None = None) -> Path:
    main = tmp_path / "proj" / "sess.jsonl"
    sub = tmp_path / "proj" / "sess" / "subagents"
    sub.mkdir(parents=True, exist_ok=True)
    record = {"type": "user", "message": {"role": "user", "content": dispatch}}
    if ts:
        record["timestamp"] = ts
    (sub / ("agent-%s.jsonl" % agent_id)).write_text(json.dumps(record) + "\n", encoding="utf-8")
    return main


def _hp(tmp_path: Path, *parts) -> str:
    return str(tmp_path.joinpath(*parts))


def _edit(path, agent_id="w1"):
    return {"ts": "2026-07-16T10:00:00.000000", "tool_name": "Write", "agent_id": agent_id, "file_path": path}


def _rows():
    one = lambda t: "handoff: %s -- the report" % _hp(t, HANDOFFS, "r.md")
    return [
        # id: dispatch lines, edits, stops, expected exit codes per stop
        ("written-by-this-agent", one, lambda t: [_edit(_hp(t, HANDOFFS, "r.md"))], 1, [0]),
        ("not-written-blocks-once", one, lambda t: [], 1, [2]),
        ("second-stop-after-block-passes", one, lambda t: [], 2, [2, 0]),
        ("no-handoff-line", lambda t: "", lambda t: [], 1, [0]),
        ("path-outside-handoff-dirs", lambda t: "handoff: %s" % _hp(t, "tools", "r.md"), lambda t: [], 1, [0]),
        ("two-candidates",
         lambda t: "handoff:\n%s\n%s" % (_hp(t, HANDOFFS, "a.md"), _hp(t, HANDOFFS, "b.md")), lambda t: [], 1, [0]),
        ("written-by-main-blocks-once", one, lambda t: [_edit(_hp(t, HANDOFFS, "r.md"), agent_id=None)], 1, [2]),
        ("worktree-copy-of-the-path", one,
         lambda t: [_edit(_hp(t, ".claude", "worktrees", "agent-x", HANDOFFS, "r.md"))], 1, [0]),
        ("case-and-slash-direction", one,
         lambda t: [_edit(_hp(t, HANDOFFS, "r.md").replace("\\", "/").swapcase() if os.name == "nt"
                          else _hp(t, HANDOFFS, "r.md").replace("/", "//"))], 1, [0]),
        # the two rows that need another carrier: readers that do not import; the real hook on a track that
        # does not exist (no edits at all)
        ("readers-import-fails", one, lambda t: [], 1, [0]),
        ("no-edit-critic-no-track-file", one, lambda t: [], 2, [2, 0]),
        # B-1: the file exists on disk (a worktree worker wrote the dispatch's main-clone path: no track edit)
        ("file-fresh-not-in-track", one, lambda t: [], 1, [0]),
        ("file-older-than-dispatch", one, lambda t: [], 1, [2]),
        ("file-exists-start-unreadable", one, lambda t: [], 1, [0]),
        # F-4: the handoff block counts toward consecutive_blocks; at 2 the check is skipped (the valve)
        ("valve-counts-the-handoff-block", one, lambda t: [_edit(_hp(t, "src", "x.py"))], 3, [2, 2, 0]),
    ]


# dispatch timestamp (first record of the worker transcript) and whether the handoff file exists, per row
_FILE_ROWS = {
    "file-fresh-not-in-track": ("2000-01-01T00:00:00Z", True),
    "file-older-than-dispatch": ("2999-01-01T00:00:00Z", True),
    "file-exists-start-unreadable": (None, True),
}
_NO_GREEN_ROWS = ("valve-counts-the-handoff-block",)


@pytest.mark.parametrize("row", _rows(), ids=[r[0] for r in _rows()])
def test_handoff_missing_table(tmp_path, row, monkeypatch, capsys):
    _id, handoff_for, edits_for, stops, expected = row
    ts, exists = _FILE_ROWS.get(_id, (None, False))
    main = _worker(tmp_path, _dispatch_with(handoff_for(tmp_path)), ts=ts)
    if exists:
        report = tmp_path.joinpath(*HANDOFFS.split("/"), "r.md")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text("report", encoding="utf-8")
    if _id == "no-edit-critic-no-track-file":
        payload = _stop_payload(str(tmp_path), "sess-hm", agent_id="w1")
        payload["transcript_path"] = str(main)
        track_file = tmp_path / ".claude" / "dod_track" / "sess-hm.json"
        first = _run_hook(payload, cwd=tmp_path)
        assert first.returncode == 2 and "HANDOFF MISSING" in first.stderr
        saved = json.loads(track_file.read_text(encoding="utf-8"))
        assert saved["gate_state"]["per_agent"]["w1"]["handoff_missing_blocked"] is True
        assert _run_hook(payload, cwd=tmp_path).returncode == 0
        return
    if _id == "readers-import-fails":
        def _boom():
            raise ImportError("transcripts gone")
        monkeypatch.setattr(dod_gate, "_import_readers", _boom)
    runs = [] if _id in _NO_GREEN_ROWS else [{"ts": "2026-07-16T10:00:05.000000", "outcome": "green",
                                              "agent_id": "w1"}]
    track = {"edits": edits_for(tmp_path), "runs": runs}
    payload = {"agent_id": "w1", "transcript_path": str(main)}
    codes = []
    for _ in range(stops):
        handoffs = dod_gate.named_handoffs(payload, str(tmp_path))
        code, message, track = dod_gate.decide(track, "w1", handoffs, str(tmp_path))
        codes.append(code)
        if code == 2 and "HANDOFF" in message[:20]:
            assert message.startswith("HANDOFF MISSING:") and "will not repeat" in message
    assert codes[-len(expected):] == expected
    state = track["gate_state"]["per_agent"]["w1"]
    if _id in _NO_GREEN_ROWS:
        actions = [g["action"] for g in track["gate_log"]]
        assert actions[:3] == ["handoff_missing", "blocked", "skipped_after_2_blocks"]
        assert actions.count("handoff_missing") == 1
    elif 2 in codes:
        assert state["handoff_missing_blocked"] is True
        assert [g["action"] for g in track["gate_log"]] == ["handoff_missing"]
    if _id == "readers-import-fails":
        assert "handoff check skipped" in capsys.readouterr().err


def test_handoff_check_skipped_when_the_valve_is_already_spent(tmp_path):
    """F-4: consecutive_blocks already >= 2 -> the handoff check is skipped (pass direction)."""
    main = _worker(tmp_path, _dispatch_with("handoff: %s" % _hp(tmp_path, HANDOFFS, "r.md")))
    handoffs = dod_gate.named_handoffs({"agent_id": "w1", "transcript_path": str(main)}, str(tmp_path))
    assert handoffs
    track = {"edits": [], "runs": [], "gate_state": {"per_agent": {"w1": {"consecutive_blocks": 2}}}}
    code, _message, track = dod_gate.decide(track, "w1", handoffs, str(tmp_path))
    assert code == 0 and "handoff_missing" not in [g["action"] for g in track.get("gate_log", [])]


def test_no_handoff_no_track_file_still_writes_nothing(tmp_path):
    main = _worker(tmp_path, _dispatch_with(""))
    payload = _stop_payload(str(tmp_path), "sess-nh", agent_id="w1")
    payload["transcript_path"] = str(main)
    assert _run_hook(payload, cwd=tmp_path).returncode == 0
    assert not (tmp_path / ".claude" / "dod_track" / "sess-nh.json").exists()


# ---- BLOCK_MESSAGE carries a re-submission hint ----


def test_block_message_names_resubmission_is_a_full_report():
    # Only the LAST message reaches the coordinator -- a
    # re-submission after this block must redeliver the whole report,
    # not point back at an earlier one. The exact wording is this
    # toolkit's own (not a byte-for-byte copy of any other repo's
    # phrasing) -- this test checks the SUBSTANCE survives, not a
    # specific sentence.
    msg = dod_gate.BLOCK_MESSAGE
    assert "complete" in msg.lower() or "whole" in msg.lower() or "all over again" in msg.lower()
    assert "last" in msg.lower()
    assert "coordinator" in msg.lower()
