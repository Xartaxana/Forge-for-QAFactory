"""Tests for tools/usage_report.py. No network, no LLM calls -- pure
parsing/SQL over a small sanitized fixture transcript
(tools/fixtures/sample_transcript.jsonl, synthetic usage numbers only,
no real prompt content).

Run from tools/: python -m pytest test_usage_report.py
"""

import json
import re
import sqlite3
from pathlib import Path

import pytest

import usage_report
from usage_report import (
    PricesError,
    SCHEMA,
    SKIP_MODELS,
    accounted_cost,
    backfill_costs,
    build_report,
    format_report,
    import_transcripts,
    iter_assistant_turns,
    load_prices,
    main,
    transcript_glob,
)

# The price table now lives in tools/model_prices.json (F6-6); these
# aliases keep the older tests below reading the same names.
_TABLE = load_prices()
# F6-24: a model is a ModelPrice record now; the older tests read (input, output) pairs of the file's models
PRICES_PER_TOKEN_USD = {m: (p.input, p.output) for m, p in _TABLE["models"].items()}
CACHE_WRITE_MULTIPLIER = _TABLE["cache_write_multiplier"]
CACHE_READ_MULTIPLIER = _TABLE["cache_read_multiplier"]

FIXTURE = str(Path(__file__).parent / "fixtures" / "sample_transcript.jsonl")


def _write_jsonl(path: Path, lines: list):
    """Test helper: write a list of dicts as a JSONL transcript file,
    creating parent directories as needed (used to build the nested
    <project>/<session>/subagents/agent-*.jsonl layout in tmp dirs,
    since the projects root cannot be hardcoded -- Delegated Task 6)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for obj in lines:
            f.write(json.dumps(obj) + "\n")


def _assistant_line(session_id=None, request_id="req-x", is_sidechain=False,
                     model="claude-sonnet-5", uuid="uuid-x", extra=None):
    obj = {
        "type": "assistant",
        "uuid": uuid,
        "requestId": request_id,
        "isSidechain": is_sidechain,
        "timestamp": "2026-07-07T12:00:00.000Z",
        "parentUuid": None,
        "message": {
            "id": f"msg_{uuid}",
            "model": model,
            "role": "assistant",
            "usage": {
                "input_tokens": 10, "output_tokens": 5,
                "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
            },
            "content": [{"type": "text", "text": "synthetic fixture text"}],
        },
    }
    if session_id is not None:
        obj["sessionId"] = session_id
    if extra:
        obj.update(extra)
    return obj


@pytest.fixture()
def db_file(tmp_path):
    return tmp_path / "requests.db"


# ---- parsing ----

def test_parses_only_assistant_lines_and_skips_synthetic():
    turns = list(iter_assistant_turns(FIXTURE))
    models = [t["model"] for t in turns]
    assert "<synthetic>" not in models
    # 8 lines in the fixture: 1 user line and 1 <synthetic> line must be
    # excluded, leaving 6 assistant turns (including the 2 duplicate-
    # requestId lines, which iter_assistant_turns does NOT dedupe --
    # that's import_transcripts's job via the UNIQUE constraint).
    assert len(turns) == 6


def test_skips_non_assistant_line_types():
    turns = list(iter_assistant_turns(FIXTURE))
    for t in turns:
        assert t["model"] != "<synthetic>"
    # the 'user' line in the fixture carries no usage field and no
    # model -- confirm nothing resembling it leaked through.
    assert all(t["model"] for t in turns)


def test_session_id_prefers_json_field_over_filename():
    turns = list(iter_assistant_turns(FIXTURE))
    sessions = {t["session_id"] for t in turns}
    assert sessions == {"session-aaa", "session-bbb"}


def test_dedupe_key_shared_by_split_turn():
    turns = list(iter_assistant_turns(FIXTURE))
    # req-0002 appears on two JSONL lines (uuid-0002, uuid-0003) with
    # identical usage -- both must produce the SAME dedupe_key so the
    # importer's UNIQUE constraint collapses them to one row.
    dupe_keys = [t["dedupe_key"] for t in turns if t["dedupe_key"].endswith(":req-0002")]
    assert len(dupe_keys) == 2
    assert dupe_keys[0] == dupe_keys[1]


# ---- idempotent import / dedup ----

def test_import_is_idempotent(db_file):
    rows1, sessions1, warnings1 = import_transcripts(FIXTURE, db_file)
    rows2, sessions2, warnings2 = import_transcripts(FIXTURE, db_file)

    conn = sqlite3.connect(db_file)
    count = conn.execute("SELECT COUNT(*) FROM cc_usage").fetchone()[0]

    # 6 assistant turns in the fixture, but req-0002's split lines
    # collapse to 1 row -> 5 distinct API turns.
    assert count == 5
    assert rows1 == 5
    # Second run finds nothing new to insert (INSERT OR IGNORE).
    assert rows2 == 0


def test_import_does_not_touch_requests_table(db_file):
    # Pre-seed a `requests` table row (as the gateway would) and verify
    # the importer never touches it -- cc_usage is a new table, spec
    # explicitly forbids touching `requests`.
    conn = sqlite3.connect(db_file)
    conn.execute(
        "CREATE TABLE requests (id INTEGER PRIMARY KEY, model TEXT)"
    )
    conn.execute("INSERT INTO requests (model) VALUES ('sentinel')")
    conn.commit()
    conn.close()

    import_transcripts(FIXTURE, db_file)

    conn = sqlite3.connect(db_file)
    row = conn.execute("SELECT model FROM requests").fetchone()
    assert row == ("sentinel",)


def test_cc_usage_schema_has_required_columns(db_file):
    import_transcripts(FIXTURE, db_file)
    conn = sqlite3.connect(db_file)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(cc_usage)")}
    for expected in (
        "ts", "project", "session_id", "turn_index", "model",
        "input_tokens", "output_tokens", "cache_creation_tokens",
        "cache_read_tokens", "accounted_cost_usd", "traffic_kind",
        "is_sidechain",
    ):
        assert expected in columns


def test_is_sidechain_flag_recorded(db_file):
    import_transcripts(FIXTURE, db_file)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE model = 'claude-opus-4-8'"
    ).fetchone()
    assert row["is_sidechain"] == 1
    assert row["traffic_kind"] == "real"


# ---- price math including cache rates ----

def test_accounted_cost_known_model():
    cost, warning = accounted_cost(
        "claude-sonnet-5",
        input_tokens=1000, output_tokens=200,
        cache_creation_tokens=500, cache_read_tokens=4000,
    )
    assert warning is None
    input_price, output_price = PRICES_PER_TOKEN_USD["claude-sonnet-5"]
    expected = (
        1000 * input_price
        + 200 * output_price
        + 500 * input_price * CACHE_WRITE_MULTIPLIER
        + 4000 * input_price * CACHE_READ_MULTIPLIER
    )
    assert cost == pytest.approx(expected)


def test_accounted_cost_cache_rates_are_distinct_from_base_input():
    # cache write and cache read must NOT be priced the same as a bare
    # input token, or the "cache write/read price distinction"
    # requirement is violated.
    base_cost, _ = accounted_cost("claude-sonnet-5", 1000, 0, 0, 0)
    write_cost, _ = accounted_cost("claude-sonnet-5", 0, 0, 1000, 0)
    read_cost, _ = accounted_cost("claude-sonnet-5", 0, 0, 0, 1000)
    assert write_cost > base_cost  # 1.25x premium
    assert read_cost < base_cost  # 0.1x discount
    assert write_cost != read_cost


# ---- unknown-model warning path ----

def test_unknown_model_cost_is_none_without_a_per_turn_warning():
    cost, warning = accounted_cost("claude-unknown-model-x", 500, 100, 0, 0)
    assert cost is None
    assert warning is None  # F6-6: the report prints one summary line per model


def test_unknown_model_never_silently_zero(db_file):
    import_transcripts(FIXTURE, db_file)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE model = 'claude-unknown-model-x'"
    ).fetchone()
    assert row is not None
    assert row["accounted_cost_usd"] is None  # None, never 0.0


def test_report_surfaces_unknown_model_as_one_summary_line(db_file):
    _, _, warnings = import_transcripts(FIXTURE, db_file)
    assert warnings == []
    text = format_report(build_report(db_file, days=None), warnings)
    assert text.count("unknown price: claude-unknown-model-x: 1 turn(s)") == 1
    assert "WARNING" not in text


# ---- report building ----

def test_build_report_totals_exclude_unknown_cost_from_sum(db_file):
    import_transcripts(FIXTURE, db_file)
    report = build_report(db_file, days=None)
    assert report["totals"]["rows"] == 5
    assert report["totals"]["unknown_cost_rows"] == 1
    # accounted_cost_usd sum should be a real float, not NaN/None, and
    # should not silently include the unknown-model row as $0 hidden
    # inside a total that looks complete.
    assert report["totals"]["accounted_cost_usd"] > 0


def test_build_report_per_project_and_per_session(db_file):
    import_transcripts(FIXTURE, db_file)
    report = build_report(db_file, days=None)
    # both fixture rows share one project dir (the fixture file's own
    # parent directory name), but two distinct session_ids.
    assert len(report["per_project"]) == 1
    session_keys = {s["session_id"] for s in report["top_sessions_by_cost"]}
    assert "session-aaa" in session_keys
    assert "session-bbb" in session_keys


def test_build_report_cache_read_share_of_input(db_file):
    import_transcripts(FIXTURE, db_file)
    report = build_report(db_file, days=None)
    share = report["cache_read_share_of_input"]
    assert share is not None
    assert 0 <= share <= 1


def test_build_report_sidechain_share(db_file):
    import_transcripts(FIXTURE, db_file)
    report = build_report(db_file, days=None)
    assert report["sidechain_tokens"] > 0
    assert report["sidechain_share_of_tokens"] is not None
    assert 0 < report["sidechain_share_of_tokens"] < 1


def test_build_report_days_filter_excludes_old_rows(db_file):
    # The fixture's timestamps are 2026-07-01; a days=1 window relative
    # to "now" (run date is long after the fixture dates) should
    # exclude everything.
    import_transcripts(FIXTURE, db_file)
    report = build_report(db_file, days=1)
    assert report["totals"]["rows"] == 0


# ---- subagent/sidechain transcripts (Delegated Task 6) ----
#
# Real subagent transcripts live at
# <project>/<session-id>/subagents/agent-*.jsonl, one directory layer
# deeper than the top-level <project>/<session>.jsonl layout. The
# projects root cannot be hardcoded here (real path is
# ~/.claude/projects, but tests must not depend on the developer
# machine's home directory), so each test below builds its own tmp_path
# tree with both layouts and points transcript_glob()/import_transcripts
# at it via the base_dir override.

def test_project_attribution_top_level_layout(tmp_path):
    path = tmp_path / "myproj" / "session-1.jsonl"
    _write_jsonl(path, [_assistant_line(session_id="session-1")])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    assert turns[0]["project"] == "myproj"
    assert turns[0]["session_id"] == "session-1"


def test_project_attribution_subagent_layout(tmp_path):
    path = tmp_path / "myproj" / "session-1" / "subagents" / "agent-x.jsonl"
    _write_jsonl(path, [_assistant_line(session_id="session-1", is_sidechain=True)])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    # Must be "myproj" (the real project), NOT "subagents" (the file's
    # immediate parent dir name) and not "session-1" either.
    assert turns[0]["project"] == "myproj"
    assert turns[0]["session_id"] == "session-1"
    assert turns[0]["is_sidechain"] == 1


def test_subagent_layout_session_id_fallback_uses_directory_not_agent_filename(tmp_path):
    # No "sessionId" JSON field at all -- the fallback must derive the
    # session id from the <session-id> directory name one level above
    # subagents/, NOT from the file's own stem (which is the sub-agent
    # id, e.g. "agent-y", and would be wrong as a session id).
    path = tmp_path / "myproj2" / "sess-xyz" / "subagents" / "agent-y.jsonl"
    _write_jsonl(path, [_assistant_line(session_id=None, is_sidechain=True)])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    assert turns[0]["session_id"] == "sess-xyz"
    assert turns[0]["project"] == "myproj2"


def test_transcript_glob_returns_two_patterns(tmp_path):
    patterns = transcript_glob(base_dir=tmp_path)
    assert isinstance(patterns, list)
    assert len(patterns) == 2
    assert str(tmp_path) in patterns[0]
    assert patterns[0].endswith("*.jsonl")
    assert "subagents" in patterns[1]
    assert patterns[1].endswith("*.jsonl")


def test_import_transcripts_scans_both_layouts_together(tmp_path, db_file):
    top_level = tmp_path / "projA" / "session-1.jsonl"
    _write_jsonl(top_level, [
        _assistant_line(session_id="session-1", request_id="req-parent-1"),
    ])
    sub = tmp_path / "projA" / "session-1" / "subagents" / "agent-a1.jsonl"
    _write_jsonl(sub, [
        _assistant_line(session_id="session-1", request_id="req-sub-1", is_sidechain=True),
    ])

    patterns = transcript_glob(base_dir=tmp_path)
    rows_imported, sessions_seen, warnings = import_transcripts(patterns, db_file)

    assert rows_imported == 2
    assert sessions_seen == {"session-1"}

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM cc_usage ORDER BY dedupe_key").fetchall()
    assert len(rows) == 2
    by_sidechain = {r["is_sidechain"] for r in rows}
    assert by_sidechain == {0, 1}
    for r in rows:
        # Both rows must attribute to the real project "projA", never
        # "subagents" or the session id.
        assert r["project"] == "projA"
        assert r["session_id"] == "session-1"
    # No dedupe_key collision between the parent-session row and the
    # subagent row sharing the same session_id.
    dedupe_keys = {r["dedupe_key"] for r in rows}
    assert len(dedupe_keys) == 2


def test_import_transcripts_subagent_layout_is_idempotent(tmp_path, db_file):
    sub = tmp_path / "projB" / "session-2" / "subagents" / "agent-b1.jsonl"
    _write_jsonl(sub, [
        _assistant_line(session_id="session-2", request_id="req-sub-2", is_sidechain=True),
    ])
    patterns = transcript_glob(base_dir=tmp_path)

    rows1, _, _ = import_transcripts(patterns, db_file)
    rows2, _, _ = import_transcripts(patterns, db_file)

    assert rows1 == 1
    assert rows2 == 0  # second run finds nothing new

    conn = sqlite3.connect(db_file)
    count = conn.execute("SELECT COUNT(*) FROM cc_usage").fetchone()[0]
    assert count == 1



# ---- agent attribution + haiku pricing (Delegated Task 7) ----

def test_migration_adds_columns_to_old_schema_db_without_data_loss(db_file):
    # Simulate a pre-Task-7 database: the OLD schema (no agent_id/
    # agent_type columns), with a real row already in it.
    conn = sqlite3.connect(db_file)
    conn.execute(
        """
        CREATE TABLE cc_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            project TEXT NOT NULL,
            session_id TEXT NOT NULL,
            turn_index INTEGER NOT NULL,
            model TEXT NOT NULL,
            input_tokens INTEGER NOT NULL,
            output_tokens INTEGER NOT NULL,
            cache_creation_tokens INTEGER NOT NULL,
            cache_read_tokens INTEGER NOT NULL,
            accounted_cost_usd REAL,
            traffic_kind TEXT NOT NULL DEFAULT 'real',
            is_sidechain INTEGER NOT NULL DEFAULT 0,
            dedupe_key TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.execute(
        """
        INSERT INTO cc_usage
            (ts, project, session_id, turn_index, model, input_tokens,
             output_tokens, cache_creation_tokens, cache_read_tokens,
             accounted_cost_usd, traffic_kind, is_sidechain, dedupe_key)
        VALUES ('2026-07-01T00:00:00Z', 'oldproj', 'old-session', 0,
                'claude-sonnet-5', 100, 50, 0, 0, 0.001, 'real', 0, 'old-session:req-old')
        """
    )
    conn.commit()
    conn.close()

    # Any import (even of an empty/unrelated transcript set) goes
    # through _connect(), which must migrate the existing table
    # in-place rather than erroring or dropping data.
    import_transcripts(FIXTURE, db_file)

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    columns = {row[1] for row in conn.execute("PRAGMA table_info(cc_usage)")}
    assert "agent_id" in columns
    assert "agent_type" in columns

    old_row = conn.execute(
        "SELECT * FROM cc_usage WHERE dedupe_key = 'old-session:req-old'"
    ).fetchone()
    assert old_row is not None
    assert old_row["model"] == "claude-sonnet-5"
    assert old_row["accounted_cost_usd"] == pytest.approx(0.001)
    assert old_row["agent_id"] is None
    assert old_row["agent_type"] is None


