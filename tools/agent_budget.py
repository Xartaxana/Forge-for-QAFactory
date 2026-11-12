"""agent_budget.py -- PreToolUse hook (all tools): a context-size and test-run budget for a worker
and for the main session (B-462..B-466, t-575). A measurement that reaches the session, never a
verdict on the work: WARN as additionalContext; a worker past the STOP cap is blocked (exit 2) on
every tool except the three moves that close it out.

Hook input keys the harness gives (measured, t-575): session_id, transcript_path (the MAIN session
file), cwd, tool_name, tool_input and -- inside a subagent only -- agent_id (recorded in
.claude/dod_track/*.json: a string for a worker, null for the main thread). The worker's own
transcript is <transcript_path minus .jsonl>/subagents/agent-<agent_id>.jsonl.

Which transcript is measured (t-576 F1, the Lead's decision: the worker is identified ONLY by agent_id):
 A. agent_id is a non-empty string -> that worker's file (exact; a missing file or an unsafe id ->
    silent, never the main one);
 B. no agent_id (absent, null, empty or not a string) -> the MAIN transcript_path, always. A STOP is
    therefore never taken from a call that is not provably a worker's.
Context size at a turn = input_tokens + cache_creation_input_tokens + cache_read_input_tokens of the
last assistant line that carries message.usage. It is read from the tail transcripts.tail_lines gives: the
last 64 KB plus the file's LAST line whole whatever its length (t-840, F6-7), so a long newest line that
carries the usage is measured directly. When the newest line is a long one WITHOUT usage (a 70 KB tool
result), the assistant line before it lies outside the tail: the last usage the incremental scan saw (kept
in the sidecar as `ctx`) is used -- so the context is never unknown for want of a short last line.
Test runs / waits are counted over the whole transcript incrementally: a sidecar
.claude/agent_budget/<stem>.json keeps the byte offset and the counts; an unparsable or mistyped
sidecar, one older than the transcript's creation, or one whose offset is past the end of the file is
rebuilt from scratch.

Reading a transcript (the tail, the usage line, the line split, the layout of a worker's file) is
tools/transcripts.py's job -- the one reader that dispatch_gate, journal_echo and tier_echo share;
context_size and is_finished here are thin delegates to it. Lines are split on "\n" only (JSONL).
If that module EXISTS but does not import (a SyntaxError, an error at import time), this hook fails open
with ONE stderr line naming the cause (it runs on every tool call, a silent off-switch is a leak, t-844);
if it is simply absent (the hook deployed alone in a folder) it fails open silently.
is_finished(path) -- a worker transcript whose last assistant line with tool_use calls
SubagentHandback is finished (measured on 425 real worker files of one session: 415 end that way);
tools/dispatch_gate.py leaves finished transcripts out of its parallel cap (through transcripts.py).

STOP at the cap lets through exactly three moves: SubagentHandback; Write/Edit of a file under
<cwd>/<a folder of ALLOWED_DIRS>/ -- docs/tasks/handoffs, docs/tasks/specs/reports and the report folders of
dispatch_manifest.HANDOFF_DIRS (t-744; the file a reading role may write is further narrowed to the one path
of its dispatch's handoff: line by tools/handoff_gate.py) -- (the real path, cwd = the hook input's
cwd, else the current directory); a Bash/PowerShell command that is ONE plain git command
(add/commit/status/stash/diff --stat) with no shell metacharacter at all (PLAIN_GIT_RE). Quotes are fine.
Note: the character class is a deny-list of the characters that chain, redirect, substitute or escape in
bash AND PowerShell; the SIBLING_MAP axis 11 convergence to hooklib.command_segments is queued (B-434).

Thresholds (module constants, env overrides read per call): AGENT_BUDGET_WORKER_WARN=250000,
AGENT_BUDGET_WORKER_STOP=400000, AGENT_BUDGET_MAIN_WARN=300000, AGENT_BUDGET_MAIN_STEP=50000,
AGENT_BUDGET_TEST_RUNS_WARN=10, AGENT_BUDGET_TEST_RUNS_STEP=5. A WARN repeats only when a NEW step is
crossed (the sidecar remembers the last warned level); a worker's context WARN is given once.
AGENT_BUDGET_DIR moves the sidecar folder (tests).

Fail-open (edge i): any failure -> exit 0, nothing printed; one stderr line only when
AGENT_BUDGET_DEBUG=1. The exception: a transcripts that exists but failed to import prints its one line always."""

