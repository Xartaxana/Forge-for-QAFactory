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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0
    assert violations == []


# ---- 1. append-only ----

def test_append_only_violation_when_existing_line_modified():
    tampered_head = json.loads(HEAD_LINE)
    tampered_head["notes"] = "rewritten"
    staged = json.dumps(tampered_head, ensure_ascii=False) + "\n"
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("append-only" in v for v in violations)


def test_append_only_violation_when_lines_removed():
    code, violations = jv.decide("", HEAD_TEXT, NOW)
    assert code == 1
    assert any("append-only" in v for v in violations)


# ---- 2. required fields ----

def test_missing_required_field_notes_fails():
    obj = json.loads(_line(event="dispatch_skipped", ts="2026-07-10T08:10:00",
                            agent="scout", category="recon", notes="x"))
    del obj["notes"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("notes" in v for v in violations)


def test_invalid_json_line_fails():
    staged = HEAD_TEXT + "{not valid json\n"
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("invalid JSON" in v for v in violations)


# ---- 3. event enum ----

def test_unknown_event_fails():
    staged = _staged(_line(event="reticulated", ts="2026-07-10T08:10:00", agent="lead",
                            category="x", notes="x"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert len(violations) == 1 and named in violations[0], violations
    code2, violations2, _w = jv.decide_with_warnings(staged, HEAD_TEXT, NOW)
    assert code2 == 1 and violations2 == violations


# ---- 4. model required ----

def test_model_missing_for_delegated_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-002",
                            notes="no model"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'model'" in v for v in violations)


# ---- 5. task_id required + format ----

def test_task_id_missing_for_delegated_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            notes="no task_id"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'task_id'" in v for v in violations)


def test_task_id_bad_format_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-2", notes="bad format"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("t-NNN format" in v for v in violations)


# ---- 5b. worker_ref required for delegated ----

def test_delegated_missing_worker_ref_fails():
    obj = json.loads(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="no worker_ref"))
    del obj["worker_ref"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_empty_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="", notes="empty worker_ref"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_whitespace_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="   ", notes="whitespace worker_ref"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_nonstring_worker_ref_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref=123, notes="nonstring worker_ref"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("worker_ref" in v for v in violations)


def test_delegated_valid_worker_ref_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", worker_ref="cli:2026-07-10T08:10:00",
                            notes="valid worker_ref"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_escalated_needs_no_worker_ref():
    obj = json.loads(_line(event="escalated", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", notes="escalated, no worker_ref"))
    del obj["worker_ref"]
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 6. rejected: attempt / failure_class ----

def test_rejected_invalid_attempt_and_failure_class_fail():
    staged = _staged(_line(event="rejected", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", attempt=0,
                            failure_class="mystery", by="opus", notes="bad rejected"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'attempt'" in v for v in violations)
    assert any("'failure_class'" in v for v in violations)


# ---- 7. accepted + agent=builder: witness ----

def test_accepted_builder_missing_witness_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", by="opus",
                            notes="no witness"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'witness'" in v for v in violations)


# ---- 8. defect_found: ref ----

def test_defect_found_missing_ref_fails():
    staged = _staged(_line(event="defect_found", ts="2026-07-10T08:10:00", agent="builder",
                            task_id="t-001", notes="late defect"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'ref'" in v for v in violations)


# ---- 9. task_id novelty / reference ----

def test_delegated_novelty_violation_wrong_number():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-005", notes="skipped ahead"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("task_id novelty" in v for v in violations)


def test_delegated_novelty_correct_max_plus_one_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="correct next id"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_accepted_references_nonexistent_task_id_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-099", witness="w", by="opus",
                            notes="dangling ref"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 9 (Lead correction, live precedent): re-delegated task_id --
# a/b/v legal, two g negatives (a real duplicate-delegation defect once
# found in a production journal; delegated after accepted) ----

def test_9a_new_task_max_plus_one_passes():
    # (a) restated for clarity alongside b/v/g below: a brand-new task_id
    # equal to max+1 is legal regardless of any b/v/g machinery.
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", model="sonnet",
                            task_id="t-002", notes="new task, case a"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9g_duplicate_pattern_same_agent_no_attempt_no_rejected_fails():
    # (g) negative #1: an actual defect once found in a production
    # journal -- same agent re-delegated
    # on an open task_id, no attempt field, no rejected above. Must FAIL.
    staged = _staged(_line(event="delegated", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", notes="duplicate delegation, no attempt/rejected"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9c2_replaces_worker_fabricated_handle_fails():
    # The claimed handle does not match ANY earlier delegated
    # worker_ref for this task_id -- a fabricated replacement, FAIL.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", worker_ref="cli:2026-07-10T08:10:00",
              notes="replaces_worker:cli:2026-07-10T07:00:00 (never happened)")
    )
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_9c2_replaces_worker_takes_priority_over_plain_duplicate_fail():
    # Sanity: without the marker, the same shape of line fails as a
    # plain duplicate (case d) -- proves the c2 test above is actually
    # exercising the marker branch, not some other path to a pass.
    staged = _staged(
        _line(event="delegated", ts="2026-07-10T08:10:00", agent="builder", model="sonnet",
              task_id="t-001", notes="no replaces_worker marker here at all")
    )
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, head_with_accept, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("not monotonic" in v for v in violations)


def test_ts_earlier_than_last_head_line_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-10T07:00:00", model="sonnet",
                            task_id="t-002", notes="before HEAD's last ts"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("not monotonic" in v for v in violations)


def test_ts_narrative_future_beyond_now_plus_10min_fails():
    staged = _staged(_line(event="delegated", ts="2026-07-11T00:00:00", model="sonnet",
                            task_id="t-002", notes="far future (narrative-future timestamp)"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("later than now+10min" in v and "narrated" in v for v in violations)


def test_ts_within_10min_future_grace_passes():
    staged = _staged(_line(event="delegated", ts="2026-07-10T12:05:00", model="sonnet",
                            task_id="t-002", notes="clock skew grace"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- 11. role-vs-tier acceptance matrix ----

def test_matrix_missing_by_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", witness="w",
                            notes="no by field"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("'by'" in v for v in violations)


def test_matrix_scout_accepted_by_same_tier_without_basis_fails():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku",
                            notes="peer accepting peer, no basis"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations)


def test_matrix_scout_accepted_by_higher_tier_passes():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="opus",
                            notes="opus accepts scout"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_matrix_scout_accepted_same_tier_with_basis_now_fails_below_sonnet_floor():
    # CORRECTED: this used to assert code==0 under an old, bare membership
    # check ("basis in BASIS_VALUES", no by/agent pair check) -- the exact
    # class of hole a live leak exposed (queued-to-lead passing membership
    # regardless of WHICH by/agent). by="haiku" is a KNOWN tier strictly
    # below sonnet -- "Role != tier"
    # matrix: "below Sonnet: no coordination is provided for" -- no basis
    # rescues it now.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku", basis="queued-to-lead",
                            notes="basis fallback -- now illegal, by below sonnet"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations)


def test_matrix_model_id_in_by_fails_as_unknown_tier():
    # RENAMED (a critic verdict): the old names/claims here were stale.
    # (a) test_matrix_non_claude_by_with_basis_critic_passes asserted
    # code==0 for a full model id in "by" with basis="critic" -- that was
    # EXACTLY the hole this revision closes, and became a
    # verbatim duplicate of the sibling by=sonnet/agent=builder/
    # basis=critic pair-legality case elsewhere in this file
    # once "by" was corrected to a legal tier word -- deleted, no
    # information lost. (b) this test (test_matrix_non_claude_by_requires_basis)
    # asserted "requires basis" as if that were still a distinct rule --
    # it is not: a full model id in "by" is now simply an UNKNOWN-TIER
    # value, and fails identically WITH or WITHOUT basis (the enum gate
    # runs before any basis is even inspected). A model id belongs in
    # "model", never in "by" -- "by" is always a bare TIER_ORDER keyword,
    # even for non-Claude workers.
    staged_no_basis = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                                     model="sonnet", task_id="t-001", witness="w",
                                     by="gemini-2.5-flash",
                                     notes="model id in by, no basis -- unknown tier, not 'requires basis'"))
    code, violations = jv.decide(staged_no_basis, HEAD_TEXT, NOW)
    assert code == 1
    assert any("is not a known tier" in v for v in violations), violations

    staged_critic_basis = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                                         model="sonnet", task_id="t-001", witness="w",
                                         by="gemini-2.5-flash", basis="critic",
                                         notes="model id in by, critic basis -- still unknown tier, still fails"))
    code, violations = jv.decide(staged_critic_basis, HEAD_TEXT, NOW)
    assert code == 1
    assert any("is not a known tier" in v for v in violations), violations


# ---- an unknown "by" fails the role-vs-tier matrix UNCONDITIONALLY --
# a "by" outside TIER_ORDER is never legalized by any basis, including
# "judge"; the enum/shape check runs BEFORE every branch of
# _matrix_d0058_violation. ----

def test_unknown_by_fails_even_with_critic_basis():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="banana",
                            basis="critic", notes="unknown by, critic basis -- must fail"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("is not a known tier" in v and "banana" in v for v in violations), violations


def test_unknown_by_case_sensitive_fails_not_via_queued_to_lead_branch():
    # "Sonnet" (capitalized) is NOT the same key as "sonnet" in
    # TIER_ORDER -- case sensitivity is part of the enum check itself,
    # not a separate rule; must fail via the unknown-by branch, not
    # the queued-to-lead pair-message (rule e).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="Sonnet", basis="queued-to-lead",
                            notes="capitalized by -- unknown tier, not the legal 'sonnet'"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("is not a known tier" in v for v in violations), violations
    assert not any("queued-to-lead" in v for v in violations), violations


def test_unknown_by_fails_before_judge_branch_even_on_leaf_category():
    # the enum/shape check runs BEFORE basis=="judge" is even inspected
    # -- an unknown by fails even on a leaf-class category, where judge
    # would otherwise be by-independent.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="banana",
                            basis="judge", category="implementation",
                            notes="unknown by, judge basis, leaf category -- still fails"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("is not a known tier" in v for v in violations), violations
    assert not any("leaf-class dispatch" in v for v in violations), violations


def test_boundary_fable_known_tier_still_passes_via_ok_tier():
    obj = json.loads(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="fable",
                            notes="fable is a KNOWN tier -- ok_tier unaffected"))
    assert "basis" not in obj
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_boundary_haiku_known_tier_floor_message_unchanged():
    # regression pin: "haiku" IS a known tier (present in TIER_ORDER) --
    # the unknown-by branch must NOT fire for it; the pre-existing
    # floor message (rule c) still names it, byte-for-byte unchanged.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="haiku",
                            basis="critic", notes="known tier below sonnet -- floor, not the new branch"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("tier below sonnet" in v for v in violations), violations
    assert not any("is not a known tier" in v for v in violations), violations


# ---- role-vs-tier pair-legality table --
# membership-in-set replaced by legality-per-(by, agent)-pair, after a
# live leak (two different sonnet-tier coordinators accepted sonnet-class
# (builder) results via basis=queued-to-lead -- the validator at the
# time checked basis only by set membership). ----

def test_pair_sonnet_by_builder_agent_critic_basis_ok():
    # (1) by=sonnet/agent=builder/basis=critic -> OK (critic-tier opus is
    # strictly above builder-tier sonnet).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="sonnet",
                            basis="critic", notes="case 1: builder accepted by sonnet with critic basis"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_pair_sonnet_by_builder_agent_queued_to_lead_fails():
    # (2) by=sonnet/agent=builder/basis=queued-to-lead -> FAIL -- a
    # sonnet-tier coordinator accepting a sonnet-class (builder) result
    # via the "queued-to-lead" escape hatch, which the matrix reserves
    # for critic-class work only.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="sonnet",
                            basis="queued-to-lead",
                            notes="case 2: builder accepted by sonnet via queued-to-lead"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v and "queued-to-lead" in v and "builder" in v and "sonnet" in v
               for v in violations), violations


def test_pair_sonnet_by_critic_agent_queued_to_lead_ok():
    # (3) by=sonnet/agent=critic/basis=queued-to-lead -> OK (critic-class
    # work queued to the Lead through a sonnet coordinator is legal).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="sonnet", basis="queued-to-lead",
                            notes="case 3: critic accepted by sonnet via queued-to-lead"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_pair_opus_by_critic_agent_queued_to_lead_ok():
    # (4) by=opus/agent=critic/basis=queued-to-lead -> OK (equal tier,
    # the matrix explicitly allows the queue for critic-class work at an
    # opus coordinator).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="opus", basis="queued-to-lead",
                            notes="pair case 4: critic accepted by opus via queued-to-lead"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_pair_opus_by_builder_agent_no_basis_ok_via_ok_tier():
    # (5) by=opus/agent=builder, no basis at all -> OK (ok_tier: opus
    # strictly above builder-tier sonnet -- no basis needed).
    obj = json.loads(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="opus",
                            notes="pair case 5: builder accepted by opus, no basis, ok_tier"))
    assert "basis" not in obj
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_pair_haiku_by_scout_agent_critic_basis_decision_fork_fails():
    # (6) by=haiku/agent=scout/basis=critic -- THE decision fork named in
    # the dispatch: the core rule's literal text ("OR the decision
    # carries a higher tier's input (a critic verdict)") would read this
    # as legal (critic-tier opus IS strictly above scout-tier haiku,
    # satisfying the basis="critic" rule in isolation). But the Role !=
    # tier matrix's "below Sonnet" row says, without exception, "no
    # coordination is provided for" -- a haiku-tier session is not a
    # functioning coordinator at all in this structure, regardless of
    # what verdict got attached to its acceptance event. DECISION
    # (documented per the dispatch's explicit instruction not to resolve
    # this silently): the floor wins -- FAIL. Both quotes:
    #   core: "the decision carries a higher tier's input (a critic
    #   verdict)"
    #   matrix: "| below Sonnet | no coordination is provided for | -- |"
    # Implemented as the FLOOR (checked before the basis=="critic"
    # branch) so it takes precedence for any by with a KNOWN tier
    # strictly below sonnet -- i.e. by=="haiku" specifically. basis==
    # "judge" is the one carve-out (checked first, unaffected by this
    # floor -- t-276/toolkit-native leaf-judge pairs with by=haiku remain
    # legal, see test_matrix_judge_basis_passes_on_recon_category above).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku", basis="critic",
                            notes="pair case 6 (decision fork): scout accepted by haiku with critic basis"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v and "haiku" in v for v in violations), violations


def test_pair_boundary_fable_by_critic_agent_ok_via_ok_tier_no_basis_needed():
    # boundary companion to case 5/e: by=fable/agent=critic needs no
    # basis at all -- ok_tier alone covers it (fable strictly above opus).
    obj = json.loads(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="fable",
                            notes="fable accepts critic, no basis, ok_tier"))
    assert "basis" not in obj
    staged = _staged(json.dumps(obj, ensure_ascii=False))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_pair_boundary_sonnet_by_critic_agent_no_basis_fails():
    # boundary companion to case 3: SAME pair (by=sonnet, agent=critic)
    # WITHOUT queued-to-lead -- must still FAIL (equal tier, no rescuing
    # basis at all).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="sonnet",
                            notes="critic accepted by sonnet, no basis at all"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations), violations


def test_pair_boundary_haiku_by_builder_agent_queued_to_lead_fails_floor():
    # boundary: by=haiku (known tier below sonnet) with agent=builder and
    # basis=queued-to-lead -- the floor fires before the queued-to-lead
    # branch is even reached; message must name the floor, not the
    # generic queued-to-lead pair message.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="haiku",
                            basis="queued-to-lead",
                            notes="builder accepted by haiku via queued-to-lead -- floor, not pair message"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("tier below sonnet" in v for v in violations), violations


def test_pair_boundary_haiku_by_judge_basis_leaf_still_passes_unaffected_by_floor():
    # boundary: by=haiku with basis=judge on a leaf category is NOT
    # touched by the new floor -- judge is checked first, independent of
    # by's tier (calibrated-judge acceptance is not a coordinator-tier
    # resolution at all). Regression lock alongside
    # test_matrix_judge_basis_passes_on_recon_category.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku", basis="judge",
                            category="recon", notes="judge on leaf, by=haiku -- floor does not apply"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_agent_lead_needs_only_presence_of_by():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="lead",
                            model="fable", task_id="t-001", by="haiku",
                            notes="lead-tier accept, matrix not applied"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


def test_matrix_rejected_only_needs_by_present_no_tier_check():
    # literal reading of the spec: tier/basis check text only names
    # "accepted"; rejected carries 'by' without a further tier/basis gate.
    staged = _staged(_line(event="rejected", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", attempt=1, failure_class="recon",
                            by="haiku", notes="rejected, same-tier by, no basis"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0


# ---- designer tier addendum (AGENT_TIER += "designer": "opus"):
# designer's deployment binding is opus (.claude/agents/designer.md),
# same tier as critic. ----

def test_matrix_designer_accepted_by_fable_passes():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                            model="opus", task_id="t-001", by="fable",
                            notes="fable accepts designer's draft"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_designer_accepted_by_opus_without_basis_fails_equal_tier():
    # designer's own tier is opus (same as critic) -- an equal-tier
    # acceptance with no basis at all must still fail the matrix, same
    # class as test_matrix_scout_accepted_by_same_tier_without_basis_fails
    # above.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                            model="opus", task_id="t-001", by="opus",
                            notes="peer accepting peer, no basis"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations), violations


def test_matrix_agent_outside_agent_tier_regression_pin():
    # Regression pin: an agent name OUTSIDE AGENT_TIER (e.g. "analyst")
    # is documented, pre-existing behavior -- the matrix is simply not
    # defined for it (return None before any branch), unchanged by the
    # designer addition above.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="analyst",
                            model="haiku", task_id="t-001", by="haiku",
                            notes="agent outside AGENT_TIER -- matrix not applied"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


# ---- branch (5) queued-to-lead generalized to the upper-mid-tier CLASS
# (QUEUED_TO_LEAD_AGENTS = {critic, designer}), not the literal name
# "critic"; branch (1) judge narrowed to agent in {scout, builder} (a
# critic finding: designer+judge+category=implementation used to pass
# wrongly, since only category was checked, not agent). ----

def test_matrix_designer_by_opus_queued_to_lead_passes():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                            model="opus", task_id="t-001", by="opus", basis="queued-to-lead",
                            notes="designer queued to Lead via an opus coordinator"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_designer_by_sonnet_queued_to_lead_passes():
    # the queue is legal from ANY coordinator tier not above designer's
    # own (sonnet here) -- same class as the existing critic/sonnet case.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                            model="opus", task_id="t-001", by="sonnet", basis="queued-to-lead",
                            notes="designer queued to Lead via a sonnet coordinator"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_designer_by_opus_critic_basis_fails():
    # basis="critic" does NOT rescue designer -- critic (opus) is not
    # strictly above designer's own opus tier, same as it doesn't
    # rescue agent="critic" itself.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                            model="opus", task_id="t-001", by="opus", basis="critic",
                            notes="designer accepted by opus via critic basis -- must fail"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v and "designer" in v for v in violations), violations
    # the fixed message names the ACTUAL agent and the actually-legal
    # path -- no stale advice about a literal agent='critic' path.
    assert not any("agent='critic'" in v for v in violations), violations


def test_matrix_designer_judge_basis_fails_regardless_of_category():
    for category in ("recon", "implementation", "review", None):
        kw = {} if category is None else {"category": category}
        staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="designer",
                                model="opus", task_id="t-001", by="opus", basis="judge",
                                notes="designer via judge -- must fail regardless of category",
                                **kw))
        code, violations = jv.decide(staged, HEAD_TEXT, NOW)
        assert code == 1, (category, violations)


