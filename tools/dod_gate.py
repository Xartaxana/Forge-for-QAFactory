"""dod_gate.py -- SubagentStop hook that blocks a worker's stop if
there is no green verification run after its last edit (rule 11: DoD
witness). It reads the track that tools/dod_track.py (PostToolUse)
writes -- see that file's docstring for the full track format.

Contract (SubagentStop hook stdin JSON): base fields (session_id, cwd)
plus hook_event_name="SubagentStop", agent_id, agent_type,
stop_hook_active. "Blocked" for a command hook means exit code 2 (this
hook's own protocol) -- the same convention as every other hook in
this file set.

Logic (main()):
 1. Read the track .claude/dod_track/<session_id>.json. No file, or no
    edits belonging to this agent -- nothing to check (a typical
    scout/critic-class subagent that never edited a file) -- pass,
    exit 0, gate_state untouched.
 2. There were edits: compare max(edit ts) against max(GREEN run ts),
    BOTH filtered to this agent's own records (see evaluate() below).
    No green run, or the last green run is earlier than the last
    edit -> DoD invariant violated.
 3. No violation (a green run exists after the last edit) -> exit 0;
    a consecutive_blocks counter accumulated from earlier violations
    resets to 0 (a successful stop clears the safety valve).
 4. Violation: look at gate_state.consecutive_blocks (0 by default).
      - < 2: block (exit 2 + BLOCK_MESSAGE on stderr), counter += 1.
      - >= 2 (this would be the THIRD consecutive block): safety valve
        -- do NOT block (exit 0), write SAFETY_SKIP_MESSAGE to stderr,
        reset the counter to 0 (a new cycle starts), and record a
        "skipped_after_2_blocks" gate_log event (visible for later
        review -- the skip is a fact, not silently dropped).
    Both branches append a gate_log event ("blocked" |
    "skipped_after_2_blocks") under the "gate_log" key of the same
    track file, alongside "edits"/"runs"/"gate_state"; dod_track.py's
    own read-modify-write leaves unknown keys alone.

Per-agent filtering (evaluate()/decide() take an agent_id parameter):
this hook's invariant is scoped to records belonging to THIS worker --
a coordinator's own main-thread edits (agent_id is None) and another
parallel worker's edits are NOT visible to this evaluation. Without
this, a shared track file (session_id is common to the main thread and
every subagent) would let one worker's unreviewed edit block a
completely different worker's stop, or let the coordinator's own
unreviewed edits block a clean subagent that never touched a file
itself. The coordinator's own zone belongs entirely to
tools/main_gate.py (Stop) -- dod_gate.py never looks at it, at any
agent_id. If a SubagentStop payload carries no agent_id at all
(a defensive branch -- agent_id=None passed to evaluate()/decide()),
the fallback is "every non-main record" (any non-empty agent_id):
main-thread edits are still excluded, but different workers are not
told apart from each other in this fallback path.

Doc-only exemption: if EVERY edit belonging to this agent has a
file_path ending in .md/.json/.jsonl (DOC_ONLY_EXTENSIONS), the
invariant is skipped entirely -- no run is required at all, not just
"a run after the last edit". .jsonl is included because editing
logs/routing-log.jsonl is a routine operation on every acceptance
turn, and it is data, not code -- gated by its own dedicated validator,
not by a test run. An edit record with an unknown file_path (None --
either an older track predating this field, or a malformed payload) is
treated CONSERVATIVELY as NOT doc-only -- the one fail-CLOSED branch
in an otherwise fail-open file: mistaking "unknown" for "definitely
just docs" is riskier than one extra block.

consecutive_blocks is ALSO scoped per-agent (gate_state["per_agent"][
<agent_key>]), not a single session-global counter -- see the
_FALLBACK_AGENT_KEY docstring above for the class of bug this fixes
(one worker's exhausted safety valve silently spending itself on a
different worker's first-ever block in the same session). gate_log
entries carry ts and agent_id (the deciding worker's own) -- old
entries without these fields still read back without raising
(append-only, nothing here parses gate_log entries back
programmatically).

Doc-only "whole-or-nothing" over edits AFTER the last green run of
THIS agent (edits_after_green), not over its whole filtered history in
the track -- ported from the same fix in main_gate.evaluate() (see its
docstring for the full class-of-bug rationale: an early code edit used
to void the doc-only exemption forever, even after a green run and a
purely doc-only tail).

Handoff missing (B2, spec fg-context-and-hygiene): for EVERY stopping
agent, BEFORE the "no-edits" return, the worker's dispatch is read
(handoff_gate's readers; no second parser). When exactly one `handoff:`
path lies in a HANDOFF_DIRS folder and the track holds no Write/Edit by
THIS agent_id matching it (equal normcase(realpath), or equal trailing
segments from the folder down), the stop is blocked ONCE
(per_agent[<agent>]["handoff_missing_blocked"], separate from
consecutive_blocks, never reset; the block counts toward the safety
valve). Error direction: any doubt -- unreadable dispatch, import
failure, degraded cut, two or more candidates -- PASSES, never a second
block. main() saves the track when this block fires even if it did not
exist before.

Fail-open: a missing session_id, or an unparseable payload, exits 0
without side effects, same as the rest of this file set.
"""

