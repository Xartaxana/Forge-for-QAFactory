"""tools/handoff_gate.py -- PreToolUse hook (Edit|Write): a READING worker writes exactly ONE file, the
path named on the `handoff:` line of its dispatch (t-744, node F5-1 N3, feature F19; spec
docs/tasks/specs/t-744-f5-1-handback-carrier.md section 3.1, decisions F-1 B, F-2 A, F-3, F-6 B).

WHY. A critic or a designer hands its whole report back as a file it writes itself (the file at
`handoff:` is what the coordinator reads at acceptance), instead of text the Lead retypes. That gives a
reading role the Write tool; this hook is the whole protection: it lets such a worker write the one
path of its dispatch and refuses every other Edit/Write.

WHO IS GATED. GATED_KINDS = critic, designer (the worker's kind is the sidecar meta's `agentType`,
transcripts.agent_type). Never gated: the main session (no `agent_id` in the payload), builder (writes its
owns and its report where it likes), scout (has no Write: its final message is the report), judge, Explore,
Plan, general-purpose (their tools: lines say what they may do). An UNKNOWN kind (no meta, or a bad one, F-6 B)
is decided by the dispatch text, as transcripts.is_writer does: an owns path in it -> a writing worker, pass;
none -> a reading one, gated like the kinds above against the report folders of every role.

THE ORDER (decide):
 1. the tool is not Write/Edit -> pass.            2. no agent_id -> pass.
 3. the worker's transcript = <subagents folder of transcript_path>/agent-<agent_id>.jsonl; its kind.
 4. a kind that is known and not gated -> pass.
 5. the dispatch text = transcripts.first_user_text; unreadable (no file, no user line, OSError) or its cut
    degraded -> REFUSED (an unknown is never a pass, FR-59). An unknown kind with an owns path -> pass.
 6. the candidates = dispatch_manifest.handoff_paths(cut) (the ONE reader of the dispatch's sections) that
    end in `.md` and whose parent ends with the kind's folder (dispatch_manifest.HANDOFF_DIRS; compared by
    TRAILING SEGMENTS, never from a cwd: a worker in a worktree and a path in the main tree are equal).
    A handoff path outside the folder is a mention, not a target and not counted. None -> REFUSED; two or
    more -> REFUSED naming them.
 7. the target (realpath + normcase of cwd/file_path) equals the one candidate -> pass (an Edit of the
    worker's own report file passes the same way), else REFUSED.

ERROR DIRECTION (F-2 A, the opposite of agent_budget): a failure of this code is NEVER a pass for a gated
worker. An exception in decide with an `agent_id` and tool Write/Edit -> exit 2 with a one-line reason; with
no `agent_id` or another tool -> exit 0. Unparsable stdin, a non-dict payload, a stdin timeout -> exit 0
(nothing is known about the call). So the main session is never blocked by this hook, and a builder is
blocked only by a broken transcripts import or a bug here (a broken dispatch_manifest import blocks only the
gated and unknown kinds: a builder must be able to repair that file); the refusal says so.

REFUSAL (exit 2, stderr; FR-1 / P15): what is wrong, what is expected, the door -- the whole report goes into
the final message and the coordinator extracts it (tools/handback_extract.py).

The hook is INERT until the Lead registers it in .claude/settings.json (matcher `Edit|Write`) and adds it to
tools/mechanism_gate.py MECHANISM_PREFIXES (CLAUDE.md rule 2: a self-activating enforcement file is placed on
its live path by the Lead). Like every chain link it keeps its own copy of the stdin deadline (SIBLING_MAP
axis 15) and does not import tools/streams.py.
"""

import json
import os
import re
import sys
import threading
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
# decide() raises on None: a broken import is a refusal for a worker, never a pass -- but each module on its
# own, so a broken dispatch_manifest leaves transcripts alive and a builder (kind read from it) still passes
try:
    import transcripts
except Exception:
    transcripts = None
try:
    import dispatch_manifest
except Exception:
    dispatch_manifest = None