def test_matrix_builder_judge_basis_implementation_still_passes_not_broken():
    # regression pin: the narrowing to agent in {scout, builder} must
    # not break the existing builder+judge+leaf-category path.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", witness="w", by="sonnet",
                            basis="judge", category="implementation",
                            notes="builder via judge on implementation -- still legal"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_scout_judge_basis_recon_still_passes_not_broken():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku",
                            basis="judge", category="recon",
                            notes="scout via judge on recon -- still legal"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_critic_judge_basis_leaf_category_now_fails():
    # a critic finding, adjacent surface: agent="critic" itself is ALSO
    # excluded from judge acceptance now (the review/spec class, not
    # just designer) -- even on an otherwise-leaf category.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="critic",
                            model="opus", task_id="t-001", by="opus",
                            basis="judge", category="implementation",
                            notes="critic via judge on implementation -- now fails"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1, violations


# ---- 11b. basis "judge" -- legal ONLY on a leaf-class dispatch
# (category recon/implementation; this toolkit's own CLAUDE.md "Leaf
# routing" section -- see the module docstring's rule 11 NOTE for the
# empirical finding that the reference validator does not itself gate
# this, despite documenting the restriction). ----


def test_matrix_judge_basis_passes_on_recon_category():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="scout",
                            model="haiku", task_id="t-001", by="haiku", basis="judge",
                            category="recon", notes="judge accepts a recon leaf"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_judge_basis_passes_on_implementation_category():
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", by="sonnet", basis="judge",
                            category="implementation", witness="w",
                            notes="judge accepts an implementation leaf"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 0, violations


