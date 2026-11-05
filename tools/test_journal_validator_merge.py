"""Tests for the MERGE MODE of the routing-journal validator (t-430): decide_merge() and the
MERGE_HEAD branch of _main(). decide_merge() is a pure function, tested with synthetic text; two
cases at the bottom run _main() against a real temp git repo whose conflicted merge is being
concluded.

TEMPORAL: until the Lead places the proposed module on the live path, the code under test is
tools/journal_validator.proposed.py (loaded by path); once that file is gone, the live module
journal_validator is imported. Both worlds must pass.

Run from the repo root: python -m pytest tools/test_journal_validator_merge.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest

import journal_keys as jk

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
_REAL_IS_DECL, _REAL_GET_DECL = jv.is_declaration_staged, jv.get_staged_declaration   # before the autouse stubs

NOW = jv.datetime.datetime(2026, 7, 10, 12, 0, 0)


def _obj(event="delegated", ts="2026-07-10T08:00:00", agent="builder",
         category="implementation", notes="note", worker_ref="cli:x", **kw) -> dict:
    d = {"ts": ts, "event": event, "agent": agent, "category": category, "notes": notes,
         "worker_ref": worker_ref}
    d.update(kw)
    return d


def _dump(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _text(*lines: str) -> str:
    return "".join(l + "\n" for l in lines)


# The base line both clones hold; then each clone's own tail. Both clones issued t-002 for
# different work (the measured case: ids t-014..t-077 on both sides).
B1 = _dump(_obj(task_id="t-001", model="sonnet", ts="2026-07-10T08:00:00"))
H1 = _dump(_obj(task_id="t-002", model="sonnet", ts="2026-07-10T10:00:00", notes="head t-002"))
H2 = _dump(_obj(event="accepted", task_id="t-002", model="sonnet", by="opus",
                witness="pytest ... passed", ts="2026-07-10T10:05:00", notes="head accepted t-002"))
O1 = _dump(_obj(agent="scout", category="recon", task_id="t-002", model="haiku",
                ts="2026-07-10T09:00:00", notes="other t-002, a different task"))
O2 = _dump(_obj(agent="scout", category="recon", task_id="t-003", model="haiku",
                ts="2026-07-10T09:10:00", notes="other t-003"))

HEAD_TEXT = _text(B1, H1, H2)
OTHER_TEXT = _text(B1, O1, O2)
UNION = _text(B1, H1, H2, O1, O2)          # what merge=union leaves: ours first, then theirs


COLLISION = "task id(s) issued by BOTH clones are not declared"


@pytest.fixture(autouse=True)
def _no_declaration_in_the_index(request, monkeypatch):
    """B-402: _main also asks git whether logs/journal-segments.json is staged / what the index
    holds. A test that stubs the journal wrappers must not depend on the declaration of whatever
    repository the suite runs in (committed after placement, absent before); tests that build a real
    temp repo (they take `tmp_path`) use the real wrappers."""
    if "tmp_path" not in request.fixturenames:
        monkeypatch.setattr(jv, "is_declaration_staged", lambda *a, **k: False)
        monkeypatch.setattr(jv, "get_staged_declaration", lambda *a, **k: None)
        # t-581: the per-developer files and the freeze of the history are read from git too; a stubbed
        # run must not depend on whether the repository the suite runs in has switched
        monkeypatch.setattr(jv, "staged_journal_changes", lambda *a, **k: [])
        monkeypatch.setattr(jv, "tree_has_developer_file", lambda *a, **k: False)


def _merge(staged: str, head=HEAD_TEXT, other=OTHER_TEXT, known=None):
    """decide_merge with NO_SEGMENTS (E10: no fixture reads the repository's declaration). The base
    fixtures collide on t-002 on purpose; the collision WARN (B-402, tested on its own further down,
    K7) is filtered out here so that these older tests keep asserting what they always asserted."""
    code, violations, warnings = jv.decide_merge(staged, head, other, NOW, known, segments=jk.NO_SEGMENTS)
    return code, violations, [w for w in warnings if COLLISION not in w]


def _with_feature(line: str, feature="F01", first=False) -> str:
    obj = json.loads(line)
    return _dump({"feature": feature, **obj} if first else {**obj, "feature": feature})


def _assert_fails(res, *needles: str):
    code, violations, _w = res
    assert code == 1, res
    joined = "\n".join(violations)
    for n in needles:
        if n.startswith(("HEAD line", "MERGE_HEAD line")):
            # the parent is named EXACTLY: "HEAD line 3" is a substring of "MERGE_HEAD line 3"
            assert any(v.startswith(f"merge: {n} ") for v in violations), (n, violations)
        else:
            assert n in joined, (n, violations)
    return violations


# ---- positive: the union of two tails ----

def test_union_precondition_fails_without_merge_mode():
    # the 79-violations case: against HEAD alone the union is refused (closed id, ts order)
    code, violations = jv.decide(UNION, HEAD_TEXT, NOW)
    assert code == 1
    assert any("CLOSED task" in v for v in violations)
    assert any("ts is not monotonic" in v for v in violations)


def test_union_of_two_tails_sharing_a_task_id_passes():
    assert _merge(UNION) == (0, [], [])


def test_union_in_the_other_order_also_passes():
    assert _merge(_text(B1, O1, O2, H1, H2)) == (0, [], [])


def test_staged_equal_to_head_with_other_already_inside_passes():
    assert _merge(HEAD_TEXT, other=_text(B1)) == (0, [], [])


# ---- positive: an added feature on a parent line ----

def test_parent_lines_with_only_an_added_feature_pass():
    staged = _text(_with_feature(B1), _with_feature(H1), H2, _with_feature(O1), O2)
    assert _merge(staged) == (0, [], [])


def test_feature_key_order_is_free():
    staged = _text(_with_feature(B1, first=True), H1, H2, _with_feature(O1, first=True), O2)
    assert _merge(staged) == (0, [], [])


def test_one_staged_line_with_feature_serves_both_parents():
    staged = _text(_with_feature(B1), H1, H2, O1, O2)    # B1 is the base line, in both parents
    assert _merge(staged) == (0, [], [])


# ---- negative controls: each -> 1, with a text naming the parent and the line ----

def test_head_line_dropped():
    v = _assert_fails(_merge(_text(B1, H1, O1, O2)), "HEAD line 3")
    assert len(v) == 1 and "MERGE_HEAD line" not in v[0]
    assert "every line of both merged journals is kept unchanged and in its order" in v[0]
    assert "added `feature` field" in v[0]


def test_merge_head_line_dropped():
    v = _assert_fails(_merge(_text(B1, H1, H2, O1)), "MERGE_HEAD line 3")
    assert len(v) == 1 and v[0].startswith("merge: MERGE_HEAD line 3 (")
    assert repr(O2[:80]) in v[0]


def test_two_head_lines_swapped():
    v = _assert_fails(_merge(_text(B1, H2, H1, O1, O2)), "HEAD line 3")
    assert len(v) == 1 and "MERGE_HEAD" not in v[0]


def test_two_merge_head_lines_swapped():
    v = _assert_fails(_merge(_text(B1, H1, H2, O2, O1)), "MERGE_HEAD line 3")
    assert len(v) == 1


def test_parent_line_with_another_field_changed():
    changed = json.loads(H1)
    changed["notes"] = "reworded"
    _assert_fails(_merge(_text(B1, _dump(changed), H2, O1, O2)), "HEAD line 2")


def test_parent_line_with_another_field_changed_and_a_feature_added():
    changed = json.loads(O1)
    changed["notes"] = "reworded"
    changed["feature"] = "F01"
    _assert_fails(_merge(_text(B1, H1, H2, _dump(changed), O2)), "MERGE_HEAD line 2")


def test_value_type_change_is_not_kept():
    # 1 == True in Python; a changed value must not pass because of that
    head = _text(_dump(_obj(task_id="t-001", model="sonnet", attempt=1)))
    staged = _text(_dump(_obj(task_id="t-001", model="sonnet", attempt=True, feature="F01")))
    _assert_fails(_merge(staged, head=head, other=""), "HEAD line 1")


def test_parent_line_that_already_had_a_feature_given_a_different_one():
    head = _text(B1, _with_feature(H1, "F01"))
    staged = _text(B1, _with_feature(H1, "F02"), O1)
    _assert_fails(_merge(staged, head=head, other=_text(B1, O1)), "HEAD line 2")


def test_parent_line_that_already_had_a_feature_stays_by_equality():
    head = _text(B1, _with_feature(H1, "F01"))
    staged = _text(B1, _with_feature(H1, "F01"), O1)
    assert _merge(staged, head=head, other=_text(B1, O1)) == (0, [], [])


def test_feature_set_to_an_empty_string():
    staged = _text(B1, _with_feature(H1, ""), H2, O1, O2)
    _assert_fails(_merge(staged), "HEAD line 2")


def test_feature_that_is_not_a_string():
    staged = _text(B1, _with_feature(H1, 5), H2, O1, O2)
    _assert_fails(_merge(staged), "HEAD line 2")


def test_new_line_between_two_kept_lines():
    new = _dump(_obj(task_id="t-004", model="sonnet", ts="2026-07-10T11:00:00"))
    v = _assert_fails(_merge(_text(B1, H1, new, H2, O1, O2)), "staged line 3", "new events go at the tail")
    assert len(v) == 1
    assert "or remove it if it duplicates a line one of the merged journals already holds" in v[0]


def test_new_line_above_every_kept_line_but_the_last():
    new = _dump(_obj(task_id="t-004", model="sonnet", ts="2026-07-10T11:00:00"))
    _assert_fails(_merge(_text(B1, H1, H2, O1, new, O2)), "staged line 5", "new events go at the tail")


def test_new_tail_line_older_than_the_last_kept_line_today_rule_fires():
    new = _dump(_obj(task_id="t-004", model="sonnet", ts="2026-07-10T08:30:00"))
    v = _assert_fails(_merge(UNION + new + "\n"), "ts is not monotonic")
    assert "line 6" in v[0]                      # numbered as in the staged file


def _new_at(ts: str, task_id="t-004") -> str:
    return _dump(_obj(task_id=task_id, model="sonnet", ts=ts))


def test_new_tail_line_older_than_heads_own_last_ts_fails_naming_it():
    # S1: HEAD ends 10:05, MERGE_HEAD ends 09:10, the union ends with MERGE_HEAD's tail
    v = _assert_fails(_merge(_text(B1, H1, H2, O1, O2, _new_at("2026-07-10T09:30:00"))),
                      "ts is not monotonic")
    assert len(v) == 1 and v[0].startswith("line 6 event='delegated' task_id='t-004'")
    assert "2026-07-10T09:30:00 is earlier than the previous 2026-07-10T10:05:00" in v[0]


def test_new_tail_line_after_the_newest_parent_event_passes():
    assert _merge(_text(B1, H1, H2, O1, O2, _new_at("2026-07-10T10:06:00"))) == (0, [], [])


def test_new_tail_line_equal_to_the_anchor_passes():
    assert _merge(_text(B1, H1, H2, O1, O2, _new_at("2026-07-10T10:05:00"))) == (0, [], [])


def test_f4_a_foreign_clock_that_is_ahead_does_not_close_the_door():
    # t-525 F4: MERGE_HEAD's last ts (10:30) is NEWER than HEAD's (10:05) and than the tail line (10:10).
    # The tail is OUR side's: anchored on HEAD's own last ts, so it is accepted
    late_o = _dump(_obj(agent="scout", category="recon", task_id="t-003", model="haiku",
                        ts="2026-07-10T10:30:00", notes="other t-003"))
    other = _text(B1, O1, late_o)
    staged = _text(B1, O1, late_o, H1, H2, _new_at("2026-07-10T10:10:00"))
    assert _merge(staged, other=other) == (0, [], [])
    # ... a line before HEAD's OWN last ts is still refused
    v = _assert_fails(_merge(_text(B1, O1, late_o, H1, H2, _new_at("2026-07-10T10:04:00")), other=other),
                      "ts is not monotonic")
    assert "earlier than the previous 2026-07-10T10:05:00" in v[0]


def test_f4_the_merge_accepts_door_works_when_the_foreign_tail_is_hours_ahead():
    # foreign last ts 14:30, now 12:00 (NOW), the foreign line is missing `model`
    bad = _dump(_obj(agent="scout", category="recon", task_id="t-003", ts="2026-07-10T14:30:00"))
    ack_ok = _ack("merge-accepts:2:model claude-sonnet-4-5 -- not recorded", ts="2026-07-10T11:59:00")
    staged = _text(B1, H1, H2, bad, ack_ok)
    assert _merge(staged, other=_text(B1, bad)) == (0, [], [])                  # 11:59 > HEAD's 10:05, < now+10min
    # a token line dated AFTER the foreign tail is the "later than now+10min" case: still refused
    ack_late = _ack("merge-accepts:2:model claude-sonnet-4-5 -- not recorded", ts="2026-07-10T14:31:00")
    _assert_fails(_merge(_text(B1, H1, H2, bad, ack_late), other=_text(B1, bad)), "later than now+10min")
    # a token line before HEAD's own last ts is refused
    ack_old = _ack("merge-accepts:2:model claude-sonnet-4-5 -- not recorded", ts="2026-07-10T10:00:00")
    _assert_fails(_merge(_text(B1, H1, H2, bad, ack_old), other=_text(B1, bad)), "ts is not monotonic")


def test_only_the_first_new_line_is_compared_with_the_anchor_the_rest_chain():
    a = _new_at("2026-07-10T10:06:00", "t-004")
    b = _new_at("2026-07-10T10:05:30", "t-005")             # earlier than a: today's chain rule fires
    v = _assert_fails(_merge(_text(B1, H1, H2, O1, O2, a, b)), "ts is not monotonic")
    assert len(v) == 1 and v[0].startswith("line 7 ")


def test_anchor_with_both_violations_orders_them_by_line_and_does_not_double_report():
    a = _new_at("2026-07-10T09:30:00", "t-004")
    b = _new_at("2026-07-10T09:20:00", "t-005")
    v = _assert_fails(_merge(_text(B1, H1, H2, O1, O2, a, b)), "ts is not monotonic")
    assert [x.split(" event=")[0] for x in v] == ["line 6", "line 7"]


def test_a_parent_with_no_lines_or_an_unparseable_last_ts_gives_no_anchor():
    new = _new_at("2026-07-10T09:30:00")
    # HEAD's last line is not JSON, MERGE_HEAD ends 09:10: the anchor is MERGE_HEAD's
    head = _text(B1, "not json")
    staged = _text(B1, "not json", O1, O2, new)
    assert _merge(staged, head=head)[0] == 0
    # MERGE_HEAD empty: HEAD ends 10:05 and is the anchor
    v = _assert_fails(_merge(_text(B1, H1, H2, _new_at("2026-07-10T09:30:00", "t-003")), other=""),
                      "ts is not monotonic")
    assert len(v) == 1 and "earlier than the previous 2026-07-10T10:05:00" in v[0]
    # neither parent gives an anchor: today's rule (anchored on the last kept line, none here)
    assert _merge(_text(_new_at("2026-07-10T09:30:00", "t-001")), head="", other="") == (0, [], [])
    # a last line with a ts that does not parse gives none either
    bad_ts = _dump(_obj(task_id="t-001", model="sonnet", ts="not a ts"))
    assert _merge(_text(bad_ts, _new_at("2026-07-10T09:30:00", "t-002")),
                  head=_text(bad_ts), other="") == (0, [], [])


def test_both_parents_empty_equals_decide_with_warnings_on_an_empty_head():
    staged = _text(_new_at("2026-07-10T09:00:00", "t-001"), _new_at("2026-07-10T08:00:00", "t-002"))
    assert (jv.decide_merge(staged, "", "", NOW, None, segments=jk.NO_SEGMENTS)
            == jv.decide_with_warnings(staged, "", NOW, None))


def test_duplicate_staged_line_between_kept_lines_names_both_doors():
    # S2: X is held by both parents (at different places); the staged text has it twice
    x = _dump(_obj(task_id="t-005", model="sonnet", ts="2026-07-10T07:00:00", notes="shared X"))
    head = _text(B1, x, H1)
    other = _text(B1, O1, x)
    v = _assert_fails(_merge(_text(B1, O1, x, x, H1), head=head, other=other),
                      "staged line 4", "new events go at the tail")
    assert len(v) == 1
    assert "or remove it if it duplicates a line one of the merged journals already holds" in v[0]
    assert _merge(_text(B1, O1, x, H1), head=head, other=other) == (0, [], [])


def test_duplicate_json_keys_cannot_reword_a_kept_line_under_an_added_feature():
    # M1: json.loads keeps the last repeated key, so the staged object looks equal to the parent's
    parent = '{"ts":"2026-07-10T08:00:00","event":"dispatch_skipped","agent":"lead","category":"x","notes":"head"}'
    evil = ('{"ts":"2026-07-10T08:00:00","event":"dispatch_skipped","agent":"lead","category":"x",'
            '"notes":"EVIL","notes":"head","feature":"F01"}')
    assert json.loads(evil)["notes"] == "head"                # the premise of the probe
    v = _assert_fails(_merge(_text(evil), head=_text(parent), other=""), "HEAD line 1")
    assert len(v) == 1
    honest = parent[:-1] + ',"feature":"F01"}'
    assert _merge(_text(honest), head=_text(parent), other="") == (0, [], [])
    # a line with repeated keys that is string-equal to its parent stays kept (equality)
    assert _merge(_text(evil), head=_text(evil), other="") == (0, [], [])
    # a repeated key nested inside the object is the same
    nested = parent[:-1] + ',"extra":{"a":1,"a":1},"feature":"F01"}'
    parent_nested = parent[:-1] + ',"extra":{"a":1,"a":1}}'
    assert _merge(_text(nested), head=_text(parent_nested), other="")[0] == 1


def test_new_tail_line_reusing_a_closed_id_today_rule_fires():
    new = _dump(_obj(task_id="t-002", model="sonnet", ts="2026-07-10T11:00:00"))
    v = _assert_fails(_merge(_text(B1, H1, H2, O1, O2, new)), "CLOSED task")
    assert "line 6" in v[0]


def test_new_tail_line_with_a_wrong_new_id_today_rule_fires():
    new = _dump(_obj(task_id="t-009", model="sonnet", ts="2026-07-10T11:00:00"))
    _assert_fails(_merge(_text(B1, H1, H2, O1, O2, new)), "task_id novelty")


def test_valid_new_tail_passes():
    new = _dump(_obj(task_id="t-004", model="sonnet", ts="2026-07-10T11:00:00"))
    assert _merge(_text(B1, H1, H2, O1, O2, new)) == (0, [], [])


def test_warnings_come_from_the_new_tail_only():
    kept_a = _dump(_obj(task_id="t-001", model="sonnet", ts="2026-10-03T08:00:00"))
    kept_b = _dump(_obj(task_id="t-002", model="sonnet", ts="2026-10-03T09:00:00"))
    new = _dump(_obj(task_id="t-003", model="sonnet", ts="2026-10-03T10:00:00"))
    now = jv.datetime.datetime(2026, 10, 4, 12, 0, 0)
    code, violations, warnings = jv.decide_merge(_text(kept_a, kept_b, new), _text(kept_a),
                                                 _text(kept_a, kept_b), now, known=set(),
                                                 segments=jk.NO_SEGMENTS)
    assert code == 0 and violations == []
    assert len(warnings) == 1 and "line 3" in warnings[0] and "WARN no 'feature'" in warnings[0]


# ---- edges: duplicates, non-JSON lines ----

def test_parent_line_present_twice_must_be_found_twice():
    head = _text(B1, H1, H1)
    _assert_fails(_merge(_text(B1, H1), head=head, other=""), "HEAD line 3")
    assert _merge(_text(B1, H1, H1), head=head, other="") == (0, [], [])


def test_non_json_line_is_kept_only_by_exact_string_equality():
    head = _text(B1, "not json at all")
    assert _merge(_text(B1, "not json at all"), head=head, other="") == (0, [], [])
    _assert_fails(_merge(_text(B1, "not json at all!"), head=head, other=""), "HEAD line 2")


def test_non_json_parent_line_does_not_take_a_feature():
    head = _text(B1, "not json at all")
    staged = _text(B1, _dump({"feature": "F01"}))
    _assert_fails(_merge(staged, head=head, other=""), "HEAD line 2")


def test_a_long_dropped_line_is_cut_to_80_characters():
    long_line = _dump(_obj(task_id="t-001", model="sonnet", notes="x" * 300))
    v = _assert_fails(_merge("", head=_text(long_line), other=""), "HEAD line 1")
    assert repr(long_line[:80]) in v[0] and long_line[:81] not in v[0]


# ---- boundaries ----

def test_empty_other_text():
    assert _merge(HEAD_TEXT, other="") == (0, [], [])
    assert _merge(HEAD_TEXT, other=None) == (0, [], [])


def test_empty_head_text():
    assert _merge(OTHER_TEXT, head="") == (0, [], [])
    assert _merge(OTHER_TEXT, head=None) == (0, [], [])


def test_all_three_empty():
    assert _merge("", head="", other="") == (0, [], [])
    assert _merge(None, head=None, other=None) == (0, [], [])


def test_empty_staged_with_non_empty_parents_names_every_line():
    code, violations, _w = _merge("")
    assert code == 1
    assert len([v for v in violations if v.startswith("merge: HEAD line ")]) == 3
    assert len([v for v in violations if v.startswith("merge: MERGE_HEAD line ")]) == 3


def test_staged_lines_with_both_parents_empty_are_all_new_and_validated():
    ok = _dump(_obj(task_id="t-001", model="sonnet"))
    assert _merge(_text(ok), head="", other="") == (0, [], [])
    bad = _dump(_obj(task_id="t-005", model="sonnet"))
    _assert_fails(_merge(_text(bad), head="", other=""), "task_id novelty")


# ---- decide / decide_with_warnings are untouched: outside a merge append-only stands ----

def test_a_rewritten_head_line_still_fails_outside_a_merge():
    staged = _text(B1, _with_feature(H1), H2)
    code, violations = jv.decide(staged, HEAD_TEXT, NOW)
    assert code == 1 and any("append-only" in v for v in violations)
    code, violations, warnings = jv.decide_with_warnings(staged, HEAD_TEXT, NOW)
    assert code == 1 and any("append-only" in v for v in violations) and warnings == []
    # ... while the same text, in merge mode, is the allowed door
    assert jv.decide_merge(staged, HEAD_TEXT, "", NOW, segments=jk.NO_SEGMENTS) == (0, [], [])


def test_dropped_head_line_still_fails_outside_a_merge():
    code, violations = jv.decide(_text(B1, H1), HEAD_TEXT, NOW)
    assert code == 1 and any("FEWER lines" in v for v in violations)


# ---- _main: the branch, with the git wrappers replaced ----

def _patch_main(monkeypatch, staged, head, other, merging):
    calls = []
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: True)
    monkeypatch.setattr(jv, "is_declaration_staged", lambda *a, **k: False)     # B-402: no declaration in the index
    monkeypatch.setattr(jv, "get_staged_declaration", lambda *a, **k: None)
    monkeypatch.setattr(jv, "get_staged_text", lambda *a, **k: staged)
    monkeypatch.setattr(jv, "get_head_text", lambda *a, **k: head)
    monkeypatch.setattr(jv, "is_merge_in_progress", lambda: merging)
    monkeypatch.setattr(jv, "get_merge_head_text", lambda *a, **k: calls.append("other") or other)
    return calls


def test_main_uses_merge_mode_only_when_merge_head_exists(monkeypatch, capsys):
    calls = _patch_main(monkeypatch, UNION, HEAD_TEXT, OTHER_TEXT, merging=True)
    assert jv.main([]) == 0
    assert calls == ["other"]
    calls = _patch_main(monkeypatch, UNION, HEAD_TEXT, OTHER_TEXT, merging=False)
    assert jv.main([]) == 1                                   # today's path: against HEAD alone
    assert calls == []                                        # MERGE_HEAD is not even read
    assert "FAILED validation" in capsys.readouterr().err


def test_main_not_staged_is_silent_zero_even_in_a_merge(monkeypatch, capsys):
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: False)
    monkeypatch.setattr(jv, "is_declaration_staged", lambda *a, **k: False)
    monkeypatch.setattr(jv, "is_merge_in_progress", lambda: pytest.fail("must not be asked"))
    assert jv.main([]) == 0
    assert capsys.readouterr().err == ""


# ---- _main end-to-end in a temp repo: a conflicted merge, concluded by hand ----

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _g(root: Path, *args: str, check=True) -> str:
    proc = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                           *args], cwd=root, capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _conflicted_merge(root: Path, other_lines=(O1, O2)) -> None:
    """Leaves root in the middle of a merge: the journal merged by union and staged, x.txt
    conflicted and resolved by hand (the state in which `git commit` runs pre-commit)."""
    root.mkdir(parents=True)
    _g(root, "init", "-q")
    _g(root, "config", "core.autocrlf", "false")
    _write(root, ".gitattributes", "logs/routing-log.jsonl merge=union\n")
    _write(root, "logs/routing-log.jsonl", _text(B1))
    _write(root, "x.txt", "base\n")
    _g(root, "add", "-A")
    _g(root, "commit", "-q", "-m", "base")
    _g(root, "branch", "-M", "main")
    _g(root, "checkout", "-q", "-b", "other")
    _write(root, "logs/routing-log.jsonl", _text(B1, *other_lines))
    _write(root, "x.txt", "other\n")
    _g(root, "commit", "-q", "-am", "other tail")
    _g(root, "checkout", "-q", "main")
    _write(root, "logs/routing-log.jsonl", _text(B1, H1, H2))
    _write(root, "x.txt", "main\n")
    _g(root, "commit", "-q", "-am", "main tail")
    _g(root, "merge", "--no-commit", "other", check=False)       # x.txt conflicts, the journal unions
    assert (root / ".git" / "MERGE_HEAD").exists()
    _write(root, "x.txt", "resolved\n")
    _g(root, "add", "x.txt")


@needs_git
def test_main_end_to_end_conflicted_merge_concluded_by_hand(tmp_path, monkeypatch, capsys):
    root = tmp_path / "m"
    _conflicted_merge(root)
    staged = _g(root, "show", ":./logs/routing-log.jsonl")
    assert staged.count("\n") == 5                               # both tails are in the index
    monkeypatch.chdir(root)
    assert jv.main([]) == 0
    err = capsys.readouterr().err            # B-402: the fixtures collide on t-002 and nothing declares it -> a WARN, never a FAIL
    assert "FAILED" not in err and "issued by BOTH clones are not declared: t-002" in err
    # the door: the feature added to a line of the other parent
    lines = jv.split_lines(staged)
    lines[lines.index(O2)] = _with_feature(O2)
    _write(root, "logs/routing-log.jsonl", _text(*lines))
    _g(root, "add", "logs/routing-log.jsonl")
    assert jv.main([]) == 0


@needs_git
def test_main_end_to_end_dropped_line_of_the_other_parent_fails(tmp_path, monkeypatch, capsys):
    root = tmp_path / "m"
    _conflicted_merge(root)
    staged = jv.split_lines(_g(root, "show", ":./logs/routing-log.jsonl"))
    staged.remove(O2)
    _write(root, "logs/routing-log.jsonl", _text(*staged))
    _g(root, "add", "logs/routing-log.jsonl")
    monkeypatch.chdir(root)
    assert jv.main([]) == 1
    err = capsys.readouterr().err
    assert "MERGE_HEAD line 3" in err and "FAILED validation" in err
    assert jv.get_merge_head_text() == OTHER_TEXT


@needs_git
def test_get_merge_head_text_is_empty_when_git_fails(tmp_path, monkeypatch):
    root = tmp_path / "plain"
    root.mkdir()
    _g(root, "init", "-q")
    monkeypatch.chdir(root)
    assert jv.is_merge_in_progress() is False
    assert jv.get_merge_head_text() == ""


# =====================================================================================
# B-401: the FORM of the lines the other clone brought, the merge-accepts token, the clean-merge
# path (pre-merge-commit hook, `--merge-parent env`)
# =====================================================================================

import os
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent


def _fields(violations) -> list[str]:
    """The `[field]` of each form violation, in order (merge-form texts only)."""
    out = []
    for v in violations:
        m = re.search(r" \[([a-z_]+)\]: ", v)
        if v.startswith("merge: MERGE_HEAD line ") and m:
            out.append(m.group(1))
    return out


def _without(line: str, *keys: str) -> str:
    return _dump({k: v for k, v in json.loads(line).items() if k not in keys})


def _foreign(bad: str, tail: tuple = ()) -> tuple:
    """The other clone brought `bad` as ITS line 2 (staged line 4) and a clean line 3 after it;
    HEAD brought H1/H2. `tail` = new lines appended after the union (a merge-accepts carrier)."""
    staged = _text(B1, H1, H2, bad, O2, *tail)
    return _merge(staged, other=_text(B1, bad, O2))


def _ok(**kw) -> dict:
    d = {"ts": "2026-07-10T09:20:00", "task_id": "t-050", "model": "sonnet"}
    d.update(kw)
    return d


def _acc(**kw) -> str:
    return _dump(_obj(event="accepted", agent="builder", witness="w", **_ok(**kw)))


_REJ = _dump(_obj(event="rejected", agent="builder", by="opus", failure_class="spec", attempt=1, **_ok()))
_DUP_NOTES = ('{"ts":"2026-07-10T09:20:00","event":"delegated","agent":"builder","category":"implementation",'
              '"notes":"a","notes":"b","task_id":"t-050","model":"sonnet","worker_ref":"cli:x"}')

# the A8 table: every fixture stays refused, with its field (id = fixture, field)
A8 = [
    ("repeated-notes-key", _DUP_NOTES, "line"),
    ("json-list", "[1, 2, 3]", "line"),
    ("not-json", "{not json", "line"),
    ("empty-line", "", "line"),
    ("attempt-NaN", _REJ.replace('"attempt": 1', '"attempt": NaN'), "attempt"),
    ("attempt-true", _REJ.replace('"attempt": 1', '"attempt": true'), "attempt"),
    ("by-Fable", _acc(by="Fable"), "by"),
    ("by-model-id", _acc(by="claude-opus-4-8"), "by"),
    ("by-sonnet-no-basis", _acc(by="sonnet"), "by"),
    ("ts-Z", _dump(_obj(**_ok(ts="2026-07-10T09:20:00Z"))), "ts"),
    ("ts-offset", _dump(_obj(**_ok(ts="2026-07-10T09:20:00+03:00"))), "ts"),
    ("ts-space", _dump(_obj(**_ok(ts="2026-07-10 09:20:00"))), "ts"),
    ("task-id-t-14", _dump(_obj(**_ok(task_id="t-14"))), "task_id"),
    ("event-delegate", _dump(_obj(event="delegate", **_ok())), "event"),
    # B-454 item 2: an unhashable value in a form field is a NAMED violation, never a TypeError
    ("event-list", _dump(_obj(event=["x"], **_ok())), "event"),
    ("task-id-dict", _dump(_obj(**_ok(task_id={"a": 1}))), "task_id"),
    ("by-list", _acc(by=["opus"]), "by"),
]


def test_a8_premises_the_fixtures_are_what_they_say():
    assert "NaN" in A8[4][1] and "true" in A8[5][1]
    assert json.loads(_DUP_NOTES)["notes"] == "b"                     # the last repeated key wins in json.loads
    assert A8[3][1] == "" and len(A8) == 17


@pytest.mark.parametrize("name,bad,field", A8, ids=[f"{a}-{c}" for a, _b, c in A8])
def test_a8_foreign_defect_stays_refused_with_its_field(name, bad, field):
    code, violations, _w = _foreign(bad)
    assert code == 1, violations
    assert _fields(violations) == [field], violations                 # one violation, the field named
    v = violations[0]
    assert v.startswith("merge: MERGE_HEAD line 2 (staged line 4) event="), v   # both line numbers
    assert f"[{field}]" in v
    assert f"merge-accepts:2:{field}" in v                            # the door names the exact token
    assert "append-only forbids editing it there or here" in v and "git merge --no-commit <branch>" in v


def test_a8_two_unhashable_fields_two_violations_one_token_clears_both():
    # B-454 item 2 edge: a foreign line with two non-string fields -> one violation per field, and one
    # token naming both fields clears the line (never a traceback)
    bad = _acc(by=["opus"], task_id={"a": 1})
    code, violations, _w = _foreign(bad)
    assert code == 1 and _fields(violations) == ["task_id", "by"], violations
    ack = _ack("merge-accepts:2:task_id,by the other clone's line is kept as it is")
    assert _foreign(bad, (ack,)) == (0, [], [])


def test_a8_by_Fable_is_not_refused_where_the_matrix_does_not_apply():
    # not refused by design (today's rule-11 scope, the matrix exits early): agent lead, and a rejected
    lead = _dump(_obj(event="accepted", agent="lead", by="Fable", **_ok()))
    assert _foreign(lead)[0] == 0
    rej = _dump(_obj(event="rejected", agent="builder", by="Fable", failure_class="spec", attempt=1, **_ok()))
    assert _foreign(rej)[0] == 0


def test_a_good_foreign_line_gives_nothing():
    assert _foreign(_dump(_obj(**_ok()))) == (0, [], [])


def test_foreign_texts_name_the_event_and_the_task_id():
    assert "event='delegated' task_id='t-14'" in _foreign(_dump(_obj(**_ok(task_id="t-14"))))[1][0]
    assert "event=None task_id=None" in _foreign("[1, 2, 3]")[1][0]


# ---- K-D: the excluded rules do not fire on MERGE_HEAD-only lines (and do fire in the tail) ----

_EXCL = {
    "novelty-jump-t-009": _dump(_obj(**_ok(task_id="t-009", ts="2026-07-10T09:15:00"))),
    "delegated-on-id-closed-in-head": _dump(_obj(**_ok(task_id="t-002", ts="2026-07-10T09:15:00"))),
    "ts-older-than-heads-tail": _dump(_obj(**_ok(ts="2026-07-10T08:30:00", task_id="t-003"))),
    "ts-now-plus-11-min": _dump(_obj(**_ok(ts="2026-07-10T12:11:00", task_id="t-003"))),
    "accepted-on-an-id-unseen-anywhere": _acc(task_id="t-777", by="opus", ts="2026-07-10T09:30:00"),
}


@pytest.mark.parametrize("name", sorted(_EXCL))
def test_excluded_rules_do_not_fire_on_foreign_lines(name):
    x = _EXCL[name]
    assert _merge(_text(B1, H1, H2, x), other=_text(B1, x)) == (0, [], [])
    # the control: the same line as a NEW tail line IS refused (the rule is alive, only excluded here)
    assert _merge(_text(B1, H1, H2, x), other="")[0] == 1


def test_feature_warn_is_not_raised_for_foreign_lines():
    now = jv.datetime.datetime(2026, 10, 4, 12, 0, 0)
    x = _dump(_obj(**_ok(ts="2026-10-03T09:15:00")))
    assert jv.decide_merge(_text(B1, x), _text(B1), _text(B1, x), now, known=set()) == (0, [], [])


# ---- K-E: HEAD-only and shared defective lines still give 0 ----

def test_head_only_and_shared_defective_lines_give_zero():
    bad = _dump(_obj(**_ok(task_id="t-14")))                  # a task_id defect
    assert _merge(_text(B1, bad), head=_text(B1, bad), other=_text(B1)) == (0, [], [])
    assert _merge(_text(B1, bad), head=_text(B1, bad), other=_text(B1, bad)) == (0, [], [])
    assert _merge(_text(B1, bad), head=_text(B1), other=_text(B1, bad))[0] == 1       # control: other-only


# ---- K-F: the merge-accepts token ----

BAD_MODEL = _dump(_obj(agent="scout", category="recon", task_id="t-003", ts="2026-07-10T09:20:00"))   # no model
BAD_PAIR = _without(_acc(by="sonnet"), "model")               # a missing model AND an illegal pair (sonnet, builder, no basis)


def _ack(notes: str, ts="2026-07-10T11:00:00") -> str:
    return _dump({"ts": ts, "event": "dispatch_skipped", "agent": "lead", "category": "ack", "notes": notes})


def _merge_one(bad: str, *tail: str, head=HEAD_TEXT):
    return _merge(_text(B1, H1, H2, bad, *tail), head=head, other=_text(B1, bad))


def test_token_premises_the_fixtures_have_exactly_the_defects_named():
    assert "model" not in json.loads(BAD_PAIR)
    assert _fields(_merge_one(BAD_PAIR)[1]) == ["model", "by"]
    assert _fields(_merge_one(BAD_MODEL)[1]) == ["model"]


def test_token_clears_exactly_the_named_field():
    ack = _ack("merge-accepts:2:model claude-sonnet-4-5 -- the other clone never recorded it")
    assert _merge_one(BAD_MODEL, ack) == (0, [], [])
    # a line that also has an illegal pair: the token names `model` only, so `by` still refuses
    code, violations, _w = _merge_one(BAD_PAIR, ack)
    assert code == 1 and _fields(violations) == ["by"]


def test_token_with_several_fields_and_several_tokens_add_up():
    both = _ack("merge-accepts:2:model,by the corrected pair and the Lead's decision")
    assert _merge_one(BAD_PAIR, both) == (0, [], [])
    two = (_ack("merge-accepts:2:model one", "2026-07-10T11:00:00"), _ack("merge-accepts:2:by two", "2026-07-10T11:01:00"))
    assert _merge_one(BAD_PAIR, *two) == (0, [], [])


def test_bare_token_clears_nothing_and_warns():
    code, violations, warnings = _merge_one(BAD_PAIR, _ack("merge-accepts:2 everything is fine"))
    assert code == 1 and _fields(violations) == ["model", "by"]
    assert len(warnings) == 1 and "names no field" in warnings[0] and "merge-accepts:2:<field>" in warnings[0]


def test_unknown_field_and_a_field_without_a_violation_warn_and_clear_nothing():
    code, violations, warnings = _merge_one(BAD_MODEL, _ack("merge-accepts:2:modle typo"))
    assert code == 1 and _fields(violations) == ["model"]
    assert len(warnings) == 1 and "unknown field 'modle'" in warnings[0]
    code, violations, warnings = _merge_one(BAD_MODEL, _ack("merge-accepts:2:ts the ts is fine"))
    assert code == 1 and _fields(violations) == ["model"]
    assert "has no violation on that field" in warnings[0] and "it has: model" in warnings[0]
    # a mixed token: the real field is cleared, the unknown one warns
    code, violations, warnings = _merge_one(BAD_MODEL, _ack("merge-accepts:2:model,bogus x"))
    assert code == 0 and violations == [] and "unknown field 'bogus'" in warnings[0]


def test_token_with_a_number_that_names_no_defective_line_warns():
    # n=0, n=len(MERGE_HEAD)+1 (3), n=1 (the base line both parents hold), n=2 with the right field
    notes = "merge-accepts:0:model a merge-accepts:3:model b merge-accepts:1:model c merge-accepts:2:model d"
    code, violations, warnings = _merge_one(BAD_MODEL, _ack(notes))
    assert code == 0 and violations == []
    assert len(warnings) == 3 and all("not a defective line the merged branch brought" in w for w in warnings)
    # a number outside the journal alone clears nothing
    assert _merge_one(BAD_MODEL, _ack("merge-accepts:3:model b"))[0] == 1


def test_token_in_a_kept_line_does_not_count():
    kept = _dump(_obj(**_ok(task_id="t-002", ts="2026-07-10T10:00:00", notes="merge-accepts:2:model old")))
    head = _text(B1, kept)
    assert _merge(_text(B1, kept, BAD_MODEL), head=head, other=_text(B1, BAD_MODEL))[0] == 1
    # the other parent's own kept line carrying the token for itself
    selfish = json.loads(BAD_MODEL)
    selfish["notes"] = "merge-accepts:2:model me"
    selfish = _dump(selfish)
    assert _merge(_text(B1, selfish), head=_text(B1), other=_text(B1, selfish))[0] == 1


def test_token_in_a_misplaced_new_line_does_not_count():
    carrier = _ack("merge-accepts:2:model late", ts="2026-07-10T08:30:00")
    staged = _text(B1, carrier, H1, H2, BAD_MODEL)           # a NEW line placed above kept lines
    code, violations, _w = _merge(staged, other=_text(B1, BAD_MODEL))
    assert code == 1
    assert _fields(violations) == ["model"]
    assert any("is a new event placed above kept line 5" in v for v in violations)


# ---- K-G: form, placement and the tail in ONE run ----

def test_form_placement_and_tail_violations_come_back_in_one_run():
    misplaced = _dump(_obj(**_ok(task_id="t-004", ts="2026-07-10T07:59:00")))
    tail = _acc(task_id="t-004", by="opus", ts="2026-07-10T08:00:00")      # cites the misplaced id; ts too old
    staged = _text(B1, misplaced, H1, H2, BAD_MODEL, tail)
    code, violations, _w = _merge(staged, other=_text(B1, BAD_MODEL))
    assert code == 1
    assert len(violations) == 3, violations
    assert violations[0].startswith("merge: MERGE_HEAD line 2 (staged line 5)") and "[model]" in violations[0]
    assert violations[1].startswith("merge: staged line 2 ") and "placed above kept line 5" in violations[1]
    assert violations[2].startswith("line 6 event='accepted'") and "ts is not monotonic" in violations[2]
    # the misplaced line is reported by placement only: the tail may cite its id without an orphan report
    assert not any("does not reference" in v for v in violations)
    assert sum("staged line 2" in v for v in violations) == 1


def test_a_misplaced_line_alone_is_one_violation():
    misplaced = _dump(_obj(**_ok(task_id="t-004", ts="2026-07-10T07:59:00")))
    code, violations, _w = _merge(_text(B1, misplaced, H1, H2, O1, O2))
    assert code == 1 and len(violations) == 1 and violations[0].startswith("merge: staged line 2 ")


# ---- R0: the premise on the real journal, with its positive control ----

def _r0_violations(text: str) -> list:
    found = []
    for n, line in enumerate(jv.split_lines(text), start=1):
        found += jv._foreign_line_violations(line, jv._parse_obj_nodup(line), n, n)
    return found


def test_r0_the_real_journal_has_no_form_violation():
    history = REPO_ROOT / "logs" / "routing-log.jsonl"
    real = ([history] if history.exists() else []) + [REPO_ROOT / f.path for f in jk.load_all(REPO_ROOT).files]   # the clone's own files
    if not real:
        pytest.skip("no journal file in this clone (github-move FK-14)")
    for path in real:
        text = path.read_text(encoding="utf-8")
        assert len(jv.split_lines(text)) > (100 if path == history else 0), path.name
        assert _r0_violations(text) == [], path.name
    # the control, the same function and call shape: injected lines ARE found (1 and 3 violations)
    text = real[0].read_text(encoding="utf-8")
    one = _without(_dump(_obj(**_ok())), "model")
    three = _without(_dump(_obj(**_ok(ts="2026-07-10T09:20:00Z"))), "model", "worker_ref")
    assert len(_r0_violations(text + one + "\n")) == 1
    assert [f for f, _t in _r0_violations(three + "\n")] == ["model", "worker_ref", "ts"]


# ---- the clean-merge path: GITHEAD, the parent, the CLI ----

def test_merge_parents_from_env():
    sha1, sha2 = "a" * 40, "0123456789abcdef" * 4
    assert jv.merge_parents_from_env({}) == []
    assert jv.merge_parents_from_env({"PATH": "x", f"GITHEAD_{sha1}": "other"}) == [sha1]
    assert jv.merge_parents_from_env({f"GITHEAD_{sha1}": "a", f"GITHEAD_{sha2}": "b"}) == sorted([sha1, sha2])
    # names that do not match the pattern are ignored: non-hex suffix, too short, too long, a prefix, a suffix
    env = {"GITHEAD_xyz": "1", "GITHEAD_abc123": "1", f"GITHEAD_{'a' * 65}": "1",
           f"XGITHEAD_{sha1}": "1", f"GITHEAD_{sha1}x": "1"}
    assert jv.merge_parents_from_env(env) == []
    # Windows: os.environ upper-cases the names, so the sha arrives upper-cased and is returned lower-cased
    assert jv.merge_parents_from_env({f"GITHEAD_{sha2.upper()}": "1"}) == [sha2]
    assert jv.merge_parents_from_env({f"GITHEAD_{'b' * 7}": "1"}) == ["b" * 7]       # the lower bound, 7


def test_main_merge_parent_not_staged_is_silent_zero_even_with_two_parents(monkeypatch, capsys):
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: False)
    monkeypatch.setenv(f"GITHEAD_{'a' * 40}", "x")
    monkeypatch.setenv(f"GITHEAD_{'b' * 40}", "y")
    assert jv.main(["--merge-parent", "env"]) == 0
    assert capsys.readouterr().err == ""


def test_main_merge_parent_needs_a_value(capsys):
    assert jv.main(["--merge-parent"]) == 1
    assert "--merge-parent needs a value" in capsys.readouterr().err


def test_main_refuses_the_positional_path_the_old_ci_line_passed(monkeypatch, capsys):
    # t-581: the old CI line passed the journal path positionally and the gate ignored it (so the line
    # checked nothing); an argument the gate does not know is now a refusal that names it
    calls = _patch_main(monkeypatch, UNION, HEAD_TEXT, OTHER_TEXT, merging=True)
    assert jv.main(["logs/routing-log.jsonl"]) == 1
    assert calls == []
    assert "unknown argument 'logs/routing-log.jsonl'" in capsys.readouterr().err


def test_main_merge_parent_sha_reads_that_parent_not_merge_head(monkeypatch):
    sha = "c" * 40
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: True)
    monkeypatch.setattr(jv, "get_staged_text", lambda *a, **k: UNION)
    monkeypatch.setattr(jv, "get_head_text", lambda *a, **k: HEAD_TEXT)
    monkeypatch.setattr(jv, "is_commit", lambda s: s == sha)
    monkeypatch.setattr(jv, "get_parent_text", lambda s, *a, **k: OTHER_TEXT if s == sha else "")
    monkeypatch.setattr(jv, "is_merge_in_progress", lambda: pytest.fail("MERGE_HEAD must not be asked"))
    assert jv.main(["--merge-parent", sha]) == 0
    assert jv.main([f"--merge-parent={sha}"]) == 0


def test_main_merge_parent_env_with_no_githead_is_zero_plus_a_warn(monkeypatch, capsys):
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: True)
    for k in list(os.environ):
        if k.startswith("GITHEAD_"):
            monkeypatch.delenv(k)
    assert jv.main(["--merge-parent", "env"]) == 0
    err = capsys.readouterr().err
    assert "WARN the merged parent is not in the environment (GITHEAD_*)" in err
    assert "the other branch's journal lines were not checked" in err
    assert "git merge --no-commit <branch>" in err and "git commit" in err


def test_main_merge_parent_env_with_two_githeads_is_one_naming_both(monkeypatch, capsys):
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: True)
    monkeypatch.setenv(f"GITHEAD_{'a' * 40}", "x")
    monkeypatch.setenv(f"GITHEAD_{'b' * 40}", "y")
    assert jv.main(["--merge-parent", "env"]) == 1
    err = capsys.readouterr().err
    assert "a" * 40 in err and "b" * 40 in err and "merge one branch at a time" in err


def test_main_merge_parent_that_is_not_a_commit_is_one_naming_it(monkeypatch, capsys):
    monkeypatch.setattr(jv, "is_journal_staged", lambda *a, **k: True)
    monkeypatch.setattr(jv, "is_commit", lambda s: False)
    monkeypatch.setenv(f"GITHEAD_{'d' * 40}", "x")
    assert jv.main(["--merge-parent", "env"]) == 1
    err = capsys.readouterr().err
    assert "d" * 40 in err and "is not a commit" in err and "git merge --no-commit <branch>" in err


# ---- end to end, conflicted merge: the token through main() and real git ----

@needs_git
def test_main_end_to_end_conflicted_merge_foreign_defect_and_its_token(tmp_path, monkeypatch, capsys):
    root = tmp_path / "m"
    _conflicted_merge(root, other_lines=(O1, BAD_MODEL))             # BAD_MODEL = MERGE_HEAD line 3
    monkeypatch.chdir(root)
    assert jv.main([]) == 1
    err = capsys.readouterr().err
    assert "MERGE_HEAD line 3" in err and "[model]" in err and "merge-accepts:3:model" in err
    staged = jv.split_lines(_g(root, "show", ":./logs/routing-log.jsonl"))
    ack = _ack("merge-accepts:3:model claude-sonnet-4-5 -- the other clone never recorded the model")
    _write(root, "logs/routing-log.jsonl", _text(*staged, ack))
    _g(root, "add", "logs/routing-log.jsonl")
    assert jv.main([]) == 0
    err = capsys.readouterr().err
    assert "FAILED" not in err and "[model]" not in err        # only the t-002 collision WARN is left
    # the same token for another line number clears nothing
    _write(root, "logs/routing-log.jsonl", _text(*staged, _ack("merge-accepts:2:model wrong line")))
    _g(root, "add", "logs/routing-log.jsonl")
    assert jv.main([]) == 1
    err = capsys.readouterr().err
    assert "MERGE_HEAD line 3" in err and "WARN" in err and "not a defective line" in err


# ---- end to end, CLEAN merge: the real pre-merge-commit hook, real git ----

def _gr(root: Path, *args: str, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                           *args], cwd=root, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env)


def _clean_repo(root: Path, other_lines: tuple, with_hook: bool = True) -> None:
    """main: B1,H1,H2; other: B1,*other_lines; no file conflicts, so `git merge other` is clean
    (merge=union on the journal) and only the pre-merge-commit hook can look at it."""
    root.mkdir(parents=True)
    _gr(root, "init", "-q")
    _gr(root, "config", "core.autocrlf", "false")
    _write(root, ".gitattributes", "logs/routing-log.jsonl merge=union\n")
    _write(root, "logs/routing-log.jsonl", _text(B1))
    _gr(root, "add", "-A")
    _gr(root, "commit", "-q", "-m", "base")
    _gr(root, "branch", "-M", "main")
    _gr(root, "checkout", "-q", "-b", "other")
    _write(root, "logs/routing-log.jsonl", _text(B1, *other_lines))
    _gr(root, "commit", "-q", "-am", "other tail")
    _gr(root, "checkout", "-q", "main")
    _write(root, "logs/routing-log.jsonl", _text(B1, H1, H2))
    _gr(root, "commit", "-q", "-am", "main tail")
    if with_hook:
        hooks = root.parent / (root.name + "-hooks")
        hooks.mkdir()
        hook = hooks / "pre-merge-commit"
        body = f'#!/bin/sh\nexec "{Path(sys.executable).as_posix()}" "{Path(jv.__file__).as_posix()}" --merge-parent env\n'
        with open(hook, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        hook.chmod(0o755)
        _gr(root, "config", "core.hooksPath", hooks.as_posix())


@needs_git
def test_clean_merge_with_a_defective_foreign_line_is_refused_by_the_hook(tmp_path):
    root = tmp_path / "c"
    _clean_repo(root, (O1, BAD_MODEL))
    before = _gr(root, "rev-parse", "HEAD").stdout.strip()
    proc = _gr(root, "merge", "other", "-m", "merge other")
    assert proc.returncode != 0, (proc.stdout, proc.stderr)
    out = proc.stdout + proc.stderr
    assert "MERGE_HEAD line 3" in out and "[model]" in out and "merge-accepts:3:model" in out
    assert _gr(root, "rev-parse", "HEAD").stdout.strip() == before          # no merge commit was made


@needs_git
def test_clean_merge_with_a_clean_foreign_tail_lands(tmp_path):
    root = tmp_path / "c"
    _clean_repo(root, (O1, O2))
    proc = _gr(root, "merge", "other", "-m", "merge other")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert len(_gr(root, "rev-list", "--parents", "-n1", "HEAD").stdout.split()) == 3     # sha + two parents
    assert len(jv.split_lines((root / "logs" / "routing-log.jsonl").read_text(encoding="utf-8"))) == 5


@needs_git
def test_clean_merge_door_a_token_in_the_tail_of_the_merge_git_left_in_progress(tmp_path):
    # measured (git 2.45.1, Windows): a refused pre-merge-commit leaves the merge IN PROGRESS
    # ("Not committing merge; use 'git commit'"), MERGE_HEAD present, the union staged
    root = tmp_path / "c"
    _clean_repo(root, (O1, BAD_MODEL))
    assert _gr(root, "merge", "other", "-m", "merge other").returncode != 0
    assert (root / ".git" / "MERGE_HEAD").exists()
    staged = jv.split_lines(_gr(root, "show", ":./logs/routing-log.jsonl").stdout)
    ack = _ack("merge-accepts:3:model claude-sonnet-4-5 -- not recorded")
    _write(root, "logs/routing-log.jsonl", _text(*staged, ack))
    _gr(root, "add", "logs/routing-log.jsonl")
    proc = _gr(root, "commit", "--no-edit")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert len(_gr(root, "rev-list", "--parents", "-n1", "HEAD").stdout.split()) == 3


@needs_git
def test_clean_merge_door_a_token_in_the_tail_of_a_merge_started_again(tmp_path):
    root = tmp_path / "c"
    _clean_repo(root, (O1, BAD_MODEL))
    assert _gr(root, "merge", "other", "-m", "merge other").returncode != 0
    _gr(root, "reset", "-q", "--hard", "HEAD")                            # the door's other state: start again
    assert _gr(root, "merge", "--no-commit", "other").returncode == 0, "the merge must start again"
    staged = jv.split_lines(_gr(root, "show", ":./logs/routing-log.jsonl").stdout)
    ack = _ack("merge-accepts:3:model claude-sonnet-4-5 -- not recorded")
    _write(root, "logs/routing-log.jsonl", _text(*staged, ack))
    _gr(root, "add", "logs/routing-log.jsonl")
    proc = _gr(root, "commit", "--no-edit")                               # lands: the token clears the only defect
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert len(_gr(root, "rev-list", "--parents", "-n1", "HEAD").stdout.split()) == 3
    last = (root / "logs" / "routing-log.jsonl").read_text(encoding="utf-8").rstrip("\n").split("\n")[-1]
    assert last == ack


def _cli(root: Path, *args: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, jv.__file__, *args], cwd=root, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)


def _env_without_githead(**extra) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GITHEAD_")}
    env.update(extra)
    return env


@needs_git
def test_cli_merge_parent_env_one_none_two_in_a_real_merge_state(tmp_path, monkeypatch):
    # K-H through the CLI: the merge is started with --no-commit (the union is staged), the
    # environment is what the hook would see
    root = tmp_path / "c"
    _clean_repo(root, (O1, BAD_MODEL), with_hook=False)
    assert _gr(root, "merge", "--no-commit", "other").returncode == 0
    other_sha = _gr(root, "rev-parse", "other").stdout.strip()
    one = _cli(root, "--merge-parent", "env", env=_env_without_githead(**{f"GITHEAD_{other_sha}": "other"}))
    assert one.returncode == 1 and "MERGE_HEAD line 3" in one.stderr and "[model]" in one.stderr
    none = _cli(root, "--merge-parent", "env", env=_env_without_githead())
    assert none.returncode == 0 and "not in the environment (GITHEAD_*)" in none.stderr
    two = _cli(root, "--merge-parent", "env",
               env=_env_without_githead(**{f"GITHEAD_{other_sha}": "other", f"GITHEAD_{'e' * 40}": "x"}))
    assert two.returncode == 1 and other_sha in two.stderr and "e" * 40 in two.stderr
    notcommit = _cli(root, "--merge-parent", "env", env=_env_without_githead(**{f"GITHEAD_{'f' * 40}": "x"}))
    assert notcommit.returncode == 1 and "f" * 40 in notcommit.stderr and "is not a commit" in notcommit.stderr
    explicit = _cli(root, "--merge-parent", other_sha, env=_env_without_githead())
    assert explicit.returncode == 1 and "MERGE_HEAD line 3" in explicit.stderr
    # a parent that lacks the file reads as an empty other side
    monkeypatch.chdir(root)
    assert jv.get_parent_text(other_sha, "no/such/journal.jsonl") == ""


# ---- K-I: the 13(l) paragraph of the calibration protocol, key-presence with a negative control ----

# the keys, quoted from the DoD (the t-465 spec, Spec 1 R6) BEFORE the check was written
KEYS_13L = [
    "(l) MERGE ACKNOWLEDGEMENTS (B-401)",
    "git log --merges --full-history --since=<window start> -- logs/routing-log.jsonl",
    "`merge-accepts:<n>:<fields>` tokens",
    "case-insensitive content search for `merge-accepts:`",
    "positive control of the same form",
    "A token with no corrected value or no reason is a finding",
    "A token naming `by`",
    "unless its notes name the Lead's decision",
    'the explicit line "no merge acknowledgements"',
]


def _missing_keys(text: str, keys: list) -> list:
    flat = " ".join(text.split())
    return [k for k in keys if k not in flat]


def test_13l_paragraph_is_present_with_every_key():
    text = (REPO_ROOT / "PROCESS" / "WEEKLY_CALIBRATION_PROTOCOL.md").read_text(encoding="utf-8")
    assert _missing_keys(text, KEYS_13L) == []
    assert text.index("(k) DOC-DISPATCH WITNESS") < text.index("(l) MERGE ACKNOWLEDGEMENTS (B-401)") < text.index(
        "14. **A golden set")                                          # after 13(k), before item 14
    # the negative control: one key deliberately absent -> the check reports failure
    flat = " ".join(text.split())                                         # the paragraph is hard-wrapped
    assert _missing_keys(flat.replace("positive control of the same form", "a control"), KEYS_13L) == [
        "positive control of the same form"]
    assert _missing_keys("", KEYS_13L) == KEYS_13L


# =====================================================================================
# B-402: the collision WARN of decide_merge (K7, E10, E11), the declaration it reads
# =====================================================================================

def _collide(n_ids: int, first=100):
    """HEAD and MERGE_HEAD each issued the ids t-<first>.. (different agents, ts, worker refs):
    returns (staged, head, other, head_lines, other_lines). MERGE_HEAD-only staged lines are
    n_ids+2 .. 2*n_ids+1 (B1 is line 1)."""
    ids = [f"t-{first + i}" for i in range(n_ids)]
    hl = [_dump(_obj(agent="builder", worker_ref=f"cli:h-{t}", **_ok(task_id=t, ts="2026-07-10T09:00:00"))) for t in ids]
    ol = [_dump(_obj(agent="scout", category="recon", worker_ref=f"cli:o-{t}",
                     **_ok(task_id=t, ts="2026-07-10T09:30:00"))) for t in ids]
    return _text(B1, *hl, *ol), _text(B1, *hl), _text(B1, *ol), hl, ol


def _declared(label: str, *lines: str) -> jk.Segments:
    return jk.Segments(1, [(label, "why", tuple(jk.identity(json.loads(l)) for l in lines))])


def _decide(staged, head, other, segments, **kw):
    return jv.decide_merge(staged, head, other, NOW, segments=segments, **kw)


def test_collision_warn_lists_the_ids_the_range_and_the_door_and_never_changes_the_code():
    staged, head, other, hl, ol = _collide(3)
    code, violations, warnings = _decide(staged, head, other, jk.NO_SEGMENTS)
    assert (code, violations) == (0, []) and len(warnings) == 1
    w = warnings[0]
    assert "3 task id(s) issued by BOTH clones are not declared: t-100, t-101, t-102" in w
    assert "python tools/journal_keys.py declare --label <name> --lines 5-7 --why" in w
    assert "stage logs/journal-segments.json in this merge commit" in w
    assert "(a warning only, the code never changes)" in w


def test_collision_warn_in_the_hook_path_says_the_next_commit():
    staged, head, other, *_ = _collide(2)
    w = _decide(staged, head, other, jk.NO_SEGMENTS, hook_path=True)[2][0]
    assert "stage it in the next commit" in w and "in this merge commit" not in w


@pytest.mark.parametrize("n,more", [(10, None), (11, "and 1 more"), (14, "and 4 more")])
def test_collision_warn_cap_is_ten_ids(n, more):
    staged, head, other, *_ = _collide(n)
    w = _decide(staged, head, other, jk.NO_SEGMENTS)[2][0]
    shown = w.split("not declared: ", 1)[1].split(" -- ", 1)[0]
    assert f"{n} task id(s)" in w
    assert shown.startswith("t-100, t-101") and "t-109" in shown
    if more is None:
        assert " more" not in shown and shown.count("t-1") == 10
    else:
        assert shown.endswith(more) and shown.count("t-1") == 10 and "t-110" not in shown


def test_a_declaration_of_one_side_covers_the_id_and_a_partial_one_does_not():
    staged, head, other, hl, ol = _collide(3)
    # every MERGE_HEAD-only line declared -> no WARN; every HEAD-only line declared -> no WARN either
    assert _decide(staged, head, other, _declared("other", *ol)) == (0, [], [])
    assert _decide(staged, head, other, _declared("head", *hl)) == (0, [], [])
    # t-100 declared on the MERGE_HEAD side only: the other two ids still warn
    w = _decide(staged, head, other, _declared("other", ol[0]))[2]
    assert len(w) == 1 and "2 task id(s)" in w[0] and "t-101, t-102" in w[0] and "t-100," not in w[0]
    # an id with two lines on a side, only one declared: not covered
    extra = _dump(_obj(agent="scout", category="recon", worker_ref="cli:o-extra", **_ok(task_id="t-100", ts="2026-07-10T09:40:00",
                                                                                      event="accepted", by="opus")))
    staged2, other2 = _text(B1, *hl, *ol, extra), _text(B1, *ol, extra)
    w2 = _decide(staged2, head, other2, _declared("other", ol[0]))[2][0]
    # t-525 F3: look INSIDE the "not declared:" list (t-100 also appears in the still-delegated clause)
    assert "3 task id(s)" in w2 and "not declared: t-100, t-101, t-102 --" in w2


def test_collision_warn_names_the_declared_instances_still_open_and_a_qualified_closes_removes_them():
    staged, head, other, hl, ol = _collide(2)
    # t-100's MERGE_HEAD side is declared (open: a delegated, no accepted); t-101 collides undeclared
    seg = _declared("other", ol[0])
    w = _decide(staged, head, other, seg)[2]
    assert len(w) == 1 and "1 task id(s)" in w[0] and "t-101" in w[0]
    # t-525 F2: the clause says what it counts -- delegated with no accepted line, no qualified closes
    assert "declared instances delegated with no accepted line (and no closes:t-NNN@label): t-100@other" in w[0]
    assert "closes:t-NNN@<label>" in w[0] and "still open" not in w[0]
    closer = _dump({"ts": "2026-07-10T10:30:00", "event": "dispatch_skipped", "agent": "lead", "category": "x",
                    "notes": "closes:t-100@other the dispatch was accepted on its clone"})
    w = _decide(_text(B1, *hl, *ol, closer), head, other, seg)[2]
    assert len(w) == 1 and "declared instances delegated" not in w[0]
    bad_closer = closer.replace("closes:t-100@other", "closes:t-100@Other")        # a malformed label closes nothing
    w = _decide(_text(B1, *hl, *ol, bad_closer), head, other, seg)[2]
    assert "declared instances delegated with no accepted line (and no closes:t-NNN@label): t-100@other" in w[0]


def test_no_warn_when_no_id_has_lines_on_both_sides():
    # ids with lines on one side only are not collisions
    assert _decide(UNION, HEAD_TEXT, OTHER_TEXT, jk.NO_SEGMENTS)[2] != []       # t-002: both clones (the base fixtures)
    one_sided = _text(B1, H1, H2, O2)                                         # O2 is t-003, only MERGE_HEAD has it
    assert _decide(one_sided, HEAD_TEXT, _text(B1, O2), jk.NO_SEGMENTS)[2] == []


def _fake_repo(tmp_path: Path, journal: str, declaration) -> Path:
    repo = tmp_path / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "logs").mkdir()
    (repo / "logs" / "routing-log.jsonl").write_text(journal, encoding="utf-8")
    if declaration is not None:
        data = declaration if isinstance(declaration, bytes) else declaration.encode("utf-8")
        (repo / "logs" / "journal-segments.json").write_bytes(data)
    return repo


def test_segments_none_reads_the_repository_declaration_and_a_corrupt_file_only_adds_one_warn(tmp_path, monkeypatch):
    # E10: `None` = the declaration of the repository holding the validator, read the way the readers read it
    staged, head, other, hl, ol = _collide(2)
    base = _decide(staged, head, other, jk.NO_SEGMENTS)
    assert base[0] == 0 and len(base[2]) == 1
    for name, payload in [("corrupt", b"\x00\x01{{{"), ("non-utf8", b"\xff\xfe{"), ("list", b"[]"),
                          ("version-2", '{"version": 2, "segments": []}'), ("failing-check", '{"version": 1, "segments": ['
                           '{"label": "x", "why": "w", "lines": [["a", "t-100", "delegated", "scout", ""]]}]}')]:
        repo = _fake_repo(tmp_path / name, staged, payload)
        monkeypatch.setattr(jv, "__file__", str(repo / "tools" / "journal_validator.py"))
        got = jv.decide_merge(staged, head, other, NOW, segments=None)
        assert got[0] == base[0] and got[1] == base[1], name
        unreadable = [w for w in got[2] if "unreadable" in w]
        assert len(unreadable) == 1 and "logs/journal-segments.json is unreadable" in unreadable[0], name
        assert [w for w in got[2] if w not in unreadable] == base[2], name
    # an absent file is NO_SEGMENTS with no extra WARN
    repo = _fake_repo(tmp_path / "absent", staged, None)
    monkeypatch.setattr(jv, "__file__", str(repo / "tools" / "journal_validator.py"))
    assert jv.decide_merge(staged, head, other, NOW, segments=None) == base
    # a good declaration of the repository covers t-100's MERGE_HEAD side
    good = jk.dumps_declaration(_declared("other", ol[0]))
    repo = _fake_repo(tmp_path / "good", staged, good)
    monkeypatch.setattr(jv, "__file__", str(repo / "tools" / "journal_validator.py"))
    code, violations, warnings = jv.decide_merge(staged, head, other, NOW, segments=None)
    assert code == 0 and len(warnings) == 1 and "t-101" in warnings[0] and "t-100," not in warnings[0]


def test_the_warns_come_back_unreadable_declaration_then_collision_then_the_token(tmp_path, monkeypatch):
    # B-426 D9: the order of the three WARN sources is part of the result (a split must keep it)
    staged, head, other, hl, ol = _collide(2)
    tail = _ack("merge-accepts:2 everything is fine")                    # a bare token: clears nothing, WARNs
    staged = staged + tail + "\n"
    repo = _fake_repo(tmp_path / "corrupt", staged, b"\x00\x01{{{")
    monkeypatch.setattr(jv, "__file__", str(repo / "tools" / "journal_validator.py"))
    code, violations, warnings = jv.decide_merge(staged, head, other, NOW, segments=None)
    assert (code, violations) == (0, []) and len(warnings) == 3, warnings
    assert "journal-segments.json is unreadable" in warnings[0]
    assert "task id(s) issued by BOTH clones are not declared" in warnings[1]
    assert "names no field" in warnings[2]


def test_decide_merge_is_the_only_one_that_takes_segments():
    import inspect
    assert "segments" not in inspect.signature(jv.decide).parameters
    assert "segments" not in inspect.signature(jv.decide_with_warnings).parameters
    p = inspect.signature(jv.decide_merge).parameters["segments"]
    assert p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is None


# ---- K7 end to end, both merge paths, real git ----

@needs_git
def test_k7_conflicted_merge_the_warn_fires_and_a_declaration_in_the_merge_commit_clears_it(tmp_path, monkeypatch, capsys):
    root = tmp_path / "m"
    _conflicted_merge(root)                                               # staged union: B1 H1 H2 O1 O2; O1 = t-002 (collides with H1/H2)
    monkeypatch.chdir(root)
    assert jv.main([]) == 0
    err = capsys.readouterr().err
    assert "issued by BOTH clones are not declared: t-002" in err and "--lines 4-5" in err
    assert "stage logs/journal-segments.json in this merge commit" in err
    # the door: declare the other clone's t-002 line (line 4) and stage the file into the merge commit
    assert jk.main(["--journal", str(root / "logs" / "routing-log.jsonl"), "declare", "--label", "other",
                    "--lines", "4-4", "--why", "t-002 was issued by both clones"]) == 0
    _g(root, "add", "logs/journal-segments.json")
    assert jv.main([]) == 0
    assert capsys.readouterr().err == ""
    # a broken declaration staged into the merge commit is a FAIL, whatever the journal says
    _write(root, "logs/journal-segments.json", "{broken")
    _g(root, "add", "logs/journal-segments.json")
    assert jv.main([]) == 1
    assert "journal-segments.json is unreadable" in capsys.readouterr().err


# ---- K7 clean path: the hook's CLI says "the next commit" ----

def test_f6_one_split_lines_and_one_git_diff_per_run(monkeypatch):
    assert jv.split_lines is jk.split_lines                      # the gate and the readers share one implementation
    calls = []

    def fake_git(*args):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout="somewhere/else.txt\n", stderr="")

    monkeypatch.setattr(jv, "_git", fake_git)
    monkeypatch.setattr(jv, "is_declaration_staged", _REAL_IS_DECL)        # the REAL wrappers (the autouse stubs off)
    monkeypatch.setattr(jv, "get_staged_declaration", _REAL_GET_DECL)
    assert jv.main([]) == 0
    assert [c for c in calls if c[:2] == ("diff", "--cached")] == [("diff", "--cached", "--name-only")]   # asked once
    assert jv._STAGED_CACHE is None                                # and the cache does not outlive the run
    jv.is_journal_staged()
    jv.is_journal_staged()
    assert len([c for c in calls if c[0] == "diff"]) == 3          # outside a run every ask is a fresh git call


def test_f5_the_live_pre_merge_commit_hook_calls_the_journal_validator_after_forge_metrics():
    # t-525 F5: the e2e tests above use a SYNTHETIC hook, and wiring_check only asks that the file
    # exists -- nothing else pins the placed content. RED until the Lead places the B-401 hook
    # content on .githooks/pre-merge-commit (the placement commit turns it green).
    text = (REPO_ROOT / ".githooks" / "pre-merge-commit").read_text(encoding="utf-8")
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    forge, validator = "python tools/forge_metrics.py --check", "python tools/journal_validator.py --merge-parent env"
    assert forge in lines, lines
    assert validator in lines, "the hook does not run the journal validator for the merged parent (B-401)"
    assert lines.index(forge) < lines.index(validator)
    assert "set -e" in lines


@needs_git
def test_k7_clean_merge_the_hook_prints_the_warn_with_the_next_commit_door(tmp_path):
    root = tmp_path / "c"
    _clean_repo(root, (O1, O2))
    proc = _gr(root, "merge", "other", "-m", "merge other")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)               # a WARN never blocks
    out = proc.stdout + proc.stderr
    assert "issued by BOTH clones are not declared: t-002" in out and "stage it in the next commit" in out
