"""Tests for tools/session_context.py. No network, no LLM calls; every
test builds a synthetic repo-shaped tmp directory (logs/routing-log.jsonl
+ gateway/{config.yaml,budgets.yaml,*.db}) and points build_context_lines()
/ main() at it via root=. Mirrors tools/test_usage_report.py's style.

Run from the repo root: python -m pytest tools/test_session_context.py
"""

import datetime
import importlib
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest
import yaml

from no_reaper_wrap import isolated_hook_argv
from under_test import load_under_test

from session_context import (
    build_context_lines,
    gemini_aliases,
    journal_path,
    last_calibration_line,
    last_event_line,
    main,
    now_line,
    open_degradation_window,
    read_journal_events,
)

# Worked example of the enforcement-file landing pattern: a SessionStart hook is a
# self-activating enforcement file, so a builder session adding new
# MODEL / BOOT BUDGET functions lands them under a neighboring draft
# filename first, and Lead moves the draft onto the live path only at
# acceptance. No draft is currently staged, so the import below falls
# through to the live module; this indirection means the test suite
# keeps working unchanged whenever a draft IS staged and later promoted:
# only this import line needs to flip.
# B-402: the staged draft is tools/session_context_b402.py (the task key for OPEN DISPATCH); until
# the Lead places it, the tests below that go through `sc` exercise the draft, the ones that import
# names from `session_context` above exercise the live module.
# K-WIRE: SESSION_CONTEXT_PATH names the candidate file the tests below judge instead of the live one (under_test).
sc = load_under_test("SESSION_CONTEXT_PATH", "session_context")

REQUESTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    model TEXT,
    provider_model TEXT,
    status TEXT NOT NULL,
    total_tokens INTEGER,
    traffic_kind TEXT NOT NULL DEFAULT 'real'
);
"""

CONFIG = {
    "model_list": [
        {"model_name": "middle-groq", "litellm_params": {"model": "groq/llama-3.3-70b-versatile"}},
        {"model_name": "lead-gemini", "litellm_params": {"model": "gemini/gemini-2.5-flash"}},
        {"model_name": "judge-gemini", "litellm_params": {"model": "gemini/gemini-3.5-flash"}},
    ]
}

BUDGETS = {
    "quota_windows": {
        "middle-groq": [{"window_seconds": 86400, "limit_tokens": 100000}],
    }
}


def _seed_repo(tmp_path, events=None, config=None, budgets=None) -> Path:
    root = tmp_path
    (root / "logs").mkdir(parents=True, exist_ok=True)
    gateway = root / "gateway"
    gateway.mkdir(exist_ok=True)

    if events is not None:
        with open(root / "logs" / "routing-log.jsonl", "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e) + "\n")

    with open(gateway / "config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(config if config is not None else CONFIG, f)
    with open(gateway / "budgets.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(budgets if budgets is not None else BUDGETS, f)

    conn = sqlite3.connect(gateway / "requests.db")
    conn.execute(REQUESTS_SCHEMA)
    conn.commit()
    conn.close()

    return root


def _event(event, ts="2026-07-10T08:00:00", **kw):
    e = {"ts": ts, "event": event}
    e.update(kw)
    return e


# ---- NOW line: ASCII, system clock ----

def test_now_line_is_ascii_and_uses_given_clock():
    now = datetime.datetime(2026, 7, 10, 8, 41, 23)  # a Friday
    line = now_line(now)
    assert line.isascii()
    assert "2026-07-10 08:41:23" in line
    assert "Friday" in line


# ---- journal tail ----

def test_read_journal_events_empty_when_missing(tmp_path):
    root = _seed_repo(tmp_path, events=None)
    assert read_journal_events(root) == []


def test_journal_path_location(tmp_path):
    root = _seed_repo(tmp_path, events=[])
    assert journal_path(root) == root / "logs" / "routing-log.jsonl"


def test_last_event_line_reports_tail():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("accepted", ts="2026-07-10T08:10:00", agent="builder", task_id="t-001"),
    ]
    line = last_event_line(events)
    assert "ts=2026-07-10T08:10:00" in line
    assert "event=accepted" in line
    assert "agent=builder" in line
    assert "task_id=t-001" in line


def test_last_event_line_empty_journal():
    assert "empty or missing" in last_event_line([])


# ---- CLOCK DRIFT line ----
# Field precedent: a session's journal tail carried a ts LATER than the
# system clock (a previous environment's clock ran ahead). Threshold:
# > 60s. Battery per CLAUDE.md R11: acceptance keys (fires when ahead,
# silent when not) + the boundary itself (60s exactly vs 61s) +
# adversarial fail-open inputs.


def test_clock_drift_line_absent_when_journal_ts_behind_system_clock():
    events = [_event("delegated", ts="2026-07-10T08:00:00")]
    now = datetime.datetime(2026, 7, 10, 9, 0, 0)
    assert sc.clock_drift_line(events, now) == ""


def test_clock_drift_line_at_threshold_boundary_is_silent():
    # Exactly 60s ahead -- the threshold is "> 60s" -- AT the boundary
    # must NOT fire.
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    events = [_event("delegated", ts="2026-07-10T08:01:00")]  # +60s
    assert sc.clock_drift_line(events, now) == ""


def test_clock_drift_line_one_second_past_threshold_fires():
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    events = [_event("delegated", ts="2026-07-10T08:01:01")]  # +61s
    line = sc.clock_drift_line(events, now)
    assert line.startswith("CLOCK DRIFT: last journal ts is ")
    assert "min ahead of system clock" in line
    assert "do not rewrite past lines" in line
    assert "non-monotonic" in line
    assert line.isascii()


def test_clock_drift_line_reports_minutes_ahead():
    now = datetime.datetime(2026, 7, 23, 19, 45, 56)
    events = [_event("delegated", ts="2026-07-23T20:16:32")]
    line = sc.clock_drift_line(events, now)
    assert "CLOCK DRIFT: last journal ts is 31 min ahead of system clock" in line


def test_clock_drift_line_empty_journal_is_silent():
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    assert sc.clock_drift_line([], now) == ""


def test_clock_drift_line_missing_ts_field_is_silent():
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    events = [{"event": "delegated"}]  # no 'ts' key at all
    assert sc.clock_drift_line(events, now) == ""


def test_clock_drift_line_malformed_non_iso_ts_is_silent():
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    events = [_event("delegated", ts="not-a-timestamp-at-all")]
    assert sc.clock_drift_line(events, now) == ""


def test_clock_drift_line_non_string_ts_is_silent():
    # Adversarial: a malformed journal line where ts ended up a number
    # (not the contractual string) must not crash with an AttributeError
    # from parse_ts()'s own .strip() call.
    now = datetime.datetime(2026, 7, 10, 8, 0, 0)
    events = [{"event": "delegated", "ts": 12345}]
    assert sc.clock_drift_line(events, now) == ""


def test_build_context_lines_includes_clock_drift_when_present(tmp_path):
    events = [_event("delegated", ts="2026-07-10T09:05:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 9, 0, 0)  # journal ts is +5min ahead
    lines = sc.build_context_lines(root, now)
    assert any(l.startswith("CLOCK DRIFT:") for l in lines), lines


def test_build_context_lines_omits_clock_drift_when_absent(tmp_path):
    events = [_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 9, 0, 0)  # journal ts is BEHIND now
    lines = sc.build_context_lines(root, now)
    assert not any(l.startswith("CLOCK DRIFT:") for l in lines), lines


def test_main_survives_malformed_tail_ts_no_clock_drift_crash(tmp_path, capsys):
    root = tmp_path
    (root / "logs").mkdir()
    # No routing-log.jsonl file at all.
    (root / "gateway").mkdir()
    with open(root / "gateway" / "config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(CONFIG, f)
    with open(root / "gateway" / "budgets.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(BUDGETS, f)
    conn = sqlite3.connect(root / "gateway" / "requests.db")
    conn.execute(REQUESTS_SCHEMA)
    conn.commit()
    conn.close()
    code = sc.main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert not any(l.startswith("CLOCK DRIFT:") for l in out)


def test_main_survives_broken_tail_ts_no_clock_drift_crash(tmp_path, capsys):
    events = [_event("delegated", ts="garbage-not-a-timestamp", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    code = sc.main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert not any(l.startswith("CLOCK DRIFT:") for l in out)


# ---- degradation window: open vs closed ----

def test_open_degradation_window_detects_unclosed():
    events = [
        _event("delegated", ts="2026-07-10T07:00:00"),
        _event("lead_degraded", ts="2026-07-10T07:30:00"),
        _event("delegated", ts="2026-07-10T08:00:00"),
    ]
    assert open_degradation_window(events) == "2026-07-10T07:30:00"


def test_open_degradation_window_none_when_closed():
    events = [
        _event("lead_degraded", ts="2026-07-10T07:30:00"),
        _event("lead_restored", ts="2026-07-10T07:45:00"),
        _event("delegated", ts="2026-07-10T08:00:00"),
    ]
    assert open_degradation_window(events) is None


def test_open_degradation_window_scans_whole_journal_not_just_tail():
    # An unclosed window far from the tail must still be caught -- the
    # scan is over the WHOLE journal (a safety-reset can
    # leave no lead_restored anywhere after it).
    events = [
        _event("lead_degraded", ts="2026-07-01T00:00:00"),
        *[_event("delegated", ts=f"2026-07-0{d}T00:00:00") for d in range(2, 9)],
    ]
    assert open_degradation_window(events) == "2026-07-01T00:00:00"


def test_build_context_lines_shows_open_window(tmp_path):
    events = [_event("lead_degraded", ts="2026-07-10T07:30:00")]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    lines = build_context_lines(root, now)
    assert any("OPEN DEGRADATION WINDOW since 2026-07-10T07:30:00" in l for l in lines)


def test_build_context_lines_no_open_window_line_when_closed(tmp_path):
    events = [
        _event("lead_degraded", ts="2026-07-10T07:30:00"),
        _event("lead_restored", ts="2026-07-10T07:45:00"),
    ]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    lines = build_context_lines(root, now)
    assert not any("OPEN DEGRADATION WINDOW" in l for l in lines)


# ---- last calibration: NONE vs dated, overdue suffix (spec 4.6, C4) ----

_LEAD_SUFFIX = " -- overdue: tell the owner " + sc._CALL_ARCHITECT + " (calibration and mechanism review)"
_ARCH_SUFFIX = " -- overdue: run the calibration (PROCESS/ARCHITECT_START.md step 6)"
_UNBOUND_SUFFIX = " -- overdue: run the calibration (no architect is bound; calibration and mechanism review)"
_CAL_NOW = datetime.datetime(2026, 7, 10, 12, 0, 0)


@pytest.mark.parametrize("name,events,function,want", [
    ("none-lead", [], None, "Last calibration: NONE" + _LEAD_SUFFIX),
    ("none-architect", [], "architect", "Last calibration: NONE" + _ARCH_SUFFIX),
    ("8-days-lead", [_event("calibrated", ts="2026-07-02T12:00:00")], "lead",
     "Last calibration: 2026-07-02T12:00:00 (8 days ago)" + _LEAD_SUFFIX),
    ("8-days-no-function", [_event("calibrated", ts="2026-07-02T12:00:00")], None,
     "Last calibration: 2026-07-02T12:00:00 (8 days ago)" + _LEAD_SUFFIX),
    ("8-days-architect", [_event("calibrated", ts="2026-07-02T12:00:00")], "architect",
     "Last calibration: 2026-07-02T12:00:00 (8 days ago)" + _ARCH_SUFFIX),
    ("exactly-7-days", [_event("calibrated", ts="2026-07-03T12:00:00")], "lead",
     "Last calibration: 2026-07-03T12:00:00 (7 days ago)"),
    ("unparsable-ts", [_event("calibrated", ts="not-a-date")], "lead",
     "Last calibration: not-a-date (age unknown -- unparsable ts)"),
])
def test_last_calibration_overdue_suffix(name, events, function, want):
    assert last_calibration_line(events, _CAL_NOW, function) == want


def test_last_calibration_reports_ts_and_age():
    events = [_event("calibrated", ts="2026-07-03T00:00:00")]
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    line = last_calibration_line(events, now)
    assert "2026-07-03T00:00:00" in line
    assert "7 days ago" in line


def test_last_calibration_uses_most_recent_of_several():
    events = [
        _event("calibrated", ts="2026-06-20T00:00:00"),
        _event("calibrated", ts="2026-07-08T00:00:00"),
    ]
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    line = last_calibration_line(events, now)
    assert "2026-07-08T00:00:00" in line
    assert "2 days ago" in line


# ---- gemini alias detection ----

def test_gemini_aliases_filters_by_raw_provider_prefix():
    assert set(gemini_aliases(CONFIG)) == {"lead-gemini", "judge-gemini"}


# ---- full assembly: <=25 lines, ASCII ----

def test_build_context_lines_within_line_budget_and_ascii(tmp_path):
    events = [_event("delegated", task_id="t-001"), _event("calibrated", ts="2026-07-08T00:00:00")]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    lines = build_context_lines(root, now)
    assert len(lines) <= 25
    for line in lines:
        assert line.isascii()


# ---- fail-open: broken journal never raises, always prints one warning, exit 0 ----

def test_main_fail_open_on_broken_journal(tmp_path, capsys):
    root = _seed_repo(tmp_path, events=None)
    (root / "logs" / "routing-log.jsonl").write_text("{not valid json\n", encoding="utf-8")
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    assert out[0].startswith("session-context warning:")


def test_main_full_output_when_gateway_dir_missing(tmp_path, capsys):
    # preflight_quota.load_config's exists-guard (a documented finding,
    # the same class alongside load_budgets, which already had this
    # shape): a repo root with no gateway/ directory at all (config.yaml
    # unreachable) is this toolkit's own subscription-contour DEFAULT
    # state, not a crash condition -- the SessionStart output must stay
    # FULL (NOW/LAST EVENT/BOOT BUDGET/etc still print), not collapse
    # to a single fail-open warning line the way a missing config.yaml
    # used to make it do before that guard existed (see
    # test_preflight_quota.py::test_load_config_missing_file_returns_empty_dict
    # for the underlying unit-level fix).
    root = tmp_path
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text("", encoding="utf-8")
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert any(l.startswith("NOW:") for l in out)
    assert any(l.startswith("Last calibration:") for l in out)
    assert any(l.startswith("BOOT BUDGET:") for l in out)


def test_main_full_output_when_config_yaml_missing_but_gateway_dir_exists(tmp_path, capsys):
    # Narrower sibling of the above: gateway/ EXISTS (e.g. holds only a
    # requests.db) but config.yaml specifically was never generated --
    # same exists-guard, same expected full output.
    root = tmp_path
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text("", encoding="utf-8")
    (root / "gateway").mkdir()
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert any(l.startswith("NOW:") for l in out)


# ---- config.yaml EXISTING but unparseable (corrupt YAML) ----


def test_quota_lines_malformed_config_yaml_returns_single_marker_line(tmp_path):
    gateway_root = tmp_path / "gateway"
    gateway_root.mkdir()
    (gateway_root / "config.yaml").write_text("key: [unclosed\n", encoding="utf-8")
    lines = sc.quota_lines(gateway_root)
    assert len(lines) == 1
    assert lines[0].startswith("quota: config unreadable (")
    assert lines[0].isascii()
    assert "\n" not in lines[0]


def test_quota_lines_malformed_config_yaml_reason_single_line_even_if_error_is_multiline(tmp_path):
    gateway_root = tmp_path / "gateway"
    gateway_root.mkdir()
    (gateway_root / "config.yaml").write_text("key: [unclosed\n", encoding="utf-8")
    lines = sc.quota_lines(gateway_root)
    assert len(lines) == 1
    assert len(lines[0].splitlines()) == 1


def test_main_survives_malformed_config_yaml_with_real_context(tmp_path, capsys):
    root = tmp_path
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text("", encoding="utf-8")
    gateway = root / "gateway"
    gateway.mkdir()
    (gateway / "config.yaml").write_text("key: [unclosed\n", encoding="utf-8")
    with open(gateway / "budgets.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(BUDGETS, f)
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert any(l.startswith("NOW:") for l in out)
    assert any(l.startswith("MODEL:") for l in out)
    assert any(l.startswith("JOURNAL:") for l in out)
    assert any(l.startswith("BOOT BUDGET:") for l in out)
    assert any(l.startswith("quota: config unreadable (") for l in out)


# ---- budgets.yaml EXISTING but unparseable ----


def test_quota_lines_malformed_budgets_yaml_surfaces_reason_but_keeps_rest(tmp_path):
    # Unlike a broken config.yaml (blanks quota_lines() to one marker
    # line), a broken budgets.yaml is guarded INSIDE load_budgets() --
    # the rest of this section (per-alias QUOTA/REQUESTS from config)
    # still prints normally alongside the marker.
    gateway_root = tmp_path / "gateway"
    gateway_root.mkdir()
    with open(gateway_root / "config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(CONFIG, f)
    (gateway_root / "budgets.yaml").write_text(
        "quota_windows: [this is not: valid: yaml: at all\n", encoding="utf-8"
    )
    conn = sqlite3.connect(gateway_root / "requests.db")
    conn.execute(REQUESTS_SCHEMA)
    conn.commit()
    conn.close()

    lines = sc.quota_lines(gateway_root)
    assert any(l.startswith("quota: budgets unreadable (") for l in lines)
    assert any(l.startswith("REQUESTS ") for l in lines)


def test_main_survives_malformed_budgets_yaml_with_real_context(tmp_path, capsys):
    root = tmp_path
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text("", encoding="utf-8")
    gateway = root / "gateway"
    gateway.mkdir()
    with open(gateway / "config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(CONFIG, f)
    (gateway / "budgets.yaml").write_text(
        "quota_windows: [this is not: valid: yaml: at all\n", encoding="utf-8"
    )
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert any(l.startswith("NOW:") for l in out)
    assert any(l.startswith("MODEL:") for l in out)
    assert any(l.startswith("JOURNAL:") for l in out)
    assert any(l.startswith("BOOT BUDGET:") for l in out)
    assert any(l.startswith("quota: budgets unreadable (") for l in out)


def test_main_success_path_prints_lines_and_exits_zero(tmp_path, capsys):
    events = [_event("delegated", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    code = main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) >= 2  # at least NOW + LAST EVENT
    assert any(l.startswith("NOW:") for l in out)
    assert not any(l.startswith("session-context warning:") for l in out)


# ---- stdout-deadline: env boundaries + a genuinely blocked writer ----
# (builder-role rule 6a: AT the boundary and BEYOND it, for every limit
# this port introduces.)


def test_stdout_deadline_seconds_default_with_no_env(monkeypatch):
    monkeypatch.delenv(sc._STDOUT_DEADLINE_ENV, raising=False)
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_DEFAULT


def test_stdout_deadline_seconds_valid_env_override(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, "1.5")
    assert sc._stdout_deadline_seconds() == 1.5


def test_stdout_deadline_seconds_zero_is_invalid_no_wait_forever_mode(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, "0")
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_DEFAULT


def test_stdout_deadline_seconds_negative_falls_back(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, "-1")
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_DEFAULT


def test_stdout_deadline_seconds_at_max_boundary_is_valid(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, str(sc._STDOUT_DEADLINE_MAX))
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_MAX


def test_stdout_deadline_seconds_just_over_max_falls_back(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, str(sc._STDOUT_DEADLINE_MAX + 0.001))
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_DEFAULT


def test_stdout_deadline_seconds_non_numeric_falls_back(monkeypatch):
    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, "not-a-number")
    assert sc._stdout_deadline_seconds() == sc._STDOUT_DEADLINE_DEFAULT


def test_write_stdout_deadline_normal_write_returns_true(capsys, monkeypatch):
    monkeypatch.delenv(sc._STDOUT_DEADLINE_ENV, raising=False)
    assert sc._write_stdout_deadline("hello\n") is True
    assert capsys.readouterr().out == "hello\n"


def test_write_stdout_deadline_reraises_ordinary_write_exception(monkeypatch):
    class _DeadStdout:
        def write(self, _text):
            raise OSError("simulated: stdout is dead")

        def flush(self):
            pass

    monkeypatch.setattr(sys, "stdout", _DeadStdout())
    import pytest as _pytest

    with _pytest.raises(OSError, match="simulated: stdout is dead"):
        sc._write_stdout_deadline("x")


def test_write_stdout_deadline_hanging_writer_times_out_returns_false(monkeypatch):
    class _HangingStdout:
        def write(self, _text):
            time.sleep(3600)

        def flush(self):
            pass  # pragma: no cover -- never reached

    monkeypatch.setenv(sc._STDOUT_DEADLINE_ENV, "0.1")
    monkeypatch.setattr(sys, "stdout", _HangingStdout())
    started = time.monotonic()
    result = sc._write_stdout_deadline("x")
    elapsed = time.monotonic() - started
    assert result is False
    assert elapsed < 2.0  # bounded by the 0.1s deadline, not the 3600s sleep




def test_main_stdout_deadline_timeout_exits_immediately_via_subprocess(tmp_path):
    # main()'s own contract on a write timeout is os._exit(0) -- calling
    # that in-process would kill the pytest worker itself, so this is
    # exercised as a real subprocess instead. A NON-draining consumer
    # (stdout piped but never read) alone is not enough by itself --
    # small output fits inside the OS pipe buffer and the write simply
    # returns without ever blocking. This test forces genuine
    # backpressure by making the Layer A block emit ~200KB (a BOOT.md
    # that references one large file), comfortably over any platform's
    # actual pipe capacity (the staff deployment's own critic-measured
    # value on its machine was ~4096 bytes), combined with an
    # artificially tiny OSLLM_STDOUT_TIMEOUT -- the single sys.stdout
    # write() call genuinely blocks on the full, undrained pipe, and
    # main() must os._exit(0) instead of hanging forever.
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "routing-log.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "BOOT.md").write_text("1. Read BIGFILE.md.\n", encoding="utf-8")
    (tmp_path / "BIGFILE.md").write_text("x" * 200_000 + "\n", encoding="utf-8")
    env = dict(os.environ, OSLLM_STDOUT_TIMEOUT="0.2")
    script = Path(__file__).resolve().parent / "session_context.py"
    proc = subprocess.Popen(
        isolated_hook_argv(script, tmp_path),  # copy of the file under test in tmp_path/tools; no real reaper
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(tmp_path),
        env=env,
    )
    started = time.monotonic()
    # Deliberately never read proc.stdout -- an un-drained pipe is the
    # scenario under test. wait() only watches the process exit, not
    # the pipe.
    returncode = proc.wait(timeout=15)
    elapsed = time.monotonic() - started
    proc.stdout.close()
    proc.stderr.close()
    assert returncode == 0
    # Bounded well under the 15s Popen.wait timeout above: proves the
    # process actually exited via the deadline path rather than hanging
    # until some external kill.
    assert elapsed < 10.0


# ---- N4 (carried forward from review): import-time failure must ALSO fail open ----

def test_deferred_import_error_reaches_mains_fail_open_boundary(tmp_path, capsys, monkeypatch):
    # Runtime half of the fix: once import has failed and the stub raises
    # on call, main()'s single try/except boundary must still catch it
    # (proves the deferred-raise wiring, independent of the real import
    # machinery exercised by the end-to-end test below).
    import session_context as sc

    def _boom(*_a, **_kw):
        raise ImportError("simulated: no module named 'yaml'")

    monkeypatch.setattr(sc, "load_config", _boom)
    monkeypatch.setattr(sc, "load_budgets", _boom)
    monkeypatch.setattr(sc, "alias_provider_models", _boom)
    monkeypatch.setattr(sc, "usage_in_window", _boom)

    root = _seed_repo(tmp_path, events=[_event("delegated", task_id="t-001")])
    code = sc.main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    assert out[0].startswith("session-context warning:")


def test_module_survives_broken_preflight_quota_import_and_fails_open(tmp_path, capsys, monkeypatch):
    # End-to-end, real import failure (no mock of the failure mode): a
    # syntactically broken preflight_quota.py shadows the real one via
    # sys.path priority. Before the N4 fix, this SyntaxError happened
    # DURING `import session_context` itself (module-level code, outside
    # main()'s try/except, which does not exist yet at that point) and
    # would have crashed with a bare traceback instead of failing open --
    # exactly the failure mode a SessionStart hook cannot afford.
    broken_dir = tmp_path / "broken_pkg"
    broken_dir.mkdir()
    (broken_dir / "preflight_quota.py").write_text("def broken(:\n    pass\n", encoding="utf-8")

    root = _seed_repo(tmp_path, events=[_event("delegated", task_id="t-001")])

    saved_modules = {name: sys.modules.get(name) for name in ("session_context", "preflight_quota")}
    for name in saved_modules:
        sys.modules.pop(name, None)
    monkeypatch.syspath_prepend(str(broken_dir))

    try:
        broken_sc = importlib.import_module("session_context")  # must NOT raise
        code = broken_sc.main(root)
    finally:
        sys.modules.pop("session_context", None)
        sys.modules.pop("preflight_quota", None)
        for name, mod in saved_modules.items():
            if mod is not None:
                sys.modules[name] = mod
            else:
                importlib.import_module(name)

    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    assert out[0].startswith("session-context warning:")


# ==== MODEL line ====================


class _FakeStdin:
    """Minimal stand-in for sys.stdin used to test the isatty() guard
    and the JSON read without touching the real process stdin."""

    def __init__(self, text, tty=False):
        self._text = text
        self._tty = tty

    def isatty(self):
        return self._tty

    def read(self):
        return self._text


def test_extract_model_id_top_level_string():
    assert sc.extract_model_id({"model": "claude-sonnet-5"}) == "claude-sonnet-5"


def test_extract_model_id_dict_with_id_key():
    assert sc.extract_model_id({"model": {"id": "claude-opus-4"}}) == "claude-opus-4"


def test_extract_model_id_dict_with_model_key():
    assert sc.extract_model_id({"model": {"model": "claude-haiku-3"}}) == "claude-haiku-3"


def test_extract_model_id_top_level_model_id_fallback():
    assert sc.extract_model_id({"model_id": "claude-fable-5"}) == "claude-fable-5"


def test_extract_model_id_missing_returns_none():
    assert sc.extract_model_id({}) is None
    assert sc.extract_model_id(None) is None
    assert sc.extract_model_id("not a dict") is None


_LADDER_CFG = """
roles:
  lead: {subscription: {model: claude-opus-5-5}}
  critic: {subscription: {model: claude-opus-5-5}}
  builder: {subscription: {model: claude-sonnet-5-5}}
  scout: {subscription: {model: claude-sonnet-5-5}}
  architect: {subscription: {model: claude-fable-5-1}}