import json
import os
import re
import sys
from pathlib import Path

TRANSCRIPTS_OFF = "the budget gate runs without transcripts: the context size is unknown, no WARN/STOP possible"


def _transcripts_import_failed(exc: Exception):
    """transcripts present but broken (SyntaxError, an error at import time, a ModuleNotFoundError of ANOTHER
    module inside it) must not kill this hook (it runs on EVERY tool call) and must not switch the cost gate
    off in silence: ONE stderr line (class + the message squeezed to a line and cut), evaluate() then passes.
    transcripts ITSELF absent (ModuleNotFoundError named transcripts: the hook deployed alone in a folder)
    stays silent -- test_transcripts.test_agent_budget_alone_in_a_folder_exits_zero_and_silent."""
    if isinstance(exc, ModuleNotFoundError) and exc.name == "transcripts":
        return None
    detail = " ".join(str(exc).split())[:40]  # the whole line stays under 200 characters
    print("agent_budget: transcripts did not import (%s: %s); %s" % (type(exc).__name__, detail, TRANSCRIPTS_OFF),
          file=sys.stderr)
    return None


try:
    from tools import transcripts  # package-style
except ImportError:  # absent as a package: the sibling path still gets its try
    try:
        import transcripts  # sibling-module fallback (also what the mechanism net's import walk sees)
    except Exception as _exc:  # absent here too, or present but broken
        transcripts = _transcripts_import_failed(_exc)
except Exception as _exc:  # present as a package but broken
    transcripts = _transcripts_import_failed(_exc)


def _manifest_import_failed(exc: Exception):
    """A dispatch_manifest that EXISTS but does not import (SyntaxError, a runtime error at import) must not kill
    this hook (it runs on EVERY tool call): one stderr line, ALLOWED_DIRS keeps the two report folders."""
    print("agent_budget: tools/dispatch_manifest.py did not import (%s); STOP keeps the two report folders"
          % type(exc).__name__, file=sys.stderr)
    return None


try:
    from tools import dispatch_manifest  # package-style (pure module: HANDOFF_DIRS is data)
except ImportError:  # absent (the plain case: the hook copied alone) -> silent (this module is optional)
    try:
        import dispatch_manifest  # sibling-module fallback
    except ImportError:
        dispatch_manifest = None  # ALLOWED_DIRS then keeps the two report folders it always had
    except Exception as _exc:
        dispatch_manifest = _manifest_import_failed(_exc)
except Exception as _exc:  # present but broken
    dispatch_manifest = _manifest_import_failed(_exc)

WORKER_WARN = 250000
WORKER_STOP = 400000
MAIN_WARN = 300000
MAIN_STEP = 50000
TEST_RUNS_WARN = 10
TEST_RUNS_STEP = 5

TEST_RE = re.compile(r"pytest|selftest\.py|tests[\\/]test_\w+\.py|unittest")
WAIT_RE = re.compile(r"(?:^|[\s;&|(])(?:sleep|until)\b")
PLAIN_GIT_RE = re.compile(r"^\s*git (add|commit|status|stash|diff --stat)\b[^;&|<>`$\\()\r\n]*$")
_REPORT_DIRS = ("docs/tasks/handoffs", "docs/tasks/specs/reports")
# the report folders of every role (dispatch_manifest.HANDOFF_DIRS, t-744 F-3) join the two above, so the
# STOP advice never contradicts tools/handoff_gate.py (a critic's file is in docs/tasks/specs/reviews)
ALLOWED_DIRS = _REPORT_DIRS + tuple(d for d in (dispatch_manifest.HANDOFF_DIRS.values() if dispatch_manifest else ())
                                    if d not in _REPORT_DIRS)
SIDECAR_DIR = Path(__file__).resolve().parents[1] / ".claude" / "agent_budget"
FRESH_STATE = {"offset": 0, "tests": 0, "waits": 0, "ctx": 0, "ctx_level": 0, "tests_level": 0}


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, ""))
    except ValueError:
        return default


def _debug(what: str) -> None:
    if os.environ.get("AGENT_BUDGET_DEBUG") == "1":
        sys.stderr.write("agent_budget: %s\n" % what)


def context_size(path: Path):
    """Tokens in context at the last turn that carries usage; None when no usage line is in the tail."""
    return transcripts.context_size(path)