import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path


def _now_iso() -> str:
    # Same format as tools/dod_track.py._now_iso().
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


# consecutive_blocks is counted PER-AGENT, not globally. Before this fix
# the counter was ONE per session (gate_state.consecutive_blocks) -- a
# worker X that exhausted the safety valve (2 blocks) let its own
# exhausted counter "spend itself" on a COMPLETELY DIFFERENT worker Y
# meeting a block for the first time in the same session (fail-open in
# the wrong direction -- Y would skip a verification it never actually
# passed). The counter now lives in
# gate_state["per_agent"][<agent_key>], independent per agent -- the
# same "own zone" semantics as evaluate()'s per-agent filter.
# _FALLBACK_AGENT_KEY is the key for the defensive branch (a payload
# with no agent_id at all -- see evaluate()/decide()).
_FALLBACK_AGENT_KEY = "__none__"


def _agent_state_key(agent_id) -> str:
    return agent_id if agent_id else _FALLBACK_AGENT_KEY


def _default_gate_state() -> dict:
    return {"consecutive_blocks": 0, "per_agent": {}}

BLOCK_MESSAGE = (
    "Stop blocked: there is no green verification run after the last "
    "edit. Run your DoD check (pytest / your verification command) "
    "and stop on green. Re-submission = repeat the path and the digest "
    "whole (or, with no handoff path, the full report); only your LAST "
    "message reaches the coordinator -- earlier text in this session is "
    "not delivered to it; a reference back to it is not a substitute)."
)

HANDOFF_MISSING_MESSAGE = (
    "HANDOFF MISSING: your dispatch names {path} and you did not write it. "
    "Write the report there; if the Write was refused, put the full report "
    "in your final message -- this block will not repeat."
)

# Once-key of the "handoff missing" block (B2): lives in the agent's own
# per_agent dict, SEPARATE from consecutive_blocks, never reset by a
# passing stop.
HANDOFF_ONCE_KEY = "handoff_missing_blocked"

SAFETY_SKIP_MESSAGE = (
    "dod_gate: safety valve triggered -- 2 consecutive blocks already "
    "happened in this session, the stop is allowed WITHOUT a green run "
    "(recorded in the track; this is not a substitute for verification)."
)

CONSECUTIVE_BLOCK_LIMIT = 2

# Extensions treated as "documentation/config, not code" -- an edit
# touching ONLY these does not require a verification run.
DOC_ONLY_EXTENSIONS = {".md", ".json", ".jsonl"}

# Known, code-less dotfiles WITHOUT a suffix (see main_gate.py for the
# full rationale and the final-list choice against this template's own
# actual files).
DOC_ONLY_DOTFILES = {".gitignore", ".gitattributes", ".editorconfig"}


def _is_doc_only_file(file_path) -> bool:
    if not isinstance(file_path, str) or not file_path:
        return False  # unknown path -- conservatively NOT doc-only
    path = Path(file_path)
    if path.name.lower() in DOC_ONLY_DOTFILES:
        return True
    return path.suffix.lower() in DOC_ONLY_EXTENSIONS


def _all_edits_doc_only(edits) -> bool:
    """True iff EVERY edit record has a known, doc-only (.md/.json/
    .jsonl) file_path. See the module docstring for the fail-closed
    rationale on an unknown file_path."""
    if not edits:
        return False
    return all(_is_doc_only_file(e.get("file_path")) for e in edits)


