#!/usr/bin/env python3
"""B-012: an infrastructure failure of `claude -p` is not a role's result.

On TP1-13877 a login error, a usage limit and a Cloudflare page each came back from `claude -p`
as the "final message" of a role; the driver resumed the role on them, called the conductor with
them and put them to the person as the conductor's question (5 conductor sessions and 4 resumes,
`state/driver-runs.jsonl` rows 1-4, 7, 17). Nothing here reaches a network or a model: `claude` is
the stub of `story_run_common.py` behind a PRELUDE that pops `control["infra_queue"]` (one entry per
call: a JSON result or raw text, its stderr, its exit code, and the files the cut-off role had
already written) and only when the queue is empty runs the ordinary stub. Every call, queued or
not, is logged with its argv, its prompt and the environment names the control asks about.

What is proved (K = the acceptance keys of the spec):
  K1  the classifier on the three wire forms, and where it must say nothing;
  K2  auth stops the driver with exit 5 - no question file, no conductor, no saved result;
  K3  limit: the reset is quoted, or its absence is said; the session that worked is kept;
  K4  transient then success: one retry after 5 s that resumes the failed session;
  K5  transient x3: exactly three calls (AT the limit) and never a fourth (BEYOND it);
  K6  which session a retry or a rerun continues, at the num_turns boundary;
  K7  a rerun continues the interrupted dispatch, by resume or fresh with a note;
  K8  a result saved by the driver before this change (the 13877 S3 file) is classified too;
  K9  the conductor's own call is covered; K10 the S0 tracker read (t-267: REST, a lost login is
      the adapter's exit 5, not a tracker-agent call); K11 unclassified is
      today's path; K12 the child environment; K13 UTF-8 children; K14 the texts obey the human
      text rules; K15 a retry does not count as a conductor call.
"""
import contextlib
import io
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in, finish  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import story_run_common as T  # noqa: E402

TASK = "QA-9"
START_CWD = os.getcwd()

# The texts of TP1-13877, VERBATIM (state/conductor.jsonl rows 2 and 5; state/driver-runs/
# S3-qa-test-strategist-1.json). The dots and the dash are written as code points so that the
# file stays plain ASCII.
AUTH = "Not logged in " + chr(0xB7) + " Please run /login"
LIMIT = "You've hit your weekly limit " + chr(0xB7) + " resets 2am (Europe/Madrid)"
LIMIT_NO_RESET = "You've hit your limit"
MALFORMED = ("API Error: API returned an empty or malformed response (HTTP 200) \u2014 check for a proxy or "
             "gateway intercepting the request. Response: content-type html, body is an HTML page, 16066 "
             "bytes, request-id absent, server cloudflare, intermediary headers cf-cache-status cf-ray "
             "content-encoding transfer-encoding. This was the non-streaming retry of streaming request "
             "(no Anthropic request-id), which failed with: no_events, StreamNoEventsError; 0 stream "
             "events received.")
S3_SAVED = {"session_id": "531ae422-15be-43a9-bbef-2bcb38cb8e2d", "result": MALFORMED, "num_turns": 29,
            "total_cost_usd": 2.0212816, "duration_ms": 1048688, "is_error": True, "exit_code": 1, "stderr": ""}

PRELUDE = r'''
import io, json, os, re, sys
from pathlib import Path
_data = sys.stdin.buffer.read()
sys.stdin = io.TextIOWrapper(io.BytesIO(_data), encoding="utf-8")
_control = json.loads(Path(os.environ["STUB_CONTROL"]).read_text(encoding="utf-8"))
_dir = Path(os.environ["STUB_LOG"]).parent
_count = _dir / "infra-count.txt"
_n = int(_count.read_text()) if _count.exists() else 0
_queue = _control.get("infra_queue") or []
_prompt = _data.decode("utf-8")
with (_dir / "infra-log.jsonl").open("a", encoding="utf-8") as _h:
    _h.write(json.dumps({"n": _n, "queued": _n < len(_queue), "argv": sys.argv[1:], "prompt": _prompt,
                         "env": {k: os.environ.get(k) for k in _control.get("log_env") or []}}) + "\n")
if _n < len(_queue):
    _count.write_text(str(_n + 1))
    _e = _queue[_n]
    _m = re.search(r"Artifacts dir: (\S+)", _prompt)
    if _m:
        for _rel, _c in (_e.get("files") or {}).items():
            _p = Path(_m.group(1)) / _rel
            _p.parent.mkdir(parents=True, exist_ok=True)
            _p.write_text(_c, encoding="utf-8")
    if "json" in _e and not _e["json"].get("is_error"):
        write_receipt(_e["json"].get("session_id"))     # a queued SUCCESS is a session whose hooks reported (B-014)
    if "raw" in _e:
        sys.stdout.buffer.write(_e["raw"].encode("utf-8"))
    else:
        sys.stdout.buffer.write(json.dumps(_e["json"]).encode("utf-8"))
    sys.stderr.write(_e.get("stderr", ""))
    sys.stderr.flush()
    sys.stdout.flush()
    sys.exit(int(_e.get("exit", 1)))
'''

LOG_ENV = ["ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY", "CLAUDE_CODE_USE_BEDROCK",
           "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST", "CLAUDE_CODE_HOST_AUTH_ENV_VAR", "MY_TOK", "FOO",
           "PYTHONUTF8", "PYTHONIOENCODING"]
FILES = {"work/context-manifest.json": json.dumps(T.GOOD_MANIFEST).replace("{task}", TASK),
         "work/context-bundle.json": "{}"}
DIGEST = T.SCOUT_DIGEST.replace("{task}", TASK)


def entry(text, *, turns=1, session="sess-infra", cost=0, files=None, exit_code=1, stderr="", subtype="success"):
    return {"json": {"type": "result", "subtype": subtype, "is_error": True, "session_id": session,
                     "num_turns": turns, "total_cost_usd": cost, "duration_ms": 10, "result": text},
            "exit": exit_code, "files": files or {}, "stderr": stderr}


def control(queue=None, **more):
    base = {"roles": {"qa-scout": {"files": FILES, "result": DIGEST}}, "resume": {"result": DIGEST},
            "conductor": {"action": "continue", "did": "nothing"}, "log_env": LOG_ENV,
            "infra_queue": queue or []}
    base.update(more)
    return base


def install(root, ctl):
    (root / "fake_claude.py").write_text(T.RECEIPT + PRELUDE + T.STUB, encoding="utf-8")
    T.set_control(root, ctl)


def calls(root):
    """Every claude call the stub saw. The prompt arrives with the platform's newlines (subprocess text
    mode writes CRLF on Windows): normalised here, because the tests compare words, not line ends."""
    rows = T.jsonl(root / "infra-log.jsonl")
    for row in rows:
        row["prompt"] = row["prompt"].replace("\r\n", "\n")
    return rows


def taken(root):
    path = root / "infra-count.txt"
    return int(path.read_text()) if path.exists() else 0


def prompt_for(task_root, dispatch="S1-qa-scout-1"):
    return f"You are qa-scout. Dispatch: {dispatch}.\nArtifacts dir: {task_root}\nDo the work."


def project_of(ctl=None, task=TASK, **over):
    """A seeded project whose `claude` is the queue stub, and an in-process Driver over it whose
    sleeps are recorded, never taken."""
    root, task_root, env = T.seed(task)
    install(root, ctl or control())
    driver = T.driver_for(root, env, task, **over)
    delays = []
    driver.sleep = delays.append
    return root, task_root, env, driver, delays


def done(root):
    os.chdir(START_CWD)
    harness.cleanup(root)


def scenario(fn):
    try:
        fn()
    except Exception:  # a scenario that cannot even run is a red result, not a crash of the others
        check(f"{fn.__name__} ran to its end", False, traceback.format_exc()[-1500:])
        os.chdir(START_CWD)


def state_of(task_root):
    return T.s0_state(task_root)


def infra_of(exc_or_none):
    return getattr(exc_or_none, "kind", None)


def raised(driver, *args, **kwargs):
    """(InfraStop or None, result or None) of one run_claude call."""
    import story_run
    try:
        return None, driver.run_claude(*args, **kwargs)
    except story_run.InfraStop as stop:
        return stop, None


