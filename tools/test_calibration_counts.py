"""Tests for tools/calibration_counts.py. Synthetic journal fixtures on
tmp_path, one case per class from the spec, plus a CLI smoke test."""
import json

import pytest

from calibration_counts import analyze_journal, main, parse_ts


def write_journal(path, lines):
    """lines: a list of dicts OR raw strings (for unparsable lines /
    the spaced-JSON format)."""
    with open(path, "w", encoding="utf-8") as fh:
        for line in lines:
            if isinstance(line, str):
                fh.write(line + "\n")
            else:
                fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def ev(ts, event, **kw):
    d = {"ts": ts, "event": event}
    d.update(kw)
    return d


# ---------------------------------------------------------------------
# 1. rule-6 pair without escalated -> candidate
# ---------------------------------------------------------------------
def test_rule6_pair_without_escalated_is_candidate(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "journal_created", notes="init"),
        ev("2026-07-08T01:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:10:00", "rejected", agent="scout", model="haiku",
           task_id="t-001", attempt=1, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-08T01:20:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:30:00", "rejected", agent="scout", model="haiku",
           task_id="t-001", attempt=2, failure_class="tooling", category="recon", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert len(report["rule6_candidates"]) == 1
    assert report["rule6_candidates"][0]["task_id"] == "t-001"


# ---------------------------------------------------------------------
# 2. rule-6 pair WITH escalated -> NOT a candidate
# ---------------------------------------------------------------------
def test_rule6_pair_with_escalated_not_candidate(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "journal_created", notes="init"),
        ev("2026-07-08T01:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:10:00", "rejected", agent="scout", model="haiku",
           task_id="t-001", attempt=1, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-08T01:20:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:30:00", "rejected", agent="scout", model="haiku",
           task_id="t-001", attempt=2, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-08T01:40:00", "escalated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert report["rule6_candidates"] == []


# ---------------------------------------------------------------------
# 3. rejected without failure_class -> violation
# ---------------------------------------------------------------------
def test_rejected_missing_failure_class_is_violation(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-09T00:10:00", "rejected", agent="builder", model="sonnet",
           task_id="t-001", attempt=1, category="implementation", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    viol = [v for v in report["field_violations"] if v["event"] == "rejected"]
    assert len(viol) == 1
    assert "failure_class" in viol[0]["missing_fields"]


# ---------------------------------------------------------------------
# 4. accepted(builder) without witness -> violation
# ---------------------------------------------------------------------
def test_accepted_builder_missing_witness_is_violation(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-09T00:10:00", "accepted", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    viol = [v for v in report["field_violations"] if v["event"] == "accepted"]
    assert len(viol) == 1
    assert "witness" in viol[0]["missing_fields"]


# ---------------------------------------------------------------------
# 5. missing 'by' after the cutoff vs. legal before it
# ---------------------------------------------------------------------
def test_by_missing_after_cutoff_legal_before(tmp_path):
    p = tmp_path / "j.jsonl"
    by_since = "2026-07-10T13:14:00"
    write_journal(p, [
        ev("2026-07-09T00:00:00", "accepted", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),  # before cutoff, no by -> legal
        ev("2026-07-10T14:00:00", "accepted", agent="scout", model="haiku",
           task_id="t-002", category="recon", notes="n"),  # after cutoff, no by -> candidate
        ev("2026-07-10T15:00:00", "accepted", agent="scout", model="haiku",
           task_id="t-003", category="recon", notes="n", by="fable"),  # after, with by -> ok
    ])
    report = analyze_journal(str(p), None, None, parse_ts(by_since))
    assert len(report["by_violations"]) == 1
    assert report["by_violations"][0]["task_id"] == "t-002"


# ---------------------------------------------------------------------
# 6. duplicate task_id: after accepted / critic-entry / continuation / retry
# ---------------------------------------------------------------------
def test_duplicate_delegate_after_accepted_is_candidate(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T00:10:00", "accepted", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T00:20:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),  # duplicate/reopen, no attempt>=2, not critic
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    dups = report["duplicate_delegates"]
    assert len(dups) == 1
    assert dups[0]["branch"] == "candidate-duplicate"


def test_duplicate_delegate_critic_entry_is_legal_branch(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-08T00:10:00", "accepted", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n", witness="ok"),
        ev("2026-07-08T00:20:00", "delegated", agent="critic", model="opus",
           task_id="t-001", category="review", notes="n"),  # critic-entry on an open/closed task
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    dups = report["duplicate_delegates"]
    assert len(dups) == 1
    assert dups[0]["branch"] == "critic-entry"


def test_duplicate_delegate_continuation_after_rejected(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-08T00:10:00", "rejected", agent="builder", model="sonnet",
           task_id="t-001", attempt=1, failure_class="spec", category="implementation", notes="n"),
        ev("2026-07-08T00:20:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),  # continuation, same tier
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    dups = report["duplicate_delegates"]
    assert len(dups) == 1
    assert dups[0]["branch"] == "continuation"


def test_duplicate_delegate_retry_attempt_2(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-08T00:10:00", "rejected", agent="builder", model="sonnet",
           task_id="t-001", attempt=1, failure_class="tooling", category="implementation", notes="n"),
        ev("2026-07-08T00:20:00", "escalated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-08T00:30:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", attempt=2, category="implementation", notes="n"),  # retry, post-escalation
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    dups = report["duplicate_delegates"]
    assert len(dups) == 1
    assert dups[0]["branch"] == "retry"


# ---------------------------------------------------------------------
# 7. ts non-monotonicity
# ---------------------------------------------------------------------
def test_ts_non_monotonic_detected(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T10:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T09:00:00", "accepted", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),  # earlier than the previous line
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert len(report["ts_anomalies"]) == 1
    assert report["ts_anomalies"][0]["line"] == 2


# ---------------------------------------------------------------------
# 8. unparsable line
# ---------------------------------------------------------------------
def test_unparsable_line_reported(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "journal_created", notes="init"),
        "{ this is not valid json",
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert len(report["unparsable"]) == 1
    assert report["unparsable"][0]["line"] == 2


# ---------------------------------------------------------------------
# 9. the spaced-JSON format (spaces after colons)
# ---------------------------------------------------------------------
def test_external_journal_format_with_spaces_parses(tmp_path):
    p = tmp_path / "j.jsonl"
    raw = ('{"ts": "2026-07-08T00:00:00", "event": "delegated", "agent": "builder", '
           '"category": "implementation", "notes": "n", "task_id": "at-bug-001"}')
    write_journal(p, [raw])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert report["parsed_lines"] == 1
    assert report["unparsable"] == []
    assert report["counts"]["by_event"]["delegated"] == 1


# ---------------------------------------------------------------------
# 10. window filter
# ---------------------------------------------------------------------
def test_window_filter_excludes_outside_events(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-09T00:00:00", "accepted", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-10T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-002", category="recon", notes="n"),
    ])
    start = parse_ts("2026-07-09T00:00:00")
    end = parse_ts("2026-07-10T00:00:00")
    report = analyze_journal(str(p), start, end, parse_ts("2026-07-10T13:14:00"))
    assert report["in_window_count"] == 1
    assert report["counts"]["by_event"] == {"accepted": 1}


# ---------------------------------------------------------------------
# 11. legacy section, pre-typed-fields-schema (migration installs only:
# a fresh install keeps both cutovers at the epoch, so the legacy branch
# is exercised here by patching the cutoff the way a migrating
# deployment would set it)
# ---------------------------------------------------------------------
def test_legacy_events_before_cutoff_not_counted_as_violation(tmp_path, monkeypatch):
    import calibration_counts as cc
    monkeypatch.setattr(cc, "LEGACY_CUTOFF", "2026-07-08T20:00:00")
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        # before the (patched) LEGACY_CUTOFF, rejected with no
        # failure_class -- legacy
        ev("2026-07-08T10:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-001", category="implementation", notes="n"),
        ev("2026-07-08T10:10:00", "rejected", agent="builder", model="sonnet",
           task_id="t-001", attempt=1, category="implementation", notes="n"),
        # after the cutoff, the same defect -- a real violation
        ev("2026-07-09T10:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-002", category="implementation", notes="n"),
        ev("2026-07-09T10:10:00", "rejected", agent="builder", model="sonnet",
           task_id="t-002", attempt=1, category="implementation", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert len(report["legacy_events"]) == 1
    assert report["legacy_events"][0]["task_id"] == "t-001"
    field_viol_task_ids = [v["task_id"] for v in report["field_violations"]]
    assert "t-002" in field_viol_task_ids
    assert "t-001" not in field_viol_task_ids


# ---------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------
def test_cli_json_smoke(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "journal_created", notes="init"),
        ev("2026-07-08T01:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:10:00", "accepted", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
    ])
    # a direct call to the module's main() is more reliable than subprocess
    # (not tied to cwd/PYTHONPATH)
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(["--journal", str(p), "--json"])
    assert code == 0
    parsed = json.loads(buf.getvalue())
    assert "journals" in parsed
    assert len(parsed["journals"]) == 1
    assert parsed["journals"][0]["counts"]["by_event"]["delegated"] == 1


def test_cli_text_mode_exit_zero(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-08T00:00:00", "journal_created", notes="init"),
    ])
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(["--journal", str(p)])
    assert code == 0
    assert "journal_created" in buf.getvalue()


def test_cli_invalid_window_start_exit_2(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    code = main(["--journal", str(p), "--window-start", "not-a-date"])
    assert code == 2


def test_cli_missing_file_exit_2(tmp_path):
    code = main(["--journal", str(tmp_path / "does-not-exist.jsonl")])
    assert code == 2


# ---------------------------------------------------------------------
# Schema constants stay in sync with journal_validator (a prior review
# finding): both copies encode the SAME typed-fields schema (a gate on
# write, a counter on read); a silent divergence would quietly skew the
# calibration count.
# ---------------------------------------------------------------------
def test_schema_constants_match_journal_validator():
    import journal_validator as jv
    import calibration_counts as cc
    assert cc.MODEL_REQUIRED_EVENTS == jv.MODEL_REQUIRED_EVENTS
    assert cc.TASK_ID_REQUIRED_EVENTS == jv.TASK_ID_REQUIRED_EVENTS
    assert cc.FAILURE_CLASSES == jv.FAILURE_CLASSES


# ---------------------------------------------------------------------
# The "other" branch (a prior review finding): a repeated delegated
# AFTER escalated with no attempt (a live precedent) -> an honest
# catch-all, surfaced in the report with prior_status for a human
# verdict.
# ---------------------------------------------------------------------
def test_duplicate_delegate_after_escalated_without_attempt_is_other(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T01:00:00", "delegated", agent="scout", model="m",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-09T01:10:00", "rejected", agent="scout", model="m",
           task_id="t-001", attempt=1, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-09T01:15:00", "rejected", agent="scout", model="m",
           task_id="t-001", attempt=2, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-09T01:20:00", "escalated", agent="scout", model="m",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-09T01:30:00", "delegated", agent="scout", model="m",
           task_id="t-001", category="recon", notes="attempt 3 with no attempt field"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    other = [d for d in report["duplicate_delegates"] if d["branch"] == "other"]
    assert len(other) == 1
    assert other[0]["prior_status"] == "escalated"
    assert other[0]["attempt"] is None


# ---------------------------------------------------------------------
# False-accept rate by tier (a prior review finding).
# ---------------------------------------------------------------------
def test_false_accept_rate_per_agent(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T01:00:00", "delegated", agent="builder", model="m",
           task_id="t-001", category="i", notes="n"),
        ev("2026-07-09T01:10:00", "accepted", agent="builder", model="m",
           task_id="t-001", witness="w", category="i", notes="n"),
        ev("2026-07-09T01:20:00", "delegated", agent="builder", model="m",
           task_id="t-002", category="i", notes="n"),
        ev("2026-07-09T01:30:00", "accepted", agent="builder", model="m",
           task_id="t-002", witness="w", category="i", notes="n"),
        ev("2026-07-09T02:00:00", "defect_found", agent="builder", model="m",
           task_id="t-003", ref="t-001", category="i", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    fa = report["false_accept"]["builder"]
    assert fa == {"defect_found": 1, "accepted": 2, "rate": 0.5}


# ---------------------------------------------------------------------
# Degradation pairs (journal side): a closed pair and an unclosed tail.
# ---------------------------------------------------------------------
def test_degradation_pairs_closed_and_open_tail(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T01:00:00", "lead_degraded", agent="lead", model="opus",
           category="degradation", notes="switch down"),
        ev("2026-07-09T02:00:00", "lead_restored", agent="lead", model="fable",
           category="degradation", notes="window review: empty"),
        ev("2026-07-09T03:00:00", "lead_degraded", agent="lead", model="sonnet",
           category="degradation", notes="switch down again"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    pairs = report["degradation_pairs"]
    assert len(pairs) == 2
    assert pairs[0]["note"] == "closed"
    assert pairs[0]["restored_line"] == 2
    assert pairs[1]["restored_line"] is None
    assert "NOT CLOSED" in pairs[1]["note"]


# ---------------------------------------------------------------------
# rejected distribution by failure_class x agent x model.
# ---------------------------------------------------------------------
def test_rejected_distribution_grouping(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T01:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-09T01:10:00", "rejected", agent="scout", model="haiku",
           task_id="t-001", attempt=1, failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-09T01:20:00", "delegated", agent="builder", model="sonnet",
           task_id="t-002", category="i", notes="n"),
        ev("2026-07-09T01:30:00", "rejected", agent="builder", model="sonnet",
           task_id="t-002", attempt=1, failure_class="spec", category="i", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    dist = {(d["failure_class"], d["agent"], d["model"]): d["count"]
            for d in report["rejected_distribution"]}
    assert dist == {("tooling", "scout", "haiku"): 1, ("spec", "builder", "sonnet"): 1}


# ---------------------------------------------------------------------
# Unclosed tasks: last lifecycle event is delegated -> listed.
# ---------------------------------------------------------------------
def test_unclosed_tasks_listed(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-09T01:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        ev("2026-07-09T01:10:00", "delegated", agent="builder", model="sonnet",
           task_id="t-002", category="i", notes="n"),
        ev("2026-07-09T01:30:00", "accepted", agent="builder", model="sonnet",
           task_id="t-002", witness="w", category="i", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-10T13:14:00"))
    assert report["unclosed_tasks"] == ["t-001"]


# ---------------------------------------------------------------------
# A prior review finding: closing semantics in "unclosed tasks" -- a
# closes: token in ANY later event's notes, and decomposable as a
# closing status. Case 3 (regression guard: a purely open delegated ->
# IS in unclosed) is already covered by test_unclosed_tasks_listed
# above -- not duplicated here.
# ---------------------------------------------------------------------
def test_unclosed_closed_by_closes_token_in_later_event(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-001", category="recon", notes="n"),
        # a later event that is NOT a lifecycle event (calibrated), but
        # its notes still carry a closes: token that must close t-001
        ev("2026-07-15T01:00:00", "calibrated", agent="lead", model="fable",
           category="calibration", notes="weekly run closes:t-001"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []


def test_unclosed_closed_by_decomposable(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-002", category="recon", notes="n"),
        ev("2026-07-15T00:10:00", "decomposable", agent="scout", model="haiku",
           task_id="t-002", category="recon", notes="decomposable into parts"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []
    assert report["closed_by_decomposable"] == ["t-002"]


def test_unclosed_closes_token_trailing_punctuation(tmp_path):
    # "closes:t-042;" -- closes per the scanner's own shape
    # (session_context.py's _CLOSES_RE: t-\d+, trailing punctuation is
    # naturally excluded by \d+ itself, no separate trimming needed).
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-042", category="implementation", notes="n"),
        ev("2026-07-15T00:10:00", "dispatch_skipped", agent="builder", model="sonnet",
           category="implementation", notes="small-work batch; closes:t-042; continued in t-050"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []


# ---------------------------------------------------------------------
# accepted_tids (journal law, mirroring session_context.py): ANY
# accepted closes its task_id unconditionally, regardless of file
# position or ts. The load-bearing case: an orphan delegated inserted
# IN THE FILE after its own accepted (file position lies, ts is
# truthful) -- a plain last-lifecycle-status-by-position scan would
# wrongly list that task as still open.
# ---------------------------------------------------------------------
def test_accepted_closes_task_even_when_orphan_delegated_is_later_in_file(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-10T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-099", category="recon", notes="n"),
        ev("2026-07-10T00:10:00", "accepted", agent="lead", model="fable",
           task_id="t-099", by="fable", category="recon", notes="n"),
        # Orphan delegated: written LATER in the file, but its own ts is
        # EARLIER than the accepted above (a ts-unordered segment) --
        # file position lies, ts is truthful; this must NOT reopen the
        # task for this counter.
        ev("2026-07-09T23:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-099", category="recon", notes="retro/duplicate entry"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []


def test_accepted_with_empty_or_non_string_task_id_ignored_no_crash(tmp_path):
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-003", category="recon", notes="n"),
        ev("2026-07-15T00:10:00", "accepted", agent="lead", model="fable",
           task_id="", by="fable", category="recon", notes="n"),
        ev("2026-07-15T00:20:00", "accepted", agent="lead", model="fable",
           task_id=123, by="fable", category="recon", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    # Neither malformed accepted closes t-003 -- it is still genuinely
    # open (a plain delegated with no real accepted of its own).
    assert report["unclosed_tasks"] == ["t-003"]


def test_empty_journal_no_accepted_output_unchanged(tmp_path):
    """Regression pin: an empty journal (no accepted at all) produces
    the same unclosed-tasks output as before this fix -- an empty
    list, no crash on the new accepted_tids machinery."""
    p = tmp_path / "j.jsonl"
    write_journal(p, [])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []
    assert report["closed_by_decomposable"] == []


def test_last_status_decomposable_with_accepted_closed_by_accepted_not_decomposable(tmp_path):
    """Order pin: when a task's last lifecycle status (by file order) is
    decomposable BUT it also carries an accepted somewhere in the
    journal, accepted_tids is checked FIRST -- the task is closed via
    the accepted path, not counted in closed_by_decomposable."""
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="scout", model="haiku",
           task_id="t-004", category="recon", notes="n"),
        ev("2026-07-15T00:10:00", "decomposable", agent="scout", model="haiku",
           task_id="t-004", category="recon", notes="decomposable into parts"),
        ev("2026-07-15T00:20:00", "accepted", agent="lead", model="fable",
           task_id="t-004", by="fable", category="recon", notes="n"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []
    assert report["closed_by_decomposable"] == []


def test_closes_token_and_accepted_both_present_no_double_counting(tmp_path):
    """Both a closes: token AND a real accepted close the same task --
    it must appear closed (not in unclosed_tasks), counted once, no
    double-accounting artifact."""
    p = tmp_path / "j.jsonl"
    write_journal(p, [
        ev("2026-07-15T00:00:00", "delegated", agent="builder", model="sonnet",
           task_id="t-005", category="implementation", notes="n"),
        ev("2026-07-15T00:10:00", "accepted", agent="lead", model="fable",
           task_id="t-005", by="fable", category="implementation", notes="n"),
        ev("2026-07-15T00:20:00", "dispatch_skipped", agent="builder", model="sonnet",
           category="implementation", notes="small-work batch; closes:t-005"),
    ])
    report = analyze_journal(str(p), None, None, parse_ts("2026-07-16T00:00:00"))
    assert report["unclosed_tasks"] == []
    assert report["closed_by_decomposable"] == []


# ---------------------------------------------------------------------
# B-402 (K6): sections 2 and 10 are keyed by the task key (label, task_id); section 5 stays bare
# ---------------------------------------------------------------------
import calibration_counts as cc
import journal_keys as jk

WINDOW_END = parse_ts("2026-07-16T00:00:00")


def _ek(ts, event, tid="t-050", agent="scout", **kw):
    return ev(ts, event, agent=agent, model="haiku", task_id=tid, category="recon", notes="n", **kw)


def _declare(tmp_path, lines, *idents_of, label="codex-fixes"):
    """Writes journal-segments.json beside the journal declaring the given line dicts."""
    segs = jk.Segments(1, [(label, "t-050 issued by both clones", tuple(jk.identity(l) for l in idents_of))])
    (tmp_path / "journal-segments.json").write_text(jk.dumps_declaration(segs), encoding="utf-8")


def _two_clones(tmp_path, extra_a=(), extra_b=()):
    a_d = _ek("2026-07-15T10:00:00", "delegated", worker_ref="agent:aaa")
    b_d = _ek("2026-07-15T11:00:00", "delegated", worker_ref="agent:bbb")
    b_acc = _ek("2026-07-15T11:05:00", "accepted", by="sonnet")
    lines = [a_d, b_d, b_acc, *extra_a, *extra_b]
    p = tmp_path / "j.jsonl"
    write_journal(p, lines)
    return p, a_d, b_d, b_acc


def test_k6_unclosed_declared_instance_is_listed_and_the_bare_reading_hides_it(tmp_path):
    p, a_d, _b, _c = _two_clones(tmp_path)
    assert analyze_journal(str(p), None, None, WINDOW_END)["unclosed_tasks"] == []          # no declaration: the false close
    _declare(tmp_path, None, a_d)
    assert analyze_journal(str(p), None, None, WINDOW_END)["unclosed_tasks"] == ["t-050@codex-fixes"]


def test_k6_qualified_closes_token_closes_exactly_that_instance(tmp_path):
    closer = ev("2026-07-15T12:00:00", "dispatch_skipped", agent="lead", category="x",
                notes="closes:t-050@codex-fixes accepted on its clone")
    p, a_d, _b, _c = _two_clones(tmp_path, extra_a=[closer])
    _declare(tmp_path, None, a_d)
    assert analyze_journal(str(p), None, None, WINDOW_END)["unclosed_tasks"] == []
    # a bare token carried by an undeclared event closes the undeclared key only
    bare = ev("2026-07-15T12:00:00", "dispatch_skipped", agent="lead", category="x", notes="closes:t-050 done")
    p, a_d, _b, _c = _two_clones(tmp_path, extra_a=[bare])
    assert analyze_journal(str(p), None, None, WINDOW_END)["unclosed_tasks"] == ["t-050@codex-fixes"]


def test_k6_section_2_escalation_pairing_is_keyed(tmp_path):
    a_d = _ek("2026-07-15T10:00:00", "delegated", worker_ref="agent:aaa")
    a_r1 = _ek("2026-07-15T10:10:00", "rejected", attempt=1, failure_class="tooling")
    a_r2 = _ek("2026-07-15T10:20:00", "rejected", attempt=2, failure_class="tooling")
    b_d = _ek("2026-07-15T11:00:00", "delegated", worker_ref="agent:bbb")
    b_esc = _ek("2026-07-15T11:30:00", "escalated")
    p = tmp_path / "j.jsonl"
    write_journal(p, [a_d, a_r1, a_r2, b_d, b_esc])
    assert analyze_journal(str(p), None, None, WINDOW_END)["rule6_candidates"] == []        # glued: the other clone's escalated pairs it
    _declare(tmp_path, None, a_d, a_r1, a_r2)
    got = analyze_journal(str(p), None, None, WINDOW_END)["rule6_candidates"]
    assert len(got) == 1 and got[0]["task_id"] == "t-050@codex-fixes"


def test_k6_section_5_repeated_delegated_stays_bare(tmp_path):
    a_d = _ek("2026-07-15T10:00:00", "delegated", worker_ref="agent:aaa")
    a_acc = _ek("2026-07-15T10:05:00", "accepted", by="sonnet")
    b_d = _ek("2026-07-15T11:00:00", "delegated", worker_ref="agent:bbb")
    p = tmp_path / "j.jsonl"
    write_journal(p, [a_d, a_acc, b_d])
    before = analyze_journal(str(p), None, None, WINDOW_END)["duplicate_delegates"]
    assert len(before) == 1 and before[0]["branch"] == "candidate-duplicate"
    _declare(tmp_path, None, a_d, a_acc)
    after = analyze_journal(str(p), None, None, WINDOW_END)["duplicate_delegates"]
    assert after == before                                          # id reuse after an accepted is ALWAYS a candidate


def test_k6_no_declaration_gives_the_same_report_as_an_empty_one(tmp_path):
    p, *_ = _two_clones(tmp_path)
    base = analyze_journal(str(p), None, None, WINDOW_END)
    (tmp_path / "journal-segments.json").write_text('{"version": 1, "segments": []}', encoding="utf-8")
    assert analyze_journal(str(p), None, None, WINDOW_END) == base


def test_k6_a_broken_declaration_reads_as_none_and_says_so_on_stderr(tmp_path, capsys):
    p, *_ = _two_clones(tmp_path)
    base = analyze_journal(str(p), None, None, WINDOW_END)
    capsys.readouterr()
    for payload in (b"\x00{{{", b"[]", b'{"version": 2, "segments": []}', b"\xff\xfe"):
        (tmp_path / "journal-segments.json").write_bytes(payload)
        assert analyze_journal(str(p), None, None, WINDOW_END) == base
        err = capsys.readouterr().err
        assert "task-key declaration beside" in err and "colliding task ids are read as one task" in err


def test_k6_without_journal_keys_the_script_runs_and_reads_a_qualified_token_as_bare(tmp_path, monkeypatch):
    closer = ev("2026-07-15T12:00:00", "dispatch_skipped", agent="lead", category="x", notes="closes:t-050@x")
    p, a_d, _b, _c = _two_clones(tmp_path, extra_a=[closer])
    _declare(tmp_path, None, a_d)
    monkeypatch.setattr(cc, "_jk", None)
    report = analyze_journal(str(p), None, None, WINDOW_END)
    assert report["unclosed_tasks"] == []                           # bare: the accepted closes t-050
    assert cc._closes_key("t-050@x", {}, None) == ("", "t-050")


def test_k6_closes_token_shapes():
    assert cc.extract_closes_tokens("closes:t-050 closes:t-051@codex-fixes.") == ["t-050", "t-051@codex-fixes"]
    assert cc.extract_closes_tokens("closes:t-050@Codex") == []             # a malformed label closes nothing
    assert cc.extract_closes_tokens("discloses:t-050") == [] and cc.extract_closes_tokens(None) == []


def test_k6_fallback_regex_is_pinned_equal_to_journal_keys_and_reads_the_same(monkeypatch):
    assert cc.CLOSES_RE.pattern == jk.CLOSES_RE.pattern
    samples = ["closes:t-050 closes:t-051@codex-fixes.", "closes:t-050@Codex", "closes:t-050@", "discloses:t-050",
               "closes:t-050@codex_x closes:t-051", "closes:t-5", "closes:t-050@" + "a" * 25]
    want = [jk.closes_tokens(s) for s in samples]
    monkeypatch.setattr(cc, "_jk", None)
    assert [cc.extract_closes_tokens(s) for s in samples] == want


def test_k6_a_malformed_label_closes_nothing_and_a_valid_one_closes_its_instance(tmp_path):
    def run(notes):
        closer = ev("2026-07-15T12:00:00", "dispatch_skipped", agent="lead", category="x", notes=notes)
        a_d = _ek("2026-07-15T10:00:00", "delegated", worker_ref="agent:aaa")
        b_d = _ek("2026-07-15T11:00:00", "delegated", worker_ref="agent:bbb")      # the undeclared instance, open too
        p = tmp_path / "j.jsonl"
        write_journal(p, [a_d, b_d, closer])
        _declare(tmp_path, None, a_d, label="codex")
        return analyze_journal(str(p), None, None, WINDOW_END)["unclosed_tasks"]
    assert run("nothing closes") == ["t-050", "t-050@codex"]
    assert run("closes:t-050@Codex") == ["t-050", "t-050@codex"]       # closes nothing: neither instance
    assert run("closes:t-050@nolabel") == ["t-050", "t-050@codex"]     # an undeclared label: nothing either
    assert run("closes:t-050@codex") == ["t-050"]                      # exactly the codex one
    assert run("closes:t-050") == ["t-050@codex"]                      # bare, from a carrier without task_id: the undeclared one


# ---------------------------------------------------------------------
# K14 (t-581, F0-4): no --journal = every file of the root, sections by file, closes across files
# ---------------------------------------------------------------------
from test_journal_per_developer import (DEV1, DEV2, M_CREATED, N_CREATED, accepted as _acc14,
                                        delegated as _dl14, ev as _ev14, jtext as _jt14, make_root as _root14)


def _k14(tmp_path, capsys, dev1_extra=(), dev2_lines=None, args=()):
    n_lines = dev2_lines if dev2_lines is not None else [_dl14("t-001", "2026-10-02T09:00:00"),
                                                                _dl14("t-002", "2026-10-02T09:10:00")]
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED, _dl14("t-003", "2026-10-02T08:30:00"), *dev1_extra),
                                    DEV2: _jt14(N_CREATED, *n_lines)}, slug="dev1")
    rc = main(["--root", str(root), "--json", *args])
    out = capsys.readouterr()
    return rc, json.loads(out.out)["journals"] if rc == 0 else None, out.err


def _by_name(reports):
    return {r["journal"].replace("\\", "/").rsplit("/", 1)[-1]: r for r in reports}


def test_k14_default_mode_reads_the_history_and_every_developer_file_one_report_each(tmp_path, capsys):
    rc, reports, _ = _k14(tmp_path, capsys)
    assert rc == 0 and list(_by_name(reports)) == ["routing-log.jsonl", "dev1.jsonl", "dev2.jsonl"]
    by = _by_name(reports)
    assert by["routing-log.jsonl"]["counts"]["by_event"] == {"delegated": 2, "accepted": 1}
    assert by["dev1.jsonl"]["counts"]["by_event"] == {"journal_created": 1, "delegated": 1}
    assert by["dev2.jsonl"]["counts"]["by_event"] == {"journal_created": 1, "delegated": 2}


def test_k14_unclosed_tasks_are_by_key_across_files(tmp_path, capsys):
    close_hist = _acc14("t-002", "2026-10-02T09:00:00")                     # the owner's file closes the HISTORY's t-002
    _, reports, _ = _k14(tmp_path / "a", capsys, dev1_extra=[close_hist])
    by = _by_name(reports)
    assert by["routing-log.jsonl"]["unclosed_tasks"] == []                  # one logical journal: history ++ successor
    assert by["dev1.jsonl"]["unclosed_tasks"] == ["t-003"]
    assert by["dev2.jsonl"]["unclosed_tasks"] == ["t-001@dev2", "t-002@dev2"]    # her own, not closed by the owner's accepted
    # a labelled closes: from the owner's file closes hers, a bare one does not, an unknown label closes nothing
    for notes, left in (("closes:t-001@dev2", ["t-002@dev2"]), ("closes:t-001", ["t-001@dev2", "t-002@dev2"]),
                        ("closes:t-001@ghost", ["t-001@dev2", "t-002@dev2"])):
        carrier = _ev14("dispatch_skipped", "2026-10-02T10:00:00", agent="scout", notes=notes)
        _, reports, _ = _k14(tmp_path / notes.replace(":", "_").replace("@", "_"), capsys, dev1_extra=[close_hist, carrier])
        assert _by_name(reports)["dev2.jsonl"]["unclosed_tasks"] == left, notes


def test_k14_order_dependent_sections_are_per_file(tmp_path, capsys):
    # a ts that goes backwards in dev2's file is HER file's anomaly, not the history's or the owner's
    back = [_dl14("t-001", "2026-10-02T09:00:00"), _dl14("t-002", "2026-10-02T08:50:00")]
    _, reports, _ = _k14(tmp_path, capsys, dev2_lines=back)
    by = _by_name(reports)
    assert len(by["dev2.jsonl"]["ts_anomalies"]) >= 1
    assert by["routing-log.jsonl"]["ts_anomalies"] == [] and by["dev1.jsonl"]["ts_anomalies"] == []
    # the same id issued in both files is not a duplicate delegation: the files are different namespaces
    same = [_dl14("t-003", "2026-10-02T09:00:00")]
    _, reports, _ = _k14(tmp_path / "same", capsys, dev2_lines=same)
    assert all(r["duplicate_delegates"] == [] for r in reports)


def test_k14_text_output_names_the_file_of_each_section_and_summarises(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED), DEV2: _jt14(N_CREATED)}, slug="dev1")
    assert main(["--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "dev1.jsonl" in out and "dev2.jsonl" in out and "routing-log.jsonl" in out
    assert "SUMMARY across all journals" in out


def test_k14_no_journal_under_the_root_exits_2_and_says_where_it_looked(tmp_path, capsys):
    assert main(["--root", str(tmp_path / "empty")]) == 2
    err = capsys.readouterr().err
    assert "no journal under" in err and "logs/routing-log.jsonl" in err and "logs/journal/*.jsonl" in err


def test_k14_an_explicit_journal_still_reads_just_that_file(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV2: _jt14(N_CREATED, _dl14("t-001", "2026-10-02T09:00:00"))}, slug="dev1")
    assert main(["--journal", str(root / DEV2), "--json"]) == 0
    reports = json.loads(capsys.readouterr().out)["journals"]
    assert len(reports) == 1 and reports[0]["journal"].endswith("dev2.jsonl")


def test_k14_a_problem_of_the_loader_is_printed_and_does_not_stop_the_report(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED), DEV2: _jt14(N_CREATED), "logs/journal/Bad Name.jsonl": "x\n"},
                   slug="dev1")
    assert main(["--root", str(root), "--json"]) == 0
    out = capsys.readouterr()
    assert "journal problem:" in out.err and "Bad Name.jsonl" in out.err
    assert len(json.loads(out.out)["journals"]) == 3


# ---------------------------------------------------------------------
# B-426 D10: characterisation of analyze_journal, written BEFORE the split into one helper per
# section. ONE synthetic journal that exercises all ten sections (counts, rule-6 pairing, typed
# fields + legacy, `by`, repeated delegated, ts order, false-accept, rejected distribution,
# degradation pairs, unclosed tasks), read in five configurations: the declaration beside the
# journal, a window, a fixed label + a cross-file object, no declaration, an empty file. The whole
# report of each is compared as json.dumps(sort_keys=True); sort_keys hides the key ORDER, so the
# top-level order is pinned on its own.
# ---------------------------------------------------------------------
_CHAR_KEYS = ["journal", "total_lines", "parsed_lines", "unparsable", "in_window_count", "counts",
              "rule6_candidates", "field_violations", "legacy_events", "by_violations",
              "duplicate_delegates", "ts_anomalies", "false_accept", "rejected_distribution",
              "degradation_pairs", "unclosed_tasks", "closed_by_decomposable"]


def _char_lines():
    """The journal: line numbers matter (the report names lines), so the order here is the contract."""
    a_d = _ek("2026-07-15T10:00:00", "delegated", worker_ref="agent:aaa")            # clone A of t-050 (declared)
    b_d = _ek("2026-07-15T10:01:00", "delegated", worker_ref="agent:bbb")            # clone B of t-050
    b_acc = _ek("2026-07-15T10:02:00", "accepted", by="sonnet")
    lines = [
        ev("2026-07-15T08:00:00", "delegated", agent="scout"),                         # legacy (before the patched cutoff), no fields
        ev("2026-07-15T09:00:00", "journal_created", agent="lead", category="infra", notes="n"),
        a_d, b_d, b_acc,
        _ek("2026-07-15T10:03:00", "delegated", tid="t-051", agent="builder", worker_ref="agent:c1"),
        _ek("2026-07-15T10:04:00", "accepted", tid="t-051", agent="builder"),          # no witness, no by
        _ek("2026-07-15T10:05:00", "delegated", tid="t-051", agent="builder", worker_ref="agent:c2"),   # after accepted
        _ek("2026-07-15T10:06:00", "delegated", tid="t-052", worker_ref="agent:d1"),
        _ek("2026-07-15T10:07:00", "rejected", tid="t-052"),                           # no failure_class, no attempt, no by
        _ek("2026-07-15T10:08:00", "rejected", tid="t-052", attempt=2, failure_class="spec", by="sonnet"),
        _ek("2026-07-15T10:09:00", "delegated", tid="t-052", worker_ref="agent:d2"),   # continuation
        _ek("2026-07-15T10:10:00", "delegated", tid="t-052", agent="critic", worker_ref="agent:d3"),    # critic-entry
        _ek("2026-07-15T10:11:00", "delegated", tid="t-052", attempt=3, worker_ref="agent:d4"),         # retry
        _ek("2026-07-15T10:12:00", "delegated", tid="t-052", worker_ref="agent:d5"),   # other
        _ek("2026-07-15T10:13:00", "delegated", tid="t-053", agent="builder", worker_ref="agent:e1"),
        _ek("2026-07-15T10:14:00", "rejected", tid="t-053", agent="builder", attempt=1, failure_class="capability", by="opus"),
        _ek("2026-07-15T10:15:00", "rejected", tid="t-053", agent="builder", attempt=2, failure_class="capability", by="opus"),
        _ek("2026-07-15T10:16:00", "escalated", tid="t-053", agent="builder"),
        _ek("2026-07-15T10:17:00", "defect_found", tid="t-060", agent="builder", ref="t-051"),
        _ek("2026-07-15T10:18:00", "defect_found", tid="t-061", agent="critic"),         # no ref
        _ek("2026-07-15T10:19:00", "delegated", tid="t-054", worker_ref="agent:f1"),
        ev("2026-07-15T10:20:00", "dispatch_skipped", agent="lead", category="x", notes="closes:t-054 done"),
        _ek("2026-07-15T10:21:00", "delegated", tid="t-056", worker_ref="agent:g1"),
        _ek("2026-07-15T10:22:00", "decomposable", tid="t-056"),
        _ek("2026-07-15T10:23:00", "delegated", tid="t-055", worker_ref="agent:h1"),   # stays unclosed
        ev("2026-07-15T10:24:00", "rejected", category="x", notes="n", task_id="t-070", model="m"),     # no agent key
        ev("2026-07-15T11:00:00", "lead_degraded", agent="lead", category="infra", notes="n"),
        ev("2026-07-15T11:05:00", "lead_degraded", agent="lead", category="infra", notes="n"),
        ev("2026-07-15T11:10:00", "lead_restored", agent="lead", category="infra", notes="n"),
        ev("2026-07-15T11:20:00", "lead_restored", agent="lead", category="infra", notes="n"),
        ev("2026-07-15T11:30:00", "lead_degraded", agent="lead", category="infra", notes="n"),
        ev("2026-07-15T10:30:00", "calibrated", agent="lead", category="infra", notes="n"),     # ts goes back
        {"event": "calibrated", "agent": "lead", "category": "infra", "notes": "n"},           # no ts
        "{not json",
        "[1, 2]",
    ]
    return lines, a_d


class _FakeCross:
    """The CrossFile surface analyze_journal reads: tokens, accepted, escalated_outside(path)."""
    tokens = {("dev1", "t-055")}
    accepted = {("dev1", "t-056")}

    def escalated_outside(self, path):
        return {("dev1", "t-052")}


def _char_reports(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "LEGACY_CUTOFF", "2026-07-15T08:30:00")
    lines, a_d = _char_lines()
    out = {}
    decl = tmp_path / "decl"
    decl.mkdir()
    p = decl / "j.jsonl"
    write_journal(p, lines)
    _declare(decl, None, a_d)
    by_since = parse_ts("2026-07-15T10:03:30")
    out["declared"] = analyze_journal(str(p), None, None, by_since)
    out["window"] = analyze_journal(str(p), parse_ts("2026-07-15T10:05:00"), parse_ts("2026-07-15T11:10:00"), by_since)
    out["fixed_cross"] = analyze_journal(str(p), None, None, by_since, jk.NO_SEGMENTS,
                                         fixed_label="dev1", cross=_FakeCross())
    bare = tmp_path / "bare"
    bare.mkdir()
    q = bare / "j.jsonl"
    write_journal(q, lines)
    out["bare"] = analyze_journal(str(q), None, None, parse_ts("1970-01-01T00:00:00"))
    e = bare / "empty.jsonl"
    e.write_text("", encoding="utf-8")
    out["empty"] = analyze_journal(str(e), None, None, parse_ts("1970-01-01T00:00:00"))
    for rep in out.values():
        rep["journal"] = "J"                                       # the tmp path is the only run-dependent value
    return out


_NOTE_6 = ("candidate; no escalated with this task_id found after the 2nd rejected (by file position). Could be "
           "closed/superseded (the thread continued under a different task_id) -- a human verdict, not something "
           "this script can decide.")
_ERR_JSON = "invalid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
_UNPARSABLE = [{"line": 35, "error": _ERR_JSON, "raw": "{not json"},
               {"line": 36, "error": "not a JSON object (not a dict)", "raw": "[1, 2]"}]
_DEGRADED_OPEN = ("NOT CLOSED by the end of the window/file -- legal if the session is still alive / recorded as "
                  "the last event")
_DUP = [{"line": 8, "task_id": "t-051", "agent": "builder", "attempt": None, "prior_status": "accepted",
         "branch": "candidate-duplicate"},
        {"line": 12, "task_id": "t-052", "agent": "scout", "attempt": None, "prior_status": "rejected",
         "branch": "continuation"},
        {"line": 13, "task_id": "t-052", "agent": "critic", "attempt": None, "prior_status": "delegated",
         "branch": "critic-entry"},
        {"line": 14, "task_id": "t-052", "agent": "scout", "attempt": 3, "prior_status": "delegated",
         "branch": "retry"},
        {"line": 15, "task_id": "t-052", "agent": "scout", "attempt": None, "prior_status": "delegated",
         "branch": "other"}]
_REJ_DIST = [{"failure_class": "<none>", "agent": "<none>", "model": "m", "count": 1},
             {"failure_class": "<none>", "agent": "scout", "model": "haiku", "count": 1},
             {"failure_class": "capability", "agent": "builder", "model": "haiku", "count": 2},
             {"failure_class": "spec", "agent": "scout", "model": "haiku", "count": 1}]
_BY_V = [{"line": 7, "event": "accepted", "task_id": "t-051", "ts": "2026-07-15T10:04:00"},
         {"line": 10, "event": "rejected", "task_id": "t-052", "ts": "2026-07-15T10:07:00"},
         {"line": 27, "event": "rejected", "task_id": "t-070", "ts": "2026-07-15T10:24:00"}]
_FIELDS = [{"line": 7, "event": "accepted", "task_id": "t-051", "missing_fields": ["witness"]},
           {"line": 10, "event": "rejected", "task_id": "t-052", "missing_fields": ["failure_class", "attempt"]},
           {"line": 21, "event": "defect_found", "task_id": "t-061", "missing_fields": ["ref"]},
           {"line": 27, "event": "rejected", "task_id": "t-070",
            "missing_fields": ["agent", "failure_class", "attempt"]}]
# the five configurations differ in a few keys, so the two full reports are written out and the three
# that read the same lines are derived from the first
_GOLDEN_DECLARED = {
    "journal": "J", "total_lines": 36, "parsed_lines": 34, "unparsable": _UNPARSABLE, "in_window_count": 34,
    "counts": {
        "by_event": {"accepted": 2, "calibrated": 2, "decomposable": 1, "defect_found": 2, "delegated": 14,
                     "dispatch_skipped": 1, "escalated": 1, "journal_created": 1, "lead_degraded": 3,
                     "lead_restored": 2, "rejected": 5},
        "by_agent_event": {
            "builder": {"accepted": 1, "defect_found": 1, "delegated": 3, "escalated": 1, "rejected": 2},
            "critic": {"defect_found": 1, "delegated": 1},
            "lead": {"calibrated": 2, "dispatch_skipped": 1, "journal_created": 1, "lead_degraded": 3,
                     "lead_restored": 2},
            "scout": {"accepted": 1, "decomposable": 1, "delegated": 10, "rejected": 2}}},
    "rule6_candidates": [{"task_id": "t-052", "agent": "scout", "rejected_lines": [10, 11], "note": _NOTE_6}],
    "field_violations": _FIELDS,
    "legacy_events": [{"line": 1, "event": "delegated", "task_id": None,
                       "missing_fields": ["category", "notes", "model", "task_id"]}],
    "by_violations": _BY_V,
    "duplicate_delegates": [{"line": 4, "task_id": "t-050", "agent": "scout", "attempt": None,
                             "prior_status": "delegated", "branch": "other"}] + _DUP,
    "ts_anomalies": [{"line": 33, "ts": "2026-07-15T10:30:00", "prev_line": 32, "prev_ts": "2026-07-15T11:30:00"}],
    "false_accept": {"builder": {"defect_found": 1, "accepted": 1, "rate": 1.0},
                     "critic": {"defect_found": 1, "accepted": 0, "rate": None},
                     "scout": {"defect_found": 0, "accepted": 1, "rate": 0.0}},
    "rejected_distribution": _REJ_DIST,
    "degradation_pairs": [
        {"degraded_line": 28, "degraded_ts": "2026-07-15T11:00:00", "restored_line": None, "restored_ts": None,
         "note": "not closed by a following lead_degraded (another degraded before a restored)"},
        {"degraded_line": 29, "degraded_ts": "2026-07-15T11:05:00", "restored_line": 30,
         "restored_ts": "2026-07-15T11:10:00", "note": "closed"},
        {"degraded_line": None, "degraded_ts": None, "restored_line": 31, "restored_ts": "2026-07-15T11:20:00",
         "note": "lead_restored with no preceding lead_degraded in window"},
        {"degraded_line": 32, "degraded_ts": "2026-07-15T11:30:00", "restored_line": None, "restored_ts": None,
         "note": _DEGRADED_OPEN}],
    "unclosed_tasks": ["t-050@codex-fixes", "t-052", "t-055"],
    "closed_by_decomposable": ["t-056"],
}
_GOLDEN_WINDOW = dict(
    _GOLDEN_DECLARED, in_window_count=24,
    counts={"by_event": {"calibrated": 2, "decomposable": 1, "defect_found": 2, "delegated": 10,
                         "dispatch_skipped": 1, "escalated": 1, "lead_degraded": 2, "rejected": 5},
            "by_agent_event": {
                "builder": {"defect_found": 1, "delegated": 2, "escalated": 1, "rejected": 2},
                "critic": {"defect_found": 1, "delegated": 1},
                "lead": {"calibrated": 2, "dispatch_skipped": 1, "lead_degraded": 2},
                "scout": {"decomposable": 1, "delegated": 7, "rejected": 2}}},
    field_violations=_FIELDS[1:], legacy_events=[], by_violations=_BY_V[1:], duplicate_delegates=_DUP,
    ts_anomalies=[{"line": 33, "ts": "2026-07-15T10:30:00", "prev_line": 29, "prev_ts": "2026-07-15T11:05:00"}],
    false_accept={"builder": {"defect_found": 1, "accepted": 0, "rate": None},
                  "critic": {"defect_found": 1, "accepted": 0, "rate": None}},
    degradation_pairs=[
        {"degraded_line": 28, "degraded_ts": "2026-07-15T11:00:00", "restored_line": None, "restored_ts": None,
         "note": "not closed by a following lead_degraded (another degraded before a restored)"},
        {"degraded_line": 29, "degraded_ts": "2026-07-15T11:05:00", "restored_line": None, "restored_ts": None,
         "note": _DEGRADED_OPEN}])
_CHAR_GOLDEN = {
    "declared": _GOLDEN_DECLARED,
    "window": _GOLDEN_WINDOW,
    # no declaration: the foreign t-050 reads as the accepted one
    "bare": dict(_GOLDEN_DECLARED, unclosed_tasks=["t-052", "t-055"]),
    # a fixed label + the cross object: its tokens/accepted close t-055/t-056, its escalated_outside skips t-052
    "fixed_cross": dict(_GOLDEN_DECLARED, rule6_candidates=[], closed_by_decomposable=[],
                        unclosed_tasks=["t-052@dev1", "t-054@dev1"]),
    "empty": {"journal": "J", "total_lines": 0, "parsed_lines": 0, "unparsable": [], "in_window_count": 0,
              "counts": {"by_event": {}, "by_agent_event": {}}, "rule6_candidates": [], "field_violations": [],
              "legacy_events": [], "by_violations": [], "duplicate_delegates": [], "ts_anomalies": [],
              "false_accept": {}, "rejected_distribution": [], "degradation_pairs": [], "unclosed_tasks": [],
              "closed_by_decomposable": []},
}


def test_d10_analyze_journal_whole_report_is_unchanged(tmp_path, monkeypatch):
    reports = _char_reports(tmp_path, monkeypatch)
    assert set(reports) == set(_CHAR_GOLDEN)
    for name, rep in reports.items():
        assert list(rep.keys()) == _CHAR_KEYS, name                       # sort_keys hides the order
        assert list(rep["counts"].keys()) == ["by_event", "by_agent_event"], name
    for name, rep in reports.items():
        assert json.dumps(rep, sort_keys=True) == json.dumps(_CHAR_GOLDEN[name], sort_keys=True), name


# ---------------------------------------------------------------------
# t-667 D2: characterisation of render_text, written BEFORE the eight identical `if items: for ... else: (none)`
# blocks became one helper. Two hand-built reports (not analyze_journal output, so the golden does not move with
# the analysis): one in which EVERY section is non-empty, one in which every section is empty. The expected
# text was recorded from render_text at 79ea49ee, byte for byte.
# ---------------------------------------------------------------------
def _full_report():
    return {
        "journal": "logs/j.jsonl", "total_lines": 40, "parsed_lines": 38, "in_window_count": 30,
        "unparsable": [{"line": 3, "error": "invalid JSON: Expecting value", "raw": "{x"},
                       {"line": 9, "error": "not a JSON object (not a dict)", "raw": "[1]"}],
        "counts": {"by_event": {"delegated": 3, "accepted": 2},
                   "by_agent_event": {"scout": {"delegated": 1, "accepted": 1},
                                      "builder": {"delegated": 2, "accepted": 1}}},
        "rule6_candidates": [{"task_id": "t-001", "agent": "scout", "rejected_lines": [4, 5], "note": "a note"}],
        "field_violations": [{"line": 6, "event": "accepted", "task_id": "t-002", "missing_fields": ["witness"]}],
        "legacy_events": [{"line": 1}, {"line": 2}],
        "by_violations": [{"line": 7, "event": "accepted", "task_id": "t-003", "ts": "2026-07-15T10:00:00"}],
        "duplicate_delegates": [
            {"line": 10, "task_id": "t-004", "agent": "scout", "attempt": None, "prior_status": "accepted",
             "branch": "candidate-duplicate"},
            {"line": 11, "task_id": "t-004", "agent": "scout", "attempt": 3, "prior_status": "escalated",
             "branch": "other"}],
        "ts_anomalies": [{"line": 12, "ts": "2026-07-15T09:00:00", "prev_line": 11, "prev_ts": "2026-07-15T10:00:00"}],
        "false_accept": {"builder": {"defect_found": 1, "accepted": 4, "rate": 0.25},
                         "critic": {"defect_found": 1, "accepted": 0, "rate": None}},
        "rejected_distribution": [{"failure_class": "spec", "agent": "builder", "model": "sonnet", "count": 2},
                                  {"failure_class": "<none>", "agent": "scout", "model": "haiku", "count": 1}],
        "degradation_pairs": [{"degraded_line": 13, "degraded_ts": "2026-07-15T11:00:00", "restored_line": 14,
                               "restored_ts": "2026-07-15T11:10:00", "note": "closed"},
                              {"degraded_line": 15, "degraded_ts": "2026-07-15T11:30:00", "restored_line": None,
                               "restored_ts": None, "note": "NOT CLOSED"}],
        "unclosed_tasks": ["t-001", "t-050@codex"], "closed_by_decomposable": ["t-056", "t-057"],
    }


def _empty_report():
    return {
        "journal": "logs/e.jsonl", "total_lines": 0, "parsed_lines": 0, "in_window_count": 0, "unparsable": [],
        "counts": {"by_event": {}, "by_agent_event": {}}, "rule6_candidates": [], "field_violations": [],
        "legacy_events": [], "by_violations": [], "duplicate_delegates": [], "ts_anomalies": [],
        "false_accept": {}, "rejected_distribution": [], "degradation_pairs": [], "unclosed_tasks": [],
        "closed_by_decomposable": [],
    }


_RENDER_FULL = """# Journal: logs/j.jsonl
Total lines: 40; parsed: 38; in window: 30

=== Unparsable lines (candidate violation) ===

  line 3: invalid JSON: Expecting value
  line 9: not a JSON object (not a dict)

=== Counts by event type ===

  accepted: 2
  delegated: 3

=== Counts by tier x event (agent x event) ===

  builder: accepted=1, delegated=2
  scout: accepted=1, delegated=1

=== Escalation-pairing candidates (a rejected pair with no escalated) ===

  task_id=t-001 agent=scout rejected_lines=[4, 5] -- a note

=== Missing typed fields (candidate violation, post-legacy) ===

  line 6 event=accepted task_id=t-002: missing ['witness']

=== Legacy (ts < 1970-01-01T00:00:00, not violations) ===

  2 event(s) with missing fields, pre-dating the typed-fields schema

=== Missing 'by' (post by-since) ===

  line 7 event=accepted task_id=t-003 ts=2026-07-15T10:00:00

=== Repeated delegated by task_id (branch classification) ===

  line 10 task_id=t-004 agent=scout attempt=None prior_status=accepted -> candidate-duplicate
  line 11 task_id=t-004 agent=scout attempt=3 prior_status=escalated -> other (anomalous repeat outside the canonical branches -- needs a human verdict)

=== ts anomalies (informational, known non-monotonic-clock classes) ===

  line 12 ts=2026-07-15T09:00:00 < line 11 prev_ts=2026-07-15T10:00:00

=== False-accept rate by tier ===

  builder: defect_found=1 / accepted=4 = 0.2500
  critic: defect_found=1 / accepted=0 = n/a (accepted=0)

=== Rejected by failure_class x agent x model ===

  spec / builder / sonnet: 2
  <none> / scout / haiku: 1

=== lead_degraded/lead_restored pairs ===

  degraded(line=13, ts=2026-07-15T11:00:00) -> restored(line=14, ts=2026-07-15T11:10:00): closed
  degraded(line=15, ts=2026-07-15T11:30:00) -> restored(line=None, ts=None): NOT CLOSED

=== Unclosed tasks (last lifecycle event = delegated, no closes: token) ===

  t-001, t-050@codex
  closed: decomposable -- t-056, t-057"""

_RENDER_EMPTY = """# Journal: logs/e.jsonl
Total lines: 0; parsed: 0; in window: 0

=== Unparsable lines (candidate violation) ===

  (none)

=== Counts by event type ===


=== Counts by tier x event (agent x event) ===


=== Escalation-pairing candidates (a rejected pair with no escalated) ===

  (no candidates)

=== Missing typed fields (candidate violation, post-legacy) ===

  (none)

=== Legacy (ts < 1970-01-01T00:00:00, not violations) ===

  0 event(s) with missing fields, pre-dating the typed-fields schema

=== Missing 'by' (post by-since) ===

  (none)

=== Repeated delegated by task_id (branch classification) ===

  (no repeats)

=== ts anomalies (informational, known non-monotonic-clock classes) ===

  (none)

=== False-accept rate by tier ===


=== Rejected by failure_class x agent x model ===

  (no rejected in window)

=== lead_degraded/lead_restored pairs ===

  (no degradation events in window)

=== Unclosed tasks (last lifecycle event = delegated, no closes: token) ===

  (none)"""


def test_d2_render_text_of_a_report_with_every_section_non_empty_is_byte_unchanged():
    assert cc.render_text(_full_report()) == _RENDER_FULL


def test_d2_render_text_of_a_report_with_every_section_empty_is_byte_unchanged():
    assert cc.render_text(_empty_report()) == _RENDER_EMPTY


def test_d2_each_section_keeps_its_own_empty_text_and_its_own_place():
    # one section empty at a time: its "(none)" text appears under ITS title and the other seven are unchanged
    for key, title, empty in (
            ("unparsable", "Unparsable lines (candidate violation)", "  (none)"),
            ("rule6_candidates", "Escalation-pairing candidates (a rejected pair with no escalated)", "  (no candidates)"),
            ("field_violations", "Missing typed fields (candidate violation, post-legacy)", "  (none)"),
            ("by_violations", "Missing 'by' (post by-since)", "  (none)"),
            ("duplicate_delegates", "Repeated delegated by task_id (branch classification)", "  (no repeats)"),
            ("ts_anomalies", "ts anomalies (informational, known non-monotonic-clock classes)", "  (none)"),
            ("rejected_distribution", "Rejected by failure_class x agent x model", "  (no rejected in window)"),
            ("degradation_pairs", "lead_degraded/lead_restored pairs", "  (no degradation events in window)")):
        report = _full_report()
        report[key] = []
        text = cc.render_text(report)
        assert f"=== {title} ===\n\n{empty}\n" in text, key
        assert text.count("(none)") + text.count("(no ") == 1, key


# ---------------------------------------------------------------------
# t-667 D3: characterisation of main(), written BEFORE it was split into _parse_window / _default_reports /
# _print_summary. Exit 2 for each invalid timestamp flag (and which one is named first), for the --journal OSError,
# for the default-mode OSError and for "no journal"; --json; the SUMMARY only with more than one report.
# ---------------------------------------------------------------------
def _run_main(capsys, *argv):
    code = main(list(argv))
    out = capsys.readouterr()
    return code, out.out, out.err


@pytest.mark.parametrize("flag", ["--window-start", "--window-end", "--by-since"])
def test_d3_each_invalid_timestamp_flag_exits_2_and_names_itself(tmp_path, capsys, flag):
    p = tmp_path / "j.jsonl"
    write_journal(p, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    code, out, err = _run_main(capsys, "--journal", str(p), flag, "nope")
    assert (code, out) == (2, "")
    assert err == f"calibration_counts: invalid {flag} 'nope'\n"


def test_d3_the_first_invalid_flag_in_the_order_start_end_by_since_is_the_one_named(tmp_path, capsys):
    p = tmp_path / "j.jsonl"
    write_journal(p, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    both = ("--window-start", "a", "--window-end", "b", "--by-since", "c")
    assert _run_main(capsys, "--journal", str(p), *both)[2] == "calibration_counts: invalid --window-start 'a'\n"
    assert _run_main(capsys, "--journal", str(p), *both[2:])[2] == "calibration_counts: invalid --window-end 'b'\n"
    assert _run_main(capsys, "--journal", str(p), *both[4:])[2] == "calibration_counts: invalid --by-since 'c'\n"


def test_d3_the_parsed_flags_reach_analyze_journal_and_an_empty_window_flag_is_not_given(tmp_path, capsys, monkeypatch):
    p = tmp_path / "j.jsonl"
    write_journal(p, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    calls = []
    monkeypatch.setattr(cc, "analyze_journal", lambda *a, **kw: calls.append((a, kw)) or {"journal": a[0]})
    assert _run_main(capsys, "--journal", str(p), "--json")[0] == 0
    assert calls == [((str(p), None, None, parse_ts(cc.DEFAULT_BY_SINCE)), {})]
    calls.clear()
    code = _run_main(capsys, "--journal", str(p), "--json", "--window-start", "2026-07-09T00:00:00",
                     "--window-end", "2026-07-10T00:00:00", "--by-since", "2026-07-11T12:30:00")[0]
    assert code == 0 and calls == [((str(p), parse_ts("2026-07-09T00:00:00"), parse_ts("2026-07-10T00:00:00"),
                                     parse_ts("2026-07-11T12:30:00")), {})]
    calls.clear()
    assert _run_main(capsys, "--journal", str(p), "--json", "--window-start", "", "--window-end", "")[0] == 0
    assert calls[0][0][1:3] == (None, None)                    # an empty window flag reads as not given ...
    code, out, err = _run_main(capsys, "--journal", str(p), "--by-since", "")
    assert (code, out, err) == (2, "", "calibration_counts: invalid --by-since ''\n")   # ... an empty --by-since does not


def test_d3_a_journal_that_cannot_be_read_exits_2_before_any_output(tmp_path, capsys):
    good, missing = tmp_path / "good.jsonl", tmp_path / "missing.jsonl"
    write_journal(good, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    code, out, err = _run_main(capsys, "--journal", str(good), "--journal", str(missing))
    assert (code, out) == (2, "")                               # the good report is not printed either
    assert err.startswith(f"calibration_counts: failed to read {str(missing)!r}: ") and err.count("\n") == 1


def test_d3_the_default_mode_stops_at_the_first_unreadable_journal_file_naming_it(tmp_path, capsys, monkeypatch):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED), DEV2: _jt14(N_CREATED)}, slug="dev1")
    seen = []

    def fail(path, *a, **kw):
        seen.append(path)
        raise OSError("boom")

    monkeypatch.setattr(cc, "analyze_journal", fail)
    code, out, err = _run_main(capsys, "--root", str(root))
    assert (code, out) == (2, "") and len(seen) == 1
    assert err == f"calibration_counts: failed to read {jk.HISTORY_REL!r}: boom\n"


def test_d3_the_default_mode_without_journal_keys_exits_2_and_says_to_pass_a_journal(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(cc, "_jk", None)
    code, out, err = _run_main(capsys, "--root", str(tmp_path))
    assert (code, out) == (2, "")
    assert err == "calibration_counts: journal_keys is not importable; pass --journal PATH\n"
    p = tmp_path / "j.jsonl"                                    # with --journal the same run is fine
    write_journal(p, [ev("2026-07-08T00:00:00", "journal_created", notes="init")])
    assert _run_main(capsys, "--journal", str(p))[0] == 0


def _two_journals(tmp_path):
    a, b = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    write_journal(a, [ev("2026-07-08T00:00:00", "journal_created", agent="lead", category="infra", notes="init")])
    write_journal(b, [
        ev("2026-07-08T01:00:00", "delegated", agent="scout", model="m", task_id="t-001", category="recon", notes="n"),
        ev("2026-07-08T01:10:00", "rejected", agent="scout", model="m", task_id="t-001", attempt=1,
           failure_class="tooling", category="recon", notes="n"),
        ev("2026-07-08T01:20:00", "rejected", agent="scout", model="m", task_id="t-001", attempt=2,
           failure_class="tooling", category="recon", notes="n"),
        "{not json",
    ])
    return a, b


def test_d3_the_summary_appears_only_with_more_than_one_report_and_after_every_report(tmp_path, capsys):
    a, b = _two_journals(tmp_path)
    by_since = parse_ts(cc.DEFAULT_BY_SINCE)
    reports = [analyze_journal(str(x), None, None, by_since) for x in (a, b)]
    code, out, _ = _run_main(capsys, "--journal", str(a))
    assert code == 0 and "SUMMARY" not in out and out == cc.render_text(reports[0]) + "\n"
    code, out, _ = _run_main(capsys, "--journal", str(a), "--journal", str(b))
    summary = ("\n=== SUMMARY across all journals ===\n\n"
               f"  {a}: rejected=0, rule6_candidates=0, field_violations=0, by_violations=0, "
               "duplicate_delegates=0, ts_anomalies=0, unparsable=0\n"
               f"  {b}: rejected=2, rule6_candidates=1, field_violations=0, by_violations=2, "
               "duplicate_delegates=0, ts_anomalies=0, unparsable=1\n")
    assert code == 0 and out == "".join(cc.render_text(r) + "\n" for r in reports) + summary


def test_d3_json_prints_the_reports_only_never_the_summary(tmp_path, capsys):
    a, b = _two_journals(tmp_path)
    code, out, _ = _run_main(capsys, "--journal", str(a), "--journal", str(b), "--json")
    assert code == 0 and "SUMMARY" not in out
    assert [r["journal"] for r in json.loads(out)["journals"]] == [str(a), str(b)]


# ---------------------------------------------------------------------
# t-852 (F6-3): the default load names the files it read; a dead-worker replacement is its own branch
# ---------------------------------------------------------------------
import journal_validator as jv

_OTHER_NOTE = " (anomalous repeat outside the canonical branches -- needs a human verdict)"


def _rw(ts, ref, notes="n", tid="t-060", agent="builder", **kw):
    """A delegated with a worker_ref and notes; the repeat classifier reads both."""
    return ev(ts, "delegated", agent=agent, model="sonnet", task_id=tid, category="implementation",
              notes=notes, worker_ref=ref, **kw)


def _repeats(tmp_path, lines, *, window_start=None, name="j.jsonl"):
    p = tmp_path / name
    write_journal(p, lines)
    return analyze_journal(str(p), window_start, None, parse_ts(cc.DEFAULT_BY_SINCE))["duplicate_delegates"]


def _branch_and_reason(entry):
    return entry["branch"], entry.get("reason")


def test_t852_default_load_counts_every_file_and_the_header_names_each_with_its_events(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED, _dl14("t-003", "2026-10-02T08:30:00")),
                                    DEV2: _jt14(N_CREATED, _dl14("t-001", "2026-10-02T09:00:00"),
                                                   _dl14("t-002", "2026-10-02T09:10:00"))}, slug="dev1")
    code, out, _ = _run_main(capsys, "--root", str(root))
    assert code == 0
    head, rest = out.split("# Journal: ", 1)
    assert head.splitlines()[0] == "# Journals loaded: 3 file(s)"
    counts = {line.split(": ", 1)[0].strip().replace("\\", "/").rsplit("/", 1)[-1]: line.split(": ", 1)[1]
              for line in head.splitlines()[1:]}
    assert counts == {"routing-log.jsonl": "3 events (3 in window)", "dev1.jsonl": "2 events (2 in window)",
                      "dev2.jsonl": "3 events (3 in window)"}
    # the events of both developer files are counted: one report each, in the same run
    _, reports, _ = _k14(tmp_path / "json", capsys)
    assert sorted(r["parsed_lines"] for r in reports) == [2, 3, 3]


def test_t852_an_explicit_journal_overrides_the_load_reads_only_that_file_and_prints_no_header(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED), DEV2: _jt14(N_CREATED, _dl14("t-001", "2026-10-02T09:00:00"))},
                   slug="dev1")
    code, out, _ = _run_main(capsys, "--root", str(root), "--journal", str(root / DEV2))
    assert code == 0 and "Journals loaded" not in out and out.count("# Journal: ") == 1
    assert out.startswith(f"# Journal: {root / DEV2}")
    code, out, _ = _run_main(capsys, "--root", str(root), "--json")                   # --json: the reports only, no header
    assert code == 0 and "Journals loaded" not in out and len(json.loads(out)["journals"]) == 3


def test_t852_an_empty_and_a_malformed_developer_journal_are_listed_never_dropped(tmp_path, capsys):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED), DEV2: "", "logs/journal/olga.jsonl": "{not json\n"},
                   slug="dev1")
    code, out, err = _run_main(capsys, "--root", str(root))
    assert code == 0
    head = out.split("# Journal: ", 1)[0]
    assert "# Journals loaded: 4 file(s)" in head
    assert "dev2.jsonl: 0 events (0 in window)" in head                              # empty: listed with zero events
    assert "olga.jsonl: 0 events (0 in window, 1 unparsable)" in head                   # malformed line: counted aside
    assert "invalid JSON" in out                                                         # ... and reported in its own section


def test_t852_the_default_load_without_journal_keys_refuses_and_prints_nothing(tmp_path, capsys, monkeypatch):
    root = _root14(tmp_path, files={DEV1: _jt14(M_CREATED)}, slug="dev1")
    monkeypatch.setattr(cc, "_jk", None)
    code, out, err = _run_main(capsys, "--root", str(root))
    assert (code, out) == (2, "") and err == "calibration_counts: journal_keys is not importable; pass --journal PATH\n"


def test_t852_existing_sections_are_unchanged_for_a_journal_without_the_marker(tmp_path, capsys):
    lines = [_rw("2026-07-08T00:00:00", "agent:a"),
             ev("2026-07-08T00:10:00", "accepted", agent="builder", model="sonnet", task_id="t-060",
                category="implementation", notes="n", witness="ok"),
             _rw("2026-07-08T00:20:00", "agent:b"),                                      # duplicate after accepted
             ev("2026-07-08T00:30:00", "delegated", agent="critic", model="opus", task_id="t-060", category="review", notes="n"),
             _rw("2026-07-08T00:40:00", "agent:c", tid="t-061"),
             _rw("2026-07-08T00:50:00", "agent:d", tid="t-061")]                          # "other"
    dups = _repeats(tmp_path, lines)
    assert [d["branch"] for d in dups] == ["candidate-duplicate", "critic-entry", "other"]
    assert all(set(d) == {"line", "task_id", "agent", "attempt", "prior_status", "branch"} for d in dups)   # no new keys
    p = tmp_path / "j.jsonl"
    code, out, _ = _run_main(capsys, "--journal", str(p))
    assert code == 0 and "replacement" not in out and "Journals loaded" not in out
    assert ("  line 6 task_id=t-061 agent=builder attempt=None prior_status=delegated -> other" + _OTHER_NOTE) in out


def test_t852_a_replacement_with_a_matching_ref_is_its_own_branch_and_its_own_count_line(tmp_path, capsys):
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:dead"),
                               _rw("2026-07-08T01:00:00", "agent:new", notes="replaces_worker:agent:dead (it died)")])
    assert len(dups) == 1 and _branch_and_reason(dups[0]) == ("replacement", None) and dups[0]["replaces_worker"] == "agent:dead"
    code, out, _ = _run_main(capsys, "--journal", str(tmp_path / "j.jsonl"))
    assert "-> replacement (dead worker)\n" in out and "anomalous" not in out.split("=== Repeated")[1].split("===")[0].replace(
        "not anomalous", "")
    assert "  replacement (dead worker): 1 (legitimate" in out


def test_t852_a_chain_of_replacements_matches_each_ref_against_the_earlier_lines(tmp_path):
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:a"),
                               _rw("2026-07-08T01:00:00", "agent:b", notes="replaces_worker:agent:a"),
                               _rw("2026-07-08T02:00:00", "agent:c", notes="replaces_worker:agent:b")])
    assert [d["branch"] for d in dups] == ["replacement", "replacement"]


def test_t852_a_ref_that_matches_no_earlier_line_stays_anomalous_with_its_reason(tmp_path, capsys):
    lines = [_rw("2026-07-08T00:00:00", "agent:dead"),
             _rw("2026-07-08T01:00:00", "agent:new", notes="replaces_worker:agent:nobody"),
             _rw("2026-07-08T02:00:00", "agent:late", notes="replaces_worker:agent:later"),     # a ref from a LATER line
             _rw("2026-07-08T03:00:00", "agent:later")]
    dups = _repeats(tmp_path, lines)
    assert [_branch_and_reason(d) for d in dups[:2]] == [("other", "replaces_worker ref not found")] * 2
    code, out, _ = _run_main(capsys, "--journal", str(tmp_path / "j.jsonl"))
    assert "-> other (anomalous repeat outside the canonical branches -- needs a human verdict: replaces_worker ref not found)" in out
    assert "replacement (dead worker):" not in out                                       # no replacement, no count line


def test_t852_a_ref_of_another_task_does_not_match(tmp_path):
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:other-task", tid="t-070"),
                               _rw("2026-07-08T00:30:00", "agent:dead"),
                               _rw("2026-07-08T01:00:00", "agent:new", notes="replaces_worker:agent:other-task")])
    assert _branch_and_reason(dups[0]) == ("other", "replaces_worker ref not found")


@pytest.mark.parametrize("notes", ["replaces_worker:agent:dead.", "replaces_worker:agent:dead,", "replaces_worker:agent:dead)",
                                   "replaces_worker: agent:dead", "replaces_worker:"])
def test_t852_the_token_is_the_validators_first_non_whitespace_run_so_punctuation_or_a_gap_does_not_match(tmp_path, notes):
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:dead"), _rw("2026-07-08T01:00:00", "agent:new", notes=notes)])
    assert dups[0]["branch"] == "other"
    # the same tokenizer the validator uses, not a copy of it
    assert cc._replaces_ref("x replaces_worker:agent:dead. y") == jv.extract_replaces_worker("x replaces_worker:agent:dead. y")


def test_t852_a_grown_attempt_on_a_replacement_is_said_in_the_line_and_still_a_replacement(tmp_path, capsys):
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:dead"),
                               _rw("2026-07-08T01:00:00", "agent:new", notes="replaces_worker:agent:dead", attempt=2)])
    assert dups[0]["branch"] == "replacement" and dups[0]["attempt"] == 2
    code, out, _ = _run_main(capsys, "--journal", str(tmp_path / "j.jsonl"))
    assert "-> replacement (dead worker) -- attempt grew on a replacement, it should not" in out