def test_matrix_judge_basis_fails_on_non_leaf_category():
    # boundary: "judge" is a KNOWN basis value, but the category on
    # THIS line is neither "recon" nor "implementation" -- must still
    # fail (a graph/review/mechanism-class dispatch is never
    # judge-acceptable).
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", by="sonnet", basis="judge",
                            category="review", witness="w",
                            notes="judge basis on a non-leaf category must fail"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations)


def test_matrix_judge_basis_fails_when_category_missing():
    # a missing/invalid category is caught as its own separate form
    # defect (rule 2), but it must ALSO fail the leaf-class judge check
    # (category not in LEAF_CATEGORIES) rather than being silently
    # treated as a leaf by default.
    staged = _staged(_line(event="accepted", ts="2026-07-10T08:10:00", agent="builder",
                            model="sonnet", task_id="t-001", by="sonnet", basis="judge",
                            category="", witness="w",
                            notes="judge basis with an empty category must fail"))
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1
    assert any("role-vs-tier" in v for v in violations)


# ---- B-401: the form checks were moved into _line_form_violations; the order of the texts of one
# line is part of the contract (K-B: the non-merge list is byte-identical to what it was) ----

def test_one_line_with_three_defects_gives_the_exact_ordered_list():
    obj = json.loads(_line(event="delegated", ts="2026-07-10T08:10:00Z", model="sonnet", task_id="t-002",
                           notes="three defects"))
    del obj["model"], obj["worker_ref"]
    code, violations = jv.decide(_staged(json.dumps(obj, ensure_ascii=False)), HEAD_TEXT, NOW)
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
    code, violations = jv.decide(head + retry + "\n", head, NOW)
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
    code, violations = jv.decide(staged, "", NOW)
    assert code == 0