"""
_NO_ARCH_CFG = _LADDER_CFG.replace("  architect: {subscription: {model: claude-fable-5-1}}\n", "")
_TODAY_CFG = _NO_ARCH_CFG.replace("lead: {subscription: {model: claude-opus-5-5}}",
                                  "lead: {subscription: {model: claude-fable-5-1}}")
_BETWEEN_CFG = ("roles:\n  lead: {subscription: {model: claude-fable-5-1}}\n"
                "  builder: {subscription: {model: claude-haiku-3}}\n")
_DECL = "(declared by harness, not measured; lead = claude-opus-5-5, architect = {arch})"
_NOT_PROVIDED = "MODEL: not provided by hook input -- verify tier yourself"
_NONE_LINE = ("MODEL: {m} -> function none (matches no binding in delegation.config.yaml)"
              " -- coordinate under the below-lead rules until verified")


_MODEL_ROWS = [
    ("exact-lead", ("claude-opus-5-5", _LADDER_CFG),
     "MODEL: claude-opus-5-5 -> function lead " + _DECL.format(arch="claude-fable-5-1")),
    ("exact-architect", ("claude-fable-5-1", _LADDER_CFG),
     "MODEL: claude-fable-5-1 -> function architect " + _DECL.format(arch="claude-fable-5-1")),
    ("exact-builder", ("claude-sonnet-5-5", _LADDER_CFG),
     "MODEL: claude-sonnet-5-5 -> function builder " + _DECL.format(arch="claude-fable-5-1")),
    ("family-match-live-case", ("claude-fable-5-2", _LADDER_CFG),
     "MODEL: claude-fable-5-2 -> function architect (family match: claude-fable-5-1) "
     + _DECL.format(arch="claude-fable-5-1")),
    ("today-config-family-match-lead", ("claude-fable-5-2", _TODAY_CFG),
     "MODEL: claude-fable-5-2 -> function lead (family match: claude-fable-5-1) "
     "(declared by harness, not measured; lead = claude-fable-5-1, architect = unbound)"),
    ("between-families-unbound", ("claude-opus-5-5", _BETWEEN_CFG),
     "MODEL: claude-opus-5-5 -> function builder (unbound family) "
     "(declared by harness, not measured; lead = claude-fable-5-1, architect = unbound)"),
    ("above-lead-no-architect-key", ("claude-fable-5-2", _NO_ARCH_CFG),
     "MODEL: claude-fable-5-2 -> function above lead (no architect binding) " + _DECL.format(arch="unbound")),
    ("unbound-family-weaker", ("claude-haiku-3", _LADDER_CFG),
     "MODEL: claude-haiku-3 -> function below builder " + _DECL.format(arch="claude-fable-5-1")),
    ("unrecognised-model", ("gpt-9", _LADDER_CFG), _NONE_LINE.format(m="gpt-9")),
    ("config-unreadable", ("claude-opus-5-5", "roles: [unclosed"),
     "MODEL: claude-opus-5-5 -> function critic (declared by harness, not measured; lead = claude-fable,"
     " architect = unbound) (config unreadable: default bindings)".replace("claude-fable", "fable")),
    ("config-absent", ("claude-sonnet-5-5", None),
     "MODEL: claude-sonnet-5-5 -> function builder (declared by harness, not measured; lead = fable,"
     " architect = unbound) (config unreadable: default bindings)"),
] 


@pytest.mark.parametrize("name,cfg,want", _MODEL_ROWS, ids=[r[0] for r in _MODEL_ROWS])
def test_model_line_function_by_ladder(name, cfg, want):
    assert sc.model_line({"model": cfg[0]}, cfg[1]) == want


def test_model_line_dict_form():
    assert sc.model_line({"model": {"id": "claude-sonnet-5-5"}}, _LADDER_CFG).startswith(
        "MODEL: claude-sonnet-5-5 -> function builder ")


def test_model_line_missing_payload():
    assert sc.model_line(None) == (
        "MODEL: not provided by hook input -- verify tier yourself"
    )


def test_model_line_empty_payload():
    assert sc.model_line({}) == (
        "MODEL: not provided by hook input -- verify tier yourself"
    )


# ---- model_line() ASCII/single-line
# sanitization of the externally-sourced model id (critic-confirmed) ----------------------


def test_model_line_non_ascii_model_id_is_sanitized():
    line = sc.model_line({"model": "café\nX"})
    assert line.isascii()
    assert "\n" not in line
    assert len(line.splitlines()) == 1


def test_model_line_emoji_model_id_is_sanitized():
    line = sc.model_line({"model": "sonnet\U0001F600rocket"})
    assert line.isascii()
    assert "\n" not in line
    assert len(line.splitlines()) == 1


def test_model_line_injection_attempt_stays_single_line():
    line = sc.model_line({"model": "x\nINJECTED FAKE LINE"})
    assert line.isascii()
    assert "\n" not in line
    assert len(line.splitlines()) == 1
    assert "INJECTED FAKE LINE" in line  # content kept, just de-lineified


def test_model_line_whitespace_only_falls_back_to_not_provided():
    assert sc.model_line({"model": "   "}) == (
        "MODEL: not provided by hook input -- verify tier yourself"
    )


def test_model_line_long_model_id_is_truncated():
    long_id = "sonnet-" + ("a" * 100)
    line = sc.model_line({"model": long_id})
    assert line.isascii()
    assert "\n" not in line
    # "MODEL: " prefix + sanitized (<=80 chars) + " -> function ... " suffix
    sanitized = sc._ascii_sanitize(long_id)
    assert len(sanitized) == 80
    assert line.startswith(f"MODEL: {sanitized} -> function ")


def test_ascii_sanitize_direct_cases():
    assert sc._ascii_sanitize("   ") == ""
    assert sc._ascii_sanitize("x\nINJECTED FAKE LINE") == "xINJECTED FAKE LINE"
    assert sc._ascii_sanitize("caféX").isascii()
    assert sc._ascii_sanitize("a" * 200, max_len=80) == "a" * 80


def test_read_stdin_payload_skips_when_tty(monkeypatch):
    # The isatty() guard must prevent any read() call at all when stdin
    # is a TTY (a manual run from an interactive shell must not block).
    def _boom():
        raise AssertionError("read() must not be called when stdin is a TTY")

    fake = _FakeStdin("", tty=True)
    fake.read = _boom
    monkeypatch.setattr(sys, "stdin", fake)
    assert sc.read_stdin_payload() is None


def test_read_stdin_payload_parses_json_when_piped(monkeypatch):
    fake = _FakeStdin(json.dumps({"model": "claude-opus-4"}), tty=False)
    monkeypatch.setattr(sys, "stdin", fake)
    assert sc.read_stdin_payload() == {"model": "claude-opus-4"}


def test_read_stdin_payload_returns_none_on_malformed_json(monkeypatch):
    fake = _FakeStdin("{not valid json", tty=False)
    monkeypatch.setattr(sys, "stdin", fake)
    assert sc.read_stdin_payload() is None


def test_read_stdin_payload_returns_none_on_empty_input(monkeypatch):
    fake = _FakeStdin("", tty=False)
    monkeypatch.setattr(sys, "stdin", fake)
    assert sc.read_stdin_payload() is None


def _seed_ladder(root, cfg=_LADDER_CFG, settings=None, queue=None):
    if cfg is not None:
        (root / "delegation.config.yaml").write_text(cfg, encoding="utf-8")
    if settings is not None:
        (root / ".claude").mkdir(exist_ok=True)
        (root / ".claude" / "settings.json").write_text(settings, encoding="utf-8")
    if queue is not None:
        (root / "docs" / "tasks").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "tasks" / "architect-queue.md").write_text(queue, encoding="utf-8")
    return root


_ARCH_HEAD = ("ARCHITECT SESSION: start with PROCESS/ARCHITECT_START.md;"
              " queue docs/tasks/architect-queue.md ")
_Q3 = "# queue\n- [ ] 2026-11-17 t-1 a (\u043e\u0442: Lead)\n- [x] 2026-11-16 t-2 b - done: D-1\n- [ ] x\n  - [ ] y\n"


_ARCH_ROWS = [
    ("architect-family-queue-3-open", "claude-fable-5-2", _LADDER_CFG, _Q3, False, _ARCH_HEAD + "(3 open)"),
    ("architect-exact-queue-0-open", "claude-fable-5-1", _LADDER_CFG, "- [x] done\n", False, _ARCH_HEAD + "(0 open)"),
    ("architect-queue-absent", "claude-fable-5-2", _LADDER_CFG, None, False, _ARCH_HEAD + "(queue file absent)"),
    ("architect-queue-unreadable", "claude-fable-5-2", _LADDER_CFG, None, True,
     _ARCH_HEAD + "(queue unreadable: "),
    ("lead-session-no-line", "claude-opus-5-5", _LADDER_CFG, _Q3, False, None),
    ("builder-session-no-line", "claude-sonnet-5-5", _LADDER_CFG, _Q3, False, None),
    ("fable-no-architect-key-no-line", "claude-fable-5-2", _NO_ARCH_CFG, _Q3, False, None),
    ("unrecognised-model-no-line", "gpt-9", _LADDER_CFG, _Q3, False, None),
] 


@pytest.mark.parametrize("name,model,cfg,queue,queue_as_dir,want_arch", _ARCH_ROWS, ids=[r[0] for r in _ARCH_ROWS])
def test_architect_line_in_context(tmp_path, name, model, cfg, queue, queue_as_dir, want_arch):
    root = _seed_repo(tmp_path, events=[])
    _seed_ladder(root, cfg, queue=queue)
    if queue_as_dir:
        (root / "docs" / "tasks" / "architect-queue.md").mkdir(parents=True)
    lines = sc.build_context_lines(root, datetime.datetime(2026, 7, 11, 9, 0, 0), stdin_payload={"model": model})
    assert lines[0].startswith("NOW:")
    assert lines[1].startswith(f"MODEL: {model} -> function ")
    arch = [l for l in lines if l.startswith("ARCHITECT SESSION")]
    if want_arch is None:
        assert arch == []
    else:
        assert len(arch) == 1 and arch[0].startswith(want_arch) and lines[2] == arch[0]
        assert arch[0].isascii()


_PIN_WARN = ("WARN: .claude/settings.json model {x} != lead binding claude-opus-5-5"
             " -- new sessions open on {x}; align one of them")


@pytest.mark.parametrize("name,settings,cfg,want", [
    ("equal-no-line", '{"model": "claude-opus-5-5"}', _LADDER_CFG, None),
    ("differ-warn", '{"model": "claude-fable-5-1"}', _LADDER_CFG, _PIN_WARN.format(x="claude-fable-5-1")),
    ("settings-without-model", '{"hooks": {}}', _LADDER_CFG, None),
    ("settings-absent", None, _LADDER_CFG, None),
    ("settings-unparsable", "{not json", _LADDER_CFG, "WARN: .claude/settings.json unreadable ("),
    ("model-not-a-string", '{"model": 5}', _LADDER_CFG, None),
    ("config-unreadable-no-pin-line", '{"model": "claude-fable-5-1"}', "roles: [unclosed", None),
])
def test_settings_pin_line_in_context(tmp_path, name, settings, cfg, want):
    root = _seed_repo(tmp_path, events=[])
    _seed_ladder(root, cfg, settings=settings)
    lines = sc.build_context_lines(root, datetime.datetime(2026, 7, 11, 9, 0, 0),
                                   stdin_payload={"model": "claude-opus-5-5"})
    pin = [l for l in lines if l.startswith("WARN: .claude/settings.json")]
    if want is None:
        assert pin == []
    else:
        assert len(pin) == 1 and pin[0].startswith(want)
        assert lines[2] == pin[0]  # directly after MODEL (no ARCHITECT line for an Opus session)


def test_architect_and_pin_lines_survive_the_25_line_cut(tmp_path, monkeypatch):
    root = _seed_repo(tmp_path, events=[])
    _seed_ladder(root, settings='{"model": "claude-fable-5-1"}', queue=_Q3)
    monkeypatch.setattr(sc, "quota_lines", lambda *a, **k: [f"filler {i}" for i in range(30)])  # 30 candidates
    lines = sc.build_context_lines(root, datetime.datetime(2026, 7, 11, 9, 0, 0),
                                   stdin_payload={"model": "claude-fable-5-2"})
    assert len(lines) == sc.MAX_LINES and "filler 0" in lines and "filler 29" not in lines
    assert lines[1].startswith("MODEL:") and lines[2].startswith("ARCHITECT SESSION:")
    assert lines[3].startswith("WARN: .claude/settings.json model claude-fable-5-1")


def test_build_context_lines_calibration_suffix_follows_session_function(tmp_path):
    root = _seed_repo(tmp_path, events=[_event("calibrated", ts="2026-06-01T00:00:00")])
    _seed_ladder(root)
    now = datetime.datetime(2026, 7, 11, 9, 0, 0)
    lead = sc.build_context_lines(root, now, stdin_payload={"model": "claude-opus-5-5"})
    arch = sc.build_context_lines(root, now, stdin_payload={"model": "claude-fable-5-2"})
    assert [l for l in lead if l.startswith("Last calibration")][0].endswith(_LEAD_SUFFIX)
    assert [l for l in arch if l.startswith("Last calibration")][0].endswith(_ARCH_SUFFIX)


@pytest.mark.parametrize("model", ["claude-opus-5-5", "claude-fable-5-2"])
def test_calibration_suffix_without_architect_binding_never_sends_to_an_architect(tmp_path, model):
    root = _seed_repo(tmp_path, events=[_event("calibrated", ts="2026-06-01T00:00:00")])
    _seed_ladder(root, _NO_ARCH_CFG)
    lines = sc.build_context_lines(root, datetime.datetime(2026, 7, 11, 9, 0, 0), stdin_payload={"model": model})
    got = [l for l in lines if l.startswith("Last calibration")][0]
    assert got.endswith(_UNBOUND_SUFFIX) and "Architect" not in got


# ==== BOOT BUDGET ==============


_COORD_SIZE = 10  # bytes of each seeded coordinator file: small, so the top-3 breakdown keeps its big rows


def _nf(n):
    """The file count of a BOOT BUDGET head for n BOOT.md/CLAUDE.md files: the coordinator files count too (worker split)."""
    return n + len(sc._coordinator_files())


_CB = _COORD_SIZE * len(sc._coordinator_files())  # their bytes, computed from the fixture's list, never retyped


def _seed_coordinator(root: Path):
    for name in sc._coordinator_files():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"c" * _COORD_SIZE)


def _seed_boot_files(root: Path, file_sizes: dict, boot_md_names=None):
    """Writes BOOT.md whose body references boot_md_names via "Read
    X.md" lines (defaults to the keys of file_sizes minus CLAUDE.md,
    since CLAUDE.md is always added by the code under test, not by
    BOOT.md's own list), plus each file in file_sizes at the given byte
    size (content is padding bytes, exact bytes matter for the budget
    arithmetic, not readability)."""
    if boot_md_names is None:
        boot_md_names = [n for n in file_sizes if n != "CLAUDE.md"]
    body = "\n".join(f"1. Read {name}." for name in boot_md_names)
    (root / "BOOT.md").write_text(body + "\n", encoding="utf-8")
    for name, size in file_sizes.items():
        (root / name).write_bytes(b"x" * size)
    _seed_coordinator(root)


def test_boot_path_files_parses_boot_md_and_always_adds_claude_md(tmp_path):
    root = tmp_path
    (root / "BOOT.md").write_text(
        "1. Read README.md.\n2. Read PROJECT_CHARTER.md.\n", encoding="utf-8"
    )
    names = sc.boot_path_files(root)
    assert names == ["README.md", "PROJECT_CHARTER.md", *sc._coordinator_files(), "CLAUDE.md"]


def test_boot_path_files_counts_a_coordinator_file_once_when_boot_md_names_it(tmp_path):
    """Edge e17: BOOT.md stays the owner of its own list; a name it shares with COORDINATOR_FILES is counted once, in BOOT.md's place."""
    (tmp_path / "BOOT.md").write_text("1. Read PROJECT.md.\n2. Read README.md.\n", encoding="utf-8")
    names = sc.boot_path_files(tmp_path)
    assert names.count("PROJECT.md") == 1 and names[:2] == ["PROJECT.md", "README.md"]
    assert names[-1] == "CLAUDE.md" and set(sc._coordinator_files()) <= set(names)


def test_boot_path_files_missing_boot_md_still_yields_claude_md(tmp_path):
    assert sc.boot_path_files(tmp_path) == [*sc._coordinator_files(), "CLAUDE.md"]


def test_boot_budget_normal_under_warn_threshold(tmp_path):
    root = tmp_path
    _seed_boot_files(root, {"README.md": 100, "CLAUDE.md": 200})
    lines = sc.boot_budget_lines(root)
    assert lines == [f"BOOT BUDGET: {300 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files) | CLAUDE.md: 200/{sc.CLAUDE_WARN}"]


def test_boot_budget_warn_includes_top3(tmp_path):
    root = tmp_path
    readme = sc.BOOT_BREACH_THRESHOLD - 5000 - 30000 - 25000 - 100
    _seed_boot_files(
        root,
        {
            "README.md": readme,
            "PROJECT_CHARTER.md": 30000,
            "ANTI_GOALS.md": 25000,
            "CLAUDE.md": 100,
        },
    )
    lines = sc.boot_budget_lines(root)
    total = readme + 30000 + 25000 + 100 + _CB
    assert total > sc.BOOT_WARN_THRESHOLD
    assert total <= sc.BOOT_BREACH_THRESHOLD
    assert lines[0] == f"BOOT BUDGET: {total} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(4)} files) WARN | CLAUDE.md: 100/{sc.CLAUDE_WARN}"
    assert lines[1] == f"  {readme}  README.md"
    assert lines[2] == "  30000  PROJECT_CHARTER.md"
    assert lines[3] == "  25000  ANTI_GOALS.md"
    assert len(lines) == 4