def test_t852_a_critic_entry_a_retry_and_a_continuation_are_classified_as_before(tmp_path):
    base = [_rw("2026-07-08T00:00:00", "agent:a"),
            ev("2026-07-08T00:10:00", "rejected", agent="builder", model="sonnet", task_id="t-060", attempt=1,
               failure_class="spec", category="implementation", notes="n")]
    assert _branch_and_reason(_repeats(tmp_path, base + [_rw("2026-07-08T00:20:00", "agent:b")])[0]) == ("continuation", None)
    esc = ev("2026-07-08T00:15:00", "escalated", agent="builder", model="sonnet", task_id="t-060", category="implementation", notes="n")
    assert _repeats(tmp_path, base + [esc, _rw("2026-07-08T00:20:00", "agent:b", attempt=2)])[0]["branch"] == "retry"
    crit = ev("2026-07-08T00:20:00", "delegated", agent="critic", model="opus", task_id="t-060", category="review",
              notes="n", worker_ref="agent:c")
    assert _repeats(tmp_path, base + [crit])[0]["branch"] == "critic-entry"
    # a candidate-duplicate with a marker that matches nothing stays a candidate-duplicate (no reason: it is not "other")
    acc = ev("2026-07-08T00:15:00", "accepted", agent="builder", model="sonnet", task_id="t-060", category="implementation",
             notes="n", witness="ok")
    dup = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:a"), acc,
                              _rw("2026-07-08T00:20:00", "agent:b", notes="replaces_worker:agent:ghost")])
    assert _branch_and_reason(dup[0]) == ("candidate-duplicate", None)