# --- K1 -----------------------------------------------------------------------------------------
def k1_classify():
    import hooklib
    import infra_failure as I
    rules, notes = I.rules()
    check_eq("K1: the shipped data file is read without a note", notes, [])
    check("K1: and carries the wire rows", {"not_logged_in", "usage_limit", "malformed_response"}
          <= {r["id"] for r in rules.get("failures", [])})
    call = {"is_error": True, "exit_code": 1, "stderr": ""}
    got = I.classify(dict(call, result=AUTH), rules)
    check_eq("K1: `Not logged in` is auth", (got["kind"], got["rule"]), ("auth", "not_logged_in"))
    got = I.classify(dict(call, result=LIMIT), rules)
    check_eq("K1: a usage limit is limit, with the reset as the service wrote it",
             (got["kind"], got["reset"]), ("limit", "2am (Europe/Madrid)"))
    check_eq("K1: a limit that names no reset has an empty one", I.classify(dict(call, result=LIMIT_NO_RESET), rules)["reset"], "")
    got = I.classify(dict(call, result=MALFORMED), rules)
    check_eq("K1: the Cloudflare page is transient and carries its retry word",
             (got["kind"], got["retry_code"]), ("transient", "service_unavailable"))
    check_eq("K1: the saved 13877 S3 file classifies the same", I.classify(S3_SAVED, rules)["kind"], "transient")
    fixture = harness.PLUGIN_ROOT.parents[1] / "experiments/TP1-13877/state/driver-runs/S3-qa-test-strategist-1.json"
    if fixture.is_file():  # only where the repository that made this test is around
        check_eq("K1: and the embedded text IS the fixture's", json.loads(fixture.read_text(encoding="utf-8")),
                 {k: S3_SAVED[k] for k in ("session_id", "result", "num_turns", "total_cost_usd", "duration_ms", "is_error", "exit_code", "stderr")})
    check_eq("K1: the words of a call that did not fail are never read (FR-12)",
             I.classify({"is_error": False, "exit_code": 0, "result": AUTH}, rules), None)
    check_eq("K1: a non-zero exit with is_error false is a failed call and is read",
             I.classify({"is_error": False, "exit_code": 1, "result": AUTH}, rules)["kind"], "auth")
    check_eq("K1: is_error with exit 0 is read as well",
             I.classify({"is_error": True, "exit_code": 0, "result": AUTH}, rules)["kind"], "auth")
    check_eq("K1: max turns is the role's own outcome, whatever the text says",
             I.classify(dict(call, result=AUTH, subtype="error_max_turns"), rules), None)
    check_eq("K1: an unmatched failure is unclassified", I.classify(dict(call, result="boom"), rules),
             {"kind": "unclassified", "rule": ""})
    check_eq("K1: an empty result is read from stderr",
             I.classify(dict(call, result="", stderr=AUTH), rules)["kind"], "auth")
    check_eq("K1: empty everywhere, still a failure: unclassified",
             I.classify(dict(call, result=""), rules)["kind"], "unclassified")

    real = hooklib.load_ref_json
    hooklib.load_ref_json = lambda name: {} if name == "driver-infra.json" else real(name)
    try:
        gone, notes = I.rules()
        check_eq("K1: with the data file absent the rules are empty", gone, {})
        check_in("K1: and one note says so", "references/driver-infra.json unreadable", notes)
        check_eq("K1: every failure is then unclassified", I.classify(dict(call, result=AUTH), gone)["kind"], "unclassified")
    finally:
        hooklib.load_ref_json = real
    bad = {"failures": [{"id": "broken", "kind": "auth", "pattern": "(unclosed"},
                        {"id": "fine", "kind": "auth", "pattern": "Not logged in"},
                        {"id": "odd", "kind": "sulk", "pattern": "x"}]}
    hooklib.load_ref_json = lambda name: bad if name == "driver-infra.json" else real(name)
    try:
        partial, notes = I.rules()
        check_eq("K1: a row whose regex does not compile is skipped, a row of an unknown kind too",
                 [r["id"] for r in partial["failures"]], ["fine"])
        check_eq("K1: each skip is named", sum("skipped" in n for n in notes), 2)
        check_eq("K1: and the other rows still match", I.classify(dict(call, result=AUTH), partial)["rule"], "fine")
    finally:
        hooklib.load_ref_json = real


# --- K2, K3, K7: a stop and a rerun ---------------------------------------------------------------
def k2_auth_stops_the_driver():
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control([entry(AUTH)]))
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "1")
        T.eq("K2: exit 5", out.returncode, 5, out.stdout[-1200:] + out.stderr[-600:])
        check_in("K2: stdout says the login is missing", "logged in", out.stdout)
        check_in("K2: and gives the command to go on", "story_run.py", out.stdout)
        check_in("K2: with the task and the project", f"--task {TASK} --project", out.stdout)
        check_not_in("K2: no answer file in a command that has nothing to answer", "--answer", out.stdout)
        check("K2: no question file for the person", not (task_root / "state/driver-question.md").exists())
        check_eq("K2: the ordinary stub was never reached: no conductor call, no role call", T.stub_calls(root), [])
        check_eq("K2: exactly one claude call", len(calls(root)), 1)
        check("K2: no conductor row", not (task_root / "state/conductor.jsonl").exists())
        check("K2: no saved role result", not (task_root / "state/driver-runs/S1-qa-scout-1.json").exists())
        held = state_of(task_root)
        record = (held.get("interrupted") or {}).get("S1-qa-scout-1") or {}
        check_eq("K2: the dispatch is recorded as interrupted by auth", (record.get("kind"), record.get("rule")),
                 ("auth", "not_logged_in"))
        check_eq("K2: a one-turn call did no work", record.get("worked"), False)
        check_eq("K2: the record names the call, the stage, the role and the dispatch",
                 (record.get("call"), record.get("stage"), record.get("role"), record.get("dispatch")),
                 ("role", "S1", "qa-scout", "S1-qa-scout-1"))
        check("K2: and no session is stored for it", "S1-qa-scout-1" not in (held.get("sessions") or {}))
        runs = T.jsonl(task_root / "state/driver-runs.jsonl")
        check_eq("K2: one journal line for the one invocation", len(runs), 1)
        check_eq("K2: it carries subtype, infra, rule and retry",
                 (runs[0].get("subtype"), runs[0].get("infra"), runs[0].get("infra_rule"), runs[0].get("retry")),
                 ("success", "auth", "not_logged_in", 0))
        check_eq("K2: the dispatch is still the controller's (running), not dropped",
                 json.loads((task_root / "state/controller.json").read_text(encoding="utf-8"))["dispatches"]["S1-qa-scout-1"]["status"],
                 "running")

        # K7 (after K2): the rerun finds the interrupted record and starts the role fresh, with the note
        install(root, control([entry(AUTH)]))
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "1")
        T.eq("K7: the rerun after an auth stop finishes the stage", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        log = calls(root)
        check_eq("K7: it made one more claude call", len(log), 2)
        second = log[1]
        check_not_in("K7: a session that did nothing is not resumed", "--resume", " ".join(second["argv"]))
        check_in("K7: the fresh prompt says this is not a rework", "Not a rework: continue this dispatch", second["prompt"])
        check_in("K7: and carries the note", "cut by an infrastructure failure", second["prompt"])
        check_in("K7: and the original dispatch prompt", "Dispatch: S1-qa-scout-1.", second["prompt"])
        check_eq("K7: S1 is done", json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))["stages"]["S1"]["status"], "done")
        check_eq("K7: the interrupted record is cleared by the successful call", state_of(task_root).get("interrupted"), {})
    finally:
        done(root)


