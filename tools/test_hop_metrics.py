"""Tests for tools/hop_metrics.py (t-797 F5-2 M3, node N2): chars and tokens per hop of a task chain.

Every test builds its own tiny world in tmp_path -- a journal and a `projects` folder (a main transcript plus
subagents/agent-<id>.jsonl) -- and passes `root`/`projects` (F14: nothing touches the home folder). The edges
E12-E31 of the spec are named in the test names; U4 (a hop with no transcript is n/d, not 0), U5 (the prose is the
WHOLE text, not the lines above the first header) and U10 (an intake is read from text, never from a tool_result)
are killed here.

Run from the repo root: python -m pytest tools/test_hop_metrics.py -q
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hop_metrics as hm  # noqa: E402

TOOLS = Path(__file__).resolve().parent
REPORT = "C:\\fake\\docs\\tasks\\handoffs\\t-001-report.md"
PROMPT = ("Task t-001 intro line.\n\ngiven: C:\\fake\\a.md\nowns:\nC:\\fake\\b.py\nnon-goals: none\n"
          "handoff: " + REPORT + "\nedges: none -- x\nDoD: `pytest -q`\n")


def _dump(obj):
    return json.dumps(obj, ensure_ascii=False)


class World:
    """A journal (logs/routing-log.jsonl) and a projects folder in tmp_path."""

    def __init__(self, tmp_path):
        self.root = tmp_path / "repo"
        (self.root / "logs").mkdir(parents=True)
        self.projects = tmp_path / "projects"
        self.proj = self.projects / "proj-a"
        self.proj.mkdir(parents=True)
        self.events = []

    def delegated(self, tid, aid="aaa1", agent="scout", ts="2026-10-15T04:00:00", notes="n", ref=None, **extra):
        ev = {"ts": ts, "event": "delegated", "agent": agent, "task_id": tid, "category": "recon", "notes": notes,
              "worker_ref": ref if ref is not None else "agent:%s" % aid}
        ev.update(extra)
        self.events.append(ev)
        return ev

    def flush(self, name="routing-log.jsonl"):
        (self.root / "logs" / name).write_text("".join(_dump(e) + "\n" for e in self.events), encoding="utf-8")

    def worker(self, aid, session="sess-1", prompt=PROMPT, requests=None, handback="the report text", kind="scout"):
        """subagents/agent-<aid>.jsonl: the dispatch, assistant lines with usage, a SubagentHandback; and its meta."""
        folder = self.proj / session / "subagents"
        folder.mkdir(parents=True, exist_ok=True)
        lines = [_dump({"type": "user", "message": {"role": "user", "content": prompt}})]
        for rid, usages in (requests or []):
            for i, u in enumerate(usages):
                lines.append(_dump({"type": "assistant", "requestId": rid, "uuid": "%s-%d" % (rid, i),
                                    "message": {"role": "assistant", "model": "m", "content": [{"type": "text", "text": "t"}],
                                                "usage": u}}))
        if handback is not None:
            lines.append(_dump({"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "hb", "name": "SubagentHandback", "input": {"message": handback}}]}}))
        (folder / ("agent-%s.jsonl" % aid)).write_text("\n".join(lines) + "\n", encoding="utf-8")
        (folder / ("agent-%s.meta.json" % aid)).write_text(_dump({"agentType": kind}), encoding="utf-8")

    def main(self, lines, session="sess-1"):
        path = self.proj / (session + ".jsonl")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def collect(self, **kw):
        self.flush()
        return hm.collect(self.root, self.projects, **kw)


def _call(tid, name, inp):
    return _dump({"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": tid, "name": name, "input": inp}]}})


def _result(tid, text):
    return _dump({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tid, "content": text}]}})


def _launch(tid, aid):
    return _result(tid, "Async agent launched successfully. (internal metadata) agentId: %s (use SendMessage)" % aid)


def _intake(aid, body="[hand-back] the report"):
    return _dump({"type": "user", "message": {"role": "user", "content":
                  'Another Claude session sent a message:\n<agent-message from="%s">\n%s\n</agent-message>' % (aid, body)}})


def _hop(report, task):
    for chain in report["chains"] + [{"hops": report["unlinked"]["hops"]}]:
        for h in chain["hops"]:
            if h["task_id"] == task:
                return h
    raise AssertionError("no hop %s in the report" % task)


# --- the weights ------------------------------------------------------------------------------------------------

def test_unit_weights_are_the_one_carrier_and_input_is_the_assumption():
    assert hm.UNIT_WEIGHTS == {"input": 1, "cache_write": 2, "cache_read": 0.1, "output": 5}
    assert "ASSUMPTION" in hm.__doc__ and "check 17" in hm.__doc__


def test_units_are_the_weighted_sum_over_requests_with_the_max_per_field_inside_one(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    big = {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000}
    w.worker("aaa1", requests=[("r1", [dict(big, output_tokens=17), dict(big, output_tokens=17), dict(big, output_tokens=485)]),
                               ("r2", [{"input_tokens": 1, "cache_read_input_tokens": 500, "output_tokens": 20}])])
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["units"] == 2886.0 and h["requests"] == 2          # (10 + 200 + 100 + 2425) + (1 + 0 + 50 + 100)


# --- E16 E17 E30: the worker side, n/d and never 0 --------------------------------------------------------------

def test_e16_u4_a_hop_without_a_transcript_is_nd_not_zero_and_stays_out_of_the_totals(tmp_path):
    """U4: the mutant gives such a hop units 0 / brief 0 (a measured zero) instead of n/d."""
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.delegated("t-002", "ghost", node="forge/5/F5-9")                 # agent id with no transcript
    w.delegated("t-003", ref="cli:20261015", node="forge/5/F5-9")      # a worker_ref that is not an agent
    w.delegated("t-004", ref="retro:t-003", node="forge/5/F5-9")
    w.worker("aaa1", requests=[("r1", [{"input_tokens": 4, "output_tokens": 1}])])
    rep = w.collect(node="forge/5/F5-9")
    ghost, cli, retro = _hop(rep, "t-002"), _hop(rep, "t-003"), _hop(rep, "t-004")
    for h in (ghost, cli, retro):
        assert h["units"] is None and h["brief_chars"] is None and h["handback_chars"] is None and h["chars"] is None
        assert list(h["nd"]) == ["worker"]
    assert ghost["nd"]["worker"]["code"] == "no_transcript" and cli["nd"]["worker"]["code"] == "bad_ref"
    chain = rep["chains"][0]
    assert chain["totals"]["units"] == 9.0 and chain["totals"]["nd_hops"] == 4       # the 3 are counted, not summed
    assert rep["nd"] == {"hops": 4, "reasons": {"bad_ref": 2, "no_main": 1, "no_transcript": 1}}   # + t-001: no main here
    text = hm.render(rep)
    assert "n/d hops: 4 (bad_ref x2, no_main x1, no_transcript x1)" in text and "| t-002 | scout |" in text
    assert re.search(r"\| t-002 .*\| n/d \| n/d \|", text)


def test_e16_an_agent_id_in_two_sessions_is_ambiguous_and_nd(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", session="sess-1")
    w.worker("aaa1", session="sess-2")
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["units"] is None and h["nd"]["worker"]["code"] == "no_transcript"


def test_e17_zero_bytes_no_usage_broken_lines_and_a_non_numeric_usage(tmp_path):
    w = World(tmp_path)
    for tid, aid in (("t-001", "z0"), ("t-002", "nou"), ("t-003", "bad"), ("t-004", "brk")):
        w.delegated(tid, aid, node="forge/5/F5-9")
    folder = w.proj / "sess-1" / "subagents"
    folder.mkdir(parents=True)
    (folder / "agent-z0.jsonl").write_bytes(b"")
    w.worker("nou", requests=[])
    w.worker("bad", requests=[("r1", [{"output_tokens": "many"}])])
    w.worker("brk", requests=[("r1", [{"output_tokens": 3}])])
    with open(folder / "agent-brk.jsonl", "a", encoding="utf-8") as fh:
        fh.write("not json at all\n" + "[" * 5000 + "\n")
    rep = w.collect(node="forge/5/F5-9")
    zero, nou, bad, brk = (_hop(rep, t) for t in ("t-001", "t-002", "t-003", "t-004"))
    assert zero["units"] is None and zero["nd"]["units"]["code"] == "no_usage" and zero["nd"]["brief"]["code"] == "no_brief"
    assert zero["nd"]["handback_chars"]["code"] == "no_text"                              # E30 for the empty file
    assert nou["nd"]["units"]["code"] == "no_usage" and bad["nd"]["units"] == {"code": "bad_usage", "why": "bad usage value"}
    assert brk["units"] == 15.0 and "units" not in brk["nd"]                              # broken lines are skipped


def test_e30_a_hand_back_without_text_is_nd_for_chars_and_form(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", requests=[("r1", [{"output_tokens": 1}])], handback=None)
    w.proj.joinpath("sess-1", "subagents", "agent-aaa1.jsonl").write_text(
        _dump({"type": "user", "message": {"content": PROMPT}}) + "\n" + _dump({"type": "assistant", "requestId": "r", "message": {
            "usage": {"output_tokens": 1}, "content": [{"type": "tool_use", "id": "x", "name": "Read", "input": {}}]}}) + "\n",
        encoding="utf-8")
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["handback_chars"] is None and h["form"] is None and h["flags"] is None
    assert h["nd"]["handback_chars"]["code"] == "no_text" and h["units"] == 5.0


def test_the_form_of_a_v1_digest_and_of_prose_is_read_from_the_handback(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.delegated("t-002", "bbb2", node="forge/5/F5-9")
    w.worker("aaa1", handback="digest: v1 t-001\n## Objects\n| id | kind | gist | paths | status | owner | links | ev |\n"
                              "|---|---|---|---|---|---|---|---|\n| o1 | claim | a gist | a.py | done | — | — | R1 |\n"
                              "## Trail\n| tid | op | target | pattern / range | flags | result | control |\n|---|---|---|---|---|---|---|\n"
                              "| R1 | read | a.py | all | — | read a.py:1 | — |")
    w.worker("bbb2", handback="plain prose report")
    rep = w.collect(node="forge/5/F5-9")
    v1, prose = _hop(rep, "t-001"), _hop(rep, "t-002")
    assert (v1["form"], v1["flags"]) == ("v1", 0) and (prose["form"], prose["flags"]) == ("none", None)
    assert prose["handback_chars"] == len("plain prose report")


# --- E12-E15: the prose of a brief ------------------------------------------------------------------------------

def test_e12_u5_prose_after_the_manifest_block_counts(tmp_path):
    """U5: the previous reading counted only the lines above the first header (here 1 of 4)."""
    prompt = ("Intro line one.\n\ngiven: C:\\fake\\a.md\nhandoff: " + REPORT + "\n\nAfter the manifest: prose two.\n"
              "After the manifest: prose three.\n\nowns:\nC:\\fake\\b.py\n\nPlus a closing line four.\n")
    count, degraded, handoff = hm.prose_lines(prompt)
    assert (count, degraded, handoff) == (4, False, [REPORT])
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", prompt=prompt)
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["brief_prose_lines"] == 4


def test_e13_prose_glued_to_a_header_is_read_as_manifest(tmp_path):
    count, _d, _h = hm.prose_lines("Intro.\n\ngiven: C:\\fake\\a.md\nglued prose with no blank line\n\nafter\n")
    assert count == 2                                      # "Intro." and "after"; the glued line is an under-count, named


def test_e14_fences_and_quotes_are_not_prose_the_skip_line_is_not_prose_and_n_and_n_plus_1_only_report():
    prompt = ("Intro.\n\n```\nfenced line one\nfenced line two\n```\n\n> quoted line\n\n"
              "manifest-skip: edges -- measured elsewhere\n\nTail.\n")
    assert hm.prose_lines(prompt)[0] == 2
    for n in (8, 9):                                       # the target N = 8 is a report, never a refusal
        assert hm.prose_lines("\n".join("line %d" % i for i in range(n)))[0] == n


def test_e14_a_degraded_cut_reads_everything_outside_the_manifest_as_prose_and_says_so(tmp_path, monkeypatch):
    monkeypatch.setattr(hm.dispatch_manifest, "_scan", lambda md, text: ([], True, "forced"))
    count, degraded, _h = hm.prose_lines("Intro.\n\n```\nfenced\n```\n\ngiven: C:\\fake\\a.md\n")
    assert degraded is True and count == 4                 # Intro, the fence lines and the fenced line: all prose now
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", prompt="Intro.\n\n```\nfenced\n```\n")
    rep = w.collect(node="forge/5/F5-9")
    h = _hop(rep, "t-001")
    assert h["cut"] == "degraded" and "cut=degraded" in hm.render(rep)


def test_e15_the_given_anchor_is_not_checked_not_applicable():
    count, _d, _h = hm.prose_lines("Intro.\n\ngiven: C:\\fake\\nowhere.py:99999\n")
    assert count == 1                                       # an anchor past the end of a file is not looked at


def test_the_prose_of_a_long_line_is_counted_by_the_25_line_rule(tmp_path):
    assert hm.prose_lines("x" * 450)[0] == 3               # ceil(450 / 200)


# --- E18-E24: the Lead side -------------------------------------------------------------------------------------

def _scout_world(tmp_path, with_intake=True, extra=(), prompt=PROMPT):
    """A scout t-001 (node forge/5/F5-9 by a notes token) with its launch, hand-back message, handback_extract call and
    reads of the extracted report; `extra` lines are appended to the main transcript."""
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", notes="forge/5 F5-9 verify")
    w.worker("aaa1", prompt=prompt, requests=[("r1", [{"input_tokens": 4, "output_tokens": 1}])])
    out = "C:\\fake\\reports\\t-001-r.md"
    lines = [_call("tu1", "Agent", {"prompt": "go; the report goes to " + out}), _launch("tu1", "aaa1")]
    if with_intake:
        lines.append(_intake("aaa1"))
    lines += [_call("tu2", "PowerShell", {"command": "python tools/handback_extract.py --agent aaa1 " + out}),
              _result("tu2", "written %s bytes=100 lines=3 source=handback finished=yes digest=none" % out),
              _call("tu3", "Read", {"file_path": out}), _result("tu3", "r" * 500),
              _call("tu4", "Grep", {"pattern": "foo", "path": "C:/fake/reports/T-001-R.md"}), _result("tu4", "g" * 40)]
    w.main(lines + list(extra))
    return w


def test_the_lead_side_of_a_scout_intake_read_and_the_written_path(tmp_path):
    w = _scout_world(tmp_path)
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["node"] == "forge/5/F5-9"                                    # the token of the notes, normalized
    assert h["lead_intake_chars"] == len(_loads_text(_intake("aaa1")))
    written = len("written C:\\fake\\reports\\t-001-r.md bytes=100 lines=3 source=handback finished=yes digest=none")
    assert h["lead_read_chars"] == 500 + 40 + written                      # Read + Grep + the extract call that names the file
    assert h["lead_write_chars"] == 0 and h["notes"] == [] and h["session"] == "sess-1"
    assert h["chars"] == h["brief_chars"] + h["lead_intake_chars"] + h["lead_read_chars"]


def _loads_text(line):
    return json.loads(line)["message"]["content"]


def test_e20_a_hop_without_an_intake_line_is_nd_with_the_session_named_and_its_units_still_count(tmp_path):
    w = _scout_world(tmp_path, with_intake=False)
    rep = w.collect(node="forge/5/F5-9")
    h = _hop(rep, "t-001")
    assert h["lead_intake_chars"] is None and h["units"] == 4 + 5.0
    assert h["nd"]["lead_intake_chars"] == {"code": "no_intake", "why": "no intake line in session sess-1"}
    assert "n/d hops: 1 (no_intake x1)" in hm.render(rep) and h["lead_read_chars"] > 0


def test_e21_an_intake_in_another_session_is_not_seen(tmp_path):
    w = _scout_world(tmp_path, with_intake=False)
    (w.proj / "sess-2.jsonl").write_text(_intake("aaa1") + "\n", encoding="utf-8")
    rep = w.collect(node="forge/5/F5-9")
    assert _hop(rep, "t-001")["lead_intake_chars"] is None
    assert "scanned: parent sessions only" in hm.render(rep) and rep["sessions"] == ["sess-1"]


def test_u10_an_intake_is_read_from_text_never_from_a_tool_result_block(tmp_path):
    """U10: a Read result that QUOTES an agent-message tag is not an intake; the line is credited to no agent."""
    quote = _dump({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "tu9", "content": '<agent-message from="aaa1">\nquoted report\n</agent-message>'}]}})
    quote_text_block = _dump({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "tu8", "content": [{"type": "text", "text": '<task-id>aaa1</task-id> quoted'}]}]}})
    w = _scout_world(tmp_path, with_intake=False, extra=[quote, quote_text_block])
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["lead_intake_chars"] is None
    idx = hm.session_index(w.proj / "sess-1.jsonl")
    assert idx["intake"] == {}


def test_the_intake_is_summed_over_a_message_and_a_task_notification_and_text_blocks_count(tmp_path):
    notification = _dump({"type": "user", "message": {"role": "user", "content": "<task-notification>\n<task-id>aaa1</task-id>\n</task-notification>"}})
    blocks = _dump({"type": "user", "message": {"role": "user", "content": [
        {"type": "text", "text": '<agent-message from="aaa1">\nmore\n</agent-message>'}, {"type": "image", "source": "x"}]}})
    w = _scout_world(tmp_path, extra=[notification, blocks])
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["lead_intake_chars"] == (len(_loads_text(_intake("aaa1"))) + len(_loads_text(notification))
                                      + len('<agent-message from="aaa1">\nmore\n</agent-message>'))
    other = _dump({"type": "queue-operation", "content": '<agent-message from="aaa1">x</agent-message>'})
    assert hm.session_index(_scout_world(tmp_path / "again", extra=[other]).proj / "sess-1.jsonl")["intake"]["aaa1"] == len(_loads_text(_intake("aaa1")))


# --- FX-1 (E32): the harness re-writes a record under the same uuid ----------------------------------------------

def _uuid(line, uid):
    obj = json.loads(line)
    obj["uuid"] = uid
    return _dump(obj)


def _fx1_world(tmp_path, main_lines):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", notes="forge/5 F5-9")
    w.worker("aaa1")
    w.main(main_lines)
    return w


def test_fx1_a_rewritten_intake_and_a_rewritten_read_do_not_double(tmp_path):
    intake, call, res = (_uuid(_intake("aaa1"), "u-in"), _uuid(_call("tu3", "Read", {"file_path": REPORT}), "u-rd"),
                         _uuid(_result("tu3", "r" * 500), "u-rs"))
    w = _fx1_world(tmp_path, [_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), intake, call, res,
                              intake, call, res, intake])                    # every record written 2-3 times
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["lead_intake_chars"] == len(_loads_text(_intake("aaa1")))      # once, not 3 x
    assert h["lead_read_chars"] == 500                                      # the Read once, not 2 x
    idx = hm.session_index(w.proj / "sess-1.jsonl")
    assert [c["id"] for c in idx["calls"]] == ["tu1", "tu3"]


def test_fx1_e24_a_rewritten_edit_after_the_next_launch_stays_with_the_hop_that_made_it(tmp_path):
    edit = _uuid(_call("t1", "Edit", {"file_path": REPORT, "new_string": "e" * 30}), "u-edit")
    launch1 = _uuid(_launch("tu1", "aaa1"), "u-l1")
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", agent="designer", notes="forge/5 F5-2", ts="2026-10-15T04:00:00")
    w.delegated("t-002", "bbb2", agent="designer", notes="fix round of the spec", ts="2026-10-15T05:00:00")
    w.worker("aaa1", kind="designer")
    w.worker("bbb2", kind="designer")
    w.main([_call("tu1", "Agent", {"prompt": "1"}), launch1, edit, _result("t1", "ok"),
            _call("tu2", "Agent", {"prompt": "2"}), _launch("tu2", "bbb2"),
            edit, launch1])                                                   # copies written AFTER the second launch
    rep = w.collect(node="forge/5/F5-2")
    assert _hop(rep, "t-001")["lead_write_chars"] == 30 and _hop(rep, "t-002")["lead_write_chars"] == 0


def test_fx1_a_tool_use_id_is_taken_once_even_under_another_uuid(tmp_path):
    first, again = (_uuid(_call("tu3", "Read", {"file_path": REPORT}), "u-1"),
                    _uuid(_call("tu3", "Read", {"file_path": REPORT}), "u-2"))
    w = _fx1_world(tmp_path, [_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), first, again,
                              _result("tu3", "r" * 40)])
    assert [c["id"] for c in hm.session_index(w.proj / "sess-1.jsonl")["calls"]] == ["tu1", "tu3"]
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["lead_read_chars"] == 40


def test_fx1_a_record_without_a_uuid_is_its_own_record_counted_by_its_line(tmp_path):
    w = _fx1_world(tmp_path, [_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), _intake("aaa1"), _intake("aaa1")])
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["lead_intake_chars"] == 2 * len(_loads_text(_intake("aaa1")))
    assert hm.session_index(w.proj / "sess-1.jsonl")["uuids"] == set()


def test_fx1_the_first_copy_wins_when_a_later_copy_differs(tmp_path):
    first, later = _uuid(_intake("aaa1", "short"), "u-x"), _uuid(_intake("aaa1", "a much longer later copy"), "u-x")
    w = _fx1_world(tmp_path, [_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), first, later])
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["lead_intake_chars"] == len(_loads_text(first))


# --- FX-2 (L-5 Q1, L-6): the attachment carrier of the intake ----------------------------------------------------

def _msg(aid, body):
    return '<agent-message from="%s">\n%s\n</agent-message>' % (aid, body)


def _attach(text, kind="peer", att_type="queued_command", uid=None, key="prompt"):
    att = {"type": att_type, key: text}
    if kind is not None:
        att["origin"] = {"kind": kind}
    rec = {"type": "attachment", "attachment": att}
    if uid:
        rec["uuid"] = uid
    return _dump(rec)


def _intake_of(tmp_path, extra, aid="aaa1"):
    w = _scout_world(tmp_path, with_intake=False, extra=extra)
    return _hop(w.collect(node="forge/5/F5-9"), "t-001"), hm.session_index(w.proj / "sess-1.jsonl")


def test_fx2_intake_from_a_user_line_only(tmp_path):
    text = _msg("aaa1", "from a user line")
    h, _idx = _intake_of(tmp_path, [_dump({"type": "user", "message": {"role": "user", "content": text}})])
    assert h["lead_intake_chars"] == len(text)


def test_fx2_intake_from_an_attachment_only_peer_and_task_notification(tmp_path):
    peer, note = _msg("aaa1", "from a peer attachment"), "<task-notification>\n<task-id>aaa1</task-id>\n</task-notification>"
    h, _idx = _intake_of(tmp_path, [_attach(peer, "peer")])
    assert h["lead_intake_chars"] == len(peer) and "lead_intake_chars" not in h["nd"]     # not no_intake
    h2, _idx = _intake_of(tmp_path / "n", [_attach(note, "task-notification")])
    assert h2["lead_intake_chars"] == len(note)


def test_fx2_one_message_in_both_carriers_counts_once_in_either_order(tmp_path):
    text = _msg("aaa1", "the same message")
    user = _dump({"type": "user", "message": {"role": "user", "content": text}})
    for n, order in enumerate(([user, _attach(text)], [_attach(text), user], [_attach(text), _attach(text, "task-notification")])):
        h, _idx = _intake_of(tmp_path / str(n), order)
        assert h["lead_intake_chars"] == len(text), order
    h, _idx = _intake_of(tmp_path / "w", [_attach(text, uid="u-a"), _attach(text, uid="u-a"), user])    # + a re-written attachment
    assert h["lead_intake_chars"] == len(text)


def test_fx2_an_instructions_attachment_carrying_the_tag_is_not_an_intake(tmp_path):
    quoted = "CLAUDE.md says: " + _msg("aaa1", "a tag quoted inside file contents")
    both = [_attach(quoted, kind=None, att_type="instructions", key="content"), _attach(quoted, kind="peer", att_type="instructions"),
            _attach(quoted, kind="peer", att_type="file")]
    h, idx = _intake_of(tmp_path, both)
    assert h["lead_intake_chars"] is None and h["nd"]["lead_intake_chars"]["code"] == "no_intake" and idx["intake"] == {}


def test_fx2_two_different_attachment_messages_of_one_agent_both_count_next_to_a_user_line(tmp_path):
    a, b, c = _msg("aaa1", "one"), _msg("aaa1", "two, longer"), _msg("aaa1", "three")
    user = _dump({"type": "user", "message": {"role": "user", "content": c}})
    h, _idx = _intake_of(tmp_path, [_attach(a), _attach(b, "task-notification"), user])
    assert h["lead_intake_chars"] == len(a) + len(b) + len(c)          # per MESSAGE, not per agent: the user line does not hide them


def test_fx2_the_same_text_in_two_attachments_of_one_agent_counts_once(tmp_path):
    text = _msg("aaa1", "repeated")
    h, _idx = _intake_of(tmp_path, [_attach(text, uid="u-1"), _attach(text, "task-notification", uid="u-2")])
    assert h["lead_intake_chars"] == len(text)


def test_fx2_a_human_origin_or_an_unknown_kind_or_a_tool_result_is_never_an_intake_and_a_missing_origin_has_a_code(tmp_path):
    text = _msg("aaa1", "quoted by a person")
    quote = _dump({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t9", "content": text}]}})
    h, idx = _intake_of(tmp_path, [_attach(text, "human"), _attach(text, ["peer"]), quote])      # kind: a str not in the set / a list
    assert idx["intake"] == {} and idx["no_origin"] == {"aaa1"}                                  # the list kind is "no str kind"
    assert h["nd"]["lead_intake_chars"]["code"] == "no_origin"
    h2, idx2 = _intake_of(tmp_path / "n", [_attach(text, None)])                                  # origin absent
    assert idx2["intake"] == {} and h2["nd"]["lead_intake_chars"]["code"] == "no_origin"
    h3, _i = _intake_of(tmp_path / "c", [_attach(text, None), _attach(_msg("aaa1", "real"), "peer")])   # a counted one beats the code
    assert h3["lead_intake_chars"] == len(_msg("aaa1", "real")) and "lead_intake_chars" not in h3["nd"]


def test_e22_read_times_zero_is_a_measured_zero_and_a_read_through_the_shell_counts(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", notes="forge/5 F5-9")
    w.worker("aaa1")
    w.main([_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), _intake("aaa1")])
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["lead_read_chars"] == 0 and h["lead_write_chars"] == 0 and h["lead_intake_chars"] > 0   # measured zeros, not n/d
    assert not [f for f in h["nd"] if f.startswith("lead_")] and h["notes"] == []                   # the dispatch names REPORT
    w.main([_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), _intake("aaa1"),
            _call("tu2", "PowerShell", {"command": "Get-Content " + REPORT}), _result("tu2", "s" * 77),
            _call("tu3", "Bash", {"command": "cat docs/tasks/handoffs/T-001-REPORT.md"}), _result("tu3", "b" * 11)])
    assert _hop(w.collect(node="forge/5/F5-9"), "t-001")["lead_read_chars"] == 88


def test_e23_a_hop_without_a_handoff_and_without_a_written_path_has_no_report_path(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", notes="forge/5 F5-9")
    w.worker("aaa1", prompt="Just a prose brief, no manifest at all.\n")
    w.main([_call("tu1", "Agent", {"prompt": "go"}), _launch("tu1", "aaa1"), _intake("aaa1"),
            _call("tu2", "Read", {"file_path": REPORT}), _result("tu2", "x" * 9)])
    rep = w.collect(node="forge/5/F5-9")
    h = _hop(rep, "t-001")
    assert h["lead_read_chars"] == 0 and h["lead_intake_chars"] > 0                          # measured 0, the intake still counts
    assert h["notes"][0] == "lead_read_chars: 0 (no report path)" and "lead_read_chars: 0 (no report path)" in hm.render(rep)


def test_e24_two_hops_on_one_report_path_the_call_goes_to_the_last_launched_before_it(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", agent="designer", notes="forge/5 F5-2", ts="2026-10-15T04:00:00")
    w.delegated("t-002", "bbb2", agent="designer", notes="fix round of the spec", ts="2026-10-15T05:00:00")
    w.worker("aaa1", kind="designer")
    w.worker("bbb2", kind="designer")
    w.main([_call("t0", "Edit", {"file_path": REPORT, "new_string": "before any launch"}), _result("t0", "ok"),
            _call("tu1", "Agent", {"prompt": "1"}), _launch("tu1", "aaa1"),
            _call("t1", "Edit", {"file_path": REPORT.upper().replace("C:", "c:"), "new_string": "e" * 30}), _result("t1", "ok"),
            _call("tu2", "Agent", {"prompt": "2"}), _launch("tu2", "bbb2"),
            _call("t2", "Edit", {"file_path": REPORT, "new_string": "e" * 7}), _result("t2", "ok"),
            _call("t3", "Write", {"file_path": REPORT, "content": "w" * 100}), _result("t3", "ok"),
            _call("t4", "Read", {"file_path": REPORT}), _result("t4", "r" * 9)])
    rep = w.collect(node="forge/5/F5-2")
    first, fix = _hop(rep, "t-001"), _hop(rep, "t-002")
    assert (first["lead_write_chars"], first["lead_read_chars"]) == (30, 0)       # the call before any launch is nobody's
    assert fix["shares_report_path_with"] == ["t-001"] and fix["unlinked_reason"] == "no_node"
    full = hm.collect(w.root, w.projects)
    assert (_hop(full, "t-002")["lead_write_chars"], _hop(full, "t-002")["lead_read_chars"]) == (107, 9)


def test_e19_no_main_transcript_the_lead_columns_are_nd_and_the_worker_side_counts(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", notes="forge/5 F5-9")
    w.worker("aaa1", requests=[("r1", [{"output_tokens": 2}])])
    rep = w.collect(node="forge/5/F5-9")
    h = _hop(rep, "t-001")
    assert h["units"] == 10.0 and h["brief_chars"] == len(PROMPT) and h["handback_chars"] == len("the report text")
    for f in ("lead_intake_chars", "lead_read_chars", "lead_write_chars"):
        assert h[f] is None and h["nd"][f]["code"] == "no_main"
    assert h["chars"] == len(PROMPT) and h["chars_partial"] is True                  # the known column is still summed, as a LOWER BOUND
    assert hm.hop_cells(h)[-1] == "%d+" % len(PROMPT) and ("| %d+ |" % len(PROMPT)) in hm.render(rep)   # FX-3: never a bare number


def test_e19_a_main_transcript_that_fails_mid_pass_is_nd_not_a_half_number(tmp_path, monkeypatch):
    w = _scout_world(tmp_path)
    real = hm.transcripts.iter_lines

    def broken(path):
        yield from list(real(path))[:3]
        raise OSError("disk went away")

    monkeypatch.setattr(hm.transcripts, "iter_lines", lambda p: broken(p) if str(p).endswith("sess-1.jsonl") else real(p))
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["lead_read_chars"] is None and h["nd"]["lead_read_chars"]["code"] == "unreadable" and h["units"] is not None


def test_e19_the_pass_is_one_streaming_pass_per_session_and_cached(tmp_path, monkeypatch):
    w = _scout_world(tmp_path)
    w.delegated("t-002", "bbb2", notes="forge/5 F5-9")
    w.worker("bbb2")
    w.flush()
    opened = []
    real = hm.transcripts.iter_lines
    monkeypatch.setattr(hm.transcripts, "iter_lines", lambda p: (opened.append(str(p)) or real(p)))
    hm.collect(w.root, w.projects, node="forge/5/F5-9")
    assert sum(1 for p in opened if p.endswith("sess-1.jsonl")) == 1


def test_a_line_cut_by_a_write_at_the_end_of_the_main_transcript_is_skipped(tmp_path):
    w = _scout_world(tmp_path)
    with open(w.proj / "sess-1.jsonl", "a", encoding="utf-8") as fh:
        fh.write('{"type": "user", "message": {"role": "user", "content": "<agent-message from=\\"aaa1\\"> half a li')
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["lead_intake_chars"] == len(_loads_text(_intake("aaa1")))


# --- E25-E29: the chain, the node, the CLI ----------------------------------------------------------------------

def test_e25_e26_e27_the_node_by_field_by_token_two_tokens_a_bad_field_and_a_non_string(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "a1", node="forge/5/F5-2", notes="x")
    w.delegated("t-002", "a2", notes="forge/5 F5-2 old line")
    w.delegated("t-003", "a3", node="conductor/2/C2-1", notes="forge/5 F5-2 disagrees")
    w.delegated("t-004", "a4", notes="forge/5 F5-2 and conductor/2 C2-1")
    w.delegated("t-005", "a5", node="F5-2")
    w.delegated("t-006", "a6", node=["forge/5/F5-2"])
    w.delegated("t-007", "a7", notes="no node anywhere")
    rep = w.collect()
    by = {h["task_id"]: h for h in [x for c in rep["chains"] for x in c["hops"]] + rep["unlinked"]["hops"]}
    assert by["t-001"]["node"] == by["t-002"]["node"] == "forge/5/F5-2" and by["t-003"]["node"] == "conductor/2/C2-1"
    assert {t: by[t]["unlinked_reason"] for t in ("t-004", "t-005", "t-006", "t-007")} == {
        "t-004": "two_tokens", "t-005": "node_not_form", "t-006": "node_not_string", "t-007": "no_node"}
    assert rep["warnings"] == ["t-003: node_token_differ", "t-005: node_not_form", "t-006: node_not_string"]
    assert rep["unlinked"]["count"] == 4 and "unlinked: 4 (" in hm.render(rep)


def test_e28_two_clones_with_one_task_id_are_two_tasks_and_a_replacement_is_its_own_hop(tmp_path):
    w = World(tmp_path)
    w.delegated("t-050", "a1", notes="forge/5 F5-2", ts="2026-10-15T04:00:00")
    w.delegated("t-050", "a2", notes="forge/5 F5-2 replaces_worker:agent:a1", ts="2026-10-15T04:30:00")
    w.flush()
    other = [dict(e, task_id="t-050", worker_ref="agent:a3", notes="forge/5 F5-2 other clone") for e in w.events[:1]]
    (w.root / "logs" / "journal").mkdir()
    (w.root / "logs" / "journal" / "bob.jsonl").write_text("".join(_dump(e) + "\n" for e in other), encoding="utf-8")
    rep = hm.collect(w.root, w.projects, node="forge/5/F5-2")
    hops = rep["chains"][0]["hops"]
    assert len(hops) == 3 and sorted(h["label"] for h in hops) == ["", "", "bob"]
    assert [h["replaced"] for h in hops if h["worker_ref"] == "agent:a2"] == [True] and "replaced" in hm.render(rep)
    assert sum(1 for h in hops if h["replaced"]) == 1


def test_a_window_keeps_the_hops_from_that_day_on(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "a1", notes="forge/5 F5-2", ts="2026-10-14T23:59:59")
    w.delegated("t-002", "a2", notes="forge/5 F5-2", ts="2026-10-15T00:00:00")
    w.delegated("t-003", "a3", notes="plain", ts="2026-10-16T09:00:00")
    rep = w.collect(window="2026-10-15")
    assert [h["task_id"] for h in rep["chains"][0]["hops"]] == ["t-002"] and rep["unlinked"]["count"] == 1


def _cli(w, *args):
    w.flush()
    return subprocess.run([sys.executable, str(TOOLS / "hop_metrics.py"), "--root", str(w.root), "--projects-root", str(w.projects),
                           *args], capture_output=True, text=True, encoding="utf-8")


@pytest.mark.parametrize("node", ["F5-2", "forge/5", "forge/5/F5-2\n", "Forge/5/F5-2", "", "forge/5/F5-2/x",
                                  "forge/5/F5-", "forge/5/F5-2-"])           # F6-15: an id that ends in a dash is no node
def test_e29_a_node_that_is_not_slug_n_id_is_exit_1_and_names_the_form(tmp_path, node):
    w = World(tmp_path)
    w.delegated("t-001", "a1", notes="forge/5 F5-2")
    proc = _cli(w, "--node", node)
    assert proc.returncode == 1 and "<slug>/<N>/<id>" in proc.stderr and proc.stdout == ""


def test_e29_a_missing_projects_root_a_bad_date_and_a_missing_root_are_exit_1(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "a1", notes="forge/5 F5-2")
    w.flush()
    base = [sys.executable, str(TOOLS / "hop_metrics.py")]
    gone = subprocess.run(base + ["--root", str(w.root), "--projects-root", str(tmp_path / "gone")], capture_output=True, text=True)
    assert gone.returncode == 1 and "no folder" in gone.stderr
    noroot = subprocess.run(base + ["--root", str(tmp_path / "gone"), "--projects-root", str(w.projects)], capture_output=True, text=True)
    assert noroot.returncode == 1
    for bad in ("2026-13-45", "15.10.2026", "2026-1-5", ""):
        proc = _cli(w, "--window", bad)
        assert proc.returncode == 1 and "YYYY-MM-DD" in proc.stderr, bad
    assert _cli(w, "--bogus").returncode == 1                       # argparse would say 2: here 2 means "journal unreadable"
    assert _cli(w, "--help").returncode == 0


def test_e29_a_node_without_hops_is_a_line_and_exit_0_and_an_unreadable_journal_is_exit_2(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "a1", notes="forge/5 F5-2")
    proc = _cli(w, "--node", "forge/9/F9-9")
    assert proc.returncode == 0 and "no hops for forge/9/F9-9" in proc.stdout and "scanned: parent sessions only" in proc.stdout
    missing = World(tmp_path / "missing")                           # logs/ exists, NO journal file (no flush)
    proc = subprocess.run([sys.executable, str(TOOLS / "hop_metrics.py"), "--root", str(missing.root),
                           "--projects-root", str(missing.projects)], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 2 and "cannot be read" in proc.stderr and "no journal file" in proc.stderr


def _main_over(w, capsys, *args):
    """(exit code, stdout, stderr) of hop_metrics.main over the world's folders, in-process."""
    code = hm.main(["--root", str(w.root), "--projects-root", str(w.projects), *args])
    out = capsys.readouterr()
    return code, out.out, out.err