def test_agent_id_and_type_stored_for_subagent_layout_line(tmp_path, db_file):
    path = tmp_path / "myproj" / "session-1" / "subagents" / "agent-x.jsonl"
    _write_jsonl(path, [
        _assistant_line(
            session_id="session-1", is_sidechain=True,
            extra={"agentId": "agent-x-id", "attributionAgent": "test-maintainer"},
        ),
    ])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    assert turns[0]["agent_id"] == "agent-x-id"
    assert turns[0]["agent_type"] == "test-maintainer"

    import_transcripts(str(tmp_path / "*" / "*" / "subagents" / "*.jsonl"), db_file)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE session_id = 'session-1'"
    ).fetchone()
    assert row["agent_id"] == "agent-x-id"
    assert row["agent_type"] == "test-maintainer"


def test_top_level_line_gets_null_agent_id():
    # The fixture's top-level lines carry neither agentId nor
    # attributionAgent (real top-level transcripts never do either,
    # per the module docstring).
    turns = list(iter_assistant_turns(FIXTURE))
    assert all(t["agent_id"] is None for t in turns)
    assert all(t["agent_type"] is None for t in turns)


def test_haiku_cost_computed_no_warning():
    cost, warning = accounted_cost(
        "claude-haiku-4-5-20251001",
        input_tokens=1_000_000, output_tokens=1_000_000,
        cache_creation_tokens=0, cache_read_tokens=0,
    )
    assert warning is None
    assert cost == pytest.approx(1.00 + 5.00)


def test_haiku_bare_id_also_priced():
    cost, warning = accounted_cost("claude-haiku-4-5", 1_000_000, 0, 0, 0)
    assert warning is None
    assert cost == pytest.approx(1.00)


# ---------------------------------------------------------------------
# claude-opus-5 pricing (a newly-bound model must never be a silent
# $0): positive control (a priced model) and its negative control (a
# totally unknown model id) in the same shape.
# ---------------------------------------------------------------------


def test_claude_opus_5_is_priced_identically_to_opus_4_8():
    cost, warning = accounted_cost(
        "claude-opus-5", 1_000_000, 1_000_000, 0, 0,
    )
    assert warning is None
    assert cost == pytest.approx(5.00 + 25.00)
    assert PRICES_PER_TOKEN_USD["claude-opus-5"] == PRICES_PER_TOKEN_USD["claude-opus-4-8"]


def test_totally_unknown_model_id_yields_cost_none_never_zero():
    """Negative control for the positive claim above: an unrecognized
    model id must yield cost=None (an unpriced window stays visibly
    unpriced), never a silent 0.0."""
    cost, warning = accounted_cost("totally-unknown-model-xyz", 1_000_000, 1_000_000, 0, 0)
    assert cost is None
    assert cost != 0.0


def test_empty_and_none_model_id_yield_cost_none_no_exception():
    cost_empty, _ = accounted_cost("", 1_000_000, 0, 0, 0)
    assert cost_empty is None
    cost_none, _ = accounted_cost(None, 1_000_000, 0, 0, 0)
    assert cost_none is None


def test_prices_per_token_usd_existing_rows_unchanged():
    """Regression pin: the pre-existing price rows are untouched by the
    claude-opus-5 addition."""
    assert PRICES_PER_TOKEN_USD["claude-fable-5"] == (10.00 / 1_000_000, 50.00 / 1_000_000)
    assert PRICES_PER_TOKEN_USD["claude-opus-4-8"] == (5.00 / 1_000_000, 25.00 / 1_000_000)
    assert PRICES_PER_TOKEN_USD["claude-sonnet-5"] == (3.00 / 1_000_000, 15.00 / 1_000_000)
    assert PRICES_PER_TOKEN_USD["claude-sonnet-4-6"] == (3.00 / 1_000_000, 15.00 / 1_000_000)
    assert PRICES_PER_TOKEN_USD["claude-haiku-4-5-20251001"] == (1.00 / 1_000_000, 5.00 / 1_000_000)
    assert PRICES_PER_TOKEN_USD["claude-haiku-4-5"] == (1.00 / 1_000_000, 5.00 / 1_000_000)


def test_claude_opus_5_only_bare_form_no_dated_variant():
    """Only the bare "claude-opus-5" id is priced -- unlike haiku, no
    dated variant (claude-opus-5-YYYYMMDD) has been observed for this
    model, so none is added (SKIP_MODELS is also unchanged by this
    addition). F6-24 re-pin: the old pin said "no id starts with
    claude-opus-5-", which the new model claude-opus-5-5 legitimately
    breaks; a DATED variant is what the pin is about."""
    assert "claude-opus-5" in PRICES_PER_TOKEN_USD  # priced models only
    assert not any(
        re.fullmatch(r"claude-opus-5-\d{8}", model_id) for model_id in PRICES_PER_TOKEN_USD
    )
    assert SKIP_MODELS == {"<synthetic>"}


def test_backfill_fills_agent_fields_and_null_costs_idempotently(tmp_path, db_file):
    # Simulate a row imported BEFORE Task 7: no agent_id/agent_type,
    # and a NULL cost because its model (haiku) wasn't priced yet at
    # import time.
    sub = tmp_path / "projB" / "session-9" / "subagents" / "agent-b9.jsonl"
    _write_jsonl(sub, [
        _assistant_line(
            session_id="session-9", request_id="req-b9", is_sidechain=True,
            model="claude-haiku-4-5-20251001",
            extra={"agentId": "agent-b9-id", "attributionAgent": "builder"},
        ),
    ])

    conn = sqlite3.connect(db_file)
    conn.execute(SCHEMA)
    conn.execute(
        """
        INSERT INTO cc_usage
            (ts, project, session_id, turn_index, model, input_tokens,
             output_tokens, cache_creation_tokens, cache_read_tokens,
             accounted_cost_usd, traffic_kind, is_sidechain, agent_id,
             agent_type, dedupe_key)
        VALUES ('2026-07-07T12:00:00.000Z', 'projB', 'session-9', 0,
                'claude-haiku-4-5-20251001', 10, 5, 0, 0, NULL, 'real', 1,
                NULL, NULL, 'session-9:req-b9')
        """
    )
    conn.commit()
    conn.close()

    patterns = str(tmp_path / "*" / "*" / "subagents" / "*.jsonl")
    rows1, _, _ = import_transcripts(patterns, db_file)
    assert rows1 == 0  # the row already existed; nothing NEW inserted

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM cc_usage WHERE dedupe_key = 'session-9:req-b9'").fetchone()
    assert row["agent_id"] == "agent-b9-id"
    assert row["agent_type"] == "builder"
    assert row["accounted_cost_usd"] is not None
    assert row["accounted_cost_usd"] > 0
    conn.close()

    # Idempotent: a second run updates 0 rows (the columns are already filled).
    rows2, _, _ = import_transcripts(patterns, db_file)
    assert rows2 == 0
    conn = sqlite3.connect(db_file)
    updated_again = backfill_costs(conn)
    conn.commit()
    conn.close()
    assert updated_again == 0


# ---- deep subagent transcripts under workflows/ (regression) ----
#
# A workflow tool can write agent transcripts at a THIRD depth, still
# under .../subagents/ but nested further:
# <project>/<session>/subagents/workflows/wf_*/agent-*.jsonl. The
# Task 6 glob/detection (one directory deep only) silently missed
# these. Regression coverage below builds a tmp tree with all three
# layouts together (top-level session, flat subagent, deep workflow
# subagent) and confirms every one is counted.

def test_project_attribution_deep_workflow_subagent_layout(tmp_path):
    path = (
        tmp_path / "myproj" / "session-1" / "subagents" / "workflows"
        / "wf_abc123" / "agent-deep1.jsonl"
    )
    _write_jsonl(path, [_assistant_line(session_id="session-1", is_sidechain=True)])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    # Must attribute to the real project/session two levels above the
    # "subagents" ancestor, NOT "wf_abc123", "workflows", or
    # "subagents" itself.
    assert turns[0]["project"] == "myproj"
    assert turns[0]["session_id"] == "session-1"
    assert turns[0]["is_sidechain"] == 1


def test_deep_workflow_subagent_session_id_fallback_uses_directory_not_agent_filename(tmp_path):
    # No "sessionId" JSON field -- fallback must still resolve to the
    # session directory one level above "subagents/", regardless of
    # how many extra directories (workflows/wf_x/...) sit in between.
    path = (
        tmp_path / "myproj2" / "sess-xyz" / "subagents" / "workflows"
        / "wf_def456" / "agent-deep2.jsonl"
    )
    _write_jsonl(path, [_assistant_line(session_id=None, is_sidechain=True)])
    turns = list(iter_assistant_turns(str(path)))
    assert len(turns) == 1
    assert turns[0]["session_id"] == "sess-xyz"
    assert turns[0]["project"] == "myproj2"