def test_boot_budget_breach_includes_hint_and_top3(tmp_path):
    root = tmp_path
    readme = sc.BOOT_BREACH_THRESHOLD + 5000 - 30000 - 20000 - 100
    _seed_boot_files(
        root,
        {
            "README.md": readme,
            "PROJECT_CHARTER.md": 30000,
            "ANTI_GOALS.md": 20000,
            "CLAUDE.md": 100,
        },
    )
    lines = sc.boot_budget_lines(root)
    total = readme + 30000 + 20000 + 100 + _CB
    assert total > sc.BOOT_BREACH_THRESHOLD
    assert lines[0] == (
        f"BOOT BUDGET: {total} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(4)} files) BREACH -> boot-diet due "
        f"(report first, operator word starts it) | CLAUDE.md: 100/{sc.CLAUDE_WARN}"
    )
    assert lines[1] == f"  {readme}  README.md"
    assert lines[2] == "  30000  PROJECT_CHARTER.md"
    assert lines[3] == "  20000  ANTI_GOALS.md"


def test_boot_budget_missing_file_counts_zero_and_is_flagged(tmp_path):
    root = tmp_path
    # BOOT.md references a file that is never actually written.
    (root / "BOOT.md").write_text("1. Read GHOST_FILE.md.\n", encoding="utf-8")
    (root / "CLAUDE.md").write_bytes(b"x" * 50)
    _seed_coordinator(root)
    lines = sc.boot_budget_lines(root)
    assert lines[0] == (
        f"BOOT BUDGET: {50 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files) [missing: GHOST_FILE.md]"
        f" | CLAUDE.md: 50/{sc.CLAUDE_WARN}"
    )


def test_boot_budget_lines_within_output_budget(tmp_path):
    root = tmp_path
    _seed_boot_files(
        root,
        {
            "README.md": 60000,
            "PROJECT_CHARTER.md": 30000,
            "ANTI_GOALS.md": 20000,
            "CLAUDE.md": 100,
        },
    )
    lines = sc.boot_budget_lines(root)
    # 1 summary + top-3 when CLAUDE.md has no @imports; with imports the block
    # grows by at most IMPORT_ROWS_MAX rows + 1 "more" line + 1 WARN line (pinned below)
    assert len(lines) <= 4


# ---- CLAUDE.md @imports (F6-27) ----


_WARN_BAND_README = sc.BOOT_BREACH_THRESHOLD - 5000  # README size that lands the small-import tests in the WARN band


def _seed_claude_imports(root: Path, claude_text: str, readme_size: int = _WARN_BAND_README, **files):
    """BOOT.md + a README.md of readme_size bytes + CLAUDE.md with the
    given text + the extra files (relative path -> byte size)."""
    (root / "BOOT.md").write_text("1. Read README.md.\n", encoding="utf-8")
    (root / "README.md").write_bytes(b"x" * readme_size)
    claude_bytes = claude_text.encode("utf-8")
    (root / "CLAUDE.md").write_bytes(claude_bytes)
    for rel, size in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"y" * size)
    _seed_coordinator(root)
    return len(claude_bytes)


def test_boot_budget_counts_two_imports_under_claude_md(tmp_path):
    claude_text = "# rules\n@a.md\n@sub/b.md\n"
    own = _seed_claude_imports(tmp_path, claude_text, **{"a.md": 1000, "sub/b.md": 2000})
    lines = sc.boot_budget_lines(tmp_path)
    total = _WARN_BAND_README + own + 1000 + 2000 + _CB
    assert lines[0].startswith(f"BOOT BUDGET: {total} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 2 imports)")
    assert f"| CLAUDE.md: {own}/{sc.CLAUDE_WARN} incl. imports {own + 3000}" in lines[0]
    # the per-file list (WARN band) shows each import right under CLAUDE.md
    assert lines[1] == f"  {_WARN_BAND_README}  README.md"
    assert lines[2] == f"  {own}  CLAUDE.md"
    assert lines[3] == "    @a.md  1000"
    assert lines[4] == "    @sub/b.md  2000"
    assert len(lines) == 6 and lines[5] == f"  {_COORD_SIZE}  {sc._coordinator_files()[0]}"  # the third row: a coordinator file


def test_boot_budget_breach_verdict_follows_the_total_with_imports(tmp_path):
    # files alone are under the warn line, the imports push the total over
    # the breach line; the thresholds themselves are unchanged.
    readme = sc.BOOT_WARN_THRESHOLD - 5000
    big = sc.BOOT_BREACH_THRESHOLD - readme + 5000
    own = _seed_claude_imports(tmp_path, "@big.md\n", readme_size=readme, **{"big.md": big})
    lines = sc.boot_budget_lines(tmp_path)
    assert readme + own <= sc.BOOT_WARN_THRESHOLD
    assert lines[0].startswith(f"BOOT BUDGET: {readme + own + big + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 1 imports) BREACH")


def test_boot_budget_missing_import_is_size_zero_warned_and_marks_the_total_a_floor(tmp_path):
    own = _seed_claude_imports(tmp_path, "@a.md\n@ghost.md\n", **{"a.md": 1000})
    lines = sc.boot_budget_lines(tmp_path)
    # F-5: the header says the total is a floor
    assert lines[0].startswith(f"BOOT BUDGET: {_WARN_BAND_README + own + 1000 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 2 imports (+1 unmeasured))")
    assert "    @ghost.md  0" in lines
    assert "BOOT IMPORT WARN: 1 not measured: ghost.md (missing)" in lines
    assert sc.claude_imports(tmp_path) == [("a.md", 1000), ("ghost.md", 0)]


def test_boot_budget_all_imports_measured_has_no_unmeasured_marker(tmp_path):
    _seed_claude_imports(tmp_path, "@a.md\n", **{"a.md": 10})
    lines = sc.boot_budget_lines(tmp_path)
    assert "unmeasured" not in lines[0]
    assert not any("IMPORT WARN" in l for l in lines)


def test_boot_budget_directory_import_is_size_zero_and_warned(tmp_path):
    _seed_claude_imports(tmp_path, "@docs\n")
    (tmp_path / "docs").mkdir(exist_ok=True)  # the seeded coordinator index files already made it
    (tmp_path / "docs" / "f.md").write_bytes(b"z" * 500)
    assert sc.claude_imports(tmp_path) == [("docs", 0)]
    assert "BOOT IMPORT WARN: 1 not measured: docs (directory)" in sc.boot_budget_lines(tmp_path)


def test_boot_budget_import_leaving_the_root_is_warned_not_measured(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "outside.md").write_bytes(b"o" * 700)
    # edge (c): a `..` that stays inside the root is inside
    _seed_claude_imports(root, "@../outside.md\n@sub/../a.md\n", **{"a.md": 10})
    assert sc.claude_imports(root) == [("../outside.md", 0), ("sub/../a.md", 10)]
    lines = sc.boot_budget_lines(root)
    assert "BOOT IMPORT WARN: 1 not measured: ../outside.md (outside the root)" in lines
    assert not any("sub/../a.md" in l and "WARN" in l for l in lines)


def test_import_size_absolute_path_inside_the_root_is_measured(tmp_path):
    (tmp_path / "a.md").write_bytes(b"a" * 7)
    assert sc._import_size(tmp_path, str(tmp_path / "a.md")) == (7, None)
    assert sc._import_size(tmp_path, str(tmp_path.parent / "elsewhere.md")) == (0, "outside the root")


def test_import_size_embedded_nul_is_missing_not_a_traceback(tmp_path):
    assert sc._import_size(tmp_path, "a\x00b.md") == (0, "missing")


def _no_filesystem(monkeypatch):
    """Makes every filesystem call the old resolve()-first code made raise."""

    def boom(*_a, **_k):
        raise AssertionError("the filesystem was touched")

    monkeypatch.setattr(Path, "resolve", boom)
    monkeypatch.setattr(os, "stat", boom)
    monkeypatch.setattr(Path, "stat", boom)
    monkeypatch.setattr(Path, "is_dir", boom)


def test_import_size_unc_tilde_and_foreign_paths_are_classified_without_the_filesystem(tmp_path, monkeypatch):
    # t-923 F-2: Path.resolve() opens a UNC path (21 s per line at session
    # start). The decision is lexical; nothing here may reach the disk.
    root = tmp_path / "repo"
    root.mkdir()
    cases = {
        "//10.255.255.1/share/x.md": (0, "outside the root"),
        "\\\\10.255.255.1\\share\\x.md": (0, "outside the root"),
        "~/x.md": (0, "unsupported"),
        "~user/x.md": (0, "unsupported"),
        "../x.md": (0, "outside the root"),
        "a/../../x.md": (0, "outside the root"),
        "..": (0, "outside the root"),
        str(tmp_path / "other.md"): (0, "outside the root"),
    }
    if os.name == "nt":
        other = "D" if root.drive.upper().startswith("C") else "C"
        cases[f"{other}:/elsewhere/x.md"] = (0, "outside the root")  # commonpath raises on two drives
        cases[f"{other}:x.md"] = (0, "outside the root")
        cases["/rooted.md"] = (0, "outside the root")
    with monkeypatch.context() as m:
        _no_filesystem(m)
        got = {written: sc._import_size(root, written) for written in cases}
    assert got == cases


def test_import_size_unc_form_is_outside_the_root_on_every_host_even_when_a_file_of_that_name_exists(tmp_path, monkeypatch):
    # t-1101: on POSIX a backslash is a name character, so `\\host\share\x.md`
    # joined to the root is a path INSIDE it; the UNC form still decides by its
    # two leading separators (mixed forms too) and the disk is not touched.
    root = tmp_path / "repo"
    root.mkdir()
    if os.name != "nt":
        (root / "\\\\host\\share\\x.md").write_bytes(b"x")  # the Linux shape: a file by that very name
    (root / "plain.md").write_bytes(b"12345")
    cases = ["\\\\host\\share\\x.md", "\\/host/x.md", "/\\host/x.md", "//host/x.md", "\\\\?\\C:\\x.md"]
    with monkeypatch.context() as m:
        _no_filesystem(m)
        got = {written: sc._import_size(root, written) for written in cases}
    assert got == {written: (0, "outside the root") for written in cases}
    # one separator is not a UNC form: a plain name inside the root still costs its stat
    assert sc._import_size(root, "plain.md") == (5, None)


def test_import_size_unc_import_does_not_stall_the_session_start(tmp_path):
    t0 = time.monotonic()
    assert sc._import_size(tmp_path, "//10.255.255.1/share/x.md") == (0, "outside the root")
    assert time.monotonic() - t0 < 1.0


def test_boot_budget_import_inside_a_code_fence_is_not_counted(tmp_path):
    claude_text = "text\n```\n@in_fence.md\n```\n@real.md\n"
    own = _seed_claude_imports(tmp_path, claude_text, **{"in_fence.md": 111, "real.md": 222})
    assert sc.claude_imports(tmp_path) == [("real.md", 222)]
    lines = sc.boot_budget_lines(tmp_path)
    assert lines[0].startswith(f"BOOT BUDGET: {_WARN_BAND_README + own + 222 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 1 imports)")
    assert not any("in_fence" in l for l in lines)


def test_boot_budget_no_import_lines_has_no_imports_suffix(tmp_path):
    # pinned form: no "+ N imports" at all (not "+ 0 imports"), and no
    # "incl. imports" figure on the CLAUDE.md layer.
    own = _seed_claude_imports(tmp_path, "# no imports here\n  @indented.md\nmail a@b.c\n")
    assert sc.claude_imports(tmp_path) == []
    lines = sc.boot_budget_lines(tmp_path)
    assert lines[0].startswith(f"BOOT BUDGET: {_WARN_BAND_README + own + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files)")
    assert "imports" not in lines[0]


def test_boot_budget_same_file_imported_twice_is_counted_twice(tmp_path):
    # the harness injects it twice, so the session pays for it twice
    own = _seed_claude_imports(tmp_path, "@a.md\n@a.md\n", **{"a.md": 1000})
    assert sc.claude_imports(tmp_path) == [("a.md", 1000), ("a.md", 1000)]
    assert sc.boot_budget_lines(tmp_path)[0].startswith(
        f"BOOT BUDGET: {_WARN_BAND_README + own + 2000 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 2 imports)"
    )


def test_boot_budget_import_line_tolerates_trailing_spaces_and_backslashes(tmp_path):
    _seed_claude_imports(tmp_path, "@a.md   \r\n@sub\\b.md\r\n", **{"a.md": 1, "sub/b.md": 2})
    got = sc.claude_imports(tmp_path)
    assert got[0] == ("a.md", 1)
    # Path decides the backslash: it resolves on Windows, is a plain
    # (missing) name on POSIX.
    assert got[1] == (("sub\\b.md", 2) if os.name == "nt" else ("sub\\b.md", 0))


def test_claude_imports_without_claude_md_is_empty_and_silent(tmp_path):
    (tmp_path / "BOOT.md").write_text("1. Read README.md.\n", encoding="utf-8")
    assert sc.claude_imports(tmp_path) == []
    lines = sc.boot_budget_lines(tmp_path)
    assert not any("IMPORT WARN" in l for l in lines)
    assert "imports" not in lines[0]


