"""tier_echo.py -- SubagentStop hook that prints the coordinator the
ACTUAL model(s) a finished subagent ran on, measured from its own jsonl
transcript -- a response to the class "a tier requirement with no code
cross-check" (code guarantees the ENCOUNTER with a measurement; the
session/coordinator still judges any discrepancy). This hook never
blocks anything and never argues with the session -- it just places the
measured fact in front of it.

SubagentStop PAYLOAD CONTRACT (verified empirically against the
installed harness): base fields (session_id, transcript_path, cwd,
prompt_id?) + hook_event_name="SubagentStop", stop_hook_active: bool,
agent_id, agent_transcript_path, agent_type, last_assistant_message?,
background_tasks?. `agent_transcript_path` is a REQUIRED field of the
SubagentStop event specifically -- so the finished subagent's
transcript path is built deterministically straight from
payload["agent_transcript_path"]; no guessing by mtime/glob is needed
or done.

IMPORTANT EMPIRICAL CAVEAT: the confirmed payload schema carries
neither a "model"/"model_id" field (the requested model) nor a
"description" field (the dispatch label's tier prefix, "haiku: ..." /
"opus: ..."). Both are fields of the Task/Agent tool's INPUT
(PreToolUse), not confirmed as part of the SubagentStop event. This
hook nonetheless supports comparing against payload["description"] IF
it carries a tier-prefixed label in the dispatch-label convention
("<word>: ..."): if the field is absent, the MISMATCH branch is simply
skipped (the measured part still prints, unflagged). On the real,
empirically-confirmed payload this branch will practically never fire
(the field isn't there) -- the code supports it anyway because the
comparison is cheap and harmless when the field is absent, and it costs
nothing to leave the door open for a harness that does add it.

OUTPUT CHANNEL: `hookSpecificOutput.additionalContext` on stdout, exit
0 -- the channel confirmed to actually reach the coordinator (bare
stderr at exit 0 is swallowed by the harness). The response shape
mirrors hygiene_gate.py's, adjusted for this hook's own event name:

  {"hookSpecificOutput": {"hookEventName": "SubagentStop",
                           "additionalContext": "<TIER ECHO line...>"}}

The previous stderr write is KEPT in addition (not replaced): it does
not hurt (nobody reads it, but it doesn't corrupt anything either), and
keeping it lowers the regression risk for any external consumer that
may already be parsing this hook's stderr. Both writes only happen when
counts is non-empty (main() step 4 below); on every silent branch
(malformed payload, no transcript_path, file didn't open, empty/all-
synthetic transcript) neither channel is touched at all.

main() logic:
 1. Byte-safe stdin read -> JSON. A parse failure (or payload not a
    dict) -> silent exit 0.
 2. agent_transcript_path = payload.get("agent_transcript_path") --
    must be a non-empty string; otherwise (missing, empty, not a
    string) -> silent exit 0 (guessing by another method is
    deliberately not done).
 3. Read the jsonl file line by line (byte-safe, errors="replace" --
    survives invalid UTF-8 BYTES in the file itself, not just stdin;
    through tools/transcripts.py, lines split on "\n" only);
    a missing/unopenable file -> silent exit 0. Malformed JSON lines
    are skipped without breaking the rest of the parse. For each line
    with type=="assistant" and a valid string message.model, NOT in
    SKIP_MODELS ("<synthetic>" -- harness-internal stop-sequence lines,
    not a real subagent turn) -- count a turn for that model (order of
    first appearance in the transcript = output order). A non-string/
    empty/synthetic model does not count as a turn (does not break the
    parse either).
 4. No counted model at all (empty/all-non-assistant transcript) ->
    silent exit 0 -- nothing to report.
 5. Builds the line "TIER ECHO (measured): <model>=<turns>[, ...]"; if
    the payload carries "description" in the dispatch-label convention
    ("<word>: ...", word being exactly one of haiku/sonnet/opus/fable)
    AND no measured model-string contains that word as a
    case-insensitive substring -- appends " MISMATCH vs declared
    '<word>'". The line goes through an ASCII sanitizer -- a local
    copy, not a shared import. The ONE cross-file import of this file
    is tools/transcripts.py (the shared reader of worker transcripts,
    B-467). WITHOUT it (absent or broken, t-859 F6-20) the hook has
    nothing to measure: it still reads stdin, prints nothing on stdout,
    exits 0 -- silent when the module is simply absent, ONE stderr line
    "tier_echo: tier echo off -- transcripts <class>: <message>" when it
    exists but does not import (no traceback; journal_echo imports this
    file, so a broken reader must not take the journal validation down
    with it); the sanitizers and the stdin helper stay local copies.
 6. Prints the line to stderr (kept, see "OUTPUT CHANNEL" above) AND
    prints the JSON {"hookSpecificOutput": {"hookEventName":
    "SubagentStop", "additionalContext": "<same line>"}} as one line
    on stdout -- the channel that actually reaches the coordinator.
    Exit 0 always. Any unexpected exception anywhere in main() is
    caught by ONE boundary and turned into a silent exit 0 (fail-open,
    the same principle as every hook in this toolkit)."""