def test_f6_15_an_empty_journal_file_reads_as_empty_and_exit_0_not_as_unreadable(tmp_path):
    empty = World(tmp_path / "empty")
    proc = _cli(empty)                                              # flush writes a journal file with 0 bytes
    assert (empty.root / "logs" / "routing-log.jsonl").stat().st_size == 0
    assert proc.returncode == 0 and "journal: empty (0 events)" in proc.stdout and proc.stderr == ""
    data = json.loads(_cli(empty, "--json").stdout)
    assert data["journal_empty"] is True and data["journal_rows"] == 0 and data["chains"] == []
    full = World(tmp_path / "full")                                 # control: a journal with one event is not "empty"
    full.delegated("t-001", "a1", notes="forge/5 F5-2")
    again = _cli(full)
    assert again.returncode == 0 and "journal: empty" not in again.stdout
    assert json.loads(_cli(full, "--json").stdout)["journal_empty"] is False


def test_f6_15_an_empty_slug_file_alone_is_empty_too(tmp_path, capsys):
    w = World(tmp_path)
    (w.root / "logs" / "journal").mkdir()
    (w.root / "logs" / "journal" / "bob.jsonl").write_text("", encoding="utf-8")
    code, out, err = _main_over(w, capsys)
    assert code == 0 and "journal: empty (0 events)" in out and err == ""