def test_t852_a_window_that_cuts_between_the_original_and_the_replacement_still_finds_the_original(tmp_path):
    lines = [_rw("2026-07-08T00:00:00", "agent:dead"),
             _rw("2026-07-09T00:00:00", "agent:new", notes="replaces_worker:agent:dead")]
    dups = _repeats(tmp_path, lines, window_start=parse_ts("2026-07-08T12:00:00"))      # the original is OUTSIDE the window
    assert len(dups) == 1 and dups[0]["branch"] == "replacement"


def _two_file_root(tmp_path, dev1_lines, dev2_lines):
    return _root14(tmp_path, files={DEV1: _jt14(M_CREATED, *dev1_lines), DEV2: _jt14(N_CREATED, *dev2_lines)},
                   slug="dev1")


def _reports_by_name(root, capsys):
    assert main(["--root", str(root), "--json"]) == 0
    return _by_name(json.loads(capsys.readouterr().out)["journals"])


def test_t852_an_original_in_the_history_is_matched_across_files_by_key(tmp_path, capsys):
    # H3 = delegated t-002 agent:t-002-10:00:00 in the HISTORY; the owner's file (the history's successor, the same key)
    # holds a plain delegated and then the replacement of the HISTORY's worker
    root = _two_file_root(tmp_path, [_dl14("t-002", "2026-10-02T09:00:00"),
                                     _dl14("t-002", "2026-10-02T09:30:00", notes="replaces_worker:agent:t-002-10:00:00")], [])
    got = _reports_by_name(root, capsys)["dev1.jsonl"]["duplicate_delegates"]
    assert [_branch_and_reason(d) for d in got] == [("replacement", None)]