def is_finished(path: Path) -> bool:
    """True when the last assistant line with tool_use calls SubagentHandback (a worker that handed back)."""
    return transcripts.is_finished(path)


def resolve_transcript(payload: dict):
    """(path, is_worker) per branches A-B of the module docstring; (None, False) when nothing to measure."""
    main_path = payload.get("transcript_path")
    if not isinstance(main_path, str) or not main_path:
        return None, False
    agent_id = payload.get("agent_id")
    if not (isinstance(agent_id, str) and agent_id):
        return Path(main_path), False
    name = transcripts.agent_file_name(agent_id)
    f = transcripts.subagents_dir_of(main_path) / name if name else None
    return (f, True) if f is not None and f.is_file() else (None, False)


def _creation_time(st):
    born = getattr(st, "st_birthtime", None)
    if born is None and os.name == "nt":
        born = st.st_ctime
    return born


def _scan_commands(chunk: str, tests: int, waits: int):
    for line in transcripts.split_lines(chunk):
        if '"command"' not in line:
            continue
        for block in transcripts.content_blocks(transcripts.parse_line(line)):
            if not (isinstance(block, dict) and block.get("type") == "tool_use"):
                continue
            if block.get("name") not in ("Bash", "PowerShell"):
                continue
            cmd = (block.get("input") or {}).get("command")
            if isinstance(cmd, str):
                tests += 1 if TEST_RE.search(cmd) else 0
                waits += 1 if WAIT_RE.search(cmd) else 0
    return tests, waits


def _load_sidecar(side: Path, transcript: Path) -> dict:
    fresh = dict(FRESH_STATE)
    try:
        state = json.loads(side.read_text(encoding="utf-8"))
        st = transcript.stat()
        born = _creation_time(st)
        if not isinstance(state, dict):
            return fresh
        if any(type(state.get(k, v)) is not int for k, v in fresh.items()):
            return fresh
        if not 0 <= state.get("offset", 0) <= st.st_size:
            return fresh
        if born is not None and side.stat().st_mtime < born:
            return fresh
        return {**fresh, **state}
    except (TypeError, ValueError, KeyError, AttributeError, OSError):
        return fresh


def update_counts(transcript: Path, state: dict) -> dict:
    """Advance the sidecar state over the complete new lines of the transcript."""
    with open(transcript, "rb") as fh:
        fh.seek(state["offset"])
        data = fh.read()
    cut = data.rfind(b"\n") + 1
    chunk = data[:cut].decode("utf-8", errors="replace")
    state["tests"], state["waits"] = _scan_commands(chunk, state["tests"], state["waits"])
    seen = transcripts.last_usage(transcripts.split_lines(chunk))
    if seen is not None:
        state["ctx"] = seen
    state["offset"] += cut
    return state


def _level(value: int, warn: int, step: int) -> int:
    return 0 if value < warn else (value - warn) // max(step, 1) + 1


def _command_allowed(cmd: str) -> bool:
    """The WHOLE command is one plain git command: no chaining, redirect, substitution, escape or CR."""
    return bool(PLAIN_GIT_RE.match(cmd))


def _path_allowed(file_path, cwd=None) -> bool:
    """The real path of file_path lies under <cwd>/<one of ALLOWED_DIRS>/."""
    if not isinstance(file_path, str) or not file_path:
        return False
    base = cwd if isinstance(cwd, str) and cwd else os.getcwd()
    real = os.path.normcase(os.path.realpath(os.path.join(base, file_path)))
    for folder in ALLOWED_DIRS:
        root = os.path.normcase(os.path.realpath(os.path.join(base, folder)))
        if real.startswith(root + os.sep):
            return True
    return False


def stop_allows(tool_name, tool_input, cwd=None) -> bool:
    """The three moves that close a worker out at the STOP cap (edge vi)."""
    if tool_name == "SubagentHandback":
        return True
    ti = tool_input if isinstance(tool_input, dict) else {}
    if tool_name in ("Write", "Edit"):
        return _path_allowed(ti.get("file_path"), cwd)
    if tool_name in ("Bash", "PowerShell"):
        cmd = ti.get("command")
        return isinstance(cmd, str) and _command_allowed(cmd)
    return False