import json
import os
import re
import sys
import threading
from pathlib import Path

def _transcripts_off_line(exc: Exception):
    """The ONE stderr line for a transcripts that EXISTS but does not import, or None when the module is
    simply absent (ModuleNotFoundError named transcripts: silent). The same rule as
    agent_budget._transcripts_import_failed / dispatch_gate._transcripts_import_failed (t-844 F6-9) -- a
    comment-named copy, not a shared helper: this hook is deployed beside its siblings with no other file
    (mechanism_gate's live-wiring net lists each file), and the wording is the hook's own. The message is
    squeezed to one ASCII line and cut, so the line stays under 200 characters on any console codepage."""
    if isinstance(exc, ModuleNotFoundError) and exc.name == "transcripts":
        return None
    detail = " ".join(str(exc).split())[:40].encode("ascii", "replace").decode("ascii")
    return "tier_echo: tier echo off -- transcripts %s: %s" % (type(exc).__name__, detail)


# Not printed here: journal_echo imports this file, and a message at import time would be a second line on
# its stderr. main() prints it, once.
transcripts = None
_TRANSCRIPTS_OFF_LINE = None
try:
    from tools import transcripts  # package-style
except ImportError:
    try:
        import transcripts  # sibling-module fallback (what the mechanism net's import walk sees)
    except Exception as _exc:  # absent here too, or present but broken
        _TRANSCRIPTS_OFF_LINE = _transcripts_off_line(_exc)
except Exception as _exc:  # present as a package but broken
    _TRANSCRIPTS_OFF_LINE = _transcripts_off_line(_exc)

KNOWN_TIER_WORDS = ("haiku", "sonnet", "opus", "fable")

# Harness-internal stop-sequence transcript lines carry
# model=="<synthetic>" -- not a real subagent turn, meaningless for the
# echo and would distort the turn count/model list. The set lives in
# tools/transcripts.py (a format fact of the transcript, shared by every reader);
# without the module nothing is measured, so the set is empty.
SKIP_MODELS = transcripts.SKIP_MODELS if transcripts is not None else frozenset()


def _ascii_sanitize(s: str, max_len: int = 80) -> str:
    """Local copy of the console-safety pattern used across this
    toolkit's hooks: any externally-sourced value gets its control
    chars stripped, non-ASCII replaced, and length capped. A copy, not
    an import -- see the module docstring (the one shared import is transcripts)."""
    s = str(s).strip()
    s = re.sub(r"[\x00-\x1f\x7f]", "", s)
    s = s.encode("ascii", "replace").decode("ascii")
    return s[:max_len]


def _extract_agent_transcript_path(payload: dict):
    """agent_transcript_path -- a field of the SubagentStop event (see
    module docstring for the confirmed schema). Returns None if the
    field is missing, empty, or not a string -- the caller then exits
    silently, without trying to guess the path another way (the
    contract deliberately forbids that)."""
    value = payload.get("agent_transcript_path")
    return value if isinstance(value, str) and value else None