WRITE_TOOLS = ("Write", "Edit")
GATED_KINDS = ("critic", "designer")  # F-1 B: scout has no Write, builder is never gated
SEGMENT_SPLIT_RE = re.compile(r"[\\/]+")

DOOR = ("put your whole report into your final message instead; the coordinator extracts it "
        "(tools/handback_extract.py)")
DOOR_RESEND = "ask the coordinator to re-send the dispatch with an owns: line (a writing worker) -- or: " + DOOR
REFUSAL_TEMPLATE = ("HANDOFF GATE: this {kind} worker may write only the one report file its dispatch names on "
                    "the handoff: line, inside {dirs}. Refused: {path} -- {reason}. Expected: {expected}. "
                    "Door: {door}.")
REASON_UNREADABLE = "the dispatch text could not be read"
REASON_NO_PATH = "no handoff path inside {dirs} in the dispatch"
REASON_MANY = "the dispatch names {n} handoff paths inside {dirs}: {paths}; exactly one is expected"
REASON_OTHER = "not the handoff path ({expected})"


def _refusal(kind, dirs, path, reason, expected, door=DOOR) -> str:
    return REFUSAL_TEMPLATE.format(kind=kind or "reading", dirs=dirs, path=path, reason=reason,
                                   expected=expected, door=door)


def _in_folder(path: str, folder: str) -> bool:
    """A `.md` file whose parent folder ENDS with the segments of `folder`: its direct child. A deeper
    subfolder (docs/tasks/specs/reviews for the folder docs/tasks/specs) is not the folder."""
    if not path.lower().endswith(".md"):
        return False
    segs = [os.path.normcase(s) for s in SEGMENT_SPLIT_RE.split(path) if s]
    want = [os.path.normcase(s) for s in folder.split("/")]
    parent = segs[:-1]
    return len(parent) >= len(want) and parent[-len(want):] == want


def _real(path: str, base: str) -> str:
    return os.path.normcase(os.path.realpath(os.path.join(base, path)))


def _worker_file(transcript_path, agent_id):
    """The worker's transcript path (not checked to exist); None when it cannot be composed."""
    name = transcripts.agent_file_name(agent_id)
    if name is None or not isinstance(transcript_path, str) or not transcript_path:
        return None
    return transcripts.subagents_dir_of(transcript_path) / name


def _dispatch_text(worker_file):
    """The dispatch prompt of the worker, None when it cannot be read."""
    if worker_file is None:
        return None
    try:
        return transcripts.first_user_text(worker_file)
    except OSError:
        return None


def _file_path(payload: dict) -> str:
    """tool_input.file_path when it is a non-empty str, else ""."""
    tool_input = payload.get("tool_input")
    path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    return path if isinstance(path, str) else ""


def decide(payload: dict):
    """(exit_code, stderr_message). Raises on any failure; main() turns that into a refusal for a worker."""
    if payload.get("tool_name") not in WRITE_TOOLS:
        return 0, ""
    agent_id = payload.get("agent_id")
    if not (isinstance(agent_id, str) and agent_id):
        return 0, ""
    if transcripts is None:
        raise RuntimeError("tools/transcripts.py did not import")
    worker_file = _worker_file(payload.get("transcript_path"), agent_id)
    kind = transcripts.agent_type(worker_file) if worker_file is not None else None
    kind = kind.strip().lower() if kind else None
    if kind is not None and kind not in GATED_KINDS:
        return 0, ""  # a builder is never refused for a broken dispatch_manifest: it must be able to repair it
    if dispatch_manifest is None:
        raise RuntimeError("tools/dispatch_manifest.py did not import")
    folders = [dispatch_manifest.HANDOFF_DIRS[kind]] if kind else list(dispatch_manifest.HANDOFF_DIRS.values())
    base = payload.get("cwd")
    return _gate(kind, folders, _dispatch_text(worker_file), _file_path(payload),
                 base if isinstance(base, str) and base else os.getcwd())