def stop_message(ctx: int, cap: int) -> str:
    return ("AGENT BUDGET STOP: this worker's context is %d tokens, the cap is %d. Every tool except the "
            "close-out moves is blocked. Do exactly three things: (1) commit the work in progress "
            "(git add / git commit: one plain git command, no shell syntax), (2) write your report into "
            "the path on the handoff: line of your dispatch, and when it has none into docs/tasks/handoffs/ "
            "or docs/tasks/specs/reports/ (a reading worker at STOP writes its report to the `handoff:` path of "
            "its dispatch; with no `handoff:` path the final message is the report), "
            "(3) hand back with SubagentHandback. "
            "The Lead relaunches a fresh agent with your report." % (ctx, cap))


def _warns(state: dict, ctx, is_worker: bool) -> list:
    out = []
    if is_worker:
        warn, step = _int_env("AGENT_BUDGET_WORKER_WARN", WORKER_WARN), 1 << 60
    else:
        warn = _int_env("AGENT_BUDGET_MAIN_WARN", MAIN_WARN)
        step = _int_env("AGENT_BUDGET_MAIN_STEP", MAIN_STEP)
    level = _level(ctx, warn, step) if ctx is not None else state["ctx_level"]
    if level > state["ctx_level"]:
        who = "worker" if is_worker else "main session"
        again = "" if is_worker else ", repeated every %d" % step
        duty = "" if is_worker else (" Write the compact snapshot (docs/tasks/compact-snapshots/) and tell the "
                                     "operator the one line (PROJECT.md).")
        out.append("AGENT BUDGET WARN: the %s context is %d tokens (warn from %d%s); every turn re-reads it. "
                   "Trim output, stop re-running after each edit, commit and hand over before the cap.%s"
                   % (who, ctx, warn, again, duty))
    state["ctx_level"] = level
    t_warn = _int_env("AGENT_BUDGET_TEST_RUNS_WARN", TEST_RUNS_WARN)
    t_level = _level(state["tests"], t_warn, _int_env("AGENT_BUDGET_TEST_RUNS_STEP", TEST_RUNS_STEP))
    if t_level > state["tests_level"]:
        out.append("AGENT BUDGET WARN: %d test runs, %d waits (sleep/until) in this transcript; one witness "
                   "run per round, no re-run after every edit." % (state["tests"], state["waits"]))
    state["tests_level"] = t_level
    return out


def _sidecar_path(transcript: Path) -> Path:
    base = Path(os.environ["AGENT_BUDGET_DIR"]) if os.environ.get("AGENT_BUDGET_DIR") else SIDECAR_DIR
    return base / (transcript.stem + ".json")


def evaluate(payload: dict):
    """(exit_code, stderr_text, warn_lines). Raises on any failure -- main() turns that into fail-open.
    tools/transcripts.py did not import: nothing can be measured -- (0, "", []); the one stderr line was
    printed at import when the module was broken (_transcripts_import_failed); silent when it was absent."""
    if transcripts is None:
        return 0, "", []
    path, is_worker = resolve_transcript(payload)
    if path is None or not path.is_file():
        return 0, "", []
    side = _sidecar_path(path)
    state = update_counts(path, _load_sidecar(side, path))
    tail = context_size(path)
    ctx = tail if tail is not None else (state["ctx"] or None)
    stop = _int_env("AGENT_BUDGET_WORKER_STOP", WORKER_STOP)
    over = is_worker and ctx is not None and ctx >= stop
    allowed = stop_allows(payload.get("tool_name"), payload.get("tool_input"), payload.get("cwd"))
    blocked = over and not allowed
    warns = [] if blocked else _warns(state, ctx, is_worker)
    try:
        side.parent.mkdir(parents=True, exist_ok=True)
        side.write_text(json.dumps(state), encoding="utf-8")
    except OSError as exc:
        _debug("sidecar not written: %s" % exc)
    return (2, stop_message(ctx, stop), []) if blocked else (0, "", warns)


def main() -> int:
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
        payload = json.loads(raw) if raw.strip() else None
        if not isinstance(payload, dict):
            return 0
        code, text, warns = evaluate(payload)
    except Exception as exc:  # fail-open: a budget hook never locks a session
        _debug("failed open: %s: %s" % (type(exc).__name__, exc))
        return 0
    if code == 2:
        sys.stderr.write(text + "\n")
        return 2
    if warns:
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "\n\n".join(warns)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