def test_transcript_glob_recursive_pattern_covers_deep_workflow_files(tmp_path, db_file):
    # PIN: on the pre-fix code (glob pattern "subagents/*.jsonl", one
    # directory deep only), this test fails -- the deep workflow file
    # is invisible to both the glob and iter_assistant_turns's
    # "immediate parent == subagents" check. All three real-world
    # layouts, together:
    top_level = tmp_path / "projA" / "session-1.jsonl"
    _write_jsonl(top_level, [
        _assistant_line(session_id="session-1", request_id="req-top-1"),
    ])
    flat_sub = tmp_path / "projA" / "session-1" / "subagents" / "agent-flat1.jsonl"
    _write_jsonl(flat_sub, [
        _assistant_line(session_id="session-1", request_id="req-flat-1", is_sidechain=True),
    ])
    deep_sub = (
        tmp_path / "projA" / "session-1" / "subagents" / "workflows"
        / "wf_xyz789" / "agent-deep1.jsonl"
    )
    _write_jsonl(deep_sub, [
        _assistant_line(session_id="session-1", request_id="req-deep-1", is_sidechain=True),
    ])
    # A workflow journal.jsonl sitting right next to the deep agent
    # file, real-shape lines (type: "started"/"result", no
    # message.usage) -- must stay inert, matched by the wider glob but
    # contributing zero rows, not an error.
    journal = deep_sub.parent / "journal.jsonl"
    _write_jsonl(journal, [
        {"type": "started", "key": "v2:abc", "agentId": "agent-deep1"},
        {"type": "result", "key": "v2:abc", "agentId": "agent-deep1", "result": {"summary": "ok"}},
    ])

    patterns = transcript_glob(base_dir=tmp_path)
    rows_imported, sessions_seen, warnings = import_transcripts(patterns, db_file)

    # 3 real assistant turns (top-level + flat subagent + deep
    # workflow subagent); the journal.jsonl contributes 0.
    assert rows_imported == 3
    assert sessions_seen == {"session-1"}

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM cc_usage ORDER BY dedupe_key").fetchall()
    assert len(rows) == 3
    for r in rows:
        assert r["project"] == "projA"
        assert r["session_id"] == "session-1"
    request_ids_seen = {r["dedupe_key"].split(":", 1)[1] for r in rows}
    assert request_ids_seen == {"req-top-1", "req-flat-1", "req-deep-1"}


def test_import_transcripts_deep_workflow_layout_is_idempotent(tmp_path, db_file):
    deep_sub = (
        tmp_path / "projD" / "session-4" / "subagents" / "workflows"
        / "wf_qqq" / "agent-deep-idem.jsonl"
    )
    _write_jsonl(deep_sub, [
        _assistant_line(session_id="session-4", request_id="req-deep-idem", is_sidechain=True),
    ])
    patterns = transcript_glob(base_dir=tmp_path)

    rows1, _, _ = import_transcripts(patterns, db_file)
    rows2, _, _ = import_transcripts(patterns, db_file)

    assert rows1 == 1
    assert rows2 == 0

    conn = sqlite3.connect(db_file)
    count = conn.execute("SELECT COUNT(*) FROM cc_usage").fetchone()[0]
    assert count == 1


# ---- max-output-tokens dedup (regression) ----
#
# A split subagent turn's lines share input/cache tokens but carry a
# placeholder output_tokens (2-7) on every line except the one that
# carries the real value. Deduping by FIRST occurrence (INSERT OR
# IGNORE) keeps the placeholder. Tie-breaking on LAST occurrence
# instead is also wrong -- it depends on `sorted(paths)`/line order,
# which is wrong for the cross-file collision case covered further
# below (test_max_wins_for_cross_file_dedupe_key_collision) --
# occurrence order there is an artifact of glob/filename sort,
# unrelated to which file holds the real value. The fix ties-break on
# VALUE instead: output_tokens/accounted_cost_usd is only overwritten
# when the new line's output_tokens is STRICTLY GREATER than what is
# stored (MAX-wins), which is order-independent by construction. These
# tests build the split-turn shape directly (not via `_assistant_line`,
# which hardcodes output_tokens=5 for every line) and PIN the fix.

def _split_turn_lines(session_id, request_id, outputs, model="claude-sonnet-5",
                       is_sidechain=True, agent_id="agent-e1-id",
                       attribution_agent="builder"):
    lines = []
    for i, out in enumerate(outputs):
        obj = {
            "type": "assistant",
            "uuid": f"uuid-{request_id}-{i}",
            "requestId": request_id,
            "sessionId": session_id,
            "isSidechain": is_sidechain,
            "timestamp": "2026-07-14T00:00:00.000Z",
            "parentUuid": None,
            "message": {
                "id": f"msg_{request_id}_{i}",
                "model": model,
                "role": "assistant",
                "usage": {
                    "input_tokens": 100, "output_tokens": out,
                    "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
                },
                "content": [{"type": "text", "text": "synthetic fixture text"}],
            },
        }
        if is_sidechain:
            obj["agentId"] = agent_id
            obj["attributionAgent"] = attribution_agent
        lines.append(obj)
    return lines


def test_max_wins_for_split_turn_output_tokens(tmp_path, db_file):
    # PIN: on the pre-fix code (INSERT OR IGNORE, first line wins),
    # this test fails -- the stored output_tokens is 5 (the first
    # line's placeholder), not 383 (the real value, only on the last
    # line). It also passes under a last-wins fix, since here the real
    # value happens to be last -- see
    # test_max_wins_for_cross_file_dedupe_key_collision below for the
    # case that distinguishes max-wins from last-wins.
    sub = tmp_path / "projE" / "session-5" / "subagents" / "agent-e1.jsonl"
    _write_jsonl(sub, _split_turn_lines("session-5", "req-split-1", [5, 5, 5, 383]))

    rows_imported, _, _ = import_transcripts(str(sub), db_file)
    assert rows_imported == 1  # one distinct API turn (one dedupe_key)

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE dedupe_key = 'session-5:req-split-1'"
    ).fetchone()
    assert row is not None
    assert row["output_tokens"] == 383
    assert row["input_tokens"] == 100  # unaffected -- identical across all 4 lines
    input_price, output_price = PRICES_PER_TOKEN_USD["claude-sonnet-5"]
    assert row["accounted_cost_usd"] == pytest.approx(100 * input_price + 383 * output_price)


def test_max_wins_survives_reimport_and_stays_idempotent(tmp_path, db_file):
    # Re-running the importer over the SAME split-turn file must keep
    # the corrected value (not regress it back to a placeholder
    # mid-way through the re-scan) and must not inflate rows_imported
    # once the row is already correct. Under max-wins this also covers
    # the case where the re-scan re-presents an EQUAL (not smaller)
    # value -- output_tokens must stay at 383, not merely "not regress
    # to something smaller".
    sub = tmp_path / "projF" / "session-6" / "subagents" / "agent-f1.jsonl"
    _write_jsonl(sub, _split_turn_lines("session-6", "req-split-2", [3, 383]))

    rows1, _, _ = import_transcripts(str(sub), db_file)
    rows2, _, _ = import_transcripts(str(sub), db_file)

    assert rows1 == 1
    assert rows2 == 0  # nothing NEW on the second run

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE dedupe_key = 'session-6:req-split-2'"
    ).fetchone()
    assert row["output_tokens"] == 383
    count = conn.execute("SELECT COUNT(*) FROM cc_usage").fetchone()[0]
    assert count == 1  # still exactly one row, no duplicate


def test_max_wins_does_not_break_main_chain_identical_duplicates(tmp_path, db_file):
    # Main-chain duplicate lines are byte-identical (first == last) --
    # confirm the max-wins fix is a genuine no-op in value for that
    # already-correct case (equal values are never "strictly greater",
    # so the conditional UPDATE never fires).
    top_level = tmp_path / "projG" / "session-7.jsonl"
    _write_jsonl(top_level, _split_turn_lines(
        "session-7", "req-main-dup", [50, 50], is_sidechain=False,
    ))

    rows_imported, _, _ = import_transcripts(str(top_level), db_file)
    assert rows_imported == 1

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE dedupe_key = 'session-7:req-main-dup'"
    ).fetchone()
    assert row["output_tokens"] == 50


def test_max_wins_for_cross_file_dedupe_key_collision(tmp_path, db_file):
    # PIN: the same dedupe_key can appear in TWO DIFFERENT sibling
    # subagent files under one session's subagents/ directory, not
    # just on two lines of one file. This test builds a neutral
    # fixture reproducing that shape: a file that sorts FIRST carries
    # the real output_tokens; a file that sorts LATER carries only a
    # placeholder line for the SAME requestId.
    #
    # On a last-occurrence-wins fix, this test FAILS:
    # import_transcripts() processes files in sorted(paths) order, so
    # the later-sorting placeholder file overwrites the earlier-
    # sorting real value, leaving output_tokens == 3, not 3772.
    # Max-wins (the actual fix) is order-independent and keeps 3772
    # regardless of which file the glob visits first.
    session_id = "session-collision-1"
    request_id = "req-collision-1"
    real_file = tmp_path / "projH" / session_id / "subagents" / "agent-a-real.jsonl"
    placeholder_file = tmp_path / "projH" / session_id / "subagents" / "agent-b-placeholder.jsonl"
    assert str(real_file) < str(placeholder_file)  # sanity: matches the intended sort order

    _write_jsonl(real_file, _split_turn_lines(
        session_id, request_id, [3772], agent_id="agent-a-real", attribution_agent="worker-a",
    ))
    _write_jsonl(placeholder_file, _split_turn_lines(
        session_id, request_id, [3], agent_id="agent-b-placeholder", attribution_agent="worker-b",
    ))

    patterns = str(tmp_path / "*" / "*" / "subagents" / "*.jsonl")
    rows_imported, _, _ = import_transcripts(patterns, db_file)
    assert rows_imported == 1  # one distinct dedupe_key across the two files

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM cc_usage WHERE dedupe_key = ?",
        (f"{session_id}:{request_id}",),
    ).fetchone()
    assert row is not None
    assert row["output_tokens"] == 3772
    input_price, output_price = PRICES_PER_TOKEN_USD["claude-sonnet-5"]
    assert row["accounted_cost_usd"] == pytest.approx(100 * input_price + 3772 * output_price)


def test_import_transcripts_accepts_single_string_pattern_backward_compat(tmp_path, db_file):
    # The pre-Task-6 API (single glob string) must keep working, since
    # both the CLI --transcripts-glob override and any external caller
    # may still pass a plain string.
    sub = tmp_path / "projC" / "session-3" / "subagents" / "agent-c1.jsonl"
    _write_jsonl(sub, [
        _assistant_line(session_id="session-3", request_id="req-sub-3", is_sidechain=True),
    ])
    single_pattern = str(tmp_path / "*" / "*" / "subagents" / "*.jsonl")
    rows_imported, sessions_seen, _ = import_transcripts(single_pattern, db_file)
    assert rows_imported == 1
    assert sessions_seen == {"session-3"}


# ---------------------------------------------------------------------
# F6-6: the price table is DATA (tools/model_prices.json); an unknown
# price is ONE summary line per model plus a "partial" mark on the
# total; an unreadable price file stops the tool (exit 2).
# ---------------------------------------------------------------------

