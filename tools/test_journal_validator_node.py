"""Tests for the `node` field of the journal gate (t-797 F5-2, node N3): rule 18 of tools/journal_validator.py and node_warnings.

The invariants under test: (1) a NEW line whose `node` is present and is not `<slug>/<N>/<id>` is a violation with the FR-1 text, an
ABSENT field never is, and an OLD line is never judged (append-only; spec edges E25-E27); (2) the gate asks journal_keys.node_of and
holds no regex of its own (one reader of the form); (3) F-9 (c): a NEW `delegated` dated NODE_WARN_FROM or later that names its node
only in `notes` earns a WARN, never a refusal -- none before the date, none when the field is there, none for a line with no token.

Edges (spec section 5):
  E25  a `delegated` with no `node` after the field appeared: no violation; a WARN only with a token in notes, from the date on.
  E26  field and token disagree -> the field wins, a WARN; two tokens, no field -> a WARN naming `two_tokens`.
  E27  a `node` that is not a string (list, dict, number): a violation on a new line; nothing on an old one, never a TypeError.

Run from the repo root: python -m pytest tools/test_journal_validator_node.py -q
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import journal_keys as jk  # noqa: E402
import journal_validator as jv  # noqa: E402

NOW = jv.datetime.datetime(2026, 10, 15, 12, 0, 0)
FROM = jv.NODE_WARN_FROM                                  # "2026-10-15"
DAY_BEFORE = "2026-10-14T09:00:00"
DAY_OF = "2026-10-15T09:00:00"
GOOD = "forge/5/F5-2"
FR1_TAIL = "is not `<slug>/<N>/<id>`; write e.g. `forge/5/F5-2`"
FEATURE = "F01"                                           # a registered feature on every line: the `feature` WARN is not under test here
FEATURES = {FEATURE}
NO_VALUE = object()                                      # "the field is not there at all"


def line(event="delegated", ts=DAY_OF, task_id="t-002", node=NO_VALUE, notes="work on a node", **kw) -> str:
    obj = {"ts": ts, "event": event, "agent": "builder", "category": "implementation", "notes": notes, "task_id": task_id,
           "model": "sonnet", "worker_ref": "agent:x1", "feature": FEATURE}
    if event in ("accepted", "rejected"):
        obj.update(by="opus", witness="w", basis="critic", failure_class="spec", attempt=1)
    if node is not NO_VALUE:
        obj["node"] = node
    obj.update(kw)
    return json.dumps(obj, ensure_ascii=False)


HEAD_LINE = line(task_id="t-001", ts="2026-10-14T08:00:00", notes="the first line")
HEAD = HEAD_LINE + "\n"


def staged(*new_lines: str, head: str = HEAD) -> str:
    return head + "".join(l + "\n" for l in new_lines)


def gate(*new_lines: str, head: str = HEAD):
    """(code, violations, warnings) of the ordinary gate over new lines appended to `head`."""
    return jv.decide_with_warnings(staged(*new_lines, head=head), head, NOW, FEATURES)


# ----- the violation: a `node` present and not a node -----------------------------------------------------------------------

@pytest.mark.parametrize("node", ["forge/5/F5-2", "conductor/2/C2-1", "forge/4/D9", "a/1/b", "gitlab-mirror/12/Node-3"])
def test_a_node_in_the_form_is_clean_on_a_new_line(node):
    code, violations, warnings = gate(line(node=node, notes="no token here"))
    assert (code, violations, warnings) == (0, [], [])


def test_a_bare_id_is_a_violation_with_the_fr1_text():
    code, violations, _w = gate(line(node="F5-2"))
    assert code == 1 and len(violations) == 1, violations
    v = violations[0]
    assert v.startswith("line 2 event='delegated' task_id='t-002': `node` = 'F5-2' " + FR1_TAIL), v
    assert v.endswith("(rule 18)")


@pytest.mark.parametrize("bad", [
    "forge/5", "forge/5/", "/5/F5-2", "Forge/5/F5-2", "forge/05/F5-2", "forge/0/F5-2", "forge/5/5-2", "forge/5/F5-2/x", "forge 5 F5-2",
    "forge/5/F5-2\n", " forge/5/F5-2", "forge/5/F5-2 ", "", "forge/5/F5_2", "forge/5/Ф",
])
def test_a_string_outside_the_form_is_a_violation(bad):
    code, violations, _w = gate(line(node=bad))
    assert code == 1 and len(violations) == 1, (bad, violations)
    assert "`node` = %r %s" % (bad, FR1_TAIL) in violations[0]                     # the repr of the value is in the text


@pytest.mark.parametrize("bad", [["forge/5/F5-2"], {"id": GOOD}, 5, 1.5, True, False, [], {}])
def test_e27_a_node_that_is_not_a_string_is_a_violation_never_a_traceback(bad):
    code, violations, _w = gate(line(node=bad))
    assert code == 1 and len(violations) == 1, (bad, violations)
    assert "`node` = %r %s" % (bad, FR1_TAIL) in violations[0]


def test_an_absent_field_is_never_a_violation_whatever_the_event():
    for event, task_id in (("delegated", "t-002"), ("accepted", "t-001"), ("rejected", "t-001")):
        code, violations, warnings = gate(line(event=event, task_id=task_id))
        assert (code, violations, warnings) == (0, [], []), event


def test_null_reads_as_absent_like_node_of_does():
    """journal_keys.node_of: `a field that is present (not absent, not null) decides alone`; the gate mirrors its reader."""
    assert jk.node_of({"node": None, "notes": "x"}) == (None, "no_node")
    assert gate(line(node=None)) == (0, [], [])


@pytest.mark.parametrize("event", ["accepted", "rejected"])
def test_the_field_is_legal_on_the_other_events_with_the_same_check(event):
    assert gate(line(event=event, node=GOOD, task_id="t-001")) == (0, [], [])
    code, violations, _w = gate(line(event=event, node="F5-2", task_id="t-001"))
    assert code == 1 and len(violations) == 1 and FR1_TAIL in violations[0] and "event=%r" % event in violations[0]


def test_two_bad_lines_two_violations_each_with_its_own_line_number():
    code, violations, _w = gate(line(task_id="t-002", node="F5-2"), line(task_id="t-003", node=[1]))
    assert code == 1 and [v.split(":")[0] for v in violations] == ["line 2 event='delegated' task_id='t-002'",
                                                                    "line 3 event='delegated' task_id='t-003'"]


def test_the_violation_does_not_depend_on_the_date_only_the_warn_does():
    assert gate(line(ts=DAY_BEFORE, node="F5-2"))[0] == 1


# ----- the gate's scope: new lines only ------------------------------------------------------------------------------------

@pytest.mark.parametrize("bad", ["F5-2", ["a"], {"a": 1}, 7])
def test_an_old_line_with_a_bad_node_is_never_a_refusal(bad):
    head = HEAD + line(task_id="t-002", ts="2026-10-14T09:00:00", node=bad) + "\n"
    code, violations, warnings = gate(line(task_id="t-003"), head=head)
    assert (code, violations, warnings) == (0, [], [])


def test_the_journal_before_any_node_field_passes_unchanged():
    old = [line(task_id="t-00%d" % n, ts="2026-10-1%dT08:00:00" % n, notes="work of that day") for n in range(1, 4)]
    head = "".join(l + "\n" for l in old)
    assert jv.decide_with_warnings(head + line(task_id="t-004", notes="plain") + "\n", head, NOW, FEATURES) == (0, [], [])


# ----- the merge: a foreign line is form-checked too, the door is merge-accepts:<n>:node ------------------------------------

def _merge(bad: str, *tail: str):
    base = line(task_id="t-001", ts="2026-10-14T08:00:00", notes="the base")
    mine = line(task_id="t-002", ts="2026-10-14T10:00:00", notes="mine")
    def text(*lines):
        return "".join(l + "\n" for l in lines)
    return jv.decide_merge(text(base, mine, bad, *tail), text(base, mine), text(base, bad), NOW, FEATURES, segments=jk.NO_SEGMENTS)


def test_a_foreign_line_with_a_bad_node_is_refused_by_field_and_the_door_clears_it():
    bad = line(task_id="t-003", ts="2026-10-14T09:00:00", node="F5-2")
    code, violations, _w = _merge(bad)
    assert code == 1 and len(violations) == 1, violations
    assert "[node]" in violations[0] and "merge-accepts:2:node" in violations[0] and FR1_TAIL in violations[0]
    ack = json.dumps({"ts": "2026-10-15T11:00:00", "event": "dispatch_skipped", "agent": "lead", "category": "ack",
                      "notes": "merge-accepts:2:node forge/5/F5-2 -- the other clone wrote a bare id"})
    assert _merge(bad, ack)[:2] == (0, [])


def test_a_foreign_line_with_a_good_node_or_none_is_clean():
    assert _merge(line(task_id="t-003", ts="2026-10-14T09:00:00", node=GOOD))[:2] == (0, [])
    assert _merge(line(task_id="t-003", ts="2026-10-14T09:00:00"))[:2] == (0, [])


# ----- one reader of the form: the gate asks journal_keys.node_of -----------------------------------------------------------

RE_CALLS = {"compile", "match", "search", "fullmatch", "findall", "finditer", "sub", "subn", "split"}
NODE_RE_NAMES = {"NODE_RE", "NODE_TOKEN_RE"}
NODE_FRAGMENTS = ("[1-9][0-9]*", "[a-z][a-z0-9-]*", "[A-Za-z][A-Za-z0-9-]*")      # pieces of NODE_RE / NODE_TOKEN_RE


def node_pattern_copies(source: str) -> list[str]:
    """The shapes of a second copy of the node form in a module source: a name NODE_RE / NODE_TOKEN_RE bound here, a string literal
    carrying a piece of the pattern, a `re.<call>` whose literal pattern holds a slash or the word node. [] = the module is clean."""
    found: list[str] = []
    for n in ast.walk(ast.parse(source)):
        targets = n.targets if isinstance(n, ast.Assign) else [n.target] if isinstance(n, (ast.AnnAssign, ast.AugAssign)) else []
        found += ["name %s" % t.id for t in targets if isinstance(t, ast.Name) and t.id in NODE_RE_NAMES]
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            found += ["literal %r" % f for f in NODE_FRAGMENTS if f in n.value]
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "re" and n.func.attr in RE_CALLS and n.args
                and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)
                and ("/" in n.args[0].value or "node" in n.args[0].value.lower())):
            found.append("re.%s(%r)" % (n.func.attr, n.args[0].value))
    return found


def test_the_gate_consults_node_of_and_holds_no_regex_of_the_form(monkeypatch):
    monkeypatch.setattr(jv._jk, "node_of", lambda obj: (None, "node_not_form"))
    assert gate(line(node=GOOD))[0] == 1                                              # even a good value: the reader said no
    monkeypatch.setattr(jv._jk, "node_of", lambda obj: (obj.get("node"), None))
    assert gate(line(node="F5-2")) == (0, [], [])                                    # and a bare id: the reader said yes
    assert node_pattern_copies(Path(jv.__file__).read_text(encoding="utf-8")) == []   # no copy of NODE_RE / NODE_TOKEN_RE here


@pytest.mark.parametrize("copy", [
    'import re\nX = re.compile(r"^[a-z][a-z0-9-]*/[1-9][0-9]*/[A-Za-z][A-Za-z0-9-]*$")\n',       # a re.compile of NODE_RE
    'import re\nX = re.compile(r"([a-z][a-z0-9-]*)/([1-9][0-9]*)[ /]")\n',                          # the NODE_TOKEN_RE shape
    'P = "^[a-z][a-z0-9-]*/[1-9][0-9]*/x"\n',                                                      # a string literal of the pattern
    'import re\nok = re.match(r"^[a-z]+/[0-9]+/[a-z]+$", s)\n',                                            # an inline re.match
    'import journal_keys\nNODE_RE = journal_keys.NODE_RE\n',                                       # a second NODE_RE name
    'NODE_TOKEN_RE: object = None\n',
])
def test_the_copy_detector_sees_every_shape_it_is_asked_about(copy):
    """Negative control of the pin above: each shape of a second copy is found; the clean module is not."""
    assert node_pattern_copies(copy) != []
    assert node_pattern_copies("import re\nTS = re.compile(r'^[0-9]{4}$')\nnode = _jk.node_of(obj)\n") == []


def test_the_warn_side_consults_node_of_too(monkeypatch):
    """The WARN reader is journal_keys.node_of as well: a node it returns for a field-less line with no token in notes is named."""
    plain = line(notes="no token anywhere")
    assert gate(plain) == (0, [], [])                                                 # the real reader: silence
    monkeypatch.setattr(jv._jk, "node_of", lambda obj: ("x/1/Y1", None))
    code, violations, warnings = gate(plain)
    assert code == 0 and violations == [] and len(warnings) == 1, warnings
    assert "WARN no 'node' field" in warnings[0] and "'x/1/Y1'" in warnings[0]
    monkeypatch.setattr(jv._jk, "node_of", lambda obj: ("x/1/Y1", "node_token_differ"))
    _c, _v, warnings = gate(line(node=GOOD, notes="no token anywhere"))
    assert len(warnings) == 1 and "another node" in warnings[0] and "'x/1/Y1'" in warnings[0]   # the field-vs-token branch too


def test_the_node_pattern_itself_refuses_a_bare_id():
    """The premise of the bare-id test, stated at the reader: with NODE_RE accepting a bare id (mutation U11) this file fails."""
    assert jk.NODE_RE.match("F5-2") is None and jk.NODE_RE.match(GOOD) is not None
    assert jk.node_of({"node": "F5-2"}) == (None, "node_not_form")
    assert jk.node_of({"node": GOOD})[0] == GOOD


# ----- the WARN (F-9 (c)): a token in notes, no field, from NODE_WARN_FROM -------------------------------------------------

def test_the_warn_date_is_the_merge_day_of_n3():
    assert FROM == "2026-10-15" and jv.NODE_WARN_FROM == FROM


@pytest.mark.parametrize("notes", ["F5-2 of forge/5 F5-2 started", "node forge/5/F5-2", "forge/5 F5-2: the form (t-797)"])
def test_f9c_a_token_and_no_field_from_the_date_on_is_a_warn_never_a_refusal(notes):
    code, violations, warnings = gate(line(notes=notes))
    assert code == 0 and violations == [] and len(warnings) == 1, warnings
    w = warnings[0]
    assert w.startswith("line 2 event='delegated' task_id='t-002': WARN no 'node' field") and "'forge/5/F5-2'" in w
    assert w.endswith("(a warning only, the journal is not blocked)") and "forge/5/F5-2" in w


def test_f9c_none_before_the_date():
    assert gate(line(ts=DAY_BEFORE, notes="forge/5 F5-2 started")) == (0, [], [])


def test_f9c_none_with_the_field_present_and_the_same_token():
    assert gate(line(node=GOOD, notes="forge/5 F5-2 started")) == (0, [], [])
    assert gate(line(node=GOOD, notes="forge/5/F5-2 started")) == (0, [], [])


def test_f9c_none_with_the_field_and_no_token_and_none_with_neither():
    assert gate(line(node=GOOD, notes="no token")) == (0, [], [])
    assert gate(line(notes="work outside the piles, no node anywhere")) == (0, [], [])


@pytest.mark.parametrize("notes", ["3070 passed", "conductor/1 node is meant", "failed/3070 passed", "see path/to/file.py"])
def test_f9c_prose_that_only_looks_like_a_token_is_silent(notes):
    assert gate(line(notes=notes)) == (0, [], [])


def test_f9c_only_delegated_is_warned():
    for event in ("accepted", "rejected"):
        assert gate(line(event=event, task_id="t-001", notes="forge/5 F5-2 merged")) == (0, [], []), event


def test_e26_the_field_and_a_token_that_disagree_the_field_wins_and_a_warn_says_so():
    code, violations, warnings = gate(line(node="forge/5/F5-2", notes="the work of forge/5 F5-10"))
    assert code == 0 and violations == [] and len(warnings) == 1, warnings
    assert "'node' = 'forge/5/F5-2' but notes name another node (node_token_differ)" in warnings[0] and "'forge/5/F5-2'" in warnings[0]
    assert gate(line(node="forge/5/F5-2", notes="forge/5 F5-2 and forge/5 F5-10"))[2]       # a second token also disagrees
    assert gate(line(node="forge/5/F5-2", ts=DAY_BEFORE, notes="forge/5 F5-10"))[2] == []   # not before the date


def test_e26_two_tokens_and_no_field_a_warn_naming_two_tokens():
    code, violations, warnings = gate(line(notes="forge/5 F5-2 then forge/5 F5-10"))
    assert code == 0 and violations == [] and len(warnings) == 1, warnings
    assert "two_tokens" in warnings[0] and "WARN no 'node' field" in warnings[0]


def test_a_bad_field_is_a_violation_and_earns_no_warn_even_with_a_token():
    code, violations, warnings = gate(line(node="F5-2", notes="forge/5 F5-2 started"))
    assert code == 1 and len(violations) == 1 and warnings == []


def test_null_with_a_token_is_warned_like_an_absent_field():
    code, _v, warnings = gate(line(node=None, notes="forge/5 F5-2 started"))
    assert code == 0 and len(warnings) == 1 and "no 'node' field" in warnings[0]


def test_node_warnings_skips_what_it_cannot_read():
    new = ["not json", "[1, 2]", json.dumps({"event": ["x"], "ts": DAY_OF}), json.dumps({"event": "delegated", "ts": 5, "notes": "forge/5 F5-2"}),
           json.dumps({"event": "delegated", "ts": "garbage", "notes": "forge/5 F5-2"}),
           json.dumps({"event": "delegated", "ts": DAY_OF, "notes": ["forge/5 F5-2"]})]
    assert jv.node_warnings(new, [HEAD_LINE]) == []


def test_the_warn_line_number_counts_the_head_lines():
    new = [line(task_id="t-002", notes="plain"), line(task_id="t-003", notes="forge/5 F5-2")]
    warnings = jv.node_warnings(new, [HEAD_LINE, HEAD_LINE])
    assert len(warnings) == 1 and warnings[0].startswith("line 4 event='delegated' task_id='t-003'")


def test_a_merge_tail_line_earns_the_warn_too():
    base = line(task_id="t-001", ts="2026-10-14T08:00:00", notes="the base")
    tail = line(task_id="t-002", notes="forge/5 F5-2 started")
    code, violations, warnings = jv.decide_merge(base + "\n" + tail + "\n", base + "\n", base + "\n", NOW, FEATURES, segments=jk.NO_SEGMENTS)
    assert code == 0 and violations == [] and any("WARN no 'node' field" in w for w in warnings), warnings


def test_the_warn_never_changes_the_exit_code():
    plain = gate(line(notes="no node"))[0]
    warned = gate(line(notes="forge/5 F5-2"))
    assert warned[2] and warned[0] == plain == 0


# ----- F6-16 (critic t-815 F-5): the dated WARNs share ONE skeleton and ONE line shape --------------------------------------

WARN_SUFFIX = " (a warning only, the journal is not blocked)"


def test_the_warn_line_shape_is_pinned_once():
    assert jv._warn_line("line 7 event='x' task_id='t'", "body") == "line 7 event='x' task_id='t': WARN body" + WARN_SUFFIX


def test_both_dated_warns_wear_the_one_shape_and_the_one_tag():
    node = jv.node_warnings([line(task_id="t-003", notes="forge/5 F5-2")], [HEAD_LINE])
    feat = jv.feature_warnings([line(task_id="t-003", feature=None)], [HEAD_LINE], FEATURES)
    for w, ev in ((node, "delegated"), (feat, "delegated")):
        assert len(w) == 1 and w[0].startswith("line 2 event=%r task_id='t-003': WARN " % ev) and w[0].endswith(WARN_SUFFIX), w
    assert "no 'node' field" in node[0] and "no 'feature' field" in feat[0]


def test_dated_new_objs_filters_by_event_and_by_the_date_at_and_below_it():
    new = [line(ts=DAY_BEFORE, task_id="t-1"), line(ts=DAY_OF, task_id="t-2"), line(ts="2026-10-15", task_id="t-3"),
           line(event="accepted", task_id="t-4")]
    got = list(jv._dated_new_objs(new, [HEAD_LINE, HEAD_LINE], {"delegated"}, FROM))
    assert [(o["task_id"], tag.split()[1]) for o, tag in got] == [("t-2", "4")]       # t-3 has no parseable ts (date only)
    both = list(jv._dated_new_objs(new, [], {"delegated", "accepted"}, FROM))
    assert [o["task_id"] for o, _ in both] == ["t-2", "t-4"] and both[1][1].startswith("line 4 event='accepted' ")
    assert list(jv._dated_new_objs(new, [], {"delegated"}, "2026-10-14"))[0][0]["task_id"] == "t-1"       # the date is a bound, AT it counts


def test_dated_new_objs_skips_what_it_cannot_read_and_never_hashes_a_list_event():
    new = ["not json", "[1, 2]", json.dumps({"event": ["delegated"], "ts": DAY_OF}), json.dumps({"event": {"a": 1}, "ts": DAY_OF}),
           json.dumps({"event": "delegated", "ts": 5}), json.dumps({"event": "delegated", "ts": "garbage"}),
           json.dumps({"event": "delegated"})]
    assert list(jv._dated_new_objs(new, [HEAD_LINE], {"delegated"}, FROM)) == []


def test_both_dated_warns_go_through_the_one_skeleton(monkeypatch):
    calls = []
    real = jv._dated_new_objs
    monkeypatch.setattr(jv, "_dated_new_objs", lambda *a: calls.append(a[2:]) or real(*a))
    jv.node_warnings([], [])
    jv.feature_warnings([], [], FEATURES)
    assert calls == [(jv.NODE_WARN_EVENTS, jv.NODE_WARN_FROM), (jv.FEATURE_WARN_EVENTS, jv.FEATURE_WARN_FROM)]