def _track_path(cwd: str, session_id: str) -> Path:
    return Path(cwd or ".") / ".claude" / "dod_track" / f"{session_id}.json"


def _load_track(path: Path) -> dict:
    if not path.exists():
        return {"edits": [], "runs": [], "gate_state": _default_gate_state()}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"edits": [], "runs": [], "gate_state": _default_gate_state()}
    if not isinstance(data, dict):
        return {"edits": [], "runs": [], "gate_state": _default_gate_state()}
    data.setdefault("edits", [])
    data.setdefault("runs", [])
    data.setdefault("gate_state", _default_gate_state())
    # Backward compat: an old track carries only a flat
    # "consecutive_blocks" (pre-per-agent) -- "per_agent" is added
    # ALONGSIDE it, the old field is left untouched.
    data["gate_state"].setdefault("consecutive_blocks", 0)
    data["gate_state"].setdefault("per_agent", {})
    return data


def _save_track(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def evaluate(track: dict, agent_id: str | None = None) -> tuple[bool, str]:
    """Pure invariant logic, no I/O -- directly testable.

    agent_id given (the normal SubagentStop path): edits and runs are
    filtered to records belonging to exactly this agent
    (e.get("agent_id") == agent_id) BEFORE the rest of the logic
    applies -- other workers' edits and main-thread edits (agent_id
    None/empty) are invisible to this evaluation.
    agent_id NOT given (None -- a defensive branch, a payload with no
    agent_id field): a conservative fallback, "every non-main record"
    (any non-empty agent_id) -- main-thread edits are still excluded,
    but different workers are not told apart from each other here.

    Returns (violation: bool, reason: str). reason is for debugging/
    tests only, not parsed by the caller.

    Doc-only "whole-or-nothing" over edits AFTER the last green run of
    THIS agent (edits_after_green), not over its whole filtered
    history in the track -- ported from the same fix in
    main_gate.evaluate() (see its docstring for the full class-of-bug
    rationale: an early code edit used to void the doc-only exemption
    forever, even after a green run and a purely doc-only tail)."""
    all_edits = track.get("edits") or []
    if agent_id:
        edits = [e for e in all_edits if e.get("agent_id") == agent_id]
    else:
        edits = [e for e in all_edits if e.get("agent_id")]
    if not edits:
        return False, "no-edits"

    all_runs = track.get("runs") or []
    if agent_id:
        runs = [r for r in all_runs if r.get("agent_id") == agent_id]
    else:
        runs = [r for r in all_runs if r.get("agent_id")]

    green_runs = [r for r in runs if r.get("outcome") == "green"]

    if not green_runs:
        if _all_edits_doc_only(edits):
            return False, "doc-only-edits-exempt"
        return True, "no-green-run"

    last_green_ts = max(r["ts"] for r in green_runs)
    edits_after_green = [e for e in edits if e["ts"] > last_green_ts]

    if not edits_after_green:
        return False, "green-after-last-edit"

    if _all_edits_doc_only(edits_after_green):
        return False, "doc-only-edits-exempt"

    return True, "green-before-last-edit"


def _segments(hg, path: str) -> list:
    return [os.path.normcase(s) for s in hg.SEGMENT_SPLIT_RE.split(path) if s]


def _written_paths(hg, track: dict, agent_id, base: str) -> list:
    """(real, path) of every Write/Edit record of THIS agent (the same
    per-agent filter as evaluate())."""
    out = []
    for e in track.get("edits") or []:
        mine = e.get("agent_id") == agent_id if agent_id else bool(e.get("agent_id"))
        fp = e.get("file_path")
        if mine and isinstance(fp, str) and fp:
            out.append((hg._real(fp, base), fp))
    return out


def handoff_written(track: dict, agent_id, candidate: tuple, base: str) -> bool:
    """True when this agent wrote the one candidate (path, folder, ...):
    equal normcase(realpath) values, OR equal trailing segments from the
    HANDOFF_DIRS folder down to the file name (a worktree copy matches the
    dispatch's path in the main clone). handoff_gate's own _real and
    SEGMENT_SPLIT_RE are the one reader (no copy); an unusable import
    -> True (pass)."""
    try:
        hg = _import_readers()[0]
    except Exception:
        return True
    path, folder = candidate[0], candidate[1]
    real = hg._real(path, base)
    tail = _segments(hg, folder) + _segments(hg, path)[-1:]
    for wreal, fp in _written_paths(hg, track, agent_id, base):
        if wreal == real:
            return True
        segs = _segments(hg, fp)
        if len(segs) >= len(tail) and segs[-len(tail):] == tail:
            return True
    return False


def _file_fresh(candidate: tuple, base: str) -> bool:
    """B-1: the candidate file exists and was modified no earlier than the
    worker's dispatch (candidate[2], epoch seconds; None = the start could
    not be read -> the file merely existing is enough)."""
    try:
        mtime = os.path.getmtime(os.path.join(base, candidate[0]))
    except OSError:
        return False
    start = candidate[2] if len(candidate) > 2 else None
    return start is None or mtime >= start


def _start_time(worker_file):
    """Epoch seconds of the first record's `timestamp` of the worker
    transcript, None when unreadable."""
    try:
        with open(worker_file, "r", encoding="utf-8") as fh:
            ts = json.loads(fh.readline()).get("timestamp")
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def _import_readers():
    """(handoff_gate, dispatch_manifest) with their own imports checked;
    raises when a reader is not usable (the caller passes, B2 error
    direction)."""
    tools_dir = str(Path(__file__).resolve().parent)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import handoff_gate
    import dispatch_manifest
    if handoff_gate.transcripts is None or handoff_gate.dispatch_manifest is None:
        raise RuntimeError("transcripts/dispatch_manifest did not import")
    return handoff_gate, dispatch_manifest


def named_handoffs(payload: dict, base: str) -> list:
    """The ONE handoff candidate of the stopping worker's dispatch as
    [(path, folder, start_epoch_or_None)], else []. Reads the dispatch through the readers
    handoff_gate uses (no second parser). May err toward [] (= pass):
    unreadable dispatch, import failure, degraded cut, two or more
    candidates -- with a stderr line where something failed."""
    try:
        agent_id = payload.get("agent_id")
        if not (isinstance(agent_id, str) and agent_id):
            return []
        tp = payload.get("transcript_path")
        atp = payload.get("agent_transcript_path")
        if not (isinstance(tp, str) and tp) and not (isinstance(atp, str) and atp):
            return []  # no transcript named: nothing to read, nothing failed
        hg, dm = _import_readers()
        if isinstance(atp, str) and atp:
            worker_file = Path(atp)  # the host names the worker's own file
        else:
            worker_file = hg._worker_file(tp, agent_id)
        text = hg._dispatch_text(worker_file)
        if text is None:
            sys.stderr.write("dod_gate: handoff check skipped -- dispatch unreadable\n")
            return []
        cut = dm.section_cut(text)
        if cut is None or cut.degraded:
            sys.stderr.write("dod_gate: handoff check skipped -- dispatch cut degraded\n")
            return []
        named = {}
        for p in dm.handoff_paths(cut):
            for folder in dm.HANDOFF_DIRS.values():
                if hg._in_folder(p, folder):
                    named.setdefault(hg._real(p, base), (p, folder))
                    break
        cands = list(named.values())
        if len(cands) != 1:
            return []
        start = _start_time(worker_file)
        return [(cands[0][0], cands[0][1], start)]
    except Exception as exc:
        sys.stderr.write("dod_gate: handoff check skipped -- %s: %s\n" % (type(exc).__name__, exc))
        return []


def _handoff_block(track, agent_id, agent_state, handoffs, base):
    """The path to report when the once-block is due, else None."""
    if not handoffs or len(handoffs) != 1 or agent_state.get(HANDOFF_ONCE_KEY):
        return None
    if agent_state.get("consecutive_blocks", 0) >= CONSECUTIVE_BLOCK_LIMIT:
        return None  # the safety valve is spent: the normal path decides
    if handoff_written(track, agent_id, handoffs[0], base):
        return None
    if _file_fresh(handoffs[0], base):
        return None  # B-1: written outside the track's cwd (a worktree worker, the main-clone path)
    return handoffs[0][0]


def decide(track: dict, agent_id: str | None = None, handoffs=None,
           base: str | None = None) -> tuple[int, str, dict]:
    """Pure decision logic after the track is loaded. agent_id passes
    straight through to evaluate() (see its docstring for the filter
    semantics) AND is used here for per-agent consecutive_blocks (see
    the _FALLBACK_AGENT_KEY docstring above). Returns (exit_code,
    stderr_message, updated_track); updated_track carries the updated
    gate_state/an appended gate_log event -- writing it to disk is
    main()'s job.

    handoffs: [(path, folder)] from named_handoffs() -- the worker's
    dispatch handoff candidates ([] / None = no check). The "handoff
    missing" check runs BEFORE evaluate() (so before its "no-edits"
    return): when the one candidate was not written by this agent, block
    ONCE (HANDOFF_ONCE_KEY, separate from consecutive_blocks, never
    reset); the block counts toward the safety valve."""
    gate_state = track.setdefault("gate_state", _default_gate_state())
    gate_state.setdefault("per_agent", {})
    key = _agent_state_key(agent_id)
    agent_state = gate_state["per_agent"].setdefault(key, {"consecutive_blocks": 0})
    missing = _handoff_block(track, agent_id, agent_state, handoffs, base or os.getcwd())
    if missing is not None:
        agent_state[HANDOFF_ONCE_KEY] = True
        agent_state["consecutive_blocks"] = agent_state.get("consecutive_blocks", 0) + 1
        track.setdefault("gate_log", []).append(
            {"action": "handoff_missing", "reason": missing, "ts": _now_iso(), "agent_id": agent_id}
        )
        return 2, HANDOFF_MISSING_MESSAGE.format(path=missing), track

    violation, reason = evaluate(track, agent_id)
    consecutive = agent_state.get("consecutive_blocks", 0)

    if not violation:
        if consecutive:
            agent_state["consecutive_blocks"] = 0
        return 0, "", track

    # gate_log entries carry ts (_now_iso) and agent_id -- backward
    # compat: old gate_log entries without these fields read back
    # without raising (append-only, nothing here parses them back).
    if consecutive >= CONSECUTIVE_BLOCK_LIMIT:
        agent_state["consecutive_blocks"] = 0
        # F2 (release-gate v0.8.1, ported from tools/dod_gate.py's own
        # attempt-2 fix, same class): a PERSISTENT fact in the agent's
        # OWN agent_state dict (the same dict "consecutive_blocks"
        # already lives in) -- the fact tools/session_context.py's
        # GATE BREAK-GLASS surfacing reads on the NEXT SessionStart.
        # agent_id is included IN THE VALUE (not only the per_agent
        # key) -- the fallback branch (agent_id=None) files entries
        # under _FALLBACK_AGENT_KEY ("__none__"), so the real agent_id
        # would otherwise be lost unless saved alongside explicitly.
        # Not erased by a later successful run: the "not violation"
        # branch above only ever resets "consecutive_blocks" of this
        # same agent_state, it never touches this key. A LIST
        # ("unsafe_completions"), not a single overwritable dict --
        # append, never overwrite, so a second (or later) valve trip by
        # the same agent in the same session does not silently erase
        # the first occurrence's fact.
        agent_state.setdefault("unsafe_completions", []).append(
            {"ts": _now_iso(), "reason": reason, "agent_id": agent_id}
        )
        track.setdefault("gate_log", []).append(
            {
                "action": "skipped_after_2_blocks",
                "reason": reason,
                "ts": _now_iso(),
                "agent_id": agent_id,
            }
        )
        return 0, SAFETY_SKIP_MESSAGE, track

    agent_state["consecutive_blocks"] = consecutive + 1
    track.setdefault("gate_log", []).append(
        {"action": "blocked", "reason": reason, "ts": _now_iso(), "agent_id": agent_id}
    )
    return 2, BLOCK_MESSAGE, track


def _reconfigure_stderr_utf8():
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _extract_agent_id_from_payload(payload: dict):
    """Reads the top-level "agent_id" payload field -- same "empty
    means unset" treatment as dod_track.py._extract_agent_id and
    main_gate.py's own main-entry check."""
    value = payload.get("agent_id")
    return value if isinstance(value, str) and value else None


# --- stdin deadline (P4 class; a LOCAL copy, no shared module -- the
# same helper toolkit/tools/owns_gate.py/dispatch_gate.py already carry)
# ------------------------------------------------------------------

_STDIN_DEADLINE_DEFAULT = 10.0
_STDIN_DEADLINE_MAX = 600.0
_STDIN_DEADLINE_ENV = "OSLLM_STDIN_TIMEOUT"


def _stdin_deadline_seconds():
    """Seconds to wait for stdin: env override, else the default.
    Invalid, non-numeric, <=0, or > _STDIN_DEADLINE_MAX all fall back to
    the default -- there is deliberately NO "0 = wait forever" mode (that
    would resurrect the exact hang this helper exists to close)."""
    try:
        value = float(os.environ.get(_STDIN_DEADLINE_ENV, ""))
    except (TypeError, ValueError):
        return _STDIN_DEADLINE_DEFAULT
    if not (0.0 < value <= _STDIN_DEADLINE_MAX):
        return _STDIN_DEADLINE_DEFAULT
    return value


def _read_stdin_bytes_deadline():
    """Returns (bytes, timed_out). Reads stdin to EOF, but no longer
    than the deadline. Cross-platform by construction: select/poll do
    not work on pipes on Windows, so a background daemon thread does
    the actual blocking read and the deadline is enforced via
    thread.join(timeout). A TTY returns b"" without reading anything.
    Any read error degrades to b"" (fail-open)."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return b"", False
    try:
        if stdin.isatty():
            return b"", False
    except Exception:
        pass
    stream = getattr(stdin, "buffer", stdin)
    box = {}

    def _reader():
        try:
            box["data"] = stream.read()
        except Exception:
            box["data"] = b""

    thread = threading.Thread(target=_reader, name="stdin-deadline", daemon=True)
    thread.start()
    thread.join(_stdin_deadline_seconds())
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8", "replace")
    return data, False


_STDIN_DEADLINE_MSG = "stdin deadline exceeded -- fail-open, payload discarded"

# A background reader thread may still be blocked deep in a platform
# read syscall at normal interpreter shutdown, which can crash the
# process ("Fatal Python error: _enter_buffered_busy") instead of
# exiting cleanly. main() itself is UNCHANGED (still a plain
# `return 0`, safe in-process); only the actual __main__ script-exit
# path below escalates to os._exit().
_STDIN_DEADLINE_STATE = {"hit": False}


def main() -> int:
    _reconfigure_stderr_utf8()

    # P4: byte-safe read via the stdin-deadline helper (replaces the
    # former direct sys.stdin.buffer.read() -- bounded by
    # OSLLM_STDIN_TIMEOUT instead of blocking forever with no EOF).
    raw_bytes, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        _STDIN_DEADLINE_STATE["hit"] = True
        sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
        return 0
    raw = raw_bytes.decode("utf-8", errors="replace")
    try:
        payload = json.loads(raw)
    except Exception:
        return 0

    session_id = payload.get("session_id")
    if not session_id:
        return 0

    cwd = payload.get("cwd") or "."
    path = _track_path(cwd, session_id)
    existed_before = path.exists()
    track = _load_track(path)

    agent_id = _extract_agent_id_from_payload(payload)
    handoffs = named_handoffs(payload, cwd)
    exit_code, message, updated_track = decide(track, agent_id, handoffs, cwd)

    # "No edits -> pass" (see evaluate()): if the track file didn't
    # exist before AND this call adds no edits, do nothing at all --
    # a scout/critic-class subagent that never touched a file should
    # not grow an empty .claude/dod_track/<session_id>.json. If the
    # file already existed (dod_track.py created it earlier), always
    # write, to keep gate_state/gate_log consistent. Exception (B2): a
    # "handoff missing" block must persist its once-key even on a track
    # that did not exist.
    once_fired = bool(
        updated_track["gate_state"]["per_agent"].get(_agent_state_key(agent_id), {}).get(HANDOFF_ONCE_KEY)
    )
    if existed_before or updated_track.get("edits") or once_fired:
        _save_track(path, updated_track)

    if message:
        sys.stderr.write(message + "\n")

    return exit_code


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:
        try:
            sys.stdout.flush()
        except Exception:
            pass
        try:
            sys.stderr.flush()
        except Exception:
            pass
        os._exit(_rc)
    sys.exit(_rc)