# The table of the code literal that F6-6 removed, written out as the
# expected value (the control that nothing was lost in the move).
OLD_LITERAL_TABLE = {
    "claude-fable-5": (10.00 / 1_000_000, 50.00 / 1_000_000),
    "claude-opus-4-8": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-opus-5": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-sonnet-5": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-sonnet-4-6": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-haiku-4-5-20251001": (1.00 / 1_000_000, 5.00 / 1_000_000),
    "claude-haiku-4-5": (1.00 / 1_000_000, 5.00 / 1_000_000),
}
CLAUDE_5_X_ROWS = ["claude-fable-5-1", "claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]


def _prices_file(tmp_path, model_rows, **top):
    data = {
        "as_of": "2026-10-16", "unit": "usd_per_token",
        "cache_write_multiplier": 1.25, "cache_write_1h_multiplier": 2, "cache_read_multiplier": 0.1,
        "models": model_rows,
    }
    data.update(top)
    data = {k: v for k, v in data.items() if v is not ...}  # `...` drops a key
    path = tmp_path / "prices.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _run(tmp_path, capsys, prices, lines=None, glob_arg=None, extra=()):
    """Runs main() over a one-file transcript (or `glob_arg`) with --all."""
    if glob_arg is None:
        transcript = tmp_path / "proj" / "s1.jsonl"
        _write_jsonl(transcript, lines or [])
        glob_arg = str(transcript)
    argv = ["--transcripts-glob", glob_arg, "--db", str(tmp_path / "t.db"), "--all"]
    if prices is not None:
        argv += ["--prices", str(prices)]
    code = main(argv + list(extra))
    out = capsys.readouterr()
    return code, out.out, out.err


def test_known_model_cost_pinned_to_the_value_before_the_move():
    # Expected literals were computed by the code that held the price
    # table as literals, BEFORE F6-6 (opus-4-8 / sonnet-4-6 are Claude 4).
    assert accounted_cost("claude-opus-4-8", 1000, 500, 200, 3000) == (0.020250000000000004, None)
    assert accounted_cost("claude-sonnet-4-6", 123456, 7890, 54321, 987654) == (0.9887179500000001, None)


def test_every_model_of_the_old_literal_table_is_in_the_file_with_the_same_numbers():
    # F6-24 re-pin: the file also holds the four Claude 5.x rows now, so the old table is a SUBSET of it
    # (the (input, output) pairs of the old models are the control that nothing was lost); the file-level
    # multipliers and the old models' own multipliers are the file's.
    assert {m: PRICES_PER_TOKEN_USD[m] for m in OLD_LITERAL_TABLE} == OLD_LITERAL_TABLE
    assert (CACHE_WRITE_MULTIPLIER, CACHE_READ_MULTIPLIER) == (1.25, 0.1)
    assert _TABLE["cache_write_1h_multiplier"] == 2
    for model_id in OLD_LITERAL_TABLE:
        record = _TABLE["models"][model_id]
        assert (record.cache_write_multiplier, record.cache_write_1h_multiplier, record.cache_read_multiplier) == (1.25, 2, 0.1)


# F6-24: the page https://platform.claude.com/docs/en/about-claude/pricing of 16.10.2026, USD per token, and the
# cache-read multiplier of each Claude 5.x row (footnotes 1 and 2 of the page; Haiku 5.5 keeps the file's 0.1).
CLAUDE_5_X_PAGE = {
    "claude-fable-5-1": (1e-05, 5e-05, 0.025),
    "claude-opus-5-5": (4e-06, 2e-05, 0.05),
    "claude-sonnet-5-5": (2e-06, 1e-05, 0.05),
    "claude-haiku-5-5": (1e-07, 5e-07, 0.1),
}
# one control token profile for the four hand-computed values below
CONTROL = dict(input_tokens=1000, output_tokens=500, cache_creation_tokens=0, cache_read_tokens=10000)


def test_claude_5_x_rows_are_priced_from_the_page_and_carry_the_source():
    raw = json.loads((Path(usage_report.__file__).parent / "model_prices.json").read_text(encoding="utf-8"))
    assert raw["as_of"] == "2026-10-16"
    assert raw["source"] == "https://platform.claude.com/docs/en/about-claude/pricing"
    assert set(CLAUDE_5_X_ROWS) == set(CLAUDE_5_X_PAGE)
    for model_id, (price_in, price_out, read_multiplier) in CLAUDE_5_X_PAGE.items():
        record = _TABLE["models"][model_id]  # priced: present in the loader's table
        assert (record.input, record.output, record.cache_read_multiplier) == (price_in, price_out, read_multiplier)
        assert (record.cache_write_multiplier, record.cache_write_1h_multiplier) == (1.25, 2)
        assert "to be filled" not in raw["models"][model_id].get("note", "")
    assert "100,000 tokens" in raw["models"]["claude-haiku-5-5"]["note"]  # the second Haiku tariff is a note, no code
    assert "cache_read_multiplier" not in raw["models"]["claude-haiku-5-5"]  # Haiku keeps the file's 0.1


@pytest.mark.parametrize("model_id, hand_computed", [
    # 1000 in + 500 out + 10000 cache-read, arithmetic by hand from the page's $/MTok:
    # fable 5.1:  1000*1e-05 + 500*5e-05 + 10000*1e-05*0.025 = 0.01 + 0.025 + 0.0025
    ("claude-fable-5-1", 0.0375),
    # opus 5.5:   1000*4e-06 + 500*2e-05 + 10000*4e-06*0.05  = 0.004 + 0.01 + 0.002
    ("claude-opus-5-5", 0.016),
    # sonnet 5.5: 1000*2e-06 + 500*1e-05 + 10000*2e-06*0.05  = 0.002 + 0.005 + 0.001
    ("claude-sonnet-5-5", 0.008),
    # haiku 5.5:  1000*1e-07 + 500*5e-07 + 10000*1e-07*0.1   = 0.0001 + 0.00025 + 0.0001
    ("claude-haiku-5-5", 0.00045),
], ids=str)
def test_claude_5_x_control_value_by_hand_from_the_page(model_id, hand_computed):
    cost, warning = accounted_cost(model_id, **CONTROL)
    assert warning is None
    assert cost == pytest.approx(hand_computed, rel=1e-9)


def test_negative_control_the_old_read_multiplier_would_cost_more():
    # the same tokens on claude-fable-5 (cache reads at the file's 0.1x): 0.01 + 0.025 + 10000*1e-05*0.1 = 0.045,
    # MORE than fable 5.1's 0.0375 - the per-model 0.025 is what the 5.1 control kills
    assert accounted_cost("claude-fable-5", **CONTROL)[0] == pytest.approx(0.045, rel=1e-9)
    assert accounted_cost("claude-fable-5", **CONTROL)[0] > accounted_cost("claude-fable-5-1", **CONTROL)[0]


def test_cache_writes_split_by_the_ttl_by_hand():
    # fable 5.1, 2000 cache-write tokens: 1000 of them 1-hour. 1000*1e-05*1.25 + 1000*1e-05*2 = 0.0125 + 0.02
    cost, _ = accounted_cost("claude-fable-5-1", 0, 0, 2000, 0, None, 1000)
    assert cost == pytest.approx(0.0325, rel=1e-9)
    # no split known (None): the whole write is a 5-minute write, 2000*1e-05*1.25
    assert accounted_cost("claude-fable-5-1", 0, 0, 2000, 0)[0] == pytest.approx(0.025, rel=1e-9)
    # all 1-hour: 2000*1e-05*2; a split of 0 is a KNOWN split (all 5-minute)
    assert accounted_cost("claude-fable-5-1", 0, 0, 2000, 0, None, 2000)[0] == pytest.approx(0.04, rel=1e-9)
    assert accounted_cost("claude-fable-5-1", 0, 0, 2000, 0, None, 0)[0] == pytest.approx(0.025, rel=1e-9)


@pytest.mark.parametrize("split, expected", [(-5, 0.025), (2001, 0.04)], ids=["negative", "beyond-the-write"])
def test_a_split_outside_the_write_is_clamped_into_it(split, expected):
    assert accounted_cost("claude-fable-5-1", 0, 0, 2000, 0, None, split)[0] == pytest.approx(expected, rel=1e-9)


def test_unpriced_turns_of_the_four_claude_5_x_models_are_zero_after_the_fill(tmp_path, db_file):
    lines = [_assistant_line(session_id="s1", request_id=f"r{i}", model=m, uuid=f"u{i}")
             for i, m in enumerate(CLAUDE_5_X_ROWS)]
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, lines)
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    assert usage_report.unpriced_turns(conn) == {}  # no row of the four is left with a NULL cost
    assert conn.execute("SELECT COUNT(*) FROM cc_usage WHERE accounted_cost_usd IS NOT NULL").fetchone()[0] == 4


def test_null_price_model_gives_one_summary_line_and_the_partial_mark(tmp_path, capsys):
    prices = _prices_file(tmp_path, {
        "claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05},
        "claude-sonnet-5-5": {"input": None, "output": None, "note": "to fill in"},
    })
    lines = [
        _assistant_line(session_id="s1", request_id=f"r{i}", model="claude-sonnet-5-5", uuid=f"u{i}")
        for i in range(3)
    ] + [_assistant_line(session_id="s1", request_id="rk", model="claude-sonnet-5", uuid="uk")]
    code, out, err = _run(tmp_path, capsys, prices, lines)
    assert code == 0
    assert out.count("unknown price: claude-sonnet-5-5: 3 turn(s)") == 1
    assert out.count("unknown price:") == 1
    assert "(partial: 3 turn(s) without a price)" in out
    assert "WARNING" not in out and "WARNING" not in err