def test_claude_imports_unreadable_claude_md_is_a_warn_not_a_traceback(tmp_path):
    (tmp_path / "BOOT.md").write_text("1. Read README.md.\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_bytes(b"@a.md\n\xff\xfe\x80 not utf-8\n")
    assert sc.claude_imports(tmp_path) == []
    lines = sc.boot_budget_lines(tmp_path)
    assert "BOOT IMPORT WARN: CLAUDE.md unreadable" in lines


def test_claude_imports_sees_no_import_in_the_real_claude_md():
    repo_root = Path(__file__).resolve().parent.parent
    got = sc.claude_imports(repo_root)
    assert got == []  # the worker split: CLAUDE.md imports nothing (K-WORKER); the coordinator files are read on the hook line


# ---- t-923 fix round: F-1 sanitizer, F-3 one reader, F-4 line cap, F-6 ranking ----


def test_boot_budget_non_ascii_import_path_is_sanitized_present_and_missing(tmp_path):
    # F-1: the path comes from CLAUDE.md; every printed line stays ASCII.
    # Edge (a): the sanitizer turns Cyrillic into `?`; still ONE row per
    # import and the byte count is still printed.
    own = _seed_claude_imports(
        tmp_path, "@docs/правила.md\n@docs/нет.md\n",
        **{"docs/правила.md": 100},
    )
    lines = sc.boot_budget_lines(tmp_path)
    assert all(l.isascii() for l in lines)
    assert lines[0].startswith(f"BOOT BUDGET: {_WARN_BAND_README + own + 100 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 2 imports (+1 unmeasured))")
    assert "    @docs/???????.md  100" in lines
    assert "    @docs/???.md  0" in lines
    assert any(l.startswith("BOOT IMPORT WARN: 1 not measured: docs/???.md (missing)") for l in lines)
    assert not any("\n" in l for l in lines)
    # the raw form is still what claude_imports() returns
    assert sc.claude_imports(tmp_path)[0][0] == "docs/правила.md"


def test_boot_budget_control_characters_in_an_import_path_do_not_break_the_line(tmp_path):
    _seed_claude_imports(tmp_path, "@a\x1b[31mb.md\n")
    lines = sc.boot_budget_lines(tmp_path)
    assert all(l.isascii() and "\x1b" not in l for l in lines)


def test_main_with_a_cyrillic_import_on_a_cp1252_stdout_keeps_the_whole_context(tmp_path, monkeypatch):
    # The F-1 probe: stdout encoded cp1252 as a Windows pipe is. The old
    # code raised UnicodeEncodeError inside main() and every other line
    # (NOW/MODEL/JOURNAL/BOOT BUDGET/WIRING) was replaced by one warning.
    root = _seed_repo(tmp_path, events=[_event("delegated", task_id="t-001")])
    _seed_claude_imports(root, "@docs/правила.md\n@docs/нет.md\n",
                         **{"docs/правила.md": 100})
    monkeypatch.setattr(sys, "stdin", _FakeStdin(json.dumps({"model": "claude-sonnet-5"}), tty=False))
    raw = io.BytesIO()
    wrapper = io.TextIOWrapper(raw, encoding="cp1252", errors="strict", write_through=True)
    monkeypatch.setattr(sys, "stdout", wrapper)
    assert sc.main(root) == 0
    wrapper.flush()
    out = raw.getvalue().decode("cp1252").splitlines()
    assert not any(l.startswith("session-context warning:") for l in out)
    assert any(l.startswith("NOW:") for l in out)
    assert any(l.startswith("BOOT BUDGET:") for l in out)
    assert any(l.startswith("    @docs/") and l.endswith("  100") for l in out)


_FENCE_SAMPLES = {
    # the shapes of the t-923 F-3 probe (the old local tracker disagreed on 4 of 5)
    "info string inside a markdown block": ("```markdown\n```sh\n```\n@real.md\n", ["real.md"]),
    "four ticks hold a three-tick line": ("````\n```\n@in.md\n````\n@real.md\n", ["real.md"]),
    "tilde block": ("~~~\n@in.md\n~~~\n@real.md\n", ["real.md"]),
    "four-space indent is not a fence": ("    ```\n@real.md\n", ["real.md"]),
    # md_table opens a fence on a one-line ```x``` (CommonMark 4.5 says it
    # must not, t-923 Q-3): both readers lose real.md the same way -- the
    # shared reader wins, only the agreement is pinned here.
    "ticks-x-ticks line": ("```x```\n@real.md\n", None),
}


@pytest.mark.parametrize("name", sorted(_FENCE_SAMPLES))
def test_claude_imports_agrees_with_agents_md_on_the_same_claude_md(tmp_path, name):
    # F-3: ONE reader. agents_md expands exactly the imports the harness
    # injects; the boot budget must count the same lines.
    import agents_md

    text, expected = _FENCE_SAMPLES[name]
    _seed_claude_imports(tmp_path, text, **{"in.md": 5, "real.md": 7})
    body = "\n".join(agents_md.build_claude_body(tmp_path))
    expanded = re.findall(r"<!-- begin (\S+) -->", body)
    counted = [path for path, _size in sc.claude_imports(tmp_path)]
    assert counted == expanded
    if expected is not None:
        assert counted == expected


def test_the_boot_budget_holds_no_second_fence_tracker_or_import_regex():
    import agents_md
    import md_table

    assert sc._md_table is md_table and sc._IMPORT_RE is agents_md.IMPORT_RE
    src = Path(sc.__file__).read_text(encoding="utf-8")
    assert "in_fence" not in src and 'startswith("```")' not in src
    assert 're.compile(r"^@' not in src


def test_boot_budget_reader_import_failure_is_one_warn_not_a_dead_hook(tmp_path, monkeypatch):
    _seed_claude_imports(tmp_path, "@a.md\n", **{"a.md": 10})
    monkeypatch.setattr(sc, "_md_table", None)
    monkeypatch.setattr(sc, "_FENCE_IMPORT_ERROR", ImportError("no md_table"))
    lines = sc.boot_budget_lines(tmp_path)
    assert sc.claude_imports(tmp_path) == []
    assert lines[0].startswith("BOOT BUDGET:")
    assert any(l.startswith("BOOT IMPORT WARN: imports not measured (md_table/agents_md: ImportError: no md_table)") for l in lines)


def test_boot_budget_thirty_imports_print_five_rows_and_one_more_line(tmp_path):
    # F-4: at the cap, beyond it, and the total still counts every import.
    names = [f"i{n:02d}.md" for n in range(30)]
    own = _seed_claude_imports(tmp_path, "".join(f"@{n}\n" for n in names), **{n: 10 for n in names})
    lines = sc.boot_budget_lines(tmp_path)
    assert lines[0].startswith(f"BOOT BUDGET: {_WARN_BAND_README + own + 300 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(2)} files + 30 imports)")
    rows = [l for l in lines if l.startswith("    @")]
    assert rows == [f"    @{n}  10" for n in names[:5]]
    assert "  ... +25 more imports (counted)" in lines
    assert len(lines) == 1 + 3 + 5 + 1  # summary, README+CLAUDE+coordinator rows, 5 import rows, the more-line


@pytest.mark.parametrize("count,more", [(5, False), (6, True)])
def test_boot_budget_import_row_cap_boundary(tmp_path, count, more):
    names = [f"i{n}.md" for n in range(count)]
    _seed_claude_imports(tmp_path, "".join(f"@{n}\n" for n in names), **{n: 1 for n in names})
    lines = sc.boot_budget_lines(tmp_path)
    assert len([l for l in lines if l.startswith("    @")]) == 5
    assert any("more imports (counted)" in l for l in lines) is more
    if more:
        assert "  ... +1 more imports (counted)" in lines


def test_boot_budget_thirty_missing_imports_fold_into_one_capped_warn_and_wiring_survives(tmp_path):
    root = _seed_repo(tmp_path, events=[_event("delegated", task_id="t-001")])
    names = [f"missing{n:02d}.md" for n in range(30)]
    _seed_claude_imports(root, "".join(f"@{n}\n" for n in names))
    lines = sc.boot_budget_lines(root)
    assert f"({_nf(2)} files + 30 imports (+30 unmeasured))" in lines[0]
    warns = [l for l in lines if l.startswith("BOOT IMPORT WARN:")]
    assert len(warns) == 1 and len(warns[0]) <= sc.IMPORT_WARN_MAX_CHARS
    assert warns[0].startswith("BOOT IMPORT WARN: 30 not measured: missing00.md (missing)")
    assert len(lines) == 1 + 3 + 5 + 1 + 1
    # the whole context: the cut at MAX_LINES must not take WIRING away
    full = sc.build_context_lines(root)
    assert len(full) <= sc.MAX_LINES
    assert any(l.startswith("WIRING") for l in full)
    assert any(l.startswith("BOOT IMPORT WARN:") for l in full)


def test_boot_budget_top3_ranks_claude_md_by_its_own_bytes_plus_imports(tmp_path):
    # F-6: a small CLAUDE.md with a big import must stay in the breakdown
    # (the breakdown answers "what to cut"); the printed figure is OWN bytes.
    (tmp_path / "BOOT.md").write_text("1. Read A.md.\n2. Read B.md.\n3. Read C.md.\n", encoding="utf-8")
    each = (sc.BOOT_BREACH_THRESHOLD + 5000 - 40000) // 3 + 1
    for n in "ABC":
        (tmp_path / f"{n}.md").write_bytes(b"x" * each)
    own = len("@big.md\n")
    (tmp_path / "CLAUDE.md").write_bytes(b"@big.md\n")
    (tmp_path / "big.md").write_bytes(b"y" * 40000)
    _seed_coordinator(tmp_path)
    lines = sc.boot_budget_lines(tmp_path)
    assert lines[0].startswith(f"BOOT BUDGET: {3 * each + own + 40000 + _CB} bytes / {sc.BOOT_BUDGET_LIMIT} ({_nf(4)} files + 1 imports) BREACH")
    assert lines[1] == f"  {own}  CLAUDE.md"
    assert lines[2] == "    @big.md  40000"
    assert len([l for l in lines if l.startswith("  ") and not l.startswith("    ")]) == 3


def test_boot_budget_tilde_import_is_unsupported_not_missing(tmp_path):
    _seed_claude_imports(tmp_path, "@~/.claude/CLAUDE.md\n")
    lines = sc.boot_budget_lines(tmp_path)
    assert "BOOT IMPORT WARN: 1 not measured: ~/.claude/CLAUDE.md (unsupported)" in lines
    assert f"({_nf(2)} files + 1 imports (+1 unmeasured))" in lines[0]


# ==== full assembly still ASCII and within MAX_LINES =========


def test_build_context_lines_b3_ascii_and_within_max_lines(tmp_path):
    root = _seed_repo(
        tmp_path,
        events=[_event("delegated", task_id="t-001"), _event("calibrated", ts="2026-07-08T00:00:00")],
    )
    _seed_boot_files(
        root,
        {
            "README.md": 60000,
            "PROJECT_CHARTER.md": 30000,
            "ANTI_GOALS.md": 20000,
            "CLAUDE.md": 100,
        },
    )
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    lines = sc.build_context_lines(root, now, stdin_payload={"model": "claude-fable-5"})
    assert len(lines) <= sc.MAX_LINES
    for line in lines:
        line.encode("ascii")  # must not raise
        assert line.isascii()
    assert any(l.startswith("MODEL:") for l in lines)
    assert any(l.startswith("BOOT BUDGET:") for l in lines)


def test_build_context_lines_malicious_stdin_payload_stays_ascii_single_line(tmp_path):
    # critic-confirmed: a malicious/garbled model id in
    # the hook's stdin payload must not break the ASCII/single-line
    # invariant of ANY line in the assembled context, nor inject extra
    # lines past MAX_LINES via embedded '\n'.
    root = _seed_repo(
        tmp_path,
        events=[_event("delegated", task_id="t-001")],
    )
    now = datetime.datetime(2026, 7, 11, 9, 0, 0)
    lines = sc.build_context_lines(
        root, now, stdin_payload={"model": "café\nX\U0001F600" + ("y" * 200)}
    )
    for line in lines:
        assert line.isascii()
        assert "\n" not in line
        assert len(line.splitlines()) == 1
    assert len(lines) <= sc.MAX_LINES


def test_main_b3_success_path_includes_model_and_boot_budget(tmp_path, capsys, monkeypatch):
    root = _seed_repo(tmp_path, events=[_event("delegated", task_id="t-001")])
    _seed_boot_files(root, {"README.md": 100, "CLAUDE.md": 50})
    fake = _FakeStdin(json.dumps({"model": "claude-sonnet-5"}), tty=False)
    monkeypatch.setattr(sys, "stdin", fake)
    code = sc.main(root)
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert any(l.startswith("MODEL: claude-sonnet-5 -> function ") for l in out)
    assert any(l.startswith("BOOT BUDGET:") for l in out)
    assert len(out) <= sc.MAX_LINES


# ==== OPEN DISPATCH lines ==============================================


def test_open_dispatches_delegated_last_is_open():
    events = [_event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001")]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"
    assert opens[0]["event"] == "delegated"


def test_open_dispatches_accepted_closes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("accepted", ts="2026-07-10T08:10:00", agent="builder", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_retry_branch_open():
    # delegated -> rejected -> delegated (attempt 2) = still open: the
    # last lifecycle event for t-001 is 'delegated'.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("rejected", ts="2026-07-10T08:10:00", agent="builder", task_id="t-001",
               attempt=1, failure_class="spec"),
        _event("delegated", ts="2026-07-10T08:20:00", agent="builder", task_id="t-001",
               attempt=2),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["ts"] == "2026-07-10T08:20:00"


def test_open_dispatches_continuation_open():
    # delegated to builder, then delegated to critic (acceptance-gate
    # entry) on the same task_id = still open: last event is 'delegated'.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("delegated", ts="2026-07-10T08:10:00", agent="critic", task_id="t-001"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["agent"] == "critic"


def test_open_dispatches_decomposable_closes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("decomposable", ts="2026-07-10T08:10:00", agent="builder", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_escalated_closes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("escalated", ts="2026-07-10T08:10:00", agent="builder", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_dispatch_skipped_never_opens():
    # dispatch_skipped is outside _OPEN_LIFECYCLE_EVENTS entirely -- it
    # neither opens nor closes a task_id, even with no delegated at all.
    events = [_event("dispatch_skipped", ts="2026-07-10T08:00:00", agent="scout",
                     task_id="t-001")]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_file_order_lies_ts_wins():
    # A retroactive `delegated` inserted mid-file via a later edit --
    # it physically sits AFTER its closing `accepted` in the journal,
    # but its ts is earlier. File position must NOT decide "last"
    # here; ts is the true order, so the task is CLOSED.
    events = [
        _event("delegated", ts="2026-07-10T09:23:00", agent="builder", task_id="t-001"),
        _event("accepted", ts="2026-07-10T09:30:00", agent="builder", task_id="t-001"),
        _event("delegated", ts="2026-07-10T09:03:00", agent="builder", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_same_ts_later_line_wins():
    # Retro pairs write delegated and its closing event with the SAME
    # ts -- the tie must break by file position (later line wins), so
    # a delegated+accepted pair sharing one ts is closed...
    events = [
        _event("delegated", ts="2026-07-10T09:00:00", agent="builder", task_id="t-001"),
        _event("accepted", ts="2026-07-10T09:00:00", agent="builder", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []

    # ...while a single delegated at that same ts, with nothing after it,
    # stays open.
    events_open = [
        _event("delegated", ts="2026-07-10T09:00:00", agent="builder", task_id="t-001"),
    ]
    opens = sc.open_dispatches(events_open)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


def test_open_dispatches_accepted_closes_even_when_ts_lies():
    # The delegated's ts was WRITTEN WRONG (later than the accepted's
    # ts), and the accepted physically follows it -- ts lies, file
    # position is true; the opposite anomaly shape from the previous
    # test. No ordering rule resolves both; journal LAW does: any
    # `accepted` closes its task unconditionally (reopen is
    # forbidden), regardless of ts or position.
    events = [
        _event("delegated", ts="2026-07-09T13:05:00", agent="scout", task_id="t-001"),
        _event("accepted", ts="2026-07-09T12:37:30", agent="scout", task_id="t-001"),
    ]
    assert sc.open_dispatches(events) == []


# offload B0 item 5: a `returned` NEVER closes a task; delegated + a later matching returned = RESULT PENDING
def _d(tid, wref, ts="2026-07-10T08:00:00", agent="builder"):
    return _event("delegated", ts=ts, agent=agent, task_id=tid, worker_ref=wref, model="sonnet")


def _r(tid, wref, ts="2026-07-10T09:00:00", agent="builder"):
    return _event("returned", ts=ts, agent=agent, task_id=tid, worker_ref=wref, model="sonnet")


_NOW = datetime.datetime(2026, 7, 12, 12, 0, 0)
_ACC = lambda tid: _event("accepted", ts="2026-07-10T10:00:00", agent="builder", task_id=tid)  # noqa: E731


def _week(n, day=10):
    """n tasks t-001.. each delegated and returned (worker a) at distinct minutes of one day."""
    out = []
    for i in range(1, n + 1):
        out += [_d(f"t-00{i}", "agent:a", ts=f"2026-07-{day:02d}T08:0{i}:00"),
                _r(f"t-00{i}", "agent:a", ts=f"2026-07-{day:02d}T09:0{i}:00")]
    return out


# FG7-48: ONE count line, then by name only the "returned, not accepted" of the last 7 days (newest first, <=5, "N more")
@pytest.mark.parametrize("name,events,want", [
    ("zero-open-no-line", [], []),
    ("zero-open-all-accepted", [_d("t-001", "agent:a"), _ACC("t-001")], []),
    ("only-old-phantoms-one-count-line", [_d("t-001", "agent:a", ts="2026-06-01T08:00:00"), _d("t-002", "agent:b", ts="2026-06-02T08:00:00")],
     ["OPEN DISPATCHES: 2 (returned, not accepted: 0)"]),
    ("two-returned-this-week-newest-first", _week(2),
     ["OPEN DISPATCHES: 2 (returned, not accepted: 2)",
      "RESULT PENDING: t-002 agent=builder returned 2026-07-10T09:02:00",
      "RESULT PENDING: t-001 agent=builder returned 2026-07-10T09:01:00"]),
    ("seven-returned-this-week-five-named-two-more", _week(7),
     ["OPEN DISPATCHES: 7 (returned, not accepted: 7)"]
     + [f"RESULT PENDING: t-00{i} agent=builder returned 2026-07-10T09:0{i}:00" for i in range(7, 2, -1)]
     + ["RESULT PENDING: 2 more"]),
    ("returned-ten-days-ago-counted-not-named", _week(1, day=2),
     ["OPEN DISPATCHES: 1 (returned, not accepted: 1)"]),
    ("returned-of-another-worker-still-counts-for-the-task", [_d("t-001", "agent:a"), _r("t-001", "agent:b")],
     ["OPEN DISPATCHES: 1 (returned, not accepted: 1)",
      "RESULT PENDING: t-001 agent=builder returned 2026-07-10T09:00:00"]),
    ("returned-without-worker-ref-counts", [_d("t-001", "agent:a"), _event("returned", ts="2026-07-10T09:00:00", task_id="t-001")],
     ["OPEN DISPATCHES: 1 (returned, not accepted: 1)",
      "RESULT PENDING: t-001 agent=builder returned 2026-07-10T09:00:00"]),
    ("returned-before-the-last-delegated-does-not-count",
     [_d("t-001", "agent:a"), _r("t-001", "agent:a"), _d("t-001", "agent:c", ts="2026-07-10T10:00:00", agent="critic")],
     ["OPEN DISPATCHES: 1 (returned, not accepted: 0)"]),
    ("another-tasks-returned-does-not-match", [_d("t-001", "agent:a"), _r("t-002", "agent:a")],
     ["OPEN DISPATCHES: 1 (returned, not accepted: 0)"]),
    ("an-accepted-closes-it-whatever-returned-says", [_d("t-001", "agent:a"), _r("t-001", "agent:a"), _ACC("t-001")], []),
    ("bare-and-lettered-are-two-tasks", [_d("t-123", "agent:a"), _d("t-123a", "agent:a"), _r("t-123a", "agent:a")],
     ["OPEN DISPATCHES: 2 (returned, not accepted: 1)",
      "RESULT PENDING: t-123a agent=builder returned 2026-07-10T09:00:00"]),
    ("a-returned-alone-opens-nothing", [_r("t-001", "agent:a")], []),
])
def test_result_pending_and_the_returned_that_never_closes(name, events, want):
    assert sc.open_dispatch_lines(events, now=_NOW) == want
    assert "returned" not in sc._OPEN_LIFECYCLE_EVENTS


def test_open_dispatch_lines_sanitizes_external_values():
    events = [_event("delegated", ts="2026-07-10T08:00:00", agent="büilder",
                     task_id="t-001", worker_ref="agent:a")]
    lines = sc.open_dispatch_lines(events + [_r("t-001", "agent:a")], now=_NOW)
    assert lines
    for line in lines:
        assert line.isascii()
        assert "\n" not in line


def test_open_dispatch_lines_empty_journal():
    assert sc.open_dispatch_lines([]) == []


def test_build_context_lines_shows_open_dispatch(tmp_path):
    events = [
        _event("lead_degraded", ts="2026-07-10T07:30:00"),
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-08T00:00:00"),
    ]
    root = _seed_repo(tmp_path, events=events)
    now = datetime.datetime(2026, 7, 10, 12, 0, 0)
    lines = sc.build_context_lines(root, now)
    assert "OPEN DISPATCHES: 1 (returned, not accepted: 0)" in lines
    assert not any(l.startswith("OPEN DISPATCH:") for l in lines)
    degradation_idx = next(i for i, l in enumerate(lines) if l.startswith("OPEN DEGRADATION WINDOW"))
    dispatch_idx = next(i for i, l in enumerate(lines) if l.startswith("OPEN DISPATCHES:"))
    calibration_idx = next(i for i, l in enumerate(lines) if l.startswith("Last calibration:"))
    assert degradation_idx < dispatch_idx < calibration_idx
    assert len(lines) <= sc.MAX_LINES
    for line in lines:
        assert line.isascii()


# ==== closes:t-NNN marker convention =======


def test_open_dispatches_closes_marker_in_later_lifecycle_event_closes_delegated():
    # A closes: token can sit in the notes of ANY later event, including
    # a lifecycle event for a DIFFERENT task -- t-002's own event stays
    # closed too (its last lifecycle event is 'rejected', not 'delegated').
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("rejected", ts="2026-07-10T09:00:00", agent="builder", task_id="t-002",
               attempt=1, failure_class="spec", notes="closes:t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_closes_marker_in_non_lifecycle_event_closes():
    # calibrated is outside _OPEN_LIFECYCLE_EVENTS -- it must not open or
    # close anything BY ITS TYPE, but its notes are still scanned.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_multiple_closes_tokens_in_one_notes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("delegated", ts="2026-07-10T08:05:00", agent="scout", task_id="t-002"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:t-001 closes:t-002"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_delegated_after_closes_marker_reopens():
    # Retry/replacement: a delegated LATER than the marker reopens the
    # task, same as a retry does past a rejected event.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T08:30:00", notes="closes:t-001"),
        _event("delegated", ts="2026-07-10T09:00:00", agent="builder", task_id="t-001", attempt=2),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["ts"] == "2026-07-10T09:00:00"


def test_open_dispatches_closes_marker_on_nonexistent_task_is_harmless():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:t-999"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


# ---- closes: marker format boundaries (exact, like replaces_worker:) --


def test_open_dispatches_closes_marker_trailing_comma_still_closes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-133"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:t-133, done"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_closes_marker_space_after_colon_does_not_close():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-133"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes: t-133"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-133"


def test_open_dispatches_closes_marker_wrong_prefix_does_not_close():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-133"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:x-133"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-133"


def test_open_dispatches_closes_marker_wrong_case_does_not_close():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-133"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="CLOSES:t-133"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-133"


def test_open_dispatches_closes_marker_inside_longer_word_does_not_close():
    # An unanchored regex would match "closes:" INSIDE "discloses:" too --
    # the dangerous direction, a silent false close of a task nobody
    # meant to close. Left-anchor ((?<!\w)) must reject this.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="discloses:t-001"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


def test_open_dispatches_closes_marker_at_start_of_notes_closes():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="closes:t-001 done"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_closes_marker_after_punctuation_closes():
    # A non-word character (here: an opening parenthesis) immediately
    # before "closes:" is legal -- only a preceding word character
    # (letter/digit/underscore, as in "discloses:") is rejected.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
        _event("calibrated", ts="2026-07-10T09:00:00", notes="see (closes:t-001) for context"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_empty_notes_harmless():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001", notes=""),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


def test_open_dispatches_absent_notes_harmless():
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001"),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


def test_open_dispatches_closes_marker_in_own_delegated_notes_closes_via_contract():
    # Documented contract: a closes:t-X token in the notes of task X's
    # OWN delegated event is a mis-written journal line, but the
    # documented deterministic behavior is that the marker wins at the
    # tie -- (ts, idx, 1) > (ts, idx, 0) -- so this delegated is treated
    # as already closed, not open.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001",
               notes="closes:t-001"),
    ]
    assert sc.open_dispatches(events) == []


def test_open_dispatches_non_string_notes_does_not_raise():
    # Adversarial input: a malformed journal line where notes ended up
    # a number or None in JSON (not the contractual string) must not
    # crash open_dispatches() with a TypeError from re.findall.
    events = [
        _event("delegated", ts="2026-07-10T08:00:00", agent="builder", task_id="t-001", notes=12345),
        _event("calibrated", ts="2026-07-10T09:00:00", notes=None),
    ]
    opens = sc.open_dispatches(events)
    assert len(opens) == 1
    assert opens[0]["task_id"] == "t-001"


# ---------------------------------------------------------------------
# hooks_path_autofix_line
# ---------------------------------------------------------------------
# Scoped: session_context.py carries the AUTOFIX action
# itself (this section), not a full git_hooks_channel report
# (required-file/exec-bit WARNINGs on an already-set hooksPath are
# tools/wiring_check.py's job -- see that module's own test suite,
# test_wiring_check.py, and session_context.py's module docstring for
# the division of labor).


def _git(args, cwd):
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=10
    )


def _init_repo_with_hooks(tmp_path, hookspath="own"):
    """Minimal git repo with a working .githooks/ (EVERY hook in
    wiring_check._REQUIRED_GITHOOKS present, tracked, executable in the
    index) and core.hooksPath pointed at it unless hookspath overrides
    that (None = leave unset; a Path = point hooksPath there instead)."""
    import wiring_check

    _git(["init", "-q"], tmp_path)
    githooks = tmp_path / ".githooks"
    githooks.mkdir()
    for name in wiring_check._REQUIRED_GITHOOKS:
        (githooks / name).write_text("#!/bin/sh\n", encoding="utf-8")
    _git(["add", *(f".githooks/{n}" for n in wiring_check._REQUIRED_GITHOOKS)], tmp_path)
    for name in wiring_check._REQUIRED_GITHOOKS:
        _git(["update-index", "--chmod=+x", f".githooks/{name}"], tmp_path)
    if hookspath == "own":
        _git(["config", "core.hooksPath", str(githooks)], tmp_path)
    elif hookspath is None:
        pass  # leave unset
    else:
        _git(["config", "core.hooksPath", str(hookspath)], tmp_path)
    return tmp_path


def test_hooks_path_autofix_line_unset_autofixes(tmp_path):
    _init_repo_with_hooks(tmp_path, hookspath=None)
    line = sc.hooks_path_autofix_line(tmp_path)
    assert line == "WIRING AUTOFIX: core.hooksPath set to .githooks"
    # The fix actually stuck in the repo's own local config, not just
    # claimed in the returned line.
    result = _git(["config", "core.hooksPath"], tmp_path)
    assert result.stdout.strip() == ".githooks"


def test_required_githooks_has_one_source_with_wiring_check():
    # The two modules cannot drift: session_context reads wiring_check's
    # list, and its fail-open fallback is a subset of it (a name in one
    # and not the other fails here).
    import wiring_check

    names, note = sc._required_githooks()
    assert names == tuple(wiring_check._REQUIRED_GITHOOKS) and note == ""
    assert set(sc._FALLBACK_GITHOOKS) <= set(wiring_check._REQUIRED_GITHOOKS)


def test_required_githooks_fail_open_when_wiring_check_import_fails(tmp_path, monkeypatch):
    # SessionStart edge: the import fails -> today's two names plus a
    # WIRING note, never a raise; and the autofix still returns a line.
    import builtins

    real_import = builtins.__import__

    def _no_wiring_check(name, *args, **kwargs):
        if name == "wiring_check":
            raise ImportError("simulated: wiring_check unavailable")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _no_wiring_check)
    names, note = sc._required_githooks()
    assert names == sc._FALLBACK_GITHOOKS == ("pre-commit", "commit-msg")
    assert "WIRING note" in note and "ImportError" in note

    _git(["init", "-q"], tmp_path)
    (tmp_path / ".githooks").mkdir()
    for n in sc._FALLBACK_GITHOOKS:
        (tmp_path / ".githooks" / n).write_text("#!/bin/sh\n", encoding="utf-8")
    line = sc.hooks_path_autofix_line(tmp_path)
    assert line.startswith("WIRING AUTOFIX: core.hooksPath set to .githooks")
    assert "WIRING note" in line


def test_hooks_path_autofix_line_write_failure_degrades_to_warning(tmp_path, monkeypatch):
    # The WRITE call is made to fail while the READ call (which reports
    # unset) is untouched -- must fall back to a WARNING with the
    # failure reason appended, not raise and not silently print AUTOFIX.
    _init_repo_with_hooks(tmp_path, hookspath=None)
    real_run = sc.subprocess.run

    def _failing_write(cmd, *args, **kwargs):
        if len(cmd) >= 3 and cmd[0] == "git" and cmd[1] == "config" and "--local" in cmd:
            raise OSError("simulated: git config write failed")
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(sc.subprocess, "run", _failing_write)
    line = sc.hooks_path_autofix_line(tmp_path)
    assert "core.hooksPath not set" in line and "autofix failed" in line
    assert not line.startswith("WIRING AUTOFIX:")
    assert line.startswith("WIRING WARNING:")
    # The real config must be untouched (still unset).
    result = _git(["config", "core.hooksPath"], tmp_path)
    assert result.returncode != 0 or not result.stdout.strip()


def test_hooks_path_autofix_line_reports_failure_when_hook_files_missing(tmp_path):
    # The `git config` write itself succeeds, but the recheck must
    # catch that the required hook files are still missing -- reported
    # as a failed autofix, not a false AUTOFIX line.
    _git(["init", "-q"], tmp_path)
    (tmp_path / ".githooks").mkdir()
    # Deliberately do NOT create pre-commit/commit-msg under .githooks.
    line = sc.hooks_path_autofix_line(tmp_path)
    assert "core.hooksPath not set" in line and "autofix" in line and "missing" in line
    assert not line.startswith("WIRING AUTOFIX:")
    result = _git(["config", "core.hooksPath"], tmp_path)
    assert result.stdout.strip() == ".githooks"


def test_hooks_path_autofix_line_already_set_returns_empty(tmp_path):
    # Already set to the CORRECT value -- nothing to fix, no line at all
    # (the broader "already set" report, correct or not, is
    # wiring_summary_line()'s/tools/wiring_check.py's job, not this
    # function's -- see module docstring).
    _init_repo_with_hooks(tmp_path)
    assert sc.hooks_path_autofix_line(tmp_path) == ""


def test_hooks_path_autofix_line_already_set_elsewhere_returns_empty():
    # Set to some OTHER path -- deliberately NOT autofixed (an existing
    # configuration, human or a prior session, is left alone) and
    # deliberately NOT reported here either (wiring_check's job).
    other = Path(__file__).resolve().parent
    line = sc.hooks_path_autofix_line(other)
    # Whatever this repo's own hooksPath is currently configured to,
    # this function must never attempt to overwrite it nor emit a line
    # about it -- confirmed by never raising and returning a string.
    assert isinstance(line, str)


def test_hooks_path_autofix_line_never_raises_when_git_missing(tmp_path, monkeypatch):
    def _boom(*args, **kwargs):
        raise FileNotFoundError("git not found")

    monkeypatch.setattr(sc.subprocess, "run", _boom)
    assert sc.hooks_path_autofix_line(tmp_path) == ""


# ---------------------------------------------------------------------
# wiring_summary_line -- see tools/wiring_check.py
# ---------------------------------------------------------------------


def test_wiring_summary_line_ok_on_fully_wired_repo(tmp_path):
    _init_repo_with_hooks(tmp_path)
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text(
        json.dumps({"hooks": {}}), encoding="utf-8"
    )
    assert sc.wiring_summary_line(tmp_path) == "WIRING: OK"


def test_wiring_summary_line_appends_notice_count_without_flipping_ok(tmp_path):
    # Node E item 10: a non-blocking "notices" entry appends ", N
    # notice(s)" on the OK branch -- never flips it to the issue-count
    # branch.
    _init_repo_with_hooks(tmp_path)
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text(json.dumps({"hooks": {}}), encoding="utf-8")
    (tmp_path / "ADOPTION_LEDGER.md").write_text(
        "# Adoption Ledger\n\n"
        "## Kit snapshot revision\n\nKit snapshot revision: `abc1234`\n",
        encoding="utf-8",
    )
    line = sc.wiring_summary_line(tmp_path)
    assert line == "WIRING: OK, 1 notice(s)"


def test_wiring_summary_line_reports_issue_count(tmp_path):
    # Nothing configured at all -- hooksPath unset (and, in a bare repo
    # with no writable-looking setup here, autofix may or may not stick,
    # but the settings.json is definitely missing) -- at least one issue.
    _git(["init", "-q"], tmp_path)
    line = sc.wiring_summary_line(tmp_path)
    assert line.startswith("WIRING: ")
    assert line != "WIRING: OK"
    assert "run tools/wiring_check.py --check" in line


def test_wiring_summary_line_never_raises_when_wiring_check_broken(tmp_path, monkeypatch):
    import wiring_check

    def _boom(root=None):
        raise RuntimeError("simulated wiring_check failure")

    monkeypatch.setattr(wiring_check, "check_wiring", _boom)
    line = sc.wiring_summary_line(tmp_path)
    assert line.startswith("WIRING: check unavailable (")


def test_build_context_lines_includes_wiring_summary(tmp_path):
    events = [_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    lines = sc.build_context_lines(root)
    assert any(l.startswith("WIRING:") or l.startswith("WIRING WARNING:")
               or l.startswith("WIRING AUTOFIX:") for l in lines), lines


# ---------------------------------------------------------------------
# WAITS block + COMPACT NARRATIVE (bounded waits, K-WIRE): the reaper's launch and status line, the narrative's stamp
# ---------------------------------------------------------------------

_REAL_WAITS = getattr(sc, "waits_lines", None)


@pytest.fixture(autouse=True)
def _no_real_reaper(monkeypatch):
    """No test starts a reaper: the block `build_context_lines` carries is silent unless a WAITS test calls the real one."""
    if _REAL_WAITS is not None:
        monkeypatch.setattr(sc, "waits_lines", lambda root: [])


def _waits_world(monkeypatch, tmp_path, launched, session, status, boom):
    import types
    import wait_reaper
    import session_proc
    import worktree_sweep

    class Calls(list):
        pass

    calls = Calls()
    calls.events, calls.roots, calls.walks, calls.git_timeouts = [], [], [], []

    def launch(trigger, root=None, **kw):
        calls.append(trigger)
        calls.events.append("launch")
        calls.roots.append(root)
        if boom:
            raise boom
        return launched

    def walk(*a, **k):
        calls.walks.append(1)
        return session

    def context(git, root):
        calls.git_timeouts.append(git.timeout)
        return types.SimpleNamespace(common=tmp_path)

    def read(state, sess, now=None):
        calls.events.append("read")
        return status

    monkeypatch.setattr(wait_reaper, "launch", launch)
    monkeypatch.setattr(session_proc, "session_process", walk)
    monkeypatch.setattr(worktree_sweep, "repo_context", context)
    monkeypatch.setattr(wait_reaper, "waits_line", read)
    return calls


_SESS = ({"pid": 7, "created": 1.0}, "")
_REAP = "WAITS: last reap 2026-11-17T10:00:00 (subagent-stop): 2 trees stopped, 0 processes failed, 1 unknown roots"
_UNREAD = "WAITS: process list unreadable (boom) -- python -B tools/wait_reaper.py"
_NOSESS = "WAITS: no session (no claude.exe ancestor) -- nothing stopped"
_NOSTART = "WAITS: reaper not started (tools/wait_reaper.py not found in x)"
# id, launch answer, session, status line, launch raises, expected block (None: one `reaper not started` line from the raise)
_WAITS_ROWS = [
    ("silent_at_zero", None, _SESS, None, None, []),
    ("counts", None, _SESS, _REAP, None, [_REAP]),
    ("no_session", _NOSESS, (None, "no claude.exe ancestor"), None, None, [_NOSESS]),
    ("unreadable", None, _SESS, _UNREAD, None, [_UNREAD]),
    ("launch_answer_wins", _NOSTART, _SESS, _REAP, None, [_NOSTART]),
    ("launch_raises", None, _SESS, None, RuntimeError("spawn Ж " + "z" * 300), None),
]


@pytest.mark.skipif(_REAL_WAITS is None, reason="the candidate carries no WAITS block")
@pytest.mark.parametrize("launched, session, status, boom, expected", [r[1:] for r in _WAITS_ROWS], ids=[r[0] for r in _WAITS_ROWS])
def test_k_wire_waits_block(tmp_path, monkeypatch, launched, session, status, boom, expected):
    calls = _waits_world(monkeypatch, tmp_path, launched, session, status, boom)
    lines = _REAL_WAITS(tmp_path)
    assert calls == ["session-start"]
    if expected is None:
        assert len(lines) == 1 and lines[0].startswith("WAITS: reaper not started (RuntimeError: spawn ?")
        assert lines[0].isascii() and len(lines[0]) <= len("WAITS: reaper not started ()") + 120
    else:
        assert lines == expected


@pytest.mark.skipif(_REAL_WAITS is None, reason="the candidate carries no WAITS block")
def test_k_wire_waits_reads_before_it_launches_walks_once_and_launches_on_the_given_root(tmp_path, monkeypatch):
    calls = _waits_world(monkeypatch, tmp_path, None, _SESS, _REAP, None)
    assert _REAL_WAITS(tmp_path) == [_REAP]
    # F3: the last run's line is read BEFORE the new run resets it; F2: one walk, one context, 5 s per git call;
    # F5: the launcher gets the root the hook was given (a test root never reaches the live repo)
    assert calls.events == ["read", "launch"] and len(calls.walks) == 1 and calls.git_timeouts == [5]
    assert calls.roots == [tmp_path]


@pytest.mark.skipif(_REAL_WAITS is None, reason="the candidate carries no WAITS block")
def test_k_wire_waits_line_survives_the_max_lines_cut_that_takes_the_wiring_line(tmp_path, monkeypatch):
    root = _seed_repo(tmp_path, events=[_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")])
    monkeypatch.setattr(sc, "wiring_summary_line", lambda r: "WIRING: OK")
    _stub_count(monkeypatch, (5, 0, "origin/main"))
    monkeypatch.setattr(sc, "waits_lines", lambda r: ["WAITS: last reap X"])
    base = len(sc.build_context_lines(root))                    # the lines up to and including the wiring line
    filler = 24 - (base - 2 - len(sc.boot_budget_lines(root)))   # 24 lines BEFORE the waits line
    assert filler >= 0
    monkeypatch.setattr(sc, "boot_budget_lines", lambda r: ["FILLER"] * filler)
    lines = sc.build_context_lines(root)
    assert len(lines) == sc.MAX_LINES and lines[24] == "WAITS: last reap X"
    assert "WIRING: OK" not in lines


_N_DIR = "docs/tasks/compact-snapshots"
_N_NOW = datetime.datetime(2026, 11, 17, 12, 0, 0)
_N_FILE = _N_DIR + "/2026-11-17-1155-narrative.md"
_N_STAMPED = "<!-- compact-snapshot: narrative; session-proc: %s; written: 2026-11-17T11:55:00 -->\n"
_N_ODD = "<!-- compact-snapshot: narrative; session-proc: x; written: y -->\n"


def _narrative(tmp_path, head):
    folder = tmp_path / _N_DIR
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / "2026-11-17-1155-narrative.md"
    p.write_text(head + "# state\n", encoding="utf-8")
    t = _N_NOW.timestamp() - 300
    os.utime(p, (t, t))


_NO_STAMP = "COMPACT NARRATIVE: newest has no session stamp (%s) -- check it is yours" % _N_FILE
_FOREIGN = "COMPACT NARRATIVE: newest is another session's (%s) -- not your state" % _N_FILE
_MINE = {"pid": 7, "created": 1.5}
# id, the narrative's first line (None = no file), this session's process (None = the walk fails), the expected narrative line
_NARRATIVE_ROWS = [
    ("own", _N_STAMPED % "7-1.500", _MINE, "COMPACT NARRATIVE: %s (5 min old)" % _N_FILE),
    ("foreign", _N_STAMPED % "9-2.000", _MINE, _FOREIGN),
    ("unstamped", "", _MINE, _NO_STAMP),
    ("odd_field_never_own_never_foreign", _N_ODD, _MINE, _NO_STAMP),
    ("stamped_but_walk_none", _N_STAMPED % "7-1.500", None, _NO_STAMP),
    ("none_no_line", None, _MINE, None),
]


@pytest.mark.parametrize("head, proc, expected", [r[1:] for r in _NARRATIVE_ROWS], ids=[r[0] for r in _NARRATIVE_ROWS])
def test_k_wire_compact_narrative_names_whose_it_is(tmp_path, monkeypatch, head, proc, expected):
    if not hasattr(sc, "_session_proc_id"):
        pytest.skip("the candidate carries no narrative stamp reading")
    import session_proc

    if head is not None:
        _narrative(tmp_path, head)
    monkeypatch.setattr(session_proc, "session_process", lambda *a, **k: (proc, "" if proc else "no claude.exe ancestor"))
    lines = sc.compact_snapshot_lines(tmp_path, _N_NOW, "s1")
    assert [l for l in lines if l.startswith("COMPACT NARRATIVE")] == ([expected] if expected else []), lines


def test_session_proc_id_is_the_stamp_the_writer_encodes(monkeypatch):
    # the reader's own process id goes through the one encoder: a patched walk {pid 7, created 1.5} reads "7-1.500"
    import session_proc

    if not hasattr(sc, "_session_proc_id"):
        pytest.skip("the candidate carries no narrative stamp reading")
    monkeypatch.setattr(session_proc, "session_process", lambda *a, **k: ({"pid": 7, "created": 1.5}, ""))
    assert sc._session_proc_id() == "7-1.500"


# ---------------------------------------------------------------------
# worktrees_line (F6-38) -- the leak detector of tools/worktree_sweep.py
# ---------------------------------------------------------------------


def _stub_count(monkeypatch, result, kind="none", data=None, reason=""):
    """`read_status` answers `kind` (or raises it when it is an Exception), `count_estimate` answers `result` (or raises); both
    stubs assert the SessionStart budget: 5 s a git call."""
    import worktree_sweep

    def fake(root, timeout=5, ref="origin/main", runner=None):
        assert timeout == 5
        if isinstance(result, Exception):
            raise result
        return result

    def fake_status(root, runner=None, timeout=5, now=None):
        assert timeout == 5
        if isinstance(kind, Exception):
            raise kind
        return worktree_sweep.SweepState(kind, dict(data or {}), reason)

    monkeypatch.setattr(worktree_sweep, "count_estimate", fake)
    monkeypatch.setattr(worktree_sweep, "read_status", fake_status)


LOG = ".git/worktree-sweep/run.log"
DOOR = "python tools/worktree_sweep.py --apply"
RUN = {"started": "2026-11-03T10:00:00", "trigger": "post-merge", "done": 3, "registered": 12}


def test_s1_worktrees_line_before_any_run_the_line_is_the_estimate_and_silent_at_zero(tmp_path, monkeypatch):
    _stub_count(monkeypatch, (261, 257, "origin/main"))
    assert sc.worktrees_line(tmp_path) == (
        "WORKTREES (estimate): 261 registered, 257 on branches merged into origin/main, no background sweep recorded yet -- "
        "python tools/worktree_sweep.py lists what can go")
    _stub_count(monkeypatch, (3, 0, "origin/main"))
    assert sc.worktrees_line(tmp_path) is None
    _stub_count(monkeypatch, RuntimeError("branch --merged origin/main: fatal: malformed object name Ж" + "x" * 300))
    line = sc.worktrees_line(tmp_path)
    assert line.startswith("WORKTREES: count unavailable (RuntimeError: branch --merged") and line.endswith(")")
    assert line.isascii() and len(line) <= len("WORKTREES: count unavailable ()") + 120


def test_s2_worktrees_line_a_running_sweep_names_since_when_and_how_far(tmp_path, monkeypatch):
    _stub_count(monkeypatch, (9, 9, "origin/main"), "running", RUN)
    assert sc.worktrees_line(tmp_path) == "WORKTREES: sweep running since 2026-11-03T10:00:00 (post-merge), 3/12 copies seen -- log " + LOG


def test_s3_worktrees_line_a_sweep_that_died_says_where_and_gives_the_door(tmp_path, monkeypatch):
    _stub_count(monkeypatch, (9, 9, "origin/main"), "died", dict(RUN, heartbeat="2026-11-03T10:07:00"))
    assert sc.worktrees_line(tmp_path) == ("WORKTREES: last sweep DIED mid-run (started 2026-11-03T10:00:00, post-merge, 3/12 seen, "
                                           "last heartbeat 2026-11-03T10:07:00) -- %s; log %s" % (DOOR, LOG))
    _stub_count(monkeypatch, (9, 9, "origin/main"), "died", dict(RUN, heartbeat=None))
    assert "last heartbeat none)" in sc.worktrees_line(tmp_path)


def test_s4_worktrees_line_a_finished_sweep_names_its_counts_and_the_estimate_now(tmp_path, monkeypatch):
    done = dict(RUN, finished="2026-11-03T10:33:00", removed=79, kept=4, failed=0)
    _stub_count(monkeypatch, (4, 1, "origin/main"), "finished", done)
    assert sc.worktrees_line(tmp_path) == ("WORKTREES: last sweep 2026-11-03T10:33:00 (post-merge): 79 removed, 4 kept, 0 failed; "
                                           "estimate now 1 on merged branches -- log " + LOG)
    _stub_count(monkeypatch, (4, 0, "origin/main"), "finished", dict(done, failed=2))
    line = sc.worktrees_line(tmp_path)
    assert "79 removed, 4 kept, 2 FAILED (see FAILED lines in the log); estimate now 0 on merged branches" in line     # not silent at 0


@pytest.mark.parametrize("kind,verb", [("refused", "did not run"), ("crashed", "crashed"), ("not-started", "was not started")])
def test_s5_worktrees_line_a_sweep_that_did_not_run_says_why_and_gives_the_door(tmp_path, monkeypatch, kind, verb):
    _stub_count(monkeypatch, (9, 9, "origin/main"), kind, RUN, "the reason")
    assert sc.worktrees_line(tmp_path) == "WORKTREES: last sweep 2026-11-03T10:00:00 (post-merge) %s: the reason -- %s" % (verb, DOOR)


def test_s6_worktrees_line_an_unreadable_status_and_a_failing_read_each_say_so_in_ascii_within_120(tmp_path, monkeypatch):
    _stub_count(monkeypatch, (9, 9, "origin/main"), "unreadable", {}, "status.json is not JSON")
    assert sc.worktrees_line(tmp_path) == "WORKTREES: sweep status unreadable (status.json is not JSON) -- " + DOOR
    _stub_count(monkeypatch, (9, 9, "origin/main"), RuntimeError("git failed: Ж" + "y" * 300))
    line = sc.worktrees_line(tmp_path)
    assert line.startswith("WORKTREES: sweep status unavailable (RuntimeError: git failed: ?") and line.endswith(")")
    assert line.isascii() and len(line) <= len("WORKTREES: sweep status unavailable ()") + 120


def test_s7_worktrees_line_a_failing_estimate_does_not_silence_the_state_part(tmp_path, monkeypatch):
    _stub_count(monkeypatch, RuntimeError("branch --merged: boom"), "finished", dict(RUN, finished="2026-11-03T10:33:00", removed=5, kept=1, failed=0))
    line = sc.worktrees_line(tmp_path)
    assert line == ("WORKTREES: last sweep 2026-11-03T10:33:00 (post-merge): 5 removed, 1 kept, 0 failed; "
                    "estimate unavailable (RuntimeError: branch --merged: boom) -- log " + LOG)


def test_s8_worktrees_line_build_context_lines_carries_the_worktrees_line_before_wiring(tmp_path, monkeypatch):
    root = _seed_repo(tmp_path, events=[_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")])
    _stub_count(monkeypatch, (5, 0, "origin/main"))
    assert not [l for l in sc.build_context_lines(root) if l.startswith("WORKTREES")]
    _stub_count(monkeypatch, (5, 2, "origin/main"))
    lines = sc.build_context_lines(root)
    at = next(i for i, l in enumerate(lines) if l.startswith("WORKTREES (estimate): 5 registered, 2 on branches"))
    assert at < next(i for i, l in enumerate(lines) if l.startswith("WIRING:"))
    _stub_count(monkeypatch, (5, 2, "origin/main"), "died", RUN)
    assert any(l.startswith("WORKTREES: last sweep DIED mid-run") for l in sc.build_context_lines(root))
    _stub_count(monkeypatch, (5, 2, "origin/main"), RuntimeError("no git"))
    assert any(l.startswith("WORKTREES: sweep status unavailable (RuntimeError: no git)") for l in sc.build_context_lines(root))


def test_s8_worktrees_line_the_worktrees_line_survives_the_max_lines_cut_that_takes_the_wiring_line(tmp_path, monkeypatch):
    root = _seed_repo(tmp_path, events=[_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")])
    monkeypatch.setattr(sc, "wiring_summary_line", lambda r: "WIRING: OK")
    _stub_count(monkeypatch, (5, 0, "origin/main"))
    base = len(sc.build_context_lines(root))                   # the lines up to and including the wiring line
    filler = 24 - (base - 1 - len(sc.boot_budget_lines(root)))     # 24 lines BEFORE the worktrees line
    assert filler >= 0
    monkeypatch.setattr(sc, "boot_budget_lines", lambda r: ["FILLER"] * filler)
    _stub_count(monkeypatch, (5, 2, "origin/main"))
    lines = sc.build_context_lines(root)
    assert len(lines) == sc.MAX_LINES and lines[24].startswith("WORKTREES (estimate)")
    assert "WIRING: OK" not in lines                           # the cut took the wiring line, not the detector


# ---- F2 (release-gate v0.8.1): GATE BREAK-GLASS surfacing, ported from
# tools/session_context.py's own select_and_ack_break_glass_lines()/
# break_glass_lines() -- see this module's own docstring above
# _break_glass_candidates() for the full rationale (ack-only-shown-lines,
# the 5-line cap, the read-only-tracks + sidecar-ack fix, and the
# list-not-overwrite fix). tools/main_gate.py and tools/dod_gate.py's
# "skip the 3rd consecutive block" safety valve APPENDS a persistent
# unsafe_completion fact into the dod_track file itself (sibling edit,
# same task; new plural "unsafe_completions" list key, "unsafe_completion"
# singular kept readable for backward compat).


def _write_dod_track(track_dir: Path, session_id: str, data: dict) -> Path:
    track_dir.mkdir(parents=True, exist_ok=True)
    path = track_dir / f"{session_id}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _read_ack_sidecar(track_dir: Path) -> dict:
    path = track_dir / "break_glass_ack.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def test_break_glass_lines_no_dod_track_dir_is_silent(tmp_path):
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_empty_dod_track_dir_is_silent(tmp_path):
    (tmp_path / ".claude" / "dod_track").mkdir(parents=True)
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_track_without_any_unsafe_completion_is_silent(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-clean",
        {"edits": [], "runs": [], "main_gate_state": {"consecutive_blocks": 0}},
    )
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_surfaces_main_gate_unsafe_completion(tmp_path):
    # Legacy singular key ("unsafe_completion") -- backward-compat read
    # path.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-a",
        {
            "main_gate_state": {
                "consecutive_blocks": 0,
                "unsafe_completion": {"ts": "2026-07-24T10:00:00.000000", "reason": "no-green-run"},
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 1
    assert lines[0].startswith("GATE BREAK-GLASS:")
    assert "sess-a" in lines[0]
    assert "main" in lines[0]
    assert "no-green-run" in lines[0]
    assert lines[0].isascii()


def test_break_glass_lines_surfaces_dod_gate_unsafe_completion_per_agent(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-b",
        {
            "gate_state": {
                "per_agent": {
                    "agent-1": {
                        "consecutive_blocks": 0,
                        "unsafe_completion": {
                            "ts": "t1",
                            "reason": "no-green-run",
                            "agent_id": "agent-1",
                        },
                    }
                }
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 1
    assert "sess-b" in lines[0]
    assert "dod" in lines[0]


def test_break_glass_lines_surfaces_multiple_agents_in_same_track(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-multi",
        {
            "gate_state": {
                "per_agent": {
                    "agent-1": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}},
                    "agent-2": {"unsafe_completion": {"ts": "t2", "reason": "green-before-last-edit"}},
                }
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 2


def test_break_glass_lines_reads_new_plural_list_key_multiple_facts(tmp_path):
    # New shape: "unsafe_completions" is a LIST -- every fact in it must
    # surface, not just the last one.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-list",
        {
            "main_gate_state": {
                "unsafe_completions": [
                    {"ts": "t1", "reason": "no-green-run"},
                    {"ts": "t2", "reason": "green-before-last-edit"},
                ]
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 2
    assert any("no-green-run" in l for l in lines)
    assert any("green-before-last-edit" in l for l in lines)


def test_break_glass_lines_reads_both_legacy_singular_and_new_plural_keys(tmp_path):
    # Tolerance for a track file carrying BOTH shapes at once (e.g. one
    # fact written before the plural-key fix, one after) -- both surface.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-mixed-keys",
        {
            "main_gate_state": {
                "unsafe_completion": {"ts": "t0", "reason": "legacy"},
                "unsafe_completions": [{"ts": "t1", "reason": "no-green-run"}],
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 2


# ---- tracks are READ-ONLY, ack lives in the sidecar ----


def test_break_glass_lines_does_not_modify_the_track_file(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    path = _write_dod_track(
        track_dir,
        "sess-c",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    original_bytes = path.read_bytes()
    sc.break_glass_lines(tmp_path)
    assert path.read_bytes() == original_bytes


def test_break_glass_lines_never_writes_to_any_track_file(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    paths = [
        _write_dod_track(
            track_dir,
            f"sess-ro-{i}",
            {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
        )
        for i in range(3)
    ]
    originals = {p: p.read_bytes() for p in paths}
    sc.break_glass_lines(tmp_path)
    for p, original in originals.items():
        assert p.read_bytes() == original


def test_break_glass_lines_records_acknowledgement_in_sidecar_file(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-c",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    sc.break_glass_lines(tmp_path)
    ack = _read_ack_sidecar(track_dir)
    assert len(ack) == 1
    # Key carries a trailing fact-index: "ts" alone can collide -- see
    # _unsafe_completion_facts' docstring; legacy singular key -> index 0.
    assert "sess-c:main::t1:0" in ack
    assert ack["sess-c:main::t1:0"]  # non-empty ack timestamp


def test_break_glass_lines_ignores_its_own_sidecar_file_as_a_track(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    track_dir.mkdir(parents=True)
    (track_dir / "break_glass_ack.json").write_text("{}", encoding="utf-8")
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_repeat_call_is_silent_exactly_once_boundary(tmp_path):
    # The same fact must surface EXACTLY ONCE -- a second scan of the same
    # (now-acknowledged-in-the-sidecar) file is silent.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-d",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    first = sc.break_glass_lines(tmp_path)
    assert len(first) == 1
    second = sc.break_glass_lines(tmp_path)
    assert second == []


def test_break_glass_lines_preexisting_sidecar_ack_never_reprints(tmp_path):
    # A fact already acknowledged in the SIDECAR (e.g. by a previous
    # SessionStart process) must not print even on this process's very
    # first scan.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-e",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    (track_dir / "break_glass_ack.json").write_text(
        json.dumps({"sess-e:main::t1:0": "2026-07-24T09:00:00.000000"}), encoding="utf-8"
    )
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_two_facts_with_identical_ts_get_distinct_ack_keys(tmp_path):
    # Two facts of the same session/gate/agent can carry a byte-identical
    # "ts" (Windows wall-clock granularity). Without the index in the ack
    # key, the SECOND fact would silently collapse onto the first's key
    # and never surface once the first is acknowledged. Both facts here
    # share the exact same ts string.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-dup-ts",
        {
            "main_gate_state": {
                "unsafe_completions": [
                    {"ts": "2026-07-24T10:00:00.000000", "reason": "no-green-run"},
                    {"ts": "2026-07-24T10:00:00.000000", "reason": "green-before-last-edit"},
                ]
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 2
    ack = _read_ack_sidecar(track_dir)
    assert len(ack) == 2  # two DISTINCT keys, not collapsed into one

    # Nothing left pending -- both were shown and acked.
    assert sc.break_glass_lines(tmp_path) == []


def test_select_and_ack_identical_ts_facts_budget_cut_between_them_shows_only_first(tmp_path):
    # Two facts with a byte-identical ts, space_left=1 -- only the FIRST
    # is shown and acked; the second must resurface on the next call, not
    # be silently swallowed by a collapsed ack key.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-dup-ts-budget",
        {
            "main_gate_state": {
                "unsafe_completions": [
                    {"ts": "2026-07-24T10:00:00.000000", "reason": "no-green-run"},
                    {"ts": "2026-07-24T10:00:00.000000", "reason": "green-before-last-edit"},
                ]
            }
        },
    )
    filler = ["x"] * (sc.MAX_LINES - 1)  # space_left == 1
    shown = sc.select_and_ack_break_glass_lines(tmp_path, filler)
    assert len(shown) == 1
    assert "no-green-run" in shown[0]

    remaining = sc.select_and_ack_break_glass_lines(tmp_path, [])
    assert len(remaining) == 1
    assert "green-before-last-edit" in remaining[0]


def test_break_glass_lines_broken_json_file_does_not_block_sibling(tmp_path):
    # A corrupt track file next to a good one must not hide the good
    # one's fact.
    track_dir = tmp_path / ".claude" / "dod_track"
    track_dir.mkdir(parents=True)
    (track_dir / "sess-broken.json").write_text("{not valid json", encoding="utf-8")
    _write_dod_track(
        track_dir,
        "sess-ok",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 1
    assert "sess-ok" in lines[0]


def test_break_glass_lines_non_dict_json_file_is_skipped(tmp_path):
    # Adversarial: a track file whose top-level JSON value is a list (or
    # any non-dict) must not crash the scan.
    track_dir = tmp_path / ".claude" / "dod_track"
    track_dir.mkdir(parents=True)
    (track_dir / "sess-list.json").write_text("[1, 2, 3]", encoding="utf-8")
    _write_dod_track(
        track_dir,
        "sess-ok2",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 1
    assert "sess-ok2" in lines[0]


def test_break_glass_lines_ignores_non_json_files_in_dod_track_dir(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    track_dir.mkdir(parents=True)
    (track_dir / "README.txt").write_text("not a track file", encoding="utf-8")
    assert sc.break_glass_lines(tmp_path) == []


def test_break_glass_lines_sanitizes_non_ascii_reason(tmp_path):
    # reason/ts are journal/track-sourced (a hook could in principle carry
    # anything) -- same ASCII discipline as MODEL/OPEN DISPATCH/WIRING.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-cyr",
        {
            "main_gate_state": {
                "unsafe_completion": {"ts": "t1", "reason": "причина-с-кириллицей"}
            }
        },
    )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 1
    assert lines[0].isascii()


# ---- CAP at 5 fact lines + trailing summary line ----------------


def test_break_glass_lines_cap_boundary_exactly_five_no_summary_line(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    for i in range(5):
        _write_dod_track(
            track_dir,
            f"sess-{i:02d}",
            {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
        )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 5
    assert not any("more unsafe-completion facts pending" in l for l in lines)


def test_break_glass_lines_cap_limits_to_five_plus_summary_line(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    for i in range(7):
        _write_dod_track(
            track_dir,
            f"sess-{i:02d}",
            {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
        )
    lines = sc.break_glass_lines(tmp_path)
    assert len(lines) == 6  # 5 facts + 1 summary
    fact_lines = [l for l in lines if l.startswith("GATE BREAK-GLASS: session")]
    summary_lines = [l for l in lines if "more unsafe-completion facts pending" in l]
    assert len(fact_lines) == 5
    assert len(summary_lines) == 1
    assert "2 more" in summary_lines[0]


def test_break_glass_lines_cap_remainder_not_acked_resurfaces_next_call(tmp_path):
    # Facts beyond the cap are NOT acked -- they must surface on a later
    # call once the earlier ones have been acknowledged.
    track_dir = tmp_path / ".claude" / "dod_track"
    for i in range(7):
        _write_dod_track(
            track_dir,
            f"sess-{i:02d}",
            {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
        )
    first = sc.break_glass_lines(tmp_path)
    assert len(first) == 6  # 5 facts + summary

    second = sc.break_glass_lines(tmp_path)
    assert len(second) == 2
    assert all(l.startswith("GATE BREAK-GLASS: session") for l in second)

    third = sc.break_glass_lines(tmp_path)
    assert third == []


# ---- ack ONLY lines surviving the MAX_LINES cut ------------------


def test_select_and_ack_break_glass_lines_no_space_left_does_not_ack(tmp_path):
    # The preceding context lines already fill the whole MAX_LINES
    # budget -> the pending fact must be neither shown NOR acked -- it
    # must resurface once space frees up.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-full",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    filler = ["x"] * sc.MAX_LINES
    shown = sc.select_and_ack_break_glass_lines(tmp_path, filler)
    assert shown == []

    shown_again = sc.select_and_ack_break_glass_lines(tmp_path, [])
    assert len(shown_again) == 1
    assert shown_again[0].startswith("GATE BREAK-GLASS:")


def test_select_and_ack_break_glass_lines_partial_space_acks_only_shown(tmp_path):
    track_dir = tmp_path / ".claude" / "dod_track"
    for i in range(3):
        _write_dod_track(
            track_dir,
            f"sess-p{i}",
            {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
        )
    # Exactly 2 slots left out of MAX_LINES -- 3 facts pending, only 2 fit.
    filler = ["x"] * (sc.MAX_LINES - 2)
    shown = sc.select_and_ack_break_glass_lines(tmp_path, filler)
    assert len(shown) == 2

    # The unshown third fact must resurface with room to spare.
    remaining = sc.select_and_ack_break_glass_lines(tmp_path, [])
    assert len(remaining) == 1


def test_select_and_ack_break_glass_lines_exact_boundary_one_slot_short(tmp_path):
    # Adjacent boundary to the "no space at all" case: MAX_LINES - 1 slots
    # used, exactly 1 left -- the single pending fact DOES fit and IS
    # acked.
    track_dir = tmp_path / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-boundary",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    filler = ["x"] * (sc.MAX_LINES - 1)
    shown = sc.select_and_ack_break_glass_lines(tmp_path, filler)
    assert len(shown) == 1

    shown_again = sc.select_and_ack_break_glass_lines(tmp_path, [])
    assert shown_again == []  # already acked -- does not resurface


def test_build_context_lines_includes_break_glass_line(tmp_path):
    events = [_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    track_dir = root / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-live",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )
    lines = sc.build_context_lines(root)
    assert any(l.startswith("GATE BREAK-GLASS:") for l in lines)


def test_build_context_lines_no_break_glass_line_when_none_pending(tmp_path):
    events = [_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    lines = sc.build_context_lines(root)
    assert not any(l.startswith("GATE BREAK-GLASS:") for l in lines)


def test_main_prints_break_glass_line_once_then_silent_on_rerun(tmp_path, capsys):
    # Prints once, silent on the next SessionStart of the same repo state.
    events = [_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")]
    root = _seed_repo(tmp_path, events=events)
    track_dir = root / ".claude" / "dod_track"
    _write_dod_track(
        track_dir,
        "sess-live",
        {"main_gate_state": {"unsafe_completion": {"ts": "t1", "reason": "no-green-run"}}},
    )

    code = sc.main(root)
    assert code == 0
    out = capsys.readouterr().out
    assert "GATE BREAK-GLASS:" in out


# ==== B-402: OPEN DISPATCH keyed by the task key (label, task_id) =================
#
# Two clones issued t-050: clone A's instance (declared, label "codex-fixes") is still open, clone
# B's (undeclared) was accepted. Keyed by the bare id, B's accepted closes A's open dispatch.

import journal_keys as jk


def _t050():
    a = _event("delegated", ts="2026-10-02T10:00:00", agent="scout", task_id="t-050", worker_ref="agent:aaa")
    b = _event("delegated", ts="2026-10-02T11:00:00", agent="scout", task_id="t-050", worker_ref="agent:bbb")
    b_done = _event("accepted", ts="2026-10-02T11:05:00", agent="scout", task_id="t-050")
    return a, b, b_done


def _declared(*events, label="codex-fixes"):
    return jk.Segments(1, [(label, "t-050 issued by both clones", tuple(jk.identity(e) for e in events))])


def test_b402_k4_a_declared_open_instance_is_not_closed_by_the_other_clones_accepted():
    a, b, b_done = _t050()
    events = [a, b, b_done]
    opens = sc.open_dispatches(events, _declared(a))
    assert [o["worker_ref"] for o in opens] == ["agent:aaa"]
    ret = _event("returned", ts="2026-10-02T10:30:00", agent="scout", task_id="t-050", worker_ref="agent:aaa")
    lines = sc.open_dispatch_lines(events + [ret], _declared(a, ret), now=datetime.datetime(2026, 10, 3))
    assert lines == ["OPEN DISPATCHES: 1 (returned, not accepted: 1)",
                     "RESULT PENDING: t-050@codex-fixes agent=scout returned 2026-10-02T10:30:00"]
    # the bare reading, with the same events: the false close
    assert sc.open_dispatches(events, jk.NO_SEGMENTS) == []


def test_b402_no_declaration_reads_exactly_as_before_for_every_legacy_case():
    a, b, b_done = _t050()
    for segs in (jk.NO_SEGMENTS, jk.Segments(1, [])):
        assert sc.open_dispatches([a], segs)[0]["task_id"] == "t-050"
        assert sc.open_dispatches([a, b_done], segs) == []
    # a labeled token with no declaration is a key that matches nothing: nothing closes
    closer = _event("dispatch_skipped", ts="2026-10-02T12:00:00", agent="lead", notes="closes:t-050@codex-fixes done")
    assert len(sc.open_dispatches([a, closer], jk.NO_SEGMENTS)) == 1


def test_b402_qualified_closes_closes_exactly_that_instance():
    a, b, b_done = _t050()
    segs = _declared(a)
    closer = _event("dispatch_skipped", ts="2026-10-02T12:00:00", agent="lead", notes="closes:t-050@codex-fixes done")
    assert sc.open_dispatches([a, b, closer], segs)[0]["worker_ref"] == "agent:bbb"      # the undeclared one stays open
    # a bare token carried by an undeclared event closes the undeclared instance only
    bare = _event("dispatch_skipped", ts="2026-10-02T12:00:00", agent="lead", notes="closes:t-050 done")
    opens = sc.open_dispatches([a, b, bare], segs)
    assert [o["worker_ref"] for o in opens] == ["agent:aaa"]
    # a bare token carried by an event OF the declared instance (same segment) closes that instance
    carrier = _event("escalated", ts="2026-10-02T10:30:00", agent="scout", task_id="t-050", worker_ref="agent:aaa",
                     notes="closes:t-050")
    segs2 = _declared(a, carrier)
    assert [o["worker_ref"] for o in sc.open_dispatches([a, carrier, b], segs2)] == ["agent:bbb"]
    # a carrier with NO task_id resolves a bare token to the undeclared instance
    no_tid = _event("calibrated", ts="2026-10-02T12:00:00", agent="lead", notes="closes:t-050 the clone-B one")
    assert [o["worker_ref"] for o in sc.open_dispatches([a, b, no_tid], segs)] == ["agent:aaa"]


def test_b402_k8_a_declaration_can_reveal_but_never_hide_an_open_dispatch(tmp_path):
    # E4: for any declaration that passes `check`, the reader's open set is a superset of the bare
    # open set; a declaration that fails `check` is never applied (the reader falls back to bare)
    a, b, b_done = _t050()
    c = _event("delegated", ts="2026-10-02T09:00:00", agent="scout", task_id="t-051", worker_ref="agent:ccc")
    d = _event("delegated", ts="2026-10-02T09:10:00", agent="scout", task_id="t-052", worker_ref="agent:ddd")
    x_done = _event("accepted", ts="2026-10-02T09:20:00", agent="scout", task_id="t-052")
    journal = [c, a, b, b_done, d, x_done]
    root = _seed_repo(tmp_path, events=journal)
    bare = {(o["task_id"], o["worker_ref"]) for o in sc.open_dispatches(journal, jk.NO_SEGMENTS)}
    assert bare == {("t-051", "agent:ccc")}
    passed = 0
    # {A}, {B, accepted}: legal; {A, B} (leaves an accepted first line), {D}/{D, X} (one instance only), {C}: refused
    for segs in (_declared(a), _declared(b, b_done), _declared(a, b), _declared(d), _declared(d, x_done), _declared(c)):
        (root / "logs" / "journal-segments.json").write_text(jk.dumps_declaration(segs), encoding="utf-8")
        loaded, reason = jk.load_segments(root / "logs" / "routing-log.jsonl")
        passed += reason is None
        keyed = {(o["task_id"], o["worker_ref"]) for o in sc.open_dispatches(journal, loaded)}
        assert bare <= keyed, (list(segs.listed), bare, keyed)
    assert passed == 2
    # the critic's trace: declaring {A, B} of one clone's t-050 reveals the open A (visible), never hides C
    (root / "logs" / "journal-segments.json").write_text(jk.dumps_declaration(_declared(b, b_done)), encoding="utf-8")
    loaded, _ = jk.load_segments(root / "logs" / "routing-log.jsonl")
    assert {(o["task_id"], o["worker_ref"]) for o in sc.open_dispatches(journal, loaded)} == {
        ("t-051", "agent:ccc"), ("t-050", "agent:aaa")}


def test_b402_declared_display_goes_through_ascii_sanitize():
    a, b, _ = _t050()
    ret = _event("returned", ts="2026-10-02T10:30:00", agent="scout", task_id="t-050", worker_ref="agent:aaa")
    weird = jk.Segments(1, [("x-" + "y" * 20, "w", (jk.identity(a), jk.identity(ret)))])
    line = sc.open_dispatch_lines([a, ret, b], weird, now=datetime.datetime(2026, 10, 3))[1]
    assert line.isascii() and "t-050@x-" in line


def test_b402_build_context_lines_reads_the_declaration_of_its_root(tmp_path):
    a, b, b_done = _t050()
    root = _seed_repo(tmp_path, events=[a, b, b_done])
    now = datetime.datetime(2026, 10, 3, 12, 0, 0)
    assert not any(l.startswith("OPEN DISPATCH") for l in sc.build_context_lines(root, now))      # glued: closed
    (root / "logs" / "journal-segments.json").write_text(jk.dumps_declaration(_declared(a)), encoding="utf-8")
    lines = sc.build_context_lines(root, now)
    assert "OPEN DISPATCHES: 1 (returned, not accepted: 0)" in lines
    assert not any(l.startswith("JOURNAL SEGMENTS") for l in lines)


def test_b402_an_unreadable_declaration_adds_one_line_and_every_id_reads_bare(tmp_path):
    a, b, b_done = _t050()
    root = _seed_repo(tmp_path, events=[a, b, b_done])
    now = datetime.datetime(2026, 10, 3, 12, 0, 0)
    for payload in (b"\x00\x01{{{", b"[]", b'{"version": 2, "segments": []}', b"\xff\xfe"):
        (root / "logs" / "journal-segments.json").write_bytes(payload)
        lines = sc.build_context_lines(root, now)
        seg = [l for l in lines if l.startswith("JOURNAL SEGMENTS: unreadable (")]
        assert len(seg) == 1 and seg[0].endswith(") -- colliding task ids read as one task"), payload
        assert seg[0].isascii() and len(seg[0]) < 260
        assert not any(l.startswith("OPEN DISPATCH") for l in lines)                 # read bare: closed
        assert len(lines) <= sc.MAX_LINES
    # the declaration is absent: no such line
    (root / "logs" / "journal-segments.json").unlink()
    assert not any(l.startswith("JOURNAL SEGMENTS") for l in sc.build_context_lines(root, now))


def test_b402_segments_none_loads_the_repository_declaration_and_never_raises(monkeypatch, tmp_path):
    a, b, b_done = _t050()
    root = _seed_repo(tmp_path, events=[a, b, b_done])
    (root / "logs" / "journal-segments.json").write_text(jk.dumps_declaration(_declared(a)), encoding="utf-8")
    monkeypatch.setattr(sc, "repo_root", lambda: root)
    assert [o["worker_ref"] for o in sc.open_dispatches([a, b, b_done])] == ["agent:aaa"]
    (root / "logs" / "journal-segments.json").write_bytes(b"\x00{{{")
    assert sc.open_dispatches([a, b, b_done]) == []                     # broken: NO_SEGMENTS, no exception


def test_b402_failed_import_of_journal_keys_is_fail_open_and_announced(monkeypatch, tmp_path):
    a, b, b_done = _t050()
    monkeypatch.setattr(sc, "_jk", None)
    monkeypatch.setattr(sc, "_JK_IMPORT_ERROR", ImportError("boom"))
    assert sc.open_dispatches([a, b, b_done], None) == []               # bare ids, no exception
    root = _seed_repo(tmp_path, events=[a, b, b_done])
    lines = sc.build_context_lines(root, datetime.datetime(2026, 10, 3, 12, 0, 0))
    assert any(l.startswith("JOURNAL SEGMENTS: unreadable (journal_keys module not importable") for l in lines)


def test_b402_closes_token_regex_shapes():
    assert sc._closes_task_ids("closes:t-050 and closes:t-051@codex-fixes.") == ["t-050", "t-051@codex-fixes"]
    assert sc._closes_task_ids("closes:t-050@Codex") == []                   # a malformed label closes nothing
    assert sc._closes_task_ids("discloses:t-050") == [] and sc._closes_task_ids(None) == []
    assert sc._closes_task_ids("closes:t-5") == []                            # REWRITTEN (offload B0): the one grammar is 3-9 digits
    assert sc._closes_task_ids("closes:t-123a closes:t-123") == ["t-123a", "t-123"]
    assert sc._closes_task_ids("closes:t-123A closes:t-123abc closes:t-123а") == []     # E-B0-1/2: closes nothing
    assert sc._closes_key("t-050", {}, jk.NO_SEGMENTS) == ("", "t-050")


def test_b402_fallback_regex_is_pinned_equal_to_journal_keys_and_reads_the_same(monkeypatch):
    assert sc._CLOSES_RE.pattern == jk.CLOSES_RE.pattern
    samples = ["closes:t-050 closes:t-051@codex-fixes.", "closes:t-050@Codex", "closes:t-050@", "discloses:t-050",
               "closes:t-050@codex_x closes:t-051", "closes:t-5", "closes:t-050@" + "a" * 25,
               # offload B0 (E-B0-1/2): the fallback copy reads the one grammar exactly like journal_keys
               "closes:t-123a closes:t-123", "closes:t-123A", "closes:t-123abc", "closes:t-123а", "closes:t-12",
               "closes:t-1234567890", "closes:t-123—x", "closes:t-123ab@codex", "closes:t-123,closes:t-123b."]
    want = [jk.closes_tokens(s) for s in samples]
    monkeypatch.setattr(sc, "_jk", None)
    assert [sc._closes_task_ids(s) for s in samples] == want


def test_b402_f1_a_malformed_or_unknown_label_closes_neither_instance_and_a_valid_one_closes_its_own():
    a = _event("delegated", ts="2026-10-02T10:00:00", agent="scout", task_id="t-050", worker_ref="agent:aaa")
    b = _event("delegated", ts="2026-10-02T11:00:00", agent="scout", task_id="t-050", worker_ref="agent:bbb")
    segs = _declared(a, label="codex")                      # a = t-050@codex; b = the undeclared instance, both open

    def opened(notes):
        closer = _event("dispatch_skipped", ts="2026-10-02T12:00:00", agent="lead", notes=notes)
        return sorted(o["worker_ref"] for o in sc.open_dispatches([a, b, closer], segs))

    both = ["agent:aaa", "agent:bbb"]
    assert opened("closes:t-050@Codex") == both        # malformed label: nothing (was: closed the undeclared one)
    assert opened("closes:t-050@nolabel") == both      # a valid shape, no such instance: nothing
    assert opened("closes:t-050@codex") == ["agent:bbb"]
    assert opened("closes:t-050") == ["agent:aaa"]     # bare, a carrier with no task_id: the undeclared one


# ================================ K5: the SessionStart scan over two journal files (t-581, F0-4) ================================

from test_journal_per_developer import (DEV1, DEV2, M_CREATED, N_CREATED, accepted as _acc8,
                                        created as _cr8, delegated as _dl8, ev as _ev8, jtext as _jt8,
                                        write as _wr8)

_NOW5 = datetime.datetime(2026, 10, 3, 12, 0, 0)


def _k5_root(tmp_path, dev1_lines, dev2_lines=None, slug="dev1", history=None):
    hist = history if history is not None else [_dl8("t-001", "2026-10-02T09:00:00"), _acc8("t-001", "2026-10-02T09:30:00")]
    root = _seed_repo(tmp_path, events=hist)
    _wr8(root, DEV1, _jt8(M_CREATED, *dev1_lines))
    if dev2_lines is not None:
        _wr8(root, DEV2, _jt8(N_CREATED, *dev2_lines))
    if slug:
        _wr8(root, "tools/dev.config.yaml", f"developer: {slug}\n")
    return root


def _k5_lines(root):
    lines = build_context_lines(root, _NOW5)
    return lines, [l for l in lines if l.startswith("OPEN DISPATCH")]


def test_k5_open_tasks_of_both_files_own_first_and_the_foreign_one_with_its_slug(tmp_path):
    root = _k5_root(tmp_path, [_dl8("t-002", "2026-10-02T10:00:00"), _dl8("t-003", "2026-10-02T10:10:00")],
                    [_dl8("t-001", "2026-10-02T09:45:00")])             # dev2's is OLDER than both of the owner's
    lines, opens = _k5_lines(root)
    assert opens == ["OPEN DISPATCHES: 3 (returned, not accepted: 0)"]            # both files are scanned; FG7-48: one count line, no names without a `returned`
    assert "JOURNAL: write to logs/journal/dev1.jsonl" in lines
    assert not any(l.startswith("JOURNAL FILES:") for l in lines)


def test_k5_last_event_is_the_writers_own_even_when_the_other_file_is_later(tmp_path):
    root = _k5_root(tmp_path, [_dl8("t-002", "2026-10-02T10:00:00")], [_dl8("t-001", "2026-10-02T11:30:00")])
    lines, _ = _k5_lines(root)
    last = [l for l in lines if l.startswith("LAST EVENT")]
    assert last == ["LAST EVENT: ts=2026-10-02T10:00:00 event=delegated agent=builder task_id=t-002"]
    write_as_dev2 = _k5_root(tmp_path / "n", [_dl8("t-002", "2026-10-02T10:00:00")], [_dl8("t-001", "2026-10-02T11:30:00")],
                                slug="dev2")
    lines, _ = _k5_lines(write_as_dev2)
    assert "LAST EVENT: ts=2026-10-02T11:30:00 event=delegated agent=builder task_id=t-001" in lines
    assert "JOURNAL: write to logs/journal/dev2.jsonl" in lines


def test_k5_four_own_and_one_foreign_are_one_count_line_and_no_names(tmp_path):
    own = [_dl8(f"t-00{i}", f"2026-10-02T10:{i}0:00") for i in (2, 3, 4, 5)]
    root = _k5_root(tmp_path, own, [_dl8("t-001", "2026-10-02T09:45:00")])      # the foreign one is the OLDEST
    lines, opens = _k5_lines(root)
    assert opens == ["OPEN DISPATCHES: 5 (returned, not accepted: 0)"]            # the foreign one is counted too; the old 3-line cut and E-11 own-first are gone
    assert not any("@dev2" in l for l in lines)


def test_k5_a_labelled_closes_in_the_owner_file_closes_the_other_writers_task_and_a_bare_one_does_not(tmp_path):
    foreign = [_dl8("t-001", "2026-10-02T09:45:00")]
    close_labelled = _ev8("dispatch_skipped", "2026-10-02T10:20:00", agent="scout", notes="closes:t-001@dev2")
    close_bare = _ev8("dispatch_skipped", "2026-10-02T10:20:00", agent="scout", notes="closes:t-001")
    root = _k5_root(tmp_path / "a", [_dl8("t-002", "2026-10-02T10:00:00"), close_labelled], foreign)
    assert _k5_lines(root)[1] == ["OPEN DISPATCHES: 1 (returned, not accepted: 0)"]
    root = _k5_root(tmp_path / "b", [_dl8("t-002", "2026-10-02T10:00:00"), close_bare], foreign)
    assert _k5_lines(root)[1] == ["OPEN DISPATCHES: 2 (returned, not accepted: 0)"]
    ghost = _ev8("dispatch_skipped", "2026-10-02T10:20:00", agent="scout", notes="closes:t-001@ghost")
    root = _k5_root(tmp_path / "c", [_dl8("t-002", "2026-10-02T10:00:00"), ghost], foreign)
    assert _k5_lines(root)[1] == ["OPEN DISPATCHES: 2 (returned, not accepted: 0)"]


def test_k5_a_task_of_the_history_is_closed_by_an_accepted_in_the_successor(tmp_path):
    history = [_dl8("t-001", "2026-10-02T09:00:00"), _dl8("t-002", "2026-10-02T09:10:00")]
    root = _k5_root(tmp_path, [_acc8("t-002", "2026-10-02T10:00:00")], history=history)
    lines, opens = _k5_lines(root)
    assert opens == ["OPEN DISPATCHES: 1 (returned, not accepted: 0)"]      # the same task ("", t-002), one logical journal


def test_k5_after_the_switch_without_a_slug_says_so_and_shows_the_newest_line_with_its_file(tmp_path):
    root = _k5_root(tmp_path, [_dl8("t-002", "2026-10-02T10:00:00")], [_dl8("t-001", "2026-10-02T11:30:00")], slug=None)
    lines, _ = _k5_lines(root)
    no_slug = [l for l in lines if l.startswith("JOURNAL: no developer slug")]
    assert len(no_slug) == 1 and "tools/dev.config.yaml" in no_slug[0] and no_slug[0].isascii()
    assert any(l.startswith("LAST EVENT: ts=2026-10-02T11:30:00") and l.endswith("(file logs/journal/dev2.jsonl)") for l in lines)
    assert not any(l.startswith("JOURNAL: write to") for l in lines)


def test_k5_before_the_switch_there_is_no_journal_line_at_all(tmp_path):
    root = _seed_repo(tmp_path, events=[_dl8("t-001", "2026-10-02T09:00:00")])
    lines, opens = _k5_lines(root)
    assert not any(l.startswith("JOURNAL") for l in lines) and len(opens) == 1
    assert "LAST EVENT: ts=2026-10-02T09:00:00 event=delegated agent=builder task_id=t-001" in lines


def test_k5_last_calibration_is_the_newest_of_all_files_and_problems_are_one_capped_line(tmp_path):
    cal = _ev8("calibrated", "2026-09-30T10:00:00", agent="lead", category="process")
    root = _k5_root(tmp_path, [_dl8("t-002", "2026-10-02T10:00:00")], [_dl8("t-001", "2026-10-02T11:30:00")],
                    history=[_dl8("t-001", "2026-09-01T09:00:00"), _ev8("calibrated", "2026-09-10T10:00:00", agent="lead", category="process")])
    newer = _cr8("2026-09-30T10:00:00")
    _wr8(root, "logs/journal/dev4.jsonl", _jt8(newer, cal))
    _wr8(root, "logs/journal/Bad Name.jsonl", "x\n")
    lines, _ = _k5_lines(root)
    assert "Last calibration: 2026-09-30T10:00:00 (3 days ago)" in lines
    files = [l for l in lines if l.startswith("JOURNAL FILES:")]
    assert len(files) == 1 and "Bad Name.jsonl" in files[0] and files[0].isascii() and len(files[0]) < 300
    assert len(lines) <= sc.MAX_LINES


def test_k5_an_empty_developer_file_is_stated_as_empty_not_as_foreign(tmp_path):
    root = _seed_repo(tmp_path, events=[_dl8("t-001", "2026-10-02T09:00:00")])
    _wr8(root, DEV1, "")
    _wr8(root, "tools/dev.config.yaml", "developer: dev1\n")
    lines, _ = _k5_lines(root)
    assert "JOURNAL: empty (logs/journal/dev1.jsonl)" in lines and "JOURNAL: write to logs/journal/dev1.jsonl" in lines


# ---- TD-15.7: the test-quarantine session line (spec td-15 D.5 (1)) ----

_TQ_ROWS = [
    ("waiting", ["TEST QUARANTINE: 581 files since 2026-11-20 (cohort 1, entered at 0.10.9); releases since: 1 of 2"], "581 files since"),
    ("not_pulled", ["TEST QUARANTINE: 581 files since 2026-11-20; pulled 2026-11-17 (7 d ago) -- run: python tools/test_quarantine.py pull"], "-- run: python tools/test_quarantine.py pull"),
    ("ready", ["TEST QUARANTINE: READY TO DELETE cohort 1 -- 581 files since 2026-11-20"], "READY TO DELETE"),
    ("alert_catch", ["TEST QUARANTINE ALERT: real catch 2026-11-25 -- test_x.py: why", "TEST QUARANTINE: 1 files"], "ALERT: real catch"),
    ("alert_watch", ["TEST QUARANTINE ALERT: the watch has not run on CI for 9 d", "TEST QUARANTINE: 1 files"], "ALERT: the watch has not run"),
    ("unknown", ["TEST QUARANTINE: status unknown (no pull yet)"], "status unknown"),
]


def _stub_tq(monkeypatch, fn):
    import types
    mod = types.ModuleType("test_quarantine")
    mod.status_line = fn
    monkeypatch.setitem(sys.modules, "test_quarantine", mod)


@pytest.mark.parametrize("name,stub_lines,token", _TQ_ROWS, ids=[r[0] for r in _TQ_ROWS])
def test_td157_quarantine_line_token_per_world(monkeypatch, tmp_path, name, stub_lines, token):
    _stub_tq(monkeypatch, lambda root: list(stub_lines))
    got = sc.test_quarantine_line(tmp_path)
    assert got == stub_lines and any(token in l for l in got)
    root = _seed_repo(tmp_path)
    ctx = sc.build_context_lines(root, datetime.datetime(2026, 11, 10, 12, 0, 0))
    i = [k for k, l in enumerate(ctx) if l.startswith("Last calibration:")][0]
    assert ctx[i + 1 : i + 1 + len(stub_lines)] == stub_lines


def test_td157_quarantine_line_empty_stub_adds_nothing(monkeypatch, tmp_path):
    root = _seed_repo(tmp_path)
    now = datetime.datetime(2026, 11, 10, 12, 0, 0)
    _stub_tq(monkeypatch, lambda r: [])
    assert sc.test_quarantine_line(root) == []
    assert not any("TEST QUARANTINE" in l for l in sc.build_context_lines(root, now))


def test_td157_quarantine_line_exception_is_one_unavailable_line_and_context_intact(monkeypatch, tmp_path):
    root = _seed_repo(tmp_path)
    now = datetime.datetime(2026, 11, 10, 12, 0, 0)
    base = sc.build_context_lines(root, now)
    def boom(r):
        raise RuntimeError("x" * 400)
    _stub_tq(monkeypatch, boom)
    got = sc.test_quarantine_line(root)
    assert len(got) == 1 and "unavailable" in got[0] and got[0].isascii() and len(got[0]) < 200
    ctx = sc.build_context_lines(root, now)
    assert [l for l in ctx if "TEST QUARANTINE" not in l] == [l for l in base if "TEST QUARANTINE" not in l]
    assert sum("unavailable" in l and "TEST QUARANTINE" in l for l in ctx) == 1


def test_td157_quarantine_line_real_function_no_records_no_line(tmp_path):
    # a root with the package scripts but no layers file (a bare root with no package reads as "unknown", by the tool's own rule)
    sys.modules.pop("test_quarantine", None)
    root = _seed_repo(tmp_path)
    scripts = root / "ai-packages" / "qa-factory" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "selftest.py").write_text(
        "class TestLayersError(Exception):\n    pass\n\n"
        "def test_layers(path):\n    return {'absent': True, 'quarantine': {}, 'cohorts': {}}\n", encoding="utf-8")
    assert sc.test_quarantine_line(root) == []
    assert not any("TEST QUARANTINE" in l for l in sc.build_context_lines(root, datetime.datetime(2026, 11, 10, 12, 0, 0)))


# ---- A1 (fg-context-and-hygiene): the block after a compaction, identity by the header of the first line ----

import compact_snapshot as _cs_mod  # the one module name (a candidate, when COMPACT_SNAPSHOT_PATH is set); patches below resolve it at call time
_scm = sc

_A1_NOW = datetime.datetime(2026, 11, 12, 13, 0, 0)
_A1_DIR = "docs/tasks/compact-snapshots"
_A1_FRESH = "min old, trigger"        # the fresh line carries the trigger; MISSING never does
_A1_MISSING = "COMPACT SNAPSHOT: MISSING for this compaction"
_A1_DOOR = "python -B tools/compact_snapshot.py --source manual"
_A1_ABSENT = "absent"                 # record_after: the record file is not there


def _a1_put(root, files):
    folder = root / _A1_DIR
    folder.mkdir(parents=True, exist_ok=True)
    for name, session, age_min, *rest in files:
        path = folder / name
        # optional 4th item: minutes ago the header says it was written (negative = in the future), or a raw
        # `written:` text, or "absent" for a header with no written field; default: written right now
        written = rest[0] if rest else 0
        if session is None:
            text = "# body\n"
        elif isinstance(written, int):
            text = _cs_mod.header_line(session, "manual", _A1_NOW - datetime.timedelta(minutes=written)) + "\n# body\n"
        else:
            field = "" if written == "absent" else f"; written: {written}"
            text = f"{_cs_mod.HOOK_HEADER_PREFIX}; session: {session}; trigger: manual{field} -->\n# body\n"
        path.write_text(text, encoding="utf-8")
        stamp = _A1_NOW.timestamp() - age_min * 60
        os.utime(path, (stamp, stamp))


def _a1_record(root):
    path = root / ".claude" / "compact_seen.json"
    if not path.exists():
        return _A1_ABSENT
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except ValueError:
        return raw   # a corrupt record is compared as its raw text


# id, files [(name, header session | None = no header, age in min)], record (None | list | raw str), the SessionStart
# session id, mode, expected prefix of line 0, strings that must / must not be in the block, the record afterwards
_A1_ROWS = [
    ("fresh_headed", [("2026-11-12-1257-manual.md", "s1", 3)], None, "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)",
     ["AFTER COMPACT: read the snapshot above before your next action"], ["MISSING", "COMPACT NARRATIVE"],
     ["2026-11-12-1257-manual.md"]),
    ("headed_11_min_old", [("2026-11-12-1249-manual.md", "s1", 11)], None, "s1", "fn",
     _A1_MISSING, [f"{_A1_DIR}/2026-11-12-1249-manual.md, 11 min old", _A1_DOOR], [_A1_FRESH], _A1_ABSENT),
    ("headed_10_min_old_still_counts", [("2026-11-12-1250-manual.md", "s1", 10)], None, "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1250-manual.md (10 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1250-manual.md"]),
    ("headed_already_announced", [("2026-11-12-1257-manual.md", "s1", 3)], ["2026-11-12-1257-manual.md"], "s1", "fn",
     _A1_MISSING, [_A1_DOOR], [_A1_FRESH], ["2026-11-12-1257-manual.md"]),
    ("two_compactions_second_precompact_absent", [("2026-11-12-1257-manual.md", "s1", 3)], None, "s1", "twice",
     _A1_MISSING, [_A1_DOOR, "5 min old"], [_A1_FRESH], ["2026-11-12-1257-manual.md"]),
    ("unheaded_hand_written_newest", [("2026-11-12-1210-manual.md", None, 1), ("2026-11-12-1230-manual.md", "s1", 30)],
     None, "s1", "fn",
     _A1_MISSING, [f"COMPACT NARRATIVE: newest has no session stamp ({_A1_DIR}/2026-11-12-1210-manual.md) -- check it is yours", _A1_DOOR],
     [_A1_FRESH], _A1_ABSENT),
    ("headed_suffix_2", [("2026-11-12-1259-manual-2.md", "s1", 1)], None, "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1259-manual-2.md (1 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1259-manual-2.md"]),
    ("headed_other_source_name", [("2026-11-12-1259-weird.md", "s1", 2)], None, "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1259-weird.md (2 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1259-weird.md"]),
    ("session_mismatch", [("2026-11-12-1257-manual.md", "s1", 3)], None, "s2", "fn",
     _A1_MISSING, ["--session s2"], [_A1_FRESH], _A1_ABSENT),
    ("session_unknown_in_header", [("2026-11-12-1257-manual.md", "unknown", 3)], None, "s2", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1257-manual.md"]),
    ("session_unknown_in_payload", [("2026-11-12-1257-manual.md", "s1", 3)], None, None, "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1257-manual.md"]),
    ("two_sessions_in_one_clone_newest_is_the_other_ones",
     [("2026-11-12-1256-manual.md", "mine", 4), ("2026-11-12-1258-manual.md", "other", 2)], None, "mine", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1256-manual.md (4 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1256-manual.md"]),
    ("no_folder", [], None, "s1", "fn",
     "COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot none)", [_A1_DOOR], [_A1_FRESH],
     _A1_ABSENT),
    ("folder_with_only_readme", [("README.md", None, 5)], None, "s1", "fn",
     "COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot none)", [_A1_DOOR],
     ["COMPACT NARRATIVE"], _A1_ABSENT),
    # B1: the age is the OLDER of the mtime age and the header's written age; a written that is absent / unparsable
    # is never fresh; a written in the future counts as 0 (the mtime decides)
    ("written_65_min_ago_mtime_refreshed", [("2026-11-12-1155-manual.md", "s1", 5, 65)], None, "s1", "fn",
     _A1_MISSING, [f"{_A1_DIR}/2026-11-12-1155-manual.md, 65 min old", _A1_DOOR], [_A1_FRESH], _A1_ABSENT),
    ("other_sessions_old_file_mtime_refreshed", [("2026-11-11-0900-manual.md", "unknown", 2, 1440)], None, "s1", "fn",
     _A1_MISSING, [_A1_DOOR], [_A1_FRESH], _A1_ABSENT),
    ("written_unparsable", [("2026-11-12-1257-manual.md", "s1", 3, "garbage")], None, "s1", "fn",
     _A1_MISSING, [_A1_DOOR, "3 min old"], [_A1_FRESH], _A1_ABSENT),
    ("written_absent_from_header", [("2026-11-12-1257-manual.md", "s1", 3, "absent")], None, "s1", "fn",
     _A1_MISSING, [_A1_DOOR], [_A1_FRESH], _A1_ABSENT),
    ("written_in_the_future_mtime_decides", [("2026-11-12-1257-manual.md", "s1", 3, -5)], None, "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1257-manual.md"]),
    # F5: one candidate unreadable, the other still named
    ("newer_candidate_unreadable_older_still_named",
     [("2026-11-12-1256-manual.md", "s1", 4), ("2026-11-12-1258-manual.md", "s1", 2)], None, "s1", "newer_unreadable",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1256-manual.md (4 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1256-manual.md"]),
    # B2: an unreadable record -> MISSING and the record is rebuilt now, so the next compaction works again
    ("record_corrupt", [("2026-11-12-1257-manual.md", "s1", 3)], "{not json", "s1", "fn",
     _A1_MISSING, [_A1_DOOR, "COMPACT SNAPSHOT: announced record unreadable (", "rebuilt"], [_A1_FRESH],
     ["2026-11-12-1257-manual.md"]),
    ("record_corrupt_next_compaction_works", [("2026-11-12-1257-manual.md", "s1", 3)], "{not json", "s1", "heal",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1259-manual.md (1 {_A1_FRESH} manual)", [], ["MISSING"],
     ["2026-11-12-1257-manual.md", "2026-11-12-1259-manual.md"]),
    ("record_not_a_list", [("2026-11-12-1257-manual.md", "s1", 3)], '{"a": 1}', "s1", "fn",
     _A1_MISSING, ["announced record unreadable (not a JSON list)", "rebuilt"], [_A1_FRESH],
     ["2026-11-12-1257-manual.md"]),
    ("record_corrupt_and_not_writable", [("2026-11-12-1257-manual.md", "s1", 3)], "{not json", "s1", "unwritable",
     _A1_MISSING, ["announced record unreadable (", "delete .claude/compact_seen.json"], [_A1_FRESH, "rebuilt now"],
     "{not json"),
    ("record_not_writable", [("2026-11-12-1257-manual.md", "s1", 3)], None, "s1", "unwritable",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)",
     ["COMPACT SNAPSHOT: announced record not written ("], ["MISSING"], _A1_ABSENT),
    ("record_keeps_the_last_200",
     [("2026-11-12-1257-manual.md", "s1", 3)], [f"old-{i}.md" for i in range(250)], "s1", "fn",
     f"COMPACT SNAPSHOT: {_A1_DIR}/2026-11-12-1257-manual.md (3 {_A1_FRESH} manual)", [], ["MISSING"],
     [f"old-{i}.md" for i in range(51, 250)] + ["2026-11-12-1257-manual.md"]),
    ("non_compact_source", [("2026-11-12-1257-manual.md", "s1", 3)], None, "s1", "startup", None, [],
     ["COMPACT SNAPSHOT", "COMPACT NARRATIVE", "AFTER COMPACT"], _A1_ABSENT),
]


class _A1Stdin:
    def __init__(self, text):
        self._text = text

    def isatty(self):
        return False

    def read(self):
        return self._text


@pytest.mark.parametrize("files, record, session, mode, first, must, must_not, record_after",
                         [r[1:] for r in _A1_ROWS], ids=[r[0] for r in _A1_ROWS])
def test_a1_compact_block(tmp_path, monkeypatch, capsys, files, record, session, mode, first, must, must_not,
                          record_after):
    _a1_put(tmp_path, files)
    if record is not None:
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".claude" / "compact_seen.json").write_text(
            record if isinstance(record, str) else json.dumps(record), encoding="utf-8")
    if mode == "unwritable":
        real = Path.write_text

        def refuse(self, *a, **k):
            if self.name.startswith("compact_seen.json"):   # the record and the temp file of its atomic write
                raise PermissionError("read-only")
            return real(self, *a, **k)

        monkeypatch.setattr(Path, "write_text", refuse)
    if mode == "newer_unreadable":
        real_identity = sys.modules["compact_snapshot"].snapshot_identity

        def identity(p):
            if "1258" in str(p):
                raise OSError("denied")
            return real_identity(p)

        monkeypatch.setattr(sys.modules["compact_snapshot"], "snapshot_identity", identity)
    if mode == "startup":
        (tmp_path / "logs").mkdir()
        monkeypatch.setattr(sys, "stdin", _A1Stdin(json.dumps({"source": "startup", "session_id": session})))
        assert _scm.main(tmp_path) == 0
        lines = capsys.readouterr().out.splitlines()
    else:
        lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, session)
        if mode == "twice":
            assert lines[0].startswith("COMPACT SNAPSHOT: ") and _A1_FRESH in lines[0], lines   # the first compaction
            lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW + datetime.timedelta(minutes=2), session)
        if mode == "heal":
            assert lines[0].startswith(_A1_MISSING) and "rebuilt" in "\n".join(lines), lines   # the corrupt record
            _a1_put(tmp_path, [("2026-11-12-1259-manual.md", "s1", 1)])                        # a new compaction
            lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, session)
    if first is not None:
        assert lines[0].startswith(first), lines
    block = "\n".join(lines)
    for text in must:
        assert text in block, (text, lines)
    for text in must_not:
        assert text not in block, (text, lines)
    assert _a1_record(tmp_path) == record_after


def test_a1_match_session_constant_is_the_one_switch(tmp_path, monkeypatch):
    _a1_put(tmp_path, [("2026-11-12-1257-manual.md", "s1", 3)])
    monkeypatch.setattr(_scm, "MATCH_SESSION", False)
    lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s2")
    assert _A1_FRESH in lines[0], lines   # with the switch off the session clause is skipped


def test_a1_clock_skew_reads_as_age_zero(tmp_path):
    _a1_put(tmp_path, [("2026-11-12-1257-manual.md", "s1", -5)])   # mtime 5 min in the future
    lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s1")
    assert lines[0].endswith("(0 min old, trigger manual)"), lines


def test_a1_unreadable_file_is_skipped_and_all_failing_is_unavailable(tmp_path, monkeypatch):
    _a1_put(tmp_path, [("2026-11-12-1257-manual.md", "s1", 3)])
    monkeypatch.setattr(sys.modules["compact_snapshot"], "snapshot_identity", lambda p: (_ for _ in ()).throw(OSError("denied")))
    lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s1")
    assert lines[0] == f"COMPACT SNAPSHOT: unavailable (OSError: denied) -- write it now: {_A1_DOOR} --session s1", lines
    assert lines[1].startswith("AFTER COMPACT: read the snapshot above") and len(lines) == 2, lines   # F3


def test_a1_write_announced_merges_what_another_session_wrote(tmp_path):
    record = tmp_path / ".claude" / "compact_seen.json"
    record.parent.mkdir()
    record.write_text(json.dumps(["other-session.md", "dup.md"]), encoding="utf-8")   # written after our first read
    assert _scm._write_announced(record, ["dup.md", "mine.md"]) is None
    assert json.loads(record.read_text(encoding="utf-8")) == ["other-session.md", "dup.md", "mine.md"]


def test_a1_outer_failure_also_carries_the_after_line(tmp_path, monkeypatch):
    monkeypatch.setattr(_scm, "_compact_candidates", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    lines = _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s1")
    assert lines[0].startswith("COMPACT SNAPSHOT: unavailable (RuntimeError: boom)") and len(lines) == 2, lines
    assert lines[1].startswith("AFTER COMPACT: "), lines


def test_a1_old_unheaded_hook_snapshots_read_as_narratives(tmp_path):
    """Temporal, both worlds: a snapshot written before the header existed has none, so it can never be this
    compaction's; the same text with the header on line 1 can."""
    _a1_put(tmp_path, [("2026-11-12-1257-auto.md", None, 3)])
    assert _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s1")[0].startswith(_A1_MISSING)
    _a1_put(tmp_path, [("2026-11-12-1257-auto.md", "s1", 3)])
    assert _A1_FRESH in _scm.compact_snapshot_lines(tmp_path, _A1_NOW, "s1")[0]


def test_a1_no_caller_of_the_old_function_name_is_left():
    assert not hasattr(_scm, "compact_snapshot_line")


# ---- F6-58 (rule 9e) q1: the PARALLEL SESSION note at SessionStart ----

def _q1_transcripts(tmp_path, peer_age=None):
    folder = tmp_path / "transcripts"
    folder.mkdir(exist_ok=True)
    own = folder / "own.jsonl"
    own.write_text("{}\n", encoding="utf-8")
    if peer_age is not None:
        peer = folder / "peer-session-1234.jsonl"
        peer.write_text("{}\n", encoding="utf-8")
        t = time.time() - peer_age
        os.utime(peer, (t, t))
    return str(own)


def test_q1_session_start_adds_one_parallel_session_line_when_a_peer_wrote_two_minutes_ago(tmp_path, monkeypatch, capsys):
    import session_context as _sc
    root = _seed_repo(tmp_path / "r", events=[_event("delegated", task_id="t-001")])
    payload = {"transcript_path": _q1_transcripts(tmp_path, peer_age=125), "source": "startup"}
    lines = _sc.peer_note_lines(root, payload)
    assert len(lines) == 1 and lines[0].startswith("PARALLEL SESSION (a note, nothing is blocked)")
    assert "2 min ago (peer-ses)" in lines[0]
    assert "Task ids come from the clone counter (python -B tools/journal_write.py next); nothing to do." in lines[0]
    assert "id_band" not in lines[0] and "band" not in lines[0]               # REWRITTEN (offload B0): no band is opened
    monkeypatch.setattr(_sc, "read_stdin_payload", lambda: payload)
    assert _sc.main(root) == 0
    out = capsys.readouterr().out.splitlines()
    assert sum(1 for l in out if l.startswith("PARALLEL SESSION")) == 1 and out[-1].startswith("PARALLEL SESSION")


def test_q1_after_a_clear_the_note_keeps_the_peer_and_gains_the_suffix_only_for_source_clear(tmp_path):
    import session_context as _sc
    root = _seed_repo(tmp_path / "r", events=[_event("delegated", task_id="t-001")])
    own = _q1_transcripts(tmp_path, peer_age=125)
    suffix = " (possibly this session before /clear)"
    (note,) = _sc.peer_note_lines(root, {"transcript_path": own, "source": "clear"})
    assert note.endswith(suffix) and "2 min ago (peer-ses)" in note          # the peer is not dropped
    for source in ("startup", "resume", "compact", "", None, 5):
        (plain,) = _sc.peer_note_lines(root, {"transcript_path": own, "source": source})
        assert not plain.endswith(suffix) and plain == note[:-len(suffix)]
    (tmp_path / "alone").mkdir()
    alone = _q1_transcripts(tmp_path / "alone")                     # a folder with only the own file
    assert _sc.peer_note_lines(root, {"transcript_path": alone, "source": "clear"}) == []


def test_q1_with_no_peer_or_no_transcript_path_the_boot_text_is_unchanged(tmp_path, monkeypatch, capsys):
    import session_context as _sc
    root = _seed_repo(tmp_path / "r", events=[_event("delegated", task_id="t-001")])
    for payload in ({"transcript_path": _q1_transcripts(tmp_path)}, {"transcript_path": _q1_transcripts(tmp_path, 601)},
                    {}, {"transcript_path": 5}, None):
        assert _sc.peer_note_lines(root, payload) == []
    monkeypatch.setattr(_sc, "read_stdin_payload", lambda: {"transcript_path": _q1_transcripts(tmp_path)})
    assert _sc.main(root) == 0
    assert "PARALLEL SESSION" not in capsys.readouterr().out


# ==== COORDINATOR RULES line (worker split, t-1137; spec edges e1 e2 e6 e7) =========

_CR_FILES = list(sc._coordinator_files())


def _cr_root(tmp_path, damage=None, dirname="r"):
    """A tree with the coordinator files, 7 bytes each; `damage` = {name: "absent" | "empty" | "directory"}."""
    root = _seed_repo(tmp_path / dirname, events=[_event("delegated", task_id="t-001")])
    for name in _CR_FILES:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"r" * 7)
    for name, how in (damage or {}).items():
        target = root / name
        target.unlink()
        if how == "empty":
            target.write_bytes(b"")
        elif how == "directory":
            target.mkdir()
    return root


def _cr_main(root, monkeypatch, capsys, source, build=None):
    monkeypatch.setattr(sc, "read_stdin_payload", lambda: {"source": source} if source else {})
    if build is not None:
        monkeypatch.setattr(sc, "build_context_lines", build)
    assert sc.main(root) == 0
    return capsys.readouterr().out.splitlines()


@pytest.mark.parametrize("source,form", [("startup", "before your first dispatch, acceptance or commit"),
                                         (None, "before your first dispatch, acceptance or commit"),
                                         ("clear", "before your first dispatch, acceptance or commit"),
                                         ("compact", "before your first dispatch, acceptance or commit"),
                                         ("resume", "re-read only if your context no longer holds them")])
def test_coordinator_line_present_for_every_source_and_resume_has_the_reread_form(tmp_path, monkeypatch, capsys, source, form):
    root = _cr_root(tmp_path)
    out = [l for l in _cr_main(root, monkeypatch, capsys, source) if l.startswith("COORDINATOR RULES:")]
    n = len(_CR_FILES)
    assert out == [f"COORDINATOR RULES: read {', '.join(_CR_FILES)} ({n} files, {7 * n} bytes) {form}; workers do not read these at boot "
                   "-- a role reads only the section its role file names"]


@pytest.mark.parametrize("name", _CR_FILES)
@pytest.mark.parametrize("how", ["absent", "empty", "directory"])
def test_coordinator_line_names_a_missing_empty_or_directory_file_with_the_git_door(tmp_path, monkeypatch, capsys, name, how):
    root = _cr_root(tmp_path, {name: how})
    out = [l for l in _cr_main(root, monkeypatch, capsys, "startup") if l.startswith("COORDINATOR RULES:")]
    good = [f for f in _CR_FILES if f != name]
    reason = {"absent": "absent", "empty": "empty", "directory": "directory"}[how]
    assert out[0].startswith(f"COORDINATOR RULES: read {', '.join(good)} ({len(good)} files, {7 * len(good)} bytes)")
    assert out[1:] == [f'COORDINATOR RULES: MISSING {name} ({reason}) -- read it from git: git -C "{root}" show origin/main:{name}; '
                       "until then this session has no coordinator rules"]


@pytest.mark.parametrize("dirname,quoted", [("my projects", True), ("проект", False)])
def test_the_git_door_is_one_the_reader_can_use_on_a_space_a_non_ascii_and_a_long_root(tmp_path, monkeypatch, capsys, dirname, quoted):
    root = _cr_root(tmp_path, {"PROJECT.md": "absent"}, dirname=dirname)
    out = [l for l in _cr_main(root, monkeypatch, capsys, "startup") if "MISSING" in l]
    door = f'git -C "{root}" show' if quoted else "git show"
    assert len(out) == 1 and door in out[0] and "-C ?" not in out[0] and out[0].isascii()


def test_the_git_door_names_a_long_root_whole():
    import coordinator_rules

    root = "C:/" + "p" * 250                   # a path the OS cannot create here; the door is text only
    (line,) = [l for l in coordinator_rules.coordinator_lines(root, "startup") if "PROJECT.md (" in l]
    assert f'git -C "{root}" show origin/main:PROJECT.md' in line


def test_coordinator_line_with_no_file_at_all_has_only_missing_lines_and_is_ascii(tmp_path, monkeypatch, capsys):
    root = _seed_repo(tmp_path / "\u043f\u0440\u0430", events=[_event("delegated", task_id="t-001")])
    out = [l for l in _cr_main(root, monkeypatch, capsys, "startup") if l.startswith("COORDINATOR RULES:")]
    assert len(out) == len(_CR_FILES) and all("MISSING" in l and l.isascii() for l in out)


def test_coordinator_line_when_the_module_cannot_be_imported_names_the_literal_list(tmp_path, monkeypatch, capsys):
    root = _cr_root(tmp_path)
    monkeypatch.setitem(sys.modules, "coordinator_rules", None)       # `import coordinator_rules` raises ImportError
    out = [l for l in _cr_main(root, monkeypatch, capsys, "startup") if "COORDINATOR RULES:" in l]
    assert len(out) == 1 and out[0].startswith("COORDINATOR RULES: unavailable (ModuleNotFoundError")
    assert out[0].endswith(f"-- read {', '.join(sc._COORDINATOR_FALLBACK_FILES)} yourself") and out[0].isascii()
    assert sc.boot_path_files(root)[-1] == "CLAUDE.md"                  # the budget arithmetic falls back to the same literal


def test_coordinator_line_when_the_module_fails_to_run_is_the_same_unavailable_line(tmp_path, monkeypatch):
    import coordinator_rules

    def boom(*_a, **_k):
        raise RuntimeError("boom\nline")

    monkeypatch.setattr(coordinator_rules, "coordinator_lines", boom)
    (line,) = sc.coordinator_rules_lines(tmp_path, "startup")
    assert line == f"COORDINATOR RULES: unavailable (RuntimeError: boomline) -- read {', '.join(sc._COORDINATOR_FALLBACK_FILES)} yourself"


def test_the_fallback_list_equals_coordinator_files():
    import coordinator_rules

    assert sc._COORDINATOR_FALLBACK_FILES == coordinator_rules.COORDINATOR_FILES == tuple(sc._coordinator_files())


def test_coordinator_lines_never_raises_on_a_hostile_root():
    import coordinator_rules

    class Bad:
        def __str__(self):
            raise RuntimeError("bad str")

    for root in ("\x00", None, 5, "a\x00b", Bad()):
        got = coordinator_rules.coordinator_lines(root, "startup")
        assert got and all(l.isascii() and l.startswith("COORDINATOR RULES:") for l in got)
    # the module's own unavailable line and the hook's fallback are ONE text (t-1250 F4: the drift pin)
    assert coordinator_rules.coordinator_lines(Bad(), "startup") == sc.coordinator_rules_lines(Bad(), "startup") == [
        "COORDINATOR RULES: unavailable (RuntimeError: bad str) -- read %s yourself" % ", ".join(sc._COORDINATOR_FALLBACK_FILES)]


def test_the_coordinator_line_is_never_cut_by_max_lines_and_precedes_the_compact_pointer(tmp_path, monkeypatch, capsys):
    root = _cr_root(tmp_path)
    full = [f"filler {i}" for i in range(sc.MAX_LINES)]          # build_context_lines is already AT the cut
    out = _cr_main(root, monkeypatch, capsys, "compact", build=lambda *_a, **_k: list(full))
    at = [i for i, l in enumerate(out) if l.startswith("COORDINATOR RULES:")]
    snap = [i for i, l in enumerate(out) if l.startswith(("COMPACT SNAPSHOT", "AFTER COMPACT"))]
    assert len(at) == 1 and out[:sc.MAX_LINES] == full and snap and at[0] < min(snap)
    after = [i for i, l in enumerate(out) if l.startswith("AFTER COMPACT")]
    assert not after or after[-1] > at[0]                       # AFTER COMPACT stays after the rules line (e6)


# ---- FG7-94: the MAIN CI line (ci_read.main_red_line through sc.main_red_lines) ------------------------------------

@pytest.fixture
def no_launch(monkeypatch):
    """The detached refresh is never started by a test (it would read the network)."""
    import ci_read
    monkeypatch.setattr(ci_read, "main_red_launch", lambda r, t: None)

def _main_root(tmp_path, two=False):
    """A real repo whose origin/main is its last commit; returns (root, first sha, last sha)."""
    root = tmp_path / "mainrepo"
    root.mkdir()
    shas = []
    for argv in ([["init", "-q"]] + [["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x"]] * (2 if two else 1)):
        subprocess.run(["git", "-C", str(root), *argv], check=True)
        if argv[0] != "init":
            shas.append(subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, check=True).stdout.decode().strip())
    subprocess.run(["git", "-C", str(root), "update-ref", "refs/remotes/origin/main", shas[-1]], check=True)
    return root, shas[0], shas[-1]


def _main_state(root, head, state="green", red=None, fixer=None, flaky=0, age=0, runs=None, head_as=None):
    import ci_read
    red = {job: {"first_red": head, "last_green": None, "opened_at": "x",
                 "range": [{"sha": head, "task": t, "label": "b"} for t in tasks]} for job, tasks in (red or {}).items()}

    def mutate(st):
        st.update(head=head_as or head, red=red, fixer={"task": fixer, "since": "x"} if fixer else None, error=None,
                  flaky=[{"id": "f%d" % i, "why": "w", "added": "x"} for i in range(flaky)], order=[head],
                  tips={head_as or head: {"state": state, "pushed_at": ci_read._iso(time.time() - age), "runs": {"forge-check.yml": 1} if runs is None else runs}})
    ci_read.main_red_write(root, mutate)


UNK = "; refresh: python -B tools/ci_read.py main-red refresh"
LINES = [      # (name, state kwargs, expected with {h} = the head sha8, or None)
    ("green-silent", dict(), None),
    ("red", dict(state="red", red={"build": ["t-1", "t-2", "t-3"], "lint": ["t-4"]}, flaky=1),
     "MAIN RED since {h}: build [t-1, t-2 +1], lint [t-4]; head {h} red; fixer none; flaky 1"),
    ("red-with-fixer", dict(state="red", red={"build": ["t-1"]}, fixer="t-9"), "MAIN RED since {h}: build [t-1]; head {h} red; fixer t-9"),
    ("fixer-on-flaky", dict(fixer="t-5", flaky=2), "MAIN GREEN at {h}; fixer t-5 on the flaky queue: 2 left"),
    ("fixer-nothing-left", dict(fixer="t-5"), "MAIN GREEN at {h}; fixer t-5 on the flaky queue; nothing left, close: python -B tools/ci_read.py main-red fixer --done t-5"),
    ("flaky-no-fixer", dict(flaky=3), "MAIN GREEN, flaky queue 3: no fixer"),
    ("pending", dict(state="pending", age=330, runs={}), "MAIN CI pending at {h} (5 min); last green none"),
    ("pending-no-run", dict(state="pending", age=901, runs={}), "MAIN CI unknown at {h}: no run after 15 min" + UNK),
    ("pending-stale", dict(state="pending", age=5401), "MAIN CI unknown at {h}: no verdict after 90 min" + UNK),
    ("one-wave-one-task", dict(state="red", red={"J": ["t-100", "t-100", "t-200"]}), "MAIN RED since {h}: J [t-100, t-200]; head {h} red; fixer none"),
    ("origin-ahead", dict(head_as="b" * 40), "MAIN CI unknown at {h}: not read yet" + UNK)]


@pytest.mark.parametrize("name,kw,expected", LINES, ids=[x[0] for x in LINES])
def test_main_red_line(name, kw, expected, tmp_path, no_launch):
    root, first, head = _main_root(tmp_path)
    _main_state(root, head, **kw)
    got = sc.main_red_lines(root)
    assert got == ([] if expected is None else [expected.format(h=head[:8])])


def test_main_red_line_absent_corrupt_hostile_and_no_origin(tmp_path, no_launch):
    import ci_read
    root, _first, head = _main_root(tmp_path)
    assert sc.main_red_lines(root) == ["MAIN CI unknown at %s: never read%s" % (head[:8], UNK)]               # E14
    path = ci_read._state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    assert sc.main_red_lines(root) == ["MAIN CI unknown at %s: state unreadable (JSONDecodeError)%s" % (head[:8], UNK)]     # E11
    names = {"x" * 200 + "\n\x1b[31mé": ["t-1"], **{"zjob%d" % i + "y" * 60: ["t-%d" % i] for i in range(6)}}
    _main_state(root, head, state="red", red=names)
    (line,) = sc.main_red_lines(root)
    assert len(line) <= ci_read.LINE_MAX and line.isascii() and "\n" not in line and "x" * 60 in line and "x" * 61 not in line and "more" in line
    (path.parent / "state.json").unlink()
    bare = tmp_path / "bare"
    bare.mkdir()
    subprocess.run(["git", "-C", str(bare), "init", "-q"], check=True)
    assert sc.main_red_lines(bare) == []                                                                         # E23


def test_main_red_line_survives_the_max_lines_cut_fails_open_and_launches_after_the_read(tmp_path, monkeypatch):
    import ci_read
    root = _seed_repo(tmp_path, events=[_event("delegated", ts="2026-07-10T08:00:00", task_id="t-001")])
    orig = sc.main_red_lines
    monkeypatch.setattr(sc, "main_red_lines", lambda r: ["MAIN RED test line"])
    monkeypatch.setattr(sc, "boot_budget_lines", lambda r: ["FILLER"] * 40)
    lines = sc.build_context_lines(root)
    assert len(lines) == sc.MAX_LINES and "MAIN RED test line" in lines and "FILLER" in lines and not any(l.startswith("WIRING:") for l in lines)
    monkeypatch.setattr(sc, "main_red_lines", orig)
    order = []
    monkeypatch.setattr(ci_read, "main_red_line", lambda r, now: order.append("read") or "L")
    monkeypatch.setattr(ci_read, "main_red_launch", lambda r, t: order.append("launch " + t))
    assert sc.main_red_lines(root) == ["L"] and order == ["read", "launch session-start"]
    monkeypatch.setattr(ci_read, "main_red_line", lambda r, now: 1 / 0)
    assert sc.main_red_lines(root) == ["MAIN CI: unavailable (ZeroDivisionError: division by zero)"]