def _extract_declared_tier(payload: dict):
    """Looks for a dispatch-label tier prefix in payload["description"]
    (the "haiku: ..." / "sonnet: ..." / "opus: ..." / "fable: ..."
    convention). Returns the word in lowercase only if the prefix up to
    the first colon matches exactly one of KNOWN_TIER_WORDS -- otherwise
    None (no colon at all, a prefix like "opus2" -- undeterminable, the
    MISMATCH branch is skipped entirely)."""
    description = payload.get("description")
    if not isinstance(description, str) or not description:
        return None
    if ":" not in description:
        return None
    prefix = description.split(":", 1)[0].strip().lower()
    if prefix in KNOWN_TIER_WORDS:
        return prefix
    return None


def iter_transcript_models(path: str):
    """Yields one model string per assistant turn of the transcript, in
    file order -- the stream is tools/transcripts.py's iter_models (the
    one reader of worker transcripts): a byte-safe read
    (errors="replace"), lines split on "\\n" only, a malformed or
    absurdly nested JSON line skipped silently without interrupting the
    rest of the parse. Line shape: top-level "type"=="assistant",
    "message"."model", with the SKIP_MODELS filter for synthetic lines.
    Lines with message.model missing/not a string/synthetic are skipped
    (not counted as a turn), without breaking the parse. An unreadable
    file raises OSError on the first next().

    Honest counting semantics: "=N" in the final line is a count of
    assistant-type JSONL lines in THIS transcript, not deduplicated by
    an API-level request id the way a cost-accounting report would --
    the set of models encountered plus a rough line count is enough for
    an echo to the coordinator; cost-grade deduplication is not needed
    here. Without the transcripts module: nothing to read, an empty stream."""
    if transcripts is None:
        return iter(())
    return transcripts.iter_models(path)


def count_models(models) -> dict:
    """Counts turns per model, PRESERVING first-appearance order
    (a plain Python 3.7+ dict, insertion order), for a deterministic
    build_line() output."""
    counts = {}
    for model in models:
        counts[model] = counts.get(model, 0) + 1
    return counts


def build_line(counts: dict, declared_tier) -> str:
    """Assembles the final line from the counted models (in counts
    order, i.e. first appearance) plus, if applicable, a MISMATCH
    suffix (only when declared_tier is set AND no measured model
    contains it as a case-insensitive substring)."""
    parts = [
        f"{_ascii_sanitize(model)}={count}" for model, count in counts.items()
    ]
    line = "TIER ECHO (measured): " + ", ".join(parts)

    if declared_tier:
        matched = any(declared_tier in model.lower() for model in counts)
        if not matched:
            line += f" MISMATCH vs declared '{_ascii_sanitize(declared_tier)}'"

    return line


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
    try:
        raw_bytes, timed_out = _read_stdin_bytes_deadline()
        if timed_out:
            _STDIN_DEADLINE_STATE["hit"] = True
            sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
            return 0
        if transcripts is None:  # nothing to measure with: one line when the module is broken, silence when absent
            if _TRANSCRIPTS_OFF_LINE:
                sys.stderr.write(_TRANSCRIPTS_OFF_LINE + "\n")
            return 0
        raw = raw_bytes.decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except Exception:
            return 0
        if not isinstance(payload, dict):
            return 0

        transcript_path = _extract_agent_transcript_path(payload)
        if not transcript_path:
            return 0

        try:
            models = list(iter_transcript_models(transcript_path))
        except OSError:
            return 0

        counts = count_models(models)
        if not counts:
            return 0

        declared_tier = _extract_declared_tier(payload)
        line = build_line(counts, declared_tier)

        sys.stderr.write(line + "\n")

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "additionalContext": line,
            }
        }
        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
        return 0
    except Exception:
        return 0


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