def test_model_absent_from_the_file_gives_the_same_line_and_mark(tmp_path, capsys):
    prices = _prices_file(tmp_path, {"claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05}})
    lines = [_assistant_line(session_id="s1", request_id=f"r{i}", model="never-heard-of-it", uuid=f"u{i}")
             for i in range(2)]
    code, out, err = _run(tmp_path, capsys, prices, lines)
    assert code == 0
    assert out.count("unknown price: never-heard-of-it: 2 turn(s)") == 1
    assert "(partial: 2 turn(s) without a price)" in out
    assert "WARNING" not in out and "WARNING" not in err


def test_input_set_with_output_null_is_unknown(tmp_path, capsys):
    prices = _prices_file(tmp_path, {"half-priced": {"input": 3e-06, "output": None}})
    assert accounted_cost("half-priced", 1000, 1000, 0, 0, load_prices(prices)) == (None, None)
    lines = [_assistant_line(session_id="s1", model="half-priced")]
    _, out, _ = _run(tmp_path, capsys, prices, lines)
    assert "unknown price: half-priced: 1 turn(s)" in out
    assert "(partial: 1 turn(s) without a price)" in out


def test_all_priced_window_has_no_unknown_line_and_no_partial_mark(tmp_path, capsys):
    lines = [_assistant_line(session_id="s1", model="claude-opus-4-8")]
    code, out, _ = _run(tmp_path, capsys, None, lines)
    assert code == 0
    assert "unknown price" not in out and "partial" not in out


def test_zero_turns_in_the_window_has_no_unknown_line_and_no_partial_mark(tmp_path, capsys):
    code, out, _ = _run(tmp_path, capsys, None, glob_arg=str(tmp_path / "nothing-*.jsonl"))
    assert code == 0
    assert "0 turns" in out
    assert "unknown price" not in out and "partial" not in out


def test_known_model_total_is_unchanged_to_the_cent(tmp_path, capsys):
    # one opus-4-8 turn: 10 in + 5 out tokens -> 10*5e-6 + 5*2.5e-5
    lines = [_assistant_line(session_id="s1", model="claude-opus-4-8")]
    _, out, _ = _run(tmp_path, capsys, None, lines)
    assert f"${10 * 5e-06 + 5 * 2.5e-05:.4f} accounted" in out


def test_prices_given_twice_the_last_wins(tmp_path, capsys):
    good = _prices_file(tmp_path, {"claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05}})
    lines = [_assistant_line(session_id="s1", model="claude-sonnet-5")]
    code, out, _ = _run(tmp_path, capsys, tmp_path / "no-such-first.json", lines, extra=["--prices", str(good)])
    assert code == 0
    assert "unknown price" not in out


def test_extra_top_level_keys_and_a_model_note_are_ignored(tmp_path):
    prices = _prices_file(
        tmp_path, {"m": {"input": 1e-06, "output": 2e-06, "note": "x"}},
        owner="someone", comment="free text",
    )
    # F6-24 re-pin: a model is a ModelPrice record (the file's multipliers resolved in), not an (input, output) pair
    assert load_prices(prices)["models"] == {"m": (1e-06, 2e-06, 1.25, 2, 0.1)}


@pytest.mark.parametrize("key", ["cache_raed_multiplier", "cache_write_1h_multiplier", "extra"],
                         ids=["typo", "per-row-1h-not-supported", "free-key"])
def test_an_unknown_key_on_a_model_row_is_refused_naming_the_model_and_the_key(tmp_path, key):
    # F-4: a typo'd multiplier must not price silently at the file default (FR-41). Allowed on a row:
    # input, output, note, cache_read_multiplier, cache_write_multiplier.
    path = _prices_file(tmp_path, {"claude-x-1": {"input": 1e-06, "output": 2e-06, key: 0.05}})
    with pytest.raises(PricesError) as caught:
        load_prices(path)
    message = str(caught.value)
    assert "claude-x-1" in message and f"unknown key '{key}'" in message and str(path) in message
    assert "cache_read_multiplier" in message and "note" in message  # the allowed keys are named


def test_every_allowed_key_loads_and_the_unknown_key_beats_a_null_price(tmp_path):
    ok = {"m": {"input": 1e-06, "output": 2e-06, "note": "n", "cache_read_multiplier": 0.05, "cache_write_multiplier": 1.5}}
    assert load_prices(_prices_file(tmp_path, ok))["models"]["m"] == (1e-06, 2e-06, 1.5, 2, 0.05)  # control: the five keys pass
    both = {"m": {"input": None, "output": None, "cache_raed_multiplier": 0.05}}  # a null price AND a typo: the typo first
    with pytest.raises(PricesError, match="unknown key 'cache_raed_multiplier'"):
        load_prices(_prices_file(tmp_path, both))


def test_the_real_price_file_has_only_allowed_keys():
    assert load_prices()["models"]  # loads: no row of tools/model_prices.json carries an unknown key


# --- F6-24: per-model cache multipliers ---

def _cost_of(tmp_path, rows, model, **tokens):
    profile = dict(input_tokens=0, output_tokens=0, cache_creation_tokens=0, cache_read_tokens=0)
    profile.update(tokens)
    return accounted_cost(model, prices=load_prices(_prices_file(tmp_path, rows)), **profile)[0]


def test_a_model_multiplier_beats_the_files_and_a_row_without_one_takes_the_files(tmp_path):
    rows = {
        "own": {"input": 1e-06, "output": 2e-06, "cache_read_multiplier": 0.5, "cache_write_multiplier": 3},
        "plain": {"input": 1e-06, "output": 2e-06},
        "read-only": {"input": 1e-06, "output": 2e-06, "cache_read_multiplier": 0.5},
    }
    table = load_prices(_prices_file(tmp_path, rows))
    assert table["models"]["own"] == (1e-06, 2e-06, 3, 2, 0.5)
    assert table["models"]["plain"] == (1e-06, 2e-06, 1.25, 2, 0.1)
    assert table["models"]["read-only"] == (1e-06, 2e-06, 1.25, 2, 0.5)  # an override of ONE key leaves the other the file's
    tokens = dict(input_tokens=100, cache_creation_tokens=1000, cache_read_tokens=1000)
    # own:   100*1e-06 + 1000*1e-06*3    + 1000*1e-06*0.5 = 0.0001 + 0.003   + 0.0005 = 0.0036
    # plain: 100*1e-06 + 1000*1e-06*1.25 + 1000*1e-06*0.1 = 0.0001 + 0.00125 + 0.0001 = 0.00145
    assert _cost_of(tmp_path, rows, "own", **tokens) == pytest.approx(0.0036, rel=1e-9)
    assert _cost_of(tmp_path, rows, "plain", **tokens) == pytest.approx(0.00145, rel=1e-9)


def test_a_zero_model_multiplier_is_legal_free_cache_reads(tmp_path):
    rows = {"free": {"input": 1e-06, "output": 2e-06, "cache_read_multiplier": 0}}
    # 100 in + 1000000 cache-read tokens: only the 100 input tokens cost, 100*1e-06 = 0.0001
    assert _cost_of(tmp_path, rows, "free", input_tokens=100, cache_read_tokens=1_000_000) == pytest.approx(0.0001, rel=1e-9)


def test_a_null_price_row_with_a_multiplier_is_still_unpriced_without_an_error(tmp_path):
    rows = {"half": {"input": None, "output": None, "cache_read_multiplier": 0.05, "note": "to fill in"}}
    table = load_prices(_prices_file(tmp_path, rows))
    assert "half" not in table["models"]
    assert accounted_cost("half", 1000, 1000, 0, 0, table) == (None, None)


@pytest.mark.parametrize("key", ["cache_read_multiplier", "cache_write_multiplier"])
@pytest.mark.parametrize("bad", ["0.05", -0.5, None, True, [0.1]], ids=["string", "negative", "null", "bool", "list"])
def test_a_malformed_model_multiplier_names_the_model_and_the_key(tmp_path, key, bad):
    path = _prices_file(tmp_path, {"claude-x-1": {"input": 1e-06, "output": 2e-06, key: bad}})
    with pytest.raises(PricesError) as caught:
        load_prices(path)
    assert "claude-x-1" in str(caught.value) and f"'{key}'" in str(caught.value) and str(path) in str(caught.value)


def test_a_malformed_model_multiplier_stops_the_tool_with_exit_2(tmp_path, capsys):
    path = _prices_file(tmp_path, {"claude-x-1": {"input": 1e-06, "output": 2e-06, "cache_read_multiplier": -1}})
    code, out, err = _run(tmp_path, capsys, path, [_assistant_line(session_id="s1")])
    assert code == 2 and out == ""
    assert len(err.strip().splitlines()) == 1 and "claude-x-1" in err and "cache_read_multiplier" in err


def test_a_malformed_multiplier_on_a_null_price_row_is_refused_too(tmp_path):
    path = _prices_file(tmp_path, {"half": {"input": None, "output": None, "cache_read_multiplier": "x"}})
    with pytest.raises(PricesError, match="half"):
        load_prices(path)


# --- F6-24: the 5-minute / 1-hour cache-write split of the transcript usage, stored and priced ---

def _split_line(request_id, write_5m, write_1h, model="claude-fable-5-1"):
    line = _assistant_line(session_id="s1", request_id=request_id, uuid=request_id, model=model)
    line["message"]["usage"].update({
        "cache_creation_input_tokens": write_5m + write_1h,
        "cache_creation": {"ephemeral_5m_input_tokens": write_5m, "ephemeral_1h_input_tokens": write_1h},
    })
    return line


def test_the_split_is_read_from_the_transcript_and_unknown_when_absent_or_broken(tmp_path):
    no_dict = _assistant_line(session_id="s1", request_id="a", uuid="a")
    no_dict["message"]["usage"]["cache_creation"] = "junk"
    no_key = _assistant_line(session_id="s1", request_id="b", uuid="b")
    no_key["message"]["usage"]["cache_creation"] = {"ephemeral_5m_input_tokens": 5}
    negative = _split_line("c", 0, 0)
    negative["message"]["usage"]["cache_creation"]["ephemeral_1h_input_tokens"] = -3
    as_bool = _split_line("d", 0, 0)
    as_bool["message"]["usage"]["cache_creation"]["ephemeral_1h_input_tokens"] = True
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, [_split_line("e", 100, 300), _split_line("f", 40, 0),
                              _assistant_line(session_id="s1", request_id="g", uuid="g"), no_dict, no_key, negative, as_bool])
    got = [t["cache_creation_1h_tokens"] for t in iter_assistant_turns(str(transcript))]
    assert got == [300, 0, None, None, None, None, None]  # 0 is a KNOWN split, None is unknown


def test_import_stores_the_split_and_prices_the_writes_by_it(tmp_path, db_file):
    transcript = tmp_path / "proj" / "s1.jsonl"
    # 1000 5m + 1000 1h on fable 5.1 (no input/output): 1000*1e-05*1.25 + 1000*1e-05*2 = 0.0125 + 0.02
    _write_jsonl(transcript, [_split_line("r1", 1000, 1000), _assistant_line(session_id="s1", request_id="r2", uuid="r2")])
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    rows = dict(conn.execute("SELECT dedupe_key, cache_creation_1h_tokens FROM cc_usage"))
    assert rows == {"s1:r1": 1000, "s1:r2": None}
    cost = conn.execute("SELECT accounted_cost_usd FROM cc_usage WHERE dedupe_key = 's1:r1'").fetchone()[0]
    # + the line's own 10 in + 5 out tokens: 10*1e-05 + 5*5e-05 = 0.00035
    assert cost == pytest.approx(0.0325 + 0.00035, rel=1e-9)


def _old_schema_db(db_file, with_old_row=False):
    """A database built with the OLD schema (no cache_creation_1h_tokens column), optionally holding the row of
    s1:r1 as the old importer stored it: priced as all-5-minute writes, no split."""
    conn = sqlite3.connect(db_file)
    conn.execute(SCHEMA.replace("    cache_creation_1h_tokens INTEGER,\n", ""))
    if with_old_row:
        conn.execute(
            "INSERT INTO cc_usage (ts, project, session_id, turn_index, model, input_tokens, output_tokens,"
            " cache_creation_tokens, cache_read_tokens, accounted_cost_usd, dedupe_key)"
            " VALUES ('2026-07-07T12:00:00Z', 'proj', 's1', 0, 'claude-fable-5-1', 10, 5, 2000, 0, 0.02535, 's1:r1')")
    conn.commit()
    conn.close()


def _columns(db_file):
    conn = sqlite3.connect(db_file)
    try:
        return {row[1] for row in conn.execute("PRAGMA table_info(cc_usage)")}
    finally:
        conn.close()


def test_an_import_adds_the_split_column_to_an_old_db_and_reprices_the_old_row_idempotently(tmp_path, db_file):
    # F-1 / E4: the old-schema database gets the column from _connect's one ALTER loop; the re-import fills the old
    # row by request id and prices it by its split; a second import changes nothing.
    _old_schema_db(db_file, with_old_row=True)
    assert "cache_creation_1h_tokens" not in _columns(db_file)                    # control: the old schema really lacks it
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, [_split_line("r1", 1000, 1000)])
    imported, _, warnings = import_transcripts(str(transcript), db_file)
    assert imported == 0 and warnings == []                                      # the row existed; no warning about the schema
    assert "cache_creation_1h_tokens" in _columns(db_file)                        # added by the import
    conn = sqlite3.connect(db_file)
    first = conn.execute("SELECT cache_creation_1h_tokens, accounted_cost_usd FROM cc_usage").fetchall()
    # 10 in + 5 out + 1000 5m + 1000 1h on fable 5.1: 10*1e-05 + 5*5e-05 + 1000*1e-05*1.25 + 1000*1e-05*2 = 0.00035 + 0.0325
    assert len(first) == 1 and first[0][0] == 1000 and first[0][1] == pytest.approx(0.03285, rel=1e-9)
    conn.close()
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    assert conn.execute("SELECT cache_creation_1h_tokens, accounted_cost_usd FROM cc_usage").fetchall() == first  # idempotent
    conn.close()


def test_a_db_with_the_column_already_is_left_as_it_is_by_the_import(tmp_path, db_file):
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, [_split_line("r1", 1000, 1000)])
    import_transcripts(str(transcript), db_file)
    before = _columns(db_file)
    import_transcripts(str(transcript), db_file)                                  # the column exists: nothing to add, no error
    assert _columns(db_file) == before and "cache_creation_1h_tokens" in before


def test_a_row_whose_transcript_is_gone_keeps_a_null_split_and_the_report_counts_it_as_an_estimate(tmp_path, db_file):
    _old_schema_db(db_file, with_old_row=True)
    transcript = tmp_path / "proj" / "other.jsonl"
    _write_jsonl(transcript, [_assistant_line(session_id="s2", request_id="x", uuid="x")])  # not the old row's transcript
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    assert conn.execute("SELECT cache_creation_1h_tokens FROM cc_usage WHERE dedupe_key = 's1:r1'").fetchone() == (None,)
    conn.close()
    assert build_report(db_file, None)["cache_write_estimate"]["turns"] == 1     # priced as 5-minute writes: said out loud


def test_the_report_of_a_db_never_imported_since_the_column_exists_says_it_is_an_estimate(tmp_path, db_file):
    _old_schema_db(db_file, with_old_row=True)                                    # no import: read as it is
    assert build_report(db_file, None)["cache_write_estimate"]["turns"] == 1


def test_a_duplicate_line_without_a_split_keeps_the_stored_split_and_prices_by_it(tmp_path, db_file):
    # F-5: the second line of the SAME request carries a higher output and NO cache_creation object; MAX-wins must
    # not reprice the stored row as all-5-minute writes while the stored split stays
    with_split = _split_line("r1", 0, 1000)
    no_split = _assistant_line(session_id="s1", request_id="r1", uuid="r1b", model="claude-fable-5-1")
    no_split["message"]["usage"]["cache_creation_input_tokens"] = 1000
    no_split["message"]["usage"]["output_tokens"] = 100
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, [with_split, no_split])
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    output, split, cost = conn.execute(
        "SELECT output_tokens, cache_creation_1h_tokens, accounted_cost_usd FROM cc_usage").fetchone()
    # the higher output wins (100); the split 1000 stays; cost = 10*1e-05 + 100*5e-05 + 1000*1e-05*2 = 0.0001 + 0.005 + 0.02
    assert (output, split) == (100, 1000) and cost == pytest.approx(0.0251, rel=1e-9)
    assert build_report(db_file, None)["cache_write_estimate"]["turns"] == 0      # the row is not an estimate


def test_a_row_stored_without_a_split_gets_it_and_the_cost_from_its_own_tokens_on_reimport(tmp_path, db_file):
    transcript = tmp_path / "proj" / "s1.jsonl"
    # the placeholder line (output 1) of a split subagent turn comes AFTER the real one (output 50): the repricing
    # must use the STORED output (50), never the placeholder line's
    real, placeholder = _split_line("r1", 0, 2000), _split_line("r1", 0, 2000)
    real["message"]["usage"]["output_tokens"] = 50
    placeholder["message"]["usage"]["output_tokens"] = 1
    _write_jsonl(transcript, [real, placeholder])
    conn = sqlite3.connect(db_file)
    conn.execute(SCHEMA)
    conn.execute(
        "INSERT INTO cc_usage (ts, project, session_id, turn_index, model, input_tokens, output_tokens,"
        " cache_creation_tokens, cache_read_tokens, accounted_cost_usd, dedupe_key)"
        " VALUES ('2026-07-07T12:00:00Z', 'proj', 's1', 0, 'claude-fable-5-1', 10, 50, 2000, 0, 123.0, 's1:r1')")
    conn.commit()
    conn.close()
    import_transcripts(str(transcript), db_file)
    conn = sqlite3.connect(db_file)
    split, cost = conn.execute("SELECT cache_creation_1h_tokens, accounted_cost_usd FROM cc_usage").fetchone()
    assert split == 2000
    # 10*1e-05 + 50*5e-05 + 2000*1e-05*2 = 0.0001 + 0.0025 + 0.04
    assert cost == pytest.approx(0.0426, rel=1e-9)