def test_f6_15_a_directory_in_place_of_the_journal_stays_cannot_be_read(tmp_path, capsys):
    w = World(tmp_path)
    (w.root / "logs" / "routing-log.jsonl").mkdir()
    code, out, err = _main_over(w, capsys)
    assert code == 2 and out == "" and "cannot be read" in err


def test_f6_15_an_unreadable_journal_file_stays_cannot_be_read_even_next_to_an_empty_one(tmp_path, capsys, monkeypatch):
    w = World(tmp_path)
    w.flush()                                                       # an EMPTY history, read fine
    (w.root / "logs" / "journal").mkdir()
    (w.root / "logs" / "journal" / "bob.jsonl").write_text("{}\n", encoding="utf-8")
    real = hm.journal_keys._read_text

    def unreadable(root, rel, problems):
        if rel.endswith("bob.jsonl"):
            problems.append("%s cannot be read (PermissionError: denied)" % rel)
            return None
        return real(root, rel, problems)

    assert _main_over(w, capsys)[0] == 0                            # control: with both readable the journal reads
    monkeypatch.setattr(hm.journal_keys, "_read_text", unreadable)
    code, out, err = _main_over(w, capsys)
    assert code == 2 and out == "" and "cannot be read" in err and "PermissionError" in err


def test_the_json_is_the_data_of_the_table_sorted_and_no_money(tmp_path):
    w = _scout_world(tmp_path)
    w.delegated("t-002", "bbb2", agent="critic", notes="forge/5 F5-9 review")
    w.delegated("t-003", "ccc3", agent="critic", notes="unlinked review")
    w.worker("bbb2", kind="critic", prompt=PROMPT.replace("t-001-report", "t-002-report"))
    w.worker("ccc3", kind="critic", prompt=PROMPT.replace("t-001-report", "t-003-report"))
    w.flush()
    table = _cli(w, "--node", "forge/5/F5-9")
    as_json = _cli(w, "--node", "forge/5/F5-9", "--json")
    assert table.returncode == as_json.returncode == 0
    data = json.loads(as_json.stdout)
    assert as_json.stdout == json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    first_table = table.stdout.split("\n\n")[0]
    rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in first_table.splitlines()
            if line.startswith("| ") and not line.startswith("| task")]
    hops = data["chains"][0]["hops"]
    assert [r[0] for r in rows] == [h["task_id"] for h in hops] == ["t-001", "t-002"]
    assert rows == [hm.hop_cells(h) for h in hops]                    # the same cells, from the same data
    assert "total: chars=%d units=%s" % (data["chains"][0]["totals"]["chars"], hm._cell(data["chains"][0]["totals"]["units"])) in table.stdout
    assert not re.search(r"\$|usd|price|cost", table.stdout + as_json.stdout, re.I)