def test_t852_a_ref_written_later_in_another_file_is_not_an_earlier_line(tmp_path, capsys):
    root = _two_file_root(tmp_path, [_dl14("t-003", "2026-10-02T09:00:00"),
                                     _dl14("t-003", "2026-10-02T09:30:00", notes="replaces_worker:agent:t-003-11:00:00")], [])
    (root / "logs/routing-log.jsonl").write_text(
        (root / "logs/routing-log.jsonl").read_text(encoding="utf-8") + _jt14(_dl14("t-003", "2026-10-02T11:00:00")), encoding="utf-8")
    got = _reports_by_name(root, capsys)["dev1.jsonl"]["duplicate_delegates"]
    assert [_branch_and_reason(d) for d in got] == [("other", "replaces_worker ref not found")]


def test_t852_the_same_task_id_in_two_journals_is_two_keys_so_a_ref_of_the_other_one_does_not_match(tmp_path, capsys):
    # dev2's t-001 (key t-001@dev2) and the owner's t-001 (key "") are different tasks
    root = _two_file_root(tmp_path, [_dl14("t-001", "2026-10-02T09:00:00"),
                                     _dl14("t-001", "2026-10-02T09:30:00", notes="replaces_worker:agent:t-001-09:00:00")],
                          [_dl14("t-001", "2026-10-02T08:50:00")])
    by = _reports_by_name(root, capsys)
    assert [d["branch"] for d in by["dev1.jsonl"]["duplicate_delegates"]] == ["replacement"]       # her own earlier line: found
    assert by["dev2.jsonl"]["duplicate_delegates"] == []                                            # no cross-file repeat
    root2 = _two_file_root(tmp_path / "x", [_dl14("t-001", "2026-10-02T09:00:00"),
                                            _dl14("t-001", "2026-10-02T09:30:00", notes="replaces_worker:agent:t-001-08:50:00")],
                           [_dl14("t-001", "2026-10-02T08:50:00")])
    got = _reports_by_name(root2, capsys)["dev1.jsonl"]["duplicate_delegates"]
    assert [_branch_and_reason(d) for d in got] == [("other", "replaces_worker ref not found")]       # the ref is dev2's


def test_t852_without_journal_validator_the_marker_is_not_read_and_the_reading_is_the_old_one(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "_jv", None)
    dups = _repeats(tmp_path, [_rw("2026-07-08T00:00:00", "agent:dead"),
                               _rw("2026-07-08T01:00:00", "agent:new", notes="replaces_worker:agent:dead")])
    assert _branch_and_reason(dups[0]) == ("other", None) and "replaces_worker" not in dups[0]