def k3_limit_worked_then_continued():
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control([entry(LIMIT, turns=15, session="sess-limit", cost=8.67, files=FILES)]))
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "1")
        T.eq("K3: exit 5", out.returncode, 5, out.stdout[-1200:])
        check_in("K3: the reset is quoted as the service wrote it", "2am (Europe/Madrid)", out.stdout)
        record = (state_of(task_root).get("interrupted") or {}).get("S1-qa-scout-1") or {}
        check_eq("K3: fifteen turns is work: worked, with its session", (record.get("worked"), record.get("session_id"), record.get("num_turns")),
                 (True, "sess-limit", 15))
        check_eq("K3: and the reset is in the record", record.get("reset"), "2am (Europe/Madrid)")

        # K7 (after K3): the rerun RESUMES that session with the note alone
        install(root, control())
        (root / "infra-count.txt").unlink()
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "1")
        T.eq("K7: the rerun after a limit stop finishes the stage", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        second = calls(root)[-1]
        check_eq("K7: it resumes the session that worked", second["argv"][second["argv"].index("--resume") + 1], "sess-limit")
        check_in("K7: with the note", "cut by an infrastructure failure", second["prompt"])
        check_in("K7: which lists what the role had written", "work/context-manifest.json (", second["prompt"])
        check_not_in("K7: and is not the dispatch prompt again", "Dispatch:", second["prompt"])
        check_in("K7: it ends in the handoff form", "· ok|concerns|halt|impossible", second["prompt"])
        check_eq("K7: the record is cleared", state_of(task_root).get("interrupted"), {})
        check_eq("K7: the session is stored now", state_of(task_root)["sessions"].get("S1-qa-scout-1"), "sess-limit")
    finally:
        done(root)


def k3_a_second_stop_keeps_the_session_that_worked():
    """A rerun resumes the worked session and the login fails at one turn: the record keeps that
    session (worked, its turns) and refreshes only what failed; the next rerun resumes it."""
    queue = [entry(LIMIT, turns=15, session="sess-limit"), entry(AUTH, turns=1, session="sess-limit")]
    root, task_root, env, driver, delays = project_of(control(queue))
    try:
        args = ("role", prompt_for(task_root))
        kw = dict(role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        stop, _ = raised(driver, *args, **kw)
        check_eq("K3b: the first stop is the limit, worked", (infra_of(stop), driver.state["interrupted"]["S1-qa-scout-1"]["worked"]), ("limit", True))
        stop, _ = raised(driver, *args, **kw)
        record = driver.state["interrupted"]["S1-qa-scout-1"]
        check_eq("K3b: the rerun resumed the recorded session and met auth", (infra_of(stop), calls(root)[1]["argv"][calls(root)[1]["argv"].index("--resume") + 1]), ("auth", "sess-limit"))
        check_eq("K3b: the record still has the session, worked, and its 15 turns",
                 (record["session_id"], record["worked"], record["num_turns"]), ("sess-limit", True, 15))
        check_eq("K3b: only what failed is refreshed", (record["kind"], record["rule"]), ("auth", "not_logged_in"))
        stop, result = raised(driver, *args, **kw)
        third = calls(root)[2]
        check_eq("K3b: the next rerun resumes that session", (stop, third["argv"][third["argv"].index("--resume") + 1]), (None, "sess-limit"))
        check_eq("K3b: and the record leaves", driver.state["interrupted"], {})
    finally:
        done(root)
    # a stop of a FRESH session (the record did no work) overwrites, as before
    root, task_root, env, driver, delays = project_of(control([entry(AUTH, turns=1, session="sess-a"), entry(AUTH, turns=1, session="sess-b")]))
    try:
        raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        record = driver.state["interrupted"]["S1-qa-scout-1"]
        check_eq("K3b: a fresh-session stop overwrites the record", (record["session_id"], record["worked"]), ("sess-b", False))
    finally:
        done(root)


def k5_transient_retries_keep_the_recorded_session():
    """The driver resumed the session that worked (step a); three broken answers at one turn must not
    send the retries to a fresh session or overwrite the record."""
    queue = [entry(MALFORMED, turns=1, session="sess-x") for _ in range(3)]
    root, task_root, env, driver, delays = project_of(control(queue))
    try:
        driver.state["interrupted"]["S1-qa-scout-1"] = {"kind": "limit", "rule": "usage_limit", "session_id": "sess-prior",
                                                        "num_turns": 15, "worked": True, "call": "role"}
        stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        log = calls(root)
        check_eq("K5b: three calls, then the stop", (infra_of(stop), len(log)), ("transient", 3))
        check_eq("K5b: every call resumes the recorded session",
                 [c["argv"][c["argv"].index("--resume") + 1] if "--resume" in c["argv"] else None for c in log], ["sess-prior"] * 3)
        check_not_in("K5b: with the note, never the dispatch prompt", "Dispatch:", log[2]["prompt"])
        record = driver.state["interrupted"]["S1-qa-scout-1"]
        check_eq("K5b: the record keeps the session and that it worked",
                 (record["session_id"], record["worked"], record["num_turns"], record["kind"]), ("sess-prior", True, 15, "transient"))
    finally:
        done(root)


def k3_a_limit_without_a_reset_says_so():
    root, task_root, env, driver, delays = project_of(control([entry(LIMIT_NO_RESET, turns=2, session="sess-l2")]))
    try:
        stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K3: a limit without a reset stops as limit", infra_of(stop), "limit")
        check_in("K3: and says the service named no reset time", "no reset time", stop.reason if stop else "")
        check_eq("K3: two turns count as work", driver.state["interrupted"]["S1-qa-scout-1"]["worked"], True)
        check_eq("K3: a limit is not retried", (delays, len(calls(root))), ([], 1))
    finally:
        done(root)


# --- K4, K5 ---------------------------------------------------------------------------------------
def k4_transient_then_success():
    root, task_root, env, driver, delays = project_of(
        control([entry(MALFORMED, turns=3, session="sess-cut", files=FILES)]), max_boundaries=1)
    try:
        code = driver.run()
        check_eq("K4: the story goes on: exit 0", code, 0)
        check_eq("K4: one sleep of five seconds", delays, [5])
        log = calls(root)
        check_eq("K4: two calls", len(log), 2)
        argv = log[1]["argv"]
        check_eq("K4: the second resumes the session that failed", argv[argv.index("--resume") + 1], "sess-cut")
        check_in("K4: its prompt carries the note", "cut by an infrastructure failure", log[1]["prompt"])
        check_not_in("K4: and is not the dispatch prompt", "Dispatch:", log[1]["prompt"])
        check_eq("K4: S1 is done", json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))["stages"]["S1"]["status"], "done")
        check_eq("K4: the ordinary stub saw the retry only (a resume), no conductor", [c["kind"] for c in T.stub_calls(root)], ["resume"])
        check("K4: no conductor row", not (task_root / "state/conductor.jsonl").exists())
        runs = T.jsonl(task_root / "state/driver-runs.jsonl")
        check_eq("K4: two journal lines, the retry counted", [(r["infra"], r["retry"], r["resumed"]) for r in runs],
                 [("transient", 0, False), (None, 1, True)])
        check_eq("K4: and the malformed text is nowhere in a refusal or a question",
                 (task_root / "state/driver-question.md").exists(), False)
    finally:
        done(root)


def k5_transient_three_times():
    import story_run
    queue = [entry(MALFORMED, session="sess-a"), entry(MALFORMED, session="sess-b"), entry(MALFORMED, session="sess-c"),
             entry(MALFORMED, session="sess-never")]
    root, task_root, env, driver, delays = project_of(control(queue))
    try:
        stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K5: three broken answers in a row stop the driver as transient", infra_of(stop), "transient")
        check_eq("K5: the exit code is 5", stop.code if stop else None, story_run.EXIT_INFRA)
        check_eq("K5: the waits are 5 and 15 seconds", delays, [5, 15])
        check_eq("K5: exactly three calls - AT the limit", len(calls(root)), 3)
        check_eq("K5: and no fourth - BEYOND it", taken(root), 3)
        runs = T.jsonl(task_root / "state/driver-runs.jsonl")
        check_eq("K5: three journal lines, retry 0, 1, 2", [r["retry"] for r in runs], [0, 1, 2])
        check_in("K5: the message counts the answers", "3 times in a row", stop.reason if stop else "")
        check("K5: no session is stored for the dispatch", "S1-qa-scout-1" not in driver.state["sessions"])
        check_eq("K5: the dispatch is recorded as interrupted", driver.state["interrupted"]["S1-qa-scout-1"]["kind"], "transient")
        check_eq("K5: retries never became conductor calls", driver.conductor_calls, {})
    finally:
        done(root)


def k5_two_retries_then_success_is_at_the_limit():
    queue = [entry(MALFORMED, session="sess-a"), entry(MALFORMED, session="sess-b")]
    root, task_root, env, driver, delays = project_of(control(queue))
    try:
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K5: two retries and then an answer is not a stop", (stop, bool(result)), (None, True))
        check_eq("K5: with both waits", delays, [5, 15])
        check_eq("K5: on the third call", len(calls(root)), 3)
        check_eq("K5: and the result is the role's own", result["is_error"], False)
    finally:
        done(root)