def test_the_two_sums_chars_and_units_are_never_one_number(tmp_path):
    w = _scout_world(tmp_path)
    rep = w.collect(node="forge/5/F5-9")
    totals = rep["chains"][0]["totals"]
    assert set(totals) == {"hops", "nd_hops", "chars", "units", "chars_by_column"}
    assert totals["chars"] == sum(totals["chars_by_column"].values()) and totals["units"] == 9.0
    assert "handback_chars" not in totals["chars_by_column"]


def test_main_prints_nothing_to_stderr_and_writes_no_file(tmp_path, capsys):
    w = _scout_world(tmp_path)
    w.flush()
    before = sorted(p.name for p in tmp_path.rglob("*"))
    assert hm.main(["--root", str(w.root), "--projects-root", str(w.projects), "--node", "forge/5/F5-9"]) == 0
    out = capsys.readouterr()
    assert "chain forge/5/F5-9 (1 hops)" in out.out and out.err == ""
    assert sorted(p.name for p in tmp_path.rglob("*")) == before


def test_fx3_chars_is_partial_only_when_a_column_is_nd_and_nd_when_every_column_is(tmp_path):
    w = _scout_world(tmp_path)
    full = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert full["chars_partial"] is False and "+" not in hm.hop_cells(full)[-1]            # all four columns known
    w2 = _scout_world(tmp_path / "p", with_intake=False)                                    # intake n/d, the rest known
    part = _hop(w2.collect(node="forge/5/F5-9"), "t-001")
    known = part["brief_chars"] + part["lead_read_chars"] + part["lead_write_chars"]
    assert part["chars"] == known and part["chars_partial"] is True and hm.hop_cells(part)[-1] == "%d+" % known
    w3 = World(tmp_path / "g")                                                              # no transcript: every column n/d
    w3.delegated("t-009", "ghost", node="forge/5/F5-9")
    w3.flush()
    ghost = _hop(hm.collect(w3.root, w3.projects, node="forge/5/F5-9"), "t-009")
    assert ghost["chars"] is None and ghost["chars_partial"] is False and hm.hop_cells(ghost)[-1] == "n/d"
    data = json.loads(json.dumps(w2.collect(node="forge/5/F5-9")))
    assert data["chains"][0]["hops"][0]["chars_partial"] is True