def test_the_estimate_line_is_printed_only_for_turns_without_a_split(tmp_path, capsys):
    plain = _assistant_line(session_id="s1", request_id="p", uuid="p", model="claude-sonnet-5")
    plain["message"]["usage"]["cache_creation_input_tokens"] = 500
    code, out, _ = _run(tmp_path, capsys, None, [plain, _split_line("q", 0, 500)])
    assert code == 0
    assert out.count("estimate: cache writes priced as 5-minute writes for 1 turn(s)") == 1
    (tmp_path / "second").mkdir()
    code, out, _ = _run(tmp_path / "second", capsys, None, [_split_line("q", 0, 500)])
    assert "estimate:" not in out


@pytest.mark.parametrize("break_it", [
    "missing-file", "malformed-json", "empty-file", "not-an-object", "no-models-key", "models-not-object",
    "price-is-string", "price-is-bool", "price-is-negative", "price-is-nan", "model-not-object",
    "price-key-absent", "write-multiplier-absent", "write-1h-multiplier-absent", "read-multiplier-absent",
    "multiplier-is-string",
    "path-is-a-directory",
], ids=str)
def test_unreadable_price_file_stops_with_exit_2_and_one_stderr_line(tmp_path, capsys, break_it):
    good = {"claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05}}
    path = tmp_path / "prices.json"
    if break_it == "missing-file":
        path = tmp_path / "nope.json"
    elif break_it == "malformed-json":
        path.write_text('{"models": {', encoding="utf-8")
    elif break_it == "empty-file":
        path.write_text("", encoding="utf-8")
    elif break_it == "not-an-object":
        path.write_text("[1, 2]", encoding="utf-8")
    elif break_it == "path-is-a-directory":
        path = tmp_path
    else:
        top = {}
        models = good
        if break_it == "no-models-key":
            top["models"] = ...
        elif break_it == "models-not-object":
            top["models"] = ["a"]
        elif break_it == "price-is-string":
            models = {"claude-sonnet-5": {"input": "3e-06", "output": 1.5e-05}}
        elif break_it == "price-is-bool":
            models = {"claude-sonnet-5": {"input": True, "output": 1.5e-05}}
        elif break_it == "price-is-negative":
            models = {"claude-sonnet-5": {"input": -1.0, "output": 1.5e-05}}
        elif break_it == "model-not-object":
            models = {"claude-sonnet-5": [3e-06, 1.5e-05]}
        elif break_it == "price-key-absent":
            models = {"claude-sonnet-5": {"input": 3e-06}}
        elif break_it == "write-multiplier-absent":
            top["cache_write_multiplier"] = ...
        elif break_it == "write-1h-multiplier-absent":
            top["cache_write_1h_multiplier"] = ...
        elif break_it == "read-multiplier-absent":
            top["cache_read_multiplier"] = ...
        elif break_it == "multiplier-is-string":
            top["cache_read_multiplier"] = "0.1"
        if break_it == "price-is-nan":
            path.write_text(
                '{"cache_write_multiplier": 1.25, "cache_write_1h_multiplier": 2, "cache_read_multiplier": 0.1,'
                ' "models": {"m": {"input": NaN, "output": 1.0}}}', encoding="utf-8")
        else:
            path = _prices_file(tmp_path, models, **top)
    code, out, err = _run(tmp_path, capsys, path, [_assistant_line(session_id="s1")])
    assert code == 2
    assert out == ""  # nothing reported as if the prices were fine
    assert len(err.strip().splitlines()) == 1
    assert str(path) in err
    assert not (tmp_path / "t.db").exists()  # stopped before any import


def test_corrupted_copy_of_the_real_file_is_refused(tmp_path, capsys):
    """NEGATIVE control: the real file passes; a copy with one price
    turned into a string is refused with exit 2 naming the model."""
    real = Path(usage_report.__file__).parent / "model_prices.json"
    assert load_prices(real)["models"]  # the real file is accepted
    data = json.loads(real.read_text(encoding="utf-8"))
    data["models"]["claude-opus-4-8"]["input"] = "5e-06"
    copy = tmp_path / "corrupted.json"
    copy.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(PricesError, match="claude-opus-4-8"):
        load_prices(copy)
    code, _, err = _run(tmp_path, capsys, copy, [_assistant_line(session_id="s1")])
    assert code == 2
    assert "claude-opus-4-8" in err and str(copy) in err


def test_transcript_turns_without_a_model_field_get_one_summary_line(tmp_path, capsys):
    """A turn with no model cannot be stored (cc_usage.model is NOT
    NULL; the import is INSERT OR IGNORE) -- it is not priced and not in
    the totals, but it is NOT silent (FR-41): ONE line, counted by
    request (two lines of one request count once)."""
    def modelless(request_id):
        line = _assistant_line(session_id="s1", request_id=request_id, uuid=request_id)
        del line["message"]["model"]
        return line
    lines = [modelless("a"), modelless("a"), modelless("b"),
             _assistant_line(session_id="s1", request_id="c", model="claude-opus-4-8", uuid="c")]
    assert accounted_cost(None, 10, 5, 0, 0) == (None, None)
    code, out, _ = _run(tmp_path, capsys, None, lines)
    assert code == 0
    assert out.count("turns without a model field: 2") == 1
    assert out.count("turns without a model field") == 1
    assert "1 turns," in out  # only the priced turn is in the totals
    assert "unknown price" not in out


def test_no_model_less_turns_means_no_model_field_line(tmp_path, capsys):
    _, out, _ = _run(tmp_path, capsys, None, [_assistant_line(session_id="s1", model="claude-opus-4-8")])
    assert "without a model field" not in out


def test_default_price_file_is_the_one_next_to_the_module():
    assert usage_report.PRICES_FILE == Path(usage_report.__file__).parent / "model_prices.json"
    assert load_prices() == load_prices(usage_report.PRICES_FILE)


# --- F6-21: the unpriced-turn counting is ONE function, shared with savings_report ---

def test_unpriced_turns_counts_null_cost_turns_per_model_under_the_condition():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE cc_usage (ts TEXT, model TEXT, accounted_cost_usd REAL)")
    conn.executemany("INSERT INTO cc_usage VALUES (?,?,?)", [
        ("2026-10-09", "m-null", None), ("2026-10-09", "m-null", None), ("2026-10-10", "a-null", None),
        ("2026-10-09", "m-priced", 0.5), ("2026-10-20", "m-null", None)])
    assert usage_report.unpriced_turns(conn) == {"a-null": 1, "m-null": 3}  # sorted by model
    assert usage_report.unpriced_turns(conn, "ts < ?", ("2026-10-10",)) == {"m-null": 2}
    assert usage_report.unpriced_turns(conn, "ts < ?", ("2026-01-01",)) == {}  # nothing in the window
    assert usage_report.unpriced_turns(conn, "ts < ? or ts > ?", ("2026-10-10", "2026-10-15")) == {"m-null": 3}  # OR stays inside its parentheses


# --- F6-15: the join of a request's lines is transcripts.request_usages (one reader) ---

SAMPLE_STDOUT = """CLAUDE CODE USAGE REPORT (all time)

Totals:
  5 turns, 13800+1750 tok (+8500 cache-write, +25000 cache-read), $0.3010 accounted (partial: 1 turn(s) without a price)
  unknown price: claude-unknown-model-x: 1 turn(s)
  estimate: cache writes priced as 5-minute writes for 2 turn(s) with no 1-hour/5-minute split in the usage data (a 1-hour write costs more)

Per day:
  2026-07-01: 5 turns, 13800+1750 tok, $0.3010

Per model:
  claude-fable-5: 1 turns, 10000+1000 tok (+8000 cache-write, +20000 cache-read), $0.2700
  claude-opus-4-8: 1 turns, 2000+400 tok (+0 cache-write, +0 cache-read), $0.0200
  claude-sonnet-5: 2 turns, 1300+250 tok (+500 cache-write, +5000 cache-read), $0.0110
  claude-unknown-model-x: 1 turns, 500+100 tok (+0 cache-write, +0 cache-read), $0.0000

Per project:
  fixtures: 5 turns, 13800+1750 tok, $0.3010

Top 5 sessions by accounted cost:
  fixtures / session-bbb: 3 turns, $0.2900
  fixtures / session-aaa: 2 turns, $0.0110

Cache economics:
  cache_read share of input: 52.9%
  accounted savings vs. uncached: $0.1935

Sidechain (subagent) traffic:
  2400 tok, $0.0200 accounted
  share of total tokens: 4.9%

(this run: 5 new row(s) imported from 2 session file(s) matching <FIXTURE>)
"""


def test_f6_15_the_whole_stdout_on_the_sample_transcript_is_pinned(tmp_path, capsys):
    """The stdout of the CLI over tools/fixtures/sample_transcript.jsonl, captured from the code BEFORE the join
    moved onto transcripts.request_usages, byte for byte (the price file is a fixed one: a price change moves
    nothing here)."""
    prices = _prices_file(tmp_path, {"claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05},
                                     "claude-opus-4-8": {"input": 5e-06, "output": 2.5e-05},
                                     "claude-fable-5": {"input": 1e-05, "output": 5e-05}})
    code, out, err = _run(tmp_path, capsys, prices, glob_arg=FIXTURE)
    assert code == 0 and err == ""
    assert out.replace(FIXTURE, "<FIXTURE>") == SAMPLE_STDOUT


# --- F6-23: a request whose lines carry DIFFERENT models is priced per model; a single-model request is unchanged ---

def _request_lines(request_id, model, usages, session_id="s1", first=0):
    """One assistant line per usage dict, all of ONE request (the harness writes a line per content block)."""
    lines = []
    for i, usage in enumerate(usages):
        line = _assistant_line(session_id=session_id, request_id=request_id, model=model, uuid=f"{request_id}-{first + i}")
        line["message"]["usage"] = usage
        lines.append(line)
    return lines


_FB_FIRST = {"input_tokens": 2, "cache_creation_input_tokens": 625, "cache_read_input_tokens": 102517, "output_tokens": 3,
             "cache_creation": {"ephemeral_5m_input_tokens": 625, "ephemeral_1h_input_tokens": 0}}
_FB_LAST = {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 98101, "output_tokens": 390,
            "cache_creation": {"ephemeral_1h_input_tokens": 0, "ephemeral_5m_input_tokens": 625}}
# Copied from the real subagent transcript cb6de03f-9956-460e-ba12-af9136534048/subagents/agent-a877f9d0d06e97281.jsonl,
# lines 108-112 (27.08.2026), model + usage only: the request req_011CeTQmWnYoVsGZrpJVsvGh, a fallback fable-5 -> opus-4-8.
# Line 112 is the fallback's own usage; lines 109-111 are labelled opus-4-8 but repeat the usage of line 108.
# _FALLBACK_27_08 is the request WITHOUT the iterations (the MAX reader's fixture); _FALLBACK_27_08_REAL has them, as the
# real line 112 does: usage.iterations = the provider's own record of the two messages.
_FB_ITERATIONS = [
    {"input_tokens": 2, "output_tokens": 869, "cache_read_input_tokens": 102517, "cache_creation_input_tokens": 625,
     "cache_creation": {"ephemeral_5m_input_tokens": 625, "ephemeral_1h_input_tokens": 0}, "type": "message", "model": "claude-fable-5"},
    {"input_tokens": 2, "output_tokens": 390, "cache_read_input_tokens": 98101, "cache_creation_input_tokens": 0,
     "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "type": "fallback_message",
     "model": "claude-opus-4-8"}]
_FALLBACK_27_08 = (_request_lines("req_011CeTQmWnYoVsGZrpJVsvGh", "claude-fable-5", [_FB_FIRST], "cb6de03f")
                   + _request_lines("req_011CeTQmWnYoVsGZrpJVsvGh", "claude-opus-4-8", [_FB_FIRST, _FB_FIRST, _FB_FIRST, _FB_LAST],
                                    "cb6de03f", first=1))
_FALLBACK_27_08_REAL = (_request_lines("req_011CeTQmWnYoVsGZrpJVsvGh", "claude-fable-5", [_FB_FIRST], "cb6de03f")
                        + _request_lines("req_011CeTQmWnYoVsGZrpJVsvGh", "claude-opus-4-8",
                                         [_FB_FIRST, _FB_FIRST, _FB_FIRST, dict(_FB_LAST, iterations=_FB_ITERATIONS)],
                                         "cb6de03f", first=1))
# req_011CeTUqHEnonHCQfNdNXVaS (cb6de03f-....jsonl lines 655-659, model + usage only): five lines, EVERY one labelled
# opus-4-8 and every one carrying the same iterations -- a fable-5 message and an opus-4-8 fallback message.
_UQ_USAGE = {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 206526, "output_tokens": 874,
             "cache_creation": {"ephemeral_1h_input_tokens": 2972, "ephemeral_5m_input_tokens": 0},
             "iterations": [
                 {"input_tokens": 2, "output_tokens": 279, "cache_read_input_tokens": 229161, "cache_creation_input_tokens": 2972,
                  "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 2972}, "type": "message",
                  "model": "claude-fable-5"},
                 {"input_tokens": 2, "output_tokens": 874, "cache_read_input_tokens": 206526, "cache_creation_input_tokens": 0,
                  "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "type": "fallback_message",
                  "model": "claude-opus-4-8"}]}
_FALLBACK_UQ = _request_lines("req_011CeTUqHEnonHCQfNdNXVaS", "claude-opus-4-8", [_UQ_USAGE] * 5, "cb6de03f")
_FIXED_PRICES = {"claude-fable-5": {"input": 1e-05, "output": 5e-05}, "claude-opus-4-8": {"input": 5e-06, "output": 2.5e-05},
                 "claude-sonnet-5": {"input": 3e-06, "output": 1.5e-05},
                 "claude-fable-5-1": {"input": 1e-05, "output": 5e-05, "cache_read_multiplier": 0.025},
                 "claude-opus-5-5": {"input": 4e-06, "output": 2e-05, "cache_read_multiplier": 0.05}}


def _imported_rows(tmp_path, db_file, lines):
    """(import result, {dedupe_key: (model, input, output, cache write, cache read, 1h split, cost)}) of an import of
    `lines` as one transcript under the fixed price table."""
    transcript = tmp_path / "proj" / "s1.jsonl"
    _write_jsonl(transcript, lines)
    result = import_transcripts(str(transcript), db_file, load_prices(_prices_file(tmp_path, _FIXED_PRICES)))
    conn = sqlite3.connect(db_file)
    rows = {r[0]: r[1:] for r in conn.execute(
        "SELECT dedupe_key, model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens,"
        " cache_creation_1h_tokens, accounted_cost_usd FROM cc_usage")}
    conn.close()
    return result, rows


def test_f6_23_a_fallback_request_without_iterations_is_priced_per_model_by_the_max_of_its_lines(tmp_path, db_file):
    """The rule's second branch (no usage.iterations anywhere in the request): one part per MODEL of the lines, each
    the MAX per field over that model's lines, each priced by ITS OWN prices; the request is the sum. This is NOT the
    provider's figure for the real request (that carries iterations: 0.21261, see the next test) -- it is what the
    lines alone give. By hand, with the cache multipliers of F6-24 (write 1.25, read 0.1, no 1-hour part on any line):
      fable-5 (1e-05 / 5e-05), the part (2 in, 3 out, 625 write, 102517 read):
        2*1e-05 + 3*5e-05 + 625*1e-05*1.25 + 102517*1e-05*0.1 = 0.00002 + 0.00015 + 0.0078125 + 0.102517 = 0.1104995
      opus-4-8 (5e-06 / 2.5e-05), the part (2 in, 390 out, 625 write, 102517 read -- the MAX over its four lines):
        2*5e-06 + 390*2.5e-05 + 625*5e-06*1.25 + 102517*5e-06*0.1 = 0.00001 + 0.00975 + 0.00390625 + 0.0512585 = 0.06492475
      the request: 0.1104995 + 0.06492475 = 0.17542425.
    The two figures this request had before are neither: 0.0588105 (the old reader: the first line's tokens at the
    last line's price) and 0.1298495 (the first fold: the first model at the MAX tokens)."""
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, _FALLBACK_27_08)
    base = "cb6de03f:req_011CeTQmWnYoVsGZrpJVsvGh"
    assert warnings == [] and rows_imported == 2
    assert set(rows) == {base, base + "|claude-opus-4-8"}
    assert rows[base][:-1] == ("claude-fable-5", 2, 3, 625, 102517, 0)
    assert rows[base + "|claude-opus-4-8"][:-1] == ("claude-opus-4-8", 2, 390, 625, 102517, 0)
    assert rows[base][-1] == pytest.approx(0.1104995, rel=1e-12)
    assert rows[base + "|claude-opus-4-8"][-1] == pytest.approx(0.06492475, rel=1e-12)
    total = sum(r[-1] for r in rows.values())
    assert total == pytest.approx(0.17542425, rel=1e-12)
    assert total != pytest.approx(0.0588105, rel=1e-3) and total != pytest.approx(0.1298495, rel=1e-3)
    # every one of the five lines is a turn; the five carry two dedupe keys (the importer collapses the repeats)
    turns = list(iter_assistant_turns(str(tmp_path / "proj" / "s1.jsonl")))
    assert [t["dedupe_key"] for t in turns] == [base] + [base + "|claude-opus-4-8"] * 4
    assert [t["turn_index"] for t in turns] == [0, 1, 2, 3, 4]