def test_empty_head_no_lower_ts_bound():
    staged = _line(event="delegated", ts="2020-01-01T00:00:00", model="sonnet", task_id="t-001",
                   notes="old ts, no HEAD to compare against") + "\n"
    code, violations = jv.decide(staged, "", NOW)
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
    bad_line = _line(event="delegated", ts="2026-07-10T08:10:00", task_id="t-999", model="sonnet",
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
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
    return jv.decide(_jtext(*objs), head, _NOW8, seed_text=seed)


def test_k8_the_next_id_is_the_max_of_the_history_plus_one_and_only_that():
    ok = _k8(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00"))
    assert ok == (0, [])
    for wrong in ("t-002", "t-004", "t-009"):                # +0 (a repeat of an open task), +2 and beyond
        code, violations = _k8(M_CREATED, _deleg(wrong, "2026-10-02T08:30:00"))
        assert code == 1 and violations, wrong
    code, violations = _k8(M_CREATED, _deleg("t-004", "2026-10-02T08:30:00"))
    assert any("got t-004; the next new id is t-003" in v for v in violations)
    code, violations = _k8(M_CREATED, _deleg("t-001", "2026-10-02T08:30:00"))
    assert any("CLOSED task" in v for v in violations)      # t-001 is accepted in the history


def test_k8_without_the_seed_the_same_file_starts_at_t_001():
    code, violations = _k8(M_CREATED, _deleg("t-003", "2026-10-02T08:30:00"), seed=None)
    assert code == 1 and any("got t-003; the next new id is t-001" in v for v in violations)
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
    code, violations = _k8(M_CREATED, _deleg("t-009", "2026-10-02T08:30:00"))
    assert code == 1 and violations[0].startswith("line 2 ")


def test_k8_an_empty_developer_file_passes_and_has_no_line_1_to_check():
    assert jv.decide("", None, _NOW8) == (0, [])
    assert jv.decide("", None, _NOW8, seed_text=HISTORY_TEXT) == (0, [])
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


# ================================ id bands (F6-58, rule 9e): rows j1-j18 ================================
# A spec is ("d", id[, band]) for a delegated line or ("x", None[, band]) for a decomposable line that carries only a
# band; a 3rd element, even None, writes the `id_band` field. HEAD specs are state (never judged), NEW specs are judged.

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


_B450 = ("d", "t-450", "t-450..t-499")
_J1 = [_B450, ("d", "t-357"), ("d", "t-451", "t-450..t-499"), ("d", "t-358")]   # every band line carries its band
_FILLED_400 = [("x", None, "t-400..t-449")] + _ids(341, 399) + [("d", "t-400", "t-400..t-449")]
_DOOR_451 = 't-451 lies in the id band t-450..t-499 of another writer; a line issued from a band carries "id_band":"t-450..t-499"'
_EDGE_400 = [("d", "t-340"), ("x", None, "t-400..t-449")] + _ids(341, 399)
_HUGE = "t-" + "9" * 5000 + ".."
_FORM_VALUES = ["t-5..t-9", "500..", "t-500 .. t-510", "t-500–t-510", "", ["t-1"], {"from": "t-1"}, 500,
                "t-４００..t-４４９", "t-1234567890..", _HUGE]

# (row, head specs, new specs, needles that must ALL appear in the violations; () = no violation at all)
ID_BAND_ROWS = [
    ("j1", [("d", "t-356")], _J1, ()),
    ("j2", [("d", "t-356")], _J1 + [("d", "t-455", "t-450..t-499")],
     ("task_id novelty violated", "got t-455", "t-452 (band t-450..t-499)")),
    # F1 (t-402): a band's next id is issuable only by a line that carries that band in its own id_band
    ("S1-naive-max-plus-1", [("d", "t-356")], [_B450, ("d", "t-451")],
     ("task_id novelty violated", "got t-451", "the next new id is t-357", _DOOR_451)),
    ("S1-band-owner-with-field", [("d", "t-356")], [_B450, ("d", "t-451", "t-450..t-499")], ()),
    ("P10-plain-id-at-a-band-first-id", [("d", "t-356"), ("x", None, "t-500..t-549")], [("d", "t-500")],
     ("got t-500", "the next new id is t-357",
      't-500 lies in the id band t-500..t-549 of another writer; a line issued from a band carries "id_band":"t-500..t-549"')),
    ("edge-main-at-a-band-edge-takes-the-next-after-it", _EDGE_400, [("d", "t-450")], ()),
    ("edge-main-at-a-band-edge-plain-first-id-refused", _EDGE_400, [("d", "t-400")],
     ("got t-400", "the next new id is t-450", "t-400 lies in the id band t-400..t-449")),
    ("band-never-declared-opens-on-its-own-line-and-its-id-is-judged", [("d", "t-356")], [("d", "t-455", "t-450..t-499")],
     ("got t-455", "or t-450 (band t-450..t-499)")),
    ("a-line-carries-another-bands-field", [("d", "t-356"), _B450, ("x", None, "t-600..t-649")],
     [("d", "t-600", "t-450..t-499")], ("got t-600", "lies in the id band t-600..t-649")),
    ("a-band-line-without-a-new-id-needs-no-field-for-9d", [("d", "t-356"), _B450], [("d", "t-450")],
     ("repeated delegated by the same agent",)),
    ("j3", [("d", "t-356")], [("x", None, "t-300..t-310")], ("starts at or below t-356", "start it at t-450", "(rule 9e)")),
    ("j4", [("d", "t-356"), _B450], [("x", None, "t-470..t-480")], ("starts at or below t-499", "start it at t-550")),
    ("j5a-jump", [("d", "t-356")], [("x", None, "t-999999999..")], ("starts 999999643 ids above t-356", "at most 10000")),
    ("j5a-nine-digits-parse", [("d", "t-999999000")], [("x", None, "t-999999100..")], ()),
    ("j6", [("d", "t-356")], [("x", None, "t-500..t-499")], ("ends below its start", "(rule 9e)")),
    ("j7-1000", [("d", "t-356")], [("x", None, "t-500..t-1499")], ()),
    ("j7-1001", [("d", "t-356")], [("x", None, "t-500..t-1500")], ("holds 1001 ids", "at most 1000")),
    ("j8-pass", [("d", "t-433")], [("x", None, "t-500.."), ("d", "t-500")], ()),
    ("j8-novelty", [("d", "t-433")], [("x", None, "t-500.."), ("d", "t-500"), ("d", "t-434")],
     ("task_id novelty violated", "got t-434", "the next new id is t-501")),
    ("j9-10000", [("d", "t-100")], [("x", None, "t-10100..")], ()),
    ("j9-10001", [("d", "t-100")], [("x", None, "t-10101..")], ("starts 10001 ids above t-100", "start it nearer, at t-150")),
    ("j10-pass", [("d", "t-340")], _FILLED_400 + [("d", "t-450")], ()),
    ("j10-skip-in-band", [("d", "t-340")], _FILLED_400 + [("d", "t-402")],
     ("got t-402", "the next new id is t-450", "or t-401 (band t-400..t-449)")),
    ("j10-skip-in-band-with-field", [("d", "t-340")], _FILLED_400 + [("d", "t-402", "t-400..t-449")],
     ("got t-402", "or t-401 (band t-400..t-449)")),
    ("j10-reuse",[("d", "t-340")], _FILLED_400 + [("d", "t-400")], ("repeated delegated by the same agent",)),
    ("j11", [("d", "t-340")],
     [("x", None, "t-400..t-402")] + _ids(341, 360) + [("d", f"t-{n}", "t-400..t-402") for n in (400, 401, 402)] + [("d", "t-403")],
     ("got t-403", "the next new id is t-361", "band t-400..t-402 is used up -- open a new band at t-500")),
    ("j12", [("d", "t-356", "junk")], [("d", "t-357")], ()),
    ("j13", [("d", "t-356")], [("x", None, None), ("d", "t-357", None)], ()),
    ("j15-near", [("d", "t-356")], [("x", None, "t-405..t-410")], ("starts 49 ids above t-356", "at least 50", "start it at t-450")),
    ("j15-gap-50", [("d", "t-356")], [("x", None, "t-406..t-410")], ()),
    ("j16", [("d", "t-356")], [("x", None, "t-357.."), ("d", "t-357")], ()),
    ("j17", [("d", "t-356")], [("d", "t-300", "t-300..t-310")],
     ("starts at or below t-356", "task_id novelty violated", "got t-300")),
    ("j18", [("d", "t-356")], [("x", None, "t-450..t-499"), ("d", "t-450", "t-450..t-499")], ()),
    ("j14-no-band-old-reading", [("d", "t-356")], [("d", "t-357"), ("d", "t-358")], ()),
    ("j14-no-band-gap", [("d", "t-356")], [("d", "t-358")], ("got t-358", "the next new id is t-357")),
] + [(f"j5-form-{i}", [("d", "t-356")], [("x", None, v)], ("is not \"t-A..t-B\"", "(rule 9e)"))
     for i, v in enumerate(_FORM_VALUES)]


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
    if row.startswith("j5-form"):
        assert len(violations) == 1 and "id_band" in violations[0]       # one text per bad value, nothing raised


def test_id_band_a_refused_band_never_enters_the_state_and_a_foreign_bad_band_is_clearable():
    # the refused band of j17 does not make t-301 issuable on the next line either
    v = _band_run([("d", "t-356")], [("x", None, "t-300..t-310"), ("d", "t-300")])
    assert any("task_id novelty violated" in x and "got t-300" in x for x in v)
    assert "id_band" in jv.FORM_FIELDS
    assert [f for f, _t in jv._line_form_violations(json.loads(_line(id_band="junk", event="decomposable")), "T")] == ["id_band"]
    assert jv._line_form_violations(json.loads(_line(event="decomposable", id_band=None)), "T") == []


# ---- rule 19 (FG7-32): the order-known door, ONE table ----
# HEAD holds t-001 @08:00. Each case is (new lines, seed_text, expected code, [texts the violations must hold],
# [texts the WARN list must hold], declared count). The defects: an id out of order (t-005, next is t-002), a ts
# earlier than HEAD's last line, a repeated delegated by one agent with no attempt.
_D = "2026-07-10T"


def _tok(ts, at, notes=None):
    return _line(event="dispatch_skipped", ts=_D + at, notes=notes or f"order-known:{_D}{ts}")


def _id_bad(ts="09:00:00", tid="t-005", **kw):
    return _line(task_id=tid, model="sonnet", ts=_D + ts, **kw)


_TS_BAD = _line(task_id="t-002", model="sonnet", ts=_D + "07:00:00")
_DUP_OK = _line(task_id="t-002", model="sonnet", ts=_D + "09:00:00")
_DUP_BAD = _line(task_id="t-002", model="sonnet", ts=_D + "10:00:00")
_DEFECTS = {
    "id": ([_id_bad()], "09:00:00", "t-005", "10:30:00"),
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
    [_id_bad(), _id_bad(tid="t-009"), _tok("09:00:00", "10:30:00")], None, 0, [], [], 2)
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