def test_fx4_a_broken_digest_form_is_form_error_and_a_failed_prose_count_is_prose_error(tmp_path, monkeypatch):
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", handback="a report")

    def boom(*_a, **_k):
        raise RuntimeError("boom")

    monkeypatch.setattr(hm.digest_form, "parse", boom)
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["nd"]["form"]["code"] == "form_error" and h["handback_chars"] == len("a report") and "handback_chars" not in h["nd"]
    monkeypatch.undo()
    monkeypatch.setattr(hm, "prose_lines", boom)
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["nd"]["brief"]["code"] == "prose_error" and h["brief_chars"] == len(PROMPT) and h["brief_prose_lines"] is None
    for code in ("form_error", "prose_error", "no_origin"):
        assert code in hm.__doc__


def test_fx5_the_text_of_a_message_has_one_reader_in_transcripts():
    source = (TOOLS / "hop_metrics.py").read_text(encoding="utf-8")
    assert "_text_blocks" not in source and source.count("transcripts.content_text(") >= 3
    assert not re.search(r'b\.get\("type"\) == "text"', source)                        # the join expression is not repeated here


def test_the_module_functions_stay_within_sixty_lines():
    import ast
    tree = ast.parse((TOOLS / "hop_metrics.py").read_text(encoding="utf-8"))
    long = [(n.name, n.end_lineno - n.lineno + 1) for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
            and n.end_lineno - n.lineno + 1 > 60]
    assert long == []
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"load_chains", "hops_of", "worker_side", "session_index", "lead_side", "render"} <= names


