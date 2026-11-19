"""Tests for tools/journal_validator.py. Style mirrors
tools/test_mechanism_gate.py: decide() is a pure function, tested
directly with synthetic staged/head text -- no git needed for most
cases. One integration test at the bottom exercises the real git
wiring (is_journal_staged / get_staged_text / get_head_text) against a
real tmp_path git repo, and one exercises main()'s exit-2 crash path.

Run from the repo root: python -m pytest tools/test_journal_validator.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import pytest
from pathlib import Path

# TEMPORAL (B-401/B-402): until the Lead places the proposed module on the live path, the code
# under test is tools/journal_validator.proposed.py (loaded by path, the same `_load` as
# test_journal_validator_merge.py); once that file is gone, the live module is imported. Both
# worlds must pass.
_PROPOSED = Path(__file__).resolve().parent / "journal_validator.proposed.py"


def _load():
    if _PROPOSED.exists():
        spec = importlib.util.spec_from_file_location("journal_validator_proposed", _PROPOSED)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    import journal_validator
    return journal_validator


jv = _load()

NOW = jv.datetime.datetime(2026, 7, 10, 12, 0, 0)


def _line(event="delegated", ts="2026-07-10T08:00:00", agent="builder",
          category="implementation", notes="note",
          worker_ref="cli:2026-07-10T08:00:00", **kw) -> str:
    obj = {"ts": ts, "event": event, "agent": agent, "category": category, "notes": notes,
           "worker_ref": worker_ref}
    obj.update(kw)
    return json.dumps(obj, ensure_ascii=False)


HEAD_LINE = _line(event="delegated", task_id="t-001", model="sonnet", ts="2026-07-10T08:00:00")
HEAD_TEXT = HEAD_LINE + "\n"


def _staged(*new_lines: str) -> str:
    return HEAD_TEXT + "".join(l + "\n" for l in new_lines)


def _decide(*args, **kw):
    """jv.decide on TODAY's config unless a test names its own: no test reads the live delegation.config.yaml of the
    tree it runs in (critic t-946 B-1: lead flips to opus at stream L, and the verdicts must not follow it)."""
    kw.setdefault("config_text", CFG_TODAY)
    return jv.decide(*args, **kw)


# ---- not staged at all -> main() must exit 0 silently (tested separately below) ----

# ---- positive case: valid new lines pass clean ----

def test_positive_case_valid_new_lines_pass(tmp_path):
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-002", model="sonnet",
              notes="delegating t-002"),
        _line(event="accepted", ts="2026-07-10T08:20:00", agent="builder", task_id="t-002",
              model="sonnet", witness="pytest ... 1 passed", by="opus",
              notes="accepted t-002"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0
    assert violations == []


# ---- 1. append-only ----

def test_append_only_violation_when_existing_line_modified():
    tampered_head = json.loads(HEAD_LINE)
    tampered_head["notes"] = "rewritten"
    staged = json.dumps(tampered_head, ensure_ascii=False) + "\n"
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("append-only" in v for v in violations)


def test_append_only_violation_when_lines_removed():
    code, violations = _decide("", HEAD_TEXT, NOW)
    assert code == 1
    assert any("append-only" in v for v in violations)


# ---- 2. required fields ----

def test_missing_required_field_notes_fails():
    obj = json.loads(_line(event="dispatch_skipped", ts="2026-07-10T08:10:00",
                            agent="scout", category="recon", notes="x"))
    del obj["notes"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("notes" in v for v in violations)


def test_invalid_json_line_fails():
    staged = HEAD_TEXT + "{not valid json\n"
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("invalid JSON" in v for v in violations)


# ---- 3. event enum ----

def test_unknown_event_fails():
    staged = _staged(_line(event="reticulated", ts="2026-07-10T08:10:00", agent="lead",
                            category="x", notes="x"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("enum" in v for v in violations)


# B-454 item 2: a list/dict in event, task_id or by is a NAMED violation (exit 1), never an
# unhashable TypeError reaching the main() boundary
_UNHASHABLE_OWN = [
    ("event-list", dict(event=["x"], task_id="t-002", model="sonnet"), "'event' is missing/invalid"),
    ("task-id-dict", dict(event="delegated", task_id={"a": 1}, model="sonnet"), "'task_id' is required"),
    ("by-list", dict(event="accepted", task_id="t-001", model="sonnet", by=["opus"],
                     witness="pytest ... 1 passed"), "'by' is required"),
]


@pytest.mark.parametrize("name,kw,named", _UNHASHABLE_OWN, ids=[a for a, _b, _c in _UNHASHABLE_OWN])
def test_unhashable_form_field_is_a_named_violation_not_a_traceback(name, kw, named):
    staged = _staged(_line(ts="2026-07-10T08:10:00", **kw))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert len(violations) == 1 and named in violations[0], violations
    code2, violations2, _w = jv.decide_with_warnings(staged, HEAD_TEXT, NOW)
    assert code2 == 1 and violations2 == violations


# ---- 4. model required ----

def test_model_missing_for_delegated_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-002",
                            notes="no model"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'model'" in v for v in violations)


# ---- 5. task_id required + format ----

def test_task_id_missing_for_delegated_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            notes="no task_id"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'task_id'" in v for v in violations)


def test_task_id_bad_format_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-2", notes="bad format"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("t-NNN format" in v for v in violations)


# ---- 5b. worker_ref required for delegated ----

def test_delegated_missing_worker_ref_fails():
    obj = json.loads(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="no worker_ref"))
    del obj["worker_ref"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_empty_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="", notes="empty worker_ref"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_whitespace_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="   ", notes="whitespace worker_ref"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_nonstring_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref=123, notes="nonstring worker_ref"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_valid_worker_ref_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="cli:2026-07-10T08:10:00",
                            notes="valid worker_ref"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_escalated_needs_no_worker_ref():
    obj = json.loads(_line(event="escalated", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", notes="escalated, no worker_ref"))
    del obj["worker_ref"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 6. rejected: attempt / failure_class ----

def test_rejected_invalid_attempt_and_failure_class_fail():
    staged = _staged(_line(event="rejected", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", attempt=0,
                            failure_class="mystery", by="opus", notes="bad rejected"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'attempt'" in v for v in violations)
    assert any("'failure_class'" in v for v in violations)


# ---- 7. accepted + agent=builder: witness ----

def test_accepted_builder_missing_witness_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", by="opus",
                            notes="no witness"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'witness'" in v for v in violations)


# ---- 8. defect_found: ref ----

def test_defect_found_missing_ref_fails():
    staged = _staged(_line(event="defect_found", ts="2026-07-10T08:10:00", agent="builder",
                            task_id="t-001", notes="late defect"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'ref'" in v for v in violations)


# ---- 9. task_id novelty / reference ----

def test_delegated_novelty_violation_jump_beyond_the_cap():
    # REWRITTEN (offload B0, rule 9a''): "t-005 after t-001" used to be the max+1 violation; a gap is legal now, a
    # jump of more than ID_JUMP_MAX above the max is the refusal
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-1500", notes="skipped far ahead"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("task_id novelty" in v and "jumps more than 1000" in v for v in violations)
    assert any("python -B tools/journal_write.py next" in v and "band" not in v for v in violations)


def test_delegated_novelty_a_gap_of_a_few_is_legal():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-005", notes="a reserved id, gap"))
    assert _decide(staged, HEAD_TEXT, NOW) == (0, [])


def test_delegated_novelty_correct_max_plus_one_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="correct next id"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_accepted_references_nonexistent_task_id_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-099", witness="w", by="opus",
                            notes="dangling ref"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("does not reference" in v for v in violations)


def test_accepted_can_reference_task_id_delegated_earlier_in_same_commit():
    # t-002 delegated and then accepted in the SAME staged batch -- rule 9
    # allows referencing task_ids introduced earlier in this very commit,
    # not only ones already in HEAD.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet", task_id="t-002",
              notes="new task"),
        _line(event="accepted", ts="2026-07-10T08:20:00", agent="builder", model="sonnet",
              task_id="t-002", witness="w", by="opus", notes="accept same-commit task"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 9 (Lead correction, live precedent): re-delegated task_id --
# a/b/v legal, two g negatives (a real duplicate-delegation defect once
# found in a production journal; delegated after accepted) ----

def test_9a_new_task_max_plus_one_passes():
    # (a) restated for clarity alongside b/v/g below: a brand-new task_id
    # equal to max+1 is legal regardless of any b/v/g machinery.
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="new task, case a"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9b_continuation_dispatch_different_agent_passes():
    # (b) t-001 delegated to builder in HEAD; task is still open (no
    # accepted yet); a NEW delegated on the SAME task_id but a DIFFERENT
    # agent (critic acceptance-gate entry) is legal with no attempt/
    # rejected needed -- exactly the pattern a real critic-gate
    # continuation dispatch needs (builder then critic).
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001",
                            notes="critic-gate continuation dispatch, case b"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9v_retry_after_rejected_with_attempt_passes():
    # (v) t-001 rejected, then re-delegated to the SAME agent (builder)
    # WITH attempt>=2 -- legal retry.
    staged = _staged(
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="opus", notes="first attempt rejected"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, notes="retry after rejection, case v"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9g_duplicate_pattern_same_agent_no_attempt_no_rejected_fails():
    # (g) negative #1: an actual defect once found in a production
    # journal -- same agent re-delegated
    # on an open task_id, no attempt field, no rejected above. Must FAIL.
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", notes="duplicate delegation, no attempt/rejected"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("forbidden duplicate" in v for v in violations)


# ---- 9c2. dead-worker replacement (replaces_worker marker) ----


def test_9c2_replaces_worker_matching_prior_ref_passes():
    # t-001 delegated to builder in HEAD with worker_ref
    # "cli:2026-07-10T08:00:00" (see HEAD_LINE's default worker_ref).
    # A NEW delegated by the SAME agent, no attempt, no rejected above
    # -- but notes carry a replaces_worker marker whose handle matches
    # that exact worker_ref -- legal (a dead-worker replacement, not a
    # rule-6 retry).
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", worker_ref="cli:2026-07-10T08:10:00",
              notes="replaces_worker:cli:2026-07-10T08:00:00 (worker died, no verdict)")
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9c2_replaces_worker_fabricated_handle_fails():
    # The claimed handle does not match ANY earlier delegated
    # worker_ref for this task_id -- a fabricated replacement, FAIL.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", worker_ref="cli:2026-07-10T08:10:00",
              notes="replaces_worker:cli:2026-07-10T07:00:00 (never happened)")
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("fabricated replacement" in v for v in violations)


def test_9c2_replaces_worker_matches_ref_from_a_different_agents_delegated_line():
    # Rule 9(c2) searches worker_ref across delegated lines of ANY
    # agent for this task_id, not only lines by the same agent as the
    # new one: a critic-entry's worker_ref can legitimately be claimed
    # as replaced by a later builder retry.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="critic", model="opus",
              task_id="t-001", worker_ref="agent:critic-1",
              notes="critic-gate continuation dispatch, case b"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", worker_ref="agent:critic-2",
              notes="replaces_worker:agent:critic-1 (critic-1 died mid-review)"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9c2_replaces_worker_handle_from_unrelated_task_id_does_not_count():
    # A handle that is a real worker_ref, but for a DIFFERENT task_id,
    # must not satisfy rule 9(c2) for this one -- the prior-refs set
    # is scoped per task_id.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet", task_id="t-002",
              worker_ref="cli:2026-07-10T08:10:00", notes="unrelated task"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="builder", model="sonnet",
              task_id="t-001", worker_ref="cli:2026-07-10T08:20:00",
              notes="replaces_worker:cli:2026-07-10T08:10:00 (wrong task's ref)"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("fabricated replacement" in v for v in violations)


def test_9c2_replaces_worker_does_not_require_attempt_field():
    # rule 9(c2) explicitly does not require attempt to grow -- a bare
    # replaces_worker marker with no attempt field at all is legal.
    obj = json.loads(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", worker_ref="cli:2026-07-10T08:10:00",
              notes="replaces_worker:cli:2026-07-10T08:00:00")
    )
    assert "attempt" not in obj
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9c2_replaces_worker_takes_priority_over_plain_duplicate_fail():
    # Sanity: without the marker, the same shape of line fails as a
    # plain duplicate (case d) -- proves the c2 test above is actually
    # exercising the marker branch, not some other path to a pass.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", notes="no replaces_worker marker here at all")
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("forbidden duplicate" in v for v in violations)


def test_9g_delegated_after_accepted_fails_reopen_forbidden():
    # (g) negative #2: task_id already closed (accepted above) -- a new
    # delegated on it is a forbidden reopen (treated as two tasks),
    # regardless of which agent issues it.
    head_with_accept = HEAD_TEXT + _line(
        event="accepted", ts="2026-07-10T08:05:00", agent="builder", model="sonnet",
        task_id="t-001", witness="pytest ok", by="opus", notes="t-001 already accepted",
    ) + "\n"
    staged = head_with_accept + _line(event="delegated", ts="2026-07-10T08:10:00", agent="critic",
                                       model="opus", task_id="t-001", notes="reopen attempt") + "\n"
    code, violations = _decide(staged, head_with_accept, NOW)
    assert code == 1
    assert any("CLOSED task" in v and "reopening" in v for v in violations)


# ---- 10. ts monotonicity / no narrative future ----

def test_ts_not_monotonic_relative_to_previous_new_line_fails():
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:20:00", model="sonnet", task_id="t-002",
              notes="later"),
        _line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet", task_id="t-003",
              notes="earlier than previous new line"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("not monotonic" in v for v in violations)


def test_ts_earlier_than_last_head_line_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T07:00:00", model="sonnet",
                            task_id="t-002", notes="before HEAD's last ts"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("not monotonic" in v for v in violations)


def test_ts_narrative_future_beyond_now_plus_10min_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-11T00:00:00", model="sonnet",
                            task_id="t-002", notes="far future (narrative-future timestamp)"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("later than now+10min" in v and "narrated" in v for v in violations)


def test_ts_within_10min_future_grace_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T12:05:00", model="sonnet",
                            task_id="t-002", notes="clock skew grace"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 11. role-vs-tier acceptance matrix: every `accepted` cell is a row of MATRIX_ROWS below (the per-cell tests were
# folded into it, critic t-946 N-B1); what is left here is no cell of it ----

def test_matrix_rejected_only_needs_by_present_no_tier_check():
    # literal reading of the spec: tier/basis check text only names
    # "accepted"; rejected carries 'by' without a further tier/basis gate.
    staged = _staged(_line(event="rejected", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", attempt=1, failure_class="recon",
                            by="haiku", notes="rejected, same-tier by, no basis"))
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- the acceptance matrix by FUNCTION RANK (spec 20261116-architect-tier 3.1, 3.4; stream B items B1, B2): ONE table, one
# row per cell. Config TODAY = lead on Fable (the transitional world: every verdict equals the old one); config AFTER =
# lead on Opus + an architect rung on Fable (stream L's flip); cfg None = no config file -> DEFAULT_BINDINGS. ----

def _cfg(lead, architect=None):
    roles = {"lead": lead, "critic": "claude-opus-5-5", "builder": "claude-sonnet-5-5", "scout": "claude-sonnet-5-5"}
    if architect:
        roles["architect"] = architect
    return "roles:\n" + "".join(f"  {fn}:\n    subscription:\n      model: {model}\n" for fn, model in roles.items())


CFG_TODAY = _cfg("claude-fable-5-1")
CFG_AFTER = _cfg("claude-opus-5-5", "claude-fable-5-1")
CFG_AFTER_NO_ARCHITECT = _cfg("claude-opus-5-5")
GENERIC = "by is not strictly above the executor's rank"
FLOOR = "a tier below sonnet"
JUDGE = 'basis "judge" is not legal here'
UNKNOWN_BY = "is not a known tier"


def _row(rid, cfg, agent, by, basis=None, expect=None, category=None):
    return pytest.param(cfg, agent, by, basis, category, expect, id=rid)


MATRIX_ROWS = [
    # every cell of 3.1 on config AFTER (acceptor columns: haiku / sonnet / opus / fable)
    _row("after-scout-haiku", CFG_AFTER, "scout", "haiku", None, FLOOR),
    _row("after-scout-sonnet", CFG_AFTER, "scout", "sonnet"),
    _row("after-scout-opus", CFG_AFTER, "scout", "opus"),
    _row("after-scout-fable", CFG_AFTER, "scout", "fable"),
    _row("after-builder-haiku-critic", CFG_AFTER, "builder", "haiku", "critic", FLOOR),
    _row("after-builder-sonnet-bare", CFG_AFTER, "builder", "sonnet", None, GENERIC),
    _row("after-builder-sonnet-critic", CFG_AFTER, "builder", "sonnet", "critic"),
    _row("after-builder-sonnet-queued", CFG_AFTER, "builder", "sonnet", "queued-to-lead", "queued-to-lead"),
    _row("after-builder-opus-waiver", CFG_AFTER, "builder", "opus"),
    _row("after-builder-fable", CFG_AFTER, "builder", "fable"),
    _row("after-critic-haiku-queued", CFG_AFTER, "critic", "haiku", "queued-to-lead", FLOOR),
    _row("after-critic-sonnet-bare", CFG_AFTER, "critic", "sonnet", None, GENERIC),
    _row("after-critic-sonnet-queued", CFG_AFTER, "critic", "sonnet", "queued-to-lead"),
    _row("after-critic-sonnet-critic-basis", CFG_AFTER, "critic", "sonnet", "critic", "basis='critic'"),
    _row("after-critic-opus-lead-accepts", CFG_AFTER, "critic", "opus"),
    _row("after-critic-opus-queued-to-itself", CFG_AFTER, "critic", "opus", "queued-to-lead"),
    _row("after-critic-fable", CFG_AFTER, "critic", "fable"),
    _row("after-designer-haiku", CFG_AFTER, "designer", "haiku", None, FLOOR),
    _row("after-designer-sonnet-bare", CFG_AFTER, "designer", "sonnet", None, GENERIC),
    _row("after-designer-sonnet-queued", CFG_AFTER, "designer", "sonnet", "queued-to-lead"),
    _row("after-designer-sonnet-critic-basis", CFG_AFTER, "designer", "sonnet", "critic", "basis='critic'"),
    _row("after-designer-opus-lead-accepts", CFG_AFTER, "designer", "opus"),
    _row("after-designer-fable", CFG_AFTER, "designer", "fable"),
    _row("after-lead-no-matrix", CFG_AFTER, "lead", "haiku"),
    _row("after-architect-no-matrix", CFG_AFTER, "architect", "haiku"),
    _row("after-unknown-agent-no-matrix", CFG_AFTER, "analyst", "haiku"),
    # F22: a model ranked above a binding stands in -- never refused; no architect key: fable still outranks lead=opus
    _row("after-no-architect-key-fable-critic", CFG_AFTER_NO_ARCHITECT, "critic", "fable"),
    _row("after-no-architect-key-opus-critic", CFG_AFTER_NO_ARCHITECT, "critic", "opus"),
    # the six transitional pairs of 3.4 on config TODAY: each equals today's verdict
    _row("today-critic-opus-bare", CFG_TODAY, "critic", "opus", None, GENERIC),
    _row("today-critic-opus-queued", CFG_TODAY, "critic", "opus", "queued-to-lead"),
    _row("today-critic-fable", CFG_TODAY, "critic", "fable"),
    _row("today-builder-sonnet-critic", CFG_TODAY, "builder", "sonnet", "critic"),
    _row("today-scout-haiku-critic", CFG_TODAY, "scout", "haiku", "critic", FLOOR),
    _row("today-builder-opus", CFG_TODAY, "builder", "opus"),
    _row("today-designer-opus-bare", CFG_TODAY, "designer", "opus", None, GENERIC),
    _row("today-designer-opus-critic-basis", CFG_TODAY, "designer", "opus", "critic", "basis='critic'"),
    _row("today-designer-opus-queued", CFG_TODAY, "designer", "opus", "queued-to-lead"),
    _row("today-critic-sonnet-queued", CFG_TODAY, "critic", "sonnet", "queued-to-lead"),
    _row("today-builder-sonnet-queued", CFG_TODAY, "builder", "sonnet", "queued-to-lead", "queued-to-lead"),
    # no config file at the root -> DEFAULT_BINDINGS = today's ranks
    _row("default-critic-opus-bare", None, "critic", "opus", None, GENERIC),
    _row("default-critic-fable", None, "critic", "fable"),
    # B2 (FG7-16): basis "judge" is refused on every agent / category / by -- before ok_rank, so not even fable legalizes it
    _row("judge-scout-recon-haiku", CFG_TODAY, "scout", "haiku", "judge", JUDGE, "recon"),
    _row("judge-scout-recon-fable", CFG_AFTER, "scout", "fable", "judge", JUDGE, "recon"),
    _row("judge-builder-recon-fable", CFG_AFTER, "builder", "fable", "judge", JUDGE, "recon"),
    _row("judge-builder-implementation-sonnet", CFG_TODAY, "builder", "sonnet", "judge", JUDGE, "implementation"),
    _row("judge-critic-implementation-fable", CFG_AFTER, "critic", "fable", "judge", JUDGE, "implementation"),
    _row("judge-designer-review-opus", CFG_AFTER, "designer", "opus", "judge", JUDGE, "review"),
    _row("judge-builder-empty-category", CFG_TODAY, "builder", "sonnet", "judge", JUDGE, ""),
    # `by` is the bare lower-case FAMILY word: a model id, a function word, another case, an alias all FAIL first
    _row("by-model-id", CFG_AFTER, "builder", "claude-opus-5-5", "critic", UNKNOWN_BY),
    _row("by-function-word-lead", CFG_AFTER, "critic", "lead", None, "FUNCTION word"),
    _row("by-function-word-architect-with-judge", CFG_AFTER, "builder", "architect", "judge", "FUNCTION word"),
    _row("by-capitalised", CFG_AFTER, "scout", "Opus", None, UNKNOWN_BY),
    _row("by-padded", CFG_TODAY, "scout", " opus ", None, UNKNOWN_BY),
    _row("by-alias", CFG_AFTER, "scout", "mythos", None, UNKNOWN_BY),
    _row("by-capitalised-queued", CFG_TODAY, "scout", "Sonnet", "queued-to-lead", UNKNOWN_BY),
    _row("by-missing", CFG_TODAY, "scout", None, None, "'by'"),
]
# FG7-88 Q2 / QE1, QE4: a `critic:<task id>` twin of every row whose basis is `critic` -- the same verdict
MATRIX_ROWS += [_row(p.id + "-cited", *p.values[:3], "critic:t-123", p.values[5], p.values[4])
                for p in list(MATRIX_ROWS) if p.values[3] == "critic"]
# QE2: a malformed critic basis gets the verdict of basis None (builder/sonnet: GENERIC), never a pass
MATRIX_ROWS += [_row("qe2-" + rid, CFG_AFTER, "builder", "sonnet", b, GENERIC) for rid, b in [
    ("empty-id", "critic:"), ("short-id", "critic:t-12"), ("trailing-space", "critic:t-123 "),
    ("leading-space", "critic: t-123"), ("upper", "CRITIC:t-123"), ("fullwidth", "critic:t-１２３"),
    ("upper-suffix", "critic:t-123A"), ("semicolon", "critic:t-123;x"), ("word", "critic:lead"),
    ("list", ["critic"]), ("int", 7), ("huge", "critic:t-" + "9" * 5000), ("cyrillic", "critic:t-123а")]]


@pytest.mark.parametrize("cfg,agent,by,basis,category,expect", MATRIX_ROWS)
def test_matrix_by_function_rank(cfg, agent, by, basis, category, expect):
    kw = {} if by is None else {"by": by}
    if basis:
        kw["basis"] = basis
    if category is not None:
        kw["category"] = category
    if agent == "builder":
        kw["witness"] = "w"
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent=agent, model="sonnet", task_id="t-001",
                           notes="matrix cell", **kw))
    code, violations = _decide(staged, HEAD_TEXT, NOW, config_text=cfg)
    if expect is None:
        assert (code, violations) == (0, [])
    else:
        assert code == 1 and any(expect in v for v in violations), violations


# ---- B3 / B4: the two WARNs on a line the matrix PASSED (never a FAIL) ----

def _warn_row(rid, cfg, agent, by, basis, delegated, expect):
    return pytest.param(cfg, agent, by, basis, delegated, expect, id=rid)


WARN_ROWS = [
    _warn_row("after-opus-critic-queued-agent-ref", CFG_AFTER, "critic", "opus", "queued-to-lead", ("critic", "agent:abc"),
              ["queued to itself"]),
    _warn_row("after-opus-critic-queued-nothing-delegated", CFG_AFTER, "critic", "opus", "queued-to-lead", None,
              ["INDEPENDENT CONTEXT", "queued to itself"]),
    _warn_row("today-opus-critic-queued-no-warn", CFG_TODAY, "critic", "opus", "queued-to-lead", None, []),
    _warn_row("after-opus-critic-agent-ref", CFG_AFTER, "critic", "opus", None, ("critic", "agent:abc"), []),
    _warn_row("after-opus-critic-cli-ref", CFG_AFTER, "critic", "opus", None, ("critic", "cli:2026-07-10T08:05:00"),
              ["INDEPENDENT CONTEXT"]),
    _warn_row("after-opus-critic-retro-ref", CFG_AFTER, "critic", "opus", None, ("critic", "retro:later"),
              ["INDEPENDENT CONTEXT"]),
    _warn_row("after-opus-critic-other-agents-agent-ref", CFG_AFTER, "critic", "opus", None, ("scout", "agent:abc"),
              ["INDEPENDENT CONTEXT"]),
    _warn_row("after-opus-designer-nothing-delegated", CFG_AFTER, "designer", "opus", None, None, ["INDEPENDENT CONTEXT"]),
    _warn_row("after-fable-critic-agent-ref", CFG_AFTER, "critic", "fable", None, ("critic", "agent:abc"), []),
    _warn_row("after-fable-critic-nothing-delegated", CFG_AFTER, "critic", "fable", None, None, ["INDEPENDENT CONTEXT"]),
    _warn_row("today-fable-critic-nothing-delegated", CFG_TODAY, "critic", "fable", None, None, ["INDEPENDENT CONTEXT"]),
    _warn_row("today-opus-critic-no-warn", CFG_TODAY, "critic", "opus", "queued-to-lead", ("critic", "cli:x"), []),
    _warn_row("after-sonnet-critic-queued-no-warn", CFG_AFTER, "critic", "sonnet", "queued-to-lead", None, []),
    _warn_row("after-opus-scout-no-warn", CFG_AFTER, "scout", "opus", None, None, []),
]


@pytest.mark.parametrize("cfg,agent,by,basis,delegated,expect", WARN_ROWS)
def test_matrix_warns_on_a_passed_line(cfg, agent, by, basis, delegated, expect):
    new = []
    if delegated:
        new.append(_line(event="delegated", ts="2026-07-10T08:05:00", agent=delegated[0], model="opus", task_id="t-001",
                         worker_ref=delegated[1], notes="a worker of the task"))
    kw = {"by": by}
    if basis:
        kw["basis"] = basis
    new.append(_line(event="accepted", ts="2026-07-10T08:10:00", agent=agent, model="opus", task_id="t-001",
                     notes="accepted", **kw))
    code, violations, warns = jv.decide_with_warnings(_staged(*new), HEAD_TEXT, NOW, known=set(), config_text=cfg)
    assert code == 0, violations
    got = sorted(w.split("WARN ", 1)[1].split(":", 1)[0] for w in warns
                 if "queued to itself" in w or "INDEPENDENT CONTEXT" in w)
    assert got == expect, warns


# ---- FG7-22: a verdict written before the worker returned (WARN only; matrix_warnings -> returned_order_warnings) ----
RET_NOW = jv.datetime.datetime(2026, 11, 18, 12, 0, 0)
D, R, A, X, RS = "delegated", "returned", "accepted", "rejected", "resumed"


def _ret_line(n, ev, tid, agent="builder", ref="agent:a1", ts=None, **kw):
    ts = ts or f"2026-11-17T10:{n:02d}:00"
    if ev == A:
        kw.setdefault("by", "opus")
        kw.setdefault("witness", "pytest -q: 3 passed")
    if ev == X:
        kw.update(by="opus", attempt=1, failure_class="spec")
    if ev in (R, RS):
        kw.update(via="hook")
    return _line(event=ev, ts=ts, agent=agent, model="opus", task_id=tid, worker_ref=ref, notes="n", **kw)


# (id, [(event, task, agent, ref, extra)], expected number of WARNs, texts every WARN holds)
RETURN_ROWS = [
    ("accept-before-return", [(D, "t-002", "builder", "agent:a1", {}), (A, "t-002", "builder", "agent:a1", {})], 1,
     ["agent:a1 (builder)", "t-002", "accepted before the worker returned"]),
    ("returned-then-accept", [(D, "t-002", "builder", "agent:a1", {}), (R, "t-002", "builder", "agent:a1", {}),
                              (A, "t-002", "builder", "agent:a1", {})], 0, []),
    ("pre-era-delegated", [(D, "t-002", "builder", "agent:a1", {"ts": "2026-11-16T22:00:00"}),
                           (A, "t-002", "builder", "agent:a1", {"ts": "2026-11-17T10:30:00"})], 0, []),
    ("other-returned", [(D, "t-002", "builder", "agent:a1", {}), (D, "t-003", "builder", "agent:a2", {}),
                        (R, "t-003", "builder", "agent:a2", {}),
                        (A, "t-002", "builder", "agent:a1", {})], 1, ["agent:a1 (builder)"]),
    ("critic-entry-running", [(D, "t-002", "builder", "agent:a1", {}), (R, "t-002", "builder", "agent:a1", {}),
                              (D, "t-002", "critic", "agent:c1", {}), (A, "t-002", "builder", "agent:a1", {})], 1,
     ["agent:c1 (critic)"]),
    ("superseded-retry", [(D, "t-002", "builder", "agent:a1", {}), (X, "t-002", "builder", "agent:a1", {}),
                          (D, "t-002", "builder", "agent:a2", {"attempt": 2}), (R, "t-002", "builder", "agent:a2", {}),
                          (A, "t-002", "builder", "agent:a2", {})], 1, ["rejected before the worker returned"]),  # only the rejected warns; the accepted is silent
    ("batch", [(D, "t-002", "builder", "agent:a1", {}), (D, "t-003", "builder", "agent:a2", {}),
               (A, "t-002", "builder", "agent:a1", {}), (R, "t-003", "builder", "agent:a2", {}),
               (A, "t-003", "builder", "agent:a2", {})], 1, ["t-002"]),
    ("rejected-before-return", [(D, "t-002", "builder", "agent:a1", {}), (X, "t-002", "builder", "agent:a1", {})], 1,
     ["rejected before the worker returned"]),
    ("cli-ref-and-broken-head", [(D, "t-002", "builder", "cli:x", {}), (A, "t-002", "builder", "cli:x", {})], 0, []),
    ("resumed-verdict-before-second-stop", [(D, "t-002", "builder", "agent:a1", {}), (R, "t-002", "builder", "agent:a1", {}),
                                            (RS, "t-002", "builder", "agent:a1", {}), (A, "t-002", "builder", "agent:a1", {})],
     1, ["agent:a1 (builder)", "accepted before the worker returned"]),                                  # FG7-88 E2
    ("resumed-second-returned-then-verdict", [(D, "t-002", "builder", "agent:a1", {}), (R, "t-002", "builder", "agent:a1", {}),
                                              (RS, "t-002", "builder", "agent:a1", {}), (R, "t-002", "builder", "agent:a1", {}),
                                              (A, "t-002", "builder", "agent:a1", {})], 0, []),            # FG7-88 E1
]


@pytest.mark.parametrize("rid,rows,count,holds", RETURN_ROWS, ids=[r[0] for r in RETURN_ROWS])
def test_verdict_before_returned_warns(rid, rows, count, holds):
    new = [_ret_line(i + 1, ev, tid, agent, ref, **extra) for i, (ev, tid, agent, ref, extra) in enumerate(rows)]
    head = HEAD_TEXT + ("not json at all\n" if rid.startswith("cli-ref") else "")
    code, violations, warns = jv.decide_with_warnings(head + "".join(l + "\n" for l in new), head, RET_NOW, known=set(),
                                                      config_text=CFG_TODAY)
    assert code == 0, violations
    got = [w for w in warns if "before the worker returned" in w]
    assert len(got) == count, warns
    assert all(h in w for w in got for h in holds), got


# ---- the config is read from the ROOT of the repo being validated; absent -> defaults; unreadable -> ONE stderr WARN ----

def _opus_critic_bare():
    return _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic", model="opus", task_id="t-001",
                         by="opus", notes="lead accepts a critic verdict"))


@pytest.mark.parametrize("content,passes,warns", [
    (None, False, False),                                                      # absent: DEFAULT_BINDINGS, silent
    (CFG_AFTER.encode(), True, False),                                         # the file of the repo being validated
    (CFG_TODAY.encode(), False, False),
    (b"roles: [unclosed", False, True),                                        # unparsable
    (b"roles:\n  lead: &a {subscription: {model: x}}\n  critic: *a\n", False, True),   # an alias
    (b"\xff\xfe not utf-8 \x80", False, True),                                 # not text
    (b"#" * (64 * 1024 + 1), False, True),                                     # one byte over 64 KB
    (b"roles:\n  critic: {subscription: {model: claude-opus-5-5}}\n", False, True),   # no lead model
], ids=["absent", "after", "today", "unparsable", "alias", "not-utf8", "oversize", "no-lead"])
def test_config_comes_from_the_root_of_the_validated_repo(tmp_path, monkeypatch, capsys, content, passes, warns):
    if content is not None:
        (tmp_path / "delegation.config.yaml").write_bytes(content)
    monkeypatch.setattr(jv, "_repo_root", lambda: tmp_path)       # the repo being validated
    monkeypatch.setattr(jv, "_CONFIG_ROOTS", {})
    monkeypatch.setattr(jv, "_CONFIG_WARNED", set())
    for _ in range(2):                                                         # twice: the WARN is once per run
        code, violations = jv.decide(_opus_critic_bare(), HEAD_TEXT, NOW)
        assert (code == 0) is passes, violations
    err = capsys.readouterr().err
    assert err.count("delegation.config.yaml") == (1 if warns else 0), err
    assert (not warns) or "default bindings (lead=fable) used" in err


# ---- B5 (F6): an `escalated` of agent `architect` may OPEN a task (the novelty rule of a new delegated) ----

@pytest.mark.parametrize("agent,task_id,expect", [
    ("architect", "t-002", None),                                              # a fresh idea: no task yet
    ("architect", "t-001", None),                                              # an existing task: as before
    ("critic", "t-002", "does not reference anything existing"),               # any other agent: still needs an earlier event
    ("architect", "t-0002", "task_id novelty violated"),                       # not canonical
    ("architect", "t-9999", "jumps more than"),                                # beyond the jump limit
], ids=["architect-opens-task", "architect-existing-task", "other-agent-unseen-task", "architect-non-canonical",
        "architect-jump"])
def test_escalated_architect_may_open_a_task(agent, task_id, expect):
    staged = _staged(_line(event="escalated", ts="2026-07-10T08:10:00", agent=agent, model="fable", task_id=task_id,
                           notes="a question for the Architect"))
    code, violations = _decide(staged, HEAD_TEXT, NOW, config_text=None)
    if expect is None:
        assert (code, violations) == (0, [])
    else:
        assert code == 1 and any(expect in v for v in violations), violations


# ---- B6 (F9): `calibrated` may carry `reviewed_through`, a git sha of 7-40 lower-case hex; nothing else carries it ----

@pytest.mark.parametrize("event,value,bad", [
    ("calibrated", "abc1234", False),                                          # 7 chars
    ("calibrated", "0123456789abcdef0123456789abcdef01234567", False),         # 40 chars
    ("calibrated", "ABC1234", True),                                           # upper case
    ("calibrated", "abc123", True),                                            # 6 chars
    ("calibrated", "0123456789abcdef0123456789abcdef012345678", True),         # 41 chars
    ("calibrated", "xyz1234", True),                                           # not hex
    ("calibrated", "abc1234\n", True),                                         # a trailing newline is not a sha
    ("calibrated", 1234567, True),                                             # not a string
    ("accepted", "abc1234", True),                                             # another event
    ("delegated", "abc1234", True),
], ids=["sha-7", "sha-40", "upper", "six-chars", "forty-one-chars", "non-hex", "trailing-newline", "not-a-string",
        "on-accepted", "on-delegated"])
def test_reviewed_through_is_a_sha_on_calibrated_only(event, value, bad):
    extra = {"model": "sonnet", "task_id": "t-002"} if event != "calibrated" else {}
    if event == "accepted":
        extra.update(agent="scout", by="sonnet")
    obj = json.loads(_line(event=event, ts="2026-07-10T08:10:00", agent=extra.pop("agent", "lead"),
                           category="calibration", notes="Architect review", reviewed_through=value, **extra))
    code, violations = _decide(_staged(json.dumps(obj)), HEAD_TEXT, NOW, config_text=None)
    if bad:
        assert code == 1 and any("reviewed_through" in v for v in violations), violations
    else:
        assert (code, violations) == (0, [])


# ---- B-401: the form checks were moved into _line_form_violations; the order of the texts of one
# line is part of the contract (K-B: the non-merge list is byte-identical to what it was) ----

def test_one_line_with_three_defects_gives_the_exact_ordered_list():
    obj = json.loads(_line(event="delegated", ts="2026-07-10T08:10:00Z", model="sonnet", task_id="t-002",
                           notes="three defects"))
    del obj["model"], obj["worker_ref"]
    code, violations = _decide(_staged(json.dumps(obj, ensure_ascii=False)), HEAD_TEXT, NOW)
    assert code == 1
    assert len(violations) == 3, violations
    tag = "line 2 event='delegated' task_id='t-002'"
    assert violations[0].startswith(f"{tag}: 'model' is required for event=delegated -- ")
    assert violations[1].startswith(f"{tag}: 'worker_ref' is required (non-empty string) for delegated -- ")
    assert violations[2].startswith(f"{tag}: ts '2026-07-10T08:10:00Z' is not ISO format without a timezone -- ")
    assert violations[0].endswith("set model (rule 4)") and violations[1].endswith("(rule 12)")
    assert violations[2].endswith("(rule 10)")


def test_form_fields_vocabulary_and_pairs_cover_every_check():
    # every field a form violation can carry is in FORM_FIELDS ("line" is the parse failures, merge mode)
    cases = [
        {},                                                                   # ts, event, agent, category, notes
        {"ts": "x", "event": "reticulated", "agent": "a", "category": "c", "notes": "n"},
        {"ts": "2026-07-10T08:00:00", "event": "delegated", "agent": "a", "category": "c", "notes": "n"},
        {"ts": "2026-07-10T08:00:00", "event": "rejected", "agent": "a", "category": "c", "notes": "n", "task_id": "t-1"},
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "builder", "category": "c", "notes": "n"},
        {"ts": "2026-07-10T08:00:00", "event": "defect_found", "agent": "a", "category": "c", "notes": "n"},
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "node": "F5-2"},   # t-814: rule 18
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "id_band": "x"},  # F6-58: rule 9e
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "via": "pigeon"},   # rule 20
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "session": "x" * 17},
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "witness_by": "memory"},
        {"ts": "2026-07-10T08:00:00", "event": "accepted", "agent": "a", "category": "c", "notes": "n", "reviewed_through": "abc1234"},  # F9
    ]
    seen = set()
    for obj in cases:
        for field, text in jv._line_form_violations(obj, "T"):
            assert field in jv.FORM_FIELDS and text.startswith("T: ")
            seen.add(field)
    assert seen == set(jv.FORM_FIELDS) - {"line"}


# ---- B-402 K5: the gate stays on BARE ids; only readers key by (label, id) ----

def test_k5_a_retry_on_an_id_whose_declared_instance_is_accepted_is_still_refused_as_closed():
    # t-001 was issued by two clones: the "" instance is open, the (declared) other instance is
    # accepted. A reader keyed by (label, id) would call the "" instance open; the gate does not
    # key -- it over-refuses (the allowed direction) and the door is a fresh id.
    inst_a = _line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-001", model="sonnet", worker_ref="cli:a")
    inst_b = _line(event="delegated", ts="2026-07-10T08:01:00", agent="scout", category="recon", task_id="t-001",
                   model="haiku", worker_ref="cli:b")
    b_done = _line(event="accepted", ts="2026-07-10T08:02:00", agent="scout", category="recon", task_id="t-001",
                   model="haiku", by="sonnet", notes="accepted on the other clone")
    head = "".join(l + "\n" for l in (inst_a, inst_b, b_done))
    retry = _line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-001", model="sonnet", attempt=2,
                  worker_ref="cli:r", notes="retry of the open instance")
    code, violations = _decide(head + retry + "\n", head, NOW)
    assert code == 1 and len(violations) == 1
    assert "delegated on a CLOSED task 't-001'" in violations[0] and "issue a fresh task_id" in violations[0]
    assert "segments" not in jv.decide.__code__.co_varnames


def test_k5_the_real_journal_passes_the_ordinary_path_unchanged():
    import journal_keys as jk
    root = Path(__file__).resolve().parent.parent
    real = [root / "logs" / "routing-log.jsonl"] if (root / "logs" / "routing-log.jsonl").exists() else []
    real += [root / f.path for f in jk.load_all(root).files]                  # the clone's own journal files (the new repository has no history)
    if not real:
        pytest.skip("no journal file in this clone (github-move FK-14)")
    for path in real:
        text = path.read_text(encoding="utf-8")
        assert text.strip() and (len(text.split("\n")) > 100 or path.name != "routing-log.jsonl"), path.name
        assert jv.decide_with_warnings(text, text, NOW) == (0, [], []), path.name


_COLLIDING_LINES = (
    _line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-001", model="sonnet", worker_ref="cli:a"),
    _line(event="delegated", ts="2026-07-10T08:05:00", task_id="t-001", model="sonnet", worker_ref="cli:b"),
)
_GOOD_DECL = json.dumps({"version": 1, "segments": [{"label": "other", "why": "t-001 issued twice", "lines": [
    ["2026-07-10T08:05:00", "t-001", "delegated", "builder", "cli:b"]]}]})
_FAILING_DECL = json.dumps({"version": 1, "segments": [{"label": "other", "why": "x", "lines": [
    ["2026-07-10T08:05:00", "t-001", "delegated", "builder", "cli:zzz"]]}]})


def _repo_with_committed_collision(root: Path):
    _init_repo(root)
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text("".join(l + "\n" for l in _COLLIDING_LINES), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "journal with a collision")


def test_k5_staging_only_the_declaration_runs_the_validator(tmp_path, capsys, monkeypatch):
    root = tmp_path
    _repo_with_committed_collision(root)
    monkeypatch.chdir(root)
    assert jv.main([]) == 0 and capsys.readouterr().err == ""                      # nothing staged: silent
    for name, payload, needle in [("unreadable", "{broken", "journal-segments.json is unreadable"),
                                  ("failing-check", _FAILING_DECL, "matches 0 journal lines")]:
        (root / "logs" / "journal-segments.json").write_text(payload, encoding="utf-8")
        _git(root, "add", "logs/journal-segments.json")                            # the JOURNAL is not staged
        assert jv.main([]) == 1, name
        err = capsys.readouterr().err
        assert "FAILED validation" in err and needle in err, (name, err)
    (root / "logs" / "journal-segments.json").write_text(_GOOD_DECL, encoding="utf-8")
    _git(root, "add", "logs/journal-segments.json")
    assert jv.main([]) == 0 and capsys.readouterr().err == ""                      # a good one lands


def test_k5_a_committed_declaration_that_is_broken_is_a_warn_not_a_fail(tmp_path, capsys, monkeypatch):
    root = tmp_path
    _repo_with_committed_collision(root)
    (root / "logs" / "journal-segments.json").write_text("{broken", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "a broken declaration slipped in")
    new = _line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-002", model="sonnet", notes="next task")
    journal = root / "logs" / "routing-log.jsonl"
    journal.write_text(journal.read_text(encoding="utf-8") + new + "\n", encoding="utf-8")
    _git(root, "add", "logs/routing-log.jsonl")
    monkeypatch.chdir(root)
    assert jv.main([]) == 0
    err = capsys.readouterr().err
    assert "WARN" in err and "journal-segments.json is unreadable or fails its check" in err


# ---- HEAD empty (first-ever commit / fresh deploy) ----

def test_empty_head_first_delegated_must_be_t001():
    staged = _line(event="delegated", ts="2026-07-10T08:00:00", model="sonnet", task_id="t-001",
                   notes="very first task") + "\n"
    code, violations = _decide(staged, "", NOW)
    assert code == 0


def test_empty_head_no_lower_ts_bound():
    staged = _line(event="delegated", ts="2020-01-01T00:00:00", model="sonnet", task_id="t-001",
                   notes="old ts, no HEAD to compare against") + "\n"
    code, violations = _decide(staged, "", NOW)
    assert code == 0


# ---- crash path: main() fail-closed with exit 2 on unexpected exception ----

def test_main_crashes_exit_2_with_traceback(monkeypatch, capsys):
    def _boom():
        raise RuntimeError("simulated crash, not a validation FAIL")

    monkeypatch.setattr(jv, "is_journal_staged", _boom)
    code = jv.main([])
    assert code == 2
    err = capsys.readouterr().err
    assert "Traceback" in err
    assert "simulated crash" in err


# ---- real git integration: not-staged -> exit 0 silently; staged violation -> exit 1 ----

def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")


def _init_repo(root: Path):
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")


def test_main_exits_zero_when_journal_not_staged(tmp_path, capsys, monkeypatch):
    root = tmp_path
    _init_repo(root)
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text(HEAD_TEXT, encoding="utf-8")
    _git(root, "add", "logs/routing-log.jsonl")
    _git(root, "commit", "-q", "-m", "seed journal")
    # nothing staged now (working tree clean)
    monkeypatch.chdir(root)
    code = jv.main([])
    assert code == 0
    assert capsys.readouterr().out == ""


def test_main_exits_one_on_real_staged_violation(tmp_path, capsys, monkeypatch):
    root = tmp_path
    _init_repo(root)
    (root / "logs").mkdir()
    (root / "logs" / "routing-log.jsonl").write_text(HEAD_TEXT, encoding="utf-8")
    _git(root, "add", "logs/routing-log.jsonl")
    _git(root, "commit", "-q", "-m", "seed journal")
    bad_line = _line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-9999", model="sonnet",
                      notes="wrong novelty")
    (root / "logs" / "routing-log.jsonl").write_text(_staged(bad_line), encoding="utf-8")
    _git(root, "add", "logs/routing-log.jsonl")
    monkeypatch.chdir(root)
    code = jv.main([])
    assert code == 1
    err = capsys.readouterr().err
    assert "FAILED validation" in err
    assert "task_id novelty" in err


# =======================================================================
# The self/foreign-retry gap (rule 9c): "chuzhoi" (foreign) rejected --
# a rejected of an EXECUTOR does not, by itself, legalize a REVIEWER's
# repeat delegated on the same task_id; a foreign-retry entry is legal
# only with a new-version signal AFTER the re-entering agent's own last
# delegated. Self-retry (the same agent whose own result was rejected)
# stays unconditional, unchanged.
# =======================================================================


def test_b3_second_critic_entry_without_executor_rework_between_is_dup():
    # critic enters review (case b, first entry), then rejects builder's
    # result (rejected agent=builder) -- and tries a SECOND entry with
    # NOTHING reworked by builder in between (no new delegated builder,
    # no lead fix, no escalated). The unqualified old form would have
    # legalized this entry merely by the task carrying a rejected --
    # the fixed form must FAIL.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1, case b"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work"),
        _line(event="delegated", ts="2026-07-10T08:15:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, NO rework between -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


def test_b3_stale_rework_signal_from_earlier_round_does_not_legalize_next_round():
    # Round 1: builder reworks (own retry) AFTER critic's entry 1 -- a
    # valid "delegated of a different agent" signal, legalizing critic's
    # entry 2. Round 2: builder rejected AGAIN, critic tries a THIRD
    # entry citing the SAME (now stale, round-1) rework signal -- the
    # signal predates critic's entry-2 delegated (its own last
    # delegated), so it must NOT legalize round 2 -- FAIL.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="round 1 reject"),
        _line(event="delegated", ts="2026-07-10T08:15:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, notes="builder self-retry -- also a rework SIGNAL for critic"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, legal via round-1 rework signal"),
        _line(event="rejected", ts="2026-07-10T08:25:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, failure_class="spec", by="critic",
              notes="round 2 reject, no new rework signal since entry 2"),
        _line(event="delegated", ts="2026-07-10T08:30:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 3, citing STALE round-1 signal -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


def test_b3_self_retry_still_legal_without_any_other_agent_delegated_between():
    # (c-i) self-retry: builder rejected, then builder retries -- no
    # other agent delegated anywhere in between. Must stay legal
    # (unchanged class, a regression pin for the "as before" form).
    staged = _staged(
        _line(event="rejected", ts="2026-07-10T08:05:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="opus",
              notes="builder rejected"),
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, notes="builder self-retry, nothing else happened between"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_b3_new_delegated_of_different_agent_after_own_rejected_not_required():
    # (c-i) self-retry doesn't NEED a signal -- even though critic is
    # ALREADY present in this task's delegated_agents (entry 1),
    # builder's own retry after its OWN rejected does not require a
    # fresh critic delegated between the reject and the retry.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work"),
        _line(event="delegated", ts="2026-07-10T08:15:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2,
              notes="builder self-retry -- own rejected is enough, no fresh critic-delegated needed"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_b3_lead_self_fix_rejected_signal_legalizes_review_round():
    # (c-ii) signal (2): a rejected event with agent=lead (a Lead
    # self-fix with no own delegated) counts as a new-version signal --
    # it legalizes critic's second entry even though nobody issued a
    # fresh delegated.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work"),
        _line(event="rejected", ts="2026-07-10T08:15:00", agent="lead", model="fable",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="Lead self-fixed the code directly, no own delegated -- the fix itself is the signal"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, legal via lead-self-fix signal"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_b3_stale_lead_self_fix_signal_from_earlier_round():
    # Same staleness class as the rework-signal test, but with a
    # lead-self-fix signal: round 1's lead-fix legalizes entry 2, but
    # round 2's third entry cannot reuse that same, now-stale signal.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="round 1 reject"),
        _line(event="rejected", ts="2026-07-10T08:15:00", agent="lead", model="fable",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="Lead self-fix, round 1 signal"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, legal via round-1 lead-fix signal"),
        _line(event="rejected", ts="2026-07-10T08:25:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, failure_class="spec", by="critic",
              notes="round 2 reject, no new lead-fix signal since entry 2"),
        _line(event="delegated", ts="2026-07-10T08:30:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 3, citing STALE round-1 lead-fix -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


def test_b3_escalated_signal_legalizes_review_round():
    # (c-ii) signal (3): a new escalated event on the task_id.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="builder", model="opus",
              task_id="t-001", notes="task escalated one tier up"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, legal via escalated signal"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_b3_stale_escalated_signal_from_earlier_round():
    # Staleness class for the escalated signal: round 1's escalated
    # legalizes entry 2, round 2's entry 3 cannot reuse it.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="round 1 reject"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="builder", model="opus",
              task_id="t-001", notes="round 1 escalated signal"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 2, legal via round-1 escalated signal"),
        _line(event="rejected", ts="2026-07-10T08:25:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=2, failure_class="spec", by="critic",
              notes="round 2 reject, no new escalated signal since entry 2"),
        _line(event="delegated", ts="2026-07-10T08:30:00", agent="critic", model="opus",
              task_id="t-001", attempt=2, notes="critic entry 3, citing STALE round-1 escalated -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


def test_b3_boundary_signal_on_different_task_id_does_not_legalize_this_one():
    # A rework signal (delegated of a different agent) fired on t-002
    # must NOT legalize a foreign retry on t-001 -- signal_log is keyed
    # per task_id; this pins that isolation.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-002", notes="unrelated task t-002, NOT t-001 -- signal must not leak"),
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1 on t-001"),
        _line(event="rejected", ts="2026-07-10T08:15:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work on t-001"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2,
              notes="critic entry 2 on t-001, only signal available is on t-002 -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


# ---- failure text branches by valid_attempt FIRST, not by signal state -


def test_foreign_rejected_fresh_signal_but_missing_attempt_names_attempt_not_signal():
    # A foreign rejected EXISTS, a fresh valid signal (escalated by a
    # DIFFERENT agent, strictly after critic's own last delegated)
    # EXISTS -- but attempt on the repeat delegated is ABSENT. The
    # unbranched text would falsely claim "no signal, or stale"; the
    # fix must name attempt specifically and must NOT claim the signal
    # is absent/stale.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work -- foreign rejected for critic"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="builder", model="opus",
              task_id="t-001", notes="fresh valid signal, strictly after critic's entry 1"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 2, NO attempt field -- must FAIL naming attempt"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any("'attempt' field" in v for v in violations), violations
    assert not any('"foreign" rejected' in v for v in violations), violations


def test_same_history_with_valid_attempt_passes():
    # LITERALLY the same history, the only difference -- attempt=2 is
    # present on the repeat delegated -- legal (proves the signal really
    # was fresh and valid; the real defect above was attempt, not the
    # signal).
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work -- foreign rejected for critic"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="builder", model="opus",
              task_id="t-001", notes="fresh valid signal, strictly after critic's entry 1"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2,
              notes="critic entry 2, attempt=2 present -- must PASS"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_self_recorded_escalated_does_not_legalize_own_reentry():
    # critic records an escalated on its OWN task (agent=critic on the
    # escalated event), then tries a repeat entry citing that same
    # escalated as a new-version signal -- a self-legalizing loop, must
    # FAIL (escalated only counts as a signal when it names a DIFFERENT
    # agent).
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work -- foreign rejected for critic"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="critic", model="opus",
              task_id="t-001", notes="critic escalates ITSELF on its own task_id"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2,
              notes="critic entry 2, citing its OWN escalated as signal -- must FAIL"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations
    assert any('"foreign" rejected' in v for v in violations), violations


def test_positive_pair_escalated_of_different_agent_still_legalizes():
    # The paired positive (same shape, but escalated by a DIFFERENT
    # agent, not critic) -- stays legal as before (the narrowing above
    # only excludes SELF-escalation, not escalated in general).
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:05:00", agent="critic", model="opus",
              task_id="t-001", notes="critic entry 1"),
        _line(event="rejected", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", attempt=1, failure_class="spec", by="critic",
              notes="critic rejects builder's work -- foreign rejected for critic"),
        _line(event="escalated", ts="2026-07-10T08:15:00", agent="builder", model="opus",
              task_id="t-001", notes="escalated by a different agent -- still a valid signal"),
        _line(event="delegated", ts="2026-07-10T08:20:00", agent="critic", model="opus",
              task_id="t-001", attempt=2,
              notes="critic entry 2, legal via a different-agent escalated"),
    )
    code, violations = _decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


# ---- direct unit coverage of the harvest/signal helpers ---------------


def test_has_new_version_signal_direct_stale_vs_fresh_boundary():
    signal_log = {"t-001": [(5, "delegated", "builder"), (10, "escalated", "builder")]}
    # A signal at idx==after_idx is NOT strictly after -- stale.
    assert jv._has_new_version_signal("t-001", "critic", 5, signal_log) is True  # idx 10 > 5
    assert jv._has_new_version_signal("t-001", "critic", 10, signal_log) is False  # nothing > 10
    assert jv._has_new_version_signal("t-001", "critic", 11, signal_log) is False


def test_has_new_version_signal_ignores_same_agent_kinds():
    signal_log = {"t-001": [(5, "delegated", "critic"), (6, "escalated", "critic")]}
    # Both signals are BY the same agent asking the question -- neither
    # counts (a delegated/escalated must be of a DIFFERENT agent).
    assert jv._has_new_version_signal("t-001", "critic", 0, signal_log) is False


def test_harvest_task_state_returns_seven_tuple():
    delegated_agents, closed_tasks, rejected_tasks, task_worker_refs, rejected_by_agent, last_delegated_idx, signal_log = jv.harvest_task_state(
        [_line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-001", agent="builder", model="sonnet")]
    )
    assert delegated_agents == {"t-001": {"builder"}}
    assert last_delegated_idx[("t-001", "builder")] == 0
    assert signal_log["t-001"] == [(0, "delegated", "builder")]


# ================================ K8: the file that continues the history (t-581, F0-4) ================================
# decide(..., seed_text=<the history>) is what the pre-commit gate, the echo and --all call for the
# developer file whose line 1 carries `continues`. The git halves (two successors, the freeze) are in
# test_journal_per_developer.py.

from test_journal_per_developer import (HISTORY, HISTORY_TEXT, M_CREATED, accepted as _acc, created as _created,
                                        delegated as _deleg, jtext as _jtext)

_NOW8 = jv.datetime.datetime(2026, 10, 3, 12, 0, 0)          # the history of the fixture ends at t-002, 2026-10-01T10:00
_FILE8 = "logs/journal/dev1.jsonl"


def _k8(*objs, seed=HISTORY_TEXT, head=None):
    return _decide(_jtext(*objs), head, _NOW8, seed_text=seed)


def test_k8_the_history_is_the_seen_set_and_the_jump_base_of_the_file():
    # REWRITTEN (offload B0, rule 9a''): "the next id is the max of the history + 1 and only that" is retired; a gap
    # (t-004, t-009) is legal, a seen id is a repeat (9b-9d), a jump over 1000 above the history's max is refused
    assert _k8(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00")) == (0, [])
    for gap in ("t-004", "t-009", "t-1002"):                 # +1, +6 and exactly the cap above the history's t-002
        assert _k8(M_CREATED, _deleg(gap, "2026-10-02T08:30:00")) == (0, []), gap
    code, violations = _k8(M_CREATED, _deleg("t-002", "2026-10-02T08:30:00"))
    assert code == 1 and any("repeated delegated" in v for v in violations)     # t-002 of the history is a SEEN open task
    code, violations = _k8(M_CREATED, _deleg("t-1003", "2026-10-02T08:30:00"))
    assert code == 1 and any("jumps more than 1000 above the sequence (the highest t-NNN is 2)" in v for v in violations)
    code, violations = _k8(M_CREATED, _deleg("t-001", "2026-10-02T08:30:00"))
    assert any("CLOSED task" in v for v in violations)      # t-001 is accepted in the history


def test_k8_without_the_seed_the_jump_is_measured_from_zero():
    assert _k8(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00"), seed=None) == (0, [])
    assert _k8(M_CREATED, _deleg("t-1000", "2026-10-02T08:30:00"), seed=None) == (0, [])
    code, violations = _k8(M_CREATED, _deleg("t-1002", "2026-10-02T08:30:00"), seed=None)      # legal WITH the seed (above)
    assert code == 1 and any("no id exists yet" in v for v in violations)
    assert _k8(_created("2026-10-02T08:00:00"), _deleg("t-001", "2026-10-02T08:30:00"), seed=None) == (0, [])


def test_k8_an_accepted_of_a_task_of_the_history_passes_in_the_successor_and_fails_without_the_seed():
    lines = (M_CREATED, _acc("t-002", "2026-10-02T09:00:00"))
    assert _k8(*lines) == (0, [])
    code, violations = _k8(*lines, seed=None)
    assert code == 1 and any("does not reference anything existing earlier in the file" in v for v in violations)


def test_k8_the_ts_of_the_first_line_is_anchored_on_the_history():
    code, violations = _k8(_created("2026-09-30T08:00:00", continues=HISTORY))      # before the history's last line
    assert code == 1 and any("not monotonic" in v for v in violations)


def test_k8_line_numbers_in_the_messages_are_those_of_the_file_not_of_the_seed():
    code, violations = _k8(M_CREATED, _deleg("t-2500", "2026-10-02T08:30:00"))
    assert code == 1 and violations[0].startswith("line 2 ")


def test_k8_an_empty_developer_file_passes_and_has_no_line_1_to_check():
    assert _decide("", None, _NOW8) == (0, [])
    assert _decide("", None, _NOW8, seed_text=HISTORY_TEXT) == (0, [])
    assert jv.developer_file_violations(_FILE8, []) == []


def test_k8_line_1_must_be_a_journal_created_and_continues_only_on_line_1_with_the_history():
    refused = jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_deleg("t-003", "2026-10-02T08:30:00"))))
    assert len(refused) == 1 and refused[0].startswith(f"{_FILE8} line 1 is not a journal_created event")
    assert jv.developer_file_violations(_FILE8, jv.split_lines(_jtext("{not json"))) != []         # an unparsable line 1
    assert jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(M_CREATED))) == []
    assert jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_created("2026-10-02T08:00:00")))) == []
    line2 = jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_created("2026-10-02T08:00:00"), M_CREATED)))
    assert len(line2) == 1 and "line 2: `continues` is allowed on line 1 only" in line2[0]
    elsewhere = jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_created("2026-10-02T08:00:00", continues="logs/other.jsonl"))))
    assert len(elsewhere) == 1 and "`continues` must be 'logs/routing-log.jsonl'" in elsewhere[0]
    # a non-string value is a value that is not the history, and a 60-character cap keeps the text short
    huge = jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_created("2026-10-02T08:00:00", continues="x" * 500))))
    assert len(huge) == 1 and len(huge[0]) < 400
    assert jv.developer_file_violations(_FILE8, jv.split_lines(_jtext(_created("2026-10-02T08:00:00", continues=7)))) != []


def test_k8_the_merge_mode_passes_the_seed_too():
    head = _jtext(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00"))
    other = _jtext(M_CREATED, _deleg("t-004", "2026-10-02T08:40:00"))
    staged = _jtext(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00"), _deleg("t-004", "2026-10-02T08:40:00"))
    code, violations, _w = jv.decide_merge(staged, head, other, _NOW8, segments=jv._jk.NO_SEGMENTS, seed_text=HISTORY_TEXT)
    assert (code, violations) == (0, [])


# ================ rule 9a'' (offload B0, BL-1): the id of a NEW delegated; rule 9e (bands) RETIRED ================
# REWRITTEN group (the F6-58 rows j1-j18 + S1/P10/edge/j10/j11 band rows): a new line carrying `id_band` is a
# `band_retired` violation, an old band in HEAD still feeds the jump base (TEMPORAL, read-only), and the id of a new
# line is judged by "never seen + canonical + at most 1000 above the max of its letter". A spec is ("d", id[, band]) for a
# delegated line or ("x", None[, band]) for a decomposable line that carries only a band; a 3rd element, even None,
# writes the `id_band` field. HEAD specs are state (never judged), NEW specs are judged.

def _band_lines(specs, base_hour):
    out = []
    for i, spec in enumerate(specs):
        ts = (jv.datetime.datetime(2026, 7, 10, base_hour) + jv.datetime.timedelta(seconds=i)).isoformat()
        kw = {"id_band": spec[2]} if len(spec) == 3 else {}
        if spec[0] == "d":
            out.append(_line(event="delegated", task_id=spec[1], model="sonnet", ts=ts, **kw))
        else:
            out.append(_line(event="decomposable", agent="lead", category="process", ts=ts, **kw))
    return out


def _band_run(head, new):
    return jv.validate_new_lines(_band_lines(new, 9), _band_lines(head, 6), NOW)


def _ids(a, b):
    return [("d", f"t-{n}") for n in range(a, b + 1)]


_HUGE = "t-" + "9" * 5000 + ".."
_FORM_VALUES = ["t-5..t-9", "500..", "t-500 .. t-510", "t-500–t-510", "", ["t-1"], {"from": "t-1"}, 500,
                "t-４００..t-４４９", "t-1234567890..", _HUGE]
_RETIRED = ("band_retired", "`id_band` is retired", "python -B tools/journal_write.py next")

# (row, head specs, new specs, needles that must ALL appear in the violations; () = no violation at all)
ID_BAND_ROWS = [
    # --- the retired road: a band on a NEW line is refused, whatever it holds, and names the writer ---
    ("j1-band-on-a-new-delegated", [("d", "t-356")], [("d", "t-357", "t-450..t-499")], _RETIRED),
    ("j1-band-on-a-new-decomposable", [("d", "t-356")], [("x", None, "t-450..t-499")], _RETIRED),
    ("j1-open-band", [("d", "t-356")], [("x", None, "t-450..")], _RETIRED),
    ("j1-band-with-its-first-id", [("d", "t-356")], [("d", "t-450", "t-450..t-499")], _RETIRED),
    ("j3-band-below-the-sequence", [("d", "t-356")], [("x", None, "t-300..t-310")], _RETIRED),
    ("j6-reversed-band", [("d", "t-356")], [("x", None, "t-500..t-499")], _RETIRED),
    ("j7-1001-band", [("d", "t-356")], [("x", None, "t-500..t-1500")], _RETIRED),
    # the band never makes an id legal: an id far above the sequence stays a jump, the band is a second violation
    ("j17-band-never-legalises-an-id", [("d", "t-356")], [("x", None, "t-5000..t-5010"), ("d", "t-5000", "t-5000..t-5010")],
     _RETIRED + ("got t-5000", "jumps more than 1000 above the sequence (the highest t-NNN is 356)")),
    # --- null and absent bands are not bands; a junk band of an OLD line is never judged (temporal) ---
    ("j13-null-band-is-no-band", [("d", "t-356")], [("x", None, None), ("d", "t-357", None)], ()),
    ("j12-old-junk-band-in-head-is-not-judged", [("d", "t-356", "junk")], [("d", "t-357")], ()),
    # --- rule 9a'': gaps and out-of-order are legal; the jump cap is 1000 above the max of the letter ---
    ("j14-no-band-in-order", [("d", "t-356")], [("d", "t-357"), ("d", "t-358")], ()),
    ("j14-gap-of-one-is-legal", [("d", "t-356")], [("d", "t-358")], ()),
    ("e3-jump-at-1000-is-legal", [("d", "t-356")], [("d", "t-1356")], ()),
    ("e3-jump-at-1001-is-refused", [("d", "t-356")], [("d", "t-1357")],
     ("task_id novelty violated", "got t-1357", "jumps more than 1000 above the sequence (the highest t-NNN is 356)")),
    ("e8-reserved-lower-id-after-a-higher-one", [("d", "t-356")], [("d", "t-358"), ("d", "t-357"), ("d", "t-359")], ()),
    ("e8-next-n3-written-in-the-reverse-order", [("d", "t-899")], [("d", "t-902"), ("d", "t-900"), ("d", "t-901")], ()),
    ("e8-t901-then-t900", [("d", "t-899")], [("d", "t-901"), ("d", "t-900")], ()),
    ("e3-the-jump-base-follows-the-highest-new-line", [("d", "t-356")], [("d", "t-1356"), ("d", "t-2356"), ("d", "t-2357")], ()),
    ("e3-the-jump-base-follows-the-highest-new-line-beyond", [("d", "t-356")], [("d", "t-1356"), ("d", "t-2357")],
     ("got t-2357", "highest t-NNN is 1356")),
    # --- E-B0-4: an id issued twice is a SEEN id, judged as a repeat (9b-9d), never as a new one ---
    ("e4-same-id-twice-same-agent", [("d", "t-356")], [("d", "t-357"), ("d", "t-357")], ("repeated delegated by the same agent",)),
    ("e4-reused-id-of-head", [("d", "t-356")], [("d", "t-356")], ("repeated delegated by the same agent",)),
    # --- E-B0-1: an id the issue grammar refuses (readable as a string, never issued) ---
    ("e1-leading-zero", [("d", "t-356")], [("d", "t-0357")], ("got t-0357", "is not canonical")),
    ("e1-000", [("d", "t-356")], [("d", "t-000")], ("got t-000", "is not canonical")),
    ("e1-0001", [("d", "t-356")], [("d", "t-0001")], ("got t-0001", "is not canonical")),
    ("e1-4-digit-no-zero-is-canonical", [("d", "t-999")], [("d", "t-1000")], ()),
    # --- the letter: t-123 and t-123a are two tasks, each with its own jump base ---
    ("l1-first-id-of-a-letter", [("d", "t-356")], [("d", "t-001a")], ()),
    ("l2-letter-at-1000-is-legal", [("d", "t-356")], [("d", "t-1000a")], ()),
    ("l2-letter-at-1001-is-refused", [("d", "t-356")], [("d", "t-1001a")],
     ("got t-1001a", "jumps more than 1000 above the sequence (no id with letter 'a' exists yet)")),
    ("l3-the-letter-has-its-own-base", [("d", "t-356"), ("d", "t-040a")], [("d", "t-1040a")], ()),
    ("l3-the-letter-has-its-own-base-beyond", [("d", "t-356"), ("d", "t-040a")], [("d", "t-1041a")],
     ("got t-1041a", "the highest t-NNNa is 40")),
    ("l4-the-same-number-with-a-letter-is-a-new-id", [("d", "t-356")], [("d", "t-356a")], ()),
    ("l4-the-bare-number-after-its-lettered-twin-is-new", [("d", "t-356a")], [("d", "t-356")], ()),
    ("l5-two-letters", [("d", "t-356")], [("d", "t-001ab")], ()),
    ("l6-a-lettered-id-twice-is-a-repeat", [("d", "t-356a")], [("d", "t-356a")], ("repeated delegated by the same agent",)),
    # --- TEMPORAL: the old bands in HEAD still feed the base of the letterless sequence (both worlds on one row) ---
    ("old-band-in-head-feeds-the-base-legal", [("d", "t-356"), ("x", None, "t-400..t-449")], [("d", "t-1449")], ()),
    ("old-band-in-head-feeds-the-base-beyond", [("d", "t-356"), ("x", None, "t-400..t-449")], [("d", "t-1450")],
     ("got t-1450", "the highest t-NNN is 449")),
    ("old-band-in-head-does-not-reserve-its-ids", [("d", "t-356"), ("x", None, "t-400..t-449")], [("d", "t-357")], ()),
] + [(f"j5-form-{i}", [("d", "t-356")], [("x", None, v)], _RETIRED) for i, v in enumerate(_FORM_VALUES)]


@pytest.mark.parametrize("row,head,new,needles", ID_BAND_ROWS, ids=[r[0] for r in ID_BAND_ROWS])
def test_id_band(row, head, new, needles):
    violations = _band_run(head, new)
    joined = "\n".join(violations)
    if not needles:
        assert violations == [], violations
        return
    assert violations, row
    for needle in needles:
        assert needle in joined, (needle, violations)
    assert not any("max+1" in v or "id band" in v or "open a band" in v for v in violations)       # no band advice left


def test_id_band_a_band_on_a_new_line_never_enters_the_state_and_a_foreign_bad_band_is_clearable():
    # the retired band of a NEW line does not make a later id issuable: t-5001 stays a jump
    v = _band_run([("d", "t-356")], [("x", None, "t-5000..t-5010"), ("d", "t-5001")])
    assert any("task_id novelty violated" in x and "got t-5001" in x for x in v)
    assert "id_band" in jv.FORM_FIELDS
    assert [f for f, _t in jv._line_form_violations(json.loads(_line(id_band="junk", event="decomposable")), "T")] == ["id_band"]
    assert jv._line_form_violations(json.loads(_line(event="decomposable", id_band=None)), "T") == []


def test_the_novelty_text_names_the_writer_and_gives_no_band_advice():
    v = _band_run([("d", "t-356")], [("d", "t-0357"), ("d", "t-2357")])
    assert len(v) == 2
    for text in v:
        assert "python -B tools/journal_write.py next" in text and "(rule 9a'')" in text
        assert "band" not in text and "id_band" not in text and "journal_keys.py where" not in text
    assert "is not canonical" in v[0] and "jumps more than 1000" in v[1]


# ---- rule 19 (FG7-32): the order-known door, ONE table ----
# HEAD holds t-001 @08:00. Each case is (new lines, seed_text, expected code, [texts the violations must hold],
# [texts the WARN list must hold], declared count). The defects: an id past the jump cap (t-2005, rule 9a''), a ts
# earlier than HEAD's last line, a repeated delegated by one agent with no attempt.
_D = "2026-07-10T"


def _tok(ts, at, notes=None):
    return _line(event="dispatch_skipped", ts=_D + at, notes=notes or f"order-known:{_D}{ts}")


def _id_bad(ts="09:00:00", tid="t-2005", **kw):       # REWRITTEN: t-005 is a legal gap now; t-2005 jumps over the cap
    return _line(task_id=tid, model="sonnet", ts=_D + ts, **kw)


_TS_BAD = _line(task_id="t-002", model="sonnet", ts=_D + "07:00:00")
_DUP_OK = _line(task_id="t-002", model="sonnet", ts=_D + "09:00:00")
_DUP_BAD = _line(task_id="t-002", model="sonnet", ts=_D + "10:00:00")
_DEFECTS = {
    "id": ([_id_bad()], "09:00:00", "t-2005", "10:30:00"),
    "ts": ([_TS_BAD], "07:00:00", "t-002", "09:00:00"),
    "dup": ([_DUP_OK, _DUP_BAD], "10:00:00", "t-002", "10:30:00"),
}
_CASES = {}
for _name, (_lines, _dts, _tid, _later) in _DEFECTS.items():
    _tk = f"order-known:{_D}{_dts}"
    _CASES[f"{_name}-not-declared"] = (_lines, None, 1, [_tk, _tid], [], 0)
    _CASES[f"{_name}-declared-by-later-line"] = (_lines + [_tok(_dts, _later)], None, 0, [], [], 1)
    _CASES[f"{_name}-declared-with-ts-naming-no-line"] = (
        _lines + [_tok("11:11:11", _later)], None, 1, [_tk, "names no line", f"order-known:{_D}11:11:11"], [], 0)
_CASES["edge4-token-before-the-line-does-not-count"] = (
    [_tok("09:00:00", "08:30:00"), _id_bad()], None, 1,
    [f"order-known:{_D}09:00:00", "names no line"], [], 0)
_CASES["edge4-token-naming-a-clean-line-is-a-warn"] = (
    [_tok("08:00:00", "09:00:00")], None, 0, [],
    ["names a line already in HEAD; HEAD lines are not judged, so nothing was declared"], 0)
_CASES["f1-prose-ts-placeholder-is-a-warn-and-code-0"] = (
    [_line(event="dispatch_skipped", ts=_D + "09:00:00", notes="the form is order-known:<ts> in prose")], None, 0, [],
    ["is not a ts", "order-known:<ts>"], 0)
_CASES["f1-prose-ts-placeholder-never-declares-the-defect-stays-refused"] = (
    [_id_bad(), _tok("09:00:00", "10:30:00", "the form is order-known:<ts>)")], None, 1,
    [f"order-known:{_D}09:00:00", "task_id novelty"], ["is not a ts"], 0)
_CASES["f1-ts-shaped-typo-still-names-no-line"] = (
    [_id_bad(), _tok("09:00:01", "10:30:00")], None, 1,
    [f"order-known:{_D}09:00:01", "names no line"], [], 0)
_CASES["f2-one-token-over-a-line-with-two-defects-counts-1"] = (
    [_id_bad(ts="07:00:00"), _tok("07:00:00", "10:30:00")], None, 0, [], [], 1)
_CASES["f3-order-defect-and-missing-worker-ref-and-token-stays-refused"] = (
    [_id_bad(worker_ref=None), _tok("09:00:00", "10:30:00")], None, 1, ["worker_ref"], [], 1)
_CASES["edge4-two-lines-with-one-ts-both-covered"] = (
    [_id_bad(), _id_bad(tid="t-3009"), _tok("09:00:00", "10:30:00")], None, 0, [], [], 2)
_CASES["edge4-token-on-the-defective-line-itself-does-not-count"] = (
    [_id_bad(notes=f"order-known:{_D}09:00:00")], None, 1, [f"order-known:{_D}09:00:00"], [], 0)
_CASES["edge5-empty-token-is-ignored-and-warned"] = (
    [_id_bad(), _tok("09:00:00", "10:30:00", "order-known: nothing")], None, 1,
    [f"order-known:{_D}09:00:00"], ["nothing after the colon"], 0)
_CASES["edge6-a-token-of-another-file-declares-nothing"] = (
    [_id_bad()], _tok("09:00:00", "09:30:00") + "\n", 1, [f"order-known:{_D}09:00:00"], [], 0)


@pytest.mark.parametrize("case", sorted(_CASES))
def test_order_known_door_table(case):
    lines, seed, code_want, viol_want, warn_want, declared_want = _CASES[case]
    code, violations, warnings = jv.decide_with_warnings(_staged(*lines), HEAD_TEXT, NOW, known=set(), seed_text=seed)
    assert code == code_want, (violations, warnings)
    joined = "\n".join(violations)
    for text in viol_want:
        assert text in joined, (text, violations)
    wjoined = "\n".join(warnings)
    for text in warn_want:
        assert text in wjoined, (text, warnings)
    if declared_want:
        assert f"order-known: {declared_want} declared" in wjoined
    else:
        assert not any(w.startswith("order-known: ") for w in warnings)


# FG7-34: the count line is printed by ONE producer on the commit, merge and --all paths: a row per path x count.
def _order_known_warns(path, staged):
    if path == "merge":
        return jv.decide_merge(staged, HEAD_TEXT, None, NOW, known=set())[2]
    return jv._developer_file_result("logs/journal/x.jsonl", staged, HEAD_TEXT, None, NOW, drift=False,
                                     one_writer=False)[1]


@pytest.mark.parametrize("path", ["merge", "all"])
@pytest.mark.parametrize("declared", [0, 1])
def test_order_known_count_on_every_path(path, declared):
    lines = [_id_bad(), _tok("09:00:00", "10:30:00")] if declared else [_id_bad(ts="10:00:00", tid="t-002")]
    counts = [w for w in _order_known_warns(path, _staged(*lines)) if w.startswith("order-known: ")]
    assert (len(counts) == 1 and counts[0].startswith("order-known: 1 declared")) if declared else not counts


# ================ offload B0: `returned` (rule 9f, E-B0-6), rule 20 fields, E-B0-1 form, E-B0-5 both worlds ================
# HEAD holds t-001 delegated to builder with worker_ref cli:2026-07-10T08:00:00 (an OPEN task).
_WREF = "cli:2026-07-10T08:00:00"


def _ret(ts="2026-07-10T08:30:00", tid="t-001", wref=_WREF, **kw):
    return _line(event="returned", ts=ts, agent="builder", model="sonnet", task_id=tid, worker_ref=wref,
                 notes="the dispatch returned", **kw)


_CLOSED_HEAD = HEAD_TEXT + _line(event="accepted", ts="2026-07-10T08:20:00", agent="builder", model="sonnet",
                                 task_id="t-001", by="opus", witness="w", notes="closed") + "\n"
_RETURNED_DOOR = "journal_write.py returned --task <id> --worker <worker_ref>"


def _res(ts="2026-07-10T08:31:00", tid="t-001", wref=_WREF):
    return _line(event="resumed", ts=ts, agent="builder", model="sonnet", task_id=tid, worker_ref=wref, notes="resumed")


# (row, staged new lines, head text, code, [needles in the violations])
RETURNED_ROWS = [
    ("matching-open-delegated", [_ret()], HEAD_TEXT, 0, []),
    ("matching-with-optional-fields", [_ret(via="hook", session="a1-B2", witness_by="run")], HEAD_TEXT, 0, []),
    ("wrong-worker-ref", [_ret(wref="agent:other")], HEAD_TEXT, 1,
     ["no earlier open delegated of t-001 carries worker_ref 'agent:other'", _RETURNED_DOOR, "(rule 9f)"]),
    ("closed-task", [_ret(ts="2026-07-10T08:30:00")], _CLOSED_HEAD, 1, ["t-001 is already closed", _RETURNED_DOOR]),
    ("no-task-at-all", [_ret(tid="t-077")], HEAD_TEXT, 1, ["t-077 has no delegated earlier in this journal", _RETURNED_DOOR]),
    ("twice-for-one-pair", [_ret(), _ret(ts="2026-07-10T08:31:00")], HEAD_TEXT, 1,
     ["t-001 already has a returned for worker_ref"]),
    ("resumed-then-second-returned", [_ret(), _res(), _ret(ts="2026-07-10T08:32:00")], HEAD_TEXT, 0, []),
    ("returned-twice-after-one-resume", [_ret(), _res(), _ret(ts="2026-07-10T08:32:00"), _ret(ts="2026-07-10T08:33:00")],
     HEAD_TEXT, 1, ["already has a returned for worker_ref", "no resumed since"]),
    ("resumed-while-round-open", [_res()], HEAD_TEXT, 1, ["has not returned since its last start", "(rule 9h)"]),
    ("resumed-on-closed-task", [_res()], _CLOSED_HEAD, 1, ["t-001 is already closed", "(rule 9h)"]),
    ("resumed-unknown-ref", [_ret(), _res(wref="agent:other")], HEAD_TEXT, 1,
     ["no earlier open delegated of t-001 carries worker_ref 'agent:other'", "(rule 9h)"]),
    ("two-workers-two-returned", [_line(event="delegated", ts="2026-07-10T08:10:00", agent="critic", model="opus",
                                        task_id="t-001", worker_ref="agent:crit", notes="critic entry"),
                                  _ret(), _ret(ts="2026-07-10T08:31:00", wref="agent:crit")], HEAD_TEXT, 0, []),
    ("returned-after-its-delegated-in-the-same-commit",
     [_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet", task_id="t-002", worker_ref="agent:new", notes="d"),
      _ret(ts="2026-07-10T08:20:00", tid="t-002", wref="agent:new")], HEAD_TEXT, 0, []),
    ("returned-before-its-delegated-never-opens-the-task",
     [_ret(tid="t-002", wref="agent:new"),
      _line(event="delegated", ts="2026-07-10T08:40:00", model="sonnet", task_id="t-002", worker_ref="agent:new", notes="d")],
     HEAD_TEXT, 1, ["t-002 has no delegated earlier in this journal"]),
    ("missing-worker-ref", [_ret(wref=None)], HEAD_TEXT, 1, ["'worker_ref' is required (non-empty string) for returned"]),
    ("blank-worker-ref", [_ret(wref="  ")], HEAD_TEXT, 1, ["'worker_ref' is required (non-empty string) for returned"]),
    ("missing-task-id", [_line(event="returned", ts="2026-07-10T08:30:00", model="sonnet", notes="n")], HEAD_TEXT, 1, ["'task_id'"]),
    ("missing-model", [_line(event="returned", ts="2026-07-10T08:30:00", task_id="t-001", notes="n")], HEAD_TEXT, 1,
     ["'model' is required for event=returned"]),
    ("a-returned-is-not-novelty-issuing-an-unseen-far-id-names-the-door-only",
     [_ret(tid="t-5000")], HEAD_TEXT, 1, ["t-5000 has no delegated earlier", _RETURNED_DOOR]),
]


@pytest.mark.parametrize("row,new,head,code_want,needles", RETURNED_ROWS, ids=[r[0] for r in RETURNED_ROWS])
def test_returned_rule_9f(row, new, head, code_want, needles):
    code, violations = _decide(head + "".join(l + "\n" for l in new), head, NOW)
    assert code == code_want, violations
    joined = "\n".join(violations)
    for needle in needles:
        assert needle in joined, (needle, violations)
    assert "task_id novelty" not in joined                      # a returned never goes through the id check


def test_a_returned_never_closes_or_reopens_a_task_the_critic_entry_and_the_accept_still_work():
    staged = _staged(
        _ret(),
        _line(event="delegated", ts="2026-07-10T08:40:00", agent="critic", model="opus", task_id="t-001",
              worker_ref="agent:crit", notes="critic entry after the builder returned"),
        _line(event="accepted", ts="2026-07-10T08:50:00", agent="builder", model="sonnet", task_id="t-001", by="opus",
              witness="w", notes="accept"))
    assert _decide(staged, HEAD_TEXT, NOW) == (0, [])
    # after the accept the task is closed: a returned is refused, a reopening delegated stays refused too
    code, violations = _decide(_staged(*(staged.splitlines()[1:])) + _ret(ts="2026-07-10T09:00:00") + "\n", HEAD_TEXT, NOW)
    assert code == 1 and any("t-001 is already closed" in v for v in violations)


def test_returned_is_in_the_event_set_and_the_required_field_sets():
    assert "returned" in jv.EVENTS
    for needed in (jv.MODEL_REQUIRED_EVENTS, jv.TASK_ID_REQUIRED_EVENTS):
        assert "returned" in needed
    assert "returned" not in {"delegated"}                       # novelty is `delegated` only (the loop reads that event)


# rule 20: `via` / `session` / `witness_by`: absent or null is never a violation, a present bad value is
@pytest.mark.parametrize("kw,named", [
    ({}, None), ({"via": None, "session": None, "witness_by": None}, None),
    ({"via": "hook"}, None), ({"via": "cli"}, None), ({"via": "Hook"}, "via"), ({"via": ""}, "via"), ({"via": 1}, "via"),
    ({"via": ["hook"]}, "via"),
    ({"session": "a" * 16}, None), ({"session": "a" * 17}, "session"), ({"session": ""}, "session"),
    ({"session": "ab cd"}, "session"), ({"session": "аbc"}, "session"), ({"session": 5}, "session"),
    ({"session": "x\n"}, "session"), ({"session": "a-B-9"}, None),
    ({"witness_by": "run"}, None), ({"witness_by": "file"}, None), ({"witness_by": "text"}, None),
    ({"witness_by": "RUN"}, "witness_by"), ({"witness_by": True}, "witness_by"), ({"witness_by": {"a": 1}}, "witness_by"),
])
def test_rule_20_optional_fields_are_judged_by_value(kw, named):
    code, violations = _decide(_staged(_line(event="dispatch_skipped", ts="2026-07-10T08:10:00", **kw)), HEAD_TEXT, NOW)
    if named is None:
        assert (code, violations) == (0, [])
    else:
        assert code == 1 and len(violations) == 1 and f"`{named}` = " in violations[0] and "(rule 20)" in violations[0], violations


# E-B0-1 on a NEW line: an id outside the read grammar is a form violation for every event that carries one
_BAD_IDS = ["t-123A", "t-123а", "t-１２３", "t-123abc", "t-12", "t-1234567890", "T-123", "t-123 ", "t-", ""]


@pytest.mark.parametrize("bad", _BAD_IDS, ids=[repr(b) for b in _BAD_IDS])
@pytest.mark.parametrize("event", ["delegated", "accepted", "returned"])
def test_e_b0_1_an_id_outside_the_read_grammar_is_a_form_violation_on_a_new_line(event, bad):
    extra = {"by": "opus", "witness": "w"} if event == "accepted" else {}
    code, violations = _decide(_staged(_line(event=event, ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
                                               task_id=bad, **extra)), HEAD_TEXT, NOW)
    assert code == 1 and violations
    if bad:
        assert any("does not match the t-NNN format (3-9 ASCII digits" in v for v in violations), violations
    assert not any("task_id novelty" in v for v in violations)          # never reaches the id check


# E-B0-5 TEMPORAL: old journals (bare ids, bands, <id>@<label>, legacy spellings) are state, never judged; the first
# new line after the switch with a gap is legal. Both worlds on ONE fixture.
def test_e_b0_5_an_old_journal_validates_as_before_and_the_first_new_line_may_leave_a_gap():
    old = [
        _line(event="delegated", ts="2026-07-10T07:00:00", task_id="t-001", model="sonnet"),
        _line(event="delegated", ts="2026-07-10T07:01:00", task_id="t-002", model="sonnet", id_band="t-100..t-149"),
        _line(event="delegated", ts="2026-07-10T07:02:00", task_id="t-100", model="sonnet", id_band="t-100..t-149"),
        _line(event="delegated", ts="2026-07-10T07:03:00", task_id="t-0123", model="sonnet"),             # legacy spelling
        _line(event="dispatch_skipped", ts="2026-07-10T07:04:00", notes="closes:t-002@dev2 closes:t-100"),
        _line(event="accepted", ts="2026-07-10T07:05:00", task_id="t-001", model="sonnet", by="opus", witness="w"),
        _line(event="delegated", ts="2026-07-10T07:06:00", task_id="t-9", model="sonnet"),                  # an old short id
    ]
    head = "".join(l + "\n" for l in old)
    # the old world: the head is never judged; an empty new tail is clean
    assert _decide(head, head, NOW) == (0, [])
    # the new world on the same head: a gap, an out-of-order id, a lettered id are legal (jump base: max(123, band top 149))
    new = [_line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-300", model="sonnet"),
           _line(event="delegated", ts="2026-07-10T08:01:00", task_id="t-250", model="sonnet"),
           _line(event="delegated", ts="2026-07-10T08:02:00", task_id="t-001a", model="sonnet")]
    assert _decide(head + "".join(l + "\n" for l in new), head, NOW) == (0, [])
    # ... and the band of the OLD lines is still the jump base: t-1149 is the cap (149 + 1000), t-1150 is refused
    ok = _line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-1149", model="sonnet")
    bad = _line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-1150", model="sonnet")
    assert _decide(head + ok + "\n", head, NOW) == (0, [])
    code, violations = _decide(head + bad + "\n", head, NOW)
    assert code == 1 and any("the highest t-NNN is 149" in v for v in violations)
    # a NEW line may not carry a band any more, the old ones stay readable
    code, violations = _decide(head + _line(event="delegated", ts="2026-07-10T08:00:00", task_id="t-301", model="sonnet",
                                              id_band="t-400..t-449") + "\n", head, NOW)
    assert code == 1 and any("band_retired" in v for v in violations)


def test_e_b0_5_the_live_dev1_journal_validates_with_no_new_violation():
    live = Path(__file__).resolve().parent.parent / "logs" / "journal" / "dev1.jsonl"
    if not live.exists():
        pytest.skip("the developer journal is not in this clone")
    text = live.read_text(encoding="utf-8")
    now = jv.datetime.datetime(2099, 1, 1)
    line = _line(event="delegated", ts="2098-12-31T00:00:00", task_id="t-1000001", model="sonnet")
    # the live journal as head (never judged) plus one far-above line: only the jump rule fires, nothing about the old lines
    code, violations = _decide(text + line + "\n", text, now)
    assert code == 1 and len(violations) == 1 and "jumps more than 1000" in violations[0]
    assert _decide(text, text, now) == (0, [])


# ---- B-2 (critic t-946): `--all --base <sha>` (CI; calibration check 6 (i)) prints the WARNs of the matrix; the exit code is never theirs ----

def _journal_lines(*objs):
    return "".join(l + "\n" for l in objs)


@pytest.mark.parametrize("cfg,by,worker,expect_warn", [
    (CFG_AFTER, "opus", ("scout", "agent:s"), True),                           # opus accepts a critic; no agent: worker of the critic
    (CFG_AFTER, "opus", ("critic", "agent:abc"), False),                       # its own agent: worker -- the empty outcome prints nothing
    (CFG_TODAY, "fable", ("scout", "agent:s"), True),                          # fable accepts a critic with no agent: worker of it
], ids=["after-no-worker", "after-agent-worker", "today-fable-no-worker"])
def test_all_base_prints_the_independent_context_warn(tmp_path, capsys, monkeypatch, cfg, by, worker, expect_warn):
    root = tmp_path
    _init_repo(root)
    (root / "delegation.config.yaml").write_text(cfg, encoding="utf-8")
    (root / "logs" / "journal").mkdir(parents=True)
    journal = root / "logs" / "journal" / "dev1.jsonl"
    created = _line(event="journal_created", ts="2026-07-10T07:00:00", agent="lead", category="admin", notes="start")
    journal.write_text(created + "\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    base = _git(root, "rev-parse", "HEAD").stdout.strip()
    new = [_line(event="delegated", ts="2026-07-10T08:00:00", agent=worker[0], model="opus", task_id="t-001",
                 worker_ref=worker[1], notes="a worker of the task"),
           _line(event="accepted", ts="2026-07-10T08:10:00", agent="critic", model="opus", task_id="t-001", by=by,
                 notes="accepted")]
    journal.write_text("".join(l + "\n" for l in [created, *new]), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "head")
    monkeypatch.chdir(root)
    monkeypatch.setattr(jv, "_CONFIG_ROOTS", {})
    assert jv.main(["--all", "--base", base]) == 0                            # a WARN never changes the exit code
    err = capsys.readouterr().err
    assert ("INDEPENDENT CONTEXT" in err) is expect_warn, err


@pytest.mark.parametrize("path", ["merge", "all"])
def test_order_known_token_warn_on_every_path(path):
    staged = _staged(_id_bad(), _tok("09:00:00", "10:30:00", "order-known: nothing"))
    assert any("nothing after the colon" in w for w in _order_known_warns(path, staged))