def test_f6_23_the_27_08_fallback_request_is_priced_by_the_iterations_the_provider_wrote(tmp_path, db_file):
    """The rule's first branch: line 112 carries usage.iterations -- the provider's own per-message record -- so THAT
    is the carrier (P20: the record, not the lines' guess). By hand, prices of _FIXED_PRICES, write 1.25, read 0.1:
      fable-5 (1e-05 / 5e-05), the iterations entry (2 in, 869 out, 625 5m-write, 102517 read):
        2*1e-05 + 869*5e-05 + 625*1e-05*1.25 + 102517*1e-05*0.1 = 0.00002 + 0.04345 + 0.0078125 + 0.102517 = 0.1537995
      opus-4-8 (5e-06 / 2.5e-05), the fallback entry (2 in, 390 out, 0 write, 98101 read):
        2*5e-06 + 390*2.5e-05 + 98101*5e-06*0.1 = 0.00001 + 0.00975 + 0.0490505 = 0.0588105
      the request: 0.1537995 + 0.0588105 = 0.21261  (the provider's figure; the MAX reader gave 0.17542425).
    The negative control is the lines-only twin above: the same lines without the iterations stay at 0.17542425."""
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, _FALLBACK_27_08_REAL)
    base = "cb6de03f:req_011CeTQmWnYoVsGZrpJVsvGh"
    assert warnings == [] and rows_imported == 2
    assert set(rows) == {base, base + "|claude-opus-4-8"}
    assert rows[base][:-1] == ("claude-fable-5", 2, 869, 625, 102517, 0)
    assert rows[base + "|claude-opus-4-8"][:-1] == ("claude-opus-4-8", 2, 390, 0, 98101, 0)
    assert rows[base][-1] == pytest.approx(0.1537995, rel=1e-12)
    assert rows[base + "|claude-opus-4-8"][-1] == pytest.approx(0.0588105, rel=1e-12)
    assert sum(r[-1] for r in rows.values()) == pytest.approx(0.21261, rel=1e-12)


def test_f6_23_a_fallback_request_whose_lines_all_say_opus_is_priced_by_its_iterations(tmp_path, db_file):
    """req_011CeTUqHEnonHCQfNdNXVaS: five lines, every one labelled opus-4-8, so attempt 1 read it as a single-model
    request (0.125123). The iterations say fable-5 first. By hand (the 1-hour write at 2x the input price):
      fable-5 (2 in, 279 out, 229161 read, 2972 written at the 1-hour rate):
        2*1e-05 + 279*5e-05 + 229161*1e-05*0.1 + 2972*1e-05*2 = 0.00002 + 0.01395 + 0.229161 + 0.05944 = 0.302571
      opus-4-8 (2 in, 874 out, 206526 read, no write): 2*5e-06 + 874*2.5e-05 + 206526*5e-06*0.1 = 0.00001 + 0.02185 + 0.103263
        = 0.125123
      the request: 0.427694.
    The bare dedupe key stays on the model the lines are labelled with (opus: its row is the one a database filled by
    the old reader already holds); the fable part is `|claude-fable-5`, yielded by the first line."""
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, _FALLBACK_UQ)
    base = "cb6de03f:req_011CeTUqHEnonHCQfNdNXVaS"
    assert warnings == [] and rows_imported == 2
    assert set(rows) == {base, base + "|claude-fable-5"}
    assert rows[base][:-1] == ("claude-opus-4-8", 2, 874, 0, 206526, 0)
    assert rows[base + "|claude-fable-5"][:-1] == ("claude-fable-5", 2, 279, 2972, 229161, 2972)
    assert rows[base][-1] == pytest.approx(0.125123, rel=1e-12)
    assert rows[base + "|claude-fable-5"][-1] == pytest.approx(0.302571, rel=1e-12)
    assert sum(r[-1] for r in rows.values()) == pytest.approx(0.427694, rel=1e-12)
    turns = list(iter_assistant_turns(str(tmp_path / "proj" / "s1.jsonl")))
    # the labelled part (opus, the anchor) once per line; the fable part, no line is labelled with it, once, from line 1
    assert [t["dedupe_key"] for t in turns] == [base, base + "|claude-fable-5"] + [base] * 4
    assert [t["turn_index"] for t in turns] == [0, 0, 1, 2, 3, 4]


def test_f6_23_iterations_of_one_entry_are_the_max_reader(tmp_path, db_file):
    """The negative control of the carrier: every single-model request carries `iterations` with ONE entry (174,032 of
    273,485 real usage lines); they change nothing. The same three single-model requests with a one-entry iterations
    on every line give the rows the old reader stored."""
    lines = _single_model_lines()
    for line in lines:
        usage = line["message"]["usage"]
        usage["iterations"] = [dict(usage, type="message", model=line["message"]["model"])]
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == [] and rows_imported == 3
    for key, old in OLD_SINGLE_MODEL_ROWS.items():
        assert rows[key][:-1] == old[:-1], key
        assert rows[key][-1] == pytest.approx(old[-1], rel=1e-12), key


def test_f6_23_lines_labelled_with_a_model_the_iterations_do_not_name_follow_the_iterations(tmp_path, db_file):
    """Labels are not the carrier: lines labelled sonnet-5 whose iterations hold fable-5 and opus-4-8 give two rows by
    those models and none by sonnet; the anchor (the bare key) is the first part, the second is `|<model>`."""
    usage = dict(_FB_LAST, iterations=_FB_ITERATIONS)
    lines = _request_lines("r", "claude-sonnet-5", [_FB_FIRST, usage])
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == [] and rows_imported == 2
    assert set(rows) == {"s1:r", "s1:r|claude-opus-4-8"}
    assert rows["s1:r"][0] == "claude-fable-5" and rows["s1:r|claude-opus-4-8"][0] == "claude-opus-4-8"
    assert sum(r[-1] for r in rows.values()) == pytest.approx(0.21261, rel=1e-12)