def test_hop_metrics_imports_no_gate_and_no_second_jsonl_reader():
    source = (TOOLS / "hop_metrics.py").read_text(encoding="utf-8")
    assert "json.loads" not in source and "open(" not in source           # the transcripts are read through transcripts.py only
    assert "import piles" not in source and "import forge_metrics" not in source


# --- F6-15: the leftovers of the critic's FX-6 (t-812) ----------------------------------------------------------

_BLOCKS = (ast.For, ast.While, ast.If, ast.Try, ast.With)


def _nesting(node, depth=0):
    """The deepest nesting of control blocks (for / while / if / try / with) under `node`; an `elif` is not deeper
    than its `if`."""
    deepest = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _BLOCKS):
            is_elif = isinstance(node, ast.If) and isinstance(child, ast.If) and node.orelse == [child]
            deepest = max(deepest, _nesting(child, depth if is_elif else depth + 1))
        else:
            deepest = max(deepest, _nesting(child, depth))
    return deepest


def test_f6_15_no_function_of_the_module_nests_control_blocks_deeper_than_three():
    tree = ast.parse((TOOLS / "hop_metrics.py").read_text(encoding="utf-8"))
    deep = {n.name: _nesting(n) for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and _nesting(n) > 3}
    assert deep == {}
    # the detector sees a deep function (negative control: for / for / for / if is 4)
    sample = ast.parse("def f(a):\n for x in a:\n  for y in x:\n   for z in y:\n    if z:\n     pass\n")
    assert _nesting(sample.body[0]) == 4