# --- K6 -------------------------------------------------------------------------------------------
def k6_resume_choice():
    def retry_of(first, **kwargs):
        root, task_root, env, driver, delays = project_of(control([first]))
        try:
            p = prompt_for(task_root)
            stop, result = raised(driver, "role", p, role="qa-scout", dispatch="S1-qa-scout-1", stage="S1", **kwargs)
            log = calls(root)
            return stop, result, log, p, driver
        finally:
            done(root)

    def resumed(log):
        argv = log[1]["argv"]
        return argv[argv.index("--resume") + 1] if "--resume" in argv else None

    stop, result, log, p, _ = retry_of(entry(MALFORMED, turns=1, session="sess-t1"))
    check_eq("K6: one turn: the retry of a first call starts fresh", resumed(log), None)
    check_eq("K6: and with the prompt as it was", log[1]["prompt"], p)
    stop, result, log, p, _ = retry_of(entry(MALFORMED, turns=2, session="sess-t2"))
    check_eq("K6: two turns: the retry resumes that session", resumed(log), "sess-t2")
    check_in("K6: with the note", "cut by an infrastructure failure", log[1]["prompt"])
    first = entry(MALFORMED, session="sess-none")
    first["json"]["num_turns"] = None
    stop, result, log, p, _ = retry_of(first)
    check_eq("K6: an unknown number of turns counts as one: fresh", resumed(log), None)
    stop, result, log, p, _ = retry_of(entry(MALFORMED, turns=5, session=""))
    check_eq("K6: many turns and no session id: fresh", resumed(log), None)
    stop, result, log, p, _ = retry_of(entry(MALFORMED, turns=1, session="sess-lost"), resume="sess-orig")
    check_eq("K6: a handoff-repair call that failed at one turn is retried on the ORIGINAL session", resumed(log), "sess-orig")
    check_eq("K6: with the caller's own prompt", log[1]["prompt"], p)
    stop, result, log, p, _ = retry_of(entry(MALFORMED, turns=9, session="sess-more"), resume="sess-orig")
    check_eq("K6: the same call that did work is retried on the session that worked", resumed(log), "sess-more")

    # a resume the DRIVER chose, and the session is gone: one fresh attempt, then the result as it is
    lost = entry("No conversation found with session ID: sess-prior", turns=1, session="sess-x")
    root, task_root, env, driver, delays = project_of(control([lost]))
    try:
        driver.state["interrupted"]["S1-qa-scout-1"] = {"kind": "limit", "rule": "usage_limit", "session_id": "sess-prior",
                                                        "num_turns": 15, "worked": True, "call": "role"}
        p = prompt_for(task_root)
        stop, result = raised(driver, "role", p, role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        log = calls(root)
        check_eq("K6: the first call resumed the recorded session", log[0]["argv"][log[0]["argv"].index("--resume") + 1], "sess-prior")
        check_eq("K6: the lost session is followed by ONE fresh attempt", (len(log), "--resume" in log[1]["argv"]), (2, False))
        check_in("K6: with the original prompt", "Dispatch: S1-qa-scout-1.", log[1]["prompt"])
        check_in("K6: and the note", "cut by an infrastructure failure", log[1]["prompt"])
        check_eq("K6: which succeeded, and the record is cleared", (stop, result["is_error"], driver.state["interrupted"]), (None, False, {}))
    finally:
        done(root)
    root, task_root, env, driver, delays = project_of(control([lost, dict(lost)]))
    try:
        driver.state["interrupted"]["S1-qa-scout-1"] = {"kind": "limit", "rule": "usage_limit", "session_id": "sess-prior",
                                                        "num_turns": 15, "worked": True, "call": "role"}
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K6: when the fresh attempt fails as well the result comes back as any failure does",
                 (stop, result["is_error"], len(calls(root))), (None, True, 2))
        check_eq("K6: as unclassified", result["infra"]["kind"], "unclassified")
    finally:
        done(root)

    # the boundary of `worked` on the write side
    for turns, session, expected in ((1, "s", False), (2, "s", True), (None, "s", False), (5, "", False)):
        one = entry(AUTH, turns=1, session=session)
        one["json"]["num_turns"] = turns
        root, task_root, env, driver, delays = project_of(control([one]))
        try:
            raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
            check_eq(f"K6: an interrupted call of {turns} turns and session {session!r} is worked={expected}",
                     driver.state["interrupted"]["S1-qa-scout-1"]["worked"], expected)
        finally:
            done(root)


# --- K8 -------------------------------------------------------------------------------------------
def k8_a_result_saved_before_this_change():
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control())
        started = harness.run_script("story_step.py", "start", "--task", TASK, "--stage", "S1", "--role", "qa-scout",
                                     cwd=root, env=dict(env, QA_FACTORY_RUN_MODE="driver"))
        check_eq("K8: the dispatch is registered", started.returncode, 0)
        for rel, content in FILES.items():
            path = task_root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        saved = task_root / "state/driver-runs/S1-qa-scout-1.json"
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text(json.dumps(S3_SAVED), encoding="utf-8")
        check("K8: no `interrupted` key in the state, as an older driver left it",
              "interrupted" not in state_of(task_root))
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "1")
        T.eq("K8: the driver goes on and finishes the stage", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        aside = task_root / "state/driver-runs/S1-qa-scout-1.infra.json"
        check("K8: the infrastructure result is set aside as .infra.json", aside.is_file())
        check_eq("K8: unchanged", json.loads(aside.read_text(encoding="utf-8")), S3_SAVED)
        log = calls(root)
        argv = log[0]["argv"]
        check_eq("K8: its session is resumed", argv[argv.index("--resume") + 1], S3_SAVED["session_id"])
        check_in("K8: with the note", "cut by an infrastructure failure", log[0]["prompt"])
        conductor = (task_root / "state/conductor.jsonl")
        check("K8: no conductor row mentions the API error",
              not conductor.exists() or "API Error" not in conductor.read_text(encoding="utf-8"))
        check_eq("K8: no question", (task_root / "state/driver-question.md").exists(), False)
        check_eq("K8: S1 is done", json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))["stages"]["S1"]["status"], "done")
    finally:
        done(root)


# --- K9, K10, K11, K15 ----------------------------------------------------------------------------
def k9_the_conductor_meets_auth():
    import story_run
    root, task_root, env, driver, delays = project_of(control([entry(AUTH)]))
    try:
        def unknown():
            raise story_run.Refusal("controller: the moon is down and nobody knows why")
        driver.where = unknown
        code = driver.run()
        check_eq("K9: a conductor call that meets auth ends the run with 5", code, 5)
        check("K9: no question file", not (task_root / "state/driver-question.md").exists())
        check("K9: no conductor row", not (task_root / "state/conductor.jsonl").exists())
        check_eq("K9: the conductor call is not remembered as an interrupted dispatch", driver.state["interrupted"], {})
    finally:
        done(root)