def _gate(kind, folders, text, path, base):
    """Steps 5-7 of the order above for a worker that is gated: (exit_code, message). `path` is the
    tool's file_path ("" when it has none), `text` the dispatch (None when unreadable)."""
    dirs = " or ".join(folders)
    shown = path or "(no file_path)"
    door = DOOR if kind else DOOR_RESEND
    cut = dispatch_manifest.section_cut(text) if text is not None else None
    if cut is None or cut.degraded:
        return 2, _refusal(kind, dirs, shown, REASON_UNREADABLE, "a dispatch whose text can be read", door)
    if kind is None and dispatch_manifest.owned_paths(cut):
        return 0, ""
    named = {}  # one path in two spellings (case, slashes, `..`) is one path: the first spelling is kept
    for p in dispatch_manifest.handoff_paths(cut):
        if any(_in_folder(p, f) for f in folders):
            named.setdefault(_real(p, base), p)
    cands = list(named.values())
    if not cands:
        return 2, _refusal(kind, dirs, shown, REASON_NO_PATH.format(dirs=dirs),
                           "one absolute .md path on the handoff: line of the dispatch, inside " + dirs, door)
    if len(cands) > 1:
        return 2, _refusal(kind, dirs, shown, REASON_MANY.format(n=len(cands), dirs=dirs, paths=", ".join(cands)),
                           "exactly one handoff: path inside " + dirs, door)
    if path and _real(path, base) == _real(cands[0], base):
        return 0, ""
    return 2, _refusal(kind, dirs, shown, REASON_OTHER.format(expected=cands[0]), cands[0], door)


# --- stdin deadline (a LOCAL copy of the bounded read, as in every chain link; SIBLING_MAP axis 15) ----------
# The deadline is a fixed constant: the OSLLM_STDIN_TIMEOUT override reader of the other links is not copied
# (a 15th copy of `_stdin_deadline_seconds` turns tools/dup_ratchet.py red, and this link's deadline is never tuned).

STDIN_DEADLINE_SECONDS = 10.0
_STDIN_DEADLINE_STATE = {"hit": False}


def _read_stdin_bytes_deadline():
    """(bytes, timed_out): stdin to EOF, but no longer than the deadline (a daemon thread does the blocking
    read, join(timeout) enforces the deadline; a TTY reads nothing)."""
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
    thread.join(STDIN_DEADLINE_SECONDS)
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    return (data if isinstance(data, bytes) else str(data).encode("utf-8", "replace")), False


def _emit(message: str) -> None:
    """The refusal to stderr as UTF-8 bytes (undecodable -> replaced): a console that cannot encode a path
    never turns a refusal into an exit 1. No stream reconfigure: SIBLING_MAP axis 15 census (test_streams S3)."""
    try:
        stream = getattr(sys.stderr, "buffer", None)
        if stream is None:
            sys.stderr.write(message + "\n")
        else:
            stream.write((message + "\n").encode("utf-8", errors="replace"))
        sys.stderr.flush()
    except Exception:
        pass


def _safe_kind(payload: dict):
    """The worker's kind for the exception refusal, best effort: None when it cannot be read (never raises)."""
    try:
        worker_file = _worker_file(payload.get("transcript_path"), payload.get("agent_id"))
        kind = transcripts.agent_type(worker_file) if worker_file is not None else None
        return kind.strip().lower() if kind else None
    except Exception:
        return None


def main() -> int:
    raw_bytes, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        _STDIN_DEADLINE_STATE["hit"] = True
        return 0
    try:
        payload = json.loads(raw_bytes.decode("utf-8", errors="replace"))
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0
    try:
        code, message = decide(payload)
    except Exception as exc:
        agent_id = payload.get("agent_id")
        if isinstance(agent_id, str) and agent_id and payload.get("tool_name") in WRITE_TOOLS:
            code = 2
            message = _refusal(_safe_kind(payload) or "unidentified", "its report folder", _file_path(payload) or "(the write)",
                               REASON_UNREADABLE + " (hook error: %s)" % type(exc).__name__,
                               "a hook that runs to the end", DOOR)
        else:
            return 0
    if message:
        _emit(message)
    return code


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:
        for _stream in (sys.stdout, sys.stderr):
            try:
                _stream.flush()
            except Exception:
                pass
        os._exit(_rc)
    sys.exit(_rc)