def test_f6_15_a_node_field_with_a_trailing_dash_is_a_bad_field_never_a_chain(tmp_path):
    w = World(tmp_path)
    w.delegated("t-001", "a1", node="forge/5/F5-")
    w.delegated("t-002", "a2", node="forge/5/F5-2")                     # control: the same field without the dash links
    rep = w.collect()
    assert [c["node"] for c in rep["chains"]] == ["forge/5/F5-2"]
    assert _hop(rep, "t-001")["unlinked_reason"] == "node_not_form" and rep["warnings"] == ["t-001: node_not_form"]


def test_f6_15_count_by_is_a_counter_and_the_json_keeps_its_shape(tmp_path):
    from collections import Counter
    assert not hasattr(hm, "_count_by")
    w = World(tmp_path)
    w.delegated("t-001", "ghost", node="forge/5/F5-9")                  # no transcript: n/d no_transcript
    w.delegated("t-002", "ghost2", notes="plain")                       # unlinked: no_node
    w.delegated("t-003", "ghost3", notes="plain again")
    rep = w.collect()
    assert isinstance(rep["nd"]["reasons"], Counter) and isinstance(rep["unlinked"]["reasons"], Counter)
    assert rep["nd"]["reasons"] == {"no_transcript": 3} and rep["unlinked"]["reasons"] == {"no_node": 2}
    data = json.loads(_cli(w, "--json").stdout)
    assert data["nd"]["reasons"] == {"no_transcript": 3} and data["unlinked"]["reasons"] == {"no_node": 2}
    assert "n/d hops: 3 (no_transcript x3)" in hm.render(rep) and "unlinked: 2 (no_node x2)" in hm.render(rep)