def k10_the_tracker_meets_auth():
    """t-267 C4 / t-278: the tracker is read by REST and not through the tracker agent (D-06), so the lost login S0 can meet
    is the adapter's exit 5 (a 401, a 403 or a login page that a re-read confirms). C1-3 F3 (a): it is the `ticket_auth` QUESTION (exit
    3: the person can renew the token, paste the ticket or say it is not needed; the variable stands in the answer block), never the
    `ticket_read` question and no longer an infrastructure stop - the exit-5 `InfraStop` of THIS file belongs to `claude -p` alone."""
    import story_run
    root, task_root, env, driver, delays = project_of(control())
    try:
        driver.config.setdefault("adapters", {})["ticket"] = {"kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": {
            "base_url": "https://jira.example.test", "auth_type": "basic_token", "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN"}}
        driver.py_stdout = lambda *a, **k: (5, "", "ticket_adapter: Jira stopped accepting the token (HTTP 401 while reading the ticket QA-1)")
        try:
            driver.s0_rest_read()
            said = "returned"
        except story_run.InfraStop as stop:
            said = "InfraStop:" + stop.kind
        except story_run.Person as person:
            said = "Person:" + person.kind
        # F3 (a) (C1-3 node B): the tracker's lost login is the `ticket_auth` QUESTION (exit 3), not `claude -p`'s infrastructure (exit 5)
        check_eq("K10: the adapter's exit 5 is the `ticket_auth` halt question (the person can renew, paste or say not needed), not a stop",
                 said, "Person:halt")
        check_eq("K10: its block is `ticket_auth`", driver.state.get("s0_block"), "ticket_auth")
    finally:
        done(root)
    # the whole S0, as a process against a Jira that refuses the token: the launch flags come back in the command
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    hits = []

    class Refuses(BaseHTTPRequestHandler):
        def do_GET(self):
            hits.append(self.path)
            self.send_response(401)
            self.end_headers()

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Refuses)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    direct = {"base_url": f"http://127.0.0.1:{server.server_address[1]}", "api_version": "2", "auth_type": "basic_token",
              "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN"}
    root, task_root, env = T.s0_project("QA-1", config={"adapters": {"ticket": {
        "kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": direct}}})
    env.update(QA_JIRA_EMAIL="reader@example.invalid", QA_JIRA_API_TOKEN="test-only-token")
    try:
        out = T.run_driver(root, env, "--task", "QA-1", "--max-boundaries", "0", "--mr", "12", "--branch-suffix", "my suffix",
                           "--env", "local", "--ungrounded")
        T.eq("K10: S0 asks the `ticket_auth` question: exit 3, not the infrastructure stop 5", out.returncode, 3, out.stdout[-1500:] + out.stderr[-800:])
        ask = T.s0_question(task_root)
        for flag in ('--mr 12', '--branch-suffix "my suffix"', "--env local", "--ungrounded"):
            check_not_in(f"K10: no flag is repeated for the person to retype ({flag})", flag, ask)
        check("K10: the answer block exists (the body is what stands above the rule line)", "\n---\n" in ask)
        check_in("K10: the token variable the config names stands in the answer block (the one place an instruction may)", "QA_JIRA_API_TOKEN",
                 ask.split("\n---\n", 1)[-1])
        check_not_in("K10: and not in the body", "QA_JIRA_API_TOKEN", ask.split("\n---\n")[0])
        check_eq("K10: the block is `ticket_auth`, not `ticket_read`, and no agent or conductor was called",
                 (T.s0_state(task_root).get("s0_block"), (root / "stub-log.jsonl").exists()), ("ticket_auth", False))
        check("K10: its answers are priced option lines: `retry`, `not needed`, the ticket as text, `stop`",
              all(word in ask for word in ("`retry` — ", "`not needed` — ", "paste the ticket here as text", "`stop` — ")), ask)
        check("K10: nothing was written for the story: no snapshot, no pipeline", not (task_root / "work/ticket-snapshot.json").exists()
              and not (task_root / "pipeline.json").exists())
        check("K10 (control for the next run): with the variable SET the tracker was asked", len(hits) > 0, str(hits))
    finally:
        harness.cleanup(root)
    # t-287 item 3: the same S0, the variable that holds the token NOT SET in the shell and everything else fine. It is the
    # login's stop as well - the door names THE VARIABLE, there is no "network or VPN" sentence, no `ticket_read` question -
    # and not one request reaches the tracker (the server above counted the first run's and sees none from this one).
    hits.clear()
    root, task_root, env = T.s0_project("QA-1", config={"adapters": {"ticket": {
        "kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": direct}}})
    env.update(QA_JIRA_EMAIL="reader@example.invalid")
    env.pop("QA_JIRA_API_TOKEN", None)
    try:
        out = T.run_driver(root, env, "--task", "QA-1", "--max-boundaries", "0", "--mr", "12", "--branch-suffix", "my suffix",
                           "--env", "local", "--ungrounded")
        T.eq("K10 (item 3): a token variable the shell lacks: the same `ticket_auth` question (exit 3)", out.returncode, 3, out.stdout[-1500:] + out.stderr[-800:])
        ask = T.s0_question(task_root)
        details = (task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8")
        check_eq("K10 (item 3): it is the `ticket_auth` block, no agent called", (T.s0_state(task_root).get("s0_block"), (root / "stub-log.jsonl").exists()),
                 ("ticket_auth", False))
        check("K10 (item 3): the question names the VARIABLE - in the answer block and in the adapter's own sentence beside it - and never a value",
              ask.count("QA_JIRA_API_TOKEN") + details.count("QA_JIRA_API_TOKEN") >= 2 and "reader@example.invalid" not in ask + details
              and "test-only-token" not in ask + details, ask[-900:] + details[-400:])
        check("K10 (item 3): and says the shell lacks it (in the factory's own words): no 'network or VPN' advice, no `ticket_read` question",
              "VPN" not in ask and "not set in this shell" in details, details[-500:])
        T.eq("K10 (item 3): not one request reached the tracker (the first run's control counted them)", hits, [])
        check("K10 (item 3): nothing was written for the story", not (task_root / "work/ticket-snapshot.json").exists() and not (task_root / "pipeline.json").exists())
    finally:
        server.shutdown()
        server.server_close()
        harness.cleanup(root)


def k10b_the_tracker_is_behind_a_protection_page():
    """B-408 (AK5): the whole S0 as a process against a tracker whose address answers 403 with a protection layer's HTML
    page (Cloudflare headers, a title) to every request - the answer a colleague's machine met on 06.10.2026 and the
    driver turned into "renew the token". It is the `ticket_read` question (exit 3), never `InfraStop:auth` (exit 5):
    the body asserts no author and no token claim, the title and the check command stand in the answer block only,
    and the token's value is nowhere."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import http_client

    page = (b"<!DOCTYPE html><html><head><title>Attention Required! | Cloudflare</title></head>"
            b"<body>Sorry, you have been blocked</body></html>")
    hits = []

    class Blocks(BaseHTTPRequestHandler):
        def do_GET(self):
            hits.append((self.path, self.headers.get("User-Agent", "")))
            self.send_response(403)
            self.send_header("Server", "cloudflare")
            self.send_header("CF-RAY", "8a1b2c3d4e5f-AMS")
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Blocks)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    direct = {"base_url": base, "api_version": "2", "auth_type": "basic_token",
              "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN"}
    root, task_root, env = T.s0_project("QA-1", config={"adapters": {"ticket": {
        "kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": direct}}})
    env.update(QA_JIRA_EMAIL="reader@example.invalid", QA_JIRA_API_TOKEN="test-only-token")
    env["no_proxy"] = env["NO_PROXY"] = "127.0.0.1,localhost"
    try:
        out = T.run_driver(root, env, "--task", "QA-1", "--max-boundaries", "0", "--ungrounded", "--env", "local")
        T.eq("K10b: S0 asks the `ticket_read` question (exit 3), it does not stop as a lost login (exit 5)", out.returncode, 3,
             out.stdout[-1500:] + out.stderr[-800:])
        ask = T.s0_question(task_root)
        body, _, block = ask.partition("\n---\n")
        T.eq("K10b: the block is `ticket_read`", T.s0_state(task_root).get("s0_block"), "ticket_read")
        check_in("K10b: the body is the critic's `tried` text: something between this machine and the tracker answered, or the "
                 "answer could not be read, and the token was not checked",
                 "the answer did not come from the tracker in a form I can read: something between this machine and the tracker "
                 "(a firewall, a proxy or a protection service) answered instead, or the answer could not be read. I could not "
                 "check whether the account's token works.", body)
        check_in("K10b: ... and the `fix` text: check the address from this machine, outside the factory, with the command below",
                 "check the tracker's address from this machine, outside the factory, with the command below", body)
        check("K10b: the body carries neither the title nor any claim about the token",
              "Attention Required" not in body and "Cloudflare" not in body and "renew" not in body.lower()
              and "stopped accepting" not in body, body)
        check_in("K10b: the answer block holds what answered, in the factory's own words, with the title",
                 "What answered, in the factory's own words:", block)
        check_in("K10b: ... the title", "Attention Required! | Cloudflare", block)
        check_in("K10b: ... and the check, a GET to the tracker's own address with no credential",
                 "Check: " + http_client.curl_line(base + "/rest/api/2/serverInfo"), block)
        check("K10b: no token value or user anywhere in the question", "test-only-token" not in ask and "reader@example.invalid" not in ask)
        T.eq("K10b: the rules of the text a person reads hold", T.rules_broken(ask), [])
        check("K10b: the factory's User-Agent reached the server, never urllib's",
              bool(hits) and all(ua.startswith("qa-factory/") for _path, ua in hits), str(hits))
        check("K10b: nothing was written for the story, and no agent was called", not (task_root / "pipeline.json").exists()
              and not (task_root / "work/ticket-snapshot.json").exists() and not (root / "stub-log.jsonl").exists())
    finally:
        server.shutdown()
        server.server_close()
        harness.cleanup(root)


def k11_unclassified_is_todays_path():
    root, task_root, env, driver, delays = project_of(control([entry("boom: something nobody has met", turns=4, session="sess-u")]))
    try:
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K11: no stop", stop, None)
        check_eq("K11: the caller gets the failure as before, and the classification with it",
                 (result["is_error"], result["result"], result["infra"]["kind"]), (True, "boom: something nobody has met", "unclassified"))
        check_eq("K11: the session is stored as before", driver.state["sessions"]["S1-qa-scout-1"], "sess-u")
        row = T.jsonl(task_root / "state/driver-runs.jsonl")[0]
        check_eq("K11: the journal says unclassified", (row["infra"], row["infra_rule"], row["retry"]), ("unclassified", "", 0))
        check_eq("K11: nothing was retried", (delays, len(calls(root))), ([], 1))
    finally:
        done(root)
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control([entry("boom: something nobody has met", turns=4, session="sess-u")],
                              conductor={"action": "ask_person", "question": "Which stand should I use?", "did": "read"}))
        # t-261 (K11, critic t-244): two boundaries, not one. The first boundary's refusal is answered by the role's own
        # resume (t-217 §1: once per finding set); the SECOND is the person's - and the road is the person's own (the seam's since C1-5d2, below), not the
        # conductor's: the conductor stub above (`ask_person`) is never called. (The old pin of one boundary proved the
        # conductor road; since t-217 a second identical refusal is a fact the factory already knows - fork 3.)
        # t-828 (re-pinned to conductor/1 C1-5d2, t-698 sec. 12.2.1/12.2.2, sec. 13 F-d1): the refusal that survives the resume
        # limit is asked by the ONE seam `exit_limit` - the site's own question (kind `exit_limit`, key `exit.resume_limit`,
        # stage and dispatch as its fields), `call=False`: still no conductor call.
        out = T.run_driver(root, env, "--task", TASK, "--max-boundaries", "2")
        check_eq("K11: an unclassified failure still reaches the person (exit 3)", out.returncode, 3)
        asked = json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8")).get("asked") or {}
        check_eq("K11: and the question is of kind `exit_limit` (the seam's road after the t-217 resume, not the conductor's)",
                 asked.get("kind"), "exit_limit")
        check_eq("K11: about the stage and the dispatch of the refused role (the seam's fields)",
                 (asked.get("stage"), asked.get("dispatch")), ("S1", "S1-qa-scout-1"))
        check_eq("K11: the conductor stub was not called at all (its calls are in the stub's own log)", T.d2_conductor_calls(root), [])
    finally:
        done(root)


def k11_what_is_not_a_failure_is_never_read():
    root, task_root, env, driver, delays = project_of(control())
    try:
        ok_words = {"json": {"type": "result", "subtype": "success", "is_error": False, "session_id": "sess-ok", "num_turns": 3,
                             "total_cost_usd": 0.1, "duration_ms": 5, "result": "The role quoted: " + AUTH}, "exit": 0}
        install(root, control([ok_words, {"json": {"type": "result", "subtype": "success", "is_error": False, "session_id": "sess-e",
                                                   "num_turns": 1, "total_cost_usd": 0, "duration_ms": 5, "result": ""}, "exit": 0}]))
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K11: a successful call that quotes a login error is the role's result", (stop, result["result"].startswith("The role quoted")), (None, True))
        check_eq("K11: and the journal says null", T.jsonl(task_root / "state/driver-runs.jsonl")[-1]["infra"], None)
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K11: an empty successful result keeps today's path (F-9)", (stop, result["result"], result["is_error"]), (None, "", False))
        check_eq("K11: nothing was slept", delays, [])
    finally:
        done(root)


def k11_unparsable_and_stderr_only_output():
    root, task_root, env, driver, delays = project_of(control([{"raw": AUTH, "exit": 1}, {"json": {"type": "result", "is_error": True, "session_id": "s", "num_turns": 1, "result": ""}, "exit": 1, "stderr": AUTH}]))
    try:
        stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("K11: text that is not JSON takes the fallback dict and is classified", infra_of(stop), "auth")
        stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-2", stage="S1")
        check_eq("K11: an empty result with the login error on stderr is auth too", infra_of(stop), "auth")
    finally:
        done(root)


def k15_a_retry_is_not_a_conductor_call():
    root, task_root, env, driver, delays = project_of(control([entry(MALFORMED, turns=1)]))
    try:
        driver.boundary = "S1:S1-qa-scout-1"
        verdict = driver.conductor("controller: the moon is down and nobody knows why")
        check_eq("K15: the conductor's own answer comes back after the retry", verdict.get("action"), "continue")
        check_eq("K15: one call counted for the boundary, not two", driver.conductor_calls, {"S1:S1-qa-scout-1": 1})
        check_eq("K15: the wait was taken once", delays, [5])
        check_eq("K15: two claude calls made", len(calls(root)), 2)
    finally:
        done(root)


# --- K12, K13 -------------------------------------------------------------------------------------
def k12_the_claude_child_environment():
    host = {"ANTHROPIC_BASE_URL": "http://127.0.0.1:4001", "ANTHROPIC_AUTH_TOKEN": "tok", "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST": "1",
            "CLAUDE_CODE_USE_BEDROCK": "1", "CLAUDE_CODE_HOST_AUTH_ENV_VAR": "MY_TOK", "MY_TOK": "secret",
            "ANTHROPIC_API_KEY": "key-1", "PYTHONIOENCODING": "cp1252", "FOO": "foo"}
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control())
        for key in ("PYTHONUTF8",):
            env.pop(key, None)
        out = T.run_driver(root, env | host, "--task", TASK, "--max-boundaries", "1")
        T.eq("K12: the story runs", out.returncode, 0, out.stdout[-1000:] + out.stderr[-500:])
        seen = calls(root)[0]["env"]
        for name in ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST", "CLAUDE_CODE_USE_BEDROCK",
                     "CLAUDE_CODE_HOST_AUTH_ENV_VAR", "MY_TOK"):
            check_eq(f"K12: the claude child does not see {name}", seen[name], None)
        check_eq("K12: an API key stays", seen["ANTHROPIC_API_KEY"], "key-1")
        check_eq("K12: UTF-8 mode", seen["PYTHONUTF8"], "1")
        check_eq("K12: and the encoding is the driver's, not the host's", seen["PYTHONIOENCODING"], "utf-8")
        check_eq("K12: an unrelated variable stays", seen["FOO"], "foo")
    finally:
        done(root)

    # the project's doors: keep passes a host variable through, remove adds a name
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control())
        cfg_path = root / "qa-factory" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["driver"] = {"child_env": {"keep": ["ANTHROPIC_BASE_URL"], "remove": ["FOO", "ANTHROPIC_BASE_URL"]}}
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        out = T.run_driver(root, env | host, "--task", TASK, "--max-boundaries", "1")
        T.eq("K12: the story runs with a keep and a remove", out.returncode, 0, out.stdout[-1000:])
        seen = calls(root)[0]["env"]
        check_eq("K12: keep [ANTHROPIC_BASE_URL] is present in the child", seen["ANTHROPIC_BASE_URL"], "http://127.0.0.1:4001")
        check_eq("K12: remove [FOO] is gone", seen["FOO"], None)
        check_in("K12: a name in both keep and remove is kept, with a note", "`ANTHROPIC_BASE_URL` is in both keep and remove", out.stdout)
        check_eq("K12: the token is still removed: only the kept name is passed", seen["ANTHROPIC_AUTH_TOKEN"], None)
    finally:
        done(root)

    # the driver's own object: py() children keep the host's proxy and get UTF-8
    root, task_root, env, driver, delays = project_of(control())
    try:
        driver.env["ANTHROPIC_BASE_URL"] = "http://127.0.0.1:4001"
        check_eq("K12: a py() child keeps the host's BASE_URL (factory scripts may use a gateway on purpose)",
                 driver.env.get("ANTHROPIC_BASE_URL"), "http://127.0.0.1:4001")
        check_eq("K12: and has UTF-8", (driver.env.get("PYTHONUTF8"), driver.env.get("PYTHONIOENCODING")), ("1", "utf-8"))
        check_eq("K12: the object names what it removed from the claude child", isinstance(driver.env_removed, list), True)
    finally:
        done(root)


def k12_child_env_function():
    import infra_failure as I
    rules, _ = I.rules()
    base = {"ANTHROPIC_BASE_URL": "u", "CLAUDE_CODE_USE_VERTEX": "1", "CLAUDE_CODE_MESSAGING_TOKEN": "m", "CLAUDE_CODE_HOST_AUTH_ENV_VAR": "MY_TOK",
            "MY_TOK": "s", "ANTHROPIC_API_KEY": "k", "PATH": "p", "FOO": "f"}
    env, removed, notes = I.child_env(base, rules, {})
    check_eq("K12: the data list, the prefixes and the named variable go", sorted(removed),
             ["ANTHROPIC_BASE_URL", "CLAUDE_CODE_HOST_AUTH_ENV_VAR", "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_USE_VERTEX", "MY_TOK"])
    check_eq("K12: what stays", sorted(env), ["ANTHROPIC_API_KEY", "FOO", "PATH"])
    check_eq("K12: removed_present lists only names that were there", "ANTHROPIC_AUTH_TOKEN" in removed, False)
    env, removed, notes = I.child_env(base, rules, {"child_env": {"keep": ["ANTHROPIC_BASE_URL", "MY_TOK"], "remove": ["FOO"]}})
    check_eq("K12: keep beats the data list, remove adds", ("ANTHROPIC_BASE_URL" in env, "MY_TOK" in env, "FOO" in env), (True, True, False))
    env, removed, notes = I.child_env(base, rules, {"child_env": {"keep": ["FOO"], "remove": ["FOO"]}})
    check_eq("K12: a name in keep and in the config's remove is kept", "FOO" in env, True)
    check_in("K12: and says so", "`FOO` is in both keep and remove; it is kept", notes)
    env, removed, notes = I.child_env(base, rules, {"child_env": {"keep": "ANTHROPIC_BASE_URL", "remove": [1, 2]}})
    check_eq("K12: a keep or remove that is not a list of names is ignored", ("ANTHROPIC_BASE_URL" in env, "FOO" in env), (False, True))
    check_eq("K12: with one note each", sum("ignored" in n for n in notes), 2)
    env, removed, notes = I.child_env(base, {}, {})
    check_eq("K12: with no rules nothing is removed", (env, removed, notes), (base, [], []))
    check_eq("K12: the base dict is not touched", "ANTHROPIC_BASE_URL" in base, True)


def k13_a_child_prints_in_utf8():
    root, task_root, env, driver, delays = project_of(control())
    try:
        script = root / "dash.py"
        script.write_text("import sys\nprint(chr(0x2014) + chr(0x2026))\n", encoding="utf-8")
        code, out = driver.py(str(script))
        check_eq("K13: a child that prints an em dash and an ellipsis is decoded as such", (code, out), (0, chr(0x2014) + chr(0x2026)))
    finally:
        done(root)


# --- K14 ------------------------------------------------------------------------------------------
def k14_the_texts_obey_the_human_rules():
    import human_text
    for label, text, turns, queue_size in (("auth", AUTH, 1, 1), ("limit", LIMIT, 15, 1), ("limit without a reset", LIMIT_NO_RESET, 3, 1),
                                           ("transient", MALFORMED, 1, 3)):
        root, task_root, env, driver, delays = project_of(control([entry(text, turns=turns, session=f"s{i}") for i in range(queue_size)]))
        try:
            stop, _ = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
            message = stop.reason if stop else ""
            check_eq(f"K14: the {label} message breaks no rule of human-questions", human_text.problems(message), [])
            check_in(f"K14: the {label} message ends in a how-to-answer block that gives the command", "## How to answer\nNothing to answer:", message)
            body = message.split("\n## How to answer")[0]
            for shape in ("story_run", ".py", "exit 5", "S1-qa-scout-1", "--"):
                check_not_in(f"K14: the {label} body carries no `{shape}`", shape, body)
            check_in(f"K14: the {label} body says nothing about the story is wrong or lost", "nothing", body.lower())
            if label == "auth":
                check_in("K14: auth lists what was taken from the child and the door to keep it", "driver.child_env.keep", message)
        finally:
            done(root)


# --- the command, the note, the flags, the conflicts ------------------------------------------------
def command_and_flags():
    root, task_root, env, driver, delays = project_of(control())
    try:
        base = f'python "{driver.scripts / "story_run.py"}" --task {TASK} --project "{driver.project}"'
        driver.flags.max_boundaries = 80      # driver_for's own default is 10, which IS a non-default
        check_eq("cmd: the default command is the task and the project only", driver.continue_command(), base)
        f = driver.flags
        f.plugin_dir, f.model, f.until, f.mr, f.branch, f.commit = "C:/a b/plugin", "opus", "gate_A", "12", "br x", "abc"
        f.ungrounded, f.ticket_file, f.env, f.branch_suffix, f.max_boundaries, f.no_trace = True, "t k.md", "local", "s 1", "3", True
        got = driver.continue_command()
        for part in ('--plugin-dir "C:/a b/plugin"', "--model opus", "--until gate_A", "--mr 12", '--branch "br x"', "--commit abc",
                     "--ungrounded", '--ticket-file "t k.md"', "--env local", '--branch-suffix "s 1"', "--max-boundaries 3", "--no-trace"):
            check_in(f"cmd: every non-default flag is repeated: {part}", part, got)
        f.model, f.until, f.max_boundaries = "sonnet", "end", 80
        check_not_in("cmd: the defaults are not", "--model", driver.continue_command())
        check_not_in("cmd: max-boundaries 80 is not", "--max-boundaries", driver.continue_command())
        f.answer = str(root / "answer.md")
        driver.state["asked"] = {}
        check_not_in("cmd: an answer already taken is not offered again", "--answer", driver.continue_command())
        driver.state["asked"] = {"kind": "halt", "stage": "S1", "dispatch": "S1-qa-scout-1"}
        check_in("cmd: during take_answer (the question still open) the answer file is repeated", "--answer", driver.continue_command())
        f.answer = None
        check_not_in("cmd: an open question with no answer file given is not", "--answer", driver.continue_command())
    finally:
        done(root)


def k9b_a_stop_during_take_answer_repeats_the_answer():
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control([entry(AUTH)]))
        (task_root / "state").mkdir(parents=True, exist_ok=True)
        (task_root / "state/driver-question.md").write_text("# Driver question\nkind: halt\nstage: S1\ndispatch: S1-qa-scout-1\n\nQuestion?\n", encoding="utf-8")
        (task_root / "state/driver-state.json").write_text(json.dumps({"asked": {"kind": "halt", "stage": "S1", "dispatch": "S1-qa-scout-1"}}), encoding="utf-8")
        answer = root / "answer.md"
        answer.write_text("go on please", encoding="utf-8")
        out = T.run_driver(root, env, "--task", TASK, "--answer", str(answer), "--max-boundaries", "1")
        T.eq("take_answer: a conductor call that meets auth while the answer is taken stops with 5", out.returncode, 5, out.stdout[-1200:] + out.stderr[-500:])
        check_in("take_answer: and the command carries the answer file", f"--answer {answer}", out.stdout)
    finally:
        done(root)


def the_continuation_note():
    root, task_root, env, driver, delays = project_of(control())
    try:
        check_eq("note: no outputs and no record: no note for a fresh role call",
                 driver.continuation_note("role", "qa-scout", "S1", "S1-qa-scout-1", alone=False, known=False), "")
        generic = driver.continuation_note("conductor", "", "S1", "", alone=True, known=True)
        check_in("note: a call that is not a role's gets the generic note", "cut by an infrastructure failure, not by anything you did", generic)
        check_not_in("note: without a list of outputs", "Continue them", generic)
        for rel, content in FILES.items():
            (task_root / rel).parent.mkdir(parents=True, exist_ok=True)
            (task_root / rel).write_text(content, encoding="utf-8")
        form = task_root / "work/handoffs/S1-qa-scout-1.yaml"
        form.parent.mkdir(parents=True, exist_ok=True)
        form.write_text("header: {}\n", encoding="utf-8")
        note = driver.continuation_note("role", "qa-scout", "S1", "S1-qa-scout-1", alone=True, known=True)
        check_in("note: it says it is the same dispatch with the same inputs", "same dispatch with the same inputs", note)
        check_in("note: it lists the role's own outputs with their size", f"work/context-manifest.json ({len(FILES['work/context-manifest.json'].encode())} bytes)", note)
        check_not_in("note: and not what code writes (the bundle)", "context-bundle.json (", note)
        check_in("note: and the handover form", "work/handoffs/S1-qa-scout-1.yaml", note)
        check_in("note: it names the doors of a role that has Bash", "artifact_supersede.py", note)
        check_in("note: and the plan check", "planning_contract.py --kind plan", note)
        check_in("note: and ends in the handoff form", "· ok|concerns|halt|impossible", note)
        (task_root / "work/test-plan.json").write_text(json.dumps({"rows": [{"id": "TS-1"}]}), encoding="utf-8")
        strategist = driver.continuation_note("role", "qa-test-strategist", "S3", "S3-qa-test-strategist-1", alone=True, known=True)
        check_in("note: the strategist's plan is listed", "work/test-plan.json (", strategist)
        check_not_in("note: a role with no Bash is not sent to a script it cannot run (FR-2)", "artifact_supersede.py", strategist)
        check_in("note: it is sent to the point editor instead", "Edit", strategist)
        (task_root / "work/test-cases").mkdir(parents=True, exist_ok=True)
        (task_root / "work/test-cases/TC-1.md").write_text("x", encoding="utf-8")
        (task_root / "work/test-cases/TC-2.md").write_text("y", encoding="utf-8")
        designer = driver.continuation_note("role", "qa-case-designer", "S4", "S4-qa-case-designer-1", alone=True, known=True)
        check_in("note: a directory is its file count", "work/test-cases/ (2 files)", designer)
        (driver.project / "bugs").mkdir(exist_ok=True)
        (driver.project / "bugs/b1.md").write_text("z", encoding="utf-8")
        reporter = driver.continuation_note("role", "qa-bug-reporter", "S8", "S8-qa-bug-reporter-1", alone=True, known=True)
        check_in("note: `project:` resolves against the project root", "project:bugs/ (1 file)", reporter)
    finally:
        done(root)


def conflicts():
    root, task_root, env, driver, delays = project_of(control())
    try:
        driver.state["interrupted"]["S1-qa-scout-1"] = {"kind": "limit", "rule": "usage_limit", "session_id": "sess-prior",
                                                        "num_turns": 15, "worked": True, "call": "role"}
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1",
                              resume="sess-explicit")
        first = calls(root)[0]
        check_eq("conflict: an explicit resume wins over the interrupted record",
                 first["argv"][first["argv"].index("--resume") + 1], "sess-explicit")
        check_in("conflict: and the note is appended to the caller's prompt", "cut by an infrastructure failure", first["prompt"])
        check_in("conflict: after the caller's own words", "Do the work.", first["prompt"])
    finally:
        done(root)

    root, task_root, env, driver, delays = project_of(control())
    try:
        started = harness.run_script("story_step.py", "start", "--task", TASK, "--stage", "S1", "--role", "qa-scout", cwd=root,
                                     env=dict(env, QA_FACTORY_RUN_MODE="driver"))
        check_eq("conflict: a dispatch to hold both", started.returncode, 0)
        seen = []
        driver.resume_role = lambda *a, **k: seen.append("resume_role")
        driver.run_role = lambda *a, **k: seen.append("run_role")
        driver.handoff = lambda *a, **k: seen.append("handoff") or "digest"
        driver.finish = lambda *a, **k: seen.append("finish")
        driver.state["interrupted"]["S1-qa-scout-1"] = {"kind": "limit", "worked": True, "session_id": "s", "call": "role"}
        driver.state["pending_words"]["S1-qa-scout-1"] = "the person's words"
        driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": "S1-qa-scout-1"})
        check_eq("conflict: the person's words win over an interrupted record", seen, ["resume_role"])
        driver.state["pending_words"].pop("S1-qa-scout-1")
        saved = task_root / "state/driver-runs/S1-qa-scout-1.json"
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text(json.dumps({"session_id": "s1", "result": DIGEST, "num_turns": 3, "is_error": False, "exit_code": 0, "stderr": ""}), encoding="utf-8")
        seen.clear()
        driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": "S1-qa-scout-1"})
        check_eq("conflict: a valid saved result wins over an interrupted record", seen, ["handoff", "finish"])
        check("conflict: and the saved result is not set aside", saved.is_file() and not saved.with_name("S1-qa-scout-1.infra.json").exists())
        seen.clear()
        saved.write_text(json.dumps(dict(S3_SAVED)), encoding="utf-8")
        driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": "S1-qa-scout-1"})
        check_eq("conflict: an infrastructure result saved beside a record is set aside and the dispatch continues", seen, ["run_role"])
        check("conflict: as .infra.json", saved.with_name("S1-qa-scout-1.infra.json").is_file() and not saved.exists())
    finally:
        done(root)


def the_data_file_absent_is_one_note():
    import hooklib
    real = hooklib.load_ref_json
    hooklib.load_ref_json = lambda name: {} if name == "driver-infra.json" else real(name)
    root, task_root, env = T.seed(TASK)
    try:
        install(root, control([entry(AUTH)]))
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            driver = T.driver_for(root, env, TASK)
        check_eq("temporal: one printed note that the failures are not recognised", buffer.getvalue().count("infrastructure failures not recognised"), 1)
        driver.sleep = lambda s: None
        check_eq("temporal: the environment is the host's plus UTF-8, nothing removed", (driver.env_removed, driver.claude_env == driver.env), ([], True))
        check_eq("temporal: an old state file gets the key", driver.state.get("interrupted"), {})
        stop, result = raised(driver, "role", prompt_for(task_root), role="qa-scout", dispatch="S1-qa-scout-1", stage="S1")
        check_eq("temporal: a login failure is then today's failure, unclassified", (stop, result["infra"]["kind"]), (None, "unclassified"))
        check_eq("temporal: and journalled as such", T.jsonl(task_root / "state/driver-runs.jsonl")[0]["infra"], "unclassified")
    finally:
        hooklib.load_ref_json = real
        done(root)


def delivery_carries_its_key():
    root, task_root, env, driver, delays = project_of(control([entry(LIMIT, turns=6, session="sess-deliv")]))
    try:
        stop, _ = raised(driver, "conductor", "deliver it", stage="S8", resume_key="S8:delivery")
        check_eq("delivery: a conductor call with a key is remembered", infra_of(stop), "limit")
        record = driver.state["interrupted"].get("S8:delivery") or {}
        check_eq("delivery: under that key, with its session", (record.get("call"), record.get("session_id"), record.get("worked")),
                 ("conductor", "sess-deliv", True))
        install(root, control())
        stop, result = raised(driver, "conductor", "deliver it", stage="S8", resume_key="S8:delivery")
        second = calls(root)[-1]
        check_eq("delivery: the rerun resumes that session", second["argv"][second["argv"].index("--resume") + 1], "sess-deliv")
        check_not_in("delivery: with the note alone, not the delivery prompt again", "deliver it", second["prompt"])
        check_eq("delivery: and the record is cleared", driver.state["interrupted"], {})
    finally:
        done(root)


def f4_rows_carry_their_hosts():
    """CX1-15 F-4: a `codex_*` row is tried only for a call of its host. A role's text on Claude that says `401 unauthorized` (an
    API test's output) in a FAILED call is not a Codex login failure; the same text on a Codex call is; a caller naming no host
    tries the rows without `hosts` only (the rows there were before the key existed)."""
    import infra_failure as IF
    rules, notes = IF.rules()
    check_eq("F-4: the packaged data loads clean", notes, [])
    codex_rows = {r["id"]: r.get("hosts") for r in rules["failures"] if r["id"].startswith("codex_")}
    check_eq("F-4: the three codex rows are in the data, each for the codex host only", codex_rows,
             {"codex_not_logged_in": ["codex"], "codex_usage_limit": ["codex"], "codex_stream_broken": ["codex"]})
    text = {"is_error": True, "exit_code": 1, "result": "the API test got 401 unauthorized from the stand", "stderr": ""}
    check_eq("F-4: on Claude that text is unclassified", IF.classify(text, rules, "claude"), {"kind": "unclassified", "rule": ""})
    check_eq("F-4: with no host named it is unclassified too (the rows before `hosts`)", IF.classify(text, rules), {"kind": "unclassified", "rule": ""})
    check_eq("F-4: on Codex it is the login failure", (IF.classify(text, rules, "codex") or {}).get("rule"), "codex_not_logged_in")
    check_eq("F-4: a row without `hosts` still reads every host (the Claude login row on Codex)",
             (IF.classify(dict(text, result="Not logged in"), rules, "codex") or {}).get("rule"), "not_logged_in")
    import hooklib
    saved = hooklib.load_ref_json
    try:
        hooklib.load_ref_json = lambda name: {"failures": [dict(rules["failures"][0], id="x", hosts="codex"),
                                                           {"id": "ok", "kind": "auth", "pattern": "z"}]}
        good, bad_notes = IF.rules()
    finally:
        hooklib.load_ref_json = saved
    check_eq("F-4: a `hosts` that is no list is skipped with a note, the other rows still match",
             ([r["id"] for r in good["failures"]], any("`hosts` must be a non-empty list" in n for n in bad_notes)), (["ok"], True))


SCENARIOS = (f4_rows_carry_their_hosts, k1_classify, k2_auth_stops_the_driver, k3_limit_worked_then_continued, k3_a_second_stop_keeps_the_session_that_worked,
             k5_transient_retries_keep_the_recorded_session, k3_a_limit_without_a_reset_says_so,
             k4_transient_then_success, k5_transient_three_times, k5_two_retries_then_success_is_at_the_limit, k6_resume_choice,
             k8_a_result_saved_before_this_change, k9_the_conductor_meets_auth, k9b_a_stop_during_take_answer_repeats_the_answer,
             k10_the_tracker_meets_auth, k10b_the_tracker_is_behind_a_protection_page, k11_unclassified_is_todays_path, k11_what_is_not_a_failure_is_never_read,
             k11_unparsable_and_stderr_only_output, k15_a_retry_is_not_a_conductor_call, k12_the_claude_child_environment,
             k12_child_env_function, k13_a_child_prints_in_utf8, k14_the_texts_obey_the_human_rules, command_and_flags,
             the_continuation_note, conflicts, the_data_file_absent_is_one_note, delivery_carries_its_key)

# `test_infra_failure.py k2_auth_stops_the_driver k5_transient_three_times` runs only those (a mutation
# control names the one scenario it targets); with no names, all of them run - the witness is that run.
for _fn in SCENARIOS:
    if not sys.argv[1:] or _fn.__name__ in sys.argv[1:]:
        scenario(_fn)

finish("test_infra_failure")
