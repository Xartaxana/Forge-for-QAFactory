"""Tests of tools/journal_write.py (the one journal writer) and tools/journal_lock.py (offload spec r2 §3.B1, F-T1).

One table per subcommand family over a temp git repo with a seeded journal (never the real logs/journal); the concurrency
rows use real processes; the `--run` rows go through the real hygiene gate and real bash (skipped with a reason when the
probe finds no bash that sees the repo -- a capability). Row ids carry the E-B1-n of the spec."""
import contextlib
import datetime
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import journal_lock as jl  # noqa: E402
import journal_validator as jv  # noqa: E402
import journal_write as jw  # noqa: E402

JW = TOOLS / "journal_write.py"
SEED = ('{"ts":"2026-11-05T14:29:30","event":"journal_created","agent":"lead","category":"journal","feature":"F19",'
        '"notes":"seed"}\n')
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
DELEG = ["delegated", "--agent", "builder", "--model", "sonnet", "--feature", "F19", "--notes", "n"]


def git(repo, *args):
    return subprocess.run([*GIT, "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


@pytest.fixture(scope="module")
def template(tmp_path_factory):
    """A committed temp clone with the registry and the clone's letter claimed ("" for slug dev1)."""
    repo = tmp_path_factory.mktemp("tpl") / "r"
    (repo / "tools").mkdir(parents=True)
    (repo / "logs/journal").mkdir(parents=True)
    git(repo, "init", "-q")
    git(repo, "config", "core.autocrlf", "false")
    (repo / "tools/dev.config.yaml").write_text("developer: dev1\n")
    (repo / "tools/journal_write.py").write_text("# stub: the --run capability probe looks for this file\n")
    (repo / "logs/journal/dev1.jsonl").write_text(SEED)
    shutil.copy(TOOLS.parent / "logs/journal-letters.json", repo / "logs/journal-letters.json")
    assert cli(repo, "clone", "--claim")[0] == 0
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "seed")
    return repo


@pytest.fixture
def repo(template, tmp_path):
    dst = tmp_path / "r"
    shutil.copytree(template, dst)
    return dst


def cli(repo, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = jw.main([*args, "--repo", str(repo)])
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def lines(repo):
    return (repo / "logs/journal/dev1.jsonl").read_text(encoding="utf-8").splitlines()


def last(repo):
    return json.loads(lines(repo)[-1])


def deleg(repo, worker="agent:w1", *more):
    code, out, err = cli(repo, *DELEG, "--worker", worker, *more)
    assert code == 0, err
    return last(repo)["task_id"]


def refused(repo, *args, code=2, text=""):
    before = (repo / "logs/journal/dev1.jsonl").read_bytes()
    got, out, err = cli(repo, *args)
    assert got == code and text in err, (got, out, err)
    assert (repo / "logs/journal/dev1.jsonl").read_bytes() == before
    return err


@pytest.fixture
def needs_bash(repo):
    try:
        jw._find_bash(repo)
    except jw.Refused as exc:
        pytest.skip(f"no bash that sees this repo (capability of this machine): {exc.text}")


# ------------------------------------------------------------------ lock (E-B1-3, E-B1-15, S-2, S-3)

def test_e_b1_15_one_lock_path_from_root_subfolder_and_linked_worktree(repo, tmp_path):
    (repo / "sub").mkdir()
    git(repo, "worktree", "add", "-q", str(tmp_path / "wt2"))
    paths = {jl.lock_path(d, "journal") for d in (repo, repo / "tools", repo / "sub", tmp_path / "wt2")}
    assert paths == {(repo / ".git/forge-journal/journal.lock").resolve()}


@pytest.mark.parametrize("answer,sub,expect", [(".git", "", ".git"), ("../.git", "tools", ".git")], ids=["root", "subfolder"])
def test_s3_a_relative_common_dir_resolves_against_the_asked_dir(repo, monkeypatch, answer, sub, expect):
    def fake(directory, *args):
        if "--path-format=absolute" in args:
            raise jl.LockError("old git")
        return answer
    monkeypatch.setattr(jl, "git_out", fake)
    assert jl.common_dir(repo / sub) == (repo / expect).resolve()


HOLD = ("import sys, time; sys.path.insert(0, sys.argv[3]); import journal_lock as L\n"
        "with L.machine_lock('journal', 5, repo=sys.argv[1]):\n print('held', flush=True); time.sleep(float(sys.argv[2]))")


def test_e_b1_3_a_busy_lock_names_the_holder_and_writes_nothing(repo):
    p = subprocess.Popen([sys.executable, "-B", "-c", HOLD, str(repo), "6", str(TOOLS)], stdout=subprocess.PIPE, text=True)
    try:
        assert p.stdout.readline().strip() == "held"
        holder = jl.read_holder(jl.lock_path(repo, "journal"))          # bytes 0-63, readable while held (S-2)
        assert holder.split()[0] == str(p.pid)
        with pytest.raises(jl.LockBusy, match=f"held by pid {p.pid} since"):
            with jl.machine_lock("journal", 0.2, repo=repo):
                pass
        before = lines(repo)
        res = jw.write_event(repo, {"event": "dispatch_skipped", "agent": "builder", "category": "implementation",
                                    "notes": "x"}, lock_timeout=0.2)
        assert (res.written, res.code, lines(repo)) == (False, 3, before)
        assert "journal busy: held by pid" in res.messages[0]
    finally:
        p.kill()
        p.wait()
    with jl.machine_lock("journal", 2, repo=repo):          # the OS released it when the holder died
        pass


def test_lock_is_released_when_the_body_raises(repo):
    with pytest.raises(RuntimeError):
        with jl.machine_lock("journal", 1, repo=repo):
            raise RuntimeError
    with jl.machine_lock("journal", 0.5, repo=repo):
        pass


# ------------------------------------------------------------------ pure helpers

@pytest.mark.parametrize("n,expect_head,rows", [
    (3, "l0", 3), (41, "[… 1 lines cut]\nl1", 41), (400, "[… 360 lines cut]\nl360", 41)], ids=["short", "just-over", "long"])
def test_cut_witness_keeps_the_last_forty_lines(n, expect_head, rows):
    out = jw.cut_witness("\n".join(f"l{i}" for i in range(n)))
    assert out.startswith(expect_head) and out.endswith(f"l{n - 1}") and len(out.split("\n")) == rows


def test_cut_witness_caps_characters_and_a_giant_line():
    big = "\n".join("x" * 500 for _ in range(30))
    assert len(jw.cut_witness(big)) <= 6000 and jw.cut_witness(big).startswith("[… ")
    giant = jw.cut_witness("y" * 20000)
    assert len(giant) <= 6000 and giant.endswith("y")


# ------------------------------------------------------------------ E-B1-1 notes, E-B1-4 repo, events table

@pytest.mark.parametrize("notes,ok", [("a" * 300, True), ("a" * 301, False), ("", False), ("   ", False)],
                         ids=["at-300", "over-300", "empty", "whitespace"])
def test_e_b1_1_notes_limit_and_emptiness(repo, notes, ok):
    args = ("skip", "--agent", "builder", "--feature", "F19", "--notes", notes)
    if ok:
        assert cli(repo, *args)[0] == 0
    else:
        refused(repo, *args, text="notes are")


def test_e_b1_1_control_characters_never_split_the_line_and_non_ascii_stays_readable(repo):
    assert cli(repo, "skip", "--agent", "builder", "--feature", "F19", "--notes", "a\x00b\nc\x1fd é й")[0] == 0
    assert len(lines(repo)) == 2 and last(repo)["notes"] == "a b c d é й" and "é" in lines(repo)[-1]


def test_e_b1_4_not_a_git_repo_and_git_missing_write_nothing(tmp_path, monkeypatch, repo):
    assert cli(tmp_path, "skip", "--agent", "builder", "--notes", "x")[0] == 2
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    before = lines(repo)
    code, _out, err = cli(repo, "skip", "--agent", "builder", "--notes", "x")
    assert code == 2 and "git is not installed" in err and lines(repo) == before


EVENTS = [
    ("skip", ["--agent", "builder", "--feature", "F19", "--notes", "n"], "dispatch_skipped", {"category": "implementation"}),
    ("degraded", ["--reason", "r", "--scope", "s", "--feature", "F19", "--notes", "n"], "lead_degraded",
     {"agent": "lead", "reason": "r", "scope": "s", "category": "coordination"}),
    ("restored", ["--feature", "F19", "--notes", "n"], "lead_restored", {"agent": "lead", "category": "process"}),
    ("calibrated", ["--period", "p", "--events-reviewed", "7", "--feature", "F19", "--notes", "n"], "calibrated",
     {"events_reviewed": 7, "category": "calibration"}),
    ("event", ["--json", '{"event":"dispatch_skipped","agent":"scout","category":"recon","notes":"retroactive: n"}'],
     "dispatch_skipped", {"agent": "scout"}),
]


@pytest.mark.parametrize("cmd,args,event,fields", EVENTS, ids=[e[0] for e in EVENTS])
def test_events_without_a_task_write_their_shape(repo, cmd, args, event, fields):
    code, out, err = cli(repo, cmd, *args)
    assert code == 0 and out.startswith(f"journal: {event} - written (logs/journal/dev1.jsonl:2)"), (out, err)
    obj = last(repo)
    assert obj["event"] == event and obj["via"] == "cli" and obj["ts"][:2] == "20" and all(obj[k] == v for k, v in fields.items())


def test_a_task_family_escalate_defect_decomposable_reject_on_one_task(repo):
    t = deleg(repo)
    for cmd, args, key in [("escalate", ["--agent", "builder", "--model", "opus"], "model"),
                           ("decomposable", ["--agent", "builder"], "event"),
                           ("defect", ["--agent", "builder"], "ref"),
                           ("reject", ["--agent", "builder", "--model", "sonnet", "--by", "opus", "--attempt", "1",
                                       "--failure-class", "spec"], "failure_class")]:
        assert cli(repo, cmd, "--task", t, "--feature", "F19", "--notes", "n", *args)[0] == 0
        assert key in last(repo) and last(repo)["task_id"] == t
    assert last(repo)["event"] == "rejected" and last(repo)["attempt"] == 1


def test_an_agent_without_a_category_row_writes_other_with_a_warn(repo):
    code, out, _ = cli(repo, "skip", "--agent", "stranger", "--feature", "F19", "--notes", "n")
    assert code == 0 and last(repo)["category"] == "other" and "WARN agent 'stranger'" in out


def test_e_b1_7_equal_ts_legal_and_clock_behind_refused(repo, monkeypatch):
    fixed = datetime.datetime.now().replace(microsecond=0)
    monkeypatch.setattr(jw, "_now", lambda: fixed)
    assert cli(repo, "skip", "--agent", "builder", "--feature", "F19", "--notes", "a")[0] == 0
    assert cli(repo, "skip", "--agent", "builder", "--feature", "F19", "--notes", "b")[0] == 0
    monkeypatch.setattr(jw, "_now", lambda: fixed - datetime.timedelta(minutes=1))
    refused(repo, "skip", "--agent", "builder", "--feature", "F19", "--notes", "c", text="ts")


@pytest.mark.parametrize("args,text", [
    (["event", "--json", '{"ts":"2026-11-14T10:00:00","event":"calibrated","agent":"lead","category":"c","notes":"n"}'], "must not carry `ts`"),
    (["event", "--json", "[1]"], "one JSON object"),
    (["event", "--json", "{nope"], "not valid JSON"),
    (["event", "--json", '{"event":"made_up","agent":"lead","category":"c","notes":"n"}'], "enum"),
    (["event", "--json", '{"event":"calibrated","agent":"lead","category":"c","notes":"n","id_band":"t-500.."}'], "band"),
    (["reject", "--task", "t-001", "--agent", "builder", "--model", "m", "--by", "opus", "--attempt", "0",
      "--failure-class", "spec", "--notes", "n"], "attempt"),
], ids=["ts-given", "not-object", "broken-json", "bad-event", "band-retired", "attempt-zero"])
def test_a_violation_or_bad_input_writes_nothing_and_says_why(repo, args, text):
    deleg(repo)                                                       # t-001 exists for the reject row
    refused(repo, *args, text=text)


# ------------------------------------------------------------------ ids: E-B1-2, E-B1-5, E-B1-6, E-B1-13

def test_ids_are_issued_in_sequence_and_next_reserves_out_of_order_legal(repo):
    assert [deleg(repo, "agent:a"), deleg(repo, "agent:b")] == ["t-001", "t-002"]
    code, out, _ = cli(repo, "next", "--n", "3")
    assert (code, out.split()) == (0, ["t-003", "t-004", "t-005"])
    for tid in ("t-005", "t-003", "t-004"):                           # E-B1-13: reserved ids written out of order
        assert cli(repo, *DELEG, "--worker", f"agent:{tid}", "--task", tid)[0] == 0
    assert [json.loads(x).get("task_id") for x in lines(repo)[-3:]] == ["t-005", "t-003", "t-004"]
    assert deleg(repo, "agent:z") == "t-006"


@pytest.mark.parametrize("task,text", [
    ("t-905", "was not issued"), ("t-1", "expected a task id"), ("T-005", "expected a task id"), ("t-123A", "expected a task id"),
    ("t-123а", "expected a task id"), ("t-0123", "not canonical"), ("t-001b", "letter")],
    ids=["unissued", "short", "upper-T", "upper-letter", "cyrillic", "not-canonical", "foreign-letter"])
def test_e_b1_2_e_b1_13_a_given_new_id_must_be_issued_canonical_and_ours(repo, task, text):
    refused(repo, *DELEG, "--worker", "agent:q", "--task", task, text=text)


def test_e_b1_2_a_foreign_letter_id_on_an_existing_task_is_legal(repo):
    jw_line = ('{"ts":"2026-11-06T10:00:00","event":"delegated","agent":"builder","model":"sonnet","task_id":"t-050z",'
               '"category":"implementation","worker_ref":"agent:old","feature":"F19","notes":"other clone"}\n')
    with open(repo / "logs/journal/dev1.jsonl", "a", encoding="utf-8", newline="") as f:
        f.write(jw_line)
    assert cli(repo, "escalate", "--task", "t-050z", "--agent", "builder", "--model", "opus", "--feature", "F19", "--notes", "n")[0] == 0


@pytest.mark.parametrize("n", ["0", "21", "x"])
def test_next_bounds(repo, n):
    refused(repo, "next", "--n", n, code=2)


def test_without_a_registry_row_issuing_is_refused_with_the_claim_door(repo):
    (repo / "logs/journal-letters.json").write_text('{"letters": [\n]}\n')
    refused(repo, *DELEG, "--worker", "agent:w", text="clone --claim")
    refused(repo, "next", text="clone --claim")
    res = jw.write_event(repo, {"event": "delegated", "agent": "builder", "model": "m", "worker_ref": "w", "notes": "n"})
    assert not res.written and "clone --claim" in res.messages[0]


@pytest.mark.parametrize("content", ["{bad", "[]", '{"": -1}', '{"": "x"}', '{"A": 3}'], ids=["nonjson", "array", "negative", "text", "key"])
def test_e_b1_5_a_damaged_counter_is_rebuilt_higher_with_one_note(repo, content):
    deleg(repo)
    (repo / ".git/forge-journal/counter.json").write_text(content)
    code, out, err = cli(repo, *DELEG, "--worker", "agent:w2")
    assert code == 0 and last(repo)["task_id"] == "t-002" and err.count("damaged") == 1


def test_e_b1_5_e_b1_6_a_counter_below_the_file_max_and_a_crash_before_the_counter_never_reuse(repo):
    deleg(repo)
    line = jw_delegated_line("t-020")
    with open(repo / "logs/journal/dev1.jsonl", "a", encoding="utf-8", newline="") as f:
        f.write(line)                                                   # appended, the counter never touched
    assert json.loads((repo / ".git/forge-journal/counter.json").read_text())[""] == 1
    assert deleg(repo, "agent:w3") == "t-021"


def jw_delegated_line(tid):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    return json.dumps({"ts": ts, "event": "delegated", "agent": "builder", "model": "sonnet", "task_id": tid,
                       "category": "implementation", "worker_ref": "agent:hand", "feature": "F19", "notes": "by hand"}) + "\n"


# ------------------------------------------------------------------ returned, clone letters

def test_returned_takes_model_and_agent_from_the_delegated_and_never_closes(repo):
    t = deleg(repo, "agent:r1")
    assert cli(repo, "returned", "--task", t, "--worker", "agent:r1")[0] == 0
    obj = last(repo)
    assert (obj["event"], obj["agent"], obj["model"], obj["worker_ref"]) == ("returned", "builder", "sonnet", "agent:r1")
    refused(repo, "returned", "--task", t, "--worker", "agent:r1", text="returned")           # one per pair
    refused(repo, "returned", "--task", t, "--worker", "agent:nope", text="no delegated")


def test_clone_claim_is_idempotent_and_a_second_clone_of_one_slug_takes_the_next_letter(repo, tmp_path):
    assert "nothing to do" in cli(repo, "clone", "--claim")[1]
    assert "letter '(none)'" in cli(repo, "clone", "--show")[1]
    other = tmp_path / "second"
    git(tmp_path, "clone", "-q", str(repo), str(other))
    (other / "tools/dev.config.yaml").write_text("developer: dev1\n")
    code, out, _ = cli(other, "clone", "--claim")
    assert code == 0 and "letter 'a'" in out
    rows = json.loads((other / "logs/journal-letters.json").read_text())["letters"]
    assert [r["letter"] for r in rows] == ["", "a"] and rows[0]["clone"] != rows[1]["clone"]
    t = deleg(other)
    assert t == "t-001a"                                                  # a clone only issues ids of its own letter
    refused(other, *DELEG, "--worker", "agent:x", "--task", "t-002", text="letter")


def test_a_linked_worktree_of_the_claiming_clone_copies_the_row_and_keeps_the_letter(repo, tmp_path):
    wt = tmp_path / "wt"
    git(repo, "worktree", "add", "-q", str(wt))
    (wt / "tools/dev.config.yaml").write_text("developer: dev1\n")
    (wt / "logs/journal-letters.json").write_text('{"letters": [\n]}\n')             # the row is not merged there yet
    code, out, _ = cli(wt, "clone", "--claim")
    assert code == 0 and "claimed letter '(none)'" in out
    assert json.loads((wt / "logs/journal-letters.json").read_text())["letters"][0]["letter"] == ""


# ------------------------------------------------------------------ accept: witness rows

def accept(repo, t, *more, agent="builder", by="opus"):
    return cli(repo, "accept", "--task", t, "--agent", agent, "--model", "sonnet", "--by", by, "--feature", "F19",
               "--notes", "ok SECRETNOTE", *more)


def test_accept_text_witness_and_a_non_builder_without_one(repo):
    t = deleg(repo)
    code, out, err = accept(repo, t, "--witness", "SECRETWITNESS 5 passed")
    assert code == 0 and last(repo)["witness"] == "SECRETWITNESS 5 passed" and last(repo)["witness_by"] == "text"
    assert "SECRETWITNESS" not in out + err and "SECRETNOTE" not in out + err          # E-B1-16
    assert accept(repo, t, agent="scout", by="sonnet")[0] == 0 and "witness" not in last(repo)


@pytest.mark.parametrize("more,text", [
    ([], "needs a witness"), (["--witness", "a", "--witness-file", "x"], "exactly one"), (["--allow-red", "r"], "--run only"),
    (["--witness-file", "nofile.txt"], "does not exist")], ids=["none", "two", "allow-red-alone", "missing-file"])
def test_accept_refusals(repo, more, text):
    refused(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--feature", "F19",
            "--notes", "ok", *more, text=text)


@pytest.mark.parametrize("make,text", [
    (lambda p: p.mkdir(), "not a file"), (lambda p: p.write_bytes(b"\xff\xfe\x00bad"), "not UTF-8"),
    (lambda p: p.write_bytes(b"x" * ((1 << 20) + 1)), "1 MB"), (lambda p: p.write_text(" \n"), "empty")],
    ids=["directory", "non-utf8", "over-1MB", "empty"])
def test_e_b1_10_witness_file_refusals(repo, tmp_path, make, text):
    f = tmp_path / "w.txt"
    make(f)
    refused(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--feature", "F19",
            "--notes", "ok", "--witness-file", str(f), text=text)


def test_e_b1_10_a_long_witness_file_is_cut_from_the_start(repo, tmp_path):
    f = tmp_path / "w.txt"
    f.write_text("\n".join(f"line {i}" for i in range(100)), encoding="utf-8")
    assert accept(repo, deleg(repo), "--witness-file", str(f))[0] == 0
    w = last(repo)["witness"]
    assert w.startswith("[… 60 lines cut]\nline 60") and w.endswith("line 99") and last(repo)["witness_by"] == "file"


# ------------------------------------------------------------------ --run: E-B1-8, E-B1-9

def test_e_b1_8_run_green_red_and_allow_red(repo, needs_bash):
    t = deleg(repo)
    code, out, err = accept(repo, t, "--run", "echo green-output")
    assert code == 0 and "run: exit=0" in out and "green-output" not in out + err
    assert last(repo)["witness"] == "$ echo green-output\ngreen-output\nexit=0" and last(repo)["witness_by"] == "run"
    n = len(lines(repo))
    refused(repo, "accept", "--task", t, "--agent", "builder", "--model", "sonnet", "--by", "opus", "--feature", "F19",
            "--notes", "ok", "--run", "exit 3", text="non-zero")
    assert len(lines(repo)) == n
    assert accept(repo, t, "--run", "exit 3", "--allow-red", "known red")[0] == 0
    assert "allow-red: known red" in last(repo)["notes"] and last(repo)["witness"].endswith("exit=3")


def test_e_b1_8_a_missing_or_blind_bash_refuses_with_the_witness_file_door(repo, monkeypatch):
    t = deleg(repo)
    for which in (lambda _n: None, lambda _n: sys.executable):          # no bash / a launcher that does not see the repo
        monkeypatch.setattr(jw.shutil, "which", which)
        refused(repo, "accept", "--task", t, "--agent", "builder", "--model", "sonnet", "--by", "opus", "--notes", "ok",
                "--run", "echo hi", text="--witness-file")


def test_e_b1_8_a_timeout_kills_the_run_and_writes_nothing(repo, needs_bash, monkeypatch):
    monkeypatch.setattr(jw, "RUN_TIMEOUT", 1)
    refused(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--notes", "ok",
            "--run", "sleep 20", code=3, text="timed out")


@pytest.mark.parametrize("cmd", [
    "echo x >> logs/journal/dev1.jsonl", "echo x >> logs\\journal\\dev1.jsonl",
    "python -c \"open('logs/journal/dev1.jsonl','a').write('x')\"", "cd tools && pytest", "$(echo cd) x", "echo " + "a" * 70000],
    ids=["redirect", "backslash", "python-c", "cd", "dynamic-word", "70KB"])
def test_e_b1_9_refused_by_the_gate_before_anything_runs(repo, needs_bash, cmd):
    refused(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--notes", "ok",
            "--run", cmd, text="refused by the hygiene gate")


def test_e_b1_9_git_checkout_on_a_dirty_tree_and_a_nul_byte_are_refused(repo, needs_bash):
    (repo / "tools/dev.config.yaml").write_text("developer: dev1\n# dirty\n")
    refused(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--notes", "ok",
            "--run", "git checkout -- .", text="refused by the hygiene gate")
    with pytest.raises(jw.Refused):
        jw.run_witness("echo a\x00b", repo, allow_red=None)


@pytest.mark.parametrize("cmd", ["echo ' >> logs\\journal\\probe.jsonl '", "python -m pytest -q ' & echo x >> logs\\journal\\probe.jsonl '"],
                         ids=["echo-quoted", "pytest-quoted"])
def test_e_b1_9_quoted_redirects_stay_harmless_under_bash(repo, needs_bash, cmd):
    cli(repo, "accept", "--task", deleg(repo), "--agent", "builder", "--model", "sonnet", "--by", "opus", "--notes", "ok",
        "--run", cmd, "--allow-red", "probe")
    assert not (repo / "logs/journal/probe.jsonl").exists()


# ------------------------------------------------------------------ concurrency: E-B1-11, E-B1-12, E-B1-14 (real processes)

def spawn(repo, *args):
    return subprocess.Popen([sys.executable, "-B", str(JW), *args, "--repo", str(repo)], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)


def test_e_b1_11_simultaneous_delegations_get_distinct_ids(repo):
    procs = [spawn(repo, *DELEG, "--worker", f"agent:p{i}") for i in range(4)]
    assert [p.wait(timeout=120) for p in procs] == [0, 0, 0, 0]
    ids = [json.loads(x)["task_id"] for x in lines(repo)[1:]]
    assert len(set(ids)) == 4 and jv.decide("\n".join(lines(repo)) + "\n", SEED)[0] == 0


def test_e_b1_12_two_worktrees_issue_distinct_numbers_and_their_copies_union_merge(repo, tmp_path):
    wt = tmp_path / "wt2"
    git(repo, "worktree", "add", "-q", str(wt))
    (wt / "tools/dev.config.yaml").write_text("developer: dev1\n")
    ids = []
    for i in range(3):
        for where in (repo, wt):
            assert cli(where, *DELEG, "--worker", f"agent:{where.name}{i}")[0] == 0
            ids.append(json.loads((where / "logs/journal/dev1.jsonl").read_text().splitlines()[-1])["task_id"])
    assert len(set(ids)) == 6
    merged = sorted({*lines(repo)[1:], *(wt / "logs/journal/dev1.jsonl").read_text().splitlines()[1:]},
                    key=lambda s: json.loads(s)["ts"])
    assert jv.decide(SEED + "\n".join(merged) + "\n", SEED)[0] == 0


def test_e_b1_14_a_slow_run_in_one_process_does_not_block_another_writer(repo, tmp_path, needs_bash):
    t = deleg(repo)
    flag = (tmp_path / "started").as_posix()
    a = spawn(repo, "accept", "--task", t, "--agent", "builder", "--model", "sonnet", "--by", "opus", "--feature", "F19",
              "--notes", "ok", "--run", f"touch {flag}; sleep 6")
    try:
        deadline = time.monotonic() + 60
        while not Path(flag).exists() and a.poll() is None and time.monotonic() < deadline:
            time.sleep(0.1)
        assert Path(flag).exists(), a.communicate()
        started = time.monotonic()
        b = spawn(repo, *DELEG, "--worker", "agent:b")
        assert b.wait(timeout=30) == 0 and a.poll() is None                    # B wrote while A's command still ran
        assert time.monotonic() - started < 5.5
        assert a.wait(timeout=60) == 0
    finally:
        a.kill()
    events = [json.loads(x)["event"] for x in lines(repo)[2:]]
    assert events == ["delegated", "accepted"]


def test_hooks_call_the_library_with_a_short_timeout_and_never_get_an_exception(repo):
    res = jw.write_event(repo, {"event": "dispatch_skipped", "agent": "builder", "category": "implementation",
                                "notes": "h" * 400}, via="hook", lock_timeout=5)
    assert res.written and last(repo)["via"] == "hook"                         # the 300 limit is the CLI's
    assert jw.write_event(repo / "missing", {"event": "x"}).written is False
    assert jw.write_event(repo, {"event": "dispatch_skipped"}).written is False