def test_f6_15_a_warning_names_the_task_with_its_label_and_the_raw_key_of_an_undeclared_one(tmp_path):
    w = World(tmp_path)
    w.delegated("t-003", "a3", node="conductor/2/C2-1", notes="forge/5 F5-2 disagrees")      # the history: no label
    w.flush()
    other = [dict(w.events[0], task_id="t-050", node="F5-2", worker_ref="agent:a4")]          # a clone's file `bob`
    (w.root / "logs" / "journal").mkdir()
    (w.root / "logs" / "journal" / "bob.jsonl").write_text("".join(_dump(e) + "\n" for e in other), encoding="utf-8")
    rep = hm.collect(w.root, w.projects)
    assert sorted(rep["warnings"]) == ["t-003: node_token_differ", "t-050@bob: node_not_form"]    # no segment declares `bob`
    bob = _hop(rep, "t-050")
    assert hm.hop_cells(bob)[0] == "t-050@bob" and hm.hop_cells(_hop(rep, "t-003"))[0] == "t-003"


def test_f6_15_a_flat_section_scan_gives_the_manifest_lines_of_the_cut():
    import dispatch_manifest
    cut = dispatch_manifest.section_cut(PROMPT)
    lines = hm._manifest_lines(cut)
    assert 0 not in lines and {i for i, ln in enumerate(cut.lines) if ln.startswith(("given:", "owns:", "handoff:"))} <= lines
    assert hm.prose_lines(PROMPT)[0] == 1                                # only "Task t-001 intro line." is prose


@pytest.mark.parametrize("notes", [
    "forge/5 F5-2 replaces_worker:agent:a1", "replaces_worker:agent:a1.", "x replaces_worker:cli:2026-10-15 y",
    "replaces_worker:", "replaces_worker: agent:a1", "no marker", "xreplaces_worker:agent:a1", "",
    "replaces_worker:agent:a1 replaces_worker:agent:a2"])
def test_f6_15_the_replacement_marker_is_read_by_the_gates_own_reader(tmp_path, notes):
    import journal_validator
    w = World(tmp_path)
    ev = w.delegated("t-050", "a2", notes=notes)
    hop = hm._blank_hop({"key": ("", "t-050"), "node": None, "reason": None}, ev)
    expected = journal_validator.extract_replaces_worker(notes)
    assert (hop["replaced"], hop["replaces"]) == (expected is not None, expected)
    assert not hasattr(hm, "REPLACES_RE")
    assert hm._blank_hop({"key": ("", "t-051"), "node": None, "reason": None}, dict(ev, notes=None))["replaced"] is False


def test_f6_15_probe_a_record_rewritten_under_one_uuid_in_a_worker_transcript(tmp_path):
    """The probe of FX-6: the harness re-writes a record under the same uuid (E32). hop_metrics joins the worker's
    lines per request (transcripts.request_usages: MAX per field), so one request rewritten three times is ONE
    request with the units of one; tier_echo's `=N` counts assistant LINES (transcripts.iter_models), so it counts
    the rewrite -- measured, not fixed (tier_echo is F6-20's). The assertion on tier_echo is one-sided on purpose:
    its count never goes UNDER the request count."""
    import tier_echo
    w = World(tmp_path)
    w.delegated("t-001", "aaa1", node="forge/5/F5-9")
    w.worker("aaa1", requests=[("r1", [{"input_tokens": 4, "output_tokens": 1}])])
    path = w.proj / "sess-1" / "subagents" / "agent-aaa1.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    record = next(ln for ln in lines if '"requestId": "r1"' in ln)
    path.write_text("\n".join(lines[:2] + [record, record] + lines[2:]) + "\n", encoding="utf-8")
    assert sum(1 for ln in path.read_text(encoding="utf-8").splitlines() if ln == record) == 3
    h = _hop(w.collect(node="forge/5/F5-9"), "t-001")
    assert h["requests"] == 1 and h["units"] == 9.0                      # one request, the units of ONE (4 + 1*5)
    counts = tier_echo.count_models(tier_echo.iter_transcript_models(str(path)))
    assert counts["m"] >= h["requests"]                                  # measured 3 on 16.10: the lines, not the requests