def test_f6_23_two_iterations_of_one_model_are_two_rows(tmp_path, db_file):
    """Never merged, never overwritten: two entries of one model get distinct keys (`|<model>`, then `|<model>#2`)."""
    entry = {"input_tokens": 1000, "output_tokens": 100, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
             "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "type": "message"}
    iterations = [dict(entry, model="claude-sonnet-5"), dict(entry, model="claude-sonnet-5"),
                  dict(entry, model="claude-sonnet-5", output_tokens=300)]
    lines = _request_lines("r", "claude-sonnet-5", [dict(entry, iterations=iterations)])
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == [] and rows_imported == 3
    assert set(rows) == {"s1:r", "s1:r|claude-sonnet-5", "s1:r|claude-sonnet-5#2"}
    assert sorted(r[2] for r in rows.values()) == [100, 100, 300]


def test_f6_23_an_iterations_entry_with_an_unpriced_model_is_unpriced_never_a_neighbours_price(tmp_path, db_file):
    """FR-41 through the iterations branch: the entry whose model is absent from the price file has a NULL cost (its own
    row, the report says «partial»); the priced entry keeps its own cost."""
    iterations = [dict(_FB_ITERATIONS[0], model="claude-never-priced"), _FB_ITERATIONS[1]]
    lines = _request_lines("r", "claude-opus-4-8", [dict(_FB_LAST, iterations=iterations)])
    (_n, _s, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == []
    assert rows["s1:r|claude-never-priced"][-1] is None
    assert rows["s1:r"][-1] == pytest.approx(0.0588105, rel=1e-12)
    conn = sqlite3.connect(db_file)
    assert usage_report.unpriced_turns(conn) == {"claude-never-priced": 1}
    conn.close()


@pytest.mark.parametrize("bad_iterations", [
    "two messages",                                                            # not a list
    {"a": 1},                                                                  # not a list
    [dict(_FB_ITERATIONS[0]), {"input_tokens": 5, "output_tokens": 5}],        # an entry with no model
    [dict(_FB_ITERATIONS[0]), {"model": "claude-opus-4-8"}],                   # an entry with no usage
    [dict(_FB_ITERATIONS[0]), "claude-opus-4-8"],                              # an entry that is not an object
    [dict(_FB_ITERATIONS[0]), dict(_FB_ITERATIONS[1], output_tokens="many")],  # a mistyped value
], ids=["str", "dict", "no-model", "no-usage", "not-object", "mistyped"])
def test_f6_23_malformed_iterations_are_ignored_with_one_counted_warning_and_the_max_reader_is_used(tmp_path, db_file, bad_iterations):
    """No traceback, ONE warning (counted per line); the rows are the MAX reader's, i.e. those of the same lines
    without any iterations."""
    lines = _request_lines("r", "claude-opus-4-8", [_FB_FIRST, dict(_FB_LAST, iterations=bad_iterations)])
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == ["usage.iterations ignored (not a list, or an entry without a model or usage): 1 line(s); "
                        "the per-model MAX of the lines was used"]
    plain = _request_lines("r", "claude-opus-4-8", [_FB_FIRST, _FB_LAST])
    plain_dir = tmp_path / "plain"
    plain_dir.mkdir()
    (_n, _s, plain_warnings), plain_rows = _imported_rows(plain_dir, plain_dir / "requests.db", plain)
    assert plain_warnings == [] and rows == plain_rows and rows_imported == 1


def test_f6_23_an_iterations_entry_without_a_split_is_priced_as_a_5_minute_write_and_counted(tmp_path, db_file):
    """Never an invented proportion: the entry has 1000 written and no `cache_creation` object, so the write is priced
    at the 5-minute rate (1000*1e-05*1.25 = 0.0125) and ONE warning counts the missing split; the entry that has its
    split (1-hour 1000: 1000*5e-06*2 = 0.01) is priced by it."""
    no_split = dict(_FB_ITERATIONS[0], cache_creation_input_tokens=1000, input_tokens=0, output_tokens=0, cache_read_input_tokens=0)
    del no_split["cache_creation"]
    with_split = dict(_FB_ITERATIONS[1], cache_creation_input_tokens=1000, input_tokens=0, output_tokens=0, cache_read_input_tokens=0,
                      cache_creation={"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 1000})
    lines = _request_lines("r", "claude-opus-4-8", [dict(_FB_LAST, iterations=[no_split, with_split])])
    (_n, _s, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == ["split missing on an iterations entry: 1 (its cache writes are priced as 5-minute writes)"]
    assert rows["s1:r|claude-fable-5"][-2:] == (None, pytest.approx(0.0125, rel=1e-12))
    assert rows["s1:r"][-2:] == (1000, pytest.approx(0.01, rel=1e-12))


def test_f6_23_the_file_is_read_once_so_a_line_appended_while_importing_is_never_a_zero_row(tmp_path, monkeypatch):
    """t-886 F-2. The reader is replaced by one that yields from ONE list per call and grows it by a line of a new
    request after the first call (a live transcript between two passes). One pass: the new line is simply not seen
    (the next import takes it whole); two passes: it would meet the second pass with no part and be stored as a zero
    row that max-wins never repairs. Asserted: one call, no turn of the new request."""
    transcript = tmp_path / "proj" / "s1.jsonl"
    first = _request_lines("r1", "claude-sonnet-5", [{"input_tokens": 100, "output_tokens": 50}])
    grown = first + _request_lines("r2", "claude-sonnet-5", [{"input_tokens": 100, "output_tokens": 50}], first=9)
    _write_jsonl(transcript, first)
    calls = []

    def growing_reader(path):
        calls.append(path)
        return iter([json.dumps(o) for o in (first if len(calls) == 1 else grown)])

    monkeypatch.setattr(usage_report.transcripts, "iter_lines", growing_reader)
    turns = list(iter_assistant_turns(str(transcript)))
    assert len(calls) == 1
    assert [(t["dedupe_key"], t["output_tokens"]) for t in turns] == [("s1:r1", 50)]


def test_f6_23_a_line_appended_after_an_import_is_stored_whole_by_the_next_import(tmp_path, db_file):
    transcript = tmp_path / "proj" / "s1.jsonl"
    prices = load_prices(_prices_file(tmp_path, _FIXED_PRICES))
    _write_jsonl(transcript, _request_lines("r1", "claude-sonnet-5", [{"input_tokens": 100, "output_tokens": 50}]))
    import_transcripts(str(transcript), db_file, prices)
    _write_jsonl(transcript, _request_lines("r1", "claude-sonnet-5", [{"input_tokens": 100, "output_tokens": 50}])
                 + _request_lines("r2", "claude-sonnet-5", [{"input_tokens": 100, "output_tokens": 50}], first=9))
    import_transcripts(str(transcript), db_file, prices)
    conn = sqlite3.connect(db_file)
    assert conn.execute("SELECT input_tokens, output_tokens FROM cc_usage WHERE dedupe_key = 's1:r2'").fetchone() == (100, 50)
    conn.close()


def test_f6_23_two_models_in_one_request_are_the_sum_of_two_prices_with_the_cache_split_per_line(tmp_path, db_file):
    """By hand. sonnet-5 line: 1000 in, 100 out, 1000 written of which 600 at the 1-hour rate:
        1000*3e-06 + 100*1.5e-05 + 400*3e-06*1.25 + 600*3e-06*2 = 0.003 + 0.0015 + 0.0015 + 0.0036 = 0.0096
    opus-4-8 line: 2000 in, 400 out, 400 written, none at the 1-hour rate (the split says 0, a KNOWN split):
        2000*5e-06 + 400*2.5e-05 + 400*5e-06*1.25 = 0.01 + 0.01 + 0.0025 = 0.0225
    The request: 0.0321. The mutants: the whole request at the first model's price (the second line at sonnet-5:
    0.006 + 0.006 + 0.0015 = 0.0135, the request 0.0231) and the 1-hour part of the first line priced as a 5-minute
    write (1000*3e-06*1.25 = 0.00375, the first line 0.00825)."""
    first = {"input_tokens": 1000, "output_tokens": 100, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 0,
             "cache_creation": {"ephemeral_5m_input_tokens": 400, "ephemeral_1h_input_tokens": 600}}
    second = {"input_tokens": 2000, "output_tokens": 400, "cache_creation_input_tokens": 400, "cache_read_input_tokens": 0,
              "cache_creation": {"ephemeral_5m_input_tokens": 400, "ephemeral_1h_input_tokens": 0}}
    lines = _request_lines("r", "claude-sonnet-5", [first]) + _request_lines("r", "claude-opus-4-8", [second], first=1)
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == [] and rows_imported == 2
    assert rows["s1:r"][-2:] == (600, pytest.approx(0.0096, rel=1e-12))
    assert rows["s1:r|claude-opus-4-8"][-2:] == (0, pytest.approx(0.0225, rel=1e-12))
    assert sum(r[-1] for r in rows.values()) == pytest.approx(0.0321, rel=1e-12)


def test_f6_23_an_unpriced_model_in_a_multi_model_request_is_unpriced_never_priced_as_a_neighbour(tmp_path, db_file):
    """FR-41: the model with no price has a NULL cost (its own row, «unknown price: <model>: 1 turn(s)» in the report),
    is not given the price of the model beside it, and the report marks the total «partial»; nothing prices the
    whole request by the first model, also not the backfill that fills NULL costs later."""
    lines = (_request_lines("r", "claude-sonnet-5", [{"input_tokens": 1000, "output_tokens": 100}])
             + _request_lines("r", "claude-never-priced", [{"input_tokens": 5000, "output_tokens": 500}], first=1))
    (_n, _s, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == []
    assert rows["s1:r"][-1] == pytest.approx(1000 * 3e-06 + 100 * 1.5e-05, rel=1e-12)
    assert rows["s1:r|claude-never-priced"][-1] is None
    conn = sqlite3.connect(db_file)
    assert backfill_costs(conn, load_prices(_prices_file(tmp_path, _FIXED_PRICES))) == 0
    assert conn.execute("SELECT accounted_cost_usd FROM cc_usage WHERE model = 'claude-never-priced'").fetchone() == (None,)
    assert usage_report.unpriced_turns(conn) == {"claude-never-priced": 1}
    conn.close()


# Three single-model requests in the shape of real ones (model + usage copied; the requests are named per test): the old
# reader's rows are the NEGATIVE CONTROL -- the fold must not move a single-model request by one token or one cent.
#  S1 sonnet-5, a subagent request, req_011CfMRNedFf77wejvdD8KLV (agent-a2959d04d4b5eb18d.jsonl, 24.09): output 4/4/4/4/592
#  S2 fable-5-1, a main-chain request, req_011Cesr4hPVwENh2bSVsDhku (0b52ac4e-bbc7-4d7a-b054-3d01d6aacf5a.jsonl, 09.09): three
#     equal lines, a 1-hour write of 16864
#  S3 opus-5-5, req_011CfYcEvBFDqpeyfZA18dNK (agent-a0079aebca59bf4f6.jsonl, 29.09): output 7/7/331
def _single_model_lines():
    cw = {"ephemeral_5m_input_tokens": 29932, "ephemeral_1h_input_tokens": 0}
    s1 = [{"input_tokens": 2, "output_tokens": out, "cache_creation_input_tokens": 29932, "cache_read_input_tokens": 0,
           "cache_creation": cw} for out in (4, 4, 4, 4, 592)]
    s2 = [{"input_tokens": 2, "output_tokens": 528, "cache_creation_input_tokens": 16864, "cache_read_input_tokens": 42378,
           "cache_creation": {"ephemeral_1h_input_tokens": 16864, "ephemeral_5m_input_tokens": 0}}] * 3
    s3 = [{"input_tokens": 2, "output_tokens": out, "cache_creation_input_tokens": 25587, "cache_read_input_tokens": 32427,
           "cache_creation": {"ephemeral_5m_input_tokens": 25587, "ephemeral_1h_input_tokens": 0}} for out in (7, 7, 331)]
    return (_request_lines("req_011CfMRNedFf77wejvdD8KLV", "claude-sonnet-5", s1)
            + _request_lines("req_011Cesr4hPVwENh2bSVsDhku", "claude-fable-5-1", s2)
            + _request_lines("req_011CfYcEvBFDqpeyfZA18dNK", "claude-opus-5-5", s3))


# The rows the OLD reader (72e2f22c, before the fold) stored for _single_model_lines under _FIXED_PRICES, captured by running
# that commit's usage_report over exactly these lines: (model, input, output, cache write, cache read, 1-hour split, cost).
OLD_SINGLE_MODEL_ROWS = {
    "s1:req_011CfMRNedFf77wejvdD8KLV": ("claude-sonnet-5", 2, 592, 29932, 0, 0, 0.121131),
    "s1:req_011Cesr4hPVwENh2bSVsDhku": ("claude-fable-5-1", 2, 528, 16864, 42378, 16864, 0.37429450000000003),
    "s1:req_011CfYcEvBFDqpeyfZA18dNK": ("claude-opus-5-5", 2, 331, 25587, 32427, 0, 0.1410484),
}


def test_f6_23_single_model_requests_are_unchanged_against_the_old_reader(tmp_path, db_file):
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, _single_model_lines())
    assert warnings == [] and rows_imported == 3
    assert set(rows) == set(OLD_SINGLE_MODEL_ROWS)
    for key, old in OLD_SINGLE_MODEL_ROWS.items():
        assert rows[key][:-1] == old[:-1], key
        assert rows[key][-1] == pytest.approx(old[-1], rel=1e-12), key


def test_f6_23_a_usage_that_is_not_an_object_or_is_mistyped_is_skipped_with_one_counted_warning(tmp_path, db_file):
    """No traceback, one WARN for all of them; the good lines are imported; `usage: null` is an absent usage, not a
    bad one (it never was a warning)."""
    def bare(request_id, usage):
        line = _assistant_line(session_id="s1", request_id=request_id, uuid=request_id)
        line["message"]["usage"] = usage
        return line
    lines = [bare("a", "text"), bare("b", [1, 2]), bare("c", {"output_tokens": "many"}), bare("d", 7), bare("n", None),
             _assistant_line(session_id="s1", request_id="good", uuid="good")]
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == ["usage blocks skipped (not an object, or a mistyped value): 4"]
    assert set(rows) == {"s1:good", "s1:n"} and rows_imported == 2
    assert rows["s1:n"][1:5] == (0, 0, 0, 0)  # the null usage: zeros, as before


def test_f6_23_a_line_with_neither_request_id_nor_uuid_is_its_own_row_and_is_counted(tmp_path, db_file):
    lines = [_assistant_line(session_id="s1", request_id=None, uuid=None) for _ in range(2)]
    lines.insert(1, _assistant_line(session_id="s1", request_id="real", uuid="real"))
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, lines)
    assert warnings == ["turns without a requestId and a uuid: 2 (each its own row, keyed by its line position)"]
    assert rows_imported == 3 and set(rows) == {"s1:line:s1:1", "s1:real", "s1:line:s1:3"}
    # a second import of the same file: the keys are stable, nothing new
    again = import_transcripts(str(tmp_path / "proj" / "s1.jsonl"), db_file, load_prices(_prices_file(tmp_path, _FIXED_PRICES)))
    assert again[0] == 0


def test_f6_23_a_request_with_no_usage_line_gets_no_part_and_no_warning(tmp_path, db_file):
    """The edge: assistant lines of a request carrying no usage at all join nothing (transcripts.request_parts gives no
    record); the row stays what it was before the fold -- zero tokens at the model's price, no warning."""
    line = _assistant_line(session_id="s1", request_id="z", uuid="z")
    del line["message"]["usage"]
    (rows_imported, _sessions, warnings), rows = _imported_rows(tmp_path, db_file, [line, dict(line, uuid="z2")])
    assert warnings == [] and rows_imported == 1
    assert rows == {"s1:z": ("claude-sonnet-5", 0, 0, 0, 0, None, 0.0)}
