"""Tests of tools/journal_hooks.py (offload spec r2 §3.B23, F-T1): the payload table (E-B23-1..6/12), the order rows
(E-B23-7/8), the linked-worktree rows (E-B23-10), the pre-edit rows in both modes (E-B23-13), the stores and their prune.
Every row runs over a temp git repo with a seeded journal (never the real logs/journal). Row ids carry the E-B23-n."""
import io
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import dispatch_manifest as dm  # noqa: E402
import journal_hooks as jh  # noqa: E402
import journal_lock as jl  # noqa: E402
import journal_write as jw  # noqa: E402

SEED = ('{"ts":"2026-11-05T14:29:30","event":"journal_created","agent":"lead","category":"journal","feature":"F19",'
        '"notes":"seed"}\n')
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
DOOR = "python -B tools/journal_write.py delegated"


def git(repo, *args):
    return subprocess.run([*GIT, "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


@pytest.fixture(scope="module")
def template(tmp_path_factory):
    repo = tmp_path_factory.mktemp("tpl") / "r"
    (repo / "tools").mkdir(parents=True)
    (repo / "logs/journal").mkdir(parents=True)
    git(repo, "init", "-q")
    git(repo, "config", "core.autocrlf", "false")
    (repo / "tools/dev.config.yaml").write_text("developer: dev1\n")
    (repo / "logs/journal/dev1.jsonl").write_text(SEED)
    (repo / "plans").mkdir()
    (repo / "plans/features.json").write_text('{"features": [{"id": "F19"}]}\n')   # FG7-70: never the live registry
    shutil.copy(TOOLS.parent / "logs/journal-letters.json", repo / "logs/journal-letters.json")
    assert jw.claim_letter(repo).code == 0
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "seed")
    return repo


@pytest.fixture
def repo(template, tmp_path):
    dst = tmp_path / "r"
    shutil.copytree(template, dst)
    return dst


def journal(root):
    return [json.loads(x) for x in (Path(root) / "logs/journal/dev1.jsonl").read_text(encoding="utf-8").splitlines()]


def events(root, kind=None):
    return [o for o in journal(root) if kind is None or o["event"] == kind]


def payload(cwd, agent_id="a1b2c3", desc="sonnet: scout the thing", prompt="Recon only.", agent="scout", **extra):
    obj = {"tool_name": "Agent", "cwd": str(cwd), "session_id": "sess1234-abcd",
           "tool_input": {"subagent_type": agent, "description": desc, "prompt": prompt},
           "tool_response": {"isAsync": True, "status": "async_launched", "agentId": agent_id, "resolvedModel": "claude-sonnet-5-5"}}
    obj.update(extra)
    return obj


def stop(cwd, agent_id="a1b2c3"):
    return {"session_id": "sess1234-abcd", "cwd": str(cwd), "hook_event_name": "SubagentStop", "agent_id": agent_id}


def launch_text(agent_id):
    return {"type": "text", "text": f"Async agent launched successfully.\nagentId: {agent_id} (internal ID)\nThe agent is working."}


def say(lines):
    return " | ".join(lines)


def run_main(mode, raw: bytes, monkeypatch, capsys):
    class _In:
        buffer = io.BytesIO(raw)
    monkeypatch.setattr(sys, "stdin", _In())
    code = jh.main([mode])
    return code, capsys.readouterr().out


# ------------------------------------------------------------------ E-B23-1 / E-B23-2: the payload table

NOT_RECORDED = {
    "no_tool_response": lambda c: {k: v for k, v in payload(c).items() if k != "tool_response"},
    "string_without_id": lambda c: payload(c, tool_response="launched, no id here"),
    "blocks_without_id": lambda c: payload(c, tool_response=[{"type": "text", "text": "nothing"}, {"type": "image"}]),
    "nested_dicts": lambda c: payload(c, tool_response={"result": {"inner": {"agentId": "deep"}}}),
    "unsafe_id_field": lambda c: payload(c, tool_response={"agentId": "../../etc"}),
    "two_mb_response": lambda c: payload(c, tool_response="x" * (2 * 1024 * 1024)),
    "list_payload": lambda c: [payload(c)],
    "no_tool_input": lambda c: {k: v for k, v in payload(c).items() if k != "tool_input"},
    "no_subagent_type": lambda c: payload(c, agent=None),
    "description_without_tier_word": lambda c: payload(c, desc="fix flaky test"),                      # E-B23-3
    "description_missing": lambda c: payload(c, desc=None),
}


@pytest.mark.parametrize("name", sorted(NOT_RECORDED))
def test_e_b23_1_3_an_unrecordable_launch_writes_nothing_and_says_so_with_the_door(repo, name):
    before = (repo / "logs/journal/dev1.jsonl").read_bytes()
    out = jh.post_agent(NOT_RECORDED[name](repo))
    assert len(out) == 1 and out[0].startswith("JOURNAL: delegated NOT written -- ") and DOOR in out[0], out
    assert (repo / "logs/journal/dev1.jsonl").read_bytes() == before


@pytest.mark.parametrize("raw", [b"", b"not json", b"\xff\xfe\x00bad", b"[1,2]", b"null", b'{"tool_input": 5}'],
                         ids=["empty", "text", "non_utf8", "list", "null", "tool_input_not_dict"])
def test_e_b23_1_raw_stdin_forms_exit_zero_and_give_the_door(repo, monkeypatch, capsys, raw):
    code, out = run_main("post-agent", raw, monkeypatch, capsys)
    assert code == 0
    assert DOOR in json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert len(events(repo)) == 1


@pytest.mark.parametrize("response,expected", [
    ({"agentId": "dictid"}, "dictid"),
    ("agentId: texid1 (internal)", "texid1"),
    ([launch_text("blockid")], "blockid"),
    ({"content": [launch_text("inner1")]}, "inner1"),
    ({"agentId": "fieldwins", "content": [launch_text("textloses")]}, "fieldwins"),            # E-B23-2: the field wins
    ("agentId: first1 and later agentId: second2", "first1"),                                    # E-B23-2: else the first
], ids=["dict", "text", "blocks", "dict_content", "field_over_text", "first_of_two"])
def test_e_b23_2_the_agent_id_comes_from_the_one_reader(repo, response, expected):
    out = jh.post_agent(payload(repo, tool_response=response))
    assert out[0].startswith("JOURNAL: delegated t-"), out
    assert events(repo, "delegated")[-1]["worker_ref"] == f"agent:{expected}"


def test_a_recorded_launch_has_the_fields_the_validator_and_check_46_read(repo):
    out = jh.post_agent(payload(repo, prompt="task: t-901\nfeature: F19\nnode: forge/5/F5-2\nbody"))
    assert "t-901" not in out[0] or "NOT written" in out[0]       # t-901 was never issued: the writer refuses (E-B23-5)
    task = jw.reserve_ids(repo, 1).ids[0]
    out = jh.post_agent(payload(repo, prompt=f"task: {task}\nfeature: F19\nnode: forge/5/F5-2\nbody"))
    row = events(repo, "delegated")[-1]
    assert out[0].startswith(f"JOURNAL: delegated {task} written")
    assert (row["agent"], row["model"], row["task_id"], row["worker_ref"], row["feature"], row["node"]) == (
        "scout", "sonnet", task, "agent:a1b2c3", "F19", "forge/5/F5-2")
    assert row["via"] == "hook" and row["session"] == "sess1234" and row["category"] == "recon"
    assert (Path(jl.lock_dir(repo)) / "open/a1b2c3").read_text(encoding="utf-8") == str(repo / "logs/journal/dev1.jsonl")


def test_e_b23_3_a_tier_word_description_family_is_what_is_written(repo):
    jh.post_agent(payload(repo, desc="opus-x: review the diff", agent="critic"))
    assert events(repo, "delegated")[-1]["model"] == "opus"


def test_e_b23_4_no_task_id_gets_one_from_the_counter_and_the_line_says_so(repo):
    out = jh.post_agent(payload(repo))
    task = events(repo, "delegated")[-1]["task_id"]
    assert f"task id issued by the hook: {task} (the dispatch named none)" in out[0]


def test_e_b23_5_a_validator_refusal_writes_nothing_and_shows_its_text_with_the_door(repo):
    task = jw.reserve_ids(repo, 1).ids[0]
    assert jh.post_agent(payload(repo, prompt=f"task: {task}\nx"))[0].startswith("JOURNAL: delegated")
    res = jw.write_event(repo, {"event": "accepted", "agent": "scout", "model": "sonnet", "task_id": task, "by": "fable",
                                "category": "recon", "feature": "F19", "notes": "closed"})
    assert res.written, res.messages
    before = (repo / "logs/journal/dev1.jsonl").read_bytes()
    out = jh.post_agent(payload(repo, agent_id="other9", prompt=f"task: {task}\nx"))
    assert len(out) == 1 and "NOT written" in out[0] and "CLOSED" in out[0] and DOOR in out[0]
    assert (repo / "logs/journal/dev1.jsonl").read_bytes() == before


def test_e_b23_6_a_busy_lock_writes_nothing_waits_only_the_timeout_and_shows_the_door(repo, monkeypatch):
    monkeypatch.setattr(jh, "HOOK_LOCK_TIMEOUT", 0.3)
    before = (repo / "logs/journal/dev1.jsonl").read_bytes()
    with jl.machine_lock("journal", 1, repo=repo):
        start = time.monotonic()
        out = jh.post_agent(payload(repo))
    assert time.monotonic() - start < 4
    assert "NOT written" in out[0] and "journal busy" in out[0] and DOOR in out[0]
    assert (repo / "logs/journal/dev1.jsonl").read_bytes() == before


def test_the_retry_of_a_rejected_task_carries_attempt_rejected_plus_one(repo):
    task = jw.reserve_ids(repo, 1).ids[0]
    jh.post_agent(payload(repo, agent_id="r1", agent="builder", desc="sonnet: build", prompt=f"task: {task}\nx"))
    res = jw.write_event(repo, {"event": "rejected", "agent": "builder", "model": "sonnet", "task_id": task, "by": "fable",
                                "attempt": 1, "failure_class": "spec", "category": "implementation", "notes": "no witness"})
    assert res.written, res.messages
    out = jh.post_agent(payload(repo, agent_id="r2", agent="builder", desc="sonnet: build again", prompt=f"task: {task}\nx"))
    assert out[0].startswith("JOURNAL: delegated"), out
    assert events(repo, "delegated")[-1]["attempt"] == 2


def test_a_critic_entry_on_an_open_task_needs_no_attempt(repo):
    task = jw.reserve_ids(repo, 1).ids[0]
    jh.post_agent(payload(repo, agent_id="b1", agent="builder", desc="sonnet: build", prompt=f"task: {task}\nx"))
    out = jh.post_agent(payload(repo, agent_id="c1", agent="critic", desc="opus: review", prompt=f"task: {task}\nx"))
    assert out[0].startswith("JOURNAL: delegated"), out
    assert "attempt" not in events(repo, "delegated")[-1]


@pytest.mark.parametrize("desc_len,token", [(40, ""), (299, ""), (300, ""), (301, ""), (1000, ""), (1000, "agent:rep1")],
                         ids=["short", "299", "300", "301", "1000", "1000_with_token"])
def test_hook_notes_are_at_most_300_chars_cut_with_an_ellipsis_and_keep_the_replaces_token(repo, desc_len, token):
    task = jw.reserve_ids(repo, 1).ids[0]
    if token:
        jh.post_agent(payload(repo, agent_id="rep1", agent="builder", desc="sonnet: first", prompt=f"task: {task}\nx"))
    desc = "sonnet: " + "d" * (desc_len - len("sonnet: "))
    prompt = f"task: {task}\nreplaces_worker:{token}\nx" if token else f"task: {task}\nx"
    out = jh.post_agent(payload(repo, agent_id="n1", agent="builder", desc=desc, prompt=prompt))
    assert out[0].startswith("JOURNAL: delegated"), out
    notes = events(repo, "delegated")[-1]["notes"]
    assert len(notes) <= 300
    assert (notes.endswith("…") or len(desc) <= 300 or token) and (not token or notes.endswith(f"replaces_worker:{token}"))
    if desc_len > 300 and not token:
        assert notes.endswith("…") and len(notes) == 300


def test_a_designer_skip_header_also_writes_dispatch_skipped_once_per_task(repo):
    task = jw.reserve_ids(repo, 1).ids[0]
    owns = "\n".join(f"owns: {repo}/f{i}.py" for i in range(3)).replace("\\", "/")
    prompt = f"task: {task}\n{owns}\ndesigner: skip -- no design content\n"
    assert dm.designer_skip_reason(dm.cut_payload({"tool_input": {"subagent_type": "builder", "prompt": prompt}})[1]) == "no design content"
    jh.post_agent(payload(repo, agent_id="s1", agent="builder", desc="sonnet: build", prompt=prompt))
    jh.post_agent(payload(repo, agent_id="s2", agent="builder", desc="sonnet: build", prompt=prompt, ))
    skips = events(repo, "dispatch_skipped")
    assert len(skips) == 1 and skips[0]["agent"] == "designer" and skips[0]["notes"] == f"designer skip for {task}: no design content"


# ------------------------------------------------------------------ E-B23-7/8/12: order, idempotence

def test_e_b23_12_a_second_post_tool_use_for_the_same_agent_writes_nothing_and_never_returned(repo):
    jh.post_agent(payload(repo))
    n = len(journal(repo))
    assert jh.post_agent(payload(repo, tool_response={"agentId": "a1b2c3", "status": "completed"})) == []
    assert len(journal(repo)) == n and not events(repo, "returned")


def test_e_b23_8_foreground_stop_first_leaves_a_marker_and_post_writes_delegated_then_returned(repo):
    assert jh.record_returned(stop(repo)) == []
    marker = jl.lock_dir(repo) / "pending-returns/a1b2c3"
    assert marker.is_file() and not events(repo, "returned")
    out = jh.post_agent(payload(repo))
    kinds = [o["event"] for o in journal(repo)]
    assert kinds[-2:] == ["delegated", "returned"] and kinds.count("returned") == 1
    assert not marker.exists() and any(x.startswith("JOURNAL: returned t-") for x in out)
    assert events(repo, "returned")[-1]["worker_ref"] == "agent:a1b2c3" and events(repo, "returned")[-1]["model"] == "sonnet"


def test_e_b23_7_background_stop_after_post_writes_returned_once_and_the_index_is_spent(repo):
    jh.post_agent(payload(repo))
    jh.record_returned(stop(repo))
    jh.record_returned(stop(repo))                                    # a second stop: idempotent, nothing more
    assert len(events(repo, "returned")) == 1
    assert not (jl.lock_dir(repo) / "open/a1b2c3").exists() and not (jl.lock_dir(repo) / "pending-returns/a1b2c3").exists()


@pytest.mark.parametrize("bad", [None, {}, {"agent_id": ""}, {"agent_id": "../x", "cwd": "."}, "str", [1]],
                         ids=["none", "empty", "empty_id", "unsafe_id", "string", "list"])
def test_record_returned_ignores_a_payload_it_cannot_use(bad):
    assert jh.record_returned(bad) == []


def test_record_returned_in_a_repo_without_a_journal_creates_no_marker(tmp_path):
    (tmp_path / "r").mkdir()
    git(tmp_path / "r", "init", "-q")
    assert jh.record_returned(stop(tmp_path / "r")) == []
    assert not (tmp_path / "r/.git/forge-journal/pending-returns/a1b2c3").exists()


def test_the_unknown_mode_and_a_pre_tool_use_style_call_write_nothing(repo, monkeypatch, capsys):
    before = (repo / "logs/journal/dev1.jsonl").read_bytes()
    code, out = run_main("pre-agent", json.dumps(payload(repo)).encode(), monkeypatch, capsys)
    assert code == 0 and out == "" and (repo / "logs/journal/dev1.jsonl").read_bytes() == before      # E-B23-9: only post-agent writes


# ------------------------------------------------------------------ E-B23-10: a linked worktree

@pytest.fixture
def two_trees(repo, tmp_path):
    wt = tmp_path / "wt2"
    git(repo, "worktree", "add", "-q", str(wt))
    return repo, wt


def test_e_b23_10_returned_goes_into_the_worktree_copy_through_the_index(two_trees):
    root, wt = two_trees
    jh.post_agent(payload(wt))
    assert events(wt, "delegated") and not events(root, "delegated")
    jh.record_returned(stop(root))                                    # the stop reports from the OTHER tree
    assert len(events(wt, "returned")) == 1 and not events(root, "returned")


def test_e_b23_10_and_through_the_scan_when_the_index_is_gone(two_trees):
    root, wt = two_trees
    jh.post_agent(payload(wt))
    (jl.lock_dir(root) / "open/a1b2c3").unlink()
    jh.record_returned(stop(root))
    assert len(events(wt, "returned")) == 1 and not events(root, "returned")


@pytest.mark.parametrize("index_gone", [False, True], ids=["through_the_index", "through_the_scan"])
def test_f1_a_stop_from_a_linked_worktree_without_dev_config_still_writes_returned_into_the_root_copy(two_trees, index_gone):
    root, wt = two_trees
    (wt / "tools/dev.config.yaml").unlink()                           # the real case: dev.config is untracked, no linked tree has it
    jh.post_agent(payload(root))
    assert events(root, "delegated")
    if index_gone:
        (jl.lock_dir(root) / "open/a1b2c3").unlink()
    assert not any("NOT" in x for x in jh.record_returned(stop(wt)))
    assert len(events(root, "returned")) == 1
    assert not (jl.lock_dir(root) / "pending-returns/a1b2c3").exists()


# ------------------------------------------------------------------ F2 / F4 / F5: the stop side is loud, and never doubles

class _Refused:
    written, path, line_no, task_id = False, None, None, None

    def __init__(self, text):
        self.messages = [text]


def _patch_returned(monkeypatch, behave):
    real = jw.write_event

    def fake(root, obj, **kw):
        return behave(real, root, obj, kw) if obj.get("event") == "returned" else real(root, obj, **kw)
    monkeypatch.setattr(jw, "write_event", fake)


def test_f2_a_refused_returned_is_logged_for_check_48c_keeps_its_marker_and_the_next_post_agent_retries_it(repo, monkeypatch):
    jh.post_agent(payload(repo))
    _patch_returned(monkeypatch, lambda real, root, obj, kw: _Refused("lock busy"))
    out = jh.record_returned(stop(repo))
    assert len(out) == 1 and out[0].startswith("JOURNAL: returned NOT written for agent:a1b2c3 -- lock busy")
    assert "NOT written for agent:a1b2c3" in (jl.lock_dir(repo) / "warn.log").read_text(encoding="utf-8")
    marker = jl.lock_dir(repo) / "pending-returns/a1b2c3"
    assert marker.is_file() and not events(repo, "returned")
    monkeypatch.undo()
    again = jh.post_agent(payload(repo, tool_response={"agentId": "a1b2c3", "status": "completed"}))
    assert len(events(repo, "returned")) == 1 and not marker.exists() and any(x.startswith("JOURNAL: returned t-") for x in again)


def test_f2_prune_warns_from_the_stop_path_reach_the_log_too(repo):
    folder = jl.lock_dir(repo)
    (folder / "pending-returns").mkdir(exist_ok=True)
    stale = folder / "pending-returns/stale1"
    stale.write_text("x")
    old = time.time() - 25 * 3600
    os.utime(stale, (old, old))
    out = jh.record_returned(stop(repo, "other9"))
    assert any("returned lost for agent:stale1" in x for x in out)
    assert "returned lost for agent:stale1" in (folder / "warn.log").read_text(encoding="utf-8")


def test_f4_a_lost_race_says_nothing_when_the_other_writer_already_wrote_returned(repo, monkeypatch):
    jh.post_agent(payload(repo))

    def other_writer_won(real, root, obj, kw):
        real(root, obj, **kw)                                         # the competitor's line lands first ...
        return _Refused("rule 9f: a second returned")                 # ... and ours is refused by the validator
    _patch_returned(monkeypatch, other_writer_won)
    assert jh.record_returned(stop(repo)) == []
    assert len(events(repo, "returned")) == 1 and not (jl.lock_dir(repo) / "warn.log").exists()


def test_f5_a_hook_failure_in_record_returned_is_one_line_not_silence(repo, monkeypatch):
    jh.post_agent(payload(repo))

    def boom(*a, **k):
        raise RuntimeError("x")
    monkeypatch.setattr(jh, "_locate", boom)
    out = jh.record_returned(stop(repo))
    assert out == ["JOURNAL: returned NOT recorded for agent:a1b2c3 -- the hook failed (RuntimeError)"]
    assert "NOT recorded for agent:a1b2c3" in (jl.lock_dir(repo) / "warn.log").read_text(encoding="utf-8")


# ------------------------------------------------------------------ F3: the stdin deadline

class _Hung:
    """A stdin with no EOF: read() blocks until released."""
    def __init__(self):
        self.release = threading.Event()
        outer = self

        class _Buf:
            def read(self):
                outer.release.wait(30)
                return b""
        self.buffer = _Buf()


@pytest.mark.parametrize("mode,expect_door", [("post-agent", True), ("pre-edit", False)])
def test_f3_a_stdin_with_no_eof_ends_at_the_deadline_with_the_door_or_silence(mode, expect_door, monkeypatch, capsys):
    hung = _Hung()
    monkeypatch.setattr(sys, "stdin", hung)
    monkeypatch.setenv("OSLLM_STDIN_TIMEOUT", "0.3")
    started = time.monotonic()
    try:
        code = jh.main([mode])
    finally:
        hung.release.set()
        jh._STDIN_DEADLINE_STATE["hit"] = False
    out = capsys.readouterr().out
    assert code == 0 and time.monotonic() - started < 10
    if expect_door:
        assert DOOR in json.loads(out)["hookSpecificOutput"]["additionalContext"] and "stdin deadline" in out
    else:
        assert out == ""


# ------------------------------------------------------------------ E-B23-11: parallel sessions

def test_e_b23_11_two_parallel_sessions_both_write_each_with_its_session_field(repo):
    results = {}

    def go(n):
        results[n] = jh.post_agent(payload(repo, agent_id=f"p{n}", session_id=f"sess000{n}-zzzz"))

    threads = [threading.Thread(target=go, args=(n,)) for n in (1, 2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    rows = events(repo, "delegated")
    assert sorted(o["session"] for o in rows) == ["sess0001", "sess0002"] and len({o["task_id"] for o in rows}) == 2


# ------------------------------------------------------------------ the stores: prune

def test_pending_markers_over_24h_and_index_entries_over_7_days_are_pruned_with_a_warn_each(repo):
    folder = jl.lock_dir(repo)
    (folder / "pending-returns").mkdir(exist_ok=True)
    (folder / "open").mkdir(exist_ok=True)
    old = time.time() - 25 * 3600
    fresh = folder / "pending-returns/fresh1"
    fresh.write_text("x")
    stale = folder / "pending-returns/stale1"
    stale.write_text("x")
    os.utime(stale, (old, old))
    ancient = folder / "open/anc1"
    ancient.write_text("x")
    os.utime(ancient, (time.time() - 8 * 86400,) * 2)
    young = folder / "open/young1"
    young.write_text("x")
    os.utime(young, (time.time() - 6 * 86400,) * 2)
    out = jh.prune(repo)
    assert any(x.startswith("JOURNAL: returned lost for agent:stale1 (stop at ") and x.endswith("no delegated found in 24 h)") for x in out)
    assert "JOURNAL: open-dispatch index entry for agent:anc1 pruned" in out and len(out) == 2
    assert fresh.exists() and young.exists() and not stale.exists() and not ancient.exists()


# ------------------------------------------------------------------ E-B23-13: pre-edit

JOURNAL_PATHS = ["logs/journal/dev1.jsonl", "C:\\x\\wt\\logs\\journal\\dev1.jsonl", "C:/x/logs/journal/../routing-log.jsonl",
                 "C:/X/WT/LOGS/Journal/dev1.jsonl", "c:/other-worktree/logs/routing-log.jsonl", "/abs/other/wt/logs/journal/dev2.jsonl"]
OTHER_PATHS = ["logs/other.jsonl", "src/app.py", "logs/journal/notes.md", "xlogs/routing-log.jsonl", "logs/journal/a/b.jsonl", ""]


def edit(path):
    return {"tool_name": "Edit", "tool_input": {"file_path": path}}


@pytest.mark.parametrize("path", JOURNAL_PATHS)
def test_e_b23_13_a_journal_path_warns_in_warn_mode_with_the_writer_door(monkeypatch, path):
    monkeypatch.setattr(jh, "JOURNAL_EDIT_MODE", "warn")
    hso = jh.pre_edit(edit(path))["hookSpecificOutput"]
    assert "permissionDecision" not in hso
    assert hso["additionalContext"].startswith("JOURNAL: by-hand edit -- the writer is python -B tools/journal_write.py <event>")
    assert "this becomes a refusal at node B23-S" in hso["additionalContext"] and "\n" not in hso["additionalContext"]


@pytest.mark.parametrize("path", JOURNAL_PATHS)
def test_e_b23_13_the_same_path_is_denied_in_refuse_mode_with_the_same_door(monkeypatch, path):
    monkeypatch.setattr(jh, "JOURNAL_EDIT_MODE", "refuse")
    hso = jh.pre_edit(edit(path))["hookSpecificOutput"]
    assert hso["permissionDecision"] == "deny" and "python -B tools/journal_write.py <event>" in hso["permissionDecisionReason"]


@pytest.mark.parametrize("mode", ["warn", "refuse"])
@pytest.mark.parametrize("path", OTHER_PATHS)
def test_e_b23_13_a_non_journal_path_is_silent_in_both_modes(monkeypatch, mode, path):
    monkeypatch.setattr(jh, "JOURNAL_EDIT_MODE", mode)
    assert jh.pre_edit(edit(path)) is None


@pytest.mark.parametrize("bad", [None, [], {}, {"tool_input": 5}, {"tool_input": {"file_path": 7}}])
def test_pre_edit_ignores_a_payload_without_a_path(bad):
    assert jh.pre_edit(bad) is None


def test_the_shipped_mode_is_warn():
    assert jh.JOURNAL_EDIT_MODE == "warn"


def test_pre_edit_main_prints_the_json_and_exits_zero(monkeypatch, capsys):
    code, out = run_main("pre-edit", json.dumps(edit("logs/journal/dev1.jsonl")).encode(), monkeypatch, capsys)
    assert code == 0 and "by-hand edit" in json.loads(out)["hookSpecificOutput"]["additionalContext"]
    code, out = run_main("pre-edit", b"garbage", monkeypatch, capsys)
    assert code == 0 and out == ""


def test_the_script_runs_as_a_hook_process_and_exits_zero_on_garbage(tmp_path):
    for mode in ("post-agent", "pre-edit"):
        proc = subprocess.run([sys.executable, str(TOOLS / "journal_hooks.py"), mode], input=b"\xff garbage", capture_output=True, cwd=tmp_path)
        assert proc.returncode == 0
